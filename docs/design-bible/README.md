# Artometrics design bible

A working reference for making [artometrics.com](https://artometrics.com) read as a **data magazine**—not a blog theme, not a dashboard, not a generic SaaS shell. This folder complements `docs/design-system/` (Kruger/Swiss HTML comps) and the shipped tokens in `constants/Colors.ts`.

## What we are optimizing for

| Priority | Outcome |
|----------|---------|
| **Editorial authority** | Every page feels edited: hierarchy, measure, captions, issue rhythm. |
| **Data credibility** | Charts and tables look like exhibits in a report, with source lines and figure numbers. |
| **Brand recall** | Anaglyph red/blue signal on black and white; Chomsky masthead only; DM Sans + DM Mono everywhere else. |
| **Reuse, not rewrite** | Lexington Themes (licensed, local clones under `~/worker/lexington/`) supply **patterns**; Artometrics ships in Expo + Quarto. |

## Principles

1. **One spine, many surfaces** — Home, report, podcast, and Studio share one token set (`tokens.md`) and component vocabulary (`components.md`). No one-off hex values in feature code.
2. **Magazine pacing** — Alternate **dense** (text + sidebar) and **breath** (full-bleed figure, pull quote, stat band). Avoid uniform card grids that flatten priority.
3. **Typography does the work** — Headlines in DM Sans (semibold, tight tracking); body in DM Sans at 17–18px with ~1.55 line-height; all numbers, dates, axes, and labels in DM Mono.
4. **Figures are first-class** — Hero, chart, and photo each get a **figure label** (mono, small caps), optional **credit**, and a **rule** tying them to the paragraph they support.
5. **Navigation is editorial** — Section fronts (Arts, Sports, Science…) behave like magazine desks, not filter chips. The masthead stays minimal; wayfinding lives in the content band.
6. **Motion with restraint** — Scroll-linked reveals and Lenis-style smooth scroll are optional garnish; reduced-motion users get the same hierarchy without animation.
7. **Licensed themes stay outside the repo** — Study Lexington sources locally; document patterns here. Never commit theme vendor trees to Artometrics.

## Files in this bible

| File | Purpose |
|------|---------|
| [themes.md](./themes.md) | Per-theme notes (Ella Mae, Hemingway, Northbound, Outkast, Semplice) and when to borrow each |
| [tokens.md](./tokens.md) | Proposed Artometrics token set (anaglyph red/blue, B&W, type roles) |
| [components.md](./components.md) | Mix-and-match catalog: which theme patterns map to which Artometrics surfaces |
| [magazine-upgrade.md](./magazine-upgrade.md) | Prioritized site upgrade plan with before/after references |
| [screenshots/](./screenshots/) | Live site captures + local Hemingway demo (reference only) |
| [mockups/](./mockups/) | Static HTML “after” comps (not wired to the app) |

## How to use this with the codebase

- **Expo UI:** `components/`, `app/(site)/`, `global.css`, `constants/Colors.ts`
- **Long-form reports:** `public/css/artometrics-article.css`, Quarto homes under `articles/<slug>/`
- **Content OS / social packs:** `docs/content-os/STYLE_GUIDE.md`, `npm run cos:*`

When implementing, pick a **base theme** (see `themes.md`—default recommendation: **Hemingway**) and apply **Artometrics tokens** on top rather than importing Astro layouts wholesale.

## Screenshots

Captured during bible authoring (Oct 2026):

- `screenshots/artometrics-*.png` — production site
- `screenshots/lex-hemingway-*-local.png` — Hemingway theme built locally (`npm run build` + preview); Lexington cloud demos were not reachable from the agent environment
