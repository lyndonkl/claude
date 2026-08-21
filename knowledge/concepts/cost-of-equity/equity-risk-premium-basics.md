# The equity risk premium: what it is and the three ways to estimate it

**Core idea:** The equity risk premium (ERP) is the extra return investors demand for holding an average-risk equity investment instead of the riskfree asset. It is the single number that prices risk in an entire market, and in a CAPM cost of equity it is the only input that is market-wide rather than company-specific. Three properties must hold for any estimate: it must be positive, it must rise as investors become more risk averse, and it must rise as the average investment becomes riskier. There are exactly three families of estimation method — survey investors, average what stocks actually earned in the past (historical), or back it out of what investors are paying for stocks today (implied). Damodaran uses the implied premium as his default.

**Formulas:**
- Definition: ERP = Expected return on the market portfolio − Riskfree rate = E(R_m) − R_f.
- Cost of equity uses it as: Cost of Equity = R_f + Beta × ERP.
- Market equilibrium view: the market ERP is a wealth-weighted average of the premiums individual investors demand, so wealthier investors' risk aversion counts more.
- Sanity check against credit: ERP ≈ 2 × Baa corporate default spread (median ratio 2.02 over 1960-2020).

Symbols: E(R_m) = expected return on a portfolio of all stocks; R_f = riskfree rate in the same currency; Beta = the firm's relative risk (see [[regression-beta]], [[bottom-up-beta]]).

**Procedure:**
1. Fix the currency and riskfree rate first — an ERP is always "premium over *this* riskfree rate" (see [[riskfree-rate-fundamentals]]).
2. Choose an estimation family:
   - **Survey**: ask investors, CFOs, or analysts what premium they demand and average. Cheap, but unconstrained (surveys can produce negative or absurd premiums), backward-looking, and almost always short-horizon (one year or less). Not recommended as a primary source.
   - **Historical**: average the realized return on a stock index minus the realized return on a riskless security over a long window. See [[historical-equity-risk-premium]].
   - **Implied**: solve for the discount rate that equates the present value of expected market cash flows to the current index level, then subtract the riskfree rate. See [[implied-equity-risk-premium]].
3. Apply the three sanity checks: is it positive? Does it move up when fear rises? Is it consistent with the riskiness of the market you are pricing?
4. Cross-check against the credit market. Divide your ERP by the current Baa−T.Bond default spread. A ratio far from 2 means equity and credit markets are pricing risk very differently, which needs an explanation.
5. For a market outside the US, do not reach for local historical data first. Non-US return histories are short and emerging-market histories are shorter still, so the standard errors swamp the estimate. Build the country ERP off a mature-market premium instead — see [[country-risk-premium]].
6. Re-estimate. Premiums are not constants. They spike in crises and mean-revert (the implied ERP went from ~4.3% in September 2008 to nearly 8% in November 2008, and from 4.83% in February 2020 to 7.75% at the March 23, 2020 COVID bottom).

**Reference data:**

Survey-based ERP estimates:

| Group surveyed | Survey by | ERP | Note |
|---|---|---|---|
| Individual investors | Securities Industries Association | 8.3% (2004) | One-year premium |
| Institutional investors | Merrill Lynch | 4.8% (2013) | Monthly updates |
| CFOs | Campbell Harvey & John Graham | 4.48% (2012) | 5-8% response rate |
| Analysts | Pablo Fernandez | 5.0% (2011) | Lowest standard deviation |
| Academics | Pablo Fernandez | 5.7% (2011) | Higher for emerging markets |

Benchmark ERP values used across the packets: **4.72%** (implied, 1/1/2021, the mature-market premium used throughout the 2021 valuation packet); 5.20% (implied, 1/1/2020); 5.5% (implied, November 2013).

Long-run averages of the US implied ERP: 1960-2020 = 4.21%; 2001-2020 = 4.95%; 2011-2020 = 5.53%.

**Worked example:** On January 1, 2021 the mature-market ERP is 4.72% and the US 10-year T.Bond rate is 0.93%. A US company with a beta of 1.10 therefore has a cost of equity of 0.93% + 1.10 × 4.72% = **6.12%**. Sanity checks: the premium is positive; it sits above the 4.21% 1960-2020 average, consistent with a post-COVID market that is not complacent; and the implied expected return on stocks is 5.65%, the lowest in 60 years — driven by the riskfree rate, not by a collapse in the premium.

**Determinism:**
- DETERMINISTIC: (R_f, Beta, ERP) → cost of equity; (ERP, Baa spread) → the cross-market ratio; averaging a series of survey or implied premiums.
- JUDGMENT: which estimation family to use; whether the current premium or a long-run average is the right forward-looking number; whether an observed premium is "too high" or "too low"; how much weight to give surveys (very little).

**Pitfalls:**
- Treating the ERP as a fixed constant ("the equity risk premium is 6%") when it demonstrably moves with market conditions.
- Pairing an ERP with the wrong riskfree rate. A premium measured over T.Bills cannot be added to a T.Bond rate.
- Using survey premiums for long-horizon valuation. They are short-term and unconstrained.
- Estimating a local historical premium from twenty years of emerging-market data. The standard error will exceed the estimate.
- Forgetting that the premium you choose is applied to *every* company you value, so an error here is a systematic bias, not a random one.

**Sources:**
- corporate_finance--lecture_slides--cfpacket1spr20 p.108-113, p.119, p.126
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.22, p.26, p.70, p.72, p.74
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.22, p.26, p.72

**Related:** [[historical-equity-risk-premium]], [[implied-equity-risk-premium]], [[choosing-an-equity-risk-premium]], [[country-risk-premium]], [[capm-cost-of-equity]], [[riskfree-rate-fundamentals]]
