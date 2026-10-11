#!/usr/bin/env python3
"""Refresh data/reference/cpi from FRED (or BLS if BLS_API_KEY set)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from lib.cpi import CPI_ANNUAL, refresh_cpi_cache  # noqa: E402


def main() -> None:
    import os

    prefer_bls = bool(os.environ.get("BLS_API_KEY"))
    refresh_cpi_cache(prefer_bls=prefer_bls)
    print(f"Wrote {CPI_ANNUAL}")


if __name__ == "__main__":
    main()
