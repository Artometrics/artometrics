from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


def build_face_contact_sheet(
    samples: dict[str, list[tuple[str, Path]]],
    out_path: Path,
    thumb: int = 96,
    cols: int = 6,
) -> None:
    """samples: cluster_id -> list of (image_id, local_path) up to 6."""
    rows_data = []
    for cluster_id in sorted(samples.keys(), key=lambda x: (len(samples[x]), x), reverse=True):
        rows_data.append((cluster_id, samples[cluster_id][:cols]))
    if not rows_data:
        return
    row_h = thumb + 28
    width = cols * thumb + 20
    height = len(rows_data) * row_h + 20
    canvas = Image.new("RGB", (width, height), (24, 24, 24))
    draw = ImageDraw.Draw(canvas)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)
    except OSError:
        font = ImageFont.load_default()
    y = 10
    for cluster_id, cells in rows_data:
        draw.text((10, y), cluster_id, fill=(220, 220, 220), font=font)
        y += 18
        x = 10
        for image_id, path in cells:
            try:
                im = Image.open(path).convert("RGB")
                im.thumbnail((thumb, thumb))
                canvas.paste(im, (x, y))
            except OSError:
                pass
            x += thumb
        y += thumb + 10
    out_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out_path, quality=85)
