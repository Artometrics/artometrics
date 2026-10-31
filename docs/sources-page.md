# Decided

Sources page. These choices are the contract for `/sources`.

1. The ledger is a new crawlable `/sources` route, linked from the Resources page.
2. Reports are grouped by the site's existing topics: Arts, Sports, Science, Humanities, Civics, and Culture.
3. "Updated through" is the data coverage end when a citation states one. Otherwise it is the latest citation date. Otherwise it says "not yet checked". Editorial indexes say "editorial index" instead of a date.
4. Data-fix notes sit under their parent issue (`anime-data-fix` under Anime, and the same for Padres and Franchise).
5. Dataset links appear only where a dataset pack already exists in `data/datasets.ts`.
6. Citations without a URL are plain text with a "no link yet" tag.
7. The page is generated from `magazine/issues.json` at build time (`npm run sources`, also run by `npm run content`) into `src/generated/sources.json`.
