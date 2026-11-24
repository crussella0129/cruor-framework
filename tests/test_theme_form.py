"""The write-up of the theme file's form: that it names all the file holds."""

import tomllib

from helpers import ROOT

THEME = tomllib.loads((ROOT / "look" / "theme.toml").read_text(encoding="utf-8"))
FORM = (ROOT / "look" / "THEME.md").read_text(encoding="utf-8")


def test_theme_form_names_every_key():
    # Every table of the theme file has a section of the write-up, and every
    # key of the table a row in it, so that a person can write another look
    # from the write-up alone.
    sections = {}
    name = None
    for line in FORM.splitlines():
        if line.startswith("## "):
            name = line[3:]
            sections[name] = []
        elif name is not None:
            sections[name].append(line)

    def rows(section: str) -> set[str]:
        assert section in sections, section
        return {
            line.split("|")[1].strip().strip("`")
            for line in sections[section]
            if line.startswith("| `")
        }

    at_the_top = {
        key for key, value in THEME.items() if not isinstance(value, dict | list)
    }
    assert rows("At the top") == at_the_top

    for table in ("font", "colour", "void", "stone", "measure"):
        assert rows(f"`[{table}]`") == set(THEME[table]), table

    levels = THEME["heading"]
    assert list(levels) == ["h1", "h2", "h3", "h4", "h5", "h6"]
    for level, settings in levels.items():
        assert rows("`[heading.h1]` to `[heading.h6]`") == set(settings), level

    # No table of the file is left without a section.
    tables = {key for key, value in THEME.items() if isinstance(value, dict | list)}
    written_up = {
        section.split("]")[0].strip("`[").split(".")[0]
        for section in sections
        if section.startswith("`[")
    }
    assert tables == written_up
