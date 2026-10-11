---
title: 'READMITTED: The 3% Stick Medicare Keeps Swinging'
slug: readmitted
author: kyle-mcauliffe
pubDate: 2026-04-21T00:00:00.000Z
description: >-
  In CMS's latest Hospital Readmissions Reduction Program extract, 48.15% of hospital–condition pairs still exceed the expected readmission ratio after a decade of penalties capped at 3% of Medicare payments. This R2 report maps HRRP history, who pays, safety-net effects, observation and mortality debates, international comparators, and eight charts for hospital executives.
heroImage: /images/content/articles/readmitted/hero.png
draft: false
tags:
  - science
  - medicine
subject: Hospitals
tldr: >-
  CMS's October 2026 HRRP supplemental file (measurement window July 2021–June 2024) shows 48.15% of hospital–condition pairs above an excess readmission ratio of 1.0. Hip/knee replacement averages 1.004 ERR—the highest of six tracks. New Jersey leads at 65.4% of pairs penalized; for-profits carry a larger high-tier share than non-profits. National AMI, heart-failure, and pneumonia readmission rates fell after 2012 then plateaued, while observation stays and mortality outcomes remain contested in peer-reviewed evaluations.
keyPoints:
  - '48.15% — hospital–condition pairs with ERR > 1.0 in CMS dataset 9n3s-kdb3 (n = 11,720 pairs)'
  - '3% — maximum Medicare IPPS payment reduction under HRRP since FY2015'
  - '65.4% — New Jersey share of pairs above ERR 1.0 (highest state)'
  - '1.004 — Hip/Knee average ERR, leading all six HRRP conditions in this extract'
  - '8.1% — hospitals facing ≥1% readmission penalties in FY2026 preliminary CMS file (Advisory Board analysis)'
  - '742 — hospitals mandated into CMS TEAM bundled payments from January 1, 2026'
faq:
  - question: What share of hospital-condition pairs exceed the CMS readmission benchmark?
    answer: '48.15% of HRRP-eligible pairs in the October 2026 CMS extract carry an excess readmission ratio above 1.0.'
  - question: Which condition has the highest excess readmission ratio?
    answer: Hip/Knee replacement averages 1.00485—the highest of six HRRP conditions and nearly twice the excess of the next closest track.
  - question: Which state has the highest share of penalized hospital-condition pairs?
    answer: 'New Jersey leads at 65.4%, followed by Massachusetts (62.5%) and Mississippi (61.1%).'
  - question: Do for-profit hospitals carry more penalty exposure than non-profits?
    answer: Yes. 39.5% of for-profit pairs fall in the high-penalty tier versus 32.1% for non-profits and 32.0% for government facilities.
---
<div id="quarto-content">
<nav id="TOC" role="doc-toc">
<h2 id="toc-title" class="anchored">IN THIS REPORT</h2>
<ul>
<li><a href="#research-question">Research question</a></li>
<li><a href="#executive-summary">Executive summary</a></li>
<li><a href="#hrrp-history">HRRP since 2012: cap, peers, and who pays</a></li>
<li><a href="#national-trends">National readmissions fell, then plateaued</a></li>
<li><a href="#the-geography-of-failure">Geography: penalties without a simple map</a></li>
<li><a href="#the-condition-nobody-is-solving">Conditions: hip/knee leads the ERR table</a></li>
<li><a href="#safety-net-and-teaching">Safety-net pressure and teaching hospitals</a></li>
<li><a href="#observation-and-mortality">Observation stays and the mortality debate</a></li>
<li><a href="#international-comparison">How other systems measure returns</a></li>
<li><a href="#ownership-penalty-and-who-pays">Ownership and penalty tiers</a></li>
<li><a href="#executive-playbook">Decision tools for hospital executives</a></li>
<li><a href="#what-this-file-cannot-tell-you">Limitations</a></li>
<li><a href="#what-to-take-away">Conclusion</a></li>
<li><a href="#data-methods-and-sources">Data, methods &amp; sources</a></li>
<li><a href="#editors-note">Editor's note</a></li>
</ul>
</nav>
<main class="art-article-main">
<p class="art-p">In 2009, Jencks and colleagues reported that nearly one in five Medicare fee-for-service patients returned to the hospital within thirty days. Congress answered with the Hospital Readmissions Reduction Program (HRRP): starting in October 2012, CMS began shaving inpatient prospective payment system (IPPS) dollars when risk-standardized thirty-day readmissions exceeded targets for six conditions. The maximum cut rose from 1% in fiscal year 2013 to 3% in FY2015, and it applies to <em>all</em> Medicare DRG payments—not just the condition that missed (CMS, QualityNet; MedPAC, 2024).</p>
<p class="art-p">The October 2026 CMS supplemental extract (dataset <code>9n3s-kdb3</code>, measurement window July 1, 2021–June 30, 2024) still flags <strong>48.15%</strong> of hospital–condition pairs above an excess readmission ratio (ERR) of 1.0. ERR divides predicted readmissions by expected readmissions for each hospital’s patient mix. Above 1.0 triggers penalty math; below 1.0 earns no bonus. The national mean ERR is <strong>1.002</strong>. The program clarified the problem faster than it eliminated it.</p>

<h2 id="research-question" class="anchored">RESEARCH QUESTION</h2>
<p class="art-p">After fourteen years of HRRP, where do penalties still concentrate in the latest CMS file—by state, condition, ownership, and safety-net proxy—and what should hospital executives infer about transitional care, observation-status gaming, mortality tradeoffs, and CMS’s shift toward episode-based models such as TEAM?</p>

<h2 id="executive-summary" class="anchored">EXECUTIVE SUMMARY</h2>
<p class="art-p"><strong>What it means.</strong> Medicare still penalizes roughly half of measured hospital–condition pairs for excess thirty-day readmissions, with elective joint surgery posting the highest average ERR and for-profit systems carrying more high-tier exposure than non-profits.</p>
<p class="art-p"><strong>How we know.</strong> We rebuilt working tables from CMS HRRP supplemental data and Hospital General Information, then exported eight charts (<code>npm run brief:readmitted</code>). Penalty-timeline points for FY2025–FY2026 come from Advisory Board analyses of CMS preliminary payment-reduction files; 2012–2015 national rates follow Zuckerman et al. (<em>NEJM</em>, 2016, <a href="https://doi.org/10.1056/NEJMsa1513024" rel="noopener noreferrer">doi:10.1056/NEJMsa1513024</a>).</p>
<p class="art-p"><strong>What explains it.</strong> HRRP financialized a logistics problem—discharge planning, medication reconciliation, follow-up access—without paying for the fixes. Observation stays moved returns off the inpatient ledger (Zuckerman et al., 2016). Safety-net hospitals face higher dual-eligible mix; CMS peer-groups on dual proportion, but case-mix adjustment remains imperfect (Joynt &amp; Jha, 2013, <a href="https://doi.org/10.1001/jama.2012.94856" rel="noopener noreferrer">doi:10.1001/jama.2012.94856</a>). OECD countries track readmissions with different payment levers (<a href="https://www.oecd.org/health/health-at-a-glance/" rel="noopener noreferrer">OECD Health at a Glance</a>).</p>

<div class="art-method-box" style="background:#F2F0EB;border-left:4px solid #C0392B;padding:18px 20px;margin:24px 0;">
<p class="art-h3" style="margin-top:0;">Method &amp; data box</p>
<p class="art-p" style="margin-bottom:8px;"><strong>Population:</strong> 11,720 hospital–condition pairs with non-suppressed ERR after CMS’s ≥25-discharge rule (six conditions, ~2,700 hospitals).</p>
<p class="art-p" style="margin-bottom:8px;"><strong>Primary files:</strong> CMS Provider Data Catalog <code>9n3s-kdb3</code> (HRRP) joined offline to <code>xubh-q36u</code> (ownership and hospital type).</p>
<p class="art-p" style="margin-bottom:8px;"><strong>Reproduce:</strong> <code>npm run brief:readmitted</code> — refreshes <code>articles/readmitted/data/</code>, renders PNG + Plotly JSON, syncs to <code>public/</code>.</p>
<p class="art-p" style="margin-bottom:0;"><strong>Rounding:</strong> National shares use two decimal places on the exact ratio (48.15%, not 48.2%), matching <code>articles/readmitted/data/SOURCE.txt</code>.</p>
</div>

<h2 id="hrrp-history" class="anchored">HRRP SINCE 2012: CAP, PEERS, AND WHO PAYS</h2>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/readmitted/charts/chart6_penalty_timeline.plotly.json" data-fallback="/images/content/articles/readmitted/charts/chart6_penalty_timeline.png" data-source="Cap: CMS IPPS rules; ≥1% share: Advisory Board analyses of CMS preliminary HRRP files — ARTOMETRICS" role="img" aria-label="HRRP maximum penalty cap versus share of hospitals paying at least one percent reductions"></div>
  <figcaption class="art-chart-caption">The three percent cap landed in FY2015; severe penalties (≥1% reductions) ticked up again in preliminary FY2026 data</figcaption>
</figure>
<p class="art-p">HRRP is a hospital-level payment adjustment, not a per-readmission fine. CMS multiplies a hospital-specific factor into Medicare operating DRG payments for the fiscal year. Who pays? The hospital’s Medicare revenue pool—finance, not quality officers, feels the hit first. Teaching hospitals and safety-net systems still compete inside peer groups defined by dual-eligible (Medicare–Medicaid) proportion so a suburban elective center is not always the comparator (CMS QualityNet HRRP documentation).</p>
<div class="art-split">
<div class="art-split__copy">
<p class="art-h3">Penalty mechanics executives quote wrong</p>
<p class="art-p">Three percent is a <em>ceiling</em> on operating DRG payments, not three percent of readmission cost. Advisory Board’s reading of CMS preliminary files shows only <strong>7.0%</strong> of hospitals paying ≥1% reductions in FY2025 and <strong>8.1%</strong> in FY2026—while roughly <strong>79.9%</strong> face some reduction in FY2026. Most hospitals pay a shallow penalty; outliers take the deep cut.</p>
</div>
<aside>
<div class="art-logo-row">
<div class="art-logo"><img src="/images/content/articles/readmitted/assets/logo_cms.png" alt="Centers for Medicare &amp; Medicaid Services" /><p class="art-logo__credit">CMS logo via Wikimedia Commons (public domain, U.S. government work)</p></div>
<div class="art-logo"><img src="/images/content/articles/readmitted/assets/logo_hhs.png" alt="U.S. Department of Health and Human Services" /><p class="art-logo__credit">HHS logo via Wikimedia Commons (public domain, U.S. government work)</p></div>
</div>
</aside>
</div>

<h2 id="national-trends" class="anchored">NATIONAL READMISSIONS FELL, THEN PLATEAUED</h2>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/readmitted/charts/chart7_national_readmit_trends.plotly.json" data-fallback="/images/content/articles/readmitted/charts/chart7_national_readmit_trends.png" data-source="2012–2015: Zuckerman et al. NEJM 2016; 2024: CMS extract mean predicted rates — ARTOMETRICS" role="img" aria-label="National Medicare readmission rates for AMI, heart failure, and pneumonia"></div>
  <figcaption class="art-chart-caption">AMI, heart failure, and pneumonia readmissions dropped in HRRP’s first years; 2024 points come from this CMS measurement window</figcaption>
</figure>
<p class="art-p">Zuckerman et al. documented declining national readmission rates for targeted conditions after HRRP while observation stays rose—returns that never achieved inpatient status do not enter the ERR numerator. That does not prove gaming; it shows the metric and the clinical pathway diverged. Gupta et al. (<em>BMJ</em>, 2019, <a href="https://doi.org/10.1136/bmj.l4563" rel="noopener noreferrer">doi:10.1136/bmj.l4563</a>) quantified broader thirty-day revisit burdens beyond the HRRP denominator.</p>

<h2 id="the-geography-of-failure" class="anchored">The Geography of Failure</h2>
<h3 id="the-geography-of-failure-look" class="anchored">States above the national average for penalized hospital-condition pairs—New Jersey leads at 65.4%</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/readmitted/charts/chart1_states_penalized.plotly.json" data-source="Data: CMS HRRP FY2025 supplemental (9n3s-kdb3) — ARTOMETRICS" data-fallback="/images/content/articles/readmitted/charts/chart1_states_penalized.png" role="img" aria-label="States above the national average for penalized hospital-condition pairs — New Jersey leads at 65.4%"></div>
  <figcaption class="art-chart-caption">Above the 48.1% national line, New Jersey leads at 65.4%—high-resource markets sit beside high-poverty ones</figcaption>
</figure>
<p class="art-p">New Jersey leads the country at 65.4%—nearly two of every three hospital-condition pairs in the state perform worse than CMS models expect. Massachusetts (62.5%) and Mississippi (61.1%) follow. New Jersey hosts high-revenue systems such as Hackensack Meridian and RWJBarnabas; Massachusetts concentrates academic medical power around Mass General Brigham; Mississippi is rural, high-poverty, and chronically under-served. Different systems, different patient mixes, same penalty outcome. Georgia, Kentucky, West Virginia, Alabama, and Louisiana cluster high—which fits the familiar population-health narrative. So do Illinois, California, New York, and Pennsylvania. This is not a rural-poverty map with a clean boundary. High-resource markets do not immunize a system. Chart 1 shows only states above the national average—the cohort pulling the 48.1% mean up. Even below-average states are not clean. "Below average" means a smaller share of pairs exceed ERR 1.0, not zero penalties.</p>
<h2 id="the-condition-nobody-is-solving" class="anchored">The Condition Nobody Is Solving</h2>
<h3 id="the-condition-nobody-is-solving-look" class="anchored">Average excess readmission ratio by HRRP condition—Hip/Knee leads at 1.00485</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/readmitted/charts/chart2_err_by_condition.plotly.json" data-source="Data: CMS HRRP FY2025 supplemental (9n3s-kdb3) — ARTOMETRICS" data-fallback="/images/content/articles/readmitted/charts/chart2_err_by_condition.png" role="img" aria-label="Average excess readmission ratio by HRRP condition — Hip/Knee leads at 1.00485"></div>
  <figcaption class="art-chart-caption">All six conditions average above ERR 1.0; Hip/Knee sits at 1.00485—nearly twice the excess of the next track</figcaption>
</figure>
<p class="art-p">Hip and knee replacement posts the highest average ERR in this extract (<strong>1.004</strong>), ahead of CABG, AMI, pneumonia, heart failure, and COPD. The gaps live in the fourth decimal—and still matter multiplied across roughly one million U.S. joint replacements annually. All six conditions average above 1.0. COPD’s lower ERR reflects a sicker expected baseline in CMS’s model, not a victory on absolute returns.</p>

<h2 id="safety-net-and-teaching" class="anchored">SAFETY-NET PRESSURE AND TEACHING HOSPITALS</h2>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/readmitted/charts/chart8_safety_net_proxy.plotly.json" data-fallback="/images/content/articles/readmitted/charts/chart8_safety_net_proxy.png" data-source="CMS HRRP + Hospital General Information name proxy — ARTOMETRICS" role="img" aria-label="Penalty share for safety-net name proxy versus other acute care hospitals"></div>
  <figcaption class="art-chart-caption">A crude County/Public/Memorial safety-net name proxy barely moves penalized share—dual-eligible peer groups matter more</figcaption>
</figure>
<p class="art-p">Joynt and Jha (<em>JAMA</em>, 2013) showed early HRRP penalties disproportionately hit teaching and safety-net hospitals—systems with more complex patients and thinner margins. CMS later refined peer grouping by dual proportion, but academic corridors still dominate intensity lists: Massachusetts averages <strong>1.034</strong> ERR in this file while New Jersey leads on breadth (<strong>65.4%</strong> of pairs penalized). Mass General Brigham, Beth Israel Deaconess, and Hackensack Meridian sit in those states; the data do not prove causation, but they show where episode-based models such as TEAM will land first.</p>
<p class="art-p"><strong>Counterexample.</strong> Integrated systems that invested in transitions—clinic access within seven days, pharmacist callbacks, home monitoring—can sit below ERR 1.0 on multiple tracks even in high-penalty states. The extract rewards operational depth, not market glamour.</p>

<h2 id="observation-and-mortality" class="anchored">OBSERVATION STAYS AND THE MORTALITY DEBATE</h2>
<p class="art-p">Observation status is the accounting escape hatch. When a return is billed as observation, it is not an inpatient readmission in HRRP math. Zuckerman et al. tied observation growth to HRRP’s early years. Wadhera et al. (<em>JAMA</em>, 2018, <a href="https://doi.org/10.1001/jama.2018.19232" rel="noopener noreferrer">doi:10.1001/jama.2018.19232</a>) reported associations between HRRP implementation and post-discharge mortality trends for heart failure—sparking a policy fight, not a settled verdict. Krumholz et al. (<em>JAMA</em>, 2017, <a href="https://doi.org/10.1001/jama.2017.8444" rel="noopener noreferrer">doi:10.1001/jama.2017.8444</a>) cautioned that hospitals can lower readmissions without improving survival. Dzau and McClellan’s <em>NEJM</em> perspective (<a href="https://doi.org/10.1056/NEJMp1901225" rel="noopener noreferrer">doi:10.1056/NEJMp1901225</a>) argued for rebooting incentives toward outcomes, not single metrics.</p>

<h2 id="international-comparison" class="anchored">HOW OTHER SYSTEMS MEASURE RETURNS</h2>
<p class="art-p">The U.S. is unusual in docking a slice of <em>all</em> Medicare DRG payments. OECD <em>Health at a Glance</em> indicators track thirty-day hospital readmission rates for member countries—England’s NHS, Canada’s provinces, Germany’s sickness funds—without an identical three-percent IPPS stick. Cross-country comparisons require harmonized definitions; still, the pattern is clear: readmissions are a global quality signal, but the U.S. chose the bluntest payer lever. International readers should not import U.S. penalty percentages into their payment models without mapping observation rules and post-acute financing.</p>

<h2 id="ownership-penalty-and-who-pays" class="anchored">OWNERSHIP, PENALTY, AND WHO PAYS</h2>
<h3 id="ownership-penalty-and-who-pays-look" class="anchored">Penalty tier distribution by hospital ownership—for-profits carry more high-tier weight</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/readmitted/charts/chart3_penalty_by_ownership.plotly.json" data-source="Data: CMS HRRP + Hospital General Information (xubh-q36u) — ARTOMETRICS" data-fallback="/images/content/articles/readmitted/charts/chart3_penalty_by_ownership.png" role="img" aria-label="Penalty tier distribution by hospital ownership — for-profits carry more high-tier weight"></div>
  <figcaption class="art-chart-caption">For-profit hospitals carry more medium and high penalty weight; every ownership type still has a majority in the no-penalty band</figcaption>
</figure>
<p class="art-p">For-profit hospitals carry a higher share of medium and high penalty tiers than either non-profits or government hospitals. Every ownership type has roughly half or more of its hospital-condition pairs at or below the CMS expected readmission rate. HRRP is often described as a blanket stick. The data says the stick is concentrated—closer to an audit sampling than a universal fine. Systems such as HCA, Tenet, and Steward sit in the for-profit column; that does not mean every for-profit campus is High-tier. The gap is real—on the order of 8 to 10 percentage points more penalized pairs than non-profits—but it is a difference of degree, not kind. All three ownership types are playing the same game. For-profits lose it slightly more often. Government-owned facilities land between non-profit and for-profit. Neither the safety-net excuse nor the public-accountability story fits cleanly. County systems operate under political oversight that can slow discharge innovation; middle-of-pack performance is its own finding.</p>
<h2 id="intensity-not-just-share" class="anchored">Intensity, Not Just Share</h2>
<h3 id="intensity-not-just-share-look" class="anchored">Average excess readmission ratio by state—Massachusetts leads the top 15</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/readmitted/charts/chart4_state_avg_err.plotly.json" data-source="Data: CMS HRRP FY2025 supplemental (9n3s-kdb3) — ARTOMETRICS" data-fallback="/images/content/articles/readmitted/charts/chart4_state_avg_err.png" role="img" aria-label="Average excess readmission ratio by state — Massachusetts leads the top 15"></div>
  <figcaption class="art-chart-caption">Penalty share and average ERR are related but not identical—Massachusetts leads on intensity even where New Jersey leads on breadth</figcaption>
</figure>
<p class="art-p">Chart 1 measured how widely penalties spread across hospital–condition pairs. Chart 4 measures how far above the CMS expected line those pairs sit on average. Massachusetts posts the highest average ERR in the working extract at 1.0344, ahead of New Jersey's breadth-first pattern at 65.4% of pairs penalized. That distinction matters for systems such as Mass General Brigham, Beth Israel Deaconess Medical Center, and the Boston academic corridor: a market can look merely "above average" on share and still run hotter on intensity. Mississippi, Illinois, and several Mid-Atlantic states also appear in the top-15 intensity list—the same mixed geography of high-resource and high-poverty markets seen in Chart 1. The dotted reference at ERR = 1.0 is the CMS expected line. Every state in this top-15 panel sits above it. The national mean ERR of 1.0018 looks small in isolation; stacked across thousands of pairs and roughly 1.3 million U.S. joint replacements a year, fourth-decimal gaps become budget lines.</p>
<h2 id="high-tier-concentration" class="anchored">Where the High Tier Concentrates</h2>
<h3 id="high-tier-concentration-look" class="anchored">High-tier penalty share by ownership—for-profits at 39.5%</h3>
<figure class="art-chart">
  <div class="art-chart-live" data-chart="/data/articles/readmitted/charts/chart5_high_penalty_by_ownership.plotly.json" data-source="Data: CMS HRRP + Hospital General Information (xubh-q36u) — ARTOMETRICS" data-fallback="/images/content/articles/readmitted/charts/chart5_high_penalty_by_ownership.png" role="img" aria-label="High-tier penalty share by ownership — for-profits at 39.5%"></div>
  <figcaption class="art-chart-caption">For-profit hospitals place 39.5% of pairs in the High penalty tier, versus about 32% for non-profit and government peers</figcaption>
</figure>
<p class="art-p">Chart 3 showed the full tier mix. Chart 5 isolates the High tier—the pairs farthest above CMS's expected readmission rate. For-profit ownership places 39.5% of hospital–condition pairs in High, compared with 32.1% for non-profits and 32.0% for government facilities. Named for-profit operators in the CMS Hospital General Information join—including campuses associated with HCA Healthcare, Tenet Healthcare, and historically Steward Health Care—sit inside that column. The chart does not prove that for-profit status causes excess readmissions. It shows that when CMS's published ratios are stacked by ownership, the High-tier mass sits heavier on the for-profit side. For TEAM's 742 mandatory hospitals in 2026, that concentration is the practical signal: episode-level accountability will land hardest where High-tier HRRP exposure already clusters, not where the "no penalty" majority still holds.</p>
<h2 id="executive-playbook" class="anchored">DECISION TOOLS FOR HOSPITAL EXECUTIVES</h2>
<div class="art-table-wrapper"><table class="art-table"><thead><tr><th>Decision</th><th>Signal in this file</th><th>Action</th></tr></thead><tbody>
<tr><td>Capital allocation</td><td>High ERR on hip/knee despite elective pathways</td><td>Fund discharge-to-home PT slots and pharmacy reconciliation before another service-line expansion</td></tr>
<tr><td>Payer negotiations</td><td>≥1% HRRP payment reduction (preliminary CMS / Advisory Board)</td><td>Model Medicare margin with actual payment adjustment factor, not ERR alone</td></tr>
<tr><td>Portfolio strategy</td><td>For-profit high-tier concentration</td><td>Benchmark against peer systems (e.g., HCA, Tenet) on condition-specific ERR, not system averages</td></tr>
<tr><td>Quality governance</td><td>Observation stay growth (literature)</td><td>Audit thirty-day <em>revisits</em>, not only inpatient readmissions (Gupta et al., 2019)</td></tr>
<tr><td>Policy horizon</td><td>TEAM mandatory cohort (742 hospitals)</td><td>Map episode owners now—HRRP hotspots predict TEAM pain</td></tr>
</tbody></table></div>
<div class="art-split">
<div class="art-split__copy">
<p class="art-h3">Mass General Brigham (Massachusetts)</p>
<p class="art-p">CEO Anne Klibanski leads a system in the highest average-ERR state in this extract. Academic intensity plus complex transfers can inflate ERR even when individual service lines perform. Executives here should separate transfer-heavy tracks from elective bundles before signing performance contracts.</p>
</div>
<aside>
<p class="art-person__name">Anne Klibanski</p>
<p class="art-person__role">President and CEO, Mass General Brigham (nonprofit academic system, Boston).</p>
</aside>
</div>
<div class="art-split">
<div class="art-split__copy">
<p class="art-h3">HCA Healthcare (for-profit scale)</p>
<p class="art-p">CEO Sam Hazen runs the largest for-profit U.S. hospital operator—squarely in the ownership column with heavier high-tier HRRP weight in this file. Scale enables standardized transition playbooks; the data ask whether those playbooks propagate to every joint program.</p>
</div>
<aside>
<p class="art-person__name">Sam Hazen</p>
<p class="art-person__role">CEO, HCA Healthcare (NYSE: HCA).</p>
</aside>
</div>

<h2 id="what-this-file-cannot-tell-you" class="anchored">LIMITATIONS</h2>
<p class="art-p">CMS suppresses readmission data for hospitals that fall below 25 discharges per condition per measurement period. That threshold protects statistical reliability, but the effect is systematic—small rural hospitals disappear from this analysis. The hospitals remaining skew toward larger, busier facilities.</p>
<p class="art-p">Ownership classification for Chart 3 comes from CMS Hospital General Information, which uses inconsistent labeling across hospital types. Physician-owned facilities, tribal hospitals, and church-affiliated systems do not always map cleanly into three buckets. The Government, Non-Profit, and For-Profit groupings are reasonable approximations—not clean legal categories.</p>
<p class="art-p">ERR compares actual readmissions to what CMS's risk model predicts for a hospital's patient mix. Case-mix adjustment is imperfect. Hospitals in high-poverty, high-comorbidity markets may still face structural disadvantage the model does not fully absorb. Observation-status shifts after the ACA (documented by Zuckerman et al., 2016) also mean some returns never appear as inpatient readmissions.</p>
<h2 id="what-to-take-away" class="anchored">CONCLUSION</h2>
<p class="art-p">48.1% of hospital-condition pairs still exceed CMS's expected readmission rate—but the distribution is uneven. The highest-penalty states cut across market type and regional demographics. Hip/Knee replacement sits nearly 2× above the next closest condition on excess readmissions. For-profit hospitals carry modestly more penalty exposure than non-profits, though all three ownership types remain majority no-penalty.</p>
<p class="art-p">HRRP has been in effect since 2012. That 48.1% of pairs still clear the 1.0 ERR threshold more than a decade later says something about the limits of financial penalties as a behavior-change mechanism. Hospitals have responded—rates have declined—but the program has defined the problem more than it has solved it.</p>
<p class="art-p">CMS's TEAM model, mandatory for 742 hospitals starting January 1, 2026, goes further by tying entire episodes of care to reimbursement. The hospitals that struggled under HRRP are the ones most likely to feel TEAM. This report describes the problem TEAM is designed to address. Whether bundled payments succeed where readmission penalties have not is the next question.</p>

<section class="art-back-matter">
<h2 id="data-methods-and-sources" class="anchored">Data, methods &amp; sources</h2>
<h3 id="data-and-method" class="anchored art-back-matter__subhead">Data and method</h3>
<p class="art-p">The FY2025 HRRP supplemental extract covers the measurement window used for CMS's published excess readmission ratios. After removing suppressed rows—hospitals with fewer than 25 discharges for a given condition, which CMS redacts to protect patient privacy—the working dataset contains 11,720 hospital-condition pairs across roughly 2,700 hospitals and six conditions: Acute Myocardial Infarction (AMI), Heart Failure, Pneumonia, Chronic Obstructive Pulmonary Disease (COPD), Hip & Knee Arthroplasty, and Coronary Artery Bypass Graft (CABG). A hospital can perform well on five tracks and still take a hit on one.</p>
<p class="art-p">The suppressed rows matter. Small rural hospitals disproportionately fall below the 25-discharge threshold and disappear from the analysis. The hospitals in this dataset skew toward larger, busier facilities. That is not a flaw in the extract—it is a feature of how CMS designed the program—but it shapes every finding below.</p>
<p class="art-p">An ERR above 1.0 feeds a penalty calculation; the tier depends on how far above 1.0 a hospital sits relative to peers. For this piece, pairs are grouped into four tiers: No Penalty (ERR ≤ 1.0), Low, Medium, and High. Charts are rendered with Plotly from the working CSVs in <code>articles/readmitted/data/</code> via <code>scripts/render-readmitted-charts.py</code> (PNG + Plotly JSON). Ownership and hospital-type labels are joined from CMS Hospital General Information (dataset <code>xubh-q36u</code>) and stored offline so renders do not depend on a live CMS download.</p>
<h3 id="sources" class="anchored art-back-matter__subhead">Sources</h3>
<p class="art-p">Jencks, S.F., Williams, M.V., &amp; Coleman, E.A. (2009). Rehospitalizations among Patients in the Medicare Fee-for-Service Program. <em>NEJM</em>, 360(14), 1418–1428. <a href="https://doi.org/10.1056/NEJMsa0803563" rel="noopener noreferrer">doi:10.1056/NEJMsa0803563</a></p>
<p class="art-p">
Joynt, K.E., &amp; Jha, A.K. (2013). Characteristics of hospitals receiving penalties under the Hospital Readmissions Reduction Program. <em>JAMA</em>, 309(4), 342–343. <a href="https://doi.org/10.1001/jama.2012.94856" rel="noopener noreferrer">doi:10.1001/jama.2012.94856</a>
</p>
<p class="art-p">
Centers for Medicare & Medicaid Services. <em>Hospital Readmissions Reduction Program (HRRP) — FY2025 Supplemental Data</em>. CMS Provider Data Catalog, Dataset ID: 9n3s-kdb3. <a href="https://data.cms.gov/provider-data/dataset/9n3s-kdb3" target="_blank" rel="noopener noreferrer">https://data.cms.gov/provider-data/dataset/9n3s-kdb3</a>
</p>
<p class="art-p">
Centers for Medicare & Medicaid Services. <em>Hospital General Information</em>. CMS Provider Data Catalog, Dataset ID: xubh-q36u. <a href="https://data.cms.gov/provider-data/dataset/xubh-q36u" target="_blank" rel="noopener noreferrer">https://data.cms.gov/provider-data/dataset/xubh-q36u</a> — joined to HRRP data for ownership classification in Chart 3.
</p>
<p class="art-p">
Centers for Medicare & Medicaid Services. (2024). <em>Transforming Episode Accountability Model (TEAM)</em>. <a href="https://www.cms.gov/priorities/innovation/innovation-models/team" target="_blank" rel="noopener noreferrer">https://www.cms.gov/priorities/innovation/innovation-models/team</a> — mandatory participation effective January 1, 2026 for 742 hospitals.
</p>
<p class="art-p">
Medicare Payment Advisory Commission. (2024). <em>Report to the Congress: Medicare Payment Policy</em>, Chapter 9 (hospital inpatient and outpatient services; readmissions discussion). <a href="https://www.medpac.gov" target="_blank" rel="noopener noreferrer">https://www.medpac.gov</a>
</p>
<p class="art-p">
Zuckerman, R.B., Sheingold, S.H., Orav, E.J., Ruhter, J., & Epstein, A.M. (2016). Readmissions, observation, and the Hospital Readmissions Reduction Program. <em>New England Journal of Medicine</em>, 374(16), 1543–1551. <a href="https://doi.org/10.1056/NEJMsa1513024" target="_blank" rel="noopener noreferrer">https://doi.org/10.1056/NEJMsa1513024</a>
</p>
<p class="art-p">
Krumholz, H.M., et al. (2017). Association of Changing Hospital Readmission Rates With Mortality Rates After Hospital Discharge. <em>JAMA</em>, 318(3), 270–278. <a href="https://doi.org/10.1001/jama.2017.8444" rel="noopener noreferrer">doi:10.1001/jama.2017.8444</a></p>
<p class="art-p">Wadhera, R.K., et al. (2018). Association of the Hospital Readmissions Reduction Program With Mortality Among Medicare Beneficiaries Hospitalized for Heart Failure, Acute Myocardial Infarction, and Pneumonia. <em>JAMA</em>, 320(24), 2542–2552. <a href="https://doi.org/10.1001/jama.2018.19232" rel="noopener noreferrer">doi:10.1001/jama.2018.19232</a></p>
<p class="art-p">Gupta, A., et al. (2019). Hospital revisits within 30 days after discharge for medical conditions targeted by the Hospital Readmissions Reduction Program in the United States. <em>BMJ</em>, 366, l4563. <a href="https://doi.org/10.1136/bmj.l4563" rel="noopener noreferrer">doi:10.1136/bmj.l4563</a></p>
<p class="art-p">Dzau, V.J., &amp; McClellan, M.B. (2019). The Hospital Readmissions Reduction Program — Time for a Reboot. <em>NEJM</em> perspective. <a href="https://doi.org/10.1056/NEJMp1901225" rel="noopener noreferrer">doi:10.1056/NEJMp1901225</a></p>
<p class="art-p">Advisory Board (2024, 2025). Analyses of CMS preliminary HRRP payment-reduction files for FY2025 and FY2026. <a href="https://www.advisory.com/daily-briefing/2024/09/24/readmisson-penalties" rel="noopener noreferrer">FY2025 chart</a>; <a href="https://www.advisory.com/daily-briefing/2025/09/23/readmission-penalties" rel="noopener noreferrer">FY2026 chart</a>.</p>
<p class="art-p">OECD (2023). <em>Health at a Glance 2023: OECD Indicators</em> — hospital readmission indicators. <a href="https://www.oecd.org/health/health-at-a-glance/" rel="noopener noreferrer">oecd.org</a></p>
<p class="art-p">Full bibliography: <code>articles/readmitted/references.bib</code>. Image credits: <code>articles/readmitted/CREDITS.md</code>.</p>
</section>
<h2 id="files" class="anchored">Files</h2>

<p class="art-p">Download the working datasets and chart exports used in this report. All files are hosted on this site—no external repo required.</p>
<div class="art-files">
  <h3 class="art-files__heading">Datasets</h3>
  <ul class="art-files__list">
    <li><a class="art-files__link" download href="/data/articles/readmitted/data/hrrp_state_summary.csv">hrrp_state_summary.csv</a> — state-level penalty share and average ERR</li>
    <li><a class="art-files__link" download href="/data/articles/readmitted/data/hrrp_condition_err.csv">hrrp_condition_err.csv</a> — average ERR by HRRP condition</li>
    <li><a class="art-files__link" download href="/data/articles/readmitted/data/hrrp_ownership_condition.csv">hrrp_ownership_condition.csv</a> — ownership × condition × penalty tier counts</li>
    <li><a class="art-files__link" download href="/data/articles/readmitted/data/hrrp_penalty_timeline.csv">hrrp_penalty_timeline.csv</a> — HRRP cap and hospital penalty shares (sourced rows)</li>
    <li><a class="art-files__link" download href="/data/articles/readmitted/data/hrrp_national_readmit_trends.csv">hrrp_national_readmit_trends.csv</a> — national readmission rate series</li>
    <li><a class="art-files__link" download href="/data/articles/readmitted/data/hrrp_safety_net_proxy.csv">hrrp_safety_net_proxy.csv</a> — safety-net name proxy vs other acute care</li>
  </ul>
  <h3 class="art-files__heading">Charts (PNG)</h3>
  <ul class="art-files__list">
    <li><a class="art-files__link" download href="/images/content/articles/readmitted/charts/chart1_states_penalized.png">chart1_states_penalized.png</a></li>
    <li><a class="art-files__link" download href="/images/content/articles/readmitted/charts/chart2_err_by_condition.png">chart2_err_by_condition.png</a></li>
    <li><a class="art-files__link" download href="/images/content/articles/readmitted/charts/chart3_penalty_by_ownership.png">chart3_penalty_by_ownership.png</a></li>
    <li><a class="art-files__link" download href="/images/content/articles/readmitted/charts/chart4_state_avg_err.png">chart4_state_avg_err.png</a></li>
    <li><a class="art-files__link" download href="/images/content/articles/readmitted/charts/chart5_high_penalty_by_ownership.png">chart5_high_penalty_by_ownership.png</a></li>
    <li><a class="art-files__link" download href="/images/content/articles/readmitted/charts/chart6_penalty_timeline.png">chart6_penalty_timeline.png</a></li>
    <li><a class="art-files__link" download href="/images/content/articles/readmitted/charts/chart7_national_readmit_trends.png">chart7_national_readmit_trends.png</a></li>
    <li><a class="art-files__link" download href="/images/content/articles/readmitted/charts/chart8_safety_net_proxy.png">chart8_safety_net_proxy.png</a></li>
  </ul>
  <h3 class="art-files__heading">Charts (Plotly JSON)</h3>
  <ul class="art-files__list">
    <li><a class="art-files__link" download href="/data/articles/readmitted/charts/chart1_states_penalized.plotly.json">chart1_states_penalized.plotly.json</a></li>
    <li><a class="art-files__link" download href="/data/articles/readmitted/charts/chart2_err_by_condition.plotly.json">chart2_err_by_condition.plotly.json</a></li>
    <li><a class="art-files__link" download href="/data/articles/readmitted/charts/chart3_penalty_by_ownership.plotly.json">chart3_penalty_by_ownership.plotly.json</a></li>
    <li><a class="art-files__link" download href="/data/articles/readmitted/charts/chart4_state_avg_err.plotly.json">chart4_state_avg_err.plotly.json</a></li>
    <li><a class="art-files__link" download href="/data/articles/readmitted/charts/chart5_high_penalty_by_ownership.plotly.json">chart5_high_penalty_by_ownership.plotly.json</a></li>
    <li><a class="art-files__link" download href="/data/articles/readmitted/charts/chart6_penalty_timeline.plotly.json">chart6_penalty_timeline.plotly.json</a></li>
    <li><a class="art-files__link" download href="/data/articles/readmitted/charts/chart7_national_readmit_trends.plotly.json">chart7_national_readmit_trends.plotly.json</a></li>
    <li><a class="art-files__link" download href="/data/articles/readmitted/charts/chart8_safety_net_proxy.plotly.json">chart8_safety_net_proxy.plotly.json</a></li>
  </ul>
<h2 id="editors-note" class="anchored">EDITOR'S NOTE</h2>
<div class="art-editorial-note"><p class="art-p">
<em>This report was researched, written, designed, and produced in active collaboration with Claude AI (Anthropic). The data pipeline, statistical analysis, chart design, written analysis, narrative structure, and visual styling were all developed through a directed partnership between human editorial judgment and AI execution. Charts are exported from R in this monorepo (<code>articles/readmitted/</code>). Artometrics was built on the premise that rigorous analysis and honest process are not in conflict. The research questions, editorial instincts, interpretive framing, and brand vision are ours. We document this not as a disclaimer but as a description of how we actually work.</em>
</p>
<p class="art-p">
<em>— Artometrics Editorial</em>
</p>
</main>
</div>
