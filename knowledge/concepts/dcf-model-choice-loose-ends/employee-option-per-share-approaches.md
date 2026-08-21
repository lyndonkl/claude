# Employee options and value per share: three approaches

**Core idea:** Outstanding employee options reduce value per share, but not for the reason most people give. Dilution alone is not the problem. Options hurt because they are exercised only when in the money, so the firm issues shares below the prevailing market price. Equivalently, the firm spends cash that would have gone to equity investors buying back shares to deliver on exercise. Either way, existing shareholders lose. And options affect value *before* exercise too, because today's valuation must build in the probability and cost of future exercise. Three methods are in circulation. Two are wrong in predictable directions. The third — value the options and subtract them as a separate claim — is the one to use.

**Formulas:**
- I. Diluted share count: `Value per share = (Firm value − Debt) / (Existing shares + shares from option exercise)`. Ignores exercise proceeds → understates value per share.
- II. Treasury stock: `Value per share = (Equity value + Option exercise proceeds) / Diluted shares`, with `proceeds = number of options × strike price`. Ignores the option time premium → overstates value per share.
- III. Option value drag (preferred): `Value per share = (Equity value − Value of all option claims) / Actual shares outstanding`.
  - `Value of Warrants = Market Price per Warrant × Number of Warrants` (or an option pricing model).
  - `Value of Conversion Option = Market Value of Convertible Bonds − Value of the Straight Debt Portion`.
  - `Value of employee options = option pricing model run at the average exercise price and average maturity`.

**Reference data — the three approaches compared on one example:**

| Approach | Formula applied to XYZ | Value per share | Bias |
|---|---|---|---|
| I. Diluted share count | 1,000 / 110 | **$9.09** | Too low — ignores the cash exercise brings in |
| II. Treasury stock | (1,000 + 100) / 110 | **$10.00** | Too high — ignores the options' time premium |
| III. Option value drag | (1,000 − 54.2) / 100 | **$9.46** | Consistent; sits between the other two |

Known failure of the treasury stock method: it mishandles out-of-the-money options. Include them and they can perversely *raise* value per share (the proceeds are added, the value is not). Exclude them and they are treated as worthless, even though an out-of-the-money option still has time value.

**Procedure (the option value drag method):**
1. Value the firm with a DCF or another model.
2. Subtract outstanding debt to get the value of equity (or estimate equity directly).
3. Subtract the market value, or estimated value, of every other equity claim: warrants, the conversion option inside convertible bonds, and employee options. Value the employee options with an option pricing model at the average exercise price and average maturity — see [[valuing-employee-options]].
4. Divide the remaining equity by **actual** shares outstanding, not diluted shares.
5. If option exercise generates a tax deduction for the firm, use the after-tax option cost.
6. Handle expected future grants separately, as an operating expense ([[restricted-stock-and-future-grants]]).

**Worked example (XYZ):** XYZ has FCFF of $100 million growing 3% a year forever, a cost of capital of 8%, 100 million shares and $1 billion of debt.
- Base case: `Value of firm = 100/(0.08 − 0.03) = 2,000`. Equity = 2,000 − 1,000 = 1,000. Value per share = 1,000/100 = **$10.00**.
- XYZ now grants its CEO **10 million at-the-money options** with a $10 strike. What happens to value per share? The answer is not "nothing" (the options are not in the money yet, but they have time value) and not "−10%" (exercise brings cash into the firm). The correct answer: value falls by **less than 10%**.
- Approach I: diluted shares = 110 → 1,000/110 = **$9.09**.
- Approach II: proceeds = 10 × $10 = $100 → (1,000 + 100)/110 = **$10.00**, identical to the no-option value, which cannot be right.
- Approach III: each option is worth $5.42 by a dilution-adjusted Black-Scholes ([[valuing-employee-options]]). Total option value = 10 × 5.42 = $54.2m. Equity in common stock = 1,000 − 54.2 = 945.8. Value per share = 945.8/100 = **$9.46** — a 5.4% drop, between the two flawed answers, exactly as the logic predicts.

**Determinism:**
- DETERMINISTIC: all three per-share calculations given equity value, option count, strike, share count and per-option value. Also the bracketing property: the drag answer always sits between the diluted and treasury answers for in-the-money-or-at-the-money grants.
- JUDGMENT: the option valuation inputs (volatility, effective maturity, vesting probability) and whether to tax-adjust. See [[valuing-employee-options]].

**Pitfalls:**
- Subtracting option value **and** dividing by diluted shares. That is the same cost twice.
- Using the treasury stock method because it is what the accounting diluted EPS calculation does. Accounting convention is not valuation.
- Counting out-of-the-money options as non-existent.
- Ignoring warrants and the conversion option embedded in convertible bonds; they are option claims on the same equity.
- Treating the option drag as a one-off. If the firm grants every year, future grants need the expense treatment too.

**Sources:**
- valpacket1spr21 p.244-248, p.251
- valpacket1spr20 p.240-244, p.247

**Related:** [[valuing-employee-options]], [[restricted-stock-and-future-grants]], [[equity-value-bridge]], [[debt-and-other-claims-in-the-bridge]], [[convertible-bond-valuation]]
