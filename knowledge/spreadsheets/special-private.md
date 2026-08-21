# Damodaran — Private Company Valuation Spreadsheets

Source folder: `/Users/kushaldsouza/Downloads/2020/Spreadsheets/Private Companies/`

All three files are BIFF8 `.xls`. Formulas below were extracted directly from the binary FORMULA records (not inferred) unless explicitly flagged "(inferred)". Every worked example was recomputed and matches the values stored in the sheets.

---

### liqdisc.xls

**Purpose:** Estimates the **illiquidity (marketability) discount** to apply to the value of equity in a private business. Damodaran offers two independent estimators, each on its own sheet:

1. **Restricted Stock Regression** — starts from a base discount (25% for a $10 million-revenue profitable firm, drawn from restricted-stock studies) and adjusts it for the subject firm's revenues, block size, and profitability using the coefficients of the Silber (1991) restricted-stock regression: `ln(RPRS) = 4.33 + 0.036 ln(Revenues) − 0.142 ln(RBRT) + 0.174 DERN (+ 0.332 DCUST, unused here)`.
2. **Bid-Ask Spread** — treats the bid-ask spread as the observable cost of illiquidity for public firms and applies Damodaran's cross-sectional spread regression to the private firm's characteristics; the predicted "spread" is used directly as the illiquidity discount.

Used at the end of a private-company valuation. Value the firm or equity first, then knock off the discount when the buyer will not have a liquid exit. Typical settings: selling a stake in a private business, or estate valuations.

**Sheets:** `Restricted Stock Regression`, `Bid-Ask Spread`, `Sheet2` (pre-computed discount lookup table), `Sheet3` (empty, skipped).

#### Sheet: Restricted Stock Regression

**Inputs**

| Cell | Label | Example value |
|---|---|---|
| B2 | Base Discount for firm with $10 million revenue | 0.25 |
| B3 | Revenues (in $ millions) | 209.0 |
| B4 | Size of block as % of stock outstanding (entered as a decimal fraction; 1.0 = 100%) | 1.0 |
| B5 | Positive or Negative Earnings (1 = positive/profitable, 0 = negative) | 1.0 |

**Logic** (formula extracted verbatim from B8, parentheses lightly cleaned):

```
B8 = B2 - ( (100 - EXP(4.33 + 0.036*LN(10)  - 0.142*LN(B4*100) + 0.174*1 ))/100
          - (100 - EXP(4.33 + 0.036*LN(B3) - 0.142*LN(B4*100) + 0.174*B5))/100 )
```

In math notation, with the Silber regression score `S(Rev, Block%, DERN) = 4.33 + 0.036·ln(Rev) − 0.142·ln(Block%) + 0.174·DERN` and predicted discount `d(·) = (100 − e^{S})/100`:

```
Illiquidity discount = BaseDiscount − [ d(10, Block%, 1) − d(Rev, Block%, DERN) ]
```

In words: the model predicts a discount for the subject firm and for an anchor firm ($10M revenues, profitable, same block size). The 25% base discount is shifted by the gap between those two predictions. `Block% = B4*100` — the fraction input converted to percent (B4 = 1.0 → Block% = 100). Note that both the anchor term and the firm term contain the same `−0.142·LN(B4*100)`. The block terms therefore cancel exactly, and block size has no effect on the output as the formula is written.

Note: the anchor revenue (10) and anchor DERN (=1) are hard-coded in the formula; B2 is the only part of the anchor the user can change.

**Outputs**

| Cell | Meaning | Value |
|---|---|---|
| B8 | Illiquidity Discount (fraction of estimated equity value to subtract) | 0.19095516638888976 |

**Worked example** (values currently in sheet): S_anchor = 4.33 + 0.036·ln 10 − 0.142·ln 100 + 0.174 = 3.932977 → d_anchor = (100 − e^3.932977)/100 = 0.489466. S_firm = 4.33 + 0.036·ln 209 − 0.142·ln 100 + 0.174·1 = 4.042398 → d_firm = (100 − e^4.042398)/100 = 0.430425. Discount = 0.25 − (0.489466 − 0.430425) = **0.190955** ✓ matches B8.

#### Sheet: Bid-Ask Spread

**Inputs**

| Cell | Label | Example value |
|---|---|---|
| B3 | Revenues ($ millions) | 209.0 |
| B4 | Positive or Negative Earnings (1/0) — **not a direct input**: `B4 ='Restricted Stock Regression'!B5` (linked to the other sheet) | 1.0 |
| B5 | Cash/Value (cash as fraction of firm value) | 0.03 |
| B6 | Trading Volume/Value (monthly $ trading volume / firm value; 0 for a private firm) | 0.0 |

**Logic** (formula extracted verbatim from B9):

```
B9 = 0.145 - 0.0022*LN(B3) - 0.015*B4 - 0.016*B5 - 0.11*B6
```

This is Damodaran's regression of bid-ask spreads on firm characteristics; the fitted "spread" for a firm with zero trading volume is used as the illiquidity discount:

```
Discount = 0.145 − 0.0022·ln(Revenues) − 0.015·DERN − 0.016·(Cash/Value) − 0.11·(TradingVol/Value)
```

**Outputs**

| Cell | Meaning | Value |
|---|---|---|
| B9 | Illiquidity Discount | 0.1177668646456774 |

**Worked example:** 0.145 − 0.0022·ln(209) − 0.015·1 − 0.016·0.03 − 0.11·0 = 0.145 − 0.011753 − 0.015 − 0.00048 = **0.117767** ✓.

#### Sheet: Sheet2 — pre-computed discount table (reference data, verbatim)

Illiquidity discounts by revenue level ($ millions), generated from the Restricted Stock Regression formula with Block% = 100 (verified: recomputing with the B8 formula reproduces these to 4 decimals; profitable → DERN = 1, unprofitable → DERN = 0). Column A rows 4–11 are formulas `=prev+5`; columns B and C are stored as static constants.

| Revenues ($mm) | Profitable firm | Unprofitable firm |
|---|---|---|
| 5 | 0.2626 | 0.3421 |
| 10 | 0.2500 | 0.3315 |
| 15 | 0.2425 | 0.3252 |
| 20 | 0.2371 | 0.3207 |
| 25 | 0.2329 | 0.3172 |
| 30 | 0.2294 | 0.3142 |
| 35 | 0.2264 | 0.3117 |
| 40 | 0.2239 | 0.3096 |
| 45 | 0.2216 | 0.3077 |
| 50 | 0.2195 | 0.3059 |
| 100 | 0.2059 | 0.2945 |
| 200 | 0.1919 | 0.2827 |
| 300 | 0.1835 | 0.2757 |
| 400 | 0.1775 | 0.2706 |
| 500 | 0.1728 | 0.2667 |
| 1000 | 0.1579 | 0.2542 |

**Reimplementation notes**

- Inputs:
  - `base_discount: float` — default 0.25.
  - `revenues: float` — $ millions; must be > 0 because of `ln`.
  - `block_fraction: float` — decimal fraction of shares outstanding. The formula multiplies it by 100 before `ln`. As written, the block term cancels between the anchor and firm terms. A faithful port keeps the term in both places. A corrected port might fix the anchor's block at a constant size.
  - `positive_earnings: bool` → DERN ∈ {0, 1}.
  - Bid-ask variant only: `cash_to_value: float` and `trading_volume_to_value: float` (0 for private firms).
- Outputs: `illiquidity_discount: float` (fraction) from each method. Apply as `value_after_discount = equity_value * (1 - discount)`.
- Edge cases:
  - revenues ≤ 0 or block_fraction ≤ 0 → `ln` undefined; raise an error.
  - Very large revenues can push the bid-ask discount negative in theory (Rev ≳ e^59 — never in practice). Clamp at 0 for safety.
  - Unprofitable firms with tiny revenues get a discount above the 25% base. That is intended — see Sheet2.
  - The two sheets share DERN via a cross-sheet link. In Python, make it one parameter.

---

### minoritydiscount.xls

**Purpose:** Estimates the **minority (lack of control) discount** for a minority stake in a private firm. Damodaran's view: the value of control = difference between the firm's *optimal* value (run by a value-maximizing controller) and its *status quo* value (run by incumbent management). A majority stake carries the power to move the firm to the optimal; a minority stake does not, so it is priced off the status quo value. Used when valuing a below-50% stake in a private business, or when setting the premium for a controlling stake.

**Sheets:** `Sheet1` (only populated sheet; Sheet2/Sheet3 empty).

**Inputs**

| Cell | Label | Example value |
|---|---|---|
| B2 | Optimal value for equity | 14700.0 |
| B3 | Status quo value for equity | 12500.0 |
| B4 | Majority stake (fraction) | 0.51 |
| B5 | Minority stake being valued (fraction) | 0.49 |

**Logic** (formulas extracted verbatim):

```
B7 = B4*B2                      Value of majority stake = majority % × optimal equity value
B8 = B2 + B5*B3                 Value of minority stake  (formula as stored — see note)
B9 = (B2-B3)/B2                 Minority discount = (optimal − status quo) / optimal
```

**Note on B8:** the stored formula is literally `=B2+(B5*B3)` = 14700 + 0.49×12500 = 20825, which is labeled "Value of minority stake =" but cannot be a stake value (it exceeds the whole firm). This is almost certainly a spreadsheet bug; the intended formula is `B5*B3` = minority % × status quo value = 6125 (inferred — consistent with B7's pattern and with Damodaran's published treatment). A Python port should implement `minority_stake_value = minority_pct * status_quo_value` and may optionally reproduce the literal cell for fidelity.

The headline result is B9: the maximum discount for lack of control, i.e., a minority share is worth `(1 − B9)` × its pro-rata share of optimal value, equivalently its pro-rata share of status quo value.

Caveat printed in the sheet (A11:A12): "This analysis will yield meaningful values only if the current price lies between the status quo and the optimal value. If not, …" (text truncated in file).

**Reference data:** none.

**Outputs**

| Cell | Meaning | Value |
|---|---|---|
| B7 | Value of majority stake (control basis) | 7497.0 |
| B8 | "Value of minority stake" (buggy as stored; intended 6125, see note) | 20825.0 |
| B9 | Minority discount (fraction) | 0.14965986394557823 |

**Worked example:** optimal 14,700 vs status quo 12,500 → minority discount = (14700 − 12500)/14700 = **14.97%**. Majority (51%) stake = 0.51 × 14700 = **7,497**. Minority (49%) stake intended = 0.49 × 12500 = **6,125** (sheet stores the buggy 20,825).

**Reimplementation notes**

- Inputs: `optimal_equity_value: float`, `status_quo_equity_value: float`, `majority_pct: float (0–1)`, `minority_pct: float (0–1)`.
- Outputs: `minority_discount = (optimal − status_quo)/optimal`; `majority_stake_value = majority_pct × optimal`; `minority_stake_value = minority_pct × status_quo`.
- Edge cases: optimal ≤ 0 → division undefined; if optimal < status quo the "discount" goes negative (means incumbent management is better than optimal — flag as invalid); model is only meaningful when status_quo ≤ current price ≤ optimal (per the sheet's own caveat). Probability-weighted variants (probability of management change) are not in this spreadsheet.

---

### pvtdiscrate.xls

**Purpose:** Estimates the **cost of capital (discount rate) for a private company**, correcting for the fact that a private owner is undiversified. Cost of equity uses either a **total beta** (market beta scaled up by dividing by the owner's correlation with the market) or a plain levered beta plus an ad-hoc "private company premium". Cost of debt is either entered directly or built from a **synthetic rating** (interest coverage ratio → rating → default spread) on the second sheet. Used when discounting private-company cash flows for a buyer who cannot diversify (contrast: for a sale to a public/diversified buyer, use the ordinary market beta).

**Sheets:** `Total Beta approach` (main), `Synthetic ratings` (cost-of-debt module), `Sheet3` (empty, skipped).

#### Sheet: Total Beta approach

**Inputs**

| Cell | Label | Example value |
|---|---|---|
| B3 | Unlevered beta for business (bottom-up, market beta) | 1.02 |
| B4 | Add a "private company premium" (P) or use a "total beta" (T)? | 'T' |
| B5 | If private company premium: the premium (decimal; 0.1 = 10%) | 0.1 |
| B6 | If total beta: correlation of comparable firms with the market (R, not R²) | 0.45 |
| B7 | Riskfree rate | 0.06 |
| B8 | Risk premium (equity risk premium) | 0.055 |
| B11 | Estimate a synthetic cost of debt? (Y/N) | 'N' |
| B12 | Pre-tax cost of debt (used when B11 = 'N') | 0.07 |
| B13 | Tax rate | 0.4 |
| B16 | Use industry average debt-to-capital ratio? (Y/N) | 'Y' |
| B17 | If yes: industry average market debt-to-capital ratio | 0.15 |
| B18 | If no: target debt ratio for the private firm | (empty) |

**Logic** (formulas extracted verbatim):

```
B21 = IF(B16="Y", B17, B18)                       Debt/Capital ratio used
B22 = (B3/B6) * (1 + (1-B13)*(B21/(1-B21)))       Total beta = (unlevered beta / correlation),
                                                   then levered at D/E = B21/(1-B21)
B25 = 1-B21                                        Equity weight
C25 = 1-B25                                        Debt weight
D25 = SUM(B25:C25)                                 = 1 (check)
B26 = IF(B4="T",
        B7 + B8*B22,                               Cost of equity, total-beta route
        B3*(1 + (1-B13)*(B21/(1-B21)))*B8 + B7 + B5)   Premium route: levered MARKET beta
                                                        × ERP + riskfree + private premium
C26 = IF(B11="Y",
        'Synthetic ratings'!D10 * (1-B13),         After-tax synthetic cost of debt
        B12 * (1-B13))                             After-tax entered cost of debt
D26 = B25*B26 + C25*C26                            Cost of capital (WACC)
```

Key mechanics: total beta = market beta ÷ correlation (because an undiversified owner bears total risk σ, not just β·σ_m; total beta = β/ρ). Levering uses the Hamada form `β_L = β_U·(1 + (1−t)·D/E)`. In the premium route, note the premium B5 is added as a flat addition to the cost of equity (not scaled by beta), and the beta used is the ordinary levered market beta, not the total beta.

**Outputs**

| Cell | Meaning | Value |
|---|---|---|
| B21 | Debt-to-capital ratio for private firm | 0.15 |
| B22 | Total beta for firm (levered) | 2.506666666666667 |
| B25 / C25 / D25 | Weights: equity / debt / total | 0.85 / 0.15 / 1.0 |
| B26 | Cost of equity | 0.19786666666666666 |
| C26 | After-tax cost of debt | 0.042 |
| D26 | Cost of capital | 0.17448666666666665 |

**Worked example:** B21 = 0.15 (industry). Total beta = (1.02/0.45)·(1 + 0.6·(0.15/0.85)) = 2.26667 × 1.105882 = **2.50667**. Cost of equity (T route) = 0.06 + 0.055 × 2.50667 = **19.787%**. After-tax cost of debt = 0.07 × (1 − 0.4) = **4.2%**. Cost of capital = 0.85 × 0.19787 + 0.15 × 0.042 = **17.449%**. ✓ all match stored values.

#### Sheet: Synthetic ratings

**Inputs**

| Cell | Label | Example value |
|---|---|---|
| F3 | Current EBIT (add back only long-term interest expense for financial firms) | 10000.0 |
| F4 | Current interest expenses (long-term only for financial firms) | 2500.0 |
| F5 | Current long-term government bond rate | 0.06 |

**Logic** (formulas extracted verbatim):

```
D7  = IF(F4>0, F3/F4, 10000000)          Interest coverage ratio; if no interest expense,
                                          set to 10,000,000 (→ AAA)
D8  = VLOOKUP(D7, A15:D28, 3)            Rating (approximate match on lower bound, col A)
D9  = VLOOKUP(D7, A15:D28, 4)            Default spread
D10 = F5 + D9                            Pre-tax cost of debt = riskfree + spread
```

Note: negative EBIT with positive interest gives a negative coverage ratio, which the VLOOKUP maps to the first row (D rating) because the table starts at −100000. Excel `VLOOKUP` with approximate match returns the row whose column-A value is the largest value ≤ the lookup value.

**Reference data (verbatim)** — single ratings table (no large/small firm split in this file):

| If interest coverage ratio is > | ≤ | Rating | Spread |
|---|---|---|---|
| -100000 | 0.499999 | D | 0.14 |
| 0.5 | 0.799999 | C | 0.127 |
| 0.8 | 1.249999 | CC | 0.115 |
| 1.25 | 1.499999 | CCC | 0.10 |
| 1.5 | 1.999999 | B- | 0.08 |
| 2.0 | 2.499999 | B | 0.065 |
| 2.5 | 2.999999 | B+ | 0.0475 |
| 3.0 | 3.499999 | BB | 0.035 |
| 3.5 | 4.499999 | BBB | 0.0225 |
| 4.5 | 5.999999 | A- | 0.02 |
| 6.0 | 7.499999 | A | 0.018 |
| 7.5 | 9.499999 | A+ | 0.015 |
| 9.5 | 12.499999 | AA | 0.01 |
| 12.5 | 100000 | AAA | 0.0075 |

**Outputs**

| Cell | Meaning | Value |
|---|---|---|
| D7 | Interest coverage ratio | 4.0 |
| D8 | Estimated bond rating | 'BBB' |
| D9 | Estimated default spread | 0.0225 |
| D10 | Estimated pre-tax cost of debt | 0.08249999999999999 |

**Worked example:** coverage = 10000/2500 = 4.0 → falls in (3.5, 4.499999] → **BBB**, spread **2.25%** → cost of debt = 6% + 2.25% = **8.25%**. Fed into C26 only if B11 = 'Y' (here B11 = 'N', so 7% entered rate is used instead).

**Reimplementation notes**

- Inputs: `unlevered_beta: float`, `mode: {"total_beta","premium"}`, `correlation: float (0–1, mode=total_beta)`, `private_premium: float (decimal, mode=premium)`, `riskfree: float`, `erp: float`, `tax_rate: float`, `use_synthetic_debt: bool`, `pretax_cost_of_debt: float` (if not synthetic), `use_industry_debt_ratio: bool`, `industry_dc: float` or `target_dc: float`; synthetic module: `ebit: float`, `interest_expense: float`, `long_bond_rate: float`.
- Outputs: `debt_to_capital`, `total_beta`, `cost_of_equity`, `after_tax_cost_of_debt`, `wacc`; synthetic module: `coverage`, `rating`, `spread`, `pretax_cost_of_debt`.
- Branches: (a) B4 T vs P selects total-beta vs levered-market-beta+premium cost of equity; (b) B11 Y/N selects synthetic vs entered cost of debt; (c) B16 Y/N selects industry vs target debt ratio; (d) coverage-ratio branch: interest ≤ 0 → coverage = 1e7 → AAA.
- Edge cases:
  - `debt_to_capital = 1` → division by zero in D/E = dc/(1−dc).
  - `correlation = 0` → division by zero in total beta; require ρ > 0.
  - Negative EBIT → negative coverage → D rating, 14% spread (the table's −100000 floor catches it).
  - B16 = 'N' with B18 empty: Excel treats the blank as 0 (all-equity). A port should require the target ratio in that branch.
  - `correlation` must be the correlation coefficient R. Damodaran sometimes derives it as sqrt(R²) from sector regressions.
  - The coverage-ratio table here is the single legacy table. Later Damodaran spreadsheets split it by market cap (large vs small firms) and update the spreads. Keep the table as a swappable parameter.
