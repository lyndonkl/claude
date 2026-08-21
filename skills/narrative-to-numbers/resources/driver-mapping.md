# The driver mapping in detail

Every claim moves one lever. Every lever is chosen against a reference class. This file
holds the mapping, the reference menus, the terminal defaults, and what overriding each
default requires you to say out loud.

The target is the `dcf-valuation-engine` payload. Check the shape before you write it:

```bash
python3 <skills>/dcf-valuation-engine/resources/dcf.py value --example
```

---

## 1. How a driver is stated

Three forms, so a fading assumption stays one line.

| Form | Syntax | Use it for |
|---|---|---|
| Constant | `"sales_to_capital": 2.0` | a ratio you expect to hold |
| Per-year list | `"revenue_growth": [0.4, 0.3, 0.2, 0.1, 0.05]` | a path you computed elsewhere |
| Glide | `{"start": 0.40, "end": 0.03, "converge_by": 8}` | growth, margin, tax, cost of capital |

A glide moves linearly from start to end by the named year, then holds. It is usually what
you want. Real companies converge toward their industry. A company growing 40% in year 1
and 40% in year 10 is almost always a modelling error rather than a forecast.

---

## 2. Lever by lever

### Total market and market share → `base_revenue`, `revenue_growth`

The engine consumes a revenue path, not a market times a share. Do the multiplication
yourself and hand over the implied growth rate:

```
target revenue_N = total market_N x market share_N x revenue slice
total market_N   = total market_0 x (1 + market growth)^N
revenue_growth   = (target revenue_N / base_revenue)^(1/N) - 1
```

Keep the market size, its growth rate, the share and the slice in `drivers.json` as the
story record. Those are the numbers a reader argues with. The CAGR is only what the engine
eats.

Set the lever from an **end-state revenue level**, never from a rate. Picking "35% growth"
hides the dollars. Picking "$300 billion of revenue in 2030" exposes them, and forces the
question of who loses that revenue.

Taper the rate as the base grows rather than holding it flat and cliffing it to the
terminal rate. A glide with `converge_by` equal to `forecast_years` does this.

**Reference menu — an end-state revenue target for Tesla, November 2021:**

| Choice | 2030 revenues | Implied CAGR |
|---|---|---|
| BMW-like | $100 billion | 12.00% |
| Ford and Honda-like | $150 billion | 18.00% |
| Daimler-like | $200 billion | 22.50% |
| Toyota and VW-like | $300 billion | 30.00% |
| 20% of the auto market | $500 billion | 40.00% |
| Direct input (chosen) | — | 35.00% |

The menu is the point. A growth rate chosen against named companies is a claim about
becoming one of them.

### Pricing power and cost structure → `operating_margin`

State a **target margin** anchored on mature firms with the same business model, and say
which percentile of that class you picked. Never anchor on a loss-making current margin.
Then converge to it:

```
margin_t = target - (target - base) / Y x (Y - t)   for t <= Y
```

`Y` is `operating_margin.converge_by`. It is a claim about how fast scale arrives.

**Reference menu — target operating margin, Tesla, November 2021:**

| Choice | Target margin |
|---|---|
| Auto industry first quartile | −5.87% |
| Auto industry median | 3.01% |
| Auto industry third quartile | 7.52% |
| Technology median | 10.25% |
| Software | 21.24% |
| FAANG aggregate | 19.87% |
| Direct input (chosen) | 16.00% |

Choosing a margin far outside the reference class is allowed. It is now an explicit claim
about pricing power, and the prose has to carry it.

Watch the growth-margin trade-off. Strategies that push for more growth generally deliver
less margin. Scaling up is not an automatic cure for losing money — costs have to grow
slower than revenues, and that is not guaranteed.

### Capital intensity → `sales_to_capital`

```
reinvestment_t = (revenue_t - revenue_{t-1}) / sales_to_capital_t
FCFF_t         = EBIT(1-t)_t - reinvestment_t
```

This single ratio bundles net cap ex, acquisitions, capitalized R&D and working capital.
Do not subtract a working-capital change again anywhere — that is double-count register
entry F13.

The ratio may vary by phase. Asset-light early and heavier later is common when capacity
already exists; the reverse is common when a plant has to be built first.

**Reference menu — sales to invested capital, Tesla, November 2021:**

| Choice | Sales to capital |
|---|---|
| Auto industry first quartile | 0.75 |
| Auto industry median | 1.37 |
| Auto industry third quartile | 2.42 |
| Technology median | 1.51 |
| Software | 2.30 |
| FAANG aggregate | 1.27 |
| Direct input (chosen) | 4.00 |

A ratio well above the industry quietly assumes growth is nearly free. The marginal ROIC
will show it. Tesla's 4.00 against a 1.37 median produced a marginal ROIC of 51.66%.

### Tax → `tax_rate`, `net_operating_loss_carryforward`

The standard path holds the effective rate for the near years, then ramps to the marginal
rate. State both rates. Where accumulated losses exist, pass the carryforward and let the
engine shelter income until it burns.

The rate used here must be the rate used in the after-tax cost of debt. In zero-tax years
the debt tax shield is zero as well.

### Operating risk and maturity → `cost_of_capital`, `terminal.cost_of_capital`

Set the initial rate from the market's own distribution of costs of capital, not from a
theoretical construct. It is what investors currently demand.

**Reference menu — initial cost of capital, November 2021:**

| Choice | Rate |
|---|---|
| Automobile median | 5.24% |
| Technology median | 7.16% |
| All companies, first quartile | 4.57% |
| All companies, median | 5.90% |
| All companies, third quartile | 7.01% |
| Direct input (chosen) | 6.00% |

Two cautions. The cost of capital is not among the top levers driving value, so do not
spend the day on it. And the number itself belongs to `cost-of-capital-toolkit` when the
valuation is a full pipeline run rather than a quick story test — this menu is a sanity
check on that output, not a replacement for it.

Uber's path is the shape to copy for a young firm: 12% for years 1–5, declining to 8% by
year 10 as the business matures.

### Survival → `failure`

```json
"failure": {"probability": 0.20, "proceeds_basis": "book_value",
            "book_value_of_capital": 4000, "proceeds_percent": 0.5}
```

```
value = going-concern value x (1 - p) + distress proceeds x p
```

Mandatory for young firms and for distress markers. A going-concern DCF alone prices only
the branch where the company survives.

**Reference menu — probability of failure:**

| Situation | p |
|---|---|
| No realistic chance of failure | 0% |
| Marginal profitability, high debt | 10% |
| Money loser, high debt | 20% |
| Low growth, money loser, high debt | 50% |

Sector survival rates anchor the choice, and they range widely.

| Sector | Long-run survival rate |
|---|---|
| Management of companies and enterprises | 35.2% |
| Utilities | 28.4% |
| Health care and social assistance | 19.9% |
| Wholesale trade | 14.0% |
| Transportation and warehousing | 12.9% |
| Information | 11.5% |
| All-sector average | 16.6% |

Using the all-sector average when the sector rate is available throws away the spread.

Never apply a failure probability **and** a distress-adjusted discount rate. That is
double-count register entry F10.

### The bridge → `bridge`

Debt, cash, minority interests, non-operating assets, employee option value, share count,
and the current price for the gap calculation. The narrative rarely sets these — the
statement work does. Two narrative-side judgments do land here: how much cash is operating
rather than excess, and whether cash held by a value-destroying management is worth face
value.

Value employee options with `option-valuation-toolkit` and pass the result in. Do not
inflate the share count instead, and do not subtract option value and then divide by
diluted shares.

---

## 3. Terminal defaults, and what overriding one costs you

Each default is overridable. Each override is a claim that has to appear in the prose.

| Default | Value | Override requires |
|---|---|---|
| Terminal growth | the riskfree rate in the valuation currency | nothing — it is a ceiling, and going lower is often right |
| Terminal cost of capital | a mature company's rate, riskfree plus about 4.5% | an argument that this firm stays riskier or safer than mature peers |
| Terminal return on capital | equal to the terminal cost of capital, so no excess returns | a named barrier to entry that survives in perpetuity |
| Terminal reinvestment rate | computed as `g / ROC` | never override; the engine computes it |
| Failure probability in the terminal phase | zero | a firm that could still fail after ten years is not in a stable phase |
| Tax rate | migrated to the marginal rate, no loss carryforward left | a durable structural tax advantage |

A mature firm inside an economy that also contains high-growth firms probably grows below
the aggregate. Setting terminal growth *below* the riskfree rate needs no special defence.

The terminal return on capital is the override that matters most, and the one most often
left on by accident. Tesla's model set it to 15% against a terminal cost of capital of
6.06%, justified by "cost of entry will limit competition". That sentence is the whole
defence, and without it the model grants a perpetual moat by default.

---

## 4. The completeness check

Two counts, both mechanical, both required to be zero before the model is trusted.

```
model inputs with no story sentence  = 0
story claims with no driver          = 0
```

A claim mapping to two drivers is double counted. A claim mapping to none is decoration,
and should be deleted or moved to the option layer.

The report layout enforces the discipline on its own: narrative in prose at the top, the
driver assumptions in the middle with a **link to story** note on every row, and the value
bridge at the bottom.
