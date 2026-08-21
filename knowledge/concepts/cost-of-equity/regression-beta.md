# Regression (top-down) beta and why it fails

**Core idea:** The standard way to estimate beta is to regress a stock's returns against a market index's returns. The slope is the beta. This regression beta has three structural problems: it carries a high standard error, it reflects the firm's business mix over the *past* estimation window rather than today's, and it reflects the firm's *average* leverage over that window rather than its current leverage. On top of that, it is manipulable — an analyst can shop across listings, indices, periods, and return intervals until the beta says what they want. A regression beta can be unreliable when the statistics look bad **and** when they look good. Damodaran's conclusion is to prefer a bottom-up beta and to use the regression mainly as a diagnostic.

**Formulas:**
- Regression: **R_j = a + b × R_m**, where R_j = stock returns, R_m = market index returns, a = intercept, b = slope = **beta**.
- Beta = Covariance(R_j, R_m) / Variance(R_m).
- Return in a period = (Price_end − Price_beginning + Dividends in period) / Price_beginning. Count dividends only in the ex-dividend period. With splits: R = (Price_end × Split factor + DPS − Price_beginning) / Price_beginning.
- **R² = proportion of the firm's variance that is market risk.** 1 − R² = firm-specific (diversifiable) risk. Systematic variance = β² × Var(market); unsystematic variance = Var(stock) − systematic variance.
- Confidence ranges: 67% range = beta ± 1 standard error; 95% range = beta ± 2 standard errors.
- Bloomberg adjusted beta = **0.67 × Raw beta + 0.33 × 1.0** (equivalently 2/3 raw + 1/3 market), a mechanical shrink toward 1.
- Portfolio/merged-firm beta = Σ_i (w_i × β_i), with w_i = market-value weights. A firm's beta is the value-weighted average of its divisions' betas.

**Procedure:**
1. **Estimation period.** Commercial services use 2 to 5 years. Longer gives more observations but a staler business mix; shorter is more exposed to one-off firm-specific events.
2. **Return interval.** Daily, weekly, or monthly. Shorter intervals give more observations but more noise, and non-trading biases all betas toward 1 for illiquid stocks. Damodaran's default for Disney: 5 years of monthly returns.
3. **Compute returns including dividends** for both stock and index, over identical intervals, adjusting for splits.
4. **Choose the market index.** This is the most consequential and most abusable choice — see the reference data. Use an index that represents the marginal investor's portfolio.
5. **Run OLS.** Record slope (beta), intercept, R², standard error of beta, t-statistic, and number of observations.
6. **Diagnose before using:**
   - Standard error. Report the 67% and 95% ranges. If the 95% range spans 0.6 to 2.6, the beta is close to useless.
   - R². Below ~0.10 the market explains almost nothing about the stock.
   - Index domination. A very high R² can be an artifact of the stock being a huge share of its own index.
   - Regime change. If the company or the stock's behavior changed inside the window, the estimate is about a company that no longer exists.
7. **Remember what you have.** A regression beta is a **levered** beta (it comes from stock prices, which embed leverage) and it reflects the *average* D/E over the window, not today's. To use it forward, unlever at the average D/E and relever at the current D/E — see [[levering-and-unlevering-beta]].
8. Extract the second output: the intercept, which gives Jensen's alpha — see [[jensen-alpha]].
9. Prefer a bottom-up beta for the actual cost of equity — see [[bottom-up-beta]].

**Reference data:**

Regression betas that look bad, and are bad — GoPro (GPRO) vs S&P 500, weekly, 2014-2016:

| Statistic | Value |
|---|---|
| Raw beta | 1.604 |
| Adjusted beta | 1.403 |
| Alpha (intercept) | −0.835 |
| R² | 0.095 |
| Correlation | 0.309 |
| Std error of beta | 0.497 |
| t-statistic | 3.230 |
| Observations | 101 |

Only 9.5% of GoPro's risk is market risk, and the 95% range for beta runs roughly 0.6 to 2.6.

Regression betas that look superb, and are still misleading — Nokia vs the Helsinki HEX index, weekly, 8/1998-8/2000: raw beta 1.27, adjusted 1.18, alpha 0.42, R² **0.94**, std error of beta **0.03**, 103 points. Nokia was roughly 70% of the HEX index, so the regression was effectively running the stock against itself. A tight fit does not mean the beta measures Nokia's risk to a globally diversified investor.

One slice of history — GameStop (GME) vs S&P 500, weekly, 2/2019-2/2020: raw beta **−0.619**, adjusted −0.080, alpha 6.230, R² 0.002, std error of beta 1.319, 104 points. The stock then went from single digits to about $400 in January 2021 and stood at $50.99 on 2/12/2021. The regression says nothing about forward-looking risk. Valeant Pharmaceuticals over 2014-2016 is the same lesson: raw beta 0.355, R² 0.004, std error 0.535, estimated while the company was collapsing.

Game playing through index choice — Bombardier, same 2014-2016 weekly window:

| Listing / index | Raw beta | Adjusted beta | R² | Std error |
|---|---|---|---|---|
| BDRBF (US) vs S&P 500 | 1.704 | 1.470 | 0.093 | 0.529 |
| BBD/B (Canada) vs S&P/TSX Composite | 1.206 | 1.137 | 0.060 | 0.476 |

Same firm, same period, betas 0.5 apart. Vale shows the same effect: Brazilian preferred shares vs Bovespa give raw beta 0.890 (R² 0.570, SE 0.101), while the US ADR vs S&P 500 gives raw beta 1.365 (R² 0.412, SE 0.214). Deutsche Bank vs the DAX gives beta 1.58 (SE 0.21, R² 51%) but vs the FTSE Euro 100 gives 1.98 (SE 0.29, R² 29%). Baidu vs the S&P 500 gives 1.63 (SE 0.28, R² 37%) and vs NASDAQ 1.65 (SE 0.23, R² 47%).

Distribution of standard errors of beta across US stocks (approximate firm counts): <0.10 ≈ 230; 0.10-0.20 ≈ 580; 0.20-0.30 ≈ 1,550; 0.30-0.40 ≈ 1,440; 0.40-0.50 ≈ 750; 0.50-0.75 ≈ 600; >0.75 ≈ 500. Most betas are estimated with substantial error.

A clean regression for contrast — Disney vs S&P 500, monthly, 10/2008-9/2013 (60 points): Return_Disney = 0.0071 + 1.2517 × Return_Market; std error of beta 0.10; R² 0.734; correlation 0.857; t-statistic 12.659. Bloomberg's screen for the same data reports raw beta 1.247, adjusted beta 1.165, alpha 0.599 (monthly %), std dev of error 3.957, std error of alpha 0.516. Beta 1.25 with SE 0.10 gives a 67% range of 1.15-1.35 and a 95% range of 1.05-1.45. R² = 73% means 73% of Disney's risk is market risk and 27% is firm-specific.

Tata Motors vs the S&P BSE Sensex, monthly, 9/2008-9/2013: raw beta 1.831, adjusted 1.554, alpha 2.282, R² 0.690, std error of beta 0.161, t 11.349, 60 points → 67% range 1.67-1.99; 69% market risk / 31% firm-specific.

**Worked example (Disney, monthly return computation):** End-November 2009 price $30.22; end-December 2009 price $32.25; dividends in the ex-dividend month $0.35. Return = (32.25 − 30.22 + 0.35) / 30.22 = **7.88%**. The S&P 500 over the same month: 1095.63 → 1115.10 with index dividends of 1.683, so the market return = (1115.10 − 1095.63 + 1.683) / 1095.63 = **1.78%**. Sixty such pairs give the regression above: slope 1.2517, R² 0.734, standard error 0.10.

**Worked example (variance decomposition, `risk.xls`):** With 52 monthly return pairs, β = ΣK/ΣJ = 1.77881 where J and K accumulate (R_m − R̄_m)² and (R_j − R̄_j)(R_m − R̄_m). Intercept = R̄_j − β·R̄_m = −0.00447. Var(stock) = 0.01911, Var(market) = 0.00278, systematic variance = β²·Var(market) = 0.00880, unsystematic = 0.01031, R² = 0.46028. So 46% of that stock's variance was market-driven.

**Determinism:**
- DETERMINISTIC: (price series, dividend series, split factors, index series) → returns → OLS slope, intercept, R², standard error, t-statistic; (beta, SE) → confidence ranges; (raw beta) → Bloomberg adjusted beta; (R²) → market/firm-specific split; (component betas, market-value weights) → portfolio or merged-firm beta.
- JUDGMENT: estimation period, return interval, and market index; whether the resulting beta is usable at all; whether the company changed inside the window; whether the stock dominates its own index.

**Pitfalls:**
- Reporting a beta as a point estimate with no standard error. Most US betas have SEs between 0.20 and 0.40.
- Trusting a high R² blindly. Nokia's 0.94 came from regressing a stock against an index it dominated.
- Using a beta estimated across a crisis or a short squeeze (Valeant, GameStop) as a forward-looking risk measure.
- Index shopping. Betas differ by 0.5 across listings for the same company in the same period.
- Forgetting that the regression beta is levered at the *average* leverage over the window, not today's.
- Using an adjusted beta (0.67 raw + 0.33) without knowing that the adjustment is a mechanical shrink toward 1, not an estimate of anything.
- Choosing between two equal-beta stocks on R². A diversified investor should be indifferent; only an undiversified investor prefers the higher-R² stock.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.81-86
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.79-84
- corporate_finance--lecture_slides--cfpacket1spr20 p.132, p.134-136, p.139-143, p.149-151, p.161
- spreadsheet `risk.xls` (Corporate Finance collection): market-model regression from raw price data, with variance decomposition
- spreadsheet `riskchecker.xls` (Corporate Finance collection): beta confidence ranges from raw beta and its standard error

**Related:** [[bottom-up-beta]], [[levering-and-unlevering-beta]], [[jensen-alpha]], [[beta-determinants]], [[capm-cost-of-equity]], [[total-beta]], [[non-traded-asset-betas]]
