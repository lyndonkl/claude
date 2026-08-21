# Cash flow from operations and the working capital effect

**Core idea:** Cash flow from operations starts at net income and works backward out of accrual accounting. Non-cash charges are added back, because they reduced income without using cash. Then changes in non-cash working capital are added or subtracted, because accrual revenue and expense are not the same as cash collected and paid. The working capital effect runs in one direction: when non-cash working capital rises, cash flow falls, and when it falls, cash flow rises. Non-cash working capital ties up cash and capital. So a firm with higher working-capital needs has lower operating cash flow, at any given net income, than a firm with lower needs.

**Formulas:**
- `Cash Flow from Operations = Net Income + Depreciation and Amortization + Other non-cash Expenses ± Change in Accounts Receivable ± Change in Inventory ± Change in Other Current Assets ± Change in Accounts Payable ± Change in Taxes Due`. The five change items together are the change in non-cash working capital.
- `Non-cash Working Capital = Non-cash current assets − Non-debt current liabilities`.
- `Effect on CFO = − Change in Non-cash Working Capital`. An increase in non-cash working capital is a cash use.
- Simplified period cash flow: `Cash flow = Earnings + Non-cash expenses − Capital expenditures − Change in non-cash working capital`.

Symbols: Net Income = accrual equity earnings for the period. D&A = depreciation and amortization charged in the period. Other non-cash expenses = charges deducted in accounting with no cash outlay, notably stock-based compensation, deferred taxes and impairments. Non-cash current assets = current assets excluding cash and near-cash securities. Non-debt current liabilities = current liabilities excluding interest-bearing short-term borrowings.

**Reference data:** The operating-section build-up.

| Cash flow effect | Item | Why |
|---|---|---|
| Start with | Net Income | Equity income |
| Plus | Depreciation and Amortization | Add back non-cash items |
| Plus | Other non-cash Expenses | Add back non-cash items |
| Plus or Minus | Change in Accounts Receivable | Get to cash to equity from operations |
| Plus or Minus | Change in Inventory | Get to cash to equity from operations |
| Plus or Minus | Change in Other Current Assets | Get to cash to equity from operations |
| Plus or Minus | Change in Accounts Payable | Get to cash to equity from operations |
| Plus or Minus | Change in Taxes Due | Get to cash to equity from operations |
| Equals | **Cash flow from Operations** | |

Sign rules for working capital changes:

| Change | Cash effect |
|---|---|
| Receivables up | Cash down |
| Inventory up | Cash down |
| Other current assets up | Cash down |
| Accounts payable up | Cash up |
| Taxes due up | Cash up |
| Non-cash working capital up overall | Cash flow down |
| Non-cash working capital down overall | Cash flow up |

Common non-cash add-backs seen in practice:

| Add-back | Example (year, firm) |
|---|---|
| Depreciation and amortization | Coca-Cola 1,365 ($M, 2019); Dr. Reddy's 7,892 (₹M, FY2020) |
| Stock-based compensation | Peloton 89.5 ($M, FY2019) vs Coca-Cola 201 ($M, 2019) |
| Deferred income taxes | Toyota +192,147 (¥M, FY2020) after (86,594) in FY2019 |
| Depreciation, depletion, amortization and impairment | Total 16,401 ($M, 2019) |
| Content amortization | Netflix 9,216,247 ($ thousands, 2019) |

**Procedure:**
1. Copy the operating section verbatim. Separate the non-cash add-backs from the working-capital change lines.
2. Compute non-cash working capital at both period ends. Take current assets, remove cash and near-cash securities. Take current liabilities, remove all interest-bearing short-term borrowing. Subtract.
3. Verify that the change in non-cash working capital you computed matches the sum of the working-capital lines in the statement, in sign and roughly in size. Acquisitions and FX cause legitimate gaps.
4. Check the size of each non-cash add-back relative to net income. A stock-based compensation add-back that is a large fraction of the loss, as at Peloton, means reported cash burn understates the economic cost of running the firm.
5. Compute operating cash flow per unit of net income. A ratio persistently below 1 for a profitable firm is a red flag.
6. If working capital is systematically negative, note it. Firms whose suppliers and customers fund the operating cycle generate cash as they grow.
7. Do not use the section total alone in valuation. You need the individual lines to build [[potential-dividends-fcfe]].

**Worked example:** Peloton, fiscal 2019 ($ millions). Net loss (195.6) + D&A 21.7 + stock-based compensation 89.5, then working-capital changes including inventories (111.3) and accounts payable +117.3, give operating cash flow of (108.6). Two lessons sit in that arithmetic. First, the non-cash add-back of 89.5 is nearly half the size of the net loss, so cash burn looks far smaller than the accounting loss. Second, inventory alone consumed 111.3 million of cash while the business grew revenue from 435.0 to 915.0 million — the working capital effect in its rawest form, partly offset by supplier credit of 117.3. Compare Coca-Cola in 2019: net income 8,985 + D&A 1,365 + other adjustments → operating cash 10,471, a ratio of 1.17 to net income and a mark of mature-stable cash generation.

**Determinism:**
- DETERMINISTIC: the whole build-up. Inputs = net income, non-cash charges, and the five working-capital change lines. Output = cash flow from operations. Also deterministic: non-cash working capital from classified balance-sheet lines, and the change between two balance sheets.
- JUDGMENT: deciding which balance-sheet lines count as non-cash current assets and non-debt current liabilities; deciding whether an add-back is genuinely non-cash in economic substance (stock-based compensation is non-cash but not costless); deciding whether an earnings-to-cash gap is normal or a warning. This needs the balance sheet detail and multi-year history.

**Pitfalls:**
- Leaving interest-bearing short-term debt inside current liabilities when computing non-cash working capital.
- Treating stock-based compensation as a free add-back. It dilutes existing owners even though no cash leaves.
- Ignoring the working capital drag when forecasting a growing firm. Growth in revenue drags working capital with it, and that consumes cash every year.
- Assuming the statement's working-capital lines equal the balance-sheet change. Acquisitions, divestitures and currency translation break the tie.
- Forgetting that interest expense is already deducted before this line, so operating cash flow is a post-interest, equity-perspective number.

**Sources:**
- accounting__101--cashflow p.4-5
- foundations_of_finance--cash_flows p.3
- accounting__101--cashflow_illustrations p.3
- accounting__101--cashflow_illustrations p.5
- accounting__101--cashflow_illustrations p.6
- accounting__101--cashflow_illustrations p.10

**Related:** [[cash-flow-statement-structure]], [[potential-dividends-fcfe]], [[liabilities-debt-and-leases]], [[earnings-versus-cash-flows]], [[expense-classification-and-depreciation]], [[accrual-accounting-and-revenue-recognition]], [[working-capital-forecasting]]
