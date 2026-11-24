"""The one list of the furniture's parts.

Every test that runs over the furniture reads this list: which class a part
is, which page of `tests/pages/` holds it, which of its text is measured and
at which bound, whether the blood fills it, what of it takes the keyboard,
and the states it has. A part is tested when it is in the list. The list is
whole when every part of the sprint's plan is in it.

A state at rest is found on the part's page as it lies. A state a hand
brings about is brought about by the tests: the pointer moved over the
part, the part pressed and held, Tab pressed until the keyboard is on it, or
the button that raises it pressed.

The bounds are the look's: 4.5 for interface text; 3.3 for an inscription,
which is running text of 24 pixels or more; and 3 for a part that cannot be
used.
"""

import dataclasses

INTERFACE = 4.5
INSCRIPTION = 3.3
UNABLE = 3.0

AT_REST = None
POINTER_OVER = "pointer over"
PRESSED = "pressed"
KEYBOARD = "keyboard on it"
RAISED = "raised from its button"


@dataclasses.dataclass(frozen=True)
class State:
    """One state of a part: its name, the element that is in it, how it is
    brought about (or `AT_REST`), and the lettering measured in it, each
    with its bound. A part that is raised names the button that raises it."""

    name: str
    selector: str
    how: str | None = AT_REST
    texts: tuple[tuple[str, float], ...] = ()
    by: str = ""


@dataclasses.dataclass(frozen=True)
class Part:
    name: str
    css_class: str
    page: str
    states: tuple[State, ...]
    # What takes the keyboard: selectors, in no order.
    keyboard: tuple[str, ...] = ()
    # Elements that the blood fills.
    blood: tuple[str, ...] = ()

    @property
    def at_rest(self) -> tuple[State, ...]:
        return tuple(state for state in self.states if state.how is AT_REST)


def handled(selector: str, bound: float = INTERFACE) -> tuple[State, ...]:
    """The three states a hand brings about on a control, with its own
    lettering measured in each."""
    texts = ((selector, bound),)
    return (
        State(POINTER_OVER, selector, POINTER_OVER, texts),
        State(PRESSED, selector, PRESSED, texts),
        State(KEYBOARD, selector, KEYBOARD, texts),
    )


CONTROLS = "tests/pages/controls.html"
CONTAINERS = "tests/pages/containers.html"
PIECES = "tests/pages/pieces.html"
# A page that holds one of every part, for what is asked of them all at once.
EVERY_PART = "tests/pages/every-part.html"

PARTS: tuple[Part, ...] = (
    Part(
        "button",
        "cruor-button",
        CONTROLS,
        (
            State("as it lies", "#button", texts=(("#button", INTERFACE),)),
            State("a link", "#button-link", texts=(("#button-link", INTERFACE),)),
            State("unable", "#button-unable", texts=(("#button-unable", UNABLE),)),
            *handled("#button"),
            *handled("#button-link"),
        ),
        keyboard=("#button", "#button-link"),
    ),
    Part(
        "field",
        "cruor-field",
        CONTROLS,
        (
            State("filled", "#field", texts=(("#field", INTERFACE),)),
            # An empty field's lettering is the words it shows then.
            State("empty", "#field-empty", texts=(("#field-empty", INTERFACE),)),
            State("faulty", "#field-faulty", texts=(("#field-faulty", INTERFACE),)),
            State("unable", "#field-unable", texts=(("#field-unable", UNABLE),)),
            State("many lines", "#lines", texts=(("#lines", INTERFACE),)),
            State(POINTER_OVER, "#field", POINTER_OVER, (("#field", INTERFACE),)),
            State(KEYBOARD, "#field", KEYBOARD, (("#field", INTERFACE),)),
            State(KEYBOARD, "#field-empty", KEYBOARD, (("#field-empty", INTERFACE),)),
        ),
        keyboard=("#field", "#field-empty", "#field-faulty", "#lines"),
    ),
    Part(
        "label",
        "cruor-label",
        CONTROLS,
        (State("as it lies", "#label", texts=(("#label", INTERFACE),)),),
    ),
    Part(
        "hint",
        "cruor-hint",
        CONTROLS,
        (State("as it lies", "#hint", texts=(("#hint", INTERFACE),)),),
    ),
    Part(
        "fault",
        "cruor-fault",
        CONTROLS,
        (State("as it lies", "#fault", texts=(("#fault", INTERFACE),)),),
    ),
    Part(
        "choice",
        "cruor-choice",
        CONTROLS,
        (
            State("as it lies", "#choice", texts=(("#choice", INTERFACE),)),
            State("unable", "#choice-unable", texts=(("#choice-unable", UNABLE),)),
            State(POINTER_OVER, "#choice", POINTER_OVER, (("#choice", INTERFACE),)),
            State(KEYBOARD, "#choice", KEYBOARD, (("#choice", INTERFACE),)),
        ),
        keyboard=("#choice",),
    ),
    Part(
        "tick box",
        "cruor-tick",
        CONTROLS,
        (
            State("unticked", "#tick"),
            State("ticked", "#tick-ticked"),
            State("unable", "#tick-unable"),
            State(KEYBOARD, "#tick", KEYBOARD),
        ),
        keyboard=("#tick", "#tick-ticked"),
    ),
    Part(
        "radio button",
        "cruor-radio",
        CONTROLS,
        (
            State("unpicked", "#radio"),
            State("picked", "#radio-picked"),
            State("unable", "#radio-unable"),
            State(KEYBOARD, "#radio-picked", KEYBOARD),
        ),
        # Of a set of radio buttons the keyboard goes to the one picked.
        keyboard=("#radio-picked",),
    ),
    Part(
        "slider",
        "cruor-slider",
        CONTROLS,
        (
            State("as it lies", "#slider"),
            State("unable", "#slider-unable"),
            State(KEYBOARD, "#slider", KEYBOARD),
        ),
        keyboard=("#slider",),
        blood=("#slider",),
    ),
    Part(
        "progress",
        "cruor-progress",
        CONTROLS,
        (
            State("with a value", "#progress"),
            State("without one", "#progress-unmeasured"),
        ),
        blood=("#progress",),
    ),
    Part(
        "measure",
        "cruor-measure",
        CONTROLS,
        (
            State("high", "#measure-high"),
            State("middling", "#measure-middling"),
            State("low", "#measure-low"),
        ),
        blood=("#measure-high", "#measure-middling"),
    ),
    Part(
        "plate",
        "cruor-plate",
        CONTAINERS,
        (
            State(
                "as it lies",
                "#plate",
                texts=(("#plate-text", INSCRIPTION), ("#plate-small", INTERFACE)),
            ),
            State("a link", "#plate-link", texts=(("#plate-link-title", INTERFACE),)),
            State(
                POINTER_OVER,
                "#plate-link",
                POINTER_OVER,
                (("#plate-link-title", INTERFACE),),
            ),
            State(
                KEYBOARD, "#plate-link", KEYBOARD, (("#plate-link-title", INTERFACE),)
            ),
        ),
        keyboard=("#plate-link",),
    ),
    Part(
        "panel",
        "cruor-panel",
        CONTAINERS,
        (
            State(
                "as it lies",
                "#panel",
                texts=(("#panel-text", INSCRIPTION), ("#panel-small", INTERFACE)),
            ),
        ),
    ),
    Part(
        "the void",
        "cruor-void",
        CONTAINERS,
        (
            State(
                "as it lies",
                "#void",
                texts=(
                    ("#void-heading", INTERFACE),
                    ("#void-text", INTERFACE),
                    ("#void-item", INTERFACE),
                    ("#void-subdued", INTERFACE),
                ),
            ),
            State("with a current row", "#void", texts=(("#void-row", INTERFACE),)),
        ),
        keyboard=("#void-item", "#void-row"),
    ),
    Part(
        "notice",
        "cruor-notice",
        CONTAINERS,
        (
            State(
                "a note", "#notice-note", texts=(("#notice-note-text", INSCRIPTION),)
            ),
            State(
                "a warning",
                "#notice-warning",
                texts=(("#notice-warning-text", INSCRIPTION),),
            ),
            State(
                "a fault", "#notice-fault", texts=(("#notice-fault-text", INSCRIPTION),)
            ),
        ),
    ),
    Part(
        "fold",
        "cruor-fold",
        CONTAINERS,
        (
            State("shut", "#fold", texts=(("#fold-summary", INTERFACE),)),
            State(
                "open",
                "#fold-open",
                texts=(
                    ("#fold-open-summary", INTERFACE),
                    ("#fold-open-text", INSCRIPTION),
                ),
            ),
            State(KEYBOARD, "#fold-summary", KEYBOARD, (("#fold-summary", INTERFACE),)),
        ),
        keyboard=("#fold-summary", "#fold-open-summary"),
    ),
    Part(
        "rise",
        "cruor-rise",
        CONTAINERS,
        (
            State(
                "a dialog, open",
                "#rise-open",
                texts=(
                    ("#rise-open-text", INSCRIPTION),
                    ("#rise-open-small", INTERFACE),
                ),
            ),
            State(
                "shown from its button",
                "#rise",
                RAISED,
                (("#rise-text", INSCRIPTION), ("#rise-small", INTERFACE)),
                by="#raise",
            ),
            State(
                "shown as a modal dialog from its button",
                "#dialog",
                RAISED,
                (("#dialog-text", INSCRIPTION),),
                by="#raise-dialog",
            ),
        ),
        # What takes the keyboard is the button that raises it, and what is
        # inside it.
        keyboard=("#raise", "#raise-dialog", "#rise-open-close"),
    ),
    Part(
        "masthead",
        "cruor-masthead",
        PIECES,
        # Its title is carved, and held by the theme file's entries for the
        # page and the stone. It has no ground of its own.
        (State("as it lies", "#masthead", texts=(("#masthead-small", INTERFACE),)),),
    ),
    Part(
        "bar of links",
        "cruor-links",
        PIECES,
        (
            State(
                "with a current link",
                "#links",
                texts=(("#links-item", INTERFACE), ("#links-current", INTERFACE)),
            ),
            State(
                POINTER_OVER, "#links-item", POINTER_OVER, (("#links-item", INTERFACE),)
            ),
            State(KEYBOARD, "#links-item", KEYBOARD, (("#links-item", INTERFACE),)),
        ),
        keyboard=("#links-item", "#links-current", "#links-other"),
    ),
    Part(
        "trail",
        "cruor-trail",
        PIECES,
        (
            State(
                "with a current place",
                "#trail",
                texts=(("#trail-link", INTERFACE), ("#trail-current", INTERFACE)),
            ),
            State(KEYBOARD, "#trail-link", KEYBOARD, (("#trail-link", INTERFACE),)),
        ),
        keyboard=("#trail-link", "#trail-second"),
    ),
    Part(
        "badge",
        "cruor-badge",
        PIECES,
        (
            State("as it lies", "#badge", texts=(("#badge", INTERFACE),)),
            State("a fault", "#badge-fault", texts=(("#badge-fault", INTERFACE),)),
        ),
    ),
    Part("seal", "cruor-seal", PIECES, (State("as it lies", "#seal"),)),
    Part("sigil", "cruor-sigil", PIECES, (State("as it lies", "#sigil"),)),
    Part("hairline", "cruor-hairline", PIECES, (State("as it lies", "#hairline"),)),
    Part("loader", "cruor-loader", PIECES, (State("as it lies", "#loader"),)),
)


def pages() -> list[str]:
    """Every page that holds a part, once each, in the list's order."""
    return list(dict.fromkeys(part.page for part in PARTS))


def classes() -> list[str]:
    return [part.css_class for part in PARTS]
