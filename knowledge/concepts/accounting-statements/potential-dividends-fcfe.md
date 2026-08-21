# Potential dividends: free cash flow to equity from the statement

**Core idea:** Free cash flow to equity is the potential dividend — the cash a firm *could* pay out to its equity investors, whether or not it does. The statement of cash flows already contains every item needed to build it, because the statement views cash flows through the eyes of equity investors. Three steps get there. Start at net income, add back non-cash charges and adjust for working capital to reach cash flow from operations. Subtract capital expenditures and cash acquisitions and add divestitures to reach FCFE before debt. Add debt raised and subtract debt repaid to reach FCFE after debt. The same statement also shows what equity investors actually received, as dividends and buybacks. The gap between potential and actual is the analyst's real subject.

**Formulas:**
- `Cash Flow from Operations = Net Income + Depreciation and Amortization + Other non-cash Expenses ± Changes in (Accounts Receivable, Inventory, Other Current Assets, Accounts Payable, Taxes Due)`.
- `FCFE before debt = Cash Flow from Operations − Capital Expenditures + Divestitures of assets − Cash Acquisitions`.
- `FCFE after debt = FCFE before debt + Debt Raised − Debt Repaid`.
- Residual-claim form: `Residual cash flow to equity = Cash from operations − Taxes − Capital investments − Debt payments`. The result may be negative when contractual claims exceed the cash operations generate.
- Cash flow to the firm (pre-debt), from the same statement: `CF to Firm ≈ FCFE after debt + Interest Expense × (1 − tax rate) − Net Debt Issued`. Interest was already netted out on the way to net income, so you must trace it and add it back.
- `Actual cash returned = Dividends Paid + Stock Buybacks`. `Payout gap = FCFE after debt − Actual cash returned`.

**Reference data:** The build-up ladder.

| Cash flow effect | Item |
|---|---|
| Start with | Net Income |
| Plus | Depreciation and Amortization |
| Plus | Other non-cash Expenses |
| Plus or Minus | Change in Accounts Receivable |
| Plus or Minus | Change in Inventory |
| Plus or Minus | Change in Other Current Assets |
| Plus or Minus | Change in Accounts Payable |
| Plus or Minus | Change in Taxes Due |
| Equals | **Cash flow from Operations** |
| Minus | Capital Expenditures |
| Plus | Divestitures of assets |
| Minus | Cash Acquisitions |
| Equals | **FCFE before debt** |
| Plus | Debt Raised |
| Minus | Debt Repaid |
| Equals | **FCFE after Debt** |

Which measure to use:

| Measure you want | Where to start | Adjustment needed |
|---|---|---|
| Cash flow to equity | The statement of cash flows, directly | None — the statement is already on the equity perspective |
| Cash actually received by equity | Financing section | Read off dividends and buybacks |
| Cash flow to the firm, prior to debt payments | The statement of cash flows | Find interest expense and add it back; remove net debt flows |

**Procedure:**
1. Take cash flow from operations from the statement, or rebuild it line by line if the filer's classification is unusual.
2. Move any reinvestment the filer buried in the operating section down into the investing step. Content spending and capitalized development costs are the common cases.
3. Subtract capital expenditures and cash acquisitions, add operating divestitures. That gives FCFE before debt.
4. Add debt raised and subtract debt repaid to get FCFE after debt.
5. Read dividends and buybacks off the financing section. Compare with FCFE after debt.
6. Interpret the gap. FCFE well above actual payout means the firm is accumulating cash. FCFE below actual payout means the firm is funding its payout from the cash balance or from borrowing.
7. If you need cash flow to the firm instead, find interest expense — it will be in the income statement, not the cash flow statement — and add it back after tax. Then strip out the debt raised and repaid lines.
8. Never assume the reported dividend is the firm's capacity to pay. The whole point of FCFE is to measure capacity, not practice.

**Worked example:** Coca-Cola, 2019 ($ millions). Cash flow from operations 10,471. Subtract PP&E purchases (2,054) and acquisitions of businesses, equity method investments and nonmarketable securities (5,542), giving FCFE before debt of 2,875. Debt issuances 23,009 less debt payments (24,850) give net debt of (1,841), so FCFE after debt is 1,034. Actual cash returned was dividends 6,845 plus buybacks 1,103 = 7,948. The payout gap is 1,034 − 7,948 = (6,914). Coca-Cola returned far more than it generated after acquisitions, drawing down cash: the balance fell from 9,077 to 6,480 over the year. That is precisely the kind of finding the potential-dividend calculation exists to surface, and it is invisible in the dividend payout ratio alone.

**Determinism:**
- DETERMINISTIC: the entire ladder. Inputs = the cash flow statement line items. Outputs = cash flow from operations, FCFE before debt, FCFE after debt, actual cash returned, and the payout gap. The interest add-back is deterministic once interest expense is located.
- JUDGMENT: choosing which cash flow measure the analysis needs; deciding which operating-section items are really reinvestment; tracing interest expense through a filing that nets or omits it; deciding whether a payout gap is sustainable. This needs the income statement, the debt footnote and multi-year history.

**Pitfalls:**
- Using the statement's operating cash flow as FCFE. It is only the first of three steps.
- Forgetting that interest expense was already deducted. Any firm-level (pre-debt) cash flow requires an explicit add-back.
- Ignoring reinvestment classified as operating, which inflates FCFE at firms like Netflix.
- Confusing FCFE with dividends paid. FCFE is potential; dividends are what managers chose.
- Omitting cash acquisitions from reinvestment. At acquisitive firms they exceed capex several times over.
- Treating a negative FCFE as an error. It is normal for young and high-growth firms and is exactly what the financing section funds.

**Sources:**
- accounting__101--cashflow p.11
- accounting__101--cashflow_illustrations p.11
- foundations_of_finance--cash_flows p.6
- accounting__101--cashflow_illustrations p.5

**Related:** [[cash-flow-from-operations-and-working-capital]], [[investing-cash-flows-and-reinvestment]], [[financing-cash-flows-and-cash-returned]], [[cash-flow-statement-structure]], [[cash-flow-claim-types]], [[earnings-versus-cash-flows]], [[free-cash-flow-to-firm]], [[dividend-policy]]
