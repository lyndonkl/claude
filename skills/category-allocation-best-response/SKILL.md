---
name: category-allocation-best-response
description: Computes the best-response allocation of roster resources across categories in a Head-to-Head Categories matchup. Given our per-category capacity, the opponent's projected output, per-category win probabilities (from matchup-win-probability-sim), and a K-of-N winning threshold, classifies categories into pushed / contested / conceded buckets, emits per-category leverage weights for downstream lineup and streaming decisions, computes the resulting K-of-N win probability, and writes a plain-English rationale. Domain-neutral — portable to any fantasy sport with H2H Cats scoring (MLB 10-cat, NBA 9-cat, NHL 10-cat). Use when you need push/punt decisions, dominated-strategy elimination, leverage weights per cat, or best-response allocation; or when the user mentions "category allocation", "push or punt", "K of N cats", "dominated strategy elimination", "best response allocation", "Blotto fantasy", "leverage weights per cat", or "which cats to push".
---
# Category Allocation Best-Response

## Table of Contents
- [Example](#example)
- [Workflow](#workflow)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Example

**Scenario**: Yahoo MLB 10-category H2H, Week 8. Threshold = 6 of 10. Upstream `matchup-win-probability-sim` returned `per_cat_win_probability` for the current week. Our resources: 5 open roster slots, $80 FAAB, 3 streamer starts.

**Inputs**:

| Cat | our_capacity | opp_projection | per_cat_win_prob | Inverse? |
|-----|--------------|----------------|------------------|----------|
| R | 42 | 38 | 0.64 | no |
| HR | 12 | 14 | 0.35 | no |
| RBI | 40 | 41 | 0.47 | no |
| SB | 6 | 4 | 0.72 | no |
| OBP | 0.335 | 0.328 | 0.64 | no |
| K | 55 | 50 | 0.64 | no |
| ERA | 3.85 | 4.10 | 0.65 | yes |
| WHIP | 1.22 | 1.28 | 0.68 | yes |
| QS | 4 | 3 | 0.69 | no |
| SV | 2 | 5 | 0.08 | no |

**Classification by win probability**:

- SV (0.08): `conceded` — dominated strategy. Opponent has 5 projected SV to our 2; no marginal roster slot flips this. Leverage = 0.
- HR (0.35): `contested` — borderline-losing but within reach. Leverage = 1.5.
- RBI (0.47): `contested` — coin-flip. Leverage = 1.5.
- R (0.64), OBP (0.64), K (0.64), ERA (0.65), WHIP (0.68), QS (0.69): `pushed` (lock-in needs attention, 0.25–0.85). Leverage = 1.2. (0.70 is the boundary — one of these would sit on the `contested` side at 1.5 if very close to the line.)
- SB (0.72): `pushed`. Leverage = 1.2.

No cat exceeds 0.85 on this week; no cats are `locked`.

**Outputs**:

- `pushed_cats`: `[SB, QS, WHIP, ERA, K, R, OBP]` (7 cats at 0.64–0.72, ordered by win prob descending)
- `conceded_cats`: `[SV]`
- `contested_cats`: `[HR, RBI]`
- `leverage_weights`: `{R: 1.2, HR: 1.5, RBI: 1.5, SB: 1.2, OBP: 1.2, K: 1.2, ERA: 1.2, WHIP: 1.2, QS: 1.2, SV: 0.0}`
- `k_of_n_win_probability`: **0.605** (Poisson-binomial over the 10 per-cat probabilities with threshold 6)
- `rationale`: *"SV is a dominated strategy (8% flip probability) — do not spend a reliever slot. The 7 pushed cats cover the 6-cat threshold on median, so lock them in and invest marginal resources into HR and RBI (contested, 1.5x leverage) where one extra power bat can flip the matchup."*

Interpretation: if we simply defend the 7 pushed cats we hit threshold in expectation. The contested cats (HR, RBI) are where the highest-leverage moves live — every marginal HR or RBI unit maps almost 1-for-1 to matchup win probability.

## Workflow

Copy this checklist and track progress:

```
Category Allocation Best-Response Progress:
- [ ] Step 1: Validate inputs and confirm upstream signals
- [ ] Step 2: Classify each cat by per_cat_win_probability
- [ ] Step 3: Assign leverage_weights
- [ ] Step 4: Check threshold satisfaction (pushed + contested >= K?)
- [ ] Step 5: Apply borderline-upgrade logic if threshold not met
- [ ] Step 6: Compute k_of_n_win_probability via Poisson-binomial
- [ ] Step 7: Write rationale and emit outputs
```

**Step 1: Validate inputs and confirm upstream signals**

`per_cat_win_probability` is the critical upstream dependency and must come from `matchup-win-probability-sim` (or an equivalent simulator). Do not invent per-cat probabilities from raw capacity vs projection — `matchup-win-probability-sim` accounts for variance, and variance is what determines flip probability for contested cats. See [resources/methodology.md](resources/methodology.md#upstream-dependency-on-matchup-win-probability-sim).

- [ ] Every cat appears in `our_per_cat_capacity`, `opp_per_cat_projection`, and `per_cat_win_probability`
- [ ] All `per_cat_win_probability` values are in `[0, 1]`
- [ ] `cat_win_threshold` is in `[1, N]` where `N = len(cats)`
- [ ] `inverse_cats` is a subset of the cat list
- [ ] `resources_available` dict is present (even if empty — downstream skills may still consume leverage weights without a resource plan)
- [ ] Upstream `random_seed` from `matchup-win-probability-sim` is recorded for audit

**Step 2: Classify each cat by per_cat_win_probability**

Apply the four-tier classification in [Quick Reference](#quick-reference). The thresholds are deliberate — see [resources/methodology.md](resources/methodology.md#why-these-thresholds) for the Blotto-derived rationale.

- [ ] `< 0.25` → `conceded_cats` (dominated strategy — any roster slot here is strictly worse than redeploying)
- [ ] `0.25–0.70` → `contested_cats` (highest marginal value of one more unit)
- [ ] `0.70–0.85` → `pushed_cats` (needs attention but should hold)
- [ ] `> 0.85` → `locked` (do not waste marginal resources — returns are near-zero)
- [ ] Inverse cats (ERA, WHIP, TO, GAA, etc.) use `per_cat_win_probability` directly — the inverse handling has already been applied upstream by `matchup-win-probability-sim`. Do not re-invert.

**Step 3: Assign leverage_weights**

Leverage weights propagate to `mlb-lineup-optimizer`, `mlb-streaming-strategist`, `mlb-waiver-analyst`, and any downstream consumer that maximizes `Σ daily_quality × leverage[cat]`. See [resources/methodology.md](resources/methodology.md#leverage-weight-derivation).

- [ ] `leverage = 0.0` for `conceded_cats` (hard zero — not low, zero)
- [ ] `leverage = 1.5` for `contested_cats` (high marginal value of one more unit)
- [ ] `leverage = 1.2` for `pushed_cats` (above default but below contested)
- [ ] `leverage = 1.0` for `locked` cats (default — marginal gains are redundant)

**Step 4: Threshold satisfaction check**

Verify `len(pushed_cats) + len(contested_cats) >= cat_win_threshold`. If not, we are mathematically unable to reach the win threshold even if we go 100% on our defensible cats; the matchup is presumptively losing and we must either upgrade a borderline-conceded cat or pivot to variance-seeking play. See principle #6 in `frameworks/game-theory-principles.md`.

- [ ] Count `pushed_cats + contested_cats` (these are the cats where we have nonzero flip probability)
- [ ] If count `>= cat_win_threshold`: threshold satisfied, proceed to Step 6
- [ ] If count `< cat_win_threshold`: apply Step 5 borderline-upgrade logic
- [ ] If still insufficient after Step 5: flag the matchup for `variance-strategy-selector` as a high-variance play candidate

**Step 5: Borderline-upgrade logic (conditional)**

If Step 4 fails, look for `conceded_cats` with `per_cat_win_probability` in the `[0.20, 0.25)` "upgrade band". These are just below the concede line — a moderate resource investment (one waiver add, one FAAB bid, one streamer start) can lift them over 0.25 and into the `contested` tier.

- [ ] Sort `conceded_cats` by `per_cat_win_probability` descending
- [ ] Pick the top candidate(s) with `per_cat_win_probability >= 0.20`
- [ ] Reclassify to `contested` and set `leverage = 1.5`
- [ ] Document the upgrade in the rationale with the specific resource cost (e.g., "upgrading HR from conceded: spend 1 roster slot + $15 FAAB on a power bat")
- [ ] Re-run Step 4 — if still short, this matchup is presumptively losing; set a flag and defer to the variance-strategy-selector skill

**Step 6: Compute k_of_n_win_probability via Poisson-binomial**

Treat per-cat wins as independent Bernoullis (the same approximation used by `matchup-win-probability-sim` in `poisson_binomial` mode). Compute `P(sum >= cat_win_threshold)` via the standard PB recurrence. See [resources/methodology.md](resources/methodology.md#poisson-binomial-recurrence).

```
P_0(0) = 1
P_i(k) = P_{i-1}(k) * (1 - p_i) + P_{i-1}(k-1) * p_i   for i = 1..N, k = 0..N
k_of_n_win_probability = sum over k >= threshold of P_N(k)
```

- [ ] Use the post-upgrade `per_cat_win_probability` vector (Step 5 may have modified one entry)
- [ ] Return the overall `k_of_n_win_probability`
- [ ] If the value diverges from the `matchup_win_probability` returned by `matchup-win-probability-sim` by more than 0.03, investigate — the two should match within PB approximation error

**Step 7: Write rationale and emit outputs**

Rationale is a 2–4 sentence plain-English summary of the allocation logic. Name the conceded cats and why, name the contested cats and the highest-leverage resource move, call out any borderline upgrades, and state the computed `k_of_n_win_probability`. See [resources/template.md](resources/template.md#rationale-template) for worked examples.

- [ ] All outputs present: `pushed_cats`, `conceded_cats`, `contested_cats`, `leverage_weights`, `k_of_n_win_probability`, `rationale`
- [ ] `leverage_weights` has one entry per cat (not one per push/concede/contest bucket)
- [ ] Rationale names at least one conceded cat and one contested cat explicitly
- [ ] Validate using [resources/evaluators/rubric_category_allocation_best_response.json](resources/evaluators/rubric_category_allocation_best_response.json). Minimum standard: average score 3.5 or above.

## Common Patterns

**Pattern 1: MLB 10-cat (Yahoo 5x5)**
- **cats**: `[R, HR, RBI, SB, OBP, K, ERA, WHIP, QS, SV]`
- **cat_win_threshold**: 6
- **inverse_cats**: `[ERA, WHIP]`
- **Typical concedes**: SV (vs closer-heavy opponents), SB (vs power-heavy rosters), QS (vs all-RP staffs)
- **Resources**: roster_slots (typically 4–6 bench), faab ($0–$100), streamer_starts (2–4 per week)
- **Downstream consumers**: `mlb-lineup-optimizer` (principle #5), `mlb-streaming-strategist` (principle #1), `mlb-waiver-analyst` (principle #2)

**Pattern 2: NBA 9-cat**
- **cats**: `[PTS, REB, AST, STL, BLK, 3PM, FG%, FT%, TO]`
- **cat_win_threshold**: 5
- **inverse_cats**: `[TO]`
- **Typical concedes**: FT% (vs Giannis/Simmons-type rosters), TO (vs low-usage rosters), 3PM (vs shooting-punt rosters)
- **Resources**: roster_slots, streamer_games (NBA has daily streaming via DTD lineups)
- **Special**: NBA has higher cat-to-cat correlation (PTS-AST-3PM from team usage); the `pushed` tier tends to move together, so a single roster move can lift multiple cats at once. This makes contested-cat leverage particularly high.

**Pattern 3: NHL 10-cat**
- **cats**: `[G, A, +/-, PIM, PPP, SOG, W, GAA, SV%, SO]`
- **cat_win_threshold**: 6
- **inverse_cats**: `[GAA]`
- **Typical concedes**: SO (shutouts are low-count lottery), PIM (vs goon-free rosters), +/- (high variance)
- **Resources**: roster_slots, streamer_games, goalie_starts
- **Special**: Goalie cats (W, GAA, SV%, SO) are deeply correlated through the same player — a single streamer start affects four cats at once. Treat goalie-cat leverage as a bundle rather than four independent decisions.

**Pattern 4: Variance-seeking underdog (cross-domain)**
- When `k_of_n_win_probability < 0.40`: we are the underdog. Raise leverage on contested cats to `1.5`, and flag the matchup for `variance-strategy-selector`. High-variance lineup construction (boom-bust players, one-start studs) can lift our win probability from ~35% to ~45% even without roster improvements. See principle #6 in `frameworks/game-theory-principles.md`.

## Guardrails

1. **Do not invent per-cat probabilities**. This skill is a downstream consumer of `matchup-win-probability-sim`. If you do not have `per_cat_win_probability` from a proper simulator, do not proceed — compute them first. Eyeballing probabilities from raw projections ignores variance, which is the whole point of the contested-cat classification.

2. **Leverage weight 0.0 is a hard constraint, not a preference**. When `mlb-lineup-optimizer` reads `leverage[SV] = 0.0`, it will refuse to start a pure-SV reliever even if the reliever has a high `daily_quality`. This is correct behavior (principle #1 in `frameworks/game-theory-principles.md`) — do not soften the zero to 0.1 or 0.2 to "keep options open". Zero means zero.

3. **Contested-cat leverage stays 1.5 even if we are favored in the cat**. The 1.5 multiplier captures the marginal value of one extra unit — which is high whenever the cat is close. A cat at `per_cat_win_probability = 0.68` still has room for marginal gains to flip it to a near-certain win; leverage remains 1.5 (it is a `pushed` cat at 1.2, and moves to 1.5 if it drops into the contested band below 0.70).

4. **Threshold and count must match the league format**. `cat_win_threshold = 6` for 10-cat MLB (strict majority). `5` for 9-cat NBA. `6` for 10-cat NHL. Passing the wrong threshold produces a silently wrong classification. Always confirm the league's tie-break rules — some leagues award ties for half-wins.

5. **Dominated-strategy elimination is per-matchup, not per-season**. A cat conceded this week vs a closer-heavy opponent may be a push cat next week vs a different opponent. Do not cache `conceded_cats` across weeks. Re-run the classification every matchup.

6. **Inverse-cat handling is upstream's job**. `matchup-win-probability-sim` already returns `per_cat_win_probability` with inverse handling applied (ERA 3.50 beats ERA 4.20 = win probability near 1.0). This skill consumes those probabilities directly. Do not re-invert, and do not treat inverse cats differently at the classification step.

7. **Upgrade band is narrow (0.20–0.25)**. Only upgrade a `conceded` cat when its `per_cat_win_probability` is within the narrow `[0.20, 0.25)` band and we have resources available. Upgrading a 0.15-probability cat is throwing resources at a losing cause. Upgrading a 0.24-probability cat with a single waiver add may flip it to 0.30 — worth it.

8. **Document resource cost when recommending upgrades**. Abstract "upgrade HR" is unactionable. Say "upgrade HR with 1 roster slot + $15 FAAB on a power bat who adds ~3 HR/week", so `mlb-waiver-analyst` and `mlb-faab-sizer` have a concrete target.

9. **When the matchup is presumptively losing, pivot to variance, not to pushing harder**. If `k_of_n_win_probability < 0.40` after classification and upgrades, the best move is to maximize variance (principle #6), not to redouble on `pushed_cats`. Flag the matchup in the rationale and call `variance-strategy-selector` downstream.

10. **The skill is domain-neutral — resist MLB-specific assumptions**. When called from NBA or NHL contexts, the thresholds (0.25 / 0.70 / 0.85), bands, leverage weights, and upgrade-band logic all apply unchanged. Only the cat list and win threshold change between sports. Keep the core logic sport-agnostic.

## Quick Reference

**Four-tier classification (from `per_cat_win_probability`)**:

| Range | Bucket | Leverage | Rationale |
|-------|--------|----------|-----------|
| `[0.00, 0.25)` | `conceded` | 0.0 | Dominated strategy. Marginal unit has near-zero flip impact. |
| `[0.25, 0.70)` | `contested` | 1.5 | Highest marginal value — one more unit often flips outcome. |
| `[0.70, 0.85]` | `pushed` | 1.2 | Should hold but not guaranteed; defend with attention. |
| `(0.85, 1.00]` | `locked` | 1.0 | Default weight; marginal gains are near-redundant. |

**Upgrade band (for borderline concedes)**:

| Range | Action |
|-------|--------|
| `[0.20, 0.25)` | Candidate for upgrade if Step 4 threshold check fails. |
| `[0.00, 0.20)` | Do not upgrade. Resources are better spent on contested cats. |

**Poisson-binomial recurrence (for `k_of_n_win_probability`)**:

```
Given p = [p_1, p_2, ..., p_N] and threshold K:

P_0(0) = 1
P_0(k) = 0 for k >= 1

For i = 1..N:
  P_i(0) = P_{i-1}(0) * (1 - p_i)
  For k = 1..i:
    P_i(k) = P_{i-1}(k) * (1 - p_i) + P_{i-1}(k-1) * p_i

k_of_n_win_probability = sum_{k=K}^{N} P_N(k)
```

**Inputs required**:

- `our_per_cat_capacity`: `dict[cat, number]` — our projected per-cat output (remaining-week or full-week)
- `opp_per_cat_projection`: `dict[cat, number]` — opponent's projected per-cat output
- `per_cat_win_probability`: `dict[cat, float in [0,1]]` — FROM `matchup-win-probability-sim`
- `cat_win_threshold`: `int` — 6 for MLB 10-cat, 5 for NBA 9-cat, 6 for NHL 10-cat
- `resources_available`: `dict[str, number]` — e.g., `{"roster_slots": 5, "faab": 80, "streamer_starts": 3}`
- `inverse_cats`: `list[str]` — cats where lower is better (ERA, WHIP, TO, GAA, etc.)

**Outputs produced**:

- `pushed_cats`: `list[cat]` — ordered by `per_cat_win_probability` descending
- `conceded_cats`: `list[cat]` — dominated; leverage 0.0
- `contested_cats`: `list[cat]` — highest marginal leverage
- `leverage_weights`: `dict[cat, float]` — values in `{0.0, 1.0, 1.2, 1.5}`
- `k_of_n_win_probability`: `float in [0,1]` — overall matchup win prob under this allocation
- `rationale`: `string` — 2–4 sentences of plain-English allocation logic

**Upstream dependencies**:

- `matchup-win-probability-sim` (REQUIRED) — supplies `per_cat_win_probability` and overall `matchup_win_probability` for cross-validation
- `*-category-state-analyzer` (optional, MLB/NBA/NHL) — supplies the per-cat capacity and opponent projection

**Downstream consumers**:

- `mlb-lineup-optimizer` / NBA / NHL equivalents — consume `leverage_weights` (principle #5)
- `mlb-streaming-strategist` — reads `conceded_cats` as hard constraint (principle #1)
- `mlb-waiver-analyst` / `mlb-faab-sizer` — consume `contested_cats` + `resources_available` to target high-leverage adds
- `variance-strategy-selector` — consumes `k_of_n_win_probability` to decide favorite-vs-underdog play style (principle #6)

**Key resources**:

- **[resources/template.md](resources/template.md)**: Input/output contract, MLB 10-cat worked example, NBA 9-cat worked example, rationale templates
- **[resources/methodology.md](resources/methodology.md)**: Colonel Blotto origins and H2H-variant math, why K-of-N is not winner-takes-all, Nash equilibrium for symmetric cases, heuristic best-response for asymmetric cases, dominated-strategy elimination, upstream-signal derivation, variance-pivot logic
- **[resources/evaluators/rubric_category_allocation_best_response.json](resources/evaluators/rubric_category_allocation_best_response.json)**: 10 criteria — classification accuracy, leverage weight assignment, dominated-strategy identification, threshold satisfaction check, rationale quality, borderline-upgrade logic, generalization to non-10-cat leagues, output completeness, upstream-signal integration, citations
