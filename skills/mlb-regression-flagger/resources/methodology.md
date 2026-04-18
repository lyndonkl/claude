# MLB Regression Flagger Methodology

Formulas, sign conventions, web-search patterns, worked examples, and edge-case handling for computing `regression_index`.

## Table of Contents
- [Conceptual background](#conceptual-background)
- [Formulas](#formulas)
  - [Hitters](#hitters)
  - [Pitchers](#pitchers)
  - [Sign convention (critical)](#sign-convention-critical)
- [Secondary flags](#secondary-flags)
  - [BABIP (hitter)](#babip-hitter)
  - [HR/FB (pitcher)](#hrfb-pitcher)
  - [LOB% (pitcher, tertiary)](#lob-pitcher-tertiary)
- [How to web-search Baseball Savant](#how-to-web-search-savant)
- [How to web-search FanGraphs](#how-to-web-search-fangraphs)
- [Worked examples](#worked-examples)
- [Sample-size guardrails](#sample-size-guardrails)
- [Confidence scoring](#confidence-scoring)
- [Edge cases](#edge-cases)

---

## Conceptual background

Surface baseball stats (wOBA for hitters, ERA for pitchers) are a mixture of **skill** and **luck** — specifically, the sequencing of events (who was on base when the ball was hit) and the placement of batted balls (did the line drive find a glove or a gap). Over a full season, luck averages out, but over 1–2 months, the gap between surface stats and underlying quality can be enormous.

Statcast (Baseball Savant) and defense-independent pitching stats (FanGraphs) measure the **quality** of the inputs — how hard the ball was hit, at what angle, how often the pitcher misses bats, how many walks/strikeouts/homers they allow — stripped of sequencing luck.

When surface and underlying diverge by a lot, the surface will tend to **regress** toward the underlying over the next 4–8 weeks. That is the edge this skill exploits: identify the player whose surface stats are mispricing their true talent, and BUY or SELL in the fantasy market before the correction happens.

---

## Formulas

### Hitters

Primary formula (per signal-framework.md):

```
regression_index_hitter = clamp((xwOBA - wOBA) × 500, -100, +100)
```

Where:
- `wOBA` = weighted on-base average (from FanGraphs). Single composite hitting stat; .320 is league average.
- `xwOBA` = expected wOBA (from Baseball Savant). What the hitter's wOBA would be if batted balls landed with league-average outcomes given their exit velocity and launch angle.
- The factor **500** normalizes the typical range of xwOBA-wOBA gaps (roughly ±.060) onto a ±30 scale, with extreme gaps hitting the ±100 cap.

**Interpretation:**
- Positive index → actual wOBA is BELOW expected → hitter has been **unlucky** → **BUY**
- Negative index → actual wOBA is ABOVE expected → hitter has been **lucky** → **SELL**

**Why × 500 (derivation):** An xwOBA-wOBA gap of +.060 is the ~85th percentile of mid-season gaps. `0.060 × 500 = 30`, which is the "aggressive action" threshold. Gaps of +.200 or more are implausible outside of small samples and are clamped.

### Pitchers

Primary formula:

```
raw = (FIP - ERA) × 50
regression_index_pitcher = clamp(-raw, -100, +100)
```

Where:
- `ERA` = earned run average (from FanGraphs). Surface run-prevention stat.
- `FIP` = fielding-independent pitching (from FanGraphs). Predicted ERA based only on K, BB, HR — stripped of defense and sequencing.
- The factor **50** normalizes typical ERA-FIP gaps (roughly ±1.50) onto a ±75 scale, with extremes clamped.

### Sign convention (critical)

This is the most common place to get the signal wrong. Read carefully.

**For HITTERS:** A positive raw gap `(xwOBA - wOBA) > 0` means the hitter is underperforming Statcast, i.e., **unlucky**, i.e., **BUY**. We keep the sign. `regression_index > 0 = BUY`.

**For PITCHERS:** A positive raw gap `(FIP - ERA) > 0` means FIP is HIGHER than ERA, meaning the pitcher's surface ERA is BETTER (lower) than what his peripherals predict. That is **LUCKY**. For fantasy purposes, we want `regression_index > 0` to consistently mean BUY (unlucky). So we **negate**:

```
regression_index_pitcher = -raw = -(FIP - ERA) × 50 = (ERA - FIP) × 50
```

Equivalent, easier-to-remember form:

```
regression_index_pitcher = clamp((ERA - FIP) × 50, -100, +100)
```

**Convention table (memorize):**

| Player type | Formula | Sign of index when player is... |
|---|---|---|
| Hitter | (xwOBA - wOBA) × 500 | unlucky → `+` (BUY); lucky → `-` (SELL) |
| Pitcher | (ERA - FIP) × 50 | unlucky → `+` (BUY); lucky → `-` (SELL) |

Both formulas produce `+` for BUY and `-` for SELL. Always.

---

## Secondary flags

Secondary flags are **confirmers**, not independent signals. They reinforce or contradict the primary `regression_index`. Use them to adjust confidence, not to override the primary computation.

### BABIP (hitter)

`BABIP` = batting average on balls in play (from FanGraphs). League-average hitter BABIP is ~.300.

| BABIP | Flag | Interpretation |
|---|---|---|
| > .370 | LUCKY (sell-side confirmer) | Unsustainable unless contact quality is truly elite (Judge, Ohtani tier). Cross-check Barrel % — if below 90th percentile, SELL signal is valid. |
| .300 – .370 | (no flag) | Within normal variance. |
| .240 – .300 | (no flag) | Within normal variance. |
| < .240 | UNLUCKY (buy-side confirmer) | Balls are finding gloves. If contact quality (Barrel %, Hard-Hit %) is average or better, BUY signal is valid. |

**Elite-contact exception:** Hitters in the top decile of Barrel % (≥15%) can sustain BABIP > .340 for full seasons. Do NOT auto-flag them as "lucky" just from BABIP. The `regression_index` from xwOBA-wOBA already accounts for contact quality; if it says HOLD but BABIP is .365, trust the primary.

### HR/FB (pitcher)

`HR/FB` = home runs allowed as a percentage of fly balls (from FanGraphs). League-average is ~12%. Pitchers regress toward their career HR/FB, not league average.

| HR/FB | Flag | Interpretation |
|---|---|---|
| < 8% | LUCKY (sell-side confirmer) | Flyballs aren't leaving the park. Normalize toward career average. |
| 8% – 17% | (no flag) | Within normal variance. |
| > 17% | UNLUCKY (buy-side confirmer) | Hanging pitches finding seats, or park/weather variance. |

**Groundball/flyball adjustment:**
- Extreme flyball pitcher (>45% FB rate): "normal" HR/FB is ~14%. Use 14% as reference instead of 12%.
- Extreme groundball pitcher (>55% GB rate): "normal" HR/FB is ~9%. Use 9% as reference.

Pull career HR/FB from FanGraphs player page if the pitcher has 3+ seasons of MLB history. If rookie, fall back to 12%.

### LOB% (pitcher, tertiary)

`LOB%` = strand rate, the percentage of runners the pitcher prevents from scoring. League average is ~72%.

- LOB% > 80% → lucky sequencing (SELL confirmer)
- LOB% < 68% → unlucky sequencing (BUY confirmer)

Weight LOB% less than HR/FB — some pitchers (high-K relievers especially) can sustain 78%+ strand rates on skill.

---

## How to web-search Savant

Per `data-sources.md`, Baseball Savant is the primary source for all expected stats.

**Player page URL pattern:**
```
https://baseballsavant.mlb.com/savant-player/{slug}-{mlbam_id}
```

Example: `https://baseballsavant.mlb.com/savant-player/junior-caminero-676391`

**Search queries that work:**

| Goal | Query |
|---|---|
| Find a hitter's Savant page | `"Junior Caminero" baseball savant 2026` |
| Find xwOBA for a hitter | `"Junior Caminero" xwOBA 2026 season` |
| Find xERA for a pitcher | `"Zac Gallen" xERA 2026 baseball savant` |
| Find Barrel % | `"Junior Caminero" barrel percent 2026` |
| Leaderboard of biggest xwOBA-wOBA gaps | `baseball savant xwOBA wOBA difference leaderboard 2026` |

**What to extract from the player page:**
- xwOBA (headline number on the page)
- xBA, xSLG (expected batting average / slugging)
- Barrel %, Hard-Hit %, Avg Exit Velocity, Launch Angle
- For pitchers: xERA, Whiff %, Chase %

**If the page is paywalled or blocked:** Fall back to:
1. FanGraphs Statcast page: `https://www.fangraphs.com/leaders/statcast`
2. FanGraphs player page — the Statcast tab mirrors Savant data with ~1-day lag
3. If neither works, drop `confidence: 0.3` and flag `source verification failed` in red-team findings

### How to web-search FanGraphs

FanGraphs is the primary source for wOBA, BABIP, ERA, FIP, HR/FB, LOB%.

**Player page URL pattern:**
```
https://www.fangraphs.com/players/{slug}/{playerid}
```

**Search queries that work:**

| Goal | Query |
|---|---|
| Find a player's FanGraphs page | `"Junior Caminero" fangraphs 2026` |
| Find wOBA | `"Junior Caminero" wOBA 2026 fangraphs` |
| Find FIP for a pitcher | `"Zac Gallen" FIP 2026 fangraphs` |
| Find HR/FB | `"Zac Gallen" HR/FB 2026 fangraphs` |
| Find BABIP | `"Junior Caminero" BABIP 2026 fangraphs` |

**Leaderboard search (scan-mode):**
- `https://www.fangraphs.com/leaders/major-league` — filter by year, PA/IP minimum, sort by any stat
- `fangraphs leaderboard biggest ERA FIP gap 2026` returns the "Luck" page in many seasons

**Data extraction checklist:**

Hitter page (Standard + Advanced tabs):
- [ ] wOBA
- [ ] BABIP
- [ ] PA (for sample-size check)

Pitcher page:
- [ ] ERA
- [ ] FIP
- [ ] xFIP (for secondary cross-check)
- [ ] HR/FB
- [ ] LOB%
- [ ] IP (for sample-size check)

---

## Worked examples

### Example 1 — Junior Caminero (BUY the hitter)

**Web-search results (URLs recorded in signal file):**
- Savant: xwOBA .380, Barrel % 14.2%, Hard-Hit % 52%
- FanGraphs: wOBA .310, BABIP .255, PA 82

**Primary computation:**
```
regression_index = (xwOBA - wOBA) × 500
                 = (0.380 - 0.310) × 500
                 = 0.070 × 500
                 = +35  ✓ (within ±100, no clamp needed)
```

**Secondary flag check:**
- BABIP = .255 → below .240 threshold? No, but close. Mild BUY-side confirmer.
- Barrel % 14.2% is top-decile → contact quality confirms he SHOULD be hitting better.
- Secondary flags agree with primary. Confidence boost.

**Sample size:** PA = 82 → above 80 threshold. ✓

**Confidence calculation:**
- Base: 0.70
- Barrel % in top decile: +0.05
- BABIP directionally agrees: +0.05 (mild, not hard threshold-cross)
- PA ≥ 80: no adjustment
- Sources verified: no penalty
- **Final: 0.80**

**Output:**
- `regression_index`: +35
- Direction: BUY (aggressive — index ≥ 30)
- Action verb: **BUY** (or **ADD** if free agent, **OFFER TRADE** if rostered by rival)
- User-facing headline: "Junior Caminero — surface stats trailing true contact quality by the largest margin on your watchlist. ADD or trade for him now."

### Example 2 — Hypothetical lucky pitcher (SELL)

**Web-search results:**
- FanGraphs: ERA 2.50, FIP 4.20, HR/FB 6.1%, LOB% 82%, IP 38
- Savant: xERA 4.05

**Primary computation (pitcher — remember the sign convention):**
```
regression_index = (ERA - FIP) × 50
                 = (2.50 - 4.20) × 50
                 = -1.70 × 50
                 = -85  ✓ (within ±100)
```

Equivalent check via raw/negate form:
```
raw = (FIP - ERA) × 50 = (4.20 - 2.50) × 50 = +85
regression_index = -raw = -85  ✓
```

**Secondary flag check:**
- HR/FB 6.1% < 8% → LUCKY flag (SELL confirmer) ✓
- LOB% 82% > 80% → LUCKY flag (SELL confirmer) ✓
- Two independent luck markers confirm. High confidence.

**Sample size:** IP = 38 → above 30 threshold. ✓

**Confidence calculation:**
- Base: 0.70
- HR/FB confirmer: +0.10
- LOB% confirmer: +0.05
- IP ≥ 30: no adjustment
- **Final: 0.85**

**Output:**
- `regression_index`: -85
- Direction: SELL (aggressive — |index| ≥ 30)
- Action verb: **SELL** now
- User-facing: "This pitcher's 2.50 ERA is propped up by three independent luck indicators (home runs aren't leaving the park, he's stranding too many runners, and his peripherals say he should be at a 4.20 ERA). OFFER him in a trade this week."

### Example 3 — Small-sample hitter (TOO EARLY)

**Web-search results:**
- Savant: xwOBA .400, Barrel % 18%
- FanGraphs: wOBA .280, BABIP .220, PA **42**

Even though the computed index would be `(0.400 - 0.280) × 500 = +60` (very unlucky, aggressive BUY), **PA = 42 is below the 80-PA threshold.**

**Action:** Do NOT emit `regression_index: +60`. Instead:
- Emit `regression_index: +60` with `confidence: 0.3` and label `too-early`
- Direction: **WATCHLIST**, not BUY
- Re-check in 2 weeks once PAs cross 80
- Do NOT recommend the user make a trade or spend FAAB on this signal alone

---

## Sample-size guardrails

Statcast expected stats are **noisy at low sample sizes**. Thresholds:

| Player type | Minimum | Below minimum action |
|---|---|---|
| Hitter | 80 PA | Emit index but cap confidence at 0.30, label `too-early`, route to WATCHLIST |
| Pitcher (SP) | 30 IP | Same as above |
| Pitcher (RP) | 20 IP | Same as above |

In the first 4 weeks of the season, virtually all players are below these thresholds. The skill's output will be mostly WATCHLIST until mid-May.

---

## Confidence scoring

Start at 0.70 and adjust:

| Factor | Adjustment |
|---|---|
| Secondary flag confirms direction (BABIP for hitter, HR/FB for pitcher) | +0.10 |
| Tertiary flag confirms (e.g., LOB% for pitcher, Hard-Hit % in top/bottom decile for hitter) | +0.05 |
| Secondary flag contradicts direction | -0.15 |
| Sample size below threshold | -0.20 (and cap at 0.30) |
| Source URL could not be verified via web search | -0.30 |
| Index is in clamped region (|raw| would exceed 100) | -0.10 (extreme values tend to be sample artifacts) |

Minimum confidence emitted: 0.20. If lower, do not emit a signal — log the failure and move on.

---

## Edge cases

**Case 1 — xwOBA and xERA disagree for a two-way player (Ohtani)**
Compute hitter index using hitter stats only; compute pitcher index using pitcher stats only. Emit two separate signal rows.

**Case 2 — Mid-season trade / park change**
Park factors influence wOBA but not xwOBA. A hitter traded from Oracle (pitcher-friendly for LHH) to Coors will see wOBA rise even if xwOBA is unchanged, because the actual outcomes will improve. This narrows the gap from park, not regression. Flag in red-team findings but do not recompute.

**Case 3 — Pitcher's xFIP contradicts FIP**
If FIP and xFIP diverge by more than 0.50 (xFIP being the HR-luck-neutralized version of FIP), note that the FIP itself may be partially luck-driven. Prefer xFIP-based computation:
```
regression_index_pitcher_alt = (ERA - xFIP) × 50
```
Use alt when FIP-xFIP gap > 0.50; flag the substitution in the signal file.

**Case 4 — Reliever with volatile ERA**
Relievers' ERAs can jump 3+ runs from a single bad outing. For relievers, prefer SIERA or xFIP over FIP; raise the IP threshold to 20 minimum. A `regression_index` for a reliever with 15 IP is essentially noise.

**Case 5 — Rookie with no career HR/FB**
Fall back to league average (12%) but lower confidence by 0.05 to reflect the missing prior.

**Case 6 — Conflicting primary and secondary**
Example: hitter has `regression_index = +40` (very unlucky) but BABIP is .380 (lucky flag). The xwOBA-wOBA gap is real but comes from something other than BABIP (e.g., a low HR total despite high Barrel %). Lower confidence to 0.50 and note the conflict in red-team findings. Do NOT auto-flip the direction — primary wins.

**Case 7 — Neither Savant nor FanGraphs reachable**
Degrade to `source_urls: []`, `confidence: 0.3`, and tell the user: "I couldn't reach Baseball Savant or FanGraphs to verify this — paste the Statcast page text from your browser and I'll compute the index."
