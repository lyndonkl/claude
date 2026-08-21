# Country risk with a scalpel: exposure-weighted premiums and lambda

**Core idea:** Emerging-market companies do carry extra risk, because they operate in countries with more political and economic risk. But that risk is not a property of the passport. A Brazilian exporter selling to the world is far less exposed to Brazil than a Brazilian retailer, and Coca-Cola or Heineken carry plenty of emerging-market risk despite being incorporated in developed markets. So country risk should be attached by **exposure**, not by country of incorporation. Two tools do this: a revenue-weighted country risk premium, and a lambda that scales a company's exposure to its home country's premium using more than revenues.

**Formulas:**
- Country equity risk premium: `CRP = Country default spread × Relative equity market volatility`. Example: India, April 2010, `3% × 1.50 = 4.50%`.
- Total equity risk premium for a country: `ERP_country = Mature-market ERP + CRP`. In the January 2021 data set the mature-market ERP is **4.72%**.
- Lambda form of the cost of equity: `Cost of equity = Riskfree rate + Beta × Mature-market ERP + Lambda × Country equity risk premium`.
- Revenue-weighted form: `ERP_company = Σ_i w_i × ERP_i`, with `w_i` the share of revenues from country or region `i`. Use this in the standard CAPM: `Cost of equity = Riskfree + Beta × ERP_company`.
- Lambda benchmarks: `λ = 1` means average exposure for a firm in that country; `λ < 1` for exporters and globally diversified firms; `λ > 1` for firms more exposed than the average domestic company. A crude estimator is the ratio of the company's domestic revenue share to the average domestic revenue share of firms in that market.
- Country default spread also enters the cost of debt: `Pre-tax cost of debt = Riskfree rate + Company default spread + Country default spread`.

**Procedure:**
1. Decide the currency first, since the riskfree rate must match it ([[currency-consistency-and-invariance]]).
2. Get the mature-market ERP and each country's CRP. The country table gives, per country, a Moody's rating, an adjusted default spread, a total ERP and a CRP, with `ERP = mature ERP + CRP`.
3. Choose the exposure method:
   - **Revenue-weighted ERP** when you have a revenue breakdown by country or region. Simple, transparent, defensible.
   - **Lambda** when exposure differs from the revenue split — production facilities, input sourcing, hedging, or a business whose demand tracks the local economy more or less than its revenue share suggests.
4. Compute the cost of equity with the chosen method and a bottom-up beta for the business.
5. Add the country default spread to the cost of debt, on top of the company's own default spread.
6. Keep company risk and country risk separate in the write-up, so a reader can change one without the other.
7. Do not also apply a blanket "emerging-market discount" to the resulting value. That is the bludgeon this concept exists to replace.

**Reference data (1):** The Tata Group, April 2010 — one framework, four exposures. Common inputs: rupee riskfree rate 5%, mature-market premium 4.5%, India CRP 4.50% (= 3% default spread × 1.50 relative equity volatility).

| Company | Beta | Lambda | Cost of equity | WACC | Expected growth | ROC | Value/share | Price |
|---|---|---|---|---|---|---|---|---|
| Tata Chemicals | 1.21 | 0.75 | 13.82% | 11.62% | 5.85% (RIR 56.5%) | 10.35% | Rs 372 | Rs 314 |
| Tata Steel | 1.57 | 1.10 | 17.02% | 13.79% | 5.11% (RIR 38.1%) | 13.42% | Rs 844 | Rs 632 |
| Tata Motors | 1.20 | 0.80 | 14.00% | 12.50% | 12.01% (RIR 70%) | 17.16% | Rs 665 | Rs 781 |
| TCS | 1.05 | 0.20 | 10.63% | 10.62% (E = 99.9%) | 23.05% (RIR 56.73%) | 40.63% | ~Rs 1,144 | Rs 841 |

The lambda spread from 0.20 (export-driven TCS) to 1.10 (Tata Steel) is the whole lesson: same country, same date, wildly different exposure.

**Reference data (2):** Revenue-weighted ERP, Heineken, September 2019.

| Region | Revenues (€m) | Weight | ERP |
|---|---|---|---|
| Europe | 10,348 | 50.24% | 6.90% |
| North America | 5,920 | 28.74% | 5.75% |
| Asia | 2,919 | 14.17% | 7.22% |
| Latin America & Caribbean | 781 | 3.79% | 10.53% |
| Africa & Middle East | 631 | 3.06% | 9.30% |
| **Total** | **20,599** | **100.00%** | **6.83%** |

**Reference data (3):** Sample country risk premiums from the January 2021 table (mature-market ERP 4.72%; ERP = 4.72% + CRP).

| Country | Moody's | Adj. default spread | ERP | CRP |
|---|---|---|---|---|
| United States / Germany / Canada / Australia / Singapore | Aaa | 0.00% | 4.72% | 0.00% |
| China | A1 | 0.62% | 5.40% | 0.68% |
| Saudi Arabia | A1 | 0.62% | 5.40% | 0.68% |
| Mexico | Baa1 | 1.41% | 6.27% | 1.55% |
| India | Baa3 | 1.95% | 6.85% | 2.13% |
| Italy | Baa3 | 1.95% | 6.85% | 2.13% |
| Indonesia | Baa2 | 1.68% | 6.56% | 1.84% |
| Brazil | Ba2 | 2.65% | 7.63% | 2.91% |
| South Africa | Ba2 | 2.65% | 7.63% | 2.91% |
| Egypt | B2 | 4.86% | 10.05% | 5.33% |
| Argentina | Ca | 10.60% | 16.34% | 11.62% |
| Lebanon | C | 17.50% | 23.90% | 19.18% |

**Worked example:** Embraer, May 2008, valued entirely in US dollars with a lambda. Country ERP for Brazil = 2.2% default spread × 1.64 relative equity market volatility = 3.66%. Embraer sells aircraft globally, so its lambda is only 0.27. Cost of equity = 3.8% + 0.88 × 4% + 0.27 × 3.66% = **8.31%** (beta 0.88 from an unlevered sector beta of 0.75 at D/E 26.84%). Cost of debt = (3.8% + 1.7% company spread + 1.1% country spread) × (1 − 0.34) = 4.36%. WACC = 8.31% × 0.788 + 4.36% × 0.212 = 7.47%. Base EBIT(1−t) $434m, normalized reinvestment rate 40%, ROC 18.1% → growth 7.2% for 5 years. Stable phase: g = 3.8%, beta 1.00, country premium 1.5%, cost of capital 7.38%, ROC 7.38%, RIR = 3.8/7.38 = 51.47%. Terminal value = 254/(0.0738 − 0.038) = $8,371m. Operating assets $6,239m + cash $3,068m − debt $2,070m − minority interests $177m = equity $7,059m; − options $4m → **$9.53 per share = R$15.72** versus R$17.20 on 22 May 2008.

**Determinism:** DETERMINISTIC — (country default spread, relative equity volatility) → CRP; (mature ERP, CRP) → country ERP; (revenue split by country, country ERPs) → weighted ERP; (riskfree, beta, mature ERP, lambda, CRP) → cost of equity; and the whole DCF that follows. JUDGMENT: the lambda itself (needs revenue geography, production locations, hedging policy, and how the company's demand tracks the local economy), the choice between the lambda and revenue-weighting, the relative equity market volatility multiple, and the stable-period country premium.

**Pitfalls:**
- Assigning country risk by country of incorporation. That is the bludgeon: it over-charges exporters and under-charges developed-market firms with emerging-market operations.
- Applying a country premium **and** an additional discount to the resulting value for "emerging-market risk".
- Forgetting the country default spread in the cost of debt while remembering it in the cost of equity.
- Leaving the country premium at its current level forever. In stable growth it is usually assumed to fall (Tube Investments: 5.23% in the high-growth phase, 3% in stable growth; Embraer: 3.66% → 1.5%).
- Mixing a US-dollar riskfree rate with local-currency cash flows ([[currency-consistency-and-invariance]]).
- Using a lambda you cannot justify. If the only evidence is revenue geography, use the revenue-weighted ERP and say so.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.326-327
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.335
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.331
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.316-318
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.320
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.322
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.326
- spreadsheet model doc: ginzu-fcff-corona.md — Country equity risk premiums sheet (Jan 2021) and Cost of capital worksheet ERP logic

**Related:** [[currency-consistency-and-invariance]], [[cross-holdings]], [[truncation-and-political-risk]], [[return-improvement-and-governance-drag]], [[equity-risk-premium]], [[bottom-up-beta]], [[cost-of-capital]], [[difficult-company-taxonomy]]
