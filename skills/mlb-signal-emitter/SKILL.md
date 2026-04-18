---
name: mlb-signal-emitter
description: Validates and persists signal files to the yahoo-mlb signals directory. Every MLB skill calls this skill before writing a signal. Enforces the signal-framework.md schema -- required YAML frontmatter fields (type, date, emitted_by, confidence, source_urls), range-checks numeric signals (0-100 unipolar, -100 to +100 bipolar), verifies variant_synthesis metadata, and enforces file naming. On validation failure, does not persist and routes a failure entry to mlb-decision-logger. Use when an agent or skill needs to emit a signal, validate a signal file, write to signals/YYYY-MM-DD-<type>.md, or check signal frontmatter. Triggers: "emit signal", "validate signal", "write signal file", "signal frontmatter".
---
# MLB Signal Emitter

## Table of Contents
- [Example](#example)
- [Workflow](#workflow)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Example

**Scenario**: `mlb-player-analyzer` has computed a `daily_quality` signal for Junior Caminero on 2026-04-17 and wants to persist it.

**Inputs passed to this skill**:
- `type: player`
- `date: 2026-04-17`
- `emitted_by: mlb-player-analyzer`
- `variant_synthesis: true`, `variants_fired: [advocate, critic]`
- Body contains: `form_score: 68`, `matchup_score: 74`, `opportunity_score: 62`, `daily_quality: 69`, `regression_index: +18`, `confidence: 0.78`
- `source_urls: [baseballsavant..., fangraphs..., mlb.com/gameday...]`

**Validation pass** (what this skill checks):

| Check | Result |
|---|---|
| YAML frontmatter parses | PASS |
| `type` is in allowed enum | PASS (`player`) |
| `date` is ISO YYYY-MM-DD | PASS |
| `emitted_by` present | PASS |
| `confidence` in [0.0, 1.0] | PASS (0.78) |
| `source_urls` is non-empty list | PASS (3 URLs) |
| `variant_synthesis: true` implies `variants_fired` has >= 1 | PASS (2 fired) |
| All numeric signals in declared range | PASS (all 0-100 signals clamped; regression_index in +-100) |
| File path matches `signals/YYYY-MM-DD-<type>.md` convention | PASS |

**Action**: Write to `~/Documents/Projects/yahoo-mlb/signals/2026-04-17-player-caminero.md` and return the absolute path.

**Failure scenario**: If `confidence: 1.4` had been passed, validation fails. The skill does NOT write the file. It calls `mlb-decision-logger` with a failure entry: `kind: signal_validation_failure`, `signal_type: player`, `reason: confidence out of range (1.4 not in [0.0, 1.0])`, `emitter: mlb-player-analyzer`, and returns an error to the calling agent.

## Workflow

Copy this checklist and track progress:

```
Signal Emission Progress:
- [ ] Step 1: Receive signal payload from upstream skill/agent
- [ ] Step 2: Validate YAML frontmatter (required fields)
- [ ] Step 3: Range-check all numeric signals
- [ ] Step 4: Validate variant synthesis metadata
- [ ] Step 5: Determine and validate file path
- [ ] Step 6: Write file OR log validation failure
```

**Step 1: Receive signal payload**

The caller hands in three things: (1) YAML frontmatter key-value pairs, (2) signal body (markdown tables), (3) intent (e.g., "this is a final synthesized signal" vs. "this is an intermediate variant dump"). See [resources/template.md](resources/template.md) for the canonical input shape.

- [ ] Frontmatter fields collected
- [ ] Body (markdown tables) supplied
- [ ] Intent known: final vs. variant-intermediate

**Step 2: Validate YAML frontmatter**

Confirm all required keys are present and well-typed. See [resources/methodology.md](resources/methodology.md#required-frontmatter-fields) for the full list.

- [ ] `type` present and in the allowed enum (lineup, waivers, streaming, trade, category-plan, playoff-push, player, matchup, regression, two-start, closer, faab, cat-state)
- [ ] `date` present and formatted `YYYY-MM-DD`
- [ ] `emitted_by` present and references a known skill or agent
- [ ] `confidence` present as a float in [0.0, 1.0]
- [ ] `source_urls` present as a non-empty list of URLs

**Step 3: Range-check numeric signals**

Every numeric signal in the body must fall inside its declared range. See [resources/methodology.md](resources/methodology.md#range-check-rules) for the per-signal range table (it mirrors signal-framework.md).

- [ ] Unipolar signals (form_score, matchup_score, opportunity_score, daily_quality, qs_probability, streamability_score, role_certainty, cat_pressure, playoff_matchup_quality, etc.) in [0, 100]
- [ ] Bipolar signals (regression_index, positional_flex_delta) in [-100, +100]
- [ ] Integer signals (playoff_games) >= 0
- [ ] Dollar signals (acquisition_value, faab_max_bid, faab_rec_bid) >= 0
- [ ] Enum signals (cat_position, verdict) inside their declared allowed sets

**Step 4: Validate variant synthesis metadata**

If this is a synthesized final signal, it must declare which variants produced it.

- [ ] If `variant_synthesis: true`, `variants_fired` is a list with >= 1 entry
- [ ] If `variant_synthesis: true`, `synthesis_confidence` is present and in [0.0, 1.0]
- [ ] If `variant_synthesis: false`, the file is an intermediate variant dump; filename must include the variant suffix (see Step 5)
- [ ] `red_team_findings` (if present) is a list of objects with `severity`, `likelihood`, `score`, `note` fields

**Step 5: Determine and validate file path**

The canonical path is `~/Documents/Projects/yahoo-mlb/signals/YYYY-MM-DD-<type>.md`. For an intermediate variant dump, use `YYYY-MM-DD-<type>-<variant>.md`. For per-player or per-game files, an optional identifier suffix is allowed: `YYYY-MM-DD-<type>-<identifier>.md`.

- [ ] Compute path from `date` and `type` in frontmatter
- [ ] Check that a signal of this type+date does not already exist unless the caller explicitly passed `overwrite: true`
- [ ] Ensure the parent directory exists (create if missing)
- [ ] Reject paths that escape the `signals/` directory

**Step 6: Write file OR log validation failure**

If all checks pass: write the file, return the absolute path. If any check fails: do NOT write, call `mlb-decision-logger` with a structured failure entry, return an error object to the caller. See [resources/methodology.md](resources/methodology.md#handling-validation-failures) for the failure log schema.

- [ ] On pass: write file, return absolute path
- [ ] On fail: build failure object (reason, field, expected, actual), send to `mlb-decision-logger`, return error

## Common Patterns

**Pattern 1: Per-player daily signal (`type: player`)**
- Filename: `YYYY-MM-DD-player-<lastname>.md` (e.g., `2026-04-17-player-caminero.md`)
- Required numeric signals in body: `daily_quality`, plus the three components (`form_score`, `matchup_score`, `opportunity_score`)
- Always a final synthesized signal when emitted by `mlb-player-analyzer` -- so `variant_synthesis: true` and `variants_fired: [advocate, critic]`
- Source URLs must include Baseball Savant, FanGraphs, and MLB.com (confirmed lineup)

**Pattern 2: Daily lineup roll-up (`type: lineup`)**
- Filename: `YYYY-MM-DD-lineup.md`
- Body references, by name, the per-player signal files it consumed (provenance chain)
- `synthesis_confidence` reflects agreement between the advocate (bat-everyone) and critic (sit-risky) variants
- Red-team findings typically flag weather, role uncertainty, or fragile platoon calls

**Pattern 3: Intermediate variant dump (variant suffix in filename)**
- Filename: `YYYY-MM-DD-<type>-advocate.md` or `YYYY-MM-DD-<type>-critic.md`
- `variant_synthesis: false` (this IS a variant, not a synthesis)
- `emitted_by` names the agent and variant (e.g., `mlb-lineup-optimizer/advocate`)
- The synthesizing agent reads these two intermediate files, produces the final synthesized signal, then emits with `variant_synthesis: true`

**Pattern 4: Low-confidence graceful degrade**
- When a web search fails, the upstream skill should still emit a signal but with `confidence <= 0.3` and a `red_team_findings` entry flagging the missing data source
- This skill does NOT reject low-confidence signals -- low confidence is legitimate. It only rejects out-of-range or missing fields.
- Flag in body: "Could not verify opposing pitcher; using prior-start proxy."

## Guardrails

1. **Never silently drop a signal.** If validation fails, the failure must be logged via `mlb-decision-logger` so the calibration review can see what was rejected and why. A signal that never gets written AND never gets logged is invisible to the team.

2. **Do not re-derive signal values.** This skill is a validator and file-writer only. It never computes `daily_quality` or any other signal itself. If an upstream skill passes in a half-computed signal, reject it rather than filling in the blanks.

3. **Reject unknown `type` values.** The enum in signal-framework.md is the authoritative list. If a caller passes `type: vibe-check`, reject and log. Adding a new signal type requires updating signal-framework.md first, then this skill's validator.

4. **Range checks are hard limits.** A `form_score` of 105 is not "close enough" -- it indicates a bug upstream (probably forgot to normalize). Reject and log. Do NOT clamp-and-accept.

5. **`confidence` is required, not optional.** Even a perfectly-computed signal with three source URLs must carry a confidence float. A missing confidence is a validator failure, not a warning.

6. **`source_urls` must be a non-empty list.** Per CLAUDE.md rule 1 ("Web-search everything"), every factual signal is backed by a live source. An empty `source_urls` list means the signal was not grounded -- reject and log.

7. **Variant synthesis claims must be provable.** If `variant_synthesis: true` but `variants_fired` is empty or missing, that is a lie about the team's process. Reject and log.

8. **Do not overwrite without explicit consent.** If a signal already exists at the target path, refuse to overwrite unless the caller passes `overwrite: true`. This prevents losing an earlier morning's signal when a mid-day re-run happens.

## Quick Reference

**Required frontmatter fields (always):**
- `type` (enum)
- `date` (YYYY-MM-DD)
- `emitted_by` (string)
- `confidence` (float 0.0-1.0)
- `source_urls` (non-empty list)

**Required when `variant_synthesis: true`:**
- `variants_fired` (list, >= 1)
- `synthesis_confidence` (float 0.0-1.0)

**File path conventions:**
- Final synthesized: `signals/YYYY-MM-DD-<type>.md`
- With identifier: `signals/YYYY-MM-DD-<type>-<id>.md`
- Intermediate variant: `signals/YYYY-MM-DD-<type>-<variant>.md`

**Signal ranges (see [resources/methodology.md](resources/methodology.md#range-check-rules) for the full table):**
- Unipolar (0-100): form_score, matchup_score, opportunity_score, daily_quality, qs_probability, k_ceiling, era_whip_risk, streamability_score, role_certainty, save_role_certainty, cat_pressure, cat_reachability, cat_punt_score, positional_need_fit, opp_sp_quality, park_hitter_factor, park_pitcher_factor, weather_risk, bullpen_state, playoff_matchup_quality, holding_value, obp_contribution, sb_opportunity
- Bipolar (-100 to +100): regression_index, positional_flex_delta
- Dollar (>= 0): acquisition_value, faab_max_bid, faab_rec_bid, trade_value_delta
- Integer (>= 0): playoff_games
- Enum: cat_position (winning|tied|losing), verdict (accept|counter|reject)

**On validation failure:**
1. Do NOT write the signal file.
2. Build failure entry: `{kind: signal_validation_failure, signal_type, reason, field, expected, actual, emitter, timestamp}`.
3. Call `mlb-decision-logger` with the failure entry.
4. Return an error object to the caller.

**Key resources:**
- **[resources/template.md](resources/template.md)**: Canonical signal file template with every required frontmatter field and a fully-populated example body
- **[resources/methodology.md](resources/methodology.md)**: Validation rules -- required fields, range checks, variant-synthesis checks, path conventions, failure handling
- **[resources/evaluators/rubric_mlb_signal_emitter.json](resources/evaluators/rubric_mlb_signal_emitter.json)**: 8 criteria for evaluating the emitter's behavior

**Inputs required:**
- Frontmatter key-value pairs from caller
- Signal body (markdown tables)
- `overwrite` flag (default false)

**Outputs produced:**
- On success: absolute file path of the written signal
- On failure: error object; a failure entry appended to `tracker/decisions-log.md` via `mlb-decision-logger`
