# Book-value multiples: PBV and EV/Invested Capital

**Core idea:** Price-to-book compares what the market pays for equity with what accountants say the equity cost. Its companion variable is ROE. Divide the dividend discount model by book value and the whole multiple collapses to the gap between what the firm earns on equity and what investors require: PBV = (ROE − g)/(r − g). A firm that earns its cost of equity is worth book value. Earn more, and it trades above book; earn less, and it trades below. The enterprise-value twin works the same way with ROC and the cost of capital: EV/Invested Capital = (ROC − g)/(WACC − g). Because these multiples map so directly onto excess returns, they have the tightest empirical fits of any multiple family. In January 2021 regional EV/IC regressions on ROIC produced R² of 50-63%, the highest of any multiple.

**Formulas:**

Equity side (PBV):
- `P₀ = DPS₁/(r − gn)` with `ROE = EPS₀/BV₀`
- `P₀ = BV₀ × ROE × Payout × (1 + gn)/(r − gn)`
- `PBV = P₀/BV₀ = ROE × Payout × (1 + gn)/(r − gn)` (trailing ROE)
- `PBV = ROE × Payout/(r − gn)` if ROE is based on expected next-period earnings
- Substituting the sustainable growth relation `gn = (1 − Payout) × ROE`: `PBV = (ROE − gn)/(r − gn)`

Enterprise side (EV/Book Capital, a.k.a. EV/Invested Capital):
- `V₀ = FCFF₁/(WACC − g)`
- `FCFF = EBIT(1−t) − (g/ROC) × EBIT(1−t)`, i.e. the reinvestment rate is g/ROC
- `V₀/BV = (ROC − g)/(WACC − g)`

Symbols:
- BV₀ = current book value of equity (per share for PBV per share).
- BV in the enterprise formula = book value of invested capital = Book Equity + Book Debt − Cash.
- ROE = return on equity; ROC (= ROIC) = after-tax return on invested capital.
- r = cost of equity; WACC = cost of capital; gn, g = stable growth; t = tax rate.
- Payout = dividends / net income.

**Procedure:**
1. Compute the firm's ROE (net income / book equity) or ROC (after-tax EBIT / invested capital) for the most recent year, and normalize if the year was unusual.
2. Estimate the cost of equity (for PBV) or cost of capital (for EV/IC), plus a stable growth rate.
3. Compute the justified multiple: (ROE − g)/(r − g) or (ROC − g)/(WACC − g).
4. Apply the decision rule. ROE > cost of equity → PBV should exceed 1. ROE < cost of equity → PBV below 1. ROE = cost of equity → PBV of 1. Same rule with ROC and WACC for EV/IC.
5. Compare with the traded multiple. A firm with low PBV *and* high ROE is the classic cheap candidate; low PBV with low ROE is usually just a bad business.
6. Across a sector, plot PBV against ROE, or regress PBV on ROE plus risk and growth. Points well above the fitted band are expensive for their ROE; points below are cheap.
7. Check for omitted dimensions before acting. Expected growth and risk both shift PBV at a given ROE.

**Reference data:**

European banks, 2010 sample used throughout the lectures (18 banks; sector average PBV 2.05, median 2.07; average ROE 12.54%, median 11.82%; average std deviation 24.99%, median 21.93%):

| Bank | PBV | ROE | Std deviation |
|---|---|---|---|
| Bayerische Hypo-und Vereinsbank | 0.80 | −1.66% | 49.06% |
| Commerzbank | 1.09 | −6.72% | 36.21% |
| Deutsche Bank | 1.23 | 1.32% | 35.79% |
| Banca Intesa | 1.66 | 1.56% | 34.14% |
| BNP Paribas | 1.72 | 12.46% | 31.03% |
| Banco Santander | 1.86 | 11.06% | 28.36% |
| Sanpaolo IMI | 1.96 | 8.55% | 26.64% |
| BBVA | 1.98 | 11.17% | 18.62% |
| Societe Generale | 2.04 | 9.71% | 22.55% |
| Royal Bank of Scotland | 2.09 | 20.22% | 18.35% |
| HBOS | 2.15 | 22.45% | 21.95% |
| Barclays | 2.23 | 21.16% | 20.73% |
| Unicredito Italiano | 2.30 | 14.86% | 13.79% |
| Kredietbank Luxembourgeoise | 2.46 | 17.74% | 12.38% |
| Erste Bank | 2.53 | 10.28% | 21.91% |
| Standard Chartered | 2.59 | 20.18% | 19.93% |
| HSBC | 2.94 | 18.50% | 19.66% |
| Lloyds TSB | 3.33 | 32.84% | 18.66% |

Largest US stocks, January 2010 — multiple regression of PBV:
`Predicted PBV = 0.406 − 0.065 × Beta + 9.340 × Expected 5-yr EPS growth + 10.546 × ROE` (growth and ROE as decimals)

| Variable | B | Std. Error | Std. Beta | t | Sig. |
|---|---|---|---|---|---|
| Constant | 0.406 | 0.424 | — | 0.958 | 0.340 |
| Regression Beta | −0.065 | 0.253 | −0.015 | −0.256 | 0.799 |
| Expected growth (5 yrs) | 9.340 | 2.366 | 0.228 | 3.947 | 0.000 |
| ROE | 10.546 | 0.771 | 0.777 | 13.672 | 0.000 |

R = 0.819, R² = 0.670, adjusted R² = 0.661. ROE dominates; beta is insignificant once ROE and growth are in.

Simple bivariate fits of PBV on ROE for large US firms: January 2010 R² = 0.592; January 2020 fitted line `PBV = 0.54 + 0.26 × ROE` (ROE in percentage points) with R² = 0.490. The ROE-PBV link survives a decade, though the fit loosens.

Regional PBV regressions, January 2021 (beta, payout, expected EPS growth, ROE; growth/ROE as decimals):

| Region | Regression | R² |
|---|---|---|
| US | PBV = 1.72 − 1.13 Beta + 0.50 Payout + 11.00 g_EPS + 11.10 ROE | 45.2% |
| Europe | PBV = 3.11 − 1.17 Beta + 0.20 Payout + 4.30 g_EPS + 10.30 ROE | 34.9% |
| Japan | PBV = 0.98 + 0.47 Beta − 0.20 Payout + 11.20 g_EPS + 14.60 ROE | 27.8% |
| Emerging Markets | PBV = −0.32 − 0.05 Beta + 0.90 Payout + 5.00 g_EPS + 17.20 ROE | 48.3% |
| Australia, NZ, Canada | PBV = 1.73 − 1.22 Beta + 0.30 Payout + 3.90 g_EPS + 9.80 ROE | 32.4% |
| Global | PBV = 1.61 − 0.70 Beta + 0.40 Payout + 6.10 g_EPS + 12.40 ROE | 39.1% |

Regional EV/Invested Capital regressions (debt ratio, expected revenue growth, ROIC):

| Region | Regression | R² |
|---|---|---|
| United States | EV/IC = 4.29 − 4.20 DFR + 2.10 g + 6.00 ROIC | 57.3% |
| Europe | EV/IC = 3.77 − 3.70 DFR + 0.80 g + 6.20 ROIC | 57.9% |
| Japan | EV/IC = 3.04 − 3.10 DFR + 6.10 g + 5.30 ROIC | 50.5% |
| Emerging Markets | EV/IC = 3.14 − 3.70 DFR + 2.50 g + 7.50 ROIC | 62.8% |
| Australia, NZ & Canada | EV/IC = 2.87 − 2.60 DFR + 0.80 g + 4.30 ROIC | 50.9% |
| Global | EV/IC = 3.62 − 3.70 DFR + 1.70 g + 6.70 ROIC | 57.5% |

DFR = debt ratio = Total Debt/(Total Debt + Market value of equity).

Cross-market PBV medians, January 2013: US 1.54, Europe 1.22, Japan 0.67, Aus/NZ/Canada 1.21, Emerging Markets 1.18, Global 1.16. Japan's persistent discount is the standing exam question — cheap, or justified by low ROE?

**Worked example:** A bank with ROE 20.22% and a cost of equity of 9%, in stable growth at 4%. Justified PBV = (0.2022 − 0.04)/(0.09 − 0.04) = 3.24. It trades at 2.09 (Royal Bank of Scotland in the 2010 sample). On the fundamental formula it looks cheap. The peer regression run on that sample (`PBV = 2.27 + 3.63 × ROE − 2.68 × Std dev`) predicts 2.51 for RBS, and its actual 2.09 is 16.65% below — the most undervalued bank in the sample on that metric. Two different benchmarks, same direction.

**Determinism:** DETERMINISTIC — the justified PBV or EV/IC from ROE/ROC, growth and discount rate; predicted values from any regression above; the above/below-one screen. JUDGMENT — normalizing ROE (especially for banks and cyclical firms), choosing the cost of equity, deciding whether the book value is economically meaningful, and interpreting outliers on a scatter.

**Pitfalls:**
- Buying low PBV without checking ROE. Low PBV with low ROE is deserved, not cheap.
- Comparing PBV across markets with different accounting for goodwill, write-offs, and buybacks; book equity is an accounting number.
- Using PBV where book value is meaningless (firms with large intangibles, heavy buyback history, or negative book equity).
- Forgetting the growth dimension. Firms that look mispriced on PBV-vs-ROE alone are often explained by expected growth.
- Applying the equity multiple to a firm-level cash flow, or the reverse. Use PBV with equity book value and EV/IC with invested capital.

**Sources:**
- valpacket2spr21 p.42-44, p.60, p.64-68, p.96, p.99
- valpacket2spr20 p.42-44, p.60, p.64-68, p.94, p.97

**Related:** [[intrinsic-multiple-derivation]], [[sector-regressions]], [[comparable-selection-and-controls]], [[cross-market-multiple-regressions]], [[ev-ebitda-multiple]], [[industry-average-multiples]], [[return-on-equity]], [[return-on-invested-capital]], [[excess-returns]]
