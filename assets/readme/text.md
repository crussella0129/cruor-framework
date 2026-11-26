# The Cruor Framework

A kit that gives a web page the look called **Cruentous Atonement**, set in
Cruor.

*Cruor* is Latin for blood that has been shed, and *cruentus* is its
adjective. Cruor is a typeface family of tall, narrow letters with ornament
of its own: curled spurs, and thorns that are called thornaments.

**What it holds.** The look is in the kit: Cruor's web fonts; Cruentous
Atonement as stylesheets, made from one theme file; and the look's
furniture, the parts a page is built from. A page takes all of it on with
four stylesheets and one class, and the kit holds no script.

**The showroom** is a place built from the kit and from nothing else, where
the look and every part can be seen and tried:
[crussella0129.github.io/cruor-framework/showroom/](https://crussella0129.github.io/cruor-framework/showroom/).
That address answers once the showroom is published. Until then, and at any
time, serve a copy of the repository and open `showroom/index.html`.

The first release, 0.1.0, holds the fonts alone; a release from 0.2.0 holds
the look as well. The
[releases page](https://github.com/crussella0129/cruor-framework/releases)
shows what has been published.

The repository's front page shows these words as one picture: every letter
is drawn from the fonts, in the look's colours. `assets/readme/text.md`
holds the same words as text.

## What is in it

| where | what |
|---|---|
| `fonts/` | Cruor's web fonts, thirty-two `.woff2` files; `fonts/fonts.css`, which declares them; `fonts/OFL.txt`, their licence; `fonts/specimen.html`, a page that sets a line in every one |
| `look/` | the look: `look/theme.toml`, where it is written down once; `look/tokens.css`, made from that file; `look/cruentous-atonement.css`, the stone and the dress of plain HTML; `look/furniture.css`, the parts; `look/THEME.md`, the form of the theme file |
| `showroom/` | the showroom: one page built from the kit alone, with every part in use and the HTML that makes each beside it |
| `examples/fetch-release.mjs` | a worked example of a build fetching a release and checking it |
| `src/` | the tool that writes the stylesheet, the manifest and a release |
| `tools/` | the checks; `tools/draw_readme.py`, which draws the front page; `tools/draw_showroom.py`, which draws the showroom's pictures; `tools/build-site.sh`, which puts the showroom's site together |
| `assets/readme/` | the front page's words, its two pictures of a statue, and the picture drawn from them all |
| `docs/` | the project's record: what it is for, and how each part came to be |

## The look

A page takes Cruentous Atonement on by linking four stylesheets and setting
one class on its body:

```html
<link rel="stylesheet" href="fonts/fonts.css">
<link rel="stylesheet" href="look/tokens.css">
<link rel="stylesheet" href="look/cruentous-atonement.css">
<link rel="stylesheet" href="look/furniture.css">

<body class="cruentous-atonement">
```

Plain HTML is then dressed with no further markup: the obsidian stone
beneath the page, running text as an inscription in crimson, carved
headings, links, lists, quotations, rules, code and tables. A page that
does not set the class is not touched. All motion stops for a reader who
asks for stillness, and in print the page is black on white.

The four stylesheets name no path and none imports another, so they work
wherever they are served together. The first three are enough for a page
that wants the look without the parts.

### The furniture

The parts a page is built from. Each is asked for by a class on the element
HTML already has for it:

| kind | parts |
|---|---|
| controls | `cruor-button`, `cruor-field`, `cruor-label`, `cruor-hint`, `cruor-fault`, `cruor-choice`, `cruor-tick`, `cruor-radio`, `cruor-slider`, `cruor-progress`, `cruor-measure` |
| containers | `cruor-plate`, `cruor-panel`, `cruor-void`, `cruor-notice`, `cruor-fold`, `cruor-rise` |
| ways through a page | `cruor-masthead`, `cruor-links`, `cruor-trail` |
| small pieces | `cruor-badge`, `cruor-seal`, `cruor-sigil`, `cruor-hairline`, `cruor-loader` |

A field with its label, the fault it reports, and a button:

```html
<label class="cruor-label" for="day">The day it was incurred</label>
<input class="cruor-field" id="day" aria-invalid="true"
       aria-describedby="day-fault">
<p class="cruor-fault" id="day-fault">That is no day of the calendar.</p>

<button class="cruor-button">Atone</button>
```

A state is asked for as HTML asks for it: `disabled`, `aria-invalid="true"`,
`aria-current`, an open `<details>`. A part's kind is given by `data-kind`,
as a notice's `note`, `warning` or `fault` is. The showroom shows each part
in every state, with its HTML.

### The theme file

`look/theme.toml` is the look written down once, by role: its colours, the
families that set the title, the headings, the text and code, each level of
heading, its measures, and the contrast it promises between lettering and
ground. `look/tokens.css` is made from that file by the tool and never by
hand, and the tool refuses a theme that does not keep the contrast it
promises. `look/THEME.md` gives the file's form, so that another look can be
written in it.

## The fonts

Eight families, each in four styles: Regular, Bold, Italic and Bold Italic.

<!-- specimen -->

| family | what it is |
|---|---|
| Cruor Sans Regular | the bare letters, each at a width of its own |
| Cruor Lite Regular | curled spurs at the posts and one thornament a letter, each letter at a width of its own |
| Cruor Thornamental Regular | three tiers of thornaments on the capitals, barbs, and a channel cut along the broad strokes, each letter at a width of its own |
| Cruor Sans Mono | the bare letters, every character in one cell |
| Cruor Lite Mono | the Lite letters, every character in one cell |
| Cruor Thornamental Mono | the Thornamental letters, every character in one cell |
| Cruor Sans Pixelated | the Sans letters on a lattice of squares, every character in one cell |
| Cruor Pixelated | the Lite letters on the same lattice |

A font file is named for its family and style, as
`CruorLiteMono-BoldItalic.woff2` is. Open `fonts/specimen.html` in a browser
to see all thirty-two.

### Using them in a page

Serve the fonts' folder with the page, link `fonts.css`, and name a family:

```html
<link rel="stylesheet" href="fonts/fonts.css">
<style>
  body { font-family: "Cruor Lite Regular", serif; }
  h1 { font-family: "Cruor Thornamental Regular", serif; }
  code { font-family: "Cruor Sans Mono", monospace; }
</style>
```

`fonts.css` names each font by its bare file name, so it works wherever it
is served beside the fonts. A browser fetches only the faces a page uses.

A family's bold and italic are asked for with `font-weight` and
`font-style`, as for any family: an `<h1>` or a `<strong>` set in
"Cruor Lite Regular" is given that family's Bold, and an `<em>` its Italic.

In a name such as "Cruor Sans Regular" the last word is part of the family's
name, not a style. It tells the family whose letters each have a width of
their own from Cruor Sans Mono, whose characters all fill one cell. So
`font-family: "Cruor Sans Regular"; font-weight: bold` is the Bold of Cruor
Sans Regular.

<!-- picture weeping-profile -->

## Taking a release into a build

Each version of the framework is a release on GitHub, and a page takes the
framework in by fetching a release's files when it builds. A page that
builds this way keeps no font file in its own repository.

A release's files are one flat set of names, each at

```text
https://github.com/crussella0129/cruor-framework/releases/download/v<version>/<file>
```

A release holds the thirty-two fonts, `fonts.css`, `OFL.txt`, `LICENSE-MIT`
and `LICENSE-APACHE`; from 0.2.0, the look's four files as well,
`theme.toml`, `tokens.css`, `cruentous-atonement.css` and `furniture.css`;
`manifest.json`, which gives the version and each of those files' name, size
and SHA-256; one archive of them all, `cruor-framework-v<version>.zip`; and
the archive's checksum beside it. The showroom is no part of a release.

`examples/fetch-release.mjs` shows a build fetching a release and checking
every file against the manifest. It needs Node 20 or newer and nothing else:

```sh
node examples/fetch-release.mjs \
  https://github.com/crussella0129/cruor-framework/releases/download/v0.1.0/ \
  public/fonts \
  --manifest-sha256 <the SHA-256 of that release's manifest.json>
```

Pin the manifest's SHA-256 in your build, beside the version. With that one
value fixed, every file the manifest lists is fixed too, and the build gets
exactly the files it expects. Without `--manifest-sha256` the check shows
only that the files and the manifest agree with each other.

The example fails if a file cannot be fetched or does not check. Copy it
into a build and change it to suit: a build may prefer to warn and carry on
with a fallback font.

## The tool

```sh
cargo run --release -- css
cargo run --release -- manifest
cargo run --release -- look
cargo run --release -- check
cargo run --release -- bundle --out dist
```

- `css` writes `fonts/fonts.css` from the list of families,
  `fonts/families.toml`.
- `manifest` writes `fonts/manifest.toml`: each font's size and SHA-256,
  and the commit of Cruor the fonts were built at.
- `look` writes `look/tokens.css` from the theme file, `look/theme.toml`.
- `check` fails if the fonts' stylesheet, the manifest or the look's tokens
  is not current, if a font has changed, or if the theme file does not keep
  the contrast it promises.
- `bundle` puts a release together in a folder, exactly as it would be
  published. The same commit gives the same bytes every time.

A release is published by `.github/workflows/release.yml` when a version tag
is pushed, and only for a tagged commit on `main`. The showroom is published
by `.github/workflows/pages.yml` from `main`, once the repository has been
set to allow it.

## Checking

```sh
bash tools/run-guards.sh
```

This is every check the repository has, and it is what CI runs. It needs:

- the Rust toolchain that `rust-toolchain.toml` names;
- Python 3.11 or newer with the packages of `tools/requirements.txt`;
- the browser Playwright drives, had with
  `python -m playwright install chromium`;
- Node 20 or newer;
- on Windows, Git Bash.

## Terms

**The fonts** are offered under the SIL Open Font License 1.1, with the
font name Cruor reserved. `fonts/OFL.txt` is what states the fonts' terms;
the font files carry no licence text of their own. You may use the fonts,
change them and pass them on, in commercial work too. A changed version, a
subset included, must take another name.

**The code** (the stylesheets, the tool, the checks and the examples) is
offered under `MIT OR Apache-2.0`, at your choice: see `LICENSE-MIT` and
`LICENSE-APACHE`.

**The statue** on the front page and in the showroom is Michelangelo's
David, drawn from two photographs by Jörg Bittner Unna:
[JBU 005](https://commons.wikimedia.org/wiki/File:%27David%27_by_Michelangelo_FI_Acca_JBU_005.jpg)
and
[JBU 014](https://commons.wikimedia.org/wiki/File:%27David%27_by_Michelangelo_FI_Acca_JBU_014.jpg),
both offered under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Each was cut from
its ground, darkened, given tears of blood and reduced to squares. The two
pictures made from them, `assets/readme/weeping-face.txt` and
`assets/readme/weeping-profile.txt`, are offered under CC BY 4.0 as well,
and so are the front page's picture where it shows them and the showroom's
pictures drawn from them. They are not part of a release.

**The head** over the door to the showroom is drawn from a photograph of a
plaster cast of David's head by Palnatoke,
[Fra statuen af David](https://commons.wikimedia.org/wiki/File:Fra_statuen_af_David_DSCF0465.JPG),
offered under
[CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/). It was cut
from its ground, darkened and reduced to squares. The picture made from it,
`assets/readme/door-crest.txt`, is offered under CC BY-SA 3.0, and so is the
door's picture, `assets/readme/door.svg`, which shows it. Neither is part of
a release.

<!-- sigil -->

Copyright (c) 2026 Charles Russella.
