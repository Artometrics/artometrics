# Artometrics design system (v1.0)

Barbara Kruger–influenced **anaglyph magazine** on a newsprint base for [artometrics.com](https://artometrics.com).

Canonical product reference also lives in Notion: **Artometrics Design System**. Implementation bible: `docs/design-bible/tokens.md`.

These HTML files are design references — recreate in the Expo codebase (`components/`, `app/(site)/`, Content OS packs). Do not freestyle a second brand.

## Tokens

| Token | Hex | Use |
|-------|-----|-----|
| `--art-paper` / `--color-white` | `#FFFFFF` | Primary reading surface |
| `--art-paper-muted` | `#F2F2F2` | Stat bands, inset panels |
| `--art-ink` / `--color-black` | `#000000` | Text, 2px rules |
| `--art-ink-muted` | `#525252` | Secondary prose, captions |
| `--art-rule` | `#E5E5E5` | Hairlines between stories |
| `--art-red` / `--color-accent` | `#E60000` | Links, active nav, chart callouts |
| `--art-blue` / `--color-secondary` | `#0047FF` | Data links, secondary series |

**Type:** Display, headlines, and body — **DM Sans** (bold/italic/underline for emphasis). Wordmark only — **Chomsky**. Data, labels, datelines, axes — **DM Mono**.

**Rules:** 2px solid black section dividers; short red accent rules. No border-radius on editorial surfaces, no soft multi-layer shadows, no gradients, no cream/gold drift in the magazine default.

Swiss edition (optional brand toggle) may still load Piazzolla + Archivo via `constants/Colors.ts` `SwissFonts`.

## Reference files

| File | Purpose |
|------|---------|
| `Artometrics_Design_System.dc_ffd4.html` | Tokens, type, components, do/don’t |
| `Artometrics_Website_Home.dc_80ca.html` | Newsstand + homepage bands |
| `Artometrics_Edition_Cover.dc_2241.html` | Edition cover block |
| `Artometrics_Edition_Page.dc_7e08.html` | Dark edition article layout |
| `Artometrics_IG_Zine_Pack.dc_50e8.html` | 6-slide 4:5 zine |
| `Artometrics_IG_Carousel_-_Kruger_Style.dc_622f.html` | 1:1 Kruger carousel |
| `Artometrics_IG_Carousel_-_Live_Content.dc_fc6a.html` | Live-headline carousel |
| `Artometrics_OG_Card.dc_cb3c.html` | 1200×630 share card |
| `Artometrics_Media___Books_-_VHS_Shelf.dc_97a6.html` | VHS media shelf |

## Mapped into product

- Tokens: `constants/Colors.ts`, `global.css`, `public/css/artometrics-article.css`
- Home: `components/HomeMagazine.tsx` — asymmetric lead, 2px rules, “This week” row
- Reports: `app/(site)/[slug].tsx` — display title → full-bleed hero → byline band
- Chart exhibits: `lib/artExhibit.web.ts`, `components/ArticleBody.web.tsx`
- IG zine packer: `npm run cos:zine` → `scripts/content-os/pack-ig-zine.mjs`
- OG default: `public/images/brand/og-default.png`
