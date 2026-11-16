---
name: mm-plan
description: Turn a rough idea into an approved, decision-complete plan by interrogating the user round by round. Use when the user wants to plan, design, stress-test, or judge whether to build something — 出方案、怎么设计、值不值得、有没有必要 — or asks how they should approach a change. Not for bug fixes, error diagnosis, or small edits.
---

# Plan

A plan is not a document you produce. It is a design tree you and the user settle
together: every decision branches into the decisions that hang off it, and the plan
is done when no branch is left silently assumed.

## Gate first

Three exits, chosen before any questioning.

- **Not my job.** Bug reports, stack traces, flaky tests, and "why is this broken"
  are diagnosis, not planning. Say so in one line and route out. A plan built on an
  undiagnosed bug is speculation with extra steps.
- **Lightweight.** The problem is defined and the only open question is how to fix
  it, with no real alternatives. Answer in 2-3 sentences — what changes, where, why
  — after naming the brute-force version in one line. Then wait for approval.
- **Full.** Everything else. Proceed below.

Upgrade from lightweight when you find three or more genuinely different approaches
with meaningful tradeoffs. See `references/modes.md` for the lightweight, evaluation,
and triage variants.

## Ground

Read before proposing anything:

- Root `AGENTS.md`, plus only the domain rule that matches this problem. Loading the
  whole tree dilutes the rules that actually bind.
- `.agents/ADR/AGENTS.md`, the `implemented/` records covering this area, and any
  `proposed/` record that overlaps. A plan that duplicates an open proposal is
  either that proposal's continuation or its replacement — say which. If the repo
  has no `.agents/ADR/`, skip it: this skill has to work before setup has run.
- The real config file when the plan touches a default, port, env var, or flag. Lift
  the live value; never quote one from memory.

If the emerging plan contradicts a documented rule or an ADR — a "never X", a
"must Y" — say which rule, which step, and what you recommend. Do not silently
override it, and do not stop dead either: the conflict should reach the user while
there is still time to choose. If the plan supersedes an ADR, it produces a new
record that cross-links the old one; never edit the old decision into a different
one.

## Facts are yours, decisions are theirs

Look up everything you can: framework built-ins, official patterns, ecosystem
standards, current file contents, whether a dependency already solves this. An
existing official solution is the default recommendation unless you can say why it
falls short for this specific case.

For a lookup that spans files or needs current external docs, dispatch a subagent
instead of spending the planning context on it. Never ask the user for a fact you
could find yourself. Never block a whole round on a lookup either — only the
questions downstream of that fact wait; ask the rest of the frontier now.

Decisions belong to the user. Put each one to them with a recommendation, and wait.

## Rounds

Work the tree in rounds. The **frontier** is every decision whose prerequisites are
already settled — what you can ask now without guessing at answers you have not
heard. Ask the whole frontier in one round, then stop.

```
❓ **Q1** — **<question title>**

<one sentence of context>

- **A.** <option> — <what it costs or buys>
- **B.** <option> — <what it costs or buys>

➡️ **A**, because <reason>.

---

❓ **Q2** — **<question title>**

<context; no options — the answer is a fact about intent, not a design choice>

➡️ <your recommended answer>
```

Give multiple options whenever the design space really has them: naming the options
makes the question cheap to answer and shows what you considered. Write each option
with its consequence, not just its name — the user is choosing a consequence, not a
label. Skip the list when the answer is an intent, a number, or a fact about the
world.

Never present a set of equal options with no recommendation. A menu is a way of not
deciding, and it moves the work back to the user without shrinking it.

Word each question so that "yes" accepts your recommendation. A question that
depends on another question still open in this round belongs to a later round, not
this one.

Each round reshapes the tree: settled decisions push the frontier outward and
unblock what depended on them. Recompute the frontier and ask the next round.

Keep a running list of settled decisions. After three rounds most of the tree is
behind you, and a plan that forgets what was already decided starts re-asking it.

If the user does not know the answer to a frontier question, it is not a decision:
either it is a fact to look up, or it is a constraint to assume out loud ("assuming
X for now, which means Y"). Never let an unanswered question quietly become a
default.

## Converge

When the frontier is thin enough to see the shape of the answer:

- Give **one** recommended approach: rationale, effort, risk, and what existing code
  it builds on.
- Always include the minimal option — the version that adds the least.
- Mention an alternative only when a concrete tradeoff could change the user's
  choice. A menu of equal options is a way of not deciding.
- Name the most fragile assumption: "This plan assumes X. If X does not hold, Y
  happens." If it is load-bearing, deform the design to survive its failure instead
  of planning on hope.
- Anything that makes every future user install or configure something is a setup
  cost. Default to the zero-setup form; name why it cannot do the job before
  offering the setup-requiring one.

Run the attack angles in `references/modes.md` only when the plan involves external
dependencies, high concurrency, or data migration. If an attack breaks the approach,
discard it and say why — never present a plan that failed an attack without
disclosing the failure.

## Gate before exit

- **Simplicity.** Every try/catch, retry, fallback, and flag maps to one named
  failure mode. Delete the layers that only might fail. If the plan is mostly
  workaround machinery around a misbehaving dependency, the premise is wrong — name
  the route change instead.
- **Surface delta.** List new commands, env vars, flags, services. Prefer +0.
- **Blast radius.** More than ~8 files, or a new service, gets said out loud.
- **Rollback.** What state can you return to, and how much work is that?
- **No placeholders.** TBD, TODO, "implement later", "similar to step N" — a plan
  containing one is a promise to plan later.
- **Phase independence.** Each phase must be usable on its own if the next never
  lands. If the work cannot be cut that way, ship one phase. A "Phase 0:
  investigate" is the same red flag: investigation happens before the plan.

## Output

- **Building** — what this is, one paragraph.
- **Not building** — explicit out-of-scope list. This is what stops scope creep.
- **Approach** — chosen option and why.
- **Key decisions** — 3-5, with the reasoning that made them decisions.
- **Unknowns** — only items deliberately deferred, each with a reason and an owner.
  A vague gap is not an unknown; it is an unfinished plan, so loop back.

If the decision is durable — expensive to reverse, or likely to be re-litigated —
produce two artifacts, both only after the user approves them:

- `proposed/{class}/yyyy-mm-dd-title.md` — the record, per `.agents/ADR/AGENTS.md`.
- `proposed/{class}/yyyy-mm-dd-title.plan.md` — the execution attachment, per
  `references/plan-file.md`.

Never write an `implemented/` record for something that has not shipped. The record
moves there after acceptance, when `mm-land` runs — not before.

The plan file is also the handoff. When the user asks for one, or the environment
cannot continue, write it rather than explaining why you stopped.

The session ends when the frontier is empty. Do not write code until the user
confirms you reached a shared understanding — unless they already authorized
implementation for this same task ("直接做", "按你说的来"), in which case state
which plan you are executing, check for drift since it was approved, and proceed.
