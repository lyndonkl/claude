# Alternatives to beta: the menu of relative risk measures

**Core idea:** Rejecting betas or modern portfolio theory does not free you from measuring relative risk. It only changes the instrument. Two questions organize the whole menu. First, do you believe the marginal investors who price the asset are diversified? Second, do you believe price-based risk measures? The four answer combinations point to four different families of measure, from the CAPM at one corner to accounting-ratio risk scores at the other. Every family still produces a number that scales a risk premium, so you cannot escape the estimation problem — you can only relocate it.

**Formulas:**
- Relative volatility = Standard deviation of the stock / Average standard deviation across all stocks. (Captures **total** risk, not just market risk.)
- CAPM Plus: Cost of equity = R_f + β × ERP + additional proxy premiums (e.g. a small-cap premium).
- Proxy model: E(R) = a + Σ_j b_j Y_j, estimated by regressing historical returns of individual stocks on firm fundamentals Y_j (market cap, momentum, liquidity, book-to-market).
- Accounting beta: run the beta regression with changes in accounting earnings for the firm against changes in aggregate/market earnings, instead of stock returns against index returns.
- Relative earnings volatility = Standard deviation of the firm's accounting earnings / Average standard deviation of earnings across firms.
- Debt-based: **Cost of equity = Cost of debt × Scaling factor**, where the scaling factor can be derived from implied volatilities of the firm's traded options and debt.
- Total beta = Market beta / Correlation with the market — the price-based, undiversified-investor answer; see [[total-beta]].

**Procedure:**
1. Answer question 1: **is the marginal investor diversified?** Use ownership structure (high institutional holdings → yes; a closely held private firm → no).
2. Answer question 2: **do you trust market-price-based risk measures?** For a thinly traded stock, a private firm, or a company whose stock price is dominated by a single episode, the answer may be no.
3. Read the family off the grid:
   - Diversified + price-based → CAPM, APM, or multi-factor models.
   - Diversified + not price-based → accounting betas, or cost-of-debt-based models.
   - Not diversified + price-based → relative price volatility, proxy models, CAPM Plus, or an implied cost of capital.
   - Not diversified + not price-based → relative earnings volatility, or accounting-ratio-based risk scores.
4. Estimate the chosen measure. Standardize it so that 1.0 means average risk, exactly as beta is standardized.
5. Multiply by an appropriate premium and add the riskfree rate.
6. State clearly what risk your measure captures. Relative volatility and total beta capture total risk. Beta captures only market risk. The two are not interchangeable and give very different costs of equity for the same firm.

**Reference data:**

The decision grid:

| | Price-based measures | Not price-based |
|---|---|---|
| **Marginal investor diversified** | CAPM; APM; multi-factor models | Accounting betas; cost-of-debt-based models |
| **Marginal investor not diversified** | Relative price volatility; proxy models; CAPM Plus; implied cost of capital | Relative earnings volatility; accounting-ratio-based models |

Non-price-based measures in detail:
- **Accounting risk measures**: an accounting beta or relative earnings volatility computed from reported earnings; or a risk score built from balance-sheet ratios such as debt ratios and cash holdings, in the spirit of default-risk scores like the Z-score.
- **Qualitative risk models**: risk assessments based at least partly on qualitative factors such as quality of management.
- **Debt-based measures**: scale the observable cost of debt up to a cost of equity.

Proxy-model history: the approach started with market capitalization (the small-cap effect) and has since accumulated momentum, liquidity, and other variables. CAPM Plus is the hybrid — keep the CAPM and bolt an extra premium on for each proxy.

**Worked example:** A closely held private manufacturer has no traded stock and an undiversified owner. Question 1 answers "not diversified"; question 2 answers "no price data exists", so you land in the bottom-right cell — relative earnings volatility or accounting ratios. In practice the packet's preferred route for such a firm is a hybrid: build a bottom-up beta from listed comparables (see [[non-traded-asset-betas]]), then convert it to a total beta to reflect the owner's lack of diversification (see [[total-beta]]). For Bookscape, that raised the beta from 0.8558 to 1.6783 and the cost of equity from 7.46% to 11.98%.

**Determinism:**
- DETERMINISTIC: (stock return series, cross-sectional average volatility) → relative volatility; (earnings series) → accounting beta or relative earnings volatility; (returns panel, fundamentals panel) → proxy-model regression coefficients; (cost of debt, scaling factor) → cost of equity.
- JUDGMENT: whether the marginal investor is diversified; whether to trust prices; which proxies belong in a proxy model and what premium each earns; the scaling factor in the debt-based model; the entire content of a qualitative risk model.

**Pitfalls:**
- Treating relative volatility as a substitute for beta. It measures total risk, so it produces a higher cost of equity for the same firm, and mixing the two across comparables makes results incomparable.
- Adding a small-cap premium on top of a bottom-up beta that already came from small-cap comparables — the premium gets counted twice.
- Using accounting betas from annual data. You get four or five observations per decade, so the standard errors are enormous.
- Building a qualitative risk model and presenting its output as if it were estimated.
- Forgetting that leaving the CAPM does not remove the need to justify your risk measure. It raises the bar.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.87-89
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.85-87
- corporate_finance--lecture_slides--cfpacket1spr20 p.93-95

**Related:** [[capm-cost-of-equity]], [[total-beta]], [[non-traded-asset-betas]], [[regression-beta]], [[bottom-up-beta]], [[cost-of-debt]]
