---
name: mlb-two-start-scout
description: For a given fantasy week (Monday-Sunday), identifies every starting pitcher scheduled to start twice, validates both probable starts, grades each matchup against the league's Quality Starts (QS) scoring rules, and ranks the list by streamability_score. Flags bullpen-game and opener risks that nearly never produce QS. Use when user mentions "two-start pitchers", "weekly streaming", "Monday-Sunday pitcher plan", "double start", "2-start SP", or preparing the weekly streaming plan on Sunday nights.
---
# MLB Two-Start Scout

## Table of Contents
- [Example](#example)
- [Workflow](#workflow)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Example

**Scenario**: Fantasy week of Monday 2026-04-20 through Sunday 2026-04-26. League scores Quality Starts (QS = 6+IP and <=3ER), not Wins. User needs to decide which two-start SPs to stream from free agency.

**Step 1 outputs (from web search)** -- FantasyPros two-start-pitchers.php plus FanGraphs probables-grid cross-check:

| SP | Team | Start 1 | Start 2 | Notes |
|---|---|---|---|---|
| Logan Webb | SFG | Mon 4/20 @ COL | Sat 4/25 vs WSH | confirmed on both sources |
| Seth Lugo | KCR | Tue 4/21 @ DET | Sun 4/26 vs NYY | confirmed |
| Bryan Woo | SEA | Mon 4/20 vs HOU | Sun 4/26 @ OAK | confirmed |
| Ranger Suarez | PHI | Tue 4/21 vs NYM | Sun 4/26 @ ATL | confirmed |
| (Team TBD) | MIA | Wed 4/23 vs STL | Mon (next wk)?? | OPENER RISK -- drop |

**Step 2 outputs** -- matchup signals per start:

Logan Webb: Start 1 at Coors (park_pitcher_factor 25, brutal) but weak COL lineup; Start 2 vs WSH at home (park 55). qs_probability 58, k_ceiling 62, era_whip_risk 55, streamability_score 62.

Seth Lugo: Start 1 at DET (avg), Start 2 vs NYY (top-3 wOBA). qs_probability 45, era_whip_risk 68, streamability_score 48.

Bryan Woo: Start 1 vs HOU (tough), Start 2 at OAK (weakest AL lineup, pitcher park 60). qs_probability 66, k_ceiling 70, streamability_score 71.

Ranger Suarez: Start 1 vs NYM (tough), Start 2 at ATL (top-2 wOBA, hitter park). qs_probability 40, era_whip_risk 72, streamability_score 42.

**Step 3 output** -- ranked two-start board (only free agents shown to user):

| Rank | SP | FA status | Streamability | QS prob | K ceiling | Risk | Verdict |
|---|---|---|---|---|---|---|---|
| 1 | Bryan Woo | FA in your league | 71 | 66 | 70 | 45 | ADD + START both |
| 2 | Logan Webb | Rostered | 62 | 58 | 62 | 55 | - (not available) |
| 3 | Seth Lugo | FA | 48 | 45 | 58 | 68 | SKIP -- risky vs NYY |
| 4 | Ranger Suarez | FA | 42 | 40 | 55 | 72 | SKIP -- both matchups bad |
| -- | MIA opener | FA | -- | -- | -- | -- | IGNORE -- bullpen game |

**User-facing recommendation (delivered by streaming-strategist via communication-storytelling skill):**

> "This week has one strong two-start streamer: Bryan Woo of Seattle. He pitches twice (Monday vs Houston, Sunday at Oakland) and Oakland has the weakest hitting lineup in the American League. ADD Bryan Woo if he is a free agent. Bid $3-5 FAAB. Two starts means double the strikeouts and double the chance at a Quality Start -- even if Monday's matchup vs Houston goes poorly, the Oakland start is likely to salvage the week."

## Workflow

Copy this checklist and track progress:

```
Two-Start Scout Progress:
- [ ] Step 1: Define the fantasy week (Mon-Sun dates) and pull the two-start list
- [ ] Step 2: Cross-reference two lists and validate both probable starts per SP
- [ ] Step 3: Flag bullpen-game and opener risks -- remove from board
- [ ] Step 4: Compute per-start matchup signals (qs_probability, k_ceiling, era_whip_risk)
- [ ] Step 5: Aggregate to per-SP streamability_score
- [ ] Step 6: Cross-reference with Yahoo free-agent pool, rank, and emit signal file
```

**Step 1: Define the week and pull the two-start list**

Confirm the Monday-Sunday dates in ISO format (e.g., 2026-04-20 through 2026-04-26). Yahoo fantasy weeks lock at 9am ET Monday. See [resources/methodology.md](resources/methodology.md#week-definition) for week-boundary handling.

- [ ] Monday date confirmed (start of week)
- [ ] Sunday date confirmed (end of week)
- [ ] Web-search FantasyPros two-start-pitchers.php for the upcoming week
- [ ] Record URL and `computed_at` timestamp for the signal frontmatter

**Step 2: Cross-reference and validate both starts**

FantasyPros is primary but lags short-notice rotation changes. Cross-check FanGraphs probables-grid to verify both starts are still scheduled and neither has been pushed or bumped. See [resources/methodology.md](resources/methodology.md#cross-reference-validation).

- [ ] For each SP on the FantasyPros list, find both probable-start dates on FanGraphs grid
- [ ] If FanGraphs shows a different pitcher for one of the two dates, reduce confidence and note the conflict
- [ ] If the SP has been scratched or pushed (injury news, weather makeup), remove from board or flag
- [ ] Record both sources in `source_urls`

**Step 3: Flag bullpen-game and opener risks**

Teams that deploy openers (e.g., rebuilding clubs using a 1-inning reliever to start the game) rarely produce QS for the "nominal starter". These hurt ERA/WHIP and give zero QS. De-prioritize or drop entirely. See [resources/methodology.md](resources/methodology.md#opener-bullpen-detection).

- [ ] Check each SP's recent game logs -- is their typical outing <5 IP? Opener risk.
- [ ] Check if the team has announced a "bullpen day" for either scheduled start
- [ ] Flag any SP whose team is known to use openers regularly (mark `opener_risk: true`)
- [ ] Remove opener-risk SPs from the top of the ranking or drop entirely

**Step 4: Compute per-start matchup signals**

For EACH of the two starts, compute matchup signals individually. A two-start SP with one great matchup and one terrible matchup is materially different from one with two average matchups. See [resources/methodology.md](resources/methodology.md#per-start-scoring).

- [ ] For each start: pull opponent team wOBA vs pitcher handedness
- [ ] For each start: pull park factor (hitter vs pitcher park)
- [ ] For each start: pull weather (rain-out and wind risk)
- [ ] For each start: compute `qs_probability`, `k_ceiling`, `era_whip_risk` per the signal-framework definitions

**Step 5: Aggregate to per-SP streamability_score**

Average the two starts, weighted toward QS probability because our league is QS-scoring (not W-scoring). See [Quick Reference](#quick-reference) for the exact weighting formula.

- [ ] Compute per-SP `streamability_score` using the QS-weighted formula
- [ ] Flag SPs with one "great" matchup and one "disaster" matchup separately -- variance matters
- [ ] Apply opener-risk penalty if any
- [ ] Rank SPs from highest to lowest `streamability_score`

**Step 6: Cross-reference free agents, rank, and emit signal**

The user can only stream SPs who are free agents (FA). Filter the board to rostered vs available, and annotate the Yahoo FA status. Emit the signal file following [resources/template.md](resources/template.md).

- [ ] Pull Yahoo FA pool for SP position (via `mlb-league-state-reader` or handoff)
- [ ] Annotate each SP as `roster_status: fa | rostered-other | rostered-user`
- [ ] Emit signal file `signals/YYYY-MM-DD-two-start.md` using the template
- [ ] Validate via `mlb-signal-emitter` (all scores in range, confidence >= 0.4, sources cited)
- [ ] Hand off to `mlb-streaming-strategist` (which runs advocate + critic variants)

Minimum standard: average rubric score of 3.5 or above. Validate using [resources/evaluators/rubric_mlb_two_start_scout.json](resources/evaluators/rubric_mlb_two_start_scout.json).

## Common Patterns

**Pattern 1: Two good matchups (rare, high-value stream)**
- **Profile**: Both starts vs bottom-tier offenses, at least one in a pitcher-friendly park, neither in Coors or GABP.
- **Action**: Strong ADD candidate. Willing to bid real FAAB (see `mlb-faab-sizer`). Start both games.
- **Watch for**: A hot FA is likely to draw multiple bids -- the `mlb-waiver-analyst` will size the bid.

**Pattern 2: One good, one disaster (split decision)**
- **Profile**: One start vs WSH or COL hitters (disaster), one vs OAK or CHW (plum).
- **Action**: Depends on daily-lineup flexibility. If the user can START the good day and BENCH the bad day, this becomes a high-value add. If the league locks weekly, score this lower -- the bad start will tank ratios.
- **Watch for**: Note the league's lineup cadence. Yahoo daily lineup lock means we can bench the bad start. Flag explicitly.

**Pattern 3: Two bad matchups (avoid)**
- **Profile**: Both starts vs top-10 offenses, one or both in hitter parks.
- **Action**: Even with two starts, expected Ks are undone by the ERA/WHIP damage. SKIP. Note that 2-start weeks are not automatically good.
- **Watch for**: The "two starts!" heuristic can trap beginners. Always check matchup quality, not just start count.

**Pattern 4: Opener / bullpen-game risk**
- **Profile**: Rebuilding team (MIA, OAK, CHW, PIT, WAS) deploys a 1-inning opener; the "starter" enters in the 2nd. Their typical outing is 3-4 IP.
- **Action**: IGNORE. Zero QS upside, full ratio risk. Remove from board.
- **Watch for**: FantasyPros sometimes lists the nominal starter without flagging opener risk. Cross-check the pitcher's recent game logs for sub-5-IP outings.

## Guardrails

1. **Two starts does not mean good streamer.** The volume multiplier only pays off when the per-start matchup quality is at or above league average. Two starts vs top-5 offenses can produce negative QS value. Always evaluate matchup quality, not just the start count.

2. **Our league is QS, not W.** Weighting must reflect this. 6+IP <=3ER matters more than wins. A pitcher on a bad team with good matchups can still produce QS. A pitcher on a great team with bad matchups cannot reliably. The formula in [Quick Reference](#quick-reference) codifies this.

3. **Validate BOTH starts on FanGraphs.** FantasyPros publishes Sunday night; rotation changes happen Monday-Wednesday. If the second start shifts to a different pitcher, the SP is no longer a two-start SP -- remove from the board. Never use the FantasyPros list as the only source.

4. **Opener teams are traps.** MIA, OAK, CHW, PIT, WAS and a rotating cast of rebuilders use openers or short starts. The nominal "starter" listed may throw 3 innings. Zero QS upside. Always cross-check recent game logs.

5. **Weather matters more for two-start weeks.** A rain-out of one of the two starts converts a two-start SP to a one-start SP, and the value drops by roughly half. Flag any start with >30% rain probability as a downgrade on confidence.

6. **Coors Field is a cliff.** Any start in Coors (COL home) automatically caps `streamability_score` at ~60 no matter the matchup. The park factor is extreme enough that even an ace gives up 5+ runs some nights. Two-start SPs with a Coors game should rank below SPs with two neutral-park starts.

7. **Cross-reference Yahoo FA status before ranking.** A top-ranked two-start SP who is already rostered is irrelevant to the streaming decision. Always annotate `roster_status` and present the user only with actionable (FA) options at the top, with rostered SPs as context below.

8. **Signal file is authoritative.** Downstream agents (streaming-strategist, waiver-analyst) read the emitted signal file and do not re-derive. If the signal file is missing a field or has confidence < 0.4, downstream agents must flag it, not fill it in.

## Quick Reference

**Key formulas:**

```
qs_probability (per start) = rolling_QS_rate * matchup_multiplier
  where matchup_multiplier =
      0.35 * (100 - opp_wOBA_normalized)    # worse offense = higher QS
    + 0.25 * park_pitcher_factor            # pitcher park = higher QS
    + 0.25 * (100 - weather_risk)           # dry = higher QS
    + 0.15 * bullpen_state_of_own_team      # bullpen backs up 6+IP

k_ceiling (per start) = projected_Ks * 100 / 12
  # 12 Ks in a start = 100 ceiling

era_whip_risk (per start) = 0.5 * opp_wOBA_normalized
                          + 0.3 * park_hitter_factor
                          + 0.2 * pitcher_blowup_history

streamability_score (per start) =
    0.55 * qs_probability          # QS-league weight -- DOMINANT
  + 0.25 * k_ceiling
  + 0.20 * (100 - era_whip_risk)

streamability_score (per SP, two-start week) =
    mean(start_1_score, start_2_score)
  - opener_risk_penalty                    # -30 if either start has opener risk
  - coors_penalty                          # -10 if either start is at Coors
  - weather_penalty                        # -5 per start with rain risk > 30%
```

**Recommendation thresholds:**

| streamability_score | Recommendation (if FA) |
|---|---|
| >= 70 | ADD + START both. Bid $3-8 FAAB. |
| 55-69 | ADD + START both if SP slot open. Bid $1-3 FAAB. |
| 40-54 | Only add if you have daily flexibility to bench the bad start. |
| < 40 | SKIP. Two starts does not salvage two bad matchups. |

**Opener-risk teams (as of 2026-04-17, verify each week):**

| Team | Opener frequency | Typical starter IP |
|---|---|---|
| MIA | High | 3-4 IP |
| OAK | High | 3-5 IP |
| CHW | Moderate | 4-5 IP |
| PIT | Moderate | 4-5 IP |
| WAS | Occasional | 5-6 IP |

**Park-factor extremes (pitcher-friendly = high, hitter-friendly = low in pitcher_factor terms):**

| Park | Pitcher factor | Notes |
|---|---|---|
| Coors (COL) | ~20 | Disaster for any pitcher |
| GABP (CIN) | ~35 | Hitter-friendly, especially for LHB |
| Fenway (BOS) | ~45 | Lefty matters a lot |
| Petco (SDP) | ~65 | Pitcher-friendly |
| Oracle (SFG) | ~68 | Pitcher-friendly |
| T-Mobile (SEA) | ~70 | Most pitcher-friendly |

**Key resources:**

- **[resources/template.md](resources/template.md)**: Ranked two-start board output format with per-start breakdowns and verdict column
- **[resources/methodology.md](resources/methodology.md)**: Web-search recipes for FantasyPros + FanGraphs, cross-reference validation, opener detection, QS-weighted scoring procedure
- **[resources/evaluators/rubric_mlb_two_start_scout.json](resources/evaluators/rubric_mlb_two_start_scout.json)**: Quality criteria across 8 dimensions

**Inputs required:**

- Fantasy week definition (Monday date, Sunday date, ISO format)
- Yahoo free-agent pool for SP position (or handoff from `mlb-league-state-reader`)
- Web-search access (FantasyPros, FanGraphs, RotoWire weather, MLB.com)

**Outputs produced:**

- Ranked list of two-start SPs with per-start matchup scores
- Per-SP `streamability_score` (QS-weighted)
- Opener-risk flags and Coors/weather penalties
- Free-agent annotations
- Signal file `signals/YYYY-MM-DD-two-start.md` for downstream agents
