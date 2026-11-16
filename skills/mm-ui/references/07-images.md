# §7 · Working with Images

14 rules (§7.1–§7.4.2). The sixth lens.

## §7.1 Use good photos

**Symptom**: everything else is fine, but the photos are bad and the design collapses.

**Practice**, two options only: hire a professional for specific shots (good photography
is lighting, composition and color — not the camera), or use quality stock (Unsplash is
free and good).

**Never design with placeholders intending to replace them with phone snapshots later.**
That never works.

## §7.2 Text needs consistent contrast

**Symptom**: a headline over a large image is unreadable whatever color you make it.

**Mechanism**: the problem is the image, not the text. Photos have a wide dynamic range —
light text works in the dark areas and vanishes in the bright ones; dark text does the
opposite.

**§7.2.1 Background images.** **Reduce the image's dynamic range** so the text/background
contrast is stable across the whole area.

**§7.2.2 Add an overlay.** Semi-transparent black tones down bright areas for light text;
semi-transparent white brightens dark areas for dark text. Cost: the whole image is
adjusted, not just the problem regions.

**§7.2.3 Lower the image contrast.** More controllable than an overlay, because it changes
the image itself. Adjust brightness afterward to compensate.

**§7.2.4 Colorize the image.** Three steps: lower contrast → desaturate → overlay a solid
fill in `multiply` mode. It also brings photography in line with the brand color.

**§7.2.5 Add a text shadow.** For preserving more of the image's range. What you want is a
**glow, not a shadow**: large blur radius, **no offset**. Still reduce image contrast, just
less.

## §7.3 Everything has an intended size

Upscaling bitmaps is obviously bad, but scaling has more failure modes.

**§7.3.1 Don't scale up icons.** Vectors don't degrade, but icons drawn at 16–24px look
chunky and detail-poor at 3–4×. If small icons are all you have, **enclose the icon at its
intended size inside a larger shape with a background color** — the icon stays near the
size it was drawn for while filling a bigger space.

**§7.3.2 Don't scale down screenshots.** A full-size screenshot at 70% turns 16px text into
4px. Instead: screenshot at a smaller viewport (tablet layout), take a partial screenshot,
or draw a simplified interface with lines where the text was.

**§7.3.3 Don't scale down icons either.** Icons drawn large turn to mush when shrunk, and
favicons are the worst case — a 128px logo forced into 16px makes the browser cram detail
into nothing. **Redraw a simplified version at the target size.**

## §7.4 Beware user-uploaded content

Contrast, color and crop are out of your control. Two things remain.

**§7.4.1 Control shape and size.** Native aspect ratios wreck layouts, especially with
several images on screen. Center the image in a fixed-size container and crop the overflow
— in CSS, a background image with `background-size: cover`.

**§7.4.2 Prevent background bleed.** When a user's image background matches the
interface's, the image loses its shape. Don't use a border (it clashes with colors inside
the image); use a **subtle inner shadow** — most people never notice it — or a
semi-transparent inner border.
