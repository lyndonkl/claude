# MLB Category State Analyzer — Methodology

Baseball-specific state extraction and projection-dict construction for the Yahoo 10-cat H2H matchup. The matchup-level and per-cat **win-probability math is no longer computed here** — it is delegated to the sibling skill `matchup-win-probability-sim`. This file covers:

1. How to pull matchup state from Yahoo.
2. How to project remaining games/PAs/IP per roster.
3. How to turn that into `{mean, stddev}` projection dicts that feed the sim.
4. How to derive `cat_position`, `cat_pressure`, `cat_reachability`, and `cat_punt_score` from (state + sim output).

Authoritative reference: `context/frameworks/category-math.md`.

## Table of Contents
- [Pulling Matchup Data from Yahoo](#pulling-matchup-data-from-yahoo)
- [Projecting Remaining Games](#projecting-remaining-games)
- [Counting vs. Ratio Cats](#counting-vs-ratio-cats)
- [Building Per-Cat Projection Dicts](#building-per-cat-projection-dicts)
- [Invoking `matchup-win-probability-sim`](#invoking-matchup-win-probability-sim)
- [Signal Formulas](#signal-formulas)
  - [cat_position](#cat_position)
  - [cat_pressure](#cat_pressure)
  - [cat_reachability](#cat_reachability)
  - [cat_punt_score](#cat_punt_score)
- [Worked Example — OBP (ratio batting cat)](#worked-example--obp-ratio-batting-cat)
- [Worked Example — SV (volatile counting cat)](#worked-example--sv-volatile-counting-cat)
- [Worked Example — QS (counting pitching cat, not Wins)](#worked-example--qs-counting-pitching-cat-not-wins)
- [Edge Cases](#edge-cases)

---

## Pulling Matchup Data from Yahoo

### Primary source

- **URL pattern**: `https://baseball.fantasysports.yahoo.com/b1/23756/5/matchup?week=<N>`
- **Week `N`**: read from `context/league-config.md` (season start + today's date → week number).
- **Auth**: session-level Yahoo login handled by the browser/tool layer. If the page returns a login wall, degrade gracefully.

### What to extract

For each of the 10 categories, both teams:

1. **Current total** (R, HR, RBI, SB, K, QS, SV) — integer counters.
2. **Current ratio** (OBP, ERA, WHIP) — decimal with 3 places.
3. **Denominator for ratio cats**:
   - OBP: total plate appearances (PA) so far this week
   - ERA: total innings pitched (IP) so far this week
   - WHIP: total IP so far this week (same as ERA)
4. **Games/starts played so far** — used to infer remaining.

### Fallback (if Yahoo is unreachable)

1. Ask the user to paste the matchup page text (the H2H matchup tab shows all 10 cats inline).
2. If paste unavailable, degrade to **ratios only** (no volume) and flag `confidence: low` in the signal file. The ratio-cat projection dict will be unreliable — mark that in red-team findings.
3. Never fabricate — if a denominator can't be obtained, emit the sim call with a widened stddev and flag it.

### Data quality checks

- **Sanity**: R + HR + RBI totals should be internally consistent with roster size (e.g., 40+ R by Friday means the scrape might have grabbed season totals).
- **Timestamp**: Yahoo updates in near-real-time. Note the scrape time in `computed_at`.
- **Mid-game caveat**: If scraping during an active game, the denominator is moving. Prefer AM scrapes (before West Coast first pitches).

---

## Projecting Remaining Games

For each roster, count games from **tomorrow through Sunday** (or end-of-scoring-period).

### Hitter volume (for R, HR, RBI, SB, OBP)

```
Remaining hitter-games = Σ over rostered hitters of:
    (MLB team games remaining in the week)
  × (probability player is in the lineup)
  × (lineup eligibility: 1 if startable slot, 0.5 if bench-only)
```

- **MLB schedule**: MLB.com schedule page, filtered by team + date range.
- **Lineup probability**: default 0.9 for regulars, 0.6 for platoon, 0.3 for bench. Read `role_certainty` from upstream player signals if available.
- **Off-days / doubleheaders**: matter a lot. A team with 4 games vs. one with 7 has a big volume disadvantage.

### Pitcher starts remaining (for K, QS, ERA, WHIP)

```
Remaining SP starts = count of probable SP entries for rostered SPs
                      through end-of-week from RotoWire / MLB.com
```

- **Two-start pitchers**: count each start independently.
- **Streamers not yet acquired**: count only if the waiver plan locks them in.
- **Skipped starts / PPD**: adjust down.

### Projected IP

```
Projected remaining IP = Σ over scheduled starts of:
    (pitcher's average IP per start, from FanGraphs rolling)
```

Typically 5.5–6.5 IP per start. Relievers contribute 1 IP per appearance (~2 appearances per week for a closer, ~3 for a setup RP).

### Reliever days remaining (for SV)

```
Save opportunities ≈ (scheduled team games) × (team win probability) × (save situation rate ~0.25)
                     for each rostered closer
```

Much noisier than starter projections — treat as a range, not a point estimate. This noise translates directly into a higher `stddev` in the SV projection dict.

---

## Counting vs. Ratio Cats

The 10 cats split 7 counting + 3 ratio.

| Cat | Type | Unit | Volume driver |
|---|---|---|---|
| R, HR, RBI, SB | counting (bat) | integer | hitter games × PA/game |
| OBP | **ratio** (bat) | (H + BB + HBP) / PA | PA denominator |
| K | counting (pitch) | integer | SP starts × K/9 × IP |
| QS | counting (pitch) | integer | SP starts × QS probability |
| SV | counting (pitch) | integer | closer appearances |
| ERA | **ratio** (pitch) | ER × 9 / IP | IP denominator |
| WHIP | **ratio** (pitch) | (H + BB) / IP | IP denominator |

**Counting cats** are additive — projection mean stacks linearly.

**Ratio cats** are weighted averages — new production dilutes the current ratio proportionally to volume. This is the key math trap; see the OBP worked example.

---

## Building Per-Cat Projection Dicts

This is the core input to `matchup-win-probability-sim`. For each team, produce a dict:

```
projection_dict = {
  cat: {mean: float, stddev: float}
  for cat in [R, HR, RBI, SB, OBP, K, ERA, WHIP, QS, SV]
}
```

**Important convention**: use **final projected value** (current_total + expected_remaining) for counting cats, and **final projected ratio** for ratio cats. Apply the same convention on both sides. The sim compares our draw to opp draw per cat, so as long as the convention matches for both teams, margins are correct.

### Counting cats (R, HR, RBI, SB, K, QS, SV)

```
expected_remaining[cat] = Σ over roster of:
    (per-player per-game rate for cat)
  × (games remaining for player)
  × (daily_quality[player, day] averaged across days)

mean[cat]   = current_total[cat] + expected_remaining[cat]
stddev[cat] = CV × expected_remaining[cat]
              where CV ≈ 0.35 for most counting cats
              SV uses CV ≈ 0.55 (high variance)
              HR/SB use CV ≈ 0.50 (low-mean discrete)
```

**Per-player per-game rates**:
- **R/RBI**: from season rate × park factor × lineup-position adjustment.
- **HR**: from season HR/PA × expected PA × park HR factor.
- **SB**: from `sb_opportunity` signal (upstream) × games.
- **K**: Σ over scheduled SPs of (K/9 × projected IP for start).
- **QS**: Σ over scheduled SPs of `qs_probability[pitcher, start]` (upstream signal, not team win prob).
- **SV**: Σ over rostered closers of (team expected wins × ~0.45 save-situation rate × `save_role_certainty`).

### Ratio cats (OBP, ERA, WHIP)

The ratio is a weighted average:

```
projected_remaining_ratio = weighted average of rostered players' rate stat, weighted by expected volume (PA or IP)

mean[cat] = (current_ratio × current_volume
           + projected_remaining_ratio × remaining_volume)
          / (current_volume + remaining_volume)

stddev[cat] ≈ σ_per_obs / sqrt(current_volume + remaining_volume)
              where σ_per_obs is the per-observation SD:
                OBP  ≈ 0.48   → weekly stddev typically 0.012–0.020
                ERA  ≈ 3.50 × sqrt(9/IP) → weekly stddev typically 0.35–0.55
                WHIP ≈ 1.10 × sqrt(1/IP) → weekly stddev typically 0.06–0.10
```

**Roster ratio projections**:
- **OBP**: weighted-average OBP of expected-starting hitters (use OBP, not AVG).
- **ERA**: weighted-average ERA of expected-starting pitchers, IP-weighted.
- **WHIP**: weighted-average WHIP, IP-weighted.

**Key property**: as remaining_volume grows (more games left), stddev shrinks. This is what lets the sim correctly reward a large volume edge — a team with 110 projected PAs has a tighter ratio distribution than a team with 55, and the sim sees that.

### `daily_quality` signal (upstream input)

Each rostered player has a per-day `daily_quality ∈ [0, 100]` from `mlb-player-analyzer`. It bundles matchup quality, lineup slot, park, weather, and role certainty into a single multiplier. Use it as:

```
effective_rate_for_day = season_rate × (daily_quality / 100)^α
                          where α ≈ 1.0 for most cats
                          (the exponent can be sub-linear for noisy cats like SV)
```

Average `daily_quality` across the remaining days per player to get the per-game rate used in counting-cat projections.

### Minimum-threshold encoding

If either team is on pace to finish below Yahoo's weekly IP or PA minimum:

- The ratio cat auto-forfeits against that team.
- Encode by setting **their** ratio-cat `mean` to a punitive value (e.g., 99.9 for ERA) and `stddev` near zero.
- Additionally, add `+20 × below_min_threshold` to `cat_punt_score` for that cat on our side (applied after the sim — see below).

---

## Invoking `matchup-win-probability-sim`

Once both projection dicts are built, call the sibling skill:

```
inputs:
  our_per_cat_projection:  <dict from above>
  opp_per_cat_projection:  <dict from above>
  cat_list:                [R, HR, RBI, SB, OBP, K, ERA, WHIP, QS, SV]
  cat_inverse_list:        [ERA, WHIP]    # lower-is-better
  cat_win_threshold:       6              # Yahoo 10-cat majority
  sim_mode:                "monte_carlo"
  n_simulations:           10000
  random_seed:             42             # reproducibility
  tie_rule:                "half"         # matches Yahoo H2H convention

outputs:
  matchup_win_probability:   float in [0,1]
  per_cat_win_probability:   dict[cat, float]  # THIS is our cat_reachability source
  expected_cats_won:         float
  variance_estimate:         float
```

Store the full output. Persist `matchup_win_probability`, `expected_cats_won`, and the sim `meta` block (mode + n_sims + seed) in the signal-file frontmatter. All four per-cat signals in the output table are derived from `per_cat_win_probability` + baseball state — see below.

---

## Signal Formulas

All four signals are emitted per cat. Each is a numeric scalar; `cat_position` is an enum.

### `cat_position`

Enum: `winning` / `tied` / `losing`. Based on current totals (not sim).

- For ratio cats, *winning* means the direction that helps:
  - OBP: higher is winning.
  - ERA, WHIP: lower is winning.
- **Frozen cats**: if opponent is mathematically locked below/above minimum-IP/PA threshold, treat as `winning` or `losing` with confidence 1.0. Encode into the projection dict (see above) so the sim also sees it; set pressure = 20 if locked-in win, 30 if locked-in loss.

### `cat_pressure`

How much should we push this cat this week? Computed locally from baseball state (not sim). Implements `context/frameworks/category-math.md`:

```
cat_pressure =
    50                                           # neutral baseline
  + 20 × is_close_margin                         # deficit/lead ≤ 10% of current total
  + 15 × opponent_volume_exhausted               # we have more games/starts remaining
  - 10 × locked_in_win
  - 30 × locked_in_loss
  clamp to [0, 100]
```

**Triggers**:

- `is_close_margin`: for counting cats, `|margin| ≤ 0.10 × max(our_total, opp_total)` or `|margin| ≤ 3` (whichever is larger). For ratio cats, `|margin| ≤ 0.015` (15 OBP points, 0.30 ERA, 0.08 WHIP).
- `opponent_volume_exhausted`: we have ≥ 15% more remaining volume than opp (games, starts, or IP).
- `locked_in_win`: from projection-dict means + 2σ headroom — our mean − 2 × our_stddev > opp mean + 2 × opp_stddev (direction-aware for inverse cats).
- `locked_in_loss`: symmetric the other way.

### `cat_reachability`

**Now delegated to `matchup-win-probability-sim`.**

```
cat_reachability[cat] = round(100 × per_cat_win_probability[cat])
```

That's it — no z-score tables, no worst/expected/best-case buckets. The sim owns the probability math (normal draws, inverse-cat margin flip, volume-weighted stddev in ratio cats, tie-rule handling). This skill just consumes the per-cat probability and scales to [0, 100].

**Why this is better than the old heuristic**:
- Ratio cats naturally incorporate volume via the projection-dict `stddev` — a 55-IP week is wider than a 110-IP week, and the sim reflects that.
- Counting cats with low means (SV, HR for a short week) can be passed with `distribution_family = "poisson"` for correct tail behavior.
- Reachability and matchup-win probability are coherent — they come from the same sim run.
- Reproducible under a fixed `random_seed`.

### `cat_punt_score`

Higher = more sensible to concede. Computed locally using the sim's `per_cat_win_probability`:

```
cat_punt_score =
    (100 - cat_reachability) × 0.6                    # = 60 × (1 − per_cat_win_probability[cat])
  + 30 × cat_is_volatile                              # SV (and in other leagues, W)
  + 20 × below_min_threshold                          # forfeiting via min-IP/PA
  - 10 × cat_has_spillover                            # K feeds QS; OBP feeds R; HR feeds R+RBI
  clamp to [0, 100]
```

**Volatility flag** (`cat_is_volatile`): currently `True` only for SV. This is a baseball-domain tag, not something the sim can infer. Kept here.

**Spillover map**:

- K has spillover into QS (−10)
- OBP has spillover into R (−10)
- HR has spillover into both R and RBI (−10)
- ERA and WHIP co-move (if you punt one, the other typically follows; treat as independent in the score but note in red-team)

---

## Worked Example — OBP (ratio batting cat)

This is the most common ratio-cat trap. **AVG would be simpler; OBP requires tracking walks.**

### Setup

- **Week 3, Wednesday AM. vs. Los Doyers.**
- **Current**: us .342 in 82 PAs; opp .336 in 78 PAs. Margin +.006 in our favor.
- **Remaining volume**: we have ~110 PAs left; opp has ~90.
- **Roster OBP projection** (weighted average of expected starters):
  - Us: .348 (solid walk-rate roster)
  - Opp: .345 (power-biased, lower walks)

### Build the projection-dict entries

```
Our projected final OBP mean  = (.342 × 82 + .348 × 110) / 192 = .346
Our projected final OBP stddev ≈ 0.48 / sqrt(192) ≈ .035 per obs normalized to weekly ≈ .015

Opp projected final OBP mean  = (.336 × 78 + .345 × 90) / 168 = .341
Opp projected final OBP stddev ≈ 0.48 / sqrt(168) ≈ .016
```

Projection-dict entries:

```
our:  OBP: {mean: 0.346, stddev: 0.015}
opp:  OBP: {mean: 0.341, stddev: 0.016}
```

### Sim output (illustrative)

Sim returns `per_cat_win_probability[OBP] ≈ 0.60` — our mean is .005 above opp, combined stddev is ~.022, `Φ(0.005 / 0.022) ≈ Φ(0.23) ≈ 0.59`.

### Signal values

- `cat_position`: **winning** (thin margin, +.006)
- `cat_pressure`: 50 (baseline) + 20 (close margin, ≤.015) + 15 (volume edge 110 vs 90) − 0 (not locked) = **85**. Clamp fine. Published = **85**.
- `cat_reachability`: **60** (from sim, = round(100 × 0.60)).
- `cat_punt_score`: (100 − 60) × 0.6 = 24, + 0 (not volatile), + 0 (no threshold risk), − 10 (OBP → R spillover) = **14**.

### Verdict

**Push**. Lineup-optimizer should favor high-OBP bats (walks count — Juan Soto > Austin Riley on an OBP-push day). The .006 lead is brittle; one 0-for-5 day from a starter can flip it.

---

## Worked Example — SV (volatile counting cat)

Saves are the lowest-reachability, highest-punt-score cat in almost every matchup. This is why SV is the most commonly punted category in this league.

### Setup

- **Current**: us 3 SV, opp 5 SV. Deficit of 2.
- **Remaining**: 4 scoring days left.
- **Our closers**: one locked closer (projected ~1.8 saves, CV high). `save_role_certainty` = 90.
- **Opp closers**: two locked closers (projected 2.7 saves combined).

### Build the projection-dict entries

```
our: SV: {mean: 3 + 1.8 = 4.8, stddev: 0.55 × 1.8 ≈ 1.0 → use 1.4 given the low-mean discrete noise}
opp: SV: {mean: 5 + 2.7 = 7.7, stddev: 0.55 × 2.7 ≈ 1.5}
```

Margin mean = −2.9; combined stddev ≈ sqrt(1.4² + 1.5²) ≈ 2.05; Φ(−2.9 / 2.05) ≈ Φ(−1.41) ≈ 0.08.

### Sim output

`per_cat_win_probability[SV] ≈ 0.10`.

### Signal values

- `cat_position`: **losing**
- `cat_pressure`: 50 (baseline) + 0 (margin of 2 isn't close under ≤10% rule with max of 7.7) + 0 (no volume edge on RP days) − 0 (not locked-loss with variance this high) = **50**. But many analysts lean down for "losing and can't catch" and land at ~**38**. Use **38** as the published value (apply a soft −12 adjustment when both position is losing and reachability < 15).
- `cat_reachability`: **10** (from sim, = round(100 × 0.10)).
- `cat_punt_score`: (100 − 10) × 0.6 = 54, + 30 (SV is volatile), + 0 (no threshold risk), − 0 (no spillover) = **84**.

### Verdict

**Punt**. Free up the second RP slot for a streaming SP (pushes K, QS, ERA, WHIP) or a walk-heavy OBP bat. Warn the user: "We're letting saves go — keep our closer for the other matchups, but this week the bench slot serves us better on a streamer."

### When NOT to punt saves

- Lead of 1+ with 2+ locked closers on roster and opp has a shaky closer → the projection-dict will show higher mean and the sim will return `per_cat_win_probability` ~0.70, promoting SV back to push.
- Our closer is named the 9th-inning guy on a team with 4 projected wins this week → mean rises, sim reflects it.

---

## Worked Example — QS (counting pitching cat, not Wins)

QS is the pitching cat most teams undervalue. **A 5-inning outing scores zero.** The league rewards innings-eaters, not bullpen-game SPs.

### Setup

- **Current**: us 2 QS, opp 1 QS. +1 lead.
- **Remaining SP starts**: us 9 (3 two-start pitchers), opp 7.
- **QS probability per start** (from `mlb-player-analyzer`'s `qs_probability` signal):
  - Us: avg 0.45 across 9 starts → expected 4.05 QS
  - Opp: avg 0.40 across 7 starts → expected 2.80 QS

### Build the projection-dict entries

```
our: QS: {mean: 2 + 4.05 = 6.05, stddev: 0.35 × 4.05 ≈ 1.5}
opp: QS: {mean: 1 + 2.80 = 3.80, stddev: 0.35 × 2.80 ≈ 1.4}
```

Margin mean = +2.25; combined stddev ≈ sqrt(1.5² + 1.4²) ≈ 2.05; Φ(2.25 / 2.05) ≈ Φ(1.10) ≈ 0.86.

### Sim output

`per_cat_win_probability[QS] ≈ 0.85`.

### Signal values

- `cat_position`: **winning**
- `cat_pressure`: 50 + 0 (margin isn't in the ≤10% close band — max is ~6, 1/6 > 10%) + 15 (9 vs. 7 starts is a volume edge) − 10 (locked-ish win, but we don't pass the strict 2σ test, so skip) = **65**. Many analysts push to **78** for strong lead + volume-edge + favored pitching cat. Use **78** as the published value.
- `cat_reachability`: **85** (from sim, = round(100 × 0.85)).
- `cat_punt_score`: (100 − 85) × 0.6 = 9, + 0 (not volatile), + 0, − 10 (K → QS spillover; pushing K tends to push QS) = **~−1** → clamp to **9** (don't clamp negative below 0; small positive). Round to **9**.

### Verdict

**Push hard**. Start every rostered SP with a reasonable matchup. Consider FAAB on a streamer if any rostered SP has an ugly weekend slate. Do NOT stream a 5-IP "opener" type — zero QS value.

### Interplay with W-instead-of-QS leagues

This is NOT a Wins league. A 6 IP / 0 ER with a no-decision scores a QS but not a W. A 4 IP / 0 ER win scores a W but not a QS. If the user comes from a W league, correct them explicitly in the brief: "In this league, we want the pitcher to go 6+ innings with ≤3 earned runs — whether the team wins doesn't matter."

---

## Edge Cases

### Monday (start of week)

Everything is tied at 0. `cat_position` = tied across the board. `cat_pressure` defaults to 50 + volume adjustments. Projection-dict means are entirely driven by roster strength × games remaining; stddevs are largest (full-week uncertainty). The sim returns per-cat probs driven entirely by roster-quality margins. Use the season-long roster strength as the signal source for per-player rates.

### Sunday (last day)

Locked-in status applies aggressively. Projection-dict stddevs shrink dramatically; sim naturally returns `per_cat_win_probability` near 0 or 1 for most cats. Many cats will be locked — set their `cat_pressure` to 20 or 30 manually, `cat_reachability` will be 100 (locked win) or 0 (locked loss) via the sim. Signal confidence 0.95+.

### Ratio cat with min-IP/PA risk

Yahoo requires a minimum IP (typically 20) for the week. If opp is projected to finish at 15 IP, they auto-forfeit ERA and WHIP. Encode by setting opp ERA mean = 99.9 and stddev = 0.01 in the projection dict → sim returns `per_cat_win_probability = 1.0`. Also add `+20 × below_min_threshold` to `cat_punt_score` if we're the one at risk. Note prominently in red-team findings.

### Two-way eligibility (Ohtani case)

Shohei Ohtani counts toward both batting and pitching volumes. Double-count him correctly: PAs add to batting volume; IP on his starting days add to pitching volume. Do not double-count his plate appearances for pitching IP.

### Mid-week injury

If a key roster player lands on the IL mid-week, rebuild the projection dict with updated games-remaining × roster and re-invoke the sim. If the change pushes a cat from push → punt, flag as a red-team finding for the coach to communicate.

### Trades executed mid-matchup

Yahoo's default is that stats from the acquired player count from acquisition date forward. Recompute remaining volume with the new roster; rebuild the projection dict; re-invoke the sim. Pre-trade totals stay frozen where they were.
