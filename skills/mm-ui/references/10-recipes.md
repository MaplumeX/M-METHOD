# Component recipes

Not new rules — the rules from §2–§8 applied to the components that come up most.
**Token names are placeholders**: `primary` / `neutral` / `danger` come from the project's
own ramps, `N1…N6` are steps on its spacing scale (say 4/8/12/16/24/32), `T1…T5` are steps
on its type scale. Never treat an example color here as an answer — that is exactly what
§5.3 prevents.

No coverage obligation (see `00-coverage.md`).

## Button

Three levels by the action pyramid, not by color.

```
primary    bg primary-600  text white         padding 12/24  radius md  weight 600
secondary  bg transparent  border 1px neutral-200  text neutral-700
tertiary   no bg, no border  text primary-600  padding 8/12
```

- Three sizes: sm 8/16, md 12/24, lg 16/32. **Large buttons want disproportionately
  generous padding** (§3.5.1).
- Hover: primary drops one step (primary-700); secondary darkens border and text one step.
  **Never use opacity alone.**
- Disabled: neutral-100 background, neutral-400 text, no shadow.
- Focus: 2px outline, 2px offset, primary-600. A keyboard user who cannot see focus is a
  serious defect.
- Tertiary gets smaller padding because it usually sits inline.
- Rules: §2.8 §6.1.2 §5.6
- Common errors: every button solid and primary (§2.8); destructive actions loud by
  default (§2.8.1).

## Form group

```
label      T2, neutral-700, weight 500
input      height N5, padding N2/N3, radius md, border neutral-300, inset shadow
help       T2, neutral-500, N1 from the input
error      T2, danger-600, N1 from the input
group gap  N5 — must exceed every gap inside the group
```

- Label-to-input and help-to-input share the same small gap; **group-to-group must be two
  steps larger**, or users fill in the wrong field (§3.6).
- The input needs inset depth (§6.1.3): lighter bottom edge, small dark inset shadow at the
  top.
- Focus: border becomes primary-600 plus a 2px ring. Don't signal focus by border color
  alone.
- Error: border danger-600 plus **actionable** copy below — not "invalid input".
- Required markers use words, not a red asterisk alone (§5.7).
- Rules: §3.6 §4.4 §5.6 §6.1.3 §8.5

## Card

```
background  white (on a neutral-50 page)
border      none — use a background difference or a shadow (§8.5)
padding     N4
radius      md (consistent with the rest of the site, §1.4.3)
title       T3, neutral-900, weight 600
body        T2, neutral-600, line-height from line length (§4.5.1)
```

- One primary action per card; everything else demoted.
- Don't let cards widen indefinitely with the screen; give a max-width (§3.4.2).
- Lift with the lowest shadow step, and never lift every card on screen at once (§6.2).
- Rules: §6.2 §8.5 §3.4.2

## Empty state

```
illustration  a simple shape, low contrast (§8.3.3)
title         T4, neutral-900
body          T2, neutral-600, constrained to 45–75 characters
CTA           one primary button
```

- **Hide all supporting UI that does nothing yet**: tabs, filters, search (§8.4).
- This is the first contact with the feature; it earns an illustration. "No data" is not a
  design.
- Rules: §8.4 §8.3.3

## Table

```
header     T2, neutral-500, weight 500, bottom border 1px neutral-200
cell       T2, neutral-700, vertical padding N2
numbers    right-aligned (§4.7.2)
separation background stripes or spacing; avoid horizontal rules (§8.5)
```

- Hierarchy need not be one field per column: merge related columns (§8.6).
- Empty cells get an em dash, not blank space.
- Row actions: one explicit action plus a "more" menu, not four icons per row.
- Rules: §4.7.2 §8.5 §8.6

## Dropdown

```
panel      white, radius md, shadow step 3 (§6.2.1), padding N1
item       height N4, padding N1/N2, radius sm, text neutral-700
divider    1px neutral-100, only between item groups
```

- A dropdown is just a floating box: sections, columns, supporting text and colored icons
  are all allowed (§8.6).
- Hover uses a neutral-50 background; don't change the text color.
- Rules: §6.2 §8.6

## Modal

```
scrim      neutral-900 at 40%
panel      white, radius lg, shadow step 5 (§6.2.1), padding N4, max-width 480–560
title      T4, weight 600
actions    bottom right, primary action last
```

- Close button top right, **and Escape must work**.
- Destructive confirmation: the title states the consequence, the primary button uses
  danger, cancel is present.
- Rules: §2.8.1 §6.2 §8.5

## Alert

```
success  bg green-50   left border 4px green-500   text green-800
warning  bg yellow-50  left border 4px yellow-500  text yellow-800
error    bg red-50     left border 4px red-500     text red-800
```

- Use a **left accent border**, not a full outline (§8.2).
- Always include an icon: color cannot carry meaning alone (§5.7).
- With an action ("Undo"), place it to the right of the text as a tertiary button.
- Check text contrast at 4.5:1; dark-on-light is the easy direction (§5.6.1).
- Rules: §5.6 §5.7 §8.2

## Global check

After writing any component, answer four questions:

1. Is every height, spacing and type value on the project's scale? (§1.5)
2. Is there exactly one primary action? (§2.8)
3. Has the text contrast been measured? (§5.6, with `scripts/check_contrast.py`)
4. Can it be empty? What does it look like then? (§8.4)
