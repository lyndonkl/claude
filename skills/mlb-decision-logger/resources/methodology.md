# MLB Decision Logger Methodology

Complete operational procedures for appending, calibrating, serializing concurrent writes, and recomputing the variant scoreboard.

## Table of Contents
- [Mode Selection](#mode-selection)
- [Append Protocol](#append-protocol)
- [Calibration Protocol](#calibration-protocol)
- [Concurrent Writes](#concurrent-writes)
- [Write Protocol](#write-protocol)
- [Scoreboard Update](#scoreboard-update)
- [Tilt Recomputation](#tilt-recomputation)
- [Validation Rules](#validation-rules)
- [Failure Handling](#failure-handling)
- [Sample Log Sequence](#sample-log-sequence)

---

## Mode Selection

Exactly one mode fires per skill invocation. The calling agent declares the mode in its payload.

```
IF payload.mode == "append":
    go to Append Protocol
ELIF payload.mode == "calibrate":
    go to Calibration Protocol
ELSE:
    return error: "mode must be 'append' or 'calibrate'"
```

If the payload has both a full decision body AND a `decision_id` with outcome fields, treat as ambiguous and reject. The agent must pick one.

---

## Append Protocol

**Purpose**: Add a brand-new entry. Never rewrites existing content.

```
1. Validate payload (see Validation Rules).
2. Read the tail (~80 lines) of tracker/decisions-log.md.
3. Parse all entries from TODAY matching decision_type.
4. Set NN = max(existing NN for that day+type) + 1, zero-padded to 2 digits.
   If none today yet, NN = 01.
5. Assemble decision_id = {YYYY-MM-DD}-{decision_type}-{NN}.
6. Format the entry block exactly per resources/template.md.
7. Leave outcome_recorded_on, outcome, variant_that_was_right empty.
8. Append to tracker/decisions-log.md:
   a. blank line
   b. formatted entry block
   c. blank line
   d. `---` separator
9. Return decision_id to caller.
```

**Example NN assignment** on 2026-04-17 where the log already contains `2026-04-17-lineup-01` and `2026-04-17-waiver-01`:

- next `lineup` append -> `2026-04-17-lineup-02`
- next `waiver` append -> `2026-04-17-waiver-02`
- next `stream` append -> `2026-04-17-stream-01`

---

## Calibration Protocol

**Purpose**: Fill in `outcome_recorded_on`, `outcome`, `variant_that_was_right` on an existing entry. Nothing else changes.

```
1. Validate payload has: decision_id, outcome_recorded_on, outcome,
   variant_that_was_right.
2. Read tracker/decisions-log.md. Locate entry by exact decision_id match.
3. If entry not found: return error "decision_id not in log".
4. If entry already has outcome_recorded_on populated: return
   "already calibrated on {date}" -- do not overwrite.
5. Surgical edit:
   - Find line "- **outcome_recorded_on:**" in that entry block.
   - Replace with "- **outcome_recorded_on:** {date}".
   - Same pattern for outcome and variant_that_was_right.
   - Preserve all other bytes (timestamps, decision_id line, recommendation,
     variants, synthesis, red-team, confidence, will_verify_on).
6. Update the scoreboard (see Scoreboard Update).
7. If confidence was >= 0.80 and outcome == "did not happen" (or the variant
   that was right was the critic despite high-confidence advocate synthesis):
   append a lesson entry to tracker/calibration-review.md.
8. Return "calibrated {decision_id}; scoreboard row {agent} updated".
```

The calibration pass does NOT touch any other field. If an outcome is genuinely unknown on the verify date, the caller should postpone by re-calling the skill with a future date -- but this requires explicit edit of `will_verify_on`, which is OUT OF SCOPE for this skill (manual edit by coach with audit note).

---

## Concurrent Writes

Multiple agents can call this skill in one coach run (typical morning brief fires 2-4 agents). There is no OS-level file lock; serialization is achieved by:

```
FOR each skill invocation:
    1. Re-read the log tail IMMEDIATELY before writing.
       (Do NOT cache the tail from earlier in the run.)
    2. Compute decision_id from the just-read tail.
    3. Write.
    4. If between step 1 and step 3 another agent wrote an entry with
       the same candidate decision_id (race condition), the write collides
       by having two entries with identical ids. Detection:
       - After write, re-read the last 20 lines.
       - If two entries share the assigned decision_id, the LATER
         (this invocation's) entry increments NN and rewrites in place:
         find the duplicate-id line and replace just that line with the
         bumped id. Nothing else changes.
    5. Return the final (possibly bumped) decision_id.
```

In practice, a single-threaded coach serializing skill calls avoids step 4 entirely. The collision-detection exists as a safety net, not the primary mechanism.

---

## Write Protocol

**Append writes**:
- Open file in append mode.
- Write: `\n` + entry block + `\n---\n`.
- Close. (Treat `\n` consistency with existing file; `decisions-log.md` uses LF.)

**Calibration edits**:
- Read full file into memory.
- Locate the three target lines within the target entry block by substring match on `- **outcome_recorded_on:**`, `- **outcome:**`, `- **variant_that_was_right:**` *within* the block starting with `### ... decision_id: {id}`.
- Replace those three lines only.
- Write the full file back.
- Verify by re-reading: the only byte-level diff should be on those three lines.

**Never**:
- Rewrite the entire log in append mode.
- Reorder entries.
- Edit any field other than the three outcome fields during calibration.
- Delete entries.

---

## Scoreboard Update

On every successful calibration:

```
1. Read tracker/variant-scoreboard.md.
2. Parse the markdown table; find the row where Agent == entry.emitted_by.
3. Update cells:
   - Total decisions += 1
   - Advocate correct += 1 if variant_that_was_right in {advocate, both}
   - Critic correct   += 1 if variant_that_was_right in {critic, both}
   - Synthesis correct increment rule:
     * outcome == "happened"       -> +1
     * outcome == "did not happen" -> +0
     * outcome == "partial"        -> +0.5 (shown as e.g. "3.5" in the cell)
4. Recompute Tilt (see next section).
5. Write the table back, leaving all other document text unchanged.
```

Idempotency: before step 3, confirm the entry being calibrated does NOT already have `outcome_recorded_on` populated from a previous call. If it does, skip scoreboard update (already counted).

---

## Tilt Recomputation

For each agent, compute over the **most recent 20 verified decisions** (those with `outcome_recorded_on` populated). If fewer than 10 verified, tilt is `neutral` regardless of ratio.

```
N = min(20, count of verified decisions for this agent)
IF N < 10:
    tilt = "neutral"
ELSE:
    adv_pct = advocate_correct_in_window / N * 100
    crit_pct = critic_correct_in_window / N * 100
    diff = adv_pct - crit_pct   # positive = advocate ahead
    IF diff >= 20:
        tilt = "advocate++"
    ELIF diff >= 10:
        tilt = "advocate+"
    ELIF diff <= -20:
        tilt = "critic++"
    ELIF diff <= -10:
        tilt = "critic+"
    ELSE:
        tilt = "neutral"
```

"Both" counts toward both `adv_pct` and `crit_pct` in that window. "Neither" counts toward neither.

The coach reads `tilt` at the start of each run and passes it into `dialectical-mapping-steelmanning` as a prior weighting hint.

---

## Validation Rules

Reject the payload (do not write) when any of the following fail:

| Rule | Failure example |
|---|---|
| `timestamp_iso8601` matches `YYYY-MM-DDTHH:MM:SSZ` | `2026-4-17 8:30` |
| `decision_type` in enum | `benching` |
| `emitted_by` is a known agent | `mlb-hype-bot` |
| `recommendation` starts with an action verb (`START, SIT, ADD, DROP, BID $X, ACCEPT, COUNTER, REJECT, STREAM, HOLD`) | `Consider starting Caminero` |
| `signals_in` references at least one named signal (`.` in the string or `=`) | `good matchup` |
| `variants.advocate` and `variants.critic` both present (or both `n/a` for bootstrap/ad-hoc) | only `advocate` |
| `confidence` in `[0.00, 1.00]` | `1.15`, `-0.1` |
| `will_verify_on` parseable as date, `end of week N`, or `end of season` | `soonish` |
| For calibrate: `outcome` in `{happened, did not happen, partial}` | `kinda` |
| For calibrate: `variant_that_was_right` in `{advocate, critic, both, neither}` | `synthesis` |

On failure, return:

```
{ error: "validation_failed",
  field: "<name>",
  received: "<value>",
  reason: "<why>" }
```

---

## Failure Handling

- **Log file missing**: do not create. Return error "log file not found at {path}". Coach must run bootstrap first.
- **Log file malformed** (can't parse the last entry): return error; do not attempt auto-repair. Coach investigates.
- **Duplicate `decision_id` detected after write**: bump NN and rewrite the offending id line only (see Concurrent Writes step 4).
- **Calibration on already-calibrated entry**: return "already calibrated" -- safe no-op, do not double-count.
- **Scoreboard file missing or malformed**: write the log entry first (successful), then return a second error about the scoreboard. The log append must not be rolled back.

---

## Sample Log Sequence

A full end-to-end trace: initial entry on Friday 2026-04-17, calibration pass on Monday 2026-04-21, scoreboard update.

### Step A: Initial append (Friday morning)

Coach invokes the logger with this payload from `mlb-lineup-optimizer`:

```yaml
mode: append
timestamp_iso8601: "2026-04-17T08:30:00Z"
decision_type: lineup
emitted_by: mlb-lineup-optimizer
recommendation: "START Caminero at 3B"
signals_in: "caminero.daily_quality=78 (matchup=85, form=72, opportunity=80)"
variants:
  advocate: "Start: strong matchup vs RHP, hitter-friendly park, batting 3rd"
  critic: "Sit: 0-for-12 last 3 games, BABIP-driven regression due"
dialectical_synthesis: "Advocate wins -- matchup+opportunity outweigh slump. Confidence 0.72."
red_team_findings:
  - severity: 2
    likelihood: 3
    score: 6
    note: "MIA rain watch"
    mitigation: "Check 1pm forecast; have Bench-A ready"
confidence: 0.72
will_verify_on: "2026-04-18"
```

Logger:

1. Reads tail of `decisions-log.md`. Last entry is bootstrap, dated 2026-04-17T00:00:00Z. No other 2026-04-17 `lineup` entries.
2. Assigns `decision_id = 2026-04-17-lineup-01`.
3. Appends this block to the log:

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
    - severity: 2, likelihood: 3, score: 6, note: "MIA rain watch", mitigation: "Check 1pm forecast; have Bench-A ready"
- **confidence:** 0.72
- **will_verify_on:** 2026-04-18
- **outcome_recorded_on:**
- **outcome:**
- **variant_that_was_right:**

---
```

4. Returns `{ decision_id: "2026-04-17-lineup-01", status: "appended" }`.

### Step B: Calibration pass (Monday morning)

Coach reads the log, sees `will_verify_on = 2026-04-18 <= 2026-04-21` and outcome fields empty. Web-searches and finds: Caminero went 2-for-4 with a 2B and an RBI. Classifies as `happened` (a started player producing is what the rec bet on). Calls the logger:

```yaml
mode: calibrate
decision_id: "2026-04-17-lineup-01"
outcome_recorded_on: "2026-04-21"
outcome: "happened"
variant_that_was_right: "advocate"
```

Logger:

1. Finds the entry.
2. `outcome_recorded_on` is empty -- proceed.
3. Surgically replaces the three empty outcome lines:

```markdown
- **outcome_recorded_on:** 2026-04-21
- **outcome:** happened
- **variant_that_was_right:** advocate
```

4. Updates scoreboard row for `mlb-lineup-optimizer`.

### Step C: Scoreboard update

Before:

```markdown
| mlb-lineup-optimizer | 0 | 0 | 0 | 0 | neutral |
```

After:

```markdown
| mlb-lineup-optimizer | 1 | 1 | 0 | 1 | neutral |
```

`Tilt` stays `neutral` because `N = 1 < 10`.

After the 11th verified decision (say advocate-correct on 8, critic-correct on 3, synthesis-correct on 9):

```
adv_pct = 8/11 * 100 = 72.7
crit_pct = 3/11 * 100 = 27.3
diff = 45.4 -> tilt = "advocate++"
```

Row becomes:

```markdown
| mlb-lineup-optimizer | 11 | 8 | 3 | 9 | advocate++ |
```

Coach will now pass `advocate_bias: strong` into `dialectical-mapping-steelmanning` for future lineup decisions.

### Step D: High-confidence miss triggers calibration-review

If the same decision had `confidence: 0.85` and `outcome: did not happen` (Caminero went 0-for-4, critic was right), the logger additionally appends an entry to `tracker/calibration-review.md` such as:

```markdown
## 2026-04-21: Overconfident lineup call
- **decision_id:** 2026-04-17-lineup-01
- **agent:** mlb-lineup-optimizer
- **confidence:** 0.85
- **outcome:** did not happen
- **variant_that_was_right:** critic
- **lesson:** High confidence despite explicit critic warning about 3-game slump was not warranted; slump signal should have capped confidence at 0.70 until form signal >= 70.
```

This closes the loop and seeds tomorrow's weighting.
