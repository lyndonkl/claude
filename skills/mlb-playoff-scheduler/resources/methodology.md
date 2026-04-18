# MLB Playoff Scheduler Methodology

Detailed procedures for counting games in fantasy playoff weeks 21-23, scoring opponent quality, and computing `playoff_games`, `playoff_matchup_quality`, and `holding_value`. All facts must come from web search with URL citations.

## Table of Contents
- [Pre-July Stub](#pre-july-stub)
- [Week Window Definition](#week-window-definition)
- [Schedule Lookup](#schedule-lookup)
- [Opponent Quality Scoring](#opponent-quality-scoring)
- [Normalization Rules](#normalization-rules)
- [Holding Value Weights](#holding-value-weights)
- [Pitcher Handedness Adjustment](#pitcher-handedness-adjustment)
- [Doubleheaders and Makeup Games](#doubleheaders-and-makeup-games)
- [Degraded-Data Behavior](#degraded-data-behavior)

---

## Pre-July Stub

**Rule**: If the run date < 2026-07-01, emit the stub in [resources/template.md](template.md#pre-july-stub-template) and stop. Do not web-search, do not compute.

**Why**: Schedule volatility between now and August is high enough that precomputed numbers mislead downstream agents:

1. **Deadline trades (through Aug 6)**: A rostered player may change teams in late July. Pre-July his `playoff_games` is computed against the wrong schedule.
2. **Opponent roster churn**: The wOBA-allowed of the opposing staff changes as teams shuffle rotations and call up prospects. Projections made in May are materially wrong by August.
3. **Weather-driven makeup games**: Rain postponements from April-June get makeup-dated in July-August, often as doubleheaders that inflate game counts for affected teams.
4. **Injury-driven rotation flux**: A July IL stint for an opposing ace shifts the matchup quality for that team's upcoming opponents.

The honest answer is "we don't know yet." The stub communicates that to downstream consumers. Trade-analyzer and playoff-planner must treat a `null` signal as a blocker, not a zero.

**First live run**: First Sunday on or after 2026-07-01 -> 2026-07-05. From that date, re-run every Sunday as the playoff-planner fires weekly.

---

## Week Window Definition

**Rule**: Fantasy weeks are Mon-Sun (Yahoo default). Playoffs are weeks 21, 22, 23; playoffs end Sun 2026-09-06.

Working backward from Sep 6 (Sunday):

| Fantasy Week | Start (Mon) | End (Sun) | Calendar Days |
|---|---|---|---|
| Week 21 | 2026-08-17 | 2026-08-23 | 7 |
| Week 22 | 2026-08-24 | 2026-08-30 | 7 |
| Week 23 | 2026-08-31 | 2026-09-06 | 7 |

**Total window**: 21 calendar days. **Max games per team**: ~21 (rare; most teams log 17-20). A 21-game team almost certainly has a doubleheader from a makeup game -- flag in the notes column.

**Cross-check**: If Yahoo's league page shows different week-to-date mapping (e.g., if the league commissioner shifted start-of-week for a specific holiday), the league config file wins. Re-read [context/league-config.md](../../../../yahoo-mlb/context/league-config.md) on every run to detect config changes.

---

## Schedule Lookup

**Primary source**: MLB.com schedule.
- URL pattern: `https://www.mlb.com/schedule/YYYY-MM-DD` (shows all games that day, all teams)
- Or team-scoped: `https://www.mlb.com/{team-slug}/schedule/YYYY` (full season)

**Secondary cross-check**: FanGraphs team schedule.
- URL pattern: `https://www.fangraphs.com/teams/{team}/schedule`
- FanGraphs is usually fresher on makeup games and rescheduled doubleheaders.

**Procedure**:

1. For each of the 21 calendar days (Aug 17 - Sep 6), fetch the MLB.com daily schedule page. Record every scheduled game with: date, away team, home team, start time, status.
2. For each MLB team, tally games that fall in each of the three weeks.
3. Cross-check against the team-scoped FanGraphs page for any team whose total diverges from expected norm (17-20 games).
4. Capture the URL for every page consulted into `source_urls:`.

**Search queries (when URL patterns don't resolve)**:
- `MLB schedule August 17 2026 all games`
- `Rays schedule August 2026`
- `Rays Yankees makeup game August 2026`

**Fallback**: If mlb.com is unreachable, use ESPN (`espn.com/mlb/schedule`) or CBS Sports (`cbssports.com/mlb/schedule`). Flag lower confidence (0.6 instead of 0.9) and add a red-team finding.

---

## Opponent Quality Scoring

The opponent-quality input differs for hitters vs pitchers:

### For hitters

**Metric**: Opposing team's staff-level **wOBA allowed**, season-to-date as of the run date.

**Why**: For a rostered hitter, the relevant question is "how good are the pitchers he'll face?" The aggregated staff wOBA-allowed is a clean summary -- it bakes in the rotation + bullpen + home-park effect.

**Source**:
- FanGraphs team pitching leaderboard: `https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&team=0&type=8`
- Filter: season 2026, team totals, metric = wOBA (or xwOBA if available).
- Alternative: Baseball Savant team pitching page.

**Rule**: Use staff-level, not the expected starter's individual wOBA-allowed. The staff figure is more stable and captures the bullpen innings a hitter accumulates against.

### For pitchers

**Metric**: Opposing team's **lineup wOBA** split by handedness.

**Why**: A LHP facing a LHB-heavy lineup (e.g., Yankees vs LHP) has a very different matchup than facing a RHB-heavy lineup. Use the lineup's wOBA against the specific hand of the pitcher.

**Source**:
- FanGraphs team batting splits: `https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&team=0&type=8` -> Splits tab -> vs LHP / vs RHP.
- Alternative: Baseball-Reference team splits page.

**Alternative metric**: ERA (as specified in the skill spec). ERA is a noisier proxy than wOBA-allowed but is widely reported. The primary formula uses wOBA; ERA is a fallback if wOBA is not readily available. For the ERA fallback:

```
For hitters:
  playoff_matchup_quality = 50 + (avg_opp_staff_ERA - 4.00) x 15
  (clamped [0, 100]; league-avg ERA ~ 4.00 -> 50; higher opp ERA = softer = higher score)

For pitchers: inverse, against opp lineup OPS or wRC+ if ERA is not applicable.
```

**Primary**: wOBA-based formula (see [normalization-rules](#normalization-rules)).

---

## Normalization Rules

All three signals use 0-100. `playoff_games` is a count (0-21). `playoff_matchup_quality` and `holding_value` are 0-100 with 50 = neutral.

### `playoff_matchup_quality` (wOBA formula)

```
For hitters on team T:
  avg_opp_staff_wOBA = sum over games g of (opp_staff_wOBA_allowed_g) / playoff_games_T
  playoff_matchup_quality = 100 - (avg_opp_staff_wOBA - 0.300) x 1000
  clamp to [0, 100]

For pitchers on team T with handedness H:
  avg_opp_lineup_wOBA = sum over games g of (opp_lineup_wOBA_vs_H_g) / playoff_games_T
  playoff_matchup_quality = 100 - (avg_opp_lineup_wOBA - 0.300) x 1000
  clamp to [0, 100]
```

**Anchor logic**:
- League-average staff wOBA-allowed ~ 0.320 -> score = 100 - 20 = 80. Why is average 80, not 50? Because the formula measures "softness relative to ace-level pitching (~0.290)"; a league-average staff IS softer than an ace.
- To re-anchor so 50 = league average, use: `playoff_matchup_quality = 50 + (0.320 - avg_opp_staff_wOBA) x 500`.

**Chosen anchor**: Use the **50-at-league-average** formulation throughout the skill. Updated formulas:

```
For hitters:
  playoff_matchup_quality = 50 + (0.320 - avg_opp_staff_wOBA) x 500
  clamp to [0, 100]

For pitchers (hand H):
  playoff_matchup_quality = 50 + (lg_avg_lineup_wOBA_vs_H - avg_opp_lineup_wOBA_vs_H) x 500
  clamp to [0, 100]
  (lg_avg_lineup_wOBA_vs_RHP ~ 0.315; lg_avg_lineup_wOBA_vs_LHP ~ 0.310)
```

This anchor puts 50 at league-median. Higher = softer opposition. Lower = tougher opposition.

### `playoff_games`

Integer count. No normalization -- it is the raw game count. Downstream consumers use it directly (they already know 17-20 is typical, 21 is max).

### `holding_value`

See [holding-value-weights](#holding-value-weights) below.

---

## Holding Value Weights

**Formula**:

```
volume_score = (playoff_games / 21) x 100  (0-100, scales linearly)
holding_value = 0.6 x volume_score + 0.4 x playoff_matchup_quality
                clamp to [0, 100]
```

**Weight justification**:

- **Volume weight 0.6**: Game count is certain (once the schedule is final) and directly scales accumulated stats. A player with 20 games produces ~18% more counting stats than a player with 17 games, regardless of opponent.
- **Quality weight 0.4**: Opponent quality matters but is noisier. A single hot/cold week from an opponent moves wOBA materially. Volume dominates because it's the primary lever the fantasy manager can exploit by roster construction.

**Alternative weight profiles** (if the user is punting specific categories):

| Scenario | Volume weight | Quality weight | Rationale |
|---|---|---|---|
| Default (balanced roster) | 0.60 | 0.40 | Described above |
| Punting ERA/WHIP | 0.80 | 0.20 | Only counting K, QS, SV -- volume even more dominant |
| Chasing OBP (hitters) | 0.40 | 0.60 | Quality of opposing pitching matters more for walk-heavy stats |
| Desperate category push | 0.30 | 0.70 | Short-term focus on soft matchups in a tight category |

The default 0.60/0.40 is what this skill emits. The trade-analyzer and playoff-planner can recompute with alternative weights if they have category-strategy context.

**Clamp rationale**: The formula cannot exceed 100 or go below 0 under valid inputs, but floating-point arithmetic or an edge-case wOBA (e.g., 0.450 opposing lineup) can push the quality term out of bounds. Always clamp at the end.

---

## Pitcher Handedness Adjustment

**Step 1**: Determine the pitcher's throwing hand (RHP or LHP) from FanGraphs player page.

**Step 2**: For each opposing team the pitcher's team faces, use the opposing lineup's wOBA against that hand.

**Step 3**: Compute `playoff_matchup_quality` as in [normalization-rules](#normalization-rules), using the hand-specific opposing wOBA.

**Example**:
- Blake Snell (LAD, LHP) faces [SF, COL, SD, CHC, SF, MIL] during playoff weeks.
- Opposing lineup wOBA vs LHP for each: [0.305, 0.340, 0.310, 0.315, 0.305, 0.320].
- Volume-weighted average (equal weights, one game each for this illustration): 0.3158.
- `playoff_matchup_quality` (LHP) = 50 + (0.310 - 0.3158) x 500 = 50 - 2.9 = **47** (slightly tougher than league average).

**Switch pitchers**: For a rare switch-handedness pitcher or one with extreme reverse splits, note it in `red_team_findings` and use the hand that matches their actual deployment.

**Starter vs reliever volume**:
- For starters, `playoff_games` is projected *starts* in the 21-day window. Typical: 4 starts (if on a 5-day cycle). Document turn order in the notes.
- For closers/high-leverage relievers, `playoff_games` approximates save/hold opportunities -- typically 0.6 x team game count for a primary closer.
- For middle relief, `playoff_games` = team game count x usage rate (0.3-0.5 typical).

---

## Doubleheaders and Makeup Games

**Doubleheader rule**: Two games on the same calendar day count as 2 games toward `playoff_games`. Many scraped schedule sources collapse doubleheaders into a single entry -- cross-check by comparing MLB.com to FanGraphs.

**Quality caveat**: The second game of a doubleheader is often a bullpen game (position-player starts rarely). For the *opposing* team, this means facing a weaker pitching staff in that game -- which boosts `playoff_matchup_quality` for that game. The formula captures this automatically if the opp_staff_wOBA reflects recent usage, but for a confirmed bullpen-game doubleheader, note it explicitly.

**Makeup game rule**: If a game is postponed earlier in the season and the makeup falls inside the playoff window, it counts. Check MLB.com for "makeup" tags on the daily schedule. Flag any still-TBD makeup dates as red-team findings.

**Rainout risk**: Tropicana Field, Marlins Park (retractable), Globe Life Field (retractable), and Rogers Centre are rain-proof. Outdoor parks in rain-heavy cities (Pittsburgh, Cleveland, Cincinnati, Washington, New York) carry postponement risk. This is informational only -- do not penalize `playoff_games` for potential rainouts; the makeup usually lands inside the window.

---

## Degraded-Data Behavior

If web search cannot verify a schedule or opponent wOBA:

1. **Reduce confidence**: `synthesis_confidence: 0.3` if any material fact is unverified.
2. **Flag red team**: Add a finding listing the missing data and its likely magnitude of impact.
3. **Do not emit a full signal**: If more than 20% of opponent wOBAs are missing for a team, emit that team's row with `playoff_matchup_quality: null` and note "insufficient opponent data."
4. **Fallback to ERA**: If wOBA is unreachable but ERA is available, use the ERA fallback formula (see [opponent-quality-scoring](#opponent-quality-scoring)). Flag the fallback in `red_team_findings`.

**Never fabricate**. A null signal is preferable to a made-up number. Downstream agents treat null as blocking; they treat a fabricated number as truth.

---

## Output Summary

After running, the signal file at `signals/YYYY-MM-DD-playoff.md` contains:

1. YAML frontmatter with `type: playoff-push`, `source_urls`, `synthesis_confidence`, `red_team_findings`.
2. A per-team games grid (30 rows).
3. A per-team opponent-quality table with volume-weighted averages.
4. A per-player mapping table covering every player on the user's roster.
5. Grouping: strong holds / neutral / trade candidates.

The playoff-planner and trade-analyzer read this file; they do not re-derive the signals. Re-run weekly.
