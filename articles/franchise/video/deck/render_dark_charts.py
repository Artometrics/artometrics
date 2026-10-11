#!/usr/bin/env python3
"""Rebuild franchise motion charts as dark-theme SVG HTML for the storyboard decks."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
JSON_DIR = ROOT / "public/data/articles/franchise/charts"
OUT_DIRS = [
    Path(__file__).resolve().parent.parent / "assets" / "charts",
    ROOT / "articles/franchise/charts",
    ROOT / "public/data/articles/franchise/charts",
    ROOT / "public/images/content/articles/franchise/charts",
]

COPY = {
    "chart1_top20_revenue": (
        "A handful of names carry the lifetime table.",
        "Top 20 franchise rows · n=103 in the mid-2019 file",
        "Source: S001 · TidyTuesday franchise ledger",
    ),
    "chart2_revenue_per_year": (
        "Speed is a design choice, not just age.",
        "Lifetime revenue divided by years since first release",
        "Source: S001 · n=103 franchises",
    ),
    "chart3a_disney_non_consolidated": (
        "Before the roll-up, Disney is a shorter stack.",
        "Franchise rows kept on their original owner labels",
        "Source: S001 · owner labels as published",
    ),
    "chart3b_disney_consolidated": (
        "Rolling subsidiaries changes who looks largest.",
        "Marvel, Lucasfilm, Pixar and Fox rows under Disney",
        "Source: S001 · consolidated owner view",
    ),
    "chart5_original_media_revenue": (
        "Where a story started is not where the money sits.",
        "Revenue by original medium",
        "Source: S001 · n=103 franchises",
    ),
    "chart6_revenue_streams": (
        "Merchandise is most of the file. Theatre is not.",
        "Share of lifetime revenue by stream · n=103",
        "Source: S001 · TidyTuesday / mid-2019 Wikipedia scrape",
    ),
    "chart7_top10_franchise_share": (
        "Nine of ten domestic hits were already franchises.",
        "Share of yearly top-ten films coded as franchise titles",
        "Source: Box Office Mojo yearly charts · S001 coding",
    ),
    "chart8_disney_acquisitions": (
        "The cheque is small next to the lifetime row.",
        "Deal price ($bn) vs franchise-row revenue ($bn)",
        "Source: SEC filings + S001 franchise rows",
    ),
    "chart9_disney_segments_fy2024": (
        "Parks and products sit beside the films.",
        "Disney segment revenue, FY2024",
        "Source: Disney FY2024 report",
    ),
    "chart10_wiki_2019_vs_2026": (
        "The same names moved between 2019 and 2026.",
        "Percent change, top movers · n=20 matched franchises",
        "Source: S001 + S017 · methodology, not a cash loss",
    ),
    "chart11_mix_by_original_medium": (
        "Games, manga and film do not share one mix.",
        "Revenue-stream mix by original medium",
        "Source: S001 · n=103 franchises",
    ),
    "chart12_owner_concentration": (
        "Five owners hold nearly half the file.",
        "Share of franchise-row revenue by owner",
        "Source: S001 · consolidated labels",
    ),
    "chart13_deal_price_vs_revenue": (
        "Price paid is not the lifetime total.",
        "Acquisition price against the franchise row",
        "Source: SEC deal prices + S001",
    ),
    "chart14_box_office_share_top20": (
        "Theatrical share is a thin slice for most names.",
        "Box office as a share of the franchise row",
        "Source: S001 · top 20 by lifetime revenue",
    ),
    "chart15_region_japan_us_other": (
        "Japan and the US split the ledger. The UK is third.",
        "Franchise-row revenue by region of origin · n=103",
        "Source: S001 · region_origin, hand-audited",
    ),
}


def esc(s: str) -> str:
    return html.escape(str(s), quote=True)


def strip_tags(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s or "")


def series_from_trace(tr: dict) -> tuple[list[str], list[float]]:
    if tr.get("type") == "pie":
        labels = [str(x) for x in tr.get("labels") or []]
        vals = [float(v) for v in tr.get("values") or []]
        return labels, vals
    xs, ys = tr.get("x") or [], tr.get("y") or []
    if tr.get("orientation") == "h" or (
        ys and xs and all(isinstance(y, str) for y in ys) and all(isinstance(x, (int, float)) for x in xs)
    ):
        return [str(y) for y in ys], [float(x) for x in xs]
    if xs and ys and all(isinstance(x, str) for x in xs) and all(isinstance(y, (int, float)) for y in ys):
        return [str(x) for x in xs], [float(y) for y in ys]
    text = tr.get("text") or []
    if text and ys and all(isinstance(y, (int, float)) for y in ys):
        labels = [str(t) for t in text]
        return labels, [float(y) for y in ys]
    if xs and ys and all(isinstance(x, (int, float)) for x in xs) and all(isinstance(y, (int, float)) for y in ys):
        labels = [str(t) for t in text] if text else [str(i + 1) for i in range(len(xs))]
        return labels, [float(y) for y in ys]
    return [], []


def merge_traces(spec: dict) -> tuple[list[str], list[float]]:
    labels: list[str] = []
    values: list[float] = []
    for tr in spec.get("data") or []:
        ls, vs = series_from_trace(tr)
        if not ls:
            continue
        if not labels:
            labels, values = ls, vs
        elif ls == labels and len(vs) == len(values):
            # stacked: keep the largest trace rather than summing unknowns
            if sum(abs(v) for v in vs) > sum(abs(v) for v in values):
                values = vs
        elif len(ls) > len(labels):
            labels, values = ls, vs
    # drop non-positive noise but keep zeros out of the drawn set
    pairs = [(l, v) for l, v in zip(labels, values) if l]
    pairs.sort(key=lambda p: p[1])
    return [p[0] for p in pairs], [p[1] for p in pairs]


def svg_bars(labels: list[str], values: list[float], highlight: str) -> str:
    if not values:
        return ""
    n = len(labels)
    row_h = 28 if n > 14 else 36 if n > 8 else 48
    h = 80 + n * row_h
    w = 1600
    label_w = 340
    plot_w = w - label_w - 120
    vmax = max(abs(v) for v in values) or 1
    hi = highlight.lower().strip()
    parts = [
        f'<svg class="chart-svg" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img">',
        f'<line class="stage-axes" x1="{label_w}" y1="24" x2="{label_w}" y2="{h - 28}" stroke="#3a3a3a" stroke-width="1"/>',
        f'<line class="stage-axes" x1="{label_w}" y1="{h - 28}" x2="{w - 40}" y2="{h - 28}" stroke="#3a3a3a" stroke-width="1"/>',
    ]
    for i, (lab, val) in enumerate(zip(labels, values)):
        y = 36 + i * row_h
        bw = max(2, abs(val) / vmax * plot_w)
        is_hi = hi and (hi in lab.lower() or lab.lower() in hi)
        if not hi and i == n - 1:
            is_hi = True
        color = "#E60000" if is_hi else "#6a6a6a"
        parts.append(
            f'<text class="stage-axes" x="{label_w - 12}" y="{y + row_h * 0.55}" text-anchor="end" '
            f'fill="#d0d0d0" font-family="DM Mono, monospace" font-size="14">{esc(lab[:28])}</text>'
        )
        parts.append(
            f'<rect class="stage-data bar" x="{label_w}" y="{y + 6}" width="{bw:.1f}" height="{row_h - 14}" '
            f'fill="{color}" style="animation-delay:{0.35 + i * 0.04:.2f}s"/>'
        )
        parts.append(
            f'<text class="stage-data" x="{label_w + bw + 8:.1f}" y="{y + row_h * 0.55}" '
            f'fill="#fff" font-family="DM Mono, monospace" font-size="15" '
            f'style="animation-delay:{0.35 + i * 0.04:.2f}s">{val:g}</text>'
        )
        if is_hi:
            parts.append(
                f'<rect class="stage-highlight" x="{label_w - 4}" y="{y + 2}" width="{bw + 78:.1f}" height="{row_h - 6}" '
                f'fill="none" stroke="#E60000" stroke-width="3"/>'
            )
    parts.append("</svg>")
    return "\n".join(parts)


def svg_dots(labels: list[str], values: list[float], highlight: str) -> str:
    if not values:
        return ""
    w, h = 1600, 640
    pad_l, pad_b = 80, 70
    vmax = max(values) or 1
    vmin = min(values)
    span = (vmax - vmin) or 1
    hi = highlight.lower()
    parts = [
        f'<svg class="chart-svg" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">',
        f'<line class="stage-axes" x1="{pad_l}" y1="40" x2="{pad_l}" y2="{h - pad_b}" stroke="#3a3a3a"/>',
        f'<line class="stage-axes" x1="{pad_l}" y1="{h - pad_b}" x2="{w - 40}" y2="{h - pad_b}" stroke="#3a3a3a"/>',
    ]
    n = len(values)
    for i, (lab, val) in enumerate(zip(labels, values)):
        x = pad_l + 40 + (i + 0.5) * ((w - pad_l - 80) / max(n, 1))
        y = (h - pad_b) - ((val - vmin) / span) * (h - pad_b - 80)
        is_hi = hi and hi in lab.lower()
        color = "#E60000" if is_hi else "#0047FF"
        parts.append(
            f'<circle class="stage-data" cx="{x:.1f}" cy="{y:.1f}" r="8" fill="{color}" '
            f'style="animation-delay:{0.4 + i * 0.08:.2f}s"/>'
        )
        parts.append(
            f'<text class="stage-data" x="{x:.1f}" y="{h - 28}" text-anchor="middle" fill="#bbb" '
            f'font-family="DM Mono, monospace" font-size="13">{esc(lab[:18])}</text>'
        )
        if is_hi or (not hi and i == max(range(n), key=lambda k: values[k])):
            parts.append(
                f'<rect class="stage-highlight" x="{x - 36:.1f}" y="{y - 28:.1f}" width="72" height="40" '
                f'fill="none" stroke="#E60000" stroke-width="3"/>'
            )
    parts.append("</svg>")
    return "\n".join(parts)


def build_html(name: str, spec: dict) -> str:
    headline, subtitle, source = COPY.get(
        name,
        ("The file, drawn.", "Franchise ledger", "Source: S001"),
    )
    labels, values = merge_traces(spec)
    kind = (spec.get("data") or [{}])[0].get("type", "bar")
    body = svg_dots(labels, values, "") if kind == "scatter" else svg_bars(labels, values, "")
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;600;700&family=DM+Mono:wght@400;500&display=swap"/>
<style>
  html,body {{ margin:0; height:100%; background:#0a0a0a; color:#fff; }}
  body {{ display:flex; flex-direction:column; padding:28px 36px 18px; box-sizing:border-box; font-family:"DM Sans",sans-serif; }}
  h1 {{ font-size:34px; font-weight:600; margin:0 0 8px; letter-spacing:-0.02em; }}
  .sub {{ font-family:"DM Mono",monospace; font-size:16px; color:#9a9a9a; margin:0 0 18px; }}
  .plot {{ flex:1; min-height:0; }}
  .chart-svg {{ width:100%; height:100%; }}
  .src {{ font-family:"DM Mono",monospace; font-size:14px; color:#8a8a8a; margin:10px 0 0; }}
  .stage-data {{ opacity:0; animation:rise .7s ease forwards; }}
  .stage-highlight {{ opacity:0; animation:rise .35s ease 1.15s forwards; }}
  .bar {{ transform-box:fill-box; transform-origin:left center; }}
  @keyframes rise {{ from {{ opacity:0; }} to {{ opacity:1; }} }}
</style></head>
<body>
  <h1>{esc(headline)}</h1>
  <p class="sub">{esc(subtitle)}</p>
  <div class="plot">{body}</div>
  <p class="src">{esc(source)}</p>
  <script>
    const q = new URLSearchParams(location.search);
    const hl = (q.get("hl") || "").toLowerCase();
    if (hl) {{
      document.querySelectorAll(".chart-svg text").forEach((t) => {{
        if (t.textContent.toLowerCase().includes(hl)) {{
          const y = t.getAttribute("y");
          t.setAttribute("fill", "#fff");
        }}
      }});
    }}
    setTimeout(() => document.body.setAttribute("data-chart-ready", "1"), 1500);
  </script>
</body></html>
"""


def main() -> None:
    for path in sorted(JSON_DIR.glob("chart*.plotly.json")):
        name = path.name.replace(".plotly.json", "")
        spec = json.loads(path.read_text(encoding="utf-8"))
        doc = build_html(name, spec)
        for folder in OUT_DIRS:
            folder.mkdir(parents=True, exist_ok=True)
            dest = folder / f"{name}.html"
            # video assets use chart_chartN_ prefix
            dest.write_text(doc, encoding="utf-8")
            if folder.name == "charts" and "video" in str(folder):
                (folder / f"chart_{name}.html").write_text(doc, encoding="utf-8")
        print(name, "ok", len(merge_traces(spec)[0]), "rows")


if __name__ == "__main__":
    main()
