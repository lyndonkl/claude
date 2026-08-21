# Reconciling firm (FCFF) and equity (FCFE) valuations

**Core idea:** Discounting FCFF at the cost of capital and subtracting debt must give the same equity value as discounting FCFE at the cost of equity. The identity is not automatic. It holds only if the model treats leverage the way the WACC assumes. Debt in every year equals the target debt ratio times **that year's firm value**. Interest accrues on beginning-of-year debt. New debt issued equals the change in the debt balance. Build the debt schedule that way and the two routes agree exactly. Build it any other way — fixed dollar debt, book-value debt, a debt ratio applied to book capital — and they diverge. The reconciliation is therefore a diagnostic: a mismatch tells you your financing assumptions and your discount rate disagree.

**Formulas:**
- Reinvestment consistency in each phase: `Reinvestment Rate = g / ROC`; `Reinvestment_t = EBIT(1−t)_t × RR_t`.
- `FCFF_t = EBIT(1−t)_t × (1 − RR_t)`.
- `WACC = (1 − DR) × k_e + DR × k_d(1 − t)`, DR = market-value debt ratio.
- `Firm value roll-forward: V_t = V_{t−1}(1 + WACC) − FCFF_t`.
- `Debt_t = DR × V_t`; `Interest_t = k_d,pre-tax × Debt_{t−1}`; `New Debt Issued_t = Debt_t − Debt_{t−1}`.
- `Net Income_t = (EBIT_t − Interest_t)(1 − t)`.
- `FCFE_t = Net Income_t − Reinvestment_t + New Debt Issued_t`.
- Terminal values: `TV^firm_n = FCFF_{n+1}/(WACC − g)`; `TV^equity_n = TV^firm_n − Debt_n = FCFE_{n+1}/(k_e − g)`.
- Identity: `Σ FCFF_t/(1+WACC)^t + PV(TV^firm) − Debt₀ = Σ FCFE_t/(1+k_e)^t + PV(TV^equity)`.

**Procedure:**
1. Build the FCFF model first. Set the reinvestment rate to `g/ROC` in each phase and compute firm value.
2. Roll the firm value forward year by year with `V_t = V_{t−1}(1+WACC) − FCFF_t`. The final year's rolled value should equal the terminal value.
3. Derive the debt schedule as `Debt_t = DR × V_t`. In the terminal phase, let debt grow at `g_stable`.
4. Compute interest on beginning-of-year debt, then net income, then FCFE using the **same** total reinvestment as the FCFF model.
5. Discount FCFE at the cost of equity, adding a terminal equity value equal to terminal firm value minus terminal debt.
6. Compare the two equity values. They should match exactly. If they do not, check three things in order: is reinvestment identical in both routes; is debt tied to contemporaneous firm value; is interest computed on beginning debt.
7. Note the boundary case: with DR = 0, WACC equals the cost of equity and the two streams coincide trivially.

**Worked example (`fcffvsfcfe.xls`):** EBIT₀ = 100; growth 10% for 5 years, then 5% forever; tax rate 40%; debt ratio 20% at market value; cost of equity 12%; pre-tax cost of debt 7%; ROC 12% in high growth and 10% in stable growth.
- `RR_high = 0.10/0.12 = 83.33%`; `RR_stable = 0.05/0.10 = 50%`.
- `k_d after tax = 7%(0.6) = 4.2%`; `WACC = 0.8(12%) + 0.2(4.2%) = 10.44%`.
- Year 1: EBIT 110; EBIT(1−t) 66; reinvestment 55; FCFF 11.
- Terminal FCFF = 101.462 × 0.5 = 50.731; `TV₅ = 50.731/0.0544 = 932.556`.
- Firm value = **617.006**; equity = 617.006 × 0.8 = **493.605**; debt = 123.401.
- Equity route: Debt₀ = 123.401, so interest in year 1 = 7% × 123.401 = 8.638. Net income = (110 − 8.638)(0.6) = 60.817. New debt issued = 10.683. FCFE = 60.817 − 55 + 10.683 = 16.500.
- Terminal equity value = 932.556 − 186.511 = 746.045, which also equals `52.223/(0.12 − 0.05)`.
- Discounting the FCFE stream at 12% gives **493.605** — identical to the firm route.

**Determinism:**
- DETERMINISTIC: every number above, given the nine inputs. The identity itself is an arithmetic consequence of the construction, so a script can assert it as a unit test.
- JUDGMENT: the target debt ratio, the ROC in each phase, and whether the firm will in fact keep leverage at a constant market-value ratio. Real firms issue debt in lumps and let the ratio drift, which is precisely why [[equity-versus-firm-valuation]] steers changing-leverage firms to the FCFF route.

**Pitfalls:**
- Applying the debt ratio to book capital instead of contemporaneous firm value, then wondering why the routes disagree.
- Charging interest on end-of-year debt.
- Letting reinvestment differ between the two models (for example, using `g/ROC` in the FCFF version and reported cap ex in the FCFE version).
- Violating `WACC > g_stable` or `k_e > g_stable`; the terminal values blow up.
- Reading a small residual difference as rounding. Under this construction the match is exact.

**Sources:**
- reconciliation (fcffvsfcfe.xls)
- valpacket1spr21 p.213
- valpacket1spr20 p.209

**Related:** [[equity-versus-firm-valuation]], [[ddm-fcfe-reconciliation]], [[dcf-model-choice-framework]], [[equity-value-bridge]], [[cost-of-capital]], [[economic-value-added]]
