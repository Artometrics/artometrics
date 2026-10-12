"""Parse Wikipedia highest-grossing franchises wikitext into a name→row dict."""

from __future__ import annotations

import json
import re
import urllib.request

USER_AGENT = "ArtometricsResearch/1.0 (https://artometrics.com)"


def fetch_wikitext() -> str:
    url = (
        "https://en.wikipedia.org/w/api.php?action=query"
        "&titles=List_of_highest-grossing_media_franchises"
        "&prop=revisions&rvprop=content&rvslots=main&format=json"
    )
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=120) as resp:
        payload = json.load(resp)
    return next(iter(payload["query"]["pages"].values()))["revisions"][0]["slots"]["main"]["*"]


def clean_cell(s: str) -> str:
    s = re.sub(r"\[\[([^|\]]+)\|([^\]]+)\]\]", r"\2", s)
    s = re.sub(r"\[\[([^\]]+)\]\]", r"\1", s)
    s = re.sub(r"''", "", s)
    s = re.sub(r"<br\s*/?>", " ", s, flags=re.I)
    s = re.sub(r"<[^>]+>", "", s)
    s = re.sub(r"\{\{efn[^}]*\}\}", "", s, flags=re.S)
    s = re.sub(r"\{\{[^}]+\}\}", "", s)
    return re.sub(r"\s+", " ", s).strip()


def parse_wiki_index(wikitext: str) -> dict[str, dict]:
    """Map Wikipedia display title → {total_b, owners, year}."""
    rows: dict[str, dict] = {}
    for block in re.split(r"\n\|-", wikitext):
        m = re.search(r'! scope=["\']?row["\']?\s*\|\s*(.+)', block, re.I)
        if not m:
            continue
        name = clean_cell(m.group(1))
        if not name or name.startswith("colspan"):
            continue
        parts = [p.strip() for p in block.split("\n|")[1:]]
        if len(parts) < 2:
            continue
        year = re.sub(r"[^0-9].*", "", parts[0]) or ""
        rev_m = re.search(r"\$([0-9,.]+)\s*billion", parts[1], re.I)
        total_b = float(rev_m.group(1).replace(",", "")) if rev_m else None
        owners = clean_cell(parts[5]) if len(parts) > 5 else ""
        rows[name] = {
            "year_created": year,
            "total_revenue_usd_b_2026": total_b,
            "owner_now": owners,
        }
    return rows
