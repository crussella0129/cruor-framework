"""Draws the repository's front page from its words and the fonts.

A page of Markdown cannot link a stylesheet, name a font or colour its own
ground, so README.md shows a picture: the page's words set in Cruor on the
stone, in the look's colours. Beneath it a second picture, a door drawn in
the briar, is a link to the showroom. The words are kept as text in
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
code, lists, and the marks `<!-- specimen -->`, `<!-- sigil -->` and
`<!-- picture <name> -->`, which shows the picture kept beside the words as
`<name>.txt`: a map of squares, one letter a square.
"""

import math
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
# The door to the showroom: a second picture, a link to where the showroom
# is published.
DOOR = "door.svg"
SHOWROOM = "https://crussella0129.github.io/cruor-framework/showroom/"
DOOR_ALT = (
    "A door to the showroom of the Cruor framework, where every part of the "
    "look is shown in use. Follow it to open the showroom."
)
README = (
    "<!-- This page is drawn. Its words are kept in assets/readme/text.md:\n"
    "     change them there, then run `python -I tools/draw_readme.py`. -->\n"
    f'<a href="{FOLDER}/{TEXT}"><img src="{FOLDER}/{PICTURE}" alt="{ALT}" '
    'width="100%"></a>\n'
    f'<a href="{SHOWROOM}"><img src="{FOLDER}/{DOOR}" alt="{DOOR_ALT}" '
    'width="100%"></a>\n'
)

# The crest of the door: David's head, face on, kept beside the words as a
# map of squares like the statue's; how many squares wide it is, and where
# its head is set, above the door, which is drawn this much lower to make
# room for it.
CREST = "door-crest"
CREST_WIDE = 46
CREST_TOP = -90
DOOR_DROP = 96

# What the door says.
DOOR_NAME = "The Showroom"
DOOR_WORDS = "Every part of the look, in use"
DOOR_NOTE = "Select this picture to go in."

# The picture at the head of the page, and the side of one of its squares.
HERO = "weeping-face"
SQUARE = 4

# What the masthead says beneath the title.
LOOK = "Cruentous Atonement"
NOTE = "This page is a picture. Select it to read the same words as text."

# The picture is this wide, and a page scales it to its own column.
WIDTH = 880
MARGIN = 44
COLUMN = WIDTH - 2 * MARGIN

# The look is read from its theme file: every colour by its role, and the
# four families by what they set. Nothing of the look is written out here
# but the briar's own squares, further down.
THEME = "look/theme.toml"


class Look:
    """The look's colours and families, as its theme file gives them."""

    def __init__(self, root: Path):
        path = root / THEME
        if not path.is_file():
            raise SystemExit(f"{THEME}: missing")
        theme = tomllib.loads(path.read_text(encoding="utf-8"))
        # The families that set the title, the headings, the text and code.
        self.font: dict[str, str] = theme["font"]
        self.name: str = theme["name"]
        colours = dict(theme["colour"])
        colours["candle"] = theme["stone"]["candle"]
        for role, written in colours.items():
            colour, share = self.solid(role, written)
            setattr(self, role.replace("-", "_"), colour)
            setattr(self, role.replace("-", "_") + "_share", share)
        self.candle_share = number_fine(theme["stone"]["candle-opacity"])
        self.sheen_share = number_fine(theme["stone"]["sheen-opacity"])

    @staticmethod
    def solid(role: str, written: str) -> tuple[str, str]:
        """A colour as a picture takes it: its six figures, and how much of
        it is laid on."""
        if re.fullmatch(r"#[0-9a-f]{6}", written):
            return written, "1"
        parts = re.fullmatch(r"rgba\((\d+), (\d+), (\d+), ([0-9.]+)\)", written)
        if not parts:
            raise SystemExit(f"{THEME}: colour.{role} is not a colour: {written}")
        red, green, blue = (int(parts.group(index)) for index in (1, 2, 3))
        return f"#{red:02x}{green:02x}{blue:02x}", parts.group(4)


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
    "d": "#ba1a1a",
    "e": "#6e1012",
    "f": "#3a0a0b",
    "g": "#ff3b2f",
    "h": "#d50210",
}
BRIAR_SQUARE = 3

# The door's furniture, in letters the door gives colours to: Z and S are
# bone, F, G and H are flame.
FINIAL = [
    ".Z.",
    "ZSZ",
    ".Z.",
]
CANDELABRA = [
    "..G.....G.....G..",
    ".GHG...GHG...GHG.",
    ".HFH...HFH...HFH.",
    "..F.....F.....F..",
    "..Z.....Z.....Z..",
    "..Z.....Z.....Z..",
    "..Z.....Z.....Z..",
    ".SZS...SZS...SZS.",
    "..S.....S.....S..",
    "..SS....S....SS..",
    "...SS...S...SS...",
    "....SSSSZSSSS....",
    "........Z........",
    "......ZZZZZ......",
    ".....ZZZZZZZ.....",
    ".....ZKKZKKZ.....",
    ".....ZKZZZKZ.....",
    "......ZZKZZ......",
    "......SZSZS......",
    ".......SSS.......",
    "........Z........",
    "........Z........",
    "........Z........",
    "........Z........",
    ".......SZS.......",
    "......SSZSS......",
    ".....SS.Z.SS.....",
    "....SS..Z..SS....",
    "...SSSSSZSSSSS...",
]
# A bat's wing rising from the end of a ledge, its root at the foot of the
# first column.
WING = [
    "..........K",
    ".........KT",
    "........KTK",
    ".......KTUK",
    "....K.KTUUK",
    "...KTKTUUUK",
    "..KTUTUUUK.",
    ".KTUUUUUK..",
    "KTUUUUUK...",
    "KTUUUUK....",
    "KTUUUK.....",
    "KTUK.......",
]
# The damned the door is carved of, in bone: a body climbing with its arms
# up, and a face screaming. K is hollow.
BODY = [
    "Z.....Z",
    "S.....S",
    ".S.Z.S.",
    ".SZSZS.",
    "..SKS..",
    "..TKT..",
    ".ZSSSZ.",
    "ZSTSTSZ",
    ".UTSTU.",
    "..TST..",
    "..UTU..",
    "..T.T..",
    ".T...T.",
    ".T...U.",
    "U.....U",
    "U......",
]
FACE = [
    "..ZZZ..",
    ".ZSSSZ.",
    "ZSKSKSZ",
    "ZSKSKSZ",
    "TSSUSST",
    ".TSKST.",
    ".TUKUT.",
    "..TKT..",
]


def frange(start: float, stop: float, step: float = 0.5) -> list[float]:
    """Evenly spaced values from start toward stop."""
    count = max(int(abs(stop - start) / abs(step)), 1)
    return [start + step * index for index in range(count + 1)]


class Squares:
    """Squares of the briar's colours, laid on a grid one square to a cell."""

    def __init__(self):
        self.cells: dict[tuple[int, int], str] = {}

    def put(self, x: float, y: float, letter: str, over: bool = True) -> None:
        key = (round(x), round(y))
        if over or key not in self.cells:
            self.cells[key] = letter

    def picture(self, rows: list[str], x: float, y: float) -> None:
        for row, line in enumerate(rows):
            for column, letter in enumerate(line):
                if letter != ".":
                    self.put(x + column, y + row, letter)

    def vine(self, way: list[tuple[float, float]], sway: float, thorns: int) -> None:
        """Two stems twisting about a way, with thorns and leaves along
        them. The light falls from above on the left."""
        along, last = 0.0, -1
        for index in range(1, len(way) - 1):
            (x0, y0), (x1, y1) = way[index - 1], way[index + 1]
            x, y = way[index]
            length = math.hypot(x1 - x0, y1 - y0) or 1.0
            tx, ty = (x1 - x0) / length, (y1 - y0) / length
            nx, ny = -ty, tx
            along += math.hypot(x - way[index - 1][0], y - way[index - 1][1])
            mark = int(along)
            new, last = mark != last, mark
            for strand, phase in ((1, 0.0), (-1, math.pi)):
                bend = sway * math.sin(along / 4.0 + phase)
                px, py = x + nx * bend, y + ny * bend
                self.put(px + 1, py + 1, "e", over=False)
                self.put(px, py, "d")
                if not new:
                    continue
                if mark % thorns == 0:
                    side = strand if (mark // thorns) % 2 else -strand
                    dx, dy = nx * side - tx * 0.6, ny * side - ty * 0.6
                    self.put(px + dx, py + dy, "c")
                    self.put(px + 2 * dx, py + 2 * dy, "c")
                    self.put(px + 3 * dx, py + 3 * dy, "a")
                elif mark % (thorns * 3) == thorns // 2 and strand == 1:
                    self.put(px - nx * 1.5, py - ny * 1.5, "f")
                    self.put(px - nx * 2.5 + tx, py - ny * 2.5 + ty, "f")
                    self.put(px - nx * 2.5, py - ny * 2.5, "b")

    def drip(self, x: float, y: float, length: int) -> None:
        """Blood running down from (x, y), and the drop at its end."""
        for down in range(length):
            self.put(x, y + down, "h")
        self.put(x, y + length, "g")
        self.put(x + 1, y + length, "h")
        self.put(x, y + length + 1, "h")
        self.put(x + 1, y + length + 1, "b")

    def markup(self, side: int, palette: dict | None = None) -> str:
        """The squares, `side` wide. A letter the briar does not hold is
        painted as `palette` gives it: (colour, how much of it is laid on)."""
        palette = {
            **{letter: (colour, "1") for letter, colour in BRIAR_COLOURS.items()},
            **(palette or {}),
        }
        runs: dict[str, list[str]] = {}
        rows: dict[int, dict[int, str]] = {}
        for (x, y), letter in self.cells.items():
            rows.setdefault(y, {})[x] = letter
        for y in sorted(rows):
            row = rows[y]
            columns = sorted(row)
            index = 0
            while index < len(columns):
                x, letter = columns[index], row[columns[index]]
                run = 1
                while (
                    index + run < len(columns)
                    and columns[index + run] == x + run
                    and row[x + run] == letter
                ):
                    run += 1
                runs.setdefault(letter, []).append(f"M{x} {y}h{run}v1h-{run}z")
                index += run
        return (
            f'<g transform="scale({side})" shape-rendering="crispEdges">'
            + "".join(
                f'<path fill="{palette[letter][0]}"'
                + (
                    f' fill-opacity="{palette[letter][1]}"'
                    if palette[letter][1] != "1"
                    else ""
                )
                + f' d="{"".join(found)}"/>'
                for letter, found in sorted(runs.items())
            )
            + "</g>"
        )


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
    ("specimen",), ("sigil",) and ("picture", name)."""
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
        elif mark := re.fullmatch(
            r"<!-- (specimen|sigil|picture) ?([a-z-]*) -->", line
        ):
            found.append((mark.group(1), mark.group(2)))
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
        self.look = Look(root)

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
            return self.face(self.look.font["code"])
        return self.face(
            self.look.font["text"],
            {"bold": "Bold", "italic": "Italic"}.get(style, "Regular"),
        )


# ---------------------------------------------------------------------------
# The page
# ---------------------------------------------------------------------------


class Page:
    """The picture: the stone, and what is set on it from the top down."""

    def __init__(self, faces: Faces, folder: Path):
        self.faces = faces
        self.look = faces.look
        # Where the pictures are kept, and which of them the page shows.
        self.folder = folder
        self.shown: list[str] = []
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
                f'flood-color="{self.look.shadow}" flood-opacity="0.9"/>'
                if cut
                else ""
            )
            + f'<feDropShadow dx="0" dy="0" stdDeviation="{number(size * strength)}" '
            f'flood-color="{self.look.inscription}" flood-opacity="0.22"/>'
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
            f'<stop offset="0" stop-color="{self.look.heading_top}"/>'
            f'<stop offset="0.48" stop-color="{self.look.inscription}"/>'
            f'<stop offset="1" stop-color="{self.look.heading_foot}"/>'
            "</linearGradient>",
        )
        edge = number(0.5 * face.units / size)
        self.body.append(
            f'<g filter="url(#{self.glow("cut", size, 0.15, True)})" '
            f'fill="url(#pour)" stroke="{self.look.heading_foot}" '
            'stroke-opacity="0.45" '
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
                        f'height="{number(code_size * 1.3)}" '
                        f'fill="{self.look.sunken}"/>'
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
                f'<g filter="url(#{light})" fill="{self.look.inscription}">'
                + "".join(ink)
                + "</g>"
            )
        elif ink:
            self.body.append(f'<g fill="{self.look.text}">' + "".join(ink) + "</g>")
        if code:
            self.define(
                "salmon",
                '<linearGradient id="salmon" gradientUnits="userSpaceOnUse" '
                f'x1="0" y1="{self.faces.of("code").cap}" x2="0" y2="0">'
                f'<stop offset="0" stop-color="{self.look.chip_top}"/>'
                f'<stop offset="1" stop-color="{self.look.chip_foot}"/>'
                "</linearGradient>",
            )
            self.body.append('<g fill="url(#salmon)">' + "".join(code) + "</g>")
        if links:
            self.body.append(
                f'<g fill="{self.look.inscription_link}">' + "".join(links) + "</g>"
            )
        return len(rows) * leading

    # -- the parts of the page ----------------------------------------------

    def picture(
        self, name: str, top: float, left: float | None = None, side: int = SQUARE
    ) -> float:
        """A picture kept as a map of squares, its head at `top`, set in the
        middle of the page or with its left edge at `left`, each square
        `side` wide. Says how tall it is. Where the map has a `.` the stone
        shows."""
        kept = self.folder / f"{name}.txt"
        if not kept.is_file():
            raise SystemExit(f"{FOLDER}/{name}.txt: missing")
        head, _, rest = kept.read_text(encoding="utf-8").partition("\n\n")
        colours = dict(line.split() for line in head.splitlines())
        rows = rest.splitlines()
        wide = len(rows[0])
        runs: dict[str, list[str]] = {letter: [] for letter in colours}
        for row, line in enumerate(rows):
            if len(line) != wide or set(line) - set(colours) - {"."}:
                raise SystemExit(f"{FOLDER}/{name}.txt: row {row + 1} is not right")
            column = 0
            while column < wide:
                letter = line[column]
                run = 1
                while column + run < wide and line[column + run] == letter:
                    run += 1
                if letter != ".":
                    runs[letter].append(f"M{column} {row}h{run}v1h-{run}z")
                column += run
        if left is None:
            left = (WIDTH - wide * side) / 2
        self.body.append(
            f'<g transform="translate({number(left)} {number(top)}) scale({side})" '
            'shape-rendering="crispEdges">'
            + "".join(
                f'<path fill="{colours[letter]}" d="{"".join(found)}"/>'
                for letter, found in runs.items()
                if found
            )
            + "</g>"
        )
        self.shown.append(name)
        return len(rows) * side

    def plate(self, name: str) -> None:
        """A picture between two parts of the page."""
        self.y += 8
        self.y += self.picture(name, self.y) + 34

    def masthead(self, words: str) -> None:
        """The picture at the head, the title, the look's name, and the briar
        along the foot."""
        top = self.picture(HERO, 0) - 38
        self.define(
            "candle",
            '<radialGradient id="candle" cx="0" cy="0" r="1" '
            'gradientTransform="translate(0.5 -0.08) scale(0.8 0.55)">'
            f'<stop offset="0" stop-color="{self.look.candle}" '
            f'stop-opacity="{self.look.candle_share}"/>'
            f'<stop offset="0.7" stop-color="{self.look.candle}" stop-opacity="0"/>'
            "</radialGradient>",
        )
        self.body.append(f'<rect width="{WIDTH}" height="900" fill="url(#candle)"/>')
        title = self.faces.face(self.look.font["title"])
        size = 76
        self.carved(
            title, words, size, (WIDTH - title.width(words, size)) / 2, top + 142
        )

        look = self.faces.face(self.look.font["heading"])
        size = 30
        light = self.glow("light", size, 0.3, False)
        self.body.append(
            f'<g filter="url(#{light})" fill="{self.look.inscription}">'
            + self.letters(
                look, LOOK, size, (WIDTH - look.width(LOOK, size)) / 2, top + 202
            )
            + "</g>"
        )
        note = self.faces.face(self.look.font["text"])
        size = 16
        self.plain(
            note,
            NOTE,
            size,
            (WIDTH - note.width(NOTE, size)) / 2,
            top + 240,
            self.look.text_subdued,
        )

        tall = self.briar(top + 262)
        self.y = top + 262 + tall + 30

    def briar(self, y: float) -> float:
        """The briar the width of the page, its head at y. Says how tall it
        is."""
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
            f'<g transform="translate(0 {number(y)})"><rect width="{WIDTH}" '
            f'height="{tall}" fill="url(#briar)"/></g>'
        )
        return tall

    def doorway(self) -> None:
        """The door to the showroom: a pointed arch of carved stone with
        tracery in its head and light within, wound with the briar, hung
        with drapes tied back, between two candelabras, up two carpeted
        steps; blood runs off the edge of the floor. The name is carved
        beside it."""
        look = self.look
        cell = BRIAR_SQUARE
        # All the door is drawn lower by this much, to leave room for the
        # head above it.
        start = len(self.body)
        # Where the door stands, in squares: its middle, the half width of
        # its opening, where its arch springs, where the steps begin and
        # where the floor is.
        middle, half, spring, steps, floor = 84, 20, 64, 116, 124
        frame = 6
        apex = spring - half * 3**0.5

        def inside(x: float, y: float, wide: float) -> bool:
            """Within a pointed arch `wide` either side of the middle."""
            if y >= steps:
                return False
            if y >= spring:
                return abs(x - middle) <= wide
            return (
                math.hypot(x - (middle - wide), y - spring) <= 2 * wide
                and math.hypot(x - (middle + wide), y - spring) <= 2 * wide
            )

        def outline(wide: float) -> str:
            """The same arch as a path, in the picture's own units."""
            left, right = (middle - wide) * cell, (middle + wide) * cell
            radius = number(2 * wide * cell)
            return (
                f"M{number(left)} {steps * cell}V{spring * cell}"
                f"A{radius} {radius} 0 0 1 {number(middle * cell)} "
                f"{number((spring - wide * 3**0.5) * cell)}"
                f"A{radius} {radius} 0 0 1 {number(right)} {spring * cell}"
                f"V{steps * cell}Z"
            )

        self.define(
            "candle",
            '<radialGradient id="candle" cx="0" cy="0" r="1" '
            'gradientTransform="translate(0.5 -0.08) scale(0.8 0.55)">'
            f'<stop offset="0" stop-color="{look.candle}" '
            f'stop-opacity="{look.candle_share}"/>'
            f'<stop offset="0.7" stop-color="{look.candle}" stop-opacity="0"/>'
            "</radialGradient>",
        )
        self.define(
            "within",
            '<linearGradient id="within" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{look.heading_foot}"/>'
            f'<stop offset="0.3" stop-color="{look.blood}"/>'
            f'<stop offset="0.55" stop-color="{look.shadow}"/>'
            f'<stop offset="1" stop-color="{look.heading_foot}"/>'
            "</linearGradient>",
        )
        self.define(
            "spill",
            '<radialGradient id="spill">'
            f'<stop offset="0" stop-color="{look.candle}" stop-opacity="0.32"/>'
            f'<stop offset="1" stop-color="{look.candle}" stop-opacity="0"/>'
            "</radialGradient>",
        )
        self.body.append(f'<rect width="{WIDTH}" height="460" fill="url(#candle)"/>')
        self.body.append(
            f'<ellipse cx="{middle * cell}" cy="{steps * cell}" '
            f'rx="{half * cell * 3}" ry="30" fill="url(#spill)"/>'
        )
        # The void the door hangs in glows the colour of old blood.
        self.define(
            "void",
            '<radialGradient id="void">'
            f'<stop offset="0" stop-color="{look.blood}" stop-opacity="0.95"/>'
            f'<stop offset="0.6" stop-color="{look.blood}" stop-opacity="0.5"/>'
            f'<stop offset="1" stop-color="{look.blood}" stop-opacity="0"/>'
            "</radialGradient>",
        )
        self.body.append(
            f'<ellipse cx="{middle * cell}" cy="{70 * cell}" rx="250" ry="210" '
            'fill="url(#void)"/>'
        )
        # The light within, and through the tracery.
        self.body.append(f'<path d="{outline(half)}" fill="url(#within)"/>')
        # Each flame's light about it.
        flames = []

        squares = Squares()

        # Through the doorway, and spreading about it, blood boils: cells
        # packed close, lit at their hearts, with dark crevices between.
        def boil(x: int, y: int) -> tuple[float, float]:
            """How far a square is from the nearest cell's heart, and how
            far from the crevice between it and the next."""
            found = []
            for i in (-1, 0, 1):
                for j in (-1, 0, 1):
                    gx, gy = x // 6 + i, y // 6 + j
                    seed = ((gx * 73856093) ^ (gy * 19349663)) & 0xFFFFFF
                    px = gx * 6 + seed % 6
                    py = gy * 6 + (seed >> 6) % 6
                    found.append(math.hypot(x - px, y - py))
            found.sort()
            return found[0], found[1] - found[0]

        for y in range(0, steps):
            for x in range(middle - 64, middle + 65):
                heart, crevice = boil(x, y)
                # The mass is ragged at its edge, and darkens toward it.
                angle = math.atan2(y - 66, x - middle)
                edge = 52 + 5 * math.sin(5 * angle) + 3 * math.sin(11 * angle + 1)
                far = math.hypot((x - middle) / 1.1, y - 66) / edge
                if inside(x, y, half):
                    far = 0.0
                elif far > 1:
                    continue
                if crevice < 0.9:
                    letter = "X"
                elif far > 0.8:
                    letter = "W"
                elif crevice < 1.8 or far > 0.62:
                    letter = "V"
                elif heart < 1.6 and far < 0.4:
                    letter = "O"
                else:
                    letter = "Y"
                squares.put(x, y, letter)

        # The stone: blocks of the arch laid about its middle, courses up
        # the sides. Each block is lit where the doorway's light falls on
        # it and along its upper and left edges.
        def block(x: int, y: int) -> tuple:
            if y < spring:
                return (
                    "arch",
                    int(math.degrees(math.atan2(spring - y, x - middle)) // 11),
                )
            return (
                "side",
                (y - spring) // 6,
                x < middle,
                (x + 3 * ((y - spring) // 6 % 2)) // 7,
            )

        for y in range(int(apex - frame * 2), steps):
            for x in range(middle - half - frame - 1, middle + half + frame + 2):
                if not inside(x, y, half + frame) or inside(x, y, half):
                    continue
                here = block(x, y)
                if block(x + 1, y) != here or block(x, y + 1) != here:
                    squares.put(x, y, "K")
                elif (
                    inside(x - 1, y, half)
                    or inside(x + 1, y, half)
                    or inside(x, y + 1, half)
                ):
                    squares.put(x, y, "T")
                elif block(x - 1, y) != here or block(x, y - 1) != here:
                    squares.put(x, y, "T")
                elif not inside(x, y - 2, half + frame) or not inside(
                    x - 2, y, half + frame
                ):
                    squares.put(x, y, "K")
                else:
                    squares.put(x, y, "U")

        # Tracery in the arch's head, above a bar across the doorway: two
        # lancets and a roundel with four foils.
        bar = spring + 2
        for y in range(int(apex), bar + 2):
            for x in range(middle - half, middle + half + 1):
                if not inside(x, y, half):
                    continue
                stone = y >= bar
                for side in (-1, 1):
                    centre = middle + side * half / 2
                    lancet = inside(x - (centre - middle), y - 2, half / 2 - 0.5)
                    within = inside(x - (centre - middle), y - 2, half / 2 - 1.7)
                    stone = stone or (lancet and not within)
                stone = stone or (abs(x - middle) < 1 and y >= spring - 4)
                ring = math.hypot(x - middle, y - (spring - 21))
                stone = stone or 4.6 <= ring <= 5.9
                for dx, dy in ((2.4, 0), (-2.4, 0), (0, 2.4), (0, -2.4)):
                    foil = math.hypot(x - middle - dx, y - (spring - 21) - dy)
                    stone = stone or (1.6 <= foil <= 2.5 and ring < 4.6)
                if stone:
                    lit = not inside(x, y - 1, half) or y == bar
                    squares.put(x, y, "S" if lit else "T")

        def ledge(centre: int, top: int, reach: int) -> None:
            """A floating ledge: a slab of pale stone with a carved band
            along its face, a bat's wing rising at each end, and a bracket
            hanging beneath each end. Blood runs off it."""
            for x in range(centre - reach, centre + reach + 1):
                knot = (x - centre) % 6
                squares.put(x, top, "S")
                squares.put(x, top + 1, "T")
                squares.put(x, top + 2, "U" if knot in (2, 3) else "S")
                squares.put(x, top + 3, "S" if knot in (2, 3) else "U")
                squares.put(x, top + 4, "T")
                squares.put(x, top + 5, "K")
            for side in (-1, 1):
                end = centre + side * reach
                foot = end - side * 3
                for down in range(6, 11):
                    squares.put(foot, top + down, "T")
                    squares.put(foot - side, top + down, "U")
                    squares.put(foot + side, top + down, "K")
                squares.put(foot - side * 2, top + 6, "U")
                squares.put(foot - side * 2, top + 10, "S")
                squares.put(foot + side, top + 10, "S")
                for row, line in enumerate(WING):
                    for column, letter in enumerate(line):
                        if letter != ".":
                            squares.put(
                                end + side * column, top - len(WING) + row, letter
                            )
            squares.drip(centre - reach // 2, top + 6, 3 + reach % 4)
            squares.drip(centre + reach // 3, top + 6, 2 + reach % 3)

        ledge(middle, steps, half + frame + 10)
        # The door is split down its middle, and light shows through.
        for y in range(spring + 4, steps):
            squares.put(middle - 1, y, "K")
            squares.put(middle, y, "F")
            squares.put(middle + 1, y, "K")

        # Drapes either side, hung from a rod and tied back.
        rod = int(apex - frame * 2) - 6
        tie = 90
        for side in (-1, 1):
            outer = middle + side * (half + frame + 9)
            for y in range(rod + 1, steps):
                if y < tie:
                    width = 16 - 11 * (y - rod) / (tie - rod)
                else:
                    width = 5 + 7 * ((y - tie) / (steps - tie)) ** 0.7
                for step in range(round(width) + 1):
                    x = outer - side * step
                    fold = math.cos(2 * math.pi * 2.5 * step / max(width, 1) + y / 40)
                    if step == round(width):
                        letter = "X"
                    elif fold > 0.75:
                        letter = "Y"
                    elif fold > 0.1:
                        letter = "V"
                    elif fold > -0.5:
                        letter = "W"
                    else:
                        letter = "X"
                    squares.put(x, y, letter)
            # The cord that ties it back, and its tassel.
            for step in range(0, 6):
                squares.put(outer - side * step, tie, "Z")
                squares.put(outer - side * step, tie + 1, "S")
            for drop in range(2, 8):
                squares.put(outer - side * 2, tie + drop, "Z" if drop < 4 else "S")
            for spread in (-1, 0, 1):
                squares.put(outer - side * (2 + spread), tie + 8, "S")
        for x in range(middle - half - frame - 12, middle + half + frame + 13):
            squares.put(x, rod, "Z")
            squares.put(x, rod + 1, "U")
        for side in (-1, 1):
            end = middle + side * (half + frame + 13)
            squares.picture(FINIAL, end - 1, rod - 2)

        # A candelabra either side, the door's middle between them, each on
        # a ledge of its own.
        stand = steps - 8
        for centre in (middle - 56, middle + 56):
            left = centre - len(CANDELABRA[0]) // 2
            ledge(centre, stand, 7)
            squares.picture(CANDELABRA, left, stand - len(CANDELABRA))
            for row, line in enumerate(CANDELABRA):
                for column, letter in enumerate(line):
                    if letter == "F":
                        flames.append(
                            (
                                (left + column + 0.5) * cell,
                                (stand - len(CANDELABRA) + row) * cell,
                            )
                        )

        # The briar winds about the frame, and blood runs from the arch
        # into the doorway.
        way = []
        wide = half + frame / 2
        way += [(middle - wide, steps - 1 - t) for t in frange(0, steps - 1 - spring)]
        radius = 2 * wide
        way += [
            (middle + wide - radius * math.cos(a), spring - radius * math.sin(a))
            for a in frange(0, math.pi / 3, 0.5 / radius)
        ]
        way += [
            (middle - wide + radius * math.cos(a), spring - radius * math.sin(a))
            for a in frange(math.pi / 3, 0, -0.5 / radius)
        ]
        way += [(middle + wide, spring + t) for t in frange(0, steps - 1 - spring)]
        squares.vine(way, sway=2.4, thorns=7)
        self.writhing(squares, middle, half, frame, spring, steps)
        for across, length in ((-9, 6), (-4, 10), (5, 4), (11, 8)):
            x = middle + across
            centre = middle + half if across < 0 else middle - half
            y = spring - math.sqrt(max((2 * half) ** 2 - (x - centre) ** 2, 0))
            squares.drip(x, y + 1, length)

        words = 450
        name = self.faces.face(look.font["heading"])
        self.carved(name, DOOR_NAME, 56, words, 210)
        wide = name.width(DOOR_NAME, 56)
        squares.vine(
            [(x, 228 / cell) for x in frange(words / cell, (words + wide) / cell)],
            sway=1.0,
            thorns=5,
        )
        hang = [(274 + 3 * math.sin(t / 9), t) for t in frange(-34, 40)]
        squares.vine(hang, sway=1.0, thorns=6)
        squares.drip(274 + 3 * math.sin(40 / 9), 41, 6)
        hang = [(256 + 2 * math.sin(t / 7 + 1), t) for t in frange(-34, 22)]
        squares.vine(hang, sway=0.8, thorns=6)
        # Blood runs off the edge of the floor, under the briar.
        under = floor + len(BRIAR) - 1
        for x, length in (
            (9, 5),
            (40, 8),
            (71, 3),
            (97, 7),
            (143, 4),
            (188, 9),
            (231, 5),
            (284, 6),
        ):
            squares.drip(x, under, length)

        self.define(
            "flame",
            '<radialGradient id="flame">'
            f'<stop offset="0" stop-color="{look.candle}" stop-opacity="0.45"/>'
            f'<stop offset="1" stop-color="{look.candle}" stop-opacity="0"/>'
            "</radialGradient>",
        )
        for x, y in flames:
            self.body.append(
                f'<circle cx="{number(x)}" cy="{number(y)}" r="16" fill="url(#flame)"/>'
            )
        self.body.append(
            squares.markup(
                cell,
                {
                    # Stone, in weathered bone laid thin over the obsidian.
                    "S": (look.text_subdued, "0.85"),
                    "T": (look.text_subdued, "0.42"),
                    "U": (look.text_subdued, "0.22"),
                    "K": (look.shadow, "1"),
                    # Velvet, in the look's reds.
                    "Y": (look.heading_foot, "1"),
                    "V": (look.selection, "1"),
                    "W": (look.border, "1"),
                    "X": (look.blood, "1"),
                    # Cords and candlesticks, in bone.
                    "Z": (look.text, "1"),
                    # Flames.
                    "F": (look.chip_top, "1"),
                    "O": (look.chip_foot, "1"),
                    "G": (look.heading_top, "1"),
                    "H": (look.accent, "1"),
                },
            )
        )
        # David's head is the crest, its chin on the top of the arch.
        crest_left, crest_top = middle * cell - CREST_WIDE * cell / 2, CREST_TOP
        self.picture(CREST, crest_top, crest_left, cell)

        text = self.faces.face(look.font["text"])
        light = self.glow("light", 24, 0.3, False)
        self.body.append(
            f'<g filter="url(#{light})" fill="{look.inscription}">'
            + self.letters(text, DOOR_WORDS, 24, words, 270)
            + "</g>"
        )
        self.plain(text, DOOR_NOTE, 16, words, 300, look.text_subdued)
        self.briar(floor * cell)
        self.body[start:] = [
            f'<g transform="translate(0 {DOOR_DROP})">'
            + "".join(self.body[start:])
            + "</g>"
        ]
        self.y = (floor + len(BRIAR) + 12) * cell + DOOR_DROP

    @staticmethod
    def writhing(
        squares: "Squares", middle: int, half: int, frame: int, spring: int, steps: int
    ) -> None:
        """The door's frame is the damned: bodies climbing over one another
        up each side, some fallen head down, faces screaming about the arch,
        and the greatest at the keystone, all weeping blood."""
        wide = half + frame / 2
        for side in (-1, 1):
            centre = middle + side * wide
            for turn, y in enumerate(range(steps - 16, spring - 12, -9)):
                shape = BODY if turn % 3 != 1 else BODY[::-1]
                if (turn + (side > 0)) % 2:
                    shape = [line[::-1] for line in shape]
                lean = (turn * 5 + side) % 3 - 1
                squares.picture(shape, centre - 3 + lean, y)
            radius = 2 * wide
            for a in (0.2, 0.45, 0.7):
                x = middle - side * wide + side * radius * math.cos(a)
                y = spring - radius * math.sin(a)
                squares.picture(FACE, x - 3, y - 4)
                squares.drip(x - 1 + (side > 0), y, 2 + round(a * 4))

    def heading(self, level: int, words: str) -> None:
        if level == 1:
            self.masthead(words)
            return
        face = self.faces.face(self.look.font["heading"])
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
            f'<stop offset="0" stop-color="{self.look.inscription}" stop-opacity="0"/>'
            f'<stop offset="0.18" stop-color="{self.look.inscription}"/>'
            f'<stop offset="0.82" stop-color="{self.look.heading_foot}"/>'
            f'<stop offset="1" stop-color="{self.look.heading_foot}" stop-opacity="0"/>'
            "</linearGradient>",
        )
        self.define(
            "haze",
            '<filter id="haze" x="-5%" y="-1500%" width="110%" height="3100%">'
            '<feGaussianBlur stdDeviation="3"/></filter>',
        )
        line = f'x="{MARGIN}" width="{COLUMN}" height="1"'
        self.body.append(
            f'<rect {line} y="{number(y)}" fill="{self.look.inscription}" '
            'opacity="0.45" '
            'filter="url(#haze)"/>'
        )
        self.body.append(
            f'<rect {line} y="{number(y + 1)}" fill="{self.look.blood}" opacity="0.9"/>'
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
                f'fill="{self.look.heading_foot}"/>'
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
        face = self.faces.face(self.look.font["code"])
        tall = len(lines) * leading + 2 * pad
        self.body.append(
            f'<rect x="{MARGIN + 0.5}" y="{number(self.y + 0.5)}" '
            f'width="{COLUMN - 1}" height="{number(tall - 1)}" '
            f'fill="{self.look.sunken}" '
            f'stroke="{self.look.border}"/>'
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
        self.body.append(f'<g fill="{self.look.text}">' + "".join(runs) + "</g>")
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
            f'height="{leading + 2 * pad_y}" fill="{self.look.panel}"/>'
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
        self.body.append(
            f'<path d="{"".join(rules)}" stroke="{self.look.border}" fill="none"/>'
        )
        self.body.append(
            f'<rect x="{MARGIN + 0.5}" y="{number(top + 0.5)}" width="{COLUMN - 1}" '
            f'height="{number(self.y - top - 1)}" fill="none" '
            f'stroke="{self.look.border}"/>'
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
                f'<g filter="url(#{light})" fill="{self.look.inscription}">'
                + self.letters(self.faces.face(family), family, 28, MARGIN, baseline)
                + "</g>"
            )
            x = MARGIN + 430.0
            for style in STYLES:
                face = self.faces.face(family, style)
                self.plain(face, style, 18, x, baseline, self.look.text)
                x += face.width(style, 18) + 22
            self.y += pitch
        self.y += 18

    def sigil(self) -> None:
        """A sigil between two clotted rules."""
        self.define(
            "clotted",
            '<linearGradient id="clotted">'
            f'<stop offset="0" stop-color="{self.look.border}" stop-opacity="0"/>'
            f'<stop offset="0.18" stop-color="{self.look.border}"/>'
            f'<stop offset="0.44" stop-color="{self.look.border}"/>'
            f'<stop offset="0.44" stop-color="{self.look.border}" stop-opacity="0"/>'
            f'<stop offset="0.56" stop-color="{self.look.border}" stop-opacity="0"/>'
            f'<stop offset="0.56" stop-color="{self.look.border}"/>'
            f'<stop offset="0.82" stop-color="{self.look.border}"/>'
            f'<stop offset="1" stop-color="{self.look.border}" stop-opacity="0"/>'
            "</linearGradient>",
        )
        middle = self.y + 26
        self.body.append(
            f'<rect x="{MARGIN}" y="{number(middle - 0.5)}" width="{COLUMN}" '
            'height="1" fill="url(#clotted)"/>'
        )
        self.body.append(
            f'<g transform="translate({number(WIDTH / 2 - 14)} '
            f'{number(middle - 14)}) scale(0.875)" fill="none" '
            f'stroke="{self.look.heading_foot}" '
            'stroke-width="1.3" stroke-linecap="round">'
            '<circle cx="16" cy="16" r="11.5"/>'
            '<path d="M6.6 10.6h18.8L16 27z"/>'
            '<path d="M16 1.5v29M11.5 6.5h9"/>'
            f'<circle cx="16" cy="15.2" r="1.9" fill="{self.look.heading_foot}" '
            'stroke="none"/>'
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
            'result="lit">'
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
            f'<stop offset="0" stop-color="{self.look.vignette}" '
            f'stop-opacity="{self.look.vignette_share}"/>'
            f'<stop offset="0.16" stop-color="{self.look.vignette}" stop-opacity="0"/>'
            f'<stop offset="0.84" stop-color="{self.look.vignette}" stop-opacity="0"/>'
            f'<stop offset="1" stop-color="{self.look.vignette}" '
            f'stop-opacity="{self.look.vignette_share}"/>'
            "</linearGradient>",
        )
        whole = f'width="{WIDTH}" height="{height}"'
        return [
            f'<rect {whole} fill="{self.look.page}"/>',
            f'<rect {whole} fill="url(#stone)" opacity="{self.look.sheen_share}"/>',
            f'<rect {whole} fill="url(#sides)"/>',
        ]

    def markup(self, title: str = "The Cruor Framework") -> str:
        height = round(self.y + 24)
        ground = self.stone(height)
        return (
            '<svg xmlns="http://www.w3.org/2000/svg" '
            f'viewBox="0 0 {WIDTH} {height}" width="{WIDTH}" '
            f'height="{height}" role="img">\n'
            f"<title>{title}</title>\n"
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
    drawn = Page(Faces(root), root / FOLDER)
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
        elif kind == "picture":
            drawn.plate(block[1])
        else:
            drawn.sigil()
    return drawn


def door(root: Path) -> Page:
    """The door to the showroom."""
    drawn = Page(Faces(root), root / FOLDER)
    drawn.doorway()
    return drawn


def main(arguments: list[str]) -> int:
    check = "--check" in arguments
    places = [argument for argument in arguments if argument != "--check"]
    if len(places) > 1 or any(place.startswith("-") for place in places):
        print(__doc__, file=sys.stderr)
        return 2
    root = Path(places[0]) if places else Path(__file__).resolve().parent.parent
    folder = root / FOLDER
    drawn = page(root)
    made = {
        root / "README.md": ("README.md", README),
        folder / PICTURE: (f"{FOLDER}/{PICTURE}", drawn.markup()),
        folder / DOOR: (
            f"{FOLDER}/{DOOR}",
            door(root).markup("The door to the showroom"),
        ),
    }
    shown = {TEXT, PICTURE, DOOR} | {
        f"{name}.txt" for name in drawn.shown + door(root).shown
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
        if kept.name not in shown:
            faults.append(f"{FOLDER}/{kept.name}: the front page does not show it")
    for fault in faults:
        print(fault, file=sys.stderr)
    if faults:
        print(
            "Run `python -I tools/draw_readme.py` to draw the page again.",
            file=sys.stderr,
        )
        return 1
    print(f"README.md, {FOLDER}/{PICTURE} and {FOLDER}/{DOOR} are current")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
