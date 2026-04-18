---
name: mlb-trade-evaluator
description: Computes the full impact of a proposed MLB fantasy trade across all 10 H2H categories (R/HR/RBI/SB/OBP, K/ERA/WHIP/QS/SV), rest-of-season dollar value, positional flexibility, and weeks 21-23 playoff impact. Produces a signed verdict (accept / counter / reject) with rationale and a specific counter if applicable. Use when user mentions "trade evaluation", "trade value", "should I accept", "trade delta", "counter offer", or pastes in a trade proposal from Yahoo. Biased toward reject by default — most trade offers extract value.
---
# MLB Trade Evaluator

## Table of Contents
- [Example](#example)
- [Workflow](#workflow)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Example

**Scenario**: Opponent offers Aaron Judge (OF) for Bobby Witt Jr. (SS) + Spencer Strider (SP). Today is 2026-06-10. User is 4th in 12-team league. `cat_pressure` signals from `mlb-category-state-analyzer`: SB pressure 85, HR pressure 55, K pressure 70, QS pressure 80, OBP pressure 60; others 40-50. User has spare OF depth but thin SS.

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

**Trade value delta** = $34 − ($32 + $26) = **−$24**.

**Positional flex delta**: −30 (lose a scarce SS, gain a surplus OF).
**Playoff impact** (weeks 21-23): Judge's schedule has 19 games vs Witt's 18 + Strider's 4 starts → **−35** (lose 4 starts of Ks/QS during championship weeks).

**Verdict**: **REJECT**. Offer extracts $24 of value, cripples SB (which we need) and pitching counting stats (K, QS), and weakens SS position. Counter only if opponent adds a comparable SP (e.g., Logan Webb) AND a speed source — otherwise walk away.

**Suggested counter**: Witt + Strider for Judge + [their Logan Webb] + [their Esteban Ruiz]. If opponent refuses, REJECT.

## Workflow

Copy this checklist and track progress:

```
Trade Evaluation Progress:
- [ ] Step 1: Parse the offer (players in, players out, both sides)
- [ ] Step 2: Pull rest-of-season ATC projections for every player
- [ ] Step 3: Compute per-category deltas (counting + ratio)
- [ ] Step 4: Apply cat_pressure weights from category-state-analyzer
- [ ] Step 5: Compute trade_value_delta in dollars
- [ ] Step 6: Assess positional_flex_delta
- [ ] Step 7: Compute playoff_impact (weeks 21-23 only, July+)
- [ ] Step 8: Render verdict + counter (if applicable) with bias toward reject
```

**Step 1: Parse the offer**

Record exactly who is being given up and who is being received, on both sides. Trades are zero-sum within the league, so if the opponent benefits, we lose. See [resources/template.md](resources/template.md#trade-offer-input) for the input schema.

- [ ] List all players moving to our roster (IN)
- [ ] List all players moving off our roster (OUT)
- [ ] Note each player's Yahoo position eligibility (C/1B/2B/3B/SS/OF/Util/SP/RP)
- [ ] Note any IL status, trade protection clauses, or two-start weeks in flight

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

Read the most recent `signals/YYYY-MM-DD-cat-state.md` from `mlb-category-state-analyzer`. For each of the 10 cats, multiply the raw delta by `cat_pressure / 50` (so pressure 50 = neutral weight 1.0; pressure 100 = double; pressure 0 = zero weight because we already punt that cat).

- [ ] Weighted delta = raw_delta × (cat_pressure / 50)
- [ ] Sum the weighted deltas → `cat_pressure_weighted_delta`

**Step 5: Compute `trade_value_delta`**

Use FanGraphs Auction Calculator rest-of-season dollar values (or Razzball as fallback).

```
trade_value_delta = Sum($ of players IN) − Sum($ of players OUT)
```

If positive by ≥$5, that's a real value gain. Within ±$5 is noise.

**Step 6: Assess `positional_flex_delta`**

Score −100 to +100 based on how the trade changes roster flexibility. See [resources/methodology.md#positional-flex-scoring](resources/methodology.md#positional-flex-scoring).

- Gaining a scarce position (C, SS, 2B) from surplus = positive
- Losing a scarce position = negative
- Gaining multi-position eligibility = positive
- Consolidating two bench players into one starter = positive (frees bench)

**Step 7: Compute `playoff_impact` (July 1+ only)**

For trades made July 1 or later, evaluate specifically for championship weeks 21, 22, 23. Read the `mlb-playoff-scheduler` signal file for `playoff_games` and `playoff_matchup_quality` per player. If neither exists, note the gap.

```
playoff_impact = Sum(playoff_games × matchup_quality of IN)
               − Sum(playoff_games × matchup_quality of OUT)
```

Normalize to 0-100 where 50 = neutral.

**Step 8: Render verdict**

Apply the decision logic with **explicit bias toward REJECT** (see Guardrails #1):

- `cat_pressure_weighted_delta` strongly positive (>+30) AND `trade_value_delta` ≥ +$5 AND `positional_flex_delta` ≥ 0 → **ACCEPT**
- `trade_value_delta` is mixed (−$5 to +$10) OR deltas positive on some cats, negative on cats we need → **COUNTER** (with specific suggested counter)
- `trade_value_delta` ≤ −$5 OR negative on high-pressure cats → **REJECT**

Every verdict ends with a single-verb recommendation: `ACCEPT`, `COUNTER (with specific proposal)`, or `REJECT`. No "consider."

See [resources/template.md#verdict-block](resources/template.md#verdict-block) for output schema. Validate using [resources/evaluators/rubric_mlb_trade_evaluator.json](resources/evaluators/rubric_mlb_trade_evaluator.json). Minimum average score to ship: 3.5.

## Common Patterns

**Pattern 1: Star-for-depth offer**
- Opponent offers one star for two or three of our mid-tier players. Opponent gains roster slot flexibility; we gain a headline name.
- **Typical trap**: dollar values look close, but opponent frees bench slots to stream from waivers.
- **Rule**: only accept if the incoming star covers multiple category deficits AND the players we give up are genuinely droppable-tier on waivers. Otherwise REJECT.

**Pattern 2: Category-targeted swap**
- Symmetric-value trade where both sides target their weaknesses (e.g., opponent gives us K/QS for our HR/RBI).
- **Diagnostic**: does the swap match OUR `cat_pressure`, or does it match THEIRS? If theirs, REJECT.
- **Rule**: only accept if the categories we gain have pressure ≥70 AND the categories we give up have pressure ≤40 (i.e., we're already winning or punting them).

**Pattern 3: Buy-low / sell-high regression play**
- Offer involves a player currently over/underperforming their underlying metrics. Cross-reference `mlb-regression-flagger` signal.
- **Rule**: if their player's `regression_index` is sharply positive (unlucky, will bounce back) and ours is sharply negative (lucky, will fall off), ACCEPT even if headline dollars look flat.

**Pattern 4: Injury-adjacent desperation offer**
- Opponent's player is on IL or nursing a minor injury. Offer dangles a discount.
- **Rule**: verify IL status via RotoWire injury report before any other analysis. If the injury projects to cost >4 weeks, the FanGraphs projection likely has not repriced yet — re-compute manually. Usually REJECT because ATC is stale on injuries.

**Pattern 5: Playoff-week schedule arbitrage (July+)**
- Incoming player has 20 games in weeks 21-23; outgoing has 14. Even if ROS dollar value is flat, playoff value differs.
- **Rule**: weight `playoff_impact` heavily (×2) for any trade proposed July 15 or later.

## Guardrails

1. **Bias toward REJECT.** Most trade offers are sent because the opponent expects to extract value. Default to REJECT unless the math clearly shows a gain of ≥$5 AND positive weighted category delta AND non-negative positional flex. Tie goes to reject.

2. **Use rest-of-season projections, never full-season or season-to-date.** A player who has already banked 20 HRs is worth less for the remaining schedule than his full-season line suggests. ATC rest-of-season is the right denominator.

3. **Ratio categories need volume weighting.** OBP, ERA, WHIP deltas are meaningless as simple averages. A .400 OBP hitter with 200 remaining PAs affects team OBP more than a .350 OBP hitter with 500. Always weight by PA (hitters) or IP (pitchers). See methodology.

4. **Read the `cat_pressure` signal first.** If `mlb-category-state-analyzer` has not emitted for today, run it first. Using stale pressure weights (or uniform 1.0) will systematically over-value categories the user is already winning and under-value ones he needs.

5. **Quantify the counter — don't say "ask for more."** If the verdict is COUNTER, propose a specific alternative package: "Ask them to swap [Player X] for [Player Y]" or "Ask for [Player Z] as a throw-in." Vague counters are useless to a beginner user.

6. **Check for trade deadline proximity.** Yahoo's deadline is **August 6**. Trades proposed after the deadline are invalid; trades proposed in the week before should trigger a deadline-proximity note because the user cannot un-do a bad trade.

7. **Check for commissioner review.** This league has commissioner review with 1-day reject window. If the trade is manifestly lopsided toward us, note that the commissioner may reverse it. If toward opponent, no such protection exists.

8. **Two-way impact.** Every trade also affects the opponent. If the opponent is a direct competitor for a playoff seed, a trade that helps them is doubly bad. Note opponent identity in the output block.

9. **Beginner-voice output.** The user has zero baseball knowledge. Translate every stat into plain English at least once: "OBP (how often the batter reaches base — higher is better, league average is .315)." Every user-facing recommendation ends with one of: `ACCEPT` / `COUNTER (with specific package)` / `REJECT`.

10. **Log the decision.** Emit via `mlb-decision-logger` to `tracker/decisions-log.md` with full signal values, verdict, confidence, and `will_verify_on` date (set to 4 weeks out).

## Quick Reference

**Key formulas:**

```
Counting-cat delta (cat C):
  delta_C = Sum(projected_C of IN players) − Sum(projected_C of OUT players)

Ratio-cat delta (OBP example):
  ROS_OBP_IN = Sum(OBP_i × PA_i) / Sum(PA_i)  for IN players
  ROS_OBP_OUT = Sum(OBP_j × PA_j) / Sum(PA_j) for OUT players
  delta_OBP = ROS_OBP_IN − ROS_OBP_OUT, then scale by roster PAs

Weighted cat delta:
  weighted_delta_C = raw_delta_C × (cat_pressure_C / 50)

Total weighted delta:
  trade_cat_delta = Sum over all 10 cats of weighted_delta_C

Trade value delta:
  trade_value_delta ($) = Sum($ROS_IN) − Sum($ROS_OUT)

Playoff impact (July+):
  playoff_impact = Sum(games_21_23 × matchup_q of IN)
                 − Sum(games_21_23 × matchup_q of OUT)

Verdict logic:
  IF weighted_delta > +30 AND value_delta ≥ +$5 AND flex_delta ≥ 0:
    ACCEPT
  ELIF weighted_delta ≥ 0 AND value_delta ≥ −$5:
    COUNTER (propose specific counter-package)
  ELSE:
    REJECT
```

**Verdict thresholds:**

| Signal | ACCEPT if | REJECT if |
|---|---|---|
| `trade_value_delta` ($) | ≥ +$5 | ≤ −$5 |
| `cat_pressure_weighted_delta` | > +30 | < 0 on any cat with pressure ≥80 |
| `positional_flex_delta` | ≥ 0 | ≤ −20 |
| `playoff_impact` (July+) | ≥ 55 | ≤ 40 |

**Key resources:**

- **[resources/template.md](resources/template.md)**: Offer input schema, per-cat delta table (both teams), value/flex/playoff blocks, verdict block with rationale and counter
- **[resources/methodology.md](resources/methodology.md)**: Projection sourcing order, counting vs ratio cat math, cat_pressure weighting, value dollars, flex scoring, playoff impact, verdict logic with reject bias
- **[resources/evaluators/rubric_mlb_trade_evaluator.json](resources/evaluators/rubric_mlb_trade_evaluator.json)**: 10 quality criteria for projection quality, cat math, pressure weighting, value calc, flex, playoff, verdict calibration, counter specificity, documentation, reject bias

**Inputs required:**

- Trade offer (players IN, players OUT, initiating opponent)
- Rest-of-season ATC projections (FanGraphs)
- Current `cat_pressure` signal (from `mlb-category-state-analyzer`)
- Auction-calculator dollar values (FanGraphs)
- Positional eligibility for each player (Yahoo)
- `regression_index` signal (from `mlb-regression-flagger`) for buy-low/sell-high check
- Injury status (RotoWire)
- If July+: `playoff_games` and `playoff_matchup_quality` per player

**Outputs produced:**

- `trade_cat_delta` per each of 10 cats (raw + pressure-weighted)
- `trade_value_delta` ($)
- `positional_flex_delta` (±100)
- `playoff_impact` (0-100, July+)
- `verdict` (accept / counter / reject) with rationale
- If COUNTER: specific alternative package to propose
- Signal file written to `signals/YYYY-MM-DD-trade-<opponent>.md`
- Decision log entry via `mlb-decision-logger`
