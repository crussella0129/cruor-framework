# INT-0003 — The Cruentous Atonement look

<!-- sprint-loop-intent-v2 -->
- **Intent ID:** INT-0003
- **State:** active
- **Work evidence:** [T-203 to T-207, T-209 and T-211, Sprint 1 build plan](../sprints/s1/sprint-plans/build-plan.md)
- **Completion evidence:** none
- **Code evidence:** none
- **Test evidence:** none
- **Documentation evidence:** none

## Intent

The look is called **Cruentous Atonement**. *Cruentus* is the adjective of
*cruor*, blood that has been shed, so the look and the typeface share one
root. The owner raised the name on 23 November 2026 ("which might be better
called cruentous atonement perhaps") and chose it the same day over the name
the look had carried until then, Sanguine Atonement.

It is the look of blood letters cut into obsidian, made to be read on a
tablet at a dimly lit table. A viewer should feel "oh dear" before reading a
word, and the effect comes from deliberate craft, not from flat red on flat
black. The look was first made as a theme of
[Tome](https://github.com/crussella0129/Tome); the framework holds it so any
page can take it on.

What the look is made of:

- **The stone.** A near-black page with a procedural obsidian surface (broad
  glassy glints and sparse streaks of iron), drawn with no image file, and a
  candle-dim glow from above with darkness at the edges.
- **The inscription.** Running text in hue-true arterial crimson, with no
  green or blue lift, set at 24 pixels or more. Small things (interface
  text, tables, code blocks, footnotes) speak in bone.
- **Carved headings.** Large letters are channels: the blood pours in from
  the top, catches the light, and settles dark at the foot. The first
  heading keeps a slow heartbeat.
- **Ornaments.** A seal for a passage's first letter; a sigil between two
  clotted rules for a divider; quotations as inscriptions fed by a channel
  of blood, with one drop at its foot; inline code as a salmon highlight;
  fine glowing hairlines; and an eight-bit briar, with blood on its thorns,
  for the edge of a masthead or a panel.
- **The void.** A panel of pure black beside the obsidian page, lettered in
  salmon, with crimson for its structure.
- **The type.** The title in Cruor Thornamental Regular, the headings
  beneath it in Cruor Lite Regular, and running text in Cruor Sans Regular,
  as the owner named on 23 November 2026 of the framework's front page
  ("the title should be thornamental, the headings should be cruor lite,
  and the text should be cruor sans"). This replaces what the owner named on
  21 November 2026 ("cruor thornamented for the titles and cruor lite for
  the body text"). Code is set in Cruor Sans Mono, as on the front page.
  Each of these is a line in the theme file
  ([INT-0004](INT-0004-the-look-as-a-theme-file.md)) and can be changed
  there.

A page takes the look on by linking the framework's stylesheets and setting
one class, `cruentous-atonement`, on `<body>`. The stylesheets are four
files: `fonts.css`, `tokens.css`, `cruentous-atonement.css`, and
`furniture.css` for the parts ([INT-0006](INT-0006-the-furniture.md)). None
imports another and none names a path, so the four work side by side
wherever they are served, a release among them. Plain HTML (headings, paragraphs, links, lists, quotations,
rules, code, tables) is dressed with no further markup; the ornaments that
plain HTML has no element for (the briar, the void, the hairline) are
classes a page opts into.

Boundaries:

- No script. The look is stylesheets.
- Every rule is written nested beneath the look's class. A rule inside
  `@media` or `@supports` is read by its own selector; `@keyframes` are
  named beginning `cruor-`, since they cannot be nested.
- The rite by which Tome reveals the look (its riddle, and the wash that
  follows the answer) is Tome's, and stays there.
- The framework's own names follow the new name: the class a page sets, and
  tokens that begin `--cruor-`.

## Acceptance criteria

Settled in Sprint 1's Plan, 24 November 2026:

1. A page of plain HTML that links the framework's stylesheets and sets the
   look's class shows the stone, the inscription, the carved headings and
   the ornaments, with no script and no build step.
2. Every rule is scoped beneath the look's class: a page that does not set
   it is untouched.
3. Running text meets at least 3.3:1 against every ground it renders on,
   the brightest sheen of the stone included, and is set at 24 pixels or
   more, where the large-text threshold of WCAG AA (3:1) applies. Interface
   text meets at least 4.5:1 on the same grounds. Large carved letters meet
   at least 3:1 on the page as it lies, and the stop at their top on the
   stone at its brightest as well; the stop at their foot, the pooled red
   the owner approved, stands at 2.80 there, and that is told and not
   hidden. Lettering in the void meets at least 4.5:1 on each ground it is
   set on there, and its crimson structure at least 3:1. The void's
   subdued lettering is not set on the tinted row of the current item,
   where it would fall short. The edge that a part filled with blood
   carries meets at least 3:1 against the ground beside it.
4. The stone is drawn with no image file, sits behind the content and never
   lowers those ratios.
5. All motion stops under `prefers-reduced-motion: reduce`. In print the
   page is black on white with no ornament.
6. Set beside Tome's theme, the framework's page is the same look, in
   Cruor. The owner judges this by eye.

## Rationale

The look is finished work that the owner approved over several rounds of
renders in Tome. Putting it in the framework makes it one thing that many
pages can share, with its colours' contrast held by test.

The name: the kit is Cruor's, and *cruentus* comes from *cruor*, so the
look's name now says whose it is.

## Alternatives

- **Keep the name Sanguine Atonement.** Offered. It would have left nothing
  to rename, but the kit would then be Cruor in its fonts and Sanguine in
  its look.
- **Flat pure red on pure black.** Rejected when the look was first made: it
  reads as an alarm, and pure black gives a surface no headroom.
- **Small crimson text.** Not possible: a hue-true blood red bright enough
  to read at small sizes is pure red in all but name. So the inscription is
  large, and small text is bone or salmon.

## Consequences

- Tome's theme may keep or change its own label when Tome takes the
  framework in; that is Tome's to record. Its riddle is answered with
  "Sanguine", which is a quoted line and stays as it is.
- Which fixed-pitch family sets code is chosen by eye, from a side by side,
  in the sprint that builds the look. Sprint 1 begins from Cruor Sans Mono
  and shows the others beside it when the owner judges the look.
- The furniture ([INT-0006](INT-0006-the-furniture.md)) is dressed by a
  stylesheet of its own, so that a page of plain HTML can take the look
  without the parts.
- The look has a colour for blood that has been shed and lies: `#3c0606`,
  which the owner chose on 23 November 2026 for the tears of the statue on
  the front page ("closer to a 3C0606 hex", and wholly opaque). It is near
  the page's own ground, so wherever it fills a part it carries an edge in
  the inscription's crimson, and it is never the colour of lettering.
- Nesting was chosen over `@scope` to keep the rules beneath the class,
  because it is read by every engine a reader of Tome is likely to have.
- Lifting the foot of a carved heading to `#c21b1b` would bring it to 3:1
  on the stone at its brightest. The owner was told on 24 November 2026.
  Their answer is asked for when the showroom first stands, where the
  heading can be seen on the stone (Sprint 1, T-209), and criterion 3 is
  amended to what they then say.

## Transition history
- 2026-11-23: created as `proposed` in Sprint 0's Research, from the owner's
  choice of name that day and the look as it stands in Tome.
- 2026-11-24: `proposed` to `planned`. The owner approved Sprint 1's plan,
  which builds the look as stylesheets beneath one class (T-204, T-205) and
  holds its contrast by test (T-203). Revised in the same Plan: the type
  follows the owner's words of 23 November 2026; the class a page sets is
  named; the acceptance criteria are settled as they were outlined.
- 2026-11-24: revised after the plan's first review, still `planned`. The
  four stylesheets and the rule that none imports another are named;
  nesting is recorded as how rules are kept beneath the class; the blood is
  named as a colour of the look; criterion 3 says on which ground each
  bound is held, and tells the one place a carved heading falls short.
- 2026-11-24: `planned` to `active`. Sprint 1's Build reached T-203, the test of the contrast the look promises.
