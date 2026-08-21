---
name: valuation-red-team
description: Attacks a finished valuation the way a skeptical reviewer would — hunts bias and verdict-first reasoning, checks that each risk is charged exactly once, tests whether growth is paid for, interrogates terminal value, reverse-engineers what the market price already assumes, and applies the seven deadly sins of acquisition analysis. Use when reviewing a completed valuation, red-teaming or challenging assumptions before acting on a number, auditing a DCF someone else built, or checking double counting, control premiums, synergy claims, comparable sets and route constraints.
---

# Valuation red team

This is the adversarial pass. Someone has produced a value per share. Your job is to find
the places where that number is not supported by the work behind it, and to say so in a
form the owning agent can act on.

Three rules define the role.

**You raise findings. You do not edit.** Every artifact has exactly one writer, and it is
not you. A disagreement travels as a finding with evidence and a suggested fix. If you
correct the number yourself, nobody can tell later whether the model was fixed or the
critic was.

**The burden of proof sits on the number.** You are not required to produce a better
valuation before you may reject this one. A claim with no evidence behind it is a finding,
whoever made it.

**Attack the input, never the output.** "Value is too high" is not a finding. "Terminal
return on capital sits 4 points above the terminal cost of capital and the write-up names
no barrier to entry" is.

## Before you start

You need the artifacts the analysis produced. At minimum: `classification.json`,
`cost-of-capital.json`, `forecast.json`, `dcf-result.json`, and the prose files that carry
the argument. In `acquisition`, `restructuring` and `ipo` modes you also need the stage
artifacts for those paths.

If gate `G6_valued` has not passed there is no equity value to attack. Return a `blocked`
status naming the artifact you are missing. Do not review a half-built model and grade it
as if it were finished.

Read `classification.json` first. The route decides which attacks apply and which are
irrelevant. Running the growth-reinvestment attack on a bank valued by excess return
wastes both your time and the analyst's.

## Step 0 — run the mechanical gate before you read anything

```bash
python3 <skills>/valuation-consistency-checks/resources/validate.py \
  --mandate mandate.json --classification classification.json \
  --capital capital.json --forecast forecast.json --dcf dcf-result.json --json
```

That script tests currency agreement, the terminal identities, capital weights, beta range,
the growth reconciliation, the equity bridge arithmetic, value per share, tax rates and
three constraint rules. It is free and it is deterministic. Start there so your reading
time goes to the things a script cannot see.

Convert its output as follows.

| Validator result | Becomes |
|---|---|
| `ERROR` | a `high` finding, quoting the check name and the two numbers that contradict |
| `WARN` | a `medium` finding, unless the write-up already carries a written defence |
| `INFO` | nothing; do not report checks that passed |
| `SKIP` | investigate — a missing file reads exactly like a clean pass |

The `SKIP` lines matter more than they look. A path typo makes the gate exit 0 with almost
every check unrun. Confirm each artifact you passed actually exists before you trust the
exit code.

## The attack sequence

Work these in order. Early attacks invalidate later ones: a route violation makes the
growth arithmetic moot, so there is no point pricing the terminal value of a model that
should never have been built.

| # | Attack | Default severity | Detail |
|---|---|---|---|
| A1 | Route conformance against the compiled constraints | high | [constraint-conformance.md](resources/constraint-conformance.md) |
| A2 | Bias — did the conclusion precede the analysis | medium to high | [bias-diagnostics.md](resources/bias-diagnostics.md) |
| A3 | Single charge per risk | high | [single-charge-register.md](resources/single-charge-register.md) |
| A4 | Growth must be paid for | high | this file, plus the register |
| A5 | Terminal value plausibility | high | this file |
| A6 | The equity bridge and the double-count register | high | [single-charge-register.md](resources/single-charge-register.md) |
| A7 | The implied-expectations attack | medium to high | [implied-expectations.md](resources/implied-expectations.md) |
| A8 | Comparable-set and pricing-route bias | medium to high | [comparable-set-bias.md](resources/comparable-set-bias.md) |
| A9 | The seven sins of acquisition analysis | high | [seven-sins-audit.md](resources/seven-sins-audit.md) |
| A10 | Narrative-to-number traceability | medium | this file |
| A11 | Uncertainty and the closing claim | medium | this file |

---

### A1 · Route conformance

**What to check.** Every rule in `classification.json.constraints` is a predicate over the
produced artifacts. Test each one. A constraint the diagnostician compiled and nobody
honored is the most expensive error in this domain, because the machinery that ran was
never valid for this company.

**How.** The validator enforces `no-fcff-valuation`, `require-failure-probability` and
`no-earnings-multiple` mechanically, and it needs a `method` field on the DCF artifact to
do the first one. The remaining rules you test by reading, using the predicate table in
[constraint-conformance.md](resources/constraint-conformance.md). That file carries all 28
rules from the routing framework with the artifact and field each one reads.

**Failure looks like.** A bank carrying a WACC and an enterprise value. A price-earnings
multiple applied to a trough year. An optimal-debt-ratio schedule run on an insurer. A
total beta paired with a diversified acquirer. An illiquidity discount applied to an IPO. A
terminal value set by an exit multiple.

**Severity.** High, without exception. A route violation does not degrade the answer, it
voids it.

---

### A2 · Bias

**What to check.** Whether the number was chosen before the model was built. This is the
sin that hides every other sin, because a fitted model passes consistency checks.

**How.** Reconstruct the chronology from the artifacts and their sequence. Compare each
driver against its sector benchmark and note which direction the deviations run. Count the
inputs that carry a story sentence. Run the implied-expectations solve described in A7 and
see how close the base case sits to the market price. Full diagnostic set in
[bias-diagnostics.md](resources/bias-diagnostics.md).

**Failure looks like.** Every driver sits at the favourable end of its plausible range, and
the deviations all point the same way. The value lands within a whisker of the price on a
company nobody claims is fairly valued. The write-up describes assumptions as
"conservative" without naming a number. A range is reported with no designated base cell.

**Severity.** Medium when the pattern is one-sided but each input is individually
defensible. High when the chronology shows the price came first, or when a driver was
demonstrably moved to reach a target.

---

### A3 · Single charge per risk

**What to check.** Each risk is priced exactly once. This is the audit that pays best,
because every one of its failures is the same error wearing a different costume, and each
one is quietly worth a lot of value.

**How.** Build the register: one row per risk, one column per channel it could have entered
through. Fill it by reading `cost-of-capital.json` for premiums, `forecast.json` for
haircuts and probability weights, and `dcf-result.json` for outer adjustments and bridge
discounts. Any row with two marks is a finding. The full risk list, the channels each risk
can legitimately use, and the correct channel to keep are in
[single-charge-register.md](resources/single-charge-register.md).

**Failure looks like.** A country risk premium in the cost of equity, plus a nationalization
scenario, plus a governance discount — three charges for overlapping risks. A failure
probability applied alongside a distress-adjusted discount rate. A total beta paired with an
illiquidity discount with no overlap argument. Weak governance modelled as a discount-rate
bump rather than as low returns on capital and a low probability of change.

**Severity.** High. The routing framework carries `single-charge-per-risk` as a universal
constraint, so a double charge is also a route violation.

---

### A4 · Growth must be paid for

**What to check.** Growth is bought with reinvestment at a return. The identity is
`g = reinvestment rate × return on capital` in every explicit year, and
`reinvestment rate = g / ROC` in the terminal year. Growth and reinvestment are one
decision. Setting them separately asserts a return on capital nobody examined.

**How.**

1. The validator's `growth_reconciliation` check reports the widest gap between revenue
   growth and the growth the reinvestment supports. It warns above 2 points.
2. Recompute marginal return on invested capital yourself from the forecast rows in
   `dcf-result.json`: the change in after-tax operating income across the forecast divided
   by the change in invested capital. Compare it against what the best firms in the sector
   earn.
3. Check the sales-to-capital ratio in `forecast.json` against the industry average bundled
   with `cost-of-capital-toolkit` in `resources/data`. A ratio far above the industry is an
   explicit claim that growth is nearly free.
4. Confirm the three matched pairs are not mixed. Operating income pairs with the
   reinvestment rate and return on capital. Earnings per share pairs with the retention
   ratio and return on equity. Crossing them is a silent error.

**Failure looks like.** Revenue growing much faster than the capital base with no
efficiency argument and no stated stop date. Marginal return on capital above anything the
sector has achieved. A sales-to-capital ratio taken from a different business. An
efficiency-growth term applied in every year rather than once across a transition.

**Severity.** High when the terminal identity breaks or when marginal return on capital is
implausible. Medium when only the forecast years drift and the write-up is silent.

---

### A5 · Terminal value plausibility

**What to check.** Most of the value usually sits here. Six tests, in order of how cheap
they are to run.

| Test | Predicate | Severity if it fails |
|---|---|---|
| Growth cap | terminal growth ≤ riskfree rate in the valuation currency | high |
| Finite perpetuity | terminal cost of capital strictly above terminal growth | high |
| Earned growth | terminal reinvestment rate equals `g / ROC` exactly | high |
| Named moat | terminal return on capital above terminal cost of capital only with a stated barrier and its expected life | high |
| Mature inputs | beta near 1.0, debt ratio at the industry level, country premium faded, tax at the marginal rate | medium |
| Horizon | terminal value below roughly 90% of total value, or a forecast long enough to reach maturity | medium |

**How.** The validator covers the first three and flags the fourth and sixth. Read
`forecast.json`'s terminal block for the fifth. Then run the reverse consistency check by
hand: the embedded reinvestment rate is `1 − FCFF_terminal / after-tax EBIT_terminal`, and
the implied perpetual return on capital is `g` divided by that. Never accept a valuation
whose implied perpetual return nobody looked at.

**Failure looks like.** A high-growth beta or debt ratio left standing in the terminal
year. A country risk premium held at crisis levels forever. Terminal return above the
terminal cost of capital by spreadsheet default. Terminal capital spending grown from year
N instead of back-solved from the reinvestment rule.

---

### A6 · The bridge and the double-count register

**What to check.** The walk from operating assets to value per share, and then the register
of things that get charged or credited twice. Most disputes between competent analysts
happen here rather than in the forecast.

**How.** The validator recomputes the bridge and the per-share division. Then work the
sixteen-row double-count register in
[single-charge-register.md](resources/single-charge-register.md) as a checklist. Each row
names where the double count hides and which side to delete.

**Failure looks like.** Option value subtracted and diluted shares used in the same
division. Minority interests carried at book. Brand value added on top of margins that
already reflect the brand. Goodwill added as an asset. Cash added back while interest
income is still inside the cash flows. Pension underfunding counted as debt in the weights
and subtracted again in the bridge.

**Severity.** High for arithmetic that does not tie, and for any double count large enough
to move the verdict. Medium for a double count that is real but immaterial — say so, and
say how much it is worth.

---

### A7 · The implied-expectations attack

**What to check.** What the market price already assumes, and whether the analyst's own
drivers survive being read backwards.

**How.** Run the `implied` subcommand with the market price as the target:

```bash
python3 <skills>/dcf-valuation-engine/resources/dcf.py implied --in solve.json
```

The payload takes `base_case` (the analyst's own driver set), `path` (a dotted path to the
driver that carries the story, such as `operating_margin.end` or `terminal.growth_rate`),
`target_value_per_share` set to the market price, and a `low`/`high` bracket. Then locate
the solved number in the sector distribution with `relative-valuation-toolkit`.

Procedure and worked forms are in
[implied-expectations.md](resources/implied-expectations.md), including the market-implied
probability of management change for restructuring mandates.

**Failure looks like.** Two different findings, and they point in opposite directions.

- *Against the model.* The analyst's own drivers imply a market share above 100%, a revenue
  number in year 10 that no competitor is losing, or a margin the sector has never
  sustained. That is a high finding.
- *Against the thesis, not the model.* The price implies something extreme and the write-up
  never says so. The verdict then rests on an unstated disagreement with the market. That
  is a medium finding, and the fix is a sentence, not a number.

Some scenario always justifies any price. The question is never whether a story exists but
whether it is probable.

---

### A8 · Comparable-set and pricing-route bias

**What to check.** A relative valuation runs in every mode, and it is the easiest place to
reverse-engineer a conclusion. A peer set assembled after the target price can justify
almost any number.

**How.** Rebuild the peer statistics with `relative-valuation-toolkit`. The `peer-stats`
subcommand reports the median, the quartiles, the skew and the count of firms dropped from
the sample. The `locate` subcommand places a multiple inside the bundled current
distribution. The `regress` and `predict` subcommands test whether the fitted equation is
strong enough to act on. Then check the multiple against the forbidden list for this route,
which is tabulated in [comparable-set-bias.md](resources/comparable-set-bias.md).

**Failure looks like.** A peer set of six firms with the drop-outs undocumented. Means used
where medians belong, on a distribution that is always right-skewed. A fixed threshold
applied across years or regions. A United States regression applied to a firm that operates
elsewhere. One company-wide multiple used across divisions with different economics. A
price built off precedent transactions, which is a sample of overpayments.

**Severity.** Medium in general. High when the multiple is on the forbidden list for the
route, or when the peer set was assembled after the price was known.

---

### A9 · The seven sins of acquisition analysis

**What to check.** In `acquisition`, `restructuring` and `ipo` modes, run the seven-sin
scorecard before anything else in this section. Set the prior first: acquirers usually
destroy value, and the failure is structural. The burden of proof belongs on the deal.

| Sin | The input it corrupts | Test |
|---|---|---|
| 1 Risk transference | discount rate | is the target discounted at its own cost of equity |
| 2 Debt subsidy | cost of capital | is the target's own debt capacity and cost of debt used |
| 3 Auto-pilot control | price | is the premium derived as restructured minus status quo |
| 4 Elusive synergy | cash flows and growth | does every claimed benefit map to one valuation input with a number and a date |
| 5 It's all relative | price and terminal value | is the price off precedent deals, or the terminal value an exit multiple |
| 6 Verdict first | everything | did the valuation post-date the price |
| 7 It's not my fault | delivery | is a named person accountable for the promised benefits |

**How.** Rebuild the target's own rate with `cost-of-capital-toolkit` and quantify the
transfer that the acquirer's rate creates. Re-run the synergy schedule with
`project-investment-analysis`, using `synergy` for the value and the ceiling price, and
`synergy-haircut` for what the post-merger evidence says will actually arrive. Confirm all
four numbers exist and that the acid test was applied to the one matching the stated
motive. Detail, including the four numbers and the acid test, is in
[seven-sins-audit.md](resources/seven-sins-audit.md).

**Failure looks like.** The acquirer's cost of capital on the target's cash flows. A fixed
percentage control premium. A synergy baseline built on the status quo target rather than
the restructured one, which counts control gains twice. Earnings accretion cited as a deal
test, when accretion is guaranteed whenever the acquirer's price-earnings ratio is higher.

**Severity.** High for sins 1 through 5, because each mis-states a number. High for sin 6
when the chronology shows the price came first. Medium for sin 7.

---

### A10 · Narrative-to-number traceability

**What to check.** Two counts that should both be zero: model inputs with no story
sentence, and story claims with no driver. Then the routing of each claim.

**How.** Read `narrative.md` and `drivers.json` against `forecast.json`. Confirm each claim
was routed exactly once. Probable claims belong in the base-year numbers and expected cash
flows. Plausible claims belong in the growth rate. Possible claims belong in option value
on top of the model, and nowhere else.

Where several firms chase one market, run the aggregation test. Impute each competitor's
breakeven revenue in a common year, multiply by its share of revenue from that market, and
sum. Implied market shares across the sector cannot exceed 100%.

**Failure looks like.** A market counted in the revenue path and again as option value. A
driver with no sentence behind it. A claim in the prose that moves no input, which is
decoration. An implied sector total above any credible market forecast.

**Severity.** Medium. High when a possible claim entered the cash flows and the option
layer at once, because that is a double count with a number attached.

---

### A11 · Uncertainty and the closing claim

**What to check.** Whether the point estimate was honestly converted into a range, and
whether the gap was converted into an actionable claim.

**How.** Confirm the sensitivity grid varies the two drivers that actually move value for
this route. Confirm each scenario row carries a likelihood label and that one cell is
designated the base case. Confirm the market price is located inside the distribution
rather than compared to the mean. If the analyst supplied no distribution, rebuild one with
`monte-carlo-valuation` using `simulate`, and check whether the price sits near the median.
A price near the median means the market is inside the uncertainty band and there is no
edge to act on.

Then check the closing claim. A gap needs a closing mechanism and a horizon. Margin of
safety should be widest exactly where the routing was hardest — young, distressed and
emerging-market cases.

**Failure looks like.** A point estimate quoted to the cent. A range with no chosen cell. A
gap presented as a trade with no catalyst named. A DCF value averaged with a
multiple-based price into a single number.

---

## The severity model

Three levels, and each carries a different obligation.

| Severity | Meaning | What it triggers |
|---|---|---|
| `high` | an internal contradiction, a route violation, or a claim with no evidence that moves the verdict | blocks the verdict; gate `G7_challenged` does not pass until the finding is resolved or explicitly disclosed |
| `medium` | defensible but unstated; the model is making a claim nobody wrote down | owes a written defence in the owning artifact, or a fix |
| `low` | noted for the record; does not change the number materially | nothing beyond being recorded |

Use `high` when there is no assumption set under which both halves of the contradiction are
true at once. Terminal growth above the riskfree rate is not aggressive, it is inconsistent
with the rate already chosen. Use `medium` when the model is possible but silent. The right
response there is usually a sentence in the write-up, not a change to the numbers.

Resist severity inflation. A challenge file where everything is high tells the orchestrator
nothing about what to fix first, and it burns the loopback budget on cosmetics.

**The loopback rule.** A high finding reopens the owning stage and its dependents. The cap
is two loopbacks per stage. On the third, the finding is disclosed in the report as an
unresolved risk rather than looped again. Write findings knowing this: a high finding you
cannot state precisely enough to fix will simply consume two re-runs and then appear in the
report anyway.

## The findings shape

You write two artifacts and nothing else: `challenge.json` and `challenge.md`.

`challenge.json` carries a `findings` array. Every finding has these five keys.

| Key | Contents |
|---|---|
| `id` | stable within this run, `F1`, `F2`, … The orchestrator tracks it in `state.json.open_findings` |
| `severity` | `high`, `medium` or `low` |
| `target_stage` | the stage that owns the artifact the fix belongs in |
| `claim` | one sentence stating the defect, not the consequence |
| `evidence` | the artifact, the field, and the numbers that contradict |
| `suggested_fix` | the input to change, or the sentence that has to be written |

```json
{
  "findings": [
    {
      "id": "F1",
      "severity": "high",
      "target_stage": "cost-of-capital",
      "claim": "Country risk is charged twice.",
      "evidence": "cost-of-capital.json adds a 3.1% country risk premium to the cost of equity, and dcf-result.json applies a further 12% expropriation haircut to the operating asset value. The routing constraint single-charge-per-risk permits one channel.",
      "suggested_fix": "Keep the exposure-weighted premium in the cost of equity and remove the haircut, or model expropriation as an explicit probability-weighted branch and drop the premium. State which channel was chosen."
    }
  ]
}
```

`target_stage` names the stage the orchestrator dispatched, matching the keys under
`state.json.stages`. Route each finding to the artifact's single writer, using the roster:

| Artifact | Owning agent |
|---|---|
| `classification.json`, `diagnosis.md` | `company-diagnostician` |
| `narrative.md`, `drivers.json` | `business-narrative-analyst` |
| `cleaned-financials.json`, `adjustments.md` | `financial-statement-analyst` |
| `cost-of-capital.json` / `.md` | `cost-of-capital-analyst` |
| `forecast.json`, `dcf-result.json`, `intrinsic.md` | `intrinsic-valuation-analyst` |
| `relative-result.json`, `relative.md` | `relative-valuation-analyst` |
| `capital-structure.json`, `payout.json`, `investment.json` | the matching corporate-finance analyst |
| `real-options.json` / `.md` | `real-options-analyst` |

A finding aimed at the wrong stage will be fixed by nobody. When a defect spans two stages,
route it to the upstream one, because the downstream artifact will be rebuilt anyway.

`challenge.md` is the prose companion. It carries five sections in this order. The route you
validated against. The validator run and its counts. The findings ranked by severity, with
the argument for each. The attacks you ran that found nothing. The open questions you could
not resolve from the artifacts. That fourth section matters as much as the third. It is the
record that the review was systematic rather than opportunistic.

Worked findings, including the shape of a good `evidence` field, are in
[finding-examples.md](resources/finding-examples.md).

## What this pass does not do

It does not produce an alternative valuation. If you rebuild the model to test a claim, the
rebuild is evidence inside a finding, not an artifact.

It does not edit `forecast.json`, `dcf-result.json` or any other agent's file. Not even to
fix an obvious typo.

It does not grade the analyst. It grades the argument.

It does not report checks that passed as though they were findings. Consistency is not
accuracy, and a clean validator run is a floor, not a verdict.
