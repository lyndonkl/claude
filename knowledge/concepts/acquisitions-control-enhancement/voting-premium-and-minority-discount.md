# Voting premiums and minority discounts

**Core idea:** When control has value, that value does not spread evenly across every share. It attaches to whoever can exercise it. Two settings make this visible. In a public firm with voting and non-voting classes, the expected value of control accrues to the voting shares, so they trade at a premium. In a private firm, a controlling stake can change how the business is run and is therefore priced off the optimal value, while a minority stake is stuck with the status quo. That asymmetry is the minority discount. A 2% difference in ownership can produce a large difference in value per point, because one stake carries control and the other does not.

**Formulas:**

Single share class:
- `Value per share = [Status Quo Value + P × (Optimal Value − Status Quo Value)] / N`, where `P` = probability of control changing and `N` = shares outstanding.

Two classes, extreme case where non-voting shares are completely unprotected:
- `Value per non-voting share = Status Quo Value / (V + NV)`, where `V` = number of voting shares and `NV` = number of non-voting shares.
- `Value per voting share = Value per non-voting share + [P × (Optimal Value − Status Quo Value)] / V`.
- `Voting premium % = (Value per voting share − Value per non-voting share) / Value per non-voting share`.

Private-company stakes:
- `Value of a controlling stake = Ownership % × Optimal Value` (stake > 50%).
- `Value of a minority stake = Ownership % × Status Quo Value` (stake < 50%).
- `Minority discount = 1 − (Status Quo Value / Optimal Value)` per unit of ownership.

**Procedure:**
1. Compute the status-quo value and the optimal value of the equity. Both are full DCFs.
2. Estimate `P`, the probability of control changing. In a two-class structure with entrenched voting control, `P` is usually low.
3. For share classes: count the voting and non-voting shares. Assign the status-quo value across *all* shares equally — every share owns the same cash flows. Assign the expected control value only to the voting shares.
4. Compute the two per-share values and the implied voting premium.
5. Check the structure. The formulas above assume non-voting shares are completely unprotected. Where charters, laws or tag-along rights protect the non-voting class, some control value leaks back to them, and the premium is smaller.
6. For private-company stakes: decide whether the stake conveys control. Above 50% it does; below 50% it does not.
7. Apply the ownership percentage to the optimal value for a controlling stake, and to the status-quo value for a minority stake.
8. Note that the discount widens as the gap between optimal and status-quo value widens. A badly run private firm has a large minority discount; a well-run one has almost none.

**Reference data:**

Embraer (Brazilian aerospace, common voting and preferred non-voting shares), R$ millions:

| Input | Value |
|---|---|
| Status quo equity value | 12,500 |
| Optimal equity value | 14,700 |
| Voting shares | 242.5 million |
| Non-voting shares | 476.7 million |
| Probability of management change | 20% |

| Output | Value |
|---|---|
| Value per non-voting share | R$17.38 |
| Value per voting share | R$19.19 |
| Voting premium | 10.4% |

Kristin Kandy (private candy business), $:

| Input | Value |
|---|---|
| Equity value with existing management (status quo) | $1.6 million |
| Equity value with new, more creative management (optimal) | $2.0 million |

| Stake | Calculation | Value |
|---|---|---|
| 51% (controlling) | 0.51 × $2.0M | $1,020,000 |
| 49% (minority) | 0.49 × $1.6M | $784,000 |

**Worked example — Embraer.** Every share, voting or not, owns the same cash flows under current management. So the status-quo value is spread across all 719.2 million shares: `12,500 / (242.5 + 476.7) = R$17.38 per share`. That is the value of a non-voting share.

The expected value of control is `0.20 × (14,700 − 12,500) = R$440 million`. It attaches only to the 242.5 million voting shares, adding `440 / 242.5 = R$1.81` each. So a voting share is worth `17.38 + 1.81 = R$19.19`, a **10.4% premium**.

The premium is modest because the probability is only 20%. Raise `P` to 50% and the control value per voting share rises to `0.50 × 2,200 / 242.5 = R$4.54`, a 26% premium. The voting premium is a direct read on how likely the market thinks change is.

**Worked example — Kristin Kandy.** A 51% stake is worth `0.51 × $2.0M = $1.02M`, because control lets the buyer implement the improvements. A 49% stake is worth `0.49 × $1.6M = $784,000`, because a minority holder cannot change how the firm is run. Two percentage points of ownership are worth $236,000 — far more than 2% of any value in the problem. The premium is for control, not for the extra shares.

**Determinism:**
- DETERMINISTIC: all per-share values, the voting premium and the stake values, given status-quo value, optimal value, `P` and the share counts. A script computes them directly.
- JUDGMENT: `P` itself; the two equity values; and whether the non-voting class is genuinely unprotected. Charter provisions, tag-along rights and local law determine how much control value leaks to non-voting shares, and that requires reading the documents.

**Pitfalls:**
- Assigning the status-quo value only to voting shares. Both classes own the same cash flows; only the control increment is split.
- Applying the extreme-case formula where non-voting shareholders have real protections. It overstates the premium.
- Using an observed voting premium to *infer* value without checking liquidity. Non-voting classes often trade thinner, and part of the spread is a liquidity effect, not a control effect.
- Applying a standard percentage minority discount. The discount is derived from the specific gap between optimal and status-quo value, not looked up.
- Pricing a 50/50 private stake as controlling. Below a control threshold, the status-quo value applies.
- Forgetting that a well-run private firm has almost no minority discount, because the two values coincide.

**Sources:**
- `valuations--lecture_notes--spring_2021--valpacket3spr21 p.151-153`
- `valuations--lecture_notes--spring_2020--valpacket3spr20 p.151-153`

**Related:** [[expected-value-of-control]], [[implied-probability-of-management-change]], [[restructured-value-and-value-of-control]], [[status-quo-valuation]], [[private-company-valuation]], [[illiquidity-discount]]
