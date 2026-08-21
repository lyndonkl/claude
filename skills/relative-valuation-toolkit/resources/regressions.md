# Pricing regressions: fitting, reading and the bundled library

Reference for step 4 of the four-step framework, and for the distribution tables step 2
needs.

## What the regression does

A peer comparison works when the firms differ on nothing. Story telling works when they
differ on one thing. Once they differ on several, the only honest control is statistical:
regress the multiple on its companion variables across the sample, then compare each
firm's actual multiple with the multiple the fitted line predicts for it.

```
under/over valuation = actual multiple / predicted multiple - 1
```

Negative means the firm trades below the sample's own pricing rule. That is a relative
verdict against the sample you chose, not an absolute one.

## Fitting: `regress`

```json
{
  "scope": "sector",
  "dependent": "PBV",
  "predictors": ["ROE", "stdev"],
  "log_predictors": [],
  "intercept": true,
  "observations": [{"name": "Barclays", "PBV": 2.23, "ROE": 0.2116, "stdev": 0.2073}]
}
```

- `dependent` and `predictors` are field names that must appear in every observation,
  spelled identically. Observations missing any field are dropped and listed under
  `firms_skipped`.
- `log_predictors` replaces a column with its natural log. Use it for growth in a PEG
  regression: R-squared on raw growth is 0.022 against 0.053 on ln(growth).
- `intercept: false` fits through the origin. Use it only as the negative-intercept fix.
- `scope` is `sector` or `market` and only changes which cautions come back.
- Add a `region` field to observations and the engine warns when the sample pools markets.

The engine solves the normal equations `X'X b = X'y` by Gauss-Jordan elimination with
partial pivoting, and inverts `X'X` in the same pass because the standard errors are the
square roots of the diagonal of `sigma-squared (X'X)` inverse. It returns coefficients,
standard errors, t-statistics, R-squared, adjusted R-squared, the standard error of the
regression, fitted values, residuals, and the pairwise correlation of every predictor pair.

Enter every predictor as a decimal. The normal equations lose precision when columns sit
on wildly different scales, and mixed units are the most common reason a published
equation returns a nonsense number.

## Reading the output

**t-statistics.** Above 2, the variable is doing real work. Between 1 and 2, marginal.
Below 1, noise — drop it and re-run, even when theory says it belongs. In pricing the
market decides what matters. Dropping the insignificant beta from the January 2021 US PE
regression moved R-squared from 0.396 to only 0.389.

**R-squared.** Below about 15% the sample is not priced on those fundamentals and the
prediction is weak evidence. Say so rather than pushing it. For calibration, January 2021
regional fits ran from 10.3% (Japan EV/EBITDA) to 62.8% (emerging-market EV/IC).

**Signs.** Check them against theory before anything else. PE should rise with growth and
payout. PBV should rise with ROE. EV/Sales should rise with the operating margin. EV/IC
should rise with ROIC and fall with the debt ratio. A wrong sign is almost always
multicollinearity, not a discovery.

## The four things that go wrong

**Negative intercept.** A fitted line with a negative constant hands a firm with weak
fundamentals a negative predicted multiple, which is meaningless. The engine refuses to
report an over/under percentage against it. The imperfect fix is `intercept: false`, which
forces the line through a point no firm occupies. The 2019 US PE regression through the
origin is bundled as `us_pe_2019_through_origin`.

**Multicollinearity between growth and risk.** The predictors overlap. In the January 2021
US cross-section, payout and expected growth correlated at -0.220, growth and beta at
-0.093, payout and beta at +0.080 — all statistically significant. High-growth firms pay
out less and often carry more risk. Individual coefficients become unstable and can flip
sign. The engine flags any pair above 0.5 in absolute value. When it fires, read the
prediction and ignore the individual coefficients.

**Small samples.** A 15 to 30 firm sector cannot support many predictors. The engine warns
below ten observations per coefficient and again below 30 observations in total. The
European bank regression here has 18 firms and three coefficients; it reproduces the
source exactly and is still fragile. Sector coefficients move violently between vintages:
the US grocery price-to-sales fit went from R-squared 0.595 in 2007 to 0.291 in 2015 while
the slope moved from 10.49 to 8.50.

**Comparing across markets.** Country PE levels are driven by interest rates, real growth
and country risk, exactly as firm multiples are driven by firm fundamentals. Pooling
markets into one regression attributes those country differences to the firm-level
predictors. Fit each market separately, or add region dummies. The engine warns when
observations carry more than one `region`.

## Predicting: `predict`

Three ways to supply the equation.

| Field | Meaning |
|---|---|
| `observations` | fit the sample first, then predict; omit `subject` to predict every firm |
| `equation` | your own coefficients, keyed by predictor name, plus `intercept` |
| `library` | a bundled published regression, by key |

`subject` takes one firm, `subjects` takes several. Add `actual` to any subject to get the
over/under percentage. When the equation predicts a non-positive multiple, the row comes
back refused with the reason rather than with a number.

## The bundled library

`resources/data/published_regressions.json`, `as_of` January 2021 unless the entry says
otherwise. Every entry carries its own `units`, `definition`, `r_squared` and `cautions`.

| Family | Keys |
|---|---|
| PE, market-wide US | `us_pe_jan2021`, `us_pe_jan2021_with_beta`, `us_pe_2019_through_origin` |
| PE, regional | `europe_pe_jan2021`, `japan_pe_jan2021`, `em_pe_jan2021`, `anzc_pe_jan2021`, `global_pe_jan2021` |
| PEG | `us_peg_jan2021` |
| PBV | `us_pbv_jan2021`, `europe_pbv_jan2021`, `japan_pbv_jan2021`, `em_pbv_jan2021`, `anzc_pbv_jan2021`, `global_pbv_jan2021` |
| EV/EBITDA | `us_ev_ebitda_jan2021` and the same five regions |
| EV/Sales | `us_ev_sales_jan2021` and the same five regions |
| EV/IC | `us_ev_ic_jan2021` and the same five regions |
| Whole markets | `country_pe_2000`, `sp500_earnings_yield_1960_2020` |
| Sector examples | `us_grocery_ps_2007`, `us_grocery_ps_2010`, `us_grocery_ps_2015`, `internet_ps_2000` |

Two unit conventions live in this file. Most entries take decimals. `us_peg_jan2021` and
`us_pe_2019_through_origin` reproduce statistics-package output in which payout and growth
are absolute percentages. Read the `units` field before every use.

These coefficients are a snapshot. The US price of an extra percentage point of expected
growth ranged from 0.41 in January 2012 to 2.62 in January 2003. Refresh from
`https://pages.stern.nyu.edu/~adamodar/` annually and record which vintage a valuation
used.

## Worked examples the engine reproduces

**European banks, PBV on ROE and risk.** Fitting the 18-bank sample gives
`PBV = 2.271 + 3.622 ROE - 2.689 stdev`, t-statistics 5.55, 3.30 and -2.33, adjusted
R-squared 0.794. The source reports 2.27, 3.63 and -2.68 with an R-squared of 79%. Royal
Bank of Scotland's predicted PBV is 2.51 against a traded 2.09, so it sits 16.65% below
the line — the most undervalued name in the sample. HSBC sits 21.91% above it.

**Telebras, telecom PE on growth and an emerging-market dummy.**
`PE = 13.1151 + 121.223 growth - 13.8531 emerging` predicts 8.35 for growth of 7.5% in an
emerging market. Telebras traded at 8.9, so it was 6.6% expensive despite having one of
the two lowest PEs in global telecom. A low multiple is not the same as cheap.

**Disney, market-wide US PE.** `us_pe_jan2021` with payout 20% and growth 15% predicts
43.6 against a traded 35. Run the same firm through the January 2020 equation and it comes
out roughly fair. Same company, same method, different year, different verdict.

**A European industrial, EV/IC.** `europe_ev_ic_jan2021` with ROIC 14%, debt ratio 25% and
revenue growth 4% predicts 3.745. On invested capital of 2,000m that prices the operating
assets near 7,500m. The European EV/IC fit explains 57.9% of the cross-section, so it
outranks the European EV/EBITDA fit at 15.9% when the two disagree.

**Venezuela, country PE.** `country_pe_2000` with a 15% interest rate, 3.5% real growth
and a risk score of 45 predicts 15.35 against an actual 20. Venezuela was 30% expensive
while its headline PE sat mid-pack, and Malaysia at a headline 14 was cheap.

## Distribution tables: `locate`

`resources/data/multiple_distributions.json`, January 2021 unless the entry says
otherwise.

| Key | Kind | Contents |
|---|---|---|
| `us_current_pe_2021` | percentiles | p10 6.95, p25 10.41, median 18.15, p75 37.26, p90 95.44 |
| `us_trailing_pe_2021` | percentiles | p10 7.68, p25 11.50, median 20.30, p75 40.79, p90 96.80 |
| `us_forward_pe_2021` | percentiles | p10 8.96, p25 12.36, median 18.89, p75 33.20, p90 69.40 |
| `regional_ev_ebitda_median_2021` | medians by group | 12 regions, US 16.60 to E. Europe 8.07 |
| `regional_pbv_median_2013` | medians by group | 6 regions, US 1.54 to Japan 0.67 |

The trailing PE mean was 103.25 against a median of 20.30, and the mean sat above the 90th
percentile. Only 2,481 of 7,584 US firms had a usable trailing PE at all.

`locate` reports which published band a value falls in rather than interpolating a
percentile. Five points cannot support more precision than that.

## Two special cases

**Judging a whole market.** Convert the ten-year Treasury into a PE (one divided by the
rate) and compare. At the start of 2021 the Shiller PE was 29.36 and the T.Bond PE was
107.53, a ratio of 0.51 against a 1970-2020 average of 1.06. On its own history the market
was expensive; against bonds it was cheap. Cross-check with
`sp500_earnings_yield_1960_2020`, which returns an earnings yield — invert it for a
predicted market PE.

**Young companies with no usable fundamentals.** When every firm in the sector loses money,
regressing the multiple on the current margin returns nothing: the early-2000 internet
price-to-sales fit on net margin had R-squared 0.04. Three routes work. Replace the
fundamentals with survival and growth proxies (`internet_ps_2000` uses log revenue,
revenue growth and cash over revenue). Or apply a forward multiple to a future year and
haircut it back in order: discount at the risk-adjusted cost of capital, subtract
dilution, apply the failure probability, bridge to equity, subtract the option overhang.
Tesla's year-10 value of 68,271m became 8,152m today through that sequence, and
discounting alone accounted for less than half the drop. Or let the market pick the metric:
correlate market cap against every available operating measure and price on the winner.
In October 2013 users correlated with social media market caps at 0.9812, above revenues,
EBITDA and net income.
