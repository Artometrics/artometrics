#!/usr/bin/env python3
"""Compare CMS HRRP dataset release to committed raw files; optional full rebuild."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "articles/readmitted/data"
REPORT = DATA_DIR / "cms_refresh_report.json"
SOURCE = DATA_DIR / "SOURCE.txt"
HRRP_ID = "9n3s-kdb3"
HOSP_ID = "xubh-q36u"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def cms_modified(dataset_id: str) -> str:
    url = (
        "https://data.cms.gov/provider-data/api/1/metastore/schemas/dataset/items/"
        f"{dataset_id}?show-reference-ids=false"
    )
    with urllib.request.urlopen(url, timeout=60) as resp:
        meta = json.load(resp)
    return meta.get("modified") or meta.get("date") or ""


def read_headline_stats() -> dict:
    hrrp = DATA_DIR / "raw_hrrp.csv"
    if not hrrp.exists():
        return {}
    import csv

    vals = []
    with hrrp.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            v = row.get("Excess Readmission Ratio", "").strip()
            if v and v not in ("Not Available", "NA"):
                try:
                    vals.append(float(v))
                except ValueError:
                    pass
    if not vals:
        return {}
    pct = 100 * sum(1 for x in vals if x > 1) / len(vals)
    return {"pairs_n": len(vals), "pct_err_gt_1": round(pct, 2)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh", action="store_true", help="Run full prepare-readmitted-data.py")
    args = parser.parse_args()

    local_hrrp = DATA_DIR / "raw_hrrp.csv"
    local_sha = sha256_file(local_hrrp) if local_hrrp.exists() else ""
    committed_modified = ""
    if SOURCE.exists():
        for line in SOURCE.read_text(encoding="utf-8").splitlines():
            if line.startswith("CMS HRRP modified:"):
                committed_modified = line.split(":", 1)[1].strip()

    remote_hrrp = cms_modified(HRRP_ID)
    remote_hosp = cms_modified(HOSP_ID)
    newer = bool(remote_hrrp and remote_hrrp != committed_modified)

    before = read_headline_stats()
    if args.refresh and newer:
        subprocess.run(
            [sys.executable, str(ROOT / "scripts/prepare-readmitted-data.py")],
            check=True,
            cwd=str(ROOT),
        )
    after = read_headline_stats()

    report = {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "dataset_hrrp": HRRP_ID,
        "dataset_hospital": HOSP_ID,
        "remote_modified_hrrp": remote_hrrp,
        "remote_modified_hospital": remote_hosp,
        "committed_modified_hrrp": committed_modified,
        "newer_release_available": newer,
        "local_raw_hrrp_sha256": local_sha,
        "headline_before": before,
        "headline_after": after,
        "headline_delta_pct": (
            round(after.get("pct_err_gt_1", 0) - before.get("pct_err_gt_1", 0), 2)
            if before and after
            else None
        ),
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    if newer and not args.refresh:
        sys.exit(1)  # signal workflow to refresh


if __name__ == "__main__":
    main()
