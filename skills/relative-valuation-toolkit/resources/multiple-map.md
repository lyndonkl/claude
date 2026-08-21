# The multiple map: definitions, claimholders and intrinsic forms

Reference for steps 1 and 3 of the four-step framework. Step 1 settles what the multiple
is. Step 3 recovers it from a discounted cash flow model so you know what to control for.

## Numerators

| Numerator | Formula | Prices |
|---|---|---|
| Market value of equity | price per share x shares outstanding | the equity claim only |
| Firm value | equity + market value of debt | all claims, including cash |
| Enterprise value | equity + debt - cash + minority interests | the operating assets only |

Cash leaves the enterprise numerator because interest income on cash appears in neither
EBITDA nor EBIT. Leaving it in prices an asset whose income the denominator excludes.

Minority interests come back in because a consolidated but partly owned subsidiary puts
all of its EBITDA in the denominator while the parent owns only part of the equity.

The script builds all three from `market_cap` (or `price_per_share` and
`shares_outstanding`), `debt`, `cash` and `minority_interests`. Use the **market** value
of debt, which `cost-of-capital-toolkit` produces with `mv-debt` — read
`market_value_of_debt` from its output.

## Denominators and their claimholders

| Denominator | Belongs to | Field name |
|---|---|---|
| Net income, EPS | equity | `net_income`, `eps` |
| Book value of equity | equity | `book_equity`, `book_value_per_share` |
| Dividends, FCFE | equity | `dividends`, `fcfe` |
| EBITDA, EBIT, after-tax EBIT | all capital providers | `ebitda`, `ebit`, `after_tax_ebit` |
| FCFF | all capital providers | `fcff` |
| Invested capital | all capital providers | `invested_capital` |
| Revenue | above the capital structure | `revenue` |

`financial-statement-normalization` produces most of these on a lease- and
research-adjusted basis. Its `fcff` subcommand returns `fcff` and `invested_capital`;
its `normalize` subcommand returns adjusted `ebit` and `ebitda`. Use the adjusted figures
for every firm in the comparable set, or none of them.

## The consistency rule

An equity numerator takes an equity denominator. A firm or enterprise numerator takes an
operating denominator. The script refuses the mismatches rather than computing them:

- **EV/Net Income** divides all of the value by part of the income.
- **Price/EBITDA** divides part of the value by all of the income.
- **Price/EBIT**, **Price/FCFF** and **EV/Book Equity** fail for the same reason.

Revenue is the exception by convention. It pairs with either numerator, on the condition
that the companion margin switches with it: net margin with a price numerator, after-tax
operating margin with an enterprise numerator.

## Timing and share-count variants

The same name covers several different numbers. Pick one and hold it across every firm.

- **Current PE** uses last fiscal year EPS. **Trailing PE** uses the trailing twelve
  months. **Forward PE** uses next year's forecast. Their US medians in January 2021 were
  18.15, 20.30 and 18.89 — close enough that mixing them looks harmless and far enough
  apart to change a ranking.
- **Primary EPS** ignores options. **Fully diluted** counts all of them. **Partially
  diluted** counts the in-the-money ones. None is right. Value the options separately with
  `option-valuation-toolkit` when they are material, and use fully diluted otherwise.

## The master map of intrinsic multiples

All in stable growth. Subscript 1 means next year.

**Equity side** — start from `P = Net Income x (1 - reinvestment) / (ke - g)`.

| Multiple | Intrinsic form | Companion variable |
|---|---|---|
| P/Dividends | `1/(ke - g)` | cost of equity, growth |
| PE (trailing) | `payout x (1 + g)/(ke - g)` | expected growth |
| PE (forward) | `payout/(ke - g)` | expected growth |
| PBV | `ROE x payout x (1 + g)/(ke - g)` | return on equity |
| PBV (short form) | `(ROE - g)/(ke - g)` | return on equity |
| P/Sales | `net margin x payout/(ke - g)` | net margin |

**Enterprise side** — start from `EV = EBIT(1 - t)(1 - RIR)/(WACC - g)`.

| Multiple | Intrinsic form | Companion variable |
|---|---|---|
| EV/FCFF | `1/(WACC - g)` | cost of capital, growth |
| EV/EBIT | `(1 - t)(1 - RIR)/(WACC - g)` | reinvestment rate, tax rate |
| EV/after-tax EBIT | `(1 - RIR)/(WACC - g)` | reinvestment rate |
| EV/Sales | `ATOM x (1 - RIR)/(WACC - g)` | after-tax operating margin |
| EV/IC | `(ROIC - g)/(WACC - g)` | return on invested capital |
| EV/EBITDA | see below | reinvestment needs, tax rate |

EV/EBITDA breaks into four terms because EBITDA sits above tax, depreciation and capital
spending:

```
EV/EBITDA = (1 - t)/(WACC - g)
          + [depreciation/EBITDA x t]/(WACC - g)
          - [CapEx/EBITDA]/(WACC - g)
          - [change in working capital/EBITDA]/(WACC - g)
```

Symbols: `ke` cost of equity, `WACC` cost of capital, `g` stable growth, `t` tax rate,
`payout` dividends over net income, `RIR` reinvestment rate, `ATOM` after-tax operating
margin, `ROIC` after-tax return on invested capital, `IC` book equity plus book debt minus
cash.

## Internal consistency

Growth is not free and cannot be set independently:

```
equity side:      g = (1 - payout) x ROE
enterprise side:  g = RIR x ROIC
```

Break these and the intrinsic multiple describes a firm that cannot exist. The script's
`intrinsic` subcommand computes both the long and short PBV forms, reports the implied
sustainable growth, and flags the gap.

The corpus's standing example: ROE 15%, payout 40%, cost of equity 9%, growth 4%. The long
form gives PBV 1.25, the short form 2.20. Sustainable growth on those inputs is 9%, not 4%.
Neither answer is usable until the inputs are reconciled.

On a forward basis the two forms are the same expression once growth is sustainable. That
identity is one of the engine's self-tests.

## `intrinsic` payload fields

| `multiple` | `model` | Required fields |
|---|---|---|
| `PE` | `stable` | `payout`, `growth`, `cost_of_equity`, optional `basis` |
| `PE` | `two_stage` | `payout`, `growth`, `years`, `cost_of_equity`, `stable_payout`, `stable_growth` |
| `PEG` | either | as PE; growth must be positive |
| `PBV` | `stable` | `roe`, `growth`, `cost_of_equity`, optional `payout`, `basis` |
| `P/S` | `stable` | `net_margin`, `payout`, `growth`, `cost_of_equity` |
| `EV/IC` | `stable` | `roic`, `growth`, `wacc` |
| `EV/Sales` | `stable` | `after_tax_operating_margin`, `reinvestment_rate`, `growth`, `wacc` |
| `EV/EBIT` | `stable` | `tax_rate`, `reinvestment_rate`, `growth`, `wacc`, optional `after_tax` |
| `EV/EBITDA` | `stable` | `tax_rate`, `depreciation_over_ebitda`, `capex_over_ebitda`, `wc_change_over_ebitda`, `wacc`, `growth` |

`basis` is `trailing` or `forward` and decides whether the `(1 + g)` factor appears. Add
`actual_multiple` to any payload to get the gap between traded and justified.

Take `cost_of_equity` and `wacc` from `cost-of-capital-toolkit` (`wacc` subcommand, fields
`cost_of_equity` and `wacc`). Do not estimate them here.

## Worked examples the engine reproduces

- **Two-stage PE.** Growth 25% for five years at 20% payout, then 8% growth at 50% payout,
  cost of equity 11.5%. Intrinsic PE 28.75, intrinsic PEG 1.15.
- **PBV.** ROE 20.22%, cost of equity 9%, stable growth 4%. Justified PBV 3.24, against a
  traded 2.09.
- **EV/EBITDA.** Tax 36%, depreciation 20% of EBITDA, CapEx 30% of EBITDA, WACC 10%,
  growth 5%. Justified multiple 8.24. Raise CapEx to 50% of EBITDA and it falls to 4.24 —
  the same business, priced at half, purely on reinvestment.
