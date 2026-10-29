#!/usr/bin/env python3
"""Franchise dataset audit, clean and Oct-2026 update (reproducible; stdlib + pandas/numpy).

Inputs (all committed under articles/franchise/data/):
  franchise.csv                       TidyTuesday 2019-07-02 ledger (S001), unchanged raw
  raw/wiki_franchises_rev904026364_2019-06-29.wikitext   Wikipedia revision underlying S001
  raw/wiki_franchises_rev1379832186_2026-10-12.wikitext  current Wikipedia list (S017)
  raw/wiki_2025_in_film_rev1378645325.wikitext, raw/wiki_2026_in_film_rev1379926625.wikitext
  raw/fred_CPIAUCSL_2026-10-12.csv    FRED CPI-U (S090)
Outputs: data/clean/*.csv and data/clean/old_vs_new.csv
Run: python3 scripts/franchise-data/clean_audit.py
"""
from __future__ import annotations
import re, sys, json, random
from pathlib import Path
import numpy as np, pandas as pd

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(REPO / "scripts"))
import wikiparse as wp  # noqa
from franchise_verify_numbers import infer_region_fields  # noqa
from franchise_crosswalk_data import CROSSWALK  # noqa

D = REPO / "articles/franchise/data"; RAW = D / "raw"; OUT = D / "clean"; OUT.mkdir(exist_ok=True)
SEED = 20261012; B = 5000
rng = np.random.default_rng(SEED)
log: list[str] = []

STD = [  # (regex on raw breakdown label, standard category)
    (r"box office & home video|home video & merch", "Mixed (unsplit)"),
    (r"box office", "Box Office"),
    (r"retail|merchandis|licens|livery", "Merchandise, Licensing & Retail"),
    (r"video ?game|mobile game|computer game|games & consoles|card game|pachinko|pachislot", "Video Games/Games"),
    (r"dvd|blu-ray|home (video|media|entertainment)|vhs|video rental", "Home Video/Entertainment"),
    (r"\btv\b|television|streaming", "TV"),
    (r"book", "Book sales"),
    (r"manga|comic", "Comic or Manga"),
    (r"music|soundtrack|album", "Music"),
    (r"musical|theat|stage|broadway|museum|tour|park|attraction", "Live & Other"),
]
def std_cat(label: str) -> str:
    l = label.lower()
    for rx, c in STD:
        if re.search(rx, l): return c
    return "Other"

MEDIA_STD = {"Cartoon": "Animated cartoon", "Cartoon character": "Animated cartoon", "Anime": "Animated series",
             "Book": "Novel/Book", "Novel": "Novel/Book"}
PARENTS = [  # consolidated parent as of 2026-10 (rule: earliest-matching token in owner string)
    ("Disney", r"disney|marvel|lucasfilm|pixar|20th century|fox"),
    ("Warner Bros. Discovery", r"warner|dc entertainment|dc comics|cartoon network|hbo"),
    ("Comcast (Universal)", r"universal|illumination|dreamworks|comcast"),
    ("Microsoft", r"microsoft|activision|blizzard|\bking\b|bethesda|mojang"),
    ("The Pokémon Company", r"pok[eé]mon company"),
    ("Nintendo", r"nintendo"), ("Sony", r"\bsony|aniplex|columbia"),
    ("Paramount Skydance", r"paramount|viacom|nickelodeon|cbs"),
    ("Hasbro", r"hasbro"), ("Mattel", r"mattel"), ("Sanrio", r"sanrio"),
    ("Hitotsubashi Group (Shueisha/Shogakukan)", r"shueisha|shogakukan"),
    ("Bandai Namco", r"bandai|sunrise|tsuburaya"), ("Sega Sammy", r"\bsega\b|tms entertainment"),
    ("Square Enix", r"square enix|taito"), ("Tencent", r"tencent|riot"),
]
REGION26 = {  # rule R9: hand-coded origin for 2026-only rows the 2019 inference cannot resolve (rights-holder HQ at creation)
    "Rilakkuma": "Japan", "Fortnite": "US", "Avatar": "US", "Genshin Impact": "China", "Seinfeld": "US", "The Smurfs": "Belgium",
    "Cabbage Patch Kids": "US", "Bratz": "US", "Fengshen Cinematic Universe": "China", "Terminator": "US", "Astro Boy": "Japan",
    "The Elder Scrolls": "US", "Godzilla (Gojira)": "Japan", "Madagascar": "US", "Winx Club": "Italy", "Planet of the Apes": "US",
    "Jumanji": "US", "Ghostbusters": "US", "Rocky": "US", "The Chronicles of Narnia": "UK", "Robert Langdon": "US", "Lego": "Denmark",
    "Farm Heroes Saga": "Sweden"}
def parent(owner: str) -> str:
    o = str(owner).lower(); best = None
    for name, rx in PARENTS:
        m = re.search(rx, o)
        if m and (best is None or m.start() < best[0]): best = (m.start(), name)
    return best[1] if best else re.sub(r"\s*\(.*", "", str(owner)).strip() or "Unknown"

# ---------- 1. Load + profile raw 2019 ----------
raw = pd.read_csv(D / "franchise.csv")
prof = {"rows": len(raw), "franchises": raw.franchise.nunique(), "missing_cells": int(raw.isna().sum().sum()),
        "dup_franchise_category": int(raw.duplicated(["franchise", "revenue_category"]).sum()),
        "placeholder_rows_lt_0.01B": int((raw.revenue < 0.0105).sum()),
        "citation_residue_cells": int(raw.apply(lambda c: c.astype(str).str.contains(r"\[\w+\]")).sum().sum()),
        "double_space_cells": int(raw.apply(lambda c: c.astype(str).str.contains("  ")).sum().sum()),
        "year_created_range": f"{raw.year_created.min()}-{raw.year_created.max()}"}
yr = raw.drop_duplicates("franchise").year_created
prof["franchises_by_decade"] = (yr // 10 * 10).value_counts().sort_index().to_dict()

# ---------- 2. Verify 2019 ledger against the Wikipedia revision it was scraped from ----------
w19 = {r["franchise"]: r for r in wp.parse_2019((RAW / "wiki_franchises_rev904026364_2019-06-29.wikitext").read_text())}
def norm(s): return re.sub(r"[^a-z0-9]", "", s.lower().replace("é", "e"))
w19n = {norm(k): v for k, v in w19.items()}
tot19 = raw.groupby("franchise").revenue.sum()
random.seed(SEED); sample = random.sample(sorted(tot19.index), 40)
ver = []
for f in sample:
    cand = [v for k, v in w19n.items() if k == norm(f) or k == norm(f.split("/")[0])]
    wt = cand[0]["total"] if cand else None
    ver.append({"franchise": f, "tidytuesday_sum_b": round(tot19[f], 3), "wiki_rev904026364_total_b": wt,
                "breakdown_sum_b": round(sum(x for _, x in cand[0]["breakdown"]), 3) if cand else None,
                "matched": bool(cand)})
ver = pd.DataFrame(ver)
m = ver[ver.matched]
ver["agree_breakdown_within_1pct"] = (abs(ver.tidytuesday_sum_b - ver.breakdown_sum_b) <= 0.01 * ver.breakdown_sum_b.fillna(0) + 0.002)
ver["agree_headline_within_10pct"] = (abs(ver.tidytuesday_sum_b - ver.wiki_rev904026364_total_b) <= 0.10 * ver.wiki_rev904026364_total_b.fillna(0))
ver.to_csv(OUT / "verification_sample_2019.csv", index=False)
agree = {"sample_n": len(ver), "matched": int(ver.matched.sum()),
         "breakdown_agree": int(ver[ver.matched].agree_breakdown_within_1pct.sum()),
         "headline_agree_10pct": int(ver[ver.matched].agree_headline_within_10pct.sum())}

# ---------- 3. Clean 2019 ledger ----------
c19 = raw.copy()
for col in ["franchise", "creators", "owners"]:
    c19[col] = c19[col].str.replace(r"\[[a-z0-9]+\]", "", regex=True).str.replace(r"\s+", " ", regex=True).str.strip()
c19["original_media_std"] = c19.original_media.replace(MEDIA_STD)
c19["placeholder_flag"] = c19.revenue < 0.0105
c19["owner_parent_2026"] = c19.owners.map(parent)
c19["region_origin"] = [infer_region_fields(f, o, c)[0] for f, o, c in zip(raw.franchise, raw.owners, raw.creators)]
c19.to_csv(OUT / "franchise_2019_clean.csv", index=False)

# ---------- 4. Build Oct-2026 ledger (long format) ----------
rows26 = wp.parse((RAW / "wiki_franchises_rev1379832186_2026-10-12.wikitext").read_text())
xw = {v[0]: k for k, v in CROSSWALK.items() if v[0]}
reg19 = dict(zip(c19.franchise, c19.region_origin))
long, ent, flow = [], [], {"wiki_rows_parsed": len(rows26)}
dropped = []
for r in rows26:
    if not r["total"]:
        dropped.append((r["franchise"], "no parseable total")); continue
    bsum = sum(v for _, v in r["breakdown"])
    over = bsum > r["total"] * 1.05
    f19 = xw.get(r["franchise"], "")
    r["owners"] = re.sub(r"\(\s*\)", "", r["owners"].split("|}")[0]).strip()
    reg = REGION26.get(r["franchise"]) or reg19.get(f19) or infer_region_fields(r["franchise"], r["owners"], r["creators"])[0] or "Unknown"
    ent.append({"franchise": r["franchise"], "franchise_2019_name": f19, "year_created": r["year_created"],
                "total_usd_b": r["total"], "breakdown_sum_usd_b": round(bsum, 4), "unallocated_usd_b": round(max(r["total"] - bsum, 0), 4),
                "breakdown_exceeds_total": over, "original_media": r["original_media"], "owners_raw": r["owners"],
                "owner_parent_2026": parent(r["owners"]), "region_origin": reg, "in_2019_ledger": bool(f19)})
    scale = r["total"] / bsum if over else 1.0  # rule R7: scale overshooting breakdowns to stated total
    for lab, v in r["breakdown"]:
        long.append({"franchise": r["franchise"], "category_raw": lab, "category": std_cat(lab), "revenue_usd_b": round(v * scale, 5)})
    if r["total"] - bsum > 1e-6 and not over:
        long.append({"franchise": r["franchise"], "category_raw": "(total minus itemised)", "category": "Unallocated", "revenue_usd_b": round(r["total"] - bsum, 5)})
e26 = pd.DataFrame(ent); l26 = pd.DataFrame(long)
dup = e26.duplicated("franchise").sum(); e26 = e26.drop_duplicates("franchise")
flow.update({"dropped_no_total": len(dropped), "dropped_duplicate_names": int(dup), "franchises_clean_2026": len(e26),
             "below_4B_floor": int((e26.total_usd_b < 4).sum()), "breakdown_overshoot_rescaled": int(e26.breakdown_exceeds_total.sum()),
             "with_unallocated_gt_5pct": int((e26.unallocated_usd_b > 0.05 * e26.total_usd_b).sum()),
             "matched_to_2019": int(e26.in_2019_ledger.sum()), "new_since_2019": int((~e26.in_2019_ledger).sum())})
e26.to_csv(OUT / "franchise_entities_2026-10.csv", index=False); l26.to_csv(OUT / "franchise_revenue_long_2026-10.csv", index=False)

# ---------- 5. 2025/2026 worldwide box office top-10 (new field) ----------
FR_KEYS = {"Ne Zha": "Ne Zha (Fengshen)", "Zootopia": "Zootopia", "Avatar": "Avatar", "Lilo & Stitch": "Lilo & Stitch",
           "Minecraft": "Minecraft", "Jurassic": "Jurassic Park", "Demon Slayer": "Demon Slayer", "Superman": "Superman",
           "Mission: Impossible": "Mission: Impossible", "F1": "", "Spider-Man": "Spider-Man", "Toy Story": "Toy Story",
           "Mario": "Mario", "Minions": "Despicable Me (Minions)", "Devil Wears Prada": "The Devil Wears Prada",
           "Pegasus": "Pegasus", "Fantastic Four": "Marvel Cinematic Universe", "Conjuring": "The Conjuring Universe",
           "Wicked": "Wicked", "How to Train Your Dragon": "How to Train Your Dragon", "Thunderbolts": "Marvel Cinematic Universe",
           "Captain America": "Marvel Cinematic Universe", "Final Destination": "Final Destination", "Chainsaw Man": "Chainsaw Man",
           "Detective Chinatown": "Detective Chinatown", "Five Nights": "Five Nights at Freddy's"}
bo = []
for yr_, fn in [(2025, "wiki_2025_in_film_rev1378645325.wikitext"), (2026, "wiki_2026_in_film_rev1379926625.wikitext")]:
    w = (RAW / fn).read_text(); i = w.find("==Highest-grossing films=="); tbl = w[i:w.find("|}", i)]
    for blk in re.split(r"\n\|-", tbl)[2:]:
        cells = [x for x in re.split(r"\n[|!]", blk) if x.strip()]
        if len(cells) < 4: continue
        title = re.sub(r"\s+", " ", wp.clean(re.sub(r"^\s*style=\"[^\"]*\"\s*\|", "", cells[1]))).strip()
        title = re.sub(r"\{\{sort\|[^|]*\|", "", title).strip(" }")
        g = cells[3]
        if "#expr" in g:
            gross = sum(int(x) for x in re.findall(r"\d{6,}", g))
        else:
            gross = int(re.sub(r"[^0-9]", "", wp.clean(g).split("\n")[0]) or 0)
        fr = next((v for k, v in FR_KEYS.items() if k.lower() in title.lower()), "")
        bo.append({"release_year": yr_, "rank": int(re.sub(r"\D", "", cells[0]) or 0), "title": title,
                   "distributor": re.sub(r"\s+", " ", wp.clean(cells[2])).strip(), "worldwide_gross_usd": gross,
                   "franchise_tag": fr, "is_franchise_film": bool(fr), "gross_as_of": "2026-10-12" if yr_ == 2026 else "final"})
bo = pd.DataFrame(bo); bo.to_csv(OUT / "worldwide_top10_box_office_2025_2026.csv", index=False)

# ---------- 6. CPI (FRED CPIAUCSL) ----------
cpi = pd.read_csv(RAW / "fred_CPIAUCSL_2026-10-12.csv"); cpi.columns = ["date", "cpi"]
cpi["year"] = cpi.date.str[:4].astype(int); ann = cpi.groupby("year").cpi.mean()
base = cpi.cpi.iloc[-1]; cpi_note = f"base = CPI-U {cpi.date.iloc[-1]} ({base})"
seg = pd.read_csv(D / "disney_segment_revenue_fy2024.csv")

# ---------- 7. Shares + bootstrap ----------
def shares(long_df, totals):
    s = long_df.groupby("category").revenue_usd_b.sum(); return s / totals
def boot(ent_ids, fn):
    ids = np.array(ent_ids); out = []
    for _ in range(B):
        out.append(fn(rng.choice(ids, len(ids), replace=True)))
    out = pd.DataFrame(out); return out.quantile(0.025), out.quantile(0.975)

l19 = c19.rename(columns={"revenue_category": "category", "revenue": "revenue_usd_b"})
def cat_share(df, ids):
    idx = pd.Series(ids).value_counts()
    t = df.set_index("franchise").join(idx.rename("w"), how="inner"); t["v"] = t.revenue_usd_b * t.w
    g = t.groupby("category").v.sum(); return (g / g.sum() * 100).to_dict()
res = {}
for lab, df, ids in [("2019", l19, c19.franchise.unique()), ("2026", l26, e26.franchise.values)]:
    point = cat_share(df, ids); lo, hi = boot(ids, lambda s: cat_share(df, s))
    res[lab] = {k: (round(point[k], 1), round(lo.get(k, np.nan), 1), round(hi.get(k, np.nan), 1)) for k in point}
pd.DataFrame([{"vintage": v, "category": k, "share_pct": a, "ci95_lo": b_, "ci95_hi": c} for v, d_ in res.items() for k, (a, b_, c) in d_.items()]).to_csv(OUT / "category_shares_bootstrap.csv", index=False)

def owner_shares(ent_df, col):
    t = ent_df.groupby(col).total_usd_b.sum().sort_values(ascending=False); return t / t.sum() * 100
e19 = c19.groupby("franchise").agg(total_usd_b=("revenue", "sum"), owner_parent_2026=("owner_parent_2026", "first"),
                                    region_origin=("region_origin", "first"), year_created=("year_created", "first")).reset_index()
def top_k(ent_df, ids, k):
    sub = ent_df.set_index("franchise").loc[ids]; t = sub.groupby("owner_parent_2026").total_usd_b.sum().sort_values(ascending=False)
    return t.iloc[:k].sum() / t.sum() * 100
conc = []
for lab, edf in [("2019 ledger, 2026 parents", e19), ("2026 ledger", e26)]:
    for k in (1, 5):
        pt = top_k(edf, edf.franchise.values, k)
        bs = [top_k(edf, rng.choice(edf.franchise.values, len(edf)), k) for _ in range(2000)]
        conc.append({"ledger": lab, "top_k": k, "share_pct": round(pt, 1), "ci95_lo": round(np.percentile(bs, 2.5), 1), "ci95_hi": round(np.percentile(bs, 97.5), 1),
                     "top_owners": "; ".join(owner_shares(edf, "owner_parent_2026").index[:k])})
pd.DataFrame(conc).to_csv(OUT / "owner_concentration_bootstrap.csv", index=False)

# region
def region_tbl(ent_df, long_df):
    r = ent_df.groupby("region_origin").agg(n=("franchise", "count"), total=("total_usd_b", "sum"))
    mer = long_df[long_df.category == "Merchandise, Licensing & Retail"].merge(ent_df[["franchise", "region_origin"]]).groupby("region_origin").revenue_usd_b.sum()
    r["merch_share_pct"] = (mer / r.total * 100).round(1); return r.round(3)
reg26 = region_tbl(e26, l26); reg26.to_csv(OUT / "region_summary_2026-10.csv")

# sensitivity
sens = []
nopl = l19[~c19.placeholder_flag.values]
sens.append(("2019 excl. 15 placeholder rows (<$0.01B)", cat_share(nopl, nopl.franchise.unique())))
alloc = l26[l26.category != "Unallocated"]; sens.append(("2026 excl. unallocated remainder", cat_share(alloc, e26.franchise.values)))
m82 = e26[e26.in_2019_ledger].franchise.values; sens.append(("2026 restricted to franchises matched to 2019", cat_share(l26, m82)))
big = e26[e26.total_usd_b >= 4].franchise.values; sens.append(("2026 >= $4B floor only", cat_share(l26, big)))
pd.DataFrame([{"scenario": s, "category": k, "share_pct": round(v, 1)} for s, d_ in sens for k, v in d_.items()]).to_csv(OUT / "sensitivity_category_shares.csv", index=False)

# ---------- 8. Old vs raw-new vs clean-new ----------
vn = pd.read_csv(D / "verified_numbers.csv")
T26 = e26.set_index("franchise").total_usd_b
def t26(name): return round(float(T26.get(name, np.nan)), 3)
s19 = tot19
cs19 = shares(l19, l19.revenue_usd_b.sum()) * 100; cs26 = res["2026"]
def ci(cat): a, b_, c = cs26.get(cat, (np.nan,) * 3); return f"{a} [{b_}–{c}]"
o19 = e19.groupby("owner_parent_2026").total_usd_b.sum()
o26 = e26.groupby("owner_parent_2026").total_usd_b.sum()
bo25 = bo[bo.release_year == 2025]; bo26 = bo[bo.release_year == 2026]
def fs(df): return round(df[df.is_franchise_film].worldwide_gross_usd.sum() / df.worldwide_gross_usd.sum() * 100, 1)
M = {
 "Franchises in dataset": (raw.franchise.nunique(), len(e26)),
 "Total lifetime revenue, all 103": (round(raw.revenue.sum(), 1), round(e26.total_usd_b.sum(), 1)),
 "Merchandise, Licensing & Retail share": (round(cs19["Merchandise, Licensing & Retail"], 1), ci("Merchandise, Licensing & Retail")),
 "Video games share": (round(cs19["Video Games/Games"], 1), ci("Video Games/Games")),
 "Box office share": (round(cs19["Box Office"], 1), ci("Box Office")),
 "Pokemon lifetime revenue": (round(s19["Pokémon"], 3), t26("Pokémon")),
 "Hello Kitty lifetime revenue": (round(s19["Hello Kitty"], 3), t26("Hello Kitty")),
 "Winnie the Pooh lifetime revenue": (round(s19["Winnie the Pooh"], 3), t26("Winnie-the-Pooh")),
 "Wikipedia franchises parsed (2026 scrape)": (140, len(rows26)),
 "Pokemon 2026 Wikipedia lifetime": (None, t26("Pokémon")),
 "Call of Duty 2026 Wikipedia lifetime": (None, t26("Call of Duty")),
 "Naruto 2026 Wikipedia lifetime": (None, t26("Naruto")),
 "Mortal Kombat 2026 Wikipedia lifetime": (None, t26("Mortal Kombat")),
 "Star Wars 2019 lifetime": (round(s19["Star Wars"], 3), t26("Star Wars")),
 "MCU 2019 lifetime": (round(s19["Marvel Cinematic Universe"], 3), t26("Marvel Cinematic Universe (MCU)")),
 "Disney consolidated owner total 2019": (None, round(o26.get("Disney", np.nan), 3)),
 "Top-five owner share after Fox consolidation": (None, f"{conc[3]['share_pct']} [{conc[3]['ci95_lo']}–{conc[3]['ci95_hi']}]"),
 "Top owner share after Fox consolidation": (None, f"{conc[2]['share_pct']} [{conc[2]['ci95_lo']}–{conc[2]['ci95_hi']}]"),
 "Japan region lifetime 2019": (None, reg26.total.get("Japan")), "US region lifetime 2019": (None, reg26.total.get("US")),
 "Japan merchandise share 2019": (None, reg26.merch_share_pct.get("Japan")), "US merchandise share 2019": (None, reg26.merch_share_pct.get("US")),
 "Japan franchise count 2019": (None, reg26.n.get("Japan")), "US franchise count 2019": (None, reg26.n.get("US")),
 "Toy Story 2019 lifetime": (round(s19["Toy Story"], 3), t26("Toy Story")),
 "Mario 2026 Wikipedia lifetime": (None, t26("Mario")), "Hello Kitty 2026 Wikipedia lifetime": (None, t26("Hello Kitty")),
 "Gundam 2026 Wikipedia lifetime": (None, t26("Gundam")), "Simpsons 2026 Wikipedia lifetime": (None, t26("The Simpsons")),
}
out = []
for _, r in vn.iterrows():
    rn, cn = M.get(r.figure, (None, None))
    out.append({"figure": r.figure, "old_published": str(r.value).split(" (")[0], "raw_new": rn if rn is not None else "", "clean_new_oct2026": "" if cn is None else cn, "unit": r.unit})
out += [{"figure": "NEW: franchise share of worldwide top-10 gross, 2025 releases", "old_published": "", "raw_new": "", "clean_new_oct2026": fs(bo25), "unit": "percent"},
        {"figure": "NEW: franchise share of worldwide top-10 gross, 2026 releases (to Oct 12)", "old_published": "", "raw_new": "", "clean_new_oct2026": fs(bo26), "unit": "percent"},
        {"figure": "NEW: franchises on Oct-2026 list not in 2019 ledger", "old_published": "", "raw_new": "", "clean_new_oct2026": flow["new_since_2019"], "unit": "count"}]
pd.DataFrame(out).to_csv(OUT / "old_vs_new.csv", index=False)
json.dump({"profile": prof, "verification": agree, "flow": flow, "dropped": dropped, "cpi": cpi_note,
           "cpi_2024_to_base_factor": round(base / ann[2024], 4)}, open(OUT / "audit_summary.json", "w"), indent=1, default=str)
print(json.dumps({"profile": prof, "verification": agree, "flow": flow}, indent=1, default=str))
