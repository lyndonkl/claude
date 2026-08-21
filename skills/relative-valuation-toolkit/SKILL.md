---
name: relative-valuation-toolkit
description: Prices a company against peers and the market with multiples — builds PE, PEG, PBV, EV/EBITDA, EV/EBIT, EV/Sales and EV/Invested Capital with the numerator/denominator consistency rule enforced, computes peer medians and quartiles, fits an ordinary-least-squares regression of a multiple on its companion variables for a sector or the whole market, reports predicted versus actual under and over valuation, and derives the intrinsic multiple from DCF fundamentals. Prices a conglomerate division by division with a sum of the parts, and values cross-holdings and minority interests. Bundles Damodaran's regional pricing regressions and multiple distributions. Use for relative valuation, comparable company analysis, trading comps, sector or market multiple regressions, justified multiples, PEG screens, sum-of-the-parts or break-up analysis, conglomerate discounts, cross-holdings and minority interests, or when asked whether a stock is cheap on its multiple.
---

# Relative valuation toolkit

Relative valuation infers what an asset is worth from what the market pays for similar
assets. It is pricing, not valuation. A stock can be cheap against its comparable group
and still be badly overpriced in absolute terms — in a bubble the whole group is wrong
together. Say "cheap versus these peers", never "cheap".

Practice runs on this method. Roughly 85% of equity research reports and more than half of
acquisition valuations rest on multiples, and plenty of discounted cash flow models are
relative valuations in disguise, with a terminal value set at 8x year-5 EBITDA.

The arithmetic here is scripted. Your job is choosing the comparable set, choosing the
control technique, and deciding what an unexplained residual means.

## The script

`resources/multiples.py` — pure standard library, no installation needed. Every
subcommand takes JSON on stdin (or `--in FILE`) and prints JSON.

```bash
python3 resources/multiples.py <subcommand> --example    # show input shape
python3 resources/multiples.py <subcommand> --in payload.json
python3 resources/multiples.py selftest                  # verify the engine
```

| Subcommand | Turns this | Into this |
|---|---|---|
| `multiples` | financials and a market price | traded multiples, with inconsistent pairings refused |
| `peer-stats` | a column of peer multiples | median, quartiles, skew, drop-out count, median test |
| `locate` | one multiple | where it sits in a bundled market distribution |
| `intrinsic` | DCF fundamentals | the justified multiple those fundamentals imply |
| `regress` | a sector or market sample | coefficients, R-squared, standard errors, t-statistics |
| `predict` | a fitted or published equation | predicted multiple and the over/under percentage |
| `sum-of-parts` | divisions and their multiples | per-division values and shares, the total, the gap to market |
| `cross-holdings` | stakes in other firms | what to add, what to subtract, and at what value |

`selftest` runs 106 checks: worked examples from the source, and algebraic identities a
wrong implementation cannot satisfy by accident. Run it after editing anything.

## Run the multiple through four tests

Every multiple gets four tests before you trust it. Skipping any one of them is how
comparable-company analysis becomes an exercise in confirming what you already believed.

```
Relative valuation progress:
- [ ] 1. Definitional — settle the numerator, denominator and timing
- [ ] 2. Descriptive — find where the multiple actually sits today
- [ ] 3. Analytical — derive its companion variable from a DCF
- [ ] 4. Application — pick comparables and control for the differences
```

## 1. Definitional test

A multiple is a standardized price: what you pay divided by what you get. Two rules.

**Consistency.** The numerator and denominator must belong to the same claimholders.
Equity value goes with equity earnings or equity book value. Firm or enterprise value goes
with operating measures. The script refuses the mismatches rather than computing them, so
`EV/Net Income` and `Price/EBITDA` come back with an explanation instead of a number.

**Uniformity.** Every variable must be estimated the same way across every firm in the
comparable list, accounting rules included. The same name hides many variants, so never
borrow a multiple without knowing how it was built.

```bash
python3 resources/multiples.py multiples --example | python3 resources/multiples.py multiples
```

Supply `market_cap` (or `price_per_share` and `shares_outstanding`), `debt`, `cash`,
`minority_interests`, and whichever denominators you have. Use the **market** value of
debt from `cost-of-capital-toolkit` (`mv-debt`, field `market_value_of_debt`), not book
debt. Take lease- and research-adjusted earnings from
`financial-statement-normalization`, and apply the adjustment to every firm or to none.

The script nets cash out of enterprise value because interest income on cash appears in
neither EBITDA nor EBIT. It adds minority interests back because a consolidated but
partly owned subsidiary puts all of its EBITDA in the denominator while the parent owns
only part of the equity.

Ask for an arbitrary pairing with `custom`:

```json
"custom": [{"name": "EV/Net Income", "numerator": "enterprise", "denominator": "net_income"}]
```

**Negative denominators are refused, not computed.** A PE built on a loss is not a small
number or a large one. It carries no ordering at all, so it cannot be ranked against
anything. The output says which metric was negative and what to price on instead — a
denominator that stays positive, a forward year, or a sector-specific driver. Record the
refusal. That firm has now dropped out of the sample, and the drop-out biases every peer
statistic computed without it.

Full map of numerators, denominators, timing variants and companion variables:
[resources/multiple-map.md](resources/multiple-map.md).

## 2. Descriptive test

You cannot call a multiple high or low without knowing the distribution it came from.

Multiples are bounded at zero on the left and unbounded on the right, so their
cross-sections are heavily right-skewed and the mean sits far above the median. In January
2021 the average US trailing PE was 103.25 against a median of 20.30 — the mean sat above
the 90th percentile. Use the median or a percentile band. The mean of a multiple is close
to meaningless.

```bash
python3 resources/multiples.py peer-stats --example | python3 resources/multiples.py peer-stats
```

Each firm needs `multiple`, and optionally `companion` and `risk`. Pass `universe_size` as
the number of firms you started with, not the number that survived. The output separates
`firms_with_a_usable_multiple` from `firms_dropped` and names each dropped firm, because
that count is itself a finding. Only about a third of US firms had a usable trailing PE in
January 2021, so PE-based conclusions describe the profitable subsample.

Handle outliers with care. They lie almost entirely on the positive side, so trimming them
biases the typical multiple downward. Cap or use percentiles instead.

Add a `subject` and the output runs the **median test**: cheap needs a below-median
multiple with an above-median companion variable and below-median risk. Treat it as a
screen. It weighs each variable independently and ignores the size of every gap, so it
runs out as soon as firms differ on more than one dimension.

To place a multiple in the wider market rather than in your peer set:

```bash
echo '{"table": "us_trailing_pe_2021", "value": 14.2}' | python3 resources/multiples.py locate
```

**Thresholds decay.** "Buy below 6x EBITDA" put you in the middle of the US distribution in
January 2010 and below the 10th percentile by January 2021. Run `locate` against
`regional_ev_ebitda_median_2021` and the same 6x reads as deeply cheap in the US and close
to normal in Japan. Same number, opposite verdicts, purely because the distribution moved.

## 3. Analytical test

Every multiple is a discounted cash flow model in compressed form. Divide the model by the
multiple's denominator and the drivers fall out. The one that dominates cross-sectional
differences is the **companion variable** — the thing you have to control for.

| Multiple | Companion variable |
|---|---|
| PE | expected growth, with payout and cost of equity as controls |
| PEG | risk, payout and the level of growth |
| PBV | return on equity |
| EV/Invested Capital | return on invested capital |
| EV/Sales | after-tax operating margin |
| P/Sales | net margin |
| EV/EBITDA | reinvestment needs, tax rate, cost of capital |

```bash
echo '{"multiple": "PBV", "roe": 0.2022, "growth": 0.04, "cost_of_equity": 0.09,
       "actual_multiple": 2.09}' | python3 resources/multiples.py intrinsic
```

Use an equity model for equity multiples and a firm model for enterprise multiples. Take
the discount rate from `cost-of-capital-toolkit` (`wacc`, fields `cost_of_equity` and
`wacc`). Add `actual_multiple` to get the gap between traded and justified.

Three things the output is telling you:

- **The relationship is never linear.** PE rises with growth far faster at low required
  returns than at high ones, and the drag from risk is proportionately larger for
  high-growth firms. A risky high-growth firm can deserve a lower PE than a safe
  low-growth one.
- **Growth has to be paid for.** `g = (1 - payout) x ROE` on the equity side and
  `g = reinvestment rate x ROIC` on the enterprise side. The `PBV` output reports the
  sustainable growth your inputs imply and flags the gap. When the long and short forms
  disagree, the inputs are inconsistent and neither answer is usable.
- **A low EV/EBITDA is often deserved.** EBITDA sits above the capital spending that keeps
  the assets running. Raising CapEx from 30% to 50% of EBITDA cuts the justified multiple
  from 8.24 to 4.24 on otherwise identical inputs. Ryder System at 2.81x against a
  trucking sector at 5.61x was a truck-leasing firm with an ageing fleet, not a bargain.

**PEG does not neutralise growth.** Dividing by growth does not strip growth out, because
value is non-linear in growth. PEG falls with risk and with the level of growth, so a PEG
screen systematically flags the riskiest and fastest-growing names as cheap. If you use
it, regress PEG on beta, payout and ln(growth) rather than comparing raw PEGs.

Formulas, symbol definitions and the full `intrinsic` payload table:
[resources/multiple-map.md](resources/multiple-map.md).

## 4. Application test

Pick the control technique by counting how many fundamentals differ.

| Dimensions that differ | Technique |
|---|---|
| None — true twins | Direct comparison. Higher multiple is expensive. |
| One | Tell the story, or use a modified multiple like PEG. |
| Several | Regress the multiple on the fundamentals. |

The third row is the normal case.

```bash
python3 resources/multiples.py regress --example | python3 resources/multiples.py regress
python3 resources/multiples.py predict --example | python3 resources/multiples.py predict
```

`regress` fits by the normal equations, solved with Gauss-Jordan elimination and partial
pivoting, and returns coefficients, standard errors, t-statistics, R-squared, adjusted
R-squared, residuals, and the correlation of every predictor pair. Enter every predictor
as a decimal.

`predict` takes the equation three ways: `observations` to fit the sample first,
`equation` for your own coefficients, or `library` for a bundled published regression.
Omit `subject` after fitting and it prices every firm in the sample.

```
under/over valuation = actual multiple / predicted multiple - 1
```

### Sector or market

A **sector** regression asks whether the firm is cheap against its peers. A **market-wide**
regression asks whether it is cheap against every listed firm, given its fundamentals.
Both are legitimate and they can disagree, because the peer group may itself be mispriced
against the market. State which benchmark your verdict uses.

Bundled market and regional equations cover PE, PEG, PBV, EV/EBITDA, EV/Sales and EV/IC
for six regions, plus the country PE regression and the S&P 500 earnings-yield regression.
Pick the multiple with the highest regional R-squared when several disagree — EV/IC fits
run 50-63%, PEG fits 11-33%.

### Reading a fit

Check the t-statistics first. Above 2 is real, 1 to 2 is marginal, below 1 is noise. Drop
the noise and re-run, even when theory insists the variable belongs. In pricing the market
decides what matters, and explanatory power rarely suffers.

Then check R-squared. Below about 15% the sample is not priced on those fundamentals, so
report the prediction as weak evidence rather than as an estimate.

Then check the signs against theory. A wrong sign is almost always multicollinearity, not
a discovery.

The engine raises four warnings you should read before quoting any prediction:

- **Negative intercept.** The equation can hand a weak firm a negative predicted multiple.
  The engine refuses to report an over/under against one. Re-run with `"intercept": false`
  and treat that as an imperfect fix, not a repair.
- **Multicollinearity between growth and risk.** High-growth firms pay out less and often
  carry more risk, so the predictors overlap and individual coefficients flip sign. When
  this fires, use the prediction and ignore the coefficients.
- **Small sample.** A 15 to 30 firm sector cannot support many predictors. Sector
  coefficients move violently between vintages; re-estimate every period.
- **Pooled markets.** Add a `region` field to your observations. Country PE levels are
  driven by interest rates, real growth and country risk. Pooling markets attributes those
  country differences to the firm-level predictors instead.

Fitting details, the full library index, distribution tables and reproduced worked
examples: [resources/regressions.md](resources/regressions.md).

### The lesson of the worked examples

Telebras had one of the two lowest PEs in global telecom. Controlled for growth and
emerging-market risk, it predicted at 8.35 and traded at 8.9 — slightly **expensive**. A
low multiple is not the same as cheap, and that is the whole point of step 4.

## Sum of the parts: pricing a multi-business firm

A conglomerate is not one comparable set. Price each division against its own sector, add
the pieces, then take out what the segments never contained.

```bash
python3 resources/multiples.py sum-of-parts --example | python3 resources/multiples.py sum-of-parts
python3 resources/multiples.py cross-holdings --example | python3 resources/multiples.py cross-holdings
```

### Pricing each division

Each division needs a `scalar` (`ebitda`, `revenues`, `capital`, `ebit`) and a
`scalar_value`, plus one of three routes to a multiple.

| Route | Field | What it does |
|---|---|---|
| Own multiple | `multiple` | a number you have already settled |
| Crude | `peer_multiple` | the sector median, applied as it stands |
| Refined | `regression` with `fundamentals` | the sector equation evaluated at this division's own returns and margins |

A division is not the median firm in its sector. Controlling for fundamentals moved United
Technologies from $61.7bn to $74.2bn.

Where segment disclosure stops at operating income, pass `normalized_ebit` and `d_and_a`
and the script builds EBITDA. Normalise a cyclical segment first — GE's segments run on
the 2013-17 average margin applied to 2017 revenues, not on 2017 alone.

Every division comes back with its value and its `share_of_sum_of_parts`. Those shares add
to one, so they show which business the valuation actually rests on.

Every part has to be valued before debt. An equity-level multiple is refused, because the
bridge subtracts debt once at the corporate level.

### Three traps the engine will not let you walk into

**Unallocated corporate overhead.** Segment operating income is reported before corporate
G&A, so the divisions add to more than the firm is worth. Either allocate the overhead
across the divisions before you price them (`corporate_costs_already_allocated: true`) or
pass `corporate_expenses` and let the script capitalise it:

```
drag = corporate expenses x (1 - t) x (1 + g) / (company cost of capital - g)
```

UTC's $408m of overhead is worth -$4,587m, about 6% of the total. The payload has to say
which treatment it used. Leaving the field out is refused, because a silent zero overstates
every conglomerate.

**The conglomerate discount is observed, not derived.** Pass `market_enterprise_value` and
the output reports `gap_to_market_enterprise_value`, which is 1 minus market EV over the
sum of the parts. Nothing above it is reduced. UTC's parts priced at $74.2bn against a
$52.3bn enterprise value — a 30% gap that is only money if somebody buys the pieces at peer
multiples, and may instead be the market's price for bad capital allocation. Passing a
`conglomerate_discount` of your own is refused: it makes the sum of the parts agree with
the market by construction.

**Growth has to be earned division by division.** Give each division its `roc` and
`cost_of_capital`. One earning at or below its cost of capital comes back with
`high_growth_years_allowed: 0` and a warning. UTC Fire & Security earned 6.03% against a
6.78% cost of capital, so its whole value is terminal. A sector peer multiple carries the
sector's growth with it, so applying one there prices in growth the division never earned.

### Cross holdings

Accounting reports the three ownership tiers three different ways, and each one distorts
the valuation in its own direction.

| Stake | Consolidated | Treatment |
|---|---|---|
| Minority passive, under 20% | No | add the stake |
| Minority active, 20-50% | No | add the stake, and strip its equity income out of operating income |
| Majority, above 50% | Yes | 100% is already inside the value; subtract the minority interest |

`cross-holdings` takes a list of `holdings`, each with `ownership` as a decimal. Set
`consolidated` yourself; without it the script infers from the 50% line and says so, and
control can attach below 50%.

**Subtract the minority interest at market, not at book.** Best is
`subsidiary_equity_value`, from which the script takes the fraction the parent does not
own. The fallback is `minority_interest_book` with `sector_price_to_book`. Book on its own
is refused: it runs far too low for a profitable subsidiary. On the worked exercise the
book shortcut gives $810m and the intrinsic treatment $725m, on a firm worth under a
billion.

**Add a minority stake at market where it trades** (`market_value_of_stake`), at your own
valuation where you have one (`subsidiary_equity_value`), and at `book_equity` times
`sector_price_to_book` where you have neither. The output labels which of the three it
used. Inside an intrinsic valuation a traded value imports the market's error into your
answer, and the script says so.

Net `taxes_due` on unrealised gains. They came to $5,017m on Yahoo's stakes, over 10% of
its equity value.

## Reference data

`resources/data/published_regressions.json` and
`resources/data/multiple_distributions.json` are tagged with an `as_of` date and a refresh
note. Both are snapshots. Coefficients swing hard: the US price of an extra percentage
point of expected growth ranged from 0.41 in January 2012 to 2.62 in January 2003.
Distributions move far enough to reverse a verdict. Refresh from
`https://pages.stern.nyu.edu/~adamodar/` annually, and record which vintage a valuation
used.

Two unit conventions live in the regression file. Most entries take decimals; two
reproduce statistics-package output in percentage points. Read the `units` field first.

## Handing off

| Need | Where it comes from |
|---|---|
| Cost of equity, WACC, market value of debt | `cost-of-capital-toolkit` — `wacc`, `mv-debt` |
| Adjusted EBIT, EBITDA, FCFF, invested capital, ROE, ROIC | `financial-statement-normalization` — `normalize`, `fcff` |
| Intrinsic value to compare a pricing verdict against | `dcf-valuation-engine` — `value` |
| Value of employee options before a per-share multiple | `option-valuation-toolkit` |
| Divisional costs of capital for the zero-growth rule | `cost-of-capital-toolkit` — `wacc` per division |
| The `cross_holdings` figure a sum of the parts bridges with | `cross-holdings` in this skill |
| Cross-artifact consistency before you publish | `valuation-consistency-checks` — `validate` |

A pricing verdict and a DCF that disagree is a useful result, not a problem. Run
`dcf-valuation-engine implied` to see what assumption the market price already contains,
then argue about that assumption rather than about the multiple.

## Common failures

| Symptom | Cause |
|---|---|
| Engine refuses the multiple | Numerator and denominator belong to different claimholders, or the denominator is negative — both are real errors |
| Every firm in the sector looks cheap | Comparison against a mean rather than a median on a right-skewed distribution |
| Cheap on the multiple, expensive on the regression | The low multiple was explained by weak fundamentals all along |
| Predicted multiple comes back negative | Negative intercept in the fitted equation; re-fit through the origin |
| Coefficient has the wrong sign | Multicollinearity among the predictors, not a finding |
| Verdict flips between vintages | Coefficients re-estimated on a different year; expected, and the reason to date every fit |
| Low EV/EBITDA that never re-rates | Reinvestment needs justify the low multiple; check CapEx/EBITDA |
| PEG screen keeps surfacing the same names | PEG loads on risk and high growth; it does not neutralise growth |
| Half the sector has no multiple | Negative earnings or book value; switch to a revenue or forward multiple |
| Multiple looks cheap against another market | Different interest rates, growth and country risk; compare within a market first |
| Sum of the parts refuses to run | No treatment declared for unallocated corporate overhead; allocate it or capitalise it |
| The parts beat the whole by a suspicious margin | Corporate overhead dropped, or one sector multiple applied to every division |
| A division looks cheap on its sector multiple | It earns below its cost of capital, so the sector's growth does not belong to it |
| Cross holdings refused | Book minority interest with no sector price-to-book; book is not market value |
| Equity value too high after consolidation | The minority interest was never subtracted, so shareholders get a subsidiary they part own |
