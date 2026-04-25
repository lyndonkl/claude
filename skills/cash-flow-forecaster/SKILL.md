---
name: cash-flow-forecaster
description: Projects 30-90 days of daily cash flow per cash account by combining current balance, scheduled recurring inflows and outflows from recurring.json, and a 6-month rolling average of discretionary spend, then flags days where projected balance falls below a configurable safety floor. Use for forward planning, detecting upcoming overdrafts, sizing pre-funding for sinking funds, or when user mentions cash flow projection, runway, balance forecast, or upcoming bills coverage.
---

# Cash Flow Forecaster

## Table of Contents
- [Overview](#overview)
- [Input contract](#input-contract)
- [Workflow](#workflow)
- [Discretionary modeling](#discretionary-modeling)
- [Output contract](#output-contract)
- [Guardrails](#guardrails)

## Overview

A monthly average tells you nothing about whether your rent will clear on the third when your paycheck lands on the fifth. This skill projects daily ending balance for each cash account over the forecast horizon by combining:

- Today's actual balance.
- Every scheduled recurring inflow and outflow with a `next_expected_date` in the window.
- An estimated discretionary tail derived from the last 6 months of non-recurring spend.

It surfaces the days where projected balance dips below a configurable safety floor, and the trough day for each account.

## Input contract

The caller provides:

- `accounts` — array of cash accounts: `{id, type, current_balance_cents, safety_floor_cents}`.
- `recurring` — `recurring.json` filtered to `status: active`.
- `transactions` — last 180 days of categorized transactions for each cash account.
- `today` — ISO date.
- `horizon_days` — default 60.
- `category_overrides` (optional) — explicit one-time outflows the user knows about (e.g., upcoming travel deposit).

## Workflow

```
Forecast Progress:
- [ ] Step 1: Initialize daily ledger per account with current balance
- [ ] Step 2: Project recurring flows in the horizon window
- [ ] Step 3: Compute discretionary tail (rolling 6-month average)
- [ ] Step 4: Spread discretionary across days
- [ ] Step 5: Apply category_overrides
- [ ] Step 6: Compute daily ending balance
- [ ] Step 7: Flag below-floor days; identify trough
- [ ] Step 8: Compute confidence interval around projection
```

### Step 1 — Initialize

For each account, create `ledger[account_id][day] = 0` for each day in `[today, today + horizon_days]`. Set `ledger[account_id][today].opening = current_balance_cents`.

### Step 2 — Project recurring

For each active recurring entry, walk forward from `next_expected_date` adding by `cadence` until past the horizon. For each occurrence, push `amount_cents_typical` to `ledger[recurring.account_id][occurrence_date].flows`.

Handle weekends/holidays for paychecks: most direct deposits land on weekdays. If `next_expected_date` falls on a weekend, advance to the next weekday for inflows; outflows stay on the calendar date.

### Step 3 — Compute discretionary tail

For each account, compute:

```
discretionary_total_180d = Σ amount_cents over last 180 days
                            where category NOT IN
                            { financial.transfers_internal, savings_investment.*,
                              income.* }
                            and tx_id not in any recurring cluster
```

`discretionary_daily_avg = discretionary_total_180d / 180` (this is negative — discretionary spend).

### Step 4 — Spread discretionary

The simplest approach: subtract `discretionary_daily_avg` from every day in the horizon for that account.

A better approach when day-of-week patterns matter: compute per-DOW averages (Mondays differ from Fridays) and apply by day-of-week. Default to the simple approach unless `transactions` has at least 90 days of data and the per-DOW variance is materially different.

### Step 5 — Apply overrides

For each entry in `category_overrides`, add the explicit `{date, account_id, amount_cents, reason}` to that day's flows.

### Step 6 — Roll forward

```
balance[t] = balance[t-1] + Σ flows on day t
```

Track running balance per account.

### Step 7 — Flag below-floor

For each account, find days where `balance[t] < safety_floor_cents`. Identify:
- `trough_balance_cents` — minimum balance over horizon.
- `trough_date` — when it occurs.
- `first_breach_date` — first day below floor.
- `breach_days` — count of days below floor.

### Step 8 — Confidence interval

The discretionary spread carries variance. Compute the 30-day rolling stddev of discretionary spend and express the projection as a band: `balance ± 1.5σ × √days_from_today`. Surface `lower_balance_cents` and `upper_balance_cents` on the trough day so the user sees the range, not a false-precision point estimate.

## Discretionary modeling

Default: simple daily average over 180 days, all spend not in recurring or transfers/investments/income.

Refinements (apply only when supported by data):

- **Day-of-week.** Saturdays and Sundays are typically heavier — apply per-DOW factors.
- **Month start vs end.** Discretionary tends to spike around paydays. If recurring inflows land on the 1st and 15th, consider a small post-payday boost.
- **Seasonal.** Holiday spending in November–December is real. If forecast horizon crosses these months, allow a +20% multiplier and document it.

Document any refinement in the output's `methodology` field so the user can see exactly what was assumed.

## Output contract

```json
{
  "horizon": { "start": "2026-04-25", "end": "2026-06-24", "days": 60 },
  "accounts": [
    {
      "account_id": "acc_chk_001",
      "starting_balance_cents": 1247500,
      "ending_balance_cents": 932100,
      "trough_balance_cents": 124300,
      "trough_date": "2026-05-30",
      "trough_band_cents": [82100, 166500],
      "first_breach_date": null,
      "breach_days": 0,
      "safety_floor_cents": 100000
    }
  ],
  "daily": [
    { "date": "2026-04-25", "balances": { "acc_chk_001": 1247500 }, "flows": [] },
    { "date": "2026-05-01", "balances": { "acc_chk_001": 1093200 },
      "flows": [
        { "account_id": "acc_chk_001", "amount_cents": -273500, "label": "Mortgage P&I", "type": "recurring" },
        { "account_id": "acc_chk_001", "amount_cents": -78000,  "label": "Mortgage escrow", "type": "recurring" }
      ]
    }
  ],
  "alerts": [],
  "methodology": "Daily discretionary derived from 180-day rolling average across 23 non-recurring categories; 1.5σ confidence band; weekend-adjusted paychecks; no seasonal multiplier in this horizon."
}
```

When a breach is detected:

```json
{
  "alerts": [
    {
      "severity": "high",
      "type": "projected_below_floor",
      "account_id": "acc_chk_001",
      "first_breach_date": "2026-05-15",
      "trough_balance_cents": -42000,
      "trough_date": "2026-05-30",
      "drivers": [
        { "date": "2026-05-15", "amount_cents": -350000, "label": "Property tax (annual)" }
      ],
      "suggested_actions": [
        "Move $50,000 from savings before 2026-05-14",
        "Defer discretionary spend by $20,000 across the next 3 weeks"
      ]
    }
  ]
}
```

## Guardrails

- **Never forecast for non-cash accounts.** Brokerage/401k/HSA balances are not cash flows; they're holdings. Skip them.
- **Mortgage prepayments are explicit, not implicit.** A user's standard mortgage payment is recurring; an extra principal payment is a `category_override`. Do not project extra principal.
- **Discretionary average is a tail, not a forecast.** The band exists to remind the user this is an estimate; the trough's lower bound is the planning number, not the central one.
- **Don't double-count.** Recurring entries are excluded from the discretionary calculation by definition (a transaction tied to a recurring cluster is not in the discretionary set).
- **Refresh frequently.** A 60-day forecast becomes stale in days as new transactions land. The agent layer should re-run after every drop.
