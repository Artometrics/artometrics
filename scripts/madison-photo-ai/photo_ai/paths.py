import re
from dataclasses import dataclass
from pathlib import Path

from .config import STAGING_ROOT

WORK_RE = re.compile(r"^work/([^/]+)/(\d+)\.jpg$", re.I)


@dataclass(frozen=True)
class ImageRef:
    image_id: str
    storage_path: str
    local_path: Path

    @property
    def shortcode(self) -> str:
        return self.image_id.rsplit("_", 1)[0]


def storage_path_from_parts(folder: str, index: str) -> str:
    return f"work/{folder}/{index}.jpg"


def image_id_from_storage_path(storage_path: str) -> str:
    m = WORK_RE.match(storage_path.replace("\\", "/"))
    if not m:
        raise ValueError(f"Unexpected storage path: {storage_path}")
    folder, num = m.group(1), m.group(2)
    return f"{folder}_{num}"


def discover_local_images(staging_root: Path = STAGING_ROOT) -> list[ImageRef]:
    work = staging_root / "work"
    refs: list[ImageRef] = []
    if not work.is_dir():
        return refs
    for folder in sorted(work.iterdir()):
        if not folder.is_dir():
            continue
        for jpg in sorted(folder.glob("*.jpg"), key=lambda p: int(p.stem)):
            sp = storage_path_from_parts(folder.name, jpg.stem)
            refs.append(
                ImageRef(
                    image_id=image_id_from_storage_path(sp),
                    storage_path=sp,
                    local_path=jpg,
                )
            )
    return refs
