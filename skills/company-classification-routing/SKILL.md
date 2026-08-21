---
name: company-classification-routing
description: Classifies a company and routes it to the correct analytical treatment — life cycle stage, sector type, earnings status, ownership, distress markers, geography — then compiles the hard constraints that follow into classification.json. Use before any valuation begins, when deciding which valuation model applies, or when a company looks non-standard — a bank or insurer, a pre-revenue or loss-making firm, a distressed or declining business, a private company or an IPO, a cyclical or commodity producer, an emerging-market firm, or a multi-business group.
---

# Company classification and routing

Standard valuation machinery assumes a lot. It assumes the firm survives long enough to
reach stable growth. It assumes debt is a financing choice rather than raw material. It
assumes this year's earnings say something about a normal year, and that there are
earnings at all. It assumes the owner is diversified and the shares trade.

Point that machinery at a bank, a pre-revenue startup, or a firm at a cycle trough and it
still returns a number. The number is confident and wrong. That is the most expensive
failure mode in this domain, because nothing downstream flags it: the arithmetic is
correct, the spreadsheet balances, and the answer is nonsense.

Routing comes first for that reason. This skill converts what is knowable about a company
into a *route* — one primary engine, a set of overlays, an ordered pipeline, and a list of
methods that must not be attempted. Gate `G2_classified` passes only when that route is
written and valid. Every stage after it reads the route and honors it.

**Full framework:** `knowledge/frameworks/special-situations-routing.md`. This skill is its
operating manual, and carries the parts an agent needs in hand.

## Contents

- [What this produces](#what-this-produces)
- [The four questions](#the-four-questions)
- [S0 · Evidence intake](#s0--evidence-intake)
- [S1 · Signal extraction](#s1--signal-extraction)
- [S2 · Sector gate](#s2--sector-gate)
- [S3 · Statement-repair gate](#s3--statement-repair-gate)
- [S4 · Ownership and transaction gate](#s4--ownership-and-transaction-gate)
- [S5 · Life-cycle and earnings gate](#s5--life-cycle-and-earnings-gate)
- [S6 · Survival and truncation gate](#s6--survival-and-truncation-gate)
- [S7 · Overlays and constraint compilation](#s7--overlays-and-constraint-compilation)
- [S8 · Combination rules](#s8--combination-rules)
- [The constraint catalogue](#the-constraint-catalogue)
- [Writing classification.json](#writing-classificationjson)
- [Confidence and what stays unresolved](#confidence-and-what-stays-unresolved)

**Resources**

- [Branch catalogue B1–B16](resources/branch-catalogue.md) — trigger, what breaks, what
  replaces it, and the hard constraints for each of the sixteen branches.
- [Signal extraction detail](resources/signal-extraction.md) — how each S1 signal is
  computed from filings and market data, and the judgment each one hides.
- [Combination and worked routings](resources/combination-worked-routings.md) — precedence,
  exclusion pairs, composition arithmetic, and routed real companies.
- [Pricing routes by branch](resources/pricing-routes.md) — which multiple survives this
  company's defects, and which are forbidden.
- [The classification artifact](resources/classification-artifact.md) — field-by-field
  shape, validation, and the `diagnosis.md` companion.

## What this produces

Two files, both written by `company-diagnostician` and by nobody else:

| Artifact | Contents |
|---|---|
| `02-diagnosis/classification.json` | the machine-readable route: signals, primary path, overlays, constraints, pipeline, confidence |
| `02-diagnosis/diagnosis.md` | the reasoning: what the company is, which gate fired and why, what would change the answer |

Downstream agents read `classification.json` and never re-derive it. The critic checks
every produced artifact against the compiled constraints, under rule V9, route
conformance. `valuation-consistency-checks` enforces a subset mechanically. Pass the
artifact to it with `--classification`. It then fails the run on an FCFF valuation of a
bank, a missing failure probability, or an earnings multiple on negative earnings.

## The four questions

Every valuation answers four questions, and every branch below repairs one of them.

1. What are the cash flows from existing assets?
2. What value is added by growth assets?
3. How risky are those cash flows?
4. When does maturity arrive, and what can end the story before then?

A company is difficult exactly when one of those answers is missing, unstable, or
mis-measured by accounting. Diagnose which one breaks and the repair names itself. A young
firm breaks Q1 and Q4. A bank breaks Q1 and Q3 together, because its debt is inventory. An
intangible-heavy firm breaks Q1 and Q2, because accounting expensed its capital spending.
Detail: `knowledge/concepts/dark-side-difficult/difficult-company-taxonomy.md`.

Two errors follow from skipping this step. The first is repairing a cash-flow problem in
the discount rate — failure risk, governance, distress and country risk all get pushed
there, and all belong in expected cash flows or in probability weights. The second is
treating one bucket at a time when a company sits in several. Boeing in March 2020 was
mature, cyclical and distressed at once.

## S0 · Evidence intake

Inputs: `mandate.json`, `01-data/raw-financials.json`, `01-data/market-data.json`,
`01-data/gaps.json`.

A normal valuation leans on three information sources. Record each as `present`, `thin` or
`absent`:

1. Current financial statements.
2. The firm's own financial history.
3. Industry and comparable-firm data.

Three decision rules follow.

- Two or more sources absent — this is the point of maximum temptation toward the dark
  side, where analysts declare a paradigm shift and invent metrics. Force an explicit
  mature end-state instead: target margin, terminal ROC, stable growth. Then work
  backwards. Set `route.requires_end_state = true`.
- No cash flows exist and none ever will — a currency, a collectible, a bare commodity
  holding. The asset can be priced, never valued. Emit `no-intrinsic-valuation` and route
  to pricing only. See `knowledge/concepts/narrative-numbers/value-vs-price-gap.md`.
- Fewer than three years of statements, or statements that mix personal and business
  expense — private-company cleanup runs before any forecast. See B13.

Return `blocked` when the minimum viable input set is missing and the user has supplied no
substitute. Name what is needed. Do not guess and proceed.

## S1 · Signal extraction

Every signal is computed from data, never asserted. Each carries a confidence and the
evidence that set it. These are the only inputs the gates in S2 through S6 may consult.

| Signal | Computation | Values and thresholds |
|---|---|---|
| `sector_type` | Business description, segment note, and the shape of the statements themselves | `financial-service` \| `commodity` \| `cyclical-industrial` \| `real-estate/REIT` \| `intangible-heavy` \| `ordinary` |
| `life_cycle_stage` | Revenue level, revenue growth, margin sign and stability, reinvestment intensity, age | `start-up` \| `young-growth` \| `high-growth` \| `mature-growth` \| `mature-stable` \| `decline` |
| `earnings_status` | Sign and representativeness of trailing EBIT and net income, judged after S3 cleanup | `profitable` \| `marginal` \| `negative-transient` \| `negative-structural` \| `cyclical-trough` \| `cyclical-peak` |
| `revenue_status` | Trailing revenue against the 3-year and 5-year figures | `pre-revenue` \| `growing` \| `flat` \| `declining` |
| `g_firm` vs `g_econ` | Expected near-term growth against nominal economy growth, proxied by the riskfree rate in the valuation currency | `≤ g_econ` → 1 stage; `≤ g_econ + 10%` → 2 stages; `> g_econ + 10%` → 3 or more stages |
| `leverage_state` | Market `D/(D+E)`, its distance from the sector median and from any stated target, and its trajectory | `stable` \| `changing` \| `extreme` (above 50%) |
| `payout_coverage` | `Σ5yr (dividends + buybacks) / Σ5yr FCFE` | below 80% → FCFE; 80–110% → dividends; above 110% → FCFE |
| `distress_markers` | Coverage ratio, rating, bond prices against par, negative book equity, covenant breach, going-concern note, distressed sector peers | count plus an evidence list |
| `intangible_intensity` | `R&D / revenues`, `R&D / (R&D + net capex)`, brand-advertising share, recruiting and training spend | `low` \| `moderate` \| `high` |
| `geography_exposure` | Revenue and production share by country or region — not the country of incorporation | weight vector |
| `ownership` | Public, private, subsidiary or division; free float; insider and institutional holdings; dual-class shares; cross-holdings | structure record |
| `stake_size` | Fraction of equity being valued | above 50% controlling; 50% or less minority |
| `buyer_diversification` | Who the marginal investor is for this specific transaction | `diversified` \| `partially` (with ρ) \| `undiversified` |
| `holdings_share` | Value of stakes in other firms divided by total estimated value | flag above roughly one third |
| `business_count` | Reportable segments with distinct economics and separable cash flows | `1` \| `>1` |
| `option_candidates` | Patents, undeveloped reserves, licences, exclusive expansion rights, contractual exit rights, excess debt capacity | list, each with an exclusivity note |
| `macro_driver` | Regress revenues on a commodity or cycle price and report the R² | driver plus R² |
| `transaction_motive` | Read from the mandate | valuation \| acquisition \| restructuring \| ipo \| project \| corporate-finance |

The arithmetic here is mechanical. The judgment is whether a computed signal is
*representative*: a coverage ratio taken at a trough, a regression beta on a stock that
barely trades, a margin distorted by one large contract. Record that judgment where you
make it. Computation detail and the traps in each signal:
[resources/signal-extraction.md](resources/signal-extraction.md).

## S2 · Sector gate

Evaluated first and outranking every other gate, because sector decides whether firm-level
cash flow and firm-level leverage are even defined.

```
if   sector_type == financial-service          -> B5   (ends the FCFF path entirely)
elif sector_type == real-estate/REIT           -> B5b  (payout mandated)
elif macro_driver exists and R^2 is high       -> B6   (commodity)
elif sector_type == cyclical-industrial
     and earnings_status in {trough, peak}     -> B7   (cyclical normalization)
else                                           -> continue to S3
```

Commodity and cyclical are separated by one question: does a usable price driver exist? A
high-R² regression of revenues on the commodity price sends the firm to B6, because the
price essentially is the revenue model. No usable price series sends it to B7.

For a REIT, mandated payout and tax status make optimal-debt-ratio work and
retention-based growth meaningless. Value on dividends or FFO, and exclude the firm from
any corporate-finance financing recommendation. All other routing continues normally.

Bank statements announce themselves. Revenue arrives as net interest income and net fee
income rather than sales minus cost of goods. Interest expense sits inside operations. The
credit-loss provision is a recurring operating expense. Property and equipment is
negligible, and equity is a thin slice of assets — HSBC in 2019 held equity worth 7.1% of
total assets, which is structure rather than a warning.
`knowledge/concepts/accounting-statements/sector-differences-in-financial-statements.md`.

## S3 · Statement-repair gate

Always executed. This is what sets what "earnings" means for everything downstream. The
order is fixed because each step feeds the next.

1. Update to trailing twelve months.
2. Capitalize operating leases into lease debt, restated EBIT, restated invested capital.
3. Capitalize R&D, recruiting or brand-building advertising when `intangible_intensity` is
   moderate or high. This is overlay **B8**.
4. Strip one-time items and personal expenses. Charge a market salary for uncompensated
   owner labour at a private firm.
5. Normalize only if S4 routes to B7. Normalization and the revenue-driven path are
   mutually exclusive.
6. Resolve the circularity. Restated EBIT sets interest coverage, which sets the synthetic
   rating, which sets the cost of debt, which sets the lease discount rate, which changes
   restated EBIT. Iterate to a fixed point.

Every downstream consumer of EBIT, invested capital, ROIC, coverage and reinvestment uses
the same restated basis. Mixing bases is the most common silent error in this pipeline.

`financial-statement-normalization` performs steps 2 through 4 and the ratio pack;
`cost-of-capital-toolkit` supplies the synthetic rating that closes the loop in step 6.

## S4 · Ownership and transaction gate

```
if   ownership == private and transaction_motive != ipo  -> B13 (plus sub-scenario)
elif transaction_motive == ipo                           -> B14
elif ownership == division/subsidiary being separated    -> B10 (sum-of-the-parts)
elif transaction_motive == acquisition                   -> B15 (four-number chain)
elif transaction_motive == restructuring
     or an activist/control question is live             -> B2
else                                                     -> continue to S5
```

This gate fixes two things: the **discount-rate identity** — whose risk is being priced —
and the **discount stack** of illiquidity, minority and key-person adjustments. It does not
choose the cash-flow engine. S5 does that.

The identity question matters more than it looks. A private business does not have one
value; it has a value per buyer and per purpose. The gap between a valuation for an
undiversified individual buyer and one for a diversified public acquirer is the bargaining
range, not an error. Quote one number to both sides of a negotiation and you have answered
neither question.

## S5 · Life-cycle and earnings gate

This selects the primary cash-flow engine.

```
if   revenue_status == pre-revenue
     or earnings_status == negative-structural
     or (life_cycle_stage in {start-up, young-growth}
         and earnings_status != profitable)        -> B1  revenue-driven, work backwards
elif earnings_status in {negative-transient,
                         cyclical-trough,
                         cyclical-peak}            -> B7  normalize, then standard engine
elif revenue_status == declining
     and life_cycle_stage == decline               -> B3  negative growth and reinvestment
elif life_cycle_stage in {mature-growth, mature-stable}
     and policies look consistent, stable and bad  -> B2  status quo versus optimal
else                                               -> standard path
```

The B7-versus-B1 call is the sharpest judgment in the whole gate. Normalization is
legitimate only when the trouble is temporary. Evidence for temporary: the sector is in a
known downturn, peers show the same pattern, the firm earned normal margins for years, and
the balance sheet survives until recovery. Evidence against: falling market share, a
structural demand shift, leverage forcing asset sales. All three normalization approaches
will happily produce a healthy EBIT for a firm that will never earn it again.

"Consistent, stable and bad" needs evidence too. Stability is not quality. Test for
`ROIC < WACC`, reinvestment far off the sector norm, or a debt ratio far from the sector
optimum.

**Standard path selection**, when no special branch fires:

- Equity or firm. `leverage_state == stable` takes the equity route. `changing`, or
  incomplete leverage data, takes the firm route through FCFF and WACC.
- On the equity route, apply the 80% / 110% payout screen to choose dividends against
  FCFE.
- Stage count from the `g_econ + 10%` screen in S1.

## S6 · Survival and truncation gate

Applied as an outer wrapper *after* the engine produces a going-concern value. A DCF values
a company that lives long enough to reach stable growth. When it might not, the DCF
overstates value, and the repair is never a higher discount rate.

```
survival_in_doubt = any of:
   life_cycle_stage in {start-up, young-growth}    -> B1 requires it by default
   revenue_status == declining and leverage high   -> B3 hands off to B4
   coverage < 1 or rating <= CCC                   -> B4
   traded bonds well below par                     -> B4, invert the price for pi
   bank near its regulatory capital minimum        -> B5, wipeout probability
   expropriation or regime-change exposure         -> B9 truncation
   market D/(D+E) > 50% and earnings negative      -> B4 plus equity-as-option cross-check
```

When it fires, route to **B4**, or to the truncation sub-branch of B9, or both. Source the
probability from the most informative channel available. In ascending order: sector
survival tables, then the rating-implied cumulative default rate, then a statistical model,
then an inverted traded bond price. The last is sharpest because it is the market's own
number.

Firm failure and equity wipeout are different events. A bailout can save the firm and
destroy the equity. Say which one is being modelled.

## S7 · Overlays and constraint compilation

Overlays are non-exclusive and compose. Assign every overlay whose trigger fires, then
compile the union of the constraint sets from every branch that fired. S8 resolves any
conflict.

| Overlay | Fires when |
|---|---|
| **B8** intangible-heavy | material R&D, recruiting, or brand-building advertising |
| **B9** emerging-market and country risk | material revenue, production or asset exposure to sovereign risk — assigned by exposure, not by passport |
| **B10** multi-business | more than one segment with distinct economics and separable cash flows |
| **B11** cross-holdings | a partly-owned consolidated subsidiary, a minority stake, or a pyramid group |
| **B12** real options | any `option_candidate` that clears the three-test gate |
| **B16** macro shock | a material move in riskfree rate, ERP, default spreads, base earnings or tax regime since the last valuation |

Constraint compilation is mechanical once branches are assigned. Take every constraint
listed against every fired branch in [the catalogue](#the-constraint-catalogue), plus the
two universal ones, and write them into `constraints` with a reason and a `source_branch`.
Compile nothing that no branch emitted. A constraint with no source is an opinion.

## S8 · Combination rules

Real companies sit in several buckets at once. These rules make composition deterministic.

**R1 — One engine only.** Precedence, highest first:

```
B5 financial-service  >  B13/B14 private or IPO (rate and discount identity)
                      >  B4 distress with equity wipeout
                      >  B1 revenue-driven
                      >  B7 normalized
                      >  B3 declining
                      >  B2 status quo versus optimal
                      >  standard
```

B10 sum-of-the-parts is a decomposition rather than an engine. It runs this precedence list
once per division, then aggregates.

**R2 — Overlays never replace the engine.** B8, B9, B11, B12 and B16 modify inputs, the
discount rate, or the bridge. They never change which cash flow is discounted.

**R3 — Mutually exclusive pairs.** A violation is a hard error, not a warning.

| Pair | Rule |
|---|---|
| B7 normalize ↔ B1 revenue-driven | Normalization is legitimate only when the trouble is temporary. Structural, life-cycle or leverage-driven losses route to B1 or B4. Never both. |
| B7 normalize ↔ a separate recovery assumption | Normalized earnings *are* the recovery. Assuming recovery on top counts it twice. |
| B5 ↔ FCFF, WACC, enterprise value | A financial service firm never gets a firm-level valuation. |
| Total beta ↔ a diversified buyer | One buyer identity per valuation. |
| Illiquidity discount ↔ a public buyer or an IPO | The buyer's investors already have a market. |
| B12 option value ↔ the same upside inside DCF growth | Route each claim to exactly one device. |
| A higher discount rate for failure ↔ B4 probability weighting | Pick one channel. The probability weight is the correct one. |

**R4 — Ordering when several branches fire.** The pipeline is fixed:

```
1. Clean accounts        S3: leases, R&D via B8, one-times, owner salary
2. Fix base earnings     B7 normalize, or B1 abandon earnings and drive from revenue
3. Build the rate stack  bottom-up beta -> total beta if B13-I
                         -> exposure-weighted ERP or lambda if B9
                         -> synthetic rating including country spread if B9
                         -> divisional rates if B10
4. Run the engine        per R1, and per division if B10
5. Outer adjustments     B4 failure, B9 truncation, B2 P(change) — each applied once
6. Equity bridge         debt including leases, minorities at market, cash,
                         B11 cross-holdings, employee options
7. Discount stack        B13 illiquidity then minority; key-person is already in EBIT
8. Uncertainty           scenario grid, then simulation
9. Price comparison      gap, catalyst, expected return
```

**R5 — Composition arithmetic.** Probability-weighted branches compose multiplicatively on
the going-concern value, and each risk appears exactly once:

```
V = V_going_concern × Π_i (1 − p_i × loss_fraction_i) + Σ_i p_i × proceeds_i
```

In practice, never stack more than two without arguing that the events are genuinely
distinct. A country risk premium plus a nationalization scenario plus a governance discount
is three charges for one overlapping risk.

**R6 — Governance and country risk are cash-flow facts.** Model weak governance as low
returns on capital and a low probability of change. Never as a discount-rate bump or a flat
value haircut. The same holds for emerging-market risk beyond the exposure-weighted
premium.

**R7 — Common multi-branch shapes.** Seven worked resolutions, including the distressed
emerging-market bank and the cyclical firm in a shock, are in
[resources/combination-worked-routings.md](resources/combination-worked-routings.md).

**R8 — Mode interaction.** The mandate's `mode` selects what runs *after* the engine, never
the engine itself. `acquisition` wraps the engine in B15's four-number chain.
`restructuring` routes to B2. `corporate-finance` runs the capital-structure and payout
stages, and those two stages are suppressed entirely for B5 and B5b.

## The constraint catalogue

Emitted by the branches, enforced by every downstream agent, checked by the critic under
rule V9. The IDs are stable identifiers and are the contract between agents. Write them
exactly as spelled here.

| ID | Fires when | Meaning |
|---|---|---|
| `no-fcff-valuation` | B5 | Financial service firm: debt is raw material, not financing. Value equity directly. |
| `no-optimal-debt-ratio` | B5, B5b | Regulatory capital governs. No WACC-minimizing schedule. |
| `no-enterprise-multiple` | B5, B5b | EV/EBITDA, EV/Sales and EV/IC are meaningless where debt is raw material. |
| `no-earnings-multiple` | B1, B4, B7 on the un-normalized year | PE, PEG and EV/EBIT are undefined on negative or trough earnings. |
| `no-standard-growth-model` | B1 | Growth is built from revenue and a target margin, not from an earnings growth rate. |
| `require-failure-probability` | B1, B3 with leverage, B4 | A going-concern DCF alone overstates value. |
| `require-normalized-earnings` | B6, B7 | Commodity or cyclical firm sitting at a cycle extreme. |
| `no-normalization` | B1 with structural losses, B3 | Normalizing a permanently broken business values a company that does not exist. |
| `require-total-beta` | B13-I, B13-IV early stages | An undiversified owner prices total risk. |
| `require-illiquidity-discount` | B13-I | Unless the buyer is public and liquid. |
| `no-illiquidity-discount` | B13-II, B13-III, B14 | The buyer's investors have a market. |
| `require-key-person-haircut-on-income` | B13, owner-operated | Applied to operating income, never to final value. |
| `require-rd-capitalization` | B8 | Restate EBIT, capital, ROIC, reinvestment and coverage before valuing. |
| `require-exposure-weighted-risk` | B9 | Country risk by operations, not by incorporation. |
| `no-blanket-country-discount` | B9 | A premium or a scenario, never either plus an arbitrary haircut. |
| `no-governance-discount` | B2, B9 | Model weak governance as low returns and a low probability of change. |
| `require-divisional-rates` | B10 | One cost of capital per division, never one company-wide. |
| `zero-growth-below-cost-of-capital` | B10 | A division earning at or below its cost of capital gets no high-growth period. |
| `require-market-value-minorities` | B11 | Never subtract book minority interest. |
| `require-exclusivity-scaling` | B12 | No unstated exclusivity factor of 1.0. |
| `no-option-premium-without-gate` | B12 | All three option tests must pass first. |
| `no-exit-multiple-terminal-value` | B15 | An exit multiple smuggles today's pricing into an intrinsic valuation. |
| `require-target-own-discount-rate` | B15 | No risk transference and no debt subsidy from the acquirer. |
| `synergy-baseline-is-restructured-target` | B15 | Prevents counting control gains twice. |
| `no-perpetual-growth-above-riskfree` | universal | Terminal growth cannot exceed the riskfree rate in the valuation currency. |
| `single-charge-per-risk` | universal | Each risk is priced exactly once. |
| `no-intrinsic-valuation` | S0, when no cash flows will ever exist | The asset is priceable only. |

## Writing classification.json

The contract in `knowledge/architecture/SPEC.md` §5, extended by the S7 route record. Both blocks
belong in the one file.

```json
{
  "life_cycle_stage": "young|growth|mature|aging|declining",
  "earnings_status": "profitable|marginal|negative|cyclical-trough",
  "sector_type": "non-financial|financial-service|commodity-cyclical|real-estate",
  "ownership": "public|private|subsidiary",
  "geography": {"incorporation": "US", "operations": [{"region": "...", "revenue_share": 0.0}]},
  "distress_markers": {"present": false, "evidence": []},
  "intangible_intensity": "low|moderate|high",
  "primary_path": "standard-fcff|standard-fcfe|dividend-discount|excess-return|revenue-driven|distress-adjusted|asset-based",
  "engine_branch": "B1..B16",
  "overlays": ["intangible-heavy", "emerging-market", "multi-business", "cross-holdings", "has-real-options", "macro-shock"],
  "transaction_overlay": "acquisition|restructuring|ipo|private-sale|none",
  "discount_stack": ["illiquidity", "minority", "key-person"],
  "constraints": [{"rule": "no-optimal-debt-ratio", "reason": "...", "source_branch": "B5"}],
  "pipeline": ["clean", "normalize|revenue-drive", "rate-stack", "engine", "outer-adjustments", "bridge", "simulate", "price-compare"],
  "confidence": "high|medium|low",
  "unresolved": ["what would change the routing"]
}
```

Three rules on the writing itself. `primary_path` and `engine_branch` describe the same
choice and must agree — a B5 branch never carries a `standard-fcff` path. Exactly one
engine branch appears; overlays go in `overlays`. Every constraint carries both a reason in
plain words and the branch that emitted it, because the critic reads the reason when it
finds a violation. Field-by-field guidance and the `diagnosis.md` companion:
[resources/classification-artifact.md](resources/classification-artifact.md).

## Confidence and what stays unresolved

Set `confidence` from the evidence, not from how clean the JSON looks.

| Level | When |
|---|---|
| `high` | All three S0 sources present; no gate decided on a marginal threshold; one branch clearly dominant. |
| `medium` | One source thin; or a gate turned on a judgment call such as transient against structural losses; or two engines were both arguable and R1 broke the tie. |
| `low` | Two or more sources absent; or the sector call itself is contested; or the distress probability drives most of the answer. |

`unresolved` lists the evidence that would change the routing, stated so someone could go
and find it. "A traded bond price would replace the rating-implied default probability" is
useful. "More information about the company" is not.

Low confidence is not a reason to stop. It is a reason to widen the margin of safety, run
the scenario grid on the two drivers this branch turns on, and say plainly in
`diagnosis.md` which judgment the answer rests on. The recurring pattern across every
branch is that the arithmetic is mechanical and the inputs are not. Route correctly first,
then spend the effort on the two or three judgments the branch actually turns on.
