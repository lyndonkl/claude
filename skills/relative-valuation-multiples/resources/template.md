# Relative Valuation Templates

Templates for peer selection, comparison tables, distribution analysis, sector regression, and implied value calculation.

## Table of Contents
- [Workflow](#workflow)
- [Peer Selection Criteria](#peer-selection-criteria)
- [Peer Comparison Table](#peer-comparison-table)
- [Distribution Analysis Template](#distribution-analysis-template)
- [Sector Regression Template](#sector-regression-template)
- [Simple Comparison Template](#simple-comparison-template)
- [Implied Value Calculation](#implied-value-calculation)
- [Over/Under Valuation Summary](#overunder-valuation-summary)
- [Complete Analysis Template](#complete-analysis-template)

---

## Workflow

```
Relative Valuation Analysis Progress:
- [ ] Step 1: Select appropriate multiples for company type
- [ ] Step 2: Define multiples precisely (numerator, denominator, consistency)
- [ ] Step 3: Build comparable universe and describe distributions
- [ ] Step 4: Analyze fundamental drivers of each multiple
- [ ] Step 5: Apply via simple comparison and sector regression
- [ ] Step 6: Synthesize implied values and assess relative pricing
```

**Step 1**: Select multiples using the company type table in SKILL.md Quick Reference.

**Step 2**: Define each multiple precisely using [methodology.md - Step 1: Define the Multiple](methodology.md#step-1-define-the-multiple).

**Step 3**: Build the comparable universe using [Peer Selection Criteria](#peer-selection-criteria), then populate the [Peer Comparison Table](#peer-comparison-table) and the [Distribution Analysis Template](#distribution-analysis-template).

**Step 4**: Identify fundamental drivers using [methodology.md - Step 3: Analyze the Multiple](methodology.md#step-3-analyze-the-multiple).

**Step 5**: Apply using [Simple Comparison Template](#simple-comparison-template) and/or [Sector Regression Template](#sector-regression-template).

**Step 6**: Calculate implied values with [Implied Value Calculation](#implied-value-calculation) and summarize in [Over/Under Valuation Summary](#overunder-valuation-summary).

---

## Peer Selection Criteria

**Target Company**: [Name]
**Industry**: [Sector/Sub-sector]
**Market Cap**: [Size]

### Selection Criteria Checklist

- [ ] **Same industry or sub-sector**: Firms face similar competitive dynamics and regulatory environment
- [ ] **Similar size**: Within 0.5x to 2x of target market cap (or revenue) to avoid scale distortions
- [ ] **Similar growth profile**: Expected growth rate within a reasonable range of the target
- [ ] **Similar risk profile**: Comparable leverage, beta, geographic exposure
- [ ] **Similar business model**: Revenue mix (subscription vs. transactional), margin structure, capital intensity
- [ ] **Positive denominator**: Exclude firms with negative earnings (for PE), negative EBITDA, or negative book value as applicable
- [ ] **Sufficient count**: Aim for 15-20 peers for regression; minimum 5-8 for simple comparison

### Peer Screening Results

| Criterion | Filter Applied | Firms Remaining |
|---|---|---|
| Starting universe | [Industry classification] | [N] |
| Size filter | Market cap [range] | [N] |
| Profitability filter | [Earnings/EBITDA positive] | [N] |
| Geography filter | [Region if applicable] | [N] |
| Business model filter | [Criteria] | [N] |
| **Final peer set** | | **[N]** |

**Firms excluded and rationale**: [List any notable exclusions and why]

---

## Peer Comparison Table

### PE Ratio Comparison

| Company | Price | EPS (TTM) | PE Ratio | Expected Growth (%) | Beta | Payout Ratio (%) |
|---|---|---|---|---|---|---|
| **Target** | | | | | | |
| Peer 1 | | | | | | |
| Peer 2 | | | | | | |
| Peer 3 | | | | | | |
| ... | | | | | | |
| **Median** | -- | -- | | | | |
| **Mean** | -- | -- | | | | |

### EV/EBITDA Comparison

| Company | Market Cap | Debt | Cash | EV | EBITDA | EV/EBITDA | Growth (%) | WACC (%) | Tax Rate (%) |
|---|---|---|---|---|---|---|---|---|---|
| **Target** | | | | | | | | | |
| Peer 1 | | | | | | | | | |
| Peer 2 | | | | | | | | | |
| ... | | | | | | | | | |
| **Median** | -- | -- | -- | -- | -- | | | | |

### PBV Comparison

| Company | Price | BV/Share | PBV | ROE (%) | Expected Growth (%) | Beta |
|---|---|---|---|---|---|---|
| **Target** | | | | | | |
| Peer 1 | | | | | | |
| ... | | | | | | |
| **Median** | -- | -- | | | | |

### EV/Sales Comparison

| Company | EV | Revenue | EV/Sales | Operating Margin (%) | Growth (%) | WACC (%) |
|---|---|---|---|---|---|---|
| **Target** | | | | | | |
| Peer 1 | | | | | | |
| ... | | | | | | |
| **Median** | -- | -- | | | | |

---

## Distribution Analysis Template

**Multiple analyzed**: [PE / EV/EBITDA / PBV / EV/Sales]
**Universe**: [Description of peer set, N firms]
**Date**: [As of date]

### Summary Statistics

| Statistic | Value |
|---|---|
| Count (N) | |
| Mean | |
| Median | |
| Standard Deviation | |
| 10th Percentile | |
| 25th Percentile (Q1) | |
| 75th Percentile (Q3) | |
| 90th Percentile | |
| Minimum | |
| Maximum | |
| Skewness | [Positive/Negative/Roughly symmetric] |

### Target Positioning

| Metric | Value |
|---|---|
| Target's actual multiple | |
| Percentile rank in distribution | |
| Distance from median | [+/- X% above/below] |
| Distance from mean | [+/- X% above/below] |

### Distribution Sketch

```
Frequency
|
|   *
|   **
|  ****
| ******      *
|*********  ***
|___________________
Low    Median    High

Target position: [Mark approximate location]
```

### Interpretation

- [ ] Target above median: potential premium (justify with fundamentals or flag as overpriced)
- [ ] Target below median: potential discount (justify with fundamentals or flag as undervalued)
- [ ] Target near median: fairly priced relative to peers
- [ ] Distribution is heavily skewed: median is more reliable than mean
- [ ] Outliers present: consider excluding and re-computing

---

## Sector Regression Template

### Regression Specification

**Dependent variable (Y)**: [Multiple, e.g., PE]
**Independent variables (X)**:
- X1: [e.g., Expected Earnings Growth %]
- X2: [e.g., Beta]
- X3: [e.g., Payout Ratio %]

**Sample**: [N] firms in [sector/industry], as of [date]
**Firms excluded**: [Count] with negative denominators

### Regression Output

```
Y = a + b1(X1) + b2(X2) + b3(X3)

Coefficients:
  Intercept (a):    [value]  (t-stat: [value])
  b1 (Growth):      [value]  (t-stat: [value])
  b2 (Risk):        [value]  (t-stat: [value])
  b3 (Payout/Margin): [value]  (t-stat: [value])

R-squared:          [value]
Adjusted R-squared: [value]
Standard Error:     [value]
F-statistic:        [value]
N:                  [value]
```

### Coefficient Interpretation

| Variable | Coefficient | Direction | Economic Meaning |
|---|---|---|---|
| Growth | [b1] | [+/-] | Each 1% increase in growth adds [b1] to the multiple |
| Risk | [b2] | [+/-] | Each 1-unit increase in beta changes the multiple by [b2] |
| Payout/Margin | [b3] | [+/-] | Each 1% increase changes the multiple by [b3] |

### Quality Assessment

- [ ] R-squared above 0.40 (regression explains meaningful variation)
- [ ] Coefficient signs match economic intuition (growth positive for PE, risk negative)
- [ ] T-statistics above 2.0 for key variables (statistically significant)
- [ ] Sample size at least 15-20 firms
- [ ] No severe multicollinearity (growth and payout may be correlated)

### Target Company Prediction

```
Target fundamentals:
  X1 (Growth):       [value]
  X2 (Risk):         [value]
  X3 (Payout/Margin): [value]

Predicted multiple = a + b1([X1]) + b2([X2]) + b3([X3])
                   = [calculation]
                   = [predicted multiple]

Actual multiple    = [value]

Under/overvaluation = (Actual - Predicted) / Predicted
                    = ([actual] - [predicted]) / [predicted]
                    = [X%]
```

### Interpretation

- [ ] Actual > Predicted by more than 15%: stock looks overpriced relative to fundamentals
- [ ] Actual < Predicted by more than 15%: stock looks underpriced relative to fundamentals
- [ ] Actual within 15% of Predicted: stock is approximately fairly priced relative to peers
- [ ] R-squared is low (< 0.30): regression has limited explanatory power; treat result with caution

---

## Simple Comparison Template

Use when the peer set is too small for regression (fewer than 15 firms) or as a complement to the regression approach.

### Comparison Summary

| Metric | Target | Peer Median | Target vs. Median |
|---|---|---|---|
| Multiple (e.g., PE) | | | [+X% premium / -X% discount] |
| Growth rate | | | [Higher / Lower / Similar] |
| Risk (beta) | | | [Higher / Lower / Similar] |
| Profitability (margin or ROE) | | | [Higher / Lower / Similar] |

### Qualitative Assessment

**Growth comparison**: [Target growth rate vs. peer median. Does higher/lower growth justify the premium/discount?]

**Risk comparison**: [Target risk vs. peer median. Does higher/lower risk justify the premium/discount?]

**Profitability comparison**: [Target margin or ROE vs. peer median. Does higher/lower profitability justify the premium/discount?]

### Adjusted Fair Multiple

```
Starting point: Peer median multiple = [value]

Adjustments:
  + Growth premium/discount:      [+/- X]  (growth is [X%] above/below median)
  + Risk premium/discount:        [+/- X]  (beta is [X] above/below median)
  + Profitability adjustment:     [+/- X]  (margin is [X%] above/below median)

Adjusted fair multiple:           [value]
```

---

## Implied Value Calculation

### From PE

```
Predicted PE (from regression or adjusted peer median) = [value]
Target EPS = [value]
Implied Price = Predicted PE x EPS = [value]
Current Price = [value]
Under/overvaluation = (Implied - Current) / Implied = [X%]
```

### From EV/EBITDA

```
Predicted EV/EBITDA = [value]
Target EBITDA = [value]
Implied EV = Predicted EV/EBITDA x EBITDA = [value]
Subtract: Market value of debt = [value]
Add: Cash = [value]
Implied Equity Value = [value]
Shares outstanding = [value]
Implied Price per Share = [value]
Current Price = [value]
Under/overvaluation = (Implied - Current) / Implied = [X%]
```

### From PBV

```
Predicted PBV = [value]
Target Book Value per Share = [value]
Implied Price = Predicted PBV x BV/Share = [value]
Current Price = [value]
Under/overvaluation = (Implied - Current) / Implied = [X%]
```

### From EV/Sales

```
Predicted EV/Sales = [value]
Target Revenue = [value]
Implied EV = Predicted EV/Sales x Revenue = [value]
Subtract: Market value of debt = [value]
Add: Cash = [value]
Implied Equity Value = [value]
Shares outstanding = [value]
Implied Price per Share = [value]
Current Price = [value]
Under/overvaluation = (Implied - Current) / Implied = [X%]
```

---

## Over/Under Valuation Summary

### Multi-Multiple Summary

| Multiple | Method | Predicted Multiple | Actual Multiple | Implied Price | Current Price | Over/Under (%) |
|---|---|---|---|---|---|---|
| PE | Regression | | | | | |
| PE | Simple comparison | | | | | |
| EV/EBITDA | Regression | | | | | |
| EV/EBITDA | Simple comparison | | | | | |
| PBV | Regression | | | | | |
| EV/Sales | Regression | | | | | |

### Consistency Check

- [ ] Multiple methods agree on direction (all say over- or under-valued)
- [ ] Implied prices are within 20% of each other across methods
- [ ] If results diverge: identify which multiple is most appropriate for this company type and weight accordingly

### Final Relative Valuation Estimate

**Weighted implied price**: [value] (weights based on relevance of each multiple to company type)

**Current market price**: [value]

**Relative valuation assessment**: [Undervalued / Overvalued / Fairly priced] by approximately [X%] relative to peer group

**Key caveat**: This assessment is relative to the peer group. If the sector as a whole is over- or under-priced by the market, the absolute conclusion may differ. Cross-reference with intrinsic (DCF) valuation for a complete picture.

---

## Complete Analysis Template

Structure for full documentation:

1. **Company overview**: Target company name, industry, current price, market cap, key financials
2. **Multiple selection**: Which multiples were chosen and why (linked to company type)
3. **Multiple definition**: Precise definition of each multiple (numerator, denominator, time period, dilution treatment)
4. **Peer universe**: Selection criteria, screening process, final peer list with rationale
5. **Distribution analysis**: Summary statistics, target percentile positioning, skewness assessment
6. **Fundamental driver analysis**: Driver equation for each multiple, target's position on each driver
7. **Simple comparison**: Target vs. peer median with qualitative adjustments for fundamental differences
8. **Sector regression**: Specification, output, coefficient interpretation, target prediction
9. **Implied values**: Predicted multiple to implied price for each approach
10. **Synthesis**: Multi-multiple summary table, consistency check, weighted implied price, relative valuation verdict
11. **Caveats**: Regression R-squared, sample size limitations, relative-not-absolute nature of conclusion
