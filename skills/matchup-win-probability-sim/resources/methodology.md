# Matchup Win Probability Simulator — Methodology

Formal procedures for Monte Carlo simulation, Poisson-binomial approximation, inverse-cat handling, ratio-cat volume weighting, variance estimation, and mode selection.

## Table of Contents
- [Monte Carlo Formalization](#monte-carlo-formalization)
- [Poisson-Binomial Recurrence](#poisson-binomial-recurrence)
- [Inverse Category Handling](#inverse-category-handling)
- [Ratio Category Volume Weighting](#ratio-category-volume-weighting)
- [Threshold Application and Tie Rules](#threshold-application-and-tie-rules)
- [Variance Estimation](#variance-estimation)
- [Correlated Categories](#correlated-categories)
- [Non-Normal Distributions](#non-normal-distributions)
- [Reproducibility and Seeding](#reproducibility-and-seeding)
- [When to Use Which Mode](#when-to-use-which-mode)

---

## Monte Carlo Formalization

### Setup

Let `C = {c_1, ..., c_N}` be the category set, and let `K = cat_win_threshold` (the minimum number of cat wins required to win the matchup).

For each cat `c`, let:
- `μ_us(c), σ_us(c)` — our projected mean and stddev
- `μ_op(c), σ_op(c)` — opponent's projected mean and stddev
- `I(c) = 1` if `c ∈ cat_inverse_list`, else `0`

### Procedure

For each simulation `s = 1..S`:

1. For each cat `c`:
   - Draw `X_s(c) ~ D_c(μ_us(c), σ_us(c))` where `D_c` is the per-cat distribution family (normal by default).
   - Draw `Y_s(c) ~ D_c(μ_op(c), σ_op(c))` independently.
   - Compute the margin: `M_s(c) = X_s(c) - Y_s(c)`.
   - If `I(c) = 1` (inverse cat), flip: `M_s(c) ← -M_s(c)`.
2. For each cat `c`, set the cat-win indicator:
   - If `tie_rule = "strict"`: `W_s(c) = 1` iff `M_s(c) > 0` else `0`.
   - If `tie_rule = "half"`: `W_s(c) = 1` if `M_s(c) > 0`; `0.5` if `M_s(c) = 0`; `0` if `M_s(c) < 0`. (For continuous distributions, `M_s(c) = 0` occurs with probability zero, so the half-rule is operationally indistinguishable from strict. It matters for discrete cats.)
3. Count cats won: `T_s = Σ_c W_s(c)`.
4. Matchup indicator: `Z_s = 1` iff `T_s ≥ K`, else `0`.

### Aggregate estimators

```
matchup_win_probability   = (1/S) × Σ_s Z_s
per_cat_win_probability[c] = (1/S) × Σ_s W_s(c)
expected_cats_won          = (1/S) × Σ_s T_s
variance_estimate          = (1/(S-1)) × Σ_s (T_s - expected_cats_won)^2
```

### Monte Carlo standard error

For `matchup_win_probability`:
```
SE = sqrt(p (1 - p) / S)
```
Practical targets:
- `S = 1000`:  SE ≈ 0.016 at p=0.5 (suitable for rough decisions)
- `S = 10000`: SE ≈ 0.005 (suitable for weekly strategy — **default**)
- `S = 100000`: SE ≈ 0.0016 (suitable for tight playoff-reachability decisions)

---

## Poisson-Binomial Recurrence

When all per-cat outcomes are independent Bernoullis with possibly-different probabilities, the distribution of their sum is the **Poisson-binomial distribution**. This gives a closed-form computation of `P(T ≥ K)` without simulation.

### Step 1 — compute per-cat win probability analytically

Assuming normal distributions for both sides:

```
combined_stddev(c) = sqrt( σ_us(c)^2 + σ_op(c)^2 )
margin_mean(c)     = μ_us(c) - μ_op(c)
if I(c) = 1: margin_mean(c) ← -margin_mean(c)      # inverse cats
z(c)               = margin_mean(c) / combined_stddev(c)
p(c)               = Φ(z(c))                       # standard normal CDF
```

This is exact when our output and the opponent's output are each normally distributed and independent of each other (the difference of independent normals is normal with the summed variance).

### Step 2 — apply the PB recurrence

Initialize: `P_0(0) = 1` and `P_0(k) = 0` for `k > 0`.

For `i = 1, 2, ..., N`:
```
P_i(0) = P_{i-1}(0) × (1 - p_i)
P_i(k) = P_{i-1}(k) × (1 - p_i) + P_{i-1}(k-1) × p_i     for k = 1 .. i
```

After all `N` cats have been folded in, `P_N(k)` is `P(exactly k cat wins)`.

### Step 3 — compute the tail

```
matchup_win_probability = Σ_{k = K}^{N} P_N(k)
```

### Step 4 — first and second moments (closed form)

```
expected_cats_won = Σ_c p(c)
variance_estimate = Σ_c p(c) × (1 - p(c))              # exact under independence
```

Unlike MC, these are exact (no sampling error) — but they rest on the independence assumption.

### Complexity

`O(N^2)` for the recurrence, `O(N)` for the moments. For `N = 10` this is trivially fast; for `N = 100` still < 1ms in pure Python.

---

## Inverse Category Handling

Inverse categories are cats where *lower is better* — ERA, WHIP, GAA, TO (NBA turnovers), bogey count in fantasy golf, etc.

### Why negating the margin is the right approach

Consider ERA: us 3.85, opp 4.10. Our ERA is *lower*, so **we win**. Raw margin (us − opp) is `3.85 − 4.10 = −0.25` (negative) — but we should record a win. Negating flips to `+0.25`, which the downstream `margin > 0` test correctly marks as a win.

### Two implementations and why one is right

**Wrong way — negate inputs at ingest**:
```python
if c in cat_inverse_list:
    μ_us, μ_op = -μ_us, -μ_op        # flip means
    # stddevs unchanged
```
This works for the `Φ`-based PB computation but breaks when:
- The sim trace is returned to the caller: ERA=−3.85 is nonsense to a human auditor.
- The caller supplies a `distribution_family = "poisson"` (Poisson is defined on non-negative support; negation breaks it).
- Per-cat correlations are involved (sign flips in the covariance matrix require careful handling).

**Right way — negate the computed margin at comparison time**:
```python
margin = our_draw - opp_draw
if c in cat_inverse_list:
    margin = -margin                 # flip the decision, not the inputs
cat_won = 1 if margin > 0 else (0.5 if margin == 0 else 0)
```

For PB mode, the equivalent is:
```python
margin_mean = μ_us - μ_op
if c in cat_inverse_list:
    margin_mean = -margin_mean
p_c = Φ(margin_mean / combined_stddev)
```

This preserves input semantics, works for all distribution families, and composes correctly with correlations.

### Verification test

A sanity-check the implementation should pass: if `μ_us = μ_op` and `σ_us = σ_op` for an inverse cat, the per-cat win prob must come out to exactly 0.5 (tie on symmetric distributions). If it comes out to something else, the inversion is miswired.

---

## Ratio Category Volume Weighting

Ratio cats (OBP, ERA, WHIP, FG%, SV%, GAA) are weighted aggregates over a denominator (PAs, IP, FGA, SA). The variance of a ratio depends on the *volume* of observations in the denominator.

### The variance of a rate

Given `n` independent Bernoulli-like trials with per-trial success probability `p`, the sample proportion has:
```
Var(p_hat) = p (1 - p) / n
SD(p_hat)  = sqrt( p (1 - p) / n )
```

More generally for a rate aggregated over `n` observations with per-observation variance `σ_1^2`:
```
SD(aggregate rate) = σ_1 / sqrt(n)
```

### Applied to fantasy ratio cats

**OBP**:
- Per-PA OBP outcome is roughly Bernoulli with `p ≈ 0.33`, so per-PA variance ≈ `p(1-p) ≈ 0.22`, per-PA stddev ≈ `0.47`. But the stddev *across weekly OBP outcomes* is dominated by across-player skill differences and hot/cold streaks. Empirical per-PA stddev for aggregated team OBP is ~0.15.
- For a team projected to hit 100 PA in the remaining week: `stddev_OBP ≈ 0.15 / √100 = 0.015`. Matches the worked example.

**ERA**:
- Per-IP ER outcome has stddev ~3.3 (ER/9-equivalent).
- For 55 IP remaining: `stddev_ERA ≈ 3.3 / √55 ≈ 0.445`.

**WHIP**:
- Per-IP (BB+H) has stddev ~0.6.
- For 55 IP: `stddev_WHIP ≈ 0.6 / √55 ≈ 0.081`.

### Caller responsibility vs skill responsibility

This skill treats the supplied `stddev` as authoritative. The **caller** (e.g., `mlb-category-state-analyzer`) is responsible for:
1. Estimating remaining volume (PA, IP) from roster × games-remaining.
2. Computing the volume-weighted stddev via `σ_per_obs / sqrt(n_obs)`.
3. Passing the result as `stddev` in the projection dict.

A common bug to avoid: if the caller passes a full-season stddev (e.g., 0.025 for OBP) when only a few games remain, the skill will *underestimate* variance, overstating extreme cat win probs and biasing matchup_win_probability toward 0 or 1.

### Minimum-volume cutoffs for ratio cats

Yahoo leagues typically enforce a minimum PA or minimum IP for ratio cats to count (e.g., 25 IP/week for ERA). If a team will end the week below the minimum, the cat is frozen at its current value regardless of the remaining sims. The caller should:
- Check whether the minimum is reachable.
- If not, pass `{mean: current_value, stddev: 1e-6}` (effectively deterministic).

Inside this skill, a near-zero stddev produces a near-step-function per-cat win prob, matching the economic reality of a frozen cat.

---

## Threshold Application and Tie Rules

### Threshold

`cat_win_threshold` is the minimum number of cat wins we need to win the overall matchup.

- MLB Yahoo 5x5 (10 cats): `K = 6` — strict majority.
- NBA 9-cat: `K = 5` — strict majority.
- Custom 8-cat: `K = 5` — strict majority.
- Leagues where ties are awarded half-wins in the aggregate: compute the probability of the edge case (`T = K - 0.5`) separately if the caller needs a "win or tie" probability; otherwise treat `K` as the strict-win threshold.

### Per-cat tie rule

Continuous distributions (normal) produce exact ties with probability zero, so `tie_rule` is effectively irrelevant in pure-normal MC. It matters when:
- The distribution family is discrete (Poisson for HR, SV).
- The caller rounds draws to integers before comparing.

**Rules**:
- `"half"` — tied cats count as 0.5 for both sides. Matches Yahoo's scoring for the overall matchup. A cat tied perfectly could push `T_s = K - 0.5` just below the threshold; test it carefully.
- `"strict"` — tied cats count as 0 for both sides. Slightly pessimistic relative to Yahoo behavior.

### Matchup-level tie handling

Some leagues award ties when the cats-won count is split exactly. If the user wants "win or tie" probability:
```
P(win or tie) = P(T >= K - 0.5)     # only meaningful if half-wins possible
P(strict win) = P(T >= K)
```
This skill returns `P(T >= K)` by default. A caller can recompute using `per_cat_win_probability` via the PB recurrence if they want both.

---

## Variance Estimation

Two distinct variances are commonly confused. Label them carefully.

### 1. Variance of the cats-won count

The variance of `T = Σ_c W_c`. Measures how spread out the distribution of "cats we win" is across sims.

**Monte Carlo estimator** (unbiased):
```
variance_estimate = (1/(S-1)) × Σ_s (T_s - mean(T_s))^2
```

**Poisson-binomial closed form** (under independence):
```
variance_estimate = Σ_c p_c × (1 - p_c)
```

**With correlation** (MC supplies `cat_correlation_matrix`):
```
variance_estimate = Σ_c p_c (1-p_c) + 2 × Σ_{c<c'} Cov(W_c, W_{c'})
```

The MC estimator captures this automatically; PB cannot.

Typical range for N=10 cats: `0.5 ≤ variance_estimate ≤ 2.5` (bounded above by `N/4`).

### 2. Standard error of the matchup_win_probability

Variance of our estimator `p_hat` of `matchup_win_probability`:
```
Var(p_hat) = p (1 - p) / S          # only meaningful for MC
SE(p_hat)  = sqrt( p (1-p) / S )
```

This skill returns `monte_carlo_stderr` under `meta` for MC mode (null for PB mode since PB has no sampling error under its assumptions).

### Why we return variance of T rather than of p_hat

The variance of `T` is a **property of the matchup** (informative for downstream decisions — e.g., "our week is low-variance, favor steady players"). The variance of `p_hat` is a **property of our estimate** (informative for "should we run more sims?"). Callers overwhelmingly want the first; we return both in `meta`.

---

## Correlated Categories

By default Monte Carlo treats every cat as independent. In practice:

- **MLB**: mild correlation. OBP correlates with R (on-base runners score). HR correlates with RBI. These correlations are small at the team-week level (~0.15) because different players contribute to different cats.
- **NBA**: stronger correlation. A team's offensive rating lifts PTS, AST, 3PM, and FG% simultaneously.
- **NHL**: moderate. G correlates with A and SOG.

### When to pass a correlation matrix

Pass `cat_correlation_matrix` when:
1. You have empirical correlations from a historical dataset.
2. The matchup is close and correlation direction matters (positive correlation reduces variance of `T` → either tightens or loosens matchup prob depending on sign of favoritism).

### Implementation with correlation

Given `cat_correlation_matrix` R (NxN, symmetric, PSD), construct the joint covariance of our draws:
```
Σ_us = diag(σ_us) × R × diag(σ_us)
Σ_op = diag(σ_op) × R × diag(σ_op)       # commonly the same R for both sides
```

Draw `X_s ~ MultivariateNormal(μ_us, Σ_us)` via Cholesky: `X_s = μ_us + L_us × Z_s`, `L_us = chol(Σ_us)`, `Z_s ~ N(0, I_N)`. Same for `Y_s` with an independent `Z'_s`.

The margin vector `M_s = X_s - Y_s` is then distributed `N(μ_us - μ_op, Σ_us + Σ_op)`.

### Effect on matchup_win_probability

- Positive per-cat correlation ( `+0.3`): `T` becomes more variable → underdogs see a lift, favorites see a drop. For a `p = 0.6` matchup, correlation `+0.3` moves `p` toward ~0.55.
- Negative correlation (rare in practice): opposite effect.

### Poisson-binomial limitation

PB mode **cannot** accept a correlation matrix because the PB distribution is defined over independent Bernoullis. If correlation is important, use MC.

---

## Non-Normal Distributions

Normal is a reasonable default for means ≥ ~10 (central limit theorem kicks in for sums of per-player contributions). Breaks down for:

- **Saves (SV)**: typical mean 2-5 per week, highly skewed, often truncated at 0. Normal puts mass on negatives.
- **HR in a short week**: mean 3-5, count-like, Poisson-ish.
- **QS**: sum of 0/1 start indicators, Poisson-binomial per start.
- **SB**: low mean, count, Poisson approximation decent.

### Supplying per-cat distribution families

Pass `distribution_family = {"SV": "poisson", "HR": "poisson", ...}`. For cats listed as `poisson`, the skill uses:
- MC: `numpy.random.poisson(lam=mean)` (where `mean = μ`; Poisson variance = mean, so the caller's `stddev` input is ignored — this is a known limitation; better to pre-compute `mean` consistently).
- PB: approximate `p_c` using the normal continuity correction: `Φ((μ_us - μ_op + 0.5) / sqrt(μ_us + μ_op))` (since difference of two independent Poissons is Skellam-distributed, which is well-approximated by a discrete normal with mean `μ_us - μ_op` and variance `μ_us + μ_op`).

### Negative binomial for over-dispersed counts

If a cat shows variance > mean (e.g., HR in a week with two-start boom pitchers on the opponent's staff), Poisson under-disperses. Negative-binomial is a better fit but is not first-class in this skill; emulate it by setting `distribution_family = "normal"` and choosing a `stddev` that captures the overdispersion empirically.

---

## Reproducibility and Seeding

### Deterministic output

With `sim_mode = "poisson_binomial"`, output is bit-exact deterministic regardless of `random_seed`.

With `sim_mode = "monte_carlo"`, seed the RNG as the **first step** of the function:
```python
rng = np.random.default_rng(random_seed) if random_seed is not None else np.random.default_rng()
```
All subsequent draws come from `rng` (not the global `np.random`). This ensures that multiple concurrent calls with different seeds don't interfere.

### Required for audit logs

Every call that feeds into `tracker/decisions-log.md` must pass `random_seed` (convention: use the week number, e.g., `random_seed = 8` for Week 8). This allows any reviewer to re-run and get identical numbers.

### Note on RNG library

This skill's implementation should be RNG-library-agnostic but document which library is used (numpy, random, or torch). A user who reproduces with a different library will get different draws even with the same seed. Include `"rng_library": "numpy"` in `meta` to disambiguate.

---

## When to Use Which Mode

### Decision matrix

| Situation | Use |
|-----------|-----|
| Weekly strategy briefing (default) | `monte_carlo`, N=10k |
| Need `sim_trace` audit | `monte_carlo` |
| Non-normal per-cat distribution (Poisson for SV, etc.) | `monte_carlo` with `distribution_family` |
| Per-cat correlations (NBA usage correlations) | `monte_carlo` with `cat_correlation_matrix` |
| Inner loop of an optimizer (lineup search, trade evaluator) | `poisson_binomial` (100-1000x faster) |
| Closed-form deterministic result for test harness | `poisson_binomial` |
| Sensitivity analysis (sweeping a parameter) | `poisson_binomial` first, then MC on the final candidate |
| Playoff-reachability / tight decisions (p near 0.5) | `monte_carlo`, N=100k |

### Cross-validation

When possible, run both modes and compare:
- Matchup_win_probability delta should be within `2 × SE(MC)`.
- Expected_cats_won should match closely (PB is exact under independence).
- A delta larger than `3 × SE(MC)` suggests either strong correlation or a non-normal cat is materially distorting the answer — investigate.

### Performance comparison

For N=10 cats, S=10000 MC sims (pure Python + numpy):
- Monte Carlo: ~100-200 ms
- Poisson-binomial: ~1 ms

For N=10 cats inside a 1000-call optimization loop:
- MC: ~100-200 s
- PB: ~1 s

The fidelity cost of PB (~1% error under standard fantasy conditions) is almost always dominated by the upstream uncertainty in `{mean, stddev}` inputs. Use PB liberally for inner loops.

---

## Worked mini-example of the PB recurrence

Say N=3 cats with win probs `p = [0.6, 0.5, 0.4]`, threshold `K=2`.

**Step by step**:
- `P_0 = [1, 0, 0, 0]` (indices 0..3)
- i=1 (p=0.6):
  - `P_1[0] = 1 × 0.4 = 0.4`
  - `P_1[1] = 0 × 0.4 + 1 × 0.6 = 0.6`
  - `P_1 = [0.4, 0.6, 0, 0]`
- i=2 (p=0.5):
  - `P_2[0] = 0.4 × 0.5 = 0.20`
  - `P_2[1] = 0.6 × 0.5 + 0.4 × 0.5 = 0.50`
  - `P_2[2] = 0 × 0.5 + 0.6 × 0.5 = 0.30`
  - `P_2 = [0.20, 0.50, 0.30, 0]`
- i=3 (p=0.4):
  - `P_3[0] = 0.20 × 0.6 = 0.12`
  - `P_3[1] = 0.50 × 0.6 + 0.20 × 0.4 = 0.38`
  - `P_3[2] = 0.30 × 0.6 + 0.50 × 0.4 = 0.38`
  - `P_3[3] = 0 × 0.6 + 0.30 × 0.4 = 0.12`
  - `P_3 = [0.12, 0.38, 0.38, 0.12]`

Validation: sum = 1.00 ✓

Results:
- `matchup_win_probability = P(T ≥ 2) = 0.38 + 0.12 = 0.50`
- `expected_cats_won = 0.6 + 0.5 + 0.4 = 1.50`
- `variance_estimate = 0.6×0.4 + 0.5×0.5 + 0.4×0.6 = 0.24 + 0.25 + 0.24 = 0.73`

Sanity: `E[T] = Σ k × P_3[k] = 0×0.12 + 1×0.38 + 2×0.38 + 3×0.12 = 1.50` ✓
