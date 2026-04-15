---
name: relative-valuation-multiples
description: Values a company relative to comparable firms using price multiples (PE, PBV, EV/EBITDA, EV/Sales). Implements the four-step framework (define, describe, analyze, apply) with both simple peer comparison and sector regression approaches. Use when valuing a company relative to peers, analyzing multiples, selecting comparable companies, or when user mentions PE ratio, EV/EBITDA, relative valuation, comparable companies, trading multiples, or price-to-book.
---
# Relative Valuation Multiples

## Table of Contents
- [Example](#example)
- [Workflow](#workflow)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Example

**Scenario**: Technology company trading at PE 35x vs. sector median 25x. Is the premium justified?

**Step 1 -- Define**: PE = Market Price per Share / Earnings per Share (trailing twelve months, diluted). Equity multiple: numerator (equity market value) and denominator (net income to equity) go to the same claimholders.

**Step 2 -- Describe**: Sector distribution of 45 software firms: mean 28x, median 25x, 25th percentile 18x, 75th percentile 33x, standard deviation 12x. Target sits at approximately the 75th percentile.

**Step 3 -- Analyze**: The fundamental driver equation for PE is:

```
PE = Payout Ratio x (1 + g) / (ke - g)
```

Target has expected earnings growth of 20% vs. sector median 12%, and beta of 0.95 vs. sector 1.1 (lower risk). Higher growth and lower risk both justify a higher PE.

**Step 4 -- Apply via sector regression**:

```
Regression (n=45, R-squared=0.62):
  PE = 8.2 + 1.5 x (Expected Growth %) - 0.3 x (Beta)

Target predicted PE:
  = 8.2 + 1.5 x (20) - 0.3 x (0.95)
  = 8.2 + 30.0 - 0.285
  = 37.9x (call it ~38x)

Actual PE = 35x
Under/overvaluation = (35 - 38) / 38 = -7.9%
```

**Conclusion**: The regression predicts a PE of ~38x given the company's growth and risk profile. At 35x, the stock appears approximately 8% undervalued relative to sector peers after controlling for fundamentals. Relative valuation suggests it is cheap relative to peers, though this does not address whether the entire sector is fairly priced.

## Workflow

Copy this checklist and track your progress:

```
Relative Valuation Analysis Progress:
- [ ] Step 1: Select appropriate multiples for company type
- [ ] Step 2: Define multiples precisely (numerator, denominator, consistency)
- [ ] Step 3: Build comparable universe and describe distributions
- [ ] Step 4: Analyze fundamental drivers of each multiple
- [ ] Step 5: Apply via simple comparison and sector regression
- [ ] Step 6: Synthesize implied values and assess relative pricing
```

**Step 1: Select appropriate multiples for company type**

Choose multiples based on company characteristics: earnings-positive companies (PE, EV/EBITDA), capital-intensive or financial firms (PBV), negative-earnings or early-stage firms (EV/Sales). Use at least two multiples for triangulation. See [resources/methodology.md](resources/methodology.md#multiple-selection-guide) for the selection decision tree.

**Step 2: Define multiples precisely**

For each selected multiple, specify: numerator (equity value or enterprise value), denominator (which earnings/book measure, what time period), and verify consistency (equity multiples use equity-level metrics; firm multiples use firm-level metrics). See [resources/methodology.md](resources/methodology.md#step-1-define-the-multiple) for definitional tests.

**Step 3: Build comparable universe and describe distributions**

Identify peer companies sharing similar risk, growth, and cash flow characteristics. Compute the multiple for each peer. Report distribution statistics: mean, median, 25th and 75th percentiles, standard deviation, count. See [resources/template.md](resources/template.md#peer-comparison-table) for the comparison table and [resources/template.md](resources/template.md#distribution-analysis-template) for distribution analysis.

**Step 4: Analyze fundamental drivers**

Every multiple has a fundamental driver derived from DCF. PE is driven by growth, risk, and payout. PBV is driven by ROE, growth, and risk. EV/EBITDA is driven by tax rate, reinvestment, growth, and WACC. Connect the company's fundamentals to its multiple. See [resources/methodology.md](resources/methodology.md#step-3-analyze-the-multiple) for driver equations and derivations.

**Step 5: Apply via simple comparison and sector regression**

Two approaches: (a) Simple comparison -- compare target's multiple to peer median, adjust qualitatively for fundamental differences. (b) Sector regression -- regress the multiple against its fundamental drivers across the peer universe, plug in the target's values, and compute predicted multiple. See [resources/template.md](resources/template.md#sector-regression-template) for the regression template.

**Step 6: Synthesize implied values**

Convert predicted multiples to implied share prices or enterprise values. Compute under/overvaluation percentage. Compare results across multiples for consistency. Validate using [resources/evaluators/rubric_relative_valuation_multiples.json](resources/evaluators/rubric_relative_valuation_multiples.json). **Minimum standard**: Average score of 3.5 or above.

## Common Patterns

**Pattern 1: PE Ratio Analysis**
- **When**: Earnings-positive companies, cross-sector comparisons where earnings quality is comparable
- **Multiple**: PE = Price / EPS (use diluted, trailing twelve months for consistency)
- **Fundamental driver**: PE = Payout x (1+g) / (ke - g). Higher growth and lower risk justify higher PE
- **Regression variables**: Expected earnings growth rate, beta (or other risk proxy), payout ratio
- **Pitfall**: PE is undefined for negative-earnings firms. Cyclical earnings distort trailing PE; use normalized earnings

**Pattern 2: EV/EBITDA Analysis**
- **When**: Comparing firms with different capital structures or across tax jurisdictions. Good for capital-intensive industries
- **Multiple**: EV/EBITDA = (Market Cap + Debt - Cash) / EBITDA
- **Fundamental driver**: Driven by tax rate, depreciation-to-EBITDA ratio, reinvestment rate, WACC, and growth
- **Regression variables**: Expected revenue or EBITDA growth, tax rate, reinvestment rate, WACC
- **Pitfall**: EBITDA ignores capital expenditure differences. Firms with heavy capex relative to depreciation may look artificially cheap

**Pattern 3: PBV (Price-to-Book) Analysis**
- **When**: Financial services (banks, insurance), capital-intensive industries, or when earnings are volatile
- **Multiple**: PBV = Price / Book Value per Share
- **Fundamental driver**: PBV = (ROE - g) / (ke - g). Higher ROE relative to cost of equity justifies higher PBV
- **Regression variables**: ROE, expected growth in earnings, beta or cost of equity
- **Pitfall**: Book value depends on accounting conventions (historical cost vs. fair value). Cross-country comparisons require consistent accounting standards

**Pattern 4: EV/Sales (Revenue Multiple) Analysis**
- **When**: Early-stage companies, negative-earnings firms, or when comparing firms with very different margin structures
- **Multiple**: EV/Sales = (Market Cap + Debt - Cash) / Revenue
- **Fundamental driver**: EV/Sales = After-tax operating margin x (1 - Reinvestment Rate) x (1+g) / (WACC - g). Margin is the key driver
- **Regression variables**: Expected revenue growth, operating margin (or net margin), WACC
- **Pitfall**: A low EV/Sales multiple may simply reflect low margins, not undervaluation. Control for profitability differences

## Guardrails

1. **Numerator-denominator consistency**: Equity multiples (PE, PBV) use market value of equity in the numerator and equity-level metrics in the denominator. Firm multiples (EV/EBITDA, EV/Sales) use enterprise value in the numerator and firm-level metrics in the denominator. Mixing levels produces meaningless numbers.

2. **Comparable universe quality**: Comparable companies should share similar risk, growth, and cash flow characteristics. Same industry is a starting point, not a guarantee of comparability. A fast-growing SaaS firm is not comparable to a mature enterprise software firm just because both are "technology."

3. **Report distribution statistics**: Present mean, median, 25th and 75th percentiles, standard deviation, and count. Median is more robust than mean for skewed distributions (PE ratios are heavily right-skewed). Do not rely on the average alone.

4. **Regression sample size**: Sector regressions require a minimum of 15-20 data points to produce meaningful results. Below that threshold, prefer simple peer comparison with qualitative adjustments. Report R-squared to indicate explanatory power.

5. **Negative denominators**: Exclude firms with negative earnings from PE analysis (negative PE has no economic meaning). For EV/EBITDA, exclude firms with negative EBITDA. For PBV, exclude firms with negative book value. Document how many firms were excluded and why.

6. **Fundamental driver linkage**: Every multiple is a compressed DCF. Always identify the fundamental driver equation connecting the multiple to growth, risk, and cash flow patterns. A company trading at a high PE is not "expensive" if its growth and risk profile justify it.

7. **Relative vs. absolute**: Relative valuation tells you whether a stock is cheap or expensive relative to its peers. It does not tell you whether the stock is undervalued or overvalued in absolute terms. If the entire sector is overpriced, the "cheapest" stock in the sector may still be overvalued.

## Quick Reference

**Key formulas:**

```
PE = Market Price per Share / Earnings per Share
PBV = Market Price per Share / Book Value per Share
EV/EBITDA = Enterprise Value / EBITDA
EV/Sales = Enterprise Value / Revenue
Enterprise Value = Market Cap + Market Value of Debt - Cash

Fundamental Driver Equations:

PE (stable growth):
  PE = Payout Ratio x (1 + g) / (ke - g)
  where Payout = 1 - (g / ROE)

PBV (stable growth):
  PBV = (ROE - g) / (ke - g)

EV/EBITDA:
  EV/EBITDA = (1 - t) x (1 - Reinvestment Rate / (1-t)) x (1 + g) / (WACC - g)
  simplified: driven by tax rate, depreciation/EBITDA, reinvestment, WACC, growth

EV/Sales (stable growth):
  EV/Sales = After-tax Operating Margin x (1 - Reinvestment Rate) x (1 + g) / (WACC - g)

Sector Regression (general form):
  Multiple = a + b1(Growth) + b2(Risk) + b3(Payout or Margin)

Under/Overvaluation:
  = (Actual Multiple - Predicted Multiple) / Predicted Multiple
```

**Multiple selection by company type:**

| Company Type | Primary Multiple | Secondary Multiple | Rationale |
|---|---|---|---|
| Earnings-positive, stable | PE | EV/EBITDA | Earnings reliable, PE intuitive |
| Capital-intensive | EV/EBITDA | PBV | EBITDA normalizes for depreciation methods |
| Financial services | PBV | PE | Book value is economically meaningful for banks |
| Negative earnings / early-stage | EV/Sales | EV/EBITDA (if positive) | Revenue exists even when earnings do not |
| Cross-border comparison | EV/EBITDA | EV/Sales | Firm multiples are capital-structure neutral |
| High-growth technology | EV/Sales | PE (forward) | Revenue growth is the primary value driver |

**Key resources:**

- **[resources/template.md](resources/template.md)**: Peer selection criteria, comparison table, distribution analysis, regression template, implied value calculation
- **[resources/methodology.md](resources/methodology.md)**: Four-step framework in detail, fundamental driver derivations, sector regression technique, cross-sectional market regression
- **[resources/evaluators/rubric_relative_valuation_multiples.json](resources/evaluators/rubric_relative_valuation_multiples.json)**: Quality criteria for definition consistency, comparable universe, distribution analysis, regression quality

**Inputs required:**

- **Target company financials**: EPS, book value per share, EBITDA, revenue, market cap, debt, cash
- **Comparable company data**: Same financial metrics for each peer (15-20 minimum for regression)
- **Growth estimates**: Expected earnings or revenue growth rates for target and peers
- **Risk measures**: Beta, debt ratio, cost of equity or WACC for target and peers
- **Profitability measures**: ROE, operating margin, payout ratio for target and peers

**Outputs produced:**

- `relative-valuation-analysis.md`: Full analysis with peer comparison, distribution statistics, regression output, implied values, and under/overvaluation assessment
