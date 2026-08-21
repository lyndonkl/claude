# The bid-ask spread approach to illiquidity

**Core idea:** Illiquidity is not binary. Every traded asset is somewhat illiquid, and the market already prices that: the bid-ask spread is the gap between what you can buy at and what you can sell at *at the same instant*. That makes the spread an observable cost of illiquidity for public firms. Regress the spread, as a percent of price, on characteristics that can be measured for private firms too — revenues, profitability, cash holdings, trading volume — and you have a function you can evaluate for a private company by setting its trading volume to zero. The predicted spread becomes the illiquidity discount. The appeal is that it is firm-specific and drawn from a large unbiased sample, unlike the restricted-stock and pre-IPO studies. The result is also much smaller: 12.88% for the restaurant against 25–28.75% from the rules of thumb.

**Formulas:**
- `Spread = 0.145 − 0.0022 × ln(Annual revenues) − 0.015 × DERN − 0.016 × (Cash / Firm value) − 0.11 × (Monthly dollar trading volume / Firm value)`
- Symbols:
  - `Annual revenues` in $ millions (the logarithm requires revenues > 0)
  - `DERN` = 1 if earnings are positive, 0 if negative
  - `Cash / Firm value` = cash as a fraction of firm value, entered as a decimal
  - `Monthly dollar trading volume / Firm value` = **0 for a private firm**, by construction
- `Illiquidity discount = Spread`, and `Final equity value = Equity value × (1 − Spread)`
- The regression was estimated on data from the end of 2000.

**Procedure:**
1. Value the firm and get to an equity value before any discount.
2. Collect the four inputs: annual revenues in $ millions; whether earnings are positive; cash as a fraction of firm value; trading volume as a fraction of firm value.
3. Set trading volume to zero. That is the whole point — a private firm has no trading.
4. Evaluate the regression. Every term is a subtraction from the 14.5% intercept, so bigger, profitable, cash-rich firms get smaller discounts.
5. Clamp the result at zero if it ever goes negative. In theory revenues above roughly `e^59` would push it below zero; in practice it never happens.
6. Apply the discount to the equity value.
7. Cross-check against the Silber-based route. If the two disagree by more than a few percentage points, say why you prefer one.

**Reference data — coefficient signs and what they mean:**

| Term | Coefficient | Effect on the discount |
|---|---|---|
| Intercept | +0.145 | Base spread of 14.5% |
| ln(Revenues) | −0.0022 | Larger firms are more liquid; each e-fold of revenue cuts 0.22 points |
| DERN (positive earnings) | −0.015 | Profitability cuts 1.5 percentage points |
| Cash / Firm value | −0.016 | A firm that is all cash is 1.6 points more liquid |
| Trading volume / Firm value | −0.11 | The dominant term for public firms; zero for private ones |

Sensitivity, holding DERN = 1, cash/value = 0.05, volume = 0:

| Revenues ($M) | Predicted discount |
|---|---|
| 1.2 | 12.88% |
| 10 | 12.42% |
| 100 | 11.92% |
| 209 | 11.78% |
| 1,000 | 11.42% |

**Worked example — the restaurant.** Revenues $1.2M, positive earnings, cash 5% of firm value, no trading:
`0.145 − 0.0022 × ln(1.2) − 0.015 × 1 − 0.016 × 0.05 − 0.11 × 0`
`= 0.145 − 0.000401 − 0.015 − 0.0008 − 0 = 0.12880`, i.e. **12.88%**.
Applied to the $520,990 equity value: `0.521 × (1 − 0.1288) = $0.454 million`. Compare $0.391M from a flat 25% and $0.371M from the Silber-refined 28.75%.

**Worked example — the spreadsheet's own case** (`liqdisc.xls`, "Bid-Ask Spread" sheet): revenues $209M, DERN = 1, cash/value 3%, volume 0.
`0.145 − 0.0022 × ln(209) − 0.015 − 0.016 × 0.03 = 0.145 − 0.011753 − 0.015 − 0.00048 = 0.117767`, i.e. **11.78%**.

**Determinism:**
- DETERMINISTIC: `{revenues, earnings dummy, cash/firm value, trading volume} → spread → discount → discounted equity value`. This is a closed-form function and a script computes it exactly.
- JUDGMENT: whether the spread of a thinly traded public stock is the right analogue for a wholly untraded business; whether the end-of-2000 coefficients still apply; and whether to overlay the company/time/buyer adjustments the regression cannot see. That judgment needs the current market's liquidity conditions and the buyer's holding horizon.

**Pitfalls:**
- Leaving trading volume at a non-zero value. It carries the largest coefficient and will collapse the discount.
- Entering revenues in dollars rather than $ millions. The logarithm makes the scale error silent but real.
- Entering revenues of zero or negative. The logarithm is undefined; raise an error rather than substituting.
- Treating an 11–13% answer as automatically right because it is model-based. The regression's coefficients are dated (end of 2000) and the extrapolation from "thinly traded public stock" to "no market at all" is exactly the leap being asserted.
- Assuming the low answer is conservative. It is *less* conservative than the rules of thumb, and a seller will prefer it while a buyer will not.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket2spr21 p.148-149, p.152
- valuations--lecture_notes--spring_2020--valpacket2spr20 p.146-147, p.150
- special-private.md — liqdisc.xls, sheet "Bid-Ask Spread"

**Related:** [[illiquidity-discount]], [[silber-restricted-stock-regression]], [[private-to-private-valuation]], [[private-to-public-sale]], [[minority-discount]]
