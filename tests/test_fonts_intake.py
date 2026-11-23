"""The fonts as they were taken in: which files, under which licence, and no others."""

import tomllib

from helpers import ROOT, tracked_files

FONTS = ROOT / "fonts"

STEMS = [
    "CruorSansRegular",
    "CruorLiteRegular",
    "CruorThornamentalRegular",
    "CruorSansMono",
    "CruorLiteMono",
    "CruorThornamentalMono",
    "CruorSansPixelated",
    "CruorPixelated",
]
STYLES = ["Regular", "Bold", "Italic", "BoldItalic"]
EXPECTED = sorted(f"{stem}-{style}.woff2" for stem in STEMS for style in STYLES)

COPYRIGHT = (
    "Copyright (c) 2026, Charles Russella (https://github.com/crussella0129), "
    "with Reserved Font Name Cruor."
)


def test_fonts_are_the_thirty_two():
    assert len(EXPECTED) == 32
    assert sorted(path.name for path in FONTS.glob("*.woff2")) == EXPECTED


def test_families_list_has_eight():
    families = tomllib.loads((FONTS / "families.toml").read_text(encoding="utf-8"))[
        "family"
    ]
    assert len(families) == 8
    for family in families:
        assert set(family) == {"name", "stem", "kind"}
        assert family["kind"] in {"proportional", "mono", "pixel"}
        assert family["name"].startswith("Cruor ")
    assert [family["stem"] for family in families] == STEMS
    assert len({family["name"] for family in families}) == 8


def test_ofl_text_and_copyright_line():
    text = (FONTS / "OFL.txt").read_text(encoding="utf-8")
    assert text.splitlines()[0] == COPYRIGHT
    assert "SIL OPEN FONT LICENSE Version 1.1 - 26 February 2007" in text
    # The licence's five conditions.
    conditions = text[text.index("PERMISSION & CONDITIONS") : text.index("TERMINATION")]
    for number in range(1, 6):
        assert f"\n{number}) " in conditions


def test_no_other_font_files_tracked():
    font_files = [
        name
        for name in tracked_files()
        if name.lower().endswith((".woff2", ".woff", ".ttf", ".otf"))
    ]
    assert sorted(font_files) == [f"fonts/{name}" for name in EXPECTED]
