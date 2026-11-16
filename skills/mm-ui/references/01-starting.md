# §1 · Starting from Scratch

17 rules (§1.1–§1.5.3). This chapter governs **when** decisions are made, not how —
which is why it constrains only the first three steps of Build.

## §1.1 Start with a feature, not a layout

**Symptom**: stuck choosing between top navigation and a sidebar, whether content goes
in a container, where the logo belongs.

**Mechanism**: an application is a collection of **features**. Until a few exist, you
have no information to decide the shell from. That is why the shell is frustrating.

**Practice**: start from one real feature. For flight search, build only what it
needs: origin, destination, depart date, return date, a search button. Many products
end up needing no navigation at all.

## §1.2 Detail comes later

Skip typefaces, shadows and icons early. Use the **Sharpie test**: sketch with a fat
marker, which physically prevents detail work, so you compare layouts fast.

**§1.2.1 Hold the color.** Design in grayscale and force spacing, contrast and size to
carry the screen. Harder, but the result is cleaner, and adding color afterward is
easy.

**§1.2.2 Don't over-invest.** Sketches and wireframes are disposable. They exist to
explore, and get thrown away once the decision is made. A static mockup has no value
to users.

## §1.3 Don't design too much

Don't design every feature and edge case up front. "What if the user has 2,000
contacts", "where does the error message go", "how do two overlapping meetings look" —
reasoning about these from imagination is self-inflicted pain. Fixing them in a
working interface is much easier.

**§1.3.1 Work in cycles.** Simple design → build it → iterate on the working thing →
switch back to design for the next feature. Ship something real early so you are not
carrying the whole thing in your head.

**§1.3.2 Be a pessimist.** Never imply functionality you are not ready to build. The
canonical failure: you know attachments are coming, so you draw an attachment area on
day one; the real work turns out to be much larger, the whole comment feature gets
shelved, and a comment system without attachments — which would have shipped — never
exists. **Design the smallest shippable version**; "nice to have" parts get designed
later.

## §1.4 Choose a personality

Personality sounds vague but is set by concrete factors.

| Factor | Choice | Reads as |
|---|---|---|
| §1.4.1 Typeface | Serif | Elegant, classic |
| | Rounded sans | Playful, friendly |
| | Neutral sans | Plain; lets other elements carry the character |
| §1.4.2 Color | Blue | Safe, familiar — nobody complains about blue |
| | Gold | Expensive, sophisticated |
| | Pink | Fun, not serious |
| §1.4.3 Radius | Small | Neutral |
| | Large | Playful |
| | None | Serious, formal |

**§1.4.3 Keep radius consistent.** Mixing square and rounded corners in one interface
is almost always worse than committing to either.

**§1.4.4 Language.** Interfaces are full of words; word choice shapes personality as
much as color or type. Formal copy reads official and professional; casual copy reads
friendly.

**§1.4.5 Decide what you actually want.** With no instinct to go on, look at the sites
your audience already uses. But don't borrow heavily from direct competitors — you do
not want to look like the cheap version of someone else.

## §1.5 Limit your choices

Millions of colors and thousands of typefaces are, in practice, a **decision paralysis
curse**. "12px or 13px?" "Shadow at 10% or 15%?" "Avatar 24px or 25px?" When every
option is acceptable, you have no basis for deciding quickly.

**§1.5.1 Define systems in advance.** Instead of opening a color picker for every new
shade, pick from 8–10 pre-chosen shades. Instead of nudging font sizes pixel by pixel,
define a restricted type scale first. The unpleasant work of choosing initial values
happens **once**.

**§1.5.2 Design by elimination.** With a system, choosing becomes comparing. Guess a
value (16px), then place its neighbours (12px, 24px) beside it. Usually two of the
three are obviously wrong; if the outer ones are out, the middle is the answer. If an
outer one wins, treat it as the new middle and compare again.

**§1.5.3 Systematize everything.** Systems are needed for: font size, font weight, line
height, color, margin, padding, width, height, box shadow, border radius, border width,
opacity — and anything else you keep agonizing over.

You need not define them all up front, but keep the systemic mindset: every new
decision is a chance to introduce a system, and no small decision should be made
twice.
