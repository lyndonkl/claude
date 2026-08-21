# Operation-weighted corporate equity risk premium

**Core idea:** Convention assigns a company the equity risk premium of its country of incorporation. That is wrong for any firm whose operations sit elsewhere. Risk exposure comes from where a company *does business*, not where it is registered. The fix is to compute a company-specific ERP as a weighted average of the ERPs of the countries or regions in which it operates, weighting by revenues, operating income, production, or assets. This is not a marginal refinement: Embraer's cost of equity in 2004 varies from 9.6% to 17.8% purely on how country risk is attached, and the conventional blanket treatment systematically undervalues globalized emerging-market companies.

**Formulas:**
- Company ERP = Σ_i (weight_i × ERP_i), where i indexes countries or regions, weight_i = that country's share of the chosen exposure measure (revenues, operating income, production, or assets), and ERP_i = that country's total equity risk premium.
- Company CRP = Σ_i (weight_i × CRP_i) = Company ERP − Mature market premium.
- The four exposure/attachment combinations, with Rf = riskfree rate and β = beta:
  1. Constant exposure, location CRP: E(R) = Rf + β × Mature ERP + CRP_country of incorporation.
  2. Constant exposure, operation CRP: E(R) = Rf + β × Mature ERP + Σ(weight_i × CRP_i).
  3. Beta exposure, location CRP: E(R) = Rf + β × (Mature ERP + CRP_country of incorporation).
  4. Beta exposure, operation CRP: E(R) = Rf + β × (Mature ERP + Σ(weight_i × CRP_i)).
  A fifth, lambda-based, approach appears in [[lambda-country-risk-exposure]].

**Procedure:**
1. Pull the company's **geographic breakdown of revenues** for the most recent year from the segment footnote.
2. Map each reported geography to a country or region in the country-ERP table (see [[country-risk-premium]]). Watch the aggregations: many filers report a "Pacific" region that lumps Australia and New Zealand with Asia, and labels like "Eurasia" or "Oceania" map to nothing clean.
3. If exposure spans dozens of countries, weight **regional** ERPs instead of country ERPs. Regional ERPs are GDP-weighted averages of their member countries.
4. Compute weights = geography revenue / total revenue, then take the weighted average of total ERPs. The company CRP is the weighted average minus the mature-market premium.
5. Ask whether revenues are the right weight. For a natural-resource company, **production** location is the better measure: Royal Dutch Shell sells globally but pumps oil in Nigeria, Iraq, and Oman. For a manufacturer, ask where the plants are. An emerging-market exporter selling into developed markets may still have every factory at home.
6. Decide how to attach the resulting premium: additively (constant exposure) or scaled by beta. Multiplying CRP by beta assumes beta measures country-risk exposure on top of all other macro risk, which is not established.
7. Where exposure clearly differs from any revenue or production weight — hedging programs, government involvement — move to a lambda (see [[lambda-country-risk-exposure]]).

**Reference data:**

Embraer, 2004 (mature ERP 5%, Brazil CRP 7.89%; the source table rounds Brazil to 8% CRP / 12.89% total ERP):

| | Revenues | Total ERP | CRP |
|---|---|---|---|
| US and other mature markets | 97% | 5.00% | 0.00% |
| Brazil | 3% | 12.89% | 8% |
| **Embraer (weighted)** | | **5.24%** | **0.24%** |

Ambev, 2011 (revenue-weighted across eight countries):

| Country | Revenues | % | Total ERP | CRP |
|---|---|---|---|---|
| Argentina | 19 | 9.31% | 15.00% | 9.00% |
| Bolivia | 4 | 1.96% | 10.88% | 4.88% |
| Brazil | 130 | 63.73% | 8.63% | 2.63% |
| Canada | 23 | 11.27% | 6.00% | 0.00% |
| Chile | 7 | 3.43% | 7.05% | 1.05% |
| Ecuador | 6 | 2.94% | 12.75% | 6.75% |
| Paraguay | 3 | 1.47% | 12.00% | 6.00% |
| Peru | 12 | 5.88% | 9.00% | 3.00% |
| **Ambev (total)** | **204** | | **9.11%** | **3.11%** |

Coca Cola, 2012 (regional weighting):

| Region | Revenues | Total ERP | CRP |
|---|---|---|---|
| Western Europe | 19% | 6.67% | 0.67% |
| Eastern Europe & Russia | 5% | 8.60% | 2.60% |
| Asia | 15% | 7.63% | 1.63% |
| Latin America | 15% | 9.42% | 3.42% |
| Australia | 4% | 6.00% | 0.00% |
| Africa | 4% | 9.82% | 3.82% |
| North America | 40% | 6.00% | 0.00% |
| **Coca Cola** | **100%** | **7.14%** | **1.14%** |

Royal Dutch Shell, 2015 — weighted by **oil and gas production**, not revenues (share of total | country ERP): Denmark 3.83% 6.20%; Italy 2.46% 9.14%; Norway 3.16% 6.20%; UK 4.57% 6.81%; Rest of Europe 0.19% 7.40%; Brunei 0.18% 9.04%; Iraq 4.40% 11.37%; Malaysia 5.06% 8.05%; Oman 17.26% 7.29%; Russia 4.85% 10.06%; Rest of Asia & ME 5.39% 7.74%; Oceania 1.73% 6.20%; Gabon 2.75% 11.76%; Nigeria 14.93% 11.76%; Rest of Africa 1.36% 12.17%; USA 22.95% 6.20%; Canada 1.89% 6.20%; Brazil 2.93% 9.60%; Rest of Latin America 0.13% 10.78%. **Company ERP = 8.26%.**

Disney, November 2013 — a US company that is not purely a US-ERP company:

| Region | Share of revenues | ERP |
|---|---|---|
| US & Canada | 82.01% | 5.50% |
| Europe | 11.64% | 6.72% |
| Asia-Pacific | 6.02% | 7.27% |
| Latin America | 0.33% | 9.44% |
| **Disney** | **100.00%** | **5.76%** |

Other November 2013 company ERPs on a 5.50% mature premium: Vale 7.38% (Brazil 16.9%, China 37.0%, Japan 10.3%, Europe 17.2%, rest of Asia 8.5%, US & Canada 4.9%, rest of Latin America 1.7%, rest of world 3.5%); Tata Motors 7.19% (India 23.9%, China 23.6%, UK 11.9%, US 10.0%, mainland Europe 11.7%, rest of world 18.9%); Deutsche Bank 6.12% (Germany 35.93%, North America 24.72%, rest of Europe 28.67%, Asia-Pacific 10.68%); Baidu 6.94% (China 100%); Bookscape 5.50% (US 100%).

**Worked example (Embraer, September 2004 — five treatments of the same company):** Beta 1.07, US$ riskfree 4%, mature ERP 5%, Brazil CRP 7.89%, 3% of revenues from Brazil, lambda 0.27.

| Approach | Computation | Cost of equity |
|---|---|---|
| 1. Constant exposure, location CRP | 4% + 1.07×5% + 7.89% | 17.24% |
| 2. Constant exposure, operation CRP | 4% + 1.07×5% + (0.03×7.89% + 0.97×0%) | 9.59% |
| 3. Beta exposure, location CRP | 4% + 1.07×(5% + 7.89%) | 17.79% |
| 4. Beta exposure, operation CRP | 4% + 1.07×(5% + 0.03×7.89%) | 9.60% |
| 5. Lambda exposure | 4% + 1.07×5% + 0.27×7.89% | 11.48% |

The spread is more than 8 percentage points on identical facts. Standard investment-banking practice picks approach 1 or 3, so Embraer gets discounted at 17-18% despite earning 97% of revenues in mature markets. That discount rate is far too high, so the analyst's value is far too low — meaning globalized emerging-market companies are systematically *undervalued* by analysts, and buying them is a trade if the market eventually corrects the discount rate.

**Determinism:**
- DETERMINISTIC: (geographic weights, country/regional ERPs) → company ERP and CRP; (Rf, beta, mature ERP, company CRP) → cost of equity under any of the four approaches. A script can compute all of this from a revenue table and the country-ERP lookup.
- JUDGMENT: which exposure measure to weight by (revenues, operating income, production, assets); how to map reported geographies onto the ERP table; whether to attach the CRP additively or through beta; how to handle "rest of world" buckets; whether a company's real exposure is captured by any weight at all.

**Pitfalls:**
- **Focusing only on revenues.** An emerging-market firm selling into developed markets may hold all its production, and therefore all its expropriation and currency risk, at home.
- **Location-based CRP by default.** It overstates the cost of equity for globalized emerging-market firms and understates it for developed-market firms with heavy emerging exposure.
- Assuming developed-market companies have zero country risk. Disney's operation-weighted ERP was 5.76%, not 5.50%.
- Multiplying the CRP by beta without noticing the assumption that beta measures country-risk exposure too.
- Mishandling reported regional aggregations ("Pacific", "Eurasia", "Oceania") and silently mapping them to the wrong ERP.
- Using a country ERP table from a different date than the riskfree rate and mature premium.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.54-59, p.63-64
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.54-59, p.63-64
- corporate_finance--lecture_slides--cfpacket1spr20 p.124-125, p.131

**Related:** [[country-risk-premium]], [[lambda-country-risk-exposure]], [[cost-of-equity-assembly]], [[bottom-up-beta]], [[country-risk-in-cost-of-debt]]
