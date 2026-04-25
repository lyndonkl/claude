---
name: recurring-charge-detector
description: Identifies recurring charges (subscriptions, monthly bills, biweekly paychecks) from a transaction history by clustering same-merchant transactions of similar amount on a regular cadence, requiring at least 3 confirming occurrences before promoting a candidate to active status. Detects new recurring charges, dormant subscriptions (missed expected dates), and amount drift, and computes annualized cost. Use when auditing subscriptions, building a recurring bills calendar, computing cash-flow forecast inputs, or when user mentions subscription audit, recurring detection, dormant subscription, or annualized cost.
---

# Recurring Charge Detector

## Table of Contents
- [Overview](#overview)
- [Input contract](#input-contract)
- [Cadences](#cadences)
- [Workflow](#workflow)
- [Status transitions](#status-transitions)
- [Output contract](#output-contract)
- [Guardrails](#guardrails)

## Overview

A subscription audit is mostly the same question asked many ways: which charges arrive on a clock? This skill clusters historical transactions by merchant + cadence + typical amount, requires ≥ 3 confirming occurrences before promotion, and tracks each cluster's lifecycle (active → suspected_dormant → cancelled).

It computes **annualized cost** for each active recurring entry — the single most useful number in a subscription audit ("you are spending $191 a year on Netflix").

## Input contract

The caller provides:

- `transactions` — array with `{id, account_id, date, merchant, amount_cents, category, subcategory}`.
- `existing_recurring` — current `recurring.json` state.
- `lookback_days` (default 540, ~18 months) — only transactions within this window are clustered.
- `today` — ISO date for status calculations.

## Cadences

| Cadence | Interval (days) | Tolerance |
|---|---|---|
| `weekly` | 7 | ±2 |
| `biweekly` | 14 | ±3 |
| `monthly` | 30 | ±4 |
| `quarterly` | 91 | ±10 |
| `semiannual` | 182 | ±14 |
| `annual` | 365 | ±21 |

If the inter-arrival times don't fit any of the above with the listed tolerance, mark `cadence: "irregular"` and do not promote.

## Workflow

```
Recurring Detection Progress:
- [ ] Step 1: Group transactions by (merchant, account_id)
- [ ] Step 2: For each group with >= 3 transactions, sort by date
- [ ] Step 3: Compute inter-arrival deltas; classify cadence
- [ ] Step 4: Check amount stability (±10% or fixed)
- [ ] Step 5: Promote to active if cadence + amount + occurrences pass
- [ ] Step 6: Compute next_expected_date and annualized cost
- [ ] Step 7: Diff against existing_recurring; emit transitions
- [ ] Step 8: Detect dormant (missed expected date by > tolerance)
```

### Step 1 — Group

Group by `(merchant, account_id)`. Subscriptions can split across accounts; treat each account as its own series. (One Netflix charge that moved from credit card A to credit card B will appear as two clusters; the agent layer reconciles them.)

### Step 2 — Sort and threshold

Drop groups with < 3 transactions. They cannot be promoted yet — surface them as `candidates[]` with `evidence_count` so the user knows what's accumulating.

### Step 3 — Cadence classification

Compute deltas `d_i = date[i+1] - date[i]` in days. Classify cadence using the table above. Acceptance rule:

- ≥ 80% of deltas fall within the cadence's tolerance band.
- Allow up to one large delta (`> 2× nominal`) only if it's followed by re-anchoring at the original cadence — this is normal for "skipped a month" patterns.

If multiple cadences are plausible, pick the one with tighter fit (smallest standard deviation of deltas).

### Step 4 — Amount stability

Compute mean amount `μ` and standard deviation `σ` of the cluster's amounts.

- `σ / |μ|` ≤ 0.05 → "fixed" (e.g., Netflix $15.99 every month).
- `σ / |μ|` ≤ 0.20 → "variable_low" (utilities, where amount drifts seasonally).
- `σ / |μ|` ≤ 0.40 → "variable_high" (e.g., grocery delivery — flag but allow).
- `σ / |μ|` > 0.40 → reject as recurring (probably a misclustered general merchant).

Record `amount_cents_typical = round(μ)` and `amount_cents_variance = round(σ)`.

### Step 5 — Promotion

Promote to `status: "active"` if:
- `occurrences ≥ 3`.
- `cadence` is one of the named cadences (not `irregular`).
- amount stability is `fixed` or `variable_low` (or `variable_high` with a warning).

### Step 6 — Forward projection

`next_expected_date = last_seen + cadence_interval`. Update with each new occurrence.

`annualized_cost_cents`:

| Cadence | Multiplier |
|---|---|
| weekly | 52 |
| biweekly | 26 |
| monthly | 12 |
| quarterly | 4 |
| semiannual | 2 |
| annual | 1 |

`annualized_cost_cents = amount_cents_typical × multiplier`. For inflows (paychecks), this is annualized income; for outflows, annualized cost.

### Step 7 — Diff against existing

For each existing `recurring.json` entry, find the matching new cluster (by `merchant` + `account_id` + cadence). Update fields:
- `last_seen`, `occurrences`, `amount_cents_typical`, `next_expected_date`.
- If amount drifts > 15% from prior `amount_cents_typical` → emit `event: "amount_changed"` with old and new.

For new clusters not in existing → emit `event: "new_recurring"`.

### Step 8 — Dormant detection

For each active entry where `today > next_expected_date + tolerance` and no matching transaction exists in the window:
- First miss → `status: "suspected_dormant"`, `event: "missed_expected"`.
- Two consecutive misses → propose `status: "cancelled"` with `event: "likely_cancelled"`.

The agent layer confirms before flipping to `cancelled`.

## Status transitions

```
candidate (< 3 occurrences)
   ↓ [3rd occurrence on cadence]
active
   ↓ [missed expected date]                 ↓ [user confirms]
suspected_dormant ─ [resumed] → active     paused
   ↓ [missed twice in a row]
likely_cancelled
   ↓ [user confirms]
cancelled
```

## Output contract

```json
{
  "active": [
    {
      "id": "rec_netflix",
      "merchant": "Netflix",
      "account_id": "acc_cc_001",
      "category": "entertainment.streaming",
      "amount_cents_typical": 1599,
      "amount_cents_variance": 0,
      "cadence": "monthly",
      "first_seen": "2024-03-14",
      "last_seen": "2026-01-14",
      "occurrences": 23,
      "next_expected_date": "2026-02-14",
      "annualized_cost_cents": 19188,
      "status": "active"
    }
  ],
  "candidates": [
    {
      "merchant": "Blue Bottle Coffee",
      "account_id": "acc_cc_001",
      "evidence_count": 2,
      "needed": 3,
      "reason": "below promotion threshold"
    }
  ],
  "events": [
    { "type": "new_recurring", "id": "rec_chatgpt", "evidence_count": 3 },
    { "type": "amount_changed", "id": "rec_netflix",
      "old_cents": 1499, "new_cents": 1599, "delta_pct": 6.7 },
    { "type": "missed_expected", "id": "rec_amazon_prime",
      "expected_date": "2026-01-10", "today": "2026-01-20",
      "suggested_status": "suspected_dormant" }
  ],
  "summary": {
    "active_count": 27,
    "annualized_cost_total_cents": 487200,
    "candidates": 4,
    "dormant": 1
  }
}
```

## Guardrails

- **Three is the minimum.** Two same-merchant charges a month apart are not enough — the second could be a one-off subscription trial.
- **Cluster by merchant, not by description.** Use the `merchant` field from the categorizer, not `description_raw`. Different rendering of the same merchant string would otherwise split a real recurring into two phantom ones.
- **Inflows count too.** Paychecks are recurring `income.salary`; track them. The cash-flow forecaster needs both sides.
- **Variable utilities.** Allow `variable_low` for utilities. Do not propagate variance noise into the forecaster — use `amount_cents_typical` (the mean).
- **Tax-loss-harvesting / rebalancing trades** can superficially look recurring (same security, regular pattern). Treat brokerage account transactions with `category: savings_investment.*` as exempt from recurring promotion unless the cadence is annual or longer.
- **Dormant ≠ cancelled.** Surface dormant; let the user confirm cancellation. Some merchants skip a month legitimately.
