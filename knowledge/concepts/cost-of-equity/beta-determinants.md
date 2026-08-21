# Determinants of beta: product type, operating leverage, financial leverage

**Core idea:** Beta is not an arbitrary statistical artifact. Three real business characteristics drive it. First, the **type of product or service** — the more discretionary the purchase, the more demand swings with the economy, and the higher the beta. Second, **operating leverage** — the higher the share of fixed costs, the more earnings amplify revenue swings, and the higher the beta. Third, **financial leverage** — debt creates fixed interest payments that make equity earnings more volatile, raising the equity beta. The first two determine the unlevered (business/asset) beta; the third levers it up. This is why you can sanity-check a beta against the business, and why a beta estimated for a business travels across geography.

**Formulas:**
- Equity (levered) beta = Unlevered beta × (1 + (1 − t) × D/E), with t = marginal tax rate and D/E = market-value debt-to-equity ratio.
- Operating-leverage decomposition: Unlevered beta = Pure business beta × (1 + Fixed costs / Variable costs).
- Operating leverage measure 1 (direct): Fixed Costs Measure = Fixed costs / Variable costs.
- Operating leverage measure 2 (from reported data): **EBIT Variability Measure = % change in EBIT / % change in Revenues**, averaged over a long window.

**Procedure:**
1. Classify the **product**. Higher beta is expected for: cyclical over non-cyclical firms; luxury over basic goods; high-priced over low-priced goods and services; growth over mature firms. Discretionary-ness is context-dependent — phone service is near-necessary in the US and Western Europe, but a luxury for large population segments in parts of Asia and Latin America, so emerging-market telecoms should carry higher betas against their local markets.
2. Measure **operating leverage**. The fixed/variable split is rarely observable from outside, so use the EBIT-variability measure: average the annual % change in EBIT and the annual % change in revenues over a long window, then divide. Higher ratio means higher operating leverage means higher beta. Expect higher operating leverage from firms with heavy infrastructure needs and rigid cost structures, from smaller firms, and from young firms.
3. Compare the firm's operating leverage to its sector's. If it is below the industry average, expect a lower unlevered beta than peers, other things equal.
4. In practice, accept that the fixed/variable split is usually unobtainable per firm, so **assume firms within a business have similar operating leverage** and apply one sector unlevered beta to all of them. Adjust only when you have hard evidence of a different cost structure.
5. Apply **financial leverage** last, using the firm's own market D/E — see [[levering-and-unlevering-beta]].
6. Use the determinants as a plausibility check on any estimated beta. A gold miner with a beta near zero or negative is plausible (gold moves against the market). A defensive staples firm with a beta of 2 is not.

**Reference data:**

Expected direction of each determinant:

| Determinant | Higher beta | Lower beta |
|---|---|---|
| Product type | Cyclical; luxury; high-priced; discretionary; growth | Non-cyclical; basic goods; low-priced; necessity; mature |
| Operating leverage | High fixed costs; heavy infrastructure; rigid cost structure; small; young | Flexible cost structure; large; mature |
| Financial leverage | High D/E | Low D/E |

Illustrative company betas showing the ladder:

| Company | Beta | Reading |
|---|---|---|
| Bulgari | 2.45 | Highly discretionary luxury |
| Qwest Communications | 1.85 | Telecom, high fixed costs |
| Microsoft | 1.25 | Technology |
| General Electric | 1.15 | Broad industrial |
| Exxon Mobil | 0.70 | Integrated energy |
| Altria (Philip Morris) | 0.60 | Consumer staple |
| Harmony Gold Mining | −0.15 | Gold moves against the market |

Disney operating leverage from the EBIT-variability measure (annual data):

| Window | Avg % change in sales | Avg % change in EBIT | Operating leverage |
|---|---|---|---|
| 1987-2013 | 11.79% | 11.91% | 11.91/11.79 = **1.01** |
| 1996-2013 | 8.16% | 10.20% | 10.20/8.16 = **1.25** |
| Entertainment industry average | | | **1.35** |

Disney sits below the industry average on both windows, so — other things equal — you would expect Disney to carry a *lower* beta than other entertainment companies.

Leverage effect on Disney's beta, relevering an unlevered beta of 1.11 at a 36.1% tax rate:

| Debt to capital | D/E ratio | Levered beta | Effect of leverage |
|---|---|---|---|
| 0% | 0.00% | 1.11 | 0.00 |
| 10% | 11.11% | 1.19 | 0.08 |
| 20% | 25.00% | 1.29 | 0.18 |
| 30% | 42.86% | 1.42 | 0.30 |
| 40% | 66.67% | 1.59 | 0.47 |
| 50% | 100.00% | 1.82 | 0.71 |
| 60% | 150.00% | 2.18 | 1.07 |
| 70% | 233.33% | 2.77 | 1.66 |
| 80% | 400.00% | 3.95 | 2.84 |
| 90% | 900.00% | 7.51 | 6.39 |

The effect is strongly convex — the last 10 percentage points of leverage add more beta than the first 50.

**Worked example (Disney operating leverage, 1996-2013):** Average annual revenue growth 8.16%; average annual EBIT growth 10.20%. Operating leverage = 10.20 / 8.16 = **1.25**. Against an entertainment-industry average of 1.35, Disney's cost structure is somewhat more flexible than its peers', which argues for a slightly lower unlevered beta than the peer median — a qualitative adjustment to step 2 of the bottom-up beta procedure.

**Determinism:**
- DETERMINISTIC: (sales history, EBIT history) → % changes → averages → EBIT-variability operating leverage; (fixed costs, variable costs) → fixed-cost measure; (unlevered beta, tax rate, D/E) → levered beta at any leverage level.
- JUDGMENT: classifying a product as discretionary or not, and in which market; whether an observed operating-leverage difference is real or an artifact of the window chosen; whether to override a sector unlevered beta for a specific firm; whether a negative beta is genuine.

**Pitfalls:**
- Assuming discretionary-ness is a global property of a product. The same service can be a necessity in one market and a luxury in another.
- Computing operating leverage over a window containing a restructuring or a huge acquisition, which contaminates both the sales and EBIT growth series.
- Adjusting an unlevered beta for operating leverage without any data on the fixed/variable split. Absent evidence, use the sector beta.
- Double-counting leverage: applying an operating-leverage adjustment to a comparable-firm beta that was already unlevered from firms with the same cost structure.
- Managing the business to lower beta. Every lever — making products less discretionary, cutting fixed costs, cutting debt — is a real change to the business. A high-beta firm with good projects beats a low-beta firm with bad ones.
- Forgetting the convexity of the leverage effect when stress-testing a highly levered firm.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.90-92
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.88, p.90
- corporate_finance--lecture_slides--cfpacket1spr20 p.148, p.152-157, p.160

**Related:** [[levering-and-unlevering-beta]], [[bottom-up-beta]], [[regression-beta]], [[capm-cost-of-equity]], [[optimal-capital-structure]], [[operating-leverage-and-breakeven]]
