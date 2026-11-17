# Twelve laws and the hard gates

The highest-frequency rules across the book, plus the gates every delivery passes. Each law
expands in its chapter — **this file is a lookup, not a replacement**.

No coverage obligation (see `00-coverage.md`).

## The twelve laws

1. **Hierarchy is the job.** Make importance visible instead of adding decoration. A wall of
   equally weighted content reads as noise. `§2.1`
2. **Emphasize by de-emphasizing.** When the primary element will not stand out, soften its
   competitors rather than shouting louder. `§2.4`
3. **Every value comes from a system.** Sizes, spacing, colors, shadows, radii, border
   widths — all from a predefined scale, no hand-tuned one-offs. `§1.5 §3.2 §4.1`
4. **Start with too much white space, then remove.** Adding until it stops looking bad always
   undershoots. `§3.1`
5. **Space around a group must exceed space within it.** This one rule fixes most "why does
   this look confusing" complaints. `§3.6`
6. **Size is not the only lever.** Two weights (400/500, 600/700) and three text colors carry
   almost all hierarchy. Never go below 400 for UI text. `§2.2`
7. **Never put grey text on a colored background.** You want less contrast, not greyness —
   hand-pick a same-hue color, never white at lower opacity. `§2.3`
8. **Semantics are secondary to hierarchy.** One primary action per screen, a couple of
   secondary, a few tertiary. A destructive action is not automatically loud. `§2.8`
9. **Choose elements semantically, style them hierarchically.** An `h1` is a document
   decision, not a font-size decision; section titles usually behave as labels. `§2.6`
10. **Light comes from above.** Raised = lighter top edge plus a small, sharp shadow below;
    inset = shadow on top, lighter bottom edge. `§6.1`
11. **Text measures 45–75 characters.** Line-height rises with line width and falls as font
    size grows; large headlines can sit at 1. `§4.3 §4.5`
12. **Never rely on color alone.** Color supports a signal the design already carries another
    way. `§5.7`

## Hard gates

Pass these before any UI delivery:

- **No arbitrary values.** Every size, spacing and color is a token or a scale step. A
  missing step *is* the finding. `§1.5`
- **No unconstrained content width.** Even when a sidebar is fixed and the main area
  flexes (`§3.4.1`), primary content and prose must declare a `max-width` (`§3.3`,
  `§4.3`: 45–75 characters) unless explicitly justified (`§3.3.3`).
- **Static rules pass.** Run `scripts/check_ui_rules.py` (exit 0) to catch spacing/type
  off-scale values, loose heading line-height, `center`-aligned text rows (`§4.4`), flat
  inputs (`§6.1.3`), and banned motion properties (`15-direction.md`).
- **Colors are placeholders until confirmed.** Don't default to indigo and gray because an
  example used them — that is the most recognizable tell of machine-generated UI.
- **Contrast is measured, not eyeballed.** 4.5:1 / 3:1 via `scripts/check_contrast.py`, or
  say why it wasn't. `§5.6`
- **One primary action per screen.** `§2.8`
- **Anything that can be empty has an empty state.** `§8.4`
- **Visual claims require looking at contrasts.** Build requires `1440px` wide + `400px`
  narrow + empty-state screenshots (plus grayscale/sibling comparison); Refine requires
  before/after screenshots. Never declare quality from a single screenshot without a
  reference. If the page was not rendered, say the audit was static only.

## Leveling up (§9)

Two practices that are free and compound:

- **§9.1.1 Look for decisions you would not have made.** On a design you like, ask what the
  designer did that would never have occurred to you — an inverted datepicker background, a
  button inside a text input, two text colors in one headline.
- **§9.1.2 Rebuild interfaces you admire.** Recreate a design from scratch without opening
  devtools. The discrepancies teach the details: a tighter heading line-height, letter-spaced
  uppercase, layered shadows.

Everything else in this skill is lookup. Only these two compound.
