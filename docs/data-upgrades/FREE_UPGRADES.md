# Kyle-approved free data upgrades (implementation notes)

Regenerate helpers:

| Command | Purpose |
| --- | --- |
| `npm run data:cpi` | Refresh `data/reference/cpi/` from FRED CPIAUCSL |
| `npm run data:real-usd` | CPI cache + inflation-adjusted chart siblings |
| `npm run data:sec` | SEC companyfacts revenue tables |
| `npm run cms:check-hrrp` | Compare CMS HRRP release vs `SOURCE.txt` |
| `npm run sync:padres-baseball` | Lahman attempt + MLB Stats API snapshot |

See [`REAL_USD_CHARTS.md`](./REAL_USD_CHARTS.md) for CPI-adjusted chart list.
