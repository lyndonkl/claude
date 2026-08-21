# Intrinsic PE: the fundamentals behind the price-earnings ratio

**Core idea:** The PE ratio is not a free-standing number. Divide an equity DCF by earnings per share and PE falls out as a function of three things: how much of earnings the firm can pay out, how fast earnings grow, and how risky the equity is. PE rises with payout and with growth. It falls with the cost of equity. Both relationships are steeply non-linear. Growth is worth far more when interest rates are low. Risk hurts high-growth firms much more than low-growth firms. Those two facts explain most cross-sectional and time-series PE puzzles, including why a "high" PE can be perfectly justified in a low-rate market.

**Formulas:**

Stable growth (Gordon form), dividing the DDM by current EPS:
- `P₀ = DPS₁/(r − gn)`
- `PE = P₀/EPS₀ = Payout Ratio × (1 + gn)/(r − gn)`
- FCFE version: `P₀ = FCFE₁/(r − gn)` and `PE = (FCFE/Earnings) × (1 + gn)/(r − gn)`
- Forward PE form (next year's EPS in the denominator): `PE₁ = Payout Ratio/(r − gn)`

Two-stage (high growth g for n years, then stable gn forever):
```
P₀ = EPS₀ × Payout × (1+g) × [1 − (1+g)^n/(1+r)^n]/(r − g)
   + EPS₀ × Payout_n × (1+g)^n × (1+gn)/[(r − gn)(1+r)^n]

PE = P₀/EPS₀ = Payout × (1+g) × [1 − (1+g)^n/(1+r)^n]/(r − g)
   + Payout_n × (1+g)^n × (1+gn)/[(r − gn)(1+r)^n]
```

Cost of equity from CAPM: `r = riskfree rate + beta × equity risk premium`.

Symbols:
- P₀ = price today; EPS₀ = current earnings per share.
- DPS₁ = expected dividends per share next year.
- Payout = dividend payout ratio during high growth; Payout_n = payout in stable growth.
- g = high-growth EPS growth rate; gn = stable growth rate; n = years of high growth.
- r = cost of equity; FCFE = free cash flow to equity.

**Procedure:**
1. Choose the PE variant and stay with it: current PE (last fiscal year EPS), trailing PE (last 12 months), or forward PE (next year forecast).
2. Decide whether the firm is in stable growth or has a finite high-growth phase. Stable → use the Gordon form. Otherwise → use the two-stage form with an explicit n.
3. Estimate the payout ratio. If the firm does not pay out what it can afford, substitute FCFE/Earnings for the payout ratio. Set the stable-phase payout consistently with stable growth: `Payout_n = 1 − gn/ROE_stable`.
4. Estimate the cost of equity from CAPM with the firm's beta.
5. Compute the intrinsic PE. Compare it with the traded PE. Traded PE below intrinsic PE means cheap, given those fundamentals.
6. Before comparing two firms' PEs, check both the growth gap and the risk gap. A higher-growth firm deserves a higher PE, but a higher-beta firm deserves a lower one, and the risk penalty grows with growth.
7. When the market's PE level looks extreme, check the interest-rate environment before concluding anything ([[market-pe-vs-bond-alternative]]).

**Reference data (sensitivity of the two-stage intrinsic PE; base case: g for 5 years, then 8% forever, payout 20% then 50%):**

PE against expected growth, by required return r:

| Expected growth | r = 4% | r = 6% | r = 8% | r = 10% |
|---|---|---|---|---|
| 5% | ~30 | ~20 | ~13 | ~9 |
| 25% | ~85 | ~50 | ~33 | ~20 |
| 50% | ~175 | ~95 | ~55 | ~28 |

(Values read from the lecture chart; the shape is the lesson — PE rises non-linearly with growth, and the slope is far steeper at low required returns.)

PE against beta, by growth rate (riskfree 6%, ERP 5.5%):

| Beta | g = 25% | g = 20% | g = 15% | g = 8% |
|---|---|---|---|---|
| 0.75 | ~49 | ~38 | ~29 | ~19 |
| 1.00 | ~29 | ~23 | ~18 | ~13 |
| 1.50 | ~14 | ~12 | ~10 | ~8 |
| 2.00 | ~9.5 | ~8.5 | ~7.5 | ~6 |

The spread between growth scenarios collapses as beta rises. Growth is worth much less inside a risky firm.

**Worked example (lecture case, identical in both editions):** High-growth phase: growth 25%, payout 20%, beta 1.00, 5 years. Stable phase: growth 8%, payout 50%, beta 1.00. Riskfree rate 6%, equity risk premium 5.5%, so r = 6% + 1.00 × 5.5% = 11.5%.

```
PE = 0.20 × 1.25 × [1 − 1.25^5/1.115^5]/(0.115 − 0.25)
   + 0.50 × 1.25^5 × 1.08/[(0.115 − 0.08) × 1.115^5]
   = 28.75
```
Intrinsic PE = 28.75. Note the first term has a negative denominator (r < g); the bracket is also negative, so the term is positive. That is normal in the two-stage formula and not an error.

**Determinism:** DETERMINISTIC — given payout ratios, g, gn, n, beta, riskfree rate and equity risk premium, the intrinsic PE is a closed-form number a script can compute. Also deterministic: the whole sensitivity grid. JUDGMENT — the length of the high-growth period, whether payout or FCFE/earnings is the right cash-flow measure, the beta estimate, and the reading of what a gap between actual and intrinsic PE means.

**Pitfalls:**
- Comparing PEs computed on different earnings bases (current vs. trailing vs. forward).
- Treating PE differences as mispricing when they reflect growth or risk differences.
- Ignoring that low interest rates mechanically raise justified PEs; high PEs in a low-rate market are partly a rate effect, not exuberance.
- Assuming risk and growth are separable. The drag from beta is proportionately larger for high-growth firms, so a risky high-growth firm can deserve a lower PE than a safe low-growth firm.
- Using a stable-phase payout that is inconsistent with the stable growth rate and ROE.

**Sources:**
- valpacket2spr21 p.22-26
- valpacket2spr20 p.22-26

**Related:** [[intrinsic-multiple-derivation]], [[peg-ratio]], [[multiple-definition-tests]], [[country-pe-regression]], [[market-pe-vs-bond-alternative]], [[market-wide-regressions]], [[dividend-discount-model]], [[cost-of-equity-capm]], [[stable-growth-assumptions]]
