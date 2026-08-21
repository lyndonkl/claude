# Market regression approach to predicting payout

**Core idea:** Instead of comparing a firm with a hand-picked peer group, regress dividend payout and dividend yield against fundamentals across the entire market. The fitted equation then predicts what any firm "should" pay given its risk, growth and leverage, controlling for the differences that make raw peer averages misleading. The regressions confirm the intuition: lower beta, lower expected growth and higher debt ratios all go with higher payout and yield. The comparison of actual against predicted gives a quick, market-wide verdict on whether a firm pays too much or too little in dividends. The technique's fatal limitation is that it is estimated on dividends alone, so it misclassifies any firm that returns cash through buybacks.

**Formulas:**

*US market regressions (all US companies, January 2014; t-statistics in parentheses):*

**PYT = 0.649 − 0.296 × BETA − 0.800 × EGR + 0.300 × DCAP**  (R² = 19.6%)
t-stats: 32.16, 15.40, 8.90, 7.33

**YLD = 0.0324 − 0.0154 × BETA − 0.038 × EGR + 0.023 × DCAP**  (R² = 25.8%)
t-stats: 38.81, 19.41, 13.25, 13.45

Symbols:
- PYT = dividend payout ratio = Dividends / Net Income (expressed as a decimal)
- YLD = dividend yield = Dividends / Current Price (expressed as a decimal)
- BETA = the company's beta, regression or bottom-up
- EGR = expected growth rate in earnings over the next 5 years, as a decimal (analyst estimates)
- DCAP = Total Debt / (Total Debt + Market Value of Equity), as a decimal

*Comparison metric:*
Payout gap = Actual PYT − Predicted PYT; Yield gap = Actual YLD − Predicted YLD. A negative gap means the firm pays less in dividends than the market's fundamentals-based norm.

**Procedure:**
1. Estimate the three inputs for the firm: beta (prefer a bottom-up beta), the expected 5-year earnings growth rate (analyst consensus), and the market debt-to-capital ratio. Use decimals, not percentages, in the equations.
2. Plug into both equations to get predicted payout and predicted yield.
3. Compute the gaps against the firm's actual payout and yield.
4. Apply the decision rule: if actual is materially below predicted, the firm pays too little in dividends relative to the market; if above, too much.
5. **Then check buybacks.** This is not optional. The regressions are fitted on dividends only. A firm returning large amounts through repurchases will show a large negative gap and be wrongly labeled a cash hoarder.
6. Weigh the R². At roughly 20–26%, these regressions explain a minority of the cross-sectional variation, so treat the prediction as a rough central tendency, not a target. A gap of a few percentage points is noise.
7. Re-estimate the regression on current data if you can. The coefficients shift with the market environment, and the January 2014 fit is a snapshot.
8. Use this as a cross-check on the cash/trust analysis ([[cash-trust-assessment]]), which uses firm-specific cash flows and is the primary tool.

**Reference data:**

| Equation | Constant | BETA | EGR | DCAP | R² |
|---|---|---|---|---|---|
| Payout (PYT) | 0.649 | −0.296 | −0.800 | +0.300 | 19.6% |
| Yield (YLD) | 0.0324 | −0.0154 | −0.038 | +0.023 | 25.8% |

Interpretation of the signs, which is the durable content of the regressions:
- **Beta negative.** Riskier firms pay out less; committing to a dividend when cash flows are volatile is dangerous.
- **Expected growth negative.** High-growth firms need their cash — the life-cycle result in regression form (see [[dividend-life-cycle]]).
- **Debt ratio positive.** More levered firms pay higher dividends and yields in the data.

**Worked example — Disney, January 2014:**
Inputs: bottom-up beta = 1.00; expected EPS growth (analyst estimate) = 14.73% → EGR = 0.1473; market debt-to-capital = 11.58% → DCAP = 0.1158.

Predicted payout:
PYT = 0.649 − 0.296 × (1.00) − 0.800 × (0.1473) + 0.300 × (0.1158)
= 0.649 − 0.296 − 0.11784 + 0.03474 = **0.2695 → 26.95%**

Predicted yield:
YLD = 0.0324 − 0.0154 × (1.00) − 0.038 × (0.1473) + 0.023 × (0.1158)
= 0.0324 − 0.0154 − 0.005597 + 0.002663 = **0.0140 → 1.40%**

Actual: dividend yield 1.09%, dividend payout about 21.58%. Both sit below the prediction, so the regression's verdict is that Disney pays too little in dividends.

That verdict is wrong, and the reason is instructive. In the same year Disney returned $4,087M through buybacks against $1,324M of dividends. Its total cash returned was $5,411M against FCFE of $1,503M — 360% of FCFE. A dividend-only regression labels a firm returning three and a half times its FCFE as a firm that pays too little. Always adjust for buybacks before acting on the gap.

**Determinism:**
- DETERMINISTIC: the predicted payout and yield, given beta, EGR and DCAP. The gap against actuals. Re-estimating the regression itself from a cross-section of firms is also deterministic given the data.
- JUDGMENT: estimating the inputs — which beta (bottom-up or regression), which growth forecast, and how to treat debt (book or market, including or excluding leases). Deciding whether the gap is meaningful given the low R². Interpreting the gap once buybacks are added back. Deciding whether the coefficient vintage still applies.

**Pitfalls:**
- Acting on the gap without adjusting for buybacks. This is the error the Disney example is designed to expose.
- Entering percentages instead of decimals. EGR = 14.73 instead of 0.1473 makes the prediction absurd.
- Treating the fitted value as a target rather than a central tendency. With R² near 20%, most of the variation is unexplained.
- Using stale coefficients without noting the estimation date (January 2014 here).
- Applying US-market coefficients to a non-US firm. Payout norms differ enormously by region.
- Applying the regression to financial service firms, where leverage means something different and DCAP is not comparable.
- Using it on a firm with negative or near-zero earnings, where the actual payout ratio is undefined and the gap cannot be computed.

**Sources:**
- corporate_finance--lecture_slides--cfpacket2spr20 p.222-223

**Related:** [[peer-group-payout-analysis]], [[cash-trust-assessment]], [[dividend-payout-and-yield-measures]], [[cash-returned-dividends-and-buybacks]], [[dividend-life-cycle]], [[fcfe-potential-dividends]], [[bottom-up-beta]]
