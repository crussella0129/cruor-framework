"""The look's ground, opened in a browser: the stone, the candle and the dark
at the edges, on a page that holds nothing else.
"""

import pytest

import browser
from helpers import ROOT, serve
from stylesheets import LOOK as LOOK_DIR
from stylesheets import rules

LOOK = browser.theme()
BARE = "tests/pages/bare.html"


@pytest.fixture(scope="module")
def engine():
    with browser.chromium() as found:
        yield found


@pytest.fixture(scope="module")
def address():
    with serve(ROOT) as (found, _):
        yield found


def layer(page, which: str) -> dict:
    """What a browser makes of one of the two layers of the ground."""
    return page.evaluate(
        """which => {
            const s = getComputedStyle(document.body, which);
            return {content: s.content, image: s.backgroundImage, position: s.position,
                layer: s.zIndex, pointer: s.pointerEvents, opacity: s.opacity,
                top: s.top, right: s.right, bottom: s.bottom, left: s.left,
                animation: s.animationName};
        }""",
        which,
    )


def test_stone_lies_beneath_the_page(engine, address):
    with browser.opened(engine, address + BARE) as page:
        stone = layer(page, "::before")
        # It is drawn, from a drawing in the stylesheet and no file.
        assert stone["content"] != "none"
        assert stone["image"].startswith('url("data:image/svg+xml,')
        # It is fixed to the whole window, beneath the content, and takes no
        # press meant for the page.
        assert stone["position"] == "fixed"
        assert [stone[side] for side in ("top", "right", "bottom", "left")] == [
            "0px"
        ] * 4
        assert int(stone["layer"]) < 0
        assert stone["pointer"] == "none"
        # Its strength is the theme file's, by the token.
        assert float(stone["opacity"]) == LOOK["stone"]["sheen-opacity"]
        page.evaluate(
            "document.body.style.setProperty('--cruor-stone-sheen-opacity', '0.5')"
        )
        assert layer(page, "::before")["opacity"] == "0.5"

        # The candle's layer lies above the stone and beneath the content.
        candle = layer(page, "::after")
        assert candle["position"] == "fixed" and candle["pointer"] == "none"
        assert int(stone["layer"]) < int(candle["layer"]) < 0

        # The page's own ground is the theme file's.
        ground = page.evaluate("getComputedStyle(document.body).backgroundColor")
        assert browser.colour(ground) == browser.colour(LOOK["colour"]["page"])

    # Content set on the page is above both layers: it is what a press finds.
    with browser.opened(engine, address + BARE) as page:
        page.evaluate(
            """() => {
                const p = document.createElement('p');
                p.id = 'content'; p.textContent = 'On the stone.';
                p.style.cssText = 'margin:0;padding:40px;';
                document.body.appendChild(p);
            }"""
        )
        found = page.evaluate("document.elementFromPoint(60, 60).id")
        assert found == "content"


def test_candle_takes_its_tokens(engine, address):
    # The glow's colour and its strength are the tokens': change them on the
    # page and the glow changes with them.
    with browser.opened(engine, address + BARE) as page:
        top = {"x": 600, "y": 0, "width": 80, "height": 4}
        before = browser.pixels(page.screenshot(clip=top))
        page.evaluate(
            """() => {
                document.body.style.setProperty('--cruor-stone-candle', '#00ff00');
                document.body.style.setProperty('--cruor-stone-candle-opacity', '1');
            }"""
        )
        after = browser.pixels(page.screenshot(clip=top))
        assert all(red >= green for red, green, _ in before), "a warm glow, and faint"
        assert all(green > 150 and green > 2 * red for red, green, _ in after)


def test_candle_is_never_stronger_than_when_still():
    # Stillness stops the candle's flicker and leaves it as it lies. So that
    # the still candle is the candle at its strongest, no step of the flicker
    # may lift it above that.
    text = (LOOK_DIR / "cruentous-atonement.css").read_text(encoding="utf-8")
    found = rules(text)
    steps = [
        rule
        for rule in found
        if len(rule.path) == 2 and rule.path[0] == "@keyframes cruor-candle"
    ]
    assert steps, "the candle has a flicker"
    for step in steps:
        assert [name for name, _ in step.declarations] == ["opacity"], step.path
        assert float(step.value("opacity")) <= 1, step.path
    # At rest the layer has no opacity of its own to be lifted from.
    at_rest = [rule for rule in found if rule.path[-1] == "&::after"]
    assert at_rest and all(rule.value("opacity") is None for rule in at_rest)


def test_every_bound_holds_on_the_stone_as_drawn(engine, address):
    # The theme file promises what stands on `stone`, the page at its
    # brightest, from three numbers. Here the stone is drawn and its
    # brightest pixel found, and every promise on `stone` is held against
    # that, with no allowance.
    assert browser.WINDOW == {"width": 1280, "height": 800}
    with browser.opened(engine, address + BARE) as page:
        assert not page.evaluate("document.body.getAnimations({subtree: true}).length")
        seen = set(browser.pixels(page.screenshot()))
    assert len(seen) > 50, "a surface, not a flat ground"
    brightest = max(seen, key=browser.luminance)

    for entry in LOOK["contrast"]:
        if "stone" not in entry["grounds"]:
            continue
        for role in entry["text"]:
            text = browser.colour(LOOK["colour"][role])
            found = browser.contrast(text, brightest)
            assert found >= entry["at-least"], (
                f"{role} stands at {found:.3f} on the stone's brightest pixel "
                f"{brightest}, and {entry['at-least']} is promised"
            )
    # And the stone as drawn is no brighter than the theme file says it may be.
    assert browser.luminance(brightest) <= browser.luminance(browser.stone()), brightest
