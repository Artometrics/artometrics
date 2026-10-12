#!/usr/bin/env python3
"""Pull SEC XBRL companyfacts revenue tables for media companies."""

from __future__ import annotations

import json
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data/reference/sec"
SOURCE = OUT / "SOURCE.txt"
USER_AGENT = "Artometrics Data Pipeline team@artometrics.com"

# name -> (CIK zero-padded, notes)
COMPANIES = {
    "alphabet": ("0001652044", "YouTube ads in segment notes; consolidated revenues below"),
    "disney": ("0001744489", ""),
    "netflix": ("0001065280", ""),
    "warner_bros_discovery": ("0001437107", "Warner Bros. Discovery, Inc."),
    "comcast": ("0001166691", ""),
    "paramount_global": ("0000813828", "Paramount Global"),
    "sony_group": ("0000313838", "Sony Group Corp (ADR)"),
    "nintendo": (
        "0001069392",
        "Nintendo Co Ltd — verify entity; US filers may use 20-F with limited tags",
    ),
}

REVENUE_TAGS = (
    "Revenues",
    "RevenueFromContractWithCustomerExcludingAssessedTax",
    "SalesRevenueNet",
    "RevenueFromContractWithCustomerIncludingAssessedTax",
)


def sec_get(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=90) as resp:
        return json.load(resp)


def extract_annual_revenues(facts: dict) -> list[dict]:
    us = facts.get("facts", {}).get("us-gaap", {})
    rows: list[dict] = []
    for tag in REVENUE_TAGS:
        block = us.get(tag)
        if not block:
            continue
        for unit, entries in block.get("units", {}).items():
            if unit not in ("USD", "USD/shares"):
                continue
            for e in entries:
                if e.get("form") not in ("10-K", "20-F", "40-F"):
                    continue
                fy = e.get("fy")
                if not fy:
                    continue
                rows.append(
                    {
                        "tag": tag,
                        "fiscal_year": fy,
                        "value_usd": e.get("val"),
                        "filed": e.get("filed"),
                        "form": e.get("form"),
                        "fp": e.get("fp"),
                        "unit": unit,
                    }
                )
    # dedupe: keep latest filed per fy+tag
    best: dict[tuple, dict] = {}
    for r in rows:
        key = (r["fiscal_year"], r["tag"])
        if key not in best or (r["filed"] or "") > (best[key]["filed"] or ""):
            best[key] = r
    return sorted(best.values(), key=lambda x: (x["fiscal_year"], x["tag"]))


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    manifest: list[dict] = []
    for slug, (cik, note) in COMPANIES.items():
        url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
        print(f"Fetching {slug} {url}")
        try:
            data = sec_get(url)
            time.sleep(0.2)
        except Exception as exc:  # noqa: BLE001
            manifest.append({"company": slug, "cik": cik, "error": str(exc), "url": url})
            continue
        rows = extract_annual_revenues(data)
        out_path = OUT / f"{slug}_revenues.json"
        out_path.write_text(json.dumps(rows, indent=2), encoding="utf-8")
        csv_path = OUT / f"{slug}_revenues.csv"
        if rows:
            import csv

            with csv_path.open("w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
                w.writeheader()
                w.writerows(rows)
        manifest.append(
            {
                "company": slug,
                "cik": cik,
                "note": note,
                "companyfacts_url": url,
                "rows": len(rows),
                "entity": data.get("entityName"),
            }
        )

    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    SOURCE.write_text(
        "\n".join(
            [
                "SEC EDGAR XBRL companyfacts extract",
                f"Generated: {datetime.now(timezone.utc).isoformat()}",
                f"User-Agent: {USER_AGENT}",
                "API: https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json",
                "",
                "Tables: data/reference/sec/*_revenues.csv",
                "Segment-level detail may require 10-K note parsing; this file is consolidated revenue tags.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {OUT} ({len(manifest)} companies)")


if __name__ == "__main__":
    main()
