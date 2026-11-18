# Plan file

A plan is the execution attachment to a `proposed/` ADR. It says what to do, in what
order, and how to know it worked. It does not say why that approach was chosen — the
record owns the rationale, and copying it here creates a second copy that drifts.

Path: `.agents/ADR/proposed/yyyy-mm-dd-<delivery-slug>.plan.md`, at the root of
`proposed/` (sibling to the `{class}/` folders). One plan per delivery — a delivery
may land several decisions across classes, and with a single one the slug matches the
record name.

```markdown
# Plan: <title>

ADR: <class>/<record>.md
ADR: <other-class>/<other-record>.md
Depends on: <class>/<prerequisite-record>.md
Constrained by: ../implemented/<class>/<constraint-record>.md

## Scope
## Not in scope
## Steps
## Verification
## Prerequisites
## Rollback
## Stop points
```

`Scope`, `Steps`, and `Verification` are the floor. Everything else is a slot:
include it when it has content, omit it when it does not. A heading followed by
`None.` turns the file into a form, and forms stop being filled in.

## Header

`ADR:` is a relative link from `proposed/` to each record this plan executes
(`<class>/<record>.md`), one line per decision, never a bare filename. The first is
the primary record and names a single-record delivery. A plan without that line is
unattached and cannot be closed out.

Every listed record ships with this delivery. A record that half-shipped is removed
from the header and stays in `proposed/` — `implemented/` means delivered, not
attempted.

`Depends on:` lists prerequisite ADR(s) whose delivery must complete before this plan
starts. Always point to the prerequisite ADR (`.md`), never its `.plan.md` — plans
are deleted on landing, whereas ADR links are automatically updated when the record
moves to `implemented/`.

`Constrained by:` lists other records that bind the work without being executed here
(a design system, a packaging decision that forbids new dependencies, a naming rule).
Optional, but when a second record constrains the work, this is where it goes —
otherwise the executor discovers it mid-step and treats it as an obstacle instead of a
boundary.

Both `Depends on:` and `Constrained by:` double as execution order gates: while any
referenced record still sits under `proposed/`, this plan is blocked behind it; once
`mm-land` promotes that record and rewrites the link to `../implemented/...`, this
plan becomes ready.

## Scope / Not in scope

One paragraph of what the work covers, then an explicit out-of-scope list. The
out-of-scope list is what stops the executor from quietly widening the task.

For longer multi-step plans (6+ steps), you may add a 2–3 line `Guardrails:`
bullet list at the end of `## Scope` summarizing non-negotiable ADR invariants
(what must not be broken, never why) so they stay visible late in execution.

## Steps

Each step names the files it touches and carries **one inline verification** — a
command an agent can run. A step that says "implement the feature" is not a step.
Tag UI steps with `[mm-ui: Build]` or `[mm-ui: Refine]`, split multi-file details
into short indented sub-bullets, and initialize `Verify:` with `— pending`:

```markdown
1. [mm-ui: Build] Timer UI — `src/hooks/useTimer.ts`, `src/components/{TimerRing,Controls}.tsx`.
   - SVG stroke-dashoffset ring; single-column stage `max-width: 480px`.
   Verify: `npm run build && python3 ...shoot.py ... --strict` — pending
```

During execution, replace `— pending` with **one concise summary line** (date +
measured scope/counts, e.g. ``Verify: `pnpm test src/config/load.test.ts` — passed 2026-11-16: 14 tests (1 file)``)
so a later session running `mm-land` can verify every step ran without turning
`## Steps` into a wall of prose. Keep debugging narratives and fixed-bug stories in
your chat report, not inside `Verify:`. Do not repeat these checks in
`## Verification`. That section belongs to the human, and duplicating an assertion in
two places is how the two copies end up disagreeing.

If the work cannot be cut into independently acceptable steps, say so and run it as
one step instead of inventing phases that only exist on paper. A "step 0:
investigate" is a red flag — investigation happens before the plan.

## Verification

This is the human's acceptance checklist and `mm-land`'s contract. Every line is a
checkbox with its result recorded beside it:

```markdown
- [x] `pnpm test` green — 142 passed, 2026-11-16
- [x] `config show` prints a source column — manual, 3 keys checked
- [ ] malformed TOML exits non-zero — not run
```

An unchecked line blocks promotion to `implemented/`. Recording the result, not just
the tick, is what lets a later session tell "verified" from "someone assumed".

List here only what a person confirms: manual checks, cross-step behaviour, and
at most one final end-to-end command run (e.g., full test suite + build). Per-step
unit subsets, artifact checks, and single-step screenshots stay inside `## Steps`.

## Prerequisites

Every API key, token, third-party account, tool, or service the work needs —
including auxiliary scripts or runtime libraries required by verification steps
(e.g., Playwright, Pillow) — each with a one-line explanation of what it is for.
Collect them here, up front. Asking for credentials or missing tools midway
through implementation is how a session dies.

Record anything you could not verify as a prerequisite, not as verified. Do not
install tools, launch applications, or mutate state to prove a plan works.

## Rollback

For any step that leaves external state changed — deploys, migrations, published
packages, sent messages — the way back, or an explicit statement that there is none.
An irreversible step deserves to be called irreversible.

## Stop points

Two kinds of stop points, each bound explicitly to a step number:

- **Hard gate (mandatory pause)**: the executor must stop after the named step and
  wait for explicit user confirmation before starting the next step.
- **Conditional gate (trigger pause)**: the two or three things most likely to go
  wrong, and the exact point at which the executor must stop and ask rather than
  inventing a workaround.

Format them as scannable, step-anchored items:

```markdown
- **Hard gate (After Step 2)**: confirm `Session` fields and `focusedSec` semantics before continuing.
- **Conditional gate (After Step 5)**: if the notification prompt fails in a real browser, stop and ask whether to move it into Settings rather than adding retries.
```

## When the plan changes

Plans are working state: edit them directly when a detail moves. Do not append a
changelog — git already has one, and a plan that argues with its own history is a
record wearing the wrong clothes.

On `mm-land`, the plan file is deleted: ephemeral step-level debug notes disappear
with it, while permanent fact shifts (paths, defaults, dependency versions) and any
waived `## Verification` gaps fold into the promoted ADR's `## Consequences`.

If the direction itself changes, stop editing. The record is superseded by a new
`proposed/` record, and this plan is deleted rather than migrated. A plan only ever
belongs to the record named in its header.
