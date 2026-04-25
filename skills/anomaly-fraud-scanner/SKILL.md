---
name: anomaly-fraud-scanner
description: Scans transactions for fraud and anomaly signals — duplicate charges within 48 hours, transactions more than 3 standard deviations above a merchant's historical average, first-ever transaction with a new merchant above a high-dollar threshold, and unusual geography or time. Produces severity-tagged alerts with the transaction id, evidence, and a recommended action (call bank, freeze card, dispute, monitor). Use for vigilance scans on every drop, after any large unexplained outflow, or when user mentions fraud check, suspicious charge, anomaly detection, or duplicate charge.
---

# Anomaly Fraud Scanner

## Table of Contents
- [Overview](#overview)
- [Input contract](#input-contract)
- [Detection rules](#detection-rules)
- [Workflow](#workflow)
- [Output contract](#output-contract)
- [Guardrails](#guardrails)

## Overview

Fraud detection on a household budget is a different problem from fraud detection at a bank. The bank already runs sophisticated rules; this skill exists to catch what the bank misses — small recurring fraud below their threshold, unfamiliar merchant patterns, and post-hoc audit of charges the user has not yet noticed.

It runs five complementary detectors, each producing severity-tagged alerts.

## Input contract

The caller provides:

- `transactions_new` — transactions added by the most recent drop.
- `transactions_history` — last 12 months of confirmed transactions.
- `accounts` — for context (account type, owner, geography).
- `today` — ISO date.
- `thresholds` — optional overrides:
  ```
  {
    "duplicate_window_hours": 48,
    "anomaly_sigma": 3.0,
    "first_merchant_high_dollar_cents": 50000,
    "geo_radius_miles": 1000
  }
  ```

## Detection rules

### Rule 1 — Duplicate within 48 hours

Two transactions on the same `account_id` with the same `merchant` and the same `amount_cents` posted within `duplicate_window_hours` of each other.

- Severity: `medium` for amounts < $200, `high` for amounts ≥ $200.
- Common false positives: two coffees in a day, two gas-station fill-ups during a road trip — exclude `food.coffee`, `food.restaurants`, `transportation.gas` from this rule when amount is below $30.

### Rule 2 — Statistical anomaly

For each `(merchant, account_id)` pair with ≥ 6 historical occurrences, compute mean and stddev. Flag any new transaction where `|amount − mean| > anomaly_sigma × stddev` AND `|amount − mean| ≥ $50`.

- Severity: `medium` baseline, `high` if `> 5σ` or amount > 4× mean.
- Common false positives: tip variations on restaurants, surge pricing on rideshare — bake a 25% leniency on `food.restaurants` and `transportation.rideshare`.

### Rule 3 — First merchant high dollar

A transaction with a merchant that has zero prior occurrences in `transactions_history` AND `|amount| ≥ first_merchant_high_dollar_cents`.

- Severity: `medium` for $500–$2,000, `high` for ≥ $2,000.
- Common false positives: a planned major purchase (appliance, travel booking). Suppress when a recent `category_override` or user-confirmed plan exists.

### Rule 4 — Geography or time anomaly

If `description_raw` includes a location string (state code, country code) and the inferred location differs by more than `geo_radius_miles` from the household's home location AND no travel context is set, flag.

If a transaction posts at an unusual time (between 2am–5am local) AND the merchant category is unusual for that hour (not gas station, not 24-hour pharmacy), flag.

- Severity: `medium`.
- This rule is noisy — use only when a location/time signal is clearly present.

### Rule 5 — Unexpected fee

Any transaction with `category: financial.fees` is captured. Tag with `fee_type` (overdraft, foreign-transaction, monthly-maintenance, ATM, late-payment).

- Severity: `low` for fees < $10, `medium` for fees $10–$50, `high` for overdraft fees and late-payment fees regardless of amount.
- Always actionable: most fees are negotiable or avoidable.

## Workflow

```
Anomaly Scan Progress:
- [ ] Step 1: Build merchant statistics from transactions_history
- [ ] Step 2: Run Rule 1 (duplicate within 48h)
- [ ] Step 3: Run Rule 2 (statistical anomaly)
- [ ] Step 4: Run Rule 3 (first-merchant high-dollar)
- [ ] Step 5: Run Rule 4 (geography/time)
- [ ] Step 6: Run Rule 5 (fees)
- [ ] Step 7: Deduplicate alerts (one tx may trigger multiple rules)
- [ ] Step 8: Rank by severity then dollar impact
- [ ] Step 9: Attach recommended actions
```

### Deduplication

A single transaction may legitimately trigger multiple rules (e.g., a $5,000 charge at a brand-new merchant in another state — Rules 3 and 4). Combine into a single alert with `triggered_rules: [...]` and the highest severity.

### Recommended actions

Each alert carries one of:

- `call_bank_fraud_line` — for `high` severity charges that the user does not recognize.
- `freeze_card` — for confirmed fraud or before calling the bank if multiple charges fired within hours.
- `dispute_charge` — for known-merchant overcharges or duplicate post-and-pending issues.
- `negotiate_fee` — for `financial.fees` (overdraft, monthly maintenance) that have a known negotiation playbook.
- `monitor` — for `medium`/`low` alerts where the user should confirm but no action is required if it's legitimate.

Always include a one-line `evidence` describing what triggered the rule, with concrete numbers.

## Output contract

```json
{
  "scanned": {
    "transactions_new": 142,
    "transactions_history": 1820,
    "merchants_with_stats": 218
  },
  "alerts": [
    {
      "id": "alert_20260424_001",
      "severity": "high",
      "triggered_rules": ["first_merchant_high_dollar"],
      "tx_ids": ["tx_20260424_011"],
      "merchant": "TECH-SHOP-ONLINE",
      "amount_cents": -245000,
      "account_id": "acc_cc_001",
      "evidence": "First charge ever from TECH-SHOP-ONLINE; amount $2,450 exceeds new-merchant high-dollar threshold of $500.",
      "suggested_action": "call_bank_fraud_line",
      "expected_user_response": "Confirm whether this purchase is yours; if not, freeze card and dispute."
    },
    {
      "id": "alert_20260424_002",
      "severity": "medium",
      "triggered_rules": ["statistical_anomaly"],
      "tx_ids": ["tx_20260424_023"],
      "merchant": "Whole Foods",
      "amount_cents": -38420,
      "evidence": "12-month avg $84.50, stddev $22.30; this charge ($384.20) is 13.4σ above mean.",
      "suggested_action": "monitor",
      "expected_user_response": "If you bought groceries for a party, ignore. Otherwise, check the receipt."
    },
    {
      "id": "alert_20260424_003",
      "severity": "high",
      "triggered_rules": ["fee_overdraft"],
      "tx_ids": ["tx_20260423_004"],
      "merchant": "Bank Name",
      "amount_cents": -3500,
      "evidence": "Overdraft fee of $35 charged on 2026-04-23. Account balance was negative for 2 days.",
      "suggested_action": "negotiate_fee",
      "expected_user_response": "Call the bank's customer line; first overdraft fees are typically waived on request."
    }
  ],
  "summary": {
    "alerts_total": 3,
    "high_severity": 2,
    "medium_severity": 1,
    "low_severity": 0
  }
}
```

## Guardrails

- **Never assert fraud.** Use language like "unusual," "first-ever," "above threshold." The user confirms; this skill flags.
- **Tune for false-positive cost.** A medium-severity alert is read; a high-severity alert disrupts the user's day. Reserve `high` for truly unusual.
- **Cite the math.** Every alert states the comparator (mean, stddev, occurrence count, threshold). The user must be able to evaluate the reasoning.
- **Honor history-context.** A "first-ever merchant" trigger should not fire when the merchant exists in history under a different rendered string. Use normalized merchant names from the categorizer.
- **Do not action without consent.** Suggested actions are for the user to take; the household-finance system never executes financial actions.
- **Retain the alert log.** All emitted alerts append to `reports/alerts/`. False positives feed back into the threshold tuning.
