# Artometrics Master Manual: Data Pipeline and Quantitative Methodology

Document ID: ART-DATA-METH-002  
Version: 2.0  
Classification: Internal Editorial & Analytical Standard  
Author: Artometrics Quantitative Desk & Data Science Guild  

---

## 1. Quantitative Mission and Analytical Philosophy

Artometrics bridges investigative culture journalism and rigorous data science. We reject hand-waving commentary, ungrounded rankings, and unverified PR narratives. Every claim, chart, and conclusion published in an Artometrics report must trace directly to a reproducible public or proprietary dataset, an audited mathematical methodology, and an open code execution pipeline.

---

## 2. Monorepo Quarto Architecture

Every report published in Artometrics originates in an isolated, self-contained Quarto workspace under `articles/<slug>/`:

```
articles/<slug>/
├── _quarto.yml              # Quarto project manifest and render configuration
├── index.qmd                # Scientific paper manuscript containing R/Python code blocks
├── data/                    # Raw extracts and cleaned analytical datasets
│   ├── raw/                 # Immutable upstream source snapshots
│   └── processed/           # Filtered, normalized, and feature-engineered Parquet/CSVs
├── charts/                  # Rendered visualization artifacts
│   ├── chart_01.png         # High-resolution static PNG fallback
│   ├── chart_01.json        # Plotly interactive payload for web hydration
│   └── chart_01.R           # Standalone R script for individual chart reproducibility
└── README.md                # Data dictionary, source citations, and local run instructions
```

### 2.1 The Gold Standard Prototype: READMITTED
The institutional template for all reports is `articles/readmitted/`:
- Investigates 3,000+ U.S. general acute hospitals across 6 clinical conditions penalized by CMS.
- Computes Excess Readmission Ratios (ERR), penalty exposure distributions, and hospital ownership stratifications.
- Produces paired exports: SVG/PNG high-DPI renders for print/mobile and interactive JSON specs for web canvas hydration.

---

## 3. Core Statistical Standards

### 3.1 Skewed Distributions and Median-First Reporting
Cultural, financial, and healthcare datasets are universally right-skewed (e.g., box office grosses, hospital penalty fines, streaming play counts). 
- **Standard**: The median and Interquartile Range (IQR) must be reported as the primary baseline before the arithmetic mean.
- **Reporting Rule**: Never cite an average without reporting whether the median deviates by more than 15%, which indicates extreme outlier leverage.

### 3.2 Risk Standardization and Excess Readmission Ratio (ERR)
In healthcare and policy journalism, raw readmission or mortality rates are fundamentally flawed due to patient age, comorbidities, and socio-demographic disparities:
$$\text{ERR} = \frac{\text{Predicted Readmissions}}{\text{Expected Readmissions}}$$
- An $\text{ERR} > 1.0000$ indicates that a hospital readmits more patients than expected after accounting for patient case mix.
- An $\text{ERR} \le 1.0000$ indicates average or superior performance.
- When reporting institutional differences (e.g., for-profit versus non-profit health systems), comparisons must use age-adjusted, risk-standardized metrics rather than raw discharge percentages.

### 3.3 Cell Suppression and Privacy Thresholds
To prevent identification of individuals and spurious statistical noise:
- Any clinical cell with sample size $n < 25$ is suppressed or marked with an asterisk indicating low statistical power.
- Cultural datasets (e.g., survey cohorts, rare streaming categories) require $n \ge 30$ before reporting subgroup medians.

---

## 4. The Dual-Target Chart Generation Pipeline

Artometrics utilizes R and Python to generate publication-grade graphics.

```
[Clean Data: Parquet/CSV]
           │
           ▼
[R Script: ggplot2 + theme_artometrics()]
           │
     ┌─────┴────────────────────────┐
     ▼                              ▼
[Static Target]            [Interactive Target]
High-DPI PNG                Plotly JSON
(Web fallback & Native)     (Web desktop canvas)
```

### 4.1 Shared Theme: `theme_artometrics()`
Located in `scripts/r/artometrics_theme.R`, the brand theme provides:
- Gridlines: Minimalist horizontal rules in subtle grey (`#E5E5E5`), vertical gridlines removed.
- Typography: DM Sans for titles, subtitles, and axis labels; DM Mono for coordinate ticks and numerical data callouts.
- Palette Tokens: Hot Cherry Red (`#E60000`) for focal callouts, Cobalt Blue (`#3367E7`) for baseline groups, and Slate Grey (`#6B6B6B`) for context cohorts.

### 4.2 Automated Export Command
To generate all charts for a report:
```bash
# Render specific report
npm run render:readmitted

# Or invoke the universal render runner
npm run render:articles
```

---

## 5. Structured Data Formatting: KeyPoints & Stat Grids

To power the floating stat boxes (Image 2 standard), every article's frontmatter must define `keyPoints` matching the strict parsing pattern:
```yaml
keyPoints:
  - "Metric Value — Detailed narrative description citing the finding and institutional context."
```

### 5.1 Formatting Requirements
1. **Value Prefix**: Must begin with the focal number, percentage, currency, or ratio (e.g., `48.1%`, `$85M`, `1.00485`, `742`, `13,631`).
2. **Separator**: An em-dash (`—`), en-dash (`–`), or spaced hyphen (`-`).
3. **Descriptive Sentence**: A complete, grammatically sound sentence explaining what the number means, avoiding vague assertions.
4. **Length**: Exactly 3 to 6 key points per article, with the top 4 featured in the floating hero grid.

---

## 6. Analytical Quality Assurance Checklist

Before any dataset or report moves from research to publication:
- [ ] Source data raw snapshot archived under `articles/<slug>/data/raw/`.
- [ ] Data cleaning transformations fully documented in reproducible script.
- [ ] Outlier inspection completed (z-scores > 3.0 or IQR > 1.5 flagged and evaluated).
- [ ] Confidence intervals or sample sizes explicitly stated in data footnotes.
- [ ] No emojis present in code, comments, datasets, or markdown copy.
- [ ] `npm run audit:articles` passes with zero errors and zero warnings.
