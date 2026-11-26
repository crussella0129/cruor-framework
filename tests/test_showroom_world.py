"""The showroom's world: the statue weeping blood, and the stem of thorns.

The pictures are the showroom's own, drawn by `tools/draw_showroom.py` from
the maps of squares the front page keeps. They are read as text here, and
then seen in a browser on the page.
"""

import re
import shutil
import subprocess
import sys
from html.parser import HTMLParser

import pytest

import browser
import draw_readme
import draw_showroom
from helpers import ROOT, serve

SHOWROOM = ROOT / "showroom"
PAGE = (SHOWROOM / "index.html").read_text(encoding="utf-8")
STATUE = ["weeping-face.svg", "weeping-profile.svg"]
STEM = "briar-stem.svg"
BLOOD = "#3c0606"


def draw(*arguments) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-I", str(ROOT / "tools" / "draw_showroom.py"), *arguments],
        capture_output=True,
        text=True,
        check=False,
    )


@pytest.fixture(scope="module")
def engine():
    with browser.chromium() as found:
        yield found


@pytest.fixture(scope="module")
def address():
    with serve(ROOT) as (found, _):
        yield found


# -- read as text ---------------------------------------------------------------


def test_showroom_pictures_are_current(tmp_path):
    result = draw("--check")
    assert result.returncode == 0, result.stderr
    # They are the only pictures the showroom keeps.
    assert sorted(path.name for path in SHOWROOM.glob("*.svg")) == sorted(
        [*STATUE, STEM, draw_showroom.DOOR]
    )

    # A map that changes leaves its picture behind, and the check says which.
    shutil.copytree(ROOT / "assets" / "readme", tmp_path / "assets" / "readme")
    shutil.copytree(SHOWROOM, tmp_path / "showroom")
    # The door is drawn in the fonts and the look's colours.
    shutil.copytree(ROOT / "fonts", tmp_path / "fonts")
    shutil.copytree(ROOT / "look", tmp_path / "look")
    kept = tmp_path / "assets" / "readme" / "weeping-profile.txt"
    head, gap, rest = kept.read_text(encoding="utf-8").partition("\n\n")
    letter = head.splitlines()[0].split()[0]
    assert rest[0] == "."
    kept.write_text(head + gap + letter + rest[1:], encoding="utf-8", newline="\n")
    result = draw("--check", str(tmp_path))
    assert result.returncode != 0
    assert "showroom/weeping-profile.svg: not current" in result.stderr
    assert "weeping-face.svg" not in result.stderr


@pytest.mark.parametrize("name", [*STATUE, STEM])
def test_showroom_pictures_are_squares_and_nothing_else(name):
    text = (SHOWROOM / name).read_text(encoding="utf-8")
    # Squares, each a colour: no script, no letters, no picture within the
    # picture, and nothing fetched.
    for unwanted in ("<script", "<text", "<image", "<style", "href", "url("):
        assert unwanted not in text, unwanted
    drawn = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    assert set(re.findall(r"<(\w+)", drawn)) == {"svg", "path"}
    assert 'shape-rendering="crispEdges"' in drawn
    fills = set(re.findall(r'fill="(#[0-9a-f]{6})"', drawn))
    assert len(fills) == drawn.count("<path")

    if name == STEM:
        assert fills <= set(draw_readme.BRIAR_COLOURS.values())
        # The front page's briar, turned a quarter: as tall as that is wide.
        wide, tall = len(draw_readme.BRIAR), len(draw_readme.BRIAR[0])
    else:
        colours, rows = draw_showroom.kept(ROOT, name.removesuffix(".svg"))
        assert fills <= set(colours.values())
        # The blood is the colour the owner chose for it, wholly opaque.
        assert BLOOD in fills
        assert "opacity" not in drawn
        wide, tall = len(rows[0]), len(rows)
        # It says whose photograph it was made from, and on what terms.
        assert "Jörg Bittner Unna" in text and "CC BY 4.0" in text
    assert f'viewBox="0 0 {wide} {tall}"' in drawn


def test_stem_is_the_briar_turned_upright():
    briar = draw_readme.BRIAR
    stem = draw_showroom.upright(briar)
    assert len(stem) == len(briar[0]) and len(stem[0]) == len(briar)
    # Every square of the briar is in the stem, a quarter turn on.
    for row, line in enumerate(briar):
        for column, letter in enumerate(line):
            assert stem[column][len(briar) - 1 - row] == letter
    # Its head meets its foot, so that it climbs unbroken when repeated.
    assert sorted(set(stem[0]) - {"."}) and sorted(set(stem[-1]) - {"."})


class Read(HTMLParser):
    """The pictures a page shows, and the links in its foot."""

    def __init__(self):
        super().__init__()
        self.pictures = []
        self.links = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "img":
            self.pictures.append(attributes)
        if tag == "a":
            self.links.append(attributes.get("href", ""))


def test_showroom_credits_the_photographs():
    # The statue's pictures are made from another's photographs, offered on
    # terms that ask for their maker to be named wherever they are shown.
    found = Read()
    found.feed(PAGE)
    foot = PAGE[PAGE.index('<footer class="foot">') :]
    assert "Michelangelo's David" in foot
    assert "photographs by Jörg Bittner Unna" in foot
    for number in ("005", "014"):
        address = (
            "https://commons.wikimedia.org/wiki/File:%27David%27_by_"
            f"Michelangelo_FI_Acca_JBU_{number}.jpg"
        )
        assert address in found.links
    assert "https://creativecommons.org/licenses/by/4.0/" in found.links
    assert "no part of the kit" in foot
    # Each picture says what it shows to one who cannot see it.
    assert sorted(picture["src"] for picture in found.pictures) == STATUE
    for picture in found.pictures:
        assert len(picture["alt"]) > 40 and "blood" in picture["alt"].lower()


# -- seen in a browser ----------------------------------------------------------


def test_showroom_carries_the_front_pages_world(engine, address):
    with browser.opened(engine, address + "showroom/index.html", script=False) as page:
        found = page.evaluate(
            """() => {
                const box = el => { const r = el.getBoundingClientRect();
                    return {left: r.left, right: r.right, top: r.top + scrollY,
                        bottom: r.bottom + scrollY, wide: r.width, tall: r.height}; };
                const nave = document.querySelector('main');
                const stem = getComputedStyle(nave, '::before');
                return {
                    pictures: [...document.images].map(img => ({
                        src: img.getAttribute('src'), loaded: img.complete,
                        natural: [img.naturalWidth, img.naturalHeight],
                        box: box(img), within: img.closest('section').id})),
                    title: box(document.querySelector('h1')),
                    threshold: box(document.querySelector('.threshold')),
                    wing: box(document.querySelector('aside')),
                    nave: box(nave),
                    stem: {content: stem.content, image: stem.backgroundImage,
                        repeat: stem.backgroundRepeat, tall: parseFloat(stem.height),
                        wide: parseFloat(stem.width), press: stem.pointerEvents},
                    rooms: [...document.querySelectorAll('main > section')]
                        .map(room => box(room)),
                };
            }"""
        )
        face, profile = found["pictures"]

        # The statue, from two angles: its face over the threshold, and its
        # side in the reliquary. Each is loaded, and large.
        assert face["src"] == "weeping-face.svg" and face["within"] == ""
        assert profile["src"] == "weeping-profile.svg"
        assert profile["within"] == "reliquary"
        for picture, least in ((face, 600), (profile, 300)):
            assert picture["loaded"] and picture["natural"][0] > 0
            assert picture["box"]["wide"] >= least, picture
            # A square is never drawn smaller than it was made.
            assert picture["box"]["wide"] >= picture["natural"][0] / 4

        # The threshold lies across the whole place, above both the wing and
        # the nave, and the title is cut within it, over the foot of the
        # face, where the statue goes into the dark.
        threshold = found["threshold"]
        assert threshold["left"] <= found["wing"]["left"]
        assert threshold["right"] >= found["nave"]["right"]
        assert threshold["bottom"] <= min(found["wing"]["top"], found["nave"]["top"])
        title = found["title"]
        assert threshold["top"] <= title["top"] < title["bottom"] <= threshold["bottom"]
        middle = face["box"]["top"] + face["box"]["tall"] / 2
        assert title["top"] > middle
        assert abs(title["bottom"] - face["box"]["bottom"]) < 48

        # The stem of thorns climbs the nave's edge past every room, and
        # takes no press meant for the page.
        stem = found["stem"]
        assert stem["content"] != "none"
        assert stem["image"].endswith('/showroom/briar-stem.svg")')
        assert stem["repeat"] == "repeat-y" and stem["press"] == "none"
        assert stem["tall"] >= found["rooms"][-1]["bottom"] - found["rooms"][0]["top"]
        for room in found["rooms"]:
            assert room["left"] >= found["nave"]["left"] + stem["wide"]

        # The stem is drawn: its reds are on the page where it stands.
        nave = found["nave"]
        where = {"x": nave["left"], "y": nave["top"] + 96, "width": 36, "height": 96}
        seen = browser.pixels(page.screenshot(full_page=True, clip=where))
        reds = {
            browser.colour(colour)[:3] for colour in draw_readme.BRIAR_COLOURS.values()
        }
        assert len(reds & set(seen)) >= 4


def test_showroom_world_folds_on_a_narrow_window(engine, address):
    # On a narrow window nothing of the world pushes the page sideways.
    narrow = {"width": 390, "height": 800}
    context = engine.new_context(
        viewport=narrow, java_script_enabled=False, reduced_motion="reduce"
    )
    page = context.new_page()
    try:
        page.goto(address + "showroom/index.html")
        page.wait_for_load_state("networkidle")
        found = page.evaluate(
            """() => ({page: document.documentElement.scrollWidth,
                pictures: [...document.images].map(img =>
                    img.getBoundingClientRect().right),
                stem: getComputedStyle(document.querySelector('main'), '::before')
                    .content})"""
        )
    finally:
        context.close()
    assert found["page"] <= narrow["width"]
    assert all(right <= narrow["width"] for right in found["pictures"])
    assert found["stem"] == "none"
