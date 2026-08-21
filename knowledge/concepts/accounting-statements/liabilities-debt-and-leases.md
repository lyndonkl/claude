# Current liabilities, debt and leases

**Core idea:** The liability side mixes two very different things. Some liabilities are ordinary operating claims that arise from running the business — supplier credit, accrued salaries, taxes due. Others are borrowings that carry interest and a default consequence. Only the second kind is debt for finance purposes. The rule that follows is simple and it is the single most common cleanup an analyst performs: interest-bearing short-term borrowing must be pulled out of current liabilities and moved into the debt column before you compute non-cash working capital. Since 2019, operating lease commitments count as debt too, alongside bonds, bank loans and capital leases.

**Formulas:**
- `Non-cash Working Capital = Non-cash current assets − Non-debt current liabilities`. Non-debt current liabilities exclude commercial paper, short-term debt and the current portion of long-term debt.
- `Total Debt = Long-term debt + Short-term interest-bearing borrowings + Current portion of long-term debt + Lease debt`.
- `Lease debt ≈ present value of contracted lease payments`, discounted at the firm's pre-tax cost of debt.
- `Implicit lease interest ≈ Lease debt × Current interest rate` (feeds financial expenses).
- Weighted average interest rate: `Σ (instrument amount × instrument rate) / Σ instrument amounts`.
- Refinancing pressure: `Debt due in next N years / Total debt`, read off the maturity schedule in the footnotes.

**Reference data:** The three groups of current liability.

| Group | Contents | Treatment in non-cash working capital |
|---|---|---|
| 1. Non-interest-bearing operating | Accounts payable, supplier credit | Include — part of normal operations |
| 2. Interest-bearing short-term borrowing | Commercial paper, short-term debt, current portion of long-term debt | Exclude — reclassify into the debt column |
| 3. Deferred and accrued | Deferred salaries, taxes, other short-term amounts due | Include |

The three forms of borrowing.

| Form | Source | Notes |
|---|---|---|
| Corporate bonds | Public markets | Mostly not marked to market on the balance sheet |
| Bank loans | Banks and other lenders | Mostly recorded at the amount first borrowed |
| Lease debt | Lease contracts requiring future payments | Until 2019 only capital leases counted; since 2019 operating lease commitments count too |

Coca-Cola debt composition, 31 December 2019 ($ millions):

| Instrument | 2019 amount | 2019 avg rate | 2018 amount | 2018 avg rate |
|---|---|---|---|---|
| U.S. dollar notes due 2020–2093 | 14,621 | 2.4% | 13,619 | 2.6% |
| U.S. dollar debentures due 2022–2098 | 1,366 | 4.9% | 1,390 | 5.2% |
| U.S. dollar zero coupon notes due 2020 | 168 | 8.4% | 163 | 8.4% |
| Australian dollar notes due 2020–2024 | 677 | 2.4% | 723 | 2.2% |
| Euro notes due 2021–2036 | 12,807 | 0.5% | 12,994 | 0.6% |
| Swiss franc notes due 2022–2028 | 1,129 | 3.7% | 1,128 | 3.6% |
| Other, due through 2098 | 548 | 6.2% | 300 | 4.0% |
| Fair value adjustments | 453 | N/A | 62 | N/A |
| **Total** | **31,769** | **1.9%** | **30,379** | **1.9%** |
| Less: current portion | 4,253 | | 5,003 | |
| Long-term debt | 27,516 | | 25,376 | |

Coca-Cola long-term debt maturities after 31 December 2019 ($ millions):

| Year | 2020 | 2021 | 2022 | 2023 | 2024 |
|---|---|---|---|---|---|
| Maturities | 4,253 | 3,767 | 3,788 | 4,097 | 1,974 |

**Procedure:**
1. Take the current-liabilities block and sort every line into the three groups above.
2. Move every group-2 item into the debt column. Add it to long-term debt to get total interest-bearing debt.
3. Compute non-cash working capital from what remains: non-cash current assets minus groups 1 and 3.
4. Go to the debt footnote. Extract each issue with its stated rate, its maturity, and its features — floating versus fixed, straight versus convertible.
5. Compute the weighted average interest rate across instruments. Compare it with current market rates to gauge how far book debt sits from market value.
6. Extract the five-year maturity schedule. Compute debt due in the next one, two and three years as a share of total debt. That is the refinancing-risk measure and the raw material for debt duration.
7. Add lease debt. Present-value the contracted lease payments at the pre-tax cost of debt and add the result to total debt.
8. Note the currencies. A firm borrowing in several currencies has debt whose value moves with exchange rates, and the reported total is a translation.

**Worked example:** Coca-Cola, 2019 ($ millions). Balance-sheet current liabilities total 26,973. Of that, loans and notes payable 10,994 and current maturities of long-term debt 4,253 are interest-bearing — group 2 — totalling 15,247. Move them to debt. What remains as operating current liabilities is accounts payable and accrued expenses 11,312 plus accrued income taxes 414 = 11,726. Non-cash current assets are total current assets 20,411 minus cash 6,480, short-term investments 1,467 and marketable securities 3,228 = 9,236. Non-cash working capital = 9,236 − 11,726 = (2,490), i.e. negative. Coca-Cola's suppliers fund its operating cycle. Total debt from the footnote is 31,769 at a blended rate of 1.9%, with 4,253 due in 2020 — 13.4% of the total, a modest refinancing load.

**Determinism:**
- DETERMINISTIC: the sorting rule once each line is labelled; the non-cash working capital arithmetic; the total-debt sum; the weighted average rate; the maturity-share ratios; the lease present value once the discount rate and payment schedule are fixed.
- JUDGMENT: deciding whether an ambiguous liability bears interest; choosing the discount rate for lease debt; estimating lease payments beyond the disclosed horizon; judging whether book debt is a fair proxy for market value of debt. These need the debt footnote, the lease footnote and current market yields.

**Pitfalls:**
- Leaving interest-bearing short-term debt inside current liabilities when computing working capital. This double-counts the borrowing and understates working capital needs.
- Using only the "long-term debt" line as total debt. The current portion and short-term borrowings are debt too.
- Ignoring lease commitments. Since 2019 operating leases are debt; before that they hid off balance sheet.
- Assuming book debt equals market debt. The mark-to-market push on the asset side has been muted on the liability side.
- Skipping the maturity schedule. A firm with a low average rate and a wall of near-term maturities is riskier than its blended rate suggests.

**Sources:**
- accounting__101--balance_sheet p.9-11
- accounting__101--balance_sheet_illustrations p.6
- accounting__101--balance_sheet_illustrations p.9

**Related:** [[balance-sheet-views-and-asset-measurement]], [[non-operating-items-and-cross-holdings]], [[cash-flow-from-operations-and-working-capital]], [[financing-cash-flows-and-cash-returned]], [[capitalizing-rd-and-leases]], [[cost-of-debt]], [[cash-flow-claim-types]]
