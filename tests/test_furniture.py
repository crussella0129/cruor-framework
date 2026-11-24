"""The furniture: every part of the list, read in the stylesheet and then
opened in a browser with script turned off.

The tests run over `tests/parts.py`, the one list of the parts. A part is
tested when it is in that list.
"""

import re

import pytest

import browser
import parts
from helpers import ROOT, serve
from stylesheets import LOOK as LOOK_DIR
from stylesheets import rules

LOOK = browser.theme()
FURNITURE = LOOK_DIR / "furniture.css"

# The parts of the sprint's plan, in the order its tasks build them. The
# list is whole when it holds them all; a part the owner has cut is taken
# from here and from the list in one commit.
PLANNED = [
    # T-206, the controls
    "cruor-button",
    "cruor-field",
    "cruor-label",
    "cruor-hint",
    "cruor-fault",
    "cruor-choice",
    "cruor-tick",
    "cruor-radio",
    "cruor-slider",
    "cruor-progress",
    "cruor-measure",
]


@pytest.fixture(scope="module")
def engine():
    with browser.chromium() as found:
        yield found


@pytest.fixture(scope="module")
def address():
    with serve(ROOT) as (found, _):
        yield found


def role(name: str) -> tuple:
    return browser.colour(LOOK["colour"][name])


# -- the list, and the stylesheet ---------------------------------------------


def test_parts_list_is_whole():
    assert parts.classes() == PLANNED
    for part in parts.PARTS:
        assert part.name and part.css_class.startswith("cruor-")
        assert (ROOT / part.page).is_file(), part.page
        assert part.at_rest, f"{part.name} has a state at rest"
        html = (ROOT / part.page).read_text(encoding="utf-8")
        for state in part.states:
            assert state.selector.startswith("#"), state
            assert f'id="{state.selector[1:]}"' in html, state.selector
            for selector, bound in state.texts:
                assert bound in (parts.INTERFACE, parts.INSCRIPTION, parts.UNABLE)
                assert f'id="{selector[1:]}"' in html, selector
        for selector in (*part.keyboard, *part.blood):
            assert f'id="{selector[1:]}"' in html, selector
        # Every example of the part on its page carries the part's class.
        for state in part.at_rest:
            tag = re.search(rf'<[^>]*id="{state.selector[1:]}"[^>]*>', html)
            assert tag and part.css_class in tag.group(0), state.selector


def test_furniture_has_every_part_and_no_other():
    text = FURNITURE.read_text(encoding="utf-8")
    ruled = set()
    for rule in rules(text):
        for part_of_path in rule.path:
            if not part_of_path.startswith("@keyframes"):
                ruled.update(re.findall(r"\.(cruor-[a-z-]+)", part_of_path))
    assert ruled == set(parts.classes())


# -- contrast, in every state -------------------------------------------------


def bring_about(page, state: parts.State) -> None:
    """Put a part in a state a hand brings about."""
    if state.how is parts.AT_REST:
        return
    if state.how == parts.POINTER_OVER:
        page.hover(state.selector)
    elif state.how == parts.PRESSED:
        page.hover(state.selector)
        page.mouse.down()
    elif state.how == parts.KEYBOARD:
        tab_to(page, state.selector)
    else:
        raise AssertionError(state.how)


def tab_to(page, selector: str) -> None:
    """Press Tab until the keyboard is on an element."""
    for _ in range(80):
        page.keyboard.press("Tab")
        if page.evaluate(
            "selector => document.activeElement === document.querySelector(selector)",
            selector,
        ):
            return
    raise AssertionError(f"Tab never reached {selector}")


MEASURED = [
    pytest.param(
        part,
        state,
        selector,
        bound,
        id=f"{part.name}, {state.name}: {selector}",
    )
    for part in parts.PARTS
    for state in part.states
    for selector, bound in state.texts
]


@pytest.mark.parametrize(("part", "state", "selector", "bound"), MEASURED)
def test_every_lettered_part_meets_contrast(
    engine, address, part, state, selector, bound
):
    with browser.opened(engine, address + part.page, script=False) as page:
        bring_about(page, state)
        try:
            found = browser.stands_at(page, selector)
        finally:
            if state.how == parts.PRESSED:
                page.mouse.up()
    assert found >= bound, f"{selector} stands at {found:.2f}, and {bound} is asked"


def test_states_are_brought_about(engine, address):
    # That the three ways of bringing a state about do bring it about: the
    # button shows each differently from how it lies.
    with browser.opened(engine, address + parts.CONTROLS, script=False) as page:
        read = """() => {
            const s = getComputedStyle(document.querySelector('#button'));
            return [s.borderTopColor, s.backgroundColor, s.boxShadow, s.outlineStyle];
        }"""
        at_rest = page.evaluate(read)
        page.hover("#button")
        over = page.evaluate(read)
        page.mouse.down()
        pressed = page.evaluate(read)
        page.mouse.up()
        page.mouse.move(600, 700)
        tab_to(page, "#button")
        keyboard = page.evaluate(read)
    assert over[0] != at_rest[0], "the pointer over it changes its edge"
    assert pressed[1] != at_rest[1] and pressed[2] != at_rest[2], (
        "pressed, it goes down"
    )
    assert at_rest[3] == "none" and keyboard[3] != "none", "the keyboard on it is shown"


# -- ticks, picks and what the blood fills ------------------------------------


def picture(page, selector: str) -> list:
    # The element is brought into view first, wherever on the page it lies.
    return browser.pixels(page.locator(selector).screenshot())


def test_tick_and_radio_show_their_state(engine, address):
    with browser.opened(engine, address + parts.CONTROLS, script=False) as page:
        for unset, is_set in (("#tick", "#tick-ticked"), ("#radio", "#radio-picked")):
            before = picture(page, unset)
            assert before != picture(page, is_set), unset
            # What is struck is the look's accent, set into the sunken ground.
            assert role("accent")[:3] in set(picture(page, is_set)), is_set
            assert role("accent")[:3] not in set(before), unset
        # And a press of the pointer sets one, with no script to help it.
        page.click("#tick")
        assert page.evaluate("document.querySelector('#tick').checked")
        page.mouse.move(600, 700)
        assert role("accent")[:3] in set(picture(page, "#tick"))


BLOODED = [
    pytest.param(part, selector, id=f"{part.name}: {selector}")
    for part in parts.PARTS
    for selector in part.blood
]


@pytest.mark.parametrize(("part", "selector"), BLOODED)
def test_blood_carries_an_edge(engine, address, part, selector):
    # Along the middle of a part that the blood fills: the blood, then its
    # edge, then the ground beside it. The blood lies near the page's own
    # ground, so it is the edge that must be seen against what lies beyond.
    blood, edge = role("blood")[:3], role("blood-edge")[:3]
    with browser.opened(engine, address + part.page, script=False) as page:
        png = page.locator(selector).screenshot()
    wide = browser.width(png)
    everything = browser.pixels(png)
    middle = len(everything) // wide // 2
    row = everything[middle * wide : (middle + 1) * wide]
    runs = []
    for pixel in row:
        if runs and runs[-1][0] == pixel:
            runs[-1][1] += 1
        else:
            runs.append([pixel, 1])
    colours = [colour for colour, length in runs if length >= 2]
    assert blood in colours, f"{selector} is filled with the blood"
    assert edge in colours, f"{selector}'s fill has its edge"
    at = colours.index(edge)
    assert colours[at - 1] == blood, "the edge is the blood's own"
    beside = colours[at + 1]
    assert beside == role("sunken")[:3], "beyond the edge is the unfilled channel"
    assert browser.ratio(edge, beside) >= 3, browser.ratio(edge, beside)
    assert browser.ratio(edge, blood) >= 3, "and the edge is told from the blood"


# -- the keyboard ------------------------------------------------------------


@pytest.mark.parametrize("page_path", parts.pages())
def test_keyboard_reaches_and_marks_every_part_that_takes_it(
    engine, address, page_path
):
    takes = [
        selector
        for part in parts.PARTS
        if part.page == page_path
        for selector in part.keyboard
    ]
    mark = """selector => {
        const s = getComputedStyle(document.querySelector(selector));
        return {outline: s.outlineStyle, wide: parseFloat(s.outlineWidth),
            shadow: s.boxShadow};
    }"""
    with browser.opened(engine, address + page_path, script=False) as page:
        without = {selector: page.evaluate(mark, selector) for selector in takes}
        reached = {}
        for _ in range(120):
            page.keyboard.press("Tab")
            on = page.evaluate("document.activeElement.id")
            if not on or f"#{on}" in reached:
                break
            reached[f"#{on}"] = page.evaluate(mark, f"#{on}")
    for selector in takes:
        assert selector in reached, f"Tab never reached {selector}"
        seen = reached[selector]
        shown = (seen["outline"] != "none" and seen["wide"] > 0) or (
            seen["shadow"] != without[selector]["shadow"]
        )
        assert shown, f"{selector} shows no mark with the keyboard on it"
        assert without[selector]["outline"] == "none", selector


def test_controls_are_worked_by_their_keys(engine, address):
    with browser.opened(engine, address + parts.CONTROLS, script=False) as page:
        value = "selector => document.querySelector(selector).%s"

        tab_to(page, "#tick")
        assert not page.evaluate(value % "checked", "#tick")
        page.keyboard.press("Space")
        assert page.evaluate(value % "checked", "#tick")

        tab_to(page, "#radio-picked")
        page.keyboard.press("ArrowUp")
        assert page.evaluate(value % "checked", "#radio")
        assert not page.evaluate(value % "checked", "#radio-picked")

        tab_to(page, "#slider")
        before = page.evaluate(value % "valueAsNumber", "#slider")
        page.keyboard.press("ArrowRight")
        assert page.evaluate(value % "valueAsNumber", "#slider") == before + 1

        tab_to(page, "#choice")
        assert page.evaluate(value % "selectedIndex", "#choice") == 0
        page.keyboard.press("ArrowDown")
        assert page.evaluate(value % "selectedIndex", "#choice") == 1
