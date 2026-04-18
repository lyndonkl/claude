# Opponent Archetype Classifier Templates

Input schemas, output schema, and a fully worked 6-archetype fantasy baseball example with complete posterior computation.

## Table of Contents
- [Archetype Taxonomy Schema](#archetype-taxonomy-schema)
- [Observed Features Schema](#observed-features-schema)
- [Full Input Schema](#full-input-schema)
- [Output Schema](#output-schema)
- [Worked Example: 6-Archetype Fantasy Baseball Taxonomy](#worked-example-6-archetype-fantasy-baseball-taxonomy)
- [Worked Example: Step-by-Step Posterior Computation](#worked-example-step-by-step-posterior-computation)
- [Sequential Update Worksheet](#sequential-update-worksheet)
- [Domain-Neutral Taxonomy Template (fill-in)](#domain-neutral-taxonomy-template-fill-in)

---

## Archetype Taxonomy Schema

Each archetype requires four fields:

```yaml
archetype_taxonomy:
  <archetype_name>:                 # string, unique identifier
    prior: <float>                  # [0, 1], population base rate; priors across archetypes sum to 1
    feature_distributions:          # dict; one entry per observable feature
      <feature_name>:
        # Gaussian form:
        mean: <float>
        std: <float>
        # OR categorical form:
        <category_1>: <probability>
        <category_2>: <probability>
        # ...probabilities sum to 1 per feature
    best_response:                  # list of string hints for downstream agents
      - "hint 1"
      - "hint 2"
    description: "<one-line summary of the archetype>"   # optional but recommended
```

**Rules:**
- Archetype names must be unique and stable (used as keys in the output posterior).
- Every archetype must expose the same set of feature names. If a feature is not discriminating for a particular archetype, use a flat/wide distribution (e.g., Gaussian with high std).
- Categorical probabilities should never be exactly 0; use `0.01` or apply Laplace smoothing at classification time.

---

## Observed Features Schema

```yaml
observed_features:
  <feature_name>: <value>           # numeric for Gaussian features, string category for categoricals
  # ...

observation_weight: <float>          # [0, 1]; how much to trust the observation

# Examples of observation_weight calibration:
# - 1-2 data points (e.g., Week 1-2 of a season, <50 poker hands):       0.2 - 0.3
# - Moderate sample (Week 3-5, 100-500 hands):                           0.4 - 0.6
# - Strong sample (Week 6-10, 500-2000 hands):                           0.7 - 0.85
# - Saturated sample (Week 12+, 2000+ hands):                            0.85 - 0.95
```

Missing features are acceptable: drop them and flag. Do NOT impute a value; that smuggles in a prior masquerading as evidence.

---

## Full Input Schema

```yaml
# Required
archetype_taxonomy: { ... as above ... }
observed_features:  { ... as above ... }
observation_weight: <float in [0, 1]>

# Optional
archetype_prior:                    # overrides taxonomy priors; defaults to taxonomy priors (or uniform)
  <archetype_name>: <float>
  # ...priors sum to 1

correlated_feature_pairs:           # optional: downweight correlated features
  - [feature_a, feature_b, 0.5]     # (feature name, feature name, down-weight factor)

smoothing_epsilon: 0.01              # Laplace smoothing for categoricals (default)

inconclusive_threshold: 40           # confidence floor (default 40)
```

---

## Output Schema

```yaml
posterior:                          # dict<archetype, probability>; sums to 1.0
  <archetype_name>: <float>
  # ...

map_archetype: <string>              # argmax(posterior) OR "inconclusive"

classification_confidence: <float>   # [0, 100]; = max(posterior) * observation_weight * 100

best_response_hints:                 # pulled from MAP archetype's best_response
  - <string>
  - <string>

feature_contribution_breakdown:
  <feature_name>:
    map_likelihood: <float>          # L(feature | MAP)
    alternative_max: <float>         # max_{a != MAP} L(feature | a)
    likelihood_ratio: <float>        # map_likelihood / alternative_max
    contribution_log: <float>        # log(likelihood_ratio); positive = feature supports MAP
  # ...

assumptions_flagged:                 # explicit caveats
  - "Conditional independence assumed across all features"
  - "Laplace smoothing applied to 2 categorical observations"
  - "Features X and Y are correlated (r ~ 0.7); down-weighted by 0.5"
  # ...

posterior_entropy: <float>           # Shannon entropy in nats; low entropy = peaked = decisive
sample_adequacy_note: <string>       # "Observation weight 0.7 -- add 2-3 more weeks to sharpen"
```

---

## Worked Example: 6-Archetype Fantasy Baseball Taxonomy

**Setting**: Yahoo H2H Categories league, 10 scoring categories (R, HR, RBI, SB, OBP, K, ERA, WHIP, QS, SV). Six archetypes (per `game-theory-principles.md` #7).

### Taxonomy

```yaml
archetype_taxonomy:

  balanced:
    prior: 0.30
    description: "Competes in all 10 categories; decided on weekly execution."
    feature_distributions:
      sp_roster_share:   {mean: 0.40, std: 0.06}
      closer_count:      {mean: 2.0, std: 0.6}
      sb_speed_count:    {mean: 3.0, std: 1.0}
      moves_per_week:    {mean: 2.5, std: 1.0}
      bid_aggression:    {low: 0.40, moderate: 0.40, high: 0.20}
    best_response:
      - "Match category-for-category; win on execution and daily lineup accuracy"
      - "No structural category to concede -- weekly lineup optimization is everything"
      - "FAAB: expect them as a bidder on most common-value targets"

  stars_and_scrubs:
    prior: 0.15
    description: "Top-heavy roster; high weekly variance; extreme boom-bust output."
    feature_distributions:
      sp_roster_share:   {mean: 0.40, std: 0.08}
      closer_count:      {mean: 1.8, std: 0.7}
      sb_speed_count:    {mean: 2.5, std: 1.0}
      moves_per_week:    {mean: 3.5, std: 1.2}
      bid_aggression:    {low: 0.20, moderate: 0.40, high: 0.40}
    best_response:
      - "If we are favorite: dampen variance (steady, high-contact bats) -- force them to lose the coin flip"
      - "If we are underdog: lean into our own variance (high-K pitchers, high-HR bats)"
      - "Their weekly output is bimodal -- expect blowout wins or blowout losses"

  punt_sv:
    prior: 0.15
    description: "No real closers; concedes SV for elite ratio pitchers."
    feature_distributions:
      sp_roster_share:   {mean: 0.35, std: 0.05}
      closer_count:      {mean: 0.3, std: 0.4}
      sb_speed_count:    {mean: 3.0, std: 1.0}
      moves_per_week:    {mean: 2.5, std: 1.0}
      bid_aggression:    {low: 0.50, moderate: 0.30, high: 0.20}
    best_response:
      - "SV is a free win for them -- don't fight it"
      - "They will dominate ERA/WHIP via elite starters -- concede ratios too if severely outmatched"
      - "Push all 5 hitting cats + K + QS (lock 7 of remaining 9)"

  punt_sb:
    prior: 0.15
    description: "Power-and-closer roster; no speed threats; concedes SB."
    feature_distributions:
      sp_roster_share:   {mean: 0.40, std: 0.06}
      closer_count:      {mean: 2.2, std: 0.7}
      sb_speed_count:    {mean: 0.8, std: 0.7}
      moves_per_week:    {mean: 2.5, std: 1.0}
      bid_aggression:    {low: 0.50, moderate: 0.30, high: 0.20}
    best_response:
      - "SB is a free win for us -- lock speed guys even at the cost of batting average"
      - "They will dominate HR/RBI -- concede if outmatched"
      - "Push SB, OBP, ratios (ERA/WHIP), QS (lock 5 of those 5 plus pick up 1)"

  punt_wins_qs:
    prior: 0.10
    description: "All-hitting roster + RP-only pitching staff; concedes QS and usually K."
    feature_distributions:
      sp_roster_share:   {mean: 0.20, std: 0.05}
      closer_count:      {mean: 3.0, std: 0.8}
      sb_speed_count:    {mean: 3.0, std: 1.0}
      moves_per_week:    {mean: 4.0, std: 1.2}
      bid_aggression:    {low: 0.30, moderate: 0.40, high: 0.30}
    best_response:
      - "Concede K and QS; don't stream starting pitchers against them"
      - "They will dominate SV and usually ratios (RP-heavy staff has low WHIP/ERA)"
      - "Push all 5 hitting cats -- lock 5; then we need 1 of {K, ERA, WHIP}"

  hitter_heavy:
    prior: 0.15
    description: "Tilted toward hitting; not a pure punt, but pitching is thin."
    feature_distributions:
      sp_roster_share:   {mean: 0.28, std: 0.05}
      closer_count:      {mean: 1.5, std: 0.7}
      sb_speed_count:    {mean: 3.0, std: 1.0}
      moves_per_week:    {mean: 3.0, std: 1.0}
      bid_aggression:    {low: 0.30, moderate: 0.40, high: 0.30}
    best_response:
      - "They will win most hitting cats but not dominate -- slight tilt, not a punt"
      - "Adjust category pressures by ~15-20 pts: K/QS slightly more reachable, HR/RBI slightly harder"
      - "Probe for trade: they likely have surplus bats we can consolidate for a pitcher"
```

---

## Worked Example: Step-by-Step Posterior Computation

**Observed features** (the target opponent after 4 weeks):

```yaml
observed_features:
  sp_roster_share:   0.22    # low -- thin on starters
  closer_count:      3       # heavy RP
  sb_speed_count:    2       # moderate speed
  moves_per_week:    4.2     # high activity
  bid_aggression:    high    # active FAAB bidder

observation_weight: 0.7
```

### Step 1: Gaussian log-likelihoods per feature per archetype

`log L(x | mean, std) = -log(std * sqrt(2*pi)) - 0.5 * ((x - mean) / std)^2`

#### sp_roster_share = 0.22

| Archetype | mean | std | z-score | log L |
|-----------|------|-----|---------|-------|
| balanced | 0.40 | 0.06 | -3.00 | -6.31 |
| stars_and_scrubs | 0.40 | 0.08 | -2.25 | -4.24 |
| punt_sv | 0.35 | 0.05 | -2.60 | -5.41 |
| punt_sb | 0.40 | 0.06 | -3.00 | -6.31 |
| **punt_wins_qs** | **0.20** | **0.05** | **+0.40** | **-2.14** |
| hitter_heavy | 0.28 | 0.05 | -1.20 | -2.83 |

Interpretation: sp_roster_share=0.22 is highly diagnostic. Only `punt_wins_qs` expects values this low.

#### closer_count = 3

| Archetype | mean | std | z-score | log L |
|-----------|------|-----|---------|-------|
| balanced | 2.0 | 0.6 | +1.67 | -1.80 |
| stars_and_scrubs | 1.8 | 0.7 | +1.71 | -2.03 |
| punt_sv | 0.3 | 0.4 | +6.75 | -23.70 |
| punt_sb | 2.2 | 0.7 | +1.14 | -1.22 |
| **punt_wins_qs** | **3.0** | **0.8** | **0.00** | **-0.69** |
| hitter_heavy | 1.5 | 0.7 | +2.14 | -2.86 |

Interpretation: 3 closers strongly supports `punt_wins_qs`, rules out `punt_sv`.

#### sb_speed_count = 2

| Archetype | mean | std | z-score | log L |
|-----------|------|-----|---------|-------|
| balanced | 3.0 | 1.0 | -1.00 | -1.42 |
| stars_and_scrubs | 2.5 | 1.0 | -0.50 | -1.04 |
| punt_sv | 3.0 | 1.0 | -1.00 | -1.42 |
| punt_sb | 0.8 | 0.7 | +1.71 | -2.03 |
| punt_wins_qs | 3.0 | 1.0 | -1.00 | -1.42 |
| hitter_heavy | 3.0 | 1.0 | -1.00 | -1.42 |

Interpretation: weakly discriminating. `punt_sb` slightly penalized; `stars_and_scrubs` slightly favored.

#### moves_per_week = 4.2

| Archetype | mean | std | z-score | log L |
|-----------|------|-----|---------|-------|
| balanced | 2.5 | 1.0 | +1.70 | -2.36 |
| stars_and_scrubs | 3.5 | 1.2 | +0.58 | -1.27 |
| punt_sv | 2.5 | 1.0 | +1.70 | -2.36 |
| punt_sb | 2.5 | 1.0 | +1.70 | -2.36 |
| **punt_wins_qs** | **4.0** | **1.2** | **+0.17** | **-1.11** |
| hitter_heavy | 3.0 | 1.0 | +1.20 | -1.64 |

#### bid_aggression = "high" (categorical)

| Archetype | P(high) | log L |
|-----------|---------|-------|
| balanced | 0.20 | -1.61 |
| stars_and_scrubs | 0.40 | -0.92 |
| punt_sv | 0.20 | -1.61 |
| punt_sb | 0.20 | -1.61 |
| punt_wins_qs | 0.30 | -1.20 |
| hitter_heavy | 0.30 | -1.20 |

### Step 2: Sum log-likelihoods across features (conditional independence)

| Archetype | sp | closer | sb | moves | bid | sum log L |
|-----------|-----|--------|-----|-------|-----|-----------|
| balanced | -6.31 | -1.80 | -1.42 | -2.36 | -1.61 | **-13.50** |
| stars_and_scrubs | -4.24 | -2.03 | -1.04 | -1.27 | -0.92 | **-9.50** |
| punt_sv | -5.41 | -23.70 | -1.42 | -2.36 | -1.61 | **-34.50** |
| punt_sb | -6.31 | -1.22 | -2.03 | -2.36 | -1.61 | **-13.53** |
| **punt_wins_qs** | **-2.14** | **-0.69** | **-1.42** | **-1.11** | **-1.20** | **-6.56** |
| hitter_heavy | -2.83 | -2.86 | -1.42 | -1.64 | -1.20 | **-9.95** |

### Step 3: Combine with prior

`log_posterior_unnorm = sum_log_L + log(prior)`

| Archetype | sum log L | prior | log(prior) | log_post_unnorm |
|-----------|-----------|-------|-----------|-----------------|
| balanced | -13.50 | 0.30 | -1.20 | -14.70 |
| stars_and_scrubs | -9.50 | 0.15 | -1.90 | -11.40 |
| punt_sv | -34.50 | 0.15 | -1.90 | -36.40 |
| punt_sb | -13.53 | 0.15 | -1.90 | -15.43 |
| **punt_wins_qs** | **-6.56** | **0.10** | **-2.30** | **-8.86** |
| hitter_heavy | -9.95 | 0.15 | -1.90 | -11.85 |

### Step 4: Subtract max and exponentiate

Max log_post_unnorm = -8.86 (punt_wins_qs). Subtract:

| Archetype | shifted | exp(shifted) |
|-----------|---------|--------------|
| balanced | -5.84 | 0.0029 |
| stars_and_scrubs | -2.54 | 0.0789 |
| punt_sv | -27.54 | 1.1e-12 |
| punt_sb | -6.57 | 0.0014 |
| punt_wins_qs | 0.00 | 1.0000 |
| hitter_heavy | -2.99 | 0.0502 |

### Step 5: Normalize

Sum of exp(shifted) = 1.1334. Divide each by the sum:

| Archetype | Normalized Posterior |
|-----------|---------------------|
| balanced | 0.0026 |
| stars_and_scrubs | 0.0696 |
| punt_sv | 1.0e-12 |
| punt_sb | 0.0012 |
| **punt_wins_qs** | **0.8823** |
| hitter_heavy | 0.0443 |

Sum: 1.0000 (verified).

### Step 6: MAP and confidence

```
map_archetype = punt_wins_qs
classification_confidence = 0.8823 * 0.7 * 100 = 61.8
```

Above the 40 threshold. MAP is reported with "solid" confidence band.

### Step 7: Feature contribution breakdown

For each feature compute LR = L(feature | punt_wins_qs) / max_{a != punt_wins_qs} L(feature | a):

| Feature | L(MAP) | 2nd-best archetype | L(2nd-best) | LR |
|---------|--------|--------------------|-----|----|
| sp_roster_share | exp(-2.14) = 0.117 | hitter_heavy: exp(-2.83) = 0.059 | 0.059 | 1.98 |
| closer_count | exp(-0.69) = 0.501 | punt_sb: exp(-1.22) = 0.295 | 0.295 | 1.70 |
| sb_speed_count | exp(-1.42) = 0.241 | stars_and_scrubs: exp(-1.04) = 0.353 | 0.353 | 0.68 |
| moves_per_week | exp(-1.11) = 0.329 | stars_and_scrubs: exp(-1.27) = 0.281 | 0.281 | 1.17 |
| bid_aggression | 0.30 | stars_and_scrubs: 0.40 | 0.40 | 0.75 |

Reading this: `sp_roster_share` and `closer_count` are the two features pulling toward `punt_wins_qs`; the other three are neutral or mildly against. Reassuring -- the classification is driven by the two structurally decisive roster-composition signals, not by cherry-picked noise.

### Step 8: Final output

```yaml
posterior:
  balanced: 0.003
  stars_and_scrubs: 0.070
  punt_sv: 0.000
  punt_sb: 0.001
  punt_wins_qs: 0.882
  hitter_heavy: 0.044

map_archetype: punt_wins_qs
classification_confidence: 61.8

best_response_hints:
  - "Concede K and QS; don't stream starting pitchers against them"
  - "They will dominate SV and usually ratios (RP-heavy staff has low WHIP/ERA)"
  - "Push all 5 hitting cats -- lock 5; then we need 1 of {K, ERA, WHIP}"

feature_contribution_breakdown:
  sp_roster_share:    {map_likelihood: 0.117, alternative_max: 0.059, likelihood_ratio: 1.98}
  closer_count:       {map_likelihood: 0.501, alternative_max: 0.295, likelihood_ratio: 1.70}
  sb_speed_count:     {map_likelihood: 0.241, alternative_max: 0.353, likelihood_ratio: 0.68}
  moves_per_week:     {map_likelihood: 0.329, alternative_max: 0.281, likelihood_ratio: 1.17}
  bid_aggression:     {map_likelihood: 0.300, alternative_max: 0.400, likelihood_ratio: 0.75}

assumptions_flagged:
  - "Conditional independence assumed across all 5 features"
  - "sp_roster_share and closer_count may be correlated (a true punt_wins_qs roster drives both); posterior may be slightly over-peaked"
  - "Feature distributions are SME priors; empirical refit recommended after 1 full season"

posterior_entropy: 0.48            # low -- posterior is peaked
sample_adequacy_note: "Observation weight 0.7 reflects ~4 weeks of data; confidence will sharpen with 2-3 more weeks"
```

---

## Sequential Update Worksheet

When Week t+1 arrives, use Week t's posterior as the new prior:

```yaml
# Week t posterior (previous output)
prior_t_plus_1:
  balanced: 0.003
  stars_and_scrubs: 0.070
  punt_sv: 0.000
  punt_sb: 0.001
  punt_wins_qs: 0.882
  hitter_heavy: 0.044

# Observe new features in Week t+1
new_observed_features:
  sp_roster_share:   0.21
  closer_count:      3
  sb_speed_count:    2
  moves_per_week:    5.1
  bid_aggression:    high

# Compute Week t+1 posterior using prior_t_plus_1
# (Same procedure as Steps 1-5 above, but plug in prior_t_plus_1 instead of the taxonomy priors)
```

**Key guardrail for sequential updates**: if observations are *not* independent over time (e.g., roster composition is persistent across weeks -- it barely changes), do not feed the same feature in each week; compute it once across the full observation window. Use truly-new signals (this week's moves, this week's bids) for sequential updating.

---

## Domain-Neutral Taxonomy Template (fill-in)

Copy this skeleton and fill for your domain (poker, DFS, M&A, etc.):

```yaml
archetype_taxonomy:

  <archetype_A>:
    prior: 0.??
    description: "<one-line summary>"
    feature_distributions:
      <feature_1>: {mean: ??, std: ??}     # OR categorical: {cat_1: ??, cat_2: ??, ...}
      <feature_2>: {...}
      <feature_3>: {...}
      # ...
    best_response:
      - "<hint 1>"
      - "<hint 2>"

  <archetype_B>:
    prior: 0.??
    description: "..."
    feature_distributions:
      <feature_1>: {...}
      # ... (must use the SAME feature names as archetype_A)
    best_response:
      - "..."

  # ... up to N archetypes

# Sanity checks:
# - Sum of priors across archetypes = 1.0
# - Every archetype uses the same feature-name set
# - Every feature is either Gaussian (mean, std) or categorical (cat -> prob)
# - Categorical probabilities per feature per archetype sum to 1.0
# - best_response is non-empty for every archetype
```
