---
name: mlb-closer-tracker
description: Tracks the closer role and bullpen pecking order across all 30 MLB teams — who owns the ninth-inning job today, who is next in line if the current closer falters (the handcuff), and who carries DFA or demotion risk. Emits a per-reliever `save_role_certainty` signal (0-100) and flags speculation-worthy handcuffs for waiver bids. Use when the user mentions "closer", "save role", "handcuff", "ninth inning", "bullpen depth", lost save, blown save, committee, or when the waiver analyst needs to decide whether to spend FAAB on a backup reliever. This league uses SV as one of its five pitcher categories, but SV is also the most volatile and most punt-worthy cat, so tracking should always be paired with a punt-the-cat fallback recommendation.
---
# MLB Closer Tracker

## Table of Contents
- [Example](#example)
- [Workflow](#workflow)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Example

**Scenario**: User asks "who should I stash — any good handcuff closers on waivers?" in mid-April. Three teams of interest have unsettled ninth innings.

**Inputs gathered (web search — RotoBaller primary, Closer Monkey secondary, Athlon Closer Confidential)**:

| Team | Current 9th | Next in line | Third option | Situation |
|---|---|---|---|---|
| CLE | Emmanuel Clase | Cade Smith | Hunter Gaddis | Clase firmly locked — elite K/9 and walk rate |
| TEX | Chris Martin | Robert Garcia | Hoby Milner | Committee language from manager; Martin 39 years old |
| DET | Jason Foley | Tommy Kahnle | Beau Brieske | Foley has two blown saves in a week; velo down 1.2 mph |

**Signal emission (per RP)**:

| Pitcher | save_role_certainty | Owned in league? | Rec action |
|---|---|---|---|
| Emmanuel Clase | 95 | Yes (by user) | HOLD |
| Cade Smith | 35 | No | ADD on spec, BID $2 |
| Chris Martin | 55 | Yes (opponent) | IGNORE |
| Robert Garcia | 45 | No | ADD, BID $6 — true committee, high handcuff value |
| Jason Foley | 40 | Yes (opponent) | IGNORE (hold only if we owned him) |
| Tommy Kahnle | 50 | No | ADD, BID $8 — velo trend + recent Foley blowups = highest speculation value |

**Output signal file** (`signals/2026-04-17-closer.md`):

```yaml
---
type: closer
date: 2026-04-17
emitted_by: mlb-closer-tracker
confidence: 0.78
source_urls:
  - https://www.rotoballer.com/mlb-saves-closers-depth-charts/226767
  - https://closermonkey.com
  - https://www.athlonsports.com/fantasy/closer-confidential
---
```

**Punt-SV caveat surfaced**: "If all three speculation adds fail, remember SV is our most punt-worthy cat. A plan exists in `mlb-category-strategist` output to concede SV and redirect innings to K/QS — do not chase saves past $10 FAAB on any single handcuff."

**Handoff**: `mlb-waiver-analyst` reads the signal and sizes FAAB bids on Kahnle, Garcia, and Smith. `mlb-category-strategist` reads the same signal to decide whether to push or punt SV this week.

## Workflow

Copy this checklist and track progress:

```
Closer Tracker Progress:
- [ ] Step 1: Pull RotoBaller closer depth chart (all 30 teams)
- [ ] Step 2: Cross-reference Closer Monkey and Athlon Closer Confidential
- [ ] Step 3: Score save_role_certainty for the top 3 RPs per team
- [ ] Step 4: Flag committee / DFA-risk situations
- [ ] Step 5: Identify speculation-worthy handcuffs (rostered vs available)
- [ ] Step 6: Emit signal file and hand to waiver-analyst and category-strategist
```

**Step 1: Pull the RotoBaller closer depth chart**

Web-search `site:rotoballer.com closer depth chart 2026` or hit the URL directly. This is the primary source for all 30 teams. Record each team's top 3 relievers with the role tag RotoBaller assigns (Closer / Next Man Up / Committee / Setup).

See [resources/methodology.md](resources/methodology.md#primary-source-rotoballer) for the source hierarchy and how to handle stale pages.

- [ ] All 30 teams covered (no team skipped even if role is stable)
- [ ] Top 3 RPs recorded per team
- [ ] RotoBaller role label captured verbatim

**Step 2: Cross-reference secondary sources**

Closer Monkey and Athlon's "Closer Confidential" often lead RotoBaller by 24-48 hours on role changes, especially early season. If two sources disagree, that disagreement itself lowers `save_role_certainty` (volatility penalty).

See [resources/methodology.md](resources/methodology.md#secondary-sources) for tie-break rules.

- [ ] Closer Monkey checked for the top 8-10 volatile situations
- [ ] Athlon Closer Confidential grade captured (if April / early-season)
- [ ] Any disagreements logged as volatility flags

**Step 3: Score save_role_certainty**

Use the scoring rubric in [resources/methodology.md](resources/methodology.md#save-role-certainty-rubric). The five inputs are: role label, recent blown saves, velocity trend, manager public comments, contract/age status. Output 0-100.

- [ ] Each top-3 RP scored
- [ ] Committee situations: no RP scores above 60
- [ ] Locked closers score 85-100
- [ ] DFA / demotion risk scores below 30

**Step 4: Flag committee and DFA-risk situations**

A committee is worth flagging even when we own the current "closer" — volatility means save_role_certainty is low regardless of who holds the ninth inning right now. DFA risk applies when an RP has lost the role AND is burning option years or is on a non-guaranteed deal.

- [ ] Committee flag on any team where top-2 scores are within 15 points
- [ ] DFA-risk flag on any ex-closer with role_certainty < 25

**Step 5: Identify speculation targets**

A speculation target = handcuff (next-in-line) with `save_role_certainty` in the 30-60 range whose current closer has any of: recent blown saves (2+ in 10 days), velocity loss (>1 mph), negative manager quote, age/injury flag.

See [resources/template.md](resources/template.md#speculation-target-table) for the output format.

- [ ] Each target is cross-referenced against Yahoo availability
- [ ] Targets ranked by expected save share × availability
- [ ] No speculation bid > $10 FAAB without category-strategist concurrence (SV is the most punt-worthy cat)

**Step 6: Emit signal file**

Write `signals/YYYY-MM-DD-closer.md` with one `save_role_certainty` entry per top-3 RP per team (up to 90 entries). Call `mlb-signal-emitter` to validate. See [resources/template.md](resources/template.md) for the full output structure.

- [ ] Frontmatter complete: type, date, emitted_by, confidence, source_urls
- [ ] Every RP has `save_role_certainty` in valid 0-100 range
- [ ] Committee and DFA flags included
- [ ] Handcuff recommendations ranked

Validate using [resources/evaluators/rubric_mlb_closer_tracker.json](resources/evaluators/rubric_mlb_closer_tracker.json). Minimum standard: average score 3.5 or above.

## Common Patterns

**Pattern 1: Locked Elite Closer (Clase, Duran, Iglesias tier)**
- `save_role_certainty`: 85-100 for incumbent, 15-25 for handcuff
- Handcuff has low speculation value unless incumbent is injured
- Action: HOLD if owned; no spec bid on handcuff

**Pattern 2: True Committee (manager public quote: "we'll use matchups")**
- `save_role_certainty`: 40-60 for top 2-3 arms, top-2 within 15 points
- Handcuff value is HIGH — both arms can vulture saves
- Action: If no cheap closer owned, ADD the platoon handcuff (opposite-handed reliever)

**Pattern 3: Veteran Closer On Thin Ice (age 35+, declining velo)**
- `save_role_certainty`: 55-75 for incumbent, 40-55 for heir
- Incumbent could be removed mid-April on any rough stretch
- Action: Stash the heir — this is the highest EV speculation profile

**Pattern 4: DFA-Risk Ex-Closer**
- `save_role_certainty`: < 25
- Role already lost; roster spot at risk if he can't hold setup
- Action: DROP if owned; never ADD

## Guardrails

1. **Cover all 30 teams every run.** Even locked situations need a score so downstream agents can reason about trade targets. A missing team is worse than a low-confidence score.

2. **Web-search every time.** Closer roles change overnight. A 24-hour-old RotoBaller snapshot is stale. Always pull fresh on the day you emit the signal.

3. **Committees penalize even the current closer.** If three sources call a situation a committee, the named closer does not get an 85 score — they get a 55 at most. Volatility = low certainty, regardless of who just got the last save.

4. **Never recommend a FAAB bid above $10 on a single handcuff without category-strategist concurrence.** SV is this league's most punt-worthy pitcher category. Over-spending on speculative saves drains FAAB that could land a two-start SP or a breakout hitter. The waiver-analyst enforces this ceiling.

5. **Velocity is the leading indicator.** A 1+ mph drop on a closer's fastball, sustained across 3+ outings, predicts role loss better than any single blown save. Weight velocity trend heavily in the scoring rubric.

6. **Manager quotes are data, not noise.** "He's our guy" is a 70-certainty statement. "We'll see how it plays out" is a 50. Silence after a blown save is a 40. Quote-mine the beat writer coverage (Athletic, MLB.com team pages) during volatile weeks.

7. **Platoon handcuffs matter.** If the incumbent closer is RHP and has poor splits vs LHB, the LHP setup man is a better speculation target than the RHP setup man — even if RotoBaller lists the RHP higher. Check the actual platoon usage pattern.

8. **Handcuffs are dropped first on a healthy week.** A speculation add that does not vulture a save within 10 days gets dropped for the next wave. Do not fall in love with stashes — rotate.

## Quick Reference

**Key formula (save_role_certainty):**

```
save_role_certainty = 20 x role_label_score       (0-5 scale)
                    + 20 x recent_performance     (0-5 scale: blown saves, ERA last 10 days)
                    + 20 x velocity_trend         (0-5 scale: delta from baseline)
                    + 20 x manager_signal         (0-5 scale: public quotes)
                    + 20 x contract_age_security  (0-5 scale)
```

All components 0-5, weighted equally, rescaled to 0-100.

**Role label to score mapping (RotoBaller):**

| RotoBaller label | role_label_score (0-5) |
|---|---|
| Closer (locked) | 5 |
| Closer (soft hold) | 4 |
| Committee — primary | 3 |
| Committee — secondary | 2 |
| Setup / Next Man Up | 2 |
| Middle relief | 1 |
| DFA-risk / demoted | 0 |

**Handcuff speculation tiers:**

| Tier | save_role_certainty (current closer) | Handcuff action |
|---|---|---|
| 1. Panic closer | < 50 | ADD handcuff — BID $5-10 |
| 2. Wobbly closer | 50-70 | ADD handcuff — BID $2-5 |
| 3. Stable closer | 70-85 | ADD handcuff only if cheap ($0-1) |
| 4. Elite closer | > 85 | IGNORE handcuff unless injury |

**Punt-SV trigger**: If 4+ of your 5 RP slots would need to be speculation closers to compete in SV this week, punt SV instead. Hand off to `mlb-category-strategist` with a `cat_punt_score` boost request.

**Key resources:**

- **[resources/template.md](resources/template.md)**: Per-team depth chart output format, speculation target table, full signal file template
- **[resources/methodology.md](resources/methodology.md)**: Source hierarchy, scoring rubric, committee detection, punt-SV decision logic
- **[resources/evaluators/rubric_mlb_closer_tracker.json](resources/evaluators/rubric_mlb_closer_tracker.json)**: 8-criterion quality rubric

**Inputs required:**

- RotoBaller closer depth charts (all 30 teams)
- Closer Monkey recent updates (volatile situations)
- Athlon Closer Confidential grades (early season)
- Yahoo league availability (which handcuffs are free agents)
- Recent game logs for top-3 RPs per team (blown saves, velocity)

**Outputs produced:**

- Per-RP `save_role_certainty` (0-100), up to ~90 entries
- Per-team depth chart with role labels and volatility flags
- Ranked list of speculation-worthy handcuffs with recommended FAAB bid bands
- Punt-SV recommendation flag (if triggered)
