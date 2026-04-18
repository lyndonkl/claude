# MLB Playoff Scheduler Templates

Signal file template, per-team games grid, per-opponent quality table, and per-player mapping for fantasy playoff weeks 21-23 (2026-08-17 to 2026-09-06).

## Table of Contents
- [Signal File Template (Post-July)](#signal-file-template-post-july)
- [Pre-July Stub Template](#pre-july-stub-template)
- [Per-Team Games Grid](#per-team-games-grid)
- [Per-Team Opponent Quality Table](#per-team-opponent-quality-table)
- [Per-Player Mapping Table](#per-player-mapping-table)
- [Handedness-Aware Pitcher Table](#handedness-aware-pitcher-table)

---

## Signal File Template (Post-July)

Write to `signals/YYYY-MM-DD-playoff.md`. YAML frontmatter per [context/frameworks/signal-framework.md](../../../../yahoo-mlb/context/frameworks/signal-framework.md).

```markdown
---
type: playoff-push
date: 2026-07-14
emitted_by: mlb-playoff-scheduler
variant_synthesis: false
variants_fired: []
synthesis_confidence: 0.82
red_team_findings:
  - severity: 2
    likelihood: 2
    score: 4
    note: "3 TB games in Week 22 depend on makeup of postponed May 9 vs NYY game"
    mitigation: "Re-run Jul 28 once MLB posts the makeup date"
source_urls:
  - https://www.mlb.com/schedule/2026-08-17
  - https://www.mlb.com/schedule/2026-08-24
  - https://www.mlb.com/schedule/2026-08-31
  - https://www.fangraphs.com/teams/rays/schedule
  - https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&team=0&type=8
run_metadata:
  playoff_window_start: 2026-08-17
  playoff_window_end: 2026-09-06
  weeks: [21, 22, 23]
  total_calendar_days: 21
  teams_analyzed: 30
---

# MLB Playoff Scheduler -- Week 21-23 Outlook
# Emitted: 2026-07-14

## Summary

- Highest-volume teams (21 games): [list]
- Softest schedules (top `playoff_matchup_quality`): [list]
- Highest `holding_value` hitters on user roster: [list]
- Highest `holding_value` pitchers on user roster: [list]
- Candidates to trade away (low holding_value): [list]

[Per-team games grid, per-team opponent quality, per-player mapping follow.]
```

---

## Pre-July Stub Template

When today < 2026-07-01, emit this minimal file at `signals/YYYY-MM-DD-playoff.md` and stop.

```markdown
---
type: playoff-push
date: 2026-04-17
emitted_by: mlb-playoff-scheduler
variant_synthesis: false
variants_fired: []
synthesis_confidence: 0.0
red_team_findings: []
source_urls: []
run_metadata:
  playoff_window_start: 2026-08-17
  playoff_window_end: 2026-09-06
  stub: true
  stub_reason: "pre-July-1 gate"
---

# MLB Playoff Scheduler -- Insufficient Signal

Today is 2026-04-17. Playoff weeks 21-23 (Aug 17 - Sep 6) are ~4 months away.

**Insufficient signal -- too early.** Pre-July schedule projections are unreliable because:

1. ~30-40% of opponent lineups will change (deadline trades, call-ups, demotions).
2. Rotation and bullpen composition is in flux through the All-Star break.
3. Makeup games for April/May postponements reshape the August-September calendar.

All three signals emit `null`; downstream agents must not read them.

| Signal | Value |
|---|---|
| `playoff_games` | null |
| `playoff_matchup_quality` | null |
| `holding_value` | null |

**Next re-run**: 2026-07-05 (first Sunday after July 1). From that point, the playoff-planner fires weekly.
```

---

## Per-Team Games Grid

The required "output: per-MLB-team grid of games in each playoff week." Sort descending by total.

| MLB Team | Week 21 (Aug 17-23) | Week 22 (Aug 24-30) | Week 23 (Aug 31-Sep 6) | Total | Notes |
|---|---|---|---|---|---|
| ARI | _ | _ | _ | _ | |
| ATL | _ | _ | _ | _ | |
| BAL | _ | _ | _ | _ | |
| BOS | _ | _ | _ | _ | |
| CHC | _ | _ | _ | _ | |
| CHW | _ | _ | _ | _ | |
| CIN | _ | _ | _ | _ | |
| CLE | _ | _ | _ | _ | |
| COL | _ | _ | _ | _ | |
| DET | _ | _ | _ | _ | |
| HOU | _ | _ | _ | _ | |
| KC | _ | _ | _ | _ | |
| LAA | _ | _ | _ | _ | |
| LAD | _ | _ | _ | _ | |
| MIA | _ | _ | _ | _ | |
| MIL | _ | _ | _ | _ | |
| MIN | _ | _ | _ | _ | |
| NYM | _ | _ | _ | _ | |
| NYY | _ | _ | _ | _ | |
| OAK | _ | _ | _ | _ | |
| PHI | _ | _ | _ | _ | |
| PIT | _ | _ | _ | _ | |
| SD | _ | _ | _ | _ | |
| SEA | _ | _ | _ | _ | |
| SF | _ | _ | _ | _ | |
| STL | _ | _ | _ | _ | |
| TB | _ | _ | _ | _ | |
| TEX | _ | _ | _ | _ | |
| TOR | _ | _ | _ | _ | |
| WAS | _ | _ | _ | _ | |

**Notes column usage**:
- `DH 8/24` = doubleheader on that date
- `Makeup TBD` = postponed game with undetermined makeup date
- `Rain risk high` = 4+ games in a historically rain-heavy window at a rain-prone park

---

## Per-Team Opponent Quality Table

For each team, list the opponents faced across the three playoff weeks and the key opponent metrics. This drives `playoff_matchup_quality`.

### Example: Tampa Bay Rays (TB)

| Game Date | Opponent | Venue | Home/Away | Opp Staff wOBA Allowed (season) | Opp Lineup wOBA vs RHP | Opp Lineup wOBA vs LHP |
|---|---|---|---|---|---|---|
| 2026-08-17 | BAL | Camden Yards | Away | 0.315 | 0.325 | 0.318 |
| 2026-08-18 | BAL | Camden Yards | Away | 0.315 | 0.325 | 0.318 |
| 2026-08-19 | BAL | Camden Yards | Away | 0.315 | 0.325 | 0.318 |
| 2026-08-21 | TOR | Tropicana Field | Home | 0.328 | 0.330 | 0.320 |
| 2026-08-22 | TOR | Tropicana Field | Home | 0.328 | 0.330 | 0.320 |
| 2026-08-23 | TOR | Tropicana Field | Home | 0.328 | 0.330 | 0.320 |
| ... | ... | ... | ... | ... | ... | ... |
| **Volume-weighted averages** | | | | **0.323** | **0.327** | **0.319** |

**Computed signals for TB**:
- `playoff_games` = 20
- `playoff_matchup_quality` (hitter view) = 100 - (0.323 - 0.300) x 1000 = **77**
- `playoff_matchup_quality` (RHP pitcher view) = 100 - (0.327 - 0.300) x 1000 = **73**
- `playoff_matchup_quality` (LHP pitcher view) = 100 - (0.319 - 0.300) x 1000 = **81**

---

## Per-Player Mapping Table

Map every rostered player to their team's signals. This is what downstream agents consume.

| Player | MLB Team | Position | Role (Bat/Pit/Hand) | `playoff_games` | `playoff_matchup_quality` | `holding_value` |
|---|---|---|---|---|---|---|
| Junior Caminero | TB | 3B | Bat (RHB) | 20 | 77 | 88 |
| Zac Gallen | ARI | SP | Pit (RHP) | _ | _ | _ |
| Josh Naylor | SEA | 1B | Bat (LHB) | _ | _ | _ |
| ... | | | | | | |

**Grouping for the user-facing brief**:

**Strong holds (`holding_value` >= 70)**:
| Player | `holding_value` | Why |
|---|---|---|
| Junior Caminero | 88 | 20 games + soft opposing staffs (Aug) |
| ... | | |

**Neutral (40-70)**:
| Player | `holding_value` | Why |
|---|---|---|
| ... | | |

**Trade candidates (`holding_value` < 40)**:
| Player | `holding_value` | Why |
|---|---|---|
| ... | | Low game volume and/or tough opposing staffs |

---

## Handedness-Aware Pitcher Table

Pitchers need a separate `playoff_matchup_quality` because the opposing lineup they face depends on their handedness. The table above already carries RHP and LHP variants; use the row matching the pitcher's hand.

| Pitcher | MLB Team | Hand | Opp Lineup wOBA vs [hand] (avg) | `playoff_matchup_quality` | `playoff_games` (team starts + relief appearances projected) | `holding_value` |
|---|---|---|---|---|---|---|
| Blake Snell | LAD | LHP | 0.312 | 88 | 4 starts projected | 72 |
| Zac Gallen | ARI | RHP | 0.328 | 72 | 4 starts projected | 68 |
| ... | | | | | | |

**Note on SP `playoff_games`**: for starting pitchers, `playoff_games` should reflect projected *starts* in the window (typically 4, occasionally 3 or 5), not calendar games for the team. This is the volume input that matters for SP-only categories (K, QS). Document the assumed turn order in the notes.

**Note on RP `playoff_games`**: for closers and high-leverage relievers, `playoff_games` approximates expected save/hold opportunities -- closer to the team's total game count, scaled by usage rate (typically 0.5-0.7 of team games).

---

## Output checklist

Before writing the signal file:

- [ ] Date gate checked (stub if pre-July-1)
- [ ] All 30 MLB teams in the games grid
- [ ] Doubleheaders explicitly noted
- [ ] Opponent wOBA sourced for each opponent (URL captured)
- [ ] Volume-weighted averages computed (not simple averages of the three weekly averages)
- [ ] Handedness split applied for pitcher rows
- [ ] Per-player table includes every player on the user's roster
- [ ] Strong-hold / neutral / trade-candidate grouping provided for the user-facing brief
- [ ] `source_urls` frontmatter lists every URL consulted
- [ ] `red_team_findings` lists at least one risk (makeup game TBD, rotation uncertainty, etc.)
