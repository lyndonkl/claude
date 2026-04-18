# MLB FAAB Sizer Methodology

Baseball-specific layering for `mlb-faab-sizer`. Covers `base_value` computation, the urgency and season-pace multipliers, league-inflation calibration from `tracker/faab-log.md`, value-type classification, baseball guardrails, and worked examples that trace the full delegation chain.

**Auction math is NOT in this file.** The `(N-1)/N` shading derivation lives in `@skills/auction-first-price-shading/resources/methodology.md`. The winner's-curse haircut derivation lives in `@skills/auction-winners-curse-haircut/resources/methodology.md`. This file references those skills by name at each delegation step.

## Table of Contents
- [Pipeline Overview](#pipeline-overview)
- [Step 1: base_value Layering](#step-1-base_value-layering)
- [Urgency Multiplier](#urgency-multiplier)
- [Season Pace Multiplier (Base)](#season-pace-multiplier-base)
- [League Inflation Calibration](#league-inflation-calibration)
- [Value-Type Classification](#value-type-classification)
- [Delegations](#delegations)
- [N Estimation from Opponent Profiles](#n-estimation-from-opponent-profiles)
- [Baseball-Specific Guardrails](#baseball-specific-guardrails)
- [Rounding and $0 Bids](#rounding-and-0-bids)
- [Worked Example: Sasaki Call-Up](#worked-example-sasaki-call-up)
- [Worked Example: Closer Change Mid-Season](#worked-example-closer-change-mid-season)
- [Worked Example: Private-Value Handcuff](#worked-example-private-value-handcuff)

---

## Pipeline Overview

```
(1) base_value              <- this skill (baseball layering)
(2) value_type              <- this skill (classification)
(3) adjusted_valuation      <- delegated to auction-winners-curse-haircut
(4) N                       <- this skill (opponent-profile scan)
(5) shaded_bid              <- delegated to auction-first-price-shading
(6) faab_rec_bid, faab_max_bid  <- this skill (guardrails + rounding)
```

Each step reads the outputs of the previous step and feeds only the fields the next step's contract requires. No circular references; no inline re-derivation of auction math.

---

## Step 1: base_value Layering

```
base_value = acquisition_value                  # $ on 1-100 scale
           x (positional_need_fit / 100)         # 0.0-1.0
           x (role_certainty / 100)              # 0.0-1.0
           x urgency_multiplier                  # 0.7 - 1.4
           x season_pace_multiplier_calibrated   # 0.6 - 1.4 after inflation adj.
```

The three fractional terms are unipolar 0-1 weights. A player with low `role_certainty` (e.g., 20/100) is already discounted 80% before any multipliers -- role uncertainty is the single biggest real-world driver of losing FAAB bids, so it gets full weight in the base layer.

The two multipliers bracket `base_value` between 0.42x and 1.96x of the "neutral" amount. Extreme combinations are rare and usually self-contradictory (early-April pure-speculation bids at 1.4 urgency make no sense).

**Important**: `base_value` is a DOLLAR valuation in the same scale as `acquisition_value` -- it is what the target is worth to US after baseball-specific adjustments but before game-theoretic corrections. It is the input to Step 3's haircut, not a bid amount.

---

## Urgency Multiplier

Captures time-sensitive shifts in player value NOT already priced into `acquisition_value` (which is typically a rest-of-season projection snapshot).

| Situation | `urgency_multiplier` | Rationale |
|---|---|---|
| Prospect just called up (first MLB game this week) | 1.4 | One-time window; others bid on same news |
| Closer just lost job (demotion, IL, trade) | 1.4 | Saves redistribute fast |
| Starter just promoted into rotation (5th man named) | 1.2 | News fresh, role more predictable |
| Injury replacement with announced playing time | 1.2 | Window of opportunity |
| Platoon promotion (new regular vs LHP/RHP) | 1.1 | Marginal new opportunity |
| Steady-state target (no new news) | 1.0 | Default |
| Wave of similar players expected | 0.8 | Substitutes exist |
| Pure speculation (handcuff with no role) | 0.7 | Value is optionality |

**Rule of thumb**: if you can't explain in one sentence *why this week*, the multiplier should be 1.0 or lower.

---

## Season Pace Multiplier (Base)

Before league-specific calibration:

| Week | Phase | Base `season_pace_multiplier` | Rationale |
|---|---|---|---|
| 1-4 | April | 0.6 | Early -- save budget; most "hot starts" regress by June |
| 5-13 | May-June | 1.0 | Steady state |
| 14-20 | Jul-Aug | 1.2 | Trade deadline, closer churn, playoff push |
| 21-23 | September (final 3 weeks) | 1.4 (contending) / 0.5 (eliminated) | Win-now or preserve |

**Contending** = within 1 game of final playoff seed or holding a seed per `context/team-profile.md`. If ambiguous, default to 1.0 and flag `contention_ambiguous`.

Late-April interpolation: weeks 3-4 may use 0.7 rather than strict 0.6.

---

## League Inflation Calibration

This is the baseball-specific calibration that adjusts `season_pace_multiplier` based on how our specific Yahoo league bids relative to public/industry consensus. It is NOT a winner's-curse correction (that's delegated to the sibling skill) -- it's a league-market-level rescaling.

### Step-by-step

**Step 1: Read the faab-log**

Parse `/Users/kushaldsouza/Documents/Projects/yahoo-mlb/tracker/faab-log.md`. Each entry:

```
### {date} | {player} | {result}
- our_bid: $___
- winning_bid: $___
- winner: ___
- recommended_bid: $___
- industry_consensus_at_time: $___
- outcome_3wk: ___
```

**Step 2: Filter for valid calibration rows**

Keep only rows where BOTH `winning_bid` and `industry_consensus_at_time` are populated and non-zero. Drop `NOT_BID` entries (we never saw who else bid).

If fewer than 5 valid rows exist, skip calibration. Set `calibration_confidence: low`. Do not adjust the base multiplier.

**Step 3: Compute inflation ratio**

```
inflation_ratio_i = winning_bid_i / industry_consensus_at_time_i
league_inflation_ratio = mean(inflation_ratio_i)
```

- `> 1.0`: league overbids industry (we must bid higher to win)
- `< 1.0`: league underbids (we can win with less)
- `= 1.0`: league tracks consensus

**Step 4: Calibration confidence**

| Valid rows | Confidence |
|---|---|
| 0-4 | low (do not apply) |
| 5-9 | medium |
| 10+ | high |

**Step 5: Apply**

```
season_pace_multiplier_calibrated = season_pace_multiplier_base x league_inflation_ratio
```

**Clamp** to [0.6, 1.4]. If clamping fires, flag `calibration_clamp_triggered`.

**Step 6: Recency weighting (if 10+ rows)**

Weight the 5 most recent rows 2x, earlier rows 1x.

### Example calibration

7 valid faab-log entries yield ratios [1.50, 1.20, 1.40, 1.29, 0.75, 1.22, 1.10]. Mean = **1.21**. Our league overbids industry ~21%. If base May pace = 1.0, calibrated pace = **1.21**. Confidence: medium.

---

## Value-Type Classification

Classification is a judgment call and MUST be explicit before invoking the haircut sibling. Baseball-specific examples:

**`common_value`** -- everyone's projection is similar because information is shared:
- Top-100 prospect call-ups (FanGraphs, MLB Pipeline coverage)
- Named closers after a closer-change announcement
- Star bat coming off the IL with a known timeline
- High-strikeout SP with a fresh rotation spot
- Any target FantasyPros/RotoBaller consensus is tracking actively

**`private_value`** -- the target's value is meaningfully higher for us than for others:
- Handcuff to a reliever/SP we already own
- Platoon fit for our specific lineup composition
- Punt-category-specific player (e.g., SB-only speedster when we punt saves)
- Depth piece at a position where we have one injury away from a hole

**`mixed`** -- shared core value plus a private increment:
- Hot hitter everyone agrees on as a common-value baseline but who fits a specific category need
- Closer-in-waiting when we also own the current closer (common = saves value; private = handcuff certainty)
- Record the common/private weight (default 0.6 common, but override when the private increment is large)

**Guardrail**: when uncertain, default to `common_value` (conservative -- triggers the haircut). Do not claim `private_value` unless the private reason is concrete and unique to us.

---

## Delegations

### Delegation 1: auction-winners-curse-haircut

**Skill**: `@skills/auction-winners-curse-haircut/`

**Why delegate**: the haircut formula (Bayesian over-estimation correction, Kagel-Levin experimental calibration, private-value short-circuit) is domain-neutral. Any auction caller -- fantasy FAAB, prediction market, procurement, M&A -- needs the same math. Duplicating it here would create drift.

**Invocation**:
```
inputs = {
  raw_valuation: base_value,             # from step 1 above
  value_type: <classified in step 2>,
  n_informed_bidders: N,                 # same N we use for shading in delegation 2
  signal_dispersion: 40,                 # default; see below
  mix_common_weight: 0.6,                # only if value_type == "mixed"
}
```

**Signal dispersion defaults for MLB**:
- Prospect call-up with limited major-league track record: 60
- Established player with wide public data: 30
- Reliever role-change: 40
- Platoon/role-player: 50
- Default when unsure: 40

**Outputs consumed**: `adjusted_valuation` (passed to shading as `true_value`) and `classification_rationale` (included verbatim in our user-facing rationale).

### Delegation 2: auction-first-price-shading

**Skill**: `@skills/auction-first-price-shading/`

**Why delegate**: the `(N-1)/N` equilibrium shade (with log-normal distribution adjustment and risk-aversion adjustment) is domain-neutral. Same reasoning as delegation 1.

**Invocation**:
```
inputs = {
  true_value: adjusted_valuation,        # from delegation 1
  n_bidders_estimate: N,
  value_distribution: "log-normal",      # MLB default; "uniform" only for thin-info role-players
  risk_aversion: 0.2,                    # default; 0.4 for contending September
  budget_remaining: faab_remaining,
}
```

**Outputs consumed**: `shaded_bid` (becomes `faab_rec_bid` pre-guardrails); `shade_fraction` and `assumptions_flagged` (surfaced in our rationale and `formula_trace`).

### Anti-patterns (do NOT do these)

- Do NOT compute `(N-1)/N` here. Call the sibling.
- Do NOT apply a flat 20% haircut for common-value targets. That was the v2 behavior. The sibling now computes haircut from `log(N)` and `signal_dispersion`.
- Do NOT apply the haircut inside `base_value`. It is a separate step in the pipeline and is conditional on `value_type`.
- Do NOT stack our guardrails with the sibling's caps (`0.9 x true_value` is already enforced by shading; the 35% haircut ceiling is already enforced by the haircut sibling).

---

## N Estimation from Opponent Profiles

```
N = count of opposing teams where:
    (positional_need > 50 OR target_fits_their_punt_strategy)
    AND (faab_remaining > 20% of original budget)
    AND (activity_level >= moderate)

Clamp N to [1, 8].
```

Read `opponent_profile` signals from all 11 opponents. For each, evaluate fit, budget, and activity.

**Defaults when profiles unavailable**:
- Common-value superstar target: N = 6
- Common-value role-player: N = 3
- Private-value target: N = 1-2

The same N is passed to both sibling skills (as `n_informed_bidders` to haircut, as `n_bidders_estimate` to shading) so they model the same competitive environment.

---

## Baseball-Specific Guardrails

Run after the shading sibling returns. Guardrails come from the baseball FAAB world (Yahoo rules, league management), not auction theory.

### 1. April 40% cap

```
if week_number <= 13 and faab_max_bid > 0.40 x faab_remaining:
    faab_max_bid = round(0.40 x faab_remaining)
    faab_rec_bid = min(faab_rec_bid, faab_max_bid)
    flag: april_40pct_cap_triggered
```

### 2. Speculation 20% cap

```
if situation_label == "speculation" or role_certainty < 30:
    if faab_max_bid > 0.20 x faab_remaining:
        faab_max_bid = round(0.20 x faab_remaining)
        faab_rec_bid = min(faab_rec_bid, faab_max_bid)
        flag: speculation_20pct_cap_triggered
```

### 3. $1 floor / $0 preservation

```
if shaded_bid rounds to $0:
    if positional_need_fit >= 30:
        faab_rec_bid = 1        # take the rolling-list tiebreak
    else:
        faab_rec_bid = 0
        flag: zero_bid_preservation
```

### 4. Role certainty floor

```
if role_certainty < 20:
    faab_rec_bid = 0
    flag: role_certainty_floor
```

### 5. Regression luck discount

```
if regression_index is not None and regression_index < -30:
    faab_rec_bid = round(faab_rec_bid x 0.7)
    flag: regression_luck_discount
```

### 6. Variant divergence

```
if advocate_bid and critic_bid provided:
    divergence = abs(advocate - critic) / max(advocate, critic)
    if divergence > 0.30:
        faab_rec_bid = min(advocate, critic)
        flag: variant_divergence_applied
```

### 7. Budget floor (post-July)

```
if week_number >= 14 and (faab_remaining - faab_rec_bid) < 5:
    flag: budget_floor_near_zero
    # Do not modify bid -- flag for user approval
```

### 8. Never exceed FAAB remaining

```
if faab_max_bid > faab_remaining:
    faab_max_bid = faab_remaining
    faab_rec_bid = min(faab_rec_bid, faab_remaining)
    flag: faab_remaining_cap
```

(Shading sibling already caps at `budget_remaining`; this is belt-and-suspenders for rounding.)

---

## Rounding and $0 Bids

- Round all dollar values to the nearest whole dollar (Yahoo rejects fractional).
- Minimum bid in Yahoo is $0 (free claim if nobody else bids).
- If `faab_max_bid` rounds to $0, set `faab_rec_bid = $0` as well (cannot have rec > max).
- $0 bids are valid and often correct for low-need replacements or depth claims.

---

## Worked Example: Sasaki Call-Up

**Target**: Roki Sasaki, newly called up, likely rotation spot.

**Inputs**:
- `acquisition_value` = $28
- `positional_need_fit` = 70 (thin on SP)
- `role_certainty` = 65
- FAAB remaining = $100, week 4 (April)
- Situation: `new-callup`
- faab-log: 0 valid rows -- skip calibration

**Step 1 - base_value**:
```
urgency_multiplier = 1.2 (new-callup)
season_pace_multiplier = 0.7 (late April interpolation)
base_value = 28 x 0.70 x 0.65 x 1.2 x 0.7 = $10.70
```

**Step 2 - Classify**: `common_value` (headline prospect; every team has heard of Sasaki).

**Step 3 - Delegate to auction-winners-curse-haircut**:
```
inputs = { raw_valuation: 10.70, value_type: "common_value",
           n_informed_bidders: 6, signal_dispersion: 60 }

Sibling computes:
  haircut_pct = min(35, 10 + log(6)*5 + 60*0.2)
              = min(35, 10 + 8.96 + 12)
              = min(35, 30.96) = 30.96

  adjusted_valuation = 10.70 x (1 - 0.3096) = $7.39
```

**Step 4 - N estimate**: 6 opponents with SP need + budget -> N = 6.

**Step 5 - Delegate to auction-first-price-shading**:
```
inputs = { true_value: 7.39, n_bidders_estimate: 6,
           value_distribution: "log-normal", risk_aversion: 0.2,
           budget_remaining: 100 }

Sibling computes:
  shade_base = (6-1)/6 = 0.833
  log-normal adj: 1 - 1/(6 * 1.5) = 0.889
  risk-aversion: 0.889 + 0.2 x (1 - 0.889) x 0.4 = 0.898
  raw = 7.39 x 0.898 = $6.64
  cap = min(6.64, 0.9 x 7.39, 100) = min(6.64, 6.65, 100) = 6.64

  shaded_bid = round(6.64) = 7
```

**Step 6 - Baseball guardrails**:
- April 40% cap: $7 < $40 -- OK
- Role cert floor: 65 >= 20 -- OK
- Speculation cap: situation is new-callup -- OK

**Output**:
- `faab_rec_bid` = $7
- `faab_max_bid` = round($7.39 x 0.90) = $7
- Rationale: "Sasaki just got called up. Base value $10.70. Common-value target, so we apply the winner's-curse haircut (via auction-winners-curse-haircut: 31% for 6 informed bidders with high signal dispersion) -> $7.39. Then we shade (via auction-first-price-shading: 0.90 with risk-aversion nudge for 6 bidders, log-normal) -> $7. April and role are fine -- bid $7, ceiling $7."

---

## Worked Example: Closer Change Mid-Season

**Scenario**: Incumbent closer IL'd, setup guy named interim. Week 10 (mid-June), $65 FAAB remaining, thin on saves.

**Inputs**:
- `acquisition_value` = $22, `positional_need_fit` = 85, `role_certainty` = 75
- FAAB = $65, week 10, situation `closer-change`
- faab-log: 6 valid rows, league_inflation_ratio = 1.15

**Step 1 - base_value**:
```
urgency = 1.4, pace_base = 1.0, pace_calibrated = 1.0 x 1.15 = 1.15
base_value = 22 x 0.85 x 0.75 x 1.4 x 1.15 = $22.59
```

**Step 2 - Classify**: `common_value` (named closer, every save-hunting team bidding).

**Step 3 - Delegate to auction-winners-curse-haircut**:
```
inputs = { raw_valuation: 22.59, value_type: "common_value",
           n_informed_bidders: 6, signal_dispersion: 40 }

Sibling returns: haircut_pct ~27%, adjusted_valuation ~$16.49
```

**Step 4 - N estimate**: 6 teams chasing saves.

**Step 5 - Delegate to auction-first-price-shading**:
```
inputs = { true_value: 16.49, n_bidders_estimate: 6,
           value_distribution: "log-normal", risk_aversion: 0.2,
           budget_remaining: 65 }

Sibling returns: shaded_bid ~$14.81 -> round to $15
```

**Step 6 - Guardrails**: April cap skip (week 10). Not speculation. Role certainty OK.

**Output**:
- `faab_rec_bid` = $15
- `faab_max_bid` = round($16.49 x 0.90) = $15
- Rationale cites both delegations and the 1.15 league-inflation calibration.

---

## Worked Example: Private-Value Handcuff

**Scenario**: Backup reliever to the closer we already own. Week 7, $88 FAAB remaining.

**Inputs**:
- `acquisition_value` = $8, `positional_need_fit` = 90 (direct handcuff), `role_certainty` = 45
- FAAB = $88, week 7, situation `speculation` (no current role, just handcuff)

**Step 1 - base_value**:
```
urgency = 0.7 (pure speculation), pace = 1.0
base_value = 8 x 0.90 x 0.45 x 0.7 x 1.0 = $2.27
```

**Step 2 - Classify**: `private_value` (only WE own the starter he handcuffs; no other team has a specific reason to bid).

**Step 3 - Delegate to auction-winners-curse-haircut**:
```
inputs = { raw_valuation: 2.27, value_type: "private_value",
           n_informed_bidders: 2, signal_dispersion: 30 }

Sibling short-circuits: haircut_pct = 0, adjusted_valuation = $2.27, applied = false
```

**Step 4 - N estimate**: 1-2 teams (private-value; almost no competition). Set N = 2.

**Step 5 - Delegate to auction-first-price-shading**:
```
inputs = { true_value: 2.27, n_bidders_estimate: 2,
           value_distribution: "uniform" (thin-info role-player),
           risk_aversion: 0.2, budget_remaining: 88 }

Sibling returns: shade = 0.50 + 0.04 (risk adj) = 0.54
  raw = 2.27 x 0.54 = $1.22
  cap = min(1.22, 0.9 x 2.27 = 2.04, 88) = 1.22
  shaded_bid = round(1.22) = 1
```

**Step 6 - Baseball guardrails**:
- Speculation cap: situation = speculation, $1 <= 20% of $88 -- no change
- $1 floor: shaded = $1 already, no change
- Role cert floor: 45 >= 20 -- OK

**Output**:
- `faab_rec_bid` = $1
- `faab_max_bid` = round($2.27 x 0.90) = $2
- Rationale: "Handcuff to our closer -- this is a private-value claim, so no winner's-curse haircut applies (confirmed by auction-winners-curse-haircut short-circuit). Shaded via auction-first-price-shading at N=2 gives $1. Bid $1, ceiling $2 -- the rolling-list tiebreak wins against other $1 bids."
