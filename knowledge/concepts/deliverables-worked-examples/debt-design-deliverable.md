# Debt design and the mechanics of moving to the optimal

**Core idea:** Part VII of the corporate finance project answers two separate questions. First, how does a firm get from its actual debt ratio to its recommended one — how fast, and by what mechanism? Second, what should the debt *look like* — maturity, currency, fixed or floating, and any special features? The design principle is matching: debt should behave like the assets it finances, so that cash flows on the debt move with cash flows from the assets. Three approaches estimate that behaviour — intuitive, historical (firm-level macro regressions) and cross-sectional/bottom-up (sector regressions).

**Formulas:**
- Speed and method form a 2×2: move *gradually* or *immediately*, by *altering the existing mix* (buy back stock, retire debt) or by *taking new projects* financed with debt or equity.
- Macro sensitivity regressions: regress % change in firm EBIT (or firm value) on the macro variable. The coefficients are read as:
  - Duration coefficient (sensitivity to interest rates) → target debt maturity in years.
  - Cyclicality coefficient (sensitivity to real GDP growth) → how much the debt should be tied to output.
  - Inflation coefficient → fixed vs inflation-linked.
  - Currency coefficient (sensitivity to the US dollar) → currency mix of debt.
- Bottom-up version: run the same regressions on the sector rather than the single firm, and use the sector coefficients.

**Procedure:**
1. **Decide speed.** Gradual when earnings are volatile, when a large acquisition is in flight, or when the firm already sits above its regression-predicted debt ratio and rating agencies would react. Immediate when the gap is large, earnings are stable, and there is no rating constraint.
2. **Decide method.** Altering the existing mix (buybacks funded with debt, or debt retirement) changes leverage without changing the asset base. Financing new projects with debt or equity moves the ratio while growing. Firms with a heavy investment pipeline should prefer the second.
3. **Run the historical approach.** Regress firm EBIT and enterprise value changes on macro variables. Check statistical significance.
4. **If the firm-level regressions are insignificant, switch to bottom-up.** Use sector regressions instead. Assign the firm to the sectors it actually operates in and blend.
5. **Set duration** to match project life. Long-lived store or plant expansion → long duration debt.
6. **Set currency** to match the currencies in which revenues will arise, especially for expansion into new markets.
7. **Set fixed vs floating using pricing power.** A firm that can pass input-cost increases through to customers can carry more floating-rate debt. A firm selling to powerful buyers who resist price increases should hold more fixed-rate debt.
8. **Add special features where growth is uncertain.** Convertible debt suits high-growth firms, because the conversion option prices the growth the lender cannot otherwise underwrite.
9. Write the recommendation per firm as a sentence naming maturity, currency, rate type and features.

**Reference data:** Bottom-up sector EBIT sensitivities used in the 2015 project.

| Factor | Eating and Drinking Places | Food and Kindred Products Manufacturers |
|---|---|---|
| Duration | 7.55 | 4.82 |
| Cyclicality | 0.59 | 0.79 |
| Inflation | 0.28 | 0.06 |
| Currency (US$) | −1.77 | −0.05 |

Reading: restaurants support roughly 7-8 year duration debt; food manufacturing roughly 4.8 years. Both sectors show low cyclicality. Restaurants show meaningful dollar sensitivity (−1.77), food manufacturers essentially none.

Spreadsheet referenced by the course: macrodur.xls. Published data set: firm value sensitivity by industry.

**Worked example:** The 2015 team's four recommendations.
- **Starbucks** — long-term projects (store expansion) with steady earnings, so roughly 6-8 year duration. Expansion targets non-traditional markets, so issue debt in the mix of currencies where the revenues will arise. As a restaurant with pricing power, it can carry a larger share of floating-rate debt.
- **McDonald's** — similar duration and the same match-currency logic, but expansion is more gradual because it is already present in most emerging markets. Its stable earnings and size give it more room to borrow, and it faces little rating risk.
- **Chipotle** — a rapid expansion agenda argues for convertible debt in US dollars and euros matching its target markets. High same-store-sales growth allows slightly shorter durations. Little rating risk.
- **Tyson** — long-term US dollar debt is ideal, but the move to the optimum should be gradual given acquisition risk and rating sensitivity. Tyson sells to powerful large retailers such as Walmart with little pricing flexibility, so it should hold a greater proportion of fixed-rate debt.

The historical approach was tried first and largely failed: regressions of firm EBIT and enterprise value on macro variables produced almost no statistical significance, with only the Starbucks EBIT-versus-GDP relationship significant. The team therefore fell back on the bottom-up sector approach, treating Starbucks as a restaurant/beverage mix, McDonald's and Chipotle as restaurants, and Tyson as meat processing.

**Determinism:** DETERMINISTIC — the macro regressions themselves (firm-level and sector-level), their coefficients, significance tests, and the mechanical reading of the duration coefficient as a target maturity. Assigning a firm to sectors and value-weighting the coefficients is also mechanical once the mix is known. JUDGMENT — the speed and method of the move, whether to use convertibles, the fixed/floating split, the currency mix, and the business mix used for the bottom-up blend. Pricing power in particular has no number attached; it needs knowledge of the customer base and of who holds bargaining power.

**Pitfalls:**
- Using firm-level macro regressions when they are statistically insignificant. Insignificant coefficients are noise, and reading a duration off them is worse than using the sector average.
- Matching currency to the country of listing rather than to where future revenues will arise.
- Recommending an immediate jump to the optimum for a firm with volatile EBIT or a pending acquisition. Rating agencies apply qualitative criteria and penalise fast moves.
- Assigning floating-rate debt to a firm with weak pricing power. It stacks input-cost risk on top of interest-rate risk.
- Treating debt design as cosmetic. Mismatched debt raises the probability of distress at exactly the moment the assets underperform.

**Sources:**
- corporate_finance--project--cfproj p.10
- corporate_finance--project--food2015 p.13-15

**Related:** [[optimal-debt-ratio-wacc-schedule]], [[recapitalization-value-and-stress-test]], [[qualitative-debt-tradeoff]], [[dividend-policy-deliverable]], [[corporate-finance-project-blueprint]]
