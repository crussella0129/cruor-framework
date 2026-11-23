# INT-0002 — Cruor's web fonts

<!-- sprint-loop-intent-v2 -->
- **Intent ID:** INT-0002
- **State:** proposed
- **Work evidence:** none
- **Completion evidence:** none
- **Code evidence:** none
- **Test evidence:** none
- **Documentation evidence:** none

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
answered "SIL Open Font License 1.1".

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
   the owner's copyright line, and the README says the fonts are offered
   under it.
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
- Whether the name Cruor is reserved under the licence (so that a changed
  version must take another name) is settled when the licence file is
  written.
- The fonts' own name tables carry no copyright or licence text today; that
  is set where the fonts are built, not here. The licence file beside the
  fonts is what states their terms.
- A newer build of Cruor (more characters, kerning) is taken in as a new
  version of the framework, with a new manifest.

## Transition history
- 2026-11-23: created as `proposed` in Sprint 0's Research, from the owner's
  answers that day.
