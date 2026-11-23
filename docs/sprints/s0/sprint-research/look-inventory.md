# What the look is made of today

Read on 23 November 2026 from Tome, where the look was first made as a
theme. This is a record for the sprint that builds the look
([INT-0003](../../../intents/INT-0003-cruentous-atonement-look.md),
[INT-0004](../../../intents/INT-0004-the-look-as-a-theme-file.md)); Sprint 0
builds none of it.

## Colours by role

| role | value | where it is used |
|---|---|---|
| page | `#0a0708` | the obsidian ground |
| panel | `#110b0c` | lifted glass |
| input, sunken | `#170e0f` | inputs, panels set in, the ground of an inline code chip |
| interface text | `#cbb5ab` | bone: navigation, tables, code blocks, footnotes |
| subdued text | `#9d8a82` | weathered bone |
| border | `#5a1a1c` | clotted |
| border, subdued | `rgba(213, 2, 16, 0.2)` | |
| accent | `#ff3030` | arterial: focus, the current item |
| accent, subdued | `rgba(255, 48, 48, 0.15)` | the tint behind the current item |
| link | `#ff5c4d` | fresh blood, in interface text |
| inscription | `#d50210` | running text, at 24 pixels or more |
| inscription link | `#ff3b2f` | a link within running text |
| heading, top | `#ff2a1a` | light catching the top of a carved letter |
| heading, foot | `#ba1a1a` | pooled; the darkest stop of a carved letter |
| bone, bright | `#d9c1b8` | selected text |
| selection | `#7a2226` | the ground of selected text |
| vignette | `rgba(0, 0, 0, 0.72)` | darkness at the page's edges |
| chip, top to foot | `#ff9a8a` to `#ec5658` | inline code, a salmon gradient on `#170e0f` |

The void (a panel of pure black):

| role | value |
|---|---|
| ground | `#000000` |
| sunken | `#0c0505` |
| text | `#ec5658` |
| subdued text | `#bc6957` |
| accent | `#ff7466` |
| channel | `#d50210`, and at 22% as the tint of the current row (`#2f0004` on the void, `#380407` on sunken) |
| border | `#3a0a0b` |

The stone's bounds, which the contrast test needs: the surface's brightest
tone is `#3a2a2c` laid at 30% opacity, and the candle glow is `#ff3c28` at
3% at its strongest.

## Parts

| part | how it is made |
|---|---|
| the stone | one SVG filter in a data address: fractal noise lit as a specular surface, with a second noise for streaks of iron; tiled at 720 pixels |
| the candle | two radial gradients, the upper one flickering in steps over nine seconds |
| the inscription | crimson at `1.5rem` with a faint glow |
| carved headings | a gradient clipped to the letters, twice their height, slid into place over 1.9 seconds; a hairline stroke; a drop shadow that beats every 1.6 seconds on the first heading |
| the seal | the first letter of the paragraph after the first heading, floated, 3.4 times the size, in arterial red |
| the sigil | a rule broken at its middle by a mark (a circle, a triangle, a cross) drawn as an SVG mask |
| inscription quotes | a three-pixel channel of blood down the left edge, fading from arterial to dark, with one drop at its foot |
| code chips | a salmon gradient clipped to the letters over the chip's own ground, in two background layers, with solid salmon where clipped text is not supported |
| hairlines | one pixel of crimson fading out at both ends, a faint glow, and a dark scored line beneath |
| the briar | pixel art in an SVG data address, drawn crisp: a horizontal run of 32 by 12 squares for a masthead, growing in from the left, and a vertical run of 24 by 64 pixels for a panel's edge |
| stillness | every animation is off under `prefers-reduced-motion: reduce` |
| print | black on white, with no ornament |

## What is bound to Tome and must be loosed

- Every rule hangs from Tome's theme class and from Tome's own class names
  for its chapter text, masthead and library tiles. The framework's rules
  hang from the look's class and dress plain HTML.
- The colours are set on Tome's general theme tokens and on tokens named for
  the look's old name. The framework's tokens begin `--cruor-`.
- The void and its hairlines live in the stylesheet of Tome's sidebar
  component. In the framework they are classes any panel can take.
- The contrast contract is a TypeScript module in Tome. In the framework it
  is the theme file.
