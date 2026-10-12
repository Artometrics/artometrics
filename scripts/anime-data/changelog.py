"""Build CHANGELOG markdown comparing baseline vs refreshed snapshot."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def write_changelog(
    baseline: pd.DataFrame,
    refreshed: pd.DataFrame,
    out_path: Path,
    baseline_label: str,
    refresh_label: str,
) -> dict[str, float | int]:
    base_ids = set(baseline["animeID"].astype(int))
    new_ids = set(refreshed["animeID"].astype(int))
    added = sorted(new_ids - base_ids)
    removed = sorted(base_ids - new_ids)
    shared = base_ids & new_ids

    base_cols = set(baseline.columns)
    new_cols = set(refreshed.columns)
    added_vars = sorted(new_cols - base_cols)

    drift = refreshed[refreshed["animeID"].isin(shared)][["animeID", "score"]].merge(
        baseline[["animeID", "score"]].rename(columns={"score": "score_old"}),
        on="animeID",
        how="inner",
    ).rename(columns={"score": "score_new"})

    both_scored = drift.dropna(subset=["score_new", "score_old"])
    mean_abs_drift = float((both_scored["score_new"] - both_scored["score_old"]).abs().mean()) if len(both_scored) else 0.0
    median_drift = float((both_scored["score_new"] - both_scored["score_old"]).median()) if len(both_scored) else 0.0

    changed_rows = 0
    compare_cols = [c for c in refreshed.columns if c in baseline.columns and c != "animeID"]
    merged = refreshed.merge(baseline, on="animeID", suffixes=("_new", "_old"), how="inner")
    for col in compare_cols:
        new_c = f"{col}_new" if f"{col}_new" in merged.columns else col
        old_c = f"{col}_old" if f"{col}_old" in merged.columns else col
        if new_c in merged.columns and old_c in merged.columns:
            diff = merged[new_c].astype(str) != merged[old_c].astype(str)
            changed_rows = max(changed_rows, int(diff.sum()))

    lines = [
        f"# Anime dataset changelog ({baseline_label} → {refresh_label})",
        "",
        "## Summary",
        f"- Baseline rows: **{len(baseline):,}** ({baseline_label})",
        f"- Refreshed rows: **{len(refreshed):,}** ({refresh_label})",
        f"- New titles (MAL ids): **{len(added):,}**",
        f"- Removed titles: **{len(removed):,}**",
        f"- New variables (columns): **{len(added_vars):,}**",
        f"- Shared titles with any column change (max column): **{changed_rows:,}**",
        "",
        "## Score drift (titles in both snapshots)",
        f"- Titles with scores in both: **{len(both_scored):,}**",
        f"- Mean absolute score change: **{mean_abs_drift:.3f}**",
        f"- Median score change (new − old): **{median_drift:+.3f}**",
        "",
        "## New columns",
        "",
    ]
    for col in added_vars:
        lines.append(f"- `{col}`")
    lines.extend(["", "## Sample new MAL ids (first 25)", ""])
    lines.append(", ".join(str(x) for x in added[:25]) or "(none)")
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    return {
        "new_titles": len(added),
        "removed_titles": len(removed),
        "new_variables": len(added_vars),
        "mean_abs_score_drift": mean_abs_drift,
        "shared_scored": len(both_scored),
    }
