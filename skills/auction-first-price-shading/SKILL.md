---
name: auction-first-price-shading
description: Computes the optimal shaded bid for a first-price sealed-bid auction given a true private value, an estimate of the number of competing bidders N, and a value-distribution assumption. Implements the `(N-1)/N` equilibrium shading rule for uniform private values, adjusts for log-normal or empirical value distributions, layers a risk-aversion adjustment, and caps output against the bidder's remaining budget. Domain-neutral auction theory reusable across fantasy sports (baseball FAAB, NBA/NHL waiver auctions), prediction-market limit sizing, sealed procurement bids, and any blind-bid context. Use when user mentions "first-price auction bid", "sealed bid shading", "(N-1)/N", "FAAB bid amount", "auction shading", "optimal bid first-price", "bid for sealed-bid", "blind bid sizing", or when downstream logic needs a principled shade factor rather than an ad-hoc heuristic.
---
# Auction First-Price Shading

## Table of Contents
- [Example](#example)
- [Workflow](#workflow)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Example

**Scenario**: Domain-neutral sealed-bid auction. A bidder must submit a blind bid for an item whose private value to them is 28 units of budget currency. Six other bidders are expected to compete. Values across bidders look roughly uniform. The bidder is mildly risk-averse (0.2) and has 89 units of budget remaining.

**Inputs**:
- `true_value = 28`
- `n_bidders_estimate = 6`
- `value_distribution = "uniform"`
- `risk_aversion = 0.2`
- `budget_remaining = 89`

**Core computation**:
```
shade_fraction_base = (N - 1) / N = 5 / 6 = 0.833
shaded_bid_base     = true_value x shade_fraction_base = 28 x 0.833 = 23.33
```

**Risk-aversion adjustment** (raise the bid toward true value to boost win probability):
```
shade_fraction' = shade + risk_aversion x (1 - shade) x 0.4
                = 0.833 + 0.2 x (1 - 0.833) x 0.4
                = 0.833 + 0.0133
                = 0.847
shaded_bid'     = 28 x 0.847 = 23.72
```

**Budget + safety cap**:
```
cap = min(shaded_bid', 0.9 x true_value, budget_remaining)
    = min(23.72, 25.2, 89)
    = 23.72  -> round to 24
```

**Output**:
- `shaded_bid = 24`
- `shade_fraction = 0.847`
- `rationale = "Uniform-values equilibrium shades to (N-1)/N = 0.833 at N=6. Mild risk aversion (0.2) nudges bid up to 0.847 of true value to raise win probability. Final bid capped below 0.9x true_value and well under budget. Expected to win against 5 rivals drawing values from a comparable uniform distribution."`
- `assumptions_flagged = ["uniform private-value distribution", "N=6 is an estimate, not observed", "risk_aversion=0.2 is a modeling choice"]`

## Workflow

Copy this checklist and track progress:

```
Auction Shading Progress:
- [ ] Step 1: Validate inputs (true_value > 0, 1 <= N <= 12, distribution known)
- [ ] Step 2: Compute base shade from (N-1)/N
- [ ] Step 3: Apply distribution adjustment (uniform / log-normal / empirical)
- [ ] Step 4: Apply risk-aversion adjustment
- [ ] Step 5: Apply budget and safety caps
- [ ] Step 6: Emit shaded_bid, shade_fraction, rationale, assumptions_flagged
```

**Step 1: Validate inputs**

Reject or flag bad inputs before computing. See [resources/template.md](resources/template.md#input-contract) for the full input contract.

- [ ] `true_value` is a non-negative number
- [ ] `n_bidders_estimate` is an integer, clamp to `[1, 12]`
- [ ] `value_distribution` is one of `"uniform"`, `"log-normal"`, `"empirical"`
- [ ] `risk_aversion` is in `[0, 1]` (default 0 if missing)
- [ ] `budget_remaining` is a non-negative number (if missing, treat as effectively infinite and flag)

**Step 2: Compute base shade from `(N-1)/N`**

For risk-neutral bidders drawing values from a uniform distribution on `[0, v_max]`, the symmetric Bayes-Nash equilibrium bidding strategy is `b(v) = v x (N-1)/N`. See [resources/methodology.md](resources/methodology.md#uniform-value-equilibrium-derivation) for the derivation.

- [ ] `shade_fraction = (N - 1) / N`
- [ ] Edge case `N = 1`: shade = 0, bid the minimum increment (monopsonist — no competition)
- [ ] `shaded_bid = true_value x shade_fraction`

**Step 3: Apply distribution adjustment**

Uniform values give the clean `(N-1)/N` rule. Real-world value distributions are often clustered (log-normal) or empirically lumpy. See [resources/methodology.md](resources/methodology.md#distribution-adjustment).

- [ ] If `"uniform"`: no adjustment; shade = `(N-1)/N`.
- [ ] If `"log-normal"`: values cluster around a mode with a long right tail. Shift shade toward `1 - 1/(N x spread)` where `spread >= 1` captures the coefficient of variation. Default `spread = 1.5` shifts shade up (bid closer to value) because rivals' values are less likely to be extreme.
- [ ] If `"empirical"`: distribution learned from prior auctions; pass through a shade-lookup table if available, otherwise fall back to the log-normal formula with spread inferred from observed history.

**Step 4: Apply risk-aversion adjustment**

Risk-averse bidders accept a smaller expected surplus in exchange for a higher win probability. They bid closer to true value (shade less). See [resources/methodology.md](resources/methodology.md#risk-aversion-adjustment).

- [ ] `shade_fraction' = shade + risk_aversion x (1 - shade) x 0.4`
- [ ] `risk_aversion = 0`: no change.
- [ ] `risk_aversion = 1`: shade moves 40 percent of the way from its base value to 1 (i.e., toward bidding true value).
- [ ] The 0.4 scaling factor caps the adjustment; it never closes the full gap because a fully-closed gap gives zero surplus.

**Step 5: Apply budget and safety caps**

The final bid is clamped three ways:

- [ ] `cap_value = 0.9 x true_value` — never pay more than 90 percent of what the item is worth; this preserves at least 10 percent expected surplus.
- [ ] `cap_budget = budget_remaining` — never bid more than available budget.
- [ ] `shaded_bid = min(raw_shaded_bid, cap_value, cap_budget)`.
- [ ] Flag in `assumptions_flagged` whenever a cap binds so downstream consumers know which constraint is active.

**Step 6: Emit outputs**

Return the four-field output:

- [ ] `shaded_bid` (number, rounded to the precision the caller expects — integers for most budget systems)
- [ ] `shade_fraction` (0-1, the effective shade actually used)
- [ ] `rationale` (one or two sentences explaining which rule applied and why)
- [ ] `assumptions_flagged` (string array — every assumption the downstream consumer may need to revisit)

Validate using [resources/evaluators/rubric_auction_first_price_shading.json](resources/evaluators/rubric_auction_first_price_shading.json). Minimum standard: weighted score of 3.5 or above.

## Common Patterns

**Pattern 1: Generic sealed-bid auction (uniform values, risk-neutral)**
- **When it applies**: Values are drawn from roughly the same distribution for all bidders, no unique information, no risk aversion.
- **Shade**: `(N-1)/N`. At N=2 shade to 50 percent. At N=6 shade to 83 percent. At N=8 shade to 87.5 percent.
- **Downstream examples**: Fantasy sports waiver auctions (FAAB) for private-value targets, sealed procurement bids, silent-auction pledges.

**Pattern 2: Clustered values (log-normal or empirical)**
- **When it applies**: Most bidders' valuations cluster around a shared estimate (common-value component), with a thin tail of outliers. Typical of well-known targets where public information narrows the spread of valuations.
- **Shade**: move toward `1 - 1/(N x spread)`. Higher spread means more disagreement and permits deeper shading. Low spread (tight cluster) means less room to shade — bidders must be near consensus to win.
- **Downstream examples**: FAAB bids on headline call-ups, prediction-market limit orders on well-priced contracts, M&A sealed-bid rounds with shared public data.

**Pattern 3: Risk-averse bidder**
- **When it applies**: The bidder values winning more than maximizing expected surplus — for example, a fantasy manager who must fill a lineup slot this week, or a procurement team that must secure supply.
- **Shade adjustment**: `shade' = shade + risk_aversion x (1 - shade) x 0.4`. Pushes the bid closer to true value.
- **Watch for**: never lets shade reach 1 (never bids true value), because that yields zero expected surplus. The cap at `0.9 x true_value` enforces this hard.

**Pattern 4: Budget-constrained bidder (corner solution)**
- **When it applies**: The unconstrained shaded bid exceeds `budget_remaining`. The bidder must either accept a lower win probability or forgo the auction.
- **Shade adjustment**: output equals `budget_remaining`, effective shade = `budget_remaining / true_value`. Flag that the budget constraint binds so downstream logic can decide whether to skip the auction or accept the lower probability.
- **Watch for**: If `budget_remaining < (N-1)/N x true_value`, the bidder is under-resourced to compete — flag and let the caller decide.

## Guardrails

1. **`(N-1)/N` is a symmetric-equilibrium result, not a universal truth.** It assumes all bidders use the same bidding function and draw values from the same distribution. If one bidder systematically overbids, optimal response shifts. Flag in `assumptions_flagged` whenever the user has signals that rivals are not symmetric.

2. **N is an estimate, not a datum.** Most callers do not know N exactly. Small errors in N matter little (the shade function is smooth), but mistaking N=2 for N=6 changes the bid from 50 percent to 83 percent of value. Always flag `n_bidders_estimate` as an assumption.

3. **Clamp N to `[1, 12]`.** Values below 1 are nonsense. Values above 12 rarely improve the bid materially (shade at N=12 is 0.917 vs. 0.875 at N=8) and are usually overconfident. Clamping protects against upstream errors.

4. **Never bid above `0.9 x true_value`.** This is a hard cap. Even with heavy risk aversion or very large N, crossing 0.9 reduces expected surplus below the point where shading has economic value.

5. **Never bid above `budget_remaining`.** The shaded bid is clamped to available budget. If the clamp binds, the output flag must say so — the downstream consumer may prefer to skip rather than bid the full budget on a single item.

6. **`N = 1` is a corner case.** With no competition, the dominant strategy is to bid the minimum increment (often 1 unit, sometimes 0). The skill returns `shaded_bid = max(1, floor_bid)` and flags "no competition — minimum bid wins." Callers supplying their own floor should pass it explicitly; this skill defaults to 1.

7. **Risk aversion does not dominate the math.** The adjustment `shade' = shade + risk_aversion x (1 - shade) x 0.4` is bounded by the 0.4 scaling factor. The final bid is still capped at `0.9 x true_value`. Do not let a risk-averse user bid true value.

8. **This skill is domain-neutral.** It knows nothing about baseball, prediction markets, or procurement. Downstream consumers (e.g., `mlb-faab-sizer` for fantasy baseball, or a procurement agent for sealed supplier bids) wrap this skill with domain-specific value estimation, urgency multipliers, and winner's-curse haircuts.

## Quick Reference

**Key formulas:**

```
Uniform-value risk-neutral equilibrium:
  shade_fraction = (N - 1) / N
  shaded_bid     = true_value x shade_fraction

Log-normal / empirical-cluster adjustment:
  shade_fraction_adj = 1 - 1 / (N x spread)     # spread >= 1 (CoV proxy)
  default spread = 1.5

Risk-aversion adjustment:
  shade_fraction_ra = shade + risk_aversion x (1 - shade) x 0.4

Final bid (all caps applied):
  shaded_bid = min(true_value x shade_fraction_final,
                   0.9 x true_value,
                   budget_remaining)
```

**Shade table (uniform, risk-neutral):**

| N | shade_fraction | Example: bid on true_value = 100 |
|---|----------------|-----------------------------------|
| 1 | 0.00 | 1 (minimum increment) |
| 2 | 0.50 | 50 |
| 3 | 0.67 | 67 |
| 4 | 0.75 | 75 |
| 5 | 0.80 | 80 |
| 6 | 0.83 | 83 |
| 8 | 0.875 | 87 (then capped at 90) |
| 10 | 0.90 | 90 (exactly at cap) |
| 12 | 0.917 | 90 (cap binds) |

**Input contract:**

- `true_value` (number, >= 0) — bidder's own private valuation in units of budget currency
- `n_bidders_estimate` (int, clamped to `[1, 12]`) — total number of realistic bidders including self
- `value_distribution` (`"uniform"` | `"log-normal"` | `"empirical"`) — shape assumption
- `risk_aversion` (number, `[0, 1]`, default 0) — 0 = risk-neutral, 1 = maximally risk-averse
- `budget_remaining` (number, >= 0) — hard ceiling on the output

**Output contract:**

- `shaded_bid` (number) — the deterministic bid to submit
- `shade_fraction` (number, `[0, 1]`) — effective shade actually applied
- `rationale` (string) — one-two sentence explanation for the rationale log
- `assumptions_flagged` (string[]) — every modeling assumption the caller may want to revisit

**Key resources:**

- **[resources/template.md](resources/template.md)**: Full input/output contract and a worked example
- **[resources/methodology.md](resources/methodology.md)**: Formal derivation of `(N-1)/N`, log-normal adjustment, risk-aversion adjustment, revenue equivalence theorem, three worked examples at N=2, N=6, N=8
- **[resources/evaluators/rubric_auction_first_price_shading.json](resources/evaluators/rubric_auction_first_price_shading.json)**: Eight-criterion rubric with weighted scoring
