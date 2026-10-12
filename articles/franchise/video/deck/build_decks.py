#!/usr/bin/env python3
"""Build franchise storyboard HTML decks in the Anime explainer layout."""
from __future__ import annotations

import csv
import html
import re
import sys
from collections import Counter
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


def load_visual_map() -> dict[tuple[str, str], dict]:
    path = VIDEO_DIR / "scene_visual_map.csv"
    out: dict[tuple[str, str], dict] = {}
    if not path.exists():
        return out
    for row in csv.DictReader(path.open(encoding="utf-8")):
        out[(row["version"], row["scene_id"])] = row
    return out


def visual_layer(
    deck_id: str,
    sid: str,
    vt: str,
    visuals: dict[tuple[str, str], dict],
    assets: dict[str, dict],
) -> tuple[str, str]:
    """Return (extra classes, layer markup). Headlines and captions stay untouched."""
    vis = visuals.get((deck_id, sid))
    if not vis:
        return "", ""
    kind = (vis.get("layer_type") or "").strip()
    rel = (vis.get("file") or "").strip()
    if not kind or not rel:
        return "", ""
    src = "../" + rel
    logged = assets.get(vis.get("asset_id") or "") or {}
    credit = (logged.get("credit_line") or vis.get("credit") or "").strip()

    if kind == "chart_bg_still":
        return (
            "has-chartbg",
            f'<div class="vis vis-chartbg" data-layer="chart_bg_still">'
            f'<img class="vis-media" src="{esc(src)}" alt=""/></div>',
        )

    if kind == "ai_scene":
        return (
            "has-illust",
            f'<div class="vis vis-illust" data-layer="ai_scene">'
            f'<img class="vis-media" src="{esc(src)}" alt=""/>'
            f'<div class="vis-grade"></div></div>',
        )

    if kind not in {"photo", "footage"}:
        return "", ""

    # Type cards have a single claim and room beside it. Other beats keep
    # the picture full-bleed so the red box, number, and entity row stay put.
    treat = "frame" if vt == "type card" else "bleed"
    if kind == "footage":
        media = (
            f'<video class="vis-media" muted playsinline preload="auto" '
            f'disablepictureinpicture src="{esc(src)}"></video>'
        )
    else:
        media = f'<img class="vis-media" src="{esc(src)}" alt=""/>'
    credit_html = f'<p class="vis-credit dm-mono">{esc(credit)}</p>' if credit else ""
    return (
        f"has-{treat} layer-{kind}",
        f'<div class="vis vis-{treat}" data-layer="{esc(kind)}">'
        f"{media}<div class=\"vis-grade\"></div>{credit_html}</div>",
    )


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
    figs = classify_figures(text)
    for kind in ("money", "percent", "count", "year"):
        for piece, k in figs:
            if k == kind:
                return piece
    return None


FIG_RE = re.compile(r"\$?\d[\d,]*(?:\.\d+)?(?:bn|tn|m|%)?")


def classify_figures(text: str) -> list[tuple[str, str]]:
    """Figures in reading order, after year phrases are mapped to years."""
    digitized = spoken_to_digits(text or "")
    out: list[tuple[str, str]] = []
    for match in FIG_RE.finditer(digitized):
        raw = match.group(0).rstrip(",")
        if raw.startswith("$"):
            raw = raw[1:]
        if re.fullmatch(r"(?:19|20)\d{2}", raw):
            kind = "year"
        elif raw.endswith("%"):
            kind = "percent"
        elif raw.endswith(("bn", "tn", "m")):
            kind = "money"
        else:
            kind = "count"
        out.append((raw, kind))
    return out


def beat_figure(narr: str, cap: str) -> str:
    """The stat this beat states. A truncated count-up token is not used."""
    narr_figs = classify_figures(narr)
    monies = [(i, p) for i, (p, k) in enumerate(narr_figs) if k == "money"]
    percents = [(i, p) for i, (p, k) in enumerate(narr_figs) if k == "percent"]
    counts = [p for p, k in narr_figs if k == "count"]
    years = [p for p, k in narr_figs if k == "year"]
    if monies:
        money_i, money = monies[0]
        if percents and percents[0][0] < money_i:
            return percents[0][1]
        return money
    if percents:
        return percents[0][1]
    if counts:
        return counts[0]
    cap_figs = classify_figures(cap)
    for kind in ("money", "percent", "count"):
        for piece, k in cap_figs:
            if k == kind:
                return piece
    return years[0] if years else ""


def box_stat(text: str, prefer: str = "") -> str:
    """Wrap the spoken figure so the captured frame shows the red box on it."""
    target = prefer
    if not target:
        for kind in ("money", "percent", "count", "year"):
            for piece, k in classify_figures(text):
                if k == kind and not (k == "count" and piece == "1"):
                    target = piece
                    break
            if target:
                break
    if not target:
        return esc(text)
    match = re.search(r"\$?" + re.escape(target), text)
    if not match:
        return esc(text)
    a, b = match.span()
    return esc(text[:a]) + f'<span class="red-box-target">{esc(text[a:b])}</span>' + esc(text[b:])


def scene_stat(narr: str, cap: str) -> str:
    """Figure this scene is saying, without borrowing a stray count from the caption."""
    figs = classify_figures(narr)
    monies = [(i, p) for i, (p, k) in enumerate(figs) if k == "money"]
    percents = [(i, p) for i, (p, k) in enumerate(figs) if k == "percent"]
    counts = [p for p, k in figs if k == "count" and p != "1"]
    years = [p for p, k in figs if k == "year"]
    if monies:
        money_i, money = monies[0]
        if percents and percents[0][0] < money_i:
            return percents[0][1]
        return money
    if percents:
        return percents[0][1]
    if counts:
        return counts[0]
    for piece, kind in classify_figures(cap):
        if kind in {"money", "percent"}:
            return piece
    return years[0] if years else ""


BLANK_LOGO_FILES = {
    "logo_activision_blizzard.png",
    "logo_angry_birds.png",
    "logo_call_of_duty.png",
    "logo_fast_furious.png",
    "logo_game_freak.png",
    "logo_ghostbusters.png",
    "logo_james_bond.png",
    "logo_lotr.png",
    "logo_lucasfilm.png",
    "logo_pixar.png",
    "logo_shueisha.png",
    "logo_smilegate.png",
    "logo_sony.png",
    "logo_ubisoft.png",
    "logo_universal.png",
    "logo_warner_bros.png",
}


def mark_html(src: str, name: str, extra_class: str = "") -> str:
    """A logo image, or a text wordmark when the file is missing or blank."""
    src = (src or "").split(";")[0].strip()
    base = Path(src).name
    usable = bool(src) and (VIDEO_DIR / src).exists() and base not in BLANK_LOGO_FILES
    if not usable:
        classes = "entity-wordmark dm-sans" + (f" {extra_class}" if extra_class else "")
        return f'<div class="{classes}" role="img" aria-label="{esc(name)}">{esc(name)}</div>'
    classes = extra_class
    attr = f' class="{classes}"' if classes else ""
    return f'<img{attr} src="../{esc(src)}" alt="{esc(name)}"/>'


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
    ("experiences", "experience"),
    ("entertainment", "entertainment"),
    ("sports", "sports"),
    ("mario", "mario"),
    ("simpson", "simpson"),
    ("gundam", "gundam"),
    ("batman", "batman"),
    ("top five", "after fox"),
    ("forty-six point four", "after fox"),
    ("46.4", "after fox"),
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


def pick_highlight(
    narr: str,
    labels: list[str],
    values: list[float],
    focus: list[str],
    prev_key: str,
    key: str,
    prev_hi: str,
    cap: str = "",
) -> str:
    hi = match_label(spoken_to_digits(f"{narr} {' '.join(focus)}"), labels)
    if not hi and cap:
        hi = match_label(spoken_to_digits(cap), labels)
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


# Long deep-dive beats, split only at playback. Joined words equal the storyboard line.
# At 150 words/minute, 10 words is 4.0s, so no step is longer than that.
BUILD_STEPS: dict[str, list[dict]] = {
    "d032": [
        {"words": "What that means: a green light", "box": "a green light"},
        {"words": "that cannot reach a shop or a turnstile", "box": "a shop or a turnstile"},
        {"words": "is leaving most of the file’s money on the table.", "box": "the file’s money"},
    ],
    "d038": [
        {"words": "On the 2026 Wikipedia list, Pokémon reads", "box": "Pokémon", "chart": "Pokémon"},
        {"words": "one hundred thirty point seven billion.", "box": "130.7bn", "chart": "", "stat": "130.7bn", "stat_label": "2026 list"},
    ],
    "d155": [
        {"words": "What that means: do not call a British book", "box": "a British book"},
        {"words": "an American franchise just because a studio in Burbank", "box": "Burbank"},
        {"words": "sells the toys.", "box": "the toys"},
    ],
    "d194": [
        {"words": "Disney paid four billion for Marvel", "box": "4bn", "cards": ["Marvel"]},
        {"words": "and four point zero five billion for Lucasfilm", "box": "4.05bn", "cards": ["Marvel", "Lucasfilm"]},
        {"words": "so that the characters would sit on one balance sheet,", "box": "one balance sheet", "cards": ["Marvel", "Lucasfilm"]},
    ],
    "d199": [
        {"words": "The 2019 row is ninety point nine billion", "box": "90.9bn", "stat": "90.9bn", "stat_label": "2019 row"},
        {"words": "and the 2026 list says one hundred thirty point seven,", "box": "130.7bn", "stat": "130.7bn", "stat_label": "2026 list", "line": "and the 2026 list says 130.7bn,"},
    ],
    "d201": [
        {"words": "A chief executive who wants “the Nintendo number”", "box": "the Nintendo number"},
        {"words": "has to decide whether they mean the forty-nine billion", "box": "49bn", "stat": "49bn", "stat_label": "Nintendo’s own label"},
        {"words": "on Nintendo’s own label,", "box": "Nintendo’s own label", "stat": "49bn", "stat_label": "Nintendo’s own label"},
    ],
}

BUILD_CARDS = {
    "Marvel": ("assets/logo_marvel.png", "Marvel", "$4bn"),
    "Lucasfilm": ("assets/logo_lucasfilm.png", "Lucasfilm", "$4.05bn"),
}


def expand_build_steps(rows: list[dict]) -> list[dict]:
    """Insert visual build steps. Spoken words stay in order and unchanged."""
    out: list[dict] = []
    for row in rows:
        steps = BUILD_STEPS.get(row["scene_id"])
        if not steps:
            out.append(row)
            continue
        joined = " ".join(step["words"] for step in steps)
        if joined != row["narration_words"]:
            raise SystemExit(f"{row['scene_id']} build steps do not match the storyboard line")
        for index, step in enumerate(steps):
            words = step["words"].split()
            if len(words) > 10:
                raise SystemExit(f"{row['scene_id']} step {index + 1} is {len(words)} words")
            child = dict(row)
            child["scene_id"] = row["scene_id"] if index == 0 else f"{row['scene_id']}{chr(ord('b') + index - 1)}"
            child["_layer_id"] = row["scene_id"]
            child["_source_line"] = row["narration_words"]
            child["narration_words"] = step["words"]
            child["_build"] = {"index": index, "steps": steps, "parent": row["scene_id"]}
            out.append(child)
    return out


def _step_line(step: dict) -> str:
    if step.get("line"):
        return step["line"]
    return spoken_to_digits(step["words"]).strip()


def _box_line(line: str, box: str) -> str:
    if not box:
        return esc(line)
    match = re.search(re.escape(box), line)
    if not match:
        digitized = spoken_to_digits(box).strip()
        if digitized and digitized != box:
            match = re.search(re.escape(digitized), line)
    if not match:
        return esc(line)
    a, b = match.span()
    return esc(line[:a]) + f'<span class="red-box-target">{esc(line[a:b])}</span>' + esc(line[b:])


def render_build(
    row: dict,
    aspect: str,
    extra: str,
    layer_html: str,
) -> str:
    spec = row["_build"]
    steps: list[dict] = spec["steps"]
    index = spec["index"]
    sid = row["scene_id"]
    current = steps[index]
    section = section_for(row.get("_source_line") or row["narration_words"], row["visual_type"])
    lines = []
    for i, step in enumerate(steps[: index + 1]):
        line = _step_line(step)
        state = "is-now" if i == index else "is-done"
        box_on_line = i == index and step.get("box") not in {step.get("stat"), step.get("stat_label")}
        body = _box_line(line, step.get("box") or "") if box_on_line else esc(line)
        lines.append(f'<li class="{state} dm-sans">{body}</li>')
    cards_html = ""
    names = current.get("cards") or []
    if names:
        bits = []
        for name in names:
            src, label, fig = BUILD_CARDS[name]
            hot = (current.get("box") or "") in fig
            fig_html = f'<span class="{"hot" if hot else "dim"}">{esc(fig)}</span>'
            bits.append(
                f'<figure class="build-card {"is-now" if hot else "is-done"}">'
                f'{mark_html(src, label)}'
                f'<p class="build-card-name dm-sans">{esc(label)}</p>'
                f'<p class="build-card-fig dm-mono">{fig_html}</p>'
                f'</figure>'
            )
        cards_html = f'<div class="build-cards">{"".join(bits)}</div>'
    stat_html = ""
    if current.get("stat"):
        ordered: list[dict] = []
        for step in steps[: index + 1]:
            if not step.get("stat"):
                continue
            if step is current:
                ordered = [earlier for earlier in ordered if earlier.get("stat") != step.get("stat")]
            elif any(earlier.get("stat") == step.get("stat") for earlier in ordered):
                continue
            ordered.append(step)
        shown = []
        for step in ordered:
            live = step is current
            label = step.get("stat_label") or ""
            number = f'<span class="red-box-target">{esc(step["stat"])}</span>' if live and step.get("box") == step.get("stat") else esc(step["stat"])
            label_html = f'<span class="red-box-target">{esc(label)}</span>' if live and step.get("box") == label else esc(label)
            shown.append(
                f'<div class="build-stat {"is-now" if live else "is-done"}">'
                f'<p class="dm-mono">{number}</p>'
                f'<p class="dm-sans">{label_html}</p>'
                f'</div>'
            )
        stat_html = f'<div class="build-stats">{"".join(shown)}</div>'
    chart_html = ""
    if "chart" in current:
        _head, sub, source, svg = chart_parts("chart10_wiki_2019_vs_2026", current.get("chart") or "")
        chart_html = (
            f'<p class="chart-sub dm-mono">{esc(sub)}</p>'
            f'<div class="chart-stage build-chart">{svg}</div>'
            f'<p class="chart-source dm-mono">{esc(source)}</p>'
        )
    cap = finish_caption(_step_line(current))
    return f'''<section class="slide slide-build {extra}" id="{sid}" data-scene-id="{sid}" data-visual-type="build" data-build="{index + 1}" data-build-of="{len(steps)}">
      <div class="slide-frame">
        {layer_html}
        <p class="section-label dm-mono">{esc(section)}</p>
        <ol class="build-lines">{''.join(lines)}</ol>
        {cards_html}
        {stat_html}
        {chart_html}
        <p class="caption-burn dm-sans">{esc(cap)}</p>
      </div>
      <aside class="speaker-notes">{esc(row["narration_words"])}</aside>
    </section>'''


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
    deck_id: str,
    visuals: dict[tuple[str, str], dict],
) -> str:
    sid = row["scene_id"]
    vt = row["visual_type"]
    narr = row["narration_words"]
    section = section_for(row.get("_source_line") or narr, vt)
    extra, layer_html = visual_layer(deck_id, row.get("_layer_id") or sid, vt, visuals, assets)
    if row.get("_build"):
        spec = row["_build"]
        if vt == "chart beat" and spec["index"] == len(spec["steps"]) - 1:
            key = chart_key(row.get("asset_file", ""), row.get("asset_id", ""))
            labels, values, _kind = chart_series(key) if key else ([], [], "bar")
            source_line = row.get("_source_line") or narr
            hi = pick_highlight(source_line, labels, values, [], state.get("prev_chart", ""), key, state.get("prev_hi", ""), "")
            state["prev_chart"] = key
            state["prev_hi"] = hi
        return render_build(row, aspect, extra, layer_html)
    cap = scrub_source_ids(cap)
    notes = esc(narr)
    focus = focus_names(narr, state.get("last_entities") or [])
    if entities_in(narr):
        state["last_entities"] = entities_in(narr)

    if vt == "chart beat":
        key = chart_key(row.get("asset_file", ""), row.get("asset_id", ""))
        labels, values, _kind = chart_series(key) if key else ([], [], "bar")
        hi = pick_highlight(narr, labels, values, focus, state.get("prev_chart", ""), key, state.get("prev_hi", ""), cap)
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
        return f'''<section class="slide slide-chart {extra}" id="{sid}" data-scene-id="{sid}" data-visual-type="chart beat" data-highlight="{esc(hi)}">
          <div class="slide-frame">
            {layer_html}
            <p class="section-label dm-mono">{esc(section)}</p>
            <h2 class="headline dm-sans">{esc(head) if hi else box_stat(head, scene_stat(narr, head))}</h2>
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
        num = beat_figure(narr, cap)
        low = f"{narr} {cap}".lower()
        count_103 = num.replace(",", "") == "103" and ("franchise" in low or "hundred and three" in low)
        if count_103:
            meaning_short = "franchises in the 2019 Wikipedia-based dataset"
        elif num.endswith("tn"):
            meaning_short = "trillion dollars"
        elif num.endswith("bn"):
            meaning_short = "billion dollars"
        elif num.endswith("%"):
            meaning_short = "share of the file"
        elif re.fullmatch(r"(?:19|20)\d{2}", num or ""):
            meaning_short = "the year on this beat"
        else:
            meaning_short = "the figure on this beat"
        spoken = sentence(narr)
        if any(ch.isdigit() for ch in cap):
            head = cap
        elif any(ch.isdigit() for ch in spoken):
            head = spoken
        else:
            head = f"{num} {meaning_short}." if num else cap
        head = scrub_source_ids(head)
        names = entities_in(narr)
        logo = ""
        if names:
            meta = assets.get(names[0]) or {}
            src = (meta.get("file") or "").split(";")[0].strip()
            if src:
                logo = mark_html(src, names[0], "support-mark")
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
        chars = max(len(num), 1)
        number_html = (
            f'<div class="red-box-target"><span class="count-up dm-mono" style="--chars:{chars}" data-count-up="{esc(num)}">{esc(num)}</span></div>'
            if num
            else ""
        )
        return f'''<section class="slide slide-bignum {extra}" id="{sid}" data-scene-id="{sid}" data-visual-type="big-number card">
          <div class="slide-frame">
            {layer_html}
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
                  {mark_html(src, name)}
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
        return f'''<section class="slide slide-entity {extra}" id="{sid}" data-scene-id="{sid}" data-visual-type="{esc(vt)}">
          <div class="slide-frame">
            {layer_html}
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
        return f'''<section class="slide slide-type {extra}" id="{sid}" data-scene-id="{sid}" data-visual-type="type card">
          <div class="slide-frame">
            {layer_html}
            <p class="section-label dm-mono">THE SOURCE</p>
            <h2 class="headline dm-sans">{esc(head)}</h2>
            <div class="stage" style="align-items:flex-start">
              <div>
                {'' if row.get('_clean_end') else f'<p class="type-quote dm-sans"><span class="red-box-target">{esc(claim)}</span></p>'}
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
        pictured = "" if extra else f'<div class="ai-stage"><img class="ai-image" src="{esc(src)}" alt=""/></div>'
        return f'''<section class="slide slide-atmo {extra}" id="{sid}" data-scene-id="{sid}" data-visual-type="atmosphere">
          <div class="slide-frame">
            {layer_html}
            <p class="section-label dm-mono">THE SCENE</p>
            <h2 class="headline dm-sans">{box_stat(scrub_source_ids(head))}</h2>
            <div class="stage">{pictured}</div>
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
    stage_inner = "" if extra else svg
    return f'''<section class="slide slide-diagram {extra}" id="{sid}" data-scene-id="{sid}" data-visual-type="diagram">
      <div class="slide-frame">
        {layer_html}
        <p class="section-label dm-mono">THE MACHINE</p>
        <h2 class="headline dm-sans">{box_stat(scrub_source_ids(head_d))}</h2>
        <div class="stage">{stage_inner}</div>
        <p class="caption-burn dm-sans">{esc(cap)}</p>
      </div>
      <aside class="speaker-notes">{notes}</aside>
    </section>'''


def build(
    deck_id: str,
    assets: dict[str, dict],
    franchises: dict[str, dict],
    verified: dict[str, float],
    visuals: dict[tuple[str, str], dict],
) -> tuple[Path, int]:
    fname, aspect, label = DECKS[deck_id]
    rows = expand_build_steps(list(csv.DictReader((VIDEO_DIR / fname).open(encoding="utf-8"))))
    if deck_id == "vertical" and rows:
        rows[-1] = dict(rows[-1])
        rows[-1]["_clean_end"] = True
    caps = captions_for(rows)
    state: dict = {"prev_chart": "", "prev_hi": "", "last_entities": []}
    slides = [render_bookend(deck_id, "open", label)]
    slides += [
        render_row(r, assets, franchises, verified, aspect, cap, state, deck_id, visuals)
        for r, cap in zip(rows, caps)
    ]
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
    if "px_trading_cards_p0" in text or "px_cinema_audience_v2" in text:
        problems.append("loose fit still on screen")
    if "playing-cards-king" in text:
        problems.append("playing-card still still wired")
    return problems


def main() -> int:
    assets = load_assets()
    franchises = load_franchises()
    set_franchise_needles(franchises)
    verified = load_verified()
    visuals = load_visual_map()
    counts = Counter(row["layer_type"] for row in visuals.values())
    by_deck: dict[str, Counter] = {}
    for (deck_id, _sid), row in visuals.items():
        by_deck.setdefault(deck_id, Counter())[row["layer_type"]] += 1
    print(f"visual layers {dict(counts)} across {len(visuals)} scenes")
    for deck_id, deck_counts in by_deck.items():
        print(f"  {deck_id}: {dict(deck_counts)}")
    targets = sys.argv[1:] or list(DECKS)
    failed = 0
    for deck_id in targets:
        path, n = build(deck_id, assets, franchises, verified, visuals)
        problems = audit(deck_id)
        print(f"Wrote {path} ({n} slides)" + (f" AUDIT {problems}" if problems else " audit ok"))
        failed += len(problems)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
