# §5 · Working with Color

22 rules (§5.1–§5.7). The fourth lens. **"The palette looks cheap" is almost always
one of three things**: too few colors, shades computed on the fly, contrast never
measured.

## §5.1 Ditch hex for HSL

**Symptom**: two visually close colors look unrelated in code, so you cannot reason that
"this one is slightly lighter than that one".

**Mechanism**: HSL describes color with the three properties the eye actually reads.

**§5.1.a The three components**:

- Hue is position on the wheel: 0° red, 120° green, 240° blue. It is what lets us call
  two different colors "blue".
- Saturation: 0% is grey (no color), 100% is vivid. **At 0% saturation hue is
  meaningless.**
- Lightness: 0% black, 100% white, 50% the purest version of that hue.

**§5.1.1 HSL vs HSB.** In HSB, 0% brightness is always black and 100% brightness is only
white at 0% saturation. HSB 100% brightness at 100% saturation equals HSL 100%
saturation at **50% lightness**. Design tools favour HSB; browsers only accept HSL.

## §5.2 You need more colors than you think

**Symptom**: a palette generator hands you five "perfect" colors and you can build
nothing with them.

**Mechanism**: a real interface needs a set of shades to choose from.

**§5.2.1 Greys.** Text, backgrounds, panels, form controls — almost everything is grey.
Three or four shades sounds sufficient until you want "slightly darker than 2, slightly
lighter than 3". **8–10 shades**: enough not to compromise, not so many that you waste
time between 77 and 78. **Start from a very dark grey, not true black** — pure black
reads as unnatural.

**§5.2.2 Primary color(s).** One, maybe two, for primary actions and active nav. It sets
the overall feel. **5–10 shades**: ultra-light ones for tinted backgrounds, dark ones for
text.

**§5.2.3 Accent colors.** Attention colors (yellow, pink, teal) plus semantic states
(red destructive, yellow warning, green positive). More when color must categorize items
(chart lines, calendar events, tags). A complex interface reaching **10 colors × 5–10
shades** is not unusual.

## §5.3 Define shades up front

**Symptom**: `lighten()` / `darken()` on demand, ending with 35 nearly identical blues
that look the same.

**Practice**: define a fixed set of shades in advance and pick from it.

**§5.3.1 Choose the base color first.** Take the middle shade. There is no real science
here; for primary and accent colors the rule of thumb is **a shade that works well as a
button background**. There is no "start at 50% lightness" rule — each hue behaves
differently.

**§5.3.2 Find the edges.** Think about where they will be used: the darkest shade usually
carries text, the lightest usually tints an element's background. An alert component
exercises both ends at once, which makes it a good test. Keep the base hue, adjust
saturation and lightness.

**§5.3.3 Fill in the gaps.** At least 5 shades, closer to 10 to avoid feeling
restricted. Nine divides cleanly: darkest **900**, base **500**, lightest **100** → add
**700 / 300** (each the midpoint of its gap) → then **800 / 600 / 400 / 200**.

**§5.3.4 What about greys.** Same procedure; the base matters less. Darkest = suitable
for the darkest text; lightest = suitable for a subtle off-white background.

**§5.3.5 It's not a science.** The systematic approach is a good start, and in practice
you will tweak saturation and lightness. Trust your eyes over the numbers. **But resist
adding new shades** — a palette you don't restrict is a palette you didn't need.

## §5.4 Lightness kills saturation

**Mechanism**: the closer lightness is to 0% or 100%, the weaker saturation's influence.
The same saturation looks more colorful at 50% lightness than at 90%.

**Practice**: **raise saturation as lightness moves away from 50%**, or the light and
dark shades look washed out. If the base is already 100% saturated, see below.

**§5.4.1 Use perceived brightness.** Yellow and blue can share HSL lightness while yellow
looks brighter.

```
perceived brightness = √(0.299r² + 0.587g² + 0.114b²) / 255
```

Sampling the wheel at 100% saturation and 50% lightness shows three local minima (red,
green, blue) and three maxima (yellow, cyan, magenta) — **not a linear distribution**.

**§5.4.2 Change brightness by rotating the hue.** Adjusting lightness costs intensity:
the color moves toward white or black rather than simply getting lighter or darker.

- To lighten, rotate toward the nearest bright hue: **60° / 180° / 300°**.
- To darken, rotate toward the nearest dark hue: **0° / 120° / 240°**.

Especially useful for light hues like yellow: rotate toward orange as lightness drops and
the dark shades stay warm and rich instead of turning muddy brown. Combine with lightness
adjustment freely, but **never rotate more than 20–30°**, or it becomes a different color.

## §5.5 Greys don't have to be grey

A true grey is 0% saturation, but many colors we read as grey are noticeably saturated —
which is what makes one grey feel cool and another warm.

**§5.5.1 Color temperature.** Add blue for cool, yellow or orange for warm. **Raise
saturation at both ends of the ramp too**, otherwise the extremes look washed out
compared to shades near 50% lightness. How much is a judgement call: a slight tint, or a
whole interface leaning clearly warm or cool.

## §5.6 Accessible doesn't have to mean ugly

WCAG: **4.5:1 for body text (under about 18px), 3:1 for large text.**

Dark-on-light is easy; anything colored gets harder.

**§5.6.1 Flip the contrast.** White text on a colored background often needs a
surprisingly dark background to reach 4.5:1. When those elements are not meant to be the
focus, that dark block grabs all the attention. Fix: **light background with dark text** —
the color is still there, still supporting the text, without competing.

**§5.6.2 Rotate the hue.** Colored text on a colored background (secondary text inside a
dark panel) is hardest. Adjusting only lightness and saturation climbs toward pure white,
and you don't want secondary text to look like primary. Rotate the hue **toward a
brighter hue** (cyan, magenta, yellow) to gain contrast without approaching white.

## §5.7 Don't rely on color alone

Red-green colorblind users cannot read a pure color signal; a red down arrow on a metric
card is invisible to them.

**Practice**:

- Add a supporting signal — icon, direction, text label. Color supports a message the
  design already carries; it never carries one alone.
- For multi-series charts, differentiate by **contrast** rather than unrelated hues.
  Judging light from dark is far easier than judging two hues.

## Color weight & surface proportions (extension)

Defining compliant 9-step ramps does not automatically balance how much area each color occupies on screen. Plan **color weight** deliberately before applying Pass 2 accents:

- **70 / 25 / 5 surface budget** (or 60 / 30 / 10 on expressive marketing surfaces):
  - **~70% quiet neutral canvas** (`--surface`, off-white or deep near-black neutral);
  - **~25% secondary structural surfaces & typography** (`--surface-raised`, `--surface-sunken`, `--border`, `--text*`);
  - **~5% high-intent accent** (`--accent`, `--status-*`) reserved strictly for the primary action, active navigation indicator, and true status signals.
- **Restrained atmospheric treatment**: if using subtle surface warmth or gradients (`§8.3.1`, hues `≤ 30°` apart), confine them to the canvas backdrop or hero band — never saturate every card or container simultaneously.
