#!/usr/bin/env python3
"""Refresh Lahman CSV subset for Padres + MLB Stats API season snapshot."""

from __future__ import annotations

import csv
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PADRES_DATA = ROOT / "articles/padres/data"
LAHMAN_DIR = PADRES_DATA / "lahman"
SOURCE = PADRES_DATA / "SOURCE.txt"

# Chadwick Bureau Lahman CSV mirror (core tables)
LAHMAN_BASE = (
    "https://raw.githubusercontent.com/chadwickbureau/baseballdatabank/master/core"
)
MLB_TEAM_ID = 135  # San Diego Padres
LAHMAN_TABLES = ("Teams.csv", "SeriesPost.csv", "Salaries.csv", "TeamsFranchises.csv")


def download_lahman() -> str:
    """Return status note for SOURCE.txt."""
    LAHMAN_DIR.mkdir(parents=True, exist_ok=True)
    try:
        for name in LAHMAN_TABLES:
            url = f"{LAHMAN_BASE}/{name}"
            target = LAHMAN_DIR / name
            print(f"Downloading {url}")
            with urllib.request.urlopen(url, timeout=120) as resp:
                target.write_bytes(resp.read())
        return "Lahman tables refreshed from Chadwick Bureau GitHub mirror."
    except Exception as exc:  # noqa: BLE001
        print(f"Lahman download skipped ({exc}); using committed lahman/*.csv")
        return f"Lahman download skipped ({exc}); using committed lahman/*.csv"


def mlb_padres_season(year: int) -> dict:
    url = (
        f"https://statsapi.mlb.com/api/v1/teams/{MLB_TEAM_ID}/stats"
        f"?stats=season&season={year}"
    )
    with urllib.request.urlopen(url, timeout=60) as resp:
        data = json.load(resp)
    stats = data.get("stats", [{}])[0].get("splits", [{}])[0].get("stat", {})
    return {
        "year": year,
        "wins": stats.get("wins"),
        "losses": stats.get("losses"),
        "runs": stats.get("runs"),
        "runs_allowed": stats.get("runsScoredAgainst") or stats.get("runsAllowed"),
        "source": url,
    }


def sha256(path: Path) -> str:
    import hashlib

    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    lahman_note = download_lahman()
    current_year = datetime.now(timezone.utc).year
    mlb_rows = []
    for y in range(current_year - 1, current_year + 1):
        try:
            mlb_rows.append(mlb_padres_season(y))
        except Exception as exc:  # noqa: BLE001
            mlb_rows.append({"year": y, "error": str(exc)})

    mlb_path = PADRES_DATA / "mlb_stats_api_padres.json"
    mlb_path.write_text(json.dumps(mlb_rows, indent=2), encoding="utf-8")

    artifacts = [LAHMAN_DIR / t for t in LAHMAN_TABLES] + [mlb_path]
    SOURCE.write_text(
        "\n".join(
            [
                "Artometrics Padres baseball data cache",
                f"Generated: {datetime.now(timezone.utc).isoformat()}",
                f"Lahman base: {LAHMAN_BASE}",
                lahman_note,
                "MLB Stats API: statsapi.mlb.com (unofficial public API)",
                "",
                "SHA256:",
                *[f"- {p.name}: {sha256(p)}" for p in artifacts if p.exists()],
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"Updated Lahman tables in {LAHMAN_DIR} and {mlb_path}")


if __name__ == "__main__":
    main()
