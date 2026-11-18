#!/usr/bin/env python3
"""Build a side-by-side interactive comparison page (`style-explorer.html`) for Explore mode.

Accepts either an exploration directory containing `manifest.json` or explicit
HTML candidate files, and generates a single self-contained `style-explorer.html`
with desktop (1440px scaled) and mobile (400px) viewport toggles plus a selection
export bar so the user can inspect and pick a structural direction side-by-side.

Usage:
    build_explorer.py explore/manifest.json --out explore/style-explorer.html
    build_explorer.py option-a.html option-b.html option-c.html --out style-explorer.html
"""

from __future__ import annotations

import argparse
import html
import json
import os
import sys
from pathlib import Path
from typing import Any


def _load_candidates(inputs: list[str], out_path: Path) -> tuple[str, str, list[dict[str, Any]]]:
    title = "Direction Exploration"
    recommendation = ""
    items: list[dict[str, Any]] = []

    if len(inputs) == 1 and (Path(inputs[0]).is_dir() or inputs[0].lower().endswith(".json")):
        manifest_path = Path(inputs[0]) / "manifest.json" if Path(inputs[0]).is_dir() else Path(inputs[0])
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        title = str(data.get("title") or title)
        recommendation = str(data.get("recommendation") or "")
        base = manifest_path.parent
        for idx, entry in enumerate(data.get("directions", []), 1):
            raw_file = str(entry.get("file") or "")
            src_path = (base / raw_file).resolve()
            rel_src = os.path.relpath(src_path, out_path.parent.resolve()).replace(os.sep, "/")
            items.append(
                {
                    "id": entry.get("id") or f"option-{idx}",
                    "name": entry.get("name") or f"Option {idx}",
                    "thesis": entry.get("thesis") or "",
                    "density": entry.get("density") or "standard",
                    "trade_offs": entry.get("trade_offs") or entry.get("tradeOffs") or "",
                    "recommended": bool(entry.get("recommended", False)),
                    "src": rel_src,
                }
            )
    else:
        for idx, raw in enumerate(inputs, 1):
            src_path = Path(raw).resolve()
            rel_src = os.path.relpath(src_path, out_path.parent.resolve()).replace(os.sep, "/")
            items.append(
                {
                    "id": f"option-{idx}",
                    "name": src_path.stem.replace("-", " ").replace("_", " ").title(),
                    "thesis": "",
                    "density": "standard",
                    "trade_offs": "",
                    "recommended": False,
                    "src": rel_src,
                }
            )

    if not items:
        raise ValueError("no direction HTML files supplied")
    return title, recommendation, items


def render_explorer_html(title: str, recommendation: str, candidates: list[dict[str, Any]]) -> str:
    cards_html: list[str] = []
    for c in candidates:
        rec_badge = '<span class="badge-rec">Recommended</span>' if c["recommended"] else ""
        thesis_html = f'<p class="card-thesis">{html.escape(c["thesis"])}</p>' if c["thesis"] else ""
        trade_html = f'<p class="card-meta"><strong>Trade-offs:</strong> {html.escape(c["trade_offs"])}</p>' if c["trade_offs"] else ""
        cards_html.append(
            f"""
            <article class="dir-card" data-id="{html.escape(c['id'])}">
              <header class="card-head">
                <div class="card-title-row">
                  <h2>{html.escape(c['name'])}</h2>
                  <div class="badges">
                    <span class="badge-density">{html.escape(c['density'])}</span>
                    {rec_badge}
                  </div>
                </div>
                {thesis_html}
                {trade_html}
              </header>
              <div class="stage-wrap">
                <div class="frame-shell">
                  <iframe src="{html.escape(c['src'])}" title="{html.escape(c['name'])}" loading="lazy"></iframe>
                </div>
              </div>
              <footer class="card-foot">
                <a class="link-open" href="{html.escape(c['src'])}" target="_blank" rel="noopener">Open standalone</a>
                <button type="button" class="btn-select" data-select-name="{html.escape(c['name'])}">Select this direction</button>
              </footer>
            </article>
            """
        )

    rec_banner = (
        f'<p class="rec-summary"><strong>Lead recommendation:</strong> {html.escape(recommendation)}</p>'
        if recommendation
        else ""
    )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(title)} · mm-ui Explorer</title>
  <style>
    :root {{
      --surface: #f4f5f7;
      --surface-raised: #fcfcfd;
      --surface-sunken: #e8eaef;
      --text: #18181b;
      --text-secondary: #3f3f46;
      --text-muted: #52525b;
      --border: #d4d4d8;
      --accent: #1d4ed8;
      --accent-hover: #1e40af;
      --accent-subtle: #dbeafe;
      --accent-fg: #f8fafc;
      --frame-w: 1440px;
      --frame-scale: 0.32;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans", sans-serif;
      background: var(--surface);
      color: var(--text);
      line-height: 1.5;
    }}
    .topbar {{
      position: sticky;
      top: 0;
      z-index: 20;
      background: var(--surface-raised);
      border-bottom: 1px solid var(--border);
      padding: 16px 24px;
      display: flex;
      flex-wrap: wrap;
      align-items: baseline;
      justify-content: space-between;
      gap: 16px;
    }}
    .topbar h1 {{
      margin: 0;
      font-size: 20px;
      line-height: 1.2;
      font-weight: 600;
    }}
    .rec-summary {{
      margin: 4px 0 0;
      font-size: 14px;
      color: var(--text-secondary);
      max-width: 70ch;
    }}
    .controls {{
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .vp-btn {{
      height: 36px;
      padding: 0 12px;
      border-radius: 6px;
      border: 1px solid var(--border);
      background: var(--surface-raised);
      color: var(--text);
      font-size: 14px;
      font-weight: 500;
      cursor: pointer;
    }}
    .vp-btn[aria-pressed="true"] {{
      background: var(--accent);
      border-color: var(--accent);
      color: var(--accent-fg);
    }}
    .grid {{
      max-width: 1440px;
      margin: 0 auto;
      padding: 24px;
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
      gap: 24px;
    }}
    .dir-card {{
      background: var(--surface-raised);
      border: 1px solid var(--border);
      border-radius: 8px;
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }}
    .dir-card.is-selected {{
      outline: 2px solid var(--accent);
      outline-offset: 2px;
    }}
    .card-head {{
      padding: 16px;
      border-bottom: 1px solid var(--border);
    }}
    .card-title-row {{
      display: flex;
      align-items: baseline;
      justify-content: space-between;
      gap: 12px;
    }}
    .card-head h2 {{
      margin: 0;
      font-size: 18px;
      line-height: 1.25;
      font-weight: 600;
    }}
    .badges {{
      display: flex;
      gap: 8px;
      flex-shrink: 0;
    }}
    .badge-density, .badge-rec {{
      font-size: 12px;
      line-height: 1.2;
      padding: 4px 8px;
      border-radius: 4px;
      font-weight: 600;
    }}
    .badge-density {{
      background: var(--surface-sunken);
      color: var(--text-secondary);
    }}
    .badge-rec {{
      background: var(--accent-subtle);
      color: var(--accent-hover);
    }}
    .card-thesis {{
      margin: 8px 0 0;
      font-size: 14px;
      color: var(--text-secondary);
      max-width: 65ch;
    }}
    .card-meta {{
      margin: 8px 0 0;
      font-size: 12px;
      color: var(--text-muted);
      max-width: 65ch;
    }}
    .stage-wrap {{
      background: var(--surface-sunken);
      padding: 16px;
      display: flex;
      justify-content: center;
      overflow: hidden;
    }}
    .frame-shell {{
      width: calc(var(--frame-w) * var(--frame-scale));
      max-width: 100%;
      height: 360px;
      overflow: hidden;
      border: 1px solid var(--border);
      border-radius: 6px;
      background: var(--surface-raised);
    }}
    .frame-shell iframe {{
      width: var(--frame-w);
      height: calc(360px / var(--frame-scale));
      border: 0;
      transform: scale(var(--frame-scale));
      transform-origin: top left;
      background: #fff;
    }}
    .card-foot {{
      padding: 12px 16px;
      border-top: 1px solid var(--border);
      display: flex;
      align-items: baseline;
      justify-content: space-between;
      gap: 12px;
    }}
    .link-open {{
      font-size: 14px;
      color: var(--accent);
      text-decoration: none;
      font-weight: 500;
    }}
    .link-open:hover {{ text-decoration: underline; }}
    .btn-select {{
      height: 36px;
      padding: 0 16px;
      border-radius: 6px;
      border: 0;
      background: var(--accent);
      color: var(--accent-fg);
      font-size: 14px;
      font-weight: 600;
      cursor: pointer;
    }}
    .btn-select:hover {{ background: var(--accent-hover); }}
    .selection-bar {{
      max-width: 1440px;
      margin: 0 auto 24px;
      padding: 0 24px;
    }}
    .selection-box {{
      background: var(--surface-raised);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 12px 16px;
      font-size: 14px;
      color: var(--text-secondary);
      display: none;
    }}
    .selection-box.visible {{ display: block; }}
    :focus-visible {{
      outline: 2px solid var(--accent);
      outline-offset: 2px;
    }}
  </style>
</head>
<body>
  <header class="topbar">
    <div>
      <h1>{html.escape(title)}</h1>
      {rec_banner}
    </div>
    <div class="controls" role="group" aria-label="Preview viewport">
      <button type="button" class="vp-btn" data-vp="desktop" aria-pressed="true">Desktop 1440px</button>
      <button type="button" class="vp-btn" data-vp="mobile" aria-pressed="false">Mobile 400px</button>
    </div>
  </header>

  <main class="grid">
    {''.join(cards_html)}
  </main>

  <section class="selection-bar" aria-live="polite">
    <div id="selection-box" class="selection-box"></div>
  </section>

  <script>
    const root = document.documentElement;
    let currentFrameW = 1440;
    function fitFrames() {{
      root.style.setProperty('--frame-w', `${{currentFrameW}}px`);
      for (const wrap of document.querySelectorAll('.stage-wrap')) {{
        const availW = Math.max(240, wrap.clientWidth - 32);
        const scale = Math.min(1, availW / currentFrameW);
        wrap.style.setProperty('--frame-scale', scale.toFixed(4));
      }}
    }}
    fitFrames();
    window.addEventListener('resize', fitFrames);
    for (const btn of document.querySelectorAll('.vp-btn')) {{
      btn.addEventListener('click', () => {{
        currentFrameW = btn.dataset.vp === 'mobile' ? 400 : 1440;
        fitFrames();
        for (const b of document.querySelectorAll('.vp-btn')) {{
          b.setAttribute('aria-pressed', String(b === btn));
        }}
      }});
    }}
    const box = document.getElementById('selection-box');
    for (const btn of document.querySelectorAll('.btn-select')) {{
      btn.addEventListener('click', async () => {{
        for (const card of document.querySelectorAll('.dir-card')) card.classList.remove('is-selected');
        btn.closest('.dir-card').classList.add('is-selected');
        const msg = `Selected direction: ${{btn.dataset.selectName}} — ready to proceed to Build mode.`;
        box.textContent = msg;
        box.classList.add('visible');
        if (navigator.clipboard && navigator.clipboard.writeText) {{
          try {{ await navigator.clipboard.writeText(msg); }} catch (_) {{}}
        }}
      }});
    }}
  </script>
</body>
</html>
"""


def main() -> int:
    ap = argparse.ArgumentParser(description="Build side-by-side style-explorer.html from Explore prototypes")
    ap.add_argument("inputs", nargs="+", help="manifest.json (or dir) OR 2+ HTML prototype files")
    ap.add_argument("--out", default="style-explorer.html", help="output HTML file path (default: style-explorer.html)")
    args = ap.parse_args()

    for p in args.inputs:
        if not Path(p).exists():
            print(f"error: path not found: {p}", file=sys.stderr)
            return 2

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        title, recommendation, candidates = _load_candidates(args.inputs, out_path)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    out_path.write_text(render_explorer_html(title, recommendation, candidates), encoding="utf-8")
    print(f"built explorer: {out_path} ({len(candidates)} directions)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
