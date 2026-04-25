---
name: category-trend-analyzer
description: For each spending category, computes current-period spend, 6-month rolling average, year-over-year delta, and budget variance, then flags categories that are outliers (>1.5x rolling average or >130% of budget). Produces a ranked list of categories that grew, shrank, or stayed flat, plus the top transactions driving each outlier. Use for monthly spending reviews, identifying lifestyle creep, evaluating budget adherence, or when user mentions category trends, spending changes, budget variance, or outlier spend.
---

# Category Trend Analyzer

## Table of Contents
- [Overview](#overview)
- [Input contract](#input-contract)
- [Workflow](#workflow)
- [Outlier rules](#outlier-rules)
- [Output contract](#output-contract)
- [Guardrails](#guardrails)

## Overview

The point of categorizing transactions is to see, every month, what changed. This skill computes the comparative numbers — current vs. rolling, current vs. budget, current vs. same-month-last-year — for every category, identifies outliers, and surfaces the transactions that drive them. It refuses to flag noise: small categories below a materiality floor are excluded.

## Input contract

The caller provides:

- `transactions` — at least 13 months of categorized transactions.
- `budget` — `budget.json` with target per category.
- `period_start`, `period_end` — the current period (typically a calendar month).
- `materiality_floor_cents` — default `5000` ($50). Categories with current spend below this are summarized but not flagged.
- `outlier_thresholds` — defaults: `{ rolling_multiple: 1.5, budget_pct: 130 }`.

## Workflow

```
Trend Analysis Progress:
- [ ] Step 1: Roll up transactions by category for the current period
- [ ] Step 2: Roll up the prior 6 calendar months by category
- [ ] Step 3: Roll up the same-month-last-year by category
- [ ] Step 4: Compute deltas and percent changes
- [ ] Step 5: Apply outlier rules
- [ ] Step 6: Identify driver transactions for each outlier
- [ ] Step 7: Emit ranked list and totals
```

### Step 1 — Current period totals

For each `category` and `category.subcategory`, sum spend (negative `amount_cents`) over `[period_start, period_end]`. Exclude:
- `income.*`
- `savings_investment.*`
- `financial.transfers_internal`

These are not spending. They're tracked separately for the cash-flow and savings views.

### Step 2 — Rolling 6-month average

For each category, sum spend in each of the prior 6 calendar months, then take the mean. Use **calendar month** anchoring, not trailing 180 days, so a "monthly" comparison matches user intuition.

If fewer than 3 prior months exist, mark `rolling_avg_confidence: low` and only flag outliers above the budget threshold (skip the rolling-multiple test).

### Step 3 — Year-over-year

Sum the same calendar month, one year prior. If absent (less than a year of data), set `yoy_delta_cents: null`.

### Step 4 — Compute deltas

| Metric | Formula |
|---|---|
| `vs_rolling_pct` | `(current − rolling_avg) / rolling_avg × 100` |
| `vs_budget_pct` | `current / budget × 100` (only if budget exists) |
| `vs_yoy_pct` | `(current − yoy) / yoy × 100` |

### Step 5 — Outlier rules

A category is an outlier when **any** of:

- `vs_rolling_pct ≥ (rolling_multiple − 1) × 100` (default ≥ 50% above 6-month average) AND `current_cents ≥ materiality_floor_cents`.
- `vs_budget_pct ≥ budget_pct` (default ≥ 130% of budget) AND budget exists.
- `current_cents ≥ 2 × rolling_avg_cents` AND `current_cents ≥ materiality_floor_cents` → severity `high` (real-time alert per the spending-analyst spec).

Each outlier carries:
- `severity` — `high` (≥ 2× rolling), `medium` (≥ 1.5× rolling or ≥ 130% budget), `low` (above materiality but inside thresholds — surfaced for context only).
- `reason` — which rule fired.

### Step 6 — Drivers

For each outlier, identify the top 3–5 transactions ranked by absolute amount, descending. These are the "what drove the outlier" lines for the briefing.

If a single transaction explains > 60% of the outlier, mark it `single_driver: true` so the analyst can phrase the explanation correctly ("you spent $850 at IKEA — one trip — vs. average of $120 in home maintenance").

### Step 7 — Ranking

Rank outliers by `dollar_impact_cents = |current_cents − rolling_avg_cents|`. Largest dollar movers first; small-percentage-large-dollar matters more than large-percentage-small-dollar.

## Outlier rules

Concrete examples:

| Current | Rolling 6mo avg | Budget | Outcome |
|---|---|---|---|
| $1,200 groceries | $850 | $900 | medium — 1.41× rolling, 133% of budget |
| $3,400 travel | $300 | $400 | high — 11.3× rolling, but materiality satisfied |
| $42 hobbies | $20 | $30 | not flagged (below materiality $50) |
| $850 home maintenance | $120 | $150 | high — 7.1× rolling, single-driver IKEA trip |
| $1,800 restaurants | $1,200 | — | medium — 1.5× rolling, no budget set |
| $3,200 utilities (Aug) | $2,100 | $2,400 | medium — heat wave, 1.5× rolling, 133% of budget; YoY +5% so seasonal not lifestyle |

## Output contract

```json
{
  "period": { "start": "2026-04-01", "end": "2026-04-30" },
  "totals": {
    "spend_cents": 624800,
    "spend_cents_vs_rolling": 78400,
    "spend_cents_vs_budget": -25200,
    "categories_above_floor": 18,
    "outliers_count": 3
  },
  "categories": [
    {
      "category": "food",
      "subcategory": "groceries",
      "current_cents": 102000,
      "rolling_avg_cents": 85000,
      "yoy_cents": 92000,
      "budget_cents": 90000,
      "vs_rolling_pct": 20.0,
      "vs_budget_pct": 113.3,
      "vs_yoy_pct": 10.9,
      "severity": "low",
      "outlier": false
    },
    {
      "category": "travel",
      "subcategory": null,
      "current_cents": 340000,
      "rolling_avg_cents": 30000,
      "yoy_cents": 18000,
      "budget_cents": 40000,
      "vs_rolling_pct": 1033.3,
      "vs_budget_pct": 850.0,
      "vs_yoy_pct": 1788.9,
      "severity": "high",
      "outlier": true,
      "reasons": ["above_rolling_multiple_2x", "above_budget_threshold"],
      "drivers": [
        { "tx_id": "tx_20260408_002", "amount_cents": -312000,
          "merchant": "Delta Air Lines", "single_driver": true,
          "share_of_outlier_pct": 91.8 }
      ]
    }
  ],
  "rankings": {
    "biggest_growers": ["travel", "home_maintenance", "restaurants"],
    "biggest_shrinkers": ["entertainment", "transportation.gas"]
  }
}
```

## Guardrails

- **Materiality first.** Don't flag a $20 hobbies overage. The user's attention is the scarcest resource.
- **Don't double-count subcategories and parents.** Choose a level — top-level for the headline, subcategory for the drill-down. The spending-analyst agent decides which to show.
- **Annual lumpy categories** (`auto_insurance`, `property_tax`, `home_insurance`) routinely trigger 10×+ outliers in their billing month. Skip flagging when the spike matches the merchant's annual cadence in `recurring.json`. Use the seasonal-calendar sub-signal from the spending-analyst agent.
- **Negative outliers are not always bad.** A category that drops to zero may signal a missed bill (utility autopay broken). Flag both directions, but with different framing.
- **Do not classify the cause** in this skill ("she got a raise" / "kid started camp"). Surface the data; the analyst agent provides the narrative.
