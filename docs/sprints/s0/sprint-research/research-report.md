# Sprint 0 Research Report

## Intents Reviewed
- [INT-0001](../../../intents/INT-0001-the-cruor-framework.md) — created; relevance: the framework itself, its name, its first version and the terms for its code; this sprint gives it a README and licences; current state: proposed.
- [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md) — created; relevance: the thirty-two web fonts, their licence, their stylesheet and their manifest, all of which this sprint builds; current state: proposed.
- [INT-0005](../../../intents/INT-0005-versioned-releases.md) — created; relevance: the release a build fetches, which this sprint makes ready; current state: proposed.
- [INT-0003](../../../intents/INT-0003-cruentous-atonement-look.md) — created; relevance: the look and its name; recorded now, built in a later sprint; current state: proposed.
- [INT-0004](../../../intents/INT-0004-the-look-as-a-theme-file.md) — created; relevance: the theme file the tokens are made from; recorded now, built with the look; current state: proposed.

## 1. Sprint Goal

Make the framework hold Cruor's fonts and be ready to release them. At the
end of the sprint the repository holds the thirty-two `.woff2` files with
their licence, one stylesheet that declares all eight families, and a
manifest of checksums; one command puts a release together; a pushed version
tag publishes it; and the README says what the kit is and how a build
fetches it. The look and its theme file are the next sprint. This order is
chosen because the fonts are what Tome waits on, and because a release that
holds only fonts proves the way pages take the framework in before there is
more to carry.

## 2. Existing Code Survey

This repository is new; the files surveyed are those the framework is drawn
from, in Tome and in the Cruor project, and the model the owner named.

| File | Relevance | Notes |
|------|-----------|-------|
| Tome `src/styles/sanguine.css` | high (later sprint) | The look's rules: stone, candle, inscription, carved headings, seal, sigil, quotes, chips, briar, stillness, print. Bound to Tome's class names |
| Tome `src/styles/tokens.css` | high (later sprint) | The look's colours, set on Tome's theme tokens under its theme class |
| Tome `src/styles/theme.ts` | high (later sprint) | The role contract the contrast test reads: text roles, grounds, the stone's brightest tone |
| Tome `src/components/TocSidebar.module.css` | medium (later sprint) | The void, its hairlines and the vertical briar |
| Tome `src/components/ThemePicker.tsx` | low | The riddle and the wash; stays in Tome |
| Tome `scripts/fetch-fonts.mjs` | high | How Tome takes a font in today: fetched by address when it builds, skipped if present, never failing the build. The release's files must be fetchable one by one in the same way |
| Tome `docs/intents/INT-0022`, `INT-0025` | high (later sprint) | The look's acceptance criteria and the reasons for its colours and sizes |
| Tome `docs/intents/INT-0027` | high | Tome fetches Cruor's fonts from the framework and keeps no font file; names the families it sets titles, text and code in |
| Tome `docs/intents/INT-0028` | medium (later sprint) | Themes as TOML files, with fonts by role and by heading level |
| Cruor project `README.md` | high | The eight families, their four styles, what each covers, and the one command that builds them |
| Cruor project, build output | high | Thirty-two `.woff2` files; see `font-inventory.md` |
| Cruor project `Cargo.toml`, `rust-toolchain.toml` | medium | Built in Rust on a pinned toolchain; checked with Python and fontTools. The framework's tool and checks follow the same division |
| www-sacred `global-fonts.css`, `global.css`, `components/` | medium | The model: one repository holding a look's fonts, tokens and parts. Its parts are React components; the framework's first version is stylesheets |
| www-sacred `package.json`, `LICENSE.md` | low | Version numbers on the kit; MIT |

## 3. External Sources
- [internet-development/www-sacred](https://github.com/internet-development/www-sacred) — the kit the owner named as the model; how it lays out fonts, tokens and components.
- [SIL Open Font License 1.1, official text](https://openfontlicense.org/open-font-license-official-text/) — the licence the owner chose for the fonts; it must travel with every copy, as a text file or in the fonts' own fields.
- [OFL FAQ](https://openfontlicense.org/ofl-faq/) — what reserving a font name means: a changed version, a subset included, must take another name.
- [GitHub Docs: linking to releases](https://docs.github.com/en/repositories/releasing-projects-on-github/linking-to-releases) — a release's files are had at `releases/download/<tag>/<file>`, one flat set of names for each release.
- [MDN: `@font-face`](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face) — joining four files under one family by `font-weight` and `font-style`; `font-display`.

## 4. Risks, Unknowns, Dependencies
- **Risk: a release is flat.** GitHub gives a release's files one flat set
  of names, with no folders. So the fonts, their stylesheet and their
  licence are kept together in one folder in the repository, and the
  stylesheet refers to each font by its bare file name. The same files then
  work in the repository, in an archive and as a release.
- **Risk: a font and its rule disagree.** A rule could name the wrong file,
  or a file could be the wrong style. The family and style each font gives
  for itself are checked against its `@font-face` rule, and a browser test
  loads every face.
- **Risk: the name "Cruor Sans Regular" is a family, and "Regular" is also
  a style.** The stylesheet uses each font's own family name exactly, so
  `font-family: "Cruor Sans Regular"` with `font-weight: bold` is the Bold
  of that family. The README says so.
- **Risk: publishing cannot be taken back.** Once the fonts are pushed to a
  public repository they can be had by anyone. The owner chose this and its
  terms on 23 November 2026. A release is still published only on the
  owner's word.
- **Unknown: whether the name Cruor is reserved under the licence.** It
  changes what others may do with a changed version, so it is the owner's
  to say before the licence file is written.
- **Unknown: which build of Cruor is taken in.** Cruor is still growing
  (its next characters are in progress). The framework takes one clean
  build at a commit the owner names, records that commit in the manifest,
  and takes newer builds in as newer versions.
- **Dependency: the fonts' own licence fields.** The built fonts carry no
  copyright or licence text and mark their embedding as "preview and
  print" (`font-inventory.md`). That is set in the Cruor project. The
  licence file beside the fonts satisfies the licence meanwhile.
- **Dependency: Tome.** Tome's own sprint takes the framework in. Nothing
  here changes Tome.

## 5. Recommended Approach

Primary: a small Rust tool in this repository, with Python checks beside
it, as the Cruor project itself is arranged.

- `fonts/` holds the thirty-two `.woff2` files, `OFL.txt`, `fonts.css` and
  a hand-written list of the eight families (name, file stem, kind).
- The tool reads that list and does three things: writes `fonts.css` from
  it; writes and checks the manifest (each file's size and SHA-256, and the
  commit of Cruor the fonts were built at); and puts a release together in
  an output folder (the files, one archive, the manifest).
- Python checks, with fontTools and a headless browser, prove what the tool
  cannot see: that each font's own family, style and weight agree with its
  rule, that a browser loads all thirty-two faces, and that a build which
  fetches the release over HTTP and checks it ends with the right bytes.
- CI runs all of it on each push. A second workflow publishes a release
  when a version tag is pushed.

Alternative considered: Python alone, since the checks need it anyway.
Not chosen: the tool is what pages and later sprints lean on (the theme
file's tokens will be made by it), a Rust path for it is short, and Rust is
the owner's default.

Alternative considered: the look in the same sprint. Not chosen: the look
and the theme file are one piece of work with its own judging by eye, and
the fonts alone already let Tome begin.

Rationale: the sprint ends with something a second project can use, and
with the release path proven on the smallest thing it will carry.

## Artifacts
- `font-inventory.md` — the thirty-two fonts as built: names, sizes, glyph
  counts, and what the fonts say of themselves.
- `look-inventory.md` — the look as it stands in Tome: colours by role, its
  parts and how each is made, and what binds it to Tome. For the sprint
  that builds the look.
