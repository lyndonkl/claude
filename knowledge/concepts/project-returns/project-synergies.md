# Project synergies and side benefits

**Core idea:** A project can make the firm's *other* businesses more valuable. A Disney animated movie costing $50 million generates merchandise, higher theme-park attendance, stage shows, and TV series far beyond its box office. A café inside a bookstore sells coffee and also sells more books. Netflix Fit brings new subscribers to Netflix's entertainment service. These side benefits are real, and they are routinely abused: managers invoke unquantified "synergy" late in the process to override a negative NPV. The discipline is to value the synergy explicitly, as incremental cash flows, in the *original* analysis — and to discount each synergy stream at the cost of capital of the business that receives it, not at the project's rate.

**Formulas:** Symbols: `r_receiving` = cost of capital of the business that receives the synergy; `g` = perpetual growth rate; `n` = years until the synergy begins.
- `Synergy cash flow_t = Incremental revenue in the other business_t × pre-tax operating margin × (1 − tax rate)`
- `PV of synergy = Σ_t Synergy CF_t / (1 + r_receiving)^t`
- Delayed perpetual synergy: `Value at year n = CF_{n+1} / (r_receiving − g)`; `Value today = Value at year n / (1 + r_receiving)^n`
- `Total NPV = Stand-alone NPV + PV of synergy benefits`
- Acquisition ceiling: `Maximum price = Stand-alone value of target + Value of synergy`

**Procedure:**
1. Name the synergy concretely: which other business gains, through what mechanism, starting when.
2. Forecast the incremental revenue (or cost saving) in that other business, year by year.
3. Apply that business's operating margin, then the marginal tax rate, to get after-tax synergy cash flow.
4. Decide the lag. Product adaptation, channel build-out, and integration all take time. Tata's audio synergy needs three years before any cash arrives.
5. Choose the discount rate from the *receiving* business's risk, geography, currency, and financing mix. Netflix Fit's synergy is discounted at Netflix Entertainment's 8.93%, not Netflix Fit's 8.01%.
6. Discount and add to the stand-alone NPV. Report the two numbers separately so a reader can see how much of the case rests on synergy.
7. If the project only clears the bar because of synergy, say so, and state what has to be true for the synergy to materialize.

**Reference data:** Common Disney project synergies from a single animated movie: merchandise (toys, figures, clothes), increased theme-park attendance, stage shows (Beauty and the Beast, Lion King), and TV series based on the movie.

Netflix Fit synergy assumptions (2020 case): the fitness service raises regular streaming subscription revenue by $500 million in year 1, growing at the 1% inflation rate, at a 15% pre-tax operating margin, taxed at 25%.

**Worked example:** Three cases.

*1. Bookscape café.* The café standing alone has NPV = **−$87,571** — a reject. But it raises bookstore revenues by $500,000 in year 1, growing 10%/year for four more years, at a 10% pre-tax operating margin, taxed at 40%.

| | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| Increased revenues | $500,000 | $550,000 | $605,000 | $665,500 | $732,050 |
| Operating margin | 10% | 10% | 10% | 10% | 10% |
| Operating income | $50,000 | $55,000 | $60,500 | $66,550 | $73,205 |
| After taxes @40% | $30,000 | $33,000 | $36,300 | $39,930 | $43,923 |
| PV of additional cash flows | $27,199 | $27,126 | $27,053 | $26,981 | $26,908 |

PV of synergy benefits = **$135,268**. Total NPV = −87,571 + 135,268 = **+$47,697**. The café is a good investment, but only as an attachment to the bookstore.

*2. Netflix Fit → Netflix Entertainment.* Synergy cash flows ($ millions):

| Line | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| Additional entertainment revenue | 500.00 | 505.00 | 510.05 | 515.15 | 520.30 | 525.51 | 530.76 | 536.07 | 541.43 | 546.84 |
| Pre-tax operating income @15% | 75.00 | 75.75 | 76.51 | 77.27 | 78.05 | 78.83 | 79.61 | 80.41 | 81.21 | 82.03 |
| After-tax @25% | 56.25 | 56.81 | 57.38 | 57.95 | 58.53 | 59.12 | 59.71 | 60.31 | 60.91 | 61.52 |
| PV @8.93% | 51.66 | 47.92 | 44.45 | 41.23 | 38.25 | 35.48 | 32.91 | 30.52 | 28.31 | 26.26 |

Finite-life PV of synergy = **$376.20 million** against a stand-alone project NPV of $106.37 million. Total NPV = **$482.57 million**. With an infinite life the synergy also earns a terminal value ($783.40 million at year 10), lifting the synergy NPV to $709.20 million and total NPV to $1,074.42 million. The project is marginal alone and comfortable with synergy — which is exactly why the case's recommendation hinges on whether the synergy is believable.

*3. Tata Motors / Harman merger synergy.* Tata plans to fit Harman's high-end speakers and tuners as optional upgrades on new Tata cars in India. Adapting the products takes about three years. From year 4 the synergy generates Rs 10 billion of after-tax operating income, growing 4%/year in perpetuity, India only.

The discount rate is built from the synergy's own characteristics, not Harman's and not Tata's blended rate:
- Business risk: optional add-ons in auto sales → Tata Motors' levered beta of 1.10.
- Geography: India → mature-market premium 5.5% + India country risk premium 3.60%.
- Cost of equity (rupees) = 6.57% + 1.10 × 9.10% = 16.59%.
- After-tax cost of debt (rupees) = 9.6% × (1 − 0.3245) = 6.50%.
- Cost of capital (rupees) = 16.59% × (1 − 0.2928) + 6.50% × 0.2928 = **13.63%**.

Value at end of year 3 = 10,000 / (0.1363 − 0.04) = **Rs 103,814 million**. Value today = 103,814 / 1.1363³ = **Rs 70,753 million**. At Rs 60/$, synergy = **$1,179 million**. Maximum Tata should pay = Harman's stand-alone equity value of $2,678 million + $1,179 million = **$3,857 million**. Harman's equity trades at $5,248 million. Even fully crediting the synergy, the deal destroys value at market price. Walk away.

**Determinism:** DETERMINISTIC — the inputs are a revenue path, a margin, a tax rate, a lag, a growth rate, a discount rate, and an exchange rate. From those a script computes the synergy cash flows, their present value, the combined NPV, and the maximum acquisition price. JUDGMENT — whether the synergy exists at all, its size, its timing, its durability, and which business's risk it carries. That judgment needs the receiving business's margins and competitive position, the integration plan, and an honest estimate of the adaptation lag.

**Pitfalls:**
- Invoking synergy qualitatively to override a negative NPV. If it is real, it can be valued.
- Discounting synergy cash flows at the project's or acquirer's rate rather than the receiving business's rate.
- Ignoring the lag. Synergies that "start immediately" are almost always wrong; Tata's take three years.
- Granting synergies a perpetual growth rate without asking whether the advantage lasts.
- Counting a synergy on the benefit side while ignoring cannibalization on the cost side. See [[opportunity-costs-and-side-costs]].
- Reporting only the combined NPV, hiding how much of the case rests on synergy. Netflix Fit is $106 million alone and $483 million with synergy.

**Sources:**
- corporate_finance--lecture_slides--cfpacket1spr20 p.305
- corporate_finance--lecture_slides--cfpacket1spr20 p.316-320
- corporate_finance--case--netflixfit p.5
- corporate_finance--case--netflixfitpresentation p.3
- corporate_finance--case--netflixfitpresentation p.12-13
- corporate_finance--case--netflixfitpresentation p.19

**Related:** [[opportunity-costs-and-side-costs]], [[acquisitions-as-projects]], [[project-hurdle-rate-selection]], [[incremental-cash-flow-principle]], [[terminal-value-and-project-life]], [[netflix-fit-case]], [[country-risk-premium]]
