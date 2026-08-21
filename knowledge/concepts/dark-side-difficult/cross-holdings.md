# Cross holdings: when the DCF is only half the valuation

**Core idea:** Emerging-market companies hold stakes in each other far more often than developed-market companies do. Part of the reason is history — many large listed firms were family businesses until recently. Part of it is control: the people running these firms use cross holdings to keep it. The consequence for an analyst is blunt. In many group companies the real work starts *after* the discounted cash flow is finished, because half the value sits in stakes in other companies, and those stakes must be valued with very little information. Get the operating DCF perfect and you may still have valued only half the firm.

**Formulas:**
- Equity bridge with holdings: `Value of equity = Value of operating assets − Debt − Minority interests + Cash + Value of cross holdings and other non-operating assets`.
- Majority (consolidated) holding: the subsidiary's revenues and operating income are already inside the parent's financials, so the parent's operating-asset value includes them. Subtract the **minority interest** — the portion of the consolidated subsidiary the parent does not own — at its estimated market value, not its book value.
- Minority (unconsolidated) holding: the subsidiary is *not* in the parent's operating numbers, so **add** the value of the stake: `Value of stake = Ownership % × Value of subsidiary equity`.
- Quick approximation when the subsidiary cannot be valued: `Value of stake ≈ Ownership % × (Book value of subsidiary equity × the sector's price-to-book ratio)`, or apply the parent's own or the sector's multiple to the stake's earnings.
- Composition check: `% of value from operating assets + % from holdings + % from cash = 100%`.

**Procedure:**
1. List every holding from the notes to the accounts, with the ownership percentage and the accounting treatment (consolidated, equity method, or cost).
2. Classify each as majority or minority. This determines whether you subtract a minority interest or add a stake.
3. Value the operating business with the DCF as usual.
4. For each **minority** holding: value the subsidiary if it is listed (use its market capitalisation, or better, your own valuation of it) and multiply by the ownership percentage. If it is unlisted and opaque, apply a sector multiple to its book equity or earnings and disclose the approximation.
5. For each **consolidated** subsidiary: value the minority interest at market, not at the book number that sits on the balance sheet. Book minority interests understate the claim when the subsidiary is profitable.
6. Assemble the bridge and report the composition — operating assets, holdings, cash — as percentages of total value.
7. If holdings exceed roughly a third of value, say so prominently. The valuation's error bars are then driven by the holdings, not by the DCF.
8. Watch for double counting: a stake valued separately must not also be inside the operating cash flows.

**Reference data:** The Tata Group, April 2010 — where the value actually sits.

| Company | % of value from operating assets | % from holdings | % from cash |
|---|---|---|---|
| Tata Chemicals | 47.62% | 47.06% | 5.32% |
| Tata Steel | 50.94% | 47.45% | 1.62% |
| Tata Motors | 60.41% | 36.62% | 2.97% |
| TCS | 95.13% | 4.64% | 0.22% |

Two of the four companies get roughly **half** their value from cross holdings. TCS, a pure operating business, is the exception that proves the rule.

Holdings in the equity bridge of other valuations in the packet:
- Shell (March 2016): value of operating assets $159,783.41m **+ cash $31,752m + cross holdings $33,566m** (long-term joint-venture investments) **− debt $58,379m − minority interests $1,245m** = equity $165,477.41m; ÷ 4,209.7 shares = $39.31 per share. The cross holdings alone are about 20% of equity value.
- Saudi Aramco: PV of FCFE $1,589.12bn + cash $48.84bn + holdings $10.61bn = $1,648.57bn.
- Amazon (2020): − debt and minority interests $91,401m + cash and non-operating assets $71,391m.

**Worked example:** Tata Chemicals, April 2010. The DCF of the operating business — cost of equity 13.82% (beta 1.21, lambda 0.75), WACC 11.62%, growth 5.85% from a 56.5% reinvestment rate at a 10.35% return on capital — produces only 47.62% of the company's total value. Another 47.06% comes from stakes in other Tata companies and 5.32% from cash. The final estimate of Rs 372 per share (against a price of Rs 314) is therefore about as sensitive to how the holdings were valued as to every operating assumption combined. An analyst who spent all the effort on the DCF and marked the holdings at book value would have produced a materially different, and worse, answer.

**Determinism:** DETERMINISTIC — (ownership percentages, subsidiary values, minority-interest values, operating-asset value, cash, debt) → equity value and the composition percentages. JUDGMENT: the value of each holding, especially unlisted ones (needs subsidiary financials, sector multiples, or a full valuation of each subsidiary), whether a listed subsidiary's market price is itself right, and how to treat circular cross holdings where two group companies own each other.

**Pitfalls:**
- Marking cross holdings at book value. Book value of a stake bears no relation to its worth.
- Subtracting the **book** minority interest from a consolidated valuation. Use an estimated market value.
- Adding a minority holding's value **and** leaving its earnings in the operating income — a straight double count.
- Treating a majority stake as a minority one, or vice versa; the sign of the adjustment flips.
- Spending all the analytical effort on the operating DCF when half the value is in the holdings.
- Ignoring the reason the holdings exist. Cross holdings usually exist to preserve control, which means they will not be sold to realise value, and which links straight to [[return-improvement-and-governance-drag]].

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.334-336
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.355
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.325-327
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.346
- spreadsheet model doc: ginzu-fcff-corona.md — Valuation output rows 25–29 (equity bridge)

**Related:** [[country-risk-exposure]], [[return-improvement-and-governance-drag]], [[commodity-and-cyclical-valuation]], [[truncation-and-political-risk]], [[difficult-company-taxonomy]], [[equity-bridge]], [[relative-valuation]]
