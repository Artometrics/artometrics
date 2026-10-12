# Lexington Themes — study notes

Licensed Astro + Tailwind v4 themes, shallow-cloned to `~/worker/lexington/` (never commit vendor source to Artometrics). Org inventory (`gh repo list Lexington-Themes`): **ellamae**, **hemingway**, **northbound**, **outkast**, **semplice**, plus public tooling (astro-skills, tutorials, SEO package).

Screenshots: production Artometrics in `screenshots/artometrics-*.png`; **Hemingway** built locally (`screenshots/lex-hemingway-*-local.png`). Hosted `*.lexingtonthemes.com` demos did not resolve from the cloud agent network.

---

## Hemingway — editorial / podcast magazine (primary reference)

**Overall feel:** Quiet luxury editorial. Warm neutral base scale (oklch grays + cream accent ramp), **Inter** UI + **STIX Two Text** display serif. Podcast + blog + authors + pricing—closest to Artometrics’ actual product shape.

**Best use:** Magazine home, article template, author pages, audio player chrome, newsletter CTAs.

### Layout & pages

| Page | Structure |
|------|-----------|
| **Home** | Full-viewport hero (`displayLG` serif manifesto) → 4-col popular posts grid with top rule → podcast strip → subscribe CTA |
| **Blog index** | Centered serif `displayMD` intro → post list |
| **Article** | Sticky centered `display3XL` title over scroll → hero image (`max-w-xl`) → narrow prose wrapper → author row → share → prev/next → related grid |
| **About / authors** | Standard `max-w-7xl` wrapper, large serif headlines |

**Grid:** `Wrapper` variants — `standard` (`max-w-7xl`, `px-8`), `narrow` (`max-w-xl`), `prose` (typography plugin preset with serif body, sans headings).

### Typography

- Sans: Inter with OpenType features (tabular nums, stylistic sets) in `global.css`
- Serif: STIX Two Text for display and article voice
- Scale via `Text.astro` variants (`display3XL` … `textXS`) — aggressive responsive jumps at `lg:`

### Color

- `accent-50`–`950` warm yellow-cream ramp; `base-50`–`950` neutral grays (oklch)
- High contrast black rules (`border-t border-black` on blog preview)

### Spacing

- Section padding: `pt-32`, `pb-12`, `py-24`
- Blog cards: `gap-4` grid, `mt-4 pt-4 border-t`

### Signature components

- **Hero:** oversized serif manifesto, minimal imagery on home
- **Article hero:** sticky headline + centered image (magazine cover feel)
- **BlogCard2:** image + meta for grids
- **Audio player:** custom range styling in `global.css`
- **Subscribe CTA:** repeated footer pattern
- **Prose:** `@tailwindcss/typography` with first-letter enlarge, blockquote left rule

### Motion

- Lenis smooth scroll in `BaseLayout`
- Hover opacity on author links

### Patterns worth porting to Expo

- `Text` variant map → unify with Tailwind classes in `components/`
- `Wrapper` three-tier width system → already mirrored as `Wrapper` `standard | narrow | wide | bleed`
- Article **title scrolls over image** — strong magazine trope for Artometrics reports
- Black **hairline section breaks** between home modules

---

## Northbound — retreat / experience editorial

**Overall feel:** Earthy hospitality journal. **Noto Serif Display** + **Inter**, green accent ramp (oklch), warm gray bases. Photography-forward, calm pacing.

**Best use:** Gallery grids, event schedules, “destination” story layouts—not primary for data reports.

### Layout & pages

| Page | Structure |
|------|-----------|
| **Home** | Hero → intro copy → story section → schedule → CTAs → gallery preview |
| **Blog index** | `display4XL` “The Journal” → **one BigBlogCard** (3-col image + text) → 3-col card grid |
| **Article** | (Same Lexington blog patterns as Hemingway family) |

**Grid:** `BigBlogCard` = `lg:grid-cols-3` with `aspect-square` / `lg:aspect-12/8` image.

### Typography

- Display: Noto Serif Display, light weight, `leading-snug`
- Body: Inter

### Color

- Accent: muted green (`oklch` hue ~135)
- Base: warm gray-beige scale

### Signature components

- **BigBlogCard** — lead story layout (excellent Artometrics “cover investigation” candidate)
- **Gallery** modules with saturated-50 images
- **Schedule / events** timeline rows

### Motion

- Standard Lexington `data-reveal` patterns (see Semplice/Hemingway family docs)

### Reuse for Artometrics

- Lead story **asymmetric grid** on home
- Desaturated hero photography (`saturate-50`) for photo essays

---

## Semplice — photography / fashion portfolio

**Overall feel:** White gallery wall. **Switzer** + **Fragment Mono**, zero accent color—photos carry chroma. Highest “magazine” purity, lowest data-density affordances.

**Best use:** Figure ribbon, caption typography, archive index, credits blocks.

### Layout & pages

| Page | Structure |
|------|-----------|
| **Home** | 3D **drifting photo ribbon** (`Hero.astro`) |
| **Work** | Sequence of full-width frames per project |
| **Journal** | Minimal post list + tag pages |
| **Archive** | Monospace index of every frame |
| **Article** | `PostHeader` + `max-w-2xl` prose |

### Typography

- Sans: Switzer (Fontshare)
- Mono: Fragment Mono for captions, labels, index

### Color

- Strict monochrome tokens in `colors.css` (background, foreground, muted, border)

### Signature components

- **Ribbon hero** — kinetic masthead without copy
- **Credits** lines under projects (client, stylist, date)
- **Availability** strip in nav
- **Prose** centered `max-w-2xl`

### Motion

- Lenis + ribbon drift + `data-reveal` / `data-reveal-stagger`
- Full reduced-motion fallbacks

### Reuse for Artometrics

- **Caption + credit** pattern for report figures
- **Archive index** pattern for `/blog` or datasets catalog
- Mono **figure numbers** (`FIG. 01`)

---

## Outkast — agency / studio

**Overall feel:** Swiss agency minimalism. **Geist** sans only, grayscale oklch tokens, rounded-xl imagery, generous whitespace.

**Best use:** Studio marketing, case study grids, services—not long-form data prose.

### Layout & pages

| Page | Structure |
|------|-----------|
| **Home** | Statement hero + work grid |
| **Blog** | `JournalHero` with `display` headline + 7/5 split feature post |
| **Work** | Case study cards |

### Typography

- Single family: Geist, `tracking-tighter` on big headlines (`text-5xl` → `lg:text-7xl`)

### Color

- Black/white/gray only; `accent` is mid-gray for subtle CTAs

### Signature components

- **JournalHero** — blog front with oversized title “Notes from the press office”
- **PostGrid** — rounded image cards with hover scale
- **Overlay navigation** on blog layout

### Reuse for Artometrics

- **Studio** landing and tool marketing pages
- Blog index **hero feature** row (image 7 / text 5)

---

## Ella Mae — manufacturer / product

**Overall feel:** Industrial premium. **Familjen Grotesk**, cool gray surfaces, **saturated blue** accent tiles, product cut-outs on `bg-surface` panels.

**Best use:** Hardware/configurator flows, spec tables, comparison matrices—not editorial magazine.

### Layout & pages

| Page | Structure |
|------|-----------|
| **Home** | Model tiles, configurator CTA, news/events |
| **Models** | Comparison table, per-model feature pages |
| **News** | Corporate press layout |

### Typography

- Single grotesk family, 400–700

### Color

- `background`, `surface`, `accent` (blue), `signal` (orange) semantic tokens

### Signature components

- **Comparison tables** with zebra rows
- **Configurator** panel UI
- **Product cut-out** on surface (`mix-blend-multiply`)

### Reuse for Artometrics

- **Spec / comparison tables** in reports
- **Key stats** band with blue accent tile (map to anaglyph blue)

---

## When to use which (decision table)

| Artometrics surface | Start from | Why |
|---------------------|------------|-----|
| Home / section fronts | **Hemingway** + Northbound lead card | Editorial hierarchy + asymmetric lead |
| Long-form report (Expo) | **Hemingway** article sticky title | Magazine cover scroll |
| Quarto HTML body | **Hemingway** prose + **Semplice** captions | Readable measure + figure credits |
| Podcast | **Hemingway** | Native audio + episode grids |
| Studio / tools marketing | **Outkast** | Agency clarity |
| Datasets / archive index | **Semplice** | Mono index aesthetic |
| Spec-heavy sports/business reports | **Ella Mae** tables | Comparison density |

**Recommended base theme for artometrics.com:** **Hemingway** — only theme with blog + podcast + authors + subscription flows aligned to the live product; article layout is the clearest upgrade path for reports.
