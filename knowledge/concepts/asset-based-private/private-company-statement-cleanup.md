# Cleaning up private company financial statements

**Core idea:** A private firm's reported income statement is not a valuation input until it has been restated. Four things go wrong. The history is short. The accounting standards are looser than a public firm faces. Personal and business expenses are intermingled. And there is no clean line between "salaries" and "dividends", because both end up with the same person. The two adjustments that matter most in practice: charge a **market salary** for owner labour that is currently free, and treat **operating leases as debt** rather than as an operating expense. Both lower reported operating income and both change the capital structure you feed into the cost of capital.

**Formulas:**
- Owner compensation: `Adjusted operating income = Reported operating income − (Market salary for the owner's role − Salary actually paid)`
- Lease capitalization: `Debt value of leases = Σ_t Lease payment_t / (1 + r_d)^t`. For a level annuity: `Debt = Lease payment × [1 − (1 + r_d)^(−n)] / r_d`, where `r_d` = pre-tax cost of debt, `n` = years remaining on the lease.
- `Adjusted operating income (after lease reclassification) = Reported operating income + Lease expense − Depreciation on the leased asset`. The packet's simplification adds back the full lease expense.
- `Imputed interest expense = r_d × Debt value of leases`
- `Adjusted taxable income = Adjusted operating income − Imputed interest`; `Adjusted net income = Adjusted taxable income × (1 − t)`
- Symbols: `t` = tax rate; `r_d` = pre-tax cost of debt used to discount the lease.

**Procedure:**
1. Get every year of statements available and note how few there are. A three-year history supports far less normalization than a ten-year one.
2. Scan the expense lines for personal items run through the business — vehicles, travel, family payroll, home-office costs. Remove genuinely personal items from operating expenses; they are distributions, not costs.
3. Find uncompensated or under-compensated owner labour. **Decision rule: charge the market wage for the role the owner actually performs**, whether or not any salary was paid. If the owner is drawing an above-market salary, cut it to market instead — the excess is a dividend.
4. Identify lease and other quasi-debt commitments. Pull the payment schedule and the years remaining.
5. Discount the lease commitments at the firm's pre-tax cost of debt to get a debt value. Add that to debt.
6. Remove the lease expense from operating costs and add an imputed interest charge equal to `r_d × lease debt`.
7. Recompute operating income, taxable income, taxes and net income on the adjusted basis.
8. Feed the adjusted operating income into the valuation and the lease debt into both the capital-structure weights and the final equity bridge.
9. Check whether the business is running at full capacity. If it is, revenue growth requires capital expenditure, not just optimism.

**Reference data — the restaurant's three-year history ($000s):**

| Item | 3 years ago | 2 years ago | Last year | Note |
|---|---|---|---|---|
| Revenues | 800 | 1,100 | 1,200 | Operating at full capacity |
| − Operating lease expense | 120 | 120 | 120 | 12 years left on the lease |
| − Wages | 180 | 200 | 200 | Owner/chef draws no salary |
| − Material | 200 | 275 | 300 | 25% of revenues |
| − Other operating expenses | 120 | 165 | 180 | 15% of revenues |
| Operating income | 180 | 340 | 400 | |
| − Taxes | 72 | 136 | 160 | 40% tax rate |
| Net income | 108 | 204 | 240 | |

**Worked example — the restaurant, stated vs adjusted ($000s):**

| Item | Stated | Adjusted | Note |
|---|---|---|---|
| Revenues | 1,200 | 1,200 | |
| − Operating lease expense | 120 | — | Leases are financial expenses |
| − Wages | 200 | 350 | Hire a chef for $150,000/year |
| − Material | 300 | 300 | |
| − Other operating expenses | 180 | 180 | |
| Operating income | 400 | 370 | |
| − Interest expense | 0 | 69.62 | 7.5% of 928.23 |
| Taxable income | 400 | 300.38 | |
| − Taxes | 160 | 120.15 | 40% rate |
| Net income | 240 | 180.23 | |
| Debt | 0 | 928.23 | PV of $120K for 12 years @ 7.5% |

The lease debt: `120 × [1 − 1.075^(−12)] / 0.075 = 928.23` (thousands). Imputed interest: `0.075 × 928.23 = 69.62`. Adjusted operating income: `400 + 120 − 150 = 370`. Reported net income of $240K is really $180.23K once the chef is paid and the lease is treated as financing.

**Determinism:**
- DETERMINISTIC: `{lease payment, years remaining, pre-tax cost of debt} → lease debt → imputed interest`. `{reported operating income, lease expense, market salary, salary paid, tax rate} → adjusted operating income, taxable income, net income`. Fully scriptable.
- JUDGMENT: the market salary for the owner's role; which expenses are genuinely personal; the discount rate to use on the leases (usually the firm's own pre-tax cost of debt, which itself depends on the coverage ratio you are recomputing); and whether the reported history is representative at all. That judgment needs comparable-role compensation data, the lease schedule, and enough access to the business to spot intermingled expenses.

**Pitfalls:**
- Valuing a private business off reported operating income when the owner works for free. The restaurant's $400K becomes $370K on that adjustment alone.
- Leaving leases as operating expenses. That understates debt, overstates equity value, and inflates the interest coverage ratio used for the synthetic rating.
- Circularity: the pre-tax cost of debt used to capitalize leases depends on a coverage ratio that itself uses the lease expense as interest. Damodaran uses 7.5% for both here; check for consistency.
- Forgetting to subtract the lease debt at the end. Firm value minus $928.23K of lease debt is what gets the equity value of $520.99K.
- Reading three good years as a trend. A private firm's short history is thin evidence.
- Missing that a business at full capacity cannot grow revenues without reinvestment.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket2spr21 p.126, p.130-131, p.138
- valuations--lecture_notes--spring_2020--valpacket2spr20 p.124, p.128-129, p.136

**Related:** [[private-company-valuation-framework]], [[private-company-cost-of-capital]], [[key-person-discount]], [[private-to-private-valuation]], [[operating-lease-capitalization]], [[normalizing-earnings]], [[accounting-earnings-adjustments]]
