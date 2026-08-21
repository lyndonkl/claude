# Value and EPS effects of a stock buyback

**Core idea:** A buyback does not create value simply by shrinking the share count. Its effects run through three separate channels, and they must be kept apart. First, **leverage**: funding a buyback with debt raises the debt ratio, relevers the beta, raises the cost of equity, and may lower or raise the cost of capital — the value effect comes from this, not from the repurchase itself. Second, **wealth transfer**: buying back stock below fair value transfers value from selling shareholders to those who stay, and buying above fair value does the reverse. Third, **EPS accretion**: earnings per share almost always rise when the shares bought are funded cheaply, but EPS accretion is not value creation. This concept quantifies all three, following Damodaran's `buybacks.xls` model.

**Formulas:**

*Pre-buyback state:*
- E0 = Price0 × Shares0 (market value of equity)
- D/E0 = Debt / E0; D/C0 = Debt / (Debt + E0)
- ke0 = Rf + β0 × ERP
- kd0(after tax) = kd_existing × (1 − t)
- WACC0 = ke0 × E0/(Debt + E0) + kd0(after tax) × Debt/(Debt + E0)
- EV0 = E0 + Debt − Cash (enterprise value); Firm Value0 = E0 + Debt

*Post-buyback state:*
- Cost = Buyback price × Shares bought back
- E1_mech = E0 − Cost (mechanical equity value after the cash leaves)
- D1 = Debt + New debt raised; Cash1 = Cash − Cash used
- Unlever: β_u = β0 / (1 + (1 − t) × D/E0)
- Relever: β1 = β_u × (1 + (1 − t) × D1/E1_mech)
- ke1 = Rf + β1 × ERP
- kd1(after tax) = **cost of new debt** × (1 − t), applied to all debt post-buyback in the model
- WACC1 = ke1 × E1_mech/(D1 + E1_mech) + kd1(after tax) × D1/(D1 + E1_mech)
- **EV1 = EV0 × (WACC0 − Rf) / (WACC1 − Rf)** — a growing-perpetuity revaluation, with the implicit assumption that cash flows grow forever at g = Rf
- Firm Value1 = EV1 + Cash1; E1_value = Firm Value1 − D1
- Shares1 = Shares0 − Shares bought; **Price1 = E1_value / Shares1**

*Wealth transfer (only when you have a fair-value estimate):*
- Transfer = (Fair value per share − Buyback price) × Shares bought back
- Transfer per remaining share = Transfer / Shares1
- Price with transfer = Price1 + Transfer per remaining share

*EPS and PE effects:*
- NI1 = Net Income − Interest income from cash − New debt × kd_new × (1 − t)
- EPS0 = NI / Shares0; EPS1 = NI1 / Shares1
- PE0 = Price0 / EPS0; PE1 = Price1 / EPS1

Symbols: Rf = risk-free rate; ERP = equity risk premium; t = marginal tax rate; β0 = current levered beta; β_u = unlevered beta; kd = pre-tax cost of debt.

**Procedure:**
1. Gather inputs: current price, shares outstanding, beta, interest-bearing debt (plus market value of preferred), cash and marketable securities, existing pre-tax cost of debt, net income, interest income earned on the cash, risk-free rate, equity risk premium, marginal tax rate.
2. Specify the buyback: expected buyback price, number of shares to be repurchased, how much is funded with existing cash, how much with new debt, and the pre-tax cost of that new debt. Check that cash funding + debt funding equals price × shares — the model does not enforce it, and a mismatch silently corrupts the answer.
3. Compute the pre-buyback block: E0, leverage ratios, ke0, after-tax kd0, WACC0, EV0, firm value.
4. Unlever the beta at the old debt-to-equity ratio and relever at the new one. Recompute ke1 and WACC1.
5. Revalue the enterprise: EV1 = EV0 × (WACC0 − Rf)/(WACC1 − Rf). Guard against WACC1 ≤ Rf, which makes the denominator zero or negative.
6. Rebuild equity value: add remaining cash, subtract total debt, divide by the reduced share count to get the new price per share.
7. If you have an independent fair-value estimate, compute the wealth transfer and add it per remaining share. Decision rule: buy back only when the buyback price is **below** your estimate of fair value; buying back overvalued stock transfers wealth *away* from the continuing shareholders.
8. Compute the EPS and PE effects last, and treat them as diagnostics, not as the case for the buyback. Note the arithmetic: EPS rises whenever the percentage fall in net income is smaller than the percentage fall in share count.

**Reference data — the model's two documented quirks (reproduce for parity, but flag them):**

| Quirk | What the model does | Why it matters |
|---|---|---|
| Cost of new debt applied to all debt | Post-buyback after-tax cost of debt uses the *new* debt rate for the entire debt balance, not a blend of old and new | Overstates (or understates) WACC1 whenever old and new debt rates differ |
| Interest income treatment in the EPS sheet | Subtracts the **full**, **pre-tax** interest income on cash, even when only part of the cash is used to fund the buyback | Understates post-buyback net income; the new-debt interest, by contrast, is correctly after-tax |
| Growth assumption in the EV step | The revaluation implicitly assumes cash flows grow forever at g = Rf | The value effect is entirely driven by the change in (WACC − Rf); a different g changes the answer |

**Worked example (the model's default case):**

Inputs: price $60, 2,000 shares outstanding, beta 1.2, debt $15,961, cash $3,931, existing pre-tax cost of debt 3.75%, net income $4,000, interest income from cash $60, Rf 2.75%, ERP 5%, tax rate 40%. Buyback: 200 shares at $65 (cost $13,000), funded with $3,000 of cash and $10,000 of new debt at 4.25%. Fair value estimate: $75 per share.

Pre-buyback: E0 = 60 × 2,000 = 120,000. D/E0 = 15,961/120,000 = 0.1330. ke0 = 2.75% + 1.2 × 5% = 8.75%. After-tax kd0 = 3.75% × 0.6 = 2.25%. WACC0 = 7.9869%. EV0 = 120,000 + 15,961 − 3,931 = 132,030.

Post-buyback: E1_mech = 120,000 − 13,000 = 107,000. D1 = 15,961 + 10,000 = 25,961. D/E1 = 0.2426. β_u = 1.2 / (1 + 0.6 × 0.1330) = 1.1113; β1 = 1.1113 × (1 + 0.6 × 0.2426) = 1.2731. ke1 = 2.75% + 1.2731 × 5% = 9.1155%. After-tax kd1 = 4.25% × 0.6 = 2.55%. WACC1 = 7.8335%.

Revaluation: EV1 = 132,030 × (0.079869 − 0.0275)/(0.078335 − 0.0275) = **136,014.2**. Cash1 = 931. Firm value1 = 136,945.2. E1_value = 136,945.2 − 25,961 = **110,984.2**. Shares1 = 1,800. **Price1 = 110,984.2 / 1,800 = $61.66** (+2.76%), even though total equity value fell 7.51%.

Wealth transfer: (75 − 65) × 200 = **$2,000**, or 2,000/1,800 = **$1.11 per remaining share**, giving a price with transfer of **$62.77**.

EPS effect: NI1 = 4,000 − 60 − 10,000 × 0.0425 × 0.6 = **$3,685**. EPS0 = 4,000/2,000 = $2.00; EPS1 = 3,685/1,800 = **$2.047** (+2.36%). PE0 = 30.0; PE1 = 61.66/2.047 = **30.12** (+0.39%). Net income fell 7.9% while shares fell 10%, which is the whole source of the accretion.

**Determinism:**
- DETERMINISTIC: every line above. Given the ~18 numeric inputs, a script produces the full pre/post table, the per-share price, the wealth transfer and the EPS/PE effects.
- JUDGMENT: the fair-value estimate per share, which drives the entire wealth-transfer block and is the only genuinely valuation-dependent input. Whether the new leverage is sustainable and whether the relevered beta and the new cost of debt are right. Whether the perpetual-growth-at-Rf assumption embedded in the EV revaluation is acceptable for this firm.

**Pitfalls:**
- Claiming a buyback creates value because EPS rose. EPS accretion follows mechanically whenever the after-tax cost of the funding is below the earnings yield; it says nothing about value.
- Claiming a buyback creates value because the share count fell. In this example equity value fell 7.51%; price per share rose only because the count fell faster and because leverage lowered WACC.
- Buying back overvalued stock. The transfer term flips sign and the continuing shareholders lose.
- Letting cash funding exceed the cash balance, or letting cash + debt funding differ from the buyback cost. The model checks neither.
- Buying back all or nearly all shares. The per-share math breaks down.
- Forgetting the guard on WACC1 ≤ Rf, which blows up the enterprise value revaluation.
- Treating buybacks and dividends as interchangeable in a levered firm. A debt-funded buyback also transfers wealth from lenders (see [[dividend-wealth-transfer]]).

**Sources:**
- corpfin-payout-projects — buybacks.xls, sheets `Value Effect` (inputs B6–B27; outputs C31–C42, B45–B51) and `EPS Effect` (rows 20–25)
- corporate_finance--lecture_slides--cfpacket2spr20 p.156-157
- corporate_finance--lecture_slides--cfpacket2spr20 p.175

**Related:** [[cash-returned-dividends-and-buybacks]], [[bad-reasons-for-paying-dividends]], [[dividend-wealth-transfer]], [[fcfe-potential-dividends]], [[payout-forecasting]], [[cost-of-capital]], [[bottom-up-beta]]
