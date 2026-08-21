# Gaming EVA: why year-to-year EVA is a dangerous target

**Core idea:** Firm value equals capital invested plus the present value of *all future* EVA. But firms rarely manage to that. They manage to the change in EVA from one year to the next, because it is simple, needs no forecasts, and can be pushed down to any division or person. That convenience has a cost. A manager can raise this year's EVA in three ways that destroy value: sacrifice future growth, take on riskier business, or keep investments off the capital base. A further problem sits on top. Even genuine EVA improvement may not raise the stock price, because the market already priced in an expected EVA. Beating last year is not the test; beating expectations is.

**Formulas:**
- `EVA_t = (ROC_t − WACC_t) × Capital invested at start of t`.
- `Firm value = Capital invested + Σ PV(EVA_t)` — the whole stream, not this year's number.
- `MVA = Market value − Capital invested = PV of expected EVA`.
- `ΔEVA_t = EVA_t − EVA_{t−1}` — the metric firms actually manage, and the one that can be gamed.
- Market value decomposes into `Expected EVA of assets in place + Expected EVA from future projects`, both already in the price.
- Stock price reaction depends on `Actual EVA − Expected EVA`, not on `Actual EVA − Last year's EVA`.

**Procedure — auditing an EVA increase:**
1. Confirm the arithmetic: recompute `EVA = (ROC − WACC) × Capital invested`, using beginning-of-year capital.
2. Test the growth trade-off game. Ask what was given up to deliver this year's number — deferred R&D, cancelled projects, cut maintenance, delayed capacity. Compare the reduction in future EVA against the current-year gain.
3. Test the risk game. Check whether the WACC rose. Higher dollar EVA earned in riskier businesses can still lower value, because the value of the business is the present value of EVA over time and a higher discount rate can dominate the higher EVA.
4. Test the capital-invested game. Check whether investments were routed off the capital base — expensed rather than capitalized, kept off-balance-sheet, or leased. Operating income then rises while measured capital falls, and EVA inflates mechanically from both directions.
5. Test against expectations. Estimate the EVA the market had priced in, and compare actual EVA against that, not against last year.
6. Decide whether the firm meets the three conditions under which year-to-year EVA is a safe target (see reference data). If it does not, do not use ΔEVA as the primary performance metric.

**Reference data:**

The three EVA games:

| Game | Mechanism | What to check |
|---|---|---|
| Growth trade-off | Give up valuable future growth to deliver higher EVA this year | Cancelled or deferred projects; R&D and maintenance cuts; the PV of forgone future EVA |
| Risk | Deliver higher dollar EVA from riskier businesses | Whether WACC rose; whether the discount-rate effect exceeds the EVA gain |
| Capital invested | Make investments that do not show up in capital invested | Expensed vs capitalized items; off-balance-sheet structures; leases; a falling capital base with rising operating income |

Two advantages of year-to-year EVA (why firms use it anyway):
1. It is simple and needs no forecasts of future earnings potential.
2. It can be broken down by any unit — person, division — as long as capital can be assigned and earnings allocated to those units.

Three conditions under which a year-to-year EVA focus does least damage:

| Condition | Why it helps | Which game it defuses |
|---|---|---|
| Most or all assets are already in place, so little value comes from future growth | Little future EVA to sacrifice | Growth trade-off game |
| Leverage is stable and investment decisions cannot easily change the cost of capital | WACC cannot be manipulated | Risk game |
| The sector is one where investors expect little or no surplus returns | Expected EVA is near zero, so a rise is unlikely to disappoint | Expectations problem |

**Worked example:** A division reports EVA up from $40M to $55M and claims a strong year. Run the audit.

Recompute: capital invested fell from $500M to $420M, and `EBIT(1−t)` rose from $90M to $101M. At a 10% WACC, `EVA = 101 − 0.10 × 420 = $59M` — even higher than reported. But the capital base dropped $80M. Investigation shows $60M of equipment moved to operating leases and $20M of process development expensed rather than capitalized. Restate the capital base to $500M and EVA becomes `101 − 50 = $51M`. That is the capital-invested game.

Next, check risk. The division shifted mix toward a more volatile segment, and its WACC rose from 10% to 11%. At the restated capital base, `EVA = 101 − 0.11 × 500 = $46M`. The dollar EVA rose, but the higher discount rate applies to *every future year*, so the present value of the EVA stream may well have fallen.

Finally, check expectations. If the market had priced in $60M for the year, a genuine $46M is a miss, and the stock can fall on a year-over-year "improvement."

Contrast with the clean teaching case: a firm with $100M of capital earning 15% against a 10% cost of capital is worth $170.85M, of which $70.85M is the PV of excess returns and MVA. Nothing there depends on a single year's number.

**Determinism:**
- DETERMINISTIC: EVA and ΔEVA given ROC, WACC and capital invested; restating EVA on an adjusted capital base; MVA as market value minus capital invested; the present value of an EVA stream.
- JUDGMENT: whether future growth was sacrificed, and how much it was worth. Whether a WACC change reflects a genuine risk shift or an estimation artifact. What EVA the market expected. Whether the firm meets the three safe-use conditions. This judgment needs the project pipeline, the lease and off-balance-sheet disclosures, the capital-expenditure history, and analyst expectations.

**Pitfalls:**
- Rewarding managers on ΔEVA without also measuring the capital base consistently year to year.
- Treating a rising EVA as proof of value creation. Value is the PV of the whole stream.
- Ignoring the discount-rate effect when EVA rises alongside risk.
- Allowing off-balance-sheet and expensed investment to shrink the capital base. It inflates EVA from both the numerator and the denominator.
- Expecting the stock to rise on higher EVA. Prices respond to surprises against expected EVA.
- Applying ΔEVA to a high-growth firm, where most value sits in future projects and is exactly what gets sacrificed.

**Sources:**
- `valuations--lecture_notes--spring_2021--valpacket3spr21 p.162-165`
- `valuations--lecture_notes--spring_2020--valpacket3spr20 p.162-165`

**Related:** [[eva-and-dcf-equivalence]], [[paths-to-value-creation]], [[growth-quality-and-excess-returns]], [[return-on-invested-capital]], [[management-incentives]]
