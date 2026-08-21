# Unlevering and relevering betas

**Core idea:** A beta estimated from stock prices is a **levered** beta: it embeds whatever debt the firm carried. To compare firms, to build a beta from comparables, or to reprice a firm at a different capital structure, you must first strip leverage out (unlever) and then put your own leverage back in (relever). The conventional formula assumes debt carries no market risk. A debt-adjusted version exists for firms whose debt clearly does carry market risk, but debt betas are hard to estimate. Two further wrinkles matter in practice: cash is a zero-beta asset that drags a company's unlevered beta below its operating beta, and using **net** debt instead of gross debt changes the answer — legitimately, as long as you use net debt consistently everywhere else.

**Formulas:**
- **Unlever:** β_u = β_L / (1 + (1 − t) × D/E).
- **Relever:** β_L = β_u × (1 + (1 − t) × D/E).
- Debt-adjusted relever: β_L = β_u × (1 + (1 − t)(D/E)) − β_debt × (1 − t) × (D/E), where β_debt = beta of the firm's debt.
- Some versions drop the tax term entirely: β_L = β_u × (1 + D/E).
- **Cash correction** (converting a company unlevered beta to a pure business beta): Business unlevered beta = Company unlevered beta / (1 − Cash/Firm value). This comes from the portfolio identity (Cash/Value)×0 + (1 − Cash/Value)×β_operating = β_company.
- **Net debt:** Net D/E = (Debt − Cash) / Market value of equity; β_L(net) = β_u × (1 + (1 − t) × Net D/E).
- Converting a debt-to-capital ratio to D/E: D/E = d / (1 − d), where d = Debt/(Debt + Equity).
- Portfolio identity: the beta of any portfolio, merged firm, or multi-division company is the market-value weighted average of component betas.

Symbols: β_L = levered/equity beta; β_u = unlevered/asset beta; t = marginal tax rate; D/E = **market-value** debt-to-equity ratio.

**Procedure:**
1. Start with the beta you have. If it is a **regression** beta, it is levered at the *average* D/E over the regression window — use that average D/E to unlever, not today's.
2. Unlever with the firm's marginal tax rate: β_u = β_L / (1 + (1 − t)(D/E)).
3. If you want the beta of the **operating business** rather than the company, divide by (1 − Cash/Firm value). Cash has a beta of roughly zero, so a cash-rich company's unlevered beta understates its business risk.
4. Relever at the D/E you actually want: current market D/E for today's cost of equity, target D/E for a normalized one, or a schedule of D/E ratios if leverage will change over time (in which case the levered beta changes year by year).
5. Use **market values** for both debt and equity in the ratio. Estimate the market value of debt by treating total book debt as one coupon bond: MV of debt = Interest expense × [annuity factor at the pre-tax cost of debt over the average maturity] + Book debt / (1 + cost of debt)^maturity. Add the capitalized value of operating leases to debt.
6. Decide gross versus net debt, and then be consistent. If you lever the beta on a net debt ratio, the cost-of-capital weights must also use net debt.
7. For a **merger**, unlever each firm's beta at its own D/E, take the **firm-value**-weighted average of the unlevered betas, then relever at the D/E implied by how the deal is financed.
8. For financial-service firms, skip all of this — debt and equity are not cleanly separable for banks, so use median levered comparable betas directly (see [[bottom-up-beta]]).

**Reference data:**

The full relevering schedule for a company with β_u = 1.284875 and t = 36% (`levbeta.xls`), by debt-to-capital ratio 0% to 90%: 1.2849, 1.3762, 1.4905, 1.6373, 1.8331, 2.1072, 2.5184, 3.2036, 4.5742, 8.6858. The "effect of leverage" at each level is that beta minus 1.2849. The schedule stops at 90% because D/E is undefined at 100% debt.

The `levbeta.xls` utility, step by step:

| Input | Example |
|---|---|
| Current (regression) beta | 1.40 |
| Marginal tax rate | 36% |
| Average D/E over the regression period | 14% |
| Market value of equity | 50,889.038 |
| Book value of debt | 12,342 |
| Average maturity of debt | 5 years |
| Interest expense, trailing 12 months | 876.282 |
| Current market interest rate on the debt | 7.5% |
| Custom D/E for relevering | 35% |

Computed: MV of debt = 876.282 × 4.04588 + 12,342 × 0.696559 = **12,142.263**; β_u = 1.40 / (1 + 0.64 × 0.14) = **1.284875**; current D/E = 12,142.263 / 50,889.038 = 23.862% → current levered beta = 1.284875 × (1 + 0.64 × 0.23862) = **1.481083**; at the custom D/E of 35% → 1.284875 × 1.224 = **1.572687**.

**Worked example (Disney, unlever then relever):** Regression beta 1.25, estimated over 2008-2013 when Disney's average market D/E was 19.44%, with a marginal tax rate of 36.1%. Unlevered beta = 1.25 / (1 + (1 − 0.361) × 0.1944) = **1.1119**. Relevering that at a 50% debt-to-capital ratio (D/E = 100%) gives 1.1119 × (1 + 0.639 × 1.00) ≈ **1.82**.

**Worked example (cash correction, Studio Entertainment):** Median regression equity beta for US movie firms = 1.24; median gross D/E = 21.30/78.70 = 27.06%; tax rate 40%. Company unlevered beta = 1.24 / (1 + 0.6 × 0.2706) = **1.0668**. Median cash/firm value = 2.96%, so the pure movie-business beta = 1.0668 / (1 − 0.0296) = **1.0993**. The net-debt shortcut gives a slightly different answer: net D/E = (21.30 − 2.96)/78.70 = 23.30% → 1.24 / (1 + 0.6 × 0.233) = **1.0879**.

**Worked example (gross versus net debt, Embraer):** Unlevered beta 0.95, tax rate 34%, debt 1,953m BR, cash 2,320m BR, market equity 11,042m BR.
- Gross: D/E = 1953/11,042 = 18.95% → β_L = 0.95 × (1 + 0.66 × 0.1895) = **1.07**.
- Net: Net D/E = (1953 − 2320)/11,042 = **−3.32%** (cash exceeds debt) → β_L = 0.95 × (1 + 0.66 × (−0.0332)) = **0.93**.
The net-debt cost of equity is much lower, but the cost of capital roughly evens out — because the debt ratio in the cost-of-capital weights must then also be the net debt ratio.

**Worked example (merger beta, Disney / Capital Cities 1996):** Disney equity beta 1.15, debt $3,186m, equity $31,100m, firm value $34,286m, D/E 0.10. Capital Cities beta 0.95, debt $615m, equity $18,500m, firm value $19,115m, D/E 0.03. Tax rate 36%.
- Unlever: Disney 1.15/(1 + 0.64×0.10) = 1.08; Cap Cities 0.95/(1 + 0.64×0.03) = 0.93.
- Combine on **firm-value** weights: 1.08 × (34,286/53,401) + 0.93 × (19,115/53,401) = **1.026**.
- Relever under all-equity financing: debt = 3,801, equity = 49,600, D/E = 7.66% → β = 1.026 × (1 + 0.64 × 0.0766) = **1.08**.
- Relever under the actual deal (Disney borrowed $10bn): debt = 13,801, equity = 39,600, D/E = 34.82% → β = 1.026 × (1 + 0.64 × 0.3482) = **1.25**.

**Determinism:**
- DETERMINISTIC: (β_L, t, D/E) → β_u and back; (company β_u, Cash/Value) → business β_u; (debt, cash, equity) → gross and net D/E; (interest expense, book debt, maturity, cost of debt) → market value of debt; (component betas, market-value weights) → combined beta; (β_u, t, debt-to-capital schedule) → levered beta at every leverage level.
- JUDGMENT: the marginal tax rate to use; whether to use gross or net debt; whether debt carries market risk and what β_debt is; whether to apply the cash correction; which D/E to relever at (current, target, or a time path); the average maturity assumption in the market-value-of-debt calculation.

**Pitfalls:**
- Unlevering a regression beta at **today's** D/E instead of the average D/E over the regression window.
- Using book-value debt and equity in the D/E ratio. The formula requires market values.
- Mixing gross-debt betas with net-debt cost-of-capital weights, or vice versa. The internal inconsistency shows up as a wrong cost of capital.
- Ignoring cash. A company holding 20% of its value in cash has an unlevered beta well below its operating beta.
- Forgetting operating leases in debt when computing D/E.
- Unlevering and relevering betas for banks and insurers, where debt is raw material rather than financing.
- Using firm value weights when combining *equity* betas, or equity weights when combining *unlevered* betas. Unlevered betas combine on firm value.
- Applying a single levered beta across a forecast in which the debt ratio changes materially.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.90-93, p.98
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.88, p.91, p.96
- corporate_finance--lecture_slides--cfpacket1spr20 p.158-165, p.170
- spreadsheet `levbeta.xls` (Corporate Finance collection): unlever/relever utility with a full 0-90% debt-ratio schedule

**Related:** [[bottom-up-beta]], [[beta-determinants]], [[regression-beta]], [[cost-of-equity-assembly]], [[optimal-capital-structure]], [[market-value-of-debt]]
