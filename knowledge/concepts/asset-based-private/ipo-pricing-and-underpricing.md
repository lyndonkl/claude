# IPO pricing: the banker's guarantee, underpricing, and offering quantity

**Core idea:** The offer price in an IPO is set by a banker, not by a valuation model, and the banker's incentives push it below fair value. Almost every IPO carries a pricing guarantee: the bank guarantees the offering price to the issuer and must buy the shares itself if the issue prices lower. That guarantee makes underpricing the banker's risk-management tool, and the evidence shows it works — first-day returns are positive in every size bucket, largest for the smallest deals. Underpricing is not automatically a disaster for the owner. It costs only on the shares actually sold, so an owner floating 10% loses a tenth of what an owner floating 100% loses, and the first-day pop may raise the price on the retained stake. Separately, the banker may price off comparables rather than off value, which is a different question from underpricing.

**Formulas:**
- `Cost of underpricing to the owner = Underpricing % × Value of the stake actually sold`
  `= Underpricing % × (Fraction offered × Total value investors would pay)`
- `First-day return = (Closing price on offering day − Offer price) / Offer price`
- Pricing off comparables: `Implied value = Peer multiple × Firm's metric`, e.g. `EV = EV/Sales_peers × Sales`, or `Market cap = (Market cap per user)_peers × Users`.

**Procedure:**
1. Produce the intrinsic value per share first. See [[ipo-valuation]].
2. Price the company off its peer group as a separate exercise. Choose the metric the market is actually paying on — for a user-based business that may be users rather than sales.
3. Recognize the two numbers answer different questions. The DCF says what the equity is worth; the comparables say what buyers will pay today. The offer price is a decision about which one to lead with.
4. Understand the banker's guarantee. It shifts risk to the bank if the issue fails, so the bank prefers a low offer price. Expect a discount from whichever benchmark is used.
5. Size the underpricing cost. **Decision rule: the loss equals the underpricing percentage times the value of the shares sold at the offering, not times the whole company.**
6. Choose the offering quantity accordingly. A small initial float caps the direct loss and leaves the retained stake exposed to the post-IPO price, which the pop may help.
7. If the owner plans follow-on sales, model them at the expected post-IPO price rather than at the offer price.
8. Consider the alternatives to the bank-intermediated model if the guarantee is not worth its fee.

**Reference data — offering-day returns by IPO size** (average return to investors on the offering day):

| Proceeds of IPO ($ millions) | Return on offering day |
|---|---|
| 2 – 10 | ~16.3% |
| 10 – 20 | ~9.7% |
| 20 – 40 | ~12.5% |
| 40 – 60 | ~13.7% |
| 60 – 80 | ~11.4% |
| 80 – 100 | ~9.0% |
| 100 – 200 | ~7.2% |
| 200 – 500 | ~5.7% |
| > 500 | ~7.6% |

Working assumption used in the packet's discussion: average underpricing of 10–15%.

**Reference data — social media comparables at the time of Twitter's IPO** ($ millions except per-user; users in millions):

| Company | EV | Market cap | Sales | Users | EV/Sales | Market cap/User |
|---|---|---|---|---|---|---|
| Facebook | 100,017.00 | 107,909.00 | 6,118.00 | 1,110 | 16.35 | $97.22 |
| LinkedIn | 28,448.50 | 29,321.90 | 1,244.00 | 225 | 22.87 | $130.32 |
| FB + LNKD combined | 128,465.50 | 137,230.90 | 7,362.00 | 1,335 | 17.45 | $102.79 |
| Twitter | ? | ? | 483.00 | 215 | — | — |

**Reference data — alternatives to the traditional IPO.** The bank-intermediated model has come under assault on two fronts: failures on the services (pricing and selling) sold in return for the fee, and the loss of the guarantee's credibility as bankers' public standing has fallen. Two alternatives:

| Alternative | Mechanism |
|---|---|
| Direct listing | The company lists its shares on the exchange directly; supply and demand set the price; no banker-set offer price and no guarantee |
| SPAC | A publicly traded blank-check entity raises money for an unspecified future acquisition, then buys a private company, which inherits the public listing |

**Worked example — pricing Twitter against value.** The DCF valued Twitter's equity at $9.97 billion, or $17.36 a share. Pricing it instead off the FB+LNKD combined EV/Sales of 17.45 applied to $483M of sales gives roughly $8.4bn of enterprise value. Pricing off market cap per user of $102.79 applied to 215 million users gives roughly $22.1bn of market cap. The per-user route implies more than double the DCF value. Which one goes in the prospectus is a choice about value versus price.

**Worked example — the cost of underpricing by float size.** Suppose investors would pay $20 billion for all of Twitter's common stock and the issue is underpriced by 15%.
- Offering 100%: `0.15 × $20bn = $3 billion` of wealth transferred to the initial investors.
- Offering 10%: the direct loss applies only to the $2bn sold, `0.15 × $2bn = $0.3 billion`, and the remaining 90% may be sold later at a price the first-day pop supported.

**Worked example — the arbitrage that is not one.** If IPOs are underpriced 10–15% on average, why not subscribe to every one and flip on day one? Because allocation is rationed. You receive full allotments of the overpriced deals and are cut back on the underpriced ones. That is the winner's curse, and it drives the realized return far below the headline underpricing.

**Determinism:**
- DETERMINISTIC: `{underpricing %, fraction offered, total value} → cost of underpricing`. `{peer multiple, firm metric} → implied pricing`. `{offer price, first-day close} → first-day return`. The lookup tables above.
- JUDGMENT: whether to anchor the offer price on value or on pricing; which comparable metric the market is actually paying on; the expected underpricing for this deal; how much to float initially and how to stage later sales; and whether a direct listing or SPAC beats the traditional route. That judgment needs the state of the IPO market, the peer group's current multiples, the bank's track record, and the owners' liquidity needs.

**Pitfalls:**
- Treating the offer price as the valuation. The banker's guarantee guarantees it will not be.
- Reading the underpricing evidence as a free trade. Rationing means you cannot actually harvest the average.
- Applying the underpricing loss to the whole company when only a slice is being sold.
- Ignoring that a first-day pop can raise the proceeds on later sales, which is why owners of small floats often tolerate it.
- Pricing off a metric the market has stopped paying for. Market cap per user only works while the market is paying per user.
- Assuming the peer group is fairly priced. Pricing inherits the peers' own mispricing — Twitter's implied value swung from $8.4bn to $22bn depending on which peer metric was used.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket2spr21 p.156, p.161-166
- valuations--lecture_notes--spring_2020--valpacket2spr20 p.154, p.159-163

**Related:** [[ipo-valuation]], [[silber-restricted-stock-regression]], [[vc-stage-varying-cost-of-equity]], [[private-to-public-sale]], [[pricing-vs-value]], [[relative-valuation-fundamentals]], [[market-efficiency]]
