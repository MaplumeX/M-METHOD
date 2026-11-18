# Refine & Review Modes · Auditing and Fixing Existing UI

## Read Gate (before editing or reporting)

Read before starting:

- [`09-antipatterns.md`](09-antipatterns.md) — symptom → `§id` → fix lookup
- For **Refine**: the first diagnostic lens file (`02`–`08`) that explains the symptom
- For **Review**: [`15-direction.md`](15-direction.md) in addition to `09-antipatterns.md`

## Diagnostic lens order

Sweep in this exact order and **stop at the first lens that explains the complaint** — later dimensions are usually downstream symptoms:

| # | Diagnostic lens | Reference |
|---|---|---|
| 1 | Visual hierarchy | [`02-hierarchy.md`](02-hierarchy.md) |
| 2 | Layout and spacing | [`03-spacing.md`](03-spacing.md) |
| 3 | Typography | [`04-typography.md`](04-typography.md) |
| 4 | Color | [`05-color.md`](05-color.md) |
| 5 | Depth | [`06-depth.md`](06-depth.md) |
| 6 | Images and graphics | [`07-images.md`](07-images.md) |
| 7 | Finishing touches | [`08-finishing.md`](08-finishing.md) |

## Refine · Fix existing UI

**Enter when**: "something feels off", "make it look better", or paying down UI debt.

- **Planning-period boundary**: if in `mm-plan` without implementation authorization, perform read-only diagnosis and return per-lens remediation steps to `mm-plan`; modify zero files.
- **Workflow**:
  1. Capture baseline screenshots at both desktop (`1440px`) and mobile (`400px`) widths.
  2. Check `09-antipatterns.md` first; if no direct hit, sweep lenses 1–7 and stop at the first explanatory lens.
  3. **Change one lens at a time** → re-capture screenshots → compare before/after → only then move to the next lens.
  4. Run `scripts/check_ui_rules.py <target>` (and `scripts/check_contrast.py` if colors changed).
  5. Present a reviewable diff with every change traced to its `§id` rule.
- **Stop points**: missing required tokens (switch to System mode), broken overall direction (return to Explore/Build mode), or systemic token/component drift across multiple screens (switch to [`mode-sync.md`](mode-sync.md)).
- **Completion criteria**:
  - Before/after screenshots at desktop and mobile widths (or explicit unverified-item list if headless);
  - `scripts/check_ui_rules.py` (and `check_contrast.py` if colors changed) exits `0`;
  - Every modification is traced to a `§id` rule number.

## Review · Audit without editing code

**Enter when**: "take a look", "what's wrong here", pre-launch check, or reviewing a user-supplied screenshot.

- **Independent Review Protocol (fresh-eyes isolation)**:
  - When reviewing UI generated in the same session, **do not grade from memory of authoring intent**. Either launch an isolated subagent/fresh context or audit strictly from rendered screenshots (`scripts/shoot.py` + `sheet.png` across `1440px` / `400px` / states), runtime DOM findings (horizontal overflow, console/page errors, broken images), and source code.
- **Workflow**:
  1. Run `scripts/shoot.py <target> --out shots/ --states default,empty,loading,error` (when a runnable URL/HTML exists) or inspect user-supplied screenshots; follow Refine steps 1–2 without modifying any files.
  2. Audit against [`09-antipatterns.md`](09-antipatterns.md), **State Coverage & Realistic Data** (missing `empty` / `loading` / `error` / `edge` states, or `Lorem ipsum` placeholders), and the **CRAP & Cognitive Load Checklist**:
     - **Contrast**: clear visual rank between primary, secondary, and tertiary elements (`§2.1`, `§2.4`, WCAG `§5.6`);
     - **Repetition**: consistent token scales, radii (`§1.4.3`), and interaction patterns across siblings;
     - **Alignment**: shared grid axes and `baseline` alignment on mixed text rows (`§4.4`);
     - **Proximity**: group gap > inner gap (`§3.6`), zero orphaned controls;
     - **Cognitive load & Task-first clarity**: single primary action (`§2.8`), progressive disclosure for secondary options, zero horizontal overflow or clipped controls at `1440px` and `400px`.
- **Output**:
  1. Issues ordered by **severity / impact** (not lens order): **Symptom → `§id` rule (or CRAP / State / Direction gap) → concrete fix**.
  2. **5-item AI Slop Test** verdicts (`Clear` / `Hit`) per `15-direction.md`.
  3. **State coverage & runtime verdict**: which states (`default`, `empty`, `loading`, `error`, `edge`) and runtime checks (overflow / broken images / console errors) passed vs failed/missing.
  4. Explicit statement of what was **not** checked (e.g. mobile width, dark mode, unrendered states).
- **Completion criteria**: every finding carries a `§id` rule (or `15-direction` ban / CRAP / state gap), all 5 AI Slop Test items have explicit verdicts, state & runtime coverage is reported, and unchecked areas are declared.
