# MLB Closer Tracker Methodology

Detailed procedures for pulling closer depth charts, scoring `save_role_certainty`, detecting committees, sizing speculation bets, and triggering a punt-SV fallback.

## Table of Contents
- [Source Hierarchy](#source-hierarchy)
- [Primary Source: RotoBaller](#primary-source-rotoballer)
- [Secondary Sources](#secondary-sources)
- [save_role_certainty Rubric](#save_role_certainty-rubric)
- [Committee Detection](#committee-detection)
- [DFA-Risk Detection](#dfa-risk-detection)
- [Velocity Trend Check](#velocity-trend-check)
- [Manager Signal Coding](#manager-signal-coding)
- [Speculation Target Identification](#speculation-target-identification)
- [FAAB Bid Sizing for Handcuffs](#faab-bid-sizing-for-handcuffs)
- [Punt-SV Trigger](#punt-sv-trigger)
- [Handoff Protocol](#handoff-protocol)

---

## Source Hierarchy

Every run queries three external sources plus Yahoo. Each source has a specific job.

| Tier | Source | URL | Job |
|---|---|---|---|
| Primary | RotoBaller Closer Depth Charts | https://www.rotoballer.com/mlb-saves-closers-depth-charts/226767 | 30-team baseline; role labels |
| Secondary | Closer Monkey | https://closermonkey.com | Breaking role changes (often leads by 24-48h) |
| Secondary | Athlon Closer Confidential | Search: `athlon sports closer confidential 2026` | Early-season letter grades per team |
| Context | Yahoo position depth chart | https://baseball.fantasysports.yahoo.com/b1/23756/position_depth_chart?pos=CL | League availability |
| Context | Baseball Savant | https://baseballsavant.mlb.com | Velocity trend for closers on thin ice |
| Context | Team beat writers via MLB.com / Athletic | Search per team | Manager quotes |

---

## Primary Source: RotoBaller

The RotoBaller depth chart is the baseline. It publishes role labels per team that map cleanly to the scoring rubric.

### What to extract per team

- Top 3 RPs listed
- Role label for each (Closer, Next Man Up, Committee, Setup, etc.)
- Any bolded / italicized notes (these often flag recent changes)
- "Last updated" timestamp (if older than 48h, downgrade confidence by 0.1)

### Handling stale pages

If the RotoBaller page has not been updated in 5+ days:
- Drop overall run `confidence` to 0.6 or below
- Rely more heavily on Closer Monkey for role changes
- Flag in the red-team section of the signal file

### Handling outages

If RotoBaller is unreachable:
- Fall back to Pitcher List Bullpen Report
- Fall back to Closer Monkey as primary (lower coverage breadth)
- Set overall `confidence` <= 0.5 and note the fallback in the signal frontmatter

---

## Secondary Sources

### Closer Monkey

- Updated near-daily during the season
- Strongest signal during volatile weeks (April, July trade deadline, September)
- Use to break ties when RotoBaller and intuition disagree
- Query: visit homepage, scan for teams RotoBaller flagged as anything other than "Closer (locked)"

### Athlon Closer Confidential

- Publishes letter grades (A through F) in spring training and early April
- A/A-minus grades map to save_role_certainty 85+
- B grades map to 70-85
- C grades map to 50-70 (committee-risk range)
- D/F grades map to < 50 (expect turnover)
- Less useful after mid-May — grades become stale

### Tie-break rule for conflicting sources

If RotoBaller says "Closer (locked)" but Closer Monkey says "Committee emerging":
- Cap save_role_certainty at 70 (don't give a full locked score)
- Flag as volatility in the situation tag
- Note the disagreement in the signal file body

---

## save_role_certainty Rubric

Score each component 0-5, sum, multiply by 4 to rescale to 0-100.

### Component 1: role_label_score (weight 20%)

| RotoBaller label | Score |
|---|---|
| Closer (locked) | 5 |
| Closer (soft hold) | 4 |
| Committee — primary | 3 |
| Committee — secondary | 2 |
| Setup / Next Man Up | 2 |
| Middle relief | 1 |
| DFA-risk / demoted | 0 |

### Component 2: recent_performance (weight 20%)

Look at the last 10 days of appearances.

| Condition | Score |
|---|---|
| 0 blown saves, ERA < 2.50 over last 10 days | 5 |
| 0 blown saves, ERA 2.50-4.00 | 4 |
| 1 blown save, ERA under 4.00 | 3 |
| 1 blown save, ERA 4.00-6.00 | 2 |
| 2+ blown saves OR ERA > 6.00 | 1 |
| 3+ blown saves (role loss likely) | 0 |

### Component 3: velocity_trend (weight 20%)

Compare last 3 outings' average fastball velocity to season baseline on Baseball Savant.

| Delta | Score |
|---|---|
| +0.5 mph or more | 5 |
| -0.0 to +0.5 | 4 |
| -0.5 to 0.0 | 3 |
| -1.0 to -0.5 | 2 |
| -1.5 to -1.0 | 1 |
| -1.5 mph or worse | 0 |

### Component 4: manager_signal (weight 20%)

Based on the most recent manager quote or public decision.

| Signal | Score |
|---|---|
| "He's our guy" / multi-day explicit vote of confidence | 5 |
| "He's pitching the ninth today" (single-game commit) | 4 |
| Silence after a clean outing | 3 |
| "We'll play the matchups" / "see how it plays out" | 2 |
| Silence after a blown save | 1 |
| Public criticism or named replacement | 0 |

### Component 5: contract_age_security (weight 20%)

Long-term job security factors.

| Condition | Score |
|---|---|
| Multi-year guaranteed deal, age < 32, healthy | 5 |
| Single-year deal OR age 32-34, healthy | 4 |
| Age 35+, healthy; or returning from minor injury | 3 |
| Non-guaranteed contract OR age 36+ with decline | 2 |
| Out of options OR age 37+ with injury history | 1 |
| On waivers risk; team publicly shopping for a closer | 0 |

### Computation

```
save_role_certainty = 4 x (role_label_score + recent_performance + velocity_trend
                         + manager_signal + contract_age_security)
```

Range: 0 (5 zeros) to 100 (5 fives).

### Confidence attached per RP

Attach a per-RP `score_confidence` (0.0-1.0) alongside the numeric score:
- 0.9+ if all 5 components had concrete data
- 0.7 if 4 of 5 did
- 0.5 if only 3 of 5 did
- Below 0.5: do not emit; mark the RP as "insufficient data"

---

## Committee Detection

A committee flag fires when:

1. Two or more RPs on the same team score within 15 points of each other on `save_role_certainty`, AND
2. At least one of: RotoBaller labels any of them "Committee", OR manager public quote within 7 days uses "matchups" / "play it by ear" language.

When a committee is flagged:
- **No RP on that team scores above 60**, even if they just got the last save
- Both arms are noted as speculation-worthy
- Platoon handedness matters — see [Platoon Handcuff Rule](#platoon-handcuff-rule) below

### Platoon handcuff rule

In a true committee, prefer the arm that gets the platoon advantage in typical save situations. If the league's typical high-leverage 9th-inning hitter profile skews LHB, the LHP committee arm has higher vulture potential. Check team-by-team:
- Scan the next 2 weeks of opponents
- Count expected LHB vs RHB in the 9th inning (top of order)
- Bias the speculation bid toward the platoon-advantaged arm

---

## DFA-Risk Detection

A DFA-risk flag fires when ALL of:

1. `save_role_certainty` < 25
2. Role has been lost within the last 21 days (was the closer, now is not)
3. One of: out of minor-league options, non-guaranteed deal, age 36+, demoted to mop-up

### Action when DFA-risk flag fires

- DROP if currently rostered
- Never ADD
- If the team has an open handcuff slot behind the new closer, check the *next* arm — the DFA-risk guy is not it

---

## Velocity Trend Check

For any closer whose `save_role_certainty` is below 80, pull the Baseball Savant player page and compare:
- 2026 season average fastball velocity (baseline)
- Last 3 outings' fastball velocity (trend)

A sustained -1.0 mph drop across 3 outings predicts role loss within 14 days at a ~40% rate (per internal tracking). Weight heavily.

### Where to find it

- Baseball Savant player page → "Game Logs" tab → filter to fastball
- Or Statcast Pitch Arsenal for rolling trend line

If Savant data lags by 1-2 days, that's acceptable. If the closer has not thrown in a week (typical for teams avoiding a "hurt but not IL" guy), that itself is a velocity-trend flag — score 2 or below.

---

## Manager Signal Coding

Quote hunt the beat writers, not the generic wire services. The Athletic beat writer per team, MLB.com team reporter, and occasionally the manager's postgame press conference all have distinct tones.

### Search query pattern

```
"[manager name]" "[closer name]" ninth inning [current month] 2026
```

Or:

```
[team] closer role April 2026 [manager name] quote
```

### Coding rubric

Already listed in Component 4 of the scoring rubric. Extra notes:

- **"We'll see"** is the single most important phrase to flag — it almost always precedes a role change.
- **"He's our closer"** said twice in a week is stronger than once.
- **Reporter paraphrase** ("the skipper suggested...") is softer evidence; code at 0.5x the weight of a direct quote.

---

## Speculation Target Identification

Filter criteria for the speculation target table:

1. `save_role_certainty` between 30 and 60 (the sweet spot for handcuffs), AND
2. Current incumbent has AT LEAST ONE volatility flag:
   - 2+ blown saves in 10 days
   - Velocity -1.0 mph or more
   - Non-committal manager quote in last 7 days
   - Age 35+ with recent ERA spike
   - Returning from IL or nagging injury

Then rank by:

```
speculation_score = handcuff_save_role_certainty
                  + incumbent_volatility_points
                  - ownership_penalty
```

Where:
- `incumbent_volatility_points` = sum of flags (each flag = 10 points)
- `ownership_penalty` = 30 if the handcuff is already rostered in our league; 0 if available

Top 5 uncontested speculation targets head to the waiver-analyst.

---

## FAAB Bid Sizing for Handcuffs

This league has $100 FAAB. Budget rationally. Use these bid bands:

| save_role_certainty of handcuff | Base band | Incumbent super-volatile (2+ flags) |
|---|---|---|
| 50-60 | $6-10 | $10-15 |
| 40-50 | $3-6 | $6-10 |
| 30-40 | $1-3 | $3-6 |
| < 30 | $0-1 | $1-2 |

### Ceiling rule

Never bid above $10 on a single handcuff without `mlb-category-strategist` concurrence. The justification:

- SV is this league's most volatile pitcher cat (high weekly variance)
- Speculation closers bust roughly 50% within 30 days (they don't get the role, or they blow it back quickly)
- $10 is ~10% of the season FAAB budget — a 50/50 shot for one cat's marginal benefit is a poor trade

If the category-strategist confirms SV is a must-win this week, the ceiling can rise to $20.

### Floor rule

Never bid $0 on a speculation target you believe is above 50 save_role_certainty — someone else in the league will snag for $1. Minimum $1 bid for anything worth stashing.

---

## Punt-SV Trigger

The punt-SV recommendation fires when:

1. User currently owns zero RPs with `save_role_certainty` >= 75, AND
2. To compete in SV this week, 4 or more of the user's 5 flex RP slots would need to be speculation closers (save_role_certainty 30-60 range), AND
3. `mlb-category-state-analyzer` has SV in "losing" or "tied with low reachability" status

When the trigger fires:

- Emit a `punt_sv_recommended: true` in the signal frontmatter
- Write the [punt-sv block](template.md#punt-sv-recommendation-block) in the signal body
- Suggest the category-strategist boost `cat_punt_score` for SV by +20
- Recommend redirecting 3-4 of the RP slots to high-K setup men for ratio help (boosts K, ERA, WHIP) and an additional two-start SP (boosts QS, K)

### Why this matters

This user was told from the start that SV is the most punt-worthy cat. Because closer role is volatile and because K/ERA/WHIP/QS are more stable category wins, the expected value of conceding SV and winning 4 other pitcher cats exceeds the expected value of chasing SV with unstable relievers. The coach should be given this fallback every time the reliever pool is thin.

---

## Handoff Protocol

The closer signal file is consumed by three downstream agents.

### 1. mlb-waiver-analyst

Reads:
- Speculation target table
- FAAB bid bands
- Ceiling rule / category-strategist concurrence requirement

Does NOT re-score save_role_certainty. Uses the emitted scores directly.

### 2. mlb-category-strategist

Reads:
- `punt_sv_recommended` flag
- Count of user-owned RPs by save_role_certainty band
- Committee flags (which saves are contested, therefore lower expected SV/week)

Decides final push/punt allocation for SV.

### 3. mlb-lineup-optimizer

Reads:
- save_role_certainty for each user-rostered RP
- DFA-risk flags (triggers a drop suggestion)

Does NOT need depth charts for non-rostered RPs.

### Emission requirements

Before writing, call `mlb-signal-emitter` to validate:
- Frontmatter YAML valid
- All save_role_certainty values in [0, 100]
- 30 teams covered (or missing teams noted)
- confidence >= 0.4 or flagged
- source_urls populated

If validation fails, do not persist. Log the failure to `tracker/decisions-log.md` and retry with a fresh pull.
