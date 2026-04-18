# Variance Strategy Selector Templates

Decision rules, input validation, worked examples, and output formats for the variance-strategy-selector skill.

## Table of Contents
- [Input Validation Checklist](#input-validation-checklist)
- [Decision Rule Reference](#decision-rule-reference)
- [Worked Example 1: Heavy Underdog Must-Win](#worked-example-1-heavy-underdog-must-win)
- [Worked Example 2: Modest Underdog](#worked-example-2-modest-underdog)
- [Worked Example 3: Even Matchup](#worked-example-3-even-matchup)
- [Worked Example 4: Heavy Favorite](#worked-example-4-heavy-favorite)
- [Output Format Template](#output-format-template)
- [Monotonicity Test Cases](#monotonicity-test-cases)

---

## Input Validation Checklist

Before classifying posture, validate all three inputs:

- [ ] `current_win_probability` is a float in the closed interval [0, 1]. Reject NaN, None, or values outside range.
- [ ] `downside_asymmetry` is a float in [0, 1]. If unknown, default to 0.5 (routine downside) and note the default in the rationale.
- [ ] `slots_to_decide` is a non-negative integer. If 0 slots are to be decided, the skill has nothing to do -- return posture "neutral" and multiplier 1.0 with a note that no decisions are pending.

**Common input pitfalls:**

| Pitfall | Example | Fix |
|---|---|---|
| Probability given as percentage | `win_probability = 65` | Divide by 100 to get 0.65. Always 0-1. |
| Asymmetry confused with stake size | "$10,000 is at stake" | Asymmetry is ratio of loss-pain to win-pleasure, not absolute stake. |
| Slot count includes already-locked slots | "12 lineup spots" when 9 are locked | Use only slots still being decided. |
| Win probability is a range, not a point | "between 30% and 40%" | Use midpoint (0.35) and flag uncertainty in rationale. |

---

## Decision Rule Reference

**Three-band classification** (hard thresholds):

```
win_probability < 0.40             -> posture = "seek"
0.40 <= win_probability <= 0.60    -> posture = "neutral"
win_probability > 0.60             -> posture = "minimize"
```

**Base multiplier within band:**

```
seek band:      base = 1.15 + (0.40 - win_probability) * 0.375,  clamped to [1.15, 1.30]
neutral band:   base = 1.00
minimize band:  base = 0.90 - (win_probability - 0.60) * 0.25,   clamped to [0.80, 0.90]
```

**Asymmetry shift** (applied when `downside_asymmetry > 0.8`):

```
seek + high asymmetry     -> base + 0.10
neutral + high asymmetry  -> no change
minimize + high asymmetry -> base - 0.10
```

**Slot-count dampening** (applied when `slots_to_decide > 5`):

```
factor = max(0.5, 5 / slots_to_decide)
multiplier = 1.0 + (base - 1.0) * factor
```

**Final clamp:**

```
multiplier = max(0.70, min(1.40, multiplier))
```

---

## Worked Example 1: Heavy Underdog Must-Win

**Scenario**: Fantasy manager down 15% in a must-win elimination week. 3 lineup slots left to decide.

**Inputs**:
- `current_win_probability` = 0.30
- `downside_asymmetry` = 0.90
- `slots_to_decide` = 3

**Step 1 -- Band**: 0.30 < 0.40 -> "seek". Base = 1.15 + (0.40 - 0.30) x 0.375 = 1.15 + 0.0375 = 1.1875 (rounded to 1.19).

**Step 2 -- Asymmetry**: 0.90 > 0.8 and posture = "seek" -> shift +0.10. Base = 1.29.

**Step 3 -- Slot dampening**: 3 <= 5 -> no dampening.

**Step 4 -- Clamp**: 1.29 is in [0.70, 1.40] -> 1.29.

**Output**:
```yaml
variance_posture: seek
variance_multiplier: 1.29
confidence_band: "high-variance (seek aggressively)"
rationale: >
  Pre-move win probability is 0.30 (heavy underdog, seek band) and the downside
  is catastrophic (asymmetry 0.90, elimination week), shifting the multiplier a
  further +0.10 above baseline. Only 3 slots remain, so no Central-Limit
  dampening applies. Consumer should boost the weighting of high-variance
  options (boom-bust players, concentrated positions, longshot bets) by 29%.
```

---

## Worked Example 2: Modest Underdog

**Scenario**: Poker player 10% behind in chip equity at a tournament final table, not yet elimination-critical. Next 8 hands to play.

**Inputs**:
- `current_win_probability` = 0.38
- `downside_asymmetry` = 0.55
- `slots_to_decide` = 8

**Step 1 -- Band**: 0.38 < 0.40 -> "seek". Base = 1.15 + (0.40 - 0.38) x 0.375 = 1.15 + 0.0075 = 1.16.

**Step 2 -- Asymmetry**: 0.55 is not > 0.8 -> no shift. Base = 1.16.

**Step 3 -- Slot dampening**: 8 > 5 -> factor = 5/8 = 0.625. Multiplier = 1.0 + (1.16 - 1.0) x 0.625 = 1.0 + 0.10 = 1.10.

**Step 4 -- Clamp**: 1.10 is in range -> 1.10.

**Output**:
```yaml
variance_posture: seek
variance_multiplier: 1.10
confidence_band: "mildly high-variance (tilt, don't swing)"
rationale: >
  Pre-move win probability is 0.38 (mild underdog, seek band). Downside is not
  catastrophic (asymmetry 0.55), so no amplification. With 8 independent
  decisions, Central-Limit dampening (factor 0.625) pulls the multiplier from
  1.16 to 1.10. Consumer should lightly favor higher-variance options (+10%)
  across the sequence.
```

---

## Worked Example 3: Even Matchup

**Scenario**: Portfolio allocator rebalancing 6 positions, market outlook roughly even, no near-term drawdown crisis.

**Inputs**:
- `current_win_probability` = 0.52
- `downside_asymmetry` = 0.40
- `slots_to_decide` = 6

**Step 1 -- Band**: 0.40 <= 0.52 <= 0.60 -> "neutral". Base = 1.00.

**Step 2 -- Asymmetry**: 0.40 is not > 0.8 -> no shift. (Also: neutral posture gets no asymmetry shift regardless.)

**Step 3 -- Slot dampening**: 6 > 5 -> factor = 5/6 = 0.833. Multiplier = 1.0 + (1.00 - 1.0) x 0.833 = 1.00. (Dampening toward 1.0 has no effect when already at 1.0.)

**Step 4 -- Clamp**: 1.00 -> 1.00.

**Output**:
```yaml
variance_posture: neutral
variance_multiplier: 1.00
confidence_band: "neutral (no variance tilt)"
rationale: >
  Pre-move win probability is 0.52 (even matchup, neutral band). No downside
  asymmetry to amplify. Consumer should apply no variance adjustment; choose
  options on base merit (expected value, quality score) without a volatility
  tilt.
```

---

## Worked Example 4: Heavy Favorite

**Scenario**: Racing strategist holding a 0.5-second lead with 2 laps remaining. One decision (pit or stay out). Losing this race ends the championship.

**Inputs**:
- `current_win_probability` = 0.78
- `downside_asymmetry` = 0.95
- `slots_to_decide` = 1

**Step 1 -- Band**: 0.78 > 0.60 -> "minimize". Base = 0.90 - (0.78 - 0.60) x 0.25 = 0.90 - 0.045 = 0.855 (rounded to 0.86).

**Step 2 -- Asymmetry**: 0.95 > 0.8 and posture = "minimize" -> shift -0.10. Base = 0.76.

**Step 3 -- Slot dampening**: 1 <= 5 -> no dampening.

**Step 4 -- Clamp**: 0.76 is in [0.70, 1.40] -> 0.76.

**Output**:
```yaml
variance_posture: minimize
variance_multiplier: 0.76
confidence_band: "low-variance (protect the lead hard)"
rationale: >
  Pre-move win probability is 0.78 (heavy favorite, minimize band) and the
  downside is catastrophic (asymmetry 0.95, championship-ending), shifting
  the multiplier a further -0.10 below baseline. Single decisive decision,
  so no Central-Limit dampening. Consumer should aggressively damp
  high-variance options (longshot pit strategy, boom-bust positions) by 24%.
```

---

## Output Format Template

Every invocation returns these four fields:

```yaml
variance_posture: <"seek" | "neutral" | "minimize">
variance_multiplier: <float in [0.70, 1.40]>
confidence_band: <short descriptor string>
rationale: |
  Pre-move win probability is <p> (<band descriptor>).
  <Asymmetry effect sentence: either "Downside is catastrophic (asymmetry <a>)..."
   or "Downside is routine (asymmetry <a>), no amplification.">
  <Slot effect sentence: either "With <n> slots, Central-Limit dampening reduces
   the multiplier from <pre> to <post>." or "Only <n> slots, no dampening.">
  Consumer should <"boost" | "leave unchanged" | "damp"> the weighting of
  high-variance options by <|multiplier - 1| * 100>%.
```

Canonical field names follow snake_case to match consumer skills' expectations.

---

## Monotonicity Test Cases

Use these to verify correct implementation. Each row holds two inputs fixed and varies one; the multiplier should move in the indicated direction.

**Win-probability monotonicity (asym=0.5, slots=3):**

| win_probability | expected posture | expected multiplier |
|---|---|---|
| 0.00 | seek | 1.30 |
| 0.20 | seek | 1.23 (1.15 + 0.20 x 0.375 = 1.225) |
| 0.35 | seek | 1.17 |
| 0.50 | neutral | 1.00 |
| 0.65 | minimize | 0.89 |
| 0.80 | minimize | 0.85 |
| 1.00 | minimize | 0.80 |

As `win_probability` increases, multiplier must weakly decrease.

**Downside-asymmetry monotonicity (win_prob=0.25, slots=3):**

| downside_asymmetry | expected multiplier |
|---|---|
| 0.0 | 1.21 (base only) |
| 0.5 | 1.21 |
| 0.8 | 1.21 (threshold not strictly exceeded) |
| 0.81 | 1.31 (above threshold; shift applies) |
| 1.0 | 1.31 |

As asymmetry crosses 0.8, |multiplier - 1.0| jumps up.

**Slot-count dampening (win_prob=0.25, asym=0.5):**

| slots_to_decide | expected multiplier |
|---|---|
| 1 | 1.21 |
| 5 | 1.21 |
| 10 | 1.10 (1.0 + 0.21 x 0.5) |
| 20 | 1.05 (1.0 + 0.21 x 0.25, but floor 0.5 on factor) -> 1.10 |
| 100 | 1.10 (factor floored at 0.5) |

As slots increase, multiplier asymptotes toward (but does not cross) 1.0, with the factor floor preserving some variance tilt.
