# Decision Log Entry Template

The authoritative schema lives at `~/Documents/Projects/yahoo-mlb/context/frameworks/decision-log-format.md`. This file mirrors that schema verbatim so the logger skill has a local reference. If the two diverge, `decision-log-format.md` wins and this file must be updated.

## Table of Contents
- [Entry Schema](#entry-schema)
- [Field Reference](#field-reference)
- [Decision Type Enum](#decision-type-enum)
- [Action Verb Vocabulary](#action-verb-vocabulary)
- [Append-Mode Payload](#append-mode-payload)
- [Calibrate-Mode Payload](#calibrate-mode-payload)
- [Filled Example](#filled-example)
- [Variant Scoreboard Row Schema](#variant-scoreboard-row-schema)

---

## Entry Schema

Every entry appended to `tracker/decisions-log.md` MUST match this markdown block exactly:

```markdown
### {timestamp_iso8601} | {decision_type} | {emitted_by}
- **decision_id:** {YYYY-MM-DD}-{decision_type}-{NN}
- **recommendation:** {terse verb + object; e.g., "START Caminero at 3B"}
- **signals_in:** {key_signals: values}
- **variants:**
    - advocate -> {position summary}
    - critic -> {position summary}
- **dialectical_synthesis:** {what the skill returned -- which variant won, or what third-way emerged}
- **red_team_findings:**
    - severity: {1-5}, likelihood: {1-5}, score: {s x l}, note: "{risk}", mitigation: "{action}"
- **confidence:** {0.00 - 1.00}
- **will_verify_on:** {YYYY-MM-DD or "end of week N" or "end of season"}
- **outcome_recorded_on:** {YYYY-MM-DD -- filled in by calibration pass}
- **outcome:** {happened / did not happen / partial -- filled in later}
- **variant_that_was_right:** {advocate / critic / both / neither -- filled in later}
```

Separator line (a bare `---` on its own line) follows each entry.

---

## Field Reference

| Field | Required at append? | Required at calibrate? | Format |
|---|---|---|---|
| `timestamp_iso8601` | yes | no (read-only) | `YYYY-MM-DDTHH:MM:SSZ` UTC |
| `decision_type` | yes | no (read-only) | enum; see below |
| `emitted_by` | yes | no (read-only) | agent name, e.g. `mlb-lineup-optimizer` |
| `decision_id` | auto-assigned | yes (lookup key) | `{YYYY-MM-DD}-{decision_type}-{NN}` |
| `recommendation` | yes | no (read-only) | starts with action verb |
| `signals_in` | yes | no (read-only) | `{name}={value}`, comma-separated |
| `variants.advocate` | yes (or `n/a`) | no (read-only) | 1-2 sentence position summary |
| `variants.critic` | yes (or `n/a`) | no (read-only) | 1-2 sentence position summary |
| `dialectical_synthesis` | yes (or `n/a`) | no (read-only) | resolution statement |
| `red_team_findings` | yes (or `n/a`) | no (read-only) | severity, likelihood, score, note, mitigation |
| `confidence` | yes | no (read-only) | float in `[0.00, 1.00]` |
| `will_verify_on` | yes | no (read-only) | date, `end of week N`, or `end of season` |
| `outcome_recorded_on` | empty at append | yes | `YYYY-MM-DD` |
| `outcome` | empty at append | yes | `happened` / `did not happen` / `partial` |
| `variant_that_was_right` | empty at append | yes | `advocate` / `critic` / `both` / `neither` |

---

## Decision Type Enum

```
lineup           daily start/sit from mlb-lineup-optimizer
waiver           weekly add/drop from mlb-waiver-analyst
stream           streaming-pitcher pickup from mlb-streaming-strategist
trade            trade offer evaluation from mlb-trade-analyzer
category-plan    weekly category push/punt from mlb-category-strategist
playoff-push     July+ playoff planning from mlb-playoff-planner
add-drop         ad-hoc roster move outside weekly waiver run
ad-hoc           meta-decision (framework change, weighting tweak)
```

(`bootstrap` also appears as a seed-entry type but is not emitted by agents mid-season.)

---

## Action Verb Vocabulary

The `recommendation` field must start with one of these verbs (case-sensitive):

```
START, SIT, ADD, DROP, BID $X, ACCEPT, COUNTER, REJECT, STREAM, HOLD
```

Matches the "action ladder" rule in `CLAUDE.md`. "Consider", "think about", "maybe" are rejected.

---

## Append-Mode Payload

What a calling agent hands to this skill when creating a new entry:

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

Skill auto-assigns `decision_id` and leaves the three outcome fields blank.

---

## Calibrate-Mode Payload

What a calling agent hands to this skill when filling in an outcome:

```yaml
mode: calibrate
decision_id: "2026-04-17-lineup-01"
outcome_recorded_on: "2026-04-21"
outcome: "happened"
variant_that_was_right: "advocate"
```

Skill locates the entry, overwrites only the three outcome fields, updates the scoreboard row for `emitted_by`.

---

## Filled Example

Final state of a complete, calibrated entry:

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
- **outcome_recorded_on:** 2026-04-21
- **outcome:** happened
- **variant_that_was_right:** advocate

---
```

---

## Variant Scoreboard Row Schema

Scoreboard table in `tracker/variant-scoreboard.md` uses this column layout:

```
| Agent | Total decisions | Advocate correct | Critic correct | Synthesis correct | Tilt |
```

One row per agent. On each calibration, the logger:

1. Increments `Total decisions` by 1.
2. Increments `Advocate correct` if `variant_that_was_right in {advocate, both}`.
3. Increments `Critic correct` if `variant_that_was_right in {critic, both}`.
4. Increments `Synthesis correct` if the synthesized recommendation matched reality (`outcome = happened` for a "do X" rec, or `outcome = did not happen` for a "do not do X" rec; `partial` counts as 0.5 and is tracked via a decimal in the cell).
5. Recomputes `Tilt` per the thresholds in `methodology.md`.

Empty scoreboard starts as:

```markdown
| Agent | Total decisions | Advocate correct | Critic correct | Synthesis correct | Tilt |
|---|---|---|---|---|---|
| mlb-lineup-optimizer | 0 | 0 | 0 | 0 | neutral |
| mlb-waiver-analyst | 0 | 0 | 0 | 0 | neutral |
| mlb-streaming-strategist | 0 | 0 | 0 | 0 | neutral |
| mlb-trade-analyzer | 0 | 0 | 0 | 0 | neutral |
| mlb-category-strategist | 0 | 0 | 0 | 0 | neutral |
| mlb-playoff-planner | 0 | 0 | 0 | 0 | neutral |
```
