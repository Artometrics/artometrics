# Artometrics tokens (proposed house set)

Target: **anaglyph glasses** energy on a **newsprint** base—red and blue as paired signals, black and white as structure, no cream/gold drift in the magazine default.

Canonical implementation targets: `constants/Colors.ts`, `global.css`, `lib/uniwind-theme.ts`, `public/css/artometrics-article.css`.

## Color

### Core

| Token | Hex | Role |
|-------|-----|------|
| `--art-paper` | `#FFFFFF` | Primary reading surface (web); print may use `#F7F7F5` |
| `--art-paper-muted` | `#F2F2F2` | Stat bands, code blocks, inset panels |
| `--art-ink` | `#000000` | Primary text, 2px rules |
| `--art-ink-muted` | `#525252` | Secondary prose, captions |
| `--art-ink-subtle` | `#767676` | Tertiary / placeholder |
| `--art-rule` | `#E5E5E5` | Hairlines between stories |
| `--art-rule-strong` | `#000000` | Section breaks, masthead footer |

### Anaglyph pair (UI + data emphasis)

| Token | Hex | Role |
|-------|-----|------|
| `--art-red` | `#E60000` | Primary accent: links, active nav, chart callouts, progress bar |
| `--art-red-soft` | `#FFE8E8` | Tinted bands, hover washes |
| `--art-blue` | `#3367E7` | Secondary accent: data links, chart secondary series, “see also” |
| `--art-blue-soft` | `#E8EFFF` | Inset panels, pull-quote wash (optional) |

Use red and blue **together** sparingly (e.g. red headline slug, blue deck; red axis, blue comparison)—never as a full-page gradient.

### Semantic (map into `ThemeColors`)

| Semantic | Light | Notes |
|----------|-------|-------|
| `bg` | `--art-paper` | |
| `bgElevated` | `--art-paper-muted` | |
| `text` | `--art-ink` | |
| `textMuted` | `--art-ink-muted` | |
| `border` | `--art-rule` | |
| `accent` | `--art-red` | Replace current gold-forward `magazineAccent` for magazine brand |
| `secondary` | `--art-blue` | Replace gold `secondary` for links / data |
| `rule` | `--art-rule-strong` | 2px where Kruger rules apply |

**Migration note:** Today `constants/Colors.ts` still carries warm paper/gold (“Bellum magazine”). The bible treats that as **legacy Swiss/magazine hybrid**; new magazine work should converge on the table above to match `docs/design-system/README.md`.

## Typography

| Role | Family | Weights | Usage |
|------|--------|---------|--------|
| **Wordmark** | Chomsky | n/a | Logo / “Artometrics” masthead only |
| **Display & headlines** | DM Sans | 600–700 | H1–H3, section labels, card titles |
| **Body** | DM Sans | 400–500 | Prose, decks, UI chrome |
| **Data & meta** | DM Mono | 400–500 | Dates, read time, figure nos., axis labels, table headers, nav tracking |

### Scale (web)

| Step | Size | Line height | Tracking |
|------|------|-------------|----------|
| `display-xl` | clamp(2.5rem, 5vw, 4rem) | 1.05 | -0.02em |
| `display-lg` | clamp(2rem, 4vw, 3rem) | 1.08 | -0.02em |
| `title` | 1.5–1.75rem | 1.15 | -0.01em |
| `deck` | 1.125–1.25rem | 1.45 | 0 |
| `body` | 17px (1.0625rem) | 1.55 | 0 |
| `meta` | 11–12px | 1.3 | 0.12em (uppercase labels) |
| `mono-sm` | 12–13px | 1.35 | 0.04em |

**Measure:** prose `max-width: 42rem` (narrow); feature columns `65ch`; full-bleed figures break out to `min(75rem, 100vw - 2rem)`.

## Spacing

Base unit **4px**. Prefer named steps:

| Token | Value | Typical use |
|-------|-------|-------------|
| `space-1` | 4px | Icon gaps |
| `space-2` | 8px | Inline stacks |
| `space-3` | 12px | Card padding |
| `space-4` | 16px | Paragraph spacing |
| `space-6` | 24px | Subhead margins |
| `space-8` | 32px | Section padding (mobile) |
| `space-12` | 48px | Section padding (desktop) |
| `space-16` | 64px | Hero breathing room |

**Vertical rhythm:** major section = `space-12` top + `border-t` 2px black; minor = `space-8` + 1px `--art-rule`.

## Radii, shadow, motion

| Property | Magazine default |
|----------|------------------|
| Border radius | `0` (Kruger); `4px` max on code chips only |
| Shadow | None on editorial; 1px border instead |
| Motion | 150–250ms opacity/transform; respect `prefers-reduced-motion` |
| Scroll | Optional Lenis on marketing pages only—not in long report reading mode |

## Chart / exhibit tokens

Align Plotly and static chart PNGs:

| Token | Value |
|-------|-------|
| Chart background | transparent on paper |
| Grid | `#E5E5E5` 1px |
| Primary series | `--art-red` |
| Secondary series | `--art-blue` |
| Neutral series | `#000000` / `#525252` |
| Annotation font | DM Mono 11px |
| Figure caption | DM Mono 12px uppercase label + DM Sans sentence case description |

## CSS custom properties (drop-in sketch)

```css
:root {
  --art-paper: #ffffff;
  --art-paper-muted: #f2f2f2;
  --art-ink: #000000;
  --art-ink-muted: #525252;
  --art-rule: #e5e5e5;
  --art-red: #e60000;
  --art-blue: #3367e7;
  --font-wordmark: "Chomsky", Georgia, serif;
  --font-sans: "DM Sans", system-ui, sans-serif;
  --font-mono: "DM Mono", ui-monospace, monospace;
}
```

Wire these through `lib/uniwind-theme.ts` so React Native Web and Quarto HTML exports stay aligned.
