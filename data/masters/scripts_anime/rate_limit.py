"""Simple thread-safe minimum-interval rate limiter."""

from __future__ import annotations

import threading
import time


class RateLimiter:
    def __init__(self, min_interval_s: float) -> None:
        self._min_interval_s = min_interval_s
        self._lock = threading.Lock()
        self._last_at = 0.0

    def wait(self) -> None:
        with self._lock:
            now = time.monotonic()
            elapsed = now - self._last_at
            if elapsed < self._min_interval_s:
                time.sleep(self._min_interval_s - elapsed)
            self._last_at = time.monotonic()
