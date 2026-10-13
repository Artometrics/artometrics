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
]

COPY = {
    "chart1_top20_revenue": (
        "A handful of names carry the lifetime table.",
        "Top 20 franchise rows · n=103 in the 2019 Wikipedia-based dataset",
        "Source: the 2019 Wikipedia-based dataset",
    ),
    "chart2_revenue_per_year": (
        "Speed is a design choice, not just age.",
        "Lifetime revenue divided by years since first release",
        "Source: the 2019 Wikipedia-based dataset · n=103 franchises",
    ),
    "chart3a_disney_non_consolidated": (
        "Before the roll-up, Disney is a shorter stack.",
        "Franchise rows kept on their original owner labels",
        "Source: the 2019 Wikipedia-based dataset · owner labels as published",
    ),
    "chart3b_disney_consolidated": (
        "Rolling subsidiaries changes who looks largest.",
        "Marvel, Lucasfilm, Pixar and Fox rows under Disney",
        "Source: the 2019 Wikipedia-based dataset · consolidated owner view",
    ),
    "chart5_original_media_revenue": (
        "Where a story started is not where the money sits.",
        "Revenue by original medium",
        "Source: the 2019 Wikipedia-based dataset · n=103 franchises",
    ),
    "chart6_revenue_streams": (
        "Merchandise is most of the file. Theatre is not.",
        "Share of lifetime revenue by stream · n=103",
        "Source: the 2019 Wikipedia-based dataset",
    ),
    "chart7_top10_franchise_share": (
        "Nine of ten domestic hits were already franchises.",
        "Share of yearly top-ten films coded as franchise titles",
        "Source: Box Office Mojo yearly charts",
    ),
    "chart8_disney_acquisitions": (
        "The cheque is small next to the lifetime row.",
        "Deal price ($bn) vs franchise-row revenue ($bn)",
        "Source: SEC filings and the 2019 Wikipedia-based dataset",
    ),
    "chart9_disney_segments_fy2024": (
        "Parks and products sit beside the films.",
        "Disney segment revenue, FY2024",
        "Source: Disney FY2024 report",
    ),
    "chart10_wiki_2019_vs_2026": (
        "The same names moved between 2019 and 2026.",
        "Percent change, top movers · n=20 matched franchises",
        "Source: the 2019 Wikipedia-based dataset and the 2026 Wikipedia list · methodology, not a cash loss",
    ),
    "chart11_mix_by_original_medium": (
        "Games, manga and film do not share one mix.",
        "Revenue-stream mix by original medium",
        "Source: the 2019 Wikipedia-based dataset · n=103 franchises",
    ),
    "chart12_owner_concentration": (
        "Five owners hold nearly half the file.",
        "Share of franchise-row revenue by owner",
        "Source: the 2019 Wikipedia-based dataset · consolidated labels",
    ),
    "chart13_deal_price_vs_revenue": (
        "Price paid is not the lifetime total.",
        "Acquisition price against the franchise row",
        "Source: SEC deal prices and the 2019 Wikipedia-based dataset",
    ),
    "chart14_box_office_share_top20": (
        "Theatrical share is a thin slice for most names.",
        "Box office as a share of the franchise row",
        "Source: the 2019 Wikipedia-based dataset · top 20 by lifetime revenue",
    ),
    "chart15_region_japan_us_other": (
        "Japan and the US split the ledger. The UK is third.",
        "Franchise-row revenue by region of origin · n=103",
        "Source: the 2019 Wikipedia-based dataset · region of origin, hand-audited",
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
        if all(1900 <= float(x) <= 2100 for x in xs):
            return [str(int(x)) for x in xs], [float(y) for y in ys]
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


# viewBox matches an 80% × 65% stage at 1920×1080 so 20px type is 20px on screen.
FRAME_W, FRAME_H = 1536, 702
FONT = 22

UNIT = {
    "chart6_revenue_streams": "%",
    "chart7_top10_franchise_share": "%",
    "chart10_wiki_2019_vs_2026": "%",
    "chart12_owner_concentration": "%",
    "chart14_box_office_share_top20": "%",
    "chart1_top20_revenue": "$bn",
    "chart2_revenue_per_year": "$bn/yr",
    "chart3a_disney_non_consolidated": "$bn",
    "chart3b_disney_consolidated": "$bn",
    "chart5_original_media_revenue": "$bn",
    "chart8_disney_acquisitions": "$bn",
    "chart9_disney_segments_fy2024": "$bn",
    "chart11_mix_by_original_medium": "%",
    "chart13_deal_price_vs_revenue": "$bn",
    "chart15_region_japan_us_other": "$bn",
}


def fmt_unit(val: float, unit: str) -> str:
    if unit == "%":
        text = f"{val:.1f}".rstrip("0").rstrip(".")
        return f"{text}%"
    if unit.startswith("$"):
        text = f"{val:.1f}".rstrip("0").rstrip(".")
        return f"${text}{unit[1:]}" if unit != "$bn" else f"${text}bn"
    if unit:
        return f"{val:g} {unit}"
    return f"{val:g}"


def insight_headline(name: str, labels: list[str], values: list[float]) -> str:
    unit = UNIT.get(name, "")
    if name == "chart6_revenue_streams":
        return "Merchandise is 56% of all franchise revenue. Box office is 8.9%."
    if not values:
        return COPY.get(name, ("The file, drawn.", "", ""))[0]
    order = sorted(zip(labels, values), key=lambda p: abs(p[1]), reverse=True)
    a_lab, a_val = order[0]
    if len(order) > 1:
        b_lab, b_val = order[1]
        return f"{a_lab} is {fmt_unit(a_val, unit)}. {b_lab} is {fmt_unit(b_val, unit)}."
    return f"{a_lab} is {fmt_unit(a_val, unit)}."


def svg_bars(labels: list[str], values: list[float], highlight: str, unit: str = "", blue_label: str = "", mark_max: bool = False) -> str:
    if not values:
        return ""
    n = len(labels)
    w, h = FRAME_W, FRAME_H
    label_w = 420
    plot_w = w - label_w - 150
    top, bot = 16, 28
    row_h = (h - top - bot) / max(n, 1)
    vmax = max(abs(v) for v in values) or 1
    hi = highlight.lower().strip()
    blue = blue_label.lower().strip()
    parts = [
        f'<svg class="chart-svg" viewBox="0 0 {w} {h}" preserveAspectRatio="xMinYMid meet" xmlns="http://www.w3.org/2000/svg" role="img">',
        f'<line class="stage-axes" x1="{label_w}" y1="{top}" x2="{label_w}" y2="{h - bot}" stroke="#4a4a4a" stroke-width="2"/>',
        f'<line class="stage-axes" x1="{label_w}" y1="{h - bot}" x2="{w - 36}" y2="{h - bot}" stroke="#4a4a4a" stroke-width="2"/>',
        f'<text class="stage-axes" x="{w - 36}" y="{h - 8}" text-anchor="end" fill="#9a9a9a" font-family="DM Mono, monospace" font-size="{FONT - 2}">{esc(unit or "value")}</text>',
    ]
    for i, (lab, val) in enumerate(zip(labels, values)):
        y = top + i * row_h
        bw = max(4, abs(val) / vmax * (plot_w - 90))
        is_hi = bool(hi) and (hi in lab.lower() or lab.lower() in hi)
        is_blue = bool(blue) and blue in lab.lower()
        if mark_max and not hi and not blue and i == n - 1:
            is_hi = True
        color = "#0047FF" if is_hi else "#0047FF" if is_blue else "#6a6a6a"
        shown = fmt_unit(val, unit)
        short = lab.split(",")[0].split("/")[0].strip()[:22]
        parts.append(
            f'<text class="stage-axes" x="{label_w - 16}" y="{y + row_h * 0.62}" text-anchor="end" '
            f'fill="#eee" font-family="DM Mono, monospace" font-size="{FONT}">{esc(short)}</text>'
        )
        parts.append(
            f'<rect class="stage-data bar" x="{label_w}" y="{y + row_h * 0.18:.1f}" width="{bw:.1f}" height="{row_h * 0.64:.1f}" '
            f'fill="{color}" style="animation-delay:{0.25 + i * 0.03:.2f}s"/>'
        )
        parts.append(
            f'<text class="stage-data" x="{label_w + bw + 10:.1f}" y="{y + row_h * 0.62:.1f}" '
            f'fill="#fff" font-family="DM Mono, monospace" font-size="{FONT}" '
            f'style="animation-delay:{0.25 + i * 0.03:.2f}s">{esc(shown)}</text>'
        )
        if is_hi:
            box_w = max(118, 14 * len(shown) + 36)
            parts.append(
                f'<rect class="stage-highlight" x="{label_w + bw - 4:.1f}" y="{y + row_h * 0.22:.1f}" width="{box_w}" height="{row_h * 0.56:.1f}" '
                f'fill="none" stroke="#0047FF" stroke-width="3" opacity="1"/>'
            )
    parts.append("</svg>")
    return "\n".join(parts)


def svg_dots(labels: list[str], values: list[float], highlight: str, mark_max: bool = False, unit: str = "") -> str:
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
        color = "#0047FF" if is_hi else "#0047FF"
        parts.append(
            f'<circle class="stage-data" cx="{x:.1f}" cy="{y:.1f}" r="8" fill="{color}" '
            f'style="animation-delay:{0.4 + i * 0.08:.2f}s"/>'
        )
        parts.append(
            f'<text class="stage-data" x="{x:.1f}" y="{h - 28}" text-anchor="middle" fill="#bbb" '
            f'font-family="DM Mono, monospace" font-size="13">{esc(lab[:18])}</text>'
        )
        if is_hi or (mark_max and not hi and i == max(range(n), key=lambda k: values[k])):
            shown = fmt_unit(val, unit) if unit else f"{val:g}"
            box_w = max(96, 15 * len(shown) + 28)
            parts.append(
                f'<rect class="stage-highlight" x="{x - box_w / 2:.1f}" y="{y - 52:.1f}" width="{box_w:.1f}" height="36" '
                f'fill="none" stroke="#0047FF" stroke-width="3" opacity="1"/>'
            )
            parts.append(
                f'<text class="stage-data" x="{x:.1f}" y="{y - 28:.1f}" text-anchor="middle" fill="#fff" '
                f'font-family="DM Mono, monospace" font-size="18">{esc(shown)}</text>'
            )
    parts.append("</svg>")
    return "\n".join(parts)


def load_spec(name: str) -> dict:
    path = JSON_DIR / f"{name}.plotly.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def chart_series(name: str) -> tuple[list[str], list[float], str]:
    spec = load_spec(name)
    labels, values = merge_traces(spec) if spec else ([], [])
    kind = (spec.get("data") or [{}])[0].get("type", "bar") if spec else "bar"
    return labels, values, kind


def headline_for_highlight(name: str, labels: list[str], values: list[float], highlight: str) -> str:
    if name == "chart6_revenue_streams" and (not highlight or "merch" in highlight.lower()):
        return "Merchandise is 56% of all franchise revenue. Box office is 8.9%."
    unit = UNIT.get(name, "")
    hi = highlight.lower().strip()
    if hi:
        for lab, val in zip(labels, values):
            if hi in lab.lower() or lab.lower() in hi:
                return f"{lab.split(',')[0].split('/')[0].strip()} is {fmt_unit(val, unit)}."
    return insight_headline(name, labels, values)


def chart_parts(name: str, highlight: str | None = None) -> tuple[str, str, str, str]:
    labels, values, kind = chart_series(name)
    explicit = highlight is not None
    hi = highlight or ""
    if not explicit and name == "chart6_revenue_streams":
        hi = "merchandise"
    headline = headline_for_highlight(name, labels, values, hi)
    subtitle, source = COPY.get(name, ("The file, drawn.", "Franchise ledger", "Source: the 2019 Wikipedia-based dataset"))[1:]
    unit = UNIT.get(name, "")
    blue = "box office" if name == "chart6_revenue_streams" else ""
    mark_max = not explicit and not hi
    body = svg_dots(labels, values, hi, mark_max, unit) if kind == "scatter" else svg_bars(labels, values, hi, unit, blue, mark_max)
    sub = subtitle if not unit else f"{subtitle} · unit {unit}"
    return headline, sub, source, body


def build_html(name: str, spec: dict) -> str:
    headline, subtitle, source, body = chart_parts(name)
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
