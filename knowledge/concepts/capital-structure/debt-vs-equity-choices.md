# Debt vs. equity: what the choices are and how to measure the mix

**Core idea:** A business can raise money in only two fundamental ways. Debt is a promise to make contractually fixed payments (interest and principal); fail to make them and you lose control of the business. Equity is the residual claim: whatever cash flow is left after debt is served. Real securities lie on a continuum between the two — pure debt (bank debt, commercial paper, corporate bonds), hybrids (convertible debt, preferred stock, option-linked bonds), and equity (owner's equity, venture capital, common stock, warrants) — so classification must be done on economic substance, not on the name of the security. Before any capital structure analysis you must be able to say how much debt a firm already uses, which means computing a debt-to-capital ratio with debt defined economically (all interest-bearing liabilities plus lease-like fixed commitments) and equity defined at market value. A recurring trap: managers justify debt on the grounds that "debt is cheaper than equity." It is cheaper, but only because the lender has first claim on cash flows and a pre-set payment while the equity investor is last in line; borrowing at a lower rate does not create value, it just moves risk onto equity.

**Formulas:**
- `Debt to Capital Ratio = D / (D + E)` — D = market value of all interest-bearing debt (short- and long-term) plus the debt value of other contractually pre-set commitments (capitalized leases); E = value of equity, on a book basis or (preferred) market basis. Book and market versions can differ enormously (Disney 2013: 22.88% book vs 11.58% market).
- `Debt to Equity Ratio D/E = (D/(D+E)) / (1 − D/(D+E))` — used to relever betas.
- `Net Debt to Capital = (D − Cash) / (D − Cash + E)`.
- Debt value of an operating lease commitment stream (Damodaran's capitalization, used in capstru.xlsx): `Lease Debt = Σ_{t=1..5} Commitment_t/(1+kd)^t + [ (Lump/n) × (1 − (1+kd)^(−n)) / kd ] / (1+kd)^5`, where `n = ROUND(Lump ÷ average of years 1–5 commitments)` is the number of years embedded in the "year 6 and beyond" lump sum and kd = the firm's pre-tax cost of debt.

**Procedure:**
1. Classify each claim. It is debt-like if payments are contractually fixed, tax-deductible, high priority in distress, finite-maturity, and carry no management control. It is equity-like if it is a residual, non-deductible, lowest-priority, infinite-life claim carrying control. Anything with features of both is a hybrid — split or judge which side dominates.
2. Include as debt every commitment with contractually pre-set payments that must be made regardless of the firm's financial standing. Operating leases qualify: capitalize them with the formula above and add the lease debt to interest-bearing debt (this also restates EBIT, interest expense and depreciation — see [[cost-of-capital-approach]]).
3. Value debt at market where possible. If only book debt is available, price it as a bond: `MV Debt = Interest Expense × [1 − (1+kd)^(−maturity)] / kd + Book Debt / (1+kd)^maturity`, using the weighted average maturity of debt.
4. Value equity at market (shares outstanding × price). For a private firm, estimate it from comparables (see [[optimal-debt-ratio-by-firm-type]]).
5. Compute D/(D+E) on both book and market bases; carry the market ratio into all optimal-capital-structure work.
6. Never argue for more debt on the ground that its rate is lower than the cost of equity. The right argument is the full trade-off ([[debt-equity-tradeoff]]) and the effect on cost of capital ([[cost-of-capital-approach]]).

**Reference data:** Existing financing choices of the case companies (2013 snapshot; illustrates the dimensions along which debt varies — bank vs bond, maturity, currency, fixed vs floating):

| Item | Disney | Vale | Tata Motors | Baidu |
|---|---|---|---|---|
| BV of interest-bearing debt | $14,288m | $48,469m | Rs 535,914 | ¥17,844 |
| MV of interest-bearing debt | $13,028m | $41,143m | Rs 477,268 | ¥15,403 |
| Lease debt | $2,933m | $1,248m | 0 | ¥3,051 |
| Bank debt | 7.93% | 59.97% | 62.26% | 100.00% |
| Bonds/Notes | 92.07% | 40.03% | 37.74% | 0.00% |
| Maturity <1 yr | 13.04% | 6.08% | 0.78% | 1.98% |
| 1–5 yrs | 48.93% | 23.12% | 30.24% | 68.62% |
| 5–10 yrs | 20.31% | 29.44% | 57.90% | 29.41% |
| 10–20 yrs | 4.49% | 3.00% | 10.18% | 0.00% |
| >20 yrs | 13.24% | 38.37% | 0.90% | 0.00% |
| Domestic currency | 94.51% | 34.52% | 70.56% | 17.90% |
| Foreign currency | 5.49% | 65.48% | 29.44% | 82.10% |
| Fixed rate | 94.33% | 100.00% | 100.00% | 94.63% |
| Floating rate | 5.67% | 0.00% | 0.00% | 5.37% |

**Worked example:** Bookscape (private book retailer, Damodaran case). Its only debt is capitalized operating leases with a debt value of $12.136m. Equity is not traded, so it is estimated from comparables: Net Income $1.575m × average PE of publicly traded book retailers (20) = $31.5m. Debt to capital = 12.136 / (12.136 + 31.5) = 27.81%. Facebook (capstru.xlsx, Jan 2019) is the opposite case: book debt $0, lease commitments 277/284/272/256/220 with a $1,131 lump; at kd = 3.216% the lease debt is $2,088.2m, so D/(D+E) = 2,088.2 / (2,088.2 + 552,102) = 0.38% — essentially an all-equity firm once you look past the leases.

**Determinism:**
- DETERMINISTIC: given debt value, cash, equity value → debt-to-capital and net-debt-to-capital ratios; given a lease commitment schedule and kd → lease debt, restated EBIT/interest/depreciation; given interest expense, book debt, maturity and kd → market value of debt.
- JUDGMENT: classifying hybrids (convertible debt, preferred, trust preferred) as debt or equity; deciding which off-balance-sheet commitments are debt-like; choosing the discount rate for lease capitalization when the firm is unrated; estimating equity value for a private firm.

**Pitfalls:**
- Treating "debt is cheaper than equity" as a value argument. The lower rate compensates for first claim + fixed payment; the risk moves to equity, it does not disappear.
- Using the dividend yield as the cost of equity (an Asian business magazine argued equity was cheaper than debt on exactly this basis). Equity holders expect dividends *plus* price appreciation and bear residual risk; for the same firm the cost of equity must exceed the cost of debt, always.
- Ignoring leases and other fixed commitments, which understates debt and distorts every downstream ratio.
- Mixing book equity with market debt (or vice versa) in one ratio.

**Sources:**
- corporate_finance--lecture_slides--cfpacket2spr20 p.4
- corporate_finance--lecture_slides--cfpacket2spr20 p.7
- corporate_finance--lecture_slides--cfpacket2spr20 p.10
- corporate_finance--lecture_slides--cfpacket2spr20 p.12
- corporate_finance--lecture_slides--cfpacket2spr20 p.39
- corpfin-capital-structure — capstru.xlsx, sheets `Inputs` / `Operating leases` / `Optimal Capital Structure` (lease capitalization, MV-of-debt estimation, current debt ratio)

**Related:** [[debt-equity-tradeoff]], [[financing-life-cycle]], [[cost-of-capital-approach]], [[optimal-debt-ratio-by-firm-type]], [[debt-design-framework]], [[operating-lease-adjustment]]
