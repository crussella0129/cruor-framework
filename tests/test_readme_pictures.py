"""The front page's picture: that it is current, says every word, and stands
alone."""

import collections
import re
import shutil
import subprocess
import sys

import pytest

import draw_readme
from helpers import ROOT

KEPT = ROOT / "assets" / "readme"
README = (ROOT / "README.md").read_text(encoding="utf-8")
TEXT = (KEPT / "text.md").read_text(encoding="utf-8")
PICTURE = (KEPT / "page.svg").read_text(encoding="utf-8")


def draw(*arguments) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-I", str(ROOT / "tools" / "draw_readme.py"), *arguments],
        capture_output=True,
        text=True,
        check=False,
    )


@pytest.fixture
def copy_of_repository(tmp_path):
    """A copy of what the page is drawn from, and of the page, to spoil
    without harm."""
    shutil.copy(ROOT / "README.md", tmp_path / "README.md")
    shutil.copytree(ROOT / "fonts", tmp_path / "fonts")
    shutil.copytree(KEPT, tmp_path / "assets" / "readme")
    return tmp_path


def change(path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    assert old in text
    path.write_text(text.replace(old, new), encoding="utf-8", newline="\n")


def test_readme_pictures_are_current():
    result = draw("--check")
    assert result.returncode == 0, result.stderr


def test_readme_pictures_check_passes_on_a_copy(copy_of_repository):
    result = draw("--check", str(copy_of_repository))
    assert result.returncode == 0, result.stderr


def test_readme_pictures_check_fails_on_a_changed_picture(copy_of_repository):
    change(copy_of_repository / "assets" / "readme" / "page.svg", "#0a0708", "#000000")
    result = draw("--check", str(copy_of_repository))
    assert result.returncode == 1
    assert result.stderr.splitlines()[0] == "assets/readme/page.svg: not current"


def test_readme_pictures_check_fails_on_changed_words(copy_of_repository):
    change(copy_of_repository / "assets" / "readme" / "text.md", "## Terms", "## Term")
    result = draw("--check", str(copy_of_repository))
    assert result.returncode == 1
    assert result.stderr.splitlines()[0] == "assets/readme/page.svg: not current"


def test_readme_pictures_check_fails_on_a_changed_readme(copy_of_repository):
    with (copy_of_repository / "README.md").open("a", encoding="utf-8") as readme:
        readme.write("\nA line the page does not draw.\n")
    result = draw("--check", str(copy_of_repository))
    assert result.returncode == 1
    assert result.stderr.splitlines()[0] == "README.md: not current"


def test_readme_pictures_check_fails_on_a_missing_picture(copy_of_repository):
    (copy_of_repository / "assets" / "readme" / "page.svg").unlink()
    result = draw("--check", str(copy_of_repository))
    assert result.returncode == 1
    assert result.stderr.splitlines()[0] == "assets/readme/page.svg: missing"


def test_readme_pictures_check_fails_on_a_picture_the_page_does_not_show(
    copy_of_repository,
):
    kept = copy_of_repository / "assets" / "readme"
    shutil.copy(kept / "page.svg", kept / "left-behind.svg")
    result = draw("--check", str(copy_of_repository))
    assert result.returncode == 1
    assert result.stderr.splitlines()[0] == (
        "assets/readme/left-behind.svg: the front page does not show it"
    )


def test_readme_pictures_are_drawn_the_same_twice(copy_of_repository):
    result = draw(str(copy_of_repository))
    assert result.returncode == 0, result.stderr
    for name in ["README.md", "assets/readme/page.svg"]:
        assert (copy_of_repository / name).read_bytes() == (ROOT / name).read_bytes()


def test_readme_refuses_markdown_it_does_not_read(copy_of_repository):
    # What the script cannot set, it does not set wrongly: it stops.
    change(
        copy_of_repository / "assets" / "readme" / "text.md",
        "## Terms",
        "## Terms\n\nA line with a `mark left open.",
    )
    result = draw("--check", str(copy_of_repository))
    assert result.returncode != 0
    assert "this is not read" in result.stderr


def test_readme_is_the_picture_and_nothing_else():
    # The front page is one picture, which is a link to its words as text,
    # and says in its `alt` what it is. Nothing is left for the host to set
    # in letters of its own.
    lines = [line for line in README.splitlines() if line]
    comment = README[: README.index("-->") + 3]
    assert comment.startswith("<!--")
    assert "assets/readme/text.md" in comment
    assert "python -I tools/draw_readme.py" in comment
    assert README == comment + "\n" + lines[-1] + "\n"
    shown = re.fullmatch(
        r'<a href="assets/readme/text\.md"><img src="assets/readme/page\.svg" '
        r'alt="([^"]+)" width="100%"></a>',
        lines[-1],
    )
    assert shown, lines[-1]
    alt = shown.group(1)
    assert alt.startswith("The Cruor Framework: ")
    assert "Cruentous Atonement" in alt
    assert "read the same words as text" in alt
    assert sorted(path.name for path in KEPT.iterdir()) == [
        "page.svg",
        "text.md",
        "weeping-face.txt",
        "weeping-profile.txt",
    ]


def test_readme_statue_pictures_are_maps_of_squares():
    # Each picture of the statue is kept as text: a letter a square, each
    # letter a colour, and `.` where the page's own stone shows. The page
    # draws them as squares, so they need no picture file to show.
    for name, wide, tall in [("weeping-face", 220, 125), ("weeping-profile", 130, 140)]:
        head, _, rest = (
            (KEPT / f"{name}.txt").read_text(encoding="utf-8").partition("\n\n")
        )
        colours = dict(line.split() for line in head.splitlines())
        assert all(re.fullmatch(r"#[0-9a-f]{6}", colour) for colour in colours.values())
        rows = rest.splitlines()
        assert len(rows) == tall, name
        assert {len(row) for row in rows} == {wide}, name
        assert set("".join(rows)) <= set(colours) | {"."}, name
        # The blood is the colour the owner chose for it, and is among the
        # squares.
        blood = [letter for letter, colour in colours.items() if colour == "#3c0606"]
        assert len(blood) == 1, name
        assert blood[0] in "".join(rows), name
    assert draw_readme.page(ROOT).shown == ["weeping-face", "weeping-profile"]
    assert draw_readme.HERO == "weeping-face"
    assert "<!-- picture weeping-profile -->" in TEXT


def test_readme_pictures_check_fails_on_a_missing_statue(copy_of_repository):
    (copy_of_repository / "assets" / "readme" / "weeping-profile.txt").unlink()
    result = draw("--check", str(copy_of_repository))
    assert result.returncode != 0
    assert "assets/readme/weeping-profile.txt: missing" in result.stderr


def test_readme_credits_the_photographs():
    # The statue's pictures are made from another's photographs, offered on
    # the condition that he is named, the licence is named, and the changes
    # are told.
    flowed = " ".join(TEXT.split())
    assert "photographs by Jörg Bittner Unna" in flowed
    for number in ("005", "014"):
        assert (
            f"[JBU {number}](https://commons.wikimedia.org/wiki/File:%27David%27_by_"
            f"Michelangelo_FI_Acca_JBU_{number}.jpg)" in TEXT
        )
    assert "[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)" in TEXT
    assert (
        "cut from its ground, darkened, given tears of blood and reduced to" in flowed
    )
    assert "are offered under CC BY 4.0 as well" in flowed
    assert "They are not part of a release." in flowed


def words_of(text: str) -> list[str]:
    """The words of the page's Markdown, with its marks taken off."""
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.DOTALL)
    text = re.sub(r"^```[a-z]*$", " ", text, flags=re.MULTILINE)
    text = re.sub(r"^\|[-|]+\|$", " ", text, flags=re.MULTILINE)
    kept = []
    in_code = False
    for line in text.split("\n"):
        if line.startswith("```"):
            in_code = not in_code
            continue
        if not in_code:
            line = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", line)
            line = re.sub(r"^#+ |^- |^\||\|$", " ", line)
            # A `|` between cells, and the marks of code, bold and italic.
            line = re.sub(r" \| |`|\*", " ", line)
        kept.extend(line.split())
    return kept


def test_readme_picture_says_every_word():
    # Everything the page's words say is drawn, and nothing else but what
    # the masthead and the specimen add.
    faces = draw_readme.Faces(ROOT)
    added = [draw_readme.LOOK, draw_readme.NOTE]
    for family in faces.families():
        added += [family, *draw_readme.STYLES]

    # The page draws a line in runs, a new run wherever the setting changes,
    # so a comma after a link is a run of its own. Each run is cut at its
    # marks to compare word with word.
    def words(texts: list[str]) -> collections.Counter:
        return collections.Counter(re.findall(r"[^\W_]+|[^\w\s]|_", " ".join(texts)))

    drawn = words(draw_readme.page(ROOT).said)
    expected = words(words_of(TEXT) + added)
    assert drawn == expected, (drawn - expected, expected - drawn)


def test_readme_picture_is_set_in_the_three_families():
    # The title is Cruor Thornamental Regular, the headings Cruor Lite
    # Regular, and the text Cruor Sans Regular with Cruor Sans Mono for code.
    assert draw_readme.TITLE == "Cruor Thornamental Regular"
    assert draw_readme.HEADINGS == "Cruor Lite Regular"
    assert draw_readme.RUNNING == "Cruor Sans Regular"
    assert draw_readme.FIXED == "Cruor Sans Mono"
    assert draw_readme.PROSE[0] >= 24


def test_readme_picture_has_one_ground():
    # The page is obsidian whoever looks at it: the picture paints its own
    # ground over its whole size, and asks nothing of the reader's theme.
    size = re.search(r'viewBox="0 0 (\d+) (\d+)"', PICTURE)
    whole = f'<rect width="{size.group(1)}" height="{size.group(2)}" fill="#0a0708"/>'
    assert whole in PICTURE
    assert PICTURE.index(whole) < PICTURE.index("<use ")
    assert "prefers-color-scheme" not in PICTURE


def test_readme_pictures_stand_alone():
    # A picture shown from another page may fetch nothing and run nothing,
    # so it is outlines and colours and no more: no text that needs a font,
    # no stylesheet, no script, and no address but the names within itself.
    for refused in ["<text", "<style", "<script", "<image", "<foreignObject"]:
        assert refused not in PICTURE, refused
    assert "font-family" not in PICTURE
    assert re.findall(r'https?://[^"]+', PICTURE) == ["http://www.w3.org/2000/svg"]
    for address in re.findall(r'href="([^"]*)"', PICTURE):
        assert address.startswith("#"), address
    for address in re.findall(r"url\(([^)]*)\)", PICTURE):
        assert address.startswith("#"), address
    assert "\r" not in PICTURE
