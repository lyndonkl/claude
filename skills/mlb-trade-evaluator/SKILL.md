---
name: mlb-trade-evaluator
description: Computes the full impact of a proposed MLB fantasy trade across all 10 H2H categories (R/HR/RBI/SB/OBP, K/ERA/WHIP/QS/SV), rest-of-season dollar value, positional flexibility, slot-value optionality, adverse-selection prior, and weeks 21-23 playoff impact. Produces a signed verdict (accept / counter / reject) with rationale and a specific counter if applicable. Use when user mentions "trade evaluation", "trade value", "should I accept", "trade delta", "counter offer", or pastes in a trade proposal from Yahoo. Defaults to COUNTER in the middle band — pure REJECT is reserved for clearly predatory offers.
---
# MLB Trade Evaluator

## Table of Contents
- [Example](#example)
- [Workflow](#workflow)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Example

**Scenario**: Opponent offers Aaron Judge (OF) for Bobby Witt Jr. (SS) + Spencer Strider (SP). Today is 2026-06-10. User is 4th in 12-team league. `cat_pressure` signals from `mlb-category-state-analyzer`: SB pressure 85, HR pressure 55, K pressure 70, QS pressure 80, OBP pressure 60; others 40-50. User has spare OF depth but thin SS. Opponent archetype from `mlb-opponent-profiler`: `active`.

**Rest-of-season ATC projections** (weeks 11-23, ~105 games remaining):

| Player | R | HR | RBI | SB | OBP | K | QS | SV | $ value |
|---|---|---|---|---|---|---|---|---|---|
| Judge (incoming) | 75 | 28 | 78 | 2 | .405 | — | — | — | $34 |
| Witt (outgoing) | 70 | 20 | 65 | 25 | .355 | — | — | — | $32 |
| Strider (outgoing) | — | — | — | — | — | 165 | 12 | 0 | $26 |

**Per-category delta** (ours minus theirs, weighted by `cat_pressure`):

| Cat | Delta (raw) | Pressure | Weighted Δ |
|---|---|---|---|
| R | +5 | 45 | +2.3 |
| HR | +8 | 55 | +4.4 |
| RBI | +13 | 45 | +5.9 |
| SB | **−25** | **85** | **−21.3** |
| OBP | +.050 (×PA) | 60 | +3.0 |
| K | **−165** | **70** | **−115.5** |
| QS | **−12** | **80** | **−96.0** |
| SV | 0 | 45 | 0 |
| ERA/WHIP | neutral | 50 | 0 |
| **Sum** | | | **−217.2** |

**Raw trade value delta** = $34 − ($32 + $26) = **−$24**.

**Slot-value bonus** (principle #9): 2 players out, 1 player in → we clear **+1 net slot**; they clear 0. `slot_value_delta = (1 − 0) × $2.50 = +$2.50`.

**Adverse-selection pipeline** (delegated to `@skills/adverse-selection-prior/`):
- Inputs: `offer_type=trade`, `proposer_archetype=active`, `offer_symmetry_score=20` (pre-adj ratio −37%, clearly lopsided against us), `proposer_info_asymmetry=55`.
- Output from skill: `prior_ev_probability=0.30`, `recommended_adjustment=0.85`, rationale cites active trader selecting this offer from many possibilities despite surface lopsidedness against us.

**Adjusted trade value delta**:
```
trade_value_delta_raw       = −$24.00
+ slot_value_delta          = +$2.50
= trade_value_delta_pre_adj = −$21.50
× recommended_adjustment    = × 0.85
= trade_value_delta_adjusted= −$18.28
```

Express as % of outgoing dollars: `−$18.28 / $58 = −31.5%` → below the **−20%** REJECT threshold.

**Positional flex delta**: −30 (lose a scarce SS, gain a surplus OF).
**Playoff impact** (weeks 21-23): Judge's schedule has 19 games vs Witt's 18 + Strider's 4 starts → **−35** (lose 4 starts of Ks/QS during championship weeks).

**Verdict ladder (principle #8)**:
- `delta_pct = −31.5%`, clearly below `−20%`.
- Adverse-selection prior is 0.34 (strong evidence offer is −EV for us).
- Advocate and critic agree: SB, K, QS all crushed at high pressure.
- Triggers the narrow **REJECT** case: `delta < −20%` AND clear adverse-selection evidence.

**Verdict**: **REJECT**. Even the always-counter rule yields: we include the counter we would have sent — "Judge + Webb + Ruiz for Witt + Strider" — as the walk-away ask, but pre-commit to reject because the haircut keeps it underwater.

## Workflow

Copy this checklist and track progress:

```
Trade Evaluation Progress:
- [ ] Step 1: Parse the offer (players in, players out, both sides)
- [ ] Step 2: Pull rest-of-season ATC projections for every player
- [ ] Step 3: Compute per-category deltas (counting + ratio)
- [ ] Step 4: Apply cat_pressure weights from category-state-analyzer
- [ ] Step 5: Compute raw trade_value_delta in dollars
- [ ] Step 6: Compute slot_value_delta (optionality bonus)
- [ ] Step 7: Invoke @skills/adverse-selection-prior/ and apply the haircut
- [ ] Step 8: Assess positional_flex_delta
- [ ] Step 9: Compute playoff_impact (weeks 21-23 only, July+)
- [ ] Step 10: Render verdict + counter via the +15% / -20% ladder
```

**Step 1: Parse the offer**

Record exactly who is being given up and who is being received, on both sides. Trades are zero-sum within the league. See [resources/template.md](resources/template.md#trade-offer-input) for the input schema.

- [ ] List all players moving to our roster (IN)
- [ ] List all players moving off our roster (OUT)
- [ ] Note each player's Yahoo position eligibility (C/1B/2B/3B/SS/OF/Util/SP/RP)
- [ ] Note any IL status, trade protection clauses, or two-start weeks in flight
- [ ] Capture the opponent's team slug so we can read `context/opponents/<team>.md` for their archetype

**Step 2: Pull rest-of-season projections**

The authoritative source is **FanGraphs ATC** (ensemble projection). Fallback: FanGraphs Depth Charts, then Razzball Player Rater. For every player involved, get projected totals for remaining season.

- [ ] For hitters: rest-of-season R, HR, RBI, SB, OBP, and PAs
- [ ] For pitchers: rest-of-season K, IP, ERA, WHIP, QS, SV
- [ ] Cite each source URL in the signal file frontmatter
- [ ] If a projection is missing, drop confidence to 0.5 and flag

See [resources/methodology.md#projection-sourcing](resources/methodology.md#projection-sourcing) for detailed source order.

**Step 3: Compute per-category deltas**

For counting stats (R, HR, RBI, SB, K, QS, SV): simple sum of incoming minus outgoing.

For ratio stats (OBP, ERA, WHIP): weight by projected PAs (batters) or IP (pitchers). See [resources/methodology.md#ratio-category-math](resources/methodology.md#ratio-category-math) for the weighting formula.

- [ ] Counting stat deltas per cat
- [ ] Ratio cat deltas expressed as a shift in team average, weighted by volume
- [ ] Record each in a per-cat delta table (both teams, side by side)

**Step 4: Apply `cat_pressure` weights**

Read the most recent `signals/YYYY-MM-DD-cat-state.md` from `mlb-category-state-analyzer`. For each of the 10 cats, multiply the raw delta by `cat_pressure / 50`.

- [ ] Weighted delta = raw_delta × (cat_pressure / 50)
- [ ] Sum the weighted deltas → `cat_pressure_weighted_delta`

**Step 5: Compute raw `trade_value_delta`**

Use FanGraphs Auction Calculator rest-of-season dollar values (or Razzball as fallback).

```
trade_value_delta_raw = Sum($ of players IN) − Sum($ of players OUT)
```

This is the starting point — it does NOT yet include the slot-value bonus or the adverse-selection haircut.

**Step 6: Compute `slot_value_delta` (optionality bonus)**

Every open bench slot is worth ~$2-3 in optionality: it can host a streamer, an IL stash, or a handcuff speculation. A 2-for-1 trade frees a roster slot on one side.

```
slot_value_delta = (N_slots_cleared_for_us − N_slots_cleared_for_them) × $2.50
```

Where:
- `N_slots_cleared_for_us` = (players OUT from our side) − (players IN to our side), clamped at ≥ 0
- `N_slots_cleared_for_them` = mirror on their side

Examples:
- 1-for-1: 0 slots cleared either side → `slot_value_delta = $0`
- 2-for-1 (we send 2, get 1): +1 slot us, 0 them → **+$2.50**
- 1-for-2 (we send 1, get 2): 0 us, +1 them → **−$2.50**
- 3-for-1 (we send 3, get 1): +2 us, 0 them → **+$5.00**

Add to `trade_value_delta_raw` to form `trade_value_delta_pre_adj`.

See [resources/methodology.md#slot-value-optionality](resources/methodology.md#slot-value-optionality) for the rationale (game-theory-principles.md #9).

**Step 7: Invoke `@skills/adverse-selection-prior/` and apply the haircut**

This step operationalizes principle #4 (adverse selection on incoming offers). The evaluator does NOT compute the prior itself — it delegates to the dedicated skill and consumes the output.

- [ ] Prepare inputs for `@skills/adverse-selection-prior/`:
  - `offer_type`: `trade` (or `counter_offer` if this is a counter to a prior proposal)
  - `proposer_archetype`: read from `context/opponents/<opponent-team>.md` (one of `active`, `expert`, `dormant`, `frustrated`, `unknown`). If file missing, use `unknown`.
  - `offer_symmetry_score`: integer 0-100 derived from our own surface valuation. Map via:
    - `trade_value_delta_pre_adj / Σ($_OUT)` ≥ 0 → 72 (offer looks fair-to-favorable)
    - 0 > ratio ≥ −10% → 60
    - −10% > ratio ≥ −25% → 40
    - ratio < −25% → 20
  - `proposer_info_asymmetry`: integer 0-100. Default 50. Raise toward 80+ if any of: recent injury news we have not yet verified, closer role shift pending, lineup construction change, trade-deadline timing. See [resources/methodology.md#adverse-selection-delegation](resources/methodology.md#adverse-selection-delegation) for the scoring guide.
- [ ] Invoke `@skills/adverse-selection-prior/` with those four inputs.
- [ ] Consume the skill's output contract:
  - `prior_ev_probability` — store verbatim in the signal file.
  - `recommended_adjustment` (float, typically 0.80-1.00) — this is the multiplicative haircut.
  - `bayesian_rationale` — embed in the verdict block's rationale.
  - `override_hints` — add each hint as a red_team_finding in the signal file.
- [ ] Compute:
  ```
  trade_value_delta_adjusted = trade_value_delta_pre_adj × recommended_adjustment
  ```
- [ ] Record `adverse_selection_adjustment` in the output signal block = `1 − recommended_adjustment` (expressed as a percentage haircut, e.g., 0.88 → "12% haircut").

**Sign note:** The haircut is multiplicative on the delta. It shrinks the MAGNITUDE of our estimate in both directions — a positive delta moves toward zero (we over-estimated the gain), and a negative delta also moves toward zero (we over-estimated the loss). This is mathematically correct for an Akerlof-style prior: the skill tells us our model is less reliable than we thought, so we should anchor more toward zero. The verdict ladder compensates by setting tight thresholds (+15% / −20%) on the post-haircut percentage, so a moderately negative raw delta with a deep haircut will land in the middle band (COUNTER), while a very negative raw delta with any haircut will still clear the −20% REJECT threshold. If the haircut creates a tie at a ladder boundary, resolve toward COUNTER (per the always-counter rule).

**Step 8: Assess `positional_flex_delta`**

Score −100 to +100 based on how the trade changes roster flexibility. See [resources/methodology.md#positional-flex-scoring](resources/methodology.md#positional-flex-scoring).

- Gaining a scarce position (C, SS, 2B) from surplus = positive
- Losing a scarce position = negative
- Gaining multi-position eligibility = positive
- Consolidating two bench players into one starter = positive (frees bench)

**Step 9: Compute `playoff_impact` (July 1+ only)**

For trades made July 1 or later, evaluate specifically for championship weeks 21, 22, 23. Read the `mlb-playoff-scheduler` signal file for `playoff_games` and `playoff_matchup_quality` per player.

```
playoff_impact = Sum(playoff_games × matchup_quality of IN)
               − Sum(playoff_games × matchup_quality of OUT)
```

Normalize to 0-100 where 50 = neutral.

**Step 10: Render verdict via the +15% / −20% ladder**

Express `trade_value_delta_adjusted` as a **percent of outgoing dollars**:

```
delta_pct = trade_value_delta_adjusted / Σ($_OUT)
```

Apply the principle #8 verdict ladder:

| `delta_pct` | Verdict | Conditions |
|---|---|---|
| ≥ **+15%** | **ACCEPT** | AND advocate/critic variants agree AND no cat with pressure ≥80 has negative weighted delta |
| **−20% < delta_pct < +15%** | **COUNTER (with specific package)** | ALWAYS produce a specific counter; never pure-reject in this band |
| **≤ −20%** | **REJECT** | AND `prior_ev_probability ≤ 0.35` (clear adverse-selection evidence) |

**Always-counter rule**: in the middle band, even if our instinct is to decline, we ship a specific counter-package per principle #8 (repeated-game reputation). Rejection dismissively dries up future offers; a reasoned counter keeps the pipeline open.

**If REJECT conditions are only partially met** (e.g., `delta_pct ≤ −20%` but `prior_ev_probability > 0.35`): downgrade to COUNTER with a more demanding package.

Every verdict ends with a single-verb recommendation: `ACCEPT`, `COUNTER (with specific proposal)`, or `REJECT`. No "consider."

See [resources/template.md#verdict-block](resources/template.md#verdict-block) for output schema. Validate using [resources/evaluators/rubric_mlb_trade_evaluator.json](resources/evaluators/rubric_mlb_trade_evaluator.json). Minimum average score to ship: 3.5.

## Common Patterns

**Pattern 1: Star-for-depth offer**
- Opponent offers one star for two or three of our mid-tier players. Opponent gains a headline name; we gain slot-value bonus because the 2-for-1 frees a bench slot.
- **Typical trap**: dollar values look close, but we should still expect a haircut from adverse-selection-prior because they chose this offer.
- **Rule**: `slot_value_delta` tilts toward us (+$2.50 or +$5); but the adverse-selection haircut applies — check if `trade_value_delta_adjusted` clears +15% AND the players we give up aren't droppable-tier. If in doubt, COUNTER (not REJECT).

**Pattern 2: Category-targeted swap**
- Symmetric-value trade where both sides target their weaknesses (e.g., opponent gives us K/QS for our HR/RBI).
- **Diagnostic**: does the swap match OUR `cat_pressure`, or does it match THEIRS? If theirs, haircut is deep (symmetry actually bad for us).
- **Rule**: only ACCEPT if the categories we gain have pressure ≥70 AND the categories we give up have pressure ≤40 AND `delta_pct ≥ +15%` after haircut. Otherwise COUNTER.

**Pattern 3: Buy-low / sell-high regression play**
- Offer involves a player currently over/underperforming their underlying metrics. Cross-reference `mlb-regression-flagger` signal.
- **Rule**: if their player's `regression_index` is sharply positive (unlucky, bounce-back due) AND ours is sharply negative (lucky, regression incoming), pass this to `@skills/adverse-selection-prior/` as `proposer_info_asymmetry` of 30-40 (we plausibly have better regression info than they do). The resulting shallow haircut may let `delta_pct` clear +15%.

**Pattern 4: Injury-adjacent desperation offer**
- Opponent's player is on IL or nursing a minor injury. Offer dangles a discount.
- **Rule**: set `proposer_info_asymmetry` = 80+ (they know more about the injury). The skill will return `recommended_adjustment` ≈ 0.80. Usually COUNTER or REJECT depending on whether `delta_pct` after haircut lands below −20%.

**Pattern 5: Playoff-week schedule arbitrage (July+)**
- Incoming player has 20 games in weeks 21-23; outgoing has 14. Even if ROS dollar value is flat, playoff value differs.
- **Rule**: double-weight `playoff_impact` for any trade proposed July 15 or later. Use playoff_impact positive swings to tip close COUNTER cases into ACCEPT.

## Guardrails

1. **Always counter — pure REJECT is narrow.** Per game-theory-principles.md #8 (repeated-game reputation), rejecting fairly with a counter keeps offer pipelines open; dismissive rejection dries them up. REJECT is reserved for `delta_pct ≤ −20%` AND clear adverse-selection evidence (`prior_ev_probability ≤ 0.35`). Every other middle-band offer → COUNTER with a specific package.

2. **Delegate the adverse-selection prior — never recompute it inline.** Step 7 invokes `@skills/adverse-selection-prior/`. Do not duplicate its logic here. The skill is reused across trades, waiver drops, and future M&A/negotiation skills; keeping it single-source prevents drift.

3. **Apply the haircut to `trade_value_delta_pre_adj`, not to per-category deltas.** The prior adjusts our net dollar estimate, not individual cat contributions. The cat delta table stays un-haircut and is displayed as-is in the template.

4. **Slot-value bonus is symmetric.** If they send two and we send one, `slot_value_delta` is NEGATIVE from our perspective — they got the bench-slot optionality. Do not forget the minus sign on incoming 2-for-1s.

5. **Use rest-of-season projections, never full-season or season-to-date.** Same rule as before; atcr not atc.

6. **Ratio categories need volume weighting.** OBP, ERA, WHIP deltas must be PA- or IP-weighted.

7. **Read the `cat_pressure` signal first.** If `mlb-category-state-analyzer` has not emitted for today, run it first.

8. **Quantify the counter — don't say "ask for more."** Propose a specific alternative package with named players.

9. **Check for trade deadline proximity.** Yahoo's deadline is August 6. Flag any trade proposed in the week before.

10. **Two-way impact.** If the opponent is a direct playoff-seed competitor, the trade helping them is doubly bad. Note opponent identity and their standings proximity in the output block.

11. **Beginner-voice output.** The user has zero baseball knowledge. Translate every stat into plain English at least once. Every user-facing recommendation ends with `ACCEPT`, `COUNTER (with specific package)`, or `REJECT`.

12. **Log the decision.** Emit via `mlb-decision-logger` to `tracker/decisions-log.md` with full signal values, including `prior_ev_probability`, `recommended_adjustment`, `slot_value_delta`, `trade_value_delta_adjusted`, verdict, confidence, and `will_verify_on` date (4 weeks out).

## Quick Reference

**Key formulas:**

```
Counting-cat delta (cat C):
  raw_delta_C = Σ(projected_C of IN) − Σ(projected_C of OUT)

Ratio-cat delta (OBP example):
  PA-weighted OBP_IN and OBP_OUT, then team-level shift

Weighted cat delta:
  weighted_delta_C = raw_delta_C × (cat_pressure_C / 50)

Total cat delta:
  trade_cat_delta = Σ weighted_delta_C

Raw trade value:
  trade_value_delta_raw = Σ($_IN) − Σ($_OUT)

Slot-value bonus:
  slot_value_delta = (slots_cleared_us − slots_cleared_them) × $2.50

Pre-adjustment delta:
  trade_value_delta_pre_adj = trade_value_delta_raw + slot_value_delta

Adverse-selection haircut (via @skills/adverse-selection-prior/):
  trade_value_delta_adjusted = trade_value_delta_pre_adj × recommended_adjustment

Percent expression:
  delta_pct = trade_value_delta_adjusted / Σ($_OUT)

Playoff impact (July+):
  playoff_impact = Σ(games_21_23 × matchup_q of IN)
                 − Σ(games_21_23 × matchup_q of OUT)
```

**Verdict ladder (principle #8):**

| `delta_pct` | Verdict | Additional gates |
|---|---|---|
| ≥ +15% | ACCEPT | AND advocate/critic agree AND no pressure ≥80 cat is negative |
| −20% < d < +15% | COUNTER (with specific package) | ALWAYS — never pure-reject in this band |
| ≤ −20% | REJECT | AND `prior_ev_probability ≤ 0.35` |

**Adverse-selection prior summary (from `@skills/adverse-selection-prior/`):**

| `recommended_adjustment` | Typical cause | Effect on `delta_pct` |
|---|---|---|
| 1.00 | Dormant opponent, shallow info gap | No change |
| 0.95 | Active opponent, symmetric offer | −5% on magnitude |
| 0.90 | Standard active opponent | −10% on magnitude |
| 0.85 | Expert opponent, some info gap | −15% on magnitude |
| 0.80 | Expert opponent, material info asymmetry | −20% on magnitude |

**Key resources:**

- **[resources/template.md](resources/template.md)**: Offer input schema, per-cat delta table (both teams), value/slot/adverse-selection/flex/playoff blocks, verdict block with rationale and counter, three worked examples (ACCEPT, COUNTER, REJECT)
- **[resources/methodology.md](resources/methodology.md)**: Projection sourcing, counting vs ratio cat math, cat_pressure weighting, value dollars, slot-value optionality, delegation to adverse-selection-prior, flex scoring, playoff impact, new verdict ladder with always-counter rule
- **[resources/evaluators/rubric_mlb_trade_evaluator.json](resources/evaluators/rubric_mlb_trade_evaluator.json)**: Quality criteria including adverse-selection integration, slot-value bonus application, and verdict-ladder correctness

**Inputs required:**

- Trade offer (players IN, players OUT, initiating opponent)
- Rest-of-season ATC projections (FanGraphs)
- Current `cat_pressure` signal (from `mlb-category-state-analyzer`)
- Auction-calculator dollar values (FanGraphs)
- Positional eligibility for each player (Yahoo)
- Opponent archetype from `context/opponents/<team>.md` (written by `mlb-opponent-profiler`)
- `regression_index` signal (from `mlb-regression-flagger`) for buy-low/sell-high check and info-asymmetry scoring
- Injury status (RotoWire)
- If July+: `playoff_games` and `playoff_matchup_quality` per player
- Adverse-selection output from `@skills/adverse-selection-prior/` (Step 7)

**Outputs produced:**

- `trade_cat_delta` per each of 10 cats (raw + pressure-weighted)
- `trade_value_delta_raw` ($)
- `slot_value_delta` ($)
- `trade_value_delta_pre_adj` ($)
- `prior_ev_probability` (from delegated skill)
- `recommended_adjustment` (from delegated skill)
- `adverse_selection_adjustment` (= 1 − recommended_adjustment)
- `trade_value_delta_adjusted` ($)
- `delta_pct` (trade_value_delta_adjusted / Σ$_OUT)
- `positional_flex_delta` (±100)
- `playoff_impact` (0-100, July+)
- `verdict` (accept / counter / reject) with rationale (includes `bayesian_rationale` from adverse-selection skill)
- Counter package: always specified unless verdict is ACCEPT (even on REJECT, include the counter we would have sent as context)
- Signal file written to `signals/YYYY-MM-DD-trade-<opponent>.md`
- Decision log entry via `mlb-decision-logger`
