# INT-0006 — The furniture

<!-- sprint-loop-intent-v2 -->
- **Intent ID:** INT-0006
- **State:** active
- **Work evidence:** [T-206 to T-211 and T-214, Sprint 1 build plan](../sprints/s1/sprint-plans/build-plan.md)
- **Completion evidence:** none
- **Code evidence:** none
- **Test evidence:** none
- **Documentation evidence:** none

## Intent

The framework holds furniture: the parts a page is built from, each dressed
in Cruentous Atonement
([INT-0003](INT-0003-cruentous-atonement-look.md)). A person who takes the
kit can set down a button, a field, a card or a bar of navigation and have
it belong to the look, as they can already set a line of text in Cruor.

This comes from a web designer who read the framework's front page on
23 November 2026 and whose words the owner passed on. They liked the
letters and the colours, and said of the rest that for a kit it had walls
and a carpet and no furniture. The owner had put it to them as hors
d'oeuvre served where an entree was needed, and they agreed. On 24 November 2026 the owner chose to build the furniture next
("Start that sprint").

What furniture means here:

- **Controls.** Buttons and links that act as buttons; fields for a line and
  for many lines; a choice from a list; a box to tick and one of several to
  pick; a slider; a measure of progress.
- **Containers.** A plate that holds one thing among others; a panel; a
  notice set apart from the text; a part that opens and closes; a part that
  comes up over the page and goes away again.
- **Ways through a page.** A masthead with the briar at its foot; a bar of
  links; a trail back to where one came from.
- **Small pieces.** A badge; the seal; the sigil between its rules; the
  hairline; a sign that something is being waited for.

Plain HTML that needs no class (headings, paragraphs, lists, quotations,
rules, code, tables) is the look's own business and stays in
[INT-0003](INT-0003-cruentous-atonement-look.md).

Boundaries:

- No script in the kit. Every part works by HTML and stylesheets alone,
  using what a browser already gives: a part that opens and closes, a part
  that comes up over the page, and the states of a form's controls. The
  owner ruled scripted components out of the first version on
  23 November 2026, and that stands. The one script the repository holds
  outside the showroom is the worked example of a build fetching a release
  (`examples/`, [INT-0005](INT-0005-versioned-releases.md)), which a build
  runs and a page does not.
- A part asks for one class on one element where it can, and its name
  begins `cruor-`.
- A part is a part of this look. It is not a general set of components
  with a skin.

## Acceptance criteria

Settled in Sprint 1's Plan, 24 November 2026. The owner chose the first
set of parts that day ("The first set"): button, fields, tick box, radio
button, slider, progress and measure; plate, panel, the void, notice, fold
and rise; masthead, bar of links and trail; badge, seal, sigil, hairline
and loader. Tabs, a tooltip, a tree, a dressed table beyond plain HTML's
and layouts with a sidebar are left for later.


1. Each part named above is a rule in the framework's stylesheets and can be
   used from plain HTML with no script and no build step.
2. Each part is shown in use in the showroom
   ([INT-0007](INT-0007-the-showroom.md)), in every state it has at rest:
   as it lies, unable to be used, ticked or picked, filled, faulty, open,
   and each of its kinds. The states a hand brings about (the pointer over
   it, pressed, the keyboard on it) are not imitated there, since that
   would take rules the kit does not hold; a visitor brings them about by
   trying the part, and the tests bring them about in a browser.
3. Every rule is scoped beneath the look's class.
4. A part's text meets the contrast bounds of
   [INT-0003](INT-0003-cruentous-atonement-look.md) on every ground it
   renders on, in every state. A part that cannot be used is held to 3:1
   and not 4.5:1: it is dimmed so as to be seen to be out of use, and the
   standard the bounds come from asks nothing of such a part, so 3:1 is
   more than it requires. A heading set in a container that has a ground of
   its own is lettered flat and not carved, so that it can be measured.
5. Every part can be reached and worked with the keyboard, and shows where
   the keyboard is.
6. All motion stops under `prefers-reduced-motion: reduce`. In print a part
   is black on white with no ornament.
7. The README names the parts and shows how one is used.

## Rationale

A kit is something to build with. Fonts and colours let a person set type;
they do not let a person lay out a page that works. Until the framework
holds parts, every page that takes it must make its own, and each will make
them differently.

## Alternatives

- **Keep to plain HTML and add no parts.** This was the first version the
  owner chose on 23 November 2026. The designer's reading shows what it
  leaves a person without.
- **Scripted components.** Ruled out by the owner for the first version. A
  browser now gives enough without script for every part named here.
- **More ornament for the front page instead** (stone at its sides, candles,
  the statue's blood running on down the page). Sketched on
  24 November 2026 before the designer's second message arrived. It adds to
  the walls and the carpet, which were not what was missing.

## Consequences

- The framework's next version holds stylesheets as well as fonts, so a
  release carries more files ([INT-0005](INT-0005-versioned-releases.md)).
- Three of the parts rest on things browsers gained lately: a part that
  comes up over the page (`popover`), folds that share a `name`, and a
  dialog opened by a button alone (`commandfor` with
  `command="show-modal"`), which is the newest. In an engine without the
  last, the button does nothing and the dialog stays shut; so a page should
  put nothing in such a dialog that a visitor must have. The tests run in
  one engine; what the others do is carried by backlog task T-105.
- Tome has parts of its own in this look (its library's plates, its
  masthead, its sidebar). When Tome takes the framework in, it may take the
  framework's parts for them; that is Tome's to plan.

## Transition history
- 2026-11-24: created as `proposed` in Sprint 1's Research, from a
  designer's reading of the front page and the owner's choice that day.
- 2026-11-24: `proposed` to `planned`. The owner chose the first set of
  parts and approved Sprint 1's plan, which builds them in three groups
  (T-206, T-207, T-208) and shows them in the showroom (T-209).
- 2026-11-24: revised after the plan's first review, still `planned`.
  Criterion 2 tells states that hold at rest from states a hand brings
  about; the boundary records the standing of `examples/`.
- 2026-11-24: revised after the plan's second review, still `planned`. The
  Consequences record which parts rest on newer things in a browser, and
  what a visitor without them meets.
- 2026-11-24: revised after the plan's third review, still `planned`.
  Criterion 4 states the bound for a part that cannot be used, and that a
  heading in a container is not carved.
- 2026-11-24: `planned` to `active`. Sprint 1's Build reached T-211, the means by which the parts' contrast is measured in a browser.
