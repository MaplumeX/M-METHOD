# Building a token system

The implementation behind System mode: build a token set from zero, or complete a partial
one. **Only when the project has no system** — a project with one wins, per Step 0.

No coverage obligation (see `00-coverage.md`).

## 1 · Interview

Four rounds at most. Batch what can be asked together; every question is skippable. If the
user says "pick for me", skip to step 2 with the defaults below and say that defaults were
used.

| Round | Question | Default |
|---|---|---|
| 1 | What is the brand color? Is there a logo color? | A neutral blue — not default indigo |
| 2 | Should neutrals lean cool or warm? What should the product feel like? | Cool (blue-tinted) |
| 3 | Which semantic states are needed (success / warning / error / info)? | All four |
| 4 | Dark mode? | Not now, but structure the tokens for it |

**Don't ask what you can look up**: existing CSS variables, `tailwind.config.*`, a `theme/`
directory, the component library in `package.json`. Read all of it before asking.

## 2 · Color: nine steps from a base

Don't hand-pick hex values. Follow §5.3:

```
base (500) → edges (900 / 100) → midpoints (700 / 300) → the rest (800 / 600 / 400 / 200)
```

Rules at each step:

1. **Base 500**: the shade that works as a button background. There is no "start at 50%
   lightness" rule (§5.3.1).
2. **900** for the darkest text, **100** for tinted backgrounds. An alert component
   exercises both ends at once (§5.3.2).
3. **700 / 300**: each should feel like a perfect compromise between its neighbours
   (§5.3.3).
4. **Raise saturation as lightness moves away from 50%**, or both ends look washed out
   (§5.4).
5. For more brightness range, **rotate the hue**: toward 60°/180°/300° to lighten, toward
   0°/120°/240° to darken, never more than 20–30° (§5.4.2).
6. Greys follow the same procedure. **The darkest is not pure black; the lightest is not
   pure white** (§5.2.1). Cool greys get blue, warm greys get yellow/orange (§5.5.1).

Ramps needed: `neutral` (9) + `primary` (9) + one 5–9 step ramp per semantic state +
any categorical accents (§5.2.3).

## 3 · Type: a hand-crafted scale

```
12  14  16  18  20  24  30  36  48  60  72
```

Don't compute it from a modular ratio — you will want values between 12–16 and between
16–21 anyway, and end up hand-picking (§4.1.1c). Use px or rem, **never em** (§4.1.2).

## 4 · Spacing and sizing

```
4  8  12  16  24  32  48  64  96  128  192  256  384  512  640  768
```

Base 16px; no two adjacent values closer than about 25% (§3.2.1 §3.2.2).

## 5 · Radius, elevation, borders

| Category | Steps | Rule |
|---|---|---|
| Radius | 4 steps: sm 4 / md 6 / lg 8 / xl 12 (or 0) | Pick one set, use it everywhere, never mix (§1.4.3) |
| Elevation (shadow) | 5 steps | The five values in §6.2.1 |
| Border width | 1px / 2px | Two steps only; for more presence thicken rather than darken (§2.7.2) |

## 6 · Output contract

When starting from zero, produce these four — no more:

| File | Contents |
|---|---|
| `tokens.json` | Machine-readable single source: ramps, type scale, spacing, radius, shadows |
| `tokens.css` | CSS custom properties under `:root`, named `--color-<group>-<step>`, `--text-<name>`, `--space-<n>`, `--radius-<n>`, `--shadow-<n>` |
| `DESIGN.md` | One page for humans: ramps, type scale, spacing scale, what each step is for, what not to do |
| `preview.html` | One page rendering every token: swatches, type specimens, spacing bars, shadow cards. Change tokens here first to see the effect |

**Don't invent a build step.** If the project already has a theme mechanism (Tailwind
config, CSS-in-JS theme, Sass variables), convert `tokens.json` into it; if not, ship
`tokens.css` alone.

For a Tailwind expression see `12-tailwind.md` — an optional mapping, never a requirement.

## 7 · Check before delivering

- [ ] Every foreground/background pair passes: body 4.5:1, large 3:1
      (`python3 scripts/check_contrast.py`, or `--file pairs.txt`)
- [ ] Nine steps per ramp, with no "temporary tenth step" (§5.3.5)
- [ ] Greys are neither pure grey nor pure black/white (§5.2.1 §5.5)
- [ ] Type, spacing and radius values all sit on their scales, with no orphans
- [ ] Opening `preview.html`, no step is hard to justify

## 8 · Record the decision

A token set is a **durable decision**. Write a `proposed/design/` ADR per `adr-standard.md`:

- Why this base color and these scales; put the rejected options under
  `## Alternatives considered`.
- The dark-mode strategy.
- The naming scheme.

A single screen's styling is not a decision and does not get a record.
