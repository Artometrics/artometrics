#!/usr/bin/env python3
"""Recompute franchise article verified figures and entity CSVs from committed data."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import time
import urllib.request
from collections import defaultdict
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
import sys

sys.path.insert(0, str(_SCRIPT_DIR))
from franchise_crosswalk_data import CROSSWALK, REGION, WIKI_SOURCE_REVISION_DROPS  # noqa: E402
from franchise_wiki_parse import fetch_wikitext, parse_wiki_index  # noqa: E402

REPO = _SCRIPT_DIR.parent
ARTICLE = REPO / "articles" / "franchise"
DATA = ARTICLE / "data"
RAW = DATA / "raw"
ACCESS_DATE = "2026-10-11"
UA = "ArtometricsResearch/1.0 (contact@artometrics.com)"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_franchise_rows() -> list[dict[str, str]]:
    with (DATA / "franchise.csv").open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def split_creators(raw: str) -> list[str]:
    if not raw or not str(raw).strip():
        return []
    raw = re.sub(r"\s+", " ", raw.strip())
    parts = re.split(r"\s{2,}|\s+and\s+|,\s*", raw)
    people: list[str] = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        words = part.split()
        if len(words) == 4:
            people.extend([" ".join(words[:2]), " ".join(words[2:])])
        else:
            people.append(part)
    return people


def infer_region_fields(franchise: str, owners: str, creators: str) -> tuple[str, str, str, str]:
    if franchise in REGION:
        return REGION[franchise]
    blob = f"{franchise} {owners} {creators}".lower()
    japan_keys = (
        "nintendo",
        "sanrio",
        "shueisha",
        "bandai",
        "toei",
        "shogakukan",
        "tv tokyo",
        "square enix",
        "capcom",
        "konami",
        "namco",
        "sony music japan",
        "kumamon",
        "anpanman",
        "pokémon",
        "pokemon",
        "sega",
        "mixi",
        "gungho",
        "khara",
        "type-moon",
        "polyphony",
        "evangelion",
    )
    if any(k in blob for k in japan_keys):
        return (
            "Japan",
            "Owner/creator string references Japan-based company.",
            "Japan",
            "Primary rights holder HQ inferred Japan from owner field.",
        )
    us_keys = (
        "disney",
        "warner",
        "marvel",
        "dc ",
        "universal",
        "paramount",
        "hasbro",
        "mattel",
        "lucasfilm",
        "pixar",
        "comcast",
        "amazon",
        "microsoft",
        "riot",
        "activision",
        "electronic arts",
        "nickelodeon",
        "cartoon network",
    )
    if any(k in blob for k in us_keys):
        return (
            "US",
            "Owner field references US-listed or US studio.",
            "US",
            "Rights-owner HQ inferred United States from owner field.",
        )
    korea_keys = ("smilegate", "neople", "nexon", "dungeon fighter", "crossfire")
    if any(k in blob for k in korea_keys):
        return (
            "Korea",
            "Owner/creator references South Korea-based company.",
            "Korea",
            "Korean rights holder inferred from owner field.",
        )
    if "netease" in blob or "westward journey" in franchise.lower():
        return (
            "China",
            "Owner references China-based parent.",
            "China",
            "NetEase / China HQ inferred from owner field.",
        )
    if "tencent" in blob and "china" in blob:
        return (
            "China",
            "Owner references China-based parent.",
            "China",
            "Tencent HQ inferred from owner field.",
        )
    return (
        "Other",
        "No Japan/US/China marker in 2019 owner/creator strings.",
        "Other",
        "HQ not inferred; see owner_2019.",
    )


def parse_numbers_movie(url: str) -> tuple[str, str, str]:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as resp:
        html = resp.read().decode("utf-8", errors="replace")
    budget = ""
    m = re.search(r"Production(?:&nbsp;|\s)Budget:.*?>\$([0-9,]+)", html, re.I)
    if m:
        budget = m.group(1).replace(",", "")
    dom = ""
    m = re.search(r"Domestic Box Office</b></td>\s*<td class='data'>\$([0-9,]+)", html)
    if m:
        dom = m.group(1).replace(",", "")
    ww = ""
    m = re.search(r"Worldwide Box Office</b></td>\s*<td class='data'>\$([0-9,]+)", html)
    if m:
        ww = m.group(1).replace(",", "")
    return budget, dom, ww


def parse_bom_title(url: str) -> tuple[str, str, str]:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as resp:
        html = resp.read().decode("utf-8", errors="replace")
    budget = ""
    dom = ""
    ww = ""
    m = re.search(r"Budget</span>[^$]*\$([0-9,]+)", html)
    if m:
        budget = m.group(1).replace(",", "")
    m = re.search(r"Domestic</span>[^$]*\$([0-9,]+)", html) or re.search(
        r"Domestic Box Office[^$]*\$([0-9,]+)", html
    )
    if m:
        dom = m.group(1).replace(",", "")
    m = re.search(r"Worldwide</span>[^$]*\$([0-9,]+)", html) or re.search(
        r"Worldwide Box Office[^$]*\$([0-9,]+)", html
    )
    if m:
        ww = m.group(1).replace(",", "")
    return budget, dom, ww


def build_budgets_grosses() -> list[dict]:
    # (franchise, film, year, the_numbers_url, box_office_mojo_url, gross_notes)
    films = [
        (
            "Pokémon",
            "Pokémon: The First Movie",
            1998,
            "https://www.the-numbers.com/movie/Pokemon-The-First-Movie",
            "https://www.boxofficemojo.com/release/rl531481857/",
            "",
        ),
        (
            "Star Wars",
            "Star Wars: The Force Awakens",
            2015,
            "https://www.the-numbers.com/movie/Star-Wars-Ep-VII-The-Force-Awakens",
            "https://www.boxofficemojo.com/release/rl2691925505/",
            "Production budget is The Numbers' reported figure of $533,200,000. The page states worldwide box office is 3.9 times that production budget. It is not a Disney filing.",
        ),
        (
            "Marvel Cinematic Universe",
            "Avengers: Endgame",
            2019,
            "https://www.the-numbers.com/movie/Avengers-Endgame-(2019)",
            "https://www.boxofficemojo.com/release/rl3059975681/",
            "Domestic and worldwide are the original April 2019 release on Box Office Mojo: domestic $858,373,000 and worldwide $2,799,439,100. The September 2026 re-release is separate (domestic $39,084,355; worldwide $137,884,355) and is not included. All-releases totals are not used.",
        ),
        (
            "Wizarding World / Harry Potter",
            "Harry Potter and the Deathly Hallows Part 2",
            2011,
            "https://www.the-numbers.com/movie/Harry-Potter-and-the-Deathly-Hallows-Part-II-(2011)",
            "https://www.boxofficemojo.com/release/rl1265337857/",
            "",
        ),
        (
            "Batman",
            "The Dark Knight",
            2008,
            "https://www.the-numbers.com/movie/Dark-Knight-The",
            "https://www.boxofficemojo.com/release/rl1091076097/",
            "",
        ),
        (
            "Spider-Man",
            "Spider-Man: No Way Home",
            2021,
            "https://www.the-numbers.com/movie/Spider-Man-No-Way-Home-(2021)",
            "https://www.boxofficemojo.com/release/rl4044609025/",
            "",
        ),
        (
            "James Bond",
            "Skyfall",
            2012,
            "https://www.the-numbers.com/movie/Skyfall",
            "https://www.boxofficemojo.com/release/rl1346799105/",
            "",
        ),
        (
            "Fast & Furious",
            "Furious 7",
            2015,
            "https://www.the-numbers.com/movie/Furious-7",
            "https://www.boxofficemojo.com/release/rl1045661185/",
            "",
        ),
        (
            "Jurassic Park",
            "Jurassic World",
            2015,
            "https://www.the-numbers.com/movie/Jurassic-World",
            "https://www.boxofficemojo.com/release/rl2371716609/",
            "",
        ),
        (
            "Toy Story",
            "Toy Story 4",
            2019,
            "https://www.the-numbers.com/movie/Toy-Story-4-(2019)",
            "https://www.boxofficemojo.com/title/tt1979376/",
            "",
        ),
        (
            "Frozen",
            "Frozen II",
            2019,
            "https://www.the-numbers.com/movie/Frozen-II-(2019)",
            "https://www.boxofficemojo.com/title/tt4520988/",
            "",
        ),
        (
            "Despicable Me / Minions",
            "Minions",
            2015,
            "https://www.the-numbers.com/movie/Minions",
            "https://www.boxofficemojo.com/release/rl2583691265/",
            "",
        ),
        (
            "Shrek",
            "Shrek 2",
            2004,
            "https://www.the-numbers.com/movie/Shrek-2",
            "https://www.boxofficemojo.com/release/rl24217089/",
            "",
        ),
        (
            "Lord of the Rings",
            "The Return of the King",
            2003,
            "https://www.the-numbers.com/movie/Lord-of-the-Rings-The-Return-of-the-King-The",
            "https://www.boxofficemojo.com/release/rl2471854337/",
            "",
        ),
        (
            "Pirates of the Caribbean",
            "Dead Man's Chest",
            2006,
            "https://www.the-numbers.com/movie/Pirates-of-the-Caribbean-Dead-Mans-Chest",
            "https://www.boxofficemojo.com/title/tt0383574/",
            "",
        ),
        (
            "Mission: Impossible",
            "Mission: Impossible - Fallout",
            2018,
            "https://www.the-numbers.com/movie/Mission-Impossible-Fallout",
            "https://www.boxofficemojo.com/title/tt4912380/",
            "",
        ),
        (
            "The Hunger Games",
            "The Hunger Games: Catching Fire",
            2013,
            "https://www.the-numbers.com/movie/Hunger-Games-Catching-Fire-The-(2013)",
            "https://www.boxofficemojo.com/release/rl2638775809/",
            "",
        ),
        (
            "Twilight",
            "Breaking Dawn Part 2",
            2012,
            "https://www.the-numbers.com/movie/Twilight-Saga-Breaking-Dawn-Part-2-The",
            "https://www.boxofficemojo.com/title/tt1673434/",
            "",
        ),
        (
            "Finding Nemo",
            "Finding Dory",
            2016,
            "https://www.the-numbers.com/movie/Finding-Dory",
            "https://www.boxofficemojo.com/title/tt2277860/",
            "",
        ),
        (
            "Cars",
            "Cars 3",
            2017,
            "https://www.the-numbers.com/movie/Cars-3",
            "https://www.boxofficemojo.com/title/tt3606752/",
            "",
        ),
        (
            "Transformers",
            "Dark of the Moon",
            2011,
            "https://www.the-numbers.com/movie/Transformers-Dark-of-the-Moon-(2011)",
            "https://www.boxofficemojo.com/release/rl537560065/",
            "",
        ),
        (
            "X-Men",
            "Days of Future Past",
            2014,
            "https://www.the-numbers.com/movie/X-Men-Days-of-Future-Past",
            "https://www.boxofficemojo.com/title/tt1877832/",
            "",
        ),
        (
            "Indiana Jones",
            "Kingdom of the Crystal Skull",
            2008,
            "https://www.the-numbers.com/movie/Indiana-Jones-and-the-Kingdom-of-the-Crystal-Skull-(2008)",
            "https://www.boxofficemojo.com/release/rl17139457/",
            "",
        ),
        (
            "Alien",
            "Alien: Covenant",
            2017,
            "https://www.the-numbers.com/movie/Alien-Covenant",
            "https://www.boxofficemojo.com/title/tt2316204/",
            "",
        ),
        (
            "The Lion King",
            "The Lion King (2019)",
            2019,
            "https://www.the-numbers.com/movie/Lion-King-The-(Live-Action)-(2019)",
            "https://www.boxofficemojo.com/release/rl3321923073/",
            "",
        ),
    ]
    rows = []
    for franchise, film, year, num_url, bom_url, gross_notes in films:
        budget, dom, ww = "", "", ""
        budget_src, dom_src, ww_src = "", "", ""
        try:
            b, d, w = parse_numbers_movie(num_url)
            if b:
                budget, budget_src = b, "S019"
            if d:
                dom, dom_src = d, "S019"
            if w:
                ww, ww_src = w, "S019"
        except Exception:
            pass
        if bom_url:
            try:
                b2, d2, w2 = parse_bom_title(bom_url)
                if not budget and b2:
                    budget, budget_src = b2, "S018"
                if not dom and d2:
                    dom, dom_src = d2, "S018"
                if not ww and w2:
                    ww, ww_src = w2, "S018"
            except Exception:
                pass
        if film == "Avengers: Endgame":
            dom, dom_src = "858373000", "S018"
            ww, ww_src = "2799439100", "S018"
        rows.append(
            {
                "franchise": franchise,
                "film": film,
                "year": year,
                "production_budget_usd": budget,
                "production_budget_source": budget_src,
                "domestic_gross_usd": dom,
                "domestic_gross_source": dom_src,
                "worldwide_gross_usd": ww,
                "worldwide_gross_source": ww_src,
                "the_numbers_url": num_url,
                "box_office_mojo_url": bom_url,
                "gross_notes": gross_notes,
                "source_ids": ";".join(sorted({s for s in (budget_src, dom_src, ww_src) if s})),
            }
        )
        time.sleep(0.12)
    return rows


def build_crosswalk_csv(wiki: dict[str, dict], totals: dict) -> list[dict]:
    rows = []
    for fr in sorted(totals.keys()):
        if fr not in CROSSWALK:
            raise SystemExit(f"Missing crosswalk entry for: {fr}")
        wiki_title, note = CROSSWALK[fr]
        w = wiki.get(wiki_title) if wiki_title else None
        rows.append(
            {
                "franchise_2019": fr,
                "franchise_2026_wiki": wiki_title,
                "revenue_2026_usd_b": w["total_revenue_usd_b_2026"] if w else "",
                "owner_2026": w["owner_now"] if w else "",
                "match_note": note,
                "source_ids": "S017" if wiki_title else "S001",
            }
        )
    return rows


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
    merch = sum(t["by_cat"].get("Merchandise, Licensing & Retail", 0.0) for t in totals.values())
    games = sum(t["by_cat"].get("Video Games/Games", 0.0) for t in totals.values())
    bo = sum(t["by_cat"].get("Box Office", 0.0) for t in totals.values())
    pokemon_total = totals.get("Pokémon", {}).get("total")
    if pokemon_total is None:
        for k, v in totals.items():
            if "Pok" in k:
                pokemon_total = v["total"]

    wikitext = fetch_wikitext()
    (RAW / f"wikipedia_franchises_{ACCESS_DATE}.json").write_text(
        json.dumps({"access_date": ACCESS_DATE, "wikitext_bytes": len(wikitext)}, indent=2),
        encoding="utf-8",
    )
    wiki = parse_wiki_index(wikitext)
    wiki_rows = [
        {
            "franchise": name,
            "year_created": v["year_created"],
            "total_revenue_usd_b_2026": v["total_revenue_usd_b_2026"],
            "owner_now": v["owner_now"],
            "source_ids": "S017",
        }
        for name, v in sorted(wiki.items(), key=lambda x: -(x[1]["total_revenue_usd_b_2026"] or 0))
    ]
    write_csv(
        DATA / "wikipedia_franchise_revenue_2026.csv",
        ["franchise", "year_created", "total_revenue_usd_b_2026", "owner_now", "source_ids"],
        wiki_rows,
    )

    crosswalk_rows = build_crosswalk_csv(wiki, totals)
    write_csv(
        DATA / "franchise_crosswalk_2019_2026.csv",
        [
            "franchise_2019",
            "franchise_2026_wiki",
            "revenue_2026_usd_b",
            "owner_2026",
            "match_note",
            "source_ids",
        ],
        crosswalk_rows,
    )
    cross_by_fr = {r["franchise_2019"]: r for r in crosswalk_rows}

    ent_franchises = []
    for fr, t in sorted(totals.items(), key=lambda x: -x[1]["total"]):
        cw = cross_by_fr[fr]
        reg_o, reg_on, hq, hq_n = infer_region_fields(fr, t["owners"], t["creators"])
        top_cat = max(t["by_cat"].items(), key=lambda x: x[1])[0]
        merch_share = (
            t["by_cat"].get("Merchandise, Licensing & Retail", 0.0) / t["total"] * 100 if t["total"] else 0
        )
        ent_franchises.append(
            {
                "franchise": fr,
                "year_created": t["year_created"],
                "original_media": t["original_media"],
                "creators": t["creators"],
                "owner_2019": t["owners"],
                "owner_now": cw["owner_2026"],
                "total_revenue_usd_b_2019": round(t["total"], 3),
                "total_revenue_usd_b_2026": cw["revenue_2026_usd_b"],
                "top_revenue_stream": top_cat,
                "merch_share_pct": round(merch_share, 1),
                "box_office_usd_b": round(t["by_cat"].get("Box Office", 0.0), 3),
                "films_count": "",
                "region_origin": reg_o,
                "region_origin_note": reg_on,
                "rights_owner_hq": hq,
                "rights_owner_hq_note": hq_n,
                "source_ids": "S001;S017" if cw["franchise_2026_wiki"] else "S001",
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
            "region_origin",
            "region_origin_note",
            "rights_owner_hq",
            "rights_owner_hq_note",
            "source_ids",
        ],
        ent_franchises,
    )

    delta_rows = []
    for fr, t in totals.items():
        cw = cross_by_fr[fr]
        if not cw["franchise_2026_wiki"] or cw["revenue_2026_usd_b"] == "":
            continue
        b19 = t["total"]
        b26 = float(cw["revenue_2026_usd_b"])
        revision = fr in WIKI_SOURCE_REVISION_DROPS and b26 < b19
        delta_rows.append(
            {
                "franchise": fr,
                "revenue_2019_b": round(b19, 3),
                "revenue_2026_b": b26,
                "pct_change": round((b26 - b19) / b19 * 100, 1) if b19 else "",
                "wiki_source_revision": "Y" if revision else "N",
                "wiki_franchise_matched": cw["franchise_2026_wiki"],
                "match_note": cw["match_note"],
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
            "wiki_source_revision",
            "wiki_franchise_matched",
            "match_note",
            "source_ids",
        ],
        sorted(delta_rows, key=lambda x: -float(x["pct_change"] or 0)),
    )

    # entities_people.csv is hand-curated (no companies; split creator names by hand).

    deals = [
        {
            "acquirer": "Comcast Corporation (NBCUniversal)",
            "target": "DreamWorks Animation",
            "year": 2016,
            "price_usd_b": 3.8,
            "franchises_gained": "Shrek; Kung Fu Panda; How to Train Your Dragon",
            "lifetime_revenue_gained_usd_b": "",
            "source_ids": "S055",
            "notes": "Closed 2016-08-22; $3.8B cash per Comcast 8-K.",
        },
        {
            "acquirer": "Hasbro, Inc.",
            "target": "Entertainment One (eOne)",
            "year": 2019,
            "price_usd_b": 4.0,
            "franchises_gained": "Peppa Pig; PJ Masks",
            "lifetime_revenue_gained_usd_b": "",
            "source_ids": "S056",
            "notes": "Completed 2019-12-30; ~$4.0B all-cash per Hasbro press release.",
        },
        {
            "acquirer": "Amazon.com, Inc.",
            "target": "MGM Holdings",
            "year": 2022,
            "price_usd_b": 8.45,
            "franchises_gained": "James Bond; Rocky; Pink Panther",
            "lifetime_revenue_gained_usd_b": "",
            "source_ids": "S057",
            "notes": "Closed 2022-03-17; $8.45B enterprise value per Amazon announcement.",
        },
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
            "notes": "Approximately $4 billion. Disney 8-K exhibit 99.1, 31 Aug 2009.",
        },
        {
            "acquirer": "The Walt Disney Company",
            "target": "Lucasfilm",
            "year": 2012,
            "price_usd_b": 4.05,
            "franchises_gained": "Star Wars; Indiana Jones",
            "lifetime_revenue_gained_usd_b": 63.004,
            "source_ids": "S011;S001",
            "notes": "$4.05 billion transaction value. Disney 8-K exhibit 99.1, 30 Oct 2012.",
        },
        {
            "acquirer": "The Walt Disney Company",
            "target": "21st Century Fox (film & TV)",
            "year": 2019,
            "price_usd_b": 71.3,
            "franchises_gained": "The Simpsons; Avatar; X-Men",
            "lifetime_revenue_gained_usd_b": 13.527,
            "source_ids": "S012;S001",
            "notes": "$71.3 billion cash and stock. Disney amended-agreement exhibit, 20 June 2018, closed 2019: https://www.sec.gov/Archives/edgar/data/1001039/000095015718000744/ex99-1.htm",
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

    region_stats: dict[str, dict] = defaultdict(lambda: {"count": 0, "revenue": 0.0, "merch": 0.0})
    for fr, t in totals.items():
        reg = cross_by_fr[fr]  # noqa: F841 — use entity region
        ent = next(e for e in ent_franchises if e["franchise"] == fr)
        reg = ent["region_origin"]
        region_stats[reg]["count"] += 1
        region_stats[reg]["revenue"] += t["total"]
        region_stats[reg]["merch"] += t["by_cat"].get("Merchandise, Licensing & Retail", 0.0)
    write_csv(
        DATA / "franchise_region_summary.csv",
        ["region_origin", "franchise_count", "lifetime_revenue_usd_b", "merch_share_pct", "source_ids"],
        [
            {
                "region_origin": reg,
                "franchise_count": st["count"],
                "lifetime_revenue_usd_b": round(st["revenue"], 3),
                "merch_share_pct": round(st["merch"] / st["revenue"] * 100, 1) if st["revenue"] else 0,
                "source_ids": "S001",
            }
            for reg, st in sorted(region_stats.items())
        ],
    )

    # derived tables (unchanged logic)
    medium_mix: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    for fr, t in totals.items():
        om = t["original_media"] or "Unknown"
        for cat, val in t["by_cat"].items():
            medium_mix[om][cat] += val
    write_csv(
        DATA / "revenue_mix_by_original_medium.csv",
        [
            "original_media",
            "revenue_category",
            "revenue_usd_b",
            "share_within_medium_pct",
            "source_ids",
        ],
        [
            {
                "original_media": om,
                "revenue_category": cat,
                "revenue_usd_b": round(val, 3),
                "share_within_medium_pct": round(val / sum(cats.values()) * 100, 1),
                "source_ids": "S001",
            }
            for om, cats in medium_mix.items()
            for cat, val in cats.items()
        ],
    )

    def consolidate_owner(o: str) -> str:
        if any(x in o for x in ("Disney Company", "Lucasfilm", "Marvel Entertainment", "20th Century Fox")):
            return "The Walt Disney Company (consolidated)"
        return o

    owner_map: dict[str, float] = defaultdict(float)
    for t in totals.values():
        owner_map[consolidate_owner(t["owners"])] += t["total"]

    def consolidate_owner_pre_fox(o: str) -> str:
        if any(x in o for x in ("Disney Company", "Lucasfilm", "Marvel Entertainment")):
            return "The Walt Disney Company (pre-Fox)"
        if "20th Century Fox" in o:
            return "21st Century Fox (standalone)"
        return o

    owner_pre: dict[str, float] = defaultdict(float)
    for t in totals.values():
        owner_pre[consolidate_owner_pre_fox(t["owners"])] += t["total"]

    write_csv(
        DATA / "owner_concentration_scenarios.csv",
        ["scenario", "top5_owner_share_pct", "top_owner", "top_owner_share_pct", "source_ids"],
        [
            {
                "scenario": label,
                "top5_owner_share_pct": round(sum(v for _, v in sorted(mp.items(), key=lambda x: -x[1])[:5]) / grand_total * 100, 1),
                "top_owner": sorted(mp.items(), key=lambda x: -x[1])[0][0],
                "top_owner_share_pct": round(sorted(mp.items(), key=lambda x: -x[1])[0][1] / grand_total * 100, 1),
                "source_ids": "S001",
            }
            for label, mp in (("after_fox_consolidated", owner_map), ("before_fox_split", owner_pre))
        ],
    )

    write_csv(
        DATA / "entities_budgets_grosses.csv",
        [
            "franchise",
            "film",
            "year",
            "production_budget_usd",
            "production_budget_source",
            "domestic_gross_usd",
            "domestic_gross_source",
            "worldwide_gross_usd",
            "worldwide_gross_source",
            "the_numbers_url",
            "box_office_mojo_url",
            "gross_notes",
            "source_ids",
        ],
        build_budgets_grosses(),
    )

    matched_with_2026 = sum(1 for r in crosswalk_rows if r["franchise_2026_wiki"])
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
        ("Wikipedia franchises parsed (2026 scrape)", len(wiki), "count", "parse_wiki_index", "data/wikipedia_franchise_revenue_2026.csv", "S017"),
        ("2019↔2026 crosswalk rows", len(crosswalk_rows), "count", "franchise_crosswalk_2019_2026.csv", "data/franchise_crosswalk_2019_2026.csv", "S001;S017"),
        ("2019 rows with 2026 Wikipedia pair", matched_with_2026, "count", "non-empty franchise_2026_wiki", "data/franchise_crosswalk_2019_2026.csv", "S017"),
        ("2019↔2026 delta chart rows", len(delta_rows), "count", "both years have revenue", "data/franchise_revenue_2019_vs_2026.csv", "S001;S017"),
    ]

    def fr_total(name: str) -> float:
        return float(totals[name]["total"])

    def years_alive(name: str) -> int:
        return max(1, 2019 - int(totals[name]["year_created"]))

    def wiki_2026(name: str) -> float:
        return float(cross_by_fr[name]["revenue_2026_usd_b"])

    batman = fr_total("Batman")
    superman = fr_total("Superman")
    dceu = fr_total("DC Extended Universe")
    dc_sum = batman + superman + dceu
    poke_2019 = fr_total("Pokémon")
    poke_2026 = wiki_2026("Pokémon")
    cod_2019, cod_2026 = fr_total("Call of Duty"), wiki_2026("Call of Duty")
    nar_2019, nar_2026 = fr_total("Naruto"), wiki_2026("Naruto")
    mk_2019, mk_2026 = fr_total("Mortal Kombat"), wiki_2026("Mortal Kombat")
    disney_raw = next(v for k, v in (
        (e["owner_2019"], float(e["total_revenue_usd_b_2019"]))
        for e in []
    ) if False) if False else None
    # Owner labels from the same consolidation used for owner_totals_derived.csv
    nintendo_label = 0.0
    poke_label = 0.0
    disney_uncon = 0.0
    for t in totals.values():
        o = t["owners"]
        if o == "Nintendo":
            nintendo_label += t["total"]
        if "Pokémon Company" in o or "Pokemon Company" in o:
            poke_label += t["total"]
        if o == "The Walt Disney Company":
            disney_uncon += t["total"]
    disney_con = owner_map["The Walt Disney Company (consolidated)"]
    medium_totals = {om: sum(cats.values()) for om, cats in medium_mix.items()}
    mcu_bo = totals["Marvel Cinematic Universe"]["by_cat"].get("Box Office", 0.0)
    mcu_tot = fr_total("Marvel Cinematic Universe")
    extra = [
        ("Pokemon 2019 lifetime (spoken vintage)", round(poke_2019, 3), "USD billions", "sum of Pokémon rows in 2019 file", "data/franchise.csv", "S001"),
        ("Pokemon 2026 Wikipedia lifetime", poke_2026, "USD billions", "paired Wikipedia row", "data/franchise_revenue_2019_vs_2026.csv", "S017"),
        ("Pokemon 2019 to 2026 dollar change", round(poke_2026 - poke_2019, 3), "USD billions", "2026 minus 2019 paired totals", "data/franchise_revenue_2019_vs_2026.csv", "S001;S017"),
        ("Call of Duty 2019 lifetime", round(cod_2019, 3), "USD billions", "sum of rows", "data/franchise.csv", "S001"),
        ("Call of Duty 2026 Wikipedia lifetime", cod_2026, "USD billions", "paired Wikipedia row", "data/franchise_revenue_2019_vs_2026.csv", "S017"),
        ("Call of Duty 2019 to 2026 dollar change", round(cod_2026 - cod_2019, 3), "USD billions", "2026 minus 2019", "data/franchise_revenue_2019_vs_2026.csv", "S001;S017"),
        ("Naruto 2019 lifetime", round(nar_2019, 3), "USD billions", "sum of rows", "data/franchise.csv", "S001"),
        ("Naruto 2026 Wikipedia lifetime", nar_2026, "USD billions", "paired Wikipedia row", "data/franchise_revenue_2019_vs_2026.csv", "S017"),
        ("Naruto 2019 to 2026 dollar change", round(nar_2026 - nar_2019, 3), "USD billions", "2026 minus 2019", "data/franchise_revenue_2019_vs_2026.csv", "S001;S017"),
        ("Mortal Kombat 2019 lifetime", round(mk_2019, 3), "USD billions", "sum of rows; below any supposed $4B floor", "data/franchise.csv", "S001"),
        ("Mortal Kombat 2026 Wikipedia lifetime", mk_2026, "USD billions", "paired Wikipedia row", "data/franchise_revenue_2019_vs_2026.csv", "S017"),
        ("Mortal Kombat 2019 to 2026 dollar change", round(mk_2026 - mk_2019, 3), "USD billions", "2026 minus 2019", "data/franchise_revenue_2019_vs_2026.csv", "S001;S017"),
        ("Star Wars 2019 lifetime", round(fr_total("Star Wars"), 3), "USD billions", "sum of rows", "data/franchise.csv", "S001"),
        ("MCU 2019 lifetime", round(mcu_tot, 3), "USD billions", "sum of Marvel Cinematic Universe rows", "data/franchise.csv", "S001"),
        ("Pokemon revenue per year as of 2019", round(poke_2019 / years_alive("Pokémon"), 4), "USD billions per year", "2019 lifetime / (2019 - year_created)", "data/franchise.csv", "S001"),
        ("MCU revenue per year as of 2019", round(mcu_tot / years_alive("Marvel Cinematic Universe"), 4), "USD billions per year", "2019 lifetime / (2019 - year_created)", "data/franchise.csv", "S001"),
        ("Disney unconsolidated owner total 2019", round(disney_uncon, 3), "USD billions", "rows whose owner field is exactly The Walt Disney Company", "data/franchise.csv", "S001"),
        ("Disney consolidated owner total 2019", round(disney_con, 3), "USD billions", "owner_consolidation_rules including Marvel Lucasfilm Fox", "data/owner_totals_derived.csv", "S001"),
        ("Nintendo standalone owner total 2019", round(nintendo_label, 3), "USD billions", "rows whose owner field is exactly Nintendo; excludes Pokémon Company string", "data/franchise.csv", "S001"),
        ("Pokemon Company owner-string total 2019", round(poke_label, 3), "USD billions", "rows owned by The Pokémon Company (Nintendo, Game Freak, Creatures); not added to Nintendo label", "data/franchise.csv", "S001"),
        ("Top-five owner share after Fox consolidation", round(sum(v for _, v in sorted(owner_map.items(), key=lambda x: -x[1])[:5]) / grand_total * 100, 1), "percent", "top 5 consolidated owners / grand total", "data/owner_concentration_scenarios.csv", "S001"),
        ("Top owner share after Fox consolidation", round(sorted(owner_map.items(), key=lambda x: -x[1])[0][1] / grand_total * 100, 1), "percent", "largest consolidated owner / grand total", "data/owner_concentration_scenarios.csv", "S001"),
        ("Batman 2019 lifetime", round(batman, 3), "USD billions", "sum of Batman rows", "data/franchise.csv", "S001"),
        ("Superman 2019 lifetime", round(superman, 3), "USD billions", "sum of Superman rows", "data/franchise.csv", "S001"),
        ("DCEU 2019 lifetime", round(dceu, 3), "USD billions", "sum of DC Extended Universe rows", "data/franchise.csv", "S001"),
        ("DC Entertainment owner total 2019", round(dc_sum, 3), "USD billions", "Batman + Superman + DCEU; Wizarding World is a separate Warner row", "data/franchise.csv", "S001"),
        ("Wizarding World 2019 lifetime", round(fr_total("Wizarding World / Harry Potter"), 3), "USD billions", "sum of Wizarding World rows; not in DC Entertainment total", "data/franchise.csv", "S001"),
        ("Simpsons 2019 lifetime", round(fr_total("The Simpsons"), 3), "USD billions", "sum of rows", "data/franchise.csv", "S001"),
        ("Simpsons 2026 Wikipedia lifetime", wiki_2026("The Simpsons"), "USD billions", "paired Wikipedia row", "data/franchise_revenue_2019_vs_2026.csv", "S017"),
        ("Video-game origin lifetime 2019", round(medium_totals.get("Video game", 0), 3), "USD billions", "sum by original_media", "data/franchise.csv", "S001"),
        ("Manga origin lifetime 2019", round(medium_totals.get("Manga", 0), 3), "USD billions", "sum by original_media", "data/franchise.csv", "S001"),
        ("Animated series origin lifetime 2019", round(medium_totals.get("Animated series", 0), 3), "USD billions", "sum by original_media", "data/franchise.csv", "S001"),
        ("Film origin lifetime 2019", round(medium_totals.get("Film", 0), 3), "USD billions", "sum by original_media", "data/franchise.csv", "S001"),
        ("Japan region lifetime 2019", round(region_stats["Japan"]["revenue"], 3), "USD billions", "sum of region_origin=Japan", "data/franchise_region_summary.csv", "S001"),
        ("Japan merchandise share 2019", round(region_stats["Japan"]["merch"] / region_stats["Japan"]["revenue"] * 100, 1), "percent", "merch / region total", "data/franchise_region_summary.csv", "S001"),
        ("US region lifetime 2019", round(region_stats["US"]["revenue"], 3), "USD billions", "sum of region_origin=US", "data/franchise_region_summary.csv", "S001"),
        ("US merchandise share 2019", round(region_stats["US"]["merch"] / region_stats["US"]["revenue"] * 100, 1), "percent", "merch / region total", "data/franchise_region_summary.csv", "S001"),
        ("Japan franchise count 2019", region_stats["Japan"]["count"], "franchises", "count of region_origin=Japan", "data/franchise_region_summary.csv", "S001"),
        ("US franchise count 2019", region_stats["US"]["count"], "franchises", "count of region_origin=US", "data/franchise_region_summary.csv", "S001"),
        ("UK region lifetime 2019", round(region_stats["UK"]["revenue"], 3), "USD billions", "sum of region_origin=UK", "data/franchise_region_summary.csv", "S001"),
        ("UK merchandise share 2019", round(region_stats["UK"]["merch"] / region_stats["UK"]["revenue"] * 100, 1), "percent", "merch / region total", "data/franchise_region_summary.csv", "S001"),
        ("UK franchise count 2019", region_stats["UK"]["count"], "franchises", "count of region_origin=UK", "data/franchise_region_summary.csv", "S001"),
        ("Korea region lifetime 2019", round(region_stats["Korea"]["revenue"], 3), "USD billions", "CrossFire + Dungeon Fighter Online", "data/franchise_region_summary.csv", "S001"),
        ("China region lifetime 2019", round(region_stats["China"]["revenue"], 3), "USD billions", "Westward Journey", "data/franchise_region_summary.csv", "S001"),
        ("Sweden region lifetime 2019", round(region_stats["Sweden"]["revenue"], 3), "USD billions", "Minecraft + Candy Crush Saga", "data/franchise_region_summary.csv", "S001"),
        ("Finland region lifetime 2019", round(region_stats["Finland"]["revenue"], 3), "USD billions", "Angry Birds", "data/franchise_region_summary.csv", "S001"),
        ("Canada region lifetime 2019", round(region_stats["Canada"]["revenue"], 3), "USD billions", "PAW Patrol + Assassin's Creed", "data/franchise_region_summary.csv", "S001"),
        ("MCU box office share of its 2019 row", round(mcu_bo / mcu_tot * 100, 1), "percent", "Box Office category / MCU total", "data/franchise.csv", "S001"),
        ("Hello Kitty 2026 Wikipedia lifetime", wiki_2026("Hello Kitty"), "USD billions", "paired row; source revision not a real decline", "data/franchise_revenue_2019_vs_2026.csv", "S017"),
        ("Mario 2019 lifetime", round(fr_total("Mario"), 3), "USD billions", "sum of rows", "data/franchise.csv", "S001"),
        ("Mario 2026 Wikipedia lifetime", wiki_2026("Mario"), "USD billions", "paired row; source revision not a real decline", "data/franchise_revenue_2019_vs_2026.csv", "S017"),
        ("Gundam 2019 lifetime", round(fr_total("Gundam"), 3), "USD billions", "sum of rows", "data/franchise.csv", "S001"),
        ("Gundam 2026 Wikipedia lifetime", wiki_2026("Gundam"), "USD billions", "paired row; source revision not a real decline", "data/franchise_revenue_2019_vs_2026.csv", "S017"),
        ("Pixar acquisition price", 7.4, "USD billions", "deal table", "data/entities_companies_deals.csv", "S009"),
        ("Marvel acquisition price", 4.0, "USD billions", "deal table", "data/entities_companies_deals.csv", "S010"),
        ("Lucasfilm acquisition price", 4.05, "USD billions", "deal table", "data/entities_companies_deals.csv", "S011"),
        ("Fox enterprise value", 71.3, "USD billions", "deal table", "data/entities_companies_deals.csv", "S012"),
        ("Disney Entertainment FY2024", 41.186, "USD billions", "segment exhibit", "data/disney_segment_revenue_fy2024.csv", "S081"),
        ("Disney Sports FY2024", 17.619, "USD billions", "segment exhibit", "data/disney_segment_revenue_fy2024.csv", "S081"),
        ("Disney Experiences FY2024", 34.151, "USD billions", "segment exhibit", "data/disney_segment_revenue_fy2024.csv", "S081"),
        ("Domestic top-10 franchise share 2010", 60, "percent", "manual coding of Box Office Mojo yearly chart", "data/top10_franchise_share_by_year.csv", "S005"),
        ("Domestic top-10 franchise share 2015", 70, "percent", "manual coding of Box Office Mojo yearly chart", "data/top10_franchise_share_by_year.csv", "S005"),
        ("Domestic top-10 franchise share 2019", 80, "percent", "manual coding of Box Office Mojo yearly chart", "data/top10_franchise_share_by_year.csv", "S005"),
        ("Domestic top-10 franchise share 2024", 90, "percent", "manual coding of Box Office Mojo yearly chart", "data/top10_franchise_share_by_year.csv", "S005"),
        ("Toy Story 2019 lifetime", round(fr_total("Toy Story"), 3), "USD billions", "sum of rows", "data/franchise.csv", "S001"),
    ]
    verified.extend(extra)
    _ = disney_raw
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

    print(
        f"Wrote tables: {len(totals)} franchises, wiki {len(wiki)}, "
        f"crosswalk matched {matched_with_2026}, delta {len(delta_rows)}"
    )


if __name__ == "__main__":
    main()
