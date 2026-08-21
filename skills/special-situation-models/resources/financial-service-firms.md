# Valuing banks and insurers

## Why the standard machinery is off the table

For an industrial company, debt is a source of capital. You can separate the operating
decision from the financing decision, value the operating assets from free cash flow to
the firm, and discount at a weighted average cost of capital.

For a bank, debt is raw material. Deposits and borrowings are the inputs the business
transforms into loans and securities. There is no clean line between operating and
financing, so free cash flow to the firm has no meaning and neither does a cost of
capital. Value the equity directly.

Three consequences follow, and each rules out a piece of standard practice.

**No FCFF valuation.** Do not run `dcf-valuation-engine value` on a bank. Firm value is
not a number you can compute here, and the equity bridge that subtracts debt from firm
value is subtracting the raw material from the product.

**No optimal debt ratio.** Do not run `cost-of-capital-toolkit debt-schedule` on a bank.
The financing mix is not a choice management optimises against a tax shield. Regulatory
capital ratios set it, and a bank that breaches its ratio can be taken over and closed
however good its earnings look.

**No clean free cash flow to equity either, at first glance.** Capital expenditure and
working capital have no clean definition at a bank. What a bank does have is a hard
definition of reinvestment that industrial firms lack: it reinvests by adding to book
equity, and the regulator sets how much it must add.

## Choosing among the three equity models

| Model | When it fits | What it needs |
|---|---|---|
| Dividend discount | A stable bank paying out roughly what it can afford | Base earnings per share, payout, sustainable return on equity, growth |
| Excess return on equity | Payout does not reflect capacity, or you want value split into book equity and franchise | Book equity, return-on-equity path, cost-of-equity path |
| FCFE against regulatory capital | Capital ratios are moving, or the bank is in crisis | Risk-adjusted assets, the capital ratio path, the return-on-equity path |

The `excess-return` subcommand covers the second and third. Set
`reinvestment: "retention"` for the excess return model and
`reinvestment: "regulatory_capital"` for the crisis model. Both report the same value two
ways, once as book equity plus present value of excess returns and once as discounted free
cash flow to equity. Residual income and discounted cash flow are the same model written
differently, so a gap between the two routes means the book-equity rollforward disagrees
with the cash flows.

The dividend discount model is not scripted here. It is a two-stage earnings-per-share
model with a payout path, and it fits in a spreadsheet. What matters is the input, not the
arithmetic: use a **sustainable** return on equity, not the trailing one.

## The sustainable return on equity

This is the judgment the whole valuation turns on.

A trailing return on equity earned on a capital base the regulator is about to enlarge
will not survive re-regulation. The correction is a haircut:

    adjusted return on equity = trailing return on equity / (1 + required increase in capital)

Wells Fargo in October 2008 had earned 17.56% on equity. Regulators were about to demand
roughly 30% more capital, so the sustainable figure was 0.1756 / 1.3 = 13.5%. That cut
expected growth from about 8% to 6.13%, and it moved the verdict from cheap to roughly
fairly priced.

Anchor the terminal return on equity on the cost of equity unless the bank has a durable
franchise. Setting them equal forces excess returns to zero in perpetuity, which is what
competition eventually does.

Anchor the target capital ratio on the peer distribution rather than on the regulatory
minimum. Deutsche Bank's October 2016 target of 15.67% was the 75th percentile of all
banks, because the market, not just the regulator, was setting the bar.

## Payout and return on equity move together

The stable payout ratio is not a free input:

    stable payout = 1 − stable growth / stable return on equity

A high-return bank that lets its return on equity fall toward the cost of equity has to
pay out more, not the same. Holding the high-growth payout constant while the return
falls is internally inconsistent, and the script derives the stable payout from this
identity unless you override it.

Setting the stable return on equity below stable growth makes the payout negative, which
means retaining more than all earnings. The script refuses that combination rather than
carrying it mechanically the way the spreadsheet does.

## Regulatory capital as reinvestment

```
required book equity     = risk-adjusted assets × capital ratio, year by year
investment in capital    = required equity this year − required equity last year
net income               = beginning book equity × return on equity
free cash flow to equity = net income − investment in capital
```

A rising capital ratio is not free. Every increase is reinvestment and it comes straight
out of cash flow to shareholders. For a bank rebuilding capital, free cash flow to equity
is deeply negative in the early years, and that is the correct answer rather than a sign
of an error.

Subtract one-off hits to capital before the forecast starts. Deutsche Bank carried an
expected ten billion dollar Department of Justice fine, entered as
`one_off_capital_hit`.

## The wipeout overlay

A bailout can save the bank and still destroy the equity. General Motors in 2009 is the
reference case. The probability that matters to a shareholder is the probability of an
equity wipeout, not the probability of liquidation.

Set `probability_of_equity_wipeout` to apply it. Damodaran used 10% for Deutsche Bank in
October 2016, taking the value from $22.97 to $20.67 per share against a market price of
$13.33.

## Worked example: the excess return model end to end

Inputs: current book equity 17,997; prior-year book equity 15,518; net income 4,791;
earnings per share 4.75; dividends per share 0.92; 1,120.713 shares; beta 1.15; riskfree
rate 5%; premium 4%.

The fundamental return on equity is 4,791 / 15,518 = 30.87%, computed on **prior-year**
book equity. That is not sustainable, so the high-growth return is overridden to 25%. The
fundamental retention ratio is 1 − 0.92 / 4.75 = 80.63%. Stable return on equity is 15%,
stable growth 5%, stable beta 1.1, so the stable cost of equity is 9.4% and the stable
payout is 1 − 5 / 15 = 66.67%.

Year 1: net income is 0.25 × 17,997 = 4,499.25. The equity charge is 0.096 × 17,997 =
1,727.71. The excess return is 2,771.54, and its present value is 2,528.78.

Year 10 ends with book equity of 73,370.15. The terminal excess return is 4,108.73, so the
terminal value is 4,108.73 / (0.094 − 0.05) = 93,380.20. Present values sum to 65,993.76.

    value of equity = 17,997 + 65,993.76 = 83,990.76
    value per share = 83,990.76 / 1,120.713 = 74.94

The split is worth reading. Book equity is 21% of the answer and the franchise is the rest.

## Pitfalls

- Building a firm valuation for a bank, or running an optimal debt ratio on one.
- Using the trailing return on equity when the regulator is about to demand more capital.
- Treating a rising capital ratio as free.
- Letting the payout stay high while the return on equity falls toward the cost of equity.
- Using the crisis-depressed return on equity as the terminal return.
- Ignoring preferred stock, which is significant for financial firms and ranks ahead of
  common equity.
- Mixing a dollar cost of equity with local-currency earnings for an emerging-market bank.
  Convert the rate with `cost-of-capital-toolkit convert-rate`.
- Skipping the wipeout probability for a bank in genuine crisis.

## Sources

Damodaran, Valuation lecture packet 1, Spring 2020 and Spring 2021: financial service firm
valuation, bank FCFE and excess return models. Spreadsheet model `eqexret.xls`. Cases:
Wells Fargo October 2008, Commercial International Bank Egypt December 2015, Deutsche Bank
October 2016.
