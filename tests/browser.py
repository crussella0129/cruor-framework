"""The means of checking a page in a browser: opening it, and measuring what
it draws.

A page is opened in a headless Chromium, with script on or off, and by
default with stillness asked for, so that nothing is in passage between two
states when a colour is read.

Contrast is measured from what is drawn. The ground behind some lettering
is read from a picture of the page taken with that lettering made clear:
the pixels within the rectangles of the text itself, or within the content
box of a control that has no element for its text. So a ground that is a
gradient, a tint over another ground, or laid by a pseudo-element or a
box's shadow is read as it is. The lettering's own shadow is taken off with
its colour: its glow is the letter's own light and not the ground it stands
on. The lettering is then held against the pixel least favourable to it.

Lettering that lies straight on the page under the look, with no ground of
its own between, is held against the page at its brightest as well: the
theme file's stone.
"""

import contextlib
import struct
import tomllib
import zlib

from playwright.sync_api import sync_playwright

from helpers import ROOT

THEME_FILE = ROOT / "look" / "theme.toml"

WINDOW = {"width": 1280, "height": 800}

# What makes some lettering clear, and only the lettering: its colour, its
# fill, its own shadow, the line beneath it, a field's caret and the words a
# field shows when it is empty.
CLEAR = """
[data-cruor-clear], [data-cruor-clear] * {
  color: transparent !important;
  -webkit-text-fill-color: transparent !important;
  text-shadow: none !important;
  text-decoration-color: transparent !important;
  caret-color: transparent !important;
}
[data-cruor-clear]::placeholder {
  color: transparent !important;
  -webkit-text-fill-color: transparent !important;
}
"""


class NotMeasured(Exception):
    """Something the browser cannot measure, with the reason."""


# -- colours ------------------------------------------------------------------


def colour(text: str) -> tuple[float, float, float, float]:
    """A colour as a stylesheet or the theme file writes it."""
    text = text.strip()
    if text.startswith("#"):
        return (*(int(text[at : at + 2], 16) for at in (1, 3, 5)), 1.0)
    inner = text[text.index("(") + 1 : text.rindex(")")].replace("/", ",")
    parts = [float(part) for part in inner.replace(",", " ").split()]
    return (parts[0], parts[1], parts[2], parts[3] if len(parts) > 3 else 1.0)


def over(top, share: float, under) -> tuple[float, float, float]:
    """One colour laid over another at a share of its strength."""
    return tuple(top[at] * share + under[at] * (1 - share) for at in range(3))


def laid(top, under) -> tuple[float, float, float]:
    """A colour that may let its ground show through, laid over it."""
    return over(top, top[3] if len(top) > 3 else 1.0, under)


def luminance(solid) -> float:
    def linear(channel: float) -> float:
        share = channel / 255
        return share / 12.92 if share <= 0.03928 else ((share + 0.055) / 1.055) ** 2.4

    return (
        0.2126 * linear(solid[0])
        + 0.7152 * linear(solid[1])
        + 0.0722 * linear(solid[2])
    )


def ratio(one, other) -> float:
    """WCAG 2's contrast between two colours with nothing showing through."""
    one, other = luminance(one), luminance(other)
    return (max(one, other) + 0.05) / (min(one, other) + 0.05)


def contrast(text, ground) -> float:
    """The contrast of lettering on a ground. Lettering that lets its ground
    show through is laid over it first."""
    ground = ground[:3]
    return ratio(laid(text, ground), ground)


def theme() -> dict:
    return tomllib.loads(THEME_FILE.read_text(encoding="utf-8"))


def stone(look: dict | None = None) -> tuple[float, float, float]:
    """The page at its brightest: the stone's sheen laid over the page at
    its opacity, and then the candle's glow laid over that at its own."""
    look = look or theme()
    page = colour(look["colour"]["page"])[:3]
    lit = over(colour(look["stone"]["sheen"]), look["stone"]["sheen-opacity"], page)
    return over(colour(look["stone"]["candle"]), look["stone"]["candle-opacity"], lit)


# -- pictures -----------------------------------------------------------------


def pixels(png: bytes) -> list[tuple[int, int, int]]:
    """The pixels of a picture the browser took, row by row."""
    assert png[:8] == b"\x89PNG\r\n\x1a\n"
    at = 8
    packed = b""
    while at < len(png):
        (length,) = struct.unpack(">I", png[at : at + 4])
        kind = png[at + 4 : at + 8]
        body = png[at + 8 : at + 8 + length]
        if kind == b"IHDR":
            width, height, depth, colour_type, _, _, interlace = struct.unpack(
                ">IIBBBBB", body
            )
            assert depth == 8 and interlace == 0 and colour_type in (2, 6)
            size = 4 if colour_type == 6 else 3
        elif kind == b"IDAT":
            packed += body
        at += 12 + length
    raw = zlib.decompress(packed)
    stride = width * size
    found = []
    before = bytearray(stride)
    for row in range(height):
        start = row * (stride + 1)
        how = raw[start]
        line = bytearray(raw[start + 1 : start + 1 + stride])
        for index in range(stride):
            left = line[index - size] if index >= size else 0
            up = before[index]
            corner = before[index - size] if index >= size else 0
            if how == 1:
                line[index] = (line[index] + left) & 255
            elif how == 2:
                line[index] = (line[index] + up) & 255
            elif how == 3:
                line[index] = (line[index] + (left + up) // 2) & 255
            elif how == 4:
                guess = left + up - corner
                near = min((left, up, corner), key=lambda value: abs(guess - value))
                line[index] = (line[index] + near) & 255
        found.extend(
            (line[index], line[index + 1], line[index + 2])
            for index in range(0, stride, size)
        )
        before = line
    return found


# -- pages --------------------------------------------------------------------


@contextlib.contextmanager
def chromium():
    """A headless Chromium that draws colours as they are written."""
    with sync_playwright() as playwright:
        engine = playwright.chromium.launch(args=["--force-color-profile=srgb"])
        try:
            yield engine
        finally:
            engine.close()


@contextlib.contextmanager
def opened(engine, address: str, *, script: bool = True, still: bool = True, **more):
    """A page, opened. Stillness is asked for unless `still` is false."""
    context = engine.new_context(
        viewport=WINDOW,
        java_script_enabled=script,
        reduced_motion="reduce" if still else "no-preference",
        **more,
    )
    page = context.new_page()
    try:
        page.goto(address)
        page.wait_for_load_state("networkidle")
        page.evaluate("document.fonts.ready.then(() => true)")
        yield page
    finally:
        context.close()


def in_passage(page, selector: str) -> list[str]:
    """What is moving on an element or anything it stands in: the names of
    running animations and transitions."""
    return page.evaluate(
        """selector => {
            const names = [];
            for (let el = document.querySelector(selector); el; el = el.parentElement) {
                for (const moving of el.getAnimations()) {
                    if (moving.playState === 'running') {
                        names.push(moving.animationName
                            || moving.transitionProperty || 'unnamed');
                    }
                }
            }
            return names;
        }""",
        selector,
    )


def _settled(page, selector: str) -> None:
    """Refuse to read a colour that may be on its way to another."""
    if not page.evaluate("matchMedia('(prefers-reduced-motion: reduce)').matches"):
        raise NotMeasured("the page was not opened with stillness asked for")
    moving = in_passage(page, selector)
    if moving:
        raise NotMeasured(f"{selector} is still in passage: {', '.join(moving)}")


def lettering(page, selector: str) -> tuple[float, float, float, float]:
    """The colour of an element's lettering. For a field that is empty, the
    colour of the words it shows then."""
    _settled(page, selector)
    found = page.evaluate(
        """selector => {
            const el = document.querySelector(selector);
            const empty = el.matches('input, textarea') && !el.value;
            const style = getComputedStyle(el, empty ? '::placeholder' : null);
            return {
                colour: style.color,
                fill: style.webkitTextFillColor,
                clip: getComputedStyle(el).backgroundClip,
            };
        }""",
        selector,
    )
    fill = colour(found["fill"]) if found["fill"].startswith("rgb") else None
    own = colour(found["colour"])
    if "text" in found["clip"] or (fill is not None and fill[3] == 0 and own[3] > 0):
        raise NotMeasured(
            f"{selector}: its letters are clear, with a ground clipped to them; "
            "a browser cannot say what colour they are drawn in"
        )
    text = fill or own
    if text[3] == 0:
        raise NotMeasured(f"{selector}: its lettering has no colour at all")
    return text


def boxes(page, selector: str) -> list[dict]:
    """Where an element's lettering is: the rectangles of its text, or the
    content box of a control that has no element for its text."""
    return page.evaluate(
        """selector => {
            const el = document.querySelector(selector);
            el.scrollIntoView({block: 'center', behavior: 'instant'});
            const round = r => ({x: Math.floor(r.left), y: Math.floor(r.top),
                width: Math.max(1, Math.ceil(r.right) - Math.floor(r.left)),
                height: Math.max(1, Math.ceil(r.bottom) - Math.floor(r.top))});
            if (el.matches('input, textarea, select')) {
                const r = el.getBoundingClientRect();
                const s = getComputedStyle(el);
                const px = name => parseFloat(s[name]) || 0;
                return [round({
                    left: r.left + px('borderLeftWidth') + px('paddingLeft'),
                    top: r.top + px('borderTopWidth') + px('paddingTop'),
                    right: r.right - px('borderRightWidth') - px('paddingRight'),
                    bottom: r.bottom - px('borderBottomWidth') - px('paddingBottom'),
                })];
            }
            const found = [];
            const walk = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
            for (let node = walk.nextNode(); node; node = walk.nextNode()) {
                if (!node.textContent.trim()) continue;
                const range = document.createRange();
                range.selectNodeContents(node);
                for (const r of range.getClientRects()) {
                    if (r.width > 0 && r.height > 0) found.push(round(r));
                }
            }
            return found;
        }""",
        selector,
    )


def ground(page, selector: str) -> set[tuple[int, int, int]]:
    """The ground behind an element's lettering, as it is drawn: every
    colour found within the lettering's boxes once the lettering is clear."""
    _settled(page, selector)
    where = boxes(page, selector)
    if not where:
        raise NotMeasured(f"{selector}: it has no lettering to stand on a ground")
    page.evaluate(
        """([selector, css]) => {
            if (!document.getElementById('cruor-clear')) {
                const style = document.createElement('style');
                style.id = 'cruor-clear';
                style.textContent = css;
                document.head.appendChild(style);
            }
            document.querySelector(selector).setAttribute('data-cruor-clear', '');
        }""",
        [selector, CLEAR],
    )
    try:
        found: set[tuple[int, int, int]] = set()
        for box in where:
            found.update(pixels(page.screenshot(clip=box)))
    finally:
        page.evaluate(
            "selector => document.querySelector(selector)"
            ".removeAttribute('data-cruor-clear')",
            selector,
        )
    return found


def on_the_page(page, selector: str) -> bool:
    """Whether an element's lettering lies straight on a page that has taken
    the look on: nothing it stands in, short of `<body>`, has a ground."""
    return page.evaluate(
        """([selector, look]) => {
            if (!document.body.classList.contains(look)) return false;
            for (let el = document.querySelector(selector); el && el !== document.body;
                    el = el.parentElement) {
                const s = getComputedStyle(el);
                const clear = /rgba\\(.*, 0\\)|transparent/.test(s.backgroundColor);
                if (!clear || s.backgroundImage !== 'none') return false;
            }
            return true;
        }""",
        [selector, theme()["class"]],
    )


def stands_at(page, selector: str) -> float:
    """The contrast an element's lettering stands at: against the least
    favourable pixel of the ground drawn behind it, and, if it lies straight
    on the page under the look, against the stone at its brightest too."""
    text = lettering(page, selector)
    grounds = [tuple(float(part) for part in pixel) for pixel in ground(page, selector)]
    if on_the_page(page, selector):
        grounds.append(stone())
    return min(contrast(text, under) for under in grounds)
