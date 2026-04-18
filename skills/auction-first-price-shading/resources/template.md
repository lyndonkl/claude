# Auction First-Price Shading — Input/Output Contract and Worked Example

This template defines the exact contract between `auction-first-price-shading` and any upstream caller. The skill is a pure function: same inputs always produce the same outputs. Downstream consumers layer domain logic (value estimation, urgency, winner's-curse haircut) on top of this deterministic core.

## Table of Contents
- [Input Contract](#input-contract)
- [Output Contract](#output-contract)
- [Validation Rules](#validation-rules)
- [Worked Example — Fantasy Waiver Auction (FAAB)](#worked-example--fantasy-waiver-auction-faab)
- [Worked Example — Generic Sealed Procurement Bid](#worked-example--generic-sealed-procurement-bid)
- [Edge-Case Contracts](#edge-case-contracts)

---

## Input Contract

| Field | Type | Range | Default | Meaning |
|-------|------|-------|---------|---------|
| `true_value` | number | `>= 0` | required | Bidder's own private valuation of the item, in units of budget currency |
| `n_bidders_estimate` | integer | clamped to `[1, 12]` | required | Total number of realistic bidders in the auction, including self |
| `value_distribution` | string | `"uniform"` \| `"log-normal"` \| `"empirical"` | required | Assumption about the shape of rivals' value distribution |
| `risk_aversion` | number | `[0, 1]` | `0` | 0 = risk-neutral, 1 = maximally risk-averse (wants to win even at low expected surplus) |
| `budget_remaining` | number | `>= 0` | required | Remaining budget. Hard ceiling on the output. |

**Optional extended fields (if supplied, the skill uses them; otherwise defaults apply):**

| Field | Type | Default | Meaning |
|-------|------|---------|---------|
| `spread` | number | `1.5` | Coefficient-of-variation proxy for log-normal / empirical distributions. Higher = more disagreement = deeper shading allowed. |
| `min_bid_floor` | number | `1` | Minimum increment the auction accepts when there is effectively no competition (N=1). |

## Output Contract

| Field | Type | Meaning |
|-------|------|---------|
| `shaded_bid` | number | Final bid to submit, after all adjustments and caps. Rounded to the precision the caller supplies (integers by default). |
| `shade_fraction` | number in `[0, 1]` | Effective shade actually applied: `shaded_bid / true_value`. |
| `rationale` | string | One or two sentences explaining which rule applied (base uniform vs. log-normal vs. empirical), whether risk aversion moved the bid, and which cap (if any) binds. |
| `assumptions_flagged` | string[] | Every modeling assumption the caller may need to revisit — e.g., "N=6 is an estimate", "budget cap binds", "uniform-distribution assumption", "risk_aversion=0.3 modeling choice". |

## Validation Rules

Before computing, the skill enforces:

1. `true_value >= 0`. If `true_value == 0` the output is `shaded_bid = 0, shade_fraction = 0` with rationale "Zero true value — no bid warranted."
2. `n_bidders_estimate` is cast to an integer and clamped to `[1, 12]`. Values outside this range are clamped and flagged in `assumptions_flagged`.
3. `value_distribution` must be one of the three allowed strings. Any other value falls back to `"uniform"` and flags "unknown distribution — defaulted to uniform."
4. `risk_aversion` is clamped to `[0, 1]`. Values outside are clamped and flagged.
5. `budget_remaining >= 0`. If `0`, output is `shaded_bid = 0` with rationale "No budget remaining — cannot bid."

---

## Worked Example — Fantasy Waiver Auction (FAAB)

Fantasy sports waiver budgets are one real-world consumer of this skill. This example mirrors the Sasaki scenario from the FAAB framework doc, but expressed purely in domain-neutral terms. A downstream fantasy-specific skill (e.g., `mlb-faab-sizer`) computes `true_value` from projection and roster-need signals, applies a common-value winner's-curse haircut, and passes the resulting number into this skill.

**Upstream preparation (done by the domain skill, not here):**
- Raw acquisition value = 28 units.
- Positional need fit = 0.70. Role certainty = 0.65. Urgency = 1.2. Season-pace = 0.7.
- Winner's-curse haircut for common-value = 0.80.
- Effective private value passed to this skill: `28 x 0.70 x 0.65 x 1.2 x 0.7 x 0.80 = 8.56`.

**Inputs to this skill:**

```json
{
  "true_value": 8.56,
  "n_bidders_estimate": 6,
  "value_distribution": "uniform",
  "risk_aversion": 0.0,
  "budget_remaining": 89
}
```

**Computation:**

```
shade_fraction_base = (6 - 1) / 6 = 0.833
shaded_bid_raw      = 8.56 x 0.833 = 7.13

risk_aversion adjustment = 0 -> no change
shade_fraction_final = 0.833

caps:
  0.9 x true_value  = 7.70
  budget_remaining  = 89
  min of all        = 7.13

round to integer currency -> 7
```

**Output:**

```json
{
  "shaded_bid": 7,
  "shade_fraction": 0.833,
  "rationale": "Uniform-value (N-1)/N shading at N=6 gives shade 0.833; bid of 7 is below the 0.9 x true_value cap of 7.70 and far below budget. Risk-neutral; no adjustment.",
  "assumptions_flagged": [
    "N=6 is an estimate, not observed",
    "uniform private-value distribution assumed",
    "upstream common-value haircut already applied to true_value"
  ]
}
```

The downstream domain skill then reports this as "bid 7, ceiling 8, rationale: many teams will chase this target; shade because if we outbid everyone we probably overpaid."

---

## Worked Example — Generic Sealed Procurement Bid

A procurement team is soliciting one blind supply bid. The team's private valuation for securing supply is 250 units of budget currency. Three other vendors are expected to bid. Values cluster around a shared estimate (log-normal with moderate spread). The team is mildly risk-averse (supply security matters) at 0.3. Budget remaining is 500 units.

**Inputs:**

```json
{
  "true_value": 250,
  "n_bidders_estimate": 4,
  "value_distribution": "log-normal",
  "risk_aversion": 0.3,
  "budget_remaining": 500,
  "spread": 1.5
}
```

**Computation:**

```
log-normal shade = 1 - 1/(N x spread) = 1 - 1/(4 x 1.5) = 1 - 0.167 = 0.833
(compare to uniform shade: (4-1)/4 = 0.75; log-normal permits deeper shade here
 because clustered values reduce the marginal benefit of bidding aggressively)

risk_aversion adjustment:
  shade' = 0.833 + 0.3 x (1 - 0.833) x 0.4
         = 0.833 + 0.3 x 0.167 x 0.4
         = 0.833 + 0.020
         = 0.853

shaded_bid_raw = 250 x 0.853 = 213.3

caps:
  0.9 x true_value = 225
  budget_remaining = 500
  min of raw, caps = 213.3

round to integer currency -> 213
```

**Output:**

```json
{
  "shaded_bid": 213,
  "shade_fraction": 0.853,
  "rationale": "Log-normal values at N=4 with spread 1.5 shade to 0.833; risk aversion 0.3 nudges shade to 0.853. Final bid 213 sits below the 0.9 x true_value cap of 225 and well under budget.",
  "assumptions_flagged": [
    "N=4 is an estimate",
    "log-normal spread 1.5 is a modeling choice",
    "risk_aversion 0.3 reflects stated supply-security preference",
    "symmetric bidders assumed — all rivals use the same bid function"
  ]
}
```

---

## Edge-Case Contracts

**Edge case: `N = 1` — no competition**

```json
Inputs:  { "true_value": 50, "n_bidders_estimate": 1, "value_distribution": "uniform",
           "risk_aversion": 0, "budget_remaining": 100 }

Output:  { "shaded_bid": 1,
           "shade_fraction": 0.02,
           "rationale": "N=1: no realistic competition. Bid the minimum increment (1 unit).",
           "assumptions_flagged": ["min_bid_floor defaulted to 1"] }
```

**Edge case: budget cap binds**

```json
Inputs:  { "true_value": 100, "n_bidders_estimate": 8, "value_distribution": "uniform",
           "risk_aversion": 0.5, "budget_remaining": 50 }

Raw shade: 0.875, risk-adjusted to 0.925 — exceeds 0.9 cap, clamped to 0.9.
Raw bid:   90. Budget cap: 50. Final: 50.

Output:  { "shaded_bid": 50,
           "shade_fraction": 0.5,
           "rationale": "Uniform shade 0.875 at N=8 with risk aversion 0.5 would bid 90, but budget cap of 50 binds. Effective shade 0.5.",
           "assumptions_flagged": ["budget cap binds — under-resourced for this target",
                                   "0.9 x true_value safety cap also triggered before budget cap"] }
```

**Edge case: `N = 12` — many competitors**

```json
Inputs:  { "true_value": 100, "n_bidders_estimate": 12, "value_distribution": "uniform",
           "risk_aversion": 0, "budget_remaining": 500 }

Raw shade: 11/12 = 0.917. Raw bid: 91.7 -> caps at 0.9 x 100 = 90.

Output:  { "shaded_bid": 90,
           "shade_fraction": 0.90,
           "rationale": "Uniform shade at N=12 is 0.917, but 0.9 x true_value safety cap binds. Final bid 90.",
           "assumptions_flagged": ["N=12 upper clamp applied (input may have been higher)",
                                   "0.9 x true_value safety cap binds"] }
```
