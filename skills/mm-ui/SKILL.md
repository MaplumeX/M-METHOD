---
name: mm-ui
description: Design rules and workflow for web UI, distilled from Refactoring UI. Four modes — design system, build, refine, review — with three disciplines that cut across all of them. Use when building or changing a page, component, or design system, or when something "looks off" but nobody can say why — 界面设计、样式调整、UI 太丑、设计评审、视觉层级、配色、对比度、间距、排版、阴影、空状态、设计规范. Not for backend logic, copy editing, or changes with no visual surface.
---

# UI

Work that has a visual surface. Four modes, three disciplines.

Out of scope: backend logic, copy editing, changes nobody can see. This is not an
aesthetic generator either — it constrains and checks, it does not supply taste.

## Step 0 · Read the project before judging it

Run this before any design claim. It prevents the two worst failures: fighting a
design system that already exists, and emitting values the project cannot use.

Report briefly:

1. **Framework** — React / Vue / Svelte / plain HTML; SSR or SPA.
2. **Existing tokens** — CSS custom properties, a theme object, `tokens.json`, a
   `theme/` directory, a Tailwind config.
3. **Component library** — shadcn/ui, MUI, Ant Design, Chakra, Radix. These carry
   their own token contracts; read them before writing a component.
4. **Dark mode** — present, planned, absent.
5. **Existing type and spacing scales** — their real values, lifted from config, never
   from memory.

**An existing system always wins.** Where there is one, translate these principles
into its vocabulary. Where there is none, propose one. Never overwrite, never silently
migrate, never add a build-time dependency nobody asked for.

## Pick a mode

Ask in this order, stop at the first hit:

1. Does the project have a design system? No → **System**
2. Is something new being added? → **Build**
3. Should the interface change? → **Refine**
4. Only an opinion is wanted? → **Review**

When intents mix, run System → Build → Refine in that order and say which leg you are
on. Each mode's **stop points** are the only handoffs between them.

## System · Establish or change the design system

**Enters when**: no system exists, the system is being replaced, or a scale is missing.

1. Interview: brand color, neutral temperature (cool/warm), product personality, dark
   mode. Batch the questions, allow every one to be skipped, allow defaults.
2. Build nine-step ramps: base 500 → 900/100 → 700/300 → the rest. Raise saturation as
   lightness moves away from 50%.
3. Check contrast: 4.5:1 body / 3:1 large, with `scripts/check_contrast.py`, not by eye.
4. Emit four files: `tokens.json` / `tokens.css` / `DESIGN.md` / `preview.html`.
5. Record a `proposed/design/` ADR.

Details in `11-tokens.md`; for a Tailwind expression see `12-tailwind.md` (optional
mapping).

**Stops at**: ramp direction, token naming. Both are expensive to change later —
ask before committing.

**Done when**: `preview.html` has no step you cannot justify; every contrast pair
passes; the record exists.

## Build · Add an interface

**Enters when**: a new page, component, or feature block.

The order is the method. Out of order produces over-decorated, under-structured
screens.

1. Start with a feature, not a shell. `§1.1`
2. Work in grayscale — force spacing, size and contrast to carry the hierarchy. `§1.2.1`
3. Rank the content primary / secondary / tertiary, and the actions one primary / a few
   secondary / several tertiary. `§2.1 §2.8`
4. Lay out from the scale. `§3.2 §4.1`
5. Set measure and rhythm: 45–75 characters, line-height matched to width and size.
   `§4.3 §4.5`
6. Then color, then depth, then finishing — in that order. `§5 §6 §8`
7. The empty state belongs to the feature, designed with it. `§8.4`

Look up common components in `10-recipes.md` instead of re-deriving them.

**Before the first line of markup**, write a constraint brief as a comment in the
file: the content ranking, plus the token values steps 4–6 will draw from. A single
generation pass collapses "grayscale first, then rank, then color" into "write the
colored markup directly", because nothing forces the order to surface. The comment
makes the process checkable.

**Stops at**: design direction (not detail), a missing scale (go to System).

**Done when**: screenshots exist, every change traces to a rule id, the empty state is
there.

## Refine · Change an existing interface

**Enters when**: "something feels off", "make it look better", design debt.

1. Screenshot first: desktop and mobile widths.
2. Check `09-antipatterns.md` — if the symptom is listed, you already have the rule id.
   Otherwise sweep the seven lenses and **stop at the first one that explains the
   complaint**; the later ones are usually its consequences.

   | # | Lens | File |
   |---|---|---|
   | 1 | Hierarchy | `02-hierarchy.md` |
   | 2 | Layout and spacing | `03-spacing.md` |
   | 3 | Typography | `04-typography.md` |
   | 4 | Color | `05-color.md` |
   | 5 | Depth | `06-depth.md` |
   | 6 | Images | `07-images.md` |
   | 7 | Finishing | `08-finishing.md` |

3. **Change one lens at a time** → screenshot again → compare → next. Adjusting
   spacing means adjusting only spacing.
4. Submit as a reviewable diff, each change citing its rule id.

**Stops at**: a needed token (go to System), a wrong direction (go back to Build).

**Done when**: before/after screenshots exist, every change traces to a rule id.

## Review · Judge without changing

**Enters when**: "take a look", "what is wrong here", a pre-launch check, or a pasted
screenshot.

Same as Refine steps 1–2, with no code changes.

**Produces** a findings report: **symptom → rule id → concrete fix**, ordered by
severity, not by lens.

**Done when**: every finding carries a rule id, and anything you did not look at is
stated as not looked at. A finding without a rule id is an opinion — and an opinion is
what the user already had when they said something felt off.

## Three disciplines

**1. Change one lens at a time.** The biggest trap in UI work is changing everything
at once — spacing, weight, shadow — and concluding "it looks better overall". Next
time something breaks you cannot tell which change caused it. Change one dimension,
look, then the next.

**2. Evidence before opinion.** Say what is in the screenshot — how many spacing steps
are in play, what repeats, what the contrast ratio is — before saying what should
change. "Add more white space" without that is noise, and nobody knows what it points
at.

**3. A rule id is the only arguable unit.** "This feels cramped" cannot be discussed.
"Violates §3.6: group spacing equals within-group spacing" can. Every finding and
every change carries an id.

## Visual evidence

**No visual claim without looking.** Render when the environment allows — a dev server
plus screenshots at desktop and mobile widths. Reading markup and CSS finds spacing and
structure problems; it cannot find "the shadow looks dirty" or "the hierarchy does not
land".

When rendering is impossible (no browser, no network, a library-only change), say so in
the report and mark which conclusions were not visually checked.

## Decisions become records

A UI decision that outlives one screen is an ADR, not a comment:

| Decision | Where |
|---|---|
| color ramps, spacing scale, type scale, radius and elevation scales | `proposed/design/` |
| component library or design-system choice | `proposed/design/` |
| dark-mode strategy | `proposed/design/` |
| one screen's layout tradeoffs | not a record — it belongs in the plan |

Follow `.agents/ADR/AGENTS.md` when writing one. A single screen's styling is not worth
recording; the system it draws from is.

## Reference library

151 rules, split by diagnostic lens, each carrying a `§id` that resolves against
`00-coverage.md`.

| File | Contents |
|---|---|
| `01-starting.md` | Starting from scratch: when to decide (17) |
| `02-hierarchy.md` | Hierarchy (20) |
| `03-spacing.md` | Layout and spacing (18) |
| `04-typography.md` | Typography (28) |
| `05-color.md` | Color (22) |
| `06-depth.md` | Depth (17) |
| `07-images.md` | Images (14) |
| `08-finishing.md` | Finishing touches (12) |
| `09-antipatterns.md` | Symptom → rule id index |
| `10-recipes.md` | Buttons, form groups, cards, empty states, tables, dropdowns, modals, alerts |
| `11-tokens.md` | Building a token system from zero |
| `12-tailwind.md` | Optional mapping, never a binding |
| `13-beyond.md` | Dark mode, focus, target sizes, motion, breakpoints, z-index, semantic tokens |
| `14-laws.md` | Twelve laws and the hard gates |
| `00-coverage.md` | All 151 rules and where they live |
