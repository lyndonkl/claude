# Damodaran Corporate Finance Spreadsheets — Payout Policy & Project Analysis

Source folder: `/Users/kushaldsouza/Downloads/2020/Spreadsheets/Corporate Finance Spreadsheets/`
Files documented: `dividends.xls`, `buybacks.xls`, `capbudg.xls`, `oplease.xls` (2020 vintage).

All four are legacy `.xls` files: the dumps expose computed values only, no live formulas. Every
formula below was reconstructed from labels, layout, and exact numeric back-solving; each
reconstruction was verified to full float precision against the values in the sheet unless
noted otherwise. All reconstructed logic is flagged "(inferred)". Cell references are given as
`Sheet!Cell`.

---

### dividends.xls

**Purpose:** Damodaran's dividend-policy assessment model ("Analysis of Dividend Policy"). It
compares cash actually returned to stockholders (dividends + buybacks) over up to 10
historical years against what the firm *could* have returned — FCFE under three debt-policy
assumptions. It also grades investment quality (ROE vs. required return) and stock-price
performance (Jensen's alpha). Finally, it forecasts FCFE, dividends, and cash available for
buybacks for the next 5 years. Used in his corporate-finance class/valuation practice when
judging whether a firm pays out too much or too little relative to its FCFE and whether
management can be trusted with retained cash.

**Sheets:** `Read me first` (instructions only), `Inputs`, `Analysis of past dividends`,
`Forecasted Dividends & FCFE`, `Historical Stock and T.Bills` (reference data),
`Sheet1` (dropdown lists: "Yes"/"No" in A2:A3 and integers 1–10 in B2:B11 — data-validation
sources, no logic).

#### Inputs (sheet `Inputs`)

Section 1 — historical dividends & FCFE:

| Label | Cell | Example value |
|---|---|---|
| Number of years of historical data available (1–10) | E2 | 5 |
| Current debt to capital ratio | E3 | 0.11579296585803885 |
| Change to a target debt ratio? (Yes/No) | E4 | "No" |
| Target debt ratio (used only if E4 = "Yes") | E5 | 0.40 |
| Net Income, years 1..10 (year 1 = most recent, working backwards) | B9:B18 | 6136, 5682, 4807, 3963, 3307, 4427, 4687, 3374, 2533, 2345 |
| Depreciation & Amortization, years 1..10 | C9:C18 | 2192, 1987, 1841, 1713, 1631, 1582, 1491, 1437, 1339, 1210 |
| Capital Spending & operating investments (incl. acquisitions), years 1..10 | D9:D18 | 2796, 3784, 3559, 2110, 1753, 1586, 1566, 1319, 1823, 1427 |
| Change in Non-Cash Working Capital, years 1..10 | E9:E18 | −133, 940, 950, 308, −109, 485, 45, −136, 270, 51 |
| Net Debt Issued, years 1..10 | F9:F18 | 1881, 4246, 2743, 1190, −235, 1005, 4990, 2891, 1076, 276 |
| Dividends (aggregate cash dividends), years 1..10 | B22:B31 | 1324, 1076, 756, 653, 648, 664, 637, 519, 490, 430 |
| Equity Repurchases ($), years 1..10 | C22:C31 | 4087, 3015, 4993, 2669, 648, 4453, 6923, 6898, 2420, 335 |

The year-label column A9:A18 (and A22:A31) displays the year number for years ≤ E2 and 0
beyond it — (inferred) `=IF(row_index <= E2, row_index, 0)`. Ten rows of data may be entered
regardless of E2; the analysis uses only the first E2 years (with one quirk noted under Logic).

Section 2 — investment quality & stock performance:

| Label | Cell | Example value |
|---|---|---|
| Beta of the firm's equity | D37 | 0.9011 |
| Book Value of Equity, years 1..10 | B41:B50 | 380078, 330056, 194181, 84200, 63437, 91658, 79717, 63054, 44602, 37019 |
| Annual return on the stock (price appreciation + dividend yield), years 1..10 | C41:C50 | 0.3533, 0.1065, −0.0515, 0.1622, 0.3117, 0.383, −0.0345, 0.1027, −0.1155, 0.076 |
| T.Bill rate (riskfree, start of each year), years 1..10 | D41:D50 | 0.0155, 0.019391667, 0.009308333, 0.003175, 0.000525, 0.000325, 0.000583333, 0.000858333, 0.000525, 0.001366667 |
| Return on the stock market, years 1..10 | E41:E50 | 0.312236472, −0.042268693, 0.216054814, 0.117730809, 0.013788916, 0.135244216, 0.321450859, 0.158905852, 0.020983747, 0.148210923 |

(The example T.Bill/market values are the US 2019 back to 2010 rows lifted from the
`Historical Stock and T.Bills` sheet — user matches them to their data years.)

Section 3 — forecasting inputs:

| Label | Cell | Example value |
|---|---|---|
| Expected growth in Revenues over next 5 years | E55 | 0.05 |
| Expected growth in Net Income over next 5 years | E56 | 0.05 |
| Expected growth in capital expenditures over next 5 years | E57 | 0.05 |
| Expected growth in depreciation over next 5 years | E58 | 0.05 |
| Non-cash working capital as % of revenues | E59 | 0.06 |
| Revenues, most recent year | E60 | 42278 |
| Net income, most recent year (or normalized) | E61 | 6136 |
| Capital expenditures, most recent year (or normalized) | E62 | 2796 |
| Depreciation, most recent year | E63 | 2192 |
| Dividends paid, most recent year | E64 | 1324 |
| Expected growth in dividends | D66 | 0.05 |

#### Logic (sheet `Analysis of past dividends`) — all (inferred), all verified numerically

Let `t = 1..E2` index the historical years (1 = most recent), `DR_target` = E5 if E4="Yes"
else E3. Columns B..K are years 1..10; cells for `t > E2` display `' '` (space text) or 0;
row 2 repeats the year labels (0 beyond E2); row 28 "Index" = 1 for `t ≤ E2` else 0 (an
in-use flag). Column L "Aggregate" sums each row across the E2 used years.

Per year t:

```
FCFE_predebt_t     = NI_t − (CapEx_t − Depr_t) − ΔWC_t                       (row 6)
FCFE_actual_t      = FCFE_predebt_t + NetDebtIssued_t                         (row 8)
FCFE_target_t      = NI_t − (CapEx_t − Depr_t)·(1 − DR_target)
                          − ΔWC_t·(1 − DR_target)                             (row 9)
CashToStockholders_t = Dividends_t + Buybacks_t                               (row 13)

PayoutRatio_t      = Dividends_t / NI_t                                       (row 16)
CashPaid%FCFE_t    = CashToStockholders_t / FCFE_actual_t                     (row 17)

ROE_t              = NI_t / BVEquity_t          (same-year BV as entered)     (row 21)
RequiredReturn_t   = Rf_t + Beta·(Rm_t − Rf_t)                                (rows 22, 26)
ROE_minus_COE_t    = ROE_t − RequiredReturn_t                                 (row 23)
JensensAlpha_t     = StockReturn_t − RequiredReturn_t                         (row 27)
```

Note on FCFE_target: with the example DR_target = current ratio 0.115793,
year 1 = 6136 − (604 + (−133))·0.884207 = 5719.5385 ✓ (matches B9 exactly).

Summary block (rows 31–49), over the E2 = 5 used years except where noted:

```
AggNI          = Σ NI_t                       (B32 = 23895);  AvgNI = AggNI/E2       (C32 = 4779)
AggDiv         = Σ Div_t                      (B33 = 4457);   AvgDiv = /E2           (C33 = 891.4)
DivPayout_agg  = AggDiv / AggNI               (B34 = 0.18652437748482947)
DivPayout_avg  = mean of annual PayoutRatio_t (C34 = 0.1846276973824568)
AggBuybacks    = Σ Buybacks_t                 (B35 = 15412); Avg = 3082.4
AggCash        = AggDiv + AggBuybacks         (B36 = 19869); Avg = 3973.8
CashPayoutRatio        = AggCash / AggNI              (B37 = 0.8315128688010044)
AggFCFE_predebt        = 17301; avg 3460.2            (B38/C38)
AggFCFE_actual         = 27126; avg 5425.2            (B39/C39)
AggFCFE_target         = 18064.53881686791; avg 3612.907763373582 (B40/C40)
Cash% of pre-debt FCFE = AggCash/AggFCFE_predebt = 1.1484307265475984  (B41)
Cash% of actual FCFE   = AggCash/AggFCFE_actual  = 0.732470692324707   (B42)
Cash% of target FCFE   = AggCash/AggFCFE_target  = 1.0998896900399782  (B43)

Average ROE (B45) = Σ_{t=1..10} NI_t / Σ_{t=1..10} BVEquity_t = 41261/1368002
                  = 0.0301615056118339
   *** QUIRK (verified exactly): B45 sums ALL TEN input rows of NI and BV, ignoring E2 —
   NOT the average of the annual ROE row and NOT restricted to the E2 years used
   everywhere else. A faithful port must reproduce this; a "fixed" port should
   restrict to E2 years (arithmetic mean of ROE_t = 0.0314623 in this example). ***

Avg Return on Stock (B46) = arithmetic mean of StockReturn_t, t=1..E2 = 0.17644
Avg Required Return (B47) = arithmetic mean of RequiredReturn_t, t=1..E2
                          = 0.11224093867256421
ROE − Required (B48)      = B45 − B47 = −0.08207943306073032
Actual − Required (B49)   = B46 − B47 = 0.06419906132743577   (avg Jensen's alpha)
```

#### Logic (sheet `Forecasted Dividends & FCFE`) — all (inferred), verified

`DR` (B2) = E5 if E4 = "Yes" else E3 (example: 0.11579296585803885). For forecast years
t = 1..5:

```
Revenues_t = E60·(1+E55)^t                       (row 13; yr1 = 44391.9)
NI_t       = E61·(1+E56)^t                       (row 6;  yr1 = 6442.8)
CapEx_t    = E62·(1+E57)^t ; Depr_t = E63·(1+E58)^t   (not displayed; used in row 7)
ΔWC_t      = E59·(Revenues_t − Revenues_{t−1})   (row 14, labeled "Non-cash WC" but it is
             the CHANGE; Revenues_0 = E60; yr1 = 0.06·(44391.9−42278) = 126.834)
NetCapEx_net_of_debt_t = (CapEx_t − Depr_t)·(1 − DR)    (row 7; yr1 = 560.7641)
ΔWC_net_of_debt_t      = ΔWC_t·(1 − DR)                 (row 8; yr1 = 112.1475)
FCFE_t     = NI_t − row7_t − row8_t              (row 9; yr1 = 5769.888383978806)
ExpDividends_t = E64·(1+D66)^t                   (row 10; yr1 = 1390.2)
CashForBuybacks_t = FCFE_t − ExpDividends_t      (row 11; yr1 = 4379.688383978806)
```

#### Reference data (sheet `Historical Stock and T.Bills`) — VERBATIM

Annual US returns 1928–2020 (S&P 500 total return incl. dividends, 3-month T.Bill return,
10-year T.Bond total return). Used to populate the Rf and Rm input columns; also a general
reference. Values below are the sheet's floats rounded to 6 decimal places (source values
carry full double precision; e.g. 1928 S&P = 0.43811155152887893).

| Year | S&P 500 (incl. div) | 3-month T.Bill | 10-year T.Bond return |
|---|---|---|---|
| 1928 | 0.438112 | 0.0308 | 0.008355 |
| 1929 | −0.082979 | 0.0316 | 0.042038 |
| 1930 | −0.251236 | 0.0455 | 0.045409 |
| 1931 | −0.438375 | 0.0231 | −0.025589 |
| 1932 | −0.086424 | 0.0107 | 0.087903 |
| 1933 | 0.499822 | 0.0096 | 0.018553 |
| 1934 | −0.011886 | 0.002783 | 0.079634 |
| 1935 | 0.467404 | 0.001675 | 0.044720 |
| 1936 | 0.319434 | 0.001725 | 0.050179 |
| 1937 | −0.353367 | 0.002758 | 0.013791 |
| 1938 | 0.292827 | 0.000650 | 0.042132 |
| 1939 | −0.010976 | 0.000458 | 0.044123 |
| 1940 | −0.106729 | 0.000358 | 0.054025 |
| 1941 | −0.127715 | 0.001292 | −0.020222 |
| 1942 | 0.191738 | 0.003425 | 0.022949 |
| 1943 | 0.250613 | 0.003800 | 0.024900 |
| 1944 | 0.190307 | 0.003800 | 0.025776 |
| 1945 | 0.358211 | 0.003800 | 0.038044 |
| 1946 | −0.084291 | 0.003800 | 0.031284 |
| 1947 | 0.052000 | 0.006008 | 0.009197 |
| 1948 | 0.057046 | 0.010450 | 0.019510 |
| 1949 | 0.183032 | 0.011150 | 0.046635 |
| 1950 | 0.308055 | 0.012033 | 0.004296 |
| 1951 | 0.236785 | 0.015175 | −0.002953 |
| 1952 | 0.181510 | 0.017225 | 0.022680 |
| 1953 | −0.012082 | 0.018908 | 0.041438 |
| 1954 | 0.525633 | 0.009383 | 0.032898 |
| 1955 | 0.325973 | 0.017250 | −0.013364 |
| 1956 | 0.074395 | 0.026275 | −0.022558 |
| 1957 | −0.104574 | 0.032250 | 0.067970 |
| 1958 | 0.437200 | 0.017708 | −0.020990 |
| 1959 | 0.120565 | 0.033858 | −0.026466 |
| 1960 | 0.003365 | 0.028833 | 0.116395 |
| 1961 | 0.266377 | 0.023542 | 0.020609 |
| 1962 | −0.088115 | 0.027733 | 0.056935 |
| 1963 | 0.226119 | 0.031592 | 0.016842 |
| 1964 | 0.164155 | 0.035467 | 0.037281 |
| 1965 | 0.123992 | 0.039492 | 0.007189 |
| 1966 | −0.099710 | 0.048625 | 0.029079 |
| 1967 | 0.238030 | 0.043067 | −0.015806 |
| 1968 | 0.108149 | 0.053383 | 0.032746 |
| 1969 | −0.082414 | 0.066667 | −0.050140 |
| 1970 | 0.035611 | 0.063917 | 0.167547 |
| 1971 | 0.142212 | 0.043325 | 0.097869 |
| 1972 | 0.187554 | 0.040725 | 0.028184 |
| 1973 | −0.143080 | 0.070317 | 0.036587 |
| 1974 | −0.259018 | 0.078300 | 0.019886 |
| 1975 | 0.369951 | 0.057750 | 0.036053 |
| 1976 | 0.238310 | 0.049742 | 0.159846 |
| 1977 | −0.069797 | 0.052692 | 0.012900 |
| 1978 | 0.065093 | 0.071883 | −0.007776 |
| 1979 | 0.185195 | 0.100692 | 0.006707 |
| 1980 | 0.317352 | 0.114342 | −0.029897 |
| 1981 | −0.047024 | 0.140250 | 0.081992 |
| 1982 | 0.204191 | 0.106142 | 0.328145 |
| 1983 | 0.223372 | 0.086108 | 0.032002 |
| 1984 | 0.061461 | 0.095225 | 0.137334 |
| 1985 | 0.312351 | 0.074792 | 0.257125 |
| 1986 | 0.184946 | 0.059783 | 0.242842 |
| 1987 | 0.058127 | 0.057750 | −0.049605 |
| 1988 | 0.165372 | 0.066675 | 0.082236 |
| 1989 | 0.314752 | 0.081117 | 0.176936 |
| 1990 | −0.030645 | 0.074933 | 0.062354 |
| 1991 | 0.302348 | 0.053750 | 0.150045 |
| 1992 | 0.074937 | 0.034317 | 0.093616 |
| 1993 | 0.099671 | 0.029975 | 0.142110 |
| 1994 | 0.013259 | 0.042467 | −0.080367 |
| 1995 | 0.371952 | 0.054900 | 0.234808 |
| 1996 | 0.226810 | 0.050058 | 0.014286 |
| 1997 | 0.331037 | 0.050608 | 0.099391 |
| 1998 | 0.283380 | 0.047767 | 0.149214 |
| 1999 | 0.208854 | 0.046383 | −0.082542 |
| 2000 | −0.090318 | 0.058167 | 0.166553 |
| 2001 | −0.118498 | 0.033883 | 0.055722 |
| 2002 | −0.219660 | 0.016025 | 0.151164 |
| 2003 | 0.283558 | 0.010108 | 0.003753 |
| 2004 | 0.107428 | 0.013717 | 0.044907 |
| 2005 | 0.048345 | 0.031467 | 0.028675 |
| 2006 | 0.156126 | 0.047267 | 0.019610 |
| 2007 | 0.054847 | 0.043533 | 0.102099 |
| 2008 | −0.365523 | 0.013650 | 0.201013 |
| 2009 | 0.259352 | 0.001500 | −0.111167 |
| 2010 | 0.148211 | 0.001367 | 0.084629 |
| 2011 | 0.020984 | 0.000525 | 0.160353 |
| 2012 | 0.158906 | 0.000858 | 0.029716 |
| 2013 | 0.321451 | 0.000583 | −0.091046 |
| 2014 | 0.135244 | 0.000325 | 0.107462 |
| 2015 | 0.013789 | 0.000525 | 0.012843 |
| 2016 | 0.117731 | 0.003175 | 0.006906 |
| 2017 | 0.216055 | 0.009308 | 0.028017 |
| 2018 | −0.042269 | 0.019392 | −0.000167 |
| 2019 | 0.312236 | 0.015500 | 0.096356 |
| 2020 | 0.180139 | 0.000900 | 0.113319 |

#### Outputs

- `Analysis of past dividends` rows 6, 8, 9: annual FCFE under three debt assumptions
  (pre-debt, actual net debt issued, constant target/current debt ratio).
- Row 13: annual cash returned to stockholders; rows 16–17: payout ratios.
- Rows 21–27: annual ROE, required return (CAPM), excess ROE, stock return, Jensen's alpha.
- Rows 31–49: period aggregates/averages — key verdict cells: B37 cash payout ratio (0.8315),
  B41–B43 cash returned as % of each FCFE measure (1.1484 / 0.7325 / 1.0999),
  B48 ROE − required return (−0.0821), B49 actual − required stock return (+0.0642).
- `Forecasted Dividends & FCFE` rows 9–11: 5-year forecast of FCFE, expected dividends, and
  cash available for stock buybacks.

#### Worked example (values currently in sheet, 5 years of data)

Year 1: FCFE_predebt = 6136 − (2796−2192) − (−133) = 5665; + net debt 1881 → FCFE_actual
= 7546; FCFE_target = 6136 − 471·(1−0.115793) = 5719.54. Cash returned = 1324 + 4087 = 5411
= 71.7% of actual FCFE. RequiredReturn = 0.0155 + 0.9011·(0.312236 − 0.0155) = 0.282889;
Jensen's alpha = 0.3533 − 0.282889 = 0.070411; ROE = 6136/380078 = 0.016144.
Over 5 years: cash returned 19,869 vs. actual FCFE 27,126 (73.2%), but 110% of target-ratio
FCFE. Avg ROE (10-yr quirk) is 3.02% vs. avg required return 11.22% → poor projects
(−8.21%). Yet the stock beat its required return by +6.42%/yr.
Forecast year 1: NI 6442.8 − 560.76 − 112.15 = FCFE 5769.89; dividends 1390.2; buyback
capacity 4379.69, growing to 5323.54 by year 5.

#### Reimplementation notes

Inputs: `n_years` (int 1–10), `current_debt_ratio` (float), `use_target_ratio` (bool),
`target_debt_ratio` (float), per-year arrays (most recent first, length ≥ n_years, currency
units): `net_income`, `depreciation`, `capex`, `chg_noncash_wc`, `net_debt_issued`,
`dividends`, `buybacks`, `bv_equity`, `stock_return`, `tbill_rate`, `market_return`;
scalar `beta`; forecast inputs: growth rates for revenues/NI/capex/depreciation/dividends
(fractions), `wc_pct_revenues`, base-year revenues/NI/capex/depreciation/dividends.
Outputs: per-year and aggregate FCFE (3 variants), cash returned, payout ratios, ROE,
required return, Jensen's alpha, period averages, and the 5-year forecast table.
Branches/edge cases:
- Debt ratio selector: target vs. current (E4/E5) feeds both FCFE_target and the forecast.
- Only the first `n_years` entries feed every statistic EXCEPT average ROE (B45), which in
  the original sums NI and BV over all ten input rows — decide whether to replicate the bug
  (flag it) or restrict to `n_years`.
- Negative NI makes PayoutRatio_t meaningless (negative); negative FCFE makes
  cash-paid-%-of-FCFE negative — guard or pass through as the sheet does (it passes through).
- Division by zero if BV equity, NI, or FCFE is 0 for a used year.
- Averages are arithmetic means over `n_years`; aggregate ratios are ratio-of-sums (the sheet
  reports both, and they differ — keep both).
- ΔWC in the forecast uses revenue *changes*, not levels; year-0 revenue is the base-year
  input.

---

### buybacks.xls

**Purpose:** Quantifies the effect of a stock buyback on firm value, equity value, enterprise
value, and value per share (sheet `Value Effect`), and on EPS and the PE ratio (sheet
`EPS Effect`). It also computes the wealth transfer between selling and remaining
shareholders when the buyback price differs from fair value. Damodaran uses it to debunk the
claim that buybacks mechanically create value or that EPS accretion equals value creation. Sheet `Sheet3` holds
only the Yes/No dropdown list.

#### Inputs (sheet `Value Effect`)

| Label | Cell | Example value |
|---|---|---|
| Current stock price | B6 | 60.0 |
| Shares outstanding before buyback | B7 | 2000.0 |
| Beta for the stock | B8 | 1.2 |
| Debt outstanding (interest-bearing, MV preferred) | B10 | 15961.0 |
| Cash and marketable securities | B11 | 3931.0 |
| Cost of debt (pre-tax, existing) | B12 | 0.0375 |
| Net income | B13 | 4000.0 |
| Interest income from cash | B14 | 60.0 |
| Have a fair-value estimate for the stock? (Yes/No) | B16 | "Yes" |
| Fair value per share (if Yes) | B17 | 75.0 |
| Expected buyback price | B19 | 65.0 |
| Number of shares bought back | B20 | 200.0 |
| Buyback funded with cash | B21 | 3000.0 |
| Buyback funded with new debt | B22 | 10000.0 |
| Cost of new debt (pre-tax) | B23 | 0.0425 |
| Risk-free rate | B25 | 0.0275 |
| Equity risk premium | B26 | 0.05 |
| Marginal tax rate | B27 | 0.4 |

`EPS Effect` sheet inputs mirror/link these: price B2=60, market cap B3=120000, cash B4=3931,
interest income B5=60, NI B6=4000, shares B7=2000. Buyback details there: shares bought
B10=200, buyback price B11=65, post-buyback price B12 (linked from Value Effect C42), cash
funding B15=3000, debt funding B16=10000, rate on new debt B17=0.0425, tax rate B18=0.4.
(Note: buyback cost B13 = 13000 = 200×65, funded here as 3000 cash + 10000 debt. The model
does not force B21+B22 = price×shares — the user should keep them consistent.)

#### Logic (all inferred; every line verified to full precision against sheet values)

Pre-buyback (column B, rows 31–42):

```
E0   = price·shares = 60·2000 = 120000                       (equity market value)
D/E0 = Debt/E0 = 0.13300833…                                 (B32)
D/C0 = Debt/(Debt+E0) = 0.11739395…                          (B33)
ke0  = Rf + β·ERP = 0.0275 + 1.2·0.05 = 0.0875               (B34)
kd0_AT = kd_existing·(1−t) = 0.0375·0.6 = 0.0225             (B35)
WACC0 = ke0·E0/(D+E0) + kd0_AT·D/(D+E0) = 0.07986939269349298  (B36)
EV0  = E0 + Debt − Cash = 132030                              (B37)
FirmValue0 = E0 + Debt = 135961                               (B38)
```

Post-buyback (column C):

```
Cost      = buyback_price·shares_bought = 65·200 = 13000
E1_mech   = E0 − Cost = 107000            (mechanical equity after cash out)
D1        = Debt + new_debt = 25961                            (C39)
D/E1      = D1/E1_mech = 0.24262616822429905                   (C32)
β_u       = β/(1 + (1−t)·D/E0) = 1.2/1.079805 = 1.1113114…
β1        = β_u·(1 + (1−t)·D/E1) = 1.2730917537161761          (C31)
ke1       = Rf + β1·ERP = 0.09115458768580881                  (C34)
kd1_AT    = cost_of_NEW_debt·(1−t) = 0.0425·0.6 = 0.0255       (C35)
            *** applied to ALL debt post-buyback, not blended with old debt ***
D/C1      = D1/(D1+E1_mech) = 0.1952527432856251               (C33)
WACC1     = ke1·E1_mech/(D1+E1_mech) + kd1_AT·D1/(D1+E1_mech)
          = 0.07833534933086801                                (C36)
EV1       = EV0·(WACC0 − Rf)/(WACC1 − Rf) = 136014.23041905585 (C37)
            (growing-perpetuity revaluation with growth rate g = Rf:
             EV = CF/(WACC−g) ⇒ EV1/EV0 = (WACC0−Rf)/(WACC1−Rf); verified exactly)
Cash1     = Cash − cash_used = 3931 − 3000 = 931
FirmValue1 = EV1 + Cash1 = 136945.23041905585                  (C38)
E1_value  = FirmValue1 − D1 = 110984.23041905585               (C40)
Shares1   = shares − bought = 1800                             (C41)
Price1    = E1_value/Shares1 = 61.65790578836436               (C42)
%Change column D = C/B − 1 for rows 37–42.
```

Value transfer (rows 45–51):

```
FairValue  = B17 if B16="Yes" (else presumably current price — not observable) (B45 = 75)
Transfer   = (FairValue − buyback_price)·shares_bought = (75−65)·200 = 2000    (B48)
RemShares  = 1800                                                              (B49)
Transfer/share = 2000/1800 = 1.1111111111111112                                (B50)
Price with transfer = Price1 + Transfer/share = 61.65791 + 1.11111
                    = 62.769016899475474                                       (B51)
```

Sheet `EPS Effect` (rows 20–25):

```
MktCap1 = E1_value (linked) ; Price1 linked
NI1     = NI − interest_income_from_cash − new_debt·kd_new·(1−t)
        = 4000 − 60 − 10000·0.0425·0.6 = 3685                  (C23)
   *** Verified exactly: the FULL interest income on cash (B5 = 60) is subtracted, even
   though only 3000 of the 3931 cash is used, and it is NOT tax-adjusted; the new-debt
   interest IS after-tax. Replicate as-is and flag. ***
EPS0 = NI/shares = 2.0 ; EPS1 = NI1/Shares1 = 3685/1800 = 2.047222…  (B24/C24)
PE0  = Price0/EPS0 = 30.0 ; PE1 = Price1/EPS1 = 30.11783729146699    (B25/C25)
% and $ change columns: D = post/pre − 1, E = post − pre.
```

**Reference data:** none (Sheet3 is just the Yes/No validation list).

#### Outputs

- `Value Effect` C31–C42 + column D: post-buyback beta, leverage ratios, costs of
  equity/debt/capital, enterprise value, firm value, equity value, share count, price per
  share, and % changes. Headline: price/share 60 → 61.658 (+2.76%) despite equity value
  falling 7.51%.
- B48–B51: wealth transfer to remaining shareholders when buying back below fair value
  (+$1.11/share here; price with transfer 62.77).
- `EPS Effect` C21–E25: post-buyback NI (3685), EPS (2.0472, +2.36%), PE (30.118, +0.39%).

#### Worked example

Buy back 200 shares at 65 (cost 13000; 3000 cash + 10000 new debt at 4.25%). Leverage rises
(D/E 0.133 → 0.243), beta relevers 1.2 → 1.2731, cost of equity 8.75% → 9.115%, but WACC
falls 7.987% → 7.834% because cheap after-tax debt (2.55%) replaces equity. EV rises to
132030·(0.079869−0.0275)/(0.078335−0.0275) = 136014.2; add remaining cash 931, subtract debt
25961 → equity 110984.2 over 1800 shares = 61.66/share. Because fair value (75) exceeds the
buyback price (65), remaining holders also gain 2000/1800 = 1.11/share → 62.77 with transfer.
EPS rises 2.00 → 2.047 (income falls 7.9% but shares fall 10%).

#### Reimplementation notes

Inputs: floats — price, shares, beta, debt, cash, kd_old, net_income, interest_income,
has_fair_value (bool), fair_value, buyback_price, shares_bought, cash_funding, debt_funding,
kd_new, rf, erp, tax_rate. Outputs: pre/post tables as above.
Branches/edge cases:
- WACC1 ≤ Rf makes the EV revaluation divide by ≤ 0 — guard.
- If has_fair_value = "No", skip/zero the value-transfer block (or use market price, making
  the transfer 0 when buyback is at market).
- cash_funding > cash balance is not checked by the sheet; neither is
  cash_funding + debt_funding == buyback cost. Validate or replicate.
- The hidden growth assumption g = Rf in the EV step and the two documented quirks
  (kd_new applied to all debt; full un-prorated, pre-tax interest income subtracted in the
  EPS sheet) must be reproduced for value-parity, but flag them.
- Buying back more shares than outstanding, or shares_bought = shares, breaks per-share math.

---

### capbudg.xls

**Purpose:** Project capital-budgeting model (single sheet `CapBudgWS`, titled "Equity
Analysis of a Project"). Builds a 1–10 year after-tax cash-flow table for a project from
revenue/expense/depreciation/working-capital assumptions, discounts at either a direct rate
or a CAPM-based cost of capital, and reports NPV, IRR, and average return on capital.
Damodaran uses it for the investment-analysis section of corporate finance (project NPV with
opportunity costs, tax credits, salvage, and working-capital effects).

#### Inputs (all on `CapBudgWS`; "user enters all bold numbers")

| Label | Cell | Example value |
|---|---|---|
| Initial investment | C4 | 50000 |
| Opportunity cost (if any) | C5 | 7484 |
| Lifetime of the investment (years, ≤ 10) | C6 | 10 |
| Salvage value at end of project | C7 | 10000 |
| Depreciation method (1 = straight line; 2 = double-declining balance) | C8 | 2 |
| Tax credit rate on investment (if any) | C9 | 0.10 |
| Other investment (non-depreciable) | C10 | 0 |
| Initial investment in working capital | C13 | 10000 |
| Working capital as % of revenues | C14 | 0.25 |
| Salvageable fraction of working capital at end | C15 | 1.0 |
| Revenues in year 1 | G4 | 40000 |
| Variable expenses as % of revenues | G5 | 0.50 |
| Fixed expenses in year 1 | G6 | 0 |
| Tax rate on net income | G7 | 0.40 |
| Discount-rate approach (1 = direct; 2 = CAPM/WACC) | K4 | 2 |
| Direct discount rate (if approach 1) | K5 | 0.10 |
| Beta | K6 | 0.9 |
| Riskless rate | K7 | 0.08 |
| Market risk premium | K8 | 0.055 |
| Debt ratio | K9 | 0.30 |
| Cost of borrowing (pre-tax) | K10 | 0.09 |
| Revenue growth rate, years 2..10 | D19:L19 | 0.1, 0.1, 0.1, 0.1, 0, 0, 0, 0, 0 |
| Fixed-expense growth rate, years 2..10 (default = revenue growth) | D20:L20 | 0.1, 0.1, 0.1, 0.1, 0, 0, 0, 0, 0 |

#### Logic (all inferred; verified against sheet values)

Discount rate (K11):

```
if approach == 1:  r = K5
else:              ke = Rf + β·MRP = 0.08 + 0.9·0.055 = 0.1295
                   r  = ke·(1 − DebtRatio) + kd·(1 − tax)·DebtRatio
                      = 0.1295·0.7 + 0.09·0.6·0.3 = 0.10685            (K11)
```

Initial investment at t = 0 (rows 25–31):

```
NetInvestment = Investment − TaxCredit·Investment = 50000 − 5000 = 45000
InitialOutlay = NetInvestment + InitialWC + OppCost + OtherInvest
              = 45000 + 10000 + 7484 + 0 = 62484                        (B31)
NATCF_0 = −InitialOutlay                                                (B49)
```

Yearly table, t = 1..10 (columns C..L). `LifetimeIndex_t` (row 38) = 1 if t ≤ lifetime else 0
(zeroes out years beyond the project life when lifetime < 10):

```
Rev_1 = G4 ;  Rev_t = Rev_{t−1}·(1 + g_rev_t)                     (row 39)
VarExp_t = G5·Rev_t                                               (row 40)
Fixed_1 = G6 ; Fixed_t = Fixed_{t−1}·(1 + g_fixed_t)              (row 41)
EBITDA_t = Rev_t − VarExp_t − Fixed_t                             (row 42)

Depreciation (rows 43/61; book value rows 60/62, depreciable base = Investment C4,
floor = SalvageValue C7):
  BV_beg_1 = Investment
  if method == 1 (straight line):  Dep_t = (Investment − Salvage)/Lifetime   (inferred, not
                                            exercised in this sheet)
  if method == 2 (DDB):  Dep_t = min( (2/Lifetime)·BV_beg_t , BV_beg_t − Salvage )
  BV_end_t = BV_beg_t − Dep_t ; BV_beg_{t+1} = BV_end_t
  Example (DDB, 2/10 = 0.2): 10000, 8000, 6400, 5120, 4096, 3276.8, 2621.44, then
  485.76 in yr 8 (capped at BV − salvage), 0, 0; BV parks at salvage 10000.

EBIT_t = EBITDA_t − Dep_t                                         (row 44)
Tax_t  = G7·EBIT_t          (no loss-carryforward; negative EBIT ⇒ negative tax) (row 45)
EBIT1t_t = EBIT_t − Tax_t = EBIT_t·(1 − G7)                       (row 46)
ΔWC_t: WC_t = C14·Rev_t ;  ΔWC_1 = C14·Rev_1 − InitialWC (= 0 here);
       ΔWC_t = C14·(Rev_t − Rev_{t−1}) for t ≥ 2                  (row 48)
NATCF_t = EBIT1t_t + Dep_t − ΔWC_t                                (row 49)

Salvage flows (rows 34–35, year = lifetime only):
  EquipSalvage = C7 = 10000
  WCSalvage    = C15·WC_lifetime = 1.0·0.25·58564 = 14641.000000000005
  (Salvage is NOT in the NATCF row; it is added inside the final year's discounted CF.)

DiscountFactor_t = (1 + r)^t                                      (row 50)
DCF_t = (NATCF_t + EquipSalvage_t + WCSalvage_t)/DiscountFactor_t (row 51)
  (final year: (17569.2 + 10000 + 14641)/1.10685^10 = 15294.303917302585 ✓)

NPV = Σ_{t=0..10} DCF_t = 47927.64998482676                       (C54)
IRR = IRR of the {NATCF_0, NATCF_t + salvage_t} stream = 0.2355393602386762   (C55)
ROC = mean(EBIT1t_t, t=1..10) / mean(BV_beg_t, t=1..10)
    = 13710.72 / 22805.696 = 0.6011971746005914                   (C56)
  (Verified: uses beginning-of-year equipment book value only — working capital and
   opportunity cost are NOT in the ROC denominator.)
```

**Reference data:** none.

#### Outputs

- C54 NPV = 47927.65 (project adds value at 10.685% discount rate).
- C55 IRR = 23.554%.
- C56 ROC = 60.12% (average after-tax EBIT over average beginning book value).
- Full annual table: revenues → EBITDA → EBIT → EBIT(1−t) → NATCF → discounted CF, plus
  book-value/depreciation schedule (rows 60–62) and salvage rows.

#### Worked example

t=0 outlay 62484 (45000 net of 10% tax credit + 10000 WC + 7484 opportunity cost). Year 1:
Rev 40000, VarExp 20000, EBITDA 20000, DDB depreciation 10000 → EBIT 10000, tax 4000,
EBIT(1−t) 6000, +Dep 10000, ΔWC 0 → NATCF 16000 → PV 16000/1.10685 = 14455.44. Revenues grow
10% through year 5 (58564) then flatten; ΔWC = 25% of each revenue increment (1000…1331,
then 0). Year 10 adds equipment salvage 10000 and WC recovery 14641 → PV 15294.30.
NPV = 47927.65; IRR 23.55%; ROC 60.12%.

#### Reimplementation notes

Inputs: floats/ints per the table above plus two length-9 growth-rate vectors (years 2..10).
Outputs: NPV, IRR, ROC, and the full annual cash-flow table.
Branches/edge cases:
- Discount-rate approach switch (direct vs. WACC).
- Depreciation-method switch (SL vs. DDB); DDB must cap each year's charge at
  BV − salvage and hold BV at salvage thereafter (year-8 cap in the example is the
  regression test: 485.7600000000075).
- lifetime < 10: LifetimeIndex zeroes years beyond life; salvage flows land in year
  `lifetime`, not year 10.
- Year-1 ΔWC = WC%·Rev_1 − InitialWC (can be nonzero/negative if the user's initial WC
  doesn't equal WC%·Rev_1).
- Negative EBIT produces a negative tax (implicit full loss offset) — replicate or flag.
- IRR needs a root-finder; the stream must include t=0 outlay and salvage in the final year.
- ROC denominator = beginning equipment BV only (no WC, no opportunity cost).

---

### oplease.xls

**Purpose:** Operating-lease converter (sheet `Operating Lease Converter`; `Sheet3` is
empty). Converts future operating-lease commitments (from the financial-statement footnote)
into a debt equivalent by discounting them at the firm's pre-tax cost of debt, then restates
operating income and total debt. Damodaran uses this before computing ratios, cost of
capital, and reinvestment for any firm with material operating leases (pre-IFRS 16/ASC 842
statements).

#### Inputs

| Label | Cell | Example value |
|---|---|---|
| Operating lease expense in current year | E7 | 2500 |
| Lease commitment, year 1 (next year) | B10 | 2000 |
| Lease commitment, year 2 | B11 | 2000 |
| Lease commitment, year 3 | B12 | 2000 |
| Lease commitment, year 4 | B13 | 1800 |
| Lease commitment, year 5 | B14 | 1600 |
| Lease commitment, "6 and beyond" (lump sum) | B15 | 8000 |
| Pre-tax cost of debt | C17 | 0.0548 |
| Reported operating income (EBIT, current income statement) | D20 | 10000 |
| Reported debt (interest-bearing, balance sheet) | D21 | 25000 |
| Reported interest expenses | D22 | 2000 |

#### Logic (all inferred; verified to full precision)

```
kd = C17
AvgCommitment_1to5 = mean(B10:B14) = 9400/5 = 1880
N_beyond = ROUND(B15 / AvgCommitment_1to5, 0) = ROUND(8000/1880) = ROUND(4.255) = 4   (D24)
   ("Number of years embedded in yr 6 estimate" — the lump sum is spread over this many
    years as a level annuity. The cell comment at D33 saying "annuity for ten years" is
    stale boilerplate; the actual annuity length is D24.)
AnnuityPayment_beyond = B15 / N_beyond = 8000/4 = 2000                                (B33)

PV_t = Commitment_t / (1+kd)^t  for t = 1..5                                          (C28:C32)
   e.g. C28 = 2000/1.0548 = 1896.0940462646947 ; C32 = 1600/1.0548^5 = 1225.3760197097213
PV_beyond = [AnnuityPayment_beyond · (1 − (1+kd)^−N_beyond)/kd] / (1+kd)^5
          = [2000·(1 − 1.0548^−4)/0.0548] / 1.0548^5 = 5371.386001674705              (C33)
   (annuity valued at end of year 5, then discounted 5 years back)

DebtValueOfLeases = Σ PV = 13448.731193418043                                         (C34)

Restated financials ("short cut"):
AdjustedEBIT_shortcut = D20 + DebtValueOfLeases·kd
                      = 10000 + 13448.731·0.0548 = 10736.990469399308                 (F37)
AdjustedDebt = D21 + DebtValueOfLeases = 38448.73119341805                            (F38)

Full adjustment:
LeaseLife = 5 + N_beyond = 9
DepreciationOnLeasedAsset = DebtValueOfLeases / LeaseLife
                          = 13448.731193418043/9 = 1494.3034659353382                 (D44)
AdjustedEBIT_full = D20 + E7 − DepreciationOnLeasedAsset
                  = 10000 + 2500 − 1494.303 = 11005.696534064662                      (D45)
```

(D22 Reported Interest Expenses is collected as an input but does not feed any output cell in
this sheet — carried for the user's ratio work.)

**Reference data:** none.

#### Outputs

- C34: Debt value of operating leases = 13448.73 (add to debt everywhere).
- F37: Adjusted operating income, short cut (EBIT + kd·lease debt) = 10736.99.
- F38: Adjusted total debt = 38448.73.
- D45: Adjusted operating income, full method (EBIT + current lease expense − depreciation on
  the capitalized leased asset) = 11005.70.
- D24: years embedded in the "6 and beyond" lump (4), C28:C33 per-period PVs.

#### Worked example

Commitments 2000/2000/2000/1800/1600 then 8000 beyond year 5; kd = 5.48%. Average of years
1–5 = 1880, so the 8000 lump ≈ 4 years at 2000/yr. PVs: 1896.09, 1797.59, 1704.20, 1454.09,
1225.38, plus a 4-year 2000 annuity discounted from year 5 = 5371.39. Total lease debt
13448.73. Short-cut EBIT: 10000 + 0.0548·13448.73 = 10736.99; full-method EBIT:
10000 + 2500 − 13448.73/9 = 11005.70. Debt restated 25000 → 38448.73.

#### Reimplementation notes

Inputs: `current_lease_expense` (float, currency), `commitments` (list of 5 floats, years
1–5), `beyond_lump` (float), `pretax_cost_of_debt` (float, fraction), `reported_ebit`,
`reported_debt`, `reported_interest_expense` (floats). Outputs: lease debt value, per-period
PVs, n_beyond, adjusted EBIT (both methods), adjusted debt.
Branches/edge cases:
- `beyond_lump = 0` ⇒ N_beyond division still runs; PV_beyond should be 0 (and avoid
  ROUND(0/avg) issues — N_beyond = 0 means skip the annuity and use lease life 5).
- All five commitments zero ⇒ AvgCommitment = 0 ⇒ division by zero computing N_beyond; guard.
- ROUND is standard half-away-from-zero Excel rounding to 0 decimals (Python's
  `round()` banker's rounding differs at .5 — use `math.floor(x+0.5)` semantics).
- N_beyond = 0 after rounding (small lump) ⇒ annuity payment divides by zero; treat lump as
  a single year-6 payment or zero, and set LeaseLife = 5.
- The five-year footnote format is US GAAP-specific; fewer years of commitments requires
  generalizing the "5" constants (base years, annuity start, LeaseLife = base + N_beyond).
- kd = 0 breaks the annuity formula (use N_beyond·payment undiscounted).
