---
name: portfolio-drift-rebalancer
description: Aggregates investment holdings across taxable brokerage, 401k, and HSA into a single asset-allocation view, computes drift versus a target allocation, and produces a tax-efficient rebalance proposal that prefers tax-advantaged accounts for the trades and never executes. Flags drift over 5 percentage points and free-money issues like missed 401k employer match. Use when reviewing portfolio allocation, planning a rebalance, computing drift, or when user mentions asset allocation, drift, rebalancing proposal, or 401k match.
---

# Portfolio Drift Rebalancer

## Table of Contents
- [Overview](#overview)
- [Input contract](#input-contract)
- [Workflow](#workflow)
- [Tax-efficient rebalancing logic](#tax-efficient-rebalancing-logic)
- [Output contract](#output-contract)
- [Guardrails](#guardrails)

## Overview

The household typically holds investments across three account types: a taxable brokerage (e.g., Fidelity), a 401k, and an HSA's invested portion. A target allocation is defined at the household level (e.g., 55/20/20/5 US/intl/bonds/cash). This skill rolls up *current* allocation across all three accounts, computes the drift from target, and proposes specific buys and sells to restore target — preferring trades inside tax-advantaged accounts (401k, HSA) where realized gains have no tax consequence.

**It never executes trades.** It produces a proposal for the user.

## Input contract

The caller provides:

- `accounts` — array of investment accounts: `{id, type, institution, holdings[]}` where each holding has `{symbol, shares, value_cents, cost_basis_cents, asset_class}`.
- `target_allocation` — `{ asset_class: target_pct }` summing to 1.0.
- `drift_threshold_pct` — default 5 percentage points (5.0). Below threshold, no rebalance proposed.
- `cash_to_deploy_cents` — optional new cash being added (e.g., a paycheck deposit).
- `tax_rate_long_term` — for cost-comparison estimates (default 15%).

## Workflow

```
Drift / Rebalance Progress:
- [ ] Step 1: Aggregate holdings by asset_class across all accounts
- [ ] Step 2: Compute current allocation percentages
- [ ] Step 3: Compute drift vs target
- [ ] Step 4: Check drift threshold; if all classes within threshold, return no-op
- [ ] Step 5: If new cash, allocate it preferentially to under-target classes
- [ ] Step 6: For remaining drift, plan trades
- [ ] Step 7: Order trades by tax cost (advantaged-account first)
- [ ] Step 8: Verify proposal nets to zero cash impact (or matches new-cash deposit)
- [ ] Step 9: Emit proposal with per-trade rationale
```

### Step 1 — Aggregate

For each `asset_class` in target, sum `value_cents` across all holdings of all accounts. Include cash positions in the brokerage (typically asset_class `cash`).

### Step 2 — Allocation

`current_pct[class] = total_value[class] / total_value_all`. Keep two decimal places.

### Step 3 — Drift

`drift_pp[class] = current_pct[class] − target_pct[class]` in percentage points.

### Step 4 — Threshold

If `max(|drift_pp|)` < `drift_threshold_pct`, emit `rebalance_needed: false` and stop. Surface drift values for context but propose no trades.

### Step 5 — Deploy new cash

If `cash_to_deploy_cents > 0`, allocate to under-target classes first. Each dollar of new cash to under-target classes reduces the trade volume needed in step 6.

Allocation order: largest negative `drift_pp` first.

### Step 6 — Plan trades

After cash deployment, residual drift calls for trades. For each over-target class, compute `excess_cents`; for each under-target class, compute `shortfall_cents`. Match by greedy pairing (largest excess to largest shortfall), producing a list of `(sell_class, buy_class, amount_cents)` swaps.

### Step 7 — Tax-efficient ordering

Within each swap, choose specific holdings:

**Sell side priority** (most preferred to least):
1. Holdings inside `401k` or `hsa` (any sale is tax-free).
2. Holdings in taxable brokerage with **unrealized loss** (sale generates harvestable loss — coordinate with `tax-loss-harvest-scanner`).
3. Holdings in taxable brokerage with **smallest unrealized gain** (least tax cost).
4. Holdings in taxable brokerage with long-term gains (taxed at 15%).
5. Holdings in taxable brokerage with short-term gains (taxed at marginal rate).

**Buy side priority**:
1. Holdings inside `401k` or `hsa` of the desired asset class (no transaction-tax friction).
2. Existing holdings in taxable brokerage of the desired asset class (avoid wash-sale by not buying back something just sold).
3. New holding (broad-market index fund preferred).

For each proposed sell from a taxable account, compute and surface the estimated tax cost: `(value − cost_basis) × tax_rate_long_term`. The user can decide whether the rebalance benefit exceeds the tax cost.

### Step 8 — Verify

The proposal must satisfy: `Σ buys = Σ sells + cash_to_deploy_cents`. If not, the planning has a bug — emit a `proposal_invalid` warning and stop.

### Step 9 — Emit

Per-trade output includes: account, symbol, action (buy/sell), shares, dollar amount, asset_class change, estimated tax cost, rationale (under-target / over-target / new cash deploy).

## Tax-efficient rebalancing logic

| Account | Sale tax cost | Notes |
|---|---|---|
| 401k | $0 | All sales tax-free |
| HSA (invested) | $0 | All sales tax-free |
| Brokerage (long-term gain) | 15% × gain | Hold > 1 year |
| Brokerage (short-term gain) | marginal income tax × gain | Hold < 1 year — usually avoid |
| Brokerage (loss) | savings (TLH benefit) | Coordinate with tax-loss-harvest-scanner |

**Wash-sale awareness.** If a sell is paired with a buy of substantially identical security within 30 days (in any account, including the spouse's), the loss is disallowed. When a rebalance proposes selling an ETF in taxable for a loss, the buy side must use a *different but similar* ETF (e.g., sell VTI, buy ITOT). Document the wash-sale guard on each trade.

**Free-money flags** — emit even when no rebalance is needed:

- 401k contribution rate < employer-match cap → `free_money_alert: missed_employer_match`.
- HSA cash balance > investment threshold but not invested → `free_money_alert: idle_hsa_cash`.

## Output contract

```json
{
  "as_of": "2026-04-25",
  "totals": {
    "portfolio_value_cents": 49250000,
    "by_account": {
      "acc_inv_fid_001": 18750000,
      "acc_401k_001": 22500000,
      "acc_hsa_001": 8000000
    }
  },
  "current_allocation": {
    "us_equity": 0.625,
    "intl_equity": 0.155,
    "us_bond": 0.180,
    "cash": 0.040
  },
  "target_allocation": {
    "us_equity": 0.55,
    "intl_equity": 0.20,
    "us_bond": 0.20,
    "cash": 0.05
  },
  "drift_pp": {
    "us_equity":  7.5,
    "intl_equity": -4.5,
    "us_bond":    -2.0,
    "cash":       -1.0
  },
  "rebalance_needed": true,
  "max_drift_pp": 7.5,
  "trades": [
    {
      "account_id": "acc_401k_001",
      "action": "sell",
      "symbol": "FXAIX",
      "asset_class": "us_equity",
      "value_cents": 1850000,
      "shares": 18.5,
      "tax_cost_cents": 0,
      "rationale": "Reduce US equity overweight using tax-advantaged account"
    },
    {
      "account_id": "acc_401k_001",
      "action": "buy",
      "symbol": "FSPSX",
      "asset_class": "intl_equity",
      "value_cents": 1850000,
      "shares": 41.0,
      "tax_cost_cents": 0,
      "rationale": "Increase intl equity to target via tax-advantaged account"
    }
  ],
  "alerts": [],
  "free_money": [
    {
      "type": "missed_employer_match",
      "account_id": "acc_401k_001",
      "current_contribution_pct": 3,
      "match_cap_pct": 4,
      "annual_dollars_left_cents": 200000,
      "action": "increase 401k contribution from 3% to 4%"
    }
  ]
}
```

## Guardrails

- **Never execute.** This skill produces proposals only.
- **Drift threshold is meaningful.** Sub-5pp drift is noise; rebalancing it generates frictional costs (taxes, transaction overhead).
- **Tax-cost transparency.** Every taxable sale carries an explicit estimated tax cost. The user must see it.
- **Wash-sale guard.** Pair sell-for-loss with a different (not substantially identical) buy. Document.
- **Whole shares only** when a holding doesn't support fractional shares — round to nearest whole share and surface the residual cash.
- **Don't auto-deploy new cash to over-target classes.** Even if it minimizes trades, it widens drift; deploy to under-target instead.
- **Account-level constraints respected.** A 401k might only offer specific funds; never propose buying a fund the account does not support. The agent layer reads the eligible-fund list per account.
