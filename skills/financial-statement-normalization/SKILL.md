---
name: financial-statement-normalization
description: Converts reported financial statements into valuation-ready numbers — capitalizes R&D into a research asset, capitalizes operating leases into debt, strips one-time items, normalizes cyclical or trough earnings, derives FCFF and FCFE, and computes invested capital, ROIC, economic value added and the diagnostic ratio pack. Use when cleaning up EBIT before a DCF, capitalizing research or leases, deciding whether a restructuring charge is really non-recurring, computing free cash flow to the firm or to equity, measuring return on invested capital, normalizing earnings for a cyclical or commodity company, or building the base-year operating income and capital base that a valuation model consumes.
---

# Financial statement normalization

Accounting statements are not built for valuation. They are built to be auditable and
comparable, and those goals push them away from economic substance in three specific ways.
Research spending is an investment that the accountant expensed. Leases are debt that sat
off the balance sheet for decades and still get reported on rules nobody trusts. One-time
items sit inside operating income and get relabelled by management every year.

This skill applies the corrections and then derives what follows from them: cash flows,
the capital base, and the return earned on that capital. Every number the script produces
is a pure transform of numbers you supply. Which items are non-recurring, and how long
research takes to pay off in this business, are your calls.

## The script

`resources/normalize.py` — pure standard library, no installation needed. Every subcommand
takes JSON on stdin (or `--in FILE`) and prints JSON.

```bash
python3 resources/normalize.py <subcommand> --example    # show the input shape
python3 resources/normalize.py <subcommand> --in payload.json
python3 resources/normalize.py selftest                  # verify the engine
```

| Subcommand | Turns this | Into this |
|---|---|---|
| `capitalize-rd` | R&D history and an amortizable life | research asset, this year's amortization, the EBIT adjustment |
| `capitalize-leases` | lease commitments and a pre-tax cost of debt | lease debt, lease-asset depreciation, imputed interest, the EBIT adjustment |
| `cashflow` | corrected EBIT and reinvestment | FCFF, reinvestment rate, FCFE by either route |
| `invested-capital` | book equity, book debt, cash and the corrections | invested capital, ROIC, return spread, economic value added |
| `normalize-earnings` | a cycle of margins, returns or earnings | mid-cycle operating income |
| `ratios` | any subset of statement lines | margins, efficiency, leverage, liquidity, returns |
| `full` | all of the above in one payload | the whole chain, run in dependency order |

`selftest` checks 26 cases, including the algebraic invariant that flat R&D forever leaves
operating income untouched, and that spending exactly one amortizable life ago contributes
nothing to the research asset. A wrong amortization schedule fails both.

## The order of operations

The corrections are not independent. Leases change interest coverage, which changes the
cost of debt, which changes the discount rate used on the leases. R&D changes both the
numerator and the denominator of ROIC. Run them in this order.

```
Normalization progress:
- [ ] 1. Update the statements to a trailing twelve months
- [ ] 2. Capitalize R&D and any other multi-year spending
- [ ] 3. Capitalize operating leases, iterating on the cost of debt
- [ ] 4. Strip genuinely non-recurring items
- [ ] 5. Normalize the year if it is a peak or a trough
- [ ] 6. Rebuild invested capital and ROIC on the corrected numbers
- [ ] 7. Derive FCFF and FCFE
- [ ] 8. Read the ratio pack and check the story holds together
```

### 1. Update first

An annual report goes stale fast. Build trailing-twelve-month figures from the last 10-K
plus the latest 10-Q:

    TTM item = last 10-K annual figure − prior-year year-to-date + current-year year-to-date

This matters most for small firms, volatile firms, and firms that recently restructured.
The script has no subcommand for this because it is subtraction, not modelling. Do it
before anything else, so every correction below lands on current numbers.

## 2. Capitalizing R&D

Research spending buys benefits over several years, which makes it a capital expenditure
in economic substance. Accounting requires it to be expensed. The consequence is that an
R&D-heavy firm looks like it earns less than it does and reinvests nothing at all, while
its return on capital looks spectacular because the capital it built is invisible.

The fix treats each of the last N years of R&D as an investment being written off straight
line over N years. What is left unwritten-off is the **research asset**.

```bash
echo '{"current_rd": 100, "past_rd": [90, 80, 70, 60, 50], "amortizable_life": 5}' \
  | python3 resources/normalize.py capitalize-rd
```

`past_rd` runs backwards: index 0 is last year, index 1 the year before. Spending from
exactly `amortizable_life` years ago is fully written off, contributes nothing to the
asset, and still contributes its share to this year's amortization. Keep that row in.

Read three fields:

- `research_asset` — add to invested capital and to book equity.
- `amortization_this_year` — the charge that replaces this year's expensing.
- `adjustment_to_operating_income` — current R&D minus amortization. Add to reported EBIT.

The adjustment is positive when R&D is growing and negative when it is shrinking. For a
firm whose R&D has been flat for years it is zero, which is the sanity check: the
correction only matters when research spending is changing.

### Choosing the amortizable life

This is the one genuine judgment in the calculation. Ask how long research takes to pay
off in this business, then use the industry table as a default rather than a fact.

| Guideline block | Life | Typical sectors |
|---|---|---|
| Non-technological service | 2 | retail stores, grocery, banks, brokerage |
| Retail and technology service | 3 | software and IT services, internet, publishing, medical services |
| Light manufacturing | 5 | semiconductors, computer hardware, electronics, petroleum, medical supplies |
| Heavy manufacturing | 10 | machinery, autos, chemicals, electrical equipment, telecom equipment |
| Research with patenting | 10 | pharmaceuticals and biotech |
| Long gestation | 10 | aerospace and defence, air transport, utilities, cable |

The two cases worth naming: a software company amortizes over roughly three years — five
if it sells enterprise platforms with long product cycles — because a code base ages fast.
A pharmaceutical company amortizes over ten, because a compound spends most of a decade in
trials before it earns anything. Using a software life on a drug company shrinks the
research asset and inflates ROIC.

If you have fewer than N years of history, pad the missing years with zeros and say so.
The research asset is understated by exactly the padding.

The same machinery capitalizes any other spending that buys multi-year benefits: brand
advertising, employee training. Run it as a second `capitalize-rd` call with a different
life, and add both assets to capital.

## 3. Capitalizing operating leases

A lease is a fixed, tax-deductible commitment that must be paid whatever operations do,
and non-payment costs the firm the asset. That is the definition of debt. Treating the
payment as an operating expense understates both debt and operating income, and the effect
is enormous in lease-heavy sectors. Lease expense runs about 12.5% of operating income for
the whole market, about 27% for restaurants, about 44% for apparel stores, and about 50%
for furniture stores.

Discount the disclosed commitments at the **pre-tax cost of debt** — not the cost of
capital, not the riskfree rate.

```bash
echo '{"commitments": [100, 100, 100, 100, 100], "lump_sum_beyond": 300,
       "pre_tax_cost_of_debt": 0.05, "current_lease_expense": 110}' \
  | python3 resources/normalize.py capitalize-leases
```

`commitments` is the itemized schedule from the footnotes, usually five years.
`lump_sum_beyond` is the single "thereafter" figure. It is not one payment. The script
infers how many years it covers by dividing it by the average of the itemized years and
rounding, then discounts it as an annuity starting after the itemized years. Here 300
against an average of 100 implies three more years, so the lease life is eight.

Read four fields:

- `lease_debt` — add to debt, to invested capital, and to debt in the equity bridge.
- `depreciation_on_lease_asset` — lease debt divided by the full lease life.
- `adjustment_to_operating_income` — lease expense minus that depreciation. Add to EBIT.
- `imputed_lease_interest` — lease debt times the pre-tax cost of debt. Add to interest
  expense wherever interest coverage is computed.

The asset is created at exactly the same value as the debt. Adding the debt and forgetting
the asset understates capital and inflates every return you compute afterwards.

Check the result: net income must be unchanged. The higher EBIT is exactly offset by the
higher imputed interest. If net income moves, the lease payment has been counted twice.

### The circularity, and how to iterate it

Discounting leases needs a pre-tax cost of debt. When the company has no traded bonds and
no agency rating, that rate comes from a synthetic rating built on interest coverage. But
capitalizing leases changes interest coverage, in both the numerator and the denominator.
The rate depends on the answer that depends on the rate.

Iterate to a fixed point. Two to four passes is normal.

```bash
# Pass 1 — first-guess rate from reported coverage
echo '{"ebit": 1012, "interest_expense": 120, "riskfree_rate": 0.04,
       "marginal_tax_rate": 0.35, "table": "large_manufacturing"}' \
  | python3 ../cost-of-capital-toolkit/resources/costofcapital.py rating
# read pre_tax_cost_of_debt

# Pass 2 — capitalize at that rate
echo '{"commitments": [899, 846, 738, 598, 477], "lump_sum_beyond": 1425,
       "pre_tax_cost_of_debt": 0.055, "current_lease_expense": 978}' \
  | python3 resources/normalize.py capitalize-leases
# read lease_debt, imputed_lease_interest, adjustment_to_operating_income

# Pass 3 — re-rate on lease-adjusted coverage, then go back to pass 2
#   ebit             = reported EBIT + adjustment_to_operating_income
#   interest_expense = reported interest + imputed_lease_interest
```

Stop when the pre-tax cost of debt moves by less than a basis point between passes. Record
the final rate, because the rest of the valuation has to use the same one.

Two notes on the modern statements. Since 2019 both IFRS and US GAAP require operating
leases on the balance sheet, which validates this adjustment. The official rules are far
more complicated than a present value, because standard-setters preserved continuity with
legacy treatment. When the reported lease liability looks inconsistent with the commitment
schedule, recompute it here and use your own number.

## 4. Stripping one-time items

A charge is non-recurring only if it is both **infrequent** and **variable in amount**. An
item that appears every year is recurring whatever the firm calls it, even when it flips
between gains and losses — a sign flip is variability, not infrequency.

Pull five to ten years of statements and count. For each item type, how many of those
years does it appear in?

| Item | Test that decides it |
|---|---|
| Gain or loss on selling a division | Does this firm divest routinely? Commodity firms do, every year |
| Restructuring charge | Repeated restructurings are an operating cost of the business model |
| Goodwill impairment | Acquisitive firms impair repeatedly; it records a real past cash overpayment |
| Litigation cost or fine | Serial litigants show this annually |
| Asset write-off | Count the years. Also note that write-offs shrink the capital base and flatter next year's ROIC |

The middle case is the one that matters most. A firm reports a $500m loss containing a
$1bn charge it calls one-time. If the charge is genuinely once-ever, value the firm off
$500m of profit. If the firm books a charge like this roughly every five years, it is a
recurring cost: build in $1,000m / 5 = $200m every year, giving $300m of sustainable
operating profit. Neither headline number is right.

Pass accepted adjustments to `full` as `one_time_items`. Sign them from the point of view
of operating income: a charge you are adding back is positive, a non-recurring gain you
are removing is negative.

```json
"one_time_items": [
  {"description": "2023 plant fire, insurance shortfall", "ebit_effect": 140.0},
  {"description": "gain on sale of the Brazilian unit", "ebit_effect": -85.0}
]
```

These carry no capital effect. Do not accept management's label, and do not accept an
"adjusted EBITDA" figure that has not been reconciled line by line to the audited
statement.

## 5. Normalizing a peak or a trough

Diagnose the cause before you normalize anything. There are five, and they split into two
treatments.

| Cause | Treatment |
|---|---|
| Temporary problem — a fire, a disrupted quarter | Normalize |
| Cyclicality — an auto or commodity firm in a recession | Normalize |
| Life cycle — a young firm, or infrastructure still being built | Forecast from revenues instead |
| Leverage — healthy operations, too much debt | Forecast from revenues instead |
| Long-term operating problem — structural cost or production trouble | Forecast from revenues instead |

Normalizing a firm whose problems are structural values a company that no longer exists.
For the three forecast cases, use `dcf-valuation-engine` with a revenue-driven build and a
target margin, rather than this subcommand.

```bash
echo '{"method": "average_margin", "historical_margins": [0.12, 0.08, -0.02, 0.05, 0.11],
       "current_revenue": 10000, "reported_ebit": -200}' \
  | python3 resources/normalize.py normalize-earnings
```

Three methods, chosen by what has changed about the firm:

- `average_margin` — average the operating margin over the cycle and apply it to current
  revenue. Use when the firm has grown or shrunk, and you want to keep its current scale.
- `average_roc` — average the return on capital and apply it to current invested capital.
  Use when you want to keep its current asset base, and when the margin is unstable
  because the asset mix changed.
- `average_earnings` — average the dollar earnings. Only defensible when firm size has
  barely moved across the window. The script returns a caveat saying so.

Choose the window to span a full cycle. Five years is the working default; commodity
cycles run longer. Do not choose a window that starts at the trough and ends at the peak.
When the firm was hit by a specific shock, use the pre-shock cycle instead of straddling it.

Then carry the fix through. Normalized EBIT changes interest coverage, which changes the
synthetic rating and the cost of debt, which changes the discount rate. It also changes
the reinvestment rate and the return on capital that drives growth. Be consistent about
which numbers are normalized: a normalized EBIT paired with a depressed current coverage
ratio is a broken model.

A normalized, mature firm may deserve no high-growth period at all.

## 6. Invested capital and ROIC

```bash
echo '{"book_value_of_equity": 5000, "book_value_of_debt": 3000, "cash": 1000,
       "lease_debt": 500, "research_asset": 250,
       "ebit_after_tax": 750, "cost_of_capital": 0.08}' \
  | python3 resources/normalize.py invested-capital
```

    invested capital = book equity + book debt − cash + lease debt + research asset

Cash comes out because it earns a financial return, not an operating one. The numerator
excludes interest income, so the denominator must exclude the cash that produced it.
Leaving cash in understates the return on the operating business.

Measure the capital at the **start** of the period, so that the income in the numerator was
actually earned on it. Using end-of-year capital mechanically depresses the ratio for a
growing firm.

The output carries `roic`, `return_spread` against the cost of capital, and
`economic_value_added`, which is the spread times the capital. A positive spread means
growth creates value; a negative one means growth destroys it, and growing faster makes it
worse.

Before trusting the number, run the six-distortion check. ROIC is built from two badly
measured numbers.

| Distortion | Where | Effect |
|---|---|---|
| Abnormal earnings this year | Numerator | The ratio reports a cycle position, not a return |
| R&D expensed, leases off balance sheet | Both | Understates income and understates capital |
| One-time gains or charges left in | Numerator | Random noise |
| Life-cycle effect at a young firm | Both | Current earnings say nothing about long-run potential |
| Past write-offs | Denominator | The worse the history, the better the ratio looks |
| Inflation on old assets | Denominator | Understates capital, overstates return for asset-heavy firms |

Compare the result to the firm's own history and to the industry. A ROIC far above the
industry that you cannot explain by a durable advantage is a signal to fade it, not to
extrapolate it. Empirically, excess returns persist longer than growth does — so fade
growth faster than you fade the spread.

### The rule that breaks most models

**The EBIT adjustment and the capital adjustment always move together.** Every correction
in this skill has two legs:

| Correction | EBIT leg | Capital leg |
|---|---|---|
| R&D capitalization | + current R&D − amortization | + research asset |
| Lease capitalization | + lease expense − lease depreciation | + lease debt |
| One-time items | ± the accepted adjustment | none |

Applying the earnings leg alone raises the numerator of ROIC and leaves the denominator
untouched. The return looks better than it is, and because fundamental growth is
`reinvestment rate × ROIC`, that error propagates straight into an inflated growth rate and
an inflated valuation. This is the single most common porting error when these adjustments
are done by hand in a spreadsheet.

The correction usually cuts ROIC rather than raising it, because capital rises
proportionally more than earnings. Capitalizing R&D at SAP moved return on capital from
29.9% to 19.2%. Capitalizing leases at The Gap moved it from 12.9% to 9.3%. If your
corrected ROIC went up, check that both legs landed.

The `full` subcommand threads both legs automatically, which is the main reason to use it.

## 7. Cash flows

```bash
echo '{"ebit": 1000, "tax_rate": 0.25, "capital_expenditures": 300, "depreciation": 200,
       "change_in_noncash_working_capital": 50, "net_income": 600, "debt_ratio": 0.3}' \
  | python3 resources/normalize.py cashflow
```

    net capital expenditures = capex + acquisitions + capitalized R&D − depreciation
    reinvestment             = net capital expenditures + change in non-cash working capital
    FCFF                     = EBIT × (1 − tax rate) − reinvestment

`ebit` here means the corrected EBIT, not the reported one. Losses are not taxed: when
EBIT is negative the script passes it through untouched rather than manufacturing a tax
credit.

Two things belong in reinvestment that the cash flow statement hides. Acquisitions sit in
the investing section, usually under "other investing activities" — pass a multi-year
average as `acquisitions`, because most firms do not acquire every year. Capitalized R&D
is not in the statement at all — pass it as `rd_capitalized_this_year`.

Use the **non-cash** working capital definition: non-cash current assets minus non-debt
current liabilities. Leaving cash and short-term debt in makes working-capital
"investment" swing with the cash balance and the debt maturity schedule, neither of which
is operating. Forecast it as a percent of revenue rather than extrapolating last year's
dollar change, which is noise.

FCFE arrives by whichever route the payload supports. Pass `debt_ratio` for the
stable-leverage shortcut, in which debt funds a constant fraction of every dollar of
reinvestment. Pass `new_debt_issued` and `debt_repaid` to model the debt flows explicitly.
Use the shortcut only when leverage really is stable; when it is changing, value the firm
with FCFF and skip FCFE entirely.

Never put interest expense, interest tax savings, or debt flows into FCFF. The tax shield
already lives in the `(1 − t)` on the cost of debt inside the WACC.

### Keeping FCFF invariant to the R&D correction

Capitalizing R&D should leave FCFF unchanged. After-tax operating income and net capital
expenditure both rise by the same amount, so the cash flow is untouched — only earnings,
capital, ROIC and therefore growth change. Two payload conventions make that identity hold,
and the script will not apply either for you.

**Add the amortization to depreciation.** Adjusted depreciation is reported D&A plus
`amortization_this_year` from `capitalize-rd`. Otherwise net capital expenditure is
overstated by the amortization.

**Do not tax the add-back.** The firm already deducted the full R&D expense, so the cash
taxes it paid were computed on reported operating income. Supply the effective rate on the
corrected EBIT:

    tax rate to pass = marginal rate × reported EBIT / adjusted EBIT

Worked check, with reported EBIT 1,000, current R&D 100, amortization 60, marginal rate
25%, capex 300, reported depreciation 200 and a working capital change of 50:

```
adjusted EBIT        = 1,040
tax rate to pass     = 0.25 × 1,000/1,040 = 0.240385
after-tax operating income = 1,040 × (1 − 0.240385) = 790   ( = 750 + 40 )
depreciation to pass = 200 + 60 = 260
net capital expenditures   = 300 + 100 − 260 = 140
FCFF = 790 − 140 − 50 = 600                                  ( = unadjusted FCFF )
```

Both conventions are payload-level, so they work inside `full` too: set
`cash_flow.depreciation` and `cash_flow.tax_rate` explicitly, and `full` will respect them.
Run `capitalize-rd` first to read the amortization, then build the payload. Left at the
defaults, `full` taxes the add-back and omits the amortization, and the bundled example
reports FCFF of 530 where the invariant says 600.

The lease correction behaves differently and does need the tax. Its imputed interest
deduction moves into the WACC, so the corrected EBIT is taxed in full. Leave net capital
expenditure alone for leases — new leases signed each year replace the depreciation — and
remember that the higher cash flow is paid for by the `lease_debt` you add to debt in the
equity bridge.

## 8. The ratio pack

```bash
python3 resources/normalize.py ratios --in statements.json
```

Every field is optional. Anything the payload does not support comes back as `null` rather
than a crash, so this is useful part-way through an analysis. Feed it corrected numbers,
not reported ones — an interest coverage ratio that ignores imputed lease interest will
buy a synthetic rating the company does not deserve.

The three readings that carry the most information: `sales_to_capital`, because it is the
input a driver-based DCF needs to convert growth into reinvestment; `interest_coverage`,
because it drives the synthetic rating; and `return_spread`, because it decides whether
growth is worth anything.

## Running the whole chain

```bash
python3 resources/normalize.py full --example
python3 resources/normalize.py full --in company.json
```

`full` applies the corrections in dependency order, threads both legs of each into EBIT and
into capital, and returns an `adjustments` array showing what each correction did to each.
Read that array first: it is the audit trail, and a reviewer will ask for it.

## Handing the results onward

| Field from this skill | Goes to | As |
|---|---|---|
| `adjusted_ebit` | `dcf-valuation-engine` `value` | `base_ebit` |
| `capital.invested_capital` | `dcf-valuation-engine` `value` | `base_invested_capital` |
| `lease_debt` | `dcf-valuation-engine` `value` | added to `bridge.debt` |
| `lease_debt` | `cost-of-capital-toolkit` `wacc` | added to the market value of debt |
| `adjusted_ebit`, imputed lease interest | `cost-of-capital-toolkit` `rating` | `ebit`, added to `interest_expense` |
| `ratios.efficiency.sales_to_capital` | `dcf-valuation-engine` `value` | `sales_to_capital` |
| `roic` | `dcf-valuation-engine` `value` | sanity bound on `terminal.return_on_capital` |

Run `valuation-consistency-checks` over the finished artifacts before accepting any of it.

## Common failures

| Symptom | Cause |
|---|---|
| ROIC rises after the corrections | The EBIT leg was applied and the capital leg was not |
| An R&D-heavy firm shows almost no reinvestment | R&D never added to capital expenditure |
| FCFF changes when R&D is capitalized | Amortization missing from depreciation, or the add-back taxed |
| Net income moves after capitalizing leases | The lease payment is counted twice |
| Synthetic rating too good for an obviously levered retailer | Imputed lease interest left out of interest coverage |
| The cost of debt keeps changing between passes | The lease circularity was never iterated to a fixed point |
| Lease debt looks implausibly small | The "thereafter" lump treated as a single payment instead of an annuity |
| Research asset far below the peer group | Fewer than N years of history, padded with zeros |
| Corrected ROIC still spectacular for an asset-heavy firm | Old book values unadjusted for inflation, or past write-offs shrank the base |
| Growth rate implausible off a normalized base | Normalized EBIT paired with an unnormalized return on capital |
| Normalized value far above any plausible price | A structural problem normalized away as though it were cyclical |
| `capitalize-leases` refuses to run | A non-positive cost of debt; commitments cannot be discounted at zero |
| Reinvestment rate returns `null` | After-tax operating income is negative or zero, so the ratio has no meaning |
