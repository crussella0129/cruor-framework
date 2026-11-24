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
    # T-207, the containers
    "cruor-plate",
    "cruor-panel",
    "cruor-void",
    "cruor-notice",
    "cruor-fold",
    "cruor-rise",
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
    elif state.how == parts.RAISED:
        page.click(state.by)
        page.wait_for_selector(state.selector, state="visible")
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


# -- the containers ------------------------------------------------------------

# A paragraph in each container that can hold one, with how the container
# comes to be shown if it is not shown as the page lies.
PARAGRAPHS = [
    ("#plate-text", None),
    ("#panel-text", None),
    ("#notice-note-text", None),
    ("#notice-warning-text", None),
    ("#notice-fault-text", None),
    ("#fold-open-text", None),
    ("#rise-open-text", None),
    ("#rise-text", "#raise"),
    ("#dialog-text", "#raise-dialog"),
]


@pytest.mark.parametrize(("paragraph", "raised_by"), PARAGRAPHS)
def test_paragraph_in_every_container_is_an_inscription(
    engine, address, paragraph, raised_by
):
    with browser.opened(engine, address + parts.CONTAINERS, script=False) as page:
        if raised_by:
            page.click(raised_by)
            page.wait_for_selector(paragraph, state="visible")
        size = page.evaluate(
            "selector => parseFloat(getComputedStyle("
            "document.querySelector(selector)).fontSize)",
            paragraph,
        )
        assert size >= 24, paragraph
        assert browser.lettering(page, paragraph) == role("inscription")
        found = browser.stands_at(page, paragraph)
    assert found >= parts.INSCRIPTION, f"{paragraph} stands at {found:.2f}"


def test_voids_current_row_meets_contrast(engine, address):
    with browser.opened(engine, address + parts.CONTAINERS, script=False) as page:
        # The row is the tint laid over the void's ground, as the theme file
        # works it, and the void's own lettering stands on it.
        void = LOOK["void"]
        row = browser.laid(browser.colour(void["row"]), browser.colour(void["ground"]))
        (seen,) = browser.ground(page, "#void-row")
        assert all(abs(seen[at] - row[at]) <= 1 for at in range(3)), (seen, row)
        assert browser.lettering(page, "#void-row") == browser.colour(void["text"])
        assert browser.stands_at(page, "#void-row") >= parts.INTERFACE
        # The row is marked by more than its tint: a channel beside it.
        shadow = page.evaluate(
            "getComputedStyle(document.querySelector('#void-row')).boxShadow"
        )
        assert "inset" in shadow
        # Subdued lettering lies off the row, on the void's own ground.
        assert browser.ground(page, "#void-subdued") == {
            browser.colour(void["ground"])[:3]
        }


HEADINGS_WITHIN = [
    "#plate-heading",
    "#panel-heading",
    "#notice-heading",
    "#fold-heading",
    "#rise-open-heading",
]


@pytest.mark.parametrize("heading", HEADINGS_WITHIN)
def test_heading_in_a_container_is_not_carved(engine, address, heading):
    with browser.opened(engine, address + parts.CONTAINERS, script=False) as page:
        clip = page.evaluate(
            "selector => getComputedStyle(document.querySelector(selector))"
            ".backgroundClip",
            heading,
        )
        assert "text" not in clip, heading
        assert browser.lettering(page, heading) == role("inscription")
        found = browser.stands_at(page, heading)
    assert found >= parts.INSCRIPTION, f"{heading} stands at {found:.2f}"


def is_open(page, selector: str) -> bool:
    return page.evaluate("selector => document.querySelector(selector).open", selector)


def test_fold_opens_without_script(engine, address):
    with browser.opened(engine, address + parts.CONTAINERS, script=False) as page:
        assert not is_open(page, "#fold")
        assert not page.locator("#fold-text").is_visible()
        page.click("#fold-summary")
        assert is_open(page, "#fold") and page.locator("#fold-text").is_visible()
        # And by the keyboard: it is on the summary, and Enter shuts it again.
        assert page.evaluate("document.activeElement.id") == "fold-summary"
        page.keyboard.press("Enter")
        assert not is_open(page, "#fold")
        page.keyboard.press("Enter")
        assert is_open(page, "#fold")


def test_folds_sharing_a_name_open_one_at_a_time(engine, address):
    with browser.opened(engine, address + parts.CONTAINERS, script=False) as page:
        page.click("#fold-a-summary")
        assert is_open(page, "#fold-a") and not is_open(page, "#fold-b")
        page.click("#fold-b-summary")
        assert is_open(page, "#fold-b") and not is_open(page, "#fold-a")


def test_rise_opens_and_closes_without_script(engine, address):
    shown = "document.querySelector('#rise').matches(':popover-open')"
    with browser.opened(engine, address + parts.CONTAINERS, script=False) as page:
        assert not page.evaluate(shown)
        assert not page.locator("#rise").is_visible()
        page.click("#raise")
        assert page.evaluate(shown) and page.locator("#rise").is_visible()
        # It is above the page: it is what a press at its middle finds.
        box = page.locator("#rise").bounding_box()
        found = page.evaluate(
            "([x, y]) => document.elementFromPoint(x, y).closest('#rise') !== null",
            [box["x"] + box["width"] / 2, box["y"] + box["height"] / 2],
        )
        assert found
        page.keyboard.press("Escape")
        assert not page.evaluate(shown)
        assert not page.locator("#rise").is_visible()


def test_dialog_opens_modal_without_script(engine, address):
    with browser.opened(engine, address + parts.CONTAINERS, script=False) as page:
        assert not is_open(page, "#dialog")
        page.click("#raise-dialog")
        assert is_open(page, "#dialog")
        assert page.evaluate("document.querySelector('#dialog').matches(':modal')")
        # The page behind it does not take the keyboard: Tab stays within.
        for _ in range(6):
            page.keyboard.press("Tab")
            inside = page.evaluate(
                "document.activeElement === document.body"
                " || document.activeElement.closest('#dialog') !== null"
            )
            assert inside, page.evaluate("document.activeElement.id")
        # Nor a press of the pointer: what lies behind is not reached.
        behind = page.evaluate(
            "(() => { const r = document.querySelector('#raise')"
            ".getBoundingClientRect();"
            " const found = document.elementFromPoint(r.x + 2, r.y + 2);"
            " return found ? found.id : ''; })()"
        )
        assert behind != "raise"
        page.keyboard.press("Escape")
        assert not is_open(page, "#dialog")
        # Its own button closes it too, by a command and no script.
        page.click("#raise-dialog")
        page.click("#dialog-close")
        assert not is_open(page, "#dialog")
