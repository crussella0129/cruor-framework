# Sprint 1 Build Plan

## Intents
- [INT-0003](../../../intents/INT-0003-cruentous-atonement-look.md) — state: planned; acceptance criteria covered: 1, 2, 3, 4 and 5. Criterion 6 is the owner's judgement by eye, asked for when the showroom first stands (T-209).
- [INT-0004](../../../intents/INT-0004-the-look-as-a-theme-file.md) — state: planned; acceptance criteria covered: 1 to 6 (all).
- [INT-0006](../../../intents/INT-0006-the-furniture.md) — state: planned; acceptance criteria covered: 1 to 7 (all).
- [INT-0007](../../../intents/INT-0007-the-showroom.md) — state: planned; acceptance criteria covered: 1 to 5 and 7. Criterion 6 is the owner's judgement by eye (T-209). That the showroom is live on the web is built here (T-213) and seen only once the owner turns GitHub Pages on; backlog task T-104 carries that check.
- [INT-0005](../../../intents/INT-0005-versioned-releases.md) — state: active; acceptance criteria covered: 1, 2, 3, 4 and 6 again, now that a release holds the look as well. Criterion 5 still waits for the first tag (backlog task T-102).
- [INT-0001](../../../intents/INT-0001-the-cruor-framework.md) — state: active; acceptance criteria covered: 2 and 4, which waited for the look, and 1 and 5.
- [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md) — state: active; nothing new is built; T-215 confirms what the default branch holds and moves it to `realized`.

The owner approved this plan on 24 November 2026. What that approval and
the four answers given before it settled is recorded in the intents: that
the showroom may hold script and is served by GitHub Pages (INT-0007, and
INT-0001 for what "no script" is held to), that the whole theme file is
built now (INT-0004), which parts the first set of furniture holds
(INT-0006), and which families set the title, the headings, the text and
code (INT-0003). The plan was then reviewed and rewritten; what the first
review found and what was done is in `critique-round-1.md`.

## Schema Tree
- The framework is something to build with
  - The rule, and what was owed
    - T-216: the review that keeps the repository in its own terms
    - T-215: the fonts intent is realized
  - The look as data
    - T-201: the theme file, its form, and a command that reads and judges it
    - T-202: `look` writes and checks the tokens
    - T-203: the contrast the theme file promises is tested
  - The means of checking
    - T-211: a page checked in a browser
  - The look as stylesheets
    - T-204: the ground: the stone, the candle, the dark at the edges
    - T-205: the dress of plain HTML
  - The furniture
    - T-206: controls, and the one list of parts
    - T-207: containers
    - T-208: ways through a page, and small pieces
  - The showroom
    - T-209: the showroom, from the kit alone, and the owner's first sight of it
    - T-210: play
  - Out of the door
    - T-212: a release carries the look
    - T-213: the showroom is published
    - T-214: the front page's words
    - T-217: the door to the showroom
    - T-218: the front page's colours come from the theme file

Layout the sprint creates:

```text
look/        theme.toml, THEME.md, tokens.css (made by the tool),
             cruentous-atonement.css, furniture.css
showroom/    index.html, showroom.css, showroom.js
tests/       parts.py (the one list of parts), browser.py, pages/
tools/       build-site.sh
.github/workflows/pages.yml
```

How a page takes the look on, which files do it and how rules are kept
beneath the class are recorded in INT-0003; what a release holds, in
INT-0005.

**Cutting.** Nothing is cut without the owner's word. The tests of the
furniture, the showroom and the front page all read the one list of parts
(`tests/parts.py`). If the sprint will not fit, the build stops and the
owner is offered, in this order: the door's picture (T-217), the plaything
of T-210, then parts from the end of the list. What each cut leaves, which
is recorded in the test report and in the intent named:

- the door: INT-0007 criterion 5 is unmet; T-218 does not rest on it;
- the plaything: INT-0007 criterion 7 is met only in its second half (a
  part's HTML can still be taken with one press), and is recorded as
  half met;
- a part: the list and the test that pins the list to the table below
  (`test_parts_list_is_whole`) change together in one commit, and INT-0006
  is amended to say what the first set then holds.

**The designer's unread word.** What the designer meant by "rex" is left to
the owner to ask. Nothing in the sprint waits on it.

### The parts, and the states each has

| part | class, and what it goes on | text, and its bound | takes the keyboard | states at rest | states a hand brings about |
|---|---|---|---|---|---|
| button | `cruor-button`, a `<button>` or a link | its label, 4.5 | yes | as it lies; unable | pointer over; pressed; keyboard on it |
| field | `cruor-field`, an `<input>` or `<textarea>` | what is written in it, and when empty its placeholder, 4.5 | yes | empty; filled; faulty (`aria-invalid="true"`); unable | keyboard on it |
| label, hint, fault | `cruor-label`, `cruor-hint`, `cruor-fault` | its words, 4.5 | no | as it lies | none |
| choice | `cruor-choice`, a `<select>` | what is chosen, 4.5 | yes | as it lies; unable | keyboard on it. Its open list is the system's own and is not measured |
| tick box | `cruor-tick`, a checkbox | none | yes | unticked; ticked; unable | keyboard on it |
| radio button | `cruor-radio`, a radio button | none | yes | unpicked; picked; unable | keyboard on it |
| slider | `cruor-slider`, a range | none; filled with the blood | yes | as it lies; unable | keyboard on it |
| progress | `cruor-progress`, a `<progress>` | none; filled with the blood | no | with a value; without one | none |
| measure | `cruor-measure`, a `<meter>` | none; filled with the blood | no | low; middling; high | none |
| plate | `cruor-plate`, any block, or a link | a paragraph in it, 3.3; small text in it, 4.5 | when a link | as it lies | pointer over; keyboard on it |
| panel | `cruor-panel` | a paragraph in it, 3.3; small text in it, 4.5 | no | as it lies | none |
| the void | `cruor-void` | its lettering, 4.5, on its ground and on a current row | no | as it lies; with a current row | none |
| notice | `cruor-notice` | a paragraph in it, 3.3 | no | each of three kinds, asked for by `data-kind`: `note`, `warning`, `fault` | none |
| fold | `cruor-fold`, a `<details>` | its summary, 4.5; a paragraph in it, 3.3 | its summary | shut; open | keyboard on its summary |
| rise | `cruor-rise`, anything with `popover`, or a `<dialog>` | a paragraph in it, 3.3; small text in it, 4.5 | the button that raises it, and what is inside it | a `<dialog open>` | shown from its button; shown as a modal dialog from its button |
| masthead | `cruor-masthead`; it has no ground of its own and lies on the page | its title is carved, and held by the theme file's entries for the page and the stone; small text in it, 4.5 | no | as it lies | none |
| bar of links | `cruor-links` | each link, 4.5 | yes | with a current link | pointer over a link; keyboard on a link |
| trail | `cruor-trail` | each place, 4.5 | yes | with a current place | keyboard on a link |
| badge | `cruor-badge` | its word, 4.5 | no | each of two kinds: as it lies, and `data-kind="fault"` | none |
| seal, sigil, hairline, loader | `cruor-seal`, `cruor-sigil`, `cruor-hairline`, `cruor-loader` | none | no | as it lies | none |

The bounds are INT-0003's: 4.5 for interface text; 3.3 for an inscription,
which is running text of 24 pixels or more; carved letters by the theme
file's entries alone, since a browser cannot measure them. A paragraph set
in a container is an inscription there as it is on the page. A heading set
in a container that has a ground of its own is not carved: it is lettered
flat in the inscription's colour, so that it can be measured there. The
blood is never a ground that lettering is set on.

## Execution Sequence

### T-216: Before every push, search what it carries for other typefaces' names, and record it.
- **Intent:** [INT-0001](../../../intents/INT-0001-the-cruor-framework.md)
- **Touches:** docs/sprints/s1/sprint-tests/own-terms-review.md
- **Depends on:** (none)
- **Acceptance criterion:** INT-0001 5: nothing in the repository or its history names another typeface or sets Cruor beside one.
- **Success criterion (EARS):**
  - **WHEN** a push is about to be made, **THEN** an entry **SHALL** first be added to `docs/sprints/s1/sprint-tests/own-terms-review.md` naming every commit the push carries and what was found, and the push **SHALL** not be made if anything is found.
- **Notes:** this task stands first because it governs every push of the sprint; nothing is pushed before its first entry. The search is made from outside the repository, with a list kept outside it, as in Sprint 0.

### T-215: Confirm what the default branch holds and mark the fonts intent realized.
- **Intent:** [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md), [INT-0001](../../../intents/INT-0001-the-cruor-framework.md)
- **Touches:** docs/intents/INT-0002-cruor-web-fonts.md, docs/intents/INT-0001-the-cruor-framework.md, docs/work/tasks.md
- **Depends on:** (none)
- **Acceptance criterion:** INT-0002, all: it is `realized` when the default branch holds what it describes, by the rule recorded in INT-0001. INT-0001 1: the public repository holds the Book and a README.
- **Success criterion (EARS):**
  - **WHEN** the default branch on GitHub is listed, **THEN** it **SHALL** hold the thirty-two fonts, `fonts/OFL.txt`, `fonts/fonts.css`, `fonts/manifest.toml`, the Book and the README; INT-0002 **SHALL** then be moved to `realized` with that listing as its evidence, and INT-0001 **SHALL** record criterion 1 as true of the default branch.
- **Notes:** this is backlog task T-103 of Sprint 0, whole. It is done second, before any of the sprint's own work, since it rests on nothing.

### T-201: Write the look down once as `look/theme.toml`, write up the file's form, and give the tool a command that reads and judges it.
- **Intent:** [INT-0004](../../../intents/INT-0004-the-look-as-a-theme-file.md)
- **Touches:** look/theme.toml, look/THEME.md, src/theme.rs, src/main.rs, tests/theme.rs, tests/common/mod.rs, tests/test_theme_form.py
- **Depends on:** (none)
- **Acceptance criterion:** INT-0004 1: one TOML file states the look's fonts, colours and measures by role, and the form is written up so a person can write another.
- **Success criterion (EARS):**
  - **WHEN** `look --check` reads `look/theme.toml`, **THEN** it **SHALL** find: the look's name and class; the four font roles `title`, `heading`, `text` and `code`; the colour roles `page`, `panel`, `sunken`, `text`, `text-subdued`, `text-bright`, `border`, `border-subdued`, `accent`, `accent-subdued`, `link`, `inscription`, `inscription-link`, `heading-top`, `heading-foot`, `selection`, `chip-top`, `chip-foot`, `blood`, `blood-edge`, `shadow` and `vignette`; the void's `ground`, `sunken`, `row`, `text`, `text-subdued`, `accent`, `channel` and `border`; the stone's `sheen`, `sheen-opacity`, `candle` and `candle-opacity`; the measures `inscription-size`, `interface-size`, `line`, `column`, `seal-size` and `seal-font`; and for each of `h1` to `h6` a `font`, `bold`, `italic`, `underline` and `size`.
  - **WHEN** a theme file lacks any of those keys, or holds a key the form does not have, **THEN** `look --check` **SHALL** exit non-zero and name the key.
  - **WHEN** a colour is not `#rrggbb` or `rgba(r, g, b, a)`, **THEN** it **SHALL** exit non-zero and name the key.
  - **WHEN** a font role names a family that `fonts/families.toml` does not list, or a heading's `font` or the measure `seal-font` is neither one of the four roles nor such a family, **THEN** it **SHALL** exit non-zero and name the key; and **WHEN** a heading's `font` is a family the kit holds, by name, **THEN** it **SHALL** be taken.
  - **WHEN** `look/THEME.md` is read, **THEN** it **SHALL** name every table and every key that `look/theme.toml` holds.
- **Notes:** the colours are those of `docs/sprints/s0/sprint-research/look-inventory.md`, with the blood and its edge as INT-0003 records them. In this task `look --check` judges the theme file and nothing else; T-202 adds the tokens to it. `tests/common/mod.rs` learns to copy `look/` into a test's folder. Read with the `toml` crate, as `src/families.rs` reads its list.

### T-202: Have `look` write `look/tokens.css` from the theme file, and `look --check` hold the two together.
- **Intent:** [INT-0004](../../../intents/INT-0004-the-look-as-a-theme-file.md)
- **Touches:** src/look.rs, src/main.rs, look/tokens.css, tests/look.rs, tests/cli.rs
- **Depends on:** T-201
- **Acceptance criterion:** INT-0004 2: the token stylesheet is made from the theme file by one command, and a check fails if the two disagree.
- **Success criterion (EARS):**
  - **WHEN** `look` is run, **THEN** `look/tokens.css` **SHALL** hold exactly one rule, on the look's class, with one custom property beginning `--cruor-` for every colour role, every role of the void, each of the stone's four keys, every font role, every measure and each of the five settings of each heading level, each with the theme file's value, and no other declaration.
  - **WHEN** `look` is run twice, **THEN** the two files **SHALL** be byte-identical.
  - **WHEN** `look --check` is run and `look/tokens.css` is absent or differs from what the theme file gives, **THEN** it **SHALL** exit non-zero and name the file; **WHEN** they agree, **THEN** it **SHALL** exit zero.
  - **WHEN** `check` is run, **THEN** it **SHALL** fail if `look --check` would.
- **Notes:** follow `src/css.rs`: build the text in memory, compare bytes, write with line feeds. A heading's `bold`, `italic` and `underline` become `font-weight`, `font-style` and `text-decoration-line` values; its `font`, when a role, becomes that role's family. The guard script is not changed: its tests reach the look through `check`.

### T-203: Test, from the theme file, the contrast it promises.
- **Intent:** [INT-0003](../../../intents/INT-0003-cruentous-atonement-look.md), [INT-0004](../../../intents/INT-0004-the-look-as-a-theme-file.md)
- **Touches:** src/contrast.rs, src/theme.rs, src/look.rs, look/theme.toml, look/THEME.md, tests/contrast.rs, tests/test_promised_pairs.py
- **Depends on:** T-202
- **Acceptance criterion:** INT-0003 3 and 4: each text role meets its ratio on every ground it is set on, the brightest sheen of the stone included, as that criterion tells for each; INT-0004 3: those bounds are tested from the theme file's colours.
- **Success criterion (EARS):**
  - **WHEN** the theme file is read, **THEN** its `[[contrast]]` entries **SHALL** hold, each naming its text roles, its grounds and its ratio: `inscription` and `inscription-link` on `page`, `stone` and `panel` at 3.3; `text`, `text-subdued`, `link` and `accent` on `page`, `stone`, `panel` and `sunken` at 4.5; `heading-top` and `heading-foot` on `page`, and `heading-top` on `stone`, at 3; `chip-top` and `chip-foot` on `sunken` at 4.5; `text-bright` on `selection` at 4.5; the void's `text`, `text-subdued` and `accent` on its `ground` and `sunken` at 4.5; the void's `text` and `accent` on its tinted row over each of those at 4.5; the void's `channel` on its `ground` and `sunken` at 3; and `blood-edge` on `page`, `stone`, `panel` and `sunken` at 3.
  - **WHEN** `look --check` is run on the theme as written, **THEN** every entry **SHALL** hold, where `stone` is the page with the stone's sheen laid over it at its opacity and then the candle's glow laid over that at its opacity, a colour with an alpha is laid over its ground before it is measured, and the ratio found is compared with the bound without rounding.
  - **WHEN** a text colour in a copy of the theme file is dimmed until an entry fails, **THEN** `look --check` **SHALL** exit non-zero and name the text role, the ground and the ratio found to two places.
  - **WHEN** `look` is run on a theme whose contrast fails, **THEN** it **SHALL** exit non-zero and write nothing.
  - **WHEN** a `[[contrast]]` entry names a text role or a ground the theme file does not have, **THEN** `look --check` **SHALL** exit non-zero and name it.
  - **WHEN** a rule of `look/cruentous-atonement.css` or `look/furniture.css` sets both a text colour and a ground by tokens, **THEN** an entry of the theme file **SHALL** cover that pair.
- **Notes:** the ratio is WCAG 2's, from relative luminance. The last clause is tested against each stylesheet as it comes to exist; it holds trivially until T-204. It sees only a rule that sets both colours itself; a pair that arises from a ground set by one rule and lettering set or inherited from another is held by the browser's tests over the list of parts (T-206 to T-208), which measure what is drawn. The foot of a carved heading stands at 2.80 on `stone`, which INT-0003 tells; no entry promises it there, and the owner is asked about it when the showroom stands (T-209). If the owner has it lifted, the entry for the stone gains the foot and the colour changes in the theme file alone.

### T-211: Make the means of checking a page in a browser.
- **Intent:** [INT-0006](../../../intents/INT-0006-the-furniture.md), [INT-0003](../../../intents/INT-0003-cruentous-atonement-look.md)
- **Touches:** tests/helpers.py, tests/browser.py, tests/test_browser_means.py
- **Depends on:** T-203
- **Acceptance criterion:** INT-0006 4 and INT-0003 3: the bounds are checked on what a browser renders, in every state.
- **Success criterion (EARS):**
  - **WHEN** the contrast of two colours is asked of the helper, **THEN** it **SHALL** give WCAG 2's ratio: 21 for black on white, and 4.48 to two places for `#777777` on white.
  - **WHEN** a colour with an alpha is measured, **THEN** it **SHALL** first be laid over the ground given.
  - **WHEN** the ground behind some lettering is asked for, **THEN** the helper **SHALL** read it from a picture of the page with that lettering made clear: the pixels within the rectangles of the text itself, or within the content box of a control that has no element for its text, of which it gives the one least favourable to the lettering. The lettering's own shadow is taken off with its colour, since its glow is the letter's own light and not the ground it stands on. So a ground that is a gradient, a tint over another ground, or laid by a pseudo-element or a box's shadow is read as it is drawn.
  - **WHEN** the lettering lies straight on the page under the look, with no ground of its own between, **THEN** the helper **SHALL** hold it against the theme file's `stone` as well, which is the page at its brightest: with the theme as written, red 31.3, green 18.8 and blue 19.4 of 255, on which the inscription stands at 3.31.
  - **WHEN** the lettering's own colour is clear, as a carved letter's is, **THEN** the helper **SHALL** refuse to measure it and say why.
  - **WHEN** colours are read, **THEN** the page **SHALL** have been opened with stillness asked for, so that nothing is in passage between two states and no animation is running.
  - **WHEN** a page is opened with script turned off, **THEN** a script in that page **SHALL** not have run.
- **Notes:** it extends `tests/helpers.py`, which already serves a folder over HTTP for the specimen's test. The pages these tests open are written by the tests into a temporary folder and are not tracked, the one with a script in it among them, so the check that no tracked page holds a script (T-210) has nothing to trip on. Letters with a gradient clipped to them (carved headings, code chips) and visited links cannot be measured in a browser; they are held by the theme file's entries alone (T-203).

### T-204: Lay the look's ground in `look/cruentous-atonement.css`: the stone, the candle and the dark at the edges.
- **Intent:** [INT-0003](../../../intents/INT-0003-cruentous-atonement-look.md), [INT-0004](../../../intents/INT-0004-the-look-as-a-theme-file.md)
- **Touches:** look/cruentous-atonement.css, tests/test_look_css.py, tests/test_look_ground.py, tests/pages/bare.html
- **Depends on:** T-211
- **Acceptance criterion:** INT-0003 1, 2 and 4: a page that sets the class shows the stone; every rule is scoped beneath the class; the stone is drawn with no image file, sits behind the content and never lowers the ratios. INT-0004 6: the stylesheets name colours by token.
- **Success criterion (EARS):**
  - **WHEN** a stylesheet of `look/` other than `tokens.css` is read, **THEN** every style rule in it **SHALL** be nested beneath the look's class, a rule inside `@media` or `@supports` being read by its own selector; every `@keyframes` **SHALL** be named beginning `cruor-`; and it **SHALL** hold no `@import` and no `url()` whose address is not a `data:` address.
  - **WHEN** such a stylesheet names a colour outside a `data:` address, **THEN** it **SHALL** name it by a token.
  - **WHEN** a page that sets the class is opened, **THEN** `<body>` **SHALL** have a pseudo-element whose image is a `data:` address, which is fixed to the window, lies beneath the page's content, ignores the pointer, and whose opacity is the token made from the theme file's `sheen-opacity`; the candle's glow **SHALL** take its colour and its strength from the tokens made from `candle` and `candle-opacity`; and the page's ground **SHALL** be the theme file's `page`.
  - **WHEN** a page holding nothing but the stone is pictured, in a window of 1280 by 800 with stillness asked for so that the candle is at its strongest, **THEN** every `[[contrast]]` entry of the theme file on the ground `stone` **SHALL** hold against the brightest pixel of that picture, with no allowance.
  - **WHEN** the stylesheet's rules for the candle are read, **THEN** no step of its flicker **SHALL** be stronger than the candle as it is when still.
- **Notes:** the first two clauses are tested against each stylesheet as it comes to exist, so `furniture.css` falls under them from T-206. The stone is the filter recorded in the look inventory, in a `data:` address. The candle and the vignette are gradients on a second pseudo-element. This is the first time the stone's brightness is measured and not only stated. If the last clause fails, the build stops and the owner chooses between a dimmer filter and a lower opacity; no bound is loosened to pass it.

### T-205: Dress plain HTML: the inscription, carved headings, the seal, links, lists, quotations, the sigil, code and tables.
- **Intent:** [INT-0003](../../../intents/INT-0003-cruentous-atonement-look.md), [INT-0004](../../../intents/INT-0004-the-look-as-a-theme-file.md)
- **Touches:** look/cruentous-atonement.css, tests/test_look_page.py, tests/pages/plain.html
- **Depends on:** T-204
- **Acceptance criterion:** INT-0003 1 and 5: plain HTML is dressed with no further markup; motion stops under `prefers-reduced-motion: reduce`, and print is black on white with no ornament. INT-0004 4: changing a heading level in the theme file changes that heading on the page.
- **Success criterion (EARS):**
  - **WHEN** a page of plain HTML that sets the class is opened, **THEN** a paragraph **SHALL** be in the text font and the inscription's colour at 24 pixels or more; `h1` to `h6` **SHALL** each be in the font, weight, slant, underline and size the theme file gives that level; a table's cells and a code block **SHALL** be in the interface colour; inline code **SHALL** be in the code font; and a link **SHALL** be in the inscription's link colour.
  - **WHEN** that page is opened, **THEN** `h1`, `h2` and `h3` **SHALL** carry a gradient clipped to their letters; the first letter of the paragraph after the first `h1` **SHALL** be the theme file's `seal-size` times the text's size, within a pixel; an `<hr>` **SHALL** draw the sigil from a `data:` address; a `<blockquote>` **SHALL** carry a channel down its left edge; and an item of a `<ul>` **SHALL** carry a mark that is not the browser's own.
  - **WHEN** the same page is opened without the class, **THEN** the computed colour, ground, font and size of `body`, `h1`, `p`, `a`, `code`, `blockquote`, `table` and `hr` **SHALL** be those of the same page with no stylesheet linked.
  - **WHEN** the page is opened and stillness is not asked for, **THEN** at least one animation **SHALL** be running on it; and **WHEN** it is opened with `prefers-reduced-motion: reduce`, **THEN** none **SHALL** be, and no element of the page **SHALL** have a transition of any length.
  - **WHEN** the page is rendered for print, **THEN** its ground **SHALL** be white, its text black, and the stone, the candle, the seal's shadow and the sigil not shown.
  - **WHEN** a heading level's size, font, weight, slant or underline is changed in a copy of the theme file and `look` is run on the copy, **THEN** that heading on a page linking the copy's tokens **SHALL** show that change, and the other levels **SHALL** not, for each of the five settings in turn.
- **Notes:** headings read `--cruor-h1-font` and its kin, never a family by name. The carved gradient, the seal and the sigil are as the look inventory records them.

### T-206: Furniture, the controls, and the one list of parts.
- **Intent:** [INT-0006](../../../intents/INT-0006-the-furniture.md)
- **Touches:** look/furniture.css, tests/parts.py, tests/test_furniture.py, tests/test_look_css.py, tests/pages/controls.html
- **Depends on:** T-205
- **Acceptance criterion:** INT-0006 1, 4 and 5: each part is a rule usable from plain HTML with no script; its text meets the contrast bounds in every state; it can be reached and worked by the keyboard and shows where the keyboard is.
- **Success criterion (EARS):**
  - **WHEN** `tests/parts.py` is read, **THEN** it **SHALL** give, for every part of the table above that has been built, its class, the page that holds it, which of its text is measured and at which bound, whether it is filled with the blood, what of it takes the keyboard, and its states, as the table gives them.
  - **WHEN** `look/furniture.css` is read, **THEN** it **SHALL** hold a rule for the class of every part in that list, and for no class beginning `cruor-` that is not in it.
  - **WHEN** a part of this task is in any of its states, at rest or brought about, **THEN** each text the list names for it **SHALL** stand at the bound the list gives against the ground behind it, save when the part is unable to be used, where it **SHALL** stand at 3 or more.
  - **WHEN** a tick box or a radio button is ticked or picked, with script turned off, **THEN** what is drawn **SHALL** differ from what is drawn when it is not; and **WHEN** a part the list says is filled with the blood is shown, **THEN** the edge of its fill **SHALL** stand at 3 or more against the ground beside it.
  - **WHEN** Tab is pressed through the page of controls, **THEN** every part of this task that takes the keyboard **SHALL** take it in turn and, while it has it, **SHALL** show an outline or a shadow it does not show without.
  - **WHEN** Space is pressed on a tick box, an arrow on a radio button, an arrow on a slider, and an arrow on a choice, with script turned off, **THEN** each **SHALL** change as a plain control of its kind does.
- **Notes:** the parts of this task are the button, the field with its label, hint and fault, the choice, the tick box, the radio button, the slider, progress and measure. A button's label is small, so it is bone or salmon, never the inscription's crimson. The page of controls is opened with script off in every test.

### T-207: Furniture, the containers: plate, panel, the void, notice, fold and rise.
- **Intent:** [INT-0006](../../../intents/INT-0006-the-furniture.md)
- **Touches:** look/furniture.css, tests/parts.py, tests/test_furniture.py, tests/pages/containers.html
- **Depends on:** T-206
- **Acceptance criterion:** INT-0006 1, 4 and 5.
- **Success criterion (EARS):**
  - **WHEN** this task is done, **THEN** the list of parts **SHALL** hold the plate, the panel, the void, the notice, the fold and the rise, and the clauses of T-206 that run over the list (a rule for every part, contrast in every state, the keyboard reaching and marking) **SHALL** hold for them.
  - **WHEN** a paragraph is set in a plate, a panel, a notice of each kind, an open fold or a shown rise, **THEN** it **SHALL** be an inscription of 24 pixels or more and stand at 3.3 or more against that container's ground; and **WHEN** the void has a current row, **THEN** the lettering on that row **SHALL** stand at 4.5 or more against the row.
  - **WHEN** an `h1`, `h2` or `h3` is set in a plate, a panel, a notice, a fold or a rise, **THEN** it **SHALL** not be carved: its colour **SHALL** be the inscription's, and it **SHALL** stand at 3.3 or more against that container's ground.
  - **WHEN** a fold's summary is clicked or given Enter, with script turned off, **THEN** the fold **SHALL** open; and **WHEN** folds share a `name`, **THEN** opening one **SHALL** close the other.
  - **WHEN** a button whose `popovertarget` names a rise is clicked, with script turned off, **THEN** the rise **SHALL** be shown above the page; and **WHEN** Escape is pressed, **THEN** it **SHALL** be hidden.
  - **WHEN** a button whose `commandfor` names a `<dialog class="cruor-rise">` and whose `command` is `show-modal` is clicked, with script turned off, **THEN** the dialog **SHALL** open as a modal one, the page behind it **SHALL** not take the keyboard, and Escape **SHALL** close it.
- **Notes:** a fold is `<details class="cruor-fold">`. If the engine the tests run in does not open a dialog from `commandfor`, the build stops and the owner is asked; the dialog is not moved into script.

### T-208: Furniture, ways through a page and small pieces: masthead, bar of links, trail, badge, seal, sigil, hairline and loader.
- **Intent:** [INT-0006](../../../intents/INT-0006-the-furniture.md)
- **Touches:** look/furniture.css, tests/parts.py, tests/test_furniture.py, tests/pages/pieces.html, tests/pages/every-part.html
- **Depends on:** T-207
- **Acceptance criterion:** INT-0006 1, 3, 4, 5 and 6: each part is a rule beneath the class; text meets its bounds and the keyboard is shown; motion stops when asked, and print is plain.
- **Success criterion (EARS):**
  - **WHEN** this task is done, **THEN** the list of parts **SHALL** hold every part of the table above, and the clauses of T-206 that run over the list **SHALL** hold for all of them.
  - **WHEN** a masthead is shown, **THEN** the briar **SHALL** be drawn along its foot from a `data:` address; and the current link in a bar of links, and the current place in a trail, **SHALL** each be marked by `aria-current` and shown by more than its colour.
  - **WHEN** `tests/pages/every-part.html`, which holds every part of the list, is opened and stillness is not asked for, **THEN** at least one animation **SHALL** be running on it; and **WHEN** it is opened with `prefers-reduced-motion: reduce`, **THEN** none **SHALL** be, and no part **SHALL** have a transition of any length.
  - **WHEN** that page is rendered for print, **THEN** every part's ground **SHALL** be white or none, its text black, and the briar, the sigil and the loader not shown.
- **Notes:** the briar's squares are those already in `tools/draw_readme.py`.

### T-209: Build the showroom from the kit alone, laid out as a place, and show it to the owner.
- **Intent:** [INT-0007](../../../intents/INT-0007-the-showroom.md), [INT-0006](../../../intents/INT-0006-the-furniture.md), [INT-0003](../../../intents/INT-0003-cruentous-atonement-look.md)
- **Touches:** showroom/index.html, showroom/showroom.css, tests/test_showroom.py; and, only if the owner's answers ask for a change, look/theme.toml, look/tokens.css and docs/intents/INT-0003-cruentous-atonement-look.md
- **Depends on:** T-208
- **Acceptance criterion:** INT-0007 1 to 4 and 6; INT-0006 2: every part is shown in use, in every state it has at rest; INT-0003 6.
- **Success criterion (EARS):**
  - **WHEN** `showroom/index.html` is opened over HTTP from a copy of the repository, **THEN** every Cruor face it uses **SHALL** load, no request **SHALL** fail, and no request **SHALL** go to any other host.
  - **WHEN** the page is read, **THEN** every part of the list **SHALL** appear in it, in every state the list gives it at rest; and `showroom.css` **SHALL** hold no rule on a class beginning `cruor-` and no pseudo-class of state.
  - **WHEN** a part is shown, **THEN** beside it **SHALL** stand the HTML that makes it, and that HTML, set in a page of its own with the kit linked, **SHALL** draw a part of the same size and colours.
  - **WHEN** the page's stylesheets are listed, **THEN** they **SHALL** be the framework's four and `showroom.css`; and `showroom.css` **SHALL** name no colour but by a token.
  - **WHEN** the page is opened with script turned off, **THEN** every part **SHALL** still be shown.
  - **WHEN** the page is read, **THEN** it **SHALL** hold one line of code set in each of Cruor's fixed-pitch families, side by side, each named.
  - **WHEN** the showroom first stands and its tests pass, **THEN** the owner **SHALL** be shown it, and T-210, T-213, T-214, T-217 and T-218 **SHALL** not begin until the owner has said whether it is a place and not a list; whether it is the same look as Tome's; which family sets code; and whether the foot of a carved heading stays as it is, at 2.80 on the stone at its brightest, or is lifted.
- **Notes:** the page is laid out as one a visitor walks down, with parts used where such a part would be used. The side by side is what INT-0003's Consequences promise. If the owner says no, T-209 is done again before anything rests on it.

### T-210: Add play to the showroom, in script: a plaything, and a way to take a part's HTML.
- **Intent:** [INT-0007](../../../intents/INT-0007-the-showroom.md), [INT-0001](../../../intents/INT-0001-the-cruor-framework.md)
- **Touches:** showroom/showroom.js, showroom/index.html, showroom/showroom.css, tests/test_showroom_play.py, tests/test_kit_has_no_script.py
- **Depends on:** T-209
- **Acceptance criterion:** INT-0007 7: with script on, a visitor can play. INT-0001 4: a page that takes the kit on needs no script.
- **Success criterion (EARS):**
  - **WHEN** the repository's tracked files are listed, **THEN** no file whose name ends `.js` or `.mjs` **SHALL** be found outside `showroom/` and `examples/`; and no tracked HTML or SVG outside `showroom/` **SHALL** hold a `<script` element, an attribute beginning `on`, or a `javascript:` address.
  - **WHEN** the plaything is pressed and held, **THEN** blood **SHALL** fall from where it is pressed and come to rest at the foot of its ground, so that once it has settled the lowest row holds blood and the rows above the press hold none.
  - **WHEN** the button beside a part is pressed, **THEN** that part's HTML **SHALL** be on the clipboard.
  - **WHEN** the page is opened with `prefers-reduced-motion: reduce`, **THEN** the plaything **SHALL** move only while it is pressed.
- **Notes:** the plaything is a small grid of squares in the look's colours, where a square of blood falls if the square below is empty and else slides aside. Every page under `tests/pages/` is opened with script off, which the tests of T-206 to T-208 already do.

### T-212: Make a release carry the look, and make the version 0.2.0.
- **Intent:** [INT-0005](../../../intents/INT-0005-versioned-releases.md), [INT-0004](../../../intents/INT-0004-the-look-as-a-theme-file.md), [INT-0001](../../../intents/INT-0001-the-cruor-framework.md)
- **Touches:** src/bundle.rs, Cargo.toml, Cargo.lock, tests/bundle.rs, tests/common/mod.rs, tests/test_repository.py, tests/test_fetch_release.py, tests/test_release_look.py, tests/test_release.py, .github/workflows/release.yml
- **Depends on:** T-208
- **Acceptance criterion:** INT-0005 1 to 4: a release is one flat set of files with a manifest, the same bytes every time, its stylesheets working wherever they are served together, and a build that fetches it ends with the repository's files. INT-0004 5: the theme file is in each release from the one that first holds the look.
- **Success criterion (EARS):**
  - **WHEN** `bundle` is run, **THEN** the folder **SHALL** hold exactly the files of a release of 0.1.0 and, beside them, `tokens.css`, `cruentous-atonement.css`, `furniture.css` and `theme.toml`, each byte-identical to the repository's, and nothing of `showroom/`; and `manifest.json` **SHALL** give each one's size and SHA-256.
  - **WHEN** `bundle` is run twice, **THEN** the two folders **SHALL** be byte-identical.
  - **WHEN** `look/tokens.css` is not what the theme file gives, **THEN** `bundle` **SHALL** exit non-zero and write nothing.
  - **WHEN** a page in the bundle's folder links the four stylesheets by bare name and sets the class, **THEN** every face it uses **SHALL** load and the page's ground **SHALL** be the look's.
  - **WHEN** `examples/fetch-release.mjs` fetches a bundle served over HTTP, **THEN** the look's four files among those fetched **SHALL** be byte-identical to the repository's.
  - **WHEN** the crate's manifest is read, **THEN** its version **SHALL** be `0.2.0`; and the release workflow's notes **SHALL** say that a release holds the look as well as the fonts.
- **Notes:** `bundle` already refuses when a check fails. The front page's words are not changed here; they say until T-214 that the first release holds the fonts alone, which stays true of 0.1.0.

### T-213: Publish the showroom: a workflow that puts it on GitHub Pages from `main`.
- **Intent:** [INT-0007](../../../intents/INT-0007-the-showroom.md)
- **Touches:** tools/build-site.sh, .github/workflows/pages.yml, tests/test_pages.py, tests/test_release.py
- **Depends on:** T-209
- **Acceptance criterion:** INT-0007 1, as settled: the showroom is served on the web by GitHub Pages.
- **Success criterion (EARS):**
  - **WHEN** `tools/build-site.sh <folder>` is run, **THEN** the folder **SHALL** hold `showroom/`, `fonts/` and `look/` as the repository does, and an `index.html` that sends a visitor to `showroom/`; and the showroom opened from that folder over HTTP **SHALL** load every face with no failed request.
  - **WHEN** the workflow is read, **THEN** it **SHALL** run on a push to `main` and by hand; run the guards before it publishes; publish what `tools/build-site.sh` makes; hold exactly the permissions `contents: read`, `pages: write` and `id-token: write`; and publish only when the repository variable `SHOWROOM` is `published`.
- **Notes:** the owner turns Pages on and sets that variable; until then the workflow runs the guards on `main` and publishes nothing, so no run fails for want of Pages. The test that no workflow but the release's may write is amended to know this one. That the page is live is backlog task T-104.

### T-214: Bring the front page's words up to date.
- **Intent:** [INT-0001](../../../intents/INT-0001-the-cruor-framework.md), [INT-0006](../../../intents/INT-0006-the-furniture.md), [INT-0005](../../../intents/INT-0005-versioned-releases.md)
- **Touches:** assets/readme/text.md, assets/readme/page.svg, tests/test_readme.py
- **Depends on:** T-212, T-213
- **Acceptance criterion:** INT-0006 7: the README names the parts and shows how one is used. INT-0001 1, 2 and 4. INT-0005 6: the README says what a release holds.
- **Success criterion (EARS):**
  - **WHEN** the front page's words are read, **THEN** they **SHALL** say the look is in the kit; show a page linking the four stylesheets and setting the class; name every part of the list; show the HTML of one part; name `look/` and `showroom/` and what each holds; show the `look` command with the tool's others; say that a release from 0.2.0 holds the four files of the look as well; and give the showroom's address.
  - **WHEN** `python -I tools/draw_readme.py --check` is run, **THEN** it **SHALL** pass.
- **Notes:** the sentence the README's tests pin about the look not being in the kit changes here, as the test's own comment foresaw. The words say of the showroom's address that it answers once the showroom is published.

### T-217: Put a door to the showroom on the front page.
- **Intent:** [INT-0007](../../../intents/INT-0007-the-showroom.md)
- **Touches:** tools/draw_readme.py, assets/readme/door.svg, README.md, tests/test_readme_pictures.py
- **Depends on:** T-214
- **Acceptance criterion:** INT-0007 5: the front page points to the showroom through a door, a picture that is a link to it.
- **Success criterion (EARS):**
  - **WHEN** `README.md` is read, **THEN** it **SHALL** hold two pictures: the page, a link to its words, and the door, a link to the showroom's address, with an `alt` that says where it leads.
  - **WHEN** `assets/readme/door.svg` is read, **THEN** it **SHALL** stand alone as the page's picture does: no text that needs a font, no stylesheet, no script, no address but the names within itself.
  - **WHEN** `python -I tools/draw_readme.py --check` is run after the door or the words are changed by hand, **THEN** it **SHALL** fail and name which.
- **Notes:** the door is a drawing, as INT-0007 says: the showroom's name and a few shapes in the look's colours. It is the first thing offered if the sprint must be cut.

### T-218: Have the front page's script take the look's colours from the theme file.
- **Intent:** [INT-0004](../../../intents/INT-0004-the-look-as-a-theme-file.md)
- **Touches:** tools/draw_readme.py, assets/readme/page.svg, tests/test_readme_pictures.py; and assets/readme/door.svg if the door exists
- **Depends on:** T-214
- **Acceptance criterion:** INT-0004 6: everything in the repository that shows the look takes its colours and its families from the theme file.
- **Success criterion (EARS):**
  - **WHEN** `tools/draw_readme.py` is read, **THEN** the only colours written out in it **SHALL** be the briar's squares, and every other colour **SHALL** be read from `look/theme.toml` by its role; and the families it sets the title, the headings, the text and code in **SHALL** be read from the theme file's four font roles.
  - **WHEN** a colour role is changed in a copy of the theme file and the script is run on the copy, **THEN** the page's picture **SHALL** hold the new colour and not the old.
- **Notes:** a drawing's own colours are the briar's squares, in the script, and the statue's two maps, which are files of their own. The sizes the picture sets its words at stay the picture's own: it is laid out to be read at the width a README is shown, which is not what the look's measures are for. It draws the door again only if the door exists (T-217), and does not rest on it; when both are built it follows T-217 in the sequence, since both change the script and its tests.
