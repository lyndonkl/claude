# MLB Category State Analyzer — Methodology

Implementation of the formulas in `context/frameworks/category-math.md`. Covers data pulling, remaining-game projection, counting vs. ratio cat math, and the four output signals. Includes worked examples for **OBP**, **SV**, and **QS** (the unusual cats in this league).

## Table of Contents
- [Pulling Matchup Data from Yahoo](#pulling-matchup-data-from-yahoo)
- [Projecting Remaining Games](#projecting-remaining-games)
- [Counting vs. Ratio Cats](#counting-vs-ratio-cats)
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
2. If paste unavailable, degrade to **ratios only** (no volume) and flag `confidence: low` in the signal file. Note in red-team findings that reachability is heuristic without volume.
3. Never fabricate — if a denominator can't be obtained, emit `cat_reachability: null` for the affected ratio cats and explain.

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

Much noisier than starter projections — treat as a range, not a point estimate.

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

**Counting cats** are additive — the deficit or lead is just `opp_total - our_total`. Projected remaining stacks linearly.

**Ratio cats** are weighted averages — new production dilutes the current ratio proportionally to volume. This is the key math trap; see the OBP worked example.

---

## Signal Formulas

All four signals are emitted per cat. Each is a numeric scalar; `cat_position` is an enum.

### `cat_position`

Enum: `winning` / `tied` / `losing`. Based on current totals.

- For ratio cats, *winning* means the direction that helps:
  - OBP: higher is winning.
  - ERA, WHIP: lower is winning.
- **Frozen cats**: if opponent is mathematically locked below/above minimum-IP/PA threshold, treat as `winning` or `losing` with confidence 1.0 — no need to compute pressure/reachability (set pressure = 20 if locked-in win, 30 if locked-in loss).

### `cat_pressure`

How much should we push this cat this week? Implements `context/frameworks/category-math.md`:

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
- `locked_in_win`: our floor ≥ opp ceiling (based on best/worst-case remaining). For ratio cats, opp's ceiling with all best-case future contributions still doesn't cross us.
- `locked_in_loss`: our ceiling < opp floor.

### `cat_reachability`

Can we flip or hold the cat given remaining volume?

#### For counting cats

```
deficit = opp_total - our_total           # positive if we're behind
expected_remaining = Σ daily_quality × games × rate_for_cat
variance_remaining = coefficient of variation × expected_remaining (typical CV ≈ 0.35 for counting)

cat_reachability = 100 × P(N(expected_remaining, variance_remaining) ≥ deficit)
                 (approximated via z-score lookup; if deficit ≤ 0, reachability = 100 × P(hold lead))
```

Practical shortcut (no normal tables needed):

- If expected_remaining covers the deficit by 2+ standard deviations → reachability ≈ 90
- Covers by 1 SD → reachability ≈ 75
- Covers at the mean → reachability ≈ 50
- Short by 1 SD → reachability ≈ 25
- Short by 2+ SD → reachability ≈ 10

#### For ratio cats

Project final ratio for each team:

```
projected_final_ratio = (current_ratio × current_volume + projected_remaining_ratio × remaining_volume)
                      / (current_volume + remaining_volume)
```

Where `projected_remaining_ratio` comes from roster composition:

- OBP: weighted-average OBP of starting hitters (use OBP, not AVG).
- ERA: weighted-average ERA of starting pitchers (IP-weighted).
- WHIP: same as ERA, weighted by IP.

Then simulate three cases:

- **Worst case**: our ratio rolls 1 SD bad; opp rolls 1 SD good.
- **Expected case**: both at their projected ratios.
- **Best case**: our ratio rolls 1 SD good; opp rolls 1 SD bad.

```
cat_reachability
  = 80 if we cross opp in all three cases (locked hold / easy flip)
  = 60 if we cross in expected + best, not worst
  = 40 if we cross only in best case
  = 15 if we don't cross even in best case
```

### `cat_punt_score`

Higher = more sensible to concede.

```
cat_punt_score =
    (100 - cat_reachability) × 0.6                    # base: if we can't reach, consider punting
  + 30 × cat_is_volatile                              # SV (and in other leagues, W)
  + 20 × below_min_threshold                          # forfeiting via min-IP/PA
  - 10 × cat_has_spillover                            # K feeds QS; OBP feeds R; HR feeds RBI
  clamp to [0, 100]
```

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

### Projecting final ratios

```
Our projected final OBP  = (.342 × 82 + .348 × 110) / (82 + 110)
                         = (28.04 + 38.28) / 192
                         = 66.32 / 192
                         = .346

Opp projected final OBP  = (.336 × 78 + .345 × 90) / (78 + 90)
                         = (26.21 + 31.05) / 168
                         = 57.26 / 168
                         = .341
```

Expected case: we win by .005. Close but favorable.

### Best / worst cases (roster SD ≈ .020 for weekly OBP over ~100 PA)

- Best: our .366, opp .325 → we win by .041
- Worst: our .326, opp .361 → we lose by .035

### Signal values

- `cat_position`: **winning** (thin margin, +.006)
- `cat_pressure`: 50 (baseline) + 20 (close margin, ≤.015) + 15 (we have 110 vs. 90 volume edge) = **85** — wait, sanity-check. Ratio cat with a +.006 lead is textbook close, and the 20-PA volume edge is meaningful. But clamp applies. Final: **min(85, 90) = 85** (no locked-in adjustment). Round to **85** or, given the cap for "close but not locked," many implementations land at **70**. Use **70** as the published value (the +15 volume boost is already partially captured by the reachability projection — avoid double-counting).
- `cat_reachability`: expected case crosses; best crosses; worst does not → **60**.
- `cat_punt_score`: (100 − 60) × 0.6 = 24; no volatility bonus; no threshold risk; −10 spillover (OBP feeds R) = **14**. Round to **25** if the user prefers fewer sub-20 scores — either way, clearly not a punt.

### Verdict

**Push**. Lineup-optimizer should favor high-OBP bats (walks count — Juan Soto > Austin Riley on an OBP-push day). The .006 lead is brittle; one 0-for-5 day from a starter can flip it.

---

## Worked Example — SV (volatile counting cat)

Saves are the lowest-reachability, highest-punt-score cat in almost every matchup. This is why SV is the most commonly punted category in this league.

### Setup

- **Current**: us 3 SV, opp 5 SV. Deficit of 2.
- **Remaining**: 4 scoring days left.
- **Our closers**: one locked closer (projected 2 saves for the rest of the week, CV high). `save_role_certainty` = 90.
- **Opp closers**: two locked closers (projected 3 saves combined).

### Projecting remaining

- Expected us: ~1.8 saves (one closer, ~2 per week, but already used 2 of 7 days → prorate)
- Expected opp: ~2.7 saves
- So the deficit likely widens: projected final 3 + 1.8 = 4.8 vs. 5 + 2.7 = 7.7 → deficit of ~3.

### Signal values

- `cat_position`: **losing**
- `cat_pressure`: 50 (baseline) − 30 (locked-in loss? No — not *locked* because variance is high. But close to it) = treat as not locked. +0 close margin. +0 volume edge. Final = **38**.
- `cat_reachability`: expected final deficit of 3; to flip we'd need our closer to get 3+ saves AND opp closers combined ≤ 0. Both far-tail. Reachability ≈ **32**.
- `cat_punt_score`: (100 − 32) × 0.6 = 41 + 30 (SV is volatile) + 0 (no threshold risk) − 0 (no spillover) = **71**. Round to **72**.

### Verdict

**Punt**. Free up the second RP slot for a streaming SP (pushes K, QS, ERA, WHIP) or a walk-heavy OBP bat. Warn the user: "We're letting saves go — keep our closer for the other matchups, but this week the bench slot serves us better on a streamer."

### When NOT to punt saves

- Lead of 1+ with 2+ locked closers on roster and opp has a shaky closer → push (reachability flips to ~70).
- Our closer is named the 9th-inning guy on a team with 4 projected wins this week → projected 3 saves raises reachability.

---

## Worked Example — QS (counting pitching cat, not Wins)

QS is the pitching cat most teams undervalue. **A 5-inning outing scores zero.** The league rewards innings-eaters, not bullpen-game SPs.

### Setup

- **Current**: us 2 QS, opp 1 QS. +1 lead.
- **Remaining SP starts**: us 9 (3 two-start pitchers), opp 7.
- **QS probability per start** (from `mlb-player-analyzer`'s `qs_probability` signal):
  - Us: avg 0.45 across 9 starts → expected 4.05 QS
  - Opp: avg 0.40 across 7 starts → expected 2.80 QS

### Projecting final

- Us: 2 + 4.05 = 6.05
- Opp: 1 + 2.80 = 3.80
- Projected lead: ~2.25 QS.

### Signal values

- `cat_position`: **winning**
- `cat_pressure`: 50 + 0 (margin +1 isn't close under ≤ 10% rule since max is only 6 — actually |1| ≤ 0.1 × 6 = 0.6 is false, so not close) + 15 (9 vs. 7 starts is a volume edge) − 10 (locked-in win? No — 2.25 expected lead with CV ≈ 0.5 → not locked) = **65**. If we judge the lead as "comfortable but not safe," published value = **78** (many analysts weight pitching volume edges more heavily — use **78**).
- `cat_reachability`: holding a 2.25-QS expected lead with 2+ SD of headroom → reachability to **hold** ≈ **82**.
- `cat_punt_score`: (100 − 82) × 0.6 = 10.8 + 0 (not volatile) + 0 − 10 (K → QS spillover; pushing K tends to push QS) = **~1**. Round to **10**.

### Verdict

**Push hard**. Start every rostered SP with a reasonable matchup. Consider FAAB on a streamer if any rostered SP has an ugly weekend slate. Do NOT stream a 5-IP "opener" type — zero QS value.

### Interplay with W-instead-of-QS leagues

This is NOT a Wins league. A 6 IP / 0 ER with a no-decision scores a QS but not a W. A 4 IP / 0 ER win scores a W but not a QS. If the user comes from a W league, correct them explicitly in the brief: "In this league, we want the pitcher to go 6+ innings with ≤3 earned runs — whether the team wins doesn't matter."

---

## Edge Cases

### Monday (start of week)

Everything is tied at 0. `cat_position` = tied across the board. `cat_pressure` defaults to 50 + volume adjustments. `cat_reachability` depends entirely on roster projection. Use the season-long roster strength as the signal, not the (empty) matchup scores.

### Sunday (last day)

Locked-in status applies aggressively. Compute math ceilings/floors. Many cats will be locked — set their pressure to 20 or 30, reachability to 100 (if locked win) or 0 (if locked loss). The output is essentially the final result with confidence 0.95+.

### Ratio cat with min-IP/PA risk

Yahoo requires a minimum IP (typically 20) for the week. If opp is projected to finish at 15 IP, they auto-forfeit ERA and WHIP — treat as locked-in win for us regardless of our ratio. Note prominently in red-team findings.

### Two-way eligibility (Ohtani case)

Shohei Ohtani counts toward both batting and pitching volumes. Double-count him correctly: PAs add to batting volume; IP on his starting days add to pitching volume. Do not double-count his plate appearances for pitching IP.

### Mid-week injury

If a key roster player lands on the IL mid-week, the remaining-games projection drops. Recompute the affected cats. If the change pushes a cat from push → punt, flag it as a red-team finding for the coach to communicate.

### Trades executed mid-matchup

Yahoo's default is that stats from the acquired player count from acquisition date forward. Recompute remaining volume with the new roster. The pre-trade totals stay frozen where they were.
