# The pricing playbook — relative valuation and asset-based valuation

**Layer:** FRAMEWORK (top rung). This document orchestrates the concept notes; it does not restate
their derivations. Every stage names the concept files that carry the formulas, tables and worked
examples. Read this to know *what runs, in what order, with what inputs, and which decision rule
fires*. Read the cited concept to know *how the number is computed*.

**Scope.** Everything that prices an asset against other assets, and everything that values an asset
by valuing its pieces:

- the four-step multiple discipline (define / describe / analyze / apply);
- picking the right multiple for a sector and a company type;
- building and cleaning a comparable sample;
- controlling for differences — companion variables, modified multiples, sector regressions,
  market-wide and cross-market regressions;
- sum-of-the-parts for multi-business firms (pricing route and intrinsic route);
- liquidation and fair-value (accounting) asset-based valuation;
- market- and country-level pricing;
- stake-level adjustments (control, minority, illiquidity, key person) applied to a pricing output;
- reconciling a pricing verdict with an intrinsic verdict into one decision.

**Out of scope (handoffs).** The DCF engine itself (forecast, terminal value, cost of capital,
equity bridge construction) belongs to the intrinsic-valuation framework. This playbook *consumes*
its outputs at Stage 10B and Stage 15, and *supplies* it terminal-multiple sanity checks. Full
private-company valuation pipelines (statement cleanup → total beta → DCF) belong to the
special-situations framework; Stage 14 here covers only the stake-level adjustments that sit on top
of any value or price.

**The governing proposition.** A relative verdict is never an absolute one. Every output of this
playbook is a statement of the form *"cheap or expensive versus this benchmark, given these
fundamentals"*. It inherits whatever mispricing the benchmark carries
(`concepts/relative-valuation/pricing-vs-value.md`). Any stage that emits a verdict must emit the
benchmark alongside it.

---

## 0. Stage map

| Stage | Name | Runs when | Terminal artifact |
|---|---|---|---|
| S0 | Route selection | always | `route.pricing` block |
| S1 | Preconditions and constraint set | always | `constraints[]`, blocked-multiple list |
| S2 | Define the multiple | routes R, M, SOTP-pricing | `multiple_spec` |
| S3 | Describe the distribution | routes R, M, SOTP-pricing | `distribution` block |
| S4 | Analyze — intrinsic derivation, companion variable | routes R, M, SOTP-pricing | `companion_variable`, `intrinsic_multiple` |
| S5 | Build the comparable sample | routes R, SOTP-pricing | `peer_set`, `sample_diagnostics` |
| S6 | Choose the control technique (6 branches) | routes R, SOTP-pricing | `control_method`, `predicted_multiple` |
| S7 | Company-type overrides (6 branches) | conditional on S1 | modified inputs to S2–S6 |
| S8 | Predicted multiple → value → per share | routes R, SOTP-pricing | `implied_value_per_share` |
| S9 | Multi-multiple reconciliation, pricing verdict | routes R, SOTP-pricing | `pricing_verdict` |
| S10 | Sum-of-the-parts (3 branches) | route A3 / overlay `multi-business` | `sotp` block, conglomerate discount |
| S11 | Liquidation valuation | route A1 | `liquidation_value` |
| S12 | Fair value (FAS 157) | route A2 | `fair_value` + measurement level |
| S13 | Market- and country-level pricing | route M or as macro context | `market_pricing` block |
| S14 | Stake, control and liquidity adjustments | conditional | `stake_adjustments` |
| S15 | Reconcile pricing vs intrinsic → recommendation | always (terminal) | `verdict`, `RELATIVE.md` |
| S16 | Validation gates and red team | after every stage | `findings[]` |

Branch count: S0 emits 5 routes; S6 has 6 branches; S7 has 6 branches; S10 has 3 branches.
**17 stages, 20 branches.**

### Gates

Gates are predicates checked before dispatching a stage. A failed gate returns `blocked` naming
the missing input; it never proceeds with a default.

| Gate | Passes when | Blocks |
|---|---|---|
| `P0_route` | Motive, benchmark scope and value measure fixed | everything |
| `P1_clean` | Cleaned financials exist; leases capitalized; R&D capitalized if intangible-heavy; earnings normalized if cyclical | S2 onward |
| `P2_classified` | Company type, sector, region, life-cycle stage fixed; blocked-multiple list produced | S2 onward |
| `P3_defined` | Numerator/denominator claimholder-consistent; timing variant and share-count convention fixed and uniform across the sample | S5 onward |
| `P4_sample` | Peer set assembled with drop-out count and reason recorded | S6 onward |
| `P5_controlled` | Control technique matched to the number of differing dimensions; fit statistics recorded | S8 onward |
| `P6_bridged` | Enterprise-to-equity bridge complete and non-double-counting | S9 onward |
| `P7_reconciled` | Pricing verdict stated against a named benchmark; gap to intrinsic explained not averaged | S15 |

---

## S0 — Route selection

**Purpose.** The motive determines the method. Running the wrong route produces a number nobody can
transact on.

**Inputs.** Mandate (why is this valuation being done); who the asker is (passive investor, activist,
acquirer, accountant, liquidator, banker, owner); horizon; benchmark the analyst is judged against;
whether the firm is single- or multi-business; whether the assets are separable.

**Procedure.**

1. Decide pricing versus valuing. Pricing is the right frame when the objective is to transact at
   today's price (IPO, M&A, divestiture), when the strategy is momentum-based, when the analyst is
   judged on relative performance, or when information is too scarce for a DCF. Intrinsic valuation
   is the right frame when hunting absolute mispricing that will correct over time. Most mandates
   need both, run separately and reconciled at S15
   (`concepts/relative-valuation/pricing-vs-value.md`,
   `concepts/narrative-numbers/three-approaches-to-valuation.md`,
   `concepts/dark-side-difficult/value-versus-price.md`).
2. Run the **asset-based feasibility test** before admitting any asset-based route
   (`concepts/asset-based-private/asset-based-valuation-overview.md`). Three predicates:
   - **Separability** — can the assets be sold apart from each other? Real-estate portfolios and
     holding companies pass; brand name never does, because it cuts across every asset.
   - **Traceable cash flows** — can earnings be assigned to individual assets?
   - **Active market** — do comparable assets trade, so transaction prices exist?
   Score each pass/fail. All three pass → asset-based routes are defensible. Two fail → asset-based
   valuation is not the right frame; record the failure and route to R.
3. Emit the route.

**Routes.**

| Route | Fires when | Stages |
|---|---|---|
| **R — firm-level pricing** | default for any listed or comparable-rich company | S1→S2→S3→S4→S5→S6→S7→S8→S9→S15 |
| **A1 — liquidation** | intent is piecemeal sale; or a distressed firm where liquidation may exceed going concern | S1→S11→S15 |
| **A2 — fair value / accounting** | an accounting mandate (FAS 157 / IFRS 13) requires an exit price | S1→S12→S15 |
| **A3 — sum-of-the-parts** | multi-business firm; break-up, spin-off, activist or conglomerate-discount thesis | S1→S10 (→S2–S8 per division for 10A) →S15 |
| **M — market / country pricing** | the subject is an index or a national market, or the firm's verdict needs a macro anchor | S1→S13→S15 |

**Motive → mechanic mapping** (`concepts/asset-based-private/asset-based-valuation-overview.md`,
`concepts/asset-based-private/sum-of-the-parts-framework.md`):

| Who is asking | Route | Mechanic | Why |
|---|---|---|---|
| Passive long-term investor | A3 | intrinsic (10B) | thesis is that the market misprices the pieces and will correct |
| Activist / acquirer / board weighing a break-up | A3 | relative (10A) | the pieces will change hands at market prices |
| Firm preparing a spin-off or divisional sale | A3 | relative for the transaction price, intrinsic for the reservation price | both numbers are needed |
| Accountant under fair value | A2 | relative first, intrinsic only at level 3 | the standard demands an *exit* price |
| Liquidator | A1 | relative (price the assets) | you are selling, not holding |
| Firm testing whether it is well run | A3 | run 10A **and** 10B and compare to a whole-company DCF | the spread is the finding |

**Outputs.** `route.pricing = {primary_route, motive, benchmark_scope, value_measure_intent,
feasibility_test: {separable, traceable, active_market}}`.

**Draws on:** `concepts/relative-valuation/pricing-vs-value.md`,
`concepts/asset-based-private/asset-based-valuation-overview.md`,
`concepts/asset-based-private/sum-of-the-parts-framework.md`,
`concepts/narrative-numbers/three-approaches-to-valuation.md`,
`concepts/dark-side-difficult/value-versus-price.md`,
`concepts/narrative-numbers/value-vs-price-gap.md`.

---

## S1 — Preconditions and the constraint set

**Purpose.** Classification precedes everything. Running standard multiple machinery on a bank, a
loss-maker or a cyclical at a trough produces confident nonsense. This stage produces the list of
multiples that are *blocked* before any multiple is chosen.

**Inputs.** Cleaned financials; company classification (life-cycle stage, earnings status, sector
type, ownership, geography, intangible intensity, distress markers); market data.

**Procedure.**

1. Confirm the accounting cleanups have already run. Order matters and each one changes the
   denominator of several multiples:
   - **Operating leases capitalized as debt** — changes EBIT, debt, invested capital, EV, and the
     coverage ratio (`concepts/cost-of-debt-capital/operating-leases-as-debt.md`,
     `concepts/asset-based-private/private-company-statement-cleanup.md`).
   - **R&D capitalized** if intangible-heavy — changes EBIT, book equity, invested capital, ROC,
     ROE and reinvestment. Expect ROE and ROC to **fall**, not rise. The adjustment to EBIT is
     negative when R&D spending is shrinking (`concepts/dark-side-difficult/capitalizing-rd.md`).
   - **Earnings normalized** if cyclical or at a cycle extreme
     (`concepts/dark-side-difficult/normalized-earnings.md`).
   - **One-time items stripped**; trailing-12-month basis adopted
     (`concepts/dcf-cashflows-growth/reported-to-actual-earnings.md`).
   These cleanups must be applied identically to every comparable, or the uniformity test at S2
   fails. If peer data is only available on an unadjusted basis, use the unadjusted basis for the
   *whole* sample and record the compromise.
2. Build the blocked-multiple list from the classification.

**Decision rules — blocked multiples.**

| Condition | Blocked | Substitute | Source |
|---|---|---|---|
| Negative or trough earnings | PE, PEG, EV/EBIT, EV/EBITDA (if EBITDA<0) | EV/Sales, EV/IC, PBV, forward multiples, survival-proxy regression | `relative-valuation/multiple-distribution-statistics.md`, `relative-valuation/pricing-young-companies.md` |
| Financial service firm (bank, insurer, brokerage) | **all enterprise-value multiples** — debt is raw material, not financing; EV/EBITDA is meaningless and reported as NA in the industry tables | PE, PBV (companion variable ROE), price/deposits | `relative-valuation/comparable-selection-and-controls.md`, `relative-valuation/industry-average-multiples.md`, `dark-side-difficult/financial-service-firm-valuation.md` |
| Negative book equity, heavy buyback history, or large unrecognized intangibles | PBV, EV/IC | EV/Sales, EV/EBITDA | `relative-valuation/book-value-multiples.md` |
| Negative EBITDA | EV/EBITDA (firm silently drops out of samples) | EV/Sales | `relative-valuation/ev-ebitda-multiple.md` |
| Pre-revenue | every conventional multiple | market-implied operating metric (users, subscribers); forward multiple with the full haircut | `relative-valuation/pricing-young-companies.md` |
| Cash > ~20% of firm value | raw PE, raw PBV — cash inflates both (cash alone carries PE = 1/riskfree) | EV multiples, or split operating from cash and price separately | `dcf-model-choice-loose-ends/cash-in-valuation.md` |
| Consolidated but partly owned subsidiaries | uncorrected EV/EBITDA (100% of EBITDA against a partial equity claim) | EV net of minority interests at market | `relative-valuation/multiple-definition-tests.md`, `dark-side-difficult/cross-holdings.md` |
| Cross holdings > ~1/3 of value | any multiple on consolidated numbers alone | price operating business separately, add stakes | `dark-side-difficult/cross-holdings.md` |
| Leverage differs sharply across the peer set | equity multiples (PE, PBV, P/S) | enterprise multiples | `relative-valuation/comparable-selection-and-controls.md` |

**Outputs.** `constraints[] = [{rule, reason}]`; `blocked_multiples[]`; `cleanups_applied[]`;
`classification` echo.

**Draws on:** `concepts/dark-side-difficult/difficult-company-taxonomy.md`,
`concepts/dark-side-difficult/capitalizing-rd.md`,
`concepts/dark-side-difficult/normalized-earnings.md`,
`concepts/accounting-statements/sector-differences-in-financial-statements.md`,
`concepts/accounting-statements/non-operating-items-and-cross-holdings.md`,
`concepts/dcf-model-choice-loose-ends/cash-in-valuation.md`.

---

## S2 — Define the multiple (four-step, step 1)

**Purpose.** Settle numerator, denominator, timing and share count so every firm in the sample is
measured the same way. Skipping this is how borrowed multiples smuggle in someone else's
conventions (`concepts/relative-valuation/four-step-multiple-framework.md`).

**Inputs.** Candidate multiples (blocked list removed); market values; book values; cash; debt;
minority interests; option counts; the chosen denominator series for the firm and every peer.

**Procedure.**

1. Classify the numerator: market value of equity, firm value (= equity + debt), or enterprise value
   (= equity + debt − cash).
2. Classify the denominator by claimholder and **reject or restate mismatches**. Equity value goes
   with equity measures (net income, EPS, book equity, FCFE); firm/enterprise value goes with
   operating measures (EBIT, EBITDA, sales, invested capital, FCFF). Price/EBITDA is inconsistent
   and is rejected, not adjusted.
3. Pin the timing variant and hold it across the whole sample: current (last fiscal year), trailing
   (last twelve months), forward (next year), or a far-forward year. Never mix.
4. Pin the share-count convention for per-share multiples: primary, fully diluted, or partially
   diluted. If options are material, prefer valuing them separately and using actual shares
   (see S8 bridge rule).
5. For EV multiples, net cash out of the numerator, because interest income on cash is not in EBITDA
   or EBIT.
6. Correct cross holdings: subtract minority interests at estimated market value from EV when the
   firm consolidates a partly owned subsidiary; handle passive stakes as the mirror problem.
7. Confirm uniformity: every comparable's multiple was built with the same rules and the same
   accounting adjustments.

**Consistency rules (hard).**
- Claimholder match on both sides of the ratio.
- Same timing variant across every firm.
- Same share-count convention across every firm.
- EV numerator nets cash *iff* the denominator excludes interest income.
- Minority interests removed from EV whenever the denominator is consolidated.

**Outputs.** `multiple_spec = {numerator_type, denominator, timing_variant, share_count_convention,
cash_treatment, minority_treatment, adjustments_applied[]}`.

**Draws on:** `concepts/relative-valuation/multiple-definition-tests.md`,
`concepts/relative-valuation/four-step-multiple-framework.md`,
`concepts/dark-side-difficult/cross-holdings.md`,
`concepts/dcf-model-choice-loose-ends/cash-in-valuation.md`.

---

## S3 — Describe the distribution (four-step, step 2)

**Purpose.** You cannot call a multiple high or low without the current, local distribution. Fixed
thresholds decay and reverse.

**Inputs.** The multiple computed for every firm in the chosen universe (market, region, or sector) —
including the firms where it *cannot* be computed.

**Procedure.**

1. Compute the multiple for every firm in the universe. Record how many drop out and why (negative
   earnings, negative book equity, negative EBITDA).
2. Compute median, 10th/25th/75th/90th percentiles, and the mean. Expect mean >> median.
3. Use the **median** or a percentile band as "typical". Never the mean.
4. Handle outliers by capping or by percentile, not by one-sided trimming — outliers lie almost
   entirely on the positive side, so trimming biases the typical multiple downward.
5. Locate the subject firm's multiple as a percentile in that distribution.
6. Re-check by region. The same number can be cheap in one market and expensive in another.

**Decision rules with thresholds.**
- If **> 50% of the universe drops out** on this multiple, flag `sample_bias = high`; conclusions
  describe a profitable subsample, not the market. (Jan 2021: only 32.4% of US firms had a positive
  trailing PE; Canada 18.3%.)
- If **mean / median > 3**, the mean is unusable; the artifact must record medians only. (Jan 2021
  US trailing PE: mean 103.25, median 20.30.)
- Reject any absolute rule of thumb ("cheap under 6x EBITDA") unless it is restated as a percentile
  in the current distribution. 6x EV/EBITDA sat near the modal US bucket in Jan 2010 and below the
  10th percentile by Jan 2021 (US median 16.60); in Japan (median 8.46) it was near normal.
- Industry averages from the January-2022 US table are **averages, not medians**, and several
  trailing-PE cells are contaminated by near-zero-earnings firms (Environmental & Waste 735, Retail
  Distributors 897, Telecom Services 742, Metals & Mining 727). Never use a cell above ~100 as a
  sector anchor.

**Outputs.** `distribution = {universe, n_total, n_estimable, drop_reasons, median, p10, p25, p75,
p90, mean, subject_percentile, sample_bias}`.

**Draws on:** `concepts/relative-valuation/multiple-distribution-statistics.md`,
`concepts/relative-valuation/industry-average-multiples.md`.

---

## S4 — Analyze: derive the intrinsic multiple and name the companion variable (four-step, step 3)

**Purpose.** Every multiple is a compressed DCF. Recovering it names the variable you *must* control
for, and produces a justified multiple to compare against the traded one.

**Inputs.** The firm's growth, payout or reinvestment rate, return (ROE / ROC), margin, tax rate,
cost of equity or cost of capital, stable-growth assumption.

**Procedure.**

1. Classify the multiple as equity or enterprise (from S2).
2. Take the matching value model — DDM/FCFE for equity, FCFF for enterprise — in stable-growth form
   for a first pass, two-stage if a distinct high-growth phase exists.
3. Divide by the multiple's denominator and simplify. The master map of every intrinsic multiple and
   its drivers is in `concepts/relative-valuation/intrinsic-multiple-derivation.md`; per-family
   detail lives in the notes below.
4. Name the companion variable and record it.
5. Evaluate the intrinsic multiple at the firm's own fundamentals; compare against the traded
   multiple.
6. Never assume linearity. Check the sensitivity shapes before extrapolating.

**Multiple → companion variable → concept file.**

| Multiple | Companion variable | Secondary controls | Concept |
|---|---|---|---|
| PE (and forward PE) | expected growth | payout, cost of equity; growth×risk interaction | `relative-valuation/intrinsic-pe-fundamentals.md` |
| PEG | **not** growth-neutral: risk, payout, *level* of growth | use ln(growth) | `relative-valuation/peg-ratio.md`, `asset-based-private/peg-ratio-regression.md` |
| PBV | ROE | risk, growth, payout | `relative-valuation/book-value-multiples.md` |
| EV/Invested Capital | ROIC | debt ratio, growth | `relative-valuation/book-value-multiples.md` |
| EV/Sales, P/Sales | after-tax operating margin (net margin for P/S) | reinvestment, tax rate, growth | `relative-valuation/ev-sales-and-brand-value.md` |
| EV/EBITDA | reinvestment need (CapEx/EBITDA) | tax rate, cost of capital, growth, D&A/EBITDA | `relative-valuation/ev-ebitda-multiple.md` |
| EV/EBIT | reinvestment rate | tax rate, cost of capital | `relative-valuation/intrinsic-multiple-derivation.md` |
| Dividend yield | cost of equity, growth | — | `relative-valuation/intrinsic-multiple-derivation.md` |

**Decision rules with thresholds.**
- **Excess-return screen.** `PBV > 1 ⟺ ROE > cost of equity`; `EV/IC > 1 ⟺ ROC > WACC`. A firm with
  low PBV *and* low ROE is a bad business, not a bargain. Low PBV *and* high ROE is the classic
  candidate.
- **Reinvestment trap.** A low EV/EBITDA is deserved when CapEx/EBITDA is high or the asset base is
  aging. Do not call it cheap without computing CapEx/EBITDA, D&A/EBITDA, ΔWC/EBITDA and the
  effective tax rate for the firm and its peers.
- **Margin trap.** A low EV/Sales with a low operating margin is deserved.
- **PEG traps.** PEG falls with risk and with the level of growth, so a "cheap" PEG usually flags
  the riskiest or fastest-growing firm in the set. PEG is also biased *against* low-growth firms.
  Three checks before reading a low PEG as cheap: risk (beta vs peers), growth quality (reinvestment
  needed to buy the growth), growth level (distance from the peer average).
- **Internal-consistency check.** The fundamentals fed into any intrinsic multiple must satisfy
  `g = (1 − payout) × ROE` or `g = RIR × ROIC`. If they do not, the "justified" multiple describes a
  firm that cannot exist. (The canonical trap: ROE 15%, payout 40%, g 4% — sustainable growth is 9%,
  not 4%, and the long and short PBV forms disagree by a factor of 1.8 as a result.)

**Outputs.** `companion_variable`, `intrinsic_multiple`, `consistency_check{g_vs_ROE_payout,
g_vs_RIR_ROIC}`.

**Draws on:** `concepts/relative-valuation/intrinsic-multiple-derivation.md` plus the per-family
files above; `concepts/dcf-cashflows-growth/fundamental-growth-equity.md`,
`concepts/dcf-cashflows-growth/fundamental-growth-operating.md`.

---

## S5 — Build the comparable sample (four-step, step 4a)

**Purpose.** A comparable firm is one with similar **risk, growth and cash-flow characteristics** —
not one with the same SIC code. Sector membership is a starting heuristic, never the criterion
(`concepts/relative-valuation/comparable-selection-and-controls.md`).

**Inputs.** Sector classification by the business actually operated; screening criteria; peer
financials; region.

**Procedure.**

1. Fix the **four pricing-game choices** explicitly before assembling anything:
   - **Value measure** — equity, firm or enterprise? (Financial service firms force equity; sharply
     differing leverage forces enterprise.)
   - **Scalar** — revenues, earnings, cash flow or book value? Is it positive for every firm? How
     much do accounting choices distort it?
   - **Timing / normalization** — current, trailing, forward, far-forward? Where is the firm in its
     life cycle; how cyclical is the metric; do forecasts exist?
   - **Comparable group** — global or local; size-matched or all firms; how large a sample is needed
     and how will differences be controlled?
2. Choose a point on the **sampling spectrum**. A small tight sample needs few controls but yields
   noisy statistics; a large loose sample yields better statistics but demands heavy controls. Both
   are legitimate — the choice determines S6.
3. State the screens: industry, revenue floor, growth band, region. These are the most challengeable
   part of the analysis and must be recorded verbatim.
4. Clean the sample: drop firms where the multiple is not computable and record the count and reason;
   drop or flag outliers; do not silently lose money-losers.
5. Assign the firm to an industry by the business it operates, not by its listing classification.
6. For a non-US firm, decide region assignment now — a globally diversified company must not be
   assigned to a region by listing venue alone.

**Decision rules with thresholds.**
- Peer set size ≤ 25 → at most **one** explanatory variable at S6D.
- Peer set 15–30 → at most **two to three** explanatory variables.
- Peer set < 8 usable firms → the sector-regression branch is unavailable; fall back to S6B
  (story telling + median test) or escalate to S6E/S6F.
- If more than half the intended peer set drops out on the chosen scalar, the scalar is wrong;
  return to S2.
- If the sector's own fundamentals are uninformative (see the S7A trigger, sector regression
  R² ≈ 0), the sample is not the problem — the metric is.

**Outputs.** `peer_set[]` with per-firm multiple + companion variable + risk measure;
`sample_diagnostics = {n_screened, n_kept, n_dropped, drop_reasons, screens[], region}`.

**Draws on:** `concepts/relative-valuation/comparable-selection-and-controls.md`,
`concepts/relative-valuation/industry-average-multiples.md`,
`concepts/deliverables-worked-examples/relative-valuation-comparables-regression.md`.

---

## S6 — Choose the control technique (four-step, step 4b)

**Purpose.** Control for whatever differences remain. **The technique is selected by counting the
dimensions on which the subject differs from the peer set.** Getting this wrong means the reported
"mispricing" is the analyst's uncontrolled comparison.

**Selector.**

| Dimensions differing | Branch |
|---|---|
| none (true twins) | **S6A** direct comparison |
| one | **S6B** story telling / median test, or **S6C** modified multiple |
| several, peer set adequate | **S6D** sector regression |
| several, peer set inadequate or whole sector suspect | **S6E** market-wide regression |
| non-US firm | **S6F** regional cross-market regression |
| quick anchor / division-level | **S6G** industry-average scaling (used inside S10A) |

*(S6G is a sub-case of S6A/S6B applied to sector table anchors; it is counted with S6A.)*

### S6A — Direct comparison

**Fires when** the peer set genuinely matches on risk, growth and cash-flow characteristics.
**Rule.** Higher multiple = expensive, lower = cheap. **Output** the gap in multiple points and
percent. **Rarely legitimate** — record the evidence that no dimension differs.
Industry-average anchoring: read the industry multiple *and* its companion variable together, then
scale the industry multiple by the ratio of the firm's companion variable to the industry's
(`concepts/relative-valuation/industry-average-multiples.md`). This is mechanical once the rule is
fixed, but it controls for exactly one dimension.

### S6B — Story telling and the median test

**Fires when** exactly one fundamental differs, or as a screen before any regression.

**Story-telling procedure.** State the claim as a proposition about fundamentals ("trades at 12x
against 10x for the sector, but is cheap because its growth is much higher"), then **check the claim
against every firm in the table, not just the one you like**. A story that explains your favourite
and contradicts three others is not a control.

**Median test** (deterministic screen):
- Undervalued: multiple < sector median **AND** companion variable > sector median **AND** risk
  measure < sector median.
- Overvalued: multiple > sector median **AND** companion variable < sector median.
- Any other pattern → **the test has run out; escalate to S6D**. This is the explicit escalation
  trigger; do not force a verdict from a mixed pattern.

**Caveat.** The median test ignores the size of each gap and the correlation among the variables.
It is a screen, never a verdict.

**Draws on:** `concepts/relative-valuation/comparable-selection-and-controls.md`,
`concepts/relative-valuation/book-value-multiples.md`.

### S6C — Modified multiple (PEG and relatives)

**Fires when** exactly one dimension differs and folding it into the multiple is convenient.

**Rule.** A modified multiple does **not** neutralize the dimension it divides by. PEG still loads on
risk, payout and the level of growth. If any of the three PEG checks at S4 fails, abandon S6C and go
to S6D/S6E with ln(growth) as a regressor.

**Threshold.** Never screen on "PEG below 1"; that screen loads on high beta and mid-to-high growth.
Match the growth horizon to the EPS basis of the PE (a trailing PE with a five-year forward growth
rate is a definitional error).

**Draws on:** `concepts/relative-valuation/peg-ratio.md`,
`concepts/asset-based-private/peg-ratio-regression.md`.

### S6D — Sector regression

**Fires when** more than one fundamental differs and the peer set can support a regression. **This
is the normal case.**

**Procedure.**
1. Assemble the peer set with the multiple and its companion variables (chosen from the S4
   derivation, not from convenience).
2. Drop or flag non-computable firms; record the bias.
3. Regress. Keep the specification small (see S5 thresholds).
4. Check t-statistics. **t > 2 keep; 1 < t ≤ 2 marginal; t ≤ 1 drop and re-run.** In pricing, the
   market decides what matters — drop insignificant variables even when theory says they should
   matter.
5. Check R². Record it. A weak fit means the sector is *not* priced on those fundamentals; say so
   rather than pushing the prediction.
6. Evaluate the fitted equation at the subject's own fundamentals → `predicted_multiple`.
7. `over_under_pct = actual_multiple / predicted_multiple − 1`. Negative = trades below the sector's
   own pricing rule.
8. Ask what the regression omits before acting. A firm above the line may have an unmodelled
   advantage; below the line, an unmodelled problem.
9. Re-estimate every period. Sector coefficients move violently.

**Multiple-selection rule inside a sector.** When more than one multiple is available, **use the one
whose sector regression has the highest R²**. This is the same rule used to pick the "best multiple"
per division in sum-of-the-parts (S10A).

**Thresholds.**
- R² < 0.15 → prediction is weak evidence; it may be reported but must not carry the verdict.
- R² < 0.30 → weight the DCF above the regression at S15.
- A counter-intuitive coefficient sign is a warning about the sample, not a finding about value.
- Discard any predicted multiple that is economically implausible (negative, or an order of
  magnitude off) rather than averaging it in.

**Reference fits available in the concepts:** telecom PE on growth + emerging-market dummy
(R² 66.2%); European bank PBV on ROE + std deviation (R² 79%); US grocery P/S on net margin across
four vintages (R² 0.595 → 0.801 → 0.638 → 0.291 — the collapse is the lesson); six sector regressions
used for the UTC divisions (R² 36–55%); six project-level sector regressions (R² 25–56%).

**Draws on:** `concepts/relative-valuation/sector-regressions.md`,
`concepts/deliverables-worked-examples/relative-valuation-comparables-regression.md`,
`concepts/asset-based-private/sum-of-the-parts-pricing.md`.

### S6E — Market-wide regression

**Fires when** several dimensions differ and either the peer set is inadequate, or the peer group
itself may be mispriced, or a second independent benchmark is wanted.

**Procedure.**
1. Pick the universe (US, region, global) and the predictors from the S4 derivation: payout, beta,
   expected EPS growth for PE; add ROE for PBV; debt ratio, growth, tax rate for EV/EBITDA;
   margin for EV/Sales; ROIC for EV/IC.
2. Run weighted least squares by market cap if the result should reflect where the money is.
3. Apply the same t-statistic ladder as S6D. Dropping an insignificant variable rarely costs
   explanatory power (Jan 2021 US PE: dropping beta moved R² from 0.396 to 0.389).
4. If the intercept is negative, predicted multiples can come out negative. Fix by re-running
   through the origin — imperfect but usable.
5. Inspect the correlation matrix. **Wrong-sign coefficients are a multicollinearity symptom, not a
   discovery.** (Jan 2021 US: growth vs payout −0.220, growth vs beta −0.093, payout vs beta +0.080.)
6. Evaluate at the subject's inputs; compare with the traded multiple.
7. **State the benchmark explicitly.** Market-wide and peer-group verdicts can disagree, because the
   peer group may itself be mispriced against the market. Both are correct answers to different
   questions.

**Units rule (hard).** Two forms of the same equation circulate. The SPSS output enters payout and
growth as *absolute percent* (25% → 25); the slide form enters them as *decimals* (25% → 0.25) with
coefficients scaled by 100. Record which form the coefficients belong to and validate against a
known worked case before use.

**Secondary output — the market price of growth.** The growth coefficient is the market's price for
an extra percentage point of expected growth. It has ranged from **0.41 (Jan 2012) to 2.62 (Jan 2003)**
over two decades and was 2.28 in Jan 2021. Report it alongside the implied ERP as a regime marker.

**Draws on:** `concepts/relative-valuation/market-wide-regressions.md`,
`concepts/asset-based-private/market-multiple-regression.md`,
`concepts/deliverables-worked-examples/market-wide-multiple-regression.md`.

### S6F — Cross-market (regional) regression

**Fires when** the subject is outside the US, or when a portable pricing rule is wanted.

**Procedure.**
1. Assign the region: US, Europe, Japan, Emerging Markets, Australia/NZ/Canada, or Global as
   fallback. A globally diversified firm must not be assigned by listing venue; use operating
   exposure (see S7E).
2. Pick the multiple whose companion variable can be measured reliably for this firm.
3. Look up the regional regression and **check its R² first** — that is the trust weight.
4. Compute inputs on the exact definitions, **in decimals**.
5. Evaluate; compute `actual/predicted − 1`.
6. Run more than one multiple when possible. Agreement strengthens the verdict; disagreement points
   to an input problem or an unmodelled feature. **When they conflict, prefer the multiple with the
   highest regional R².**

**Trust ladder (Jan 2021 regional fits, from the concept tables).** EV/Invested Capital 50.5–62.8%
(strongest of any multiple family, everywhere); PBV 27.8–48.3%; EV/Sales 13.2–31.8%; PE 14.5–39.4%;
EV/EBITDA 10.3–27.8%; PEG 11.3–33.2%. **R² < 15% → weak evidence; do not let it carry a verdict**
(Japan EV/EBITDA is 10.3%).

**Vintage rule (hard).** Never mix coefficient vintages. Jan 2020 and Jan 2021 US equations differ
sharply (US PE R² 25.2% → 39.4%; the growth coefficient 137.19 → 228.40 in decimal form). Record the
`as_of` date of every regression used, and refresh when more than a year stale.

**Draws on:** `concepts/relative-valuation/cross-market-multiple-regressions.md`,
`concepts/relative-valuation/book-value-multiples.md`,
`concepts/relative-valuation/ev-ebitda-multiple.md`,
`concepts/relative-valuation/ev-sales-and-brand-value.md`.

**S6 outputs (all branches).** `control_method`, `predicted_multiple`, `fit = {r2, t_stats,
n, specification, as_of, units}`, `over_under_pct`, `benchmark_named`, `omitted_dimensions[]`.

---

## S7 — Company-type overrides

These branches fire from the S1 classification and modify S2–S6 rather than replacing them. Several
can fire at once; apply them in the order given, because each changes the inputs of the next.

### S7A — Young, negative-earnings or pre-revenue firms

**Trigger.** Negative or trough earnings across the *sector*, not just the firm; or a regression of
the multiple on its conventional companion variable across the sector returns **R² ≈ 0 with an
insignificant slope** (early-2000 internet stocks: `PS = 81.36 − 7.54 × Net Margin`, t = 0.49,
R² = 0.04). That is the diagnostic: current fundamentals are uninformative.

**Three routes, run in this preference order.**

1. **Survival and growth proxies.** Replace the conventional companion variable with what actually
   separates survivors from failures: revenue scale (as a size control, keep it even if
   insignificant), revenue growth, and cash relative to revenues (the survival proxy). Fit the
   regression, check significance, predict.
2. **Forward multiple with the full haircut sequence.** Apply **all six steps, in order** — skipping
   any one overstates today's value, usually by a large factor:
   (i) value in year N from the forward multiple; (ii) discount N years at the **risk-adjusted cost
   of capital, never the riskfree rate**; (iii) subtract expected dilution from equity issued to
   fund growth; (iv) multiply by (1 − probability of failure); (v) adjust for debt and cash;
   (vi) subtract the option overhang. In the Tesla case a year-10 value of 68,271 becomes 8,152
   today; discounting alone leaves 52,050, so steps (iii)–(vi) do most of the work.
3. **Let the market pick the metric.** Build the correlation matrix of market cap and enterprise
   value against every available operating metric across the sector; price on the winner. (Social
   media, Oct 2013: users correlated 0.9812 with market cap, above revenues 0.8933 and EBITDA
   0.9709.) **Caveat:** a per-user multiple only works while the market is paying per user, and it
   says nothing about monetization — Netflix's EV/User of $576.82 against Trulia's $20.59 is a
   statement about business models, not about value.

**Mandatory disclosure.** Report the result as relative and state explicitly what would have to be
true for the *whole sector* to be correctly priced. Amazon in early 2000 was undervalued relative to
other internet stocks — a group that was collectively overpriced.

**Cross-check.** Excess growth over the industry average dies within roughly **five years** of an
IPO. A forward multiple built on a decade of above-industry growth fails this screen.

**Draws on:** `concepts/relative-valuation/pricing-young-companies.md`,
`concepts/dark-side-difficult/young-company-valuation.md`,
`concepts/dark-side-difficult/dilution-and-employee-options.md`,
`concepts/dark-side-difficult/distress-and-failure-adjusted-value.md`.

### S7B — Financial service firms

**Trigger.** Bank, insurer, brokerage, or any firm where debt is raw material.

**Overrides.** Enterprise multiples are blocked (S1). Use PE and **PBV with ROE as the companion
variable** — the tightest empirical relationship in the whole area. Regress PBV on ROE plus a risk
measure (standard deviation) across the peer set; the European bank case fits at R² 79%.

**Additional rules.**
- Normalize ROE for any required increase in regulatory capital before using it as the companion
  variable: `Adjusted ROE = Trailing ROE / (1 + required capital increase)`. Leverage-driven ROE does
  not survive re-regulation.
- The hard constraint with no analogue elsewhere: a bank breaching its regulatory capital ratio can
  be shut down however good its earnings look. A pricing verdict on a bank near its minimum must
  carry a wipeout-probability overlay (S15).
- Industry-average tables show NA for EV/EBITDA, ROC and reinvestment for banks and brokerages. That
  NA is informative, not missing data.

**Draws on:** `concepts/relative-valuation/book-value-multiples.md`,
`concepts/dark-side-difficult/financial-service-firm-valuation.md`,
`concepts/dark-side-difficult/bank-fcfe-and-excess-return-models.md`,
`concepts/accounting-statements/sector-differences-in-financial-statements.md`.

### S7C — Cyclical and commodity firms

**Trigger.** The firm's earnings are driven by a cycle or a commodity price, and the current year sits
at an extreme.

**Overrides.**
- **Normalize before pricing.** Three approaches, in ascending order of information needed:
  (1) average EBIT over a full cycle (≈5 years) — only when scale has not changed; (2) average
  pre-tax ROC × current book capital — when the firm has grown; (3) **sector or own aggregate
  historical margin × current revenues** — the default when revenue is stable and margins have
  collapsed. Use the aggregate `ΣEBIT/ΣRevenues`, never an average of annual margin ratios.
- Legitimacy test: normalize only if the trouble is temporary (peers show the same pattern; the firm
  earned normal margins for years; the balance sheet survives until recovery). If losses come from a
  broken model, a permanent demand shift or crushing leverage, normalizing is wishful thinking →
  route to S7A or the distress overlay.
- Recompute everything downstream from the normalized figure: coverage ratio, synthetic rating, cost
  of debt, ROC, reinvestment rate. **Resolve the circularity** (rating ← EBIT ← lease adjustment ←
  cost of debt ← rating) by iterating to a fixed point.
- Never use a single year's industry-average table for a cyclical industry near a peak or trough.

**Draws on:** `concepts/dark-side-difficult/normalized-earnings.md`,
`concepts/dark-side-difficult/commodity-and-cyclical-valuation.md`,
`concepts/cost-of-debt-capital/synthetic-rating.md`.

### S7D — Intangible-heavy firms

**Trigger.** R&D-intensive (pharma, technology), human-capital-intensive (consulting), or
brand-driven consumer businesses.

**Overrides.** Capitalize R&D (and recruiting/training, and the brand-building share of advertising)
**before** any multiple is computed, and apply the same treatment to every comparable. Consequences
that must all move together: EBIT and net income rise (or fall, when R&D spending is shrinking);
book equity and invested capital rise; ROE and ROC usually **fall**; capex must include current-year
R&D; the coverage ratio and hence the synthetic rating change.

**Brand valuation via the margin route.** Value the firm twice — once at its own after-tax operating
margin, once at a credible generic producer's — holding revenues, capital turnover, cost of capital,
growth period and stable-phase assumptions fixed, and letting ROC and growth adjust because
`ROC = margin × sales/capital` and `g = RIR × ROC`. The difference is the brand.
`Brand value = [(V/S)_branded − (V/S)_generic] × Sales`.

**Hard rule.** Never add brand value on top of a valuation whose margins already reflect brand
pricing power. That is the same double count as adding a brand premium to a completed DCF.

**Draws on:** `concepts/dark-side-difficult/capitalizing-rd.md`,
`concepts/relative-valuation/ev-sales-and-brand-value.md`,
`concepts/dcf-model-choice-loose-ends/other-non-operating-assets.md`.

### S7E — Emerging-market and multinational firms

**Trigger.** Material operations outside the region of incorporation, or material country risk.

**Overrides.**
- **Region assignment by exposure, not passport.** Assign the S6F region and any country adjustment
  by revenue weights or lambda, not by listing venue. An exporter carries far less home-country risk
  than a domestic retailer with the same passport.
- **Cross holdings first.** If holdings exceed roughly one third of value, price the operating
  business separately and add the stakes; a multiple on consolidated numbers is meaningless. Value
  minority (unconsolidated) stakes and **add**; value the minority interest in consolidated
  subsidiaries at market and **subtract**. Report the composition (operating / holdings / cash) as
  percentages. (Tata Chemicals and Tata Steel: roughly half of value sat in holdings.)
- **Currency.** Cash flows, growth and discount rate must live in one currency. The equity risk
  premium tracks operating exposure and does **not** change when the unit of account changes.
- **Never stack.** A country risk premium in the discount rate *plus* an emerging-market discount on
  the value *plus* a governance discount is three charges for overlapping risks.
- A cross-market regression's emerging-market coefficients already embed average country risk;
  adding a separate country haircut on top double counts.

**Draws on:** `concepts/dark-side-difficult/country-risk-exposure.md`,
`concepts/dark-side-difficult/cross-holdings.md`,
`concepts/dark-side-difficult/currency-consistency-and-invariance.md`,
`concepts/dark-side-difficult/return-improvement-and-governance-drag.md`,
`concepts/cost-of-equity/operation-weighted-erp.md`.

### S7F — Declining and distressed firms

**Trigger.** Falling revenues, sub-WACC returns, high leverage, or a real chance of not surviving.

**Overrides.**
- A low multiple on a declining firm is usually deserved. Check whether the sector median margin is
  reachable before treating the gap as mispricing.
- **Distress must be handled as a probability weight on value, never as a higher multiple or a higher
  discount rate.** Get the probability from (in ascending order of information content) the bond
  rating's historical cumulative default rate; a statistical model; or by inverting a traded bond
  price (discount promised payments at the **riskfree rate**, weight by survival, solve for the
  annual π, then convert to the cumulative probability over the forecast horizon). The bond-implied
  number is usually far more pessimistic than the rating table — that gap is information, not error.
- Check whether equity gets anything: if expected distress proceeds < face value of debt, equity is
  worth **zero** in that branch.
- **Liquidation cross-check.** If liquidation value (S11) exceeds going-concern value, the business
  is worth more dead than alive, and the value of continuing operations is negative.
- **Equity-as-call-option trigger.** Loss-making **and** market debt-to-capital **> 50%** → value
  equity as a call option on firm value as an additional estimate.

**Draws on:** `concepts/dark-side-difficult/declining-firm-valuation.md`,
`concepts/dark-side-difficult/distress-and-failure-adjusted-value.md`,
`concepts/dark-side-difficult/bond-implied-distress-probability.md`,
`concepts/deliverables-worked-examples/equity-as-call-option-valuation.md`,
`concepts/asset-based-private/liquidation-valuation.md`.

---

## S8 — Predicted multiple → value → value per share

**Purpose.** Turn a multiple into a number that can be compared with a price.

**Inputs.** `predicted_multiple` (S6); the subject's matching scalar; balance-sheet bridge items.

**Procedure.**

1. **Match multiple to scalar.** An EV/Capital multiple applied to EBITDA, or an equity multiple
   applied to an enterprise scalar, is an error, not an approximation.
2. `implied_value = predicted_multiple × scalar`.
3. If the multiple is an enterprise multiple, bridge to equity:
   `Equity = Enterprise value + cash + cross holdings + other non-operating assets − all debt
   (including capitalized leases and any captive finance arm's debt) − minority interests
   − other claims (pension underfunding, contingent liabilities)`.
4. Subtract the value of employee options, warrants and conversion options.
5. Divide by **actual** shares outstanding, plus every claim that converts to common (convertible
   preferred, RSUs, shares owed under acquisition agreements), **excluding options**.
6. Also compute the peer-average implied price as a second, cruder estimate; report both separately.

**Consistency rules (hard).**
- Options are handled **once**: either subtract their value and divide by actual shares, or use a
  diluted count — never both.
- Cash is handled **once**: either inside the flows or added in the bridge.
- A stake valued separately must not also sit inside the operating numbers.
- Book debt is never subtracted from a market-based enterprise value; use market value of debt.
- Goodwill is an accounting residual, never an asset to add.
- Gross-debt and net-debt conventions are never mixed within one valuation.

**Outputs.** `implied_value_enterprise`, `implied_value_equity`, `implied_value_per_share`,
`peer_average_implied_price`, `bridge[]`.

**Draws on:** `concepts/dcf-model-choice-loose-ends/equity-value-bridge.md`,
`concepts/dcf-model-choice-loose-ends/cash-in-valuation.md`,
`concepts/dcf-model-choice-loose-ends/employee-option-per-share-approaches.md`,
`concepts/dark-side-difficult/dilution-and-employee-options.md`,
`concepts/asset-based-private/sum-of-the-parts-pricing.md` (bridge worked end to end),
`concepts/asset-based-private/ipo-valuation.md` (share-count treatment of converting claims).

---

## S9 — Multi-multiple reconciliation and the pricing verdict

**Purpose.** Produce one pricing verdict from several multiples and several benchmarks, without
averaging away the information in their disagreement.

**Inputs.** Every `(multiple, control_method, benchmark, predicted_multiple, implied_price, fit)`
tuple produced; the market price.

**Procedure.**

1. Assemble the estimate table: peer-average price, sector-regression price, market-regression price,
   regional-regression price, industry-anchor price — one row per method, with its R² and its
   benchmark.
2. **Discard implausible estimates and say why.** Do not let them into an average. (The canonical
   failure: applying a US PEG regression to a firm in another market produced a predicted price three
   orders of magnitude off; it was rejected outright.)
3. Weight by fit: prefer the multiple with the highest R² for this sector/region; downweight anything
   under 0.30; do not act on anything under 0.15.
4. **Read the disagreements as findings.** Sector-regression vs market-regression disagreement means
   the sector is pricing a driver differently from the market as a whole — that is the finding. Peer
   average vs sector regression disagreement means the subject is not the median firm in its sector.
5. Emit the verdict with its benchmark attached, never as an absolute claim.

**Thresholds.**
- `over_under_pct` beyond ±20% on the highest-R² method → material; carry to S15.
- Two independent methods agreeing within ~5% → agreement is itself evidence; state it.
- All methods except one pointing the same way → strong evidence; state which one dissents and why.

**Outputs.** `pricing_verdict = {estimates[], preferred_method, preferred_price, over_under_pct,
benchmark, dissenting_methods[], confidence}`.

**Draws on:** `concepts/relative-valuation/comparable-selection-and-controls.md`,
`concepts/relative-valuation/cross-market-multiple-regressions.md`,
`concepts/deliverables-worked-examples/valuation-triangulation-and-recommendation.md`,
`concepts/deliverables-worked-examples/market-wide-multiple-regression.md`.

---

## S10 — Sum-of-the-parts (multi-business firms)

**Purpose.** Value a multi-business firm piece by piece. The route is set by the motive at S0; in
practice run **both** and compare four numbers.

**Inputs.** Segment disclosures: revenues, operating income, capital invested, and ideally capex and
D&A per segment; unallocated corporate expenses; cash; cross holdings; minority interests; all debt
including any captive finance arm's; option value; share count.

**S10 shared setup.**

1. **Define the parts.** Use reported segments unless you can do better. Reconcile segments +
   eliminations to consolidated totals; if they do not tie, a corporate or elimination column has
   been missed. Separate business-type segments from geographic ones — mixing them double-counts.
2. **Normalize segment earnings** if the latest year is unrepresentative. The standard technique:
   apply each segment's multi-year average margin (e.g. 5-year) to current-year revenues. Segment
   EBITDA when only EBIT is reported: `EBITDA_i = Normalized EBIT_i + D&A_i`.
3. **Account for everything the segments do not contain**: unallocated corporate expenses, cash,
   cross holdings, minority interests, debt. Every one must appear in the bridge or the total is
   wrong.

### S10A — Pricing the parts (relative route)

**Fires for** activists, acquirers, boards weighing a break-up, liquidators, accountants.

**Procedure.**
1. Assign each division to a sector and collect that sector's peer group.
2. **Choose the multiple per sector by highest regression R².** Do **not** force one multiple across
   all divisions — the crude single-multiple version understated one worked case by $12.6bn against
   the fundamentals-controlled version ($61.7bn → $74.2bn).
3. Estimate (or look up) the sector regression of that multiple on its companion variables. Common
   forms: `EV/EBITDA = a + b·TaxRate + c·ROC`; `EV/Revenues = a + b·Pre-tax operating margin`;
   `EV/Capital = a + b·ROC` — all fundamentals in decimals.
4. Evaluate at the **division's own** ROC, margin and tax rate → division-specific predicted
   multiple.
5. `Value(Division_i) = predicted multiple × the division's matching scalar`.
6. Sum. Subtract the **capitalized value of unallocated corporate expenses** if segment earnings were
   reported before corporate G&A (formula in S10B).
7. Bridge to equity (S8 rules), remembering a captive finance arm's debt as a separate subtraction.

**Crude fallback.** Median sector multiple × division scalar. Legitimate only as a floor or as a
liquidator's estimate; record that it controls for nothing.

**Draws on:** `concepts/asset-based-private/sum-of-the-parts-pricing.md`,
`concepts/relative-valuation/sector-regressions.md`,
`concepts/relative-valuation/industry-average-multiples.md`,
`concepts/accounting-statements/segment-and-geographic-reporting.md`.

### S10B — Valuing the parts (intrinsic route)

**Fires for** passive long-term investors betting on a correction, and as the reservation price for
any seller.

**Procedure.**
1. **Every division gets its own cost of capital.** Take a bottom-up unlevered beta from the
   division's sector, lever at the company's D/E (unless the division would carry different debt
   standalone), and combine with the company's after-tax cost of debt and weights.
2. Build each division's `ROC = after-tax operating income / capital invested` and
   `RIR = allocated reinvestment / after-tax operating income`; set `g = RIR × ROC`.
3. **Growth-period decision rule: if a division's ROC ≤ its cost of capital, give it a zero-year
   growth period.** Growth there destroys value; its entire value is terminal. Otherwise the default
   is 5 years.
4. **Stable-ROC decision rule: terminal ROC = the division's cost of capital**, unless a durable
   competitive advantage is argued explicitly.
5. Discount each division's FCFF at its own cost of capital. A very high reinvestment rate makes
   near-term FCFF negative — that is arithmetic, not an error.
6. Capitalize unallocated corporate expenses as a growing perpetuity at the **company-wide** cost of
   capital and subtract:
   `Value of corporate expenses = Corporate expenses × (1 − t) × (1 + g) / (WACC_company − g)`.
7. Bridge to equity (S8 rules).

**Hard rule.** One company-wide cost of capital across divisions is the single most common error and
it moves the answer a lot (one worked case spans 6.78% to 9.94% across six divisions).

**Draws on:** `concepts/asset-based-private/sum-of-the-parts-dcf.md`,
`concepts/cost-of-debt-capital/divisional-cost-of-capital.md`,
`concepts/cost-of-equity/bottom-up-beta.md`,
`concepts/dcf-cashflows-growth/terminal-value.md`.

### S10C — The four-number comparison

**Purpose.** The spread between the four estimates *is* the finding.

**Procedure.** Assemble and compare:
1. Sum of the parts, intrinsic (S10B).
2. Sum of the parts, relative (S10A).
3. Whole-company DCF (from the intrinsic framework).
4. Enterprise value at market prices.

`Conglomerate discount = 1 − (Market enterprise value / Sum-of-the-parts value)`.

**Decision rules.**
- For an **activist**, the operative number is the relative sum of the parts, because a break-up
  realizes sector prices.
- For a **passive investor**, the operative number is the intrinsic sum of the parts, because the
  thesis is that the market will eventually pay for the cash flows.
- A conglomerate discount is **not** automatic free money. Test three alternatives first:

| Alternative explanation | What it means |
|---|---|
| No buyer | The pieces only fetch peer multiples if somebody actually buys them |
| Real cost of conglomeration | Bad capital allocation, cross-subsidy or entrenchment can justify the discount |
| Genuine synergy | Real cross-division synergies make the pieces worth *less* apart than together |

- Weight by the probability that a break-up actually happens; a theoretical break-up value is not a
  price.

**Outputs.** `sotp = {divisions[], intrinsic_total, relative_total, whole_company_dcf, market_ev,
conglomerate_discount, operative_number, probability_of_breakup}`.

**Draws on:** `concepts/asset-based-private/sum-of-the-parts-framework.md`,
`concepts/asset-based-private/sum-of-the-parts-pricing.md`,
`concepts/asset-based-private/sum-of-the-parts-dcf.md`,
`concepts/dark-side-difficult/value-of-control-and-restructuring.md`.

---

## S11 — Liquidation valuation

**Purpose.** What the assets fetch sold piecemeal today.

**Inputs.** Asset classes that can genuinely be sold separately; recent arm's-length transaction
evidence per class; book values as fallback; liabilities; the sale timetable.

**Procedure.**

1. Break the business into separately saleable asset classes (real estate, equipment, receivables,
   inventory, whole divisions, intangibles with transferable title).
2. Choose the evidence source per class in this priority order:

| Priority | Evidence available | What to do |
|---|---|---|
| 1 | Recent arm's-length transactions in similar assets | Price directly off them. This is the preferred route |
| 2 | No active market, but a reliable carrying amount | Use book value as a proxy, flagged as such |
| 3 | Neither | The asset is probably not separable. Question whether liquidation is the right frame |

3. **Do not build a DCF of each asset.** Liquidation is a pricing exercise; the buyer's cash flows,
   not yours, set the price.
4. Classify the liquidation as orderly or urgent. Apply an additional fire-sale discount `d_urgency`
   only when urgent (creditor-forced sale, bankruptcy timetable, thin credit market, few bidders).
   Size grows with asset specificity, thinness of the buyer pool, and shortness of the window. An
   orderly divestiture programme takes **no** urgency discount.
   The empirical bracket for "cannot sell freely right now": restricted-stock discounts ~33–35%,
   pre-IPO discounts ~42–60% — both heavily sampling-biased; the pure illiquidity component may be
   under 10% (`concepts/asset-based-private/silber-restricted-stock-regression.md`).
5. `Liquidation value of equity = Σ estimated sale prices × (1 − d_urgency) − liabilities`.
6. Compare with going-concern value. **If liquidation > going concern, the value of continuing
   operations is negative** — that is the finding.

**Hard rules.** Book value is a proxy of last resort and is usually far too high for specialized or
obsolete assets. Never add back going-concern items (brand, assembled workforce, synergies) that do
not survive a piecemeal sale.

**Outputs.** `liquidation_value = {asset_classes[], evidence_source_per_class, d_urgency,
gross_proceeds, liabilities, equity_value, vs_going_concern}`.

**Draws on:** `concepts/asset-based-private/liquidation-valuation.md`,
`concepts/asset-based-private/asset-based-valuation-overview.md`,
`concepts/asset-based-private/silber-restricted-stock-regression.md`,
`concepts/dark-side-difficult/distress-and-failure-adjusted-value.md`.

---

## S12 — Fair value (FAS 157 / accounting mandate)

**Purpose.** Restate an asset or liability at its **exit price** — the price a market participant
would pay to take it, not what it is worth to you and not an entry price.

**Procedure — the measurement hierarchy, in strict order.**

| Level | Input | Approach | Rule |
|---|---|---|---|
| 1 | quoted price, active market, identical asset | pure pricing | if found, that **is** fair value; stop |
| 2 | observable prices/inputs for similar assets | pricing with adjustment | use a sector regression evaluated at the asset's own fundamentals |
| 3 | unobservable inputs, entity's own assumptions | intrinsic model (DCF) | only when 1 and 2 fail |

**Decision rules.**
- Report the level used. A balance sheet dominated by level 3 is a balance sheet of opinions.
- **Reverse-engineering check.** When a level 3 model is used to support a level 1 or 2 number,
  check the direction of causation. If the model's assumptions were chosen to reproduce a value
  already decided, the "valuation" is a rationalization and must be flagged.
- Never treat a level 3 number as carrying level 1 reliability.
- Fair value restates assets one at a time; it still misses anything that exists only at the business
  level.

**Outputs.** `fair_value = {asset, exit_market, level_used, inputs[], value, reverse_engineering_flag}`.

**Draws on:** `concepts/asset-based-private/fair-value-accounting-fas157.md`,
`concepts/asset-based-private/sum-of-the-parts-pricing.md`,
`concepts/accounting-statements/balance-sheet-views-and-asset-measurement.md`,
`concepts/accounting-statements/intangibles-and-goodwill.md`.

---

## S13 — Market- and country-level pricing

**Purpose.** Apply the same discipline to a whole market. Two independent checks; run both.

### S13a — Country PE against fundamentals

`PE = a + b·Interest Rate + c·Real GDP Growth + d·Country Risk`, with rates and growth as decimals
and the risk score on the scale the equation was fitted on.

**Rules.** Signs must match theory (rates negative, real growth positive, risk negative); a wrong
sign means collinearity or a bad risk measure. A large negative residual is a **candidate, not a
conclusion** — the three variables omit currency risk, governance, accounting quality and index
sector mix. Refit whenever rates or risk scores move materially; the published coefficients are a
snapshot, and a 16-observation, 3-predictor fit is fragile.

**The lesson to encode:** low headline PEs usually pair with high rates, low growth and high country
risk, all of which justify them. Controlling for fundamentals routinely reverses the raw ranking.

### S13b — Market PE against the bond alternative

1. Compute the index PE on at least two bases: raw PE and a normalized/Shiller PE (raw PE is jumpy on
   cyclical or crisis earnings).
2. Compare each with its own long-run average; note the verdict but do not stop there.
3. `T.Bond PE = 1 / ten-year Treasury rate`.
4. `Relative measure = Shiller PE / T.Bond PE`; compare with its own historical average (≈1.06 for
   1970–2020).
5. **Decision rule: ratio below its average → stocks are cheap relative to bonds even when their own
   PE looks high.** Both statements ("expensive on its own history", "cheap against bonds") can be
   true at once; the second governs an allocation decision.
6. Cross-check with the earnings-yield regression on the T.Bond rate and the term-structure spread;
   invert the predicted E/P for a predicted market PE.
7. Treat the regression cautiously post-2008: the fit fell (50.71% → 44.81%) and the term-structure
   variable lost significance once rates were managed near zero.

**Caveat that must be printed with any output.** "Cheap versus bonds" compares two possibly
overpriced assets. It is still a relative statement.

**Outputs.** `market_pricing = {country_pe_actual, country_pe_predicted, gap, index_pe_variants,
tbond_pe, shiller_to_bond_ratio, ratio_vs_average, regression_predicted_pe, verdict, caveats[]}`.

**Draws on:** `concepts/relative-valuation/country-pe-regression.md`,
`concepts/relative-valuation/market-pe-vs-bond-alternative.md`,
`concepts/relative-valuation/multiple-distribution-statistics.md`,
`concepts/dark-side-difficult/market-and-macro-crisis-valuation.md`.

---

## S14 — Stake, control and liquidity adjustments

**Purpose.** A business does not have one value. It has a value per buyer, per stake and per purpose.
These adjustments sit on top of any output from S8, S9, S10 or S11 — never inside them.

**Order of application (fixed).**

1. **Key person** — applied to **operating income**, before growth and reinvestment, never to the
   final value. `Operating income after departure = Adjusted operating income × (1 − k)`, where `k`
   is the share of the business that leaves with the owner. It is distinct from the market-salary
   adjustment: the salary prices the owner's *work*, `k` prices the owner's *pull*. `k` is
   negotiable — transition arrangements, non-competes and earn-outs shrink it. Applying it to value
   alone misses the interaction with reinvestment and growth
   (`concepts/asset-based-private/key-person-discount.md`).
2. **Control / minority** — computed from two valuations, never looked up.
   `Value of control = Optimal equity value − Status quo equity value`;
   `Minority discount = (Optimal − Status quo) / Optimal`.
   Price a stake **> 50%** off the optimal value and a stake **< 50%** off the status quo value.
   Refine by the probability that control actually changes:
   `Expected value = Status quo × (1 − P) + Optimal × P`.
   **Validity gate:** the analysis is meaningful only if the market or transaction price lies between
   the status-quo and optimal values. If Optimal < Status quo, the inputs are invalid, not the
   finding. If Optimal ≤ 0, the discount is undefined
   (`concepts/asset-based-private/minority-discount.md`,
   `concepts/acquisitions-control-enhancement/voting-premium-and-minority-discount.md`).
   **Reject all fixed-percentage control premiums.** A perfectly run target carries a control premium
   of **zero**, whatever a survey says. If you cannot name a specific change you would make, the
   premium is zero (`concepts/acquisitions-control-enhancement/control-premium-rules-of-thumb.md`).
3. **Voting premium** — where two share classes exist, spread the status-quo value across **all**
   shares (both classes own the same cash flows) and attach only the expected control increment
   `P × (Optimal − Status quo)` to the voting shares. Assign no premium where charters, law or
   tag-along rights protect the non-voting class. Part of an observed spread is liquidity, not
   control.
4. **Illiquidity** — applied to **equity value**, not firm value, and only when the buyer cannot exit
   into a market.
   **Applies:** private-to-private buyer. **Does not apply:** publicly traded acquirer (its investors
   can sell), IPO buyer, any listed subject.
   Three routes, in descending order of defensibility: (a) the bid-ask spread regression evaluated at
   zero trading volume — most firm-specific, drawn from a large unbiased sample, and materially
   smaller than the rules of thumb; (b) the Silber-refined base, restricted-stock anchored and
   varying with size and profitability; (c) a flat 20–30% as a sanity check only. Overlay the three
   dimensions the models cannot see: **company** (larger/healthier/profitable/liquid assets → smaller),
   **time** (tight credit and bad economy → larger), **buyer** (short horizon and high cash needs →
   larger). Report which route was used — the spread between the crudest and the most refined route
   was ~16% of equity value in the worked restaurant case
   (`concepts/asset-based-private/illiquidity-discount.md`,
   `concepts/asset-based-private/bid-ask-spread-illiquidity-regression.md`,
   `concepts/asset-based-private/silber-restricted-stock-regression.md`).
5. **Complexity / opacity** — pick **one** route (cash flows, discount rate, growth, or a final
   haircut) and never stack them (`concepts/dcf-model-choice-loose-ends/complexity-discount.md`).

**Hard rules.**
- Illiquidity and lack of control are **different frictions**. Applying both to the same stake needs
  a reason, not reflex.
- Never stack a discount that the pricing benchmark already contains. If the peer set is itself
  illiquid, the multiple already embeds illiquidity.
- The discount rate, not the discount, carries the buyer's diversification. An undiversified buyer
  uses a total beta; a diversified buyer uses the market beta. Do not express diversification twice.
- Quote different numbers to different parties knowingly: the seller's value and the buyer's value
  are both correct and answer different questions. The gap is the bargaining range, and where the
  price lands inside it depends on the number of bidders and the urgency of each side
  (`concepts/asset-based-private/private-to-public-sale.md`).

**Outputs.** `stake_adjustments = {k_applied_to, control_value, minority_discount, P_change,
voting_premium, illiquidity_route, illiquidity_pct, complexity_route, final_value,
bargaining_range}`.

**Draws on (additionally):** `concepts/asset-based-private/private-company-valuation-framework.md`,
`concepts/asset-based-private/private-to-private-valuation.md`,
`concepts/asset-based-private/total-beta.md`,
`concepts/asset-based-private/vc-stage-varying-cost-of-equity.md`,
`concepts/asset-based-private/ipo-pricing-and-underpricing.md`.

---

## S15 — Reconciling pricing with intrinsic value → recommendation

**Purpose.** The terminal stage. Convert conflicting numbers into one decision with the reasoning
visible. **Never average a DCF and a pricing estimate into one number** — explain the gap.

**Inputs.** `pricing_verdict` (S9) and/or `sotp` (S10) and/or `liquidation_value` (S11); the DCF value
per share and its sensitivity range from the intrinsic framework; the market price; the news history
for the analysis period.

**Procedure.**

1. **News check first.** Review events during the analysis period. Ask whether any changes the
   narrative and therefore the inputs. Update before recommending. A valuation built on a narrative
   events have overtaken is worse than none.
2. **Build the final analysis table.** Standard rows: current price; DCF base; DCF low and high from
   the sensitivity grid; peer-average implied price; sector-regression implied price; market- or
   regional-regression implied price; sum-of-the-parts (both routes) where applicable; liquidation
   value where applicable; option value where the S7F trigger fired.
3. **Discard implausible estimates explicitly**, with the reason, rather than letting them drag an
   average. Also discard sensitivity-grid extremes that were already rejected in the sensitivity
   analysis itself.
4. **Weight and defend the weighting.** Default: **when comparables selection is ambiguous, weight
   the DCF above the relative-valuation regressions** — the DCF carries the richest information and
   its assumptions are auditable. Raise the weight on pricing when the mandate is to transact today
   (IPO, sale, break-up), when the horizon is short, when the analyst is judged on relative
   performance, or when the DCF inputs are unusually speculative.
5. **Look for unanimity.** Every method but one pointing the same way is strong evidence; say so and
   name the dissenter.
6. **Explain, do not average, systematic disagreement.** Sector vs market regression disagreement =
   the sector prices a driver differently from the market. Pricing vs DCF disagreement = either the
   peer group is mispriced or your DCF inputs differ from the market's implied ones. Reverse-engineer
   the market price into implied growth and margin and ask whether that scenario is **probable**, not
   merely possible — there is always a scenario that justifies any price.
7. **Convert the gap into an expected return** so the thesis is comparable to other opportunities:
   `E[P₁] = Value × (1 + cost of equity) − E[Dividend₁]`;
   `E[return] = (E[P₁] + Dividend₁ − Price) / Price`.
8. **Name the closing mechanism.** A gap with no catalyst and no long horizon is an opinion, not a
   trade. Catalysts: new management, a blockbuster product, an acquisition bid, an activist, an index
   event, a break-up, an earnings report.
9. **Size the margin of safety** to the uncertainty about the gap — largest for young, distressed and
   emerging-market companies, which is exactly where it is most often skipped.
10. Issue the call — buy / sell / hold — naming the estimate it rests on and the gap to price.

**Decision rules with thresholds.**
- SELL when the preferred estimate sits below the market price; BUY when the preferred estimate — and
  preferably nearly every method — sits above it.
- Acknowledge narrow-margin calls explicitly. A verdict resting on a 3% gap must say so.
- Never report a relative verdict as absolute. Attach the benchmark to every line.
- Cross-check with the excess-return test: a firm with ROC below WACC cannot justify growth-driven
  value, and its low multiple is deserved
  (`concepts/deliverables-worked-examples/return-spread-and-eva-analysis.md`).
- Where a probability overlay applies (failure, distress, regime change, equity wipeout, management
  change), apply it as a probability weight on value, in **one** place only.

**Outputs.** `verdict = {estimate_table[], discarded[], weighting_rationale, preferred_estimate,
gap_pct, expected_return, catalyst, margin_of_safety, recommendation, unresolved_risks[]}` plus a
written `RELATIVE.md` carrying the estimate table and the reconciliation narrative.

**Draws on:** `concepts/deliverables-worked-examples/valuation-triangulation-and-recommendation.md`,
`concepts/dark-side-difficult/value-versus-price.md`,
`concepts/narrative-numbers/value-vs-price-gap.md`,
`concepts/relative-valuation/pricing-vs-value.md`,
`concepts/dark-side-difficult/scenario-analysis-and-simulation.md`,
`concepts/deliverables-worked-examples/equity-valuation-project-blueprint.md`.

---

## S16 — Validation gates and red team

Run after every stage. Each rule is a predicate; a failure returns a finding with a `target_stage`.

### Definitional consistency (targets S2)
1. Numerator and denominator belong to the same claimholders.
2. One timing variant across the entire sample.
3. One share-count convention across the entire sample.
4. EV nets cash **iff** the denominator excludes interest income.
5. Minority interests removed from EV where the denominator is consolidated.
6. Every accounting cleanup (leases, R&D, one-time items, normalization) applied identically to the
   subject and to every comparable — or the compromise recorded.

### Statistical validity (targets S3, S6)
7. Medians, not means, for any skewed multiple. Mean/median > 3 → medians only.
8. Drop-out count and reason recorded; > 50% drop-out flags `sample_bias = high`.
9. Variable count within the sample-size ceiling (≤25 firms → 1 variable; 15–30 → 2–3).
10. t-statistic ladder applied and insignificant variables dropped and re-run.
11. R² recorded with every predicted multiple; < 0.15 cannot carry a verdict.
12. Negative intercepts checked for negative predicted multiples; through-origin fix recorded if used.
13. Correlation matrix inspected; wrong-sign coefficients labelled as multicollinearity artefacts.
14. Coefficient **units** (decimals vs absolute percent) and **vintage** (`as_of`) recorded and
    validated against a known worked case.
15. Region assignment justified by operating exposure, not by listing venue.

### Fundamental consistency (targets S4, S10B)
16. `g = (1 − payout) × ROE` and `g = RIR × ROIC` hold for every set of fundamentals fed into an
    intrinsic multiple.
17. Terminal growth ≤ the riskfree rate in the valuation currency.
18. Terminal ROC = cost of capital unless a durable advantage is argued.
19. Divisions with ROC ≤ WACC carry zero growth years.
20. Excess-return direction checks: PBV > 1 ⟺ ROE > ke; EV/IC > 1 ⟺ ROC > WACC.
21. A low multiple is checked against its companion variable before being called cheap — reinvestment
    for EV/EBITDA, margin for EV/Sales, ROE for PBV, growth **and** risk for PE, risk and growth
    quality for PEG.

### Double-count register (targets S8, S10, S14, S15)
22. Options: value subtracted **or** diluted shares — never both.
23. Cash: in the flows **or** in the bridge — never both.
24. Cross holdings: valued separately **or** inside the operating numbers — never both.
25. Brand: in the margins **or** as an added asset — never both.
26. Country risk: in the discount rate/premium **or** as a value discount — never both.
27. Failure/distress: as a probability weight **or** in the discount rate — never both, and never in
    the cash flows as well.
28. Complexity/opacity: one route only.
29. Governance: modelled as low returns **or** as a flat discount — never both.
30. Dilution in a young-company DCF: negative early FCFF already contains it; no separate haircut.
31. Discount stacking (illiquidity + minority + key person) requires an explicit reason per layer.
32. Buyer diversification expressed once — in the beta, not also in a discount.

### Frame and disclosure (targets S9, S15)
33. Every verdict carries its benchmark.
34. Implausible estimates discarded with a reason, not averaged.
35. Peer-average and regression estimates reported separately, never merged.
36. Precedent-transaction multiples flagged: a sample of past acquisitions inherits that sample's
    overpayment bias, so matching it replicates the mistake
    (`concepts/acquisitions-control-enhancement/transaction-and-exit-multiples.md`).
37. Exit multiples in a terminal value flagged: they smuggle today's market pricing into an
    "intrinsic" model and assume stationarity. If used, back out the implied growth and ROC and check
    them against a stable-growth firm.
38. EPS accretion is never reported as a deal test: an all-stock deal is accretive whenever
    `PE_acquirer > PE_target`, which is arithmetic, not evidence.
39. Comparable sets assembled **after** a target price was set are flagged as verdict-first
    reasoning.
40. Bubble disclosure: for any sector-relative verdict, state what would have to be true for the
    whole sector to be correctly priced.

### Artifact schema (contract)

```
relative-result.json
{
  "as_of": "YYYY-MM-DD",
  "route": {...},                       // S0
  "constraints": [...],                 // S1
  "multiple_spec": {...},               // S2
  "distribution": {...},                // S3
  "companion_variable": "...",          // S4
  "intrinsic_multiple": 0.0,
  "peer_set": [...], "sample_diagnostics": {...},   // S5
  "controls": [ {multiple, method, benchmark, predicted, fit:{r2,t_stats,n,units,as_of},
                 actual, over_under_pct, implied_price} ],   // S6/S8
  "overrides_applied": [...],           // S7
  "pricing_verdict": {...},             // S9
  "sotp": {...},                        // S10
  "liquidation_value": {...},           // S11
  "fair_value": {...},                  // S12
  "market_pricing": {...},              // S13
  "stake_adjustments": {...},           // S14
  "verdict": {...},                     // S15
  "findings": [ {id, rule, severity, target_stage, claim, evidence, suggested_fix} ]  // S16
}
```

**Draws on:** `concepts/relative-valuation/four-step-multiple-framework.md`,
`concepts/relative-valuation/pricing-vs-value.md`,
`concepts/acquisitions-control-enhancement/transaction-and-exit-multiples.md`,
`concepts/acquisitions-control-enhancement/control-premium-rules-of-thumb.md`,
`concepts/narrative-numbers/valuation-misconceptions.md`,
`concepts/dcf-model-choice-loose-ends/equity-value-bridge.md`.

---

## Appendix A — The seven-move standard pass (route R, no overrides)

For orchestration shorthand. Each move is one stage.

1. Define the multiple (S2).
2. Locate it in the current distribution (S3).
3. Derive its companion variable (S4).
4. Choose comparables and a control technique (S5, S6).
5. Compute the predicted multiple (S6) and convert it to a price (S8).
6. Compare with the traded multiple (S9).
7. State the verdict as **relative**, with its benchmark, and reconcile against intrinsic value (S15).

## Appendix B — Multiple-selection quick table

| If the firm is… | Lead multiple | Companion variable | Why |
|---|---|---|---|
| profitable, stable, comparable-rich | PE or EV/EBITDA | growth / reinvestment need | direct and widely quoted |
| capital-intensive with a measurable ROIC | **EV/Invested Capital** | ROIC | highest R² of any family in every region (50–63%) |
| a bank or insurer | **PBV** | ROE | enterprise multiples are meaningless; ROE fit is the tightest available |
| loss-making but with real revenue | EV/Sales | after-tax operating margin | revenue is always positive |
| loss-making with collapsed sector margins | survival-proxy regression, or a market-implied metric | cash/revenue, revenue growth, users | current fundamentals are uninformative |
| cyclical at an extreme | EV/EBITDA or PE **on normalized earnings** | normalized margin / ROC | the trough year is not the business |
| intangible-heavy | any, but **after** capitalizing R&D | restated ROC / margin | unadjusted earnings and capital are both wrong |
| multi-business | **one multiple per division**, chosen by sector R² | per-division ROC / margin | a single company-wide multiple understates or overstates every part |
| a whole market | PE against rates, real growth and country risk; Shiller PE vs T.Bond PE | interest rate, real growth, risk | the same fundamentals drive a market's PE as a firm's |

## Appendix C — Escalation ladder

```
direct comparison (S6A)
   └─ one dimension differs → story telling + median test (S6B)
        └─ median test gives a mixed pattern, or a modified multiple leaks (S6C)
             └─ several dimensions differ → sector regression (S6D)
                  └─ peer set too small / R² collapsed / whole sector suspect
                       └─ market-wide regression (S6E)  ── non-US ──> regional regression (S6F)
                            └─ conventional fundamentals uninformative (R² ≈ 0)
                                 └─ survival proxies / forward multiple with full haircut /
                                    market-implied metric (S7A)
                                      └─ no comparables at all, assets separable
                                           └─ asset-based routes (S10 / S11 / S12)
```
