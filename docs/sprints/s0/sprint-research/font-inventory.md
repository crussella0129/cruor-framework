# Cruor's built web fonts, as read on 23 November 2026

Read from the Cruor project's build output with fontTools. Nothing here was
copied into this repository; taking the fonts in is Build work.

Every file is WOFF2. The four styles of a family share one family name, and
the bold styles carry weight 700, so the four join under one `font-family`.

| family (the font's own name) | file stem | glyphs | fixed pitch | Regular | Bold | Italic | Bold Italic |
|---|---|---|---|---|---|---|---|
| Cruor Sans Regular | `CruorSansRegular` | 328 | no | 19,304 | 20,704 | 20,972 | 22,312 |
| Cruor Lite Regular | `CruorLiteRegular` | 328 | no | 22,480 | 25,792 | 24,240 | 27,300 |
| Cruor Thornamental Regular | `CruorThornamentalRegular` | 328 | no | 26,176 | 31,216 | 28,456 | 33,304 |
| Cruor Sans Mono | `CruorSansMono` | 779 | yes | 24,028 | 25,372 | 25,552 | 26,972 |
| Cruor Lite Mono | `CruorLiteMono` | 779 | yes | 26,824 | 30,268 | 28,832 | 31,776 |
| Cruor Thornamental Mono | `CruorThornamentalMono` | 779 | yes | 30,888 | 35,188 | 33,212 | 37,528 |
| Cruor Sans Pixelated | `CruorSansPixelated` | 779 | yes | 12,832 | 12,896 | 13,480 | 13,408 |
| Cruor Pixelated | `CruorPixelated` | 779 | yes | 14,120 | 13,896 | 14,700 | 14,296 |

Sizes are in bytes. The thirty-two files come to 768,324 bytes.

File names are the stem, a hyphen and the style: `-Regular`, `-Bold`,
`-Italic`, `-BoldItalic`, then `.woff2`.

## What the fonts say of themselves

- Family name (name ID 1) as in the table; style name (ID 2) one of
  `Regular`, `Bold`, `Italic`, `Bold Italic`.
- Version (ID 5): `Version 0.001`.
- Weight class: 400 for Regular and Italic, 700 for Bold and Bold Italic.
- No copyright (ID 0), licence (ID 13) or licence address (ID 14) is set.
- The embedding field (`OS/2.fsType`) is 4, "preview and print". Fonts
  offered under an open licence usually set 0, "installable". Browsers load
  a web font whatever this field says.

Both of the last two are set where the fonts are built. They are noted here
for the Cruor project; this repository states the fonts' terms in the
licence file beside them.

## What a proportional font covers

Cruor Lite Regular maps U+0020 to U+007E, U+00A0 to U+017F, U+2013, U+2014,
U+2018, U+2019, U+201C, U+201D, U+2022 and U+2026: Basic Latin, Latin-1
Supplement, Latin Extended-A and ten of punctuation. The Mono and Pixelated
families add box drawing, block elements, Braille, four Powerline
separators, arrows and shapes.
