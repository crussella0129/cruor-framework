"""Reading the look's stylesheets as text: their rules and what each declares.

The stylesheets are written nested, a rule inside a rule, so a rule is read
with the selectors it stands beneath. Nothing here knows the look; the tests
that do are in test_look_css.py and test_promised_pairs.py.
"""

import dataclasses
import re

from helpers import ROOT

LOOK = ROOT / "look"
TOKENS = "tokens.css"


def stylesheets() -> list:
    """The look's stylesheets that are written by hand: every one in
    `look/` but the tokens, which the tool makes."""
    return sorted(path for path in LOOK.glob("*.css") if path.name != TOKENS)


def without_comments(text: str) -> str:
    return re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)


@dataclasses.dataclass
class Rule:
    """One block of a stylesheet: what stands before each brace that holds
    it, outermost first, and the declarations it holds itself."""

    path: tuple[str, ...]
    declarations: list[tuple[str, str]]

    @property
    def selector(self) -> str:
        return self.path[-1]

    def value(self, property_name: str) -> str | None:
        found = [value for name, value in self.declarations if name == property_name]
        return found[-1] if found else None


def rules(text: str) -> list[Rule]:
    """Every block of a stylesheet, nested ones among them. A brace or a
    semicolon inside a quoted string or a pair of brackets is not a mark."""
    text = without_comments(text)
    found: list[Rule] = []
    stack: list[Rule] = []
    buffer = ""
    quote = ""
    depth = 0
    for character in text:
        if quote:
            buffer += character
            if character == quote:
                quote = ""
            continue
        if character in "\"'":
            quote = character
            buffer += character
        elif character == "(":
            depth += 1
            buffer += character
        elif character == ")":
            depth -= 1
            buffer += character
        elif depth:
            buffer += character
        elif character == "{":
            before = tuple(rule.selector for rule in stack)
            rule = Rule((*before, " ".join(buffer.split())), [])
            found.append(rule)
            stack.append(rule)
            buffer = ""
        elif character in ";}":
            declaration = buffer.strip()
            buffer = ""
            if declaration:
                name, _, value = declaration.partition(":")
                stack[-1].declarations.append((name.strip(), " ".join(value.split())))
            if character == "}":
                stack.pop()
        else:
            buffer += character
    assert not stack and not buffer.strip(), "the stylesheet's braces are matched"
    return found
