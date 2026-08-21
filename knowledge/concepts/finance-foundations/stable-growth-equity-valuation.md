# Stable-Growth Equity Valuation: Dividends versus FCFE

**Core idea:** For a mature company growing at a constant rate forever, equity value collapses to a single line: next year's cash flow to equity divided by the cost of equity minus the growth rate. The open question is which cash flow to put in the numerator. Dividends are the only cash flow that equity investors in a public firm actually receive, and the earliest valuation models were built on them. But dividends are what management *chose* to pay, not necessarily what the firm *could* pay. Free cash flow to equity measures potential dividends: what is left after operating expenses, interest expenses, net debt payments, and reinvestment needs. Using dividends implicitly assumes the firm pays out what it can afford. When FCFE and dividends differ, the two models give different values, and the gap is informative.

**Formulas:**
- Dividend discount model, stable growth (Gordon growth): `Value per share = DPS₀ × (1 + g) / (r − g)`. `DPS₀` = current dividends per share; `g` = perpetual growth rate of dividends; `r` = cost of equity. Requires `r > g` and genuinely stable growth.
- FCFE version: `Value per share = FCFE₀ × (1 + g) / (r − g)`, with FCFE replacing dividends and the same symbols otherwise.
- FCFE definition: `FCFE = Cash flow after operating expenses, interest expenses, net debt payments, and reinvestment needs`, where `Net debt payments = Repayments of old debt − New debt issued`. If new debt issued exceeds repayments, FCFE is higher.
- Payout check: `Payout ratio = DPS / EPS`. Compare with `DPS / FCFE per share` to see whether the firm is paying out more or less than it can afford.
- Over/undervaluation rule: if intrinsic value per share is below the market price, the stock is overvalued; if above, undervalued.

**Procedure:**
1. Confirm the firm is actually in stable growth before using a single-stage model. A stable-growth firm has a growth rate at or below the growth rate of the economy it operates in, and no prospect of a high-growth phase. The perpetual growth rate is bounded by the riskfree rate in that currency.
2. Estimate the cost of equity for the marginal investor, in the currency of the cash flows.
3. Compute both cash flow measures for the most recent period: dividends per share, and FCFE per share.
4. Compare them. If FCFE materially exceeds dividends, the firm is paying out less than it can afford, and the dividend model will understate value. If dividends exceed FCFE, the firm is paying out more than it can afford — often funded by debt — and the dividend model will overstate value and is unsustainable.
5. Choose the numerator deliberately. Use dividends when the firm has a credible, stable payout policy. Use FCFE when payout and capacity diverge, and say which you used.
6. Grow the base cash flow one period, then divide by `(r − g)`.
7. Compare with the market price to reach a view. State the value and the price together; a valuation without a comparison is not a recommendation.
8. Stress-test `g` and `r`. In a stable-growth model, value is extremely sensitive to the `(r − g)` denominator. A 1-point change in either input moves value by a large multiple of that.

**Reference data:**

| Cash flow measure | What it is | When it is the right numerator |
|---|---|---|
| Dividends per share | The only cash flow equity investors actually receive from the firm | Mature firms with credible, stable payout policies |
| FCFE per share | Potential dividends: cash left after operating expenses, interest, net debt payments, and reinvestment | Whenever payout diverges from capacity |

| Con Ed inputs, 2016 (Damodaran, Foundations of Finance Session 8) | Value |
|---|---|
| Dividends per share, 2016 | $4.00 |
| Payout ratio | about 70% of that year's EPS |
| FCFE per share, trailing twelve months | $4.25 |
| Perpetual growth rate `g` | 2% |
| Cost of equity `r` | 8% |
| Market price | $70.00 |

**Worked example:** Consolidated Edison, the New York City utility, in 2016. It paid $4.00 per share in dividends, roughly 70% of that year's earnings per share. As a mature regulated utility it was expected to grow 2% a year in perpetuity, with dividends following. Its cost of equity was 8%.

Dividend model: `Value per share = $4.00 × 1.02 / (0.08 − 0.02) = $4.08 / 0.06 = $68.00`. Against a market price of $70, the stock looks slightly overvalued.

FCFE model: FCFE was $4.25 per share over the trailing twelve months, more than the $4.00 paid out. `Value per share = $4.25 × 1.02 / (0.08 − 0.02) = $4.335 / 0.06 = $72.25`. Against the same $70 price, the stock now looks slightly undervalued.

The two models disagree on the recommendation, and the entire disagreement comes from a 25-cent gap between what Con Ed paid and what it could have paid. That is the practical reason to compute both.

**Determinism:**
- DETERMINISTIC: the value per share, given `DPS₀` or `FCFE₀`, `g`, and `r`. The payout ratio. The comparison against market price. FCFE itself, given operating cash flow, interest expense, new debt issued, debt repaid, and reinvestment.
- JUDGMENT: whether the firm is truly in stable growth. The perpetual growth rate `g`. The cost of equity `r`. Whether dividends or FCFE is the right numerator. Whether the trailing FCFE is representative or distorted by a one-off in reinvestment or debt issuance. These need several years of financial statements, the firm's stated payout policy, its regulatory environment, and the long-run growth rate of its economy.

**Pitfalls:**
- Applying a single-stage stable-growth model to a firm that still has a high-growth phase ahead. The model will badly understate value.
- Setting `g` above the riskfree rate or above the economy's growth rate. A firm cannot outgrow its economy forever.
- Letting `g` approach `r`. The denominator collapses and value explodes toward infinity, which signals an impossible assumption rather than a valuable firm.
- Using the *current* cash flow in the numerator without growing it one period.
- Assuming dividends equal capacity. They often do not, and the direction of the error depends on which way the gap runs.
- Reading a $68 value against a $70 price as a confident sell. The gap is well inside the noise of the `g` and `r` estimates.
- Comparing an FCFE-based value with a dividend-based value from another analyst without noting the difference in numerator.

**Sources:**
- `foundations_of_finance--valuing_equity p.4, p.6-7`

**Related:** [[equity-vs-firm-valuation]], [[cost-of-capital]], [[present-value-of-the-five-cash-flow-types]], [[marginal-investor-and-beta]], [[terminal-value]], [[fcff-vs-fcfe]]
