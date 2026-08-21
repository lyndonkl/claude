# Dividends versus FCFE (choosing the equity cash flow)

**Core idea:** If you have decided to value equity directly, you still must pick the cash flow. Dividends are what the firm actually paid. FCFE is what it *could have* paid. The two diverge when management hoards cash or borrows to fund payouts. A dividend discount model then values only the cash you receive as a shareholder, ignoring the cash piling up inside the firm. An FCFE model values the whole equity claim. Damodaran resolves the choice with a numeric screen over a five-year window, plus two exceptions: banks (where FCFE is nearly impossible to estimate) and firms with no dividend history at all.

**Formulas:**
- `FCFE = Net Income − (CapEx − Depreciation) − ΔNon-cash Working Capital + (New Debt Issued − Debt Repaid)`.
- Debt-ratio short form: `FCFE = Net Income − (1 − δ)(CapEx − Depreciation) − (1 − δ)(ΔWorking Capital)`, δ = fraction of reinvestment financed with debt.
- Payout screen: `Dividend Coverage = Σ_{5 years} (Dividends + Buybacks) / Σ_{5 years} FCFE`.
- Dividend discount value (stable): `P₀ = DPS₁ / (k_e − g)`, with `DPS₁ = DPS₀ × (1 + g)`.
- FCFE value (stable): `P₀ = FCFE₁ / (k_e − g)` where `FCFE₁ = EPS₁ × (1 − Reinvestment Rate)` and, in steady state, `Reinvestment Rate = g / ROE`.
- Stable-period payout implied by fundamentals: `Payout = 1 − g / ROE`.

**Reference data — the decision screen:**

| Dividend Coverage over 5 years | Model to use |
|---|---|
| Dividends < 80% of FCFE | FCFE model (cash is accumulating inside the firm) |
| 80% ≤ Dividends ≤ 110% of FCFE | Dividend discount model |
| Dividends > 110% of FCFE | FCFE model (payout is being funded from debt or cash reserves) |

Exceptions that override the screen:
- Banks and other financial service firms: use dividends. CapEx, depreciation and working capital have no clean meaning for them, so FCFE cannot be estimated reliably.
- Private companies and IPOs: no dividend history exists, so use FCFE.
- Add buybacks to dividends before running the screen. Firms increasingly return cash by repurchase rather than dividend.

**Procedure:**
1. Pull five years of dividends and of stock buybacks; sum them.
2. Compute FCFE for each of those five years from net income, net cap ex, working-capital change, and net debt issuance; sum.
3. Take the ratio. Apply the 80%/110% thresholds above.
4. Check the exceptions. Financial service firm → dividends regardless of the ratio. No dividend record → FCFE.
5. If you use the DDM but the firm's dividends fall well short of FCFE, expect your value to sit below the FCFE value; quantify the gap with [[ddm-fcfe-reconciliation]] before concluding the stock is overvalued.
6. Whichever measure you use, tie the terminal-period payout or reinvestment rate to fundamentals: `payout = 1 − g/ROE`, never a number carried over from the high-growth phase.

**Worked example (Con Ed, August 2008):** Con Ed paid out roughly **97%** of FCFE as dividends over the previous five years. That sits inside the 80%–110% band, so a dividend discount model is appropriate. Damodaran adds two supporting tests. Test 1: the payout ratio is 73% (EPS $3.17, DPS $2.32 for the trailing 12 months through June 2008) — high payout is what a stable firm looks like. Test 2: retention 27% × ROE 7.7% = 2.1% expected growth, consistent with the g used. Test 3: beta 0.80 lies at the low end of the 0.8–1.2 stable-company range. Value = `2.32(1.021)/(0.077 − 0.021)` = $42.30.

**Contrast (the focussed spreadsheets):** the stable DDM (`ddmst`) values a share at `DPS₀(1+g)/(k_e − g)` — with EPS₀ 4.33, payout 63%, k_e 12.225%, g 6%, the value is 46.45. The stable FCFE model (`fcfest`) instead sets the reinvestment rate from fundamentals: with EPS 5.45, ROE 12% and g 6%, `RR = 0.06/0.12 = 0.5`, so FCFE = 2.725 and the value is `2.725(1.06)/(0.1305 − 0.06)` = 40.97. Had the same sheet used the reported cap ex, depreciation and working-capital lines instead, FCFE would be 4.85 and the value 72.96 — a reminder that the reinvestment assumption drives the FCFE answer.

**Determinism:**
- DETERMINISTIC: the five-year coverage ratio and its comparison to 80%/110%; FCFE from the accounting line items; both valuation formulas given DPS/FCFE, k_e and g.
- JUDGMENT: whether FCFE is estimable at all (the bank exception), whether the last five years are representative of dividend policy, and the stable-period ROE that sets the terminal payout. That judgment needs the firm's dividend policy statements, buyback history, and regulatory capital rules for financial firms.

**Pitfalls:**
- Running the screen on dividends alone while the firm returns most of its cash through buybacks.
- Using a DDM for a cash-hoarding firm and reading the low value as "overvalued stock" instead of "trapped cash".
- Carrying the current payout ratio into the terminal year, which breaks the `payout = 1 − g/ROE` consistency.
- Applying FCFE to a bank by treating loans as working capital.

**Sources:**
- valpacket1spr21 p.214
- valpacket1spr20 p.210
- valpacket1spr21 p.279 (Con Ed: "why dividends" — 97% of FCFE)
- valpacket1spr20 p.275 (Con Ed tests)
- focussed-ddm (ddmst worked example)
- focussed-fcfe (fcfest worked example)

**Related:** [[dcf-model-choice-framework]], [[equity-versus-firm-valuation]], [[ddm-fcfe-reconciliation]], [[growth-pattern-and-stage-count]], [[fundamental-growth-rate]], [[valuing-financial-service-firms]]
