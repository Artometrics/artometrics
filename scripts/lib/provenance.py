"""SOURCE.txt + SHA256 helpers for frozen data extracts."""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def write_source_txt(
    dest: Path,
    header_lines: list[str],
    artifact_paths: list[Path],
) -> None:
    lines = list(header_lines)
    lines.append("")
    lines.append("SHA256 (committed artifacts):")
    for p in sorted(artifact_paths):
        if p.exists():
            rel = p
            try:
                rel = p.relative_to(dest.parent.parent.parent)
            except ValueError:
                pass
            lines.append(f"- {rel}: {sha256_file(p)}")
    lines.append(f"Generated: {datetime.now(timezone.utc).isoformat()}")
    dest.write_text("\n".join(lines) + "\n", encoding="utf-8")
