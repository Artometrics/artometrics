from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
from tqdm import tqdm

from . import clip_tags, dupes, faces
from .caption import ollama_caption
from .checklist import load_catalog_index, match_checklist_item, parse_checklist
from .config import (
    CAPTION_MAX_IMAGES,
    CATALOG_PATH,
    CHECKLIST_PATH,
    DHASH_MAX_DIST,
    FACE_CLUSTER_EPS,
    FACE_CLUSTER_MIN_SIZE,
    OUT_DIR,
    PHASH_MAX_DIST,
    STATE_PATH,
)
from .contact_sheet import build_face_contact_sheet
from .faces import cluster_embeddings, detect_faces, face_key
from .firestore_io import (
    init_firebase,
    merge_face_cluster,
    merge_image_signals,
    upload_clip_embedding,
    write_checklist_match,
)
from .paths import ImageRef, discover_local_images


def _load_state() -> dict:
    if STATE_PATH.is_file():
        return json.loads(STATE_PATH.read_text())
    return {"processed": {}, "stats": {}}


def _save_state(state: dict) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2))


def _needs_processing(ref: ImageRef, state: dict) -> bool:
    st = ref.local_path.stat()
    prev = state.get("processed", {}).get(ref.image_id)
    if not prev:
        return True
    return prev.get("mtime") != st.st_mtime or prev.get("size") != st.st_size


def run_pipeline(
    limit: int | None = None,
    write_firestore: bool = True,
    skip_caption: bool = False,
) -> dict:
    t0 = time.time()
    refs = discover_local_images()
    if limit:
        refs = refs[:limit]
    state = _load_state()
    todo = [r for r in refs if _needs_processing(r, state)]
    print(f"Images total={len(refs)} incremental_todo={len(todo)}")

    signals: dict[str, dict] = {}
    face_records: list[tuple[str, np.ndarray]] = []
    per_image_faces: dict[str, list[dict]] = {}
    timings: dict[str, list[float]] = {
        "hash": [],
        "faces": [],
        "clip": [],
        "caption": [],
    }

    caption_budget = CAPTION_MAX_IMAGES
    caption_skipped = "disabled"

    for ref in tqdm(todo, desc="per-image"):
        th = time.time()
        ph, dh, qual = dupes.compute_hashes(ref.local_path)
        timings["hash"].append(time.time() - th)

        tf = time.time()
        hits = detect_faces(ref.local_path)
        timings["faces"].append(time.time() - tf)
        face_list = []
        for i, h in enumerate(hits):
            fk = face_key(ref.image_id, i)
            face_records.append((fk, h.embedding))
            face_list.append({"cluster_id": None, "bbox": h.bbox})
        per_image_faces[ref.image_id] = face_list

        tc = time.time()
        tags, tag_scores = clip_tags.zero_shot_tags(ref.local_path)
        emb = clip_tags.encode_image(ref.local_path)
        timings["clip"].append(time.time() - tc)

        caption = None
        if not skip_caption and caption_budget > 0:
            caption = ollama_caption(ref.local_path)
            if caption is None:
                caption_skipped = "ollama_timeout_or_missing_model"
            caption_budget -= 1
        elif skip_caption:
            caption_skipped = "skip_flag"
        timings["caption"].append(0.0)

        signals[ref.image_id] = {
            "phash": ph,
            "dhash": dh,
            "tags": tags,
            "tag_scores": tag_scores,
            "caption": caption,
            "quality": qual,
            "_clip_embedding": emb,
        }

        st = ref.local_path.stat()
        state.setdefault("processed", {})[ref.image_id] = {
            "mtime": st.st_mtime,
            "size": st.st_size,
            "storage_path": ref.storage_path,
        }

    hash_items: list[tuple[ImageRef, str, str, dict]] = []
    for ref in refs:
        if ref.image_id in signals:
            sig = signals[ref.image_id]
            hash_items.append(
                (ref, sig["phash"], sig["dhash"], sig["quality"])
            )
            continue
        prev = state.get("processed", {}).get(ref.image_id) or {}
        if prev.get("phash") and prev.get("dhash"):
            qual = prev.get("quality") or {"score": 1.0}
            hash_items.append((ref, prev["phash"], prev["dhash"], qual))
            signals.setdefault(
                ref.image_id,
                {
                    "phash": prev["phash"],
                    "dhash": prev["dhash"],
                    "tags": prev.get("tags", []),
                    "tag_scores": prev.get("tag_scores", {}),
                    "caption": prev.get("caption"),
                    "quality": qual,
                },
            )
        else:
            ph, dh, qual = dupes.compute_hashes(ref.local_path)
            hash_items.append((ref, ph, dh, qual))

    stack_for_image, best_for_image, stacks = dupes.build_duplicate_stacks(
        hash_items, PHASH_MAX_DIST, DHASH_MAX_DIST
    )

    cluster_map = cluster_embeddings(
        face_records, eps=FACE_CLUSTER_EPS, min_samples=FACE_CLUSTER_MIN_SIZE
    )
    cluster_samples: dict[str, list[tuple[str, Path]]] = {}
    # Faces on incremental todo only; clusters use this run's detections
    for ref in todo:
        fl = per_image_faces.get(ref.image_id) or []
        for i, face in enumerate(fl):
            fk = face_key(ref.image_id, i)
            cid = cluster_map.get(fk)
            if cid is None:
                continue
            cluster_doc_id = f"face_{cid}"
            face["cluster_id"] = cluster_doc_id
            cluster_samples.setdefault(cluster_doc_id, [])
            if len(cluster_samples[cluster_doc_id]) < 6:
                cluster_samples[cluster_doc_id].append((ref.image_id, ref.local_path))

    if write_firestore:
        init_firebase()

    todo_set = set(todo)
    report_uploads = 0
    for ref in tqdm(todo, desc="firestore-upload"):
        sig = signals.get(ref.image_id)
        if not sig:
            continue
        emb = sig.pop("_clip_embedding", None)
        doc = {
            "storage_path": ref.storage_path,
            "phash": sig["phash"],
            "dhash": sig["dhash"],
            "dup_stack_id": stack_for_image.get(ref.image_id),
            "is_best_in_stack": best_for_image.get(ref.image_id, True),
            "tags": sig["tags"],
            "tag_scores": sig["tag_scores"],
            "caption": sig["caption"],
            "faces": per_image_faces.get(ref.image_id, []),
            "quality": sig["quality"],
            "clip_embedding_path": None,
        }
        if emb is not None:
            if write_firestore:
                doc["clip_embedding_path"] = upload_clip_embedding(ref.image_id, emb)
                report_uploads += 1
            else:
                np.save(OUT_DIR / f"clip_{ref.image_id}.npy", emb)

        if write_firestore:
            merge_image_signals(ref.image_id, doc, skip_if_processed=False)
        prev = state["processed"].setdefault(ref.image_id, {})
        prev.update(
            {
                "phash": doc["phash"],
                "dhash": doc["dhash"],
                "tags": doc["tags"],
                "tag_scores": doc["tag_scores"],
                "caption": doc["caption"],
                "quality": doc["quality"],
            }
        )

    for cluster_doc_id, samples in cluster_samples.items():
        if write_firestore:
            merge_face_cluster(
                cluster_doc_id,
                {
                    "sample_image_ids": [s[0] for s in samples],
                    "size": len(samples),
                    "label": None,
                },
            )

    sheet_path = OUT_DIR / "face_clusters_contact.png"
    build_face_contact_sheet(cluster_samples, sheet_path)

    emb_dir = OUT_DIR / "embeddings"
    emb_dir.mkdir(parents=True, exist_ok=True)
    for ref in refs:
        sig = signals.setdefault(ref.image_id, {})
        if "_clip_embedding" in sig:
            np.save(emb_dir / f"{ref.image_id}.npy", sig["_clip_embedding"])
            continue
        cache = emb_dir / f"{ref.image_id}.npy"
        if cache.is_file():
            sig["_clip_embedding"] = np.load(cache)
        else:
            sig["_clip_embedding"] = clip_tags.encode_image(ref.local_path)
            np.save(cache, sig["_clip_embedding"])

    catalog_index = load_catalog_index(CATALOG_PATH)
    checklist_items = parse_checklist(CHECKLIST_PATH)
    match_summary = {"high": [], "medium": [], "low": [], "none": [], "skipped_posted": []}
    match_signals = {
        iid: {k: v for k, v in sig.items()}
        for iid, sig in signals.items()
    }
    for item in checklist_items:
        result = match_checklist_item(item, match_signals, catalog_index)
        match_summary.setdefault(result["confidence"], []).append(item.title)
        if write_firestore and result["confidence"] not in ("skipped_posted",):
            write_checklist_match(
                item.item_id,
                {
                    "item_title": item.title,
                    "candidates": result["candidates"],
                    "confidence": result["confidence"],
                },
            )

    def _avg(key: str) -> float:
        xs = timings.get(key) or []
        return round(sum(xs) / len(xs), 3) if xs else 0.0

    stats = {
        "images_total": len(refs),
        "images_processed_this_run": len(todo),
        "dup_stacks": len(stacks),
        "face_clusters": len(cluster_samples),
        "clip_uploads": report_uploads,
        "seconds_total": round(time.time() - t0, 1),
        "seconds_per_image_hash": _avg("hash"),
        "seconds_per_image_faces": _avg("faces"),
        "seconds_per_image_clip": _avg("clip"),
        "caption_mode": caption_skipped,
        "checklist_high": len(match_summary.get("high", [])),
        "checklist_none": len(match_summary.get("none", [])),
    }
    state["stats"] = stats
    state["stacks"] = {k: v for k, v in list(stacks.items())[:50]}
    _save_state(state)

    summary_path = OUT_DIR / "run_summary.json"
    summary_path.write_text(
        json.dumps(
            {"stats": stats, "checklist_matches": match_summary, "match_lists": match_summary},
            indent=2,
        )
    )
    return stats
