# AGENTS.md — Artometrics

This file describes **this repo only** — the Artometrics magazine product at [artometrics.com](https://artometrics.com).

## What this project is

Artometrics is an independent **data-science magazine and creative platform** for the creative industries and culture. It publishes editorial data reports (with reproducible charts and public datasets), a podcast, author profiles, legal/ethics pages, membership flows, **Studio** (Twilda + Aftercare on one Supabase profile), public member profiles, and a publish/social layer.

Primary use case: long-form investigative reports by editorial desk, plus subscriber podcast episodes, Studio creative tools, member profiles, and published writing — on **web and native** from one Expo codebase.

Platform UX plan: `docs/PLATFORM_UX_PLAN.md`.

## Tech stack

From `package.json` and `app.json`:

- **Expo** `~57` + **Expo Router** (file-based routes in `app/`)
- **React Native** / **React Native Web** (static web export via `expo export -p web`)
- **Content:** markdown in `src/content/*` → `scripts/build-content.mjs` → `src/generated/*.json` (Sanity is the target editorial CMS — see `sanity/` + `docs/SANITY_SETUP.md`)
- **Charts:** Plotly on web (`components/ArticleBody.web.tsx`); PNG fallbacks on native WebView
- **Membership / social:** `@supabase/supabase-js`, Stripe via Netlify functions; private tools + member posts + comments/follows in Supabase
- **Site URL:** `https://artometrics.com` (`EXPO_PUBLIC_SITE_URL`)

## Folder map

| Area | Path | Notes |
|------|------|-------|
| Routes | `app/` | Expo Router (`(site)` chrome + screens) |
| Components | `components/` | Header, footer, cards, article body |
| Lib | `lib/` | Content accessors, auth, Supabase, plans |
| Brand tokens | `constants/Colors.ts` | Accent red + base neutrals |
| Content (source) | `src/content/` | Markdown/MDX per collection |
| Content (built) | `src/generated/` | JSON consumed by the app |
| Article homes | `articles/<slug>/` | Rainfall-style Quarto monorepo — one folder per report (`_quarto.yml`, `.qmd`, `data/`, `charts/`); gold prototype `articles/readmitted/` |
| Scripts | `scripts/` | Content build, GitHub article sync, READMITTED render/sync |
| Styles (articles) | `public/css/artometrics-article.css` | Quarto/article chrome |
| Public assets | `public/` | Images, audios, chart JSON, fonts |
| Native assets | `assets/` | Icons, splash, Chomsky font |
| Brand SVG kit | `brand/svg/` | Monogram, wordmark, lockups (mirrored to `public/images/brand/svg/`) |
| Reference catalogs | `public/data/reference/` | Gutenberg / WikiArt / Wikipedia JSON |
| Studio / tools | `app/(site)/studio/`, `app/(site)/tools/`, `lib/twilda/`, `lib/aftercare/`, `lib/samples/`, `lib/palette/`, `lib/platform/` | Studio home + Twilda/Aftercare/Sample Maker/Color Kit |
| Profiles / social | `app/(site)/u/`, `app/(site)/me.tsx`, `app/(site)/following.tsx` | Public profiles, hub, following feed |
| Sanity | `sanity/` | Editorial CMS schemas + Studio (optional package) |
| Netlify | `netlify/` + `netlify.toml` | Functions + redirects (incl. `/api/aftercare/*`, platform APIs) |

Path alias: `@/*` → project root (`tsconfig.json`).

## Content collections

Schemas are enforced by `scripts/build-content.mjs` (not Astro Zod).

### `blog` — `src/content/blog/`

- Required frontmatter: `title`, `slug`, `pubDate`, `description`, `heroImage`, `tags` (`[domain, subdomain]` — domains: `arts|sports|science|humanities|civics|culture`; see `data/sections.ts` for the 43 subdomains)
- Optional: `draft`, `author`, `tldr`, `keyPoints`, `faq`, `audioSrc`
- Body is HTML (narrative magazine prose; Plotly charts preserved)
- Voice: professional, objective, insightful, no fluff — named/dated facts only
- Template: `src/content/blog/anime.md` (gold monorepo prototype: `readmitted`)
- Import: monorepo `articles/<slug>/` via `npm run sync:readmitted` (gold path); older pieces may still use `npm run sync:articles`

### `authors` — `src/content/authors/`

- Required: `name`, `image: { url, alt }`
- Optional: `role`, `bio`, `socials`
- Template: `src/content/authors/juliet-ramos.md`

### `podcast` — `src/content/podcast/`

- Required: `title`, `pubDate`, `description`, `author`, `image`, `guestAvatar`, `tags`
- Optional: `episodeNumber`, `duration`, `audioSrc`, `isRecent`, `isPopular`, `isLocked`
- Template: `src/content/podcast/1.md`

### `legal` — `src/content/legal/`

- Required: `page`, `pubDate`
- Template: `src/content/legal/ethics-statement.md`

## Routing conventions

- **Home:** `/`
- **Blog listing:** `/blog` (nav label “Reports”)
- **Blog post:** `/<slug>` via `app/(site)/[slug].tsx`
- **Podcast:** `/podcast`, episodes at `/podcast/interviews/<id>`
- **Authors:** `/authors`, `/authors/<id>`
- **Legal:** `/legal/<id>`
- **Membership:** `/login`, `/signup`, `/pricing`, `/account` (hub), `/settings`
- **Studio (signed-in):** `/studio` (hub); deep routes `/tools/twilda/*`, `/tools/aftercare/*`, `/tools/samples/*`, `/tools/palette/*` (`/tools` redirects to `/studio`)
- **Profiles:** `/u/<handle>` (public), `/me` (private hub)
- **Social:** `/following`
- **Library / reference:** `/library`, `/library/reference`
- **Special editions:** `/editions`, `/editions/<id>` (Vice-style manifests in `data/editions.ts`; packs via `cos:ebook` / `cos:pdf -- --edition`)
- **About / contact:** `/about`, `/contact`
- **RSS / AEO:** `/rss.xml`, `/llms.txt`, `/sitemap.xml`

Vision / phases: `docs/00_ARTOMETRICS_MASTER_VISION.md`, `docs/01_BUILD_PHASES_AND_CHECKLIST.md`, `docs/PLATFORM_UX_PLAN.md`. Tools DB: `docs/TOOLS_SETUP.md`. Sanity: `docs/SANITY_SETUP.md`.

## Commands

| Command | Action |
|--------|--------|
| `npm install` | Install dependencies |
| `npm run setup:pipeline` | R + Quarto + pandoc + Python + print libs |
| `npm run setup:clis` | Netlify / Supabase / Stripe CLIs |
| `npm run doctor` | Green/red toolchain inventory |
| `npm run content` | Rebuild `src/generated/*` |
| `npm run dev` | Expo web |
| `npm start` | Expo CLI |
| `npm run build` | Static web export → `dist/` |
| `npm run sync:articles` | Sync Quarto repos → blog markdown + chart assets (legacy path) |
| `npm run materialize:articles` | Create/update all `articles/<slug>/` from blog + public assets |
| `npm run articles:html-to-qmd` | Bulk-convert blog HTML bodies → Quarto `.qmd` (skips Tier A unless `--force`) |
| `npm run link:article-assets` | Symlink `assets/`, copy `styles/report.css` into each article folder |
| `npm run render:articles` | `Rscript articles/R/render_all.R` — render every `_quarto.yml` project |
| `npm run sync:article -- --slug …` | Copy one article home → `public/` |
| `npm run sync:readmitted` | Wrapper: `sync:article --slug readmitted` |
| `npm run calendar:content` | Regenerate `docs/content-os/content-calendar.csv` (Friday release schedule) |
| `npm run render:readmitted` | R export PNG + Plotly JSON for READMITTED |
| `npm run render:readmitted:py` | Python fallback chart export (debug only) |
| `npm run cos:pdf -- --slug …` | Article PDF → `public/exports/` |
| `npm run cos:ebook -- --slug …` | Article EPUB |
| `npm run cos:narrate -- --slug …` | ElevenLabs MP3 (needs `ELEVENLABS_API_KEY`) |

Full stack recipe: `docs/FULL_STACK_RECIPE.md`. Backend hookup: `docs/BACKEND_HOOKUP_SESSION.md`.

## Article pipeline (monorepo gold → app)

**Article monorepo:** Every report has a Quarto home at `articles/<slug>/` (see [`articles/README.md`](articles/README.md)). **READMITTED** is the Tier A gold prototype (`articles/readmitted/`). Render charts with `npm run render:readmitted -- --render` or R scripts; sync assets with `npm run sync:article -- --slug …`; site body stays in `src/content/blog/<slug>.md`. Friday release order: [`docs/content-os/content-calendar.csv`](docs/content-os/content-calendar.csv).

Older reports may still use singular repos under [Artometrics](https://github.com/Artometrics) and `scripts/sync-github-articles.mjs` until migrated. Run `npm run content` after syncing so the Expo app picks up new posts.

| Path | Purpose |
|------|---------|
| `articles/readmitted/` | Gold report home (data, Quarto, charts, QA) |
| `scripts/render-readmitted-charts.R` | R PNG + Plotly JSON export → `articles/` + `public/` |
| `scripts/sync-readmitted.mjs` | Copy local article assets into `public/` |
| `scripts/sync-github-articles.mjs` | Legacy: clone external Quarto repos, rewrite blog body |
| `scripts/r/artometrics_theme.R` | Shared `theme_artometrics()` + chart export helpers |
| `pilot-drafts/readmitted/` | Earlier pilot bundle (superseded by `articles/readmitted/`) |
| `public/data/articles/<slug>/charts/` | Plotly JSON for live charts |

## Content OS (editorial factory)

Keyword briefs, style rules, draft scaffolds, and AEO live under `docs/content-os/`.

| Command | Action |
|--------|--------|
| `npm run cos:brief -- --slug … --desk arts --subdomain film --title "…"` | New keyword brief |
| `npm run cos:scaffold -- --brief docs/content-os/briefs/<slug>.json` | Draft HTML report scaffold |
| `npm run cos:banner-prompt -- --brief …` | Higgsfield banner prompt |
| `npm run cos:publish -- --slug …` | Copy draft → `src/content/blog/` + rebuild JSON + `llms.txt` |
| `npm run cos:aeo` | Regenerate llms.txt, llms-full, sitemap, RSS |
| `npm run cos:zine -- --slug <slug>` | Instagram zine pack (slides.html + caption) |
| `npm run cos:carousel -- --slug <slug>` | Kruger 1:1 IG carousel pack |
| `npm run cos:carousel -- --brand` | Newsstand brand carousel |
| `npm run cos:pdf -- --slug <slug>` | Print PDF pack |
| `npm run cos:ebook -- --slug <slug>` | EPUB pack |
| `npm run cos:narrate -- --slug <slug>` | ElevenLabs narration MP3 |

Style bible: `docs/content-os/STYLE_GUIDE.md`. Overview: `docs/content-os/README.md`.  
Ops plan: `docs/MEDIA_COMPANY_PLAN.md`. Vision: `docs/MEDIA_EMPIRE_VISION.md`. Hand-off checklist: `docs/NEXT_STEPS.md`. Backend session: `docs/BACKEND_HOOKUP_SESSION.md`.

## Cursor Cloud specific instructions

The Expo web app is the development target for Cloud Agents. `npm ci` is enough to install it. Generated JSON in `src/generated/` is already committed; run `npm run content` after editing markdown under `src/content/`.

On boot, the dev server listens at http://127.0.0.1:8081 (`npx expo start --web --port 8081`, with `EXPO_NO_TELEMETRY=1` and `BROWSER=none`). Leave `CI` unset so Metro keeps file watching. Check readiness with `curl -sf http://127.0.0.1:8081/status`.

Public magazine pages render without membership secrets. Copy `.env.example` to `.env` when testing login, checkout, or Supabase-backed tools.

Useful checks against the running server:

- `npm run test:unit`
- `PREVIEW_URL=http://127.0.0.1:8081 npm run test:smoke`
- `npm run build` (static web export to `dist/`)

R, Quarto, pandoc, and the Python media packs are a separate editorial toolchain. Run `npm run setup:pipeline` when a task needs chart rendering or print packs. `npm run doctor` lists what is present.

## Guardrails for AI / contributors

- Prefer **minimal diffs** and `@/` imports from the project root.
- Keep public-facing copy **Artometrics-branded**.
- Do **not** reintroduce Astro; this product is Expo-only.
- Verify `npm run build` after changing routes or the content builder.
- Netlify API redirects (`/api/*`) must stay above the SPA fallback in `netlify.toml`.
- New reports should start from a Content OS brief when possible.
