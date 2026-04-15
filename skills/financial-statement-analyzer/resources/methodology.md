# Financial Statement Analyzer Methodology

Detailed procedures for accounting adjustments, free cash flow computation, and financial statement normalization.

## Table of Contents
- [R&D Capitalization](#rd-capitalization)
- [Operating Lease Conversion](#operating-lease-conversion)
- [Stock-Based Compensation Treatment](#stock-based-compensation-treatment)
- [One-Time Item Normalization](#one-time-item-normalization)
- [Three-Viewpoint Balance Sheet Analysis](#three-viewpoint-balance-sheet-analysis)
- [Free Cash Flow Computation](#free-cash-flow-computation)
- [Invested Capital Calculation](#invested-capital-calculation)
- [Tax Rate Selection](#tax-rate-selection)
- [Operating vs Non-Operating Item Separation](#operating-vs-non-operating-item-separation)

---

## R&D Capitalization

Accounting standards treat R&D as an operating expense. For valuation, R&D is better understood as a capital expenditure -- money spent today to generate future benefits. Capitalizing R&D produces a more accurate picture of operating income and invested capital for R&D-intensive firms.

### Step-by-Step Procedure

**Step 1: Collect R&D expense history**

Gather R&D spending for (N+1) years, where N is the assumed asset life. If history is unavailable, use available years and note the limitation.

**Step 2: Determine the appropriate asset life**

The asset life represents how long R&D spending generates economic benefits:

| Industry | Typical Asset Life | Rationale |
|----------|-------------------|-----------|
| Software / Internet | 2-3 years | Rapid obsolescence, short product cycles |
| Consumer electronics | 3-5 years | Moderate product cycles |
| Consumer products | 5-7 years | Brand-supported product lines |
| Automotive | 5-7 years | Platform development cycles |
| Pharmaceuticals | 8-10 years | Long development pipeline, patent life |
| Aerospace / Defense | 10-15 years | Multi-decade program lifecycles |

**Step 3: Build the amortization schedule**

For each prior year's R&D, compute the portion that remains unamortized and the current-year amortization charge:

- Unamortized fraction for R&D spent K years ago = (N - K) / N
- Amortization in current year for R&D spent K years ago = R&D_K / N

**Step 4: Compute the research asset**

Sum the unamortized portions of all past R&D spending. This represents the "research asset" added to the balance sheet:

```
Research Asset = Sum over K=0 to N-1 of [R&D_{-K} x (N - K) / N]
```

**Step 5: Adjust operating income**

```
Adjusted Operating Income = Reported Operating Income
                          + Current Year R&D Expense (add back the full amount)
                          - Total Amortization of Past R&D (sum of amortization charges)
```

The net effect on operating income = Current R&D - Total Amortization. If R&D is growing, this adjustment increases operating income; if R&D is stable or shrinking, the effect is smaller or negative.

**Step 6: Adjust the tax bill**

The change in operating income flows through to taxes:

```
Tax Adjustment = (Adjusted OI - Reported OI) x Marginal Tax Rate
```

**Step 7: Adjust the balance sheet**

- Add the research asset to the asset side (increases invested capital)
- Increase retained earnings on the equity side by: Research Asset - Cumulative Tax Effect

### Example: 3-Year Asset Life

| Year | R&D | Unamortized Fraction | Unamortized Amount | Amortization |
|------|-----|---------------------|-------------------|-------------|
| Current | $300M | 3/3 = 100% | $300M | $100M |
| Year -1 | $270M | 2/3 = 67% | $180M | $90M |
| Year -2 | $240M | 1/3 = 33% | $80M | $80M |
| Year -3 | $210M | 0/3 = 0% | $0 | (fully amortized) |

- Research asset: $300M + $180M + $80M = $560M
- Total amortization: $100M + $90M + $80M = $270M
- Adjusted OI = Reported OI + $300M - $270M = Reported OI + $30M

---

## Operating Lease Conversion

Operating leases represent commitments to make future payments, economically similar to debt. Converting them to debt equivalents produces a more accurate picture of the company's financial obligations and true operating income.

### Step-by-Step Procedure

**Step 1: Collect lease commitment data**

Gather the schedule of future minimum lease payments. Companies report these in annual report footnotes, typically showing Years 1-5 individually and a lump sum for "thereafter."

**Step 2: Determine the discount rate**

Use the company's pre-tax cost of debt. If unavailable, estimate from the synthetic credit rating (interest coverage mapped to rating and default spread).

**Step 3: Estimate remaining lease life for "thereafter" payments**

```
Estimated remaining years = Lump Sum Amount / Year 5 Annual Payment
```

This gives an approximate number of additional years beyond Year 5.

**Step 4: Compute PV of lease commitments**

Discount each year's payment at the pre-tax cost of debt:

```
Lease Debt = Sum of [Payment_t / (1 + kd)^t] for each year t
```

For the "thereafter" lump sum, either:
- Annuitize it over the estimated remaining years and discount each payment, or
- Discount the lump sum at the midpoint of the estimated period

**Step 5: Adjust the balance sheet**

- Add lease debt to total debt on the liability side
- Add a lease asset of equal value to the asset side (represents the right-of-use asset)
- Note: Under ASC 842 / IFRS 16, many leases are already on the balance sheet. Check whether the company has already capitalized its leases before making this adjustment.

**Step 6: Adjust the income statement**

```
Adjusted Operating Income = Reported EBIT
                          + Operating Lease Expense (the full annual payment)
                          - Depreciation of Lease Asset (lease asset / total lease life)
```

The net EBIT adjustment is typically small and positive (lease expense exceeds straight-line depreciation for a portfolio of leases at different stages).

Additionally, recognize:
```
Interest Expense on Lease Debt = Lease Debt x Pre-tax Cost of Debt
```

This reclassifies part of the lease expense from operating to financing.

**Step 7: Adjust invested capital**

Add the lease asset to invested capital. This increases the denominator for ROIC, which partially offsets the operating income increase.

### Note on ASC 842 / IFRS 16

Under current accounting standards (effective since 2019), most leases already appear on the balance sheet. However:
- Verify the company has fully adopted the standard
- Short-term leases (under 12 months) and low-value leases may still be off-balance-sheet
- The discount rate used by the company (often its incremental borrowing rate) may differ from the rate appropriate for valuation

---

## Stock-Based Compensation Treatment

SBC is a real economic cost to existing shareholders because it dilutes their ownership. The treatment for valuation:

### Operating Expense (Standard Treatment)

- Treat SBC as an operating expense in the income statement (where it already appears under GAAP/IFRS)
- Do not add it back to compute "adjusted" EBITDA or "adjusted" cash flow
- When computing FCFF, SBC is already deducted from operating income as an expense

### Why Not Add Back SBC?

Adding back SBC (as many companies do in non-GAAP earnings) overstates true cash-generating ability. While SBC is a non-cash expense, it creates real dilution. If the company did not issue stock options, it would need to pay higher cash compensation.

### Diluted Share Count

When converting equity value to per-share value:
- Use diluted share count (includes in-the-money options via treasury stock method)
- Or subtract the value of outstanding options (estimated via Black-Scholes) from total equity value before dividing by basic shares

### When SBC Is Very Large

For companies where SBC exceeds 10-15% of revenue:
- Note the magnitude as a risk factor
- Consider whether SBC is likely to decline as a percentage of revenue over time (as is common for maturing tech companies)
- The gap between GAAP and non-GAAP earnings is a useful indicator of SBC significance

---

## One-Time Item Normalization

The goal is to estimate sustainable, recurring earnings that represent the company's ongoing earning power.

### Identifying Genuinely Non-Recurring Items

Items that qualify as truly non-recurring:
- Asset write-downs or impairments from specific events
- Litigation settlements (unless the company is frequently litigated against)
- Gains or losses from asset sales
- Natural disaster impacts
- Costs of specific, completed restructuring programs

Items that do not qualify (even if labeled "non-recurring"):
- Restructuring charges that appear in three or more of the past five years
- Goodwill impairments for serial acquirers (these reflect acquisition strategy, not one-time events)
- Integration costs for companies that routinely make acquisitions
- Stock-based compensation (this is a recurring operating cost)

### Normalization Techniques

**Technique 1: Remove and replace**
For genuinely one-time items: remove the item from the year it occurred and compute normalized earnings without it.

**Technique 2: Average over cycle**
For cyclical companies or items that recur irregularly: average operating income over a full business cycle (5-10 years) to smooth out peaks and troughs.

**Technique 3: Margin-based normalization**
For companies with temporarily depressed or elevated margins: apply the historical average operating margin (or industry median margin) to current revenue.

```
Normalized Operating Income = Current Revenue x Average Operating Margin (past 5-10 years)
```

### Documentation Requirement

For each normalization:
- Identify the item and its amount
- State why it is considered non-recurring (or why averaging is appropriate)
- Show the before and after impact on operating income
- Note if there is a pattern of similar "non-recurring" items

---

## Three-Viewpoint Balance Sheet Analysis

The balance sheet can be read three ways, each useful for different purposes:

**1. Record of Capital Invested**
- Focus: How much has the firm invested in assets to support operations?
- Use: Computing invested capital for ROIC
- Key items: Fixed assets + working capital + intangible assets (including capitalized R&D and leases)
- Exclusions: Cash and financial assets (non-operating)

**2. Measure of Current Value**
- Focus: What are the assets worth at current market value?
- Use: Relative valuation (price-to-book), assessing accounting distortions
- Key items: Mark-to-market financial assets, fair value of real estate, replacement cost of plant
- Limitation: Many assets are still at historical cost, especially plant and equipment

**3. Liquidation Value**
- Focus: What would assets fetch if sold today?
- Use: Distress analysis, floor valuation
- Key items: Realizable value of each asset category (typically at a discount to book value for fixed assets)
- Limitation: Does not capture going-concern value, intangibles often worth very little in liquidation

For standard valuation work, the first viewpoint (capital invested) is most relevant.

---

## Free Cash Flow Computation

### FCFF (Free Cash Flow to Firm)

FCFF represents the cash flow available to all capital providers (debt and equity) after reinvestment needs:

```
FCFF = After-tax Operating Income
     - (Capital Expenditures - Depreciation)
     - Change in Non-Cash Working Capital
```

Equivalently:
```
FCFF = EBIT x (1 - Marginal Tax Rate)
     - Net Capital Expenditure
     - Change in Non-Cash Working Capital
```

Where:
- After-tax operating income uses the adjusted EBIT (after R&D capitalization, lease conversion)
- Capital expenditures include R&D (if capitalized) -- consistency is key
- Depreciation includes R&D amortization (if capitalized)
- Non-cash working capital = Non-cash current assets - Non-debt current liabilities

### FCFE (Free Cash Flow to Equity)

FCFE represents cash flow available to equity holders after debt payments:

```
FCFE = Net Income
     - (Capital Expenditures - Depreciation)
     - Change in Non-Cash Working Capital
     - (Debt Repaid - Debt Issued)
```

Equivalently:
```
FCFE = Net Income x (1 - Equity Reinvestment Rate)
```

### Reconciliation

FCFF and FCFE are related:
```
FCFE = FCFF - Interest Expense x (1 - Tax Rate) + Net Debt Issued
```

If this relationship does not hold within rounding tolerance, there is an error. Common sources:
- Inconsistent tax rates between the two calculations
- Missing a debt issuance or repayment
- Non-operating income included in one calculation but not the other

### Working Capital Considerations

Non-cash working capital components:
- **Include**: Accounts receivable, inventory, other operating current assets, accounts payable, accrued liabilities, taxes payable
- **Exclude**: Cash and marketable securities (non-operating), short-term debt (financing, not operating), current portion of long-term debt (financing)

An increase in non-cash working capital reduces free cash flow (cash is tied up in operations). A decrease releases cash.

---

## Invested Capital Calculation

Invested capital represents the total capital deployed in the business. There are two equivalent approaches:

### Asset-Side Approach
```
Invested Capital = Total Assets
                 - Cash and Marketable Securities (non-operating)
                 - Non-operating Financial Assets
                 - Non-debt Current Liabilities (accounts payable, accrued expenses)
                 + Research Asset (if R&D is capitalized)
                 + Lease Asset (if operating leases are converted)
```

### Financing-Side Approach
```
Invested Capital = Total Debt (including capitalized leases)
                 + Shareholders' Equity
                 + Research Asset Net of Tax Effect
                 - Cash and Marketable Securities
```

Both approaches should yield the same result. The financing-side approach is often easier to compute.

---

## Tax Rate Selection

| Context | Which Tax Rate | Rationale |
|---------|---------------|-----------|
| FCFF for valuation | Marginal tax rate | Forward-looking cash flows should use the rate that will apply to incremental income |
| Historical ratio analysis | Effective tax rate | Reflects what the company actually paid |
| Tax shield on debt | Marginal tax rate | Interest deductions save taxes at the marginal rate |
| International operations | Blended marginal rate | Weight marginal rates by income generated in each jurisdiction |

Common divergences between effective and marginal rates:
- Net operating loss carryforwards (effective < marginal temporarily)
- Foreign income taxed at different rates
- R&D tax credits
- Deferred tax assets or liabilities
- Tax-exempt income

If the effective rate is significantly below the marginal rate, investigate whether this will persist or normalize over time.

---

## Operating vs Non-Operating Item Separation

Correctly separating operating and non-operating items is essential for computing clean ROIC and FCFF.

### Non-Operating Assets (exclude from invested capital)

| Item | Treatment |
|------|-----------|
| Cash above operating needs | Non-operating. Estimate operating cash as 1-2% of revenue for most companies. Excess is non-operating. |
| Marketable securities | Non-operating financial asset. Value separately. |
| Equity stakes in other companies | Non-operating. Value at market price or proportional book value. |
| Excess real estate or idle assets | Non-operating if not used in business operations. |

### Non-Operating Income/Expense (exclude from operating income)

| Item | Treatment |
|------|-----------|
| Interest income on cash | Non-operating. Exclude from EBIT. |
| Gains/losses on investments | Non-operating. Exclude from EBIT. |
| Income from equity method investees | Non-operating unless the investee is integral to operations. |
| Foreign exchange gains/losses | Operating if related to business transactions; non-operating if related to financial assets. |

### Operating Items Often Misclassified

| Item | Correct Treatment |
|------|-------------------|
| R&D expense | Operating (capital expenditure after adjustment) |
| Operating lease expense | Operating (reclassify to depreciation + interest after conversion) |
| Restructuring charges | Operating (if recurring, normalize by averaging) |
| SBC | Operating expense |
