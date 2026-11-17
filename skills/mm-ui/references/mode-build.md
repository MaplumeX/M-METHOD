# Build Mode · Creating New UI

**Enter when**: creating a new page, component, or feature surface.

If the work needs architectural or multi-page planning, `mm-plan` owns IA and step order; Build owns visual direction and execution.

## Read Gate (mandatory before writing the brief or code)

Read **all 8** of these files before drafting your Constraint Brief (do not defer `08` or `09` until the end):

- [`02-hierarchy.md`](02-hierarchy.md) — ranking content and actions, weight/color over size alone
- [`03-spacing.md`](03-spacing.md) — spacing scale, `§3.3` content width caps, `§3.6` group vs inner spacing
- [`04-typography.md`](04-typography.md) — type scale, `§4.3` 45–75ch measure, `§4.4` baseline alignment, `§4.5` proportional leading
- [`06-depth.md`](06-depth.md) — light from above, `§6.1.3` inset inputs, 5-step elevation
- [`08-finishing.md`](08-finishing.md) — `§8.4` empty-state design (mark/illustration + title + copy + CTA + hide inert UI) and `§8.5` fewer borders
- [`09-antipatterns.md`](09-antipatterns.md) — symptom → `§id` → fix negative-audit checklist
- [`10-recipes.md`](10-recipes.md) — canonical component recipes (button, form group, card, empty state, table, dropdown, modal, alert)
- [`15-direction.md`](15-direction.md) — direction lock, absolute bans, and the 5-item AI Slop Test
- Also read [`07-images.md`](07-images.md) when working with photos, avatars, or non-trivial graphics.

## Planning-period boundary

If currently in `mm-plan` without implementation authorization:

- Return direction recommendations (explicitly including main content `max-width` and density tier) and step breakdown to `mm-plan`.
- Write **zero** markup, CSS, or constraint brief comments before user confirmation.

## Execution order

**The order is the method.** Collapsing steps produces noisy, unconstrained layouts.

0. **Lock the direction** (`15-direction.md`). Name a specific aesthetic and one signature trait ("clean and modern" is rejected). State the 3-line direction (`Visual thesis`, `Content plan`, `Interaction thesis`) before writing markup.
1. Start with a concrete feature, not the shell (`§1.1`).
2. Work in grayscale first so spacing, size, and contrast carry hierarchy alone (`§1.2.1`).
3. Rank content (primary / secondary / tertiary) and actions (1 primary / few secondary / several tertiary) (`§2.1`, `§2.8`).
4. Pull spacing and type sizes strictly from the system scales (`§3.2`, `§4.1`).
5. Constrain canvas width, line length (`45–75ch`), and proportional line-height (`§3.3`, `§4.3`, `§4.5`).
6. Add color, then depth, then finishing touches — strictly in that order (`§5`, `§6`, `§8`).
7. Design the empty state together with the primary feature (`§8.4`).

## Two-pass write discipline (per new surface / step; no collapse)

Even when design-system tokens already exist, run Pass 1 → Pass 2 independently **for each new surface or step** (passing Pass 1 on an earlier main view does not exempt a later sidebar, drawer, or modal step):

- **Pass 1 (Skeleton + Grayscale + Empty State Structure + Geometric Rhythm)**:
  - Use neutral grayscale tokens only (`--surface*`, `--text*`, `--border*`).
  - Establish container `max-width`, type scale, proportional `line-height`, `45–75ch` measure, group vs inner spacing, and `baseline` row alignment.
  - Build the **`§8.4` empty state skeleton together with the primary feature** (low-contrast mark/illustration + title + 1-line explanation + single CTA, hiding tabs/filters/metrics that do nothing yet — never a bare `text-sm` placeholder).
  - **Forbidden in Pass 1**: `--accent*`, `--status-*`, chromatic classes (`bg-indigo-*`, `bg-blue-*`), and decorative non-inset `box-shadow`.
  - Run `scripts/check_ui_rules.py <target> --pass1` (supports `.css/.scss/.less/.tsx/.jsx/.html/.vue/.svelte`; refuses 0-file scans and must exit `0`), and confirm hierarchy holds in grayscale (`§1.2.1`).
- **Pass 2 (Color + Depth + Finishing)**:
  - Layer semantic accent/status colors (`§5`), inset input depth and z-axis elevation (`§6`), and finishing details (`§8`).

## Required 9-key Direction & Constraint Brief

Before writing the first line of markup, place this structured comment block at the top of the target style/component file (validated by `check_ui_rules.py --brief`):

```text
Visual thesis: <mood, material, and energy in one sentence>
Content plan: <sequence of sections/states on this surface>
Interaction thesis: <key micro-interactions, or "none" + evidence-based reason>
Rules read: <list 02-hierarchy, 03-spacing, 04-typography, 06-depth, 08-finishing, 09-antipatterns, 10-recipes, 15-direction with extracted §id & values>
Canvas & measure: <explicit width/measure for EVERY region (e.g. sidebar 360px, main max-w-768px, prose 65ch, or §3.3.3 full-bleed reason)>
Type & leading: <per-level font sizes & paired line-heights; never a single 1.5 everywhere>
Density & spacing: <density tier + explicit inner-group vs between-group spacing values>
Alignment & depth: <baseline on mixed text rows + explicit icon-control center exceptions + input/surface depth (border/inset/shadow)>
Hierarchy & empty state: <content ranks, single primary action, §8.4 empty-state mark/copy/CTA & hidden inert controls>
```

## Stop points

- Visual direction (not micro-tweaks)
- Missing base scales/tokens (return to System mode)

## Completion criteria (all 5 required; no subjective adjectives)

1. **Read Gate & Brief**: all 8 required files read and the 9-key brief comment is complete.
2. **Automated Gates**: `scripts/check_ui_rules.py <target> --brief <brief-file>` (plus `scripts/check_contrast.py` if colors were added/changed) exits `0`.
3. **Comparison Screenshots & Negative Audit**:
   - Capture **`1440px` wide + `400px` narrow + empty state** screenshots (plus Pass 1 grayscale or sibling/`preview.html` comparison).
   - Audit against [`09-antipatterns.md`](09-antipatterns.md) by falsification (`§3.3` full-width sprawl? `§4.3` >75ch lines? `§3.6` ambiguous gaps? `§4.4` centered mixed rows? `§6.1.3` flat sticker inputs? `§8.4` bare corner empty state?).
   - If rendering is impossible in the environment, declare so and list every **unverified visual item** explicitly.
4. **Rule Traceability**: delivery report maps each component/change to concrete `§id` rules (keep `§id` logs in the report, not cluttering business code).
5. **AI Slop Test**: report evaluates all **5** reflex patterns from [`15-direction.md`](15-direction.md) one by one as `Clear` or `Hit -> fixed (reason)` (verifiable with `scripts/check_ui_rules.py --report <report-file>`).
