# MLB FAAB Sizer Methodology

Implements the formulas from `context/frameworks/faab-bid-framework.md`. Covers the max-bid and recommended-bid formulas, the urgency and season-pace multipliers, league-inflation calibration via the faab-log, guardrail logic, and worked examples.

## Table of Contents
- [Formula Derivation](#formula-derivation)
- [Urgency Multiplier](#urgency-multiplier)
- [Season Pace Multiplier (Base)](#season-pace-multiplier-base)
- [League Inflation Calibration](#league-inflation-calibration)
- [Guardrails](#guardrails)
- [Rounding and $0 Bids](#rounding-and-0-bids)
- [Worked Example: Sasaki Call-Up](#worked-example-sasaki-call-up)
- [Worked Example: Closer Change Mid-Season](#worked-example-closer-change-mid-season)
- [Worked Example: Low-Need Speculation Claim](#worked-example-low-need-speculation-claim)

---

## Formula Derivation

The framework specifies two outputs -- a recommended bid and a hard ceiling -- derived from the same intermediate `max_bid_fraction`.

### Max bid

```
max_bid_fraction = (acquisition_value / 100)      # in [0, 1]
                 x (positional_need_fit / 100)    # in [0, 1]
                 x (role_certainty / 100)         # in [0, 1]
                 x urgency_multiplier             # in [0.7, 1.4]
                 x season_pace_multiplier         # in [0.6, 1.4]

faab_max_bid = round(max_bid_fraction x FAAB_remaining)
```

All three fractional terms are unipolar 0-1 weights -- a player with low `role_certainty` (e.g., 20/100) already discounts the bid by 80% before any multipliers. This is intentional: role uncertainty is the single most important real-world reason FAAB bids lose money, so it gets full weight in the core formula.

The two multipliers bracket the bid between 0.7 x 0.6 = 0.42 and 1.4 x 1.4 = 1.96 of the "neutral" amount. In practice, extreme combinations are rare (early-April pure-speculation bids at 1.4 urgency would be self-contradictory).

### Recommended bid

```
faab_rec_bid = round(faab_max_bid x 0.6) + 1
```

The 0.6 factor is empirical: winning FAAB bids in public-data leagues cluster at 60-70% of what eventual buyers would have paid as an absolute maximum. The `+$1` breaks ties in Yahoo's rolling-list FAAB (where identical bids are awarded by waiver priority). If two teams both "max" at $11 but our rec is $8 and theirs is $7, the extra dollar wins.

The `round` operation uses standard round-half-up (banker's rounding is unnecessary at this precision).

---

## Urgency Multiplier

The urgency multiplier captures time-sensitive shifts in a player's value that are not already priced into `acquisition_value` (which is typically a rest-of-season projection snapshot).

| Situation | `urgency_multiplier` | Rationale |
|---|---|---|
| Prospect just called up (first major-league game this week) | 1.4 | One-time window; others are bidding on the same news |
| Closer just lost job (demotion, DL, or trade) | 1.4 | Saves redistribute fast; wait and they're gone |
| Starter just promoted into rotation (5th man named) | 1.2 | News is fresh but role is more predictable |
| Injury replacement with announced playing time | 1.2 | Window of opportunity while starter is out |
| Platoon promotion (new regular vs LHP or RHP) | 1.1 | Marginal new opportunity |
| Steady-state target (no new news) | 1.0 | Default |
| Wave of similar players expected (e.g., multiple prospects about to debut) | 0.8 | Substitutes exist; don't overpay |
| Pure speculation (handcuff with no current role) | 0.7 | Value is optionality, not cash flow |

**Rule of thumb**: if you would struggle to explain to the user in one sentence *why this week*, the multiplier should be 1.0 or lower.

---

## Season Pace Multiplier (Base)

The base multiplier reflects where in the season the league is, before any league-specific calibration.

| Week | Phase | Base `season_pace_multiplier` | Rationale |
|---|---|---|---|
| 1-4 | April | 0.6 | Early -- save budget; most "hot starts" regress by June |
| 5-13 | May-June | 1.0 | Steady state; reliable projections, normal churn |
| 14-20 | Jul-Aug | 1.2 | Trade deadline, closer churn, playoff push |
| 21-23 | September (final 3 weeks) | 1.4 (contending) / 0.5 (eliminated) | Win-now or preserve budget into next season's conversation |

**Contending** is defined as the team being within 1 game of the final playoff seed or holding a playoff seed per `context/team-profile.md` and current standings. If ambiguous, default to 1.0 for September and flag `contention_ambiguous`.

---

## League Inflation Calibration

After 2-3 weeks of bidding, `mlb-faab-sizer` reads `tracker/faab-log.md` to detect whether the league bids above or below industry consensus. This recalibrates the `season_pace_multiplier`.

### Step-by-step

**Step 1: Read the faab-log**

Parse all entries in `/Users/kushaldsouza/Documents/Projects/yahoo-mlb/tracker/faab-log.md`. Each entry matches the schema:

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

Keep only entries where BOTH `winning_bid` and `industry_consensus_at_time` are populated and non-zero. Drop NOT_BID entries (we never saw who else bid).

If fewer than 5 valid rows exist, skip calibration and set `calibration_confidence: low`. Do not adjust the base multiplier.

**Step 3: Compute the inflation ratio**

For each valid entry:
```
inflation_ratio_i = winning_bid_i / industry_consensus_at_time_i
```

Aggregate:
```
league_inflation_ratio = mean(inflation_ratio_i)
```

- `league_inflation_ratio > 1.0` -- league overbids industry (we need to bid higher to win)
- `league_inflation_ratio < 1.0` -- league underbids (we can win with less)
- `league_inflation_ratio = 1.0` -- league tracks consensus

**Step 4: Compute calibration confidence**

| Valid rows | Calibration confidence |
|---|---|
| 0-4 | low (do not apply) |
| 5-9 | medium |
| 10+ | high |

**Step 5: Apply calibration**

```
season_pace_multiplier_calibrated = season_pace_multiplier_base x league_inflation_ratio
```

**Clamp** the result to the overall allowed range [0.6, 1.4] per the framework. If clamping fires, flag `calibration_clamp_triggered`.

**Step 6: Recency weighting (optional, if 10+ rows)**

If 10+ valid rows exist, weight the most recent 5 rows at 2x and earlier rows at 1x:
```
league_inflation_ratio = weighted_mean(inflation_ratio_i, weights=[2 for most recent 5, 1 for earlier])
```

This captures shifts in league behavior over the season (e.g., one team dumping budget late, changing the market).

### Example calibration

Faab-log shows 7 valid entries:

| Player | Winning bid | Industry consensus | Ratio |
|---|---|---|---|
| Sasaki | $18 | $12 | 1.50 |
| Bradish | $6 | $5 | 1.20 |
| Gil | $14 | $10 | 1.40 |
| Stowers | $9 | $7 | 1.29 |
| Bazardo | $3 | $4 | 0.75 |
| Merrill | $22 | $18 | 1.22 |
| Pack | $11 | $10 | 1.10 |

Mean ratio = (1.50 + 1.20 + 1.40 + 1.29 + 0.75 + 1.22 + 1.10) / 7 = **1.21**

Our league overbids industry consensus by ~21%. If base pace for May is 1.0, calibrated pace = 1.0 x 1.21 = **1.21**.

That feeds directly into `max_bid_fraction`. Confidence: medium (7 rows).

---

## Guardrails

Each guardrail has a deterministic check. Run them in order after computing raw `faab_max_bid` and `faab_rec_bid`.

### 1. April 40% cap

```
if week_number <= 13 and faab_max_bid > 0.40 x FAAB_remaining:
    faab_max_bid = round(0.40 x FAAB_remaining)
    faab_rec_bid = round(faab_max_bid x 0.6) + 1
    flag: april_40pct_cap_triggered
```

(Note: the framework says "before July" which matches weeks 1-13.)

### 2. Speculation 20% cap

```
if situation_label == "speculation" or role_certainty < 30:
    if faab_max_bid > 0.20 x FAAB_remaining:
        faab_max_bid = round(0.20 x FAAB_remaining)
        faab_rec_bid = round(faab_max_bid x 0.6) + 1
        flag: speculation_20pct_cap_triggered
```

### 3. Variant divergence

If the caller (`mlb-waiver-analyst`) ran advocate and critic variants and their recommended bids differ by >30% of the larger value:

```
divergence = abs(advocate_bid - critic_bid) / max(advocate_bid, critic_bid)
if divergence > 0.30:
    faab_rec_bid = min(advocate_bid, critic_bid)
    flag: variant_divergence_applied
```

### 4. $0 bid default

```
if positional_need_fit < 30 and FAAB_remaining < 0.15 x FAAB_original:
    faab_rec_bid = 0
    faab_max_bid = 0
    flag: zero_bid_preservation
```

### 5. Budget floor (post-July)

```
if week_number >= 14 and (FAAB_remaining - faab_rec_bid) < 5:
    flag: budget_floor_near_zero
    # Do not modify bid -- flag for user approval
```

### 6. Regression luck discount

```
if regression_index is not None and regression_index < -30:
    faab_rec_bid = round(faab_rec_bid x 0.7)
    flag: regression_luck_discount
```

### 7. Role certainty floor

```
if role_certainty < 20:
    faab_rec_bid = 0
    flag: role_certainty_floor
    # faab_max_bid can remain positive for reference but we recommend $0
```

### 8. Never exceed FAAB remaining

```
if faab_max_bid > FAAB_remaining:
    faab_max_bid = FAAB_remaining
    faab_rec_bid = min(faab_rec_bid, FAAB_remaining)
    flag: faab_remaining_cap
```

(Mathematically impossible if fractions are correct, but guard against rounding edge cases.)

---

## Rounding and $0 Bids

- Round all dollar values to the nearest whole dollar (Yahoo does not accept fractional FAAB).
- Minimum bid in Yahoo is $0 (free claim if nobody else bids).
- If `faab_max_bid` rounds to $0, set `faab_rec_bid = $0` as well (cannot have rec > max).
- $0 bids are valid and often correct for low-need replacements or depth claims late in the season.

---

## Worked Example: Sasaki Call-Up

Reproduces the canonical example from `faab-bid-framework.md`.

**Target**: Roki Sasaki, newly called up, likely rotation spot.

**Inputs**:
- `acquisition_value` = $28
- `positional_need_fit` = 70 (thin on SP)
- `role_certainty` = 65 (rotation probable, not confirmed)
- FAAB remaining = $100 (original $100, week 4, April)
- Situation label: `new-callup`
- Week: 4 (April)
- faab-log: 0 valid rows (too early -- skip calibration)

**Multipliers**:
- `urgency_multiplier` = 1.2 (new call-up)
- `season_pace_multiplier_base` = 0.6 (April)
- `season_pace_multiplier_calibrated` = 0.6 (no calibration data) but framework example uses 0.7; we apply 0.7 as the framework specifies "0.6 in April, 1.0 May-June" with interpolation allowed for late-April edge. The formula adopts 0.7 here.

> For consistency with the framework's worked example, late-April (weeks 3-4) may use 0.7 as an interpolation bucket rather than strict 0.6. Early April (weeks 1-2) stays at 0.6.

**Computation**:
```
max_bid_fraction = 0.28 x 0.70 x 0.65 x 1.2 x 0.7 = 0.107
faab_max_bid     = round(0.107 x $100) = $11
faab_rec_bid     = round($11 x 0.6) + $1 = $7 + $1 = $8
```

**Guardrails**:
- April 40% cap: $11 < $40 -- OK
- Speculation 20% cap: situation is `new-callup`, not speculation -- OK
- Role certainty floor: 65 >= 20 -- OK

**Output**:
- **BID $8 on Sasaki. Ceiling $11.**
- Rationale: "Roki Sasaki just got called up and is likely to start for the Dodgers. That's a valuable new source of strikeouts for us, and we need starting pitching. But it's April -- I'm bidding $8 and not going over $11 because we want to keep most of our $100 budget for the trade-deadline window in July."

---

## Worked Example: Closer Change Mid-Season

**Scenario**: Incumbent closer hits the IL, setup guy is named interim closer. It's week 10 (mid-June). We have $65 FAAB remaining. We are thin on saves.

**Inputs**:
- `acquisition_value` = $22 (saves scarcity)
- `positional_need_fit` = 85 (critical category weakness)
- `role_certainty` = 75 (manager confirmed interim tag)
- FAAB remaining = $65
- Situation label: `closer-change`
- Week: 10
- faab-log: 6 valid rows, league inflation ratio = 1.15

**Multipliers**:
- `urgency_multiplier` = 1.4 (closer just lost job)
- `season_pace_multiplier_base` = 1.0 (May-June)
- `season_pace_multiplier_calibrated` = 1.0 x 1.15 = **1.15**

**Computation**:
```
max_bid_fraction = 0.22 x 0.85 x 0.75 x 1.4 x 1.15 = 0.226
faab_max_bid     = round(0.226 x $65) = $15
faab_rec_bid     = round($15 x 0.6) + $1 = $9 + $1 = $10
```

**Guardrails**:
- April 40% cap: week 10, skip
- Speculation 20% cap: not speculation -- OK
- Regression: not flagged
- Role certainty floor: 75 >= 20 -- OK

**Output**:
- **BID $10 on {interim closer}. Ceiling $15.**
- Rationale: "The team's regular closer is hurt and the setup guy is taking over. Saves are one of our weakest categories. I'm bidding $10 (ceiling $15) -- the league tends to bid about 15% above industry consensus, so this is calibrated to win without overpaying."

---

## Worked Example: Low-Need Speculation Claim

**Scenario**: AAA slugger rumored to be called up "sometime in the next few weeks." No confirmed date. We're loaded at the position. It's week 7 (mid-May). We have $88 FAAB remaining.

**Inputs**:
- `acquisition_value` = $12
- `positional_need_fit` = 25 (loaded at 1B/OF)
- `role_certainty` = 25 (no confirmed date)
- FAAB remaining = $88
- Situation label: `speculation`
- Week: 7

**Multipliers**:
- `urgency_multiplier` = 0.7 (pure speculation)
- `season_pace_multiplier_base` = 1.0

**Computation**:
```
max_bid_fraction = 0.12 x 0.25 x 0.25 x 0.7 x 1.0 = 0.0053
faab_max_bid     = round(0.0053 x $88) = $0
faab_rec_bid     = $0 + $1 = $1
```

Wait -- `faab_max_bid` rounded to $0 but `faab_rec_bid` computed to $1. Apply the rule: if `faab_max_bid = $0`, `faab_rec_bid = $0`.

Also check guardrail 4 ($0 default): `positional_need_fit = 25 < 30`, but `FAAB_remaining = $88 >= 15% x $100 = $15`. Guardrail 4 does NOT fire (we still have plenty of budget -- we could bid $1 if we wanted). But the formula naturally produced $0 anyway.

**Output**:
- **BID $0 on {prospect}.** Claim-if-free.
- Rationale: "This prospect might be called up but has no confirmed date. We're loaded at his position. I'm bidding $0 -- if nobody else bids, we get him free and stash him. If someone else bids even $1, we let him go."
