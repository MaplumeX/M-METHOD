# §6 · Creating Depth

17 rules (§6.1–§6.5.1). The fifth lens. **"Dirty shadows, floating cards, input fields
that look like stickers" all live here** — depth follows one physical rule, not a pile
of effects.

## §6.1 Emulate a light source

**Mechanism**: raised and inset are distinguished by a single rule — **light comes from
above**.

**§6.1.1 Light comes from above**:

- Raised: the top edge faces the sky → lighter; the bottom edge faces away → darker.
- Inset: the top edge is shadowed by the lip above it; the bottom edge faces the sky →
  lighter.

**§6.1.2 Raised elements.** Both flat edges cannot be visible at once. People look
slightly downward, so **reveal the top edge and hide the bottom**.

- Lighter top: an upper border, or an inset shadow with a slight vertical offset.
- **Hand-pick the lighter color; do not overlay semi-transparent white** — the overlay
  desaturates the underlying color.
- The element blocks some light, so the area below it darkens: a small, dark,
  vertically-offset shadow. **The blur is only a couple of pixels and the edges should
  stay sharp** — look at the shadow a wall socket casts.

**§6.1.3 Inset elements.** Only the bottom lip is visible, so:

- Lighter bottom: a lower border, or an inset shadow with a **negative** vertical offset.
- The top is shadowed: a small, dark inset shadow with a **positive** vertical offset,
  and make sure it does not leak out the bottom.

Inputs and checkboxes use exactly this.

**§6.1.4 Don't get carried away.** Borrowing cues from the real world is good; chasing
photo-realism makes interfaces busy and unclear.

## §6.2 Shadows convey elevation

Shadows place elements on a virtual z-axis: **tight blur = slightly raised, large blur =
close to the user**. Closer grabs more attention.

**§6.2.a The three canonical uses**: small = buttons (noticed, not dominant); medium =
dropdowns; large = modals.

**§6.2.1 Establish an elevation system.** Five steps is plenty. Define the smallest and
largest, fill the middle roughly linearly:

```
0 1px 3px          0 4px 6px          0 5px 15px
0 10px 24px        0 15px 35px        (all hsla(0,0%,0%,.2))
```

**§6.2.2 Shadows and interaction.** Give a dragged list item a shadow while it is held —
it lifts off the list and signals that it can move. Pressing a button shrinks or removes
its shadow, as if pushed in.

**Choose a shadow by asking where the element should sit on the z-axis, not by how the
shadow looks.**

## §6.3 Shadows can have two parts

**Mechanism**: the best-looking shadows are usually two layers, each doing a distinct
job — not experimentation until it looks right.

**§6.3.a The two jobs**:

1. **Larger and softer**: significant vertical offset, large blur → the cast shadow from
   a direct light source.
2. **Tighter and darker**: small offset, small blur → the ambient-occlusion band
   directly beneath the object.

Together they are far more controllable than one layer: the large shadow stays soft while
the edge nearest the element stays crisp.

**§6.3.1 Accounting for elevation.** The tighter the object sits to the surface, the more
visible that ambient band. At the lowest elevation it is quite distinct; at the highest it
is almost or completely invisible.

## §6.4 Even flat designs can have depth

Flat means no shadows or gradients — not an absence of depth.

**§6.4.1 Creating depth with color.** Within one hue: lighter than the background reads as
raised, darker reads as inset. This works in non-flat designs too.

**§6.4.2 Using solid shadows.** Short, vertically offset only, **zero blur**. It lifts a
card or button slightly while keeping the flat aesthetic.

## §6.5 Overlap elements to create layers

**Practice**, any of:

- Offset a card so it crosses the boundary between two background colors, instead of
  nesting it fully inside a container.
- Make an element taller than its parent so it overlaps on both sides.
- Use it on small controls too: carousel arrows riding the edge of an image.

**§6.5.1 Overlapping images.** Overlapping images fight each other. Give each an
**invisible border** matching the background color, so there is always a gap. The layering
survives and the clash disappears.
