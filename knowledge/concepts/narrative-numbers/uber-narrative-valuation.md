# Worked example: the Uber narrative valuation, June 2014

**Core idea:** Uber in June 2014 is the course's end-to-end demonstration of the story process. A young private company with no useful history, a contested market definition and a live funding round makes every step visible. Damodaran wrote a five-part narrative, mapped each part to one value driver, built a ten-year FCFF model, adjusted for failure risk, and got $5.9 billion — against a funding round that imputed about $17 billion. He then valued the counter-narratives rather than dismissing them. The point of the case is not the number. It is that the disagreement with investors was locatable: it lived in market definition, market share and the revenue slice.

**Formulas:**
- Revenues_t = Overall market_t × Share of gross market_t × Revenue slice. Revenue slice = 20% of gross receipts.
- Overall market_t = $100,000M × (1.06)^t.
- Operating income_t = Revenues_t × Operating margin_t. Margin ramps linearly from 7.00% to 40.00% over ten years.
- After-tax operating income_t = Operating income_t × (1 − effective tax rate_t). Tax rate rises from 31% to 40%.
- Reinvestment_t = (Revenues_t − Revenues_{t−1}) / 5.00. The sales-to-capital ratio of 5.00 means $5 of incremental revenue per $1 of incremental capital.
- FCFF_t = After-tax operating income_t − Reinvestment_t.
- Stable reinvestment rate = Stable growth / Return on capital = 2.5% / 25% = 10%.
- Terminal value at year 10 = FCFF_terminal / (Stable cost of capital − Stable growth) = 793 / (0.08 − 0.025) = $14,418M.
- Expected value = Value of operating assets × (1 − probability of failure) = 6,595 × 0.90 = $5,895M.

**Procedure:** How the case was built, in the order of [[story-to-numbers-process]]:
1. **Survey the landscape.** Map the business model in six boxes. Drivers apply and get an Uber iPhone. Riders request and track cars on the app. Uber sets fares, with surge pricing at peak demand. Riders pay Uber by credit card, not the driver. Uber keeps about 20% of receipts, and its costs are R&D, technology, customer-acquisition rebates, marketing and per-city staff. Reinvestment is technology plus occasional local acquisitions, since Uber owns no cars.
2. **Write the narrative.** Five parts. An urban car service business. Expanding the market moderately, about 40% over ten years, by bringing in new users. Local networking benefits only — being big in one city does not help entering the next. Holding the 20% revenue slice on first-mover advantages. Keeping the low-capital model, with drivers as contractors.
3. **Test it.** The urban taxi market is probable, so it goes into total market, revenues and earnings. The suburban car-service and rental market is plausible, so it goes in as a higher growth rate. The car-ownership market is only possible, so it becomes option value.
4. **Map narrative to drivers.** Total market $100 billion in 2013 growing 6% a year. Market share 10%. Target pre-tax operating margin 40%. Sales-to-capital 5.00. Cost of capital 12% for years 1–5, declining to 8% by year 10. Probability of failure 10%.
5. **Value it.** Run the ten-year schedule, add terminal value, discount, then apply the failure adjustment.
6. **Keep the feedback loop.** List and value the counter-narratives.

**Reference data:** Uber intrinsic valuation, 8 June 2014 ($ millions except percentages):

| Year | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| Overall market | 106,000 | 112,360 | 119,102 | 126,248 | 133,823 | 141,852 | 150,363 | 159,385 | 168,948 | 179,085 |
| Share of market (gross) | 3.63% | 5.22% | 6.41% | 7.31% | 7.98% | 8.49% | 8.87% | 9.15% | 9.36% | 10.00% |
| Revenues as % of gross | 20% | 20% | 20% | 20% | 20% | 20% | 20% | 20% | 20% | 20% |
| Annual revenue | 769 | 1,173 | 1,528 | 1,846 | 2,137 | 2,408 | 2,666 | 2,916 | 3,163 | 3,582 |
| Operating margin | 7.00% | 10.67% | 14.33% | 18.00% | 21.67% | 25.33% | 29.00% | 32.67% | 36.33% | 40.00% |
| Operating income | 54 | 125 | 219 | 332 | 463 | 610 | 773 | 953 | 1,149 | 1,433 |
| Effective tax rate | 31% | 32% | 33% | 34% | 35% | 36% | 37% | 38% | 39% | 40% |
| − Taxes | 17 | 40 | 72 | 113 | 162 | 220 | 286 | 362 | 448 | 573 |
| After-tax operating income | 37 | 85 | 147 | 219 | 301 | 390 | 487 | 591 | 701 | 860 |
| Sales/capital ratio | 5.00 | 5.00 | 5.00 | 5.00 | 5.00 | 5.00 | 5.00 | 5.00 | 5.00 | 5.00 |
| − Reinvestment | 94 | 81 | 71 | 64 | 58 | 54 | 52 | 50 | 49 | 84 |
| FCFF | −57 | 4 | 76 | 156 | 243 | 336 | 435 | 541 | 652 | 776 |

Terminal year: EBIT(1−t) = $881M; reinvestment $88M; FCFF $793M. Stable growth 2.50%, stable cost of capital 8%, stable return on capital 25%, stable reinvestment rate 10%. Terminal value at year 10 = 793 / (0.08 − 0.025) = $14,418M.

Value of operating assets = $6,595M. After a 10% probability of failure: expected value = 6,595 × 0.9 = $5,895M. For contrast, the $1.2 billion investment in June 2014 imputed roughly $17 billion for Uber's operating assets.

Competing narratives, same machinery:

| | Uber (Gurley) | Uber (Gurley modified) | Uber (Damodaran) |
|---|---|---|---|
| Total market | $300 billion, growing 3%/yr | $300 billion, growing 3%/yr | $100 billion, growing 6%/yr |
| Market share | 40% | 40% | 10% |
| Revenue slice | 20% | 10% | 20% |
| Value | $53.4 billion + $10 billion+ option value | $28.7 billion + $6 billion+ option value | $5.9 billion + $2–3 billion option value |

The full twelve-cell narrative grid, ranging from $799M to $90,457M, is reproduced in [[narrative-scenario-grids]].

**Worked example:** Trace year 1 end to end. Overall market = 100,000 × 1.06 = $106,000M. Share of gross = 3.63%, so gross bookings = $3,847M. Uber's slice of 20% gives revenue of $769M. Margin of 7.00% gives operating income of $54M. Tax at 31% leaves $37M. Revenue rose from a base of $302M to $769M, so reinvestment = ΔRevenue / 5.00 = $94M. FCFF = 37 − 94 = −$57M. Negative in year 1, positive from year 2, and the growth is paid for out of the same model that produces the value.

**Determinism:**
- DETERMINISTIC: everything below the driver set. The market path from $100 billion at 6%. Revenues from share and slice. Operating income from the margin ramp, and taxes from the rate path. Reinvestment from ΔRevenue / 5.00, then FCFF. Discounting at 12% falling to 8%. Terminal value from 793/(0.08−0.025). The failure adjustment, 6,595 × 0.9.
- JUDGMENT: the market definition, $100 billion urban taxi against $300 billion mobility. The 6% market growth and the 10% share. The 40% target margin. Whether the 20% slice holds under competition. The 5.00 sales-to-capital. The 12%-to-8% cost-of-capital path. The 10% failure probability. Each needs evidence — industry market-size studies, competitor pricing behaviour, comparable margins, and the capital intensity of an asset-light model.

**Pitfalls:**
- Arguing about the value instead of the drivers. The $5.9 billion versus $53.4 billion gap is entirely market size, share and slice.
- Assuming the 20% revenue slice survives competition. It had already been cut in cities facing Lyft and Hailo, and the modified Gurley case shows a slice cut to 10% roughly halves the value.
- Treating local network effects as global. That single assumption is worth billions in the grid.
- Forgetting the failure adjustment on a young private company, which cost 10% of value here.
- Putting the car-ownership market into the cash flows. It belongs in option value.
- Reading the imputed $17 billion from a funding round as a valuation. It is a price, set by a negotiation. See [[value-vs-price-gap]].

**Sources:**
- valpacket1spr21 p.258, p.260, p.263, p.269, p.270, p.271, p.272, p.273
- valpacket1spr20 p.254, p.256, p.259, p.265, p.266, p.267, p.268, p.269

**Related:** [[story-to-numbers-process]], [[landscape-survey]], [[possible-plausible-probable]], [[narrative-to-value-drivers]], [[narrative-scenario-grids]], [[narrative-updating-feedback-loop]], [[contingent-claim-valuation]], [[tesla-motley-fool-valuation]]
