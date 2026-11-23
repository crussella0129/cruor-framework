"""Check that each font is what its rule says it is.

    python -I tools/check_fonts.py fonts

A stylesheet can name the wrong file, and a file can hold the wrong style;
neither shows until a page asks for a bold and is given something else. This
opens every font the list of families calls for and sets what the font says
of itself (its family, its style, its weight, its slant) against the list
and against its `@font-face` rule in fonts.css. It exits 0 if all agree, and
otherwise names each file and the field that disagrees.
"""

import pathlib
import re
import sys
import tomllib

from fontTools.ttLib import TTFont

# For each style, as a file's name writes it: the style's name as a font
# gives it, its weight, and whether it leans.
STYLES = {
    "Regular": ("Regular", 400, False),
    "Bold": ("Bold", 700, False),
    "Italic": ("Italic", 400, True),
    "BoldItalic": ("Bold Italic", 700, True),
}


def read_rules(css: str) -> dict[str, dict]:
    """The `@font-face` rules of a stylesheet, by the file each one names."""
    rules = {}
    for block in re.finditer(r"@font-face\s*\{(.*?)\}", css, re.DOTALL):
        declarations = {}
        for declaration in block.group(1).split(";"):
            if ":" in declaration:
                name, value = declaration.split(":", 1)
                declarations[name.strip()] = value.strip()
        address = re.search(r'url\("([^"]*)"\)', declarations.get("src", ""))
        if not address:
            continue
        rules[address.group(1)] = {
            "family": declarations.get("font-family", "").strip('"'),
            "weight": declarations.get("font-weight", ""),
            "slant": declarations.get("font-style", ""),
        }
    return rules


def read_font(path: pathlib.Path) -> dict:
    """What a font says of itself."""
    font = TTFont(path)
    names = font["name"]
    return {
        "family": names.getDebugName(1),
        "style": names.getDebugName(2),
        "weight": font["OS/2"].usWeightClass,
        # The italic bit of the font's selection flags.
        "italic": bool(font["OS/2"].fsSelection & 1),
    }


def check(folder: pathlib.Path) -> list[str]:
    """Every disagreement in a folder of fonts, each as one line."""
    families = tomllib.loads((folder / "families.toml").read_text(encoding="utf-8"))
    rules = read_rules((folder / "fonts.css").read_text(encoding="utf-8"))
    faults = []
    listed = set()
    for family in families["family"]:
        for suffix, (style, weight, italic) in STYLES.items():
            name = f"{family['stem']}-{suffix}.woff2"
            listed.add(name)
            path = folder / name
            if not path.is_file():
                faults.append(f"{name}: file: the list calls for it and it is missing")
                continue
            font = read_font(path)
            if font["family"] != family["name"]:
                faults.append(
                    f"{name}: family: the font says {font['family']!r}, "
                    f"the list says {family['name']!r}"
                )
            if font["style"] != style:
                faults.append(
                    f"{name}: style: the font says {font['style']!r}, "
                    f"its file's name says {style!r}"
                )
            if font["weight"] != weight:
                faults.append(
                    f"{name}: weight: the font says {font['weight']}, "
                    f"its file's name says {weight}"
                )
            if font["italic"] != italic:
                faults.append(
                    f"{name}: slant: the font says "
                    f"{'italic' if font['italic'] else 'upright'}, its file's name "
                    f"says {'italic' if italic else 'upright'}"
                )
            rule = rules.get(name)
            if rule is None:
                faults.append(f"{name}: rule: no rule in fonts.css names it")
                continue
            if rule["family"] != font["family"]:
                faults.append(
                    f"{name}: family: the font says {font['family']!r}, "
                    f"its rule says {rule['family']!r}"
                )
            if rule["weight"] != str(font["weight"]):
                faults.append(
                    f"{name}: weight: the font says {font['weight']}, "
                    f"its rule says {rule['weight']}"
                )
            if rule["slant"] != ("italic" if font["italic"] else "normal"):
                faults.append(
                    f"{name}: slant: the font says "
                    f"{'italic' if font['italic'] else 'upright'}, its rule says "
                    f"{rule['slant']}"
                )
    for name in sorted(set(rules) - listed):
        faults.append(f"{name}: rule: fonts.css names it and the list does not")
    return faults


def main(arguments: list[str]) -> int:
    if len(arguments) != 1:
        print(
            "usage: python -I tools/check_fonts.py <folder of fonts>", file=sys.stderr
        )
        return 2
    folder = pathlib.Path(arguments[0])
    faults = check(folder)
    for fault in faults:
        print(fault, file=sys.stderr)
    if faults:
        print(f"{len(faults)} disagreement(s) in {folder}", file=sys.stderr)
        return 1
    print(f"every font in {folder} agrees with the list and with its rule")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
