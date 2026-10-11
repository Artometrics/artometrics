# Magazine upgrade plan — artometrics.com

**Scope:** Design and documentation only (this PR). No production code changes.

**Evidence:** `screenshots/artometrics-*.png` (live site, Oct 2026), `screenshots/lex-hemingway-*-local.png` (target patterns), `mockups/home-magazine-after.html` (static “after” comp).

---

## Part B — What makes a site feel like a magazine (public patterns)

Observed from public pages only (The Economist, Financial Times, Bloomberg Businessweek, The Pudding, WSJ Graphics, Wired). These are **patterns**, not assets to copy.

| Publication | Pattern | Artometrics application |
|-------------|---------|-------------------------|
| **The Economist** | Strong **section fronts** (Finance, Culture) with identical grid grammar; red accent reserved for urgency | Desk pages `/desks/[desk]` as weekly fronts; red for breaking data only |
| **Financial Times** | **Pink/salmon** brand bar + dense multi-column home; clear **lead** vs **briefs** | Optional top “market data” mono strip; home lead story dominates viewport |
| **Bloomberg Businessweek** | **Bold cover** imagery + oversized headline; issue metaphor | Treat each Friday report as a “cover” with full-bleed hero |
| **The Pudding** | **Scrolly** charts tied to copy; figure stays in view while text advances | Phase 2 for select investigations; keep static PNG fallback |
| **WSJ Graphics** | **Chart as exhibit**: title, subtitle, source, byline outside the plot | Wrap every Plotly block in `figure.art-exhibit` |
| **Wired** | **Tag-led** discovery + high-contrast display type | Uppercase mono section labels (already started on home) |

**Cross-cutting magazine signals**

1. **Issue rhythm** — Dated bundles (“This week”, “Friday release”) not an infinite scroll of equals.
2. **Typographic contrast** — Display size jumps between lead and briefs (2–3×), not 30px vs 23px.
3. **Editorial furniture** — Bylines, datelines, figure numbers, continuation markers.
4. **Column variation** — 1-col prose vs 3-col home vs full-bleed figure; avoid one `max-w` everywhere.
5. **Restrained chrome** — Nav recedes; content shouts.
6. **Photography as cover** — Crop for drama; captions credit sources.

---

## Part C — Why artometrics.com does not feel like a magazine yet

### Home (`/` — `HomeMagazine.tsx`)

| Observation | Why it reads “blog” |
|-------------|---------------------|
| See `screenshots/artometrics-home.png` | Lead story is **text → small bordered image**; magazines lead with **cover scale** imagery or a dominant display line |
| Gold/warm tokens (`Colors.ts`) | Palette says **literary journal**, not Kruger/anaglyph data magazine in `docs/design-system/` |
| Secondary stories | Horizontal thumb + title is **RSS reader**, not FT/BW brief column |
| “Editor’s picks” rail | Useful, but **weak typographic step-down** from lead; all items feel same weight |
| No issue band | Missing “Week of …” / release calendar tie-in (`docs/content-os/content-calendar.csv`) |
| Header | Center logo + uppercase gold links — **brand** reads, but no **dateline** or “Reports” volume signal |

### Reports index (`/blog`)

| Observation | Issue |
|-------------|-------|
| `screenshots/artometrics-blog-index.png` | Likely card grid parity with home; no **journal** cover line or single featured investigation |

### Article template (`/[slug]` — e.g. readmitted

| Observation | Issue |
|-------------|-------|
| `screenshots/artometrics-readmitted.png` | **50/50 hero + headline** split reads as CMS template; magazines stack **display title** then **full-width figure** |
| Headline treatment | Slug in accent + subtitle is on-brand for data, but size stops at ~42px — not **cover scale** |
| Typography stack | `global.css` loads **Piazzolla/Archivo** while design system specifies **DM Sans**; split identity |
| Body | Quarto HTML + `artometrics-article.css` is capable, but chart blocks float without **exhibit framing** |
| Nav chrome | Breadcrumb + actions row competes with headline for first attention |

### Charts & data

- Plotly embeds inherit web defaults; missing consistent **DM Mono axes**, **figure label**, **source line**
- Key stats (`ReportStatGrid`) help but sit **above** body without narrative bridge

### Navigation & imagery

- Primary nav lists desks but home does not **mirror** newspaper sections (no “Contents” jump)
- Hero images often **contain** in bordered box — magazines **bleed** or crop boldly
- Vertical rhythm: even `gap-8` spacing — magazines use **rules** and **whitespace blocks** alternation

### Repo vs live

- Quarto pipeline (`articles/<slug>/`, `artometrics-article.css`) can exceed Expo wrapper polish — **two visual systems** on one URL

---

## Part D — Prioritized upgrade plan

### P0 — Brand alignment (1 PR, low risk)

1. **Unify magazine fonts** — DM Sans body/display, DM Mono data site-wide; Piazzolla/Archivo → Swiss edition only or remove from default magazine (`global.css`, `Colors.ts` `MagazineFonts`).
2. **Token swap** — Gold paper/ink → white/black + anaglyph red/blue (`tokens.md`) in `uniwind-theme` + Tailwind theme.
3. **Header dateline** — Mono strip: `ARTOMETRICS · {date} · DATA REPORTS` under masthead.

**After:** Mockup `mockups/home-magazine-after.html` (typography + colors only).

### P1 — Home as a front page

4. **Lead layout** — Northbound-style asymmetric lead (image 2/3, story 1/3) or Hemingway text-first with **full-bleed** image break below title.
5. **Section rules** — 2px black `border-t` between home bands (Hemingway `BlogPreview` pattern).
6. **Friday issue row** — Pull next 3 slugs from content calendar; label “This week’s investigations”.
7. **Deprioritize grid** — Top stories grid becomes **briefs** (mono title list), not another card row.

### P1 — Article as cover story

8. **Reorder hero** — Title block (display) → full-width hero → byline band → stats → body (Hemingway sticky title optional phase).
9. **Figure exhibit component** — Shared wrapper for charts/images (caption, source, download).
10. **Harmonize Quarto + Expo** — Same `--art-*` vars in `artometrics-article.css` and app shell.

### P2 — Desk fronts & index

11. **Redesign `/blog`** — Outkast `JournalHero` + 3-col grid.
12. **`/desks/[desk]`** — Section front with lead + 4 briefs (Economist grammar).

### P2 — Data storytelling

13. **Plotly theme** — Central `lib/charts/plotlyTheme.ts` from tokens.
14. **Scrolly template** — One pilot slug (Pudding pattern) with static fallback.

### P3 — Motion & delight

15. Lenis on home only; Semplice ribbon on `/about` or special editions.
16. Progress bar stays (already on-brand red).

---

## Before / after references

| View | Before | After (mock) |
|------|--------|----------------|
| Home | `screenshots/artometrics-home.png` | `mockups/home-magazine-after.html` (open in browser) |
| Article | `screenshots/artometrics-readmitted.png` | Hemingway `screenshots/lex-hemingway-article-local.png` (pattern reference) |
| Blog index | `screenshots/artometrics-blog-index.png` | (Future mock in P2) |

---

## Success metrics (qualitative)

- First-time visitor describes site as **“magazine / publication”** not “blog” or “news site”
- Lead story identifiable in **< 2 seconds** (squint test)
- Charts cite **source** without scrolling into body
- Brand recognizable in **B&W thumbnail** (anaglyph red/blue accents)

---

## Base theme recommendation

**Hemingway** — blog + podcast + authors + subscribe + article layout maps 1:1 to Artometrics routes; STIX/Inter pairing is replaceable with DM Sans while keeping layout DNA. Layer **Semplice** captions and **Northbound** lead asymmetry via `components.md` recipe.
