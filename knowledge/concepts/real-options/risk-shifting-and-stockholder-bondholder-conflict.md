# Risk shifting and the stockholder-bondholder conflict

**Core idea:** If equity is a call option on the firm, then equity holders are long volatility. Raising the variance of firm value raises the value of their call — even if the action that raises variance destroys firm value. Since firm value is fixed at the moment of the action, any gain to equity must come out of debtholders' pockets. This is the risk-shifting (asset-substitution) conflict, and the option model makes it quantitative rather than rhetorical. It explains why bond covenants exist, why lenders to volatile businesses demand high rates, and why distressed managers gamble.

**Formulas:**
- Equity value before and after the action: `E = S x N(d1) - K x e^(-r*t) x N(d2)`, recomputed with the new `S` and new `sigma^2`.
- Post-action firm value: `S_new = S_old + NPV of the project` (negative NPV lowers `S`).
- Post-action variance: `sigma^2_new` = the new variance in firm value.
- Debt value is the residual: `D = S - E`. Debtholders bear whatever equity does not.
- Wealth transfer: `Transfer to stockholders = E_new - E_old`, funded by `D_old - D_new`.
- Stockholders take the project whenever `E_new > E_old`, which can hold even when `NPV < 0`.

**Procedure:**
1. Value the firm's equity and debt as options before the action, using [[equity-as-call-option]].
2. Model the action's two effects separately. First, its NPV changes firm value `S`. Second, its risk changes the variance of firm value `sigma^2`.
3. Recompute the equity call with both new inputs.
4. Compute the new debt value as the residual `S_new - E_new`.
5. Compare. If equity value rises, stockholders rationally take the project regardless of its NPV. Compute the transfer from debtholders.
6. Draw the governance implication. A manager acting purely in stockholders' interests will accept some negative-NPV, risk-increasing projects. Lenders anticipate this and price it, or contract against it with covenants.
7. Apply the same logic in reverse for risk-*reducing* actions: they transfer wealth from stockholders to bondholders. See [[conglomerate-merger-wealth-transfer]].

**Reference data:**

Direction of wealth transfer under the option model:

| Action | Effect on firm value | Effect on variance | Stockholders | Bondholders |
|---|---|---|---|---|
| Risky negative-NPV project | Down | Up | Can gain | Lose |
| Risk-reducing diversifying merger (no releveraging) | Neutral | Down | Lose | Gain |
| Increase in leverage | Neutral or up | Up on remaining debt | Gain | Lose |
| Cash payout to shareholders | Down | Neutral or up | Can gain | Lose |

**Worked example:** The negative-NPV, risk-increasing project.

*Before.* Firm asset value $100 million; 10-year zero-coupon debt with face value $80 million; standard deviation 40% (`sigma^2` = 0.16); riskless rate 10%. From [[equity-as-call-option]]: Equity = $75.94 million, Debt = $24.06 million, Firm = $100 million.

*The proposal.* Stockholders can take a project with an NPV of **-$2 million** that is very risky and would push the standard deviation of firm value up to 50%. As a stockholder, would you invest?

*After.* New inputs: `S` = $100m - $2m = $98 million; `K` = $80 million; `t` = 10 years; `sigma^2` = 0.25; `r` = 10%.

| Item | Before | After | Change |
|---|---|---|---|
| Value of Equity | $75.94m | $77.71m | **+$1.77m** |
| Value of Debt | $24.06m | $20.29m | **-$3.77m** |
| Value of Firm | $100.00m | $98.00m | -$2.00m |

Equity value **rises** by $1.77 million even though the firm loses $2 million. The gain comes entirely at bondholders' expense: their claim falls by about $3.8 million. Stockholders answer yes. The firm is worse off.

(Note: the packet's narrative text quotes the post-project bondholder value as $20.19 million while the itemized table shows $20.29 million. Use $20.29 million, which is consistent with the $98 million firm value and $77.71 million equity.)

**Determinism:** **DETERMINISTIC**: the before-and-after option values. Given `(S, K, t, sigma, r)` in each state, a script returns $75.94m/$24.06m before and $77.71m/$20.29m after, plus the changes and the implied transfer. The rule "take it if `E_new > E_old`" is a mechanical comparison. **JUDGMENT**: the two inputs that drive the whole result — the project's NPV of -$2 million and the claim that it lifts firm-value standard deviation from 40% to 50%. Both are forecasts. Also judgment: whether managers actually behave this way, whether covenants block the action, and whether the reputational cost of expropriating lenders offsets the $1.77 million gain in a repeated-game setting.

**Pitfalls:**
- Assuming stockholders always want positive-NPV projects and reject negative-NPV ones. With levered equity as a call, that is false.
- Attributing the equity gain to value creation. Firm value fell. The gain is a transfer, not creation.
- Ignoring the variance change and modelling only the NPV effect. The variance move from 0.16 to 0.25 is what produces the gain; the NPV effect alone would reduce equity.
- Reading this as a prescription. It is a positive description of an agency conflict, and the reason lenders write covenants and price default risk.
- Forgetting the symmetric case. Actions that lower firm-value variance hurt stockholders and help bondholders.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket3spr21 p.71-73
- valuations--lecture_notes--spring_2020--valpacket3spr20 p.71-73

**Related:** [[equity-as-call-option]], [[distressed-equity-time-value]], [[conglomerate-merger-wealth-transfer]], [[equity-option-inputs-troubled-firms]], [[option-payoffs-and-determinants]], [[agency-costs-of-debt]], [[cost-of-debt]], [[optimal-capital-structure]]
