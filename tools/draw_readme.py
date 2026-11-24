"""Draws the repository's front page from its words and the fonts.

A page of Markdown cannot link a stylesheet, name a font or colour its own
ground, so README.md shows one picture: the page's words set in Cruor on the
stone, in the look's colours. The words are kept as text in
assets/readme/text.md, and the picture is a link to them, since no one can
copy a command out of a picture. The letters are drawn as outlines taken
from the font files, so the picture needs no font, no stylesheet and no
other file to show as it should.

    python -I tools/draw_readme.py           writes the picture and README.md
    python -I tools/draw_readme.py --check   fails if either is not current
    python -I tools/draw_readme.py --check <folder>
                                             the same, of a copy of the
                                             repository in <folder>

To change the front page, change assets/readme/text.md and run this again.
It reads the Markdown that file uses and no more: headings, paragraphs,
bold, italic, code and links within a line, tables of two columns, fenced
code, lists, and the two marks `<!-- specimen -->` and `<!-- sigil -->`.
"""

import re
import sys
import tomllib
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont

# Where the words and the picture are kept.
FOLDER = "assets/readme"
TEXT = "text.md"
PICTURE = "page.svg"

# What a reader who cannot see the picture is told in its place.
ALT = (
    "The Cruor Framework: a kit that gives a web page the look called "
    "Cruentous Atonement, set in Cruor. This page is a picture, drawn in "
    "Cruor. Follow it to read the same words as text."
)
README = (
    "<!-- This page is drawn. Its words are kept in assets/readme/text.md:\n"
    "     change them there, then run `python -I tools/draw_readme.py`. -->\n"
    f'<a href="{FOLDER}/{TEXT}"><img src="{FOLDER}/{PICTURE}" alt="{ALT}" '
    'width="100%"></a>\n'
)

# What the masthead says beneath the title.
LOOK = "Cruentous Atonement"
NOTE = "This page is a picture. Select it to read the same words as text."

# The picture is this wide, and a page scales it to its own column.
WIDTH = 880
MARGIN = 44
COLUMN = WIDTH - 2 * MARGIN

# The look's colours, by role.
GROUND = "#0a0708"
PANEL = "#110b0c"
SUNKEN = "#170e0f"
BONE = "#cbb5ab"
WEATHERED = "#9d8a82"
CLOTTED = "#5a1a1c"
INSCRIPTION = "#d50210"
VEIN = "#ff3b2f"
ARTERIAL = "#ff2a1a"
POOLED = "#ba1a1a"
SCORED = "#3a0a0b"
SALMON = ("#ff9a8a", "#ec5658")

# The families: the title, the headings, the text, and code.
TITLE = "Cruor Thornamental Regular"
HEADINGS = "Cruor Lite Regular"
RUNNING = "Cruor Sans Regular"
FIXED = "Cruor Sans Mono"

STYLES = ["Regular", "Bold", "Italic", "Bold Italic"]

# How text is set: (the size of its letters, the size of code within it, the
# distance from one line to the next). Running text is an inscription, and
# is never smaller than 24. Small things are set smaller, in bone.
PROSE = (24, 21, 36)
CELL = (19, 17, 28)
CODE = (18, 18, 27)

# The briar, one square to a character. It repeats along the masthead's foot.
BRIAR = [
    "................................",
    "................................",
    "............................a...",
    "...a..........a.......bb...c....",
    "..c..........c.......bb...cc....",
    ".cc.dddddd..cc......bb..dddd....",
    "ddddeeeeeedddd......ddddeeeedddd",
    "eeeefccf.feeeeddddddeeeedf.eeeee",
    ".f....c.ghf..eeeeeeed.f.....fccf",
    ".......a.hh.....fccf..........c.",
    "..................c............a",
    "...................a............",
]
BRIAR_COLOURS = {
    "a": "#ff4b4b",
    "b": "#5c1416",
    "c": "#8a1c1c",
    "d": POOLED,
    "e": "#6e1012",
    "f": SCORED,
    "g": VEIN,
    "h": INSCRIPTION,
}
BRIAR_SQUARE = 3

# Within a line: code, bold, italic, and a link.
INLINE = re.compile(r"`([^`]+)`|\*\*([^*]+)\*\*|\*([^*]+)\*|\[([^\]]+)\]\(([^)\s]+)\)")


def number(value: float) -> str:
    """A number as the picture writes it: two places at most, and no more
    characters than it needs."""
    text = f"{value:.2f}".rstrip("0").rstrip(".")
    return "0" if text in ("", "-0") else text


def number_fine(value: float) -> str:
    """A scale, which needs more places than a position does."""
    return f"{value:.5f}".rstrip("0").rstrip(".")


# ---------------------------------------------------------------------------
# The words
# ---------------------------------------------------------------------------


def pieces(text: str) -> list[tuple[str, str]]:
    """A line of the words as pieces, each (how it is set, what it says)."""
    found = []
    at = 0
    for mark in INLINE.finditer(text):
        if mark.start() > at:
            found.append(("plain", text[at : mark.start()]))
        code, bold, italic, link, _address = mark.groups()
        if code is not None:
            found.append(("code", code))
        elif bold is not None:
            found.append(("bold", bold))
        elif italic is not None:
            found.append(("italic", italic))
        else:
            found.append(("link", link))
        at = mark.end()
    if at < len(text):
        found.append(("plain", text[at:]))
    for style, said in found:
        if style != "code" and re.search(r"[`*\[\]]", said):
            raise SystemExit(f"{FOLDER}/{TEXT}: this is not read: {said!r}")
    return found


def blocks(text: str) -> list[tuple]:
    """The words as blocks, in order: ("heading", level, words),
    ("words", line), ("table", rows), ("code", lines), ("list", items),
    ("specimen",) and ("sigil",)."""
    lines = text.split("\n")
    found: list[tuple] = []
    at = 0
    while at < len(lines):
        line = lines[at]
        if not line.strip():
            at += 1
        elif line.startswith("```"):
            end = lines.index("```", at + 1)
            found.append(("code", lines[at + 1 : end]))
            at = end + 1
        elif heading := re.fullmatch(r"(#{1,3}) (.+)", line):
            found.append(("heading", len(heading.group(1)), heading.group(2)))
            at += 1
        elif mark := re.fullmatch(r"<!-- (specimen|sigil) -->", line):
            found.append((mark.group(1),))
            at += 1
        elif line.startswith("|"):
            rows = []
            while at < len(lines) and lines[at].startswith("|"):
                rows.append([cell.strip() for cell in lines[at].strip("|").split("|")])
                at += 1
            if any(len(row) != 2 for row in rows) or set(rows[1]) != {"---"}:
                raise SystemExit(f"{FOLDER}/{TEXT}: a table has two columns")
            found.append(("table", [rows[0], *rows[2:]]))
        elif line.startswith("- "):
            items = []
            while at < len(lines) and lines[at].startswith(("- ", "  ")):
                if lines[at].startswith("- "):
                    items.append(lines[at][2:])
                else:
                    items[-1] += " " + lines[at].strip()
                at += 1
            found.append(("list", items))
        else:
            words = []
            while at < len(lines) and lines[at].strip():
                if lines[at].startswith(("```", "#", "|", "- ", "<!--")):
                    break
                words.append(lines[at].strip())
                at += 1
            found.append(("words", " ".join(words)))
    return found


# ---------------------------------------------------------------------------
# The fonts
# ---------------------------------------------------------------------------


class Face:
    """One font file, read for its outlines and its widths."""

    def __init__(self, path: Path):
        font = TTFont(path)
        self.stem = path.stem
        self.units = font["head"].unitsPerEm
        self.cap = font["OS/2"].sCapHeight
        self.ascent = font["hhea"].ascent
        self.descent = font["hhea"].descent
        self.names = font.getBestCmap()
        self.outlines = font.getGlyphSet()
        self.widths = font["hmtx"]

    def glyph(self, character: str) -> str:
        if ord(character) not in self.names:
            raise SystemExit(f"{self.stem} has no {character!r}")
        return self.names[ord(character)]

    def outline(self, glyph: str) -> str:
        pen = SVGPathPen(self.outlines)
        self.outlines[glyph].draw(pen)
        return pen.getCommands()

    def width(self, text: str, size: float) -> float:
        units = sum(self.widths[self.glyph(character)][0] for character in text)
        return units * size / self.units


class Faces:
    """The fonts of the repository, opened as they are asked for."""

    def __init__(self, root: Path):
        self.folder = root / "fonts"
        listed = tomllib.loads(
            (self.folder / "families.toml").read_text(encoding="utf-8")
        )["family"]
        self.stems = {family["name"]: family["stem"] for family in listed}
        self.opened: dict[str, Face] = {}

    def families(self) -> list[str]:
        return list(self.stems)

    def face(self, family: str, style: str = "Regular") -> Face:
        name = f"{self.stems[family]}-{style.replace(' ', '')}"
        if name not in self.opened:
            self.opened[name] = Face(self.folder / f"{name}.woff2")
        return self.opened[name]

    def of(self, style: str) -> Face:
        """The face a piece of text is set in."""
        if style == "code":
            return self.face(FIXED)
        return self.face(
            RUNNING, {"bold": "Bold", "italic": "Italic"}.get(style, "Regular")
        )


# ---------------------------------------------------------------------------
# The page
# ---------------------------------------------------------------------------


class Page:
    """The picture: the stone, and what is set on it from the top down."""

    def __init__(self, faces: Faces):
        self.faces = faces
        self.defs: list[str] = []
        self.body: list[str] = []
        self.glyphs: dict[tuple[str, str], str] = {}
        self.defined: set[str] = set()
        # Everything the picture says, in the order it is drawn.
        self.said: list[str] = []
        # How far down the page is filled.
        self.y = 0.0

    def define(self, name: str, markup: str) -> None:
        if name not in self.defined:
            self.defined.add(name)
            self.defs.append(markup)

    # -- letters ------------------------------------------------------------

    def letters(self, face: Face, text: str, size: float, x: float, y: float) -> str:
        """The outlines of a run of text, its left end at x and its baseline
        at y. Each glyph is kept once and used where it falls."""
        self.said.append(text)
        placed = []
        pen = 0
        for character in text:
            glyph = face.glyph(character)
            key = (face.stem, glyph)
            if key not in self.glyphs:
                outline = face.outline(glyph)
                self.glyphs[key] = f"g{len(self.glyphs)}" if outline else ""
                if outline:
                    self.defs.append(f'<path id="{self.glyphs[key]}" d="{outline}"/>')
            if self.glyphs[key]:
                at = f' x="{pen}"' if pen else ""
                placed.append(f'<use href="#{self.glyphs[key]}"{at}/>')
            pen += face.widths[glyph][0]
        scale = size / face.units
        return (
            f'<g transform="translate({number(x)} {number(y)}) '
            f'scale({number_fine(scale)} {number_fine(-scale)})">'
            + "".join(placed)
            + "</g>"
        )

    def glow(self, name: str, size: float, strength: float, cut: bool) -> str:
        """The faint light the blood gives off; under carved letters, the
        dark edge of the cut as well."""
        name = f"{name}{number(size)}".replace(".", "-")
        self.define(
            name,
            f'<filter id="{name}" x="-10%" y="-100%" width="120%" height="300%" '
            'color-interpolation-filters="sRGB">'
            + (
                '<feDropShadow dx="0" dy="1" stdDeviation="0" '
                'flood-color="#000000" flood-opacity="0.9"/>'
                if cut
                else ""
            )
            + f'<feDropShadow dx="0" dy="0" stdDeviation="{number(size * strength)}" '
            f'flood-color="{INSCRIPTION}" flood-opacity="0.22"/>'
            "</filter>",
        )
        return name

    def carved(self, face: Face, text: str, size: float, x: float, y: float) -> None:
        """Large letters are channels: the blood catches the light at the
        top and settles dark at the foot."""
        self.define(
            "pour",
            '<linearGradient id="pour" gradientUnits="userSpaceOnUse" '
            f'x1="0" y1="{face.ascent}" x2="0" y2="{face.descent}">'
            f'<stop offset="0" stop-color="{ARTERIAL}"/>'
            f'<stop offset="0.48" stop-color="{INSCRIPTION}"/>'
            f'<stop offset="1" stop-color="{POOLED}"/>'
            "</linearGradient>",
        )
        edge = number(0.5 * face.units / size)
        self.body.append(
            f'<g filter="url(#{self.glow("cut", size, 0.15, True)})" '
            f'fill="url(#pour)" stroke="{POOLED}" stroke-opacity="0.45" '
            f'stroke-width="{edge}">' + self.letters(face, text, size, x, y) + "</g>"
        )

    def plain(
        self, face: Face, text: str, size: float, x: float, y: float, fill: str
    ) -> None:
        self.body.append(
            f'<g fill="{fill}">' + self.letters(face, text, size, x, y) + "</g>"
        )

    # -- text that runs and breaks ------------------------------------------

    def measure(self, style: str, text: str, setting: tuple) -> float:
        size = setting[1] if style == "code" else setting[0]
        return self.faces.of(style).width(text, size)

    def lines(self, line: list[tuple[str, str]], setting: tuple, width: float) -> list:
        """The pieces broken into lines no wider than the width. A line
        breaks only at a space."""
        # Words that touch stay together, whatever they are set in.
        atoms: list[list[tuple[str, str]]] = [[]]
        gaps: list[str] = []
        for style, said in line:
            for part in re.findall(r"\S+|\s+", said):
                if part.isspace():
                    if atoms[-1]:
                        atoms.append([])
                        gaps.append(style)
                else:
                    atoms[-1].append((style, part))
        if not atoms[-1]:
            atoms.pop()
            gaps = gaps[: max(len(atoms) - 1, 0)]

        broken: list[list[tuple[str, str]]] = []
        used = 0.0
        for count, atom in enumerate(atoms):
            wide = sum(self.measure(style, said, setting) for style, said in atom)
            gap = gaps[count - 1] if count else ""
            space = self.measure(gap, " ", setting) if gap else 0.0
            if broken and used + space + wide <= width:
                broken[-1].append((gap, " "))
                used += space
            else:
                broken.append([])
                used = 0.0
            broken[-1].extend(atom)
            used += wide

        # Neighbours set alike are one run.
        joined = []
        for row in broken:
            runs: list[list[str]] = []
            for style, said in row:
                if runs and runs[-1][0] == style:
                    runs[-1][1] += said
                else:
                    runs.append([style, said])
            joined.append([(style, said) for style, said in runs])
        return joined

    def set(
        self,
        line: list[tuple[str, str]],
        setting: tuple,
        x: float,
        top: float,
        width: float,
        inscription: bool,
    ) -> float:
        """Set pieces of text from the top down, and say how tall they
        came to. An inscription is crimson and glows; small text is bone."""
        size, code_size, leading = setting
        grounds: list[str] = []
        ink: list[str] = []
        code: list[str] = []
        links: list[str] = []
        rows = self.lines(line, setting, width)
        cap = size * self.faces.of("plain").cap / self.faces.of("plain").units
        for count, row in enumerate(rows):
            baseline = top + count * leading + (leading + cap) / 2
            at = x
            for style, said in row:
                face = self.faces.of(style)
                wide = self.measure(style, said, setting)
                if style == "code":
                    grounds.append(
                        f'<rect x="{number(at - 3)}" '
                        f'y="{number(baseline - code_size)}" '
                        f'width="{number(wide + 6)}" '
                        f'height="{number(code_size * 1.3)}" fill="{SUNKEN}"/>'
                    )
                    code.append(self.letters(face, said, code_size, at, baseline))
                elif style == "link":
                    links.append(self.letters(face, said, size, at, baseline))
                    links.append(
                        f'<rect x="{number(at)}" y="{number(baseline + 3)}" '
                        f'width="{number(wide)}" height="1" opacity="0.45"/>'
                    )
                else:
                    ink.append(self.letters(face, said, size, at, baseline))
                at += wide
        self.body.extend(grounds)
        if ink and inscription:
            light = self.glow("light", size, 0.3, False)
            self.body.append(
                f'<g filter="url(#{light})" fill="{INSCRIPTION}">'
                + "".join(ink)
                + "</g>"
            )
        elif ink:
            self.body.append(f'<g fill="{BONE}">' + "".join(ink) + "</g>")
        if code:
            self.define(
                "salmon",
                '<linearGradient id="salmon" gradientUnits="userSpaceOnUse" '
                f'x1="0" y1="{self.faces.of("code").cap}" x2="0" y2="0">'
                f'<stop offset="0" stop-color="{SALMON[0]}"/>'
                f'<stop offset="1" stop-color="{SALMON[1]}"/>'
                "</linearGradient>",
            )
            self.body.append('<g fill="url(#salmon)">' + "".join(code) + "</g>")
        if links:
            self.body.append(f'<g fill="{VEIN}">' + "".join(links) + "</g>")
        return len(rows) * leading

    # -- the parts of the page ----------------------------------------------

    def masthead(self, words: str) -> None:
        """The title, the look's name, and the briar along the foot."""
        self.define(
            "candle",
            '<radialGradient id="candle" cx="0" cy="0" r="1" '
            'gradientTransform="translate(0.5 -0.08) scale(0.8 0.55)">'
            '<stop offset="0" stop-color="#ff3c28" stop-opacity="0.03"/>'
            '<stop offset="0.7" stop-color="#ff3c28" stop-opacity="0"/>'
            "</radialGradient>",
        )
        self.body.append(f'<rect width="{WIDTH}" height="900" fill="url(#candle)"/>')
        title = self.faces.face(TITLE)
        size = 76
        self.carved(title, words, size, (WIDTH - title.width(words, size)) / 2, 142)

        look = self.faces.face(HEADINGS)
        size = 30
        light = self.glow("light", size, 0.3, False)
        self.body.append(
            f'<g filter="url(#{light})" fill="{INSCRIPTION}">'
            + self.letters(look, LOOK, size, (WIDTH - look.width(LOOK, size)) / 2, 202)
            + "</g>"
        )
        note = self.faces.face(RUNNING)
        size = 16
        self.plain(
            note, NOTE, size, (WIDTH - note.width(NOTE, size)) / 2, 240, WEATHERED
        )

        squares = []
        for row, line in enumerate(BRIAR):
            column = 0
            while column < len(line):
                letter = line[column]
                run = 1
                while column + run < len(line) and line[column + run] == letter:
                    run += 1
                if letter != ".":
                    squares.append(
                        f'<rect x="{column}" y="{row}" width="{run}" height="1" '
                        f'fill="{BRIAR_COLOURS[letter]}"/>'
                    )
                column += run
        wide = len(BRIAR[0]) * BRIAR_SQUARE
        tall = len(BRIAR) * BRIAR_SQUARE
        self.define(
            "briar",
            f'<pattern id="briar" width="{wide}" height="{tall}" '
            f'patternUnits="userSpaceOnUse" viewBox="0 0 {len(BRIAR[0])} '
            f'{len(BRIAR)}" shape-rendering="crispEdges">'
            + "".join(squares)
            + "</pattern>",
        )
        self.body.append(
            f'<g transform="translate(0 262)"><rect width="{WIDTH}" '
            f'height="{tall}" fill="url(#briar)"/></g>'
        )
        self.y = 262 + tall + 30

    def heading(self, level: int, words: str) -> None:
        if level == 1:
            self.masthead(words)
            return
        face = self.faces.face(HEADINGS)
        size, above, below = {2: (40, 26, 30), 3: (30, 12, 28)}[level]
        self.y += above
        baseline = self.y + size * face.cap / face.units
        self.carved(face, words, size, MARGIN, baseline)
        self.y = baseline
        if level == 2:
            self.hairline(self.y + 14)
            self.y += 14
        self.y += below

    def hairline(self, y: float) -> None:
        """One line of crimson fading out at both ends, with a faint glow
        and a dark scored line beneath."""
        self.define(
            "hairline",
            '<linearGradient id="hairline">'
            f'<stop offset="0" stop-color="{INSCRIPTION}" stop-opacity="0"/>'
            f'<stop offset="0.18" stop-color="{INSCRIPTION}"/>'
            f'<stop offset="0.82" stop-color="{POOLED}"/>'
            f'<stop offset="1" stop-color="{POOLED}" stop-opacity="0"/>'
            "</linearGradient>",
        )
        self.define(
            "haze",
            '<filter id="haze" x="-5%" y="-1500%" width="110%" height="3100%">'
            '<feGaussianBlur stdDeviation="3"/></filter>',
        )
        line = f'x="{MARGIN}" width="{COLUMN}" height="1"'
        self.body.append(
            f'<rect {line} y="{number(y)}" fill="{INSCRIPTION}" opacity="0.45" '
            'filter="url(#haze)"/>'
        )
        self.body.append(
            f'<rect {line} y="{number(y + 1)}" fill="{SCORED}" opacity="0.9"/>'
        )
        self.body.append(f'<rect {line} y="{number(y)}" fill="url(#hairline)"/>')

    def words(self, line: str) -> None:
        self.y += self.set(pieces(line), PROSE, MARGIN, self.y, COLUMN, True) + 20

    def listed(self, items: list[str]) -> None:
        indent = 30
        for item in items:
            middle = self.y + PROSE[2] / 2
            self.body.append(
                f'<path d="M{MARGIN + 10} {number(middle - 5)}l5 5l-5 5l-5 -5z" '
                f'fill="{POOLED}"/>'
            )
            self.y += self.set(
                pieces(item), PROSE, MARGIN + indent, self.y, COLUMN - indent, True
            )
            self.y += 6
        self.y += 14

    def code(self, lines: list[str]) -> None:
        """Code is small, so it speaks in bone, on a sunken ground."""
        size, _, leading = CODE
        pad = 18
        face = self.faces.face(FIXED)
        tall = len(lines) * leading + 2 * pad
        self.body.append(
            f'<rect x="{MARGIN + 0.5}" y="{number(self.y + 0.5)}" '
            f'width="{COLUMN - 1}" height="{number(tall - 1)}" fill="{SUNKEN}" '
            f'stroke="{CLOTTED}"/>'
        )
        cap = size * face.cap / face.units
        runs = []
        for count, line in enumerate(lines):
            if face.width(line, size) > COLUMN - 2 * pad:
                raise SystemExit(f"{FOLDER}/{TEXT}: too long a line of code: {line}")
            baseline = self.y + pad + count * leading + (leading + cap) / 2
            if line.strip():
                inset = len(line) - len(line.lstrip(" "))
                x = MARGIN + pad + face.width(" " * inset, size)
                runs.append(self.letters(face, line.strip(), size, x, baseline))
        self.body.append(f'<g fill="{BONE}">' + "".join(runs) + "</g>")
        self.y += tall + 24

    def table(self, rows: list[list[str]]) -> None:
        """A table is small, so it speaks in bone, between clotted rules."""
        pad_x, pad_y = 14, 9
        leading = CELL[2]
        first = [
            [("bold", row[0])] if count == 0 else pieces(row[0])
            for count, row in enumerate(rows)
        ]
        second = [
            [("bold", row[1])] if count == 0 else pieces(row[1])
            for count, row in enumerate(rows)
        ]
        natural = max(
            sum(self.measure(style, said, CELL) for style, said in cell)
            for cell in first
        )
        left = min(natural, 250) + 2 * pad_x
        right = COLUMN - left
        top = self.y
        self.body.append(
            f'<rect x="{MARGIN}" y="{number(top)}" width="{COLUMN}" '
            f'height="{leading + 2 * pad_y}" fill="{PANEL}"/>'
        )
        rules = []
        for one, other in zip(first, second, strict=True):
            tall = max(
                len(self.lines(one, CELL, left - 2 * pad_x)),
                len(self.lines(other, CELL, right - 2 * pad_x)),
            )
            self.set(one, CELL, MARGIN + pad_x, self.y + pad_y, left - 2 * pad_x, False)
            self.set(
                other,
                CELL,
                MARGIN + left + pad_x,
                self.y + pad_y,
                right - 2 * pad_x,
                False,
            )
            self.y += tall * leading + 2 * pad_y
            rules.append(f"M{MARGIN} {number(self.y - 0.5)}h{COLUMN}")
        rules.pop()
        rules.append(f"M{number(MARGIN + left - 0.5)} {number(top)}V{number(self.y)}")
        self.body.append(f'<path d="{"".join(rules)}" stroke="{CLOTTED}" fill="none"/>')
        self.body.append(
            f'<rect x="{MARGIN + 0.5}" y="{number(top + 0.5)}" width="{COLUMN - 1}" '
            f'height="{number(self.y - top - 1)}" fill="none" stroke="{CLOTTED}"/>'
        )
        self.y += 24

    def specimen(self) -> None:
        """Each family's name in its own letters, and each style's in its
        own."""
        pitch = 46
        for family in self.faces.families():
            baseline = self.y + 30
            light = self.glow("light", 28, 0.3, False)
            self.body.append(
                f'<g filter="url(#{light})" fill="{INSCRIPTION}">'
                + self.letters(self.faces.face(family), family, 28, MARGIN, baseline)
                + "</g>"
            )
            x = MARGIN + 430.0
            for style in STYLES:
                face = self.faces.face(family, style)
                self.plain(face, style, 18, x, baseline, BONE)
                x += face.width(style, 18) + 22
            self.y += pitch
        self.y += 18

    def sigil(self) -> None:
        """A sigil between two clotted rules."""
        self.define(
            "clotted",
            '<linearGradient id="clotted">'
            f'<stop offset="0" stop-color="{CLOTTED}" stop-opacity="0"/>'
            f'<stop offset="0.18" stop-color="{CLOTTED}"/>'
            f'<stop offset="0.44" stop-color="{CLOTTED}"/>'
            f'<stop offset="0.44" stop-color="{CLOTTED}" stop-opacity="0"/>'
            f'<stop offset="0.56" stop-color="{CLOTTED}" stop-opacity="0"/>'
            f'<stop offset="0.56" stop-color="{CLOTTED}"/>'
            f'<stop offset="0.82" stop-color="{CLOTTED}"/>'
            f'<stop offset="1" stop-color="{CLOTTED}" stop-opacity="0"/>'
            "</linearGradient>",
        )
        middle = self.y + 26
        self.body.append(
            f'<rect x="{MARGIN}" y="{number(middle - 0.5)}" width="{COLUMN}" '
            'height="1" fill="url(#clotted)"/>'
        )
        self.body.append(
            f'<g transform="translate({number(WIDTH / 2 - 14)} '
            f'{number(middle - 14)}) scale(0.875)" fill="none" stroke="{POOLED}" '
            'stroke-width="1.3" stroke-linecap="round">'
            '<circle cx="16" cy="16" r="11.5"/>'
            '<path d="M6.6 10.6h18.8L16 27z"/>'
            '<path d="M16 1.5v29M11.5 6.5h9"/>'
            f'<circle cx="16" cy="15.2" r="1.9" fill="{POOLED}" stroke="none"/>'
            "</g>"
        )
        self.y += 52 + 20

    # -- the whole ----------------------------------------------------------

    def stone(self, height: int) -> list[str]:
        """The ground: obsidian with broad glints and streaks of iron, laid
        in tiles, and darkness at the page's sides."""
        tile = 720
        self.defs.insert(
            0,
            '<filter id="glints" x="0" y="0" width="100%" height="100%" '
            'color-interpolation-filters="sRGB">'
            '<feTurbulence type="fractalNoise" baseFrequency="0.0022 0.0034" '
            'numOctaves="4" seed="7" stitchTiles="stitch" result="swell"/>'
            '<feSpecularLighting in="swell" surfaceScale="20" '
            'specularConstant="1.2" specularExponent="18" '
            'lighting-color="#ffffff" result="lit">'
            '<feDistantLight azimuth="235" elevation="38"/>'
            "</feSpecularLighting>"
            '<feComponentTransfer in="lit" result="glint">'
            '<feFuncR type="table" tableValues="0 0.114 0.182 0.227"/>'
            '<feFuncG type="table" tableValues="0 0.083 0.132 0.165"/>'
            '<feFuncB type="table" tableValues="0 0.086 0.138 0.173"/>'
            '<feFuncA type="table" tableValues="0 0.4 0.9 1"/>'
            "</feComponentTransfer>"
            '<feTurbulence type="fractalNoise" baseFrequency="0.0011 0.017" '
            'numOctaves="2" seed="29" stitchTiles="stitch" result="vein"/>'
            '<feColorMatrix in="vein" type="matrix" values="0 0 0 0 0.29 '
            '0 0 0 0 0.09 0 0 0 0 0.063 5 0 0 0 -3.3" result="iron"/>'
            '<feComposite in="glint" in2="iron" operator="over"/>'
            "</filter>"
            f'<pattern id="stone" width="{tile}" height="{tile}" '
            'patternUnits="userSpaceOnUse">'
            f'<rect width="{tile}" height="{tile}" filter="url(#glints)"/>'
            "</pattern>"
            '<linearGradient id="sides">'
            '<stop offset="0" stop-color="#000000" stop-opacity="0.72"/>'
            '<stop offset="0.16" stop-color="#000000" stop-opacity="0"/>'
            '<stop offset="0.84" stop-color="#000000" stop-opacity="0"/>'
            '<stop offset="1" stop-color="#000000" stop-opacity="0.72"/>'
            "</linearGradient>",
        )
        whole = f'width="{WIDTH}" height="{height}"'
        return [
            f'<rect {whole} fill="{GROUND}"/>',
            f'<rect {whole} fill="url(#stone)" opacity="0.3"/>',
            f'<rect {whole} fill="url(#sides)"/>',
        ]

    def markup(self) -> str:
        height = round(self.y + 24)
        ground = self.stone(height)
        return (
            '<svg xmlns="http://www.w3.org/2000/svg" '
            f'viewBox="0 0 {WIDTH} {height}" width="{WIDTH}" '
            f'height="{height}" role="img">\n'
            "<title>The Cruor Framework</title>\n"
            "<defs>\n"
            + "\n".join(self.defs)
            + "\n</defs>\n"
            + "\n".join(ground + self.body)
            + "\n</svg>\n"
        )


def page(root: Path) -> Page:
    """The front page, laid out from its words."""
    text = (root / FOLDER / TEXT).read_text(encoding="utf-8")
    found = blocks(text)
    if not found or found[0][:2] != ("heading", 1):
        raise SystemExit(f"{FOLDER}/{TEXT}: the first line is the title")
    drawn = Page(Faces(root))
    for block in found:
        kind = block[0]
        if kind == "heading":
            if block[1] == 1 and drawn.y:
                raise SystemExit(f"{FOLDER}/{TEXT}: there is one title")
            drawn.heading(block[1], block[2])
        elif kind == "words":
            drawn.words(block[1])
        elif kind == "table":
            drawn.table(block[1])
        elif kind == "code":
            drawn.code(block[1])
        elif kind == "list":
            drawn.listed(block[1])
        elif kind == "specimen":
            drawn.specimen()
        else:
            drawn.sigil()
    return drawn


def main(arguments: list[str]) -> int:
    check = "--check" in arguments
    places = [argument for argument in arguments if argument != "--check"]
    if len(places) > 1 or any(place.startswith("-") for place in places):
        print(__doc__, file=sys.stderr)
        return 2
    root = Path(places[0]) if places else Path(__file__).resolve().parent.parent
    folder = root / FOLDER
    made = {
        root / "README.md": ("README.md", README),
        folder / PICTURE: (f"{FOLDER}/{PICTURE}", page(root).markup()),
    }

    if not check:
        for path, (name, content) in made.items():
            path.write_text(content, encoding="utf-8", newline="\n")
            print(f"{name}: written")
        return 0

    faults = []
    for path, (name, content) in made.items():
        if not path.is_file():
            faults.append(f"{name}: missing")
        elif path.read_bytes() != content.encode("utf-8"):
            faults.append(f"{name}: not current")
    for kept in sorted(folder.iterdir()):
        if kept.name not in (TEXT, PICTURE):
            faults.append(f"{FOLDER}/{kept.name}: the front page does not show it")
    for fault in faults:
        print(fault, file=sys.stderr)
    if faults:
        print(
            "Run `python -I tools/draw_readme.py` to draw the page again.",
            file=sys.stderr,
        )
        return 1
    print(f"README.md and {FOLDER}/{PICTURE} are current")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
