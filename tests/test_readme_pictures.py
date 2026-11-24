"""The README's pictures: that they are current, and that each stands alone."""

import re
import shutil
import subprocess
import sys

import pytest

from helpers import ROOT

README = (ROOT / "README.md").read_text(encoding="utf-8")
PICTURES = ROOT / "assets" / "readme"

# A heading as the README writes it: its level, its picture and its words.
HEADINGS = re.findall(
    r'^<h([1-3])><img src="assets/readme/([a-z0-9-]+\.svg)" alt="([^"]+)" '
    r'width="100%"></h\1>$',
    README,
    re.MULTILINE,
)


def draw(*arguments) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-I", str(ROOT / "tools" / "draw_readme.py"), *arguments],
        capture_output=True,
        text=True,
        check=False,
    )


@pytest.fixture
def copy_of_repository(tmp_path):
    """A copy of what the pictures are drawn from, and of the pictures, to
    spoil without harm."""
    shutil.copy(ROOT / "README.md", tmp_path / "README.md")
    shutil.copytree(ROOT / "fonts", tmp_path / "fonts")
    shutil.copytree(PICTURES, tmp_path / "assets" / "readme")
    return tmp_path


def test_readme_pictures_are_current():
    result = draw("--check")
    assert result.returncode == 0, result.stderr


def test_readme_pictures_check_passes_on_a_copy(copy_of_repository):
    result = draw("--check", str(copy_of_repository))
    assert result.returncode == 0, result.stderr


def test_readme_pictures_check_fails_on_a_changed_picture(copy_of_repository):
    picture = copy_of_repository / "assets" / "readme" / "the-fonts.svg"
    picture.write_text(
        picture.read_text(encoding="utf-8").replace("#0a0708", "#000000"),
        encoding="utf-8",
        newline="\n",
    )
    result = draw("--check", str(copy_of_repository))
    assert result.returncode == 1
    assert result.stderr.splitlines()[0] == "assets/readme/the-fonts.svg: not current"


def test_readme_pictures_check_fails_on_a_changed_heading(copy_of_repository):
    readme = copy_of_repository / "README.md"
    readme.write_text(
        readme.read_text(encoding="utf-8").replace('alt="Terms"', 'alt="The terms"'),
        encoding="utf-8",
        newline="\n",
    )
    result = draw("--check", str(copy_of_repository))
    assert result.returncode == 1
    assert result.stderr.splitlines()[0] == "assets/readme/terms.svg: not current"


def test_readme_pictures_check_fails_on_a_missing_picture(copy_of_repository):
    (copy_of_repository / "assets" / "readme" / "sigil.svg").unlink()
    result = draw("--check", str(copy_of_repository))
    assert result.returncode == 1
    assert result.stderr.splitlines()[0] == "assets/readme/sigil.svg: missing"


def test_readme_pictures_check_fails_on_a_picture_no_heading_names(
    copy_of_repository,
):
    kept = copy_of_repository / "assets" / "readme"
    shutil.copy(kept / "terms.svg", kept / "left-behind.svg")
    result = draw("--check", str(copy_of_repository))
    assert result.returncode == 1
    assert result.stderr.splitlines()[0] == (
        "assets/readme/left-behind.svg: no heading names it"
    )


def test_readme_pictures_are_drawn_the_same_twice(copy_of_repository):
    result = draw(str(copy_of_repository))
    assert result.returncode == 0, result.stderr
    for picture in sorted(PICTURES.iterdir()):
        again = copy_of_repository / "assets" / "readme" / picture.name
        assert again.read_bytes() == picture.read_bytes(), picture.name


def test_readme_headings_are_pictures():
    # Every heading is a picture, and no heading is left as plain Markdown.
    outside_blocks = re.sub(r"```.*?```", "", README, flags=re.DOTALL)
    assert re.findall(r"^#+ ", outside_blocks, re.MULTILINE) == []
    assert len(re.findall(r"^<h[1-6]", README, re.MULTILINE)) == len(HEADINGS)
    assert [level for level, _, _ in HEADINGS].count("1") == 1
    assert HEADINGS[0] == ("1", "masthead.svg", "The Cruor framework")
    assert [words for _, _, words in HEADINGS[1:]] == [
        "What is in it",
        "The fonts",
        "Using them in a page",
        "Taking a release into a build",
        "The tool",
        "Checking",
        "Terms",
    ]


def test_readme_shows_every_picture_and_no_other():
    shown = re.findall(r'<img src="([^"]+)"', README)
    assert len(shown) == len(set(shown))
    assert sorted(shown) == sorted(
        f"assets/readme/{picture.name}" for picture in PICTURES.iterdir()
    )
    # A picture with words in it says them in its `alt`; the one with none,
    # the sigil, has an empty one.
    for tag in re.findall(r"<img [^>]+>", README):
        said = re.search(r' alt="([^"]*)"', tag)
        assert said, tag
        assert bool(said.group(1)) != ("sigil.svg" in tag), tag


def test_readme_picture_names_its_words():
    # Each heading's picture carries the heading's words as its own title.
    for _, name, words in HEADINGS:
        picture = (PICTURES / name).read_text(encoding="utf-8")
        assert f"<title>{words}</title>" in picture, name


def test_readme_pictures_stand_alone():
    # A picture shown from another page may fetch nothing and run nothing,
    # so each is outlines and colours and no more: no text that needs a font,
    # no stylesheet, no script, and no address but the names within itself.
    for path in sorted(PICTURES.iterdir()):
        picture = path.read_text(encoding="utf-8")
        for refused in ["<text", "<style", "<script", "<image", "<foreignObject"]:
            assert refused not in picture, (path.name, refused)
        assert "font-family" not in picture, path.name
        assert re.findall(r'https?://[^"]+', picture) == [
            "http://www.w3.org/2000/svg"
        ], path.name
        for address in re.findall(r'href="([^"]*)"', picture):
            assert address.startswith("#"), (path.name, address)
        for address in re.findall(r"url\(([^)]*)\)", picture):
            assert address.startswith("#"), (path.name, address)
        assert "\r" not in picture, path.name
