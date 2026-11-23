"""The check that each font is what its rule says it is."""

import shutil
import subprocess
import sys

import pytest

from helpers import ROOT
from test_guards import CHECKS, run_guards

FONTS = ROOT / "fonts"
CHECK_FONTS = "python -I tools/check_fonts.py fonts"


def check_fonts(folder) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-I", str(ROOT / "tools" / "check_fonts.py"), str(folder)],
        capture_output=True,
        text=True,
        check=False,
    )


@pytest.fixture
def copy_of_fonts(tmp_path):
    """A copy of the fonts' folder, to spoil without harm."""
    return shutil.copytree(FONTS, tmp_path / "fonts")


def test_check_fonts_passes_on_repository():
    result = check_fonts(FONTS)
    assert result.returncode == 0, result.stderr


def test_check_fonts_fails_on_swapped_fonts(copy_of_fonts):
    bold = copy_of_fonts / "CruorLiteRegular-Bold.woff2"
    italic = copy_of_fonts / "CruorLiteRegular-Italic.woff2"
    held = bold.read_bytes()
    bold.write_bytes(italic.read_bytes())
    italic.write_bytes(held)

    result = check_fonts(copy_of_fonts)
    assert result.returncode != 0
    said = result.stderr.splitlines()
    # The file named -Bold now holds the Italic, and says so of itself.
    assert any(
        line.startswith("CruorLiteRegular-Bold.woff2: style:") and "'Italic'" in line
        for line in said
    ), result.stderr
    assert any(
        line.startswith("CruorLiteRegular-Bold.woff2: weight:") for line in said
    ), result.stderr
    assert any(
        line.startswith("CruorLiteRegular-Italic.woff2: slant:") for line in said
    ), result.stderr
    # No other family is named.
    assert all("CruorLiteRegular-" in line for line in said[:-1]), result.stderr


def test_check_fonts_fails_on_wrong_weight_in_rule(copy_of_fonts):
    css = copy_of_fonts / "fonts.css"
    text = css.read_text(encoding="utf-8")
    rule_start = text.index('src: url("CruorSansMono-Bold.woff2")')
    block_start = text.rindex("@font-face", 0, rule_start)
    block = text[block_start:rule_start]
    assert "font-weight: 700" in block
    text = (
        text[:block_start]
        + block.replace("font-weight: 700", "font-weight: 400")
        + text[rule_start:]
    )
    css.write_text(text, encoding="utf-8", newline="\n")

    result = check_fonts(copy_of_fonts)
    assert result.returncode != 0
    faults = result.stderr.splitlines()[:-1]
    assert faults == [
        "CruorSansMono-Bold.woff2: weight: the font says 700, its rule says 400"
    ]


def test_guards_run_check_fonts(tmp_path):
    assert CHECK_FONTS in CHECKS
    status, calls = run_guards(tmp_path, fails=CHECK_FONTS)
    assert status != 0
    assert calls[-1] == CHECK_FONTS
