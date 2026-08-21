# Jensen's alpha from the beta regression

**Core idea:** The beta regression produces two numbers, not one. The slope is the beta. The **intercept** measures how the stock performed over the estimation period relative to what the CAPM predicted. The intercept is not compared to zero. Rewriting the CAPM in regression form shows the correct benchmark is R_f(1 − β), where R_f is the riskfree rate *during* the regression period, expressed per return interval. Jensen's alpha is the intercept minus that benchmark. It is a backward-looking, model-dependent performance measure. It says nothing directly about management quality and nothing reliable about future returns.

**Formulas:**
- CAPM rewritten: R_j = R_f + β(R_m − R_f) = **R_f(1 − β) + β·R_m**.
- Regression estimated: R_j = a + β·R_m.
- **Jensen's alpha = a − R_f(1 − β)**, where a = regression intercept and R_f = riskfree rate over the regression period, per return interval.
- Per-interval riskfree rate: R_f,period = Annual riskfree rate / n, where n = 12 for monthly returns and 52 for weekly returns. (A geometric variant uses (1 + annual R_f)^(1/n) − 1; `risk.xls` uses the geometric form, `riskchecker.xls` the simple division. Either is acceptable; be consistent.)
- Annualized alpha = (1 + Jensen's alpha per period)^n − 1.

**Procedure:**
1. Run the beta regression and record the **intercept** and the **beta** (see [[regression-beta]]). Note the return interval used.
2. Note that Bloomberg-style screens report the intercept in **percent** — an "ALPHA" of 0.599 means 0.599% per month, and a value shown as 0.05 means 0.05%.
3. Get the **average riskfree rate over the regression period**, not today's rate. Use the average T-bill rate across those years in the right currency.
4. Convert it to the return interval: divide by 12 for monthly data or 52 for weekly data.
5. Compute the benchmark R_f(1 − β). It is negative whenever β > 1.
6. Jensen's alpha = intercept − R_f(1 − β).
7. Annualize by compounding over n periods.
8. Interpret: a > R_f(1 − β) means the stock beat CAPM expectations over that window; a = R_f(1 − β) means it performed as expected; a < R_f(1 − β) means it underperformed.

**Reference data:**

Average riskfree rates by currency for use as the "past" riskfree rate (from `riskchecker.xls`):

| Currency | Avg riskfree, last 2 years | Avg riskfree, last 5 years |
|---|---|---|
| US $ | 0.20% | 0.50% |
| Euro | 0.25% | 0.60% |
| British £ | 1.00% | 2.00% |
| Japanese Yen | 0.30% | 0.50% |
| Brazilian Real | 5.00% | 7.00% |
| Indian Rupee | 6.00% | 7.00% |
| Chinese Yuan | 3.00% | 4.00% |
| Swiss Franc | 0.50% | 0.75% |

If the currency is not listed, use 4% as the average riskfree rate.

Interpretation rules:
- Averaged across all stocks on an exchange, Jensen's alpha should be close to zero. It is a zero-sum measure relative to the model.
- A positive alpha over a past window is not proof that management did a good job. It measures stock performance against a risk model, and a stock can outperform for reasons management does not control.
- A positive past alpha carries little information about future returns.

**Worked example (Disney, October 2008 - September 2013, monthly):** Regression intercept 0.712% per month; beta 1.252. The average annualized T-bill rate over the period was 0.50%, so the monthly riskfree rate = 0.50%/12 = 0.042%.

- Benchmark: R_f(1 − β) = 0.042% × (1 − 1.252) = **−0.0105%**.
- Jensen's alpha = 0.712% − (−0.0105%) = **0.723% per month**.
- Annualized: (1 + 0.00723)^12 − 1 = **9.02% per year**.

Disney beat CAPM expectations by about 9% a year over that window.

**Worked example (Tata Motors, September 2008 - September 2013, monthly, rupees):** Intercept 2.28% per month; beta 1.83; average annual rupee riskfree rate over the period 4%, so monthly R_f = 4%/12 = 0.333%. Jensen's alpha = 2.28% − 0.333% × (1 − 1.83) = **2.56% per month**, or (1.0256)^12 − 1 = **35.42% per year**.

**Worked example (weekly data, `riskchecker.xls`):** Weekly returns (n = 52), raw beta 1.192, intercept 0.00078 (i.e. 0.078%), past annual riskfree rate 0.25%. Per-week R_f = 0.0025/52 = 0.0000481. Benchmark = 0.0000481 × (1 − 1.192) = −0.0000092. Jensen's alpha = 0.00078 + 0.0000092 = **0.00078923 per week**, annualized to (1.00078923)^52 − 1 = **4.19%**.

**Worked example (underperformance, `risk.xls`):** Intercept −0.447% per month, beta 1.779, in-period riskfree rate 6% per year = 0.487% per month (geometric). Benchmark = 0.487% × (1 − 1.779) = −0.379%. Jensen's alpha = −0.447% − (−0.379%) = **−0.068% per month** — slight underperformance.

**Determinism:**
- DETERMINISTIC: (regression intercept, beta, past annual riskfree rate, periods per year) → Jensen's alpha per period and annualized. A script needs only those four numbers.
- JUDGMENT: which riskfree rate represents "the period"; whether to de-annualize simply or geometrically; whether the CAPM is the right benchmark at all (alpha is defined relative to a model, so a different model gives a different alpha); what, if anything, a positive alpha implies.

**Pitfalls:**
- Comparing the intercept to zero instead of to R_f(1 − β). For a high-beta stock the benchmark is negative, so this error understates alpha.
- Using **today's** riskfree rate rather than the average over the regression window.
- Forgetting to convert the annual riskfree rate to the return interval.
- Missing that Bloomberg reports the intercept in percent, which shifts the answer by two orders of magnitude.
- Reading alpha as a verdict on management. The regression measures the stock, not the managers.
- Extrapolating a past alpha into the future.

**Sources:**
- corporate_finance--lecture_slides--cfpacket1spr20 p.133, p.137-138, p.143, p.147, p.149
- spreadsheet `risk.xls` (Corporate Finance collection): alpha, Rf(1−β), and Jensen's alpha from a hand-built regression
- spreadsheet `riskchecker.xls` (Corporate Finance collection): Jensen's alpha per period and annualized, plus beta confidence ranges, from Bloomberg outputs

**Related:** [[regression-beta]], [[capm-cost-of-equity]], [[bottom-up-beta]], [[market-efficiency]]
