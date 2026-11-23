"""The repository as git keeps it: line ends, and the crate's own particulars."""

import subprocess
import tomllib

from helpers import ROOT


def cargo_manifest() -> dict:
    return tomllib.loads((ROOT / "Cargo.toml").read_text(encoding="utf-8"))


def test_gitattributes_fixes_line_ends():
    lines = (ROOT / ".gitattributes").read_text(encoding="utf-8").splitlines()
    rules = [
        line.split() for line in lines if line.strip() and not line.startswith("#")
    ]
    assert ["*", "text=auto", "eol=lf"] in rules
    assert ["*.woff2", "binary"] in rules


def test_tracked_text_has_no_carriage_returns():
    # `-I` passes over binary files; `--cached` reads what git stores, not what
    # this system checked out.
    found = subprocess.run(
        ["git", "grep", "--cached", "-I", "-l", "-e", "\r"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert found.stdout.splitlines() == []
    # Exit 1 is git's "none found". Any other code is a search that did not
    # run, which finds nothing either.
    assert found.returncode == 1, found.stderr


def test_crate_version_is_first_release():
    assert cargo_manifest()["package"]["version"] == "0.1.0"
