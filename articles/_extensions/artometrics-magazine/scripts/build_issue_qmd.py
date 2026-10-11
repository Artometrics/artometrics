#!/usr/bin/env python3
"""Transcribe a published Artometrics blog HTML report into magazine .qmd.

The magazine renders articles/anime/anime.qmd. This helper rebuilds that
file from src/content/blog/anime.md so the words and figures stay the
published ones. It does not paraphrase. Re-run from the repo root:

  python3 articles/_extensions/artometrics-magazine/scripts/build_issue_qmd.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup, Comment, NavigableString, Tag

ROOT = Path(__file__).resolve().parents[4]
BLOG = ROOT / "src/content/blog/anime.md"
SESSION = ROOT / "articles/anime/data/sessionInfo.txt"
OUT = ROOT / "articles/anime/anime.qmd"

PULLS = {
    "research-question": (
        "32 : 1",
        "On television, light-novel adaptations draw a median of 153,184 platform members. Manga adaptations draw 37,500 and original series 4,738, which puts light novels about 32 times ahead of originals.",
    ),
    "studio-league": (
        "4.6%",
        "Their median score is 6.63, and only 4.6% reach 8.0 or higher.",
    ),
    "buried-canon": (
        "6.99",
        "Sequels have a median score of 6.99, against 6.76 for the other 3,373 titles, and 14.8% of them score 8.0 or higher (128 of 867), against 6.5% (218 of 3,373).",
    ),
    "limitations": (
        "11",
        "Limiting the list to TV series and films with no earlier prequel, parent story, or full story of any type leaves 11.",
    ),
}

SIDEBOXES = (
    (
        "This report reads the archive as the record of a production system",
        "Mechanism",
    ),
    (
        "The mechanism is the media mix.",
        "Mechanism",
    ),
    (
        "The pattern is consistent with selection, not with any effect of being a sequel.",
        "Context",
    ),
)


def parse_frontmatter(raw: str) -> tuple[str, str]:
    match = re.match(r"^---\n([\s\S]*?)\n---\n([\s\S]*)$", raw)
    if not match:
        raise SystemExit("blog file has no frontmatter")
    return match.group(1), match.group(2)


def fm_block(fm: str, key: str) -> str:
    folded = re.search(rf"^{key}:\s*>-\s*\n([\s\S]*?)(?=\n[A-Za-z0-9_]+:|\Z)", fm, re.M)
    if folded:
        return re.sub(r"\n\s+", " ", folded.group(1)).strip()
    quoted = re.search(rf'^{key}:\s*"([^"]*)"', fm, re.M)
    if quoted:
        return quoted.group(1).strip()
    plain = re.search(rf"^{key}:\s*(\S.*)$", fm, re.M)
    return plain.group(1).strip() if plain else ""


def fm_list(fm: str, key: str) -> list[str]:
    match = re.search(rf"^{key}:\s*\n((?:\s+-\s+.*\n)*)", fm, re.M)
    if not match:
        return []
    items = []
    for line in match.group(1).splitlines():
        item = re.sub(r'^\s+-\s+"?', "", line).strip().strip('"')
        if item:
            items.append(item)
    return items


def inline(node: Tag) -> str:
    parts: list[str] = []
    for child in node.children:
        if isinstance(child, Comment):
            continue
        if isinstance(child, NavigableString):
            parts.append(str(child).replace("\n", " "))
            continue
        if not isinstance(child, Tag):
            continue
        if child.name == "em":
            parts.append(f"*{inline(child)}*")
        elif child.name == "strong":
            parts.append(f"**{inline(child)}**")
        elif child.name == "code":
            parts.append(f"`{inline(child)}`")
        elif child.name == "a":
            href = child.get("href", "").replace(" ", "%20")
            parts.append(f"[{inline(child)}]({href})")
        elif child.name == "br":
            parts.append(" ")
        else:
            parts.append(inline(child))
    text = "".join(parts)
    text = text.replace("\xa0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def heading(tag: Tag, level: int, extra_class: str = "") -> str:
    ident = tag.get("id") or ""
    classes = extra_class.strip()
    attr = ""
    if ident or classes:
        bits = []
        if ident:
            bits.append(f"#{ident}")
        if classes:
            bits.append(f".{classes}" if not classes.startswith(".") else classes)
        # multiple classes: ".page-break" already, or "page-break unlisted"
        attr_body = []
        if ident:
            attr_body.append(f"#{ident}")
        for cls in classes.split():
            attr_body.append(f".{cls.lstrip('.')}")
        attr = " {" + " ".join(attr_body) + "}"
    return f"{'#' * level} {inline(tag)}{attr}\n"


def image_md(img: Tag, width: str) -> str:
    src = img.get("src", "")
    name = Path(src).name
    if "/charts/" in src:
        path = f"charts/{name}"
    else:
        path = f"assets/{name}"
    alt = (img.get("alt") or "").replace('"', "'")
    # Empty markdown caption so Pandoc does not print the alt as a figure title.
    # The credit line under the image is the published credit.
    return f"![]({path}){{width={width} fig-alt=\"{alt}\"}}\n"


def credit_block(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return ""
    return f"\n::: {{.credit}}\n{text}\n:::\n"


def render_logo(node: Tag) -> str:
    img = node.find("img")
    credit = node.find(class_="art-logo__credit")
    word = node.find(class_="art-wordmark")
    parts = ["\n::: {.logo}\n"]
    if img:
        parts.append(image_md(img, "1.25in"))
    if word:
        parts.append(f"\n**{inline(word)}**\n")
    if credit:
        parts.append(credit_block(inline(credit)))
    parts.append(":::\n")
    return "".join(parts)


def render_person(node: Tag) -> str:
    img = node.find("img")
    name = node.find(class_="art-person__name")
    role = node.find(class_="art-person__role")
    credit = node.find(class_="art-person__credit")
    parts = ["\n::: {.person}\n"]
    if img:
        parts.append(image_md(img, "1.15in"))
    if name:
        parts.append(f"\n**{inline(name)}**\n")
    if role:
        parts.append(f"\n{inline(role)}\n")
    if credit:
        parts.append(credit_block(inline(credit)))
    parts.append(":::\n")
    return "".join(parts)


def render_studio_card(node: Tag) -> str:
    parts = ["\n::: {.studio-card}\n"]
    logo = node.find("img", class_="art-studio-card__logo")
    if logo:
        parts.append(image_md(logo, "1.3in"))
    credit = node.find(class_="art-studio-card__credit")
    if credit:
        parts.append(credit_block(inline(credit)))
    name = node.find(class_="art-studio-card__name")
    if name:
        parts.append(f"\n### {inline(name)}\n")
    facts = node.find("ul", class_="art-studio-card__facts")
    if facts:
        for li in facts.find_all("li", recursive=False):
            label = li.find("span")
            value = li.find("strong")
            if label and value:
                parts.append(f"- {inline(label)} **{inline(value)}**\n")
    sig = node.find(class_="art-studio-card__sig")
    if sig:
        parts.append(f"\n{inline(sig)}\n")
    history = node.find(class_="art-studio-card__history")
    if history:
        parts.append(f"\n{inline(history)}\n")
    league = node.find(class_="art-league-mini__label")
    if league:
        parts.append(f"\n{inline(league)}\n")
    for person in node.find_all(class_="art-person"):
        parts.append(render_person(person))
    parts.append(":::\n")
    return "".join(parts)


def render_title_card(node: Tag) -> str:
    name = node.find(class_="art-title-card__name")
    link = node.find("a", class_="art-title-card__link")
    word = node.find(class_="art-wordmark")
    parts = ["\n::: {.title-card}\n"]
    if name:
        parts.append(f"**{inline(name)}**\n")
    if word:
        parts.append(f"\n{inline(word)}\n")
    if link:
        href = link.get("href", "")
        parts.append(f"\n[{inline(link)}]({href})\n")
    parts.append(":::\n")
    return "".join(parts)


def render_aside(aside: Tag) -> str:
    classes = aside.get("class") or []
    if "art-studio-card" in classes:
        return "\n::: {.side}\n" + render_studio_card(aside) + ":::\n"
    parts: list[str] = []
    for child in aside.children:
        if not isinstance(child, Tag):
            continue
        classes = child.get("class") or []
        if "art-logo-row" in classes:
            for logo in child.find_all(class_="art-logo", recursive=False):
                parts.append(render_logo(logo))
        elif "art-logo" in classes:
            parts.append(render_logo(child))
        elif "art-person" in classes:
            parts.append(render_person(child))
        elif "art-studio-card" in classes:
            parts.append(render_studio_card(child))
        elif "art-title-card" in classes:
            parts.append(render_title_card(child))
    if any("art-title-card" in (c.get("class") or []) for c in aside.find_all(class_="art-title-card")):
        # Title cards are a grid, not a narrow sidebar stacked under a 7-column table.
        return "\n::: {.title-cards}\n" + "".join(parts) + ":::\n"
    return "\n::: {.side}\n" + "".join(parts) + ":::\n"


def render_table(wrapper: Tag) -> str:
    table = wrapper.find("table")
    if table is None:
        return ""
    for comment in table.find_all(string=lambda t: isinstance(t, Comment)):
        comment.extract()
    html = str(table)
    html = re.sub(r"\n{2,}", "\n", html)
    return f"\n\n{html}\n\n"


def render_chart(figure: Tag) -> str:
    caption_el = figure.find("figcaption")
    caption = inline(caption_el) if caption_el else ""
    live = figure.find(class_="art-chart-live")
    alt = (live.get("aria-label") if live else "") or ""
    alt = alt.replace('"', "'")
    source = (live.get("data-source") if live else "") or ""
    fallback = (live.get("data-fallback") if live else "") or ""
    name = Path(fallback).name
    return (
        "\n::: {.chart-page}\n"
        f"![{caption}](charts/{name}){{width=5.85in fig-alt=\"{alt}\"}}\n"
        + credit_block(source)
        + ":::\n"
    )


def maybe_sidebox(text: str, paragraph: str) -> str:
    for prefix, kicker in SIDEBOXES:
        if text.startswith(prefix):
            return f"\n::: {{.sidebox}}\n::: {{.kicker}}\n{kicker}\n:::\n\n{paragraph}\n:::\n"
    return f"\n{paragraph}\n"


def render_copy_blocks(container: Tag, first_para: dict) -> str:
    parts: list[str] = []
    for child in container.children:
        if not isinstance(child, Tag):
            continue
        classes = child.get("class") or []
        if child.name == "p" and "art-h3" in classes:
            parts.append(f"\n### {inline(child)}\n")
        elif child.name == "p":
            text = inline(child)
            md = text
            if not first_para["used"] and "art-h3" not in classes:
                md = text
                first_para["used"] = True
                # The opening paragraph is marked only at the top level, not inside cards.
            parts.append(maybe_sidebox(text, md))
        elif child.name == "div" and "art-table-wrapper" in classes:
            parts.append(render_table(child))
        elif child.name in ("h2", "h3"):
            level = 2 if child.name == "h2" else 3
            parts.append("\n" + heading(child, level))
        elif child.name == "ul":
            parts.append(render_list(child))
    return "".join(parts)


def render_list(ul: Tag) -> str:
    lines = ["\n"]
    for li in ul.find_all("li", recursive=False):
        lines.append(f"- {inline(li)}\n")
    return "".join(lines)


def render_split(div: Tag, first_para: dict) -> str:
    copy = div.find(class_="art-split__copy")
    aside = div.find("aside")
    title_cards = aside and aside.find(class_="art-title-card")
    copy_md = render_copy_blocks(copy, first_para) if copy else ""
    aside_md = render_aside(aside) if aside else ""
    if title_cards:
        # The shortlist table needs the full measure. Title cards sit under it.
        return copy_md + "\n" + aside_md
    return f"\n::: {{.spread}}\n::: {{.copy}}\n{copy_md}\n:::\n{aside_md}:::\n"


def session_block() -> str:
    text = SESSION.read_text(encoding="utf-8")
    lines = text.splitlines()
    keep = []
    for line in lines:
        if line.startswith("R version") or line.startswith("Platform:"):
            keep.append(line)
    # Attached package block, verbatim.
    start = next(i for i, line in enumerate(lines) if line.startswith("other attached packages"))
    end = next(i for i, line in enumerate(lines) if line.startswith("loaded via a namespace"))
    block = lines[start:end]
    scales = next(line for line in lines if "scales_" in line)
    body = "\n".join(keep + [""] + block + ["", scales.strip()])
    return f"\n::: {{.versions}}\nPackage versions recorded in `data/sessionInfo.txt`.\n\n```\n{body}\n```\n:::\n"


def checksum_block(main: Tag) -> str:
    code = main.find("code")
    digest = ""
    for node in main.find_all("code"):
        token = node.get_text(strip=True)
        if re.fullmatch(r"[0-9a-f]{64}", token):
            digest = token
            break
    if not digest:
        raise SystemExit("checksum code element not found")
    return (
        "\n::: {.checksum}\n"
        "Dataset SHA-256\n\n"
        f"`{digest}`\n\n"
        "tidy_anime.csv · TidyTuesday 2019-04-23 · one row per animeID after the studio/genre duplicate rows are collapsed.\n"
        ":::\n"
    )


def build_body(main: Tag) -> str:
    parts: list[str] = []
    first_para = {"used": False}
    children = [c for c in main.children if isinstance(c, Tag)]
    i = 0
    in_single = False
    while i < len(children):
        child = children[i]
        classes = child.get("class") or []
        nxt = children[i + 1] if i + 1 < len(children) else None
        nxt_classes = (nxt.get("class") or []) if isinstance(nxt, Tag) else []

        if child.name == "h2":
            ident = child.get("id") or ""
            if ident in PULLS:
                stat, quote = PULLS[ident]
                parts.append(
                    f"\n::: {{.pullquote}}\n::: {{.stat}}\n{stat}\n:::\n\n{quote}\n:::\n"
                )
            if ident == "data-methods-and-sources":
                parts.append("\n::: {.single}\n")
                in_single = True
                parts.append("\n" + heading(child, 2, "page-break"))
                i += 1
                continue
            if ident == "editors-note" and in_single:
                parts.append(":::\n")
                in_single = False
            if isinstance(nxt, Tag) and "art-chart" in nxt_classes:
                parts.append("\n::: {.chart-page}\n")
                parts.append(heading(child, 2))
                parts.append(render_chart(nxt))
                # render_chart already opens and closes chart-page; close the outer one
                # by not double-wrapping. Rebuild without the inner fences.
                parts.pop()
                parts.append(render_chart(nxt).replace("\n::: {.chart-page}\n", "", 1))
                i += 2
                continue
            parts.append("\n" + heading(child, 2))
            i += 1
            continue

        if child.name == "h3":
            parts.append("\n" + heading(child, 3))
        elif child.name == "p" and "art-p" in classes:
            text = inline(child)
            paragraph = text
            if not first_para["used"]:
                paragraph = f"::: {{.lede}}\n{text}\n:::"
                first_para["used"] = True
            parts.append(maybe_sidebox(text, paragraph))
        elif child.name == "figure" and "art-chart" in classes:
            parts.append(render_chart(child))
            if "chart_reach.png" in str(child):
                parts.append(
                    "\n::: {.pullquote}\n::: {.stat}\n0.74\n:::\n\n"
                    "A rank (Spearman) correlation gives 0.74, and correlating score with the log of member count gives 0.72.\n:::\n"
                )
        elif child.name == "div" and "art-table-wrapper" in classes:
            parts.append(render_table(child))
        elif child.name == "div" and "art-split" in classes:
            parts.append(render_split(child, first_para))
        elif child.name == "section" and "art-back-matter" in classes:
            parts.append(render_back_matter(child))
        elif child.name == "div" and "art-editorial-note" in classes:
            notes = []
            for p in child.find_all("p"):
                notes.append(inline(p))
            parts.append("\n::: {.editors-note}\n" + "\n\n".join(notes) + "\n:::\n")
        elif child.name == "ul":
            parts.append(render_list(child))
        i += 1
    if in_single:
        parts.append(":::\n")
    return "".join(parts)


def render_back_matter(section: Tag) -> str:
    parts = ["\n::: {.single}\n"]
    for child in section.children:
        if not isinstance(child, Tag):
            continue
        if child.name == "h2":
            parts.append("\n" + heading(child, 2, "page-break"))
            parts.append(checksum_block(section))
        elif child.name == "h3":
            ident = child.get("id") or ""
            parts.append("\n" + heading(child, 3))
            if ident == "sources":
                parts.append(session_block())
        elif child.name == "p":
            parts.append(f"\n{inline(child)}\n")
        elif child.name == "ul":
            parts.append(render_list(child))
    parts.append(":::\n")
    return "".join(parts)


def exec_summary(tldr: str, points: list[str]) -> str:
    cards = ["\n::: {.exec-summary}\n", "## Key findings {.unlisted}\n", f"\n{tldr}\n", "\n::: {.cards}\n"]
    for point in points:
        stat, _, label = point.partition(" — ")
        if not label:
            stat, _, label = point.partition(" - ")
        cards.append(f"::: {{.card}}\n::: {{.stat}}\n{stat.strip()}\n:::\n\n{label.strip()}\n:::\n")
    cards.append(":::\n:::\n")
    return "".join(cards)


def yaml_quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def fidelity(main: Tag, qmd: str) -> None:
    def norm(s: str) -> str:
        s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s)
        s = s.replace("*", "").replace("`", "")
        s = s.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
        s = re.sub(r"\{[#.][^}]*\}", "", s)
        s = s.replace("\u00a0", " ")
        s = re.sub(r"\(\s+", "(", s)
        s = re.sub(r"\s+\)", ")", s)
        s = re.sub(r"\s+([,.;:!?])", r"\1", s)
        s = re.sub(r"\s+", " ", s).strip()
        return s

    haystack = norm(qmd)
    missing = []
    for tag in main.find_all(["p", "li", "h2", "h3", "figcaption", "td", "th"]):
        if tag.find_parent(class_="art-league-mini__track"):
            continue
        text = norm(tag.get_text(" ", strip=True))
        if len(text) < 2:
            continue
        if text not in haystack:
            missing.append(text[:180])
    if missing:
        print(f"FIDELITY: {len(missing)} snippets missing from qmd", file=sys.stderr)
        for item in missing[:12]:
            print(" -", item, file=sys.stderr)
        debug = ROOT / "articles/anime/anime.qmd.fidelity-debug.txt"
        debug.write_text("\n\n".join(missing), encoding="utf-8")
        raise SystemExit(1)
    print("fidelity ok")


def main() -> None:
    raw = BLOG.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(raw)
    title = fm_block(fm, "title")
    description = fm_block(fm, "description")
    tldr = fm_block(fm, "tldr")
    points = fm_list(fm, "keyPoints")
    if len(points) != 5:
        raise SystemExit(f"expected 5 keyPoints, found {len(points)}")
    soup = BeautifulSoup(body, "html.parser")
    main_el = soup.find("main")
    if main_el is None:
        raise SystemExit("no <main> in blog body")
    article = build_body(main_el)
    # The back-matter section is inside main and also walked if we don't skip it.
    # build_body handles the section tag. Good.
    qmd = f"""---
title: {yaml_quote(title)}
subtitle: "What 13,631 titles say about source, studio, and risk"
description: {yaml_quote(description)}
author: "Kyle McAuliffe"
date: 2026-03-31
lang: en
magazine:
  issue: "01"
  kicker: "Arts · Film"
  running: "ANIME"
  hero-stat: "32 : 1"
  hero-label: "Median members, light-novel TV adaptations vs original TV series"
  hero-detail: "153,184 vs 4,738"
  url: "https://artometrics.com/anime/"
---

{exec_summary(tldr, points)}
{article}
"""
    qmd = re.sub(r"\n{3,}", "\n\n", qmd).rstrip() + "\n"
    OUT.write_text(qmd, encoding="utf-8")
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")
    fidelity(main_el, qmd)


if __name__ == "__main__":
    main()
