# Financial Statement Analyzer Templates

Input templates, adjustment documentation, ratio dashboards, and calculation worksheets for financial statement analysis.

## Table of Contents
- [Financial Data Input Template](#financial-data-input-template)
- [R&D Expense History Table](#rd-expense-history-table)
- [Operating Lease Commitments Table](#operating-lease-commitments-table)
- [Adjustment Documentation Template](#adjustment-documentation-template)
- [FCFF Calculation Worksheet](#fcff-calculation-worksheet)
- [FCFE Calculation Worksheet](#fcfe-calculation-worksheet)
- [Cash Flow Reconciliation](#cash-flow-reconciliation)
- [Ratio Dashboard Template](#ratio-dashboard-template)
- [Industry Comparison Template](#industry-comparison-template)

---

## Financial Data Input Template

### Income Statement

| Line Item | Year -2 | Year -1 | Current Year |
|-----------|---------|---------|-------------|
| Revenue | | | |
| Cost of Goods Sold (COGS) | | | |
| **Gross Profit** | | | |
| Research & Development (R&D) | | | |
| Selling, General & Administrative (SG&A) | | | |
| Stock-Based Compensation (SBC) | | | |
| Other Operating Expenses | | | |
| **Operating Income (EBIT)** | | | |
| Interest Expense | | | |
| Other Non-Operating Income/Expense | | | |
| **Pre-Tax Income** | | | |
| Income Taxes (reported) | | | |
| **Net Income** | | | |

**Supplemental income statement data:**
- Effective tax rate: ____%
- Marginal tax rate: ____%
- SBC included in which line items: ____
- One-time items included above (describe): ____

### Balance Sheet

| Line Item | Year -1 | Current Year |
|-----------|---------|-------------|
| **Assets** | | |
| Cash & Marketable Securities | | |
| Accounts Receivable | | |
| Inventory | | |
| Other Current Assets | | |
| **Total Current Assets** | | |
| Property, Plant & Equipment (net) | | |
| Goodwill | | |
| Other Intangible Assets | | |
| Financial Assets / Investments | | |
| Other Non-Current Assets | | |
| **Total Assets** | | |
| **Liabilities** | | |
| Accounts Payable | | |
| Short-Term Debt | | |
| Current Portion of Long-Term Debt | | |
| Other Current Liabilities | | |
| **Total Current Liabilities** | | |
| Long-Term Debt | | |
| Operating Lease Liabilities (if on balance sheet) | | |
| Other Long-Term Liabilities | | |
| Minority Interest / Non-Controlling Interest | | |
| **Total Liabilities** | | |
| **Shareholders' Equity** | | |
| Common Stock & APIC | | |
| Retained Earnings | | |
| Treasury Stock | | |
| Other Comprehensive Income | | |
| **Total Equity** | | |

### Cash Flow Statement

| Line Item | Year -2 | Year -1 | Current Year |
|-----------|---------|---------|-------------|
| **Cash Flow from Operations** | | | |
| Net Income | | | |
| Depreciation & Amortization | | | |
| Stock-Based Compensation | | | |
| Change in Accounts Receivable | | | |
| Change in Inventory | | | |
| Change in Accounts Payable | | | |
| Change in Other Working Capital | | | |
| Other Operating Adjustments | | | |
| **Total Operating Cash Flow** | | | |
| **Cash Flow from Investing** | | | |
| Capital Expenditures | | | |
| Acquisitions | | | |
| Purchases of Investments | | | |
| Sales of Investments | | | |
| Other Investing Activities | | | |
| **Total Investing Cash Flow** | | | |
| **Cash Flow from Financing** | | | |
| Debt Issued | | | |
| Debt Repaid | | | |
| Shares Issued | | | |
| Shares Repurchased | | | |
| Dividends Paid | | | |
| Other Financing Activities | | | |
| **Total Financing Cash Flow** | | | |
| **Net Change in Cash** | | | |

---

## R&D Expense History Table

Collect R&D expenses for N+1 years (where N = assumed asset life) to compute the research asset and amortization schedule.

| Year | R&D Expense | Unamortized Portion | Amortization in Current Year |
|------|-------------|--------------------|-----------------------------|
| Current year | $____ | 100% (fully unamortized) | $____ (= R&D / N) |
| Year -1 | $____ | (N-1)/N = ____% | $____ |
| Year -2 | $____ | (N-2)/N = ____% | $____ |
| Year -3 | $____ | (N-3)/N = ____% | $____ |
| Year -4 | $____ | (N-4)/N = ____% | $____ |
| Year -5 | $____ | (if N > 5: ____%) | $____ |
| **Totals** | | **Research Asset: $____** | **Total Amortization: $____** |

**Adjustment to operating income:**
- Add back: Current year R&D expense = $____
- Subtract: Total amortization of past R&D = $____
- Net adjustment to operating income = $____
- Tax effect of adjustment: Net adjustment x marginal tax rate = $____

---

## Operating Lease Commitments Table

Record future minimum lease payments and compute the present value debt equivalent.

| Year | Lease Payment | PV Factor (at pre-tax kd = ____%) | Present Value |
|------|--------------|----------------------------------|---------------|
| Year 1 | $____ | ____ | $____ |
| Year 2 | $____ | ____ | $____ |
| Year 3 | $____ | ____ | $____ |
| Year 4 | $____ | ____ | $____ |
| Year 5 | $____ | ____ | $____ |
| Year 6+ (lump sum) | $____ | ____ | $____ |
| **Total** | **$____** | | **PV = $____** |

**For the Year 6+ lump sum**: If the company reports a total for "thereafter," estimate the number of remaining years by dividing the lump sum by the Year 5 payment. Discount at the midpoint of the estimated remaining period.

**Adjustment to financials:**
- Lease debt added to balance sheet: $____
- Lease asset added to balance sheet: $____ (equals lease debt at inception)
- Operating income adjustment: Add back operating lease expense ($____), subtract depreciation of lease asset ($____ = lease asset / lease life)
- Net adjustment to EBIT: $____
- Interest expense on lease debt: $____ (= lease debt x pre-tax cost of debt)

---

## Adjustment Documentation Template

For each adjustment applied, complete this documentation block:

### Adjustment: [Name]

| Item | Value |
|------|-------|
| **Adjustment type** | R&D capitalization / Lease conversion / SBC / Normalization / Other |
| **Rationale** | Why this adjustment is necessary |
| **Pre-adjustment EBIT** | $____ |
| **Post-adjustment EBIT** | $____ |
| **Change in EBIT** | $____ (+/-) |
| **Pre-adjustment invested capital** | $____ |
| **Post-adjustment invested capital** | $____ |
| **Change in invested capital** | $____ (+/-) |
| **Tax impact** | $____ |
| **Effect on FCFF** | $____ (+/-) |
| **Key assumptions** | Asset life, discount rate, etc. |

**Summary of all adjustments:**

| Adjustment | EBIT Impact | Invested Capital Impact | FCFF Impact |
|------------|------------|------------------------|-------------|
| R&D capitalization | $____ | $____ | $____ |
| Operating lease conversion | $____ | $____ | $____ |
| SBC treatment | $____ | $____ | $____ |
| One-time item normalization | $____ | $____ | $____ |
| **Total adjustments** | **$____** | **$____** | **$____** |

---

## FCFF Calculation Worksheet

```
  Adjusted Operating Income (EBIT)                    $________
- Taxes on operating income (EBIT x marginal tax rate) $________
= After-tax Operating Income (NOPAT)                  $________

- Capital Expenditures                                 $________
+ Depreciation                                         $________
= Net Capital Expenditure                              $________

- Change in Non-Cash Working Capital                   $________

= Free Cash Flow to Firm (FCFF)                        $________
```

**Working capital detail:**

| Component | Year -1 | Current Year | Change |
|-----------|---------|-------------|--------|
| Accounts Receivable | $____ | $____ | $____ |
| Inventory | $____ | $____ | $____ |
| Other Current Assets (non-cash) | $____ | $____ | $____ |
| Accounts Payable | ($____) | ($____) | ($____) |
| Other Current Liabilities (non-debt) | ($____) | ($____) | ($____) |
| **Non-Cash Working Capital** | **$____** | **$____** | **$____** |

---

## FCFE Calculation Worksheet

```
  Net Income                                           $________
- Capital Expenditures                                 $________
+ Depreciation                                         $________
= Net Capital Expenditure                              $________
- Change in Non-Cash Working Capital                   $________
- Debt Repaid                                          $________
+ New Debt Issued                                      $________
= Net Debt Change                                      $________

= Free Cash Flow to Equity (FCFE)                      $________
```

---

## Cash Flow Reconciliation

Verify FCFF and FCFE are internally consistent:

```
  FCFF                                                 $________
- Interest Expense x (1 - Tax Rate)                    $________
+ Net Debt Issued (New Debt - Debt Repaid)             $________
= FCFE (should match above)                            $________

  Calculated FCFE from reconciliation:                 $________
  Calculated FCFE from worksheet:                      $________
  Difference:                                          $________
```

If the difference is non-zero, investigate:
- [ ] Missed a debt issuance or repayment
- [ ] Tax rate inconsistency between FCFF and FCFE calculations
- [ ] Non-operating income included in one but not the other
- [ ] Preferred dividend or minority interest not accounted for

---

## Ratio Dashboard Template

### Profitability Ratios

| Ratio | Formula | Year -2 | Year -1 | Current | Industry Median |
|-------|---------|---------|---------|---------|----------------|
| Gross Margin | Gross Profit / Revenue | ____% | ____% | ____% | ____% |
| Operating Margin | Adjusted EBIT / Revenue | ____% | ____% | ____% | ____% |
| Net Margin | Net Income / Revenue | ____% | ____% | ____% | ____% |
| ROIC | NOPAT / Invested Capital | ____% | ____% | ____% | ____% |
| ROE | Net Income / Book Equity | ____% | ____% | ____% | ____% |
| ROA | Net Income / Total Assets | ____% | ____% | ____% | ____% |

### Leverage Ratios

| Ratio | Formula | Year -2 | Year -1 | Current | Industry Median |
|-------|---------|---------|---------|---------|----------------|
| Debt-to-Capital | Debt / (Debt + Equity) | ____% | ____% | ____% | ____% |
| Debt-to-EBITDA | Total Debt / EBITDA | ____x | ____x | ____x | ____x |
| Interest Coverage | EBIT / Interest Expense | ____x | ____x | ____x | ____x |
| Net Debt-to-EBITDA | (Debt - Cash) / EBITDA | ____x | ____x | ____x | ____x |

### Efficiency Ratios

| Ratio | Formula | Year -2 | Year -1 | Current | Industry Median |
|-------|---------|---------|---------|---------|----------------|
| Reinvestment Rate | (Net CapEx + dWC) / NOPAT | ____% | ____% | ____% | ____% |
| Sales-to-Capital | Revenue / Invested Capital | ____x | ____x | ____x | ____x |
| Asset Turnover | Revenue / Total Assets | ____x | ____x | ____x | ____x |
| Days Sales Outstanding | (AR / Revenue) x 365 | ____ | ____ | ____ | ____ |
| Days Inventory Outstanding | (Inventory / COGS) x 365 | ____ | ____ | ____ | ____ |

### Liquidity Ratios

| Ratio | Formula | Year -2 | Year -1 | Current | Industry Median |
|-------|---------|---------|---------|---------|----------------|
| Current Ratio | Current Assets / Current Liabilities | ____x | ____x | ____x | ____x |
| Quick Ratio | (Cash + AR) / Current Liabilities | ____x | ____x | ____x | ____x |

---

## Industry Comparison Template

| Metric | Company (Adjusted) | Sector 25th Pctl | Sector Median | Sector 75th Pctl | Assessment |
|--------|-------------------|------------------|---------------|------------------|------------|
| Operating Margin | ____% | ____% | ____% | ____% | Above/At/Below median |
| ROIC | ____% | ____% | ____% | ____% | Above/At/Below median |
| Debt-to-Capital | ____% | ____% | ____% | ____% | Above/At/Below median |
| Reinvestment Rate | ____% | ____% | ____% | ____% | Above/At/Below median |
| Sales-to-Capital | ____x | ____x | ____x | ____x | Above/At/Below median |
| Interest Coverage | ____x | ____x | ____x | ____x | Above/At/Below median |

**Key takeaways from industry comparison:**
1. ____
2. ____
3. ____
