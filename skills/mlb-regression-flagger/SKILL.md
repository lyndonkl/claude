---
name: mlb-regression-flagger
description: Identifies fantasy baseball players whose surface stats (wOBA, ERA, batting average) are diverging from their underlying Statcast quality (xwOBA, FIP, xBA) — emits a `regression_index` from -100 (very lucky, sell high) to +100 (very unlucky, buy low). Primary signal for buy-low/sell-high decisions on trades and waivers. Use when user mentions "buy low", "sell high", "regression candidate", "lucky", "unlucky", "xwOBA gap", "ERA-FIP gap", "BABIP", "due for regression", or is deciding whether to trade for / trade away a player based on over- or under-performance.
---
# MLB Regression Flagger

## Table of Contents
- [Example](#example)
- [Workflow](#workflow)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Example

**Scenario**: User asks "Is Junior Caminero a buy-low candidate or am I chasing noise?"

**Raw data gathered from Baseball Savant + FanGraphs (cite URLs)**:
- Caminero 2026 wOBA: .310 (actual results)
- Caminero 2026 xwOBA: .380 (expected based on exit velocity + launch angle)
- BABIP: .255 (well below .300 league mean)
- Barrel %: 14.2% (elite, 90th percentile)
- Hard-Hit %: 52% (elite)

**Regression index calculation**:
```
regression_index = (xwOBA - wOBA) x 500
                 = (.380 - .310) x 500
                 = +35
```

**Secondary check — BABIP**: .255 is below the .240 lower-outlier threshold for hitters only if we tighten further, but .255 plus elite contact quality confirms unlucky. Not a "will correct to .300" player, but unlikely to stay at .255 given the batted-ball profile.

**Verdict**: `regression_index = +35` → **BUY**. Caminero has been unlucky; underlying contact quality is elite. Expect his surface stats to catch up over the next 30 days.

**User-facing translation** (per CLAUDE.md rule #5 — beginner writing):
> "Junior Caminero's raw numbers look mediocre (.310 wOBA — that's a catch-all hitting stat), but the quality of his actual contact (how hard and at what angle he hits the ball) suggests he should be hitting .380. The gap is one of the biggest in the league. ADD if available, or OFFER a trade for him before his stats correct."

**Signal file emission** (per signal-framework.md):
```yaml
---
type: regression
date: 2026-04-17
emitted_by: mlb-regression-flagger
player: Junior Caminero
regression_index: +35
direction: BUY
confidence: 0.78
source_urls:
  - https://baseballsavant.mlb.com/savant-player/junior-caminero-...
  - https://www.fangraphs.com/players/junior-caminero/...
---
```

## Workflow

Copy this checklist and track progress:

```
Regression Flagger Progress:
- [ ] Step 1: Define the candidate list (who to check)
- [ ] Step 2: Web-search Savant for expected stats (xwOBA, xERA, xBA)
- [ ] Step 3: Web-search FanGraphs for surface stats (wOBA, ERA, BABIP, HR/FB)
- [ ] Step 4: Compute regression_index per player
- [ ] Step 5: Apply secondary flags (BABIP, HR/FB)
- [ ] Step 6: Emit signal file + user-facing translation
```

**Step 1: Define the candidate list**

Who are we checking? Three entry points:
- [ ] User's current roster (for SELL candidates — anyone overperforming)
- [ ] Free agents + waiver wire (for BUY candidates — anyone underperforming with elite underlying metrics)
- [ ] Specific player asked about (e.g., trade target)

**Step 2: Web-search Baseball Savant for expected stats**

See [resources/methodology.md](resources/methodology.md#how-to-web-search-savant) for exact queries and URL patterns.

- [ ] Hitters: `xwOBA`, `xBA`, `xSLG`, Barrel %, Hard-Hit %
- [ ] Pitchers: `xERA`, Expected Batting Average against, Whiff %, Chase %
- [ ] Record each URL in `source_urls` for the signal file

**Step 3: Web-search FanGraphs for surface stats**

See [resources/methodology.md](resources/methodology.md#how-to-web-search-fangraphs) for query patterns.

- [ ] Hitters: `wOBA`, `BABIP`, AVG, OBP, SLG
- [ ] Pitchers: `ERA`, `FIP`, `xFIP`, HR/FB %, LOB %
- [ ] Record each URL

**Step 4: Compute regression_index**

See [resources/methodology.md](resources/methodology.md#formulas) for the formulas.

- [ ] Hitter: `regression_index = (xwOBA - wOBA) x 500`, clamped to ±100
- [ ] Pitcher: `regression_index = (FIP - ERA) x 50`, clamped to ±100
  - Note: for pitchers, a LARGER (more positive) FIP than ERA = pitcher has been lucky (negative signal for fantasy); a SMALLER FIP than ERA = pitcher has been unlucky (positive signal). See methodology for sign convention.
- [ ] Populate [resources/template.md](resources/template.md#flagged-players-table) with the result

**Step 5: Apply secondary flags**

- [ ] Hitter BABIP check: flag if > .370 (unsustainably lucky) or < .240 (unsustainably unlucky)
- [ ] Pitcher HR/FB check: flag if > 17% (unlucky, normalizes to ~12%) or < 8% (lucky)
- [ ] Note: secondary flags reinforce or contradict the primary `regression_index`. When they agree, confidence goes up; when they disagree, confidence drops and the player goes into a "watchlist" bucket instead of an actionable BUY/SELL.

**Step 6: Emit signal file + user-facing translation**

- [ ] Write `signals/YYYY-MM-DD-regression.md` with frontmatter per signal-framework.md
- [ ] Translate every stat to plain English for the user (per CLAUDE.md rule #5)
- [ ] End every recommendation with an action verb: `BUY` / `SELL` / `HOLD` / `ADD` / `DROP` (per CLAUDE.md rule #6)
- [ ] Validate against [resources/evaluators/rubric_mlb_regression_flagger.json](resources/evaluators/rubric_mlb_regression_flagger.json). Target average ≥ 3.5.

## Common Patterns

**Pattern 1: The Elite-Contact, Bad-Luck Hitter (classic BUY)**
- **Signals**: xwOBA - wOBA ≥ +.050, Barrel % ≥ 90th percentile, BABIP ≤ .260
- **Typical profile**: Young hitter with elite exit velocity whose line drives are finding gloves
- **Action**: Aggressive BUY. Offer a trade for them before the market catches on. Bid FAAB if they are on waivers.
- **Example**: Junior Caminero — xwOBA .380 vs wOBA .310, BABIP .255 → `+35`, BUY.

**Pattern 2: The Lucky Journeyman (classic SELL)**
- **Signals**: wOBA - xwOBA ≥ +.050, Barrel % below median, BABIP ≥ .360
- **Typical profile**: Career-average hitter riding a hot streak on soft contact
- **Action**: SELL high. Try to trade them for a BUY-LOW target of real talent.
- **Example** (hypothetical): Utility IF hitting .310 with a .360 BABIP and xwOBA .295 vs wOBA .340 → `-22`, SELL.

**Pattern 3: The Pitcher-Lucky Starter (SELL)**
- **Signals**: ERA much lower than FIP (e.g., 2.50 ERA, 4.20 FIP), HR/FB < 8%, strand rate (LOB%) > 80%
- **Typical profile**: Starter whose fly balls aren't leaving the park and whose inherited runners aren't scoring
- **Action**: SELL while his ERA still looks shiny.
- **Regression_index example**: `(FIP - ERA) x 50 = (4.20 - 2.50) x 50 = +85`. But for pitchers a large FIP-ERA gap means he has been LUCKY → flip sign → `-85`, SELL. See methodology for sign convention.

**Pattern 4: The Pitcher-Unlucky Starter (BUY)**
- **Signals**: ERA well above FIP (e.g., 5.10 ERA, 3.40 FIP), HR/FB > 17%, LOB% < 68%
- **Typical profile**: Good stuff, bad sequencing / BABIP luck
- **Action**: BUY before the ERA corrects.

**Pattern 5: Conflicting Signals (WATCHLIST, not actionable)**
- **Signals**: xwOBA-wOBA gap is large but Barrel % is below median, OR BABIP is extreme but contact quality confirms it
- **Action**: Do NOT auto-flag BUY/SELL. Emit `regression_index` with reduced confidence (< 0.5) and place on watchlist for another week.

## Guardrails

1. **Sample-size minimum**: Do not emit a `regression_index` for a hitter with fewer than 80 PAs or a pitcher with fewer than 30 IP. Statcast expected stats are noisy below that. If below threshold, emit `confidence: 0.3` and label `too-early`.

2. **Sign convention for pitchers**: `(FIP - ERA) x 50` gives a raw number. A POSITIVE raw number means ERA < FIP → the pitcher has been LUCKY → negate to produce a NEGATIVE `regression_index` (SELL signal). A NEGATIVE raw number means ERA > FIP → UNLUCKY → negate to POSITIVE (BUY). Always negate. See methodology for the worked example. Hitters use the raw sign directly.

3. **Clamp to ±100**: Extreme xwOBA gaps (>.200) are almost always small-sample artifacts. Clamp hard. Do not report `regression_index` of +140.

4. **Park and platoon adjustments**: xwOBA from Savant is park-neutral but does not adjust for platoon splits. For a LHH playing in a tough-for-lefties park (e.g., Oracle) with many LHP starts ahead, the regression may be slower than the index suggests. Note as a caveat; do not recompute.

5. **BABIP is secondary, not primary**: A high BABIP alone is not a SELL signal if underlying contact quality is elite. Hitters with extreme exit velocity (e.g., Judge, Ohtani) sustain BABIPs above .340 for full seasons. Always cross-check BABIP against Hard-Hit % before flagging.

6. **HR/FB normalization for pitchers**: League-average HR/FB is ~12%. Pitchers regress toward their career HR/FB, not league average. A flyball pitcher's "normal" HR/FB is 14%; a groundball pitcher's is 9%. Use career or 3-year average when available; fall back to 12% only if no history.

7. **Web-search every fact (per CLAUDE.md)**: Every number that enters the formula must come from a live web search with the URL recorded in `source_urls:`. Never fill in from memory or training data. If a search fails, degrade to `confidence: 0.3` and flag in the red-team pass.

8. **Translate for the beginner**: The user has zero baseball knowledge. Every user-facing sentence that uses "xwOBA", "FIP", "BABIP" must include an inline translation on first use. See CLAUDE.md rule #5 and the [Example](#example) above.

## Quick Reference

**Core formulas:**

```
HITTER:  regression_index = clamp((xwOBA - wOBA) x 500, -100, +100)
         positive = UNLUCKY (BUY); negative = LUCKY (SELL)

PITCHER: raw = (FIP - ERA) x 50
         regression_index = clamp(-raw, -100, +100)
         positive = UNLUCKY (BUY); negative = LUCKY (SELL)

SECONDARY (hitter):  BABIP > .370 → lucky flag; BABIP < .240 → unlucky flag
SECONDARY (pitcher): HR/FB < 8% → lucky flag; HR/FB > 17% → unlucky flag
```

**Action thresholds:**

| `regression_index` | Direction | Fantasy action |
|---|---|---|
| ≥ +30 | Very unlucky | Aggressive BUY / ADD / high FAAB bid |
| +15 to +29 | Mildly unlucky | BUY if available cheaply |
| -14 to +14 | Noise | HOLD / no action |
| -29 to -15 | Mildly lucky | SELL if offered market-rate |
| ≤ -30 | Very lucky | Aggressive SELL / DROP / decline offers |

**Data source map (per data-sources.md):**

| Stat | Primary source | URL pattern |
|---|---|---|
| xwOBA, xBA, xSLG, Barrel %, Hard-Hit % | Baseball Savant | https://baseballsavant.mlb.com/savant-player/{slug}-{id} |
| wOBA, BABIP (hitter) | FanGraphs | https://www.fangraphs.com/players/{slug}/{id} |
| ERA, FIP, xFIP, HR/FB, LOB% | FanGraphs | same |
| xERA | Baseball Savant | same |

**Key resources:**

- **[resources/template.md](resources/template.md)**: Flagged-players table, per-player worksheet, signal file template
- **[resources/methodology.md](resources/methodology.md)**: Formulas with sign conventions, web-search query patterns, worked examples, BABIP & HR/FB normalization
- **[resources/evaluators/rubric_mlb_regression_flagger.json](resources/evaluators/rubric_mlb_regression_flagger.json)**: 8-criterion scoring rubric

**Inputs required:**

- Player name(s) or "scan roster" / "scan waivers"
- League context: weeks remaining, category needs (from `context/league-config.md` and `mlb-category-state-analyzer` signals)

**Outputs produced:**

- `regression_index` per player (-100 to +100)
- Direction tag: `BUY` / `SELL` / `HOLD` / `WATCHLIST`
- Secondary flag notes (BABIP, HR/FB)
- Signal file at `signals/YYYY-MM-DD-regression.md`
- User-facing summary with inline jargon translations and an action verb
