# Madison photo-ai (local)

Open-source pipeline on the Mac mini for duplicate stacks, face clusters, CLIP tags, and Kyle’s IG release checklist matching. Writes to Firebase project `madison-510519`.

## Paths

| Item | Location |
|------|----------|
| Venv + code | `~/worker/photo-ai/` |
| Staged JPEGs | `~/worker/agency/madison/staging/work/<shortcode>/<n>.jpg` |
| Catalog | `~/worker/agency/madison/madison/dashboard/src/data/catalog.json` |
| Checklist | `~/worker/photo-ai/data/release-checklist.md` |
| Outputs | `~/worker/photo-ai/out/` (`state.json`, `face_clusters_contact.png`, `run_summary.json`) |

**Image IDs:** `imageId = <shortcode>_<n>` (e.g. `ig_17841490468051707_1`). Storage layout is `work/<shortcode>/<n>.jpg`. Some docs say `col_<shortcode>`; this bucket currently uses `ig_*` post folders—the same ID rule applies.

## One command

```bash
export GOOGLE_CLOUD_QUOTA_PROJECT=madison-510519
~/worker/photo-ai/run.sh
```

Incremental: only images whose file mtime/size changed are reprocessed. Delete `~/worker/photo-ai/out/state.json` for a full rebuild.

### Options

```bash
~/worker/photo-ai/run.sh --no-firestore    # local dry run
~/worker/photo-ai/run.sh --limit 20        # smoke test
CAPTION_MAX_IMAGES=5 ~/worker/photo-ai/run.sh   # Ollama captions (slow)
```

Captions use `OLLAMA_VISION_MODEL` (default `qwen2.5vl:3b`). Pull the model first; default `CAPTION_MAX_IMAGES=0` skips captions.

## Firestore / Storage

- `image_signals/{imageId}` — phash, dhash, dup stack, tags, caption, faces, quality, `clip_embedding_path`
- `face_clusters/{id}` — sample image IDs, size, `label: null`
- `checklist_matches/{itemId}` — candidates + confidence (skipped when `human_confirmed` is true)
- CLIP vectors: `gs://madison-510519.firebasestorage.app/signals/clip/{imageId}.npy` (float16)

## Stack (open source)

| Step | Tool |
|------|------|
| Duplicates | `imagehash` (pHash + dHash), sharpness × resolution for best-in-stack |
| Faces | **InsightFace `buffalo_l`** via ONNX Runtime (**CoreML** on Apple Silicon) + HDBSCAN |
| Tags / embeddings | `open_clip` ViT-B-32 |
| Captions (optional) | Ollama vision |
| Cloud | `firebase-admin` + ADC (`gcloud auth application-default login`) |

### InsightFace licence (commercial blocker)

InsightFace model zoo weights (including `buffalo_l`) are distributed for **non-commercial research** unless you obtain a separate licence from the authors. **Do not ship this stack in a paid product without replacing the face model.**

Permissive alternative: **`face_recognition` / dlib** (MIT) or **MediaPipe Face Detection** + a small open embedding head—swap `photo_ai/faces.py` and re-cluster.

## Setup (once)

```bash
cd ~/worker/photo-ai
uv venv && source .venv/bin/activate
uv pip install -e .
```

InsightFace downloads `buffalo_l` to `~/.insightface/models/` on first run (~275 MB).

## Auth

```bash
export GOOGLE_CLOUD_QUOTA_PROJECT=madison-510519
gcloud auth application-default login
```

Scripts in the Artometrics repo: `scripts/madison-photo-ai/` (mirrors this layout for version control).
