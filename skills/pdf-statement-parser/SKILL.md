---
name: pdf-statement-parser
description: Parses a single financial statement PDF (checking, savings, credit card, brokerage, 401k, HSA, mortgage, tax form) and emits a normalized JSON record with institution, account mask, statement period, opening/closing balances, line-item transactions or holdings, and a confidence score. Use when extracting structured data from a bank, brokerage, retirement, or HSA PDF statement, when ingesting a drop of household finance documents, or when user mentions parsing a statement, extracting transactions from a PDF, or normalizing statement data.
---

# PDF Statement Parser

## Table of Contents
- [Overview](#overview)
- [Input contract](#input-contract)
- [Workflow](#workflow)
- [Document type playbooks](#document-type-playbooks)
- [Output contract](#output-contract)
- [Confidence scoring](#confidence-scoring)
- [Guardrails](#guardrails)
- [Example](#example)

## Overview

Bank, brokerage, retirement, HSA, and mortgage statements arrive as PDFs in many house-styles. This skill is the prompt-driven extraction methodology: identify the document type, locate the canonical fields by their labels (not position), pull every transaction or holding row, and emit a strict JSON record. All monetary values become **integer cents**, all dates become **ISO 8601 (YYYY-MM-DD)**.

Use directly with Claude's PDF reading: `Read` the PDF, then run this skill's workflow on the visible content. No external library needed.

## Input contract

The caller provides:

- `pdf_path` — absolute path to a single statement PDF.
- `expected_type` (optional) — one of `checking_statement | savings_statement | credit_card_statement | brokerage_statement | 401k_statement | hsa_statement | mortgage_statement | tax_form | insurance_doc | unknown`. If absent, the skill detects it.
- `known_accounts` (optional) — array of `{id, institution, mask, type}` for matching.

## Workflow

```
- [ ] Step 1: Read the PDF (first pass: pages 1-2 for header)
- [ ] Step 2: Detect document type from header keywords
- [ ] Step 3: Extract account identity (institution + mask + type)
- [ ] Step 4: Extract statement period (start/end dates)
- [ ] Step 5: Extract balance markers (opening / closing / available)
- [ ] Step 6: Extract line items (transactions, holdings, or events)
- [ ] Step 7: Normalize to integer cents and ISO dates
- [ ] Step 8: Score confidence on each field; emit JSON
```

### Step 1 — Read the PDF

Use the `Read` tool with the PDF path. For PDFs > 10 pages, read in chunks: pages 1–5 (header + first transactions), then subsequent ranges as needed. Track total page count.

### Step 2 — Detect document type

Look for these header signals (in order of authority):

| Signal | Document type |
|---|---|
| "Statement of Account" + "Available Balance" + checking-style transactions | `checking_statement` |
| "Savings Statement" / "Money Market Statement" | `savings_statement` |
| "Credit Card Statement" + "Payment Due" + "Minimum Payment" | `credit_card_statement` |
| "Account Summary" + "Holdings" + ticker symbols | `brokerage_statement` |
| "401(k) Statement" / "Retirement Plan" + "Vested Balance" | `401k_statement` |
| "Health Savings Account" / "HSA" + "Contribution Limit" | `hsa_statement` |
| "Mortgage Statement" + "Principal" + "Escrow" | `mortgage_statement` |
| "W-2" / "1099" / "1098" / "5498" form numbers | `tax_form` |
| Policy declaration page, premium, deductible | `insurance_doc` |

If two signals tie, prefer the one in the document title or page header.

### Step 3 — Extract account identity

- **Institution**: top-of-page logo text or "Issued by" / "Statement from" label.
- **Mask**: last 4 digits — search for `****1234`, `xxxx1234`, `Account ending in 1234`, or the redacted form the institution uses. Always store as `****1234`.
- **Account type**: derived from §2 above plus visible labels ("Checking", "Visa Signature", "Roth IRA").
- **Owner names**: full names of account holders (used for matching to `household.json` members downstream).

Match against `known_accounts` by `(institution, mask)`. If no match, mark `account_match: "new"` and propose an `account_id` like `acc_<type>_<incrementing>`.

### Step 4 — Extract statement period

Find labels: "Statement Period", "Cycle Date", "Closing Date", "Period Beginning … Period Ending". Output:
- `period_start` — first day covered (ISO).
- `period_end` — last day covered, also the statement closing date (ISO).

If only a closing date is present, set `period_end = closing_date` and `period_start = null` with `confidence: 0.6` on the period.

### Step 5 — Extract balance markers

For cash/credit accounts: `opening_balance_cents`, `closing_balance_cents`, `available_balance_cents` (if present). For credit cards, also `statement_balance_cents`, `minimum_payment_cents`, `payment_due_date`.

For brokerage / 401k / HSA: `total_value_cents`, `cash_cents`, `invested_cents`. Skip opening/closing transaction balances — these are holdings statements.

For mortgages: `current_principal_cents`, `monthly_pi_cents`, `monthly_escrow_cents`, `next_payment_due`, `extra_principal_ytd_cents`.

### Step 6 — Extract line items

Three modes:

**Cash/credit transactions.** For each row in the transactions table, capture: `date`, `post_date` (if separate column), `description_raw`, `amount`. Sign convention: outflows negative, inflows positive. If statement uses two columns ("Withdrawals" and "Deposits"), set sign accordingly. Preserve `description_raw` exactly as printed — the bookkeeper will normalize the merchant name later.

**Brokerage / 401k / HSA holdings.** For each holding row: `symbol`, `description`, `shares` (decimal), `price` (per-share), `value`, `cost_basis` (if shown), `asset_class` (mapped from fund description: see playbook below).

**Mortgage activity.** Recent payments table: each entry with `date`, `total_paid_cents`, `principal_cents`, `interest_cents`, `escrow_cents`, `extra_principal_cents`.

**Tax forms.** Form-specific fields per playbook (W-2 boxes, 1099-DIV ordinary/qualified dividends, 1098 mortgage interest paid, 5498-SA HSA contributions).

### Step 7 — Normalize

- Money: `$1,247.50` → `124750` cents. Negative outflow: `-$87.42` → `-8742`.
- Dates: `01/15/26` → `2026-01-15`. Two-digit years assume current century unless context says otherwise.
- Trim whitespace from descriptions; preserve case.

### Step 8 — Confidence scoring

Per field, assign a confidence in `[0.0, 1.0]`:
- `1.0` — extracted directly from a labeled field.
- `0.85–0.95` — extracted from positional context (column header inferred, value clear).
- `0.6–0.8` — inferred from surrounding text or partially OCR'd.
- `< 0.6` — flag for human review.

The overall record gets `confidence = min(per-field confidences for required fields)`.

## Document type playbooks

### checking_statement / savings_statement

Required: institution, mask, period_start, period_end, opening_balance_cents, closing_balance_cents, transactions[]. Reconcile: `opening + Σ(transactions.amount) = closing` within ±$1.

### credit_card_statement

Required: institution, mask, period_start, period_end, opening_balance_cents, closing_balance_cents, statement_balance_cents, minimum_payment_cents, payment_due_date, transactions[]. Note: credit-card outflows from the cardholder's perspective are *purchases* (positive on the card balance) — but for the unified household ledger, treat purchases as **negative** (money leaving the household) and payments to the card as **positive** (or as internal transfers). Document the sign convention you used.

### brokerage_statement

Required: institution, mask, account_type, period_end, total_value_cents, holdings[]. Optional: cash_cents, transactions[] (buys/sells/dividends). Asset-class mapping:

| Fund hint | asset_class |
|---|---|
| "S&P 500", "Total Stock Market", "Large Cap Blend", VOO/VTI/SPY | `us_equity` |
| "International", "Developed Markets", "Emerging Markets", VXUS/IXUS | `intl_equity` |
| "Total Bond", "Aggregate Bond", "Treasury", BND/AGG | `us_bond` |
| "Money Market", "Cash Reserve", SPAXX | `cash` |
| "REIT", "Real Estate" | `reit` |
| "Target Date 20XX" | `target_date` (note the year) |

If unmappable, leave `asset_class: null` with confidence `0.5`.

### 401k_statement

Required: institution, owner, period_end, total_balance_cents, ytd_contribution_cents (if shown), employer_match_ytd_cents (if shown), holdings[]. Watch for vesting columns — record `vested_cents` separately if shown.

### hsa_statement

Required: institution, period_end, cash_cents, invested_cents, total_cents, ytd_contribution_cents, ytd_distribution_cents (if shown). Note coverage type if printed: `self_only` or `family`.

### mortgage_statement

Required: institution, mask, period_end, current_principal_cents, monthly_pi_cents, monthly_escrow_cents, next_payment_due, recent_payments[]. Capture the rate APR if printed.

### tax_form

Required: form_type (`W-2`, `1099-DIV`, `1099-INT`, `1099-B`, `1098`, `5498-SA`, `1095`), tax_year, issuer, recipient, key_boxes (form-specific). Defer interpretation to the tax-compliance agent — this skill just captures the boxes.

## Output contract

Emit a single JSON object:

```json
{
  "document_type": "checking_statement",
  "source_path": "inbox/2026-01-15-batch/checking-jan.pdf",
  "institution": "Bank Name",
  "account": {
    "mask": "****1234",
    "type": "checking",
    "owners": ["Jane Doe", "John Doe"],
    "match": "acc_chk_001",
    "match_confidence": 0.95
  },
  "period": {
    "start": "2025-12-15",
    "end": "2026-01-14"
  },
  "balances": {
    "opening_cents": 1124300,
    "closing_cents": 1247500,
    "available_cents": 1247500
  },
  "transactions": [
    {
      "date": "2025-12-16",
      "post_date": "2025-12-17",
      "description_raw": "TRADER JOE'S #123 PORTLAND OR",
      "amount_cents": -8742,
      "confidence": 0.97
    }
  ],
  "reconciliation": {
    "expected_closing_cents": 1247500,
    "computed_closing_cents": 1247500,
    "diff_cents": 0,
    "ok": true
  },
  "extracted_at": "2026-01-20T14:00:00Z",
  "overall_confidence": 0.94,
  "warnings": []
}
```

For brokerage/401k/HSA replace `transactions` with `holdings` and balance fields per playbook.

## Confidence scoring

Reduce overall confidence and add a `warnings[]` entry whenever:
- Reconciliation diff > $1 → `warning: "reconcile_failed: diff $X.XX"` and `overall_confidence: max(0.5, current * 0.7)`.
- Any required field missing → `warning: "missing_required: <field>"` and `overall_confidence ≤ 0.5`.
- OCR-quality page (illegible characters) → `warning: "low_ocr_quality_page_<n>"` and apply the per-field confidence penalty.
- Unknown asset class on > 20% of holdings → `warning: "unknown_asset_class_high"`.

## Guardrails

- **Never invent values.** If a field is not visible in the PDF, set `null` and add a warning. Do not interpolate.
- **Never normalize merchant names here.** That is the bookkeeper's job; preserve `description_raw` byte-for-byte.
- **Never categorize transactions here.** Categorization is downstream (`transaction-categorizer`).
- **Always reconcile** for cash/credit statements before declaring `ok: true`.
- **Currency**: assume USD unless the statement says otherwise. If non-USD, capture the currency code; do not auto-convert.
- **Account mask only.** Never extract or store the full account number.

## Example

Given a 4-page Chase checking statement for the cycle 2025-12-15 to 2026-01-14 with opening balance $11,243.00, three deposits totaling $4,832.00, twenty-seven debits totaling $3,600.00, and closing balance $12,475.00, the parser emits:

- `document_type: "checking_statement"`
- `institution: "Chase"`
- `account.mask: "****1234"`, `account.type: "checking"`
- `period.start: "2025-12-15"`, `period.end: "2026-01-14"`
- `balances.opening_cents: 1124300`, `balances.closing_cents: 1247500`
- `transactions: [...]` — 30 entries, each with `description_raw`, `amount_cents` (signed), and per-field confidence ≥ 0.92
- `reconciliation.ok: true`, `diff_cents: 0`
- `overall_confidence: 0.95`, `warnings: []`
