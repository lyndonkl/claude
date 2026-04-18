# MLB FAAB Sizer Templates

Input block, output template (with delegation trace), per-target brief format, signal-file layout, and a worked example showing the full delegation pipeline.

## Table of Contents
- [Input Block](#input-block)
- [Output Template](#output-template)
- [Per-Target User Brief](#per-target-user-brief)
- [Signal File Layout](#signal-file-layout)
- [faab-log Append Entry](#faab-log-append-entry)
- [Worked Delegation Flow](#worked-delegation-flow)

---

## Input Block

Collect all inputs before computing. Any missing required field fails fast with a prompt back to the caller.

```yaml
target:
  player_name: ________
  mlb_team: ________
  eligible_positions: [____]              # e.g., [SP, P]
  situation_label: ________               # new-callup | closer-change | platoon-promotion | injury-replacement | steady-state | speculation

signals_from_player_analyzer:
  acquisition_value_usd: ___              # $ on 1-100 scale
  role_certainty: ___                     # 0-100
  regression_index: ___                   # -100 to +100 (optional)

signals_from_waiver_analyst:
  positional_need_fit: ___                # 0-100

budget_state:
  faab_remaining_usd: ___                 # $
  faab_original_usd: 100                  # Yahoo default
  week_number: ___                        # 1-26
  today: YYYY-MM-DD
  team_contending: true | false

comparable_bids_from_faab_log:
  entries_read: ___
  avg_winning_bid_vs_industry_ratio: ___  # e.g., 1.15 = league overbids 15%
```

---

## Output Template

The skill emits a structured output block (with the full delegation trace) plus a plain-English rationale.

```yaml
output:
  player_name: ________
  faab_rec_bid_usd: $___
  faab_max_bid_usd: $___

  # Step 1 -- baseball-specific base_value (computed by this skill)
  base_value_trace:
    acquisition_value_usd: $___
    positional_need_fit_fraction: 0.___
    role_certainty_fraction: 0.___
    urgency_multiplier: ___               # 0.7 - 1.4
    season_pace_multiplier_base: ___      # calendar bucket
    league_inflation_ratio: ___           # from faab-log
    season_pace_multiplier_calibrated: ___
    base_value_usd: $___

  # Step 2 -- value-type classification (computed by this skill)
  value_type: common_value | private_value | mixed
  value_type_rationale: "______"          # one sentence

  # Step 3 -- DELEGATED to auction-winners-curse-haircut
  winners_curse_delegation:
    skill: auction-winners-curse-haircut
    inputs:
      raw_valuation: $___
      value_type: ____
      n_informed_bidders: ___
      signal_dispersion: ___              # 0-100
      mix_common_weight: ___              # only if value_type == mixed
    outputs:
      adjusted_valuation_usd: $___
      haircut_pct: ___                    # 0-35
      classification_rationale: "______"
      applied: true | false

  # Step 4 -- N estimate (computed by this skill)
  n_bidders_estimate: ___                 # 1-8
  n_estimate_source: opponent_profile_scan | default_table

  # Step 5 -- DELEGATED to auction-first-price-shading
  first_price_shading_delegation:
    skill: auction-first-price-shading
    inputs:
      true_value: $___                    # = adjusted_valuation from step 3
      n_bidders_estimate: ___
      value_distribution: uniform | log-normal | empirical
      risk_aversion: ___                  # 0-1
      budget_remaining_usd: $___
    outputs:
      shaded_bid_usd: $___
      shade_fraction: 0.___
      rationale: "______"
      assumptions_flagged: [______]

  # Step 6 -- baseball-specific guardrails (this skill)
  guardrails_triggered:
    - name: ________                      # e.g., april_40pct_cap_triggered
      effect: ________
      original_value: $___
      capped_value: $___

  # Step 7 -- calibration metadata
  calibration:
    faab_log_entries_read: ___
    league_inflation_ratio: ___
    calibration_confidence: low | medium | high

  confidence: 0.___                       # 0.0 - 1.0
  source_urls:
    - ________
```

The four blocks `base_value_trace`, `winners_curse_delegation`, `n_bidders_estimate`, and `first_price_shading_delegation` together form the full reproducible trace. Any reviewer can re-run the pipeline from these fields.

---

## Per-Target User Brief

Beginner-safe, jargon translated inline, ends in a verb. MUST name both sibling skills by purpose (not jargon) so the user can trust the chain.

```markdown
### BID $___ on {Player Name} (ceiling $___)

**Why**: {1-2 sentences in plain English}.
Example: "Roki Sasaki just got called up to the Dodgers rotation. He's a high-strikeout pitcher and we need starting pitching."

**How I sized the bid** (each line comes from a specific step):
- Baseball value (pos fit, role certainty, urgency, April-pace, our league's inflation): **$___**
- Classified as {common-value / private-value / mixed}: {one-sentence reason}
- Winner's-curse correction (because {N} other informed teams are likely bidding and winning is itself evidence we over-estimated): haircut **{haircut_pct}%** -> **$___**
- First-price shading (in a sealed-bid auction against {N} competitors, the equilibrium bid is a fraction of true value): shade **{shade_fraction}** -> **$___**
- Baseball guardrails applied: {list, or "none"}

**Don't exceed $___.** If the bid market goes higher, let him go -- we still need budget for {next target or trade-deadline opportunities}.

**Guardrails flagged**:
- {list, or "none"}

**If we lose this bid**: {fallback player, or "wait for next waiver cycle"}

**Sources checked**:
- {source URL 1}
- {source URL 2}
```

---

## Signal File Layout

Written to `signals/YYYY-MM-DD-faab.md` via `mlb-signal-emitter`.

```markdown
---
type: faab
date: YYYY-MM-DD
emitted_by: mlb-faab-sizer
delegation_chain:
  - auction-winners-curse-haircut
  - auction-first-price-shading
variant_synthesis: true
variants_fired: [advocate, critic]
synthesis_confidence: 0.___
source_urls:
  - ________
---

# FAAB Bid Recommendations -- {date}

## Target 1: {Player Name}

| Field | Value |
|---|---|
| `acquisition_value` | $___ |
| `positional_need_fit` | ___/100 |
| `role_certainty` | ___/100 |
| `base_value` | $___ |
| `value_type` | common \| private \| mixed |
| `adjusted_valuation` (post haircut) | $___ |
| `haircut_pct` | ___% |
| `n_bidders_estimate` | ___ |
| `shade_fraction` | 0.___ |
| `shaded_bid` | $___ |
| `faab_rec_bid` | $___ |
| `faab_max_bid` | $___ |
| Guardrails triggered | ___ |

Rationale: {1-2 sentences, beginner-safe, names both sibling skills}

## Target 2: {Player Name}
...
```

---

## faab-log Append Entry

After a bid is placed, append to `tracker/faab-log.md`:

```markdown
### YYYY-MM-DD | {Player Name} | {WON | LOST | NOT_BID}
- **our_bid:** $___
- **winning_bid:** $___
- **winner:** {team name or "us"}
- **recommended_bid:** $___
- **industry_consensus_at_time:** $___
- **outcome_3wk:** {filled later}
```

`industry_consensus_at_time` is populated by web-searching FAAB consensus trackers (FantasyPros, RotoBaller). If unavailable, leave blank and flag `no_industry_benchmark`.

---

## Worked Delegation Flow

End-to-end trace for Roki Sasaki (the canonical example). Shows what gets passed to each sibling skill and what comes back.

**Inputs**:
```yaml
target:
  player_name: Roki Sasaki
  situation_label: new-callup
signals:
  acquisition_value_usd: 28
  positional_need_fit: 70
  role_certainty: 65
budget_state:
  faab_remaining_usd: 100
  week_number: 4
faab_log: 0 valid rows (skip calibration)
```

**Step 1 - base_value (this skill)**:
```
urgency = 1.2, pace_base = 0.7 (late April interp), inflation = N/A
base_value = 28 x 0.70 x 0.65 x 1.2 x 0.7 = 10.70
```

**Step 2 - classify (this skill)**: `common_value`
> "Headline prospect -- FanGraphs/MLB Pipeline projection, every save-hunting team has the same info."

**Step 3 - call auction-winners-curse-haircut**:
```
inputs = {
  raw_valuation: 10.70,
  value_type: "common_value",
  n_informed_bidders: 6,
  signal_dispersion: 60,        # prospect with limited MLB track record
}
```
Sibling returns:
```
{
  adjusted_valuation: 7.39,
  haircut_pct: 30.96,
  classification_rationale: "Common-value target with 6 informed bidders and high signal dispersion. Kagel-Levin range applies.",
  applied: true,
}
```

**Step 4 - N estimate (this skill)**: opponent-profile scan -> N = 6.

**Step 5 - call auction-first-price-shading**:
```
inputs = {
  true_value: 7.39,
  n_bidders_estimate: 6,
  value_distribution: "log-normal",
  risk_aversion: 0.2,
  budget_remaining: 100,
}
```
Sibling returns:
```
{
  shaded_bid: 7,
  shade_fraction: 0.898,
  rationale: "Log-normal cluster adjustment raises shade from (N-1)/N = 0.833 to 0.889; risk-aversion nudges to 0.898. Budget and 0.9x-value caps non-binding.",
  assumptions_flagged: ["log-normal spread = 1.5 default", "N=6 is an estimate"],
}
```

**Step 6 - baseball guardrails (this skill)**:
- April 40% cap: $7 < $40 -- OK
- Speculation cap: new-callup, role_cert 65 -- no trigger
- Role certainty floor: 65 >= 20 -- OK
- None triggered.

**Step 7 - emit**:
```yaml
output:
  player_name: Roki Sasaki
  faab_rec_bid_usd: 7
  faab_max_bid_usd: 7          # round(7.39 x 0.90)
  base_value_trace:
    base_value_usd: 10.70
    urgency_multiplier: 1.2
    season_pace_multiplier_calibrated: 0.7
  value_type: common_value
  winners_curse_delegation:
    inputs: {raw_valuation: 10.70, value_type: common_value, n: 6, dispersion: 60}
    outputs: {adjusted_valuation: 7.39, haircut_pct: 30.96, applied: true}
  n_bidders_estimate: 6
  first_price_shading_delegation:
    inputs: {true_value: 7.39, n: 6, dist: log-normal, risk: 0.2}
    outputs: {shaded_bid: 7, shade_fraction: 0.898}
  guardrails_triggered: []
  confidence: 0.78
```

**User-facing brief**:
```
### BID $7 on Roki Sasaki (ceiling $7)

**Why**: Sasaki just got called up to the Dodgers rotation. He's a high-strikeout pitcher and we need starting pitching.

**How I sized the bid**:
- Baseball value (pos fit 70, role certainty 65, urgency 1.2 for new callup, April pace 0.7): $10.70
- Classified as common-value: every team sees the same FanGraphs projection on a headline prospect.
- Winner's-curse correction (because 6 other informed teams are bidding and winning is itself a signal we over-valued): 31% haircut -> $7.39
- First-price shading (sealed-bid auction against 6 competitors, log-normal values, mild risk aversion): shade 0.90 -> $7
- Baseball guardrails: none triggered.

**Don't exceed $7.** If the market goes higher, let him go -- we want to keep budget for the July trade-deadline window.

**Sources**: FanGraphs/ATC, RotoBaller Call-Ups.
```
