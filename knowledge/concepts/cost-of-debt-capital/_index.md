# Cost of debt and cost of capital — concept index

Area: everything between "I have a cost of equity" and "I have a discount rate I can use." Definition of debt, ratings and default spreads, hybrids, market-value weights, and the assembly and currency conversion of the WACC.

| Concept | What it covers | Determinism |
|---|---|---|
| [[what-counts-as-debt]] | The three-part test for debt; include interest-bearing liabilities and all leases; exclude payables; classification checklist | JUDGMENT (classification) → DETERMINISTIC (aggregation) |
| [[cost-of-debt-estimation-routes]] | The four-route decision tree: traded bond YTM, actual rating, recent bank loan, synthetic rating; currency consistency; median rating rule | JUDGMENT (route choice) → DETERMINISTIC (within route) |
| [[interest-coverage-ratio]] | EBIT/interest; normalizing EBIT; lease-adjusted coverage; emerging-market interest-rate scaling; the rating/lease circularity | MIXED — ratio deterministic, normalization judgment |
| [[synthetic-rating]] | Coverage → rating → spread; full lookup tables for large, small/risky and financial firms across four vintages (2020, ratings.xls, Nov 2013, 2004) | DETERMINISTIC (table lookup); JUDGMENT on firm class |
| [[synthetic-vs-actual-rating]] | Why the two diverge: extra information, sector bias, normalized earnings, country risk; when to use which | JUDGMENT |
| [[default-spreads-over-time]] | Spreads by rating and date; the 2008 crisis table, the COVID 2020 table, four spread vintages; why the table must be refreshed | DETERMINISTIC lookup; JUDGMENT on which date |
| [[country-risk-in-cost-of-debt]] | Sovereign vs company spread; lambda (fraction of country risk borne); global vs local-agency ratings; country default spread and marginal tax rate tables | MIXED — lambda is judgment, the rest deterministic |
| [[after-tax-cost-of-debt]] | The (1−t) factor; marginal not effective rate; why the tax shield is in the discount rate and not in FCFF; country marginal tax rates | DETERMINISTIC; JUDGMENT on which marginal rate |
| [[subsidized-debt]] | Fair cost of debt for the WACC, subsidy valued separately; the Embraer 6% vs 9.25% case | JUDGMENT |
| [[preferred-stock-cost]] | Cost = dividend yield, no tax shield; third component of capital; the 5%-of-firm-value shortcut | DETERMINISTIC; JUDGMENT on terms and materiality |
| [[convertible-debt-decomposition]] | Splitting a convertible into straight debt (discounted at the straight-bond rate) and a conversion option counted as equity | DETERMINISTIC; JUDGMENT on the straight-bond rate |
| [[operating-leases-as-debt]] | Full lease-capitalization algorithm (n₆, annuity, PV, depreciation, EBIT and debt restatement); Disney and oplease.xls worked through; IFRS 16 / ASC 842 caveat | DETERMINISTIC; JUDGMENT on discount rate and tail |
| [[market-value-of-debt]] | Book debt → market value by treating total debt as one coupon bond; weighted-average maturity; the 3-year default | DETERMINISTIC; JUDGMENT on maturity |
| [[market-value-weights]] | Why market values, not book; the three specious arguments rebutted; private-firm D/E rule | DETERMINISTIC arithmetic; JUDGMENT on inclusion rules |
| [[net-debt-vs-gross-debt]] | Two conventions, the consistency requirement, negative net debt ratios, cash-adjusted unlevered betas | DETERMINISTIC; JUDGMENT on convention |
| [[cost-of-capital-assembly]] | The WACC formula end to end; consistency checks; assembled rates for Disney, Vale, Tata, Baidu, Bookscape, Embraer, Facebook | DETERMINISTIC; JUDGMENT lives upstream |
| [[divisional-cost-of-capital]] | Per-division rates: debt allocation, divisional D/E, relevering, divisional WACC; Disney's five divisions and Vale's four businesses | DETERMINISTIC; JUDGMENT on divisions and allocation key |
| [[currency-conversion-of-discount-rates]] | Differential-inflation conversion of any discount rate; the direct-rebuild cross-check; Vale and Embraer | DETERMINISTIC; JUDGMENT on inflation forecasts |
| [[wacc-calculator-workflow]] | wacccalc.xls as an executable pipeline: order of operations, the lease/rating circularity, the full input surface, iteration and edge cases | DETERMINISTIC pipeline; JUDGMENT on approach flags |
| [[hurdle-rate-choice]] | Matching the hurdle rate to the claimholders and to the project's risk and currency; Disney movie and Rio Disney cases | JUDGMENT (matching rule) |

## How these connect, and in what order to use them

Start by deciding **what counts as debt**. Nothing downstream is stable until you have fixed the boundary of the debt claim: interest-bearing liabilities in, payables out, leases capitalized, convertibles split, preferred handled separately. That single decision feeds three different places — the interest coverage ratio, the market value of debt, and the cost-of-capital weights.

Then estimate the **cost of debt**. Walk the estimation-routes decision tree. If the firm has no usable rating, compute the **interest coverage ratio** (normalized and lease-adjusted) and run the **synthetic rating** lookup. Take the spread from a **current** spread table, not a stale one. If the firm sits in an emerging market, decide whether **country risk** is already inside its rating or must be added, and with what lambda. Reconcile the **synthetic against the actual rating** and explain any gap; that gap is often the country-risk story. Handle **subsidized debt** by using the fair rate here and valuing the subsidy separately. Apply the marginal tax rate to get the **after-tax cost of debt**.

Note the loop hiding in that paragraph: **operating leases** must be capitalized to get the coverage ratio, but capitalizing them needs the cost of debt, which needs the rating, which needs the coverage ratio. The **WACC calculator workflow** concept gives the fixed-point iteration that resolves it and fixes the order of every other step.

Next build the **weights**. Convert book debt to a **market value of debt**, add capitalized leases, add the straight-debt half of any convertible, and value **preferred stock** separately if it is material. Insist on **market-value weights**, and stay inside one convention — **net debt or gross debt**, never both.

Now **assemble the cost of capital**: a cost of equity from the beta area, the after-tax cost of debt from this area, and market-value weights. For a multi-business firm, do it once per division rather than once for the company — **divisional cost of capital**. If the valuation currency differs from the currency you built the rate in, **convert with the inflation differential**. Finally, before using the number, apply the **hurdle-rate matching rule**: equity returns against the cost of equity, firm returns against the cost of capital, always at the risk level and in the currency of the thing being measured.

Inbound dependencies from other areas: the cost of equity, bottom-up and levered betas, the equity risk premium and country risk premium, the riskfree rate, and total beta for private firms. Outbound: this area's output is the discount rate used in DCF valuation, the hurdle rate used in capital budgeting, and the benchmark used to compute excess returns and EVA.
