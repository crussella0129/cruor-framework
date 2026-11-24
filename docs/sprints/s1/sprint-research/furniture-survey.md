# What furniture a kit of this kind holds

Made on 24 November 2026 for
[INT-0006](../../../intents/INT-0006-the-furniture.md) and
[INT-0007](../../../intents/INT-0007-the-showroom.md). Three things were
read: the look as it stands in Tome, where it has parts of its own; the kit
the owner named as the model in Sprint 0, which is a set of parts; and what
a browser gives without script.

## What the look already dresses in Tome

From Tome's stylesheet for the look and the inventory made in Sprint 0
(`docs/sprints/s0/sprint-research/look-inventory.md`):

| part | in Tome | carried by |
|---|---|---|
| the stone, the candle, the vignette | the page's ground | INT-0003 |
| the inscription, carved headings, the seal | chapter text | INT-0003 |
| links, lists with a diamond for a mark | chapter text | INT-0003 |
| quotations and callouts fed by a channel of blood | chapter text | INT-0003; the callout is furniture |
| inline code as a salmon chip; code blocks in bone | chapter text | INT-0003 |
| the sigil between clotted rules; hairlines | dividers | INT-0003 and INT-0006 |
| the briar | the masthead's foot, a panel's edge | INT-0006, with the masthead |
| a plate (a tile that links to a book, with a hard shadow) | the library | INT-0006 |
| the void (a black panel lettered in salmon) | the sidebar | INT-0006 |
| fields (caret in arterial red, sunken ground) | the riddle's dialog | INT-0006 |
| selection in bright bone on a clotted ground | everywhere | INT-0003 |

Tome has no button, tick box, slider, measure of progress, badge or bar of
links in this look. Those are new.

## What the model kit holds

The kit the owner named as the model in Sprint 0's research holds, as
parts: an accordion, action bars and buttons, an alert banner, an avatar,
badges, loaders and bars of progress, breadcrumbs, buttons and groups of
them, cards, a checkbox, a code block, a combo box, tables, a date picker,
a dialog, a divider, a drawer, a dropdown menu, a grid, inputs, list items,
navigation, a range slider, a popover, radio buttons, a select, a sidebar
layout, a text area, a tooltip, a tree view and a window. It also holds
playthings: a snake game, a platformer and a chessboard.

Its parts are scripted components. The framework's are not to be. But the
list says what a person expects to find in a kit, and that a kit of this
kind is allowed to play.

## What a browser gives without script

| wanted | given by |
|---|---|
| a part that opens and closes | `<details>` and `<summary>`; several sharing a `name` open one at a time |
| a part that comes up over the page | the `popover` attribute, opened by a button's `popovertarget` |
| a dialog | `<dialog>` shown as a popover; a true modal one needs script |
| a tooltip | a popover, or a rule on `:hover` and `:focus-visible` |
| a choice from a list | `<select>`; its open list is the system's own and cannot be dressed everywhere |
| tick boxes and radio buttons | `<input>` with `appearance: none`, drawn by rules on `:checked` |
| a slider | `<input type="range">`, its track and thumb dressed by the engines' own pseudo-elements |
| a measure of progress | `<progress>` and `<meter>`, dressed the same way |
| tabs | radio buttons and `:has()`, or `<details>` sharing a `name` |
| a state that depends on what is inside | `:has()` |
| rules kept beneath one class | nesting, or `@scope` |
| motion | animations and transitions, stopped under `prefers-reduced-motion` |

What cannot be had without script: a true modal dialog, a combo box that
filters as it is typed in, a date picker beyond the system's own, a tree
that remembers what was open, and playthings such as a game.

## A first set

Sorted by what a page most often needs and by what the look already has an
answer for:

1. **Button** (and a link that is one): at rest, hovered, pressed, with the
   keyboard on it, and unable to be pressed.
2. **Fields**: one line, many lines, a choice from a list; with a label, a
   hint and a fault.
3. **Tick box, radio button, slider.**
4. **Progress and measure.**
5. **Plate**: a card, and a card that is a link.
6. **Panel and the void.**
7. **Notice**: a callout fed by a channel of blood, in a few kinds.
8. **Fold**: `<details>`, one or several.
9. **Rise**: a popover, and a dialog shown as one.
10. **Masthead** with the briar; **bar of links**; **trail**.
11. **Badge, seal, sigil, hairline, loader.**

Left for later: tabs, tooltip, tree, a dressed table beyond plain HTML's,
layouts with a sidebar, and anything that needs script.

## Play without script

The designer asked for play. Within the kit's rule of no script, play is in
how a part answers a hand:

- a button whose channel fills with blood as it is pressed;
- a tick box that is struck like a seal;
- a slider and a bar of progress that are a vial filling;
- a fold whose mark turns and whose rule bleeds open;
- a loader that is a drop gathering and falling;
- the briar growing along a masthead as the page opens.

Play beyond that (a thing to toy with, matter that behaves) needs script,
and belongs to the showroom if the owner wants it there.
