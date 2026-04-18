---
name: opponent-archetype-classifier
description: Classifies an opposing player, manager, or agent into one of a configurable archetype set using Bayesian inference over observed behavior (roster composition, transaction pattern, lineup moves, trade activity). Domain-neutral scaffold -- callers supply the archetype taxonomy (names, priors, characteristic feature distributions) and observed features; the skill returns a normalized posterior, MAP archetype, classification confidence, feature-contribution breakdown, and best-response hints. Use when modeling opponents, classifying player types, performing Bayesian archetype inference, producing opponent posteriors, or when user mentions opponent archetype, classify opponent, Bayesian archetype inference, player type classification, opponent modeling, or archetype posterior.
---
# Opponent Archetype Classifier

## Table of Contents
- [Example](#example)
- [Workflow](#workflow)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Example

**Scenario**: Fantasy baseball league, Week 5. Classify opponent "Manager A" into one of six archetypes -- `balanced`, `stars_and_scrubs`, `punt_sv`, `punt_sb`, `punt_wins_qs`, `hitter_heavy`.

**Inputs** (abbreviated; full taxonomy in [resources/template.md](resources/template.md#worked-example-6-archetype-fantasy-baseball-taxonomy)):

```yaml
archetype_taxonomy:
  balanced:          {prior: 0.30, feature_distributions: {sp_roster_share: {mean: 0.40, std: 0.06}, closer_count: {mean: 2.0, std: 0.6}, sb_speed_count: {mean: 3.0, std: 1.0}, moves_per_week: {mean: 2.5, std: 1.0}, bid_aggression: {low: 0.5, high: 0.5}}}
  stars_and_scrubs:  {prior: 0.15, ...}
  punt_sv:           {prior: 0.15, feature_distributions: {closer_count: {mean: 0.3, std: 0.4}, ...}}
  punt_sb:           {prior: 0.15, feature_distributions: {sb_speed_count: {mean: 0.8, std: 0.7}, ...}}
  punt_wins_qs:      {prior: 0.10, feature_distributions: {sp_roster_share: {mean: 0.20, std: 0.05}, closer_count: {mean: 3.0, std: 0.8}, moves_per_week: {mean: 4.0, std: 1.2}, ...}}
  hitter_heavy:      {prior: 0.15, feature_distributions: {sp_roster_share: {mean: 0.28, std: 0.05}, ...}}

observed_features:
  sp_roster_share:   0.22    # low -- thin on starters
  closer_count:      3       # heavy RP
  sb_speed_count:    2       # moderate speed
  moves_per_week:    4.2     # high activity
  bid_aggression:    high    # active FAAB bidder

observation_weight: 0.7        # ~4 weeks of data
```

**Computation (per-feature log-likelihood, summed, exponentiated, multiplied by prior, normalized)**:

| Archetype | log L(features) | L * prior | Normalized Posterior |
|-----------|-----------------|-----------|---------------------|
| balanced | -14.8 | 1.1e-7 | 0.04 |
| stars_and_scrubs | -12.5 | 5.6e-7 | 0.21 |
| punt_sv | -18.2 | 1.8e-9 | 0.00 |
| punt_sb | -22.6 | 2.3e-11 | 0.00 |
| **punt_wins_qs** | **-10.1** | **1.8e-6** | **0.68** |
| hitter_heavy | -13.2 | 4.2e-7 | 0.16 |

**Outputs**:

```yaml
posterior:
  balanced: 0.04
  stars_and_scrubs: 0.21
  punt_sv: 0.00
  punt_sb: 0.00
  punt_wins_qs: 0.68
  hitter_heavy: 0.16

map_archetype: punt_wins_qs

classification_confidence: 47.6     # = max_posterior (0.68) * observation_weight (0.7) * 100

best_response_hints:
  - "Concede K and QS; lock 6 of remaining 8 cats"
  - "Don't stream starting pitchers against them"
  - "They will dominate SV and ratios via all-RP staff; push hitting cats hard"

feature_contribution_breakdown:
  sp_roster_share:  {map_likelihood: 0.92, alternative_max: 0.15, likelihood_ratio: 6.1}   # low SP share -- strong punt_wins_qs signal
  closer_count:     {map_likelihood: 0.52, alternative_max: 0.46, likelihood_ratio: 1.1}   # 3 closers fits several archetypes
  sb_speed_count:   {map_likelihood: 0.38, alternative_max: 0.41, likelihood_ratio: 0.9}   # not discriminating
  moves_per_week:   {map_likelihood: 0.33, alternative_max: 0.28, likelihood_ratio: 1.2}
  bid_aggression:   {map_likelihood: 0.70, alternative_max: 0.60, likelihood_ratio: 1.2}

assumptions_flagged:
  - "Conditional independence across features assumed -- sp_roster_share and moves_per_week may be correlated (active punt strategy drives both)"
  - "Feature distributions are SME priors, not empirically fit -- refresh after season 1 with posterior data"
```

**Note on confidence**: posterior peaks at 0.68 but `observation_weight=0.7` (only 4 weeks of data) dampens confidence to 47.6. Above the 40 threshold, so MAP is reported; but caller is advised that another 2-3 weeks of observation will sharpen the call.

## Workflow

Copy this checklist and track progress:

```
Opponent Archetype Classification Progress:
- [ ] Step 1: Load archetype taxonomy (names, priors, feature distributions)
- [ ] Step 2: Collect observed features for the target opponent
- [ ] Step 3: Compute per-feature likelihood under each archetype
- [ ] Step 4: Combine likelihoods (assume conditional independence; flag it)
- [ ] Step 5: Apply Bayes rule, normalize posterior
- [ ] Step 6: Select MAP archetype; compute confidence
- [ ] Step 7: Check inconclusive threshold; report or defer
- [ ] Step 8: Produce feature-contribution breakdown and best-response hints
```

**Step 1: Load archetype taxonomy**

The caller supplies the taxonomy. See [resources/template.md](resources/template.md#archetype-taxonomy-schema) for required fields.

- [ ] Each archetype has a name, a prior probability, and a feature distribution per observable
- [ ] Priors sum to 1.0 (normalize if not)
- [ ] Each feature has either a parametric distribution (Gaussian with mean/std) or a categorical (value -> probability)
- [ ] Each archetype has a documented `best_response` string array

**Step 2: Collect observed features**

Observed features must match feature names in the taxonomy. Missing features are dropped (not imputed) and flagged.

- [ ] Feature names match taxonomy keys exactly
- [ ] Numeric features in the taxonomy's expected units
- [ ] Categorical features use the taxonomy's category labels
- [ ] `observation_weight` (0-1) supplied; rises with sample size -- see [methodology.md](resources/methodology.md#observation-weight-calibration)

**Step 3: Compute per-feature likelihood**

For each (archetype, feature) pair compute `P(feature_value | archetype)`. See [methodology.md](resources/methodology.md#likelihood-function-design).

- [ ] Gaussian feature: `L = (1/(std*sqrt(2*pi))) * exp(-0.5 * ((x - mean)/std)^2)`
- [ ] Categorical feature: `L = P_archetype[category]` with Laplace smoothing if zero
- [ ] Work in log-space (`log L`) to avoid underflow when combining 5+ features

**Step 4: Combine likelihoods (conditional independence)**

First-approximation assumption: features are conditionally independent given archetype. This is rarely exactly true; flag it.

- [ ] Sum log-likelihoods across features per archetype
- [ ] Flag correlated feature pairs (e.g., `sp_roster_share` and `moves_per_week` in fantasy baseball)
- [ ] If two features are strongly correlated, consider merging them or down-weighting one; document the choice

**Step 5: Apply Bayes rule, normalize**

```
posterior_unnorm[a] = exp(sum_log_L[a]) * prior[a]
posterior[a] = posterior_unnorm[a] / sum_a(posterior_unnorm[a])
```

- [ ] Compute in log-space for numerical stability, then subtract max before exponentiating
- [ ] Verify `sum(posterior) == 1.0` within rounding
- [ ] Document any archetype with posterior < 1e-6 as "ruled out"

**Step 6: Select MAP archetype; compute confidence**

```
map_archetype = argmax(posterior)
classification_confidence = max(posterior) * observation_weight * 100
```

- [ ] MAP is the most likely archetype, not the only possibility
- [ ] Confidence blends how peaked the posterior is with how much we trust the observation

**Step 7: Inconclusive threshold**

If `classification_confidence < 40`:

- [ ] Return `map_archetype: "inconclusive"`
- [ ] Return the full posterior anyway (caller may still act on the top-2)
- [ ] Advise: "Collect 2-3 more weeks of observation before committing to a classification"

**Step 8: Feature-contribution breakdown + best-response hints**

- [ ] For each feature compute likelihood ratio: `L(feature | MAP) / max_{a != MAP} L(feature | a)`
- [ ] Pull `best_response_hints` from the MAP archetype's documented string array
- [ ] Return alongside the posterior so caller sees *why* this archetype was selected

## Common Patterns

**Pattern 1: Fantasy sports (baseball, basketball, hockey) manager archetypes**
- **Taxonomy**: 5-8 archetypes like `balanced`, `punt_<cat>`, `stars_and_scrubs`, `inactive` covering category-league strategy.
- **Features**: roster composition by position, transaction frequency, FAAB aggression, lineup-setting accuracy.
- **Conditional-independence risk**: several features covary (an inactive manager has low moves AND low bids AND stale lineup). Down-weight or collapse.
- **Observation weight**: 0.3 by Week 2, 0.6 by Week 5, 0.85 by Week 10.

**Pattern 2: Poker opponent archetypes**
- **Taxonomy**: `tight_aggressive (TAG)`, `loose_aggressive (LAG)`, `tight_passive (rock)`, `loose_passive (calling station)`, `maniac`.
- **Features**: VPIP, PFR, 3-bet %, aggression factor, c-bet frequency, showdown frequency.
- **Conditional-independence risk**: VPIP and PFR are tightly linked; keep both but note the correlation.
- **Observation weight**: rises sharply with hand count -- 0.4 at 100 hands, 0.75 at 500 hands, 0.9 at 2000+.

**Pattern 3: DFS lineup-construction archetypes**
- **Taxonomy**: `cash_game_optimizer`, `GPP_ceiling_chaser`, `contrarian_pivot`, `chalk_herding`.
- **Features**: average salary usage, stack count, ownership-vs-projection ratio, tournament vs cash entry split.
- **Conditional-independence risk**: stack count and ownership-vs-projection covary for GPP players.

**Pattern 4: M&A / auction bidder archetypes**
- **Taxonomy**: `strategic_premium_bidder`, `financial_disciplined_bidder`, `fishing_expedition`, `structured_earnout_preferer`.
- **Features**: announced bid count per quarter, strategic vs financial press-release language, premium multiple paid, deal structure (cash vs stock vs earnout).
- **Observation weight**: low at any single deal; rises with repeated bidding history.

## Guardrails

1. **Conditional independence is almost never exactly true.** Always flag it. If two features are strongly correlated (|r| > 0.6), merge them into a single composite feature or down-weight one by 50%. Otherwise the confident archetype gets credited twice for the same underlying signal.

2. **Priors matter when data is thin.** Uniform priors are a choice, not a neutral default. Use domain-informed priors when the population distribution is known (e.g., in a 12-team fantasy league, `inactive` has a real base rate of ~1-2 managers, not 1/12).

3. **Numeric stability: work in log-space.** Multiplying 5+ small likelihoods underflows to 0 in float64. Sum log-likelihoods, subtract the max log-posterior before exponentiating, then normalize.

4. **Laplace smoothing for categoricals.** If an archetype has `P(category=X) = 0` in its distribution and the observation is X, the posterior for that archetype becomes 0 -- permanently ruling it out on one data point. Apply add-epsilon smoothing (epsilon = 0.01 is typical).

5. **Inconclusive is a feature, not a failure.** A low-confidence classification is valuable information -- it tells the caller to gather more data before committing. Don't force a MAP when confidence is below 40.

6. **Best-response hints come from the taxonomy, not the classifier.** The skill should not invent strategy; it should retrieve what the taxonomy author documented for that archetype. If the taxonomy's `best_response` is empty, return an empty array and note that the taxonomy needs enrichment.

7. **Posterior is a distribution, not a point estimate.** When downstream agents consume the output, they should ideally consume the full posterior (and make expected-value decisions over it) rather than collapsing to MAP. Expose both.

8. **Update sequentially as new observations arrive.** The current week's posterior becomes next week's prior. See [methodology.md](resources/methodology.md#sequential-posterior-updating) for the recursive formula.

9. **Feature contribution breakdown guards against overfitting.** If one feature's likelihood ratio is > 10, that single feature is driving the classification -- verify the feature was measured correctly before trusting the result.

10. **Refresh feature distributions with empirical data once available.** Initial distributions are SME priors. After N opponents have been labelled and observed, fit the distributions empirically and replace the SME priors.

## Quick Reference

**Key formulas:**

```
Gaussian likelihood:
  L(x | a) = (1 / (std_a * sqrt(2*pi))) * exp(-0.5 * ((x - mean_a) / std_a)^2)

Categorical likelihood (with Laplace smoothing, epsilon = 0.01):
  L(x = c | a) = (count_a[c] + epsilon) / (sum_c' count_a[c'] + epsilon * num_categories)

Joint likelihood (conditional independence assumption):
  L(features | a) = prod_f L(feature_f | a)

Log-space joint likelihood:
  log L(features | a) = sum_f log L(feature_f | a)

Bayes posterior:
  posterior(a) proportional to L(features | a) * prior(a)
  posterior(a) = posterior_unnorm(a) / sum_a' posterior_unnorm(a')

MAP selection:
  map_archetype = argmax_a posterior(a)

Classification confidence:
  confidence = max_a posterior(a) * observation_weight * 100
  if confidence < 40:
      map_archetype = "inconclusive"

Sequential update (week t):
  prior_t(a) = posterior_{t-1}(a)
  posterior_t(a) proportional to L(new_features_t | a) * prior_t(a)

Feature contribution (likelihood ratio):
  LR(feature_f) = L(feature_f | MAP) / max_{a != MAP} L(feature_f | a)
```

**Confidence bands:**

| Confidence | Interpretation | Action |
|------------|---------------|--------|
| 0-39 | Inconclusive | Gather more data |
| 40-59 | Weak MAP | Treat MAP as tentative; hedge downstream decisions |
| 60-79 | Solid MAP | Act on MAP but keep top-2 in mind |
| 80-100 | Confident MAP | Commit to MAP |

**Key resources:**

- **[resources/template.md](resources/template.md)**: Archetype taxonomy schema (YAML), observed-features schema, output schema, fully worked 6-archetype fantasy baseball example.
- **[resources/methodology.md](resources/methodology.md)**: Bayesian classification primer, likelihood function design, characteristic-feature distribution construction (empirical vs SME), conditional independence assumption and when it breaks, sequential posterior updating.
- **[resources/evaluators/rubric_opponent_archetype_classifier.json](resources/evaluators/rubric_opponent_archetype_classifier.json)**: 10 quality criteria for evaluating the output.

**Inputs required:**

- `archetype_taxonomy`: dict of archetype_name -> `{prior, feature_distributions, best_response}`
- `observed_features`: dict of feature_name -> observed value
- `observation_weight`: 0-1, how much to trust the observation vs the prior
- `archetype_prior` (optional): dict of archetype_name -> prior; defaults to taxonomy priors (or uniform)

**Outputs produced:**

- `posterior`: dict<archetype, probability>, sums to 1
- `map_archetype`: string, most likely archetype (or `"inconclusive"`)
- `classification_confidence`: 0-100
- `best_response_hints`: string[], pulled from the MAP archetype's documented best-response
- `feature_contribution_breakdown`: dict<feature, {map_likelihood, alternative_max, likelihood_ratio}>
- `assumptions_flagged`: string[], e.g., correlated features, smoothing applied, priors forced uniform
