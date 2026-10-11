# FRANCHISE — deep dive (~12:00)

## Cold open

A trading card worth lunch money and a two-hundred-million-dollar Marvel sequel sit on the same balance-sheet idea: recurring rights. The mid-2019 media-franchise file is our x-ray — one hundred three properties that Wikipedia editors judged above roughly four billion dollars in lifetime revenue, scraped for TidyTuesday on July second, twenty-nineteen. Every figure below is an estimate. Every pattern is still operational.

## Executive frame

Henry Jenkins called it convergence culture: stories that jump formats because audiences follow characters, not channels. Marc Steinberg’s media-mix work in Japan shows the extreme case — anime as billboard for merchandise. American studios learned the same lesson through theme parks, licensing desks, and balance-sheet M&A.

This report asks three questions CEOs actually need answered. Where does franchise money pool? Who owns the pools after subsidiaries are folded? And when does theatrical success stop predicting enterprise value?

## The ledger

Recompute from `franchise.csv` and merchandise is fifty-six point zero percent of row-sum revenue. Video games are twenty point zero. Box office is eight point nine. The old headline “sixty-one percent merchandise” was rounding and franchise-count drift; we publish the recomputed share and document the gap in the methods box.

Pokémon leads at ninety point nine billion — not because it out-earned every combination of Marvel, Star Wars, and Wizarding World rows you could stitch together, but because it is the single largest named property in the file. Star Wars is sixty-three. The MCU row is thirty-one. Add them and you are already past Pokémon before merchandise sub-rows elsewhere.

Chart one stacks the top twenty by revenue stream. Merchandise paints the bars red. Mario stays Nintendo-blue because the company historically refuses to license the plumber into every aisle. Jump comics stay purple — publishing, not plush.

Chart two divides lifetime totals by years alive as of twenty-nineteen. Pokémon clears about four billion per year. Hello Kitty’s eighty billion is legacy mass, not speed.

## Disney as case study

Chart three is an ownership literacy test. Raw owners show Disney at two hundred fifty-nine billion, Marvel at twenty, Fox at seventeen — as if they compete. Consolidated, Disney is four hundred twenty-six billion in attributed franchise rows. Nintendo is forty-nine on its own label, ninety-one if you merge Pokémon Company strings.

Chart eight plots acquisition price against a single anchor franchise row — not ROI, a sanity check. Lucasfilm for four billion against a sixty-three-billion Star Wars row. Marvel for four billion against thirty-one for the MCU label. Fox for seventy-one billion against a thirteen-billion Simpsons anchor — the deal was infrastructure, not one IP.

Chart nine leaves Wikipedia for audited money: Disney’s FY twenty-twenty-four Form ten-K. Experiences — parks and cruise — thirty-four point two billion. Entertainment forty-two point two. Sports eighteen. Parks are not a side hustle; they are a third of the enterprise, and they monetize the same characters the box office advertises.

## Theatrical seriality

Chart seven tracks franchise installments as a share of the domestic top ten for selected years. Sixty percent in twenty-ten. Seventy in twenty-fifteen. Eighty in twenty-nineteen. Ninety in twenty-twenty-four. Method: Box Office Mojo yearly pages, manual franchise coding, documented in `top10_franchise_share_by_year.csv`.

This is why sequel greenlights feel like risk management. Recognition lowers marketing cost. Shared universes amortize development. The counterexamples — Dark Universe, DC’s false starts, Fantastic Beasts fatigue — prove the strategy is not automatic.

## Comparisons

Warner’s DC rows total forty-four billion in the file — formidable on paper, volatile in execution. Sony and Universal spread across Spider-Man adjunct rows, Jurassic, and Fast & Furious without a single Disney-scale consolidator. Nintendo keeps hardware and IP married; Pokémon proves game-first franchises can outrun film-first ones. Toho’s Godzilla rows are smaller in the Wikipedia table but culturally load-bearing in Japan — a reminder that the four-billion floor excludes most national icons.

## Failure modes

Read `franchise_failures.csv` as a counterfactual library. Universal shelved Dark Universe after *The Mummy*. Ghostbusters twenty-sixteen rebooted into backlash. Angry Birds peaked on mobile while merchandise rows linger. DC’s extended universe spent years proving that IP ownership without slate discipline is an expensive hobby.

## Decision tools

**Ownership lens.** Before benchmarking Disney versus Nintendo, consolidate subsidiaries. M&A is how modern libraries are built.

**Margin lens.** Rank revenue streams for your property: theatrical, home, games, merchandise, parks, subscription. Box office rank alone will mis-rank Hello Kitty against Pokémon.

**Capital lens.** Acquisition price is the NPV of licensing you believe you can still extract. Compare check size to franchise-row scale, then to parks and merchandise capacity — not opening weekend.

## Close

Franchise economics is the art of turning attention into repeatable property rights. The mid-2019 file is a photograph, not a live feed. But the structure — merchandise-heavy ledgers, consolidated Disney scale, serial domestic box office — still governs how CEOs should read the next greenlight.

Reproduce every chart: `npm run brief:franchise`. Read the methods box on the live report. Download the CSVs. Then decide what you are buying when you buy a sequel: a movie, or a license to print money.
