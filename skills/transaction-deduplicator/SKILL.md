---
name: transaction-deduplicator
description: Detects and removes duplicate transactions across overlapping bank, credit-card, and brokerage statement imports using a stable composite key (account_id, date ±1d, amount_cents, description_normalized). Emits a list of new transactions to commit, a list of suppressed duplicates with their reasons, and a list of suspicious near-duplicates that need human review. Use when ingesting financial statements that may overlap prior drops, merging multiple export sources for the same account, or when user mentions duplicate transactions, deduping a transaction file, or reconciling overlapping statements.
---

# Transaction Deduplicator

## Table of Contents
- [Overview](#overview)
- [Input contract](#input-contract)
- [The dedupe key](#the-dedupe-key)
- [Workflow](#workflow)
- [Near-duplicate handling](#near-duplicate-handling)
- [Output contract](#output-contract)
- [Guardrails](#guardrails)

## Overview

Statement drops often overlap. A January statement covers December 15 → January 14; the December statement covers November 15 → December 14; the same December 15 transaction appears in both. This skill identifies those duplicates without losing legitimate same-day same-amount same-merchant repeat charges (e.g., two coffees in one day).

## Input contract

The caller provides:

- `incoming` — array of newly extracted transactions: `{date, post_date, account_id, amount_cents, description_raw, source}`.
- `existing` — array of transactions already in the store with the same fields plus `id`.

## The dedupe key

A duplicate is identified by the tuple:

```
(account_id, abs(amount_cents), description_normalized, |date_a - date_b| <= 1 day)
```

- `description_normalized` uses the same normalization as the categorizer (uppercase, strip vendor codes, strip geo, collapse spaces, drop dates).
- The 1-day window absorbs `date` vs `post_date` mismatches between two sources.
- `abs(amount_cents)` allows a refund matched against the original purchase to NOT be considered a duplicate (different sign). The composite key uses signed amount.

Use **signed** `amount_cents`. Refunds (opposite sign) are never duplicates of purchases.

## Workflow

```
Dedupe Progress:
- [ ] Step 1: Index existing transactions by (account_id, signed_amount, normalized_desc)
- [ ] Step 2: For each incoming, look up the index
- [ ] Step 3: Filter index hits by date proximity (≤ 1 day)
- [ ] Step 4: If no hit, mark as new
- [ ] Step 5: If exactly one hit, mark as duplicate of that id
- [ ] Step 6: If multiple hits, run the multi-instance same-day rule
- [ ] Step 7: Surface near-duplicates (different amount or desc) for review
```

### Step 1 — Index

Build `existing_by_key[(account_id, amount_cents, description_normalized)] = [tx, …]`.

### Step 2 — Lookup

For each incoming transaction, compute its key tuple and look up the bucket.

### Step 3 — Date proximity filter

For each candidate in the bucket, keep only those with `|incoming.date − candidate.date| ≤ 1 day`. Use `min(date, post_date)` on each side if `post_date` exists.

### Step 4 — No hit

Mark `decision: "new"`. The bookkeeper will append it to `transactions.json`.

### Step 5 — Exactly one hit

Mark `decision: "duplicate"` and link `duplicate_of: <existing_id>`. Do not import.

### Step 6 — Multiple hits (legitimate same-day repeats)

When the existing store already has N transactions with the identical key on the same day, and the incoming batch contains M transactions with the same key on that day:

- If `M ≤ N` → all incoming considered duplicates of existing ones (1:1 pairing in date order).
- If `M > N` → the first N incoming are duplicates; the remaining `M − N` are new transactions (legitimate same-day repeat charges, e.g., two coffees, gas-station pre-auth + final).

This rule preserves real repeat charges while still suppressing overlap-import duplicates.

### Step 7 — Near-duplicate review

A *near-duplicate* shares everything except amount or description and is within 1 day. These commonly arise when:
- A pending charge ($45.00) finalizes at a slightly different amount ($45.83) — keep the final, drop the pending.
- The merchant string changes mid-cycle ("AMAZON.COM*ABC123" → "AMZN Mktp US").

Emit these to `review[]` with both records side-by-side and a suggested action: `keep_incoming_drop_existing | keep_existing_drop_incoming | keep_both | merge`.

## Near-duplicate handling

Compute a similarity score on near-misses:
- Amount delta: 1.0 if equal, 0.9 if within $1 or 2%, 0.5 if within $5 or 10%, else 0.0.
- Description Jaccard on token sets: 0.0–1.0.
- Date proximity: 1.0 same day, 0.7 within 1 day, 0.4 within 3 days.

`near_dup_score = 0.4*amount + 0.4*description + 0.2*date`.

Surface for review when `0.7 ≤ near_dup_score < 0.95`. Above `0.95` is treated as duplicate; below `0.7` is treated as independent.

## Output contract

```json
{
  "new": [
    { "id": "tx_20260115_017", "decision": "new" }
  ],
  "duplicates": [
    {
      "incoming_index": 4,
      "decision": "duplicate",
      "duplicate_of": "tx_20251220_003",
      "reason": "exact key match within 1 day window"
    }
  ],
  "review": [
    {
      "incoming_index": 12,
      "matched_existing_id": "tx_20260108_005",
      "near_dup_score": 0.86,
      "diff": {
        "amount_cents": [-4500, -4583],
        "description_raw": ["AMAZON PENDING", "AMZN MKTP US*AB12CD"]
      },
      "suggested_action": "keep_incoming_drop_existing",
      "rationale": "incoming is the finalized charge (post_date set, definite merchant code)"
    }
  ],
  "summary": {
    "incoming_total": 142,
    "new_count": 96,
    "duplicate_count": 44,
    "review_count": 2
  }
}
```

## Guardrails

- **Sign matters.** Never collapse a refund and a purchase by absolute value. Use signed amount in the key.
- **One-day window only.** Wider windows produce false positives across pay cycles.
- **Same-account only.** Never dedupe across accounts. A $50 transfer out of checking and a $50 deposit into savings are two records, not one duplicate.
- **Preserve raw description in review.** Show both `description_raw` strings to the human; do not show the normalized form.
- **Idempotency.** Running the dedupe on the same input twice produces the same output. The skill never mutates `existing`.
- **Audit.** For every suppressed duplicate, log `duplicate_of` so the user can trace why a transaction did not appear in the new import.
