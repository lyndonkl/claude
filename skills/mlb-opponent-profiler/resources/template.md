# MLB Opponent Profiler -- Templates

Three templates in this file:

1. [MLB 10-Archetype Taxonomy](#mlb-10-archetype-taxonomy) -- YAML passed to `opponent-archetype-classifier`
2. [Per-Opponent Profile Template](#per-opponent-profile-template) -- output written to `context/opponents/<slug>.md`, matches `opponent-profile-schema.md`
3. [Weekly Summary Signal Template](#weekly-summary-signal-template) -- emitted to `signals/wkNN-opponent-profiles.md`

---

## MLB 10-Archetype Taxonomy

This is the `archetype_taxonomy` argument passed to `opponent-archetype-classifier`. Priors reflect 12-team H2H-Categories base rates observed across multiple Yahoo seasons (SME-derived; refresh empirically after Season 1).

Feature distributions use Gaussian `{mean, std}` for continuous features and categorical `{value: probability}` for discrete ones. **All feature names MUST match the feature-extraction keys in [methodology.md](methodology.md#feature-extraction) exactly.**

```yaml
archetype_taxonomy:

  balanced:
    prior: 0.25
    feature_distributions:
      sp_roster_share:        {mean: 0.38, std: 0.05}   # healthy mix
      closer_count:           {mean: 2.0,  std: 0.6}
      sb_speed_count:         {mean: 3.0,  std: 1.0}
      power_bat_count:        {mean: 4.0,  std: 1.2}
      moves_per_week:         {mean: 2.5,  std: 1.0}
      faab_spent_pct:         {mean: 0.20, std: 0.10}
      faab_avg_bid:           {mean: 3.5,  std: 2.0}
      lineup_set_daily:       {true: 0.85, false: 0.15}
      trade_offers_sent:      {mean: 0.8,  std: 0.7}
      days_since_last_login:  {mean: 1.0,  std: 1.2}
    best_response:
      - "Match cat-for-cat; matchup decided on weekly execution"
      - "Include in N-estimate for common-value FAAB targets"
      - "Use variance-seeking only when we are the underdog (matchup_win_prob < 0.40)"
      - "Probe with fair consolidation trades; likely to counter rather than ignore"

  stars_and_scrubs:
    prior: 0.10
    feature_distributions:
      sp_roster_share:        {mean: 0.38, std: 0.06}
      closer_count:           {mean: 1.8,  std: 0.8}
      sb_speed_count:         {mean: 2.0,  std: 1.2}
      power_bat_count:        {mean: 3.5,  std: 1.4}
      moves_per_week:         {mean: 3.5,  std: 1.3}   # churn the scrub slots
      faab_spent_pct:         {mean: 0.35, std: 0.15}
      faab_avg_bid:           {mean: 2.0,  std: 1.5}   # lotto tickets
      lineup_set_daily:       {true: 0.70, false: 0.30}
      trade_offers_sent:      {mean: 1.5,  std: 1.0}
      days_since_last_login:  {mean: 1.0,  std: 1.0}
    best_response:
      - "High weekly variance -- if we are favorite, damp their variance by neutral lineup"
      - "If we are underdog, lean into our own variance to catch their cold weeks"
      - "Trade target: offer roster-consolidation (three depth pieces for one of their studs)"

  punt_sv:
    prior: 0.10
    feature_distributions:
      sp_roster_share:        {mean: 0.50, std: 0.06}  # SP-heavy
      closer_count:           {mean: 0.3,  std: 0.4}   # 0-1 closers
      sb_speed_count:         {mean: 3.0,  std: 1.2}
      power_bat_count:        {mean: 4.0,  std: 1.2}
      moves_per_week:         {mean: 2.0,  std: 1.0}
      faab_spent_pct:         {mean: 0.15, std: 0.10}
      faab_avg_bid:           {mean: 3.0,  std: 2.0}
      lineup_set_daily:       {true: 0.80, false: 0.20}
      trade_offers_sent:      {mean: 0.7,  std: 0.7}
      days_since_last_login:  {mean: 1.0,  std: 1.2}
    best_response:
      - "Concede SV; push all 5 hitting cats + K + QS + ERA + WHIP"
      - "Do not chase closers as streamers in this matchup"
      - "They will dominate ratios via elite SP -- high-variance IP-heavy SP is our counter"

  punt_sb:
    prior: 0.10
    feature_distributions:
      sp_roster_share:        {mean: 0.38, std: 0.06}
      closer_count:           {mean: 2.0,  std: 0.8}
      sb_speed_count:         {mean: 0.8,  std: 0.7}   # very few speed bats
      power_bat_count:        {mean: 6.0,  std: 1.5}   # power-heavy
      moves_per_week:         {mean: 2.0,  std: 1.0}
      faab_spent_pct:         {mean: 0.15, std: 0.10}
      faab_avg_bid:           {mean: 3.0,  std: 2.0}
      lineup_set_daily:       {true: 0.85, false: 0.15}
      trade_offers_sent:      {mean: 0.7,  std: 0.7}
      days_since_last_login:  {mean: 1.0,  std: 1.2}
    best_response:
      - "Concede HR and RBI (or play close); push SB and ratios"
      - "Sell-high power bats we were on the fence about -- they are a buyer"
      - "Speed-only waiver adds have high leverage against them this week"

  punt_wins_qs:
    prior: 0.05
    feature_distributions:
      sp_roster_share:        {mean: 0.20, std: 0.05}  # very thin SP
      closer_count:           {mean: 3.2,  std: 0.8}   # RP-heavy (Marmol)
      sb_speed_count:         {mean: 3.0,  std: 1.2}
      power_bat_count:        {mean: 5.0,  std: 1.3}
      moves_per_week:         {mean: 4.0,  std: 1.2}   # active
      faab_spent_pct:         {mean: 0.40, std: 0.18}
      faab_avg_bid:           {mean: 3.5,  std: 2.5}
      lineup_set_daily:       {true: 0.85, false: 0.15}
      trade_offers_sent:      {mean: 1.2,  std: 1.0}
      days_since_last_login:  {mean: 0.8,  std: 1.0}
    best_response:
      - "Concede K and QS (two free cat losses)"
      - "Lock 6 of remaining 8 cats -- ratios will be elite on their side"
      - "Do not stream SPs against them; streaming cost with no reward"

  hitter_heavy:
    prior: 0.10
    feature_distributions:
      sp_roster_share:        {mean: 0.28, std: 0.05}  # light on SP
      closer_count:           {mean: 1.8,  std: 0.8}
      sb_speed_count:         {mean: 3.2,  std: 1.2}
      power_bat_count:        {mean: 5.0,  std: 1.3}
      moves_per_week:         {mean: 2.8,  std: 1.2}
      faab_spent_pct:         {mean: 0.22, std: 0.12}
      faab_avg_bid:           {mean: 3.0,  std: 2.0}
      lineup_set_daily:       {true: 0.85, false: 0.15}
      trade_offers_sent:      {mean: 1.0,  std: 0.9}
      days_since_last_login:  {mean: 1.0,  std: 1.2}
    best_response:
      - "Tilt to ~15-20 point pitching advantage; they bleed K and QS"
      - "Do not overbid on closers against them; they will not chase"
      - "Fair trade target for pitching-for-hitting consolidations"

  pitcher_heavy:
    prior: 0.10
    feature_distributions:
      sp_roster_share:        {mean: 0.48, std: 0.05}  # heavy SP
      closer_count:           {mean: 2.5,  std: 0.8}
      sb_speed_count:         {mean: 2.0,  std: 1.2}
      power_bat_count:        {mean: 3.2,  std: 1.3}
      moves_per_week:         {mean: 2.8,  std: 1.2}
      faab_spent_pct:         {mean: 0.22, std: 0.12}
      faab_avg_bid:           {mean: 3.0,  std: 2.0}
      lineup_set_daily:       {true: 0.85, false: 0.15}
      trade_offers_sent:      {mean: 1.0,  std: 0.9}
      days_since_last_login:  {mean: 1.0,  std: 1.2}
    best_response:
      - "Tilt to ~15-20 point hitting advantage; they lack depth"
      - "Do not chase SPs on waivers against them; they are buyers"
      - "Fair trade target for hitting-for-pitching consolidations"

  inactive:
    prior: 0.10
    feature_distributions:
      sp_roster_share:        {mean: 0.38, std: 0.10}  # whatever they drafted
      closer_count:           {mean: 1.8,  std: 0.9}
      sb_speed_count:         {mean: 3.0,  std: 1.2}
      power_bat_count:        {mean: 4.0,  std: 1.4}
      moves_per_week:         {mean: 0.1,  std: 0.2}   # near-zero
      faab_spent_pct:         {mean: 0.02, std: 0.04}
      faab_avg_bid:           {mean: 0.5,  std: 0.8}
      lineup_set_daily:       {true: 0.20, false: 0.80}  # stale lineups
      trade_offers_sent:      {mean: 0.1,  std: 0.3}
      days_since_last_login:  {mean: 4.0,  std: 2.5}   # rarely logs in
    best_response:
      - "Exclude from N-bidder FAAB estimates; N drops by 1"
      - "Send fair consolidation trades repeatedly; dormant managers sometimes accept to clear notifications"
      - "Expect roster atrophy -- our matchup_win_probability rises week-over-week"
      - "Do NOT attempt to fleece -- commissioner trade review is the guardrail"

  frustrated_active:
    prior: 0.05
    feature_distributions:
      sp_roster_share:        {mean: 0.38, std: 0.08}
      closer_count:           {mean: 1.8,  std: 0.9}
      sb_speed_count:         {mean: 3.0,  std: 1.2}
      power_bat_count:        {mean: 4.0,  std: 1.3}
      moves_per_week:         {mean: 4.5,  std: 1.5}   # very high
      faab_spent_pct:         {mean: 0.45, std: 0.20}
      faab_avg_bid:           {mean: 4.0,  std: 2.5}
      lineup_set_daily:       {true: 0.90, false: 0.10}  # trying hard
      trade_offers_sent:      {mean: 2.5,  std: 1.5}   # motivated trader
      days_since_last_login:  {mean: 0.3,  std: 0.6}
      # Note: recent_record W% is a soft gate -- classifier sees low-record-with-high-activity signature
    best_response:
      - "Prime trade partner -- they are motivated to shake things up"
      - "Target their cooling stars (buy-low for us, sell-high for them psychologically)"
      - "Expect aggressive FAAB bids; shade our bids up on shared targets"

  unknown:
    prior: 0.05
    # Used as the MAP when classification_confidence < 40 (inconclusive threshold)
    # Feature distributions are uniform-ish -- this archetype is a placeholder, not a real type
    feature_distributions:
      sp_roster_share:        {mean: 0.38, std: 0.15}
      closer_count:           {mean: 2.0,  std: 1.5}
      sb_speed_count:         {mean: 2.5,  std: 1.5}
      power_bat_count:        {mean: 4.0,  std: 1.5}
      moves_per_week:         {mean: 2.5,  std: 2.0}
      faab_spent_pct:         {mean: 0.20, std: 0.20}
      faab_avg_bid:           {mean: 3.0,  std: 3.0}
      lineup_set_daily:       {true: 0.50, false: 0.50}
      trade_offers_sent:      {mean: 1.0,  std: 1.5}
      days_since_last_login:  {mean: 2.0,  std: 2.5}
    best_response:
      - "Treat as balanced-default; gather 2-3 more weeks of observation"
      - "Include in N-estimate conservatively (assume 50% bidder on common targets)"
      - "Do not probe trades yet -- send signal first via public chat or waiver activity"
```

**Correlated feature pairs to pass to the classifier** (down-weights double-counting):

```yaml
correlated_feature_pairs:
  - [moves_per_week, faab_spent_pct]           # active managers do both
  - [sp_roster_share, closer_count]            # roster-slot tradeoff
  - [moves_per_week, days_since_last_login]    # active = recent login
  - [power_bat_count, sb_speed_count]          # bat-slot tradeoff (weak)
```

---

## Per-Opponent Profile Template

Output file at `context/opponents/<team-slug>.md`. Structure matches `opponent-profile-schema.md` exactly.

**Machine-maintained sections (this skill rewrites on refresh):** frontmatter, §2 Archetype, §3 Category strength, §4 Behavioral, §7 Matchup history.

**Manual-authored sections (NEVER overwrite):** §1 Summary, §5 Apparent weaknesses / surpluses, §6 Best response, §8 Reactivity triggers, §9 Open questions.

```markdown
---
team_name: {canonical Yahoo team name}
team_id: {1-12}
manager_alias: {first name / handle}
last_updated: {YYYY-MM-DD}
confidence: {0.00-1.00}
source_urls:
  - https://baseball.fantasysports.yahoo.com/b1/23756/teams
  - https://baseball.fantasysports.yahoo.com/b1/23756/{team_id}
  - https://baseball.fantasysports.yahoo.com/b1/23756/{team_id}/draftresults
  - https://baseball.fantasysports.yahoo.com/b1/23756/transactions?tid={team_id}
# Populated by classifier; downstream agents can read the full posterior.
posterior:
  balanced:          {p}
  stars_and_scrubs:  {p}
  punt_sv:           {p}
  punt_sb:           {p}
  punt_wins_qs:      {p}
  hitter_heavy:      {p}
  pitcher_heavy:     {p}
  inactive:          {p}
  frustrated_active: {p}
  unknown:           {p}
# Populated only if any scrape step failed -- downstream should treat profile as degraded.
scrape_errors: []
---

# {team_name} -- profile (week {NN})

## 1. Summary
{manual-authored paragraph -- PRESERVED ACROSS REFRESHES}

## 2. Archetype
```yaml
archetype: {balanced | stars_and_scrubs | punt_sv | punt_sb | punt_wins_qs |
            hitter_heavy | pitcher_heavy | inactive | frustrated_active | unknown}
archetype_confidence: {0.00-1.00}
archetype_evidence:
  - "{observed signal 1}"
  - "{observed signal 2}"
  - "{observed signal 3}"
```

## 3. Category strength
```yaml
cat_strength:
  R:    {0-100}
  HR:   {0-100}
  RBI:  {0-100}
  SB:   {0-100}
  OBP:  {0-100}
  K:    {0-100}
  ERA:  {0-100}
  WHIP: {0-100}
  QS:   {0-100}
  SV:   {0-100}
presumed_punts: [{cats with score < 35}]
likely_pushes:  [{cats with score > 65}]
```

## 4. Behavioral signals
```yaml
activity_level:           {high | moderate | low | dormant}
last_active:              {YYYY-MM-DD HH:MM TZ}
waiver_aggression:        {passive | moderate | aggressive}
faab_remaining:           ${amount}
faab_avg_bid_pct:         {0.00-1.00 | null}
trade_propensity:         {quiet | occasional | active | untested}
trade_cooperation_score:  {0-100 | null}
```

## 5. Apparent weaknesses / surpluses
{manual-authored bulleted lists -- PRESERVED ACROSS REFRESHES}

## 6. Best response
{manual-authored strategic plays -- PRESERVED ACROSS REFRESHES}

## 7. Matchup history
```yaml
h2h_record_vs_us:             {W-L-T}
avg_cat_margin_when_facing_us: {optional}
notes: []
```

## 8. Reactivity triggers
{manual-authored event list -- PRESERVED ACROSS REFRESHES}

## 9. Open questions
{manual-authored TODO list -- PRESERVED ACROSS REFRESHES}
```

---

## Weekly Summary Signal Template

Emitted at `signals/wkNN-opponent-profiles.md` only after `all_opponents: true` refresh completes.

```markdown
---
type: opponent_profile_summary
date: {YYYY-MM-DD}
week: {NN}
emitted_by: mlb-opponent-profiler
confidence: {0.00-1.00}   # average classification_confidence across 11 teams
source_urls:
  - {dedupe union across all 11 teams; teams index + 11 team pages + 11 transactions pages}
---

# Week {NN} Opponent Profile Summary

## Archetype shifts since Week {NN-1}

Teams whose top-posterior archetype changed, or whose MAP-archetype posterior shifted by > 0.05.

| Team | Prior MAP (post) | New MAP (post) | Conf prior -> new | Note |
|------|------------------|----------------|-------------------|------|
| {team}| {arch (p)} | {arch (p)} | {c1 -> c2} | {one-line why} |

## Confidence changes

Teams where `archetype_confidence` changed by > 0.10 this week (separate from posterior shifts).

- {team}: {c1} -> {c2} -- {rationale}

## Reactivity triggers fired

Observable events this week that updated opponent profiles mid-week (FAAB bids observed, trade offers received, record drops).

- [{team}] {event description} (per `context/opponents/{slug}.md` §8)

## Scrape health

Teams with `scrape_errors` set this week (degraded confidence):

- {team}: {which URLs failed}

## Action items for downstream agents

Concrete reads for the week ahead:

- **mlb-faab-sizer**: N-bidder estimates for upcoming waivers should exclude {inactive teams}
- **mlb-trade-analyzer**: open trade probes this week = {frustrated_active + balanced teams with untested trade_propensity}
- **mlb-fantasy-coach**: this week's matchup opponent is {team} -- §6 best_response for morning brief
- **mlb-lineup-optimizer**: opponent cat_strength for leverage calc = {matchup opponent cat_strength}
- **mlb-category-state-analyzer**: opponent presumed_punts = {list}
```
