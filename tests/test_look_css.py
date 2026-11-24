"""The look's stylesheets, read as text: that every rule keeps beneath the
look's class, that nothing is fetched, and that no colour is written out.

These run over every stylesheet in `look/` that is written by hand, each as
it comes to exist.
"""

import re
import tomllib

import pytest

from stylesheets import LOOK, rules, stylesheets, without_comments

CLASS = tomllib.loads((LOOK / "theme.toml").read_text(encoding="utf-8"))["class"]

SHEETS = pytest.mark.parametrize("path", stylesheets(), ids=lambda path: path.name)

# Words that are colours when a stylesheet writes them out. `transparent`
# and `currentColor` are not colours of the look and may be written.
NAMED = (
    "black white red green blue yellow orange purple pink brown gray grey "
    "silver gold maroon crimson salmon ivory beige navy teal olive"
).split()


def without_drawings(text: str) -> str:
    """A stylesheet without its comments and without what stands inside a
    `data:` address, which is a drawing and keeps colours of its own."""
    return re.sub(r'url\("data:[^"]*"\)', 'url("data:")', without_comments(text))


def test_a_stylesheet_is_read_nested():
    # The reading itself, on a stylesheet made for it.
    text = """
    /* a comment with a { brace */
    .look {
      color: red;
      & p { margin: 0; }
      &::before { content: "a } brace; in a string"; }
      @media (prefers-reduced-motion: reduce) { & p { animation: none; } }
    }
    @keyframes cruor-turn { from { opacity: 0; } to { opacity: 1; } }
    """
    found = [(rule.path, rule.declarations) for rule in rules(text)]
    assert found[0] == ((".look",), [("color", "red")])
    assert found[1] == ((".look", "& p"), [("margin", "0")])
    assert found[2][0] == (".look", "&::before")
    assert found[2][1] == [("content", '"a } brace; in a string"')]
    assert found[3][0] == (".look", "@media (prefers-reduced-motion: reduce)")
    assert found[4][0][-1] == "& p"
    assert [path for path, _ in found[5:]] == [
        ("@keyframes cruor-turn",),
        ("@keyframes cruor-turn", "from"),
        ("@keyframes cruor-turn", "to"),
    ]


def test_the_look_has_a_stylesheet():
    assert (LOOK / "cruentous-atonement.css") in stylesheets()


@SHEETS
def test_every_rule_sits_beneath_the_class(path):
    # A rule is beneath the class when the outermost thing it stands in is
    # the class itself. A rule inside `@media` or `@supports` is read by its
    # own selector, so such a block at the top must hold the class first.
    for rule in rules(path.read_text(encoding="utf-8")):
        own = [
            part for part in rule.path if not part.startswith(("@media", "@supports"))
        ]
        if own and own[0].startswith("@keyframes"):
            continue
        assert own, f"{path.name}: {' '.join(rule.path)} holds no rule"
        assert own[0] == f".{CLASS}", f"{path.name}: {' '.join(rule.path)}"


@SHEETS
def test_keyframes_are_named_for_cruor(path):
    text = without_comments(path.read_text(encoding="utf-8"))
    named = re.findall(r"@keyframes\s+([^\s{]+)", text)
    for name in named:
        assert name.startswith("cruor-"), f"{path.name}: {name}"
    # And every animation a rule asks for is one of them.
    for rule in rules(text):
        for prop, value in rule.declarations:
            asked = value.replace("!important", "").strip()
            if prop in ("animation", "animation-name") and asked != "none":
                assert any(name in asked.split() for name in named), value


@SHEETS
def test_stylesheets_fetch_nothing(path):
    text = without_comments(path.read_text(encoding="utf-8"))
    assert "@import" not in text
    for address in re.findall(r"url\(\s*([^)]*)\)", text):
        assert address.startswith('"data:'), f"{path.name}: {address[:60]}"
    # A `data:` address is always quoted, so a brace inside one is not read
    # as the end of a rule.
    assert not re.search(r"url\(\s*data:", text)


@SHEETS
def test_stylesheets_name_colours_by_token(path):
    text = without_drawings(path.read_text(encoding="utf-8"))
    assert not re.findall(r"#[0-9a-fA-F]{3,8}\b", text), path.name
    assert not re.findall(r"\b(?:rgba?|hsla?|hwb|lab|lch|oklab|oklch)\(", text)
    for rule in rules(text):
        for prop, value in rule.declarations:
            words = re.findall(r"[a-z]+", re.sub(r"var\([^)]*\)", "", value))
            written = [word for word in words if word in NAMED]
            assert not written, f"{path.name}: {prop}: {value}"
