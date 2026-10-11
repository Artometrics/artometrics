# FRANCHISE — deep dive (~11:00, ~1,700 words)

## Opening

Picture two ledgers.

On a playground, a child swaps a cardboard Pikachu.

In a boardroom, Bob Iger signs a seventy-one point three billion dollar check for Twenty-First Century Fox.

Both trades assume the same asset: a character that can be sold again tomorrow.

This deep dive walks one mid-2019 photograph of that market — the TidyTuesday media-franchise file scraped from Wikipedia on July second, twenty-nineteen.

One hundred and three franchises.

One point five two two trillion dollars in lifetime revenue estimates.

Not audited studio profit.

Still the cleanest public way to compare how money attaches to intellectual property.

Every number below traces to franchise.csv or verified_numbers.csv, sources S001 and S017, unless we explicitly switch to SEC filings.

## The consultant frame

Henry Jenkins described convergence culture: audiences follow characters across formats.

Marc Steinberg’s media-mix scholarship shows the Japanese extreme — television animation as billboard for merchandise, rooted in sponsor models from the nineteen-sixties.

Hollywood’s parallel is vertical integration: own the character, own the park ticket, own the streaming shelf.

This report is not fan ranking.

It is licensing geometry.

For each pattern we ask three things.

What does it mean for a buyer?

How do we know it — source and method?

What mechanism explains it — economics, technology, who could acquire whom, and cultural history?

## Pattern one — merchandise owns the row sum

Recompute every revenue category in the committed CSV.

Merchandise, licensing, and retail: fifty-six point zero percent.

Video games: twenty point zero.

Box office: eight point nine.

Total lifetime revenue across rows: one point five two two trillion.

Method: category sums divided by total revenue, logged in verified_numbers.csv.

Mechanism: theatrical releases are high-visibility, low-repeat events.

Merchandise and games are inventory you can ship weekly.

Japan’s production-committee system splits copyright among publishers, broadcasters, and toy makers, which hard-wires plush and magazines into the budget.

Hollywood historically relied on distributors and licensors, but Disney’s Experiences segment — parks, resorts, cruise, merchandise — is the American answer to the same question.

Counterexample: properties born as games.

Video-game-origin franchises in the file sum to three hundred thirty-four point nine billion dollars in lifetime totals by original-media tag — larger than film-first seeds.

Mario stays Nintendo-blue on the chart because the company couples hardware and mascot IP.

## Pattern one-b — revenue per year rewards compounding SKUs

Divide lifetime totals by years alive as of twenty-nineteen.

Pokémon clears about three point nine five billion dollars per calendar year of existence.

The Marvel Cinematic Universe row clears about two point eight billion despite being younger.

Hello Kitty’s eighty billion lifetime total spans decades — legacy mass, not speed.

Method: chart two, lifetime revenue divided by max of one year and twenty-nineteen minus year_created.

Mechanism: games and cards bill monthly; theatrical bills once per cycle.

Counterexample: young film franchises that spike on opening weekend but lack merchandise depth — pretty on the marquee, thin in the CSV.

## Pattern two — who tops the table, and who is missing

Pokémon leads at ninety point nine billion on screen — ninety point eight six three in the file.

Hello Kitty: eighty point zero three.

Winnie the Pooh: seventy-four point five.

Star Wars: sixty-three point zero.

Marvel Cinematic Universe row: thirty-one point zero.

Method: sum revenue rows per franchise name in franchise.csv.

Mechanism: Pokémon is a game-first flywheel — anime promotes cards; cards promote games.

Hello Kitty is almost entirely merchandise.

Star Wars is the Hollywood template Disney paid four point zero five billion to buy in Lucasfilm — theatrical plus licensing at scale.

Counterexample: stacking rows.

Pokémon is the largest single named property, but Star Wars plus MCU already exceed it before Spider-Man adjunct rows or Wizarding World.

The chart teaches composition, not crowning one winner.

## Pattern three — geography and the four-billion-dollar floor

Thirty-five Japanese-origin franchises in our entity table contribute six hundred thirty-two point eight billion in lifetime totals.

Forty-six United States-origin franchises contribute seven hundred eighteen point nine billion.

Merchandise share within those buckets: fifty-two point three percent for Japan, sixty-three point seven for the US.

Method: region_origin tags in entities_franchises.csv, summed revenue, chart fifteen.

Mechanism: US studios built global theatrical pipelines and theme-park engines.

Japanese media-mix franchises optimised for domestic retail density and long-tail collectibles.

Counterexample: national icons below Wikipedia’s informal four-billion-dollar inclusion floor — many tokusatsu and anime properties never enter the English table even when culturally load-bearing at home.

## Pattern four — Wikipedia moved between twenty-nineteen and twenty-twenty-six

We hand-mapped one hundred and three twenty-nineteen rows to twenty-twenty-six Wikipedia titles.

Eighty-two pairs carry revenue in both years.

Method: franchise_crosswalk_2019_2026.csv and a delta chart — chart ten.

Largest upward revisions in that paired set include mobile-native titles such as Candy Crush Saga and Mortal Kombat, plus anime rows like Naruto.

Mechanism: editors add categories — mobile games, live-service revenue — that the twenty-nineteen scrape under-weighted.

Counterexample: paired rows that fall — often when Wikipedia splits or re-labels a property.

Treat the ledger as a survey, not GAAP.

## Pattern four-b — original medium sets the extraction layer

Summing lifetime revenue by original_media tag, video games lead at three hundred thirty-four point nine billion, manga at two hundred fifty-three point eight, animated series at one hundred twenty-one.

Film-origin totals are one hundred eleven point seven billion — substantial, but not the whole story.

Method: chart five and revenue_mix_by_original_medium.csv.

Mechanism: a franchise is not defined by its debut channel but by which streams the owner chooses to license.

Shueisha’s Jump comics rows show publishing plus animation plus games stacked on one character bible.

Disney Princess is a retail line built atop film assets — ninety-nine point nine percent merchandise in the Pokémon row’s cousin property Disney Princess.

Counterexample: novel-first Wizarding World — books set the canon, but Warner Bros. had to build theatrical and merchandise desks to capture value.

## Pattern five — box office is not how the top twenty breathe

Among the top twenty franchises by lifetime revenue, box office is often a thin slice.

The Marvel Cinematic Universe row is sixty-seven point seven percent box office in the file — an outlier.

Hello Kitty, Disney Princess, Mario — near zero theatrical share.

Method: chart fourteen, box-office dollars divided by franchise total for each top-twenty row.

Mechanism: film-first universes amortise development across sequels; character-first mascots skip the cinema tax entirely.

Counterexample: Wizarding World still carries a double-digit box-office band because Warner Bros. built a theatrical cycle — until Fantastic Beasts fatigue showed that even billion-dollar literary IP needs slate discipline.

## Pattern six — Disney as ownership literacy

Unconsolidated owner totals show The Walt Disney Company at two hundred fifty-eight point nine billion, Lucasfilm at sixty-three, Marvel labels separate.

Consolidated: four hundred twenty-six point two billion.

Nintendo’s owner label: forty-nine point zero billion.

Top owner share after Fox consolidation: twenty-eight percent of the file.

Top-five owners: forty-six point four percent.

Method: owner_consolidation_rules.csv and owner_totals_derived.csv, charts three-a, three-b, twelve.

Mechanism: modern libraries are assembled by M&A — Pixar seven point four billion, Marvel four billion, Lucasfilm four point zero five billion, Fox seventy-one point three billion enterprise value per merger proxy, sources S009 through S012.

Compare check size to a single anchor franchise row — chart thirteen — and you see capitalization of future licensing, not applause for one weekend.

Audited FY twenty-twenty-four segment revenue from Disney’s Form ten-K exhibit: Entertainment forty-one point one eight six billion, Sports seventeen point six one nine, Experiences thirty-four point one five one — source S081.

Experiences is not a side hustle.

It is the physical licensing engine for the same characters box office promotes.

## Pattern six-b — Sony, Universal, and fragmented libraries

Spider-Man sits in a split-rights cage: Marvel Entertainment on merchandise rows, Sony Pictures on film grosses in the owner string.

Fast and Furious and Jurassic World show Universal’s blockbuster model without Disney-scale consolidation.

Method: read owner fields literally in franchise.csv; do not assume one checkbook.

Mechanism: when theatrical rights sit with a rival studio, enterprise value leaks across corporate boundaries — a lesson for any CEO evaluating co-production.

Counterexample: Nintendo — forty-nine billion on the owner label, ninety point nine on Pokémon rows — hardware and IP married on one Japanese balance sheet.

## Pattern seven — theatrical seriality as risk management

Franchise installments as a share of domestic top-ten films: sixty percent in twenty-ten, seventy in twenty-fifteen, eighty in twenty-nineteen, ninety in twenty-twenty-four.

Method: Box Office Mojo yearly pages, manual coding in top10_franchise_share_by_year.csv.

Mechanism: recognition lowers marketing cost; shared universes amortise development.

Counterexamples: Universal’s Dark Universe after The Mummy, DC extended-universe false starts, Ghostbusters twenty-sixteen backlash, Angry Birds mobile peak-and-fade documented in franchise_failures.csv.

Ownership without operating discipline is expensive noise.

DC Entertainment rows sum to about forty-four point four billion in the file — Batman, Wizarding World, and adjacent labels — yet Warner Bros. spent a decade proving that table strength is not slate execution.

Toho’s Godzilla rows are smaller in the English Wikipedia table but anchor national merchandise cycles at home — a reminder that our geography tags describe origin, not audience size.

## Pattern eight — what we still cannot see

The file has no per-title profit, no streaming ARPU, no China-only mobile revenue except where editors added it by twenty-twenty-six.

Method: read limitations alongside every chart.

Mechanism: public ledgers lag private dashboards — especially for live-service games and theme-park yield management.

Counterexample: trusting a single Wikipedia row for Simpsons after Fox — thirteen point five billion in twenty-nineteen versus a much lower twenty-twenty-six figure when editors re-scoped the entry.

Always pair S001 with S017 when you quote growth.

## Close — three decision tools

Ownership lens: consolidate subsidiaries before benchmarking Disney versus Nintendo.

Margin lens: rank streams for your property — merchandise, games, parks, subscription — because box-office rank mis-ranks Hello Kitty against Pokémon.

Capital lens: acquisition price is the net present value of licensing you believe remains.

Reproduce charts with npm run brief:franchise.

Read the methods box on the live report.

Then decide what you are buying when you greenlight a sequel: a movie, or a license to print money.

The playground trade and the Fox check differ in scale, not in logic.

Both bet that attention converts into property rights you can invoice again next quarter — merchandise rows, game micro-transactions, or a park turnstile.

That is the story the mid-2019 file still tells in twenty-twenty-six.
