# Minority (lack of control) discount

**Core idea:** Control is worth what you could do with it. A firm has a *status quo* value under incumbent management and an *optimal* value under a manager who runs it to maximize value. The difference is the value of control. Whoever holds a majority stake holds the power to move the firm from status quo to optimal, so a majority stake is priced off the optimal value. A minority holder cannot force that change, so a minority stake is priced off the status quo value. The minority discount is therefore not an arbitrary haircut; it is the fraction of value that control creates. It is distinct from the illiquidity discount, which prices the inability to *exit* rather than the inability to *direct*.

**Formulas:**
- `Value of control = Optimal equity value − Status quo equity value`
- `Minority discount = (Optimal equity value − Status quo equity value) / Optimal equity value`
- `Value of majority stake = Majority % × Optimal equity value`
- `Value of minority stake = Minority % × Status quo equity value`
- Equivalently: `Value of minority stake = Minority % × Optimal equity value × (1 − Minority discount)`
- Symbols: `Optimal equity value` = value with a value-maximizing controller in place; `Status quo equity value` = value under current management and current policies.

**Procedure:**
1. Value the firm **as it is run today**. Current investment, financing and dividend policy, current margins, current returns on capital. That is the status quo value.
2. Value the firm **as it could be run**. Fix the policies a value-maximizing controller would fix: reinvest only above the cost of capital, move to the optimal debt ratio, return excess cash. That is the optimal value.
3. `Minority discount = (Optimal − Status quo) / Optimal`. This is the *maximum* lack-of-control discount.
4. Price the stake being valued:
   - Majority (>50%): `stake % × optimal value`.
   - Minority (<50%): `stake % × status quo value`.
5. Sanity check the sign and the range. **Decision rule: the analysis is meaningful only if the current market or transaction price lies between the status quo value and the optimal value.** If optimal < status quo, the "discount" comes out negative, which says incumbent management beats your hypothetical optimum — treat that as an invalid input, not a finding.
6. Apply the illiquidity discount separately if the stake is also unmarketable. The two frictions are different and both can bind.
7. In practice, weight by the probability that control actually changes. A minority holder in a firm where a control contest is imminent faces a smaller effective discount. The base spreadsheet does not do this.

**Reference data:** No lookup table exists — the discount is computed firm by firm from the two valuations. The spreadsheet's caveat, printed on the sheet: "This analysis will yield meaningful values only if the current price lies between the status quo and the optimal value."

Edge cases to guard:

| Condition | Consequence |
|---|---|
| Optimal equity value ≤ 0 | Discount undefined (division by zero) |
| Optimal < Status quo | Negative discount — flag as invalid inputs |
| Price outside [status quo, optimal] | Model's own caveat: result is not meaningful |

**Worked example** (`minoritydiscount.xls` default case): optimal equity value 14,700; status quo equity value 12,500; majority stake 51%; minority stake 49%.
- `Minority discount = (14,700 − 12,500) / 14,700 = 14.97%`
- `Value of majority stake = 0.51 × 14,700 = 7,497`
- `Value of minority stake = 0.49 × 12,500 = 6,125`

Note: the shipped spreadsheet stores `=B2+(B5*B3)` for the minority stake, giving 20,825 — a value larger than the whole firm. That is a spreadsheet bug. The intended and correct formula is `minority % × status quo value = 6,125`.

**Determinism:**
- DETERMINISTIC: `{optimal equity value, status quo equity value, majority %, minority %} → minority discount, majority stake value, minority stake value`. Pure arithmetic.
- JUDGMENT: both input valuations. The status quo value needs the firm's actual policies and performance. The optimal value needs a specific, defensible account of what a better controller would change and what it would be worth. Also judgment: the probability that control actually changes hands, which the base model ignores.

**Pitfalls:**
- Reaching for a conventional "minority discount" percentage. The number is supposed to fall out of two valuations, not out of a convention.
- Reproducing the spreadsheet's stored minority-stake formula. It is wrong; use `minority % × status quo value`.
- Assuming a large gap between optimal and status quo is automatically capturable. If no mechanism exists to change management, the optimal value is theoretical and the minority discount is effectively 100% of a gap nobody will close.
- Confusing this with the illiquidity discount. Control and marketability are separate frictions.
- Stacking a full minority discount on top of a full illiquidity discount without asking whether that double-counts.
- Ignoring the probability of a control change, which is the realistic refinement the base model omits.

**Sources:**
- special-private.md — minoritydiscount.xls, Sheet1
- valuations--lecture_notes--spring_2021--valpacket2spr21 p.127 (motive: valuing one partner's interest for sale to another), p.153
- valuations--lecture_notes--spring_2020--valpacket2spr20 p.125, p.151

**Related:** [[illiquidity-discount]], [[private-company-valuation-framework]], [[private-to-private-valuation]], [[value-of-control]], [[optimal-capital-structure]], [[corporate-governance]]
