# Status quo valuation: the target as currently run

**Core idea:** The status-quo value is the DCF value of a firm under existing management, with its current margins, current reinvestment policy and current capital structure. It is the anchor for everything else in control and acquisition analysis. Compare it to the market price and you learn whether the firm is undervalued. Subtract it from the restructured value and you get the value of control. Feed it into the acid test and it tells you whether the undervaluation motive survives. For firms with joint ventures and associate holdings, build it in pieces — each with its own cost of capital and growth — then consolidate.

**Formulas:**
- `Expected growth in operating income = Reinvestment rate × After-tax return on capital`.
- `Reinvestment rate = (Net capital expenditures + Change in working capital) / EBIT(1−t)`.
- `After-tax return on capital = EBIT(1−t) / Invested capital`.
- `FCFF = EBIT(1−t) − Net capital expenditures − Change in working capital`, equivalently `EBIT(1−t) × (1 − Reinvestment rate)`.
- `WACC = k_e × E/(D+E) + k_d × (1−t) × D/(D+E)`.
- `Terminal value_n = FCFF_{n+1} / (Stable WACC − g_stable)`.
- `Value of operating assets = Σ PV(FCFF in high growth) + PV(Terminal value)`.
- `Value of equity = Value of operating assets + Cash + Minority holdings (cross-holdings) − Debt − Minority interests`.

**Procedure:**
1. Normalize the base year. Get revenues, operating margin, EBIT, effective tax rate, and invested capital as currently reported.
2. Compute the current reinvestment rate and the current after-tax return on capital from those figures.
3. Set expected growth as the product of the two. Do not impose a growth rate independently; growth must be paid for with reinvestment.
4. Estimate the cost of equity bottom-up: unlevered beta for the businesses, relevered at the firm's current debt-to-equity ratio, with an equity risk premium reflecting the revenue geography.
5. Estimate the after-tax cost of debt from the firm's own rating or a synthetic rating, and build the WACC at the firm's current debt ratio.
6. Forecast FCFF over the high-growth period (commonly 5 years), then a terminal value using stable-growth assumptions.
7. If the firm holds joint ventures or associates, value each separately with its own margin, ROC, reinvestment rate, ERP and cost of capital, then add the operating-asset values.
8. Bridge from operating assets to equity: add cash and cross-holdings, subtract debt and minority interests.
9. Compare the equity value to the market capitalization. If market cap exceeds status-quo value, the firm is not undervalued.

**Reference data:**

SABMiller status quo, 2015, $ millions — a sum-of-parts consolidation:

| Item | SABMiller | + Coors JV | + Share of Associates | Consolidated |
|---|---|---|---|---|
| Revenues | 22,130.00 | 5,201.00 | 6,099.00 | |
| Operating margin | 19.97% | 15.38% | 10.72% | |
| Operating income (EBIT) | 4,420.00 | 800.00 | 654.00 | |
| Invested capital | 31,526.00 | 5,428.00 | 4,459.00 | |
| Beta | 0.7977 | 0.6872 | 0.6872 | |
| ERP | 8.90% | 6.00% | 7.90% | |
| Cost of equity | 9.10% | 6.12% | 7.43% | |
| After-tax cost of debt | 2.24% | 2.08% | 2.24% | |
| Debt to capital ratio | 14.67% | 0.00% | 0.00% | |
| Cost of capital | 8.09% | 6.12% | 7.43% | |
| After-tax return on capital | 10.33% | 11.05% | 11.00% | |
| Reinvestment rate | 16.02% | 40.00% | 40.00% | |
| Expected growth rate | 1.65% | 4.42% | 4.40% | |
| Years of growth | 5 | 5 | 5 | |
| PV of FCFF in high growth | 11,411.72 | 1,715.25 | 1,351.68 | |
| Terminal value | 47,711.04 | 15,094.36 | 9,354.28 | |
| Value of operating assets | 43,747.24 | 12,929.46 | 7,889.56 | **64,566.26** |
| + Cash | | | | 1,027.00 |
| − Debt | | | | 12,918.00 |
| − Minority interests | | | | 1,183.00 |
| **Value of equity** | | | | **51,492.26** |

SAP status quo, May 5, 2005, euros: risk-free rate 3.41%, beta 1.26, ERP 4.25% (4% mature market + 0.25% country), so cost of equity = `3.41% + 1.26 × 4.25% = 8.77%`. After-tax cost of debt = `(3.41% + 0.35%) × (1 − 0.3654) = 2.39%`. WACC = `8.77% × 0.986 + 2.39% × 0.014 = 8.68%`. Base FCFF = `1,414 − 831 − (−19) = 602`; reinvestment rate = `812/1,414 = 57.42%`; ROC = 19.93%, so growth = `0.5742 × 0.1993 = 11.44%` for 5 years, declining to 3.41%. Stable phase: beta 1.00, debt ratio 20%, cost of capital 6.62%, ROC 6.62%, reinvestment rate 51.54%. `TV_10 = 1,717/(0.0662 − 0.0341) = 53,546`. Operating assets 31,615 + cash 3,018 − debt 558 − pension liability 305 − minority interest 55 = equity 34,656; less options 180 gives **€106.12 per share** against a market price of €122.

Blockbuster status quo, 2005, $ millions: cost of equity = `4.10% + 1.10 × 4% = 8.50%`; after-tax cost of debt = `(4.10% + 2%) × (1 − 0.35) = 3.97%`; WACC = `8.50% × 0.486 + 3.97% × 0.514 = 6.17%`. Base EBIT(1−t) = 163, net cap ex 39, ΔWC 4, so FCFF = 120. Reinvestment rate = `43/163 = 26.46%`, ROC = 4.06%, growth = `0.2646 × 0.0406 = 1.07%` for 5 years. FCFF years 1–5: $121, $123, $118, $109, $99. Stable: g = 3%, cost of capital 6.76%, ROC 6.76%, reinvestment rate 44.37%. `TV_5 = 104/(0.0676 − 0.03) = 2,714`. Operating assets 2,472 + cash 330 − debt 1,847 = equity **$955M**, or **$5.13 per share**.

**Worked example:** Follow the SABMiller consolidation. The parent's own operating assets are worth $43,747.24M. The Coors JV stake adds $12,929.46M and the associates add $7,889.56M, for $64,566.26M of operating assets. Add cash of $1,027M, subtract debt of $12,918M and minority interests of $1,183M, and equity is worth $51,492.26M — about $51.5B.

Check the growth line for internal consistency: `16.02% × 10.33% = 1.65%`, matching the table. SABMiller's growth is low because it reinvests little, not because its business is bad.

Now compare with the market: $75B on September 15, 2015, against $51.5B of status-quo value. SABMiller was not undervalued. The undervaluation motive for the acquisition is dead before any premium is discussed.

**Determinism:**
- DETERMINISTIC: given margins, tax rate, invested capital, reinvestment rate, betas, ERP, debt ratios and growth-period length, the entire DCF and the equity bridge are computable. So are the identities `g = RR × ROC` and `Reinvestment rate = (Net cap ex + ΔWC)/EBIT(1−t)`.
- JUDGMENT: base-year normalization; the unlevered beta and the ERP for a firm's revenue geography; the length of the high-growth period; the stable-growth rate and stable ROC; whether to value JVs and associates separately or consolidate them.

**Pitfalls:**
- Imposing a growth rate that the firm's reinvestment cannot fund. Growth must equal reinvestment rate times ROC.
- Using the acquirer's cost of capital instead of the target's.
- Forgetting cross-holdings. In the SABMiller restructured case, minority holdings of $20,819M sit in the equity bridge; omitting them understates equity badly.
- Consolidating a JV's operating assets while also carrying its equity value as a holding — double counting.
- Treating status-quo value as a verdict on the business. A low value with a low ROC is a signal of control potential, not a reason to walk away.

**Sources:**
- `valuations--lecture_notes--spring_2021--valpacket3spr21 p.125, p.140, p.143`
- `valuations--lecture_notes--spring_2020--valpacket3spr20 p.125, p.140, p.143`

**Related:** [[restructured-value-and-value-of-control]], [[three-reasons-and-acid-test]], [[target-discount-rate-discipline]], [[expected-value-of-control]], [[abinbev-sabmiller-case]], [[terminal-value]], [[bottom-up-beta]], [[fcff]]
