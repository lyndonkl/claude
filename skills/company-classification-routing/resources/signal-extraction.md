# Signal extraction — how each S1 signal is computed

The gates in S2 through S6 consult signals, not impressions. Every signal is computed from
`raw-financials.json` and `market-data.json`, carries a confidence, and cites the evidence
that set it.

The arithmetic is mechanical. The judgment is whether the computed number is
*representative*. A coverage ratio taken at a trough, a beta on a barely-traded stock, a
margin distorted by one large contract — each is correctly computed and wrong to route on.
Record that judgment beside the number, in `diagnosis.md`.

## Order of computation

Some signals depend on others. Compute in this order.

1. `sector_type` — everything else reads differently once you know this.
2. `revenue_status`, `life_cycle_stage`, `intangible_intensity` — read off the statements.
3. Run the S3 statement repair. It changes EBIT, invested capital and coverage.
4. `earnings_status`, `leverage_state`, `distress_markers` — these use the restated basis.
5. `payout_coverage`, `macro_driver`, `holdings_share`, `business_count`.
6. `ownership`, `stake_size`, `buyer_diversification`, `transaction_motive`,
   `geography_exposure`, `option_candidates` — read from the mandate and the filings.

Step 3 matters. An unrepaired coverage ratio at an intangible-heavy firm is wrong in both
directions at once, because R&D sits in the wrong place.

---

## sector_type

**Inputs.** Business description, segment note, and the shape of the three statements.

**How to read the statements.** The shape is more reliable than the label a data vendor
attached.

| Sector | Income statement tell | Balance sheet tell |
|---|---|---|
| Financial service | Revenue reported as net interest income and net fee income. Interest expense inside operations. A recurring credit-loss provision. | Almost entirely financial assets. Deposits the largest liability. Equity a thin slice — HSBC ran 7.1% of assets in 2019. Negligible PP&E. |
| Commodity | Excise taxes deducted from sales. Exploration costs a separate line. Very large depreciation, depletion and impairment. | Value in PP&E and reserves. Inventories swing with prices. |
| Intangible-heavy | Large R&D or brand-advertising lines. | Accounting intangibles far below firm value, because R&D was expensed. |
| Captive finance inside a manufacturer | Financing revenues and cost of financing reported separately. | Large current and non-current finance receivables. |

**Judgment.** Hybrid firms. A manufacturer with a captive finance arm is not a bank, but
its finance arm is, and B10 splits them. A fintech that lends off its own balance sheet is
a financial service firm whatever it calls itself. An insurer is B5.

**Detail.** `knowledge/concepts/accounting-statements/sector-differences-in-financial-statements.md`.

---

## life_cycle_stage

**Inputs.** Revenue level, revenue growth, margin sign and stability, reinvestment
intensity, firm age.

**Method.** Match three patterns and take the majority.

1. **Revenue and profit.** Small revenue with high growth and losses is start-up. High
   growth with accelerating losses is young growth. High growth with losses shrinking into
   profits is high growth. Slowing growth with climbing profits is mature growth. Flat
   revenue with level profits is mature stable. Falling revenue with profits falling faster
   is decline.
2. **The cash flow sign triple** — the signs of operating, investing and financing cash
   flow. Negative operating cash with heavy investing and equity inflows means start-up or
   young growth. Positive and growing operating cash with slowing investing means high or
   mature growth. Stable operating cash with maintenance investing and cash returned to
   equity means mature stable. Falling operating cash with divestitures and debt repayment
   means decline.
3. **Balance-sheet cross-check.** Negative equity from accumulated losses plus
   cash-dominated assets means young. Large retained earnings, heavy treasury stock and a
   high `Accumulated depreciation / Gross PP&E` ratio mean mature or aging. Toyota ran
   56.7% on that ratio in FY2020.

**Judgment.** Do not force one label when the signals conflict. Note which statement points
where. Netflix in 2019 looked mature on the income statement and young on the cash flow
statement. Two firms with identical sign triples sit in different stages when one is
capital-light software and the other a capital-heavy manufacturer.

**Why it matters beyond routing.** The stage names the dominant uncertainty, and therefore
where the analytical effort goes. Stage 1 asks whether the idea has potential. Stages 2
through 5 are dominated by macro questions: is there a business model, will it generate
profits, can it be scaled, can it be defended. Stage 6 asks whether management will face
reality. Stages 1 and 6 are company-specific; the middle is macro.

**Detail.** `knowledge/concepts/accounting-statements/life-cycle-patterns-in-financial-statements.md`,
`knowledge/concepts/narrative-numbers/life-cycle-uncertainty.md`.

---

## earnings_status

**Inputs.** Trailing twelve-month EBIT and net income, on the S3-restated basis.

**Method.** Take the sign first. Then test representativeness against the firm's own
five-year history and the sector's current position.

| Value | Test |
|---|---|
| `profitable` | Positive EBIT, within the normal band of the firm's own history. |
| `marginal` | Positive but thin enough that small assumption changes flip the sign. |
| `negative-transient` | Negative, with peers showing the same pattern, a known sector downturn, years of prior normal margins, and a balance sheet that survives to recovery. |
| `negative-structural` | Negative, with falling market share, a structural demand shift, or leverage forcing asset sales. |
| `cyclical-trough` | Positive but well below the firm's full-cycle average, at a recognised low in the cycle. |
| `cyclical-peak` | Positive and well above the full-cycle average, at a recognised high. |

**Judgment.** The transient-versus-structural call is the single highest-leverage judgment
in the routing tree. It decides B7 against B1, and the two produce very different values
from identical data. Normalization applied to a permanently broken business produces a
healthy EBIT for a firm that will never earn it. State the evidence on both sides in
`diagnosis.md`, then say which side wins and why.

---

## revenue_status

**Inputs.** Trailing revenue against the three-year and five-year figures.

`pre-revenue` means no meaningful revenue at all, not merely small revenue. `declining`
needs a multi-year window, because one bad year is noise. Check for an acquisition or
divestiture inside the window before reading a growth rate.

---

## g_firm versus g_econ

**Computation.** Expected near-term growth, against nominal growth in the economy of the
valuation currency. The riskfree rate in that currency is the standing proxy for nominal
economy growth.

| Screen | Stage count |
|---|---|
| `g_firm ≤ g_econ` | one stage |
| `g_firm ≤ g_econ + 10%` | two stages |
| `g_firm > g_econ + 10%` | three or more stages |

This sets the shape of the forecast, not the growth rate itself.

---

## leverage_state

**Computation.** Market `D/(D+E)`, including capitalized lease debt. Compare against the
sector median and against any stated target. Look at the trajectory over three to five
years.

`extreme` is above 50%. That threshold also appears in S6, where extreme leverage plus
negative earnings triggers the equity-as-option cross-check.

**Judgment.** Gross against net debt. A firm holding large cash for a known purpose is not
the same as one holding it idly. Say which basis you used and use it consistently
downstream.

---

## payout_coverage

**Computation.** `Σ5yr (dividends + buybacks) / Σ5yr FCFE`. Buybacks belong in the
numerator; a firm returning cash only through repurchases has not stopped paying out.

| Range | Route on the equity path |
|---|---|
| Below 80% | FCFE — dividends understate capacity |
| 80% to 110% | Dividends — payout tracks capacity |
| Above 110% | FCFE — the firm is paying more than it generates |

---

## distress_markers

**Inputs and count.** Each marker present is recorded with its evidence.

- Interest coverage below 1, on the restated basis.
- Rating at or below CCC.
- Traded bonds well below par.
- Negative book equity.
- A covenant breach, actual or waived.
- A going-concern note from the auditor.
- Sector peers already in distress.

One marker is a flag. Two or more push S6 to fire. The bond price is the most informative
single marker, because it is the market's own probability and can be inverted directly.

**Judgment.** A depressed bond price can reflect illiquidity rather than default risk.
Check the issue size and recent trading before inverting it.

---

## intangible_intensity

**Computation.** `R&D / revenues` and `R&D / (R&D + net capex)`. For human-capital firms
substitute recruiting and training spend. For consumer-products firms use the
brand-building share of advertising.

**Judgment.** Splitting advertising into brand-building and maintenance. Only the
brand-building portion is capital. Treating the whole budget as capital is a listed B8
constraint violation.

---

## geography_exposure

**Computation.** Revenue share by country or region, and production share where it differs.
Read from the geographic segment note.

**The rule.** Assign by exposure, never by country of incorporation. A Brazilian exporter
carries less Brazil risk than a Brazilian retailer. Coca-Cola and Heineken carry
substantial emerging-market risk while incorporated in developed markets.

Where production location, sourcing, hedging or demand sensitivity make exposure differ
from the revenue split, the B9 lambda route replaces revenue weighting. Use a lambda only
when you can justify it. Otherwise fall back to revenue weighting and say so.

---

## ownership, stake_size and buyer_diversification

**ownership.** Public, private, subsidiary or division. Record free float, insider and
institutional holdings, dual-class structure, and any cross-holdings. Fewer than three
years of statements, or statements mixing personal and business expense, force the B13
cleanup regardless of what the ownership field says.

**stake_size.** Above 50% is controlling and prices off the optimal value. At or below 50%
is minority and prices off the status quo value.

**buyer_diversification.** This is a fact about the transaction, not about the company. A
single undiversified individual buyer prices total risk, so B13-I applies a total beta. A
public acquirer's investors are diversified, so a market beta applies. A PE or VC fund sits
between the two: use that fund's own portfolio correlation with the market, not a
single-asset holder's.

---

## holdings_share, business_count, option_candidates

**holdings_share.** Value of stakes in other firms divided by total estimated value. Flag
above roughly one third. Above that line the error bars live in the holdings rather than in
the DCF, and B11 becomes the main event.

**business_count.** Reportable segments with distinct economics *and* separable, traceable
cash flows. Two segments that share a brand, a sales force and a plant are one business for
routing purposes. Run the B10 feasibility test before setting this above 1.

**option_candidates.** List each with an exclusivity note. Patents, undeveloped reserves,
exclusive licences, contractual exit rights, expansion rights, excess debt capacity. The
note matters more than the list, because most candidates fail the B12 exclusivity test and
are worth nothing.

---

## macro_driver

**Computation.** Regress revenues on the candidate commodity or cycle price over as long a
history as available. Report the R² and the sample period.

A high R² sends the firm to B6, because the price essentially is the revenue model. No
usable price series sends a cyclical firm to B7 instead. Report the R² in the artifact
either way, because it is the evidence for the branch.

---

## transaction_motive

Read from `mandate.json`. It is one of valuation, acquisition, restructuring, ipo, project
or corporate-finance. This is the only signal that does not come from the company. It
drives the S4 gate and, through R8, what runs after the engine.
