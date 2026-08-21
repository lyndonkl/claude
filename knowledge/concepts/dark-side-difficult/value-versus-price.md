# Value versus price: the gap, the catalyst and being wrong well

**Core idea:** Valuing and pricing are two different processes with different tools, different drivers and different skills. Intrinsic value is the value of cash flows adjusted for time and risk, driven by cash flows from existing assets, growth, and the quality of that growth, and estimated with discounted cash flow models, intrinsic multiples, book-value approaches and excess-return models. Price is set by demand and supply, driven by mood, momentum, liquidity, incremental news and herd behaviour, and estimated with multiples and comparables, charting and "pseudo DCF". Between them sits the gap. An investment thesis needs two beliefs, not one: that a gap exists, and that it will close. Most analysis that calls itself valuation is pricing wearing a costume.

**Formulas:**
- Percentage gap: `% difference = (Price − Value) / Value`. Positive means overvalued.
- Expected price one year out if today's value estimate, cost of equity and dividend are all fair:
  `E[P_1] = Value today × (1 + Cost of equity) − Expected dividend`.
- Expected annual return from buying at today's price, assuming price converges to value:
  `E[return] = (E[P_1] + Dividend_1 − Price paid) / Price paid`.
- Margin of safety: buy only when `Price ≤ Value × (1 − margin)`, with the margin sized to your uncertainty about the gap.
- Unbiasedness test: over many valuations, the count of upward revisions should be roughly equal to the count of downward revisions.

**Procedure:**
1. Classify what you are doing. Intrinsic tools and intrinsic drivers mean valuing. Comparables, target prices, momentum and net-asset-value discounts mean pricing. Both are legitimate; confusing them is not.
2. Estimate intrinsic value with the model that fits the company's difficulty ([[difficult-company-taxonomy]]).
3. Compute the gap against the market price.
4. Deal with uncertainty about the **size** of the gap. Four tools: demand a margin of safety; collect more information about the company; ask what-if questions through scenario analysis; or confront the uncertainty directly and model it ([[scenario-analysis-and-simulation]]).
5. Deal with uncertainty about whether the gap will **close**. Two strategies: the karmic approach (buy and wait, trusting the market to correct) or the catalyst approach. Catalysts worth watching for: a new CEO or management team, a blockbuster new product, an acquisition bid for the firm, or your own activist buying.
6. Lengthen your time horizon. It is the cheapest way to reduce exposure to the risk that convergence never happens.
7. Convert the gap into an expected return using the formulas above, so the thesis is comparable to other opportunities.
8. Update the valuation as information arrives, and track your own revisions for bias.

**Reference data (1):** The two processes side by side.

| | Value | Price |
|---|---|---|
| Determined by | Cash flows, adjusted for time and risk | Demand and supply |
| Drivers | Cash flows from existing assets; growth in cash flows; quality of growth | Mood and momentum; liquidity and ease of trading; incremental information versus expectations; group think |
| Tools | DCF valuation; intrinsic multiples; book-value approaches; excess-return models | Multiples and comparables; charting and technical indicators; pseudo DCF |
| The gap between them | Drivers: information, liquidity, corporate governance. Tools: behavioural finance, price catalysts | |

**Reference data (2):** Three views of the gap and the strategy each implies.

| Camp | View of the gap | Strategy |
|---|---|---|
| The efficient marketer | Gaps, if they occur, are random | Index funds |
| The value extremist | Pricers are dilettantes moving fad to fad; price eventually converges on value | Buy and hold undervalued stocks |
| The pricing extremist | Value lives only in the heads of eggheads; even if it exists, price may never converge | Find mispriced securities; get ahead of shifts in demand and momentum |

The pricer's dilemma has three parts. Without a value estimate there is **no anchor**, so you are pushed back and forth as price moves and everything becomes relative. Strategy becomes **reactive** rather than proactive. And **crowds are fickle**: success requires reading crowd mood and spotting shifts early, which is nearly impossible to model systematically.

**Reference data (3):** Apple — Damodaran's own value estimates against the price.

| Month | Price per share | Value per share | % difference |
|---|---|---|---|
| Sep-11 | $54.47 | $69.30 | −21.39% |
| Sep-12 | $95.30 | $91.29 | +4.40% |
| Sep-13 | $68.11 | $86.43 | −21.20% |
| Sep-14 | $100.75 | $97.91 | +2.90% |
| Sep-15 | $110.30 | $130.91 | −15.74% |
| Sep-16 | $113.05 | $126.47 | −10.61% |
| Sep-17 | $154.12 | $158.33 | −2.66% |
| Sep-18 | $225.74 | $201.50 | +12.03% |
| Sep-19 | $249.75 | $243.25 | +2.67% |

Gaps open and close repeatedly even for the most heavily followed stock in the world.

**Reference data (4):** Amazon, value versus price at four analysis dates. 2000: value ≈$35, price ≈$84 (overvalued). 2001: value ≈$20, price ≈$12 (undervalued). 2002: value ≈$24, price ≈$16 (undervalued). 2003: value ≈$36, price ≈$59 (overvalued). Both move, but price swings around value far more violently. The analyst may always be wrong; the market is often **more** wrong.

**Reference data (5):** Two classroom tests for telling pricing from valuing. First, a Redfin listing: 5369 La Jolla Mesa Dr, La Jolla, CA, $995,000, 3 beds, 2.5 baths, 1,440 sq ft at $691 per square foot, built 1955. Real-estate "appraisal" by price per square foot against comparable homes is pricing, not valuation. Second, a Deutsche Bank report on BB Biotech dated 13 August 2013: Buy, price CHF 124.00, target raised from CHF 106.50 to CHF 164.50 (+54.5%), 52-week range CHF 128.40–84.90, arguing that net asset value rose 36% in the first half of 2013 against 27% for the Nasdaq Biotech Index, that shares trade at a 23% discount to net asset value, that the fund yields 5% a year, and that the sector is re-rating on M&A, cheap money and high liquidity. Despite the language of value, every argument is relative, momentum-based and target-price driven. It is pricing.

**Worked example (the gap turned into a return):** Con Edison. The DCF value is $42.30 per share, the cost of equity is 7.70%, the current dividend is $2.32 growing at 2.1%, and the market price is $40.76.
- Expected dividend next year = 2.32 × 1.021 = **$2.369**.
- Expected price in one year = 42.30 × 1.077 − 2.369 = **$43.19**.
- Expected return if the market corrects = (43.19 + 2.369 − 40.76)/40.76 = **11.8%**.
The gap of $1.54 per share becomes a quantified expected return, comparable against any other investment.

**Worked example (being wrong well):** the 2014 retrospective on the 2000 Amazon forecast. Revenues were badly over-forecast early (2004 forecast $19,059m against $6,921m actual) and badly under-forecast late (2013 forecast $49,244m against $74,452m actual; 2014 LTM forecast $51,460m against $85,247m actual). Margins were the real miss: the forecast converged to 10%, while actual margins peaked at 6.36% in 2004 and fell to 1.00% in 2013 and 0.11% in 2014 LTM. Amazon chose scale over profitability. The direction call in 2000 was defensible; nearly every line item was wrong. Value estimates change as information arrives, and that is the essence of risk, not a failure of the analyst.

**Determinism:** DETERMINISTIC — `(Price, Value) → % difference`; `(Value, cost of equity, dividend) → expected price in one year`; `(expected price, dividend, price paid) → expected return`; and the count of upward versus downward revisions in a bias test. JUDGMENT: the value estimate itself, whether a given analysis is pricing or valuing, the size of the margin of safety, whether a catalyst exists and when it will fire, and the time horizon you can hold. That judgment needs ownership data, activist activity, product pipelines, the takeover market, and honest self-assessment of your own track record.

**Pitfalls:**
- Calling a target price, a net-asset-value discount or a per-square-foot comparison a "valuation". Those are pricing.
- Buying a gap with no view on why it should close. Without a catalyst or a long horizon, an undervalued stock can stay undervalued indefinitely.
- Treating a changed valuation as a failure. New information should move your estimate; if it never does, you are anchoring.
- Systematic bias in one direction. If your revisions are overwhelmingly upward or downward, your process is skewed.
- Playing the pricing game without an anchor, which leaves you reactive and reading crowds you cannot model.
- Assuming your value estimate is right and the market's price is wrong every time. Both move, and both are estimates; the market's error is usually larger, but not always.
- Skipping the margin of safety in exactly the cases — young, distressed, emerging-market companies — where uncertainty about the gap is largest.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.281
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.308-310
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.358-369
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.299-301
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.349-360

**Related:** [[scenario-analysis-and-simulation]], [[difficult-company-taxonomy]], [[value-of-control-and-restructuring]], [[market-and-macro-crisis-valuation]], [[young-company-valuation]], [[relative-valuation]], [[dividend-discount-model]], [[cost-of-equity]]
