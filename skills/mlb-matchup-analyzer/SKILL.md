---
name: mlb-matchup-analyzer
description: Analyzes a single MLB game from a fantasy perspective given home team, away team, and date. Emits structured matchup signals -- opp_sp_quality, park_hitter_factor, park_pitcher_factor, weather_risk, bullpen_state -- and a short narrative of platoon implications (handedness matchup for hitters). Use when preparing daily start/sit calls, evaluating a streaming pitcher's environment, sizing weather risk, or when user mentions matchup analysis, park factor, opposing pitcher, weather risk, or platoon.
---
# MLB Matchup Analyzer

## Table of Contents
- [Example](#example)
- [Workflow](#workflow)
- [Signal Outputs](#signal-outputs)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Example

**Scenario**: User needs to decide whether to start Junior Caminero (TB, RHB) for today's game. Game: Tampa Bay Rays @ Colorado Rockies, 2026-04-17, Coors Field.

**Research pass (web search, cite every URL)**:
- MLB.com probable pitchers -> COL SP is German Marquez (RHP), 2026 ERA 5.10, K% 19.0%, hard-hit% 43%
- FanGraphs park factors 2026 -> Coors Field: wOBAcon 1.18 (league-leading hitter park)
- RotoWire weather (Denver, 7:10 PT first pitch) -> 82F, 0% precip, wind out to CF 9 mph
- RotoBaller closer chart -> COL bullpen: closer healthy, setup mix stable; TB bullpen: closer used 3 of last 4, likely unavailable

**Normalization pass**:
- `opp_sp_quality` (COL SP viewed from TB hitters' side): Marquez is below-average -> low hitter-opposition. Score = 30 (50 = league-average starter; lower = easier matchup for hitters).
- `park_hitter_factor`: Coors wOBAcon 1.18 -> normalize so 1.00 = 50. Score = **74** (very hitter-friendly).
- `park_pitcher_factor`: inverse of above. Score = **26** (very unfriendly to pitchers).
- `weather_risk`: 0% precip + mild temp + supportive wind -> **8** (very low disruption risk).
- `bullpen_state` (for the home team, COL): closer rested, setup healthy -> **65**. (For TB: closer gassed -> **35**.)

**Platoon narrative (plain English, no jargon)**:
"Caminero hits right-handed and faces a right-handed pitcher. This is a neutral handedness matchup, not a platoon advantage. However, Caminero's hard-hit rate vs RHP is above his season average, and Coors Field is the best hitter park in baseball, so the overall matchup is strongly positive."

**Composed downstream**: `mlb-player-analyzer` reads these signals and produces `matchup_score` = 40% opp_sp + 25% park_hitter + 25% platoon + 10% weather -> ~72 for Caminero today. That feeds `daily_quality` -> `START`.

## Workflow

Copy this checklist and track progress:

```
MLB Matchup Analysis Progress:
- [ ] Step 1: Collect game identifiers (home, away, date, first pitch time)
- [ ] Step 2: Identify both probable starting pitchers + handedness
- [ ] Step 3: Pull park factors (home park)
- [ ] Step 4: Pull weather forecast for first-pitch window
- [ ] Step 5: Assess bullpen state for both teams
- [ ] Step 6: Normalize each signal to 0-100 (50 = neutral)
- [ ] Step 7: Write platoon narrative (plain English)
- [ ] Step 8: Emit signal file and validate
```

**Step 1: Collect game identifiers**

- [ ] Home team, away team, local game date, first-pitch time, venue
- [ ] Confirm the game is not already postponed or rescheduled

**Step 2: Identify probable starters**

Pull from MLB.com probable pitchers (https://www.mlb.com/probable-pitchers). See [resources/methodology.md](resources/methodology.md#probable-pitcher-research) for search procedure and fallbacks.

- [ ] Home SP: name, handedness (L/R), season ERA, K%, xFIP
- [ ] Away SP: same fields
- [ ] Role certainty: is the start confirmed or only projected?

**Step 3: Pull park factors**

Use FanGraphs 2026 park factors (guts.aspx?type=pf). See [resources/methodology.md](resources/methodology.md#park-factor-normalization) for the normalization formula (raw factor -> 0-100 scale).

- [ ] Composite park factor (hitter perspective)
- [ ] Composite park factor (pitcher perspective)
- [ ] Handedness-specific factors (L/R) if material

**Step 4: Pull weather forecast**

Use RotoWire weather (rotowire.com/baseball/weather-forecast.php). See [resources/methodology.md](resources/methodology.md#weather-risk-computation) for the risk formula.

- [ ] Precipitation probability at first-pitch window
- [ ] Temperature + wind direction + wind speed
- [ ] Is this a dome / retractable-roof park? (overrides weather)
- [ ] Game importance multiplier (standings-critical games face more delay/reschedule friction)

**Step 5: Assess bullpen state**

Use RotoBaller closer depth chart + last-7-day usage reports. See [resources/methodology.md](resources/methodology.md#bullpen-state-assessment).

- [ ] Closer availability (appearances in last 3 days, pitch counts)
- [ ] High-leverage setup arms available
- [ ] Any IL additions or demotions in last 72 hours

**Step 6: Normalize signals**

Every signal must land on a 0-100 scale where **50 = league-average / neutral**. See [resources/methodology.md](resources/methodology.md#normalization-rules) for each signal's formula.

- [ ] `opp_sp_quality` computed from each side's perspective
- [ ] `park_hitter_factor` anchored so neutral park = 50
- [ ] `park_pitcher_factor` = 100 - park_hitter_factor (approximate inverse)
- [ ] `weather_risk` = rain_prob_pct x importance_multiplier, capped at 100
- [ ] `bullpen_state` computed per team (home + away)

**Step 7: Write platoon narrative**

Per [CLAUDE.md](../../../yahoo-mlb/CLAUDE.md) rule 5: jargon-free or translated inline. For each key hitter of interest, state handedness and the SP's handedness, then describe the platoon edge or lack thereof in plain English. See [resources/template.md](resources/template.md#platoon-narrative-template).

**Step 8: Emit and validate**

Write to `signals/YYYY-MM-DD-matchup.md` using [resources/template.md](resources/template.md). Call `mlb-signal-emitter` for validation. Validate against [resources/evaluators/rubric_mlb_matchup_analyzer.json](resources/evaluators/rubric_mlb_matchup_analyzer.json). Minimum standard: average score 3.5+.

## Signal Outputs

| Signal | Range | Meaning |
|---|---|---|
| `opp_sp_quality` | 0-100 | Opposing starter's true-talent + today's matchup. 50 = league-average SP. Higher = tougher matchup for the hitters facing them. |
| `park_hitter_factor` | 0-100 | 50 = neutral. >50 = hitter-friendly (Coors, Cincinnati). <50 = pitcher-friendly (Oracle, T-Mobile). |
| `park_pitcher_factor` | 0-100 | 50 = neutral. >50 = pitcher-friendly. Typically ~= 100 - park_hitter_factor, with small corrections for park-specific effects (foul territory, etc.). |
| `weather_risk` | 0-100 | 0 = dome or perfect conditions. 100 = high postponement + in-game disruption risk. |
| `bullpen_state` | 0-100 | Per team. 50 = normal. >50 = bullpen healthy and rested. <50 = gassed / depleted / IL-depleted. |

Plus a narrative block covering platoon implications for both lineups.

## Guardrails

1. **50 is neutral, always.** Every signal is anchored so 50 = league-average. If your formula produces a distribution that doesn't hit 50 at the median, it's wrong -- re-anchor.

2. **Cite every URL.** Every signal value must be traceable to a specific source URL in `source_urls:`. If a fact cannot be verified via web search, drop `confidence` to 0.3 or lower and flag in red team.

3. **Park factors are context-dependent.** Handedness splits matter: Yankee Stadium favors LHB; Fenway's Green Monster favors RHB pull-hitters. If a key hitter has extreme splits, use the handedness-specific park factor, not the composite.

4. **Weather = rain probability x importance multiplier.** A 30% rain chance matters more in a September pennant race than in April. See methodology for the importance multiplier.

5. **Bullpen state is per team, not per game.** Emit two values: `bullpen_state_home` and `bullpen_state_away`. Downstream consumers pick the one they need (e.g., the streaming-strategist cares about the opposing bullpen for a late-game lead).

6. **Platoon narrative must be jargon-free.** Never write "positive splits vs RHP." Write "hits right-handed pitchers better than left-handed pitchers." Translate every stat the first time it appears.

7. **Dome overrides weather.** If the home park is a dome (or the roof is confirmed closed), set `weather_risk` = 0 regardless of forecast, and note the roof status in the signal body.

8. **Both SPs, both sides.** The signal file should report `opp_sp_quality` from both perspectives: the home team's hitters face the away SP, and vice versa. Do not pick only one.

## Quick Reference

**Key formulas**:

```
park_hitter_factor = 50 + (raw_wOBAcon_factor - 1.00) * 200
  (clamped to [0, 100]; neutral park wOBAcon ~ 1.00 -> 50)

park_pitcher_factor = 100 - park_hitter_factor (first-order approximation)

opp_sp_quality = 50 + (lg_avg_xFIP - SP_xFIP) * 15
  (better SP = higher score = tougher on opposing hitters)

weather_risk = min(100, rain_prob_pct * importance_multiplier)
  importance_multiplier: 1.0 (early season) .. 1.5 (playoff push) .. 2.0 (postseason)

bullpen_state = 50
  - 15 if closer unavailable
  - 10 per high-leverage arm unavailable
  + 5 if closer had 2+ days rest and full bullpen rested
  (clamped [0, 100])
```

**Key sources** (see `context/frameworks/data-sources.md` for the full list):

- Probable pitchers: https://www.mlb.com/probable-pitchers
- Park factors: https://www.fangraphs.com/guts.aspx?type=pf&season=2026
- Weather: https://www.rotowire.com/baseball/weather-forecast.php
- Bullpen: https://www.rotoballer.com/mlb-saves-closers-depth-charts/226767
- Platoon splits: FanGraphs player page -> Splits tab

**Inputs required**: home team, away team, date (YYYY-MM-DD), first-pitch time (optional).

**Outputs produced**: one signal file at `signals/YYYY-MM-DD-matchup.md` with frontmatter + matchup summary table + platoon narrative + source URLs.

**Key resources**:

- **[resources/template.md](resources/template.md)**: Signal file template with YAML frontmatter, matchup summary table, platoon narrative block
- **[resources/methodology.md](resources/methodology.md)**: Where to search, normalization formulas, park factor conversion, weather risk computation, bullpen assessment
- **[resources/evaluators/rubric_mlb_matchup_analyzer.json](resources/evaluators/rubric_mlb_matchup_analyzer.json)**: 8-criterion quality rubric
