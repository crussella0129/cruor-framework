"""The front page's words: that they say what they must, and name nothing
that is not there. The words are kept as text beside the picture README.md
shows; see test_readme_pictures.py for the picture."""

import re
import subprocess
import tomllib

import parts
from helpers import ROOT

README = (ROOT / "assets" / "readme" / "text.md").read_text(encoding="utf-8")
# The README with its lines joined, so a sentence can be found across them.
FLOWED = " ".join(README.split())

FAMILIES = [
    family["name"]
    for family in tomllib.loads(
        (ROOT / "fonts" / "families.toml").read_text(encoding="utf-8")
    )["family"]
]


def code_blocks() -> list[str]:
    return re.findall(r"```[a-z]*\n(.*?)```", README, re.DOTALL)


def code_spans() -> list[str]:
    outside_blocks = re.sub(r"```.*?```", "", README, flags=re.DOTALL)
    return re.findall(r"`([^`\n]+)`", outside_blocks)


def sentences() -> list[str]:
    return re.split(r"(?<=[.:])\s+", FLOWED)


def test_readme_says_what_the_kit_is():
    assert README.startswith("# The Cruor Framework\n")
    assert "gives a web page the look called **Cruentous Atonement**" in FLOWED
    # The look is in the kit, with the fonts and the furniture, and the kit
    # holds no script.
    assert "is not in the kit yet" not in FLOWED
    assert "The look is in the kit" in FLOWED
    for held in ("Cruor's web fonts", "one theme file", "the look's furniture"):
        assert held in FLOWED, held
    assert "the kit holds no script" in FLOWED
    assert "The first release, 0.1.0, holds the fonts alone" in FLOWED
    assert "a release from 0.2.0 holds the look as well" in FLOWED


LOOK = ["fonts.css", "tokens.css", "cruentous-atonement.css", "furniture.css"]


def test_readme_shows_taking_the_look_on():
    # One block of HTML links the four stylesheets, in the order they are
    # read, and sets the class on the body.
    pages = [block for block in code_blocks() if "cruentous-atonement.css" in block]
    assert len(pages) == 1
    linked = re.findall(r'<link rel="stylesheet" href="([^"]+)">', pages[0])
    assert [address.rsplit("/", 1)[-1] for address in linked] == LOOK
    for address in linked:
        assert (ROOT / address).is_file(), address
    assert '<body class="cruentous-atonement">' in pages[0]
    assert "A page that does not set the class is not touched" in FLOWED


def test_readme_names_every_part():
    spans = code_spans()
    assert len(parts.PARTS) == 25
    for part in parts.PARTS:
        assert part.css_class in spans, part.name
    # And no class that is not a part's.
    named = {span for span in spans if re.fullmatch(r"cruor-[a-z]+", span)}
    assert named == set(parts.classes())


def test_readme_shows_a_parts_html():
    # One block holds parts as a page would write them: each class it uses
    # is a part's, and is set on the element the furniture dresses.
    shown = [block for block in code_blocks() if 'class="cruor-' in block]
    assert len(shown) == 1
    used = re.findall(r'<(\w+) class="(cruor-[a-z]+)"', shown[0])
    assert ("button", "cruor-button") in used and ("input", "cruor-field") in used
    for _, css_class in used:
        assert css_class in parts.classes(), css_class
    # A state is asked for as HTML asks for it.
    assert 'aria-invalid="true"' in shown[0]
    assert "A state is asked for as HTML asks for it" in FLOWED


def test_readme_says_what_a_release_holds():
    about = [sentence for sentence in sentences() if "from 0.2.0" in sentence]
    held = [sentence for sentence in about if "`manifest.json`" in sentence]
    assert len(held) == 1
    for name in ("theme.toml", *LOOK[1:]):
        assert f"`{name}`" in held[0], name
        assert (ROOT / "look" / name).is_file(), name
    assert "The showroom is no part of a release" in FLOWED


SHOWROOM = "https://crussella0129.github.io/cruor-framework/showroom/"


def test_readme_points_to_the_showroom():
    assert f"]({SHOWROOM})" in README
    # The address is the one the site is published at: the repository's
    # pages, and the folder the site keeps the showroom in.
    assert (ROOT / "showroom" / "index.html").is_file()
    assert "That address answers once the showroom is published" in FLOWED
    assert "serve a copy of the repository and open `showroom/index.html`" in FLOWED


def test_readme_lists_eight_families():
    assert len(FAMILIES) == 8
    for family in FAMILIES:
        assert f"| {family} |" in README, family
    assert "four styles: Regular, Bold, Italic and Bold Italic" in FLOWED


def test_readme_shows_linking_page():
    # A page that takes the fonts alone: it links their stylesheet and names
    # a family for itself.
    pages = [block for block in code_blocks() if "<style>" in block]
    assert len(pages) == 1
    page = pages[0]
    assert re.search(r'<link rel="stylesheet" href="[^"]*fonts\.css">', page)
    named = re.findall(r'font-family: "([^"]+)"', page)
    assert named, "the page names a family"
    for family in named:
        assert family in FAMILIES, family


def test_readme_explains_weight_and_style():
    about_styles = [
        sentence
        for sentence in sentences()
        if "`font-weight`" in sentence and "`font-style`" in sentence
    ]
    assert len(about_styles) == 1
    assert "bold and italic" in about_styles[0]

    about_the_name = [
        sentence for sentence in sentences() if '"Cruor Sans Regular"' in sentence
    ]
    assert any(
        "the last word is part of the family's name, not a style" in sentence
        for sentence in about_the_name
    )
    assert (
        '`font-family: "Cruor Sans Regular"; font-weight: bold` is the Bold of '
        "Cruor Sans Regular" in FLOWED
    )


def test_readme_gives_release_address():
    assert (
        "https://github.com/crussella0129/cruor-framework/releases/download/"
        "v<version>/<file>" in README
    )
    for name in [
        "`fonts.css`",
        "`OFL.txt`",
        "`LICENSE-MIT`",
        "`LICENSE-APACHE`",
        "`manifest.json`",
        "`cruor-framework-v<version>.zip`",
    ]:
        assert name in README, name


def test_readme_shows_fetch_example():
    shown = [block for block in code_blocks() if "fetch-release.mjs" in block]
    assert len(shown) == 1
    command = " ".join(shown[0].replace("\\\n", " ").split())
    assert re.fullmatch(
        r"node examples/fetch-release\.mjs "
        r"https://github\.com/crussella0129/cruor-framework/releases/download/"
        r"v0\.1\.0/ "
        r"\S+ --manifest-sha256 <[^>]+>",
        command,
    ), command
    assert "Pin the manifest's SHA-256 in your build" in FLOWED


def test_readme_states_check_requirements():
    assert "bash tools/run-guards.sh" in README
    for needed in [
        "`rust-toolchain.toml`",
        "`tools/requirements.txt`",
        "the browser Playwright drives",
        "`python -m playwright install chromium`",
        "Node 20 or newer",
    ]:
        assert needed in FLOWED, needed


def test_readme_states_terms():
    assert (
        "offered under the SIL Open Font License 1.1, with the font name Cruor "
        "reserved" in FLOWED
    )
    assert "`fonts/OFL.txt` is what states the fonts' terms" in FLOWED
    assert "offered under `MIT OR Apache-2.0`" in FLOWED
    assert "`LICENSE-MIT`" in FLOWED
    assert "`LICENSE-APACHE`" in FLOWED


def test_readme_names_existing_paths_and_commands():
    # Every path of the repository that the README gives in code marks.
    roots = (
        "fonts/",
        "look/",
        "showroom/",
        "examples/",
        "src/",
        "tools/",
        "assets/",
        "docs/",
        "tests/",
        ".github/",
    )
    files_at_root = {path.name for path in ROOT.iterdir() if path.is_file()}
    named = set()
    for span in code_spans():
        if span.startswith(roots) or span in files_at_root:
            named.add(span)
    assert {
        "fonts/fonts.css",
        "examples/fetch-release.mjs",
        "tools/draw_readme.py",
        "tools/draw_showroom.py",
        "tools/build-site.sh",
        "look/",
        "look/theme.toml",
        "look/tokens.css",
        "look/cruentous-atonement.css",
        "look/furniture.css",
        "look/THEME.md",
        "showroom/",
        "showroom/index.html",
        ".github/workflows/pages.yml",
        "assets/readme/",
        "assets/readme/text.md",
        "LICENSE-MIT",
    } <= named
    for path in sorted(named):
        assert (ROOT / path).exists(), path

    # Every command of the tool that the README shows.
    help_text = subprocess.run(
        ["cargo", "run", "--quiet", "--", "--help"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    commands = re.findall(r"^\s+([a-z]+)\s", help_text.split("Commands:")[1], re.M)
    shown = re.findall(r"cargo run --release -- ([a-z]+)", README)
    assert sorted(shown) == ["bundle", "check", "css", "look", "manifest"]
    # Every command the tool has is shown, but the one that prints its help.
    assert sorted(shown) == sorted(set(commands) - {"help"})
    for span in ("css", "manifest", "look", "check", "bundle"):
        assert span in code_spans(), span

    # The scripts it tells a reader to run.
    assert "bash tools/run-guards.sh" in README
    assert (ROOT / "tools" / "run-guards.sh").is_file()
    assert (ROOT / ".github" / "workflows" / "release.yml").is_file()
