---
name: mlb-faab-sizer
description: Computes FAAB (Free Agent Acquisition Budget) recommended and maximum bids for Yahoo fantasy baseball waiver targets. Implements the faab-bid-framework formula combining acquisition_value, positional_need_fit, role_certainty, FAAB budget remaining, season timing, and league inflation calibration from the faab-log. Produces a recommended bid, a hard ceiling, a rationale, and guardrail flags. Use when the user asks "how much should I bid on X", mentions FAAB bid, waiver bid amount, blind bid, Yahoo waiver claim sizing, or when mlb-waiver-analyst needs a bid amount for an identified target.
---
# MLB FAAB Sizer

## Table of Contents
- [Example](#example)
- [Workflow](#workflow)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Example

**Scenario**: Roki Sasaki just got called up and is likely to enter the Dodgers rotation. User has $100 FAAB remaining, it is late April (week 4 of the season).

**Signal inputs** (from `mlb-waiver-analyst` / `mlb-player-analyzer`):
- `acquisition_value` = $28 (rest-of-season value, 1-100 dollar scale)
- `positional_need_fit` = 70 (roster is thin on SP)
- `role_certainty` = 65 (rotation probable, not confirmed starter)
- FAAB remaining = $100
- Week number = 4 (late April)
- Recent comparable bids in faab-log: Luis Gil $14 (we won at $18), Kyle Bradish $6

**Multipliers**:
- `urgency_multiplier` = 1.2 (new call-up, fresh news)
- `season_pace_multiplier` = 0.7 (early April bucket, save budget for later)

**Computation**:
```
max_bid_fraction = 0.28 x 0.70 x 0.65 x 1.2 x 0.7 = 0.107
faab_max_bid     = 0.107 x $100 = $10.70 -> round to $11
faab_rec_bid     = $11 x 0.6 + $1 = $7.60 -> round to $8
```

**Output**: Bid **$8** on Sasaki. Ceiling **$11**. Rationale: high-ceiling new starter, but we are in April and want to preserve FAAB for the July-August window.

## Workflow

Copy this checklist and track progress:

```
FAAB Sizing Progress:
- [ ] Step 1: Collect input signals and budget state
- [ ] Step 2: Determine urgency_multiplier
- [ ] Step 3: Determine base season_pace_multiplier (calendar bucket)
- [ ] Step 4: Read faab-log, calibrate season_pace_multiplier for league inflation
- [ ] Step 5: Compute faab_max_bid
- [ ] Step 6: Compute faab_rec_bid
- [ ] Step 7: Apply guardrails, flag violations
- [ ] Step 8: Emit signal + user-facing rationale
```

**Step 1: Collect input signals and budget state**

Required inputs (ask the caller if missing -- do not assume):

- [ ] `acquisition_value` ($, 1-100 scale) -- from `mlb-player-analyzer`
- [ ] `positional_need_fit` (0-100) -- from `mlb-waiver-analyst`
- [ ] `role_certainty` (0-100) -- from `mlb-player-analyzer`
- [ ] FAAB remaining ($) -- from `context/team-profile.md`
- [ ] Current week number (1-26) -- derive from today's date
- [ ] Target's situation label (e.g., `new-callup`, `closer-change`, `replacement-level`, `speculation`)

See [resources/template.md](resources/template.md#input-block) for the input block format.

**Step 2: Determine urgency_multiplier**

| Situation | urgency_multiplier |
|---|---|
| Closer just lost job / prospect just called up / starter just promoted | 1.4 |
| New opportunity this week (injury replacement, platoon promotion) | 1.2 |
| Steady-state target (no new news) | 1.0 |
| Wave of similar players expected (e.g., multiple call-ups imminent) | 0.8 |
| Pure speculation (handcuff with no current role) | 0.7 |

**Step 3: Determine base season_pace_multiplier (calendar bucket)**

| Date range | Base `season_pace_multiplier` | Rationale |
|---|---|---|
| Weeks 1-4 (April) | 0.6 | Early -- save budget, avoid premature depletion |
| Weeks 5-13 (May-June) | 1.0 | Steady state |
| Weeks 14-20 (July-August) | 1.2 | Trade deadline, playoff push, closer churn |
| Weeks 21-23 (September, final 3) | 1.4 (if contending) / 0.5 (if eliminated) | Win-now or conserve |

**Step 4: Read faab-log, calibrate season_pace_multiplier for league inflation**

Read `/Users/kushaldsouza/Documents/Projects/yahoo-mlb/tracker/faab-log.md`. For each entry where `industry_consensus_at_time` and `winning_bid` are both recorded, compute the league inflation ratio. See [resources/methodology.md](resources/methodology.md#league-inflation-calibration) for the exact procedure. Adjust the base multiplier by the inflation factor (clamped to 0.6-1.4 overall).

Minimum data: 5 comparable entries with both fields. If fewer, skip calibration and flag `low_calibration_data: true` in the output.

**Step 5: Compute faab_max_bid**

```
max_bid_fraction = (acquisition_value / 100)
                 x (positional_need_fit / 100)
                 x (role_certainty / 100)
                 x urgency_multiplier
                 x season_pace_multiplier

faab_max_bid = round(max_bid_fraction x FAAB_remaining)
```

Round to the nearest whole dollar. Minimum `faab_max_bid` is $0 (valid "claim if nobody else bids" scenario when need is low).

**Step 6: Compute faab_rec_bid**

```
faab_rec_bid = round(faab_max_bid x 0.6) + 1
```

The `+1` breaks ties in Yahoo's rolling-list FAAB (e.g., $8 beats $7 with identical waiver priority). If `faab_max_bid` is $0, set `faab_rec_bid` to $0 as well.

**Step 7: Apply guardrails, flag violations**

See [Guardrails](#guardrails) below. Each guardrail either modifies the bid or flags the output. Never silently violate -- always flag in the signal file.

**Step 8: Emit signal + user-facing rationale**

Write the waiver signal via `mlb-signal-emitter` and produce a user-facing rationale per [resources/template.md](resources/template.md#output-template). Validate with [resources/evaluators/rubric_mlb_faab_sizer.json](resources/evaluators/rubric_mlb_faab_sizer.json). Minimum acceptable score: 3.5.

## Common Patterns

**Pattern 1: Hot new call-up (early season)**
- **Inputs**: High `acquisition_value` ($20-30), moderate `role_certainty` (60-75), early calendar
- **Multipliers**: urgency 1.2-1.4, pace 0.6-0.7
- **Typical output**: $5-$15 rec, $10-$25 ceiling on a $100 budget
- **Watch for**: Role uncertainty (AAA depth chart, manager quotes) -- do not let hype push past role_certainty

**Pattern 2: Closer change (mid-season)**
- **Inputs**: Moderate `acquisition_value` ($15-25 for saves), high `positional_need_fit` if thin on saves, role_certainty variable
- **Multipliers**: urgency 1.4 (just happened), pace 1.0-1.2
- **Typical output**: $10-$30 rec, $25-$50 ceiling
- **Watch for**: Closer-by-committee situations; role_certainty below 50 slashes the bid fast

**Pattern 3: Streamer / replacement-level hitter**
- **Inputs**: Low `acquisition_value` ($2-8), variable fit, high role_certainty
- **Multipliers**: urgency 1.0, pace per calendar
- **Typical output**: $0-$3 rec, $1-$5 ceiling
- **Watch for**: 40% FAAB guardrail never triggers here, but 20% speculation guardrail might if role is murky

**Pattern 4: Playoff push stretch target (September)**
- **Inputs**: High `positional_need_fit` (covering weak category), high role_certainty, high pace
- **Multipliers**: urgency 1.0-1.2, pace 1.4 (if contending)
- **Typical output**: Can go up to 40-60% of remaining FAAB
- **Watch for**: Contention status -- if not contending, pace should drop to 0.5 and preserve nothing

## Guardrails

1. **April 40% cap**: Before July 1, `faab_max_bid` cannot exceed 40% of FAAB remaining without explicit user approval. If formula produces more, cap at 40% and flag `guardrail: april_40pct_cap_triggered`.

2. **Speculation 20% cap**: If the target is flagged as speculation (handcuff with no current role, `role_certainty < 30`, or situation label `speculation`), cap `faab_max_bid` at 20% of FAAB remaining. Flag `guardrail: speculation_20pct_cap_triggered`.

3. **Variant divergence**: If the `mlb-waiver-analyst` advocate and critic variants produce bids that differ by >30%, lower `faab_rec_bid` to match the critic's number and flag `guardrail: variant_divergence_applied`.

4. **$0 bids are valid**: If `positional_need_fit < 30` AND FAAB remaining < 15% of original budget, default to `faab_rec_bid = $0`. This claims the player if nobody else bids at zero cost.

5. **Budget floor**: Never produce a bid that would leave less than $5 remaining after July 1, unless this is explicitly a "last bid of the season" call. Flag `guardrail: budget_floor_near_zero`.

6. **Regression override**: If the target is flagged as BABIP-lucky (`regression_index < -30` from `mlb-player-analyzer`), cut `faab_rec_bid` by 30% and flag `guardrail: regression_luck_discount`.

7. **Role certainty floor**: If `role_certainty < 20`, force `faab_rec_bid` to $0 regardless of other signals. A player who will not play has no value.

8. **Log the decision**: Every bid computation (including $0 bids) is written to `tracker/decisions-log.md` via `mlb-decision-logger` with all inputs, multipliers, and guardrail flags.

## Quick Reference

**Core formulas**:
```
max_bid_fraction = (acquisition_value / 100)
                 x (positional_need_fit / 100)
                 x (role_certainty / 100)
                 x urgency_multiplier      [0.7 - 1.4]
                 x season_pace_multiplier  [0.6 - 1.4]

faab_max_bid = round(max_bid_fraction x FAAB_remaining)
faab_rec_bid = round(faab_max_bid x 0.6) + 1
```

**Multiplier ranges**:
| Multiplier | Min | Max | Default |
|---|---|---|---|
| `urgency_multiplier` | 0.7 | 1.4 | 1.0 |
| `season_pace_multiplier` | 0.6 | 1.4 | 1.0 (May-June) |

**Calendar buckets**:
| Weeks | Phase | Base pace |
|---|---|---|
| 1-4 | April | 0.6 |
| 5-13 | May-June | 1.0 |
| 14-20 | Jul-Aug | 1.2 |
| 21-23 | Final push | 1.4 or 0.5 |

**Inputs required**:
- `acquisition_value` ($)
- `positional_need_fit` (0-100)
- `role_certainty` (0-100)
- FAAB remaining ($)
- Current week number
- Situation label (for urgency_multiplier)
- Regression index (from player-analyzer, optional)

**Outputs produced**:
- `faab_rec_bid` ($)
- `faab_max_bid` ($)
- Multipliers used (urgency, pace, inflation adjustment)
- Guardrail flags (any triggered)
- User-facing rationale (plain English, beginner-safe)

**Key resources**:
- **[resources/template.md](resources/template.md)**: Input block, output template, per-target brief format
- **[resources/methodology.md](resources/methodology.md)**: Formula derivation, league inflation calibration from faab-log, worked examples
- **[resources/evaluators/rubric_mlb_faab_sizer.json](resources/evaluators/rubric_mlb_faab_sizer.json)**: 8-criterion quality rubric
