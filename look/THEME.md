# The form of a theme file

`theme.toml` is Cruentous Atonement written down once, by role. The
framework's tokens, `tokens.css`, are made from it by the tool:

```sh
cargo run --release -- look
cargo run --release -- look --check
```

`look --check` changes nothing. It fails if the file is not as this page
describes, and it names the key at fault as it is written here, table and
all: `colour.inscription`, `heading.h2.font`. It fails too if the file's
colours do not keep the contrast the file promises, and then it names the
text, the ground and the ratio found. `look` writes nothing when either is
so.

The form is strict. A key it requires must be there, and a key it does not
have must not be, so that a slip in a name is told and not passed over. To
write another look, copy the file and change its values; the keys stay.

## At the top

| key | what it is |
|---|---|
| `name` | the look's name, as it is said |
| `class` | the class a page sets on `<body>` to take the look on: small letters, digits and hyphens |

## `[font]`

The families, by what they set. Each must be a family the kit holds, named
as `fonts/families.toml` names it.

| key | what it sets |
|---|---|
| `title` | the title of a page |
| `heading` | the headings beneath it |
| `text` | running text |
| `code` | code, in a fixed pitch |

## `[colour]`

The colours, by role. A colour is written `#rrggbb`, or
`rgba(r, g, b, a)` where it lets what lies beneath it show through.

| key | what it colours |
|---|---|
| `page` | the ground of the page |
| `panel` | a ground lifted above the page |
| `sunken` | a ground set into it: a field, the ground of inline code |
| `text` | interface text: tables, code blocks, the lettering of a part |
| `text-subdued` | interface text of less weight |
| `text-bright` | selected text |
| `border` | a rule or an edge |
| `border-subdued` | a fainter one |
| `accent` | what marks where the keyboard is, and the current item |
| `accent-subdued` | the tint behind the current item |
| `link` | a link in interface text |
| `inscription` | running text, which is never set smaller than 24 pixels |
| `inscription-link` | a link within running text |
| `heading-top` | a carved heading, where light catches the top of a letter |
| `heading-foot` | a carved heading, at the foot of a letter |
| `selection` | the ground of selected text |
| `chip-top` | inline code, at the top of its letters |
| `chip-foot` | inline code, at their foot |
| `blood` | what fills a part that fills: a bar of progress, a slider's run. It is never the colour of lettering nor a ground for it |
| `blood-edge` | the edge such a fill carries, so that it is seen against the page |
| `shadow` | the hard shadow of a plate |
| `vignette` | the dark at the page's edges |

## `[void]`

The void is a panel of pure black beside the page, with colours of its own.

| key | what it colours |
|---|---|
| `ground` | the void itself |
| `sunken` | a ground set into it |
| `row` | the tint laid over the row of the current item |
| `text` | its lettering |
| `text-subdued` | lettering of less weight. It is not set on the tinted row |
| `accent` | the current item, and where the keyboard is |
| `channel` | its structure: the mark beside the current item, its hairlines |
| `border` | a rule or an edge |

## `[stone]`

The stone's surface is drawn in the stylesheet. These keys say how bright
it may be.

| key | what it is |
|---|---|
| `sheen` | the surface's brightest tone |
| `sheen-opacity` | how strongly the surface is laid over the page, from 0 to 1 |
| `candle` | the colour of the glow from above |
| `candle-opacity` | the glow's strength at its strongest, from 0 to 1 |

## `[measure]`

A length is a number and `rem`, `em` or `px`.

| key | what it measures |
|---|---|
| `inscription-size` | the size of running text |
| `interface-size` | the size of small things: tables, code blocks, parts |
| `line` | the height of a line of running text, as a multiple of its size |
| `column` | the widest a column of running text is set |
| `seal-size` | the large first letter, as a multiple of the text's size |
| `seal-font` | the font of that letter: one of the four roles of `[font]`, or a family the kit holds, by name |

## `[heading.h1]` to `[heading.h6]`

One table for each level of heading, each with the same five keys.

| key | what it sets |
|---|---|
| `font` | one of the four roles of `[font]`, or a family the kit holds, by name |
| `bold` | `true` or `false` |
| `italic` | `true` or `false` |
| `underline` | `true` or `false` |
| `size` | a length |

## `[[contrast]]`

The contract: which text may sit on which ground, and at what ratio at
least. There is one entry for each bound, and as many entries as the look
needs. Every pair an entry makes, of one of its texts with one of its
grounds, is measured as WCAG 2 measures contrast and compared with the
bound without rounding.

| key | what it is |
|---|---|
| `text` | a list of text roles: a key of `[colour]`, or `void.` and a key of `[void]` |
| `grounds` | a list of grounds: a key of `[colour]`; `stone`; `void.ground` or `void.sunken`; `void.row` or `void.sunken-row` |
| `at-least` | the ratio each of those texts must reach on each of those grounds |

`stone` is the page at its brightest: the stone's `sheen` laid over `page`
at `sheen-opacity`, and then `candle` laid over that at `candle-opacity`.
`void.row` and `void.sunken-row` are the tint `row` laid over the void's
`ground` and over its `sunken`. A colour that lets what lies beneath it
show through is laid over its ground before it is measured.

The look's stylesheets may set lettering on a ground only where an entry
covers the pair, and a test of the repository holds them to it. So a new
pairing begins here, with an entry, and is refused if its colours cannot be
read.

