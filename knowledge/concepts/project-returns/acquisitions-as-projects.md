# Acquisitions as projects

**Core idea:** An acquisition is an investment like any other, and every rule for traditional projects applies. It makes sense only if the present value of expected cash flows from the target — including any synergy — exceeds the price paid. Equivalently, the IRR on those cash flows must exceed the cost of capital (or cost of equity, on equity cash flows). One rule deserves special emphasis: the discount rate must reflect the risk of the *target*, not the acquirer. A low-risk acquirer buying a high-risk target does not make the target's cash flows safe. Acquisitions are the place where firms most often abandon their own capital-budgeting discipline, treating the deal under separate and looser rules.

**Formulas:** Symbols: `r` = cost of capital appropriate to the target; `g` = stable growth rate.
- `Acquisition NPV = PV(expected cash flows including synergy) − price paid`. Accept if positive.
- `Value of operating assets = Expected FCFF next year / (r − g)` for a stable-growth target
- `Value of equity = Value of operating assets + Cash − Debt` (debt including the debt value of leases)
- `Maximum price = Stand-alone equity value + Value of synergy`
- `FCFF = Operating income × (1 − tax rate) + Depreciation − Capital expenditures − Change in non-cash working capital`

**Procedure:**
1. Value the target stand-alone, before any synergy. Use the target's currency, business, risk, and financing.
2. Normalize the base-year operating income. Add back non-recurring items such as restructuring charges. Capitalize operating lease commitments as debt and restate operating income accordingly.
3. Choose the tax rate. Use the effective rate the target actually paid if you are projecting its own historical economics; use the marginal rate for incremental analysis.
4. Normalize reinvestment. A one-off working-capital spike in the base year must not be projected forward. Set working capital as a percent of revenues and apply it to the *change* in revenues.
5. Build the cost of capital from the target's characteristics: its industry's unlevered beta, its geographic revenue exposure for the ERP, its rating for the cost of debt, and its debt ratio.
6. Compute the value of operating assets, add cash, subtract debt, and compare to market capitalization. That gap is what the synergy must cover.
7. Value the synergy separately, at the risk of the business receiving it. See [[project-synergies]].
8. Set the ceiling price at stand-alone value plus synergy value. If market price exceeds it, walk away.

**Reference data:** Harman International base year (2013, $ millions), the running example:

| Item | Value |
|---|---|
| Revenues | $4,297.80 |
| Reported operating income | $201.25 |
| Restructuring charge add-back | $83.20 |
| Adjusted operating income (after lease conversion) | $313.19 |
| Effective tax rate paid in 2013 | 18.21% |
| Depreciation | $128.20 |
| Capital expenditures + acquisitions | $206.40 |
| Increase in non-cash working capital (one-off) | $272.60 |
| Non-cash working capital as % of revenues | 13.54% |
| Stable growth rate | 2.75% |
| Cash | $515 |
| Debt including leases | $313 |
| Market capitalization (November 2013) | $5,428 (quoted as $5,248 in the synergy slide) |

Harman cost of capital build-up:
- Currency: US$, matching the cash flows.
- Beta: unlevered beta of US electronics companies = 1.17. Levered = 1.17 × (1 + 0.60 × 0.0798) = 1.226.
- ERP: revenue-weighted across regions = 6.13%.
- Cost of equity = 2.75% + 1.226 × 6.13% = 10.26%.
- Debt: Harman's own debt/capital 7.39% (D/E 7.98%), pre-tax cost of debt 4.75% on a BBB− rating, marginal tax rate 40%.
- Cost of capital = 10.26% × 0.9261 + 4.75% × 0.60 × 0.0739 = **9.67%**.

**Worked example:** Tata Motors / Harman International, end to end ($ millions).

*Step 1 — base year to forecast.* Everything grows at 2.75%; working capital normalizes to 13.54% of the *change* in revenues.

| Item | 2013 | 2014 |
|---|---|---|
| Revenues | $4,297.80 | $4,415.99 |
| Operating income | $313.19 | $321.80 |
| Tax rate | 18.21% | 18.21% |
| After-tax operating income | $256.16 | $263.21 |
| + Depreciation | $128.20 | $131.73 |
| − Capital expenditures | $206.40 | $212.08 |
| − Change in non-cash working capital | $272.60 | $16.01 |
| **Cash flow to the firm** | **−$94.64** | **$166.85** |

Normalizing the working-capital line alone flips FCFF from −$94.64 million to +$166.85 million. The 2013 spike was a one-off; the 2014 figure is 13.54% × ($4,415.99 − $4,297.80) = $16.01 million.

*Step 2 — stand-alone value.* Value of operating assets = 166.85 / (0.0967 − 0.0275) = **$2,476 million**. Value of equity = 2,476 + 515 − 313 = **$2,678 million**. Harman's market equity is $5,428 million, so buying at market price requires synergy worth more than roughly **$2,750 million**.

*Step 3 — synergy.* Tata expects to fit Harman audio as optional upgrades on Indian cars. From year 4, Rs 10 billion of after-tax operating income growing 4% forever, discounted at a rupee cost of capital of 13.63% built from Tata's beta, India's country risk premium, and rupee financing. Value at year 3 = 10,000/(0.1363 − 0.04) = Rs 103,814 million. Discounted three years: Rs 70,753 million. At Rs 60/$: **$1,179 million**.

*Step 4 — verdict.* Maximum justifiable price = 2,678 + 1,179 = **$3,857 million** against a market price of $5,248 million. Even with the synergy fully credited, the acquisition destroys about $1.4 billion of value. Do not acquire at market price.

**Determinism:** DETERMINISTIC — the inputs are the base-year financials, a growth rate, a tax rate, a working-capital ratio, a cost of capital, cash, and debt. A script turns those into the FCFF forecast, the stand-alone value of operating assets and equity, the synergy value, and the maximum price. JUDGMENT — the normalization decisions (which charges are non-recurring, how to treat leases), the stable growth rate, and the entire synergy story. That judgment needs the target's segment financials, its lease footnote, its credit rating, and a credible integration plan.

**Pitfalls:**
- Using the acquirer's cost of capital, which flatters a deal whenever the acquirer is safer than the target.
- Projecting a one-off working-capital swing, a restructuring charge, or an unusual tax rate into perpetuity.
- Failing to capitalize operating leases before computing operating income, debt, and the cost of capital.
- Paying market price without checking what synergy that price implicitly requires. For Harman it required $2,750 million; the credible synergy was $1,179 million.
- Adding a control premium and a synergy value that overlap.
- Treating the acquisition under "M&A rules" instead of the firm's own investment-analysis discipline.

**Sources:**
- corporate_finance--lecture_slides--cfpacket1spr20 p.210-211
- corporate_finance--lecture_slides--cfpacket1spr20 p.276-281
- corporate_finance--lecture_slides--cfpacket1spr20 p.318-320

**Related:** [[project-synergies]], [[project-hurdle-rate-selection]], [[npv-and-irr-mechanics]], [[terminal-value-and-project-life]], [[earnings-vs-cash-flows]], [[currency-and-inflation-consistency]], [[operating-lease-capitalization]], [[cost-of-capital]]
