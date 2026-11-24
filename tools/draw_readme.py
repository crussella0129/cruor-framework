"""Draws the README's lettering from the fonts.

A page of Markdown cannot link a stylesheet or name a font, so the README
wears the look in pictures: each heading is a slab of the stone with its
words cut in Cruor, and the README's own `alt` text says which words. The
letters are drawn as outlines taken from the font files, so a picture needs
no font, no stylesheet and no other file to show as it should.

    python -I tools/draw_readme.py           writes the pictures
    python -I tools/draw_readme.py --check   fails if a picture is not current
    python -I tools/draw_readme.py --check <folder>
                                             the same, of a copy of the
                                             repository in <folder>

To change a heading, change its `alt` text in README.md and run this again.
"""

import re
import sys
import tomllib
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont

# Where the pictures are kept, as the README names them.
FOLDER = "assets/readme"

# A heading of the README: its level, its picture and its words.
HEADING = re.compile(
    r'^<h([1-3])><img src="' + FOLDER + r'/([a-z0-9-]+\.svg)" alt="([^"]+)" '
    r'width="100%"></h\1>$',
    re.MULTILINE,
)

# The pictures that are not headings.
SPECIMEN = "specimen.svg"
SIGIL = "sigil.svg"

# Every picture is this wide, and a page scales it to its own column.
WIDTH = 880
MARGIN = 28

# The look's colours, by role.
GROUND = "#0a0708"
BONE = "#cbb5ab"
CLOTTED = "#5a1a1c"
INSCRIPTION = "#d50210"
ARTERIAL = "#ff2a1a"
POOLED = "#ba1a1a"
SCORED = "#3a0a0b"

# The families whose letters the headings and the masthead are cut in.
TITLES = "Cruor Thornamental Regular"
RUNNING = "Cruor Lite Regular"

STYLES = ["Regular", "Bold", "Italic", "Bold Italic"]

# The briar, one square to a character. It repeats along a masthead's foot.
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
    "g": "#ff3b2f",
    "h": INSCRIPTION,
}
BRIAR_SQUARE = 3


def number(value: float) -> str:
    """A number as a picture writes it: two places at most, and no more
    characters than it needs."""
    text = f"{value:.2f}".rstrip("0").rstrip(".")
    return "0" if text in ("", "-0") else text


def number_fine(value: float) -> str:
    """A scale, which needs more places than a position does."""
    return f"{value:.5f}".rstrip("0").rstrip(".")


class Face:
    """One font file, read for its outlines and its widths."""

    def __init__(self, path: Path):
        font = TTFont(path)
        self.stem = path.stem
        self.units = font["head"].unitsPerEm
        self.ascent = font["hhea"].ascent
        self.descent = font["hhea"].descent
        self.names = font.getBestCmap()
        self.outlines = font.getGlyphSet()
        self.widths = font["hmtx"]

    def glyph(self, character: str) -> str:
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


class Picture:
    """One picture: a slab of the stone, and what is cut into it."""

    def __init__(self, height: int, title: str):
        self.height = height
        self.title = title
        self.defs: list[str] = []
        self.body: list[str] = []
        self.glyphs: dict[tuple[str, str], str] = {}
        self.defined: set[str] = set()
        self.stone()

    def define(self, name: str, markup: str) -> None:
        if name not in self.defined:
            self.defined.add(name)
            self.defs.append(markup)

    def stone(self) -> None:
        """The ground: obsidian with broad glints and streaks of iron, and
        darkness at its edges."""
        self.define(
            "stone",
            '<filter id="stone" x="0" y="0" width="100%" height="100%" '
            'color-interpolation-filters="sRGB">'
            '<feTurbulence type="fractalNoise" baseFrequency="0.0022 0.0034" '
            'numOctaves="4" seed="7" result="swell"/>'
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
            'numOctaves="2" seed="29" result="vein"/>'
            '<feColorMatrix in="vein" type="matrix" values="0 0 0 0 0.29 '
            '0 0 0 0 0.09 0 0 0 0 0.063 5 0 0 0 -3.3" result="iron"/>'
            '<feComposite in="glint" in2="iron" operator="over"/>'
            "</filter>",
        )
        self.define(
            "edge",
            '<radialGradient id="edge" cx="0.5" cy="0.38" r="1.2">'
            '<stop offset="0.48" stop-color="#000000" stop-opacity="0"/>'
            '<stop offset="1" stop-color="#000000" stop-opacity="0.72"/>'
            "</radialGradient>",
        )
        whole = f'width="{WIDTH}" height="{self.height}"'
        self.body.append(f'<rect {whole} fill="{GROUND}"/>')
        self.body.append(f'<rect {whole} filter="url(#stone)" opacity="0.3"/>')
        self.body.append(f'<rect {whole} fill="url(#edge)"/>')

    def candle(self) -> None:
        """A faint warm glow from above."""
        self.define(
            "candle",
            '<radialGradient id="candle" cx="0" cy="0" r="1" '
            'gradientTransform="translate(0.5 -0.08) scale(0.8 0.55)">'
            '<stop offset="0" stop-color="#ff3c28" stop-opacity="0.03"/>'
            '<stop offset="0.7" stop-color="#ff3c28" stop-opacity="0"/>'
            "</radialGradient>",
        )
        self.body.append(
            f'<rect width="{WIDTH}" height="{self.height}" fill="url(#candle)"/>'
        )

    def letters(self, face: Face, text: str, size: float, x: float, y: float) -> str:
        """The outlines of a line of text, its left end at x and its
        baseline at y. Each glyph is kept once and used where it falls."""
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
        glow = f"glow{number(size)}".replace(".", "-")
        self.define(
            glow,
            f'<filter id="{glow}" x="-10%" y="-60%" width="120%" height="220%" '
            'color-interpolation-filters="sRGB">'
            '<feDropShadow dx="0" dy="1" stdDeviation="0" '
            'flood-color="#000000" flood-opacity="0.9"/>'
            f'<feDropShadow dx="0" dy="0" stdDeviation="{number(size * 0.15)}" '
            f'flood-color="{INSCRIPTION}" flood-opacity="0.22"/>'
            "</filter>",
        )
        edge = number(0.5 * face.units / size)
        self.body.append(
            f'<g filter="url(#{glow})" fill="url(#pour)" stroke="{POOLED}" '
            f'stroke-opacity="0.45" stroke-width="{edge}">'
            + self.letters(face, text, size, x, y)
            + "</g>"
        )

    def inscribed(self, face: Face, text: str, size: float, x: float, y: float) -> None:
        """Running text: crimson, giving off the faintest light."""
        glow = f"light{number(size)}".replace(".", "-")
        self.define(
            glow,
            f'<filter id="{glow}" x="-10%" y="-60%" width="120%" height="220%" '
            'color-interpolation-filters="sRGB">'
            f'<feDropShadow dx="0" dy="0" stdDeviation="{number(size * 0.3)}" '
            f'flood-color="{INSCRIPTION}" flood-opacity="0.22"/>'
            "</filter>",
        )
        self.body.append(
            f'<g filter="url(#{glow})" fill="{INSCRIPTION}">'
            + self.letters(face, text, size, x, y)
            + "</g>"
        )

    def small(self, face: Face, text: str, size: float, x: float, y: float) -> None:
        """Small things speak in bone."""
        self.body.append(
            f'<g fill="{BONE}">' + self.letters(face, text, size, x, y) + "</g>"
        )

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
        line = f'x="{MARGIN}" width="{WIDTH - 2 * MARGIN}" height="1"'
        self.body.append(
            f'<rect {line} y="{number(y)}" fill="{INSCRIPTION}" opacity="0.45" '
            'filter="url(#haze)"/>'
        )
        self.body.append(
            f'<rect {line} y="{number(y + 1)}" fill="{SCORED}" opacity="0.9"/>'
        )
        self.body.append(f'<rect {line} y="{number(y)}" fill="url(#hairline)"/>')

    def briar(self, y: int) -> None:
        """The briar along a masthead's foot: a stem, hooked thorns with
        blood on their points, a leaf and a cluster of berries."""
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
            f'<g transform="translate(0 {y})"><rect width="{WIDTH}" '
            f'height="{tall}" fill="url(#briar)"/></g>'
        )

    def sigil(self, y: float) -> None:
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
        self.body.append(
            f'<rect y="{number(y)}" width="{WIDTH}" height="1" fill="url(#clotted)"/>'
        )
        self.body.append(
            f'<g transform="translate({number(WIDTH / 2 - 14)} {number(y - 13.5)}) '
            f'scale(0.875)" fill="none" stroke="{POOLED}" stroke-width="1.3" '
            'stroke-linecap="round">'
            '<circle cx="16" cy="16" r="11.5"/>'
            '<path d="M6.6 10.6h18.8L16 27z"/>'
            '<path d="M16 1.5v29M11.5 6.5h9"/>'
            f'<circle cx="16" cy="15.2" r="1.9" fill="{POOLED}" stroke="none"/>'
            "</g>"
        )

    def markup(self) -> str:
        return (
            '<svg xmlns="http://www.w3.org/2000/svg" '
            f'viewBox="0 0 {WIDTH} {self.height}" width="{WIDTH}" '
            f'height="{self.height}" role="img">\n'
            + (f"<title>{self.title}</title>\n" if self.title else "")
            + "<defs>\n"
            + "\n".join(self.defs)
            + "\n</defs>\n"
            + "\n".join(self.body)
            + "\n</svg>\n"
        )


def masthead(faces: Faces, words: str) -> str:
    picture = Picture(300, words)
    picture.candle()
    title = faces.face(TITLES)
    size = 76
    picture.carved(title, words, size, (WIDTH - title.width(words, size)) / 2, 150)
    look = "Cruentous Atonement"
    running = faces.face(RUNNING)
    size = 30
    picture.inscribed(running, look, size, (WIDTH - running.width(look, size)) / 2, 214)
    picture.briar(300 - 44)
    return picture.markup()


def band(faces: Faces, level: int, words: str) -> str:
    size, height, baseline = {2: (40, 80, 51), 3: (30, 64, 40)}[level]
    picture = Picture(height, words)
    picture.carved(faces.face(TITLES), words, size, MARGIN, baseline)
    picture.hairline(height - 12)
    return picture.markup()


def specimen(faces: Faces) -> str:
    """Each family's name in its own letters, and each style's in its own."""
    families = faces.families()
    pitch = 46
    picture = Picture(2 * MARGIN + pitch * len(families) - 8, "The families of Cruor")
    for row, family in enumerate(families):
        baseline = MARGIN + 30 + pitch * row
        picture.inscribed(faces.face(family), family, 28, MARGIN, baseline)
        x = 470.0
        for style in STYLES:
            face = faces.face(family, style)
            picture.small(face, style, 18, x, baseline)
            x += face.width(style, 18) + 22
    return picture.markup()


def sigil() -> str:
    picture = Picture(64, "")
    picture.sigil(31.5)
    return picture.markup()


def pictures(root: Path) -> dict[str, str]:
    """Every picture the README shows, by file name."""
    readme = (root / "README.md").read_text(encoding="utf-8")
    faces = Faces(root)
    drawn = {}
    for level, name, words in HEADING.findall(readme):
        if name in drawn or name in (SPECIMEN, SIGIL):
            raise SystemExit(f"README.md: two pictures are named {name}")
        if level == "1":
            drawn[name] = masthead(faces, words)
        else:
            drawn[name] = band(faces, int(level), words)
    if not drawn:
        raise SystemExit("README.md: no heading names a picture")
    drawn[SPECIMEN] = specimen(faces)
    drawn[SIGIL] = sigil()
    return drawn


def main(arguments: list[str]) -> int:
    check = "--check" in arguments
    places = [argument for argument in arguments if argument != "--check"]
    if len(places) > 1 or any(place.startswith("-") for place in places):
        print(__doc__, file=sys.stderr)
        return 2
    root = Path(places[0]) if places else Path(__file__).resolve().parent.parent
    folder = root / FOLDER
    drawn = pictures(root)

    if not check:
        folder.mkdir(parents=True, exist_ok=True)
        for kept in folder.glob("*.svg"):
            if kept.name not in drawn:
                kept.unlink()
        for name, markup in drawn.items():
            (folder / name).write_text(markup, encoding="utf-8", newline="\n")
        print(f"{FOLDER}: {len(drawn)} pictures written")
        return 0

    faults = []
    for name, markup in sorted(drawn.items()):
        path = folder / name
        if not path.is_file():
            faults.append(f"{FOLDER}/{name}: missing")
        elif path.read_bytes() != markup.encode("utf-8"):
            faults.append(f"{FOLDER}/{name}: not current")
    if folder.is_dir():
        for kept in sorted(folder.iterdir()):
            if kept.name not in drawn:
                faults.append(f"{FOLDER}/{kept.name}: no heading names it")
    for fault in faults:
        print(fault, file=sys.stderr)
    if faults:
        print(
            "Run `python -I tools/draw_readme.py` to draw them again.",
            file=sys.stderr,
        )
        return 1
    print(f"{FOLDER}: {len(drawn)} pictures are current")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
