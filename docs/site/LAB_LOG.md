# Artometrics site docs & lab log

## Workflow
Find data → audit → SQL (DuckDB) → charts (Plotly/R) → story (markdown in `src/content/blog/`).

## Where things live
- Pages: `app/(site)/` (new: `lab-log.tsx` → `/lab-log`)
- Narration MP3s: `public/audios/` (wired via `audioSrc` frontmatter)
- Magazine issue PDFs: `public/downloads/magazine/`
- Hosting: Firebase `artometrics-510519` and Netlify. DNS is unchanged.

## Indexing
Public. robots allow, sitemap on, no noindex meta or X-Robots-Tag. Full reports live at `/{slug}` (dark site chrome). The abbreviated page-flip magazine is at `/mag` and `/mag/{slug}`.

## Log
- 2026-10-23 Lab log page, magazine PDFs, this doc
- 2026-10-21 Style Lab house style
- 2026-10-14 Editor's picks redesign, a11y fixes
- 2026-10-12 Franchise Kore narration v4; Anime clean ledger + charts
