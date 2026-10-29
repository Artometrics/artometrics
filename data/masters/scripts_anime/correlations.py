#!/usr/bin/env python3
"""Exploratory correlation charts for the refreshed anime dataset (not article assets)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "data" / "anime"
OUT_DIR = DATA_DIR / "exploratory"
FONTS_DIR = REPO_ROOT / "assets" / "fonts"

ART_RED = "#C0392B"
ART_BLUE = "#1C4E80"
ART_DARK = "#1C1C1E"
ART_MID = "#6B6B6B"
ART_CREAM = "#FAFAF8"


def setup_fonts() -> None:
    sans = FONTS_DIR / "DMSans.ttf"
    mono = FONTS_DIR / "DMMono-Regular.ttf"
    if sans.exists():
        fm.fontManager.addfont(str(sans))
    if mono.exists():
        fm.fontManager.addfont(str(mono))
    plt.rcParams.update(
        {
            "font.family": "DM Sans",
            "font.sans-serif": ["DM Sans", "DejaVu Sans", "sans-serif"],
            "axes.labelcolor": ART_MID,
            "axes.edgecolor": "#D5D5D5",
            "axes.facecolor": ART_CREAM,
            "figure.facecolor": ART_CREAM,
            "text.color": ART_DARK,
            "axes.titleweight": "bold",
        }
    )


def parse_json_list(val: str) -> list[str]:
    if not val or val == "[]":
        return []
    try:
        return json.loads(val)
    except json.JSONDecodeError:
        return []


def style_ax(ax: plt.Axes, title: str, subtitle: str, caption: str) -> None:
    ax.set_title(title, fontsize=14, pad=12)
    ax.text(0, 1.02, subtitle, transform=ax.transAxes, fontsize=10, color=ART_MID)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.figure.text(0.01, 0.01, caption, fontsize=8, color=ART_MID)


def chart_streaming_vs_score(df: pd.DataFrame) -> None:
    scored = df.dropna(subset=["score"]).copy()
    scored["sites"] = scored["streaming_sites"].map(parse_json_list)
    scored = scored[scored["sites"].map(len) > 0]
    scored["primary_site"] = scored["sites"].map(lambda s: s[0])
    top = scored["primary_site"].value_counts().head(6).index
    subset = scored[scored["primary_site"].isin(top)]
    means = subset.groupby("primary_site")["score"].mean().sort_values(ascending=False)
    counts = subset.groupby("primary_site")["score"].count()

    fig, ax = plt.subplots(figsize=(8, 4.5))
    bars = ax.bar(means.index, means.values, color=[ART_BLUE if i % 2 else ART_RED for i in range(len(means))])
    for bar, m, n in zip(bars, means.values, counts.values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.03,
            f"{m:.2f}\nn={n}",
            ha="center",
            va="bottom",
            fontsize=8,
            fontfamily="DM Mono",
        )
    ax.set_ylabel("Mean MAL score")
    ax.set_ylim(0, max(means.values) * 1.15)
    style_ax(
        ax,
        "Streaming footprint vs audience score",
        "Among titles with a known primary streaming link (AniList/Jikan)",
        f"Top platforms by title count; mean score {means.mean():.2f} across groups.",
    )
    fig.tight_layout()
    fig.savefig(OUT_DIR / "corr_streaming_vs_score.png", dpi=160)
    plt.close(fig)


def chart_studio_output_trend(df: pd.DataFrame) -> None:
    tv = df[df["type"] == "TV"].copy()
    tv["studios"] = tv["studio"].map(parse_json_list)
    tv = tv[tv["studios"].map(len) > 0]
    tv["main_studio"] = tv["studios"].map(lambda s: s[0])
    tv = tv[(tv["season_year"] >= 2019) & (tv["season_year"] <= 2026)]
    top_studios = tv["main_studio"].value_counts().head(5).index
    pivot = (
        tv[tv["main_studio"].isin(top_studios)]
        .groupby(["season_year", "main_studio"])
        .size()
        .unstack(fill_value=0)
    )
    fig, ax = plt.subplots(figsize=(8, 4.5))
    years = pivot.index.values
    for studio, color in zip(pivot.columns, [ART_RED, ART_BLUE, ART_DARK, ART_MID, "#8B3228"]):
        ax.plot(years, pivot[studio].values, marker="o", label=studio, color=color, linewidth=2)
    ax.set_xlabel("Season year")
    ax.set_ylabel("TV anime count")
    ax.legend(frameon=False, fontsize=8)
    style_ax(
        ax,
        "Top studios: seasonal TV output since 2019",
        "Main studio (first listed) per MAL title",
        f"2019–2026 TV rows: {len(tv):,}; top-5 studios shown.",
    )
    fig.tight_layout()
    fig.savefig(OUT_DIR / "corr_studio_output_2019_2026.png", dpi=160)
    plt.close(fig)


def chart_source_material_shift(df: pd.DataFrame) -> None:
    tv = df[(df["type"] == "TV") & (df["season_year"].between(2015, 2026))].copy()
    tv = tv.dropna(subset=["source"])
    counts = tv.groupby(["season_year", "source"]).size().unstack(fill_value=0)
    top_sources = tv["source"].value_counts().head(4).index
    counts = counts[top_sources]
    fig, ax = plt.subplots(figsize=(8, 4.5))
    bottom = np.zeros(len(counts))
    colors = [ART_RED, ART_BLUE, ART_DARK, ART_MID]
    for src, color in zip(counts.columns, colors):
        ax.bar(counts.index, counts[src], bottom=bottom, label=src, color=color, width=0.75)
        bottom += counts[src].values
    ax.set_xlabel("Season year")
    ax.set_ylabel("TV titles")
    ax.legend(frameon=False, fontsize=8, ncol=2)
    style_ax(
        ax,
        "Source material mix on seasonal TV anime",
        "Share of top adaptation sources by premiere year",
        f"Manga share 2024: {counts.get('Manga', pd.Series()).get(2024, 0) / max(counts.loc[2024].sum(),1) * 100:.0f}% of labeled TV rows.",
    )
    fig.tight_layout()
    fig.savefig(OUT_DIR / "corr_source_material_shift.png", dpi=160)
    plt.close(fig)


def chart_trending_vs_members(df: pd.DataFrame) -> None:
    sub = df.dropna(subset=["anilist_trending", "members"]).copy()
    sub = sub[(sub["members"] > 0) & (sub["anilist_trending"] > 0)]
    if len(sub) > 8000:
        sub = sub.sample(8000, random_state=42)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.scatter(
        np.log10(sub["members"]),
        sub["anilist_trending"],
        alpha=0.25,
        s=12,
        c=ART_BLUE,
        edgecolors="none",
    )
    r = sub["members"].corr(sub["anilist_trending"])
    ax.set_xlabel("log10(MAL members)")
    ax.set_ylabel("AniList trending rank")
    style_ax(
        ax,
        "Catalog size vs AniList momentum",
        "Each point is one anime title",
        f"Pearson r(members, trending) = {r:.3f} on n={len(sub):,} titles with both fields.",
    )
    fig.tight_layout()
    fig.savefig(OUT_DIR / "corr_trending_vs_members.png", dpi=160)
    plt.close(fig)


def chart_isekai_tag_growth(df: pd.DataFrame) -> None:
    df = df.copy()
    df["tags"] = df["anilist_tags"].map(parse_json_list)
    df["is_isekai"] = df["tags"].map(lambda t: any("Isekai" in x for x in t))
    tv = df[(df["type"] == "TV") & df["season_year"].between(2010, 2026)]
    yearly = tv.groupby("season_year")["is_isekai"].mean() * 100
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.fill_between(yearly.index, yearly.values, color=ART_RED, alpha=0.25)
    ax.plot(yearly.index, yearly.values, color=ART_RED, linewidth=2.2, marker="o")
    ax.set_ylabel("% TV titles tagged Isekai (AniList)")
    ax.set_xlabel("Season year")
    style_ax(
        ax,
        "Isekai tag prevalence among TV anime",
        "AniList tag list contains “Isekai”",
        f"2024: {yearly.get(2024, float('nan')):.1f}% of TV rows; peak {yearly.max():.1f}% in {int(yearly.idxmax())}.",
    )
    fig.tight_layout()
    fig.savefig(OUT_DIR / "corr_isekai_tag_growth.png", dpi=160)
    plt.close(fig)


def main() -> int:
    setup_fonts()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    snapshots = sorted(DATA_DIR.glob("anime_*.parquet"))
    if not snapshots:
        print("No snapshot parquet found; run refresh.py first", file=sys.stderr)
        return 1
    df = pd.read_parquet(snapshots[-1])
    chart_streaming_vs_score(df)
    chart_studio_output_trend(df)
    chart_source_material_shift(df)
    chart_trending_vs_members(df)
    chart_isekai_tag_growth(df)
    print(f"Wrote charts to {OUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
