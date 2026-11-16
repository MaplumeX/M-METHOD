# Direction, bans, and the slop test

Three things the rule library cannot cover. The 151 rules say whether a design is
**correct**; this file is about whether it has a **point of view** — and how to catch the
shapes that make an interface look machine-made.

No coverage obligation (see `00-coverage.md`).

## Lock the direction first

Resolve these five before writing any code.

1. **Who uses this, and in what context?** An analyst dashboard, a landing page and an
   onboarding flow are different products with the same components.
2. **What is the aesthetic direction?** Name it precisely: dense editorial, raw terminal,
   ink-on-paper, brutalist grid, warm analog. **"Clean and modern" is not a direction.**
   If the user names a reference product ("feels like Linear"), do not accept it as a
   direction — extract three concrete properties instead: the radius philosophy, the
   surface-depth treatment (shadow vs background step vs border), and the accent color
   family. Then name those.
3. **What is the design signature?** A typeface, a color system, an unexpected motion, an
   asymmetric layout. Pick one and make it obvious; a design with no signature is the
   default.
4. **What are the hard constraints?** Framework, bundle budget, contrast minimums,
   keyboard reachability.
5. **What is the signature micro-interaction?** Scale on press, staggered reveal,
   contextual icon animation. Pick one and know how it is implemented. **"None" is a valid
   answer** with a reason — a quiet utility surface may deliberately have no signature
   motion.

Where the answers come from, in order: the current product's tokens, sibling components,
screenshots and git history; then other shipped products by the same team; then the
conversation. Model-default palettes, default fonts and freehand graphics are the last
resort, allowed only when no reference exists.

Ask at most one compact round, and only about answers that would materially change the
deliverable. State your strongest inference for every open dimension and ask for
corrections; an omitted answer accepts the stated assumption.

**New surface inside a mature product**: the direction is the app. Find the existing
sibling component first and reuse its container, motion and typography tokens. Inventing
a new style needs a stated reason why no existing component fits.

State the direction in three lines before writing markup:

- **Visual thesis** — mood, material and energy in one sentence ("warm brutalist editorial
  with high-contrast ink type and rough paper texture").
- **Content plan** — the sequence in one line each. App and dashboard surfaces skip the
  marketing structure: orient, show status, enable action. No hero unless asked.
- **Interaction thesis** — either `none` with one evidence-based reason, or two or three
  specific motions that change how the surface feels.

## Absolute bans

Six shapes that make an interface read as generated. Each has a rewrite; the rewrite is
what belongs in the code.

| Ban | Why it reads as machine-made | Instead |
|---|---|---|
| Thick side-border accents on cards | The first trick every generator reaches for; it shouts "designed" without doing any design | Background step, elevation step, or nothing at all |
| Gradient text | Almost always illegible at the edges and impossible to keep accessible | A solid color at sufficient contrast; put the gradient in the background if you need energy |
| Glass / frosted cards by default | Assumes a colorful backdrop to blur; on a flat page it is a grey smear | A solid surface plus one border or one elevation step |
| Purple-to-blue or cyan-on-dark gradients | The default palette of every generated landing page | The project's own accent ramp, at one hue |
| Rounded shadow-card grids | Three identical boxes is a layout decision made by not deciding | Vary the treatment by importance, or use a list, table or split layout |
| Modals for ordinary overflow | Traps content, breaks back-navigation, stacks on mobile | Inline expansion, a drawer, or a dedicated route |

Two more that apply to motion specifically:

- **`transition: all`** — it animates properties you did not choose, including layout.
  Name the properties: `transition: opacity 150ms ease-out`.
- **Animating layout properties** — `width`, `height`, `top`, `left` force layout on every
  frame. Use `transform` and `opacity`.

## AI Slop Test

One question, asked at the end of Build and Review:

> Would a stranger glancing at the first viewport say "an AI made this"?

Scan for the reflex set:

- Inter (or the default sans) used with no stated reason
- A gradient with no source in the brand
- A centered hero with two CTAs side by side
- Three identical cards in a row
- A generic top navigation bar

If a hit is **not** an explicit part of the direction, fix it. If it **is** part of the
direction, keep it — the direction now justifies it, and you should be able to say why in
one sentence.

Fix first, then report. Naming a slop shape without fixing it is the same failure with
better vocabulary.

## Relationship to the rule library

Passing all 151 rules is necessary and not sufficient: a design can be correct and still
have no point of view. This file supplies the point of view; the lens files check that the
execution holds up. Both are required.
