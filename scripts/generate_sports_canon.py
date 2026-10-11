#!/usr/bin/env python3
"""Generate the first Artometrics sports canon batch.

The batch is intentionally curated: small, sourced from public reference
records, and built around five distinct editorial charts per article.
"""

from __future__ import annotations

import json
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parents[1]
BLOG_DIR = ROOT / "src" / "content" / "blog"
DATA_DIR = ROOT / "public" / "data" / "articles"
IMG_DIR = ROOT / "public" / "images" / "content" / "articles"
PUBLIC = ROOT / "public"
DOCS_DIR = ROOT / "docs"

ART_RED = "#C0392B"
ART_BLUE = "#2C3E6B"
ART_DARK = "#1C1C1E"
ART_MID = "#6B6B6B"
ART_CREAM = "#F2F0EB"
ART_GREY = "#D5D5D5"


def layout(title: str, subtitle: str, *, x_title: str = "", y_title: str = "", height: int = 540):
    return {
        "title": {
            "text": f"<b>{title}<br><span style='color:{ART_RED}'>{subtitle}</span></b>",
            "font": {"family": "DM Sans, Helvetica, sans-serif", "size": 15, "color": ART_DARK},
            "x": 0.5,
            "xanchor": "center",
            # Anchor the two-line title inside the top margin; without this the
            # first line is cropped out of the static PNG export.
            "y": 0.97,
            "yanchor": "top",
            "automargin": True,
        },
        "paper_bgcolor": ART_CREAM,
        "plot_bgcolor": ART_CREAM,
        "font": {"family": "DM Sans, Helvetica, sans-serif", "color": ART_DARK, "size": 12},
        "margin": {"l": 84, "r": 52, "t": 104, "b": 64},
        "height": height,
        "hovermode": "closest",
        "showlegend": False,
        "xaxis": {
            "title": {"text": x_title},
            "showgrid": True,
            "gridcolor": "#DEDAD1",
            "linecolor": ART_MID,
            "tickfont": {"color": ART_MID, "size": 11},
            "zeroline": False,
        },
        "yaxis": {
            "title": {"text": y_title},
            "showgrid": True,
            "gridcolor": "#DEDAD1",
            "linecolor": ART_MID,
            "tickfont": {"color": ART_MID, "size": 11},
            "zeroline": False,
            "automargin": True,
        },
    }


def write_chart(slug: str, chart_id: str, spec: dict):
    path = DATA_DIR / slug / "charts" / f"{chart_id}.plotly.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(spec, separators=(",", ":")))
    # Dual export: interactive JSON + static print PNG (+ standalone HTML).
    try:
        import plotly.graph_objects as go

        fig = go.Figure(data=spec.get("data") or [], layout=spec.get("layout") or {}, skip_invalid=True)
        png_path = IMG_DIR / slug / "charts" / f"{chart_id}.png"
        png_path.parent.mkdir(parents=True, exist_ok=True)
        fig.write_image(str(png_path), width=1200, height=700, scale=2)
        fig.write_html(
            str(path.with_name(f"{chart_id}.html")),
            include_plotlyjs="cdn",
            full_html=True,
            config={"responsive": True, "displayModeBar": False},
        )
    except Exception as exc:  # noqa: BLE001
        print(f"warn: could not dual-export {slug}/{chart_id}: {exc}")


def bar_h(y, x, colors=None, *, name="", hover="<b>%{y}</b><br>Value: %{x}<extra></extra>"):
    trace = {
        "type": "bar",
        "orientation": "h",
        "y": y,
        "x": x,
        "marker": {
            "color": colors or [ART_BLUE] * len(x),
            "line": {"color": ART_DARK, "width": 0.4},
        },
        "hovertemplate": hover,
    }
    if name:
        trace["name"] = name
    return trace


def bar_v(x, y, colors=None, *, name="", hover="<b>%{x}</b><br>Value: %{y}<extra></extra>"):
    trace = {
        "type": "bar",
        "x": x,
        "y": y,
        "marker": {
            "color": colors or [ART_BLUE] * len(y),
            "line": {"color": ART_DARK, "width": 0.4},
        },
        "hovertemplate": hover,
    }
    if name:
        trace["name"] = name
    return trace


def line(x, y, *, color=ART_RED, name="", hover="%{x}<br>%{y}<extra></extra>"):
    trace = {
        "type": "scatter",
        "mode": "lines+markers",
        "x": x,
        "y": y,
        "line": {"color": color, "width": 3},
        "marker": {"size": 8, "color": color},
        "hovertemplate": hover,
    }
    if name:
        trace["name"] = name
    return trace


def scatter(x, y, text, size, color, *, name="", customdata=None, hover="<b>%{text}</b><br>x: %{x}<br>y: %{y}<extra></extra>"):
    trace = {
        "type": "scatter",
        "mode": "markers+text",
        "x": x,
        "y": y,
        "text": text,
        "textposition": "top center",
        "marker": {
            "size": size,
            "color": color,
            "opacity": 0.86,
            "line": {"color": ART_DARK, "width": 0.5},
        },
        "hovertemplate": hover,
    }
    if customdata is not None:
        trace["customdata"] = customdata
    if name:
        trace["name"] = name
    return trace


def chart_html(slug: str, chart_id: str, caption: str, source: str) -> str:
    return (
        '<figure class="art-chart">\n'
        f'  <div class="art-chart-live" data-chart="/data/articles/{slug}/charts/{chart_id}.plotly.json" '
        f'data-fallback="/images/content/articles/{slug}/charts/{chart_id}.png" '
        f'data-source="{source}" role="img" aria-label="{caption}"></div>\n'
        f'  <figcaption class="art-chart-caption">{caption}</figcaption>\n'
        "</figure>"
    )


def facts_html(facts):
    return "\n".join(
        f'  <div class="fact-box"><span class="fact-number">{value}</span><span class="fact-label">{label}</span></div>'
        for value, label in facts
    )


def write_hero(slug: str, title: str, description: str, tags: str) -> None:
    from backfill_report_heroes import render_hero

    render_hero(title, description, tags, PUBLIC / "images/content/articles" / slug / "hero.png")


def article(
    slug: str,
    title: str,
    description: str,
    tags: str,
    toc,
    intro,
    facts,
    context,
    sections,
    conclusion,
    references,
    note,
    source_credit: str,
    *,
    author: str | None = None,
    pub_date: str = "2026-07-01",
    include_toc: bool = True,
    context_heading: str = "DATASET CONTEXT",
):
    tag_list = [t.strip() for t in tags.split(",") if t.strip()]
    tags_yaml = "\n".join(f"  - {t}" for t in tag_list) if tag_list else f"  - {tags}"
    toc_items = "\n".join(f'  <li><a href="#{sid}" id="toc-{sid}">{label}</a></li>' for sid, label in toc)
    body = [
        "---",
        f'title: "{title}"',
        f"slug: {slug}",
    ]
    if author:
        body.append(f"author: {author}")
    body += [
        f"pubDate: {pub_date}",
        f'description: "{description}"',
        f"heroImage: /images/content/articles/{slug}/hero.png",
        "draft: false",
        "tags:",
        tags_yaml,
        "---",
        '<div id="quarto-content">',
    ]
    if include_toc:
        body += [
            '<nav id="TOC" role="doc-toc">',
            '    <h2 id="toc-title">IN THIS REPORT</h2>',
            "  <ul>",
            toc_items,
            "  </ul>",
            "</nav>",
        ]
    body += [
        '<main class="art-article-main">',
        *[f'<p class="art-p">{p}</p>' for p in intro],
        '<h2 id="fast-facts" class="anchored">Fast facts</h2>',
        f'<div class="facts-grid">\n{facts_html(facts)}\n</div>',
        f'<h2 id="dataset-context" class="anchored">{context_heading}</h2>',
        *[f'<p class="art-p">{p}</p>' for p in context],
    ]
    for section in sections:
        body += [
            f'<h2 id="{section["id"]}" class="anchored">{section["title"]}</h2>',
        ]
        if section.get("subtitle"):
            body.append(f'<h3 id="{section["id"]}-look" class="anchored">{section["subtitle"]}</h3>')
        body += [
            chart_html(slug, section["chart"], section["caption"], section.get("source", source_credit)),
            *[f'<p class="art-p">{p}</p>' for p in section["prose"]],
        ]
    body += [
        '<h2 id="conclusion" class="anchored">Conclusion</h2>',
        *[f'<p class="art-p">{p}</p>' for p in conclusion],
        '<h2 id="references" class="anchored">References</h2>',
        *[f"<p>{p}</p>" for p in references],
        '<h2 id="editors-note" class="anchored">Editor\'s note</h2>',
        f'<div class="art-editorial-note"><p><em>{note}</em></p></div>',
        "</main>",
        "</div>",
        "",
    ]
    (BLOG_DIR / f"{slug}.md").write_text("\n".join(body))
    write_hero(slug, title, description, tags)


def yaml_str(value: str) -> str:
    """Double-quoted YAML scalar."""
    return '"' + str(value).replace("\\", "\\\\").replace('"', '\\"') + '"'


def feature(
    slug: str,
    title: str,
    description: str,
    tags: str,
    *,
    author: str,
    pub_date: str,
    standfirst: str,
    lede,
    facts,
    method,
    sections,
    ending,
    ending_heading: str,
    references,
    note,
    source_credit: str,
    tldr: str,
    key_points,
    faq,
    facts_heading: str = "The numbers behind the story",
    method_heading: str = "Data and method",
):
    """Render a long-form magazine feature.

    Unlike `article()`, which pairs each chart with a two-line data read, this
    renderer treats charts as evidence inside continuous narrative sections.
    """
    tag_list = [t.strip() for t in tags.split(",") if t.strip()]
    front = [
        "---",
        f"title: {yaml_str(title)}",
        f"slug: {slug}",
        f"author: {author}",
        f"pubDate: {pub_date}",
        f"description: {yaml_str(description)}",
        f"heroImage: /images/content/articles/{slug}/hero.png",
        "draft: false",
        "tags:",
        *[f"  - {t}" for t in tag_list],
        f"tldr: {yaml_str(tldr)}",
        "keyPoints:",
        *[f"  - {yaml_str(p)}" for p in key_points],
        "faq:",
    ]
    for question, answer in faq:
        front += [f"  - question: {yaml_str(question)}", f"    answer: {yaml_str(answer)}"]
    front.append("---")

    body = front + [
        '<div id="quarto-content">',
        '<main class="art-article-main">',
        f'<p class="art-p art-lede">{standfirst}</p>',
        *[f'<p class="art-p">{p}</p>' for p in lede],
        f'<h2 id="fast-facts" class="anchored">{facts_heading}</h2>',
        f'<div class="facts-grid">\n{facts_html(facts)}\n</div>',
    ]
    for section in sections:
        body.append(f'<h2 id="{section["id"]}" class="anchored">{section["title"]}</h2>')
        chart_at = section.get("chart_after", 1) if section.get("chart") else None
        for index, paragraph in enumerate(section["prose"]):
            if chart_at is not None and index == chart_at:
                body.append(
                    chart_html(slug, section["chart"], section["caption"], section.get("source", source_credit))
                )
            body.append(f'<p class="art-p">{paragraph}</p>')
        if chart_at is not None and chart_at >= len(section["prose"]):
            body.append(chart_html(slug, section["chart"], section["caption"], section.get("source", source_credit)))
        if section.get("pullquote"):
            body.append(f"<blockquote><p>{section['pullquote']}</p></blockquote>")
    body += [
        f'<h2 id="conclusion" class="anchored">{ending_heading}</h2>',
        *[f'<p class="art-p">{p}</p>' for p in ending],
        f'<h2 id="dataset-context" class="anchored">{method_heading}</h2>',
        *[f'<p class="art-p">{p}</p>' for p in method],
        '<h2 id="references" class="anchored">References</h2>',
        *[f"<p>{p}</p>" for p in references],
        '<h2 id="editors-note" class="anchored">Editor\'s note</h2>',
        f'<div class="art-editorial-note"><p><em>{note}</em></p></div>',
        "</main>",
        "</div>",
        "",
    ]
    (BLOG_DIR / f"{slug}.md").write_text("\n".join(body))
    write_hero(slug, title, description, tags)


def yankees():
    slug = "yankees"
    decades = ["1920s", "1930s", "1940s", "1950s", "1960s", "1970s", "1980s", "1990s", "2000s", "2010s", "2020s"]
    titles = [3, 5, 4, 6, 2, 2, 0, 3, 2, 0, 0]
    write_chart(slug, "chart1_banner_clusters", {"data": [bar_v(decades, titles, [ART_RED if v >= 3 else ART_BLUE for v in titles])], "layout": layout("The Yankees did not win evenly", "THE EMPIRE ARRIVED IN CLUSTERS", x_title="Decade", y_title="World Series titles")})

    clubs = ["Athletics", "Red Sox", "Giants", "Dodgers", "Cardinals", "Yankees"]
    club_titles = [9, 9, 8, 7, 11, 27]
    write_chart(slug, "chart2_empire_gap", {"data": [bar_h(clubs, club_titles, [ART_BLUE] * 5 + [ART_RED])], "layout": layout("Baseball's title gap is still enormous", "THE YANKEES ARE A DIFFERENT SCALE", x_title="World Series titles")})

    drought_teams = ["Yankees", "Dodgers pre-2020", "Cubs pre-2016", "Red Sox pre-2004", "White Sox pre-2005"]
    droughts = [15, 31, 108, 86, 88]
    write_chart(slug, "chart3_drought_context", {"data": [bar_h(drought_teams, droughts, [ART_RED] + [ART_BLUE] * 4)], "layout": layout("In the Bronx, 15 years feels like failure", "DROUGHT IS RELATIVE TO EXPECTATION", x_title="Years between titles or active drought")})

    years = [1996, 1998, 1999, 2000, 2003, 2009, 2012, 2017, 2019, 2022, 2024]
    payroll_rank = [1, 2, 1, 1, 1, 1, 1, 2, 3, 3, 2]
    result_score = [4, 4, 4, 4, 2, 4, 1, 2, 2, 1, 2]
    outcomes = ["World Series title", "World Series title", "World Series title", "World Series title", "Pennant, no title", "World Series title", "Early exit", "ALCS loss", "ALCS loss", "Early exit", "Pennant, no title"]
    write_chart(slug, "chart4_money_conversion", {"data": [scatter(years, payroll_rank, [str(y) for y in years], [12 + s * 5 for s in result_score], [ART_RED if s == 4 else ART_BLUE for s in result_score], customdata=outcomes, hover="<b>%{text}</b><br>Payroll rank: %{y}<br>October: %{customdata}<extra></extra>")], "layout": {**layout("Money still buys contention", "BUT IT NO LONGER BUYS OCTOBER CERTAINTY", x_title="Season", y_title="Payroll rank (lower is richer)"), "yaxis": {**layout("", "")["yaxis"], "autorange": "reversed", "title": {"text": "Payroll rank (lower is richer)"}}}})

    eras = ["Ruth/Gehrig", "DiMaggio", "Mantle", "Steinbrenner I", "Core Four", "Post-2009"]
    pennants = [7, 10, 9, 4, 6, 1]
    rings = [4, 8, 5, 2, 5, 0]
    write_chart(slug, "chart5_pennant_conversion", {"data": [
        bar_h(eras, pennants, [ART_GREY] * len(eras), name="Pennants", hover="<b>%{y}</b><br>Pennants: %{x}<extra></extra>"),
        bar_h(eras, rings, [ART_RED] * len(eras), name="World Series titles", hover="<b>%{y}</b><br>Titles: %{x}<extra></extra>"),
    ], "layout": {**layout("The machine was built for pennants", "RINGS ARE THE HARDER CONVERSION", x_title="Pennants and titles"), "barmode": "overlay", "showlegend": True, "legend": {"orientation": "h", "x": 0.5, "xanchor": "center", "y": 1.04}}})

    sections = [
        {"id": "banner-clusters", "title": "CHART 1 - BANNER CLUSTERS", "chart": "chart1_banner_clusters", "caption": "World Series titles by decade", "prose": ["The Yankees are remembered as a permanent empire, but the banners arrived in bursts. The 1930s, 1940s, and 1950s did the compounding. Later eras mostly managed the expectation created by that original surplus.", "Hypothesis confirmed: the franchise's identity is not merely winning; it is historical clustering so dense that ordinary contention now reads as decline."]},
        {"id": "empire-gap", "title": "CHART 2 - THE EMPIRE GAP", "chart": "chart2_empire_gap", "caption": "World Series titles compared with other historic MLB franchises", "prose": ["The Yankees do not lead baseball by a normal margin. They sit closer to a separate category: not the best team in a ranking, but the institution that defines the ranking.", "For a baseball obsessive, this is the conversation: whether the Yankees are a team or a standard of measurement."]},
        {"id": "drought-context", "title": "CHART 3 - DROUGHT IS RELATIVE", "chart": "chart3_drought_context", "caption": "Championship droughts in context", "prose": ["A 15-year drought is not historically large. It only feels enormous because Yankee time is compressed. Other franchises waited lifetimes; the Yankees experience a decade and a half as institutional malfunction.", "That emotional gap is measurable: expectation changes the meaning of the same number."]},
        {"id": "money-conversion", "title": "CHART 4 - MONEY AND OCTOBER", "chart": "chart4_money_conversion", "caption": "Payroll rank and postseason outcome markers", "prose": ["The post-1990s Yankees still spend like an empire. What changed is conversion. The payroll rank remains elite; the championship output does not.", "This is the modern front-office problem: capital is necessary, but it is no longer sufficiently rare to guarantee separation."]},
        {"id": "pennant-conversion", "title": "CHART 5 - PENNANTS TO RINGS", "chart": "chart5_pennant_conversion", "caption": "Pennants and World Series titles by Yankee era", "prose": ["The old Yankees converted pennants into titles with terrifying efficiency. The later story is messier: enough appearances to preserve mythology, not enough rings to refresh it.", "The dynasty was not just talent. It was conversion under pressure."]},
    ]
    article(
        slug,
        "YANKEES: The Artometrics of Baseball's Empire",
        "The Yankees are not merely baseball's most decorated franchise. They are the sport's benchmark for expectation, drought, payroll pressure, and historical scale.",
        "atlas, power",
        [("fast-facts", "FAST FACTS"), ("dataset-context", "DATASET CONTEXT")] + [(s["id"], s["title"]) for s in sections] + [("conclusion", "CONCLUSION"), ("references", "REFERENCES"), ("editors-note", "EDITOR'S NOTE")],
        [
            "The New York Yankees are what happens when winning stops being an achievement and becomes an operating requirement. Twenty-seven World Series titles do not merely decorate the franchise; they distort the measurement system around it.",
            "This report tests a simple hypothesis: Yankee exceptionalism is not only the number of championships. It is the mismatch between their historical surplus and the modern difficulty of converting money into October certainty.",
        ],
        [("27", "World Series championships, the most in Major League Baseball"), ("40", "American League pennants, the deepest October archive in the sport"), ("2009", "Most recent World Series title"), ("15", "Active title drought entering 2025"), ("5", "Titles from the Core Four era, 1996-2009"), ("1923", "First Yankee championship, the Ruth-era ignition point")],
        [
            "The charts use curated public-reference records from Baseball Reference, Retrosheet-style season summaries, Lahman historical tables, and widely cited payroll/value rankings. The intent is not to replace a play-by-play model; it is to quantify franchise identity at the institutional scale.",
            "A baseball professional would look for conversion: how money becomes wins, how wins become postseason chances, and how postseason chances become flags. A fan mostly feels the gap between mythology and the current roster. This report puts both conversations on the same page.",
        ],
        sections,
        ["The Yankees are still rich, still relevant, and still structurally advantaged. The data does not say the empire is dead. It says the monopoly on conversion is gone.", "That is the modern Yankee paradox: the franchise remains baseball's reference point even when it is no longer baseball's final boss."],
        ["Baseball Reference. <em>New York Yankees Franchise History</em>.", "Lahman, S. <em>Lahman Baseball Database</em>.", "Forbes. <em>MLB Team Valuations</em>, historical rankings.", "Retrosheet and Baseball Almanac championship/pennant records."],
        "This report uses public historical records and rounded franchise-era summaries. Payroll-rank points are editorial markers, not a complete salary model.",
        "Data: Baseball Reference, Lahman, Retrosheet, Forbes - ARTOMETRICS",
    )


def lakers():
    slug = "lakers"
    decades = ["1940s", "1950s", "1960s", "1970s", "1980s", "1990s", "2000s", "2010s", "2020s"]
    titles = [1, 5, 0, 1, 5, 0, 4, 1, 1]
    write_chart(slug, "chart1_titles_by_decade", {"data": [bar_v(decades, titles, [ART_RED if v >= 4 else ART_BLUE for v in titles])], "layout": layout("Laker history moves in star cycles", "BANNERS ARRIVE WHEN ERAS ALIGN", x_title="Decade", y_title="NBA titles")})

    peers = ["76ers", "Pistons", "Warriors", "Bulls", "Spurs", "Lakers", "Celtics"]
    peer_titles = [3, 3, 7, 6, 5, 17, 18]
    write_chart(slug, "chart2_title_race", {"data": [bar_h(peers, peer_titles, [ART_BLUE] * 5 + [ART_RED, ART_BLUE])], "layout": layout("The NBA title race is a two-name argument", "LAKERS AND CELTICS SET THE CEILING", x_title="Championships")})

    eras = ["Mikan", "West/Wilt", "Showtime", "Shaq/Kobe", "Kobe/Pau", "LeBron/AD"]
    era_titles = [5, 1, 5, 3, 2, 1]
    write_chart(slug, "chart3_star_engines", {"data": [bar_h(eras, era_titles, [ART_RED if v >= 5 else ART_BLUE for v in era_titles])], "layout": layout("The Lakers are a star-delivery system", "EVERY TRUE DYNASTY HAS A FACE", x_title="Titles in era")})

    finals_decades = ["1950s", "1960s", "1970s", "1980s", "1990s", "2000s", "2010s", "2020s"]
    finals = [6, 7, 3, 8, 1, 6, 1, 1]
    write_chart(slug, "chart4_finals_frequency", {"data": [line(finals_decades, finals)], "layout": layout("Los Angeles keeps returning to the final table", "FINALS FREQUENCY IS THE REAL BRAND ASSET", x_title="Decade", y_title="Finals appearances")})

    gap_labels = ["1954-72", "1972-80", "1988-2000", "2002-09", "2010-20"]
    gaps = [18, 8, 12, 7, 10]
    write_chart(slug, "chart5_banner_gaps", {"data": [bar_v(gap_labels, gaps, [ART_RED if v >= 12 else ART_BLUE for v in gaps])], "layout": layout("Even glamour has winter", "THE BRAND SURVIVES THE GAPS", x_title="Title gap", y_title="Years")})

    sections = [
        {"id": "titles-by-decade", "title": "CHART 1 - BANNER CYCLES", "chart": "chart1_titles_by_decade", "caption": "Lakers championships by decade", "prose": ["The Lakers do not win as a smooth institution. They win in eras: Mikan, Showtime, Shaq and Kobe, Kobe and Pau, LeBron and Davis.", "The data confirms the folklore. Los Angeles is not a steady-state winner; it is a machine for converting transcendent stars into concentrated title runs."]},
        {"id": "title-race", "title": "CHART 2 - THE TWO-NAME CEILING", "chart": "chart2_title_race", "caption": "NBA championships by major franchise", "prose": ["The Lakers-Celtics comparison is not sports-talk filler. It is the actual shape of NBA history. Everyone else is fighting for the second tier.", "For an NBA expert, the argument is not whether the Lakers are elite. It is how often glamour can rebuild itself before the market advantage decays."]},
        {"id": "star-engines", "title": "CHART 3 - STAR ENGINES", "chart": "chart3_star_engines", "caption": "Championships by defining Lakers star era", "prose": ["The Lakers' front office product is not simply basketball. It is star gravity. When the right face arrives, the rest of the system suddenly makes sense.", "The risky part is visible too: between stars, the franchise can look ordinary faster than its brand admits."]},
        {"id": "finals-frequency", "title": "CHART 4 - FINAL TABLE FREQUENCY", "chart": "chart4_finals_frequency", "caption": "Finals appearances by decade", "prose": ["Championships are rare, but appearances show institutional access. The Lakers have repeatedly returned to the final table across tactical eras, ownership eras, and league economics.", "That is the real glamour metric: not invincibility, but recurring invitation."]},
        {"id": "banner-gaps", "title": "CHART 5 - WINTER IN LOS ANGELES", "chart": "chart5_banner_gaps", "caption": "Selected gaps between Lakers championships", "prose": ["The Lakers have winters. They just rarely become permanent seasons. The brand's advantage is patience with a recruitment magnet attached.", "The chart is a reminder that even the most glamorous franchise needs the next organizing star."]},
    ]
    article(
        slug,
        "LAKERS: The Artometrics of Basketball Glamour",
        "The Lakers are basketball's glamour machine: a franchise that converts stars, market gravity, and expectation into recurring championship eras.",
        "culture, power",
        [("fast-facts", "FAST FACTS"), ("dataset-context", "DATASET CONTEXT")] + [(s["id"], s["title"]) for s in sections] + [("conclusion", "CONCLUSION"), ("references", "REFERENCES"), ("editors-note", "EDITOR'S NOTE")],
        ["The Los Angeles Lakers are what happens when winning and celebrity become the same operating system. Other teams develop stars. The Lakers absorb them, frame them, and turn them into eras.", "This report tests whether the Laker mystique is sentimental mythology or a measurable structure. The answer is both: glamour does not guarantee winning, but it repeatedly lowers the cost of becoming relevant again."],
        [("17", "NBA championships in franchise history"), ("32", "Approximate Finals appearances, the league's deepest final-round archive"), ("5", "Titles in the Showtime decade"), ("6", "Defining title eras from Mikan to LeBron/AD"), ("1949", "First championship season"), ("2020", "Most recent championship")],
        ["The report uses public NBA championship records, Basketball Reference franchise histories, and league-reference summaries. Era buckets are editorial groupings around the players and teams most responsible for each title window.", "Professionals would ask how a franchise repeatedly reopens title windows. Fans ask why the jersey seems to summon stars. The charts show the same mechanism from two angles: market gravity plus historical proof."],
        sections,
        ["The Lakers' advantage is not that they avoid decline. It is that decline rarely destroys the recruitment story. The next star can always imagine becoming the next chapter.", "That is why Lakers data looks less like a franchise line and more like a sequence of Hollywood acts: fade-out, casting, title run, repeat."],
        ["Basketball Reference. <em>Los Angeles Lakers Franchise Index</em>.", "NBA.com historical championship records.", "Sports Reference and Basketball Reference Finals appearance summaries."],
        "Finals-appearance counts are rounded to the conventional franchise-history record; era labels are editorial groupings used to clarify the franchise's star-cycle pattern.",
        "Data: Basketball Reference, NBA.com, Sports Reference - ARTOMETRICS",
    )


def cowboys():
    slug = "cowboys"
    eras = ["Landry 1970s", "Aikman 1990s", "Post-1995"]
    super_bowls = [2, 3, 0]
    write_chart(slug, "chart1_titles_by_era", {"data": [bar_h(eras, super_bowls, [ART_BLUE, ART_RED, ART_GREY])], "layout": layout("America's Team stopped winning titles in 1995", "THE BRAND KEPT COMPOUNDING ANYWAY", x_title="Super Bowl wins")})

    teams = ["Chiefs", "Patriots", "Steelers", "49ers", "Eagles", "Cowboys"]
    playoff_wins_since_1996 = [17, 30, 16, 16, 15, 5]
    values = [4.9, 7.4, 5.3, 6.8, 6.6, 10.1]
    write_chart(slug, "chart2_value_vs_playoffs", {"data": [scatter(values, playoff_wins_since_1996, teams, [28, 36, 26, 28, 26, 42], [ART_BLUE, ART_BLUE, ART_BLUE, ART_BLUE, ART_BLUE, ART_RED], hover="%{text}<br>Value: $%{x}B<br>Playoff wins since 1996: %{y}<extra></extra>")], "layout": layout("The Cowboys are the outlier brand", "VALUE AND PLAYOFF OUTPUT DECOUPLED", x_title="Estimated franchise value ($B)", y_title="Playoff wins since 1996")})

    decades = ["1970s", "1980s", "1990s", "2000s", "2010s", "2020s"]
    p_wins = [14, 4, 12, 1, 3, 1]
    write_chart(slug, "chart3_playoff_wins_decade", {"data": [bar_v(decades, p_wins, [ART_RED if v >= 10 else ART_BLUE for v in p_wins])], "layout": layout("The playoff machine shut down", "DALLAS HAS NOT REPLACED ITS OLD OCTOBER ENGINE", x_title="Decade", y_title="Playoff wins")})

    qbs = ["Staubach", "Aikman", "Romo", "Prescott"]
    win_pct = [0.746, 0.570, 0.614, 0.640]
    write_chart(slug, "chart4_qb_eras", {"data": [bar_h(qbs, win_pct, [ART_RED, ART_BLUE, ART_BLUE, ART_BLUE], hover="%{y}<br>Win pct: %{x:.3f}<extra></extra>")], "layout": layout("Quarterback stability was not the problem", "POSTSEASON CONVERSION WAS", x_title="Regular-season win percentage as starter")})

    drought_teams = ["Cowboys", "Dolphins", "Commanders", "Bears", "Jets"]
    drought = [29, 39, 32, 39, 55]
    write_chart(slug, "chart5_conference_drought", {"data": [bar_h(drought_teams, drought, [ART_RED] + [ART_BLUE] * 4)], "layout": layout("The drought is no longer small", "NFC TITLE-GAME ABSENCE HAS BECOME IDENTITY", x_title="Years since last conference championship appearance")})

    sections = [
        {"id": "titles-by-era", "title": "CHART 1 - TITLES BY ERA", "chart": "chart1_titles_by_era", "caption": "Cowboys Super Bowl wins by defining era", "prose": ["The Cowboys' title history is concentrated in two old engines: Landry's 1970s and the Aikman-Smith-Irvin 1990s. Since then, the Super Bowl column is empty.", "The hypothesis is already visible: Dallas did not stop being important when it stopped winning titles. That is precisely the Artometrics problem."]},
        {"id": "value-vs-playoffs", "title": "CHART 2 - BRAND OUTLIER", "chart": "chart2_value_vs_playoffs", "caption": "Estimated franchise value and playoff wins since 1996", "prose": ["The Cowboys are the strangest point in modern football economics: the richest brand with a modest recent playoff archive.", "For a football expert, this is where the conversation gets interesting. The organization is elite at monetizing attention and only average at converting January chances."]},
        {"id": "playoff-machine", "title": "CHART 3 - THE OLD OCTOBER ENGINE", "chart": "chart3_playoff_wins_decade", "caption": "Cowboys playoff wins by decade", "prose": ["The 1970s and 1990s still carry the franchise memory. The decades after do not match the logo's gravity.", "This is not a losing franchise in the ordinary sense. It is a famous franchise whose postseason output no longer fits its public size."]},
        {"id": "qb-eras", "title": "CHART 4 - QUARTERBACK ERA PARADOX", "chart": "chart4_qb_eras", "caption": "Regular-season win percentage by quarterback era", "prose": ["Quarterback competence has not been absent. Romo and Prescott produced enough regular-season winning to keep Dallas nationally relevant.", "The missing variable is conversion: turning stable quarterback play into deep playoff survival."]},
        {"id": "conference-drought", "title": "CHART 5 - THE CONFERENCE WALL", "chart": "chart5_conference_drought", "caption": "Years since selected teams reached a conference championship game", "prose": ["The Cowboys' NFC championship drought now belongs in the same chart as franchises fans instinctively associate with frustration.", "That is the mirror the data holds up: Dallas is not cursed by invisibility. It is cursed by being watched."]},
    ]
    article(
        slug,
        "COWBOYS: The Artometrics of America's Team",
        "The Dallas Cowboys are the NFL's clearest separation between brand value and postseason conversion: a global sports machine with an old championship engine.",
        "atlas, power",
        [("fast-facts", "FAST FACTS"), ("dataset-context", "DATASET CONTEXT")] + [(s["id"], s["title"]) for s in sections] + [("conclusion", "CONCLUSION"), ("references", "REFERENCES"), ("editors-note", "EDITOR'S NOTE")],
        ["The Dallas Cowboys are no longer just a football team. They are a national attention market. Every season begins with disproportionate coverage, disproportionate expectation, and the same question: when does brand gravity become football gravity again?", "This report tests the Cowboys paradox: the most valuable franchise in American sports has not reached a conference championship game since the 1995 season. The data story is not losing. It is non-conversion under maximum visibility."],
        [("5", "Super Bowl championships"), ("1995", "Most recent Super Bowl-winning season"), ("29", "Years since last NFC championship appearance entering 2025"), ("$10B+", "Widely cited estimated franchise value range"), ("3", "Super Bowls from the 1990s Aikman-Smith-Irvin core"), ("0", "Conference championship appearances since the 1995 season")],
        ["The report uses public Pro Football Reference playoff records, Sports Reference franchise summaries, and Forbes-style franchise valuation estimates. Values are rounded because the analysis depends on order of magnitude, not accounting precision.", "A front-office analyst would call this a conversion problem. A Cowboys fan would call it pain. Artometrics treats both as measurable: the gap between attention and January output."],
        sections,
        ["The Cowboys are not a failed sports business. They may be the most successful sports business in America. That is why the football gap is so stark.", "The numbers say America's Team has mastered demand. The unfinished work is turning demand back into postseason supply."],
        ["Pro Football Reference. <em>Dallas Cowboys Franchise Encyclopedia</em>.", "Forbes. <em>NFL Team Valuations</em>, recent estimates.", "Sports Reference playoff and quarterback starter records.", "NFL historical postseason records."],
        "Franchise values are rounded public estimates. Quarterback win percentages are conventional starter-record summaries and should be interpreted as era indicators, not individual value models.",
        "Data: Pro Football Reference, NFL records, Forbes - ARTOMETRICS",
    )


def celtics():
    slug = "celtics"
    decades = ["1950s", "1960s", "1970s", "1980s", "1990s", "2000s", "2010s", "2020s"]
    titles = [3, 9, 2, 3, 0, 1, 0, 1]
    write_chart(slug, "chart1_banner_density", {"data": [bar_v(decades, titles, [ART_RED if v >= 3 else ART_BLUE for v in titles])], "layout": layout("Boston built the NBA's first title factory", "THE 1960s STILL DISTORT THE SCALE", x_title="Decade", y_title="NBA titles")})

    peers = ["76ers", "Pistons", "Warriors", "Bulls", "Spurs", "Lakers", "Celtics"]
    peer_titles = [3, 3, 7, 6, 5, 17, 18]
    write_chart(slug, "chart2_title_ceiling", {"data": [bar_h(peers, peer_titles, [ART_BLUE] * 6 + [ART_RED])], "layout": layout("The Celtics sit at the NBA ceiling", "BOSTON'S LEAD IS INSTITUTIONAL, NOT JUST RECENT", x_title="Championships")})

    eras = ["Russell", "Cowens/Havlicek", "Bird", "Pierce/KG", "Tatum/Brown"]
    finals = [12, 3, 5, 2, 2]
    rings = [11, 2, 3, 1, 1]
    write_chart(slug, "chart3_era_conversion", {"data": [
        bar_h(eras, finals, [ART_GREY] * len(eras), name="Finals appearances", hover="<b>%{y}</b><br>Finals: %{x}<extra></extra>"),
        bar_h(eras, rings, [ART_RED] * len(eras), name="NBA titles", hover="<b>%{y}</b><br>Titles: %{x}<extra></extra>"),
    ], "layout": {**layout("Boston's best eras converted appearances", "THE RUSSELL STANDARD IS UNREPEATABLE", x_title="Finals and titles"), "barmode": "overlay", "showlegend": True, "legend": {"orientation": "h", "x": 0.5, "xanchor": "center", "y": 1.04}}})

    gaps = ["1969-74", "1976-81", "1986-2008", "2008-24"]
    years = [5, 5, 22, 16]
    write_chart(slug, "chart4_drought_pressure", {"data": [bar_v(gaps, years, [ART_BLUE, ART_BLUE, ART_RED, ART_RED])], "layout": layout("Even the Celtics have long winters", "EXPECTATION MAKES GAPS FEEL LOUDER", x_title="Title gap", y_title="Years")})

    teams = ["Lakers", "Celtics", "Spurs", "Warriors", "Heat", "Bulls"]
    recent_finals = [8, 4, 6, 6, 7, 0]
    recent_titles = [6, 2, 5, 4, 3, 0]
    write_chart(slug, "chart5_modern_access", {"data": [scatter(recent_finals, recent_titles, teams, [28, 26, 28, 30, 28, 18], [ART_BLUE, ART_RED, ART_BLUE, ART_BLUE, ART_BLUE, ART_GREY], hover="%{text}<br>Finals since 1990: %{x}<br>Titles: %{y}<extra></extra>")], "layout": layout("Boston remains in the modern title economy", "ACCESS RETURNED BEFORE THE BANNERS DID", x_title="Finals appearances since 1990", y_title="Titles since 1990")})

    sections = [
        {"id": "banner-density", "title": "CHART 1 - BANNER DENSITY", "chart": "chart1_banner_density", "caption": "Celtics NBA titles by decade", "prose": ["The Celtics' historical lead is not evenly distributed. The 1960s are the gravitational anomaly: a decade so dominant it still defines the franchise's moral economy.", "The hypothesis is that Boston is less a normal contender than an institution built around inherited expectation. The data supports it."]},
        {"id": "title-ceiling", "title": "CHART 2 - TITLE CEILING", "chart": "chart2_title_ceiling", "caption": "NBA championships by major franchise", "prose": ["Boston and Los Angeles form the NBA's summit. Everyone else is explaining distance.", "For a Celtics fan, this is not trivia. It is the operating standard by which every rebuild is judged."]},
        {"id": "era-conversion", "title": "CHART 3 - ERA CONVERSION", "chart": "chart3_era_conversion", "caption": "Finals appearances and titles by Celtics era", "prose": ["The Russell era was not merely successful; it converted nearly every opportunity into a ring. Later eras are great by normal standards and modest by Boston standards.", "This is institutional burden in chart form: greatness becomes smaller when the archive is impossible."]},
        {"id": "drought-pressure", "title": "CHART 4 - DROUGHT PRESSURE", "chart": "chart4_drought_pressure", "caption": "Selected Celtics championship gaps", "prose": ["A 22-year gap from Bird to Pierce/KG shows how long even a privileged franchise can wander. The 2024 title ended another pressure cycle.", "The Celtics do not avoid droughts; they narrate them as temporary violations of the natural order."]},
        {"id": "modern-access", "title": "CHART 5 - MODERN ACCESS", "chart": "chart5_modern_access", "caption": "Modern Finals access and title conversion", "prose": ["Boston has been present in the modern title economy, but not as frequently as its mythology implies. The 2020s core matters because it reopened the institutional pipeline.", "The chart shows the gap between historical identity and contemporary output narrowing again."]},
    ]
    article(
        slug,
        "CELTICS: The Artometrics of Institutional Winning",
        "The Celtics are basketball's clearest example of inherited expectation: a franchise whose 1960s dominance still shapes every modern season.",
        "atlas, power",
        [("fast-facts", "FAST FACTS"), ("dataset-context", "DATASET CONTEXT")] + [(s["id"], s["title"]) for s in sections] + [("conclusion", "CONCLUSION"), ("references", "REFERENCES"), ("editors-note", "EDITOR'S NOTE")],
        ["The Boston Celtics are what happens when a franchise wins so much, so early, that history becomes a front-office department. Every roster is compared not only with its peers, but with ghosts.", "This report tests whether Celtics exceptionalism is still active or mostly archival. The answer is that the archive remains powerful, but the modern team has reopened the claim."],
        [("18", "NBA championships, the league record entering 2025"), ("11", "Titles won during the Bill Russell era"), ("2024", "Most recent championship"), ("22", "Years between the 1986 and 2008 titles"), ("5", "Defining Celtics title eras used in this report"), ("2", "Modern Finals appearances by the Tatum/Brown core through 2024")],
        ["The report uses public NBA championship records, Basketball Reference franchise summaries, and conventional era groupings around the players most responsible for each window.", "An expert fan would ask whether Boston's identity is still earned. An Artometrician asks how historical surplus changes the interpretation of modern results."],
        sections,
        ["The Celtics are not just successful. They are historically overcapitalized: so rich in past winning that even good seasons can feel underleveraged.", "The 2024 title matters because it reconnects the present roster to the institution's oldest claim: Boston is supposed to convert windows into banners."],
        ["Basketball Reference. <em>Boston Celtics Franchise Index</em>.", "NBA.com historical championship records.", "Sports Reference Finals appearance summaries."],
        "Era groupings are editorial simplifications. Counts use conventional public championship and Finals records.",
        "Data: Basketball Reference, NBA.com, Sports Reference - ARTOMETRICS",
    )


def dodgers():
    slug = "dodgers"
    decades = ["1950s", "1960s", "1970s", "1980s", "1990s", "2000s", "2010s", "2020s"]
    pennants = [5, 4, 3, 2, 0, 0, 2, 2]
    write_chart(slug, "chart1_pennant_machine", {"data": [bar_v(decades, pennants, [ART_RED if v >= 3 else ART_BLUE for v in pennants])], "layout": layout("The Dodgers specialize in access", "PENNANTS ARRIVE MORE OFTEN THAN RINGS", x_title="Decade", y_title="NL pennants")})

    clubs = ["Mets", "Braves", "Cubs", "Giants", "Cardinals", "Dodgers", "Yankees"]
    titles = [2, 4, 3, 8, 11, 8, 27]
    write_chart(slug, "chart2_title_context", {"data": [bar_h(clubs, titles, [ART_BLUE] * 5 + [ART_RED, ART_BLUE])], "layout": layout("The Dodgers are elite, not Yankee-scale", "MODERN CONSISTENCY IS THEIR ADVANTAGE", x_title="World Series titles")})

    years = ["2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024"]
    wins = [92, 94, 92, 91, 104, 92, 106, 43, 106, 111, 100, 98]
    write_chart(slug, "chart3_regular_season_floor", {"data": [line(years, wins)], "layout": layout("The modern Dodgers turned 90 wins into a floor", "CONSISTENCY IS THE PRODUCT", x_title="Season", y_title="Regular-season wins")})

    spend_years = [2013, 2015, 2017, 2019, 2021, 2023, 2024]
    payroll_rank = [2, 1, 1, 3, 1, 5, 2]
    october = [1, 1, 3, 1, 2, 0, 4]
    outcomes = ["NLCS", "NLDS exit", "Pennant", "NLDS exit", "NLCS", "NLDS exit", "World Series title"]
    write_chart(slug, "chart4_spending_conversion", {"data": [scatter(spend_years, payroll_rank, [str(y) for y in spend_years], [14 + o * 6 for o in october], [ART_RED if o >= 3 else ART_BLUE for o in october], customdata=outcomes, hover="<b>%{text}</b><br>Payroll rank: %{y}<br>October: %{customdata}<extra></extra>")], "layout": {**layout("Money became infrastructure in Los Angeles", "THE QUESTION IS OCTOBER CONVERSION", x_title="Season", y_title="Payroll rank (lower is richer)"), "yaxis": {**layout("", "")["yaxis"], "autorange": "reversed", "title": {"text": "Payroll rank (lower is richer)"}}}})

    gaps = ["1959-63", "1965-81", "1988-2020", "2020-24"]
    gap_years = [4, 16, 32, 4]
    write_chart(slug, "chart5_ring_gap", {"data": [bar_v(gaps, gap_years, [ART_BLUE, ART_BLUE, ART_RED, ART_BLUE])], "layout": layout("Access does not erase drought", "THE 1988-2020 GAP DEFINED MODERN PRESSURE", x_title="Title gap", y_title="Years")})

    sections = [
        {"id": "pennant-machine", "title": "CHART 1 - PENNANT MACHINE", "chart": "chart1_pennant_machine", "caption": "Dodgers pennants by decade", "prose": ["The Dodgers are built around access: reaching October, reaching the pennant race, repeatedly giving randomness a chance to break their way.", "The hypothesis is that Los Angeles is better understood as a machine for opportunity than as a pure championship machine."]},
        {"id": "title-context", "title": "CHART 2 - TITLE CONTEXT", "chart": "chart2_title_context", "caption": "World Series titles among historic MLB franchises", "prose": ["The Dodgers are historically elite, but not Yankee-scale. Their modern argument rests on consistency: they have made contention feel industrial.", "For a baseball expert, the question is not whether the Dodgers are good. It is whether a high-floor machine can beat postseason variance often enough."]},
        {"id": "regular-season-floor", "title": "CHART 3 - THE 90-WIN FLOOR", "chart": "chart3_regular_season_floor", "caption": "Dodgers regular-season wins in the modern contention era", "prose": ["Since the early 2010s, the Dodgers have made 90-win baseball look normal. That is not normal. It is organizational infrastructure showing up as a line chart.", "The shortened 2020 season interrupts the scale, but not the story: the floor stayed high."]},
        {"id": "spending-conversion", "title": "CHART 4 - SPENDING CONVERSION", "chart": "chart4_spending_conversion", "caption": "Payroll rank and October outcome markers", "prose": ["Los Angeles spends, but the spending is less impulsive than structural: depth, scouting, player development, stars, and injury insurance.", "The contradiction is that postseason baseball can make the best infrastructure look fragile in a five-game sample."]},
        {"id": "ring-gap", "title": "CHART 5 - THE 1988 SHADOW", "chart": "chart5_ring_gap", "caption": "Selected Dodgers championship gaps", "prose": ["The 1988-to-2020 gap is the emotional center of modern Dodger analysis. The team was often good, sometimes excellent, and still ringless.", "That is why the 2020 and 2024 titles matter differently: they validate the machine after decades of access without closure."]},
    ]
    article(
        slug,
        "DODGERS: The Artometrics of Baseball's Modern Machine",
        "The Dodgers are baseball's modern consistency machine: a franchise that turned money, development, and depth into recurring October access.",
        "atlas, power",
        [("fast-facts", "FAST FACTS"), ("dataset-context", "DATASET CONTEXT")] + [(s["id"], s["title"]) for s in sections] + [("conclusion", "CONCLUSION"), ("references", "REFERENCES"), ("editors-note", "EDITOR'S NOTE")],
        ["The Los Angeles Dodgers are the closest thing modern baseball has to an industrial contender. The roster changes, the stars change, the October heartbreak changes shape, but the regular-season floor keeps reappearing.", "This report tests whether the Dodgers are best understood as a dynasty, a spending machine, or something stranger: an access machine designed to survive variance until variance finally cooperates."],
        [("8", "World Series championships in franchise history"), ("25", "Approximate National League pennants"), ("111", "Regular-season wins in 2022"), ("32", "Years between the 1988 and 2020 titles"), ("12", "Straight postseason appearances from 2013 through 2024"), ("2024", "Most recent championship")],
        ["The report uses public Baseball Reference franchise records, Lahman-style season summaries, and widely cited payroll-rank histories. The charts emphasize franchise identity and era structure rather than player-level WAR modeling.", "A professional analyst would focus on depth and conversion. A fan feels the distance between being excellent for six months and surviving October. This report charts that gap."],
        sections,
        ["The Dodgers are not merely rich. They are system-rich: player development, payroll, scouting, and market power working together to keep the contention line high.", "The data says their defining trait is not one championship. It is repeated access to the conditions where championships become possible."],
        ["Baseball Reference. <em>Los Angeles Dodgers Franchise History</em>.", "Lahman, S. <em>Lahman Baseball Database</em>.", "Forbes and public payroll-rank summaries.", "Retrosheet and Baseball Almanac pennant/title records."],
        "Recent win totals and payroll ranks are rounded public-reference summaries. The 2020 shortened season is left unadjusted and interpreted separately in the prose.",
        "Data: Baseball Reference, Lahman, Retrosheet, Forbes - ARTOMETRICS",
    )


def padres():
    """The live page is published from the Quarto source.

    Regenerating it here is what split the page from the .qmd: this function
    wrote a shorter body, and a later paragraph merge then spliced the
    expansion section into the opener. Charts and copy now come from
    articles/padres/.
    """
    qmd = ROOT / "articles" / "padres" / "padres-the-artometrics-of-paying-for-october.qmd"
    if qmd.exists() and "publishBody: true" in qmd.read_text(encoding="utf-8"):
        print("padres: published from the .qmd; skipping the sports-canon rewrite")
        return

    slug = "padres"

    decades = ["1970s", "1980s", "1990s", "2000s", "2010s", "2020s"]
    playoff_apps = [0, 1, 2, 2, 0, 4]
    write_chart(
        slug,
        "chart1_october_scarcity",
        {
            "data": [bar_v(decades, playoff_apps, [ART_RED if v >= 3 else ART_BLUE for v in playoff_apps])],
            "layout": layout(
                "Nine trips to October in 57 seasons",
                "THE 2020s ARE THE FIRST DECADE SAN DIEGO MADE A HABIT OF IT",
                x_title="Decade",
                y_title="Postseason appearances",
            ),
        },
    )

    clubs = [
        "Padres",
        "Brewers",
        "Mariners",
        "Rockies",
        "Rays",
        "Angels",
        "D-backs",
        "Nationals",
        "Rangers",
        "Mets",
        "Royals",
        "Blue Jays",
        "Marlins",
        "Astros",
    ]
    titles = [0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 2]
    write_chart(
        slug,
        "chart2_expansion_peer_gap",
        {
            "data": [
                bar_h(
                    clubs,
                    titles,
                    [ART_RED if c == "Padres" else ART_BLUE for c in clubs],
                    hover="<b>%{y}</b><br>World Series titles: %{x}<extra></extra>",
                )
            ],
            "layout": layout(
                "Nine of the 14 expansion clubs have closed. San Diego has not",
                "THE FOUR OTHERS AT ZERO HAVE NEVER SPENT LIKE THIS",
                x_title="World Series titles won since joining the league",
                height=620,
            ),
        },
    )

    years = ["2019", "2020", "2021", "2022", "2023", "2024", "2025"]
    wins = [70, 37, 79, 89, 82, 93, 90]
    write_chart(
        slug,
        "chart3_star_market_floor",
        {
            "data": [line(years, wins)],
            "layout": layout(
                "The spending raised the floor",
                "FROM 70 WINS IN 2019 TO A 90-WIN HABIT",
                x_title="Season (2020 was a 60-game schedule)",
                y_title="Regular-season wins",
            ),
        },
    )

    spend_years = [2021, 2022, 2023, 2024, 2025, 2026]
    tax_payroll = [216.5, 235.1, 291.2, 227.8, 270.4, 259.1]
    october_depth = [0, 3, 0, 2, 1, 0]
    outcomes = [
        "Missed the playoffs",
        "Beat the Dodgers, lost the NLCS",
        "Missed the playoffs",
        "NLDS Game 5 loss, shut out twice",
        "Wild-card exit, five runs in three games",
        "In progress: 55-53",
    ]
    write_chart(
        slug,
        "chart4_payroll_conversion",
        {
            "data": [
                scatter(
                    spend_years,
                    tax_payroll,
                    [str(y) for y in spend_years],
                    [16 + o * 7 for o in october_depth],
                    [ART_RED if o >= 2 else ART_BLUE for o in october_depth],
                    customdata=outcomes,
                    hover="<b>%{text}</b><br>Tax payroll: $%{y}M<br>October: %{customdata}<extra></extra>",
                )
            ],
            "layout": layout(
                "Six seasons, about $1.5bn of payroll, no pennant",
                "SPENDING BOUGHT ACCESS TO OCTOBER, NOT PASSAGE THROUGH IT",
                x_title="Season",
                y_title="Competitive-balance-tax payroll, $M",
            ),
        },
    )

    gaps = ["1969-84", "1984-98", "1998-2026"]
    gap_years = [15, 14, 28]
    write_chart(
        slug,
        "chart5_pennant_gaps",
        {
            "data": [bar_v(gaps, gap_years, [ART_BLUE, ART_BLUE, ART_RED])],
            "layout": layout(
                "Two pennants, then a generation without one",
                "THE ENTIRE STAR-MARKET ERA FITS INSIDE THE CURRENT WAIT",
                x_title="Years between National League pennants",
                y_title="Years",
            ),
        },
    )

    sections = [
        {
            "id": "october-scarcity",
            "title": "Fifty-seven seasons, nine trips to October",
            "chart": "chart1_october_scarcity",
            "caption": "Padres postseason appearances by decade, 1970s to 2020s",
            "prose": [
                "The scarcity is the part outsiders forget. San Diego joined the National League in 1969 and was bad enough, fast enough, that by 1974 the club had been sold to a buyer who intended to move it to Washington. Topps had already printed baseball cards listing the players as members of a Washington team when Ray Kroc, of McDonald’s, bought the franchise and kept it in San Diego.",
                "What followed was not a franchise so much as a sequence of unconnected good years. The 1984 team, built around Tony Gwynn, Steve Garvey and Goose Gossage, came back from 0-2 against the Cubs to win the pennant, then lost the World Series to Detroit in five games. The 1998 team won 98 games, beat Atlanta, and was swept by a Yankees club that had won 114. The division titles of 2005 and 2006 arrived with 82 and 88 wins, the thinnest credentials the modern West has sent to October.",
                "Nine postseason appearances in 57 seasons, four of them since 2020. That late cluster is not a dynasty forming. It is the first sustained October habit the franchise has ever had, and it arrived only once the club began paying like the teams it was chasing.",
            ],
        },
        {
            "id": "preller-doctrine",
            "title": "The Preller doctrine: buy now, always",
            "chart": "chart3_star_market_floor",
            "chart_after": 2,
            "caption": "Padres regular-season wins, 2019 to 2025",
            "prose": [
                "A.J. Preller has run baseball operations in San Diego since 2014, and his method has never really changed: convert the future into the present, at a premium, repeatedly. The first attempt — the 2015 winter of Matt Kemp, Justin Upton, Wil Myers and James Shields — returned 74 wins and a teardown. The second attempt worked better because it was aimed at stars rather than useful veterans.",
                "Manny Machado signed for 10 years and $300m in 2019, then re-signed for 11 years and $350m in 2023. Fernando Tatis Jr. signed for 14 years and $340m in 2021, the longest contract in the sport at the time. Xander Bogaerts signed for 11 years and $280m. In 2022 Preller sent six players to Washington — a package including James Wood, MacKenzie Gore and CJ Abrams — for Juan Soto, who was still two years from free agency, and then traded Soto to the Yankees sixteen months later.",
                "In the narrow sense, it worked. San Diego went from 70 wins in 2019 to 89 in 2022, 93 in 2024 and 90 in 2025. The floor rose and stayed up. What never arrived was the thing the spending was supposed to buy.",
            ],
        },
        {
            "id": "payroll-conversion",
            "title": "What $1.5bn of payroll bought",
            "chart": "chart4_payroll_conversion",
            "caption": "Padres tax payroll and postseason outcome by season, 2021 to 2026",
            "prose": [
                "Add the past six years of Padres payroll together and the figure is roughly $1.5bn in salary, a top-ten number every season and top-six in three of them. Set that against the October return and the pattern is uncomfortably legible.",
                "2021: a $216m payroll and a September collapse that missed the playoffs outright. 2022: an upset of a 111-win Dodgers team in the division series, then five games and out against Philadelphia. 2023: the largest payroll in club history, $291m, and an 82-80 finish. 2024: 93 wins, a Game 5 loss to Los Angeles in which the offense was shut out over the final two games. 2025: 90 wins, and three games at Wrigley Field in which it scored five runs.",
                "This is the specific way the Padres lose, and it is worth naming precisely, because it is not the same as losing to money. San Diego has bought its way into the highest-variance rounds of a tournament and has then failed, in consecutive seasons, to score in the games that decide them.",
            ],
            "pullquote": "Two straight seasons have ended in a winner-take-all game the offense never turned up for: shut out over the last two games of 2024, five runs across three games in 2025.",
        },
        {
            "id": "expansion-peer-gap",
            "title": "The company San Diego keeps",
            "chart": "chart2_expansion_peer_gap",
            "caption": "World Series titles won by the 14 expansion clubs added since 1961",
            "prose": [
                "Fourteen clubs have joined the major leagues since 1961. Nine have won a World Series. The five that have not are the Padres, Brewers, Mariners, Rockies and Rays.",
                "The other four have an alibi. Tampa Bay and Milwaukee have spent most of their existence in the bottom third of payrolls — the Brewers are 67-40 this season on a $124m Opening Day payroll, which is the thing clubs do instead of spending. Seattle and Colorado have been indifferent or poor for long stretches. San Diego has no such defence. It has the seventh-largest tax payroll in baseball at $259m, three consecutive franchise attendance records, and an empty trophy case.",
                "That is the Artometrics reading of this franchise. Not a small-market club that cannot compete, and not a badly run club that wastes money. A club that has solved demand, solved payroll, and never solved conversion.",
            ],
        },
        {
            "id": "seidler-decade",
            "title": "The Seidler decade, and the bill that came with it",
            "chart": "chart5_pennant_gaps",
            "chart_after": 4,
            "caption": "Gaps between Padres National League pennants",
            "prose": [
                "Peter Seidler became control person after the 2020 season and behaved like a man working against a clock, which he was. He authorised the Tatis, Machado and Bogaerts contracts, absorbed the luxury-tax bills, and told anyone who asked that the point of all of it was a first title. He died in November 2023.",
                "What followed was less romantic. Seidler’s widow, Sheel, sued his brothers Bob and Matt in Texas probate court over their conduct as trustees of the trust that holds the family’s controlling stake; most of the claims were dropped by February. In November 2025 the family retained BDT &amp; MSD to explore a sale. By spring the field was four bidders — Feliciano and Jones, Dan Friedkin, Joe Lacob and Tom Gores — with three bids of at least $3.5bn. Feliciano and Jones won at $3.9bn, and the transfer now waits on 22 of the other 29 owners.",
                "The buyer inherits three things. First, the best-supported baseball audience outside Los Angeles: 3.4m admissions in 2025, second only to the Dodgers; about 42,000 a game this season; 25,000 full-season memberships with a wait list three years old; and 70,000 direct-to-consumer streaming subscribers, more than any club under the league’s local-media umbrella.",
                "Second, $858m of guaranteed money owed after this season to five players — Tatis through 2034, Machado and Bogaerts through 2033, Jackson Merrill through 2034, Jake Cronenworth through 2030. Third, the emptiest farm system in the sport: last of 30 in FanGraphs’ July ranking, and last again in the assessment of the evaluators consulted by the San Diego Union-Tribune, after the 2025 deadline trade that sent Leo De Vries — then among the three or four best prospects in baseball — to the Athletics for the closer Mason Miller.",
                "The franchise’s two pennants are 1984 and 1998. Fourteen years separated them. Twenty-eight years and counting have followed, the longest wait in club history, and the entire modern spending era fits inside it.",
                "The 2026 team is the same argument in miniature. It is 55-53 and third in the West, thirteen games behind a Dodgers club that has won the past two World Series. It has been outscored by 18 runs. Against opponents at .500 or better it is 25-38. It is also, as of this week, on a five-game winning streak and a game and a half out of a wild card — which is precisely the position San Diego has learned to occupy. Close enough to justify buying. Never close enough to be safe.",
            ],
        },
    ]

    feature(
        slug,
        "The Most Expensive Team That Has Never Won Anything",
        "San Diego just agreed to the richest sale in baseball history. The Padres have also never won a World Series. Those two facts belong to the same story.",
        "sports, baseball",
        author="kyle-mcauliffe",
        pub_date="2026-07-31T00:00:00.000Z",
        standfirst="A record $3.9bn says the Padres are one of the most valuable properties in baseball. Fifty-seven seasons say nobody has worked out how to convert it.",
        lede=[
            "On the evening of October 2nd 2025, Fernando Tatis Jr. stood at his locker inside Wrigley Field, red-eyed, and tried to account for a season that had just ended in a 3-1 defeat. He had gone 0-for-4 with three strikeouts. The Padres, who had won 90 games and spent like a superpower to do it, had scored five runs in three games. “It sucks,” Manny Machado said afterwards. “We wanted to be holding up the trophy at the end of the year. We fell short.”",
            "Seven months later the Seidler family signed a definitive agreement to hand the franchise to José E. Feliciano, a co-founder of Clearlake Capital, and his wife, Kwanza Jones, at a valuation of $3.9bn. It is the largest price ever agreed for a Major League Baseball club: $1.48bn more than Steve Cohen paid for the Mets in 2020, and nearly five times the $800m that a group including the late Peter Seidler paid John Moores for the Padres in 2012.",
            "The two events are usually filed separately — one a sporting disappointment, the other a financial triumph. They are the same story. San Diego has discovered that in modern baseball it is possible to build an extraordinarily valuable business out of the pursuit of a championship, and that the pursuit is considerably easier to monetise than the championship itself.",
            "The Padres have played 57 seasons and won none. They are now the most expensive franchise in the history of the sport never to have won anything, and the record price is not in spite of that fact. It is priced around it.",
        ],
        facts=[
            ("$3.9bn", "Agreed sale price, a record for a Major League club"),
            ("0", "World Series titles in 57 seasons"),
            ("2", "National League pennants, in 1984 and 1998"),
            ("28", "Years since the most recent pennant"),
            ("$259M", "2026 tax payroll, seventh-largest in baseball"),
            ("30th", "Farm system rank of 30 clubs, July 2026"),
        ],
        sections=sections,
        ending_heading="What the buyer is actually buying",
        ending=[
            "The Padres are the best-attended unfinished business in American sport. Everything sellable in San Diego has been sold: tickets, sponsorship, streaming subscriptions, and now the franchise itself, at a price no baseball club has ever commanded.",
            "What has not been sold is the outcome. The $3.9bn is a wager that the final piece is still available, and that the version of this team which eventually scores in October is worth materially more than the version that keeps not doing so. Nothing in 57 seasons says that is a bad bet. Nothing in it says the bet is safe.",
            "The companion memo to this report takes the other side of the desk: what the incoming owners inherit, where the balance sheet breaks, and the six moves that would actually buy San Diego a first title.",
        ],
        method=[
            "Season records, win totals and player value figures come from Baseball Reference and are current through games of July 29th 2026. Payroll figures are competitive-balance-tax payrolls as compiled by Spotrac, which is why they differ from Opening Day salary tables. Sale terms, bidder detail and the approval timetable come from MLB.com, Sportico, Sports Business Journal and the San Diego Union-Tribune. Attendance, membership and subscription figures come from the club and SBJ. Farm-system ranks are FanGraphs and Baseball America, July 2026.",
            "The 60-game 2020 season is shown unadjusted and read separately in the prose. Each qualifying season counts as one postseason appearance. Expansion-club counts cover the 14 franchises added to the National and American Leagues since 1961.",
        ],
        references=[
            "Baseball Reference. <em>San Diego Padres Franchise History; 2025 and 2026 season pages</em>.",
            "MLB.com. <em>Padres agree to sell team to Kwanza Jones, José E. Feliciano</em>, May 2026.",
            "Sportico. <em>San Diego Padres Sale: Feliciano, Jones to Pay MLB-Record $3.9 Billion</em>, 2026.",
            "Forbes. <em>Baseball’s Most Valuable Teams 2026</em>, March 2026.",
            "Sports Business Journal. <em>Padres have 70,000 DTC subscribers in record-breaking year</em>, October 2025.",
            "FanGraphs and Baseball America farm-system rankings, July 2026; Spotrac payroll tables.",
            'Related Artometrics reports: <a href="/padres-blueprint">The Padres Cost $3.9 Billion. Winning Will Cost More.</a> · <a href="/dodgers">Dodgers</a> · <a href="/giants">Giants</a> · <a href="/yankees">Yankees</a>.',
        ],
        note="Payroll figures are tax payrolls rather than Opening Day totals; the two series differ by tens of millions of dollars in some seasons. Records and player value figures are current through July 29th 2026, and the 2026 season is unfinished. The sale remains subject to approval by 22 of the other 29 club owners.",
        source_credit="Data: Baseball Reference, Spotrac, Forbes, FanGraphs - ARTOMETRICS",
        tldr="San Diego agreed in May 2026 to sell for $3.9bn, the largest price ever paid for a baseball club. The Padres have played 57 seasons without winning a World Series, have committed about $1.5bn to payroll in six years, and have lost two consecutive winner-take-all games in which the offense all but disappeared. The record price is a wager on the one asset the franchise has never delivered.",
        key_points=[
            "$3.9bn — record agreed sale price, pending a vote of 22 of the other 29 owners",
            "0 titles in 57 seasons — the most valuable franchise never to win anything",
            "$1.5bn — payroll committed across the past six seasons, top-ten every year",
            "5 runs in 3 games — the 2025 wild-card exit at Wrigley Field",
            "$858M — guaranteed money owed to five players after 2026",
            "30th of 30 — farm-system rank after the Leo De Vries trade",
        ],
        faq=[
            (
                "Have the San Diego Padres ever won a World Series?",
                "No. In 57 seasons since their 1969 debut they have won two National League pennants, in 1984 and 1998, and lost both World Series — to Detroit in five games and to the Yankees in a sweep. The 28-year wait since the 1998 flag is the longest in franchise history.",
            ),
            (
                "How much did the Padres sell for, and is the sale final?",
                "The Seidler family agreed in May 2026 to transfer control to a group led by José E. Feliciano and Kwanza Jones at a $3.9bn valuation, a record for a Major League club. The deal still needs approval from 22 of the other 29 owners; final documentation was filed in late July and a vote is expected in August.",
            ),
            (
                "Why has the Padres’ spending not delivered a championship?",
                "Payroll has bought access rather than conversion. San Diego has committed roughly $1.5bn in salary since 2021 and reached the postseason four times in six years, but keeps losing short series: shut out over the last two games of the 2024 division series, and held to five runs across three games in the 2025 wild-card round.",
            ),
            (
                "What condition is the franchise in for a new owner?",
                "Strong on demand, weak on supply. Attendance has set franchise records three years running and the club has the most direct-to-consumer streaming subscribers of any team under MLB’s local-media umbrella, but $858m is owed to five players after 2026 and the farm system ranks last in baseball.",
            ),
        ],
    )


def padres_ownership_blueprint():
    """Long-form buyer's memo: what $3.9bn buys in San Diego, and what to fix first."""
    slug = "padres-blueprint"

    marks = [
        "2012 purchase price",
        "Previous MLB record (Mets, 2020)",
        "Forbes valuation (Mar 2026)",
        "Agreed sale price (2026)",
    ]
    values = [0.80, 2.42, 3.10, 3.90]
    write_chart(
        slug,
        "chart1_franchise_capital",
        {
            "data": [
                bar_h(
                    marks,
                    values,
                    [ART_BLUE, ART_BLUE, ART_GREY, ART_RED],
                    hover="<b>%{y}</b><br>$%{x}B<extra></extra>",
                )
            ],
            "layout": layout(
                "A 26% premium to the published mark, and a new record",
                "SAN DIEGO SOLD FOR NEARLY FIVE TIMES ITS 2012 PRICE",
                x_title="Valuation, $bn",
            ),
        },
    )

    players = ["Cronenworth", "Machado", "Bogaerts", "Merrill", "Tatis Jr.", "Miller", "King"]
    war = [-0.1, 0.8, 1.0, 1.2, 1.6, 2.7, 2.9]
    cheap = {"Miller", "Merrill", "King"}
    write_chart(
        slug,
        "chart2_player_assets",
        {
            "data": [
                bar_h(
                    players,
                    war,
                    [ART_RED if p in cheap else ART_BLUE for p in players],
                    hover="<b>%{y}</b><br>2026 bWAR: %{x}<extra></extra>",
                )
            ],
            "layout": layout(
                "The engine is two pitchers, not the long contracts",
                "2026 WINS ABOVE REPLACEMENT, THROUGH JULY 29TH",
                x_title="2026 Baseball Reference WAR",
            ),
        },
    )

    names = ["Miller", "Cronenworth", "Merrill", "Tatis Jr.", "King", "Bogaerts", "Machado"]
    aav = [4.0, 11.4, 15.0, 24.3, 25.0, 25.5, 31.8]
    war_now = [2.7, -0.1, 1.2, 1.6, 2.9, 1.0, 0.8]
    write_chart(
        slug,
        "chart3_cost_vs_war",
        {
            "data": [
                scatter(
                    aav,
                    war_now,
                    names,
                    [18 + max(w, 0) * 6 for w in war_now],
                    [ART_RED if a <= 25.0 and w >= 1.2 else ART_BLUE for a, w in zip(aav, war_now)],
                    hover="<b>%{text}</b><br>Contract average: $%{x}M a year<br>2026 bWAR: %{y}<extra></extra>",
                )
            ],
            "layout": layout(
                "Championship rosters are built on the gap between cost and value",
                "SAN DIEGO’S SURPLUS SITS IN THREE CONTRACTS",
                x_title="Contract average annual value, $M",
                y_title="2026 Baseball Reference WAR",
            ),
        },
    )

    peers = ["Padres", "Dodgers", "Brewers", "Phillies", "Astros"]
    market = [74, 100, 46, 82, 78]
    payroll = [88, 100, 42, 95, 84]
    controllable_idx = [52, 78, 92, 60, 70]
    farm = [12, 84, 90, 55, 48]
    october = [18, 96, 40, 68, 80]
    write_chart(
        slug,
        "chart4_asset_stack",
        {
            "data": [
                bar_h(peers, market, [ART_GREY] * len(peers), name="Market capital", hover="<b>%{y}</b><br>Market capital: %{x}<extra></extra>"),
                bar_h(peers, payroll, [ART_BLUE] * len(peers), name="Payroll firepower", hover="<b>%{y}</b><br>Payroll firepower: %{x}<extra></extra>"),
                bar_h(peers, controllable_idx, [ART_MID] * len(peers), name="Controllable talent", hover="<b>%{y}</b><br>Controllable talent: %{x}<extra></extra>"),
                bar_h(peers, farm, ["#8E7B67"] * len(peers), name="Farm replenishment", hover="<b>%{y}</b><br>Farm replenishment: %{x}<extra></extra>"),
                bar_h(peers, october, [ART_RED] * len(peers), name="October conversion", hover="<b>%{y}</b><br>October conversion: %{x}<extra></extra>"),
            ],
            "layout": {
                **layout(
                    "Capital and payroll are competitive. Replenishment is not",
                    "THE CHAMPIONSHIP GAP IS STRUCTURAL, NOT COSMETIC",
                    x_title="Editorial championship-asset index (0-100)",
                    height=640,
                ),
                "barmode": "group",
                "showlegend": True,
                "legend": {"orientation": "h", "x": 0.5, "xanchor": "center", "y": 1.08},
                "margin": {"l": 84, "r": 52, "t": 110, "b": 64},
            },
        },
    )

    levers = [
        "Sign another $300M star",
        "Settle baseball governance",
        "Extend Miller, protect Merrill",
        "Rebuild the local media business",
        "Fix the October offense",
        "Buy rotation innings",
        "Refund the pipeline",
    ]
    urgency = [22, 58, 66, 71, 78, 84, 94]
    write_chart(
        slug,
        "chart5_ownership_playbook",
        {
            "data": [
                bar_h(
                    levers,
                    urgency,
                    [ART_RED if u >= 70 else ART_BLUE for u in urgency],
                    hover="<b>%{y}</b><br>Urgency: %{x}<extra></extra>",
                )
            ],
            "layout": layout(
                "The first move is not a signing",
                "WHERE NEW OWNERSHIP SHOULD SPEND ITS FIRST YEAR",
                x_title="Editorial urgency index (higher = close this gap first)",
            ),
        },
    )

    sections = [
        {
            "id": "demand-asset",
            "title": "Asset: demand is not the problem",
            "chart": "chart1_franchise_capital",
            "chart_after": 1,
            "caption": "What the Padres have been worth, 2012 to 2026",
            "prose": [
                "Start with the reason the price was a record. San Diego is the only major-league franchise left in the city, and it behaves like a far larger market than its television rank implies. The club drew 3.4m in 2025, second in baseball behind the Dodgers, and is averaging close to 42,000 a game in 2026. It has set franchise attendance records in three consecutive seasons, holds about 25,000 full-season memberships against a wait list three years old, and renewed 94% of them into 2026 after a 7% price rise.",
                "The valuation ladder tells the same story from the other end. The Fowler-Seidler group paid $800m in 2012. Forbes marked the club at $3.1bn in March, a 59% jump in a year and tenth in the sport. The agreed sale is $3.9bn. Whatever else is wrong here, no one is being asked to create a market.",
                "The underpriced line item is geography. The club’s home television territory includes Tijuana, and no other franchise in the sport has an adjacent metropolitan area of that size with no competing team in it.",
            ],
        },
        {
            "id": "media-liability",
            "title": "Liability: the television hole",
            "prose": [
                "The largest structural problem is not on the field. In May 2023 Diamond Sports stopped paying on a 20-year, $1.2bn contract, and the collapse of Bally Sports San Diego erased more than $60m a year of contracted revenue. MLB has produced and distributed the club’s local telecasts ever since — San Diego was the first team into the league’s local-media portfolio — and reported local media revenue is now in the $20m-$30m range, with industry sources placing it a little higher.",
                "The club has handled the transition better than anyone: 70,000 direct-to-consumer subscribers to Padres.TV, the largest such base under the league’s umbrella, plus ten free over-the-air Saturday games through the local CBS affiliate. ESPN takes in-market streaming rights in 2026 under the league’s new agreement. But the underlying position has not changed. San Diego has been paying a top-seven payroll out of a bottom-tier local media base, and the difference was covered by an owner willing to lose money.",
                "Forbes’ estimate — roughly $20m of operating income on $484m of revenue — is the thesis in one line. The incoming owners are buying a club whose competitive posture depends on a continued appetite for absorbing losses.",
            ],
        },
        {
            "id": "win-engine",
            "title": "Asset: the win engine, and what it costs",
            "chart": "chart2_player_assets",
            "caption": "Padres wins above replacement in 2026, through July 29th",
            "prose": [
                "Now the roster. Through July 29th the most productive Padres by Baseball Reference’s wins above replacement are Michael King at 2.9, Mason Miller at 2.7, Tatis at 1.6, Jackson Merrill at 1.2 and Machado at 0.8.",
                "Miller’s season is an outlier in the sport: a 0.79 earned-run average, 28 saves, 85 strikeouts in 45⅔ innings, an adjusted ERA more than five times the league norm. He is being paid $4m and is under club control through 2029. King is in the first year of a three-year, $75m contract with player options attached, and is the only starter to have held the rotation together through an injury-wrecked summer.",
                "Together those two pitchers have produced 5.6 wins for about $21m of 2026 salary. The five players owed $858m after this season — Tatis, Machado, Bogaerts, Merrill and Cronenworth — have produced 4.5 between them.",
            ],
            "pullquote": "Two pitchers costing $21m this season have been worth more than the five players owed $858m after it.",
        },
        {
            "id": "pipeline-liability",
            "title": "Liability: the pipeline is empty",
            "prose": [
                "FanGraphs ranks the Padres’ farm system last in baseball. Baseball America places it 30th, describing the strength as a handful of high-ceiling names and the weakness as depth, with minor-league rosters “full of old-for-their-level players.” Scouts consulted by the Union-Tribune in late July put it last of 30.",
                "The proximate cause is the July 2025 trade that sent Leo De Vries and three other young arms to the Athletics for Miller and JP Sears. Miller has been superb. De Vries is now rated the second-best prospect in the sport. That is the Preller method in a single transaction: certainty now, paid for with the only cheap wins a club ever gets.",
                "Ethan Salas, a 20-year-old catcher at Double-A, is healthy and hitting again and remains a top-ten prospect nationally. Two Single-A left-handers, Kruz Schoolcraft and Kash Mayfield, are the next-best assets, and both are years away. The consequence for an owner is not sentimental: an empty system means every hole on the roster is filled at retail, permanently, which is a large part of why the payroll is $259m and the run differential is minus 18.",
            ],
        },
        {
            "id": "surplus",
            "title": "Where the surplus actually sits",
            "chart": "chart3_cost_vs_war",
            "caption": "Contract average annual value against 2026 value produced",
            "prose": [
                "Championship teams are not built on the largest contracts. They are built on the gap between what players produce and what they cost, and in San Diego that gap is concentrated in three places.",
                "Merrill’s nine-year, $135m extension, signed before this season at a $15m average, pays him $7.1m in 2027. Miller is arbitration-controlled through 2029. King’s deal is expensive but short. Against them sit Machado at a $31.8m average through 2033, Bogaerts at $25.5m through 2033 and Cronenworth at $11.4m through 2030 — a trio worth 1.7 wins between them this year, at 33, 33 and 32 years old.",
                "The instruction that follows is unglamorous. The surplus contracts are the franchise, and the temptation before the August 3rd deadline will be to spend them: San Diego has been widely reported as a possible seller of Miller. Trading three controlled years of the best relief pitcher in baseball to relieve a balance sheet that a $3.9bn buyer is about to recapitalise would be the most expensive kind of saving.",
            ],
        },
        {
            "id": "peer-gap",
            "title": "The peer gap, measured against the clubs in the way",
            "chart": "chart4_asset_stack",
            "caption": "Editorial championship-asset index: Padres against four contenders",
            "prose": [
                "Set the Padres against the teams they have to beat and the shape of the deficit is consistent. Capital and payroll are competitive. Replenishment and October conversion are not.",
                "The Dodgers are the immediate obstacle and cannot be outspent: back-to-back champions, roughly twice San Diego’s revenue, thirteen games clear in the division. Milwaukee is the more instructive comparison — 67-40 this season on a $124m Opening Day payroll, built almost entirely through internal development. San Diego has spent five years trying to beat Los Angeles at its own game on a fifth of its local media revenue, while running Milwaukee’s problem in reverse.",
                "The championship-asset index is editorial rather than a model. It scores five dimensions on a 0-100 scale to make the shape of the gap legible; the inputs behind it are valuation, tax payroll, share of value from controlled players, published farm rankings and postseason results since 2020.",
            ],
        },
        {
            "id": "playbook",
            "title": "The memo: six moves, in order",
            "chart": "chart5_ownership_playbook",
            "caption": "Where new ownership should spend its first year",
            "prose": [
                "The instinct at this price will be a statement signing. It is the wrong first move: the roster’s marginal need is not another $300m bat. In rough order of urgency:",
                "<strong>1. Refund the pipeline as a capital project, not a scouting line.</strong> Spend the full draft and international bonus pools, buy development infrastructure and hire away the staff that rival clubs use to turn marginal prospects into major leaguers. It is the cheapest source of wins in the sport and the only one that compounds. It is also the item the outgoing regime spent.",
                "<strong>2. Buy innings, not headliners.</strong> The rotation has been carried by King through a summer in which the salary sitting on the injured list has been the ninth-largest in baseball. October is decided by a club’s fourth and fifth-best pitchers, which is the category San Diego has never bought and the one available cheaply every winter.",
                "<strong>3. Fix the October offense deliberately.</strong> The last two eliminations were failures to score: shut out over the final two games of the 2024 division series, five runs across three games in 2025. This lineup is built on power and aggression, a profile that fails against elite pitching in short series. On-base skill and contact are the missing inputs, and they cost less than power does.",
                "<strong>4. Treat local media as a business you own.</strong> Seventy thousand direct subscribers is the biggest such base in baseball and it was assembled in three seasons out of a bankruptcy. Own the funnel, price it properly and extend it across the border rather than waiting for a regional network that is not coming back.",
                "<strong>5. Extend Miller; treat Merrill as untouchable.</strong> Both are cheap, both are in their twenties, and neither can be replaced from within this system. Buying out Miller’s arbitration years fixes a cost curve for four seasons; trading him fixes a quarter.",
                "<strong>6. Settle governance before the winter.</strong> Feliciano will be the control person and intends to run the club in partnership with Jones. The most valuable document they can produce internally is the mandate: one decision-maker for baseball, one time horizon, one definition of success. The Seidler era’s strength was clarity of purpose; its weakness was that the purpose outlived the plan for achieving it.",
            ],
        },
    ]

    feature(
        slug,
        "The Padres Cost $3.9 Billion. Winning Will Cost More.",
        "A buyer’s memo on baseball’s record franchise sale: what San Diego’s assets are worth, where the balance sheet breaks, and how to buy a title.",
        "sports, baseball",
        author="kyle-mcauliffe",
        pub_date="2026-07-31T00:00:00.000Z",
        standfirst="The most expensive baseball team ever sold has the emptiest farm system in the sport, $858m owed to five players and no regional television network. This is the asset sheet.",
        lede=[
            "The price is $3.9bn. Forbes valued the San Diego Padres at $3.1bn in March, on estimated revenue of $484m and operating income of about $20m. José E. Feliciano and Kwanza Jones agreed in May to pay a 26% premium to that mark — roughly eight times revenue, for a club in the 30th-largest media market in the United States.",
            "That arithmetic sets the terms of everything below. No plausible baseball operating margin services $3.9bn. The return has to come from franchise appreciation, from the events and property business around Petco Park, and from the one asset San Diego has never held: a championship, and the permanent revaluation of a market that has waited 57 years for one.",
            "The transfer is not yet complete. Final documentation reached the league in late July, approval requires 22 of the other 29 owners, and a vote is expected in August, after the August 3rd trade deadline. “It’s a question of getting investment commitments, documentation to be put in a condition that it’s ready for a club vote,” the commissioner, Rob Manfred, said on July 14th.",
            "What follows is the memo a buyer wants on day one: what works, what is broken, where the surplus sits, and what to do first.",
        ],
        facts=[
            ("$3.9bn", "Agreed price, pending a vote of 22 of 29 owners"),
            ("$3.1bn", "Forbes’ March 2026 valuation, on $484M of revenue"),
            ("$858M", "Guaranteed money owed to five players after 2026"),
            ("30th", "Farm-system rank of 30 clubs, July 2026"),
            ("$259M", "2026 tax payroll, seventh in baseball"),
            ("5.6", "Wins from King and Miller, who cost $21M this season"),
        ],
        sections=sections,
        ending_heading="The arithmetic of a first title",
        ending=[
            "San Diego does not have a 90-win problem. It has reached the postseason four times in six years and will probably do so again inside two. It has a twelve-game problem: the tournament that follows the season, which the Padres have entered four times since 2020 and left without a pennant every time.",
            "Closing that gap is not a payroll exercise, which is fortunate, because payroll is the one lever this club has already pulled to its limit. It is a depth-and-pipeline exercise, and those are the two things a recapitalised franchise can buy quickly — if the owners spend on infrastructure rather than announcements.",
            "The Padres are worth a record price because someone finally believes the last step is available. Those six moves are what has to be true for that belief to pay. The companion report explains why 57 years of evidence makes it such an expensive bet.",
        ],
        method=[
            "Player value figures are Baseball Reference wins above replacement, current through games of July 29th 2026. Contract terms and average annual values come from Spotrac and FanGraphs’ RosterResource; tax payrolls are Spotrac’s. Valuations are Forbes, March 2026; sale terms and the approval timetable come from MLB.com, Sportico, Sports Business Journal and the San Diego Union-Tribune. Farm-system ranks are FanGraphs, Baseball America and MLB Pipeline, July 2026. Media revenue figures are as reported by SBJ and the Union-Tribune.",
            "The championship-asset index is editorial. It converts five inputs — valuation, tax payroll, share of value from controlled players, published farm rank and postseason results since 2020 — into a 0-100 score per club so the shape of the gap can be read at a glance. It is a framing device, not a forecast, and no projection of wins or title probability is implied.",
        ],
        references=[
            "Baseball Reference. <em>2026 San Diego Padres Statistics</em>.",
            "Forbes. <em>Baseball’s Most Valuable Teams 2026</em>, March 2026.",
            "Sportico. <em>San Diego Padres Sale: Feliciano, Jones to Pay MLB-Record $3.9 Billion</em>, 2026.",
            "Sports Business Journal. <em>Feliciano group submits final documentation for Padres sale</em>, July 2026.",
            "San Diego Union-Tribune. <em>Padres have minor-league pieces to entice teams at trade deadline</em>, July 2026.",
            "Baseball America. <em>MLB Farm System Midseason Talent Rankings</em>, July 2026; FanGraphs RosterResource; Spotrac contract tables.",
            'Related Artometrics reports: <a href="/padres">The Most Expensive Team That Has Never Won Anything</a> · <a href="/dodgers">Dodgers</a> · <a href="/dynasty-index">Sports Dynasty Index</a>.',
        ],
        note="This report is editorial analysis, not investment advice, and Artometrics has no relationship with any party to the transaction. Valuations, revenue and media-rights figures are third-party estimates. Player value figures are current through July 29th 2026 and the season is unfinished. The championship-asset and urgency indices are editorial constructs, clearly labelled as such.",
        source_credit="Data: Baseball Reference, Forbes, Spotrac, FanGraphs, Baseball America - ARTOMETRICS",
        tldr="A group led by José E. Feliciano and Kwanza Jones agreed to pay $3.9bn for the Padres, a record for a baseball club and a 26% premium to Forbes’ valuation. They inherit baseball’s second-best attended club and its worst farm system, $858m owed to five players after 2026, and a local television business that lost more than $60m a year in 2023. The path to a first title runs through pipeline, pitching depth and October offense — not another maximum contract.",
        key_points=[
            "$3.9bn agreed price against a $3.1bn Forbes mark and $484M of revenue",
            "5.6 wins from King and Miller for $21M; 4.5 from the five players owed $858M",
            "Farm system ranked last of 30 after the Leo De Vries trade for Mason Miller",
            "Local media revenue fell from $60M+ a year to a reported $20M-$30M after 2023",
            "70,000 direct-to-consumer subscribers, the most under MLB’s local-media umbrella",
            "Six ownership moves, in order: pipeline, innings, October offense, media, extensions, governance",
        ],
        faq=[
            (
                "Who is buying the Padres and for how much?",
                "A group led by José E. Feliciano, a co-founder of Clearlake Capital, and his wife, Kwanza Jones, agreed in May 2026 to acquire control at a $3.9bn valuation — a record for a Major League club. Feliciano will be the control person. The deal requires approval from 22 of the other 29 owners, and a vote is expected in August 2026.",
            ),
            (
                "What is the Padres’ biggest problem for a new owner?",
                "Two: the farm system ranks last of 30 clubs, so every roster hole is filled at retail; and local media revenue collapsed from more than $60m a year to a reported $20m-$30m after Diamond Sports stopped paying in 2023, leaving a top-seven payroll funded by ownership losses.",
            ),
            (
                "How much money do the Padres owe their existing players?",
                "About $858m is guaranteed after the 2026 season to five players: Fernando Tatis Jr. through 2034, Manny Machado and Xander Bogaerts through 2033, Jackson Merrill through 2034 and Jake Cronenworth through 2030. Those five have produced 4.5 wins above replacement in 2026 through July 29th.",
            ),
            (
                "What would it take for the Padres to win a World Series?",
                "On this analysis, depth rather than star power: refunding a last-ranked farm system, buying rotation innings instead of headliners, adding on-base and contact skills to a lineup that has failed to score in consecutive eliminations, rebuilding local media revenue, extending cheap young assets such as Mason Miller and Jackson Merrill, and settling a single line of baseball authority under the new owners.",
            ),
        ],
    )


def patriots():
    slug = "patriots"
    periods = ["1960-1992", "Parcells/Bledsoe", "Brady/Belichick", "Post-Brady"]
    playoff_wins = [3, 3, 30, 0]
    write_chart(slug, "chart1_system_shock", {"data": [bar_h(periods, playoff_wins, [ART_GREY, ART_BLUE, ART_RED, ART_GREY])], "layout": layout("New England's history has one giant discontinuity", "THE BRADY/BELICHICK ERA BROKE THE FRANCHISE SCALE", x_title="Approximate playoff wins")})

    teams = ["Cowboys", "Steelers", "49ers", "Chiefs", "Patriots"]
    super_bowls = [5, 6, 5, 4, 6]
    write_chart(slug, "chart2_super_bowl_tier", {"data": [bar_h(teams, super_bowls, [ART_BLUE, ART_BLUE, ART_BLUE, ART_BLUE, ART_RED])], "layout": layout("The Patriots reached the NFL summit fast", "ONE ERA BUILT A HISTORIC TOTAL", x_title="Super Bowl wins")})

    seasons = ["2001", "2003", "2004", "2007", "2011", "2014", "2016", "2017", "2018", "2019"]
    wins = [11, 14, 14, 16, 13, 12, 14, 13, 11, 12]
    write_chart(slug, "chart3_regular_season_machine", {"data": [line(seasons, wins)], "layout": layout("The dynasty was a regular-season machine too", "DOUBLE-DIGIT WINS BECAME ROUTINE", x_title="Season", y_title="Regular-season wins")})

    afc_teams = ["Ravens", "Broncos", "Steelers", "Colts", "Chiefs", "Patriots"]
    afc_apps = [4, 4, 5, 4, 6, 13]
    write_chart(slug, "chart4_conference_gate", {"data": [bar_h(afc_teams, afc_apps, [ART_BLUE] * 5 + [ART_RED])], "layout": layout("For two decades, Foxborough was the AFC gate", "CONFERENCE ACCESS WAS THE TRUE CHOKEPOINT", x_title="Conference championship appearances since 2001")})

    eras = ["Pre-Brady", "Brady peak", "Late Brady", "Post-Brady"]
    value_rank = [21, 8, 2, 2]
    football_rank = [20, 1, 2, 22]
    write_chart(slug, "chart5_brand_after_system", {"data": [
        scatter(value_rank, football_rank, eras, [22, 42, 36, 28], [ART_GREY, ART_RED, ART_BLUE, ART_GREY], hover="%{text}<br>Brand rank: %{x}<br>Football rank: %{y}<extra></extra>")
    ], "layout": {**layout("The brand survived the system's end", "FOOTBALL OUTPUT FELL FASTER THAN VALUE", x_title="Estimated brand/value rank (lower is better)", y_title="Football power rank (lower is better)"), "xaxis": {**layout("", "")["xaxis"], "autorange": "reversed", "title": {"text": "Estimated brand/value rank (lower is better)"}}, "yaxis": {**layout("", "")["yaxis"], "autorange": "reversed", "title": {"text": "Football power rank (lower is better)"}}}})

    sections = [
        {"id": "system-shock", "title": "CHART 1 - SYSTEM SHOCK", "chart": "chart1_system_shock", "caption": "Patriots playoff wins by broad franchise period", "prose": ["The Patriots are not a smooth historical franchise. They are a before-and-after experiment. One era overwhelms the rest of the archive.", "The hypothesis is that New England's dynasty was not just a great team; it was a system shock that rewrote franchise identity."]},
        {"id": "super-bowl-tier", "title": "CHART 2 - SUPER BOWL TIER", "chart": "chart2_super_bowl_tier", "caption": "Super Bowl titles among major NFL franchises", "prose": ["The Patriots reached the NFL summit with extraordinary speed. Other franchises accumulated titles over generations; New England compressed its case into two decades.", "That compression is the story. The franchise became ancient history almost overnight."]},
        {"id": "regular-season-machine", "title": "CHART 3 - REGULAR-SEASON MACHINE", "chart": "chart3_regular_season_machine", "caption": "Selected Patriots regular-season wins during the dynasty", "prose": ["Dynasties are remembered through rings, but the Patriots' real violence was routine. Twelve, thirteen, fourteen wins stopped feeling exceptional.", "This is how a system announces itself: excellence becomes boring before it becomes legendary."]},
        {"id": "conference-gate", "title": "CHART 4 - AFC GATE", "chart": "chart4_conference_gate", "caption": "AFC championship appearances since 2001", "prose": ["The Patriots did not merely win Super Bowls. They controlled access to the AFC's final room.", "For rival fan bases, the dynasty was experienced less as a team and more as a recurring gatekeeping mechanism."]},
        {"id": "brand-after-system", "title": "CHART 5 - AFTER THE SYSTEM", "chart": "chart5_brand_after_system", "caption": "Brand rank and football output before and after the dynasty", "prose": ["The post-Brady years expose the separation between brand capital and football output. The value remains; the machine does not.", "That is the afterlife of a dynasty: the market remembers longer than the scoreboard does."]},
    ]
    article(
        slug,
        "PATRIOTS: The Artometrics of the System Dynasty",
        "The Patriots are the NFL's great system shock: a franchise whose Brady/Belichick era compressed a century of legacy into two decades.",
        "atlas, power",
        [("fast-facts", "FAST FACTS"), ("dataset-context", "DATASET CONTEXT")] + [(s["id"], s["title"]) for s in sections] + [("conclusion", "CONCLUSION"), ("references", "REFERENCES"), ("editors-note", "EDITOR'S NOTE")],
        ["The New England Patriots used to be ordinary. Then they became the NFL's most efficient argument about systems, quarterbacks, coaching, and institutional compounding.", "This report tests whether the dynasty is best understood as Brady, Belichick, ownership, luck, or infrastructure. The data points to a system shock: one era so large it became the franchise."],
        [("6", "Super Bowl championships"), ("9", "Super Bowl appearances during the Brady/Belichick era"), ("30", "Approximate playoff wins from 2001 through 2019"), ("13", "AFC championship appearances since 2001"), ("16-0", "Perfect 2007 regular season"), ("2020", "First post-Brady season")],
        ["The report uses public Pro Football Reference franchise records, NFL postseason histories, and Forbes-style franchise value summaries. Periods are editorial groupings designed to isolate the dynasty discontinuity.", "An NFL analyst would ask how much of the dynasty was quarterback versus system. A fan asks why the same logo feels so different after Brady. The charts show both questions share the same hinge."],
        sections,
        ["The Patriots dynasty was not normal greatness. It was a discontinuity: one era that swallowed the franchise before and after it.", "The data says New England's new challenge is not legacy. Legacy is secure. The challenge is proving the institution can produce again without the system that made it famous."],
        ["Pro Football Reference. <em>New England Patriots Franchise Encyclopedia</em>.", "NFL historical postseason records.", "Forbes. <em>NFL Team Valuations</em>, recent estimates.", "Sports Reference team season summaries."],
        "Period totals are rounded public-reference summaries. Brand/value and football-rank points are editorial markers for the shape of the post-dynasty transition, not a formal valuation model.",
        "Data: Pro Football Reference, NFL records, Forbes - ARTOMETRICS",
    )


def cross_sport_dynasty_index():
    slug = "dynasty-index"
    source = "Data: Baseball Reference, Basketball Reference, Pro Football Reference, Hockey Reference, Forbes - ARTOMETRICS"

    teams = ["Yankees", "Celtics", "Lakers", "Patriots", "Steelers", "Canadiens", "Dodgers", "Cowboys", "Warriors", "Maple Leafs"]
    titles = [27, 18, 17, 6, 6, 24, 8, 5, 7, 13]
    write_chart(slug, "chart1_title_mass", {"data": [bar_h(teams, titles, [ART_RED if t in {"Yankees", "Celtics", "Lakers", "Canadiens"} else ART_BLUE for t in teams], hover="<b>%{y}</b><br>Major titles: %{x}<extra></extra>")], "layout": layout("Dynasty mass is not evenly distributed", "A FEW BRANDS HOARD THE ARCHIVE", x_title="Major professional championships")})

    modern_teams = ["Patriots", "Warriors", "Chiefs", "Dodgers", "Spurs", "Red Sox", "Cubs", "Cowboys"]
    shots = [9, 6, 5, 4, 6, 4, 1, 0]
    rings = [6, 4, 3, 2, 5, 4, 1, 0]
    write_chart(slug, "chart2_finals_conversion", {"data": [
        bar_h(modern_teams, shots, [ART_GREY] * len(modern_teams), name="Finals/Super Bowl/World Series appearances", hover="<b>%{y}</b><br>Appearances: %{x}<extra></extra>"),
        bar_h(modern_teams, rings, [ART_RED] * len(modern_teams), name="Titles", hover="<b>%{y}</b><br>Titles: %{x}<extra></extra>"),
    ], "layout": {**layout("Getting there is not the same as closing", "CONVERSION SEPARATES DYNASTIES FROM GOOD TEAMS", x_title="Appearances and titles since 1996"), "barmode": "overlay", "showlegend": True, "legend": {"orientation": "h", "x": 0.5, "xanchor": "center", "y": 1.04}}})

    brands = ["Cowboys", "Yankees", "Lakers", "Warriors", "Patriots", "Dodgers", "Knicks", "Giants", "Celtics", "Chiefs"]
    value = [10.1, 7.6, 7.1, 7.7, 7.4, 5.5, 6.6, 7.3, 5.1, 6.1]
    title_10 = [0, 0, 1, 4, 3, 2, 0, 0, 1, 3]
    write_chart(slug, "chart3_brand_vs_recent_titles", {"data": [scatter(value, title_10, brands, [18 + v * 4 for v in value], [ART_RED if t >= 3 else ART_BLUE for t in title_10], hover="<b>%{text}</b><br>Estimated value: $%{x}B<br>Titles since 2014: %{y}<extra></extra>")], "layout": layout("Brand value and winning now diverge", "THE COWBOYS ARE THE OUTLIER WARNING", x_title="Estimated franchise value, $B", y_title="Titles since 2014")})

    leagues = ["MLB", "NBA", "NFL", "NHL"]
    teams_count = [30, 30, 32, 32]
    unique_champs = [15, 12, 14, 13]
    write_chart(slug, "chart4_league_rotation", {"data": [bar_v(leagues, [round(c / t * 100, 1) for c, t in zip(unique_champs, teams_count)], [ART_RED, ART_BLUE, ART_BLUE, ART_GREY], hover="<b>%{x}</b><br>Share of league winning at least one title since 2000: %{y}%<extra></extra>")], "layout": layout("Some leagues rotate glory faster", "PARITY IS A CULTURAL PRODUCT", x_title="League", y_title="% of teams with a title since 2000")})

    pain_teams = ["Maple Leafs", "Jets", "Browns", "Lions", "Knicks", "Mets", "Suns", "Mariners", "Cowboys", "Yankees"]
    droughts = [57, 55, 59, 67, 51, 38, 56, 48, 29, 15]
    attention = [92, 79, 82, 76, 88, 74, 67, 58, 96, 98]
    write_chart(slug, "chart5_pain_vs_attention", {"data": [scatter(droughts, attention, pain_teams, [14 + d / 4 for d in droughts], [ART_RED if a >= 88 else ART_BLUE for a in attention], hover="<b>%{text}</b><br>Title drought: %{x} years<br>Cultural attention index: %{y}<extra></extra>")], "layout": layout("Pain is drought multiplied by attention", "THE LOUDEST LOSING IS NOT ALWAYS THE LONGEST", x_title="Years since most recent title", y_title="Cultural attention index")})

    sections = [
        {"id": "title-mass", "title": "CHART 1 - DYNASTY MASS", "chart": "chart1_title_mass", "caption": "A few franchises carry an outsized share of championship memory", "prose": ["Cross-sport comparison starts with mass. The Yankees and Canadiens look like institutions because their title archives are not normal franchise resumes; they are historical infrastructure.", "This chart gives future team reports a shared scale. A fan can ask whether a club is chasing its league or chasing one of the archive monopolies."]},
        {"id": "conversion", "title": "CHART 2 - CONVERSION", "chart": "chart2_finals_conversion", "caption": "Modern dynasties are defined by converting appearances into titles", "prose": ["Appearances measure access. Titles measure finishing. The Patriots, Spurs, Warriors, and Red Sox produced different kinds of modern dominance, but each solved the conversion problem better than its peers.", "That is why a merely famous team can feel weaker than a smaller, colder machine."]},
        {"id": "brand-gap", "title": "CHART 3 - BRAND VERSUS OUTPUT", "chart": "chart3_brand_vs_recent_titles", "caption": "The richest sports brands do not all convert attention into recent championships", "prose": ["Value is not a scoreboard. The Cowboys, Knicks, and Yankees show that brand equity can survive long title gaps, while the Chiefs and Warriors show what happens when current winning catches the market's imagination.", "From a metric standpoint, this is the first big split: market power and competitive power are related, but they are not the same variable."]},
        {"id": "league-rotation", "title": "CHART 4 - LEAGUE ROTATION", "chart": "chart4_league_rotation", "caption": "Title rotation differs by league structure and postseason randomness", "prose": ["Leagues write different scripts. Baseball's long season and playoff volatility create a different kind of access than the NBA's star-driven tournament or the NFL's single-elimination machine.", "The cultural output is visible: every league teaches fans a different theory of fairness."]},
        {"id": "pain-attention", "title": "CHART 5 - PAIN AND ATTENTION", "chart": "chart5_pain_vs_attention", "caption": "Fan pain grows when droughts happen under a bright spotlight", "prose": ["The longest drought is not always the loudest drought. A small-market wait can be existential; a New York, Toronto, or Dallas wait becomes national theater.", "This is why cross-report analysis matters. The number is only half the story; the attention system decides how the number feels."]},
    ]
    article(
        slug,
        "SPORTS DYNASTY INDEX: Best, Worst, and Most Misleading Teams",
        "A cross-league Artometrics report comparing championship mass, conversion, market value, parity, and fan pain across major sports franchises.",
        "atlas, power",
        [("fast-facts", "FAST FACTS"), ("dataset-context", "DATASET CONTEXT")] + [(s["id"], s["title"]) for s in sections] + [("conclusion", "CONCLUSION"), ("references", "REFERENCES"), ("editors-note", "EDITOR'S NOTE")],
        [
            "Team reports answer one fan base at a time. This report changes the lens: it asks which sports brands look strongest when the measurement system crosses league borders.",
            "The hypothesis is that greatness has at least three separable components: archive mass, conversion efficiency, and attention. A franchise can win one of those categories and still lose the broader identity test.",
        ],
        [("351", "Charts now audited across the Artometrics corpus"), ("4", "Major North American leagues compared"), ("27", "Yankees titles, the largest MLB archive"), ("0", "Cowboys titles since the 1990s dynasty"), ("57", "Maple Leafs active Stanley Cup drought entering 2025"), ("5", "Charts in this cross-report")],
        [
            "This is a curated comparative model built from public reference records rather than a proprietary win-probability system. The goal is to create a shared vocabulary that later team profiles can reference.",
            "A front-office analyst might want causal variables: payroll, age curves, draft capital, injuries, ownership. An Artometrician starts one level higher: what does the institution look like when winning, money, attention, and pain are placed on the same page?",
        ],
        sections,
        ["The cleanest finding is that sports greatness is not one ranking. The Yankees and Canadiens own archive mass; the Patriots and Warriors define recent conversion; the Cowboys own the contradiction between brand and output.", "Future reports can now point back to this index whenever a single-team story needs a cross-league benchmark."],
        ["Baseball Reference. Franchise history pages.", "Basketball Reference. Team season and playoff records.", "Pro Football Reference. Team franchise records.", "Hockey Reference. Franchise records.", "Forbes. Professional sports franchise valuations, recent lists."],
        "Figures use rounded public-reference values and editorial indices for attention. The report is intended as a comparative map, not a betting model.",
        source,
    )


def league_money_and_skill_report():
    slug = "leagues"
    source = "Data: Forbes, Spotrac, Basketball Reference, Baseball Reference, Pro Football Reference, Hockey Reference - ARTOMETRICS"

    leagues = ["NFL", "NBA", "MLB", "NHL", "Premier League", "MLS"]
    avg_value = [6.5, 4.4, 2.4, 1.4, 2.1, 0.7]
    write_chart(slug, "chart1_league_value_floor", {"data": [bar_h(leagues, avg_value, [ART_RED if l == "NFL" else ART_BLUE for l in leagues], hover="<b>%{y}</b><br>Approx. average club value: $%{x}B<extra></extra>")], "layout": layout("The NFL is the value machine", "MEDIA SCARCITY MAKES EVERY TEAM EXPENSIVE", x_title="Approximate average franchise value, $B")})

    leagues2 = ["NBA", "NFL", "MLB", "NHL", "Premier League"]
    star_leverage = [92, 58, 54, 48, 72]
    roster_size = [15, 53, 26, 23, 25]
    write_chart(slug, "chart2_star_leverage", {"data": [scatter(roster_size, star_leverage, leagues2, [28, 18, 20, 19, 23], [ART_RED, ART_BLUE, ART_BLUE, ART_GREY, ART_BLUE], hover="<b>%{text}</b><br>Active roster scale: %{x}<br>Star leverage index: %{y}<extra></extra>")], "layout": layout("Small rosters make stars louder", "THE NBA HAS THE CLEANEST SUPERSTAR SIGNAL", x_title="Typical active roster scale", y_title="Star leverage index")})

    leagues3 = ["NFL", "NBA", "MLB", "NHL"]
    hard_cap = [95, 76, 35, 90]
    payroll_spread = [42, 58, 86, 45]
    write_chart(slug, "chart3_cap_vs_payroll_spread", {"data": [scatter(hard_cap, payroll_spread, leagues3, [28, 25, 26, 22], [ART_RED if l == "MLB" else ART_BLUE for l in leagues3], hover="<b>%{text}</b><br>Salary-control index: %{x}<br>Payroll-spread index: %{y}<extra></extra>")], "layout": layout("Rules decide how money becomes talent", "BASEBALL LETS PAYROLL SPREAD WIDEN", x_title="Salary-control index", y_title="Payroll-spread index")})

    products = ["NFL game", "NBA game", "MLB game", "NHL game", "Premier League match", "MLS match"]
    event_count = [17, 82, 162, 82, 38, 34]
    write_chart(slug, "chart4_event_scarcity", {"data": [bar_v(products, event_count, [ART_RED, ART_BLUE, ART_BLUE, ART_GREY, ART_BLUE, ART_GREY], hover="<b>%{x}</b><br>Regular-season events per team: %{y}<extra></extra>")], "layout": layout("Scarcity changes fan attention", "THE NFL MAKES EACH GAME FEEL LIKE A PUBLIC EVENT", x_title="Product", y_title="Regular-season games/matches")})

    leagues4 = ["NFL", "NBA", "MLB", "NHL", "Premier League", "MLS"]
    globality = [72, 86, 61, 55, 94, 58]
    domesticity = [94, 78, 84, 69, 62, 73]
    write_chart(slug, "chart5_global_vs_domestic", {"data": [scatter(globality, domesticity, leagues4, [24, 24, 22, 20, 26, 18], [ART_RED if l in {"Premier League", "NBA"} else ART_BLUE for l in leagues4], hover="<b>%{text}</b><br>Global cultural reach: %{x}<br>Domestic ritual index: %{y}<extra></extra>")], "layout": layout("Leagues sell different kinds of belonging", "GLOBAL REACH AND LOCAL RITUAL ARE NOT THE SAME", x_title="Global cultural reach index", y_title="Domestic ritual index")})

    sections = [
        {"id": "value-floor", "title": "CHART 1 - VALUE FLOOR", "chart": "chart1_league_value_floor", "caption": "The NFL turns scarcity and national television into the highest average club value", "prose": ["The NFL does not need every team to be glamorous. Its media structure makes the ordinary franchise expensive because the league product is scarce, synchronized, and nationally distributed.", "That is a metric difference and a cultural difference: football teams are local flags plugged into a national machine."]},
        {"id": "star-leverage", "title": "CHART 2 - STAR LEVERAGE", "chart": "chart2_star_leverage", "caption": "The NBA gives individual stars the strongest control over team identity", "prose": ["A basketball star touches a huge share of possessions. A baseball star can disappear into lineup order and variance. A football star may be trapped inside scheme, injuries, and roster scale.", "This is why NBA identity travels through names, while NFL identity often travels through systems."]},
        {"id": "rules-money", "title": "CHART 3 - RULES AND MONEY", "chart": "chart3_cap_vs_payroll_spread", "caption": "League rules shape whether money becomes separation or merely survival", "prose": ["Salary caps, luxury taxes, revenue sharing, and roster rules are not administrative details. They are identity engines.", "The MLB gap is partly the point: baseball lets market and development systems express themselves with less hard compression than the NFL or NHL."]},
        {"id": "event-scarcity", "title": "CHART 4 - EVENT SCARCITY", "chart": "chart4_event_scarcity", "caption": "The number of games changes how fans process failure", "prose": ["A baseball team can lose four straight and still be fine. An NFL team can lose two games and trigger a referendum. The schedule is a psychology machine.", "This matters for future reports because pain, momentum, and panic are not measured on the same clock across leagues."]},
        {"id": "belonging", "title": "CHART 5 - BELONGING", "chart": "chart5_global_vs_domestic", "caption": "Global reach and domestic ritual create different cultural signatures", "prose": ["The Premier League and NBA travel globally with exceptional ease. The NFL remains more domestically ritualized even as its value dominates.", "The Artometrics question is not simply which league is bigger. It is what kind of belonging each league manufactures."]},
    ]
    article(
        slug,
        "LEAGUE MONEY, SKILL, AND STAR SYSTEMS",
        "A cross-sport report on how league rules, money, roster scale, event scarcity, and cultural reach shape the way teams become meaningful.",
        "atlas, culture",
        [("fast-facts", "FAST FACTS"), ("dataset-context", "DATASET CONTEXT")] + [(s["id"], s["title"]) for s in sections] + [("conclusion", "CONCLUSION"), ("references", "REFERENCES"), ("editors-note", "EDITOR'S NOTE")],
        [
            "A sports league is a measurement system before it is an entertainment product. It decides how much money can matter, how much one player can matter, how often fans get to reset emotionally, and how widely the story can travel.",
            "This report builds a cross-league lens for future Artometrics profiles: money, skill, star leverage, schedule density, and culture are not interchangeable across sports.",
        ],
        [("$6.5B", "Approximate average NFL franchise value in recent Forbes-style estimates"), ("17", "NFL regular-season games per team"), ("162", "MLB regular-season games per team"), ("92", "NBA star leverage index in this editorial model"), ("6", "Leagues compared"), ("5", "Charts in this report")],
        [
            "The figures combine public valuation summaries, reference-record league structures, and editorial indices. The indices are deliberately transparent: they exist to compare systems, not to pretend every input is observed with laboratory precision.",
            "A commissioner, analyst, or fan would ask different questions. The useful layer is the shared one: what does the league make easy, what does it make scarce, and what does it make emotionally expensive?",
        ],
        sections,
        ["The cleanest conclusion is that league design creates fan reality. The same owner, player, or city would produce a different identity under a different schedule, cap structure, roster size, and media architecture.", "That is why future team profiles should not compare teams without comparing the sports that made them."],
        ["Forbes. Professional sports franchise valuation lists.", "Spotrac. Salary-cap and payroll summaries.", "Basketball Reference, Baseball Reference, Pro Football Reference, Hockey Reference. League and team records.", "Premier League and MLS public competition records."],
        "Index values are editorial approximations designed for cross-sport interpretation. They should be read as comparative signals, not official league statistics.",
        source,
    )


def regional_sports_identity_map():
    slug = "fandom"
    source = "Data: Reference franchise histories, Census regional framing, Forbes, public attendance and championship records - ARTOMETRICS"

    regions = ["Northeast", "California", "Texas", "Great Lakes", "Florida", "Pacific NW", "Mid-South"]
    titles = [86, 49, 20, 54, 15, 3, 18]
    write_chart(slug, "chart1_regional_title_density", {"data": [bar_h(regions, titles, [ART_RED if r in {"Northeast", "Great Lakes"} else ART_BLUE for r in regions], hover="<b>%{y}</b><br>Approx. major pro titles: %{x}<extra></extra>")], "layout": layout("Sports memory is region-locked", "THE NORTHEAST AND GREAT LAKES CARRY OLD ARCHIVES", x_title="Approximate major pro championships")})

    markets = ["New York", "Los Angeles", "Boston", "Bay Area", "Dallas", "Chicago", "Philadelphia", "Detroit", "Miami", "Seattle"]
    team_count = [9, 8, 5, 6, 5, 5, 4, 4, 4, 4]
    market_value = [43, 35, 23, 25, 24, 18, 15, 12, 14, 11]
    write_chart(slug, "chart2_market_stack", {"data": [scatter(team_count, market_value, markets, [18 + v / 2 for v in team_count], [ART_RED if m in {"New York", "Los Angeles"} else ART_BLUE for m in markets], hover="<b>%{text}</b><br>Major teams: %{x}<br>Estimated combined value: $%{y}B<extra></extra>")], "layout": layout("Market depth compounds cultural volume", "NEW YORK AND LOS ANGELES ARE SPORTS MEDIA ECOSYSTEMS", x_title="Major pro teams in market", y_title="Estimated combined value, $B")})

    region_order = ["Northeast", "California", "Texas", "Great Lakes", "Florida", "Pacific NW"]
    baseball = [92, 72, 45, 81, 54, 48]
    football = [73, 58, 95, 84, 78, 74]
    basketball = [82, 88, 66, 71, 70, 69]
    write_chart(slug, "chart3_sport_dna", {"data": [
        line(region_order, baseball, color=ART_RED, name="Baseball memory", hover="<b>%{x}</b><br>Baseball identity: %{y}<extra></extra>"),
        line(region_order, football, color=ART_BLUE, name="Football ritual", hover="<b>%{x}</b><br>Football identity: %{y}<extra></extra>"),
        line(region_order, basketball, color="#16A085", name="Basketball/star culture", hover="<b>%{x}</b><br>Basketball identity: %{y}<extra></extra>"),
    ], "layout": {**layout("Regions specialize emotionally", "EACH MARKET HAS A DIFFERENT SPORTS DNA", x_title="Region", y_title="Identity index"), "showlegend": True, "legend": {"orientation": "h", "x": 0.5, "xanchor": "center", "y": 1.08}}})

    cities = ["Boston", "New York", "Los Angeles", "Dallas", "Cleveland", "Toronto", "Phoenix", "Seattle", "Detroit", "San Francisco"]
    drought_pain = [18, 52, 22, 73, 90, 94, 86, 71, 67, 28]
    recent_success = [82, 38, 79, 41, 30, 22, 35, 45, 48, 86]
    write_chart(slug, "chart4_city_pain_success", {"data": [scatter(recent_success, drought_pain, cities, [20, 24, 22, 22, 20, 20, 19, 18, 19, 22], [ART_RED if p >= 80 else ART_BLUE for p in drought_pain], hover="<b>%{text}</b><br>Recent success index: %{x}<br>Drought/pain index: %{y}<extra></extra>")], "layout": layout("Cities carry different emotional balances", "SUCCESS DOES NOT ERASE THE PAIN OF THE WRONG TEAM", x_title="Recent multi-team success index", y_title="Drought/pain index")})

    cultures = ["Legacy archive", "Star glamour", "Football ritual", "Underdog pain", "Expansion hunger", "Global gateway"]
    scores = [94, 88, 84, 76, 58, 72]
    write_chart(slug, "chart5_identity_types", {"data": [bar_v(cultures, scores, [ART_RED, ART_BLUE, ART_BLUE, ART_GREY, ART_GREY, ART_BLUE], hover="<b>%{x}</b><br>Regional identity strength: %{y}<extra></extra>")], "layout": layout("Regional identity has types", "A SPORTS CITY IS A PORTFOLIO OF MYTHS", x_title="Identity type", y_title="Strength index")})

    sections = [
        {"id": "regional-titles", "title": "CHART 1 - REGIONAL TITLE DENSITY", "chart": "chart1_regional_title_density", "caption": "Championship memory clusters by region", "prose": ["A region's sports identity is not only current fandom. It is the sediment of old championships, old rivalries, and inherited expectations.", "The Northeast and Great Lakes have unusually deep archives because their leagues, cities, and media systems matured early."]},
        {"id": "market-stack", "title": "CHART 2 - MARKET STACK", "chart": "chart2_market_stack", "caption": "Deep markets create sports media ecosystems rather than single-team identities", "prose": ["New York and Los Angeles are not simply large markets. They are sports ecosystems where multiple teams compete for attention, mythology, and local legitimacy.", "That makes cross-report comparison useful: a Knicks drought and a Lakers title live in the same media bloodstream."]},
        {"id": "sport-dna", "title": "CHART 3 - SPORT DNA", "chart": "chart3_sport_dna", "caption": "Regions specialize in different sports identities", "prose": ["Texas reads as football ritual. California leans toward basketball and glamour. The Northeast keeps baseball memory unusually alive.", "The point is not stereotype; it is signal. Regional sports culture gives the same win-loss record a different accent."]},
        {"id": "pain-success", "title": "CHART 4 - CITY PAIN VERSUS SUCCESS", "chart": "chart4_city_pain_success", "caption": "A city can be successful overall and still carry a famous wound", "prose": ["Multi-team cities do not experience success cleanly. A Boston fan can live near constant banners while a specific rival city experiences one drought as civic identity.", "Pain is often team-specific, but markets distribute and amplify it."]},
        {"id": "identity-types", "title": "CHART 5 - IDENTITY TYPES", "chart": "chart5_identity_types", "caption": "Sports cities are portfolios of myths", "prose": ["Some places sell archive. Some sell stars. Some sell football Sundays. Some sell hunger because they have not yet received the validating title.", "This is the bridge to future city bioeconomics reports: sports data is one part of a place's cultural fingerprint."]},
    ]
    article(
        slug,
        "REGIONAL SPORTS IDENTITY MAP",
        "A cross-report map of how regions, markets, leagues, and droughts create different sports identities across American cities.",
        "atlas, culture",
        [("fast-facts", "FAST FACTS"), ("dataset-context", "DATASET CONTEXT")] + [(s["id"], s["title"]) for s in sections] + [("conclusion", "CONCLUSION"), ("references", "REFERENCES"), ("editors-note", "EDITOR'S NOTE")],
        [
            "A team is never just a team. It is attached to a region, a media market, a league structure, and a local memory system. That context changes what the same number means.",
            "This report turns the sports canon toward geography. The goal is to show how regions become recognizable under the data microscope.",
        ],
        [("10", "Large markets/cities compared"), ("7", "Regions grouped for title-density analysis"), ("6", "Identity archetypes used in the map"), ("94", "Toronto drought/pain index in this editorial model"), ("43B", "Approximate combined New York major-team value"), ("5", "Charts in this report")],
        [
            "The charts use public franchise histories, rounded valuation summaries, and editorial identity indices. The indices are not official statistics; they are structured prompts for comparing markets.",
            "A cultural economist would ask how facilities, media density, migration, ownership, and league rules shape local identity. This report is the first map layer for that conversation.",
        ],
        sections,
        ["The main finding is that sports identity is regional before it is rational. Market size, title archives, sport specialization, and drought all shape the meaning of a fan base.", "This gives the next batch a new tool: every team profile can now ask not only how good the team is, but what kind of place produced that version of good, bad, rich, cursed, or glamorous."],
        ["Reference franchise histories from Baseball Reference, Basketball Reference, Pro Football Reference, and Hockey Reference.", "Forbes. Professional sports franchise valuation lists.", "U.S. Census regional framing, used only as a broad geography reference.", "Public attendance, championship, and market summaries from league history pages."],
        "Regional and identity indices are editorial approximations designed to organize cross-report thinking. They should be refined as more city/team reports are added.",
        source,
    )


def write_plan():
    plan = dedent(
        """
        # Artometrics sports canon source plan

        This plan turns the Warriors/Giants model into a repeatable sports-report system:
        every article gets five charts, but each chart must answer a different editorial
        question: history, peer comparison, efficiency, pain/volatility, and identity.

        ## First canon batch

        1. `yankees`
           - Theme: empire, expectation, payroll conversion.
           - Sources: Baseball Reference, Lahman, Retrosheet/Baseball Almanac, Forbes.
        2. `lakers`
           - Theme: star cycles, glamour, recurring Finals access.
           - Sources: Basketball Reference, NBA history, Sports Reference.
        3. `cowboys`
           - Theme: brand value versus postseason conversion.
           - Sources: Pro Football Reference, NFL records, Forbes.

        ## Next canon batch

        4. `celtics`
           - Theme: inherited expectation, title density, modern access.
           - Sources: Basketball Reference, NBA history, Sports Reference.
        5. `dodgers`
           - Theme: high-floor contention, spending infrastructure, October conversion.
           - Sources: Baseball Reference, Lahman, payroll-rank summaries, Retrosheet/Baseball Almanac.
        6. `patriots`
           - Theme: system shock, Brady/Belichick discontinuity, brand after dynasty.
           - Sources: Pro Football Reference, NFL records, Forbes.

        ## Cross-report analysis batch

        7. `dynasty-index`
           - Theme: championship mass, conversion, brand/output gaps, fan pain.
           - Sources: Baseball/Basketball/Football/Hockey Reference, Forbes.
        8. `leagues`
           - Theme: league economics, salary rules, star leverage, event scarcity.
           - Sources: Forbes, Spotrac, major reference databases.
        9. `fandom`
           - Theme: region-locked sports identity, market depth, drought and civic memory.
           - Sources: franchise histories, valuation summaries, public regional framing.

        ## Chart contract

        Each report receives:

        - Chart 1: historical spine (titles, wins, eras, or long-run trend)
        - Chart 2: peer comparison (where this subject sits against the field)
        - Chart 3: identity metric (what makes the subject culturally/statistically itself)
        - Chart 4: contradiction chart (money vs wins, brand vs output, talent vs conversion)
        - Chart 5: pain, gap, or frontier chart (what fans/professionals argue about)

        ## Scale-up order

        ### Batch 2b - NL West companion
        5b. `padres`
           - Theme: star payroll without ring conversion; expansion scarcity; pennant drought.
           - Sources: Baseball Reference, Lahman, payroll-rank summaries, Retrosheet/Baseball Almanac.
           - Cross-refs: Dodgers machine, Giants arc, sports dynasty index.
        5c. `padres-blueprint`
           - Theme: buyer memo — franchise capital, player assets, peer gaps, first-title operating plan.
           - Sources: Forbes valuations, Baseball Reference WAR, payroll markers, farm context.
           - Cross-refs: Padres paying-for-October, Dodgers machine, dynasty index, league money.

        ### Batch 3 - league pillars
        - NBA: Knicks, Spurs, Bulls.
        - MLB: Red Sox, Cubs, A's.
        - NFL: Chiefs, 49ers, Steelers.

        ### Batch 4 - droughts, villains, and fan pain
        - NBA: Clippers, Kings, Suns.
        - MLB: Mets, Mariners, Cardinals.
        - NFL: Browns, Lions, Jets.

        ### Batch 5 - NHL and global football entry
        - NHL: Canadiens, Maple Leafs, Rangers, Bruins, Red Wings, Penguins, Oilers.
        - Soccer: Real Madrid, Barcelona, Manchester United, Liverpool, Bayern, PSG.

        ### Batch 6 - individual sports and games
        - Tennis: Serena, Federer, Nadal, Djokovic.
        - Golf/chess: Tiger, Magnus, Kasparov, Polgar.
        - Olympics: USA, China, Soviet/Russia, small-country medal efficiency.

        ## Editorial rule

        A chart is not included because it exists. A chart is included because it changes
        the conversation between an Artometrician and an expert fan.

        ## Cross-reference rule

        Team profiles should now point to at least one cross-report benchmark:
        dynasty index, league economics, or regional identity. This makes the sports
        canon feel like one connected atlas rather than isolated one-off posts.
        """
    ).strip()
    DOCS_DIR.mkdir(exist_ok=True)
    (DOCS_DIR / "sports-canon-source-plan.md").write_text(plan + "\n")


GENERATORS = {
    "yankees": yankees,
    "lakers": lakers,
    "cowboys": cowboys,
    "celtics": celtics,
    "dodgers": dodgers,
    "padres": padres,
    "padres-blueprint": padres_ownership_blueprint,
    "patriots": patriots,
    "dynasty-index": cross_sport_dynasty_index,
    "league-money": league_money_and_skill_report,
    "regional-identity": regional_sports_identity_map,
}


def main(argv: list[str] | None = None):
    import sys

    args = list(sys.argv[1:] if argv is None else argv)
    write_plan()
    if "--only" in args:
        idx = args.index("--only")
        key = args[idx + 1] if idx + 1 < len(args) else ""
        if key not in GENERATORS:
            raise SystemExit(f"Unknown --only target {key!r}; choose from {', '.join(GENERATORS)}")
        GENERATORS[key]()
        print(f"Generated sports canon plan and report: {key}")
        return

    for fn in GENERATORS.values():
        fn()
    print("Generated sports canon plan, team reports, and cross-sports reports.")


if __name__ == "__main__":
    main()
