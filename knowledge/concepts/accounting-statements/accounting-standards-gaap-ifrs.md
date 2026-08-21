# Accounting standards: GAAP, IFRS and comparability

**Core idea:** Accounting is a rule-driven process. Two forces drove the rules to be formalized, above all for publicly traded firms. One is standardization, so that firms can be compared. The other is first principles, so that earnings, asset value and cash flows measure what they are supposed to measure. World standards remain different, but they have largely converged on two: GAAP for US reporting, and IFRS for most of the rest. The practical lesson is that the convergence is real but incomplete. Gross profit, operating income and net income remain the common comparison anchors, yet inconsistent measurement and categorization of expenses can still break a cross-company comparison.

**Formulas:** None. This is an institutional and mapping concept. The relevant "formula" is the comparison anchor set: compare firms at `Gross Profit`, `Operating Income` and `Net Income`, after normalizing the expense classifications that feed each.

**Reference data:**

| Standard | Full name | Rule-setter | Scope |
|---|---|---|---|
| GAAP | Generally Accepted Accounting Principles | FASB (Financial Accounting Standards Board) | US financial reporting |
| IFRS | International Financial Reporting Standards | IASB (International Accounting Standards Board) | Companies listed globally; ~90 countries as of 2020 |

IFRS adoption status by country (as of the 2020 world map in the source):

| Category | Examples |
|---|---|
| IFRS required for domestic public companies | Canada, Latin America, Europe, Russia, much of Africa, the Middle East, Australia, much of Asia |
| Not required (major non-adopters) | United States (GAAP), China, India, Japan |
| Other legend categories on the map | IFRS permitted but not required for domestic public companies; IFRS required or permitted for foreign listings; IFRS for SMEs required or permitted; IFRS for SMEs under consideration |

Presentation differences you will actually meet:

| Feature | US GAAP filing | IFRS / Ind-AS filing |
|---|---|---|
| Balance sheet order | Current assets first | Non-current assets first; equity often before liabilities |
| Expense grouping | By function (COGS, SG&A, R&D) | Often by nature (materials consumed, employee benefits, depreciation) |
| Other comprehensive income | Separate statement or appended | Split into items that will and will not be reclassified to profit or loss |
| Terminology | Revenues, net income, stockholders' equity | Revenue from operations, profit for the year, total equity |

**Procedure:**
1. Identify the filer's regime from the auditor's report and the statement headings. US 10-K → GAAP. "Prepared in accordance with IFRS" or Ind-AS → IFRS family.
2. If comparing across regimes, do not compare line items directly. Map both filings to the three anchors: gross profit, operating income, net income.
3. Where the filing lists expenses by nature, re-map them to functional buckets before computing gross profit. Cost of materials consumed plus changes in inventories plus the production share of employee benefits approximates COGS.
4. Check where each firm draws the operating-income line. Some push equity income, FX gains and restructuring above it, others below. Move them to a consistent place yourself.
5. Note the currency and the fiscal-year end. Toyota's FY2020 ends 31 March 2020; Coca-Cola's 2019 ends 31 December 2019. These are not the same economic period.
6. Recompute the anchors on your own consistent definitions, then compare. Document every reclassification so the comparison is reproducible.

**Worked example:** Comparing Coca-Cola (GAAP, 2019, $ millions) with Dr. Reddy's Laboratories (Ind-AS/IFRS, FY2020, ₹ millions). Coca-Cola reports COGS of 14,619 and SG&A of 12,103, so gross profit (37,266 − 14,619) = 22,647 falls straight out. Dr. Reddy's reports no COGS line. It lists cost of materials consumed 25,565, purchase of stock-in-trade 11,172, changes in inventories (999), employee benefits 20,302, depreciation and amortisation 7,892, and "selling and other expenses" 33,768. To get a comparable gross profit, build a COGS proxy from the first three lines. Then split employee benefits and depreciation between production and overhead. That split is a judgment call. It is exactly the comparability problem the source warns about.

**Determinism:**
- DETERMINISTIC: identifying the regime from the filing; the arithmetic of the anchors once buckets are fixed; the currency and fiscal-year metadata.
- JUDGMENT: mapping nature-based expense lines onto functional buckets; deciding where the operating-income line belongs; deciding whether two firms' expense definitions are close enough to compare. This judgment needs the accounting-policy footnote and the segment note.

**Pitfalls:**
- Assuming that "same standard" means "same numbers." Even within GAAP, firms categorize expenses differently.
- Assuming standards are diverging. The source's view is the opposite — they are converging globally, so the differences that remain are mostly presentational and definitional, not conceptual.
- Comparing a nature-based expense statement with a function-based one line by line.
- Forgetting that revenues and operating expenses legitimately take different forms — product sales, subscriptions, interest income, commodity sales — while the end game (gross profit, operating income, net income) is the same.

**Sources:**
- accounting__101--financial_statements_overview p.9-10
- accounting__101--income_statements_illustrations p.13
- accounting__101--income_statements_illustrations p.12

**Related:** [[role-of-accounting-and-three-statements]], [[income-statement-structure]], [[sector-differences-in-financial-statements]], [[expense-classification-and-depreciation]], [[intangibles-and-goodwill]]
