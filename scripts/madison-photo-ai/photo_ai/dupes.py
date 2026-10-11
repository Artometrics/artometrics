from __future__ import annotations

import imagehash
from PIL import Image

from .paths import ImageRef


def _sharpness(im: Image.Image) -> float:
    import cv2
    import numpy as np

    gray = np.array(im.convert("L"))
    return float(cv2.Laplacian(gray, cv2.CV_64F).var())


def _quality(im: Image.Image) -> dict:
    w, h = im.size
    sharp = _sharpness(im)
    score = sharp * (w * h) ** 0.25
    return {"width": w, "height": h, "sharpness": round(sharp, 2), "score": round(score, 2)}


def compute_hashes(path) -> tuple[str, str, dict]:
    with Image.open(path) as im:
        ph = str(imagehash.phash(im))
        dh = str(imagehash.dhash(im))
        qual = _quality(im)
    return ph, dh, qual


def hamming_hex(a: str, b: str) -> int:
    return imagehash.hex_to_hash(a) - imagehash.hex_to_hash(b)


def build_duplicate_stacks(
    items: list[tuple[ImageRef, str, str, dict]],
    phash_max: int,
    dhash_max: int,
) -> tuple[dict[str, str], dict[str, bool], dict[str, list[str]]]:
    """Return per-image dup_stack_id, is_best_in_stack, and stack_id -> member ids."""
    n = len(items)
    parent = list(range(n))

    def find(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(i: int, j: int) -> None:
        ri, rj = find(i), find(j)
        if ri != rj:
            parent[rj] = ri

    for i in range(n):
        for j in range(i + 1, n):
            ph_i, dh_i = items[i][1], items[i][2]
            ph_j, dh_j = items[j][1], items[j][2]
            if hamming_hex(ph_i, ph_j) <= phash_max or hamming_hex(dh_i, dh_j) <= dhash_max:
                union(i, j)

    groups: dict[int, list[int]] = {}
    for i in range(n):
        groups.setdefault(find(i), []).append(i)

    stack_for_image: dict[str, str] = {}
    best_for_image: dict[str, bool] = {}
    stacks: dict[str, list[str]] = {}

    for members in groups.values():
        ranked = sorted(
            members,
            key=lambda idx: items[idx][3]["score"],
            reverse=True,
        )
        best_idx = ranked[0]
        stack_id = f"stack_{items[best_idx][0].image_id}"
        ids = [items[i][0].image_id for i in members]
        stacks[stack_id] = ids
        for i in members:
            ref = items[i][0]
            stack_for_image[ref.image_id] = stack_id
            best_for_image[ref.image_id] = i == best_idx

    return stack_for_image, best_for_image, stacks
