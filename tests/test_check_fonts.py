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


def test_check_fonts_fails_on_fonts_swapped_across_families(copy_of_fonts):
    sans = copy_of_fonts / "CruorSansMono-Regular.woff2"
    lite = copy_of_fonts / "CruorLiteMono-Regular.woff2"
    held = sans.read_bytes()
    sans.write_bytes(lite.read_bytes())
    lite.write_bytes(held)

    result = check_fonts(copy_of_fonts)
    assert result.returncode != 0
    said = result.stderr.splitlines()
    # Each file now holds the other family's Regular, and says so of itself.
    assert any(
        line.startswith("CruorSansMono-Regular.woff2: family:")
        and "the font says 'Cruor Lite Mono'" in line
        for line in said
    ), result.stderr
    assert any(
        line.startswith("CruorLiteMono-Regular.woff2: family:")
        and "the font says 'Cruor Sans Mono'" in line
        for line in said
    ), result.stderr
    # Their styles agree, so nothing but the family is at fault.
    assert all(": family: " in line for line in said[:-1]), result.stderr


def change_in_rule(folder, file: str, old: str, new: str) -> None:
    """Change one declaration of the rule that names a font file."""
    css = folder / "fonts.css"
    text = css.read_text(encoding="utf-8")
    rule_start = text.index(f'src: url("{file}")')
    block_start = text.rindex("@font-face", 0, rule_start)
    block = text[block_start:rule_start]
    assert old in block
    text = text[:block_start] + block.replace(old, new) + text[rule_start:]
    css.write_text(text, encoding="utf-8", newline="\n")


def test_check_fonts_fails_on_wrong_family_in_rule(copy_of_fonts):
    change_in_rule(
        copy_of_fonts,
        "CruorSansMono-Bold.woff2",
        'font-family: "Cruor Sans Mono"',
        'font-family: "Cruor Lite Mono"',
    )

    result = check_fonts(copy_of_fonts)
    assert result.returncode != 0
    faults = result.stderr.splitlines()[:-1]
    assert (
        "CruorSansMono-Bold.woff2: family: the font says 'Cruor Sans Mono', "
        "its rule says 'Cruor Lite Mono'"
    ) in faults, result.stderr


def test_check_fonts_fails_on_wrong_weight_in_rule(copy_of_fonts):
    change_in_rule(
        copy_of_fonts,
        "CruorSansMono-Bold.woff2",
        "font-weight: 700",
        "font-weight: 400",
    )

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
