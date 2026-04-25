---
name: tax-loss-harvest-scanner
description: Scans a taxable brokerage account for individual lots with unrealized losses above a configurable threshold, identifies wash-sale risks by checking recent buys and forward planned buys of substantially identical securities (across all household accounts including spousal), and proposes harvest pairs (sell-for-loss + immediate buy of a similar-but-not-identical replacement). Use for year-end tax planning, monthly TLH scans, after market drawdowns, or when user mentions tax-loss harvesting, TLH, wash sale, or harvest candidates.
---

# Tax-Loss Harvest Scanner

## Table of Contents
- [Overview](#overview)
- [Input contract](#input-contract)
- [Wash-sale rules](#wash-sale-rules)
- [Workflow](#workflow)
- [Substitute pairs](#substitute-pairs)
- [Output contract](#output-contract)
- [Guardrails](#guardrails)

## Overview

Tax-loss harvesting realizes losses in a taxable brokerage to offset gains (and up to $3,000 of ordinary income per year) without changing the household's economic position — the proceeds buy a similar-but-not-identical security, keeping market exposure intact. The hardest part is the wash-sale rule: a sale at a loss is disallowed if a substantially identical security is bought within 30 days *in any household account, including a spouse's IRA*.

This skill scans the taxable brokerage for harvest candidates and validates each against the wash-sale window across all household accounts.

## Input contract

The caller provides:

- `taxable_holdings` — lots in the taxable brokerage, ideally per-lot: `{symbol, shares, cost_basis_cents, value_cents, acquisition_date}`. If only aggregate position-level data is available, mark `lot_resolution: aggregate` and document the limitation.
- `all_account_transactions_60d` — every buy/sell/dividend reinvest across **every** household account (taxable, 401k, IRA, spouse's IRA, HSA) in the last 60 days. Used for wash-sale detection.
- `planned_buys_30d` (optional) — dividend reinvest schedules, 401k contributions, automatic deposits — anything that will *buy* in the next 30 days.
- `loss_threshold_cents` — minimum unrealized loss to consider; default `50000` ($500).
- `today` — ISO date.

## Wash-sale rules

Per IRS, a wash sale is triggered when a security sold at a loss is replaced by a "substantially identical" security purchased within the 61-day window centered on the sale date (30 days before, 30 days after).

For this skill:

1. **Same ticker.** Always substantially identical. Period.
2. **Same fund family, same index.** VTI ↔ VFIAX ↔ FXAIX (S&P 500 / Total US trackers from different families) are *generally not considered identical* by IRS guidance — but the skill conservatively treats two funds tracking the **same index** as substantially identical.
3. **Different index, similar exposure.** VTI (Total US Market) ↔ ITOT (Total US Market different family) — not substantially identical. These are valid TLH pairs.
4. **All household accounts count.** Spouse's IRA, 401k auto-purchases, HSA auto-buys — all in scope.
5. **Dividend reinvestment.** A dividend reinvest within the 30-day window IS a wash-sale triggering buy. Disable DRIP on the harvested security before the sale.

## Workflow

```
TLH Scan Progress:
- [ ] Step 1: Filter taxable lots with unrealized loss >= loss_threshold
- [ ] Step 2: For each candidate, check 30-day backward wash-sale window
- [ ] Step 3: For each candidate, check 30-day forward planned-buys window
- [ ] Step 4: Identify substitute security (similar exposure, not identical)
- [ ] Step 5: Compute realized loss and tax savings estimate
- [ ] Step 6: Emit harvest proposals with explicit wash-sale guard
- [ ] Step 7: Surface candidates blocked by wash sale with the unblock date
```

### Step 1 — Loss filter

`unrealized_loss_cents = value_cents − cost_basis_cents` (negative). Keep lots where `|unrealized_loss_cents| ≥ loss_threshold_cents` AND `unrealized_loss_cents < 0`.

If lot-level resolution is unavailable, fall back to position-level using `weighted_avg_cost_basis`. Document `lot_resolution: aggregate` and warn that some lots may have gains while others have losses; only the aggregate is loss-positive.

### Step 2 — Backward window

For each candidate symbol, look back 30 days in `all_account_transactions_60d` for any buy of the same or substantially-identical security. If found, the sale would be partially or fully washed — disallow until 30 days after the most recent buy. Surface as `blocked_until: YYYY-MM-DD`.

### Step 3 — Forward window

Look at `planned_buys_30d` for the same or substantially-identical security. Common cases:
- 401k payroll contribution buys an S&P 500 index fund every 2 weeks → if harvesting S&P 500 in taxable, the next 401k buy washes the loss.
- Dividend reinvest scheduled.
- Automatic monthly brokerage deposit.

Resolutions:
- For 401k payroll: if practical, change the 401k buy to a different asset class for one cycle; otherwise harvest a different security.
- For DRIP: turn off DRIP on the harvest target ≥ 1 day before sale.
- For automatic deposits: defer or redirect.

### Step 4 — Substitute pair

Pick a substitute that maintains market exposure. The skill carries a default mapping (see [Substitute pairs](#substitute-pairs)). The substitute must:
- Track a similar but distinct index.
- Be available in the destination account.
- Have low expense ratio (ideally ≤ 0.10%).

### Step 5 — Tax savings estimate

`tax_savings_cents ≈ |realized_loss_cents| × marginal_rate`, where marginal rate is provided or defaulted to 24% for offsetting ordinary income up to $3,000 and 15% for offsetting long-term gains. Surface both.

### Step 6 — Emit proposal

Each proposal includes:
- Sell side: account, symbol, lot(s), shares, realized loss.
- Buy side: account, substitute symbol, shares, dollar amount.
- Wash-sale guard: confirmed clear ±30 days.
- Tax savings estimate.
- Disable-DRIP step (if applicable).

### Step 7 — Blocked candidates

For losses that are blocked, emit a `blocked[]` list with `unblock_date` so the user knows when the candidate becomes harvestable.

## Substitute pairs

Reasonable starting pairs (skill emits these as proposed, not authoritative):

| Sell | Buy substitute | Rationale |
|---|---|---|
| VTI (Total US Market) | ITOT (Total US Market, iShares) | Different family, similar exposure |
| VOO (S&P 500) | VTI (Total US Market) | Different index |
| VXUS (Total Intl) | IXUS (Total Intl, iShares) | Different family |
| BND (US Aggregate Bond) | AGG (US Aggregate Bond, iShares) | Different family, same exposure — borderline; prefer a slightly different index like SCHZ |
| IEFA (Developed Intl) | VEA (Developed Intl) | Different family |
| FXAIX (Fidelity S&P 500) | FSKAX (Fidelity Total Market) | Different index |

Always document the substitute as a *suggestion* — the user verifies appropriateness for their plan.

## Output contract

```json
{
  "as_of": "2026-04-25",
  "candidates_total": 5,
  "harvest_proposals": [
    {
      "id": "tlh_20260425_001",
      "sell": {
        "account_id": "acc_inv_fid_001",
        "symbol": "VTI",
        "lots": [
          { "acquisition_date": "2024-09-12", "shares": 35, "cost_basis_cents": 985250, "value_cents": 935500 }
        ],
        "realized_loss_cents": -49750
      },
      "buy": {
        "account_id": "acc_inv_fid_001",
        "symbol": "ITOT",
        "shares": 38,
        "value_cents": 935500,
        "rationale": "Substantially similar exposure to VTI, different index family — not substantially identical per common interpretation"
      },
      "wash_sale_check": {
        "backward_30d_clear": true,
        "forward_30d_clear": false,
        "blockers": [
          { "type": "401k_payroll_buy", "symbol_substantially_identical": "FSKAX", "buy_date": "2026-05-02" }
        ],
        "remediation": "Change 401k allocation away from FSKAX for the 2026-05-02 cycle, or harvest a different security"
      },
      "tax_savings_estimate_cents": 11940,
      "drip_disable_required": true,
      "status": "remediation_required"
    }
  ],
  "blocked": [
    {
      "symbol": "VXUS",
      "reason": "spouse_ira_buy_within_30d",
      "unblock_date": "2026-05-12"
    }
  ],
  "warnings": []
}
```

## Guardrails

- **Wash-sale check across ALL household accounts.** Spousal IRAs count. 401k auto-purchases count. DRIP counts.
- **Lot-level resolution preferred.** Aggregate-only data should reduce confidence and surface a warning.
- **Substitute is a proposal.** The user must confirm it's not "substantially identical" per their interpretation; the IRS has not crisply defined this for all index pairs.
- **Disable DRIP before the sale.** If DRIP is on for the harvested security, the next dividend washes the loss.
- **Don't pair across account types blindly.** A loss harvested in taxable cannot be replaced by a buy in 401k of the same security — that's still a wash sale.
- **Track realized losses YTD.** Surface running total — once the user has $3,000 of net realized losses to offset ordinary income, additional harvesting only carries forward (still useful, but lower marginal benefit).
- **Never execute.** Proposals only.
