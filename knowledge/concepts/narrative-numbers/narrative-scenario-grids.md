# Narrative scenario grids: different stories, different numbers

**Core idea:** Value is a function of the story, so a range of stories gives a range of values. A scenario grid makes that explicit. Pick the two to four story dimensions that actually drive value, define discrete levels for each, run the same model for every combination, and tabulate the value. The spread is usually enormous — for Uber, more than a hundredfold from the narrowest story to the widest. The grid is not a hedge or an averaging device. It is a map that shows which story choices matter, and it forces you to say which cell you believe and why. Pair every grid with a likelihood label per row, or it degenerates into "anything is possible".

**Formulas:**
- Value_cell = Model(driver set implied by that combination of story levels). The model is unchanged across cells; only the inputs move.
- Spread = Max value / Min value. Report it. A 100x spread means the value is a statement about the story, not about the arithmetic.
- Breakeven scenario: the combination of inputs at which model value equals the market price. Solve for it and then judge whether it is probable.

**Procedure:**
1. **Choose the dimensions that move value most.** Usually total market definition, market growth effect, network effects, competitive advantage, take rate, target margin and cost of capital. Two to four dimensions keeps the grid readable.
2. **Define discrete, named levels for each dimension.** Name them in story language ("A3: Logistics", "Delivery Juggernaut"), not just numbers, so the grid reads as stories.
3. **Hold everything else fixed,** including the model structure and any driver you are not testing. In the Zomato grid, market share is held at 40% in every row.
4. **Run the model per combination.** This is mechanical.
5. **Sort by value and inspect the ends.** The extremes tell you what each dimension is worth.
6. **Label each row possible, plausible or probable.** See [[possible-plausible-probable]]. Only probable rows deserve weight in a base case.
7. **Locate the market price on the grid.** Find the cheapest scenario that justifies the current price, then ask whether that scenario is probable — not whether it is possible. Some scenario always justifies any price.
8. **State your chosen cell and the evidence for it.** That is your base case, and the grid is now your sensitivity analysis.

**Reference data:** Uber narrative grid, June 2014 ($ millions). Four dimensions were varied:
- Total market: A1 urban car service, A2 all car service, A3 logistics, A4 mobility services.
- Growth effect: B1 none, B3 increase market by 50%, B4 double market size.
- Network effect: C1 none, C3 strong local, C5 strong global.
- Competitive advantage: D1 none, D3 semi-strong, D4 strong and sustainable.

| Total market | Growth effect | Network effect | Competitive advantage | Value of Uber |
|---|---|---|---|---|
| A4. Mobility services | B4. Double market size | C5. Strong global | D4. Strong & sustainable | $90,457 |
| A3. Logistics | B4. Double market size | C5. Strong global | D4. Strong & sustainable | $65,158 |
| A4. Mobility services | B3. Increase market by 50% | C3. Strong local | D3. Semi-strong | $52,346 |
| A2. All car service | B4. Double market size | C5. Strong global | D4. Strong & sustainable | $47,764 |
| A1. Urban car service | B4. Double market size | C5. Strong global | D4. Strong & sustainable | $31,952 |
| A3. Logistics | B3. Increase market by 50% | C3. Strong local | D3. Semi-strong | $14,321 |
| A1. Urban car service | B3. Increase market by 50% | C3. Strong local | D3. Semi-strong | $7,127 |
| A2. All car service | B3. Increase market by 50% | C3. Strong local | D3. Semi-strong | $4,764 |
| A4. Mobility services | B1. None | C1. None | D1. None | $1,888 |
| A3. Logistics | B1. None | C1. None | D1. None | $1,417 |
| A2. All car service | B1. None | C1. None | D1. None | $1,094 |
| A1. Urban car service | B1. None | C1. None | D1. None | $799 |

Range: $799M to $90,457M, a spread of about 113x, driven entirely by narrative choices.

Zomato story grid, 2021 (TAM in ₹ millions; market share held at 40% throughout):

| Story | TAM | Revenue slice | Target margin | Cost of capital | Value/share | Class |
|---|---|---|---|---|---|---|
| Delivery Juggernaut | 5,000,000 | 25% | 45% | 9.50% | ₹150.02 | Plausible |
| Delivery Star | 5,000,000 | 22% | 35% | 9.50% | ₹93.00 | Plausible |
| Delivery Leader + Competition | 5,000,000 | 15% | 35% | 10.99% | ₹61.55 | Plausible |
| Restaurant Delivery Juggernaut + High Growth India | 3,000,000 | 25% | 45% | 9.50% | ₹94.31 | Probable |
| Restaurant Delivery Star + High Growth India | 3,000,000 | 22% | 35% | 9.50% | ₹59.02 | Probable |
| Restaurant Delivery + Competition + High Growth India | 3,000,000 | 20% | 25% | 10.99% | ₹35.52 | Probable |
| Base Case, Positive | 2,000,000 | 25% | 45% | 10.25% | ₹56.66 | Probable |
| Base Case | 2,000,000 | 22% | 35% | 10.25% | ₹39.48 | Probable |
| Base Case, Negative | 2,000,000 | 20% | 25% | 10.25% | ₹26.16 | Probable |
| Restaurant Delivery Juggernaut + Low Growth India | 1,125,000 | 25% | 45% | 9.50% | ₹36.48 | Plausible |
| Restaurant Delivery Star + Low Growth India | 1,125,000 | 22% | 35% | 9.50% | ₹24.02 | Plausible |
| Restaurant Delivery + Competition + Low Growth India | 1,125,000 | 20% | 25% | 10.99% | ₹16.58 | Plausible |

Three competing Uber narratives valued with the same machinery:

| | Uber (Gurley) | Uber (Gurley modified) | Uber (Damodaran) |
|---|---|---|---|
| Narrative | Expands the car-service market substantially, pulling in mass-transit users and suburban non-users; networking advantage gives a dominant share; keeps a 20% slice | Same expansion and dominant share, but competition cuts prices and the slice to 10% | Expands the market moderately, mainly urban; competitive advantages give a significant but not dominant share; 20% slice |
| Total market | $300 billion, growing 3%/yr | $300 billion, growing 3%/yr | $100 billion, growing 6%/yr |
| Market share | 40% | 40% | 10% |
| Revenue slice | 20% | 10% | 20% |
| Value | $53.4 billion + option value of $10 billion+ | $28.7 billion + option value of $6 billion+ | $5.9 billion + option value of $2–3 billion |

Two-way sensitivity table, Amazon, January 2000 — value per share by compounded revenue growth rate and target operating margin:

| Growth \ Margin | 6% | 8% | 10% | 12% | 14% |
|---|---|---|---|---|---|
| 30% | $(1.94) | $2.95 | $7.84 | $12.71 | $17.57 |
| 35% | $1.41 | $8.37 | $15.33 | $22.27 | $29.21 |
| 40% | $6.10 | $15.93 | $25.74 | $35.54 | $45.34 |
| 45% | $12.59 | $26.34 | $40.05 | $53.77 | $67.48 |
| 50% | $21.47 | $40.50 | $59.52 | $78.53 | $97.54 |
| 55% | $33.47 | $59.60 | $85.72 | $111.84 | $137.95 |
| 60% | $49.53 | $85.10 | $120.66 | $156.22 | $191.77 |

At a market price of $84, only the most aggressive cells reach it: 60% growth with 8% margin or better, 55% growth with 10% or better, and 50% growth with 14%. The scenario exists. The question is whether it is probable.

**Worked example:** Uber, June 2014, three narratives. Damodaran's moderate-expansion, urban, local-network story values Uber at $5.9 billion. Bill Gurley's story — a substantially larger market at $300 billion, a dominant 40% share via network effects, the 20% slice held — values it at $53.4 billion. A modified Gurley story, where competition cuts the slice to 10%, lands at $28.7 billion in between. Nothing in the model changed. Three story choices moved the value by roughly 9x.

**Determinism:**
- DETERMINISTIC: each cell's value, given its input set. Also the spread, the sort order, and the breakeven scenario that reproduces the market price.
- JUDGMENT: which dimensions to vary, what levels to define, which rows are probable versus merely plausible, and which cell is your base case. That judgment needs market-size evidence, competitive analysis and evidence of product and financial success.

**Pitfalls:**
- Presenting the range as the answer. A range with no chosen cell is an abdication.
- Averaging the cells, which invents a story nobody holds.
- Varying inputs that do not move value, producing a wide grid with no information.
- Letting the grid justify the market price by pointing to an extreme cell. There is always such a cell. See the Amazon table.
- Omitting the likelihood labels, which is what separates the Zomato grid from a wish list.
- Varying one input while leaving a linked input fixed, creating internally inconsistent cells. See [[narrative-consistency-checks]].

**Sources:**
- valpacket1spr21 p.272, p.273
- valpacket1spr20 p.268, p.269
- valuationmotleyfool p.25
- valpacket1spr21 p.307 (Amazon two-way table; there are always scenarios that justify the price)

**Related:** [[possible-plausible-probable]], [[monte-carlo-valuation-simulation]], [[narrative-to-value-drivers]], [[uber-narrative-valuation]], [[value-vs-price-gap]], [[narrative-consistency-checks]]
