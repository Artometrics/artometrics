#!/usr/bin/env python3
"""
Generate AI illustration PNGs for franchise video prompts (run locally on Mac mini).

Requires:
  pip install google-genai
  export GEMINI_API_KEY=...
  export GEMINI_IMAGE_MODEL=gemini-2.5-flash-image   # or your preferred image model

Reads:
  articles/franchise/video/assets/ai_prompt_library.csv
  articles/franchise/video/assets/ai_prompts.csv (to know which prompts appear in vertical)

Writes:
  assets/ai/{prompt_id}_16x9.png
  assets/ai/{prompt_id}_9x16.png  (only for prompt_ids used in storyboard-vertical.csv scenes)
"""
from __future__ import annotations

import base64
import csv
import os
import sys
from pathlib import Path

ASSETS_DIR = Path(__file__).resolve().parent
VIDEO_DIR = ASSETS_DIR.parent
OUT_DIR = ASSETS_DIR / "ai"
LIBRARY = ASSETS_DIR / "ai_prompt_library.csv"
SCENE_PROMPTS = ASSETS_DIR / "ai_prompts.csv"
VERTICAL_STORYBOARD = VIDEO_DIR / "storyboard-vertical.csv"


def vertical_prompt_ids() -> set[str]:
    if not SCENE_PROMPTS.exists() or not VERTICAL_STORYBOARD.exists():
        return set()
    vertical_scenes = {
        row["scene_id"]
        for row in csv.DictReader(VERTICAL_STORYBOARD.open(encoding="utf-8"))
    }
    ids: set[str] = set()
    for row in csv.DictReader(SCENE_PROMPTS.open(encoding="utf-8")):
        if row["scene_id"] in vertical_scenes:
            ids.add(row["prompt_id"])
    return ids


def load_library() -> dict[str, str]:
    lib: dict[str, str] = {}
    with LIBRARY.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            lib[row["prompt_id"]] = row["prompt"]
    return lib


def save_inline_image(data_b64: str, mime: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    raw = base64.b64decode(data_b64)
    if mime == "image/jpeg":
        dest = dest.with_suffix(".jpg")
    else:
        dest = dest.with_suffix(".png")
    dest.write_bytes(raw)
    print(f"Wrote {dest}")


def generate_one(client, model: str, prompt: str, aspect: str) -> tuple[str, str]:
    full_prompt = f"{prompt} Composition aspect ratio {aspect}. No text, no watermark."
    response = client.models.generate_content(model=model, contents=full_prompt)
    parts = response.candidates[0].content.parts if response.candidates else []
    for part in parts:
        inline = getattr(part, "inline_data", None) or getattr(part, "inlineData", None)
        if not inline:
            continue
        data = inline.data if hasattr(inline, "data") else inline.get("data")
        mime = inline.mime_type if hasattr(inline, "mime_type") else inline.get("mimeType", "image/png")
        if data:
            return data, mime
    raise RuntimeError("No image bytes in Gemini response")


def main() -> int:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY is not set.", file=sys.stderr)
        return 1
    model = os.environ.get("GEMINI_IMAGE_MODEL", "gemini-2.5-flash-image")

    try:
        from google import genai
    except ImportError:
        print("Install google-genai: pip install google-genai", file=sys.stderr)
        return 1

    client = genai.Client(api_key=api_key)
    library = load_library()
    vertical_ids = vertical_prompt_ids()

    for prompt_id, prompt in sorted(library.items()):
        for aspect in ("16:9",):
            suffix = "16x9"
            dest = OUT_DIR / f"{prompt_id}_{suffix}.png"
            if dest.exists():
                print(f"Skip {dest} (exists)")
                continue
            data, mime = generate_one(client, model, prompt, aspect)
            save_inline_image(data, mime, dest)

        if prompt_id in vertical_ids:
            dest = OUT_DIR / f"{prompt_id}_9x16.png"
            if dest.exists():
                print(f"Skip {dest} (exists)")
                continue
            data, mime = generate_one(client, model, prompt, "9:16")
            save_inline_image(data, mime, dest)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
