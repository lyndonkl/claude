---
name: option-valuation-toolkit
description: Prices options for valuation work — Black-Scholes with a cost-of-delay yield, binomial trees that allow early exercise, dilution-adjusted employee options for the equity bridge, equity in a heavily levered firm valued as a call on firm value, and implied volatility. Use when employee options or warrants must be subtracted before computing value per share, when a distressed or negative-earnings company's equity still trades above zero, when testing whether a patent, licence, undeveloped reserve or expansion right is a real option that deserves a premium, or when early exercise makes a European formula wrong. Triggers on option pricing, Black-Scholes, binomial tree, real options, option to delay, patent as an option, equity as a call option, distress and default probability, employee stock options, dilution, warrants, implied volatility, put-call parity.
---

# Option valuation toolkit

Four option problems recur in valuation work.

Employee options are a claim on equity. They have to be priced and subtracted before you
divide by shares. The equity of a deeply indebted firm behaves like a call option on the
firm's assets, which is why a stock keeps trading after a discounted cash flow model says
the company is worth nothing. A patent, a licence or an undeveloped reserve can carry
value that a static DCF misses. And some options get exercised early, which a European
formula cannot see.

The arithmetic here is exact. The inputs usually are not. When the underlying asset does
not trade, no replicating portfolio can be built and no arbitrage disciplines the answer.
Treat the output as an estimate with a wide band around it, and never quote it to the
dollar.

## The script

`resources/options.py` — pure standard library, no installation needed. Every subcommand
reads JSON on stdin (or `--in FILE`) and prints JSON.

```bash
python3 resources/options.py <subcommand> --example      # show the input shape
python3 resources/options.py <subcommand> --in payload.json
python3 resources/options.py selftest                    # verify the engine
```

| Subcommand | Turns this | Into this |
|---|---|---|
| `black-scholes` | spot, strike, life, volatility, riskfree rate, dividend yield | European call or put value, `d1`, `d2`, `N(d1)`, `N(d2)`, intrinsic and time value |
| `binomial` | the same inputs plus `steps` and `american` | tree value, up and down factors, risk-neutral probability |
| `employee-options` | equity value, share count, option terms | total option claim, value per option, value per share |
| `equity-as-option` | firm value, face value of debt, debt maturity | equity value, implied debt value, probability of default |
| `implied-vol` | an observed option price | the volatility consistent with that price |

`selftest` runs 18 checks and should report 18 passed. It holds put-call parity to nine
decimals. It confirms that a 500-step binomial tree converges to the Black-Scholes value.
It checks that an American put is never worth less than its European twin. It also verifies
that the dilution loop converges and that implied volatility inverts the pricer. Run it
after touching anything.

## Before you price a real option, run the three tests

Real options are everywhere. Most of them are worth nothing. The premium is admitted only
when three tests pass in order, and the burden of proof sits with whoever wants the
premium.

| Test | Question | Fails when |
|---|---|---|
| 1. Is there an option? | Can you name a specific underlying asset whose value moves unpredictably, and a payoff contingent on a stated event inside a finite window? | You cannot write down both. There is no option, so add nothing. |
| 2. Is it worth anything? | Does something stop competitors from exploiting the same contingency? | The product market is competitive. Rivals compete the excess return away, and the option is worth zero no matter how volatile the underlying. |
| 3. Can a model price it? | Is the underlying traded, is the option itself traded, and is the exercise cost knowable? | Usually at least one fails for a real asset. Trust the number roughly in proportion to how many hold. |

Test 2 is the one that kills most claims. Exclusivity is a spectrum, and the value you may
claim scales with it. Ranked from weakest barrier to strongest: first-mover advantage,
technological edge, brand name, telecom licences, pharmaceutical patents. Multiply the full
option value by an exclusivity factor between 0 and 1 rather than pretending the barrier is
absolute. A patent stops copies; it does not stop a rival developing a different drug for
the same disease.

**Opportunities are not options.** An opportunity is something you might do. An option is a
right that others do not have, with a defined underlying, a defined strike and a defined
expiry. "Real options" belongs in the same family as "synergy" and "strategic
considerations" — language reached for when a price has already been decided and needs
justifying. If test 1 or test 2 fails, add nothing to the DCF value. If test 3 fails alone,
use a decision tree instead and treat any option number as an order of magnitude.

Whatever you do, guard against double counting. If you value a patent separately as an
option, remove the growth that same patent would produce from the DCF of the existing
business.

### Mapping a real option onto the script

There is no separate real-option subcommand. You map the business facts onto
`black-scholes` or `binomial` inputs yourself.

| Real option | Type | `spot` | `strike` | `time_to_expiry` | `dividend_yield` |
|---|---|---|---|---|---|
| Option to delay | call | PV of project cash flows if taken now | initial investment | remaining exclusive rights | cost of delay |
| Product patent | call | PV of cash flows from launching now | PV of development cost | patent life | cost of delay |
| Undeveloped reserve | call | value of the developed reserve | development cost | relinquishment period | net production revenue as a share of value |
| Option to expand | call | PV of cash flows from the expansion | cost of entry | window before the right lapses | cost of delay |
| Option to abandon | put | PV of remaining project cash flows | salvage or abandonment value | remaining life of the escape clause | — |

The `dividend_yield` field is the single most consequential input in real-option work and
the one most often left at zero. It represents value leaking out of the underlying while
you wait. For a right that expires in `n` years, `1/n` is the working default: each year of
delay is one year of cash flows you will never collect. Real-option lives run five to
seventeen years, so omitting this yield overstates the answer badly.

Match the riskfree rate to the option's life. A seventeen-year option takes a
seventeen-year government bond rate, not a short rate.

### Worked example: a pharmaceutical patent

Biogen's patent on Avonex. The underlying is the drug: the present value of cash flows
from launching now is $3,422m, and development would cost $2,875m in present-value dollars.
The patent runs 17 years. Biotech industry variance of log value is 0.224, so volatility is
`sqrt(0.224)` = 0.4733. The 17-year bond rate is 6.7%. Cost of delay is `1/17` = 5.89%.

```bash
echo '{"spot": 3422, "strike": 2875, "time_to_expiry": 17, "volatility": 0.47328637,
       "riskfree_rate": 0.067, "dividend_yield": 0.0589, "option_type": "call"}' \
  | python3 resources/options.py black-scholes
```

The result is $905m, against an intrinsic value of $547m. The published figure is $907m;
the difference comes from reading `N(d)` off a table rounded to four decimals. Waiting is
worth roughly $358m more than developing today.

Optimal exercise falls out of repeating the calculation. Hold while the option value
exceeds `spot − strike`; exercise once it drops below. Re-run with `time_to_expiry` set to
16, 15, 14 and so on, and compare each result with the constant $547m. For Avonex the lines
cross at about eight years of remaining patent life. Past that point the cost of delay
dominates and holding destroys value.

## When a binomial tree beats Black-Scholes

Black-Scholes is the continuous-time limit of the binomial model. Both give the same answer
when their assumptions hold, which the selftest confirms to within a fifth of a cent at 500
steps. Use the tree when one of those assumptions breaks.

| Situation | Model |
|---|---|
| European exercise, continuous price process, no jumps | `black-scholes` |
| Early exercise is genuinely on the table | `binomial` with `"american": true` |
| Underlying value jumps rather than drifting | `binomial`, or a jump model outside this toolkit |
| An American put, or any option on an asset paying out cash | `binomial` |

Early exercise is the rule for real options rather than the exception, because a firm takes
a project the moment waiting stops paying. A European formula cannot represent that choice
and will understate the option.

```bash
echo '{"spot": 100, "strike": 100, "time_to_expiry": 1, "volatility": 0.3,
       "riskfree_rate": 0.05, "steps": 200, "option_type": "put", "american": true}' \
  | python3 resources/options.py binomial
```

That returns 9.863. The same put priced European is 9.354, so the right to exercise early
is worth about half a point, roughly 5% of the option. For a call on an asset with no
payout the premium is zero, since exercising early only surrenders time value.

Choose `steps` by watching the answer settle. The value oscillates at low step counts and
converges from there: 9.969 at 25 steps, 9.856 at 100, 9.863 at 200, 9.867 at 500. A few
hundred steps is enough for most work, and the cost grows with the square of the count. If
the script refuses to run because the risk-neutral probability falls outside [0, 1], the
volatility is too low relative to the rates for the step size — raise `steps`.

The tree is also the bridge to decision-tree analysis. A binomial tree and a capital
budgeting decision tree have the same shape. They differ in the discount rate, not the
logic. Where the pricing test fails but the option is real, build the decision tree
instead. Do not build both and add them together.

## Employee options

Outstanding employee options reduce value per share. The reason is not dilution as such.
Options are exercised only when they are in the money, so the firm issues shares below the
prevailing price, and existing shareholders pay the difference. Options also matter before
exercise, because today's value must already carry the probability and cost of exercise
later.

Three methods are in circulation. Two are biased in a predictable direction.

| Method | Formula | XYZ result | Bias |
|---|---|---|---|
| Diluted share count | equity / (shares + option shares) | $9.09 | Too low. Ignores the cash exercise brings in. |
| Treasury stock | (equity + strike proceeds) / diluted shares | $10.00 | Too high. Ignores the options' time premium. |
| Option value drag | (equity − option value) / actual shares | $9.46 | Consistent. Sits between the other two. |

The treasury-stock shortcut is what accounting uses for diluted earnings per share, which
is why it keeps appearing in valuations. Look at the XYZ column: a firm grants 10 million
at-the-money options on a $10 stock and the treasury method says value per share is
unchanged at $10.00. That cannot be right. Options at the money have real time value, and
someone paid for them. The method also mishandles out-of-the-money options in both
directions. Include them and the strike proceeds get added while the value does not, which
perversely raises value per share. Exclude them and you have declared time value to be
zero.

So value the options and subtract them as a separate claim. That is what
`employee-options` does.

### Why the calculation has to iterate

Exercise creates new shares. New shares lower the value of every share. A lower share value
lowers the option's own payoff. So the underlying that belongs in the pricer is not the
share value today but a diluted one:

    adjusted spot = (equity value + total option value) / (shares + options)

The total option value appears on both sides. There is no closed-form solution, so the
script starts from an undiluted guess and iterates to a fixed point. Convergence takes
under a dozen passes and the output reports `iterations` and `converged`.

```bash
echo '{"equity_value": 1000, "shares_outstanding": 100, "options_outstanding": 10,
       "average_strike_price": 10, "average_time_to_expiry": 10,
       "volatility": 0.40, "riskfree_rate": 0.04}' \
  | python3 resources/options.py employee-options
```

XYZ has equity of $1,000m and 100 million shares, so $10.00 per share before the grant.
Ten million at-the-money options with a $10 strike and ten years to run, at 40%
volatility, converge to an adjusted spot of $9.584 and a value of $5.423 per option. The
total claim is $54.2m, leaving $945.8m of equity in common stock and $9.46 per share. The
grant cost shareholders 5.4%, not the 10% a share-count adjustment would suggest and not
the zero the treasury method reports.

### Choosing the inputs

**Which equity value.** The `equity_value` field sets the underlying. Passing share count
times the current market price reproduces the published models and keeps the option value
anchored to something observable. Passing your own DCF equity value keeps the valuation
internally consistent, at the cost of making the option value move with your assumptions.
The two answers diverge exactly when you disagree with the market, which is when it
matters. Pick one, say which, and recompute the options whenever the share value changes.

**Maturity.** Use expected life, not contractual life. Employees exercise early and often,
and Black-Scholes is a European model. Shortening the maturity is the standard proxy for
that behaviour. A ten-year grant exercised on average in six years takes six.

**Volatility.** Take the stock's own history, then adjust downward if the firm is maturing.
A large option pool relative to shares makes the answer sensitive to this input.

**Vesting and tax.** The script does not apply either. Multiply `total_option_value` by the
probability of vesting when a material share of the pool is unvested. Multiply by
`(1 − marginal tax rate)` when exercise creates a deduction for the firm — and only then.

**Repricing.** If the plan allows the strike to be reset after a price fall, the option is
worth more than the model says, and the extra comes straight out of shareholders' pockets.
Note it even if you cannot price it.

### What not to do afterwards

Subtract the option value and divide by **actual** shares outstanding. Doing both — netting
out the option value and using a diluted count — charges shareholders the same cost twice.

Options already granted are a claim on existing equity, so they belong in the bridge.
Options expected to be granted in future are compensation, so they belong in forecast
operating expenses. Never put the same grant in both places, and do not add back
stock-based compensation as a non-cash charge.

## Equity as a call option on the firm

Shareholders own a residual claim protected by limited liability. If firm value at the
debt's maturity exceeds what is owed, they keep the difference. If it falls short, they
hand over the keys and lose no more than their stake. That payoff is
`max(firm value − debt owed, 0)`, which is a call option struck at the face value of debt
and expiring when the debt matures.

This is why the stock of an insolvent company still trades. A DCF says the firm is worth
$800m against $1,000m of debt, so the equity is worth nothing. The option model disagrees.
Firm value is volatile and the debt is not due yet. There is still a path where the assets
recover past $1,000m, and shareholders capture all of the upside on that path while bearing
none of the extra downside.

```bash
echo '{"firm_value": 800, "face_value_of_debt": 1000, "debt_maturity": 5,
       "firm_value_volatility": 0.40, "riskfree_rate": 0.05}' \
  | python3 resources/options.py equity-as-option
```

Equity is worth $283m even though the firm owes $200m more than it is worth. The implied
value of the debt is the remainder, $517m, and the yield lenders are demanding on that is
14.1%. The probability of default, read off `1 − N(d2)`, is 66%. All of these come from one
calculation, which is a useful discipline: an equity value you like and a default
probability you refuse to believe cannot both be kept.

**When to reach for this.** Two conditions together. Earnings are negative because of debt
rather than because the business is young, and market-value debt to capital is above 50%.
Below that threshold the ordinary DCF is the better answer. Run the DCF first regardless —
it is where `firm_value` comes from.

**Risk shifting falls out of the model.** Raise `firm_value_volatility` from 0.40 to 0.80
and equity rises from $283m to $507m while the implied debt value drops from $517m to
$293m. Firm value has not changed. Volatility alone moved $224m from lenders to
shareholders. The model explains three things at once. Managers of a distressed firm take
gambles their lenders hate. Lenders write covenants to stop them. And shareholders
sometimes fight a rescue that reduces risk, because it hands their option value back to the
lenders.

**Inputs for this subcommand:**

| Field | What it is |
|---|---|
| `firm_value` | DCF value of the operating assets plus cash — the whole firm, not the equity |
| `face_value_of_debt` | Aggregate principal owed, not the market value of the debt |
| `debt_maturity` | Weighted-average maturity or duration; the model collapses a debt ladder into one zero-coupon claim |
| `firm_value_volatility` | Standard deviation of the log of firm value; a weighted blend of equity and debt volatility is the usual proxy |
| `payout_ratio` | Cash paid to all claimholders as a share of firm value, since that value leaks away before the option matures |
| `shares_outstanding` | Optional; adds a value per share to the output |

Firm value volatility is the weakest input in the calculation. Vary it and report the
range rather than a single figure.

**Treat the answer as one branch.** The option approach and the probability-weighted
distress approach are alternative ways to price the same survival risk. Use one. Do not
also raise the discount rate for failure risk, and do not shrink the cash flows for it.

## Implied volatility

`implied-vol` inverts the pricer by bisection. Feed it an observed option price and it
returns the volatility that reproduces it, along with the recomputed price so you can see
the fit.

```bash
echo '{"spot": 100, "strike": 100, "time_to_expiry": 1, "riskfree_rate": 0.05,
       "option_price": 14.23, "option_type": "call"}' \
  | python3 resources/options.py implied-vol
```

Two uses. Traded warrants or listed options on the company give a market view of volatility
that beats a historical estimate for pricing employee options. And running an implied
volatility on your own equity-as-option inputs shows what the market believes about firm
value volatility, which is often more informative than arguing about your own proxy.

The search covers volatilities from near zero up to 500%. A price outside that range makes
the script stop and report the achievable span, which almost always means the spot, strike
or maturity is wrong.

## Handoffs to the other engines

| You need | Get it from | Field |
|---|---|---|
| Equity value before options | `dcf-valuation-engine` — `dcf.py value` | `bridge.equity_value` |
| Firm value for `equity-as-option` | `dcf-valuation-engine` — `dcf.py value` | `value_of_operating_assets` plus cash |
| Option value back into the bridge | this toolkit — `employee-options` | `total_option_value` → dcf.py `bridge.employee_options_value` |
| Weighted-average debt maturity | `cost-of-capital-toolkit` — `costofcapital.py mv-debt` | the `maturity` you passed in |
| Riskfree rate matched to the option's life | `cost-of-capital-toolkit` | the currency-matched riskfree rate |

The equity bridge is circular in the same way the dilution loop is: the DCF needs an option
value and the option value needs an equity value. One pass is enough in practice. Take
`bridge.equity_value` from a DCF run with `employee_options_value` set to zero, price the
options, then re-run the DCF with the answer in place.

Run `valuation-consistency-checks` over the finished artifacts before accepting anything.

## Sanity checks before quoting a number

Six inputs drive every option value, and their directions are facts rather than estimates.
Check each against the table before believing an output.

| Input | Call value | Put value |
|---|---|---|
| Value of the underlying | rises | falls |
| Volatility | rises | rises |
| Dividend or payout yield | falls | rises |
| Strike price | falls | rises |
| Life of the option | rises | rises |
| Riskfree rate | rises | falls |

Volatility raises both calls and puts, because the downside is truncated either way. A real
option value that falls when you raise volatility means a sign error or a mistaken input.

Two more checks. The `time_value` field should be positive for any live option; a European
option can show negative time value only if the underlying pays out heavily, and it usually
signals a wrong yield. And a deep out-of-the-money real option can still be worth a lot,
which is exactly why the exclusivity test matters so much.

## Common failures

| Symptom | Cause |
|---|---|
| Real-option premium looks implausibly large | `dividend_yield` left at zero on a long-dated option, so no cost of delay is charged |
| Patent or licence value survives no scrutiny | Test 2 never run; competitors can exploit the same contingency, so the option is worth zero |
| Firm value equals DCF value plus the patent option | Double counting — the patent's growth is still inside the DCF |
| Employee option value looks too high | Undiluted spot used, or contractual maturity used where expected life belongs |
| Value per share drops by the full grant percentage | Option value subtracted and diluted share count used together |
| Grant appears to cost shareholders nothing | Treasury-stock method, which ignores time value |
| Distressed equity worth zero when the stock clearly trades | DCF applied where the equity is an option; leverage above 50% of capital needs `equity-as-option` |
| Default probability from `equity-as-option` looks absurd | `firm_value_volatility` is an equity volatility rather than a firm-value volatility |
| Distress charged twice | Option approach used alongside a failure probability, or alongside a raised discount rate |
| Binomial refuses to run | Risk-neutral probability outside [0, 1]; volatility too low for the rates at that step size — raise `steps` |
| American call equals the European call | Correct, when the underlying has no payout; early exercise only gives up time value |
| Implied volatility not reachable | The observed price is impossible for those inputs; check spot, strike and maturity |
| Stack trace mentioning a KeyError | A required field is missing from the payload; run the subcommand with `--example` to see the full shape |
