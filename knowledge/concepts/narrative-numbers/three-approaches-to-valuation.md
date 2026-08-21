# The three approaches to valuation, and when each works

**Core idea:** There are hundreds of models but only three approaches. **Intrinsic valuation** ties an asset's value to the cash flows it can generate and the risk in those cash flows; its usual form is a DCF. **Relative valuation (pricing)** asks what buyers pay for comparable assets, after scaling price by a shared metric such as earnings, revenues or subscribers. **Contingent claim valuation** adds value for payoffs that depend on an event happening. A fourth label, asset-based valuation, is not a real fourth approach: to value each separate asset you still need cash flows or comparables. The three approaches can give three different numbers for the same asset on the same day. Which one fits depends on your horizon, your benchmark and what you can act on.

**Formulas:**
- Intrinsic (DCF): Value of asset = Σ_t E(CF_t) / (1 + r)^t, over t = 1…n. E(CF_t) = expected cash flow in period t. r = discount rate reflecting the risk of those cash flows. n = life of the asset.
- Relative: Multiple = Market price / Standardising variable. The variable is a value the comparables share — earnings, book value, revenues, subscribers.
- Contingent claim: see [[contingent-claim-valuation]].

**Procedure:**
1. **Check the asset can be valued at all.** It needs cash flows. Gold, currencies and collectibles have none, so they can only be priced. See [[value-vs-price-gap]].
2. **State the market inefficiency you are betting on.** Every approach assumes markets make a mistake, plus a view on how it gets corrected. DCF assumes mispricing across time, corrected as news arrives. Relative valuation assumes mispricing *between* similar assets, corrected fast. If you believe markets are efficient, price is your best estimate and any model just rationalises it.
3. **Match the approach to the investor.** Use DCF if you have a long horizon, or can supply the catalyst (activist, acquirer), or can hold against peer pressure. Use pricing if your horizon is short, you are judged against a benchmark, or you can go long-short.
4. **Check the prerequisites for pricing.** You need many comparable assets, market prices for them, and a standardising variable. Missing any one kills the approach.
5. **Use asset-based valuation only in its three contexts.** Liquidation, accounting (fair value or goodwill), or sum-of-the-parts. It works only when assets are separable with stand-alone cash flows.
6. **Do not stop at one approach.** Run at least an intrinsic value and a pricing check, then explain the gap between them rather than averaging it away.

**Reference data:**

| Approach | Philosophical basis | Information needed | Market inefficiency assumed |
|---|---|---|---|
| Intrinsic / DCF | Every asset has an intrinsic value set by cash flows, growth and risk | Life of the asset; cash flows over that life; a discount rate | Assets are mispriced across time; prices correct as news arrives |
| Relative / pricing | Intrinsic value is impossible or near-impossible to estimate; price is what the market will pay | An identical asset or a group of comparables; a standardised measure; controls for differences | Pricing errors across similar assets are easier to spot, easier to exploit and corrected faster |
| Contingent claim | Some cash flows only arrive if an event occurs | Value and variance of an underlying asset; exercise price; life | Conventional models miss the value of optionality |

Advantages and disadvantages:

| | DCF | Relative valuation |
|---|---|---|
| Advantages | Built on fundamentals, so less exposed to market moods; the right frame if you buy businesses not stocks; forces you to understand the business and confronts you with what the price assumes; a long horizon insulates you from market opinion | Reflects market moods, which is what you want when selling today (IPO, M&A) or trading momentum; always produces some cheap and some dear names, which suits relative-performance mandates; needs less explicit information; lets you play the "incremental" game on the next earnings report or news item |
| Disadvantages | Needs far more explicit inputs; those inputs are noisy and can be bent to a desired answer, so analyst "quality" becomes skill at hiding the tweak; nothing guarantees anything looks cheap — you can find an entire market overvalued, which is a problem for sell-side analysts and fully-invested managers | A relatively cheap portfolio can still be absolutely expensive; it assumes the market is right in aggregate and wrong on single names, so it fails when whole markets are mispriced; it only *appears* to need less information — the implicit assumptions are still there, just unstated |

**Worked example:** Con Ed, August 2008, is a clean intrinsic case. It is a regulated utility with slow-growing demand, a debt ratio stable near 30% for decades, and dividends equal to about 97% of FCFE. That profile justifies a stable-growth dividend discount model. Cost of equity = 4.10% + 0.80 × 4.5% = 7.70%. Growth = retention 27% × ROE 7.7% ≈ 2.1%. Value per share = 2.32 × 1.021 / (0.077 − 0.021) = $42.30, against a market price of $40.76 on 12 August 2008. The same toolkit applied to Tesla in November 2021 gave $571.29 against a $1,200 price — the model is identical, the confidence is not.

**Determinism:**
- DETERMINISTIC: the discounting itself (cash flows, discount rate, life → present value); computing any multiple (price, standardising variable → multiple); the Con Ed Gordon-growth arithmetic (DPS, g, r → value per share).
- JUDGMENT: choosing the approach, which needs the investor's horizon, benchmark and ability to act. Estimating cash flows, growth, life and the discount rate. Picking comparables and the controls for their differences. Judging whether the going concern is worth more than liquidation.

**Pitfalls:**
- Using DCF on an asset with no cash flows.
- Treating relative valuation as assumption-free. The assumptions are implicit, not absent.
- Averaging a DCF value and a multiples-based price into one number instead of explaining the gap.
- Mandate mismatch: a fully-invested long-only manager cannot act on "everything is overvalued," so a pure DCF process will fight the job description.
- Treating asset-based valuation as an independent third approach.

**Sources:**
- valintrospr21 p.5-17, p.24
- valintrospr20 p.5-17, p.24
- valintrospr20-repost p.5-17, p.24
- valpacket1spr21 p.279 (Con Ed stable-growth DDM worked example)
- valpacket1spr20 p.275 (same Con Ed case, 2020 edition)

**Related:** [[contingent-claim-valuation]], [[value-vs-price-gap]], [[valuation-misconceptions]], [[narrative-to-value-drivers]], [[story-to-numbers-process]]
