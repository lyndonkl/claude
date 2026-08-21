# Role of accounting and the three statements

**Core idea:** Accounting has three jobs — check transactions as they occur, record them consistently, and report them in standardized form. It is *not* accounting's job to forecast the future or to value assets and operations; the accountant is a historian, not a prophet. Accounting exists to answer three questions. What do you own — the assets, what was spent on them, and perhaps what they are worth now? What do you owe — every contractual commitment, not just borrowings? And how much money did you make, measured both on accounting judgment and on cash in versus cash out? Those three questions map one-to-one onto the three financial statements. Because the raw material for almost all financial analysis and valuation arrives as accounting statements, an analyst must understand how accountants think even when disagreeing with them — and must track how that thinking changes over time.

**Formulas:**
- Balance sheet identity: `Assets = Liabilities + Shareholders' Equity`. Assets = resources the firm has invested in; Liabilities = contractual claims on the firm; Equity = residual book claim of owners.
- Income statement cascade: `Net Income = Revenues − Operating Expenses − Financial Expenses − Taxes` (see [[income-statement-structure]] for the full ladder).
- Cash flow identity: `Net Change in Cash Balance = CF from Operations + CF from Investing + CF from Financing`.
- Retained-earnings link: `Ending Retained Earnings = Beginning Retained Earnings + Net Income − Dividends − (buyback charges to retained earnings)`.

**Reference data:** The three statements and what each answers.

| Statement | Accounting question | Time dimension | What it delivers |
|---|---|---|---|
| Balance sheet | What do you own? What do you owe? | Snapshot at a point in time | Assets owned, money owed, and an accounting estimate of what equity is worth |
| Income statement | How much money did you make (accrual)? | Covers a period | Revenues, expenses, and profit at several levels |
| Statement of cash flows | How much money did you make (cash)? | Covers a period | Cash inflows and outflows; cash earnings as opposed to accounting earnings |

The four interconnections that stitch them together:

| Link | From | To | Mechanism |
|---|---|---|---|
| 1 | Income statement | Balance sheet | Depreciation on fixed assets is an expense that also reduces recorded fixed-asset values |
| 2 | Income statement | Balance sheet | Net income (or loss) flows into equity through retained earnings |
| 3 | Income statement | Cash flow statement | Net income is the starting line of cash flow from operations |
| 4 | Cash flow statement | Balance sheet | Operating, investing and financing flows change balance-sheet accounts, including the cash balance |

**Procedure:**
1. Pull all three statements for the same fiscal period, plus the prior period's balance sheet (you need two balance sheets to compute any change).
2. Check the balance sheet balances: Assets = Liabilities + Equity. If it does not, you have mis-transcribed or missed a mezzanine/noncontrolling line.
3. Tie net income on the income statement to the first line of the operating section of the cash flow statement. They must match (for IFRS filers the cash flow statement may start at profit *before* tax instead — then tie to that line and confirm the tax-paid adjustment).
4. Tie the retained-earnings roll-forward: prior retained earnings + net income − dividends should reconcile to current retained earnings; any residual is a buyback, write-off or reclassification to investigate.
5. Tie depreciation and amortization: the D&A add-back in the cash flow statement should match the D&A expensed in the income statement (or in the notes when it is buried inside COGS/SG&A).
6. Tie the cash balance: beginning cash + net change in cash (three sections plus FX effect) = ending cash on the balance sheet.
7. Only after these six ties hold should you start interpreting. Never read one statement alone: a firm can look profitable on the income statement and be burning cash on the cash flow statement (see [[earnings-versus-cash-flows]]).
8. Treat every accounting number as a record of the past. Do not import it into a valuation as though it were an estimate of value; convert it deliberately (see [[financial-balance-sheet]]).

**Worked example:** Netflix, fiscal 2019 (10-K, $ thousands). Income statement net income = 1,866,916. The cash flow statement's operating section begins at exactly that 1,866,916 (link 3). Retained earnings move from 2,942,359 (2018) to 4,811,749 (2019). That difference of 1,869,390 is net income 1,866,916 plus 2,474 of other adjustments; Netflix paid no dividends (link 2). The three cash flow sections were operating (2,887,322), investing (387,064) and financing +4,505,662. They net to a cash increase of 1,231,745. That carries cash and equivalents from 3,794,483 to 5,018,437 on the balance sheet (link 4). Total assets 33,975,712 = total liabilities 26,393,555 + stockholders' equity 7,582,157.

**Determinism:**
- DETERMINISTIC: all six ties in the procedure. Inputs = the three statements plus prior-period balance sheet; outputs = pass/fail on each reconciliation plus the residuals. A script can compute the balance check, the net-income tie, the retained-earnings residual, the D&A tie and the cash tie.
- JUDGMENT: interpreting what the reconciliations mean, deciding whether a retained-earnings residual is benign, and deciding how far the accounting numbers can be trusted as inputs to valuation. This needs the filing's footnotes and knowledge of the firm's business.

**Pitfalls:**
- Treating accounting statements as forecasts or as valuations. They are historical records; accountants are explicitly not in the forecasting or valuation business.
- Reading one statement in isolation. Depreciation, net income and cash all cross between statements; a conclusion drawn from one is frequently reversed by another.
- Assuming "what do you owe" equals "borrowings." It includes all contractual commitments, of which debt is only one form.
- Assuming accounting rules are stable. They change; an analyst has to track both what changed and why, or year-over-year comparisons silently break.

**Sources:**
- accounting__101--financial_statements_overview p.2-4
- accounting__101--financial_statements_overview p.8
- accounting__101--financial_statements_overview p.11

**Related:** [[income-statement-structure]], [[balance-sheet-views-and-asset-measurement]], [[cash-flow-statement-structure]], [[accounting-standards-gaap-ifrs]], [[earnings-versus-cash-flows]], [[financial-balance-sheet]], [[accounting-earnings-adjustments]]
