from __future__ import annotations

import base64
import json
import urllib.request
from pathlib import Path

from .config import CAPTION_SAMPLE_SEC, OLLAMA_URL, OLLAMA_VISION_MODEL


def ollama_caption(path: Path, timeout: float = CAPTION_SAMPLE_SEC) -> str | None:
    try:
        data = path.read_bytes()
        b64 = base64.b64encode(data).decode("ascii")
        payload = {
            "model": OLLAMA_VISION_MODEL,
            "prompt": "Describe the outfit, colors, fabrics, and event setting in one short sentence.",
            "images": [b64],
            "stream": False,
        }
        req = urllib.request.Request(
            f"{OLLAMA_URL}/api/generate",
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = json.loads(resp.read().decode())
        return (body.get("response") or "").strip() or None
    except Exception:
        return None
