# Fluid Viewports, Workbench Scroll & Narrative Layouts

Extensions beyond *Refactoring UI* for marketing sites, scroll-driven product tours, and multi-panel app workbenches.

No coverage obligation (see `00-coverage.md`).

## 1. Fluid viewport rhythm (`clamp()`)

- **Never scale a desktop layout 1:1 down onto mobile.** A `1440px` reference composition shrinks into unreadable micro-type and tiny tap targets if treated proportionally. On `400px`, reflow multi-column regions, keep body copy `>= 16px`, and keep interactive targets `>= 44×44px` (`13-beyond.md`).
- **Use `clamp(min, preferred, max)` for display type and section breathing room** so hierarchy compresses smoothly across `400px → 1440px` without abrupt step jumps:
  - Example section vertical padding: `padding-block: clamp(32px, 6vw, 96px);`
  - Example hero headline: `font-size: clamp(30px, 4.5vw, 60px); line-height: 1.08;` (keep `min` and `max` aligned to the project's scale steps in `§4.1` / `§3.2`, or document the fluid range).
- **Respect `§3.3` on wide screens**: once a reading or form column reaches its `max-width` (`45–75ch` prose, `640–768px` main column), stop widening it and let outer margins absorb extra viewport width.

## 2. App workbenches: independent panel scrolling

For dense productivity tools, editors, or master-detail dashboards (`≥ 1024px`):

- **Use `100dvh` (not `100vh`)** so mobile browser chrome and dynamic toolbars do not clip bottom controls.
- **Give each scrolling column `min-height: 0; overflow-y: auto;`** inside a fixed-height grid/flex shell (`nav rail` + `item list` + `detail / inspector`), keeping persistent toolbars and primary actions pinned without scrolling the whole document.
- **Collapse gracefully below `1024px`**: disable locked `100dvh` nested scrolling on narrow viewports (`400px` / `< 1024px`) and return to normal single-document vertical flow so users never fight trapped inner scrollbars.

## 3. Marketing & product tours: scroll narratives

When building a landing page, editorial essay, or product tour (when explicitly requested — never inject marketing hero/scroll sections into an app dashboard per `15-direction.md`):

- **Sticky split narrative**: place concise narrative beats in a scrolling column (`45–65ch` max width, generous vertical beat spacing) beside a `position: sticky; top: 96px;` visual stage (code specimen, interactive preview, or diagram) that swaps cleanly as each beat enters view.
- **Zero layout shift**: reserve explicit `aspect-ratio` or `min-height` on sticky media stages before hydration/image load.
- **Motion & scroll performance**:
  - Animate `transform` and `opacity` only (`15-direction.md`); never animate `top`, `height`, or `width` on scroll.
  - Keep scroll-triggered reveals short (`200–300ms`, `ease-out`) and subtle (`8–16px` travel).
  - Under `@media (prefers-reduced-motion: reduce)`, disable sticky-scrubbed transforms and parallax; render sections statically visible with instant or opacity-only transitions.
- **Mobile fallback (`< 768px`)**: unpin `position: sticky` media stages and pair each narrative beat sequentially with its corresponding visual (`beat 1 → visual 1 → beat 2 → visual 2`) so text and media never decouple.
