---
name: transaction-categorizer
description: Assigns a category and subcategory to a financial transaction by matching its raw description against a configurable taxonomy and rules table, falling back to LLM inference when no rule matches. Emits a normalized merchant name, category path, recurring flag, and confidence score, and proposes new rules from confirmed classifications. Use when categorizing bank, credit-card, or brokerage transactions, building or refining a category taxonomy, or when user mentions transaction categorization, merchant normalization, expense classification, or category rules.
---

# Transaction Categorizer

## Table of Contents
- [Overview](#overview)
- [Input contract](#input-contract)
- [Workflow](#workflow)
- [Taxonomy](#taxonomy)
- [Rule format](#rule-format)
- [Confidence and audit](#confidence-and-audit)
- [Output contract](#output-contract)
- [Guardrails](#guardrails)

## Overview

A transaction is just a `description_raw` string and a signed `amount_cents`. This skill turns that into a clean `merchant`, a `category` + `subcategory`, an `is_recurring` boolean candidate, and a confidence. It applies rules first (cheap, deterministic) and only falls back to LLM inference for the residual.

It also produces *learned rules* — when a confident classification matches a clear merchant pattern, propose a new rule for the rule table so future identical transactions match for free.

## Input contract

The caller provides:

- `transactions` — array of `{id, description_raw, amount_cents, account_id, date, account_type}`.
- `taxonomy` — the `categories.json` taxonomy block (top-level → subcategory list).
- `rules` — array of existing rules (see [Rule format](#rule-format)).
- `account_type_hints` (optional) — when known, helps disambiguate (e.g., a deposit on a brokerage account is more likely `dividends` than `salary`).

## Workflow

```
Categorization Progress:
- [ ] Step 1: Normalize description_raw
- [ ] Step 2: Apply rules in priority order
- [ ] Step 3: Classify residual via LLM with taxonomy guard
- [ ] Step 4: Detect recurring candidates
- [ ] Step 5: Score confidence
- [ ] Step 6: Propose new rules from high-confidence matches
```

### Step 1 — Normalize

Build a `description_normalized` for matching only — never overwrite `description_raw`.

- Uppercase.
- Strip leading vendor codes (`SQ *`, `TST*`, `PAYPAL *`, `CKCD`, `POS DEBIT`, `ACH DEBIT`).
- Strip trailing geo (` PORTLAND OR`, ` 800-555-1234 CA`, ` #1234`).
- Collapse multiple spaces.
- Drop date numerics inside the description.

`SQ *TRADER JOES #123 PORTLAND OR` → `TRADER JOES`.

### Step 2 — Apply rules

For each transaction, walk `rules` in priority order. First rule whose `match` substring (case-insensitive) is a substring of `description_normalized` wins. Apply its `merchant`, `category`, `subcategory`, and `is_recurring` (if set).

If multiple rules match, the most specific (longest `match`) wins.

If a rule matches, set `source: "rule"` and `confidence: 1.0`.

### Step 3 — Classify residual

For unmatched transactions, classify via LLM:

- Constrain output to the supplied `taxonomy` — never invent a category.
- Pick `category.subcategory` (e.g., `food.groceries`).
- Propose a clean `merchant` name.
- If sign and account_type imply income, prefer the `income.*` branch.
- If account_type is `brokerage` or `401k` and amount is positive, prefer `income.dividends`, `income.interest_earned`, or `savings_investment.*`.
- If `description_raw` looks like an internal transfer between two of the user's accounts, classify as `financial.transfers_internal`.

Set `source: "llm"` and `confidence: 0.6–0.9` based on signal strength.

### Step 4 — Detect recurring candidates

Set `is_recurring: true` candidate if:
- The merchant has been seen ≥ 3 times in the last 90 days on the same account, with amount within ±10%, at a regular cadence (weekly, biweekly, monthly, quarterly).
- OR a matched rule explicitly set `is_recurring: true`.

This is a *candidate* — promotion to `recurring.json` is the recurring-charge-detector skill's job.

### Step 5 — Confidence

| Source | Default confidence |
|---|---|
| Rule match (substring length ≥ 8) | 1.00 |
| Rule match (substring length 4–7) | 0.92 |
| LLM with strong taxonomic signal (e.g., "NETFLIX" → entertainment.streaming) | 0.85 |
| LLM with weak signal | 0.65 |
| Cannot classify above `uncategorized` | 0.30 |

If confidence < 0.5, mark `category: "uncategorized.unknown"` and flag for review.

### Step 6 — Propose new rules

After classification, scan high-confidence LLM matches (`confidence ≥ 0.85`) where the same `description_normalized` substring covers ≥ 3 transactions in the input set. For each, propose a new rule and append to `rules.proposed[]` in the output. The bookkeeper agent confirms these before they merge into `categories.json`.

## Taxonomy

The skill respects the taxonomy supplied by the caller. The default taxonomy used by the household-finance team is:

```
housing → mortgage, rent, property_tax, hoa, home_insurance, home_maintenance,
          utilities_electric, utilities_gas, utilities_water, utilities_internet
food → groceries, restaurants, coffee, alcohol
transportation → gas, auto_insurance, auto_maintenance, public_transit, rideshare,
                 parking, tolls
health → medical_copay, prescriptions, dental, vision, mental_health, gym
personal → clothing, haircare, subscriptions_personal
kids → childcare, school, activities, kids_clothing
entertainment → streaming, events, hobbies, books
travel → flights, lodging, travel_food, travel_other
financial → fees, interest_paid, transfers_internal
income → salary, bonus, interest_earned, dividends, capital_gains, refund, other_income
savings_investment → 401k_contribution, ira_contribution, hsa_contribution,
                     brokerage_deposit, savings_deposit
uncategorized → unknown
```

Never invent a category. If a transaction does not fit, use `uncategorized.unknown` and emit a `taxonomy_gap` warning.

## Rule format

```json
{
  "match": "TRADER JOE",
  "merchant": "Trader Joe's",
  "category": "food",
  "subcategory": "groceries",
  "is_recurring": false,
  "priority": 100,
  "added_on": "2026-01-20",
  "source": "user_confirmed | learned"
}
```

Higher `priority` values win ties. Rules added by humans default to priority 200; rules learned by this skill default to 100.

## Confidence and audit

Every output transaction carries:
- `category` and `subcategory` — must be in taxonomy.
- `merchant` — clean display name.
- `confidence` — `[0.0, 1.0]`.
- `source` — `rule | llm | uncategorized`.
- `matched_rule_id` (if `source: rule`).

Never overwrite `description_raw`; always preserve it for re-classification.

## Output contract

```json
{
  "categorized": [
    {
      "id": "tx_20260115_001",
      "merchant": "Trader Joe's",
      "category": "food",
      "subcategory": "groceries",
      "is_recurring_candidate": false,
      "confidence": 1.0,
      "source": "rule",
      "matched_rule_id": "rule_trader_joes"
    }
  ],
  "rules_proposed": [
    {
      "match": "BLUE BOTTLE",
      "merchant": "Blue Bottle Coffee",
      "category": "food",
      "subcategory": "coffee",
      "evidence_count": 4,
      "evidence_tx_ids": ["tx_20260103_004", "tx_20260110_002", "tx_20260117_007", "tx_20260124_001"]
    }
  ],
  "warnings": [
    { "tx_id": "tx_20260118_009", "type": "taxonomy_gap", "description_raw": "ZELLE TO M COPPENS" }
  ],
  "summary": {
    "total": 142,
    "rule_matched": 118,
    "llm_classified": 22,
    "uncategorized": 2,
    "uncategorized_pct": 1.4
  }
}
```

## Guardrails

- **Preserve `description_raw`** byte-for-byte. Normalization is for matching only.
- **Never invent categories.** Stay within the supplied taxonomy.
- **Account-type aware.** A "deposit" on a brokerage account is not salary; a "withdrawal" on a savings account is likely a transfer, not spending.
- **Internal transfers must net to zero across accounts.** If a `financial.transfers_internal` is classified on one side, the matching opposite-sign transaction on the other account should also be `transfers_internal` — flag if not.
- **Uncategorized rate** above 5% of new transactions in a batch is a quality signal; surface it in the summary.
- **No PII in proposed rules.** A rule like `match: "ZELLE TO JOHN SMITH"` exposes a name; redact or skip such proposals.
