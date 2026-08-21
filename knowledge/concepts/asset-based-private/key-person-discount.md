# Key person discount

**Core idea:** In many private businesses the owner *is* part of the product. Revenues and operating profit reflect the current owner's presence — the chef's reputation, the surgeon's patient list, the consultant's relationships — and not just the business's own potential. A buyer who acquires the business without the person does not acquire those cash flows. So the correct treatment is not a discount on the final value but a haircut on the **operating income** the business will generate after the key person leaves. That flows through the whole valuation: cash flows, reinvestment, and terminal value all shrink together.

**Formulas:**
- `Operating income after key-person departure = Adjusted operating income × (1 − k)`, where `k` = the fraction of revenues or profit attributable to the key person's presence.
- Equivalent value-level statement: `Key person discount = Value of business with the key person − Value of business without the key person`.
- Note the ordering: `k` is applied *after* the statement cleanup that charges a market salary for the owner's labour. The two adjustments are different. The salary adjustment prices the owner's *work*; the key-person haircut prices the owner's *pull*.

**Procedure:**
1. Complete the statement cleanup first, including a market salary for whoever will do the owner's job. See [[private-company-statement-cleanup]].
2. Ask what share of the business walks out with the owner. Evidence to look for: what fraction of customers were personally referred or would follow the owner; the concentration of relationships; whether the reputation is attached to the person or to the establishment; how transferable the skill is.
3. Set `k`. Damodaran uses 20% for the restaurant, on the reasoning that roughly 20% of patrons come for the chef's reputation.
4. Apply `k` to adjusted operating income, not to the final equity value.
5. Value the business off the reduced operating income.
6. Ask what the seller can do to mitigate the loss. Transition arrangements, a non-compete, an earn-out, a period of continued employment, or explicit transfer of relationships all shrink `k` and are worth real money to the seller.
7. Note the buyer-side implication: a buyer who "thinks highly of the seller personally" will impose a larger `k`. From the seller's side, the ideal buyer is one who does not attribute much of the business to you.

**Reference data:** No lookup table exists — `k` is estimated case by case. The packet's benchmarks:

| Business | Key person | k used | Basis |
|---|---|---|---|
| Upscale French restaurant | Owner/chef | 20% | Share of patrons drawn by the chef's reputation |

Screening questions for setting `k`: Is the business named after the person? Do customers ask for the person by name? What share of revenue comes from relationships the owner personally holds? Is there a second-tier team the customers already know?

**Worked example:** The restaurant. Adjusted operating income after paying a $150,000 market chef salary is **$370,000**. If 20% of patrons come because of the current owner/chef's reputation, then expected operating income after his departure is `370,000 × (1 − 0.20) = $296,000`. The valuation runs off $296,000, not $370,000. With a 2% growth rate, a 10% reinvestment rate, a 40% tax rate and a 13.25% cost of capital, that produces a business value of `296,000 × 1.02 × 0.60 × 0.90 / (0.1325 − 0.02) = $1,449,220`. Valuing off $370,000 instead would have given roughly $1.81 million — a $360,000 overstatement of firm value from ignoring `k`.

**Determinism:**
- DETERMINISTIC: `{adjusted operating income, k} → post-departure operating income`, and every downstream valuation step.
- JUDGMENT: `k` itself. Estimating it needs customer-concentration data, an understanding of why customers buy, the transferability of the owner's skill, and knowledge of any transition arrangements in the deal. There is no table to look it up in.

**Pitfalls:**
- Applying the key-person discount to the final value instead of to operating income. Applying it to value alone misses the interaction with reinvestment and growth.
- Double-counting with the owner-salary adjustment. Charging a market chef salary *and* assuming the food gets worse is only correct if the reputation, not the labour, is what leaves.
- Forgetting the discount entirely in owner-operated businesses, which is the single most common private-company valuation error.
- Applying it when the key person is staying, or when the buyer is acquiring the person along with the business.
- Treating `k` as fixed. It is negotiable. Transition terms, non-competes and earn-outs are exactly the tools that shrink it.
- Assuming the discount is symmetric across buyers. A buyer who does not know the seller may assign a much smaller `k` — which is why a seller should look for one.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket2spr21 p.129, p.139, p.152, p.170
- valuations--lecture_notes--spring_2020--valpacket2spr20 p.127, p.137, p.150, p.167

**Related:** [[private-company-statement-cleanup]], [[private-to-private-valuation]], [[private-company-valuation-framework]], [[private-to-public-sale]], [[illiquidity-discount]], [[normalizing-earnings]]
