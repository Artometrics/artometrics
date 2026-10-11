#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
export PHOTO_AI_ROOT="$ROOT"
export GOOGLE_CLOUD_QUOTA_PROJECT="${GOOGLE_CLOUD_QUOTA_PROJECT:-madison-510519}"
export GOOGLE_CLOUD_PROJECT="${GOOGLE_CLOUD_PROJECT:-madison-510519}"
export FIREBASE_PROJECT="${FIREBASE_PROJECT:-madison-510519}"
export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
# Captions off by default (pull qwen2.5vl:3b + set CAPTION_MAX_IMAGES>0 to enable)
export CAPTION_MAX_IMAGES="${CAPTION_MAX_IMAGES:-0}"
source "$ROOT/.venv/bin/activate"
exec python -m photo_ai.cli "$@"
