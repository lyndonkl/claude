# Non-operating items, financial expenses and cross-holdings

**Core idea:** Below the operating-income line sit items that do not belong to the core business. Financial expenses are the cost of non-equity capital, mainly interest on debt, plus implicit interest imputed on lease commitments. Non-operating income comes from cash parked in marketable securities and from stakes in other firms. How a cross-holding is reported depends entirely on the size of the stake. A majority stake forces consolidation, which pulls 100% of the subsidiary into the parent's revenues and operating income even though the parent does not own all of it. A minority stake shows up as a single income line and a single asset. Getting this boundary right decides whether your operating income measures the business you are valuing or something else.

**Formulas:**
- `Net Interest Expense = Interest Expense − Interest Income`. A negative result is net interest income.
- `Implicit interest ≈ Debt-equivalent value of the commitment × Current interest rate`. Used for leases and similar commitments treated as debt.
- Consolidation: `Parent Revenues = Parent's own revenues + 100% of subsidiary revenues (intercompany eliminated)`. The outside share appears as `Noncontrolling (minority) interest` on the liability side of the balance sheet and as a deduction from consolidated net income.
- Equity method: `Equity income = Ownership % × Subsidiary net income`, reported below operating income; the balance-sheet asset rolls forward as `Investment = Prior investment + Equity income − Dividends received`.

**Reference data:** Treatment of a stake in another company.

| Stake / intent | Income statement | Balance sheet |
|---|---|---|
| Majority (>50%) | Consolidate: 100% of subsidiary revenues, operating expenses and operating income; deduct NCI share of net income | Subsidiary assets fully consolidated; outside share shown as minority (noncontrolling) interest on the liability side |
| Minority (<50%), long-term investment | Equity income (or dividend income) as a separate line below operating income | The stake shown as an asset at book value |
| Minority (<50%), held for trading | Gains/losses flow through income | Marked to market |
| Publicly traded securities | Investment income line, or netted against interest expense | Almost always marked to current market prices |
| Liquid, near-riskless securities | Interest income | Classified as cash & marketable securities, not as an investing asset |

Financial expense components:

| Item | Source | Note |
|---|---|---|
| Interest on bank loans | Bank borrowing | Explicit |
| Coupon on corporate bonds | Public markets | Explicit |
| Lease interest | Lease contracts treated as debt | Implicit; computed from the debt value of the commitment and current rates |
| Interest income offset | Cash and marketable securities | Some firms net it against interest expense and report a single net line |

**Procedure:**
1. Draw the operating-income line yourself. Everything that is not an operating expense of the core business this period goes below it.
2. Find the interest lines. If the filer reports a single net interest figure, dig into the footnote for gross interest expense and gross interest income. You need gross interest expense to compute cash flow to the firm and to compute interest coverage.
3. Add implicit interest on lease commitments. Since 2019, operating lease commitments count as debt, so the imputed interest is a financial expense.
4. Inventory every cross-holding. For each, record the ownership percentage, whether it is consolidated, and the reported income line.
5. If a majority-owned subsidiary is consolidated, check that you subtract the noncontrolling-interest share of net income before computing per-share numbers.
6. If minority stakes are material, decide whether to value them separately. Their payoff shows up below operating income, so operating-income-based valuation misses them entirely. Add their value back as a non-operating asset.
7. Watch for stock-funded acquisitions. No cash changes hands, so they never appear in the cash flow statement, yet the subsidiary shows up in the consolidated income statement from the deal date.

**Worked example:** Coca-Cola, 2019 ($ millions). Interest income was 563 and interest expense 946, so net interest expense is 946 − 563 = 383. Equity income (loss) — net was 1,049, income from minority stakes in bottlers accounted for under the equity method. That 1,049 sits below operating income of 10,086, and the matching asset is "equity method investments" of 19,025 on the balance sheet. The segment note shows that 836 of the 1,049 came from Bottling Investments alone. Coca-Cola also consolidates subsidiaries it does not wholly own: consolidated net income was 8,985, of which 65 went to noncontrolling interests, leaving 8,920 for Coca-Cola shareowners. Toyota shows the same pattern under a different label: equity in earnings of affiliated companies of ¥271,152 million in FY2020, against an "affiliated companies" investment balance of ¥4,123,453 million.

**Determinism:**
- DETERMINISTIC: the netting of interest; the equity-income calculation given ownership percentage and subsidiary income; the NCI deduction; the mapping from stake size to accounting treatment.
- JUDGMENT: estimating the debt-equivalent value of lease and similar commitments; classifying a minority stake as held-for-trading versus long-term; deciding which assets are operating and which are non-operating; deciding whether to value cross-holdings separately. This needs the investments footnote, the lease footnote, and the segment disclosure.

**Pitfalls:**
- Accepting a consolidated operating income as the parent's own. Consolidation counts 100% of a subsidiary the parent may own only 60% of.
- Using consolidated net income for EPS or equity value without removing noncontrolling interests.
- Using a net interest line where gross interest expense is needed. The netting hides the true cost of debt.
- Double-counting cross-holdings: adding the value of a minority stake as a non-operating asset while also leaving its equity income in your operating earnings.
- Forgetting that stock-funded deals leave no trace in the cash flow statement.
- Treating liquid near-riskless securities as investing outflows. They belong with cash.

**Sources:**
- accounting__101--income_statements p.10-11
- accounting__101--balance_sheet p.5
- accounting__101--cashflow p.7
- accounting__101--income_statements_illustrations p.5
- accounting__101--income_statements_illustrations p.7

**Related:** [[income-statement-structure]], [[liabilities-debt-and-leases]], [[balance-sheet-views-and-asset-measurement]], [[investing-cash-flows-and-reinvestment]], [[intangibles-and-goodwill]], [[sector-differences-in-financial-statements]]
