---
name: household-finance-dashboard-builder
description: Generates a single self-contained static HTML dashboard for a household finance JSON store, with embedded D3.js, inlined data, and six standard panels (net worth over time, monthly cash flow, recurring & subscriptions, goals progress, asset allocation, vigilance feed). Applies cognitive-design principles for visual hierarchy and visual-storytelling-design for narrative annotations. Use when emitting a weekly or monthly finance dashboard, or when user mentions weekly dashboard, household dashboard, finance HTML report, or static dashboard.
---

# Household Finance Dashboard Builder

## Table of Contents
- [Overview](#overview)
- [Output shape](#output-shape)
- [Input contract](#input-contract)
- [Workflow](#workflow)
- [The six panels](#the-six-panels)
- [Cognitive principles applied](#cognitive-principles-applied)
- [Storytelling overlay](#storytelling-overlay)
- [HTML scaffold](#html-scaffold)
- [Guardrails](#guardrails)

## Overview

This is the static-output cousin of the more general `d3-visualization` skill. It produces a single self-contained HTML file that opens in any browser without a server, with all data and chart code inlined. The dashboard is designed to be regenerated weekly from the household's JSON data store and committed to `reports/dashboards/YYYY-MM-DD-weekly.html`.

The skill assumes a JSON store conforming to the household-finance schema (accounts, transactions, balances, recurring, goals, investments, mortgage, alerts).

## Output shape

A **single HTML file** containing:
- Inline `<style>` block (no external CSS).
- Inline data block: `<script id="dashboard-data" type="application/json">{...}</script>`.
- D3 v7 vendored inline (or via a single `<script>` tag with integrity hash if offline-rendering is acceptable).
- Six panels rendered in CSS Grid.
- A short narrative header generated via `visual-storytelling-design`.
- A footer with generation timestamp and source data versions.

File size target: < 1 MB. If the data exceeds this, downsample time-series before embedding (daily → weekly aggregation is usually enough).

## Input contract

The caller provides:

- `data_root` — path to the household-finance `data/` directory.
- `output_path` — where to write the HTML.
- `generated_for` — `weekly` or `monthly` (changes the time scope and headline).
- `as_of` — ISO date for the snapshot.
- `prior_snapshot_path` (optional) — a previous dashboard's data block for week-over-week deltas.

The skill reads:
- `accounts.json`
- `balances.json`
- `transactions.json` (filtered to relevant window)
- `recurring.json`
- `goals.json`
- `investments.json`
- `mortgage.json`
- recent files in `reports/alerts/`
- the most recent `reports/monthly/*.json` for narrative context.

## Workflow

```
Dashboard Build Progress:
- [ ] Step 1: Read data; validate completeness; compute snapshot
- [ ] Step 2: Compute the six panel datasets
- [ ] Step 3: Apply cognitive-design principles to layout choices
- [ ] Step 4: Generate narrative header via visual-storytelling-design
- [ ] Step 5: Render HTML scaffold + inline data + D3 code per panel
- [ ] Step 6: Run cognitive-fallacies-guard self-check on charts
- [ ] Step 7: Write to output_path; emit data quality footer
```

### Step 1 — Snapshot

Compute the headline numbers:
- `net_worth_cents` — sum of cash + invested + home equity estimate − liabilities (mortgage + other).
- `delta_vs_prior_cents` — vs. the prior snapshot if available.
- `month_to_date_spend_cents`, `month_to_date_income_cents`, `month_to_date_savings_rate`.
- `goals_on_track`, `goals_behind`, `goals_ahead` counts.
- `alerts_open` count.

If any required file is missing, fall back gracefully: hide that panel and surface a `data_gap` line in the footer.

### Step 2 — Panel datasets

Compute exactly the data each panel needs (see [The six panels](#the-six-panels)). Keep arrays small — pre-aggregate to the resolution the chart needs.

### Step 3 — Cognitive principles

Apply these defaults (delegate detailed reasoning to `cognitive-design`):

- **Visual hierarchy.** The single most important number on the page is the net-worth delta. Render it largest, top-left.
- **Chunking.** Six panels organized into 3×2 grid; each panel has a single insight.
- **Encoding hierarchy.** Position > length > slope > area > color hue (per Cleveland & McGill). Use position for comparison panels; reserve color for categorical encoding only.
- **Working memory.** No panel asks the user to compare more than 7 things. Aggregate small categories into "Other."
- **Recognition over recall.** Label every series directly on the chart. No legend-only encodings.

### Step 4 — Narrative header

Invoke `visual-storytelling-design` to generate a 3–5 line narrative:
- Lead with the insight, not the topic ("Net worth grew $4,200 this week, driven by 401k contributions and equity gains" not "Weekly Update").
- One sentence of context (vs prior week / month / year).
- One sentence flagging anything that needs attention from the alerts feed.

### Step 5 — Render

Build the HTML scaffold (see [HTML scaffold](#html-scaffold)). Inline:
- The data block.
- A small D3 v7 bundle (or external CDN with integrity hash).
- One `renderPanel*()` function per panel.

Each render function follows the standard D3 data-join pattern from `d3-visualization`.

### Step 6 — Self-check

Before writing, run a `cognitive-fallacies-guard` pass on the rendered SVGs (or their data + axis configurations):
- No truncated axes that exaggerate change.
- No 3D effects.
- Donut chart: total displayed inside.
- Pie / donut: max 6 slices, rest aggregated.
- Time-series: include zero baseline UNLESS doing so hides the signal — in which case annotate the baseline change explicitly.

If the self-check finds issues, fix and re-render.

### Step 7 — Write

Write to `output_path`. Emit a footer with generation timestamp, schema version, last-drop date, and any data gaps.

## The six panels

### Panel 1 — Net worth over time

**Data**: monthly net worth points from `balances.json` + `investments.json` + `mortgage.json` (current_principal as liability) + home equity estimate (home value - current_principal).

**Chart**: line chart with annotated key events (mortgage origination, large contributions, market dislocations). Y-axis starts at 0 (this is a net-worth scale where 0 matters); X-axis covers the full history.

**Headline annotation**: latest value + delta vs prior snapshot.

### Panel 2 — Monthly cash flow

**Data**: per-month income (positive bars) and spending (negative bars) over the trailing 12 months, with a line showing the rolling 6-month savings rate.

**Chart**: diverging bar chart (income up, spending down) with savings-rate line overlay. Color: muted teal for income, muted coral for spending.

**Drill-down (optional, hover)**: top 5 spending categories for the latest month.

### Panel 3 — Recurring & subscriptions

**Data**: every active row from `recurring.json`, sorted by `annualized_cost_cents` descending.

**Chart**: horizontal bar chart of the top 15 by annualized cost. Each bar labeled with merchant + cadence + monthly equivalent.

**Annotation**: total annualized cost across all active recurring at the top. Highlight any with `status: suspected_dormant` or amount-changed events.

### Panel 4 — Goals progress

**Data**: every entry in `goals.json` with `current_cents`, `target_cents`, `target_date`.

**Chart**: horizontal stacked bar — completed vs. remaining — one row per goal. Annotate "On track / Behind / Ahead" per goal based on linear pacing to target date.

**Headline**: "X of Y goals on track."

### Panel 5 — Asset allocation

**Data**: aggregated holdings by `asset_class` from `investments.json` (across taxable + 401k + HSA), plus the target allocation.

**Chart**: two donuts side by side (current vs target) OR a single donut with a target ring overlay. Label each slice directly with asset class + percentage.

**Annotation**: max drift in percentage points; flag if > 5pp.

### Panel 6 — Vigilance feed

**Data**: most recent 10 entries from `reports/alerts/`, severity-tagged.

**Chart**: a styled list — not a chart. Each entry: severity badge + one-line evidence + suggested action.

This panel is intentionally text-heavy. The dashboard is informational *and* operational; the user should be able to scan it and find things to do.

## Cognitive principles applied

| Principle | Application in this dashboard |
|---|---|
| Pre-attentive attributes | Severity badges in the vigilance panel use color hue; everything else uses position |
| Gestalt proximity | Each panel is bounded with whitespace, then a thin border, then a header |
| Gestalt similarity | All numeric labels use the same monospaced font; all charts use the same axis style |
| Reading order (F-pattern) | Net worth top-left; vigilance bottom-right (the actionable end of the read) |
| Working memory | Max 6 categories per chart; rest aggregated |
| Recognition over recall | Direct labeling — no legend-only charts |
| Data-ink ratio | No 3D, no chartjunk, no decorative gradients |
| Mental models | Cash flow chart uses the universally-recognized green-up/red-down convention |

## Storytelling overlay

The narrative header follows: **Context → Change → Drivers → What needs attention.**

Example:

> **Net worth $1,247,300 — up $4,200 this week.** The increase came mostly from a $3,800 401k contribution and a small market gain in your taxable brokerage. Spending was steady at $7,840 month-to-date, slightly under your $8,500 target. **One thing to watch**: your portfolio drifted to 62.5% US equity, 7.5pp above your 55% target — a rebalance proposal is queued in this week's alerts.

## HTML scaffold

```
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Household Finance — [date]</title>
  <style>
    /* layout: 3x2 grid; max-width 1280px; light theme */
    /* typography: Inter for text, JetBrains Mono for numbers */
    /* colors: muted, accessible, single accent for "needs attention" */
  </style>
</head>
<body>
  <header>
    <h1 class="net-worth-headline">$<!-- net worth --></h1>
    <p class="net-worth-delta">[+/-]$<!-- delta --> this <!-- week|month --></p>
    <p class="narrative">[generated narrative]</p>
  </header>

  <main class="grid">
    <section id="panel-net-worth"></section>
    <section id="panel-cash-flow"></section>
    <section id="panel-recurring"></section>
    <section id="panel-goals"></section>
    <section id="panel-allocation"></section>
    <section id="panel-vigilance"></section>
  </main>

  <footer>
    <p>Generated [timestamp] from data/ as of [last-drop-date]. Schema version [X].</p>
    <p>Data gaps: [if any].</p>
  </footer>

  <script id="dashboard-data" type="application/json">
    { /* inlined data */ }
  </script>
  <script src="https://cdn.jsdelivr.net/npm/d3@7" integrity="sha384-..." crossorigin></script>
  <script>
    /* renderPanelNetWorth(), renderPanelCashFlow(), renderPanelRecurring(),
       renderPanelGoals(), renderPanelAllocation(), renderPanelVigilance() */
  </script>
</body>
</html>
```

For full offline use, vendor D3 inline rather than via CDN. The dashboard agent decides per-environment.

## Guardrails

- **Self-contained file.** No external data fetches. The user can email the file or save to disk and it still works.
- **Honest charts.** Zero baselines on bar charts; no truncated y-axes; no 3D; no chartjunk.
- **Privacy.** This dashboard contains the household's finances — embed account masks (`****1234`), never full account numbers. No SSNs, no full names where masks suffice.
- **Reproducibility.** Same input data + same generation date should produce byte-identical HTML (modulo timestamp). Sort all arrays deterministically before rendering.
- **Performance.** Down-sample series so the file stays under 1 MB. The dashboard renders in < 200ms on a typical laptop.
- **Accessibility.** All charts have title + summary `aria-labels`; tabular data alternative for each chart accessible via a "Show data" toggle.
- **Mobile-friendly.** Grid collapses to single column under 768px width; font sizes scale.
- **Versioning.** Footer carries the schema version and the generation script version so future regenerations are traceable.
