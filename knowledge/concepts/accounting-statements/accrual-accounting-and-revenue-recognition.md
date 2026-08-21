# Accrual accounting and revenue recognition

**Core idea:** Accrual accounting books a transaction when it occurs, not when cash moves. Revenue is recorded when the product or service is sold, not when the customer pays. Expenses are matched to the period of the sale they support, even if the cash was spent earlier or will be paid later. Cash accounting does the opposite: it books revenue on receipt and expense on payment. Only small or personal businesses may use cash accounting. This timing choice is the first of two reasons earnings differ from cash flows, and it is why revenue recognition rules matter so much for firms that sell over many years.

**Formulas:**
- Accrual revenue for a period under ASC 606: `Revenue recognized = Σ (transaction price allocated to each performance obligation × fraction of that obligation satisfied in the period)`. Transaction price = the consideration the entity expects to be entitled to. Performance obligation = a distinct promised good or service in the contract.
- Percentage-of-completion proxy for long projects: `Revenue in year t = Total contract price × (Costs incurred through t / Total expected costs) − Revenue recognized before t`.
- Timing difference: `Revenue recognized − Cash collected = Change in Accounts Receivable − Change in Deferred Revenue`. Deferred revenue rises when customers pay in advance.

**Reference data:**

| Basis | Revenue booked when | Expense booked when | Who may use it |
|---|---|---|---|
| Accrual | Product or service is sold | In the period of the sale it supports | Required for any business that is not small or personal |
| Cash | Payment is received | Payment is made | Small or personal businesses only |

ASC 606 core principle, verbatim: recognize revenue to "depict the transfer of promised goods or services to customers in an amount that reflects the consideration to which the entity expects to be entitled in exchange for those goods or services."

Application patterns named in the source:

| Business | Recognition pattern |
|---|---|
| Ordinary product sale | Book the whole amount at the point of sale |
| Real estate developer, multi-year build | Book revenue as construction progresses |
| Software firm, multi-year contract | Book revenue as performance obligations are met |
| Subscription business | Book ratably over the subscription period; cash received up front sits in deferred revenue |

**Procedure:**
1. Read the revenue-recognition policy footnote. Identify the performance obligations the firm has defined.
2. Classify the firm's contracts. Point-of-sale contracts need no work. Multi-period contracts do.
3. For each multi-period contract type, find the measure of progress the firm uses — costs incurred, units delivered, time elapsed, milestones.
4. Compute the revenue attributable to the period from that measure of progress. Where the firm discloses only totals, use the change in deferred revenue and receivables to sanity-check the timing.
5. Compare revenue growth with the growth in receivables and deferred revenue. Receivables growing much faster than revenue signals aggressive recognition or collection trouble. Deferred revenue growing faster than revenue signals cash arriving ahead of recognition, which is conservative.
6. Where the estimate of progress is subjective, flag it. This is the single largest lever a firm has to shift revenue between years.

**Worked example:** Netflix, 2019 balance sheet ($ thousands). Deferred revenue was 924,745 at end-2019 versus 760,899 at end-2018. Subscribers pay in advance, so cash arrives before the service is delivered. The 163,846 increase means Netflix collected that much more cash than it recognized as revenue on new subscription balances during the year. Revenues recognized were 20,156,447. Peloton shows the same mechanic on its 2019 balance sheet: customer deposits and deferred revenue of 90.8 million against 2019 revenue of 915.0 million, cash held for products and subscriptions not yet delivered.

**Determinism:**
- DETERMINISTIC: the arithmetic once the measure of progress is fixed. Inputs = contract price, costs incurred, total expected costs, prior recognition. Output = revenue for the period. Also deterministic: computing the revenue-to-receivables and revenue-to-deferred-revenue ratios and their year-over-year changes.
- JUDGMENT: deciding when a deal "occurs"; identifying performance obligations; judging progress on a multi-year build; deciding whether a firm's recognition is aggressive. This needs the revenue-policy footnote, the contract-balance disclosure, and comparison with peers.

**Pitfalls:**
- Assuming revenue equals cash collected. It does not, and the gap is where earnings management lives.
- Taking a multi-year contract's revenue split at face value. How much to book in the sale year and how much later is genuinely open to debate.
- Ignoring deferred revenue. It is a liability that represents cash already banked, and it behaves nothing like debt.
- Treating a rising receivables balance as automatically bad. Growth firms build receivables naturally; the test is whether receivables grow faster than revenue for several years running.

**Sources:**
- accounting__101--income_statements p.2
- accounting__101--income_statements p.6
- foundations_of_finance--cash_flows p.2
- accounting__101--balance_sheet_illustrations p.4

**Related:** [[income-statement-structure]], [[expense-classification-and-depreciation]], [[earnings-versus-cash-flows]], [[cash-flow-from-operations-and-working-capital]], [[segment-and-geographic-reporting]]
