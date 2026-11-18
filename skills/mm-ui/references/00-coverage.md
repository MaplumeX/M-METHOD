# Coverage

The authoritative inventory of *Refactoring UI*: **50 top-level rules + 101 sub-points
= 151 items**. A reference file is not done until every row assigned to it is marked
`done`.

- `HV` = carries hard values that must survive verbatim (no rounding, no "simplifying").
- Status: `done` · `todo` · `omitted` (an omission needs a stated reason in the file).
- `§n.n` is a top-level rule, `§n.n.n` a sub-point, `§n.n.a` a point stated only in body
  prose and absent from the book's table of contents.

Sources and licences: [ATTRIBUTION.md](../ATTRIBUTION.md).

## Ch 1 · Starting from Scratch → `01-starting.md`

| ID | Book section | Core assertion | HV | Status |
|---|---|---|---|---|
| 1.1 | Start with a feature, not a layout | Design a real piece of functionality first; the shell cannot be decided before features exist | | done |
| 1.2 | Detail comes later | Defer typefaces, shadows and icons during exploration; low fidelity on purpose | | done |
| 1.2.1 | Hold the color | Design in grayscale first so spacing, contrast and size carry the hierarchy | | done |
| 1.2.2 | Don't over-invest | Sketches are disposable; abandon them once the decision is made | | done |
| 1.3 | Don't design too much | Don't design every feature and edge case up front | | done |
| 1.3.1 | Work in cycles | Design simple → build real → iterate on the working thing → return to design | | done |
| 1.3.2 | Be a pessimist | Never imply functionality you are not ready to build; design the smallest shippable version | | done |
| 1.4 | Choose a personality | Personality comes from concrete factors, not vibes | | done |
| 1.4.1 | Font choice | Serif = elegant; rounded sans = playful; neutral sans = plain | | done |
| 1.4.2 | Color | Blue = safe; gold = expensive; pink = fun, not serious | | done |
| 1.4.3 | Border radius | Small = neutral; large = playful; none = formal. Must be consistent — never mix | | done |
| 1.4.4 | Language | Word choice drives personality as much as any visual property | | done |
| 1.4.5 | Deciding what you actually want | Look at sites your audience already uses; don't copy direct competitors | | done |
| 1.5 | Limit your choices | Unconstrained choice is paralysis; near-identical options cannot be decided between | HV | done |
| 1.5.1 | Define systems in advance | Pick 8–10 shades and a restrictive type scale ahead of time, not per decision | HV | done |
| 1.5.2 | Designing by elimination | Guess the middle, test the neighbours; re-center if an outer value wins | | done |
| 1.5.3 | Systematize everything | Type size, weight, line height, color, margin, padding, width, height, shadow, radius, border width, opacity | HV | done |

## Ch 2 · Hierarchy is Everything → `02-hierarchy.md`

| ID | Book section | Core assertion | HV | Status |
|---|---|---|---|---|
| 2.1 | Not all elements are equal | Visual hierarchy is the highest-leverage tool for making something feel designed; independent of color, font and layout | | done |
| 2.2 | Size isn't everything | Over-relying on size produces oversized primary and undersized secondary content; use weight and color | HV | done |
| 2.2.a | Three text colors | Dark = primary, grey = secondary, lighter grey = tertiary | HV | done |
| 2.2.b | Two font weights | 400/500 normal, 600/700 emphasis; never below 400 for UI text | HV | done |
| 2.3 | Don't use grey text on colored backgrounds | The mechanism is reduced contrast, not greyness; hand-pick a same-hue color with adjusted S/L | | done |
| 2.3.a | Why not opacity | White at lower opacity looks washed out and lets patterned backgrounds bleed through | | done |
| 2.4 | Emphasize by de-emphasizing | Soften the competitors instead of amplifying the primary element | | done |
| 2.4.a | Applies at section scale | A competing sidebar is fixed by removing its background, not by restyling its content | | done |
| 2.5 | Labels are a last resort | Naive `label: value` gives every datum equal emphasis and blocks hierarchy | | done |
| 2.5.1 | You might not need a label at all | Format (email, phone, price) or context often identifies the data | | done |
| 2.5.2 | Combine labels and values | "12 left in stock" over "In stock: 12"; "3 bedrooms" over "Bedrooms: 3" | | done |
| 2.5.3 | Labels are secondary | De-emphasize: smaller, lower contrast, lighter weight, or a combination | | done |
| 2.5.4 | When to emphasize a label | Only when the user scans for the label (spec tables); keep the value close behind | | done |
| 2.6 | Separate visual from document hierarchy | Choose elements semantically, style them for hierarchy; section titles usually behave as labels | | done |
| 2.7 | Balance weight and contrast | Emphasis tracks surface area — bold text covers more pixels in the same space | | done |
| 2.7.1 | Contrast compensates for weight | Icons are heavy and cannot change weight; lower their contrast | | done |
| 2.7.2 | Weight compensates for contrast | A 1px border too subtle and a darker color too harsh: thicken the border | | done |
| 2.8 | Semantics are secondary | One primary action, a couple of secondary, a few tertiary | | done |
| 2.8.a | The three treatments | Primary = solid fill; secondary = outline or low-contrast fill; tertiary = link-styled | | done |
| 2.8.1 | Destructive actions | Severity is not prominence; demote, then use the loud treatment inside the confirmation step | | done |

## Ch 3 · Layout and Spacing → `03-spacing.md`

| ID | Book section | Core assertion | HV | Status |
|---|---|---|---|---|
| 3.1 | Start with too much white space | Extra breathing room is the cheapest cleanup available | | done |
| 3.1.1 | Remove, don't add | Adding until it stops looking bad always undershoots; start excessive and subtract | | done |
| 3.1.2 | Dense UIs have their place | Density must be a deliberate decision, not the default | | done |
| 3.2 | Establish a spacing and sizing system | Never nitpick 120px against 125px; choose from a fixed set | | done |
| 3.2.1 | A linear scale won't work | Multiples of 4px don't help; no two adjacent values closer than ~25% | HV | done |
| 3.2.2 | Defining the system | Base 16px, tight at the low end: 4, 8, 12, 16, 24, 32, 48, 64, 96, 128, 192, 256, 384, 512, 640, 768 | HV | done |
| 3.2.3 | Using the system | Pick from the scale; the next value up is usually right | | done |
| 3.3 | You don't have to fill the screen | Canvas is not an obligation; 600px content stays 600px | HV | done |
| 3.3.1 | Shrink the canvas | Design the mobile layout first on a ~400px canvas, then adapt upward | HV | done |
| 3.3.2 | Think in columns | Split into columns rather than widening past the optimal width | | done |
| 3.3.3 | Don't force it | Use the space when the content needs it | | done |
| 3.4 | Grids are overrated | A grid is constrained percentage widths; outsourcing every decision to it backfires | HV | done |
| 3.4.1 | Not all elements should be fluid | Sidebars want a fixed width; the main area flexes and runs its own grid | HV | done |
| 3.4.2 | Don't shrink until you need to | Give a max-width and shrink only below it | HV | done |
| 3.5 | Relative sizing doesn't scale | Large elements must shrink faster than small ones | HV | done |
| 3.5.1 | Relationships within elements | Button padding shouldn't be em-derived; large buttons want disproportionately generous padding | HV | done |
| 3.6 | Avoid ambiguous spacing | Space around a group must exceed space within it, vertically and horizontally | | done |
| 3.6.a | The four manifestations | Form label/input; heading above a section; list items against line-height; horizontal groups | | done |

## Ch 4 · Designing Text → `04-typography.md`

| ID | Book section | Core assertion | HV | Status |
|---|---|---|---|---|
| 4.1 | Establish a type scale | Unsystematic sizes cause inconsistency and slow the workflow | | done |
| 4.1.1 | Choosing a scale | A linear scale fails here too; small jumps matter at the bottom | | done |
| 4.1.1a | Modular scales | 4:5 major third, 2:3 perfect fifth, 1:1.618 golden; compounded from 16px | HV | done |
| 4.1.1b | You end up with fractions | 31.25 / 39.063 / 48.828px; round manually if used | HV | done |
| 4.1.1c | You usually need more sizes | Rounded 3:4 gives 12/16/21/28; you will want values between them | HV | done |
| 4.1.1d | Hand-crafted scales | 12, 14, 16, 18, 20, 24, 30, 36, 48, 60, 72 | HV | done |
| 4.1.2 | Avoid em units | em compounds in nested elements; use px or rem | HV | done |
| 4.2 | Use good fonts | Judging typefaces takes years; use shortcuts meanwhile | | done |
| 4.2.1 | Play it safe | Neutral sans; `-apple-system, Segoe UI, Roboto, Noto Sans, Ubuntu, Cantarell, Helvetica Neue` | HV | done |
| 4.2.2 | Ignore faces with fewer than five weights | Filter to 10+ styles; removes ~85% of Google Fonts | HV | done |
| 4.2.3 | Optimize for legibility | Headline faces: tight spacing, short x-height; text faces: wider spacing, tall x-height | | done |
| 4.2.4 | Trust the wisdom of the crowd | Sort by popularity; especially useful for a serif with personality | | done |
| 4.2.5 | Steal from people who care | Inspect typefaces on sites you admire | | done |
| 4.2.6 | Develop your intuition | Taste accrues from deliberate attention | | done |
| 4.3 | Keep line length in check | 45–75 characters; on the web 20–35em; past 75 is risky | HV | done |
| 4.3.1 | Wider content | Constrain paragraph width even when the container must be wider | | done |
| 4.4 | Baseline, not center | Align mixed sizes on the baseline; the mismatch shows most when text is close together | | done |
| 4.5 | Line-height is proportional | The 1.5 rule of thumb is not universal | HV | done |
| 4.5.1 | Accounting for line length | Proportional: narrow ≈1.5, wide up to 2 | HV | done |
| 4.5.2 | Accounting for font size | Inversely proportional; large headlines can sit at 1 | HV | done |
| 4.6 | Not every link needs a color | Use weight or a darker color; reveal underline on hover for ancillary links | | done |
| 4.7 | Align with readability in mind | Follow the language direction | | done |
| 4.7.1 | Don't center long form text | Past 2–3 lines, left-align; prefer rewriting shorter | HV | done |
| 4.7.2 | Right-align numbers | Aligned decimal positions make columns comparable | | done |
| 4.7.3 | Hyphenate justified text | Justification without hyphenation creates word gaps | | done |
| 4.8 | Use letter-spacing effectively | Default: trust the type designer | | done |
| 4.8.1 | Tightening headlines | Tighten a text-optimised family used for headlines; never loosen a headline face for small sizes | | done |
| 4.8.2 | Improving all-caps legibility | Lowercase has x-height and ascender/descender variety; all-caps does not, so add spacing | | done |

## Ch 5 · Working with Color → `05-color.md`

| ID | Book section | Core assertion | HV | Status |
|---|---|---|---|---|
| 5.1 | Ditch hex for HSL | Hex and RGB make visually related colors look unrelated in code | | done |
| 5.1.a | The three components | Hue 0° red / 120° green / 240° blue; saturation 0% grey to 100% vivid; lightness 0% black, 100% white, 50% pure | HV | done |
| 5.1.1 | HSL vs HSB | HSB 100% brightness at 100% saturation equals HSL 50% lightness; tools favour HSB, browsers take HSL | HV | done |
| 5.2 | You need more colors than you think | Five-hex palette generators cannot build a real interface | | done |
| 5.2.1 | Greys | 8–10 shades; start from a very dark grey, never true black | HV | done |
| 5.2.2 | Primary color(s) | One, maybe two; 5–10 shades; ultra-light for tinted backgrounds, dark for text | HV | done |
| 5.2.3 | Accent colors | Attention colors plus semantic states; up to ~10 colors × 5–10 shades in a complex UI | HV | done |
| 5.3 | Define shades up front | Never generate with lighten()/darken(); that is how you get 35 near-identical blues | | done |
| 5.3.1 | Choose the base color first | The middle shade; something that works as a button background. No "start at 50% lightness" rule | | done |
| 5.3.2 | Finding the edges | Darkest is usually text, lightest usually a tinted background; an alert exercises both | | done |
| 5.3.3 | Filling in the gaps | At least 5, ~10 preferred; 900 / 500 / 100 → 700 / 300 → 800 / 600 / 400 / 200 | HV | done |
| 5.3.4 | What about greys | Same procedure; the base matters less | | done |
| 5.3.5 | It's not a science | Trust your eyes over the math, but resist adding new shades | | done |
| 5.4 | Lightness kills saturation | Near 0% or 100% lightness, saturation weakens; raise it as lightness moves away from 50% | HV | done |
| 5.4.1 | Perceived brightness | `√(0.299r² + 0.587g² + 0.114b²) / 255`; three minima and three maxima around the wheel | HV | done |
| 5.4.2 | Changing brightness by rotating hue | Lighten toward 60/180/300, darken toward 0/120/240; never more than 20–30° | HV | done |
| 5.5 | Greys don't have to be grey | True grey is 0% saturation; good UI greys are noticeably saturated | | done |
| 5.5.1 | Color temperature | Blue for cool, yellow/orange for warm; raise saturation at both ends | | done |
| 5.6 | Accessible doesn't have to mean ugly | 4.5:1 for body text, 3:1 for large text | HV | done |
| 5.6.1 | Flipping the contrast | White on color needs surprisingly dark backgrounds; invert to dark text on a light background | | done |
| 5.6.2 | Rotating the hue | For colored text on color, rotate toward a brighter hue instead of approaching white | | done |
| 5.7 | Don't rely on color alone | Add a supporting signal; graphs differentiate by contrast rather than hue | | done |

## Ch 6 · Creating Depth → `06-depth.md`

| ID | Book section | Core assertion | HV | Status |
|---|---|---|---|---|
| 6.1 | Emulate a light source | Depth is one rule, not a bag of effects | | done |
| 6.1.1 | Light comes from above | Raised: top edge lighter, bottom darker. Inset: shadow on top, bottom edge lighter | | done |
| 6.1.2 | Raised elements | Reveal the top edge; hand-pick the lighter color rather than overlaying semi-transparent white; small dark shadow below with a couple of pixels of blur | HV | done |
| 6.1.3 | Inset elements | Lighter bottom border or negative-offset inset shadow, plus a small dark inset shadow with positive offset on top | | done |
| 6.1.4 | Don't get carried away | Borrow real-world cues; don't chase photo-realism | | done |
| 6.2 | Shadows convey elevation | Tight blur = slightly raised, large blur = close to the user; closer attracts more focus | | done |
| 6.2.a | The three canonical uses | Small = buttons, medium = dropdowns, large = modals | | done |
| 6.2.1 | Elevation system | Five shadows: `0 1px 3px`, `0 4px 6px`, `0 5px 15px`, `0 10px 24px`, `0 15px 35px`, all `hsla(0,0%,0%,.2)` | HV | done |
| 6.2.2 | Shadows and interaction | Choose by intended z-position, not by how the shadow looks | | done |
| 6.3 | Shadows can have two parts | Two shadows do two distinct jobs | | done |
| 6.3.a | The two jobs | Larger and softer = cast shadow; tighter and darker = ambient occlusion directly beneath | | done |
| 6.3.1 | Accounting for elevation | The tight ambient shadow fades as the object rises; invisible at the highest level | | done |
| 6.4 | Even flat designs can have depth | Flat means no shadows or gradients, not no depth | | done |
| 6.4.1 | Creating depth with color | Lighter than the background reads as raised, darker as inset | | done |
| 6.4.2 | Using solid shadows | Short, vertically offset, zero blur | | done |
| 6.5 | Overlap elements to create layers | Cross a background transition or exceed the parent's height; works for small controls too | | done |
| 6.5.1 | Overlapping images | Give them an invisible border matching the background | | done |

## Ch 7 · Working with Images → `07-images.md`

| ID | Book section | Core assertion | HV | Status |
|---|---|---|---|---|
| 7.1 | Use good photos | Bad photos ruin a good design; hire a professional or use quality stock; never design with placeholders | | done |
| 7.2 | Text needs consistent contrast | The problem is the image, not the text color | | done |
| 7.2.1 | Background images | Photos are dynamic; reduce the image's dynamic range | | done |
| 7.2.2 | Add an overlay | Black tones down light areas for light text; white brightens dark areas for dark text | | done |
| 7.2.3 | Lower the image contrast | More control than an overlay; adjust brightness afterward to compensate | | done |
| 7.2.4 | Colorize the image | Lower contrast → desaturate → solid fill in multiply mode | | done |
| 7.2.5 | Add a text shadow | Large blur, no offset — a glow, not a shadow | | done |
| 7.3 | Everything has an intended size | Upscaling bitmaps is not the only scaling failure | | done |
| 7.3.1 | Don't scale up icons | 16–24px icons at 3–4× look chunky; enclose the icon at its intended size in a larger shape | HV | done |
| 7.3.2 | Don't scale down screenshots | Screenshot at a smaller viewport, take a partial shot, or draw a simplified UI | HV | done |
| 7.3.3 | Don't scale down icons either | Redraw a simplified version at the target size; favicons worst of all | HV | done |
| 7.4 | Beware user-uploaded content | You lose control of contrast, color and crop | | done |
| 7.4.1 | Control shape and size | Center in a fixed container and crop the overflow — `background-size: cover` | | done |
| 7.4.2 | Prevent background bleed | Subtle inner shadow or semi-transparent inner border, not a solid border | | done |

## Ch 8 · Finishing Touches → `08-finishing.md`

| ID | Book section | Core assertion | HV | Status |
|---|---|---|---|---|
| 8.1 | Supercharge the defaults | Icons as list bullets, promoted quote marks, custom link styling, branded checkboxes and radios | | done |
| 8.2 | Add color with accent borders | Card top, active nav item, alert edge, short underline, layout top edge | | done |
| 8.3 | Decorate your backgrounds | Break up monotony without redesigning | | done |
| 8.3.1 | Change the background color | Emphasize a panel or separate sections; a gradient with hues no more than ~30° apart | HV | done |
| 8.3.2 | Use a repeating pattern | Subtle, low contrast; can repeat along a single edge | | done |
| 8.3.3 | Add a simple shape or illustration | Geometric shapes, a slice of a pattern, a simplified map; keep contrast low | | done |
| 8.4 | Don't overlook empty states | The empty state is the first interaction; hide supporting UI that does nothing yet | | done |
| 8.5 | Use fewer borders | Borders stack into clutter; reach for an alternative first | | done |
| 8.5.1 | Use a box shadow | Outlines like a border but more subtle | | done |
| 8.5.2 | Use two background colors | If a color difference and a border both exist, drop the border | | done |
| 8.5.3 | Add extra spacing | Separation by distance introduces no new UI | | done |
| 8.6 | Think outside the box | Dropdowns can have sections and columns; table columns can merge; radio groups can become cards | | done |

## Ch 9 · Leveling Up → folded into `14-laws.md`

| ID | Book section | Core assertion | HV | Status |
|---|---|---|---|---|
| 9.1 | Leveling up | Two durable practices for continued growth | | done |
| 9.1.1 | Look for decisions you wouldn't have made | On a design you like, ask what the designer did that would never have occurred to you | | done |
| 9.1.2 | Rebuild your favorite interfaces | Recreate from scratch without devtools; the discrepancies teach the details | | done |

## Synthesized files (no coverage obligation)

| File | Draws from | Purpose |
|---|---|---|
| [`09-antipatterns.md`](09-antipatterns.md) | all chapters | Symptom → rule id → fix, for auditing |
| [`10-recipes.md`](10-recipes.md) | §2.8 §3.5 §3.6 §4.7 §5.6 §5.7 §6.1 §6.2 §8.2 §8.4 §8.5 §8.6 | Buttons, form groups, cards, empty states, tables, dropdowns, modals, alerts |
| [`11-tokens.md`](11-tokens.md) | §1.5 §3.2 §4.1 §5.1–§5.6 §6.2.1 | Building a token system: interview, ramps, output contract |
| [`12-tailwind.md`](12-tailwind.md) | the scales from every chapter | Optional mapping: spacing, text, color, shadow, radius, focus |
| [`13-beyond.md`](13-beyond.md) | — outside the book | Dark mode, focus, target sizes, motion, breakpoints, z-index, semantic tokens, form a11y, loading, truncation |
| [`14-laws.md`](14-laws.md) | the highest-frequency rules | Twelve laws, hard gates, §9 practices |
| [`15-direction.md`](15-direction.md) | — outside the book | Peer analysis, material/scene direction lock, absolute bans, the AI Slop Test |
| [`16-layout-patterns.md`](16-layout-patterns.md) | — outside the book | Fluid `clamp()` viewports, workbench independent panel scroll, sticky scroll narratives |
