import os
from pathlib import Path

HOME = Path.home()
ROOT = Path(os.environ.get("PHOTO_AI_ROOT", HOME / "worker" / "photo-ai"))
STAGING_ROOT = Path(
    os.environ.get(
        "MADISON_STAGING",
        HOME / "worker" / "agency" / "madison" / "staging",
    )
)
CATALOG_PATH = Path(
    os.environ.get(
        "MADISON_CATALOG",
        HOME
        / "worker"
        / "agency"
        / "madison"
        / "madison"
        / "dashboard"
        / "src"
        / "data"
        / "catalog.json",
    )
)
CHECKLIST_PATH = ROOT / "data" / "release-checklist.md"
OUT_DIR = ROOT / "out"
STATE_PATH = OUT_DIR / "state.json"
CACHE_DIR = ROOT / ".cache"

FIREBASE_PROJECT = os.environ.get("FIREBASE_PROJECT", "madison-510519")
STORAGE_BUCKET = os.environ.get(
    "STORAGE_BUCKET", "madison-510519.firebasestorage.app"
)
GCS_WORK_PREFIX = "work/"

os.environ.setdefault("GOOGLE_CLOUD_QUOTA_PROJECT", FIREBASE_PROJECT)

PHASH_MAX_DIST = 10
DHASH_MAX_DIST = 10

FACE_CLUSTER_MIN_SIZE = 2
FACE_CLUSTER_EPS = 0.45

CLIP_MODEL = "ViT-B-32"
CLIP_PRETRAINED = "openai"

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434")
OLLAMA_VISION_MODEL = os.environ.get("OLLAMA_VISION_MODEL", "qwen2.5vl:3b")
CAPTION_MAX_IMAGES = int(os.environ.get("CAPTION_MAX_IMAGES", "0"))
CAPTION_SAMPLE_SEC = float(os.environ.get("CAPTION_SAMPLE_SEC", "8.0"))
