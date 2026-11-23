# INT-0004 — The look as a theme file

<!-- sprint-loop-intent-v2 -->
- **Intent ID:** INT-0004
- **State:** proposed
- **Work evidence:** none
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

- the fonts: titles, running text and code; and for each heading level its
  font, whether it is bold, italic or underlined, and its size;
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

To be settled when a sprint plans it. The outline:

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
5. The theme file is in each release
   ([INT-0005](INT-0005-versioned-releases.md)).

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
