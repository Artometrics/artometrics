# ANIME: Source Sets the Audience Floor

**Desk:** arts · **Live:** https://artometrics.com/anime/

Executive brief. The page, the tables, and the five charts are written by `scripts/build_brief.R`.

## Reproduce

From the repo root, one command:

```bash
npm run brief:anime
```

That runs `Rscript articles/anime/scripts/build_brief.R` and then syncs the charts and tables into `public/`. If `tidyverse`, `jsonlite`, `showtext`, or `sysfonts` are missing, the script installs them into `R_LIBS_USER` from CRAN and continues. A fresh machine does not need a separate install step.

The script loads:

| Package | Why |
| --- | --- |
| `tidyverse` | dplyr, ggplot2, readr, tidyr, stringr, tibble, and the rest of the tidyverse. `scales` comes in with ggplot2. |
| `jsonlite` | Plotly JSON |
| `showtext` | Anton titles and DM Sans labels on the PNGs. Pulls in `showtextdb`. |
| `sysfonts` | Registers `assets/fonts/Anton-Regular.ttf` and `assets/fonts/DMSans.ttf` |

`grid`, `tools`, and `utils` are base R. `oxipng` is optional; without it the script still writes the PNGs and warns.

To install those packages yourself:

```bash
Rscript -e 'install.packages(c("tidyverse", "jsonlite", "showtext", "sysfonts"), repos = "https://cloud.r-project.org")'
```

Pinned versions for a lockfile restore are in `renv.lock`:

```bash
Rscript -e 'if (!requireNamespace("renv", quietly = TRUE)) install.packages("renv", repos = "https://cloud.r-project.org"); renv::restore(lockfile = "articles/anime/renv.lock", prompt = FALSE)'
```

The raw file `data/raw/tidy_anime.csv` is downloaded on the first run when it is missing. Expected SHA-256: `5ea3a14492b5c559c728af0c7ec57b81c919d0efa4d381e54b0f7cde9934a1c2`.


## Magazine edition

Issue 01 of the Artometrics magazine edition renders from this folder's `anime.qmd` (the same words and figures as the published report). From the repo root:

```bash
npm run magazine -- anime
```

PDF and paginated HTML land in `magazine/`. The format is the shared Quarto extension `articles/_extensions/artometrics-magazine/`. See that folder's README to opt another article in.

The page rounds half up. Displayed figures use half-up on the exact value (`sign(x) * floor(abs(x) * 10^d + 0.5 + 1e-9) / 10^d`), not R's `round()`, which uses banker's rounding. A median of 4737.5 is published as 4,738, and an IQR of 0.985 is published as 0.99.
