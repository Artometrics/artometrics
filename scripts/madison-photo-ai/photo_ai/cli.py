from __future__ import annotations

import argparse

from .pipeline import run_pipeline


def main() -> None:
    p = argparse.ArgumentParser(description="Madison photo intelligence pipeline")
    p.add_argument("--limit", type=int, default=None, help="Process only N images (eval)")
    p.add_argument("--no-firestore", action="store_true", help="Skip Firestore/Storage writes")
    p.add_argument("--skip-caption", action="store_true", help="Skip Ollama vision captions")
    args = p.parse_args()
    stats = run_pipeline(
        limit=args.limit,
        write_firestore=not args.no_firestore,
        skip_caption=args.skip_caption,
    )
    print(stats)


if __name__ == "__main__":
    main()
