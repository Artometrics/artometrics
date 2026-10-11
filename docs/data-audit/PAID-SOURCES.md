# Paid and subscription data sources — research memo

**Status:** Informational research for Artometrics editorial and data engineering. **Not procurement advice or legal guidance.** Verify price, license, and publication rights with each vendor before signing or publishing.

**Audience:** Small independent data-journalism shop (anime/media, franchises & IP, box office, MLB, healthcare, YouTube/creators, consumer markets).

**Related:** [`AUDIT.md`](./AUDIT.md) (free/open inventory), [`candidate_sources.csv`](./candidate_sources.csv) (API-first upgrades).

**Price as of:** Public web pages and vendor docs reviewed **October 2026**; enterprise products change frequently.

---

## How to read the tables

| Column | Meaning |
| --- | --- |
| **Price tier** | Typical entry cost; “Quote” = no public list price |
| **Publish charts?** | Whether contract terms *commonly* allow publishing **derived** statistics/graphics (not raw dumps). Always confirm in writing. |
| **API** | Self-serve programmatic access vs export-only vs none |
| **Value (us)** | **High** = directly strengthens Tier A reports; **Med** = useful cross-check or desk-specific; **Low** = niche or poor fit at our scale |

---

## 1. Vendor catalog (requested candidates)

### Media, franchises, box office, streaming

| Source | Price tier (indicative) | What you get | License / publish derived work | API | Value (us) |
| --- | --- | --- | --- | --- | --- |
| **Statista** | Free (limited); **Starter ~$199/mo** (annual); **Personal ~$649/mo**; **Professional/Enterprise = quote** (often $10k+/yr) | Premium stats, Market Insights, reports, Research AI | **Publication rights included on Professional+**, not on individual Starter/Personal per Statista’s plan matrix — cite Statista as source | Statista Connect (enterprise add-on) | **Med** — fast context stats; weak for reproducible primary research; expensive for real publication rights |
| **Luminate** (music/film/TV CONNECT) | **Quote**; promo **~$495/mo** (12-mo, label/distributor eligibility); **Luminate Intelligence ~$995/yr** (SMB) | Streaming/airplay/sales by ISRC, artist rankings, global consumption | Commercial license; redistribution restricted — charts usually need license review | **Music API** + Snowflake shares (separate subscription) | **Med** for music/streaming crossover; **Low** for anime-first unless music-IP angle |
| **The Numbers** (site) | **Free** public grosses with limits | Domestic BO, some budgets, research articles | Site **ToS**; editorial use of **facts** generally OK; bulk reuse restricted | No official API | **High** for franchise theatrical work — pair with manual archive + [`candidate_sources`](./candidate_sources.csv) TMDB/SEC |
| **The Numbers Pro / Business Report** | **~$69/mo** (promos ~$99/3 mo); **OpusData** = quote (commercial/academic/press tiers) | Forecasts, bankability, deeper industry analysis | Subscription content — **do not republish report PDFs**; derived charts from **licensed OpusData** need contract | OpusData for licensees | **Med–High** if doing recurring BO forecasting; press may get **one-off extracts** via support@the-numbers.com |
| **Comscore** | **Quote** (enterprise; often five–six figures/yr) | Cross-platform measurement, OTT, campaigns | Strict — typically **no** public redistribution of raw panels | Client integrations | **Low** at indie budget — use Nielsen press + Parrot lite |
| **Parrot Analytics** | **DEMAND360 Lite ~$99/mo** (self-serve); enterprise DEMAND360 = quote | Global “demand” scores, rankings, streaming economics reports | Subscription — publish **your analysis**, not their UI exports wholesale; check attribution | Limited on Lite; enterprise APIs | **High** for streaming/franchise demand narratives at **$99** entry |
| **Nielsen** | **Quote** (Gauge/Distributor Gauge = enterprise); **press releases free** | TV usage, distributor share (what Artometrics already cites for YouTube) | **Press figures** OK with attribution; **subscription data** not redistributable | Partner APIs only | **Med** — use **free press PDFs** + manual tables; skip full Nielsen unless sponsor |

### Sports (MLB)

| Source | Price tier | What you get | License / publish | API | Value (us) |
| --- | --- | --- | --- | --- | --- |
| **FanGraphs** | **$15/mo** / **$80/yr** / **$200/3yr**; MVP **$500/yr** | Advanced stats, projections, ad-free | **Membership ToS** — editorial citation OK; **not** a data vendor license for bulk republication of their tables | No data API | **Med** — analysis & leaderboards for **padres/yankees** prose; Lahman remains primary |
| **Baseball Prospectus** | **~$75–100/yr** premium tiers; **~$20/mo** monthly | PECOTA, scouting, fantasy tools | Same as FanGraphs — journalism cites, don’t resell their CSVs | No | **Med** for projection context |
| **Sports Info Solutions (SIS)** | **Quote** (teams/media; typically thousands+/yr) | Batted-ball tags, defensive runs, pitch typing beyond public Statcast | **Proprietary** — publication requires media deal | Team/media feeds | **Low** at our budget — use **Baseball Savant + Lahman** |
| **MLB Stats API / Savant** | **Free** (unofficial/stable-ish) | Stats, Statcast exports | **MLB ToS** — attribute MLBAM | Unofficial JSON | **High** (free) — see open registry |

### Healthcare

| Source | Price tier | What you get | License / publish | API | Value (us) |
| --- | --- | --- | --- | --- | --- |
| **Definitive Healthcare** | **Quote**; third-party benchmarks **~$25k–60k+/yr** small team | Hospital profiles, affiliations, claims modules, IDN intelligence | **Commercial** — no casual publishing of raw exports | Enterprise API add-on | **Low** for indie — **CMS public data** covers **readmitted**; use Definitive only for sales-side hospital strategy pieces |
| **CMS / Care Compare / HCRIS** | **$0** | HRRP, quality, cost reports | **U.S. public domain** | data.cms.gov | **High** (free) |

### YouTube, creators, social

| Source | Price tier | What you get | License / publish | API | Value (us) |
| --- | --- | --- | --- | --- | --- |
| **YouTube Data API v3** | **Free quota**; Google Cloud overage | Video/channel metadata, stats | **Google ToS** — store minimally, attribute | Official REST | **High** (already in **youtube** / h3) |
| **Social Blade** (Premium) | **~$60–600+/yr** tiers | UI analytics, projections, live counts | **ToS** — screenshots/figures for journalism usually OK; **Business API** separate | **Business API**: prepaid credits from **~$50/100 credits** (~$0.50/credit/profile) | **Med** — trend charts; API expensive at scale |
| **VidIQ** | **Free**; **Pro ~$7.50/mo** (annual); **Boost ~$39/mo**; coaching **$415+/mo** | SEO, keywords, competitor tracking, AI credits | Creator tool — **not** a licensed data product for republication | No public data API on low tiers | **Low–Med** — writer tooling, not primary sourcing |
| **Similarweb** | **Free sample**; **Starter ~$125/mo** (annual) or **$199/mo** | Traffic estimates, keywords, competitors | **ToS** — publish **aggregated insights**, not bulk export | Limited on Starter | **Med** for **youtube** vs Netflix web traffic claims |

### Companies, markets, industry research

| Source | Price tier | What you get | License / publish | API | Value (us) |
| --- | --- | --- | --- | --- | --- |
| **Crunchbase** | **Pro ~$99/mo** (monthly); Enterprise = quote | Private company funding, investors, exports (row caps) | **ToS** — charts from **your analysis** generally OK; respect export limits | Crunchbase API (higher tiers) | **Med** for M&A / studio ownership stories |
| **PitchBook** | **Quote** (often **$20k+/yr** per seat) | PE/VC deals, valuations, cap tables | **Strict** — essentially no public redistribution | Licensed API | **Low** unless franchise/M&A desk funded |
| **IBISWorld** | **Quote** (~$2k–5k+/report or portal subs) | Industry reports, NAICS narratives | **Report text** cannot be republished verbatim; **derived stats** with attribution sometimes OK | Limited | **Med** for consumer/market primers — prefer **Census/BLS** |
| **Euromonitor** | **Quote** (enterprise) | Global consumer markets, brand shares | Same as IBISWorld | Passport API (enterprise) | **Low–Med** unless international consumer desk grows |

### Data marketplaces, proxies, automation

| Source | Price tier | What you get | License / publish | API | Value (us) |
| --- | --- | --- | --- | --- | --- |
| **Kaggle** | **$0** (datasets) | Community datasets, notebooks | **Per-dataset license** (CC, NC, etc.) — **check each** | Download / API via kernels | **Med** — discovery only; many Artometrics pieces already use TidyTuesday/Kaggle mirrors |
| **data.world** | **Free** tier; **Team/Enterprise** quote | Dataset hosting, collaboration, some connectors | Host **your** data; third-party sets vary | REST | **Low–Med** — internal data catalog, not primary vendor |
| **Bright Data** | **PAYG** proxies **~$4–8/GB** residential; scraper APIs **~$500+/mo** commitments | Proxies, Web Unlocker, Scraping Browser, SERP | **Infrastructure** — you own output **if** target site ToS allows | Yes | **Med** as **gap-fill** when no API — **legal review mandatory** |
| **Oxylabs** | Similar to Bright Data (**PAYG GB** + enterprise) | Residential/datacenter proxies, scraper APIs | Same | Yes | **Med** — alternative to Bright Data |
| **Apify** | **Free $5/mo credits**; **Starter ~$19–39/mo**; **Scale $199/mo**; **Business $999/mo** | Actor marketplace (scrapers), scheduling, storage | **You** responsible for target site compliance; Apify hosts execution | First-class REST | **High** for **repeatable** extracts (BOM pages, press tables) **after** ToS review |

---

## 2. How data newsrooms source (public practices)

Patterns observed across shops Artometrics often cites as quality bars. These are **descriptive**, not endorsements.

| Outlet | Typical sourcing mix | Notes for a small shop |
| --- | --- | --- |
| **The Pudding** | **FOIA** (e.g. NOAA marine mammal inventory), **crowdsourced** supplements (Ceta-Base), **manual digitization** (newspaper archives), **open GitHub** data repos per story | Gold standard for **provenance READMEs** — mirror with `SOURCE.txt` + SHA256 |
| **FiveThirtyEight / 538** | **Public polls**, sports leagues, government stats; **GitHub CC BY 4.0** data releases; heavy **methodology** pages | Model: publish **data + code** alongside story; pollster review process for corrections |
| **Our World in Data** | **Official international agencies** (UN, World Bank, OECD), academic papers, **open licenses** | Prefer **primary agency** over secondary stat portals |
| **The Economist data team** | **Official statistics**, **EIU** (in-house), surveys, **academic** partners | In-house macro data — indie equivalent = **FRED + World Bank + OECD** |
| **Bloomberg Graphics** | **Bloomberg terminal** (proprietary), filings, surveys, **custom collection** | Terminal = **$$$**; indie path = **SEC EDGAR + FRED + BLS** |
| **Axios** | **Wire sources**, polls, company announcements, **expert interviews** | Less raw-data-heavy; good for **deadline context** |

### Tactics worth copying (legal)

1. **FOIA / public records** — federal and state (healthcare, education, transit). Slow but defensible.
2. **Academic partnerships** — university IRB-safe datasets, co-authorship, shared grant costs.
3. **Press / research desks** — Nielsen, Luminate, OpusData, Statista sometimes offer **story-specific** extracts; ask explicitly for **publication rights**.
4. **Data-sharing agreements** — memorialize license, embargo, attribution, and **derivative chart** rights.
5. **Crowdsourcing + validation** — community datasets (Wiki-style) only with **duplicate checks** (Pudding cetaceans model).
6. **Open-first pipeline** — freeze primary extracts in `articles/<slug>/data/raw/` (per `docs/master/03_DATA_SOURCES_AND_REGISTRY.md`).

---

## 3. Grey areas (informational only — not recommended)

Some organizations have used practices below. Artometrics should treat this table as **risk disclosure**, not a playbook.

| Practice | Why teams do it | Legal / ToU risk | Safer alternative |
| --- | --- | --- | --- |
| **Scraping sites that prohibit automated access** (BOM, MAL, Spotrac) | No API; public HTML | **CFAA / contract (ToS)** exposure; cease-and-desist | Manual CSV archive; licensed **OpusData**; **TMDB/SEC**; **Apify** only with counsel + robots review |
| **Reusing paywalled tables** (Statista screenshot, WSJ chart) | Speed | **Copyright**; vendor **license breach** | Buy **publication tier**; cite **primary** source Statista aggregated |
| **Unofficial APIs** (MLB stats.nba.com-style, scraped GraphQL) | Stability vs official | **IP/ToS**; breakage | Official or **documented** open data (Lahman, CMS, EDGAR) |
| **Sharing login-gated exports** among staff in cloud | Collaboration | Violates **seat license** | Vendor **team** plan or internal DB with license |
| **PUBLISHING raw Nielsen/Parrot/Comscore panels** | “Data journalism” | **Contract violation** | Publish **your aggregates** with vendor approval + attribution |
| **Kaggle NC datasets in commercial magazine** | Convenience | **License violation** | Use **CC0/CC-BY** sets or get owner permission |
| **Residential proxies to bypass geo/block** | Access | **Fraud/ToS** on target + proxy AUP | Official regional API or licensed partner |
| **IMDb non-commercial dump on commercial site** | Coverage | **IMDb ToS** — commercial use blocked | **TMDB** with attribution |
| **YouTube bulk download / re-host** | Offline ML | **YouTube ToS** | **Data API** metadata only; link out to videos |
| **Definitive/CMS “merge” without hospital consent** | Story | **HIPAA** not in play for public CMS, but **re-identification** care | Aggregate to **state/condition**; suppress small *n* |

---

## 4. Recommended starter stacks (monthly burn)

Assumes **U.S.-focused** investigative reports, **open data first**, paid tools only where they replace fragile manual work.

### ~$0 / month (baseline Artometrics today)

| Layer | Tools |
| --- | --- |
| Anime / culture | **Jikan/AniList** (free APIs), TidyTuesday archives, **Wikidata** |
| MLB | **Lahman**, Baseball-Reference manual supplements, **Baseball Savant** exports |
| Franchise / film | **SEC EDGAR**, **TMDB** (free key), manual BOM tables, **BLS CPI** |
| Healthcare | **CMS** Provider Data Catalog, Care Compare |
| YouTube | **YouTube Data API** (quota), **SEC** Alphabet filings, **Nielsen press releases** |
| Infra | **GitHub** frozen CSVs, `npm run brief:*`, optional **Apify Free** ($5 credits) for experiments |
| **Skip** | Statista, Nielsen subs, Definitive, PitchBook, Bright Data at volume |

### ~$50 / month (single editor + data)

| Allocation | ~Cost | Purpose |
| --- | --- | --- |
| **Parrot DEMAND360 Lite** | $99 | *Stretch:* drop to **$0** and use press — or **The Numbers Business Report** ~$69 if BO-heavy quarter |
| **FanGraphs** annual amortized | ~$7 | MLB analysis depth |
| **Crunchbase Pro** (1 month on/off) | $99 | *Optional spike* for M&A month — not continuous |
| **Apify Starter** | $19–39 | Scheduled **Actors** for BOM/yearly pages **after** ToS sign-off |
| **Realistic $50 mix** | **~$39 Apify Starter** + **~$7 FanGraphs** + free CMS/SEC | Automation + baseball; streaming demand from **free Nielsen PDFs** |

*Note:* True **$50** all-in is tight; the highest ROI single paid line is often **Apify Starter** (repeatable extracts) or **one** industry newsletter (**Numbers** ~$69).

### ~$200 / month (serious indie desk)

| Allocation | ~Cost | Purpose |
| --- | --- | --- |
| **Parrot DEMAND360 Lite** | $99 | Streaming/franchise demand cross-check |
| **The Numbers Business Report** | $69 | Theatrical forecasting + industry features |
| **Apify Starter / light Scale** | $39–79 | BOM, press tables, social archives |
| **VidIQ Pro** (optional) | ~$8 | Creator-economy research UX |
| **Social Blade API credits** | ~$50 one-time as needed | Channel trajectory snapshots |
| **Buffer / contingency** | remainder | **Crunchbase Pro** one month per quarter for deal stories |

**Still defer:** Statista Professional (publication rights), Nielsen enterprise, Definitive, PitchBook, Similarweb Starter ($125+), Luminate full CONNECT — until revenue or grant funds them.

---

## 5. Fit with Artometrics Tier A reports

| Report | Paid source most aligned | Free-first path |
| --- | --- | --- |
| **anime** | — | Jikan/AniList refresh |
| **franchise** | Numbers Pro + Parrot; OpusData if budget | SEC + TMDB + manual BOM |
| **padres** | FanGraphs/BP (analysis only) | Lahman + Savant |
| **readmitted** | — | CMS only |
| **youtube** | Parrot; Social Blade API spot checks | SEC + Nielsen press + YouTube API |
| **poison** | Numbers (BO case studies) | Franchise ledger refresh |

---

## 6. Maintenance

- Re-verify **public pricing** before purchase; link vendor **Terms** and **Data use** PDFs in `articles/<slug>/data/SOURCE.txt` when licensed.
- Add paid feeds to [`datasets.csv`](./datasets.csv) when subscribed (new rows: `license=commercial`, `obtained_via=subscription`).

**Document owner:** Artometrics research desk — generated October 2026 alongside PR #89 data audit.
