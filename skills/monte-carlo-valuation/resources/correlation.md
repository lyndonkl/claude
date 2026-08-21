# Correlation: the common-factor model and its limits

## Why it matters

Independent draws on correlated drivers produce trials that describe no possible company.
High revenue growth paired with a collapsing margin. Falling earnings paired with an
unchanged payout ratio. Every such trial dilutes the output, and they do not cancel out.

The effect is systematic, not random. When two drivers that both raise value move together,
independent sampling removes the trials where both are high and the trials where both are
low. The distribution loses both tails and the middle looks tighter than it is. When the
correlation is negative, independent sampling does the opposite and widens the range.

So a simulation with the correlations left out is not a conservative simulation. It is a
simulation of the wrong thing, and the direction of the error depends on the signs you
omitted.

## How this script does it

One shared common factor per named group. Each driver declares a `loading` on a factor:

```json
{"name": "revenue growth", "path": "revenue_growth.start",
 "distribution": {"type": "lognormal", "mean": 0.20, "sd": 0.06},
 "factor": "demand", "loading": 0.7},
{"name": "target margin", "path": "operating_margin.end",
 "distribution": {"type": "triangular", "min": 0.08, "likeliest": 0.14, "max": 0.20},
 "factor": "demand", "loading": 0.5}
```

Per trial, one standard normal `Z` is drawn for each factor. Each driver then gets its own
standard normal `e`, and its latent value is

    z_i = loading_i × Z_factor + √(1 − loading_i²) × e_i

`z_i` is still standard normal, so the driver's own distribution is untouched. Two drivers
on the same factor carry a latent correlation of `loading_i × loading_j`. In the example
above that is 0.35.

The latent normal is then pushed through the driver's inverse CDF. This is a Gaussian
copula: it preserves the rank correlation exactly and the linear correlation approximately.
For a strongly skewed shape such as a lognormal, the realized Pearson correlation comes in
slightly below the latent one. The output reports both numbers, side by side, so you can
see the difference rather than assume it away.

Check it directly with `sample`, which needs no valuation:

```bash
python3 resources/simulate.py sample --example | python3 resources/simulate.py sample
```

## Choosing loadings

Get the sign right first. The size is a second-order question, and the corpus is explicit
that the sign carries most of the information.

| Relationship | Typical signs |
|---|---|
| Revenue growth and operating margin, scale-driven business | both positive, 0.5 to 0.8 |
| Revenue growth and operating margin, price-competition business | opposite signs |
| Earnings and payout ratio | opposite signs — a bad year returns less cash |
| Earnings in consecutive years | both positive and high; Damodaran used 0.80 for the S&P 500 |
| Commodity price and margin for a producer | both positive, and often the only correlation that matters |
| Cost of capital and operating drivers | usually leave uncorrelated unless the macro factor drives both |

To hit a target pairwise correlation `ρ` between two drivers, give both a loading of `√ρ`.
For 0.5, use about 0.71 on each. For a negative pair, load one positively and the other
negatively: +0.71 and −0.71 gives −0.5.

Damodaran's published runs stay coarse on purpose. Paytm used one correlation of 0.50
between the target margin and the take rate. The S&P 500 run used 0.80 between consecutive
years of earnings and −0.50 between payout and earnings. Three numbers, all of them round.

## What one factor cannot do

The model is a simplification, and these are the places it bites.

- **Only one correlation per pair, and it factors.** With three drivers on one factor at
  loadings a, b and c, the pairwise correlations are forced to be ab, ac and bc. You cannot
  set an arbitrary correlation matrix. Correlations of 0.8, 0.8 and −0.5 among three
  drivers are not reachable.
- **Multiple factors are independent of each other.** Drivers on `demand` and drivers on
  `rates` are uncorrelated across the two groups. That is a real assumption, and for a
  company where the macro cycle drives both, it is a wrong one. Put them on one factor.
- **The correlation is constant across the range.** Real drivers often couple more tightly
  in a crisis than in normal times. A Gaussian copula has no tail dependence, so it
  understates joint disasters. For a distress case, model the disaster as a discrete
  scenario rather than trusting the tail of the copula.
- **The realized Pearson correlation drifts below the target for skewed shapes.** Read the
  `realized_correlation` field rather than assuming the loading landed.

If you need a full correlation matrix with arbitrary entries, this is not the tool. The
honest response in that situation is usually to notice that you cannot defend a full matrix
either, and to reduce the driver set until one factor is enough.

## Reporting it

Say what you correlated and why, in words, next to the percentile table. "Growth and margin
were loaded 0.7 and 0.5 on a single demand factor, giving a correlation of about 0.35,
because this business gets its margin from scale" is a claim a reader can argue with. A
correlation matrix with no story behind it is not.
