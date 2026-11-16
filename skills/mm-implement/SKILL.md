---
name: mm-implement
description: Execute an approved plan file one step at a time, verifying each step before moving on. Use when the user says 按 plan 做、开工、开始实现、继续做、implement the plan, or asks what is left of a plan. Requires an existing .plan.md — without one this is planning or a small edit.
---

# Implement

A plan is a promise made before the work existed. Executing it is mostly a
discipline problem: the code is the easy part, and the failures are scope creep,
skipped verification, and decisions changed on the fly to fit the code.

## Entry

Find the plan:

```bash
ls .agents/ADR/proposed/**/*.plan.md
```

More than one and the user did not say which → ask. None → this is not the skill's
job: a small edit just gets done, and anything larger goes back to `mm-plan`. If the
user insists on proceeding without a plan, say out loud that the work is unplanned
and record the deviation in the report.

Read the plan and the record its `ADR:` line points to. The record is read-only
here: it explains constraints, it does not authorize edits.

## Preflight

- Walk `## Prerequisites`. Anything missing gets reported as missing — never mocked,
  never silently skipped, never "temporarily stubbed".
- Check the working tree. Uncommitted work that is not yours means stop and ask
  before touching the same files.

## Steps

Work the steps in order without asking permission between them. Stop on a failed
verification, a triggered stop point, or a disagreement with the record — not on
every step boundary.

- After each step, run that step's inline verification. A step without a green check
  is not finished, and the next step waits.
- `## Not in scope` is a list of things not to do. A problem found there gets
  recorded in the report and left alone; fixing it is how a two-step change becomes
  a review nobody can read.
- When a comment is needed to explain a constraint, write it in the same edit that
  writes the code, following the record standard's `## References from code`: the
  consequence first, then `ADR <date>-<slug>`. Adding them in a final pass produces
  pointers with no consequence, and misses the places that needed one.
- If the user names a subset of steps, do that subset and state what stayed undone.

## When reality disagrees

- The record's decision does not hold → stop, say why, and route back to `mm-plan`
  for a superseding record. Never rewrite the record to match the code.
- A step's premise is gone (file moved, dependency changed, API differs) → stop and
  report. Either the plan is revised or the approach changes; picking one silently
  is how the plan and the code stop describing the same thing.
- A stop point triggers → stop and ask. That is what it is for.

## Report

- Steps completed, with the result of each inline verification.
- `## Verification` lines you could run and what they returned. Lines that need a
  human stay unchecked — ticking them is signing for someone else's acceptance.
- Anything found and deliberately not fixed, with the reason.
- Whether the plan needs revising before the rest can proceed.

Do not commit unless asked. Do not move the record, do not delete the plan, and do
not run `mm-land` — promotion belongs to the user's acceptance, not to the code
being green.

## Exit condition

- Every step completed with a recorded verification.
- Every automatable line in `## Verification` run, with its result written beside
  the checkbox.
- The record still sits in `proposed/`, the plan is still in place.
- The user has been told what to check manually and what was left undone.
