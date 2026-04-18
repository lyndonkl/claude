# Player Signal File Template

This is the schema for `signals/YYYY-MM-DD-player-<lastname>-<firstinitial>.md`. One file per player analyzed per day. Two variants below: **hitter** and **pitcher**. A worked example follows each.

All YAML keys in the frontmatter are required unless marked optional. Signal numeric values must fall in their declared ranges per `signal-framework.md` (0-100 unipolar, +/-100 bipolar).

---

## Hitter template

```markdown
---
type: player
role: hitter
date: YYYY-MM-DD
computed_at: YYYY-MM-DDTHH:MMZ
emitted_by: mlb-player-analyzer
player_name: "First Last"
mlb_team: XXX                      # 3-letter abbr (TB, LAD, BOS, ...)
position: "3B"                     # primary position today
opp_team: XXX
opp_sp: "First Last"               # or null if unannounced
opp_sp_hand: R                     # R or L
park: "Park Name"
variant_synthesis: false           # this skill emits raw signals; synthesis happens at the agent layer
signals:
  form_score: 66
  matchup_score: 58
  opportunity_score: 78
  daily_quality: 66                # = 0.35*form + 0.40*matchup + 0.25*opportunity
  regression_index: 15             # +/- 100, positive = unlucky
  obp_contribution: 62
  sb_opportunity: 35
  role_certainty: 100
confidence:
  form_score: 0.85
  matchup_score: 0.80
  opportunity_score: 0.95
  daily_quality: 0.85
  regression_index: 0.80
  obp_contribution: 0.75
  sb_opportunity: 0.65
  role_certainty: 1.00
source_urls:
  - https://baseballsavant.mlb.com/savant-player/<slug>
  - https://www.fangraphs.com/players/<slug>/<id>
  - https://www.fangraphs.com/players/<slug>/<id>?position=&stats=bat&type=splits
  - https://www.mlb.com/starting-lineups
  - https://www.rotowire.com/baseball/weather-forecast.php
red_team_findings:
  - severity: 1
    likelihood: 2
    score: 2
    note: "Sprint speed from 2025; 2026 not yet populated on Savant"
    mitigation: "Re-check in 2 weeks"
---

# <Player Name> — <Date>

## What the signals say, in plain English

<2-3 sentences translating the key numbers. Example: "Caminero is in form
(hitting the ball hard even when outs find gloves), faces a middling righty
in a hitter-friendly park, and is locked into the #3 spot for ~4.6 plate
appearances. Start him.">

## Signal table

| Signal | Value | Read |
|---|---|---|
| form_score | 66 | Rolling 15-day xwOBA 15% above season baseline |
| matchup_score | 58 | Decent park (Fenway +3 R), neutral SP, slight wind-aided |
| opportunity_score | 78 | Confirmed #3 slot, ~4.6 expected PAs |
| **daily_quality** | **66** | **START** (threshold: >=60) |
| regression_index | +15 | Slightly unlucky -- room to run |
| obp_contribution | 62 | Projected .355 OBP x 4.6 PAs |
| sb_opportunity | 35 | Bello holds runners average, BOS catcher CS 28% |
| role_certainty | 100 | Lineup posted |

## Action for downstream agents

- **lineup-optimizer**: START
- **category-strategist**: OBP contributor, mild SB upside
- **waiver-analyst**: no action (owned)
- **regression flag**: positive +15 -- buy window, do not trade away
```

---

## Hitter — worked example

```markdown
---
type: player
role: hitter
date: 2026-04-17
computed_at: 2026-04-17T13:42Z
emitted_by: mlb-player-analyzer
player_name: "Junior Caminero"
mlb_team: TB
position: "3B"
opp_team: BOS
opp_sp: "Brayan Bello"
opp_sp_hand: R
park: "Fenway Park"
variant_synthesis: false
signals:
  form_score: 66
  matchup_score: 58
  opportunity_score: 78
  daily_quality: 66
  regression_index: 15
  obp_contribution: 62
  sb_opportunity: 35
  role_certainty: 100
confidence:
  form_score: 0.85
  matchup_score: 0.80
  opportunity_score: 0.95
  daily_quality: 0.85
  regression_index: 0.80
  obp_contribution: 0.75
  sb_opportunity: 0.65
  role_certainty: 1.00
source_urls:
  - https://baseballsavant.mlb.com/savant-player/junior-caminero-676609
  - https://www.fangraphs.com/players/junior-caminero/27479
  - https://www.fangraphs.com/players/junior-caminero/27479?position=3B&stats=bat&type=splits
  - https://www.mlb.com/starting-lineups
  - https://www.rotowire.com/baseball/weather-forecast.php
  - https://www.fangraphs.com/guts.aspx?type=pf&season=2026&teamid=3
red_team_findings:
  - severity: 1
    likelihood: 2
    score: 2
    note: "Caminero sprint speed drawn from partial 2026 sample (sub-50 PAs)"
    mitigation: "Re-weight sb_opportunity confidence down if sample stays sparse through May"
---

# Junior Caminero — 2026-04-17

## What the signals say, in plain English

Caminero has been hitting the ball hard for the past two weeks (scouts would
call it "loud contact") even when the results are ordinary. He faces a
right-handed pitcher he should handle fine in a park that helps hitters.
He is batting third and will get five chances at the plate. **START him
today.**

## Signal table

| Signal | Value | Read |
|---|---|---|
| form_score | 66 | 15-day xwOBA .410 vs season .355 |
| matchup_score | 58 | Fenway +3 R factor, Bello is league-average RHP, wind 8mph LF-to-CF |
| opportunity_score | 78 | #3 hitter, expected 4.6 PAs |
| **daily_quality** | **66** | **START** |
| regression_index | +15 | Season wOBA .340 vs xwOBA .370 -- slightly unlucky |
| obp_contribution | 62 | Projected OBP .355 x 4.6 PAs |
| sb_opportunity | 35 | Bello average at holding runners; BOS catcher CS 28% |
| role_certainty | 100 | Confirmed #3 on MLB.com starting lineups |

## Action for downstream agents

- **mlb-lineup-optimizer**: START
- **mlb-category-strategist**: contributes OBP + HR; modest SB upside
- **mlb-regression-flagger**: +15 buy-window; do not shop in trade
- **mlb-waiver-analyst**: rostered, no action
```

---

## Pitcher template

```markdown
---
type: player
role: pitcher
subrole: SP                        # SP or RP
date: YYYY-MM-DD
computed_at: YYYY-MM-DDTHH:MMZ
emitted_by: mlb-player-analyzer
player_name: "First Last"
mlb_team: XXX
opp_team: XXX
park: "Park Name"
variant_synthesis: false
signals:
  qs_probability: 48               # 0-100; probability of 6+ IP and <=3 ER
  k_ceiling: 62                    # 0-100; projected Ks normalized
  era_whip_risk: 44                # 0-100; blowup risk
  streamability_score: 56          # = 0.40*qs_prob + 0.30*k_ceiling + 0.30*(100 - era_whip_risk)
  two_start_bonus: false           # bool
  save_role_certainty: null        # only populated for RP
confidence:
  qs_probability: 0.75
  k_ceiling: 0.80
  era_whip_risk: 0.70
  streamability_score: 0.75
  two_start_bonus: 1.00
  save_role_certainty: null
source_urls:
  - https://www.fangraphs.com/players/<slug>/<id>
  - https://baseballsavant.mlb.com/savant-player/<slug>
  - https://www.fantasypros.com/mlb/two-start-pitchers.php
  - https://www.mlb.com/probable-pitchers
red_team_findings:
  - severity: 2
    likelihood: 3
    score: 6
    note: "Opponent lineup missing two LHH -- right-handed threat elevated"
    mitigation: "k_ceiling could be lower than computed; trim by ~5"
---

# <Pitcher Name> — <Date>

## What the signals say, in plain English

<2-3 sentences. Example: "Bowden Francis is a decent K arm but he pitches in
Coors today. Every rate stat you care about will get worse. Ks might hold up,
but ERA and WHIP will take a hit. **Do not stream.**">

## Signal table

| Signal | Value | Read |
|---|---|---|
| qs_probability | 28 | Career QS rate 45%, but Coors cuts it ~60% |
| k_ceiling | 40 | Projected 4.1 Ks -- below stream-level 6 |
| era_whip_risk | 82 | Coors + COL wOBA vs RHP .335 |
| **streamability_score** | **32** | **SIT** (threshold: >=70) |
| two_start_bonus | false | Single start this week |
| save_role_certainty | -- | N/A (SP) |

## Action for downstream agents

- **mlb-streaming-strategist**: DO NOT STREAM
- **mlb-lineup-optimizer**: SIT (if rostered)
- **mlb-waiver-analyst**: no action
```

---

## Pitcher — worked example (RP closer)

```markdown
---
type: player
role: pitcher
subrole: RP
date: 2026-04-17
computed_at: 2026-04-17T13:55Z
emitted_by: mlb-player-analyzer
player_name: "Emmanuel Clase"
mlb_team: CLE
opp_team: CWS
park: "Guaranteed Rate Field"
variant_synthesis: false
signals:
  qs_probability: null
  k_ceiling: 58
  era_whip_risk: 22
  streamability_score: null
  two_start_bonus: null
  save_role_certainty: 95
confidence:
  qs_probability: null
  k_ceiling: 0.85
  era_whip_risk: 0.85
  streamability_score: null
  two_start_bonus: null
  save_role_certainty: 0.95
source_urls:
  - https://baseballsavant.mlb.com/savant-player/emmanuel-clase-661403
  - https://www.fangraphs.com/players/emmanuel-clase/19222
  - https://www.rotoballer.com/mlb-saves-closers-depth-charts/226767
red_team_findings: []
---

# Emmanuel Clase — 2026-04-17

## What the signals say, in plain English

Clase is the locked-in closer in Cleveland. He gets the 9th inning when
Cleveland leads. Low blowup risk, moderate strikeouts, reliable saves.
**Keep rostered; no action needed.**

## Signal table

| Signal | Value | Read |
|---|---|---|
| k_ceiling | 58 | ~1.2 K per appearance projected |
| era_whip_risk | 22 | Elite command, hard cutter, low walk rate |
| save_role_certainty | 95 | RotoBaller Tier 1 closer, no committee risk |

## Action for downstream agents

- **mlb-lineup-optimizer**: START (saves opportunity if CLE leads)
- **mlb-waiver-analyst**: HOLD (high value)
- **mlb-category-strategist**: anchor SV contributor
```

---

## Field-by-field notes

- **`confidence:`** per-signal floats in [0.0, 1.0]. If any component's confidence < 0.4, populate `red_team_findings` with the gap and a mitigation.
- **`source_urls:`** must list the actual URLs visited in this analysis. Do not list generic landing pages if a specific player page was used.
- **`signals.daily_quality`** for hitters and **`signals.streamability_score`** for SPs are the **primary** signals the lineup-optimizer and streaming-strategist consume. Downstream agents read these; they do not recompute.
- **Unused signals** (e.g., `qs_probability` on a hitter file, `sb_opportunity` on a pitcher) are omitted or set to `null`. Do not write zero -- zero means "the number is zero," which is a different claim.
- **Red-team findings** follow the severity(1-3) x likelihood(1-3) = score rubric from the signal framework. Any signal with confidence < 0.4 should surface a finding.
