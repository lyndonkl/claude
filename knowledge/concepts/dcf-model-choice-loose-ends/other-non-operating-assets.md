# Other assets not yet counted (and the ones you must not add)

**Core idea:** After cash and cross holdings, the bridge invites you to add "other assets". One test governs: does the asset generate cash flows that are already in your forecast? If yes, its value is inside the DCF, and adding it again double counts. That rules out the office building you work in, the factories, the brand name and the customer list. Brand value shows up as higher margins or faster growth, not as a separate line. Never add goodwill. It is an accounting residual from past deals, not an asset. Two categories do qualify: overfunded pension plans, and unutilized assets that earn nothing today.

**Formulas:**
- Inclusion test: add an asset only if `cash flows from that asset ∉ forecast cash flows`.
- Overfunded pension: `Addable value = (Plan assets − Expected plan liabilities) × (1 − effective tax on withdrawal) × probability you can actually claim it`.
- Unutilized asset: `Addable value = estimated market value of the asset` (appraisal or comparable transaction).

**Reference data — the add/do-not-add list:**

| Asset | Add to DCF value? | Why |
|---|---|---|
| Real estate housing your offices | No | Already generating the cash flows you forecast |
| Property, plant and equipment (factories, productive assets) | No | Same |
| Brand names, customer lists | No | Value is embedded in margins and growth |
| Goodwill | **Never** | Not an asset; an accounting plug |
| Overfunded defined-benefit pension plan | Yes, with caveats | Surplus is a real claim, but may be blocked or heavily taxed |
| Unutilized assets (vacant land, idle plant, non-operating real estate) | Yes | Produce no cash flows, so they are absent from the DCF |

Caveats on pension surplus: collective bargaining agreements may prevent the company from claiming the excess, and withdrawals from pension plans are often taxed at much higher rates than ordinary income.

**Procedure:**
1. List every material asset on the balance sheet and in the notes.
2. For each, ask whether its earnings are inside your forecast operating income. If yes, stop — it is already valued.
3. Flag assets producing no revenue: vacant land, closed facilities, art collections, non-core real estate, unused spectrum or licences.
4. Estimate a market value for each flagged asset from appraisals or comparable transactions, and add it to firm value.
5. Check the pension footnote. If plan assets exceed the projected benefit obligation, quantify the surplus, then haircut it for bargaining constraints and withdrawal taxes before adding anything.
6. Strike goodwill from consideration entirely.
7. If an "asset" is a mothballed operation you might restart, consider whether it is better handled as a real option than as a market-value add-on.

**Worked example:** The Playboy Mansion — for decades Hugh Hefner's home, carried by the company and later sold to Daren Metropoulos of Metropoulos & Co. for a reported **$200 million**. It generated no operating cash flow for the business, so no DCF of Playboy's publishing and licensing operations would have captured it. That is the textbook shape of an addable asset: real, marketable, and absent from the cash flows. Contrast it with the Playboy brand itself, whose value flows through licensing revenue that a DCF already counts.

**Determinism:**
- DETERMINISTIC: the arithmetic of adding an estimated market value to firm value; the pension surplus given plan assets, liabilities and a tax rate.
- JUDGMENT: identifying which assets are genuinely idle; estimating their market value; assessing whether pension surplus is claimable and at what tax cost. This needs the pension footnote, union agreements, property appraisals and local tax rules.

**Pitfalls:**
- Adding brand value on top of a DCF whose margins already reflect the brand. This is the most common double count in practice.
- Adding goodwill because it sits on the asset side of the balance sheet.
- Counting headquarters real estate as a hidden asset while continuing to forecast rent-free operations.
- Booking the full pension surplus without the tax and bargaining haircuts.
- Valuing an idle asset at book value when book has no relationship to what a buyer would pay.

**Sources:**
- valpacket1spr21 p.233-234
- valpacket1spr20 p.229-230

**Related:** [[equity-value-bridge]], [[cross-holdings]], [[cash-in-valuation]], [[debt-and-other-claims-in-the-bridge]], [[real-options-in-valuation]], [[complexity-discount]]
