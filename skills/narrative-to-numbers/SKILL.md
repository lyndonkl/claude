---
name: narrative-to-numbers
description: Builds the business story behind a valuation and connects it to the drivers that carry value — market size, growth, margin, reinvestment efficiency and risk. Tests a narrative as possible, plausible and probable, and keeps the feedback loop open. Use when starting a valuation, writing the story behind a company, setting growth or margin assumptions, sanity-checking a story against its numbers, choosing a target margin or sales-to-capital ratio, or when a valuation needs a defensible reason for its inputs.
---

# Narrative to numbers

A story without numbers is a fairy tale. It cannot be wrong, so it cannot be tested, and
it never tells you what price to pay. Numbers without a story are a spreadsheet nobody
believes. Every input came from somewhere, but nobody can say where, so any reader who
disagrees has nothing to argue with except the answer.

The bridge between them is a mapping rule, and it runs both ways:

- Every claim in the story moves **exactly one** driver in the model.
- Every input in the model carries **one sentence** of story.

Two counts prove the bridge holds. Model inputs with no story sentence: zero. Story claims
with no driver: zero. Both counts are mechanical, and the second one is where most
valuations fail — a claim that moves no driver is decoration, and a claim that moves two
is double counted.

This skill owns stages S1, S2, S11 (the driver choices) and S18 of
`knowledge/frameworks/intrinsic-valuation-playbook.md`. It produces `03-narrative/narrative.md` and
`03-narrative/drivers.json`.

## The sequence

```
1. Survey the landscape     business map + base-year numbers + benchmarks
2. Write the narrative      prose, spreadsheet closed
3. Test it                  possible / plausible / probable, then the three screens
4. Connect to drivers       each claim -> one payload field
5. Value it                 dcf-valuation-engine, then the consistency validator
6. Keep the loop open       counter-narratives now, break/shift/change later
```

The order is binding. Starting at step 4 with a template of inputs and inventing a story
afterwards produces a rationalisation, not a valuation. No downstream check can detect it,
because the numbers will be internally consistent with each other and with nothing else.

Before step 1, run the bias audit. Name who pays for this valuation, what answer they
want, what public position you already hold, and whether you have seen the market price.
Do the qualitative work before looking at price. If you have already seen it, treat it as
an anchor to argue against, never toward.

---

## Step 1 — Survey the landscape

The output is not numbers. It is a business-model map plus the benchmarks that tell you
what is normal in this business. Those benchmarks are what stop the story from drifting.

Map the business as a loop in about six boxes: suppliers, customers, who sets price, what
slice the firm keeps, what it must invest in to grow, what it spends to get there. For
Uber in 2014 those six boxes were drivers, riders, surge pricing, payment through the app,
the 20% slice, and technology as the only real reinvestment. Each box became a driver.

The numeric half belongs to other skills. `financial-statement-normalization` produces
trailing-twelve-month revenue and EBIT, capitalizes leases and R&D, and rebuilds invested
capital. Read its output, not the raw filing. A base year with R&D still expensed
understates both EBIT and invested capital, so the margin and the ROIC you benchmark
against the industry are both wrong.

Benchmark three things against the industry and against the largest incumbents: revenue
growth, pre-tax operating margin, and sales-to-capital or ROIC. For a company claiming it
will become the largest player in its business, look at what the largest players actually
earn. Global automakers earn 0.3% to 8.5% operating margins. A 16% target margin for a car
company is a claim about the world, not a rounding of the industry median.

Read the quarterly trend as evidence that a claimed inflection has started. Do not
extrapolate it. Momentum is not a narrative.

---

## Step 2 — Write the narrative

Write it in prose with the spreadsheet closed. Three rules: keep it simple, keep it
focused, stay grounded in reality. If it does not fit in a paragraph, you do not have a
narrative yet.

A narrative has to constrain something. "Uber is a technology company" rules nothing out
and sets no driver. Compare it with this. Uber is an urban car-service company. It expands
the car-service market moderately, holds a 20% slice against competition, benefits from
local rather than global network effects, and owns no cars. That version fixes five drivers
and can be shown wrong on any of them.

Give the narrative a title that states the bet. Damodaran's Tesla story is titled "The
Payoff to Flexibility — A Plausible Path to Auto Dominance", and the word *plausible* in
that title is doing real work. It says which grade the story earns before anyone reads it.

Then break the prose into discrete claims. One market, one capability, one margin path per
claim. The claim list is the input to step 3.

---

## Step 3 — Test it

Two tests run here, and they catch different things.

**The grading ladder** sorts each claim by how confidently you can assign a probability,
and routes it to the matching device.

| Grade | Definition | Where it goes | What promotes it |
|---|---|---|---|
| Probable | expected, with evidence — product success, financial results | base-year numbers and expected cash flows | — |
| Plausible | a reasoned argument, no tangible evidence yet | a higher expected growth rate inside the DCF | product success, financial results |
| Possible | the probability cannot be assessed at all | option value, added on top of the DCF, once | market-potential evidence, product testing |

"Possible" does not mean unlikely. It means unassessable, which is why it gets a
different tool. A claim is routed exactly once. A market counted in revenues may not also
be counted as option value.

Write down the promotion trigger for every claim now. Step 6 has nothing to watch for
otherwise.

**The three screens** test the finished set of claims against arithmetic, economics and
business reality. The impossible is never allowed. The implausible needs extraordinary
justification. The improbable is the dangerous class: each assumption looks fine alone,
and together they contradict how business works.

Full screen list, the aggregation test for a crowded market, and the growth/risk/
reinvestment triangle: `resources/narrative-tests.md`.

---

## Step 4 — Connect the narrative to the drivers

This is the bridge itself. The value chain is fixed:

```
total market x market share = revenues
revenues - operating expenses  = operating income
             - taxes           = after-tax operating income
             - reinvestment    = free cash flow to the firm
```

Those cash flows are then adjusted for time and operating risk through the discount rate,
and for survival through a probability of failure.

Each claim maps to exactly one field in the `dcf-valuation-engine` payload. This table is
the working core of the skill.

| Narrative claim is about | Driver | Payload field |
|---|---|---|
| Market definition, market size, how fast that market grows | Total market | `base_revenue` plus `revenue_growth` (see the conversion below) |
| Competitive position, network effects, the share the firm attains | Market share | `revenue_growth` |
| The slice of the transaction the firm keeps | Revenue slice | `revenue_growth` (it scales the revenue path) |
| Pricing power, cost structure, scale economies | Operating margin | `operating_margin`, as a glide to the target |
| How long until the target margin is reached | Margin convergence | `operating_margin.converge_by` |
| Capital intensity: asset-light or asset-heavy | Reinvestment efficiency | `sales_to_capital` |
| Tax domicile, tax migration, accumulated losses | Tax | `tax_rate`, `net_operating_loss_carryforward` |
| Business maturity, operating risk, country exposure | Discount rate | `cost_of_capital`, `terminal.cost_of_capital` |
| How long the moat holds off competition | Length of the growth phase | `forecast_years`, and each `converge_by` |
| Whether excess returns survive in perpetuity | Terminal excess return | `terminal.return_on_capital` |
| The economy-wide ceiling on perpetual growth | Terminal growth | `terminal.growth_rate` |
| Whether the business can fail outright | Survival | `failure.probability`, `failure.proceeds_basis`, `failure.proceeds_percent` |
| Debt, cash, minorities, holdings, options, share count | Bridge | `bridge.debt`, `bridge.cash`, `bridge.minority_interests`, `bridge.non_operating_assets`, `bridge.employee_options_value`, `bridge.shares_outstanding` |
| A market you cannot assign a probability to | None — the option layer | Not in this payload. Value it with `option-valuation-toolkit` and add it once, after the DCF |

**The market-and-share conversion.** The engine takes a revenue path, not a market and a
share. Do the multiplication yourself, then hand over the growth rate:

```
target revenue_N = total market_N x market share_N x revenue slice
revenue_growth   = (target revenue_N / base_revenue)^(1/N) - 1
```

Keep the market, the share and the slice in `drivers.json` as the story record, because
they are the numbers a reader will argue with. The growth rate is what the engine consumes.
Set the growth lever from an end-state revenue level, never from a rate you like the look
of. That forces you to look at absolute dollars in year N and ask who loses that revenue.

**Every lever gets a reference class.** A target margin picked against the auto industry
median of 3.01%, the technology median of 10.25% and the software median of 21.24% is a
choice you have to defend. A target margin picked from nowhere is a number nobody can
argue with. The lever menus Damodaran uses, and the terminal defaults with the argument
each override requires: `resources/driver-mapping.md`.

**Write the story link on every row.** A row with no link is deleted, or the missing claim
is found. That single discipline is what the whole skill exists to enforce.

### The artifact

`drivers.json` carries the `dcf-valuation-engine` payload, plus two blocks that keep the
bridge auditable:

```json
{
  "base_revenue": 46848, "base_ebit": 5650.4, "base_invested_capital": 27818.4,
  "forecast_years": 10,
  "revenue_growth": {"start": 0.35, "end": 0.0156, "converge_by": 10},
  "operating_margin": {"start": 0.1206, "end": 0.16, "converge_by": 5},
  "sales_to_capital": 4.0,
  "tax_rate": {"start": 0.1199, "end": 0.25, "converge_by": 10},
  "cost_of_capital": {"start": 0.06, "end": 0.0606, "converge_by": 10},
  "terminal": {"growth_rate": 0.0156, "cost_of_capital": 0.0606,
               "return_on_capital": 0.15},
  "failure": {"probability": 0.0},
  "bridge": {"debt": 10158, "cash": 16095, "shares_outstanding": 1123,
             "current_price": 1200.00},
  "currency": "USD",

  "story_links": {
    "revenue_growth": "EV market growth plus Tesla's early-mover advantage",
    "operating_margin": "continued economies of scale and brand",
    "sales_to_capital": "capacity already built, so less reinvestment in the near years",
    "terminal.return_on_capital": "cost of entry will limit competition"
  },
  "claim_ledger": [
    {"claim": "...", "grade": "probable", "driver": "operating_margin",
     "promotion_trigger": "..."}
  ]
}
```

`currency` must match the cost-of-capital artifact. The validator checks it, and a currency
mismatch is the most common silent error in DCF work.

---

## Step 5 — Value it

The arithmetic belongs to the engine. Hand it the payload:

```bash
python3 <skills>/dcf-valuation-engine/resources/dcf.py value --in drivers.json > dcf-result.json
```

Then run `valuation-consistency-checks` before reading the answer. It re-runs the
impossible screens mechanically on the finished model, checks that the terminal
reinvestment rate equals `g / ROC`, and flags a terminal return on capital above the
terminal cost of capital. Fix the offending input, not the output, and re-run.

Two diagnostics decide whether the story survived contact with the arithmetic:

- **Marginal ROIC** over the forecast. Tesla's 4.00 sales-to-capital against an auto median
  of 1.37 implies a marginal ROIC of 51.66%. That is a claim about a permanent advantage,
  and it has to be argued in the prose or the ratio has to come down.
- **Terminal excess return**, `terminal.return_on_capital` minus `terminal.cost_of_capital`.
  Anything above zero claims a moat that survives forever. Name the moat or set them equal.

Then convert the point estimate into a range. Use a scenario grid when the doubt is about
*which* story, and `monte-carlo-valuation` when it is about *how much*. Label every row
possible, plausible or probable, and name the cell you actually believe. A range with no
chosen cell is an abdication. A range with no likelihood labels is a wish list.

Finally, run `implied` backwards against the market price. "The stock is worth $571 and
trades at $1,200" invites an argument about your assumptions. "At $1,200 the market assumes
a margin no firm in this industry has sustained" is a claim about the world, and it is
checkable. Ask whether that assumption is probable, not whether it is possible. Some
scenario always justifies any price.

---

## Step 6 — Keep the feedback loop open

A narrative is a working hypothesis, not a position. Two habits keep it honest.

**Value the counter-narratives.** Ask what would have to be true for a much higher value,
and for a much lower one. Then run the alternative story through the same model, changing
only the drivers that story changes. Knowing what someone else's story is worth beats
knowing that you disagree with it. Damodaran valued Uber at $5.9bn and Bill Gurley at
$53.4bn, and the counter-narrative run showed the entire gap living in three drivers:
market size, market share and the revenue slice. Nothing else was in dispute.

**Classify the news when it arrives.** That diagnosis is the only one that matters.

| Change | What happened | Response | Tool |
|---|---|---|---|
| Break | events end the story — legal, political, competitive, default | existing cash-flow, growth and risk estimates stop being operative | probability of the break, times its consequences |
| Shift | the business model improves or deteriorates; market size, share or margin move | revise those drivers and re-run | scenario grid or simulation |
| Change | unexpected entry into or exit from a market | redo the valuation on new market potential | real options |

Treating a break as a shift keeps the model running on a business that no longer exists.
Treating a shift as a break abandons a valuation over one bad quarter.

Re-grade the claim ledger against the promotion triggers written at step 3. A promotion
from possible to plausible moves a market out of the option layer and into the growth rate,
and the value moves with it.

Two disciplines close the loop. Revise on business news, never on price moves — price
moving against you is not information about the business. And count your revisions in both
directions over time. They should be roughly symmetric. A one-sided revision record is
evidence of a biased process, not of bad luck.

Re-enter the pipeline at the stage that owns the change, not at the top. A margin
re-estimate re-runs the forecast onward. A classification change re-runs everything.

---

## The failure gallery

Three ways a narrative goes wrong, each with a different tell and a different defence.
Detail, tables and the full cases: `resources/failure-gallery.md`.

**The runaway story.** A charismatic narrator, plus a disliked status quo being disrupted,
plus a claimed societal benefit. Once all three are present the questions stop, because
the answers might put the story at risk. Theranos was valued at $9 billion in October 2015.
Its board held two former Secretaries of State, a Senate Majority Leader, two generals and
exactly one person with a medical background. Prestigious, and irrelevant to whether a drop
of blood can run 200 tests. No discount rate saves you here. The claim was in the
impossible class, and the only defence was refusing to let the story stop the questions.

**The big market delusion.** Every company chasing a huge market can be individually
defensible and collectively impossible. Aggregate the revenue each company's price
requires, and the total exceeds any plausible size for the market. In 2015 the implied 2025
online-advertising revenue across twenty-one companies came to about $522 billion, against
$146.6 billion of actual revenue at the time. Not one of those valuations looked silly
alone. This failure is invisible from inside a single valuation, so run the aggregation
test whenever your company is one of many chasing one market.

**The improbable but not impossible case.** A mid-2013 sell-side model took Tesla from
24,298 vehicles to 1,137,780, expanded the EBIT margin from 1.8% to 15.3%, and held capital
spending at 3% of sales with negative working-capital changes. Every line is arguable on
its own. Together they claim enormous growth, expanding margins and almost no reinvestment
at the same time. No screen for the impossible catches it. The triangle does.

---

## Common failures

| Symptom | Cause |
|---|---|
| The story reads as unarguable | It constrains no driver. Rewrite until a claim can be shown false |
| Value moves hundreds of dollars a share on one input | Normal for a growth company. Say so, and show the grid |
| A claim shows up in both growth and option value | Double counted. Route each claim once |
| Terminal ROC left above terminal cost of capital | A perpetual moat granted by default. State it or set them equal |
| Sales-to-capital far above the industry | Growth assumed to be nearly free. Check marginal ROIC |
| The range spans 100x with no chosen cell | A grid without a base case is an abdication |
| The narrative changed after the price moved | Herding with extra steps. Revise on business news |
| An input nobody can explain in a sentence | Delete it or find the claim behind it |

## Reference files

- `resources/narrative-tests.md` — the grading ladder, the impossible/implausible/improbable
  screens, the growth/risk/reinvestment triangle, the sector aggregation test.
- `resources/driver-mapping.md` — every lever with its reference menu, the end-state revenue
  method, terminal defaults and what overriding each one requires.
- `resources/failure-gallery.md` — Theranos, the online-advertising aggregation table, the
  improbable Tesla sell-side model, and the Amazon breakeven grid.
- `resources/worked-examples.md` — Uber June 2014 and Tesla November 2021, end to end.

## Related

`company-classification-routing` fixes the life-cycle stage and constraint set this skill
inherits. `financial-statement-normalization` produces the base year. `dcf-valuation-engine`
runs the arithmetic. `valuation-consistency-checks` gates the result.
`valuation-red-team` attacks the finished story. `monte-carlo-valuation` and
`option-valuation-toolkit` handle the uncertainty and the option layer.

Deeper background: `knowledge/concepts/narrative-numbers/` for all nineteen concept notes, and
`knowledge/frameworks/intrinsic-valuation-playbook.md` stages S1, S2, S11, S16 and S18.
