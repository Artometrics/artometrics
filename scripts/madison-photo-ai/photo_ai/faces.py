from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np
from sklearn.cluster import DBSCAN


@dataclass
class FaceHit:
    bbox: list[float]
    embedding: np.ndarray


_face_app = None


def get_face_app():
    global _face_app
    if _face_app is None:
        from insightface.app import FaceAnalysis

        _face_app = FaceAnalysis(
            name="buffalo_l",
            providers=["CoreMLExecutionProvider", "CPUExecutionProvider"],
        )
        _face_app.prepare(ctx_id=0, det_size=(640, 640))
    return _face_app


def detect_faces(path: Path) -> list[FaceHit]:
    app = get_face_app()
    img = cv2.imread(str(path))
    if img is None:
        return []
    hits: list[FaceHit] = []
    for f in app.get(img):
        bbox = [float(x) for x in f.bbox.tolist()]
        emb = np.asarray(f.normed_embedding, dtype=np.float32)
        hits.append(FaceHit(bbox=bbox, embedding=emb))
    return hits


def cluster_embeddings(
    all_embeddings: list[tuple[str, np.ndarray]],
    eps: float,
    min_samples: int,
) -> dict[str, int]:
    if not all_embeddings:
        return {}
    ids = [x[0] for x in all_embeddings]
    X = np.stack([x[1] for x in all_embeddings], axis=0)
    try:
        import hdbscan

        clusterer = hdbscan.HDBSCAN(
            min_cluster_size=min_samples,
            metric="euclidean",
            cluster_selection_epsilon=eps,
        )
        labels = clusterer.fit_predict(X)
    except Exception:
        labels = DBSCAN(eps=eps, min_samples=min_samples, metric="cosine").fit_predict(
            X
        )

    out: dict[str, int] = {}
    for face_key, lab in zip(ids, labels):
        if lab < 0:
            continue
        out[face_key] = int(lab)
    return out


def face_key(image_id: str, index: int) -> str:
    return f"{image_id}#{index}"
