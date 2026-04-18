# Auction Winner's-Curse Haircut Templates

Classification decision tree, worked examples, and input/output templates for the `auction-winners-curse-haircut` skill.

## Table of Contents
- [Value-Type Decision Tree](#value-type-decision-tree)
- [Worked Examples](#worked-examples)
- [Input Template](#input-template)
- [Output Template](#output-template)
- [Classification Worksheet](#classification-worksheet)

---

## Value-Type Decision Tree

Use this tree before calling the skill. The `value_type` choice is the single most important input -- it switches the short-circuit on or off and drives the entire haircut magnitude.

```
                           START
                             |
                             v
          Q1. Would other informed bidders,
              given the same public info,
              arrive at a similar valuation?
                   /                  \
                 YES                  NO
                  |                    |
                  v                    v
      Q2. Does this bidder       Q3. Is the private
          have a meaningful         component large
          private-value increment   enough to dominate
          on top of that shared     any shared-value
          value?                    base?
            /         \               /         \
          NO          YES           YES         NO
           |           |             |           |
           v           v             v           v
      COMMON_VALUE   MIXED      PRIVATE_VALUE  MIXED
                                            (lean common)
```

**Question 1 -- Shared informational basis**: If you dropped this target into any other informed bidder's analysis, would their number be close to yours? "Close" roughly means within ~20% for a common-value target; wider spreads suggest private value or poor information.

**Question 2 -- Private increment on top of common core**: Does some structural feature (positional fit, complementarity, unique use-case) raise the target's value for this bidder specifically -- in a way other bidders would not replicate? If yes, and that increment is non-trivial but not dominant, the target is `mixed`.

**Question 3 -- Private-value dominance**: If the private component is so large that the shared-information base is a minor footnote (handcuff with near-zero value to anyone else), classify as `private_value` and apply zero haircut.

**Fallback rule**: When in doubt between `common_value` and `mixed`, choose `common_value` (more conservative -- larger haircut). When in doubt between `private_value` and `mixed`, choose `mixed` (also more conservative -- keeps a partial haircut).

---

## Worked Examples

### Example 1 -- Closer on waivers (COMMON_VALUE)

**Context**: A named closer has just lost his role; the replacement closer is on the waiver wire. Every serious bidder in the league has seen the box score and read the same beat-writer tweets.

**Classification walk-through**:
- Q1: Would other informed bidders arrive at a similar valuation? **YES** -- saves projections, ratios, role certainty are public.
- Q2: Does this bidder have a private-value increment? **NO** -- no unique complementarity; saves are a common league scoring category.
- Result: **COMMON_VALUE**

**Inputs**:
- `raw_valuation`: 25
- `value_type`: `common_value`
- `n_informed_bidders`: 6
- `signal_dispersion`: 30

**Computation**:
```
haircut_pct = min(35, 10 + log(6) x 5 + 30 x 0.2)
            = min(35, 10 + 8.96 + 6)
            = 24.96
adjusted_valuation = 25 x (1 - 0.2496) = 18.76
```

**Output**:
- `adjusted_valuation`: 18.76
- `haircut_pct`: 24.96
- `classification_rationale`: "Common-value target (named closer, public info); 6 informed bidders with moderate estimate dispersion implies strong adverse-selection on winning."
- `applied`: true

---

### Example 2 -- Handcuff reliever (PRIVATE_VALUE)

**Context**: The backup to a closer you already own. No other manager in the league owns that closer, so no one else gets the same complementary value from rostering the handcuff. Two other managers might bid $1 as pure speculation.

**Classification walk-through**:
- Q1: Would other informed bidders arrive at a similar valuation? **NO** -- they do not own the starter, so the handcuff's insurance value is structurally absent for them.
- Q3: Is the private component dominant? **YES** -- the entire rationale for rostering this player is the complementarity.
- Result: **PRIVATE_VALUE**

**Inputs**:
- `raw_valuation`: 5
- `value_type`: `private_value`
- `n_informed_bidders`: 2
- `signal_dispersion`: 60 (doesn't matter -- short-circuited)

**Computation**:
```
(short-circuit)
haircut_pct = 0
adjusted_valuation = 5 x (1 - 0) = 5
```

**Output**:
- `adjusted_valuation`: 5.00
- `haircut_pct`: 0
- `classification_rationale`: "Private-value handcuff; winning this auction is not adverse because competing bidders do not share the complementarity and are not valuing the same object."
- `applied`: false

---

### Example 3 -- Late-season hot hitter (MIXED)

**Context**: Mid-August. A previously-rostered hitter was dropped; now hitting .330/.400/.550 over 14 days. Public projection systems all agree on a reasonable rest-of-season value (common base). But the bidder is punting SB and badly needs HR/RBI in this week's matchup -- category fit is the private increment.

**Classification walk-through**:
- Q1: Would other informed bidders arrive at a similar valuation of base value? **YES** -- rest-of-season projections converge.
- Q2: Private increment? **YES** -- category-need fit is structurally higher for this bidder's specific matchup state.
- Q3: Is the private component dominant? **NO** -- the base projection is still most of the value.
- Result: **MIXED**, leaning common (mix_common_weight = 0.7)

**Inputs**:
- `raw_valuation`: 18
- `value_type`: `mixed`
- `n_informed_bidders`: 4
- `signal_dispersion`: 25
- `mix_common_weight`: 0.7

**Computation**:
```
common_haircut = min(35, 10 + log(4) x 5 + 25 x 0.2)
              = min(35, 10 + 6.93 + 5)
              = 21.93
haircut_pct   = 0.7 x 21.93 = 15.35
adjusted_valuation = 18 x (1 - 0.1535) = 15.24
```

**Output**:
- `adjusted_valuation`: 15.24
- `haircut_pct`: 15.35
- `classification_rationale`: "Mixed value: public projections converge (common core, 70% weight) but category-need fit gives this bidder a private increment (30% weight); adverse-selection applies only to the common portion."
- `applied`: true

---

### Example 4 -- Cross-domain: prediction-market contract (COMMON_VALUE)

**Context**: A prediction market contract on a well-covered political event. Thousands of traders have the same public information set; this bidder is one of many informed participants.

**Inputs**:
- `raw_valuation`: 0.62 (probability)
- `value_type`: `common_value`
- `n_informed_bidders`: 12 (effective informed counterparties)
- `signal_dispersion`: 15 (thin market dispersion; public polls aligned)

**Computation**:
```
haircut_pct = min(35, 10 + log(12) x 5 + 15 x 0.2)
            = min(35, 10 + 12.42 + 3)
            = 25.42
adjusted_valuation = 0.62 x (1 - 0.2542) = 0.4624
```

Note: in prediction-market usage, the "valuation" is a probability estimate that would translate to a fair price. The caller interprets the adjusted value as a post-haircut fair price before applying any separate bid-shading step.

---

### Example 5 -- Cross-domain: M&A target with thick field (COMMON_VALUE, many bidders)

**Context**: Competitive M&A auction for a publicly traded target. Six strategic acquirers plus three financial sponsors have signed NDAs.

**Inputs**:
- `raw_valuation`: 4200 ($M)
- `value_type`: `common_value`
- `n_informed_bidders`: 9
- `signal_dispersion`: 35

**Computation**:
```
haircut_pct = min(35, 10 + log(9) x 5 + 35 x 0.2)
            = min(35, 10 + 10.99 + 7)
            = 27.99
adjusted_valuation = 4200 x (1 - 0.2799) = 3024.42
```

Interpretation: if the bidder's model says the target is worth $4.2B, paying above ~$3.0B in a competitive auction is probability-weighted evidence of over-estimation, before any separate strategic shading.

---

## Input Template

```
{
  "raw_valuation": <number, >= 0>,
  "value_type": "common_value" | "private_value" | "mixed",
  "n_informed_bidders": <int, >= 1>,
  "signal_dispersion": <number in [0, 100]>,
  "mix_common_weight": <number in [0, 1], only if mixed; default 0.6>
}
```

**Field notes:**

- `raw_valuation`: Units are the caller's -- dollars, FAAB, probability, cents-per-click, share count. The skill is unit-agnostic.
- `value_type`: Required string. Must match exactly one of three enum values. See decision tree.
- `n_informed_bidders`: Informed competitors, not total auction participants. An uninformed bidder who bids randomly does not contribute to adverse selection.
- `signal_dispersion`: 0 = all informed bidders have identical estimates; 100 = estimates span a very wide range. Use 25-50 as a reasonable default when uncertain.

---

## Output Template

```
{
  "adjusted_valuation": <number, in [0, raw_valuation]>,
  "haircut_pct": <number, in [0, 40]>,
  "classification_rationale": "<one-sentence justification>",
  "applied": <bool, false iff private-value>
}
```

**Rationale format**: The `classification_rationale` should name the chosen `value_type`, the key driver (N or dispersion or private-value assertion), and the Bayesian intuition in one sentence. Example: "Common-value target with N=6 informed bidders and moderate dispersion; winning is evidence of over-estimation."

---

## Classification Worksheet

Copy and fill in before calling the skill:

```
Target description:     __________________________________________
Raw valuation:          __________ (units: __________)

Q1. Would other informed bidders arrive at a similar valuation?
    [ ] Yes - shared information basis
    [ ] No  - structurally different value for this bidder

Q2. (If Q1 yes) Is there a meaningful private increment?
    [ ] No   -> COMMON_VALUE
    [ ] Yes  -> MIXED

Q3. (If Q1 no) Does the private component dominate?
    [ ] Yes  -> PRIVATE_VALUE
    [ ] No   -> MIXED

Chosen value_type:          __________
If mixed, mix_common_weight: __________
Justification:              __________________________________________

N_informed_bidders:         __________
  Basis: ____________________________________________________________

Signal dispersion (0-100):  __________
  Basis: ____________________________________________________________
```
