# System Mode · Building or Updating a Design System

**Enter when**: the project has no design system, is replacing a legacy one, or is missing core scales.

## Read Gate (before designing or writing)

Read before starting:

- [`11-tokens.md`](11-tokens.md) — full token architecture and output contract
- [`05-color.md`](05-color.md) — HSL reasoning, 9-step shade derivation, saturation/hue rules, contrast
- [`12-tailwind.md`](12-tailwind.md) — only if the project uses Tailwind

## Planning-period read-only boundary

If invoked from `mm-plan` (or before user confirmation/authorization):

- **Write zero files**: do not create `tokens.json`, `tokens.css`, `DESIGN.md`, `preview.html`, ADR files, or `.plan.md`.
- Run `scripts/check_contrast.py` directly with inline `"fg:bg"` pairs (no temporary清单 files).
- Return the design-system draft (ramps, typography/spacing/radius/elevation scales, semantic mapping, contrast results, and planned target paths) to `mm-plan` for user approval.

## Workflow

1. **Interview (up to 4 rounds, batch questions; defaults allowed)**:
   - Brand hue, neutral temperature (cool/warm), semantic states (`success / warning / error / info`);
   - Product personality & typography (neutral sans / serif / rounded sans; CJK pairing; monospace needs);
   - Shape & depth philosophy (sharp `0` vs restrained `4–6px` vs playful `8–12px` radius; flat borders vs background steps vs shadows);
   - Dark mode & UI density (compact tool vs standard vs touch-first).
2. **Generate 9-step color ramps & base scales**:
   - **Never hand-pick hexes to chase contrast.** Derive every 9-step ramp programmatically via `scripts/generate_ramp.py` (`500` base → `900 / 100` edges → `700 / 300` midpoints → `800 / 600 / 400 / 200` fill), raising saturation away from 50% lightness (`§5.3–§5.5`).
   - Define full typography (font stacks, 11-step size scale, primary/secondary weights `>= 400`, companion line heights & prose measure), spacing & control heights (`32 / 36 / 44px`), active radii, 5 elevation shadows, border widths (`1px / 2px`), focus ring, `z-index`, motion, and breakpoints.
3. **Build semantic alias layer & dark mode mapping**:
   - Define `--surface*`, `--text*`, `--border*`, `--accent*`, `--status-*`, `--disabled-*` over raw scales; components consume semantic tokens only.
   - If dark mode is enabled, swap semantic mappings only (never `#000`, step accents lighter, replace dark shadows with a lighter surface + `1px` border).
4. **Run automated gates**:
   - `scripts/check_contrast.py`: verify all foreground/background pairs in light and dark mode (`>= 4.5:1` body, `>= 3:1` large).
   - `scripts/check_ui_rules.py --tokens <tokens.css|tokens.json>`: verify 9 steps per ramp (`100..900`), monotonic lightness, no `#000`/`#fff`, non-achromatic neutrals, and edge saturation (`§5.2.1`, `§5.3–§5.5`).
5. **Write the 4 contract files (only after implementation authorization)**:
   - `tokens.json`, `tokens.css`, `DESIGN.md` (with cross-component conventions), and `preview.html` (all tokens + **4 canary specimens**: Button, Form Input, Card, Alert).
   - Follow existing project theme/style directory conventions, or confirm the default directory with the user. Do not pre-build full business component libraries here (those belong in Build per `10-recipes.md`).
6. **Record ADR**:
   - If `.agents/ADR/` exists (if missing during `mm-plan`, hand back to `mm-plan` to ask about `mm-setup`; never create half-initialized ADR dirs):
     - From `mm-plan` after user confirmation: write `proposed/design/` ADR and `.plan.md` only; implement the 4 files separately and promote via `mm-land`.
     - Direct authorized implementation: write `proposed/design/` ADR alongside the 4 files, and remind the user to promote to `implemented/design/` via `mm-land` after verifying `preview.html`.

## Stop points

Confirm before locking or writing: palette direction, typography/radius/depth philosophy, token & semantic naming, and any disk write (ADR / `.plan.md` / token files).

## Completion criteria

- **Planning (pre-confirmation)**: design-system draft & verification checklist returned to `mm-plan` with zero workspace writes.
- **Planning (post-confirmation)**: `proposed/design/` ADR and `.plan.md` written.
- **Authorized implementation**:
  1. `scripts/check_contrast.py` exits `0` for all light/dark pairs;
  2. `scripts/check_ui_rules.py --tokens` (on `tokens.*`) and `scripts/check_ui_rules.py` (on `preview.html`) exit `0`;
  3. All 4 canary specimens in `preview.html` rendered and checked in enabled themes (or unverified items explicitly listed per Visual Evidence);
  4. `proposed/design/` ADR written and `mm-land` promotion noted.
