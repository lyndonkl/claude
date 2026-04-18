# Opponent Archetype Classifier Methodology

Bayesian classification primer, likelihood function design, characteristic-feature distribution construction, conditional-independence assumption analysis, sequential posterior updating, and observation weight calibration.

## Table of Contents
- [Bayesian Classification Primer](#bayesian-classification-primer)
- [Likelihood Function Design](#likelihood-function-design)
- [Constructing Characteristic-Feature Distributions](#constructing-characteristic-feature-distributions)
- [Conditional Independence Assumption](#conditional-independence-assumption)
- [When Conditional Independence Breaks](#when-conditional-independence-breaks)
- [Observation Weight Calibration](#observation-weight-calibration)
- [Sequential Posterior Updating](#sequential-posterior-updating)
- [Inconclusive Handling](#inconclusive-handling)
- [Numerical Stability in Log-Space](#numerical-stability-in-log-space)
- [Posterior Diagnostics](#posterior-diagnostics)

---

## Bayesian Classification Primer

The classifier answers: given everything I've observed about this opponent, which archetype is most likely?

**Bayes' rule applied to archetype inference:**

```
P(archetype = a | features) = P(features | a) * P(a) / P(features)
```

- `P(a)` is the prior: how common is this archetype in the population? (Taxonomy input.)
- `P(features | a)` is the likelihood: how often would an archetype-a opponent produce exactly this observation pattern?
- `P(features)` is the evidence: doesn't depend on `a`, so it's a normalization constant. We compute unnormalized posteriors and divide by their sum.

**The classifier's job is to convert weak per-feature signals into a calibrated distribution over archetypes.**

A single feature rarely discriminates well. Many features together, combined through Bayes, produce a peaked posterior when the data is genuinely informative -- and appropriately stay diffuse when it isn't. The posterior communicates not just "which archetype" but "how sure."

**Why Bayesian, not a decision tree or SVM?**

- **Interpretability**: every classification comes with a posterior distribution, not just a label. Downstream decision-makers can do expected-value reasoning over the full posterior.
- **Prior integration**: domain experts supply prior distributions for each archetype's behavior. The classifier respects those priors; it doesn't need a training set of labelled opponents.
- **Graceful degradation with thin data**: when features are few or noisy, the posterior stays close to the prior instead of overconfidently guessing.
- **Composability across domains**: the same math works for fantasy, poker, DFS, M&A -- swap the taxonomy.

---

## Likelihood Function Design

For each (archetype `a`, feature `f`), the taxonomy specifies a distribution. Two forms:

### Gaussian (continuous features)

```
L(x | a, f) = (1 / (std_{a,f} * sqrt(2*pi))) * exp(-0.5 * ((x - mean_{a,f}) / std_{a,f})^2)
log L(x | a, f) = -log(std_{a,f}) - 0.5 * log(2*pi) - 0.5 * ((x - mean_{a,f}) / std_{a,f})^2
```

**Choosing mean and std:**

- `mean_{a,f}` = the expected value of feature f for an archetype-a opponent. Elicit from domain expert or fit from labelled data.
- `std_{a,f}` = how much variation around the mean is normal for that archetype. **Be generous.** Too-narrow stds produce a classifier that confidently rules out archetypes on noise. A good heuristic: `std >= (feature range) / 6` -- covers the full range within +/- 3 standard deviations.

### Categorical (discrete features)

```
L(x = c | a, f) = (count_{a,f}[c] + epsilon) / (sum_{c'} count_{a,f}[c'] + epsilon * num_categories)
```

The `epsilon` (typically 0.01) is **Laplace smoothing** -- it ensures no category has probability exactly 0, which would permanently rule out an archetype on one observation.

**When to use which:**

- Use Gaussian when the feature is naturally continuous (counts, fractions, averages, rates).
- Use categorical for ordinal buckets (`low | moderate | high`), enumerated states (`passive | moderate | aggressive`), or truly nominal features (handedness, position).
- If in doubt, discretize to categorical -- it's more robust to mis-specified std.

### Truncated distributions

For features with natural bounds (e.g., `bid_aggression_pct` in [0, 1]), the Gaussian may put probability mass outside the bound. Two fixes:

1. **Truncate and renormalize**: redefine the distribution only on the valid range. Exact but requires recomputing the normalization constant.
2. **Transform the feature**: apply a logit or log transform to map the bounded feature to the real line before fitting a Gaussian.
3. **Accept the approximation**: if the bound is far from the mean (>3 std away), the mass leak is negligible and ignoring it is fine.

---

## Constructing Characteristic-Feature Distributions

Two routes: **empirical** (fit from labelled data) or **SME prior** (elicit from subject-matter expert).

### Empirical fitting

When you have a dataset of opponents already labelled with their true archetype:

1. **Group observations by archetype.** For each archetype `a`, collect all feature vectors.
2. **Fit per-feature distribution.** For continuous features, compute sample mean and sample std (use `ddof=1` for unbiased std). For categorical features, compute category frequencies and apply Laplace smoothing.
3. **Sanity check via leave-one-out cross-validation.** Hold out each labelled opponent, fit on the rest, classify the held-out one. Measure top-1 accuracy and posterior calibration.
4. **Inflate std slightly** (multiply by 1.2-1.5) to account for the fact that real opponents are drawn from a broader distribution than the (finite) training sample suggests.

### SME prior elicitation

When no labelled dataset exists (most domains at cold start):

1. **Interview the SME.** Ask: "For an archetype-a opponent, what's a typical value of feature f? How much would it vary?"
2. **Extract triplet.** For each (a, f): elicit low, typical, high values. Set `mean = typical`; set `std = (high - low) / 4` (treating low/high as roughly +/- 2 std bounds).
3. **Validate against known exemplars.** Show the SME 3-5 historical opponents whose archetype is known. Compute each opponent's likelihood under the elicited distributions. If the true archetype doesn't dominate, revise the distributions.
4. **Refresh empirically.** Once you've classified 20+ opponents using the SME priors, refit the distributions from observed feature vectors (weighted by posterior, not hard labels).

### Hybrid: empirical Bayes

Combine both routes: use the SME elicitation as a prior over the distribution parameters, and update with empirical data as it accumulates. The fewer observations, the more weight on the SME prior; the more observations, the more weight on the data.

---

## Conditional Independence Assumption

**The core assumption (naive Bayes):**

```
P(features | a) = prod_f P(feature_f | a)
```

This holds exactly when all features are independent given the archetype. In practice it rarely holds exactly, but it is often "good enough" to produce a useful classifier.

### Why it's a first approximation

If features are truly conditionally independent given archetype, the joint likelihood factorizes cleanly and we only need per-feature distributions -- O(N_archetypes * N_features) parameters instead of the exponentially larger joint distribution.

### What goes wrong when features are correlated

Suppose `sp_roster_share` and `moves_per_week` are correlated for a `punt_wins_qs` opponent (both signals of an actively-punted pitching strategy). Using naive Bayes, the posterior "double-counts" the signal:

- Feature 1 says: this is `punt_wins_qs` with log-LR = +2
- Feature 2 says: this is `punt_wins_qs` with log-LR = +2
- Naive Bayes posterior: log-LR = +4 (overconfident -- the two features are really one underlying signal)
- Correct joint posterior: log-LR ~= +2.5 (the second feature adds only marginal information)

**Result**: the classifier is overconfident in the MAP archetype and under-hedges.

---

## When Conditional Independence Breaks

**Red flags that features are correlated given archetype:**

1. **Two features measure the same underlying construct.** E.g., `moves_per_week` and `bids_per_week` -- both measure "activity level." Collapse into one composite.

2. **One feature is a function of another.** E.g., `sp_roster_share` and `rp_roster_share` -- they sum to a fixed total, so knowing one determines the other within a constant. Keep only one.

3. **The archetype definition explicitly ties features together.** `punt_sv` is defined partly as "few closers" -- so `closer_count` and the punt itself are correlated. This is usually fine because it's what makes the feature diagnostic; but be aware that other features downstream of the same behavioral choice (e.g., `sv_total_projection`) are redundant.

**Remedies:**

1. **Collapse correlated features into a composite.** Compute a z-score for each, average them, feed the average as a single feature.

2. **Down-weight one of the pair.** If correlation r ~ 0.7, down-weight the "extra" feature's log-likelihood by `(1 - r^2) = 0.51`. Crude but effective.

3. **Model the correlation explicitly.** Move from naive Bayes to a multivariate Gaussian likelihood with a covariance matrix. Requires more data to estimate reliably.

4. **Feature-cluster the observations.** Group correlated features into independent "blocks," fit a low-dim distribution per block, assume independence across blocks (not within).

**Always flag the assumption in the output** (`assumptions_flagged`). Downstream consumers can then decide whether to trust the confidence number or hedge further.

---

## Observation Weight Calibration

`observation_weight` (0-1) reflects how much we trust this week's observation relative to the baseline prior. It does NOT scale the likelihoods (the math is unchanged); it scales the *confidence score* reported to downstream consumers.

**Why a separate knob instead of letting the likelihoods speak?**

- The feature distributions assume the observation is "clean" (representative of steady-state behavior). In early weeks the data is noisy -- 2 weeks of draft-party fatigue or a vacation.
- `observation_weight` lets the caller dampen downstream action when they know the data is thin, without distorting the posterior itself.

### Calibration table (by domain)

**Fantasy sports (season-long):**

| Weeks observed | observation_weight |
|----------------|-------------------|
| 1-2 | 0.25 |
| 3-4 | 0.45 |
| 5-7 | 0.65 |
| 8-11 | 0.80 |
| 12+ | 0.90 |

**Poker (hand-based):**

| Hands observed | observation_weight |
|----------------|-------------------|
| <100 | 0.20 |
| 100-500 | 0.45 |
| 500-2000 | 0.70 |
| 2000-10000 | 0.85 |
| 10000+ | 0.95 |

**DFS (entry-based):**

| Entries observed | observation_weight |
|------------------|-------------------|
| <5 | 0.20 |
| 5-20 | 0.50 |
| 20-100 | 0.75 |
| 100+ | 0.90 |

**M&A (deal-based):**

| Deals observed | observation_weight |
|----------------|-------------------|
| 1 | 0.25 |
| 2-3 | 0.50 |
| 4-6 | 0.70 |
| 7+ | 0.85 |

### Reliability dampers

Multiply the base weight by 0.5-0.8 if any of:

- Data is from a known anomalous period (e.g., mid-season injury that forced non-representative moves).
- One feature dominates the others and may be noisy.
- The opponent recently changed behavior (e.g., team sold, new manager).

---

## Sequential Posterior Updating

As new observations arrive, update the posterior recursively:

```
prior_{t} = posterior_{t-1}
posterior_{t}(a) proportional to L(new_features_t | a) * prior_{t}(a)
```

**Key property: the posterior is a sufficient statistic of all past observations.** You don't need to re-run the computation over the full history; just use last week's posterior as this week's prior.

### Practical rules

1. **Don't re-feed persistent features every week.** Roster composition barely changes week-to-week. If you add `closer_count = 3` every week as "new" evidence, the posterior will become artificially overconfident. Instead, include persistent features only in the initial classification; use only truly-new signals for sequential updates.

2. **Use a "fresh-evidence" feature set.** Define two subsets:
   - **State features** (persistent): roster composition, typical bid style. Fed once.
   - **Flow features** (renewing): this week's moves, this week's bids, this week's trade activity. Fed each week.

3. **Apply a decay factor** for older flow observations. If `punt_wins_qs` behavior was clear in Weeks 3-5 but moves trended toward balanced in Weeks 6-8, the recent observations should matter more. Multiply the log-likelihood of a k-weeks-ago observation by `exp(-k / tau)` with `tau = 4-6 weeks`.

4. **Watch for archetype drift.** If the MAP posterior jumps from one archetype to another between weeks (e.g., `inactive` to `active punt_sb`), the opponent may have structurally changed. Consider restarting with a flat prior rather than blending with the old posterior.

### Drift detection

Compute the KL divergence between consecutive posteriors:

```
KL(posterior_{t} || posterior_{t-1}) = sum_a posterior_{t}(a) * log(posterior_{t}(a) / posterior_{t-1}(a))
```

If KL > 2.0, flag as "possible archetype drift." Do not silently average -- surface to the caller.

---

## Inconclusive Handling

**Rule**: if `classification_confidence < 40`, return `map_archetype = "inconclusive"` AND the full posterior.

**Why return the full posterior even when inconclusive?**

The caller may still be able to act on the top-2 or top-3 archetypes -- e.g., "we think it's either `balanced` or `hitter_heavy`; both call for roughly the same response this week, so we proceed; but we flag uncertainty."

**What counts as inconclusive:**

| max(posterior) | observation_weight | confidence | map_archetype |
|----------------|-------------------|------------|---------------|
| 0.30 | 1.0 | 30 | inconclusive |
| 0.50 | 0.7 | 35 | inconclusive |
| 0.60 | 0.6 | 36 | inconclusive |
| 0.40 | 1.0 | 40 | (weak) MAP |
| 0.80 | 0.5 | 40 | (weak) MAP |

**What the caller should do with inconclusive output:**

1. Report uncertainty explicitly to the user.
2. Collect more observations (wait 1-2 more weeks, or run more targeted probes).
3. Act cautiously on the posterior: if the top 2 archetypes have the same best-response, execute that common response; otherwise hedge.
4. Do NOT force a MAP decision. It's better to say "we don't know yet" than to overcommit to a noisy guess.

### Tuning the threshold

The 40 threshold is a sensible default. Adjust if:

- **High-stakes domains (M&A, major trades)**: raise to 55-60 -- the cost of a wrong classification is large.
- **Low-stakes repeated decisions (daily DFS, weekly streaming)**: lower to 30 -- hundreds of calls over a season; being directionally right on the majority is enough.
- **Cost-asymmetric decisions**: if false-positive is cheap but false-negative is expensive, lower the threshold; raise it if the reverse.

---

## Numerical Stability in Log-Space

### Why log-space

With 5+ features and likelihoods around 0.01-0.5, the joint likelihood is `< 1e-5`. Multiplying a few more features drives it below `1e-30` -- fine in float64, but 10+ features risk underflow. In log-space everything is additive and stable.

### The log-sum-exp trick

To normalize `log_posterior_unnorm[a]` to a proper distribution without exponentiating huge negative numbers:

```
M = max_a log_posterior_unnorm[a]
shifted[a] = log_posterior_unnorm[a] - M
posterior[a] = exp(shifted[a]) / sum_a' exp(shifted[a'])
```

Subtracting the max before exponentiating ensures the largest term becomes `exp(0) = 1`, and all others are `exp(negative) <= 1`. No overflow, no underflow for anything within ~700 log-units of the max (plenty of headroom).

### Pseudocode

```
log_likelihood = {a: 0 for a in archetypes}
for a in archetypes:
    for f, x in observed_features.items():
        log_likelihood[a] += log_L(x, taxonomy[a].feature_distributions[f])

log_post_unnorm = {a: log_likelihood[a] + log(prior[a]) for a in archetypes}
M = max(log_post_unnorm.values())
shifted = {a: log_post_unnorm[a] - M for a in archetypes}
exp_shifted = {a: exp(shifted[a]) for a in archetypes}
Z = sum(exp_shifted.values())
posterior = {a: exp_shifted[a] / Z for a in archetypes}
```

---

## Posterior Diagnostics

Beyond MAP and confidence, the output should expose:

### Shannon entropy

```
H(posterior) = -sum_a posterior(a) * log(posterior(a))       # in nats; multiply by log2(e) for bits
```

- Uniform over 6 archetypes: H ~= 1.79 nats (maximum).
- Peaked on one archetype: H ~= 0.
- **Rule of thumb**: H < 0.5 means a confident classification; H > 1.0 means mostly uninformative.

### Top-2 gap

```
gap = posterior[MAP] - posterior[second_best]
```

A gap of 0.5+ means MAP is clearly separated. A gap of <0.2 means two archetypes are essentially tied -- in that case the caller should consider whether the tied archetypes have the same best-response (in which case classification is practically-moot) or divergent ones (in which case hedge or collect more data).

### Feature-contribution sanity

Compute `LR(feature) = L(feature | MAP) / max_{a != MAP} L(feature | a)` for each feature.

- If one feature's LR > 10, the classification hinges on that single feature -- verify it was measured correctly.
- If every feature's LR is in [0.8, 1.2], no feature is discriminating; the posterior is being driven by priors. Fine, but flag that data is uninformative.
- If some features have LR < 1.0 (point against MAP), they are evidence against the chosen archetype. That's OK if others strongly favor MAP, but the presence of against-features should be visible to the caller.

### Report template

Always include in the output:

```yaml
posterior_entropy: <float>                  # nats
top2_gap: <float>                           # posterior[MAP] - posterior[2nd]
features_supporting_map: <int>              # count of features with LR > 1.0
features_against_map: <int>                 # count with LR < 1.0
dominant_feature: <string>                  # name of feature with largest LR
sample_adequacy_note: <string>              # plain-English summary
```

This metadata is what turns a bare posterior into an interpretable classification result.
