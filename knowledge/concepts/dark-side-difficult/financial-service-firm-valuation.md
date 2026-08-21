# Valuing financial service firms: why FCFF fails and dividends step in

**Core idea:** For a bank or an insurer, debt is raw material, not a source of capital. You cannot separate operating from financing decisions, so free cash flow to the **firm** and the cost of capital are meaningless — value the equity directly. The next problem is that free cash flow to equity is barely estimable either, because capital expenditures and working capital have no clean definition at a bank. That leaves dividends. This is a Faustian bargain, and the source says so plainly: banks tell us very little about the quality of their assets (loans are not broken out by default risk), but in return their assets are marked to market by accountants who presumably have the information we lack, and we trust them to pay out what they can afford. The dividend discount model is the default. It stops being trustworthy in a crisis, or whenever payout diverges from capacity.

**Formulas:**
- `Expected growth in earnings = Retention ratio × Return on equity`, with `Retention ratio = 1 − Payout ratio`.
- `Cost of equity = Riskfree rate + Beta × Equity risk premium`. Use a bank-sector beta; the currency of the riskfree rate must match the cash flows ([[currency-consistency-and-invariance]]).
- Sustainable stable payout: `Payout_stable = 1 − g_stable / ROE_stable`.
- Terminal value of equity at the end of the explicit forecast: `TV_n = EPS_{n+1} × Payout_stable / (k_e,stable − g_stable)`.
- `Value per share = Σ_{t=1..n} DPS_t / (1 + k_e)^t + TV_n / (1 + k_e)^n`.
- Regulatory-capital haircut on ROE: `Adjusted ROE = Trailing ROE / (1 + required increase in capital base)`. Wells Fargo: `0.1756 / 1.3 = 13.5%` for an assumed 30% increase in required capital.
- Anchoring stable ROE: set `ROE_stable = k_e,stable` unless the bank has a durable franchise. That forces excess returns to zero in perpetuity.

**Procedure:**
1. Decide the model. Dividends by default; switch to an FCFE-to-regulatory-capital model or an excess-return model when payout does not reflect capacity, when the bank is in crisis, or when capital ratios are moving ([[bank-fcfe-and-excess-return-models]]).
2. Set the currency and build the riskfree rate in it.
3. Estimate the cost of equity with a sector beta (Wells Fargo used 1.20, the average US bank beta over the prior year; CIB Egypt used 0.81, the average bank beta) and an exposure-appropriate equity risk premium.
4. Establish base EPS, dividends per share and the payout ratio.
5. Estimate a **sustainable** ROE, not the trailing one. Adjust downward for any required increase in the capital base, and for any part of past returns driven by leverage the regulator will no longer permit.
6. Growth = retention × sustainable ROE. Use a two-stage model whenever near-term growth exceeds stable growth.
7. Fade growth toward stable growth and fade the payout ratio up toward `1 − g/ROE` over the transition. High-ROE banks must pay out more as ROE falls.
8. Compute the terminal value with the sustainable payout, discount everything at the cost of equity, and compare with the price.
9. Sanity-check the implied book equity and the implied capital ratio. A model that pays out more than the bank can afford while still meeting its capital ratio is not internally consistent.

**Reference data (1):** Wells Fargo, 7 October 2008 — a two-stage dividend discount model mid-crisis.

| Input | Value |
|---|---|
| Trailing 12-month EPS | $2.16 |
| Payout ratio | 54.63% (DPS $1.18) |
| Trailing ROE | 17.56% |
| Assumed capital-base increase | +30% (tighter regulation) |
| Sustainable ROE | 0.1756/1.3 = 13.5% |
| Retention ratio | 45.37% |
| Expected growth | 45.37% × 13.5% = 6.13% |
| Riskfree rate / beta / ERP | 3.60% / 1.20 / 5% (country risk 0%) |
| Cost of equity | 9.60% |
| Forecast EPS, years 1–5 | $2.29, $2.43, $2.58, $2.74, $2.91 |
| Forecast DPS, years 1–5 | $1.25, $1.33, $1.41, $1.50, $1.59 |
| Stable phase | g = 3%, ROE 7.6% (= stable cost of equity), beta 1.00, ERP 4%, payout = 1 − 3/7.6 = 60.55% |
| Terminal value | ($3.00 × 0.6055)/(0.076 − 0.03) = $39.41 |
| **Value per share** | **$30.29** versus a price of $33 |

**Reference data (2):** Commercial International Bank (CIB) Egypt, December 2015 — the same model in a high-inflation currency.

| Input | Value |
|---|---|
| Base EPS / payout / DPS | 4.04 EGP / 24.75% / 1.00 EGP |
| ROE | 42.48%; retention 75.25% |
| High growth | 75.25% × 42.48% = 31.96% for 5 years |
| Growth fade, years 6–10 | 27.57%, 23.18%, 18.79%, 14.39%, 10.00% |
| EGP riskfree rate | (1.0227) × (1.097/1.015) − 1 = 10.53% |
| Cost of equity | 10.53% + 0.81 × 15.70% = 23.25% (100% Egypt exposure) |
| EPS path (EGP) | 5.33, 7.04, 9.28, 12.25, 16.17, 20.63, 25.41, 30.18, 34.52, 37.97 |
| Payout path | 24.75% rising to 60% by year 10 |
| DPS path (EGP) | 1.32, 1.74, 2.30, 3.03, 4.00, 6.56, 9.87, 13.85, 18.28, 22.78 |
| Stable phase | g = 10%, ROE 25% (= stable cost of equity), payout = 1 − 10/25 = 60% |
| Terminal value | (37.97 × 0.60)/(0.2325 − 0.10) = 189.20 EGP |
| **Value per share** | **41.93 EGP** versus a price of 36 EGP |

**Worked example:** Wells Fargo, October 2008. Everything hinges on one judgment: the trailing ROE of 17.56% was earned on a capital base that regulators were about to demand be 30% larger. Dividing by 1.3 gives a sustainable ROE of 13.5%, which cuts expected growth from about 8% to 6.13%. Discounting five years of dividends ($1.25 to $1.59) plus a terminal value of $39.41 at 9.60% gives **$30.29 per share**, against a market price of $33. Without the capital haircut the model would have said Wells Fargo was cheap; with it, the stock looked roughly fairly priced.

**Determinism:** DETERMINISTIC — (base EPS, payout path, ROE, growth path, cost of equity, stable growth and stable ROE) → EPS and DPS paths, terminal value, value per share. Both tables above are exactly reproducible. Also deterministic: `payout_stable = 1 − g/ROE` and the riskfree-rate construction from an inflation differential. JUDGMENT: the sustainable ROE (needs the regulatory capital trajectory, the bank's asset quality, and peer ROEs), the size of any required capital increase, the beta and equity risk premium, the growth-fade schedule, and whether dividends are a fair proxy for capacity at all.

**Pitfalls:**
- Building an FCFF model for a bank. Debt is raw material; there is no meaningful cost of capital and no meaningful firm value.
- Using the trailing ROE when the regulator is about to demand more capital. Leverage-driven ROE does not survive re-regulation.
- Trusting the dividend discount model in a crisis, or when a bank is paying out far more or far less than it can afford.
- Letting the payout ratio stay at its high-growth level while ROE falls toward the cost of equity. The two are linked by `payout = 1 − g/ROE`.
- Ignoring preferred stock, which is a significant source of capital for financial firms and a claim ahead of common equity.
- Forgetting the hard constraint that has no analogue elsewhere: a bank that breaches its regulatory capital ratio can be taken over and shut down, however good its earnings look.
- Mixing a US-dollar cost of equity with local-currency earnings for an emerging-market bank.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.341-344
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.332-335

**Related:** [[bank-fcfe-and-excess-return-models]], [[currency-consistency-and-invariance]], [[country-risk-exposure]], [[difficult-company-taxonomy]], [[dividend-discount-model]], [[sustainable-growth]], [[cost-of-equity]]
