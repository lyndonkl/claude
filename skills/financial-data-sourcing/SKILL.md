---
name: financial-data-sourcing
description: Maps every input a company analysis needs to where it comes from — filing line items, market data, Damodaran reference datasets, macro series — with units, update frequency, acceptable fallbacks and the consistency rules that bind them. Use when gathering data for a valuation, when an input is missing and a substitute is needed, when deciding whether a user-supplied figure can be accepted at face value, or when checking that figures are internally consistent.
---

# Financial data sourcing

Every number in a valuation comes from somewhere, and the analysis is only as good as the
worst-sourced number in it. This skill is the input contract. It says what to fetch, from
which source, in what units, how stale it may be, whether a user may hand it over directly,
and what to substitute when it cannot be found.

Two consumers depend on it. The `financial-data-collector` agent uses it to fill four
artifacts. The orchestrator's gates `G1_data`, `G3_financials`, `G4_discount_rate` and
`G5_forecast` are predicates over the fields defined here.

This skill does not carry method. It says what must be in hand before a procedure can run.
For how a number is used, follow the concept path cited beside it.

## What you produce

| Artifact | Contents |
|---|---|
| `01-data/raw-financials.json` | Every company field, per period, with `source` and `as_of` on each leaf |
| `01-data/market-data.json` | Every market field, plus the loaded reference-table snapshots with their `as_of` |
| `01-data/sources.md` | One line per source actually used, with retrieval date and document reference; every fallback and stale field listed |
| `01-data/gaps.json` | One entry per attempted field: status, fallback applied, and the stage it constrains |

Collect. Do not compute. Derived quantities belong to the downstream skills:
`financial-statement-normalization` for lease and R&D capitalization, invested capital and
cash flows, and `cost-of-capital-toolkit` for ratings, spreads, betas and WACC. A collector
that quietly computes a ratio has erased the provenance the report needs.

## Source classes

Every field carries exactly one class. The class decides caching, refresh policy and where
blame lands when the number is wrong.

| Class | Code | What it is | Keyed by |
|---|---|---|---|
| Company-specific | CO | This company's filings, its own prices, its own ownership records | ticker + fiscal period |
| Market-wide | MK | A price or rate observed in a market, not attributable to one firm | currency or country + date |
| Reference table | RT | A published lookup, refreshed on a vintage cycle | table name + `as_of` |
| Derived | DV | Computed by the pipeline from the other three | not fetched |

Fetch CO, MK and RT. Never fetch DV. Where a DV field is listed anywhere below, it is
because a later stage treats it as an input and must be able to name its provenance.

The source identifiers used throughout — `F-10K`, `F-LEASE`, `M-PX`, `M-RATING`, `D-ERP`,
`X-FRED` and the rest — are defined in [resources/source-registry.md](resources/source-registry.md).

## Status vocabulary for gaps.json

Every field you attempt resolves to exactly one status.

| Status | Meaning | Effect |
|---|---|---|
| `found` | Retrieved from the named source at the named vintage | none |
| `user` | Supplied by the user, validation passed | record it and flag it in the report |
| `derived` | Computed from other found fields through a stated identity | record the identity |
| `fallback` | Primary source unavailable, documented default applied | must appear in `sources.md` and in the report's assumption list |
| `stale` | Found, but older than the freshness limit | usable, flagged; not allowed for vintage-critical fields |
| `missing` | Not obtainable and no fallback exists | triggers the stage's blocking rule |

One entry per attempted field, shaped like this:

```json
{"field": "lease.commitments", "status": "fallback", "source": "F-LEASE",
 "as_of": "2024-12-31", "applied": "reported IFRS 16 liability used in place of the PV of commitments",
 "constrains": ["B2 lease capitalization", "B4 cost of debt"]}
```

The `constrains` list is what makes the file useful. A gap nobody traced to a stage is a
gap nobody will remember at the point where it bites.

### What a user may supply

Three answers per field, recorded in the tables in the resource files.

- `Y` — accept the user's value as authoritative and record `source: "user"`.
- `Y*` — accept it after the stated validation runs.
- `N` — never accept a bare value. It is derivable, or it must trace to a source.

Some fields are freely user-suppliable. These are the judgments the pipeline cannot make
for itself.

- Mode, company identity, valuation currency, valuation date
- Target operating margin, market size, market-share path, sales-to-capital
- Growth-period length; terminal growth and terminal return on capital, subject to the cap
- Failure probability, recovery rate, bankruptcy-cost percentage, distress severity
- Buyer type, lambda, debt-allocation key, illiquidity route
- Synergy assumptions, rating constraints, peer-set definitions

Seven things are never accepted bare. A statement line with no filing reference. A
rate-table row with no vintage. A WACC, cost of equity or beta given as a single number
without its components. A normalized riskfree rate. A control premium expressed as a
bolt-on percentage. A terminal growth rate above the riskfree rate. A growth rate and a
reinvestment rate set independently of each other.

## The rules that bind every stage

These hold across all sources. A violation is a failure, not a warning.

### Matching

| Rule | Statement | Checked at |
|---|---|---|
| R1 currency | Riskfree rate, equity risk premium, cost of debt, cash flows, growth and terminal growth are all in one currency | G4, G5 |
| R2 claimholder | Equity cash flows go with the cost of equity, firm cash flows with the cost of capital. Return on equity goes with the cost of equity, return on capital with the cost of capital | G4, G6 |
| R3 basis | Nominal cash flows with a nominal rate, real with real. The inflation assumption in the cash flows equals the one used in any currency conversion | G5 |
| R4 time | Every vintage-critical reference table shares one `as_of`, and that `as_of` is inside the freshness limit for the valuation date | G1, G4 |
| R5 debt convention | Gross debt throughout, or net debt throughout. The convention used to lever the beta equals the one in the WACC weights and in the equity bridge | G4, G6 |

R4 stated as a predicate: across
`{D-ERP, D-CTRY, D-SOVSPR, D-RATE1, D-RATE2, D-RATE3, D-SPREAD, D-MULTREG, D-DISTRIB}`,
`max(as_of) − min(as_of) ≤ 3 months` and `valuation_date − min(as_of) ≤ 12 months`.

Concepts: `knowledge/concepts/cost-of-equity/cost-of-equity-assembly.md`,
`knowledge/concepts/cost-of-debt-capital/hurdle-rate-choice.md`,
`knowledge/concepts/cost-of-debt-capital/net-debt-vs-gross-debt.md`.

### Single count

Ten versions of one error. Each names a quantity that may enter the valuation exactly once.

| Rule | Counted once through |
|---|---|
| N1 | The interest tax shield lives in the `(1−t)` factor of the discount rate, never also in FCFF |
| N2 | Country risk enters through the equity risk premium, or lambda, or the cash flows — one of the three |
| N3 | Employee option value is subtracted, or diluted shares are used, never both |
| N4 | Cash sits inside the cash flows with its interest income and a cash-diluted beta, or outside and added back |
| N5 | A cross-holding is a non-operating asset, or its equity income sits in operating earnings |
| N6 | Failure risk enters through a probability weight, or through a raised discount rate |
| N7 | Downside is protected by a rating constraint, or by an EBIT haircut |
| N8 | A complexity or opacity adjustment is made in one place: cash flows, rate, growth, or a final haircut |
| N9 | A real-option premium is added only after the matching optimism leaves the DCF |
| N10 | Control value is added only for a buyer who can force the change |

N2 is the one that bites hardest during collection. If the sovereign spread was stripped out
of the riskfree rate, it may not also sit inside the equity risk premium build.

### Units and signs

- Percentages are decimal fractions in every artifact. Store 0.0472, never 4.72. This
  covers growth, margins, tax rates, payout ratios, debt ratios, returns and spreads.
- Currency fields carry an explicit `{value, currency, scale}` triple. Never mix scales
  inside one table.
- Cash-flow-statement lines arrive already signed. Capital expenditure and working-capital
  changes are added, not subtracted.
- A positive change in non-cash working capital is a cash outflow.
- Balance-sheet items are point-in-time; income and cash-flow items cover a period. Any
  ratio that mixes them declares whether it uses beginning-of-period or average balances.
  Return on invested capital and return on equity use beginning-of-period capital.
- Interest-rate and inflation changes are absolute changes in the rate. GDP and currency
  changes are percentage changes.

## Collect in stages

Run A1 first, because it parameterises every later fetch. A2 through A8 then run in
parallel except where a dependency is named. Full field tables, with units, source, user
rule and fallback for each, live in the resource files.

### A1 — Mandate, identity and routing

Fixes the frame: `mode`, company name, ticker and exchange, country of incorporation,
valuation currency, valuation date, fiscal year end, industry keys, public or private,
reporting standard. Mode, identity, currency and valuation date block everything when
absent. The rest have inference fallbacks.

Two judgments here shape the whole run. First, map the industry by the business the firm
actually operates, not by its listing classification. A firm in several businesses gets a
list of industries with revenue weights, not one label. Second, if the valuation currency
differs from the filing's reporting currency, flag every downstream stage as needing a
conversion and record which route will be used. The routes are differential-inflation
conversion of a finished rate, or a rebuild from the local riskfree rate.

Reporting standard matters more than it looks. An IFRS or Ind-AS filer often groups
expenses by nature rather than by function, so there may be no cost-of-goods line at all.
See `knowledge/concepts/accounting-statements/accounting-standards-gaap-ifrs.md`.

Fields: [resources/company-inputs.md](resources/company-inputs.md).

### A2 — Financial statements

Pull ten fiscal years where available, five as the working minimum, one as the absolute
floor. One year makes normalization impossible and blocks several routes.

Income statement, balance sheet and cash flow statement, from `F-10K` plus `F-10Q` whenever
the last annual report is more than a quarter old. The quarterly filing is what lets you
rebuild trailing twelve-month figures.

Three collection habits decide whether this stage is usable. Take the cash-flow statement's
build-up lines, not just the section totals — free cash flow to equity cannot be built from
a total. Take gross interest expense; a netted figure is not enough, so go to the debt
footnote when the filer nets it. Label special items year by year over five to ten years,
because the recurrence test needs the frequency and the variability, not this year's
headline.

Six reconciliation ties run before the stage is marked complete. The balance sheet balances.
Net income ties into the first line of cash flow from operations. The retained-earnings
roll-forward closes. Income-statement depreciation ties to the cash-flow add-back. The cash
tie closes. Segment third-party revenues plus eliminations reconcile to consolidated
revenues. Failures of the first, second and fifth block the run; the rest flag.

Fields and ties: [resources/company-inputs.md](resources/company-inputs.md).

### A3 — Footnotes and structured disclosures

Everything the face of the statements leaves out. This is the stage that separates a usable
valuation from a plausible-looking wrong one.

Lease footnote for the commitment schedule and the reported liability. Debt footnote for
the instrument list and the maturity schedule. Segment footnote for business and geographic
splits. Stock-compensation footnote for options. Investments footnote for cross-holdings.
Tax footnote for the effective rate and loss carryforwards. Pension, contingencies and
acquisitions notes for the bridge.

The defaults here carry real cost, so record each one you use. Weighted-average debt
maturity defaults to three years. Option life defaults to four years and the strike to the
current price. Geographic weights default to one hundred percent in the country of
incorporation, which is the single most common cause of a wrong equity risk premium — flag
it loudly and carry a sensitivity. R&D history padded with zeros understates the research
asset, so say so.

Use third-party segment revenue for geographic weights, never revenue including
intersegment sales. For a natural-resource firm prefer production location. For a
manufacturer, ask where the plants are.
See `knowledge/concepts/cost-of-equity/operation-weighted-erp.md`.

Fields: [resources/company-inputs.md](resources/company-inputs.md).

### A4 — Company market data

Price, actual shares outstanding, return series, traded bonds, ratings, volatility,
dividend history, preferred stock and convertibles.

Two flags decide later stages. Tag every rating as global-agency or local-scale: a
local-scale rating does not embed sovereign risk, a global one does, and that single flag
decides whether the country default spread gets added. Tag every bond for usability: a
yield is a usable cost of debt only when the bond is straight, long-term and liquid.
Anything else has option value inside its yield.

Record the beta regression's parameters even though the regression beta is a diagnostic
rather than the production input. Five years of monthly returns is the default. Index
choice can move a beta by half a point on identical data, so name the index and justify it
by the marginal investor's portfolio.

Fields: [resources/market-and-macro-inputs.md](resources/market-and-macro-inputs.md).

### A5 — Macro and currency

Fetched per currency and per operating country, keyed to the valuation date. Government
bond yields, sovereign ratings and spreads, expected inflation, expected real growth, the
Baa spread for the premium cross-check, and spot and forward exchange rates.

The riskfree rate has a four-rung ladder. A sovereign rated Aaa in its own currency gives
its ten-year bond rate directly. Where several sovereigns issue in one currency, take the
minimum ten-year rate across them, not the average and not the home sovereign. Below Aaa,
subtract the sovereign default spread from the local ten-year rate, preferring a market
measure of that spread over a rating lookup, and report the range across every route
available. With no trustworthy local rate, build up from expected inflation and a real
rate, or convert from the US dollar rate by the inflation differential, or switch the whole
valuation to a major currency and restate every other input.

Never substitute a normalized historical riskfree rate for the observed one. If a user
insists, normalize the riskfree rate, inflation, real growth and the equity risk premium
together, and label the result a valuation of a hypothetical economy. Take negative rates
as observed rather than flooring them at zero, and check that the growth and inflation
assumptions in that currency are correspondingly low.
See `knowledge/concepts/cost-of-equity/riskfree-rate-fundamentals.md` and `.../currency-riskfree-rate.md`.

Fields: [resources/market-and-macro-inputs.md](resources/market-and-macro-inputs.md).

### A6 — Reference-table load

Load every reference dataset at one consistent `as_of` and record the vintage on the
snapshot you write into `market-data.json`. Details in the next section.

### A7 — Ownership, governance and marginal investor

Required for `mode = corporate-finance`, and for any run where the marginal-investor
question is live: private firms, closely held firms, family groups.

Institutional and insider percentages, the largest holders with their type, the board
table, executive compensation, charter provisions, and a governance score if one is
available.

The reading matters more than the numbers. A high institutional share of float with a low
insider percentage means a diversified marginal investor, so a market beta is right. Low
institutional ownership with a founder or family who does not trade means an undiversified
marginal investor, which requires a total beta even for a listed firm. A controlling stake
held through a partnership or holding company is undiversified even when it is classified
as institutional. Institutional ownership above one hundred percent of float is a reporting
artifact; leave it alone.

Fields: [resources/context-and-peer-inputs.md](resources/context-and-peer-inputs.md).

### A8 — Comparable firms

Two peer sets, and they are not interchangeable.

Beta comparables serve the bottom-up beta, one set per business the firm operates in. Cast
the net wide — global, with a size floor — because business risk travels across borders
while country risk belongs in the premium. Ten to several hundred firms is normal, and the
standard error falls with the square root of the count. Use the median, never the mean: one
comparable with a debt-to-equity ratio in the hundreds of percent destroys an average. Do
not unlever bank betas; use median levered betas weighted by net revenues.

Pricing comparables serve relative valuation and are defined by risk, growth and cash-flow
characteristics, not by sector code. Record the screen explicitly — sector, geography, size
floor, growth band — because it is the most challengeable part of the analysis. When a
multiple is not computable for a firm, drop the firm and record the count. If most of the
universe drops out, the survivors are profitable survivors and any conclusion says so.

Fields: [resources/context-and-peer-inputs.md](resources/context-and-peer-inputs.md).

### Conditional branches

Classification adds inputs on top of the standard stages. Financial-service firms need
regulatory capital and risk-weighted assets. Young firms need a market size and a target
margin. Distressed firms need a traded bond or a default table. Cyclical firms need a full
cycle of history. Emerging-market exposure needs country weights. Private firms need owner
compensation and a buyer type. Multi-business firms need the segment table. More than one
branch can be live at once, and their input sets compose.

Per-branch fields: [resources/branch-inputs.md](resources/branch-inputs.md).

## The Damodaran reference datasets

These are the named lookup tables the pipeline reads. They are published annually — the
country and premium tables twice a year, in January and July — so each one must be tagged
with the vintage it came from. A table without an `as_of` is not usable.

| ID | Dataset | Vintage-critical |
|---|---|---|
| `D-ERP` | Implied equity risk premium for the S&P 500, with its annual history | Yes |
| `D-HIST` | Historical returns: arithmetic and geometric premiums by window, with standard errors | No |
| `D-CTRY` | Country equity risk premiums: rating, default spread, country premium, total premium, regional averages, PRS mapping | Yes |
| `D-SOVSPR` | Sovereign rating to default spread | Yes |
| `D-TAX` | Country corporate marginal tax rates | Yes |
| `D-RATE1` `D-RATE2` `D-RATE3` | Synthetic rating tables: large and stable, small and risky, financial-service | Yes for the spreads |
| `D-SPREAD` | Rating to default spread, by date | Yes |
| `D-INDUS` `D-GLOB` | US and global industry averages: unlevered beta, market debt-to-equity, returns, margins, working capital over revenues, sales-to-capital, multiples, costs of capital | Yes |
| `D-DEFPROB` | Cumulative default probability by rating | Yes |
| `D-MULTREG` `D-DISTRIB` | Regional multiple regressions; multiple distribution percentiles | Yes |
| `D-DEBTREG` `D-PAYREG` | Market debt-ratio and payout regressions | Yes |
| `D-CPXSEC` `D-RDLIFE` `D-MACRO` | Sector capital-expenditure ratios; R&D amortizable life; sector macro sensitivities | No |
| `D-DISTRESS` `D-ILLIQ` `D-SURV` | Bankruptcy-cost haircuts; illiquidity regressions; survival tables | No |

Three rules govern their use.

All vintage-critical tables share one `as_of`. Mixing a current riskfree rate with a
decade-old country premium table, or a current premium with stale spreads, is a hard
failure. Spreads are the most volatile of the group: they roughly doubled to tripled at
every rating between January 2008 and January 2009, and spiked and reverted inside 2020.
See `knowledge/concepts/cost-of-debt-capital/default-spreads-over-time.md`.

When a vintage-critical table is more than a year older than the valuation date, attempt a
refresh from the publisher. On failure, continue with `status: stale` and disclose the
vintage in the report.

Reproduce a shipped table verbatim. Some published synthetic-rating tables carry
non-monotonic labels or spreads below the B3 bracket. Flag the anomaly rather than quietly
correcting it, because a silent fix cannot be reconciled against the source.
See `knowledge/concepts/cost-of-debt-capital/synthetic-rating.md`.

The bundled snapshots live in `cost-of-capital-toolkit/resources/data/`, each carrying its
own `as_of`, `source` and `refresh` fields. Read them from the path passed in so a
refreshed table can be swapped without touching code.

Column detail and freshness limits: [resources/reference-datasets.md](resources/reference-datasets.md).

## When an input is missing

Walk the ladder for that field and record where you stopped. Every rung costs something,
and the cost is the thing the report has to disclose.

The ladders that matter most, best rung first:

- **Riskfree rate.** Aaa sovereign ten-year, then the minimum across same-currency
  sovereigns, then the local rate less the sovereign spread, then an inflation-plus-real
  build-up, then differential inflation from the US dollar, then a currency switch. The
  last rung forces every other input to be restated.
- **Mature-market equity risk premium.** Current implied, then the average implied premium
  over a stated window, then the historical geometric premium over bonds, longest window.
- **Unlevered beta.** Comparable median, cash-corrected, then the industry table, then a
  regression beta unlevered at the window-average debt-to-equity ratio.
- **Cost of debt.** Straight-bond yield, then a global rating spread, then a recent bank
  loan rate, then a synthetic rating, then a local rating plus lambda times the sovereign
  spread.
- **Lease debt.** Present value of disclosed commitments at the pre-tax cost of debt, then
  the reported lease liability, then zero. Zero understates debt and overstates both return
  on capital and the equity weight.
- **Market debt-to-equity.** Market equity and market debt, then the industry median. Book
  debt-to-equity is never acceptable.
- **Failure probability.** Bond-implied, then the rating default table, then sector
  survival rates.

The full ladder table, with the cost of the last rung on each:
[resources/fallback-ladders.md](resources/fallback-ladders.md).

## Before handing off

`G1_data` passes when the universal minimum is present, the mode-specific additions are
present, and no blocking rule fires.

The universal minimum, for every mode:

- Identity, valuation currency, valuation date, industry key
- One full fiscal year of statements, with a balance sheet that balances
- The debt boundary: short-term debt, long-term debt and the current portion, plus either a
  lease schedule or a reported lease liability
- Cash and marketable securities
- An actual share count, or a private-firm equity-value proxy
- A ten-year riskfree rate in the valuation currency
- A mature-market equity risk premium at a stated vintage
- A beta path: either a comparable set or an industry unlevered beta
- A marginal tax rate for the domicile
- Every vintage-critical table loaded at one `as_of`

Five things block outright. The balance-sheet, net-income and cash ties must hold. A
vintage-critical table missing with no fallback blocks. A live requirement for a failure
probability with no source blocks. A live requirement for a total beta with no comparable
R² blocks. Statements older than eighteen months with no interim filing block a valuation,
and degrade to stale for corporate-finance work.

Geography weights defaulted to the country of incorporation do not block a firm with
country risk above zero, but they carry a mandatory disclosure and a required sensitivity.

Mode-specific minimums, the consolidated validation catalogue and the non-blocking
diagnostics: [resources/gates-and-validation.md](resources/gates-and-validation.md).

## Reference files

- [resources/source-registry.md](resources/source-registry.md) — every source identifier, what it yields, and the trust rule for estimates
- [resources/company-inputs.md](resources/company-inputs.md) — A1 to A3 field tables: identity, three statements, footnotes
- [resources/market-and-macro-inputs.md](resources/market-and-macro-inputs.md) — A4 and A5 field tables: prices, ratings, bonds, rates, inflation, currency
- [resources/reference-datasets.md](resources/reference-datasets.md) — A6: the reference tables, their columns and their freshness limits
- [resources/context-and-peer-inputs.md](resources/context-and-peer-inputs.md) — A7 and A8 field tables: ownership, governance, both peer sets
- [resources/branch-inputs.md](resources/branch-inputs.md) — extra inputs by company type
- [resources/fallback-ladders.md](resources/fallback-ladders.md) — the substitution table and the refresh policy
- [resources/gates-and-validation.md](resources/gates-and-validation.md) — the G1 predicate, the validation catalogue, the diagnostics
