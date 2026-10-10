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
