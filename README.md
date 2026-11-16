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

## Dev loop

Install once, from this repo's parent directory:

```bash
pi install /home/maplume/projects/M-METHOD
```

Local packages are loaded from the resolved path without copying, so edits take
effect on `/reload` — write and use from the same directory.

Then:

```
/skill:<name> [args]    force-load a skill
```

## Conventions

- Prefix every skill name (`mm-`) — skill names share a global namespace.
- `description` in frontmatter is the only trigger. Write what it does **and** when
  to use it, including the words a user would actually say.
- Orchestrator skills (the ones you type yourself) set
  `disable-model-invocation: true`. Discipline skills stay model-invokable.
- Orchestrators may call discipline skills; discipline skills never call orchestrators.
- Every skill needs an exit condition, otherwise it turns into an unbounded chat.
