---
name: mlb-opponent-profiler
description: Weekly refresh of per-opponent archetype + behavioral profiles for the 11 opposing teams in the user's Yahoo Fantasy Baseball league (ID 23756). Thin baseball-specific wrapper around the domain-neutral `opponent-archetype-classifier` -- provides the 10-archetype MLB taxonomy (balanced, stars_and_scrubs, punt_sv, punt_sb, punt_wins_qs, hitter_heavy, pitcher_heavy, inactive, frustrated_active, unknown), extracts MLB features from Yahoo pages (draft distribution, FAAB spend, waiver pattern, roster composition, lineup consistency, trade activity, recent record, activity recency), invokes the classifier, and writes/updates `context/opponents/<team-slug>.md` files per `opponent-profile-schema.md`. Read-modify-write preserves manual notes. Emits a weekly summary signal at `signals/wkNN-opponent-profiles.md`. Use when user says "opponent profiling", "classify opposing manager", "update opponent profiles", "refresh opponents", "weekly opponent scout", or "MLB fantasy opponent archetype".
---
# MLB Opponent Profiler

## Table of Contents
- [Example](#example)
- [Workflow](#workflow)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Example

**Scenario**: Monday morning of Week 5. Refresh profile for `Springfield Isotopes` (manager Nikolay) after observing another high-activity week (7 moves, $14 spent on adds, 4-1 matchup win).

**Inputs**:
```yaml
team_name: "Springfield Isotopes"
yahoo_session: <authenticated chrome context>
prior_profile:                       # from context/opponents/springfield-isotopes.md (Week 4)
  archetype: balanced
  archetype_confidence: 0.50
  posterior: {balanced: 0.42, stars_and_scrubs: 0.18, punt_sv: 0.02, punt_sb: 0.04,
              punt_wins_qs: 0.03, hitter_heavy: 0.12, pitcher_heavy: 0.08,
              inactive: 0.00, frustrated_active: 0.11, unknown: 0.00}
```

**Step 1 -- Yahoo scrape (4 pages)**: teams index, team page for `team_id=8`, draftresults, transactions filtered by `tid=8`. URLs in [methodology.md](resources/methodology.md#yahoo-scrape-flow).

**Step 2 -- MLB feature extraction** yields:
```yaml
sp_roster_share: 0.35; closer_count: 2; sb_speed_count: 4; power_bat_count: 6
moves_per_week: 3.3; faab_spent_pct: 0.32; faab_avg_bid: 2.5
lineup_set_daily: true; trade_offers_sent: 1; trade_offers_received: 0
record_last_2_weeks: "8-2-0"; days_since_last_login: 0
```

**Step 3 -- Invoke `opponent-archetype-classifier`**:
```yaml
archetype_taxonomy:            # see resources/template.md -- 10 archetypes
  balanced: {...}
  stars_and_scrubs: {...}
  ...
observed_features: <from step 2>
archetype_prior: <prior_profile.posterior>     # sequential: last week's posterior is this week's prior
observation_weight: 0.65        # Week 5 -- see methodology.md observation_weight_calibration
correlated_feature_pairs:
  - [moves_per_week, faab_spent_pct]            # active managers do both
  - [sp_roster_share, closer_count]             # they trade off
```

**Step 4 -- Classifier returns**:
```yaml
posterior:
  balanced:            0.58    # up from 0.42 -- evidence accumulating
  stars_and_scrubs:    0.12
  hitter_heavy:        0.10
  frustrated_active:   0.08    # record is winning, so frustrated_active down
  pitcher_heavy:       0.07
  punt_sb:             0.03
  punt_sv:             0.01
  punt_wins_qs:        0.01
  inactive:            0.00
  unknown:             0.00

map_archetype: balanced
classification_confidence: 37.7      # 0.58 * 0.65 * 100 -- still just under 40
best_response_hints:
  - "Match cat-for-cat; decided on execution"
  - "Include in N-estimate for every common-value FAAB target"
  - "Active manager -- probe for fair consolidation trades"
```

**Step 5 -- Read existing `context/opponents/springfield-isotopes.md`, preserve manual notes, update machine-generated sections**:

The "Summary", "Apparent weaknesses", "Best response" and "Open questions" sections contain hand-authored user notes -- **keep verbatim**. Only these get refreshed:
- YAML frontmatter: `last_updated`, `confidence`, `source_urls`
- Section 2 (Archetype): archetype, archetype_confidence, archetype_evidence
- Section 3 (Category strength): cat_strength, presumed_punts, likely_pushes
- Section 4 (Behavioral): activity_level, last_active, waiver_aggression, faab_remaining, faab_avg_bid_pct, trade_propensity

**Step 6 -- Emit weekly signal** at `signals/wk05-opponent-profiles.md`:
```markdown
---
type: opponent_profile_summary
date: 2026-04-20
week: 5
emitted_by: mlb-opponent-profiler
confidence: 0.65
source_urls: [<11 team pages + transactions + teams>]
---
## Archetype shifts since Week 4
- Springfield Isotopes: balanced 0.42 -> 0.58 (confidence 0.50 -> 0.66). Nikolay continues active pattern, record confirms execution.
- Jennys Team: inactive 0.78 -> 0.84 (confidence 0.80 -> 0.85). Still zero moves. Profile hardening.
- ...9 more

## New reactivity triggers fired
- Team 7 (Kenyi) -- outbid us on Wade Miley at $14; shift `faab_avg_bid_pct` up
```

## Workflow

Copy this checklist and track progress:

```
Opponent Profiler Progress (per team, x 11 for all_opponents):
- [ ] Step 1: Resolve team identity (team_name -> team_id, manager_alias)
- [ ] Step 2: Scrape 4 Yahoo pages for this team
- [ ] Step 3: Extract MLB-specific features (9 features; see template.md)
- [ ] Step 4: Load prior_profile.posterior as archetype_prior (sequential update)
- [ ] Step 5: Invoke opponent-archetype-classifier with 10-archetype MLB taxonomy
- [ ] Step 6: Compute cat_strength (0-100 per cat) from roster composition
- [ ] Step 7: Read existing context/opponents/<slug>.md; identify manual-notes sections
- [ ] Step 8: Write updated file atomically (preserve manual notes)
- [ ] Step 9: (at end of batch) Emit signals/wkNN-opponent-profiles.md summary
```

**Step 1: Resolve team identity**

Input is either a single `team_name` (case-insensitive, fuzzy match against canonical Yahoo names) or `all_opponents: true` (iterate over team_ids 1-12, skipping user's own team_id). Map to `team_id` and `team-slug` (lowercased, hyphenated).

- [ ] If `team_name` does not match any Yahoo team, return error -- do not guess
- [ ] `team-slug` must match the filename on disk at `context/opponents/<slug>.md` (or create new file if absent)

**Step 2: Scrape 4 Yahoo pages**

Exact URL flow documented in [resources/methodology.md](resources/methodology.md#yahoo-scrape-flow). Pages needed:

- [ ] `https://baseball.fantasysports.yahoo.com/b1/23756/teams` -- manager, last-login, W-L
- [ ] `https://baseball.fantasysports.yahoo.com/b1/23756/<team_id>` -- roster + FAAB remaining
- [ ] `https://baseball.fantasysports.yahoo.com/b1/23756/<team_id>/draftresults` -- draft pick distribution
- [ ] `https://baseball.fantasysports.yahoo.com/b1/23756/transactions?tid=<team_id>` -- adds/drops/bids/trades
- [ ] Each scrape records the exact URL in `source_urls` (for citation)
- [ ] If any page returns 4xx/5xx or auth failure, degrade gracefully (see Guardrails #3)

**Step 3: Extract MLB features**

Computed from scraped pages. See [resources/methodology.md](resources/methodology.md#feature-extraction) for exact formulas.

- [ ] `sp_roster_share`, `closer_count`, `sb_speed_count`, `power_bat_count` (roster composition)
- [ ] `moves_per_week`, `faab_spent_pct`, `faab_avg_bid` (waiver activity)
- [ ] `lineup_set_daily` (bool -- any benched-but-MLB-starting players in last 7 days?)
- [ ] `trade_offers_sent`, `trade_offers_received`
- [ ] `record_last_2_weeks`, `days_since_last_login`

**Step 4: Sequential-update prior**

Read `prior_profile.posterior` (if supplied) and pass as `archetype_prior` to the classifier. This is the key sequential-Bayes move: last week's posterior becomes this week's prior.

- [ ] If no `prior_profile`, use taxonomy priors (Week 1 only)
- [ ] If `prior_profile.posterior` sums to != 1.0, normalize and flag in `assumptions_flagged`
- [ ] Observation weight rises with week number: Wk1-2 = 0.25, Wk3-4 = 0.45, Wk5-7 = 0.65, Wk8-11 = 0.80, Wk12+ = 0.90

**Step 5: Invoke `opponent-archetype-classifier`**

Pass the 10-archetype MLB taxonomy from [resources/template.md](resources/template.md#mlb-10-archetype-taxonomy) along with the observed features, prior, and observation_weight. **Do not re-implement Bayesian math in this skill.** The classifier returns `posterior`, `map_archetype`, `classification_confidence`, `best_response_hints`, `feature_contribution_breakdown`, `assumptions_flagged`.

- [ ] Pass `correlated_feature_pairs` (see Guardrails #1)
- [ ] If classifier returns `map_archetype: "inconclusive"`, write archetype as `unknown` with confidence as returned
- [ ] Do not override or reinterpret classifier output -- store it as-is

**Step 6: Compute `cat_strength` (0-100 per cat)**

Classifier returns the archetype; the 10 per-cat strength scores come from a separate roster-based estimator (this is MLB-specific and stays in this skill). Method in [resources/methodology.md](resources/methodology.md#cat-strength-estimation).

- [ ] Sum projected season totals for each cat across roster
- [ ] Normalize to 0-100 where 50 is league average
- [ ] Derive `presumed_punts`: cats where score < 35
- [ ] Derive `likely_pushes`: cats where score > 65

**Step 7: Read existing file, identify manual-notes sections**

**Critical: this skill never overwrites manually-authored notes.** See [resources/methodology.md](resources/methodology.md#read-modify-write-protocol).

- [ ] Open `context/opponents/<slug>.md`; if not present, emit new file from template
- [ ] Preserve Sections 1 (Summary), 5 (Apparent weaknesses / surpluses), 6 (Best response), 8 (Reactivity triggers), 9 (Open questions) verbatim
- [ ] Refresh only: frontmatter (last_updated, confidence, source_urls), Section 2 (Archetype), Section 3 (Category strength), Section 4 (Behavioral), Section 7 (Matchup history -- if we played them)

**Step 8: Write file atomically**

- [ ] Write to temp file `<slug>.md.tmp`, fsync, rename
- [ ] Validate output against [opponent-profile-schema.md](../../../yahoo-mlb/context/frameworks/opponent-profile-schema.md) frontmatter + section order before rename

**Step 9: Emit signal file**

After all 11 updates complete (for `all_opponents: true` mode), emit `signals/wkNN-opponent-profiles.md`. Format in [resources/template.md](resources/template.md#weekly-summary-signal-template).

- [ ] Include every archetype posterior that shifted by > 0.05 since last week
- [ ] Include every confidence change > 0.10
- [ ] List any reactivity-trigger events fired this week

## Common Patterns

**Pattern 1: `inactive` (dormant manager -- e.g. Jenny's Team)**
- **Signals**: `moves_per_week < 0.5`, `faab_spent_pct < 0.05`, `days_since_last_login > 3` or `lineup_set_daily = false`
- **Best-response**: Don't include in N-bidder FAAB estimates. Send consolidation trade offers. Expect roster atrophy -- exploit lineup-neglect advantage week-over-week.
- **Confidence grows fast**: inactivity is unambiguous; expect `archetype_confidence` above 0.80 by Week 4.

**Pattern 2: `punt_wins_qs` (Marmol strategy -- all-hitter + RP-only staff)**
- **Signals**: `sp_roster_share < 0.25`, `closer_count >= 3`, `moves_per_week > 3` (cycling for hitter production)
- **Best-response**: Concede K and QS (two free cat losses); lock 6 of remaining 8 cats. Do not stream SPs against them.

**Pattern 3: `punt_sv` (no closers, elite SP + hitting)**
- **Signals**: `closer_count = 0`, `sp_roster_share > 0.40`, high-end SP drafted in round 1-3
- **Best-response**: Concede SV; push all 5 hitting + K + QS + ERA + WHIP. Do not chase closers as streamers.

**Pattern 4: `frustrated_active` (active but losing -- motivated trader)**
- **Signals**: `moves_per_week > 4` AND `record_last_2_weeks` W% < 0.35
- **Best-response**: Prime trade partner. They'll respond to offers. Target their cooling stars (sell-high for them, buy-low for us).

**Pattern 5: `balanced` (the default)**
- **Signals**: No strong punts; roster composition within 1 std of league average across all features
- **Best-response**: Match cat-for-cat; matchup decided on weekly execution. Use variance-seeking when we're the underdog (`matchup_win_probability < 0.40`).

## Guardrails

1. **Classifier delegation purity.** This skill MUST NOT implement Bayesian math. If you find yourself computing posteriors, likelihoods, or normalizations, stop -- those belong in `opponent-archetype-classifier`. This skill contributes the taxonomy (MLB-specific), feature extraction (Yahoo-specific), and output formatting. Any math beyond "sum projected season totals for cat_strength" is a smell.

2. **Manual-notes preservation is non-negotiable.** Users hand-author Sections 1, 5, 6, 8, 9 with strategic notes this skill cannot reproduce (e.g. "Jennifer's email bounced, suggest probe via DM"). Blind-overwriting those sections destroys user work. Always read-modify-write. Validate diff before commit: only frontmatter + Sections 2, 3, 4, 7 should change.

3. **Graceful scrape failure.** If a Yahoo page returns 4xx/5xx or the session is unauthenticated: do NOT guess. Mark the corresponding features as `null`, record the failed URL in a `scrape_errors:` block in frontmatter, and drop `confidence` by 0.2. The profile should still emit, just with lowered confidence. A partial profile is better than a missing one.

4. **Sequential-update discipline.** Last week's posterior becomes this week's prior -- always. Do NOT restart from taxonomy priors each week (that throws away 1-4 weeks of evidence). The one exception: if `prior_profile.confidence < 0.20`, restart (the prior profile is essentially garbage).

5. **Correlated-feature handling.** `moves_per_week` and `faab_spent_pct` are strongly correlated (active managers do both). Pass `correlated_feature_pairs` to the classifier so it down-weights. Same for `sp_roster_share` and `closer_count` (they trade off by roster-slot constraint).

6. **Do not invent cat_strength from the archetype.** `cat_strength` is a separate estimator based on actual roster composition, NOT derived from `archetype`. A `balanced` team with a thin OF has below-average SB; don't paper over that by inheriting "balanced = 50s across the board". Compute from roster.

7. **Archetype `unknown` is valid.** When classification_confidence < 40, write `archetype: unknown` with `archetype_confidence` reflecting the classifier output. Do not force a MAP on thin evidence. Downstream agents handle `unknown` by falling back to broad heuristics.

8. **Citation requirement.** Every emitted profile lists exact Yahoo URLs in `source_urls`. The weekly signal file lists all URLs across all 11 teams (dedupe the teams-page URL).

9. **One-shot vs all-opponents mode.** Single-team refreshes (on trade-offer arrival, FAAB competition observation) emit only the profile file -- no weekly summary signal. Weekly summary signal is emitted only after all 11 refreshes complete.

10. **Team slugs stable.** Slugs are lowercased + hyphenated team name, stable across the season (e.g., `jennys-team`, `springfield-isotopes`). If a manager renames their team mid-season, keep the original slug and store the new `team_name` in frontmatter -- do not rename the file (breaks downstream agent references).

## Quick Reference

**Pipeline one-liner:**

```
scrape_yahoo(4_pages) -> extract_mlb_features -> invoke(opponent-archetype-classifier,
  taxonomy=mlb_10_archetype, prior=last_week_posterior, observation_weight=f(week))
  -> compute_cat_strength(roster) -> read_existing_md -> merge_preserve_notes
  -> atomic_write -> [if all_opponents] emit_weekly_signal
```

**MLB 10-archetype taxonomy (baked in):**

| Archetype | Core signal | Prior (Wk 1) |
|-----------|-------------|--------------|
| `balanced` | no punts, pushes all cats | 0.25 |
| `stars_and_scrubs` | 4-5 elite + bench scrubs | 0.10 |
| `punt_sv` | 0 closers, loaded elsewhere | 0.10 |
| `punt_sb` | power-only offense | 0.10 |
| `punt_wins_qs` | SP thin, RP-heavy (Marmol) | 0.05 |
| `hitter_heavy` | sp_roster_share < 0.30 | 0.10 |
| `pitcher_heavy` | sp_roster_share > 0.45 | 0.10 |
| `inactive` | zero moves, stale lineup | 0.10 |
| `frustrated_active` | high moves + losing record | 0.05 |
| `unknown` | inconclusive threshold | 0.05 |

Priors sum to 1.00. Informed (not uniform) per guardrail on 12-team base rates.

**Observation weight schedule:**

| Week | Weight | Rationale |
|------|--------|-----------|
| 1-2 | 0.25 | Draft-only evidence; noisy |
| 3-4 | 0.45 | First waivers visible |
| 5-7 | 0.65 | Patterns stabilizing |
| 8-11 | 0.80 | Behavior well-characterized |
| 12+ | 0.90 | Any remaining doubt is true ambiguity |

**Key resources:**

- **[resources/template.md](resources/template.md)**: 10-archetype MLB taxonomy YAML (passed to classifier), per-opponent `.md` output template (matches `opponent-profile-schema.md`), weekly summary signal template.
- **[resources/methodology.md](resources/methodology.md)**: Yahoo scrape URL flow, feature-extraction formulas, cat_strength estimator, read-modify-write protocol, sequential-update protocol, graceful-degradation handling.
- **[resources/evaluators/rubric_mlb_opponent_profiler.json](resources/evaluators/rubric_mlb_opponent_profiler.json)**: 10 quality criteria (Taxonomy Completeness, Feature Extraction Correctness, Yahoo Scrape Coverage, Classifier Delegation Purity, Output Schema Conformance, Preserve Manual Notes, Sequential-Update Correctness, Signal File Emission, Graceful Scrape Failure, Citations).

**Inputs required:**

- `team_name` (string, single team) OR `all_opponents: true`
- `yahoo_session` (authenticated Chrome context)
- `prior_profile` (optional; if missing, bootstrap from taxonomy priors)

**Outputs produced:**

- Updated `context/opponents/<team-slug>.md` (one per refreshed team) -- manual notes preserved
- `signals/wkNN-opponent-profiles.md` (only in `all_opponents` mode) -- summary of archetype shifts + confidence changes + reactivity events

**Downstream consumers (5 agents):**

- `mlb-lineup-optimizer` -- reads §3 cat_strength + §6 best_response for `leverage_vs_opponent`
- `mlb-category-state-analyzer` -- reads §2 archetype + §3 to anticipate opponent push/punt
- `mlb-faab-sizer` -- reads §4 (waiver_aggression, faab_remaining) across all 11 for N-bidder estimate
- `mlb-trade-analyzer` -- reads §4 (trade_propensity, trade_cooperation_score) + §5 weaknesses
- `mlb-fantasy-coach` -- reads §6 for the week's opponent for morning brief
