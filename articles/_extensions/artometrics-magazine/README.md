# Artometrics magazine

A Quarto extension that turns one article `.qmd` into two editions of the same issue:

- a print PDF (Typst)
- a paginated HTML edition (paged.js)

The article text, figures, and credits stay in the `.qmd`. The extension only adds the cover, contents, running header, and back cover.

## Opt in

From the article folder, link the extension once (the npm script does this):

```bash
mkdir -p articles/<slug>/_extensions
ln -s ../../_extensions/artometrics-magazine articles/<slug>/_extensions/artometrics-magazine
```

In that article's `_quarto.yml`:

```yaml
format:
  html: default
  artometrics-magazine-typst:
    font-paths:
      - _extensions/artometrics-magazine/fonts
  artometrics-magazine-html: default
```

Put the issue fields in the `.qmd` front matter. Body copy is ordinary Markdown. These divs are optional and map to magazine parts:

| Class | What it is |
| --- | --- |
| `exec-summary` | Key-findings page. Nested `card` / `stat` divs. |
| `lede` | Opening paragraph, full measure. |
| `pullquote` | A number (`stat`) plus a sentence already in the article. |
| `sidebox` | Mechanism or context. Nested `kicker`. |
| `chart-page` | Full page for one existing figure, with its caption and credit. |
| `spread` | Two-column `copy` and `side` (studio cards, logos, portraits). |
| `title-cards` | A grid of `title-card` divs. |
| `single` | Methods and other pages that should not sit in two columns. |
| `checksum` | Dataset digest, set in DM Mono on a black bar. |
| `versions` | Package versions that produced the figures. |
| `editors-note` | Closing note. |
| `credit` | The image credit, same wording as the site. |

Chart images should be the article's existing files. In the Markdown, set the width to `5.85in` or narrower. The Anime charts are 1,792 pixels wide, so 5.85 inches prints them at about 306 dpi.

```yaml
magazine:
  issue: "02"
  kicker: "Arts · Film"
  running: "SHORT NAME"
  hero-stat: "12 : 1"
  hero-label: "What the hero number measures"
  hero-detail: "The two figures behind it"
  url: "https://artometrics.com/<slug>/"
```

`running` is the short name in the header. `description` is the dek. `title` is the cover headline.

## Render

From the repo root:

```bash
npm run magazine -- <slug>
```

Outputs:

- `articles/<slug>/magazine/<slug>-issue-01.pdf`
- `articles/<slug>/magazine/<slug>-issue-01.html` (open it next to `paged.polyfill.js`)

If `src/content/blog/<slug>.md` exists, the script stops when a number in the published report is missing from the `.qmd`.

Issue 1 is Anime. Its `.qmd` was transcribed from `src/content/blog/anime.md` by `scripts/build_issue_qmd.py`. Re-run that only when you intend to rebuild the Quarto source from the blog file. The magazine render does not rewrite the article.

## Type

- **DM Sans** for text. Headlines are bold. Emphasis is italic or underline.
- **DM Mono** for numbers, labels, and data.
- **Chomsky** for the Artometrics wordmark only. The file is `fonts/Chomsky.otf`, copied from `public/fonts/Chomsky.otf`.

DM Sans in the repo is a variable font. Typst embeds the static Regular, Bold, Italic, and Bold Italic cuts in `fonts/`, instantiated from `public/fonts/DMSans.ttf` and `DMSans-Italic.ttf` at optical size 14. DM Mono is copied from `public/fonts/`.

Chomsky ships with this repo and is already the site wordmark. A separate license file for Chomsky is not in the repo. DM Sans and DM Mono are the SIL Open Font License faces already used on the site.

## Color

Red `#E60000`. Blue `#4D8DFF` on black, `#0047FF` on white. Black and white do the rest. The hero number is an anaglyph: red and blue offsets under a white numeral.
