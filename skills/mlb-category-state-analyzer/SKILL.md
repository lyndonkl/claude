---
name: mlb-category-state-analyzer
description: Computes the weekly category state for a Yahoo H2H Categories matchup across all 10 scoring categories (R, HR, RBI, SB, OBP, K, ERA, WHIP, QS, SV). Pulls current totals from Yahoo, builds rest-of-week per-cat projections from roster + schedule, then DELEGATES matchup/per-cat win-probability math to `matchup-win-probability-sim`. Consumes the sim's `per_cat_win_probability` and `matchup_win_probability` to derive cat_position, cat_pressure, cat_reachability, and cat_punt_score, and emits a "push 6, punt N" plan that drives waiver, streaming, and lineup decisions. Use when user asks about "category state", "where am I winning", "should I punt", "matchup score", "cat pressure", weekly category planning, or which cats to push vs. concede.
---
# MLB Category State Analyzer

## Table of Contents
- [Example](#example)
- [Workflow](#workflow)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Example

**Scenario**: Week 3, K L's Boomers (Team 5) vs. Los Doyers. Wednesday AM (mid-week). 4 scoring days remain.

**Raw matchup scores (pulled from Yahoo matchup page)**:

| Cat | Us | Opp | Margin | Games left (us/opp) |
|---|---|---|---|---|
| R | 28 | 31 | -3 | 26 / 22 |
| HR | 9 | 7 | +2 | 26 / 22 |
| RBI | 30 | 29 | +1 | 26 / 22 |
| SB | 4 | 6 | -2 | 26 / 22 |
| OBP | .342 (82 PA) | .336 (78 PA) | +.006 | 26 / 22 GP |
| K | 42 | 38 | +4 | 9 SP starts / 7 SP starts |
| ERA | 3.80 (21 IP) | 4.12 (19 IP) | -0.32 (better) | 9 / 7 |
| WHIP | 1.18 (21 IP) | 1.25 (19 IP) | -0.07 (better) | 9 / 7 |
| QS | 2 | 1 | +1 | 9 / 7 |
| SV | 3 | 5 | -2 | ~8 RP days / ~8 RP days |

**Projections built for the sim** (rest-of-week `{mean, stddev}` — see [resources/methodology.md](resources/methodology.md#building-per-cat-projection-dicts)):

| Cat | Our projection | Opp projection |
|---|---|---|
| R | final 52 ± 9 | final 57 ± 8 |
| HR | final 15 ± 3.5 | final 13 ± 3.2 |
| RBI | final 52 ± 9 | final 55 ± 8 |
| SB | final 6 ± 2.3 | final 10 ± 2.5 |
| OBP | .346 ± .015 | .341 ± .014 |
| K | final 96 ± 11 | final 85 ± 10 |
| ERA | 3.88 ± 0.40 | 4.05 ± 0.45 |
| WHIP | 1.20 ± 0.07 | 1.25 ± 0.08 |
| QS | final 6.1 ± 1.5 | final 3.8 ± 1.4 |
| SV | final 4.8 ± 1.4 | final 7.7 ± 1.5 |

**Delegate to `matchup-win-probability-sim`** with:
- `cat_list = [R, HR, RBI, SB, OBP, K, ERA, WHIP, QS, SV]`
- `cat_inverse_list = [ERA, WHIP]`
- `cat_win_threshold = 6`
- `our_per_cat_projection` / `opp_per_cat_projection` from the table above
- `sim_mode = "monte_carlo"`, `n_simulations = 10000`, `random_seed = 42`

**Sim output (consumed by this skill)**:
- `matchup_win_probability = 0.58`
- `per_cat_win_probability`: R 0.36, HR 0.65, RBI 0.42, SB 0.16, OBP 0.60, K 0.74, ERA 0.62, WHIP 0.68, QS 0.85, SV 0.10
- `expected_cats_won = 5.18`

**Per-cat signals (derived here from sim output + baseball state — see [resources/methodology.md](resources/methodology.md#signal-formulas))**:

| Cat | Position (from state) | Pressure (state + pace) | Reachability (= round(100 × p_cat)) | Punt Score (= f(1 − p_cat) + volatility) | Verdict |
|---|---|---|---|---|---|
| R | losing | 72 | 36 | 44 | push (contested) |
| HR | winning | 48 | 65 | 21 | maintain |
| RBI | winning (thin) | 65 | 42 | 35 | push |
| SB | losing | 55 | 16 | 58 | evaluate punt |
| OBP | winning (thin) | 70 | 60 | 24 | push |
| K | winning | 55 | 74 | 16 | push |
| ERA | winning | 62 | 62 | 23 | push |
| WHIP | winning | 60 | 68 | 19 | maintain |
| QS | winning | 78 | 85 | 9 | push hard |
| SV | losing | 38 | 10 | 84 | punt |

**Overall recommendation**: **Push 6, maintain 2, punt 2.** Matchup win prob 58% (neutral favorite).

- **Push (6)**: HR, OBP, K, ERA, QS — each has `per_cat_win_probability ≥ 0.60`. Plus RBI as the contested-but-reachable 6th.
- **Maintain (2)**: WHIP (locked-ish), R (reachability lowish but not a true punt).
- **Punt (2)**: SB (p = 0.16, low reach) and SV (p = 0.10 + volatility bonus → punt score 84).

**Downstream implications for other agents**:
- Lineup optimizer: `matchup_win_probability = 0.58` → neutral-to-favorite, standard daily_quality optimization (no variance tilt).
- Waiver analyst: prioritize SP (QS, K, ERA), OBP-heavy bats; not closers or speed specialists.
- Streaming strategist: every QS-capable SP starts; skip any 5-inning risk arm.

## Workflow

Copy this checklist and track progress:

```
MLB Category State Analysis Progress:
- [ ] Step 1: Pull current matchup scores from Yahoo
- [ ] Step 2: Count remaining games/PAs/IP for both rosters
- [ ] Step 3: Build per-cat projection dicts ({mean, stddev}) for both rosters
- [ ] Step 4: Delegate to matchup-win-probability-sim (pass cat_list, projections, threshold=6, inverse=[ERA,WHIP])
- [ ] Step 5: Derive cat_position (from state), cat_pressure, cat_reachability, cat_punt_score from sim output
- [ ] Step 6: Rank cats and emit push/maintain/punt plan
- [ ] Step 7: Write signal file with YAML frontmatter (include matchup_win_probability from sim)
```

**Step 1: Pull current matchup scores**

Web-fetch the Yahoo matchup page: `https://baseball.fantasysports.yahoo.com/b1/23756/5/matchup?week=N`. Extract current totals for both teams in each of the 10 cats. For ratio cats (OBP, ERA, WHIP), also capture the denominator (PAs for OBP, IP for ERA/WHIP). This is **required** — you cannot build a ratio-cat projection without the volume underlying the ratio.

- [ ] 5 batting cats: R, HR, RBI, SB, OBP (+ at-bats / plate-appearances)
- [ ] 5 pitching cats: K, ERA, WHIP, QS, SV (+ innings pitched)
- [ ] Source URL cited in signal file

See [resources/methodology.md](resources/methodology.md#pulling-matchup-data-from-yahoo) for scrape procedure and fallback if Yahoo is unreachable.

**Step 2: Count remaining games/PAs/IP**

For each roster, count the number of MLB games its players will play for the rest of the scoring period, and project PAs (hitters) and IP (pitchers).

- [ ] Hitter games remaining: sum of (each rostered hitter's team games × probability they start)
- [ ] Pitcher starts remaining: number of scheduled SP starts for the rest of the week per roster
- [ ] Reliever days remaining: days × eligible RPs (for SV projection)
- [ ] Volume imbalance: if one team has meaningfully more games, that will show up directly in the projection means (and so in `per_cat_win_probability`)

Use MLB.com schedules + probable pitcher grids. See [resources/methodology.md](resources/methodology.md#projecting-remaining-games).

**Step 3: Build per-cat projection dicts**

For each team, build a dict `{cat: {mean, stddev}}` where `mean` is the projected **final** (or remaining, consistently used across both teams — pick one convention) and `stddev` reflects uncertainty given remaining volume.

- [ ] **Counting cats** (R, HR, RBI, SB, K, QS, SV): `mean = current_total + Σ(per-player per-game rate × games remaining × daily_quality)`. `stddev ≈ 0.35 × expected_remaining` as a default CV.
- [ ] **Ratio cats** (OBP, ERA, WHIP): `mean = (current_ratio × current_volume + projected_remaining_ratio × remaining_volume) / total_volume`. `stddev ≈ σ_per_obs / sqrt(total_volume)` — shrinks as total IP/PA grows.
- [ ] Both dicts have identical keys and the exact league `cat_list`.
- [ ] Use OBP (not AVG) and `qs_probability` (not W) from upstream `mlb-player-analyzer` signals — see Guardrails.

See [resources/methodology.md](resources/methodology.md#building-per-cat-projection-dicts).

**Step 4: Delegate to `matchup-win-probability-sim`**

Invoke the sibling skill with a well-formed input payload:

```
inputs to matchup-win-probability-sim:
  cat_list:           [R, HR, RBI, SB, OBP, K, ERA, WHIP, QS, SV]
  cat_inverse_list:   [ERA, WHIP]
  cat_win_threshold:  6
  our_per_cat_projection:  <dict from Step 3>
  opp_per_cat_projection:  <dict from Step 3>
  sim_mode:           "monte_carlo"
  n_simulations:      10000
  random_seed:        42
  tie_rule:           "half"

outputs consumed:
  matchup_win_probability  (float in [0,1])
  per_cat_win_probability  (dict[cat, float])
  expected_cats_won        (float)
  variance_estimate        (float)
```

- [ ] All 10 cats present in both projection dicts
- [ ] `cat_inverse_list = [ERA, WHIP]` (lower-is-better)
- [ ] `cat_win_threshold = 6` (Yahoo 10-cat majority)
- [ ] Seed passed for reproducibility
- [ ] Sim output fields captured and stored for Step 5

**Step 5: Derive per-cat signals from sim output + state**

Apply the formulas in [resources/methodology.md](resources/methodology.md#signal-formulas). The sim owns the probability math; this skill owns the baseball-state interpretation.

- [ ] `cat_position` ∈ {winning, tied, losing} — computed locally from **current totals** (not sim). Ratio-cat direction handled (OBP higher = winning; ERA/WHIP lower = winning).
- [ ] `cat_pressure` (0–100) — simple arithmetic from position + close-margin + volume-edge + locked-in flags. See pressure formula in Quick Reference.
- [ ] `cat_reachability` (0–100) — **now = round(100 × per_cat_win_probability[cat])**, taken directly from the sim.
- [ ] `cat_punt_score` (0–100) — `(100 × (1 − per_cat_win_probability[cat])) × 0.6 + 30 × is_volatile + 20 × below_min_threshold − 10 × has_spillover`, clamped.

**Step 6: Rank and emit plan**

Rank all 10 cats by `cat_pressure × cat_reachability / 100`:

- [ ] **Top 6**: push — mark these as priority for waivers, streams, starts
- [ ] **Middle 2**: maintain — hold position, don't overspend
- [ ] **Bottom 2**: evaluate punt — if `cat_punt_score > 60`, confirm punt; otherwise hold

Goal in H2H Cats is 6-of-10. A defensible plan is "push 6, concede up to 4." See [resources/template.md](resources/template.md#per-cat-signal-table) for the output signal format.

**Step 7: Write signal file**

Write to `signals/YYYY-MM-DD-cat-state.md` with YAML frontmatter (type: `cat-state`). Include `matchup_win_probability` from the sim as a top-level field. Validate with `mlb-signal-emitter` before persisting.

- [ ] All 10 cats present with all 4 signals each
- [ ] `matchup_win_probability` and `expected_cats_won` recorded in frontmatter
- [ ] `sim_meta` block (sim_mode, n_simulations, random_seed) recorded for reproducibility
- [ ] Confidence reflects data quality (lower if Yahoo scrape was partial)
- [ ] `source_urls` includes Yahoo matchup page + MLB.com schedule pages + a reference to the sim skill
- [ ] Red-team findings noted (e.g., "Opp has a two-start ace coming that could flip K + ERA + WHIP all at once")

Validate output using [resources/evaluators/rubric_mlb_category_state_analyzer.json](resources/evaluators/rubric_mlb_category_state_analyzer.json). Minimum: average score of 3.5 or above.

## Common Patterns

**Pattern 1: Balanced mid-week state**
- Typical Wednesday AM state: 3-4 cats already locked, 3-4 close, 2-3 volatile.
- Action: push the close cats hardest, coast the locked wins, ignore locked losses.
- The sim's per-cat probs already reflect this — cats with `p ∈ [0.40, 0.65]` are the contested ones.

**Pattern 2: Volume-imbalanced matchup**
- We have 30 hitter games left, opp has 22. Our counting-cat projection means rise; sim's `per_cat_win_probability` for R/HR/RBI/SB rises accordingly.
- Action: stack the lineup (fewer off-days, prefer teams playing doubleheaders), bid on streamers. Pressure boost comes from the volume-edge flag, reachability boost comes automatically from the sim.

**Pattern 3: Two-start ace incoming (us or them)**
- One pitcher's two-start week can swing K, ERA, WHIP, QS simultaneously.
- Encode this in the projection dict: their expected IP and K rise, ERA/WHIP means improve (toward their ERA/WHIP), QS mean rises by ~0.45 per expected QS-quality start.
- The sim then shows 4 pitching cats moving together in `per_cat_win_probability` deltas.

**Pattern 4: Save-category volatility**
- SVs are low-frequency; one walkoff blown save flips the category.
- In the projection dict, use a low mean (≤ 2.5/week per locked closer) and moderate stddev (≥ 1.2). The sim will naturally report `per_cat_win_probability` near 0.1–0.25 when behind by 2+.
- The +30 volatility bonus in `cat_punt_score` (applied here, not in the sim) pushes SV to punt when sim reachability agrees.

**Pattern 5: Ratio-cat "freeze"**
- Late in the week, if opp is far below the IP/PA minimum (e.g., has 9 IP on Friday with no more starts), their ratio cats are locked at whatever they have.
- Encode by setting opp ratio-cat stddev near zero and their mean at a punitive-or-forfeited value. The sim then returns `per_cat_win_probability ≈ 1.0` for those cats.

## Guardrails

1. **Never compute OBP/ERA/WHIP from rates alone — always include volume (PA/IP).** A .400 OBP in 10 PAs is not better than .342 in 82 PAs. The projection-dict mean/stddev for ratio cats must come from the weighted-average formula; the sim takes those as truth.

2. **QS is the #1 category, not Wins.** This league uses Quality Starts (6+ IP, ≤3 ER). A 5-inning outing scores zero. When projecting remaining QS, multiply each SP start by its QS probability (from `mlb-player-analyzer`'s `qs_probability` signal) — don't just count scheduled starts.

3. **OBP is the #5 category, not AVG.** Walks count. When projecting OBP contribution, use players' OBP (not AVG). A high-BB, low-AVG player like Juan Soto is worth more in this league than his raw hit rate suggests.

4. **SV is volatile — trust the punt when signals agree.** Unlike counting batting cats, a 2-save deficit with 3 days left has low `per_cat_win_probability` regardless of roster. Don't fight for saves if the closer role on your roster isn't locked (check `save_role_certainty` < 70 → automatic punt candidate). The volatility bonus in `cat_punt_score` is applied **here**, not in the sim — the sim returns raw probability.

5. **`cat_reachability` comes from the sim — don't recompute.** This is a delegation. If the sim returns `per_cat_win_probability[R] = 0.36`, then `cat_reachability[R] = 36`. Do not apply z-score shortcuts or best/worst-case buckets here — those lived in the old heuristic and are now owned by the sim skill.

6. **Locked-in cats get pressure adjustments, not zero.** A locked-in win still has `cat_pressure ≈ 40` (it's banked). A locked-in loss still has `cat_pressure ≈ 20` (stop investing). Don't set them to zero — downstream agents use non-zero values to decide bench vs. drop.

7. **Ratio cats need the minimum-IP/PA rule.** Yahoo enforces minimums for pitcher ratio cats (usually 20 IP for the week). If either roster is tracking below the minimum late in the week, the ratio cat may auto-loss. Encode this in the projection dict (stddev → 0, mean → punitive) before calling the sim, AND add +20 `below_min_threshold` to `cat_punt_score`.

8. **Never re-derive upstream signals.** `qs_probability`, `sb_opportunity`, `obp_contribution`, `save_role_certainty` come from `mlb-player-analyzer`. Read them from the signal directory; do not recompute.

9. **Always pass a `random_seed` to the sim.** Without it, two runs of this skill produce slightly different `cat_reachability` values, which will confuse downstream agents doing diff comparisons. Default seed: `42`.

## Quick Reference

**Where the math lives now:**

| Signal | Owner | Formula |
|---|---|---|
| `cat_position` | this skill | enum from current totals (ratio-direction aware) |
| `cat_pressure` | this skill | baseline 50 + 20 × close + 15 × vol-edge − 10 × locked_win − 30 × locked_loss |
| `cat_reachability` | **delegated to `matchup-win-probability-sim`** | = round(100 × `per_cat_win_probability[cat]`) |
| `cat_punt_score` | this skill (uses sim output) | (100 × (1 − p_cat)) × 0.6 + 30 × volatile + 20 × below_min − 10 × spillover |
| `matchup_win_probability` | **delegated to `matchup-win-probability-sim`** | Monte Carlo P(cats_won ≥ 6) |

```
cat_pressure =
    50                                         # neutral baseline
  + 20 × (is_close_margin: deficit/lead ≤ 10% of total)
  + 15 × (opponent_volume_exhausted: we have more games left)
  - 10 × (locked_in_win)
  - 30 × (locked_in_loss)
  clamp(0, 100)

cat_reachability = round(100 × per_cat_win_probability[cat])   # from sim

cat_punt_score =
    (100 - cat_reachability) × 0.6                      # base: if we can't reach, consider punting
  + 30 × (cat is traditionally volatile: SV)
  + 20 × (below min-PA/IP threshold)
  - 10 × (cat has spillover: K→QS, OBP→R, HR→R+RBI)
  clamp(0, 100)
```

**League constants (from `context/league-config.md`):**

- 10 cats: **R, HR, RBI, SB, OBP, K, ERA, WHIP, QS, SV**
- Inverse cats: **ERA, WHIP** (lower-is-better — passed as `cat_inverse_list` to the sim)
- OBP (not AVG) — walks matter
- QS (not W) — 6+ IP with ≤3 ER
- H2H Cats, goal = win 6+ of 10 each week (`cat_win_threshold = 6`)
- Daily lineup lock; weekly matchup rolls Mon-Sun

**Signal file output schema (from `context/frameworks/signal-framework.md`):**

```yaml
---
type: cat-state
date: YYYY-MM-DD
emitted_by: mlb-category-state-analyzer
week: N
matchup_opponent: <team name>
scoring_days_remaining: N
matchup_win_probability: 0.58          # from matchup-win-probability-sim
expected_cats_won: 5.18                # from matchup-win-probability-sim
sim_meta:
  sim_mode: monte_carlo
  n_simulations: 10000
  random_seed: 42
synthesis_confidence: 0.0-1.0
source_urls:
  - https://baseball.fantasysports.yahoo.com/b1/23756/5/matchup?week=N
---
```

Body: per-cat table + overall push/maintain/punt recommendation + red-team findings.

**Thresholds used downstream:**

| Agent | Threshold | Effect |
|---|---|---|
| Waiver analyst | `cat_pressure ≥ 60` | Prioritize targets that fill that cat |
| Streaming strategist | `cat_pressure (ERA/WHIP) < 30` | Allow riskier streamers (we're punting) |
| Lineup optimizer | `matchup_win_probability < 0.4` / `> 0.6` | Variance-seek as underdog / damp as favorite |
| Trade analyzer | weights `trade_cat_delta` | Multiplied by `cat_pressure / 50` |

**Key resources:**

- **[resources/template.md](resources/template.md)**: Output signal file format, per-cat table, sim-integration worked example
- **[resources/methodology.md](resources/methodology.md)**: Yahoo scrape procedure, remaining-games projection, building per-cat projection dicts, sim-integration formulas
- **[resources/evaluators/rubric_mlb_category_state_analyzer.json](resources/evaluators/rubric_mlb_category_state_analyzer.json)**: Evaluator rubric
- **Sibling skill: `matchup-win-probability-sim`** — owns per-cat and matchup-level win-probability math via Monte Carlo / Poisson-binomial

**Inputs required:**

- Current matchup scores (10 cats, both teams, with volume for ratio cats)
- Roster IDs for both teams
- Remaining MLB schedule through Sunday
- Upstream signals: `qs_probability`, `save_role_certainty`, `obp_contribution`, `sb_opportunity`, `daily_quality`
- League config (cats list, min-IP/PA thresholds, `cat_win_threshold`)

**Outputs produced:**

- `signals/YYYY-MM-DD-cat-state.md` — signal file with 10-cat table, overall plan, `matchup_win_probability`, confidence, source URLs
- `cat_position`, `cat_pressure`, `cat_reachability`, `cat_punt_score` per cat
- Overall "push N, maintain M, punt P" recommendation (N + M + P = 10, target N ≥ 6)
- `matchup_win_probability` (from sim delegate) for lineup-optimizer variance decisions
