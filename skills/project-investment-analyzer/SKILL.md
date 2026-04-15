---
name: project-investment-analyzer
description: Evaluates investment projects using NPV, IRR, and return on capital analysis. Determines whether a project clears its hurdle rate (ROC > WACC), computes economic value added (EVA), and adjusts discount rates for regional or project-specific risk. Use when evaluating capital investments, analyzing project returns, comparing investment alternatives, or when user mentions NPV, IRR, hurdle rate, capital budgeting, project evaluation, EVA, or return on invested capital.
---
# Project Investment Analyzer

## Table of Contents
- [Example](#example)
- [Workflow](#workflow)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Example

**Scenario**: Netflix-style international expansion -- "Netflix Fit" fitness equipment and subscription service

**Project scope**: $2.4B upfront manufacturing investment, 10-year depreciable life (salvage $400M), global rollout with 60% of revenue outside North America.

**Cash flow identification**:
- Sunk costs excluded: $250M already spent on R&D (irrelevant to decision)
- Equipment revenue: new subscribers buy $1,000 unit (cost $400), prices grow with inflation
- Subscription revenue: $120/year per subscriber, $24/year servicing cost, both grow with inflation
- Content costs: $400M year 1, growing 10% for 5 years then at inflation
- Side effects included: $500M boost to core streaming revenue (15% operating margin), growing at inflation
- Working capital: 10% of equipment revenue (inventory) + 5% AR - 5% AP, invested at start of each year

**Discount rate adjustment**:
- Base WACC (US): 9.0% (bottom-up beta from fitness peers, relevered at Netflix capital structure)
- Revenue-weighted country risk premium: 40% North America (0%), 15% Western Europe (+0.5%), 15% Asia (+2.5%), 10% Central/South America (+3.0%), 5% Africa (+4.0%), 5% Eastern Europe (+3.5%), 5% Australia (+0%), 5% Middle East (+2.0%)
- Blended additional CRP: ~1.4%
- Project WACC: 10.4%

**Results**:
- NPV at 10.4%: +$1.8B (positive -- invest)
- IRR: 14.2% (exceeds 10.4% hurdle)
- Steady-state ROC: 16% vs. WACC 10.4% (value-creating)
- EVA at steady state: (16% - 10.4%) x $2.4B = ~$134M/year
- Recommendation: Invest. NPV remains positive even if market share reaches only 15% instead of 25%.

## Workflow

Copy this checklist and track your progress:

```
Project Investment Analysis Progress:
- [ ] Step 1: Define project scope and identify cash flows
- [ ] Step 2: Determine project-specific discount rate
- [ ] Step 3: Compute NPV and IRR
- [ ] Step 4: Assess value creation (ROC vs WACC, EVA)
- [ ] Step 5: Run sensitivity analysis
- [ ] Step 6: Make recommendation (invest / defer / reject)
```

**Step 1: Define project scope and identify cash flows**

Map all incremental cash flows attributable to the project. Exclude sunk costs (already spent regardless of decision). Include opportunity costs (forgone alternative uses of resources). Capture side effects such as cannibalization of existing products or synergy with other divisions. See [resources/template.md](resources/template.md#project-cash-flow-template) for the year-by-year cash flow input template.

**Step 2: Determine project-specific discount rate**

If the project has different risk characteristics than the company overall, compute a project-specific discount rate. For international projects, add a revenue-weighted country risk premium to the base WACC. For projects in a different industry than the parent, use a bottom-up beta from peers in that industry. See [resources/methodology.md](resources/methodology.md#project-specific-discount-rates) for regional risk adjustment and project beta estimation.

**Step 3: Compute NPV and IRR**

Discount incremental after-tax cash flows at the project-specific hurdle rate. Compute NPV as the sum of discounted cash flows minus the initial investment. Find the IRR (discount rate at which NPV equals zero). See [resources/template.md](resources/template.md#npv-irr-calculation-template) for the NPV/IRR calculation worksheet.

**Step 4: Assess value creation (ROC vs WACC, EVA)**

Compute the project's return on invested capital once it reaches steady state. Compare ROC to the project's WACC. Calculate EVA as (ROC - WACC) x Invested Capital. A project creates value when ROC exceeds WACC. See [resources/methodology.md](resources/methodology.md#eva-framework) for the economic value added framework.

**Step 5: Run sensitivity analysis**

Identify the 3-5 assumptions that most affect NPV (typically: market share, pricing, discount rate, cost inflation, project life). Vary each independently and observe the impact on NPV and the invest/reject decision. See [resources/template.md](resources/template.md#sensitivity-grid) for the sensitivity grid template.

**Step 6: Make recommendation (invest / defer / reject)**

Synthesize NPV, IRR, ROC/EVA, and sensitivity results into a clear recommendation. If NPV is positive across plausible scenarios, recommend investing. If NPV is positive only under optimistic assumptions, recommend deferring until uncertainty resolves. If NPV is negative under most scenarios, recommend rejecting. Validate using [resources/evaluators/rubric_project_investment_analyzer.json](resources/evaluators/rubric_project_investment_analyzer.json). **Minimum standard**: Average score of 3.5 or above.

## Common Patterns

**Pattern 1: Domestic Expansion**
- **Context**: New plant, product line, or capacity expansion within the company's home market
- **Discount rate**: Use company WACC (no country risk adjustment needed)
- **Key considerations**: Cannibalization of existing products (include as negative cash flow), economies of scale, capacity utilization ramp-up
- **Cash flows**: CapEx, incremental revenue, incremental operating costs, working capital, depreciation tax shield
- **Decision rule**: NPV > 0 and IRR > WACC

**Pattern 2: International / Emerging Market Project**
- **Context**: Expansion into new geography with different risk profile (e.g., building a facility in India or Brazil)
- **Discount rate**: Adjust WACC for country risk premium, weighted by revenue exposure to each region
- **Key considerations**: Currency risk (match cash flow currency to discount rate currency), political risk, local operating cost differences, regulatory environment
- **Cash flows**: Same as domestic plus currency conversion, potentially higher operating costs, region-specific tax rates
- **Decision rule**: NPV > 0 at risk-adjusted rate. Compare project IRR to the higher regional hurdle rate.

**Pattern 3: Existing Investment Assessment (Backward-Looking)**
- **Context**: Evaluating whether a past investment has created or destroyed value
- **Discount rate**: WACC at the time of investment (or current WACC if re-evaluating going forward)
- **Key considerations**: Compare realized ROC to WACC over the investment's life. Compute cumulative EVA. Identify whether the project earned its cost of capital.
- **Decision rule**: If ROC > WACC, value was created. If ROC < WACC, capital was destroyed regardless of accounting profitability.

## Guardrails

1. **Exclude sunk costs**: Money already spent and unrecoverable is irrelevant to the go/no-go decision. The $250M already spent on R&D in the Netflix Fit example does not factor into the NPV calculation, even if it feels psychologically relevant.

2. **Include opportunity costs**: If the project uses resources that could generate value elsewhere (e.g., excess studio capacity that could be rented out), the forgone revenue is a real cost of the project.

3. **Use project-specific discount rates when risk differs from the company average**: A technology company entering the restaurant business faces restaurant-level risk on that project, not tech-level risk. Use bottom-up beta from the project's industry.

4. **Be cautious with IRR**: IRR can be misleading when cash flows change sign more than once (producing multiple IRRs). It also cannot rank mutually exclusive projects of different scale -- a small project with 50% IRR may create less value than a large project with 20% IRR. When in doubt, rely on NPV.

5. **For mutually exclusive projects, choose highest NPV, not highest IRR**: IRR does not account for scale. A $1M project earning 30% IRR creates less value than a $100M project earning 15% IRR.

6. **Include all side effects in cash flows**: Cannibalization (new product steals sales from existing product) reduces incremental cash flows. Synergy (new product boosts demand for existing products) increases them. Both belong in the analysis.

7. **Match cash flow currency to discount rate currency**: If cash flows are in local currency (e.g., Indian rupees), discount at a rupee-denominated rate. If cash flows are converted to USD, discount at a USD rate with country risk premium.

**Common pitfalls:**

- Counting sunk costs as part of the investment (they are irrelevant once spent)
- Forgetting working capital investment (inventory, receivables build as revenue grows)
- Using the company's overall WACC for a project with different risk characteristics
- Ignoring the time value of the salvage value (discount it back to present)
- Double-counting depreciation (it is a non-cash charge that creates a tax shield, not a cash outflow)
- Confusing accounting profit with cash flow (add back depreciation, subtract CapEx and working capital changes)

## Quick Reference

**Key formulas:**

```
NPV = Sum of [CF_t / (1 + r)^t] for t=0 to n
    where CF_0 is typically the initial investment (negative)
    and r is the project-specific discount rate

IRR = discount rate r such that NPV = 0

ROC (Return on Capital) = After-tax Operating Income / Invested Capital

ROE (Return on Equity) = Net Income / Book Value of Equity

EVA (Economic Value Added) = (ROC - WACC) x Invested Capital

Depreciation Tax Shield = Depreciation x Tax Rate

After-tax Salvage = Salvage Value - Tax Rate x (Salvage - Book Value)

Incremental Cash Flow = After-tax Operating Income
                        + Depreciation
                        - Capital Expenditure
                        - Change in Working Capital
                        + After-tax Salvage (in final year)

Project-Specific WACC = Base WACC + Revenue-Weighted Country Risk Premium
```

**Decision rules:**

| Metric | Invest | Defer | Reject |
|--------|--------|-------|--------|
| **NPV** | > 0 across scenarios | > 0 base case, < 0 pessimistic | < 0 in most scenarios |
| **IRR** | > hurdle rate | Near hurdle rate | < hurdle rate |
| **ROC vs WACC** | ROC > WACC | ROC near WACC | ROC < WACC |
| **EVA** | Positive | Near zero | Negative |

**Key resources:**

- **[resources/template.md](resources/template.md)**: Project cash flow template, NPV/IRR calculation worksheet, value creation scorecard, sensitivity grid, project comparison matrix
- **[resources/methodology.md](resources/methodology.md)**: NPV mechanics, IRR pitfalls, project-specific discount rates, EVA framework, sunk cost and opportunity cost treatment
- **[resources/evaluators/rubric_project_investment_analyzer.json](resources/evaluators/rubric_project_investment_analyzer.json)**: Quality criteria for cash flow identification, discount rate, NPV/IRR, sensitivity, recommendation

**Inputs required:**

- **Project cash flows**: Year-by-year revenue, operating costs, CapEx, working capital, taxes, salvage value
- **Project risk profile**: Geographic revenue breakdown, industry of project, project-specific beta (if different from company)
- **Discount rate components**: Risk-free rate, equity risk premium, country risk premiums, beta, tax rate, capital structure
- **Decision context**: Is this a go/no-go decision, a choice among mutually exclusive projects, or a backward-looking assessment?

**Outputs produced:**

- `project-investment-analysis.md`: Complete analysis with cash flow table, discount rate computation, NPV, IRR, ROC, EVA, sensitivity analysis, and recommendation
