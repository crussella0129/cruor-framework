# INT-0003 — The Cruentous Atonement look

<!-- sprint-loop-intent-v2 -->
- **Intent ID:** INT-0003
- **State:** proposed
- **Work evidence:** none
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
- **The type.** Titles in Cruor Thornamental Regular and running text in
  Cruor Lite Regular, as the owner named on 21 November 2026 ("cruor
  thornamented for the titles and cruor lite for the body text"). Code is
  set in one of Cruor's fixed-pitch families.

A page takes the look on by linking the framework's stylesheets and setting
one class. Plain HTML (headings, paragraphs, links, lists, quotations,
rules, code, tables) is dressed with no further markup; the ornaments that
plain HTML has no element for (the briar, the void, the hairline) are
classes a page opts into.

Boundaries:

- No script. The look is stylesheets.
- The rite by which Tome reveals the look (its riddle, and the wash that
  follows the answer) is Tome's, and stays there.
- The framework's own names follow the new name: the class a page sets, and
  tokens that begin `--cruor-`.

## Acceptance criteria

To be settled when a sprint plans it. The outline:

1. A page of plain HTML that links the framework's stylesheets and sets the
   look's class shows the stone, the inscription, the carved headings and
   the ornaments, with no script and no build step.
2. Every rule is scoped beneath the look's class: a page that does not set
   it is untouched.
3. Running text meets at least 3.3:1 against every ground it renders on,
   the brightest sheen of the stone included, and is set at 24 pixels or
   more, where the large-text threshold of WCAG AA (3:1) applies. Interface
   text meets at least 4.5:1 on the same grounds. Large carved letters meet
   at least 3:1. Lettering in the void meets at least 4.5:1 on each ground
   it meets there, and its crimson structure at least 3:1.
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
  in the sprint that builds the look.

## Transition history
- 2026-11-23: created as `proposed` in Sprint 0's Research, from the owner's
  choice of name that day and the look as it stands in Tome.
