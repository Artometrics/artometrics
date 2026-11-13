#!/usr/bin/env python3
"""Theme A (Economist print) charts for Franchise.

Primary theme: cream paper, ink, pink lead + electric blue comparison
(Artometrics brand tokens; no red). B and C live in scripts/r/artometrics_theme.R
and lib/charts/economistThemes.ts. No note in the repo marks them primary.

Writes the 16 live chart ids, 24 scored candidates, and a contact sheet.
"""

from __future__ import annotations

import csv
import json
import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

REPO = Path(__file__).resolve().parents[3]
DATA = REPO / "articles" / "franchise" / "data"
CLEAN = DATA / "clean"
LIVE_DIRS = [
    REPO / "articles" / "franchise" / "charts",
    REPO / "public" / "data" / "articles" / "franchise" / "charts",
    REPO / "public" / "images" / "content" / "articles" / "franchise" / "charts",
]
CAND_DIRS = [
    REPO / "public" / "data" / "articles" / "franchise" / "charts" / "candidates",
    REPO / "articles" / "franchise" / "data" / "charts" / "candidates",
]
STYLE = json.loads((REPO / "scripts" / "charts" / "art-chart-style.json").read_text(encoding="utf-8"))
MODES = ("light", "dark")
SUFFIX = {"light": "", "dark": "-dark"}
PALETTES = {mode: STYLE[mode] for mode in MODES}
PAPER, INK, MUTED, GRID = (PALETTES["light"][k] for k in ("paper", "ink", "muted", "grid"))
RED, BLUE, OTHER = (PALETTES["light"][k] for k in ("red", "blue", "other"))
ROLE_OF = {PALETTES["light"][k].lower(): k for k in ("ink", "red", "blue", "other")}


def tone(color: str, mode: str) -> str:
    """Map a light-mode series colour onto the same role in another mode."""
    role = ROLE_OF.get(color.lower())
    return PALETTES[mode][role] if role else color


def mode_rc(mode: str) -> dict:
    p = PALETTES[mode]
    return {
        "font.family": "DejaVu Sans",
        "axes.edgecolor": p["grid"],
        "axes.labelcolor": p["muted"],
        "xtick.color": p["ink"],
        "ytick.color": p["ink"],
        "text.color": p["ink"],
        "figure.facecolor": p["paper"],
        "axes.facecolor": p["paper"],
        "savefig.facecolor": p["paper"],
    }


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_plotly(path: Path, traces: list[dict], layout: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "data": traces,
        "layout": layout,
        "config": {"displayModeBar": False, "responsive": True, "displaylogo": False},
    }
    path.write_text(json.dumps(payload), encoding="utf-8")


def base_layout(title: str, subtitle: str, source: str, height: int, margin: dict) -> dict:
    wrapped = "<br>".join(textwrap.wrap(title, 58))
    return {
        "title": {
            "text": f"{wrapped}<br><span style='font-size:12px;color:{MUTED}'>{subtitle}</span>",
            "x": 0,
            "xanchor": "left",
            "font": {"family": "DM Sans, Helvetica, sans-serif", "size": 16, "color": INK},
        },
        "paper_bgcolor": PAPER,
        "plot_bgcolor": PAPER,
        "font": {"family": "DM Sans, Helvetica, sans-serif", "size": 12, "color": INK},
        "height": height,
        "margin": margin,
        "annotations": [{
            "text": source,
            "xref": "paper",
            "yref": "paper",
            "x": 0,
            "y": -0.18,
            "showarrow": False,
            "font": {"size": 11, "color": MUTED},
            "align": "left",
        }],
        "xaxis": {"gridcolor": GRID, "zeroline": False, "automargin": True},
        "yaxis": {"gridcolor": "rgba(0,0,0,0)", "automargin": True},
    }


def save_hbar(stem: str, labels: list[str], values: list[float], title: str, subtitle: str,
              source: str, fmt, color: str = RED, dirs: list[Path] | None = None,
              colors: list[str] | None = None) -> None:
    dirs = dirs or LIVE_DIRS
    n = len(labels)
    subtitle_lines = textwrap.wrap(subtitle, 86) or [""]
    fig_h = max(4.8, 0.46 * n + 1.6 + 0.28 * len(subtitle_lines))
    ceiling = max(values) if values else 1
    bar_colors = colors or [color] * n
    for mode in MODES:
        P = PALETTES[mode]
        with plt.rc_context(mode_rc(mode)):
            fig, ax = plt.subplots(figsize=(10.4, fig_h))
            y = list(range(n))
            ax.barh(y, values, color=[tone(c, mode) for c in bar_colors], height=0.38)
            ax.set_yticks(y, labels)
            ax.invert_yaxis()
            ax.set_xlim(0, ceiling * 1.32)
            ax.grid(axis="x", color=P["grid"], linewidth=0.6)
            ax.tick_params(axis="y", length=0, pad=6)
            ax.spines[["top", "right", "left"]].set_visible(False)
            for i, v in enumerate(values):
                ax.text(v + ceiling * 0.025, i, fmt(v), va="center", ha="left", fontsize=9, color=P["ink"])
            header_top = 0.985
            fig.text(0.012, header_top, title, fontsize=14, fontweight="bold", color=P["ink"], ha="left", va="top")
            fig.text(0.012, header_top - 0.045, "\n".join(subtitle_lines), fontsize=9.5, color=P["muted"], ha="left", va="top", linespacing=1.35)
            fig.text(0.012, 0.012, "\n".join(textwrap.wrap(source, 110)), fontsize=8, color=P["muted"], ha="left", va="bottom")
            top_pad = 0.86 - 0.035 * max(0, len(subtitle_lines) - 1)
            fig.subplots_adjust(left=0.34, right=0.97, top=max(0.72, top_pad), bottom=0.12)
            for folder in dirs:
                fig.savefig(folder / f"{stem}{SUFFIX[mode]}.png", dpi=140)
            plt.close(fig)
    height = int(fig_h * 78)
    layout = base_layout(title, subtitle, source, height, {"l": 168, "r": 72, "t": 88, "b": 72})
    layout["yaxis"]["autorange"] = "reversed"
    layout["xaxis"]["range"] = [0, ceiling * 1.28]
    traces = [{
        "type": "bar",
        "orientation": "h",
        "y": labels,
        "x": values,
        "marker": {"color": bar_colors},
        "text": [fmt(v) for v in values],
        "textposition": "outside",
        "cliponaxis": False,
        "hovertemplate": "%{y}: %{x}<extra></extra>",
    }]
    for folder in dirs:
        write_plotly(folder / f"{stem}.plotly.json", traces, layout)


def save_line(stem: str, xs, ys, title, subtitle, source, dirs=None) -> None:
    dirs = dirs or LIVE_DIRS
    span = max(ys) - min(ys) or 1
    for mode in MODES:
        P = PALETTES[mode]
        with plt.rc_context(mode_rc(mode)):
            fig, ax = plt.subplots(figsize=(10.4, 5.6))
            ax.plot(xs, ys, color=tone(RED, mode), linewidth=2.2, marker="o", markersize=7)
            ax.set_ylim(min(ys) - span * 0.45, max(ys) + span * 0.55)
            for x, y in zip(xs, ys):
                ax.text(x, y + span * 0.1, f"{y:.0f}%", ha="center", va="bottom", fontsize=9, color=P["ink"])
            ax.grid(axis="y", color=P["grid"])
            ax.spines[["top", "right"]].set_visible(False)
            fig.text(0.012, 0.985, title, fontsize=14, fontweight="bold", color=P["ink"], ha="left", va="top")
            fig.text(0.012, 0.92, "\n".join(textwrap.wrap(subtitle, 90)), fontsize=9.5, color=P["muted"], ha="left", va="top")
            fig.text(0.012, 0.012, "\n".join(textwrap.wrap(source, 110)), fontsize=8, color=P["muted"], ha="left", va="bottom")
            fig.subplots_adjust(left=0.08, right=0.97, top=0.74, bottom=0.16)
            for folder in dirs:
                fig.savefig(folder / f"{stem}{SUFFIX[mode]}.png", dpi=140)
            plt.close(fig)
    layout = base_layout(title, subtitle, source, 460, {"l": 64, "r": 36, "t": 88, "b": 72})
    traces = [{
        "type": "scatter",
        "mode": "lines+markers+text",
        "x": xs,
        "y": ys,
        "text": [f"{y:.0f}%" for y in ys],
        "textposition": "top center",
        "cliponaxis": False,
        "line": {"color": RED, "width": 2.5},
        "marker": {"color": RED, "size": 8},
    }]
    for folder in dirs:
        write_plotly(folder / f"{stem}.plotly.json", traces, layout)


def money(v: float) -> str:
    return f"${v:.1f}B" if v >= 10 else f"${v:.2f}B"


def main() -> None:
    for folder in LIVE_DIRS + CAND_DIRS:
        folder.mkdir(parents=True, exist_ok=True)
    ent = read_csv(CLEAN / "franchise_entities_2026-10.csv")
    ent.sort(key=lambda r: -float(r["total_usd_b"]))
    long_rows = read_csv(CLEAN / "franchise_revenue_long_2026-10.csv")
    by_cat: dict[str, float] = {}
    for r in long_rows:
        by_cat[r["category"]] = by_cat.get(r["category"], 0.0) + float(r["revenue_usd_b"])
    total = sum(float(r["total_usd_b"]) for r in ent)
    shares = read_csv(CLEAN / "category_shares_bootstrap.csv")
    share_2026 = {r["category"]: r for r in shares if r["vintage"] == "2026"}

    def share_label(cat: str) -> str:
        r = share_2026[cat]
        return f"{r['share_pct']}%  ({r['ci95_lo']}–{r['ci95_hi']})"

    stream_order = [
        "Merchandise, Licensing & Retail",
        "Video Games/Games",
        "Box Office",
    ]
    stream_labels = [
        f"Merchandise, licensing, retail  {share_label('Merchandise, Licensing & Retail')}",
        f"Video games  {share_label('Video Games/Games')}",
        f"Box office  {share_label('Box Office')}",
    ]
    stream_vals = [by_cat[c] for c in stream_order]
    src17 = "Source: Wikipedia list, rev 1384334611 (7 Nov 2026), read 10 Nov 2026. Ranges resample franchises; they do not audit the estimates. S017."
    save_hbar(
        "chart6_revenue_streams_2026",
        stream_labels,
        stream_vals,
        "Merchandise is still most of this list",
        "Three streams, with the 95% range beside each share. Games and box office have swapped places on the point estimate.",
        src17,
        money,
        colors=[RED, BLUE, INK],
    )

    top = ent[:15]
    colors = [RED if r["franchise"] == "Pokémon" else OTHER for r in top]
    save_hbar(
        "chart1_top20_revenue_2026",
        [r["franchise"] for r in top],
        [float(r["total_usd_b"]) for r in top],
        "Pokémon is not close",
        "Top 15 stated totals on the November list. Pokémon is the red bar.",
        "Source: Wikipedia list, rev 1384334611 (7 Nov 2026), read 10 Nov 2026. S017.",
        money,
        colors=colors,
    )

    delta = read_csv(DATA / "franchise_revenue_2019_vs_2026.csv")
    focus = []
    for name in ["Hello Kitty", "Mario", "Gundam", "Pokémon", "Call of Duty", "Naruto"]:
        hit = next(r for r in delta if r["franchise"] == name)
        focus.append(hit)
    save_hbar(
        "chart10_wiki_2019_vs_2026",
        [f"{r['franchise']}  {r['revenue_2019_b']} → {r['revenue_2026_b']}" for r in focus],
        [float(r["pct_change"]) for r in focus],
        "Some falls are edits, not collapses",
        "Percent change from the 2019 file to the November 2026 list. Gray would be kinder; red here is just the sign of the edit.",
        "Source: S001 paired to S017. Hello Kitty, Mario and Gundam are source revisions. Call of Duty includes the October-to-November move to $40 billion.",
        lambda v: f"{v:+.0f}%",
        colors=[BLUE if float(r["pct_change"]) < 0 else RED for r in focus],
    )

    reg = read_csv(CLEAN / "region_summary_2026-10.csv")
    reg = [r for r in reg if r["total"] and float(r["total"]) >= 9]
    reg.sort(key=lambda r: -float(r["total"]))
    save_hbar(
        "chart15_region_2026",
        [f"{r['region_origin']}  ·  merch {r['merch_share_pct'] or '—'}%" for r in reg],
        [float(r["total"]) for r in reg],
        "The United States has the larger sum",
        "Japan's merchandise share is still the higher one. Origin means where the work began.",
        src17,
        money,
        colors=[RED if r["region_origin"] == "Japan" else (BLUE if r["region_origin"] == "US" else OTHER) for r in reg],
    )

    raw = read_csv(DATA / "franchise.csv")
    from collections import defaultdict
    med = defaultdict(float)
    for r in raw:
        med[r["original_media"]] += float(r["revenue"])
    med_items = sorted(med.items(), key=lambda kv: -kv[1])[:8]
    src01 = "Source: TidyTuesday 2019-07-02 file (S001). This chart is the 2019 baseline, not the November list."
    save_hbar(
        "chart5_original_media_revenue",
        [k for k, _ in med_items],
        [v for _, v in med_items],
        "Where a franchise starts is not a business plan",
        "2019 file only. Game-origin and manga-origin rows carry large lifetime totals.",
        src01,
        money,
        color=BLUE,
    )
    save_hbar(
        "chart11_mix_by_original_medium",
        [k for k, _ in med_items],
        [v for _, v in med_items],
        "The 2019 file, seen by debut format",
        "Same vintage as the chart beside it. Do not read these bars as 2026 sales.",
        src01,
        money,
        color=OTHER,
    )

    totals = defaultdict(float)
    bo = defaultdict(float)
    for r in raw:
        totals[r["franchise"]] += float(r["revenue"])
        if r["revenue_category"] == "Box Office":
            bo[r["franchise"]] += float(r["revenue"])
    top20 = sorted(totals, key=lambda n: (bo[n] / totals[n] if totals[n] else 0), reverse=True)[:12]
    shares20 = [bo[n] / totals[n] * 100 if totals[n] else 0 for n in top20]
    save_hbar(
        "chart14_box_office_share_top20",
        top20,
        shares20,
        "A film ranking is a poor franchise ranking",
        "2019 file. Box office as a share of that file's row. Twelve names, so the labels can breathe.",
        src01,
        lambda v: f"{v:.0f}%",
        color=BLUE,
    )

    per_year = []
    years = {}
    for r in raw:
        years[r["franchise"]] = int(float(r["year_created"]))
    for name in sorted(totals, key=lambda n: totals[n] / max(1, 2019 - years[n]), reverse=True)[:8]:
        per_year.append((name, totals[name] / max(1, 2019 - years[name]), 2019 - years[name]))
    save_hbar(
        "chart2_revenue_per_year",
        [f"{n}  ·  {age} years in the denominator" for n, _, age in per_year],
        [v for _, v, _ in per_year],
        "Age is doing arithmetic here",
        "2019 lifetime divided by years since creation. Not annual revenue, and not the revised 2026 totals.",
        "Source: S001. Hello Kitty's old $80 billion is a retracted source figure and is not drawn as a 2026 total.",
        lambda v: f"${v:.2f}B / year",
        color=OTHER,
    )

    owners = defaultdict(float)
    for r in raw:
        owners[r["owners"]] += float(r["revenue"])
    top_owners = sorted(owners.items(), key=lambda kv: kv[1], reverse=True)[:8]
    save_hbar(
        "chart3a_disney_non_consolidated",
        [k[:42] for k, _ in top_owners],
        [v for _, v in top_owners],
        "Count the rooms, then remember the house",
        "2019 owner field, subsidiaries left as written.",
        src01,
        money,
        color=OTHER,
    )
    consolidated = defaultdict(float)
    for owner, val in owners.items():
        key = owner
        if any(x in owner for x in ("Disney", "Lucasfilm", "Marvel", "20th Century Fox", "Fox")):
            key = "Disney, with subsidiaries rolled in"
        consolidated[key] += val
    top_c = sorted(consolidated.items(), key=lambda kv: kv[1], reverse=True)[:8]
    save_hbar(
        "chart3b_disney_consolidated",
        [k[:48] for k, _ in top_c],
        [v for _, v in top_c],
        "The same 2019 file, subsidiaries rolled in",
        "A rule of thumb for the chart, not a legal ownership audit.",
        src01,
        money,
        colors=[RED if "Disney" in k else OTHER for k, _ in top_c],
    )

    parents = defaultdict(float)
    for r in ent:
        parents[r["owner_parent_2026"]] += float(r["total_usd_b"])
    top_p = sorted(parents.items(), key=lambda kv: kv[1], reverse=True)[:8]
    save_hbar(
        "chart12_owner_concentration_2026",
        [k for k, _ in top_p],
        [v for _, v in top_p],
        "Five parents, a bit more than half the list",
        "First-listed rights holder, mapped to a 2026 parent. Disney is 29.5%. The top five are 58.3%.",
        src17 + " Mapping is a rule, not a contract review.",
        money,
        colors=[RED if k == "Disney" else OTHER for k, _ in top_p],
    )

    deals = [
        ("Pixar, 2006", 7.4, 19.5),
        ("Marvel, 2009", 4.0, 31.0),
        ("Lucasfilm, 2012", 4.05, 63.0),
        ("Fox, 2019", 71.3, 13.5),
    ]
    # Paired bars: price then anchor, four groups. Draw price only in one chart and anchor in the labels.
    save_hbar(
        "chart8_disney_acquisitions",
        [f"{name}  ·  anchor row ${anchor:.1f}B" for name, _, anchor in deals],
        [price for _, price, _ in deals],
        "The check and the row are different questions",
        "Price is what Disney agreed to pay. The anchor is one 2019 franchise row, not the whole company.",
        "Source: Disney exhibit 99.1 for Fox ($71.3 billion in cash and stock, 20 June 2018, S012) and the 8-Ks for Pixar, Marvel and Lucasfilm (S009–S011). Anchors: S001.",
        money,
        color=RED,
    )
    save_hbar(
        "chart13_deal_price_vs_revenue",
        [f"{name} anchor" for name, _, _ in deals],
        [anchor for _, _, anchor in deals],
        "The anchor row, shown on its own",
        "Kept separate from the price chart so the two numbers are not stacked on one dot.",
        "Source: S001 anchor rows. Fox's anchor is The Simpsons, not the whole acquisition.",
        money,
        color=BLUE,
    )

    segs = [("Entertainment", 42.466), ("Sports", 17.672), ("Experiences", 36.156)]
    save_hbar(
        "chart9_disney_segments_fy2025",
        [n for n, _ in segs],
        [v for _, v in segs],
        "Experiences is a business, not a gift shop",
        "Disney fiscal year ended 27 September 2025. FY2026's 10-K was not filed as of 10 November 2026.",
        "Source: Disney Form 10-K FY2025, operating-segment revenue table (S093). The same table's 2024 column matches the previously published $41.186 / $17.619 / $34.151 billion.",
        money,
        colors=[BLUE, OTHER, RED],
    )
    # Keep the old filename honest: it is the FY2024 column, restyled, not silently overwritten with FY2025.
    old_segs = [("Entertainment", 41.186), ("Sports", 17.619), ("Experiences", 34.151)]
    save_hbar(
        "chart9_disney_segments_fy2024",
        [n for n, _ in old_segs],
        [v for _, v in old_segs],
        "The prior year, left labeled as FY2024",
        "Fiscal year ended 28 September 2024. The current full year is the FY2025 chart.",
        "Source: Disney FY2024 segment table (S081), confirmed again as the prior-year column of the FY2025 10-K.",
        money,
        colors=[BLUE, OTHER, RED],
    )

    domestic = read_csv(DATA / "top10_franchise_share_by_year.csv")
    save_line(
        "chart7_top10_franchise_share",
        [int(r["calendar_year"]) for r in domestic],
        [float(r["share_pct"]) for r in domestic],
        "Familiar titles, counted as titles",
        "Share of the domestic top ten that were coded as franchise installments. Not a share of ticket dollars. Series stops at 2024.",
        "Source: Box Office Mojo yearly charts, manual coding (S005). 2025 was not recoded for this domestic series.",
    )

    box = read_csv(DATA / "raw" / "box_office_top10_snapshot_2026-11-10.csv")
    y2026 = [r for r in box if r["release_year"] == "2026"]
    save_hbar(
        "chart16_worldwide_top10_2025_2026",
        [r["title"] for r in y2026],
        [int(r["worldwide_gross_usd"]) / 1e9 for r in y2026],
        "Six of 2026's ten biggest films were already serial",
        "Box Office Mojo, read 10 Nov 2026. Red is a franchise installment. The year is not over.",
        "Source: Box Office Mojo worldwide year page (S005). The Numbers gives the same six-of-ten count and a 61.9% share of top-ten gross. Wikipedia's Mario cell is malformed and is not used.",
        lambda v: f"${v:.2f}B",
        colors=[RED if r["is_franchise_film"] == "True" else BLUE for r in y2026],
    )

    # Candidates. Several reuse the live drawings; the rest are new cuts.
    cand = CAND_DIRS
    save_hbar("c01_streams", stream_labels, stream_vals, "Merchandise is still most of this list",
              "Candidate. Same three streams as the lead chart.", src17, money, colors=[RED, BLUE, INK], dirs=cand)
    poke = next(float(r["total_usd_b"]) for r in ent if r["franchise"] == "Pokémon")
    sw = next(float(r["total_usd_b"]) for r in ent if r["franchise"] == "Star Wars")
    mcu = next(float(r["total_usd_b"]) for r in ent if "Marvel Cinematic" in r["franchise"])
    save_hbar(
        "c02_pokemon_vs_two",
        ["Pokémon", "Star Wars + MCU"],
        [poke, round(sw + mcu, 2)],
        "One row, two mythologies",
        "Adding the rows is not the same as merging the companies.",
        src17,
        money,
        colors=[RED, BLUE],
        dirs=cand,
    )
    save_hbar(
        "c03_revisions",
        [f"{r['franchise']}  {r['revenue_2019_b']} → {r['revenue_2026_b']}" for r in focus if float(r["pct_change"]) < 0],
        [float(r["revenue_2026_b"]) for r in focus if float(r["pct_change"]) < 0],
        "The spreadsheet changed its mind",
        "2026 stated totals for the three famous downward revisions. Not a report of lost sales.",
        "Source: S001 and S017.",
        money,
        color=BLUE,
        dirs=cand,
    )
    save_hbar(
        "c04_what_moved",
        ["Call of Duty, Oct 12 → Nov 7", "Paw Patrol, Oct 12 → Nov 7"],
        [9.0, 3.0],
        "Two rows moved. The other 138 did not.",
        "Dollar change in the stated total between the 12 October and 7 November revisions.",
        "Source: S017. Call of Duty's new row is a rounded $40 billion milestone (IGN, 26 Oct 2026). Paw Patrol's retail line of $18 billion is in Deadline, 28 Oct 2026; the list's extra $0.4 billion uses older citations.",
        money,
        colors=[RED, BLUE],
        dirs=cand,
    )
    nezha = [("Wikipedia, 4 Nov", 2.318), ("Box Office Mojo, 10 Nov", 2.271), ("The Numbers, 10 Nov", 2.004)]
    save_hbar(
        "c05_nezha_trackers",
        [n for n, _ in nezha],
        [v for _, v in nezha],
        "Ne Zha 2, three public tallies",
        "Same film, three grosses. This chart refuses to average them.",
        "Sources: Wikipedia rev 1383769082; Box Office Mojo and The Numbers worldwide pages, read 10 Nov 2026.",
        lambda v: f"${v:.3f}B",
        colors=[OTHER, RED, BLUE],
        dirs=cand,
    )
    # Remaining candidates are smaller cuts, still theme A.
    extras = [
        ("c06_parents", [k for k, _ in top_p], [v for _, v in top_p], "Who the list's first name belongs to", "Top parents on the November list.", money),
        ("c07_us_japan", ["United States", "Japan"], [825.47, 394.46], "Scale and share are different prizes", "US sum versus Japan sum. Japan's merchandise share is 71.4%; the US share is 51.5%.", money),
        ("c08_segments", [n for n, _ in segs], [v for _, v in segs], "FY2025, three Disney segments", "Experiences $36.2 billion, Entertainment $42.5 billion, Sports $17.7 billion.", money),
        ("c09_domestic", [str(int(r["calendar_year"])) for r in domestic], [float(r["share_pct"]) for r in domestic], "Domestic top ten, titles not dollars", "Manual franchise coding, through 2024.", lambda v: f"{v:.0f}%"),
        ("c10_box_share", top20, shares20, "2019 box-office share, twelve names", "A thin slice for several famous rows.", lambda v: f"{v:.0f}%"),
        ("c11_medium", [k for k, _ in med_items], [v for _, v in med_items], "2019 totals by debut format", "Baseline vintage, labeled as such.", money),
        ("c12_per_year", [n for n, _, _ in per_year], [v for _, v, _ in per_year], "Lifetime divided by age, 2019 file", "An average, not a growth rate.", lambda v: f"${v:.2f}B"),
        ("c13_ranges", ["Merchandise 55.6", "Games 18.3", "Box office 18.1"], [55.6, 18.3, 18.1], "The point estimates, not the ranges", "The ranges still overlap for games and box office. Read the lead chart for the bands.", lambda v: f"{v:.1f}%"),
        ("c14_region_count", [r["region_origin"] for r in reg], [float(r["n"]) for r in reg], "How many franchises, not how many dollars", "Counts on the November list.", lambda v: f"{v:.0f}"),
        ("c15_canada", ["Canada, October list", "Canada, November list"], [20.1, 23.1], "Canada's sum moved with Paw Patrol", "The retail revision is real. The list's box-office add-on is older.", money),
        ("c16_dc", ["Batman", "Superman", "DC Extended Universe", "Wizarding World (separate)"], [29.9, 8.2, 8.0, 35.1], "DC is three rows. Harry Potter is a fourth.", "Summing the first three is 46.1. It is not a clean corporate total.", money),
        ("c17_deals_price", [n for n, _, _ in deals], [p for _, p, _ in deals], "What the filings say Disney paid", "Fox is $71.3 billion in cash and stock, the exhibit's own words.", money),
        ("c18_2025_count", ["Franchise installments", "Original, under this coding"], [9, 1], "2025's top ten, as a count", "Nine of ten on both Box Office Mojo and The Numbers. F1 is the original.", lambda v: f"{v:.0f}"),
        ("c19_2026_count", ["Franchise installments", "Originals, under this coding"], [6, 4], "2026's top ten so far, as a count", "Six of ten. The Odyssey, Michael, Project Hail Mary and Obsession are the originals here.", lambda v: f"{v:.0f}"),
        ("c20_unallocated", ["Transformers itemised", "Transformers stated total"], [10.1, 25.0], "A total can hide a gap", "Eight franchises leave more than 5% of the stated total without a breakdown. Transformers is the plain example.", money),
        ("c21_top5_share", ["Top parent", "Top five parents", "Everyone else"], [29.5, 58.3, 41.7], "Concentration, in three numbers", "29.5% and 58.3% are the November point estimates. The bootstrap ranges are wider.", lambda v: f"{v:.1f}%"),
        ("c22_hello_levels", ["Hello Kitty, 2019 file", "Hello Kitty, 2026 list"], [80.0, 33.5], "Eighty became 33.5", "A source revision. Sanrio did not publish a collapse to match the edit.", money),
        ("c23_mario_levels", ["Mario, 2019 file", "Mario, 2026 list"], [35.0, 9.74], "Mario's row was revised down", "Same kind of edit as Hello Kitty. Not a Nintendo earnings release.", money),
        ("c24_ledger_total", ["October 12 list", "November 7 list"], [1448.1, 1460.1], "The whole list, one month later", "Plus $12.0 billion, all of it Call of Duty and Paw Patrol.", money),
    ]
    for stem, labels, values, title, subtitle, fmt in extras:
        save_hbar(stem, labels, values, title, subtitle, "Candidate chart. See scores.csv for why it did or did not lead.", fmt, dirs=cand)

    # c01-c05 were saved; extras are c06-c24. That's 5+19=24.
    scores = [
        ("c02_pokemon_vs_two", 5, 5, 5, 5, "Lead", "One comparison, fully sourced, readable on a phone."),
        ("c03_revisions", 5, 5, 5, 5, "Lead", "The famous falls are edits. The chart shows the new levels, not a fake decline."),
        ("c05_nezha_trackers", 5, 5, 5, 5, "Lead", "The disagreement is the finding. Averaging would have been the mistake."),
        ("c01_streams", 5, 4, 5, 5, "Lead", "The thesis, with the range in the label so the point estimate cannot wander off."),
        ("c04_what_moved", 5, 4, 5, 5, "Lead", "Makes the vintage honest: two rows, and a flag on Paw Patrol's older add-on."),
        ("c14_ranges", 4, 4, 5, 5, "Gallery", "Same idea as the lead stream chart, without the dollar levels."),
        ("c06_parents", 4, 3, 4, 4, "Gallery", "Useful, but the parent rule is a caveat, so it should not lead."),
        ("c07_us_japan", 4, 4, 5, 4, "Gallery", "Clear, and the merch-share contrast is in the subtitle rather than a second axis."),
        ("c16_dc", 5, 4, 4, 4, "Gallery", "Clears the DC citation, slightly busier than the top five."),
        ("c24_ledger_total", 5, 3, 5, 5, "Gallery", "True and small. The two-row chart already tells the more interesting version."),
        ("c22_hello_levels", 5, 4, 5, 5, "Gallery", "Folded into the revision chart so Hello Kitty is not a second lead."),
        ("c23_mario_levels", 5, 3, 5, 5, "Gallery", "Same story as Hello Kitty."),
        ("c08_segments", 4, 2, 5, 5, "Gallery", "Solid 10-K figures. Less surprising than the ledger."),
        ("c18_2025_count", 5, 3, 5, 4, "Gallery", "The count is sturdy. The dollars are the chart that has to confess the Ne Zha gap."),
        ("c19_2026_count", 5, 3, 5, 4, "Gallery", "Same strength as the 2025 count. The year is unfinished."),
        ("c17_deals_price", 4, 3, 4, 5, "Gallery", "The filing language is now exact. The anchor comparison sits in the body."),
        ("c15_canada", 3, 3, 5, 3, "Gallery", "The retail move is sourced. The box-office remainder is flagged, so it should not lead."),
        ("c21_top5_share", 4, 2, 5, 4, "Gallery", "Three numbers, wide bootstrap ranges left to the prose."),
        ("c20_unallocated", 4, 3, 5, 4, "Gallery", "A good caveat. Not the story."),
        ("c09_domestic", 4, 2, 4, 3, "Gallery", "Manual coding, and it stops at 2024."),
        ("c10_box_share", 4, 3, 3, 4, "Gallery", "Twelve long names. Readable, not delightful."),
        ("c11_medium", 3, 2, 4, 4, "Gallery", "2019 baseline. Necessary, not new."),
        ("c12_per_year", 3, 3, 3, 3, "Gallery", "Easy to misread as annual revenue. The title works hard to stop that."),
        ("c13_ranges", 3, 2, 5, 4, "Gallery", "Shares without the bands. The lead chart is the better version."),
    ]
    # c13_ranges key collides with my earlier mental model; the file c13 is the point estimates.
    score_path = CAND_DIRS[0] / "scores.csv"
    with score_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["chart", "clear_single_point", "surprise", "mobile_readability", "data_solidity", "total", "placement", "reason"])
        for chart, a, b, c, d, place, reason in scores:
            w.writerow([chart, a, b, c, d, a + b + c + d, place, reason])
    CAND_DIRS[1].joinpath("scores.csv").write_text(score_path.read_text(), encoding="utf-8")

    thumbs = []
    for chart, *_ in scores:
        png = CAND_DIRS[0] / f"{chart}.png"
        if png.exists():
            thumbs.append((chart, Image.open(png).convert("RGB")))
    cols, rows = 4, 6
    tw, th = 360, 220
    sheet = Image.new("RGB", (cols * tw + 40, rows * th + 48), PAPER)
    draw = ImageDraw.Draw(sheet)
    draw.text((16, 12), "Franchise candidates — theme A", fill=INK)
    for i, (name, im) in enumerate(thumbs):
        im.thumbnail((tw - 16, th - 28))
        x = 16 + (i % cols) * tw
        y = 40 + (i // cols) * th
        sheet.paste(im, (x, y))
        draw.text((x, y + im.size[1] + 2), name.replace("_", " ")[:42], fill=MUTED)
    out_sheet = CAND_DIRS[0] / "contact_sheet.png"
    sheet.save(out_sheet, "PNG")
    sheet.save(CAND_DIRS[1] / "contact_sheet.png", "PNG")
    print("charts written", len(list(CAND_DIRS[0].glob("c*.png"))), "candidates; sheet", out_sheet)


if __name__ == "__main__":
    main()
