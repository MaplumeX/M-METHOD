# §3 · Layout and Spacing

18 rules (§3.1–§3.6.a). The second lens. **"Cramped, loose, slightly misaligned" almost
always lives here**, and the fixes are far safer than touching color.

## §3.1 Start with too much white space

**Symptom**: the interface feels tight, cheap, dirty.

**Mechanism**: white space is almost always **added** — you see crowding, add a little
margin or padding, stop when it looks acceptable. That process lands on the minimum
required to stop being obviously bad, not on good.

**§3.1.1 Remove, don't add.** Start with far more space than you think you need, then
subtract until satisfied. What looks "a bit too much" on one element in isolation is
usually "just right" in the context of the full interface.

**§3.1.2 Dense UIs have their place.** When a screen must hold a lot at once
(dashboards), density is a **deliberate decision**, not a default. The signal is clear:
needing less space is far more obvious than needing more.

## §3.2 Establish a spacing and sizing system

Don't agonize between 120px and 125px. Trying made-up values pixel by pixel slows you
down at best and produces inconsistent, ugly design at worst.

**§3.2.1 A linear scale won't work.** "Everything is a multiple of 4px" does not help
you choose. A system needs to account for **relative** difference: 12px → 16px is 33%
and nobody misses it; 500px → 520px is 4%, eight times less noticeable. **No two
adjacent values closer than about 25%.**

**§3.2.2 Defining the system.** Start from a base that divides cleanly — 16px, which is
also the default in every major browser — and build from its factors and multiples:
tight at the low end, progressively wider apart.

```
4  8  12  16  24  32  48  64  96  128  192  256  384  512  640  768
```

**§3.2.3 Using the system.** Need space below an element? Take a value from the scale.
Not enough? The next one up is usually right. Typing numbers in the browser makes it
easier to stay on the scale than dragging with a mouse.

## §3.3 You don't have to fill the screen

**Symptom**: content that wants 600px spread across a 1400px canvas, harder to read
than before.

**Mechanism**: available canvas is not an obligation. Spreading out or widening without
need only makes the interface harder to follow.

**Practice**: 600px of content stays 600px. Give each element exactly the space it
needs; don't make something worse to line up with something else.

**§3.3.1 Shrink the canvas.** If a small interface is hard to design on a large canvas,
shrink the canvas. For responsive apps, start at roughly 400px and design the mobile
layout first — then move up and fix what felt compromised. Usually less than expected.

**§3.3.2 Think in columns.** When something works best narrow but looks unbalanced
inside a wide layout, **split it into columns** rather than widening it. A narrow form
becomes a form column plus an explanation column.

**§3.3.3 Don't force it.** The reverse holds too: when content genuinely needs room,
use it. Don't cram everything into a small area out of politeness.

## §3.4 Grids are overrated

A grid is constrained percentage widths — useful for simplifying layout decisions and
for a sense of order. Outsourcing **every** layout decision to it backfires.

**§3.4.1 Not all elements should be fluid.** Many elements want a **fixed** width far
more than a relative one. A sidebar should be fixed at a width optimized for its
contents; the main area flexes and runs its own internal grid.

**§3.4.2 Don't shrink until you need to.** Give an element a max-width and shrink only
below it. Otherwise a flexibly-sized card can end up **wider on a mid-size screen than
on a large one**, because it fills a smaller container.

## §3.5 Relative sizing doesn't scale

**Symptom**: `2.5em` fixes "headline = 2.5 × body". On a small screen the body drops to
14px, so the headline renders at 35px — absurdly large.

**Mechanism**: a ratio that is right on a large screen is wrong on a small one. No fixed
relationship exists between them.

**Practice**: **elements that are large on big screens must shrink faster than elements
that were already small.** Gaps should compress as the screen shrinks. Use px or rem
rather than encoding relationships in em.

**§3.5.1 Relationships within elements don't scale either.** Button padding should not
be derived from font size. Large buttons want disproportionately generous padding and
small buttons want tighter padding — so a large button **feels** large rather than
looking like a scaled photograph of a small one.

## §3.6 Avoid ambiguous spacing

**Symptom**: in a stacked form, the gap below a label equals the gap below its input, so
nothing reads as a pair. Mildly confusing at best; users fill the wrong field at worst.

**Mechanism**: without a visible separator (border, background), only spacing says which
elements belong together.

**Practice**: **space around a group must exceed space within it**, vertically and
horizontally.

**§3.6.a The four manifestations**:

- Form label and its input.
- A section heading and the content it introduces.
- Bulleted list items — item spacing must exceed line-height, or each item reads as two
  lines.
- Horizontal groups of components — spacing within a group smaller than between groups.
