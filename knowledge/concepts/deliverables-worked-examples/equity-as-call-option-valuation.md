# Equity as a call option (the distressed-firm case)

**Core idea:** In a highly levered firm with negative earnings, equity holders own something closer to an option than a claim on cash flows. They can walk away with limited liability, so their position is a call on the value of the firm's assets, struck at the face value of the debt and expiring when the debt matures. Black-Scholes then values that call. This matters because a DCF on a loss-making, over-levered firm often produces a very low or negative equity value, while the option value can be materially positive — the option captures the chance that asset values recover before the debt comes due. The equity valuation project applies it under a strict, narrow trigger.

**Formulas:**
- Value of equity = S × N(d1) − K × e^(−rT) × N(d2).
  - S = value of the firm's assets (the underlying).
  - K = strike = face value of the outstanding debt obligations.
  - T = weighted average life (duration) of the debt, in years.
  - r = risk-free rate, typically the T-bond rate matched to T.
  - σ² = variance of firm value, built from industry-average standard deviations of stock and bond prices.
  - Dividend yield = 0 unless the firm pays out.
  - d1 = [ln(S/K) + (r + σ²/2)T] / (σ√T); d2 = d1 − σ√T.
- Value of outstanding debt = Firm value − Value of equity as a call.
- Implied (appropriate) interest rate on the risky debt = the yield that discounts the face value to the implied market debt value over T.
- Trigger rule: apply this model only when the negative-earnings firm's **market-value debt-to-capital ratio > 50%**.

**Procedure:**
1. Confirm the trigger. The firm must have negative earnings *and* market-value debt-to-capital above 50%. If leverage is below the threshold, do not use the model.
2. Estimate S, the value of the firm's assets. The DCF firm value is the natural source.
3. Estimate K, the face value of debt obligations, and T, the weighted average debt life.
4. Estimate the variance of firm value. Use industry-average standard deviations of stock and bond prices when the firm's own history is too short or too erratic.
5. Take r as the T-bond rate over the horizon T, and set the dividend yield (zero for a distressed firm).
6. Compute d1, d2, N(d1), N(d2) and the equity value. Divide by shares for value per share.
7. Back out the implied debt value and the implied interest rate on the debt. A very high implied rate is a consistency check on the distress assumption.
8. Carry the option value into the final reconciliation alongside the DCF and relative values. See [[valuation-triangulation-and-recommendation]].

**Reference data:** Nextel Partners Black-Scholes inputs and outputs (equity valuation project, ca. 2003).

| Input | Value |
|---|---|
| S (value of the firm / underlying, as printed) | $9,823 |
| K (strike = face value of debt obligations, as printed) | $92,569.73 |
| T (weighted average debt life) | 6.4 years |
| r (T-bond rate) | 4.4% |
| Variance of firm value | 0.468755 |
| Dividend yield | 0.0% |

| Output | Value |
|---|---|
| d1 | −0.266884801 |
| N(d1) | 0.394778988 |
| d2 | −1.998944408 |
| N(d2) | 0.022807115 |
| Value of equity as a call | $2,283.80 → $9.09 per share |
| Value of outstanding debt (firm value − equity) | $7,539.20 |
| Implied interest rate on the debt | 47.97% |

Supporting inputs from Nextel's DCF: debt ratio 39%, beta 3.93, cost of debt 15.9%, ROC −19.71%, tax rate 0% while losses persist, DCF equity value $1,026m, DCF value per share $11.08, market price $11.72. Variance and standard deviations came from industry averages; the 6.4-year average debt life came from the firm's maturity schedule.

**Worked example:** Nextel Partners provides digital mobile communications under the Nextel brand in mid-sized and tertiary US markets. It has negative earnings and high leverage — exactly the case the trigger is written for. The DCF, an n-stage FCFF model, gives $11.08 per share. The option model gives $9.09 per share: with d1 = −0.2669 and d2 = −1.9989, N(d1) = 0.3948 and N(d2) = 0.0228, so equity is worth $2,283.80 against a firm value of $9,823. The implied value of the debt is $7,539.20 and the implied interest rate on it is 47.97%, which confirms how distressed the debt really is. Both the DCF value and the option value sit below the $11.72 market price, and the final recommendation is SELL.

**Determinism:** DETERMINISTIC — given S, K, T, r, variance and the dividend yield, the Black-Scholes calculation produces d1, d2, N(d1), N(d2), the equity value, the implied debt value and the implied interest rate exactly. The trigger test (market debt-to-capital above 50%) is a mechanical comparison. JUDGMENT — estimating S when the firm is distressed, deciding what counts as the face value and the weighted average life of a mixed debt structure, and choosing the variance source when the firm's own price history is unusable. Whether the option value or the DCF value should dominate the recommendation is also judgment.

**Pitfalls:**
- Applying the model to any loss-making firm. The gate is leverage above 50% market debt-to-capital, not negative earnings alone.
- Using the firm's own equity volatility as the firm-value variance. In a highly levered firm equity volatility far exceeds asset volatility.
- Double-counting. The option value is an *alternative* estimate of equity value, not something to add to the DCF equity value.
- Ignoring the implied debt interest rate. If it comes out implausible, the inputs are inconsistent.
- Forgetting that the DCF for the same firm must use a 0% tax rate while losses persist, since net operating losses shield income; otherwise S itself is wrong.

**Sources:**
- valuations--projects--eqprojspr19 p.7
- valuations--projects--valproject2 p.18-20

**Related:** [[dcf-model-selection]], [[valuation-triangulation-and-recommendation]], [[equity-valuation-project-blueprint]], [[project-company-selection]], [[return-spread-and-eva-analysis]]
