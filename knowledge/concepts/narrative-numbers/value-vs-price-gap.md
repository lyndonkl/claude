# Value versus price, and the gap between them

**Core idea:** Value and price are two different numbers set by two different processes. **Intrinsic value** is driven by the cash flows from existing assets, the growth in those cash flows, and the quality of that growth. You estimate it with accounting data and valuation tools. **Price** is driven by market mood and momentum, plus surface stories about demand and supply. Between the two sits THE GAP. An investor has three questions, in order: is there a gap? Will it close? If it will close, what will make it close? A DCF that ignores the third question is an academic exercise. Some assets can only be priced, never valued, because they generate no cash flows.

**Formulas:**
- Gap = Intrinsic value per share − Market price per share. Report it as a ratio too: Price as % of value = Price / Estimated value per share.
- Expected price in 1 year (if the market corrects) = Value today × (1 + cost of equity) − expected dividend next year.
- Expected 1-year return if the market corrects = (Expected price₁ + Dividend₁ − Price paid today) / Price paid today.

**Procedure:**
1. **Check the asset is valuable, not merely priceable.** Cash-flow assets can be valued and priced. Commodities can be valued loosely from utilitarian demand and supply, with long lags, and priced against their own normalised history. Currencies and collectibles can only be priced.
2. **Estimate value from the story**, using [[story-to-numbers-process]]. Do not look at price while doing it, so the price does not anchor the inputs.
3. **Compute the gap** and express it as price/value. In the Tesla model the Diagnostics sheet flags value below 50% of price as "value seems low", and value above 200% of price as "value seems high" — a prompt to recheck inputs, not proof of mispricing.
4. **Ask whether the gap will close.** This is a claim about market inefficiency plus a correction mechanism. Name the mechanism: news arrival, an earnings report, an activist, an acquirer, an index event.
5. **Convert to an expected return.** Roll value forward to a target price at the cost of equity, add the expected dividend, and compare with today's price.
6. **Match the gap to your horizon.** Time-based mispricing needs patience or a catalyst. Cross-sectional mispricing between comparables corrects faster. See [[three-approaches-to-valuation]].
7. **Accept that both sides move.** Value changes as information arrives; price swings around value much more violently. Being wrong is normal; the market is often more wrong.

**Reference data:** What can be valued and what can only be priced:

| Investment type | To value | To price |
|---|---|---|
| Assets (cash-flow generating) | Value from expected cash flows: higher cash flows and lower risk mean higher value | Price against similar assets, controlling for cash flows and risk |
| Commodity | Value from utilitarian demand and supply, but with long lags in both | Price against its own history (normalised price over time) |
| Currency | Cannot be valued | Price against other currencies: wider acceptance and more stable purchasing power mean a higher price |
| Collectible | Cannot be valued | Price on scarcity and desirability |

**Worked example:** Tesla, 1 November 2021. Damodaran's narrative gives an estimated value of $571.29 per share. The stock trades at $1,200. Price is 210.05% of value, so the gap is $628.71 per share, and the story would have to change materially to close it. Contrast Con Ed, August 2008: value $42.30, price $40.76, a gap of about 4%. There the implied perpetual growth rate in the price sits just below the 2.1% fundamental estimate, so the disagreement with the market is small enough that either side could be right.

**Determinism:**
- DETERMINISTIC: the gap and the price/value ratio, from value per share and price. The target price and expected return, from value, cost of equity, dividend and purchase price. The implied breakeven growth rate that sets model value equal to price.
- JUDGMENT: the value estimate itself; whether a gap is real or an artefact of your assumptions; whether and how the gap will close, which needs a view on the correction mechanism and your holding period.

**Pitfalls:**
- Treating a gap as a trade. Without a closing mechanism and a horizon, a gap is just an opinion.
- Reverse-engineering value from price, then calling the result independent.
- Valuing things that can only be priced: gold, currencies, collectibles.
- Reading a large gap as proof the market is wrong. Check your own inputs first — the Diagnostics verdict exists for that reason.
- Forgetting that the value estimate moves too, so today's gap is not tomorrow's.

**Sources:**
- valuationmotleyfool p.2 (value vs price, THE GAP, three questions), p.23 (Tesla price 210% of value)
- valintrospr21 p.6, p.15
- valintrospr20 p.6, p.15
- valintrospr20-repost p.6, p.15
- valpacket1spr21 p.280-281 (Con Ed breakeven growth, target price and expected return), p.309 (price swings around value)
- valpacket1spr20 p.276-277
- motley-fool-tesla-xlsx: `Valuation output` B33/B34/B35 (value, price, price as % of value), `Diagnostics` B9/B10 (value as % of price and the verdict thresholds)

**Related:** [[three-approaches-to-valuation]], [[narrative-numbers-bridge]], [[tesla-motley-fool-valuation]], [[narrative-updating-feedback-loop]], [[big-market-delusion]]
