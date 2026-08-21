# Moving to the optimal: speed, direction and mechanics

**Core idea:** Once you have an actual and an optimal debt ratio, the analysis ends in one of three verdicts — right mix, under-levered, or over-levered. Two questions follow. How fast should the firm move? And what instruments should it use? Speed depends on urgency: an over-levered firm facing bankruptcy and an under-levered firm facing a takeover both need to move immediately, while everyone else can move gradually. Instruments depend on whether the firm has good projects. A firm with projects earning more than its hurdle rates should fund them with whichever side of the balance sheet it is short of, since that closes the gap while creating value. A firm without good projects must move through financial transactions — buybacks, dividends, debt repayment, or swaps.

**Formulas:**
- Good projects test: `ROE > Cost of equity` and `ROC > Cost of capital`.
- Gradual-path arithmetic: `Expected price appreciation = Cost of equity − Dividend yield`. Equity value grows at that rate if the stock is fairly valued, so the denominator of the debt ratio is a moving target.
- Fast-change mechanics: any transaction that changes D or E changes `d = D/(D+E)` arithmetically.

**Procedure (the decision tree):**
1. **Actual > Optimal (over-levered).** Ask: is the firm under threat of bankruptcy?
   - *Yes* → reduce debt quickly: (a) equity-for-debt swaps, (b) sell assets and use the cash to pay off debt, (c) renegotiate with lenders.
   - *No* → does it have good projects (ROE > cost of equity, ROC > cost of capital)?
     - *Yes* → take the good projects, funding them with new equity or retained earnings.
     - *No* → (a) pay off debt with retained earnings, (b) reduce or eliminate dividends, (c) issue new equity and pay off debt.
2. **Actual < Optimal (under-levered).** Ask: is the firm a takeover target?
   - *Yes* → increase leverage quickly: (a) debt-for-equity swaps, (b) borrow money and buy back shares.
   - *No* → does it have good projects?
     - *Yes* → take the good projects, funding them with debt.
     - *No* → do stockholders like dividends? Yes → pay dividends. No → buy back stock.
3. **Fast mechanics (balance-sheet view).** To *decrease* the debt ratio: sell operating assets and pay down debt; issue new stock to retire debt; get debt holders to accept equity. To *increase* it: sell operating assets and buy back stock or pay a special dividend; borrow and buy back stock or pay a large special dividend.
4. **Gradual mechanics.** Dividends and buybacks shrink equity value; debt repayments shrink debt value. Plan the path against a growing firm value — if equity is fairly valued today it should appreciate at (cost of equity − dividend yield), and debt values move with firm value too.
5. Re-verify the optimum after any material change in business mix or tax rate.

**Reference data:** Return spreads globally (January 2017), which is why the "good projects" branch matters so much — most firms do not have them:

| ROIC − cost of capital | Firms (approx.) |
|---|---|
| −6% or worse | 5,200 |
| −6% to −2% | 5,750 |
| −2% to 0% | 2,150 |
| 0 to 2% | 8,900 |
| 2% to 6% | 2,600 |
| 6% to 10% | 1,800 |
| > 10% | 5,865 |

Grouped: 10,961 firms (33.96%) earn at least 2% *below* their cost of capital; 11,049 (34.23%) run in place within ±2%; 10,264 (31.80%) earn at least 2% above, of which 5,865 clear it by 10% or more.

**Worked example:** Disney through the tree. Actual 11.58% < optimal 40%, so it is under-levered. Is it a takeover target? No — very large market capitalization and a positive Jensen's alpha. Does it have good projects? Yes — ROC exceeds the cost of capital. Conclusion: **move to the optimal gradually, by taking good projects with debt.** The alternative fast route (borrow $39.14B and buy back stock) is available and would be worth roughly $10.90 per share ([[recapitalization-and-buyback-price]]), but the tree does not call for it in the absence of a takeover threat.

**Determinism:**
- DETERMINISTIC: the tree traversal once the three answers are known; the arithmetic effect of any given transaction on the debt ratio; the projected debt-ratio path given planned dividends, buybacks, repayments, cost of equity and dividend yield.
- JUDGMENT: whether the firm faces a real bankruptcy threat; whether it is a plausible takeover target; whether its projects genuinely clear the hurdle rates going forward; whether stockholders prefer dividends or buybacks.

**Pitfalls:**
- Recommending an immediate recapitalization when neither urgency condition holds. Gradual adjustment through project financing avoids transaction costs and preserves flexibility.
- Assuming good projects exist. Roughly a third of global firms earn returns below their cost of capital.
- Planning a gradual path against a static firm value. Equity appreciates, so a fixed dollar buyback program moves the ratio less than expected.
- Using the ROE test alone. Both tests (ROE vs cost of equity, ROC vs cost of capital) should point the same way.
- Forgetting that an over-levered firm with good projects should still take them — funded with equity, not debt.

**Sources:**
- corporate_finance--lecture_slides--cfpacket2spr20 p.88
- corporate_finance--lecture_slides--cfpacket2spr20 p.104-109

**Related:** [[recapitalization-and-buyback-price]], [[cost-of-capital-approach]], [[pathways-to-the-optimal-debt-ratio]], [[downside-risk-and-rating-constraints]], [[pecking-order]], [[debt-design-framework]], [[dividend-policy-framework]], [[jensens-alpha]]
