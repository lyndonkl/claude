# Opportunity costs, excess capacity and cannibalization

**Core idea:** Most projects impose costs on the rest of the business that no accounting system charges to them. Three kinds recur. An **opportunity cost** arises whenever a project uses a resource the firm already owns; the resource must be priced at its next best alternative use, never at zero and never at book value. **Excess capacity** looks free because the asset is already paid for, but using it today pulls forward the date the firm must buy more capacity or cut production. **Cannibalization** is revenue the project steals from the firm's own existing products. It counts as a cost only to the extent those sales would otherwise have been kept — in a fiercely competitive market, they might have been lost to rivals anyway.

**Formulas:** Symbols: `t` = tax rate; `r` = discount rate.
- Opportunity cost via sale: `after-tax proceeds = Market value − t_capital gains × (Market value − Book value)`
- Opportunity cost via rental/lease: `PV of after-tax rental or lease revenues foregone`
- Opportunity cost via internal use: `replacement cost of the resource`
- Excess capacity, production cut: `cost = PV of after-tax cash flows on the lost sales`
- Excess capacity, earlier expansion: `cost = PV(capacity investment at the earlier date) − PV(capacity investment at the later date)`
- Side cost adjustment: `Adjusted NPV = Stand-alone NPV − PV(after-tax side costs)`, with `after-tax cost = pre-tax cost × (1 − t)`

**Procedure:**
1. Inventory every firm-owned resource the project will consume: land, buildings, equipment, capacity, management time, brand, distribution.
2. For each, identify the single best alternative use. Sale, rental, or redeployment elsewhere in the business.
3. Price it. Sale → after-tax proceeds. Rental → present value of after-tax rents. Internal redeployment → replacement cost.
4. For excess capacity, answer three questions in order. When do I run out of capacity if I do *not* add the new product? When do I run out if I *do*? What will I do when I run out?
5. If the answer to question three is "cut back production," charge the PV of after-tax cash flows on the lost sales. If it is "buy new capacity," charge the PV difference between building earlier and building later.
6. For cannibalization, estimate what share of the diverted revenue the firm would have kept in the absence of the new project. Charge only that share.
7. Convert each side cost to after-tax terms and discount at the project's rate. Subtract from the stand-alone NPV, or fold the annual after-tax amounts into the yearly cash flows. Both give the same answer.
8. Re-test the decision. A project can survive its side costs, as Bookscape Online does, or fail because of them.

**Reference data:** Pricing rules for owned resources:

| Alternative use | Opportunity cost |
|---|---|
| Sell the asset | Expected sale proceeds net of capital gains taxes |
| Rent or lease it out | Expected present value of after-tax rental/lease revenues |
| Use it elsewhere in the business | Cost of replacing it |
| No alternative use at all, now or later | Zero — but verify the "or later" |

Cannibalization judgment:

| Competitive setting | Treatment |
|---|---|
| Exclusive, differentiated product (a Disney park) | Diverted sales would have been retained → count as a full cost |
| Highly competitive market (a TV time slot) | Viewers might have gone to rivals anyway → not fully incremental |

**Worked example:** Three cases.

*1. Foregone sale — Disney Rio land.* Disney bought undeveloped land in Rio years ago for $5 million for a hotel never built. If the theme park proceeds, the land will house Disney Rio's offices. The land could be sold today for $40 million, with the gain taxed at 20%. Four tempting wrong answers: ignore it (Disney owns it), use book value ($5M), use market value ($40M), or split the difference. The right charge is the after-tax foregone sale proceeds: 40 − 0.20 × (40 − 5) = **$33 million**, charged to the theme-park project.

*2. Side costs — Bookscape Online.* The stand-alone online venture has NPV = $76,375 at an 18.12% cost of capital. Two side costs were missed. The bookstore general manager's workload rises, so his salary goes from $100,000 to $120,000 next year — an incremental $20,000 growing 5%/year for four years, reverting afterwards. And the office the venture will occupy currently stores financial records, which must move to a bank vault at $1,000/year.

| Year | Incremental salary | After-tax @40% | PV @18.12% |
|---|---|---|---|
| 1 | $20,000 | $12,000 | $10,159 |
| 2 | $21,000 | $12,600 | $9,030 |
| 3 | $22,050 | $13,230 | $8,027 |
| 4 | $23,153 | $13,892 | $7,136 |
| **Total** | | | **$34,352** |

Office cost: $1,000 × (1 − 0.40) = $600/year; PV over 4 years at 18.12% = $1,610.

Adjusted NPV = 76,375 − 34,352 − 1,610 = **$40,413**. Still positive, so the venture survives. Folding the after-tax costs into the annual cash flows (−$1,150,000; $327,400; $401,800; $432,670; $706,238) gives the identical $40,413.

*3. Excess capacity — Vale.* Vale will route the new mine's output through its existing distribution system. The mine manager argues there is no cost: the system is already paid for and cannot be sold or leased to a competitor. That is a sunk-cost argument wearing a different hat. "Already paid for" says nothing about the future. Run the three questions: when does the system fill up without the mine, when does it fill up with the mine, and what happens then? If Vale must expand two years earlier, the cost is the PV difference between the earlier and later expansion.

*4. Cannibalization — Rio Disney and ABC.* If 20% of Rio Disney's revenues come from people who would otherwise have visited Disney's US parks, count only the 80% as incremental, because a Disney park is exclusive and those visitors were not going elsewhere. Now consider a new Disney cable channel show drawing 20% of its viewers from ABC, also Disney-owned. Television is fiercely competitive, and those viewers might have drifted to rivals regardless, so the same 20% is not fully a cost.

*5. Excess capacity — Netflix Fit.* The Mumbai studio is 40% used next year by Asian entertainment content, which grows 20% a year. Netflix Fit would take another 30% of capacity. Free today, but the combined usage hits 100% sooner, triggering a new studio costing $500 million (growing with inflation). In the case solution the trigger lands in year 4 at $520.30 million, with the offsetting saving of the *deferred* investment credited later.

**Determinism:** DETERMINISTIC — once the alternative use is chosen, the opportunity cost is a closed-form computation from book value, market value, and tax rate. Given a capacity-exhaustion date and a response, the excess-capacity cost is a PV difference. Given a cannibalization share, the revenue adjustment is arithmetic. JUDGMENT — identifying the best alternative use, forecasting when capacity runs out and how the firm will respond, and estimating what share of cannibalized sales would truly have been kept. That judgment needs the resale market for the asset, the capacity growth path of competing uses, and the competitive structure of the affected product market.

**Pitfalls:**
- Ignoring an owned resource because "we already have it."
- Charging book value instead of the after-tax value of the foregone alternative. Disney's land is worth $33 million to the project, not $5 million.
- Charging *gross* market value and forgetting the capital gains tax.
- Accepting "it's already paid for and nobody else wants it" as proof that excess capacity is free.
- Counting all cannibalized revenue as a cost in a competitive market where those sales were at risk anyway.
- Adding side costs twice, once inside the cash flows and again as a lump-sum PV deduction.

**Sources:**
- corporate_finance--lecture_slides--cfpacket1spr20 p.305-308
- corporate_finance--lecture_slides--cfpacket1spr20 p.310-315
- corporate_finance--case--netflixfit p.4
- corporate_finance--case--netflixfitpresentation p.10-11

**Related:** [[incremental-cash-flow-principle]], [[project-synergies]], [[npv-and-irr-mechanics]], [[earnings-vs-cash-flows]], [[project-hurdle-rate-selection]], [[netflix-fit-case]], [[capital-budgeting-model]]
