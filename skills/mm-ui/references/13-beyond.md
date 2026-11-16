# Beyond the book

The book is a 2018 visual-design text. These are the things real projects hit every day
that it does not cover. They are **extensions** — not sourced from the book, so they carry
no coverage obligation, though each points back to the relevant chapter.

No coverage obligation (see `00-coverage.md`).

## Dark mode

**Do not implement it with `filter: invert()` or reduced opacity.** That inverts photos,
icons and brand colors together and sends contrast out of control.

Instead: **swap semantic tokens; leave components alone.**

```css
:root {
  --surface: var(--neutral-100);
  --surface-raised: #fff;
  --text: var(--neutral-900);
  --text-muted: var(--neutral-600);
  --border: var(--neutral-200);
  --accent: var(--primary-600);
}
[data-theme="dark"] {
  --surface: var(--neutral-950);
  --surface-raised: var(--neutral-900);
  --text: var(--neutral-100);
  --text-muted: var(--neutral-400);
  --border: var(--neutral-800);
  --accent: var(--primary-400);
}
```

Three differences that matter:

1. **Never use pure black.** `#000` against light text is harsh for long reading and kills
   shadows entirely. Use a near-black neutral (say `neutral-950`).
2. **Shadows stop working on dark.** A darker shadow on a dark background is invisible;
   express elevation with a lighter surface plus a 1px border instead (§6.4.1).
3. **The contrast requirements do not change** — 4.5:1 body, 3:1 large — but they must be
   **re-measured**. A light color on a dark background is not the inverse of the reverse.

Primary colors usually need to move **one or two steps lighter** in dark mode
(`primary-600` → `primary-400`), or the color is not visible enough on a dark surface.

## Focus and keyboard

```css
:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
```

- Use `:focus-visible`, not `:focus` — a mouse click should not draw a ring; keyboard use
  must.
- **Never set `outline: none` globally.** To remove the default, replace it with the rule
  above.
- The ring must be visible on any background: dark ring on light surfaces, light ring on
  dark, or a double ring (outer color plus an inner offset in the background color).
- DOM order is visual order. Never reorder with CSS — a keyboard user loses the map.

## Target sizes

- **44×44 minimum on touch.** The visible control may be smaller; pad or extend the hit area
  with a pseudo-element.
- **32×32 minimum on desktop.** Small icon buttons inside table rows break this most often.
- Leave at least 8px between adjacent targets, or mis-taps follow. §3.6 applies here too.

## Motion

| Case | Duration | Easing |
|---|---|---|
| Button, toggle, hover | 150–200ms | `ease-out` |
| Dropdown, drawer, collapse | 200–300ms | `ease-out` in, `ease-in` out |
| Modal | 200–250ms | `ease-out`, no bounce |
| Page transition | 300–400ms | only when it means something |

- **Motion explains spatial relationships** — where something came from, where it returns.
  If it explains nothing, delete it.
- Travel only as far as necessary. An 8px fade-in distracts less than a 100px slide.
- Respect `prefers-reduced-motion: reduce`: remove translation and scaling, keep opacity
  changes.

## Breakpoints

**Content decides, not devices.** Four steps cover most projects:

```
400px   single column, mobile
768px   two columns start
1024px  sidebar appears
1280px  content reaches max width; beyond this, add space only
```

The method: narrow the window slowly; **the first width where it starts looking bad is the
breakpoint**. Not "an iPad is 768".

Once content hits its max width, stop widening it (§3.3); give the extra space to padding or
columns (§3.3.2).

## z-index

Never write `z-index: 9999`. Define six layers and use only those:

| Layer | Value | Use |
|---|---|---|
| base | 0 | normal content |
| sticky | 10 | sticky headers, sticky toolbars |
| dropdown | 20 | dropdowns, popovers, tooltips |
| overlay | 30 | scrims |
| modal | 40 | modals, drawers |
| toast | 50 | global notifications |

Needing a seventh usually means a structural problem — for example rendering a modal inside
a container with `transform`, which creates a new stacking context and breaks
`position: fixed`.

## Semantic token naming

Beyond `<group>-<step>`, add a semantic alias layer. It is the precondition for dark mode and
theming:

| Raw token | Semantic token | Use |
|---|---|---|
| `neutral-100` | `--surface` | page background |
| `#fff` | `--surface-raised` | cards, panels |
| `neutral-900` | `--text` | primary text |
| `neutral-600` | `--text-muted` | secondary text |
| `neutral-200` | `--border` | dividers |
| `primary-600` | `--accent` | primary actions |

Components use semantic tokens only. Changing one card's background means changing the
semantic layer, not hard-coding a ramp step inside a component.

## Form accessibility

- Every input has a `<label for>` or an `aria-label`. **A placeholder is not a label** — it
  disappears once you type.
- Errors use `aria-invalid="true"` plus `aria-describedby` pointing at the message; not a
  red border alone (§5.7).
- Error copy says **how to fix it**, not "invalid input".
- Required markers use words, not a lone red asterisk.
- Group related fields with `<fieldset>` and `<legend>`; the legend can be visually small.

## Loading states

- Under 300ms, show nothing — a flickering spinner is worse than no spinner.
- 300ms–1s: a skeleton or an inline spinner.
- Over 1s: a skeleton whose shape matches the real content, not a row of equal grey bars.
- Over 10s: progress plus the ability to cancel.
- **Skeleton dimensions must match the loaded content**, or the layout jumps when data
  arrives, which is more unsettling than waiting.

## Long text and truncation

- Single-line truncation (`text-overflow: ellipsis`) only where there is **definitely one
  line of space**.
- Multi-line uses `line-clamp` with an explicit line count — two lines and three lines have
  different visual rhythm (§4.5).
- **Truncation must offer a way to see the whole thing**: hover tooltip, detail view, or
  expand. Truncating with no path to the content is deleting it.
- For CJK text, the same `line-height` reads tighter than it does for Latin text, because
  glyphs fill more of the em box. Judge vertical rhythm on the actual language, not on a
  Latin specimen.
