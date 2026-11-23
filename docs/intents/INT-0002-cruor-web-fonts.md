# INT-0002 — Cruor's web fonts

<!-- sprint-loop-intent-v2 -->
- **Intent ID:** INT-0002
- **State:** active
- **Work evidence:** [T-001, T-003 to T-007, T-011 and T-013, Sprint 0 build plan](../sprints/s0/sprint-plans/build-plan.md), [T-101 and T-103 backlog](../work/tasks.md)
- **Completion evidence:** [T-001, T-003 to T-007, T-011 and T-013, completed tasks](../work/completed-tasks.md)
- **Code evidence:** [fonts/fonts.css](../../fonts/fonts.css), [fonts/manifest.toml](../../fonts/manifest.toml), [fonts/OFL.txt](../../fonts/OFL.txt), [fonts/specimen.html](../../fonts/specimen.html), [tools/check_fonts.py](../../tools/check_fonts.py)
- **Test evidence:** [Sprint 0 test report](../sprints/s0/sprint-tests/test-report.md)
- **Documentation evidence:** [README](../../README.md)

## Intent

The framework holds Cruor's web fonts, and a page that links one stylesheet
can set its text in any of them.

Asked on 23 November 2026 which families are published, the owner answered
"All eight families". Each family has four styles, Regular, Bold, Italic and
Bold Italic, so the framework holds thirty-two `.woff2` files:

| family | what it is |
|---|---|
| Cruor Sans Regular | the bare letters, each at a width of its own |
| Cruor Lite Regular | curled spurs at the posts and one thornament a letter, each letter at a width of its own |
| Cruor Thornamental Regular | three tiers of thornaments on the capitals, barbs, and a channel cut along the broad strokes, each letter at a width of its own |
| Cruor Sans Mono | the bare letters, every character in one cell |
| Cruor Lite Mono | the Lite letters, every character in one cell |
| Cruor Thornamental Mono | the Thornamental letters, every character in one cell |
| Cruor Sans Pixelated | the Sans letters on a lattice of squares |
| Cruor Pixelated | the Lite letters on the same lattice |

Asked the same day under what terms the fonts are offered, the owner
answered "SIL Open Font License 1.1". Asked whether the licence reserves a
font name, they answered: 'Reserve "Cruor"'.

Boundaries:

- The fonts are published as WOFF2, the form a web page loads. Other forms
  are not part of this intent.
- The framework does not draw, change or rebuild the fonts. It takes the
  files as the Cruor project builds them, and records which build they are.

## Acceptance criteria

1. The repository holds the thirty-two `.woff2` files of the eight families
   above, named by family and style (as `CruorLiteMono-BoldItalic.woff2`
   is).
2. The text of the SIL Open Font License 1.1 stands beside the fonts with
   the copyright line "Copyright (c) 2026, Charles Russella
   (https://github.com/crussella0129), with Reserved Font Name Cruor.", and
   the README says the fonts are offered under it.
3. One stylesheet declares every family under its own name with its four
   styles joined, so that a page asking a family for its bold or its italic
   is given that file.
4. In a browser, a page that links that stylesheet loads each of the
   thirty-two faces and sets text in it.
5. A manifest records, for every font file, its SHA-256 and its size, and
   which build of Cruor the files came from. A check fails if a font file
   and the manifest disagree, or if a font's own name for its family and
   style disagrees with its `@font-face` rule.
6. No file from the Cruor project other than these thirty-two is in the
   repository.

## Rationale

The fonts are what makes the look the owner's own, and they are the first
thing Tome waits on. Holding all eight families keeps one place where every
published cut of Cruor can be had. The Open Font License is the owner's
choice of terms.

## Alternatives

- **The six smooth families only**, leaving the two Pixelated families for
  later. Offered; the owner chose all eight.
- **The three proportional families only.** Code on a page would then fall
  back to the reader's own fixed-pitch font.
- **Other terms** (all rights reserved; deciding later). The owner chose the
  Open Font License.
- **Fonts attached to releases but not tracked in the repository.** Not
  taken: the repository is the kit, a release is put together from tracked
  files, and anyone reading the repository can see exactly what a release
  holds.

## Consequences

- Once published, the font files can be had by anyone, and the licence lets
  them be used, changed and passed on.
- The name Cruor is reserved under the licence. Anyone may use, change and
  pass on the fonts, but a changed version must take another name, and that
  includes a subset made to save bytes. The owner's own releases keep the
  name.
- The fonts' own name tables carry no copyright or licence text today, and
  their embedding field says "preview and print" where a font under an open
  licence usually says "installable". Both are set where the fonts are
  built, not here. The fonts are taken in as they are built; the licence
  file beside them is what states their terms, and the README says so. A
  later build of Cruor that sets these fields is taken in as a later
  version (backlog task T-101).
- Which build is taken in: a clean build at the head of the Cruor
  project's working branch at the time, with its commit recorded in the
  manifest. The owner approved this with Sprint 0's plan. Cruor's next
  characters are still being drawn; what the first intake holds is what
  that build holds, and the manifest and the review of the intake say what
  that is.
- A newer build of Cruor (more characters, kerning) is taken in as a new
  version of the framework, with a new manifest.

## Transition history
- 2026-11-23: created as `proposed` in Sprint 0's Research, from the owner's
  answers that day.
- 2026-11-23: revised during Sprint 0's Plan, still `proposed`. The owner
  chose to reserve the font name Cruor; criterion 2 and the Consequences now
  say so.
- 2026-11-23: `proposed` to `planned`. The owner approved Sprint 0's plan, which takes the fonts in and builds their licence file, stylesheet, manifest, checks and specimen page (T-001, T-003 to T-007).
- 2026-11-23: revised after the plan's review, still `planned`. Criterion 2
  now gives the copyright line as written; the Consequences record the
  fonts' embedding field, that the fonts go in as built (T-101 carries the
  rest), and which build is taken in.
- 2026-11-23: revised after the plan's second review, still `planned`. The
  Consequences no longer say in advance what the first intake covers.
- 2026-11-23: `planned` to `active`. Sprint 0's Build began with T-001, the
  ground the checks stand on.
- 2026-11-23: Test evidence attached, still `active`. Sprint 0's Test
  phase proved all six criteria on `dev`. The criteria speak of what the
  repository holds, and its default branch holds no font until the
  sprint's pull request is merged, so the move to `realized` waits for
  that merge.
