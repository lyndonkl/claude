---
name: cost-of-capital-toolkit
description: Estimates discount rates and the optimal financing mix — riskfree rate in any currency, equity risk premium including country risk, bottom-up and total betas, synthetic credit ratings from interest coverage, cost of debt, market value of debt, WACC, the implied equity risk premium solved from current index levels, and the cost-of-capital schedule across debt ratios that locates the optimal debt ratio, with an APV cross-check and a stress test under rating constraints. Bundles Damodaran's rating and spread tables, Altman default probabilities, industry-average betas and multiples, and country risk premiums, each tagged with its vintage. Use when estimating a discount rate, WACC, hurdle rate, cost of equity or cost of debt, unlevering or relevering a beta, when a company has no credit rating, when estimating the equity risk premium priced into the market, when looking up a sector beta or country risk premium, when converting a rate between currencies, or when finding or stressing an optimal capital structure.
---

# Cost of capital toolkit

Every discounted valuation needs a rate. Most valuation errors that survive review are rate
errors. A rate built in one currency gets applied to cash flows in another. A regression
beta describes a period that no longer matches the business. Book weights sit where market
weights belong.

The arithmetic is fully scripted. Your job is choosing the inputs — which comparables,
which premium estimator, gross or net debt — and defending those choices.

## The scripts

Two of them, both pure standard library with nothing to install. Every subcommand takes
JSON on stdin (or `--in FILE`) and prints JSON.

`resources/costofcapital.py` does the arithmetic.

```bash
python3 resources/costofcapital.py <subcommand> --example    # show input shape
python3 resources/costofcapital.py <subcommand> --in payload.json
python3 resources/costofcapital.py selftest                  # verify the engine
```

| Subcommand | Turns this | Into this |
|---|---|---|
| `rating` | EBIT and interest expense | synthetic rating, default spread, pre-tax and after-tax cost of debt |
| `beta` | comparable betas, or one levered beta | unlevered, relevered, bottom-up, or total beta |
| `mv-debt` | book debt, interest expense, maturity | market value of debt |
| `wacc` | component costs and values | WACC with weights |
| `debt-schedule` | unlevered beta, EBIT, firm value | cost of capital at every debt ratio, the optimum, and the value of moving there |
| `implied-erp` | index level and expected cash flows | the expected return and equity risk premium the market is pricing in |
| `apv` | equity, debt, tax rate, bankruptcy cost | unlevered value, tax shield and expected distress cost at every debt ratio |
| `stress` | a `debt-schedule` payload plus haircuts or a rating floor | how far the optimum moves under weaker EBIT, and what a rating floor costs |
| `convert-rate` | a rate and two inflation rates | the same rate in another currency |

`resources/reference_data.py` serves the bundled tables. Every other engine reads its
industry and country numbers through here, so a valuation cannot quietly mix a beta from
one year with a country premium from another.

```bash
python3 resources/reference_data.py <subcommand> --example
python3 resources/reference_data.py <subcommand> --in payload.json
python3 resources/reference_data.py selftest
```

| Subcommand | Turns this | Into this |
|---|---|---|
| `lookup` | an industry, country or region name | the full reference row, tagged with its vintage |
| `erp-for-operations` | revenue shares by country | the revenue-weighted equity risk premium, and the cost of equity if you add a beta |
| `vintage` | a valuation date | the `as_of` of every bundled table, and a warning for each one the date has outrun |

Run `selftest` on both after editing anything. Between them they check the engines against
worked examples from the source models, including a full cost-of-capital build that
reproduces its sheet to eight decimals.

## Build the rate in this order

Each step feeds the next. Do not skip ahead: a beta is meaningless until you know the
currency, and weights are meaningless until debt is at market value.

```
Cost of capital progress:
- [ ] 1. Fix the currency, and the riskfree rate in it
- [ ] 2. Build the equity risk premium, including country risk
- [ ] 3. Estimate the beta bottom-up
- [ ] 4. Estimate the cost of debt
- [ ] 5. Weight at market values and assemble
- [ ] 6. Check consistency
```

### 1. Currency and riskfree rate

The currency of the rate must match the currency of the cash flows. That is a hard
constraint, not a preference — mismatching them builds an inflation differential into the
answer that has nothing to do with the business.

Take the long-term government bond yield when the government is default-free. When it is
not, strip the sovereign default spread out of the local bond yield:

    riskfree rate = local government bond yield − sovereign default spread

Get the sovereign spread from a rating-based table, a sovereign CDS, or the gap between
the government's local and hard-currency bonds. If no local bond exists, build the rate
from a mature-market rate and the inflation differential instead. Details and the
negative-rate case: [resources/methodology.md](resources/methodology.md).

Resist the urge to "normalize" a low riskfree rate upward. Doing so while leaving the
equity risk premium alone quietly raises every discount rate and understates every
company. If the rate looks wrong, change the cash flows, not the anchor.

### 2. Equity risk premium

Two layers. Start with a mature-market premium, then add country risk for where the
company actually **operates**, not where it is incorporated.

For the mature-market layer, compute the **implied premium** rather than reaching for a
historical average. Take today's index level as the price, forecast the cash the index
will return to its investors, and solve for the rate that makes the two agree. That rate
is the expected return on stocks; subtract the riskfree rate and the rest is the premium:

```bash
python3 resources/costofcapital.py implied-erp --in index.json
```

Supply the cash flows one of three ways: an explicit `cash_flows` list, an `earnings` path
with `payout_ratios`, or a `base_cash_flow` (or `dividend_yield`) with a `growth_rate`.
Whichever you use, the cash flow is **dividends plus buybacks**, not dividends alone.
Buybacks were 68.89 of the S&P 500's 127.78 in 2020; leaving them out roughly halves the
answer. Terminal growth defaults to the riskfree rate and is capped there, because no
perpetual growth rate can outrun the economy it grows in.

Why bother: the historical average is a mean with a standard error of roughly two points
on a five-point estimate, which is wide enough to swallow the number whole. The implied
premium has no standard error at all, and it moves — 4.83% in February 2020, 7.75% at the
March bottom, 5.35% by November. Re-run it whenever the market moves and record the date
you used. The same procedure works on any index: feed it the local level, the local cash
yield and the local riskfree rate.

Then the country layer:

    company ERP = mature market ERP + Σ (revenue share by country × country risk premium)

A country risk premium is the sovereign default spread scaled up for equity's greater
volatility. Weighting by operations matters: a Brazilian company earning most of its
revenue in the United States does not carry Brazil's full risk, and a US-incorporated
company earning most of its revenue in Brazil does.

```bash
echo '{"operations": [{"country": "Brazil", "revenue": 130},
                      {"country": "Canada", "revenue": 23}]}' \
  | python3 resources/reference_data.py erp-for-operations
```

Rows name a `country` or a `region`. Where a filer reports a bucket that maps to nothing
clean — "rest of world", "Eurasia", "Pacific" — give that row its own `erp` and say in
the writeup where the number came from. Weight by whatever measure locates the risk:
revenue usually, production for a resource company, assets for a manufacturer. Add a
`riskfree_rate` and a `beta` and the answer carries a cost of equity under both
attachments, adding the country premium and scaling it by beta, which on real emerging
market cases can differ by several points.

### 3. Beta

Use a bottom-up beta. Regression betas carry standard errors so large the point estimate
is rarely usable, and they describe a past business mix rather than the current one.

```bash
python3 resources/costofcapital.py beta --in businesses.json
```

Take the median unlevered beta of comparable firms in each business the company operates
in, weight by each business's estimated value, then relever at the company's own
debt-to-equity ratio:

    levered beta = unlevered beta × (1 + (1 − tax rate) × debt/equity)

Weight by value, and when segment values are not disclosed, approximate them as segment
revenue times a sector EV/Sales multiple. Both numbers come out of the same lookup:

```bash
echo '{"industry": "Aerospace/Defense",
       "fields": ["unlevered_beta", "ev_sales"]}' \
  | python3 resources/reference_data.py lookup
```

Names must match the table, but case and stray whitespace do not matter, and a miss comes
back with the near matches rather than nothing. Watch for labels the source sheet
truncated mid-word — `Insurance (Prop/Cas.)` is the real key, not a typo.

Use a **total beta** — `operation: total` — when valuing a company for an owner who cannot
diversify, typically a private business. It scales the market beta up by the inverse of
the correlation with the market, charging the owner for the firm-specific risk a
diversified investor would shed.

### 4. Cost of debt

What matters is what the company would pay to borrow **today**, not the coupon on debt it
issued years ago and not the rate a parent guarantees.

Prefer, in order: the yield to maturity on the company's own traded long-term bonds; the
spread implied by its agency rating; a synthetic rating from interest coverage.

```bash
echo '{"ebit": 2000, "interest_expense": 250, "riskfree_rate": 0.04,
       "marginal_tax_rate": 0.25, "table": "large_manufacturing"}' \
  | python3 resources/costofcapital.py rating
```

Pick the table that matches the company: `large_manufacturing` for large non-financial
firms, `small_or_risky` for smaller or more volatile ones (the same coverage buys a worse
rating), `financial_service` for banks and insurers.

    pre-tax cost of debt = riskfree rate + company default spread + country default spread

Only the marginal tax rate matters for the after-tax cost, and only to the extent there is
income to shelter — the engine caps the benefit when interest exceeds EBIT.

**Capitalized leases create a circularity.** Discounting lease commitments needs a cost of
debt; a synthetic rating needs interest coverage, which lease interest changes. Iterate:
compute a rate, capitalize leases, recompute coverage, recompute the rate, until it stops
moving. `debt-schedule` already does this internally.

### 5. Weights and assembly

Weight at **market** values. Book weights systematically understate equity for a profitable
company. Convert book debt to market by treating all of it as one coupon bond:

```bash
python3 resources/costofcapital.py mv-debt --in debt.json
```

Use the weighted-average maturity of outstanding debt; where it is not disclosed, three
years is the working default. Add capitalized lease debt afterwards — it is already a
present value.

    WACC = cost of equity × E/(D+E+P)
         + pre-tax cost of debt × (1 − tax rate) × D/(D+E+P)
         + cost of preferred × P/(D+E+P)

Preferred stock is a third component when it is material; below about 5% of capital, fold
it into debt rather than carrying a third term.

### 6. Consistency checks

- Currency of the rate equals currency of the cash flows.
- Weights sum to one and use market values.
- The tax rate used to relever the beta is the same one used for the after-tax cost of debt.
- Gross debt throughout, or net debt throughout — never mixed.
- The levered beta reflects the company's current debt ratio, not the comparables'.

## Finding the optimal debt ratio

The same machinery run in a loop. At each candidate debt ratio the engine relevers the
beta, re-prices the debt through a fresh synthetic rating, caps the tax benefit at
available income, and computes the cost of capital. The ratio with the lowest cost of
capital is the optimum, because the same cash flows discounted at a lower rate are worth
more.

```bash
python3 resources/costofcapital.py debt-schedule --in firm.json
```

Read the result with judgment:

- **The curve is usually flat near the bottom.** A move from 30% to 40% debt that saves
  four basis points is not an argument for anything. Look at the shape, not just the
  minimum.
- **Banks are excluded.** For a financial service firm, regulatory capital sets the
  financing mix. This calculation does not apply.

### Stress the answer, or constrain it

The optimum falls out of one number held fixed: operating income. Real operating income
moves. `stress` re-runs the same schedule with EBIT knocked down and reports where the
answer goes.

```bash
python3 resources/costofcapital.py stress --in firm.json
```

Take a `debt-schedule` payload and add whichever of these you have:

| Input | Effect |
|---|---|
| `haircuts` | re-runs at EBIT × (1 − h) for each h; defaults to 10% steps down to 60% |
| `recession_ebit` | re-runs at a stated recession level instead of a percentage cut |
| `ebit_history` | computes the standard deviation of annual percentage changes, then stresses by `n_sigma` of them (default 3) |
| `required_rating` | finds the highest debt ratio that still earns that rating, and prices the constraint |

The output's `safety_buffer` is the largest decline the optimum survives. Read it against
the firm's own record. Disney's 40% optimum held through a 30% cut. That is deeper than
its worst year on file and well past one standard deviation. A firm with that much room
is already protected; buying a rating floor on top pays twice for the same thing.

A `required_rating` is priced two ways: `cost_of_capital_given_up`, which is always
available, and `value_given_up`, which needs a cash flow and a growth rate to fall out of
the base schedule. Quote the second one to a board. "Sixteen basis points" does not land
the way a dollar figure does.

**Use one protection, not both.** A rating floor already guards against weak operating
income. Stacking a haircut on top leaves the firm under-levered for reasons nobody wrote
down. And separate the honest reasons for a rating floor from the vain one: protection
against downside risk is real, a ratings drop that itself damages the business is real,
and wanting to say the company is AAA-rated is not.

### The APV cross-check

`apv` answers the same question by different machinery, which is what makes it worth
running. Rather than folding distress risk into a default spread, it splits value into
three pieces: the firm with no debt, plus the tax shield debt creates, minus the expected
cost of the bankruptcy debt makes more likely.

```bash
python3 resources/costofcapital.py apv --in firm.json
```

    firm value = unlevered value + tax benefit(d) − p(default at d) × bankruptcy cost % × value at risk

Unlevered value is backed out of today's market price by removing the tax benefit the
market already pays for and adding back the distress cost it already charges for. Supply
`ebit` and `riskfree_rate` to have the rating at each debt ratio solved from interest
coverage, or supply a `ratings` list with one entry per debt ratio when you are
reproducing a published schedule or working from a rating outlook.

Two soft numbers drive the answer: `bankruptcy_cost_pct` and the default probability.
Direct bankruptcy costs run 5-10% of firm value; indirect costs are a judgment about how
badly customers, suppliers and employees would punish visible distress, and Damodaran's
worked examples use 25% in total. Treat the optimum as a region.

The two approaches should land in the same neighbourhood. When they diverge sharply,
suspect the bankruptcy cost assumption or the default probability table before you suspect
the arithmetic. The bundled probability column is genuinely non-monotonic, and that alone
can put the peak at a higher debt ratio than the economics would justify.

See [resources/optimal-capital-structure.md](resources/optimal-capital-structure.md) for
the enhanced approach with indirect bankruptcy costs and the mechanics of actually moving
to the optimal ratio.

## Reference data

The tables ship in `resources/data/`, each tagged with an `as_of` date and the source sheet
it was lifted from. The four the rate build leans on:

| File | Holds |
|---|---|
| `synthetic_ratings.json` | interest-coverage bands by firm type, and the rating-to-spread map |
| `industry_averages.json` | 96 rows of US industry averages — betas, costs of capital, sales-to-capital, multiples, margins, reinvestment rates |
| `country_risk.json` | 186 sovereigns and 10 regional aggregates — rating, default spread, country risk premium, total ERP, corporate tax rate |
| `default_probabilities.json` | Altman's rating-to-default-probability map, used by `apv` |

`default_probabilities.json` carries cumulative ten-year default rates by original rating.
Read down it and the column is not monotonic: Ba1/BB+ at 0.10 sits below Ba2/BB at 0.1663.
That is what the studies report, and it is reproduced verbatim, because it is what makes an
APV schedule peak where it does. Do not tidy it. Override it with `probabilities_path`, and
the ratings tables with `ratings_path`.

Start any valuation by checking how old they are against the date you are valuing as of.
The check reads whatever is in the directory, so a table added later is covered too:

```bash
echo '{"valuation_date": "2024-06-30"}' | python3 resources/reference_data.py vintage
```

Anything more than a year past its `as_of` gets a warning naming where to refresh it.
Damodaran reposts all three every January, and spreads in particular move by a factor of
three across vintages, so a stale table is not a rounding problem. Refresh into a copy and
point at it, rather than editing the bundled files.

Two habits worth keeping:

- **Never mix vintages inside one valuation.** A 2020 beta with a 2022 country premium is
  a number nobody can reproduce. Pass `vintage` on a lookup and it refuses to answer from
  a table that does not match.
- **`null` is not zero.** Margins, sales-to-capital, EV/EBITDA and working-capital columns
  come back null for banks, brokers and insurers, because the ratio is not defined for
  them. Read a null as zero and every average over that column is wrong.

## Common failures

| Symptom | Cause |
|---|---|
| Emerging-market company looks permanently cheap | Country risk applied by incorporation instead of operations |
| Beta swings wildly between updates | Regression beta instead of bottom-up |
| WACC below the cost of debt | Book weights, or a tax benefit not capped at available income |
| Value changes when the currency changes | Rate and cash flows in different currencies |
| Rating implausible for an obviously healthy firm | Wrong table, or EBIT not adjusted for leases and research spending first |
| Optimal debt ratio at an implausible 80% | EBIT taken at a cyclical peak, or no rating constraint applied |
| Sector benchmarks nobody can reproduce | Two reference tables of different vintages in the same build |
| A bank's sector multiple comes out at zero | A null read as a zero — the ratio is undefined for banks, not nil |
| Implied ERP comes out near half the published figure | Dividends used as the index cash flow, with buybacks left out |
| Implied ERP looks suspiciously low | Terminal growth set above the riskfree rate, inflating the terminal value |
| APV and `debt-schedule` disagree by a wide margin | The bankruptcy cost percentage, or cash netted out of one and not the other |
| The firm ends up under-levered for no stated reason | A rating floor and an EBIT haircut both applied — they guard the same risk |
