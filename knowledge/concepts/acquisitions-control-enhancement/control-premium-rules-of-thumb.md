# Control premiums and the rule-of-thumb trap

**Core idea:** Deal practice is full of fixed-percentage premiums. The most common is the "20% control premium," often cited to Mergerstat. Damodaran rejects all of them. Control is worth what you can change, and nothing more. A perfectly run target carries a control premium of zero, no matter what the survey says. The same logic kills premiums for brand name and for quality of management. If the valuation was done properly, those factors already sit inside the estimated value. Adding a premium on top is double counting.

**Formulas:**
- `Value of control = Value of firm run optimally − Value of firm run status quo`.
- Applied to the stylized target: `Value with improved margin = Revenues × new pre-tax operating margin × (1 − t) / k_e`, where `t` = tax rate and `k_e` = the target's cost of equity.
- A perfectly run firm gives `Optimal value = Status quo value`, so `Value of control = 0`.

**Procedure:**
1. Value the target as currently run. This is the status-quo value.
2. List the specific changes you would make. Name each one: raise the operating margin, raise the reinvestment rate, raise the return on capital, move to the optimal debt ratio, return idle cash.
3. Attach a number to each change and rebuild the DCF. This is the optimal (restructured) value.
4. Subtract. The difference is the maximum control premium the deal can support.
5. If you cannot name a single change, the premium is zero. Walk away or pay market price.
6. Never add a survey percentage on top of a value you already computed. Ask instead which of the four value drivers the premium is supposed to represent.
7. Treat any premium "backed by studies" with suspicion. Those studies carry heavy sampling bias and large standard errors, both of which the service selling them tends not to disclose.

**Reference data:** No defensible lookup table exists — that is the point of the concept. The commonly quoted figure is a 20% control premium attributed to Mergerstat. Damodaran's position: it has no valuation content and should not be used.

**Worked example (the stylized target):** Revenues 100, operating expenses 80, EBIT 20, taxes 8, after-tax operating income 12. No debt, no growth, cost of equity 20%. Status-quo value = `12 / 0.20 = 60`.

- Rule-of-thumb answer: pay `60 × 1.20 = 72`. This has no basis.
- Correct answer, case A — you can raise the pre-tax operating margin from 20% to 30%. New EBIT = `100 × 0.30 = 30`. At the same 40% tax rate, after-tax operating income = 18. Optimal value = `18 / 0.20 = 90`. Value of control = `90 − 60 = 30`, which is a 50% premium, not 20%.
- Correct answer, case B — the target is already perfectly run. Optimal value = status-quo value = 60. Value of control = **0**. Any premium is a pure gift to the seller.

**Determinism:**
- DETERMINISTIC: revaluing the firm at a stated new margin, ROC, reinvestment rate or debt ratio; subtracting status quo from optimal to get the control value.
- JUDGMENT: which improvements are actually achievable, by how much, and how long they take. This needs a benchmark comparison against the acquirer and the peer group, plus a concrete operating plan naming who delivers each change.

**Pitfalls:**
- Paying a premium for a well-run firm. Good management is already in the price and in the cash flows.
- Stacking premiums: a control premium, plus a brand premium, plus a management-quality premium, all on top of one DCF. Each is double counting.
- Confusing the *maximum* premium with the premium you should pay. Paying the full control value hands your entire improvement plan to the seller.
- Ignoring the delay. If the changes take three years, discount the value gain for those three years before setting the premium.
- Citing sample-average premiums as evidence. Averages of overpayments are still overpayments.

**Sources:**
- `valuations--lecture_notes--spring_2021--valpacket3spr21 p.96-97`
- `valuations--lecture_notes--spring_2020--valpacket3spr20 p.96-97`

**Related:** [[seven-sins-of-acquisitions]], [[restructured-value-and-value-of-control]], [[expected-value-of-control]], [[transaction-and-exit-multiples]], [[three-reasons-and-acid-test]]
