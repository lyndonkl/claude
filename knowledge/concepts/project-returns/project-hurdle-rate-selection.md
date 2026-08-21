# Selecting the project hurdle rate

**Core idea:** A project's hurdle rate must match four things about the cash flows it discounts: the claimholder, the business risk, the geography, and the currency. Claimholder first — cash flows to the firm get the cost of capital; cash flows to equity get the cost of equity. Business risk next — use the rate for the business the project is *in*, not the company average. A company-wide rate systematically overfunds risky divisions and starves safe ones. Geography third — a project in an emerging market carries political risk that a globally diversified investor cannot fully shed, so a country risk premium is added to the mature-market equity risk premium. Currency last — the rate must be denominated in the cash flows' currency. The Rio Disney project needs none of the six candidate rates on the slide, because none combines theme-park risk with Brazil exposure until the adjustment is made.

**Formulas:** Symbols: `E` = market value of equity; `D` = market value of debt; `t` = marginal tax rate; `ERP` = equity risk premium; `CRP` = country risk premium.
- `Cost of capital = Cost of equity × E/(D+E) + Pre-tax cost of debt × (1 − t) × D/(D+E)`
- `Cost of equity = Riskfree rate + Levered beta × Total ERP`
- `Total ERP for a project = Mature market premium + CRP`, where `CRP = country default spread × relative equity market volatility`
- Multi-region ERP: `Project ERP = Mature market premium + Σ_regions (revenue weight_region × CRP_region)`
- `Levered beta = Unlevered beta × [1 + (1 − t) × D/E]`
- Total-beta variant for undiversified private owners: `Total beta = Market beta / correlation with the market`

**Procedure:**
1. Identify the claimholder whose returns you are measuring. ROC and cash flow to the firm → cost of capital. ROE and cash flow to equity → cost of equity. Never mix.
2. Identify the business. Take the unlevered (bottom-up) beta from firms operating in that business, not from the parent company's regression beta.
3. If the owner is undiversified (a private business), use a total beta rather than a market beta. Bookscape's cost of capital is 6.57% on a market beta and 10.30% on a total beta — a 3.7-point gap that flips its ROC verdict from positive to negative.
4. Build the equity risk premium from the project's geographic revenue exposure, weighting regional country risk premiums by revenue share.
5. Choose the debt ratio. Default to the division's or the target's own debt ratio, not the parent's, when that financing will actually be used.
6. Use the marginal tax rate to compute the after-tax cost of debt.
7. Convert the rate to the cash flows' currency using the inflation differential. See [[currency-and-inflation-consistency]].
8. For an acquisition, use the *target's* risk characteristics throughout — beta, ERP, debt ratio, cost of debt. See [[acquisitions-as-projects]].
9. For a synergy stream, use the risk of the business that *receives* the synergy, and the geography where it arises.

**Reference data:**

Disney divisional costs of capital (cost of debt 3.75%, marginal tax rate 36.10%, after-tax cost of debt 2.40% for all divisions):

| Division | Cost of equity | Debt ratio | Cost of capital |
|---|---|---|---|
| Media Networks | 9.07% | 9.12% | 8.46% |
| Parks & Resorts | 7.09% | 10.24% | 6.61% |
| Studio Entertainment | 9.92% | 17.16% | 8.63% |
| Consumer Products | 9.55% | 53.94% | 5.69% |
| Interactive | 11.65% | 29.11% | 8.96% |
| **Disney Operations** | **8.52%** | **11.58%** | **7.81%** |

The spread from 5.69% to 8.96% across divisions is why a single company rate misallocates capital.

Other worked hurdle rates from the same vintage:

| Entity | Rate | Note |
|---|---|---|
| Tata Motors (rupees) | 12.15% | 14.49%×(1−0.2928) + 6.50%×0.2928 |
| Baidu (RMB) | 12.42% | 12.91%×(1−0.0523) + 3.45%×0.0523 |
| Bookscape, market beta | 6.57% | Assumes a diversified owner |
| Bookscape, total beta | 10.30% | Assumes an undiversified owner (correct for a private firm) |
| Bookscape Online venture | 18.12% | Unlevered total beta 3.02 from online retailers, relevered to D/E 21.41% |
| Rio Disney project | 8.46% (US$) | Theme parks 6.61% + Brazil risk |
| Vale iron ore (US$ cost of equity) | 11.13% | Equity-side hurdle rate |
| Harman standalone (US$) | 9.67% | Target's own beta, ERP, debt ratio |
| Tata/Harman synergy (rupees) | 13.63% | Tata's beta, India CRP, rupee financing |
| Netflix Fit | 8.01% | Fitness comps' beta, Netflix's D/E |
| Netflix Entertainment | 8.93% | Netflix's own beta 1.29 |

Rio Disney build-up, step by step:
- Theme-park cost of capital in a mature market: 6.61%, from a bottom-up levered beta of 0.7537.
- Brazil country risk premium: 3% (default spread scaled by relative equity volatility). Total ERP = 5.5% + 3% = 8.5%.
- Cost of equity in US$ = 2.75% + 0.7537 × 8.5% = 9.16%.
- Cost of capital in US$ = 9.16% × 0.8976 + 2.40% × 0.1024 = **8.46%**.

Netflix Fit build-up (2020 case):
- Fitness comparables: median regression beta 1.25, median D/E 34.92%, median cash/value 5.26%.
- Unlevered beta = 1.25/(1 + 0.75 × 0.3492) = 0.99. Corrected for cash: 0.99/(1 − 0.0526) = 1.0495.
- Netflix market equity = $368.77 × 438.81M shares = $161,820M. Market debt including lease PV = $16,888M. D/E = 10.44%, D/C = 9.45%.
- Relevered beta = 1.0495 × (1 + 0.75 × 0.1044) = 1.1274.
- Cost of equity = 1.50% + 1.1274 × 6.27% = 8.57%. Pre-tax cost of debt = 1.50% + 2.00% (Ba3 spread) = 3.50%.
- Cost of capital = 8.57% × 0.9055 + 3.50% × 0.75 × 0.0945 = **8.01%**.

Harman revenue-weighted equity risk premium (acquisition target):

| Region | Revenues 2012-13 ($M) | ERP | Weight | Weight × ERP |
|---|---|---|---|---|
| United States | $1,181 | 5.50% | 27.48% | 1.51% |
| Germany | $1,482 | 5.50% | 34.48% | 1.90% |
| Rest of Europe | $819 | 7.02% | 19.06% | 1.34% |
| Asia | $816 | 7.27% | 18.99% | 1.38% |
| **Harman** | **$4,298** | | **100.00%** | **6.13%** |

**Worked example:** Rio Disney's benchmark question. The project's average return on capital is 4.18%. Which rate should it face? Candidates offered: the 2.75% riskfree rate, Disney's 8.52% company cost of equity, the 7.09% theme-park cost of equity, the 7.81% company cost of capital, or the 6.61% theme-park cost of capital. All five are wrong. ROC measures returns to all capital, ruling out both cost-of-equity numbers and the riskfree rate. The company-wide rate ignores that this is a theme park, not a media network. The theme-park rate ignores Brazil. The correct rate is the theme-park cost of capital re-estimated with a Brazil country risk premium: **8.46%**. Against that benchmark the project's 4.18% accounting return fails, though the cash-flow analysis over the project's true life passes.

**Determinism:** DETERMINISTIC — the inputs are an unlevered beta, a debt-to-equity ratio, a tax rate, a riskfree rate, regional ERPs with revenue weights, a cost of debt, and a debt ratio. From those a script computes the levered beta, cost of equity, after-tax cost of debt, and cost of capital, in any currency. JUDGMENT — choosing the comparable-firm sample, deciding whether to use a market or total beta, estimating the country risk premium, picking the debt ratio, and deciding the project's business classification. That judgment needs comparable-company data, sovereign ratings or CDS spreads, relative equity volatility, and the geographic revenue split.

**Pitfalls:**
- Applying one company-wide hurdle rate to every project. Disney's divisional rates range across 3.3 percentage points.
- Using the acquirer's cost of capital to value a target. The rate must reflect the target's risk.
- Using a market beta for a private business whose owner is undiversified.
- Charging a country risk premium for a mature-market project, or for currency risk that is diversifiable.
- Discounting a synergy stream at the project's rate rather than the receiving business's rate.
- Forgetting to convert the rate to the cash flows' currency.
- Treating the hurdle rate as precise. Roughly 45 student groups analyzing Netflix Fit produced costs of capital from below 6% to above 9%, clustering at 8–8.5%.

**Sources:**
- corporate_finance--lecture_slides--cfpacket1spr20 p.201-204
- corporate_finance--lecture_slides--cfpacket1spr20 p.221-224
- corporate_finance--lecture_slides--cfpacket1spr20 p.264
- corporate_finance--lecture_slides--cfpacket1spr20 p.278
- corporate_finance--lecture_slides--cfpacket1spr20 p.309
- corporate_finance--lecture_slides--cfpacket1spr20 p.319
- corporate_finance--case--netflixfit p.3
- corporate_finance--case--netflixfit p.5-6
- corporate_finance--case--netflixfit p.9
- corporate_finance--case--netflixfit p.11-14
- corporate_finance--case--netflixfitpresentation p.4-5
- corpfin-ratings-risk (ratings.xls synthetic rating tables; riskchecker.xls country and regional risk premiums)

**Related:** [[currency-and-inflation-consistency]], [[accounting-returns-roc-roe-eva]], [[equity-side-project-analysis]], [[acquisitions-as-projects]], [[project-synergies]], [[netflix-fit-case]], [[cost-of-capital]], [[bottom-up-beta]], [[country-risk-premium]], [[synthetic-rating]], [[total-beta]]
