# Methodology -- MLB Two-Start Scout

Step-by-step procedures for building the two-start pitcher board. Every procedure is grounded in a web-search recipe (per CLAUDE.md operating rule #1: no API, web-search everything, cite URLs).

---

## Week definition

Yahoo fantasy weeks run **Monday 09:00 America/New_York through Sunday 23:59 America/New_York**. The lineup locks Monday at 09:00 ET -- adds after that point still take effect but cannot be started Monday.

Steps:
1. Determine the Monday of the upcoming fantasy week (the skill usually runs Sunday night for the following Monday).
2. Record `week_start = YYYY-MM-DD` (Monday) and `week_end = YYYY-MM-DD` (Sunday) in the signal frontmatter.
3. If the skill runs mid-week, use the CURRENT fantasy week (the Monday that has already passed). Note in `red_team_findings` that one or more starts may already be in the books.

Edge cases:
- **First Monday of the season**: handle the shorter partial week at the start.
- **All-Star Break week**: 2-start counts are compressed; verify both starts land in the same fantasy week on either side of the break.
- **Double-headers**: if a team plays a double-header, one pitcher may pitch twice in a single day (rare but possible). Treat as a normal two-start if both games are on the schedule.

---

## Primary web-search recipe: FantasyPros two-start pitchers

**URL (primary, per data-sources.md):** https://www.fantasypros.com/mlb/two-start-pitchers.php

**Search query style (if URL fetch fails):**
- `FantasyPros two-start pitchers week of April 20 2026`
- `"two-start pitchers" fantasypros {week_start}`

**What to extract from the page:**
- Pitcher name
- Team abbreviation
- Handedness (L/R)
- Both probable start dates
- Both opponents
- Home or away for each start

**Freshness rule:** FantasyPros publishes Sunday evening. If the page's "last updated" timestamp is older than 36 hours before `week_start`, reduce `synthesis_confidence` by 0.1 and flag.

**Record in source_urls:** the full URL including any `?week=` query parameter.

---

## Cross-reference validation: FanGraphs probables-grid

**URL pattern:** https://www.fangraphs.com/roster-resource/probables-grid

The probables-grid shows every team's next 5-7 scheduled starters by date. Use it to confirm the FantasyPros list.

**Procedure:**
1. For each SP on the FantasyPros two-start list, locate their team row in the FanGraphs grid.
2. Find the two dates that should have this SP starting.
3. Confirm the listed pitcher matches. If FanGraphs shows a different pitcher on one of the two dates:
   - The two-start status is in doubt. Drop the SP from the "confirmed" section.
   - Add to `red_team_findings` with severity 2, likelihood 3.
   - Either remove from board OR include with confidence 0.4 and a verdict of "VERIFY MONDAY AM".
4. If FanGraphs shows "TBD" on one of the dates, treat it as a soft confirmation -- the pitcher is likely but not guaranteed.

**When to reload:**
- Pull probables-grid at skill-runtime (Sunday night).
- If skill is re-run Monday morning, pull fresh. Rotation adjustments happen 12-24 hours before first pitch.

---

## Cross-reference: Yahoo free-agent pool

Two-start SPs are only actionable if they are free agents. Filter the ranked board into three categories:

1. **`fa`**: On Yahoo's free-agent list for SP position. These are the actionable streaming targets.
2. **`rostered-other`**: Rostered by another league team. Include for context but no action.
3. **`rostered-user`**: Already on the user's team. Include with a "START both" verdict if streamability is high.

**URL (data-sources.md):** https://baseball.fantasysports.yahoo.com/b1/23756/players?status=A&pos=SP

**Procedure (handoff to `mlb-league-state-reader`):**
- The two-start scout does NOT directly scrape Yahoo. It reads the latest output from `mlb-league-state-reader`, which owns the authenticated Chrome session.
- If no fresh Yahoo FA snapshot exists (< 6 hours old), request one from `mlb-league-state-reader` before proceeding.
- If Yahoo snapshot is unavailable, mark every SP `roster_status: unknown` and drop `synthesis_confidence` to <= 0.5.

---

## Opener / bullpen-game detection

Opener and bullpen-game risk is the single biggest deprioritization on the board. An SP who typically goes 3-4 IP cannot produce a QS, and two starts of 3-4 IP is actively harmful (ERA/WHIP exposure, zero QS, modest Ks).

### Signals that a start is an opener / bullpen game

1. **Team history**: The team has used an opener 3+ times in the last 4 weeks. As of 2026-04-17 the high-frequency teams are MIA, OAK, CHW, PIT (verify each week via recent game logs).
2. **Pitcher game logs**: The nominal starter's last 5 appearances average < 5.0 IP. Web-search: `{pitcher name} game log 2026 innings`.
3. **Team announcement**: The team has publicly announced a bullpen day for one of the two dates. Web-search: `{team} bullpen day {date} 2026`.
4. **Rotation churn**: The pitcher is a recent call-up whose role is ambiguous (swing starter / long relief).

### Procedure

For each SP on the board:

- [ ] Check team opener history (last 4 weeks)
- [ ] Pull nominal starter's last 5 appearances -- average IP and max IP
- [ ] Search for "bullpen day" announcements for both dates
- [ ] Assign `opener_risk: true | false` per start

**Penalty:**
- If `opener_risk: true` for EITHER start, apply `-30` penalty to the aggregated `streamability_score`.
- If `opener_risk: true` for BOTH starts, drop from board entirely and list in the "dropped" footer.

---

## Per-start scoring

For EACH of the two starts, compute three signals: `qs_probability`, `k_ceiling`, `era_whip_risk`. Aggregate to a per-start `streamability_score`, then average the two starts (with penalties) to the SP's final score.

### qs_probability (0-100) -- primary for our QS-scoring league

Formula (from the signal framework and league-specific QS weighting):

```
qs_probability = rolling_QS_rate(last 30 days) * matchup_multiplier
  where matchup_multiplier = 0.35 * (100 - opp_wOBA_normalized)
                           + 0.25 * park_pitcher_factor
                           + 0.25 * (100 - weather_risk)
                           + 0.15 * bullpen_state_of_own_team
```

**Data sources (per data-sources.md):**
- Rolling QS rate: FanGraphs pitcher page -> game log -> count games with IP >= 6 and ER <= 3
- Opponent wOBA: FanGraphs team batting -> vs LHP or vs RHP depending on pitcher handedness
- Park factor: FanGraphs park-factor table (`guts.aspx?type=pf&season=2026`)
- Weather: https://www.rotowire.com/baseball/weather-forecast.php
- Bullpen state: handoff from `mlb-matchup-analyzer` (bullpen_state signal) or a proxy (team bullpen ERA last 7 days)

**Normalization of opp_wOBA:**
- League-average wOBA is ~.315. Express each team's wOBA as a 0-100 scale where 50 = league average.
- Formula: `opp_wOBA_normalized = 50 + (team_wOBA - 0.315) * 1000`, clamped to 0-100.

### k_ceiling (0-100)

Formula:

```
k_ceiling = min(100, projected_Ks_for_start * 100 / 12)
```

- Projected Ks: FanGraphs Depth Charts projection for the start, or compute as `pitcher_K/9 * expected_IP / 9`.
- 12 Ks = 100 ceiling. 6 Ks = 50.

### era_whip_risk (0-100) -- higher = worse

Formula:

```
era_whip_risk = 0.5 * opp_wOBA_normalized
              + 0.3 * park_hitter_factor
              + 0.2 * pitcher_blowup_history
```

- `park_hitter_factor`: 100 - park_pitcher_factor.
- `pitcher_blowup_history`: fraction of last 10 starts with 5+ ER, scaled 0-100.

### Per-start streamability (0-100)

```
per_start_streamability = 0.55 * qs_probability
                        + 0.25 * k_ceiling
                        + 0.20 * (100 - era_whip_risk)
```

The 0.55 weight on QS probability enforces the league's QS-scoring rule. A standard streamability formula would weight more toward Ks and Wins; we explicitly do not, because our league does not score Wins.

---

## Aggregation to per-SP streamability

```
aggregated = mean(start_1_streamability, start_2_streamability)

penalties:
  - opener_risk penalty: -30 if either start has opener_risk = true
  - Coors penalty: -10 if either start is at COL (Coors Field)
  - weather penalty: -5 per start with rain_probability > 30%
  - variance flag: if |start_1 - start_2| > 25, add a note in the narrative block
    explaining the week is bimodal (good game + disaster game)

final_streamability = max(0, aggregated - sum_of_penalties)
```

**Why a variance flag, not a variance penalty?** In a daily-lineup league (Yahoo is daily-lock), the user can START the good matchup and BENCH the bad one, capturing asymmetric upside. We flag rather than penalize, and let the streaming-strategist decide. In a weekly-lock league, the variance would warrant a penalty.

---

## Confidence calibration

Compute `synthesis_confidence` as a function of data quality:

| Situation | Confidence |
|---|---|
| Both sources agree on both starts; all per-start signals computed with primary sources; Yahoo FA snapshot < 6h old | 0.80-0.90 |
| Minor conflict on one start OR one signal from fallback source | 0.65-0.79 |
| Major conflict (different pitcher on FanGraphs) OR missing weather OR Yahoo FA snapshot stale | 0.40-0.64 |
| Multiple sources failed, using only FantasyPros | <= 0.40 (red-team flag) |

---

## Signal emission

Write the output to `signals/YYYY-MM-DD-two-start.md` where `YYYY-MM-DD` is the Monday of the fantasy week (not today's date, unless they are the same). Follow the template in [template.md](template.md).

Before persisting, call `mlb-signal-emitter` for validation. If validation fails, do not persist; log the failure to `tracker/decisions-log.md` and re-run with fixes.

---

## Re-run cadence

- **Sunday night (primary)**: full run for the upcoming Monday-Sunday week.
- **Monday morning (optional refresh)**: pull FanGraphs probables-grid again to catch weekend rotation changes. If any two-start SP's second start has shifted, re-emit the signal file.
- **Wednesday (mid-week refresh)**: if a SP's first start was rained out or postponed, re-evaluate whether the second start alone still justifies a hold/drop decision. Emit a partial signal update with `red_team_findings` noting the rain-out.

---

## Citations and source URL format

Every signal file lists the EXACT URLs consulted, not generic domain names. Examples:

Good:
- `https://www.fantasypros.com/mlb/two-start-pitchers.php?week=18`
- `https://www.fangraphs.com/roster-resource/probables-grid?date=2026-04-20`

Bad:
- `https://fantasypros.com`
- `FanGraphs probables grid`

If a search returned nothing useful for a specific signal, set `source_urls: []` for that signal component and reduce confidence to 0.3 per CLAUDE.md operating rule #7 (degrade gracefully).
