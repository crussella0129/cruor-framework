# Sprint 1 Research Report

## Intents Reviewed
- [INT-0003](../../../intents/INT-0003-cruentous-atonement-look.md) — selected; relevance: the look itself, as stylesheets scoped beneath one class, which this sprint builds; current state: proposed.
- [INT-0006](../../../intents/INT-0006-the-furniture.md) — created; relevance: the parts a page is built from, dressed in the look, which a designer's reading showed to be missing; current state: proposed.
- [INT-0007](../../../intents/INT-0007-the-showroom.md) — created; relevance: a page built only from the kit, where the look and its parts are seen and tried; current state: proposed.
- [INT-0004](../../../intents/INT-0004-the-look-as-a-theme-file.md) — selected; relevance: the theme file the look's tokens are made from, which the look's contrast tests read; whether it is built in this sprint or the next is for the plan; current state: proposed.
- [INT-0005](../../../intents/INT-0005-versioned-releases.md) — selected; relevance: a release must carry the stylesheets as it carries the fonts; current state: active.
- [INT-0001](../../../intents/INT-0001-the-cruor-framework.md) — selected; relevance: the framework is not what it says it is until it holds the look; current state: active.
- [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md) — selected; relevance: built in Sprint 0 and now on the default branch; this sprint confirms that and moves it to `realized`; current state: active.

## 1. Sprint Goal

Make the framework something to build with. At the end of the sprint the
repository holds Cruentous Atonement as stylesheets that a page takes on by
linking them and setting one class; a first set of furniture (buttons,
fields, plates, notices, a masthead and the rest) that works from plain
HTML with no script; and a showroom, a page built from the kit alone, where
a visitor sees all of it in use and can try it. The front page points to the
showroom. A release carries the stylesheets with the fonts.

## 2. Existing Code Survey

| File | Relevance | Notes |
|------|-----------|-------|
| Tome `src/styles/sanguine.css` | high | The look's rules as they stand: stone, candle, inscription, carved headings, seal, sigil, quotations, chips, briar, plates, stillness, print. Every rule hangs from Tome's theme class and Tome's own class names |
| Tome `src/styles/tokens.css` | high | The look's colours on Tome's general tokens and on tokens named for the look's old name |
| Tome `src/components/TocSidebar.module.css` | high | The void and its hairlines |
| `docs/sprints/s0/sprint-research/look-inventory.md` | high | The look's colours by role, its parts and how each is made, and the stone's bounds for the contrast test. Made in Sprint 0 for this sprint |
| `fonts/fonts.css` | high | The families the look names; written by the tool, never by hand |
| `fonts/families.toml` | medium | The list the stylesheet is made from; the pattern a theme file would follow |
| `src/css.rs` | high | How the tool writes a stylesheet from data and checks it is current; tokens made from a theme file would be written the same way |
| `src/bundle.rs` | high | What a release holds: today the fonts, their stylesheet and the licences, by fixed names in one flat set. The look's stylesheets must be added here |
| `src/main.rs` | medium | The tool's commands; a new one for the tokens belongs beside `css` |
| `fonts/specimen.html` | medium | The one page the repository has; the showroom is its larger kin, and its test is the pattern for the showroom's |
| `tests/test_specimen.py` | high | Opens a page over HTTP in a headless browser and checks every face loads with no failed request |
| `tools/draw_readme.py` | medium | Draws the front page from its words; holds the look's colours and ornaments a second time, as constants. It must come to show the showroom |
| `assets/readme/text.md` | medium | The front page's words, which say the look is not in the kit yet |
| `tests/test_readme.py` | medium | Pins that sentence and the paragraph that names the look; both change with this sprint, as the test's own comment says |
| `tools/run-guards.sh` | medium | Every check, in one order; CI runs exactly this |
| `.github/workflows/release.yml` | low | Publishes whatever `bundle` makes; it needs no change if the bundle does the work |

## 3. External Sources

- [The model kit's components](https://github.com/internet-development/www-sacred/tree/main/components) — the kit the owner named as the model in Sprint 0: the list of parts a person expects of a kit of this kind, and that it holds playthings.
- [The popover attribute, MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/popover) — a part that comes up over the page with no script; the base of the kit's "rise".
- [The details element, MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/details) — a part that opens and closes, and several sharing a name that open one at a time.
- [Invoker Commands, MDN](https://developer.mozilla.org/en-US/docs/Web/API/Invoker_Commands_API) — a button that opens a dialog as a modal one with no script (`commandfor`, `command="show-modal"`); the newest thing the furniture rests on. Read during the Plan, after the first review, in place of a source on `@scope`: plain nesting was chosen to keep rules beneath the class, as INT-0003 records.
- [WCAG 2.2, contrast (minimum)](https://www.w3.org/TR/WCAG22/#contrast-minimum) — the bounds INT-0003 holds each text role to, and the large-text threshold the inscription relies on.

## 4. Risks, Unknowns, Dependencies

- **Risk:** the sprint is large: a look, a dozen kinds of part and a page. If it will not fit, the furniture is cut to its first few kinds before the look or the showroom is.
- **Risk:** controls drawn by rules alone differ between engines (sliders, bars of progress, the open list of a select). The tests run in one engine; what the others show is judged by eye.
- **Risk:** the look's crimson cannot be small text. Every part's lettering must be bone or salmon unless it is 24 pixels or more, which a button's label usually is not.
- **Risk:** the blood the owner chose for the statue (`#3c0606`) is near the page's ground; used for a part's fill it needs a lighter edge or it is not seen.
- **Unknown:** whether the showroom may hold script for the sake of play. The kit may not.
- **Unknown:** where the showroom is served from. Serving it on the web needs the owner to turn that on for the repository.
- **Unknown:** whether the theme file (INT-0004) is built now or after. The contrast tests want the colours as data either way.
- **Unknown:** the class a page sets, and how the stylesheets are named and divided in a release.
- **Unknown:** what the designer meant by "rex". Left to the owner to ask; nothing in the sprint waits on it.
- **Dependency:** the release path of Sprint 0 has never run; the first tag, `v0.1.0`, still waits for the owner's word. A version that holds the look would be the second.
- **Dependency:** Tome's INT-0027 takes the framework in; it expects tokens that begin `--cruor-` and a class to set.

## 5. Recommended Approach

Primary: build in three layers, each usable without the next. First the
look: tokens, the stone and the dress of plain HTML, scoped beneath one
class, with the colours' contrast held by test. Then the furniture, as one
stylesheet of parts that needs the first and no script. Then the showroom,
written in plain HTML against those two files and opened by a browser test
as the specimen is. The colours are kept as data from the start, so that
the theme file is a small step whenever it is taken. The front page gains a
pointer to the showroom and a picture of it.

Alternative considered: answer the designer with more ornament on the front
page (a sketch was made: stone, candles, blood running down the page). Not
chosen: it adds to what was said to be right already and gives a person
nothing to build with.

Alternative considered: scripted components, as the model kit has. Not
chosen: the owner ruled them out, and a browser now gives enough without.

Rationale: the look is finished work that only needs loosing from Tome; the
furniture is the new work and the risk; the showroom is what proves both
and what a visitor will judge the kit by.

## Artifacts
- `designer-reading.md` — what the designer said, as the owner passed it on, and how it is read.
- `furniture-survey.md` — the parts the look has in Tome, the parts the model kit holds, what a browser gives without script, and a first set.
