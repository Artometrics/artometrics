from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

from .clip_tags import text_image_similarity
from .paths import image_id_from_storage_path


@dataclass
class ChecklistItem:
    item_id: str
    title: str
    posted: bool


def parse_checklist(path: Path) -> list[ChecklistItem]:
    items: list[ChecklistItem] = []
    for i, line in enumerate(path.read_text().splitlines()):
        m = re.match(r"^- \[(x| )\] (.+)$", line.strip(), re.I)
        if not m:
            continue
        posted = m.group(1).lower() == "x"
        title = m.group(2).strip()
        slug = re.sub(r"[^a-z0-9]+", "_", title.lower()).strip("_")[:80]
        items.append(ChecklistItem(item_id=f"item_{i:03d}_{slug}", title=title, posted=posted))
    return items


def load_catalog_index(catalog_path: Path) -> dict[str, dict]:
    """Map image_id -> catalog text fields."""
    if not catalog_path.is_file():
        return {}
    data = json.loads(catalog_path.read_text())
    index: dict[str, dict] = {}
    for look in data.get("instagram_looks", []):
        caption = look.get("caption") or ""
        client = look.get("client_name") or look.get("client") or ""
        event = look.get("event_or_project") or look.get("look_type") or ""
        date = look.get("posted_at") or look.get("date") or ""
        text = " ".join(filter(None, [client, event, caption])).lower()
        for asset in look.get("media", []):
            sp = asset.get("storage_path")
            if not sp:
                continue
            try:
                iid = image_id_from_storage_path(sp)
            except ValueError:
                continue
            index[iid] = {
                "caption": caption,
                "client": client,
                "event": event,
                "date": str(date),
                "text": text,
            }
    return index


def _token_overlap(query: str, text: str) -> float:
    q = {w for w in re.findall(r"[a-z0-9]+", query.lower()) if len(w) > 2}
    t = {w for w in re.findall(r"[a-z0-9]+", text.lower()) if len(w) > 2}
    if not q:
        return 0.0
    return len(q & t) / len(q)


def match_checklist_item(
    item: ChecklistItem,
    signals: dict[str, dict],
    catalog_index: dict[str, dict],
    top_n: int = 12,
) -> dict:
    if item.posted:
        return {
            "item_title": item.title,
            "candidates": [],
            "confidence": "skipped_posted",
        }
    q = item.title.lower()
    candidates = []
    for image_id, sig in signals.items():
        reasons: list[str] = []
        score = 0.0
        cat = catalog_index.get(image_id, {})
        if cat.get("text"):
            ov = _token_overlap(q, cat["text"])
            if ov > 0.15:
                score += ov * 0.45
                reasons.append(f"catalog_overlap:{ov:.2f}")
        tags = [t.lower() for t in sig.get("tags", [])]
        for tag in tags:
            if tag in q or any(w in q for w in tag.split()):
                score += 0.08
                reasons.append(f"tag:{tag}")
        cap = (sig.get("caption") or "").lower()
        if cap:
            ov = _token_overlap(q, cap)
            if ov > 0.2:
                score += ov * 0.25
                reasons.append(f"caption_overlap:{ov:.2f}")
        emb = sig.get("_clip_embedding")
        if emb is not None:
            clip_s = text_image_similarity(item.title, emb)
            if clip_s > 0.2:
                score += clip_s * 0.35
                reasons.append(f"clip:{clip_s:.2f}")
        if score > 0.12:
            candidates.append(
                {
                    "imageId": image_id,
                    "score": round(score, 4),
                    "reasons": reasons,
                }
            )
    candidates.sort(key=lambda c: c["score"], reverse=True)
    candidates = candidates[:top_n]
    if not candidates:
        conf = "none"
    elif candidates[0]["score"] >= 0.55:
        conf = "high"
    elif candidates[0]["score"] >= 0.35:
        conf = "medium"
    else:
        conf = "low"
    return {
        "item_title": item.title,
        "candidates": candidates,
        "confidence": conf,
    }
