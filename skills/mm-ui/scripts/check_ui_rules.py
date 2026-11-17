#!/usr/bin/env python3
"""Static UI rule gate for mm-ui (§2.2.b, §3.2, §3.3, §4.1, §4.3, §4.4, §4.5, §5.3–§5.5, §6.1.3, Build gates).

Checks CSS files and <style> blocks inside HTML/Vue/Svelte files against
mechanically verifiable Refactoring UI / M-METHOD rules, plus optional gates
for System token ramps (--tokens), Pass 1 grayscale purity (--pass1),
Build 3-line direction + 6-item constraint brief (--brief), and final
delivery report (--report).

Usage:
    check_ui_rules.py src/
    check_ui_rules.py src/ --pass1
    check_ui_rules.py src/ --brief src/App.css
    check_ui_rules.py --tokens tokens.css
    check_ui_rules.py --report report.md

Exemptions:
    Add a CSS comment on the same line, immediately above the declaration/rule,
    or inside the rule block:
        /* mm-ui-allow §4.4: single-line icon + label alignment */
        /* mm-ui-allow §3.3: full-bleed data table */

Exit codes:
    0  No errors (and no warnings when --strict is set)
    1  One or more rule errors found (or warnings under --strict)
    2  Invalid usage or no matching files found
"""

from __future__ import annotations

import argparse
import colorsys
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_contrast import parse_color  # noqa: E402

STYLE_EXTENSIONS = {".css", ".scss", ".less"}
MARKUP_EXTENSIONS = {".html", ".htm", ".vue", ".svelte"}
SKIP_DIRS = {"node_modules", ".git", "dist", "build", ".next", ".turbo", "coverage", "__pycache__"}

SPACING_SCALE_PX = {4, 8, 12, 16, 24, 32, 48, 64, 96, 128, 192, 256, 384, 512, 640, 768}
TYPE_SCALE_PX = {12, 14, 16, 18, 20, 24, 30, 36, 48, 60, 72}

LAYOUT_ANIM_PROPS = {
    "width",
    "height",
    "min-width",
    "max-width",
    "min-height",
    "max-height",
    "top",
    "left",
    "right",
    "bottom",
    "margin",
    "margin-top",
    "margin-right",
    "margin-bottom",
    "margin-left",
    "padding",
    "padding-top",
    "padding-right",
    "padding-bottom",
    "padding-left",
}

ALLOW_RE = re.compile(r"mm-ui-allow\s+(§[\w.]+|15-direction)(?:\s*:\s*(.*))?", re.IGNORECASE)
STYLE_BLOCK_RE = re.compile(r"<style\b[^>]*>(.*?)</style>", re.IGNORECASE | re.DOTALL)

INPUT_NON_BOX_SUFFIX_RE = re.compile(
    r"(?:^|[.\s>+~])(?:\.?[\w-]*input-(?:group|row|wrap|wrapper|label|help|hint|error|icon|prefix|suffix|box-label))\b",
    re.IGNORECASE,
)
INPUT_PSEUDO_OR_NONTEXT_RE = re.compile(
    r":(?:focus|focus-visible|focus-within|hover|active|disabled|placeholder|checked)\b|"
    r"::placeholder\b|"
    r"\[type\s*=\s*['\"]?(?:checkbox|radio|range|hidden|submit|button|reset|file|color)['\"]?\]",
    re.IGNORECASE,
)
INPUT_TARGET_RE = re.compile(
    r"(?:^|[\s,>+~])(?:input|textarea|select|\[contenteditable[^\]]*\]|\.(?:[\w-]+-)?input)\b",
    re.IGNORECASE,
)

ROW_TARGET_RE = re.compile(
    r"(?:^|[\s,>+~])\.(?:[\w-]+-)?(?:row|header|list-item|title-bar|meta)\b",
    re.IGNORECASE,
)
ROW_EXEMPT_TARGET_RE = re.compile(
    r"\.(?:[\w-]+-)?(?:btn|button|badge|pill|chip|tag|icon|avatar|switch|toggle|spinner|loader|nav-item|tab|empty)\b",
    re.IGNORECASE,
)

CONTENT_CONTAINER_RE = re.compile(
    r"(?:^|[\s,>+~])(?:main|article|\.(?:[\w-]+-)?(?:main|content|page-content|list|feed|prose|thread|body-copy))\b",
    re.IGNORECASE,
)
EMPTY_TARGET_RE = re.compile(
    r"\.(?:[\w-]+-)?empty(?:-state)?\b",
    re.IGNORECASE,
)

HEADING_TARGET_RE = re.compile(
    r"(?:^|[\s,>+~])(?:h[1-3]|\.(?:[\w-]+-)?(?:title|heading|hero-title|page-title))\b",
    re.IGNORECASE,
)
TEXT_ROLE_RE = re.compile(
    r"\.(?:[\w-]+-)?(?:text|muted|secondary|label|caption|subtitle|meta|hint|help|desc|description|empty)\b",
    re.IGNORECASE,
)


@dataclass
class Declaration:
    prop: str
    value: str
    line: int


@dataclass
class Rule:
    selector: str
    declarations: list[Declaration]
    start_line: int
    end_line: int
    allows: dict[str, str]


@dataclass
class Finding:
    severity: str  # "ERROR" | "WARN"
    rule_id: str
    code: str
    file: str
    line: int
    selector: str
    message: str


def _extract_allows(comment_text: str) -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []
    for match in ALLOW_RE.finditer(comment_text):
        rule_id = match.group(1)
        reason = (match.group(2) or "").strip()
        found.append((rule_id, reason))
    return found


def strip_comments_with_allows(text: str) -> tuple[str, dict[int, list[tuple[str, str]]]]:
    """Strip CSS /* ... */ comments while preserving line count and mm-ui-allow directives."""
    out: list[str] = []
    allows_by_line: dict[int, list[tuple[str, str]]] = {}
    i = 0
    n = len(text)
    line = 1
    while i < n:
        if text[i] == "/" and i + 1 < n and text[i + 1] == "*":
            end = text.find("*/", i + 2)
            if end == -1:
                end = n
            else:
                end += 2
            comment = text[i:end]
            extracted = _extract_allows(comment)
            comment_lines = comment.count("\n")
            if extracted:
                allows_by_line.setdefault(line + comment_lines, []).extend(extracted)
            out.append("\n" * comment_lines)
            line += comment_lines
            i = end
        else:
            ch = text[i]
            if ch == "\n":
                line += 1
            out.append(ch)
            i += 1
    return "".join(out), allows_by_line


def _find_matching_brace(text: str, open_idx: int) -> int:
    depth = 0
    i = open_idx
    n = len(text)
    in_str: str | None = None
    while i < n:
        ch = text[i]
        if in_str:
            if ch == "\\" and i + 1 < n:
                i += 2
                continue
            if ch == in_str:
                in_str = None
        else:
            if ch in ("'", '"'):
                in_str = ch
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return i
        i += 1
    return n - 1


def _parse_declarations(body: str, base_line: int) -> list[Declaration]:
    decls: list[Declaration] = []
    current: list[str] = []
    stmt_start_line = base_line
    cur_line = base_line
    paren_depth = 0
    in_str: str | None = None

    def flush() -> None:
        raw = "".join(current).strip()
        current.clear()
        if not raw or ":" not in raw:
            return
        prop, val = raw.split(":", 1)
        prop_clean = prop.strip().lower()
        val_clean = val.strip()
        if prop_clean and not prop_clean.startswith("--"):
            decls.append(Declaration(prop=prop_clean, value=val_clean, line=stmt_start_line))

    for ch in body:
        if not current and not ch.strip():
            if ch == "\n":
                cur_line += 1
            stmt_start_line = cur_line
            continue

        if in_str:
            current.append(ch)
            if ch == in_str:
                in_str = None
        else:
            if ch in ("'", '"'):
                in_str = ch
                current.append(ch)
            elif ch == "(":
                paren_depth += 1
                current.append(ch)
            elif ch == ")" and paren_depth > 0:
                paren_depth -= 1
                current.append(ch)
            elif ch == ";" and paren_depth == 0:
                flush()
                stmt_start_line = cur_line
            else:
                current.append(ch)

        if ch == "\n":
            cur_line += 1

    flush()
    return decls


def _collect_rules(
    css: str,
    base_line: int,
    allows_by_line: dict[int, list[tuple[str, str]]],
    rules: list[Rule],
) -> None:
    i = 0
    n = len(css)
    cur_line = base_line
    header_start = 0
    header_line = base_line

    while i < n:
        ch = css[i]
        if ch == "{":
            raw_header = css[header_start:i].strip()
            close_idx = _find_matching_brace(css, i)
            body = css[i + 1 : close_idx]
            body_start_line = cur_line
            body_end_line = body_start_line + body.count("\n")

            header_lower = raw_header.lower()
            if header_lower.startswith("@keyframes") or header_lower.startswith("@-webkit-keyframes"):
                pass
            elif header_lower.startswith("@font-face"):
                pass
            elif header_lower.startswith("@"):
                _collect_rules(body, body_start_line, allows_by_line, rules)
            elif raw_header and not _is_token_root_selector(raw_header):
                allows: dict[str, str] = {}
                for ln in range(max(1, header_line - 1), body_end_line + 1):
                    for rid, reason in allows_by_line.get(ln, []):
                        allows[rid] = reason
                decls = _parse_declarations(body, body_start_line)
                rules.append(
                    Rule(
                        selector=" ".join(raw_header.split()),
                        declarations=decls,
                        start_line=header_line,
                        end_line=body_end_line,
                        allows=allows,
                    )
                )

            cur_line = body_end_line
            i = close_idx + 1
            header_start = i
            header_line = cur_line
            continue

        if ch == ";" and css[header_start:i].strip().startswith("@"):
            header_start = i + 1
            header_line = cur_line

        if ch == "\n":
            cur_line += 1
            if not css[header_start : i + 1].strip():
                header_line = cur_line
        i += 1


def _is_token_root_selector(selector: str) -> bool:
    s = selector.strip().lower()
    return s == ":root" or s.startswith("[data-theme") or s == ":host"


def parse_css_rules(text: str, start_line: int = 1) -> tuple[list[Rule], dict[int, list[tuple[str, str]]]]:
    clean, allows_by_line = strip_comments_with_allows(text)
    rules: list[Rule] = []
    _collect_rules(clean, start_line, allows_by_line, rules)
    return rules, allows_by_line


def _is_allowed(rule: Rule, allows_by_line: dict[int, list[tuple[str, str]]], decl_line: int, *rule_ids: str) -> bool:
    for rid in rule_ids:
        if rid in rule.allows:
            return True
    for ln in (decl_line, decl_line - 1):
        for rid, _ in allows_by_line.get(ln, []):
            if rid in rule_ids:
                return True
    return False


def _has_effective_border(decls: dict[str, list[Declaration]]) -> bool:
    for prop in ("border", "border-top", "border-right", "border-bottom", "border-left", "border-width"):
        for d in decls.get(prop, []):
            val = d.value.lower().replace("!important", "").strip()
            if val not in ("none", "0", "0px", "transparent"):
                return True
    return False


def _has_explicit_no_border(decls: dict[str, list[Declaration]]) -> Declaration | None:
    for prop in ("border", "border-width"):
        for d in decls.get(prop, []):
            val = d.value.lower().replace("!important", "").strip()
            if val in ("none", "0", "0px"):
                return d
    return None


def _has_effective_shadow(decls: dict[str, list[Declaration]]) -> bool:
    for d in decls.get("box-shadow", []):
        val = d.value.lower().replace("!important", "").strip()
        if val != "none" and val != "0":
            return True
    return False


def _parse_px(val: str) -> float | None:
    m = re.fullmatch(r"(-?\d+(?:\.\d+)?)px", val.strip().lower())
    if m:
        return float(m.group(1))
    return None


def _parse_numeric_unitless(val: str) -> float | None:
    m = re.fullmatch(r"(\d+(?:\.\d+)?)", val.strip().lower())
    if m:
        return float(m.group(1))
    return None


def _is_large_font_size(val: str) -> bool:
    v = val.strip().lower()
    px = _parse_px(v)
    if px is not None:
        return px >= 24.0
    m_rem = re.fullmatch(r"(\d+(?:\.\d+)?)rem", v)
    if m_rem:
        return float(m_rem.group(1)) >= 1.5
    if re.search(r"--text-(?:2xl|3xl|4xl|5xl|6xl|display|24|30|36|48|60|72)\b", v):
        return True
    return False


def check_rules_in_file(
    file_path: str,
    rules: list[Rule],
    allows_by_line: dict[int, list[tuple[str, str]]],
    pass1: bool = False,
) -> list[Finding]:
    findings: list[Finding] = []
    is_tokens_file = Path(file_path).name.startswith("tokens")

    all_line_heights: list[tuple[Rule, Declaration]] = []
    empty_selectors_with_measure: list[Rule] = []
    content_selectors_without_measure: list[Rule] = []

    base_input_has_depth = False
    for r in rules:
        if re.search(r"(?:^|,\s*)(?:input|textarea|select)(?:$|[\s,])", r.selector, re.IGNORECASE):
            r_decls: dict[str, list[Declaration]] = {}
            for d in r.declarations:
                r_decls.setdefault(d.prop, []).append(d)
            if _has_effective_border(r_decls) or _has_effective_shadow(r_decls):
                base_input_has_depth = True
                break

    for rule in rules:
        decls_by_prop: dict[str, list[Declaration]] = {}
        for d in rule.declarations:
            decls_by_prop.setdefault(d.prop, []).append(d)

        sel = rule.selector

        # 1. §4.1.2: Avoid em units for font-size
        for d in decls_by_prop.get("font-size", []):
            if re.search(r"\b\d*\.?\d+em\b", d.value.lower()) and not _is_allowed(rule, allows_by_line, d.line, "§4.1.2", "§4.1"):
                findings.append(
                    Finding(
                        severity="ERROR",
                        rule_id="§4.1.2",
                        code="no-em-font-size",
                        file=file_path,
                        line=d.line,
                        selector=sel,
                        message=f"font-size uses em ({d.value}); nested em compounds off-scale — use px, rem, or a --text-* token",
                    )
                )

        # 2. 15-direction: Ban transition: all and layout-property animations
        for prop in ("transition", "transition-property"):
            for d in decls_by_prop.get(prop, []):
                val_lower = d.value.lower()
                if re.search(r"\ball\b", val_lower) and not _is_allowed(rule, allows_by_line, d.line, "15-direction"):
                    findings.append(
                        Finding(
                            severity="ERROR",
                            rule_id="15-direction",
                            code="no-transition-all",
                            file=file_path,
                            line=d.line,
                            selector=sel,
                            message="transition: all animates unintended properties; name specific properties (e.g. opacity, transform)",
                        )
                    )
                for lprop in sorted(LAYOUT_ANIM_PROPS):
                    if re.search(rf"(?<![\w-]){re.escape(lprop)}(?![\w-])", val_lower) and not _is_allowed(
                        rule, allows_by_line, d.line, "15-direction"
                    ):
                        findings.append(
                            Finding(
                                severity="ERROR",
                                rule_id="15-direction",
                                code="no-layout-animation",
                                file=file_path,
                                line=d.line,
                                selector=sel,
                                message=f"transition animates layout property '{lprop}'; animate transform and opacity instead",
                            )
                        )
                        break

        # 3. §2.2.b: Never go below font-weight 400 for UI text
        for d in decls_by_prop.get("font-weight", []):
            v = d.value.lower().replace("!important", "").strip()
            num = _parse_numeric_unitless(v)
            if (v == "lighter" or (num is not None and num < 400)) and not _is_allowed(rule, allows_by_line, d.line, "§2.2.b", "§2.2"):
                findings.append(
                    Finding(
                        severity="ERROR",
                        rule_id="§2.2.b",
                        code="light-font-weight",
                        file=file_path,
                        line=d.line,
                        selector=sel,
                        message=f"font-weight {d.value} is below 400; de-emphasize with color or size rather than thin weights",
                    )
                )

        # 4. §2.3.a: Warn on opacity < 1 used to dim text
        if TEXT_ROLE_RE.search(sel) and not re.search(r":(?:disabled|hover|focus)\b|\.disabled\b", sel, re.IGNORECASE):
            for d in decls_by_prop.get("opacity", []):
                num = _parse_numeric_unitless(d.value.replace("!important", ""))
                if num is not None and 0.0 < num < 1.0 and not _is_allowed(rule, allows_by_line, d.line, "§2.3.a", "§2.3"):
                    findings.append(
                        Finding(
                            severity="WARN",
                            rule_id="§2.3.a",
                            code="opacity-dimmed-text",
                            file=file_path,
                            line=d.line,
                            selector=sel,
                            message=f"opacity: {d.value} on text role looks washed out; use a semantic text token or hand-picked same-hue color",
                        )
                    )

        # 5. §6.1.3: Inputs must not be flat sticker-like boxes (no border and no shadow)
        if (
            INPUT_TARGET_RE.search(sel)
            and not INPUT_NON_BOX_SUFFIX_RE.search(sel)
            and not INPUT_PSEUDO_OR_NONTEXT_RE.search(sel)
        ):
            no_border_decl = _has_explicit_no_border(decls_by_prop)
            has_border = _has_effective_border(decls_by_prop)
            has_shadow = _has_effective_shadow(decls_by_prop)
            has_box_styling = any(p in decls_by_prop for p in ("background", "background-color", "padding", "height", "min-height"))
            is_class_only = not re.search(r"(?:^|[\s,>+~])(?:input|textarea|select)\b", sel, re.IGNORECASE)
            inherited_base_depth = is_class_only and base_input_has_depth and no_border_decl is None
            if (no_border_decl is not None or (has_box_styling and not inherited_base_depth)) and not has_border and not has_shadow:
                check_line = no_border_decl.line if no_border_decl else rule.start_line
                if not _is_allowed(rule, allows_by_line, check_line, "§6.1.3", "§6.1"):
                    findings.append(
                        Finding(
                            severity="ERROR",
                            rule_id="§6.1.3",
                            code="flat-input",
                            file=file_path,
                            line=check_line,
                            selector=sel,
                            message="input has neither a visible border nor inset shadow; add border + inset depth (§6.1.3) so it reads as editable",
                        )
                    )

        # 6. §4.4: Baseline, not center for text rows/headers with mixed content
        if ROW_TARGET_RE.search(sel) and not ROW_EXEMPT_TARGET_RE.search(sel):
            for d in decls_by_prop.get("align-items", []):
                if d.value.lower().replace("!important", "").strip() == "center" and not _is_allowed(
                    rule, allows_by_line, d.line, "§4.4"
                ):
                    findings.append(
                        Finding(
                            severity="ERROR",
                            rule_id="§4.4",
                            code="center-aligned-row",
                            file=file_path,
                            line=d.line,
                            selector=sel,
                            message="align-items: center on text row/header misaligns mixed text sizes; use baseline (or exempt single-line icon+label with /* mm-ui-allow §4.4: ... */)",
                        )
                    )

        # 7. §3.3 & §4.3: Track max-width / measure on content vs empty states
        has_measure = "max-width" in decls_by_prop or any(
            "--measure" in d.value for decls in decls_by_prop.values() for d in decls
        )
        if EMPTY_TARGET_RE.search(sel) and has_measure:
            empty_selectors_with_measure.append(rule)

        if CONTENT_CONTAINER_RE.search(sel) and not has_measure:
            content_selectors_without_measure.append(rule)
            has_fluid_expansion = any(
                (d.prop == "flex" and re.match(r"^1\b", d.value.strip()))
                or (d.prop == "flex-grow" and d.value.strip() == "1")
                or (d.prop == "width" and d.value.strip() == "100%")
                for d in rule.declarations
            )
            if has_fluid_expansion and not _is_allowed(rule, allows_by_line, rule.start_line, "§3.3", "§4.3"):
                findings.append(
                    Finding(
                        severity="ERROR",
                        rule_id="§3.3",
                        code="unconstrained-content",
                        file=file_path,
                        line=rule.start_line,
                        selector=sel,
                        message="fluid content container expands without max-width; constrain content width (§3.3 / §4.3) or exempt with /* mm-ui-allow §3.3: ... */",
                    )
                )

        # 8. §4.5: Line-height proportional to font-size and measure
        has_large_type = HEADING_TARGET_RE.search(sel) or any(
            _is_large_font_size(d.value) for d in decls_by_prop.get("font-size", [])
        )
        for d in decls_by_prop.get("line-height", []):
            all_line_heights.append((rule, d))
            num = _parse_numeric_unitless(d.value.replace("!important", ""))
            if has_large_type and num is not None and num >= 1.4 and not _is_allowed(rule, allows_by_line, d.line, "§4.5.2", "§4.5"):
                findings.append(
                    Finding(
                        severity="ERROR",
                        rule_id="§4.5.2",
                        code="loose-heading-leading",
                        file=file_path,
                        line=d.line,
                        selector=sel,
                        message=f"large heading/title uses line-height {d.value} (>= 1.4); tighten headline leading toward 1.0–1.25",
                    )
                )

        # 9. §3.2 / §4.1: Off-scale raw px values outside tokens files
        if not is_tokens_file:
            for d in decls_by_prop.get("font-size", []):
                px = _parse_px(d.value.replace("!important", ""))
                if px is not None and px > 0 and (not px.is_integer() or int(px) not in TYPE_SCALE_PX):
                    if not _is_allowed(rule, allows_by_line, d.line, "§4.1", "§4.1.1d"):
                        findings.append(
                            Finding(
                                severity="ERROR",
                                rule_id="§4.1",
                                code="off-scale-font-size",
                                file=file_path,
                                line=d.line,
                                selector=sel,
                                message=f"font-size {d.value} is off the type scale (12 14 16 18 20 24 30 36 48 60 72); use a scale token",
                            )
                        )

            for prop in (
                "gap",
                "row-gap",
                "column-gap",
                "padding",
                "padding-top",
                "padding-right",
                "padding-bottom",
                "padding-left",
                "margin",
                "margin-top",
                "margin-right",
                "margin-bottom",
                "margin-left",
            ):
                for d in decls_by_prop.get(prop, []):
                    tokens = d.value.replace("!important", "").split()
                    for tok in tokens:
                        px = _parse_px(tok)
                        if px is not None and px > 2 and (not px.is_integer() or int(px) not in SPACING_SCALE_PX):
                            if not _is_allowed(rule, allows_by_line, d.line, "§3.2", "§3.2.2"):
                                findings.append(
                                    Finding(
                                        severity="ERROR",
                                        rule_id="§3.2",
                                        code="off-scale-spacing",
                                        file=file_path,
                                        line=d.line,
                                        selector=sel,
                                        message=f"{prop} uses off-scale value {tok}; pick from 4 8 12 16 24 32 48 64 96... or use --space-* tokens",
                                    )
                                )
                                break

        # 10. Pass 1 grayscale purity (§1.2.1): ban accent/status tokens and decorative non-inset shadows
        if pass1:
            for d in rule.declarations:
                val_lower = d.value.lower()
                if ("--accent" in val_lower or "--status-" in val_lower) and not _is_allowed(
                    rule, allows_by_line, d.line, "§1.2.1"
                ):
                    findings.append(
                        Finding(
                            severity="ERROR",
                            rule_id="§1.2.1",
                            code="pass1-color-leak",
                            file=file_path,
                            line=d.line,
                            selector=sel,
                            message=f"Pass 1 must stay grayscale; found accent/status token in '{d.prop}: {d.value}'",
                        )
                    )
                if d.prop == "box-shadow" and val_lower not in ("none", "0") and "inset" not in val_lower:
                    if not _is_allowed(rule, allows_by_line, d.line, "§1.2.1"):
                        findings.append(
                            Finding(
                                severity="ERROR",
                                rule_id="§1.2.1",
                                code="pass1-shadow-leak",
                                file=file_path,
                                line=d.line,
                                selector=sel,
                                message="Pass 1 must stay flat/grayscale; defer decorative box-shadow to Pass 2 (§6)",
                            )
                        )

    # File-level check: asymmetric measure (empty state has measure, primary content lacks max-width)
    if empty_selectors_with_measure and content_selectors_without_measure:
        already_reported = {
            (f.line, f.selector) for f in findings if f.code == "unconstrained-content"
        }
        for rule in content_selectors_without_measure:
            if (rule.start_line, rule.selector) in already_reported:
                continue
            if not _is_allowed(rule, allows_by_line, rule.start_line, "§3.3", "§4.3"):
                findings.append(
                    Finding(
                        severity="ERROR",
                        rule_id="§3.3 / §4.3",
                        code="asymmetric-measure",
                        file=file_path,
                        line=rule.start_line,
                        selector=rule.selector,
                        message="empty state sets measure/max-width while primary content container has no max-width",
                    )
                )

    # File-level check: uniform line-height across 4+ declarations
    if len(all_line_heights) >= 4:
        distinct = {d.value.replace("!important", "").strip().lower() for _, d in all_line_heights}
        if len(distinct) == 1:
            only_val = next(iter(distinct))
            first_rule, first_decl = all_line_heights[0]
            if not _is_allowed(first_rule, allows_by_line, first_decl.line, "§4.5"):
                findings.append(
                    Finding(
                        severity="WARN",
                        rule_id="§4.5",
                        code="uniform-line-height",
                        file=file_path,
                        line=first_decl.line,
                        selector=first_rule.selector,
                        message=f"all {len(all_line_heights)} line-height declarations use '{only_val}'; match line-height to font size and line width",
                    )
                )

    return findings


def scan_path(target: Path, pass1: bool = False) -> list[Finding]:
    files: list[Path] = []
    if target.is_file():
        files.append(target)
    elif target.is_dir():
        for root, dirs, filenames in os.walk(target):
            dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
            for name in sorted(filenames):
                p = Path(root) / name
                if p.suffix.lower() in STYLE_EXTENSIONS | MARKUP_EXTENSIONS:
                    files.append(p)

    all_findings: list[Finding] = []
    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        ext = path.suffix.lower()
        if ext in STYLE_EXTENSIONS:
            rules, allows = parse_css_rules(text, start_line=1)
            all_findings.extend(check_rules_in_file(str(path), rules, allows, pass1=pass1))
        elif ext in MARKUP_EXTENSIONS:
            for match in STYLE_BLOCK_RE.finditer(text):
                style_text = match.group(1)
                start_line = text[: match.start(1)].count("\n") + 1
                rules, allows = parse_css_rules(style_text, start_line=start_line)
                all_findings.extend(check_rules_in_file(str(path), rules, allows, pass1=pass1))
    return all_findings


def _rgb_to_hsl(rgb: tuple[int, int, int]) -> tuple[float, float, float]:
    r, g, b = (c / 255.0 for c in rgb)
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return (h * 360.0, s * 100.0, l * 100.0)


def check_tokens_file(path: Path) -> list[Finding]:
    """Validate 9-step color ramps in tokens.css or tokens.json (§5.2.1, §5.3, §5.4, §5.5.1)."""
    findings: list[Finding] = []
    text = path.read_text(encoding="utf-8", errors="replace")
    ramps: dict[str, dict[int, tuple[str, int]]] = {}

    if path.suffix.lower() == ".json":
        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            return [Finding("ERROR", "§5.3", "invalid-tokens-json", str(path), 1, "tokens.json", f"invalid JSON: {exc}")]

        def walk_json(obj: object, prefix: str = "") -> None:
            if not isinstance(obj, dict):
                return
            step_keys = {k: v for k, v in obj.items() if re.fullmatch(r"\d{2,3}", str(k)) and isinstance(v, str)}
            if step_keys and prefix:
                for k, v in step_keys.items():
                    ramps.setdefault(prefix, {})[int(k)] = (v, 1)
                return
            for k, v in obj.items():
                walk_json(v, k if not prefix else f"{prefix}.{k}")

        walk_json(data)
    else:
        for lineno, line in enumerate(text.splitlines(), 1):
            m = re.search(r"--(?:color-)?([a-zA-Z0-9_-]+)-(\d{2,3})\s*:\s*([^;]+);", line)
            if m:
                group, step_s, val = m.group(1), m.group(2), m.group(3).strip()
                if val.startswith("var("):
                    continue
                ramps.setdefault(group, {})[int(step_s)] = (val, lineno)

    if not ramps:
        findings.append(
            Finding("ERROR", "§5.3", "no-color-ramps", str(path), 1, "tokens", "no 9-step color ramps (--color-<group>-100..900) found")
        )
        return findings

    expected_steps = {100, 200, 300, 400, 500, 600, 700, 800, 900}
    for group, steps in sorted(ramps.items()):
        extra_steps = set(steps.keys()) - expected_steps
        # Allow optional 50/950 only on neutral/grey (e.g. dark surface neutral-950 per 13-beyond.md)
        if group.lower() in ("neutral", "gray", "grey"):
            extra_steps -= {50, 950}
        missing_steps = expected_steps - set(steps.keys())
        first_line = min(ln for _, ln in steps.values())

        if missing_steps:
            findings.append(
                Finding(
                    "ERROR",
                    "§5.3",
                    "incomplete-ramp",
                    str(path),
                    first_line,
                    group,
                    f"ramp '{group}' missing step(s) {sorted(missing_steps)}; build 9 steps (100..900) via generate_ramp.py",
                )
            )
            continue
        if extra_steps:
            findings.append(
                Finding(
                    "ERROR",
                    "§5.3.5",
                    "extra-ramp-step",
                    str(path),
                    first_line,
                    group,
                    f"ramp '{group}' has unallowed extra step(s) {sorted(extra_steps)}; resist adding steps outside 100..900",
                )
            )

        hsl_steps: dict[int, tuple[float, float, float, int]] = {}
        for step in sorted(expected_steps):
            val, ln = steps[step]
            try:
                rgb = parse_color(val)
            except ValueError:
                findings.append(
                    Finding("ERROR", "§5.3", "unparseable-ramp-color", str(path), ln, f"{group}-{step}", f"cannot parse color {val!r}")
                )
                continue
            if rgb in ((0, 0, 0), (255, 255, 255)):
                findings.append(
                    Finding(
                        "ERROR",
                        "§5.2.1",
                        "pure-bw-in-ramp",
                        str(path),
                        ln,
                        f"{group}-{step}",
                        "ramp step uses pure #000000 or #ffffff; edges must remain off-black / off-white",
                    )
                )
            h, s, l = _rgb_to_hsl(rgb)
            hsl_steps[step] = (h, s, l, ln)

        if len(hsl_steps) == 9:
            ordered = [hsl_steps[s] for s in sorted(expected_steps)]
            for idx in range(len(ordered) - 1):
                if ordered[idx][2] <= ordered[idx + 1][2]:
                    s_cur = sorted(expected_steps)[idx]
                    s_nxt = sorted(expected_steps)[idx + 1]
                    findings.append(
                        Finding(
                            "ERROR",
                            "§5.3",
                            "non-monotonic-ramp",
                            str(path),
                            ordered[idx + 1][3],
                            f"{group}-{s_cur}->{s_nxt}",
                            f"lightness is not strictly decreasing ({ordered[idx][2]:.1f}% -> {ordered[idx + 1][2]:.1f}%)",
                        )
                    )
                    break

            if group.lower() in ("neutral", "gray", "grey") and all(v[1] < 1.0 for v in ordered):
                findings.append(
                    Finding(
                        "ERROR",
                        "§5.5.1",
                        "achromatic-neutral",
                        str(path),
                        first_line,
                        group,
                        "neutral ramp has ~0% saturation everywhere; add cool or warm hue tint (§5.5.1)",
                    )
                )

            s500, l500 = hsl_steps[500][1], hsl_steps[500][2]
            if s500 > 15.0:
                for edge in (100, 900):
                    _, s_edge, l_edge, ln_edge = hsl_steps[edge]
                    if abs(l_edge - 50.0) > abs(l500 - 50.0) and s_edge < s500 * 0.65 and s_edge < 90.0:
                        findings.append(
                            Finding(
                                "WARN",
                                "§5.4",
                                "washed-out-edge",
                                str(path),
                                ln_edge,
                                f"{group}-{edge}",
                                f"edge saturation ({s_edge:.0f}%) dropped far below 500 ({s500:.0f}%); raise saturation as lightness leaves 50% (§5.4)",
                            )
                        )
    return findings


BRIEF_REQUIRED_KEYS = (
    ("Visual thesis:", "15-direction", "missing 'Visual thesis:' direction line"),
    ("Content plan:", "15-direction", "missing 'Content plan:' direction line"),
    ("Interaction thesis:", "15-direction", "missing 'Interaction thesis:' direction line"),
    ("Rules read:", "Read Gate", "missing 'Rules read:' citation line"),
    ("Canvas & measure:", "§3.3 / §4.3", "missing 'Canvas & measure:' constraint"),
    ("Type & leading:", "§4.1 / §4.5", "missing 'Type & leading:' constraint"),
    ("Density & spacing:", "§3.1.2 / §3.6", "missing 'Density & spacing:' constraint"),
    ("Alignment & depth:", "§4.4 / §6.1.3", "missing 'Alignment & depth:' constraint"),
    ("Hierarchy & empty state:", "§2.1 / §8.4", "missing 'Hierarchy & empty state:' constraint"),
)
REQUIRED_BUILD_LENSES = ("02", "03", "04", "06", "10", "15")


def check_brief_files(paths: list[Path]) -> list[Finding]:
    """Verify the 3-line direction + 6-item Constraint Brief schema and Read Gate citations."""
    combined_parts: list[str] = []
    for p in paths:
        combined_parts.append(p.read_text(encoding="utf-8", errors="replace"))
    combined = "\n".join(combined_parts)
    ref_file = str(paths[0])
    findings: list[Finding] = []

    for key, rule_id, msg in BRIEF_REQUIRED_KEYS:
        m = re.search(rf"^\s*(?:[/*#-]*\s*)?{re.escape(key)}\s*(.*)$", combined, re.IGNORECASE | re.MULTILINE)
        if not m or not m.group(1).strip():
            findings.append(Finding("ERROR", rule_id, "missing-brief-key", ref_file, 1, key, msg))

    rules_match = re.search(r"Rules read:\s*(.+)", combined, re.IGNORECASE)
    if rules_match:
        rules_val = rules_match.group(1)
        missing_lenses = [lens for lens in REQUIRED_BUILD_LENSES if not re.search(rf"\b{lens}(?:-[\w]+)?\b", rules_val)]
        if missing_lenses:
            findings.append(
                Finding(
                    "ERROR",
                    "Read Gate",
                    "missing-lens-read",
                    ref_file,
                    1,
                    "Rules read",
                    f"Rules read is missing required Build lens reference(s): {', '.join(missing_lenses)} (expected 02, 03, 04, 06, 10, 15)",
                )
            )
        if "§" not in rules_val:
            findings.append(
                Finding(
                    "ERROR",
                    "Read Gate",
                    "missing-rule-citation",
                    ref_file,
                    1,
                    "Rules read",
                    "Rules read must cite concrete §id values extracted from the lens files",
                )
            )
    return findings


def check_report_file(path: Path) -> list[Finding]:
    """Verify non-CSS delivery obligations in a final Build/Review report."""
    text = sys.stdin.read() if str(path) == "-" else path.read_text(encoding="utf-8", errors="replace")
    label = "<stdin>" if str(path) == "-" else str(path)
    findings: list[Finding] = []

    if not re.search(r"§\d+(?:\.\d+)*", text):
        findings.append(
            Finding(
                "ERROR",
                "Build Gate 4",
                "missing-traceability",
                label,
                1,
                "report",
                "delivery report has 0 §id rule traceability citations",
            )
        )

    verdicts = re.findall(r"\b(Clear|Hit)\b", text, re.IGNORECASE)
    if len(verdicts) < 5 or not re.search(r"AI\s+Slop\s+Test", text, re.IGNORECASE):
        findings.append(
            Finding(
                "ERROR",
                "15-direction",
                "incomplete-slop-test",
                label,
                1,
                "AI Slop Test",
                "report must include 'AI Slop Test' with all 5 reflex checks marked Clear or Hit",
            )
        )

    headless_claim = re.search(r"(无浏览器|无法渲染|未渲染|no browser|cannot render|static only)", text, re.IGNORECASE)
    if headless_claim:
        has_unverified_list = re.search(r"(未核验|unverified)", text, re.IGNORECASE) and re.search(
            r"^\s*(?:[-*]|\d+\.)\s+\S+", text, re.MULTILINE
        )
        if not has_unverified_list:
            findings.append(
                Finding(
                    "ERROR",
                    "Visual Evidence",
                    "missing-unverified-list",
                    label,
                    1,
                    "Visual Evidence",
                    "headless/static claim requires an explicit bulleted list of unverified visual items ('未核验项')",
                )
            )
    return findings


def main() -> int:
    ap = argparse.ArgumentParser(description="Static UI rule checker for mm-ui")
    ap.add_argument("paths", nargs="*", help="CSS/HTML/Vue/Svelte files or directories to scan")
    ap.add_argument("--strict", action="store_true", help="treat warnings as failures (exit 1)")
    ap.add_argument("--pass1", action="store_true", help="enforce Pass 1 grayscale purity (no accent/status/shadows)")
    ap.add_argument("--tokens", metavar="FILE", help="validate 9-step color ramps in tokens.css or tokens.json")
    ap.add_argument("--brief", nargs="+", metavar="FILE", help="validate 3-line direction + 6-item constraint brief")
    ap.add_argument("--report", metavar="FILE", help="validate delivery report (§id traceability, 5-item AI Slop Test, unverified items)")
    args = ap.parse_args()

    if not args.paths and not args.tokens and not args.brief and not args.report:
        ap.print_help()
        return 2

    check_exists: list[str] = list(args.paths)
    if args.tokens:
        check_exists.append(args.tokens)
    if args.brief:
        check_exists.extend(args.brief)
    if args.report and args.report != "-":
        check_exists.append(args.report)

    missing = [p for p in check_exists if not Path(p).exists()]
    if missing:
        for p in missing:
            print(f"error: path not found: {p}", file=sys.stderr)
        return 2

    findings: list[Finding] = []
    for raw_path in args.paths:
        findings.extend(scan_path(Path(raw_path), pass1=args.pass1))
    if args.tokens:
        findings.extend(check_tokens_file(Path(args.tokens)))
    if args.brief:
        findings.extend(check_brief_files([Path(p) for p in args.brief]))
    if args.report:
        findings.extend(check_report_file(Path(args.report)))

    errors = [f for f in findings if f.severity == "ERROR"]
    warnings = [f for f in findings if f.severity == "WARN"]

    if not findings:
        print("check_ui_rules: 0 errors, 0 warnings — pass")
        return 0

    for f in findings:
        print(f"{f.severity:<5} [{f.rule_id}] {f.file}:{f.line} ({f.selector}) -> {f.message}")

    print(f"\nsummary: {len(errors)} error(s), {len(warnings)} warning(s)")
    if errors or (args.strict and warnings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
