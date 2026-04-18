# MLB FAAB Sizer Templates

Input block, output template, per-target brief format, and signal-file layout for FAAB bid sizing.

## Table of Contents
- [Input Block](#input-block)
- [Output Template](#output-template)
- [Per-Target User Brief](#per-target-user-brief)
- [Signal File Layout](#signal-file-layout)
- [faab-log Append Entry](#faab-log-append-entry)

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
  faab_original_usd: 100                  # Yahoo default is $100 unless league overrides
  week_number: ___                        # 1-26
  today: YYYY-MM-DD
  team_contending: true | false           # relevant for Sept final-push pace

comparable_bids_from_faab_log:
  # (auto-populated from tracker/faab-log.md)
  entries_read: ___
  avg_winning_bid_vs_industry_ratio: ___  # e.g., 1.15 = league overbids 15%
```

---

## Output Template

The skill emits a structured output block plus a plain-English rationale.

```yaml
output:
  player_name: ________
  faab_rec_bid_usd: $___
  faab_max_bid_usd: $___

  formula_trace:
    acquisition_value_fraction: 0.___     # acquisition_value / 100
    positional_need_fit_fraction: 0.___   # positional_need_fit / 100
    role_certainty_fraction: 0.___        # role_certainty / 100
    urgency_multiplier: ___               # 0.7 - 1.4
    season_pace_multiplier_base: ___      # calendar bucket
    season_pace_multiplier_calibrated: ___ # after league-inflation adjustment
    max_bid_fraction: 0.___
    faab_remaining_usd: $___
    faab_max_bid_raw_usd: $___
    faab_max_bid_rounded_usd: $___
    faab_rec_bid_raw_usd: $___
    faab_rec_bid_rounded_usd: $___

  guardrails_triggered:
    - name: ________           # e.g., april_40pct_cap_triggered
      effect: ________
      original_value: $___
      capped_value: $___

  calibration:
    faab_log_entries_read: ___
    league_inflation_ratio: ___          # 1.0 = at industry, >1 = overbids, <1 = underbids
    calibration_confidence: low | medium | high

  confidence: 0.___                       # 0.0 - 1.0
  source_urls:
    - ________
    - ________
```

---

## Per-Target User Brief

This is what the `mlb-fantasy-coach` agent surfaces to the user. Beginner-safe, jargon translated inline, ends in a verb.

```markdown
### BID $___ on {Player Name} (ceiling $___)

**Why**: {1-2 sentences in plain English}.
Example: "Roki Sasaki got called up to the Dodgers rotation this week. He is a high-strikeout pitcher which helps our team, and we need starting pitching depth."

**How I sized the bid**:
- Rest-of-season value of the player: **$___** (think of this as "how much of a $100 budget would I spend to acquire him in a brand-new auction draft")
- How much we need his position: **___/100** (higher = bigger roster hole)
- How sure we are he'll actually play: **___/100**
- Calendar adjustment: it's {April/May-June/July-Aug/September} so {we're saving budget / we're spending}

**Don't exceed $___.** If the bid market goes higher, let him go -- we still need budget for {next target or trade-deadline opportunities}.

**Guardrails flagged**:
- {list, or "none"}

**If we lose this bid**: {fallback player to target next, or "no immediate fallback -- wait for next waiver cycle"}

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
variant_synthesis: true
variants_fired: [advocate, critic]
synthesis_confidence: 0.___
red_team_findings:
  - severity: ___
    likelihood: ___
    score: ___
    note: ________
    mitigation: ________
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
| `faab_rec_bid` | $___ |
| `faab_max_bid` | $___ |
| Urgency multiplier | ___ |
| Season pace multiplier (calibrated) | ___ |
| Guardrails triggered | ___ |

Rationale: {1-2 sentences, beginner-safe}

## Target 2: {Player Name}
...
```

---

## faab-log Append Entry

After a bid is placed (or the waiver period closes), append to `tracker/faab-log.md`:

```markdown
### YYYY-MM-DD | {Player Name} | {WON | LOST | NOT_BID}
- **our_bid:** $___
- **winning_bid:** $___
- **winner:** {team name or "us"}
- **recommended_bid:** $___ (what mlb-faab-sizer suggested)
- **industry_consensus_at_time:** $___
- **outcome_3wk:** {filled in 3 weeks after bid -- "produced as expected" | "bust" | "too early to tell"}
```

The `industry_consensus_at_time` field is populated by `mlb-faab-sizer` at bid time by web-searching "FAAB bids {player name} {week}" against FantasyPros, RotoBaller, or similar consensus-tracker sources. If unavailable, leave blank and flag `no_industry_benchmark` in the signal.
