# Bottom-up beta (and divisional betas)

**Core idea:** Instead of regressing one company's returns against an index, build its beta from the ground up. Identify the businesses the firm operates in, average the betas of many publicly traded firms in each business, unlever those averages, weight them by the value each business contributes to the firm, and relever at the firm's own leverage. This is better than a regression beta for three reasons. Averaging across many firms cuts the standard error by roughly the square root of the sample size. The result reflects the firm's *current or expected* business mix and leverage, not its past. And it can be estimated for companies with no stock price at all — IPOs, private firms, and divisions. The same procedure run at the division level produces divisional costs of equity, which are the correct hurdle rates for projects.

**Formulas:**
- Step 2: **Unlevered beta for a business = Average regression beta across comparable public firms / (1 + (1 − t) × Average D/E across those firms)**.
- Optional cash correction: Business unlevered beta = Company unlevered beta / (1 − Cash/Firm value).
- Step 4: **Bottom-up unlevered beta of the firm = Σ_i (weight_i × unlevered beta_i)**, with weight_i = the share of firm value from business i.
- Step 5: **Levered bottom-up beta = Unlevered beta × (1 + (1 − t) × D/E of the firm)**.
- Business value for weighting = Business revenues × Peer-group EV/Sales multiple.
- Standard error: **Std error of bottom-up beta = Average std error across the comparable-firm betas / sqrt(Number of firms in the sample)**.
- Divisional debt allocation: Division's allocated debt = Total firm debt × (division identifiable assets / total identifiable assets).
- Divisional cost of equity = Riskfree rate + Divisional levered beta × ERP.

**Procedure:**
1. **Identify the businesses** the firm operates in. Use the segment disclosures, but define businesses by economics, not by the filer's labels.
2. **For each business, find publicly traded comparables.** Take the **median** (preferred; more robust than the mean when D/E ratios are extreme) or average of their regression betas, and unlever using the sample's median/average D/E and tax rate. Optionally correct for cash. Optionally adjust for differences between your firm and the comparables in operating leverage and product characteristics (see [[beta-determinants]]).
3. **Estimate the value of each business.** Value weights are correct; revenues or operating income are common shortcuts. The practical method is peer-group EV/Sales × the segment's revenues.
4. **Compute the firm's unlevered beta** as the value-weighted average of the business unlevered betas. If the business mix will change over time, the weights change year by year.
5. **Relever** at the firm's own market debt-to-equity ratio and marginal tax rate. If the D/E ratio is expected to change over the forecast, the levered beta changes with it.
6. **For divisional betas:** allocate the firm's total debt across divisions in proportion to identifiable assets, derive each division's D/E from its allocated debt and its estimated equity value, relever each division's unlevered beta at its own D/E, and compute a divisional cost of equity.
7. **For financial-service firms, do not unlever or relever.** Estimating debt and equity for a bank is, in Damodaran's words, an exercise in futility. Use the median **levered** betas of comparable banks directly and weight them by net revenues.
8. Report the standard error of the bottom-up beta. It should be far smaller than any single regression's.

**Reference data:**

Vale — bottom-up beta from four businesses ($ millions):

| Business | Comparable sample | n | Unlevered beta | Revenues | Peer EV/Sales | Value of business | Share of Vale |
|---|---|---|---|---|---|---|---|
| Metals & Mining | Global metals & mining firms, mkt cap > $1bn | 48 | 0.86 | 9,013 | 1.97 | 17,739 | 16.65% |
| Iron Ore | Global iron ore firms | 78 | 0.83 | 32,717 | 2.48 | 81,188 | 76.20% |
| Fertilizers | Global specialty chemical firms | 693 | 0.99 | 3,777 | 1.52 | 5,741 | 5.39% |
| Logistics | Global transportation firms | 223 | 0.75 | 1,644 | 1.14 | 1,874 | 1.76% |
| **Vale Operations** | | | **0.8440** | **47,151** | | **106,543** | **100.00%** |

Relevered at Vale's D/E of 54.99%, with riskfree rate 2.75% and ERP 7.38%:

| Business | Unlevered beta | D/E | Levered beta | Cost of equity |
|---|---|---|---|---|
| Metals & Mining | 0.86 | 54.99% | 1.1657 | 11.35% |
| Iron Ore | 0.83 | 54.99% | 1.1358 | 11.13% |
| Fertilizers | 0.99 | 54.99% | 1.3493 | 12.70% |
| Logistics | 0.75 | 54.99% | 1.0222 | 10.29% |
| **Vale Operations** | **0.84** | **54.99%** | **1.1503** | **11.23%** |

Disney — unlevered betas by business (November 2013), showing the cash correction:

| Business | Comparables | n | Median beta | Median D/E | Median tax rate | Company unlevered beta | Median Cash/Firm value | Business unlevered beta |
|---|---|---|---|---|---|---|---|---|
| Media Networks | US broadcasting firms | 26 | 1.43 | 71.09% | 40.00% | 1.0024 | 2.80% | 1.0313 |
| Parks & Resorts | Global amusement park firms | 20 | 0.87 | 46.76% | 35.67% | 0.6677 | 4.95% | 0.7024 |
| Studio Entertainment | US movie firms | 10 | 1.24 | 27.06% | 40.00% | 1.0668 | 2.96% | 1.0993 |
| Consumer Products | Global toys/games firms | 44 | 0.74 | 29.53% | 25.00% | 0.6034 | 10.64% | 0.6752 |
| Interactive | Global computer gaming firms | 33 | 1.03 | 3.26% | 34.55% | 1.0085 | 17.25% | 1.2187 |

Disney — value weights and the company unlevered beta:

| Business | Revenues | EV/Sales | Value of business | Share | Unlevered beta |
|---|---|---|---|---|---|
| Media Networks | $20,356 | 3.27 | $66,580 | 49.27% | 1.03 |
| Parks & Resorts | $14,087 | 3.24 | $45,683 | 33.81% | 0.70 |
| Studio Entertainment | $5,979 | 3.05 | $18,234 | 13.49% | 1.10 |
| Consumer Products | $3,555 | 0.83 | $2,952 | 2.18% | 0.68 |
| Interactive | $1,064 | 1.58 | $1,684 | 1.25% | 1.22 |
| **Disney Operations** | **$45,041** | | **$135,132** | **100.00%** | **0.9239** |

Disney also held $3,931m of near-riskless cash (beta 0), so the whole-company unlevered beta = 0.9239 × (135,132/139,063) + 0 × (3,931/139,063) = **0.8978**.

Disney — divisional debt allocation and costs of equity (total debt $15,961m allocated on identifiable assets; riskfree 2.75%, ERP 5.76%):

| Business | Identifiable assets | Allocated debt | Estimated equity | D/E | Unlevered beta | Levered beta | Cost of equity |
|---|---|---|---|---|---|---|---|
| Media Networks | $28,627 | $6,072 | $60,508 | 10.03% | 1.0313 | 1.0975 | 9.07% |
| Parks & Resorts | $22,056 | $4,678 | $41,005 | 11.41% | 0.7024 | 0.7537 | 7.09% |
| Studio Entertainment | $14,750 | $3,129 | $15,106 | 20.71% | 1.0993 | 1.2448 | 9.92% |
| Consumer Products | $7,506 | $1,592 | $1,359 | 117.11% | 0.6752 | 1.1805 | 9.55% |
| Interactive | $2,311 | $490 | $1,194 | 41.07% | 1.2187 | 1.5385 | 11.61% |
| **Disney** | **$75,250** | **$15,961** | **$121,878** | **13.10%** | **0.9239** | **1.0012** | **8.52%** |

Other applications:
- **Embraer**: single business (aerospace), comparable-derived unlevered beta 0.95, D/E 18.95%, tax rate 34% → levered beta = 0.95 × (1 + 0.66 × 0.1895) = **1.07**. Yes, US and European aerospace comparables are usable for a Brazilian aerospace firm — beta measures exposure to the macroeconomic risk of the *business*, and country risk goes into the risk premium, not the beta.
- **Tata Motors**: unlevered beta 0.8601 from 76 global automotive companies; D/E 41.41%; India marginal tax rate 32.45% → levered beta = 0.8601 × (1 + 0.6755 × 0.4141) = **1.1007**; cost of equity in rupees = 6.57% + 1.1007 × 7.19% = **14.49%**.
- **Baidu**: unlevered beta 1.30 from 42 global online-advertising companies; D/E 5.23%; China tax rate 25% → levered beta = 1.30 × (1 + 0.75 × 0.0523) = **1.356**; cost of equity in renminbi = 3.50% + 1.356 × 6.94% = **12.91%**.
- **Deutsche Bank (a bank — no unlevering)**: European diversified banks (n = 84) median levered beta 1.0665, weight 54.86% of net revenues; global investment banks (n = 58) median levered beta 1.2550, weight 45.14% → firm beta **1.1516**. Costs of equity at a 1.75% Euro riskfree rate and 6.12% ERP: commercial banking 8.28%, investment banking 9.44%, Deutsche Bank overall **8.80%**.

**Worked example (Vale, end to end):** Iron ore revenues of $32,717m times the peer EV/Sales of 2.48 gives a business value of $81,188m, which is 76.20% of Vale's $106,543m total. Repeating for the other three segments and taking the value-weighted average of the unlevered betas gives **0.8440**. Relevering at Vale's D/E of 54.99% with a 34% tax rate gives a levered beta of **1.1503**, and the cost of equity is 2.75% + 1.1503 × 7.38% = **11.23%**.

**Worked example (why the standard error falls):** A single regression beta for a US stock typically carries a standard error around 0.30. Averaging 78 iron-ore comparables with a similar average standard error gives 0.30 / sqrt(78) ≈ **0.034** — an order of magnitude tighter.

**Determinism:**
- DETERMINISTIC: (comparable betas, comparable D/E, tax rate) → business unlevered beta; (segment revenues, EV/Sales multiples) → business values and weights; (weights, business betas) → firm unlevered beta; (firm unlevered beta, t, D/E) → levered beta; (Rf, beta, ERP) → cost of equity; (identifiable assets, total debt) → divisional debt allocation; (average SE, n) → bottom-up standard error.
- JUDGMENT: which businesses the firm is really in; which firms count as comparables and how wide to cast the net (global versus US, market-cap screens); median versus average; which multiple to use for segment values; whether to adjust for operating leverage or product differences; whether identifiable assets are the right debt-allocation key; how the business mix and D/E will evolve.

**Pitfalls:**
- Weighting business betas by revenues when margins differ sharply across segments. Value weights are the right ones.
- Refusing to use foreign comparables for an emerging-market firm. Business risk travels; country risk belongs in the premium.
- Using the mean beta when one comparable has an extreme D/E (Dex Media at 3190% D/E, Odyssey Pictures at 551%). Use the median.
- Skipping the cash correction for cash-rich comparable sets. The Interactive segment's comparables held 17.25% of firm value in cash.
- Unlevering bank betas.
- Using the company-wide cost of equity as the hurdle rate for every division. Disney's divisional costs of equity ranged from 7.09% to 11.61% around a company average of 8.52%, so the company rate makes safe divisions subsidize risky ones and tilts the firm toward its riskiest businesses.
- Forgetting that the bottom-up beta must be relevered at *market* D/E including capitalized leases.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.91, p.94-97, p.99
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.89, p.92-95, p.97
- corporate_finance--lecture_slides--cfpacket1spr20 p.165-177, p.183, p.200
- spreadsheet `wacccalc.xls` (Valuation Inputs collection): single-business and multi-business bottom-up beta from US/global industry-average unlevered betas, with EV/Sales value weighting and relevering at the firm's market D/E

**Related:** [[levering-and-unlevering-beta]], [[beta-determinants]], [[regression-beta]], [[cost-of-equity-assembly]], [[non-traded-asset-betas]], [[divisional-hurdle-rates]], [[cost-of-capital]]
