#!/usr/bin/env python3
"""Re-map franchise storyboards to Anime-style visual mix (pipeline cards, charts, assets, citations, capped AI)."""
from __future__ import annotations

import csv
import re
import shutil
from collections import defaultdict
from pathlib import Path

import sys

if str(Path(__file__).resolve().parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_phase4a_assets import (
    AI_PROMPTS,
    ASSETS_DIR,
    CHARTS_SRC,
    ENTITY_TO_ASSET,
    STORYBOARD_COLS,
    VIDEO_DIR,
    detect_entities,
    fetch_wiki_assets,
    pick_ai_prompt,
)
from build_phase4a_assets import WIKI_ASSETS as BASE_WIKI_ASSETS

REPO_ROOT = VIDEO_DIR.resolve().parents[2]
CHARTS_HTML_SRC = REPO_ROOT / "articles/franchise/charts"
PUBLIC_SONY = REPO_ROOT / "public/images/content/articles/franchise/assets/logo_sony_pictures.svg"

EXTENDED_WIKI_ASSETS: list[dict] = [
    {
        "asset_id": "logo_nexon",
        "entity": "Nexon",
        "wiki": "Nexon.svg",
        "type": "logo",
        "license": "Wikimedia Commons — fair use editorial (corporate logo)",
        "credit_line": "Nexon logo, Wikimedia Commons",
    },
    {
        "asset_id": "logo_tencent",
        "entity": "Tencent",
        "wiki": "Tencent Logo.svg",
        "type": "logo",
        "license": "Wikimedia Commons — fair use editorial (corporate logo)",
        "credit_line": "Tencent logo, Wikimedia Commons",
    },
    {
        "asset_id": "logo_game_freak",
        "entity": "Game Freak",
        "wiki": "GAME FREAK logo.svg",
        "type": "logo",
        "license": "Wikimedia Commons — fair use editorial (corporate logo)",
        "credit_line": "Game Freak logo, Wikimedia Commons",
    },
    {
        "asset_id": "logo_creatures",
        "entity": "Creatures Inc.",
        "wiki": "Creatures Inc..png",
        "type": "logo",
        "license": "Wikimedia Commons — fair use editorial (corporate logo)",
        "credit_line": "Creatures Inc. logo, Wikimedia Commons",
    },
    {
        "asset_id": "logo_sony",
        "entity": "Sony",
        "wiki": "Sony Pictures logo.svg",
        "type": "logo",
        "license": "Wikimedia Commons — Public domain (PD-textlogo)",
        "credit_line": "Sony Pictures logo, Wikimedia Commons",
    },
    {
        "asset_id": "logo_lego",
        "entity": "LEGO",
        "wiki": "LEGO logo.svg",
        "type": "logo",
        "license": "Wikimedia Commons — Public domain (PD-textlogo)",
        "credit_line": "LEGO logo, Wikimedia Commons",
    },
    {
        "asset_id": "logo_peanuts",
        "entity": "Peanuts",
        "wiki": "Peanuts logo.svg",
        "type": "logo",
        "license": "Wikimedia Commons — fair use editorial (text logo)",
        "credit_line": "Peanuts logo, Wikimedia Commons",
    },
    {
        "asset_id": "logo_toy_story",
        "entity": "Toy Story",
        "wiki": "Toy Story logo.svg",
        "type": "logo",
        "license": "Wikimedia Commons — fair use editorial (text logo)",
        "credit_line": "Toy Story logo, Wikimedia Commons",
    },
    {
        "asset_id": "logo_lotr",
        "entity": "Middle-earth / Lord of the Rings",
        "wiki": "The Lord of the Rings logo.svg",
        "type": "logo",
        "license": "Wikimedia Commons — fair use editorial (text logo)",
        "credit_line": "The Lord of the Rings logo, Wikimedia Commons",
    },
    {
        "asset_id": "logo_one_piece",
        "entity": "One Piece",
        "wiki": "One piece logo.svg",
        "type": "logo",
        "license": "Wikimedia Commons — fair use editorial (text logo)",
        "credit_line": "One Piece logo, Wikimedia Commons",
    },
    {
        "asset_id": "logo_dragon_ball",
        "entity": "Dragon Ball",
        "wiki": "Dragon Ball Z logo.svg",
        "type": "logo",
        "license": "Wikimedia Commons — fair use editorial (text logo)",
        "credit_line": "Dragon Ball logo, Wikimedia Commons",
    },
    {
        "asset_id": "logo_fast_furious",
        "entity": "Fast & Furious",
        "wiki": "Wild Speed logo.svg",
        "type": "logo",
        "license": "Wikimedia Commons — fair use editorial (text logo)",
        "credit_line": "Fast & Furious logo, Wikimedia Commons",
    },
]

ENTITY_TO_ASSET.update(
    {
        "Game Freak": "logo_game_freak",
        "Creatures Inc.": "logo_creatures",
        "Nexon": "logo_nexon",
        "Tencent": "logo_tencent",
        "Sony": "logo_sony",
        "LEGO": "logo_lego",
        "Peanuts": "logo_peanuts",
        "Toy Story": "logo_toy_story",
        "Middle-earth / Lord of the Rings": "logo_lotr",
        "One Piece": "logo_one_piece",
        "Dragon Ball": "logo_dragon_ball",
        "Fast & Furious": "logo_fast_furious",
        "Dungeon Fighter Online": "logo_dnf",
        "CrossFire": "logo_smilegate",
    }
)

# Patch duplicate / wrong mapping from phase 4a
ENTITY_TO_ASSET["Marc Steinberg"] = "logo_uminn_press"
ENTITY_TO_ASSET.pop("book_steinberg_media_mix", None)

TRUE_MECH_MARKERS = (
    "stick-figure executives at licensing",
    "anime-style meeting table",
    "anime-style retail aisle",
    "stylised castle turnstile",
    "mechanism diagram",
    "production-committee table",
    "partnership diagram",
    "owner consolidation flowchart",
    "uk origin map pins",
    "m&a cheque mechanism",
    "franchise slate failure",
    "selective mario licensing",
    "mobile versus fighting-game correction",
    "coverage gap:",
    "japan media-mix vs hollywood",
    "hollywood vertical stack",
)

CHART_NAMES = [
    "chart1_top20_revenue",
    "chart2_revenue_per_year",
    "chart3a_disney_non_consolidated",
    "chart3b_disney_consolidated",
    "chart5_original_media_revenue",
    "chart6_revenue_streams",
    "chart7_top10_franchise_share",
    "chart8_disney_acquisitions",
    "chart9_disney_segments_fy2024",
    "chart10_wiki_2019_vs_2026",
    "chart11_mix_by_original_medium",
    "chart12_owner_concentration",
    "chart13_deal_price_vs_revenue",
    "chart14_box_office_share_top20",
    "chart15_region_japan_us_other",
]

CITATION_RULES: list[tuple[re.Pattern[str], str, str]] = [
    (re.compile(r"wikipedia|twenty-twenty-six list|2026 list|editor.?maintained", re.I), "S017", "Wikipedia list of highest-grossing media franchises (2026 scrape)"),
    (re.compile(r"box office mojo|domestic top.?ten|top.?ten films", re.I), "S005", "Box Office Mojo domestic yearly charts (manual franchise coding)"),
    (re.compile(r"ten-?k|segment revenue|experiences segment|entertainment segment", re.I), "S081", "Disney Form 10-K FY2024 segment exhibit"),
    (re.compile(r"marvel.*2009|four billion.*marvel", re.I), "S010", "Disney–Marvel 8-K exhibit 99.1 (≈$4B, 31 Aug 2009)"),
    (re.compile(r"lucasfilm|four point zero five", re.I), "S011", "Disney–Lucasfilm 8-K exhibit 99.1 ($4.05B, Oct 2012)"),
    (re.compile(r"twenty-first century fox|seventy-one point three.*fox|71\.3.*fox", re.I), "S012", "Disney–Fox amended agreement exhibit ($71.3B, Jun 2018)"),
    (re.compile(r"steinberg|production committee", re.I), "S003", "Marc Steinberg, Anime's Media Mix (2012) — production committees"),
    (re.compile(r"crosswalk|hand-mapped|paired row", re.I), "S017", "franchise_crosswalk_2019_2026.csv (103 rows, 82 paired)"),
    (re.compile(r"verified_numbers|owner_totals|franchise\.csv", re.I), "S001", "TidyTuesday 2019-07-02 franchise.csv (verified_numbers rebuild)"),
    (re.compile(r"mid-2019|public photograph|not audited|one ledger", re.I), "S001", "TidyTuesday / Wikipedia mid-2019 franchise scrape (S001)"),
    (re.compile(r"pixar.*7\.4|seven point four.*pixar", re.I), "S009", "Disney–Pixar acquisition 8-K (2006)"),
]

NUMERIC_RE = re.compile(
    r"(\d+(\.\d+)?)\s*(billion|trillion|percent|million)|"
    r"(one point five|one point five two|ninety point nine|one hundred thirty point seven|"
    r"four hundred twenty-six|thirty-nine point eight|forty-nine|fifty-six|twenty|eight point nine|"
    r"one hundred and three|sixty-eight|forty-six point four|twenty-eight percent)",
    re.I,
)


def version_slug(scene_id: str) -> str:
    if scene_id.startswith("s"):
        return "short"
    if scene_id.startswith("d"):
        return "deepdive"
    return "vertical"


def ai_cap_for_version(slug: str, n_scenes: int) -> int:
    return max(1, int(round(n_scenes * 0.20)))


NARR_MECH_MARKERS = (
    "production committee",
    "publishers, broadcasters, and toy",
    "premiere is often the advert",
    "repeat sale is the business",
    "parks and shops",
    "attach a park",
    "media-mix",
    "double-count",
    "partner's revenue",
    "library outright",
    "dark universe",
    "not a guarantee",
    "coverage gap",
    "selective licensing",
    "burbank sells the toys",
    "cheque beside",
    "price the rights",
    "carrying capacity",
    "which stream pays",
    "poster for the product",
    "turnstile",
    "toy aisle",
    "licensing table",
)


def mechanism_score(row: dict) -> int:
    red = row["red_box_target"]
    narr = row["narration_words"]
    if is_true_mechanism(red, narr):
        return 100 + len(narr.split())
    if "minimal mechanism scene" not in red.lower():
        return 0
    pid = pick_ai_prompt(row)
    if pid != "ai25":
        return 20 + len(narr.split())
    return 3


def is_true_mechanism(red_box: str, narration: str) -> bool:
    if any(m in red_box.lower() for m in TRUE_MECH_MARKERS):
        return True
    if "minimal mechanism scene" in red_box.lower():
        narr = narration.lower()
        return any(m in narr for m in NARR_MECH_MARKERS)
    blob = f"{red_box} {narration}".lower()
    return any(m in blob for m in TRUE_MECH_MARKERS + NARR_MECH_MARKERS)


def citation_for_scene(narration: str, red_box: str) -> tuple[str, str] | None:
    blob = f"{narration} {red_box}"
    for pat, sid, label in CITATION_RULES:
        if pat.search(blob):
            return sid, label
    return None


def chart_for_scene(narration: str, red_box: str, existing: str) -> str | None:
    if existing in CHART_NAMES:
        return existing
    low = f"{narration} {red_box}".lower()
    if any(k in low for k in ("wiki", "2026 list", "twenty-twenty-six", "revised", "editor")):
        return "chart10_wiki_2019_vs_2026"
    if "fifty-six" in low or ("merchandise" in low and "percent" in low and "fifty" in low):
        return "chart6_revenue_streams"
    if "forty-two japan" in low or ("japan" in low and "681" in low):
        return "chart15_region_japan_us_other"
    if "japan" in low and ("pattern" in low or "production committee" in low):
        return "chart15_region_japan_us_other"
    if "hollywood" in low and ("park" in low or "buying" in low or "attach" in low):
        return "chart15_region_japan_us_other"
    if "nine of ten" in low or ("ninety percent" in low and "2024" in low):
        return "chart7_top10_franchise_share"
    if "ten-k" in low or ("segment" in low and "experiences" in low):
        return "chart9_disney_segments_fy2024"
    if "top twenty" in low or "tops the table" in low:
        return "chart1_top20_revenue"
    if "fold" in low and ("426" in low or "four hundred twenty-six" in low):
        return "chart3b_disney_consolidated"
    if "video games sum" in low or "manga origins" in low or "original medium" in low:
        return "chart11_mix_by_original_medium"
    if "forty-six point four" in low or "owner concentration" in low:
        return "chart12_owner_concentration"
    if "marvel cost four" in low or "cheque" in low and "billion" in low:
        return "chart13_deal_price_vs_revenue"
    if "sixty-eight percent" in low and "marvel" in low:
        return "chart14_box_office_share_top20"
    if "pixar cost" in low or "acquisition" in low and "deal" in low:
        return "chart8_disney_acquisitions"
    return None


def big_number_fields(narration: str, red_box: str, count_up: str) -> tuple[str, str] | None:
    if count_up:
        label = red_box if red_box and "minimal" not in red_box.lower() else narration[:72]
        return label, count_up
    if NUMERIC_RE.search(narration) and not chart_for_scene(narration, red_box, ""):
        m = NUMERIC_RE.search(narration)
        if m:
            return (red_box or narration)[:72], m.group(0)
    return None


def copy_chart_html_assets() -> None:
    out = ASSETS_DIR / "charts"
    out.mkdir(parents=True, exist_ok=True)
    for name in CHART_NAMES:
        src = CHARTS_HTML_SRC / f"{name}.html"
        if not src.exists():
            continue
        shutil.copy2(src, out / f"chart_{name}.html")


def load_asset_meta() -> dict[str, dict]:
    import build_phase4a_assets as b

    have = {x["asset_id"] for x in b.WIKI_ASSETS}
    for spec in EXTENDED_WIKI_ASSETS:
        if spec["asset_id"] not in have:
            b.WIKI_ASSETS.append(spec)
    meta = fetch_wiki_assets()
    # chart HTML (motion) entries — pipeline renders, no raster file required
    for name in CHART_NAMES:
        aid = f"chart_{name}"
        meta[aid] = {
            "asset_id": aid,
            "entity": name,
            "type": "chart",
            "file": f"assets/charts/chart_{name}.html",
            "source_url": f"https://artometrics.com/images/content/articles/franchise/charts/{name}.html",
            "license": "Artometrics / franchise dataset (S001)",
            "credit_line": f"Motion chart HTML — {name}",
            "notes": "Rendered by video pipeline from Plotly motion export",
        }
    return meta


def visual_type_for_asset(meta: dict) -> str:
    t = meta.get("type", "logo")
    if t == "chart":
        return "chart beat"
    if t in ("logo", "poster", "official still", "product shot"):
        return t
    return "logo"


def remap_storyboards(asset_meta: dict[str, dict]) -> dict[str, dict[str, int]]:
    rows_by_file: dict[Path, list[dict]] = {}
    all_rows: list[dict] = []

    for fp in sorted(VIDEO_DIR.glob("storyboard-*.csv")):
        rows_by_file[fp] = list(csv.DictReader(fp.open(encoding="utf-8")))
        all_rows.extend(rows_by_file[fp])

    mech_candidates: list[tuple[int, str, dict]] = []
    staged: dict[str, dict] = {}

    for fp, rows in rows_by_file.items():
        for row in rows:
            sid = row["scene_id"]
            narr = row["narration_words"]
            red = row["red_box_target"]
            count = row.get("count_up_number", "")
            blob = f"{narr} {red}"

            out = {
                "scene_id": sid,
                "narration_words": narr,
                "visual_type": row["visual_type"],
                "red_box_target": red,
                "count_up_number": count,
                "asset_id": "",
                "asset_file": "",
                "image_credit": "",
            }

            chart = chart_for_scene(narr, red, red if red in CHART_NAMES else "")
            if chart or row["visual_type"] == "chart beat":
                cname = chart or red
                aid = f"chart_{cname}"
                out["visual_type"] = "chart beat"
                out["red_box_target"] = cname
                out["asset_id"] = aid
                out["asset_file"] = asset_meta[aid]["file"]
                out["image_credit"] = asset_meta[aid]["credit_line"]
                staged[sid] = out
                continue

            bignum = big_number_fields(narr, red, count)
            if bignum or row["visual_type"] == "big number":
                label, num = bignum or (red, count)
                out["visual_type"] = "big-number card"
                out["red_box_target"] = label
                out["count_up_number"] = num
                out["image_credit"] = "Artometrics big-number card (pipeline)"
                staged[sid] = out
                continue

            ents = detect_entities(blob)
            score = mechanism_score(row)
            if score and not ents:
                mech_candidates.append((score, sid, row))
                staged[sid] = out
                continue

            cite = citation_for_scene(narr, red)
            if cite and not ents:
                sid_src, label = cite
                out["visual_type"] = "type card"
                out["red_box_target"] = label
                out["asset_id"] = f"cite_{sid_src}"
                out["image_credit"] = f"Source {sid_src} — {label}"
                staged[sid] = out
                continue

            if ents:
                ent = ents[0]
                aid = ENTITY_TO_ASSET.get(ent)
                if aid and aid in asset_meta:
                    meta = asset_meta[aid]
                    out["visual_type"] = visual_type_for_asset(meta)
                    out["red_box_target"] = ent
                    out["asset_id"] = aid
                    out["asset_file"] = meta["file"]
                    out["image_credit"] = meta["credit_line"]
                    staged[sid] = out
                    continue

            cite = citation_for_scene(narr, red)
            if cite:
                sid_src, label = cite
                out["visual_type"] = "type card"
                out["red_box_target"] = label
                out["asset_id"] = f"cite_{sid_src}"
                out["image_credit"] = f"Source {sid_src} — {label}"
            else:
                out["visual_type"] = "type card"
                out["red_box_target"] = "TidyTuesday franchise ledger (S001)"
                out["asset_id"] = "cite_S001"
                out["image_credit"] = "Source S001 — TidyTuesday 2019-07-02 media franchise file"
            staged[sid] = out

    # Assign AI to true mechanism scenes up to 20% per version
    caps = defaultdict(int)
    counts_scenes = defaultdict(int)
    for row in all_rows:
        counts_scenes[version_slug(row["scene_id"])] += 1
    for v, n in counts_scenes.items():
        caps[v] = ai_cap_for_version(v, n)

    used_ai: dict[str, int] = defaultdict(int)
    mech_candidates.sort(key=lambda x: -x[0])
    for _score, sid, row in mech_candidates:
        v = version_slug(sid)
        if used_ai[v] >= caps[v]:
            continue
        pid = pick_ai_prompt(row)
        out = staged[sid]
        out["visual_type"] = "AI illustration"
        out["red_box_target"] = row["red_box_target"]
        out["asset_id"] = pid
        out["asset_file"] = ""
        prompt = next(p for i, p in AI_PROMPTS if i == pid)
        out["image_credit"] = f"Artometrics AI — {pid}"
        staged[sid] = out
        used_ai[v] += 1

    for _score, sid, row in mech_candidates:
        out = staged[sid]
        if out["visual_type"] == "AI illustration" and not str(out.get("asset_id", "")).startswith("ai"):
            cite = citation_for_scene(row["narration_words"], row["red_box_target"])
            if cite:
                sid_src, label = cite
                out["visual_type"] = "type card"
                out["red_box_target"] = label
                out["asset_id"] = f"cite_{sid_src}"
                out["image_credit"] = f"Source {sid_src} — {label}"
            else:
                out["visual_type"] = "type card"
                out["red_box_target"] = "TidyTuesday franchise ledger (S001)"
                out["asset_id"] = "cite_S001"
                out["image_credit"] = "Source S001 — TidyTuesday 2019-07-02 media franchise file"
            out["asset_file"] = ""
            staged[sid] = out

    # Write storyboards
    for fp, rows in rows_by_file.items():
        out_rows = [staged[r["scene_id"]] for r in rows]
        with fp.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=STORYBOARD_COLS)
            w.writeheader()
            w.writerows(out_rows)

    # Stats per version
    stats: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for row in staged.values():
        stats[version_slug(row["scene_id"])][row["visual_type"]] += 1

    # Asset log
    scene_ids_by_asset: dict[str, set[str]] = defaultdict(set)
    for row in staged.values():
        aid = row.get("asset_id") or ""
        if aid and row.get("asset_file"):
            scene_ids_by_asset[aid].add(row["scene_id"])
        elif aid.startswith("chart_"):
            scene_ids_by_asset[aid].add(row["scene_id"])

    # Mention-based scene_ids for real assets
    mention_by_asset: dict[str, set[str]] = defaultdict(set)
    for row in staged.values():
        blob = f"{row['narration_words']} {row['red_box_target']}"
        for ent in detect_entities(blob):
            aid = ENTITY_TO_ASSET.get(ent)
            if aid:
                mention_by_asset[aid].add(row["scene_id"])

    log_rows: list[dict] = []
    for aid, meta in sorted(asset_meta.items()):
        if not meta.get("file") and not aid.startswith("chart_"):
            continue
        scenes = mention_by_asset.get(aid) or scene_ids_by_asset.get(aid, set())
        log_rows.append(
            {
                "asset_id": aid,
                "scene_ids": ",".join(sorted(scenes)),
                "entity": meta["entity"],
                "type": meta["type"],
                "file": meta.get("file", ""),
                "source_url": meta.get("source_url", ""),
                "license": meta.get("license", ""),
                "credit_line": meta.get("credit_line", ""),
                "notes": meta.get("notes", ""),
            }
        )

    ai_scenes: dict[str, list[str]] = defaultdict(list)
    for row in staged.values():
        if row["visual_type"] == "AI illustration" and row.get("asset_id", "").startswith("ai"):
            ai_scenes[row["asset_id"]].append(row["scene_id"])

    prompt_map = {i: p for i, p in AI_PROMPTS}
    for pid, scenes in sorted(ai_scenes.items()):
        if pid not in prompt_map:
            continue
        prompt = prompt_map[pid]
        log_rows.append(
            {
                "asset_id": pid,
                "scene_ids": ",".join(sorted(scenes)),
                "entity": "(AI illustration)",
                "type": "AI illustration (prompt only)",
                "file": "",
                "source_url": "",
                "license": "Artometrics house style — generate via gen_ai_images.py",
                "credit_line": "Artometrics AI prompt",
                "notes": prompt[:240],
            }
        )

    log_path = ASSETS_DIR / "asset_log.csv"
    with log_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "asset_id",
                "scene_ids",
                "entity",
                "type",
                "file",
                "source_url",
                "license",
                "credit_line",
                "notes",
            ],
        )
        w.writeheader()
        w.writerows(log_rows)

    ai_path = ASSETS_DIR / "ai_prompts.csv"
    with ai_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["scene_id", "prompt_id", "prompt"])
        w.writeheader()
        for row in sorted(staged.values(), key=lambda r: r["scene_id"]):
            if row["visual_type"] == "AI illustration" and str(row.get("asset_id", "")).startswith("ai"):
                pid = row["asset_id"]
                prompt = next(p for i, p in AI_PROMPTS if i == pid)
                w.writerow({"scene_id": row["scene_id"], "prompt_id": pid, "prompt": prompt})

    with (ASSETS_DIR / "ai_prompt_library.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["prompt_id", "prompt"])
        w.writeheader()
        for pid, prompt in AI_PROMPTS:
            w.writerow({"prompt_id": pid, "prompt": prompt})

    return stats


def main() -> None:
    copy_chart_html_assets()
    asset_meta = load_asset_meta()
    stats = remap_storyboards(asset_meta)

    real_files = len([p for p in ASSETS_DIR.rglob("*") if p.suffix.lower() in (".png", ".jpg", ".html")])
    print(f"Real asset files (png/jpg/html): {real_files}")
    for version in ("short", "deepdive", "vertical"):
        vstats = stats.get(version, {})
        total = sum(vstats.values())
        ai = vstats.get("AI illustration", 0)
        print(f"{version}: {total} scenes — " + ", ".join(f"{k}={v}" for k, v in sorted(vstats.items())))
        if total:
            print(f"  AI share: {ai}/{total} ({100*ai/total:.1f}%)")


if __name__ == "__main__":
    main()
