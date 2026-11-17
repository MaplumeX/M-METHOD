# Building a token system

The implementation behind System mode: build a complete, component-ready token set from
zero, or complete a partial one. **Only when the project has no system** — a project with
one wins, per Step 0.

No coverage obligation (see `00-coverage.md`).

## 1 · Interview

Four rounds at most. Batch what can be asked together; every question is skippable. If the
user says "pick for me", skip to step 2 with the defaults below and say that defaults were
used.

| Round | Question | Default |
|---|---|---|
| 1 | Brand / logo color? Neutral temperature (cool or warm)? Which semantic states are needed (`success / warning / error / info`)? | Neutral blue (not default indigo), cool greys, all four semantic states |
| 2 | Product personality and typography? (neutral sans / serif / rounded sans; CJK pairing; monospace needs?) | Neutral sans (`§4.2.1` system stack) + system monospace |
| 3 | Shape and surface-depth philosophy? (sharp `0` / restrained `4–6px` / playful `8–12px` radius; flat borders vs background steps vs shadows?) | `6px` controls / `8px` containers; background steps + `1px` borders + light shadows |
| 4 | Dark mode and UI density? (ship dark mode now or later; compact tool vs standard vs touch-first?) | Structure semantic tokens for dark mode now (single theme unless asked); standard density (`32–40px` desktop, `44px` touch) |

**Don't ask what you can look up**: existing CSS variables, `tailwind.config.*`, a `theme/`
directory, the component library in `package.json`. Read all of it before asking.

## 2 · Color: nine steps from a base

Don't hand-pick hex values. Follow §5.3 (use `scripts/generate_ramp.py --name <group> --base <color>` or `--neutral cool|warm` to derive all nine steps programmatically):

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

## 3 · Typography: family, scale, weight, and line height

Size scale (§4.1.1d):

```
12  14  16  18  20  24  30  36  48  60  72
```

Don't compute it from a modular ratio — you will want values between 12–16 and between
16–21 anyway, and end up hand-picking (§4.1.1c). Use px or rem, **never em** (§4.1.2).

Complete the type system with these companion tokens (§1.5.3 §2.2.b §4.2 §4.3 §4.5):

- **Font families**: `--font-sans`, `--font-mono` (add `--font-serif` or `--font-display`
  only if part of the chosen personality). Use the system stack (`§4.2.1`) when no custom
  font is justified; body faces must carry at least 5 weights and generous x-height
  (`§4.2.2 §4.2.3`).
- **Weights**: two primary weights carry most hierarchy (`§2.2.b`) — `--weight-normal`
  (`400` or `500`), optional `--weight-medium` (`500` for UI labels), `--weight-strong`
  (`600` or `700`). Never go below `400` for UI text.
- **Line heights & measure**: pair with size and line width (`§4.5`) — `--leading-tight`
  (`1.15–1.25` headings), `--leading-snug` (`1.35` compact UI), `--leading-normal` (`1.5`),
  `--leading-relaxed` (`1.625–1.75` wide prose or CJK body, per `13-beyond.md`), plus
  `--measure-prose: 65ch` (`45–75ch`, `§4.3`).

## 4 · Spacing, sizing, and control heights

```
4  8  12  16  24  32  48  64  96  128  192  256  384  512  640  768
```

Base 16px; no two adjacent values closer than about 25% (§3.2.1 §3.2.2).

Add **control height tokens** so buttons, inputs, and list items stay aligned without
inventing one-off padding (`13-beyond.md`):

- `--control-sm: 32px` (minimum desktop interactive target)
- `--control-md: 36px` (or `40px`, default form/button height)
- `--control-lg: 44px` (minimum touch target)

## 5 · Radius, elevation, borders, and infrastructure

| Category | Steps | Rule |
|---|---|---|
| Radius | 4 steps: sm 4 / md 6 / lg 8 / xl 12 (or `0`) | Pick at most two active steps (e.g. control + container), never mix square and round (§1.4.3) |
| Elevation (shadow) | 5 steps | The five values in §6.2.1; assign each to a role (§6.2.a) |
| Border width | 1px / 2px | Two steps only; for more presence thicken rather than darken (§2.7.2) |
| Focus ring | 2px width, 2px offset | `:focus-visible` only; never `outline: none` globally (`13-beyond.md`) |
| z-index | 6 layers: `0 / 10 / 20 / 30 / 40 / 50` | `base / sticky / dropdown / overlay / modal / toast` (`13-beyond.md`) |
| Motion | `150ms / 220ms / 300ms` + `ease-out` / `ease-in` | `transform` and `opacity` only; respect `prefers-reduced-motion` (`13-beyond.md`) |
| Breakpoints | `400px / 768px / 1024px / 1280px` | Content-driven defaults (`13-beyond.md`) |

## 6 · Semantic alias layer and dark mode

Raw ramp tokens live under `:root`, **but components consume semantic tokens only**
(`13-beyond.md`). Define the alias layer as part of the token system:

| Semantic group | Required tokens | Typical light mapping |
|---|---|---|
| Surfaces | `--surface`, `--surface-raised`, `--surface-sunken` | `neutral-100`, `#fff` / `neutral-50`, `neutral-200` |
| Text (`§2.2.a`) | `--text`, `--text-secondary`, `--text-muted` | `neutral-900`, `neutral-700`, `neutral-500` |
| Borders | `--border`, `--border-strong` | `neutral-200`, `neutral-300` |
| Accent | `--accent`, `--accent-hover`, `--accent-subtle`, `--accent-fg` | `primary-600`, `primary-700`, `primary-100`, `#fff` |
| Status (per enabled state) | `--status-<state>-bg`, `--status-<state>-border`, `--status-<state>-fg` | `100`, `500`, `800`/`900` |
| Interactive states | `--focus-ring`, `--disabled-bg`, `--disabled-fg` | `primary-600`, `neutral-100`, `neutral-400` |

When dark mode is enabled (under `[data-theme="dark"]` or the project's theme selector):

1. Swap only the semantic tokens — never rewrite components (`13-beyond.md`).
2. Never use `#000`; use a near-black neutral (`neutral-950` / `neutral-900`).
3. Shift accent tokens 1–2 steps lighter (`primary-600` → `primary-400`) and replace dark
   shadows with a lighter raised surface plus a `1px` border (`§6.4.1`).
4. **Re-measure every foreground/background pair** in dark mode with `check_contrast.py`.

## 7 · Output contract

When starting from zero, produce these four — no more:

| File | Contents |
|---|---|
| `tokens.json` | Machine-readable single source: raw ramps, semantic aliases (light + dark if enabled), typography (families, size scale, weights, line heights), spacing & control heights, radius, shadows, border widths, z-index, motion, breakpoints |
| `tokens.css` | CSS custom properties under `:root` (raw + semantic) and `[data-theme="dark"]` (if enabled): `--color-<group>-<step>`, semantic aliases (`--surface*`, `--text*`, `--border*`, `--accent*`, `--status-*`, `--disabled-*`), `--font-*`, `--text-*`, `--weight-*`, `--leading-*`, `--space-*`, `--control-*`, `--radius-*`, `--shadow-*`, `--border-width-*`, `--z-*`, `--duration-*`, `--ease-*` |
| `DESIGN.md` | One page for humans: ramps, semantic mapping, typography (with CJK rhythm if applicable), spacing & control heights, **cross-component conventions** (active radii, card elevation rule, input depth treatment, 3-tier button hierarchy, focus/disabled rules), breakpoints, what each step is for, what not to do |
| `preview.html` | One page rendering every token (swatches, type specimens, spacing bars, shadow cards) **plus 4 canary component specimens** — Button (primary/secondary/tertiary/disabled/focus), Form Input (label/normal/focus/error), Card, and Alert — with a theme toggle if dark mode is structured |

**Don't invent a build step.** If the project already has a theme mechanism (Tailwind
config, CSS-in-JS theme, Sass variables, or a component library's CSS variables such as
shadcn/ui), map `tokens.json` into it; if not, ship `tokens.css` alone. Never pre-build a
full business component library in System mode — full components belong in Build using
`10-recipes.md`.

For a Tailwind expression see `12-tailwind.md` — an optional mapping, never a requirement.

## 8 · Check before delivering

- [ ] Every foreground/background pair passes in light mode **and dark mode (if enabled)**:
      body 4.5:1, large 3:1 (`python3 scripts/check_contrast.py`, or `--file pairs.txt`)
- [ ] Nine steps per ramp, generated via §5.3 (`scripts/generate_ramp.py`) and verified
      with `scripts/check_ui_rules.py --tokens`, with no "temporary tenth step" (§5.3.5)
- [ ] Greys are neither pure grey nor pure black/white (§5.2.1 §5.5); dark surface is not `#000`
- [ ] Typography (family, size, weight `>=400`, line height), spacing, control heights,
      radius, elevation, border widths, z-index, and motion all sit on their scales with no
      orphans
- [ ] Semantic alias layer covers surfaces, three text levels, borders, accent, and enabled
      states; `preview.html` specimens consume semantic tokens only
- [ ] Opening `preview.html`, no step is hard to justify and the 4 canary specimens read
      coherently

## 9 · Record the decision

A token set is a **durable decision**. Write a `proposed/design/` ADR per `adr-standard.md`:

- Why this base color, typography/personality, radius/depth philosophy, and scales; put the
  rejected options under `## Alternatives considered`.
- The semantic alias & dark-mode strategy.
- The naming scheme and cross-component conventions (or mapping to an existing component
  library).

If invoked during `mm-plan` before the user approves the plan, keep these decisions and
the planned file targets in the presented proposal and write the ADR, `.plan.md`, and
token/preview files only after the user confirms (per `mm-plan` and `mm-ui` `SKILL.md`).

A single screen's styling is not a decision and does not get a record.
