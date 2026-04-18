---
name: mlb-playoff-scheduler
description: Counts MLB games per team during the Yahoo fantasy playoff window (weeks 21, 22, 23 -- Aug 17 through Sep 6, 2026) and grades the quality of each team's opponents. Emits three signals per rostered player -- playoff_games (int, max ~21), playoff_matchup_quality (0-100), holding_value (0-100) -- that drive trade-deadline and playoff-lineup decisions. Use when the user mentions playoff weeks, weeks 21-23, playoff schedule, game count, holding value, or asks whether to keep/trade a player for the playoff run. Pre-July 1 this skill returns "insufficient signal -- too early"; from July 1 onward it fires weekly.
---
# MLB Playoff Scheduler

## Table of Contents
- [Example](#example)
- [Workflow](#workflow)
- [Signal Outputs](#signal-outputs)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Example

**Scenario**: It is 2026-07-14. The trade deadline (Aug 6) is three weeks away. User asks "should I hold Junior Caminero (TB, 3B) or trade him for a pitcher?" The trade-analyzer needs `playoff_games`, `playoff_matchup_quality`, and `holding_value` for Caminero before it can weigh the offer.

**Research pass (web search every fact, cite every URL)**:
- MLB.com schedule -> TB plays 20 games across playoff weeks 21-23 (7 / 7 / 6).
- Week 21 (Aug 17-23): TB @ BAL (3), TB vs TOR (4). Opp wOBA avg (weighted by games): 0.322
- Week 22 (Aug 24-30): TB @ NYY (3), TB vs BOS (4). Opp wOBA avg: 0.338
- Week 23 (Aug 31-Sep 6): TB vs CLE (3), TB @ DET (3). Opp wOBA avg: 0.308
- Volume-weighted average opposing-SP wOBA against RHB: 0.323

**Normalization pass**:
- `playoff_games` = 7 + 7 + 6 = **20** (strong volume; max observed in the league this year is 21)
- `playoff_matchup_quality` (hitter view) = 100 - ((0.323 - 0.300) x 1000) = 100 - 23 = **77** (opposing pitching is worse than league average -> good for Caminero)
- `holding_value` = 0.6 x normalize(20 / 21) + 0.4 x 77 = 0.6 x 95 + 0.4 x 77 = **88**

**Downstream composition**:
- `mlb-trade-analyzer` reads these. Caminero's `holding_value` = 88 is very high. If the offered pitcher's `holding_value` is 65, the trade favors the status quo -> `REJECT` or `COUNTER` with a lesser hitter.
- `mlb-playoff-planner` reads the same signals to identify roster holes for playoff weeks (e.g., any starter with `playoff_games` < 14 is a bench candidate).

**Pre-July 1 behavior**:
If the skill is invoked before 2026-07-01, it emits a minimal signal file with all three fields set to `null`, `confidence: 0.0`, and body text: "Insufficient signal -- too early. Schedule volatility (trades, rotation flux, injuries) before July makes playoff projections unreliable. Re-run after July 1."

## Workflow

Copy this checklist and track progress:

```
MLB Playoff Scheduler Progress:
- [ ] Step 1: Check date gate (today >= 2026-07-01)
- [ ] Step 2: Define the three playoff week windows (Mon-Sun)
- [ ] Step 3: For each MLB team, pull the schedule for weeks 21-23
- [ ] Step 4: Count games per team per week
- [ ] Step 5: Score each opponent (wOBA for hitters, ERA for pitchers)
- [ ] Step 6: Compute playoff_matchup_quality per team (volume-weighted)
- [ ] Step 7: Compute holding_value per team (blend volume + quality)
- [ ] Step 8: Map per-team scores to every rostered player
- [ ] Step 9: Emit signal file and validate
```

**Step 1: Check the date gate**

Today's date is inside the prompt. If today < 2026-07-01, skip Steps 2-8 and emit the "insufficient signal" stub (see [resources/methodology.md](resources/methodology.md#pre-july-stub)). Do not guess or pre-compute; schedule churn (July trades, rotation flux, call-ups) breaks pre-July projections.

**Step 2: Define playoff week windows**

Per [context/league-config.md](../../../yahoo-mlb/context/league-config.md), playoffs are weeks 21, 22, 23 and end Sunday Sep 6, 2026. Working backward (weeks are Mon-Sun):

| Fantasy Week | Start (Mon) | End (Sun) |
|---|---|---|
| Week 21 | 2026-08-17 | 2026-08-23 |
| Week 22 | 2026-08-24 | 2026-08-30 |
| Week 23 | 2026-08-31 | 2026-09-06 |

Total: 21 calendar days. Max games per team = ~21 (only if no off-days, rare).

**Step 3: Pull each MLB team's schedule**

Web-search mlb.com/schedule and FanGraphs team schedule pages. See [resources/methodology.md](resources/methodology.md#schedule-lookup) for queries and fallbacks. Cite every URL.

- [ ] MLB.com /schedule: filter by team, date range 2026-08-17 to 2026-09-06
- [ ] Cross-check against FanGraphs team page (catches recent reschedules / doubleheaders)
- [ ] Note confirmed doubleheaders (count as 2 games on the same calendar day)
- [ ] Flag any postponement risk (team in a rain-heavy city with makeup games pending)

**Step 4: Count games per team per week**

For each of the 30 MLB teams, tally games in each of the three playoff weeks. Output a 30-row grid. See [resources/template.md](resources/template.md#per-team-games-grid) for the output format.

- [ ] Games in Week 21 (integer)
- [ ] Games in Week 22 (integer)
- [ ] Games in Week 23 (integer)
- [ ] Total = sum of the three (this is the per-team `playoff_games` figure)

**Step 5: Score each opponent**

For each opponent, pull two metrics:
- **For hitter-side scoring**: opposing team's staff wOBA allowed (season-to-date through the scheduling window). Lower = tougher matchup.
- **For pitcher-side scoring**: opposing team's lineup wOBA vs RHP and vs LHP (handedness-aware). Lower = easier matchup for a pitcher.

See [resources/methodology.md](resources/methodology.md#opponent-quality-scoring) for sources and lookup procedure. Use season-to-date as of the run date; do not forecast.

**Step 6: Compute `playoff_matchup_quality`**

Volume-weighted across all games in weeks 21-23:

```
For hitters on team T:
  avg_opp_wOBA_allowed = sum over games g of (opp_staff_wOBA_allowed_g) / playoff_games_T
  playoff_matchup_quality = 100 - (avg_opp_wOBA_allowed - 0.300) x 1000
  (clamped [0, 100]; league-average staff wOBA allowed ~ 0.320 -> score ~ 80)

For pitchers on team T:
  avg_opp_lineup_wOBA = sum over games g of (opp_lineup_wOBA_vs_P_handedness_g) / playoff_games_T
  playoff_matchup_quality = 100 - (avg_opp_lineup_wOBA - 0.300) x 1000
  (same clamp; easier-hitting opposing lineups -> higher quality for this pitcher)
```

Anchor: 50 = neutral opponent strength. See [resources/methodology.md](resources/methodology.md#normalization-rules) for the derivation.

**Step 7: Compute `holding_value`**

Blend volume and quality:

```
volume_score = (playoff_games / 21) x 100
holding_value = 0.6 x volume_score + 0.4 x playoff_matchup_quality
               (clamped [0, 100])
```

Rationale: more games carry more weight than softer opponents (volume is certain; opponent wOBA will wobble). See [resources/methodology.md](resources/methodology.md#holding-value-weights) for the weight justification and alternative blends (e.g., punting specific categories changes the weights).

**Step 8: Map team scores to players**

Every rostered player on team T inherits team T's three signals. Pitchers further modify `playoff_matchup_quality` by handedness (the lineup they face varies L/R). See [resources/methodology.md](resources/methodology.md#pitcher-handedness-adjustment).

**Step 9: Emit and validate**

Write to `signals/YYYY-MM-DD-playoff.md` using [resources/template.md](resources/template.md). Call `mlb-signal-emitter` for schema validation. Score the output against [resources/evaluators/rubric_mlb_playoff_scheduler.json](resources/evaluators/rubric_mlb_playoff_scheduler.json). Minimum standard: average 3.5+.

## Signal Outputs

| Signal | Range | Meaning |
|---|---|---|
| `playoff_games` | int 0-21 | Games scheduled across fantasy weeks 21+22+23 (Aug 17 - Sep 6). Max ~21 assuming no off-days. |
| `playoff_matchup_quality` | 0-100 | Volume-weighted opponent strength. 50 = neutral. >50 = softer opponents (good to hold). Hitter view uses opposing staff wOBA allowed; pitcher view uses opposing lineup wOBA vs this pitcher's hand. |
| `holding_value` | 0-100 | 0.6 x volume + 0.4 x quality. Primary signal for hold-vs-trade decisions. >70 = strong hold; <40 = trade candidate if you can get a higher-value bat/arm back. |

Downstream: `mlb-trade-analyzer` uses `holding_value` to value both sides of any proposed deal. `mlb-playoff-planner` uses `playoff_games` to flag bench vs start decisions for playoff weeks.

## Guardrails

1. **Pre-July 1, return the stub.** Do not pre-compute. Before July, 30-40% of teams will see rotation, bullpen, or lineup churn that invalidates opponent-quality scoring. The stub is honest; a precomputed signal is false precision.

2. **50 is neutral, always.** Every 0-100 score anchors to 50 at league average. If your distribution doesn't hit 50 at the median MLB team, re-anchor.

3. **Cite every URL.** Game counts, doubleheaders, and opponent wOBA must each be traceable to a specific mlb.com/schedule or FanGraphs URL in `source_urls:`. Signals without sources get `confidence <= 0.3` and are red-teamed.

4. **Doubleheaders count as 2.** If MLB.com schedule lists two games on the same calendar day, that is 2 games for that team. Some scraped sources collapse them -- cross-check.

5. **Use handedness-specific opponent wOBA for pitchers.** A LHP facing the Yankees (heavy LHB lineup) is not the same as a RHP facing the Yankees. Use opposing lineup wOBA vs LHP for LHP pitchers, vs RHP for RHP.

6. **Season-to-date wOBA, not projection.** The opponent quality score uses actual season stats as of the run date. Do not project forward -- projections add noise without adding signal for this short 3-week window.

7. **Max games = ~21, not 21 exactly.** A team playing every day would log 21 games but off-days are built into the MLB schedule. Typical range is 17-20. A team with 21 games has a doubleheader somewhere; flag it (DH games are often bullpen games, which changes matchup quality).

8. **Holding value is not trade value.** `holding_value` answers "is this player more valuable for MY playoff run than the replacement-level player available?" It is not a generic trade-market price. The trade-analyzer combines `holding_value` with market value to reach the final verdict.

9. **Re-run weekly after July 1.** Schedules change (rainouts, makeup games, early-September call-ups alter opponent lineups). The playoff-planner fires every Sunday; refresh these signals each time.

## Quick Reference

**Playoff week windows (2026)**:

```
Week 21: Mon 2026-08-17 -> Sun 2026-08-23
Week 22: Mon 2026-08-24 -> Sun 2026-08-30
Week 23: Mon 2026-08-31 -> Sun 2026-09-06
Total: 21 calendar days; max ~21 games per team
```

**Key formulas**:

```
playoff_games = games_wk21 + games_wk22 + games_wk23

For hitters:
  playoff_matchup_quality = 100 - (avg_opp_staff_wOBA_allowed - 0.300) x 1000
  (clamped [0, 100]; league avg ~ 0.320 -> 80)

For pitchers:
  playoff_matchup_quality = 100 - (avg_opp_lineup_wOBA_vs_hand - 0.300) x 1000
  (same clamp)

volume_score = (playoff_games / 21) x 100

holding_value = 0.6 x volume_score + 0.4 x playoff_matchup_quality
               (clamped [0, 100])

Pre-July 1: playoff_games = null, playoff_matchup_quality = null,
            holding_value = null, confidence = 0.0,
            body = "insufficient signal -- too early"
```

**Key sources** (see [context/frameworks/data-sources.md](../../../yahoo-mlb/context/frameworks/data-sources.md)):

- MLB schedule: https://www.mlb.com/schedule
- FanGraphs team schedule: https://www.fangraphs.com/teams/{team}/schedule
- Team staff wOBA allowed: https://www.fangraphs.com/leaders.aspx (pitching leaders, team totals)
- Team lineup wOBA vs RHP/LHP: https://www.fangraphs.com/leaders.aspx (batting, splits -> team totals)
- Park factors (for cross-check): https://www.fangraphs.com/guts.aspx?type=pf&season=2026

**Inputs required**: run date (always passed in); optionally, a roster list to scope output (else, emit all 30 teams).

**Outputs produced**: one signal file at `signals/YYYY-MM-DD-playoff.md` with YAML frontmatter, a 30-row per-team games grid, per-team opponent-quality table, and per-player mapping for rostered players. Fails-open pre-July 1 with the stub.

**Key resources**:

- **[resources/template.md](resources/template.md)**: Signal file template, per-team games grid, per-player mapping table
- **[resources/methodology.md](resources/methodology.md)**: Schedule lookup procedure, opponent quality scoring, normalization formulas, pre-July stub behavior, handedness adjustments
- **[resources/evaluators/rubric_mlb_playoff_scheduler.json](resources/evaluators/rubric_mlb_playoff_scheduler.json)**: 8-criterion quality rubric
