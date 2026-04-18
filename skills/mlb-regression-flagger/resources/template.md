# MLB Regression Flagger Templates

Output templates for flagged players, per-player worksheets, and the signal file that gets written to `signals/YYYY-MM-DD-regression.md`.

## Table of Contents
- [Flagged Players Table (primary output)](#flagged-players-table)
- [Per-Player Worksheet — Hitter](#per-player-worksheet--hitter)
- [Per-Player Worksheet — Pitcher](#per-player-worksheet--pitcher)
- [Signal File Template](#signal-file-template)
- [User-Facing Summary Template](#user-facing-summary-template)

---

## Flagged Players Table

The primary deliverable. One row per player. Sort descending by `|regression_index|` so the most actionable names come first.

### Hitters

| Rank | Player | Team | PA | wOBA | xwOBA | Gap | regression_index | BABIP | Barrel% | Direction | Action |
|------|--------|------|----|------|-------|-----|------------------|-------|---------|-----------|--------|
| 1 | Junior Caminero | TB | 82 | .310 | .380 | +.070 | **+35** | .255 | 14.2% | UNLUCKY | **BUY** — aggressive |
| 2 | [name] | [team] | | | | | | | | | |
| 3 | [name] | [team] | | | | | | | | | |
| ... | | | | | | | | | | | |

### Pitchers

| Rank | Player | Team | IP | ERA | FIP | Gap | regression_index | HR/FB | LOB% | Direction | Action |
|------|--------|------|----|----|-----|-----|------------------|-------|------|-----------|--------|
| 1 | [name] | [team] | 38 | 2.50 | 4.20 | +1.70 | **-85** | 6.1% | 82% | LUCKY | **SELL** — aggressive |
| 2 | [name] | [team] | | | | | | | | | |
| ... | | | | | | | | | | | |

**Legend:**
- `Direction`: `UNLUCKY` (positive index, BUY) or `LUCKY` (negative index, SELL)
- `Action`: ends with a verb per CLAUDE.md rule #6 — `BUY`, `SELL`, `HOLD`, `ADD`, `DROP`, `WATCHLIST`
- **Bold** the `regression_index` when ≥ 30 (aggressive action threshold)

---

## Per-Player Worksheet — Hitter

Fill one per flagged hitter before emitting the row.

| Field | Value | Source URL |
|-------|-------|-----------|
| Player name | | |
| Team | | |
| Date of data | | |
| Plate Appearances (PA) | | |
| **wOBA** (surface) | | FanGraphs |
| **xwOBA** (expected) | | Baseball Savant |
| xwOBA - wOBA = gap | | (computed) |
| **regression_index** = gap × 500, clamped ±100 | | (computed) |
| BABIP | | FanGraphs |
| Barrel % | | Baseball Savant |
| Hard-Hit % | | Baseball Savant |
| Avg Exit Velocity | | Baseball Savant |
| Launch Angle | | Baseball Savant |

**Secondary flag check:**
- BABIP > .370? → lucky flag (reinforces negative index) [ ] Yes / [ ] No
- BABIP < .240? → unlucky flag (reinforces positive index) [ ] Yes / [ ] No
- Does Barrel % / Hard-Hit % confirm the direction? [ ] Confirms / [ ] Contradicts

**Sample-size check:**
- PA ≥ 80? [ ] Yes → proceed / [ ] No → emit `confidence: 0.3`, label `too-early`

**Confidence score (0.0–1.0):** _____
- Start at 0.70
- +0.10 if secondary flag confirms direction
- +0.05 if Barrel% is in top or bottom decile (supports thesis)
- -0.15 if secondary flag contradicts
- -0.20 if PA < 80
- -0.30 if either xwOBA or wOBA source could not be verified via web search

**Direction tag:** [ ] BUY / [ ] SELL / [ ] HOLD / [ ] WATCHLIST

**Recommended action verb:** `_____`

---

## Per-Player Worksheet — Pitcher

Fill one per flagged pitcher before emitting the row.

| Field | Value | Source URL |
|-------|-------|-----------|
| Player name | | |
| Team | | |
| Date of data | | |
| Innings Pitched (IP) | | |
| **ERA** (surface) | | FanGraphs |
| **FIP** (expected) | | FanGraphs |
| xFIP | | FanGraphs |
| xERA (Statcast) | | Baseball Savant |
| raw = (FIP - ERA) × 50 | | (computed) |
| **regression_index** = clamp(-raw, -100, +100) | | (computed, note the negation) |
| HR/FB % | | FanGraphs |
| Career HR/FB % | | FanGraphs |
| LOB % (strand rate) | | FanGraphs |
| Whiff % | | Baseball Savant |

**Sign-convention reminder:** FIP higher than ERA → pitcher has been LUCKY (SELL). We negate raw to get the signed index: `regression_index = -raw`.

**Secondary flag check:**
- HR/FB < 8%? → lucky flag (SELL reinforcement) [ ] Yes / [ ] No
- HR/FB > 17%? → unlucky flag (BUY reinforcement) [ ] Yes / [ ] No
- LOB% > 80%? → strand-rate luck (SELL reinforcement) [ ] Yes / [ ] No
- LOB% < 68%? → strand-rate unluck (BUY reinforcement) [ ] Yes / [ ] No

**Sample-size check:**
- IP ≥ 30? [ ] Yes → proceed / [ ] No → emit `confidence: 0.3`, label `too-early`

**Confidence score (0.0–1.0):** _____
- Start at 0.70
- +0.10 if HR/FB secondary flag confirms
- +0.05 if LOB% secondary flag confirms
- -0.15 if HR/FB contradicts
- -0.20 if IP < 30
- -0.30 if source verification fails

**Direction tag:** [ ] BUY / [ ] SELL / [ ] HOLD / [ ] WATCHLIST

**Recommended action verb:** `_____`

---

## Signal File Template

Write to `signals/YYYY-MM-DD-regression.md`. Frontmatter is authoritative per `signal-framework.md`.

```markdown
---
type: regression
date: 2026-04-17
emitted_by: mlb-regression-flagger
variant_synthesis: true
variants_fired: [advocate, critic]
synthesis_confidence: 0.78
red_team_findings:
  - severity: 2
    likelihood: 2
    score: 4
    note: "Caminero's BABIP may stay low if teams continue shifting against him"
    mitigation: "Re-check after 30 more PAs"
source_urls:
  - https://baseballsavant.mlb.com/savant-player/junior-caminero-676391
  - https://www.fangraphs.com/players/junior-caminero/27479
players:
  - name: Junior Caminero
    team: TB
    pa: 82
    woba: 0.310
    xwoba: 0.380
    babip: 0.255
    barrel_pct: 14.2
    regression_index: 35
    direction: BUY
    confidence: 0.78
  - name: [second hitter]
    ...
  - name: [pitcher name]
    ip: 38
    era: 2.50
    fip: 4.20
    hr_fb: 6.1
    lob_pct: 82
    regression_index: -85
    direction: SELL
    confidence: 0.82
---

# Regression candidates — 2026-04-17

## Hitters flagged

### BUY (positive regression_index, unlucky)

| Player | Team | PA | wOBA | xwOBA | Index | Action |
|--------|------|----|----|-------|-------|--------|
| Junior Caminero | TB | 82 | .310 | .380 | +35 | BUY |

### SELL (negative regression_index, lucky)

| Player | Team | PA | wOBA | xwOBA | Index | Action |
|--------|------|----|----|-------|-------|--------|
| [name] | [team] | | | | | SELL |

## Pitchers flagged

### BUY

| Player | Team | IP | ERA | FIP | Index | Action |
|--------|------|----|----|-----|-------|--------|
| [name] | [team] | | | | | BUY |

### SELL

| Player | Team | IP | ERA | FIP | Index | Action |
|--------|------|----|----|-----|-------|--------|
| [name] | [team] | | | | | SELL |
```

---

## User-Facing Summary Template

The user has zero baseball knowledge (per CLAUDE.md). Every stat abbreviation must be translated inline on first use, and every recommendation must end with a verb.

```markdown
## Who you should target or move — 2026-04-17

### BUY LOW — their stats will probably get better

**1. Junior Caminero (Tampa Bay Rays)**
Caminero's raw hitting numbers look mediocre right now (wOBA of .310 — that's a single
catch-all hitting stat where .320 is league average). But the quality of his actual
contact — how hard and at what angle he's hitting the ball — suggests his numbers
should be .380, one of the best in baseball. His current BABIP (batting average on
balls in play) is .255, unusually low — meaning line drives are finding gloves.
This is bad luck; expect correction within ~30 days.
→ **ACTION**: ADD if on waivers (bid $15 FAAB). If owned by a rival, OFFER a trade
  for him now, before his numbers catch up and his price goes up.

### SELL HIGH — their stats will probably get worse

**1. [Pitcher Name] (Team)**
Currently posting a 2.50 ERA (earned runs per 9 innings — lower is better). But the
defense-independent metric FIP — which strips out luck — says he should be at 4.20.
His strand rate (percentage of runners he prevents from scoring) is 82%, well above
the sustainable 72%. Home runs allowed are suppressed at 6% of fly balls (normal is
~12%). All three luck metrics point to regression.
→ **ACTION**: OFFER him in a trade this week. Target a BUY-LOW hitter in return.
```

**Formatting rules for user-facing output:**
- Lead with the verb headline ("BUY LOW" / "SELL HIGH")
- Always translate the stat abbreviation the first time it appears
- End every player section with a bolded `**ACTION**:` line that uses an imperative verb
- Sort within each bucket by `|regression_index|` descending (most extreme first)
