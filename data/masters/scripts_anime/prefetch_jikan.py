"""Warm the Jikan/Tenrai disk cache in priority order (new titles first), resumable.

Usage: python prefetch_jikan.py --snapshot ../../data/anime/anime_2026-10-11.csv [--deadline-hours 6]
Then run refresh.py --max-jikan 0 --no-jikan-seasons to rebuild from cache.
"""
from __future__ import annotations
import argparse, logging, time
import pandas as pd
from config import BASELINE_CSV
from jikan_client import JikanClient, _read_cache
from refresh import load_jikan_state, save_jikan_state

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("prefetch")

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--snapshot", required=True)
    p.add_argument("--deadline-hours", type=float, default=6.0)
    a = p.parse_args()
    ids = pd.read_csv(a.snapshot, usecols=["animeID"])["animeID"].astype(int).tolist()
    base = set(pd.read_csv(BASELINE_CSV, usecols=["animeID"])["animeID"].astype(int))
    new = sorted((i for i in set(ids) if i not in base), reverse=True)
    old = sorted((i for i in set(ids) if i in base), reverse=True)
    order = new + old
    log.info("ids=%s new=%s old=%s", len(order), len(new), len(old))
    done = load_jikan_state()
    jk = JikanClient()
    end = time.time() + a.deadline_hours * 3600
    fetched = fails = consec = 0
    try:
        for n, mid in enumerate(order, 1):
            if time.time() > end:
                log.warning("deadline reached at %s/%s", n, len(order)); break
            if mid in done and _read_cache(f"anime_full:{mid}") is not None:
                continue
            data = jk.get_anime_full(mid)
            if _read_cache(f"anime_full:{mid}") is not None:
                done.add(mid); fetched += 1; consec = 0
            else:
                fails += 1; consec += 1
                if jk.unreachable:
                    log.warning("unreachable; pausing 120s"); time.sleep(120); jk.unreachable = False
                if consec >= 25:
                    log.error("25 consecutive failures; stopping"); break
            if n % 100 == 0:
                save_jikan_state(done)
                log.info("progress %s/%s fetched=%s fails=%s (new done=%s)", n, len(order), fetched, fails, sum(1 for i in new if i in done))
    finally:
        save_jikan_state(done); jk.close()
    log.info("FINISHED fetched=%s fails=%s done_total=%s new_done=%s/%s", fetched, fails, len(done), sum(1 for i in new if i in done), len(new))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
