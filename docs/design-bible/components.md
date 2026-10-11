# Component catalog — mix and match

Map Lexington **patterns** (not copied markup) onto Artometrics **surfaces**. Implementation homes are noted for when you wire this up—this bible does not change production code.

## Home page

| Piece | Borrow from | Artometrics target | Notes |
|-------|-------------|-------------------|-------|
| Masthead band | Hemingway nav density | `SiteHeader.tsx` | Centered Chomsky logo; desk links as uppercase mono labels |
| Lead story | Northbound `BigBlogCard` | `HomeMagazine.tsx` `HomeMainStory` | 2/3 image + 1/3 title stack on desktop; drop bordered thumbnail box |
| Secondary stack | Hemingway `BlogCard2` | `HomeSecondaryStory` | Hairline between stories, not `mt-8` card gap only |
| Popular grid | Hemingway `BlogPreview` | New `HomePopularGrid` | `border-t border-black` + 4-col; flag `isPopular` in blog frontmatter |
| Podcast strip | Hemingway `PodcastPreview` | `app/(site)/podcast/index.tsx` | Match home rhythm |
| Newsletter | Hemingway `Subscribe` | `app/(site)/newsletter.tsx` | Full-width rule above |
| Photo ribbon (optional) | Semplice `Hero` | Marketing `/about` only | Not on daily home—too little text hierarchy |

## Report (article) template

| Piece | Borrow from | Artometrics target | Notes |
|-------|-------------|-------------------|-------|
| Sticky display title | Hemingway `BlogLayout` | `app/(site)/[slug].tsx` | Title scrolls; hero image below fold |
| Split header (current) | — | `[slug].tsx` today | Side-by-side hero + title reads **blog CMS**, not magazine |
| Prose measure | Hemingway `Wrapper variant="prose"` | `ArticleBody.web.tsx` + `artometrics-article.css` | 42rem column; sans heads, serif optional for pull quotes only |
| Pull quote | Hemingway blockquote styles | Quarto `.blockquote` | 4px black left rule, italic |
| Figure + caption | Semplice project credits | Quarto figure + `artometrics-article.css` | `FIG. 12` mono + sentence caption |
| Key stats band | Ella Mae comparison highlight row | `ReportStatGrid.tsx` | Blue/red accent cells, mono numbers |
| Related reads | Hemingway related grid | `ReportRelatedReads.tsx` | 3-up with top rule |
| TOC sidebar | Artometrics custom | `artometrics-article.css` | Keep; restyle to mono labels |
| Chart exhibit | WSJ / Pudding pattern (see magazine-upgrade) | `ArticleBody.web.tsx` Plotly | Figure wrapper + source line |

## Blog / reports index

| Piece | Borrow from | Target |
|-------|-------------|--------|
| Journal title | Northbound blog index | `app/(site)/blog/index.tsx` |
| Lead + grid | Northbound + Outkast `JournalHero` | First post feature, rest 3-col |
| Card | Hemingway `BlogCard2` | `BlogCard.tsx` variants |

## Navigation & chrome

| Piece | Borrow from | Target |
|-------|-------------|--------|
| Overlay menu | Outkast `overlayNavigation` | `SiteNavOverlay.tsx` for mobile |
| Footer columns | Hemingway footer | `SiteFooter.tsx` |
| Breadcrumb | Artometrics | `ReportBreadcrumb.tsx` — switch to mono, slashes in red |

## Data visuals

| Piece | Borrow from | Target |
|-------|-------------|--------|
| Table zebra | Ella Mae comparison | Quarto tables + CSS |
| Axis labels | tokens.md | Plotly layout `font.family` DM Mono |
| Chart title | Economist / FT | Bold sans title outside plot area |
| Source line | FT | `DM Mono 11px` under every figure |

## Podcast

| Piece | Borrow from | Target |
|-------|-------------|--------|
| Episode card | Hemingway podcast components | `podcast/index.tsx` |
| Player | Hemingway audio CSS | `ArticleNarrationPlayer.tsx` |

## Studio / tools (secondary brand moment)

| Piece | Borrow from | Target |
|-------|-------------|--------|
| Case grid | Outkast work index | `app/(site)/studio/index.tsx` |
| Service list | Semplice services | Tool landing pages |

## Recommended default recipe (Artometrics magazine)

```
Home:     Hemingway section rules + Northbound lead asymmetry + Artometrics tokens
Article:  Hemingway sticky title + Semplice figure captions + tokens anaglyph
Index:    Outkast JournalHero + Northbound grid
Charts:   tokens chart exhibit + Pudding-style scrolly (later phase)
Chrome:   Minimal Hemingway header + Chomsky wordmark only
```

## Anti-patterns (do not mix)

- Semplice ribbon + dense data table on same view (competing focal points)
- Outkast rounded-xl cards on Kruger-zero-radius report body
- Ella Mae blue product tiles without red editorial counterweight (brand feels corporate)
- Gold/warm `Colors.ts` magazine theme **with** Kruger black/white comps in same page without a deliberate “edition” context
