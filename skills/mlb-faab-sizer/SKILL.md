---
name: mlb-faab-sizer
description: Computes FAAB (Free Agent Acquisition Budget) recommended and maximum bids for Yahoo fantasy baseball waiver targets. Implements the baseball-specific layering of the faab-bid-framework (positional_need_fit, role_certainty, urgency, season_pace, league-inflation calibration) and DELEGATES the game-theoretic primitives -- first-price shading and winner's-curse haircut -- to the sibling skills `auction-first-price-shading` and `auction-winners-curse-haircut`. Produces a recommended bid, a hard ceiling, a rationale with the full delegation chain, and guardrail flags. Use when the user asks "how much should I bid on X", mentions FAAB bid, waiver bid amount, blind bid, Yahoo waiver claim sizing, or when mlb-waiver-analyst needs a bid amount for an identified target.
---
# MLB FAAB Sizer

## Table of Contents
- [Delegation Chain](#delegation-chain)
- [Example](#example)
- [Workflow](#workflow)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Delegation Chain

This skill is a **baseball-specific orchestrator**. It does NOT compute auction math inline. It composes two domain-neutral sibling skills:

| Step | Who | Responsibility |
|---|---|---|
| 1 | this skill | Compute `base_value` from Yahoo-adjusted projection, pos fit, role certainty, urgency, season pace (with league-inflation calibration) |
| 2 | this skill | Classify target as `common_value` / `private_value` / `mixed` |
| 3 | `auction-winners-curse-haircut` | Return `adjusted_valuation` (Bayesian haircut for common-value) |
| 4 | this skill | Estimate `N` from opponent profiles |
| 5 | `auction-first-price-shading` | Return `shaded_bid` ((N-1)/N + distribution + risk adjustment) |
| 6 | this skill | Apply baseball guardrails (April 40%, speculation 20%, $1 floor, role-cert floor) |
| 7 | this skill | Emit `faab_rec_bid`, `faab_max_bid`, rationale naming both delegations |

**Invariant**: this skill never computes `(N-1)/N` or a common-value haircut directly. Any change to those primitives is made in the sibling skills.

## Example

**Scenario**: Roki Sasaki called up, likely Dodgers rotation spot. $100 FAAB remaining, week 4.

1. **base_value** (this skill): `28 x 0.70 x 0.65 x 1.2 x 0.7 = $10.70`
2. **Classify**: `common_value` (headline prospect).
3. **Invoke `auction-winners-curse-haircut`** with `(raw=10.70, type=common_value, N=6, dispersion=60)` -> `adjusted_valuation = $7.39`, haircut 31%.
4. **N estimate**: 6 opponents have SP need + budget.
5. **Invoke `auction-first-price-shading`** with `(true_value=7.39, N=6, dist=log-normal, risk=0.2, budget=100)` -> `shaded_bid = $7`, shade 0.90.
6. **Baseball guardrails**: all clear.
7. **Output**: `faab_rec_bid=$7`, `faab_max_bid=round($7.39 x 0.90)=$7`. Rationale cites both sibling skills.

Full trace in [resources/methodology.md](resources/methodology.md#worked-example-sasaki-call-up) and [resources/template.md](resources/template.md#worked-delegation-flow).

## Workflow

```
FAAB Sizing Progress:
- [ ] Step 1: Collect input signals and budget state
- [ ] Step 2: Compute base_value (baseball layering)
- [ ] Step 3: Classify value_type
- [ ] Step 4: Invoke auction-winners-curse-haircut -> adjusted_valuation
- [ ] Step 5: Estimate N from opponent profiles
- [ ] Step 6: Invoke auction-first-price-shading -> shaded_bid
- [ ] Step 7: Apply baseball guardrails
- [ ] Step 8: Emit signal + rationale with delegation trace
```

**Step 1: Collect inputs** (ask caller if missing):
- `acquisition_value` ($, 1-100 scale) -- from `mlb-player-analyzer`
- `positional_need_fit` (0-100) -- from `mlb-waiver-analyst`
- `role_certainty` (0-100) -- from `mlb-player-analyzer`
- FAAB remaining, week number, situation label

**Step 2: Compute `base_value`** (baseball-specific layering):

```
base_value = acquisition_value
           x (positional_need_fit / 100)
           x (role_certainty / 100)
           x urgency_multiplier          [0.7 - 1.4]
           x season_pace_multiplier      [0.6 - 1.4 after inflation calib]
```

Urgency: 1.4 (closer loses job / prospect called up); 1.2 (new opportunity); 1.0 (steady); 0.8 (wave); 0.7 (speculation).

Pace base: 0.6 (Apr wk 1-4), 1.0 (May-Jun), 1.2 (Jul-Aug), 1.4/0.5 (Sept contending/eliminated). Then multiply by `league_inflation_ratio` from `tracker/faab-log.md` (see [methodology.md](resources/methodology.md#league-inflation-calibration)). Min 5 valid rows; else skip calibration and flag `low_calibration_data`.

**Step 3: Classify `value_type`**:
- `common_value`: headline prospect, named closer, star off IL (same info for all teams)
- `private_value`: handcuff, platoon fit, punt-category-specific (only we weigh this way)
- `mixed`: record common/private weight

Default to `common_value` when uncertain (conservative; triggers haircut).

**Step 4: Invoke `auction-winners-curse-haircut`**:
```
inputs = { raw_valuation: base_value, value_type, n_informed_bidders: N,
           signal_dispersion: 40 (default) }
```
Consume `adjusted_valuation`. Preserve `classification_rationale` for output. Dispersion defaults: 60 for prospects, 30 for established players, 40 otherwise.

**Step 5: Estimate N** from opponent profiles (teams with positional_need > 50, faab > 20% original, activity >= moderate). Clamp [1, 8]. Defaults: common superstar 6, common role-player 3, private 1-2.

**Step 6: Invoke `auction-first-price-shading`**:
```
inputs = { true_value: adjusted_valuation, n_bidders_estimate: N,
           value_distribution: "log-normal" (MLB default),
           risk_aversion: 0.2 (bump to 0.4 for contending September),
           budget_remaining: faab_remaining }
```
`shaded_bid` becomes pre-guardrail `faab_rec_bid`. Set `faab_max_bid = round(adjusted_valuation x 0.90)`.

**Step 7: Apply baseball guardrails** (see below). Never silently violate.

**Step 8: Emit** via `mlb-signal-emitter`. User-facing rationale MUST name both sibling skills by purpose. Validate with [rubric](resources/evaluators/rubric_mlb_faab_sizer.json). Minimum 3.5.

## Common Patterns

**1. Hot common-value call-up (early season)**: N=5-7, pace 0.6-0.7, haircut ~25-30%, shade ~0.80-0.85. Typical $5-$12 rec.

**2. Private-value handcuff**: N=1-2, haircut=0 (short-circuit), shade 0.0-0.5. Typical $1-$3 rec.

**3. Closer change (mid-season, common-value)**: N=5-8, urgency 1.4, haircut ~25%, shade ~0.83. Typical $10-$30 rec.

**4. September contender stretch target**: pace 1.4, risk_aversion bumped to 0.4, shade ~0.88-0.92. Can reach 40-60% of remaining FAAB.

## Guardrails

1. **April 40% cap**: weeks 1-13, `faab_max_bid` ≤ 40% of FAAB remaining. Flag `april_40pct_cap_triggered`.
2. **Speculation 20% cap**: if `situation=speculation` or `role_certainty<30`, cap at 20%. Flag `speculation_20pct_cap_triggered`.
3. **$1 floor**: if `shaded_bid` rounds to $0 but `positional_need_fit >= 30`, bid $1 (rolling-list tiebreak). Otherwise bid $0 and flag `zero_bid_preservation`.
4. **Role certainty floor**: if `role_certainty < 20`, force `faab_rec_bid = $0`. Flag `role_certainty_floor`.
5. **Regression override**: if `regression_index < -30`, cut `faab_rec_bid` by 30%. Flag `regression_luck_discount`.
6. **Variant divergence**: advocate/critic differ >30% -> take critic. Flag `variant_divergence_applied`.
7. **Budget floor (post-July)**: if week >= 14 and remainder < $5, flag `budget_floor_near_zero`.
8. **Log the decision**: every computation via `mlb-decision-logger` (including $0 bids).

**Do NOT duplicate sibling caps**: the `0.9 x true_value` ceiling is enforced by `auction-first-price-shading`; the 35% haircut cap is enforced by `auction-winners-curse-haircut`. Trust them.

## Quick Reference

**Pipeline:**
```
base_value = acq_value x (pos_fit/100) x (role_cert/100) x urgency x pace_calibrated

adjusted_valuation = auction-winners-curse-haircut(
    raw_valuation=base_value, value_type, n_informed_bidders=N, signal_dispersion)

shaded_bid = auction-first-price-shading(
    true_value=adjusted_valuation, n_bidders_estimate=N,
    value_distribution="log-normal", risk_aversion=0.2, budget_remaining)

faab_rec_bid = round(shaded_bid)          # then baseball guardrails
faab_max_bid = round(adjusted_valuation x 0.90)
```

**Inputs required**: `acquisition_value`, `positional_need_fit`, `role_certainty`, FAAB remaining, week, situation label, `regression_index` (optional).

**Outputs**: `faab_rec_bid`, `faab_max_bid`, `value_type`, `N`, `adjusted_valuation`, `shaded_bid`, multipliers, guardrail flags, user-facing rationale.

**Sibling skills:**
- `@skills/auction-first-price-shading/` -- `(N-1)/N` + distribution + risk-aversion
- `@skills/auction-winners-curse-haircut/` -- Bayesian common-value haircut

**Key resources:**
- **[resources/template.md](resources/template.md)**: Input block, output template with delegation trace, per-target brief, worked delegation flow
- **[resources/methodology.md](resources/methodology.md)**: Baseball layering, inflation calibration, value-type classification, baseball guardrails. Auction math is in the sibling skills.
- **[resources/evaluators/rubric_mlb_faab_sizer.json](resources/evaluators/rubric_mlb_faab_sizer.json)**: Eight-criterion rubric including **Delegation Integrity**.
