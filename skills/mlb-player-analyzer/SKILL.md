---
name: mlb-player-analyzer
description: Deep-dive analysis of a single MLB player (hitter or pitcher) for the Yahoo Fantasy Baseball 2K25 league. Web-searches FanGraphs (ATC projections), Baseball Savant (xwOBA/xBA/xERA), MLB.com (lineups, probables), RotoWire (weather, injuries), and RotoBaller (closer depth) to produce the full set of structured player signals defined in the signal framework. Emits form_score, matchup_score, opportunity_score, daily_quality, regression_index, obp_contribution, sb_opportunity, role_certainty for hitters and qs_probability, k_ceiling, era_whip_risk, streamability_score, two_start_bonus, save_role_certainty for pitchers. Use when you need to analyze player, compute daily_quality, compute regression index, produce player signals, run a hitter analysis, run a pitcher analysis, or prep start/sit inputs for the lineup optimizer.
---

# MLB Player Analyzer

## Table of Contents
- [Example](#example)
- [Workflow](#workflow)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Example

**Scenario**: Hitter analysis for Junior Caminero (TB 3B), today's opponent BOS, opp SP Brayan Bello (RHP), park Fenway, light wind.

**Inputs assembled from web search**:
- Last 15 days xwOBA: .410 vs season xwOBA .355 (Baseball Savant)
- Bello 2026 K/9: 8.1, xFIP 4.05, wOBA-vs-RHH .335 (FanGraphs)
- Fenway park factor: 103 R, 105 HR (FanGraphs park factors)
- Caminero vs RHP wOBA: .360 (FanGraphs splits)
- Weather: 62F, 8mph wind LF-to-CF (RotoWire)
- Lineup: confirmed #3 hitter (MLB.com starting lineups)
- Season actual wOBA .340 vs xwOBA .370 -> unlucky +.030

**Signal computation**:

| Signal | Value | Quick read |
|---|---|---|
| form_score | 66 | rolling xwOBA 15% above season baseline |
| matchup_score | 58 | decent park, neutral SP, slight wind-aided |
| opportunity_score | 78 | #3 slot, ~4.6 expected PAs |
| daily_quality | 66 | START-tier (>=60) |
| regression_index | +15 | unlucky, buy-window |
| obp_contribution | 62 | projected .355 OBP x 4.6 PAs |
| sb_opportunity | 35 | Bello holds runners average, BOS catcher CS 28%, Caminero sprint 26.5 ft/s |
| role_certainty | 100 | confirmed lineup posted |

**Recommendation to lineup-optimizer**: `daily_quality = 66` -> START. `regression_index = +15` suggests no need to sit on any recent cold-streak noise.

**Pitcher counter-example (pitcher start)**: Bowden Francis (TOR) at COL. daily_quality replaced by `streamability_score`. Coors kills `streamability_score` regardless of raw stuff; skill would emit qs_probability ~28, k_ceiling ~40, era_whip_risk ~82 -> streamability_score ~32 (sub-70 threshold -> SIT / DO NOT STREAM).

## Workflow

Copy this checklist and track progress:

```
MLB Player Analysis Progress:
- [ ] Step 1: Classify player (hitter vs pitcher; SP vs RP)
- [ ] Step 2: Collect season + 15-day performance (Savant, FanGraphs)
- [ ] Step 3: Collect today's context (opp SP/hitters, park, weather, lineup)
- [ ] Step 4: Compute normalized component scores
- [ ] Step 5: Compute composite signals (daily_quality or streamability_score)
- [ ] Step 6: Check regression_index and role_certainty
- [ ] Step 7: Validate against rubric and emit signal file
```

**Step 1: Classify player**

Determine role: hitter (any position player), SP (starter), RP (reliever, closer or setup). The signal set is different per role. See [resources/methodology.md](resources/methodology.md#role-classification) for role determination rules when a player has dual eligibility (two-way player, opener + bulk).

- [ ] Confirm today's role: is the player in today's lineup? Is the SP on the probable-pitcher chart today?
- [ ] If RP: is this a save-role RP or middle-relief RP? Closer depth lookup required.

**Step 2: Collect performance data**

Web-search the primary sources. Every URL goes in the signal file's `source_urls:` list.

- [ ] Baseball Savant player page: season xwOBA, 15-day xwOBA, xBA, barrel %, hard-hit %, sprint speed (hitters); xERA, whiff %, chase %, CSW (pitchers)
- [ ] FanGraphs player page: ATC projections (rest-of-season rate stats), splits tab (vs LHP / vs RHP)
- [ ] If search fails for any metric: record the attempt, set `confidence: 0.3`, and note the gap in the red-team field

See [resources/data-cheatsheet](resources/methodology.md#source-cheatsheet) for exact URL patterns.

**Step 3: Collect today's context**

- [ ] Opp SP (from MLB.com probable pitchers or matchup-analyzer signal if already emitted)
- [ ] Park factor (from FanGraphs park factors, or matchup-analyzer's `park_hitter_factor` / `park_pitcher_factor`)
- [ ] Weather (from RotoWire weather-forecast, or matchup-analyzer's `weather_risk`)
- [ ] Confirmed lineup slot (from MLB.com starting-lineups; posts ~2-3h pre-game)
- [ ] If a matchup-analyzer signal file exists for today's game, consume those signals -- do not re-derive

**Step 4: Compute normalized component scores**

All raw stats are converted to 0-100 (unipolar) or +/-100 (bipolar) per the signal framework. See [resources/methodology.md](resources/methodology.md#normalization-formulas) for each formula.

- [ ] Hitter: form_score, matchup_score, opportunity_score (components of daily_quality)
- [ ] Hitter: regression_index, obp_contribution, sb_opportunity, role_certainty
- [ ] Pitcher: qs_probability, k_ceiling, era_whip_risk
- [ ] Pitcher RP: save_role_certainty

**Step 5: Compute composite signals**

- [ ] Hitter primary: `daily_quality = 0.35 * form_score + 0.40 * matchup_score + 0.25 * opportunity_score`
- [ ] Pitcher SP primary: `streamability_score = 0.40 * qs_probability + 0.30 * k_ceiling + 0.30 * (100 - era_whip_risk)`
- [ ] Pitcher SP weekly: `two_start_bonus` (bool from FantasyPros two-start page)

**Step 6: Check regression and role**

- [ ] `regression_index = clamp((xwOBA - wOBA) * 500, -100, +100)`. Positive = unlucky (buy). Negative = lucky (sell / fade).
- [ ] `role_certainty` (hitter): 100 = confirmed in today's lineup, 70 = probable per beat reporter, 40 = platoon uncertain, 0 = benched or injured
- [ ] `save_role_certainty` (RP): 100 = locked closer per RotoBaller, 50 = timeshare, 20 = 7th-inning guy

**Step 7: Validate and emit**

- [ ] Fill [resources/template.md](resources/template.md) frontmatter and tables
- [ ] Score against [resources/evaluators/rubric_mlb_player_analyzer.json](resources/evaluators/rubric_mlb_player_analyzer.json). Target average >= 3.5
- [ ] Every numeric signal has `confidence` and at least one `source_url`
- [ ] Call `mlb-signal-emitter` (validation); on failure, log to `tracker/decisions-log.md`

## Common Patterns

**Pattern 1: Hot Streak Hitter (Sell-the-News)**

- **Profile**: Rolling 15-day wOBA well above xwOBA (actual outperforming expected)
- **Signal signature**: `form_score` high (>=70), `regression_index` negative (e.g., -25)
- **Read**: Production is BABIP-aided and not backed by Statcast quality. Do not overweight recent numbers.
- **Action feed to lineup-optimizer**: trim daily_quality by ~5 points mentally; flag for the waiver-analyst if the user is considering selling high

**Pattern 2: Cold Hitter with Loud Contact (Buy-Window)**

- **Profile**: Rolling 15-day wOBA below season average but xwOBA still strong (>=season xwOBA)
- **Signal signature**: `form_score` depressed, `regression_index` positive (>=+20), barrel% still good
- **Read**: Bad-luck stretch. Underlying contact quality intact. Start through it.
- **Action**: keep daily_quality weight as computed; flag positive regression to category-strategist (this is the guy who will pop next week)

**Pattern 3: Two-Start Pitcher in a Bad Park**

- **Profile**: SP with two starts this scoring week, one of which is at COL / CIN / BOS
- **Signal signature**: `two_start_bonus = true`, but one start has `era_whip_risk` >= 70
- **Read**: Volume pays in K and QS, but a blowup in Coors could torch ERA/WHIP for the week
- **Action**: Emit both starts as separate pitcher signals, each with its own streamability_score; streaming-strategist decides whether to eat the bad park for the volume

**Pattern 4: Closer in Committee / Role Uncertainty**

- **Profile**: RP with save opportunities but manager has said "mix-and-match" or "matchup based"
- **Signal signature**: `save_role_certainty` <= 50, `k_ceiling` decent, `era_whip_risk` low
- **Read**: Rostering pays only if saves materialize. Great ratios but the fantasy cat (SV) is unreliable.
- **Action**: Note explicitly in the signal body. Waiver-analyst uses this to decide FAAB willingness.

## Guardrails

1. **Cite every fact.** Every numeric input (xwOBA, projected PAs, park factor, CS%) must trace to a URL in `source_urls:`. Unsourced claims fail the rubric's Source Citation criterion.

2. **OBP matters more than AVG for this league.** Our batting cats are R/HR/RBI/SB/OBP (not AVG). When computing `obp_contribution` and when choosing which rate stat to weight in form_score, use OBP or wOBA (which is walk-inclusive), never AVG alone. Walk rate is a feature, not a footnote.

3. **QS matters more than W for this league.** For `qs_probability`, compute the probability of 6+ IP and <=3 ER, not the probability of a win. Ignore bullpen-game starters and openers -- they score zero QS points by definition.

4. **Use ATC projections, not Steamer alone.** FanGraphs ATC is the consensus ensemble and is the most accurate single source. Steamer and ZiPS can be consulted for triangulation but do not substitute ATC without noting it.

5. **Degrade gracefully on search failure.** If a source is unreachable, do not invent numbers. Set that component's `confidence` to 0.3 and record the gap in the red-team `note` field. The red-team pass will escalate if confidence < 0.4.

6. **Do not re-derive matchup-analyzer signals.** If `signals/YYYY-MM-DD-matchup.md` exists for today's game, consume `opp_sp_quality`, `park_hitter_factor`, `park_pitcher_factor`, `weather_risk`, `bullpen_state` directly. Re-deriving wastes runtime and risks inconsistency across agents.

7. **Timestamp every signal.** `computed_at: YYYY-MM-DDTHH:MMZ`. Morning-brief calls are fresh; afternoon re-checks (once lineups post) supersede the morning signal with higher role_certainty.

8. **Range-check every number.** 0-100 signals never exceed 100 or go negative. +/-100 signals (regression_index) are clamped. The `mlb-signal-emitter` validator rejects out-of-range values -- check before calling.

9. **Plain-English body.** The frontmatter is for machines; the body must be jargon-free or translate jargon inline for the end user. "xwOBA" -> "expected offensive output based on how hard and at what angle he hit the ball, regardless of whether balls found gloves."

## Quick Reference

**Composite formulas** (see [resources/methodology.md](resources/methodology.md) for derivations):

```
daily_quality       = 0.35 * form_score + 0.40 * matchup_score + 0.25 * opportunity_score
streamability_score = 0.40 * qs_probability + 0.30 * k_ceiling + 0.30 * (100 - era_whip_risk)
regression_index    = clamp((xwOBA - wOBA) * 500, -100, +100)
```

**Action thresholds** (feed to lineup-optimizer / streaming-strategist):

| Signal | START / STREAM | Neutral | SIT / FADE |
|---|---|---|---|
| daily_quality (hitter) | >= 60 | 45-59 | < 45 |
| streamability_score (SP) | >= 70 | 55-69 | < 55 |
| save_role_certainty (RP) | >= 70 | 40-69 | < 40 |
| regression_index | >= +25 (buy) | -24..+24 | <= -25 (sell) |

**Source priority** (always try in this order):

| Need | Primary | Fallback |
|---|---|---|
| Projections | FanGraphs ATC | Steamer, ZiPS, FantasyPros |
| Statcast / xwOBA / xERA | Baseball Savant | -- (no substitute) |
| Lineup / probable SP | MLB.com | RotoWire, FanGraphs Roster Resource |
| Park factor | FanGraphs park factors | Baseball-Reference park factors |
| Weather | RotoWire weather forecast | Google weather + MLB.com game page |
| Closer depth | RotoBaller closer charts | Pitcher List, Closer Monkey |
| Two-start week | FantasyPros two-start planner | FanGraphs probables grid |

**Key resources:**

- **[resources/template.md](resources/template.md)**: Signal file template with YAML frontmatter, hitter and pitcher signal tables, plain-English body, and a worked example
- **[resources/methodology.md](resources/methodology.md)**: Source URL cheatsheet, per-signal normalization formulas, composite computation, regression math, confidence-assignment rules
- **[resources/evaluators/rubric_mlb_player_analyzer.json](resources/evaluators/rubric_mlb_player_analyzer.json)**: 9-criterion scoring rubric

**Inputs required:**

- Player name (exact, with team abbreviation if ambiguous, e.g., "Will Smith (LAD)")
- Player's MLB team (3-letter abbr)
- Today's opponent SP (if known; otherwise skill will web-search MLB.com probables)
- Today's park / weather (from matchup-analyzer signal file if available)

**Outputs produced:**

- `signals/YYYY-MM-DD-player-<lastname>-<firstinitial>.md` (one file per player analyzed per day)
- Populated with all hitter or pitcher signals per signal-framework.md
- Body includes plain-English translation for the end user
