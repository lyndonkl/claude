# FCFE for banks and financial service firms

**Core idea:** The standard FCFE formula breaks down for a bank. Capital expenditures and non-cash working capital are meaningless for a firm whose raw material is capital itself, and debt is not a financing choice but a component of the product. The fix is to redefine reinvestment as **investment in regulatory capital**. A bank that wants to grow its loan book must hold more book equity to satisfy its capital ratio, and that retained equity is exactly the cash it cannot pay out. So a bank's potential dividend is net income minus the increase in regulatory capital required to support asset growth. This matters because banks with thin capital and growing assets often have deeply negative FCFE while still paying dividends — a payout that is being funded by capital the regulator expects them to hold.

**Formulas:**

**FCFE (bank) = Net Income − Investment in Regulatory Capital**

Where the pieces are built up as:
- Tier 1 Capital_t = Risk-Adjusted Assets_t × Tier 1 Capital Ratio_t
- Investment in Regulatory Capital_t = Tier 1 Capital_t − Tier 1 Capital_(t−1) (the change in regulatory capital)
- Net Income_t = Book Equity_t × Expected ROE_t
- Book Equity_t = Book Equity_(t−1) + Investment in Regulatory Capital_t (equity grows by the retained capital)

Symbols:
- Risk-Adjusted Assets = risk-weighted assets as reported for regulatory purposes; grow them at the expected asset growth rate
- Tier 1 Capital Ratio = required or targeted regulatory capital as a percentage of risk-adjusted assets
- Expected ROE = return on book equity, the driver of projected net income
- Book Equity = book value of equity, the base to which ROE is applied

*Simple loan-book version (when only a capital ratio and loan growth are known):*
FCFE = Net Income − (New Loans − Old Loans) × Capital Ratio

**Procedure:**
1. Establish the current position: risk-adjusted (risk-weighted) assets, current Tier 1 capital, current Tier 1 ratio, book equity, and current net income or ROE.
2. Project risk-adjusted asset growth. Use the bank's expected loan/asset growth rate; a mature bank in a mature market grows at or below nominal GDP growth.
3. Set a path for the Tier 1 capital ratio. If the bank is under-capitalized relative to regulatory requirements or peers, ramp the ratio up over the forecast period rather than jumping in one year. The ramp is the single most consequential assumption: it determines how much capital must be retained.
4. Compute required Tier 1 capital each year = Risk-Adjusted Assets × Tier 1 ratio, then take the year-over-year change. That change is the reinvestment.
5. Project net income. Set a path for ROE that converges to a sustainable level (a troubled bank's ROE should recover gradually toward its cost of equity or a normalized industry level), then apply it to book equity.
6. Compute FCFE = Net Income − Change in Tier 1 Capital for each year.
7. Interpret the sign. Negative FCFE in the early years means the bank cannot fund both its growth and its dividend. A bank paying dividends while FCFE is negative is running down its capital cushion or relying on external issuance.
8. For valuation, use these potential dividends where actual dividends are not reliable — a bank that has stopped paying dividends, or one paying dividends it cannot afford, should be valued on FCFE after regulatory capital rather than on the reported dividend.

**Reference data:**

*Deutsche Bank FCFE projection, November 2013 (€ millions), assets growing 3%/yr and Tier 1 ratio rising to 18%:*

| Item | Current | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| Risk Adjusted Assets | 439,851 | 453,047 | 466,638 | 480,637 | 495,056 | 509,908 |
| Tier 1 as % of Risk Adj assets | 15.13% | 15.71% | 16.28% | 16.85% | 17.43% | 18.00% |
| Tier 1 Capital | 66,561 | 71,156 | 75,967 | 81,002 | 86,271 | 91,783 |
| Change in regulatory capital | — | 4,595 | 4,811 | 5,035 | 5,269 | 5,512 |
| Book Equity | 76,829 | 81,424 | 86,235 | 91,270 | 96,539 | 102,051 |
| ROE (rising to 8%) | −1.08% | 0.74% | 2.55% | 4.37% | 6.18% | 8.00% |
| Net Income | −716 | 602 | 2,203 | 3,988 | 5,971 | 8,164 |
| − Investment in Regulatory Capital | — | 4,595 | 4,811 | 5,035 | 5,269 | 5,512 |
| **FCFE** | — | **−3,993** | **−2,608** | **−1,047** | **702** | **2,652** |

FCFE is negative for the first three years because the capital build exceeds earnings, and turns positive only as ROE recovers to 8%.

*Deutsche Bank, October 2016 re-estimate (€ millions), assets growing 1%/yr, Tier 1 ratio rising from 12.41% to 15.67%:*

| Item | Current | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Risk Adjusted Assets | 445,570 | 450,026 | 454,526 | 459,071 | 463,662 | 468,299 | 472,982 | 477,711 | 482,488 | 487,313 | 492,186 |
| Tier 1 / RAA | 12.41% | 13.74% | 13.95% | 14.17% | 14.38% | 14.60% | 14.81% | 15.03% | 15.24% | 15.46% | 15.67% |
| Tier 1 Capital | 55,282 | 61,834 | 63,427 | 65,045 | 66,690 | 68,361 | 70,059 | 71,784 | 73,537 | 75,317 | 77,126 |
| Change in Tier 1 | | 6,552 | 1,593 | 1,619 | 1,645 | 1,671 | 1,698 | 1,725 | 1,753 | 1,780 | 1,809 |
| Book Equity | 64,609 | 71,161 | 72,754 | 74,372 | 76,017 | 77,688 | 79,386 | 81,111 | 82,864 | 84,644 | 86,453 |
| Expected ROE | −13.70% | −7.18% | −2.84% | 0.06% | 1.99% | 5.85% | 6.57% | 7.29% | 8.00% | 8.72% | 9.44% |
| Net Income | (8,851) | (5,111) | (2,065) | 43 | 1,512 | 4,545 | 5,214 | 5,910 | 6,632 | 7,383 | 8,161 |
| − Investment in Reg. Capital | | 6,552 | 1,593 | 1,619 | 1,645 | 1,671 | 1,698 | 1,725 | 1,753 | 1,780 | 1,809 |
| **FCFE** | | **(11,663)** | **(3,658)** | **(1,576)** | **(133)** | **2,874** | **3,516** | **4,185** | **4,880** | **5,602** | **6,352** |

Context: in 2007 Deutsche Bank paid €2,146M of dividends on net income of €6,510M, and the early-2008 valuation simply discounted those dividends as reasonable and sustainable. By October 2016 the bank had stopped paying dividends, was losing money, and was in deep trouble — so potential dividends had to be rebuilt from regulatory capital.

*Where this fits in model choice:* if you cannot estimate free cash flows to equity or to the firm (typical for financial service firms), the only cash flow you can discount is dividends. If the debt ratio is stable, discount FCFE at the cost of equity. If the debt ratio may change, discount FCFF at the cost of capital.

**Worked example — the simple version:** A bank has $10 billion in loans, $750 million of book equity (a 7.5% capital ratio), expects to grow loans 10% to $11 billion, and expects $150 million of net income.
Investment in regulatory capital = ($11,000M − $10,000M) × 0.075 = **$75M**.
FCFE = $150M − $75M = **$75 million**.
The bank earns $150M but can only pay out half of it; the rest must be retained to support the larger loan book.

Now the same arithmetic on Deutsche Bank's 2016 year 1: Tier 1 capital rises from €55,282M to €61,834M, so investment in regulatory capital = €6,552M. Net income = book equity €71,161M × ROE (−7.18%) = −€5,111M. FCFE = −5,111 − 6,552 = **−€11,663M**. The bank has no capacity to pay dividends at all in that year.

**Determinism:**
- DETERMINISTIC: the entire table. Given risk-adjusted assets, an asset growth rate, a Tier 1 ratio path and an ROE path, every cell — Tier 1 capital, change in regulatory capital, book equity, net income and FCFE — is computed mechanically. A script reproduces the Deutsche Bank tables exactly.
- JUDGMENT: the projections themselves. The asset growth rate, the target Tier 1 ratio and the speed of the ramp, and the ROE recovery path are all estimates. For a troubled bank the ROE path dominates the answer, and it depends on a view of the franchise, the regulatory environment and the credit cycle.

**Pitfalls:**
- Applying the standard cap-ex-and-working-capital FCFE formula to a bank. It produces nonsense; the reinvestment is regulatory capital.
- Using the *current* capital ratio when regulators are forcing it up. The ramp in the ratio is often a larger reinvestment than the asset growth itself — see Deutsche Bank 2016, where year 1's €6,552M capital build is four times the steady-state annual build.
- Trusting the reported dividend at a bank. A bank can pay dividends while FCFE is negative, and did so widely before 2008.
- Forgetting that book equity grows by the retained capital, which then drives next year's net income through ROE. The table is recursive.
- Assuming Tier 1 capital and book equity are the same thing. They differ (Deutsche Bank 2013: Tier 1 €66,561M vs book equity €76,829M); project both and be explicit about which drives reinvestment and which drives income.
- Extrapolating a negative-ROE year forever. The projections require convergence to a sustainable ROE, and that convergence assumption should be stated and defended.

**Sources:**
- corporate_finance--lecture_slides--cfpacket2spr20 p.197
- corporate_finance--lecture_slides--cfpacket2spr20 p.230
- corporate_finance--lecture_slides--cfpacket2spr20 p.234

**Related:** [[fcfe-potential-dividends]], [[cash-trust-assessment]], [[dividend-matrix]], [[peer-group-payout-analysis]], [[dividend-payout-and-yield-measures]], [[dividend-discount-model]], [[cost-of-equity]]
