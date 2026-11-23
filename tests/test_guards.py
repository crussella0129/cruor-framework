"""The guard script: that it runs every check, and stops when one fails.

No real check is run here. Each command the script calls is replaced by a
stand-in that records how it was called, so the tests are quick and the
script, which itself runs these tests, is never run for real from within
them.
"""

import os
import subprocess

import pytest

from helpers import ROOT, find_bash

# Every command the guard script runs, in its order.
CHECKS = [
    "cargo fmt --check",
    "cargo clippy --all-targets -- -D warnings",
    "cargo test",
    "ruff format --check",
    "ruff check",
    "python -I tools/check_fonts.py fonts",
    "pytest",
]

STAND_IN = """#!/usr/bin/env bash
# A stand-in for a real check. It records how it was called, and fails only
# when it is the call the test names.
call="$(basename "$0") $*"
call="${call% }"
printf '%s\\n' "$call" >> "$STAND_IN_LOG"
if [ "$call" = "$STAND_IN_FAILS" ]; then exit 1; fi
exit 0
"""


def run_guards(tmp_path, fails: str) -> tuple[int, list[str]]:
    """Run the guard script over stand-ins; give its exit code and the calls made."""
    stand_ins = tmp_path / "stand-ins"
    stand_ins.mkdir()
    for name in sorted({check.split()[0] for check in CHECKS}):
        (stand_ins / name).write_text(STAND_IN, encoding="utf-8", newline="\n")
        (stand_ins / name).chmod(0o755)
    log = tmp_path / "calls.log"
    log.write_text("", encoding="utf-8")
    environment = dict(os.environ)
    environment["PATH"] = str(stand_ins) + os.pathsep + environment["PATH"]
    environment["STAND_IN_LOG"] = str(log)
    environment["STAND_IN_FAILS"] = fails
    result = subprocess.run(
        [find_bash(), "tools/run-guards.sh"],
        cwd=ROOT,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode, log.read_text(encoding="utf-8").splitlines()


def test_guards_run_every_check(tmp_path):
    status, calls = run_guards(tmp_path, fails="none of them")
    assert status == 0
    assert calls == CHECKS


@pytest.mark.parametrize("failing", CHECKS)
def test_guards_fail_when_any_check_fails(tmp_path, failing):
    status, calls = run_guards(tmp_path, fails=failing)
    assert status != 0
    # The run stops at the failing check: it is the last call made.
    assert calls == CHECKS[: CHECKS.index(failing) + 1]
