# Reported earnings to actual earnings

**Core idea:** The earnings number a company reports is an accounting output, not a valuation input. Before it can be used in a DCF it must be put through three operations: **update** it (annual reports go stale, so rebuild a trailing-12-month figure), **cleanse** it (strip financial expenses and capital expenses that accounting has buried inside operating expenses, and strip genuinely non-recurring items), and **normalize** it (if the current year is unrepresentative). This note is the umbrella framework plus the two adjustments that have no separate procedure of their own — one-time charges and accounting malfeasance. The two big mechanical cleansings (operating leases, R&D) and the negative-earnings case have their own notes.

**Formulas:**
- Trailing-12-month (TTM) line item = Annual figure from the last 10K − Year-to-date figure for the same period last year + Year-to-date figure from the latest 10Q.
  - Example for a Q3 10Q: TTM Revenue = Revenues (last 10K) − Revenues from first 3 quarters of last year + Revenues from first 3 quarters of this year.
  - Works identically for revenues, EBIT, interest expense, taxes, R&D — any income-statement line.
- Adjusted operating income = Reported operating income + Operating-lease expense − Depreciation on the leased asset + Current-year R&D − Amortization of the research asset − (non-recurring gains) + (genuinely non-recurring charges).
  - All terms in the same currency units; the lease and R&D terms are produced by the two procedures linked below.
- Annualized recurring charge (when "one-time" charges recur every k years) = Charge amount / k, held in operating income every year.

**Procedure:**
1. **Update.** If the last 10K is more than a quarter old, build TTM figures from one 10K plus the latest 10Q, using the 10Q year-to-date columns. Prioritize updating for (a) small firms, (b) volatile firms, (c) firms that recently restructured. If no quarterly filing exists, use informal/unofficial numbers rather than a stale annual report.
2. **Remove financial expenses booked as operating.** Test: is it a *tax-deductible commitment that must be met regardless of operating results, whose non-payment costs you control of the business*? If yes it is debt service, not an operating cost. Operating leases are the canonical case -> run [[operating-lease-capitalization]]. Reclassification changes operating income and debt; it does not change equity earnings.
3. **Remove capital expenses booked as operating.** Test: *is the expense expected to generate benefits over multiple periods?* If yes it is an investment. R&D is the canonical case -> run [[rnd-capitalization]]. The same machinery handles brand-building advertising and employee training/human capital.
4. **Strip one-time and non-recurring items.** Add back genuine one-time charges (and subtract one-time gains). Decision rule: if a firm reports "one-time" charges with regularity — e.g. once every five years — they are not one-time; annualize them (charge/5 per year) and leave them in earnings instead of adding them back.
5. **Screen for accounting malfeasance.** Run the six-signal checklist (Reference data). Statement analysis cannot catch outright fraud; it can catch aggressiveness, which you then correct for (haircut earnings, raise the discount rate, or raise a failure probability).
6. **Normalize if the year is unrepresentative** (cyclical trough, temporary problem, negative earnings) -> [[normalizing-depressed-earnings]].
7. Recompute everything downstream that touches the adjusted number: effective tax rate, net cap ex, book capital, return on capital, reinvestment rate, growth.

**Reference data:**

Warning signals for aggressive/manipulated earnings:
| # | Signal |
|---|---|
| 1 | Income from unspecified/unnamed sources — undisclosed holdings, special purpose entities |
| 2 | Income from asset sales or financial transactions at a *non-financial* firm |
| 3 | Sudden changes in standard expense items — e.g. a big drop in SG&A or R&D as a percent of revenues |
| 4 | Frequent accounting restatements |
| 5 | Accrual earnings consistently running ahead of cash earnings |
| 6 | Big differences between tax-book income and reported income |

Magnitude of the two big cleansings (why they matter), as a percent of operating income:
| Item | Whole market | Worst sectors |
|---|---|---|
| Operating lease expense | ~12.5% | Furniture stores ~50%, apparel stores ~44%, restaurants ~27% |
| R&D expense | ~10.5% | Computers ~50%, petroleum ~30% |

**Worked example:** A firm reports a **$500m loss** that includes a **$1 billion one-time charge**. Do you value it off the $500m loss, or off the $500m profit (loss plus the charge added back)? If the charge is truly non-recurring, use the **$500m profit**. But if the firm books such a charge roughly **once every five years**, it is recurring: build $1,000m/5 = **$200m per year** into normalized earnings, giving $500m − $200m = **$300m** of sustainable operating profit — neither headline number.

**Determinism:**
- DETERMINISTIC: TTM construction (10K annual figure + prior-year YTD + current-year YTD -> TTM figure). Annualizing a recurring charge once the charge size and cycle length are given. The adjusted-operating-income arithmetic once the lease and R&D adjustments are computed.
- JUDGMENT: classifying an expense as financial vs operating vs capital; deciding whether a charge is genuinely one-time (needs the firm's 5–10 year history of "special items"); reading the six red flags (needs segment disclosures, cash-flow statement, tax footnote); deciding whether the current year is representative at all.

**Pitfalls:**
- Valuing off a stale 10K for a fast-moving or recently restructured company.
- Accepting management's "non-recurring" label — serial restructurers have made restructuring a recurring cost of doing business.
- Adjusting operating income for leases/R&D but forgetting the matching balance-sheet changes (lease debt + lease asset; research asset added to book capital). This silently corrupts return on capital and the reinvestment rate.
- Believing statement analysis can detect fraud. It can only detect aggressiveness.
- Double-counting: reclassifying lease expense out of operating costs and also leaving the lease payment in the forecast cash flows.

**Sources:**
- valpacket1spr21 p.121-123, p.133-134
- valpacket1spr20 p.118-120, p.130-131
- valpacket1spr21 p.124, p.129 (sector magnitude charts)
- valpacket1spr20 p.121, p.126 (sector magnitude charts)
- spreadsheet:fcffsimpleginzu.xlsx — `Trailing 12 month` helper sheet (TTM = last 10K − prior-year YTD + current-year YTD)

**Related:** [[operating-lease-capitalization]], [[rnd-capitalization]], [[normalizing-depressed-earnings]], [[tax-rate-and-nols]], [[return-on-invested-capital]], [[fcff]], [[accounting-earnings]], [[complexity-discount]]
