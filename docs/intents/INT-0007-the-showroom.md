# INT-0007 — The showroom

<!-- sprint-loop-intent-v2 -->
- **Intent ID:** INT-0007
- **State:** proposed
- **Work evidence:** none
- **Completion evidence:** none
- **Code evidence:** none
- **Test evidence:** none
- **Documentation evidence:** none

## Intent

The framework has a showroom: a page built from the kit and from nothing
else, where a visitor sees Cruentous Atonement
([INT-0003](INT-0003-cruentous-atonement-look.md)) and every piece of
furniture ([INT-0006](INT-0006-the-furniture.md)) in use, and can try them.

The designer whose reading began this (see INT-0006) asked for "some more
play", "some more world, some more place". The front page is a picture: it
can be looked at and nothing in it can be touched. The showroom is the
answer to that. It is a place a visitor is in, laid out as a real page
would be, where a button can be pressed, a field written in and a part
opened; it is not a catalogue with one of each thing in a row.

It also proves the kit. If the showroom can be built from the framework's
stylesheets and plain HTML alone, so can another person's page.

What it holds:

- the look on a whole page: the stone, the inscription, carved headings and
  the ornaments;
- every part of the furniture, in every state, used where such a part
  would be used;
- how each is written, close by, so that a visitor can take it.

Boundaries:

- It links the framework's stylesheets as any page would, and adds none of
  its own beyond what lays out the showroom itself.
- Whether it may hold script for the sake of play, which the kit itself may
  not, is the owner's to settle when a sprint plans it.
- Where it is served from is the owner's to settle too: it can always be
  opened from a copy of the repository.

## Acceptance criteria

To be settled when a sprint plans it. The outline:

1. One page in the repository shows the look and every part of the
   furniture in use, and opens from a copy of the repository with no build
   step.
2. It links only the framework's own stylesheets and fonts, and fetches
   nothing from anywhere else.
3. Beside each part is the HTML that makes it.
4. A check opens it in a browser and finds every font loaded, no failed
   request, and every part present.
5. The front page points to it and shows a picture of it.
6. The owner judges by eye that it is a place and not a list.

## Rationale

A look is judged by being in it. A person deciding whether to take the kit
wants to see a page made with it and to try its parts, before reading how.

## Alternatives

- **Show the parts on the front page alone.** The front page is a picture
  and cannot be tried.
- **A catalogue: each part once, in a grid.** It shows what exists and not
  what a page made of it is like, which is what was asked for.

## Consequences

- If it is served on the web, the repository needs that turned on by the
  owner, and each version's showroom should be the one a visitor sees.
- The front page's picture is drawn from words
  (`assets/readme/text.md`); a picture of the showroom in it is a new kind
  of thing for `tools/draw_readme.py` to place.

## Transition history
- 2026-11-24: created as `proposed` in Sprint 1's Research, from a
  designer's reading of the front page and the owner's choice that day.
