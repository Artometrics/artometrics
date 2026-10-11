#!/usr/bin/env python3
"""Build franchise storyboard HTML decks in the Anime explainer layout."""
from __future__ import annotations

import csv
import html
import re
import sys
from pathlib import Path

DECK_DIR = Path(__file__).resolve().parent
VIDEO_DIR = DECK_DIR.parent
ASSETS = VIDEO_DIR / "assets"

DECKS = {
    "short": ("storyboard-short.csv", "16x9", "Short cut"),
    "deepdive": ("storyboard-deepdive.csv", "16x9", "Deep dive"),
    "vertical": ("storyboard-vertical.csv", "9x16", "Vertical"),
}

LOGO = "../../../../public/images/brand/chomsky-a-white.png"

from render_dark_charts import chart_parts, chart_series  # noqa: E402

UNITS = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
    "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
    "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17,
    "eighteen": 18, "nineteen": 19,
}
TENS = {"twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90}
SCALES = {"hundred": 100, "thousand": 1_000, "million": 1_000_000, "billion": 1_000_000_000, "trillion": 1_000_000_000_000}

ALIASES = [
    ("the pokémon company", "The Pokémon Company"),
    ("pokemon company", "The Pokémon Company"),
    ("21st century fox", "21st Century Fox"),
    ("twenty-first century fox", "21st Century Fox"),
    ("marvel cinematic universe", "Marvel Cinematic Universe"),
    ("wizarding world", "Wizarding World"),
    ("harry potter", "Wizarding World"),
    ("hello kitty", "Hello Kitty"),
    ("winnie the pooh", "Winnie the Pooh"),
    ("call of duty", "Call of Duty"),
    ("mortal kombat", "Mortal Kombat"),
    ("game freak", "Game Freak"),
    ("creatures", "Creatures Inc."),
    ("star wars", "Star Wars"),
    ("toy story", "Toy Story"),
    ("fast and furious", "Fast & Furious"),
    ("fast & furious", "Fast & Furious"),
    ("one piece", "One Piece"),
    ("dragon ball", "Dragon Ball"),
    ("bob the builder", "Bob the Builder"),
    ("thomas", "Thomas & Friends"),
    ("assassin", "Assassin's Creed"),
    ("spider-man", "Spider-Man"),
    ("spider man", "Spider-Man"),
    ("activision", "Activision Blizzard"),
    ("warner", "Warner Bros."),
    ("lucasfilm", "Lucasfilm"),
    ("pixar", "Pixar"),
    ("nintendo", "Nintendo"),
    ("disney", "The Walt Disney Company"),
    ("marvel", "Marvel Entertainment"),
    ("pokémon", "Pokémon"),
    ("pokemon", "Pokémon"),
    ("naruto", "Naruto"),
    ("sony", "Sony"),
    ("lego", "LEGO"),
    ("tencent", "Tencent"),
    ("nexon", "Nexon"),
    ("mattel", "Mattel"),
    ("ubisoft", "Ubisoft"),
    ("shueisha", "Shueisha"),
    ("minecraft", "Minecraft"),
    ("gundam", "Gundam"),
    ("peanuts", "Peanuts"),
    ("universal", "Universal"),
    ("microsoft", "Microsoft"),
]


def esc(s: str) -> str:
    return html.escape(s or "", quote=True)


DATA_DIR = Path(__file__).resolve().parents[2] / "data"

# Display name -> exact franchise.csv name, when they differ.
FRANCHISE_ALIAS = {
    "Wizarding World": "Wizarding World / Harry Potter",
    "Harry Potter": "Wizarding World / Harry Potter",
}

# Verified figure belongs to this franchise, not to a co-owner.
FRANCHISE_VERIFIED = {
    "Pokémon": "Pokemon lifetime revenue",
    "Hello Kitty": "Hello Kitty lifetime revenue",
    "Winnie the Pooh": "Winnie the Pooh lifetime revenue",
    "Call of Duty": "Call of Duty 2019 lifetime",
    "Mortal Kombat": "Mortal Kombat 2019 lifetime",
    "Star Wars": "Star Wars 2019 lifetime",
    "Marvel Cinematic Universe": "MCU 2019 lifetime",
    "Naruto": "Naruto 2019 lifetime",
    "Wizarding World / Harry Potter": "Wizarding World 2019 lifetime",
    "Toy Story": "Toy Story 2019 lifetime",
    "Mario": "Mario 2019 lifetime",
    "Gundam": "Gundam 2019 lifetime",
    "Batman": "Batman 2019 lifetime",
    "Superman": "Superman 2019 lifetime",
    "The Simpsons": "Simpsons 2019 lifetime",
    "DC Extended Universe": "DCEU 2019 lifetime",
}

# Company totals that are explicitly theirs. Never a substring sum of franchise rows.
OWNER_VERIFIED = {
    "Nintendo": ("Nintendo standalone owner total 2019", "Standalone label, excludes the Pokémon row", False),
    "The Pokémon Company": ("Pokemon Company owner-string total 2019", "Joint owners: Nintendo, Game Freak, Creatures", False),
    "DC Entertainment": ("DC Entertainment owner total 2019", "Batman, Superman, and the DCEU row", False),
}

COOWNERS = {
    "Game Freak": "Co-owner of The Pokémon Company",
    "Creatures Inc.": "Co-owner of The Pokémon Company",
}

DEALS = {
    "Pixar": ("Pixar acquisition price", "2006", "Acquisition price"),
    "Marvel Entertainment": ("Marvel acquisition price", "2009", "Acquisition price"),
    "Lucasfilm": ("Lucasfilm acquisition price", "2012", "Acquisition price"),
    "21st Century Fox": ("Fox enterprise value", "2019", "Enterprise value"),
}


def load_franchises() -> dict[str, dict]:
    path = DATA_DIR / "franchise.csv"
    rows: dict[str, dict] = {}
    if not path.exists():
        return rows
    for row in csv.DictReader(path.open(encoding="utf-8")):
        name = (row.get("franchise") or "").strip()
        if not name:
            continue
        slot = rows.setdefault(
            name,
            {"rev": 0.0, "year": row.get("year_created") or "", "owners": row.get("owners") or "", "media": row.get("original_media") or ""},
        )
        try:
            slot["rev"] += float(row.get("revenue") or 0)
        except ValueError:
            pass
        slot["year"] = row.get("year_created") or slot["year"]
        slot["owners"] = row.get("owners") or slot["owners"]
        slot["media"] = row.get("original_media") or slot["media"]
    return rows


def load_verified() -> dict[str, float]:
    path = DATA_DIR / "verified_numbers.csv"
    out: dict[str, float] = {}
    if not path.exists():
        return out
    for row in csv.DictReader(path.open(encoding="utf-8")):
        figure = (row.get("figure") or "").strip()
        raw = row.get("value") or ""
        match = re.search(r"-?\d+(?:\.\d+)?", raw)
        if figure and match:
            out[figure] = float(match.group(0))
    return out


def verified_money(verified: dict[str, float], key: str) -> float | None:
    if key not in verified:
        return None
    return verified[key]


def load_assets() -> dict[str, dict]:
    path = ASSETS / "asset_log.csv"
    out = {}
    if not path.exists():
        return out
    for row in csv.DictReader(path.open(encoding="utf-8")):
        out[row["asset_id"]] = row
        if row.get("entity"):
            out[row["entity"]] = row
    return out


def tokenize(text: str) -> list[str]:
    return re.findall(r"[0-9]+(?:\.[0-9]+)?|[\w'’&-]+", text, flags=re.UNICODE)


def consume_number(words: list[str], i: int) -> tuple[float | None, int]:
    total = 0.0
    current = 0.0
    saw = False
    while i < len(words):
        raw = words[i].lower().strip(".,")
        w = raw.replace("twenty-", "twenty ").split()[0] if False else raw
        if w in ("and",) and saw:
            # "hundred and three" still belongs to the number. "billion, and" does not.
            if current == 0:
                break
            i += 1
            continue
        if w == "point" and saw:
            i += 1
            digits = ""
            while i < len(words):
                u = words[i].lower().strip(".,")
                if u in UNITS and UNITS[u] < 10:
                    digits += str(UNITS[u])
                    i += 1
                    saw = True
                else:
                    break
            if digits:
                val = total + current + float("0." + digits)
                if i < len(words) and words[i].lower().strip(".,") in SCALES:
                    val *= SCALES[words[i].lower().strip(".,")]
                    i += 1
                return val, i
            return total + current, i
        if w in UNITS:
            current += UNITS[w]
            saw = True
            i += 1
            continue
        if w in TENS:
            current += TENS[w]
            saw = True
            i += 1
            continue
        if w == "hundred":
            current = (current or 1) * 100
            saw = True
            i += 1
            continue
        if w in SCALES and w != "hundred":
            current = (current or 1) * SCALES[w]
            total += current
            current = 0
            saw = True
            i += 1
            continue
        break
    if not saw:
        return None, i
    return total + current, i


def fmt_num(n: float) -> str:
    if abs(n) >= 1_000_000_000_000:
        return f"{n / 1_000_000_000_000:.2f}".rstrip("0").rstrip(".") + "tn"
    if abs(n) >= 1_000_000_000:
        v = n / 1_000_000_000
        return f"{v:.2f}".rstrip("0").rstrip(".") + "bn"
    if abs(n) >= 1_000_000 and n >= 100_000:
        return f"{n / 1_000_000:.1f}".rstrip("0").rstrip(".") + "m"
    if abs(n - round(n)) < 0.001:
        return f"{int(round(n)):,}"
    return f"{n:.2f}".rstrip("0").rstrip(".")


def spoken_to_digits(text: str) -> str:
    """Digitize spoken numbers and keep commas, apostrophes, and other punctuation."""
    text = re.sub(r"(?<=[A-Za-z])-(?=[A-Za-z])", " ", text)
    for spoken, year in (
        ("twenty twenty six", "2026"),
        ("twenty twenty four", "2024"),
        ("twenty twenty three", "2023"),
        ("twenty nineteen", "2019"),
        ("twenty fifteen", "2015"),
        ("twenty ten", "2010"),
        ("nineteen ninety six", "1996"),
    ):
        text = re.sub(rf"\b{spoken}\b", year, text, flags=re.I)
    tokens = re.findall(r"\s+|[0-9]+(?:\.[0-9]+)?|[\w'’&]+|[^\s\w]", text, flags=re.UNICODE)
    words: list[str] = []
    word_at: list[int] = []
    for i, tok in enumerate(tokens):
        if re.match(r"[0-9\w]", tok):
            words.append(tok)
            word_at.append(i)
    replace: dict[int, tuple[int, str]] = {}
    i = 0
    while i < len(words):
        val, j = consume_number(words, i)
        if val is not None and j > i:
            piece = fmt_num(val)
            nxt = words[j].lower().strip(".,") if j < len(words) else ""
            if nxt == "percent":
                piece = piece + "%"
                j += 1
            elif nxt in ("dollar", "dollars"):
                piece = "$" + piece
                j += 1
            replace[i] = (j, piece)
            i = j
        else:
            i += 1
    out: list[str] = []
    consumed_until = -1
    word_i = 0
    for ti, tok in enumerate(tokens):
        if word_i < len(word_at) and word_at[word_i] == ti:
            if word_i in replace:
                j, piece = replace[word_i]
                out.append(piece)
                consumed_until = j
                word_i += 1
                continue
            if word_i < consumed_until:
                word_i += 1
                continue
            out.append(tok)
            word_i += 1
            continue
        if 0 <= word_i < consumed_until:
            continue
        out.append(tok)
    s = re.sub(r"\s+", " ", "".join(out)).strip()
    return s.replace(" ,", ",").replace(" .", ".")


def sentence(text: str) -> str:
    s = spoken_to_digits(text).strip()
    if not s:
        return ""
    s = s[0].upper() + s[1:]
    if s[-1] not in ".?!":
        s += "."
    return s


def finish_caption(phrase: str) -> str:
    s = spoken_to_digits(phrase).strip()
    s = re.sub(r"\s+", " ", s).strip(" ,;")
    if not s:
        return ""
    if s[0].islower():
        s = s[0].upper() + s[1:]
    if s[-1] not in ".?!":
        s += "."
    return s


def clause_for_scene(sent: str, scene: str) -> str:
    """Keep a short sentence whole. Cut a long one only at a clause boundary."""
    if len(sent.split()) <= 24:
        return sent
    parts = [p.strip() for p in re.split(r"(?<=,)\s+(?=(?:and|but|because|so|then|or|which|while)\b)|;\s+", sent) if p.strip()]
    if len(parts) <= 1:
        return sent
    scene_words = set(re.findall(r"[\w'’]+", scene.lower()))
    best_i, best = 0, -1
    for i, part in enumerate(parts):
        score = len(scene_words & set(re.findall(r"[\w'’]+", part.lower())))
        if score > best:
            best, best_i = score, i
    phrase = parts[best_i]
    lead = phrase.split()[0].lower().strip(",").rstrip("'’") if phrase.split() else ""
    if lead in {"and", "but", "or", "because", "so", "then", "which", "while"} and best_i > 0:
        phrase = parts[best_i - 1].rstrip(".,") + ", " + phrase
    return phrase


def captions_for(rows: list[dict]) -> list[str]:
    """Narration phrase for each scene, cut only at a sentence or clause boundary."""
    pieces = [r["narration_words"].strip() for r in rows]
    text = " ".join(pieces)
    spans: list[tuple[int, int]] = []
    pos = 0
    for piece in pieces:
        start = text.find(piece, pos)
        if start < 0:
            start = pos
        spans.append((start, start + len(piece)))
        pos = start + len(piece)
    sentences = [(m.start(), m.end(), m.group().strip()) for m in re.finditer(r"[^.?!]+(?:[.?!]|$)", text) if m.group().strip()]
    caps: list[str] = []
    for i, (a, b) in enumerate(spans):
        sent = ""
        mid = (a + b) // 2
        for s0, s1, s in sentences:
            if s0 <= mid < s1 or s0 <= a < s1:
                sent = s
                break
        phrase = clause_for_scene(sent or pieces[i], pieces[i])
        caps.append(finish_caption(phrase))
    return caps


def scrub_source_ids(text: str) -> str:
    if not text or not re.search(r"\bS\d{3}\b", text):
        return text
    text = re.sub(r"Source\s+S001\s*[—-]\s*TidyTuesday[^.\n]*", "The 2019 Wikipedia-based dataset", text, flags=re.I)
    text = re.sub(r"\bS001\b", "the 2019 Wikipedia-based dataset", text)
    text = re.sub(r"\bS017\b", "the 2026 Wikipedia list", text)
    text = re.sub(r"\bS\d{3}\b", "", text)
    text = re.sub(r"\s{2,}", " ", text)
    text = re.sub(r"\s+([,.;:])", r"\1", text)
    return text.strip(" -—")


def public_source(narr: str, raw: str) -> str:
    n = narr.lower()
    mentions_2019 = bool(re.search(r"2019|twenty-?nineteen|twenty nineteen", n))
    mentions_2026 = bool(re.search(r"2026|twenty-?twenty-?six|twenty twenty six", n))
    if mentions_2019 and mentions_2026:
        return "The 2019 Wikipedia-based dataset and the 2026 Wikipedia list"
    if mentions_2026:
        return "The 2026 Wikipedia list"
    if any(k in n for k in ("domestic", "top ten", "top-ten", "box office mojo")):
        return "Box Office Mojo yearly charts"
    if any(k in n for k in ("twenty-twenty-four", "2024", "experiences", "fy2024")):
        return "Disney FY2024 report"
    if re.search(r"sec|cheque|acquisition", n):
        return "SEC filings and the 2019 Wikipedia-based dataset"
    return "The 2019 Wikipedia-based dataset"


def first_number(text: str) -> str | None:
    text = re.sub(r"(?<=[A-Za-z])-(?=[A-Za-z])", " ", text)
    words = tokenize(text)
    val, j = consume_number(words, 0)
    # search anywhere
    i = 0
    while i < len(words):
        val, j = consume_number(words, i)
        if val is not None and j > i:
            return fmt_num(val)
        i += 1
    m = re.search(r"\d+(?:\.\d+)?", text)
    return m.group(0) if m else None


def section_for(narr: str, visual: str) -> str:
    n = narr.lower()
    if any(k in n for k in ("merchandise", "licensing", "retail", "box office", "video game", "percent")):
        return "THE MIX"
    if any(k in n for k in ("wikipedia", "2026", "twenty-twenty-six", "vintage", "which year", "pokémon", "pokemon", "quote")):
        return "THE YEAR"
    if any(k in n for k in ("disney", "owner", "warner", "fox", "acquisition", "subsidiary", "cheque", "marvel cost")):
        return "OWNERS"
    if any(k in n for k in ("committee", "licens", "royalt", "park", "flywheel", "advert")):
        return "THE MACHINE"
    if visual == "chart beat":
        return "THE FILE"
    if visual == "type card":
        return "THE SOURCE"
    return "THE FILE"


_FRANCHISE_NEEDLES: list[tuple[str, str]] = []


def set_franchise_needles(franchises: dict[str, dict]) -> None:
    global _FRANCHISE_NEEDLES
    _FRANCHISE_NEEDLES = [(name.lower(), name) for name in franchises]


def entities_in(narr: str) -> list[str]:
    low = narr.lower()
    pairs = list(ALIASES) + list(_FRANCHISE_NEEDLES)
    pairs.sort(key=lambda item: len(item[0]), reverse=True)
    taken: list[tuple[int, int]] = []
    found: list[tuple[int, str]] = []
    for needle, name in pairs:
        pos = low.find(needle)
        if pos < 0:
            continue
        end = pos + len(needle)
        if any(start <= pos and end <= stop for start, stop in taken):
            continue
        # Skip a company alias sitting inside a longer name already claimed.
        taken.append((pos, end))
        if name not in [n for _, n in found]:
            found.append((pos, name))
    found.sort()
    names = [name for _, name in found]
    limit = 4 if {"Game Freak", "Creatures Inc."} <= set(names) else 3
    return names[:limit]


def owner_display(raw: str) -> str:
    text = raw or ""
    if "pokémon company" in text.lower() or "pokemon company" in text.lower():
        return "The Pokémon Company"
    head = text.split("(")[0].strip(" ,")
    return (head or text).strip()[:48]


def disney_consolidated(narr: str) -> bool:
    low = narr.lower()
    return any(k in low for k in ("consolidat", "fold ", "rolled", "subsidiar", "four hundred twenty-six", "426"))


def entity_fact(name: str, narr: str, franchises: dict[str, dict], verified: dict[str, float]) -> dict:
    """A dollar on screen only when verified_numbers assigns it to this name."""
    blank = {"rev": None, "year": "", "owner": "", "role": "", "kind": "none", "name": name}
    if name in COOWNERS:
        return {
            "rev": None,
            "year": "",
            "owner": COOWNERS[name],
            "role": "Not a separate franchise total",
            "kind": "coowner",
            "name": name,
        }
    if name == "The Walt Disney Company":
        key = "Disney consolidated owner total 2019" if disney_consolidated(narr) else "Disney unconsolidated owner total 2019"
        rev = verified_money(verified, key)
        consolidated = key.startswith("Disney consolidated")
        return {
            "rev": rev,
            "year": "2019" if rev is not None else "",
            "owner": "With Marvel, Lucasfilm, Pixar, and Fox" if consolidated else "Unconsolidated label, 2019",
            "role": "Owner total",
            "kind": "owner",
            "name": name,
            "consolidated": consolidated,
        }
    if name in OWNER_VERIFIED:
        key, owner_line, _flag = OWNER_VERIFIED[name]
        rev = verified_money(verified, key)
        return {
            "rev": rev,
            "year": "2019" if rev is not None else "",
            "owner": owner_line,
            "role": "Owner total",
            "kind": "owner",
            "name": name,
            "consolidated": False,
        }
    franchise_name = FRANCHISE_ALIAS.get(name, name)
    if franchise_name in franchises:
        row = franchises[franchise_name]
        verified_key = FRANCHISE_VERIFIED.get(franchise_name)
        rev = verified_money(verified, verified_key) if verified_key else row["rev"]
        if rev is None:
            rev = row["rev"] or None
        since = str(row.get("year") or "")
        media = row.get("media") or "Franchise"
        role = f"{media} · since {since}" if since else media
        return {
            "rev": rev,
            "year": "2019" if rev else "",
            "owner": f"Owner · {owner_display(row.get('owners') or '')}",
            "role": role,
            "kind": "franchise",
            "name": name,
        }
    if name in DEALS:
        key, year, role = DEALS[name]
        rev = verified_money(verified, key)
        return {
            "rev": rev,
            "year": year if rev is not None else "",
            "owner": role,
            "role": role,
            "kind": "deal",
            "name": name,
        }
    return blank


def fact_headline(cards: list[dict]) -> str:
    names = {c["name"] for c in cards}
    shared = bool(names & {"Game Freak", "Creatures Inc."}) or (
        "Nintendo" in names and bool({"The Pokémon Company", "Pokémon"} & names)
    )
    if shared:
        return "Nintendo's own label is $49.0bn. The $90.9bn Pokémon row belongs to The Pokémon Company."
    if "The Pokémon Company" in names and "Nintendo" not in names:
        return "The Pokémon Company is $90.9bn in 2019, owned with Nintendo, Game Freak, and Creatures."
    bits: list[str] = []
    for card in cards:
        rev = card.get("rev")
        if rev is None:
            continue
        fig = money(rev)
        if card.get("kind") == "deal":
            bits.append(f"{card['name']} {card['role'].lower()} is {fig}.")
        elif card.get("kind") == "owner" and card.get("consolidated"):
            bits.append(f"{card['name']} is {fig} after subsidiaries are rolled in.")
        elif card.get("kind") == "owner":
            bits.append(f"{card['name']} is {fig} on its own 2019 label.")
        else:
            bits.append(f"{card['name']} is {fig} in the 2019 file.")
    return " ".join(bits[:2])


HIGHLIGHT_HINTS = [
    ("merchandise", "merchandise"),
    ("licensing", "merchandise"),
    ("box office", "box office"),
    ("video game", "video game"),
    ("manga", "manga"),
    ("hollywood", "us"),
    ("united states", "us"),
    ("japan", "japan"),
    ("lucasfilm", "lucasfilm"),
    ("star wars", "star wars"),
    ("pixar", "pixar"),
    ("marvel", "marvel"),
    ("pokémon", "pokémon"),
    ("pokemon", "pokémon"),
    ("naruto", "naruto"),
    ("call of duty", "call of duty"),
    ("hello kitty", "hello kitty"),
    ("winnie", "winnie"),
    ("candy crush", "candy"),
    ("mortal kombat", "mortal kombat"),
    ("united kingdom", "uk"),
    ("britain", "uk"),
]


def match_label(blob: str, labels: list[str]) -> str:
    low = blob.lower()
    if re.search(r"\bfox\b", low):
        for lab in labels:
            if "fox" in lab.lower():
                return lab
    for needle, hint in HIGHLIGHT_HINTS:
        if needle in low:
            cands = [lab for lab in labels if hint in lab.lower()]
            if cands:
                cands.sort(key=lambda lab: (hint not in lab.lower().split(",")[0].split("/")[0], len(lab)))
                return cands[0]
    for lab in sorted(labels, key=len, reverse=True):
        token = re.split(r"[/(]", lab)[0].strip().lower()
        if len(token) > 3 and token in low:
            return lab
    return ""


def _ranked_labels(labels: list[str], values: list[float]) -> list[str]:
    order = sorted(range(len(labels)), key=lambda i: abs(values[i]) if values else 0, reverse=True)
    return [labels[i] for i in order]


def pick_highlight(narr: str, labels: list[str], values: list[float], focus: list[str], prev_key: str, key: str, prev_hi: str) -> str:
    blob = f"{narr} {' '.join(focus)}"
    hi = match_label(blob, labels)
    same_chart = bool(key and key == prev_key and labels)
    if not hi and same_chart:
        ranked = _ranked_labels(labels, values)
        if prev_hi in ranked:
            hi = ranked[(ranked.index(prev_hi) + 1) % len(ranked)]
        elif ranked:
            hi = ranked[0]
    elif hi and same_chart and hi == prev_hi:
        ranked = _ranked_labels(labels, values)
        if hi in ranked:
            hi = ranked[(ranked.index(hi) + 1) % len(ranked)]
    return hi or ""


def chart_key(asset_file: str, asset_id: str) -> str:
    blob = f"{asset_file} {asset_id}"
    m = re.search(r"chart\d+[a-z]?_[a-z0-9_]+", blob)
    if not m:
        m = re.search(r"(chart\d+[a-z]?_[a-z0-9_]+)", blob)
    if m:
        name = m.group(0)
        if name.startswith("chart_chart"):
            name = name[len("chart_") :]
        return name
    return ""


def diagram_svg(narr: str, prompt: str) -> str:
    blob = f"{narr} {prompt}".lower()
    if any(k in blob for k in ("park", "turnstile", "experiences", "flywheel")):
        return _flywheel()
    if any(k in blob for k in ("aisle", "sku", "plush", "retail", "merchandise")):
        return _sku_stack()
    if any(k in blob for k in ("committee", "publisher", "royalt", "licens", "contract")):
        return _royalty()
    if any(k in blob for k in ("cheque", "acquisition", "deal", "marvel", "lucasfilm", "consolidat")):
        return _rollup()
    if any(k in blob for k in ("premiere", "advert", "sequel", "pipeline")):
        return _pipeline()
    return _royalty()


def _box(x, y, w, h, label, sub=""):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#141414" stroke="#444" stroke-width="2"/>'
        f'<text x="{x + w/2}" y="{y + (36 if not sub else 32)}" text-anchor="middle" fill="#fff" font-size="20">{esc(label)}</text>'
        + (f'<text x="{x + w/2}" y="{y + 58}" text-anchor="middle" fill="#9a9a9a" font-size="14">{esc(sub)}</text>' if sub else "")
    )


def _royalty() -> str:
    return f'''<svg class="diagram-svg" viewBox="0 0 1400 640" xmlns="http://www.w3.org/2000/svg">
      {_box(80, 240, 280, 120, "LICENSOR", "owns the name")}
      {_box(1020, 80, 280, 100, "LICENSEE")}
      {_box(1020, 250, 280, 100, "TOY MAKER")}
      {_box(1020, 420, 280, 100, "PARK / RETAIL")}
      <line class="stage-data" x1="360" y1="300" x2="1020" y2="130" stroke="#E60000" stroke-width="3"/>
      <line class="stage-data" x1="360" y1="300" x2="1020" y2="300" stroke="#E60000" stroke-width="3"/>
      <line class="stage-data" x1="360" y1="300" x2="1020" y2="470" stroke="#0047FF" stroke-width="3"/>
      <text x="640" y="200" fill="#E60000" font-size="18">royalty</text>
      <text x="640" y="280" fill="#E60000" font-size="18">SKU licence</text>
      <text x="640" y="430" fill="#0047FF" font-size="18">gate + shelf</text>
      <circle cx="220" cy="210" r="18" fill="none" stroke="#fff" stroke-width="2"/>
      <line x1="220" y1="228" x2="220" y2="250" stroke="#fff" stroke-width="2"/>
    </svg>'''


def _sku_stack() -> str:
    return f'''<svg class="diagram-svg" viewBox="0 0 1400 640" xmlns="http://www.w3.org/2000/svg">
      {_box(70, 230, 280, 150, "LICENSOR", "owns the name")}
      {_box(540, 230, 280, 150, "LICENCE", "royalty on the SKU")}
      {_box(1010, 80, 300, 130, "TOY AISLE")}
      {_box(1010, 250, 300, 130, "RETAIL SHELF")}
      {_box(1010, 420, 300, 130, "PARK GATE")}
      <line x1="350" y1="305" x2="540" y2="305" stroke="#E60000" stroke-width="3"/>
      <line x1="820" y1="280" x2="1010" y2="145" stroke="#E60000" stroke-width="3"/>
      <line x1="820" y1="305" x2="1010" y2="315" stroke="#E60000" stroke-width="3"/>
      <line x1="820" y1="340" x2="1010" y2="485" stroke="#0047FF" stroke-width="3"/>
      <circle cx="180" cy="190" r="16" fill="none" stroke="#fff" stroke-width="2"/>
      <line x1="180" y1="206" x2="180" y2="228" stroke="#fff" stroke-width="2"/>
    </svg>'''


def _flywheel() -> str:
    return '''<svg class="diagram-svg" viewBox="0 0 1400 640" xmlns="http://www.w3.org/2000/svg">
      <circle cx="700" cy="320" r="210" fill="none" stroke="#333" stroke-width="2"/>
      <circle cx="700" cy="90" r="64" fill="#141414" stroke="#E60000" stroke-width="3"/>
      <circle cx="930" cy="420" r="64" fill="#141414" stroke="#0047FF" stroke-width="3"/>
      <circle cx="470" cy="420" r="64" fill="#141414" stroke="#fff" stroke-width="2"/>
      <text x="700" y="96" text-anchor="middle" fill="#fff" font-size="16">FILM</text>
      <text x="930" y="426" text-anchor="middle" fill="#fff" font-size="16">PARK</text>
      <text x="470" y="426" text-anchor="middle" fill="#fff" font-size="16">SHELF</text>
      <path d="M760 120 C 900 160, 980 280, 960 360" fill="none" stroke="#E60000" stroke-width="3"/>
      <path d="M860 450 C 700 520, 540 480, 500 450" fill="none" stroke="#0047FF" stroke-width="3"/>
      <path d="M500 360 C 520 200, 600 120, 650 110" fill="none" stroke="#fff" stroke-width="3"/>
    </svg>'''


def _rollup() -> str:
    return f'''<svg class="diagram-svg" viewBox="0 0 1400 640" xmlns="http://www.w3.org/2000/svg">
      {_box(80, 80, 240, 90, "MARVEL")}
      {_box(80, 220, 240, 90, "LUCASFILM")}
      {_box(80, 360, 240, 90, "PIXAR")}
      {_box(80, 490, 240, 90, "FOX")}
      {_box(980, 240, 320, 140, "DISNEY", "one owner line")}
      <line x1="320" y1="125" x2="980" y2="280" stroke="#E60000" stroke-width="3"/>
      <line x1="320" y1="265" x2="980" y2="300" stroke="#E60000" stroke-width="3"/>
      <line x1="320" y1="405" x2="980" y2="330" stroke="#0047FF" stroke-width="3"/>
      <line x1="320" y1="535" x2="980" y2="360" stroke="#0047FF" stroke-width="3"/>
    </svg>'''


def _pipeline() -> str:
    return f'''<svg class="diagram-svg" viewBox="0 0 1400 640" xmlns="http://www.w3.org/2000/svg">
      {_box(60, 250, 240, 110, "PREMIERE")}
      {_box(460, 250, 240, 110, "ADVERT")}
      {_box(860, 250, 280, 110, "REPEAT SALE")}
      <line x1="300" y1="305" x2="460" y2="305" stroke="#E60000" stroke-width="3"/>
      <line x1="700" y1="305" x2="860" y2="305" stroke="#0047FF" stroke-width="3"/>
      <rect x="868" y="242" width="264" height="126" fill="none" stroke="#E60000" stroke-width="3"/>
    </svg>'''


def fact_line(narr: str) -> str:
    shown = spoken_to_digits(narr)
    m = re.search(r"(\$?\d[\d,\.]*%?(?:bn|tn|m)?)", shown)
    if not m:
        return ""
    fig = m.group(1)
    tail = shown.split(fig, 1)[1].strip(" .")
    tail = " ".join(tail.split()[:8])
    return f'<span class="fig hot">{esc(fig)}</span> <span class="dm-sans">{esc(tail)}</span>'


def render_bookend(deck_id: str, which: str, label: str) -> str:
    sid = f"{deck_id}-{which}"
    word = "Artometrics"
    return f'''<section class="slide slide-bookend" id="{sid}" data-scene-id="{sid}" data-visual-type="bookend">
      <div class="slide-frame">
        <img class="bookend-logo" src="{LOGO}" alt=""/>
        <p class="bookend-wordmark chomsky">{word}</p>
        <p class="bookend-sub dm-sans">{esc(label)}</p>
      </div>
      <aside class="speaker-notes">{which} bookend</aside>
    </section>'''


def money(rev: float) -> str:
    if rev >= 10:
        return f"${rev:.1f}bn"
    text = f"{rev:.2f}".rstrip("0").rstrip(".")
    return f"${text}bn"


def focus_names(narr: str, last: list[str]) -> list[str]:
    found = entities_in(narr)
    if found:
        return found
    if re.search(r"\b(the same|that name|that row|this name)\b", narr.lower()):
        return last
    return []


def render_row(
    row: dict,
    assets: dict[str, dict],
    franchises: dict[str, dict],
    verified: dict[str, float],
    aspect: str,
    cap: str,
    state: dict,
) -> str:
    sid = row["scene_id"]
    vt = row["visual_type"]
    narr = row["narration_words"]
    section = section_for(narr, vt)
    cap = scrub_source_ids(cap)
    notes = esc(narr)
    focus = focus_names(narr, state.get("last_entities") or [])
    if entities_in(narr):
        state["last_entities"] = entities_in(narr)

    if vt == "chart beat":
        key = chart_key(row.get("asset_file", ""), row.get("asset_id", ""))
        labels, values, _kind = chart_series(key) if key else ([], [], "bar")
        hi = pick_highlight(f"{narr} {cap}", labels, values, focus, state.get("prev_chart", ""), key, state.get("prev_hi", ""))
        head, sub, source, svg = chart_parts(key, hi) if key else (
            "103 franchises in the 2019 Wikipedia-based dataset.",
            "",
            "Source: the 2019 Wikipedia-based dataset",
            "",
        )
        if any(ch.isdigit() for ch in cap) and len(cap) < 180:
            head = cap
        head = scrub_source_ids(head)
        source = scrub_source_ids(source)
        state["prev_chart"] = key
        state["prev_hi"] = hi
        return f'''<section class="slide slide-chart" id="{sid}" data-scene-id="{sid}" data-visual-type="chart beat" data-highlight="{esc(hi)}">
          <div class="slide-frame">
            <p class="section-label dm-mono">{esc(section)}</p>
            <h2 class="headline dm-sans">{esc(head)}</h2>
            <p class="chart-sub dm-mono">{esc(sub)}</p>
            <div class="chart-stage">{svg}</div>
            <p class="chart-source dm-mono">{esc(source)}</p>
            <p class="caption-burn dm-sans">{esc(cap)}</p>
          </div>
          <aside class="speaker-notes">{notes}</aside>
        </section>'''

    state["prev_chart"] = ""
    state["prev_hi"] = ""

    if vt == "big-number card":
        raw = row.get("count_up_number") or narr
        num = first_number(raw) or first_number(narr) or ""
        low = narr.lower()
        count_103 = num.replace(",", "") == "103" and ("franchise" in low or "hundred and three" in low)
        if count_103:
            meaning_short = "franchises in the 2019 Wikipedia-based dataset"
        elif "franchise" in low:
            meaning_short = "franchises in the 2019 Wikipedia-based dataset"
        elif "percent" in low:
            meaning_short = "share of the file"
        elif "billion" in low or "trillion" in low:
            meaning_short = "billion dollars"
        elif "year" in low:
            meaning_short = "years on the clock"
        else:
            meaning_short = "the figure on this beat"
        if "trillion" in low:
            meaning_short = "trillion dollars"
        spoken = sentence(narr)
        if any(ch.isdigit() for ch in cap):
            head = cap
        elif any(ch.isdigit() for ch in spoken):
            head = spoken
        else:
            head = f"{num} {meaning_short}." if num else cap
        head = scrub_source_ids(head)
        narr_num = first_number(narr) or ""
        if narr_num.endswith(("bn", "tn")) and not str(num).endswith(("bn", "tn")):
            num = narr_num
        names = entities_in(narr)
        logo = ""
        if names:
            meta = assets.get(names[0]) or {}
            if meta.get("file"):
                logo = f'<img class="support-logo" src="../{esc(meta["file"])}" alt="{esc(names[0])}"/>'
        file_total_slide = count_103 or num in {"1.52tn", "$1.52tn"} or "trillion" in low
        if count_103:
            support = (
                '<p class="file-total dm-mono">$1.52tn'
                '<span>Lifetime total in the 2019 Wikipedia-based dataset</span></p>'
            )
        elif file_total_slide:
            support = '<p class="context-line dm-sans">Lifetime total in the 2019 Wikipedia-based dataset</p>' + logo
        elif num:
            compare_label, compare_val, compare_w = "File total", "$1.52tn", 100
            this_w = 70
            if "percent" in low:
                compare_label, compare_val, compare_w = "Merchandise", "56%", 100
                try:
                    this_w = max(8, min(100, float(str(num).replace("%", "").replace(",", ""))))
                except ValueError:
                    this_w = 40
            elif num.replace(",", "").isdigit():
                try:
                    this_w = max(8, min(100, int(num.replace(",", "")) / 103 * 100))
                except ValueError:
                    this_w = 60
            support = (
                f'<div class="mini-row dm-mono"><span>This beat</span><div class="mini-track">'
                f'<div class="mini-fill red" style="width:{this_w:.0f}%"></div></div><span class="hot">{esc(num)}</span></div>'
                f'<div class="mini-row dm-mono"><span>{esc(compare_label)}</span><div class="mini-track">'
                f'<div class="mini-fill blue" style="width:{compare_w}%"></div></div><span style="color:#0047FF">{esc(compare_val)}</span></div>'
                f"{logo}"
            )
        else:
            support = logo
        number_html = (
            f'<div class="red-box-target"><span class="count-up dm-mono" data-count-up="{esc(num)}">{esc(num)}</span></div>'
            if num
            else ""
        )
        return f'''<section class="slide slide-bignum" id="{sid}" data-scene-id="{sid}" data-visual-type="big-number card">
          <div class="slide-frame">
            <p class="section-label dm-mono">{esc(section)}</p>
            <h2 class="headline dm-sans">{esc(head)}</h2>
            <div class="stage"><div class="bignum-layout">
              <div class="bignum-wrap">
                {number_html}
                <p class="context-line dm-sans">{esc(meaning_short)}</p>
              </div>
              <div class="support">{support}</div>
            </div></div>
            <p class="caption-burn dm-sans">{esc(cap)}</p>
          </div>
          <aside class="speaker-notes">{notes}</aside>
        </section>'''

    if vt in {"logo", "poster", "official still", "product shot"}:
        names = entities_in(narr)
        if not names and row.get("red_box_target"):
            target = row["red_box_target"].split(".")[0][:48]
            if not re.search(r"\bS\d{3}\b|chart\d", target, re.I):
                names = [target]
        facts = [entity_fact(name, narr, franchises, verified) for name in names]
        poster = vt in {"poster", "official still"}
        cards_html = []
        for fact in facts:
            name = fact["name"]
            meta = assets.get(name) or assets.get(row.get("asset_id", "")) or {}
            src = meta.get("file") or row.get("asset_file") or ""
            rel = f"../{src}" if src else ""
            credit = scrub_source_ids(meta.get("credit_line") or row.get("image_credit") or "")
            fig_html = ""
            if fact.get("rev") is not None:
                fig_html = (
                    f'<p class="entity-fig dm-mono"><span class="hot">{esc(money(fact["rev"]))}</span>'
                    f'<span class="year">{esc(str(fact.get("year") or ""))}</span></p>'
                )
            owner = fact.get("owner") or ""
            role = fact.get("role") or ""
            if owner and role and owner.lower() == role.lower():
                role = ""
            cards_html.append(
                f'''<figure class="entity-card{' poster' if poster else ''}">
                  <img src="{esc(rel)}" alt="{esc(name)}"/>
                  <div class="fact-block">
                    <p class="entity-name dm-sans">{esc(name)}</p>
                    {f'<p class="entity-owner dm-sans">{esc(owner)}</p>' if owner else ''}
                    {fig_html}
                    {f'<p class="entity-role dm-sans">{esc(role)}</p>' if role else ''}
                    <p class="entity-credit dm-mono">{esc(credit)}</p>
                  </div>
                </figure>'''
            )
        head = fact_headline(facts) if facts else ""
        if not head:
            head = cap if any(ch.isdigit() for ch in cap) else "The 2019 Wikipedia-based dataset lists 103 franchises and $1.52tn."
        head = scrub_source_ids(head)
        nclass = f"n{min(len(cards_html), 3)}"
        return f'''<section class="slide slide-entity" id="{sid}" data-scene-id="{sid}" data-visual-type="{esc(vt)}">
          <div class="slide-frame">
            <p class="section-label dm-mono">{esc(section)}</p>
            <h2 class="headline dm-sans">{esc(head)}</h2>
            <div class="stage"><div class="entity-row {nclass}">{''.join(cards_html)}</div></div>
            <p class="caption-burn dm-sans">{esc(cap)}</p>
          </div>
          <aside class="speaker-notes">{notes}</aside>
        </section>'''

    if vt == "type card":
        source = public_source(narr, row.get("image_credit") or "")
        claim = cap
        head = claim if any(ch.isdigit() for ch in claim) else "The 2019 Wikipedia-based dataset lists 103 franchises and $1.52tn."
        head = scrub_source_ids(head)
        return f'''<section class="slide slide-type" id="{sid}" data-scene-id="{sid}" data-visual-type="type card">
          <div class="slide-frame">
            <p class="section-label dm-mono">THE SOURCE</p>
            <h2 class="headline dm-sans">{esc(head)}</h2>
            <div class="stage" style="align-items:flex-start">
              <div>
                <p class="type-quote dm-sans"><span class="red-box-target">{esc(claim)}</span></p>
                <p class="type-source dm-mono">{esc(source)}</p>
              </div>
            </div>
            <p class="caption-burn dm-sans">{esc(cap)}</p>
          </div>
          <aside class="speaker-notes">{notes}</aside>
        </section>'''

    if any(k in narr.lower() for k in ("playground", "photograph", "another room", "cardboard")):
        suffix = "9x16" if aspect == "9x16" else "16x9"
        pid = row.get("asset_id") or "ai25"
        src = f"../assets/ai/{pid}_{suffix}.png"
        head = cap if any(ch.isdigit() for ch in cap) else "103 franchises in the 2019 Wikipedia-based dataset."
        return f'''<section class="slide slide-atmo" id="{sid}" data-scene-id="{sid}" data-visual-type="atmosphere">
          <div class="slide-frame">
            <p class="section-label dm-mono">THE SCENE</p>
            <h2 class="headline dm-sans">{esc(scrub_source_ids(head))}</h2>
            <div class="stage"><div class="ai-stage"><img class="ai-image" src="{esc(src)}" alt=""/></div></div>
            <p class="caption-burn dm-sans">{esc(cap)}</p>
          </div>
          <aside class="speaker-notes">{notes}</aside>
        </section>'''

    svg = diagram_svg(narr, row.get("asset_id", ""))
    if "park" in narr.lower() or "experiences" in narr.lower():
        head_d = "Parks and products are the repeat sale. Merchandise is 56% of the file."
    elif "merchandise" in narr.lower() or "licensing" in narr.lower():
        head_d = cap if any(ch.isdigit() for ch in cap) else "Merchandise, licensing, and retail are the repeat sale."
    elif any(ch.isdigit() for ch in cap):
        head_d = cap
    else:
        head_d = "The licence is the business. Merchandise is 56% of the 2019 file."
    return f'''<section class="slide slide-diagram" id="{sid}" data-scene-id="{sid}" data-visual-type="diagram">
      <div class="slide-frame">
        <p class="section-label dm-mono">THE MACHINE</p>
        <h2 class="headline dm-sans">{esc(scrub_source_ids(head_d))}</h2>
        <div class="stage">{svg}</div>
        <p class="caption-burn dm-sans">{esc(cap)}</p>
      </div>
      <aside class="speaker-notes">{notes}</aside>
    </section>'''


def build(deck_id: str, assets: dict[str, dict], franchises: dict[str, dict], verified: dict[str, float]) -> tuple[Path, int]:
    fname, aspect, label = DECKS[deck_id]
    rows = list(csv.DictReader((VIDEO_DIR / fname).open(encoding="utf-8")))
    caps = captions_for(rows)
    state: dict = {"prev_chart": "", "prev_hi": "", "last_entities": []}
    slides = [render_bookend(deck_id, "open", label)]
    slides += [render_row(r, assets, franchises, verified, aspect, cap, state) for r, cap in zip(rows, caps)]
    slides.append(render_bookend(deck_id, "close", label))
    doc = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/>
<title>Franchise storyboard — {esc(label)}</title>
<link rel="stylesheet" href="deck.css"/>
<script defer src="slide-runtime.js"></script>
</head>
<body class="deck deck-{deck_id} aspect-{aspect}" data-deck="{deck_id}" data-aspect="{aspect}">
{''.join(slides)}
</body></html>'''
    dest = DECK_DIR / f"deck-{deck_id}.html"
    dest.write_text(doc, encoding="utf-8")
    return dest, len(slides)


def audit(deck_id: str) -> list[str]:
    text = (DECK_DIR / f"deck-{deck_id}.html").read_text(encoding="utf-8")
    problems = []
    if re.search(r"\bS\d{3}\b", text):
        problems.append("source id still on screen")
    if re.search(r'class="hot">[—\-–]\s*<', text) or 'data-count-up="—"' in text:
        problems.append("empty figure box")
    if re.search(r"Game Freak is \$90", text) or re.search(r"Creatures Inc\. is \$90", text):
        problems.append("co-owner given the Pokémon total")
    if "$143" in text:
        problems.append("Nintendo substring sum still present")
    return problems


def main() -> int:
    assets = load_assets()
    franchises = load_franchises()
    set_franchise_needles(franchises)
    verified = load_verified()
    targets = sys.argv[1:] or list(DECKS)
    failed = 0
    for deck_id in targets:
        path, n = build(deck_id, assets, franchises, verified)
        problems = audit(deck_id)
        print(f"Wrote {path} ({n} slides)" + (f" AUDIT {problems}" if problems else " audit ok"))
        failed += len(problems)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
