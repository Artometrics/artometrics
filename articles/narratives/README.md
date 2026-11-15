# NARRATIVES: The Field Guide Culture Workers Needed

**Desk:** civics · **Live:** https://artometrics.com/narratives/

A working framework for treating economic narratives as contagious, falsifiable objects — built from Shiller and Kuran, not a proprietary dataset.

## Layout

```text
narratives/
  _quarto.yml
  narratives.qmd
  data/
  charts/
  figures/
```

```bash
cd articles/narratives
quarto render
npm run sync:article -- --slug narratives
```
