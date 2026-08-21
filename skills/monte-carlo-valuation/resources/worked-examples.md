# Worked examples

Four of Damodaran's published simulations, with the commands that reproduce the parts this
script can reproduce. The published inputs, percentile tables and findings are bundled in
`data/simulation_cases.json`.

A note on fidelity. His runs use Crystal Ball on his own spreadsheets, which reinvest
through explicit capital expenditure and depreciation and offer distribution shapes this
script does not implement. The DCF engine here reinvests through a sales-to-capital ratio.
So the runs below are adaptations. They land close, and where they differ the difference is
stated.

---

## 1. Shell, March 2016 — one macro variable dominates

The archetype. An oil company's value is mostly a view on oil, so the discipline is to
value it at today's oil price and express the macro uncertainty separately.

**The link.** Revenues regressed on the annual average oil price, 1989 to 2015:

    revenues ($m) = 39,992.77 + 4,039.40 × oil price per barrel        R² = 96.44%

At $40 a barrel that is $201,569m. An R² of 96.44% means the oil price essentially is the
revenue model, which is exactly why simulating it is worth doing.

**The base case.** Margin converging from a 3.01% trough to the 9.35% long-run average over
five years, revenue growth 3.91%, tax 30%, cost of capital 9.91% falling to 8.00%, terminal
growth 2%, terminal return on capital 12.37%.

```json
{
  "base_revenue": 201568.77, "base_invested_capital": 240000.0, "forecast_years": 5,
  "revenue_growth": 0.0391,
  "operating_margin": {"start": 0.0301, "end": 0.0935, "converge_by": 5},
  "sales_to_capital": 1.5, "tax_rate": 0.30, "cost_of_capital": 0.0991,
  "terminal": {"growth_rate": 0.02, "cost_of_capital": 0.08, "return_on_capital": 0.1237},
  "bridge": {"debt": 58379.0, "cash": 31752.0, "minority_interests": 1245.0,
             "non_operating_assets": 33566.0, "shares_outstanding": 4209.7},
  "currency": "USD"
}
```

The sales-to-capital ratio of 1.5 stands in for Damodaran's explicit cap ex and
depreciation. It reproduces his net reinvestment closely, and the base case comes out at
**$39.47** against his published **$39.31** — a 0.4% gap. Note the cross holdings of
$33,566m in `non_operating_assets` and the minority interests of $1,245m. Skipping either
is a large error in a group company.

**The simulation.** Two drivers, correlated, because a higher oil price lifts the margin
too:

```json
{"seed": 20160331, "trials": 20000, "base_case": {"...": "as above"},
 "drivers": [
   {"name": "oil price", "path": "base_revenue",
    "distribution": {"type": "lognormal", "median": 40.0, "log_sd": 0.35},
    "linear_map": {"intercept": 39992.77, "slope": 4039.40},
    "factor": "oil", "loading": 0.9},
   {"name": "target operating margin", "path": "operating_margin.end",
    "distribution": {"type": "normal", "mean": 0.0935, "sd": 0.015},
    "factor": "oil", "loading": 0.5}]}
```

Everything else is held fixed, as in the source. Result:

| | This run | Damodaran |
|---|---|---|
| Base case | $39.47 | $39.31 |
| Median | $39.19 | $36.99 |
| Mean | $42.19 | — |
| 10th percentile | $24.20 | $23.90 |
| 90th percentile | $63.80 | $57.49 |

The lower tail matches almost exactly. The upper tail here is fatter, because a lognormal
with `log_sd` 0.35 is more generous about a $100 oil price than his right-skewed shape was.
That is a calibration choice, and it is the kind of choice a reader should be told about.

The `before_map` block in the driver report gives the oil price actually drawn: a median of
$39.93 with a 10th-to-90th range of $25.43 to $62.51. Those are the numbers to argue about.
If that range is not your view of oil, change it and re-run — which is the whole point of
keeping the macro out of the micro.

---

## 2. Amazon, September 2018 — where the price sits

The published inputs are four.

| Driver | Shape | Correlation |
|---|---|---|
| Revenue growth | uniform, 5% to 25% | +0.40 with the operating margin |
| Operating margin | normal, mean 12.50%, standard deviation 2.00% | — |
| Sales to invested capital | triangular, minimum 3.95, likeliest 5.95, maximum 7.95 | — |
| Cost of capital | lognormal, location 5.00%, mean 7.97%, standard deviation 0.80% | — |

In this script's parameterization those are:

```json
[{"name": "revenue growth", "path": "revenue_growth",
  "distribution": {"type": "uniform", "min": 0.05, "max": 0.25},
  "factor": "demand", "loading": 0.63},
 {"name": "operating margin", "path": "operating_margin.end",
  "distribution": {"type": "normal", "mean": 0.125, "sd": 0.02},
  "factor": "demand", "loading": 0.63},
 {"name": "sales to capital", "path": "sales_to_capital",
  "distribution": {"type": "triangular", "min": 3.95, "likeliest": 5.95, "max": 7.95}},
 {"name": "cost of capital", "path": "cost_of_capital",
  "distribution": {"type": "lognormal", "mean": 0.0797, "sd": 0.008, "shift": 0.05}}]
```

Loadings of 0.63 on both give a pairwise correlation of about 0.40, which is the published
figure. See [correlation.md](correlation.md) for why `√ρ` is the loading to use.

The growth path here is a single compounded rate, so `revenue_growth` in the base case is a
number and the driver points straight at it. When the base case uses a glide instead, point
at `revenue_growth.start` or `revenue_growth.end`.

**The output, and how to read it.** Base case $1,255.09, simulated mean $1,343.67, median
$1,241.98, against a market price of $1,970. Locate the price in the published table:

```bash
python3 resources/simulate.py percentiles --example | python3 resources/simulate.py percentiles
```

Feeding Amazon's table gives a price at the **84.2nd percentile**, so the value exceeds the
price in about 16% of trials. The source describes this as the 85th to 90th percentile.
Either way the conclusion is the same, and it is more useful than "overvalued": Amazon was
overvalued in most scenarios, not in all of them. A stock overvalued at the median but
undervalued in the top decile is a different proposition from one overvalued everywhere.

Note also that the mean sits above the median. That is the lognormal cost of capital and
the uniform growth rate working on the output, and it is why the median is the number to
quote.

---

## 3. Paytm, September 2021 — the median is not the base case

Four drivers, 100,000 trials, valued ahead of the IPO:

- GMV growth rate, years 1 to 5: lognormal.
- Target take rate (revenue over GMV), year 10: triangular.
- Target operating margin, year 10: minimum extreme, correlated 0.50 with the take rate.
- Sales to invested capital, years 2 to 10: uniform.

The minimum-extreme shape is not implemented here. Approximate it with a triangular whose
`likeliest` sits nearer the maximum than the minimum, and say that you have.

**The finding.** Base-case DCF equity value ₹1,456,708m. Simulated median ₹1,246,824m —
14% lower. The 10th to 90th percentile range ran from ₹627,263m to ₹2,010,052m, and equity
was worth nothing in about 3% of trials.

The base case is one draw from a very broad distribution. It is not the centre of that
distribution, and skew is the reason. Report the median, report the range, and report the
share of trials in which the equity is worthless.

The ₹−2,242,001m entry at the 0th percentile is a single draw and an artefact. Quoting it
as the downside would be a misreading of the run.

---

## 4. S&P 500, 1 November 2020 — a macro object, and two signed correlations

The same machinery pointed at an index rather than a company. Inputs:

| Driver | Shape | Correlation |
|---|---|---|
| 2020 earnings | likeliest 130.2, scale 6 | — |
| 2021 earnings | likeliest 166.2, scale 8 | +0.80 with 2020 earnings |
| Share of lost earnings recouped by 2024 | triangular, 60% to 100% | — |
| Equity risk premium | expected value 5.58%, relative standard deviation 15% | — |
| Cash returned as a percent of earnings, 2020 | likeliest 75.00%, scale 5% | −0.50 with earnings |

Two correlations, both of them signed by a causal story. Earnings in consecutive years move
together. Payout moves against an earnings shortfall, because a bad year returns less cash.
Neither number is precise, and neither needs to be.

To reproduce the signs here, put earnings and payout on one factor with opposite loadings:
`+0.89` on earnings and `−0.56` on payout gives about −0.50.

**The finding.** The index traded at 3,270. Running the published table through
`percentiles` puts that at the **76.4th percentile**, so the simulated value exceeded the
price in about 24% of trials. The market was at the upper-middle of the plausible range,
not obviously wrong.

That is the most common honest outcome of a simulation, and it is worth saying out loud. A
price inside your uncertainty band means you have no edge. The simulation earned its keep
by telling you that, rather than by producing a trade.

---

## Reading these together

The four cases cover the four reasons to run a simulation.

- **Shell**: one macro variable dominates, so separate it from the company view.
- **Amazon**: the price is far from your value, and you need to know how far in probability
  terms rather than in dollars.
- **Paytm**: the inputs are skewed, so the base case is not the centre and the downside tail
  matters.
- **S&P 500**: the drivers are causally linked, so the correlation signs carry the result.

In all four, the deterministic part is the mechanics. The judgment is which drivers get
distributions, what shape each one takes, what its parameters are, and what moves with
what. The output inherits that judgment completely.
