# The dividend matrix

**Core idea:** Combine the two verdicts from the cash/trust assessment into a 2×2 matrix and the dividend recommendation falls out. One axis is **cash**: does the firm return less than its FCFE (cash surplus) or more (cash deficit)? The other axis is **project quality**: does it earn excess returns (good projects) or not (poor projects)? Each quadrant has a distinct prescription, and the crucial insight is that in two of the four quadrants the real problem is not the dividend at all — it is the investment policy. The matrix prevents the most common analytical error: recommending a dividend change to fix a problem that dividends cannot fix.

**Formulas:**
- Cash axis: Surplus if (Dividends + Buybacks) < FCFE. Deficit if (Dividends + Buybacks) > FCFE. Use FCFE = Net Income − (Cap Ex − Depreciation)(1 − DR) − ΔWorking Capital × (1 − DR) with DR = debt ratio, and report the pre-debt and actual-debt variants alongside.
- Quality axis: Good projects if ROE > Cost of Equity **and/or** ROC > Cost of Capital, averaged over the period. Poor projects otherwise. Cross-check with Jensen's alpha = Stock Return − Required Return.
- Magnitude of the problem: Cash paid as % of FCFE = (Dividends + Buybacks)/FCFE. Values far from 100% in either direction indicate how urgent the fix is.

**Procedure:**
1. Run the cash/trust assessment first ([[cash-trust-assessment]]) to get both axes.
2. Place the firm in a quadrant. State the FCFE variant used, because the quadrant can change with the variant.
3. Apply the quadrant prescription from the table below.
4. If the firm is in a cash-deficit quadrant, sequence the actions correctly. With poor projects, fix the investment policy first and then cut the payout; cutting the dividend alone leaves the value destruction untouched. With good projects, reduce the payout so the firm can fund its investments internally rather than by issuing equity.
5. If the firm is in a cash-surplus quadrant with poor projects, expect and support stockholder pressure to pay out more. Management has not earned the right to hold the cash.
6. If the firm is in a cash-surplus quadrant with good projects, grant maximum flexibility. The firm can hold cash, pay dividends, or buy back stock as it sees fit.
7. Choose the *form* of any increase in payout using [[cash-returned-dividends-and-buybacks]], and manage the announcement of any cut using [[managing-dividend-changes]].
8. Re-run annually. Firms move between quadrants as management, project quality and cash flows change.

**Reference data — the matrix:**

| | **Poor projects** (ROE < Cost of Equity) | **Good projects** (ROE > Cost of Equity) |
|---|---|---|
| **Cash surplus** (Cash returned < FCFE) | Heavy pressure to pay out more to stockholders, as dividends or buybacks | **Maximum flexibility** in setting dividend policy |
| **Cash deficit** (Cash returned > FCFE) | Cut or end the cash return — but the real problem is investment policy | Reduce cash payout, if any, to stockholders |

*The decision-tree form of the same logic:*
- If FCFE > Dividends (paying out too little) → ask whether you trust the managers with the cash. Judge from the past project record (ROE vs cost of equity, ROC vs WACC). A good history earns managers flexibility to keep the cash and set dividends. A poor history means forcing managers to justify holding cash, or returning it.
- If FCFE < Dividends (paying out too much) → look at investment opportunities. With good projects, cut dividends and reinvest. With poor projects, fix the investment problem first and then cut dividends.

*Case placements from the course (2013 data):*

| Company | Cash position | Project quality | Quadrant prescription |
|---|---|---|---|
| Baidu | Surplus | Good | Maximum flexibility |
| Deutsche Bank | Deficit | Poor | Cut dividends, but the real problem is investment policy |
| Disney (2013) | Deficit (on target-ratio FCFE) | Good | Reduce cash payout |
| Vale | Deficit | Good | Reduce cash payout |
| Tata Motors | Deficit | Good | Reduce cash payout |

**Worked examples:**

*Case 1 — Disney across three decades, showing how a firm moves through the matrix.*
- **2003 (cash surplus, poor projects).** Between 1994 and 2003 Disney generated $969 million of FCFE per year and returned only $639 million per year in dividends and buybacks. Its cash balance exceeded $4 billion at the end of 2003. ROE on projects ran about 2% below the cost of equity per year, and the stock delivered about 3% less than the cost of equity per year, with most of the shortfall after the 1996 Capital Cities acquisition. Verdict: surplus plus poor projects → heavy pressure to pay out. The cash had gone into Capital Cities/ABC and the failed Go.com expansion, so the flexibility Disney might have had a decade earlier was spent. Expect constant stockholder pressure. Note the governance overlay: Michael Eisner had been CEO for a decade and had championed the Cap Cities deal, which is precisely the continuity question that decides whether you extend trust.
- **2009 (trust rebuilt).** Between 2004 and 2008 Eisner was replaced by Bob Iger, who was more responsive to stockholders. Stock performance improved to a positive Jensen's alpha. ROC moved from well below the cost of capital to above it. The firm shifted from returning less than FCFE to returning more, and avoided large acquisitions. The trust that justifies keeping cash was being rebuilt.
- **2013 (cash surplus, good projects → maximum flexibility).** Between 2008 and 2013 dividends and buybacks ran $2.6 billion below FCFE computed at a target debt ratio. Disney kept earning a return on capital well above its cost of capital, and the stock doubled over two years. A firm earning excess returns has earned the freedom to keep cash.

*Case 2 — Vale (cash deficit).* Aggregate over the period, $ millions:

| Item | Aggregate | Average |
|---|---|---|
| Net Income | 42,948.00 | 8,589.60 |
| Dividends | 23,869.00 | 4,773.80 |
| Dividend Payout Ratio | 55.58% | 87.76% |
| Stock Buybacks | 5,731.00 | 1,146.20 |
| Dividends + Buybacks | 29,600.00 | 5,920.00 |
| Cash Payout Ratio | 68.92% | |
| FCFE (pre-debt) | (3,076.00) | (615.20) |
| FCFE (actual debt) | (1,266.00) | (253.20) |
| FCFE (target debt ratio) | 13,252.43 | 2,650.49 |
| Cash payout as % of target FCFE | **223.36%** | |

Vale paid out more than twice what it could afford. FCFE was negative on both a pre-debt and an actual-debt basis, so the ratio is only meaningful against the target-ratio measure. The framework says cut — but see the constraint discussed in [[managing-dividend-changes]]: Vale has promised preferred stockholders at least 35% of earnings, and failing that threshold hands them voting rights.

*Case 3 — BP, 1982–1991 (cash deficit, poor projects).* $ millions:

| Item | Average | Std Dev | Maximum | Minimum |
|---|---|---|---|---|
| Free CF to Equity | 571.10 | 1,382.29 | 3,764.00 | (612.50) |
| Dividends | 1,496.30 | 448.77 | 2,112.00 | 831.00 |
| Dividends + Repurchases | 1,496.30 | 448.77 | 2,112.00 | 831.00 |
| Dividend Payout Ratio | 84.77% | | | |
| Cash Paid as % of FCFE | **262.00%** | | | |
| ROE − Required return | **−1.67%** | 11.49% | 20.90% | −21.59% |

BP paid 262% of FCFE while earning below its required return — the worst quadrant. The framework's verdict was "cut the dividend", and reality obliged. In 1992 BP cut its dividend by 55%, took a $1.52 billion pretax restructuring charge and laid off 11,500 employees (10% of its workforce), five weeks after chairman Robert Horton resigned under board pressure. Analysts had expected a cut, but the announced cut was at the low end of expectations and the ADRs fell 7.36% to $45.375 on heavy volume. The diagnosis of the underlying cause matched the framework exactly: costly acquisitions and heavy capital expenditure, spending enough to replace 120–130% of annual production and overspending in refining and marketing, on a bet that oil prices would rise.

*Case 4 — The Limited, 1983–1992 (cash deficit, good projects).* $ millions:

| Item | Average | Std Dev | Maximum | Minimum |
|---|---|---|---|---|
| Free CF to Equity | (34.20) | 109.74 | 96.89 | (242.17) |
| Dividends | 40.87 | 32.79 | 101.36 | 5.97 |
| Dividends + Repurchases | 40.87 | 32.79 | 101.36 | 5.97 |
| Dividend Payout Ratio | 18.59% | | | |
| Cash Paid as % of FCFE | **−119.52%** | | | |
| ROE − Required return | **+1.69%** | 19.07% | 29.26% | −19.84% |

Negative average FCFE with positive dividends and good projects. The payout ratio of 18.59% looks conservative and is completely misleading; the firm was paying dividends it could not afford while it had value-creating investments to fund. Prescription: cut or end the payout and let the firm fund its projects.

*Case 5 — Tata Motors (cash deficit).* ₹ millions:

| Item | Aggregate | Average |
|---|---|---|
| Net Income | 421,338.00 | 42,133.80 |
| Dividends | 74,214.00 | 7,421.40 |
| Dividend Payout Ratio | 17.61% | 15.09% |
| Stock Buybacks | 970.00 | 97.00 |
| Dividends + Buybacks | 75,184.00 | 7,518.40 |
| Cash Payout Ratio | 17.84% | |
| FCFE (pre-debt) | (106,871.00) | (10,687.10) |
| FCFE (actual debt) | 825,262.00 | 82,526.20 |
| FCFE (target debt ratio) | 47,796.36 | 4,779.64 |
| Cash payout as % of actual FCFE | 9.11% | |
| Cash payout as % of target FCFE | **157.30%** | |

The three variants tell three different stories. Pre-debt FCFE is negative, largely because of acquisitions. Actual-debt FCFE is hugely positive because the acquisitions were debt-funded, making the payout look trivially affordable at 9.11%. The sustainable measure — target debt ratio — shows a payout at 157.30% of capacity. This is the clearest illustration of why the target-ratio variant is the right default.

**Determinism:**
- DETERMINISTIC: the quadrant placement itself. Given FCFE, cash returned, ROE, cost of equity (and ROC, WACC), a script assigns the quadrant and computes cash paid as a percentage of FCFE.
- JUDGMENT: everything downstream. Whether the historical excess return is repeatable. Whether the investment problem is fixable and over what horizon. How aggressively to push a payout change given clientele and contractual constraints. Which FCFE variant defines the cash axis when the variants disagree — this single choice can move a firm from one column of the matrix to the other.

**Pitfalls:**
- Recommending a dividend cut in the deficit/poor-projects quadrant and stopping there. The dividend is a symptom; the investment policy is the disease. BP cut the dividend *and* restructured.
- Letting a low dividend payout ratio hide a cash deficit. The Limited paid out only 18.59% of earnings and still could not afford it, because FCFE was negative.
- Using actual-debt FCFE to define the cash axis at an acquisitive, debt-funded firm. Tata Motors looks fine at 9.11% and unsustainable at 157.30%.
- Placing a firm once and leaving it there. Disney moved from surplus/poor in 2003 to surplus/good by 2013.
- Ignoring contractual constraints on the recommendation. Vale's preferred-share promise is a hard floor on its dividend.
- Assuming the two axes are independent. A firm with poor projects often generates the surplus precisely because it has stopped investing sensibly.

**Sources:**
- corporate_finance--lecture_slides--cfpacket2spr20 p.201-209
- corporate_finance--lecture_slides--cfpacket2spr20 p.212-213
- corporate_finance--lecture_slides--cfpacket2spr20 p.215
- corporate_finance--lecture_slides--cfpacket2spr20 p.217-219

**Related:** [[cash-trust-assessment]], [[fcfe-potential-dividends]], [[managing-dividend-changes]], [[cash-returned-dividends-and-buybacks]], [[peer-group-payout-analysis]], [[dividend-signaling]], [[dividend-life-cycle]], [[return-on-capital]], [[cost-of-equity]]
