# Worked examples

Every case here is in the `selftest`, so a change that breaks one is caught immediately.
Payloads are trimmed to the fields that matter.

## Distress: the bond-implied probability

`distress.xls`, the stored case. An 8-year bond with a 12% coupon, a 5% riskfree rate, and
a market price of 653 per 1,000 of face.

```bash
echo '{"bond": {"coupon_rate": 0.12, "maturity_years": 8,
                "riskfree_rate": 0.05, "market_price": 653},
       "horizon_years": 10}' \
  | python3 resources/special.py distress
```

Annual probability 13.5317%. Five-year cumulative 51.66%. Ten-year cumulative 76.63%.

Check one year by hand. Year 1 promises 120, weighted by survival to 120 × 0.8646829 =
103.76, discounted to 103.76 / 1.05 = 98.82. Year 8 promises 1,120, weighted to 350.00,
discounted to 236.90. The present values sum to exactly 653.

## Distress: Las Vegas Sands, February 2009

Standard & Poor's rated the company B+, and historically 28.25% of B+ bonds defaulted
within ten years. The market said worse. A 6.375% coupon bond maturing in seven years
traded at $529 with a 3% riskfree rate.

The solved annual probability is 13.54%, so the ten-year cumulative probability is 76.66%
— nearly three times the rating-table number. In distress, expected proceeds of $2,769
million fell short of the face value of debt, so equity received nothing.

```
expected value per share = 8.12 × (1 − 0.7666) + 0.00 × 0.7666 = 1.90
```

Against a market price of $4.25, that is much closer than the unadjusted $8.12. The gap
between the rating-implied and the market-implied probability is information, not an error.

## Distress: JC Penney

Going-concern value of operating assets $4,841 million. The bond rating implied a 20%
chance of failure. Liquidation would recover 50% of book value, or $2,421 million.

```
4,841 × 0.80 + 2,421 × 0.20 = 4,357
```

## Distress: Boeing, March 2020

Too big to fail outright, but a bailout could wipe out equity as General Motors did in
2009. A 20% failure probability with a 50% loss to equity is a 10% haircut:

```
107,883 × (1 − 0.20 × 0.50) = 97,094.7,  a deduction of 10,788.3
```

Then subtract debt and minority interests of $28,580 million, add cash and non-operating
assets of $10,030 million, and divide by 566 shares. The answer is $138.77 per share
against a $127.68 price.

Note what this is not. It is not a higher discount rate, and it is not a cut to the cash
flows. Pick one channel for failure risk, and let it be the probability weight.

## Financial service: the equity excess return model

`eqexret.xls`, the stored case. Reproduced in full in
[financial-service-firms.md](financial-service-firms.md).

```bash
python3 resources/special.py excess-return --example \
  | python3 resources/special.py excess-return
```

Value of equity 83,990.76 against book equity of 17,997, so 74.94 per share.

## Financial service: Deutsche Bank, October 2016

The regulatory-capital route. Risk-adjusted assets of $445,570 million grow at 1%
inflation. The Tier 1 ratio rises from 12.41% to 15.67%, the seventy-fifth percentile of
all banks. Return on equity climbs from −13.70% to the 9.44% bank median.

Free cash flow to equity is −$11,663 million in year 1, because the bank has to rebuild
capital before it can pay anybody. It turns positive and reaches $6,352 million by year 10.
Equity is worth $31,839 million over 1,386 million shares, or $22.97 per share. A 10%
probability of a complete equity wipeout takes that to $20.67, against a price of $13.33.

One caution before trying to reproduce the per-share figure. The packet states the book
equity path separately from the Tier 1 ratio, and book equity sits well above Tier 1
capital: $64,609 million against $55,282 million. Multiplying risk-adjusted assets by the
Tier 1 ratio therefore gives a different capital path from the one in the case. Pass
`regulatory_capital.required_book_equity` as an explicit year-by-year list when you have
the disclosed path, and use the ratio route when you are projecting one.

## Private company: the restaurant

Comparable high-end specialty retailers have an average unlevered beta of 1.18 and an
average regression R-squared of 25%.

```bash
python3 resources/special.py private --example \
  | python3 resources/special.py private
```

Correlation 0.50, so the total unlevered beta is 2.36. Levered at a 14.33% debt-to-equity
ratio with a 40% tax rate, the total beta is 2.56 and the cost of equity is 14.50%. The
same business sold to a diversified public buyer carries a levered market beta of 1.28 and
a cost of equity of 9.38%.

The illiquidity discount on $520,990 of equity comes out at 25.00% flat, 28.75% by the
Silber route, and 12.88% by the bid-ask route.

## Private company: the spreadsheet defaults

`pvtdiscrate.xls`: an unlevered beta of 1.02, a correlation of 0.45, a 15% industry
debt-to-capital ratio and a 40% tax rate give a levered total beta of 2.5067. With a 6%
riskfree rate and a 5.5% premium, the cost of equity is 19.79%.

`liqdisc.xls`: revenues of $209 million and positive earnings give a Silber discount of
19.10% and a bid-ask discount of 11.78%.

## IPO: Twitter, October 2013

The pre-offering valuation, in $ millions. The DCF put the operating assets at 9,611 on a
beta of 1.40, a 6.15% equity risk premium and a cost of capital falling from 11.22% to 8%.
Everything below that line is the IPO bridge.

```bash
python3 resources/special.py ipo --example | python3 resources/special.py ipo
```

```
operating assets 9,611 + cash 375 + IPO proceeds 1,000 − debt 207 = equity 10,779
equity 10,779 − options and warrants 805 = common stock 9,974
```

The $1,000 million was added because the prospectus said the money would stay in the
company. Had the owners planned to withdraw half, only $500 million would have been added
and the value per share would have fallen by exactly 500 divided by the share count.

The share count is where the value goes. Common shares excluding restricted stock units and
options are 472.61 million. Adding 86 million restricted stock units and 14.791 million
shares owed to MoPub's holders takes the count past 573 million — a fifth of the value, and
the packet's own count is 574.44 million. Against that count, `9,974 / 574.44 = $17.36`.

The 44.16 million employee options are not in that count. Their $805 million of value came
out of the numerator instead. Doing both charges for them twice, and it is the standard
error in an IPO bridge.

Underpricing is a separate question. If investors would pay $20 billion for the whole
company and the issue is underpriced 15%, an owner floating 10% loses `0.15 × 0.10 ×
20,000 = $300 million`, not `0.15 × 20,000`. The loss falls only on the shares sold.

## IPO: the restaurant, private owner or public market

The same business as the private-company case above, now taken public. Nothing about the
cash flows changes. `163.04` of free cash flow to the firm next year, growing at 2%, with
$928.23 thousand of debt.

| | Private owner | Public market |
|---|---|---|
| Levered beta | 2.56 total | 1.28 market |
| Cost of equity | 14.50% | 9.38% |
| Cost of capital | 13.25% | 8.76% |
| Value of the business | 1,449.22 | 2,411.79 |
| Value of equity | 520.99 | 1,483.56 |
| Illiquidity discount | 12.88% | none |
| **Equity, final** | **453.88** | **1,483.56** |

Run it as a ladder and each line is priced separately:

```bash
echo '{"cost_of_equity": {"unlevered_market_beta": 1.18, "r_squared": 0.25,
                          "debt_equity_ratio": 0.1433, "tax_rate": 0.40,
                          "riskfree_rate": 0.0425, "equity_risk_premium": 0.04,
                          "pre_tax_cost_of_debt": 0.075},
       "revaluation": {"next_year_fcff": 163.04, "stable_growth": 0.02},
       "debt": 928.23, "illiquidity_discount": 0.1288,
       "pre_ipo_shares": 100, "shares": {"common_shares": 100},
       "offering_discount": 0.15}' \
  | python3 resources/special.py ipo
```

Removing the illiquidity discount is worth 67. Moving off the total beta is worth another
961. That second number is what diversification alone buys, and handing it to the buyer by
carrying a total beta into their valuation undervalues the business by a factor of three.

## IPO: the preferred waterfall

A cap table with 100 million common shares and one preferred round holding 50 million
as-converted shares behind a $100 million liquidation preference.

| Equity available | Round's choice | Value per common share |
|---|---|---|
| 1,000 | converts; the 50m stake is worth 333 | `1,000 / 150 = 6.67` |
| 120 | takes the preference; converting is worth 40 | `(120 − 100) / 100 = 0.20` |

Set `converts: "auto"` and the engine iterates to the fixed point, because each round's
choice moves the per-share value the others are choosing against. A round that takes cash
keeps its shares out of the denominator. If the preference stack is larger than the equity
being offered, common is worth zero and the output says so.

## Cyclical: the earnings normalizer

`normearn.xls`, the stored case. Five years of revenues 2,032 / 2,376 / 2,779 / 3,155 /
3,248 against EBIT of 186 / 454 / 529 / 448 / 383. Current revenues are 12,154 and book
capital is 11,722.

| Approach | Calculation | Result |
|---|---|---|
| 1, average EBIT | entered directly | 3,500 |
| 2, average return on capital | 0.22 × 11,722 | 2,578.84 |
| 3, aggregate margin | 0.1471670 × 12,154 | 1,788.67 |

The aggregate margin is 2,000 / 13,590 = 14.7167%, the sum of EBIT over the sum of
revenues. The average of the five yearly margins is 14.6577%, a different number. The
aggregate is the one the model uses.

Approach 1 is wrong here and the reason is visible in the inputs. The firm's revenues have
grown several-fold, so an average of old dollar earnings understates today's business.

The normalized EBIT then drives the rest of the chain. Coverage is 1,788.67 / 121 = 14.78,
using the operating lease expense as the interest charge because balance-sheet debt is
zero. Run that through `cost-of-capital-toolkit rating` for the synthetic rating and the
cost of debt.

## Commodity: Shell at $40 oil, March 2016

Annual data from 1989 to 2015 gives revenues as a linear function of the oil price with an
R-squared of 96.44%. At that fit, the oil price essentially is the revenue model.

```
revenues ($m) = 39,992.77 + 4,039.40 × price per barrel
39,992.77 + 4,039.40 × 40 = 201,569
```

The base operating margin of 3.01% is a trough number, so it converges over five years to
the 9.35% average of 2000 to 2015. Terminal return on capital is the 12.37% historical
average. Revenue growth is the firm's own 3.91% compounded rate.

The answer is $39.31 per share **at a $40 oil price**. Saying it that way is the point. A
reader who thinks oil will be $60 reruns the regression instead of arguing with the DCF.

## Young company: Amazon, January 2000

Trailing revenues $1,117 million on a −36.71% margin. The mature end-state is the 10%
operating margin of the retail industry, and the sales-to-capital ratio is 3.00.

```bash
python3 resources/special.py young-company --example \
  | python3 resources/special.py young-company
```

| Year | Growth | Revenue | Margin | EBIT | Reinvestment |
|---|---|---|---|---|---|
| 1 | 150.0% | 2,793 | −13.35% | −373 | 559 |
| 2 | 100.0% | 5,585 | −1.68% | −94 | 931 |
| 3 | 75.0% | 9,774 | 4.16% | 407 | 1,396 |
| 4 | 50.0% | 14,661 | 7.08% | 1,038 | 1,629 |
| 5 | 30.0% | 19,059 | 8.54% | 1,628 | 1,466 |
| 6 | 25.2% | 23,862 | 9.27% | 2,212 | 1,601 |
| 7 | 20.4% | 28,729 | 9.64% | 2,768 | 1,623 |
| 8 | 15.6% | 33,211 | 9.82% | 3,261 | 1,494 |
| 9 | 10.8% | 36,798 | 9.91% | 3,646 | 1,196 |
| 10 | 6.0% | 39,006 | 9.95% | 3,883 | 736 |

Two shapes are doing the work. Growth holds through year 5 and then fades linearly to the
6% stable rate. The margin closes half the remaining gap to the 10% target each year, which
is the `halving` style.

The rest of the valuation runs in `dcf-valuation-engine`. Terminal value is 1,881 / (0.0961
− 0.06) = $52,148 million. Operating assets are $15,170 million, plus $26 million of cash,
less $349 million of debt, less $2,892 million of employee options, over 340.8 shares, for
**$35.08 per share** against a market price of $84.

## What the Amazon case is actually worth knowing for

The direction call was right and nearly every line item was wrong. The assumed 10% mature
margin never arrived: the actual operating margin peaked at 6.36% in 2004 and fell to
0.11% by 2014. Revenues meanwhile blew past the forecast, $85,247 million actual against
$51,460 million forecast in 2014.

That is the argument for the sensitivity grid and the simulation rather than the point
estimate. Run `dcf-valuation-engine sensitivity` across the target margin and the growth
path before quoting a number.
