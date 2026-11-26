"""Draws the showroom's pictures from the maps the front page keeps.

The front page shows a statue weeping blood, and a briar. The showroom is a
place of the same kind, and shows them too. A page of HTML shows a picture
from a file, so each is written out as one here: the two pictures of the
statue from their maps of squares in assets/readme, and the briar turned
upright, as a stem that climbs.

The front page's door is written out here as well, the same picture, with
door.json beside it: where the doorway, and the eyes and the mouth of the
head over it, lie in the picture, for the showroom's entrance to open it by.

    python -I tools/draw_showroom.py           writes the pictures
    python -I tools/draw_showroom.py --check   fails if one is not current
    python -I tools/draw_showroom.py --check <folder>
                                               the same, of a copy of the
                                               repository in <folder>

The pictures are the showroom's own. They are no part of the kit, and no
release holds them.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import draw_readme

# Where the pictures are written.
FOLDER = "showroom"

# The statue's pictures, by the name of their map, and how many pixels of a
# page one square is drawn at when a page gives the picture no size.
STATUE = {"weeping-face": 4, "weeping-profile": 4}

# The stem of thorns: the front page's briar, turned a quarter.
STEM = "briar-stem"
STEM_SQUARE = draw_readme.BRIAR_SQUARE

# The door to the showroom, as the front page draws it, and where its parts
# lie: the doorway, the eyes and the mouth of the head over it.
DOOR = "door.svg"
DOOR_PARTS = "door.json"

CREDIT = (
    "Michelangelo's David, from a photograph by Jörg Bittner Unna offered "
    "under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/); cut "
    "from its ground, darkened, given tears of blood and reduced to squares. "
    "This picture is offered under CC BY 4.0 as well."
)


def kept(root: Path, name: str) -> tuple[dict[str, str], list[str]]:
    """A map of squares: each letter's colour, and the rows of letters."""
    path = root / draw_readme.FOLDER / f"{name}.txt"
    if not path.is_file():
        raise SystemExit(f"{draw_readme.FOLDER}/{name}.txt: missing")
    head, _, rest = path.read_text(encoding="utf-8").partition("\n\n")
    colours = dict(line.split() for line in head.splitlines())
    rows = rest.splitlines()
    wide = len(rows[0])
    for row, line in enumerate(rows):
        if len(line) != wide or set(line) - set(colours) - {"."}:
            raise SystemExit(
                f"{draw_readme.FOLDER}/{name}.txt: row {row + 1} is not right"
            )
    return colours, rows


def squares(colours: dict[str, str], rows: list[str]) -> str:
    """The squares of a map as one path to a colour. Where the map has a
    `.` nothing is drawn, and the page's own stone shows."""
    runs: dict[str, list[str]] = {letter: [] for letter in colours}
    for row, line in enumerate(rows):
        column = 0
        while column < len(line):
            letter = line[column]
            run = 1
            while column + run < len(line) and line[column + run] == letter:
                run += 1
            if letter != ".":
                runs[letter].append(f"M{column} {row}h{run}v1h-{run}z")
            column += run
    return "".join(
        f'<path fill="{colours[letter]}" d="{"".join(found)}"/>'
        for letter, found in runs.items()
        if found
    )


def picture(colours: dict[str, str], rows: list[str], square: int, told: str) -> str:
    """One picture, as a file a page can show."""
    wide, tall = len(rows[0]), len(rows)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {wide} {tall}" '
        f'width="{wide * square}" height="{tall * square}" '
        'shape-rendering="crispEdges">\n'
        f"<!-- {told} Drawn by tools/draw_showroom.py; to change it, change "
        "what that script reads and run it again. -->\n"
        f"{squares(colours, rows)}\n</svg>\n"
    )


def upright(rows: list[str]) -> list[str]:
    """A map turned a quarter, so that what ran along now climbs."""
    return [
        "".join(row[column] for row in reversed(rows)) for column in range(len(rows[0]))
    ]


def pictures(root: Path) -> dict[str, str]:
    """Every picture of the showroom, by the name of its file."""
    made = {}
    for name, square in STATUE.items():
        colours, rows = kept(root, name)
        made[f"{name}.svg"] = picture(colours, rows, square, CREDIT)
    made[f"{STEM}.svg"] = picture(
        draw_readme.BRIAR_COLOURS,
        upright(draw_readme.BRIAR),
        STEM_SQUARE,
        "The framework's briar, as a stem that climbs.",
    )
    # The front page's door, the same picture, and beside it where its parts
    # lie, for the showroom's entrance to open it by.
    door = draw_readme.door(root)
    made[DOOR] = door.markup(draw_readme.DOOR_TITLE)
    made[DOOR_PARTS] = json.dumps(door.door, indent=2, sort_keys=True) + "\n"
    return made


def main(arguments: list[str]) -> int:
    check = "--check" in arguments
    places = [argument for argument in arguments if argument != "--check"]
    if len(places) > 1 or any(place.startswith("-") for place in places):
        print(__doc__, file=sys.stderr)
        return 2
    root = Path(places[0]) if places else Path(__file__).resolve().parent.parent
    made = pictures(root)

    if not check:
        for name, content in made.items():
            (root / FOLDER / name).write_text(content, encoding="utf-8", newline="\n")
            print(f"{FOLDER}/{name}: written")
        return 0

    faults = []
    for name, content in made.items():
        path = root / FOLDER / name
        if not path.is_file():
            faults.append(f"{FOLDER}/{name}: missing")
        elif path.read_bytes() != content.encode("utf-8"):
            faults.append(f"{FOLDER}/{name}: not current")
    for found in sorted((root / FOLDER).glob("*.svg")):
        if found.name not in made:
            faults.append(f"{FOLDER}/{found.name}: this script does not draw it")
    for fault in faults:
        print(fault, file=sys.stderr)
    if faults:
        print(
            "Run `python -I tools/draw_showroom.py` to draw them again.",
            file=sys.stderr,
        )
        return 1
    print(f"the pictures of {FOLDER}/ are current")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
