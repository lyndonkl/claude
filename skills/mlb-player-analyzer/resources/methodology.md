# MLB Player Analyzer — Methodology

Authoritative math and procedure for every signal this skill emits. The signal catalog is defined in `/Users/kushaldsouza/Documents/Projects/yahoo-mlb/context/frameworks/signal-framework.md`; this document explains *how* to compute each one.

---

## League-specific weighting reminders

This is a **5x5 H2H Categories** league with:
- Batter cats: R / HR / RBI / SB / **OBP** (not AVG)
- Pitcher cats: K / ERA / WHIP / **QS** (not W) / SV

Two consequences percolate through every formula below:

1. **OBP, not AVG.** Walk rate is a category-winning feature. Every rate-stat input prefers wOBA (walk-inclusive) or OBP to AVG. A low-AVG / high-BB hitter (Soto-type) must not be penalized.
2. **QS, not W.** `qs_probability` ignores win-probability and team run support. It is the probability of **6+ IP with <=3 ER**. Openers and bulk guys throwing 4-5 innings score zero QS regardless of stuff.

---

## Source cheatsheet (where to web-search)

| Data need | Primary URL | Notes |
|---|---|---|
| Season + 15-day xwOBA (hitter) | `https://baseballsavant.mlb.com/savant-player/<slug>-<id>` | Custom date-range tool under "Statcast" tab |
| xERA, whiff%, CSW (pitcher) | `https://baseballsavant.mlb.com/savant-player/<slug>-<id>` | "Pitching" tab |
| ATC rest-of-season projections | `https://www.fangraphs.com/projections?type=atc` | ATC is the consensus ensemble |
| Player page + splits | `https://www.fangraphs.com/players/<slug>/<id>` | Splits tab for vs RHP / vs LHP |
| Confirmed lineups | `https://www.mlb.com/starting-lineups` | Posts ~2-3h pre-game |
| Probable pitchers | `https://www.mlb.com/probable-pitchers` | Updated daily |
| Park factors | `https://www.fangraphs.com/guts.aspx?type=pf&season=2026&teamid=0` | 100 = neutral |
| Weather | `https://www.rotowire.com/baseball/weather-forecast.php` | Park-by-park |
| Closer depth | `https://www.rotoballer.com/mlb-saves-closers-depth-charts/226767` | Tier 1-4 + committee notes |
| Two-start planner | `https://www.fantasypros.com/mlb/two-start-pitchers.php` | Weekly, Sun night |

Search-query style: include "2026", the player's full name, and the exact metric. Prefer `"Junior Caminero" xwOBA 2026 season` over `Caminero stats`.

**Citation rule**: every factual claim in the signal file must trace to a URL in `source_urls:`. If a source is unreachable, set that component's confidence to 0.3 and record the gap in `red_team_findings`.

---

## Role classification

Before signal computation, classify the player:

- **Hitter**: appears in today's lineup (or projected to) at a position slot. Compute hitter signals only.
- **SP**: on today's probable-pitcher chart. Compute pitcher SP signals.
- **RP (closer-role)**: RotoBaller Tier 1 or Tier 2 at the team's closer slot. Compute `k_ceiling`, `era_whip_risk`, `save_role_certainty`. Leave `qs_probability`, `streamability_score`, `two_start_bonus` null.
- **RP (non-closer)**: compute only `era_whip_risk`, `k_ceiling`, `save_role_certainty` (will be low). Low-leverage RPs are typically not rosterable.
- **Two-way (Ohtani-type)**: emit two files -- one `role: hitter`, one `role: pitcher SP` (only on days he starts).
- **Opener / bulk**: flag explicitly; `qs_probability` = 0. Streamability collapses.

---

## HITTER signals

### form_score (0-100)

Intent: Is this hitter hot or cold by Statcast truth, not box-score noise?

```
form_score = clamp(
    50 + (xwOBA_15d - xwOBA_season) * 500,
    0, 100
)
```

- `xwOBA_15d`: rolling 15-day expected wOBA from Baseball Savant
- `xwOBA_season`: season-to-date xwOBA from same source
- Multiplier of 500 scales a 0.040 xwOBA gap (large) to +/-20 points
- 50 = at season baseline; 70 = meaningfully hot; 30 = meaningfully cold

**Confidence**: 0.85 default if Savant returns both numbers. 0.60 if fewer than 40 PAs in the 15-day window. 0.30 if either number is missing.

### matchup_score (0-100)

Intent: How friendly is today's context (opp SP + park + platoon + weather)?

Weighted composite per the signal framework:

```
matchup_score = 0.40 * opp_sp_component
              + 0.25 * park_component
              + 0.25 * platoon_component
              + 0.10 * weather_component
```

Each component is itself 0-100:

- **opp_sp_component**: `100 - opp_sp_quality` (a bad SP is a good matchup). `opp_sp_quality` comes from the matchup-analyzer signal if already emitted; otherwise derive from opp SP xFIP:
  `opp_sp_quality = clamp(50 + (4.00 - xFIP) * 25, 0, 100)` (4.00 xFIP = league avg -> 50).
- **park_component**: `park_hitter_factor` from matchup-analyzer, or raw FanGraphs park factor (100 neutral) rescaled: `park_component = clamp((park_factor - 85) / 30 * 100, 0, 100)` so 85 -> 0, 100 -> 50, 115 -> 100.
- **platoon_component**: compare player's career wOBA vs the opp SP's handedness to his overall wOBA. `platoon_component = clamp(50 + (wOBA_vs_hand - wOBA_overall) * 500, 0, 100)`. A LHH vs RHP with .360 vs .330 gets 65.
- **weather_component**: start at 50. +10 if wind blowing out >=8mph, -15 if wind blowing in >=8mph, -5 for temps <55F, +5 for temps >=80F. Clamp 0-100. Pull from `weather_risk` or RotoWire.

**Confidence**: min of component confidences.

### opportunity_score (0-100)

Intent: How many plate appearances, in what lineup context?

```
opportunity_score = 40 + 10 * expected_PAs + slot_bonus
                    clamped 0..100
```

Where:
- `expected_PAs` is drawn from lineup slot: #1-#2 -> 4.8, #3-#4 -> 4.6, #5 -> 4.3, #6-#7 -> 4.0, #8-#9 -> 3.7 (American League; NL #9 is lower)
- `slot_bonus`: +5 for #1-#2 (more R chances), +10 for #3-#5 (RBI spot), 0 otherwise

If lineup not yet posted, use projected slot from FanGraphs Roster Resource and cap confidence at 0.70.

### daily_quality (0-100) — PRIMARY HITTER SIGNAL

This is the number the **lineup-optimizer** reads to decide START vs SIT.

```
daily_quality = 0.35 * form_score
              + 0.40 * matchup_score
              + 0.25 * opportunity_score
```

The matchup weight (0.40) exceeds form (0.35) because daily fantasy is overwhelmingly situation-driven; current form is noisy over a 15-day window. Opportunity (0.25) is the floor -- a guy who won't play can't produce.

**Confidence**: arithmetic mean of the three component confidences.

**Thresholds**:
- >=60: START
- 45-59: neutral (use category-pressure to tiebreak)
- <45: SIT

### regression_index (+/-100)

Intent: Is actual production being flattered or cheated by luck?

```
regression_index = clamp(
    (xwOBA_season - wOBA_season) * 500,
    -100, +100
)
```

- Positive = unlucky (buy / start through slumps)
- Negative = lucky (sell / fade)
- A +0.040 gap -> +20 regression_index; typical "buy window" threshold is >=+25

**Confidence**: 0.80 with both Savant xwOBA and FanGraphs/BRef wOBA; 0.30 if either missing.

### obp_contribution (0-100)

Intent: What is this player's projected OBP output today, normalized by position scarcity?

```
obp_projection = 0.5 * ATC_OBP + 0.5 * matchup_adjusted_OBP
matchup_adjusted_OBP = season_OBP + platoon_delta + park_OBP_nudge
obp_contribution = clamp(
    ((obp_projection * expected_PAs) / position_baseline) * 50,
    0, 100
)
```

Position baselines (rough league-average OBP x PAs for the slot):
- C: 1.35, 1B: 1.55, 2B: 1.45, 3B: 1.50, SS: 1.45, OF: 1.50, DH: 1.60

50 = position-average contribution. OBP is our category, so this signal carries more weight than AVG-based equivalents would.

### sb_opportunity (0-100)

Intent: How likely is a steal attempt to happen and succeed today?

```
sb_opportunity = 0.45 * sprint_speed_component
               + 0.25 * opp_catcher_component
               + 0.20 * opp_sp_hold_component
               + 0.10 * lineup_context_component
```

- `sprint_speed_component`: Savant sprint speed, `(sprint_ft_per_s - 25) * 25` clamped 0-100. 27+ ft/s -> 50+. Reaches ~75 at 28 ft/s.
- `opp_catcher_component`: `100 - CS%_percentile`. Low CS% = good for stealing.
- `opp_sp_hold_component`: `100 - SB_allowed_rate_percentile`. SPs with high SB rates against -> high component.
- `lineup_context_component`: 70 if green-light manager (KC, CIN, etc.), 40 if conservative manager (NYY circa 2026), 55 default.

### role_certainty (0-100)

- 100: confirmed in today's posted lineup (MLB.com starting-lineups)
- 85: beat-writer tweet says "in there" but lineup not yet posted
- 70: FanGraphs Roster Resource projects starting, no public confirmation
- 50: platoon half -- may or may not play depending on opp SP handedness
- 20: likely benched today, not on IL
- 0: on IL, suspended, or DFA'd

---

## PITCHER signals

### qs_probability (0-100)

Intent: Probability of 6+ IP and <=3 ER today.

Two-step computation:

1. **Baseline rate** from FanGraphs ATC and season history:
   - ATC projected IP/start and ERA -> derive expected QS rate
   - Or: recent QS rate (last 10 starts) as a prior if ATC unavailable
   - Typical QS rates: top SPs 55-65%, mid 35-45%, streamers 20-30%

2. **Matchup multiplier** applied:
   - Opp wOBA (higher = worse matchup): multiply by `1 - (opp_wOBA - 0.315) * 2`. A .340 opp wOBA -> 0.95x.
   - Park: multiply by `park_pitcher_factor / 50` capped at 1.25. Coors -> ~0.65x. Petco -> ~1.15x.
   - Weather: -5% if wind blowing out at a hitter-friendly park.

```
qs_probability = clamp(
    baseline_qs_rate * 100 * opp_multiplier * park_multiplier * weather_multiplier,
    0, 100
)
```

### k_ceiling (0-100)

Intent: Normalized projected Ks for this start.

```
projected_Ks = IP_projected * K_per_9 / 9
projected_Ks_matchup = projected_Ks * (opp_K_rate / 0.225)
k_ceiling = clamp((projected_Ks_matchup - 3) * 15, 0, 100)
```

- `IP_projected` from ATC
- `K_per_9` from ATC
- `opp_K_rate` is opp lineup's team strikeout rate from FanGraphs (league avg ~0.225)
- The `(projected - 3) * 15` scaling makes 6 Ks -> 45, 8 Ks -> 75, 10+ Ks -> 100

### era_whip_risk (0-100)

Intent: Probability of a blowup that tanks ratios.

```
era_whip_risk = 0.35 * opp_wOBA_component
              + 0.30 * park_component
              + 0.20 * pitcher_volatility
              + 0.15 * weather_component
```

- `opp_wOBA_component`: `(opp_wOBA - 0.290) * 1000` clamped 0-100. A .335 opp wOBA -> 45.
- `park_component`: `100 - park_pitcher_factor`. Coors is 100, Petco near 0.
- `pitcher_volatility`: std-dev of last 10 starts' game-score, normalized. High-variance SPs (6 shutout IP one day, 4 IP 6 ER the next) score higher.
- `weather_component`: 50 default, +15 if wind out 10+mph, -10 if cold and still.

### streamability_score (0-100) — PRIMARY SP SIGNAL

```
streamability_score = 0.40 * qs_probability
                    + 0.30 * k_ceiling
                    + 0.30 * (100 - era_whip_risk)
```

This is the number the **streaming-strategist** reads.

**Thresholds**:
- >=70: STREAM
- 55-69: borderline (stream only if punting ratios or needing Ks desperately)
- <55: DO NOT STREAM

### two_start_bonus (bool)

`true` if this SP appears on the FantasyPros two-start list for the scoring week containing `date`. No math; lookup only. Source URL is required.

### save_role_certainty (0-100, RP only)

Map RotoBaller closer-chart tier to numeric:

- Tier 1 (locked closer, no committee): 90-100
- Tier 2 (clear primary but shaky manager): 70-89
- Tier 3 (timeshare / matchup closer): 40-69
- Tier 4 (next-in-line / speculation): 20-39
- Not on closer chart: 0-19

Cross-check RotoBaller against Pitcher List or Closer Monkey if save uncertainty is high.

---

## Composite cheat sheet

```
# Hitter primary
daily_quality = 0.35*form_score + 0.40*matchup_score + 0.25*opportunity_score

# Pitcher SP primary
streamability_score = 0.40*qs_probability + 0.30*k_ceiling + 0.30*(100 - era_whip_risk)

# Regression (bipolar)
regression_index = clamp((xwOBA - wOBA) * 500, -100, +100)
```

---

## Confidence assignment

Per-component rules (default starting points; adjust down on data gaps):

| Signal | Confidence = 0.85+ if | Confidence = 0.30 if |
|---|---|---|
| form_score | Savant returns both 15d and season xwOBA, 40+ PAs | Either number missing |
| matchup_score | opp SP known, park/weather known, splits populated | Any two components missing |
| opportunity_score | Confirmed lineup posted | Lineup not yet out (cap 0.70 -> 0.95 once posted) |
| daily_quality | Mean of above >=0.85 | Mean <0.50 |
| regression_index | xwOBA and wOBA both available | Either missing |
| obp_contribution | ATC and season splits both available | No ATC access |
| sb_opportunity | Sprint speed + catcher CS% both available | Either missing |
| role_certainty | Lineup confirmed | Reading tea leaves |
| qs_probability | ATC IP/ER + opp team wOBA both available | Either missing |
| k_ceiling | ATC K/9 + opp team K-rate both available | Either missing |
| era_whip_risk | opp wOBA + park factor both available | Either missing |
| streamability_score | Mean of above >=0.80 | Mean <0.50 |
| save_role_certainty | RotoBaller chart accessible today | Chart stale or 404 |

**Rule**: if any component confidence drops below 0.4, populate `red_team_findings` with the gap, set severity >= 2, and propose a mitigation (e.g., "re-check once lineup posts at 2pm").

---

## Search-failure degradation

If a primary source 404s or returns empty:
1. Try the fallback (e.g., Steamer for projections when ATC is down; FanGraphs Roster Resource when MLB.com lineups lag).
2. If both fail, emit the signal with `confidence: 0.3` and a `red_team_finding` note.
3. Never fabricate a number. An omitted signal (`null`) is preferable to a guessed one.
4. Log the failure in `tracker/decisions-log.md` so the team can patch the source list.

---

## Validation before write

Run `mlb-signal-emitter` (the validator skill) on every signal file before persisting to `signals/`. It checks:
- Frontmatter parses as YAML
- All numeric signals in declared ranges (0-100 or +/-100)
- `confidence` present per signal and in [0, 1]
- `source_urls` non-empty (or, if empty, confidence for all numeric signals <= 0.3)
- `type: player` and `role` in {hitter, pitcher}
- Timestamp `computed_at` is ISO-8601

On validation failure, do not write the file. Log the failure and retry after fixing the offending field.
