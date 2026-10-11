#!/usr/bin/env python3
"""Build HTML storyboard decks from franchise storyboard CSVs (Phase 4b)."""
from __future__ import annotations

import csv
import html
import re
import sys
from pathlib import Path

DECK_DIR = Path(__file__).resolve().parent
VIDEO_DIR = DECK_DIR.parent
TPL = DECK_DIR / "templates"

DECKS = {
    "short": {
        "csv": VIDEO_DIR / "storyboard-short.csv",
        "title": "Franchise ledger — short cut",
        "aspect": "16x9",
        "bookend_sub": "Short cut · storyboard deck",
    },
    "deepdive": {
        "csv": VIDEO_DIR / "storyboard-deepdive.csv",
        "title": "Franchise ledger — deep dive",
        "aspect": "16x9",
        "bookend_sub": "Deep dive · storyboard deck",
    },
    "vertical": {
        "csv": VIDEO_DIR / "storyboard-vertical.csv",
        "title": "Franchise ledger — vertical hook",
        "aspect": "9x16",
        "bookend_sub": "Vertical 9:16 · storyboard deck",
    },
}

LOGO_SRC = "../../../../public/images/brand/chomsky-a-white.png"
ASSET_TYPES = {"logo", "poster", "official still", "product shot"}


def load_template(name: str) -> str:
    return (TPL / name).read_text(encoding="utf-8")


def esc(s: str) -> str:
    return html.escape(s or "", quote=True)


def esc_text(s: str) -> str:
    return html.escape(s or "")


def asset_rel(asset_file: str) -> str:
    if not asset_file:
        return ""
    return f"../{asset_file.lstrip('/')}"


def ai_src(prompt_id: str) -> str:
    if not prompt_id:
        return ""
    suffix = "9x16" if False else "16x9"  # per-slide override in vertical builder
    return f"../assets/ai/{prompt_id}_{suffix}.png"


def mechanism_label(red_box: str) -> str:
    s = red_box or ""
    if s.lower().startswith("minimal mechanism scene:"):
        s = s.split(":", 1)[1].strip()
    return s[:200] if s else "Mechanism"


def numeric_highlight_html(narration: str, count_up: str) -> str:
    text = esc_text(narration)
    if count_up:
        pat = re.compile(re.escape(count_up), re.I)
        if pat.search(narration):
            return pat.sub(lambda m: f'<span class="red-box-target">{esc_text(m.group(0))}</span>', text, count=1)
    m = re.search(
        r"\b(\d+(?:\.\d+)?|\d{1,3}(?:,\d{3})+"
        r"|(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
        r"thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|"
        r"thirty|forty|fifty|sixty|seventy|eighty|ninety)(?:\s+point\s+\w+)?"
        r"(?:\s+hundred(?:\s+and\s+\w+)?)?)\b",
        narration,
        re.I,
    )
    if m:
        frag = m.group(1)
        return text.replace(esc_text(frag), f'<span class="red-box-target">{esc_text(frag)}</span>', 1)
    return f'<span class="red-box-target">{text}</span>'


def entity_label_for_row(row: dict) -> str:
    red = (row.get("red_box_target") or "").strip()
    vt = row.get("visual_type") or ""
    if vt in ASSET_TYPES and red:
        return red
    if vt == "big-number card" and red and "minimal" not in red.lower():
        return red.split(".")[0][:80]
    return red[:80] if red else row.get("narration_words", "")[:60]


def render_bookend(scene_id: str, label: str, sub: str, notes: str) -> str:
    tpl = load_template("slide-bookend.html")
    return tpl.format(
        scene_id=esc(scene_id),
        logo_src=LOGO_SRC,
        bookend_label=esc_text(label),
        bookend_sub=esc_text(sub),
        speaker_notes=esc_text(notes),
    )


def render_row(row: dict, aspect: str) -> str:
    scene_id = row["scene_id"]
    vt = row["visual_type"]
    notes = row["narration_words"]
    red = row.get("red_box_target") or ""
    count_up = row.get("count_up_number") or ""
    asset_id = row.get("asset_id") or ""

    if vt == "big-number card":
        tpl = load_template("slide-big-number.html")
        entity = entity_label_for_row(row)
        display = count_up or "—"
        return tpl.format(
            scene_id=esc(scene_id),
            entity_label=esc_text(entity),
            count_up_escaped=esc(count_up),
            count_display=esc_text(display),
            context_line=esc_text(notes),
            speaker_notes=esc_text(notes),
        )

    if vt == "chart beat":
        tpl = load_template("slide-chart.html")
        chart_src = asset_rel(row.get("asset_file") or "")
        beat = count_up or red or "chart beat"
        kicker = red if red.startswith("chart") else (asset_id.replace("chart_", "") if asset_id else "Chart")
        return tpl.format(
            scene_id=esc(scene_id),
            chart_src=esc(chart_src),
            chart_kicker=esc_text(kicker.replace("chart_", "").replace("_", " ")),
            beat_target_escaped=esc(beat),
            count_up_escaped=esc(count_up),
            beat_label=esc_text(str(beat)),
            speaker_notes=esc_text(notes),
        )

    if vt in ASSET_TYPES:
        tpl = load_template("slide-asset.html")
        asset_class = vt.replace(" ", "-")
        return tpl.format(
            scene_id=esc(scene_id),
            visual_type=esc_text(vt),
            asset_class=asset_class,
            entity_label=esc_text(entity_label_for_row(row)),
            entity_escaped=esc(entity_label_for_row(row)),
            asset_src=esc(asset_rel(row.get("asset_file") or "")),
            credit_line=esc_text(row.get("image_credit") or ""),
            speaker_notes=esc_text(notes),
        )

    if vt == "type card":
        tpl = load_template("slide-type-card.html")
        source = row.get("image_credit") or red
        return tpl.format(
            scene_id=esc(scene_id),
            quote_html=numeric_highlight_html(notes, count_up),
            source_line=esc_text(source),
            speaker_notes=esc_text(notes),
        )

    if vt == "AI illustration":
        tpl = load_template("slide-ai.html")
        prompt_id = asset_id if asset_id.startswith("ai") else "ai25"
        suffix = "9x16" if aspect == "9x16" else "16x9"
        src = f"../assets/ai/{prompt_id}_{suffix}.png"
        return tpl.format(
            scene_id=esc(scene_id),
            prompt_id=esc_text(prompt_id),
            ai_src=esc(src),
            mechanism_label=esc_text(mechanism_label(red)),
            speaker_notes=esc_text(notes),
        )

    # Fallback: type card
    tpl = load_template("slide-type-card.html")
    return tpl.format(
        scene_id=esc(scene_id),
        quote_html=f'<span class="red-box-target">{esc_text(notes)}</span>',
        source_line=esc_text(vt),
        speaker_notes=esc_text(notes),
    )


def build_deck(deck_id: str) -> tuple[Path, int]:
    meta = DECKS[deck_id]
    rows = list(csv.DictReader(meta["csv"].open(encoding="utf-8")))
    slides: list[str] = []
    slides.append(
        render_bookend(
            f"{deck_id}-open",
            "Artometrics",
            meta["bookend_sub"],
            "Opening bookend — franchise video storyboard.",
        )
    )
    for row in rows:
        slides.append(render_row(row, meta["aspect"]))
    slides.append(
        render_bookend(
            f"{deck_id}-close",
            "Artometrics",
            meta["bookend_sub"],
            "Closing bookend — franchise video storyboard.",
        )
    )

    shell = load_template("deck-shell.html")
    out_html = shell.format(
        deck_title=esc_text(meta["title"]),
        deck_id=deck_id,
        aspect=meta["aspect"],
        slides="\n".join(slides),
    )
    dest = DECK_DIR / f"deck-{deck_id}.html"
    dest.write_text(out_html, encoding="utf-8")
    return dest, len(slides)


def main() -> int:
    targets = sys.argv[1:] if len(sys.argv) > 1 else list(DECKS.keys())
    for deck_id in targets:
        if deck_id not in DECKS:
            print(f"Unknown deck: {deck_id}", file=sys.stderr)
            return 1
        path, n = build_deck(deck_id)
        print(f"Wrote {path} ({n} slides)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
