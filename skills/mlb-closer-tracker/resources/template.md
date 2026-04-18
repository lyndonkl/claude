# MLB Closer Tracker Templates

Output formats for the per-team closer depth chart, the per-RP `save_role_certainty` signal, speculation target tables, and the full signal file.

## Table of Contents
- [Signal File Frontmatter](#signal-file-frontmatter)
- [Per-Team Depth Chart Table](#per-team-depth-chart-table)
- [Per-RP save_role_certainty Entry](#per-rp-save_role_certainty-entry)
- [Speculation Target Table](#speculation-target-table)
- [Committee / DFA-Risk Flag Table](#committee--dfa-risk-flag-table)
- [Full Signal File Skeleton](#full-signal-file-skeleton)
- [Punt-SV Recommendation Block](#punt-sv-recommendation-block)

---

## Signal File Frontmatter

Every closer signal file begins with this YAML block. Paste into the top of `signals/YYYY-MM-DD-closer.md`.

```yaml
---
type: closer
date: YYYY-MM-DD
emitted_by: mlb-closer-tracker
variant_synthesis: true
variants_fired: [advocate, critic]
synthesis_confidence: 0.__
confidence: 0.__
red_team_findings:
  - severity: _
    likelihood: _
    score: _
    note: "___"
    mitigation: "___"
source_urls:
  - https://www.rotoballer.com/mlb-saves-closers-depth-charts/226767
  - https://closermonkey.com
  - https://www.athlonsports.com/fantasy/closer-confidential
  - https://baseball.fantasysports.yahoo.com/b1/23756/position_depth_chart?pos=CL
teams_covered: 30
rps_scored: __
committees_flagged: __
dfa_risks_flagged: __
speculation_adds: __
punt_sv_recommended: false
---
```

`teams_covered` must equal 30 for a complete run. If less, note the missing teams in the body.

---

## Per-Team Depth Chart Table

One table per team, 30 tables total. Group alphabetically by team abbreviation.

### Template (copy 30 times)

**[TEAM]** — _situation one-liner_

| Slot | Pitcher | RotoBaller label | save_role_certainty | Throws | Owned? | Notes |
|---|---|---|---|---|---|---|
| 9th inning | _____ | _____ | __/100 | R/L | Yes / No / User | _____ |
| Next in line | _____ | _____ | __/100 | R/L | Yes / No / User | _____ |
| Third option | _____ | _____ | __/100 | R/L | Yes / No / User | _____ |

**Situation tag**: Locked / Soft hold / Committee / DFA-risk / Injury-gap

**Volatility flag**: Yes / No — _reason_

### Filled example (Cleveland Guardians)

**CLE** — elite incumbent; handcuff has no current path.

| Slot | Pitcher | RotoBaller label | save_role_certainty | Throws | Owned? | Notes |
|---|---|---|---|---|---|---|
| 9th inning | Emmanuel Clase | Closer (locked) | 95/100 | R | User | Elite K-BB%, velo stable |
| Next in line | Cade Smith | Setup | 35/100 | R | No | High-K setup, 2025 breakout |
| Third option | Hunter Gaddis | Middle relief | 15/100 | R | No | Long relief / multi-inning |

**Situation tag**: Locked
**Volatility flag**: No

---

## Per-RP save_role_certainty Entry

In the body of the signal file, after the depth charts, emit a flat table of every scored RP so downstream agents can filter quickly.

| Pitcher | Team | save_role_certainty | Role slot | Committee? | DFA-risk? | Speculation target? |
|---|---|---|---|---|---|---|
| _____ | ___ | ___/100 | 9th / Next / Third | Y/N | Y/N | Y/N |
| _____ | ___ | ___/100 | 9th / Next / Third | Y/N | Y/N | Y/N |
| ... | ... | ... | ... | ... | ... | ... |

Sort by descending `save_role_certainty` within each team block; or fully flat and sorted by team abbreviation for downstream consumption.

---

## Speculation Target Table

Specific section for waiver-analyst consumption. Only include RPs with `save_role_certainty` between 30 and 60 whose current closer shows at least one volatility flag.

| Rank | Pitcher | Team | save_role_certainty | Incumbent | Incumbent flag | FAAB band | Priority |
|---|---|---|---|---|---|---|---|
| 1 | _____ | ___ | __/100 | _____ | _____ | $__-$__ | High / Med / Low |
| 2 | _____ | ___ | __/100 | _____ | _____ | $__-$__ | High / Med / Low |
| ... | ... | ... | ... | ... | ... | ... | ... |

**Incumbent flag legend** (fill the column with whichever applies):
- 2+ blown saves in 10 days
- Velo -1 mph or more across 3+ outings
- Manager quote: non-committal
- Age 35+ with declining trend
- Recently returned from IL

**FAAB band guidance** (cap at $10 unless category-strategist concurs):

| save_role_certainty of handcuff | Band |
|---|---|
| 50-60 | $6-10 |
| 40-50 | $3-6 |
| 30-40 | $1-3 |

---

## Committee / DFA-Risk Flag Table

| Team | Flag type | Pitchers involved | save_role_certainty spread | Recommended action |
|---|---|---|---|---|
| ___ | Committee | _____, _____, _____ | __-__/100 | Target platoon-advantaged arm; BID $__ |
| ___ | DFA-risk | _____ | __/100 | DROP if owned; never ADD |

A committee flag fires when the top-2 RPs on a team are within 15 points of each other on `save_role_certainty`.

A DFA-risk flag fires when an ex-closer's `save_role_certainty` is below 25 AND they are out of options / have no guaranteed contract.

---

## Full Signal File Skeleton

```markdown
---
[frontmatter from above]
---

# Closer Tracker — YYYY-MM-DD

## Summary

- 30 teams covered
- __ RPs scored (top 3 per team = 90 entries)
- __ committees flagged
- __ DFA-risks flagged
- __ speculation targets surfaced
- Punt-SV recommended: Yes / No

## Speculation targets (ranked)

[speculation target table]

## Committees and DFA-risks

[flag table]

## Per-team depth charts

[30 per-team depth chart tables, alphabetical by abbreviation]

## Flat per-RP table

[flat save_role_certainty table, sorted]

## Punt-SV recommendation

[punt-sv block if triggered, else "Not triggered this week."]

## Sources

[source URLs and last-updated timestamps]

## Red-team findings

[risks noted in frontmatter, expanded]
```

---

## Punt-SV Recommendation Block

Include when the punt-SV trigger fires (see [methodology.md](methodology.md#punt-sv-trigger)).

```markdown
## Punt-SV recommendation

**Trigger**: __ of 5 RP slots would need to hold speculation closers to compete in SV this week.

**Context**: SV is the most volatile of our 5 pitcher categories (K / ERA / WHIP / QS / SV). Speculation closers bust ~50% of the time within 30 days.

**Recommendation to category-strategist**: Boost `cat_punt_score` for SV by +20. Redirect the 5 RP slots toward high-K setup arms (ratio help) and a second two-start SP window.

**Action ladder**:
- DROP: any speculation closer under $3 FAAB invested
- HOLD: locked closers already rostered (ratios + K value remain)
- ADD: one high-K setup man (Devin Williams / Bryan Abreu archetype) to stabilize ratios

**Review date**: next Sunday's category-state read.
```
