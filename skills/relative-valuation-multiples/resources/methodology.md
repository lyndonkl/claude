# Relative Valuation Methodology

Detailed framework for defining, describing, analyzing, and applying multiples. Includes fundamental driver derivations, sector regression techniques, and cross-sectional market regression.

## Table of Contents
- [Workflow](#workflow)
- [Multiple Selection Guide](#multiple-selection-guide)
- [The Four-Step Framework](#the-four-step-framework)
  - [Step 1: Define the Multiple](#step-1-define-the-multiple)
  - [Step 2: Describe the Multiple](#step-2-describe-the-multiple)
  - [Step 3: Analyze the Multiple](#step-3-analyze-the-multiple)
  - [Step 4: Apply the Multiple](#step-4-apply-the-multiple)
- [Fundamental Driver Equations](#fundamental-driver-equations)
- [Sector Regression Technique](#sector-regression-technique)
- [Cross-Sectional Market Regression](#cross-sectional-market-regression)
- [Common Pitfalls in Relative Valuation](#common-pitfalls-in-relative-valuation)

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

**Step 1**: Use the [Multiple Selection Guide](#multiple-selection-guide) to choose appropriate multiples.

**Step 2-5**: Follow the [Four-Step Framework](#the-four-step-framework) for each selected multiple.

**Step 6**: Synthesize results using [template.md - Over/Under Valuation Summary](template.md#overunder-valuation-summary).

---

## Multiple Selection Guide

The choice of multiple depends on the company's characteristics. Different multiples emphasize different value drivers.

### Decision Tree

```
Is the company profitable (positive net income)?
  |
  YES --> Are earnings stable and recurring?
  |         |
  |         YES --> PE is the primary multiple
  |         |       Add EV/EBITDA as a cross-check
  |         |
  |         NO (cyclical or volatile earnings) -->
  |                 Use normalized PE or EV/EBITDA
  |                 PBV as secondary for capital-intensive firms
  |
  NO (negative earnings) --> Is EBITDA positive?
            |
            YES --> EV/EBITDA is primary
            |       EV/Sales as secondary
            |
            NO --> EV/Sales is primary
                   Consider whether the company is a candidate
                   for special-situations-valuation instead
```

### Special Cases

**Financial services firms (banks, insurance, asset managers)**:
- Use PBV as the primary multiple (book value has economic meaning for financial firms)
- PE as secondary
- Do not use EV/EBITDA (debt is operational for financial firms, not financing)

**REITs and MLPs**:
- Use Price/FFO (funds from operations) or Price/AFFO (adjusted FFO)
- PBV as secondary
- Conventional earnings multiples are distorted by depreciation accounting

**Commodity companies (oil, mining, materials)**:
- Use EV/EBITDA with normalized commodity prices
- PBV as secondary
- PE is unreliable due to commodity price volatility

---

## The Four-Step Framework

Based on Damodaran's approach to deconstructing multiples: every relative valuation should follow these four steps in sequence.

### Step 1: Define the Multiple

**Goal**: Ensure the multiple is consistently defined across all firms being compared.

**Consistency test 1 -- Claimholder match**: The numerator and denominator must accrue to the same claimholders.
- Equity multiples: Market value of equity in the numerator, equity-level metric in the denominator
  - PE = Price per Share / Earnings per Share (both equity)
  - PBV = Price per Share / Book Value per Share (both equity)
  - Price/FCFE = Price per Share / Free Cash Flow to Equity per Share
- Firm multiples: Enterprise value in the numerator, firm-level metric in the denominator
  - EV/EBITDA = Enterprise Value / EBITDA (both firm-level)
  - EV/Sales = Enterprise Value / Revenue (both firm-level)
  - EV/FCFF = Enterprise Value / Free Cash Flow to Firm

**Common error**: Dividing enterprise value by net income (mixing firm numerator with equity denominator), or dividing price by EBITDA (mixing equity numerator with firm denominator).

**Consistency test 2 -- Uniform estimation**: The same accounting rules and time periods should be applied across all comparable firms.
- Time period: Use trailing twelve months (TTM) for all firms, or forward estimates for all. Do not mix trailing PE for some firms with forward PE for others.
- Dilution: Use diluted shares consistently (treasury stock method for options). Either all firms use primary EPS or all use diluted EPS.
- Accounting standards: If comparing firms across countries, adjust for GAAP vs. IFRS differences (capitalization rules, lease treatment, goodwill amortization).

**Definition checklist for each multiple**:

| Element | Specify |
|---|---|
| Numerator | Market value of equity or enterprise value? |
| Denominator | Which metric? (EPS, BV, EBITDA, Revenue) |
| Time period | Trailing 12 months, most recent fiscal year, or forward estimate? |
| Dilution treatment | Primary shares or diluted shares? |
| Adjustments | Any normalization (cyclical adjustment, one-time items)? |

---

### Step 2: Describe the Multiple

**Goal**: Understand the cross-sectional distribution of the multiple before passing judgment on any single company's value.

**Why this matters**: If PE ratios in a sector range from 8x to 80x with a median of 20x, a PE of 25x looks reasonable. If the range is 15x to 25x with a median of 20x, the same PE of 25x looks high. Context from the distribution is essential.

**Distribution statistics to report**:
- **Count (N)**: How many firms in the peer set
- **Mean**: Average multiple (sensitive to outliers, especially for PE)
- **Median**: Middle value (more robust for skewed distributions)
- **Standard deviation**: Spread around the mean
- **Percentiles**: 10th, 25th, 75th, 90th (where does the target fall?)
- **Range**: Minimum and maximum (flag outliers)
- **Skewness**: PE ratios are almost always right-skewed (long right tail). When skewness is high, the mean is misleading; prefer the median.

**Handling outliers**:
- Identify outliers (e.g., PE > 100x or PE < 5x)
- Investigate whether outliers reflect temporary distortions (one-time charge, cyclical trough) or genuinely different firms
- Consider winsorizing (capping at 5th/95th percentile) or trimming extremes for regression purposes
- Report results both with and without outliers if they materially affect the analysis

---

### Step 3: Analyze the Multiple

**Goal**: Identify the fundamental variables that drive the multiple and their relationship to it. This connects relative valuation to DCF.

**Core insight**: Every multiple can be derived from a DCF model. The multiple is a function of growth, risk, and cash flow patterns. Understanding these drivers lets you determine whether a premium or discount relative to peers is justified by fundamentals or by market mispricing.

Detailed derivations are in [Fundamental Driver Equations](#fundamental-driver-equations) below.

**Summary of drivers by multiple**:

| Multiple | Key Drivers | Positive Effect | Negative Effect |
|---|---|---|---|
| PE | Growth, Risk, Payout | Higher growth raises PE | Higher risk (ke) lowers PE |
| PBV | ROE, Growth, Risk | Higher ROE raises PBV | Higher risk (ke) lowers PBV |
| EV/EBITDA | Growth, Reinvestment, Tax, WACC | Higher growth raises multiple | Higher WACC lowers multiple |
| EV/Sales | Margin, Growth, Reinvestment, WACC | Higher margin raises multiple | Higher WACC lowers multiple |

**Analytical process**:
1. Write the fundamental driver equation for the multiple
2. For each driver variable, determine whether the target company is above or below the peer median
3. Assess whether the direction and magnitude of the target's multiple relative to the peer median is consistent with its fundamental driver profile
4. If the target's multiple is higher than its fundamentals suggest, it may be overpriced (or have qualitative advantages not captured by the regression variables)

---

### Step 4: Apply the Multiple

**Goal**: Use the multiple to estimate the value of the target company, controlling for differences between the target and its peers.

**Two approaches**:

**Approach A -- Simple Peer Comparison**:
1. Compute the peer median multiple
2. Qualitatively adjust for fundamental differences (growth, risk, profitability)
3. Multiply the adjusted multiple by the target's denominator to get implied value
4. Best for small peer sets (5-15 firms) or as a sanity check

**Approach B -- Sector Regression**:
1. Regress the multiple against its fundamental driver variables across all peers
2. Plug in the target's fundamental values to compute a predicted multiple
3. Compare actual to predicted to assess relative pricing
4. Best for larger peer sets (15+ firms) where statistical analysis is meaningful

Both approaches should be used when data permits. See [Sector Regression Technique](#sector-regression-technique) for details on Approach B.

---

## Fundamental Driver Equations

These derivations show how each multiple connects to DCF through growth, risk, and cash flow patterns.

### PE Ratio -- Derivation

Starting from the stable-growth DDM:

```
P0 = DPS1 / (ke - g)
```

where P0 = price, DPS1 = expected dividends next year, ke = cost of equity, g = stable growth rate.

Substitute DPS1 = EPS1 x Payout Ratio:

```
P0 = EPS1 x Payout Ratio / (ke - g)
```

Divide both sides by EPS1:

```
P0 / EPS1 = Payout Ratio / (ke - g)
```

For trailing PE (divide by EPS0):

```
P0 / EPS0 = Payout Ratio x (1 + g) / (ke - g)
```

**Fundamental driver equation for PE**:

```
PE = Payout x (1 + g) / (ke - g)
```

**Implications**:
- PE increases with higher expected growth rate (g)
- PE increases with higher payout ratio (for given growth)
- PE decreases with higher cost of equity (ke, which reflects risk)
- Since Payout = 1 - g/ROE, a firm with higher ROE can pay more out while maintaining the same growth

**For high-growth firms (two-stage)**:

```
PE = [Payout_hg x (1+g_hg) x (1 - (1+g_hg)^n / (1+ke_hg)^n)] / (ke_hg - g_hg)
   + [Payout_st x (1+g_st) x (1+g_hg)^n / ((ke_st - g_st) x (1+ke_hg)^n)]
```

where hg = high-growth period, st = stable period, n = years of high growth.

---

### PBV (Price-to-Book) -- Derivation

Starting from the DDM:

```
P0 = DPS1 / (ke - g) = EPS1 x Payout / (ke - g)
```

Substitute EPS1 = BV0 x ROE:

```
P0 = BV0 x ROE x Payout / (ke - g)
```

Divide both sides by BV0:

```
P0 / BV0 = ROE x Payout / (ke - g)
```

Since Payout = 1 - g/ROE:

```
PBV = ROE x (1 - g/ROE) / (ke - g) = (ROE - g) / (ke - g)
```

**Fundamental driver equation for PBV**:

```
PBV = (ROE - g) / (ke - g)
```

**Implications**:
- PBV increases with higher ROE (the key driver for this multiple)
- If ROE = ke, then PBV = 1.0 (firm earns exactly its cost of equity)
- If ROE > ke, PBV > 1.0 (firm creates value, market pays premium to book)
- If ROE < ke, PBV < 1.0 (firm destroys value, market discounts below book)
- PBV increases with higher growth (if ROE > ke)

**Why PBV matters for financial services**:
Banks and insurance companies hold assets at or near market value. Book value is a more economically meaningful anchor than for industrial companies where assets are recorded at historical cost. ROE is the natural profitability measure for firms whose primary business is managing a balance sheet.

---

### EV/EBITDA -- Derivation

Starting from the FCFF-based firm value:

```
Firm Value = FCFF1 / (WACC - g)
           = EBIT(1-t)(1 - Reinvestment Rate) x (1+g) / (WACC - g)
```

Enterprise Value adds back depreciation to get to EBITDA:

```
EV/EBITDA = [(EBIT/EBITDA)(1-t)(1 - Reinvestment Rate) x (1+g)] / (WACC - g)
```

Since EBIT = EBITDA - D&A, the ratio EBIT/EBITDA = 1 - (D&A/EBITDA):

```
EV/EBITDA = [(1 - DA/EBITDA)(1-t)(1 - Reinvestment Rate) x (1+g)] / (WACC - g)
```

**Fundamental driver equation for EV/EBITDA**:

```
EV/EBITDA = f(Tax Rate, DA/EBITDA, Reinvestment Rate, WACC, Growth)
```

**Implications**:
- EV/EBITDA increases with higher expected growth
- EV/EBITDA decreases with higher WACC (discount rate)
- EV/EBITDA decreases with higher tax rate (more cash to government)
- EV/EBITDA decreases with higher reinvestment needs
- EV/EBITDA increases when DA/EBITDA is lower (less depreciation relative to EBITDA)
- Two firms with identical EBITDA but different capex requirements should trade at different EV/EBITDA

---

### EV/Sales -- Derivation

Starting from the FCFF-based firm value:

```
Firm Value = Revenue x After-tax Operating Margin x (1 - Reinvestment Rate) x (1+g) / (WACC - g)
```

Divide both sides by Revenue:

```
EV/Sales = After-tax Margin x (1 - Reinvestment Rate) x (1+g) / (WACC - g)
```

**Fundamental driver equation for EV/Sales**:

```
EV/Sales = After-tax Operating Margin x (1 - Reinvestment Rate) x (1+g) / (WACC - g)
```

**Implications**:
- EV/Sales increases with higher after-tax operating margin (the dominant driver)
- EV/Sales increases with higher expected growth
- EV/Sales decreases with higher WACC
- EV/Sales decreases with higher reinvestment needs
- A low EV/Sales multiple may reflect low margins, not undervaluation. Two firms with the same revenue but 5% vs. 25% operating margin should trade at very different EV/Sales multiples.

---

## Sector Regression Technique

Sector regression is the most rigorous approach to controlling for differences between firms within a peer group.

### Step-by-Step Procedure

**1. Assemble the data set**

Collect for each firm in the sector:
- Dependent variable: The multiple (e.g., PE, EV/EBITDA)
- Independent variables: The fundamental drivers identified in the Analyze step
  - For PE: Expected earnings growth, beta, payout ratio
  - For PBV: ROE, expected growth, beta
  - For EV/EBITDA: Expected EBITDA growth, tax rate, reinvestment rate, WACC
  - For EV/Sales: Expected revenue growth, operating margin, WACC

Clean the data:
- Remove firms with negative denominators (negative PE is meaningless)
- Consider removing extreme outliers (PE > 100x) or winsorizing
- Verify that growth rates, betas, and margins are current and consistent across firms

**2. Run the regression**

Regress the multiple against the driver variables using ordinary least squares (OLS):

```
Multiple_i = a + b1(X1_i) + b2(X2_i) + ... + e_i
```

Example for PE:
```
PE_i = a + b1(Expected Growth_i) + b2(Beta_i) + b3(Payout_i) + e_i
```

**3. Evaluate the regression quality**

| Metric | Interpretation |
|---|---|
| R-squared | Proportion of variation explained. Above 0.40 is reasonable for cross-sectional multiple regressions. Above 0.60 is good. |
| Adjusted R-squared | Penalizes for additional variables. Use when comparing regressions with different numbers of predictors. |
| Coefficient signs | Should match economic intuition. Growth coefficient should be positive for PE. Beta coefficient should be negative for PE. |
| T-statistics | Above 2.0 indicates statistical significance at the 5% level. Focus on the sign and magnitude of coefficients whose t-stats are significant. |
| F-statistic | Tests whether the regression as a whole is significant. Should have p-value < 0.05. |
| Standard error | Measures prediction uncertainty. A standard error of 5 on a predicted PE of 25 means the 95% prediction interval is roughly 15 to 35. |

**4. Predict the target's multiple**

Plug the target company's fundamental values into the regression equation:

```
Predicted PE = a + b1(Target Growth) + b2(Target Beta) + b3(Target Payout)
```

**5. Compare actual to predicted**

```
Relative pricing = (Actual Multiple - Predicted Multiple) / Predicted Multiple
```

- If positive: stock trades at a premium to what fundamentals suggest (potentially overpriced)
- If negative: stock trades at a discount to what fundamentals suggest (potentially underpriced)
- If within about 1 standard error: the difference is not statistically significant

### Limitations of Sector Regression

- **Small sample size**: With fewer than 15 firms, regression estimates are unreliable. Consider simple comparison instead.
- **Multicollinearity**: Growth and payout are correlated (high-growth firms retain more). Consider dropping one variable if variance inflation factors are high.
- **Nonlinearity**: The relationship between growth and PE may not be linear. For extreme growth rates, the PE can increase exponentially. Consider log transformations if the scatter plot shows curvature.
- **Outlier sensitivity**: A single outlier can shift the regression line substantially. Check Cook's distance and re-run without influential observations.
- **Point-in-time snapshot**: Regressions reflect current market conditions. They do not predict future multiples.

---

## Cross-Sectional Market Regression

An alternative to sector regression: regress the multiple against fundamentals across the entire market rather than just one sector.

### When to Use

- When the sector is too small for a meaningful regression (fewer than 15 peers)
- When you want a broader perspective on how the market prices the fundamental drivers
- As a supplement to the sector regression to check consistency

### Procedure

1. Gather data on the multiple and its drivers for all firms in the market (or a broad cross-section, e.g., all US-listed firms with positive earnings)
2. Run the regression across the full sample
3. Plug in the target's fundamentals to get a market-wide predicted multiple
4. Compare actual to predicted

### Interpreting the Results

- The market-wide regression captures how the entire market trades off growth, risk, and profitability
- If the sector regression and the market regression give similar predictions, confidence increases
- If they diverge, the sector may be trading at a premium or discount relative to the broader market (sector-level mispricing)

### Example

```
Market-wide PE regression (N=3,000 US firms):
PE = 12.5 + 0.8(Growth%) - 3.2(Beta) + 0.15(Payout%)
R-squared = 0.35

Sector regression (N=40 software firms):
PE = 8.2 + 1.5(Growth%) - 0.3(Beta) + 0.05(Payout%)
R-squared = 0.62

Observation: The sector regression has higher R-squared because firms within
a sector are more homogeneous. The growth coefficient is higher in the sector
regression (1.5 vs 0.8), suggesting the market pays more for growth within
software than across all industries.
```

---

## Common Pitfalls in Relative Valuation

### Pitfall 1: "Comparable" Firms That Are Not Comparable

**Problem**: Selecting peers solely by industry classification without verifying that they share similar growth, risk, and profitability profiles.

**Example**: Comparing a high-growth cloud SaaS company (40% revenue growth, -5% operating margin) to a mature enterprise software company (5% revenue growth, 30% operating margin) because both have SIC code 7372.

**Fix**: Screen for growth rate, size, margin structure, and business model in addition to industry. A fast-growing SaaS firm may be better compared to fast-growing firms in other industries than to slow-growing firms in its own industry.

### Pitfall 2: Ignoring the Distribution

**Problem**: Comparing a company's multiple to the sector "average" without understanding the distribution. PE averages are distorted by outliers and right-skewness.

**Example**: Sector mean PE is 30x (pulled up by two firms at 80x+), but median is 22x. Concluding a firm at 25x PE is "below average" when it is actually above the median.

**Fix**: Report median, not mean, as the central tendency. Report the full distribution (quartiles, range). Position the target within the distribution.

### Pitfall 3: No Fundamental Driver Analysis

**Problem**: Comparing multiples without controlling for the variables that drive them. A firm with higher PE may simply have higher growth.

**Example**: Concluding that Company A (PE 40x, growth 25%) is "expensive" compared to Company B (PE 20x, growth 8%) without noting that growth explains the difference.

**Fix**: Always perform the Analyze step. At minimum, plot the multiple against its primary driver (PE vs. growth) and check whether the target's position is consistent with the relationship.

### Pitfall 4: Confusing Relative and Absolute Valuation

**Problem**: Concluding that a stock is "undervalued" because it trades below its sector peers, when the entire sector may be overvalued.

**Example**: In the dot-com bubble of 1999, many technology stocks appeared "cheap" relative to peers trading at 100x revenue. They were still overvalued in absolute terms.

**Fix**: Relative valuation tells you "cheap or expensive relative to peers." Intrinsic (DCF) valuation tells you "above or below fundamental value." Use both approaches and reconcile them.

### Pitfall 5: Regression with Insufficient Data

**Problem**: Running a regression with fewer than 15 observations, producing unreliable coefficients and misleading R-squared.

**Fix**: If the peer set is small, use simple peer comparison with qualitative adjustments. Reserve regression for larger samples. Report confidence intervals around predictions to convey uncertainty.

### Pitfall 6: Mixing Equity and Firm Multiples

**Problem**: Dividing enterprise value by net income (firm numerator with equity denominator) or price by EBITDA (equity numerator with firm denominator).

**Fix**: Enforce the claimholder consistency test at the start of every analysis. Equity value goes with equity metrics. Enterprise value goes with firm metrics.
