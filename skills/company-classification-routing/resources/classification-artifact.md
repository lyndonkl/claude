# The classification artifact

`02-diagnosis/classification.json` is the contract between the diagnostician and every
stage after it. `02-diagnosis/diagnosis.md` carries the reasoning a human reads. Both are
written by `company-diagnostician` and by nobody else.

Gate `G2_classified` passes when the JSON validates and a primary path plus a constraint
set exist. Everything downstream is blocked until then.

## Field by field

### Signal block

These record what the company is. They come from S1 and do not change once written.

| Field | Values | Notes |
|---|---|---|
| `life_cycle_stage` | `young` \| `growth` \| `mature` \| `aging` \| `declining` | The SPEC vocabulary. Record the finer S1 stage in `diagnosis.md`. |
| `earnings_status` | `profitable` \| `marginal` \| `negative` \| `cyclical-trough` | Say in `diagnosis.md` whether a negative status is transient or structural. That distinction drives B7 against B1. |
| `sector_type` | `non-financial` \| `financial-service` \| `commodity-cyclical` \| `real-estate` | |
| `ownership` | `public` \| `private` \| `subsidiary` | |
| `geography` | `{incorporation, operations[]}` | `operations` carries region and `revenue_share`. Shares sum to 1. Incorporation is recorded but never drives risk. |
| `distress_markers` | `{present, evidence[]}` | Every marker from S6 that fired, each with its source. |
| `intangible_intensity` | `low` \| `moderate` \| `high` | `moderate` or `high` triggers B8 in S3. |

### Route block

These record the decision. They come from S2 through S7.

| Field | Notes |
|---|---|
| `primary_path` | One of `standard-fcff`, `standard-fcfe`, `dividend-discount`, `excess-return`, `revenue-driven`, `distress-adjusted`, `asset-based`. |
| `engine_branch` | `B1` through `B16`. Exactly one. |
| `overlays` | Any of `intangible-heavy`, `emerging-market`, `multi-business`, `cross-holdings`, `has-real-options`, `macro-shock`. Zero or more. |
| `transaction_overlay` | `acquisition` \| `restructuring` \| `ipo` \| `private-sale` \| `none`. From the mandate. |
| `discount_stack` | Any of `illiquidity`, `minority`, `key-person`. Empty for a public company. |
| `constraints` | Objects with `rule`, `reason`, `source_branch`. |
| `pipeline` | The ordered step list from S8-R4. |
| `confidence` | `high` \| `medium` \| `low`. |
| `unresolved` | Strings naming evidence that would change the routing. |

## Consistency rules on the artifact itself

Check these before writing. They are cheap, and each one catches a real error.

1. **Path and branch agree.** A `B5` branch never carries `standard-fcff`. A `B1` branch
   carries `revenue-driven`. A `B4`-dominant route carries `distress-adjusted`.
2. **Exactly one engine branch.** Overlays go in `overlays`. A route naming two engines has
   not resolved R1 precedence.
3. **Every constraint has a source.** A constraint with no `source_branch` is an opinion.
   The only exceptions are the two universal ones, `no-perpetual-growth-above-riskfree` and
   `single-charge-per-risk`, which carry `source_branch: "universal"`.
4. **Constraints match the branches.** Compile the union of what the fired branches emit,
   and nothing else. `require-total-beta` on a public company is a compilation error.
5. **No contradictory pair.** `require-illiquidity-discount` and `no-illiquidity-discount`
   cannot both appear. Neither can `require-normalized-earnings` and `no-normalization`.
6. **The discount stack matches the branch.** `illiquidity` appears only for B13-I.
   `key-person` appears only for an owner-operated private firm.
7. **Geography shares sum to 1**, and `operations` is non-empty whenever the
   `emerging-market` overlay is present.

## Writing constraints

The `reason` field is read by a human, and by the critic when it finds a violation. Write
it as a sentence that explains the mechanism, not as a restatement of the rule.

Weak: `"reason": "because this is a bank"`.

Better: `"reason": "Deposits and short-term funding are inputs to the business rather than
financing, so operating and financing decisions cannot be separated and there is no
meaningful cost of capital."`

## The diagnosis.md companion

The JSON is what agents read. The markdown is what a person reads to decide whether to
trust the route. Cover six things.

1. **What the company is**, in three or four sentences. Business model, how it makes money,
   what it owns.
2. **The signal readout.** Every S1 signal, its computed value, and the evidence. Flag any
   signal you judged unrepresentative, and say why.
3. **Which gate fired and why.** Walk S2 through S6 in order. Name the gate that decided
   the engine, and the branch it sent the company to. Where a gate turned on a judgment
   call — transient against structural losses, commodity against cyclical, stable against
   changing leverage — state the evidence on both sides and say which side wins.
4. **The overlays**, each with its trigger.
5. **The constraint list**, grouped by source branch, in plain words. This is what a
   downstream agent reads when it wants to know why a method is closed to it.
6. **Confidence and what is unresolved.** Say which single piece of evidence would most
   change the answer.

## What downstream agents do with it

| Agent | Reads |
|---|---|
| `financial-statement-analyst` | `intangible_intensity` for B8, `ownership` for the private cleanup, `earnings_status` for whether to normalize |
| `cost-of-capital-analyst` | `sector_type` for whether a WACC exists at all, `geography` for the ERP build-up, `discount_stack` for total beta |
| `intrinsic-valuation-analyst` | `primary_path`, `engine_branch`, `pipeline`, and every constraint |
| `special-situations-analyst` | the whole artifact — it executes the non-standard branches |
| `relative-valuation-analyst` | the constraints that forbid multiples, plus `sector_type` for the peer set |
| `capital-structure-analyst` | `no-optimal-debt-ratio`, which suppresses the stage entirely |
| `valuation-critic` | every constraint, checked against every produced artifact under rule V9 |

No downstream agent re-derives the classification. If one disagrees, it raises a finding.
The orchestrator then reopens the diagnosis stage. Agents never edit another agent's
artifact.

## Mechanical validation

`valuation-consistency-checks` reads the artifact and enforces a subset automatically:

```bash
python3 resources/validate.py --classification classification.json --dcf dcf-result.json --relative relative-result.json
```

It fails the run on three things. An FCFF method under `no-fcff-valuation`. A missing
failure probability under `require-failure-probability`. A PE, P/E or EV/EBIT multiple
under `no-earnings-multiple`. The remaining constraints are enforced by the critic, reading
the reason text.
