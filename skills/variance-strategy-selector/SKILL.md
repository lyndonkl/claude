---
name: variance-strategy-selector
description: Given a current win probability and a downside asymmetry flag, recommends a variance-seeking, neutral, or variance-minimizing posture and emits a numeric multiplier (typically 0.8-1.3) for downstream consumers to apply to boom-bust scores, position sizes, or bet sizes. Favorites minimize variance; underdogs maximize it. Reusable across fantasy sports lineup construction, portfolio allocation, poker bankroll decisions, racing strategy, and any decision where the agent controls a variance knob. Use when user mentions variance strategy, underdog variance, variance seeking, variance minimizing, risk posture, boom bust, must-win variance, favorite strategy, or when a decision module needs a single scalar to bias toward or away from high-variance options.
---
# Variance Strategy Selector

## Table of Contents
- [Example](#example)
- [Workflow](#workflow)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Example

**Scenario**: A fantasy manager is 15% behind their opponent with 3 lineup slots left to decide this week. Losing this week eliminates them from playoff contention.

**Inputs**:
- `current_win_probability` = 0.32 (heavy underdog)
- `downside_asymmetry` = 0.90 (must-win, catastrophic if lost)
- `slots_to_decide` = 3

**Band classification**: `win_probability < 0.40` -> posture = "seek", base multiplier range 1.15-1.30.

**Asymmetry amplification**: `downside_asymmetry > 0.8` -> shift multiplier further from 1.0 by +0.10 on the seek side. Base 1.20 + 0.10 = **1.30**.

**Slot-count dampening**: `slots_to_decide = 3`, below the 5-slot threshold -> no dampening applied.

**Outputs**:
- `variance_posture`: "seek"
- `variance_multiplier`: 1.30
- `confidence_band`: "high-variance (seek aggressively)"
- `rationale`: "Pre-move win probability is 0.32 (heavy underdog) and the downside is catastrophic (must-win, asymmetry 0.90). Maximizing variance raises the probability of a right-tail outcome. Consumer should boost high-variance options (boom-bust players, concentrated positions, longshot bets) by 30%."

**Consumer application** (downstream skill applies the multiplier):
```
adjusted_player_score = base_score x (1 + (boom_bust_score - 0.5) x (variance_multiplier - 1))
```
A boom-bust score of 0.8 (high-variance player) with multiplier 1.30 gets a +9% boost relative to a steady player.

## Workflow

Copy this checklist and track progress:

```
Variance Strategy Selection Progress:
- [ ] Step 1: Collect inputs (win_probability, downside_asymmetry, slots_to_decide)
- [ ] Step 2: Classify win-probability band (seek / neutral / minimize)
- [ ] Step 3: Apply downside-asymmetry amplification
- [ ] Step 4: Apply slot-count dampening
- [ ] Step 5: Clamp multiplier to valid range and validate monotonicity
- [ ] Step 6: Emit structured output with rationale
```

**Step 1: Collect inputs**

- [ ] `current_win_probability` is a float in [0, 1]. Reject values outside this range.
- [ ] `downside_asymmetry` is a float in [0, 1] where 1.0 = losing is catastrophic (must-win for playoffs, elimination game, bankroll ruin).
- [ ] `slots_to_decide` is a non-negative integer representing how many independent decisions this posture covers (lineup slots, portfolio positions, bet sequence length).

See [resources/template.md](resources/template.md#input-validation-checklist) for input validation rules.

**Step 2: Classify win-probability band**

Apply the three-band rule:

- [ ] `win_probability < 0.40` -> posture = "seek", base multiplier 1.15-1.30
- [ ] `0.40 <= win_probability <= 0.60` -> posture = "neutral", base multiplier 1.00
- [ ] `win_probability > 0.60` -> posture = "minimize", base multiplier 0.80-0.90

Within the "seek" band, pick the base multiplier proportional to how far below 0.40 the probability is: `base = 1.15 + (0.40 - win_probability) x 0.375`, clamped to 1.30. Within "minimize", mirror: `base = 0.90 - (win_probability - 0.60) x 0.25`, clamped to 0.80.

See [resources/methodology.md](resources/methodology.md#why-underdogs-want-variance) for the underlying right-tail / left-tail logic.

**Step 3: Apply downside-asymmetry amplification**

If the loss is catastrophic, the underdog must swing harder and the favorite must protect harder. The adjustment is symmetric around 1.0.

- [ ] If `downside_asymmetry > 0.8` and posture = "seek": shift multiplier +0.10 (further above 1.0)
- [ ] If `downside_asymmetry > 0.8` and posture = "minimize": shift multiplier -0.10 (further below 1.0)
- [ ] If `downside_asymmetry > 0.8` and posture = "neutral": no shift (neutral remains neutral by definition)
- [ ] If `downside_asymmetry <= 0.8`: no shift

**Step 4: Apply slot-count dampening**

With many independent decisions, the Central Limit Theorem diversifies variance on its own. Pushing the multiplier hard across many slots is redundant.

- [ ] If `slots_to_decide > 5`: dampen the distance from 1.0 by a factor of `5 / slots_to_decide` (bounded below at 0.5). E.g. with 10 slots, reduce the gap by half.
- [ ] If `slots_to_decide <= 5`: no dampening.

See [resources/methodology.md](resources/methodology.md#central-limit-dampening) for the math.

**Step 5: Clamp and validate monotonicity**

- [ ] Clamp the final multiplier to the range [0.70, 1.40]. Values outside this range indicate an input or computation error.
- [ ] Confirm monotonicity: as `win_probability` decreases, multiplier must weakly increase. As `downside_asymmetry` increases, |multiplier - 1.0| must weakly increase.

**Step 6: Emit structured output**

Return the four required fields:

- [ ] `variance_posture` -- "seek" | "neutral" | "minimize"
- [ ] `variance_multiplier` -- final number in [0.70, 1.40]
- [ ] `confidence_band` -- short human-readable descriptor (e.g. "high-variance (seek aggressively)", "low-variance (protect the lead)")
- [ ] `rationale` -- 2-3 sentences citing win probability band, asymmetry flag, slot count effect, and how the consumer should interpret the multiplier

Validate using [resources/evaluators/rubric_variance_strategy_selector.json](resources/evaluators/rubric_variance_strategy_selector.json). Minimum standard: average score of 3.5 or above.

## Common Patterns

**Pattern 1: Heavy underdog, must-win (fantasy sports)**
- Inputs: win_prob ~0.30, asymmetry ~0.90, slots 1-3
- Output: posture "seek", multiplier ~1.30
- Rationale: Swing for the fences. Prefer a high-K / high-HR boom-bust hitter over a high-contact singles hitter; prefer a volatile SP with upside over a stable #4 starter. Consumer skill (e.g. `mlb-lineup-optimizer`) multiplies boom-bust weight by 1.30.

**Pattern 2: Heavy favorite, large portfolio / many slots**
- Inputs: win_prob ~0.75, asymmetry ~0.50, slots ~12 (full lineup / diversified portfolio)
- Output: posture "minimize", multiplier ~0.92 (after slot dampening from 0.85)
- Rationale: Protect the lead, but don't over-engineer -- with 12 slots the portfolio is already diversified by the Central Limit effect. Small damp on the variance knob is enough. Consumer reduces concentration / boom-bust weight by 8%.

**Pattern 3: Even matchup (poker mid-stack)**
- Inputs: win_prob ~0.50, asymmetry ~0.40, slots ~5 (next 5 hands)
- Output: posture "neutral", multiplier 1.00
- Rationale: Play close to GTO. No variance tilt either way. Consumer applies no adjustment to bet sizing.

**Pattern 4: Mild favorite, one decisive decision (racing / options expiry)**
- Inputs: win_prob ~0.65, asymmetry ~0.85, slots 1
- Output: posture "minimize", multiplier ~0.75 (base 0.85 - 0.10 asymmetry shift, no slot dampening)
- Rationale: One shot, lead to protect, catastrophic if squandered. The race leader does not take the high-risk inside line; the hedged call writer does not lift the hedge on expiry day. Consumer hard-damps variance.

## Guardrails

1. **Bands are hard, not fuzzy.** Do not interpolate the posture label across 0.40 and 0.60 thresholds. Posture is categorical (seek / neutral / minimize); the multiplier is continuous within each band. Consumers rely on the categorical label for branching logic.

2. **Asymmetry amplifies, never reverses.** A catastrophic downside makes a favorite more conservative and an underdog more aggressive. It never flips the direction. If the computed multiplier would cross 1.0 because of an asymmetry shift, clamp at 1.0 and recheck inputs.

3. **Slot dampening applies to the distance from 1.0, not to the multiplier itself.** Implementation: `final = 1.0 + (pre_dampening - 1.0) x min(1.0, 5 / slots)`. Dampening 1.30 across 10 slots gives 1.15, not 0.65.

4. **Edge cases at probability 0 and 1.** If `win_probability = 0`, posture is "seek" with maximum multiplier (1.30 pre-asymmetry, 1.40 post); the analogy is a lottery ticket -- variance is the only path to a non-zero outcome. If `win_probability = 1`, posture is "minimize" with maximum damp (0.80 pre-asymmetry, 0.70 post); any variance is pure downside. Document these explicitly in the rationale.

5. **The multiplier is a nudge, not a command.** It biases the downstream optimizer; it does not replace the optimizer. A 1.30 multiplier does not mean "start only boom-bust players." It means "up-weight boom-bust scores by 30% relative to stable scores within whatever optimization the consumer runs."

6. **Downside asymmetry is not the same as win probability.** A heavy underdog in week 1 of a season has low win probability but low asymmetry (plenty of chances to recover). The same underdog in week 20 has high asymmetry (last chance). Ask for both inputs; do not infer one from the other.

7. **Independence assumption underlies slot dampening.** Central-limit diversification works when slot outcomes are independent. If slots are highly correlated (e.g. all pitchers on the same team, all tech stocks in a portfolio), dampening is weaker. Flag this assumption in the rationale when the consumer domain is known to be correlated.

8. **Domain-neutral by design.** This skill does not know whether the decision is a fantasy lineup, a portfolio, a poker session, or a race. It emits a scalar. The consumer attaches domain-specific meaning. Do not hard-code domain jargon in the rationale -- use neutral terms like "high-variance options" and "stable options."

## Quick Reference

**Three-band rule:**

| Win probability | Posture | Base multiplier range |
|---|---|---|
| `< 0.40` | seek | 1.15 - 1.30 |
| `0.40 - 0.60` | neutral | 1.00 |
| `> 0.60` | minimize | 0.80 - 0.90 |

**Asymmetry shift (applied when `downside_asymmetry > 0.8`):**

| Posture | Shift |
|---|---|
| seek | +0.10 |
| neutral | 0 |
| minimize | -0.10 |

**Slot dampening:**

```
if slots_to_decide > 5:
    factor = max(0.5, 5 / slots_to_decide)
    multiplier = 1.0 + (multiplier - 1.0) x factor
```

**Full computation sketch:**

```python
def variance_strategy(p_win, asym, slots):
    # 1. Band
    if p_win < 0.40:
        posture = "seek"
        base = 1.15 + (0.40 - p_win) * 0.375
        base = min(base, 1.30)
    elif p_win > 0.60:
        posture = "minimize"
        base = 0.90 - (p_win - 0.60) * 0.25
        base = max(base, 0.80)
    else:
        posture = "neutral"
        base = 1.00

    # 2. Asymmetry
    if asym > 0.8 and posture == "seek":
        base += 0.10
    elif asym > 0.8 and posture == "minimize":
        base -= 0.10

    # 3. Slot dampening
    if slots > 5:
        factor = max(0.5, 5 / slots)
        base = 1.0 + (base - 1.0) * factor

    # 4. Clamp
    multiplier = max(0.70, min(1.40, base))
    return posture, multiplier
```

**Key resources:**

- **[resources/template.md](resources/template.md)**: Input validation checklist, worked examples across 4 scenarios (heavy underdog must-win, modest underdog, even, heavy favorite), output format
- **[resources/methodology.md](resources/methodology.md)**: Kelly Criterion reference, variance-of-sum math, right-tail / left-tail probability reasoning, Central Limit dampening, domain parallels (fantasy, poker, horse racing, portfolio)
- **[resources/evaluators/rubric_variance_strategy_selector.json](resources/evaluators/rubric_variance_strategy_selector.json)**: 8-criterion quality rubric for band accuracy, asymmetry adjustment, slot dampening, multiplier range, rationale clarity, edge cases, monotonicity, citations

**Inputs required:**

- `current_win_probability` (float, 0-1): point estimate of win probability before the variance decision is made
- `downside_asymmetry` (float, 0-1): 1.0 = losing is catastrophic (elimination, bankroll ruin); 0.5 = routine; 0.0 = no downside consequence
- `slots_to_decide` (int, >= 0): number of independent decisions this posture will be applied across

**Outputs produced:**

- `variance_posture` (string): "seek" | "neutral" | "minimize"
- `variance_multiplier` (float, 0.70-1.40): scalar for consumer to multiply against boom-bust / volatility / concentration scores
- `confidence_band` (string): short human-readable posture descriptor
- `rationale` (string): 2-3 sentences citing band, asymmetry, slot count, and interpretation

**Referenced by (consumers):**

- `mlb-lineup-optimizer` (fantasy baseball lineup selection under daily_quality x leverage x variance_multiplier)
- Portfolio allocation skills that weight high-beta vs low-beta positions
- Poker bankroll skills that pick bet-size variance
- Any agent deciding how hard to push a variance knob

**Principle reference:** Game Theory Principles #6 (Variance-seeking as underdog -- the "cope" principle) in `/Users/kushaldsouza/Documents/Projects/yahoo-mlb/context/frameworks/game-theory-principles.md`.
