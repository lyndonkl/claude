# End-to-end DCF case valuations (Disney, Vale, Tata Motors, Baidu, Deutsche Bank)

**Core idea:** Five complete valuations, done at the same date (November 2013, except Deutsche Bank), that between them exercise every model in the toolkit: a three-stage FCFF valuation of a mature firm with a moat (Disney), a single-stage FCFF valuation of a normalized commodity cyclical (Vale), a two-stage FCFE valuation of an emerging-market firm valued in local currency (Tata Motors), a changing-margin FCFF valuation of a high-growth firm (Baidu), and a dividend/regulatory-capital valuation of a bank in and out of crisis (Deutsche Bank). Studying them together shows what actually differs between valuations — the model choice, the growth period, the terminal assumptions — and what never differs: the discipline that growth must be earned by reinvestment and that only excess returns create value.

**Formulas:** All five assemble the same skeleton, differing only in which slot is filled:
- `Value of operating assets = SUM over t of FCFF_t/(1+WACC_t)^t + Terminal value/(1+WACC)^N` (Disney, Vale, Baidu)
- `Value of equity = SUM over t of FCFE_t/(1+k_e)^t + Terminal equity value/(1+k_e)^N` (Tata Motors, Deutsche Bank 2016)
- `Value of equity = SUM of PV(Dividends) + PV(Terminal value)` (Deutsche Bank 2008)
- `g = Reinvestment rate × ROC` in the explicit period; `Reinvestment rate = g/ROC` (or payout = `1 − g/ROE`) in the terminal period.
- Bridge (firm valuations): `Operating assets + cash + non-operating assets − debt − minority interests = equity; − options; / shares`.
- `WACC_t = k_e,t × (1 − DebtRatio_t) + k_d × (1 − t) × DebtRatio_t`, with the beta and debt ratio drifting toward mature levels over the transition years.

**Procedure (the common template these five follow):**
1. Cleanse the base year (capitalize leases and R&D; normalize if the year is unrepresentative).
2. Compute the base-year cash flow and the base-year reinvestment rate and ROC.
3. Build the cost of capital: bottom-up beta from business mix, ERP weighted by revenue geography, cost of debt from the rating, market-value weights.
4. Choose the growth period from the strength and durability of the competitive advantage.
5. Set growth in the explicit period as `reinvestment rate × ROC`, and fade growth, ROC, beta, debt ratio and the cost of capital to mature levels over the transition.
6. Set terminal inputs: `g` at or below the riskfree rate, a defensible perpetual ROC, and reinvestment forced to `g/ROC`.
7. Discount, bridge to equity, divide by shares, and compare to price.

**Reference data:**

Growth-period choice, justified case by case:
| Criterion | Disney | Vale | Tata Motors | Baidu |
|---|---|---|---|---|
| Size / market | Among the largest in entertainment and theme parks, but businesses being redefined and expanding | One of the largest miners globally; market constrained by resource availability | Large share of India, small globally; growth from Jaguar/Land Rover in emerging markets | Growing sector (online search) in a growing market (China) |
| Current excess returns | Earns more than its cost of capital | Returns track commodity prices; generally above cost of capital | ROC above cost of capital | Significant excess returns |
| Competitive advantage | Some of the most recognized brands in the world; Marvel, Pixar, Star Wars | Cost advantage from low-cost Brazilian iron ore reserves | Wide Indian distribution/service network but fading; Jaguar/Land Rover brand gives pricing power | Early entry and knowledge of China plus government-imposed barriers to outsiders |
| **High-growth period** | **10 years** (strong competitive advantages) | **None** (normalized earnings, moderate excess returns) | **5 years** (growth mostly from outside India) | **10 years** (strong excess returns) |

Disney's three-phase input table (November 2013):
| Input | High growth (yrs 1–5) | Transition (yrs 6–10) | Stable (after yr 10) |
|---|---|---|---|
| Tax rate | 31.02% effective / 36.1% marginal | same | same |
| Return on capital | 12.61% | declines linearly to 10% | 10% |
| Reinvestment rate | 53.93% | declines gradually to 25% | 25% (= g/ROC = 2.5/10) |
| Expected EBIT growth | 6.8% (= 0.5393 × 0.1261) | linear decline to 2.5% | 2.5% |
| Debt/capital | 11.5% | rises linearly to 20% | 20% |
| Risk | Beta 1.0013, k_e 8.52%, pre-tax k_d 3.75%, WACC 7.81% | beta -> 1.00, WACC declines to 7.29% | beta 1.00, k_e 8.51%, WACC 7.29% |

Disney's cost-of-capital path, year by year: 7.81% for years 1–5, then 7.71%, 7.60%, 7.50%, 7.39%, 7.29% as the debt ratio walks from 11.5% to 20%.

**Worked examples:**

*Disney, November 2013 ($ millions).* Base: EBIT(1−t) = 10,032 × (1 − 0.31) = 6,920; net cap ex 3,629; ΔWC 103; FCFF 3,188; reinvestment rate 53.93%; ROC 12.61% -> growth 6.8%. Cost of equity 8.52% (riskfree 2.75% + beta 1.0013 × ERP 5.76%, beta built from an unlevered sector beta of 0.9239 at D/E 13.10%); after-tax cost of debt (2.75% + 1.00%) × (1 − 0.361) = 2.40% on an A rating; weights E 88.5% / D 11.5% -> WACC 7.81%.
| Year | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| EBIT(1−t) | 7,391 | 7,893 | 8,430 | 9,003 | 9,615 | 10,187 | 10,704 | 11,156 | 11,531 | 11,819 |
| Reinvestment | 3,985 | 4,256 | 4,546 | 4,855 | 5,185 | 4,904 | 4,534 | 4,080 | 3,550 | 2,955 |
| FCFF | 3,405 | 3,637 | 3,884 | 4,148 | 4,430 | 5,283 | 6,170 | 7,076 | 7,981 | 8,864 |

Terminal: `g` 2.5%, ROC 10%, reinvestment 25%, WACC 7.29% -> terminal EBIT(1−t) 10,639, reinvestment 2,660, FCFF 7,980, `TV = 7,980/(0.0729 − 0.025) = 165,323`. Bridge: operating assets 125,477 + cash 3,931 + non-operating investments 2,849 − debt 15,961 − minority interests 2,721 = equity 113,575; − options 972 = 112,603; / shares = **$62.56 per share** versus a price of **$67.71** — modestly overvalued.

*Disney restructured.* Pull the value levers: more selective acquisitions and a gaming payoff raise ROC to **14%** and cut the reinvestment rate to **50%**, so growth rises to `0.50 × 0.14 = 7%`; move to the optimal debt ratio of **40%** (D/E 66.67%), which raises beta to 1.3175 and the cost of equity to 10.34% but cuts the WACC to `8.52% × 0.60 + 2.40% × 0.40 = 7.16%`, declining to 6.76% in stable growth. Terminal FCFF 9,206, `TV = 9,206/(0.0676 − 0.025) = 216,262`; operating assets 147,704 -> **$74.91 per share**. Restructuring adds roughly **$12 per share** — a direct measurement of the value of better investment and financing decisions.

*Vale, November 2013 ($ millions) — stable growth, no high-growth period.* Normalized EBIT 17,626, normalized effective tax rate 20.92%, normalized ROC 17.25% (from 2009–2013). Bottom-up unlevered beta 0.844 from four businesses (metals & mining 0.86, iron ore 0.83, fertilizers 0.99, logistics 0.75, weighted by segment value from peer EV/Sales multiples); levered at D/E 54.99% with a 34% Brazilian marginal rate -> beta 1.15. ERP 7.38%, revenue-weighted by geography (China 37.0% at 6.94%, Europe 17.2% at 6.72%, Brazil 16.9% at 8.50%, Japan 10.3% at 6.70%, rest of Asia 8.5% at 8.61%, US & Canada 4.9% at 5.50%, rest of LatAm 1.7% at 10.09%, rest of world 3.5% at 10.06%). Cost of equity 10.87%; pre-tax cost of debt 2.75% + 1.30% = 4.05% (A− rating); WACC 8.20% at weights E 64.52% / D 35.48%. Stable `g` = 2% -> reinvestment rate `2%/17.25% = 11.59%`.
```
Value of operating assets = 17,626 × (1 − 0.2092) × (1 − 0.1159) / (0.082 − 0.02) = 202,832
+ cash 7,133 − debt 42,879 = equity 167,086 -> $32.44 per share vs price $13.57
```
The model calls Vale deeply undervalued.

*Baidu, November 2013 (yuan millions) — changing margins.* Base revenues 28,756, EBIT 14,009 (48.72% margin), sales-to-capital 2.64. Revenue growth 25% for five years tapering to 3.5% by year 10; operating margin **declining** from 48.72% to a 35% target as competition arrives; effective tax rate rising from 16.31% to 25%; `Reinvestment_t = ΔRevenue_t/2.64`; `FCFF_t = EBIT_t(1−t) − Reinvestment_t`.
| Year | 1 | 3 | 5 | 7 | 10 |
|---|---|---|---|---|---|
| Revenues | 35,945 | 56,164 | 87,756 | 123,293 | 154,207 |
| Margin | 47.35% | 44.60% | 41.86% | 39.12% | 35.00% |
| EBIT(1−t) | 14,243 | 20,965 | 30,743 | 38,685 | 40,479 |
| Reinvestment | 2,722 | 4,253 | 6,646 | 6,577 | 1,974 |
| FCFF | 11,521 | 16,712 | 24,097 | 32,107 | 38,505 |

Cost of equity 12.91% (3.5% + beta 1.356 × ERP 6.94%, beta from an unlevered 1.30 at D/E 5.52%); after-tax cost of debt (3.5% + 0.8% + 0.3%) × (1 − 0.25) = 3.45%; WACC 12.42% falling to 10% over years 6–10. Terminal: `g` 3.5%, WACC 10%, ROC 15% -> reinvestment rate 23.33%; terminal EBIT(1−t) 41,896 − reinvestment 9,776 = FCFF 32,120; `TV = 32,120/(0.10 − 0.035) = 494,159`. Operating assets 291,618 + cash 43,300 − debt 20,895 = equity 314,023; / 2,088.87m shares = **¥150.33** versus a price of **¥160.06** — roughly fairly valued.

*Tata Motors, November 2013 (Rs millions) — FCFE in rupees.* Growth `= ROE 29.97% × equity reinvestment rate 80.50% = 24.13%` for five years. Cost of equity 13.50% = rupee riskfree 6.57% + beta 0.964 × ERP 7.19%, where the beta is the **whole-company** beta (operating-asset beta 1.1007 weighted by operating assets 1,428 of a total 1,630, with cash at beta 0) because FCFE includes interest income from cash.
| | Yr 1 | Yr 2 | Yr 3 | Yr 4 | Yr 5 |
|---|---|---|---|---|---|
| Net income | 122,794 | 152,420 | 189,194 | 234,841 | 291,500 |
| Equity reinvestment (80.5%) | 98,845 | 122,693 | 152,295 | 189,039 | 234,648 |
| FCFE | 23,949 | 29,727 | 36,899 | 45,802 | 56,852 |
| PV at 13.5% | 21,100 | 23,075 | 25,235 | 27,597 | 30,180 |

Sum of PVs = 127,187. Stable phase: beta -> 1, ERP falls to 6.98% as the firm globalizes, so `k_e = 6.57% + 6.98% = 13.55%`; `g` = 6%; ROE = 13.55% (no excess returns); equity reinvestment rate `= 6%/13.55% = 44.28%`. Year-6 FCFE = `291,500 × 1.06 × (1 − 0.4428) = 136,822`; `Terminal value = 136,822/(0.1355 − 0.06) = 2,280,372`. Equity = `127,187 + 2,280,372/1.1355^5 = 742,008`; / 2,694.08m shares = **Rs 275.42** versus a price of **Rs 427.85** — roughly 40% overvalued.

*Deutsche Bank, January 2008 (dividend discount model, EUR millions).* Normalized net income 3,954 (average 2003–07); dividends 2,146 -> payout 54.28%; normalized ROE 11.81%; `g = (1 − 0.5428) × 0.1181 = 5.4%`; cost of equity `= 4.00% + 1.162 × 4.5% = 9.23%`.
| Year | 2008 | 2009 | 2010 | 2011 | 2012 |
|---|---|---|---|---|---|
| Net income | 4,167 | 4,392 | 4,629 | 4,879 | 5,143 |
| Dividends (54.28%) | 2,262 | 2,384 | 2,513 | 2,648 | 2,791 |
| PV at 9.23% | 2,071 | 1,998 | 1,928 | 1,861 | 1,795 |

Sum = 9,653. Stable: cost of equity 8.5% (beta -> 1), ROE 8.5% (zero excess returns), `g` 3% -> payout `1 − 0.03/0.085 = 64.71%`; year-6 dividend `5,143 × 1.03 × 0.6471 = 3,427`; `TV = 3,427/(0.085 − 0.03) = 62,318`; `PV(TV) = 62,318/1.0923^5 = 40,079`. Equity = 9,653 + 40,079 = **49,732**; / 474.2m shares = **EUR 104.88** versus a price of **EUR 89** — modestly undervalued.

*Deutsche Bank, October 2016 (crisis FCFE for a bank, $ millions).* Dividends had stopped and the bank was losing money, so potential dividends are estimated as FCFE after investment in regulatory capital: project risk-adjusted assets growing 1%/yr from 445,570; raise the Tier 1 capital ratio from 12.41% to 15.67% (the 75th percentile of banks) by year 10; treat the increase in Tier 1 capital as reinvestment; project net income as book equity × an ROE recovering from −13.70% to 5.85% (25th percentile) by year 5 and 9.44% (= cost of equity) by year 10; deduct an expected $10bn DOJ fine from Tier 1 capital today. Year 1: Tier 1 rises 55,282 -> 61,834, so reinvestment 6,552; net income −5,111; **FCFE = −11,663**. FCFE turns positive in year 5 (+2,874) and reaches 6,352 by year 10; terminal equity value 87,317; equity value today 31,838.74; / 1,386m shares = **$22.97** DCF value per share. Applying a **10% probability of equity wipeout** gives `22.97 × 0.90 = $20.67` versus a price of **$13.33** on 3 October 2016.

**Determinism:**
- DETERMINISTIC: every number above, given the assumption set — the year-by-year cash flows, the discounting with a changing cost of capital, the terminal value, the bridge to equity and the per-share value. Also the restructured-Disney re-run once the new ROC, reinvestment rate and debt ratio are chosen.
- JUDGMENT: the model choice for each firm; the length of the growth period (mapped from qualitative moat assessments); the normalization windows; the target margins and ROCs; the ERP weights by revenue geography; the stable-phase beta, debt ratio and excess returns; the probability of equity wipeout for a distressed bank; and, for the restructured case, whether management will actually pull the levers.

**Pitfalls:**
- Using the operating-asset beta to discount FCFE that already contains interest income from cash (Tata Motors explicitly recomputes a whole-company beta of 0.964 from the operating-asset beta of 1.1007 for this reason).
- Applying a standard FCFE formula to a bank instead of the regulatory-capital reinvestment definition.
- Valuing a commodity cyclical off trailing earnings rather than normalized earnings — Vale's 2011 ROC was 28.01% and its 2009 ROC was 9.10%.
- Giving a high-growth period to a firm that has already matured (Vale gets none).
- Forgetting that a rising debt ratio through the transition lowers the WACC year by year, which must be reflected in a cumulative discount factor.
- Mixing currencies: Tata Motors is valued entirely in rupees, with a rupee riskfree rate and a rupee ERP.
- Reading a value/price gap as a trade without asking which assumption is doing the work. Vale at $32.44 vs $13.57 is a bet on normalized iron-ore economics, nothing else.
- Presenting a restructured value as the current value. $74.91 is what Disney is worth *if* management changes behaviour; $62.56 is what it is worth as run.

**Sources:**
- cfpacket2spr20 p.224-233, p.236-267 (valuation section opener, first principles, three approaches to valuation, DCF structure, equity vs firm valuation, choosing a cash flow, stories and numbers, ingredients of value, cash-flow estimation, Deutsche Bank dividends and regulatory-capital FCFE, Tata Motors FCFE, Disney FCFF, discount rates for all cases, changing costs of capital, growth estimation for all cases, growth-period choice, Vale full valuation, Disney stable-period inputs, per-share bridge, Deutsche Bank 2008 and 2016 valuations, Tata Motors valuation, Baidu valuation, Disney inputs and valuation picture, corporate-finance tie-in, ways of changing value, restructured Disney, closing first principles)
- valpacket1spr21 p.203 (Heineken, a sixth fully worked DCF in a negative-riskfree-rate currency)
- valpacket1spr21 p.212, p.217 / valpacket1spr20 p.208, p.213 (summarizing the inputs; the building blocks)

**Related:** [[dcf-model-choice-framework]], [[fcff]], [[fcfe]], [[terminal-value]], [[fundamental-growth-operating]], [[fundamental-growth-equity]], [[top-down-revenue-growth]], [[normalizing-depressed-earnings]], [[return-on-invested-capital]], [[value-of-growth]], [[fcff-forecast-engine]], [[bottom-up-beta]], [[country-risk-premium]], [[cost-of-capital]], [[bank-valuation]], [[equity-value-bridge]]
