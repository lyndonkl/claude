# Project options: delay, expand, abandon

**Core idea:** Static NPV analysis asks one question — is this project good if taken today, run as planned, to the end? That framing misses the flexibility embedded in real investments. Three options recur. The **option to delay** exists when the firm holds exclusive rights for a period; a project that is bad today may become good before the rights expire. The **option to expand** exists when taking a project today opens the door to other projects later. The **option to abandon** exists when the firm can walk away if cash flows disappoint, truncating the downside. All three add value. Each can turn a project that looks bad under traditional analysis into a good one. A negative traditional NPV is therefore not by itself sufficient grounds for rejection when significant options are embedded.

**Formulas:** Symbols: `PV(CF)` = present value of expected cash flows on the project.
- Option to delay: a **call option**. Underlying = `PV(CF)` on the product. Exercise price = the initial investment required. Payoff = `max(PV(CF) − Initial investment, 0)`. NPV is positive only to the right of the strike.
- Option to expand: a **call option**. Underlying = PV of cash flows from the expansion. Exercise price = the additional investment needed to expand. The firm will not expand while `PV(expansion CF) < additional investment`.
- Option to abandon: a **put option**. Underlying = `PV(CF)` on the project. The payoff floor sits at the abandonment value, with the kink at the cost of abandonment.
- Decision rule with options: accept if `Traditional NPV + Value of embedded options > 0`.
- Option value rises with the volatility of the underlying business.

**Procedure:**
1. Compute the traditional NPV first. The option value is an addition to it, never a substitute for it.
2. Ask whether the firm holds *exclusive* rights — a patent, licence, lease, or first-mover position with a defined life. Without exclusivity there is no meaningful option to delay, because a competitor will take the project.
3. Identify follow-on investments the project makes possible. Name them; a vague "strategic optionality" claim is the synergy abuse in a different costume.
4. Identify the exit route and its recovery value. An option to abandon is worth nothing if the assets cannot be sold or redeployed.
5. Map each option to its payoff structure: delay and expand are calls, abandon is a put.
6. Weigh option value against the cost of acquiring the rights — purchase price, R&D spending, development cost.
7. If the option value is what carries the decision, state that explicitly and state what has to change for the option to be exercised.

**Reference data:** Payoff structure summary:

| Option | Type | Underlying | Exercise price | Value driver |
|---|---|---|---|---|
| Delay (exclusive rights) | Call | PV of expected cash flows on the product | Initial investment in the project | Volatility of the underlying business; length of exclusivity |
| Expand / take other projects | Call | PV of cash flows from the expansion | Additional investment to expand | Size and probability of the follow-on opportunity |
| Abandon | Put | PV of expected cash flows on the project | Abandonment/salvage value net of cost of abandonment | Downside volatility; liquidity of the assets |

Three insights from viewing exclusive rights as an option:
1. Exclusive rights to a product or project are valuable even when the project is not viable today.
2. The value of those rights rises with the volatility of the underlying business, as with any option.
3. The rights cost money to acquire — by purchase or by R&D — and that cost must be weighed against the option's value.

**Worked example:** Disney California Adventure, 2008 — an abandonment/expansion option evaluated with real numbers. Disney opened DCA in 2001 for $1.5 billion, expecting 60% of Disneyland's visitors to cross over and roughly $100 million a year in after-tax cash flow. By 2007, only 6 million of Disneyland's 15 million visitors came, and cash flow averaged $50 million a year. In early 2008 Disney held three live options.

- *Abandon:* shut DCA down and recover an estimated **$500 million** of the original investment.
- *Continue:* accept that future cash flows resemble the actual $50 million, growing at 2% inflation, discounted at the 2008 theme-park cost of capital of 6.62%. Value = 50 × 1.02 / (0.0662 − 0.02) = **$1,103 million**.
- *Expand:* spend about $600 million to add family attractions, raising the Disneyland cross-over share from 40% to 60% and annual after-tax cash flow from $50 million to $80 million. The incremental $30 million perpetuity is worth 30 × 1.02 / (0.0662 − 0.02) = **$662 million** against a $600 million cost, so expansion adds about **$62 million**.

Verdict: continuing beats abandoning ($1,103M > $500M), and expanding adds value on top. Note that the $1.5 billion spent in 2001 plays no role in any of the three calculations — it is sunk.

**Determinism:** JUDGMENT for the most part. Identifying which options genuinely exist, whether exclusivity is real, and what the follow-on opportunity looks like all require reasoning about competition, technology, and contracts. That judgment needs the terms of any patent or licence, the resale market for the assets, and the volatility of the underlying business. DETERMINISTIC — once the option's inputs are estimated (underlying value, exercise price, volatility, time to expiration), option-pricing math is mechanical, as are the growing-perpetuity comparisons in the DCA example.

**Pitfalls:**
- Using "embedded options" the way managers use "synergy": an unquantified justification for a negative-NPV project.
- Claiming an option to delay without exclusive rights. If competitors can act, waiting destroys value rather than creating it.
- Ignoring the cost of acquiring or maintaining the rights. R&D and licence fees are real cash outflows.
- Valuing an abandonment option at book value when the assets have no market. DCA recovers only $500 million of a $1.5 billion investment.
- Double counting: putting optimistic expansion cash flows into the base-case NPV *and* adding an expansion option value on top.
- Forgetting that option value rises with volatility, which means the noisiest businesses carry the largest option values — and the least reliable base cases.

**Sources:**
- corporate_finance--lecture_slides--cfpacket1spr20 p.305
- corporate_finance--lecture_slides--cfpacket1spr20 p.321-325
- corporate_finance--lecture_slides--cfpacket1spr20 p.330-331
- corporate_finance--case--netflixfitpresentation p.22

**Related:** [[assessing-existing-investments]], [[uncertainty-payback-sensitivity-simulation]], [[npv-and-irr-mechanics]], [[project-synergies]], [[incremental-cash-flow-principle]], [[terminal-value-and-project-life]], [[real-options-valuation]]
