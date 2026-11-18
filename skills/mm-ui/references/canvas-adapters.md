# Output Canvas Adapters

Design reasoning (`§1`–`§15`, `Explore`, `State Matrix`, `Review`) is independent of the rendering medium. Choose the lowest-friction canvas that matches the current stage and available tools.

## 1. Standalone HTML Prototype

Single-file or local `.html` surface (e.g. `preview.html` in `System`, or a temporary exploration/prototype file) powered by `tokens.css` or inline CSS variables.

- **Best for**:
  - `System` token & 4-canary specimen verification (`preview.html`);
  - `Explore` side-by-side structural comparison when workspace writes are authorized;
  - **Prototype-first `Build`**: validating layout, typography, grayscale hierarchy (`§1.2.1`), and all interactive states of a complex new page before wiring framework routing, state stores, or API hooks.
- **Rules**:
  - Must still obey `mm-ui` semantic tokens, scales (`§3.2`, `§4.1`), realistic domain data (never `Lorem ipsum`), and `check_ui_rules.py` checks.
  - Include a lightweight, non-intrusive **state switcher bar** (fixed corner pill or top dev strip) with `data-state="<state>"` (or `data-mm-state="<state>"`) attributes on the buttons — and/or `?state=<state>` query-param handling — so both human reviewers and `scripts/shoot.py --states default,empty,loading,error` can toggle `default` / `empty` / `loading` / `error` / `edge` (plus `light` / `dark` if enabled) automatically.
  - Mark disposable exploration sketches clearly (`§1.2.2`) so they are cleaned up or promoted cleanly into production code.

## 2. Design Tool Canvas via MCP (Figma / Paper / pen.dev)

- **Activate only when**: an appropriate design-tool MCP server/tool is actually present in the current session **and** the user requests or supplies a design board/file target.
- **Never** assume or fabricate unavailable MCP tools. If no design-tool MCP is active, fall back immediately to **Standalone HTML Prototype** (or ASCII wireframes during planning-period read-only mode) and state the fallback explicitly.
- **Mapping rules when active**:
  - Sync tokens and existing Component Index entries from `DESIGN.md` before drawing new frames (`mode-sync.md`).
  - Render explicit artboards/frames for `1440px` desktop, `400px` mobile, and every confirmed state in the **State Matrix** (`default`, `empty`, `loading`, `error`, `edge`) using realistic domain copy.

## 3. Production Framework Code

Target project files (`.tsx`, `.jsx`, `.vue`, `.svelte`, `.css`, `.scss`, `.html`, Tailwind config).

- **Best for**: standard `Build` and `Refine` delivery once direction and structure are settled.
- **Rules**:
  - Reuse existing entries from the `DESIGN.md` **Component Index** before creating new primitives (`mode-sync.md`).
  - Consume semantic tokens only (`13-beyond.md`), follow `Pass 1 → Pass 2` (`mode-build.md`), and pass `scripts/check_ui_rules.py` + `scripts/check_contrast.py`.
