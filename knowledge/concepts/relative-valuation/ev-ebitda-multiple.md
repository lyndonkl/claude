# EV/EBITDA: determinants and the reinvestment trap

**Core idea:** EV/EBITDA prices the operating assets against pre-tax operating cash flow. Analysts like it because EBITDA is positive far more often than earnings. It also sidesteps leverage and depreciation policy. Its fundamentals come from the FCFF model. Four things drive it: the cost of capital, expected growth, the tax rate, and reinvestment needs. That last one gets forgotten. EBITDA is cash flow *before* the capital spending that keeps the assets running. So a firm that must plough most of its EBITDA back into capital maintenance deserves a low EV/EBITDA. Ryder System at 2.81x against a trucking-sector average of 5.61x is not a bargain. It is a truck-leasing firm with an aging fleet. By the same logic, the deserved EV/EBITDA of an infrastructure business falls as its infrastructure ages.

**Formulas:**
- `EV₀ = FCFF₁/(WACC − g)`
- Expanding FCFF into its EBITDA components:
  `EV = [EBITDA(1−t) + Depr × t − CapEx − ΔWorking Capital]/(WACC − g)`
- Dividing by EBITDA:
```
EV/EBITDA = (1−t)/(WACC−g)
          + [Depr(t)/EBITDA]/(WACC−g)
          − [CapEx/EBITDA]/(WACC−g)
          − [ΔWC/EBITDA]/(WACC−g)
```
- Definitional form: `EV/EBITDA = (MV of equity + MV of debt − Cash)/EBITDA`

Symbols:
- t = tax rate; WACC = cost of capital; g = stable growth rate.
- Depr = depreciation, so Depr × t is the depreciation tax shield.
- CapEx = capital expenditures; ΔWC = change in non-cash working capital.

**Procedure:**
1. Build the numerator consistently: market value of equity plus market value of debt minus cash. Cash comes out because interest income is not in EBITDA.
2. Fix cross-holdings. A consolidated but partly owned subsidiary puts all of its EBITDA in the denominator while you own only part of the equity. Correct for minority interests.
3. For each comparable, compute the reinvestment ratios that drive the multiple: CapEx/EBITDA, Depreciation/EBITDA, ΔWC/EBITDA, and the effective tax rate.
4. Compute the intrinsic EV/EBITDA from the formula above and compare with the traded multiple.
5. When a firm trades far below its sector on EV/EBITDA, check its reinvestment ratios before calling it cheap. High CapEx/EBITDA, high depreciation, or an aging asset base explains a low multiple.
6. Check the tax rate too. Higher effective tax rates mechanically lower the justified multiple.
7. Across a sector or market, control statistically: regress EV/EBITDA on the debt ratio, expected revenue growth, and the tax rate (see reference regressions below).
8. Always locate the multiple in the current distribution before judging it ([[multiple-distribution-statistics]]). Regional medians move by a factor of two.

**Reference data:**

Sensitivity of the intrinsic multiple (from the formula):
- Tax rate 0% → 50%: Value/EBITDA falls from roughly 14x to about 6x.
- Net CapEx as a percent of EBIT 0% → 30%: Value/EBITDA falls from roughly 10x to about 4x.
- Return on capital 6% → 15%: Value/EBITDA rises; and at every ROC level the multiple is higher when WACC is lower (curves drawn for WACC of 8%, 9%, 10%).

Regional EV/EBITDA regressions, January 2021:

| Region | Regression | R² |
|---|---|---|
| United States | EV/EBITDA = 29.71 − 23.80 DFR + 35.00 g − 32.70 Tax Rate | 26.7% |
| Europe | EV/EBITDA = 24.26 − 13.90 DFR + 28.20 g − 7.10 Tax Rate | 15.9% |
| Japan | EV/EBITDA = 20.74 + 9.50 DFR + 85.60 g − 23.70 Tax Rate | 10.3% |
| Emerging Markets | EV/EBITDA = 30.03 − 28.30 DFR + 31.80 g − 17.60 Tax Rate | 27.8% |
| Australia, NZ & Canada | EV/EBITDA = 23.60 − 10.10 DFR + 12.60 g − 15.80 Tax Rate | 10.7% |
| Global | EV/EBITDA = 27.44 − 18.60 DFR + 32.90 g − 18.60 Tax Rate | 21.5% |

DFR = Total Debt/(Total Debt + Market value of equity); g = expected revenue growth, near term; Tax Rate = effective tax rate in the most recent year.

Trucking sector (lecture sample; sector average Value/EBITDA 5.61):

| Company | Value ($m) | EBITDA ($m) | Value/EBITDA |
|---|---|---|---|
| KLLM Trans. Svcs. | 114.32 | 48.81 | 2.34 |
| Ryder System | 5,158.04 | 1,838.26 | 2.81 |
| Rollins Truck Leasing | 1,368.35 | 447.67 | 3.06 |
| Hunt (J.B.) | 982.67 | 310.22 | 3.17 |
| Yellow Corp. | 931.47 | 292.82 | 3.18 |
| Werner Enterprises | 844.39 | 196.15 | 4.30 |
| AMERCO | 1,632.30 | 345.78 | 4.72 |
| USFreightways | 983.86 | 198.91 | 4.95 |
| Arkansas Best | 578.78 | 107.15 | 5.40 |
| Amer. Freightways | 716.15 | 120.94 | 5.92 |
| Swift Transportation | 835.58 | 121.34 | 6.89 |
| CNF Transportation | 2,700.69 | 366.99 | 7.36 |
| Caliber System | 2,514.99 | 333.13 | 7.55 |
| Knight Transportation | 269.01 | 28.20 | 9.54 |
| Heartland Express | 727.50 | 64.62 | 11.26 |
| Mark VII | 160.45 | 12.96 | 12.38 |
| Coach USA | 678.38 | 51.76 | 13.11 |
| US 1 Inds. | 5.60 | (0.17) | NA (negative EBITDA) |

Current sector anchors: the January-2022 US industry-averages dataset gives EV/EBITDA by industry alongside CapEx/Revenues, reinvestment rate and effective tax rate — the exact companion variables this multiple needs ([[industry-average-multiples]]).

**Worked example (intrinsic multiple):** Stable-growth firm with tax rate 36%, CapEx/EBITDA 30%, Depreciation/EBITDA 20%, cost of capital 10%, no working capital needs, growth 5% forever.
```
Value/EBITDA = (1 − 0.36)/(0.10 − 0.05)
             + (0.20 × 0.36)/(0.10 − 0.05)
             − 0.30/(0.10 − 0.05)
             − 0/(0.10 − 0.05)
             = 12.80 + 1.44 − 6.00 − 0 = 8.24
```
Justified EV/EBITDA = 8.24. Raise CapEx/EBITDA to 50% and the multiple drops to 4.24 — the same business, priced at half, purely on reinvestment.

**Determinism:** DETERMINISTIC — the traded multiple from market values, debt, cash and EBITDA; the intrinsic multiple from t, WACC, g, Depr/EBITDA, CapEx/EBITDA and ΔWC/EBITDA; predicted values from the regional regressions. JUDGMENT — normalizing EBITDA, handling cross-holdings and minority interests, deciding whether current reinvestment is representative of future needs, and judging asset age.

**Pitfalls:**
- Reading a low EV/EBITDA as cheap without checking reinvestment needs. This is the most common misuse in the source.
- Leaving cash in the numerator while excluding interest income from EBITDA.
- Ignoring minority interests when the target consolidates partly-owned subsidiaries.
- Applying a fixed rule of thumb ("under 6x is cheap"). In January 2010 the modal US bucket was 4-6x, so 6x was not cheap. By January 2021 the US median was 16.6x, so it was.
- Assuming EV/EBITDA is leverage-neutral in practice. Empirically it falls with the debt ratio in nearly every market.
- Using it for firms with negative EBITDA, which drop out of the sample and bias the comparison.

**Sources:**
- valpacket2spr21 p.11-12, p.45-47, p.69-70, p.97
- valpacket2spr20 p.11-12, p.45-47, p.69-70, p.95
- tables (Jan-2022 US industry averages: EV/EBITDA, CapEx/Revenues, reinvestment rate, effective tax rate)

**Related:** [[intrinsic-multiple-derivation]], [[multiple-definition-tests]], [[multiple-distribution-statistics]], [[book-value-multiples]], [[ev-sales-and-brand-value]], [[cross-market-multiple-regressions]], [[industry-average-multiples]], [[reinvestment-rate]], [[cost-of-capital]]
