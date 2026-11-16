---
name: mm-setup
description: Configure a repository so coding agents record decisions as ADRs under .agents/ADR/, by installing the ADR standard and pointing AGENTS.md at it. Use when starting a repo, when the user asks where decisions, ADRs, or design docs should live — phrases like 「决策记在哪」「ADR 放哪」「记一下这个决定」— or when AGENTS.md exists but says nothing about recording decisions.
disable-model-invocation: true
---

# Setup decision records

Run this once per repository. It installs the ADR standard into `.agents/ADR/` and
adds a pointer to it in the root `AGENTS.md`. Nothing else — no sample ADR, no
guesses about the project.

## Why this exists

Agents re-litigate settled questions because the reasoning behind a choice lives in
nobody's context. Code shows *what* was chosen, never *why* or *what was ruled out*.
Without a written home for decisions, every session re-derives them and quietly
contradicts the last one.

`.agents/ADR/` is that home. It sits beside `.agents/skills/`, travels with the
repo, and is not tied to one agent tool.

## Flow

1. Find the repository root:

   ```bash
   git rev-parse --show-toplevel
   ```

   If that fails you are not in a repo. Confirm the intended root with the user
   before writing anything.

2. Read the root `AGENTS.md` if it exists. Note existing conventions — doc layout,
   naming, language. If they conflict with the ADR standard, ask which wins instead
   of silently overriding.

   If `AGENTS.md` is missing but `CLAUDE.md` exists, ask whether to create
   `AGENTS.md`, write into `CLAUDE.md`, or both.

3. Create the directory:

   ```bash
   mkdir -p .agents/ADR
   ```

4. Install the standard. Its source is `references/adr-standard.md` in this skill's
   directory — resolve it relative to the skill, not the project.

   - Target `.agents/ADR/AGENTS.md` missing → copy the file there.
   - Present and identical → skip, report "already installed".
   - Present and different → show a diff and ask. A project may have tightened the
     standard on purpose; this skill must not flatten that back to the default.

5. Write the pointer block into the root `AGENTS.md`, fenced by
   `<!-- BEGIN: decision-records -->` and `<!-- END: decision-records -->`:

   ```markdown
   <!-- BEGIN: decision-records -->
   ## Decision records

   Decisions live in `.agents/ADR/`, one file per decision, path-encoded as
   `{proposed|implemented|rejected|archived}/{architecture|feature|bug-fix|process}/yyyy-mm-dd-title.md`.
   Read `.agents/ADR/AGENTS.md` before writing or changing one.
   <!-- END: decision-records -->
   ```

   - Markers present → replace everything between them, keep the markers.
   - File exists without markers → append after a blank line.
   - File missing → create it containing exactly the block.

   The block stays this short on purpose: it is loaded in every session, so it
   carries only the location and the pointer. The rules belong in the standard,
   which is read only when someone actually writes a record.

6. Report the paths you touched and whether you created, appended, replaced, or
   skipped. Do not write a sample ADR unless asked.

## Exit condition

- `.agents/ADR/AGENTS.md` exists and matches the standard, or the user explicitly
  chose to keep their own version.
- Root `AGENTS.md` contains exactly one `decision-records` block with intact markers.
- No other section of `AGENTS.md` changed.
