# Sync Mode · Codebase ↔ Design Context (`DESIGN.md`) Sync

**Enter when**:
- **Inbound (`code → design`)**: the repository already has tokens, Tailwind config, or UI components (`src/components/`, shadcn/ui, MUI, etc.) and needs a structured `DESIGN.md` Component Index & State Matrix (or `DESIGN.md` has drifted behind code).
- **Outbound (`design → code`)**: `DESIGN.md`, `tokens.*`, or an approved design canvas/prototype changed and existing components need to be updated in code.

## Read Gate (mandatory before scanning or editing)

- [`11-tokens.md`](11-tokens.md) — token architecture and `DESIGN.md` output contract (including Component Index & State Matrix)
- [`13-beyond.md`](13-beyond.md) — semantic alias layer, dark mode, focus, target sizes, loading & truncation
- [`canvas-adapters.md`](canvas-adapters.md) — if syncing with an active design-tool MCP canvas
- Project `DESIGN.md` and `tokens.*` (if present)

## Planning-period read-only boundary

If invoked inside `mm-plan` (or before user confirmation/authorization):

- **Write zero files**: perform the read-only codebase/token scan and return the discovered Component Index or the proposed outbound impact diff to `mm-plan`.

## Inbound Sync (`code → design`)

Use this when onboarding an existing codebase into `mm-ui` (often right after `Step 0`) or refreshing a stale `DESIGN.md`:

1. **Inventory tokens**: locate CSS custom properties, `tokens.json` / `tokens.css`, Tailwind theme extensions, or CSS-in-JS theme objects. Map raw scales to semantic roles (`--surface*`, `--text*`, `--border*`, `--accent*`, `--status-*`).
2. **Inventory existing UI components**: inspect shared component directories and record each reusable primitive/composite into the **Component Index & State Matrix** in `DESIGN.md`:

| Component | Source path | Variants / sizes | States supported | Token bindings | Gaps / debt |
|---|---|---|---|---|---|
| `Button` | `src/components/ui/button.tsx` | `primary / secondary / ghost`; `sm / md / lg` | `default, hover, focus-visible, disabled, loading` | `--accent`, `--border` | Missing `sm` 32px desktop min-height check |

3. **Flag drift & missing states (do not silently rewrite code)**:
   - Run `scripts/check_ui_rules.py <ui-dir>` (and `--tokens` if `tokens.*` exists) to surface off-scale values, flat inputs (`§6.1.3`), or contrast gaps.
   - Record missing component states (`disabled`, `loading`, `error`, `empty`, `:focus-visible`) in the **Gaps / debt** column rather than silently inventing new components.
4. **Update `DESIGN.md`** (after authorization): write or refresh the Token Inventory and Component Index & State Matrix sections while preserving existing **Product & Brand Context** (audience, voice & tone, aesthetic thesis).
5. **Prevent duplicate building**: once indexed, `Build` mode must reuse or extend indexed components before creating new ones.

## Outbound Sync (`design → code`)

Use this when `DESIGN.md`, `tokens.*`, or an approved design-tool/prototype spec changed and code must catch up:

1. **Compute the delta**: compare updated tokens, semantic mappings, conventions, or component state specs against the Component Index and actual component files.
2. **Present a reviewable impact plan first (Stop point)**:
   - List affected token files and components;
   - Call out breaking token renames, contrast shifts (especially dark mode), or missing states that need new props/markup;
   - Wait for confirmation if the sync touches multiple shared components or changes public component APIs.
3. **Apply changes incrementally**:
   - Update `tokens.json` / `tokens.css` (or Tailwind/theme config) first;
   - Update affected components, keeping one diagnostic lens clean at a time;
   - Sync any design-tool MCP frame changes only if an active MCP canvas is configured (`canvas-adapters.md`).
4. **Verify & update index**:
   - Run `scripts/check_ui_rules.py <target>` (plus `--tokens` if `tokens.*` changed) and `scripts/check_contrast.py`;
   - Update the Component Index & State Matrix in `DESIGN.md` so code and documentation stay aligned.

## Completion criteria

- **Inbound**: `DESIGN.md` (or in-plan draft) contains an accurate Token Mapping + Component Index & State Matrix citing real paths, supported states, and observed static/contrast gaps.
- **Outbound**: impacted components updated via a reviewed diff, `check_ui_rules.py` and `check_contrast.py` exit `0`, and `DESIGN.md` index reflects the post-sync state.
