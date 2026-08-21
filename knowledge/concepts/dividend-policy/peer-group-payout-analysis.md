# Peer group approach to dividend policy

**Core idea:** The second way to assess dividend policy is to compare the firm with similar companies — usually the same sector and the same market — and pick a policy that makes it look comparable. This is the approach firms actually use, and it is the mechanism behind the "me-too-ism" that drives real dividend behavior. It is easy to apply and easy to misuse. Its virtues are that peers share business risk, growth prospects and capital intensity, so a large gap against the peer group is worth explaining. Its defects are that the peer average embeds whatever mistakes the sector is collectively making, the group's own FCFE is often negative, and dividend-only comparisons ignore buybacks entirely.

**Formulas:**
- Group dividend yield = Σ Dividends across peers / Σ Market Cap across peers (a value-weighted yield), or the median of individual yields for a size-neutral read.
- Group payout ratio = Σ Dividends / Σ Net Income. Note this differs from the average of individual payout ratios, sometimes hugely, when some peers have losses.
- Firm's relative position = Firm yield − Group yield, and Firm payout − Group payout.
- Buyback-inclusive comparison: Cash return / FCFE = (Dividends + Buybacks)/FCFE for each peer, then compare against the group median. Report NA when FCFE ≤ 0.

**Procedure:**
1. Define the peer group. Damodaran's practice: same sector, and either the same market or global with a size filter (for example, "Global Diversified Mining & Iron Ore, market cap > $1bn"). Say explicitly which filter you used, because the choice drives the answer.
2. For each peer collect market cap, dividends, buybacks, net income and FCFE.
3. Compute for each: dividend yield, dividend payout, and cash return as a percentage of FCFE.
4. Report both the **average** and the **median** for the group. In sectors where most firms pay nothing, the median is zero and the average is dominated by two or three large payers — the divergence is itself the finding.
5. Position the firm against both statistics, on both the trailing year and a multi-year average.
6. Before concluding, sanity-check the group. If the group's average FCFE is negative, the group is collectively paying out more than it generates, and matching it is not a target worth hitting.
7. Add buybacks. A firm that pays no dividend but returns 100% of FCFE through repurchases is not "underpaying" relative to a dividend-paying peer group.
8. Use the peer comparison as a cross-check on the cash/trust analysis ([[cash-trust-assessment]]), never as a substitute for it. If the two disagree, the FCFE-based analysis wins.

**Reference data — case companies against their peer groups (2013):**

| Company | Div Yield 2013 | Div Yield Avg 2008-12 | Div Payout 2013 | Div Payout Avg 2008-12 | Comparable Group | Group Div Yield | Group Div Payout |
|---|---|---|---|---|---|---|---|
| Disney | 1.09% | 1.17% | 21.58% | 17.11% | US Entertainment | 0.96% | 22.51% |
| Vale | 6.56% | 4.01% | 113.45% | 37.69% | Global Diversified Mining & Iron Ore (cap > $1bn) | 3.07% | 316.32% |
| Tata Motors | 1.31% | 1.82% | 16.09% | 15.53% | Global Autos (cap > $1bn) | 2.13% | 27.00% |
| Baidu | 0.00% | 0.00% | 0.00% | 0.00% | Global Online Advertising | 0.09% | 8.66% |
| Deutsche Bank | 1.96% | 3.14% | 362.63% | 37.39% | European Banks | 1.96% | 79.32% |

Note Vale's group payout of 316.32%, which shows what happens when a cyclical sector's earnings collapse while dividends persist. Matching that group would be absurd.

*Full peer group table — Disney against US Entertainment (2013, $ millions):*

| Company | Market Cap | Dividends | Dividends + Buybacks | Net Income | FCFE | Div Yield | Div Payout | Cash Return/FCFE |
|---|---|---|---|---|---|---|---|---|
| The Walt Disney Company | 134,256 | 1,324 | 5,411 | 6,136 | 1,503 | 0.99% | 21.58% | 360.01% |
| Twenty-First Century Fox | 79,796 | 415 | 2,477 | 7,097 | 2,408 | 0.52% | 6.78% | 102.87% |
| Time Warner Inc | 63,077 | 1,060 | 4,939 | 3,019 | −4,729 | 1.68% | 27.08% | NA |
| Viacom, Inc. | 38,974 | 555 | 5,219 | 2,395 | −2,219 | 1.42% | 23.17% | NA |
| The Madison Square Garden Co. | 4,426 | 0 | 0 | 142 | −119 | 0.00% | 0.00% | NA |
| Lions Gate Entertainment Corp | 4,367 | 0 | 0 | 232 | −697 | 0.00% | 0.00% | NA |
| Live Nation Entertainment | 3,894 | 0 | 0 | −163 | 288 | 0.00% | NA | 0.00% |
| Cinemark Holdings Inc | 3,844 | 101 | 101 | 169 | −180 | 2.64% | 63.04% | NA |
| MGM Holdings Inc | 3,673 | 0 | 59 | 129 | 536 | 0.00% | 0.00% | 11.00% |
| Regal Entertainment Group | 3,013 | 132 | 132 | 145 | −18 | 4.39% | 77.31% | NA |
| DreamWorks Animation SKG | 2,975 | 0 | 34 | −36 | −572 | 0.00% | NA | NA |
| AMC Entertainment Holdings | 2,001 | 0 | 0 | 63 | −52 | 0.00% | 0.00% | NA |
| World Wrestling Entertainment | 1,245 | 36 | 36 | 31 | −27 | 2.88% | 317.70% | NA |
| SFX Entertainment Inc. | 1,047 | 0 | 0 | −16 | −137 | 0.00% | NA | NA |
| Carmike Cinemas Inc. | 642 | 0 | 0 | 96 | 64 | 0.00% | 0.00% | 0.27% |
| Rentrak Corporation | 454 | 0 | 0 | −23 | −13 | 0.00% | NA | NA |
| Reading International, Inc. | 177 | 0 | 0 | −1 | 15 | 0.00% | 0.00% | 0.00% |
| **Average** | 20,462 | 213 | 1,083 | 1,142 | **−232** | 0.85% | 41.28% | 79.02% |
| **Median** | 3,673 | **0** | 34 | 129 | **−27** | **0.00%** | 6.78% | 5.63% |

**Worked example — Disney against US Entertainment, 2013:** Disney's dividend yield of 0.99% sits just above the group average of 0.85% and far above the median of 0.00%. Its payout of 21.58% is below the group average of 41.28% but well above the median of 6.78%. On dividends alone, Disney looks roughly typical or slightly generous — and this conclusion is nearly useless, because the median peer pays nothing at all and the group average is driven by four large firms.

The informative number is the last column. Disney returned **360.01%** of its FCFE ($5,411M of dividends and buybacks against FCFE of $1,503M), against a group average of 79.02% and a median of 5.63%. Note also that the group's average FCFE is **negative** (−$232M) and the median is negative (−$27M), so most of these firms could not afford any payout at all. A recommendation of the form "Disney should match its peer group" is meaningless here. The FCFE-based analysis is doing all the real work.

**Determinism:**
- DETERMINISTIC: every ratio in the tables. Given peer-level market cap, dividends, buybacks, net income and FCFE, a script produces yields, payouts, cash-return-to-FCFE, and the group average and median.
- JUDGMENT: defining the peer group — sector boundaries, geographic scope, size filters, and whether to include loss-makers. Deciding whether the group is a sensible benchmark at all. Deciding whether a gap against peers reflects a policy error or a genuine business difference. Whether to use the average or the median.

**Pitfalls:**
- Comparing dividends only, at a firm or in a sector where buybacks are large. Disney's dividend payout says one thing and its cash return says the opposite.
- Using the group average where most firms pay nothing. The median is zero, and the average is a small-sample artifact.
- Matching a group whose own FCFE is negative. US Entertainment's average FCFE was −$232M in 2013.
- Accepting a group payout ratio like Vale's 316.32% as a target. Sector earnings collapses produce nonsense denominators.
- Letting peer-group choice do the work. Changing the size filter or the geographic scope can move the group yield by a factor of two.
- Confusing "comparable to peers" with "right". Peer matching is the mechanism of me-too-ism, and it propagates sector-wide errors (see [[dividend-empirical-facts]]).
- Treating NA entries as zero. FCFE ≤ 0 makes the cash-return ratio meaningless; excluding those firms changes the group statistics.

**Sources:**
- corporate_finance--lecture_slides--cfpacket2spr20 p.190
- corporate_finance--lecture_slides--cfpacket2spr20 p.220-221

**Related:** [[cash-trust-assessment]], [[market-regression-payout-prediction]], [[dividend-payout-and-yield-measures]], [[cash-returned-dividends-and-buybacks]], [[fcfe-potential-dividends]], [[dividend-empirical-facts]]
