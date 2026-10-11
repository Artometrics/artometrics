from __future__ import annotations

import io
from pathlib import Path

import numpy as np

from .config import FIREBASE_PROJECT, STORAGE_BUCKET

_db = None
_bucket = None


def init_firebase():
    global _db, _bucket
    if _db is not None:
        return _db, _bucket
    import firebase_admin
    from firebase_admin import credentials, firestore, storage

    if not firebase_admin._apps:
        firebase_admin.initialize_app(
            credentials.ApplicationDefault(),
            {"projectId": FIREBASE_PROJECT, "storageBucket": STORAGE_BUCKET},
        )
    _db = firestore.client()
    _bucket = storage.bucket()
    return _db, _bucket


def upload_clip_embedding(image_id: str, embedding: np.ndarray) -> str:
    _, bucket = init_firebase()
    blob_path = f"signals/clip/{image_id}.npy"
    blob = bucket.blob(blob_path)
    buf = io.BytesIO()
    np.save(buf, embedding.astype(np.float16))
    buf.seek(0)
    blob.upload_from_file(buf, content_type="application/octet-stream")
    return f"gs://{STORAGE_BUCKET}/{blob_path}"


def merge_image_signals(image_id: str, doc: dict, skip_if_processed: bool = False) -> bool:
    db, _ = init_firebase()
    ref = db.collection("image_signals").document(image_id)
    if skip_if_processed and ref.get().exists:
        return False
    ref.set(doc, merge=True)
    return True


def merge_face_cluster(cluster_id: str, doc: dict) -> None:
    db, _ = init_firebase()
    db.collection("face_clusters").document(cluster_id).set(doc, merge=True)


def write_checklist_match(item_id: str, doc: dict) -> bool:
    """Returns False if human-confirmed match exists and should not be overwritten."""
    db, _ = init_firebase()
    ref = db.collection("checklist_matches").document(item_id)
    snap = ref.get()
    if snap.exists:
        data = snap.to_dict() or {}
        if data.get("human_confirmed"):
            return False
    ref.set(doc, merge=True)
    return True
