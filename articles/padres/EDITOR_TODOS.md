# Padres R2 — editor research todos (round 2)

**Agent run:** 2026-10-11 (Kyle's Mac mini worker).  
**Source cards (full citations):** `~/worker/padres-round2/source-cards-round2.md` and Google Drive `Artometrics/Padres/Reading/source-cards-round2.md` (sync attempted).  
**Raw captures:** `~/worker/padres-round2/` (`data/`, `press/`, `papers/`, `transcripts/`).

## Priority checklist

| Item | Status | Where captured |
|------|--------|----------------|
| Spotrac luxury-tax payrolls 2021–26 | **Found** | `data/payroll_tax_spotrac.csv`; HTML `~/worker/padres-round2/data/spotrac_tax_*.html` |
| Cot's / remaining contract guarantees | **Partial / needs Kyle** | Cot's BP page blocked (Anubis bot wall). Spotrac cap HTML saved; no parsed team guarantee total. Article $858M still from prior reporting. |
| DTC + season membership counts | **Found** | SBJ Oct 2025 (~70k DTC; ~25k STM; 3-year wait list); SBJ Jan 2026 sellout; MLB waitlist page |
| Farm ranks (Pipeline / FanGraphs / BA) | **Partial** | BA July 2026 HTML: **30th**; FanGraphs dead last per secondary coverage; MLB Pipeline **not fetched** (needs Kyle or manual) |
| Diamond / Bally May 2023 exit + dollars | **Found** | CNBC/AP/UT: 20-year **$1.2B** Fox deal (2012); ~**$60M+/yr** lost; payments stopped May 2023 |
| Kroc 1974 + Washington move | **Found** | UT ownership history / MLB.com feature / SABR: **$12M**; Danzansky Washington sale fell through |
| 1990 / 1994 / 2012 sale prices | **Found** | UT: Werner **$75M** (1990); Moores **~$80M** (1994); MLB.com **$800M** (2012) |
| Prop C 1998 + Petco cost | **Found** | LAT Prop C **$411M** plan; SABR/UT final **~$453.4M**; Berkeley PDF saved |
| Seidler trust litigation | **Found** | Courthouse News complaint PDF; UT/10News Feb 2026 partial settlement |
| Cohen Mets 2020 price | **Found** | Sportico: **$2.42B** (prior MLB sale record) |
| Sale legal closing after Aug 17 2026 | **Found** | MLB press release **Aug 17 2026** unanimous approval; closing "coming days"; intro presser **Aug 24** per MLB news |
| Academic papers (to-get list) | **Partial** | Berkeley Petco PDF; Hakes & Sauer AEA PDF **403** from worker IP; several Unpaywall searches empty — **needs Kyle** |
| Forbes valuations 2012–26 | **Partial** | 2017–26 on Forbes team page; 2013 & 2015 via Forbes/KPBS; **2012/2014/2016** not in carousel — **needs Kyle** archive pass |
| YouTube transcripts (8–15) | **Blocked** | Video IDs catalogued; YouTube **429/IP block** on worker after yt-dlp — **needs Kyle** (`mlx-whisper` on Mac mini) |

## Numeric notes for charts

- Spotrac **competitive balance tax** totals are in `data/payroll_tax_spotrac.csv`. Article chart uses slightly different 2026 figure ($259.1M) — reconcile against Spotrac on Kyle's pass (may be snapshot date).
- Forbes **March 2026** team value **$3.1B** (Revenue $452M; Operating income -$1.3M per team page). Agreed sale **$3.9B** (Sportico Apr 17 2026; AP May 2026).

## Still needs Kyle

1. **Cot's Baseball Contracts** (`legacy.baseballprospectus.com/compensation/cots/san-diego-padres/`) — browser session; export guarantee table.
2. **Spotrac** team **remaining guarantees** total (cap or contracts summary) to verify **$858M**.
3. **MLB Pipeline** midseason 2026 Padres rank (free page).
4. **FanGraphs** farm ranking page scrape (prospects URL returned empty table to curl).
5. **Forbes** 2012, 2014, 2016 Padres values from annual list articles (Wayback or Forbes archive).
6. **Paywalled papers** + **AEA PDF** for Hakes & Sauer (download from institutional network).
7. **YouTube**: run `mlx-whisper` / yt-dlp with home IP on catalog in `source-cards-round2.md` § YouTube.
8. **Google Drive**: if `Reading/` mkdir failed with FUSE deadlock, retry sync: `rsync -av ~/worker/padres-round2/ "$GDRIVE/Padres/Reading/"`

## Files added this round (repo)

- `articles/padres/data/payroll_tax_spotrac.csv`
- `articles/padres/data/forbes_valuations.csv`
- `articles/padres/EDITOR_TODOS.md` (this file)
