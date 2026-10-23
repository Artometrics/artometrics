# Artometrics site docs & lab log

## Workflow
Find data → audit → SQL (DuckDB) → charts (Plotly/R) → story (markdown in `src/content/blog/`).

## Where things live
- Pages: `app/(site)/` (new: `lab-log.tsx` → `/lab-log`)
- Narration MP3s: `public/audios/` (wired via `audioSrc` frontmatter)
- Magazine issue PDFs: `public/downloads/magazine/`
- Hosting: Firebase `artometrics-510519` (noindex header), Netlify config mirrors it.

## Indexing
Hidden until launch: robots Disallow, noindex meta, X-Robots-Tag, no sitemap.

## Log
- 2026-10-23 Lab log page, magazine PDFs, this doc
- 2026-10-21 Style Lab house style
- 2026-10-14 Editor's picks redesign, a11y fixes
- 2026-10-12 Franchise Kore narration v4; Anime clean ledger + charts
