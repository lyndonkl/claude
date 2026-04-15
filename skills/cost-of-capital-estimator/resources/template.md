# Cost of Capital Estimation Templates

Worksheets for riskfree rate derivation, ERP buildup, beta estimation, synthetic rating, cost of equity, cost of debt, and WACC computation.

## Table of Contents
- [Riskfree Rate Determination](#riskfree-rate-determination)
- [ERP Buildup Worksheet](#erp-buildup-worksheet)
- [Beta Estimation Template](#beta-estimation-template)
- [Cost of Equity Calculation](#cost-of-equity-calculation)
- [Synthetic Rating Worksheet](#synthetic-rating-worksheet)
- [Cost of Debt Calculation](#cost-of-debt-calculation)
- [WACC Computation Worksheet](#wacc-computation-worksheet)
- [WACC Sensitivity Table](#wacc-sensitivity-table)

---

## Riskfree Rate Determination

**Analysis Currency**: [e.g., BRL, USD, EUR, INR]

**Method A -- Subtract sovereign default spread (preferred for countries with liquid government bonds):**

| Item | Value |
|------|-------|
| Local government bond yield (10-year) | ___% |
| Sovereign credit rating (Moody's) | ___ |
| Sovereign default spread for that rating | ___% |
| **Riskfree rate = Bond yield - Default spread** | **___%** |

**Method B -- Inflation differential from US rate (use when local bond market is thin or unreliable):**

| Item | Value |
|------|-------|
| US 10-year Treasury yield | ___% |
| Expected inflation (local currency) | ___% |
| Expected inflation (USD) | ___% |
| **Riskfree rate = (1 + US Rf) x (1 + Infl_local) / (1 + Infl_US) - 1** | **___%** |

**Validation:**
- [ ] Rate is positive
- [ ] Rate is denominated in the same currency as projected cash flows
- [ ] If Method A and B both computed, they are within 50bps of each other
- [ ] Rate does not include a default premium (sovereign risk removed)

---

## ERP Buildup Worksheet

### Mature Market Premium

| Item | Value |
|------|-------|
| Implied ERP for S&P 500 (current) | ___% |
| Source / Date | ___ |

### Country Risk Premium (CRP) by Geography

| Country / Region | Revenue Weight | Sovereign Rating | Default Spread | Equity/Bond Vol Ratio | Country ERP | Weighted CRP |
|-----------------|---------------|-----------------|---------------|----------------------|-------------|-------------|
| [Country 1] | ___% | ___ | ___% | ___x | ___% | ___% |
| [Country 2] | ___% | ___ | ___% | ___x | ___% | ___% |
| [Country 3] | ___% | ___ | ___% | ___x | ___% | ___% |
| [Country 4] | ___% | ___ | ___% | ___x | ___% | ___% |
| **Total** | **100%** | | | | | **___%** |

Country ERP = Default Spread x (Equity Vol / Bond Vol). Use 1.5x as default ratio if country-specific data unavailable.

Weighted CRP = Revenue Weight x Country ERP for each row, summed.

### Total ERP

| Item | Value |
|------|-------|
| Mature market premium | ___% |
| Operation-weighted CRP | + ___% |
| **Total ERP** | **= ___%** |

**Validation:**
- [ ] Weights sum to 100%
- [ ] Mature market ERP is implied (not historical average)
- [ ] CRP based on where the company operates (revenue), not where it is incorporated
- [ ] Total ERP is reasonable for the geography (typically 5-12% for emerging markets)

---

## Beta Estimation Template

### Option A: Bottom-Up Beta (Preferred)

**Step 1 -- Select comparable firms**

| # | Company | Industry Match | Region | Levered Beta | D/E Ratio | Tax Rate | Unlevered Beta |
|---|---------|---------------|--------|-------------|-----------|----------|---------------|
| 1 | ___ | ___ | ___ | ___ | ___ | ___% | ___ |
| 2 | ___ | ___ | ___ | ___ | ___ | ___% | ___ |
| 3 | ___ | ___ | ___ | ___ | ___ | ___% | ___ |
| ... | ... | ... | ... | ... | ... | ... | ... |

Unlevered Beta = Levered Beta / (1 + (1 - Tax Rate) x (D/E))

**Step 2 -- Compute median unlevered beta**

| Item | Value |
|------|-------|
| Number of comparable firms | ___ |
| Median unlevered beta | ___ |
| Mean unlevered beta (cross-check) | ___ |

**Step 3 -- Relever at target company's capital structure**

| Item | Value |
|------|-------|
| Target D/E ratio (market values) | ___ |
| Marginal tax rate | ___% |
| Relevered beta = Unlevered x (1 + (1-t)(D/E)) | ___ |

### Option B: Regression Beta (Secondary)

| Item | Value |
|------|-------|
| Market index used | ___ |
| Regression period | ___ |
| Return interval (monthly/weekly) | ___ |
| Regression beta | ___ |
| Standard error | ___ |
| R-squared | ___ |

**Validation:**
- [ ] Minimum 15 comparable firms for bottom-up beta
- [ ] Unlevering used each firm's own D/E and tax rate (not a single average)
- [ ] Relevering used the target company's current or target D/E
- [ ] If regression beta used, standard error is noted (typically 0.20+)
- [ ] For private companies: total beta adjustment considered if owner is undiversified

---

## Cost of Equity Calculation

**Standard CAPM:**

| Item | Value |
|------|-------|
| Riskfree rate (from Step 1) | ___% |
| Beta (from Step 3) | ___ |
| Total ERP (from Step 2) | ___% |
| **Cost of Equity = Rf + Beta x ERP** | **___%** |

**Expanded form (showing CRP separately):**

| Item | Value |
|------|-------|
| Riskfree rate | ___% |
| + Beta x Mature market ERP | + ___% |
| + Lambda x Operation-weighted CRP | + ___% |
| **Cost of Equity** | **= ___%** |

(Lambda = 1 for default; use company-specific lambda only if the firm's exposure to country risk differs meaningfully from revenue proportions.)

**Validation:**
- [ ] Cost of equity is higher than riskfree rate (risk premium is positive)
- [ ] Cost of equity is in the same currency as the riskfree rate
- [ ] For US companies: typically 7-12%. For emerging market companies: typically 12-20%+
- [ ] Cost of equity exceeds cost of debt (equity is riskier than debt)

---

## Synthetic Rating Worksheet

| Item | Value |
|------|-------|
| Operating income (EBIT) | ___ |
| Interest expense | ___ |
| **Interest coverage ratio = EBIT / Interest** | **___x** |
| Firm size category | [ ] Large (revenue > $5B) / [ ] Small |
| Synthetic rating (from lookup table) | ___ |
| Default spread for that rating | ___% |

Lookup the interest coverage ratio in the synthetic rating table in [methodology.md](methodology.md#synthetic-rating-table). Use the large-firm table if annual revenue exceeds $5B; otherwise use the small-firm table.

**Validation:**
- [ ] Interest coverage computed from most recent fiscal year (or trailing twelve months)
- [ ] Correct table used (large vs. small firm)
- [ ] If company has an actual credit rating, compare to synthetic -- they should be within 1-2 notches
- [ ] For firms with no debt or negligible interest, assign highest rating (AAA)

---

## Cost of Debt Calculation

| Item | Value |
|------|-------|
| Riskfree rate (same as cost of equity) | ___% |
| Default spread (from synthetic rating) | + ___% |
| **Pre-tax cost of debt** | **= ___%** |
| Marginal tax rate | ___% |
| **After-tax cost of debt = Pre-tax x (1 - t)** | **= ___%** |

**Validation:**
- [ ] Pre-tax cost of debt is higher than riskfree rate
- [ ] Pre-tax cost of debt is lower than cost of equity
- [ ] After-tax cost of debt reflects marginal (not effective) tax rate
- [ ] Currency matches the rest of the analysis

---

## WACC Computation Worksheet

### Capital Structure Weights

| Component | Market Value | Weight |
|-----------|-------------|--------|
| Equity (shares x price) | ___ | ___% |
| Debt (market or book approximation) | ___ | ___% |
| **Total** | **___** | **100%** |

### WACC Calculation

| Component | Cost | Weight | Contribution |
|-----------|------|--------|-------------|
| Equity | ___% | ___% | ___% |
| Debt (after-tax) | ___% | ___% | ___% |
| **WACC** | | | **___%** |

WACC = Cost of Equity x (E/(D+E)) + After-tax Cost of Debt x (D/(D+E))

**Validation:**
- [ ] Weights use market values (not book values) for equity
- [ ] WACC is between cost of debt (after-tax) and cost of equity
- [ ] WACC is in the same currency as projected cash flows
- [ ] For US companies: typically 7-10%. For emerging market companies: typically 10-16%+

---

## WACC Sensitivity Table

Compute WACC at varying debt ratios to see the cost of capital curve. This also feeds into the capital-structure-optimizer skill.

| Debt Ratio (D/(D+E)) | D/E | Levered Beta | Cost of Equity | Interest Coverage | Rating | Default Spread | Pre-tax kd | After-tax kd | WACC |
|----------------------|-----|-------------|---------------|-------------------|--------|---------------|-----------|-------------|------|
| 0% | 0.00 | ___ | ___% | inf | AAA | ___% | ___% | ___% | ___% |
| 10% | 0.11 | ___ | ___% | ___ | ___ | ___% | ___% | ___% | ___% |
| 20% | 0.25 | ___ | ___% | ___ | ___ | ___% | ___% | ___% | ___% |
| 30% | 0.43 | ___ | ___% | ___ | ___ | ___% | ___% | ___% | ___% |
| 40% | 0.67 | ___ | ___% | ___ | ___ | ___% | ___% | ___% | ___% |
| 50% | 1.00 | ___ | ___% | ___ | ___ | ___% | ___% | ___% | ___% |
| 60% | 1.50 | ___ | ___% | ___ | ___ | ___% | ___% | ___% | ___% |
| 70% | 2.33 | ___ | ___% | ___ | ___ | ___% | ___% | ___% | ___% |
| 80% | 4.00 | ___ | ___% | ___ | ___ | ___% | ___% | ___% | ___% |
| 90% | 9.00 | ___ | ___% | ___ | ___ | ___% | ___% | ___% | ___% |

**How to fill in each row:**
1. For the given debt ratio, compute D/E = Debt Ratio / (1 - Debt Ratio).
2. Levered Beta = Unlevered Beta x (1 + (1-t) x D/E).
3. Cost of Equity = Riskfree Rate + Levered Beta x ERP.
4. Interest coverage at that debt level = EBIT / (Debt x Pre-tax kd). This is iterative -- estimate the interest expense at that debt level using the prior row's cost of debt as an initial guess, then update.
5. Map interest coverage to rating and default spread.
6. Pre-tax kd = Riskfree Rate + Default Spread.
7. After-tax kd = Pre-tax kd x (1 - t).
8. WACC = ke x (1 - Debt Ratio) + After-tax kd x Debt Ratio.

The minimum WACC row identifies the optimal capital structure.
