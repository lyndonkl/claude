# Macro sensitivity regressions for firm-wide debt design

**Core idea:** Treat the firm as a portfolio of projects and let its own history tell you what kind of debt it needs. Regress annual changes in firm value and in operating income against four macroeconomic variables — interest rates, real GDP, inflation and the exchange rate. Each slope answers a design question. The interest-rate slope on firm value is an empirical estimate of the duration of the firm's assets, which sets debt maturity. The GDP slope measures cyclicality, which tells you whether to borrow less or to add cash-flow-linked features. The currency slope tells you how much debt to issue in foreign currencies. The inflation slope on operating income tells you whether the firm has pricing power, which decides the fixed-versus-floating mix. Firm-specific slopes are noisy, so the bottom-up fix is to use sector-average coefficients weighted by business value, exactly as with bottom-up betas.

**Formulas:**
- Firm value change: `ΔV_t = (MarketCap_t + Debt_t) / (MarketCap_{t−1} + Debt_{t−1}) − 1`.
- Operating income change: `ΔOI_t = OI_t / OI_{t−1} − 1`.
- Four univariate OLS regressions per dependent variable (they are separate simple regressions, not one multiple regression):
  `ΔV = a + b × Δ(T.Bond rate)`, `ΔV = a + b × %ΔGDP`, `ΔV = a + b × Δ(inflation rate)`, `ΔV = a + b × %Δ(dollar)` — and the same four on ΔOI.
- `Duration of the firm's assets = max(0, −slope of ΔV on Δ interest rates)`.
- `Cyclicality = slope on %ΔGDP`; `Inflation sensitivity = slope on Δ inflation`; `Currency sensitivity = slope on %Δ dollar`.
- Bottom-up version: `Firm coefficient = Σ_i (weight_i × sector coefficient_i)`, with weights equal to business values.
- Variable conventions that must be respected: the bond-rate change and the inflation-rate change are **absolute** changes in the rate; GDP and the dollar are **percentage** changes.

**Procedure:**
1. Assemble the firm's annual (or quarterly) operating income, market capitalization and total debt, most recent period first. Use at least 4 periods; the source model allows up to 48. Skip firms listed three years or less.
2. Convert to changes: percent change in operating income, percent change in firm value (market cap + debt).
3. Pull the matching macro change series for the same fiscal years — T.Bond rate change, real GDP growth, change in the CPI inflation rate, percent change in the trade-weighted dollar.
4. Run the eight univariate regressions and record slopes and t-statistics.
5. Interpret:
   - *Interest rates.* The firm-value slope is the asset duration. The operating-income slope decides fixed versus floating: if operating income rises when rates rise, floating rate debt matches better.
   - *GDP.* Significant positive slopes mean the firm is cyclical. A cyclical firm should either issue less debt overall or add features tying debt payments to its own cash flows.
   - *Currency.* If value or income falls when the dollar strengthens, issue some debt in the currencies where revenues are earned.
   - *Inflation.* If operating income rises with inflation, the firm has pricing power and should carry a larger floating rate component.
6. Check the standard errors. These coefficients are typically noisy; a slope with a t-statistic below 2 should not drive a financing decision on its own.
7. If the firm-level estimates are unreliable or the firm has distinct businesses, switch to bottom-up: look up each business's sector coefficients, weight them by business value, and aggregate.
8. Translate the aggregate coefficients into a debt design: target duration, floating-rate share, and foreign-currency share ([[debt-design-framework]]).

**Reference data:**

*Disney's four regressions, 1985–2013 (t-statistics in parentheses):*

| Regression | Equation | Reading |
|---|---|---|
| Firm value vs. interest rates | ΔV = 0.1790 − 2.3251 × Δ rates (2.74; 0.39) | Asset duration ≈ 2.33 years, but insignificant |
| Operating income vs. interest rates | ΔOI = 0.1698 − 7.9339 × Δ rates (2.69; 1.40) | Operating income far more rate-sensitive than value |
| Firm value vs. GDP | ΔV = 0.0067 + 6.7000 × GDP growth (0.06; 2.03) | Significantly cyclical |
| Operating income vs. GDP | ΔOI = 0.0142 + 6.6443 × GDP growth (0.13; 2.05) | Significantly cyclical |
| Firm value vs. dollar | ΔV = 0.1774 − 0.5705 × Δ$ (2.76; 0.67) | Value falls as the dollar strengthens, but insignificant |
| Operating income vs. dollar | ΔOI = 0.1680 − 1.6773 × Δ$ (2.82; 2.13) | A stronger dollar significantly hurts operating income |
| Firm value vs. inflation | ΔV = 0.1855 + 2.9966 × Δ inflation (2.96; 0.90) | Value rises with inflation, weakly |
| Operating income vs. inflation | ΔOI = 0.1919 + 8.1867 × Δ inflation (3.43; 2.76) | Operating income rises with inflation → pricing power |

*Bottom-up sector coefficients for Disney's businesses (weighted by business value):*

| Business | Interest rates | GDP growth | Inflation | Currency | Weight |
|---|---|---|---|---|---|
| Media Networks | −3.70 | 0.56 | 1.41 | −1.23 | 49.27% |
| Parks & Resorts | −4.50 | 0.70 | −3.05 | −1.58 | 33.81% |
| Studio Entertainment | −6.47 | 0.22 | −1.45 | −3.21 | 13.49% |
| Consumer Products | −4.88 | 0.13 | −5.51 | −3.01 | 2.18% |
| Interactive | −1.01 | 0.25 | −3.55 | −2.86 | 1.25% |
| **Disney Operations** | **−4.34** | **0.55** | **−0.70** | **−1.67** | **100%** |

*Macro series conventions (from the FRED-sourced data sheets in macrodur.xls):* T.Bond rate = ten-year US Treasury (DGS10) with absolute changes; real GDP = GDPC1 with percent changes; CPI = the CPI inflation rate (CPIAUCSL_PC1) with absolute changes in the rate; dollar = the trade-weighted broad dollar index with percent changes. Sample annual values: 2019 rate 1.92% (change −0.75%), GDP growth 2.32%, inflation 2.29% (change +0.33%), dollar change −0.77%; 2018 rate 2.69% (change +0.27%), GDP growth 3.07%, inflation 1.95% (change −0.16%), dollar change +4.99%; 2009 rate 3.85% (change +1.56%), GDP growth 0.18%, inflation 2.81% (change +2.84%), dollar change −5.82%.

*Sector coefficient tables* exist by 4-digit SIC (two blocks: firm-value and operating-income slopes for duration, cyclicality, inflation and currency; the sheet's guidance is to use the **firm-value** columns for duration and cyclicality, and the **operating-income** columns for inflation and currency) and by 2-digit broad industry group. Example 2-digit rows (duration / cyclicality / inflation / currency): Amusement & Recreation Services 5.01 / 0.69 / 0.58 / −1.14; Communications 6.59 / 0.96 / 0.10 / −0.95; Motion Pictures 5.36 / 0.51 / 4.34 / −2.45; General Merchandise Stores 4.22 / 0.93 / 0.63 / 0.46; Food Stores 3.41 / 0.91 / 2.23 / −1.47; Oil & Gas Extraction 4.21 / 0.53 / 2.99 / −2.50; Transportation by Air 2.70 / 0.98 / −0.98 / 0.65; Depository Institutions 4.96 / 1.01 / −1.07 / 0.66. Watch the sign conventions: the SIC sheet stores raw slopes (negative duration means value falls as rates rise), while the bottom-up estimator stores sign-flipped values.

**Worked example:** Disney's design recommendation, built from the bottom-up coefficients. Duration −4.34 → debt should be long term with a duration of about 4.3 years. Operating income rises with inflation (slope +8.19, t = 2.76) and with interest rates, so a significant portion of the debt should be floating rate. The currency coefficient of −1.67 says a stronger dollar hurts, so part of the debt should be in foreign currencies; based on 2013 revenue geography, about **18%** of the debt should be non-dollar, and perhaps more, since even dollar-denominated income is exposed to currency moves. The specific currencies should follow where Disney earns revenues.

**Determinism:**
- DETERMINISTIC: operating income, market cap and debt histories plus the macro series → percent/absolute changes → OLS slopes, t-statistics, and the derived duration/cyclicality/inflation/currency measures. The bottom-up aggregation is a weighted average. Fully scriptable.
- JUDGMENT: choosing the estimation window and frequency; deciding whether a slope is reliable enough to act on; deciding when to abandon firm-specific estimates for sector averages; translating coefficients into a target foreign-currency share and floating-rate share; identifying the specific currencies.

**Pitfalls:**
- Acting on statistically insignificant slopes. Disney's firm-value duration coefficient has a t-statistic of 0.39.
- Running one multiple regression when the source model runs four separate simple regressions — the numbers will not match.
- Mixing change conventions. Interest rate and inflation changes are absolute; GDP and currency changes are percentages.
- Negative or near-zero operating income in a period makes its percent change meaningless.
- Using firm-value duration when the interest-rate slope is positive; the model floors duration at zero in that case.
- Losing track of the sign conventions between the sector-average sheet and the bottom-up estimator.
- Assuming the past relationship is stable. The regression approach assumes past project cash flows resemble future ones and that market value changes track firm value changes.

**Sources:**
- corporate_finance--lecture_slides--cfpacket2spr20 p.127-131
- corporate_finance--lecture_slides--cfpacket2spr20 p.133-142
- corpfin-capital-structure — macrodur.xls (`Inputs for top down`, `Duration Calculator`, `Bottom up Estimator`, `Annual Data`, `Quarterly Data`, `Sector Averages by SIC`)

**Related:** [[debt-design-framework]], [[project-duration-and-project-financing]], [[bottom-up-beta]], [[cost-of-capital-approach]], [[optimal-debt-ratio-by-firm-type]]
