---
name: statement-reconciler
description: Verifies that an extracted statement is internally consistent by checking that opening_balance + sum(transactions) = closing_balance within a small tolerance, and produces a reconciliation report flagging missing rows, double-counted rows, sign errors, and rounding diffs. Use as the gate between PDF extraction and committing transactions to the data store, when reconciling a statement that does not balance, or when user mentions reconcile, balance check, or statement does not tie out.
---

# Statement Reconciler

## Table of Contents
- [Overview](#overview)
- [Input contract](#input-contract)
- [The reconciliation identity](#the-reconciliation-identity)
- [Workflow](#workflow)
- [Diagnostics](#diagnostics)
- [Output contract](#output-contract)
- [Guardrails](#guardrails)

## Overview

A statement that doesn't reconcile is a statement that hasn't been parsed correctly. This skill enforces the only check that catches every failure mode of the parser at once: opening + Σ(transactions) = closing. When it fails, it diagnoses *why* — missing transaction, sign flip, double-counted row, rounding from a foreign-currency conversion — so the bookkeeper can fix or escalate before committing dirty data.

## Input contract

The caller provides the parser output:

- `account_id`, `period_start`, `period_end`.
- `opening_balance_cents`, `closing_balance_cents`.
- `transactions` — array of `{id, date, amount_cents, description_raw}`.
- `tolerance_cents` (default `100` = $1.00).
- `account_type` — affects sign convention (see below).

## The reconciliation identity

For cash and credit accounts:

```
closing_balance_cents = opening_balance_cents + Σ transactions.amount_cents
```

Sign conventions:

| Account type | Outflow (e.g., purchase, payment, withdrawal) | Inflow (e.g., deposit, payment received) |
|---|---|---|
| `checking` / `savings` | negative | positive |
| `credit_card` (household-ledger view) | negative purchase | positive card payment |
| `credit_card` (issuer's balance view) | positive (balance grows) | negative (balance shrinks) |

This skill expects the **household-ledger view** for cash and credit cards: outflows are negative, inflows are positive. If the parser used the issuer view for a credit card, flip signs before reconciling.

For brokerage / 401k / HSA holdings statements, this skill does not apply (those are point-in-time, not flow). Skip.

## Workflow

```
Reconciliation Progress:
- [ ] Step 1: Confirm account_type is in {checking, savings, credit_card, mortgage}
- [ ] Step 2: Sum signed amount_cents
- [ ] Step 3: Compute computed_closing = opening + sum
- [ ] Step 4: Compute diff = closing − computed_closing
- [ ] Step 5: If |diff| <= tolerance, return ok: true
- [ ] Step 6: Else, run diagnostics
- [ ] Step 7: Emit reconciliation report
```

### Steps 1–5

Trivial. Most statements pass step 5 immediately.

### Step 6 — Diagnostics

Walk these checks in order; the first that explains the diff wins.

**Diagnostic A — sign flip suspect.** If `|diff| / 2` matches the absolute value of any single transaction within $0.50, that transaction's sign was likely flipped during extraction. Report: `sign_flip_suspect: tx_id_X`.

**Diagnostic B — missing transaction.** If `|diff|` matches a "Fees" or "Interest" line summary on the statement but no matching individual transaction was extracted, the parser missed the row. Report: `missing_transaction_suspect: <amount> <description>`.

**Diagnostic C — double-counted transaction.** If the same `(date, amount, description)` triple appears twice in the input, and `|diff|` matches that amount, drop one and re-check. Report: `double_counted: tx_id_X`.

**Diagnostic D — fee/charge omission.** If `diff` is small (≤ $50) and consistent with a typical fee, look for "Service Charge" / "Monthly Fee" / "Foreign Transaction Fee" lines that may have been missed.

**Diagnostic E — rounding accumulation.** If `|diff| ≤ tolerance × N/100` for `N` transactions, a per-row rounding may have crept in. This is rare with integer cents but possible with foreign-currency lines. Report: `rounding_drift_suspect`.

**Diagnostic F — period mismatch.** If `period_end` does not match the statement's printed closing date, the wrong opening or closing was paired. Report: `period_mismatch_suspect`.

If no diagnostic fires, return `ok: false` with `diagnostic: "unknown"` so the bookkeeper escalates.

### Step 7 — Tolerance policy

Default tolerance: $1.00 (`100` cents).

Tighten to `0` for credit-card statements where the issuer reconciles to the cent. Loosen to `$5` only when explicitly asked, and surface the exact diff so the user knows.

## Output contract

```json
{
  "account_id": "acc_chk_001",
  "period_start": "2025-12-15",
  "period_end": "2026-01-14",
  "opening_balance_cents": 1124300,
  "closing_balance_cents": 1247500,
  "transactions_sum_cents": 123200,
  "computed_closing_cents": 1247500,
  "diff_cents": 0,
  "tolerance_cents": 100,
  "ok": true,
  "diagnostic": null,
  "suggestions": []
}
```

Failed example:

```json
{
  "account_id": "acc_cc_001",
  "period_start": "2025-12-15",
  "period_end": "2026-01-14",
  "opening_balance_cents": 0,
  "closing_balance_cents": -284300,
  "transactions_sum_cents": -283100,
  "computed_closing_cents": -283100,
  "diff_cents": -1200,
  "tolerance_cents": 100,
  "ok": false,
  "diagnostic": "missing_transaction_suspect",
  "suggestions": [
    {
      "type": "missing_transaction",
      "expected_amount_cents": -1200,
      "hint": "statement summary lists 'Foreign Transaction Fee $12.00' but no transaction extracted with that amount",
      "action": "re-parse PDF page 3, look for fee line"
    }
  ]
}
```

## Guardrails

- **Never silently widen the tolerance.** If the diff exceeds tolerance, the reconciler must fail the check — the bookkeeper agent decides whether to escalate or re-parse.
- **Never commit a non-reconciling statement.** The bookkeeper agent must hold the data until reconciliation succeeds. Failing reconciliation creates a `reports/alerts/` entry, never a silent drop.
- **Brokerage / 401k / HSA / tax forms are out of scope.** Holdings statements and tax forms do not have a single closing-balance identity; they have other consistency checks owned by their respective agents.
- **Idempotency.** Calling the reconciler twice on the same input produces the same output.
- **Useful diff sign.** A negative `diff_cents` means the computed closing is *higher* than reported (i.e., we have transactions explaining more cash than the statement says exists) — usually a missing inflow or a wrong-signed outflow.
