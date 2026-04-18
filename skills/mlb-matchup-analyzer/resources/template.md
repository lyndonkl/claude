# MLB Matchup Analyzer — Signal File Template

Copy this template to `signals/YYYY-MM-DD-matchup.md` and fill in the blanks. Every value must trace to a cited URL. Leave `confidence` below 0.4 for any signal where a source could not be reached, and flag it in red team findings.

## Table of Contents
- [Full Signal File Template](#full-signal-file-template)
- [Matchup Summary Table](#matchup-summary-table)
- [Platoon Narrative Template](#platoon-narrative-template)
- [Bullpen State Worksheet](#bullpen-state-worksheet)
- [Park Factor Normalization Worksheet](#park-factor-normalization-worksheet)

---

## Full Signal File Template

```markdown
---
type: matchup
date: YYYY-MM-DD
game: "AWY @ HOM"                    # e.g., "TB @ COL"
venue: ""                             # e.g., "Coors Field"
first_pitch_local: "HH:MM TZ"         # e.g., "19:10 MT"
emitted_by: mlb-matchup-analyzer
variant_synthesis: false              # this skill is single-pass; agents that consume it run variants
synthesis_confidence: 0.0             # overall confidence in the matchup picture (0.0-1.0)
signals:
  opp_sp_quality_vs_home_hitters: 0   # 0-100, 50 = league-average SP
  opp_sp_quality_vs_away_hitters: 0   # 0-100
  park_hitter_factor: 50              # 0-100, 50 = neutral
  park_pitcher_factor: 50             # 0-100, 50 = neutral
  park_hitter_factor_RHB: 50          # handedness-specific, if material
  park_hitter_factor_LHB: 50
  weather_risk: 0                     # 0-100, 0 = no disruption
  bullpen_state_home: 50              # 0-100
  bullpen_state_away: 50              # 0-100
  roof_status: "open|closed|dome|n/a"
red_team_findings:
  - severity: 0                       # 1-5
    likelihood: 0                     # 1-5
    score: 0                          # severity x likelihood
    note: ""
    mitigation: ""
source_urls:
  - https://www.mlb.com/probable-pitchers
  - https://www.fangraphs.com/guts.aspx?type=pf&season=YYYY
  - https://www.rotowire.com/baseball/weather-forecast.php
  - https://www.rotoballer.com/mlb-saves-closers-depth-charts/...
computed_at: YYYY-MM-DDTHH:MMZ
---

# Matchup: AWY @ HOM — YYYY-MM-DD

<Matchup summary table goes here — see below.>

## Probable Starters

<Home SP, Away SP summary.>

## Park Context

<Park factor detail + handedness splits.>

## Weather

<Forecast + roof status + risk interpretation.>

## Bullpen State

<Per-team bullpen summary.>

## Platoon Implications

<Jargon-free narrative — see template below.>

## Sources

<Bulleted list of every URL consulted.>
```

---

## Matchup Summary Table

A one-glance table at the top of the body. Every value comes from the frontmatter `signals:` block.

| Signal | Home View | Away View | Neutral (50) | Interpretation |
|---|---|---|---|---|
| `opp_sp_quality` (the SP they face) | ____ | ____ | 50 | Higher = tougher matchup for these hitters |
| `park_hitter_factor` | ____ | ____ | 50 | >50 = hitter-friendly park |
| `park_pitcher_factor` | ____ | ____ | 50 | >50 = pitcher-friendly park |
| `weather_risk` | ____ | ____ | n/a | Higher = more postponement / in-game disruption risk |
| `bullpen_state` | ____ | ____ | 50 | Higher = healthier / rested |
| `roof_status` | ____ | ____ | — | open / closed / dome / n/a |

**Overall read (1-2 sentences, beginner-level English):**

> ____

---

## Platoon Narrative Template

For each hitter the consuming agent is deciding on, produce a short block. Never use the word "splits" without translating it. Never write L/R handedness abbreviations without spelling them out first.

**Per-hitter narrative block:**

```
**{Hitter name} ({team}, bats {left|right|switch})**

They face {SP name}, a {left-handed|right-handed} pitcher. This is
{a platoon advantage for the hitter | a neutral handedness matchup | a disadvantage for the hitter}
because {plain-English reason — e.g., "right-handed hitters generally hit
left-handed pitchers better, and {Hitter} is no exception"}.

{If the hitter has strong handedness-specific numbers, cite them in plain English,
e.g., "Last season {Hitter} got on base 38% of the time against
right-handers vs 33% against left-handers."}

Park context: {one sentence on how the park amplifies or mutes this matchup
for this hitter's handedness}.

Verdict for the consuming agent: {matchup_score tilt: positive / neutral /
negative}. {One-sentence why.}
```

**Example** (Junior Caminero, TB, right-handed bat, facing German Marquez, right-handed pitcher, at Coors):

> Junior Caminero (TB, bats right) faces German Marquez, a right-handed
> pitcher. This is a neutral handedness matchup — hitters don't get a platoon
> edge when they bat the same side as the pitcher. However, Marquez has
> struggled in 2026 (ERA 5.10, opponents are hitting the ball very hard
> against him), and Coors Field is the single best hitter park in MLB —
> fly balls carry further in Denver's thin air. Even without a platoon
> edge, this is a strong positive matchup for Caminero.
>
> **Verdict: matchup tilt positive.**

---

## Bullpen State Worksheet

Fill one table per team.

**Team: ____ (home | away)**

| Role | Pitcher | Last pitched (days ago) | Pitches thrown last 3 days | Available today? | Notes |
|---|---|---|---|---|---|
| Closer | | | | Y/N | |
| Setup (high-leverage) | | | | Y/N | |
| Setup #2 | | | | Y/N | |
| Middle relief | | | | Y/N | |

**Scoring:**

```
Start at 50.
- If closer NOT available:          -15
- For each high-leverage arm NOT available: -10
- If 2+ middle relievers unavailable:       -5
+ If closer had 2+ days rest AND at least 3 of top 4 arms rested: +5
Clamp to [0, 100].
```

`bullpen_state_{team}` = ____

---

## Park Factor Normalization Worksheet

Convert FanGraphs park factors (centered near 1.00 where 1.00 = neutral) to the 0-100 scale where 50 = neutral.

**Home park: ____**

| Metric | Raw FG Factor (YYYY) | Normalized (0-100) | Source URL |
|---|---|---|---|
| wOBAcon (overall) | | | |
| wOBAcon vs RHP (LHB park factor) | | | |
| wOBAcon vs LHP (RHB park factor) | | | |
| HR factor — RHB | | | |
| HR factor — LHB | | | |

**Formula:**

```
normalized = 50 + (raw_factor - 1.00) * 200
clamp to [0, 100]
```

**Sanity checks:**
- Coors Field should land ~70-80 on the hitter scale (strongly hitter-friendly)
- Oracle Park / T-Mobile Park should land ~25-35 (strongly pitcher-friendly)
- A truly neutral park (raw factor 1.00) must produce exactly 50

If the distribution of all 30 parks does not center on 50 with ~15 SD, re-anchor.

---

## Source URL Checklist

Before emitting the signal file, verify every URL is present:

- [ ] MLB.com probable pitchers page (or FanGraphs Roster Resource probables grid as fallback)
- [ ] FanGraphs park factors page for the current season
- [ ] RotoWire weather-forecast page (or Google weather as fallback)
- [ ] RotoBaller closer depth chart (or Pitcher List bullpen report as fallback)
- [ ] FanGraphs splits page for each key hitter cited in the platoon narrative
- [ ] Any injury/usage report cited in bullpen state

If any of the above is missing or failed to load, drop `synthesis_confidence` to 0.3 or lower and add a red_team_findings entry describing the gap.
