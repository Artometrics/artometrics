# Artometrics

Independent data journalism on culture, place, history, persona, and power — built for the creative industries.

**Live site:** [artometrics.com](https://artometrics.com)

## What this is

Artometrics publishes long-form, data-driven reports and a podcast on the creative economy. The product is an **Expo** app (iOS, Android, and web) with a shared React Native codebase. Reports sync from the [Artometrics GitHub org](https://github.com/Artometrics) and render with interactive charts (web) plus PNG fallbacks (native).

Editorial desks:

| Desk | Focus |
|------|--------|
| **Culture** | Music, film, anime, games, and the business of art |
| **Atlas** | Cities, regions, and creative ecosystems |
| **History** | Long-run patterns, institutions, and civilizational data |
| **Persona** | Leaders, archetypes, and figures who shaped systems |
| **Power** | Institutions and how influence accumulates |

## Tech stack

- [Expo](https://expo.dev/) + [Expo Router](https://docs.expo.dev/router/introduction/) (web + native)
- React Native / React Native Web
- Markdown content under `src/content/` → JSON via `npm run content`
- Netlify (static Expo web export + serverless functions for auth/billing)
- Supabase + Stripe for membership

See [AGENTS.md](./AGENTS.md) for routing, content schemas, and contributor guardrails.

## Requirements

- Node.js 20+ (LTS recommended)
- npm

## Commands

| Command | Action |
| :------ | :----- |
| `npm install` | Install dependencies |
| `npm run content` | Build JSON from `src/content/**` |
| `npm run dev` / `npm run web` | Expo web dev server |
| `npm start` | Expo dev tools (pick web / iOS / Android) |
| `npm run ios` | iOS simulator |
| `npm run android` | Android emulator |
| `npm run build` | Content build + `expo export -p web` → `./dist/` |
| `npm run sync:articles` | Sync Quarto repos → blog markdown + chart assets |
| `npm run scaffold:repo -- --batch-from-site` | Scaffold local GitHub repo layouts for Python-only articles |
| `npm run upgrade:repos` | Audit/upgrade the 10 existing Artometrics GitHub repos |
| `npm run publish:repos` | Push local repo upgrades to `Artometrics/*` on `main` |
| `npm run migration:manifest` | Write `docs/migration-manifest.json` |
| `npm run render:readmitted:py` | Export readmitted PNG + Plotly JSON |
| `npm run cos:brief` | New keyword brief |
| `npm run cos:scaffold` | Scaffold draft HTML report from brief |
| `npm run cos:banner-prompt` | Print Higgsfield banner prompt |
| `npm run cos:publish` | Publish draft → `src/content/blog/` |
| `npm run cos:llms` | Regenerate `public/llms.txt` from published posts |

## Content workflows

- **Content OS:** keyword brief → scaffold → banner → publish (`docs/content-os/`)
- **Blog reports:** `src/content/blog/` — frontmatter template in `src/content/blog/anime.md`
- **Sync GitHub articles:** `npm run sync:articles`
- **Podcast episodes:** `src/content/podcast/` — template in `src/content/podcast/1.md`
- **Authors:** `src/content/authors/`

## Links

- **GitHub:** https://github.com/Artometrics
- **Ethics:** https://artometrics.com/legal/ethics-statement

## Search indexing

SEO/indexing intentionally disabled; re-enable robots, sitemap, meta at promoted launch.
