# §4 · Designing Text

28 rules (§4.1–§4.8.2). The third lens. Type covers most of the interface, and **the
three most common "unprofessional" causes** live here: an unsystematic type scale, lines
that are too long, and wrong line-height.

## §4.1 Establish a type scale

**Symptom**: every pixel value from 10px to 24px appears somewhere.

**Mechanism**: without a system, choosing sizes produces inconsistency and slows the
workflow.

**§4.1.1 Choosing a scale.** A linear scale fails here as well: small jumps matter at
the bottom and are wasted on headlines.

**§4.1.1a Modular scales.** Derive with a ratio — 4:5 (major third), 2:3 (perfect
fifth), 1:1.618 (golden) — compounding from 16px.

**§4.1.1b You end up with fractions.** 16px × 4:5 yields 31.25, 39.063, 48.828px.
Browsers round subpixel values differently; avoid them, and round manually if you use
them.

**§4.1.1c You usually need more sizes.** Rounded 3:4 gives 12 / 16 / 21 / 28 — and you
will want a value between 12–16 and between 16–21. Tightening the ratio just
reverse-engineers a scale you already knew you wanted.

**§4.1.1d Hand-crafted scales work better for interfaces.** No subpixel worries, and no
outsourcing the decision to a formula:

```
12  14  16  18  20  24  30  36  48  60  72
```

Restrictive enough to speed up decisions, loose enough not to feel short of a size. It
pairs well with the spacing scale in §3.2.2.

**§4.1.2 Avoid em units.** em is relative to the current size, so nested elements land
off-scale: `.875em` inside `1.25em` (20px) renders at 17.5px. Use px or rem.

## §4.2 Use good fonts

Judging typefaces takes years. Use shortcuts until then.

**§4.2.1 Play it safe.** A neutral sans-serif is the safest interface choice; with no
confidence in your taste, use the system stack:

```
-apple-system, Segoe UI, Roboto, Noto Sans, Ubuntu, Cantarell, Helvetica Neue
```

Unambitious, but users already know how it looks.

**§4.2.2 Ignore faces with fewer than five weights.** Well-made families usually have
complete weight sets. Filter by number of styles (weights × italics) above 10 — on
Google Fonts that removes about 85% of options, leaving under 50 sans-serifs.

**§4.2.3 Optimize for legibility.** Faces drawn for headlines have tighter spacing and a
shorter x-height; faces drawn for small sizes are wider and taller in the x-height.
**Don't use a condensed, short-x-height face for UI body text.**

**§4.2.4 Trust the wisdom of the crowd.** A popular typeface is probably good.
Especially useful when choosing something with personality, like a serif — that is hard
to judge by eye.

**§4.2.5 Steal from people who care.** Look at what the sites you admire actually use.

**§4.2.6 Develop your intuition.** Attention to well-set type compounds.

## §4.3 Keep line length in check

**Symptom**: text bends to the layout, so lines are long and tiring, and you lose your
place.

**Practice**: **45–75 characters per line**. On the web, em is easiest: **20–35em**.
Slightly over 75 can work, but it is risky territory.

**§4.3.1 Wider content.** When text sits beside images or large components, the
container may need to be wider — **the paragraph still gets constrained**. Different
widths in one region looks counterintuitive and almost always reads as more polished.

## §4.4 Baseline, not center

**Symptom**: mixing sizes on one line (a large card title, small actions top-right), then
centering them vertically, looks wrong.

**Mechanism**: the eye uses the baseline as its alignment reference; the mismatch is most
visible when the text is close together.

**Practice**: align mixed sizes on the **baseline**, not the box center.

## §4.5 Line-height is proportional

**§4.5.1 Line-height rises with line length.** Line spacing exists so the eye can find
the next line; the longer the line, the further it travels back, and the easier it
skips. Narrow content works at 1.5; wide content may need up to 2.

**§4.5.2 Line-height falls as font size grows.** Small text needs extra leading; large
text needs little. A large headline can sit at 1.

1.5 is a reasonable starting point, not a universal rule.

## §4.6 Not every link needs a color

**Symptom**: the treatment that makes a link pop out of a paragraph becomes oppressive
when almost everything is a link.

**Practice**: in link-dense interfaces, use a subtler emphasis — heavier weight or a
darker color. For peripheral links outside the main path, reveal the underline or color
only on hover; the curious still find them, and they stop competing with primary
actions.

## §4.7 Align with readability in mind

**§4.7.1 Don't center long form text.** Centering looks fine for headlines and short
standalone blocks; past 2–3 lines, left-align almost always reads better. When one block
among several centered ones is too long, **rewrite it shorter** — it fixes the alignment
and tightens the design.

**§4.7.2 Right-align numbers.** In tables, right-align numbers so decimal points line up
and columns can be compared at a glance.

**§4.7.3 Hyphenate justified text.** Justification without hyphenation leaves ugly word
gaps. Justified text suits a print-like feel (online magazines), but left-aligned works
just as well — it is preference, not correctness.

## §4.8 Use letter-spacing effectively

Default: trust the type designer. Two exceptions.

**§4.8.1 Tightening headlines.** A family optimized for body text (say Open Sans) can be
tightened when used for large headlines, to imitate a headline face. **Don't go the
other way** — adding spacing to a headline face rarely makes it work at small sizes.

**§4.8.2 Improving all-caps legibility.** Lowercase letters vary in x-height, ascenders
and descenders; all-caps letters do not, so they have fewer distinguishing features and
need more spacing.
