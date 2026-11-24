# INT-0004 — The look as a theme file

<!-- sprint-loop-intent-v2 -->
- **Intent ID:** INT-0004
- **State:** planned
- **Work evidence:** [T-201 to T-205, T-212 and T-218, Sprint 1 build plan](../sprints/s1/sprint-plans/build-plan.md)
- **Completion evidence:** none
- **Code evidence:** none
- **Test evidence:** none
- **Documentation evidence:** none

## Intent

Cruentous Atonement ([INT-0003](INT-0003-cruentous-atonement-look.md)) is
written down once, as a TOML theme file, and the framework's tokens are
made from that file. The owner chose this on 23 November 2026 as part of
what the first version holds ("Fonts, look and a theme file").

The owner's wish for themes, said of Tome on 21 November 2026: "Designing
'themes' in tome should be easy though, like configuring a TOML config (or a
dotfile in hyprland)." And on 23 November: "that could allow you to set what
Font + bold/italic/underline condition + size for each heading level too
maybe".

The theme file names, by role:

- the fonts, in four roles: the title, the headings, running text and
  code; and for each heading level its font, whether it is bold, italic or
  underlined, and its size. A heading's font is one of the four roles or,
  by name, any family the kit holds, so that each level can be set as the
  owner said. A family the kit does not hold is refused;
- the colours: the page and its panels, interface text, the inscription,
  links, the stops of a carved heading, the void and its lettering;
- the look's other measures that a page might want to change: the size of
  the inscription, and the large first letter and its font.

Boundaries:

- The file describes a look by role. The ornaments' drawings (the briar,
  the sigil, the stone's surface) stay in the stylesheet.
- The form of the file is the framework's. Tome means to read themes as
  TOML files too; whether it reads this form unchanged is settled with Tome
  when Tome plans that work.

## Acceptance criteria

Settled in Sprint 1's Plan, 24 November 2026:

1. One TOML file in the repository states Cruentous Atonement's fonts,
   colours and measures by role, and the form is written up so a person can
   write another.
2. The framework's token stylesheet is made from the theme file by one
   command, and a check fails if the two disagree.
3. The contrast bounds of [INT-0003](INT-0003-cruentous-atonement-look.md)
   are tested from the theme file's colours, each text role against every
   ground it renders on.
4. Changing a heading level's font, weight, slant, underline or size in the
   theme file changes that heading on the page once the tokens are made
   again.
5. The theme file is in each release from the one that first holds the
   look ([INT-0005](INT-0005-versioned-releases.md)).
6. Everything in the repository that shows the look takes its colours from
   the theme file: the stylesheets name colours by the tokens made from it,
   and the script that draws the front page reads the file, for its colours
   and for the four families it sets. A drawing's own colours are the only
   ones written out: the briar's squares, the statue's two pictures, and
   the drawings a stylesheet holds in a `data:` address (the stone's
   surface, the sigil, the briar), which cannot read a token.

## Rationale

The look's colours carry a contract: which text may sit on which ground,
and at what size. Written as data, that contract can be tested, the tokens
cannot drift from it, and another program can read the same file.

## Alternatives

- **Tokens written by hand in CSS, with no theme file.** Offered as the
  smaller first version. The owner chose the theme file.
- **Wait for Tome to design the form.** The framework needs the role
  contract now, to test contrast; the form is written here and can be
  revised with Tome.

## Consequences

- A tool in the repository reads the theme file and writes the tokens.
- If Tome's needs change the form, the framework revises this intent and
  the file together.

## Transition history
- 2026-11-23: created as `proposed` in Sprint 0's Research, from the owner's
  answer that day.
- 2026-11-23: revised after Sprint 0's plan review, still `proposed`.
  Criterion 5 now allows for the first release, which holds the fonts alone.
- 2026-11-24: `proposed` to `planned`. The owner chose that day to build the
  whole theme file in Sprint 1 ("The whole theme file"), and approved the
  plan: the file and its form (T-201), the tokens made from it (T-202), its
  contrast tested (T-203), headings driven by it (T-205), and the file in
  each release (T-212). The acceptance criteria are settled as they were
  outlined.
- 2026-11-24: revised after the plan's first review, still `planned`. The
  Intent names the four font roles and says what a heading's font may be.
- 2026-11-24: revised after the plan's second review, still `planned`.
  Criterion 6 is new: it states a promise the plans had made on their own,
  that what shows the look takes its colours and families from this file.
  The task that brings the front page's script under it is T-218.
