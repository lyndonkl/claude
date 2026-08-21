# Distributions: parameters, formulas and calibration

Every shape in `simulate.py` is sampled through its inverse cumulative distribution
function. A uniform draw `u` in (0,1) is mapped to the value at that probability. That is
what lets the common factor drive any mix of shapes at once, and it is why the sampler is
exactly reproducible from a seed.

## Uniform

```json
{"type": "uniform", "min": 1.5, "max": 2.5}
```

    quantile(u) = min + u × (max − min)
    mean = (min + max) / 2
    standard deviation = (max − min) / √12

Use it when you know the range and genuinely have no view inside it. That is rarer than it
looks. If you would bet on the middle, you have a view, and triangular is the honest shape.

Damodaran uses uniform for the sales-to-invested-capital ratio in the Paytm run, and for
Amazon's revenue growth between 5% and 25%.

## Triangular

```json
{"type": "triangular", "min": 3.95, "likeliest": 5.95, "max": 7.95}
```

Let `c` be the likeliest value and `F(c) = (c − min) / (max − min)`.

    quantile(u) = min + √(u × (max − min) × (c − min))            for u < F(c)
    quantile(u) = max − √((1 − u) × (max − min) × (max − c))      for u ≥ F(c)
    mean = (min + likeliest + max) / 3

The workhorse. A worst case, a likeliest case and a best case are three numbers an analyst
can source and defend, and the shape handles asymmetry without further argument.

Calibrate the endpoints from something real: the range of peer margins, the high and low of
the driver's own history, the spread of analyst estimates. Endpoints picked to feel
comfortable produce a range that looks rigorous and is not.

## Normal

```json
{"type": "normal", "mean": 0.125, "sd": 0.02}
```

    quantile(u) = mean + sd × Φ⁻¹(u)

Right for a central estimate with a symmetric error, which mostly means margins and rates.
Wrong for anything with a floor. A normal on a growth rate allows revenue to fall by more
than 100%, and a normal on a price allows a negative price.

Setting `sd` to 0 is legal and produces a constant. That is useful for pinning one driver
while another varies.

## Lognormal

Two parameterizations, because analysts hold the number two different ways.

```json
{"type": "lognormal", "mean": 0.20, "sd": 0.06}
{"type": "lognormal", "median": 40.0, "log_sd": 0.35}
{"type": "lognormal", "mean": 0.0797, "sd": 0.008, "shift": 0.05}
```

With `mean` and `sd` the parameters are arithmetic — the mean and standard deviation of the
variable itself. The script converts:

    log_sd = √( ln(1 + (sd / mean)²) )
    median = mean × e^(−log_sd² / 2)
    quantile(u) = shift + median × e^(log_sd × Φ⁻¹(u))

With `median` and `log_sd` you are stating the log-space parameters directly. Use this when
you are thinking in multiplicative terms: `log_sd` of 0.35 means roughly a factor of 1.42
per standard deviation.

`shift` moves the floor. The default floor is zero. Damodaran's Amazon cost of capital was
drawn with a location of 5.00%, a mean of 7.97% and a standard deviation of 0.80%, which is
`{"mean": 0.0797, "sd": 0.008, "shift": 0.05}`. The `mean` and `sd` describe the whole
variable, including the shift.

The median always sits below the arithmetic mean. That is the skew, and it is the reason a
simulated median can land below a base case built on mean inputs.

The classic error is passing an arithmetic mean and standard deviation to a sampler that
reads them as log-space parameters. A mean of 0.20 then becomes `e^0.20 = 1.22`, and the
run is silently wrong by a factor of six. The `sample` subcommand exists to catch this in
ten seconds.

## Discrete

```json
{"type": "discrete", "outcomes": [
  {"value": 0.25, "probability": 0.30},
  {"value": 0.15, "probability": 0.50},
  {"value": 0.05, "probability": 0.20}]}
```

The cumulative distribution steps through the outcomes in the order given, so the sampler
returns the first outcome whose running probability reaches `u`. Probabilities must sum to
1 within 1e-6, and the script refuses the run otherwise.

Use it for a variable that takes a few values rather than a continuum: a regulatory
outcome, a tax regime, a licence granted or withheld. When several drivers all switch
together on the same event, that is a scenario rather than a distribution — use the
`scenarios` subcommand.

## Shapes this script does not implement

Damodaran's published runs use a couple of shapes from Crystal Ball that are not here.

**Minimum extreme** (Paytm's target operating margin, the S&P 500 earnings inputs). A
left-skewed distribution for a variable whose surprises are mostly to the downside.
Approximate it with a triangular whose `likeliest` sits nearer the maximum than the
minimum. State that you have done so.

**Beta and gamma.** Both are usually reachable by a triangular with well-chosen endpoints,
at a level of precision the underlying judgment does not support anyway.

The absence is deliberate. The gap between a triangular and a minimum-extreme distribution
is far smaller than the gap between a defensible endpoint and an invented one.

## Calibrating any shape

1. **Find the driver's own history.** The standard deviation of a company's own revenue
   growth over ten years is a better starting point than a guess.
2. **Find the industry cross-section.** Peer margins give you a defensible minimum and
   maximum for a target margin.
3. **Ask what the endpoints imply.** A maximum revenue growth rate implies a market share.
   If that share is implausible, the endpoint is wrong.
4. **Check the realized percentiles in the output.** Each driver reports its drawn 10th,
   50th and 90th percentiles. Read them as statements and see whether you would sign them.
5. **Do not widen a distribution to express risk.** Risk is in the discount rate. The
   distribution expresses what you do not know about the driver.
