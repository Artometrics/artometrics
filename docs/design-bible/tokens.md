# Artometrics tokens (house set)

Target: **anaglyph glasses** energy on a **newsprint** base—red and blue as paired signals, black and white as structure.

Canonical implementation: `constants/Colors.ts`, `global.css`, `lib/uniwind-theme.ts`, `public/css/artometrics-article.css`.

## Anaglyph assignment (magazine UI — swapped pair)

| Role | Hex | Tailwind / semantic | Usage |
|------|-----|---------------------|--------|
| **Wordmark** | `#E60000` | `text-secondary`, Chomsky logo | Masthead only — primary red anchor |
| **UI accent** | `#0047FF` | `text-accent`, `ThemeColors.accent` | Nav links, kickers, category labels, CTAs (“Read investigation”), “This week”, progress bar, exhibit labels |
| **UI counter** | `#E60000` | `text-secondary`, `ThemeColors.secondary` | Desk/dateline meta, issue-row dates, wordmark |
| **Chart primary** | `#E60000` | `--art-chart-red` | Plotly/static series — **do not** remap with UI swap |
| **Chart secondary** | `#0047FF` | `--art-chart-blue` | Second Plotly/static series (house blue) |

Use red and blue together sparingly; the **logo stays the main red**; chrome accents lean blue.

### Accessibility (house blue `#0047FF`)

- On **white** (`#FFFFFF`): contrast ≈ **6.3:1** — passes WCAG AA for small text.
- On **black** (`#000000`): contrast ≈ **3.4:1** — fails AA for normal-sized text (passes large/bold only). Dark-mode accent links/labels keep `#0047FF` by brand choice.

### Core surfaces

| Token | Hex | Role |
|-------|-----|------|
| `--art-paper` | `#FFFFFF` | Primary reading surface |
| `--art-paper-muted` | `#F2F2F2` | Stat bands, inset panels |
| `--art-ink` | `#000000` | Primary text, 2px rules |
| `--art-ink-muted` | `#525252` | Secondary prose |
| `--art-rule` | `#E5E5E5` | Hairlines |

### Semantic (`ThemeColors` magazine light)

| Semantic | Value | Notes |
|----------|-------|-------|
| `accent` | `#0047FF` | UI accent (was red pre-swap) |
| `accentSoft` | `#E6EEFF` | Blue wash |
| `secondary` | `#E60000` | Wordmark + red meta (was blue pre-swap) |
| `bg` / `text` | paper / ink | |

Literal chart tokens `--art-red` / `--art-blue` remain the data palette in CSS and `lib/charts/plotlyTheme.ts`.

## Typography

| Role | Family | Usage |
|------|--------|--------|
| Wordmark | Chomsky | Logo only |
| Display & body | DM Sans | Headlines, prose, UI |
| Data & meta | DM Mono | Dates, labels, axes, figure nos. |

## Typography scale

See prior tables in git history for `display-xl`, `body` 17px, measure 42–68ch.

## Chart / exhibit

| Token | Value |
|-------|--------|
| Primary series | `--art-chart-red` / `#E60000` |
| Secondary series | `--art-chart-blue` / `#0047FF` |
| Exhibit chrome | `--art-highlight` (UI blue) |
| Figure caption meta | `--art-secondary` (UI red) optional |
