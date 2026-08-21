# Macro sensitivity regressions

The firm is a portfolio of projects. Rather than forecast a typical project, let the firm's
own history describe what that portfolio is sensitive to, and design the debt to share
those sensitivities.

## The eight regressions

Two dependent variables, four regressors, run as eight separate univariate regressions.

    Δfirm value_t       = (MarketCap_t + Debt_t) ÷ (MarketCap_(t−1) + Debt_(t−1)) − 1
    Δoperating income_t = OI_t ÷ OI_(t−1) − 1

    ΔV  = a + b × Δ(10-year bond rate)
    ΔV  = a + b × %ΔReal GDP
    ΔV  = a + b × Δ(inflation rate)
    ΔV  = a + b × %Δ(trade-weighted currency)

and the same four with ΔOI as the dependent variable.

They are simple regressions, one predictor each. A single multiple regression on all four
gives different coefficients and does not reproduce the method.

## Data assembly

1. Collect annual operating income, market capitalization and total debt, most recent
   period first. Use at least four periods; the source model allows up to 48. Quarterly
   data is permitted and buys observations at the cost of noise.
2. Convert to changes as above.
3. Pull the matching macro series for the same fiscal years.
4. Drop any period where operating income is near zero or negative. Its percent change is
   meaningless and will dominate the fit.

### Series and change conventions

| Variable | Series | Change type |
|---|---|---|
| Interest rate | 10-year Treasury or the local equivalent (FRED `DGS10`) | **absolute** change in the rate |
| Real GDP | Real GDP (FRED `GDPC1`) | **percentage** change |
| Inflation | CPI inflation rate (FRED `CPIAUCSL_PC1`) | **absolute** change in the rate |
| Currency | Trade-weighted broad dollar index | **percentage** change |

Sample annual values, to check a data pull: 2019 rate 1.92% (change −0.75%), GDP growth
2.32%, inflation 2.29% (change +0.33%), dollar change −0.77%. 2018 rate 2.69% (change
+0.27%), GDP growth 3.07%, inflation 1.95% (change −0.16%), dollar change +4.99%. 2009 rate
3.85% (change +1.56%), GDP growth 0.18%, inflation 2.81% (change +2.84%), dollar change
−5.82%.

Outside the United States, substitute the local ten-year sovereign yield, local real GDP,
local CPI, and the exchange rate against the firm's main revenue currency.

## Running them

```bash
python3 <skills>/debt-design/resources/macrosensitivity.py regress --in macro.json
```

Payload shape, one macro variable and one observation per year, most recent first:

```json
{
  "dependent": "firm_value",
  "macro_variable": "interest_rate",
  "history": {"market_cap": [231814, 209728], "total_debt": [54136, 53427]},
  "macro_changes": [0.0027],
  "period_labels": ["2018"]
}
```

That shape is cut to two periods to fit; a real payload needs at least five. Pass
`dependent_changes` instead of `history` when you have already built the change series.
Either way the two must be the same length: N periods of history give N−1 change rows.

The response gives the coefficient, its standard error, its t-statistic, R-squared and the
observation count. Record the coefficient and the t-statistic together in
`regression_table`.

It also grades the slope as a **finding**, a **hint** or **noise**, and explains the
grade. An insignificant slope is itself a finding here: it sends you to the bottom-up
route, not to a different specification. A short sample is capped at a hint no matter how
large its t-statistic, which is the honest reading of eight annual observations.

Then hand all four results to `debt-profile` to turn them into maturity, currency mix,
fixed against floating, and straight against convertible.

## Reading each slope

| Regression | Reading |
|---|---|
| Firm value on rates | Asset duration = max(0, −slope). Sets target debt duration. |
| Operating income on rates | Income rising with rates favours floating-rate debt. |
| Firm value on GDP | Positive and significant means cyclical. Borrow less, or tie payments to output. |
| Operating income on GDP | Same reading, on the cash flows that service the debt. |
| Firm value on currency | Value falling as the home currency strengthens argues for foreign-currency debt. |
| Operating income on currency | The stronger of the two currency signals in practice. |
| Firm value on inflation | Weak evidence on inflation protection. |
| Operating income on inflation | Rising with inflation means pricing power. Raises the floating-rate share. |

The sheet's convention is to read **duration and cyclicality off the firm-value
regressions**, and **inflation and currency off the operating-income regressions**.

The currency slope gives direction and rough size, not the target share. Set the actual
foreign-currency share from revenue geography, then check that its sign agrees with the
regression. Where dollar-denominated revenue is itself exposed to currency moves, the
share should sit above the raw revenue split.

## Reference regressions

Disney, 1985–2013, t-statistics in parentheses:

| Regression | Equation | Reading |
|---|---|---|
| Firm value on rates | ΔV = 0.1790 − 2.3251 × Δrates (2.74; 0.39) | Duration ≈ 2.33 years, insignificant |
| Operating income on rates | ΔOI = 0.1698 − 7.9339 × Δrates (2.69; 1.40) | Income far more rate-sensitive than value |
| Firm value on GDP | ΔV = 0.0067 + 6.7000 × GDP growth (0.06; 2.03) | Significantly cyclical |
| Operating income on GDP | ΔOI = 0.0142 + 6.6443 × GDP growth (0.13; 2.05) | Significantly cyclical |
| Firm value on currency | ΔV = 0.1774 − 0.5705 × Δ$ (2.76; 0.67) | Value falls as the dollar rises, insignificant |
| Operating income on currency | ΔOI = 0.1680 − 1.6773 × Δ$ (2.82; 2.13) | A stronger dollar significantly hurts income |
| Firm value on inflation | ΔV = 0.1855 + 2.9966 × Δinflation (2.96; 0.90) | Weak |
| Operating income on inflation | ΔOI = 0.1919 + 8.1867 × Δinflation (3.43; 2.76) | Pricing power |

This is a firm with 28 years of data, and five of its eight slopes are insignificant. Its
headline duration coefficient has a t-statistic of 0.39. Treat that as the base rate rather
than the exception.

## The bottom-up route

Switch to sector coefficients when firm-level slopes are insignificant, the history is
short, or the business mix has changed. The construction mirrors bottom-up betas:

    firm coefficient = Σ (business value weight × sector coefficient)

Weight by business value. Where segment values are not disclosed, approximate them as
segment revenue times a sector EV/Sales multiple.

Disney's businesses, value-weighted:

| Business | Interest rates | GDP growth | Inflation | Currency | Weight |
|---|---|---|---|---|---|
| Media Networks | −3.70 | 0.56 | 1.41 | −1.23 | 49.27% |
| Parks & Resorts | −4.50 | 0.70 | −3.05 | −1.58 | 33.81% |
| Studio Entertainment | −6.47 | 0.22 | −1.45 | −3.21 | 13.49% |
| Consumer Products | −4.88 | 0.13 | −5.51 | −3.01 | 2.18% |
| Interactive | −1.01 | 0.25 | −3.55 | −2.86 | 1.25% |
| **Aggregate** | **−4.34** | **0.55** | **−0.70** | **−1.67** | **100%** |

Reading the aggregate: duration of about 4.3 years, mild cyclicality, meaningful currency
exposure. Combined with an operating-income inflation slope of +8.19 (t = 2.76), the design
is long-ish debt, a significant floating-rate share, and roughly 18% in foreign currencies
based on revenue geography.

Sample two-digit industry rows:

| Industry group | Duration | Cyclicality | Inflation | Currency |
|---|---|---|---|---|
| Amusement & Recreation Services | 5.01 | 0.69 | 0.58 | −1.14 |
| Communications | 6.59 | 0.96 | 0.10 | −0.95 |
| Motion Pictures | 5.36 | 0.51 | 4.34 | −2.45 |
| General Merchandise Stores | 4.22 | 0.93 | 0.63 | 0.46 |
| Food Stores | 3.41 | 0.91 | 2.23 | −1.47 |
| Oil & Gas Extraction | 4.21 | 0.53 | 2.99 | −2.50 |
| Transportation by Air | 2.70 | 0.98 | −0.98 | 0.65 |

Finer tables exist by four-digit SIC. Published sector data is refreshed annually; record
the vintage used, and refresh it when it is more than a year stale.

**Watch the sign conventions.** The sector sheet stores raw slopes, so a negative duration
entry means value falls as rates rise. The bottom-up estimator stores sign-flipped values.
Check one known row before trusting a table you did not build.

## When not to use this route at all

- Fewer than about ten annual observations. Skip firms listed three years or less.
- A material acquisition, divestiture or business-mix shift inside the window. The history
  describes a company that no longer exists.
- Operating income near zero across several periods.
- A slope you cannot explain economically. A significant coefficient with the wrong sign is
  more likely a data problem than a discovery.

In each case the bottom-up sector route is the fallback, and the intuitive route is the
cross-check on it.
