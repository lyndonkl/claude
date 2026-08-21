---
name: monte-carlo-valuation
description: Turns a point-estimate valuation into a distribution — samples the drivers you are least sure about from normal, lognormal, triangular, uniform or discrete-scenario distributions, re-runs the DCF engine on every draw, and reports percentiles, mean, standard deviation, the probability the value exceeds the market price, and the share of draws the engine refused as infeasible. Correlates drivers through a shared common factor. Use when running a Monte Carlo simulation or a probabilistic valuation, putting a range or confidence band around a value per share, asking how likely it is that a stock is under- or overvalued, valuing a commodity or cyclical company where one macro variable such as the oil price dominates, or turning a scenario grid into a probability-weighted expected value.
---

# Monte Carlo valuation

A point estimate hides how much you do not know. This skill takes a finished DCF, replaces
two or three of its drivers with probability distributions, and runs the same model
thousands of times. What comes back is a distribution of value.

That distribution answers questions a single number cannot. How wide is the plausible
range? Where does today's price sit inside it? How often does this company end up worth
nothing?

The model is not reimplemented here. Every trial calls the engine in
`dcf-valuation-engine`, so the simulation and the base case are the same code with
different inputs.

## The script

`resources/simulate.py` — pure standard library, no installation needed. JSON on stdin
(or `--in FILE`), JSON out.

```bash
python3 resources/simulate.py simulate --example      # show the input shape
python3 resources/simulate.py simulate --in run.json
python3 resources/simulate.py selftest                # verify the engine
```

| Subcommand | Turns this | Into this |
|---|---|---|
| `simulate` | a base-case DCF payload plus driver distributions | the full value distribution, percentiles, price odds, refusal counts |
| `sample` | one or more distributions on their own | the moments and percentiles of the draws, and their realized correlations |
| `scenarios` | named stories with probabilities | value per story and the probability-weighted expected value |
| `percentiles` | a list of values, or a published percentile table | percentiles, moments, and where a price sits inside them |

A seed is a required input, not an option. A valuation you cannot re-run to the same
number cannot be audited. Record the seed next to the result, and the whole run is
reproducible by anyone who has the payload.

## When a simulation is the right tool

Simulation answers "how much", not "which story". Match the tool to the doubt:

| The doubt | The tool |
|---|---|
| A narrative shift — the same business, better or worse: market size, share, margin | `simulate` with distributions |
| A narrative break — a binary event ends the story you modelled | a probability and a consequence, not a distribution. Use `failure` in the DCF engine, or `scenarios` |
| A narrative expansion — a new market that may not exist yet | a real option on top of the DCF. Use `option-valuation-toolkit` |
| Genuine doubt about which of a few named stories is true | `scenarios` |

A binary risk does not belong in a continuous distribution. Widening a growth rate cannot
represent a company that either gets a licence or does not.

## The workflow

```
Simulation progress:
- [ ] 1. Finish the base-case DCF and make it defensible on its own
- [ ] 2. Pick the two to four drivers that both matter and are genuinely uncertain
- [ ] 3. Choose a shape for each, and write down why
- [ ] 4. Set the correlations, getting the signs right
- [ ] 5. Run enough trials, with a recorded seed
- [ ] 6. Read the percentiles, the refusal share and the price position
```

### 1. Start from a finished valuation

The simulation varies the inputs of an existing model. It does not replace the model, and
it does not rescue one you do not believe. If the base case is wrong about how the business
works, every trial is wrong in the same way.

Run the base case through `dcf-valuation-engine` first and check it with
`valuation-consistency-checks`. The script refuses to simulate a base case the engine
itself rejects.

### 2. Pick the drivers

Two to four. The candidates are almost always revenue growth, the target operating margin,
the sales-to-capital ratio, and the cost of capital. For a commodity firm the list starts
with the commodity price.

Distributing everything is the standard mistake. It manufactures a wide range that carries
no information, because most inputs barely move value. Run a sensitivity grid first
(`dcf-valuation-engine sensitivity`) and distribute only the drivers that show up in it.

The opposite mistake is worse: distributing three minor inputs while holding the real
driver fixed. The output then looks precise and is not.

### 3. Choose a shape

Each driver points at a leaf of the base-case payload with a dotted path, exactly as the
sensitivity grid does.

```json
{"name": "target margin", "path": "operating_margin.end",
 "distribution": {"type": "triangular", "min": 0.08, "likeliest": 0.14, "max": 0.20}}
```

| Shape | Use it when | Parameters |
|---|---|---|
| `uniform` | you know the range and have no view inside it | `min`, `max` |
| `triangular` | you can state a worst, a likeliest and a best case | `min`, `likeliest`, `max` |
| `normal` | you have a central estimate and a symmetric error around it | `mean`, `sd` |
| `lognormal` | the variable cannot go below a floor but can run far above it | `mean`, `sd` (arithmetic), or `median` and `log_sd`; optional `shift` |
| `discrete` | the variable takes a few named values | `outcomes`: a list of `value` and `probability` |

Triangular is the workhorse, because a minimum, a likeliest and a maximum are things an
analyst can actually defend. Lognormal is right for growth rates and prices, which have a
floor and a long right tail. A normal distribution on a growth rate quietly allows revenue
to fall by more than 100%.

Check a shape before you wire it in:

```bash
echo '{"seed": 1, "trials": 20000, "distributions": [
  {"name": "growth", "distribution": {"type": "lognormal", "mean": 0.20, "sd": 0.06}}]}' \
  | python3 resources/simulate.py sample
```

A lognormal given an arithmetic mean of 20% has a median near 19.1%. That gap is the
skew, and seeing it here is better than discovering it in the output.

Full parameterization, the quantile formulas and how to calibrate each shape:
[resources/distributions.md](resources/distributions.md).

### 4. Set the correlations

Drivers that share a cause have to move together. High revenue growth with a collapsing
margin, or falling earnings with an unchanged payout, are combinations that cannot happen.
Drawing them independently produces trials that describe no possible company.

Correlation here uses one shared common factor. Give a driver a `loading` between −1 and 1
on a named factor, and two drivers on the same factor end up correlated at the product of
their loadings.

```json
{"name": "revenue growth", "path": "revenue_growth.start",
 "distribution": {"type": "lognormal", "mean": 0.20, "sd": 0.06},
 "factor": "demand", "loading": 0.7}
```

Two drivers at 0.7 and 0.5 on `demand` come out correlated at about 0.35. Opposite signs
anti-correlate, which is how the payout-against-earnings link in Damodaran's S&P 500 run
is expressed. Getting the sign right matters far more than the second decimal of the size.

The output reports the correlation you asked for next to the correlation the draws
actually produced, so you can check it landed.

**Independent sampling of correlated drivers understates the tails.** Both tails, not just
the bad one. If growth and margin really move together, the good draws are better and the
bad draws are worse than an independent run will ever show, and the middle of the
distribution looks tighter than it is. The script's own test suite confirms this: the same
two drivers loaded on one factor produce a 5th-to-95th spread more than 10% wider than the
independent version.

The one-factor model is a deliberate simplification. What it captures, what it cannot, and
when you need more:
[resources/correlation.md](resources/correlation.md).

### 5. Run it

```bash
python3 resources/simulate.py simulate --in run.json
```

Ten thousand trials settles the middle of the distribution. The 5th and 95th percentiles
need more, because tail error falls only with the square root of the trial count.
Damodaran's published Paytm run used 100,000, which takes a few seconds here.

## Reading the output

```json
"distribution": {
  "mean": 17.16, "standard_deviation": 4.14, "median": 16.84,
  "percentiles": {"5": 10.89, "10": 11.98, "25": 14.18, "50": 16.84,
                  "75": 19.68, "90": 22.55, "95": 24.35},
  "range_10_to_90": [11.98, 22.55],
  "versus_price": {"current_price": 14.0,
                   "probability_value_exceeds_price": 0.76,
                   "percentile_of_price": 24.0}
}
```

- **Quote the 10th to 90th percentile as the working range.** The minimum and maximum are
  single draws. They move every run, and they are reported under `extremes` with a note
  saying so.
- **The median is the number to lead with, not the base case.** The two differ whenever an
  input is skewed. Damodaran's Paytm simulation had a median 14% below the base-case DCF,
  and the divergence was the finding.
- **`percentile_of_price` is the decision-relevant statistic.** A price at the median means
  the market sits inside your uncertainty band and you have no edge. A price above the 90th
  percentile means you have a case worth making.
- **`probability_value_at_or_below_zero`** is the failure-like tail. Paytm's was about 3%.
- **Check `drivers`.** Each one reports the mean, standard deviation and percentiles of
  the values actually drawn. If a driver's realized 90th percentile is a number you would
  not defend in writing, fix the distribution.
- **Read the `warnings` array.** It flags independent sampling, heavy refusals, thin trial
  counts, and a median far from the base case.

The width of the distribution is a statement about your uncertainty. It is not a forecast
of where the price will trade, and it is not a target price band.

## Refused trials

Some draws describe companies that cannot exist. Terminal growth above the discount rate is
the common one; reinvestment above 100% of income is the other. The DCF engine refuses
these rather than returning a number, and the simulation counts the refusals with reasons:

```json
"refused": 162, "refused_share": 0.032,
"refusals": [{"reason": "Terminal cost of capital (0.0800) must exceed terminal growth ...",
              "count": 162, "share": 0.032}]
```

Refused trials are dropped from the distribution by default. That is not neutral. Refusals
cluster in one tail, so dropping them quietly narrows the range on that side. Treat a
refusal share above a few percent as a signal to tighten the input distributions, not as
noise to read around.

If a refused draw genuinely means the equity is worthless, say so explicitly with
`"refused_value": 0.0` and the trials enter the distribution at that value.

## Commodity and cyclical companies

This is where simulation earns its keep. When one macro variable dominates value, a point
estimate blends two opinions — your view on the company and your view on the commodity —
and no reader can tell which is doing the work.

The discipline is to value the company at today's commodity price, then state the macro
uncertainty separately as a distribution. Damodaran's Shell valuation, March 2016, is the
template:

1. Regress revenues on the commodity price. Shell: `revenues = 39,992.77 + 4,039.40 × oil
   price per barrel`, with an R-squared of 96.44% over 1989 to 2015.
2. Value the firm at the market price of oil, $40, giving $39.31 per share.
3. Simulate the steady-state oil price and the target margin. Median $36.99, with a 10th to
   90th range of $23.90 to $57.49.

The `linear_map` field does step 1 inside the simulation. It applies
`intercept + slope × draw` before writing the value into the model, so you sample the oil
price and the model receives revenue:

```json
{"name": "oil price", "path": "base_revenue",
 "distribution": {"type": "lognormal", "median": 40.0, "log_sd": 0.35},
 "linear_map": {"intercept": 39992.77, "slope": 4039.40}}
```

Normalize the margin separately. A trough margin is a point in the cycle, not the business,
and simulating around it simulates the wrong centre. Use
`financial-statement-normalization` for the long-run margin and return on capital first.

Worked runs for Shell, Amazon, Paytm and the S&P 500:
[resources/worked-examples.md](resources/worked-examples.md).

## Named scenarios instead of distributions

When the doubt is about which story is true, use discrete scenarios. Each one is a named
set of overrides with a probability, and the probabilities have to sum to 1.

```bash
python3 resources/simulate.py scenarios --example | python3 resources/simulate.py scenarios
```

The output gives value per scenario, the probability-weighted expected value, the spread
from best to worst, and the cheapest scenario that clears the market price. That last field
is the point of the exercise. Some scenario always justifies any price. The question is
never whether such a scenario exists, but whether it is probable.

Label each scenario possible, plausible or probable before you weight it. Only probable
stories belong in a base case.

## What a simulation does not do

- **It does not fix a wrong narrative.** If the story about the business is wrong, the
  simulation gives you a precise distribution of wrong answers. Model risk is not in the
  output, because the model does not vary across trials.
- **The output is a distribution of your assumptions, not of reality.** Someone chose every
  shape and every parameter. The percentile table inherits all of that judgment and none of
  the modesty.
- **It is only as good as its input distributions.** A triangular distribution with made-up
  endpoints produces a confident-looking range built on two invented numbers. Calibrate
  from the driver's own history, industry ranges and peer distributions.
- **It does not add risk.** The discount rate already carries risk. Widening the
  distributions and raising the discount rate for the same uncertainty counts it twice.
- **It does not average away a decision.** The range is not the answer. You still have to
  say which part of it you believe, and why.

## Handoffs

| You need | Where it comes from |
|---|---|
| The base-case payload | `dcf-valuation-engine value` — the same JSON goes in as `base_case` |
| Which drivers to distribute | `dcf-valuation-engine sensitivity` — distribute what moves the answer |
| The cost of capital and its range | `cost-of-capital-toolkit wacc`, read `wacc` |
| Normalized margins and returns for a cyclical | `financial-statement-normalization normalize-earnings` |
| Employee option value for the bridge | `option-valuation-toolkit employee-options`, read `value_of_options` |
| A check on the base case before simulating | `valuation-consistency-checks --dcf base_case.json` |

## Reference data

`resources/data/simulation_cases.json` holds four of Damodaran's published simulations —
Paytm 2021, Amazon 2018, Shell 2016 and the S&P 500 in November 2020 — with their input
distributions, percentile tables and findings, tagged with an `as_of` date and a refresh
note. They are calibration anchors and test vectors, not inputs to a valuation.

Each case is a snapshot of a company at a date. The market prices in particular mean
nothing outside that date, so re-read the source before quoting one in live work.

## Common failures

| Symptom | Cause |
|---|---|
| The range is enormous and says nothing | Every input was distributed, including ones that barely move value |
| The range looks tight for a genuinely uncertain company | The real driver was held fixed while minor inputs were distributed |
| Percentiles move every run | Too few trials for the tails, or the seed is being changed between runs |
| The result cannot be reproduced | The seed was not recorded alongside the output |
| Trials contain impossible combinations | Correlated drivers sampled independently; set a `loading` |
| A large share of trials refused | A distribution reaches past a hard constraint, usually terminal growth above the discount rate |
| The simulated median differs from the base case | Normal with a skewed input; quote the median and say why the two differ |
| A lognormal produces values far below what was intended | `mean` and `sd` were read as log-space parameters; they are arithmetic. Use `median` and `log_sd` for log space |
| The market price sits at the median and the result feels useless | It is the result. The market is inside your uncertainty band and you have no edge |
| A binary risk produced a strange bimodal output | A narrative break was forced into a continuous distribution; use `scenarios` or the DCF `failure` branch |
| The engine refuses the whole run | The base case itself is infeasible; fix it in `dcf-valuation-engine` first |
