"""The means of checking a page in a browser, checked on pages made for it.

Each page is written by its test into a temporary folder and served from
there. None is tracked, the one with a script in it among them.
"""

import pytest

import browser
from helpers import serve

LOOK = browser.theme()


@pytest.fixture(scope="module")
def engine():
    with browser.chromium() as found:
        yield found


def page_of(tmp_path, body: str, style: str = "", body_class: str = "") -> None:
    (tmp_path / "index.html").write_text(
        f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>A page made for a test</title>
<style>
  html, body {{ margin: 0; }}
  body {{ font: 24px/1.5 sans-serif; padding: 40px; }}
{style}
</style>
</head>
<body class="{body_class}">
{body}
</body>
</html>
""",
        encoding="utf-8",
    )


def test_contrast_helper_knows_the_ratio():
    black, white = (0, 0, 0), (255, 255, 255)
    assert browser.ratio(black, white) == pytest.approx(21)
    assert round(browser.ratio((119, 119, 119), white), 2) == 4.48
    assert browser.ratio(white, black) == browser.ratio(black, white)
    assert browser.colour("#777777") == (119, 119, 119, 1.0)
    assert browser.colour("rgba(213, 2, 16, 0.2)") == (213, 2, 16, 0.2)
    assert browser.colour("rgb(10, 7, 8)") == (10, 7, 8, 1.0)


def test_contrast_helper_lays_alpha_over_ground():
    # Half-clear white on black is mid grey on black.
    black = (0, 0, 0)
    half_white = (255, 255, 255, 0.5)
    assert browser.laid(half_white, black) == (127.5, 127.5, 127.5)
    assert browser.contrast(half_white, black) == pytest.approx(
        browser.ratio((127.5, 127.5, 127.5), black)
    )


def test_ground_is_read_from_a_picture(engine, tmp_path):
    page_of(
        tmp_path,
        """
<div class="flat"><p id="glowing">Lettering with a light of its own.</p></div>
<div class="flat"><input id="field" value="written in"></div>
<div class="flat"><input id="empty" placeholder="words shown when empty"></div>
<div class="flat">
  <select id="choice"><option>one</option><option>two</option></select>
</div>
""",
        """
  .flat { background: #123456; padding: 20px; margin: 0 0 20px; }
  #glowing { margin: 0; color: #ffffff;
    text-shadow: 0 0 12px #ff0000, 0 0 2px #ff0000; }
  input, select { font: inherit; color: #ffffff; background: #204060;
    border: 6px solid #ff00ff; padding: 10px; appearance: none; }
  #empty::placeholder { color: #c0c0c0; }
  ::selection { color: #000000; background: #ffee00; }
""",
    )
    with serve(tmp_path) as (address, _), browser.opened(engine, address) as page:
        # The glow is the letter's own and is taken off with its colour.
        assert browser.ground(page, "#glowing") == {(0x12, 0x34, 0x56)}
        assert browser.lettering(page, "#glowing") == (255, 255, 255, 1.0)
        assert browser.stands_at(page, "#glowing") == pytest.approx(
            browser.ratio((255, 255, 255), (0x12, 0x34, 0x56))
        )
        # The lettering is back once the ground is read.
        assert (
            page.evaluate("getComputedStyle(document.querySelector('#glowing')).color")
            == "rgb(255, 255, 255)"
        )
        # A control has no element for its text: its content box is read,
        # which leaves its border out.
        for control in ("#field", "#empty", "#choice"):
            assert browser.ground(page, control) == {(0x20, 0x40, 0x60)}, control
        # An empty field's lettering is the words it shows then.
        assert browser.lettering(page, "#empty") == (192, 192, 192, 1.0)
        assert browser.lettering(page, "#field") == (255, 255, 255, 1.0)
        # The keyboard come to a field, a browser selects its words: they are
        # then lettered and grounded as selected words are.
        for _ in range(5):
            page.keyboard.press("Tab")
            if page.evaluate("document.activeElement.id") == "field":
                break
        assert page.evaluate("document.activeElement.id") == "field"
        assert browser.lettering(page, "#field") == (0, 0, 0, 1.0)
        assert browser.ground(page, "#field") >= {(0xFF, 0xEE, 0x00)}


def test_ground_read_sees_a_gradient(engine, tmp_path):
    page_of(
        tmp_path,
        '<p id="on-a-gradient">From dark at one end to light at the other.</p>',
        """
  #on-a-gradient { margin: 0; padding: 20px; color: #ffffff; width: 600px;
    background: linear-gradient(90deg, #000000, #888888); }
""",
    )
    with serve(tmp_path) as (address, _), browser.opened(engine, address) as page:
        seen = browser.ground(page, "#on-a-gradient")
        assert len(seen) > 20, "many tones, not one"
        # White lettering is held against the light end, where it reads worst.
        lightest = max(seen, key=browser.luminance)
        assert browser.stands_at(page, "#on-a-gradient") == pytest.approx(
            browser.ratio((255, 255, 255), lightest)
        )
        assert browser.stands_at(page, "#on-a-gradient") < browser.ratio(
            (255, 255, 255), (0x44, 0x44, 0x44)
        )


def test_ground_read_sees_a_pseudo_elements_fill(engine, tmp_path):
    page_of(
        tmp_path,
        '<div id="filled"><span id="label">Its ground is not its own.</span></div>',
        """
  #filled { position: relative; padding: 20px; z-index: 0; }
  #filled::before { content: ""; position: absolute; inset: 0; z-index: -1;
    background: #204060; }
  #label { color: #ffffff; }
""",
    )
    with serve(tmp_path) as (address, _), browser.opened(engine, address) as page:
        # The element's own ground is clear; what is drawn behind it is not.
        assert (
            page.evaluate(
                "getComputedStyle(document.querySelector('#filled')).backgroundColor"
            )
            == "rgba(0, 0, 0, 0)"
        )
        assert browser.ground(page, "#label") == {(0x20, 0x40, 0x60)}


def test_ground_read_sees_a_tint_over_what_is_beneath(engine, tmp_path):
    page_of(
        tmp_path,
        '<div id="beneath"><p id="tinted">A tint over another ground.</p></div>',
        """
  #beneath { background: #000000; padding: 20px; }
  #tinted { margin: 0; padding: 10px; color: #ffffff;
    background: rgba(255, 0, 0, 0.5); }
""",
    )
    with serve(tmp_path) as (address, _), browser.opened(engine, address) as page:
        (seen,) = browser.ground(page, "#tinted")
        assert seen[0] in (127, 128) and seen[1:] == (0, 0)


def test_lettering_on_the_page_is_held_against_the_stone(engine, tmp_path):
    # The helper's stone, worked as the tool works it: the sheen laid over
    # the page at its opacity, then the candle over that.
    stone = browser.stone()
    assert [round(channel, 1) for channel in stone] == [31.3, 18.8, 19.4]
    inscription = browser.colour(LOOK["colour"]["inscription"])
    assert round(browser.contrast(inscription, stone), 2) == 3.31

    page_colour = LOOK["colour"]["page"]
    page_of(
        tmp_path,
        """
<p id="on-the-page">Straight on the page.</p>
<div class="slab"><p id="on-a-slab">On a ground of its own.</p></div>
""",
        f"""
  body {{ background: {page_colour}; color: {LOOK["colour"]["inscription"]}; }}
  p {{ margin: 0 0 20px; }}
  .slab {{ background: {LOOK["colour"]["panel"]}; padding: 20px; }}
""",
        body_class=LOOK["class"],
    )
    with serve(tmp_path) as (address, _), browser.opened(engine, address) as page:
        page_ground = browser.colour(page_colour)[:3]
        # What is drawn behind it is the flat page, at 3.67; it is held at
        # the stone's 3.31 because it lies straight on the page.
        assert browser.ground(page, "#on-the-page") == {page_ground}
        assert round(browser.contrast(inscription, page_ground), 2) == 3.67
        assert browser.on_the_page(page, "#on-the-page")
        assert round(browser.stands_at(page, "#on-the-page"), 2) == 3.31
        # On a ground of its own it is held against that ground alone.
        assert not browser.on_the_page(page, "#on-a-slab")
        assert browser.stands_at(page, "#on-a-slab") == pytest.approx(
            browser.contrast(inscription, browser.colour(LOOK["colour"]["panel"]))
        )

    # A page that has not taken the look on has no stone to be held against.
    crimson = LOOK["colour"]["inscription"]
    page_of(
        tmp_path,
        '<p id="on-the-page">Straight on a page without the look.</p>',
        f"  body {{ background: {page_colour}; color: {crimson}; }}",
    )
    with serve(tmp_path) as (address, _), browser.opened(engine, address) as page:
        assert not browser.on_the_page(page, "#on-the-page")
        assert round(browser.stands_at(page, "#on-the-page"), 2) == 3.67


def test_helper_refuses_clear_letters(engine, tmp_path):
    page_of(
        tmp_path,
        """
<h1 id="carved">Carved</h1>
<p id="unseen">No colour at all</p>
""",
        """
  #carved { background: linear-gradient(#ff2a1a, #ba1a1a); color: #ba1a1a;
    -webkit-background-clip: text; background-clip: text;
    -webkit-text-fill-color: transparent; }
  #unseen { color: transparent; }
""",
    )
    with serve(tmp_path) as (address, _), browser.opened(engine, address) as page:
        with pytest.raises(browser.NotMeasured, match="its letters are clear"):
            browser.stands_at(page, "#carved")
        with pytest.raises(browser.NotMeasured, match="no colour at all"):
            browser.stands_at(page, "#unseen")


def test_helper_reads_with_stillness_asked(engine, tmp_path):
    page_of(
        tmp_path,
        '<p id="turning">A colour that never rests.</p>',
        """
  @keyframes turning { from { color: #ffffff; } to { color: #000000; } }
  #turning { color: #ffffff; background: #204060;
    animation: turning 1s infinite alternate; }
  @media (prefers-reduced-motion: reduce) { #turning { animation: none; } }
""",
    )
    with serve(tmp_path) as (address, _):
        # Opened as the helper opens a page, stillness is asked for, the page
        # answers it, and nothing is running when the colour is read.
        with browser.opened(engine, address) as page:
            assert page.evaluate(
                "matchMedia('(prefers-reduced-motion: reduce)').matches"
            )
            assert browser.in_passage(page, "#turning") == []
            assert browser.lettering(page, "#turning") == (255, 255, 255, 1.0)
        # Opened without it, the helper will not read a colour at all.
        with browser.opened(engine, address, still=False) as page:
            assert browser.in_passage(page, "#turning") == ["turning"]
            with pytest.raises(browser.NotMeasured, match="stillness"):
                browser.lettering(page, "#turning")

    # And where a page goes on moving though stillness was asked for, the
    # helper says what is still in passage and reads nothing.
    page_of(
        tmp_path,
        '<p id="turning">A colour that never rests, whatever is asked.</p>',
        """
  @keyframes restless { from { color: #ffffff; } to { color: #000000; } }
  #turning { background: #204060; animation: restless 1s infinite alternate; }
""",
    )
    with serve(tmp_path) as (address, _), browser.opened(engine, address) as page:
        with pytest.raises(browser.NotMeasured, match="still in passage: restless"):
            browser.stands_at(page, "#turning")


def test_browser_opens_a_page_with_script_off(engine, tmp_path):
    page_of(
        tmp_path,
        """
<p id="mark">as written</p>
<script>document.getElementById('mark').textContent = 'changed by script';</script>
""",
    )
    with serve(tmp_path) as (address, _):
        with browser.opened(engine, address, script=False) as page:
            assert page.locator("#mark").text_content() == "as written"
            # The helper's own reading still works on such a page.
            assert browser.boxes(page, "#mark")
        with browser.opened(engine, address) as page:
            assert page.locator("#mark").text_content() == "changed by script"
