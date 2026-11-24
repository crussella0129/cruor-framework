"""Plain HTML dressed in the look, opened in a browser.

`tests/pages/plain.html` holds one of each plain thing and no class of its
own. It is served from the repository and read as a browser draws it.
"""

import shutil
import subprocess

import pytest

import browser
from helpers import ROOT, serve

LOOK = browser.theme()
PLAIN = "tests/pages/plain.html"
ROOT_SIZE = 16  # what a browser takes 1rem to be

HEADINGS = ["h1", "h2", "h3", "h4", "h5", "h6"]
PLAIN_THINGS = ["body", "h1", "p", "a", "code", "blockquote", "table", "hr"]

READ = """selector => {
    const s = getComputedStyle(document.querySelector(selector));
    return {family: s.fontFamily, weight: s.fontWeight, style: s.fontStyle,
        line: s.textDecorationLine, size: parseFloat(s.fontSize), colour: s.color,
        ground: s.backgroundColor};
}"""


@pytest.fixture(scope="module")
def engine():
    with browser.chromium() as found:
        yield found


@pytest.fixture(scope="module")
def address():
    with serve(ROOT) as (found, _):
        yield found


def family(named: str, look: dict = LOOK) -> str:
    """The family a font reference of the theme file comes to."""
    return look["font"].get(named, named)


def px(length: str) -> float:
    assert length.endswith("rem"), length
    return float(length.removesuffix("rem")) * ROOT_SIZE


def role(name: str) -> tuple:
    return browser.colour(LOOK["colour"][name])


def read(page, selector: str) -> dict:
    return page.evaluate(READ, selector)


def test_plain_html_is_dressed(engine, address):
    with browser.opened(engine, address + PLAIN) as page:
        # Running text: the text font, the inscription's colour, and large.
        paragraph = read(page, "#second")
        assert paragraph["family"].startswith(f'"{family("text")}"')
        assert browser.colour(paragraph["colour"]) == role("inscription")
        assert paragraph["size"] >= 24
        assert paragraph["size"] == px(LOOK["measure"]["inscription-size"])
        for selector in ("#item", "#quotation"):
            assert browser.colour(read(page, selector)["colour"]) == role("inscription")
            assert read(page, selector)["size"] >= 24

        # Each heading level as the theme file sets it.
        for level in HEADINGS:
            set_as = LOOK["heading"][level]
            found = read(page, f"#{level}")
            assert found["family"].startswith(f'"{family(set_as["font"])}"'), level
            assert found["weight"] == ("700" if set_as["bold"] else "400"), level
            assert found["style"] == ("italic" if set_as["italic"] else "normal"), level
            assert ("underline" in found["line"]) == set_as["underline"], level
            assert found["size"] == px(set_as["size"]), level

        # Small things speak in bone.
        for selector in ("#td", "#th", "#block"):
            assert browser.colour(read(page, selector)["colour"]) == role("text")
            assert read(page, selector)["size"] == px(LOOK["measure"]["interface-size"])
        # Code is in the code font, inline and in a block.
        for selector in ("#chip", "#block", "#block code"):
            assert read(page, selector)["family"].startswith(f'"{family("code")}"')
        # A link within running text, and one in running text of its own.
        assert browser.colour(read(page, "#link")["colour"]) == role("inscription-link")
        # The page itself: its ground, and bone for whatever is not running text.
        body = read(page, "body")
        assert browser.colour(body["ground"]) == role("page")
        assert browser.colour(body["colour"]) == role("text")


def test_ornaments_are_drawn(engine, address):
    with browser.opened(engine, address + PLAIN) as page:
        found = page.evaluate(
            """() => {
                const of = (selector, pseudo) =>
                    getComputedStyle(document.querySelector(selector), pseudo);
                const carved = selector => {
                    const s = of(selector);
                    return {clip: s.backgroundClip, image: s.backgroundImage,
                        fill: s.webkitTextFillColor};
                };
                const seal = of('#first', '::first-letter');
                const mark = of('#item', '::before');
                const sigil = of('#rule', '::after');
                const quote = of('#quotation');
                return {
                    h1: carved('#h1'), h2: carved('#h2'), h3: carved('#h3'),
                    h4: carved('#h4'),
                    seal: {size: parseFloat(seal.fontSize), float: seal.float,
                        colour: seal.color, family: seal.fontFamily},
                    text: parseFloat(of('#first').fontSize),
                    plain: parseFloat(of('#second', '::first-letter').fontSize),
                    list: of('#list').listStyleType,
                    mark: {content: mark.content, ground: mark.backgroundColor},
                    sigil: {content: sigil.content,
                        mask: sigil.maskImage || sigil.webkitMaskImage},
                    quote: {edge: quote.borderLeftWidth, image: quote.backgroundImage},
                    drop: of('#quotation', '::after').content,
                };
            }"""
        )
    # The greater headings are carved: a gradient clipped to their letters.
    for level in ("h1", "h2", "h3"):
        assert "text" in found[level]["clip"], level
        assert "linear-gradient" in found[level]["image"], level
        assert browser.colour(found[level]["fill"])[3] == 0, level
    assert "text" not in found["h4"]["clip"]
    # The seal: the first letter after the first heading, at its size, in the
    # seal's font; and no other paragraph has one.
    seal_size = LOOK["measure"]["seal-size"]
    assert found["seal"]["size"] == pytest.approx(seal_size * found["text"], abs=1)
    assert found["seal"]["float"] == "left"
    assert browser.colour(found["seal"]["colour"]) == role("heading-top")
    seal_font = family(LOOK["measure"]["seal-font"])
    assert found["seal"]["family"].startswith(f'"{seal_font}"')
    assert found["plain"] == found["text"]
    # A list's mark is the look's and not the browser's.
    assert found["list"] == "none"
    assert found["mark"]["content"] != "none"
    assert browser.colour(found["mark"]["ground"]) == role("heading-foot")
    # A rule draws the sigil from a drawing in the stylesheet.
    assert found["sigil"]["content"] != "none"
    assert found["sigil"]["mask"].startswith('url("data:image/svg+xml,')
    # A quotation carries a channel down its left edge, and a drop at its foot.
    assert found["quote"]["edge"] == "3px"
    assert "linear-gradient" in found["quote"]["image"]
    assert found["drop"] != "none"


def test_page_without_the_class_is_untouched(engine, address):
    def plain_things(page) -> dict:
        return {thing: read(page, thing) for thing in PLAIN_THINGS}

    with browser.opened(engine, address + PLAIN) as page:
        dressed = plain_things(page)
        # The same page with the class taken off...
        page.evaluate("document.body.removeAttribute('class')")
        without_class = plain_things(page)
        ground_layers = page.evaluate(
            "['::before', '::after']"
            ".map(pseudo => getComputedStyle(document.body, pseudo).content)"
        )
        # ...and again with no stylesheet linked at all.
        page.evaluate(
            "document.querySelectorAll('link[rel=stylesheet]').forEach(l => l.remove())"
        )
        without_stylesheets = plain_things(page)
    assert without_class == without_stylesheets
    assert ground_layers == ["none", "none"]
    # And the class does change every one of them, so the comparison is not
    # between two pages that were never dressed.
    for thing in PLAIN_THINGS:
        assert dressed[thing] != without_class[thing], thing


MOVING = """() => document.getAnimations()
    .filter(moving => moving.playState === 'running')
    .map(moving => moving.animationName || moving.transitionProperty)"""


def test_look_moves_unless_asked_to_be_still(engine, address):
    with browser.opened(engine, address + PLAIN, still=False) as page:
        moving = page.evaluate(MOVING)
        assert "cruor-candle" in moving and "cruor-heartbeat" in moving
    with browser.opened(engine, address + PLAIN) as page:
        assert page.evaluate(MOVING) == []


def test_nothing_is_in_passage_when_stillness_is_asked(engine, address):
    # With a transition left in, a colour read just after a state changes
    # could be one in between. Under stillness nothing has a transition of
    # any length, nor an animation waiting to run.
    with browser.opened(engine, address + PLAIN) as page:
        lasting = page.evaluate(
            """() => {
                const found = [];
                const zero = text =>
                    text.split(',').every(part => parseFloat(part) === 0);
                for (const el of document.body.querySelectorAll('*')) {
                    for (const pseudo of [null, '::before', '::after']) {
                        const s = getComputedStyle(el, pseudo);
                        if (!zero(s.transitionDuration) || s.animationName !== 'none') {
                            found.push(el.tagName + (pseudo || ''));
                        }
                    }
                }
                for (const pseudo of ['::before', '::after']) {
                    const s = getComputedStyle(document.body, pseudo);
                    if (s.animationName !== 'none') found.push('body' + pseudo);
                }
                return found;
            }"""
        )
    assert lasting == []


def test_look_prints_plain(engine, address):
    with browser.opened(engine, address + PLAIN) as page:
        page.emulate_media(media="print")
        found = page.evaluate(
            """() => {
                const of = (selector, pseudo) =>
                    getComputedStyle(document.querySelector(selector), pseudo);
                const letters = selector => {
                    const s = of(selector);
                    return {colour: s.color, fill: s.webkitTextFillColor,
                        shadow: s.textShadow, image: s.backgroundImage,
                        filter: s.filter, ground: s.backgroundColor};
                };
                const seal = of('#first', '::first-letter');
                return {
                    body: letters('body'),
                    things: ['#h1', '#h3', '#h5', '#second', '#item', '#quotation',
                        '#link', '#chip', '#block', '#td', '#th'].map(letters),
                    hidden: [
                        getComputedStyle(document.body, '::before').display,
                        getComputedStyle(document.body, '::after').display,
                        of('#rule', '::after').display,
                        of('#quotation', '::after').display,
                        of('#item', '::before').display,
                    ],
                    seal: {colour: seal.color, shadow: seal.textShadow},
                };
            }"""
        )
    black, white = (0, 0, 0, 1.0), (255, 255, 255, 1.0)
    assert browser.colour(found["body"]["ground"]) == white
    assert browser.colour(found["body"]["colour"]) == black
    for thing in found["things"]:
        assert browser.colour(thing["colour"]) == black
        assert browser.colour(thing["fill"]) == black
        assert thing["shadow"] == "none" and thing["image"] == "none"
        assert thing["filter"] == "none"
        assert browser.colour(thing["ground"])[3] == 0
    # The stone, the candle, the sigil, the drop and the lozenge are gone.
    assert found["hidden"] == ["none"] * 5
    assert browser.colour(found["seal"]["colour"]) == black
    assert found["seal"]["shadow"] == "none"


@pytest.mark.parametrize(
    ("setting", "written", "changed", "reads"),
    [
        ("size", 'size = "2.25rem"', 'size = "5rem"', ("size", 80.0)),
        ("font", 'font = "heading"', 'font = "code"', ("family", "code")),
        ("weight", "bold = false", "bold = true", ("weight", "700")),
        ("slant", "italic = false", "italic = true", ("style", "italic")),
        ("underline", "underline = false", "underline = true", ("line", "underline")),
    ],
)
def test_theme_changes_a_heading(engine, tmp_path, setting, written, changed, reads):
    # A copy of what a page takes the look from, with one setting of the
    # second level changed in the theme file and the tokens made again by
    # the tool. That heading shows the change, and its neighbours do not.
    for folder in ("fonts", "look"):
        shutil.copytree(ROOT / folder, tmp_path / folder)
    (tmp_path / "tests" / "pages").mkdir(parents=True)
    shutil.copy(ROOT / PLAIN, tmp_path / PLAIN)

    theme_file = tmp_path / "look" / "theme.toml"
    text = theme_file.read_text(encoding="utf-8")
    start = text.index("[heading.h2]")
    end = text.index("[heading.h3]")
    table = text[start:end]
    assert table.count(written) == 1, written
    theme_file.write_text(
        text[:start] + table.replace(written, changed) + text[end:],
        encoding="utf-8",
        newline="\n",
    )
    made = subprocess.run(
        ["cargo", "run", "--quiet", "--", "--root", str(tmp_path), "look"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert made.returncode == 0, made.stderr

    with serve(ROOT) as (as_written, _), serve(tmp_path) as (as_changed, _):
        with browser.opened(engine, as_written + PLAIN) as page:
            before = {level: read(page, f"#{level}") for level in HEADINGS}
        with browser.opened(engine, as_changed + PLAIN) as page:
            after = {level: read(page, f"#{level}") for level in HEADINGS}

    key, expected = reads
    if key == "family":
        assert after["h2"][key].startswith(f'"{family(expected)}"')
    elif key == "line":
        assert expected in after["h2"][key]
    else:
        assert after["h2"][key] == expected
    assert after["h2"][key] != before["h2"][key], setting
    # Nothing else of that heading changed, and no other heading changed.
    for other in set(before["h2"]) - {key}:
        assert after["h2"][other] == before["h2"][other], other
    for level in HEADINGS:
        if level != "h2":
            assert after[level] == before[level], level
