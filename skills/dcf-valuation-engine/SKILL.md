---
name: dcf-valuation-engine
description: Runs an intrinsic (discounted cash flow) valuation from value drivers — builds the year-by-year forecast with fading growth, margins and reinvestment, closes it with a terminal value, adjusts for failure risk, walks the bridge from operating assets to equity value per share, and runs sensitivity grids. Also reverse-engineers the market price into the growth or margin it already assumes. Use when valuing a company intrinsically, building a DCF or FCFF/FCFE model, computing terminal value or value per share, running valuation sensitivity, or asking what the market is pricing in.
---

# DCF valuation engine

A discounted cash flow valuation is four judgments and a lot of arithmetic. The judgments
are how fast revenue grows, what margin it eventually earns, how much capital that growth
costs, and how risky the whole thing is. The arithmetic is here, so you can spend your
effort on the four numbers that actually decide the answer.

The engine never invents a driver. Every growth rate, margin and reinvestment assumption
arrives as an input you chose and can defend.

## The script

`resources/dcf.py` — pure standard library, no installation needed. JSON on stdin (or
`--in FILE`), JSON out.

```bash
python3 resources/dcf.py value --example        # show the input shape
python3 resources/dcf.py value --in drivers.json
python3 resources/dcf.py selftest               # verify the engine
```

| Subcommand | Purpose |
|---|---|
| `value` | drivers → forecast, terminal value, equity bridge, value per share |
| `sensitivity` | re-run across a grid of one or two drivers |
| `implied` | solve for the driver that makes the DCF equal the market price |

## The input

Three ways to state a driver, so a fading assumption stays one line:

- a number — constant every year: `"tax_rate": 0.25`
- a list — one entry per year: `"revenue_growth": [0.4, 0.3, 0.2, 0.1, 0.05]`
- a glide — `{"start": 0.40, "end": 0.03, "converge_by": 8}` moves linearly from start to
  end by year 8, then holds

A glide is usually what you want for growth, margin and cost of capital. Real companies
converge toward their industry; a company growing 40% in year 1 and 40% in year 10 is
almost always a modelling error rather than a forecast.

```json
{
  "base_revenue": 10000, "base_ebit": 800, "base_invested_capital": 6000,
  "forecast_years": 10,
  "revenue_growth": {"start": 0.25, "end": 0.03, "converge_by": 10},
  "operating_margin": {"start": 0.08, "end": 0.15, "converge_by": 7},
  "sales_to_capital": 2.0,
  "tax_rate": {"start": 0.15, "end": 0.25, "converge_by": 10},
  "cost_of_capital": {"start": 0.09, "end": 0.075, "converge_by": 10},
  "terminal": {"growth_rate": 0.025, "cost_of_capital": 0.075, "return_on_capital": 0.10},
  "bridge": {"debt": 3000, "cash": 1200, "minority_interests": 0,
             "non_operating_assets": 0, "employee_options_value": 0,
             "shares_outstanding": 500, "current_price": 42.00},
  "currency": "USD"
}
```

Set `currency` to the same currency as the cost of capital. The consistency validator
checks this and it is the single most common silent error in DCF work.

## How the engine computes each year

Revenue grows at the stated rate. Operating income is revenue times the margin. Tax
applies to operating income, with any loss carryforward absorbing income first. Then the
part people skip:

    reinvestment = (this year's revenue − last year's revenue) / sales-to-capital
    FCFF = after-tax operating income − reinvestment

Growth is not free. The sales-to-capital ratio says how many dollars of revenue each
dollar of capital buys, so it converts a growth assumption into the investment that growth
requires. A model that grows revenue without reinvesting is manufacturing value out of
nothing, and it is the most common way a DCF ends up too high.

Set `net_operating_loss_carryforward` when the company has accumulated losses. The engine
shelters income until the carryforward is used up.

## Terminal value

Beyond the forecast horizon the company becomes a perpetuity:

    terminal value = terminal FCFF / (terminal cost of capital − terminal growth)

Three rules the engine enforces by refusing to run:

1. **Terminal growth cannot exceed the riskfree rate.** A company growing faster than the
   economy forever eventually becomes the economy. The riskfree rate is the practical
   ceiling because it already contains expected inflation plus real growth.
2. **Terminal cost of capital must exceed terminal growth**, or the formula does not
   produce a finite number.
3. **Terminal growth must be paid for**: `reinvestment rate = growth / return on capital`.
   The engine computes this rather than accepting it, and refuses a combination that would
   require reinvesting more than 100% of income.

Set `terminal.return_on_capital` deliberately. Setting it equal to the cost of capital says
competition eventually arrives — the honest default. Setting it higher says this company
holds a barrier to entry forever, which needs naming.

## Failure risk

A going-concern DCF prices only the branch where the company survives. For a young company
or a distressed one, that overstates value:

```json
"failure": {"probability": 0.20, "proceeds_basis": "book_value",
            "book_value_of_capital": 4000, "proceeds_percent": 0.5}
```

    value = going-concern value × (1 − p) + distress proceeds × p

Use `book_value` as the basis when a failed firm would be liquidated piecemeal, and
`going_concern` when it would be sold intact at a discount.

## The bridge

Operating assets are not equity. The walk:

    equity value = operating assets − debt − minority interests + cash + non-operating assets
    equity in common = equity value − value of employee options
    value per share = equity in common / shares outstanding

Value employee options properly with `option-valuation-toolkit` and pass the result in.
Inflating the share count instead understates the cost of options; ignoring them
overstates value per share.

Do not add a control premium here and do not divide by diluted shares if you already
subtracted option value — that double-counts.

## Sensitivity and reverse engineering

A point estimate implies a false precision. Show a range.

```bash
python3 resources/dcf.py sensitivity --in grid.json
```

Point `axes` at any leaf with a dotted path — `terminal.growth_rate`,
`operating_margin.end`, `cost_of_capital` — and give the values to sweep. Sweep the drivers
that actually move the answer, which for most companies are the target margin and the
terminal assumptions rather than near-term growth.

The `implied` subcommand runs the valuation backwards: given the market price, what must be
true for that price to be right?

```bash
echo '{"base_case": {...}, "path": "operating_margin.end",
       "target_value_per_share": 42.00, "low": 0.01, "high": 0.40}' \
  | python3 resources/dcf.py implied
```

This is often the most useful output in the whole analysis. "The stock is worth $31 and
trades at $42" invites an argument about your assumptions. "At $42 the market assumes this
company reaches a 22% operating margin, which no firm in the industry has ever sustained"
is a claim about the world, and it is checkable.

## Choosing the model

This engine values the **firm** from operating cash flows (FCFF), discounted at the cost of
capital. That is the right default for most non-financial companies, and the only sensible
choice when leverage is changing.

Use something else when:

| Situation | Use instead |
|---|---|
| Financial service firm | Dividends or excess return, valuing equity directly — debt is raw material for a bank, so there is no meaningful cost of capital. Use `special-situation-models` |
| Stable leverage, equity question | FCFE discounted at the cost of equity |
| Mature dividend payer that pays out what it can | Dividend discount model |
| Negative earnings, no path to profit modelled | Revenue-driven build with failure probability. Use `special-situation-models` |
| Deeply distressed, equity is an option | Equity as a call. Use `option-valuation-toolkit` |

## Before accepting the answer

Run the validator in `valuation-consistency-checks`. Then read the output for these
tells:

- **Terminal value above 90% of total value.** The forecast horizon is too short, or the
  company is genuinely all-option and a DCF is the wrong tool.
- **ROIC climbing every year with no explanation.** Check that reinvestment is keeping up.
- **Value per share wildly different from price.** Usually the model, not the market. Run
  `implied` and see whether the market's assumption is defensible before concluding the
  market is wrong.
- **Margins that never converge.** Very few businesses out-earn their industry forever.

## Common failures

| Symptom | Cause |
|---|---|
| Value far too high | Growth without matching reinvestment; sales-to-capital set too high |
| Terminal value is most of the answer | Forecast horizon too short for a company still growing fast |
| Value changes when currency changes | Cash flows and discount rate in different currencies |
| Engine refuses to run | Terminal growth above the discount rate, or reinvestment above 100% — both are real errors, not obstacles |
| Value per share negative | Debt exceeds operating asset value; the company may be a distress case needing the option approach |
| Young company looks worth billions | No failure probability applied |
