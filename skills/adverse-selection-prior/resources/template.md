# Adverse Selection Prior -- Templates and Decision Tree

## Table of Contents
- [Input Contract Template](#input-contract-template)
- [Output Contract Template](#output-contract-template)
- [Base Prior by Offer Type](#base-prior-by-offer-type)
- [Decision Tree](#decision-tree)
- [Worked Example 1: Dormant Manager Trade Offer](#worked-example-1-dormant-manager-trade-offer)
- [Worked Example 2: Expert Trader Offer](#worked-example-2-expert-trader-offer)
- [Worked Example 3: Frustrated Loser Panic-Offer](#worked-example-3-frustrated-loser-panic-offer)
- [Prior-to-Adjustment Mapping](#prior-to-adjustment-mapping)
- [Output Assembly Template](#output-assembly-template)

---

## Input Contract Template

```yaml
offer_type: trade | waiver_claim_dropped_by_other | free_agent_pickup_available | counter_offer | generic
proposer_archetype: active | dormant | frustrated | expert | unknown
offer_symmetry_score: int  # 0-100. Surface fairness from our own valuation
proposer_info_asymmetry: int  # 0-100. Information gap they plausibly have over us
```

## Output Contract Template

```yaml
prior_ev_probability: float  # 0-1, baseline < 0.5 for received offers
recommended_adjustment: float  # multiplicative factor in [0.75, 1.00]
bayesian_rationale: string  # 2-4 sentences
override_hints: [string]  # 2-5 conditional statements
```

---

## Base Prior by Offer Type

| `offer_type` | Base prior | Selection strength | Why |
|--------------|------------|---------------------|-----|
| `trade` | 0.40 | Strong | They wrote the specific offer and sent it to you from among all possible offers they could have constructed |
| `waiver_claim_dropped_by_other` | 0.42 | Moderate | They chose to drop the player, but not specifically to transfer it to you -- the selection is weaker than a targeted trade |
| `free_agent_pickup_available` | 0.48 | Weak | The player is unclaimed by anyone. This may reflect genuine consensus-poor quality, or it may reflect no one noticing. Selection pressure is diffuse |
| `counter_offer` | 0.38 | Very strong | They rejected your first offer and replaced it with this one -- the selection is tighter because they have already filtered out your original proposal |
| `generic` | 0.40 | Default | Unknown context |

---

## Decision Tree

```
START
  |
  v
[Step 1] What is offer_type?
  |-- trade -> base_prior = 0.40
  |-- counter_offer -> base_prior = 0.38
  |-- waiver_claim_dropped_by_other -> base_prior = 0.42
  |-- free_agent_pickup_available -> base_prior = 0.48
  |-- generic -> base_prior = 0.40
  |
  v
[Step 2] What is proposer_archetype?
  |-- expert -> archetype_delta = -0.08
  |-- active -> archetype_delta = -0.05
  |-- frustrated -> archetype_delta =  0.00 (FLAG: need sub-signal -- see Step 2a)
  |-- dormant -> archetype_delta = +0.08
  |-- unknown -> archetype_delta =  0.00
  |
  v
[Step 2a] (IF frustrated) Triangulate panic vs scheme
  |-- Panic confirmed (2+ signals: losses + tone + tilt-trades + complaints)
  |     -> override archetype_delta to +0.05 (treat as semi-dormant)
  |-- Scheme suspected (offer looks TOO fair + no public frustration signal)
  |     -> override archetype_delta to -0.05 (treat as semi-active)
  |-- Ambiguous -> leave at 0.00 and note in override_hints
  |
  v
[Step 3] offer_symmetry_score?
  |-- >= 85 -> symmetry_delta = +0.10
  |-- 70-84 -> symmetry_delta = +0.05 to +0.07 (linear)
  |-- 30-69 -> symmetry_delta = 0.00
  |-- < 30  -> symmetry_delta = 0.00 AND flag "too good to be true"
  |
  v
[Step 4] proposer_info_asymmetry?
  |-- >= 80 -> asymmetry_delta = -0.15 to -0.20
  |-- 60-79 -> asymmetry_delta = -0.10 to -0.15
  |-- 30-59 -> asymmetry_delta = -0.03 to -0.05
  |-- < 30  -> asymmetry_delta = 0.00
  |
  v
[Step 5] Combine and clip
  prior = base_prior + archetype_delta + symmetry_delta + asymmetry_delta
  prior = clip(prior, 0.10, 0.70)
  |
  v
[Step 6] Map to recommended_adjustment
  |-- prior >= 0.50 -> adjustment = 1.00
  |-- 0.45-0.49     -> adjustment = 0.95
  |-- 0.40-0.44     -> adjustment = 0.90
  |-- 0.35-0.39     -> adjustment = 0.85
  |-- 0.30-0.34     -> adjustment = 0.80
  |-- prior < 0.30  -> adjustment = 0.75
  |
  v
[Step 7] Write rationale + override hints
END
```

---

## Worked Example 1: Dormant Manager Trade Offer

### Scenario
A fantasy-baseball opponent who has made only 2 waiver moves all season offers you a trade: their All-Star closer for two of your mid-tier starters. Our own projection says the deal is +8% EV for us (we need SV; we are deep in QS).

### Inputs
```yaml
offer_type: trade
proposer_archetype: dormant
offer_symmetry_score: 78
proposer_info_asymmetry: 20
```

### Walkthrough
- **Step 1**: `trade` -> `base_prior = 0.40`
- **Step 2**: `dormant` -> `archetype_delta = +0.08`
- **Step 3**: symmetry 78 is in the 70-84 band -> `symmetry_delta = +0.06`
- **Step 4**: asymmetry 20 is below 30 -> `asymmetry_delta = 0.00`
- **Step 5**: `prior = 0.40 + 0.08 + 0.06 + 0.00 = 0.54`; clip to [0.10, 0.70] -> **0.54**
- **Step 6**: prior >= 0.50 -> `recommended_adjustment = 1.00`
- **Step 7**: Rationale + hints below

### Output
```json
{
  "prior_ev_probability": 0.54,
  "recommended_adjustment": 1.00,
  "bayesian_rationale": "Dormant manager archetype weakens the adverse-selection signal -- they may be clicking without deep analysis. Combined with high surface symmetry (78) and negligible info asymmetry (20), the prior rises above neutral to 0.54. No haircut recommended; our own +8% EV estimate stands.",
  "override_hints": [
    "If recent roster activity shows dormant manager has started analyzing (3+ moves in past week), re-classify to active; prior drops to ~0.46.",
    "If the closer has been pulled from ninth-inning role this week and we missed it, re-run with asymmetry=85; prior drops to ~0.34.",
    "If this is the third trade they have offered us this month, selection pressure is higher than dormant implies -- re-run with archetype=unknown; prior drops to ~0.46."
  ]
}
```

### Interpretation
This is the rare case where the adverse-selection prior crosses 0.50. Dormant managers do not select their offers as carefully, so the market-for-lemons insight weakens. The trade is accept-candidate on our own +8% EV with zero haircut -- but the override hints preserve the ability to re-run if new information surfaces.

---

## Worked Example 2: Expert Trader Offer

### Scenario
A known sharp in the league (top-decile FAAB efficiency, 3 profitable trades already this season) offers you their 35-HR outfielder for your 25-HR outfielder plus a mid-tier SP. Our own projection says the deal is +2% EV for us. The 35-HR OF had a hamstring tweak reported 36 hours ago that we have not yet priced in.

### Inputs
```yaml
offer_type: trade
proposer_archetype: expert
offer_symmetry_score: 80
proposer_info_asymmetry: 75
```

### Walkthrough
- **Step 1**: `trade` -> `base_prior = 0.40`
- **Step 2**: `expert` -> `archetype_delta = -0.08`
- **Step 3**: symmetry 80 is in 70-84 band -> `symmetry_delta = +0.06`
- **Step 4**: asymmetry 75 is in 60-79 band -> `asymmetry_delta = -0.13`
- **Step 5**: `prior = 0.40 - 0.08 + 0.06 - 0.13 = 0.25`; clip to [0.10, 0.70] -> **0.25**
- **Step 6**: prior < 0.30 -> `recommended_adjustment = 0.75`
- **Step 7**: Rationale + hints below

### Output
```json
{
  "prior_ev_probability": 0.25,
  "recommended_adjustment": 0.75,
  "bayesian_rationale": "Expert archetype applies strongest selection pressure -- they had many possible offers and chose this specific one. Surface symmetry (80) partially offsets, but the hamstring injury (asymmetry=75) dominates. Prior of 0.25 triggers a 25% EV haircut. Our +2% becomes -23.5% after haircut (1.02 x 0.75 = 0.765) -- strong reject/counter signal.",
  "override_hints": [
    "If hamstring is confirmed minor (<5 days expected miss), asymmetry drops to 40; re-run, prior rises to ~0.37.",
    "If expert has been on a cold streak (rare for this archetype), partial-panic override may apply; re-run with archetype=frustrated and panic confirmed, prior rises to ~0.38.",
    "If we are specifically short on HR and long on SP (category plan-dependent), raw EV calculation may not capture the positional-fit premium; upstream valuation should recompute before applying this prior."
  ]
}
```

### Interpretation
The combination of expert archetype + fresh injury news is the canonical adverse-selection disaster. Our own model shows +2%, but after the 25% haircut we land at -23.5% EV. Reject or counter with a package that removes the injured player from the equation. This is exactly what the "seems fair = probably bad" heuristic is designed to catch.

---

## Worked Example 3: Frustrated Loser Panic-Offer

### Scenario
A team at 1-8 in the standings sends you a trade: their top-10 pitcher for two of your mid-tier bats. Recent signs: they made 5 waiver claims this week (up from their usual 1), they posted "this league is rigged" in chat two days ago, and they dropped a former 3rd-round pick earlier today. Our own projection says the deal is +18% EV for us.

### Inputs (initial)
```yaml
offer_type: trade
proposer_archetype: frustrated
offer_symmetry_score: 35
proposer_info_asymmetry: 25
```

### Step 2a: Triangulate panic vs scheme
Panic signals present:
1. Recent heavy losses (1-8 record): YES
2. Message tone (frustrated chat post): YES
3. Visible tilt-trades (5 waiver claims in a week + dropping a former pick): YES
4. Public complaint: YES

**Four panic signals -> panic confirmed**. Override `archetype_delta` to **+0.05** (treat as semi-dormant).

### Walkthrough
- **Step 1**: `trade` -> `base_prior = 0.40`
- **Step 2**: `frustrated` -> initially 0.00; after 2a override -> `archetype_delta = +0.05`
- **Step 3**: symmetry 35 is in 30-69 band -> `symmetry_delta = 0.00`
- **Step 4**: asymmetry 25 is below 30 -> `asymmetry_delta = 0.00`
- **Step 5**: `prior = 0.40 + 0.05 + 0.00 + 0.00 = 0.45`; clip to [0.10, 0.70] -> **0.45**
- **Step 6**: prior in 0.45-0.49 -> `recommended_adjustment = 0.95`
- **Step 7**: Rationale + hints below

### Output
```json
{
  "prior_ev_probability": 0.45,
  "recommended_adjustment": 0.95,
  "bayesian_rationale": "Frustrated archetype with four confirmed panic signals (losing record, frustrated chat, tilt-trades, dropped former pick) triggers the semi-dormant override. Low surface symmetry (35) is consistent with panic -- they are not optimizing, they are dumping. Prior lands at 0.45 with only a 5% haircut. Our +18% EV becomes +17.1% after haircut (1.18 x 0.95) -- strong accept signal.",
  "override_hints": [
    "If any panic signal turns out to be fabricated (e.g., the chat post was sarcasm), re-run with archetype=frustrated and ambiguous; prior drops to ~0.40.",
    "If we discover the 'top-10 pitcher' has a hidden issue (IL trip, role loss, suspension) in next 48h, re-run with asymmetry=75; prior drops to ~0.30.",
    "If we have a cooperation history with this counterparty showing prior non-panic frustration-dumps that turned out to be +EV for recipient, adjust base_prior up by +0.03."
  ]
}
```

### Interpretation
Panic-sells are the rare +EV-for-recipient case in adverse selection. The counterparty is not optimizing, so the selection pressure that normally makes offered deals bad for us weakens. The skill reduces the haircut to 5%, preserving most of our +18% edge. The override hints remain vigilant against scheming-disguised-as-frustration.

---

## Prior-to-Adjustment Mapping

Used in Step 6.

| Prior range | `recommended_adjustment` | Interpretation | Typical action (downstream) |
|-------------|--------------------------|----------------|-----------------------------|
| 0.50+ | 1.00 | No haircut | Accept if own EV > threshold |
| 0.45-0.49 | 0.95 | Light haircut | Accept if own EV > 1.05x threshold |
| 0.40-0.44 | 0.90 | Standard haircut | Accept if own EV > 1.11x threshold |
| 0.35-0.39 | 0.85 | Moderate haircut | Counter; rarely accept |
| 0.30-0.34 | 0.80 | Deep haircut | Counter or reject |
| <= 0.29 | 0.75 | Predatory suspicion | Default to reject |

---

## Output Assembly Template

```python
def emit_prior(base_prior, archetype_delta, symmetry_delta, asymmetry_delta,
               rationale, overrides):
    prior = base_prior + archetype_delta + symmetry_delta + asymmetry_delta
    prior = max(0.10, min(0.70, prior))  # clip

    if prior >= 0.50:
        adj = 1.00
    elif prior >= 0.45:
        adj = 0.95
    elif prior >= 0.40:
        adj = 0.90
    elif prior >= 0.35:
        adj = 0.85
    elif prior >= 0.30:
        adj = 0.80
    else:
        adj = 0.75

    return {
        "prior_ev_probability": round(prior, 2),
        "recommended_adjustment": adj,
        "bayesian_rationale": rationale,
        "override_hints": overrides,
    }
```

The function enforces the clip and the monotone prior-to-adjustment mapping. Downstream consumers should call `adjusted_EV = own_EV * recommended_adjustment` before applying their accept/counter/reject ladder.
