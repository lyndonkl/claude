# Earnings versus cash flows

**Core idea:** People judge a firm's health by the bottom line. But earnings can differ a lot from cash flows, for two reasons. First, accrual accounting books a sale or a cost when it happens, not when cash moves. Second, accounting splits costs into operating, capital and financing classes; operating and financing costs are deducted now, while capital costs are spread over time as depreciation. Three adjustments convert earnings into cash flow. When the two disagree, go with the cash flows. Income statements and cash flow statements can fairly send different messages about a firm's health. But steady, lasting gaps between the two point to accounting problems.

**Formulas:**
- `Cash flow = Earnings + Non-cash expenses − Capital expenditures − Change in non-cash working capital`.
  - Earnings = accounting earnings for the period.
  - Non-cash expenses = expenses deducted in accounting with no cash outlay, such as depreciation and amortization.
  - Capital expenditures = spending on long-lived assets during the period.
  - Change in non-cash working capital = the rise or fall in working capital, excluding cash, during the period.
- Quality-of-earnings ratio: `QoE = Cash Flow from Operations / Net Income`. Track it over five or more years.
- Accrual measure: `Accruals = Net Income − Cash Flow from Operations`. Persistently large positive accruals mean earnings run ahead of cash.

**Reference data:** The two sources of divergence.

| Source | Mechanism | Effect on earnings versus cash |
|---|---|---|
| Accrual timing | Revenue booked at sale, expenses matched to that period, regardless of cash movement | Earnings can lead cash (receivables rising) or lag it (deferred revenue rising) |
| Expense classification | Operating and financing costs deducted now; capital costs spread as depreciation | Earnings understate cash when depreciation is heavy; earnings overstate cash when capex is heavy |

Interpretation grid for the earnings-versus-cash gap:

| Pattern | Likely reading |
|---|---|
| Profit positive, operating cash negative, driven by a reinvestment line inside operations | Growth firm classifying reinvestment as operating (Netflix) |
| Profit negative, operating cash less negative, driven by non-cash add-backs | Young firm with large stock-based compensation and depreciation (Peloton) |
| Profit positive, operating cash consistently larger | Mature firm with depreciation exceeding capex (Coca-Cola) |
| Profit steady, operating cash weak, year after year, with rising receivables | Red flag for accounting problems |

**Procedure:**
1. Build a table of net income and cash flow from operations for at least five years.
2. Compute the QoE ratio and the accruals figure for each year. Plot the trend.
3. Where the two diverge in a single year, find the specific line that explains it: a working-capital swing, a large non-cash charge, or a reinvestment line sitting inside operations.
4. Where they diverge persistently and in the same direction, treat it as a red flag. Steady profits with weak operating cash year after year is the classic warning pattern.
5. Check receivables growth against revenue growth over the same window. Receivables outgrowing revenue is the mechanism behind most persistent gaps.
6. Convert earnings to cash flow explicitly using the three-step formula. Add back non-cash expenses, subtract capex, subtract the change in non-cash working capital.
7. When the converted figure and the reported earnings disagree, use the cash flow. The cash flow statement is the most direct of the three statements, built from actual cash in and out, so accounting game-playing affects it least.

**Worked example:** Netflix, 2019 ($ thousands). Net income was 1,866,916 — a solidly profitable year. Cash flow from operations was (2,887,322) — a burn of nearly three billion dollars. The single line explaining the 4.75 billion gap is additions to streaming content assets of (13,916,683), partly offset by content amortization added back of 9,216,247. Netflix's real capital spending is content, and it runs through the operating section rather than investing. QoE for the year is (2,887,322) / 1,866,916 = (1.55). The gap here is a classification story, not fraud: the firm reinvests enormously and books that reinvestment as operating. It was funded by 4,469,306 of new debt. Whether the pattern can last is the judgment the ratio forces you to make.

**Determinism:**
- DETERMINISTIC: the conversion formula given earnings, non-cash expenses, capex and the working-capital change; the QoE ratio; the accruals figure; the multi-year trend.
- JUDGMENT: deciding whether a gap between earnings and cash flows is a problem or a classification artefact. That needs the accounting-policy footnote, the receivables and deferred-revenue detail, the reinvestment lines, and peer comparison. Judging whether a reinvestment-driven burn can be sustained requires a view on the business and its funding access.

**Pitfalls:**
- Judging health by the bottom line alone. Earnings can misstate the cash a firm truly made in a period.
- Reading a single year's gap as evidence of anything. The signal is in the persistence.
- Assuming a negative operating cash flow means trouble. At Netflix it reflects reinvestment classification; at a young firm it is the norm.
- Trusting earnings over cash when they disagree. The rule runs the other way.
- Forgetting that heavy depreciation makes earnings understate cash, so a capital-intensive mature firm will show QoE well above 1 for entirely benign reasons.

**Sources:**
- foundations_of_finance--cash_flows p.2-3
- accounting__101--cashflow_illustrations p.7
- accounting__101--cashflow_illustrations p.4
- accounting__101--cashflow_illustrations p.3

**Related:** [[accrual-accounting-and-revenue-recognition]], [[expense-classification-and-depreciation]], [[cash-flow-from-operations-and-working-capital]], [[potential-dividends-fcfe]], [[extraordinary-items-and-pro-forma-earnings]], [[income-statement-structure]], [[earnings-quality-red-flags]]
