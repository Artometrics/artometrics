#!/usr/bin/env python3
"""Oct-2026 franchise charts from data/clean (house style: #0047FF accent, DM Sans/DM Mono, no red)."""
import json
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go

A = Path(__file__).resolve().parents[1]; C = A / "data/clean"; OUT = A / "charts"
BLUE, LIGHT, GREY, INK = "#0047FF", "#A9BDFF", "#B8B8B8", "#000000"

def style(fig, title, sub, kicker, source, h=560, l=200):
    title, sub, kicker = (x.replace("$", "&#36;") for x in (title, sub, kicker))
    fig.update_layout(
        title=dict(text=f"<span style='font-size:11px;color:{BLUE};font-family:DM Mono, monospace'>{kicker.upper()}</span><br><b>{title}</b><br><span style='font-size:12px;color:#6B6B6B'>{sub}</span>", x=0.01, xanchor="left", xref="container", y=0.97, yanchor="top"),
        paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF", height=h, width=900,
        font=dict(family="DM Sans, Helvetica, sans-serif", color=INK, size=12),
        margin=dict(l=l, r=50, t=130, b=150), showlegend=fig.layout.showlegend or False, hovermode="closest",
        annotations=list(fig.layout.annotations) + [
            dict(x=0, y=0, xref="paper", yref="paper", yshift=-(h*0.0+125), showarrow=False, xanchor="left", yanchor="top",
                 text=f"<span style='font-family:DM Mono, ui-monospace, monospace'>{source} · Artometrics</span>",
                 font=dict(size=9, color="#6B6B6B"))])
    fig.update_xaxes(gridcolor="#EEEEEE", zeroline=False); fig.update_yaxes(gridcolor="#EEEEEE")
    return fig

def save(fig, name):
    (OUT / f"{name}.plotly.json").write_text(fig.to_json())
    fig.write_image(OUT / f"{name}.png", scale=2)
    fig.write_html(OUT / f"{name}.html", include_plotlyjs="cdn")

SRC = "Source: Wikipedia 'List of highest-grossing media franchises' rev 1379832186 (2026-10-12) · S017"

# 1. Stream shares with bootstrap CI
cs = pd.read_csv(C / "category_shares_bootstrap.csv")
c26 = cs[cs.vintage == 2026].sort_values("share_pct"); c19 = cs[cs.vintage == 2019].set_index("category").share_pct
f = go.Figure()
f.add_bar(y=c26.category, x=c26.share_pct, orientation="h", name="Oct 2026 (140 franchises)",
          marker_color=[BLUE if s == c26.share_pct.max() else LIGHT for s in c26.share_pct],
          error_x=dict(type="data", symmetric=False, array=c26.ci95_hi - c26.share_pct, arrayminus=c26.share_pct - c26.ci95_lo, color="#333333", thickness=1))
f.add_scatter(y=c26.category, x=[c19.get(k) for k in c26.category], mode="markers", name="2019 file (103)", marker=dict(color=INK, symbol="line-ns-open", size=14, line=dict(width=2)))
f.update_layout(showlegend=True, legend=dict(orientation="h", y=1.08, x=1, xanchor="right"))
f.update_xaxes(title="share of lifetime revenue (%) · bars = 95% bootstrap range", ticksuffix="%")
save(style(f, "Merchandise still owns the ledger; box office doubled on paper", "Revenue stream shares, Oct 2026 list vs 2019 file", "Licensing and retail: 55.8%", SRC), "chart6_revenue_streams_2026")

# 2. Top 20 stacked
e = pd.read_csv(C / "franchise_entities_2026-10.csv"); lg = pd.read_csv(C / "franchise_revenue_long_2026-10.csv")
top = e.nlargest(20, "total_usd_b").franchise.tolist()
piv = lg[lg.franchise.isin(top)].pivot_table(index="franchise", columns="category", values="revenue_usd_b", aggfunc="sum").fillna(0).loc[top[::-1]]
pal = {"Merchandise, Licensing & Retail": BLUE, "Box Office": "#001F70", "Video Games/Games": "#5C85FF", "Home Video/Entertainment": "#A9BDFF", "Unallocated": "#DDDDDD"}
f = go.Figure()
for col in piv.columns:
    f.add_bar(y=piv.index, x=piv[col], orientation="h", name=col, marker_color=pal.get(col, GREY))
f.update_layout(barmode="stack", showlegend=True, legend=dict(orientation="h", y=-0.09, font=dict(size=10)))
f.update_xaxes(title="lifetime revenue, USD billions (nominal)", tickprefix="$", ticksuffix="B")
save(style(f, "The top twenty, October 2026", "Lifetime revenue by stream; grey = total not itemised by Wikipedia", "Pokémon $130.7B", SRC, h=720, l=230), "chart1_top20_revenue_2026")

# 3. Region
r = pd.read_csv(C / "region_summary_2026-10.csv").sort_values("total")
f = go.Figure()
f.add_bar(y=r.region_origin, x=r.total, orientation="h", marker_color=[BLUE if x in ("Japan", "US") else LIGHT for x in r.region_origin],
          text=[f"${t:,.0f}B · n={n}" + (f" · {m:.0f}% merch" if pd.notna(m) else "") for t, n, m in zip(r.total, r.n, r.merch_share_pct)], textposition="outside", cliponaxis=False)
f.update_xaxes(title="lifetime revenue, USD billions", tickprefix="$", range=[0, r.total.max() * 1.35])
save(style(f, "The US now out-earns Japan — Japan is the merchandise machine", "Region of origin, Oct 2026 list (140 franchises)", "US $816B vs Japan $394B", SRC + " · region rules in CLEANING_LOG"), "chart15_region_2026")

# 4. Owner concentration (consolidated parents, top 10)
o = e.groupby("owner_parent_2026").total_usd_b.sum().sort_values(ascending=False); sh = (o / o.sum() * 100).head(10)[::-1]
f = go.Figure(go.Bar(y=sh.index, x=sh.values, orientation="h", marker_color=[BLUE if v == sh.max() else LIGHT for v in sh.values],
                     text=[f"{v:.1f}%" for v in sh.values], textposition="outside", cliponaxis=False))
f.update_xaxes(title="share of lifetime revenue (%)", ticksuffix="%")
save(style(f, "Five parents hold 58% of the ledger", "Consolidated parent company as of Oct 2026 (Fox→Disney, Activision→Microsoft, Viacom→Paramount Skydance)", "Disney 29.7% [18.2–43.4]", SRC, l=280), "chart12_owner_concentration_2026")

# 5. Worldwide top 10, 2025 and 2026
bo = pd.read_csv(C / "worldwide_top10_box_office_2025_2026.csv")
f = go.Figure()
for yr, x0 in ((2025, "2025 (final)"), (2026, "2026 (to Oct 12)")):
    b = bo[bo.release_year == yr].iloc[::-1]
    f.add_bar(y=[f"{t.split(' – ')[0]} ({yr})" for t in b.title], x=b.worldwide_gross_usd / 1e9, orientation="h", name=x0,
              marker_color=[BLUE if fl else GREY for fl in b.is_franchise_film])
f.update_xaxes(title="worldwide gross, USD billions (blue = franchise installment, grey = original)", tickprefix="$", ticksuffix="B")
save(style(f, "Nine of 2025's ten biggest films were franchise entries", "Worldwide top 10 by release year; franchise share of top-10 gross: 94.4% (2025), 62.0% (2026 so far)",
           "2025: 94.4% franchise", "Source: Wikipedia '2025 in film' rev 1378645325, '2026 in film' rev 1379926625 (Box Office Mojo / The Numbers) · S091–S092", h=760, l=330), "chart16_worldwide_top10_2025_2026")

# 6. Old vs new key totals (companion)
pairs = [("Pokémon", 90.863, 130.7), ("Hello Kitty", 80.026, 33.5), ("Winnie the Pooh", 74.519, 50.2), ("Star Wars", 63.004, 46.7), ("MCU", 31.0, 37.5), ("Mario", 35.021, 9.74), ("Gundam", 25.525, 5.0), ("Toy Story", 19.54, 16.0), ("Call of Duty", 17.0, 31.0), ("Naruto", 8.854, 22.8)]
f = go.Figure()
for n, a, b in pairs:
    f.add_scatter(x=[a, b], y=[n, n], mode="lines", line=dict(color=GREY, width=3), showlegend=False, hoverinfo="skip")
f.add_scatter(x=[p[1] for p in pairs], y=[p[0] for p in pairs], mode="markers", name="2019 file (published)", marker=dict(color=GREY, size=12))
f.add_scatter(x=[p[2] for p in pairs], y=[p[0] for p in pairs], mode="markers", name="Oct 2026 clean", marker=dict(color=BLUE, size=12))
f.update_layout(showlegend=True, legend=dict(orientation="h", y=1.08, x=1, xanchor="right"))
f.update_xaxes(title="lifetime revenue, USD billions", tickprefix="$", ticksuffix="B")
save(style(f, "What moved when we fixed the data", "Published 2019 figure vs Oct 2026 clean figure", "Hello Kitty −$46.5B is a source revision", "Source: S001 (TidyTuesday 2019) vs S017 (Wikipedia 2026-10-12)"), "chart17_old_vs_new_2026")

# 7. Verification scatter (companion)
v = pd.read_csv(C / "verification_sample_2019.csv").dropna(subset=["wiki_rev904026364_total_b"])
mx = v.wiki_rev904026364_total_b.max() * 1.05
f = go.Figure([go.Scatter(x=[0, mx], y=[0, mx], mode="lines", line=dict(color=GREY, dash="dot"), name="perfect agreement"),
               go.Scatter(x=v.wiki_rev904026364_total_b, y=v.tidytuesday_sum_b, mode="markers", text=v.franchise, name="sampled franchise", marker=dict(color=BLUE, size=9))])
f.update_layout(showlegend=True, legend=dict(orientation="h", y=1.08, x=1, xanchor="right"))
f.update_xaxes(title="Wikipedia headline total, rev 904026364 (2019-06-29), $B"); f.update_yaxes(title="TidyTuesday row sum, $B")
save(style(f, "The 2019 file sits below its own source", "Random sample of 40 franchises (seed 20261012); 39 matched", "28 of 39 within 10%", "Source: S001 vs Wikipedia rev 904026364", l=90), "chart18_verification_2019")
print("ok")
