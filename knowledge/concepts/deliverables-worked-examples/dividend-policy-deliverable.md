# Dividend policy analysis (Parts VIII and IX)

**Core idea:** Two project sections cover cash return. Part VIII describes what the firm has done: dividends versus buybacks, and how much cash it has accumulated. Part IX tests whether that behaviour was right, by comparing the cash the firm *could* have returned — FCFE — against the cash it *did* return. The gap plus the cash balance drives the recommendation. A third leg benchmarks the firm's payout and yield against its peer group and against a cross-sectional regression on global companies. The framing is life-cycle: payout should rise with maturity and fall with growth and reinvestment needs.

**Formulas:**
- Cash returned = Dividends + Buybacks.
- Payout ratio = Dividends / Net income.
- Dividend yield = Dividends per share / Price per share.
- FCFE = free cash flow to equity — the cash left after reinvestment and debt payments.
- Trust metrics: Cash returned / FCFE, and Cash returned / Net income.
- Regression-expected yield and payout: predicted values from a cross-sectional regression run on worldwide comparable companies.

**Procedure:**
1. Record the history of cash return: dividends, buybacks, and the accumulated cash balance.
2. Compute payout ratio and dividend yield for the most recent year.
3. Compute FCFE — cash available after reinvestment and debt payments — over the last few years.
4. Compute cash returned / FCFE and cash returned / net income.
5. Benchmark all four measures three ways: industry average, regression-predicted value, and the firm's own history.
6. Interpret the gap:
   - Cash returned well above FCFE → excess cash being disgorged, typical of a mature firm with limited growth in its core markets.
   - Cash returned below FCFE *with good projects* → a positive signal; the firm is reinvesting and using payout as a signalling tool.
   - Cash returned below FCFE *with poor projects* → the trust problem; management is hoarding cash it cannot invest well.
   - Negative cash returned (net equity issuance) → cash constraint, not policy.
7. Check taxes. Where dividends and capital gains are taxed equally, there is no tax reason to prefer dividends over buybacks, so the choice is about flexibility and signalling.
8. Cross-check against the life-cycle stage and the return spread from Part IV. A firm with a negative ROC−WACC spread should return more, not reinvest more.
9. State the recommendation: return more cash, return less, or hold policy, and in which form.

**Reference data:** Spring 2015 payout and yield versus benchmarks.

| Dividend policy | SBUX | MCD | CMG | TSN |
|---|---|---|---|---|
| Payout ratio | 38.24% | 68.00% | 0% | 12.00% |
| Estimated payout ratio (world regression) | 47.69% | 43.11% | 48.85% | 46.16% |
| Payout, industry average | 53.64% | 55.88% | 55.88% | 40.22% |
| Dividend yield | 1.24% | 3.50% | 0% | 0.71% |
| Estimated dividend yield (world regression) | 3.15% | 3.55% | 2.93% | 2.82% |
| Yield, industry average | 2.06% | 1.88% | 1.88% | 1.89% |
| Revenue growth | 10.63% | −2.36% | 27.80% | 7.99% |

Cash returned versus FCFE:

| Cash returns | SBUX | MCD | CMG | TSN |
|---|---|---|---|---|
| FCFE ($m) | 863 | 2,111 | 429 | 6,320 |
| Dividends ($m) | 513 | 3,216 | 0 | 104 |
| Buybacks ($m) | 313 | 2,964 | 0 | −1,900 |
| Net income ($m) | 1,384 | 4,758 | 445 | 864 |
| Cash returned / FCFE | 95.62% | 292.75% | 0.00% | −31.71% |
| Industry average | 147.94% | 159.83% | 159.83% | 106.84% |
| Cash returned / net income | 59.65% | 129.89% | 0.00% | −231.94% |
| Industry average | 83.11% | 84.98% | 84.98% | 60.34% |

Spreadsheet referenced by the course: dividends.xls. Published data sets: yields and payout by industry; trade-off variables by industry; cap-ex ratios, working-capital ratios and debt ratios by industry.

**Worked example:** All four 2015 firms are US-based, so dividends and capital gains are taxed equally and there is no tax-driven preference between dividends and buybacks. The four sit at four different life-cycle points.
- **McDonald's** is the most mature — revenue growth of −2.36%, a 68% payout ratio, a 3.50% yield. It returned 292.75% of FCFE and 129.89% of net income. It is disgorging excess cash and borrowing in its investment currencies to do so. Its actual yield of 3.50% sits close to its regression-expected 3.55% but far above the 1.88% industry average, which the team read as confirmation of maturity.
- **Starbucks** returned 95.62% of FCFE, below the 147.94% industry average and below its regression-expected payout, because it is still investing in emerging-market growth. Read as a positive signal: dividends and buybacks used as a signalling tool while reinvestment continues.
- **Chipotle** returns nothing at all — a 0% payout with 27.80% revenue growth. Correct for a firm in its expansion phase.
- **Tyson** shows *negative* cash returned. It issued roughly $1.9bn of net equity to protect its rating after the debt-funded Hillshire acquisition, giving −31.71% of FCFE and −231.94% of net income. It reads as a mature company trying to buy its way back onto a growth trajectory. With little excess cash it is unlikely to pay meaningful dividends soon.

**Determinism:** DETERMINISTIC — payout ratio, yield, cash returned, FCFE, both trust ratios, the industry averages, and the regression-predicted yield and payout, given dividends, buybacks, net income, share count, price, and the regression coefficients. JUDGMENT — the interpretation. Whether below-FCFE payout is prudent reinvestment or cash hoarding depends on the quality of the firm's projects, and that comes from the Part IV return spread. The recommendation also needs the life-cycle read, the cash balance, and knowledge of pending transactions.

**Pitfalls:**
- Reading a low payout as bad. It is only bad when the firm's projects fail to clear the hurdle rate.
- Reading cash returned above 100% of FCFE as unsustainable without checking whether the firm is deliberately drawing down an accumulated cash pile or borrowing to fund payout.
- Comparing payout only to the industry average. The cross-sectional regression controls for growth, risk and leverage; the raw average does not.
- Treating negative cash returned as a policy choice. Tyson's negative figure is net equity issuance driven by a rating constraint, not a dividend decision.
- Assuming a tax preference for dividends or buybacks without checking the actual tax regime the shareholders face.

**Sources:**
- corporate_finance--project--cfproj p.11-12
- corporate_finance--project--food2015 p.15-16, p.2

**Related:** [[return-spread-and-eva-analysis]], [[debt-design-deliverable]], [[two-stage-fcff-company-valuation]], [[project-executive-summary-scorecard]], [[corporate-finance-project-blueprint]]
