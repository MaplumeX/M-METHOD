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

With the [skills CLI](https://skills.sh) — copies the skill directories:

```bash
npx skills add MaplumeX/M-METHOD -a pi        # into this project
npx skills add MaplumeX/M-METHOD -a pi -g     # for every project
npx skills add MaplumeX/M-METHOD -a pi --skill mm-plan   # just one
```

Re-run to update; edit the installed copies freely. Drop `-a pi` to pick the agent
interactively.

## Dev loop

While editing this repo, install it as a Pi package instead:

```bash
pi install /path/to/M-METHOD
```

Local packages load from the resolved path without copying, so edits take effect on
`/reload` — write and use from the same directory. Use one of the two mechanisms,
not both, or every skill is loaded twice under the same name.

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
