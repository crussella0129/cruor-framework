"""The showroom: a page built from the kit alone, read and then opened in a
browser.

`showroom/index.html` is served from a copy of the repository as it lies.
What it shows of the furniture is held against `tests/parts.py`, the one
list of the parts.
"""

import re
import tomllib
from html.parser import HTMLParser

import pytest

import browser
import parts
from helpers import ROOT, serve
from stylesheets import rules, without_comments

LOOK = browser.theme()
SHOWROOM = "showroom/index.html"
PAGE = (ROOT / SHOWROOM).read_text(encoding="utf-8")
OWN_STYLESHEET = (ROOT / "showroom" / "showroom.css").read_text(encoding="utf-8")

KIT = [
    "../fonts/fonts.css",
    "../look/tokens.css",
    "../look/cruentous-atonement.css",
    "../look/furniture.css",
]

RESTING = [
    pytest.param(part, state, id=f"{part.name}: {state.name}")
    for part in parts.PARTS
    for state in part.at_rest
]


@pytest.fixture(scope="module")
def engine():
    with browser.chromium() as found:
        yield found


@pytest.fixture(scope="module")
def address():
    with serve(ROOT) as (found, _):
        yield found


class Read(HTMLParser):
    """What the page links, and what it carries of its own."""

    def __init__(self):
        super().__init__()
        self.stylesheets = []
        self.scripts = []
        self.styles = []
        self.style_elements = 0

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "link" and attributes.get("rel") == "stylesheet":
            self.stylesheets.append(attributes.get("href"))
        if tag == "script":
            self.scripts.append(attributes.get("src"))
        if tag == "style":
            self.style_elements += 1
        if "style" in attributes:
            self.styles.append(attributes["style"])


def read_page() -> Read:
    found = Read()
    found.feed(PAGE)
    return found


# -- read as text ---------------------------------------------------------------


def test_showroom_links_only_the_kit():
    found = read_page()
    assert found.stylesheets == [*KIT, "showroom.css"]
    assert found.style_elements == 0
    # What the page styles in place is the family of a line of code, in the
    # side by side of the fixed-pitch families, and nothing else.
    for style in found.styles:
        assert re.fullmatch(r"font-family: '[A-Za-z ]+', monospace", style), style


def test_showroom_stylesheet_adds_no_colour():
    text = without_comments(OWN_STYLESHEET)
    assert not re.findall(r"#[0-9a-fA-F]{3,8}\b", text)
    written = r"\b(?:rgba?|hsla?|hwb|lab|lch|oklab|oklch|color-mix)\("
    assert not re.findall(written, text)
    for rule in rules(text):
        for name, _ in rule.declarations:
            assert "color" not in name and name not in ("background", "border"), name
    assert "url(" not in text and "@import" not in text


def test_showroom_imitates_no_state():
    # The showroom's stylesheet lays the place out. It dresses no part of
    # the kit and imitates no state of one: no rule of it is on a class of
    # the kit's, and none on a state.
    states = (
        ":hover",
        ":active",
        ":focus",
        ":checked",
        ":disabled",
        ":invalid",
        ":open",
        "[open]",
        "[aria-",
        ":popover-open",
        ":modal",
    )
    for rule in rules(OWN_STYLESHEET):
        selector = " ".join(rule.path)
        assert "cruor-" not in selector, selector
        for state in states:
            assert state not in selector, selector


# -- opened in a browser --------------------------------------------------------


def test_showroom_loads_from_the_kit_alone(engine, address):
    asked, failed, statuses = [], [], {}
    context = engine.new_context(viewport=browser.WINDOW, reduced_motion="reduce")
    page = context.new_page()
    page.on("request", lambda request: asked.append(request.url))
    page.on("requestfailed", lambda request: failed.append(request.url))
    page.on("response", lambda got: statuses.update({got.url: got.status}))
    try:
        page.goto(address + SHOWROOM)
        page.wait_for_load_state("networkidle")
        page.evaluate("document.fonts.ready.then(() => true)")
        faces = page.evaluate(
            "[...document.fonts].map(face => [face.family.replaceAll('\"', ''),"
            " face.weight, face.style, face.status])"
        )
    finally:
        context.close()
    assert asked and all(url.startswith(address) for url in asked), asked
    assert failed == []
    assert all(status == 200 for status in statuses.values()), statuses
    # Every face the page set a letter in was fetched and loaded: none was
    # left in error, and the families the look names are among them.
    assert not [face for face in faces if face[3] == "error"]
    loaded = {face[0] for face in faces if face[3] == "loaded"}
    for role in ("title", "heading", "text", "code"):
        assert LOOK["font"][role] in loaded, role
    fonts = [url for url in asked if url.endswith(".woff2")]
    assert fonts and all("/fonts/" in url for url in fonts)


def shown(page, attribute: str) -> dict | None:
    return page.evaluate(
        """shows => {
            const el = document.querySelector(`[data-shows="${shows}"]`);
            if (!el) return null;
            const r = el.getBoundingClientRect();
            const s = getComputedStyle(el);
            return {classes: [...el.classList], wide: r.width, tall: r.height,
                hidden: s.display === 'none' || s.visibility === 'hidden',
                within: [...document.querySelectorAll('[class*="cruor-"]')]
                    .filter(outer => outer.contains(el))
                    .flatMap(outer => [...outer.classList])};
        }""",
        attribute,
    )


@pytest.mark.parametrize(("part", "state"), RESTING)
def test_showroom_shows_every_part_in_every_resting_state(engine, address, part, state):
    with browser.opened(engine, address + SHOWROOM) as page:
        found = shown(page, f"{part.name}: {state.name}")
    assert found, f"the showroom shows no {part.name}, {state.name}"
    assert part.css_class in found["classes"] or part.css_class in found["within"]
    assert not found["hidden"] and found["wide"] > 0 and found["tall"] > 0


def test_showroom_stands_without_script(engine, address):
    # With script turned off, everything the showroom shows of the furniture
    # is still there to be seen.
    with browser.opened(engine, address + SHOWROOM, script=False) as page:
        for part in parts.PARTS:
            for state in part.at_rest:
                found = shown(page, f"{part.name}: {state.name}")
                assert found and not found["hidden"], (part.name, state.name)
                assert found["wide"] > 0 and found["tall"] > 0, (part.name, state.name)
        # And what a hand opens still opens.
        page.click("#rule-one > summary")
        assert page.evaluate("document.querySelector('#rule-one').open")
        assert not page.evaluate("document.querySelector('#rule-two').open")


WRITTEN = re.findall(r'<pre class="written" data-of="([a-z-]+)">', PAGE)


def test_showroom_gives_each_parts_html(engine, address):
    assert len(WRITTEN) == len(set(WRITTEN)) and len(WRITTEN) > 20
    with browser.opened(engine, address + SHOWROOM, script=False) as page:
        found = page.evaluate(
            """() => [...document.querySelectorAll('pre.written')].map(pre => {
                const live = document.getElementById(pre.dataset.of);
                const made = document.createElement('template');
                made.innerHTML = pre.textContent;
                const again = made.content.firstElementChild;
                const room = el => el.closest('section, aside, main');
                return {of: pre.dataset.of, live: live !== null,
                    one: made.content.childElementCount === 1,
                    same: live !== null && again.isEqualNode(live),
                    beside: live !== null && room(pre) === room(live),
                    folded: pre.closest('details.cruor-fold') !== null,
                    classes: [...again.querySelectorAll('[class*="cruor-"]'), again]
                        .flatMap(el => [...el.classList])};
            })"""
        )
    written_classes = set()
    for snippet in found:
        assert snippet["live"], f"nothing on the page is named {snippet['of']}"
        assert snippet["one"], snippet["of"]
        # What is written is what is there, attribute for attribute.
        assert snippet["same"], f"{snippet['of']} is not what its HTML says"
        assert snippet["beside"], f"{snippet['of']}'s HTML is in another room"
        assert snippet["folded"], snippet["of"]
        written_classes.update(snippet["classes"])
    # Every part of the list has its HTML written somewhere in the place.
    for css_class in parts.classes():
        assert css_class in written_classes, css_class


@pytest.mark.parametrize("named", WRITTEN)
def test_a_parts_html_draws_the_part(engine, address, named):
    # The HTML beside a thing, set alone in a page that has taken the look
    # on, in a space as wide as the thing has here, draws the same thing:
    # the same size, and the same colours and letters for every part in it.
    # A thing that rises is raised first, in both pages. A thing that stands
    # in a row of others here is as tall as its row, which is the row's
    # doing: alone it is given a row as tall, and what it holds is measured.
    measure = """named => {
        const root = document.getElementById(named);
        if (root.popover && !root.matches(':popover-open')) root.showPopover();
        const all = [root, ...root.querySelectorAll('[class*="cruor-"]')];
        const s = getComputedStyle(root);
        const out = s.position === 'absolute' || s.position === 'fixed';
        const around = out
            ? root.offsetParent ?? document.documentElement
            : root.parentElement;
        return {
            space: around.getBoundingClientRect().width,
            own: root.getBoundingClientRect().width,
            tall: root.getBoundingClientRect().height,
            in_a_row: !out && getComputedStyle(around).display === 'grid',
            block: !out && ['block', 'flex', 'grid', 'list-item'].includes(s.display),
            parts: all.map(el => {
                const c = getComputedStyle(el);
                const r = el.getBoundingClientRect();
                return [el.tagName, el.className,
                    Math.round(r.width), Math.round(r.height),
                    c.color, c.backgroundColor, c.borderTopColor,
                    c.fontFamily, c.fontSize];
            }),
        };
    }"""
    with browser.opened(engine, address + SHOWROOM, script=False) as page:
        here = page.evaluate(measure, named)
        snippet = page.evaluate(
            "named => [...document.querySelectorAll('pre.written')]"
            ".find(pre => pre.dataset.of === named).textContent",
            named,
        )
    wide = here["own"] if here["block"] else here["space"]
    space = f"position: relative; width: {wide}px"
    if here["in_a_row"]:
        space = (
            "display: grid; grid-template-columns: minmax(0, 1fr);"
            f" width: {wide}px; height: {here['tall']}px"
        )
    links = "\n".join(f'<link rel="stylesheet" href="{href}">' for href in KIT)
    alone = (
        '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        f"<title>One thing, alone</title>\n{links}\n</head>\n"
        '<body class="cruentous-atonement">\n'
        f'<div style="{space}">\n{snippet}\n</div>\n'
        "</body>\n</html>\n"
    )
    context = engine.new_context(
        viewport=browser.WINDOW, java_script_enabled=False, reduced_motion="reduce"
    )
    page = context.new_page()
    kind = "text/html; charset=utf-8"
    page.route(
        "**/showroom/alone.html",
        lambda route: route.fulfill(body=alone, content_type=kind),
    )
    try:
        page.goto(address + "showroom/alone.html")
        page.wait_for_load_state("networkidle")
        page.evaluate("document.fonts.ready.then(() => true)")
        there = page.evaluate(measure, named)
    finally:
        context.close()
    assert len(there["parts"]) == len(here["parts"])
    for alone_part, here_part in zip(there["parts"], here["parts"], strict=True):
        assert alone_part[:2] == here_part[:2]
        assert abs(alone_part[2] - here_part[2]) <= 1, (alone_part, here_part)
        assert abs(alone_part[3] - here_part[3]) <= 1, (alone_part, here_part)
        assert alone_part[4:] == here_part[4:], (alone_part, here_part)


def test_showroom_sets_the_fixed_pitch_families_side_by_side(engine, address):
    families = tomllib.loads(
        (ROOT / "fonts" / "families.toml").read_text(encoding="utf-8")
    )["family"]
    fixed = [family["name"] for family in families if family["kind"] != "proportional"]
    assert len(fixed) == 5
    with browser.opened(engine, address + SHOWROOM, script=False) as page:
        found = page.evaluate(
            """() => [...document.querySelectorAll('#fixed-pitch .fixed')].map(el => {
                const line = el.querySelector('pre');
                const r = line.getBoundingClientRect();
                return {family: el.dataset.family,
                    named: el.querySelector('small').textContent,
                    set: getComputedStyle(line).fontFamily,
                    loaded: document.fonts.check(`24px "${el.dataset.family}"`),
                    code: line.textContent, top: Math.round(r.top), wide: r.width};
            })"""
        )
    assert [line["family"] for line in found] == fixed
    for line in found:
        assert line["named"] == line["family"], "each is named"
        assert line["set"].startswith(f'"{line["family"]}"'), line
        assert line["loaded"], line["family"]
        assert line["code"] == found[0]["code"], "the same line in each"
    # Side by side: at least two of them stand on one row.
    tops = [line["top"] for line in found]
    assert len(set(tops)) < len(tops)
    # And the first of them is the family code is set in.
    assert found[0]["family"] == LOOK["font"]["code"]
