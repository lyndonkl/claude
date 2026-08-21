# Discount-rate discipline in acquisitions (risk transference and debt subsidies)

**Core idea:** The two most common — and most mechanical — ways to overpay for a target are to discount the target's cash flows at the acquirer's cost of equity (risk transference) and to build the acquirer's cheap, plentiful debt into the target's cost of capital (the debt subsidy). Both are errors of the same kind: the discount rate must reflect the risk and the financing capacity of the *investment*, not of the *investor*. A risky business does not become safe because a safe buyer owns it, and a target's own borrowing capacity does not expand because the acquirer's balance sheet is strong. Making either substitution mechanically raises the price you can "justify" and transfers wealth from your own shareholders to the target's.

**Formulas:**
- No-growth, all-equity target value: `V = EBIT(1−t) / k_e`, where `EBIT(1−t)` = after-tax operating income assumed perpetual and flat, `k_e` = **the target's** cost of equity.
- Correct cost of capital for a target: `WACC_target = k_e,target × E/(D+E) |_target + k_d,target × (1−t) × D/(D+E) |_target`, where every input — levered beta, pre-tax cost of debt, and debt ratio — is estimated for the target's own business and its own debt capacity.
- Wealth transferred by a debt subsidy: `Transfer = V(target discounted at acquirer's WACC) − V(target discounted at target's WACC)` — this is exactly the amount handed to the seller for the buyer's own financing strength.

**Procedure:**
1. Estimate the target's cost of equity bottom-up: unlevered beta of the target's *businesses*, relevered at the *target's* debt-to-equity ratio, plus a risk-free rate and an equity risk premium reflecting the target's geographic revenue mix.
2. Estimate the target's cost of debt from the target's own default risk — its own rating or a synthetic rating from its own interest coverage ratio — not from the acquirer's rating.
3. Estimate the target's debt capacity as a stand-alone business. The acquirer's ability to borrow more is a property of the acquirer.
4. Build `WACC_target` from steps 1–3 and discount the target's expected cash flows with it. This is the status-quo value.
5. If the acquirer genuinely brings added debt capacity to the *combined* business, treat that as a **financial synergy** and value it separately in the synergy step — do not smuggle it into the target's own discount rate.
6. Sanity check: if lowering the discount rate is what makes the deal work, the deal does not work.

**Reference data:** No lookup table. The diagnostic thresholds are relational: the discount rate applied to the target must equal the target's stand-alone cost of capital; the debt ratio in that WACC must equal the target's own optimal or actual debt ratio.

**Worked example (Damodaran's stylized target, the same firm used for all seven tests):**

| Line | Value |
|---|---|
| Revenues | 100 |
| Operating expenses | 80 |
| Operating income (EBIT) | 20 |
| Taxes | 8 |
| After-tax operating income | 12 |

Assumptions: this operating income continues forever with no growth; the firm has no debt; the target's cost of equity is 20%.

- Correct value: `12 / 0.20 = 60`.
- Risk-transference error: the acquirer is in a much safer business with a 10% cost of equity, so it discounts at 10% and gets `12 / 0.10 = 120` — double the true value. The correct answer remains **60**, because the cash flows carry the target's risk regardless of who owns them.
- Debt-subsidy error: the acquirer can borrow at 4% and plans to fund half the purchase with debt, so it blends 4% debt into the discount rate and pays still more. Correct treatment: the target has no debt capacity of its own in this example, so its cost of capital is its 20% cost of equity and its value is still **60**. Any excess paid is a transfer from the acquirer's shareholders to the target's.

**Determinism:**
- DETERMINISTIC: given after-tax operating income, growth and a discount rate, the value is arithmetic (`V = CF/(r−g)`); given beta, risk-free rate, ERP, debt ratio, pre-tax cost of debt and tax rate, `WACC` is arithmetic. A script can also compute the wealth-transfer amount from the two WACCs.
- JUDGMENT: which unlevered beta (i.e., which business mix) describes the target; what debt capacity the target could carry stand-alone; what equity risk premium fits its revenue geography; whether the acquirer's incremental debt capacity is a genuine combined-firm synergy or a fiction.

**Pitfalls:**
- Using a single corporate hurdle rate across all acquisitions — the classic institutional form of risk transference.
- Justifying the acquirer's rate on the grounds that "we are the ones raising the money." The money's cost is set by where it is invested.
- Treating cheap acquisition financing as value creation. Financing terms are a transfer, not a source of operating value; only genuine added debt capacity in the combined firm counts, and it belongs in the synergy bucket.
- Double counting: adding a financial-synergy value for added debt capacity *and* using the lower blended cost of capital in the target's own valuation.

**Sources:**
- `valuations--lecture_notes--spring_2021--valpacket3spr21 p.91-95`
- `valuations--lecture_notes--spring_2020--valpacket3spr20 p.91-95`

**Related:** [[seven-sins-of-acquisitions]], [[synergy-taxonomy]], [[valuing-synergy]], [[status-quo-valuation]], [[bottom-up-beta]], [[synthetic-rating]], [[cost-of-capital]]
