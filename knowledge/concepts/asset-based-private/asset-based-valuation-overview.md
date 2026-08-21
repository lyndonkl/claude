# Asset-based valuation: what it is and when to use it

**Core idea:** There are three ways to value a business. *Intrinsic* valuation values it from the cash flows you expect it to generate over time. *Relative* valuation values it from how similar businesses are priced. *Asset-based* valuation values the business by valuing its individual assets — tangible or intangible — one at a time and adding them up. Asset-based valuation is not a fourth theory of value; it is a re-packaging of the first two applied at the asset (rather than business) level, driven by a specific motive: liquidation, an accounting fair-value mandate, or a sum-of-the-parts analysis. It works only when the assets can actually be separated from one another, which is the exception rather than the rule in an operating business.

**Formulas:**
- `Asset-based value of business = Σ_i Value(Asset_i) − Σ_j Value(Liability_j)`, where `Value(Asset_i)` is estimated by one of the three mechanics below and the liability deduction converts an asset total into equity value.
- Mechanic 1 — intrinsic: `Value(Asset_i) = Σ_t E(CF_i,t) / (1 + r_i)^t`, where `E(CF_i,t)` = expected cash flow from asset *i* in period *t* and `r_i` = risk-adjusted discount rate for that asset.
- Mechanic 2 — relative/pricing: `Value(Asset_i) = Multiple_transaction × Scalar_i`, where `Multiple_transaction` comes from recent sales of similar assets and `Scalar_i` is the matching earnings, revenue, capacity or book-value measure for asset *i*.
- Mechanic 3 — accounting: `Value(Asset_i) = Book value of asset i` (book value used as a proxy for value).

**Procedure:**
1. Establish the motive, because it determines everything downstream. Exactly three motives justify the approach:
   - **Liquidation** — you intend to sell the assets piecemeal rather than run them as a going concern. Go to [[liquidation-valuation]].
   - **Accounting mission** — US and international standards have moved to "fair value"; the accountant must restate the balance sheet at fair rather than book value. Go to [[fair-value-accounting-fas157]].
   - **Sum of the parts** — value divisions one by one, either as a potential acquirer planning a restructuring or as an investor hunting for a company selling for less than the sum of its parts. Go to [[sum-of-the-parts-framework]].
2. Run the three-part feasibility test before proceeding. Asset-based valuation is easiest when all three hold; the more that fail, the less defensible the result:
   - **Separability.** Are the assets separable? Real-estate portfolios and holding companies of independent businesses pass easily. Interrelated assets fail; brand name cuts across every asset and cannot be carved out.
   - **Traceable cash flows.** Can earnings and cash flows be traced to individual assets? If the business makes money but no individual asset's contribution can be isolated, the intrinsic mechanic is unusable.
   - **Active market.** Is there an active market in similar assets from which you can draw transaction prices? Without one, the relative mechanic is unusable and you are pushed toward book value.
3. Pick the mechanic per asset. If step 2's active-market test passes, price the asset (mechanic 2). If the traceable-cash-flow test passes but no market exists, value it intrinsically (mechanic 1). If neither passes, fall back to book value (mechanic 3) and label it as a proxy, not a value.
4. Aggregate, then subtract debt and other non-equity claims to get equity, if equity is what you need.
5. Compare the asset-based total to the going-concern value from a whole-company DCF or pricing. A large gap is the finding, not a failure — it is either a liquidation premium/discount or a conglomerate discount.

**Reference data:** Motive → mechanic mapping (Damodaran, Spring 2021 packet):

| Motive | Preferred mechanic | Why |
|---|---|---|
| Liquidation | Relative (price the assets); book value as fallback | You are selling, so observed transaction prices are the relevant evidence |
| Accounting fair value (FAS 157) | Relative first, intrinsic only when market prices are inaccessible | The standard defines fair value as an *exit* price |
| Sum of the parts — passive long-term investor | Intrinsic | You are waiting for the market to correct a mistake |
| Sum of the parts — activist / acquirer | Relative | You will sell or spin the pieces at market prices |

**Worked example:** United Technologies (2009) is the packet's canonical separable-asset case: six distinct divisions (Carrier, Pratt & Whitney, Otis, UTC Fire & Security, Hamilton Sundstrand, Sikorsky) with individually reported revenues, EBITDA, operating income, cap ex, depreciation and total assets, plus $408 million of unallocated corporate expense. All three feasibility tests pass — divisions are separable, each reports its own earnings, and each competes in a sector with actively traded peers — so both the pricing route ($61,661M–$74,230M) and the intrinsic route ($75,663M) are available. See [[sum-of-the-parts-pricing]] and [[sum-of-the-parts-dcf]].

**Determinism:**
- DETERMINISTIC: once the per-asset values are set, the aggregation (`Σ assets − Σ liabilities`) and the comparison to going-concern value are pure arithmetic. Given a division's scalar and a multiple, or a division's cash flows and discount rate, the per-asset value is also mechanical.
- JUDGMENT: the motive; whether the separability / traceability / active-market tests pass; which mechanic to use for each asset; and whether any residual value (brand, synergy, corporate overhead) has been left out of the sum. This judgment needs the segment disclosures, the peer-transaction record for each asset class, and an understanding of how the assets interact operationally.

**Pitfalls:**
- Applying asset-based valuation to a business whose value comes from assets working together. Brand name is the canonical warning: it cuts across assets and cannot be separately valued, so the sum of the separately-valued assets misses it.
- Treating book value as *the* value rather than as a proxy of last resort.
- Forgetting that the sum of the parts omits anything that exists only at the corporate level — both the negative (unallocated corporate expenses) and the positive (cross-division synergies).
- Confusing this with a fourth valuation philosophy. Every asset value still comes from cash flows, pricing, or accounting convention.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket2spr21 p.103-107
- valuations--lecture_notes--spring_2020--valpacket2spr20 p.101-105

**Related:** [[liquidation-valuation]], [[fair-value-accounting-fas157]], [[sum-of-the-parts-framework]], [[sum-of-the-parts-pricing]], [[sum-of-the-parts-dcf]], [[private-company-valuation-framework]], [[intrinsic-vs-relative-valuation]]
