# Auction First-Price Shading — Methodology

This document derives the formulas used by `auction-first-price-shading` from auction-theoretic first principles. It is organized from the cleanest case (uniform values, risk-neutral, symmetric bidders) to progressively richer models (log-normal values, risk aversion, budget constraints).

## Table of Contents
- [Why Shading Exists](#why-shading-exists)
- [Uniform-Value Equilibrium Derivation](#uniform-value-equilibrium-derivation)
- [Vickrey (Second-Price) Reference](#vickrey-second-price-reference)
- [Revenue Equivalence Theorem](#revenue-equivalence-theorem)
- [Distribution Adjustment (Log-Normal and Empirical)](#distribution-adjustment-log-normal-and-empirical)
- [Risk-Aversion Adjustment](#risk-aversion-adjustment)
- [Budget and Safety Caps](#budget-and-safety-caps)
- [Worked Examples](#worked-examples)
  - [Example A — N = 2, uniform, risk-neutral](#example-a--n--2-uniform-risk-neutral)
  - [Example B — N = 6, uniform, mild risk aversion](#example-b--n--6-uniform-mild-risk-aversion)
  - [Example C — N = 8, log-normal, budget-constrained](#example-c--n--8-log-normal-budget-constrained)

---

## Why Shading Exists

In a first-price sealed-bid auction, each bidder submits one blind bid. The highest bid wins and pays their own bid. If a bidder bids their true value `v`, the surplus conditional on winning is exactly zero — they pay what the item is worth to them.

To capture any positive expected surplus, the bidder must shade their bid below `v`. But shading too deeply lowers win probability. The optimal shade balances **win probability** against **surplus per win**.

Formally, the bidder's expected surplus is:

```
E[surplus] = P(win | b) x (v - b)
```

where `b` is the bid and `P(win | b)` is the probability that `b` is the highest bid. Optimal `b` maximizes this product — a classic calculus-of-variations problem whose closed-form solution for uniform values is `b = v x (N-1)/N`.

Shading is not a psychological fudge factor. It is the rational response to the fact that winning and surplus are in tension.

---

## Uniform-Value Equilibrium Derivation

**Setup.** `N` bidders each draw a private value `v_i` independently and uniformly on `[0, 1]` (the interval is arbitrary; the result is scale-invariant). Each bidder knows their own value but only the distribution of others'. All bidders are risk-neutral.

**Symmetric equilibrium.** Assume all bidders use the same bid function `b(v)` that is continuous and strictly increasing. Under symmetry, bidder `i` wins iff `v_i` is the highest draw (the equilibrium bid function is monotonic, so highest value -> highest bid -> winner).

**Probability of winning with value v:** the probability that all `N-1` rivals have values below `v` is:

```
P(v_i highest) = v^(N-1)   (since values are iid Uniform[0,1])
```

**Expected surplus for a bidder with value `v` who bids `b(v)`:**

```
E[surplus | v] = v^(N-1) x (v - b(v))
```

**First-order condition.** In equilibrium, `b(v)` maximizes the bidder's expected surplus given that rivals use the same function. Taking the derivative with respect to `b` (using the inverse bid function `phi(b) = v`):

After the standard derivation (differentiate, apply the envelope theorem, integrate the resulting ODE with boundary condition `b(0) = 0`), the symmetric Bayes-Nash equilibrium bid function is:

```
b*(v) = ((N - 1) / N) x v
```

That is, **each bidder shades their bid to `(N-1)/N` of their true value**. This is the foundational formula the skill uses as its base case.

**Interpretation of `(N-1)/N`:** the shade approaches 1 as `N` grows (with many rivals, you must bid close to value to have any chance of winning). It falls sharply to 0.5 at `N = 2` (with only one rival, you can keep half the surplus). At `N = 1` it is 0 — but the formula is vacuous because there is no auction to win or lose; you bid the minimum increment.

**Expected surplus at equilibrium:**

```
E[surplus | v] = v^(N-1) x (v - (N-1)/N x v)
              = v^(N-1) x v / N
              = v^N / N
```

This shrinks rapidly with N — at N = 6, expected surplus is `v^6 / 6`, a tiny fraction of `v`. The intuition: in heavily contested auctions, even the equilibrium shade leaves very little meat on the bone.

---

## Vickrey (Second-Price) Reference

For calibration, contrast with a Vickrey auction (second-price sealed-bid). There, the dominant strategy is to bid **exactly your true value**: `b(v) = v`. The winner pays the second-highest bid, so truthful bidding is incentive-compatible — shading creates no benefit and only risks losing.

**Why this matters to the first-price skill:** Vickrey is the benchmark of truthful bidding. Every dollar of shading in a first-price auction represents the bidder exploiting the fact that they must pay their own bid rather than the next-highest. Shading reflects the mechanism, not the bidder's taste.

---

## Revenue Equivalence Theorem

**Statement.** Under independent private values, risk-neutral bidders, and any mechanism that (a) always allocates the item to the bidder with the highest value and (b) gives zero surplus to a bidder with zero value, the expected revenue to the seller is the same across mechanisms.

**Consequence.** First-price (shade to `(N-1)/N v`) and second-price (bid truthfully) auctions yield identical expected revenue to the seller and identical expected surplus to each bidder *ex ante*. What differs is the realized distribution across bidders, not the expected value.

**Why it justifies the skill.** The `(N-1)/N` shade is not merely a heuristic — it is the bid level that makes a first-price auction revenue-equivalent to a second-price auction. Any rule that deviates systematically is leaving expected surplus on the table.

---

## Distribution Adjustment (Log-Normal and Empirical)

The `(N-1)/N` formula assumes uniform values. Real-world distributions often look log-normal: most bidders' valuations cluster around a shared estimate, with a thin tail of outliers. This happens whenever there is a shared common-value component — a well-known item, public information available to all, industry-standard pricing.

**Key fact.** For a general symmetric distribution with CDF `F(v)`, the equilibrium bid function is:

```
b*(v) = v - (1 / F(v)^(N-1)) x integral from 0 to v of F(t)^(N-1) dt
```

For uniform `F(v) = v`, this reduces to `b*(v) = v (N-1)/N`. For other distributions, the shade depends on the shape of `F`.

**Log-normal approximation.** For values clustered around a mode with coefficient of variation (CoV) approximately `sigma` and heavier right tail, the equilibrium bid function is close to:

```
shade_fraction_log-normal = 1 - 1 / (N x spread)
```

where `spread >= 1` proxies for the CoV-like dispersion:
- `spread = 1` recovers the uniform formula `(N-1)/N`.
- `spread > 1` shifts shade upward (bid closer to value) because tight clustering means the second-highest value is likely close to the highest — there is less surplus to capture by deep shading.
- Default in this skill: `spread = 1.5` when the caller does not supply one.

**Empirical distributions.** When historical auction data is available, the caller can pass `value_distribution = "empirical"` and optionally a fitted `spread` from observed bids. The skill uses the log-normal formula as a tractable fallback unless a shade-lookup table is supplied.

**When this matters.** If bidders' values are sharply bimodal or multi-modal, neither uniform nor log-normal fits — the skill flags this in `assumptions_flagged` and the caller is responsible for supplying a better estimate or accepting the approximation.

---

## Risk-Aversion Adjustment

**Theory.** A risk-averse bidder has concave utility over surplus. They prefer a higher win probability at the cost of lower expected surplus per win. In the first-price model, this translates to bidding closer to true value (shading less).

**Formal result.** For CARA (constant absolute risk aversion) utility `u(x) = 1 - e^(-a x)` with coefficient `a > 0`, the equilibrium bid function for uniform values satisfies:

```
b_risk-averse(v) > b_risk-neutral(v) for all v in (0, v_max)
```

with the gap growing in `a`. For small `a`, a first-order approximation gives:

```
b_risk-averse(v) approx b_risk-neutral(v) + c x a x (v - b_risk-neutral(v))
```

for some constant `c in (0, 1)` depending on `N` and the distribution.

**Skill's adjustment.** The skill uses a simple, defensible approximation that captures the qualitative behavior:

```
shade_fraction_ra = shade + risk_aversion x (1 - shade) x 0.4
```

- `risk_aversion = 0`: no change; recovers risk-neutral shade.
- `risk_aversion = 1`: closes 40 percent of the gap between shade and 1 (true-value bidding).
- The `0.4` scaling factor caps the adjustment. It never fully closes the gap because closing the gap gives zero expected surplus regardless of win probability — which makes no rational sense under any risk preference that permits any surplus.

**Why 0.4?** Empirically reasonable range. With `0.5` the adjustment is too aggressive — at maximum risk aversion you would bid 50 percent of the way to true value, which for large N pushes past the 0.9 cap constantly. With `0.3` the adjustment barely moves the needle at mid-risk-aversion levels. `0.4` keeps most adjusted bids below the 0.9 cap while still producing visibly different behavior at different risk-aversion levels.

---

## Budget and Safety Caps

Three caps clamp the final bid:

**1. Safety cap: `0.9 x true_value`.** Never bid above 90 percent of own valuation. Rationale: below this, expected surplus is meaningful; above it, the bidder is essentially bidding for the mechanism (winning for its own sake) rather than for value. The 0.9 cap is tight enough to bite for large-N or high-risk-aversion cases, which is intentional — those are exactly the cases where unbounded math would produce unreasonable bids.

**2. Budget cap: `budget_remaining`.** Never bid more than available budget. If this binds, the bidder is under-resourced for this auction. The skill flags the binding constraint so the caller can decide whether to skip the auction, reallocate budget, or accept a lower win probability.

**3. Floor cap: `min_bid_floor` (default 1).** When N = 1 or the raw bid would be zero, submit the minimum accepted increment. This keeps the skill useful when there is effectively no competition — a `$0` bid is often not accepted, but `$1` is.

**Order of operations:**
```
raw_bid    = true_value x shade_fraction_final
capped     = min(raw_bid, 0.9 x true_value, budget_remaining)
final_bid  = max(capped, min_bid_floor if true_value > 0 else 0)
```

---

## Worked Examples

### Example A — N = 2, uniform, risk-neutral

**Setup.** Two bidders, values uniform on `[0, 100]`. You draw `v = 80`. You are risk-neutral. Budget ample.

**Inputs.**
```json
{ "true_value": 80, "n_bidders_estimate": 2, "value_distribution": "uniform",
  "risk_aversion": 0, "budget_remaining": 500 }
```

**Compute.**
```
shade_fraction = (2 - 1) / 2 = 0.5
shaded_bid_raw = 80 x 0.5   = 40
0.9 cap        = 72   (does not bind)
budget cap     = 500  (does not bind)
final          = 40
```

**Expected outcome.** Your rival's value is uniform on `[0, 100]`. Their equilibrium bid is `v_rival / 2`. You bid 40; they bid 40 iff `v_rival = 80`. You win whenever `v_rival < 80`, i.e., with probability 0.80. Conditional on winning, your surplus is `80 - 40 = 40`. Expected surplus: `0.80 x 40 = 32`. (Equivalently, `v^N / N = 80^2 / 2 / 100 = 32` after normalization.)

**Output.**
```json
{ "shaded_bid": 40,
  "shade_fraction": 0.5,
  "rationale": "Uniform (N-1)/N shading at N=2 gives shade 0.5. No caps bind. Expected surplus ~32 units.",
  "assumptions_flagged": ["N=2 is an estimate", "uniform distribution assumed"] }
```

**Sanity check.** Shading to 50 percent feels aggressive but is exactly right for two-player first-price auctions. Bidding higher (e.g., 60) would win more often but collect less surplus per win; bidding lower (e.g., 30) would win less often with more surplus per win. The math confirms 40 maximizes the product.

---

### Example B — N = 6, uniform, mild risk aversion

**Setup.** Six bidders expected. You value the item at 100. You are mildly risk-averse (0.3) because losing this auction forces you into a worse alternative. Budget is 300 (plenty).

**Inputs.**
```json
{ "true_value": 100, "n_bidders_estimate": 6, "value_distribution": "uniform",
  "risk_aversion": 0.3, "budget_remaining": 300 }
```

**Compute.**
```
shade_base          = (6 - 1) / 6 = 0.8333
shade_risk-adjusted = 0.8333 + 0.3 x (1 - 0.8333) x 0.4
                    = 0.8333 + 0.3 x 0.1667 x 0.4
                    = 0.8333 + 0.0200
                    = 0.8533
shaded_bid_raw      = 100 x 0.8533 = 85.33
0.9 cap             = 90 (does not bind)
budget cap          = 300 (does not bind)
final               = 85.33 -> round to 85
```

**Expected outcome.** Against five symmetric rivals shading to `(N-1)/N = 0.833`, your bid of 85 beats them whenever the highest of five rival values is below the `v` that produces a rival bid of 85 — i.e., whenever max rival value < `85 / 0.833 = 102`. Since values are bounded by 100 in this normalized setup, you win with probability 1 against rivals using the risk-neutral strategy (they cannot bid above 83.3). In practice rivals will have their own risk profiles; the point is that nudging shade up by 0.02 buys a meaningful win-probability increase.

**Output.**
```json
{ "shaded_bid": 85,
  "shade_fraction": 0.8533,
  "rationale": "Uniform N=6 shade 0.833; risk aversion 0.3 raises shade to 0.853. No caps bind.",
  "assumptions_flagged": ["N=6 is an estimate",
                          "uniform distribution assumed",
                          "risk_aversion 0.3 is a modeling choice"] }
```

---

### Example C — N = 8, log-normal, budget-constrained

**Setup.** An eight-bidder auction on an item with clustered valuations (log-normal, moderate spread). Your private value is 120. Risk-neutral. But budget remaining is only 75 — below what the log-normal formula alone would produce.

**Inputs.**
```json
{ "true_value": 120, "n_bidders_estimate": 8, "value_distribution": "log-normal",
  "risk_aversion": 0, "budget_remaining": 75, "spread": 1.5 }
```

**Compute.**
```
shade_log-normal = 1 - 1 / (8 x 1.5) = 1 - 0.0833 = 0.9167
(for comparison, uniform shade at N=8 is 7/8 = 0.875; log-normal permits deeper
 shade because rivals' values cluster, making the second-highest value close to
 the highest)

shaded_bid_raw = 120 x 0.9167 = 110
0.9 cap         = 108 (binds first: raw 110 > 108)
raw_after_cap   = 108
budget cap      = 75 (binds: 108 > 75)
final           = 75
effective shade = 75 / 120 = 0.625
```

**Output.**
```json
{ "shaded_bid": 75,
  "shade_fraction": 0.625,
  "rationale": "Log-normal N=8 spread 1.5 shades to 0.917, trimmed by 0.9 x true_value cap to 108, then clamped by budget 75. Effective shade 0.625 — under-resourced for this auction.",
  "assumptions_flagged": ["N=8 is an estimate",
                          "log-normal spread 1.5 is a modeling choice",
                          "0.9 x true_value safety cap would have bound",
                          "budget cap binds — caller should consider skipping"] }
```

**Note to downstream callers.** When the budget cap binds hard (effective shade << base shade), the skill is signaling that this auction may be the wrong choice — the bidder should probably redirect budget to another auction where they are not under-resourced. The skill does not make this decision; it surfaces the signal in `assumptions_flagged` so the caller can act on it.

---

## References

- Vickrey, W. (1961). "Counterspeculation, auctions, and competitive sealed tenders." Journal of Finance 16(1).
- Krishna, V. (2009). *Auction Theory* (2nd ed.), Academic Press. Chapter 2 for the `(N-1)/N` derivation, Chapter 4 for revenue equivalence, Chapter 4.4 for risk aversion.
- Milgrom, P. (2004). *Putting Auction Theory to Work*, Cambridge University Press. For empirical-distribution calibration.
