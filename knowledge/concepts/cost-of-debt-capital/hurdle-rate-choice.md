# Choosing the hurdle rate: cost of equity or cost of capital

**Core idea:** Either the cost of equity or the cost of capital can serve as a hurdle rate. Which one you use depends entirely on whose returns you are measuring. Measure returns to equity investors and the benchmark is the cost of equity. Measure returns to the whole firm — all claimholders — and the benchmark is the cost of capital. This is a matching rule, not a computation. Two further matching requirements ride along with it: the hurdle rate must reflect the risk of the specific investment, not the corporate average, and it must be in the same currency as the returns being measured.

**Formulas:**
- Returns to equity (net income, return on equity, cash flow to equity) → compare to Cost of equity = Riskfree rate + Levered beta × ERP.
- Returns to the firm (after-tax operating income, return on capital, free cash flow to the firm) → compare to Cost of capital.
- Excess return (equity) = Return on equity − Cost of equity.
- Excess return (firm) = Return on capital − Cost of capital.
- Return on capital = EBIT × (1 − t) / Book value of capital, where Book value of capital = Book debt + Book equity − Cash.
- Economic Value Added = (Return on capital − Cost of capital) × Book value of capital.

**Procedure:**
1. Identify the numerator. Is it a return to equity holders only, or to all capital providers?
2. Pick the matching denominator: cost of equity for equity returns, cost of capital for firm returns.
3. Pick the right RISK level. Use the cost of capital of the business the project belongs to, not the company average ([[divisional-cost-of-capital]]).
4. Adjust for geography. A project in an emerging market needs a country risk premium in its cost of equity, even when the parent is a developed-market firm ([[country-risk-in-cost-of-debt]]).
5. Match currencies. A rupee return is compared to a rupee hurdle rate ([[currency-conversion-of-discount-rates]]).
6. Check the horizon. An average return computed over an arbitrary window can be misleading for a long-lived project, because early-year losses drag the average down.
7. Compare and decide: accept if the return exceeds the risk-matched hurdle rate.

**Reference data:** The matching rule.

| What you measured | Hurdle rate | Level of risk |
|---|---|---|
| Return on equity, net income, FCFE | Cost of equity | Business-specific levered beta |
| Return on capital, EBIT(1−t), FCFF | Cost of capital | Business-specific, at the division's debt ratio |
| A project in an emerging market | Either, adjusted | Add a country risk premium to the ERP |
| A private firm with an undiversified owner | Total-beta version | Cost of equity built on a total beta, not a market beta |

Company-level illustration: return on capital versus cost of capital across the packet's running firms (currency in millions).

| Company | EBIT(1−t) | BV of capital | Return on capital | Cost of capital | Spread |
|---|---|---|---|---|---|
| Disney | $6,920 | $54,899 | 12.61% | 7.81% | +4.80% |
| Vale | $12,432 | $119,402 | 10.41% | 8.20% | +2.22% |
| Baidu | ¥9,111 | ¥30,320 | 30.05% | 12.42% | +17.63% |
| Tata Motors | ₹120,905 | ₹575,983 | 20.99% | 11.44% | +9.55% |
| Bookscape (total-beta cost of capital) | $1,775 | $19,136 | 9.28% | 10.30% | −1.02% |

Bookscape is the instructive case: it earns 9.28% on capital, which clears its 6.57% market-beta cost of capital but fails its 10.30% total-beta cost of capital. Which hurdle is right depends on whether the owner is diversified.

**Worked examples:**

*Disney movie project.* A big-budget movie is projected to return 9.5% on equity. Against Disney's company-wide cost of equity of 8.52% it clears. Against the Studio Entertainment cost of equity of 9.92% it fails. The movie belongs to Studio Entertainment, so the correct answer is to reject. Using the corporate average would make safe divisions such as Parks & Resorts (7.09% cost of equity) subsidize risky ones and would bias the firm toward its riskiest businesses.

*Rio Disney.* The project's average return on capital over its first ten years is 4.18%. The candidate benchmarks are the 2.75% riskfree rate, Disney's 8.52% company cost of equity, the 7.09% theme-park cost of equity, the 7.81% company cost of capital and the 6.61% theme-park cost of capital. None is right as stated. Return on capital is a return to all capital, so the benchmark must be a cost of CAPITAL. It must be the theme-park business's rate, not the company average. And it must be adjusted for Brazil. Adding a 3% Brazil country risk premium to the 5.5% mature-market premium gives a total ERP of 8.5%, so the project cost of equity = 2.75% + 0.7537 × 8.5% = 9.16%, and at a 10.24% theme-park debt ratio with a 2.40% after-tax cost of debt the project cost of capital = 9.16% × 0.8976 + 2.40% × 0.1024 = **8.46%**, versus 6.61% for a mature-market theme park. On that comparison 4.18% < 8.46% and the project fails — though the ten-year window truncates a park whose life is far longer, so the average understates the true return.

**Determinism:**
- DETERMINISTIC: computing the returns, computing each candidate hurdle rate, and comparing them.
- JUDGMENT: which hurdle rate matches. That needs a clear reading of what the numerator measures and to whom.
- JUDGMENT: which business the project belongs to, and therefore which divisional rate applies.
- JUDGMENT: whether a country risk premium is warranted. Exchange-rate risk and some political risk are diversifiable for a geographically diversified firm or globally diversified investors, so no premium is added for mature-market projects. Emerging-market political risk that cannot be diversified does warrant one.
- JUDGMENT: whether the measurement horizon makes the comparison meaningful.

**Pitfalls:**
- Comparing a return on capital to a cost of equity, or a return on equity to a cost of capital.
- Using one company-wide hurdle rate for every division and every project.
- Comparing a project return to the riskfree rate.
- Adding a currency-risk premium to the discount rate for a firm that is already geographically diversified, or for a project in another mature market.
- Judging a 25-year infrastructure project on a 10-year average return, where construction-year losses depress the average.
- Ignoring that a private firm's owner may be undiversified, which makes the market-beta hurdle rate too low.

**Sources:**
- corporate_finance--lecture_slides--cfpacket1spr20 p.173, p.204-205
- corporate_finance--lecture_slides--cfpacket1spr20 p.221-226, p.229
- corporate_finance--lecture_slides--cfpacket1spr20 p.201-202
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.115
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.112

**Related:** [[cost-of-capital-assembly]], [[divisional-cost-of-capital]], [[country-risk-in-cost-of-debt]], [[currency-conversion-of-discount-rates]], [[return-on-invested-capital]], [[economic-value-added]], [[total-beta]], [[cost-of-equity]]
