# The Cruor framework

A kit that gives a web page the look called **Cruentous Atonement**, set in
Cruor.

*Cruor* is Latin for blood that has been shed, and *cruentus* is its
adjective. Cruor is a typeface family of tall, narrow letters with ornament
of its own: curled spurs, and thorns that are called thornaments.

**Where it stands.** The kit holds Cruor's web fonts, and a page can set its
text in them today. The look itself, Cruentous Atonement (its colours, its
stylesheet and its theme file), is not in the kit yet: it is what is built
next. The first release, 0.1.0, holds the fonts alone; the
[releases page](https://github.com/crussella0129/cruor-framework/releases)
shows what has been published.

## What is in it

| where | what |
|---|---|
| `fonts/` | Cruor's web fonts, thirty-two `.woff2` files; `fonts/fonts.css`, which declares them; `fonts/OFL.txt`, their licence; `fonts/specimen.html`, a page that sets a line in every one |
| `examples/fetch-release.mjs` | a worked example of a build fetching a release and checking it |
| `src/` | the tool that writes the stylesheet, the manifest and a release |
| `tools/` | the checks |
| `docs/` | the project's record: what it is for, and how each part came to be |

## The fonts

Eight families, each in four styles: Regular, Bold, Italic and Bold Italic.

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

## Taking a release into a build

Each version of the framework is a release on GitHub, and a page takes the
framework in by fetching a release's files when it builds. A page that
builds this way keeps no font file in its own repository.

A release's files are one flat set of names, each at

```text
https://github.com/crussella0129/cruor-framework/releases/download/v<version>/<file>
```

A release holds the thirty-two fonts, `fonts.css`, `OFL.txt`, `LICENSE-MIT`
and `LICENSE-APACHE`; `manifest.json`, which gives the version and each of
those files' name, size and SHA-256; one archive of them all,
`cruor-framework-v<version>.zip`; and the archive's checksum beside it.

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
cargo run --release -- check
cargo run --release -- bundle --out dist
```

- `css` writes `fonts/fonts.css` from the list of families,
  `fonts/families.toml`.
- `manifest` writes `fonts/manifest.toml`: each font's size and SHA-256,
  and the commit of Cruor the fonts were built at.
- `check` fails if the stylesheet or the manifest is not current, or if a
  font has changed.
- `bundle` puts a release together in a folder, exactly as it would be
  published. The same commit gives the same bytes every time.

A release is published by `.github/workflows/release.yml` when a version tag
is pushed, and only for a tagged commit on `main`.

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

Copyright (c) 2026 Charles Russella.
