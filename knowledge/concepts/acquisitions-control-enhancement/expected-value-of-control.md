# The expected value of control

**Core idea:** Knowing that a firm would be worth more under better management is not enough. You also need the odds that the management actually changes. The expected value of control multiplies the two: the probability of change times the value gain from change. That single product explains four things at once. It sets what a hostile acquirer can pay. It explains why market prices sit between status-quo and optimal value. It explains why voting shares trade above non-voting shares. And it explains why minority stakes in private firms sell at a discount. The probability is not fixed. It moves with governance rules, activist activity, and events that remind investors of the power they hold.

**Formulas:**
- `Expected value of control = Probability of management change × (Optimal firm value − Status quo firm value)`.
- Market price identity: `Market value = Status quo value + (Optimal value − Status quo value) × Probability of management changing`.
- Maximum price in a control-motivated hostile bid: `Optimal (restructured) value`. So `Maximum premium per share = Optimal value per share − Current market price per share`.
- If changes take `k` years to implement, the gain must be discounted: `Adjusted control value = (Optimal − Status quo) / (1 + r)^k`, where `r` is the cost of capital or cost of equity as appropriate.

**Procedure:**
1. Compute the status-quo value and the restructured (optimal) value. Their difference is the value gain from change.
2. Estimate the probability that management actually changes. Four structural determinants: takeover restrictions, voting rules and rights, access to funds to mount a challenge, and the size of the company. Large, defended, closely held firms have low probabilities.
3. Refine the probability with the empirical determinants of forced turnover (see reference data), or fit a probit/logit on historical data from firms where change did or did not occur.
4. Multiply. That is the expected value of control embedded in the stock.
5. Adjust for implementation delay. Changes that take three years are worth less than changes that take one.
6. Apply the result to the setting you are in:
   - Hostile acquisition — you can *ensure* change after taking over, so the probability is effectively 1 and you can pay up to the optimal value. But do not pay all of it.
   - Publicly traded share price — solve for the implied probability the market is using.
   - Voting versus non-voting shares — allocate the expected control value to the voting class.
   - Private-company stakes — price a controlling stake off optimal value and a minority stake off status quo.
7. Re-estimate the probability when conditions change: new governance legislation, an activist appearing on the register, a hostile bid elsewhere in the sector.

**Reference data:**

Determinants of the probability of management change (structural):

| Factor | Direction |
|---|---|
| Takeover restrictions (poison pills, staggered boards, legal barriers) | More restrictions → lower probability |
| Voting rules and rights | Concentrated/entrenched voting → lower probability |
| Access to funds to mount a challenge | Easier financing → higher probability |
| Size of the company | Larger → lower probability |

Empirical determinants of forced management turnover (from probit/logit studies):

| Determinant | Higher probability of forced change when |
|---|---|
| Stock price and earnings performance | Firm underperforms peers and expectations |
| Board structure | Board is small, outsider-dominated, and the CEO is not also chairman |
| Ownership structure | High institutional holdings, low insider holdings, dependence on equity markets for new capital |
| Industry structure | Industry is competitive |

Why the probability shifts over time:
1. Corporate governance rules change as laws pass; rules giving stockholders more power raise the likelihood of change.
2. Activist investing ebbs and flows with markets — activists are more visible in down markets and often emerge after scandals.
3. Events such as hostile acquisitions make investors reassess the odds by reminding them of the power they possess.

Four manifestations of the value of control:

| Setting | Where control value shows up |
|---|---|
| Hostile acquisitions | The control premium should equal the value change from replacing management |
| Market prices of public firms | Every price embeds `Status quo + P × (Optimal − Status quo)` |
| Voting vs non-voting shares | The voting premium rises with the expected value of control |
| Minority stakes in private firms | The minority discount rises with the expected value of control |

**Worked example — Blockbuster, July 2005.** Status-quo value is $5.13 per share; the restructured value is $12.47 per share. The value gain from change is `12.47 − 5.13 = $7.34 per share`.

In a hostile acquisition you can guarantee the change once you control the firm, so the probability is 1 and the maximum you can pay is the optimal value of $12.47. The stock traded at $9.50, so the maximum justifiable premium is `12.47 − 9.50 = $2.97 per share`.

Two follow-on questions matter. Should you pay the full $2.97? No — that hands the entire value of your own changes to the seller, leaving you with nothing for the work and the risk. And what if the changes take three years to implement? Then the $7.34 gain arrives three years late and must be discounted, which shrinks the defensible premium well below $2.97.

**Determinism:**
- DETERMINISTIC: the multiplication once probability and the two values exist; the maximum premium as optimal value minus market price; the delay adjustment given `k` and `r`; a fitted probit/logit converting firm characteristics into a probability.
- JUDGMENT: the probability itself, which requires reading governance documents, the shareholder register, board composition, takeover defences and activist presence. Also judgment: the optimal value (a full restructuring case), the implementation timeline, and how much of the premium to concede in negotiation.

**Pitfalls:**
- Treating the probability as 1 outside a hostile takeover. In a minority position you cannot force change.
- Paying the full value of control. The maximum price is not the right price.
- Ignoring the delay. Multi-year turnarounds are worth materially less than the undiscounted gap.
- Assuming the probability is stable. An activist arriving can move it by 20 percentage points overnight.
- Using a fixed control-premium percentage instead of the product of probability and value gain.
- Forgetting that a well-run firm has a zero value gap, which makes the expected value of control zero regardless of the probability.

**Sources:**
- `valuations--lecture_notes--spring_2021--valpacket3spr21 p.145-149`
- `valuations--lecture_notes--spring_2020--valpacket3spr20 p.145-149`

**Related:** [[restructured-value-and-value-of-control]], [[status-quo-valuation]], [[implied-probability-of-management-change]], [[voting-premium-and-minority-discount]], [[control-premium-rules-of-thumb]], [[three-reasons-and-acid-test]], [[corporate-governance]]
