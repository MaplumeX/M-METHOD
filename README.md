# M-METHOD

My own bundle of agent skills for software engineering.

TODO: write the manifesto — which failure modes this set exists to fix, and what it
deliberately does not try to do. Short: 5–10 lines is enough.

## Layout

```
skills/        one directory per skill: skills/<skill-name>/SKILL.md
references/    methodology docs shared across skills
```

A skill directory becomes available as soon as it contains a `SKILL.md`:

```
skills/<skill-name>/SKILL.md
skills/<skill-name>/scripts/
skills/<skill-name>/references/
```

## Install

With the [skills CLI](https://skills.sh) — copies the skill directories into your
agent:

```bash
npx skills add MaplumeX/M-METHOD                        # pick agents interactively
npx skills add MaplumeX/M-METHOD -g                     # for every project
npx skills add MaplumeX/M-METHOD --skill mm-plan        # just one
npx skills add MaplumeX/M-METHOD --agent claude-code codex cursor
```

Re-run to update; the installed copies are yours to edit.

## Local development

Install from this checkout to try a change before pushing it:

```bash
npx skills add ./ --agent <agent>
```

The CLI copies files rather than linking them, so re-run it after each edit. If your
agent supports loading skills from an arbitrary directory, pointing it at this
checkout works too — just don't do both, or every name loads twice.

## Conventions

- Write every skill in English, including `references/` and scripts. The one
exception is `description` trigger phrases: Chinese words belong there so the skill
still matches Chinese requests.
- Prefix every skill name (`mm-`) — skill names share a global namespace.
- `description` in frontmatter is the only trigger. Write what it does **and** when
  to use it, including the words a user would actually say.
- Orchestrator skills (the ones you type yourself) set
  `disable-model-invocation: true`. Discipline skills stay model-invokable.
- Orchestrators may call discipline skills; discipline skills never call orchestrators.
- Every skill needs an exit condition, otherwise it turns into an unbounded chat.
