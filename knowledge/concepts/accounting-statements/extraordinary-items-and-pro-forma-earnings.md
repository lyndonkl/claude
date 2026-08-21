# Extraordinary items and pro-forma earnings

**Core idea:** An extraordinary item is one the firm does not face in the normal course of business. The test has two parts: it must be infrequent and its amount must vary. An item that shows up every single year is not extraordinary, even if it flips between gains and losses. Firms have grown creative with pro-forma statements that strip such items out. Some do it to fix what they see as flaws in the rules. Others do it to make profits look better. Never take a pro-forma number at face value. Build your own smell test for what should be added back and what should not.

**Formulas:**
- `Normalized Operating Income = Reported Operating Income + Add-backs you accept − Add-backs you reject − Recurring items the firm excluded`.
- Recurrence test: over a window of N years (use N ≥ 5), compute `Frequency = (number of years the item appears) / N` and `Variability = standard deviation of the item / mean absolute value of the item`.
- Decision rule: treat as extraordinary only if `Frequency` is low (the item is absent in most years) AND `Variability` is high. If `Frequency = 1.0`, the item is recurring, whatever the firm calls it.
- Average-out alternative for items that recur but swing: `Normalized charge = average annual charge over the last N years`, deducted every year rather than excluded.

**Reference data:** Items commonly labeled extraordinary, and how to test them.

| Item | Typical claim | Test |
|---|---|---|
| One-time cost or gain from selling assets or divisions | Not part of operations | Does the firm divest routinely? Commodity firms divest every year |
| Write-offs or charges from past projects | Sunk, non-recurring | Count the years it has appeared |
| Litigation costs and fines | One-off legal event | Serial litigants show this annually |
| Goodwill impairment | Non-cash, backward-looking | Acquisitive firms impair repeatedly |
| Restructuring charges | One-time reorganization | Repeated restructurings are an operating cost of the business model |

The two pro-forma manoeuvres that deserve the most attention:

| Manoeuvre | Description | When it may be merited | When it is not |
|---|---|---|---|
| Shifting expenses from operating to capital | Reclassify a current expense as an asset to be written off later | R&D and brand spending that genuinely buys multi-year benefits | Ordinary operating costs relabelled to lift current earnings |
| Removing expenses as one-time or extraordinary | Exclude a charge from "adjusted" earnings | Genuinely infrequent, variable events | Charges that recur every year in some form |

**Procedure:**
1. Pull the last five to ten years of income statements. Build a table of every item the firm has ever labelled one-time, non-recurring, extraordinary, restructuring, impairment or "adjusted out."
2. For each item type, count the number of years it appears. Any type appearing in most years is recurring. Put it back into operating expenses.
3. For types that genuinely appear rarely, check the amount's variability. Low variability plus regular appearance means it is a disguised operating cost.
4. Reconcile the firm's pro-forma earnings to GAAP or IFRS earnings, line by line. Every add-back must be named.
5. Judge each add-back separately. Accept only those that pass your recurrence test and your economic test.
6. For an operating-to-capital shift, ask whether the spending buys benefits over several years. If yes, capitalize it consistently across all years and amortize it. Do not accept a one-year shift.
7. For recurring-but-lumpy charges, do not exclude them. Average them over the window and deduct the average every year.
8. Recompute operating income and net income on your own definitions. Use those, not the firm's adjusted figures.

**Worked example:** HSBC, 2019 ($ millions). The income statement carries a goodwill impairment of (7,349) inside total operating expenses of (42,349). Profit before tax was 13,347 and profit for the year 8,708. A pro-forma presentation excluding the impairment would show profit before tax of roughly 20,696 — more than half again as large. The recurrence test asks whether an acquisitive global bank writes down goodwill only once. Because impairments track sector pricing moves and recur across cycles, the correct treatment is not simple exclusion. Either leave the charge in, or normalize it by averaging impairments over a multi-year window. Compare with Total in 2019, which reports exploration costs of 785 (against 797 in 2018 and 864 in 2017). Some firms would call exploration write-offs "one-time," but the three-year record shows a stable recurring cost of doing business.

**Determinism:**
- DETERMINISTIC: the frequency count and variability statistic over a fixed window; the reconciliation arithmetic from pro-forma back to reported earnings; the recomputed normalized income once you decide which add-backs stand.
- JUDGMENT: whether each add-back is fair. This needs the multi-year filing history, the management discussion, an understanding of the business model, and knowledge of how peers treat the same item. Whether an operating-to-capital shift is merited is judgment about the economic life of the spending.

**Pitfalls:**
- Accepting "adjusted EBITDA" or any pro-forma number without reconciling it to the audited statement.
- Treating an item as extraordinary because the firm says so. Apply the two-part test yourself.
- Excluding a charge that flips sign each year. Sign flips are variability, not infrequency; a yearly item is recurring regardless.
- Capitalizing an expense in the current year only. A capitalization must be applied to prior years too, or the trend is corrupted.
- Excluding non-cash charges reflexively. Goodwill impairment is non-cash, but it records a real past cash overpayment.

**Sources:**
- accounting__101--income_statements p.12-13
- accounting__101--income_statements_illustrations p.11
- accounting__101--income_statements_illustrations p.9

**Related:** [[expense-classification-and-depreciation]], [[income-statement-structure]], [[intangibles-and-goodwill]], [[earnings-versus-cash-flows]], [[accounting-earnings-adjustments]], [[normalized-earnings]]
