# Regression beta, Jensen's alpha and R² as a performance diagnostic

**Core idea:** Running the stock's returns against the market gives three numbers, and the project asks for all three. The slope is the regression beta — a backward-looking risk measure. The intercept, adjusted for the risk-free rate, is Jensen's alpha — the excess return the stock delivered beyond what CAPM predicted, which is the project's measure of "how much of the performance is attributable to management." R² says how much of the stock's variation the market explains, which is also the split between market risk and firm-specific risk. The diagnostic answers a project question the DCF never touches: would an investor in this stock have beaten the market, and why?

**Formulas:**
- Regression: R_stock = a + b·R_market + ε, estimated over a window of periodic returns. b = regression beta; a = intercept.
- Jensen's alpha = a − Rf·(1 − b), where Rf = the risk-free rate over the *return interval* used in the regression and b = regression beta. This converts the raw intercept into excess return over the CAPM-predicted return.
- R² = fraction of variance in the stock's returns explained by market returns. Firm-specific (diversifiable) risk share = 1 − R².

**Procedure:**
1. Regress the stock's returns on a market index over the estimation window (typically weekly or monthly returns over 2-5 years).
2. Record the intercept, the slope (regression beta), the standard error of the beta, and R².
3. Convert the intercept to Jensen's alpha with the formula above, using the risk-free rate stated over the same return interval.
4. Read alpha as performance: positive alpha = the stock beat its CAPM-predicted return; negative alpha = it lagged.
5. Read R² as a risk decomposition: low R² means the price moves largely independently of the market, so most of the risk is firm-specific and diversifiable.
6. Interpret extreme alphas in life-cycle terms. A very large positive alpha is typical of a company early in its growth cycle and is not sustainable evidence of management skill.
7. Connect negative alpha to corporate events. Sustained underperformance is a plausible driver of a management shake-up or of a strategic acquisition.
8. Do **not** use the regression beta as the hurdle-rate beta by default. The project prefers a bottom-up beta for the cost of equity; see [[cost-of-capital-buildup-deliverable]].

**Reference data:** Spring 2015 regression output (weekly-return regressions against a US index).

| Regression | SBUX | MCD | CMG | TSN |
|---|---|---|---|---|
| Regression beta | 0.77 | 0.50 | 0.48 | 0.66 |
| Alpha (raw intercept) | 1.61% | −0.17% | 38.08% | 0.42% |
| Jensen's alpha | 1.11% | −1.25% | 36.95% | −0.32% |
| R² | 23.50% | 23.50% | 4.40% | 7.80% |

Comparison betas used for the hurdle rate at the same date (bottom-up levered): SBUX 0.85, MCD 0.97, CMG 0.73, TSN 1.09. Note that the regression beta and the bottom-up beta disagree materially for McDonald's (0.50 vs 0.97).

Published data set for this part: Jensen's alpha by industry.

**Worked example:** Chipotle, 2015. Raw intercept 38.08%; Jensen's alpha 36.95% — an enormous abnormal return relative to CAPM. The team read it not as evidence of permanent management genius but as the signature of a company early in its growth cycle. Its R² is 4.40%, meaning the market explains under 5% of Chipotle's price movement; nearly all of its risk is firm-specific. McDonald's shows the opposite pattern: Jensen's alpha −1.25%, and the team connected the underperformance to the recent change in upper management. Tyson's −0.32% alpha is paired with its failure to earn its cost of capital and its Hillshire acquisition.

**Determinism:** DETERMINISTIC — given a return series for the stock and index plus a risk-free rate, a script produces beta, intercept, standard error, R² and Jensen's alpha exactly. JUDGMENT — the estimation window, the return interval, the index chosen, and the *reading*: whether a positive alpha is skill, luck or a growth-cycle artifact, and whether a negative alpha explains a corporate action. That reading needs the company's news history and life-cycle stage.

**Pitfalls:**
- Reporting the raw intercept as Jensen's alpha. The Rf·(1 − b) adjustment is required.
- Using the regression beta in the cost of equity when R² is low and the standard error is large. Low-R² regressions (Chipotle 4.4%, Tyson 7.8%) produce betas with wide confidence intervals.
- Reading a low regression beta as low risk. It can mean the business simply does not move with the market — non-cyclical demand in food processing and fast food produced low betas across this whole set.
- Annualization mismatch. Alpha and Rf must be stated over the same interval as the returns in the regression.

**Sources:**
- corporate_finance--project--cfproj p.6
- corporate_finance--project--food2015 p.7, p.2

**Related:** [[cost-of-capital-buildup-deliverable]], [[corporate-finance-project-blueprint]], [[return-spread-and-eva-analysis]], [[project-executive-summary-scorecard]]
