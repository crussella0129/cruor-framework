"""The README: that it says what it must, and names nothing that is not there."""

import re
import subprocess
import tomllib

from helpers import ROOT

README = (ROOT / "README.md").read_text(encoding="utf-8")
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
    assert README.startswith("# The Cruor framework\n")
    assert "gives a web page the look called **Cruentous Atonement**" in FLOWED
    assert "Cruentous Atonement" in FLOWED
    assert "is not in the kit yet" in FLOWED
    assert "The first release, 0.1.0, holds the fonts alone" in FLOWED


def test_readme_says_of_the_look_only_its_name():
    # Until the look is in the kit, the paragraph that first names it says
    # its name and what it is set in, and stops. The sprint that builds the
    # look changes this test with the README.
    first = " ".join(README.split("\n\n")[1].split())
    assert first == (
        "A kit that gives a web page the look called **Cruentous Atonement**, "
        "set in Cruor."
    )


def test_readme_lists_eight_families():
    assert len(FAMILIES) == 8
    for family in FAMILIES:
        assert f"| {family} |" in README, family
    assert "four styles: Regular, Bold, Italic and Bold Italic" in FLOWED


def test_readme_shows_linking_page():
    pages = [block for block in code_blocks() if "<link" in block]
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
    roots = ("fonts/", "examples/", "src/", "tools/", "docs/", "tests/", ".github/")
    files_at_root = {path.name for path in ROOT.iterdir() if path.is_file()}
    named = set()
    for span in code_spans():
        if span.startswith(roots) or span in files_at_root:
            named.add(span)
    assert {"fonts/fonts.css", "examples/fetch-release.mjs", "LICENSE-MIT"} <= named
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
    assert sorted(shown) == ["bundle", "check", "css", "manifest"]
    for command in shown:
        assert command in commands, command
    for span in code_spans():
        if span in ("css", "manifest", "check", "bundle"):
            assert span in commands

    # The scripts it tells a reader to run.
    assert "bash tools/run-guards.sh" in README
    assert (ROOT / "tools" / "run-guards.sh").is_file()
    assert (ROOT / ".github" / "workflows" / "release.yml").is_file()
