# Antipatterns

Symptom → rule id → fix. Check here first when auditing: a hit gives you the rule id
without sweeping the lens files.

Rows are drawn from all chapters; the file carries no coverage obligation (see
`00-coverage.md`).

## Hierarchy

| Symptom | Rule | Fix |
|---|---|---|
| Every element has nearly the same size and weight | §2.1 §2.2 | Rank content primary/secondary/tertiary, then express it with weight and color |
| Hierarchy is carried by font size alone; primary huge, secondary unreadable | §2.2 | Return to sane sizes; use 400/500 vs 600/700 and three text colors |
| Grey text on a colored background looks muddy | §2.3 | Hand-pick a same-hue, low-contrast color; no grey, no opacity |
| `opacity: .6` used to de-emphasize text | §2.3.a | Text looks washed out or disabled, patterns bleed through; pick a color |
| A row of equally heavy buttons | §2.8 | One primary (solid), a few secondary (outline), the rest tertiary (link) |
| Delete button is large, red and bold by default | §2.8.1 | Demote it; the loud treatment belongs in the confirmation step |
| Every datum rendered as `Label: value` | §2.5 | Drop the label when format or context carries it; keep it small and light when needed |
| `h1` used for a section title, so it dominates | §2.6 | Choose elements semantically, size them by hierarchy; section titles are usually small |

## Spacing and layout

| Symptom | Rule | Fix |
|---|---|---|
| Everything feels cramped, elements barely breathe | §3.1 | Start with too much space, then subtract |
| 16px used everywhere; padding and margin indistinguishable | §3.2 §3.6 | Take values from the scale; spacing around a group must exceed spacing within |
| Nothing is obviously misaligned but something feels off | §3.2 | Values are off-scale; pull them back onto the scale |
| Form labels and the next field are equally spaced | §3.6 | Increase the gap between groups so within-group spacing is clearly smaller |
| 600px of content spread across a 1400px canvas | §3.3 | Constrain the width; leave the rest as space |
| A card is wider on a laptop than on a large monitor | §3.4.2 | Give it a max-width and shrink only below it |
| Sidebar stretches with the window and its contents look wrong | §3.4.1 | Fix the sidebar width for its contents; let the main area flex |
| List items read as two lines each | §3.6.a | Item spacing must exceed line-height |

## Typography

| Symptom | Rule | Fix |
|---|---|---|
| Sizes 13 / 15 / 17 / 19 all appear | §4.1 | Move to the scale (12 14 16 18 20 24 30 36 48 60 72) |
| Lines run 120+ characters on a wide screen | §4.3 | Constrain paragraphs to 20–35em |
| Line-height is 1.5 everywhere | §4.5 | Wider lines need more (up to 2); larger sizes need less (headlines can be 1) |
| Large headlines at 1.5 look loose | §4.5.2 | Drop headline line-height to 1–1.1 |
| All-caps labels are cramped | §4.8.2 | Add letter-spacing |
| Nested em sizes land off-scale | §4.1.2 | Use px or rem |
| Table numbers are left-aligned and hard to compare | §4.7.2 | Right-align, decimals aligned |
| Long paragraphs centered; the eye keeps losing the start of the line | §4.7.1 | Left-align past 2–3 lines; prefer shortening the copy |
| Mixed sizes on one line, vertically centered, look wrong | §4.4 | Align on the baseline |

## Color

| Symptom | Rule | Fix |
|---|---|---|
| Instantly reads as machine-made: indigo primary, gray neutral | hard gate | Use the project's tokens; if there are none, ask — never default to indigo/gray |
| Shades produced by `lighten()` / `darken()`, 35 near-identical blues | §5.3 | Define 5–10 fixed shades up front and pick from them |
| Five color values total; nothing can be built | §5.2 | 8–10 greys, 5–10 primary shades, plus accents and semantic colors |
| Light shades look washed out; the color stops being a color | §5.4 | Raise saturation as lightness leaves 50%, or rotate the hue (≤20–30°) |
| Grey text on a grey background, contrast too low | §5.6 | Measure 4.5:1 (body) / 3:1 (large) |
| White on a colored background as the primary button; the block dominates | §5.6.1 | Invert to dark text on a light background |
| Status conveyed by red/green alone | §5.7 | Add an icon, direction or label; separate chart series by contrast |

## Depth

| Symptom | Rule | Fix |
|---|---|---|
| Shadows are dark and blurry; the screen looks dirty | §6.1.2 | Small, dark, vertically offset, a couple of pixels of blur, sharp edges |
| Every card and section carries a shadow | §6.2 | Assign by z-position; siblings usually need none |
| The lighter edge uses semi-transparent white and desaturates the surface | §6.1.2 | Hand-pick a lighter color at the same hue |
| Inputs are perfectly flat and don't look editable | §6.1.3 | Inset: lighter bottom edge plus a small dark inset shadow at the top |
| Modals and dropdowns use the same shadow weight | §6.2.a | Five-step elevation: buttons small, dropdowns medium, modals large |

## Images and finishing

| Symptom | Rule | Fix |
|---|---|---|
| Placeholder images shipped | §7.1 | Use real photos or quality stock; don't plan on swapping later |
| Text sits directly on a photo and disappears in places | §7.2 | Lower image contrast / overlay / colorize / text glow (large blur, no offset) |
| 16px icons scaled to 64px as feature icons | §7.3.1 | Keep the icon at its drawn size and enclose it in a larger colored shape |
| A full-page screenshot shrunk into a card; text is 4px | §7.3.2 | Screenshot at a smaller viewport, crop, or draw a simplified UI |
| User avatars in native aspect ratio break the layout | §7.4.1 | Fixed container, centered, cropped (`background-size: cover`) |
| A user image whose background matches the page loses its shape | §7.4.2 | Inner shadow or semi-transparent inner border, never a solid border |
| A new feature opens to a blank screen | §8.4 | Design the empty state: illustration, prominent CTA, hide the non-functional tabs and filters |
| Every section is outlined with a border | §8.5 | Use background difference, shadow or spacing first; borders are the last resort |
| Structure is fine but the result feels flat | §8.1 §8.2 | Icons as bullets, custom links and checkboxes, accent borders — don't redesign |
