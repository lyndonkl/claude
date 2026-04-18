# MLB Opponent Profiler -- Methodology

Six sections:

1. [Yahoo Scrape Flow](#yahoo-scrape-flow) -- exact URLs, what to parse from each
2. [Feature Extraction](#feature-extraction) -- formulas that turn scraped data into the feature dict
3. [Classifier Invocation](#classifier-invocation) -- how to call `opponent-archetype-classifier` with the MLB taxonomy
4. [Cat-Strength Estimation](#cat-strength-estimation) -- 0-100 per-cat score from roster composition
5. [Read-Modify-Write Protocol](#read-modify-write-protocol) -- preserving manually-authored notes
6. [Sequential-Update Protocol](#sequential-update-protocol) -- how last week's posterior becomes this week's prior
7. [Graceful Degradation](#graceful-degradation) -- scrape failures, missing features, stale auth

---

## Yahoo Scrape Flow

League ID is fixed at **23756** for the entire season. Team IDs 1-12 are stable. The user's team_id is NOT in the 11 profiled opponents.

All scrapes require an authenticated Chrome session via the `claude-in-chrome` MCP tools (`mcp__claude-in-chrome__navigate`, `mcp__claude-in-chrome__get_page_text`, `mcp__claude-in-chrome__read_page`). Yahoo has no public API for this league.

### URL 1: League teams index

```
https://baseball.fantasysports.yahoo.com/b1/23756/teams
```

Parse:
- Team rows: `team_name`, `team_id`, `manager_alias`, current record (W-L-T), current rank
- Last-login timestamp per manager (shown as "Active Nm ago" or "Active Nh ago" or a date)

Scrape this **once** per refresh run (serves all 11 teams). Cache in memory across the 11-team iteration.

### URL 2: Individual team page

```
https://baseball.fantasysports.yahoo.com/b1/23756/{team_id}
```

Parse:
- Full active roster: positions C, 1B, 2B, SS, 3B, OF, Util, SP (multiple), RP (multiple), BN
- Per player: name, position eligibility, MLB team, injury status, starting/benched today
- `faab_remaining` ($ remaining from original $100)
- `waiver_priority` (#1-12 in reverse-standings order)

Fetch once per target team. Repeat for each of the 11.

### URL 3: Draft results (per team)

```
https://baseball.fantasysports.yahoo.com/b1/23756/{team_id}/draftresults
```

Parse:
- Per draft pick: round number, overall pick, player name, player position, player cat-profile (derive via lookup: speed vs power vs ratio vs closer)

Fetched **once per team per season** (draft is immutable). Cache aggressively. If cached file exists at `context/opponents/_cache/team_{team_id}_draft.json`, skip this scrape.

### URL 4: Transactions (filtered per team)

```
https://baseball.fantasysports.yahoo.com/b1/23756/transactions?tid={team_id}
```

Parse for the current season-to-date:
- Adds: player name, source (Waivers/FA), date, FAAB $ spent (if waiver)
- Drops: player name, date
- Trades: counterparty team_id, players exchanged, date, accepted/rejected/pending
- Trade offers: sent/received count (even when rejected/expired)

Fetched **weekly** per team. Delta against the previous week's cached transactions gives "new activity this week".

### Cache strategy

- Draft results cached once (immutable)
- Transactions cached weekly at `context/opponents/_cache/team_{team_id}_txns_wk{NN}.json`
- Team index and team page are re-fetched every refresh (roster churn is fast)

---

## Feature Extraction

Nine MLB-specific features feed the classifier. All formulas below take the scraped data as input and emit a numeric (or boolean) value.

### Roster-composition features

```
sp_roster_share = count(players with primary_pos == SP) / total_active_roster_slots

closer_count = count(RP-eligible players with save_role_certainty >= 60 per mlb-closer-tracker)

sb_speed_count = count(hitters with projected SB >= 20 per FanGraphs ATC)

power_bat_count = count(hitters with projected HR >= 25 per FanGraphs ATC)
```

Cross-reference with `mlb-closer-tracker` for `save_role_certainty` (don't trust raw Yahoo position eligibility -- any RP is Yahoo-eligible but only true 9th-inning arms count for `closer_count`).

### Activity features

```
moves_per_week = count(adds + drops in season-to-date) / weeks_elapsed

faab_spent_pct = ($100 - faab_remaining) / $100

faab_avg_bid = total_faab_spent / count(successful waiver claims with non-zero bid)
             = null if count == 0

lineup_set_daily = (count(benched players whose MLB game is active) over last 7 days == 0)
                   AND (count(starting players whose MLB game is NOT active) over last 7 days == 0)
```

`lineup_set_daily` requires cross-referencing Yahoo's bench/start list against MLB.com daily lineups from `mlb-matchup-analyzer` output. If we can't validate, set `null` and flag in assumptions.

### Trade features

```
trade_offers_sent     = count(trade offers this manager initiated, season-to-date)
trade_offers_received = count(trade offers this manager received, season-to-date)
```

Both come from the transactions page (Yahoo shows proposed/rejected/expired trades).

### Record feature

```
record_last_2_weeks = "W-L-T" from last 2 full matchup periods

# Derived for classifier (not stored in profile):
recent_win_pct = W / (W + L + 0.5*T) from last 2 weeks
```

### Recency feature

```
days_since_last_login = (today - last_active_timestamp).days

# Derived for classifier:
# map to a continuous numeric feature for Gaussian likelihood
```

### Missing feature handling

If any feature cannot be computed (scrape failure, NA player, unparseable timestamp): pass `None` to the classifier (it will drop it per its contract) AND record in the output `scrape_errors` block. Never impute -- imputation biases the classification.

---

## Classifier Invocation

**This skill does NOT implement Bayes.** All Bayesian math -- likelihood computation, log-space normalization, MAP selection, confidence scoring -- is delegated to `opponent-archetype-classifier`.

The invocation contract:

```yaml
# Input payload to opponent-archetype-classifier
archetype_taxonomy: <from template.md#mlb-10-archetype-taxonomy>
observed_features: <from feature extraction, dict<name, value|null>>
archetype_prior: <prior_profile.posterior if supplied, else taxonomy priors>
observation_weight: <0.25 | 0.45 | 0.65 | 0.80 | 0.90, by current week>
correlated_feature_pairs: <from template.md bottom of taxonomy>
inconclusive_threshold: 40         # default; leave at default
```

The classifier returns:

```yaml
posterior:                         # 10 archetypes -> probability, sums to 1
map_archetype: <string or "inconclusive">
classification_confidence: 0-100
best_response_hints: [<strings>]
feature_contribution_breakdown:    # per-feature LR breakdown
assumptions_flagged: [<strings>]
```

### Mapping classifier output to the profile

```
if classifier.map_archetype == "inconclusive":
    profile.archetype = "unknown"
else:
    profile.archetype = classifier.map_archetype

profile.archetype_confidence = classifier.classification_confidence / 100
profile.archetype_evidence = top-3 features by feature_contribution_breakdown.likelihood_ratio
profile.posterior = classifier.posterior          # store full posterior in frontmatter
```

### What NOT to do in this skill

- Compute Gaussian likelihoods directly -- delegate
- Normalize posterior in log-space -- delegate
- Select MAP -- delegate
- Override or second-guess classifier output -- record it as-is

If the classifier output looks wrong (e.g. `punt_sv` MAP on a team with 4 closers), the fix is in the **taxonomy** (template.md) or the **feature extraction** (above), not in this skill's post-processing.

### Observation weight lookup

| Week | Weight | Rationale |
|------|--------|-----------|
| 1-2 | 0.25 | Draft-only evidence; very noisy |
| 3-4 | 0.45 | First waivers visible |
| 5-7 | 0.65 | Patterns stabilizing |
| 8-11 | 0.80 | Behavior well-characterized |
| 12+ | 0.90 | Remaining doubt is true ambiguity |

Hardcoded by week number at run time. Do not allow callers to override (prevents confidence inflation via artificially high weights).

---

## Cat-Strength Estimation

`cat_strength[cat]` (0-100, 50 = league average) is NOT classifier output. It is a separate roster-based estimator owned by this skill.

### Algorithm

For each of the 10 cats, compute the team's projected season total then rank-normalize against the 12-team league:

```
for cat in [R, HR, RBI, SB, OBP, K, ERA, WHIP, QS, SV]:
    team_projection[cat] = sum(player_projection[cat] for player in starting_roster)

# Rank-normalize within the league:
for cat in [R, HR, RBI, SB, K, QS, SV]:                # counting stats: higher = better
    rank = position of team_projection[cat] within all 12 teams, 1 = best
    cat_strength[cat] = round(100 - (rank - 1) * (100/11))

for cat in [OBP]:                                       # rate: higher = better (same as above)
    (same formula)

for cat in [ERA, WHIP]:                                 # rate: LOWER = better
    rank = position of team_projection[cat] within 12 teams, 1 = best (lowest)
    cat_strength[cat] = round(100 - (rank - 1) * (100/11))
```

This yields: league-best in a cat -> 100, league-worst -> 0, median -> 50.

### Rate-stat weighting

OBP/ERA/WHIP are PA- or IP-weighted, not straight averages:

```
team_OBP = sum(player_OBP * player_PA) / sum(player_PA)
team_ERA = sum(player_ER) / (sum(player_IP) / 9)
team_WHIP = (sum(player_H) + sum(player_BB)) / sum(player_IP)
```

### Derivations

```
presumed_punts = [cat for cat in cats if cat_strength[cat] < 35]
likely_pushes  = [cat for cat in cats if cat_strength[cat] > 65]
```

### Why this stays out of the classifier

The classifier's taxonomy gives `archetype -> best_response` strings, not numeric cat strengths. A `balanced` team with a weak SP staff still has weak K/ERA/WHIP/QS -- we do NOT want to paper over that with "balanced = 50s". Compute cat_strength from the roster every refresh.

---

## Read-Modify-Write Protocol

**Critical rule: never clobber manually-authored sections.**

The profile template defines 9 sections. Five are manual (§1, §5, §6, §8, §9). Four are machine-refreshed (§2, §3, §4, §7) plus frontmatter.

### Algorithm

```
1. Open context/opponents/<slug>.md
   - If file does not exist: instantiate from template.md#per-opponent-profile-template
     with manual sections stubbed as TODOs; skip preservation logic.
   - If exists: parse into sections keyed by heading.

2. Extract manual sections verbatim (byte-for-byte):
     manual = {
       "Summary":        <raw markdown of §1>,
       "Weaknesses":     <raw markdown of §5>,
       "Best response":  <raw markdown of §6>,
       "Reactivity":     <raw markdown of §8>,
       "Open questions": <raw markdown of §9>,
     }

3. Rebuild the file:
     - New frontmatter (last_updated, confidence, source_urls, posterior, scrape_errors)
     - §1 Summary = manual["Summary"]
     - §2 Archetype = freshly generated YAML from classifier output
     - §3 Category strength = freshly generated YAML from cat_strength estimator
     - §4 Behavioral = freshly generated YAML from feature extraction
     - §5 Weaknesses = manual["Weaknesses"]
     - §6 Best response = manual["Best response"]
     - §7 Matchup history = freshly generated (only updated if we played them this week)
     - §8 Reactivity = manual["Reactivity"]
     - §9 Open questions = manual["Open questions"]

4. Write to <slug>.md.tmp, fsync, rename atomically to <slug>.md.
```

### Diff-validation gate

Before rename, compute `diff old_file new_file`. The diff MUST only touch:
- YAML frontmatter
- §2 Archetype
- §3 Category strength
- §4 Behavioral signals
- §7 Matchup history

If the diff touches §1, §5, §6, §8, or §9, ABORT the write and log an error. Manual content was almost dropped.

### New-file bootstrap

If `<slug>.md` does not exist (new opponent, or first run), instantiate from the template with manual sections stubbed:

```markdown
## 1. Summary
_TODO: hand-author a one-paragraph characterization._
```

Warn the caller that manual sections are stubs and need user attention.

---

## Sequential-Update Protocol

Bayesian archetype inference is cumulative. Each week's posterior becomes next week's prior. This is how classification_confidence rises from 0.25 in Week 2 to 0.80+ by Week 8.

### Week-by-week flow

```
# Week 1 (draft just completed):
#   No prior_profile exists.
#   prior = taxonomy priors (hard-coded in template.md)
#   observation_weight = 0.25
posterior_wk1 = classifier(taxonomy, features_wk1, taxonomy_priors, 0.25)
write profile with posterior_wk1

# Week 2:
#   prior = posterior_wk1
#   observation_weight = 0.25  (still very light)
posterior_wk2 = classifier(taxonomy, features_wk2, posterior_wk1, 0.25)

# Week 3:
#   prior = posterior_wk2
#   observation_weight = 0.45
posterior_wk3 = classifier(taxonomy, features_wk3, posterior_wk2, 0.45)

# ... and so on through the season.
```

### What to re-feed vs not

**Flow features** (change weekly -- always re-feed):
- `moves_per_week`, `faab_spent_pct`, `faab_avg_bid`, `trade_offers_sent`, `trade_offers_received`, `record_last_2_weeks`, `days_since_last_login`

**State features** (slowly-changing -- re-feed each week is fine, but be aware of overconfidence):
- `sp_roster_share`, `closer_count`, `sb_speed_count`, `power_bat_count`, `lineup_set_daily`

If state features are re-fed every week unchanged, the classifier effectively "sees" the same evidence N times and confidence grows artificially. Counter-pattern: feed state features ONCE per month with high weight, then omit them on the other weekly refreshes. This skill takes the **simple approach (re-feed every week) and relies on the classifier's `observation_weight` cap** (max 0.90) to bound overconfidence.

### When to reset the prior

Exception: if `prior_profile.confidence < 0.20`, ignore the prior and restart from taxonomy priors. A prior below 0.20 confidence is essentially noise and pollutes the posterior. Log this as an assumption.

Another reset condition: if the user manually edits the profile's `archetype` field (e.g., overrides to `unknown` after observing a behavioral shift not captured by features), reset prior on next refresh.

---

## Graceful Degradation

Real Yahoo scrapes fail: timeouts, re-auth required, server errors, unexpected HTML changes. A robust profiler emits partial profiles rather than hard-failing.

### Failure modes and handling

| Failure | Action |
|---------|--------|
| Teams-index page 5xx | Abort entire run; cannot resolve team identities. Log and exit. |
| Individual team page 4xx | Mark roster-composition features as `null`, record URL in `scrape_errors`, drop profile confidence by 0.15 |
| Draft-results page 4xx | Use cached draft data if available; else skip draft-derived features |
| Transactions page 4xx | Mark activity features as `null`, record URL, drop confidence by 0.10 |
| Auth expired mid-run | Pause, surface "Re-authenticate Chrome" to the caller, do NOT write partial profiles until resumed |
| Unparseable HTML (Yahoo layout changed) | Same as 4xx -- mark null, record, lower confidence. Also flag the parser for review. |

### Confidence bookkeeping

The profile's `confidence:` field in frontmatter is:

```
base_confidence = classifier.classification_confidence / 100
confidence = base_confidence - 0.15 * (team_page_failed)
                             - 0.10 * (transactions_page_failed)
                             - 0.05 * (any other scrape failed)
confidence = max(confidence, 0.10)   # never below 0.10
```

### Never fail silently

Every scrape failure is recorded in `scrape_errors:` in frontmatter. Downstream agents check `scrape_errors` before acting on any profile -- a profile with `scrape_errors` present is treated as degraded (see `mlb-signal-emitter` contract).

### One-shot mode never writes signal files

If invoked in single-team mode (e.g., before a trade analysis), write only the profile file -- no `signals/wkNN-opponent-profiles.md`. The weekly signal is exclusively for the `all_opponents: true` Monday-morning run.
