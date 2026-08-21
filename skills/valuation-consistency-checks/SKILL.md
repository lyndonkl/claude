---
name: valuation-consistency-checks
description: Checks a finished valuation for internal consistency across its artifacts — currency agreement between cash flows and discount rate, terminal growth against the riskfree ceiling, reinvestment that pays for the growth assumed, perpetual excess returns, capital weights and beta range, equity bridge arithmetic, tax rates, and the hard constraints a company's type imposes. Grades each finding ERROR, WARN or INFO and exits 1 on any error, so it can gate a pipeline. Use before accepting a DCF, when reviewing someone else's model, when a value looks too high, or when checking terminal value assumptions, growth-versus-reinvestment consistency, currency consistency, or an equity bridge that does not tie.
---

# Valuation consistency checks

Most bad valuations contain no wrong number. They are internally inconsistent. Cash flows
sit in one currency and the discount rate was built in another. Growth appears that nobody
paid for. Terminal growth runs above the economy's. A method the company's own type rules
out was used anyway.

Each of those looks defensible when you stare at it alone. Only a check that reads several
artifacts at once catches them. That is what this script does.

Treat it as a loop, not a report:

```
run it  ->  fix what it flags  ->  run it again  ->  no errors left
```

You are done when the run comes back with zero errors and every warning has a written
defence. A warning you cannot defend is an error you have not admitted yet.

## The script

`resources/validate.py` — pure standard library, no installation needed. It reads JSON
files by path and prints findings.

```bash
python3 resources/validate.py --capital capital.json --dcf dcf.json --classification cls.json
python3 resources/validate.py --dcf dcf.json --capital capital.json --quiet
python3 resources/validate.py --dcf dcf.json --capital capital.json --json
```

| Flag | Effect |
|---|---|
| `--mandate` `--classification` `--capital` `--forecast` `--dcf` `--relative` | artifact paths |
| `--quiet` | drop the INFO and SKIP lines, show only what needs work |
| `--json` | machine-readable findings, plus `error_count` and `passed` |

Exit code is 0 when nothing reached ERROR, and 1 otherwise. Nothing else changes the exit
code — warnings never fail the run.

## The artifacts it reads

Pass any subset. Every check whose inputs are missing is skipped and printed as a `SKIP`
line with the reason, so the gate is useful part-way through an analysis. Running with only
a cost of capital artifact is a legitimate thing to do.

| Flag | What it is | Where it comes from | Fields read |
|---|---|---|---|
| `--mandate` | the brief: what is being valued, in what currency, as of when | you write it | `currency` |
| `--classification` | the company's type and the hard stops that follow | you write it | `constraints[]` |
| `--capital` | the discount rate build | `cost-of-capital-toolkit`, `wacc` subcommand | `currency`, `riskfree_rate`, `levered_beta`, `weights{}` |
| `--forecast` | the driver forecast feeding the DCF | your driver file | `currency` |
| `--dcf` | the valuation itself | `dcf-valuation-engine`, `value` subcommand | `terminal{}`, `forecast[]`, `bridge{}`, `value_per_share`, `terminal_value_share_of_total`, `method`, `failure.probability`, `currency` |
| `--relative` | the multiples work, if any | `relative-valuation-toolkit` | `multiples[].multiple` |

### Building the capital artifact

The `wacc` subcommand of `cost-of-capital-toolkit` returns `weights` and `currency` but not
the riskfree rate or the beta, because those were its inputs. Merge the input payload and
the output into one file:

```json
{
  "currency": "USD",
  "riskfree_rate": 0.0275,
  "levered_beta": 1.0013,
  "wacc": 0.0781,
  "weights": {"equity": 0.8988, "debt": 0.1012, "preferred": 0.0}
}
```

`riskfree_rate` may also sit at `cost_of_equity.riskfree_rate`, and the beta may sit at
`beta.levered`. Either nesting is read.

### Building the DCF artifact

The output of `dcf.py value` is already the right shape, with one gap: it carries no
`method` field. Add one so the constraint check can see which model was used.

```bash
python3 ../dcf-valuation-engine/resources/dcf.py value --in drivers.json > dcf.json
# then add "method": "fcff" (or "fcfe", "ddm", "excess_return") to dcf.json
```

Set `currency` in the DCF drivers file. It is copied through to the result, and without it
the currency check has nothing to compare.

### Writing the classification artifact

Nothing produces this. You write it after deciding what kind of company this is. It records
the hard stops that the company's type imposes, so that a later run cannot quietly ignore
them.

```json
{
  "company": "Deutsche Bank",
  "buckets": ["financial-service"],
  "constraints": [
    {"rule": "no-fcff-valuation", "because": "debt is raw material for a bank"},
    {"rule": "require-failure-probability", "because": "crisis bank, equity can be wiped"}
  ]
}
```

Constraints may be plain strings or objects with a `rule` key. Three rule names are
enforced:

| Rule | Fires when | Set it for |
|---|---|---|
| `no-fcff-valuation` | the DCF `method` contains `fcff` | banks, insurers, anything where debt is raw material |
| `require-failure-probability` | `failure.probability` is absent or zero | young firms, distressed firms, high leverage, political risk |
| `no-earnings-multiple` | a relative valuation used PE, P/E or EV/EBIT | negative earnings, or a cycle trough |

Any other rule name is recorded and counted but not enforced. That is deliberate: writing
down a constraint the script cannot test is still better than not writing it down.

## The severity model

| Severity | Meaning | What you owe |
|---|---|---|
| `ERROR` | an internal contradiction, not a matter of taste | a fix; the exit code is 1 until it is gone |
| `WARN` | defensible but unusual, and usually a sign of something | a written defence, or a fix |
| `INFO` | the check ran and the valuation passed it | nothing; read it as confirmation |
| `SKIP` | an input was missing, so the check never ran | supply the artifact if the check matters |

An ERROR means the model contradicts itself. There is no assumption set under which both
halves are true at once. Terminal growth above the riskfree rate is not aggressive, it is
inconsistent with the rate you already chose.

A WARN means the model is possible but is making a claim you have not stated out loud. The
right response is usually a sentence in the write-up, not a change to the numbers.

## What each check does, and what to do about it

### currency — ERROR

Compares the `currency` field across the mandate, capital, forecast and DCF artifacts.
Skipped when fewer than two of them declare one.

Currency is a measurement unit, not a value driver. A company valued in reais, in dollars
and in francs must come out to the same number once converted. That holds only when cash
flows and the rate that discounts them live in the same currency, because a currency's
riskfree rate carries its own expected inflation.

**Fix:** pick one currency and rebuild the other side. To move the rate rather than the
cash flows, use `convert-rate` in `cost-of-capital-toolkit`, which applies the inflation
differential. Do not convert the finished value at the spot rate and call it done.

### terminal_growth — ERROR

Compares `terminal.growth_rate` against `riskfree_rate` from the capital artifact.

The riskfree rate is expected inflation plus the expected real rate. Nominal economy growth
is expected inflation plus expected real growth. The two share the inflation term and their
real terms converge in a mature economy, so the riskfree rate is the working ceiling on
perpetual nominal growth. Above it, the company eventually becomes the economy.

**Fix:** lower terminal growth to the riskfree rate or below. Setting it lower is often
right — a mature firm in an economy that still contains young firms probably grows slower
than the aggregate. Disney's November 2013 valuation set 2.5% against a 2.75% riskfree
rate. A negative rate is fine too: Heineken in euros used −0.5% terminal growth against a
−0.5% riskfree rate.

If terminal growth genuinely has to be higher, the riskfree rate is the thing that is
wrong, and probably in the wrong currency.

### terminal_discount_rate — ERROR

Fires when `terminal.cost_of_capital` is at or below `terminal.growth_rate`.

The perpetuity has a zero or negative denominator, so it returns no finite number.

**Fix:** this is arithmetic, not judgment. Either growth is too high or the terminal rate is
too low. A terminal cost of capital below the terminal growth rate usually means the fade
schedule pushed the rate down too far.

### terminal_reinvestment — ERROR

Checks that `terminal.reinvestment_rate` equals `terminal.growth_rate / terminal.return_on_capital`.

Growth has to be bought. In the stable phase there is no efficiency growth left to harvest,
so reinvestment is the only remaining source of growth, and the identity binds exactly. The
classic sleight of hand is to assume capital spending merely offsets depreciation, assume
no working capital need, and then apply positive real growth anyway. Zero net reinvestment
is consistent only with roughly zero real growth.

An ERROR also fires when the required rate exceeds 100%, which says the firm must raise
capital forever just to stand still.

**Fix:** do not set growth and reinvestment independently. Choose terminal growth and a
perpetual return on capital, then let the reinvestment rate follow. Disney: 2.5% / 10% =
25%. Baidu: 3.5% / 15% = 23.33%. Heineken with negative growth: −0.5% / 5% = −10%, meaning
the firm releases capital as it shrinks. The `value` subcommand of `dcf-valuation-engine`
computes this rather than accepting it, so an error here usually means the DCF artifact was
edited by hand after the run.

### terminal_excess_return — WARN

Compares `terminal.return_on_capital` with `terminal.cost_of_capital`. Warns when the spread
is wider than 2 points in either direction.

A return above the cost of capital in perpetuity is a claim that competitors never arrive.
That claim can be true, and Disney's valuation made it — terminal return 10% against a
7.29% terminal cost of capital, on the argument that brand advantages would not have fully
dissipated. But it needs a named barrier to entry, not a spreadsheet default.

A return more than 2 points below the cost of capital is the mirror image. Growth then
destroys value, and the faster the firm grows the more it destroys.

**Fix:** either name the moat in the write-up, or set the terminal return equal to the
terminal cost of capital. Setting them equal makes growth exactly value-neutral, which is
the honest default. When the spread is negative and intended, terminal growth should be
zero or negative to match.

### terminal_value_share — WARN

Warns when `terminal_value_share_of_total` exceeds 90%.

Above that, the answer rests almost entirely on assumptions beyond the forecast horizon,
and the explicit forecast is decoration.

**Fix:** lengthen the explicit forecast until the company has actually reached maturity
inside it. Tie the length to how long the competitive advantage lasts, not to the number of
columns in a template. If the share stays high with a long horizon, the company may be an
option rather than a going concern, and a DCF is the wrong tool.

### capital_weights — ERROR

Checks that the values in `capital.weights` sum to 1, within 1e-4.

**Fix:** rebuild the weights at market values. Weights that miss usually mean a preferred
stock component was dropped, or that book equity crept in where market capitalization
belongs.

### beta_range — ERROR and WARN

A levered beta at or below zero is an ERROR: equity risk cannot be zero for an operating
company. A beta outside 0.3 to 3.0 is a WARN.

**Fix:** for the WARN, check the comparables and the debt-to-equity ratio used to relever.
A very safe or very leveraged firm can sit outside the band legitimately. A regression beta
usually cannot — use a bottom-up beta from `cost-of-capital-toolkit`.

### growth_reconciliation — WARN

For each forecast row it computes `reinvestment / invested_capital` and compares it against
that year's `revenue_growth`. It reports the widest gap, and warns above 2 percentage
points.

This is the fundamental growth identity, `g = reinvestment rate × return on capital`,
rearranged. When revenue grows faster than the capital base, the model is assuming
efficiency growth — the same assets earning a better return. That is real and it is the
cheapest growth there is, but it is a one-off improvement spread over a transition, not a
permanent source.

**Fix:** decide which of the two you meant. If efficiency growth is intended, say so and
say when it stops. If not, lower the sales-to-capital ratio so growth costs what it should.
A gap running the other way means capital is being spent with no growth to show for it.

Two notes on reading this one. The check compares against **revenue** growth, so a
deliberately expanding margin will open a gap that is not an error. And `invested_capital`
in the DCF rows is end-of-year, while the identity wants start-of-year capital, which
understates implied growth by roughly 20 basis points. Neither effect is large enough to
explain a wide gap.

### equity_bridge — ERROR

Recomputes the walk and compares it with the reported `equity_value`:

```
equity value = operating assets − debt − minority interests + cash + non-operating assets
```

The `less_debt` and `less_minority_interests` fields hold positive magnitudes and are
subtracted.

**Fix:** the arithmetic is deterministic, so a mismatch means a line item was edited without
the total following. This is where most disputes between competent analysts actually
happen, so it is worth getting exactly right. Beyond arithmetic, watch for the double
counts the check cannot see: brand value added on top of cash flows that already reflect
brand pricing power, or goodwill added as an asset when it is an accounting residual.

### value_per_share — ERROR

Checks that `bridge.equity_in_common_stock / bridge.shares_outstanding` equals
`value_per_share`.

**Fix:** if you subtracted employee option value in the bridge, divide by actual shares
outstanding. Dividing by diluted shares as well counts the options twice. Value the options
properly with `option-valuation-toolkit` and pass the result in.

### tax_rate — ERROR

Flags any forecast year whose `tax_rate` falls outside 0 to 1.

**Fix:** usually a percentage entered where a decimal belongs. A genuinely negative
effective rate belongs in the loss carryforward, which `dcf-valuation-engine` handles
through `net_operating_loss_carryforward`.

### constraints — ERROR

Enforces the three rules listed above and reports how many constraints were recorded.

**Fix, by rule:**

- `no-fcff-valuation` fired. For a bank, debt is raw material rather than financing, so
  operating and financing decisions cannot be separated and there is no meaningful cost of
  capital. Value equity directly: a dividend discount model by default, or an FCFE model
  against regulatory capital when payout no longer reflects capacity.
- `require-failure-probability` fired. A going-concern DCF prices only the branch where the
  company survives. Add an explicit probability and a distress value rather than raising the
  discount rate, which double counts. JC Penney: a 20% failure probability with proceeds at
  50% of book took operating assets from $4,841m to $4,357m.
- `no-earnings-multiple` fired. A multiple of negative or trough earnings is meaningless.
  Use revenue or book value multiples, or normalize the earnings first and say so.

## Thresholds

All of them sit as named constants at the top of `resources/validate.py`. None is settable
from the command line, on purpose — a gate you can loosen per run is not a gate.

| Constant | Value | Why |
|---|---|---|
| `TERMINAL_VALUE_SHARE_WARN` | 0.90 | above this the explicit forecast is not driving the answer |
| `BETA_LOW`, `BETA_HIGH` | 0.3, 3.0 | outside this band betas are possible but rare |
| `ARITHMETIC_TOLERANCE` | 1e-6 | for identities that should tie exactly, allowing for JSON rounding |
| `GROWTH_RECONCILIATION_TOLERANCE` | 0.02 | implied growth never matches to the decimal; flag only real gaps |
| excess-return spread | ±0.02 | inside 2 points, the terminal return is near the competitive default |

## A run, and the loop it starts

A Disney-shaped valuation, run against its own cost of capital artifact:

```
[WARN ] terminal_excess_return   The terminal period assumes a return on capital 2.71
                                 percentage points above the cost of capital, forever...
[WARN ] growth_reconciliation    In year 1 the forecast grows revenue 6.4% while the
                                 reinvestment and return assumed there support about 4.2%...
[INFO ] currency                 All artifacts agree on USD.
[INFO ] terminal_growth          Terminal growth 2.50% is within the riskfree ceiling 2.75%.
[INFO ] terminal_reinvestment    Terminal reinvestment of 25.0% of income is consistent
                                 with 2.50% growth at a 10.00% return.
[INFO ] terminal_value_share     Terminal value is 63% of total value.
[INFO ] equity_bridge            The equity bridge adds up.

0 error(s), 2 warning(s).
```

Exit 0, so the gate passes. The two warnings are the whole analytical argument. The first
says the model claims Disney out-earns its cost of capital forever, which the write-up has
to justify by naming the brand. The second says revenue grows faster than the capital base,
so returns drift up over the forecast, which has to be either intended or removed.

Break the same set deliberately — shift the DCF currency to EUR, lift terminal growth to
3.5% without touching reinvestment, add 5,000 to the equity value, and record a
`require-failure-probability` constraint — and the run returns five errors and exit 1.

That round trip is worth doing once on your own artifacts. It confirms the gate is reading
the files you think it is reading, which matters because of the trap below.

## Wiring it into a pipeline

```bash
python3 resources/validate.py \
  --mandate mandate.json --classification classification.json \
  --capital capital.json --forecast forecast.json --dcf dcf.json \
  --quiet || { echo "valuation gate failed"; exit 1; }
```

For a machine consumer, `--json` returns `findings`, `skipped`, `error_count` and a boolean
`passed`. Store the JSON alongside the valuation. A finding list with zero errors and two
defended warnings is a record that the checks ran, which is worth more later than the memory
that they did.

One trap. A path that does not exist is treated as an artifact that was not supplied. The
run then skips every check that needed it and exits 0. A typo in a filename therefore looks
exactly like a clean pass. In a pipeline, test that each file exists before calling the
validator, and read the `SKIP` lines rather than only the exit code.

## What it does not check

The gate tests internal consistency. It has no view on whether your assumptions are any
good. It cannot tell you that a 22% target margin has never been sustained in the industry,
that the sales-to-capital ratio came from a different business, or that the comparables are
the wrong ones. It will not notice a return on capital inflated by expensed research
spending, because it never sees the accounts.

For those, use `financial-statement-normalization` before the DCF, and the `implied`
subcommand of `dcf-valuation-engine` afterwards. Reverse-engineering the market price into
the growth or margin it already assumes is the check that tests your assumptions against the
world rather than against each other.

## Common failures

| Symptom | Cause |
|---|---|
| Everything reports SKIP and the run exits 0 | wrong path; a missing file is read as a missing artifact |
| `currency` skipped although the DCF has a currency | `currency` absent from the drivers file, so it was never copied into the result |
| `constraints` reports "no classification artifact" | nothing produces that file; write it yourself |
| `no-fcff-valuation` never fires for a bank | the DCF artifact has no `method` field; add one after running `dcf.py value` |
| `terminal_reinvestment` errors on an unedited DCF result | the artifact was hand-edited after the run; re-run the engine instead |
| `growth_reconciliation` warns on every model you build | sales-to-capital set too high, so growth costs less capital than it should |
| `beta_range` errors with a negative beta | an unlevering step ran with a debt-to-equity ratio taken as a percentage |
| `equity_bridge` off by exactly the option value | option value subtracted twice, or the bridge total not refreshed after an edit |
| Gate passes but the value is obviously wrong | consistency is not accuracy; run `implied` and test the assumptions against the industry |
