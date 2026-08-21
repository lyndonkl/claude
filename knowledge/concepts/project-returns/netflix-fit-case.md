# Netflix Fit: the full worked investment analysis case

**Core idea:** Netflix Fit is Damodaran's end-to-end investment-analysis case (Spring 2020). US subscriber growth is plateauing, and Netflix considers a Peloton-modeled fitness business selling exercise equipment plus a video subscription. The case exercises every part of project analysis in one place. On the cash-flow side: sunk R&D, allocated versus incremental overhead, excess capacity, and working capital. On the discount-rate side: a revenue-weighted equity risk premium and a bottom-up beta from comparable firms. On top of both: synergy with the parent business discounted at the parent's rate, and a finite-versus-infinite life comparison. The answer is deliberately marginal. Stand-alone, the project barely clears its hurdle. Counting synergy it clears comfortably. Extending the life to perpetuity makes it look far better still. The recommendation: leave the business to niche players like Peloton unless Netflix can increase the side benefits to its entertainment business.

**Formulas:** Symbols: `t` = marginal tax rate (25%); `r_Fit` = Netflix Fit cost of capital (8.01%); `r_Ent` = Netflix Entertainment cost of capital (8.93%); `g` = inflation (1%).
- `Total market_t = 20 million × (1.02)^t`; `Subscribers_t = Total market_t × market share_t`; `New subscribers_t = Subscribers_t − Subscribers_{t−1}` plus replacement buyers after year 5
- `Straight-line depreciation = (2,400 − 400)/10 = $200 million per year`
- `Net working capital_t = (5% AR + 10% inventory − 5% AP) × Equipment revenues_t = 10% × Equipment revenues_t`
- `Incremental advertising_t = 6% × 2,000 × (1.05)^t`
- `Project ERP = 5.25% + Σ_regions (revenue weight × regional CRP) = 6.27%`
- `FCFF_t = After-tax incremental operating income_t + Depreciation_t − CapEx_t − Maintenance capex_t + tax benefit of depreciation on maintenance_t − ΔNWC_t − Studio investment_t + tax benefit of incremental studio depreciation_t + Salvage/terminal value_t`
- `Terminal value = CF_11 / (r_Fit − g) = 244.33 / (0.0801 − 0.01) = $3,486 million`
- `Total NPV = NPV(FCFF at r_Fit) + NPV(synergy at r_Ent)`

**Procedure (how the case is solved):**
1. **Classify the given costs.** The $250 million of already-expensed fitness R&D is sunk — exclude it. The 4% allocation of existing firm-wide G&A ($1.5 billion growing 5%/yr with or without the project) is not incremental — exclude it. The separate $50 million of new G&A in year 1, growing with divisional revenues, *is* incremental — include it. Incremental advertising is the 6% uplift on the counterfactual advertising path.
2. **Build the revenue model.** Total market 20 million subscribers growing 2%/yr. Netflix share ramps 5%, 10%, 15%, 20%, 25% over years 1–5 and holds at 25%. Every new subscriber buys a bike or treadmill at $1,000 (cost $400), both growing with inflation. Equipment lasts five years, so subscribers past year 5 repurchase. Subscription revenue is $120/yr per subscriber, servicing cost $24/yr, both inflation-indexed. Content costs start at $400 million, grow 10%/yr for five years, then at inflation.
3. **Price the excess capacity.** The Mumbai studio is 40% used by Asian entertainment content growing 20%/yr. Netflix Fit takes 30%. When combined usage hits 100%, a new $500 million studio (inflation-adjusted) is required. In the solution the trigger investment of $520.30 million lands in year 4, with the offsetting saving of the deferred alternative credited in year 6, and only differential depreciation counted.
4. **Compute the cost of capital.** Unlever the fitness comparables' median beta, correct for cash, relever at Netflix's own market D/E, and combine with Netflix's cost of debt and marginal tax rate.
5. **Compute accounting returns.** Build operating income both ways (allocated versus incremental G&A) and divide by book invested capital.
6. **Build FCFF for a 10-year finite life**, recovering working capital and a $400 million salvage in year 10.
7. **Value the synergy separately** and discount it at Netflix Entertainment's rate.
8. **Rebuild for an infinite life**, adding maintenance capex above depreciation and a steady-state terminal value.
9. **Sensitivity-test the renewal rate**, which is the single most important business-model driver.
10. **Recommend**, stating what the decision hinges on.

**Reference data:**

Case facts (Spring 2020):

| Fact | Value |
|---|---|
| Sunk R&D already expensed | $250 million, unrecoverable |
| Up-front investment (t=0) | $2.4 billion, straight line over 10 yrs to $400 million salvage |
| Total addressable market | 20 million, growing 2%/yr in perpetuity |
| Market share path | 5% yr 1, +5 pts/yr to 25% by yr 5, held thereafter |
| Equipment | $1,000 price, $400 cost, inflation-indexed, 5-year life |
| Subscription | $120/yr, servicing cost $24/yr, inflation-indexed |
| Content costs | $400M yr 1, +10%/yr for 5 yrs, then inflation |
| Studio | Mumbai studio 40% used, entertainment usage growing 20%/yr; Fit takes 30%; new studio $500M at inflation |
| Allocated G&A | 4% of existing $1.5B G&A (growing 5%/yr) — not incremental |
| Incremental G&A | $50M yr 1, growing with divisional revenues |
| Advertising | $2B most recent year, +5%/yr baseline; with Fit, 6% higher in yrs 1–10 |
| Working capital | AR 5% + inventory 10% − AP 5% = 10% of equipment revenues, invested at start of year |
| Synergy | +$500M entertainment subscription revenue yr 1, inflation-indexed, 15% pre-tax margin |
| Netflix beta (regression) | 1.29 (weekly, 2 yrs; std error 0.194, R² 0.301) |
| Stock price / shares | $368.77 × 438.81M shares = $161.8 billion market equity |
| Debt | $14.759B book interest-bearing (avg maturity 4 yrs) + capitalized leases |
| Rating / spread | Ba3 / 2.00% |
| Tax rates | Effective 10%, **marginal 25%** (use marginal) |
| Riskfree rate / inflation | 1.50% / 1.0% |
| Mature market ERP | 5.25% |

Geographic revenue split and regional country risk premiums (over the mature-market premium):

| Region | % of revenues | Weighted average CRP | Contribution |
|---|---|---|---|
| Africa | 5% | 4.69% | 0.235% |
| Asia | 15% | 1.01% | 0.152% |
| Australia & New Zealand | 5% | 0.00% | 0.000% |
| Central and South America | 10% | 3.28% | 0.328% |
| Eastern Europe & Russia | 5% | 2.14% | 0.107% |
| Middle East | 5% | 1.57% | 0.079% |
| North America | 40% | 0.00% | 0.000% |
| Western Europe | 15% | 0.81% | 0.122% |
| **Total** | **100%** | | **≈1.02%** |

Project ERP = 5.25% + 1.02% = **6.27%**.

Fitness comparables (selected rows from the 43-company sample of publicly traded developed-market fitness and sporting-goods firms; market cap, total debt including leases, and cash in $ millions):

| Company | Industry | Market cap | Debt incl. leases | Cash | Beta |
|---|---|---|---|---|---|
| Shimano Inc. | Sporting Goods | 12,739.50 | 41.40 | 2,485.10 | 0.90 |
| Yamaha Corporation | Sporting Goods | 8,469.60 | 303.90 | 913.10 | 1.26 |
| Peloton Interactive | Sporting Goods | 8,060.80 | 286.40 | 532.80 | 0.91 |
| Planet Fitness | Gyms/Fitness | 5,659.30 | 1,875.90 | 436.30 | 1.05 |
| Brunswick Corporation | Sporting Goods | 4,313.70 | 1,553.00 | 320.30 | 1.13 |
| Thule Group AB | Sporting Goods | 2,285.20 | 258.30 | 28.70 | 1.24 |
| Technogym S.p.A. | Sporting Goods | 2,087.00 | 130.10 | 84.30 | 0.83 |
| Acushnet Holdings | Sporting Goods | 1,922.00 | 402.30 | 34.20 | 0.93 |
| Basic-Fit N.V. | Gyms/Fitness | 1,824.00 | 1,177.90 | 26.20 | 1.24 |
| Callaway Golf | Sporting Goods | 1,568.80 | 1,006.40 | 106.70 | 1.25 |
| Nautilus, Inc. | Sporting Goods | 82.20 | 36.80 | 11.10 | 1.30 |
| Town Sports, Inc. | Gyms/Fitness | 41.30 | 1,293.30 | 20.90 | 3.68 |

Sample medians used in the solution: regression beta 1.25, D/E 34.92%, cash/value 5.26%. All comparables are assumed to carry a 25% marginal tax rate with lease-inclusive debt.

**Worked example — the full solution:**

*Cost of capital.*
- Unlevered beta = 1.25 / (1 + 0.75 × 0.3492) = **0.99**
- Corrected for cash = 0.99 / (1 − 0.0526) = **1.0495**
- Netflix market debt = PV of leases $15,161M + $1,727M = $16,888M; market equity $161,820M → D/E = 10.44%, D/C = 9.45%
- Relevered beta for Netflix Fit = 1.0495 × (1 + 0.75 × 0.1044) = **1.1274**
- Cost of equity (Fit) = 1.50% + 1.1274 × 6.27% = **8.57%**; Netflix Entertainment (beta 1.29) = 1.50% + 1.29 × 6.27% = **9.59%**
- Pre-tax cost of debt = 1.50% + 2.00% = 3.50%
- **Cost of capital (Fit) = 8.57% × 0.9055 + 3.50% × 0.75 × 0.0945 = 8.01%**
- **Cost of capital (Entertainment) = 9.59% × 0.9039 + 3.50% × 0.75 × 0.0961 = 8.93%**

Across roughly 45 student groups, cost-of-capital estimates ranged from below 6% to above 9%, with the modal bin at 8–8.5%.

*Operating income, allocated versus incremental ($ millions):*

| Line | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| Revenues | 1,120.00 | 1,320.27 | 1,534.87 | 1,764.61 | 2,010.39 | 1,959.49 | 2,070.31 | 2,186.87 | 2,309.46 | 2,438.39 |
| − Equipment COGS | 400.00 | 428.24 | 458.11 | 489.68 | 523.06 | 491.38 | 523.92 | 558.29 | 594.57 | 632.87 |
| − Subscriber servicing | 24.00 | 49.93 | 77.92 | 108.08 | 140.55 | 146.21 | 152.10 | 158.23 | 164.61 | 171.24 |
| − Content costs | 400.00 | 440.00 | 484.00 | 532.40 | 585.64 | 591.50 | 597.41 | 603.39 | 609.42 | 615.51 |
| − Depreciation | 200.00 | 200.00 | 200.00 | 200.00 | 200.00 | 200.00 | 200.00 | 200.00 | 200.00 | 200.00 |
| − Selling and advertising | 126.00 | 132.30 | 138.92 | 145.86 | 153.15 | 160.81 | 168.85 | 177.29 | 186.16 | 195.47 |
| − Allocated G&A | 65.00 | 68.51 | 72.20 | 76.08 | 80.17 | 83.90 | 88.12 | 92.55 | 97.20 | 102.09 |
| Operating income | −95.00 | 1.29 | 103.73 | 212.51 | 327.82 | 285.69 | 339.90 | 397.12 | 457.50 | 521.21 |
| After-tax @25% | −71.25 | 0.97 | 77.80 | 159.38 | 245.86 | 214.27 | 254.92 | 297.84 | 343.13 | 390.90 |

Replacing allocated G&A ($65.00 in year 1) with incremental G&A ($50.00 in year 1; identical from year 2) raises year-1 operating income from −$95.00 to −$80.00 and after-tax income from −$71.25 to −$60.00. The after-tax incremental series used downstream is: −60.00, 8.14, 80.55, 157.36, 238.68, 211.59, 251.70, 294.03, 338.70, 385.83.

*Return on capital.* Invested capital = undepreciated fixed assets + book value of the studio + non-cash working capital.

| Line | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| BV of fixed assets | 2,400.00 | 2,200.00 | 2,000.00 | 1,800.00 | 1,600.00 | 1,400.00 | 1,200.00 | 1,000.00 | 800.00 | 600.00 |
| BV of working capital | 50.00 | 53.53 | 57.26 | 61.21 | 65.38 | 61.42 | 65.49 | 69.79 | 74.32 | 79.11 |
| BV of Netflix studio | 0.00 | 0.00 | 0.00 | 0.00 | 520.30 | 416.24 | 364.21 | 312.18 | 260.15 | 208.12 |
| **Invested capital** | 2,450.00 | 2,253.53 | 2,057.26 | 1,861.21 | 2,185.69 | 1,877.66 | 1,629.70 | 1,381.97 | 1,134.47 | 887.23 |
| ROIC (no synergy) | −2.91% | 0.04% | 3.78% | 8.56% | 11.25% | 11.41% | 15.64% | 21.55% | 30.25% | 44.06% |
| Incremental ROIC (no synergy) | −2.45% | 0.36% | 3.92% | 8.45% | 10.92% | 11.27% | 15.44% | 21.28% | 29.86% | 43.49% |
| ROIC (with synergy) | −0.61% | 2.56% | 6.57% | 11.68% | 13.93% | 14.56% | 19.31% | 25.92% | 35.61% | 50.99% |

Average ROC over the finite life: **10.76% without synergy, ~14.08% with synergy**, against an 8.01% cost of capital. Note how ROIC climbs mechanically as the asset base depreciates — a book-value artifact, not improving performance. Student estimates were bimodal: 9 groups below 5%, 15 groups above 20%.

*Finite-life FCFF ($ millions).* No capital maintenance, since the business is wrapped up at year 10. Year 0 = −$2,500 ($2,400 capex + $100 initial working capital). Studio investment of $520.30 in year 4; the deferred-investment saving of $541.43 appears as a negative investment (inflow) in year 6. Salvage $400 in year 10.

| Line | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Incremental operating income after taxes | | −60.00 | 8.14 | 80.55 | 157.36 | 238.68 | 211.59 | 251.70 | 294.03 | 338.70 | 385.83 |
| + Depreciation | | 200.00 | 200.00 | 200.00 | 200.00 | 200.00 | 200.00 | 200.00 | 200.00 | 200.00 | 200.00 |
| − Capital expenditures | 2,400.00 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| − Change in non-cash WC | 100.00 | 7.06 | 7.47 | 7.89 | 8.34 | −7.92 | 8.14 | 8.59 | 9.07 | 9.58 | −158.22 |
| − Studio investment | | | | | 520.30 | | −541.43 | | | | |
| + Tax benefit, incremental studio depreciation | | | | | | 13.01 | −0.53 | −0.53 | −0.53 | −0.53 | −0.53 |
| + Salvage value | | | | | | | | | | | 400.00 |
| **FCFF** | **−2,500.00** | **132.94** | **200.68** | **272.66** | **−171.29** | **459.60** | **944.35** | **442.58** | **484.43** | **528.60** | **1,143.52** |
| PV @8.01% | −2,500.00 | 123.08 | 172.02 | 216.40 | −125.87 | 312.68 | 594.84 | 258.11 | 261.57 | 264.26 | 529.28 |

**Stand-alone finite-life NPV = $106.37 million.** IRR = 8.69%.

*Synergy ($ millions).* Additional entertainment revenue $500.00 in year 1 growing 1%/yr to $546.84 in year 10, at a 15% pre-tax margin, taxed at 25%: after-tax income runs $56.25 to $61.52. Discounted at Netflix **Entertainment's** 8.93%, not the project's 8.01%: **NPV of synergy = $376.20 million**. Total finite-life NPV = 106.37 + 376.20 = **$482.57 million**. IRR with synergy = 11.17%.

*Infinite life.* Perpetual growth of 1% requires capital maintenance above depreciation: maintenance capex runs $202.00 in year 1 rising ~1%/yr to $223.13 in year 11, against $200 of depreciation, with an associated tax-benefit line of $33.87 rising to $37.42. That costs roughly $168–187 million of cash flow in every intermediate year. Year-11 steady-state FCFF is $244.33 million — far below year 10, because subscriber growth stops. Terminal value = 244.33 / (0.0801 − 0.01) = **$3,486.43 million**, placed at year 10. Stand-alone infinite-life NPV = **$365.22 million**; synergy with its own terminal value ($783.40 million at year 10) = **$709.20 million**; total = **$1,074.42 million**. IRR = 8.97% stand-alone, 11.53% with synergy.

*Summary of conclusions:*

| Metric | Finite (10 yr) | Infinite |
|---|---|---|
| NPV stand-alone | $106 million | $346–365 million |
| NPV with synergy | $483 million | $1,055–1,074 million |
| IRR stand-alone | 8.69% | 8.97% |
| IRR with synergy | 11.17% | 11.53% |
| Average ROC (no synergy) | 10.76% | — |
| Average ROC (with synergy) | ~14.08% | — |
| Cost of capital | 8.01% | 8.01% |

*Recommendation:* the project adds value, but only marginally on a stand-alone finite-life basis. All numbers assume existing users renew at close to 100%; a lower renewal rate cuts cash flows and NPV. A longer life improves the investment, but technology is a fickle advantage, so the perpetual assumption is generous. Netflix should leave this business to niche players like Peloton unless it can increase the side benefits to its entertainment business. Of 45 student groups, 17 recommended rejection and 28 recommended investing.

**Determinism:** DETERMINISTIC — the stated facts drive everything downstream. A script computes the subscriber path, revenues, all cost lines, and operating income both ways. It computes book capital and ROIC by year. It computes the cost of capital from the comparables and Netflix's own D/E. From those it builds the FCFF stream, the synergy stream, the terminal value, NPV, and IRR. JUDGMENT — the renewal rate, the project life, which costs count as incremental, when the studio capacity binds and how to book the deferred investment, whether the synergy is real, and the accept/reject recommendation. That judgment needs the churn economics of subscription fitness, the durability of the technology advantage, and Netflix's cost-accounting detail on G&A and advertising.

**Pitfalls:**
- Charging the $250 million of sunk R&D to the project.
- Charging the 4% allocated G&A instead of the $50 million of genuinely new G&A.
- Treating the Mumbai studio capacity as free because it is idle today.
- Using Netflix's 10% effective tax rate instead of the 25% marginal rate.
- Using Netflix's own 1.29 regression beta for a fitness business. The bottom-up fitness beta relevered to Netflix's D/E gives 1.1274.
- Discounting the synergy at 8.01% instead of Netflix Entertainment's 8.93%.
- Assuming perpetual life without adding maintenance capex above depreciation.
- Capitalizing year-10 FCFF ($1,143 or $3,917 million) instead of the year-11 steady-state $244.33 million.
- Presenting the with-synergy NPV without the stand-alone number. The whole recommendation turns on that gap.
- Assuming 100% renewal without sensitivity-testing it.

**Sources:**
- corporate_finance--case--netflixfit p.1-14
- corporate_finance--case--netflixfitpresentation p.1-22

**Related:** [[investment-analysis-first-principles]], [[incremental-cash-flow-principle]], [[opportunity-costs-and-side-costs]], [[project-synergies]], [[project-hurdle-rate-selection]], [[accounting-returns-roc-roe-eva]], [[terminal-value-and-project-life]], [[npv-and-irr-mechanics]], [[uncertainty-payback-sensitivity-simulation]], [[earnings-vs-cash-flows]], [[bottom-up-beta]], [[country-risk-premium]], [[operating-lease-capitalization]]
