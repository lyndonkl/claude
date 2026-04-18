# MLB Category State Analyzer — Signal File Template

Output template for the weekly category-state signal file emitted by `mlb-category-state-analyzer`. Write to `signals/YYYY-MM-DD-cat-state.md`.

## Table of Contents
- [Signal File Header](#signal-file-header)
- [Matchup Snapshot](#matchup-snapshot)
- [Per-Cat Signal Table](#per-cat-signal-table)
- [Overall Recommendation](#overall-recommendation)
- [Downstream Routing Hints](#downstream-routing-hints)
- [Red-Team Findings](#red-team-findings)
- [Worked Example (Filled)](#worked-example-filled)

---

## Signal File Header

Every signal file opens with YAML frontmatter. Fields marked `required` must be populated; `optional` fields are populated when the data is available.

```yaml
---
type: cat-state                                                # required, fixed
date: 2026-04-17                                               # required
emitted_by: mlb-category-state-analyzer                        # required, fixed
week: 3                                                        # required, fantasy week number
matchup_opponent: Los Doyers                                   # required
scoring_days_remaining: 4                                      # required, 0-7
variant_synthesis: true                                        # optional (if run via coach)
variants_fired: [advocate, critic]                             # optional
synthesis_confidence: 0.78                                     # required, 0.0-1.0
red_team_findings:                                             # optional list
  - severity: 2                                                # 1-3
    likelihood: 3                                              # 1-3
    score: 6                                                   # severity × likelihood
    note: "Opp has two-start ace (Skubal) scheduled — could flip K, ERA, WHIP together"
    mitigation: "Stream a second ace on our two-start day Friday"
source_urls:                                                   # required, min 2
  - https://baseball.fantasysports.yahoo.com/b1/23756/5/matchup?week=3
  - https://www.mlb.com/schedule/2026-04-17
---
```

---

## Matchup Snapshot

A compact current-state table so the coach doesn't need to re-fetch the matchup page.

### Current scores and volume

| Cat | Us | Opp | Margin | Our vol. | Opp vol. | Vol. edge |
|---|---|---|---|---|---|---|
| R | ____ | ____ | +/- ____ | ____ games | ____ games | us/opp/even |
| HR | ____ | ____ | +/- ____ | ____ games | ____ games | us/opp/even |
| RBI | ____ | ____ | +/- ____ | ____ games | ____ games | us/opp/even |
| SB | ____ | ____ | +/- ____ | ____ games | ____ games | us/opp/even |
| OBP | .___ (__ PA) | .___ (__ PA) | +/- .___ | __ PAs left | __ PAs left | us/opp/even |
| K | ____ | ____ | +/- ____ | __ SP starts | __ SP starts | us/opp/even |
| ERA | _.__ (__ IP) | _.__ (__ IP) | +/- _.__ | __ IP left | __ IP left | us/opp/even |
| WHIP | _.__ (__ IP) | _.__ (__ IP) | +/- _.__ | __ IP left | __ IP left | us/opp/even |
| QS | ____ | ____ | +/- ____ | __ SP starts | __ SP starts | us/opp/even |
| SV | ____ | ____ | +/- ____ | __ RP days | __ RP days | us/opp/even |

- **Total hitter games remaining (us / opp)**: ____ / ____
- **Total SP starts remaining (us / opp)**: ____ / ____
- **Total IP projected (us / opp)**: ____ / ____
- **Minimum-IP threshold** (this league): 20 IP. Opp on-pace / off-pace: ____.
- **Minimum-PA threshold** (this league): ____ PA. Opp on-pace / off-pace: ____.

---

## Per-Cat Signal Table

**The primary output.** Fill all four signals for every one of the 10 cats.

| Cat | Position | Pressure | Reachability | Punt Score | Verdict | Rationale (1 line) |
|---|---|---|---|---|---|---|
| R | winning/tied/losing | 0–100 | 0–100 | 0–100 | push/maintain/punt | |
| HR | | | | | | |
| RBI | | | | | | |
| SB | | | | | | |
| **OBP** | | | | | | ratio cat — denominator matters |
| K | | | | | | |
| **ERA** | | | | | | ratio cat — IP threshold matters |
| **WHIP** | | | | | | ratio cat — IP threshold matters |
| **QS** | | | | | | 6+ IP ≤3 ER (not W) |
| **SV** | | | | | | volatile — closer role required |

### Verdict rule

- `cat_pressure × cat_reachability / 100` ranked across all 10:
  - Top 6 → **push**
  - Middle 2 → **maintain**
  - Bottom 2 → **evaluate punt** (confirm with `cat_punt_score > 60`; otherwise hold)

---

## Overall Recommendation

A single-line summary followed by three labeled lists.

> **Plan: push N, maintain M, punt P** (N + M + P = 10; target N ≥ 6)

- **Push (N cats)**: [list] — priority for waivers, streams, and optimized lineups
- **Maintain (M cats)**: [list] — lead is safe, don't overspend roster moves
- **Punt (P cats)**: [list] — concede and reallocate; bench slots freed for push cats

**Expected matchup result**: N–(10−N) win/loss/tie (with confidence ____)

---

## Downstream Routing Hints

The category-strategist, waiver-analyst, streaming-strategist, and lineup-optimizer all read this signal. Make their job easier with explicit routing hints:

### For `mlb-waiver-analyst`
- Priority-order cats to fill: [list, highest pressure × reachability first]
- Cats to de-prioritize: [list]
- Closer adds: yes/no (yes only if SV is push and `save_role_certainty` on waivers is ≥ 70)

### For `mlb-streaming-strategist`
- Stream aggressiveness: high/medium/low
  - "High" if ERA/WHIP are punted (volatile streamers OK)
  - "Medium" if K/QS are push but ERA/WHIP are maintain (selective streams)
  - "Low" if all four pitching cats are push (only safe streamers)
- Two-start ace targets: yes/no
- Punt-ERA-and-WHIP mode: yes/no

### For `mlb-lineup-optimizer`
- OBP weight bump: yes/no (yes if OBP is push and margin is thin)
- SB deprioritize: yes/no (yes if SB is punt)
- Power bias: yes/no (yes if HR is push and OBP is punt — rare)

### For `mlb-category-strategist`
- Already consumed (this skill feeds it). Pass the full per-cat table unchanged.

---

## Red-Team Findings

Use the `red_team_findings` block in the frontmatter for severity × likelihood scoring. In the body, provide any narrative context that doesn't fit the YAML.

- **Two-start pitcher watch**: [us: list / opp: list]
- **Closer instability watch**: [any rostered closer who is a blow-save risk]
- **Weather / schedule disruption risk**: [games at risk of PPD this week]
- **Min-threshold risk**: [cats at risk of forfeit via IP/PA minimum]

---

## Worked Example (Filled)

Here is what a complete signal file body looks like. This is the example from `SKILL.md` (Week 3 vs. Los Doyers) expanded into the full template.

### Current scores and volume

| Cat | Us | Opp | Margin | Our vol. | Opp vol. | Vol. edge |
|---|---|---|---|---|---|---|
| R | 28 | 31 | -3 | 26 games | 22 games | us |
| HR | 9 | 7 | +2 | 26 games | 22 games | us |
| RBI | 30 | 29 | +1 | 26 games | 22 games | us |
| SB | 4 | 6 | -2 | 26 games | 22 games | us |
| OBP | .342 (82 PA) | .336 (78 PA) | +.006 | ~110 PAs left | ~90 PAs left | us |
| K | 42 | 38 | +4 | 9 starts | 7 starts | us |
| ERA | 3.80 (21 IP) | 4.12 (19 IP) | -0.32 | ~50 IP left | ~40 IP left | us |
| WHIP | 1.18 (21 IP) | 1.25 (19 IP) | -0.07 | ~50 IP left | ~40 IP left | us |
| QS | 2 | 1 | +1 | 9 starts | 7 starts | us |
| SV | 3 | 5 | -2 | ~8 days | ~8 days | even |

### Per-cat signals

| Cat | Position | Pressure | Reachability | Punt Score | Verdict | Rationale |
|---|---|---|---|---|---|---|
| R | losing | 72 | 68 | 22 | push | Close deficit, volume edge |
| HR | winning | 48 | 70 | 18 | maintain | Safe lead, volume edge |
| RBI | winning (thin) | 65 | 55 | 30 | push | +1 lead is fragile |
| SB | losing | 55 | 40 | 58 | evaluate punt | No reliable speed on roster |
| OBP | winning (thin) | 70 | 60 | 25 | push | Ratio cat — small lead pushable |
| K | winning | 55 | 72 | 15 | push | Two-start edge |
| ERA | winning | 62 | 58 | 28 | push | Good starters, volume edge |
| WHIP | winning | 60 | 55 | 32 | maintain | Safer to coast |
| QS | winning | 78 | 82 | 10 | push hard | 9 vs. 7 starts, +1 lead |
| SV | losing | 38 | 32 | 72 | punt | Opp has two locked closers |

**Plan: push 6, maintain 2, punt 2.**

- **Push (6)**: R, RBI, OBP, K, ERA, QS
- **Maintain (2)**: HR, WHIP
- **Punt (2)**: SB, SV

Expected result: 6–4 win (confidence 0.72).
