#!/usr/bin/env python3
"""Recompute franchise article verified figures and entity CSVs from committed data."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import urllib.request
from collections import defaultdict
from datetime import date
from difflib import SequenceMatcher
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ARTICLE = REPO / "articles" / "franchise"
DATA = ARTICLE / "data"
RAW = DATA / "raw"
ACCESS_DATE = "2026-10-11"
WIKI_USER_AGENT = "ArtometricsResearch/1.0 (https://artometrics.com; franchise phase1)"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_franchise_rows() -> list[dict[str, str]]:
    with (DATA / "franchise.csv").open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def normalize_name(name: str) -> str:
    s = name.lower()
    s = re.sub(r"[^\w\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    for old, new in (
        ("pokemon", "pokemon"),
        ("harry potter", "wizarding world"),
        ("wizarding world", "wizarding world"),
        ("marvel cinematic universe", "marvel cinematic universe"),
        ("mcu", "marvel cinematic universe"),
        ("star wars", "star wars"),
        ("winnie the pooh", "winnie the pooh"),
        ("winnie-the-pooh", "winnie the pooh"),
        ("game of thrones", "game of thrones"),
        ("a song of ice and fire", "game of thrones"),
    ):
        if old in s:
            s = new
    return s


def fetch_wikipedia_wikitext() -> str:
    url = (
        "https://en.wikipedia.org/w/api.php?action=query"
        "&titles=List_of_highest-grossing_media_franchises"
        "&prop=revisions&rvprop=content&rvslots=main&format=json"
    )
    req = urllib.request.Request(url, headers={"User-Agent": WIKI_USER_AGENT})
    with urllib.request.urlopen(req, timeout=120) as resp:
        payload = json.load(resp)
    pages = payload["query"]["pages"]
    return next(iter(pages.values()))["revisions"][0]["slots"]["main"]["*"]


def clean_wiki_cell(s: str) -> str:
    s = re.sub(r"\[\[([^|\]]+)\|([^\]]+)\]\]", r"\2", s)
    s = re.sub(r"\[\[([^\]]+)\]\]", r"\1", s)
    s = re.sub(r"''", "", s)
    s = re.sub(r"<[^>]+>", "", s)
    s = re.sub(r"\{\{[^}]+\}\}", "", s)
    return re.sub(r"\s+", " ", s).strip()


def parse_wikipedia_franchises(wikitext: str) -> list[dict]:
    rows: list[dict] = []
    for block in re.split(r"\n\|-", wikitext):
        if "! scope=row" not in block:
            continue
        m = re.search(r"! scope=row \| (.+)", block)
        if not m:
            continue
        name = clean_wiki_cell(m.group(1))
        parts = [p.strip() for p in block.split("\n|")[1:]]
        if len(parts) < 2:
            continue
        year = re.sub(r"[^0-9].*", "", parts[0]) or parts[0][:4]
        rev_cell = parts[1]
        display_m = re.search(r"\$([0-9,.]+)\s*billion", rev_cell, re.I)
        total_b = float(display_m.group(1).replace(",", "")) if display_m else None
        orig = clean_wiki_cell(parts[3]) if len(parts) > 3 else ""
        creators = clean_wiki_cell(parts[4]) if len(parts) > 4 else ""
        owners = clean_wiki_cell(parts[5]) if len(parts) > 5 else ""
        rows.append(
            {
                "franchise": name,
                "year_created": year,
                "total_revenue_usd_b_2026": total_b,
                "original_media": orig,
                "creators": creators,
                "owner_now": owners,
            }
        )
    return rows


def best_wiki_match(franchise: str, wiki_rows: list[dict]) -> dict | None:
    target = normalize_name(franchise)
    best: dict | None = None
    best_score = 0.0
    for row in wiki_rows:
        cand = normalize_name(row["franchise"])
        score = SequenceMatcher(None, target, cand).ratio()
        if target in cand or cand in target:
            score = max(score, 0.92)
        if score > best_score:
            best_score = score
            best = row
    return best if best_score >= 0.55 else None


def split_creators(raw: str) -> list[str]:
    if not raw or not raw.strip():
        return []
    parts = re.split(r"\s{2,}|\s+and\s+|,\s*", raw)
    out = []
    for p in parts:
        p = p.strip()
        if len(p) > 1:
            out.append(p)
    return out or [raw.strip()]


JAPAN_MARKERS = (
    "japan",
    "nintendo",
    "sanrio",
    "bandai",
    "toei",
    "shueisha",
    "shogakukan",
    "sony music japan",
    "tv tokyo",
    "pokemon",
    "anpanman",
    "dragon ball",
    "one piece",
    "hello kitty",
    "doraemon",
    "yokai watch",
    "gundam",
)


def region_bucket(franchise: str, owners: str, creators: str) -> str:
    blob = f"{franchise} {owners} {creators}".lower()
    if any(m in blob for m in JAPAN_MARKERS):
        return "Japan"
    us_markers = (
        "disney",
        "warner",
        "marvel",
        "dc comics",
        "universal",
        "paramount",
        "hasbro",
        "mattel",
        "lucasfilm",
        "pixar",
        "comcast",
        "amazon",
        "microsoft",
        "apple",
        "columbia",
    )
    if any(m in blob for m in us_markers):
        return "US"
    return "Other"


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    franchise_path = DATA / "franchise.csv"
    franchise_sha = sha256_file(franchise_path)

    rows = read_franchise_rows()
    totals: dict[str, dict] = {}
    for r in rows:
        fr = r["franchise"]
        rev = float(r["revenue"])
        if fr not in totals:
            totals[fr] = {
                "franchise": fr,
                "year_created": r["year_created"],
                "original_media": r["original_media"],
                "creators": r["creators"],
                "owners": r["owners"],
                "total": 0.0,
                "by_cat": defaultdict(float),
            }
        totals[fr]["total"] += rev
        totals[fr]["by_cat"][r["revenue_category"]] += rev

    grand_total = sum(t["total"] for t in totals.values())
    merch = sum(
        t["by_cat"].get("Merchandise, Licensing & Retail", 0.0) for t in totals.values()
    )
    games = sum(t["by_cat"].get("Video Games/Games", 0.0) for t in totals.values())
    bo = sum(t["by_cat"].get("Box Office", 0.0) for t in totals.values())
    pokemon_total = totals.get("Pokémon", {}).get("total")
    if pokemon_total is None:
        for k, v in totals.items():
            if "Pok" in k:
                pokemon_total = v["total"]
                break

    wikitext = fetch_wikipedia_wikitext()
    wiki_path = RAW / f"wikipedia_franchises_{ACCESS_DATE}.json"
    wiki_path.write_text(
        json.dumps({"access_date": ACCESS_DATE, "wikitext_bytes": len(wikitext)}, indent=2),
        encoding="utf-8",
    )
    wiki_rows = parse_wikipedia_franchises(wikitext)
    write_csv(
        DATA / "wikipedia_franchise_revenue_2026.csv",
        [
            "franchise",
            "year_created",
            "total_revenue_usd_b_2026",
            "original_media",
            "creators",
            "owner_now",
            "source_ids",
        ],
        [{**r, "source_ids": "S017"} for r in wiki_rows],
    )

    ent_franchises: list[dict] = []
    for fr, t in sorted(totals.items(), key=lambda x: -x[1]["total"]):
        top_cat = max(t["by_cat"].items(), key=lambda x: x[1])[0]
        merch_share = (
            t["by_cat"].get("Merchandise, Licensing & Retail", 0.0) / t["total"] * 100
            if t["total"]
            else 0.0
        )
        wiki = best_wiki_match(fr, wiki_rows)
        ent_franchises.append(
            {
                "franchise": fr,
                "year_created": t["year_created"],
                "original_media": t["original_media"],
                "creators": t["creators"],
                "owner_2019": t["owners"],
                "owner_now": wiki["owner_now"] if wiki else "",
                "total_revenue_usd_b_2019": round(t["total"], 3),
                "total_revenue_usd_b_2026": wiki["total_revenue_usd_b_2026"] if wiki else "",
                "top_revenue_stream": top_cat,
                "merch_share_pct": round(merch_share, 1),
                "box_office_usd_b": round(t["by_cat"].get("Box Office", 0.0), 3),
                "films_count": "",
                "source_ids": "S001;S017" if wiki else "S001",
            }
        )
    write_csv(
        DATA / "entities_franchises.csv",
        [
            "franchise",
            "year_created",
            "original_media",
            "creators",
            "owner_2019",
            "owner_now",
            "total_revenue_usd_b_2019",
            "total_revenue_usd_b_2026",
            "top_revenue_stream",
            "merch_share_pct",
            "box_office_usd_b",
            "films_count",
            "source_ids",
        ],
        ent_franchises,
    )

    # 2019 vs 2026 matched delta table for charts
    delta_rows = []
    for fr, t in totals.items():
        wiki = best_wiki_match(fr, wiki_rows)
        if not wiki or wiki["total_revenue_usd_b_2026"] is None:
            continue
        b19 = t["total"]
        b26 = wiki["total_revenue_usd_b_2026"]
        delta_rows.append(
            {
                "franchise": fr,
                "revenue_2019_b": round(b19, 3),
                "revenue_2026_b": b26,
                "pct_change": round((b26 - b19) / b19 * 100, 1) if b19 else "",
                "wiki_franchise_matched": wiki["franchise"],
                "source_ids": "S001;S017",
            }
        )
    write_csv(
        DATA / "franchise_revenue_2019_vs_2026.csv",
        [
            "franchise",
            "revenue_2019_b",
            "revenue_2026_b",
            "pct_change",
            "wiki_franchise_matched",
            "source_ids",
        ],
        sorted(delta_rows, key=lambda x: -float(x["pct_change"] or 0)),
    )

    # People
    people: dict[str, dict] = {}
    for fr, t in totals.items():
        for person in split_creators(t["creators"]):
            key = person.lower()
            if key not in people:
                people[key] = {"person": person, "role": "creator", "franchises": []}
            people[key]["franchises"].append(fr)
    ent_people = [
        {
            "person": v["person"],
            "role": v["role"],
            "franchises": "; ".join(sorted(set(v["franchises"]))),
            "source_ids": "S001",
        }
        for v in sorted(people.values(), key=lambda x: x["person"])
    ]
    write_csv(
        DATA / "entities_people.csv",
        ["person", "role", "franchises", "source_ids"],
        ent_people,
    )

    # Deals (seed + extensions)
    deals = [
        {
            "acquirer": "The Walt Disney Company",
            "target": "Pixar",
            "year": 2006,
            "price_usd_b": 7.4,
            "franchises_gained": "Toy Story; Cars; The Incredibles",
            "lifetime_revenue_gained_usd_b": 19.54,
            "source_ids": "S009;S001",
            "notes": "",
        },
        {
            "acquirer": "The Walt Disney Company",
            "target": "Marvel Entertainment",
            "year": 2009,
            "price_usd_b": 4.0,
            "franchises_gained": "Marvel Cinematic Universe",
            "lifetime_revenue_gained_usd_b": 31.0,
            "source_ids": "S010;S001",
            "notes": "",
        },
        {
            "acquirer": "The Walt Disney Company",
            "target": "Lucasfilm",
            "year": 2012,
            "price_usd_b": 4.05,
            "franchises_gained": "Star Wars; Indiana Jones",
            "lifetime_revenue_gained_usd_b": 63.004,
            "source_ids": "S011;S001",
            "notes": "",
        },
        {
            "acquirer": "The Walt Disney Company",
            "target": "21st Century Fox (film & TV)",
            "year": 2019,
            "price_usd_b": 71.3,
            "franchises_gained": "The Simpsons; Avatar; X-Men",
            "lifetime_revenue_gained_usd_b": 13.527,
            "source_ids": "S012;S001",
            "notes": "Enterprise value; franchise anchor is illustrative",
        },
        {
            "acquirer": "Comcast (NBCUniversal)",
            "target": "DreamWorks Animation",
            "year": 2016,
            "price_usd_b": 3.8,
            "franchises_gained": "Shrek; Kung Fu Panda; How to Train Your Dragon",
            "lifetime_revenue_gained_usd_b": "",
            "source_ids": "S055",
            "notes": "Price per Comcast 2016 8-K",
        },
        {
            "acquirer": "Hasbro",
            "target": "eOne",
            "year": 2019,
            "price_usd_b": 4.0,
            "franchises_gained": "Peppa Pig; PJ Masks",
            "lifetime_revenue_gained_usd_b": "",
            "source_ids": "S056",
            "notes": "",
        },
        {
            "acquirer": "Amazon",
            "target": "MGM Holdings",
            "year": 2022,
            "price_usd_b": 8.45,
            "franchises_gained": "James Bond; Rocky; Pink Panther",
            "lifetime_revenue_gained_usd_b": "",
            "source_ids": "S057",
            "notes": "Enterprise value per Amazon press release",
        },
    ]
    write_csv(
        DATA / "entities_companies_deals.csv",
        [
            "acquirer",
            "target",
            "year",
            "price_usd_b",
            "franchises_gained",
            "lifetime_revenue_gained_usd_b",
            "source_ids",
            "notes",
        ],
        deals,
    )

    # Region rollup
    region_stats: dict[str, dict] = defaultdict(lambda: {"count": 0, "revenue": 0.0, "merch": 0.0})
    for fr, t in totals.items():
        reg = region_bucket(fr, t["owners"], t["creators"])
        region_stats[reg]["count"] += 1
        region_stats[reg]["revenue"] += t["total"]
        region_stats[reg]["merch"] += t["by_cat"].get("Merchandise, Licensing & Retail", 0.0)
    region_rows = []
    for reg, st in region_stats.items():
        region_rows.append(
            {
                "region": reg,
                "franchise_count": st["count"],
                "lifetime_revenue_usd_b": round(st["revenue"], 3),
                "merch_share_pct": round(st["merch"] / st["revenue"] * 100, 1) if st["revenue"] else 0,
                "source_ids": "S001",
            }
        )
    write_csv(
        DATA / "franchise_region_summary.csv",
        ["region", "franchise_count", "lifetime_revenue_usd_b", "merch_share_pct", "source_ids"],
        region_rows,
    )

    # Medium stacked mix
    medium_mix: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    for fr, t in totals.items():
        om = t["original_media"] or "Unknown"
        for cat, val in t["by_cat"].items():
            medium_mix[om][cat] += val
    mix_rows = []
    for om, cats in medium_mix.items():
        tot = sum(cats.values())
        for cat, val in cats.items():
            mix_rows.append(
                {
                    "original_media": om,
                    "revenue_category": cat,
                    "revenue_usd_b": round(val, 3),
                    "share_within_medium_pct": round(val / tot * 100, 1) if tot else 0,
                    "source_ids": "S001",
                }
            )
    write_csv(
        DATA / "revenue_mix_by_original_medium.csv",
        [
            "original_media",
            "revenue_category",
            "revenue_usd_b",
            "share_within_medium_pct",
            "source_ids",
        ],
        mix_rows,
    )

    # Owner concentration before/after Fox (mid-2019 file)
    def consolidate_owner(o: str) -> str:
        if "Disney Company" in o:
            return "The Walt Disney Company (consolidated)"
        if "Lucasfilm" in o:
            return "The Walt Disney Company (consolidated)"
        if "Marvel Entertainment" in o:
            return "The Walt Disney Company (consolidated)"
        if "20th Century Fox" in o:
            return "The Walt Disney Company (consolidated)"
        return o

    owner_map: dict[str, float] = defaultdict(float)
    for t in totals.values():
        owner_map[consolidate_owner(t["owners"])] += t["total"]

    def consolidate_owner_pre_fox(o: str) -> str:
        if "Disney Company" in o:
            return "The Walt Disney Company (pre-Fox)"
        if "Lucasfilm" in o:
            return "The Walt Disney Company (pre-Fox)"
        if "Marvel Entertainment" in o:
            return "The Walt Disney Company (pre-Fox)"
        if "20th Century Fox" in o:
            return "21st Century Fox (standalone)"
        return o

    owner_pre: dict[str, float] = defaultdict(float)
    for t in totals.values():
        owner_pre[consolidate_owner_pre_fox(t["owners"])] += t["total"]

    conc_rows = []
    for label, mp in (("after_fox_consolidated", owner_map), ("before_fox_split", owner_pre)):
        top = sorted(mp.items(), key=lambda x: -x[1])[:5]
        top_sum = sum(v for _, v in top)
        conc_rows.append(
            {
                "scenario": label,
                "top5_owner_share_pct": round(top_sum / grand_total * 100, 1),
                "top_owner": top[0][0] if top else "",
                "top_owner_share_pct": round(top[0][1] / grand_total * 100, 1) if top else 0,
                "source_ids": "S001",
            }
        )
    write_csv(
        DATA / "owner_concentration_scenarios.csv",
        ["scenario", "top5_owner_share_pct", "top_owner", "top_owner_share_pct", "source_ids"],
        conc_rows,
    )

    verified = [
        ("Franchises in dataset", len(totals), "count", "unique franchise names", "data/franchise.csv", "S001"),
        ("Total lifetime revenue, all 103", round(grand_total, 1), "USD billions", "sum of revenue", "data/franchise.csv", "S001"),
        ("Merchandise, Licensing & Retail share", round(merch / grand_total * 100, 1), "percent of total", "category sum / total", "data/franchise.csv", "S001"),
        ("Video games share", round(games / grand_total * 100, 1), "percent", "category sum / total", "data/franchise.csv", "S001"),
        ("Box office share", round(bo / grand_total * 100, 1), "percent", "category sum / total", "data/franchise.csv", "S001"),
        (
            "Pokemon lifetime revenue",
            f"{round(pokemon_total, 3)} (on screen: $90.9B; spoken: ninety point nine billion)",
            "USD billions",
            "sum of Pokemon rows",
            "data/franchise.csv",
            "S001",
        ),
        ("Hello Kitty lifetime revenue", round(totals.get("Hello Kitty", {}).get("total", 0), 3), "USD billions", "sum of rows", "data/franchise.csv", "S001"),
        ("Winnie the Pooh lifetime revenue", round(totals.get("Winnie the Pooh", {}).get("total", 0), 3), "USD billions", "sum of rows", "data/franchise.csv", "S001"),
        ("franchise.csv SHA-256", franchise_sha, "hash", "sha256sum", "data/franchise.csv", "S001"),
        ("Wikipedia franchises parsed (2026 scrape)", len(wiki_rows), "count", "parse_wikipedia_franchises", "data/wikipedia_franchise_revenue_2026.csv", "S017"),
        ("2019↔2026 matched franchises", len(delta_rows), "count", "fuzzy name match", "data/franchise_revenue_2019_vs_2026.csv", "S001;S017"),
    ]
    write_csv(
        DATA / "verified_numbers.csv",
        ["figure", "value", "unit", "computed_how", "file", "source_ids", "status"],
        [
            {
                "figure": f[0],
                "value": f[1],
                "unit": f[2],
                "computed_how": f[3],
                "file": f[4],
                "source_ids": f[5],
                "status": f"verified (recomputed {ACCESS_DATE})",
            }
            for f in verified
        ],
    )

    print(f"Wrote entity + verified tables ({len(totals)} franchises, wiki {len(wiki_rows)} rows)")


if __name__ == "__main__":
    main()
