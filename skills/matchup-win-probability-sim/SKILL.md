---
name: matchup-win-probability-sim
description: Computes P(we win at least K of N categories) for a head-to-head categorical matchup via Monte-Carlo simulation or Poisson-binomial approximation. Domain-neutral — works for any fantasy sport with H2H Categories scoring (MLB, NBA, NHL) or any zero-sum per-category competition. Use when you need matchup_win_probability, per_cat_win_probability, expected_cats_won, or variance_estimate; or when user mentions "matchup win probability", "head to head simulation", "Monte Carlo matchup", "Poisson binomial matchup", "P win 6 of 10", "category matchup simulation", or "weekly win probability".
---
# Matchup Win Probability Simulator

## Table of Contents
- [Example](#example)
- [Workflow](#workflow)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Example

**Scenario**: Yahoo MLB 10-category H2H matchup, Week 8, threshold = 6 of 10. Categories: R, HR, RBI, SB, OBP (hitting); K, ERA, WHIP, QS, SV (pitching). ERA and WHIP are inverse (lower is better).

**Inputs** (remaining-week projections for both teams; mean = expected output, stddev = uncertainty):

| Cat | Our mean | Our stddev | Opp mean | Opp stddev | Inverse? |
|-----|----------|-----------|----------|-----------|----------|
| R | 42 | 8 | 38 | 7 | no |
| HR | 12 | 3.5 | 14 | 4 | no |
| RBI | 40 | 9 | 41 | 8 | no |
| SB | 6 | 2.5 | 4 | 2 | no |
| OBP | 0.335 | 0.015 | 0.328 | 0.014 | no |
| K | 55 | 10 | 50 | 9 | no |
| ERA | 3.85 | 0.45 | 4.10 | 0.50 | **yes** |
| WHIP | 1.22 | 0.08 | 1.28 | 0.09 | **yes** |
| QS | 4 | 1.5 | 3 | 1.4 | no |
| SV | 2 | 1.2 | 5 | 1.5 | no |

**Run both modes** with `random_seed=42`, `cat_win_threshold=6`, `n_simulations=10000`:

**Monte Carlo output**:
- `matchup_win_probability` = 0.612
- `expected_cats_won` = 6.18
- `variance_estimate` = 2.42 (variance of cats-won count)
- `per_cat_win_probability`: R 0.64, HR 0.35, RBI 0.47, SB 0.72, OBP 0.64, K 0.64, ERA 0.65, WHIP 0.68, QS 0.69, SV 0.08

**Poisson-binomial output** (for comparison, uses the same per-cat win probs as inputs to the PB recurrence):
- `matchup_win_probability` = 0.605
- `expected_cats_won` = 6.18 (exact — sum of per-cat probs)
- `variance_estimate` = 2.11 (variance of sum of independent Bernoullis)

Interpretation: we are a modest favorite (~61%). SV is a hard-punt cat (8% win). HR is contested but we lean losing. The six most defensible pushes are SB, QS, WHIP, ERA, R, K (and OBP). Downstream `mlb-lineup-optimizer` uses `win_prob = 0.612` to classify us as a favorite → damp variance.

## Workflow

Copy this checklist and track progress:

```
Matchup Win Probability Simulation Progress:
- [ ] Step 1: Validate inputs and cat_list coverage
- [ ] Step 2: Choose sim_mode (monte_carlo or poisson_binomial)
- [ ] Step 3: Apply inverse-cat handling
- [ ] Step 4: Run simulation with seeded RNG
- [ ] Step 5: Compute per-cat and overall win probabilities
- [ ] Step 6: Emit outputs with variance and optional sim_trace
```

**Step 1: Validate inputs**

Confirm every cat in `cat_list` has an entry in both `our_per_cat_projection` and `opp_per_cat_projection`, each with `{mean, stddev}`. Confirm `cat_win_threshold <= len(cat_list)`. Confirm `cat_inverse_list ⊆ cat_list`. See [resources/template.md](resources/template.md#input-schema).

- [ ] Every cat in `cat_list` has both sides' projections
- [ ] `stddev > 0` for all cats (zero stddev blocks correct simulation; use small floor if unknown)
- [ ] `cat_win_threshold` in `[1, len(cat_list)]`
- [ ] All `cat_inverse_list` entries are valid cat names
- [ ] If `sim_mode == "monte_carlo"`, `n_simulations >= 1000` (10k default; 100k for tight confidence)

**Step 2: Choose sim_mode**

Default to `monte_carlo` for operational decisions (full distribution of cats-won). Use `poisson_binomial` when you need a deterministic, sub-millisecond answer and are willing to assume per-cat independence. See [resources/methodology.md](resources/methodology.md#when-to-use-which-mode).

- [ ] `monte_carlo`: when you need `sim_trace` for audit, when distributions are non-normal, or when per-cat correlations are passed
- [ ] `poisson_binomial`: when you need a fast closed-form approximation, or when calling this skill inside an inner optimization loop

**Step 3: Apply inverse-cat handling**

For every cat in `cat_inverse_list`, flip the comparison: our team wins the cat when our draw is **less** than the opponent's draw (ERA 3.50 beats ERA 4.20). The cleanest implementation is to negate the margin `(our_draw - opp_draw) → (opp_draw - our_draw)` for inverse cats before counting the win. See [resources/methodology.md](resources/methodology.md#inverse-category-handling).

- [ ] Identify inverse cats from `cat_inverse_list`
- [ ] Negate margin (or flip comparison) per cat
- [ ] Verify the per-cat win prob for a known-inverse cat aligns with intuition

**Step 4: Run simulation**

With `random_seed` set, draw paired outcomes (one per team per cat per sim) from the configured distribution (normal default) and score each sim.

- [ ] Seed the RNG deterministically from `random_seed`
- [ ] For each of `n_simulations`:
  - Draw `our_draw[cat] ~ Normal(our_mean, our_stddev)` for every cat
  - Draw `opp_draw[cat] ~ Normal(opp_mean, opp_stddev)` for every cat
  - For each cat, compute margin (negated for inverse)
  - Count `cats_won = sum(margin > 0)` (tie-break rule: exact tie counts as 0.5 or 0; see guardrail #4)
  - Record `matchup_win = (cats_won >= cat_win_threshold)`

For Poisson-binomial mode instead: compute per-cat win prob `p_i = Φ(margin_mean_i / combined_stddev_i)` analytically (negate margin for inverse cats), then apply the PB recurrence to get `P(sum >= threshold)`.

**Step 5: Compute outputs**

- `matchup_win_probability` = mean of `matchup_win` across sims (MC) or closed-form PB result.
- `per_cat_win_probability[cat]` = mean of `margin > 0` per cat (MC) or `Φ(...)` per cat (PB).
- `expected_cats_won` = mean of `cats_won` (MC) or `Σ p_i` (PB).
- `variance_estimate` = variance of `cats_won` across sims (MC) or `Σ p_i(1-p_i)` (PB, since cats are modeled as independent Bernoullis).

See [resources/methodology.md](resources/methodology.md#variance-estimation) for derivation.

**Step 6: Emit outputs and audit trace**

Return the full output dict. If `return_sim_trace=true`, include the first 100 sims as `sim_trace` for caller-side audit (showing per-cat draws and the final cats_won vector).

- [ ] All outputs present: `matchup_win_probability`, `per_cat_win_probability`, `expected_cats_won`, `variance_estimate`
- [ ] Optional: `sim_trace` (first 100 sims only — keep payload small)
- [ ] Cite `random_seed` used so the caller can reproduce
- [ ] Validate using [resources/evaluators/rubric_matchup_win_probability_sim.json](resources/evaluators/rubric_matchup_win_probability_sim.json). Minimum standard: average score 3.5 or above.

## Common Patterns

**Pattern 1: MLB Yahoo 5x5 (10 cats)**
- **cat_list**: `[R, HR, RBI, SB, OBP, K, ERA, WHIP, QS, SV]`
- **cat_win_threshold**: 6
- **cat_inverse_list**: `[ERA, WHIP]`
- **Ratio cats needing volume weighting**: OBP (weight by PA), ERA (weight by IP), WHIP (weight by IP). Caller should pre-compute stddev that reflects volume — a half-week with 20 IP has larger ratio variance than a full week with 55 IP.
- **Typical runtime**: 10k sims < 200ms in plain Python

**Pattern 2: NBA 9-cat H2H**
- **cat_list**: `[PTS, REB, AST, STL, BLK, 3PM, FG%, FT%, TO]`
- **cat_win_threshold**: 5
- **cat_inverse_list**: `[TO]` (turnovers — lower is better)
- **Ratio cats**: FG%, FT% (volume-weight by FGA, FTA)
- **Special**: NBA has higher cat-to-cat correlation than MLB (team usage patterns link PTS-AST-3PM); pass correlation matrix if available

**Pattern 3: NHL 10-cat or similar**
- **cat_list** example: `[G, A, +/-, PIM, PPP, SOG, W, GAA, SV%, SO]`
- **cat_win_threshold**: 6
- **cat_inverse_list**: `[GAA]` (goals against average)
- **Ratio cats**: SV% (volume-weight by SA), GAA (volume-weight by games played)

**Pattern 4: Mid-week live matchup (partial week elapsed)**
- Caller should pass `{mean, stddev}` reflecting **remaining-week** output plus current running total. That is, `mean = running_total + expected_remaining`; `stddev` shrinks as less time remains.
- `cat_position` from `mlb-category-state-analyzer` feeds directly: locked-in cats should have near-zero stddev and a mean far outside the opponent's distribution.

## Guardrails

1. **Reproducibility requires a seed**. Without `random_seed`, two calls with identical inputs will return slightly different probabilities (Monte Carlo error). For audit logs and unit tests, always pass a seed. The Poisson-binomial mode is deterministic regardless.

2. **Monte Carlo standard error**. With `n_simulations = N` and true probability `p`, the standard error is `sqrt(p(1-p)/N)`. For `N=10000` and `p=0.5`, SE ≈ 0.005. If the caller needs 3-decimal precision, use `N >= 100000`.

3. **Inverse cats: negate the margin, not the mean**. A common bug is to negate `mean` at input time, which causes the Poisson-binomial `Φ` computation to flip sign but breaks the stddev interpretation. Preferred: keep inputs in their natural units (ERA = 3.85 stays 3.85) and negate the **computed margin** at comparison time. See [resources/methodology.md](resources/methodology.md#inverse-category-handling).

4. **Tie-break convention must be stated**. If `our_draw == opp_draw` for a cat in a given sim, the convention is `cats_won += 0.5` for both sides (H2H Cats "ties count as half wins" style) OR `cats_won += 0` (strict majority). Default: `tie_rule = "half"` to match Yahoo H2H behavior. Document which rule is in effect.

5. **Normal distribution assumption breaks for extreme counting cats**. Saves and Home Runs are low-count discrete quantities; a normal approximation puts non-trivial mass on negative values. For low-mean counting cats (`mean < 5`), the caller can specify `distribution_family = "poisson"` per cat; Monte Carlo handles this, Poisson-binomial does not (since PB needs a `Φ`-based per-cat prob — compute it from the Poisson-normal approximation with continuity correction).

6. **Ratio cats need volume weighting**. OBP, ERA, WHIP are *ratios* (weighted aggregates over PAs or IP). The stddev of the ratio depends on the volume of observations: few PAs → wide stddev. The caller is responsible for supplying a volume-adjusted stddev (see methodology for the formula `stddev_ratio ≈ σ_per_obs / sqrt(n_obs)`). This skill treats the supplied stddev as truth.

7. **Independence assumption is a simplification**. OBP and R are correlated (on-base runners generate runs). The default Monte Carlo assumes independence across cats. If the caller passes a `cat_correlation_matrix` (positive semi-definite, dimension equal to `len(cat_list)`), Monte Carlo uses it via Cholesky decomposition of the combined covariance. Poisson-binomial cannot accept correlation (the whole point of PB is independent Bernoullis).

8. **Threshold must match the league format**. `cat_win_threshold = 6` for 10-cat MLB (strict majority), `5` for 9-cat NBA, etc. Passing the wrong threshold silently produces a meaningful but wrong `matchup_win_probability`. Always confirm the league's tie-break rules for the overall matchup too (some leagues award ties for half-wins in the aggregate count).

9. **Don't aggregate across distinct matchups**. A single-call output answers "this week vs this opponent." Weighting a season-long playoff-probability from weekly win probs is a downstream caller's job (`mlb-playoff-planner`).

10. **Document the variance estimate's meaning**. `variance_estimate` is the variance of the *cats-won count* (range 0..N). It is NOT the variance of `matchup_win_probability`. The latter is the MC standard-error variance `p(1-p)/N`. Both are useful; label them clearly if returning both.

## Quick Reference

**Core formulas**:

```
Monte Carlo (per sim):
  For each cat c:
    our_draw[c]  ~ Normal(our_mean[c],  our_stddev[c])
    opp_draw[c]  ~ Normal(opp_mean[c],  opp_stddev[c])
    margin[c]    = our_draw[c] - opp_draw[c]
    if c in cat_inverse_list: margin[c] *= -1
    cat_won[c]   = (margin[c] > 0)     # or 0.5 if exact tie and tie_rule="half"
  cats_won       = sum(cat_won across cats)
  matchup_won    = (cats_won >= cat_win_threshold)

Monte Carlo aggregate (over N sims):
  matchup_win_probability    = mean(matchup_won)
  per_cat_win_probability[c] = mean(cat_won[c])
  expected_cats_won          = mean(cats_won)
  variance_estimate          = var(cats_won)

Poisson-Binomial (closed form):
  combined_stddev[c] = sqrt(our_stddev[c]^2 + opp_stddev[c]^2)
  margin_mean[c]     = our_mean[c] - opp_mean[c]    # negated for inverse cats
  per_cat_win_prob[c] = Φ(margin_mean[c] / combined_stddev[c])
  P(exactly k of N wins) via PB recurrence:
    P_0(0) = 1
    P_i(k) = P_{i-1}(k) * (1 - p_i) + P_{i-1}(k-1) * p_i
  matchup_win_probability = Σ_{k >= threshold} P_N(k)
  expected_cats_won       = Σ p_i
  variance_estimate       = Σ p_i (1 - p_i)
```

**When to use which mode**:

| Need | Use |
|------|-----|
| Full distribution of cats-won, audit trace | `monte_carlo` |
| Sub-millisecond, deterministic, exact PB result | `poisson_binomial` |
| Per-cat correlations (e.g., OBP-R) | `monte_carlo` (with correlation matrix) |
| Low-mean counting cats (SV, HR for a short week) | `monte_carlo` with `distribution_family="poisson"` |
| Inside an inner optimization loop (thousands of calls) | `poisson_binomial` |
| Default for weekly strategy | `monte_carlo` with `n_simulations=10000` |

**Inputs required**:
- `our_per_cat_projection`: `dict[cat, {mean: float, stddev: float}]`
- `opp_per_cat_projection`: `dict[cat, {mean: float, stddev: float}]`
- `cat_list`: `list[str]` — category names in canonical order
- `cat_win_threshold`: `int` (6 for 10-cat, 5 for 9-cat)
- `cat_inverse_list`: `list[str]` — cats where lower is better
- `n_simulations`: `int` (default 10000)
- `random_seed`: `int` (optional but recommended)
- `sim_mode`: `"monte_carlo"` (default) or `"poisson_binomial"`
- `tie_rule`: `"half"` (default) or `"strict"`
- `cat_correlation_matrix`: optional `float[N][N]`
- `distribution_family`: optional per-cat `dict[cat, "normal"|"poisson"]`
- `return_sim_trace`: `bool` (default false)

**Outputs produced**:
- `matchup_win_probability`: `float` in `[0, 1]`
- `per_cat_win_probability`: `dict[cat, float]`
- `expected_cats_won`: `float`
- `variance_estimate`: `float` (variance of cats-won count)
- `sim_trace`: optional `list[dict]` (first 100 sims; present only if `return_sim_trace=true`)
- `meta`: `{sim_mode, n_simulations, random_seed, tie_rule}` for audit

**Key resources**:
- **[resources/template.md](resources/template.md)**: Input schema, output schema, worked MLB 5x5 example with both modes
- **[resources/methodology.md](resources/methodology.md)**: Monte Carlo formalization, Poisson-binomial recurrence, variance derivation, inverse & ratio cat handling, mode-selection criteria
- **[resources/evaluators/rubric_matchup_win_probability_sim.json](resources/evaluators/rubric_matchup_win_probability_sim.json)**: 10 criteria for input-spec correctness, MC accuracy, PB accuracy, inverse-cat handling, ratio-cat volume weighting, threshold application, reproducibility, output completeness, variance estimation, citations

**Upstream callers** (examples):
- `mlb-category-state-analyzer` — passes remaining-week projections per cat (principles #1, #5, #6 in `frameworks/game-theory-principles.md`)
- Any fantasy `*-category-state-analyzer` equivalent for NBA/NHL
- Any caller that has per-cat `{mean, stddev}` and wants matchup-level win probability
