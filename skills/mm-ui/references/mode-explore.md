# Explore Mode · Structural Multi-Direction Exploration

**Enter when**: the layout or interaction direction is still open, the user asks for options ("give me options", "explore directions", "给几个方案", "对比布局"), or a complex new surface has multiple viable architectures before committing to Build.

**Do not enter when**: the layout structure is already settled by an existing sibling view or explicit spec — go straight to `Build`.

## Read Gate (mandatory before proposing options)

- [`01-starting.md`](01-starting.md) — `§1.1` feature-first, `§1.2` low-fidelity exploration & disposable sketches (`§1.2.2`), `§1.3.2` smallest shippable version
- [`03-spacing.md`](03-spacing.md) — `§3.3` canvas bounds, `§3.4` sidebar vs fluid main, `§3.6` spatial grouping
- [`15-direction.md`](15-direction.md) — direction lock, aesthetic positioning, and absolute bans
- [`canvas-adapters.md`](canvas-adapters.md) — choosing ASCII wireframe vs disposable HTML prototype vs design-tool MCP canvas
- Project `DESIGN.md` (if present) — honor existing audience, voice, tokens, and Component Index

## Planning-period boundary

If invoked inside `mm-plan` (or before implementation authorization):

- **Write zero files**: present all three structural directions inline in the conversation using ASCII layout skeletons and concise specs.
- Wait for the user to pick or synthesize a direction before proceeding to `.plan.md` / `Build`.

## Divergence rules (no cosmetic clones)

Generate **3 structurally distinct directions** (2 if the surface is genuinely narrow and a 3rd would be contrived — state why).

Every direction **must differ across at least two** of these structural axes:

1. **Layout architecture**: e.g. fixed sidebar + bounded main vs single-column progressive flow vs split-pane master-detail vs dense multi-panel workbench.
2. **Primary interaction model**: e.g. inline editing vs slide-over drawer vs command-driven / keyboard-first vs step-by-step wizard.
3. **Information density tier**: `compact` (tool/analyst) vs `standard` (everyday SaaS) vs `spacious` (editorial/focused task).

**Strictly forbidden**: producing 3 "options" that share the same layout skeleton and only swap accent colors, fonts, or border radii.

## Required output per direction

Keep each option crisp, comparable, and grayscale/low-fidelity (`§1.2.1`):

1. **Name & 1-sentence structural thesis**: what makes this architecture distinct.
2. **Layout skeleton**: ASCII wireframe (or a disposable standalone HTML prototype / design-tool frame per `canvas-adapters.md`, when workspace writes are authorized).
3. **Primary flow & state handling**: how the user completes the core task, plus how `empty` and `overflow / long-content` behave in this layout.
4. **Density, width & key trade-offs**: explicit content `max-width` (`§3.3`), what this option optimizes for, and what it sacrifices.

## Upfront recommendation & exit

- **Lead with 1 clear recommendation**: state which option fits the user, context (`15-direction.md` #1), and product voice (`DESIGN.md`) best, and why.
- **Stop point**: ask the user to select Option A / B / C (or combine traits, e.g. "B's layout with A's inline editing").
- **Handoff**: once chosen, lock the direction and transition to **`Build`** mode (`mode-build.md`) — or **`System`** mode (`mode-system.md`) if base tokens do not exist yet. Disposable HTML exploration sketches may be discarded (`§1.2.2`) once promoted to production code.
