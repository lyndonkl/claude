# Truncation risk: nationalization, regime change and catastrophe

**Core idea:** Some companies face risks that do not reduce cash flows — they end them. A hurricane destroys an uninsured plant. A civil war destroys the business. A government nationalizes the asset and pays owners less than fair value. A new regime rewrites the royalty and tax terms. These are truncation risks: the life of the firm, or of the equity claim, is cut short. They cannot be handled by nudging the discount rate, because they are not marginal risks and they are not diversifiable in the way the CAPM assumes. Handle them exactly like distress: build the scenarios, value each one, and weight by probability.

**Formulas:**
- `Expected value of equity = Value under status quo × P(status quo) + Value under the truncating event × P(event)`.
- The truncating branch is **not** always zero. Model it: a partial expropriation, a higher royalty and tax regime, or a compensated nationalization all have a computable value.
- Dividend discount form for a promised-payout entity: `Value of equity = Σ_{t=1..N} D_1 × (1 + g)^(t−1) / (1 + k_e)^t`, with `D_1` the promised dividend, `g` the growth in that promise, `N` the horizon, and `k_e = riskfree + β × ERP`.
- Free cash flow to equity form (potential dividends): `Equity reinvestment rate = g / ROE`; `FCFE = Net income × (1 − g/ROE)`; discount at a cost of equity built on the **operating** business beta, not the payout beta.
- Country equity risk premium as in [[country-risk-exposure]]: `ERP = Mature-market ERP + Country risk premium`.

**Procedure:**
1. Name the truncating event precisely: expropriation, regime change with harsher fiscal terms, nationalization with partial compensation, natural disaster, war.
2. Value the status quo fully, in the currency you have chosen.
3. Value the truncated branch as its own DCF wherever possible. Only use zero when the equity claim genuinely vanishes.
4. Assign a probability. This is political judgment, and it should be stated as such and stress-tested across a range.
5. Blend, and present the branch values and the probability alongside the answer so a reader can substitute their own probability.
6. Check the risk is not already double counted. If you have added a country risk premium to the cost of equity **and** a nationalization scenario, make sure the premium covers ordinary economic and political volatility while the scenario covers only the discrete, catastrophic event.
7. For small firms in disaster-prone economies with no access to insurance or derivatives, remember the exposure is undiversifiable for the owner even if it is diversifiable for a global investor.

**Reference data:** The three forms of truncation risk the source names, with what makes each hard:

| Form | Who is exposed | Why it cannot be hedged away |
|---|---|---|
| Natural disaster | Small companies in hurricane- or earthquake-prone economies | No insurance market and no derivatives available to them |
| Terrorism / civil war | Companies in unstable countries | Damage or destruction of the business, not just of cash flows |
| Nationalization | Businesses in countries with expropriation history | Less common than it once was; owners typically receive less than fair value |

**Worked example:** Saudi Aramco, valued three ways around its IPO.

*(a) Promised dividends.* Aramco promised $75 billion in year 1, growing at the US-dollar inflation rate of 1% for 50 years. Because the stream is a promise and behaves like a bond, the beta used is 0.50 — the beta of REITs and royalty trusts. Equity risk premium = 5.44% mature + 0.79% Saudi CRP = 6.23%. Cost of equity = 1.80% + 0.50 × 6.23% = **4.92%**. Dividend in year `t` = 75 × 1.01^(t−1) billion, running from $75bn to $122.13bn in year 50. Value of equity = **$1,629.61 billion**.

*(b) Potential dividends (FCFE).* Expected net income next year = $111bn × 1.018 = $113bn. With 2018 ROE of 40.96% and growth at nominal US-dollar GDP growth of 1.80%, the equity reinvestment rate is only `0.018/0.4096 = 4.39%`. FCFE = 113 × (1 − 0.0439) = **$108.03bn**, growing 1.80% for 50 years to $258.94bn. Now the full cash-flow claim is being valued, so the beta is that of integrated oil, 1.02, giving a cost of equity of 1.80% + 1.02 × 6.23% = **8.15%**. PV = $1,589.12bn; plus cash $48.84bn and holdings $10.61bn = **$1,648.57 billion**. The two approaches land within 1% of each other, because the higher cash flows are offset by the higher discount rate.

*(c) Regime change.* If the House of Saud rules indefinitely, equity is worth $1.65 trillion. If regime change is imminent and equity is fully expropriated, it is worth zero. The realistic case sits between: a DCF under a regime that raises royalties and taxes gives $0.825 trillion. With a 20% probability of that regime change:
`Expected value = 1.65 × 0.80 + 0.825 × 0.20 = $1.485 trillion`.

**Determinism:** DETERMINISTIC — (dividend level, growth, horizon, cost of equity) → the promised-dividend value; (net income, ROE, growth, beta, ERP) → the FCFE value; (branch values, probabilities) → the expected value. All three Aramco numbers are reproducible from the inputs above. JUDGMENT: the probability of regime change or nationalization (needs political analysis, history of expropriation in the country, the state's fiscal position, and the terms of the concession), the value of the truncated branch (needs an assumption about the new fiscal terms), the beta appropriate to a promised versus a residual claim, and the 50-year horizon.

**Pitfalls:**
- Adding a "political risk premium" to the discount rate instead of building scenarios. The event is discrete and catastrophic, not a marginal increase in volatility.
- Setting the truncated branch to zero by reflex. Partial expropriation is far more common than total expropriation, and the difference is worth hundreds of billions in the Aramco case.
- Using the same beta for a promised dividend stream and for the underlying business. A bond-like promise deserves a bond-like beta; the residual claim on an oil business does not.
- Double counting: a country risk premium in the cost of equity plus a nationalization scenario plus a governance discount is three charges for overlapping risks.
- Hiding the probability. State it, because it is the only genuinely subjective input and readers will want to substitute their own.
- Treating truncation risk as diversifiable for an owner who cannot diversify — a small local firm with no insurance faces the full loss.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.337-340
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.328-331

**Related:** [[distress-and-failure-adjusted-value]], [[country-risk-exposure]], [[cross-holdings]], [[currency-consistency-and-invariance]], [[financial-service-firm-valuation]], [[difficult-company-taxonomy]], [[dividend-discount-model]], [[fcfe-valuation]]
