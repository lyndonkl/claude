# Handling uncertainty: payback, sensitivity analysis and simulation

**Core idea:** A project's NPV rests on estimates that will all turn out wrong to some degree. Revenues may disappoint, costs may overrun, tax rates and interest rates may rise, risk premiums and default spreads may widen. Three tools of increasing sophistication respond to that. **Payback** is the crudest: how many years until the money comes back. It measures how long capital is at risk but ignores everything after the payback date. **Sensitivity analysis** recomputes the decision measure as one input varies, showing which assumptions actually matter. **Simulation** replaces point estimates with probability distributions and produces a full distribution of NPVs. None of these tools makes the decision. The expected NPV already prices risk through the discount rate, so a downside probability on its own is not a rejection reason.

**Formulas:**
- `Payback period` = the year in which cumulated undiscounted cash flow first turns positive, interpolated within that year.
- `Discounted payback` = the same, using cumulated present values.
- Sensitivity: recompute `NPV(x)` and `IRR(x)` over a grid of values for input `x`, holding others at base case.
- Simulation: draw each uncertain input from its distribution, recompute NPV, repeat many times, and report the mean, median, range, and `P(NPV < 0)`.

**Procedure:**
1. List the inputs the answer could plausibly turn on. Keep the list short — less is more, and not everything is worth varying.
2. Distinguish micro-drivers you control (renewal rates, margins) from macro drivers you do not (commodity prices, exchange rates, country risk premiums).
3. Run one-at-a-time sensitivity on those drivers over realistic ranges. Report NPV and IRR at each point. Plot the result — a picture beats a table.
4. Find the break-even value of each key driver, the level at which NPV crosses zero. That is the number a manager can actually monitor.
5. For the drivers that matter most, assign probability distributions rather than points, and simulate.
6. Read the simulation output for two things: central tendency (does the mean sit near the base case?) and downside (how often and how badly is NPV negative?).
7. Compute payback and discounted payback as a supplementary read on capital-at-risk duration. Do not let them override NPV.
8. Decide whether to hedge the macro risks, using the hedging decision tree below.

**Reference data:**

Rio Disney simulation input distributions:

| Input | Distribution | Base case |
|---|---|---|
| Actual revenues as % of forecast | Uniform(80%, 120%) | 100% |
| Park operating expenses as % of revenues | Triangular(~46%, 60%, ~74%) | 60% |
| Brazil country risk premium | Normal-shaped over ~0%–6% | 3% |

Rio Disney simulation output: mean NPV $3.40 billion, median $3.28 billion, range roughly −$1 billion to +$8.5 billion, `P(NPV < 0) = 12%`. The mean and median sit close to the $3.29 billion base case, so the base case is not optimistic — but there is a real tail.

Vale mine sensitivity to the iron ore price (base case $100/ton):

| Iron ore price | NPV (approx.) |
|---|---|
| $50/ton | −$1,150M |
| $60 | −$900M |
| $70 | −$550M |
| $80 | −$250M |
| $90 | ≈ $0 (break-even) |
| $100 | +$300M (base) |
| $110 | +$600M |
| $120 | +$900M |
| $130 | +$1,200M |

IRR climbs from deeply negative to over 30% across that range. The break-even iron ore price near $90/ton is the single most decision-relevant number in the analysis.

Vale mine sensitivity to the C$/US$ exchange rate (costs in C$, revenues in US$):

| Canadian dollar vs parity | NPV | IRR |
|---|---|---|
| 18% weaker | ≈ $640M | ≈ 23% |
| 12% weaker | ≈ $525M | |
| 6% weaker | ≈ $415M | |
| Parity (base) | ≈ $300M | ≈ 17% |
| 6% stronger | ≈ $190M | |
| 12% stronger | ≈ $80M | |
| 18% stronger | slightly negative | ≈ 10.5% |

Hedging decision tree:

| Situation | Action |
|---|---|
| Cost of hedging negligible + significant cash-flow or discount-rate benefit | Hedge |
| Cost negligible + no benefit | Indifferent |
| Cost high + no significant benefit | Do not hedge |
| Cost high + benefit + marginal investors cannot hedge more cheaply | Firm hedges |
| Investors can hedge more cheaply + benefits persist when they do | Pass the risk through to investors |
| Investors can hedge more cheaply but benefits do not persist | Firm hedges |

Three sources of hedging benefit. Cash-flow benefits: tax benefits and better project choices. Survival or truncation benefits: protection against catastrophic risk and lower default risk. Discount-rate benefits: hedging macro risk lowers the cost of equity, and lower default risk lowers the cost of debt or raises debt capacity.

**Worked example:** Rio Disney payback ($ millions, 8.46% discount rate). Cumulated undiscounted cash flow turns positive between years 10 and 11 → **payback = 10.3 years**. Cumulated discounted cash flow turns positive between years 16 and 17 → **discounted payback = 16.8 years**. The gap of 6.5 years is the cost of time, and it shows why a firm that stops at simple payback badly understates how long its capital is exposed.

Selected rows:

| Year | Cash flow | Cumulated CF | PV of cash flow | Cumulated DCF |
|---|---|---|---|---|
| 0 | −$2,000 | −$2,000 | −$2,000 | −$2,000 |
| 3 | −$267 | −$4,126 | −$210 | −$3,862 |
| 10 | $715 | −$237 | $317 | −$1,708 |
| 11 | $729 | $491 | $298 | −$1,409 |
| 16 | $805 | $4,360 | $219 | −$165 |
| 17 | $821 | $5,181 | $206 | $41 |

Netflix Fit uses the same logic on a micro driver: the base case assumes existing subscribers renew at close to 100%. A lower renewal rate cuts equipment replacement sales and subscription revenue, and the NPV falls with it. Because the stand-alone NPV is only $106 million on a $2.4 billion investment, that single assumption can flip the recommendation.

**Determinism:** DETERMINISTIC — payback, discounted payback, sensitivity tables, and break-even levels all follow mechanically from the cash flow model, a discount rate, and a grid of input values. Given input distributions and a random seed, a simulation's output statistics are reproducible. JUDGMENT — which variables to vary, over what ranges, which distribution shapes and parameters to assume, and what to do with a 12% probability of a negative NPV. That judgment needs the historical volatility of the drivers, management's risk tolerance, and the firm's capacity to absorb a bad outcome.

**Pitfalls:**
- Varying one input at a time when inputs move together in the real world. Revenue shortfalls and cost overruns are correlated.
- Producing more tables instead of better decisions. The objective is a decision, not a deliverable.
- Rejecting a project because simulation shows *some* chance of loss. The discount rate already charges for risk; double counting it in the decision rule rejects good projects.
- Filing simulation output away as due-diligence evidence without letting it change anything.
- Treating payback as a decision rule. It ignores all cash flows after the payback date and, in its simple form, the time value of money.
- Hedging a risk the firm's investors can shed more cheaply themselves.

**Sources:**
- corporate_finance--lecture_slides--cfpacket1spr20 p.254-260
- corporate_finance--lecture_slides--cfpacket1spr20 p.272-275
- corporate_finance--lecture_slides--cfpacket1spr20 p.303
- corporate_finance--case--netflixfit p.7
- corporate_finance--case--netflixfitpresentation p.3
- corporate_finance--case--netflixfitpresentation p.5
- corporate_finance--case--netflixfitpresentation p.9
- corporate_finance--case--netflixfitpresentation p.14
- corporate_finance--case--netflixfitpresentation p.21

**Related:** [[npv-and-irr-mechanics]], [[npv-vs-irr-conflicts]], [[project-options]], [[currency-and-inflation-consistency]], [[netflix-fit-case]], [[assessing-existing-investments]], [[hedging-decision]]
