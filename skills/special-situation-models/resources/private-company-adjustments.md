# Private company adjustments

## Who the marginal investor is

Standard risk models assume the marginal investor is diversified. Such an investor holds
many assets, firm-specific risk washes out, and only market risk gets priced. That is what
beta measures.

An owner with every dollar of wealth in one business is exposed to all of the risk. Total
beta charges for that.

```
total beta       = market beta / correlation with the market
correlation      = square root of the average R-squared of the comparables' regressions
levered total    = total unlevered beta × (1 + (1 − tax rate) × debt/equity)
cost of equity   = riskfree rate + levered total beta × equity risk premium
```

The square root matters. R-squared is a share of variance, and betas are built from
standard deviations, so the correlation is the right adjustment. Dividing a 1.18 beta by an
R-squared of 0.25 gives 4.72; dividing by the correlation of 0.50 gives 2.36. The first
number is wrong by a factor of two.

## Partial diversification

A buyer is rarely at one extreme. Use the correlation of the buyer's own portfolio with
the market, not the correlation of a single-asset holder.

| Holder | Correlation | Perceived beta | Cost of equity |
|---|---|---|---|
| Fully invested private owner | 0.25 | 4.00 | 24% |
| Specialised venture fund with several holdings | 0.50 | 2.00 | 14% |
| Diversified public investors | 1.00 | 1.00 | 9% |

Illustrative, with a sector market beta of 1, a 4% riskfree rate and a 5% premium. The
spread across the column is the whole point: the same business is worth very different
amounts to different buyers, and that difference is the negotiation.

## Choosing the comparables

Pick them on business economics, not on the industry label. Damodaran's upscale French
restaurant is the standing example. Most listed restaurants are fast-food and mass chains,
and their 0.86 unlevered beta describes a different business. High-end specialty retailers
gave 1.18 with an average R-squared of 25%. That single choice moved the beta more than
every other input combined.

Take the R-squared from the same regressions that produced the betas.

## The debt-to-equity ratio

Use the industry-average market debt-to-equity ratio of listed firms in the sector. Using
your own estimated debt and equity values is circular: you need the cost of capital to get
the values and the values to get the cost of capital. If you insist on your own, iterate
until it stops moving.

Lever the beta and weight the cost of capital at the **same** ratio. And do not confuse
debt-to-equity with debt-to-capital: a 14.33% debt-to-equity ratio is a 12.53% debt weight,
not 14.33%.

Assemble the cost of capital in `cost-of-capital-toolkit`. Its `rating` subcommand builds
the synthetic cost of debt from interest coverage, and `wacc` does the weighting. For a
restaurant with no bank debt, use the lease expense as the interest charge; a firm with
lease commitments is not a zero-leverage firm.

## The illiquidity discount

A buyer of a private business cannot sell it back to a market tomorrow. That is worth
something, and equity value has to be reduced for it.

**The discount applies only when the buyer has no liquid exit.** A private-to-private buyer
gets one. A publicly traded acquirer does not, because its own shareholders can sell. A
firm going public does not either.

Three routes, and they disagree materially on the same firm.

### Route 1: a flat rate

20% to 30%, typically 25%. No firm-specific input at all. Damodaran calls it the bludgeon
and argues against it. Use it as a sanity check or when the counterparty expects it.

### Route 2: the Silber-refined base

Silber (1991) related restricted-stock discounts to the offering's characteristics:

```
S = 4.33 + 0.036 ln(revenues) − 0.142 ln(block %) + 0.174 (1 if profitable)
predicted discount d = (100 − e^S) / 100
discount = base discount − [ d(anchor) − d(firm) ]
```

The anchor is a firm with $10 million of revenue and positive earnings, and the base
discount attached to it is 25%. The block term appears identically in both predictions and
cancels exactly, so block size does not change the answer. That is the spreadsheet's
behaviour and the script reproduces it deliberately.

Small profitable firms land near 25% to 26%. A billion-dollar profitable firm lands near
16%. Unprofitable firms run about 8 to 9 percentage points higher at every size.

### Route 3: the bid-ask spread regression

Every traded asset is somewhat illiquid, and the bid-ask spread prices that. Regress the
spread on characteristics you can also measure for a private firm, then set trading volume
to zero:

```
spread = 0.145 − 0.0022 ln(revenues) − 0.015 (1 if profitable)
         − 0.016 (cash/firm value) − 0.11 (monthly volume/firm value)
```

This is the most firm-specific route and it draws on a large unbiased sample. It also gives
much smaller answers: 12.88% for the restaurant against 28.75% from the Silber route.

Revenues go in as millions of dollars. The logarithm makes a units error silent.

### Which to prefer

The bid-ask route when you have revenues, profitability and cash. It varies with the firm
and it is the easiest to defend.

Then adjust for what no regression sees. Larger and healthier firms deserve smaller
discounts. Tight credit and a bad economy raise them. A buyer with a short horizon and
high cash needs faces a larger one than a patient holder.

### The sampling problem

Do not quote 30% to 35% as the illiquidity discount. The firms that issue restricted stock
are small, troubled and out of conventional financing options. Pre-IPO sellers were also
pricing the risk that the IPO would never happen. One comparison of all private placements
against restricted-stock offerings put pure illiquidity below 10%, leaving 20 to 25
percentage points of the headline number to sample selection.

## Lack of control is a separate discount

A minority stake cannot move the firm to how it would be optimally run, so it is priced off
the status quo value:

```
minority discount = (optimal equity value − status quo equity value) / optimal equity value
```

This is a different friction from illiquidity. Applying both to the same stake needs a
reason rather than reflex. The calculation is not in this script; it is one line, and the
work is in estimating the optimal value, which belongs in a control-premium analysis.

## Worked example: the restaurant

Revenues $1.2 million, profitable, cash 5% of firm value, no trading. Equity value before
any discount is $520,990.

| Route | Discount | Value of equity |
|---|---|---|
| Flat | 25.00% | $391,000 |
| Silber-refined | 28.75% | $371,000 |
| Bid-ask spread | 12.88% | $454,000 |

The gap between the crudest and the most refined route is $83,000 on a $521,000 business,
about 16% of the value. The choice of method is not a rounding decision, and a seller will
prefer one route while a buyer prefers another.

## Pitfalls

- Dividing by R-squared rather than by the correlation.
- Applying a total beta to a diversified buyer, which hands the surplus to the buyer.
- Applying a total beta at full strength to a partially diversified fund.
- Picking comparables by industry label.
- Applying an illiquidity discount when the buyer is a listed company or the firm is
  going public.
- Applying the discount to firm value rather than to equity value.
- Entering revenues in dollars rather than millions.
- Leaving trading volume non-zero in the bid-ask regression.

## Sources

Damodaran, Valuation lecture packet 2, Spring 2020 and Spring 2021: total beta, private
company cost of capital, the illiquidity discount, the Silber restricted-stock regression,
the bid-ask spread regression, the minority discount. Spreadsheet models `pvtdiscrate.xls`,
`liqdisc.xls`, `minoritydiscount.xls`.
