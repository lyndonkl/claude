---
name: mlb-decision-logger
description: Appends structured decision entries to the yahoo-mlb decision log (tracker/decisions-log.md) on behalf of any agent in the MLB team. Validates entries against the authoritative schema, serializes concurrent writes from parallel agents, and runs the Monday calibration pass to fill in outcomes and update the variant scoreboard. Use when any MLB agent needs to record a decision, when the coach requests "log decision", "append to decision log", "record variant outcome", or runs the "calibration pass".
---
# MLB Decision Logger

## Table of Contents
- [Example](#example)
- [Workflow](#workflow)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Example

**Scenario**: Three agents fire in a single morning brief on 2026-04-17. Each agent hands a decision payload to this skill. On Monday 2026-04-21, the coach runs the calibration pass over Friday's lineup decision.

**Sequence**:

1. `mlb-lineup-optimizer` submits a start/sit decision for Junior Caminero.
2. `mlb-waiver-analyst` submits a FAAB bid on a two-start streamer.
3. `mlb-streaming-strategist` submits a stream pickup.

**Skill behavior**:

- Reads the current tail of `tracker/decisions-log.md`.
- Auto-assigns `decision_id` by counting same-day, same-type entries and incrementing (`2026-04-17-lineup-01`, `2026-04-17-waiver-01`, `2026-04-17-stream-01`).
- Validates each payload against the schema in `context/frameworks/decision-log-format.md`.
- Appends entries in timestamp order, one at a time, re-reading the tail between writes.
- Returns the assigned `decision_id` to the calling agent.

**Monday calibration** (2026-04-21):

- Reads all entries where `will_verify_on <= 2026-04-21` and `outcome_recorded_on` is empty.
- For each entry, agent web-searches the outcome and passes result to this skill.
- Skill edits the target entry in place (only the three outcome fields) and increments the matching row in `tracker/variant-scoreboard.md`.
- Recomputes `tilt` per agent using the advocate/critic counts over the most recent 20 verified decisions.

**Worked entry appended during step 1**:

```markdown
### 2026-04-17T08:30:00Z | lineup | mlb-lineup-optimizer
- **decision_id:** 2026-04-17-lineup-01
- **recommendation:** START Caminero at 3B
- **signals_in:** caminero.daily_quality=78 (matchup=85, form=72, opportunity=80)
- **variants:**
    - advocate -> "Start: strong matchup vs RHP, hitter-friendly park, batting 3rd"
    - critic -> "Sit: 0-for-12 last 3 games, BABIP-driven regression due"
- **dialectical_synthesis:** Advocate wins -- matchup+opportunity outweigh slump. Confidence 0.72.
- **red_team_findings:**
    - severity: 2, likelihood: 3, score: 6, note: "MIA rain watch", mitigation: "Check 1pm forecast"
- **confidence:** 0.72
- **will_verify_on:** 2026-04-18
- **outcome_recorded_on:**
- **outcome:**
- **variant_that_was_right:**
```

After Monday calibration the last three fields are filled in; the scoreboard row for `mlb-lineup-optimizer` increments `Total decisions`, `Advocate correct` (if 1-for-4 with an RBI counted as success), and `Synthesis correct`; `Tilt` is recomputed.

## Workflow

Copy this checklist and track progress for each invocation:

```
Decision Logger Progress:
- [ ] Step 1: Determine mode (append vs calibrate)
- [ ] Step 2: Read current log tail
- [ ] Step 3: Validate payload against schema
- [ ] Step 4: Serialize write (append or in-place edit)
- [ ] Step 5: Update scoreboard (calibration mode only)
- [ ] Step 6: Return decision_id and confirmation
```

**Step 1: Determine mode**

Two supported modes. Exactly one fires per invocation.

- [ ] `append` -- calling agent passes a complete decision payload. Skill creates a new entry.
- [ ] `calibrate` -- calling agent passes an existing `decision_id` plus outcome fields. Skill edits that entry in place and updates the scoreboard.

See [resources/methodology.md](resources/methodology.md#mode-selection) for the full decision tree.

**Step 2: Read current log tail**

Always re-read the log immediately before any write. This is how concurrent writes from parallel agents are serialized without a real file lock.

- [ ] Read the last ~80 lines of `tracker/decisions-log.md`.
- [ ] Parse the last entry's timestamp and `decision_id`.
- [ ] If another agent has written since this invocation started, note new `decision_id` numbers used today.

See [resources/methodology.md](resources/methodology.md#concurrent-writes) for the full serialization protocol.

**Step 3: Validate payload against schema**

Check every required field. Reject (do not write) if any are missing or malformed. The authoritative schema is in `context/frameworks/decision-log-format.md`; [resources/template.md](resources/template.md) mirrors it verbatim.

- [ ] `timestamp_iso8601` is UTC ISO 8601 (`YYYY-MM-DDTHH:MM:SSZ`).
- [ ] `decision_type` in enum: `lineup | waiver | stream | trade | category-plan | playoff-push | add-drop | ad-hoc`.
- [ ] `emitted_by` is a known agent name.
- [ ] `recommendation` starts with an action verb (`START`, `SIT`, `ADD`, `DROP`, `BID $X`, `ACCEPT`, `COUNTER`, `REJECT`, `STREAM`, `HOLD`).
- [ ] `signals_in` references at least one signal by name.
- [ ] `variants` has both `advocate` and `critic` entries (or explicit `n/a` for bootstrap).
- [ ] `confidence` in `[0.00, 1.00]`.
- [ ] `will_verify_on` is a date, `end of week N`, or `end of season`.
- [ ] For `calibrate` mode: `outcome` in `{happened, did not happen, partial}`, `variant_that_was_right` in `{advocate, critic, both, neither}`.

**Step 4: Serialize write**

- [ ] `append`: assign `decision_id` using format `{YYYY-MM-DD}-{decision_type}-{NN}` where NN is `last_same_type_same_day_index + 1`, zero-padded to 2 digits. Append the formatted entry plus a trailing separator line.
- [ ] `calibrate`: locate the target entry by `decision_id`, replace only the three outcome fields, preserve everything else byte-for-byte.
- [ ] Never overwrite the full file. Never reorder entries. Never edit fields other than the three outcome fields.

See [resources/methodology.md](resources/methodology.md#write-protocol).

**Step 5: Update scoreboard (calibration mode only)**

- [ ] Read `tracker/variant-scoreboard.md`.
- [ ] Find the row for the entry's `emitted_by` agent.
- [ ] Increment `Total decisions` by 1.
- [ ] Increment `Advocate correct`, `Critic correct`, or both (for `variant_that_was_right = both`). Increment `Synthesis correct` when the synthesized recommendation matched reality.
- [ ] Recompute `Tilt` per the rules in [resources/methodology.md](resources/methodology.md#tilt-recomputation).
- [ ] Write updated table back; leave all other text unchanged.

**Step 6: Return decision_id and confirmation**

- [ ] Return assigned `decision_id` (append) or confirmation of calibrated fields (calibrate).
- [ ] If validation failed, return structured error with field name and reason; do not write.
- [ ] Validate the final output using [resources/evaluators/rubric_mlb_decision_logger.json](resources/evaluators/rubric_mlb_decision_logger.json). Minimum standard: average score 3.5+, no criterion below 2.

## Common Patterns

**Pattern 1: Parallel agent append (morning brief)**

Coach launches lineup-optimizer, waiver-analyst, and streaming-strategist in one run. Each completes its variant pair, synthesizes, and calls this skill. Skill processes them serially in arrival order, re-reading the log tail between each write, assigning unique `decision_id`s per type.

**Pattern 2: Monday calibration pass**

Coach opens the log, filters for entries where `will_verify_on <= today` and `outcome_recorded_on` is empty, and for each one: web-searches the outcome, builds the calibration payload, calls this skill in `calibrate` mode. Each call edits one entry and updates one scoreboard row.

**Pattern 3: Trade decision (on-demand, deferred verification)**

`mlb-trade-analyzer` fires when a trade offer arrives. The decision is `REJECT`, `ACCEPT`, or `COUNTER`. `will_verify_on` is typically `end of week N` or `end of season` because trade value plays out over weeks. Skill logs normally; the trade stays "open" on the calibration queue until its verify date.

**Pattern 4: Bootstrap / ad-hoc entry**

For team initialization or meta-decisions (changing a weighting, amending a framework), `decision_type = ad-hoc` or `bootstrap`, `variants = n/a`, `variant_that_was_right = neither`. Skill accepts this as a special shape.

## Guardrails

1. **Append only.** Never rewrite the log. Never reorder entries. The only edit allowed is filling in the three outcome fields on an existing entry during calibration. Any other mutation is a bug.

2. **Re-read before every write.** Parallel agents share one file. Reading the tail immediately before writing is the serialization primitive. Do not cache the tail from earlier in the run.

3. **Validate before writing.** A malformed entry poisons downstream calibration. Reject with a structured error; do not attempt partial writes or auto-fix missing fields.

4. **`decision_id` is deterministic.** Same day, same type, sequential NN. If another agent has already used `2026-04-17-lineup-01`, this agent gets `02`. Never reuse an id.

5. **Outcome-editing is surgical.** When filling outcome fields, replace only the three target lines. Preserve timestamps, `decision_id`, recommendation, variants, synthesis, red-team, confidence, and `will_verify_on` byte-for-byte. If you have to reformat to write, you are doing it wrong.

6. **Scoreboard updates are idempotent per decision.** Each `decision_id` contributes exactly one row increment. If a calibration call is retried, re-check whether the entry already has `outcome_recorded_on` populated; if so, do not double-count.

7. **Tilt needs sample size.** Report `neutral` when `Total decisions < 10` for the agent. Only switch to `advocate+` / `critic+` once both sample size and margin are met. See [resources/methodology.md](resources/methodology.md#tilt-recomputation) for exact thresholds.

8. **Agents never write to the log directly.** Every MLB agent routes through this skill. If the coach finds a malformed entry not produced here, treat it as a bug and log it under `tracker/calibration-review.md`.

## Quick Reference

**Mode inputs:**

- `append` needs: `timestamp_iso8601`, `decision_type`, `emitted_by`, `recommendation`, `signals_in`, `variants (advocate + critic)`, `dialectical_synthesis`, `red_team_findings`, `confidence`, `will_verify_on`.
- `calibrate` needs: `decision_id`, `outcome_recorded_on`, `outcome`, `variant_that_was_right`.

**`decision_id` format:**

```
{YYYY-MM-DD}-{decision_type}-{NN}
e.g., 2026-04-17-lineup-01
```

**Tilt thresholds (per agent, over last 20 verified decisions):**

| Condition | Tilt |
|---|---|
| Total < 10 verified | `neutral` |
| Advocate correct > Critic correct by 10 to 20 pct points | `advocate+` |
| Advocate correct > Critic correct by 20+ pct points | `advocate++` |
| Critic correct > Advocate correct by 10 to 20 pct points | `critic+` |
| Critic correct > Advocate correct by 20+ pct points | `critic++` |
| Within 10 pct points | `neutral` |

**Files touched:**

- `~/Documents/Projects/yahoo-mlb/tracker/decisions-log.md` (append, or surgical edit of outcome fields)
- `~/Documents/Projects/yahoo-mlb/tracker/variant-scoreboard.md` (row increments, tilt recompute)
- `~/Documents/Projects/yahoo-mlb/tracker/calibration-review.md` (written only when high-confidence decision was wrong)

**Files read:**

- `~/Documents/Projects/yahoo-mlb/context/frameworks/decision-log-format.md` (schema of record)
- `~/Documents/Projects/yahoo-mlb/tracker/decisions-log.md` (tail, for serialization and id assignment)
- `~/Documents/Projects/yahoo-mlb/tracker/variant-scoreboard.md` (for calibration updates)

**Key resources:**

- **[resources/template.md](resources/template.md)**: The exact entry format mirroring `decision-log-format.md`.
- **[resources/methodology.md](resources/methodology.md)**: Append protocol, calibration protocol, concurrency handling, tilt recomputation, worked sample log sequence.
- **[resources/evaluators/rubric_mlb_decision_logger.json](resources/evaluators/rubric_mlb_decision_logger.json)**: 8-criterion quality rubric.

**Inputs required:**

- From calling agent (append): complete decision payload as above.
- From calling agent (calibrate): `decision_id` and verified outcome fields.

**Outputs produced:**

- Append mode: assigned `decision_id`, confirmation that entry is in the log.
- Calibrate mode: confirmation of which entry was updated and the scoreboard row that changed.
- On validation failure: structured error (field name, reason, offending value), no write performed.
