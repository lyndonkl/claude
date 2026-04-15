# Project Investment Analyzer Templates

Templates for structuring project cash flows, computing NPV/IRR, assessing value creation, and running sensitivity analysis.

## Table of Contents
- [Project Cash Flow Template](#project-cash-flow-template)
- [NPV/IRR Calculation Template](#npv-irr-calculation-template)
- [Value Creation Scorecard](#value-creation-scorecard)
- [Sensitivity Grid](#sensitivity-grid)
- [Project Comparison Matrix](#project-comparison-matrix)

---

## Project Cash Flow Template

### Project Overview

| Field | Value |
|-------|-------|
| **Project name** | [Name] |
| **Description** | [What is being invested in?] |
| **Initial investment** | $[Amount] at Time 0 |
| **Project life** | [N] years |
| **Salvage value** | $[Amount] at end of year [N] |
| **Depreciation method** | [Straight-line / Accelerated] |
| **Geographic exposure** | [Countries/regions with revenue %] |

### Sunk Cost Exclusions

List costs already incurred that are excluded from the analysis:

| Cost Item | Amount | Why Excluded |
|-----------|--------|-------------|
| [e.g., Prior R&D] | $[Amount] | Already spent, unrecoverable regardless of decision |
| [e.g., Market research] | $[Amount] | Completed before investment decision |

### Opportunity Cost Inclusions

List forgone alternatives included as costs:

| Resource Used | Alternative Use | Forgone Value |
|---------------|----------------|---------------|
| [e.g., Factory capacity] | [e.g., Rent to third party] | $[Amount]/year |
| [e.g., Management time] | [e.g., Other project] | $[Amount]/year |

### Side Effects

| Side Effect | Type | Annual Impact |
|-------------|------|---------------|
| [e.g., Cannibalization of Product X] | Negative | -$[Amount] in lost margin |
| [e.g., Cross-selling boost to Service Y] | Positive | +$[Amount] in incremental margin |

### Year-by-Year Cash Flow Table

| Item | Year 0 | Year 1 | Year 2 | Year 3 | ... | Year N |
|------|--------|--------|--------|--------|-----|--------|
| **Revenue** | | | | | | |
| Equipment/product revenue | -- | | | | | |
| Subscription/recurring revenue | -- | | | | | |
| Side effect revenue | -- | | | | | |
| **Total Revenue** | -- | | | | | |
| **Operating Costs** | | | | | | |
| Cost of goods sold | -- | | | | | |
| Content/service costs | -- | | | | | |
| Incremental SG&A | -- | | | | | |
| Incremental advertising | -- | | | | | |
| **Total Operating Costs** | -- | | | | | |
| **EBITDA** | -- | | | | | |
| Depreciation | -- | | | | | |
| **EBIT (Operating Income)** | -- | | | | | |
| Taxes (at marginal rate) | -- | | | | | |
| **After-tax Operating Income** | -- | | | | | |
| + Depreciation (add back) | -- | | | | | |
| - Capital Expenditure | ($[Init]) | | | | | |
| - Change in Working Capital | | | | | | |
| + After-tax Salvage Value | -- | -- | -- | -- | -- | |
| **Free Cash Flow to Firm** | | | | | | |

### Working Capital Detail

| Component | Calculation | Year 0 | Year 1 | Year 2 | ... |
|-----------|------------|--------|--------|--------|-----|
| Accounts Receivable | [X]% of revenue | | | | |
| Inventory | [X]% of COGS or revenue | | | | |
| Accounts Payable | [X]% of COGS or revenue | | | | |
| **Net Working Capital** | AR + Inventory - AP | | | | |
| **Change in Working Capital** | Current - Prior year | | | | |

### Depreciation Schedule

| Item | Year 0 | Year 1 | Year 2 | ... | Year N |
|------|--------|--------|--------|-----|--------|
| Beginning Book Value | -- | $[Init] | | | |
| Depreciation Expense | -- | | | | |
| Ending Book Value | $[Init] | | | | $[Salvage] |
| Tax Shield (Dep x Tax Rate) | -- | | | | |

---

## NPV/IRR Calculation Template

### NPV Computation

| Year | Free Cash Flow | Discount Factor (1/(1+r)^t) | Present Value |
|------|---------------|----------------------------|---------------|
| 0 | | 1.000 | |
| 1 | | | |
| 2 | | | |
| 3 | | | |
| ... | | | |
| N | | | |
| **Sum** | | | **NPV = $[Amount]** |

**Discount rate used**: [r]% (project-specific WACC)

**NPV interpretation**:
- [ ] NPV > 0: Project creates value. Invest (subject to sensitivity check).
- [ ] NPV = 0: Project earns exactly its cost of capital. Indifferent.
- [ ] NPV < 0: Project destroys value. Reject.

### IRR Computation

**IRR**: [X]% (the discount rate at which NPV = 0)

**IRR interpretation**:
- [ ] IRR > hurdle rate ([r]%): Project clears the bar.
- [ ] IRR < hurdle rate: Project does not earn its cost of capital.

**IRR caution flags**:
- [ ] Cash flows change sign more than once? (risk of multiple IRRs)
- [ ] Comparing projects of very different scale? (use NPV for ranking instead)
- [ ] Non-conventional timing? (large cash outflows mid-project)

If any caution flag is checked, rely on NPV rather than IRR for the decision.

---

## Value Creation Scorecard

### Return on Capital Assessment

| Metric | Value | Benchmark |
|--------|-------|-----------|
| After-tax Operating Income (steady state) | $[Amount] | |
| Invested Capital | $[Amount] | |
| **ROC** | [X]% | |
| Project WACC | [Y]% | |
| **ROC - WACC (Spread)** | [X-Y]% | > 0 = value creation |
| **EVA** | $[Amount] | (ROC - WACC) x Invested Capital |

### Value Creation Summary

- [ ] ROC > WACC: Project creates economic value
- [ ] ROC = WACC: Project earns exactly its cost of capital (zero economic profit)
- [ ] ROC < WACC: Project destroys value even if accounting profitable

**Note**: A project can show positive accounting profit (net income > 0) while still destroying value if ROC < WACC. The cost of equity capital is real even though it does not appear on the income statement.

### Cumulative Value Assessment (for backward-looking analysis)

| Year | Invested Capital | After-tax OI | ROC | WACC | EVA | Cumulative EVA |
|------|-----------------|-------------|-----|------|-----|----------------|
| 1 | | | | | | |
| 2 | | | | | | |
| ... | | | | | | |
| N | | | | | | |

---

## Sensitivity Grid

### One-Variable Sensitivity (NPV vs. Key Assumption)

**Variable tested**: [e.g., Market share at steady state]

| Assumption Value | NPV ($M) | IRR (%) | Decision |
|-----------------|----------|---------|----------|
| Pessimistic: [X] | | | Invest / Reject |
| Conservative: [Y] | | | Invest / Reject |
| **Base case: [Z]** | | | **Invest / Reject** |
| Optimistic: [W] | | | Invest / Reject |

**Breakeven value**: NPV = 0 when [variable] = [breakeven value]

### Two-Variable Sensitivity Grid (NPV)

| | WACC -1% | **WACC Base** | WACC +1% | WACC +2% |
|---|----------|-------------|----------|----------|
| **Growth -2%** | | | | |
| **Growth -1%** | | | | |
| **Growth Base** | | **$[Base NPV]** | | |
| **Growth +1%** | | | | |

Shade cells: positive NPV in one style, negative in another.

### Key Assumption Sensitivity Summary

| Assumption | Base Case | Range Tested | NPV Range | Decision Flips? |
|------------|-----------|-------------|-----------|----------------|
| Market share | [X]% | [A]% to [B]% | $[Lo] to $[Hi] | Yes / No |
| Discount rate | [X]% | [A]% to [B]% | $[Lo] to $[Hi] | Yes / No |
| Price growth | [X]% | [A]% to [B]% | $[Lo] to $[Hi] | Yes / No |
| Project life | [X] years | [A] to [B] years | $[Lo] to $[Hi] | Yes / No |
| Cost inflation | [X]% | [A]% to [B]% | $[Lo] to $[Hi] | Yes / No |

**Key insight**: If the decision flips only under extreme assumptions, the recommendation is robust. If it flips under plausible scenarios, consider deferring or gathering more data.

---

## Project Comparison Matrix

Use when evaluating multiple mutually exclusive projects:

| Metric | Project A | Project B | Project C |
|--------|-----------|-----------|-----------|
| Initial Investment | | | |
| Project Life | | | |
| NPV | | | |
| IRR | | | |
| ROC (steady state) | | | |
| WACC (project-specific) | | | |
| ROC - WACC | | | |
| EVA (annual, steady state) | | | |
| Payback Period | | | |
| Key Risk | | | |

**Selection rule for mutually exclusive projects**: Choose the project with the highest NPV (not the highest IRR). IRR can be misleading when projects differ in scale or timing.

**Selection rule for independent projects with capital constraint**: Rank by profitability index (NPV / Initial Investment) and select from top until budget is exhausted.

| Project | NPV | Investment | PI (NPV/Investment) | Cumulative Investment | Select? |
|---------|-----|-----------|---------------------|----------------------|---------|
| [Rank 1] | | | | | |
| [Rank 2] | | | | | |
| [Rank 3] | | | | | |
