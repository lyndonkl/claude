# Capital Structure Optimizer Templates

Input templates, WACC schedule table, debt type matching worksheet, and implementation path frameworks.

## Table of Contents
- [Current Capital Structure Inputs](#current-capital-structure-inputs)
- [WACC Schedule Table](#wacc-schedule-table)
- [Optimal vs Current Comparison](#optimal-vs-current-comparison)
- [Debt Type Matching Worksheet](#debt-type-matching-worksheet)
- [Implementation Path Template](#implementation-path-template)
- [Industry Comparison Template](#industry-comparison-template)

---

## Current Capital Structure Inputs

**Company**: [Name]
**Currency**: [Analysis currency]
**Date**: [As of date]

### Operating Data

| Item                        | Value     | Source / Notes                    |
|-----------------------------|-----------|-----------------------------------|
| EBIT (Operating Income)     | $         | Most recent fiscal year           |
| Interest Expense            | $         | Total interest-bearing debt       |
| Marginal Tax Rate           |     %     | Statutory rate for jurisdiction   |
| Effective Tax Rate          |     %     | Taxes paid / Pre-tax income       |
| NOL Carryforwards           | $         | If material, affects tax shield   |

### Capital Structure Data

| Item                        | Value     | Source / Notes                    |
|-----------------------------|-----------|-----------------------------------|
| Market Value of Equity      | $         | Share price x diluted shares      |
| Book Value of Debt          | $         | Short-term + long-term debt       |
| Market Value of Debt        | $         | If traded; otherwise use BV       |
| Operating Lease Debt (PV)   | $         | Capitalize if material            |
| Cash and Marketable Securities | $      | Subtract for net debt if needed   |
| Current Debt/Capital Ratio  |     %     | D / (D + E) using market values   |
| Current D/E Ratio           |           | D / E using market values         |

### Cost of Capital Inputs

| Item                        | Value     | Source / Notes                    |
|-----------------------------|-----------|-----------------------------------|
| Riskfree Rate               |     %     | 10-year government bond yield     |
| Equity Risk Premium (ERP)   |     %     | Mature market + country premium   |
| Current Equity Beta         |           | Regression or bottom-up           |
| Unlevered Beta              |           | Calculated or from comparables    |

### Revenue and Asset Profile (for debt type matching)

| Item                           | Value     | Source / Notes                 |
|--------------------------------|-----------|--------------------------------|
| Revenue by Currency (top 3)    |           | e.g., 70% USD, 20% EUR, 10% GBP |
| Average Asset Life (years)     |           | Weighted avg of PP&E useful life |
| Cash Flow Volatility           |           | Std dev of EBIT / Mean EBIT     |
| Industry                       |           | For benchmark comparison         |

---

## WACC Schedule Table

For each debt ratio from 0% to 90%, compute all columns. The optimal is the row with the lowest WACC.

### Computation Steps (per row)

1. **D/E Ratio** = Debt Ratio / (1 - Debt Ratio)
2. **Levered Beta** = Unlevered Beta x (1 + (1 - t) x D/E)
3. **Cost of Equity** = Riskfree Rate + Levered Beta x ERP
4. **Dollar Debt** = Debt Ratio x (Firm Value at current WACC)
5. **Interest Expense** = Dollar Debt x (Riskfree Rate + Default Spread)
6. **Interest Coverage** = EBIT / Interest Expense
7. **Synthetic Rating** = Lookup from coverage-to-rating table (see methodology.md)
8. **Default Spread** = Lookup from rating-to-spread table (see methodology.md)
9. **Cost of Debt (pre-tax)** = Riskfree Rate + Default Spread
10. **Cost of Debt (after-tax)** = Cost of Debt (pre-tax) x (1 - t)
11. **WACC** = Cost of Equity x (1 - Debt Ratio) + Cost of Debt (after-tax) x Debt Ratio

### Schedule Table

| Debt Ratio | D/E    | Levered Beta | Cost of Equity | Interest Expense | Interest Coverage | Rating | Spread | Cost of Debt (AT) | WACC   |
|------------|--------|-------------|----------------|------------------|-------------------|--------|--------|--------------------|--------|
| 0%         |        |             |        %       | $                |        x          |        |    %   |        %           |    %   |
| 10%        |        |             |        %       | $                |        x          |        |    %   |        %           |    %   |
| 20%        |        |             |        %       | $                |        x          |        |    %   |        %           |    %   |
| 30%        |        |             |        %       | $                |        x          |        |    %   |        %           |    %   |
| 40%        |        |             |        %       | $                |        x          |        |    %   |        %           |    %   |
| 50%        |        |             |        %       | $                |        x          |        |    %   |        %           |    %   |
| 60%        |        |             |        %       | $                |        x          |        |    %   |        %           |    %   |
| 70%        |        |             |        %       | $                |        x          |        |    %   |        %           |    %   |
| 80%        |        |             |        %       | $                |        x          |        |    %   |        %           |    %   |
| 90%        |        |             |        %       | $                |        x          |        |    %   |        %           |    %   |

**Minimum WACC**: ____% at ____% debt ratio

### Circular Reference Note

Computing the WACC schedule involves a circularity: the dollar amount of debt depends on firm value, which depends on WACC, which depends on the debt ratio. The standard approach is to use an iterative process:

1. Start with current firm value as the initial estimate.
2. Compute WACC at each debt ratio.
3. Recompute firm value = EBIT(1-t) / WACC at the optimal.
4. Use the new firm value to recalculate dollar debt and interest expense.
5. Repeat until values converge (typically 2-3 iterations).

For a quick approximation, use the current firm value throughout.

---

## Optimal vs Current Comparison

| Metric                     | Current        | Optimal        | Change         |
|----------------------------|----------------|----------------|----------------|
| Debt Ratio (D/Capital)     |        %       |        %       |    +/- pp      |
| D/E Ratio                  |                |                |                |
| Levered Beta               |                |                |                |
| Cost of Equity             |        %       |        %       |    +/- bps     |
| Synthetic Rating           |                |                |                |
| Cost of Debt (after-tax)   |        %       |        %       |    +/- bps     |
| WACC                       |        %       |        %       |    +/- bps     |
| Firm Value (EBIT(1-t)/WACC)|  $             |  $             |  +/- $         |
| Value Enhancement          |                |                |  $             |
| Industry Avg Debt Ratio    |        %       | --             | vs optimal     |

### Interpretation Guidance

- **Value enhancement** = Firm Value (optimal) - Firm Value (current). This represents the maximum value created by moving to optimal structure, assuming stable operating income.
- If the enhancement is less than 2-3% of firm value, the restructuring may not justify transaction costs.
- If the optimal ratio is more than 20 percentage points away from current, plan a multi-year transition.

---

## Debt Type Matching Worksheet

### Step 1: Asset Duration Analysis

| Asset Category         | % of Assets | Useful Life (yrs) | Weighted Life |
|------------------------|-------------|--------------------|--------------:|
| Land and Buildings     |      %      |          yrs      |          yrs  |
| Machinery/Equipment    |      %      |          yrs      |          yrs  |
| Vehicles               |      %      |          yrs      |          yrs  |
| Intangibles/Goodwill   |      %      |          yrs      |          yrs  |
| Working Capital        |      %      |       1 yr        |          yrs  |
| **Weighted Average**   |  100%       |                   |    **__ yrs** |

**Debt maturity recommendation**: Match to weighted average asset life of ____ years.

### Step 2: Currency Matching

| Currency | % of Revenue | % of Existing Debt | Recommendation          |
|----------|-------------|--------------------|-----------------------------|
|          |      %      |         %          | Match debt to revenue share |
|          |      %      |         %          |                             |
|          |      %      |         %          |                             |

**Currency recommendation**: Denominate ___% of debt in primary revenue currency.

### Step 3: Fixed vs Floating Rate Decision

| Factor                          | Assessment        | Implication            |
|---------------------------------|-------------------|------------------------|
| Cash flow volatility            | Low / Med / High  | Low vol -> Fixed OK    |
| Revenue cyclicality             | Low / Med / High  | Cyclical -> Floating   |
| Interest rate environment       | Rising / Stable / Falling | Rising -> Float now |
| Existing rate mix               |   % fixed / % float | Current exposure      |

**Rate structure recommendation**: ___% fixed, ___% floating.

### Step 4: Consolidated Debt Type Recommendation

| Dimension         | Recommendation              | Rationale                          |
|-------------------|-----------------------------|------------------------------------|
| Maturity          | ____ years                  |                                    |
| Currency          | ___% [CCY1], ___% [CCY2]   |                                    |
| Rate Structure    | ___% fixed, ___% floating   |                                    |
| Instrument Type   | Bonds / Bank loans / Mix    |                                    |
| Seniority         | Senior / Subordinated       |                                    |

---

## Implementation Path Template

### Gradual Adjustment (Recommended when gap is moderate: 5-15 pp)

**Timeline**: 12-24 months
**Rationale**: Minimizes market disruption, allows monitoring of effects

| Phase     | Timing       | Action                                    | Target Debt Ratio |
|-----------|-------------|-------------------------------------------|--------------------|
| Phase 1   | Months 1-6  | [Issue debt / Repay debt / Refinance]     |        %           |
| Phase 2   | Months 7-12 | [Share repurchase / Further issuance]     |        %           |
| Phase 3   | Months 13-18| [Final adjustment / Reassess]             |        %           |
| Steady    | Ongoing     | Maintain ratio, opportunistic refinancing |        %           |

**Monitoring checkpoints**:
- [ ] After Phase 1: Verify credit rating matches expectations
- [ ] After Phase 2: Reassess WACC and compare to projection
- [ ] After Phase 3: Full reassessment of optimal ratio with updated inputs
- [ ] Annually: Re-run capital structure analysis with current financials

### Immediate Recapitalization (When gap is large: >15 pp, or catalyst exists)

**Timeline**: 1-3 months
**Rationale**: Captures full value enhancement quickly; appropriate when interest rates favorable or activist pressure

| Step | Action                                           | Details                    |
|------|--------------------------------------------------|----------------------------|
| 1    | Announce recapitalization plan                   | Board approval, investor comms |
| 2    | Issue debt (bonds or bank facility)              | Amount: $____, tenor: __ yrs  |
| 3    | Execute share repurchase (tender offer or open market) | Shares: ____, price: $____ |
| 4    | Update capital allocation policy                 | New target range: __-__% debt |

**Risk factors for immediate approach**:
- Market conditions may shift between announcement and execution
- Large share repurchase at current price may overpay if stock is overvalued
- Credit rating may be downgraded more than expected
- Consider whether stock is fairly valued before repurchasing

---

## Industry Comparison Template

| Metric                  | Company | Industry Median | Industry 25th | Industry 75th | Assessment     |
|-------------------------|---------|-----------------|---------------|---------------|----------------|
| Debt/Capital (Market)   |    %    |       %         |       %       |       %       | Above/Below/In-line |
| D/E Ratio               |         |                 |               |               |                |
| Interest Coverage       |    x    |       x         |       x       |       x       |                |
| Credit Rating           |         |                 |               |               |                |
| EBIT Volatility (5yr)   |    %    |       %         |       %       |       %       |                |
| Effective Tax Rate      |    %    |       %         |       %       |       %       |                |

**Industry debt ratio context**: Companies in this industry typically carry __-__% debt. The optimal ratio of __% is [within / above / below] industry norms because [reason: e.g., more stable cash flows, higher tax rate, lower asset tangibility].
