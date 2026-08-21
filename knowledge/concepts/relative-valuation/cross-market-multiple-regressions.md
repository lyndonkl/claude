# Cross-market regressions: the same fundamentals in every market

**Core idea:** Run the market-wide pricing regression separately in each region and the same fundamentals show up everywhere. PE rises with payout and expected growth. PBV rises with ROE. EV/Sales rises with the operating margin. EV/Invested Capital rises with ROIC. Only the coefficients and the explanatory power differ by region. That gives you a portable pricing rule for any company anywhere: pick the region, pick the multiple, plug in the fundamentals. The explanatory power tells you how much to trust it. EV/IC regressions explain 50-63% of the cross-section; PEG regressions explain 11-33%.

**Formulas:** each regression is linear in its listed variables. Variable definitions apply to all tables below.
- g_EPS = expected growth in EPS or net income over the next 5 years, in decimals.
- g (in the EV tables) = expected revenue growth, near term (2 or 5 years), in decimals.
- Beta = regression beta or bottom-up beta.
- Payout = dividends/net income in the most recent year, set to zero if net income is negative.
- ROE = net income / book value of equity, most recent year.
- ROIC = return on invested capital.
- DFR = debt ratio = Total Debt/(Total Debt + Market value of equity).
- Tax Rate = effective tax rate in the most recent year.
- Operating Margin = operating income / sales.

**Procedure:**
1. Identify the region of incorporation for the company: US, Europe, Japan, Emerging Markets, Australia/NZ/Canada, or Global as the fallback.
2. Choose the multiple whose companion variable you can measure reliably for this firm.
3. Look up the regional regression below and check its R². A fit under about 15% means the prediction is weak evidence.
4. Compute the firm's inputs on the exact definitions above, in decimals.
5. Evaluate the equation to get the predicted multiple.
6. Compare with the traded multiple: `Actual/Predicted − 1`.
7. When several multiples are available, run more than one. Agreement across multiples strengthens the verdict; disagreement points to an input problem or an unmodelled feature.
8. Prefer the multiple with the highest regional R² when they conflict. That is the same rule used to pick the "best multiple" for each business in a sum-of-the-parts pricing.

**Reference data — January 2021 regressions:**

PE ratio:

| Region | Regression | R² |
|---|---|---|
| US | PE = 4.10 + 1.71 Beta + 17.40 Payout + 230.4 g_EPS | 39.4% |
| Europe | PE = 16.69 + 4.65 Beta + 15.30 Payout + 91.80 g_EPS | 14.5% |
| Japan | PE = 20.89 − 7.63 Beta + 14.30 Payout + 149.30 g_EPS | 23.8% |
| Emerging Markets | PE = 17.88 + 0.44 Beta + 3.00 Payout + 113.80 g_EPS | 21.9% |
| Australia, NZ, Canada | PE = 12.07 + 1.72 Beta + 12.00 Payout + 114.10 g_EPS | 16.1% |
| Global | PE = 20.04 − 2.57 Beta + 8.70 Payout + 139.20 g_EPS | 23.2% |

PEG ratio (log growth):

| Region | Regression | R² |
|---|---|---|
| US | PEG = 5.63 − 1.14 Beta + 0.40 Payout − 0.66 ln(g_EPS) | 11.3% |
| Europe | PEG = 6.88 − 0.88 Beta + 0.20 Payout − 1.26 ln(g_EPS) | 27.1% |
| Japan | PEG = 6.66 − 0.62 Beta + 0.60 Payout − 1.21 ln(g_EPS) | 33.2% |
| Emerging Markets | PEG = 4.98 − 0.32 Beta + 0.10 Payout − 0.91 ln(g_EPS) | 20.2% |
| Australia, NZ, Canada | PEG = 6.68 − 0.67 Beta + 0.50 Payout − 1.36 ln(g_EPS) | 27.2% |
| Global | PEG = 5.73 − 2.57 Beta + 0.10 Payout − 0.69 ln(g_EPS) | 13.0% |

Price to book:

| Region | Regression | R² |
|---|---|---|
| US | PBV = 1.72 − 1.13 Beta + 0.50 Payout + 11.00 g_EPS + 11.10 ROE | 45.2% |
| Europe | PBV = 3.11 − 1.17 Beta + 0.20 Payout + 4.30 g_EPS + 10.30 ROE | 34.9% |
| Japan | PBV = 0.98 + 0.47 Beta − 0.20 Payout + 11.20 g_EPS + 14.60 ROE | 27.8% |
| Emerging Markets | PBV = −0.32 − 0.05 Beta + 0.90 Payout + 5.00 g_EPS + 17.20 ROE | 48.3% |
| Australia, NZ, Canada | PBV = 1.73 − 1.22 Beta + 0.30 Payout + 3.90 g_EPS + 9.80 ROE | 32.4% |
| Global | PBV = 1.61 − 0.70 Beta + 0.40 Payout + 6.10 g_EPS + 12.40 ROE | 39.1% |

EV/EBITDA:

| Region | Regression | R² |
|---|---|---|
| United States | EV/EBITDA = 29.71 − 23.80 DFR + 35.00 g − 32.70 Tax Rate | 26.7% |
| Europe | EV/EBITDA = 24.26 − 13.90 DFR + 28.20 g − 7.10 Tax Rate | 15.9% |
| Japan | EV/EBITDA = 20.74 + 9.50 DFR + 85.60 g − 23.70 Tax Rate | 10.3% |
| Emerging Markets | EV/EBITDA = 30.03 − 28.30 DFR + 31.80 g − 17.60 Tax Rate | 27.8% |
| Australia, NZ & Canada | EV/EBITDA = 23.60 − 10.10 DFR + 12.60 g − 15.80 Tax Rate | 10.7% |
| Global | EV/EBITDA = 27.44 − 18.60 DFR + 32.90 g − 18.60 Tax Rate | 21.5% |

EV/Sales (slide labelled January 2020, carried in the 2021 packet):

| Region | Regression | R² |
|---|---|---|
| United States | EV/Sales = 4.35 − 5.40 Tax Rate − 1.00 DFR + 7.80 g + 6.50 Op. Margin | 31.2% |
| Europe | EV/Sales = 1.69 + 1.70 Tax Rate + 2.20 DFR + 3.20 g + 6.70 Op. Margin | 13.2% |
| Japan | EV/Sales = 2.10 − 0.80 Tax Rate − 2.00 DFR + 9.30 g + 6.60 Op. Margin | 23.5% |
| Emerging Markets | EV/Sales = 3.48 − 2.20 Tax Rate − 1.00 DFR + 3.20 g + 5.40 Op. Margin | 14.6% |
| Australia, NZ & Canada | EV/Sales = 2.16 − 2.80 Tax Rate + 2.60 DFR + 5.70 g + 7.90 Op. Margin | 31.8% |
| Global | EV/Sales = 3.37 − 2.30 Tax Rate − 0.10 DFR + 5.20 g + 6.30 Op. Margin | 18.1% |

EV/Invested Capital (slide labelled January 2020, carried in the 2021 packet):

| Region | Regression | R² |
|---|---|---|
| United States | EV/IC = 4.29 − 4.20 DFR + 2.10 g + 6.00 ROIC | 57.3% |
| Europe | EV/IC = 3.77 − 3.70 DFR + 0.80 g + 6.20 ROIC | 57.9% |
| Japan | EV/IC = 3.04 − 3.10 DFR + 6.10 g + 5.30 ROIC | 50.5% |
| Emerging Markets | EV/IC = 3.14 − 3.70 DFR + 2.50 g + 7.50 ROIC | 62.8% |
| Australia, NZ & Canada | EV/IC = 2.87 − 2.60 DFR + 0.80 g + 4.30 ROIC | 50.9% |
| Global | EV/IC = 3.62 − 3.70 DFR + 1.70 g + 6.70 ROIC | 57.5% |

Prior-year comparison (January 2020 US equations, to show coefficient drift): `PE = 9.39 − 6.03 Beta + 20.23 Payout + 137.19 g_EPS` (R² 25.2%); `PBV = −0.41 − 0.75 Beta + 2.14 Payout + 7.87 g_EPS + 16.03 ROE` (R² 52.5%); `EV/EBITDA = 22.95 − 20.20 DFR + 33.62 g − 20.50 Tax Rate` (R² 34.5%); `EV/IC = 3.77 − 3.70 DFR + 2.30 g + 8.43 ROIC` (R² 62.6%).

**Worked example:** A European industrial firm with ROIC 14%, debt ratio 25%, expected revenue growth 4%.
```
Predicted EV/IC = 3.77 − 3.70(0.25) + 0.80(0.04) + 6.20(0.14)
                = 3.77 − 0.925 + 0.032 + 0.868 = 3.75
```
With invested capital of €2,000m, that prices the operating assets at about €7,500m. The European EV/IC regression explains 57.9% of the cross-section, so this is one of the stronger predictions available. Cross-check with the European EV/EBITDA equation, whose R² is only 15.9%, and weight the EV/IC answer more heavily if they disagree.

**Determinism:** DETERMINISTIC — given region, multiple and the firm's inputs, every predicted multiple above is a plain arithmetic evaluation, and the over/under comparison follows. JUDGMENT — which region a multinational belongs to, whether the firm's reported ROE/ROIC/margin is representative, whether the R² justifies acting, and how to reconcile conflicting multiples.

**Pitfalls:**
- Using percent instead of decimals. These slide-form equations take growth, payout, ROE, ROIC, margins, tax rates and debt ratios as decimals.
- Acting on a low-R² regression as though it were a precise estimate. Japan's EV/EBITDA fit is 10.3%.
- Ignoring the wrong-sign coefficients that show up in individual regions (Japan's positive DFR in EV/EBITDA, its positive beta in PBV). These are multicollinearity artefacts, not findings.
- Mixing years. Coefficients drift substantially between January 2020 and January 2021.
- Assigning a globally diversified company to a single region by its listing venue alone.

**Sources:**
- valpacket2spr21 p.94-99
- valpacket2spr20 p.93-97

**Related:** [[market-wide-regressions]], [[sector-regressions]], [[book-value-multiples]], [[ev-ebitda-multiple]], [[ev-sales-and-brand-value]], [[peg-ratio]], [[industry-average-multiples]], [[comparable-selection-and-controls]]
