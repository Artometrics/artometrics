# Screenshots: Kyle's iPhone review fixes

Full page, header to the end of the page. 390 px wide (phone) and 1280 px wide (desktop), light and dark. Same tool for both sets: `node scripts/capture-fullpage.mjs <dir> --paths /,/franchise` against a build of `main` (before) and this branch (after). Phone shots are saved at 1x, so text is small; open them at full size.

| Page | Before | After |
|---|---|---|
| Home, phone | `before/home-mobile-{light,dark}.jpg` | `after/home-mobile-{light,dark}.jpg` |
| Home, desktop | `before/home-desktop-{light,dark}.jpg` | `after/home-desktop-{light,dark}.jpg` |
| Franchise, phone | `before/franchise-mobile-{light,dark}.jpg` | `after/franchise-mobile-{light,dark}.jpg` |
| Franchise, desktop | `before/franchise-desktop-{light,dark}.jpg` | `after/franchise-desktop-{light,dark}.jpg` |
| Franchise PDF, first eight pages | | `after/franchise-pdf-first-pages.jpg` |

The home page and article pages have no site footer by design (`footer="none"`), so the full-page shots end with the last section.
