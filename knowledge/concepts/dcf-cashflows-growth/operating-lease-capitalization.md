# Operating lease capitalization

**Core idea:** An operating lease is a fixed, tax-deductible commitment that must be paid regardless of how operations do, and non-payment costs the firm the asset and possibly control of the business. That is the definition of debt, not of an operating expense. Accounting (pre-2019) treated lease payments as operating expenses and kept the obligation off the balance sheet, which understated both debt and operating income. The fix is to discount the future lease commitments at the pre-tax cost of debt to get a debt value, create a leased asset of exactly the same value, add the lease expense back to operating income, and subtract depreciation on the asset instead. This matters enormously in lease-heavy sectors: lease expense is ~44% of operating income for apparel stores and ~50% for furniture stores versus ~12.5% for the market.

**Formulas:**
- Debt value of operating leases = PV of future operating-lease commitments discounted at the **pre-tax cost of debt** `kd`:
  `Lease debt = SUM over t=1..5 of C_t/(1+kd)^t + PV of the "year 6 and beyond" lump`
  where `C_t` = the disclosed lease commitment for year t.
- Years embedded in the "year 6 and beyond" lump: `n6 = ROUND(Lump / average(C_1..C_5), 0)`; annual tail payment `A = Lump / n6`; PV of tail = `A * [1 − (1+kd)^(−n6)] / kd / (1+kd)^5`.
- Leased asset value = Lease debt (created at exactly the same value, by construction).
- Straight-line depreciation on the leased asset = `Lease debt / (5 + n6)` (i.e. over the full lease life).
- **Exact adjustment:** Adjusted operating income = Operating income + Current-year operating-lease expense − Depreciation on the leased asset.
- **Approximation:** Adjusted operating income = Operating income + `kd × Lease debt` (add back only the imputed interest).
- Adjusted total debt = Reported interest-bearing debt + Lease debt.
- Imputed lease interest (for interest-coverage / synthetic-rating work) = `kd × Lease debt`, added to reported interest expense.

**Procedure:**
1. Pull the operating-lease commitment schedule from the footnotes: years 1–5 individually plus the "thereafter" lump sum, and the current year's lease expense.
2. Get the pre-tax cost of debt `kd`. If you are deriving `kd` from a synthetic rating, this is circular (lease debt changes coverage, coverage changes `kd`) — iterate to a fixed point.
3. Estimate `n6`, the number of years in the "thereafter" lump: `ROUND(lump / average of the first five commitments, 0)`. If the lump is zero, `n6 = 0`.
4. Discount years 1–5 individually; convert the lump into an `n6`-year annuity starting in year 6 and discount it back. Sum -> **debt value of leases**.
5. Add the lease debt to debt (for the cost-of-capital weights, the equity bridge, and the debt ratio). Add the identical amount as a leased asset to invested capital / book capital.
6. Depreciate the asset straight-line over `5 + n6` years. Adjust operating income: add back the full current lease expense, subtract this depreciation. (Use the `kd × lease debt` approximation only when the asset life is unknowable.)
7. Recompute every ratio that uses operating income or capital: return on capital, reinvestment rate, interest coverage, cost of capital, debt ratio. Expect ROC to fall (capital rises more than earnings) and cost of capital to fall (more cheap debt in the weights).
8. Sanity check: net income must be **unchanged** — the higher EBIT is exactly offset by the higher imputed interest expense.

**Reference data:**

Operating lease expense as a percent of operating income, by sector (why the adjustment is or is not material):
| Sector | Lease expense / operating income |
|---|---|
| Whole market | ~12.5% |
| Furniture stores | ~50% |
| Apparel stores | ~44% |
| Restaurants | ~27% |

Standards note: **In 2019 both IFRS and US GAAP began requiring capitalization of operating leases**, putting the debt and a counter-asset on the balance sheet — validating this adjustment. The official rules are far more complex than this PV calculation, because standard-setters had to preserve continuity with legacy rules and because companies lobbied for sector-specific softening. For pre-2019 statements, or when the reported lease liability looks inconsistent, do the simple calculation yourself.

**Worked example — The Gap, 2003 ($ millions):**

Conventional debt $1,970; pre-tax cost of debt 6%; 2003 operating lease expense $978; stated operating income $1,012; book equity $3,130; market equity $7,350; cost of equity 8.20%; after-tax cost of debt 4.00%; tax rate 35%.

| Year | Commitment | PV at 6% |
|---|---|---|
| 1 | 899.00 | 848.11 |
| 2 | 846.00 | 752.94 |
| 3 | 738.00 | 619.64 |
| 4 | 598.00 | 473.67 |
| 5 | 477.00 | 356.44 |
| 6 & 7 | 982.50 each | 1,346.04 |
| **Total** | | **4,396.85** |

- Lease debt = leased asset = **$4,397m**. Total debt = 1,970 + 4,397 = **$6,367m**.
- Asset life = 7 years -> depreciation = 4,397/7 = $628m.
- Adjusted EBIT = 1,012 + 978 − 628 = **$1,362m**. (Approximation: 1,012 + 0.06 × 4,397 = $1,276m.)
- Cost of capital: conventional = 8.20%×(7,350/9,320) + 4%×(1,970/9,320) = **7.31%**; adjusted = 8.20%×(7,350/13,717) + 4%×(6,367/13,717) = **6.25%**.
- Return on capital: conventional = 1,012×(1−0.35)/(3,130+1,970) = **12.90%**; adjusted = 1,362×(1−0.35)/(3,130+6,367) = **9.30%**.

Interpretation: capitalizing leases makes The Gap look *less profitable* and *more levered but cheaper-financed* than the reported statements suggest.

**Determinism:**
- DETERMINISTIC: given the commitment schedule, the lump sum, `kd`, the current lease expense and the asset life -> lease debt, leased asset, depreciation, adjusted EBIT, adjusted debt, adjusted ROC, adjusted cost of capital. The `n6 = ROUND(lump/avg)` heuristic is itself deterministic.
- JUDGMENT: the choice of pre-tax cost of debt when no rating exists; whether the ROUND heuristic for the tail years is credible for this firm (some firms disclose the tail structure); whether to use the exact or the approximate operating-income adjustment; and reading the post-2019 reported lease liability versus recomputing it.

**Pitfalls:**
- Adding lease debt to debt but forgetting the counter-asset — this understates invested capital and inflates return on capital.
- Discounting lease commitments at the cost of capital or the riskfree rate instead of the **pre-tax cost of debt**.
- Letting net income change. If it does, you have double-counted the lease payment.
- Leaving the lease debt out of the interest-coverage ratio used for a synthetic rating (it must include imputed lease interest), or failing to iterate the circularity.
- Assuming the "thereafter" lump is one payment (it is a multi-year annuity) or spreading it over an arbitrary ten years.
- Forgetting to redo the cost-of-capital weights: leases can move the debt ratio by tens of percentage points in retail.

**Sources:**
- valpacket1spr21 p.123-128
- valpacket1spr20 p.120-125
- spreadsheet:wacccalc.xls — `Operating lease converter` sheet (n6 = ROUND(lump/average of yrs 1-5); depreciation = lease debt/(5+n6); EBIT adjustment = lease expense − depreciation)
- spreadsheet:fcffsimpleginzu.xlsx — `Operating lease converter` sheet and the base-year EBIT / invested-capital formulas that consume it
- spreadsheet:higrowth.xls — `Operating Leases` sheet (uses the `kd × lease debt` approximation for the EBIT adjustment)

**Related:** [[reported-to-actual-earnings]], [[rnd-capitalization]], [[return-on-invested-capital]], [[net-capital-expenditures]], [[fcff]], [[synthetic-rating]], [[cost-of-capital]], [[debt-definition]]
