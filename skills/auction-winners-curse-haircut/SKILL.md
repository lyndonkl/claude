---
name: auction-winners-curse-haircut
description: Applies a Bayesian haircut to a bid valuation for common-value auctions where winning is itself evidence the bidder over-estimated. Takes a raw valuation, a value-type classification (common_value / private_value / mixed), the number of informed bidders N, and a signal-dispersion estimate, and returns an adjusted valuation. Domain-neutral and reusable across fantasy FAAB, prediction markets, M&A bids, ad-auction budgets, and any generic bidding context. Use when user mentions "winner's curse", "common value auction", "valuation haircut", "adverse valuation", "Bayesian bid adjustment", or "over-paying in auction".
---
# Auction Winner's-Curse Haircut

## Table of Contents
- [Example](#example)
- [Workflow](#workflow)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Example

**Scenario**: Bidder has estimated a target's value at `raw_valuation = $30`. Six informed bidders are competing. Estimates across bidders are moderately dispersed (signal_dispersion = 40 out of 100). The target is a well-known commodity (everyone models it similarly).

**Inputs**:
- `raw_valuation`: 30
- `value_type`: `common_value`
- `n_informed_bidders`: 6
- `signal_dispersion`: 40

**Haircut computation**:
```
haircut_pct = min(35, 10 + log(6) x 5 + 40 x 0.2)
            = min(35, 10 + 1.792 x 5 + 8)
            = min(35, 10 + 8.96 + 8)
            = min(35, 26.96)
            = 26.96  (clamped below 35 ceiling)
```

**Output**:
- `adjusted_valuation` = 30 x (1 - 0.2696) = **$21.91**
- `haircut_pct` = **26.96**
- `classification_rationale`: "Common-value target with 6 informed bidders and moderate signal dispersion. Winning is material evidence of over-estimation; Kagel-Levin experimental range (15-30%) applies."
- `applied`: **true**

**Contrast -- private-value case**: Same raw_valuation = $30, but value_type = `private_value` (target matters uniquely to this bidder). Haircut = 0. Adjusted = $30. Applied = false. Rationale: "No informational-asymmetry discount; winning is not adverse because other bidders do not value the target similarly."

## Workflow

Copy this checklist and track progress:

```
Winner's-Curse Haircut Progress:
- [ ] Step 1: Classify value_type (common / private / mixed)
- [ ] Step 2: Validate inputs (range checks, N >= 1)
- [ ] Step 3: Short-circuit for private-value
- [ ] Step 4: Compute haircut_pct via formula
- [ ] Step 5: Apply haircut to raw_valuation
- [ ] Step 6: Emit structured output with rationale
```

**Step 1: Classify `value_type`**

Classification is a judgment call and MUST be explicit. The caller should pass it; this skill validates the choice against the decision tree in [resources/template.md](resources/template.md#value-type-decision-tree).

- [ ] `common_value` -- target's value is similar for all bidders because information is shared and the underlying quantity is the same (examples: named closer on waivers, headline prospect call-up, publicly traded stock in a tender, liquid commodity)
- [ ] `private_value` -- target's value is meaningfully higher (or lower) for this bidder than for others, due to fit, complementarity, or idiosyncratic preference (examples: handcuff to a reliever you already own, platoon fit for your lineup, a house next door to an existing property)
- [ ] `mixed` -- target has a shared core value plus a private-value increment (examples: late-season FAAB claim on a hot hitter where everyone agrees on the base projection but the bidder's specific category need is extra)

**Step 2: Validate inputs**

- [ ] `raw_valuation` is a finite non-negative number
- [ ] `value_type` is one of the three allowed strings
- [ ] `n_informed_bidders` is an integer >= 1 (clamp at upper bound if exotic, e.g. 50)
- [ ] `signal_dispersion` is in [0, 100]

**Step 3: Short-circuit for private-value**

If `value_type == "private_value"`, skip the formula entirely:
- `haircut_pct = 0`
- `adjusted_valuation = raw_valuation`
- `applied = false`

See [resources/methodology.md](resources/methodology.md#why-private-value-gets-zero-haircut) for the Bayesian reason this short-circuit is correct.

**Step 4: Compute haircut percentage**

For `common_value` targets:

```
haircut_pct = min(35, 10 + log(N) x 5 + signal_dispersion x 0.2)
```

The `min(35, ...)` ceiling hard-caps the haircut at 35% even at extreme N and dispersion. This reflects that empirical Kagel-Levin estimates rarely exceed 30%; 35% is the outer envelope.

For `mixed` targets, interpolate:

```
mix_common_weight  = 0.6  (default; caller may override)
mix_private_weight = 1 - mix_common_weight
haircut_pct = mix_common_weight x (common_value_haircut) + mix_private_weight x 0
```

See [resources/methodology.md](resources/methodology.md#haircut-formula-derivation) for formula intuition (log-N captures the adverse-selection severity growing with more competitors; linear dispersion term captures the variance of bidder estimates).

**Step 5: Apply haircut**

```
adjusted_valuation = raw_valuation x (1 - haircut_pct / 100)
```

**Step 6: Emit structured output**

Return:

```
{
  "adjusted_valuation": <number>,
  "haircut_pct": <number in [0, 35]>,
  "classification_rationale": "<one-sentence justification>",
  "applied": <bool>
}
```

Validate using [resources/evaluators/rubric_auction_winners_curse_haircut.json](resources/evaluators/rubric_auction_winners_curse_haircut.json). Minimum standard: average score >= 3.5.

## Common Patterns

**Pattern 1: Headline Common-Value Target, Many Bidders**
- **Example**: Top-100 prospect call-up in fantasy FAAB (N=6-8); prediction-market contract on a high-salience event; M&A target covered by many investment banks
- **Typical inputs**: N in [5, 10], signal_dispersion in [30, 60]
- **Typical haircut**: 22-32%
- **Why**: Strong adverse-selection; winning almost surely means you were highest of many similar estimates
- **Watch for**: Do not double-count with first-price shading -- the two are independent corrections (see `auction-first-price-shading` for shading)

**Pattern 2: Private-Value Complement (Handcuff)**
- **Example**: Backup reliever to your own closer; land adjacent to land you already own; puzzle piece that fits only your collection
- **Typical inputs**: N = 1-2, value_type = `private_value`
- **Typical haircut**: 0% (short-circuited)
- **Why**: No adverse selection -- winning is not evidence you over-estimated, because others genuinely value the target less
- **Watch for**: Make sure the private-value claim is real. If three other bidders also have a complementary use, it is closer to common-value

**Pattern 3: Mixed Late-Season Streaming Claim**
- **Example**: Hot hitter whose projection everyone agrees on, but fits a specific category need you have; ad-auction keyword with a common CPC baseline but a bidder-specific conversion uplift
- **Typical inputs**: N in [3, 5], signal_dispersion in [20, 40], value_type = `mixed` with mix_common_weight around 0.5-0.7
- **Typical haircut**: 10-18%
- **Why**: Partial adverse selection, partial private value
- **Watch for**: Explicitly estimate and record the common/private split; do not default to mixed when a clear binary classification applies

**Pattern 4: Thin-Field Common Value (Low N)**
- **Example**: Niche common-value target in a small auction pool (N = 2)
- **Typical inputs**: N = 2, dispersion anywhere
- **Typical haircut**: 14-18%
- **Why**: Even with only 2 bidders, common-value winner's curse operates -- winning means you exceeded the other informed estimate. Still smaller than large-N cases because adverse-selection severity grows with log(N)
- **Watch for**: Do not set haircut to 0 just because N is low; private-value requires a separate claim about value heterogeneity

## Guardrails

1. **Classification must be explicit.** Never infer `value_type` silently from other inputs. The caller passes it; the skill validates. A missing or ambiguous classification is an error, not a default.

2. **Private-value short-circuit is absolute.** If the caller asserts private-value, haircut is zero even when N is large. This is correct: if others genuinely value the target less, then their bids do not carry adverse information about your own estimate.

3. **Never stack this haircut with another winner's-curse correction.** Downstream systems that already apply Bayesian bid shading (e.g., auction-first-price-shading's N-bidder shade) are correcting a different phenomenon (strategic shading for expected surplus). Apply both; do not apply either twice.

4. **Cap at 35%.** The empirical Kagel-Levin range is 15-30%. The 35% ceiling provides headroom for very large N plus high dispersion but prevents the formula from producing absurd discounts (e.g., 80%).

5. **N >= 1.** N = 1 means the bidder is alone; `log(1) = 0` so the formula yields `haircut_pct = 10 + signal_dispersion x 0.2`. For a true monopsony (no competing informed bidder), the caller should pass `private_value` instead -- there is no adverse-selection mechanism without competitors.

6. **Signal dispersion is a proxy, not a measurement.** In practice it is rarely directly observable. Estimate from: historical bid-spread in comparable auctions, disagreement among public projection systems, or degree of public information asymmetry. Document the basis.

7. **Mixed value requires an explicit weight.** Do not silently default to 0.6. Callers should state the common/private split and its justification. If they cannot, classify as common_value (conservative) or private_value (aggressive), not mixed.

8. **Domain-neutral contract.** This skill does not know about FAAB, fantasy baseball, or any specific auction environment. Callers translate their domain inputs into the generic four-field contract; the skill returns a generic output which the caller then interprets.

## Quick Reference

**Core formula:**

```
if value_type == "private_value":
    haircut_pct = 0
    applied = false

elif value_type == "common_value":
    haircut_pct = min(35, 10 + log(N) x 5 + signal_dispersion x 0.2)
    applied = true

elif value_type == "mixed":
    common_haircut = min(35, 10 + log(N) x 5 + signal_dispersion x 0.2)
    haircut_pct = mix_common_weight x common_haircut   # default 0.6
    applied = true

adjusted_valuation = raw_valuation x (1 - haircut_pct / 100)
```

**Haircut lookup (common_value, approximate):**

| N | dispersion=0 | dispersion=25 | dispersion=50 | dispersion=100 |
|---|--------------|---------------|---------------|----------------|
| 1 | 10.0% | 15.0% | 20.0% | 30.0% |
| 2 | 13.5% | 18.5% | 23.5% | 33.5% |
| 4 | 16.9% | 21.9% | 26.9% | 35.0% (cap) |
| 6 | 19.0% | 24.0% | 29.0% | 35.0% (cap) |
| 8 | 20.4% | 25.4% | 30.4% | 35.0% (cap) |
| 12 | 22.4% | 27.4% | 32.4% | 35.0% (cap) |

**Input contract:**

| Field | Type | Range | Required |
|-------|------|-------|----------|
| `raw_valuation` | number | >= 0 | yes |
| `value_type` | string | `common_value` / `private_value` / `mixed` | yes |
| `n_informed_bidders` | int | >= 1 | yes |
| `signal_dispersion` | number | [0, 100] | yes |
| `mix_common_weight` | number | [0, 1] | only if `mixed` (default 0.6) |

**Output contract:**

| Field | Type | Range |
|-------|------|-------|
| `adjusted_valuation` | number | [0, raw_valuation] |
| `haircut_pct` | number | [0, 40] |
| `classification_rationale` | string | one sentence |
| `applied` | bool | false iff private-value |

**Key resources:**

- **[resources/template.md](resources/template.md)**: Classification decision tree (common vs private vs mixed), worked examples (closer = common; handcuff = private; late-season hot hitter = mixed), input/output templates
- **[resources/methodology.md](resources/methodology.md)**: Kagel & Levin experimental evidence, formal Bayesian posterior derivation, log-N and dispersion intuition, value-type classification heuristics with fantasy-FAAB examples, why private-value gets zero haircut
- **[resources/evaluators/rubric_auction_winners_curse_haircut.json](resources/evaluators/rubric_auction_winners_curse_haircut.json)**: 8-criterion quality rubric
