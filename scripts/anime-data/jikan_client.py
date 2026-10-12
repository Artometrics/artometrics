"""Jikan v4 client with disk cache, resume, and rate limits."""

from __future__ import annotations

import hashlib
import json
import logging
from pathlib import Path
from typing import Any

import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from config import (
    CACHE_DIR,
    JIKAN_BASE,
    JIKAN_CONNECT_TIMEOUT_S,
    JIKAN_MIN_INTERVAL_S,
    JIKAN_READ_TIMEOUT_S,
)
from rate_limit import RateLimiter

log = logging.getLogger(__name__)

_jikan_limiter = RateLimiter(JIKAN_MIN_INTERVAL_S)


def _cache_path(key: str) -> Path:
    digest = hashlib.sha256(key.encode()).hexdigest()[:32]
    return CACHE_DIR / "jikan" / f"{digest}.json"


def _read_cache(key: str) -> dict[str, Any] | None:
    path = _cache_path(key)
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def _write_cache(key: str, payload: dict[str, Any]) -> None:
    path = _cache_path(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


class JikanClient:
    def __init__(self, enabled: bool = True) -> None:
        self.enabled = enabled
        self._client = httpx.Client(
            base_url=JIKAN_BASE,
            timeout=httpx.Timeout(JIKAN_READ_TIMEOUT_S, connect=JIKAN_CONNECT_TIMEOUT_S),
            headers={"User-Agent": "Artometrics-anime-data/1.0 (github.com/Artometrics/artometrics)"},
        )
        self.unreachable = False

    def close(self) -> None:
        self._client.close()

    @retry(
        retry=retry_if_exception_type(httpx.HTTPStatusError),
        stop=stop_after_attempt(4),
        wait=wait_exponential(multiplier=2, min=4, max=60),
        reraise=True,
    )
    def _get_json(self, path: str) -> dict[str, Any]:
        if not self.enabled or self.unreachable:
            raise RuntimeError("jikan_disabled")
        _jikan_limiter.wait()
        try:
            resp = self._client.get(path)
        except (httpx.ConnectTimeout, httpx.ReadTimeout, httpx.ConnectError) as exc:
            self.unreachable = True
            log.warning("Jikan unreachable (%s); further Jikan calls skipped this run.", exc)
            raise RuntimeError("jikan_unreachable") from exc
        if resp.status_code == 404:
            return {"data": None, "_not_found": True}
        if resp.status_code == 429 or resp.status_code >= 500:
            raise httpx.HTTPStatusError(f"retryable {resp.status_code}", request=resp.request, response=resp)
        resp.raise_for_status()
        return resp.json()

    def get_season(self, year: int, season: str) -> list[dict[str, Any]]:
        key = f"season:{year}:{season}"
        cached = _read_cache(key)
        if cached is not None:
            return cached.get("data", [])
        try:
            body = self._get_json(f"/seasons/{year}/{season}")
        except (RuntimeError, httpx.HTTPError):
            return []
        data = body.get("data") or []
        _write_cache(key, {"data": data})
        return data

    def get_anime_full(self, mal_id: int) -> dict[str, Any] | None:
        key = f"anime_full:{mal_id}"
        cached = _read_cache(key)
        if cached is not None:
            return cached.get("data")
        try:
            body = self._get_json(f"/anime/{mal_id}/full")
        except (RuntimeError, httpx.HTTPError) as exc:
            log.warning("Jikan anime %s failed: %s", mal_id, exc)
            return None
        data = body.get("data")
        if data is not None or body.get("_not_found"):
            _write_cache(key, {"data": data})
        return data
