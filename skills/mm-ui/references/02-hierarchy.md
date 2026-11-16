# §2 · Hierarchy is Everything

20 rules (§2.1–§2.8.1). The first lens when auditing: **most "this looks off" complaints
are resolved here**, without touching color, type or layout.

## §2.1 Not all elements are equal

**Symptom**: everything competes for attention; the screen reads as a wall of text with
no visible priority.

**Mechanism**: visual hierarchy is how important each element appears relative to the
others. It is the highest-leverage tool for making something feel designed, and it is
independent of color scheme, typeface and layout.

**Practice**: rank the content primary / secondary / tertiary, and the actions one
primary / a few secondary / several tertiary. Ranking comes before styling.

## §2.2 Size isn't everything

**Symptom**: primary text keeps getting larger and secondary text smaller, and the
screen still reads flat.

**Mechanism**: font size moves one dimension, and overusing it damages both ends —
primary content too large, secondary unreadable.

**Practice**: use weight and color instead.

- **§2.2.a Three text colors**: dark = primary, grey = secondary, lighter grey =
  tertiary.
- **§2.2.b Two font weights**: 400/500 normal, 600/700 emphasis. **Never go below 400**
  for UI text — light weights work in huge headlines and fail at small sizes. To
  de-emphasize, use a lighter color or a smaller size.

## §2.3 Don't use grey text on colored backgrounds

**Symptom**: grey text that works on white looks muddy and dull on a colored surface.

**Mechanism**: on white, the thing that actually does the work is **reduced contrast**,
not greyness.

**Practice**: don't use grey, and don't lower white's opacity.

- **§2.3.a Why not opacity**: white at reduced opacity does lower contrast, but text
  looks washed out and sometimes disabled; over patterns or images the background shows
  through it.
- Instead, **hand-pick a color at the background's hue**, adjusting saturation and
  lightness until the contrast is low enough without the text going grey.

## §2.4 Emphasize by de-emphasizing

**Symptom**: the primary element refuses to stand out, and there is nothing louder to
add.

**Mechanism**: hierarchy is relative. Strengthening A and softening A's competitors have
the same effect, and the second usually looks better.

**Practice**: weaken what competes. When the active nav item is not prominent enough,
fade the inactive ones further.

**§2.4.a Applies at section scale.** If the sidebar competes with the main area, don't
restyle its contents — remove its background so the content sits on the page.

## §2.5 Labels are a last resort

**Symptom**: data laid out as `label: value`, giving every datum equal weight and no
hierarchy at all.

**§2.5.1 You might not need a label at all.** Format speaks: `janedoe@example.com` is
an email, `(555) 765-4321` a phone number, `$19.99` a price. When format is ambiguous,
context usually carries it — "Customer Support" under a name in a directory needs no
label.

**§2.5.2 Combine labels and values.** "12 left in stock" beats "In stock: 12"; "3
bedrooms" beats "Bedrooms: 3". Once merged, styling each datum meaningfully becomes
easy without losing clarity.

**§2.5.3 Labels are secondary.** When a label is genuinely needed (many similar items,
fast scanning, dashboards), treat it as supporting content: smaller, lower contrast,
lighter weight, or all three.

**§2.5.4 When to emphasize a label.** Invert only when the user is scanning **for the
label** — on a spec sheet people look for "depth", not "7.6mm". Then labels take the
darker color and values sit slightly lighter; don't bury the value.

## §2.6 Separate visual hierarchy from document hierarchy

**Symptom**: an `h1` used for "Manage Account" ends up enormous, because "h1 is
supposed to be big", and it steals the page.

**Mechanism**: `h1`–`h6` are document-structure decisions, and browsers bind them to
size, which lures you into bad choices in app UI.

**Practice**: choose elements semantically, style them for hierarchy. Section titles
usually behave as **labels** — they serve the content and should be quite small. In the
extreme, keep the heading in the markup for accessibility and hide it visually.

## §2.7 Balance weight and contrast

**Mechanism**: emphasis tracks **surface area**. Bold text occupies more pixels in the
same space, so it reads heavier.

**§2.7.1 Contrast compensates for weight.** Icons — especially solid ones — are heavy
and you cannot change their weight. Darkening the adjacent text won't help; give the
icon a softer color instead. Lowering contrast is a counterweight.

**§2.7.2 Weight compensates for contrast.** When a 1px border in a soft color is too
subtle but a darker color makes the design harsh, thicken the border.

## §2.8 Semantics are secondary

**Symptom**: every action styled the same because every action is semantically an
action; a row of equally heavy buttons.

**Mechanism**: actions sit in a pyramid of importance. Most screens have exactly one
primary action.

**§2.8.a The three treatments**:

- Primary: solid, high-contrast fill — visible at a glance.
- Secondary: outline or a lower-contrast fill — clear but not competing.
- Tertiary: styled as a link — discoverable without interrupting.

**§2.8.1 Destructive actions.** Severity is not prominence. A destructive action is
usually not the screen's primary action; treat it as secondary or tertiary and save the
loud treatment **for the confirmation step**, where it genuinely is primary.
