# Choosing comparables and controlling for differences

**Core idea:** The hard part of pricing is the last step. A comparable firm is not a firm in the same sector. It is a firm with similar risk, growth and cash-flow characteristics, even if it sells something else entirely. Since no two firms match exactly, you must control for the differences that remain. How you control depends on how many dimensions differ: none, one, or several. That choice — direct comparison, story telling, modified multiple, or regression — is the whole application step. Get it wrong and your "mispricing" is just your own uncontrolled comparison.

**Formulas:** none intrinsic to the choice. The controls themselves use the intrinsic-multiple formulas ([[intrinsic-multiple-derivation]]) or regressions ([[sector-regressions]], [[market-wide-regressions]]).

Median test screen (applied to any multiple with a companion variable and a risk measure):
- Undervalued: multiple < sector median AND companion variable (e.g. ROE) > sector median AND risk measure < sector median.
- Overvalued: multiple > sector median AND companion variable < sector median.

**Procedure:**
1. **Set the four pricing-game choices before anything else.**
   - Value measure: equity, firm, or enterprise value? Ask whether this is a financial service business (use equity multiples — debt is raw material, not financing) and whether leverage differs sharply across the peer set.
   - Scalar: revenues, earnings, cash flows or book value? Ask how you are measuring value, whether the scaling number is positive for every firm, and how much accounting choices distort it.
   - Timing and normalization: current, trailing, forward, or a far-forward number? Ask where the firm sits in its life cycle, how cyclical the metric is, and whether forecasts exist.
   - Comparable group: global or local peers, similar size or all firms? Ask how much companies share across borders, whether size changes the economics, how large a sample you need, and how you will control for differences.
2. **Pick a point on the sampling spectrum.** A small sample of firms "just like" yours needs few controls but gives noisy statistics. A large loose sample gives better statistics but demands heavy controls. Both are legitimate; the choice determines step 3.
3. **Choose the control technique by the number of differing dimensions.**
   - None (true twins): direct comparison. Higher multiple = expensive, lower = cheap.
   - One dimension: story telling, or a modified multiple that folds the dimension in (PEG is the standard example — and a flawed one, see [[peg-ratio]]).
   - Several dimensions: statistical controls — sector or market regressions.
4. **Story telling, done honestly.** State the story as a claim about fundamentals: "this company trades at 12x earnings versus 10x for the sector, but it is cheap because its growth is much higher." Then check the claim against the data for every firm in the table, not just the one you like.
5. **Median test, as a quick screen.** Compute sector medians for the multiple, its companion variable, and a risk measure. Apply the two rules above. Treat it as a screen, not a verdict — it ignores the size of each gap and the correlations among variables.
6. **Escalate to regression whenever more than one fundamental differs.** That is the normal case.
7. **State the conclusion relative to the chosen benchmark.** Peer-group pricing and market-wide pricing can disagree, because the peer group may itself be mispriced relative to the market.

**Reference data:**

Beverage companies — the story-telling data set (trailing PE, expected growth, standard deviation):

| Company | Trailing PE | Expected growth | Std deviation |
|---|---|---|---|
| Coca-Cola Bottling | 29.18 | 9.50% | 20.58% |
| Molson Inc. Ltd. 'A' | 43.65 | 15.50% | 21.88% |
| Anheuser-Busch | 24.31 | 11.00% | 22.92% |
| Corby Distilleries | 16.24 | 7.50% | 23.66% |
| Chalone Wine Group | 21.76 | 14.00% | 24.08% |
| Andres Wines Ltd. 'A' | 8.96 | 3.50% | 24.70% |
| Todhunter Int'l | 8.94 | 3.00% | 25.74% |
| Brown-Forman 'B' | 10.07 | 11.50% | 29.43% |
| Coors (Adolph) 'B' | 23.02 | 10.00% | 29.52% |
| PepsiCo | 33.00 | 10.50% | 31.35% |
| Coca-Cola | 44.33 | 19.00% | 35.51% |
| Boston Beer 'A' | 10.59 | 17.13% | 39.58% |
| Whitman Corp. | 25.19 | 11.50% | 44.26% |
| Mondavi (Robert) 'A' | 16.47 | 14.00% | 45.84% |
| Coca-Cola Enterprises | 37.14 | 27.00% | 51.34% |
| Hansen Natural | 9.70 | 17.00% | 62.45% |

European banks, 2010 — the median-test data set. Sector medians: PBV 2.07, ROE 11.82%, standard deviation 21.93%. (Full firm-level table in [[book-value-multiples]].)

**Worked example — story telling and the median test:**
An analyst claims Andres Wines (PE 8.96) and Hansen Natural (PE 9.70) are undervalued because their PEs are the lowest in the beverage sector. Check the fundamentals. Andres Wines has expected growth of 3.5%, the lowest but one in the table. Hansen Natural has a standard deviation of 62.45%, the highest in the table by a wide margin. Low growth explains the first low PE; high risk explains the second. Neither is evidence of mispricing.

Now the median test on the bank sample. Unicredito Italiano: PBV 2.30 (above the 2.07 median), ROE 14.86% (above the 11.82% median), std deviation 13.79% (below the 21.93% median). It fails the undervalued screen on PBV alone, yet it has above-median returns with below-median risk. This is exactly where the median test runs out and a regression is needed.

**Determinism:** DETERMINISTIC — computing sector medians and applying the median-test rules; computing every firm's multiple and companion variable. JUDGMENT — defining the comparable universe, choosing the value measure, scalar and timing, deciding how many dimensions really differ, and constructing the story that links a fundamental to a multiple gap.

**Pitfalls:**
- Equating sector membership with comparability. Theory says comparables share fundamentals, not SIC codes.
- Telling a story that fits one firm and ignoring the rest of the table.
- Using a modified multiple (PEG) and believing the dimension is now neutralized.
- Applying the median test when firms differ on several dimensions at once; it treats each variable independently.
- Using an earnings or book scalar that is negative for part of the sample, silently dropping those firms.
- Forgetting that leverage differences make equity multiples incomparable, and that financial service firms need equity multiples in the first place.
- Reporting a peer-relative verdict as though it were absolute ([[pricing-vs-value]]).

**Sources:**
- valpacket2spr21 p.52-56, p.60-61, p.100
- valpacket2spr20 p.52-56, p.60-61, p.98

**Related:** [[pricing-vs-value]], [[four-step-multiple-framework]], [[sector-regressions]], [[market-wide-regressions]], [[peg-ratio]], [[book-value-multiples]], [[multiple-distribution-statistics]], [[pricing-young-companies]], [[industry-average-multiples]]
