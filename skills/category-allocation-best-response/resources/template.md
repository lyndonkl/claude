# Category Allocation Best-Response — Template

## Input Schema

```yaml
our_per_cat_capacity:
  # dict[cat, number] -- our projected per-cat output for the matchup window
  # Must cover every cat in cat_win_threshold's implied list.
  R: 42
  HR: 12
  # ...

opp_per_cat_projection:
  # dict[cat, number] -- opponent's projected per-cat output for the same window.
  R: 38
  HR: 14
  # ...

per_cat_win_probability:
  # dict[cat, float in [0, 1]] -- FROM matchup-win-probability-sim.
  # This is the critical upstream signal. Do not compute by eye.
  R: 0.64
  HR: 0.35
  # ...

cat_win_threshold:
  # int -- 6 for MLB 10-cat, 5 for NBA 9-cat, 6 for NHL 10-cat.
  # Must match the league format exactly.
  value: 6

resources_available:
  # dict[resource_type, number] -- what we can deploy this week.
  # Unused resources are fine; downstream skills may consume leverage weights
  # even if no roster moves are planned.
  roster_slots: 5
  faab: 80
  streamer_starts: 3

inverse_cats:
  # list[cat] -- cats where lower is better. Upstream matchup-win-probability-sim
  # has already applied inverse handling to per_cat_win_probability; this field
  # is documentation only and does not affect classification.
  - ERA
  - WHIP
```

## Output Schema

```yaml
pushed_cats:
  # list[cat] -- cats with per_cat_win_probability in [0.70, 0.85],
  # ordered by win prob descending.
  - SB
  - QS
  - WHIP
  - ERA
  # ...

conceded_cats:
  # list[cat] -- cats with per_cat_win_probability < 0.25 (dominated strategies).
  # Leverage 0.0. Do not spend resources here.
  - SV

contested_cats:
  # list[cat] -- cats with per_cat_win_probability in [0.25, 0.70).
  # Highest marginal leverage. This is where contested-cat plays live.
  - HR
  - RBI

leverage_weights:
  # dict[cat, float] in {0.0, 1.0, 1.2, 1.5}.
  # Downstream lineup / streaming / waiver skills multiply daily_quality
  # by leverage to get competitive score.
  R: 1.2
  HR: 1.5
  RBI: 1.5
  SB: 1.2
  OBP: 1.2
  K: 1.2
  ERA: 1.2
  WHIP: 1.2
  QS: 1.2
  SV: 0.0

k_of_n_win_probability:
  # float in [0, 1] -- P(win >= K of N cats) under this allocation,
  # computed via Poisson-binomial recurrence over per_cat_win_probability.
  value: 0.605

rationale:
  # 2-4 sentences of plain-English allocation logic.
  # Must name at least one conceded cat and one contested cat.
  # If k_of_n_win_probability < 0.40, flag variance-pivot.
  text: |
    SV is conceded (8% flip probability) -- do not spend a reliever slot on a
    pure-SV arm. The 7 pushed cats (SB, QS, WHIP, ERA, K, R, OBP) defend the
    6-cat threshold on median. The two contested cats (HR, RBI) are where
    marginal resources flip the matchup -- one power bat from waivers lifts
    both simultaneously. Computed k_of_n_win_probability = 0.605.
```

## Worked Example 1: MLB H2H 10-cat (Yahoo 5x5)

**Scenario**: Week 8, our team vs a closer-heavy opponent with 5 projected SV. Threshold = 6.

**Inputs** (abbreviated):

| Cat | our_capacity | opp_projection | per_cat_win_prob |
|-----|--------------|----------------|------------------|
| R | 42 | 38 | 0.64 |
| HR | 12 | 14 | 0.35 |
| RBI | 40 | 41 | 0.47 |
| SB | 6 | 4 | 0.72 |
| OBP | 0.335 | 0.328 | 0.64 |
| K | 55 | 50 | 0.64 |
| ERA | 3.85 | 4.10 | 0.65 |
| WHIP | 1.22 | 1.28 | 0.68 |
| QS | 4 | 3 | 0.69 |
| SV | 2 | 5 | 0.08 |

`cat_win_threshold`: 6. `inverse_cats`: `[ERA, WHIP]`. `resources_available`: `{roster_slots: 5, faab: 80, streamer_starts: 3}`.

**Classification**:

| Cat | Win Prob | Bucket | Leverage |
|-----|----------|--------|----------|
| SV | 0.08 | conceded | 0.0 |
| HR | 0.35 | contested | 1.5 |
| RBI | 0.47 | contested | 1.5 |
| R | 0.64 | pushed | 1.2 |
| OBP | 0.64 | pushed | 1.2 |
| K | 0.64 | pushed | 1.2 |
| ERA | 0.65 | pushed | 1.2 |
| WHIP | 0.68 | pushed | 1.2 |
| QS | 0.69 | pushed | 1.2 |
| SB | 0.72 | pushed | 1.2 |

**Threshold check**: `pushed + contested = 9 cats >= 6` — satisfied.

**Poisson-binomial computation** (per-cat probs `[0.64, 0.35, 0.47, 0.72, 0.64, 0.64, 0.65, 0.68, 0.69, 0.08]`, threshold 6):

`k_of_n_win_probability = 0.605`

**Outputs**:

- `pushed_cats`: `[SB, QS, WHIP, ERA, K, R, OBP]`
- `conceded_cats`: `[SV]`
- `contested_cats`: `[HR, RBI]`
- `leverage_weights`: `{R: 1.2, HR: 1.5, RBI: 1.5, SB: 1.2, OBP: 1.2, K: 1.2, ERA: 1.2, WHIP: 1.2, QS: 1.2, SV: 0.0}`
- `k_of_n_win_probability`: `0.605`
- `rationale`: *"SV is conceded against a closer-heavy opponent — a reliever slot is strictly worse than redeploying to a power bat. 7 pushed cats defend the 6-cat threshold; the two contested cats (HR, RBI) carry the 1.5x leverage, so the best move is one FAAB bid on a power bat (~$20) who contributes ~3 HR and ~10 RBI per week."*

## Worked Example 2: NBA H2H 9-cat

**Scenario**: Week 12 of NBA H2H 9-cat. Threshold = 5 of 9. Our team has an elite shooter (high 3PM, high FT%) but a FG%-poor center rotation. Opponent runs a FT%-punt Giannis-style roster.

**Inputs**:

| Cat | our_capacity | opp_projection | per_cat_win_prob | Inverse? |
|-----|--------------|----------------|------------------|----------|
| PTS | 650 | 640 | 0.55 | no |
| REB | 280 | 330 | 0.25 | no |
| AST | 180 | 170 | 0.60 | no |
| STL | 45 | 42 | 0.58 | no |
| BLK | 35 | 50 | 0.18 | no |
| 3PM | 85 | 65 | 0.82 | no |
| FG% | 0.455 | 0.485 | 0.22 | no |
| FT% | 0.815 | 0.680 | 0.92 | no |
| TO | 85 | 80 | 0.45 | yes |

`cat_win_threshold`: 5. `inverse_cats`: `[TO]`. `resources_available`: `{roster_slots: 3, streamer_games: 12}`.

**Classification**:

| Cat | Win Prob | Bucket | Leverage |
|-----|----------|--------|----------|
| BLK | 0.18 | conceded | 0.0 |
| FG% | 0.22 | conceded | 0.0 |
| REB | 0.25 | contested (boundary) | 1.5 |
| TO | 0.45 | contested | 1.5 |
| PTS | 0.55 | contested | 1.5 |
| STL | 0.58 | contested | 1.5 |
| AST | 0.60 | contested | 1.5 |
| 3PM | 0.82 | pushed | 1.2 |
| FT% | 0.92 | locked | 1.0 |

**Threshold check**: `pushed + contested = 6 cats >= 5` — satisfied. (Plus `FT%` locked = 1 guaranteed win.)

**Note on borderline**: `REB = 0.25` sits exactly at the classification boundary. Convention: closed-open intervals — `[0.25, 0.70)` is contested, so `REB` goes into `contested_cats` with leverage 1.5. If `REB` had been `0.24`, it would be conceded with a possible upgrade (in the `[0.20, 0.25)` band).

**Note on upgrade consideration**: `FG% = 0.22` is in the upgrade band `[0.20, 0.25)`. But we already have 6 non-conceded cats vs a 5-cat threshold, so Step 4 is satisfied and we do not upgrade FG%. Resources are better spent on the five contested cats.

**Poisson-binomial**: `k_of_n_win_probability = 0.706`.

**Outputs**:

- `pushed_cats`: `[3PM]`
- `conceded_cats`: `[FG%, BLK]`
- `contested_cats`: `[AST, STL, PTS, TO, REB]`
- `leverage_weights`: `{PTS: 1.5, REB: 1.5, AST: 1.5, STL: 1.5, BLK: 0.0, 3PM: 1.2, "FG%": 0.0, "FT%": 1.0, TO: 1.5}`
- `k_of_n_win_probability`: `0.706`
- `rationale`: *"FG% and BLK are conceded against this roster shape — the FT%-punt opponent runs Giannis-type bigs who dominate BLK and FG%, and no marginal move flips either. FT% is locked (0.92). The leverage action is across the 5 contested cats (AST, STL, PTS, TO, REB); a streamer start on a low-TO guard moves three contested cats simultaneously. Computed k_of_n_win_probability = 0.706."*

## Rationale Template

The rationale field should follow this structure (2–4 sentences):

1. **Sentence 1**: Name the conceded cats and the reason (`"X is conceded because..."` or `"X and Y are dominated strategies against this opponent shape"`).
2. **Sentence 2**: Name the contested cats and the highest-leverage resource move (`"The leverage action is on contested cats A, B; one roster add on a C-type player lifts both"`).
3. **Sentence 3 (optional)**: Note any borderline upgrade (`"Upgrading Z from conceded: spend 1 slot + $15 FAAB on a power bat"`).
4. **Sentence 4 (optional, if `k_of_n_win_probability < 0.40`)**: Variance-pivot flag (`"Presumptive underdog (38% win prob) — flagging for variance-strategy-selector"`).

**Do not**:

- List all categories in the rationale (the structured fields already carry that info).
- Include numeric weights in prose (they belong in `leverage_weights`).
- Recommend specific players (downstream waiver/FAAB skills handle that).

## Resource Allocation Recipes (by bucket)

| Bucket | Where resources go | Where they do NOT go |
|--------|-------------------|---------------------|
| `conceded` | Nowhere. Leverage 0.0 is a hard constraint. | Not here. |
| `contested` | First priority. Roster slots, FAAB dollars, streamer starts. One unit of resource here moves win probability ~2–3x more than the same unit on a `pushed` cat. | Do not dump entire budget — marginal curve flattens. |
| `pushed` | Second priority. Defensive adds, injury backfills. | Do not over-invest — these should hold with ordinary care. |
| `locked` | Minimal. Default leverage 1.0 means no premium. | Do not spend FAAB to pad a locked cat. |

## Cross-Sport Parameter Reference

| Sport | N | K | Inverse cats | Typical concedes |
|-------|---|---|--------------|------------------|
| MLB 5x5 (Yahoo) | 10 | 6 | ERA, WHIP | SV (vs closer-heavy), SB (vs power), QS (vs RP-only) |
| NBA 9-cat | 9 | 5 | TO | FT% (vs big-man rosters), 3PM (vs traditional rosters), BLK (vs perimeter rosters) |
| NHL 10-cat | 10 | 6 | GAA | SO, PIM, +/- (all high-variance lottery cats) |
| Generic K-of-N | N | K | per league | depends on opponent shape |
