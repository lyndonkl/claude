# MLB Matchup Analyzer — Methodology

Detailed procedures for researching each input, normalizing raw factors to the 0-100 signal scale (50 = neutral), and computing weather risk and bullpen state. Every signal is anchored so **50 = league-average**.

## Table of Contents
- [Research Plan: Where to Search, in What Order](#research-plan-where-to-search-in-what-order)
- [Probable Pitcher Research](#probable-pitcher-research)
- [Park Factor Normalization](#park-factor-normalization)
- [Opposing SP Quality (opp_sp_quality)](#opposing-sp-quality-opp_sp_quality)
- [Weather Risk Computation](#weather-risk-computation)
- [Bullpen State Assessment](#bullpen-state-assessment)
- [Platoon Analysis](#platoon-analysis)
- [Normalization Rules (Summary)](#normalization-rules-summary)
- [Confidence Scoring](#confidence-scoring)

---

## Research Plan: Where to Search, in What Order

This skill is **web-search-driven**. There is no API. Every factual claim in the emitted signal file must cite a source URL. Follow this order — escalate to fallbacks only if the primary source fails.

| Fact needed | Primary source | Fallback 1 | Fallback 2 |
|---|---|---|---|
| Probable SPs + handedness | https://www.mlb.com/probable-pitchers | FanGraphs Roster Resource probables grid | RotoWire Daily Lineups |
| SP season stats (ERA, K%, xFIP, hard-hit%) | https://www.fangraphs.com/players/{slug} | Baseball Savant player page | Baseball Reference |
| Park factors | https://www.fangraphs.com/guts.aspx?type=pf&season={YYYY} | Baseball Savant park factors leaderboard | Statcast park factor reports |
| Weather (precip, temp, wind) | https://www.rotowire.com/baseball/weather-forecast.php | Google weather for the home city + first-pitch time | MLB.com Gameday page |
| Roof status | MLB.com Gameday (or team Twitter/X on game day) | — | — |
| Bullpen usage / closer availability | https://www.rotoballer.com/mlb-saves-closers-depth-charts/226767 | Pitcher List bullpen report | Closer Monkey |
| Platoon splits (hitter vs LHP/RHP) | FanGraphs player page -> Splits tab | Baseball-Reference splits | Statcast custom leaderboard |

**Search query style** — always include the season year and be specific. Good: `"German Marquez" 2026 ERA xFIP hard-hit rate`. Bad: `Marquez stats`.

If a web search fails after two attempts, record `source_urls: []` for that signal, drop `confidence` below 0.4, and log it as a red-team finding.

---

## Probable Pitcher Research

**Step 1: Get both SPs and their handedness**

Navigate to MLB.com probable pitchers page and locate the game by date + matchup. Record:
- Pitcher name (full)
- Handedness (LHP or RHP)
- Certainty indicator (confirmed / probable / TBD)

If either SP is TBD, check FanGraphs Roster Resource for the team's likely turn. If still unclear, drop `opp_sp_quality` confidence.

**Step 2: Pull SP quality stats**

For each SP, record from FanGraphs:
- Season ERA, xFIP, K%, BB%
- Rolling last-30-day ERA and K% (if available)
- Hard-hit% and barrel% allowed (Savant cross-reference)
- Career handedness splits if facing an extreme platoon lineup

**Step 3: Flag recent changes**

- IL activity in last 14 days
- Velocity trend (-1.5 mph or more in last start = red flag)
- Recent blow-ups or gems (last 3 starts) that might not yet be in the rolling stat

---

## Park Factor Normalization

FanGraphs publishes park factors centered near **1.00 = neutral**. We re-anchor to **50 = neutral** on a 0-100 scale so every matchup signal uses the same convention.

**Formula:**

```
normalized_park_factor = 50 + (raw_factor - 1.00) * 200
```

Clamp result to `[0, 100]`.

**Worked examples** (using illustrative 2026 factors):

| Park | Raw wOBAcon factor | Normalized | Interpretation |
|---|---|---|---|
| Coors Field | 1.18 | 50 + 0.18*200 = 86 | extreme hitter |
| Great American Ball Park | 1.08 | 50 + 0.08*200 = 66 | hitter-friendly |
| Yankee Stadium | 1.04 | 58 | mild hitter-friendly |
| League median | 1.00 | 50 | neutral |
| Wrigley Field | 0.97 | 44 | mild pitcher-friendly |
| Oracle Park | 0.87 | 26 | extreme pitcher |
| T-Mobile Park | 0.85 | 20 | extreme pitcher |

**`park_pitcher_factor`** = `100 - park_hitter_factor` as a first-order approximation. Apply small corrections for park-specific effects when material (e.g., extreme foul territory favors pitchers beyond what offensive factors imply).

**Handedness-specific park factors** — if a key hitter is extreme-platoon (e.g., pull-only LHB), use the LHB-specific factor instead of the composite. Yankee Stadium's short right-field porch makes it materially friendlier to LHB than the composite suggests; Fenway's Green Monster makes it materially friendlier to RHB pull hitters.

**Sanity check**: across all 30 parks, the distribution of `park_hitter_factor` should center on ~50 with a standard deviation of ~15. If your values skew (e.g., median at 55), re-anchor.

---

## Opposing SP Quality (opp_sp_quality)

**Goal**: express the SP's true talent as faced by the hitters today, on the 50-neutral scale.

**Formula:**

```
opp_sp_quality = 50 + (lg_avg_xFIP - SP_xFIP_season) * 15
```

- League average xFIP ~= 4.00 (confirm for the current season)
- Better SP (lower xFIP) -> higher score -> tougher matchup for hitters
- Clamp to [0, 100]

**Worked examples**:

| SP | Season xFIP | opp_sp_quality |
|---|---|---|
| Ace (Skubal-level) | 2.80 | 50 + (4.00 - 2.80)*15 = 68 |
| Above-average | 3.60 | 56 |
| League-average | 4.00 | 50 |
| Below-average | 4.80 | 38 |
| Replacement level | 5.40 | 29 |

**Adjustments** (apply after base computation, max ±10):
- **+5** if SP has platoon-mismatch vs lineup (e.g., RHP vs a heavily RHB lineup and SP has reverse splits is rare -- usually this is a push; apply only when the SP's splits are extreme)
- **-5** if SP on short rest (< 4 days) or has logged 100+ pitches in last outing
- **-5** if velocity has trended down >1.5 mph over last 3 starts
- **+3** if home park is strongly favorable to SP handedness (e.g., LHP in Oracle)

**Emit from both perspectives**: `opp_sp_quality_vs_home_hitters` (= quality of the AWAY SP, as those are who home hitters face) and `opp_sp_quality_vs_away_hitters` (= quality of the HOME SP).

---

## Weather Risk Computation

**Goal**: a 0-100 score where 0 = no risk and 100 = near-certain disruption.

**Formula:**

```
weather_risk = min(100, rain_probability_pct * importance_multiplier)
```

Plus surcharges for non-rain hazards.

**Importance multiplier:**

| Stage of season | Multiplier | Rationale |
|---|---|---|
| April (week 1-3) | 1.0 | Early season, easy to reschedule |
| May-July (regular) | 1.0 | Neutral |
| August (stretch) | 1.2 | Tighter schedule, harder to make up |
| September (pennant race) | 1.5 | Standings pressure + limited makeup dates |
| October (postseason) | 2.0 | Every game matters; delays are long |

**Non-rain surcharges** (additive, after base formula):

- Sustained wind 20+ mph *against* the offense (blowing in to CF at a hitter park): +5 (suppresses HRs, flattens the matchup but low disruption risk)
- Sustained wind 20+ mph *with* the offense: subtract 5 from pitcher-friendly effects but does NOT add disruption risk
- Temperature below 45 F: +10 (reduced ball carry + game-shortening risk)
- Temperature below 35 F or above 100 F: +20 (cold/heat game-management risk)
- Lightning within 30 miles at first pitch: +30
- Severe weather watch/warning in effect: +40

**Overrides:**

- **Dome or confirmed-closed roof**: `weather_risk` = 0. Record `roof_status: dome` or `roof_status: closed` and note the source.
- **Retractable roof, status unknown**: compute normally but flag with confidence ≤ 0.5 until roof status is confirmed game-day.

**Worked examples** (April):

| Scenario | rain_prob | mult | surcharges | weather_risk |
|---|---|---|---|---|
| Clear, 72 F, Coors | 0% | 1.0 | 0 | 0 |
| 30% chance of showers, Wrigley, May | 30 | 1.0 | 0 | 30 |
| 40% rain, September pennant race, Fenway | 40 | 1.5 | 0 | 60 |
| 20% rain, 38 F, Chicago April | 20 | 1.0 | +10 (cold) | 30 |
| Dome (Minute Maid closed) | — | — | — | 0 |

Clamp to [0, 100].

---

## Bullpen State Assessment

**Goal**: per-team score where 50 = normal, >50 = healthy/rested, <50 = gassed/depleted.

**Data to collect per team** (via RotoBaller closer chart + recent game logs):

1. Closer: last pitched? pitch count last 3 days?
2. Top 2-3 setup/high-leverage arms: last pitched? pitch count?
3. IL additions / option moves in last 72 hours
4. Any confirmed role demotions or closer changes

**Scoring procedure:**

```
score = 50

# Availability (today)
if closer_unavailable:                                    score -= 15
for each high-leverage arm unavailable (max 3 counted):   score -= 10
if 2+ middle relievers unavailable:                       score -= 5

# Rest bonus
if closer had 2+ days rest AND 3-of-4 top arms rested:    score += 5

# Roster state
for each high-leverage arm on IL (within last 7 days):    score -= 5
if closer role is uncertain or just changed:              score -= 5

clamp to [0, 100]
```

**"Unavailable" heuristics** (when usage data is imperfect):

- Pitched in all of the last 3 days: unavailable today
- Threw 25+ pitches yesterday: unavailable today
- Threw 35+ pitches in last 2 days combined: unavailable today

**Emit both `bullpen_state_home` and `bullpen_state_away`.** Downstream consumers select the one they need.

---

## Platoon Analysis

**Per CLAUDE.md rule 5**: jargon-free. Always spell out "right-handed" and "left-handed." Never use the word "splits" without translating it.

**Step 1: SP handedness vs hitter handedness**

| Hitter bats | SP throws | Matchup |
|---|---|---|
| Right | Left | Platoon advantage for hitter |
| Left | Right | Platoon advantage for hitter |
| Right | Right | Neutral (no platoon edge) |
| Left | Left | Neutral (no platoon edge) — typically the hitter's weakest matchup |
| Switch | Either | Hitter bats opposite -> platoon advantage |

**Step 2: Check the hitter's actual handedness numbers**

Pull from FanGraphs Splits tab: OBP, SLG, and wOBA vs each pitcher-hand. If numbers deviate significantly from the general rule (e.g., a LHB who hits LHP *better* than RHP), the individual data overrides the general rule for that hitter.

**Step 3: Factor in park handedness**

If the park has a material L/R split (Yankee Stadium, Fenway, Wrigley in wind), combine park + platoon. Example: LHB facing RHP at Yankee Stadium with wind blowing out = compound positive. LHB facing LHP at Oracle Park = compound negative.

**Step 4: Write the narrative**

Follow the template in `resources/template.md` -> Platoon Narrative Template. End with a one-sentence verdict that the consuming agent (typically `mlb-player-analyzer`) can turn into a numeric tilt.

---

## Normalization Rules (Summary)

Every signal produced by this skill must satisfy:

1. **Scale 0-100**; 50 = league-average / neutral.
2. **Clamped** to [0, 100] — no values outside the range.
3. **Symmetric around 50** (where it makes sense) — the formula should not systematically skew high or low for the population.
4. **Sanity-tested** — apply to 5-10 known reference cases (Coors, Oracle, ace SP, replacement SP) and verify the output matches intuition.

| Signal | Neutral = 50 anchor |
|---|---|
| `opp_sp_quality` | League-average xFIP = 50 |
| `park_hitter_factor` | Park factor 1.00 = 50 |
| `park_pitcher_factor` | Park factor 1.00 = 50 |
| `weather_risk` | 0 (no inherent neutral — it is unipolar risk) |
| `bullpen_state` | Normal availability = 50 |

---

## Confidence Scoring

`synthesis_confidence` is a 0.0-1.0 scalar reflecting how trustworthy the whole signal file is.

| Condition | Effect |
|---|---|
| All primary sources reached and data is current | start at 0.85 |
| One primary source used fallback | -0.10 |
| Probable SP is "TBD" (not confirmed) | -0.15 |
| Weather forecast is >24 hours out | -0.05 |
| Bullpen state based on guessing (no box-score check) | -0.10 |
| Data is from previous day (stale) | -0.15 |
| Key hitter platoon data unavailable | -0.05 |

If confidence drops below 0.4, the red team should flag this signal file as low-trust and the consuming agent should weight it accordingly.
