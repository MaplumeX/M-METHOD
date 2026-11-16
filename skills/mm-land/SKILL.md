---
name: mm-land
description: Close out accepted work by removing its plan file and promoting its ADR from proposed/ to implemented/. Use when the user says the work passed acceptance — 验收通过、做完了、可以了、land it、close it out — or asks to finish or clean up an ADR. Never use it on your own judgement that the code looks done.
---

# Land

Landing is the only transition that turns a proposal into a claim about reality.
Before it runs, `proposed/` is allowed to be wrong. After it runs, `implemented/`
must be true.

## Gate

Land only on an explicit acceptance from the user. Passing tests, a clean diff, and
a plan whose steps are all done are inputs to acceptance, not acceptance. If the
user has not said the work is accepted, stop and ask. Moving the record early makes
`implemented/` lie, and editing it back does not undo that — the lifecycle is
history.

If the user says the work did not pass, do not land. Ask which line of the plan's
`## Verification` failed; the plan gets revised, not promoted.

## Flow

1. Find the plan:

   ```bash
   ls .agents/ADR/proposed/**/*.plan.md
   ```

   More than one and the user did not say which → ask. Never guess from timestamps.
   No plan at all → still landable, but say so out loud and skip to step 6; the
   record's own `## Acceptance criteria` becomes the checklist.

2. Read the plan's header `ADR:` link. That record, and no other, is being landed.

3. Read the plan's `## Verification` checkboxes. Every line must be checked and
   carry a result. An unchecked line means that part was not accepted — report which
   ones and stop. This section is the human's acceptance, not yours.

4. Walk `## Steps` and confirm each inline verification actually ran. A step whose
   command was never run is not done, whatever the checkboxes say. Then check for
   drift between plan, record, and code: the plan was approved against a state that
   may have moved since. If a step's premise is gone, or the record's decision no
   longer matches what shipped, stop. Either the plan is revised, or the record is
   superseded by a new one — never quietly promoted with a stale decision.

5. Delete the plan:

   ```bash
   rm .agents/ADR/proposed/{class}/{name}.plan.md
   ```

6. Promote the record:

   ```bash
   mv .agents/ADR/proposed/{class}/{name}.md \
      .agents/ADR/implemented/{class}/{name}.md
   ```

   Then edit it, per `.agents/ADR/AGENTS.md`:

   - `Status: proposed` → `Status: implemented`
   - `## Proposal` → `## Decision`, present tense, describing what shipped
   - fold `## Acceptance criteria` and `## Risks` into `## Consequences`
   - correct facts that moved during implementation — paths, names, defaults. Facts
     only. If the decision itself changed, stop: that is a new record.

7. Repair inbound links. Relative links encode the lifecycle folder, so every link
   to the old path now breaks:

   ```bash
   grep -rn "proposed/{class}/{name}" .agents/ADR AGENTS.md docs 2>/dev/null
   ```

   Rewrite each hit to the `implemented/` path. Never edit an archived record to
   repair a link out of it.

8. Report the plan deleted, the record moved, the sections rewritten, the links
   repaired, and anything still owed — a PR, a release note, a follow-up record.
   Leave the change uncommitted and say so; staging and committing it is the user's
   call.

## Exit condition

- No `.plan.md` remains for this record.
- The record sits under `implemented/` with `Status: implemented`.
- No `## Proposal`, `## Plan`, `## Acceptance criteria`, or `## Risks` heading
  survives in it.
- No inbound link points at the old `proposed/` path.
- The user has been told exactly what changed.
