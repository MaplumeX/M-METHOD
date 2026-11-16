# Tailwind mapping (optional)

**An optional mapping, never a binding.** The rules give scales, not class names; use this
file when the project is on Tailwind, ignore it entirely otherwise.

No coverage obligation (see `00-coverage.md`).

## Why this mapping is so short

Tailwind's default scales *are* this book's scales — the book's author is Adam Wathan. Most
rules therefore need no translation: the defaults are already right, and the job is simply
not to override them.

## Spacing

Default `--spacing: 0.25rem`, so `p-4` is 16px. The scale maps directly:

| Token (px) | 4 | 8 | 12 | 16 | 24 | 32 | 48 | 64 | 96 | 128 |
|---|---|---|---|---|---|---|---|---|---|---|
| Class | `1` | `2` | `3` | `4` | `6` | `8` | `12` | `16` | `24` | `32` |

**Never use arbitrary values like `p-[13px]`** (§1.5). A missing step means the scale needs
one, not that the code needs a literal.

## Type

| Token (px) | 12 | 14 | 16 | 18 | 20 | 24 | 30 | 36 | 48 | 60 | 72 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Class | `text-xs` | `text-sm` | `text-base` | `text-lg` | `text-xl` | `text-2xl` | `text-3xl` | `text-4xl` | `text-5xl` | `text-6xl` | `text-7xl` |

Set line-height with the size, **never `leading-normal` everywhere** (§4.5): headlines take
`leading-none` or `leading-tight`; body takes `leading-normal` (1.5) to `leading-relaxed`
(1.625) depending on line length. Narrower lines take less.

## Measure

```html
<p class="max-w-prose">   <!-- 65ch, inside the 45–75 character range -->
```

When the container is wider, the paragraph constrains itself; text does not follow the
container (§4.3.1).

## Color

Nine-step naming aligned with the book's 100–900:

```css
/* v4 */
@theme {
  --color-primary-100: oklch(0.97 0.02 250);
  --color-primary-200: oklch(0.93 0.04 250);
  /* … 300 400 500 600 700 800 … */
  --color-primary-900: oklch(0.32 0.08 250);

  --color-neutral-100: oklch(0.97 0.005 250);
  /* … */
}
```

```js
// v3
export default {
  theme: {
    extend: {
      colors: {
        primary: { 100: '#eef4ff', /* … */ 900: '#0b1b3f' },
        neutral: { 100: '#f7f8fa', /* … */ 900: '#111318' },
      },
    },
  },
}
```

**Tailwind's default palette adds 50 and 950**, which are not among the book's nine. You can
use them, but say what they are for (50 = page background, 950 = darkest text) so they do not
become steps ten and eleven (§5.3.5).

**`indigo` and `gray` in examples are placeholders.** Copying the defaults is the most
recognizable tell of machine-generated UI.

## Shadows

Tailwind ships six steps (`shadow-sm` to `shadow-2xl`); the book has five, with different
values. Choose one:

```js
// v3: define the book's five steps
theme: {
  extend: {
    boxShadow: {
      1: '0 1px 3px hsl(0 0% 0% / .2)',
      2: '0 4px 6px hsl(0 0% 0% / .2)',
      3: '0 5px 15px hsl(0 0% 0% / .2)',
      4: '0 10px 24px hsl(0 0% 0% / .2)',
      5: '0 15px 35px hsl(0 0% 0% / .2)',
    },
  },
},
```

```css
/* v4 */
@theme {
  --shadow-1: 0 1px 3px hsl(0 0% 0% / .2);
  --shadow-2: 0 4px 6px hsl(0 0% 0% / .2);
  --shadow-3: 0 5px 15px hsl(0 0% 0% / .2);
  --shadow-4: 0 10px 24px hsl(0 0% 0% / .2);
  --shadow-5: 0 15px 35px hsl(0 0% 0% / .2);
}
```

Using the six defaults is fine, but **assign each to a role** — which one is a button, which
a dropdown, which a modal (§6.2.a) — or the same elevation ends up with two different
shadows.

## Radius

`rounded-sm` 2px, `rounded` 4px, `rounded-md` 6px, `rounded-lg` 8px, `rounded-xl` 12px.

Pick one as the default (6px for most interfaces) and one for large containers (8 or 12px).
**Use only those two across the site** (§1.4.3).

## Focus and disabled

```html
<button class="focus-visible:outline-none focus-visible:ring-2
               focus-visible:ring-primary-600 focus-visible:ring-offset-2
               disabled:bg-neutral-100 disabled:text-neutral-400">
```

Use `focus-visible`, not `focus` — a mouse click should not show a ring, a keyboard user
must. **Never set `outline: none` globally.**

## Contrast is not Tailwind's job

No class guarantees 4.5:1. Once the colors are set:

```bash
python3 scripts/check_contrast.py --file pairs.txt
```

## Dark mode

Change values in `tokens.css`; don't stack `dark:` on every component:

```css
:root { --color-surface: var(--color-neutral-100); --color-text: var(--color-neutral-900); }
[data-theme="dark"] { --color-surface: var(--color-neutral-900); --color-text: var(--color-neutral-100); }
```

Components use `bg-surface` / `text-text` style semantic classes. See `13-beyond.md`.
