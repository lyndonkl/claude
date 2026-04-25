---
name: hsa-receipt-vault
description: Maintains a ledger of HSA-qualified medical expenses paid out of pocket (not reimbursed from the HSA), each with date, amount, provider, description, and a path to the scanned receipt. Tracks the running unreimbursed total — the amount of HSA balance the household can pull tax-free at any future date — and validates each candidate against IRS-qualified-expense categories. Use when a new medical receipt arrives, when totaling future tax-free HSA reimbursements, when planning a deferred reimbursement, or when user mentions HSA receipt vault, qualified medical expenses, or HSA shoebox strategy.
---

# HSA Receipt Vault

## Table of Contents
- [Overview](#overview)
- [Why this matters](#why-this-matters)
- [Input contract](#input-contract)
- [Qualified expense categories](#qualified-expense-categories)
- [Workflow](#workflow)
- [Output contract](#output-contract)
- [Guardrails](#guardrails)

## Overview

The HSA "shoebox" strategy: pay medical bills out of pocket, save the receipts, let the HSA grow tax-free for decades, then reimburse yourself any time later — there is no time limit on HSA reimbursements as long as the expense was incurred after the HSA was opened. This skill maintains the ledger, validates entries, and exposes the running unreimbursed total.

## Why this matters

Every dollar in this ledger is a dollar the household can withdraw tax-free from the HSA at any future point — effectively making the HSA function like a Roth IRA for medical-expense-equivalent dollars, with the optionality to reimburse before retirement if cash is needed.

## Input contract

Two modes:

**A — single receipt to add:**
```
{
  "date": "2026-03-10",
  "amount_cents": 18500,
  "provider": "Dr. Smith DDS",
  "description": "Dental cleaning",
  "receipt_path": "receipts/2026/2026-03-10-smith-dds.pdf",
  "paid_from_account_id": "acc_chk_001",
  "tx_id": "tx_20260310_004"
}
```

**B — bulk reconcile** (scan transactions for `category: health.*`):
```
{
  "transactions": [...],
  "existing_vault": [...],
  "hsa_open_date": "2018-01-15"
}
```

In bulk mode, the skill walks `category: health.*` transactions, proposes vault entries for those not already in the ledger, and asks the user (via output) to confirm each.

## Qualified expense categories

IRS Publication 502 governs HSA-qualified expenses. The skill validates against these high-level categories:

| Qualified | Examples |
|---|---|
| Medical care | Doctor visits, hospital, surgery, ambulance |
| Dental | Cleanings, fillings, extractions, orthodontia |
| Vision | Eye exams, glasses, contacts, LASIK |
| Mental health | Therapy, psychiatry, prescribed inpatient treatment |
| Prescription drugs | Rx, insulin (OTC insulin since 2020) |
| OTC medicine and menstrual products | Allowed since CARES Act 2020 |
| Medical equipment | Crutches, hearing aids, CPAP, blood-pressure monitors |
| Long-term care | Premiums (within IRS limits) and qualified care |
| Acupuncture, chiropractic | Yes |
| Smoking cessation | Yes |
| Weight loss for specific diseases | Only if prescribed for diabetes, hypertension, etc. |

Generally **not** qualified:
- Gym membership (unless prescribed for a specific medical condition with a Letter of Medical Necessity).
- Cosmetic procedures.
- Vitamins and supplements (unless prescribed to treat a specific condition).
- Marriage / family counseling.
- Insurance premiums (with narrow exceptions: COBRA, while receiving unemployment, Medicare for those 65+).

If a candidate is ambiguous, mark `qualification: unclear` with the IRS Pub 502 reference and let the user confirm.

## Workflow

```
HSA Vault Progress:
- [ ] Step 1: Validate receipt date is after HSA open date
- [ ] Step 2: Map description to a qualified-expense category
- [ ] Step 3: Confirm receipt_path exists or note it's pending
- [ ] Step 4: Confirm amount paid from a non-HSA account (else not a vault entry)
- [ ] Step 5: Generate id and append to ledger
- [ ] Step 6: Update running unreimbursed_total
- [ ] Step 7: Emit warnings for ambiguous qualifications
```

### Step 1 — Date check

Receipts dated **before** the HSA was opened are NOT eligible for tax-free reimbursement, no matter when the HSA grows. Reject with a clear warning.

### Step 2 — Category mapping

Use the description and the merchant category to map to a qualified category. If unmappable, mark `qualification: unclear` and suggest the user attach a Letter of Medical Necessity if applicable.

### Step 3 — Receipt path

The receipt must be retained — the IRS can request substantiation up to the statute of limitations after reimbursement. Acceptable receipt formats: PDF, JPG, PNG. Path stored relative to the household-finance root: `receipts/YYYY/YYYY-MM-DD-provider.ext`.

If `receipt_path` is missing, accept the entry but mark `receipt_status: pending` and emit a warning. Do not allow `pending` entries to count toward the running unreimbursed_total — they will, once the receipt is attached.

### Step 4 — Source account

A receipt only enters the vault if it was paid from a *non-HSA* account. Anything paid directly from the HSA debit card or HSA bill-pay is already a tax-free distribution; it doesn't go in the shoebox.

### Step 5 — Append

Generate `id: rcpt_<year>_<seq>`, append to `hsa.json.receipt_vault[]`. Never mutate prior entries; if a correction is needed, append a `correction_of: <prior_id>` entry.

### Step 6 — Running total

`unreimbursed_total_cents = Σ amount_cents WHERE receipt_status = "ok" AND reimbursed = false`.

This is the headline number — the dollars the household can pull tax-free at any time.

### Step 7 — Warnings

- `qualification: unclear` — surface to user.
- Receipt date > 1 year old when added — informational; some users batch-enter retroactively, which is fine.
- Amount > $1,000 single receipt — informational; ensure receipt covers the full amount.
- Same date + same provider + same amount as an existing entry — possible duplicate; surface for confirmation.

## Output contract

For mode A (single add):

```json
{
  "added": {
    "id": "rcpt_2026_0014",
    "date": "2026-03-10",
    "amount_cents": 18500,
    "provider": "Dr. Smith DDS",
    "description": "Dental cleaning",
    "category": "dental",
    "qualification": "ok",
    "receipt_path": "receipts/2026/2026-03-10-smith-dds.pdf",
    "receipt_status": "ok",
    "paid_from_account_id": "acc_chk_001",
    "tx_id": "tx_20260310_004",
    "reimbursed": false,
    "tax_year": 2026
  },
  "running_totals": {
    "unreimbursed_total_cents": 4435500,
    "by_year_cents": {
      "2024": 1820000,
      "2025": 2150000,
      "2026": 465500
    }
  },
  "warnings": []
}
```

For mode B (bulk reconcile):

```json
{
  "proposed": [
    {
      "tx_id": "tx_20260118_005",
      "amount_cents": 4500,
      "provider": "CVS Pharmacy",
      "description_raw": "CVS/PHARMACY #04123",
      "suggested_category": "prescription_drugs",
      "qualification": "ok",
      "needs_receipt_upload": true
    },
    {
      "tx_id": "tx_20260201_002",
      "amount_cents": 8500,
      "provider": "Equinox",
      "description_raw": "EQUINOX MONTHLY DUES",
      "suggested_category": null,
      "qualification": "not_qualified",
      "rationale": "Gym memberships are not qualified unless prescribed for a specific medical condition with a Letter of Medical Necessity."
    }
  ],
  "running_totals": {
    "unreimbursed_total_cents": 4435500
  }
}
```

## Guardrails

- **HSA-open-date check is non-negotiable.** Pre-open expenses can never be reimbursed tax-free.
- **Source-account check is non-negotiable.** Receipts paid directly from the HSA never enter the vault.
- **Receipt retention is the user's responsibility.** Track `receipt_path` faithfully; flag missing receipts; do NOT count them toward the unreimbursed total.
- **Append-only ledger.** Never mutate. Use `correction_of` to amend.
- **The unreimbursed total is potential, not realized.** Surface it as "available for tax-free reimbursement at any time." It does not appear on a tax return until reimbursement actually occurs.
- **Do NOT propose reimbursement timing.** That's a treasury decision (cash needs vs. continued HSA growth) made by the user with the savings-debt and investment-retirement agents.
- **OTC and menstrual products are qualified post-2020.** Don't reject these by reflex.
