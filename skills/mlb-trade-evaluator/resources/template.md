# MLB Trade Evaluator Templates

Input schema, per-category delta tables, value/flex/playoff blocks, verdict block with rationale and counter. Fill every field. Empty fields flag the signal confidence as low.

## Table of Contents
- [Trade Offer Input](#trade-offer-input)
- [Player Projection Table (Rest-of-Season)](#player-projection-table-rest-of-season)
- [Per-Category Delta Table — Both Teams](#per-category-delta-table--both-teams)
- [Ratio Category Weighted Computation](#ratio-category-weighted-computation)
- [`cat_pressure` Weight Sheet](#cat_pressure-weight-sheet)
- [`trade_value_delta` Block](#trade_value_delta-block)
- [`positional_flex_delta` Block](#positional_flex_delta-block)
- [`playoff_impact` Block (July+)](#playoff_impact-block-july)
- [Verdict Block](#verdict-block)
- [Counter-Offer Construction](#counter-offer-construction)
- [Signal File Frontmatter](#signal-file-frontmatter)

---

## Trade Offer Input

| Field | Value |
|---|---|
| Evaluation date | YYYY-MM-DD |
| Initiating team (other side) | ____ |
| User's team | ⚾ K L's Boomers |
| Offer expires at | ____ |
| League standings position (us) | __ / 12 |
| Standings position (them) | __ / 12 |
| Are they a playoff-seed competitor? | yes / no |
| Days until trade deadline (Aug 6) | __ |
| Commissioner review likely? | yes / no |

**Players coming IN (to us):**

| Player | Position(s) | Team | IL? | Notes |
|---|---|---|---|---|
| | | | | |

**Players going OUT (to them):**

| Player | Position(s) | Team | IL? | Notes |
|---|---|---|---|---|
| | | | | |

---

## Player Projection Table (Rest-of-Season)

Source for every row must be cited (URL). Primary: FanGraphs ATC rest-of-season. Fallback: Depth Charts, Razzball.

**Hitters:**

| Player | Side | ROS PA | R | HR | RBI | SB | OBP | $ value | Source URL |
|---|---|---|---|---|---|---|---|---|---|
| (IN) | IN | | | | | | | | |
| (OUT) | OUT | | | | | | | | |

**Pitchers:**

| Player | Side | ROS IP | K | ERA | WHIP | QS | SV | $ value | Source URL |
|---|---|---|---|---|---|---|---|---|---|
| (IN) | IN | | | | | | | | |
| (OUT) | OUT | | | | | | | | |

**Totals:**

| Side | PA | R | HR | RBI | SB | IP | K | QS | SV | $ total |
|---|---|---|---|---|---|---|---|---|---|---|
| IN (ours after trade) | | | | | | | | | | |
| OUT (theirs after trade) | | | | | | | | | | |

---

## Per-Category Delta Table — Both Teams

This is the headline table the coach will show the user. Raw delta = IN minus OUT. Weighted delta = raw × pressure / 50.

| Cat | Our IN total | Our OUT total | Raw Δ (our side) | `cat_pressure` | Weighted Δ | Direction |
|---|---|---|---|---|---|---|
| R | | | | | | ▲ / ▼ / — |
| HR | | | | | | |
| RBI | | | | | | |
| SB | | | | | | |
| OBP | | | (see ratio table below) | | | |
| K | | | | | | |
| ERA | | | (see ratio table below) | | | |
| WHIP | | | (see ratio table below) | | | |
| QS | | | | | | |
| SV | | | | | | |
| **Sum** | | | | | **`trade_cat_delta` = ____** | |

**Mirror table — their perspective** (for red-team check; their gain should roughly mirror our loss):

| Cat | Their IN total | Their OUT total | Raw Δ (their side) | Their assumed pressure | Weighted Δ |
|---|---|---|---|---|---|
| R | | | | | |
| … | | | | | |

---

## Ratio Category Weighted Computation

Ratio cats (OBP, ERA, WHIP) require volume-weighted math. A simple arithmetic delta of averages is misleading.

### OBP

```
Incoming OBP (volume-weighted) = Σ(OBP_i × PA_i) / Σ(PA_i)   over IN hitters
Outgoing OBP (volume-weighted) = Σ(OBP_j × PA_j) / Σ(PA_j)   over OUT hitters

Team-level delta =
  (Σ_IN PA × Incoming_OBP + team_remaining_PA × team_avg_OBP) / (Σ_IN PA + team_remaining_PA)
  − (current projected team OBP)
```

| IN hitter | PA | OBP | PA × OBP |
|---|---|---|---|
| | | | |
| Sum | ___ | (weighted avg) ___ | ___ |

| OUT hitter | PA | OBP | PA × OBP |
|---|---|---|---|
| | | | |
| Sum | ___ | (weighted avg) ___ | ___ |

**Projected team OBP shift (delta)**: ____ (e.g., +.003 = slight gain; −.008 = real loss)

### ERA

```
Incoming ERA (volume-weighted) = 9 × Σ(ER_i) / Σ(IP_i)   where ER_i = ERA_i × IP_i / 9
Outgoing ERA (volume-weighted) = same formula for OUT

Team-level delta: lower ERA is better, so a negative delta is a gain.
```

| IN pitcher | IP | ERA | Implied ER = ERA × IP / 9 |
|---|---|---|---|
| | | | |
| Sum | ___ | (weighted avg) ___ | ___ |

| OUT pitcher | IP | ERA | Implied ER |
|---|---|---|---|
| | | | |
| Sum | ___ | (weighted avg) ___ | ___ |

**Projected team ERA shift (delta)**: ____ (note sign convention — negative = good)

### WHIP

Same pattern as ERA, with (BB + H) substituted for ER and no factor of 9.

```
Implied baserunners_i = WHIP_i × IP_i
Incoming WHIP = Σ(baserunners_i) / Σ(IP_i)
```

| IN pitcher | IP | WHIP | Baserunners |
|---|---|---|---|
| | | | |

**Projected team WHIP shift (delta)**: ____

---

## `cat_pressure` Weight Sheet

Pull from the most recent `signals/YYYY-MM-DD-cat-state.md`. If unavailable, run `mlb-category-state-analyzer` first. Do NOT use uniform weights — that's the default failure mode.

| Cat | `cat_position` (winning/tied/losing) | `cat_pressure` (0-100) | Weight (= pressure/50) |
|---|---|---|---|
| R | | | |
| HR | | | |
| RBI | | | |
| SB | | | |
| OBP | | | |
| K | | | |
| ERA | | | |
| WHIP | | | |
| QS | | | |
| SV | | | |

**Source signal file**: `signals/YYYY-MM-DD-cat-state.md`

---

## `trade_value_delta` Block

Uses FanGraphs Auction Calculator rest-of-season dollar values. Fallback: Razzball Player Rater.

| Player | Side | $ value | Source |
|---|---|---|---|
| (IN 1) | IN | +$ | |
| (IN 2) | IN | +$ | |
| (OUT 1) | OUT | −$ | |
| (OUT 2) | OUT | −$ | |
| **Net** | | **$ _____** | |

```
trade_value_delta = Σ $_IN − Σ $_OUT = $ _____
```

**Bucket:**
- ≥ +$5 → real value gain
- −$5 to +$5 → noise (close to fair)
- ≤ −$5 → real value loss → bias to REJECT

---

## `positional_flex_delta` Block

Score from −100 (much worse flex) to +100 (much better). Neutral = 0.

| Factor | Our roster before | Our roster after | Score impact |
|---|---|---|---|
| SS depth (scarce) | __ players eligible | __ | ±__ |
| C depth (scarce) | __ | __ | ±__ |
| 2B depth (moderate scarcity) | __ | __ | ±__ |
| OF depth (abundant) | __ | __ | ±__ |
| SP count vs 3 slot + 5 flex | __ | __ | ±__ |
| RP / closer count vs 2 slot + 5 flex | __ | __ | ±__ |
| Multi-position (2+) eligibility gained/lost | | | ±__ |
| Bench flexibility change | | | ±__ |
| **Total `positional_flex_delta`** | | | **____** |

**Scoring anchors:**
- Gaining a starter at a scarce slot from a surplus slot: +30
- Losing a starter at a scarce slot to a surplus slot: −30
- Gaining 2B/SS/OF multi-eligibility: +15
- Consolidating 2 bench into 1 starter (free a bench slot): +10
- Creating an orphaned IL slot: −10

---

## `playoff_impact` Block (July+)

**Only populate if evaluation date ≥ July 1, 2026.** Before that, write N/A and drop to 50 (neutral).

Source: `mlb-playoff-scheduler` signal file, or FanGraphs team schedules. Championship weeks are 21, 22, 23 (ends Sun Sep 6).

| Player | Side | Games in W21 | W22 | W23 | Total | Avg matchup_quality (0-100) | Contribution |
|---|---|---|---|---|---|---|---|
| (IN) | IN | | | | | | +___ |
| (OUT) | OUT | | | | | | −___ |

```
playoff_impact = Σ(games × matchup_q) of IN − Σ(games × matchup_q) of OUT
              normalized to 0-100 with 50 = neutral
```

**Bucket:**
- ≥ 55 → trade improves playoff position
- 45-55 → playoff-neutral
- ≤ 40 → playoff-harmful (REJECT trigger if evaluation is July 15+)

---

## Verdict Block

The headline the coach relays to the user. End every verdict with a single verb: `ACCEPT`, `COUNTER (with specific package)`, or `REJECT`.

### Summary signal values

| Signal | Value |
|---|---|
| `trade_cat_delta` (weighted sum across 10 cats) | |
| `trade_value_delta` ($) | |
| `positional_flex_delta` (−100 to +100) | |
| `playoff_impact` (0-100; N/A if pre-July) | |
| Confidence (0.0-1.0) | |

### Decision logic applied

- [ ] Weighted cat delta > +30? ____
- [ ] Value delta ≥ +$5? ____
- [ ] No cat with pressure ≥80 has negative delta? ____
- [ ] Flex delta ≥ 0? ____
- [ ] Playoff impact ≥ 50 (if applicable)? ____

**All boxes checked** → ACCEPT.
**Some positive, some negative, close to fair value (−$5 ≤ value ≤ +$10)** → COUNTER.
**Any high-pressure cat negative, OR value ≤ −$5** → REJECT.

### Verdict

**VERDICT: _____ [ACCEPT / COUNTER / REJECT]**

**Why (1-2 sentences, beginner-voice, jargon translated inline):**

________________________________________________

**Category impact in plain English:**

- "We gain about __ HR (home runs) and __ RBI (runs batted in) — but lose __ SB (stolen bases) and __ QS (quality starts, a good pitching start of 6+ innings and 3 or fewer earned runs)."
- "The cats we care most about right now are __ and __ (because we're losing them this week)."

**Positional impact in plain English:**

________________________________________________

**Playoff impact in plain English (July+):**

________________________________________________

---

## Counter-Offer Construction

Only populate if VERDICT = COUNTER. A vague counter is useless — propose a **specific package**.

### Target the gap

| What our offer lacks | What to ask them to add/swap |
|---|---|
| Too few Ks (need ≥ __ more) | Ask them to swap their [Player] for [Player with high K projection] |
| Too little SB | Ask for [fast player] as a throw-in |
| $ value short by $__ | Ask them to upgrade OUR side by one tier |

### Specific counter package

**Counter offer:**

Our side: ____________ + ____________
Their side: ____________ + ____________

**Why they might accept**: ________________________________________________

**If they refuse the counter**: REJECT (default).

---

## Signal File Frontmatter

Every evaluation writes a signal file to `signals/YYYY-MM-DD-trade-<opponent-slug>.md`.

```yaml
---
type: trade
date: 2026-04-17
emitted_by: mlb-trade-evaluator
variant_synthesis: true
variants_fired: [advocate, critic]
synthesis_confidence: 0.72
opponent_team: "Los Doyers"
players_in: ["Aaron Judge"]
players_out: ["Bobby Witt Jr.", "Spencer Strider"]
trade_cat_delta:
  R: +2.3
  HR: +4.4
  RBI: +5.9
  SB: -21.3
  OBP: +3.0
  K: -115.5
  ERA: 0.0
  WHIP: 0.0
  QS: -96.0
  SV: 0.0
trade_value_delta: -24
positional_flex_delta: -30
playoff_impact: 35
verdict: reject
confidence: 0.78
counter_offer_if_applicable: null
red_team_findings:
  - severity: 3
    likelihood: 4
    score: 12
    note: "FanGraphs ATC may not yet reflect Strider's recent velocity drop"
    mitigation: "Check Baseball Savant velocity trend before final call"
source_urls:
  - https://www.fangraphs.com/projections.aspx?type=atc&pos=...
  - https://www.fangraphs.com/auction-calculator
  - https://baseballsavant.mlb.com/savant-player/spencer-strider-...
  - https://www.rotowire.com/baseball/injury-report.php
---
```

---

## User-Facing Output (what the coach reads out loud)

A 5-line block the `mlb-fantasy-coach` can deliver verbatim. No jargon without inline translation.

```
TRADE FROM [opponent team]:
  Out: [our players] → In: [their players]

Our take:
  • Value: [+/−$X] — [sentence]
  • Cats we care about: [gain/lose on each]
  • Position: [gain/lose depth at __]
  • Playoff weeks: [helps/hurts/neutral]

RECOMMENDATION: [ACCEPT / COUNTER / REJECT]
[If COUNTER: specific counter package in one sentence.]
```
