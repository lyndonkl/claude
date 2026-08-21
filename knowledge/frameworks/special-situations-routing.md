# Special-situations routing: company classification → analytical treatment

**What this is.** The decision tree that converts what is knowable about a company into a *route*: a primary valuation engine, a set of overlays, a constraint set of things that must not be attempted, and an ordered pipeline. It is the operational specification behind `classification.json` (see `architecture/SPEC.md` §5) and behind the `company-classification-routing` method skill. Gate `G2_classified` passes only when this document's Stage S7 output validates.

**Why routing comes first.** Running standard machinery on a bank, a distressed firm, or a pre-revenue company produces confident nonsense — the most expensive failure mode in this domain. Every branch below rests on one taxonomy, `concepts/dark-side-difficult/difficult-company-taxonomy.md`. It says every valuation answers four questions: existing-asset cash flows, value added by growth, risk, and when maturity arrives with what can end the story early. A company is "difficult" exactly when one or more of those answers is missing, unstable, or mis-measured by accounting. Diagnose *which* question breaks and the repair names itself.

**Consumers.** `company-diagnostician` (writes the route), `valuation-orchestrator` (enforces gates and dispatch), `special-situations-analyst` (executes non-standard branches), `financial-statement-analyst`, `cost-of-capital-analyst`, `relative-valuation-analyst`, `valuation-critic` (validates against Stage S11).

**Reading conventions.** Stage = pipeline step, always executed, in order. Branch = a routing outcome that may or may not fire. `MUST` / `MUST NOT` are hard constraints enforced downstream. Thresholds in `code` are literal decision rules. Concept citations are `concepts/<area>/<slug>.md` and carry the detail this document deliberately omits.

---

## Part I — The pipeline (Stages S0–S11)

### S0 · Evidence intake and route feasibility

**Input:** `mandate.json` (mode, company, currency, valuation date), `01-data/raw-financials.json`, `01-data/market-data.json`, `01-data/gaps.json`.

**Work:** Establish which of the three information sources a normal valuation leans on actually exist: (1) current financial statements, (2) the firm's own financial history, (3) industry / comparable-firm data. Record each as `present | thin | absent`.

**Decision rules:**
- `sources_absent >= 2` → the company is at the point of maximum temptation toward the dark side. Force an explicit mature end-state (target margin, terminal ROC, stable growth) and work backwards. Set `route.requires_end_state = true`.
- No cash flows exist at all and none ever will (a currency, a collectible, a pure commodity holding) → the asset can be **priced only, never valued**. Emit `constraint: no-intrinsic-valuation` and route to Part III pricing only. `concepts/narrative-numbers/value-vs-price-gap.md`.
- Fewer than 3 years of statements, or statements that mix personal and business expense → private-company cleanup is mandatory before any forecast. See B13.

**Output:** `evidence_profile` block; `blocked` status if the minimum viable input set is missing and the user has not supplied substitutes.

**Draws on:** `concepts/dark-side-difficult/difficult-company-taxonomy.md`, `concepts/narrative-numbers/landscape-survey.md`, `concepts/narrative-numbers/value-vs-price-gap.md`, `concepts/deliverables-worked-examples/project-company-selection.md`.

---

### S1 · Signal extraction (deterministic classifiers)

Every signal below is computed from data, not asserted. Each carries a `confidence` and the evidence that set it. These are the only inputs the gates in S2–S6 may consult.

| Signal | Computation | Values / thresholds |
|---|---|---|
| `sector_type` | Business description + segment note + statement shape (`concepts/accounting-statements/sector-differences-in-financial-statements.md`) | `financial-service` \| `commodity` \| `cyclical-industrial` \| `real-estate/REIT` \| `intangible-heavy` \| `ordinary` |
| `life_cycle_stage` | Revenue level, revenue growth, margin sign and stability, reinvestment intensity, age | `start-up` \| `young-growth` \| `high-growth` \| `mature-growth` \| `mature-stable` \| `decline` |
| `earnings_status` | Sign and representativeness of TTM EBIT and net income, after S3 cleanup | `profitable` \| `marginal` \| `negative-transient` \| `negative-structural` \| `cyclical-trough` \| `cyclical-peak` |
| `revenue_status` | TTM revenue vs. 3-yr and 5-yr | `pre-revenue` \| `growing` \| `flat` \| `declining` |
| `g_firm vs g_econ` | Expected near-term growth vs. nominal economy growth (proxy: riskfree rate in valuation currency) | `≤ g_econ` → 1-stage; `≤ g_econ + 10%` → 2-stage; `> g_econ + 10%` → 3/n-stage |
| `leverage_state` | Market `D/(D+E)`; distance from sector median and from stated target; trajectory | `stable` \| `changing` \| `extreme` (`> 50%`) |
| `payout_coverage` | `Σ5yr (dividends + buybacks) / Σ5yr FCFE` | `< 80%` → FCFE; `80–110%` → dividends; `> 110%` → FCFE |
| `distress_markers` | Coverage ratio, rating, bond prices vs. par, negative book equity, covenant breach, going-concern note, sector peers distressed | count + evidence list |
| `intangible_intensity` | `R&D / revenues`, `R&D / (R&D + net capex)`, brand-advertising share, recruiting/training spend | `low` \| `moderate` \| `high` |
| `geography_exposure` | Revenue (and production) share by country/region; NOT country of incorporation | weight vector |
| `ownership` | Public / private / subsidiary / division; free float; insider and institutional shares; dual-class; cross-holdings | structure record |
| `stake_size` | Fraction of equity being valued | `> 50%` controlling, `≤ 50%` minority |
| `buyer_diversification` | Who the marginal investor is for *this* transaction | `diversified` \| `partially` (ρ known) \| `undiversified` |
| `holdings_share` | Value of stakes in other firms / total estimated value | flag when `> ~33%` |
| `business_count` | Reportable segments with distinct economics and separable cash flows | `1` \| `>1` |
| `option_candidates` | Patents, undeveloped reserves, licences, exclusive expansion rights, contractual exit rights, excess debt capacity | list, each with an exclusivity note |
| `macro_driver` | Existence and strength of a commodity/cycle driver: regress revenues on the price, report R² | driver + R² |
| `transaction_motive` | From the mandate: valuation / acquisition / restructuring / IPO / project / corporate-finance | one of |

**Draws on:** `concepts/dark-side-difficult/difficult-company-taxonomy.md`, `concepts/narrative-numbers/life-cycle-uncertainty.md`, `concepts/accounting-statements/life-cycle-patterns-in-financial-statements.md`, `concepts/dcf-model-choice-loose-ends/dividends-versus-fcfe.md`, `concepts/dcf-model-choice-loose-ends/growth-pattern-and-stage-count.md`, `concepts/cost-of-equity/operation-weighted-erp.md`.

---

### S2 · Sector gate (exclusive, evaluated first, highest precedence)

The sector gate outranks every other gate because it decides whether firm-level cash flow and firm-level leverage are even defined.

```
if sector_type == financial-service        -> B5   (terminates the FCFF path entirely)
elif sector_type == real-estate/REIT       -> B5b  (payout mandated; see note)
elif macro_driver exists and R^2 is high   -> B6   (commodity)
elif sector_type == cyclical-industrial
     and earnings_status in {trough, peak} -> B7   (cyclical normalization)
else                                       -> continue to S3
```

`REIT (B5b)`: mandated payout and tax status make optimal-debt-ratio and retention-based growth analysis meaningless; value on dividends/FFO and exclude from any corporate-finance financing recommendation (`concepts/deliverables-worked-examples/project-company-selection.md`). All other routing continues normally.

Commodity vs. cyclical is decided by whether a usable *price driver* exists. A high-R² revenue-on-price regression → B6. No usable price series → B7.

---

### S3 · Statement-repair gate (always executed; sets what "earnings" means downstream)

Nothing downstream is stable until the base year is honest. Order is fixed because each step feeds the next.

1. **Update** to trailing twelve months. `concepts/dcf-cashflows-growth/reported-to-actual-earnings.md`, `concepts/narrative-numbers/landscape-survey.md`.
2. **Capitalize operating leases** → lease debt, restated EBIT, restated invested capital. `concepts/cost-of-debt-capital/operating-leases-as-debt.md`.
3. **Capitalize R&D / recruiting / brand-building advertising** if `intangible_intensity ∈ {moderate, high}` → research asset, amortization, restated EBIT and capital. **B8**. `concepts/dark-side-difficult/capitalizing-rd.md`.
4. **Strip one-time items and personal expenses**; charge a market salary for uncompensated owner labour if private. `concepts/asset-based-private/private-company-statement-cleanup.md`.
5. **Normalize** only if S4 routes to B7 (see the mutual exclusion in S8-R3).
6. **Resolve the circularity**: normalized/restated EBIT → interest coverage → synthetic rating → cost of debt → lease discount rate → restated EBIT. Iterate to a fixed point. `concepts/cost-of-debt-capital/wacc-calculator-workflow.md`, `concepts/dark-side-difficult/normalized-earnings.md`.

**MUST:** every downstream consumer of EBIT, invested capital, ROIC, coverage and reinvestment uses the *same* restated basis. Mixing bases is the single most common silent error.

---

### S4 · Ownership and transaction gate (exclusive)

```
if ownership == private and transaction_motive != ipo   -> B13 (+ sub-scenario)
elif transaction_motive == ipo                          -> B14
elif ownership == division/subsidiary being separated   -> B10 (sum-of-the-parts, divisional)
elif transaction_motive == acquisition                  -> B15 (runs the full four-number chain)
elif transaction_motive == restructuring
     or activist/control question                       -> B2
else                                                    -> continue to S5
```

This gate sets the **discount-rate identity** (whose risk is priced) and the **discount stack** (illiquidity, minority, key-person). It does not choose the cash-flow engine; S5 does.

---

### S5 · Life-cycle and earnings gate (exclusive; selects the primary cash-flow engine)

```
if revenue_status == pre-revenue
   or earnings_status == negative-structural
   or (life_cycle_stage in {start-up, young-growth} and earnings_status != profitable)
                                             -> B1  revenue-driven, work-backwards
elif earnings_status in {negative-transient, cyclical-trough, cyclical-peak}
                                             -> B7  normalize, then standard engine
elif revenue_status == declining
     and life_cycle_stage == decline         -> B3  negative growth, negative reinvestment
elif life_cycle_stage in {mature-growth, mature-stable}
     and policies look "consistent, stable and bad"
                                             -> B2  status quo vs. optimal, weighted
else                                         -> standard path
```

**Standard path selection** (no special branch fired):
- Equity vs. firm: `leverage_state == stable` → equity route; `changing` or leverage data incomplete → firm route (FCFF/WACC). `concepts/dcf-model-choice-loose-ends/equity-versus-firm-valuation.md`.
- If equity route: apply the `80% / 110%` payout screen to choose dividends vs. FCFE. `concepts/dcf-model-choice-loose-ends/dividends-versus-fcfe.md`.
- Stage count from the `g_econ + 10%` screen. `concepts/dcf-model-choice-loose-ends/growth-pattern-and-stage-count.md`.
- Model variant matrix and the mechanics: `concepts/dcf-model-choice-loose-ends/dcf-model-choice-framework.md`, `concepts/dcf-model-choice-loose-ends/multistage-model-mechanics.md`.

---

### S6 · Survival and truncation gate (outer wrapper, applied *after* the engine produces a going-concern value)

A DCF values a going concern. It implicitly assumes the firm lives long enough to reach stable growth. If it may not, the DCF overstates value — and the repair is **never** a higher discount rate.

```
survival_in_doubt = any of:
   life_cycle_stage in {start-up, young-growth}   -> B1 requires it by default
   revenue_status == declining and leverage high  -> B3 hands off to B4
   coverage < 1 or rating <= CCC                  -> B4
   traded bonds well below par                    -> B4, invert the price for pi
   bank near regulatory capital minimum           -> B5, wipeout probability
   expropriation / regime-change exposure         -> B9 truncation
   market D/(D+E) > 50% and earnings negative     -> B4 + equity-as-option cross-check
```

If fired → **B4** (and/or the truncation sub-branch of B9). Probability sourcing hierarchy, most informative last: sector survival tables → rating-implied cumulative default rate → statistical model → **invert a traded bond price**. `concepts/dark-side-difficult/distress-and-failure-adjusted-value.md`, `concepts/dark-side-difficult/bond-implied-distress-probability.md`.

---

### S7 · Overlay assignment and constraint compilation

Overlays are **non-exclusive** and compose. Assign every overlay whose trigger fires, then compile the union of the constraint sets from every fired branch. Conflicts are resolved by S8.

Overlay branches: **B8** intangible-heavy, **B9** emerging-market/country-risk (with truncation sub-branch), **B10** multi-business, **B11** cross-holdings/group, **B12** real options, **B16** macro-shock revaluation.

**Output — the route record** (extends `classification.json`):

```json
{
  "primary_path": "standard-fcff|standard-fcfe|dividend-discount|excess-return|
                   revenue-driven|normalized|declining|distress-adjusted|
                   asset-based|option-based|sum-of-the-parts",
  "engine_branch": "B1..B16",
  "overlays": ["intangible-heavy","emerging-market","multi-business",
               "cross-holdings","has-real-options","macro-shock"],
  "transaction_overlay": "acquisition|restructuring|ipo|private-sale|none",
  "discount_stack": ["illiquidity","minority","key-person"],
  "constraints": [{"rule":"...", "reason":"...", "source_branch":"B5"}],
  "pipeline": ["clean","normalize|revenue-drive","rate-stack","engine",
               "outer-adjustments","bridge","simulate","price-compare"],
  "confidence": "high|medium|low",
  "unresolved": ["what evidence would change the routing"]
}
```

---

### S8 · Combination rules (how multiple branches compose)

Real companies sit in several buckets at once. Boeing in March 2020 was mature + cyclical + distressed. Tata Steel is emerging-market + cyclical + cross-holding-heavy. A distressed emerging-market bank needs three sets of repairs, not one. These rules make composition deterministic.

**R1 — Precedence for the engine.** Exactly one engine may run. Order of precedence, highest first:

```
B5 financial-service  >  B13/B14 private/IPO (rate & discount identity)
                      >  B4 distress-with-equity-wipeout
                      >  B1 revenue-driven (negative/structural)
                      >  B7 normalized (transient/cyclical)
                      >  B3 declining
                      >  B2 status-quo-vs-optimal
                      >  standard
```
B10 sum-of-the-parts is a *decomposition*, not an engine: it runs the precedence list **once per division** and then aggregates.

**R2 — Overlays never replace the engine.** B8, B9, B11, B12, B16 modify inputs, the discount rate, or the bridge. They never change which cash flow is discounted.

**R3 — Mutually exclusive pairs (violation is a hard error).**

| Pair | Rule |
|---|---|
| B7 normalize ↔ B1 revenue-driven | Normalization is legitimate only when the trouble is *temporary*. Structural, life-cycle, or leverage-driven losses MUST route to B1 or B4. Never both. |
| B7 normalize ↔ separate recovery assumption | Normalized earnings *are* the recovery. Assuming recovery on top double counts. |
| B5 FCFF ↔ anything | A financial service firm never gets an FCFF/WACC valuation. |
| Total beta (B13-I) ↔ diversified buyer (B13-II/III, B14) | One buyer identity per valuation. |
| Illiquidity discount ↔ public buyer / IPO | The buyer's investors have a market. |
| B12 option value ↔ the same upside inside DCF growth | Route each claim to exactly one device. |
| Higher discount rate for failure ↔ B4 probability weighting | Pick one channel. The probability weight is the correct one. |

**R4 — Ordering when several branches fire.** Fixed pipeline:

```
1. Clean accounts        (S3: leases, R&D/B8, one-times, owner salary)
2. Fix the base earnings (B7 normalize  OR  B1 abandon earnings and drive from revenue)
3. Build the rate stack  (bottom-up beta -> total beta if B13-I
                          -> exposure-weighted ERP/lambda if B9
                          -> synthetic rating incl. country spread if B9
                          -> divisional rates if B10)
4. Run the engine        (per R1; per division if B10)
5. Outer adjustments     (B4 failure weighting, B9 truncation weighting,
                          B2 P(change) weighting) -- multiplicative, applied once each
6. Equity bridge         (debt incl. leases, minorities at market, cash,
                          B11 cross-holdings, employee options)
7. Discount stack        (B13: illiquidity, then minority; key-person already in EBIT)
8. Uncertainty           (S10: scenario grid, then simulation)
9. Price comparison      (S10: gap, catalyst, expected return)
```

**R5 — Composition arithmetic for outer adjustments.** Probability-weighted branches compose multiplicatively on the *going-concern* value, and each risk may appear exactly once:
`V = V_going_concern × Π_i (1 − p_i × loss_fraction_i) + Σ_i p_i × proceeds_i` — but in practice never stack more than two (e.g. failure *and* regime change) without arguing that they are genuinely distinct events. A country risk premium in the cost of equity **plus** a nationalization scenario **plus** a governance discount is three charges for overlapping risks.

**R6 — Governance and control are cash-flow facts, not discount-rate facts.** Weak governance is modelled as low returns on capital and a low `P(change)`, never as a discount-rate bump or a flat value haircut. Same for emerging-market risk beyond the exposure-weighted premium.

**R7 — Common multi-branch resolutions.**

| Company shape | Route |
|---|---|
| Distressed emerging-market bank | Engine **B5** (FCFE-to-regulatory-capital, not dividends — payout is not capacity in a crisis). Rate stack from **B9** (local-currency riskfree built from the inflation differential; exposure-weighted ERP). Outer adjustment: probability of **equity wipeout**, not liquidation. Constraints: `no-fcff-valuation`, `no-optimal-debt-ratio`. |
| Cyclical + distressed (mature industrial in a shock) | **B7** normalize the base, then **B4** failure weighting on top. Do not normalize *and* assume the cycle recovers in the forecast. Cross-check with **B12** equity-as-call if `D/(D+E) > 50%`. |
| Young + intangible-heavy + private | **S3** capitalize R&D first (it changes invested capital and the sales-to-capital ratio), then **B1** engine, then **B13** rate identity and discount stack, then **B4** failure probability from sector survival. |
| Commodity + emerging market + cross-holdings | **B6** engine at today's price, **B9** rate stack, **B11** bridge. Report the value as "worth X at today's commodity price" and state the macro view separately. |
| Multi-business with one financial division | **B10** decomposition; the financial division is valued by **B5** on equity and added as an equity-value block; every other division on **EV**. Never blend a bank into a consolidated FCFF. |
| Mature + poorly governed + emerging market | **B2** status-quo vs. optimal with **both** return levers (new investments *and* existing assets), **B9** rate stack, and `P(change)` from ownership/voting/activist evidence. Do not add a governance discount. |
| Declining + heavy cross-holdings | **B3** engine on the operating business, **B11** for the stakes; note that holdings often exist to preserve control and will not be sold. |

**R8 — Mode interaction.** `mode` from the mandate selects what runs *after* the engine, not the engine itself. `acquisition` → B15's four-number chain wraps the engine. `restructuring` → B2. `corporate-finance` → the capital-structure and payout stages, which are **suppressed entirely** for B5 and B5b.

---

### S9 · Pricing-route selection (relative valuation per branch)

Every branch also gets a *pricing* route, because a relative check is required in every mode. The rule is not "which multiple do I like" but "which multiple survives this company's defects."

| Branch condition | Pricing route | Forbidden |
|---|---|---|
| Negative or trough earnings | Survival/growth-proxy regression; forward multiple with the **full haircut sequence**; or let the market pick the metric (highest correlation of value with an operating metric) | PE, PEG, EV/EBIT, EV/EBITDA |
| Financial service | Equity multiples only: PBV against ROE, PE | EV/EBITDA, EV/Sales, EV/IC, any enterprise multiple |
| Commodity / cyclical | Multiples on **normalized** earnings; EV/EBITDA with reinvestment control | Current-year PE at a cycle extreme |
| Intangible-heavy | Multiples on **restated** (R&D-capitalized) earnings and capital; EV/Sales with margin control | Raw PBV, raw EV/IC on unrestated capital |
| Multi-business | Price each division off its own sector's regression evaluated at that division's fundamentals; then bridge | One company-wide multiple |
| Emerging market / non-US | Regional regression, not the US one; assign region by operations, not listing | US market regression applied to a non-US firm without an ADR |
| Private | Sector multiples with the same discounts as the DCF path; regression at the firm's own fundamentals | Any multiple that assumes a traded market without a discount |
| Young / high-growth | Forward multiples and market-implied metrics, with survival proxies | Raw PS regressed on current margin |

**Universal pricing rules.** Run define/describe/analyze/apply before trusting any multiple. Use **medians**, never means. Locate the multiple in the *current, local* distribution — a fixed threshold flips meaning across years and regions. Control statistically once more than one fundamental differs. State the verdict as **relative**, never absolute.

**Draws on:** `concepts/relative-valuation/four-step-multiple-framework.md`, `concepts/relative-valuation/multiple-definition-tests.md`, `concepts/relative-valuation/multiple-distribution-statistics.md`, `concepts/relative-valuation/intrinsic-multiple-derivation.md`, `concepts/relative-valuation/comparable-selection-and-controls.md`, `concepts/relative-valuation/sector-regressions.md`, `concepts/relative-valuation/market-wide-regressions.md`, `concepts/relative-valuation/cross-market-multiple-regressions.md`, `concepts/relative-valuation/pricing-young-companies.md`, `concepts/relative-valuation/book-value-multiples.md`, `concepts/relative-valuation/ev-ebitda-multiple.md`, `concepts/relative-valuation/ev-sales-and-brand-value.md`, `concepts/relative-valuation/industry-average-multiples.md`, `concepts/relative-valuation/pricing-vs-value.md`.

---

### S10 · Uncertainty and closing (always executed)

1. **Two-way sensitivity grid** on the two drivers that actually move value for this branch (young: revenue growth × target margin; commodity: price × margin; index: earnings × ERP). Mark the cells that reach the market price. The uncomfortable truth is universal: *some* combination justifies any price. The question is never "is there a scenario?" but "is it **probable**?"
2. **Named scenario grid** when the doubt is about *which story*; **Monte Carlo** when the doubt is about *how much*. Label every row possible / plausible / probable. Specify correlations and get their signs right; independent draws on correlated inputs understate the tails.
3. **Report percentiles and where the market price sits**, not the mean.
4. **Convert the gap into an expected return** and name the catalyst — or state that the thesis relies on patience.
5. **Margin of safety sized to branch uncertainty** — largest exactly where routing was hardest (young, distressed, emerging-market).

**Draws on:** `concepts/dark-side-difficult/scenario-analysis-and-simulation.md`, `concepts/narrative-numbers/narrative-scenario-grids.md`, `concepts/narrative-numbers/monte-carlo-valuation-simulation.md`, `concepts/narrative-numbers/possible-plausible-probable.md`, `concepts/dark-side-difficult/value-versus-price.md`, `concepts/narrative-numbers/value-vs-price-gap.md`.

---

### S11 · Validation (route-aware consistency checks; the critic's checklist)

Every rule is a predicate over produced artifacts. A `high` severity failure reopens the owning stage.

| ID | Rule | Severity |
|---|---|---|
| V1 | **Single-charge rule.** Each risk is priced exactly once. Enumerate: failure risk (probability weight *or* rate, not both), country risk (premium *or* scenario, not both plus a discount), governance (low ROC *or* low P(change), never a haircut), illiquidity, control. | high |
| V2 | **Currency consistency.** Riskfree rate, cash flows, growth and inflation live in one currency. ERP tracks *operating exposure*, not the unit of account. Re-running in a second currency must reproduce the same value at the current exchange rate. | high |
| V3 | **Growth cap.** Terminal `g ≤ riskfree rate` in the valuation currency (holds for negative rates too). Implied year-10 revenue / total market `≤ 100%`. Aggregate implied sector revenue across all competitors `≤ credible market forecast`. | high |
| V4 | **Reinvestment consistency.** Growth is paid for: `g = RIR × ROC` (or `retention × ROE`). Terminal `RIR = g/ROC`. Imputed year-by-year ROC and the forecast's marginal ROIC must be defensible against the sector; a sales-to-capital ratio far above the industry is an explicit claim, not a default. | high |
| V5 | **Terminal excess returns require a named moat.** Default is terminal `ROC = terminal cost of capital`. Any override states the barrier (brand, legal protection, switching costs, cost advantage) and its expected life. | high |
| V6 | **Claimholder consistency.** Firm flows at WACC, equity flows at cost of equity; enterprise numerators with operating denominators, equity numerators with equity denominators. | high |
| V7 | **Double-count register.** Explicitly cleared: option value vs. DCF growth for the same market; dilution from negative early FCFF vs. a diluted share count; brand value vs. brand-driven margins; control value vs. synergy baseline; cash inside operating flows and again in the bridge; consolidated subsidiary earnings and its stake value. | high |
| V8 | **Bridge completeness.** Operating assets → ± lease debt, all interest-bearing debt at market, minority interests **at market not book**, cash (with any trapped-cash or deployment adjustment), cross-holdings, other non-operating assets, employee options **valued as options**, then divide by the **undiluted** share count. | high |
| V9 | **Route conformance.** No artifact violates any compiled constraint. Bank with a WACC, PE on negative earnings, optimal-debt schedule on a bank — all hard fails. | high |
| V10 | **Probability bounds.** Every probability in `[0,1]`; cumulative vs. annual stated correctly (`P_n = 1 − (1−p)^n`); market-implied `P(change) ∈ (0,1)` or the two underlying valuations are wrong. | high |
| V11 | **Normalization coherence.** If earnings were normalized, the coverage ratio, synthetic rating, cost of debt and lease capitalization used the *same* normalized figure, resolved to a fixed point. | medium |
| V12 | **Distribution sanity.** Any multiple used is located in its current, local distribution; medians not means; count of firms dropped from the sample recorded. | medium |
| V13 | **Composition audit.** Report value composition: % from operating assets, % from holdings, % from cash, % from terminal value, % from option value. Flag when holdings exceed ~⅓ of value — the error bars then live in the holdings, not the DCF. | medium |
| V14 | **Unbiasedness.** Across the analyst's record, upward and downward revisions should be roughly balanced; a one-sided record indicates a biased process. | low |

**Draws on:** `concepts/narrative-numbers/narrative-consistency-checks.md`, `concepts/narrative-numbers/big-market-delusion.md`, `concepts/narrative-numbers/valuation-misconceptions.md`, `concepts/narrative-numbers/bermuda-triangle-of-valuation.md`, `concepts/narrative-numbers/runaway-stories.md`, `concepts/dcf-model-choice-loose-ends/equity-value-bridge.md`, `concepts/dcf-cashflows-growth/terminal-value.md`.

---

## Part II — The branches (B1–B16)

Each branch states: **trigger** · **what breaks and why** · **what replaces it** · **extra inputs** · **hard constraints** · **outputs** · **concepts**.

---

### B1 · Young company with negative or trivial earnings

**Trigger.** `revenue_status == pre-revenue` OR (`earnings_status == negative-structural`) OR (`life_cycle_stage ∈ {start-up, young-growth}` AND not profitable). Also fires for any firm whose losses come from the life cycle rather than from a transient shock.

**What breaks and why.**
- *Current earnings* are meaningless — negative or trivially small. Any multiple built on them is undefined.
- *Growth from fundamentals* breaks: `g = RIR × ROC` requires a sustainable return, and ROC is negative.
- *Historical growth* is unusable off a negative or tiny base; percentage growth is dominated by the scaling effect.
- *Regression betas* are noise (Amazon Jan-2000: raw 2.23 / adjusted 1.82, R² 0.17, standard error 0.50).
- *Comparables* often do not exist — the business itself may be young.
- *Going-concern DCF* overstates value because failure is a live outcome.

**What replaces it.** Work **backwards from a mature end-state**:
1. Fix the base year (TTM revenues, adjusted EBIT, NOL balance, cash, debt, shares, options).
2. Choose the end-state **first**: target pre-tax operating margin = the mature sector's margin; terminal growth ≤ riskfree; terminal ROC = terminal cost of capital unless a moat is argued.
3. Set the revenue path backwards to that end-state; fade excess growth. Post-IPO excess growth over the industry decays to roughly zero by years 5–6.
4. Ramp the margin to target by a stated convergence year.
5. Run the **NOL engine**: no tax while losses are absorbed, no refund in loss years, then effective → marginal rate.
6. Charge for growth via the **sales-to-capital** ratio; roll invested capital forward; check imputed ROC each year and the marginal ROIC over the forecast.
7. Bottom-up sector beta fading toward 1.0; cost of capital falling as the firm matures. If desperate, start at the 90th–95th percentile of the cross-sectional cost-of-capital distribution.
8. Equity bridge; employee options valued with the **dilution-adjusted** Black-Scholes; divide by the **undiluted** share count.
9. Apply **B4** failure adjustment outside the DCF.

**Extra inputs.** Mature-sector margin distribution; total addressable market (to test implied share); sector sales-to-capital; sector unlevered beta; NOL carryforward; option pool (count, average strike, average maturity, volatility); sector survival table.

**Hard constraints.**
- `no-earnings-multiple` — PE, PEG, EV/EBIT are undefined.
- `no-standard-growth-model` — growth MUST be built from revenues and a target margin, not from an earnings growth rate.
- `require-failure-probability` — a going-concern DCF alone is not an answer.
- MUST NOT use a regression beta.
- MUST NOT put failure risk in the discount rate.
- MUST NOT hold the cost of capital constant for ten years when the whole story is maturation.
- MUST NOT apply a separate dilution haircut on top of a DCF whose early FCFF is negative — the negative early cash flows *are* the dilution.
- MUST NOT add back stock-based compensation as a non-cash charge.

**Outputs.** `forecast.json` with per-year revenue/margin/tax/reinvestment/WACC; imputed ROC series; marginal ROIC; failure block; option value; value per share.

**Concepts.** `concepts/dark-side-difficult/young-company-valuation.md`, `concepts/dark-side-difficult/sales-to-capital-reinvestment.md`, `concepts/dark-side-difficult/dilution-and-employee-options.md`, `concepts/dcf-cashflows-growth/top-down-revenue-growth.md`, `concepts/dcf-cashflows-growth/tax-rate-and-nols.md`, `concepts/dcf-cashflows-growth/fcff-forecast-engine.md`, `concepts/cost-of-equity/bottom-up-beta.md`, `concepts/narrative-numbers/narrative-to-value-drivers.md`, `concepts/narrative-numbers/uber-narrative-valuation.md`, `concepts/narrative-numbers/tesla-motley-fool-valuation.md`.

---

### B2 · Mature firm in transition — status quo versus optimally run

**Trigger.** Mature life-cycle stage with any of: `ROIC < WACC`; reinvestment far above or below the sector; debt ratio far from the sector optimum; an activist on the register; a control contest; a restructuring mandate; a governance audit that finds insiders control the votes. Also the default engine for `mode == restructuring` and the middle of the **B15** chain.

**What breaks and why.** History is rich but describes policies that are about to be abandoned. A single DCF on current policy values a company that may not exist next year; a single DCF on optimal policy values a company that does not exist *yet*.

**What replaces it.** Value the same company **twice**, then weight.
1. **Status quo**: actual reinvestment rate, actual ROC, actual debt ratio.
2. **Diagnose the three failures**: invests too little/too much; earns below its cost of capital; wrong financing mix.
3. **Operating restructuring**: raise the reinvestment rate and the return on **new** capital → new `g = RIR × ROC`. Then the second, usually larger lever: raise the return on **existing** assets, entered as an efficiency-growth term `[1 + (ROC_new − ROC_old)/ROC_old]^(1/n) − 1`, spread over `n` years and **not** applied in perpetuity.
4. **Financial restructuring**: run the cost-of-capital schedule from 0% to 90% debt in 10-point steps, relevering beta and resetting the synthetic rating at each step; cap the tax benefit where interest exceeds EBIT; take the minimum-WACC ratio.
5. **Value of control** = optimal − status quo. **Expected value** = status quo × (1 − p) + optimal × p.
6. `P(change)` from ownership and voting structure, takeover defenses, board composition, activist presence, access to challenge funding, firm size, and the empirical turnover determinants (underperformance, small outsider-dominated board, high institutional / low insider holdings, competitive industry).
7. Read the market's own odds: `P_implied = (Price − StatusQuo)/(Optimal − StatusQuo)`; `P ≥ 1` or `P ≤ 0` means an input is wrong, not a discovery.
8. Allocate control value across share classes (voting premium) and across stakes (majority off optimal, minority off status quo).

**Extra inputs.** Sector ROIC/margin/reinvestment/debt-ratio benchmarks; the acquirer's own metrics if this is B15; rating/spread table; ownership register and voting structure; takeover-defense inventory; implementation timeline.

**Hard constraints.**
- MUST NOT quote the optimally-run value as *the* value without a probability.
- MUST NOT use a fixed control-premium percentage. A perfectly run firm has a control premium of **zero**.
- MUST NOT change the discount rate between the two scenarios except through the deliberate capital-structure change.
- MUST NOT assume margin improvement without evidence of top-management commitment and explicit targets.
- MUST NOT raise the reinvestment rate while `ROC < WACC` — that accelerates value destruction. For sub-WACC firms the value-creating move is usually to **shrink** and return capital.
- MUST discount the value gain for implementation delay.

**Outputs.** Two complete valuations, the value-of-control delta, `P(change)` with evidence, the expected value, the WACC schedule, and (if a stake) the voting/minority allocation.

**Concepts.** `concepts/dark-side-difficult/value-of-control-and-restructuring.md`, `concepts/dark-side-difficult/return-improvement-and-governance-drag.md`, `concepts/acquisitions-control-enhancement/status-quo-valuation.md`, `concepts/acquisitions-control-enhancement/restructured-value-and-value-of-control.md`, `concepts/acquisitions-control-enhancement/expected-value-of-control.md`, `concepts/acquisitions-control-enhancement/implied-probability-of-management-change.md`, `concepts/acquisitions-control-enhancement/voting-premium-and-minority-discount.md`, `concepts/acquisitions-control-enhancement/paths-to-value-creation.md`, `concepts/acquisitions-control-enhancement/growth-quality-and-excess-returns.md`, `concepts/capital-structure/cost-of-capital-approach.md`, `concepts/capital-structure/optimal-debt-ratio-by-firm-type.md`, `concepts/governance-objective/ownership-and-control-structure-analysis.md`.

---

### B3 · Declining firm

**Trigger.** `revenue_status == declining` over a multi-year window AND `life_cycle_stage == decline`; typically thin margins and a material share of capital earning below the cost of capital.

**What breaks and why.** The long history describes a shrinking business, so extrapolation is worse than useless. Standard templates assume positive growth and positive reinvestment; both signs are wrong here. Anchoring the margin target on the firm's own better past overstates the recovery.

**What replaces it.**
- **Negative revenue growth path** with an explicit moderation schedule toward zero or slightly positive.
- **Margin recovery to the sector median**, not to the firm's own historical best.
- **Negative reinvestment**: `Reinvestment = ΔRevenue / (Sales/Capital)` goes negative automatically as revenues fall; net capex can be below depreciation as stores, plants and real estate are sold. FCFF can exceed EBIT(1−t) — that is arithmetic, not an error.
- Tax rate rising toward marginal as shields run out; cost of capital falling as leverage and risk normalize.
- Stable-phase `RIR = g/ROC` is **negative** when `g < 0`.
- Hand off to **B4** whenever survival is genuinely in doubt.
- Test management behaviour: if revenues and operating income are being grown by investing below the cost of capital, the model must show value falling while earnings rise.

**Extra inputs.** Sector median margin; asset-disposal schedule and expected proceeds; pension underfunding, litigation claims, liquidation preferences; bond prices or rating for the failure probability.

**Hard constraints.**
- MUST NOT force positive growth because the template assumes it.
- MUST NOT floor reinvestment at zero beyond year 1 — that discards the real cash released.
- MUST NOT value a levered declining firm as a pure going concern (`require-failure-probability`).
- MUST NOT anchor the terminal margin on the firm's own peak.
- MUST include equity-side claims that decline exposes: pension shortfalls, litigation, preferences.

**Outputs.** Negative-growth forecast, released-capital schedule, distress-weighted operating assets, bridge with decline-specific claims.

**Concepts.** `concepts/dark-side-difficult/declining-firm-valuation.md`, `concepts/dark-side-difficult/sales-to-capital-reinvestment.md`, `concepts/dark-side-difficult/distress-and-failure-adjusted-value.md`, `concepts/acquisitions-control-enhancement/growth-quality-and-excess-returns.md`, `concepts/dcf-model-choice-loose-ends/debt-and-other-claims-in-the-bridge.md`.

---

### B4 · Distress and failure adjustment

**Trigger.** Any distress marker from S6. Applies as an **outer wrapper** to whatever engine ran.

**What breaks and why.** The DCF assumes survival to stable growth. If the firm may die first and its assets would fetch less than the PV of expected cash flows, the DCF overstates value. Raising the discount rate does not fix it — failure is not a marginal, diversifiable risk, and doing both double counts.

**What replaces it.**
- `Value = Going-concern × (1 − p) + Distress proceeds × p`, at firm level or equity level.
- Partial-wipeout form when the firm survives but equity is diluted or expropriated: `V × (1 − p × loss_fraction)`.
- **Proceeds basis**: percent of book (equity + debt) or percent of going-concern value; default 50%, cut it further when the whole sector is selling the same assets at once.
- **Equity is a residual**: if proceeds < face value of debt, distress-branch equity is **zero**.
- **Probability sourcing**, in ascending information content: sector survival table → rating-implied cumulative default rate → statistical model → **inverted traded bond price** (price the promised coupons and principal, weight by `(1−π)^t`, discount at the **riskfree** rate, solve for π; convert to the cumulative probability over the forecast horizon).
- **Cross-check with the option lens** when `market D/(D+E) > 50%` and earnings are negative: equity is a call on firm value struck at the face value of debt, with life = face-value-weighted **duration** of the debt. It explains why deeply insolvent equity trades above zero (pure time value) and gives a second equity estimate. See B12.

**Extra inputs.** Traded bond terms and prices; rating and its cumulative default table; sector survival statistics; liquidation comparables; debt maturity schedule with durations; firm-value variance (from stock and bond volatilities and their correlation — **not** equity volatility alone).

**Hard constraints.**
- MUST NOT raise the discount rate for failure risk and also probability-weight.
- MUST NOT shrink the expected cash flows for failure and also probability-weight.
- MUST NOT report the annual probability where the model needs the cumulative one.
- MUST NOT assume a generous recovery in an economy-wide downturn.
- MUST NOT assume equity retains value when expected proceeds fall short of debt face value.
- MUST distinguish *firm failure* from *equity wipeout* — a bailout can save the firm and destroy the equity.
- The option cross-check is an **alternative** equity estimate, never additive to the DCF equity value.

**Outputs.** `p_failure` with source and horizon, proceeds basis and amount, blended value, both branch values reported alongside.

**Concepts.** `concepts/dark-side-difficult/distress-and-failure-adjusted-value.md`, `concepts/dark-side-difficult/bond-implied-distress-probability.md`, `concepts/real-options/equity-as-call-option.md`, `concepts/real-options/distressed-equity-time-value.md`, `concepts/real-options/equity-option-inputs-troubled-firms.md`, `concepts/deliverables-worked-examples/equity-as-call-option-valuation.md`.

---

### B5 · Financial service firms (banks, insurers, brokers)

**Trigger.** `sector_type == financial-service`. Highest precedence in S2. Also fires for any *division* that is a bank or captive finance arm inside a B10 decomposition.

**What breaks and why.**
- **Debt is raw material, not financing.** Deposits, repos and short-term funding are inputs to the business. You cannot separate operating from financing decisions, so **FCFF and the cost of capital are meaningless** and there is no meaningful firm value.
- **Reinvestment is undefined** in the ordinary sense: capital expenditure and working capital have no clean meaning, so FCFE is barely estimable by the standard formula.
- **Statements do not fit the template**: revenue is reported net (net interest income, net fee income), interest expense is an operating cost, credit-loss provisions are recurring operating expenses, PP&E is negligible, and the operating/investing/financing split of the cash-flow statement carries little information.
- **Manufacturing rating tables mis-price them.** Financial firms operate at far thinner coverage; the standard coverage-to-spread mapping assigns absurd ratings.
- **A hard constraint exists with no analogue elsewhere**: breaching a regulatory capital ratio — computed on *book* equity — can shut the firm down regardless of earnings.

**What replaces it.** Value **equity directly**, by one of three routes:
1. **Dividend discount model** (the default). Growth = retention × **sustainable** ROE. Sustainable ROE adjusts the trailing ROE for any required increase in the capital base (`ROE_sustainable = ROE_trailing / (1 + required capital increase)`) and for leverage the regulator will no longer permit. Fade the payout up toward `1 − g/ROE` as ROE falls; terminal `ROE = cost of equity` unless a durable franchise is argued.
2. **FCFE to regulatory capital** — use when payout no longer reflects capacity, in a crisis, or when capital ratios are moving. Reinvestment *is* the addition to book/regulatory equity: `Investment in regulatory capital = ratio_t × RWA_t − ratio_{t−1} × RWA_{t−1}`; `FCFE = Net income − that investment`. Expect deeply negative early FCFE while capital is rebuilt. Anchor the target ratio on the peer percentile distribution.
3. **Equity excess-return model** — `Value = current book equity + PV of (Net income − cost of equity × beginning book equity)`. Book equity is meaningful here because assets are marked to market. Roll book equity forward consistently; discount at the cumulated cost of equity.

Add an **equity-wipeout probability** for a bank in genuine crisis (a rescued bank's equity is often worth nothing).

**Extra inputs.** Risk-weighted assets path; current and target Tier 1/CET1 ratios with the peer percentile that anchors the target; ROE recovery path anchored on peer percentiles; one-off capital hits (fines, settlements); preferred stock (a real claim ahead of common); bank-sector beta; financial-firm coverage-to-spread table if any rating work is done at all.

**Hard constraints.**
- `no-fcff-valuation` — never an FCFF/WACC valuation, never an enterprise value, never EV/EBITDA or EV/Sales.
- `no-optimal-debt-ratio` — never a WACC-minimizing capital-structure schedule. Capital structure is set by regulatory capital and a chosen equity strategy (regulatory-minimum, self-regulatory, or a buffered combination).
- MUST NOT apply debt-to-capital ratios, EBITDA, or manufacturing rating tables.
- MUST NOT treat the loan-loss provision as extraordinary.
- MUST NOT use trailing ROE as terminal ROE, or when the regulator is about to demand more capital.
- MUST NOT let the payout ratio stay at its high-growth level while ROE falls — `payout = 1 − g/ROE` links them.
- MUST NOT pay dividends or buy back stock in the model when FCFE after regulatory-capital investment is negative.
- MUST NOT mix a hard-currency cost of equity with local-currency earnings (see B9).
- Downstream: the `capital-structure` and `payout` corporate-finance stages are **suppressed**; only the regulatory-capital equity plan runs.

**Outputs.** Equity-only valuation, sustainable-ROE derivation, capital-ratio path with the implied FCFE, wipeout probability, equity-multiple pricing (PBV vs. ROE).

**Concepts.** `concepts/dark-side-difficult/financial-service-firm-valuation.md`, `concepts/dark-side-difficult/bank-fcfe-and-excess-return-models.md`, `concepts/capital-structure/financial-firm-capital-structure.md`, `concepts/dividend-policy/fcfe-for-banks.md`, `concepts/accounting-statements/sector-differences-in-financial-statements.md`, `concepts/dcf-model-choice-loose-ends/dividends-versus-fcfe.md`, `concepts/relative-valuation/book-value-multiples.md`, `concepts/cost-of-debt-capital/synthetic-rating.md`.

---

### B6 · Commodity companies

**Trigger.** A macro price driver exists and explains revenues: regress revenues on the commodity price over as long a history as available and report the R². A high R² means the price essentially *is* the revenue model.

**What breaks and why.** Value depends on a price nobody can forecast reliably. Embedding your own price view makes the answer a blend of two opinions, and no reader can tell which is doing the work — nor can you act on it, because you no longer know whether you are buying a good company or a bet on a commodity. Trough (or peak) margins mistake a point in the cycle for the business. Reserves cap growth permanently.

**What replaces it.** Separate macro from micro.
1. Establish the revenue-price link empirically; report the R².
2. Set base revenue from **today's market price** or the futures strip — never your own forecast.
3. Normalize the margin toward the long-run average; normalize the terminal ROC to the long-run average return.
4. Grow revenues at the firm's own historical compounded rate unless there is a reason to differ.
5. State the answer as *"worth X at today's commodity price"*.
6. State the macro view **separately**, then quantify it: rerun at other prices, or draw the price from a right-skewed distribution and simulate.
7. Undeveloped reserves are a **call option**, not a DCF annuity → **B12**. Developed (producing) reserves are the DCF.
8. Capital structure: run the optimal-debt schedule on both current and normalized EBIT and report both optima; the choice turns on where in the cycle prices sit.

**Extra inputs.** Commodity price history and current spot / futures curve; long-run average margin and ROC windows; reserve estimates split developed vs. undeveloped, with development cost, development lag and relinquishment life; production cost, taxes and royalties per unit.

**Hard constraints.**
- `require-normalized-earnings` when valued at a cycle extreme.
- MUST NOT embed a proprietary commodity forecast in the base valuation.
- MUST NOT use trough (or peak) margins as forecast margins.
- MUST NOT treat reserve life as irrelevant.
- MUST NOT value producing reserves as options or undeveloped reserves as an annuity.
- MUST NOT present a single point estimate when the driver is a volatile price — the simulation costs almost nothing.
- MUST NOT recommend a large debt increase off peak-cycle earnings.

**Outputs.** Price-linked revenue model with R²; normalized margin and ROC anchors; value at the stated price; percentile distribution from the price simulation; option value of undeveloped reserves; both capital-structure optima.

**Concepts.** `concepts/dark-side-difficult/commodity-and-cyclical-valuation.md`, `concepts/dark-side-difficult/normalized-earnings.md`, `concepts/real-options/natural-resource-options.md`, `concepts/dark-side-difficult/scenario-analysis-and-simulation.md`, `concepts/capital-structure/optimal-debt-ratio-by-firm-type.md`, `concepts/accounting-statements/sector-differences-in-financial-statements.md`.

---

### B7 · Cyclical or temporarily troubled firm — normalization

**Trigger.** `earnings_status ∈ {negative-transient, cyclical-trough, cyclical-peak}` AND the cause is **temporary**. Evidence for temporary: the sector is in a known downturn, peers show the same pattern, the firm earned normal margins for years, and the balance sheet survives until recovery. Evidence against: falling market share, a structural demand shift, leverage forcing asset sales.

**What breaks and why.** The base year is not representative. Growth off a depressed or negative base is meaningless, and `g = RIR × ROC` needs a sustainable return. Ratings computed off trough EBIT are wrong, which makes the cost of debt wrong.

**What replaces it.** One of three normalization approaches, chosen by the data you have:
1. **Average earnings** over a full cycle (typically 5 years) — only when firm size has not changed much.
2. **Average return on capital × current book capital** — when the firm has grown, so old dollar earnings understate today's business.
3. **Sector (or own aggregate historical) operating margin × current revenues** — the default when revenues are meaningful and margins collapsed. Use the *aggregate* margin `ΣEBIT / ΣRevenues`, not an average of yearly ratios.

Then recompute everything derived: coverage → synthetic rating → cost of debt → lease capitalization → restated EBIT, iterating to a fixed point. If recovery takes time, **ramp** toward the normalized level rather than jumping to it in year 1. A normalized, mature firm may deserve **no** high-growth period at all.

**Extra inputs.** 5-year (or full-cycle) revenue and EBIT history; sector margin distribution; firm-class-appropriate rating table; a view on cycle position.

**Hard constraints.**
- MUST NOT normalize a permanently broken business — route to B1 or B4 instead. The three approaches will happily produce a healthy EBIT for a firm that will never earn it.
- MUST NOT dollar-average across a period in which the firm changed size materially.
- MUST NOT average ratios where the model wants the aggregate.
- MUST NOT choose a window that starts at the trough and ends at the peak.
- MUST NOT normalize earnings *and* assume a separate recovery in growth and margins.
- MUST NOT leave the depressed coverage ratio in the rating while using normalized EBIT in the cash flows (or vice versa).
- `no-earnings-multiple` on the un-normalized year.

**Outputs.** Normalization approach with justification, normalized EBIT, the re-derived rating/cost of debt, the recovery ramp, and a one-line statement of what normalization added or removed.

**Concepts.** `concepts/dark-side-difficult/normalized-earnings.md`, `concepts/dcf-cashflows-growth/normalizing-depressed-earnings.md`, `concepts/dcf-cashflows-growth/reported-to-actual-earnings.md`, `concepts/cost-of-debt-capital/interest-coverage-ratio.md`, `concepts/cost-of-debt-capital/synthetic-rating.md`.

---

### B8 · Intangible-heavy firms (overlay, applied in S3 before anything else)

**Trigger.** Material R&D (pharma, technology, biotech), material recruiting/training at human-capital firms, or material brand-building advertising at consumer-products firms. Screen on `R&D / revenues` and `R&D / (R&D + net capex)`.

**What breaks and why.** Accounting expenses what is economically a capital expenditure. Therefore, simultaneously: **operating income is understated**, **invested capital is understated**, **reinvestment is invisible**, and **ROIC, ROE, the reinvestment rate, the sales-to-capital ratio and the interest coverage ratio are all wrong** — at exactly the firms where growth matters most. Book-value multiples and EV/Invested-Capital are meaningless on unrestated capital. Balance-sheet intangibles sit far below true value.

**What replaces it.** Capitalize, **before** any valuation:
- Choose the amortizable life from the industry lookup (2 years for retail/services, 3 for software and consumer brands, 5 for light manufacturing and semiconductors, 10 for pharma, aerospace and heavy manufacturing).
- `Research asset = Σ_k R&D_{−k} × (N−k)/N`; `Amortization = Σ_{k≥1} R&D_{−k}/N`; `ΔEBIT = current R&D − amortization` (**can be negative** when R&D spending is shrinking).
- Add the research asset to book equity and invested capital; add current-year R&D to capital expenditure.
- Recompute ROE and ROC — they usually **fall**, because capital rises proportionally more than income.
- Recompute the coverage ratio, and therefore the synthetic rating and the cost of debt.

**Extra inputs.** R&D (or recruiting, or brand-advertising) history for N+1 years; the industry amortizable-life table; a split of advertising into brand-building versus maintenance.

**Hard constraints.**
- MUST NOT expect the fix to improve returns.
- MUST NOT add the research asset to capital while leaving R&D out of capital expenditure — that manufactures free growth.
- MUST NOT assume the EBIT adjustment is positive.
- MUST NOT use a single amortizable life across a diversified company.
- MUST NOT apply the restated ROC to set growth while leaving the reinvestment rate on the old basis.
- MUST NOT treat the whole advertising budget as capital.
- MUST propagate the restatement into coverage, rating and cost of debt.
- Brand value, if computed separately (re-value with a generic competitor's margin), MUST NOT be added on top of a valuation that already carries the brand-driven margin.

**Concepts.** `concepts/dark-side-difficult/capitalizing-rd.md`, `concepts/dcf-cashflows-growth/rnd-capitalization.md`, `concepts/accounting-statements/intangibles-and-goodwill.md`, `concepts/relative-valuation/ev-sales-and-brand-value.md`, `concepts/dcf-model-choice-loose-ends/other-non-operating-assets.md`.

---

### B9 · Emerging-market and country-risk exposure (overlay)

**Trigger.** Any material revenue, production or asset exposure to markets with sovereign risk — **assigned by exposure, not by passport**. A Brazilian exporter carries less Brazil risk than a Brazilian retailer; Coca-Cola and Heineken carry plenty of emerging-market risk while incorporated in developed markets.

**What breaks and why.** Four of the four questions bend at once. Inflation and interest-rate shifts plus weak accounting distort the earnings history. Growth is tied to the country. Country risk moves and is not captured by a domestic beta. Crises, nationalization and regime change can end the story. Equity value is distorted by cross-holdings. And the usual "fixes" — a discount-rate bump, a flat emerging-market discount, a governance haircut — are unfalsifiable and often triple-count.

**What replaces it — a four-part stack applied on top of an ordinary DCF:**

1. **Currency first.** Value in any currency; the answer must be invariant. Build the riskfree rate either from a genuinely default-free bond in that currency, or from a reliable riskfree rate plus the inflation differential: `(1+r_X) = (1+r_US) × (1+i_X)/(1+i_US)`. Strip the sovereign default spread out of a local government bond before using it. Use PPP-consistent expected exchange rates, never a flat spot rate across ten years. Negative riskfree rates are handled, not avoided — they simply push nominal stable growth negative. Cross-check by re-running in a second currency.
2. **Country risk by exposure.** `CRP = country default spread × relative equity market volatility`; `ERP_country = mature ERP + CRP`. Attach it either as a **revenue-weighted ERP** (`ERP_company = Σ w_i × ERP_i`) when a geographic revenue split exists, or via a **lambda** (`k_e = r_f + β × mature ERP + λ × CRP`) when exposure differs from the revenue split because of production location, sourcing, hedging, or demand sensitivity. `λ = 1` is average domestic exposure; exporters and globally diversified firms sit well below 1. Add the country default spread to the **cost of debt** as well.
3. **Cross-holdings** → **B11**.
4. **Truncation** (sub-branch): nationalization, regime change, war, uninsurable catastrophe. These do not reduce cash flows, they **end** them. Build the branch as its own DCF wherever possible — partial expropriation and harsher fiscal terms are far more common than total loss and have a computable value — assign a probability, and blend. State the probability prominently; it is the only genuinely subjective input.

Governance drag rides along with this stack: value the firm as run, then with returns fixed (both the new-investment lever and the larger existing-asset lever), and weight by the probability anyone forces the change → **B2**.

**Extra inputs.** Revenue (and production) split by country; country rating, default spread and relative equity-market volatility; expected inflation for both currencies; sovereign default spread for the local government bond; lambda evidence; political-risk assessment for the truncation branch; stable-phase country premium (usually assumed to fall).

**Hard constraints.**
- MUST NOT assign country risk by country of incorporation.
- MUST NOT apply a country premium **and** a blanket emerging-market value discount.
- MUST NOT stack a country risk premium + a nationalization scenario + a governance discount — that is three charges for overlapping risks.
- MUST NOT put a country premium in the cost of equity while forgetting the country spread in the cost of debt.
- MUST NOT hold the country premium at its current level in perpetuity without saying so.
- MUST NOT discount local-currency cash flows at a hard-currency cost of capital.
- MUST NOT let stable growth exceed the currency's own riskfree rate.
- MUST NOT change the ERP because the currency changed — the ERP tracks operating exposure.
- MUST NOT set the truncated branch to zero by reflex.
- MUST NOT use a lambda you cannot justify; fall back to revenue weighting and say so.

**Concepts.** `concepts/dark-side-difficult/country-risk-exposure.md`, `concepts/dark-side-difficult/currency-consistency-and-invariance.md`, `concepts/dark-side-difficult/truncation-and-political-risk.md`, `concepts/dark-side-difficult/return-improvement-and-governance-drag.md`, `concepts/cost-of-equity/country-risk-premium.md`, `concepts/cost-of-equity/operation-weighted-erp.md`, `concepts/cost-of-equity/lambda-country-risk-exposure.md`, `concepts/cost-of-equity/currency-riskfree-rate.md`, `concepts/cost-of-debt-capital/country-risk-in-cost-of-debt.md`, `concepts/cost-of-debt-capital/currency-conversion-of-discount-rates.md`.

---

### B10 · Multi-business firms, divisions and sum-of-the-parts

**Trigger.** `business_count > 1` with distinct economics and separable, traceable cash flows; or a division is being valued for a spin-off or sale; or the mandate asks whether the firm is worth more broken up.

**Feasibility test first** (all three should hold; the more that fail, the less defensible the result): **separability**, **traceable cash flows**, **an active market in similar assets**. Brand name is the canonical failure — it cuts across every asset and cannot be carved out.

**Motive determines the route:**

| Who is asking | Route |
|---|---|
| Passive long-term investor betting on a mispricing | **Intrinsic** sum-of-the-parts (divisional DCFs) |
| Activist / acquirer / board considering a break-up | **Relative** sum-of-the-parts (price each division off its sector) |
| Liquidator | Price the assets off comparable transactions; add an urgency discount if the sale is forced; book value only as a last-resort proxy |
| Accountant under a fair-value mandate | Exit price: level 1 quotes → level 2 observable inputs for similar assets → level 3 model, and report which level was used |
| Firm preparing a spin-off | Relative for the transaction price, intrinsic for the reservation price |

**What breaks and why.** One company-wide cost of capital and one company-wide multiple across divisions with different risk is the single most common error and it moves the answer a lot. Segment EBIT is often reported *before* corporate G&A, so divisional values double-count the missing overhead. A captive finance arm's debt and economics follow bank logic, not manufacturing logic.

**What replaces it.**
- **Per-division cost of capital**: bottom-up unlevered beta from that division's sector, levered at the parent's D/E unless the division would carry different debt standalone.
- **Per-division fundamentals**: `ROC = after-tax EBIT / invested capital`; `RIR = allocated reinvestment / after-tax EBIT`; `g = RIR × ROC`.
- **Zero-growth rule**: a division whose `ROC ≤ its own cost of capital` gets a **zero-year** high-growth period. Growth there adds nothing.
- **Stable ROC = that division's cost of capital** unless a durable advantage is argued.
- **Capitalize unallocated corporate expenses** as an after-tax growing perpetuity at the *company-wide* cost of capital, and subtract.
- **Relative route**: pick the multiple whose sector regression has the **highest R²** per division, evaluate it at the division's own fundamentals (not the sector median), then multiply by the matching scalar.
- **Bridge once**: subtract all debt including any finance arm's debt, subtract minority interests, add cash, subtract option value.
- **Compare four numbers**: intrinsic SOTP, relative SOTP, whole-company DCF, market enterprise value. The spread is the finding — and it is a conglomerate discount only if somebody would actually buy the pieces.

**Hard constraints.**
- MUST NOT apply one cost of capital or one multiple across divisions.
- MUST NOT grant a high-growth period to a sub-cost-of-capital division.
- MUST NOT drop unallocated corporate expenses.
- MUST NOT mismatch multiple and scalar (an EV/Capital multiple against EBITDA, an equity multiple against an enterprise scalar).
- MUST NOT forget a captive finance arm's debt in the bridge.
- MUST NOT value a bank division on FCFF — apply **B5** to it and add it as an equity block.
- MUST NOT read a conglomerate discount as automatic free money, nor ignore that pieces may be worth less apart when real synergies exist.
- MUST NOT add back going-concern items (brand, assembled workforce, synergies) in a liquidation frame.

**Concepts.** `concepts/asset-based-private/asset-based-valuation-overview.md`, `concepts/asset-based-private/sum-of-the-parts-framework.md`, `concepts/asset-based-private/sum-of-the-parts-dcf.md`, `concepts/asset-based-private/sum-of-the-parts-pricing.md`, `concepts/asset-based-private/liquidation-valuation.md`, `concepts/asset-based-private/fair-value-accounting-fas157.md`, `concepts/cost-of-debt-capital/divisional-cost-of-capital.md`, `concepts/accounting-statements/segment-and-geographic-reporting.md`.

---

### B11 · Cross-holdings and group structures (overlay, applied in the bridge)

**Trigger.** Any consolidated subsidiary less than wholly owned; any minority stake in another firm; pyramid or circular group ownership; `holdings_share` material. Common in emerging markets, where cross-holdings often exist to preserve control.

**What breaks and why.** In many group companies the real work starts *after* the DCF, because half the value sits in stakes in other companies — valued with very little information. A perfect operating DCF can still be half a valuation. Marking stakes at book value bears no relation to worth. Book minority interests understate the claim when the subsidiary is profitable.

**What replaces it.**
- List every holding with ownership % and accounting treatment (consolidated / equity method / cost).
- **Majority (consolidated)**: the subsidiary is already inside operating income → **subtract minority interest at estimated market value**, not book.
- **Minority (unconsolidated)**: not in operating income → **add** `ownership % × value of subsidiary equity`. Value it properly if listed; if opaque, apply a sector price-to-book or earnings multiple to its book equity and **disclose the approximation**.
- Report the composition: % of value from operating assets, from holdings, from cash. Flag prominently when holdings exceed roughly a third — the error bars then live in the holdings.

**Hard constraints.**
- MUST NOT mark holdings at book value.
- MUST NOT subtract book minority interest.
- MUST NOT add a stake's value while its earnings remain in operating income.
- MUST NOT flip majority/minority treatment — the sign of the adjustment reverses.
- MUST NOT consolidate a JV's operating assets and also carry its equity value as a holding.

**Concepts.** `concepts/dark-side-difficult/cross-holdings.md`, `concepts/dcf-model-choice-loose-ends/cross-holdings.md`, `concepts/accounting-statements/non-operating-items-and-cross-holdings.md`, `concepts/dcf-model-choice-loose-ends/equity-value-bridge.md`, `concepts/dcf-model-choice-loose-ends/complexity-discount.md`.

---

### B12 · Real options (overlay; gated, and most candidates fail the gate)

**Trigger.** Any item on `option_candidates`: product patents, undeveloped natural-resource reserves, exclusive licences or development rights, contractual abandonment/exit rights, expansion rights, excess debt capacity and cash held for flexibility, and equity in a deeply levered loss-making firm.

**The gate — three sequential tests. All three must pass before any premium is admissible.**
1. **Option test.** Name (a) a clearly defined underlying asset whose value changes unpredictably and (b) a payoff contingent on a specified event **within a finite period**. If you cannot name both, stop — there is no option.
2. **Exclusivity test.** In a perfectly competitive product market, no contingency generates positive NPV however volatile the underlying, because competitors compete the excess return away. Score the barrier on the ladder: first-mover advantage (weakest) < technological edge < brand name < licences < pharmaceutical patents (strongest). Then apply the three sliding scales — is the first investment a **prerequisite** for the second; is there a **competitive advantage** on the second; will the second earn **excess returns**? Any scale at zero ⇒ the option is worth **zero**, regardless of what the model returns.
3. **Pricing test.** Is the underlying traded (observable price and volatility, replication possible)? Is the option itself traded? Is the exercise cost knowable? Trust the output in proportion to how many hold. When they fail — the normal case for real assets — the estimate is far noisier and unarbitraged.

**Routing after the gate:**

| Candidate | Structure | Key mechanics |
|---|---|---|
| Product patent | Call: `S` = PV of cash flows from launching now, `K` = development cost, `t` = patent life, `y = 1/n` cost of delay | Dividend-adjusted Black-Scholes; compute the **optimal exercise date** where option value crosses `S − K` |
| Undeveloped reserves | Call: `S = reserves × (price − production cost) / (1+y)^lag`, `K = reserves × development cost`, `t` = relinquishment life | The **development-lag** discount and the net-production-revenue dividend yield are both mandatory |
| Expansion into a new market | Call on the expansion's PV, struck at entry cost | Noisiest application; scale hard by the exclusivity factor |
| Abandonment / exit right | **Put**: `S` = PV of remaining flows, `K` = salvage, `t` = **life of the exit right** (not the project life), `y = 1/project life` | Requires a real counterparty obliged to buy, or a liquid resale market |
| Financing flexibility | Call on reinvestment needs; value it, then scale by `excess return / WACC`, and compare against the **cost** (current WACC − optimal WACC) | Zero excess returns ⇒ flexibility is worth zero |
| Equity in a distressed levered firm | Call on firm value struck at debt face value, life = face-value-weighted **duration** | See B4; an alternative equity estimate, never additive |
| Whole-firm patent portfolio | `DCF of commercial products + Σ option value of undeveloped patents + PV of excess value from future R&D` | The third term is zero once research merely earns its cost of capital; truncate at the competitive-advantage window |

**Engine choice.** Prefer the **binomial** tree when early exercise matters or values jump — the normal case for real assets. Black-Scholes only for continuous processes with no jumps, and always in its **dividend-adjusted** form (omitting the cost-of-delay yield is the single largest overstatement error on long-dated real options). When the pricing test fails but tests 1 and 2 pass, use a **decision tree** instead: the option lives at the decision nodes, where you take the max over available actions.

**Extra inputs.** Underlying value `S` from a full capital-budgeting exercise; volatility proxy (comparable-firm variance, resource-price variance, or a simulation of PV); exercise cost; legal/competitive window; matched-maturity riskfree rate; cost-of-delay yield; the exclusivity factor and its justification.

**Hard constraints.**
- MUST NOT add a premium without running the exclusivity test. Most real options are worth nothing precisely because anyone can exercise them.
- MUST NOT leave the exclusivity factor at an unstated 1.0.
- MUST NOT use volatility to rescue a case with no barriers — high variance multiplies zero.
- MUST NOT double count: if the patent, reserve or expansion is valued as an option, its growth MUST be removed from the DCF.
- MUST NOT build a decision tree *and* add an option premium — they are alternative representations of the same optionality.
- MUST NOT omit the dividend/cost-of-delay yield, or the development lag on a resource option.
- MUST NOT value producing reserves as options.
- MUST NOT use the equity's own volatility where the model needs **firm-value** variance.
- MUST NOT quote real-option values to the dollar.

**Concepts.** `concepts/real-options/real-options-framework.md`, `concepts/real-options/opportunities-are-not-options.md`, `concepts/real-options/option-to-delay.md`, `concepts/real-options/patent-valuation-as-option.md`, `concepts/real-options/valuing-a-firm-with-patents.md`, `concepts/real-options/natural-resource-options.md`, `concepts/real-options/option-to-expand.md`, `concepts/real-options/option-to-abandon.md`, `concepts/real-options/financing-flexibility-option.md`, `concepts/real-options/black-scholes-model.md`, `concepts/real-options/replicating-portfolio-and-binomial-model.md`, `concepts/real-options/decision-trees-vs-option-pricing.md`, `concepts/real-options/option-payoffs-and-determinants.md`, `concepts/narrative-numbers/contingent-claim-valuation.md`, `concepts/project-returns/project-options.md`.

---

### B13 · Private companies — routing by transaction motive

**Trigger.** `ownership == private` and the mandate is not an IPO.

**What breaks and why — two structural problems.**
1. **No market value.** No market D/E for levering betas or weighting the WACC; no regression beta; no bond rating; no market price to value employee options; and — most dangerous — **no market price to bump into if you make an error**.
2. **Weak statements.** Short history; looser accounting; personal expenses run through the business; and no clean line between "salaries" and "dividends" because both end up with the same person.

On top of that, **a private business does not have one value**. It has a value per buyer and per purpose.

**Mandatory pre-steps, in order** (order matters: the coverage ratio that sets the cost of debt uses the lease expense from step 1, and the key-person haircut must precede the growth calculation):
1. **Statement cleanup** — capitalize operating leases as debt (`PV of lease payments at the pre-tax cost of debt`), charge a **market salary** for the owner's actual role, strip genuinely personal expenses, note whether the business is at full capacity (if so, revenue growth requires capital expenditure).
2. **Key-person haircut** — haircut **operating income** by the fraction `k` of the business that walks out with the owner (customer concentration, personal referrals, whether reputation attaches to the person or the establishment). Applied to income, *not* to final value, so it flows through cash flows, reinvestment and terminal value together. `k` is negotiable — transition terms, non-competes and earn-outs shrink it.
3. **Discount rate** — bottom-up unlevered beta from comparables chosen on **business economics, not industry label**; convert to a **total beta** (`market beta / ρ`, `ρ = sqrt(average comparable R²)`) if the buyer is undiversified; lever at the **industry-average market D/E** (using your own estimated values is circular and requires iteration); synthetic rating from a coverage ratio that counts lease payments as interest.

**The four scenarios (sub-branches):**

| # | Scenario | Beta | Illiquidity discount | Notes |
|---|---|---|---|---|
| **B13-I** | Private → private (undiversified individual buyer) | **Total beta** | **Yes** | The base case. `require-total-beta`, `require-illiquidity-discount`. |
| **B13-II** | Private → public company | **Market beta** | **No** | Use the buyer's tax rate. The gap between I and II is the **bargaining range**, not an error; where the price lands depends on the number of bidders and relative urgency. |
| **B13-III** | Private → IPO | **Market beta** | **No** | Routes to **B14**. |
| **B13-IV** | Private → VC → public | **Stage-varying** perceived beta | **Fades out** | Cost of equity falls in steps as ownership moves founder → specialized VC → public. Discount each year's cash flow by a **cumulated product** of that year's rate, never a single rate raised to a power. Terminal value uses the **post-transition** rate. |

A **partially diversified** buyer (PE or VC fund) sits between I and II: use that fund's own portfolio correlation with the market, not a single-asset holder's.

**Stake size.** `stake_size > 50%` → price off the **optimal** value; `≤ 50%` → price off the **status quo** value. `Minority discount = (Optimal − Status quo)/Optimal`, derived from two valuations, never from a convention. Illiquidity and lack of control are **different frictions**; applying both to the same stake needs a reason, not reflex.

**Illiquidity routes** (pick one and say which):
- Bid-ask spread regression evaluated at zero trading volume: `0.145 − 0.0022·ln(Revenues $m) − 0.015·DERN − 0.016·(Cash/Firm value) − 0.11·(Volume/Firm value)` — the most firm-specific and least sampling-biased route.
- Silber-refined base: shift a 25% base by the gap between the predicted discount for the subject firm and for a $10m-revenue profitable anchor.
- Flat 20–30% only as a sanity check or because the counterparty expects it.
- Adjust for the three dimensions the models cannot see: **company** (size, health, asset liquidity), **time** (credit conditions), **buyer** (horizon, cash needs).

**Other motives.** "Show" valuations (curiosity, estate tax, divorce) are explicitly advocacy-driven — the assumptions and the value depend on which side you sit on; state the side. Valuing a division of a public firm → **B10**.

**Hard constraints.**
- `require-total-beta` for an undiversified buyer; MUST NOT use a market beta there (it roughly doubles the value and hands the surplus to the buyer).
- `require-illiquidity-discount` unless the buyer is public/liquid; MUST NOT apply it to a public buyer or an IPO.
- MUST divide by the correlation `ρ = sqrt(R²)`, **not** by R².
- MUST NOT apply full total beta to a partially diversified fund.
- MUST lever the beta and weight the WACC at the **same** D/E; MUST NOT confuse `D/E` with `D/(D+E)`.
- MUST apply the illiquidity discount to **equity** value, not firm value.
- MUST NOT apply the key-person discount to final value.
- MUST NOT double-count the owner salary adjustment with the key-person haircut — the first prices the owner's *work*, the second the owner's *pull*.
- MUST NOT skip the capitalized lease debt in the final bridge after adding it to the capital structure.
- MUST NOT read three good years as a trend.
- MUST NOT quote one number to both sides of a negotiation — both valuations are correct and answer different questions.

**Concepts.** `concepts/asset-based-private/private-company-valuation-framework.md`, `concepts/asset-based-private/private-company-statement-cleanup.md`, `concepts/asset-based-private/key-person-discount.md`, `concepts/asset-based-private/total-beta.md`, `concepts/asset-based-private/private-company-cost-of-capital.md`, `concepts/asset-based-private/illiquidity-discount.md`, `concepts/asset-based-private/silber-restricted-stock-regression.md`, `concepts/asset-based-private/bid-ask-spread-illiquidity-regression.md`, `concepts/asset-based-private/minority-discount.md`, `concepts/asset-based-private/private-to-private-valuation.md`, `concepts/asset-based-private/private-to-public-sale.md`, `concepts/asset-based-private/vc-stage-varying-cost-of-equity.md`, `concepts/cost-of-equity/non-traded-asset-betas.md`, `concepts/capital-structure/optimal-debt-ratio-by-firm-type.md`.

---

### B14 · IPO

**Trigger.** `transaction_motive == ipo`, or a private company being valued as a prelude to an offering price.

**What breaks and why.** Two things change with the listing: **control** (the firm becomes subject to monitoring by investors, analysts and the market) and **disclosure**. The buyers are diversified, so the private-company risk identity no longer applies. And three IPO-specific adjustments sit between a correct business valuation and a correct per-share number — get any of them wrong and the value per share is wrong even when the business valuation is right.

**What replaces it.**
1. Value the business as an ordinary DCF with **market betas** and **no illiquidity discount**. Let the cost of capital decline over the forecast toward a stable-growth value as risk falls. If the firm is young and loss-making, the engine is still **B1**.
2. **Use of proceeds** — read the prospectus and classify:
   - Taken out by existing owners → **add nothing**.
   - Used to pay down debt → change the debt ratio, recompute the cost of capital, revalue.
   - Retained for future reinvestment → **add dollar for dollar**.
   - Split uses → add only the retained portion.
3. **Prior equity claims** — enumerate founder shares, each round of convertible preferred (normally converts at the offering), restricted stock units, employee options, and shares owed under acquisition agreements.
4. **Share count** — everything that is or becomes common goes in the denominator; **options stay out of the denominator and their value comes out of the numerator**. Use an expected option life, not the stated life.
5. **Pricing is a separate question from value.** The banker sets the offer price under a pricing guarantee that pushes it below fair value; expect underpricing (first-day returns positive in every size bucket, largest for the smallest deals; a 10–15% working assumption). The cost to the owner is `underpricing % × value of the shares actually sold`, not of the whole company — which is why small initial floats are common. Rationing (the winner's curse) means the average underpricing cannot be harvested. Direct listings and SPACs are the alternatives to the intermediated model.

**Extra inputs.** Prospectus use-of-proceeds language; the full cap table with conversion terms; option pool with strike, stated life and volatility; comparable-set metrics for the pricing exercise; float size and staging plan.

**Hard constraints.**
- MUST NOT use a total beta or an illiquidity discount.
- MUST NOT add proceeds the existing owners are withdrawing.
- MUST NOT count options in the denominator **and** subtract their value.
- MUST NOT omit convertible preferred, RSUs or shares owed under acquisition agreements from the share count.
- MUST NOT hold the cost of capital constant for a young company.
- MUST NOT present the offer price as the valuation, nor the peer-multiple pricing as a value.
- MUST NOT price off a metric the market has stopped paying for.

**Concepts.** `concepts/asset-based-private/ipo-valuation.md`, `concepts/asset-based-private/ipo-pricing-and-underpricing.md`, `concepts/asset-based-private/vc-stage-varying-cost-of-equity.md`, `concepts/dark-side-difficult/dilution-and-employee-options.md`, `concepts/dcf-model-choice-loose-ends/valuing-employee-options.md`, `concepts/dcf-model-choice-loose-ends/employee-option-per-share-approaches.md`, `concepts/relative-valuation/pricing-young-companies.md`.

---

### B15 · Acquisition analysis

**Trigger.** `transaction_motive == acquisition` (or `mode == acquisition`). Wraps whichever engine the target's own classification selects.

**Prior to set before any number is produced.** Acquirers usually destroy value and the failure is structural: target shareholders capture nearly all the announcement gain, bidders capture roughly nothing and drift negative; a large share of acquisition programmes fail their own value tests; a substantial fraction of deals are divested within a decade. The burden of proof belongs on the deal, not on the skeptic.

**Only three value reasons exist** — undervaluation, control, synergy. Anything else ("strategic", "transformational") is not a value reason. Each has its own benchmark, and all four numbers must be produced:

| # | Number | Source |
|---|---|---|
| 1 | Acquisition price | Negotiated; for a public target, a premium over the pre-announcement market cap |
| 2 | **Status quo value** | Full DCF of the target as currently run → **B2** step 1 |
| 3 | **Restructured value** | DCF with changed investing / financing / payout policy → **B2** |
| 4 | **Synergy value** | `Combined with synergy − [Acquirer standalone + **Restructured** target]` |

**The acid test:** undervaluation requires `Price < Status quo`; control requires `Price < Restructured`; synergy requires `Price < Restructured + Synergy`. If price exceeds the benchmark, exactly two explanations survive — the synergy was underestimated, or the acquirer is overpaying. Decide which, and say so.

**Mandatory disciplines (the seven-sin audit, run *before* commitment):**
1. **Risk transference** — discount the target at the **target's own** cost of equity and business risk. A risky business does not become safe because a safe buyer owns it.
2. **Debt subsidy** — use the **target's own** debt capacity and cost of debt. Genuine added debt capacity in the *combined* firm is a **financial synergy**, valued separately, never smuggled into the target's WACC.
3. **Control premium** — derived as `Restructured − Status quo`, never a rule-of-thumb percentage. A perfectly run target carries a control premium of zero. No stacking of brand or management-quality premiums on top of a DCF that already contains them.
4. **Synergy** — map every claimed benefit to exactly one valuation input (higher ROC, higher reinvestment rate, longer growth period, higher margin, lower tax rate, higher debt ratio). A claim that maps to nothing is a buzz word. **Diversification is not a synergy for public firms.** Split cost from revenue synergies and value them separately: cost synergies land, revenue synergies mostly do not (~70% of mergers miss expected revenue synergies); haircut revenue synergies for 2–5% integration customer attrition; subtract one-time costs to achieve; build cost synergies bottom-up, location by location.
5. **Comparables and exit multiples** — precedent-transaction multiples are a sample of *overpayments*; an exit-multiple terminal value is a relative valuation wearing DCF clothing. EPS accretion is guaranteed whenever `PE_acquirer > PE_target` and carries no information.
6. **Bias** — reconstruct the chronology. A valuation dated after the price is a rationalization. Set a walk-away price before any auction and drop out when it is exceeded (losers of bidding wars materially outperform winners).
7. **Accountability** — name the individual whose compensation depends on the promised benefits arriving, and tie advisor pay to deal performance rather than completion.

**Deal-design odds** (shift the base rate before valuing): sole bidder > bidding war; private target or subsidiary > public target; cash > stock; small target > large target; cost synergies > growth synergies. Note the interaction: large deals are dangerous for *public* targets while private and subsidiary deals perform *better* as size rises.

**Price build-up and goodwill.** Decompose the price: pre-deal book equity → + purchase-accounting intangibles = adjusted book equity → + market premium over book = pre-deal market cap → + acquirer's premium = price. `Goodwill = Price − adjusted book equity`, and it is a public promise to create that much value. Test it on announcement day, not at the write-off.

**Hard constraints.**
- MUST NOT discount the target at the acquirer's cost of equity or with the acquirer's debt capacity.
- MUST NOT use a fixed control-premium percentage.
- MUST NOT build the synergy baseline on the target's **status quo** value while also claiming control value — use the restructured value or control gains are counted twice.
- MUST NOT let the combined firm inherit a lower cost of capital purely from combining.
- MUST NOT set terminal value with an exit multiple.
- MUST NOT report accretion/dilution as a deal test.
- MUST NOT pay the full value of control or the full synergy value — that hands the entire gain to the seller.
- MUST verify the arithmetic identity: the no-synergy combined value must equal the sum of the standalone values exactly. If it does not, an assumption is inconsistent.
- Options-adjacent: a fairly priced diversifying merger with no releveraging transfers wealth from stockholders to bondholders (combined variance falls, and equity is long volatility). Treat that as a real, computable cost, not a rhetorical point.

**Concepts.** `concepts/acquisitions-control-enhancement/three-reasons-and-acid-test.md`, `concepts/acquisitions-control-enhancement/status-quo-valuation.md`, `concepts/acquisitions-control-enhancement/restructured-value-and-value-of-control.md`, `concepts/acquisitions-control-enhancement/valuing-synergy.md`, `concepts/acquisitions-control-enhancement/synergy-taxonomy.md`, `concepts/acquisitions-control-enhancement/synergy-delivery-odds.md`, `concepts/acquisitions-control-enhancement/target-discount-rate-discipline.md`, `concepts/acquisitions-control-enhancement/control-premium-rules-of-thumb.md`, `concepts/acquisitions-control-enhancement/transaction-and-exit-multiples.md`, `concepts/acquisitions-control-enhancement/seven-sins-of-acquisitions.md`, `concepts/acquisitions-control-enhancement/deal-bias-and-ego.md`, `concepts/acquisitions-control-enhancement/acquisition-empirical-record.md`, `concepts/acquisitions-control-enhancement/acquisition-strategy-design.md`, `concepts/acquisitions-control-enhancement/acquisition-price-buildup-and-goodwill.md`, `concepts/acquisitions-control-enhancement/abinbev-sabmiller-case.md`, `concepts/real-options/conglomerate-merger-wealth-transfer.md`, `concepts/project-returns/acquisitions-as-projects.md`.

---

### B16 · Macro shock and market-level revaluation (overlay)

**Trigger.** A material move in the macro inputs between the last valuation and the valuation date — riskfree rate, equity risk premium, default spreads, base earnings, tax regime — or an explicit mandate to value an index.

**What breaks and why.** Intrinsic value is not a fixed anchor the market wanders around. It is built from macro inputs, and those move violently in a crisis. Treating a fall in your own value estimate during a crisis as a mistake is itself the mistake.

**What replaces it.**
- **Index valuation** takes six inputs. Base aggregate earnings. **Augmented** cash returned, meaning dividends **plus** buybacks — buybacks are now as large as dividends, and total payout regularly exceeds 100% of earnings in stress years. An earnings path split into transitory and permanent damage, with a stated recovery fraction and year. A payout path that falls and then recovers. A required return of `riskfree + ERP`, anchored on the historical average of the **implied** premium over a stated window, plus explicit assumptions about what both do after year 5. And perpetual growth capped at the riskfree rate.
- **Company revaluation in a shock** changes four things. Base earnings. Growth inputs, usually a lower reinvestment rate or a lower ROC. The ERP and the default spread, which both spike. The capital-structure path, if the firm can no longer move to target. Then **attribute the change in value to each input separately**, so the story is auditable.
- Do not read a market rally against terrible current macro data as irrationality: stock returns correlate negatively with current-quarter GDP and positively with GDP three to four quarters ahead.

**Hard constraints.**
- MUST NOT value an index off dividends alone.
- MUST NOT combine analyst growth with an unadjusted payout ratio — `payout = 1 − g/ROE` links them.
- MUST NOT assume the crisis riskfree rate and the crisis ERP both persist forever; they usually revert in opposite directions, and the terminal value is where that matters.
- MUST NOT change several macro inputs without attributing the value change to each.

**Concepts.** `concepts/dark-side-difficult/market-and-macro-crisis-valuation.md`, `concepts/cost-of-equity/implied-equity-risk-premium.md`, `concepts/cost-of-equity/choosing-an-equity-risk-premium.md`, `concepts/relative-valuation/market-pe-vs-bond-alternative.md`, `concepts/relative-valuation/country-pe-regression.md`, `concepts/dark-side-difficult/scenario-analysis-and-simulation.md`.

---

## Part III — Constraint catalogue (the compiled hard stops)

Emitted by the branches above; enforced by every downstream agent and checked by S11-V9. IDs are stable identifiers.

| ID | Fires when | Meaning |
|---|---|---|
| `no-fcff-valuation` | B5 | Financial service firm: debt is raw material, not financing. Value equity directly. |
| `no-optimal-debt-ratio` | B5, B5b | Regulatory capital governs. No WACC-minimizing schedule. |
| `no-enterprise-multiple` | B5, B5b | EV/EBITDA, EV/Sales, EV/IC are meaningless where debt is raw material. |
| `no-earnings-multiple` | B1, B4, B7 (un-normalized year) | PE, PEG, EV/EBIT are undefined on negative or trough earnings. |
| `no-standard-growth-model` | B1 | Growth must be built from revenue and a target margin, not an earnings growth rate. |
| `require-failure-probability` | B1, B3+leverage, B4 | A going-concern DCF alone overstates value. |
| `require-normalized-earnings` | B6, B7 | Commodity or cyclical firm at a cycle extreme. |
| `no-normalization` | B1 (structural losses), B3 | Normalizing a permanently broken business values a company that does not exist. |
| `require-total-beta` | B13-I, B13-IV early stages | Undiversified owner prices total risk. |
| `require-illiquidity-discount` | B13-I | Unless the buyer is public and liquid. |
| `no-illiquidity-discount` | B13-II, B13-III, B14 | Buyer's investors have a market. |
| `require-key-person-haircut-on-income` | B13 owner-operated | Applied to operating income, never to final value. |
| `require-rd-capitalization` | B8 | Restate EBIT, capital, ROIC, reinvestment and coverage before valuing. |
| `require-exposure-weighted-risk` | B9 | Country risk by operations, not by incorporation. |
| `no-blanket-country-discount` | B9 | Premium or scenario, never plus an arbitrary haircut. |
| `no-governance-discount` | B2, B9 | Model weak governance as low returns and low `P(change)`. |
| `require-divisional-rates` | B10 | One cost of capital per division, never company-wide. |
| `zero-growth-below-cost-of-capital` | B10 | A division earning ≤ its cost of capital gets no high-growth period. |
| `require-market-value-minorities` | B11 | Never subtract book minority interest. |
| `require-exclusivity-scaling` | B12 | No unstated 1.0 exclusivity factor. |
| `no-option-premium-without-gate` | B12 | All three tests must pass. |
| `no-exit-multiple-terminal-value` | B15 | Smuggles today's pricing into an intrinsic valuation. |
| `require-target-own-discount-rate` | B15 | No risk transference, no debt subsidy. |
| `synergy-baseline-is-restructured-target` | B15 | Prevents double-counting control gains. |
| `no-perpetual-growth-above-riskfree` | universal | Terminal growth cannot exceed the riskfree rate in the valuation currency. |
| `single-charge-per-risk` | universal | Each risk priced exactly once (S11-V1). |
| `no-intrinsic-valuation` | S0 (no cash flows ever) | Priceable only. |

---

## Part IV — Determinism boundary for this framework

| Element | Script computes | Agent judges |
|---|---|---|
| S1 signals | every ratio, screen and threshold comparison | whether a computed signal is representative (a trough coverage ratio, a distorted beta, a one-off margin) |
| S2–S5 gates | the branch selection, given the signals | the sector call for a hybrid firm; whether losses are transient or structural; whether policies are "stable and bad" |
| S6 distress | probability inversion from bond prices; cumulative-from-annual conversion; the blend | the recovery percentage; whether equity retains any claim; whether the market price reflects distress or illiquidity |
| S7 constraints | compilation and conflict detection | nothing — this is mechanical once branches are assigned |
| S8 combination | precedence resolution, exclusion checks, pipeline ordering | the multi-branch resolutions where two engines are both arguable |
| S9 pricing route | multiple selection given the forbidden list; regression evaluation | comparable-set definition; whether an R² justifies acting |
| S10 uncertainty | the grid, the simulation, the percentiles, the gap-to-return conversion | which drivers deserve the grid; distribution shapes; correlations; whether a price-justifying scenario is *probable* |
| S11 validation | every predicate | severity triage and what an unresolved finding means for the verdict |

The recurring pattern across every branch: **the arithmetic is almost always mechanical; the inputs almost never are.** Route correctly first. Then spend the analytical effort on the two or three judgments the branch actually turns on. For B1 that is the mature end-state; for B5 the sustainable ROE; for B6 the price basis and the long-run margin; for B12 the exclusivity factor; for B13 `k` and the buyer's diversification; for B15 the synergy realization.
