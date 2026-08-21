# The story-to-numbers process (the five/six steps)

**Core idea:** Every valuation starts with a narrative, and the process turns that narrative into a value in a fixed order. Damodaran teaches it as five steps in the compact version and six in the lecture version. Survey the landscape. Create a narrative. Test it — is it possible, plausible, probable? Connect the narrative to the drivers of value. Value the company. Keep the feedback loop open, and be ready to modify the narrative as events unfold. The order matters. Working backwards from a target value produces a rationalisation, not a valuation.

**Formulas:** No formula for the process itself. Three rules govern the narrative you write in step 2:
- Rule 1: Keep it simple.
- Rule 2: Keep it focused.
- Rule 3: Stay grounded in reality.

Downstream, the value chain the narrative must populate is:
Total market × Market share = Revenues. Revenues − Operating expenses = Operating income. − Taxes = After-tax operating income. − Reinvestment = After-tax cash flow. Those cash flows are then adjusted for time value and operating risk through the discount rate, and for failure through a probability of failure, to give the value of operating assets. Add cash to get to the firm.

**Procedure:**
1. **Step 1 — Survey the landscape.** Assess the company (products, management, history), the market or markets it will grow in, the competition it faces and will face, and the macro environment. See [[landscape-survey]].
2. **Step 2 — Create a narrative for the future.** Write the story in prose. Simple, focused, grounded. If you cannot say it in a paragraph, you do not have it yet.
3. **Step 3 — Test the narrative.** Sort each claim into possible, plausible or probable, and check it against the impossible/implausible/improbable screens. See [[possible-plausible-probable]] and [[narrative-consistency-checks]].
4. **Step 4a — Connect the narrative to the drivers of value.** Each claim maps to exactly one driver: total market, market share, operating margin, reinvestment efficiency, discount rate, or failure probability. See [[narrative-to-value-drivers]].
5. **Step 4b/5 — Value the company.** Run the intrinsic model from those drivers to a value per share, including terminal value and the failure adjustment.
6. **Step 5/6 — Keep the feedback loop open.** Listen to people who know the business better than you. Value the counter-narratives too, so you know what someone else's story is worth. See [[narrative-updating-feedback-loop]].
7. **Step 6 — Modify the narrative as events unfold.** Classify the change as a break, a shift, or an expansion/contraction, and use the matching tool.

**Reference data:** The two step-counts are the same process:

| Lecture version (6 steps) | Compact version (5 steps) |
|---|---|
| 1. Survey the landscape | (folded into step 1) |
| 2. Create a narrative for the future | 1. Develop a narrative for the business |
| 3. Check the narrative: possible, plausible, probable | 2. Test the narrative against possible/plausible/probable |
| 4. Connect the narrative to key drivers of value | 3. Convert the narrative into drivers of value |
| 5. Value the company | 4. Connect the drivers to a valuation |
| 6. Keep the feedback loop / modify as events unfold | 5. Keep the feedback loop open |

Narrative-change taxonomy and tools (step 6):

| Change type | What happened | Valuation response | Tool |
|---|---|---|---|
| Narrative break / end | External events (legal, political, economic) or internal ones (management, competitive, default) end the story | Existing estimates of cash flows, risk, growth and value are no longer operative | Estimate the probability of the break and its consequences |
| Narrative shift | The business model improves or deteriorates: market size, market share and/or profitability move | Modify the estimates to reflect the new data | Monte Carlo simulation or scenario analysis |
| Narrative change (expansion or contraction) | Unexpected entry or success in a new market; unexpected exit or failure in an existing one | Redo the valuation with new market potential and characteristics | Real options |

**Worked example:** Uber, June 2014, runs the full loop. Step 1: map the business model — drivers, riders, a 20% revenue slice, low capital intensity. Step 2: the narrative — an urban car service company, expanding the market moderately, with local network effects, holding its 20% slice, staying capital-light. Step 3: the urban taxi market is probable, the suburban car-service market plausible, the car-ownership market only possible. Step 4: total market $100 billion growing 6%, market share 10%, target margin 40%, sales-to-capital 5.00, cost of capital 12% falling to 8%, failure probability 10%. Step 5: value of operating assets $6,595M, expected value after failure risk $5,895M. Step 6: counter-narratives — not just car service, not just urban, possibly global network effects — each of which is then valued in turn. See [[uber-narrative-valuation]].

**Determinism:**
- DETERMINISTIC: step 5 only. Given the driver set, the cash-flow schedule, terminal value, failure adjustment and value per share all follow mechanically.
- JUDGMENT: steps 1, 2, 3, 4 and 6. Writing the narrative needs company filings, market-size data, competitor behaviour and macro context. Classifying claims needs evidence on product success and financial results. Mapping claims to drivers needs industry benchmarks for margins, reinvestment and cost of capital.

**Pitfalls:**
- Starting at step 4 with a template of inputs and inventing a story afterwards.
- A narrative so broad it constrains nothing ("Uber is a technology company").
- Skipping step 3, which is where impossible and improbable stories get caught.
- Treating the feedback loop as optional. A narrative you never revise is a position, not an analysis.
- Changing the narrative every time the price moves. Revise on news about the business, not on price.

**Sources:**
- valpacket1spr21 p.257, p.259, p.261, p.269, p.270, p.271, p.274, p.277
- valpacket1spr20 p.253, p.255, p.257, p.265, p.266, p.267, p.270, p.273
- valuationmotleyfool p.10, p.24

**Related:** [[landscape-survey]], [[possible-plausible-probable]], [[narrative-consistency-checks]], [[narrative-to-value-drivers]], [[narrative-updating-feedback-loop]], [[uber-narrative-valuation]], [[tesla-motley-fool-valuation]], [[narrative-numbers-bridge]]
