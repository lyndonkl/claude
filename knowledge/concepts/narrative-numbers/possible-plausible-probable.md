# Testing a narrative: possible, plausible, probable

**Core idea:** Not every claim in a story deserves the same treatment in the numbers. Sort each claim by how confidently you can assign it a probability, then use the matching valuation device. **Possible** means you cannot assess the probability at all — it could happen, but you do not know what, when, or in what form. Value it as an option. **Plausible** means low probability with a reasoned argument but no tangible evidence yet. Show it as expected growth. **Probable** means you expect it, with some basis or evidence, though real uncertainty remains. Put it in the base-year numbers and the expected cash flows. Only probable claims belong in a base-case DCF. Claims move up the ladder as evidence arrives, and the valuation should move with them.

**Formulas:** None. The mapping is the rule:

- Possible → real option value, added on top of the DCF. Option value increases with the size of the possible market and with the exclusivity of the firm's access to it.
- Plausible → higher expected growth rate inside the DCF, with risk handled in the expected return. Value increases with market size and with the firm's competitive advantages.
- Probable → base-year numbers and expected cash flows, with risk handled in the expected return.

**Procedure:**
1. **Break the narrative into separate claims.** One market, one capability, one margin path per claim.
2. **Classify each claim.** Ask: can I attach a probability to this? If no, it is possible. If yes but there is no evidence yet, it is plausible. If there is evidence — product success, financial results — it is probable.
3. **Route each claim to its device.** Probable claims size the total market, the share and the margin. Plausible claims raise the growth rate. Possible claims leave the cash flows alone and become option value.
4. **Never double-route a claim.** A market counted in revenues cannot also be counted as option value. See [[contingent-claim-valuation]].
5. **Define what would promote a claim.** Moving from possible to plausible takes market-potential evidence and product testing. Moving from plausible to probable takes product success and financial results. Write those triggers down so the feedback loop has something to watch.
6. **Re-run the classification when news arrives.** Promotion or demotion changes which device applies, and therefore the value. See [[narrative-updating-feedback-loop]].
7. **Label the scenario set.** When you build a grid of stories, tag each row as plausible or probable so a reader knows which rows deserve weight. See [[narrative-scenario-grids]].

**Reference data:**

| Grade | Definition | Valuation response | What raises the value |
|---|---|---|---|
| It is possible | Probability cannot be assessed; you do not know what, when, or what it will look like | Value as an option | Size of the possible market; exclusivity of the firm's access |
| It is plausible | Low probability; a reasoned argument can be made, but no tangible evidence yet | Show as expected growth, adjusting for risk in the expected return | Market size; the firm's competitive advantages |
| It is probable | Increasing probability; expected to happen with some basis or evidence, though substantial uncertainty remains | Show in base-year numbers and expected cash flows, adjusting for risk in the expected return | Evidence of product success and financial results |

Promotion triggers: possible → plausible requires gauging market potential and testing products. Plausible → probable requires product success and financial results.

**Worked example:** Uber, June 2014, drawn as three nested circles. The **probable** innermost circle is the urban taxi market: it enters total market size, revenues and earnings in the base valuation ($100 billion market growing 6% a year, 10% share). The **plausible** middle circle is the suburban car service and rental market: it enters as a higher growth rate. The **possible** outermost circle is the car ownership market — people giving up cars entirely: it enters as option value on top of the DCF, worth $2–3 billion against a $5.9 billion DCF value.

Zomato, 2021, shows the same test applied to a scenario grid. The twelve stories span ₹16.58 to ₹150.02 per share. The largest-TAM "Delivery" stories (₹5,000,000M market) and the low-growth-India stories (₹1,125,000M) are classed **plausible**. The middle block — restaurant delivery with high-growth India (₹3,000,000M) and the base cases (₹2,000,000M) — is classed **probable**, and the base case is ₹39.48.

**Determinism:**
- DETERMINISTIC: once a claim is classified, the mechanics are fixed. A probable claim's effect on revenues follows from market size × share. A plausible claim's effect follows from the growth rate. A possible claim's option value follows from the option inputs.
- JUDGMENT: the classification itself. It needs evidence on market potential, product testing, product success and financial results — precisely the evidence the promotion triggers name.

**Pitfalls:**
- Putting a possible market into the cash flows because it makes the value work. That is how the impossible enters a spreadsheet.
- Counting the same market twice: once as growth, once as option value.
- Treating "possible" as a synonym for "unlikely". It means unassessable, which is why it gets a different tool.
- Never revisiting the classification, so a plausible claim stays plausible long after the evidence has arrived — or long after it failed to.
- Presenting a scenario range without saying which rows are probable. A range of stories with no likelihood labels is not analysis.

**Sources:**
- valpacket1spr21 p.261, p.263
- valpacket1spr20 p.257, p.259
- valuationmotleyfool p.10, p.25
- valpacket1spr21 p.307 (a scenario can always be found to justify a price; the test is probable, not possible)

**Related:** [[story-to-numbers-process]], [[narrative-consistency-checks]], [[contingent-claim-valuation]], [[narrative-scenario-grids]], [[uber-narrative-valuation]], [[big-market-delusion]]
