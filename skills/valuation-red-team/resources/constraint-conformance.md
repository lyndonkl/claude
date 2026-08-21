# Constraint conformance

`classification.json` carries a `constraints` array. Each entry names a rule the
diagnostician compiled from the route. Every rule is a predicate over the artifacts that
came later. This file turns each rule into something you can test.

Read the route first. `primary_path`, `engine_branch` and `overlays` tell you which rules
should be present. A missing constraint is itself a finding, aimed at the diagnostician: a
bank whose classification carries no `no-fcff-valuation` rule was mis-routed, whatever the
valuation then did.

## The predicate table

Severity is `high` for every row. A route violation voids the work rather than degrading
it.

| Rule | Read | Fails when |
|---|---|---|
| `no-fcff-valuation` | `dcf-result.json.method` | the method is FCFF, or an enterprise value appears anywhere |
| `no-optimal-debt-ratio` | `capital-structure.json` | a WACC-minimizing debt schedule was run |
| `no-enterprise-multiple` | `relative-result.json.multiples[]` | EV/EBITDA, EV/Sales or EV/Invested Capital appears |
| `no-earnings-multiple` | `relative-result.json.multiples[]` | PE, PEG or EV/EBIT appears on the un-normalized year |
| `no-standard-growth-model` | `forecast.json` | growth was set as an earnings growth rate rather than built from revenue and a target margin |
| `require-failure-probability` | `dcf-result.json.failure.probability` | absent, or zero |
| `require-normalized-earnings` | `cleaned-financials.json` | the base year is a cycle extreme and no normalization basis is recorded |
| `no-normalization` | `cleaned-financials.json` | earnings were normalized although the losses are structural |
| `require-total-beta` | `cost-of-capital.json.beta` | a market beta was used for an undiversified buyer |
| `require-illiquidity-discount` | `dcf-result.json` or the per-share block | no illiquidity discount was applied |
| `no-illiquidity-discount` | the same | an illiquidity discount was applied to a public buyer or an IPO |
| `require-key-person-haircut-on-income` | `cleaned-financials.json` | the haircut was applied to final value rather than to operating income |
| `require-rd-capitalization` | `adjustments.md`, `cleaned-financials.json` | research spending was left as an operating expense |
| `require-exposure-weighted-risk` | `cost-of-capital.json` | country risk was assigned by country of incorporation |
| `no-blanket-country-discount` | `dcf-result.json` | a flat emerging-market haircut sits alongside a country premium |
| `no-governance-discount` | `cost-of-capital.json`, `dcf-result.json` | weak governance entered as a rate bump or a value haircut |
| `require-divisional-rates` | `cost-of-capital.json` | one company-wide rate was used across divisions |
| `zero-growth-below-cost-of-capital` | `forecast.json` | a division earning at or below its own rate was granted a high-growth period |
| `require-market-value-minorities` | `dcf-result.json.bridge` | minority interests were subtracted at book |
| `require-exclusivity-scaling` | `real-options.json` | the exclusivity factor is unstated, or left at 1.0 |
| `no-option-premium-without-gate` | `real-options.json` | a premium was added without all three gate tests passing |
| `no-exit-multiple-terminal-value` | `forecast.json.terminal` | terminal value came from a multiple rather than a perpetuity |
| `require-target-own-discount-rate` | `investment.json`, `cost-of-capital.json` | the acquirer's rate or debt capacity was applied to the target |
| `synergy-baseline-is-restructured-target` | `investment.json` | synergy was measured against the status quo target |
| `no-perpetual-growth-above-riskfree` | `forecast.json.terminal`, `cost-of-capital.json` | terminal growth exceeds the riskfree rate in the valuation currency |
| `single-charge-per-risk` | everything | any risk is charged through two channels |
| `no-intrinsic-valuation` | the mode itself | a discounted cash flow value was produced for an asset that generates no cash flows |

## What the validator covers

`valuation-consistency-checks` enforces three of these mechanically:
`no-fcff-valuation`, `require-failure-probability` and `no-earnings-multiple`. It records
any other rule name it finds but does not test it. That is deliberate on its part and it
leaves the rest to you.

Two operational notes. The first rule needs a `method` field on the DCF artifact, which the
engine does not emit — if the field is missing, the check silently never fires, so confirm
it is there before trusting a clean run. The third reads the multiple names from the
relative artifact, so a multiple recorded under a nonstandard label escapes it.

## Rules that fail quietly

Four of these are worth extra attention because the artifact looks normal when they break.

**`require-exposure-weighted-risk`.** Country risk belongs to operations, not to the
passport. A Brazilian exporter carries less Brazil risk than a Brazilian retailer. Read the
geography block in `classification.json` and check the weights in `cost-of-capital.json`
against it. A single country premium stamped on a globally diversified firm is the common
form of this failure.

**`no-governance-discount`.** Weak governance is a cash-flow fact. It is modelled as low
returns on capital and a low probability that anyone forces a change. A discount-rate bump
or a flat haircut is unfalsifiable, and it usually sits on top of a country premium that is
already charging for part of the same thing.

**`zero-growth-below-cost-of-capital`.** Growth only creates value above the cost of
capital. A division earning less than its own rate is worth more shrinking. Check the
divisional table in `forecast.json` for a high-growth period granted where the return
spread is negative.

**`require-exclusivity-scaling`.** Most real-option candidates are worth nothing, because
in a competitive product market anyone can exercise them. High volatility multiplies zero.
An option premium with no stated barrier — patent, licence, brand, switching cost — and no
stated exclusivity factor is a finding regardless of what the pricing model returned.

## Mutually exclusive pairs

Some violations show up as a pair rather than as a single rule. Each pair below is a hard
error when both halves are present.

| Pair | Why only one may run |
|---|---|
| normalized earnings and a separate recovery assumption | the normalized figure already is the recovery |
| normalization and a revenue-driven engine | normalizing is legitimate only when the trouble is temporary |
| total beta and a diversified buyer | one buyer identity per valuation |
| illiquidity discount and a public buyer or IPO | the buyer's investors have a market |
| option value and the same upside inside growth | route each claim to exactly one device |
| a higher discount rate for failure and a probability weight | the probability weight is the correct channel |
| a decision tree and an option premium on the same optionality | they are alternative representations |
| consolidated joint-venture assets and its equity carried as a holding | the sign of the adjustment reverses |
