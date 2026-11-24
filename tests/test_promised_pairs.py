"""That no rule sets lettering on a ground the theme file has not promised.

The theme file says which text may sit on which ground. A rule of the
look's stylesheets that sets both a colour for its lettering and a ground,
each by a token, makes such a pair, and the pair must be one the theme
file's `[[contrast]]` entries cover.

This sees only a rule that sets both itself. A pair that arises from a
ground set by one rule and lettering set or inherited from another is held
by the tests that measure what a browser draws.
"""

import re
import tomllib

import pytest

from stylesheets import LOOK, rules, stylesheets

THEME = tomllib.loads((LOOK / "theme.toml").read_text(encoding="utf-8"))

TOKEN = re.compile(r"var\(--cruor-([a-z0-9-]+)\)")


def role(token: str) -> str:
    """A token's name as a `[[contrast]]` entry writes it."""
    if token.startswith("void-"):
        return "void." + token.removeprefix("void-")
    return token


def promised() -> set[tuple[str, str]]:
    return {
        (text, ground)
        for entry in THEME["contrast"]
        for text in entry["text"]
        for ground in entry["grounds"]
    }


def pairs(text: str) -> list[tuple[str, str, str]]:
    """Every (selector, text role, ground) that one rule sets by tokens."""
    found = []
    for rule in rules(text):
        colour = TOKEN.fullmatch(rule.value("color") or "")
        ground = rule.value("background-color") or rule.value("background") or ""
        ground = TOKEN.fullmatch(ground)
        if colour and ground:
            found.append(
                (" ".join(rule.path), role(colour.group(1)), role(ground.group(1)))
            )
    return found


def test_pairs_are_read_from_a_rule():
    # The reading itself, on a stylesheet made for it.
    text = """
    .look {
      .a { color: var(--cruor-text); background: var(--cruor-panel); }
      .b { color: var(--cruor-void-text); background-color: var(--cruor-void-row); }
      .c { color: var(--cruor-text); }
      .d { background: var(--cruor-blood); }
    }
    """
    assert pairs(text) == [
        (".look .a", "text", "panel"),
        (".look .b", "void.text", "void.row"),
    ]
    assert ("text", "panel") in promised()
    assert ("void.text", "void.row") in promised()
    # Lettering on the blood is promised nowhere, so a rule that set it
    # would be caught here.
    assert not [pair for pair in promised() if pair[1] == "blood"]


@pytest.mark.parametrize("path", stylesheets(), ids=lambda path: path.name)
def test_every_text_on_ground_pair_is_promised(path):
    kept = promised()
    for selector, text, ground in pairs(path.read_text(encoding="utf-8")):
        assert (text, ground) in kept, f"{path.name}: {selector}: {text} on {ground}"
