# Cash flow statement structure

**Core idea:** On the surface the statement of cash flows explains how much the cash balance changed during a period, and why. It does three more things underneath. It shows the company's cash earnings, in contrast to the accrual earnings of the income statement. It shows how much cash the company reinvested and where. It shows how much cash the company raised from, or returned to, its debt and equity investors. The statement keeps signs intact — outflows are minuses, inflows are pluses — and it views everything through the eyes of the equity investors in the company. It is also the most direct of the three statements. It is built from actual cash in and cash out, so accounting game-playing affects it least.

**Formulas:**
- `Net Change in Cash Balance = CF from Operations + CF from Investing + CF from Financing`. Each term is that section's net cash flow, with its sign preserved.
- With currency translation: `Ending Cash = Beginning Cash + CFO + CFI + CFF + Effect of exchange rate changes on cash`.
- `CFO` = net cash flow from operations, after taxes and interest expenses.
- `CFI` = net of buying and selling real assets (capital expenditures), buying and selling financial assets, and cash spent buying other firms.
- `CFF` = net cash flow from issuing and buying back equity and from issuing and repaying debt, after dividend payments.

**Reference data:** The three sections and what belongs in each.

| Section | Contents | Sign convention |
|---|---|---|
| Cash Flows From Operations | Net cash flow from operations, after taxes and after interest expenses | Positive when the business generates cash |
| Cash Flows From Investing | Divestiture and acquisition of real assets (capex); disposal and purchase of financial assets; cash spent to acquire other firms | Purchases negative, disposals positive |
| Cash Flows From Financing | Issuing and buying back equity; issuing and repaying debt; dividends paid | Raises positive, repayments and payouts negative |

Where common items sit — the placements that catch people out:

| Item | Section | Why |
|---|---|---|
| Interest expense | Operations | It has already reduced net income; it also shows in deferred taxes |
| Debt raised or repaid | Financing | Principal flows, not operating costs |
| Dividends and buybacks | Financing | Cash returned to equity |
| Capital expenditures | Investing | Purchase of operating assets |
| Cash acquisitions of other firms | Investing | External operating investment |
| Purchases of marketable securities | Investing, unless liquid and near-riskless | Near-riskless liquid securities count as cash, not investing |
| Stock-funded acquisitions | Nowhere | No cash changes hands |
| Netflix content spending | Operations | The filer classifies content additions as operating, not investing |

**Procedure:**
1. Pull the statement and record the three section totals plus any FX-effect line.
2. Check that the three totals plus FX equal the change in the cash balance, and that beginning plus change equals ending cash on the balance sheet.
3. Confirm the starting line. US filers start at net income. Many IFRS filers start at profit before tax and deduct taxes paid further down.
4. Read the sign pattern of the three sections as a triple. That triple, more than any single number, tells you what kind of firm you are looking at (see [[life-cycle-patterns-in-financial-statements]]).
5. Scan for items the filer has placed unusually. Content spending inside operations, finance-receivable originations inside investing, and near-cash securities inside investing all distort the standard reading.
6. Do not stop at the section totals. Every input you need for cash-flow valuation is inside the line items, not the subtotals.
7. Compare the operating section with the income statement. A persistent gap is a signal, not noise (see [[earnings-versus-cash-flows]]).

**Worked example:** Peloton, fiscal 2019 ($ millions, year ended 30 June). Operating (108.6) + investing (297.5) + financing +417.2 = +11.1, and with the small FX and restricted-cash effects the reported net change in cash was +11.3, carrying ending cash, equivalents and restricted cash to 163.0. The triple reads negative-negative-positive: the business burns cash, spends heavily, and pays for both by selling shares. Compare Coca-Cola in 2019 ($ millions): operating +10,471, investing (3,976), financing (9,004), ending cash 6,480. That triple reads positive-negative-negative: the business makes cash, reinvests modestly, and hands the rest back.

**Determinism:**
- DETERMINISTIC: the addition of the three sections plus FX; the tie to the balance sheet cash line; the extraction of every line item. Inputs = the statement. Outputs = section totals, net change, ending cash.
- JUDGMENT: reading what the sign pattern means; deciding whether the filer's placement of an item is economically right; deciding which lines constitute real reinvestment. This needs the accounting-policy footnote and knowledge of the business model.

**Pitfalls:**
- Assuming the section labels mean the same thing at every firm. Netflix's real capital spending runs through operations, and Toyota's finance-arm originations run through investing.
- Forgetting that interest expense is already inside the operating section. Any pre-debt cash flow measure must add it back.
- Ignoring the FX-effect line and then failing to tie the cash balance.
- Treating a negative investing figure as bad. Heavy investing is normal and healthy for a young firm.
- Missing stock-funded acquisitions, which never appear here at all.

**Sources:**
- accounting__101--financial_statements_overview p.7
- accounting__101--cashflow p.2-3
- accounting__101--cashflow_illustrations p.7
- accounting__101--cashflow_illustrations p.3

**Related:** [[cash-flow-from-operations-and-working-capital]], [[investing-cash-flows-and-reinvestment]], [[financing-cash-flows-and-cash-returned]], [[potential-dividends-fcfe]], [[earnings-versus-cash-flows]], [[role-of-accounting-and-three-statements]], [[life-cycle-patterns-in-financial-statements]]
