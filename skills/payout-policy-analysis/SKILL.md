---
name: payout-policy-analysis
description: Assesses whether a company returns the right amount of cash to shareholders. Computes FCFE over a history under three debt assumptions, compares it against dividends plus buybacks to give the cash surplus or deficit, places the firm in the dividend matrix of affordability against project quality, projects forward FCFE and buyback capacity, and benchmarks payout ratio and dividend yield against peers and the market. Handles bank FCFE from regulatory capital. Use for dividend policy, payout ratio, dividend yield, potential dividends, FCFE, cash returned, buybacks, share repurchase capacity, excess cash, dividend cut or increase, cash accumulator or overpayer, or the dividend matrix.
---

# Payout policy analysis

Three questions, in order. How much cash did the firm return? How much could it have
returned? And do you trust management with the difference?

The first two are arithmetic and the script does them. The third is the judgment the whole
analysis exists to support, and the script only scores the evidence for it.

The single most common error in this work is looking at dividends alone. Buybacks are
roughly 60% of cash returned in the US. A firm with a 19% dividend payout ratio can be
returning 83% of its earnings, and a firm with an 18% payout ratio can be unable to afford
it. Add buybacks on both sides of every comparison before drawing a conclusion.

## The script

`resources/payout.py` — pure standard library, no installation needed. Every subcommand
takes JSON on stdin (or `--in FILE`) and prints JSON.

```bash
python3 resources/payout.py <subcommand> --example    # show input shape
python3 resources/payout.py <subcommand> --in payload.json
python3 resources/payout.py selftest                  # verify the engine
```

| Subcommand | Turns this | Into this |
|---|---|---|
| `fcfe-history` | 1–10 years of statements, a debt ratio | FCFE in three variants against cash returned, surplus or deficit, payout ratios |
| `trust` | net income, book equity, stock and market returns, beta | annual ROE, required return, Jensen's alpha, and the project-quality verdict |
| `matrix` | FCFE, cash returned, ROE, cost of equity | the dividend matrix quadrant and its prescription |
| `sustainability` | base year and growth rates | projected FCFE, expected dividends, buyback capacity, the sustainable dividend growth ceiling |
| `peers` | a firm and its comparables | yield, payout and cash-return statistics, and where the firm sits |
| `market-norms` | beta, expected growth, debt ratio | the payout and yield the market's cross-section predicts |
| `bank-fcfe` | regulatory capital projections | FCFE for a bank or insurer |

The bundled examples are Damodaran's own cases, so `--example | <subcommand>` reproduces
his worked numbers. Run `selftest` after editing anything.

## Work it in this order

```
Payout analysis progress:
- [ ] 1. Measure what was actually returned, dividends plus buybacks
- [ ] 2. Compute FCFE over 5 years, all three variants
- [ ] 3. Score the trust evidence
- [ ] 4. Read the matrix quadrant
- [ ] 5. Project forward and test sustainability
- [ ] 6. Cross-check against peers and the market
```

### 1. What was returned

Pull dividends paid on common stock and stock repurchases from the financing section of the
cash flow statement, for each of the last five years. Report the split as well as the
total, because the split tells you whether management deliberately kept flexibility.

Net buybacks against equity issuance where stock compensation is large. Gross repurchases
at such a firm partly offset dilution rather than returning cash to anyone.

### 2. FCFE, in three variants

```bash
python3 resources/payout.py fcfe-history --in disney.json
```

Each year needs `net_income`, `depreciation`, `capex` (including acquisitions),
`change_in_noncash_wc`, `net_debt_issued`, `dividends` and `buybacks`, most recent first.
Add `preferred_dividends` where they exist.

The three variants differ only in how reinvestment is assumed to be financed:

```
Reinvestment       = (Cap Ex − Depreciation) + ΔNon-cash Working Capital
FCFE (pre-debt)    = Net Income − Reinvestment
FCFE (actual debt) = FCFE (pre-debt) + Net Debt Issued
FCFE (target DR)   = Net Income − Reinvestment × (1 − DR)
```

**Lead with the target-debt-ratio variant.** Actual-debt FCFE counts one-off borrowing as
payout capacity, which flatters an acquisitive, debt-funded firm. Tata Motors returned 9%
of actual-debt FCFE and 157% of target-ratio FCFE over the same five years. Only the second
number is sustainable capacity.

Use the actual-debt variant when debt policy is stable and deliberate. Say which one your
conclusion rests on. The engine sets `variants_agree` to false when the three disagree on
whether the firm is an accumulator or an overpayer, and that disagreement is itself a
finding worth reporting.

**Setting the debt ratio.** Use the current market debt-to-capital ratio unless you are
deliberately moving the firm to a target. If you use a target, use the same one in the
forward projection, and say you changed it. Get the market value of debt from
`cost-of-capital-toolkit`'s `mv-debt`.

**Five years, not one.** A single year is dominated by lumpy cap ex and borrowing. The
engine accepts one to ten years and refuses anything outside that.

Read the output at `comparison`. Each variant carries the aggregate FCFE, the surplus or
deficit in currency, cash returned as a percentage of FCFE, and an accumulator or overpayer
label. Where FCFE is negative the percentage is reported as null with a reason, because a
negative denominator makes it meaningless. Read the surplus in currency instead.

### 3. The trust evidence

```bash
python3 resources/payout.py trust --in disney-returns.json
```

Trust is not a feeling. It is measured two ways, and they disagree often enough that
reporting one alone is a mistake.

```
ROE_t             = Net Income_t / Book Equity_t
Required Return_t = Rf_t + β × (Rm_t − Rf_t)
Excess ROE_t      = ROE_t − Required Return_t
Jensen's alpha_t  = Stock Return_t − Required Return_t
```

The project measure asks whether the investments earned their cost of equity. The market
measure asks whether the stock beat the same bar. Disney over the five years to 2013 shows
average ROE of 3.02% against an average required return of 11.22%, yet the stock beat its
required return by 6.42% a year. On the accounting measure management destroyed value; on
the market measure it created value.

When they conflict, weight the project measure for the payout decision. A rising market
lifts alpha at firms whose managers did nothing well. Say which measure you relied on.

Two cautions on the inputs. Book equity is distorted by buybacks, write-offs and
acquisition accounting, so a low ROE at an acquisitive firm may be an artifact. And use each
year's own risk-free rate and market return, not a single long-run average.

`average_roe_method` defaults to `ratio_of_sums`; `mean_of_annual` is the alternative and
both are always reported. Damodaran's dividends.xls averages ROE over all ten input rows
regardless of the selected window, unlike every other statistic in the sheet. Supply
`extra_years_for_legacy_roe` to reproduce that figure when you need to tie out to the
sheet, and report the corrected number.

### 4. The matrix

```bash
echo '{"fcfe": 18064.5, "cash_returned": 19869, "roe": 0.0302,
       "cost_of_equity": 0.1122}' | python3 resources/payout.py matrix
```

Two axes. Can the firm afford its payout, measured by cash returned against FCFE? And does
it earn its cost of capital, measured by ROE against the cost of equity?

| | **Poor projects** (ROE < cost of equity) | **Good projects** (ROE > cost of equity) |
|---|---|---|
| **Cash surplus** (returned < FCFE) | Pay out more, as dividends or buybacks | Maximum flexibility: keep the cash and invest |
| **Cash deficit** (returned > FCFE) | Cut the payout, and fix the investing first | Reduce the payout so projects are funded internally |

The insight the matrix protects is that in two quadrants the dividend is not the problem.
Recommending a dividend cut in the deficit and poor-projects quadrant, and stopping there,
leaves the value destruction untouched. BP cut its dividend by 55% **and** restructured.

Sequencing matters in the deficit column. With poor projects, fix the investment policy
first and then cut. With good projects, reduce the payout so the firm can fund itself
rather than issuing equity at a flotation cost.

Optional inputs sharpen the quality axis. Pass `roc` and `cost_of_capital` — Damodaran's
rule is that ROE above the cost of equity and/or ROC above the cost of capital counts as
good projects. Pass `jensens_alpha` as a cross-check. The engine flags
`quality_signals_disagree` when the signals point different ways.

**The trust question is the whole point of the surplus row.** A firm with poor returns and
a large cash balance should be paying out. Whether it must depends on whether management
can be trusted to invest well from here, and that is a judgment about people and
governance, not a number. Look at management continuity — Disney's 2003 problem was that
the CEO who championed the Capital Cities deal was still in the chair. Ask where the excess
returns came from and whether that source persists. Ask whether the board is capable of
saying no. Microsoft built a $43bn cash pile by 2002 and shareholders were content, because
the project record had earned that trust; Chrysler built an $8bn pile and drew an activist
campaign. The arithmetic is identical in both cases. The verdict is not.

State the FCFE variant with the quadrant. The quadrant can change with the variant, and
Disney's does.

### 5. Sustainability

```bash
python3 resources/payout.py sustainability --in forecast.json
```

Assessing the past is half the job. The forward half projects FCFE for five years, projects
the dividend the firm will keep paying given stickiness, and takes the difference as
repurchase capacity.

```
ΔWorking Capital_t = WC% × (Revenues_t − Revenues_(t−1))
FCFE_t             = Net Income_t − (Cap Ex_t − Depreciation_t)(1 − DR) − ΔWC_t (1 − DR)
Buyback capacity_t = FCFE_t − Expected Dividends_t
```

Working capital reinvestment is driven by the revenue **increment**, not the level.
Multiplying the level by the percentage gives the balance and overstates reinvestment by an
order of magnitude. The engine does this correctly; check any hand-built model against it.

Growth rates arrive as decimals. The engine rejects anything above 1.0 with an explanation,
because entering 5 for 5% is the most common input error here.

Be realistic about the dividend growth rate. Stickiness means the dividend keeps growing at
roughly its historical rate unless management commits otherwise. If that produces negative
buyback capacity, that is the finding. Do not quietly lower the growth assumption to make
the output look better.

Read three fields:

- `dividend_sustainable` and `first_shortfall_year` — whether the path holds, and when it
  breaks.
- `max_sustainable_dividend_growth` — the fastest dividend growth this FCFE path covers in
  every forecast year. It is the ceiling on what management can promise.
- `total_buyback_capacity` — the repurchase programme the firm can fund without new
  leverage or asset sales.

**A payout that cannot be sustained is worse than a lower one.** Cuts are read as
confessions of failure and are punished accordingly, at roughly −5% to −8% on announcement.
Stickiness means firms delay cuts, so an unaffordable dividend can persist for years before
a brutal forced cut. Recommending an increase the firm cannot fund in a bad year does real
damage. Prefer a buyback for any increase that may not repeat: it returns the same cash
with no commitment attached. See
[resources/methodology.md](resources/methodology.md) for the framing evidence on cuts and
the constraints — clientele, contractual, regulatory — on executing one.

### 6. Peers and the market

```bash
python3 resources/payout.py peers --in entertainment.json
python3 resources/payout.py market-norms --in disney-2014.json
```

`peers` computes dividend yield, dividend payout, cash payout ratio and cash return as a
percentage of FCFE for every company, then the group average and median, then the firm's
gap and percentile. Averages and medians run over the companies where the metric is
defined. A payout ratio on a loss-maker and a cash-return ratio on negative FCFE are both
reported as null. Counting them as zero drags both statistics down and is the standard way
this table gets misread.

Report the average and the median together. In sectors where most firms pay nothing the
median is zero and the average reflects two or three large payers, and that divergence is
the finding. The engine warns when the median peer pays nothing, when the group returns
more through buybacks than dividends, and when the group's own average FCFE is negative.

That last warning matters most. US Entertainment in 2013 had average FCFE of −$232M, so
most of the group could not afford any payout. "Match the peer group" was a meaningless
recommendation. Peer comparison is a cross-check on the FCFE analysis, never a substitute.
Where the two disagree, the FCFE analysis wins.

`market-norms` runs the January 2014 US cross-sectional regressions, which predict payout
and yield from beta, expected growth and the debt ratio. Lower beta, lower growth and
higher leverage all predict higher payout. R-squared runs 20–26%, so treat the prediction
as a central tendency and ignore gaps of a few percentage points.

The regressions are fitted on dividends alone. Pass `dividends`, `buybacks`, `net_income`
and `market_cap` and the engine returns the buyback-inclusive overlay beside the
prediction. Disney in 2014 showed a negative payout gap against the regression while
returning 360% of its FCFE. Never act on the gap without that overlay.

## Banks and insurers

The standard formula produces nonsense for a bank. Cap ex and non-cash working capital are
meaningless at a firm whose raw material is capital, and debt is part of the product rather
than a financing choice. Reinvestment is the increase in **regulatory capital** needed to
support a larger balance sheet.

```
FCFE (bank) = Net Income − Investment in Regulatory Capital
Investment  = Risk-Adjusted Assets_t × Tier 1 Ratio_t − Tier 1 Capital_(t−1)
```

```bash
python3 resources/payout.py bank-fcfe --example | python3 resources/payout.py bank-fcfe
```

The projection mode ramps the Tier 1 ratio and the ROE linearly from current levels to
targets, grows risk-adjusted assets at `asset_growth`, and rolls book equity forward by the
capital retained. Pass `tier1_ratio_path` or `roe_path` explicitly to override either ramp.
The simple mode takes `old_loans`, `new_loans`, `capital_ratio` and `net_income` when that
is all you have.

Two things decide the answer, and both are assumptions. The speed of the ratio ramp is
often a larger reinvestment than the asset growth itself. And for a troubled bank the ROE
recovery path dominates everything. State both and defend them.

Do not read a bank's reported dividend as evidence of capacity. Banks paid dividends with
deeply negative FCFE widely before 2008, and Deutsche Bank's projected FCFE was negative for
three straight years while the market still expected a payout.

## Reference data

`resources/data/payout_benchmarks.json` (`as_of: 2020-01`) holds regional cash-return and
yield tables, the accumulator and overpayer base rates by region, the payout distribution
among payers, life-cycle payout benchmarks by expected growth, the dividend-cut
announcement returns, and the equity flotation cost bands.

`resources/data/payout_regressions.json` (`as_of: 2014-01`) holds the US payout and yield
regressions with coefficients, t-statistics and R-squared.

Both carry a `refresh` note. Buyback intensity in particular has moved since 2020. Check
the vintage, refresh from Damodaran's site if it is stale, and record which vintage the
analysis used. Pass a refreshed file with `benchmarks_path` or `regressions_path` rather
than editing the bundled copy.

## Handoffs to the other engines

| Need | Engine | Subcommand and field |
|---|---|---|
| Cost of equity for the quality axis | `cost-of-capital-toolkit` | `wacc` → `cost_of_equity` |
| Market value of debt for the debt ratio | `cost-of-capital-toolkit` | `mv-debt` → `market_value_of_debt` |
| FCFE cross-check on corrected statements | `financial-statement-normalization` | `cashflow` → `fcfe` |
| ROE and return on capital | `financial-statement-normalization` | `ratios`, `invested-capital` |
| Normalized earnings for a cyclical base year | `financial-statement-normalization` | `normalize-earnings` |
| Value effect of a repurchase, and the EPS trap | `option-valuation-toolkit`, `dcf-valuation-engine` | dilution-adjusted share count, equity bridge |
| Reinvestment consistency against a valuation | `dcf-valuation-engine` | `value` → forecast reinvestment |
| Cross-artifact consistency gate | `valuation-consistency-checks` | `validate` |

Capitalize leases and research spending before computing FCFE. Both change cap ex,
depreciation and debt, and therefore change every number in this analysis.

## Common failures

| Symptom | Cause |
|---|---|
| A firm with a 19% payout ratio looks like a cash hoarder | Dividends counted without buybacks |
| Cash returned looks trivially affordable at an acquisitive firm | Actual-debt FCFE used where target-ratio FCFE belongs |
| Pre-debt FCFE is deeply negative for no obvious reason | Acquisitions correctly inside cap ex; use the target-ratio variant |
| Cash as a percentage of FCFE comes back negative | Negative FCFE denominator; the engine returns null, so read the surplus in currency |
| Payout ratio explodes or flips sign | Net income at or below zero; the ratio is meaningless and is reported as null |
| Peer group average is wildly higher than the median | Most peers pay nothing; read the median |
| Peer benchmark suggests raising the payout at a firm already overpaying | Group FCFE is negative; the group cannot afford its own payout |
| Regression says the firm pays too little, FCFE says it overpays | Regression is dividend-only; apply the buyback overlay |
| Projected reinvestment is an order of magnitude too large | Working capital taken as a percentage of the revenue level, not the increment |
| Forecast output is absurd | Growth rates entered as percentages rather than decimals |
| Bank FCFE looks healthy while the bank is in trouble | Standard cap-ex formula applied; use `bank-fcfe` |
| Bank capital build looks too small | Current Tier 1 ratio used while regulators are forcing it up |
| The quadrant changes between two drafts | A different FCFE variant, or a different debt ratio, was used |
| Average ROE does not tie out to dividends.xls | The sheet averages ROE over all ten input rows; see `extra_years_for_legacy_roe` |
