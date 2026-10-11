#!/usr/bin/env python3
"""Split narration into phrase-level storyboard rows for franchise video scripts."""
import csv
import re
import sys
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent
COLUMNS = [
    "scene_id",
    "narration_words",
    "visual_type",
    "red_box_target",
    "count_up_number",
    "asset_id",
    "asset_file",
    "image_credit",
]


def split_phrases(text: str) -> list[str]:
    text = re.sub(r"\s+", " ", text.strip())
    # Split on sentence boundaries and em-dashes; keep clauses short for ~1 phrase per scene
    parts: list[str] = []
    for chunk in re.split(r"(?<=[.!?])\s+|(?<=—)\s*", text):
        chunk = chunk.strip()
        if not chunk:
            continue
        # Further split long sentences on commas/semicolons when needed
        if len(chunk.split()) > 14 and ("," in chunk or ";" in chunk):
            subs = re.split(r"(?<=[,;])\s+", chunk)
            for s in subs:
                s = s.strip()
                if s:
                    parts.append(s)
        else:
            parts.append(chunk)
    return parts


def default_visual(phrase: str, prefix: str, idx: int) -> tuple[str, str, str, str]:
    """Return visual_type, red_box, count_up, credit."""
    low = phrase.lower()
    credit = "Artometrics / franchise dataset (S001)" if "percent" in low or "$" in phrase or "billion" in low else ""

    # Chart beats
    chart_map = {
        "fifty-six": ("chart beat", "chart6_revenue_streams", "56", credit),
        "merchandise is fifty-six": ("chart beat", "chart6_revenue_streams", "56.0", credit),
        "chart six": ("chart beat", "chart6_revenue_streams", "", "Data: franchise.csv (S001)"),
        "top twenty": ("chart beat", "chart1_top20_revenue", "", credit),
        "two thousand nineteen": ("chart beat", "chart10_wiki_2019_vs_2026", "", "S001; S017"),
        "wikipedia": ("chart beat", "chart10_wiki_2019_vs_2026", "", "S017"),
        "japan": ("chart beat", "chart15_region_japan_us_other", "", "S001"),
        "hollywood": ("chart beat", "chart15_region_japan_us_other", "", "S001"),
        "disney": ("official logo", "The Walt Disney Company", "", "https://commons.wikimedia.org/wiki/File:The_Walt_Disney_Company_logo.svg"),
        "marvel": ("official logo", "Marvel Entertainment", "", "SEC filing (S010)"),
        "nintendo": ("official logo", "Nintendo", "", "https://commons.wikimedia.org/wiki/File:Nintendo.svg"),
        "pokémon": ("official logo", "Pokémon", "", "The Pokémon Company (fair use logo)"),
        "pokemon": ("official logo", "Pokémon", "", "The Pokémon Company (fair use logo)"),
        "box office mojo": ("chart beat", "chart7_top10_franchise_share", "", "Box Office Mojo yearly charts"),
        "nine of ten": ("chart beat", "chart7_top10_franchise_share", "90", credit),
        "ten-k": ("chart beat", "chart9_disney_segments_fy2024", "", "S004; S081"),
        "four hundred twenty-six": ("big number", "Disney consolidated franchise rows", "426.2", "owner_totals_derived.csv (S001)"),
        "ninety point nine": ("big number", "Pokémon lifetime revenue", "90.9", "verified_numbers.csv (S001)"),
        "licensing": ("AI illustration", "stick-figure executives at licensing table with contract and SKU icons", "", "Artometrics AI prompt — no real people"),
        "toy aisle": ("AI illustration", "anime-style retail aisle with generic plush silhouettes and price tags", "", "Artometrics AI prompt — no copyrighted characters"),
        "production committee": ("AI illustration", "anime-style meeting table with publisher broadcaster toy company icons", "", "Steinberg (2012) context; Artometrics AI"),
        "theme park": ("AI illustration", "stylised castle turnstile and merchandise cart silhouettes", "", "Artometrics AI prompt"),
    }
    for key, val in chart_map.items():
        if key in low:
            return val

    if re.search(r"\d+(\.\d+)?\s*(percent|billion|million)", low) or re.search(r"\$[\d.]+", phrase):
        num = re.search(r"([\d.]+\s*(?:percent|point \w+|billion|million)|\$[\d.]+[BM]?)", phrase, re.I)
        return ("big number", phrase[:60], num.group(1) if num else "", credit or "verified_numbers.csv")

    if idx == 0:
        return ("title card", prefix.upper(), "", "Artometrics")

    return ("AI illustration", f"minimal mechanism scene: {phrase[:80]}", "", "Artometrics AI prompt — no real people or IP characters")


def write_storyboard(slug: str, narration: str, min_scenes: int) -> int:
    phrases = split_phrases(narration)
    # Pad by splitting longest phrases if under minimum
    while len(phrases) < min_scenes:
        longest_i = max(range(len(phrases)), key=lambda i: len(phrases[i]))
        p = phrases[longest_i]
        words = p.split()
        if len(words) < 4:
            break
        mid = len(words) // 2
        phrases[longest_i : longest_i + 1] = [
            " ".join(words[:mid]),
            " ".join(words[mid:]),
        ]

    path = OUT_DIR / f"storyboard-{slug}.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        for i, phrase in enumerate(phrases, start=1):
            vis, red, count, cred = default_visual(phrase, slug, i)
            w.writerow(
                {
                    "scene_id": f"{slug[0]}{i:03d}",
                    "narration_words": phrase,
                    "visual_type": vis,
                    "red_box_target": red,
                    "count_up_number": count,
                    "asset_id": "",
                    "asset_file": "",
                    "image_credit": cred,
                }
            )
    return len(phrases)


def main() -> None:
    scripts = {
        "short": (OUT_DIR / "script-short.md", 90),
        "deepdive": (OUT_DIR / "script-deepdive.md", 150),
        "vertical": (OUT_DIR / "script-vertical.md", 22),
    }
    for slug, (path, min_scenes) in scripts.items():
        text = path.read_text(encoding="utf-8")
        # Strip markdown headings and metadata lines
        lines = [
            ln
            for ln in text.splitlines()
            if ln.strip() and not ln.startswith("#") and not ln.startswith("##")
        ]
        narration = " ".join(lines)
        n = write_storyboard(slug, narration, min_scenes)
        print(f"{slug}: {n} scenes -> storyboard-{slug}.csv")


if __name__ == "__main__":
    main()
