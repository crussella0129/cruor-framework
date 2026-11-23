"""The page that sets a line in every face, read and then opened in a browser.

The fonts' folder is served over HTTP on this machine alone, and a headless
Chromium opens the page as a reader's browser would.
"""

import re
import tomllib
from html.parser import HTMLParser

import pytest
from playwright.sync_api import sync_playwright

from helpers import ROOT, serve

FONTS = ROOT / "fonts"

# How a style is written in a file's name, and how a page asks for it.
STYLES = {
    "Regular": (400, "normal"),
    "Bold": (700, "normal"),
    "Italic": (400, "italic"),
    "BoldItalic": (700, "italic"),
}


def faces() -> list[tuple[str, int, str, str]]:
    """Every face the list calls for: family, weight, style and file."""
    families = tomllib.loads((FONTS / "families.toml").read_text(encoding="utf-8"))
    return [
        (family["name"], weight, style, f"{family['stem']}-{suffix}.woff2")
        for family in families["family"]
        for suffix, (weight, style) in STYLES.items()
    ]


FACES = faces()


class Addresses(HTMLParser):
    """Gathers what a page could fetch or run."""

    def __init__(self):
        super().__init__()
        self.addresses = []
        self.scripts = 0
        self.handlers = []
        self.samples = []
        self.styles = []
        self._in_style = False

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "script":
            self.scripts += 1
        if tag == "style":
            self._in_style = True
        for name, value in attributes.items():
            if name.startswith("on"):
                self.handlers.append(name)
            if name in ("href", "src", "action", "poster", "data"):
                self.addresses.append(value)
            if name == "style":
                self.styles.append(value)
        if "sample" in (attributes.get("class") or "").split():
            self.samples.append(attributes)

    def handle_endtag(self, tag):
        if tag == "style":
            self._in_style = False

    def handle_data(self, data):
        if self._in_style:
            self.styles.append(data)


def test_specimen_is_self_contained():
    page = Addresses()
    page.feed((FONTS / "specimen.html").read_text(encoding="utf-8"))

    assert page.scripts == 0
    assert page.handlers == []

    in_styles = [
        address.strip("'\" ")
        for style in page.styles
        for address in re.findall(r"url\(([^)]*)\)", style)
    ]
    assert not any("@import" in style for style in page.styles)
    addresses = page.addresses + in_styles
    assert "fonts.css" in addresses
    for address in addresses:
        assert re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", address), address
        assert (FONTS / address).is_file(), address

    # One line for each face, asking for it by family, weight and style.
    assert len(page.samples) == 32
    asked = {
        sample["data-file"]: " ".join(sample["style"].split())
        for sample in page.samples
    }
    assert asked == {
        file: f"font-family: '{family}'; font-weight: {weight}; font-style: {style}"
        for family, weight, style, file in FACES
    }


@pytest.fixture(scope="module")
def served_fonts():
    """The fonts' folder over HTTP, on this machine alone."""
    with serve(FONTS) as (address, _asked):
        yield address


@pytest.fixture(scope="module")
def chromium():
    """A headless Chromium, as a reader's browser."""
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        yield browser
        browser.close()


@pytest.fixture
def specimen(chromium, served_fonts):
    """The specimen, opened, with every request it made."""
    context = chromium.new_context(viewport={"width": 1600, "height": 900})
    page = context.new_page()
    requests, failures = [], []
    page.on("request", lambda request: requests.append(request.url))
    page.on("requestfailed", lambda request: failures.append(request.url))
    responses = []
    page.on("response", lambda response: responses.append(response))
    page.goto(served_fonts + "specimen.html")
    page.evaluate("() => document.fonts.ready.then(() => true)")
    yield page, requests, failures, responses
    context.close()


def css_font(weight: int, style: str, family: str) -> str:
    """A face, as the browser's font-loading interface is asked for it."""
    return f'{style} {weight} 28px "{family}"'


def test_specimen_loads_all_faces(specimen, served_fonts):
    page, requests, failures, responses = specimen

    assert failures == []
    assert all(url.startswith(served_fonts) for url in requests), requests
    assert all(response.status == 200 for response in responses)

    statuses = page.evaluate(
        "() => [...document.fonts].map(face => [face.family, face.weight, "
        "face.style, face.status])"
    )
    assert len(statuses) == 32
    assert [status for *_, status in statuses] == ["loaded"] * 32

    for family, weight, style, _ in FACES:
        assert page.evaluate(
            "font => document.fonts.check(font)", css_font(weight, style, family)
        ), (family, weight, style)

    fetched = sorted(url.rsplit("/", 1)[1] for url in requests if ".woff2" in url)
    assert fetched == sorted(file for *_, file in FACES)


@pytest.mark.parametrize(
    ("family", "weight", "style", "file"),
    FACES,
    ids=[file.removesuffix(".woff2") for *_, file in FACES],
)
def test_specimen_fetches_a_file_for_each_face(
    chromium, served_fonts, family, weight, style, file
):
    # A fresh page that links the stylesheet and sets no text, so nothing is
    # fetched until one face is asked for.
    context = chromium.new_context()
    context.route(
        "**/blank.html",
        lambda route: route.fulfill(
            content_type="text/html",
            body='<!doctype html><link rel="stylesheet" href="fonts.css">',
        ),
    )
    page = context.new_page()
    fetched = []
    page.on(
        "request",
        lambda request: (
            fetched.append(request.url) if ".woff2" in request.url else None
        ),
    )
    page.goto(served_fonts + "blank.html")
    assert fetched == []

    loaded = page.evaluate(
        "font => document.fonts.load(font).then(faces => faces.length)",
        css_font(weight, style, family),
    )
    context.close()

    assert loaded == 1
    assert fetched == [served_fonts + file]


@pytest.mark.parametrize("family", ["Cruor Lite Regular", "Cruor Lite Mono"])
def test_specimen_styles_of_a_family_differ(specimen, family):
    page, *_ = specimen
    files = [file for name, _, _, file in FACES if name == family]
    assert len(files) == 4
    # Each picture is of the sample sentence alone, without its label.
    pictures = [
        page.locator(f'.sample[data-file="{file}"]').screenshot() for file in files
    ]
    assert len(set(pictures)) == 4


def test_specimen_is_not_in_a_fallback(specimen):
    page, *_ = specimen
    widths = page.evaluate(
        """() => ["'Cruor Sans Regular'", "'a family no system has'"].map(family => {
            const span = document.createElement('span');
            span.style.cssText = `font: 28px ${family}; white-space: nowrap`;
            span.textContent = 'Sphinx of black quartz, judge my vow.';
            document.body.append(span);
            const width = span.getBoundingClientRect().width;
            span.remove();
            return width;
        })"""
    )
    assert widths[0] > 0
    assert widths[0] != widths[1]
