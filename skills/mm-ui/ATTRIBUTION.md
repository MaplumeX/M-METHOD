# Attribution

## The book

The rules in this skill are distilled from **Refactoring UI** by Adam Wathan and
Steve Schoger — <https://www.refactoringui.com>. Buy it; the original is better than
any summary, and the examples carry most of the teaching.

This skill is unofficial and independent. It is not affiliated with, endorsed by, or
reviewed by the book's authors.

## The Chinese translation

Wording follows the community Chinese translation at
<https://github.com/read-x/refactoring-ui-zh> (MIT for the original code, translation
and images under their own notice). This skill contains no book text and no images —
only rules restated as instructions.

## The coverage checklist

The 151-item inventory in [`references/00-coverage.md`](references/00-coverage.md) is
adapted from the coverage matrix in
<https://github.com/edisonmbli/refactoring-ui-skill> (MIT). That project is an
independent extraction of the same book; its matrix is used here as a checklist so no
rule from the book is lost, with the assertions rewritten in Chinese and the
Tailwind mappings dropped.

## What this repository adds

- Organisation by review lens rather than book chapter, so a design problem routes to
  the file that fixes it.
- Integration with the ADR workflow: design-system decisions become records, not
  tribal memory.
- No framework binding. Rule values are given as design-token scales, not class names.
