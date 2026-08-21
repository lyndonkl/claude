# Framework: The End-to-End Corporate Finance Analysis Playbook

**Mode:** `corporate-finance` (SPEC §2). **Terminal artifact:** a 10-part corporate finance assessment plus an executive scorecard and a value bridge from current policy to recommended policy.

**What this document is.** An orchestration layer. It fixes five things:
- the *order* of the analysis;
- the *inputs and outputs* of every stage;
- the *decision rules with thresholds* that convert numbers into verdicts;
- the *branches* that fire when a company breaks the standard template;
- the *consistency rules* that must hold across stages.

It does **not** restate the mechanics. Every stage names the concept files that own its detail, cited as `concepts/<area>/<slug>.md`.

**The spine.** Damodaran's first principle is that a business maximizes value through exactly three decisions. **Invest** in assets earning more than a risk-adjusted hurdle rate. **Finance** with the right mix and the right kind of debt. **Return** the cash that cannot clear the hurdle rate. Every stage below serves one of those three, and Stage 11 prices the gap between what the firm does and what it should do.
Base concept: `concepts/governance-objective/first-principles-of-corporate-finance.md`, `concepts/project-returns/investment-analysis-first-principles.md`.

**Structure.** 13 sequential stages (S0–S12) and 7 conditional branches (B1–B7). Branches are selected at S1/S2/S3 and *replace or constrain* named stages; they never run alongside the machinery they displace.

---

## Stage dependency graph

```
S0 Mandate & scoping
   |
S1 Governance & objective  -----> objective (stock price / stockholder wealth / firm value)
   |                              agency-cost prior, constraint set, archetype
S2 Stockholder & marginal investor --> risk-measure decision (market beta | total beta | alt)
   |
S3 Accounting cleanup & base-year normalization   [gate for everything numeric]
   |        \
   |         \--> B1 financial firm | B5 cyclical | B6 money-loser  (replace/constrain S3,S5,S7,S11)
   |
S4 Risk & hurdle rates ------------------------------+--------------------+
   |   (cost of equity, cost of debt, WACC,           |                    |
   |    divisional rates, past-performance diagnostics)|                   |
   |                                                   v                   v
S5 Returns on existing investments (ROE/ROC/EVA)   S6 Returns on new projects (NPV/IRR)
   |                                                   |
   +--------------------+------------------------------+
                        |
S7 Capital structure: current vs optimal (the full WACC schedule)
   |
S8 Moving to the optimal (speed, method, recapitalization value, buyback price)
   |
S9 Debt design (the right kind of debt)  <--- feeds debt capacity back into S7
   |
S10 Dividend policy (FCFE vs cash returned, matrix, peers)
   |
S11 Tying to valuation (status quo DCF vs restructured DCF; value of control)
   |
S12 Synthesis, scorecard, cross-stage validation
```

**Hard ordering rules.**
- S5 cannot be judged before S4 (returns need hurdle rates).
- S7's schedule needs S3's lease-adjusted EBIT and S4's unlevered beta.
- S9's target duration/currency feeds back into S7's debt capacity; run S7 → S9 → re-check S7 once, no more.
- S10's recommendation needs S5's return spread (the trust axis) and S7's debt ratio (the FCFE debt assumption).
- S11's growth-phase WACC must be the *recommended* structure from S7/S8, and its growth must be S5's reinvestment × ROC.
Owner concept: `concepts/deliverables-worked-examples/corporate-finance-project-blueprint.md`.

---

# S0 — Mandate and scoping

**Purpose.** Fix the invariants that every later stage inherits. Getting these wrong invalidates everything downstream silently.

**Inputs.** User request; company identity; filings; market data.

**Procedure.**
1. Fix **currency** of analysis and **nominal vs real** basis. Default: the currency in which most cash flows arise, nominal.
2. Fix the **valuation/analysis date**. Every lookup table (spreads, ERP, country premiums, tax rates) must share this vintage.
3. Fix **unit conventions** (millions vs thousands; per-share vs aggregate) and record them.
4. Fix the **gross-debt vs net-debt convention**. Default: gross debt throughout, with cash added back at the equity bridge.
5. Screen eligibility. Standard machinery is invalid for: financial-service firms (→ B1), money-losers (→ B6), captive finance arms, REITs. Flag rather than exclude, then route.
6. Fix the **fiscal-year basis** for trailing-twelve-month updates.

**Outputs.** `mandate`: {currency, nominal|real, date, units, debt_convention, fiscal_basis, eligibility_flags}.

**Decision rules.**
- If equity is not publicly traded → set `traded=false` (feeds S1's objective matrix and S2's risk measure).
- If reported financials are older than 12 months → require a TTM update before S3 can pass.

**Validation.** V-01, V-02 (see §Validation).

**Concepts.** `concepts/deliverables-worked-examples/project-company-selection.md`, `concepts/cost-of-equity/cost-of-equity-assembly.md` (the three consistency dimensions), `concepts/cost-of-debt-capital/net-debt-vs-gross-debt.md`.

---

# S1 — Governance and the objective function

**Purpose.** Decide *what number the analysis is trying to maximize*, and how much of any recommendation management will actually act on. This is Part I of the deliverable and it gates the credibility of everything after it. A board with a staggered term, takeover defenses and no majority-vote standard can ignore an optimal-debt-ratio recommendation indefinitely.

**Inputs.** Proxy statement (DEF 14A), charter and bylaws, beneficial-ownership table, 13D/13F filings, debt indentures, annual meeting results, restatement/SEC-action history, trading and coverage statistics, vendor governance score (ISS QuickScore), news.

**Procedure — the four-link audit, run in order.**

**S1.1 Ownership and control.** Compute economic stake, voting stake (share count × votes per share ÷ total votes), and the **control wedge** = voting % − economic %. Sum affiliated entities for group control; trace pyramids to a look-through economic interest. Record golden shares, dual-class ratios, VIE/shell structures, and board nomination rights.
→ `concepts/governance-objective/ownership-and-control-structure-analysis.md`

**S1.2 Board and manager-stockholder conflict (Link I).** Run the three **CalPERS tests**: (1) majority outside directors, (2) chair independent of the CEO, (3) audit and compensation committees entirely outsiders. Then go past labels: business/consulting/charitable ties, board interlocks, director stake value versus director fee, bought-versus-granted shares. Board size against the 9–11 benchmark. Nominating committee versus CEO recommendation. Withhold-vote and say-on-pay dissent percentages. Institutional voting record (mainstream families historically support management ~92% of the time — institutional ownership is **not** monitoring).
→ `concepts/governance-objective/board-independence-assessment.md`, `concepts/governance-objective/manager-stockholder-agency-conflict.md`

**S1.3 Entrenchment and the acquisition record.** Inventory anti-takeover provisions and sort by whether stockholder approval was required (greenmail / golden parachutes / poison pills = no approval; shark repellents = approval). Compute greenmail transfers and parachute multiples. For each material acquisition: premium in $ and %, acquirer announcement CAR × market cap, recovery ratio on any later divestiture.
→ `concepts/governance-objective/managerial-entrenchment-and-takeover-defenses.md`, `concepts/governance-objective/value-destroying-acquisitions.md`

**S1.4 Lender protection (Link II).** Inventory covenants by category (investment / financing / dividend policy). Check for puttable bonds and ratings-sensitive notes. Screen for live expropriation channels: payout surges unmatched by operating cash flow, risk shifting into a materially riskier business, claim dilution via new debt on the same assets.
→ `concepts/governance-objective/stockholder-bondholder-conflict.md`

**S1.5 Information and market quality (Link III).** Restatements, late filings, auditor changes, material weaknesses; bad-news timing (Friday-afternoon concentration versus base rate); GAAP-vs-adjusted earnings gap; float, volume, bid-ask spread, analyst coverage, options depth.
→ `concepts/governance-objective/firms-and-financial-markets.md`

**S1.6 Social costs (Link IV).** List material externalities. Bucket A = already priced/regulated → model directly in cash flows. Bucket B = not priced → do **not** invent a social-cost number; model the societal counter-response as regulation risk, revenue risk, or a narrower investor base.
→ `concepts/governance-objective/firms-and-society-social-costs.md`

**S1.7 Counter-forces.** Score each of the four counter-forces present / weak / absent: activists and the market for corporate control; covenants and new bond types; analyst-and-options-market scrutiny; regulation plus customer/investor backlash. Run the **hostile-takeover target screen**: ROE ≈5 percentage points below peer group, 2-year relative stock underperformance, managers hold little or no stock. All three hit and no entrenchment blocker → expect discipline within 12–24 months.
→ `concepts/governance-objective/self-correction-and-counter-forces.md`

**S1.8 Archetype.** Classify: cutthroat / utopian / managerial / crony / confused / constrained corporatism.
→ `concepts/governance-objective/corporatism-archetypes.md`, `concepts/governance-objective/alternative-governance-systems.md`, `concepts/governance-objective/alternative-objective-functions.md`

**S1.9 Set the objective (the matrix).** Three booleans: T = publicly traded and liquid; E = markets reasonably efficient for this stock; B = lenders protected.

| T | E | B | Objective |
|---|---|---|---|
| yes | yes | yes | **Maximize stock price** |
| yes | no | yes | **Maximize stockholder wealth** |
| yes | no | no | **Maximize firm value** |
| no | — | yes | **Maximize stockholder wealth** |
| no | — | no | **Maximize firm value** |

Link I and Link IV failures do **not** change the objective. They change the *constraint set* and the *agency-cost prior*.
→ `concepts/governance-objective/modified-objective-function.md`, `concepts/governance-objective/classical-objective-function-assumptions.md`

**Outputs.** `governance`: {objective, four_link_scores, archetype, control_map (economic/voting/wedge/group), board_table_vs_peers, calpers_pass[3], entrenchment_inventory, covenant_inventory, counter_force_scores, power_score, agency_cost_prior, constraint_set}.

**Decision rules and thresholds.**
- CalPERS: >50% outside directors passes T1; chair ≠ CEO and not an employee passes T2; one insider on audit or comp fails T3.
- Withhold votes above **20–30%** is a serious revolt signal; change typically requires **two or three** revolt signals arriving together (protest resignations, hostile bid, mass withhold vote).
- Governance-index magnitude for context only: strongest-vs-weakest protection portfolio earned **+8.5%** annual excess return; each point toward fewer protections associated with **−8.9%** market value (1999 cross-section). Use as a magnitude prior, never as a firm-specific discount.
- Board composition is a **weak** predictor of value; investor-protection provisions are the stronger signal. Do not build a valuation adjustment off composition alone.
- Long CEO tenure + early success + re-combined chair/CEO role + heir-apparent departures = drift back toward board capture; re-date the audit.
→ `concepts/governance-objective/governance-legislation-and-payoff.md`, `concepts/governance-objective/disney-governance-case-study.md`
- Cross-holding/group structures: reported financials get a confidence discount; ask explicitly whether the group *supports* or *extracts from* the listed entity.

**Validation.** V-03.

**Deliverable format.** `concepts/deliverables-worked-examples/governance-analysis-deliverable.md` — board/executive table against peer averages, ISS QuickScore with sub-scores, red-flag checklist, compensation risk-incentive read, social-responsibility assessment, single integer Power score.

---

# S2 — Stockholder analysis and the marginal investor

**Purpose.** Decide whose risk is priced. This single call determines whether CAPM with a market beta is legitimate, and therefore the entire hurdle-rate stack.

**Inputs.** Insider/individual/institutional ownership breakdown, float, 13F filings, trading volume, blockholder identity, holder type (index fund vs activist vs strategic vs family partnership).

**Procedure.**
1. Compute institutional % of shares outstanding, institutional % of **float**, and insider % of shares.
2. Classify each large holder on three axes: size, active/passive, short/long term.
3. Identify the marginal investor — the one most likely to **trade next**, not the largest holder.

| Institutional | Insider | Marginal investor | Risk measure |
|---|---|---|---|
| High | Low | Diversified institution | Market beta (CAPM) |
| High | High | Institution, with insider influence | Market beta |
| Low | High (founder/manager) | Ambiguous; insiders only if they trade | Judgment |
| Low | High (wealthy individual) | Fairly diversified individual | Market beta |
| Low | Low | Small, restricted-diversification individual | Total risk |

4. Record the insider stake as an input to S7 (debt's disciplinary benefit is largest when insiders control and diversified institutions are absent).

**Outputs.** `stockholders`: {institutional_pct_shares, institutional_pct_float, insider_pct, holder_classification, marginal_investor, risk_measure ∈ {market_beta, total_beta, alternative}}.

**Decision rules.**
- Marginal investor diversified → market beta, CAPM applies.
- Marginal investor **not** diversified (private firm, closely held, undiversified owner) → **B2**: use total beta = market beta / √R² of the comparables.
- Marginal investor not diversified **and** no usable price history → alternative relative-risk measures (relative earnings volatility, accounting-ratio risk scores).
- Float percentages above 100% are a reporting artifact, not an error.
- A nominally "institutional" controlling partnership is an **undiversified** holder.

**Concepts.** `concepts/cost-of-equity/capm-cost-of-equity.md`, `concepts/cost-of-equity/total-beta.md`, `concepts/cost-of-equity/alternative-relative-risk-measures.md`, `concepts/deliverables-worked-examples/stockholder-analysis-marginal-investor.md`.

---

# S3 — Accounting cleanup and base-year normalization

**Purpose.** Produce the restated numbers every later stage consumes. This is a **gate**: no hurdle rate, no return measure, no capital-structure schedule and no valuation may run on unrestated statements.

**Inputs.** Income statement, balance sheet, cash flow statement, lease footnote, debt maturity schedule, segment footnote, tax footnote, share count and options data.

**Procedure.**
1. **Update.** Roll to trailing-twelve-month figures.
2. **Define debt.** Three-part test: contractually fixed payment, tax deductible, non-payment triggers default/loss of control. In: all interest-bearing liabilities (short and long term) **plus all leases**. Out: accounts payable, accruals, deferred taxes, minority interest. Convertibles split; preferred handled separately.
   → `concepts/cost-of-debt-capital/what-counts-as-debt.md`
3. **Capitalize operating leases.** Set n₆ = round(thereafter lump ÷ mean of years 1–5). Discount years 1–5 plus the n₆-year annuity at the **pre-tax cost of debt**. Then apply all four consequences:
   - add lease debt to debt;
   - restate EBIT (+ rent − straight-line depreciation on the lease asset);
   - restate interest (+ k_d × lease debt);
   - add lease debt to invested capital.
   → `concepts/cost-of-debt-capital/operating-leases-as-debt.md`
4. **Capitalize R&D** where intangible-intensive (B-overlay). Restate operating income, invested capital, and capex consistently.
   → `concepts/dcf-cashflows-growth/rnd-capitalization.md`
5. **Cleanse.** Strip one-time and non-recurring items; reconcile adjusted-vs-reported earnings; screen for aggressive accounting.
   → `concepts/dcf-cashflows-growth/reported-to-actual-earnings.md`
6. **Normalize if unrepresentative.** Cyclical/commodity trough or peak → **B5**. Negative earnings → **B6**.
7. **Tax rate.** Use the **marginal** statutory rate of the relevant jurisdiction (not the effective rate) for hurdle rates, project analysis and the capital-structure schedule. Record the effective rate separately for return measurement.
   → `concepts/cost-of-debt-capital/after-tax-cost-of-debt.md`, `concepts/dcf-cashflows-growth/tax-rate-and-nols.md`
8. **Market values.** Equity = shares × price (plus the equity half of any convertible). Debt = bond-conversion of book debt (coupon = interest expense, face = book debt, maturity = weighted-average from the footnote, default **3 years** if undisclosed, discounted at the current pre-tax cost of debt) **plus** capitalized leases **plus** the straight-debt half of convertibles. Preferred separately if ≥5% of firm value.
   → `concepts/cost-of-debt-capital/market-value-of-debt.md`, `concepts/cost-of-debt-capital/convertible-debt-decomposition.md`, `concepts/cost-of-debt-capital/preferred-stock-cost.md`
9. **Invested capital.** BV debt + BV equity − cash (+ lease debt, + R&D asset if capitalized, − goodwill where it distorts). Measure at the **start** of the period for return ratios.
10. **Segment decomposition** where multi-business → **B4**.

**Outputs.** `cleaned`: {EBIT_adj, EBITDA_adj, D&A_adj, interest_adj, NI, revenues (total and by segment/geography), capex, ΔWC, invested_capital (start), market_equity, market_debt, lease_debt, cash, preferred, marginal_tax_rate, effective_tax_rate, share_count, options}.

**Decision rules.**
- Lease capitalization discount rate depends on the rating, which depends on lease-adjusted coverage → **fixed-point iteration** (see S4.5). Seed at riskfree + a guessed spread; stop when the rating is stable; cap iterations and take the worse rating on a two-cycle.
- Never use book weights for the cost of capital. Book weights assign *more* weight to debt and therefore *lower* the computed WACC — anti-conservative.
  → `concepts/cost-of-debt-capital/market-value-weights.md`
- Produce the capital table **twice**: on market values (for S4/S7/S11) and on net **book** values (for S5's return comparison). Comparing a market-value cost of equity to a book-value ROE can flip the sign of a spread.

**Validation.** V-04, V-05, V-06.

---

# S4 — Risk and hurdle rates

**Purpose.** Produce the firm-level and divisional cost of equity, cost of debt and cost of capital that every return test and every valuation discounts at. Part III of the deliverable.

## S4.1 Fix currency and basis
Inherit from S0. Everything below must match.
→ `concepts/cost-of-equity/cost-of-equity-assembly.md`

## S4.2 Riskfree rate
- Default-free sovereign in the analysis currency, **10-year** maturity. Nominal cash flows → nominal bond; real → inflation-indexed bond.
- Multi-issuer currency (Euro): take the **minimum** 10-year rate among issuers (Germany), never an average and never the home sovereign.
- Non-default-free sovereign: riskfree = local 10-year government bond rate **−** sovereign default spread. Estimate the spread three ways (hard-currency sovereign bond spread; sovereign CDS net of a mature-market CDS; ratings-table lookup on the **local-currency** rating) and report the range; pick one and use it consistently.
- No trustworthy local bond: build up (expected inflation + expected real rate), or scale the US$ riskfree by the inflation ratio, or switch the whole valuation to a currency that has one.
- **Do not normalize** a low or negative rate in isolation. Intrinsic riskfree = expected inflation + expected real growth. If you normalize the rate, normalize growth, inflation and the ERP together and say so.
→ `concepts/cost-of-equity/riskfree-rate-fundamentals.md`, `concepts/cost-of-equity/currency-riskfree-rate.md`, `concepts/cost-of-equity/riskfree-rate-normalization.md`

## S4.3 Equity risk premium
1. Mature-market premium: the **implied** ERP for the S&P 500 at the analysis date (course default 4.72% on 1/1/2021). Historical premium only if you believe premiums revert and your horizon realizes them — then use the **geometric, stocks-over-T.Bonds, longest-window** figure, matched to a T.Bond riskfree rate.
2. Country risk premium: **CRP = sovereign default spread × relative equity market volatility** (production multiplier 1.10 in Jan 2021, 1.18 in Jan 2020). Aaa/AAA sovereign → CRP = 0. Unrated → PRS composite score mapping.
3. **Attach by operations, not by passport.** Company ERP = Σ(exposure weight × country/region ERP). Weight by revenues normally; by **production** for natural-resource firms; by assets for asset-heavy manufacturing.
4. Attachment mechanism — choose one and only one: additive (constant exposure), through beta, or via lambda λ (λ = firm domestic revenue share ÷ average local firm's domestic revenue share, or the slope of firm returns on sovereign-bond returns).
→ `concepts/cost-of-equity/equity-risk-premium-basics.md`, `concepts/cost-of-equity/implied-equity-risk-premium.md`, `concepts/cost-of-equity/historical-equity-risk-premium.md`, `concepts/cost-of-equity/choosing-an-equity-risk-premium.md`, `concepts/cost-of-equity/country-risk-premium.md`, `concepts/cost-of-equity/operation-weighted-erp.md`, `concepts/cost-of-equity/lambda-country-risk-exposure.md`

**Threshold checks.** ERP must be positive; ERP ÷ (Baa − T.Bond spread) should sit near the 1960–2020 median of **~2.0**; riskfree + ERP must be a plausible expected return on stocks.

## S4.4 Beta
**Bottom-up is the production method.**
1. Identify the businesses (economics, not filer labels).
2. Per business: **median** (not mean) regression beta of publicly traded comparables; unlever at the comparables' median D/E and tax rate; cash-correct: business β_u = company β_u ÷ (1 − median cash/firm value).
3. Value-weight across businesses. Business value = segment revenues × peer EV/Sales.
4. Relever at the firm's own **market** D/E with its marginal tax rate: β_L = β_u × (1 + (1−t)·D/E).
5. Report standard error = average comparable SE ÷ √n.
6. Regression beta is a **diagnostic only** (it is levered at the window's *average* D/E and reflects the *past* business mix). Extract Jensen's alpha from it (see S4.7).
7. Sanity-check against the determinants: product discretionary-ness, operating leverage (avg %ΔEBIT ÷ avg %ΔRevenues over a long window), financial leverage. The leverage effect is strongly convex.
→ `concepts/cost-of-equity/bottom-up-beta.md`, `concepts/cost-of-equity/levering-and-unlevering-beta.md`, `concepts/cost-of-equity/beta-determinants.md`, `concepts/cost-of-equity/regression-beta.md`, `concepts/cost-of-equity/non-traded-asset-betas.md`

**Branch hooks.** Undiversified owner → **B2** (total beta). Bank/insurer → **B1** (do not unlever; use median **levered** comparable betas weighted by net revenues).

**Cost of equity** = Riskfree + β × ERP (with the chosen country-risk attachment).

## S4.5 Cost of debt — the four-route decision tree
1. Liquid long-term **straight** bond outstanding → its yield to maturity. Stop.
2. Rated by a global agency → take the **median** rating across instruments; look the spread up in a spread table **as of the analysis date**; pre-tax k_d = riskfree + spread.
3. Unrated, recent long-term bank borrowing → that loan rate (recency matters).
4. Otherwise → **synthetic rating**: interest coverage = lease-adjusted EBIT ÷ lease-adjusted interest → rating → spread. Choose the table by firm class: large manufacturing (market cap > ~$5bn) vs **smaller/riskier** (which demands higher coverage for the same rating) vs financial (long-term interest only — and B1 says do not do this for banks at all).
   - Edge cases: interest = 0 with positive EBIT → top bucket; negative EBIT → bottom bucket (D).
   - Emerging market with far higher local rates → divide coverage by (local long rate ÷ US long rate) before the lookup.
5. **Country risk in the cost of debt.** Global-agency rating already embeds it → add only the company spread. **Local-scale** rating (e.g. CRISIL) measures company risk against domestic peers only → add the sovereign default spread separately, scaled by λ (the fraction of country risk the firm bears; a global exporter bears less than 1).
6. **Subsidized debt:** use the **fair** rate in the WACC and value the subsidy separately. Never let a subsidized rate set the hurdle rate for new projects.
7. After-tax k_d = pre-tax k_d × (1 − marginal tax rate). The tax shield lives in the discount rate and **nowhere else**.
8. Reconcile synthetic against actual and explain the gap (extra agency information, sector convention, normalized earnings, country-risk drag, uncapitalized off-balance-sheet obligations). Default to the **actual** rating when one exists and is current.
→ `concepts/cost-of-debt-capital/cost-of-debt-estimation-routes.md`, `concepts/cost-of-debt-capital/interest-coverage-ratio.md`, `concepts/cost-of-debt-capital/synthetic-rating.md`, `concepts/cost-of-debt-capital/synthetic-vs-actual-rating.md`, `concepts/cost-of-debt-capital/default-spreads-over-time.md`, `concepts/cost-of-debt-capital/country-risk-in-cost-of-debt.md`, `concepts/cost-of-debt-capital/subsidized-debt.md`

## S4.6 Assemble the cost of capital
`WACC = k_e·E/(D+E+PS) + k_d(1−t)·D/(D+E+PS) + k_ps·PS/(D+E+PS)`, on **market-value** weights, in one currency, at one date.

Preferred stock: cost = dividend ÷ market price, with **no** tax shield. Fold it into debt only when it is under 5% of firm value.

**Execution order.** The pipeline is not arbitrary — leases must be capitalized before the rating can be computed, and the rating sets the rate that discounts the leases.

```
market equity
  → capitalize leases at a seeded k_d
  → lease-adjusted EBIT and interest
  → coverage → synthetic rating → spread → k_d
  → ITERATE TO FIXED POINT
  → market value of straight debt → convertible split → MV debt, MV preferred
  → unlevered beta → relever at market D/E
  → ERP → cost of equity
  → after-tax k_d → weights → WACC
```
→ `concepts/cost-of-debt-capital/cost-of-capital-assembly.md`, `concepts/cost-of-debt-capital/wacc-calculator-workflow.md`

## S4.7 Past-performance diagnostics
Run the market-model regression and report all three outputs:
- **Regression beta** (with standard error and 67%/95% ranges) — diagnostic, not the hurdle-rate beta.
- **Jensen's alpha** = intercept − R_f(1 − β), with R_f the **average** riskfree rate *over the regression window*, expressed per return interval. Annualize by compounding. The benchmark is R_f(1−β), never zero.
- **R²** — share of risk that is market risk; 1 − R² is firm-specific.
Read alpha with life-cycle context (a huge positive alpha at a young firm is a growth-cycle artifact, not skill) and connect a persistent negative alpha to corporate actions.
→ `concepts/cost-of-equity/jensen-alpha.md`, `concepts/deliverables-worked-examples/regression-performance-diagnostics.md`

## S4.8 Divisional and project hurdle rates
For each business:
1. Unlevered beta from that business's comparables.
2. Allocate firm debt across divisions on a stated key. Identifiable assets is the default.
3. Divisional D/E = allocated debt ÷ (division value − allocated debt).
4. Relever, then compute the divisional cost of equity.
5. Divisional WACC uses the company-wide after-tax k_d and the division's own debt ratio.
6. Add a country risk premium for divisions or projects in risky geographies.
**The matching rule (mandatory before any comparison):** returns to equity → cost of equity; returns to the whole firm → cost of capital; at the **business's** risk level, in the **cash flows' currency**.
→ `concepts/cost-of-debt-capital/divisional-cost-of-capital.md`, `concepts/cost-of-debt-capital/hurdle-rate-choice.md`, `concepts/project-returns/project-hurdle-rate-selection.md`

## S4.9 Currency conversion
`Rate_local = (1 + Rate_base) × (1 + expected inflation_local) ÷ (1 + expected inflation_base) − 1`. Applies to k_e, k_d and WACC alike. Cross-check by rebuilding directly off the local riskfree rate; agreement within ~20bp is the test. Convert the **growth rate** with the rate. Currency is a unit of measurement, not a risk factor.
→ `concepts/cost-of-debt-capital/currency-conversion-of-discount-rates.md`, `concepts/project-returns/currency-and-inflation-consistency.md`

**Outputs.** `hurdle_rates`: {currency, riskfree (with derivation), ERP build-up (mature + CRP + weights + attachment), unlevered_beta (by business, with weights), levered_beta, cost_of_equity, rating (actual|synthetic + route), default_spread + vintage, pre_tax_kd, marginal_tax_rate, after_tax_kd, market_weights, WACC, divisional_table[], book_net_version, regression_diagnostics {beta, SE, R², jensen_alpha}}.

**Validation.** V-07 through V-12.

**Deliverable format.** `concepts/deliverables-worked-examples/cost-of-capital-buildup-deliverable.md` — the build-up table produced twice (market values and net book values).

---

# S5 — Returns on existing investments

**Purpose.** Answer whether the firm has been creating or destroying value with the capital it already has. Part IV. Its output is one of the two axes of the dividend matrix (S10) and the strongest evidence for or against the growth story in S11.

**Inputs.** S3 cleaned financials (restated EBIT, invested capital measured at the **start** of the period, net income, book equity), S4 hurdle rates on the **book/net** basis.

**Procedure.**
1. `ROC = EBIT×(1−t) ÷ (BV debt + BV equity − cash)`, prior-year capital, plus lease debt and the R&D asset if capitalized.
2. `ROE = Net income ÷ BV equity`.
3. Spreads: `ROC − WACC` and `ROE − cost of equity`, on **matching bases** (book returns against the book/net hurdle rates).
4. `EVA = (ROC − WACC) × invested capital` — the dollar version.
5. Benchmark **twice**: against zero, and against the industry-average firm's EVA. A distressed firm can have a terrible spread and a less-negative EVA than its sector.
6. Ask the forward question: will future projects look like past projects, and why?
7. Multi-year: run the same measures over 3–5 years to strip one-year noise.

**Outputs.** `returns`: {ROC, ROE, WACC_book_net, COE_book_net, capital_spread, equity_spread, EVA, industry_EVA_benchmark, multiyear_series, verdict ∈ {creates_value, neutral, destroys_value}}.

**Decision rules and thresholds.**
- `ROC > WACC` ⟺ `EVA > 0` ⟺ reinvestment creates value → growth is a value driver in S11 and the "good projects" branch fires in S8/S10.
- `ROC ≈ WACC` (within ~2 points) → growth is value-neutral; focus S11's levers on existing-asset cash flows and the cost of capital.
- `ROC < WACC` → growth **destroys** value. The value-enhancing actions are *less* reinvestment, divestiture of sub-WACC assets, and returning capital. Never model growth as a value driver here.
- Base rate for calibration. Globally, ~**52%** of non-financial firms earn less than their cost of capital. About 15% sit within a couple of points of it, and ~33% clear it. Assume the firm is in the majority until the data says otherwise.
- Growth mode ranking, by value created per incremental $1m:

  | Growth mode | Value created |
  |---|---|
  | New-product market development | $1.75–2.00 |
  | Expanding an existing market | $0.30–0.75 |
  | Holding or growing share in a growing market | $0.10–0.50 |
  | Competing for share in a stable market | −$0.25 to −$0.40 |
  | Acquisition | −$0.50 to −$0.20 |

**Known distortions to check before acting on the number.** Trailing-twelve-month earnings abnormality; misclassified leases and R&D; write-offs shrinking the denominator; inflation-stale book values; depreciation-method choice; overhead allocation choice; the mechanical rise of book returns as assets depreciate; horizon truncation on long-lived assets.

**Concepts.** `concepts/project-returns/accounting-returns-roc-roe-eva.md`, `concepts/dcf-cashflows-growth/return-on-invested-capital.md`, `concepts/acquisitions-control-enhancement/growth-quality-and-excess-returns.md`, `concepts/deliverables-worked-examples/return-spread-and-eva-analysis.md`.

**EVA discipline (if the firm manages to EVA).** Firm value = capital invested + PV of *all future* EVA = the DCF. Audit any reported EVA increase for the three games — sacrificed future growth, higher risk (check whether WACC rose), and investments kept off the capital base — and test against *expected* EVA, not last year's.
→ `concepts/acquisitions-control-enhancement/eva-and-dcf-equivalence.md`, `concepts/acquisitions-control-enhancement/gaming-eva.md`

---

# S6 — Returns on new projects

**Purpose.** Test the marginal investment decision. Runs when the mandate includes a live project, an acquisition, or a capital-allocation review; otherwise S6 supplies the *method* the firm should be using and S5 supplies the *record*.

**Inputs.** Project definition and counterfactual, forecast revenues and costs, capex/depreciation schedule, working-capital ratio, project life, financing plan (if equity-side), S4 divisional/project hurdle rate.

## S6.1 Fix the perspective
Firm side (FCFF at the cost of capital) or equity side (cash flow to equity at the cost of equity). Never mix. Equity side requires a defined amortization schedule and is the natural route for financial-service firms and for projects with dedicated financing.
→ `concepts/project-returns/equity-side-project-analysis.md`

## S6.2 Build the numerator
1. Earnings: revenues, direct expenses, depreciation, allocated overhead. Tax at the **marginal** rate; negative operating income generates a credit at the same rate only if there is other income to shelter.
2. Earnings → cash flow: add back D&A in full; subtract capex (growth **and** maintenance — maintenance needs rise with project life); subtract ΔWC and recover working capital at the end.
3. **Never** deduct interest in firm-side cash flows.
→ `concepts/project-returns/earnings-vs-cash-flows.md`
4. **Strip non-incremental items.** Sunk costs out — including the depreciation tax shield on any capitalized sunk asset. Allocated overhead: charge only the **variable** share plus genuinely new overhead. Get the split from a regression of G&A on revenues (slope = variable rate; intercept = fixed pool). Reconcile the adjustment route and the direct route.
→ `concepts/project-returns/incremental-cash-flow-principle.md`
5. **Charge side costs.** Owned resources priced at their best alternative use: sale → after-tax proceeds = MV − t_cg×(MV − BV); rental → PV of after-tax rents; internal redeployment → replacement cost; genuinely no alternative now or later → zero. Excess capacity: ask when capacity runs out without the project, when with, and what happens then — charge either the PV of lost sales or the PV difference between building earlier and later. Cannibalization: charge only the share the firm would otherwise have kept (full for an exclusive product; partial in a fiercely competitive market).
→ `concepts/project-returns/opportunity-costs-and-side-costs.md`
6. **Credit side benefits.** Value each synergy explicitly, in the original analysis, at the **receiving** business's cost of capital, with an honest adoption lag. Report stand-alone NPV and synergy NPV **separately**.
→ `concepts/project-returns/project-synergies.md`
7. **Close the stream.** Short finite life → salvage = end-of-life book value of fixed assets + recovered working capital. Long/indefinite life → terminal value = steady-state CF_{n+1}/(r − g) with g ≤ inflation, and maintenance capex consistent with g (g = 0 → maintenance = depreciation; g = inflation → maintenance > depreciation). Capitalize the **steady-state** year, never a still-growing final forecast year.
→ `concepts/project-returns/terminal-value-and-project-life.md`, `concepts/project-returns/time-value-and-cash-flow-timing.md`

## S6.3 Run the tests
- `NPV = Σ CF_t/(1+r)^t`; accept if > 0. Report NPV as a dollar statement of value added.
- `IRR`: accept if > hurdle rate. Count sign changes first; more than one → multiple IRRs, fall back on NPV. Plot the NPV profile.
- Ranking rules: different scale → NPV; different timing at equal scale → the divergence is the reinvestment assumption, compute MIRR and decide with NPV; genuine capital rationing → profitability index; different lives → replication or equivalent annuities, never raw NPVs.
- Accounting cross-check: project ROC against the same risk-matched cost of capital.
→ `concepts/project-returns/npv-and-irr-mechanics.md`, `concepts/project-returns/npv-vs-irr-conflicts.md`, `concepts/project-returns/comparing-projects-different-lives.md`

## S6.4 Stress and options
Payback and discounted payback (supplementary only); one-at-a-time sensitivity over realistic ranges with **break-even levels** reported (the number a manager can monitor); Monte Carlo on the few drivers that matter, reporting mean, median, range and P(NPV<0). A downside probability is **not** by itself a rejection reason — the discount rate already charges for risk. Then add embedded options: delay (call; requires genuine exclusivity), expand (call; name the follow-on), abandon (put; requires a real exit value). Accept if `traditional NPV + option value > 0`, and say so explicitly when the option carries the decision.
→ `concepts/project-returns/uncertainty-payback-sensitivity-simulation.md`, `concepts/project-returns/project-options.md`

## S6.5 Acquisitions as projects
Same rules, one emphasis: discount at the **target's** risk and the **target's** debt capacity. Normalize the base year (restructuring add-backs, lease capitalization, one-off working-capital swings, unusual tax rates). Ceiling price = target stand-alone value + synergy value. Full deal machinery is **B7**.
→ `concepts/project-returns/acquisitions-as-projects.md`

## S6.6 Existing assets: the go-forward ladder
Post-mortem (compare actuals to original forecasts; symmetric errors = chance, one-directional = bias — diagnose only across many projects) and the forward test using **new** forecasts only:
`PV < 0` → liquidate; `PV < salvage value` → terminate; `PV < divestiture value` → divest; `PV > 0` and `PV > divestiture` → continue, and test any expansion as its own incremental project.
→ `concepts/project-returns/assessing-existing-investments.md`

**Outputs.** `investment`: {perspective, incremental_cash_flows[], hurdle_rate + derivation, NPV, IRR, MIRR/PI where relevant, ROC series, side_costs[], synergies[] (each with its own discount rate), terminal_treatment, sensitivity + break-evens, simulation summary, option_value (if any), verdict}.

**Validation.** V-13, V-14, V-15.

**Reference engine.** `concepts/project-returns/capital-budgeting-model.md`. Integrated worked case: `concepts/project-returns/netflix-fit-case.md`.

---

# S7 — Capital structure: current versus optimal

**Purpose.** Answer "how much debt". Parts V and VI. This is the most mechanically demanding stage and the one that produces the largest single value number in the playbook.

## S7.1 Current mix
Debt-to-capital on **market** values (and book, for contrast), including capitalized leases; net-debt versions alongside. Inventory each instrument on the debt-equity continuum: bank debt, bonds, leases, convertibles, preferred, equity. Record maturity profile, currency mix, fixed/floating split.
→ `concepts/capital-structure/debt-vs-equity-choices.md`

**Rule.** Reject "debt is cheaper than equity" as a value argument. The lower rate compensates for first claim plus a fixed payment; the risk moves to equity, it does not disappear.

## S7.2 Qualitative trade-off (do this BEFORE the schedule)
Score five forces and **predict** where the optimum should sit. Doing this after the spreadsheet destroys its value.

| Force | Direction | Measurable proxy |
|---|---|---|
| Tax benefit | Higher marginal tax rate → more debt | Marginal tax rate; **EBITDA/EV** vs industry average |
| Discipline | Wider manager-owner separation → more debt | Institutional % vs industry average (from S2); insider % |
| Expected bankruptcy cost | More volatile earnings, larger indirect costs → less debt | sd of %ΔEBIT (not %ΔRevenue); credit rating; product durability/service dependence |
| Agency cost | Harder-to-monitor, intangible assets → less debt | Asset tangibility; covenant load |
| Flexibility | Less predictable future funding needs → less debt | Life-cycle stage; market access |

Also check: country-specific offsets (e.g. Brazil's deduction for interest on equity capital), pending acquisitions (raise earnings uncertainty → hold below the optimum), and rating-agency behavior (agencies penalize fast moves).
→ `concepts/capital-structure/debt-equity-tradeoff.md`, `concepts/capital-structure/tax-benefit-of-debt.md`, `concepts/capital-structure/financing-life-cycle.md`, `concepts/capital-structure/pecking-order.md`, `concepts/capital-structure/miller-modigliani.md`, `concepts/deliverables-worked-examples/qualitative-debt-tradeoff.md`

**MM as a diagnostic.** Whenever a financing action is claimed to create value, name which MM assumption it violates (taxes / bankruptcy / manager-stockholder agency / lender agency / known future funding needs). If none is violated, the claimed gain is a transfer.

## S7.3 The cost-of-capital schedule (the core procedure)
**Held constant across the entire schedule:** EBITDA, depreciation, EBIT (lease-adjusted), capex, riskfree rate, ERP, unlevered beta, marginal tax rate, and **total capital** = current market equity + current market debt (incl. leases). Only the *mix* changes.

For each debt ratio `d` ∈ {0%, 10%, …, 90%} (stop at 90%; D/E is undefined at 100%):

1. `D/E = d/(1−d)`; `$Debt = d × total capital`.
2. **Solve the rating fixed point.** Seed a rate; `interest = rate × $Debt`; `coverage = EBIT ÷ interest`; look up rating (last row whose lower bound ≤ coverage) and spread; `rate = riskfree + spread (+ country default spread)`; repeat until the rating implied equals the rating used. On a two-cycle between adjacent ratings, take the worse one.
   - Refinancing assumption: default is that **all** debt reprices at the new rate. The alternative (only incremental debt reprices) must be stated.
3. **Cap the tax benefit.** `t_EBIT = t` if interest ≤ EBIT, else `t × EBIT/interest`. `t_cap = t` if interest ≤ 0.30 × M, else `t × (0.30×M)/interest`, where M = EBITDA (through 2022) or EBIT (after), where the statute applies. **`t_used = MIN(t_EBIT, t_cap)`**.
4. **Relever beta with `t_used`**, not the headline rate: `β_L = β_u × (1 + (1 − t_used)·D/E)`. This is why betas rise faster at high leverage than a constant-t calculation implies.
5. `k_e = riskfree + β_L × ERP`; `after-tax k_d = pre-tax k_d × (1 − t_used)`.
6. `WACC(d) = k_e(1−d) + after-tax k_d · d`.
7. Firm value at `d`. Incremental form: `V(d) = EV_current × [1 + (WACC_current − WACC_d)/(WACC_d − g)]` with `g = min(implied growth, riskfree rate)`. Implied growth from today's price: `g = (EV × WACC_current − FCFF)/(EV + FCFF)`.

**Optimum.** With cash flows held fixed, `d* = argmin WACC`. With indirect bankruptcy costs on (S7.4), `d* = argmax firm value` — once operating income varies with `d`, WACC is no longer a valid objective.

**Excess debt capacity** = optimal $debt − current debt.
→ `concepts/capital-structure/cost-of-capital-approach.md`, `concepts/capital-structure/levered-beta-schedule.md`, `concepts/capital-structure/synthetic-rating-and-cost-of-debt.md`, `concepts/deliverables-worked-examples/optimal-debt-ratio-wacc-schedule.md`

## S7.4 Alternate lenses (run at least one)
- **Enhanced cost of capital** — indirect bankruptcy costs as rating-keyed EBITDA haircuts (Low/Medium/High severity by how much the business depends on customer confidence in survival: durable goods and intangible/people businesses take High, immediate-consumption businesses take Low). Adds a second fixed point (haircut ↔ rating). Gross up current EBITDA first if the firm is already distress-impaired. Select on **maximum firm value**. Often the optimum barely moves; what changes is the steepness of the cliff past it — that is the finding.
- **APV** — `V = V_unlevered + tax benefits(d) − expected bankruptcy cost(d)`, with default probabilities from an Altman-style rating table and bankruptcy costs at ~25% of value (direct costs empirically 5–10%; indirect are a judgment). Values debt **levels**, not ratios. Beware non-monotonic probability columns in published tables.
- **Relative and regression** — industry average debt ratio (market and net, matched basis) and a cross-sectional regression prediction. Treat as a description of *typical* behavior, never as an optimum (market-wide R² can be as low as 8%).
- **Life-cycle** — does the answer fit the stage?
→ `concepts/capital-structure/enhanced-cost-of-capital-approach.md`, `concepts/capital-structure/apv-approach.md`, `concepts/capital-structure/relative-and-regression-analysis.md`, `concepts/capital-structure/pathways-to-the-optimal-debt-ratio.md`

## S7.5 Constraints and stress (pick ONE protection, not both)
- **Safety-buffer route.** Compute sd of annual %ΔEBIT and the worst historical recession decline. Re-run the full schedule at EBIT haircuts of 10%, 20%, … 60% (or at EBIT − 3sd) and record where the optimum first shifts down. That shift point is the buffer.
- **Rating-constraint route.** Ask management for a minimum acceptable rating; find the highest debt ratio consistent with it; **price the constraint** as firm value at the unconstrained optimum minus firm value at the constrained ratio.
Do **not** apply both — they protect against the same risk and leave the firm arbitrarily under-levered. Separate the three motives for a rating constraint before accepting it: downside protection, genuine operating feedback (which belongs in S7.4's enhanced approach), and management ego.
**Use of proceeds does not change the optimum** as long as the business mix and tax rate are unchanged.
→ `concepts/capital-structure/downside-risk-and-rating-constraints.md`

## S7.6 Explain the answer
Attribute the optimum to the four drivers: marginal tax rate (zero tax rate → optimum 0%; the relationship plateaus once the coverage-driven rating binds), **EBITDA/EV** (pre-tax cash flow return — debt capacity per dollar of value), operating risk (enters twice, through β_u and through the coverage-to-rating map), and the macro price of equity risk relative to debt risk (`ERP ÷ Baa spread`, historical median ~**1.96**).
→ `concepts/capital-structure/determinants-of-optimal-debt-ratio.md`

## S7.7 Firm-type overrides
- Volatile/commodity earnings → run the schedule twice (last-twelve-month EBIT **and** normalized EBIT) and say which you'd act on given where the cycle sits. The swing can be 20 percentage points. (**B5**)
- Young growth firm (low EBITDA/EV) → expect ratings to collapse within one or two 10% steps and the optimum to land at 0–10%. Do not force a peer-like target. (**B6**)
- Private firm → estimate equity from comparables (net income × peer PE); use **total betas** throughout the schedule. (**B2**)
- Group/affiliated company → compare standalone optimum to actual and ask whether affiliate support is being priced by lenders.
- Emerging market → add the country default spread at every rating; use a country-risk-adjusted ERP. (**B3**)
- Bank/insurer → **B1**, the schedule does not apply.
→ `concepts/capital-structure/optimal-debt-ratio-by-firm-type.md`

**Outputs.** `capital_structure`: {current_ratio (market, book, net), qualitative_scores + predicted_direction, schedule[10 rows: d, D/E, $debt, interest, coverage, rating, spread, pre_tax_kd, t_used, β_L, k_e, after_tax_kd, WACC, firm_value], optimum_standard, optimum_enhanced, optimum_APV, industry_benchmark, regression_prediction, stress_table, rating_constraint_cost, excess_debt_capacity, recommended_ratio (constrained) + rationale}.

**Decision rules.**
- Report a **range and a direction** (under-levered / at the mix / over-levered), not a single number with false precision. The grid is 10% steps and the inputs are noisy.
- Where intrinsic methods agree and comparables disagree, prefer the intrinsic answer and **explain** the gap (peers are often collectively conservative). Do not average them.
- The mechanical argmin is not the recommendation. The recommendation is the constrained answer, stated separately.

**Validation.** V-16, V-17, V-18.

---

# S8 — Moving to the optimal

**Purpose.** Convert the S7 gap into an executable plan, and price it. Part VII (first half).

**Inputs.** S7 current and recommended ratios; S5 return spreads; S1 takeover-vulnerability read; S3 FCFF and cash; share count and price.

## S8.1 The decision tree
**Over-levered (actual > optimal):**
- Bankruptcy threat? **Yes** → move fast: equity-for-debt swaps; sell assets to repay debt; renegotiate with lenders.
- **No** → good projects (ROE > k_e **and** ROC > WACC)? **Yes** → take them, funded with **equity or retained earnings**. **No** → repay debt from retained earnings; reduce/eliminate dividends; issue equity to retire debt.

**Under-levered (actual < optimal):**
- Takeover target? **Yes** → move fast: debt-for-equity swaps; borrow and buy back shares.
- **No** → good projects? **Yes** → take them, funded with **debt**. **No** → return cash: dividends if stockholders prefer them, buybacks otherwise.

Both tests (ROE and ROC) should point the same way. Base rate check: roughly a third of global firms earn at least 2 points below their cost of capital, so "we have good projects" needs evidence.
→ `concepts/capital-structure/moving-to-the-optimal.md`

## S8.2 Price the move
1. `FCFF = EBIT(1−t) + Depreciation − Capex − ΔWC`.
2. Implied growth from today's price: `g = (EV × WACC_old − FCFF)/(EV + FCFF)`.
3. **Full revaluation:** `V_new = FCFF(1+g)/(WACC_new − g)`; gain = V_new − EV.
4. **Incremental (conservative):** annual saving = `EV × (WACC_old − WACC_new)`; capitalize at `(WACC_new − riskfree)`.
   Report **both**. They can differ by a factor of two, and the difference is entirely the growth rate assumed.
5. **Rational buyback price** = current price + gain per share. It is a fixed point: buying back at that price must reproduce a post-buyback value per share equal to it. Buying back **below** it transfers value from sellers to remaining holders; the pre-announcement price is not the right assumption if the market believes the recap creates value.
6. General buyback arithmetic at any price P: `shares_after = shares_before − ΔDebt/P`; `equity_after = EV_optimal + cash − debt_optimal`; `value/share = equity_after ÷ shares_after`.
→ `concepts/capital-structure/recapitalization-and-buyback-price.md`, `concepts/deliverables-worked-examples/recapitalization-value-and-stress-test.md`

## S8.3 Speed
Move **immediately** when there is a bankruptcy or takeover threat and no offsetting constraint. Move **gradually** when EBIT is volatile, a large acquisition is in flight, the firm already sits above its regression-predicted ratio, or rating agencies would penalize the pace. Plan the gradual path against a **moving** firm value: equity appreciates at roughly (cost of equity − dividend yield), so a fixed dollar buyback program moves the ratio less than expected.

**Outputs.** `transition`: {verdict ∈ {right_mix, under_levered, over_levered}, urgency ∈ {immediate, gradual}, method ∈ {alter_mix, finance_new_projects}, instruments[], value_gain_full, value_gain_incremental, gain_per_share, rational_buyback_price, projected_path[]}.

**Answers management always asks (include them):** why do this, what if something goes wrong (point at S7.5's stress table), and what if we do not want to buy back stock (point at the project-financing route).

---

# S9 — Debt design: the right kind of debt

**Purpose.** Match debt cash flows to asset cash flows. Matching lowers default risk at any given debt level, which raises debt capacity, which feeds back into S7. Part VII (second half).

**Inputs.** Segment/project cash-flow characteristics; project duration; firm-level macro history (operating income, market cap, debt); sector macro coefficients; existing debt profile; tax code; rating-agency and analyst constraints; covenant history.

## S9.1 The six-stage pipeline
1. **Profile the asset cash flows** — duration, currency, inflation sensitivity, uncertainty, growth pattern, cyclicality. Three routes: intuitive (business-by-business reasoning), project cash flow (scenario analysis on a typical project), or historical (firm's own operating cash flow and value history).
2. **Define the debt characteristics** — asset duration → debt maturity; revenue currency → debt currency mix; inflation-linked or uncertain cash flows → more floating rate; low current cash flow with high expected growth → convertible rather than straight; specific exposures → linked features (commodity bonds, catastrophe notes).
3. **Overlay tax** — the matching is wasted if the instrument does not deliver the deduction. A large enough tax advantage can override matching.
4. **Keep analysts, agencies and regulators satisfied** — analysts watch EPS and comparables; agencies watch ratios and prefer equity; regulators watch book measures. Quasi-equity instruments (trust preferred) benefit most an **under-levered firm with a rating constraint** that moving to its optimum would breach.
5. **Soothe bondholder fears** — where cash flows are hard to observe or assets are intangible, agency costs are high: use convertibles, puttable bonds, or ratings-sensitive notes.
6. **Consider information asymmetry** — more uncertainty or a credibility problem → shorter-term debt.
Plus: **do not lock in a market mistake** — issuing long-dated debt while under-rated, or equity while under-priced, transfers wealth away from existing holders; use short-term or delayed structures until the mispricing corrects.
→ `concepts/capital-structure/debt-design-framework.md`

## S9.2 Quantify duration
Project duration = `Σ t·PV(CF_t) ÷ Σ PV(CF_t)`, terminal value included (it usually dominates). Bond duration for comparison. Note that **maturity exceeds duration** for a coupon instrument, so matching maturity to duration overshoots.
Project-specific financing is right when projects are few, large and independent; wrong for a portfolio of interdependent projects — then match at the firm level.
→ `concepts/capital-structure/project-duration-and-project-financing.md`

## S9.3 Macro sensitivity regressions (firm level, then bottom-up)
Run **four separate univariate** regressions on each of Δfirm value and Δoperating income against: Δ(10-yr T.Bond rate) [absolute change], %ΔReal GDP, Δ(inflation rate) [absolute change], %Δ(trade-weighted dollar).
- Interest-rate slope on firm value → asset duration (floored at zero) → target debt maturity.
- GDP slope → cyclicality → borrow less or tie payments to output.
- Currency slope → foreign-currency share of debt.
- Inflation slope on **operating income** → pricing power → floating-rate share.
**Threshold:** a slope with |t| < 2 must not drive a financing decision. When firm-level estimates are insignificant (common), switch to **bottom-up**: value-weight sector coefficients across the firm's businesses, exactly as with bottom-up betas.
→ `concepts/capital-structure/macro-sensitivity-regressions.md`

## S9.4 Gap table and closure
Tabulate existing debt on the same dimensions (weighted-average maturity, currency shares, fixed/floating split, convertible share) beside the recommendation. Close the gap with swaps on existing debt and by issuing new debt in the recommended form. Firm-level matching improves even when a specific new issue does not match a specific new asset.

**Outputs.** `debt_design`: {target_duration, currency_mix, fixed_floating_split, special_features, convertible_yes_no, regression_table (coefficients + t-stats, firm and bottom-up), existing_profile, gap_table, closure_instruments}.

**Feedback.** Improved matching raises debt capacity → re-check S7's optimum **once**.

**Deliverable format.** `concepts/deliverables-worked-examples/debt-design-deliverable.md`.

---

# S10 — Dividend policy

**Purpose.** Answer whether the firm returns the right amount of cash, in the right form. Parts VIII and IX.

**Inputs.** 5–10 years of: net income, depreciation, capex (**including acquisitions**), Δnon-cash working capital, net debt issued, dividends, buybacks (and equity issuance), book equity, stock returns, annual riskfree and market returns; S4 cost of equity and beta; S5 return spreads; S7 debt ratio; peer group; cash balance.

## S10.1 Frame it as a residual
Cash flow from operations → pay debt (interest and principal, net of new borrowing) → reinvest (capex and ΔWC) → **FCFE = potential dividends** → hold back a reasonable cash balance → pay out, split between dividends and buybacks by stockholder preference. Real policy departs from this because of **inertia** and **me-too-ism** — which is why the whole assessment toolkit exists.
→ `concepts/dividend-policy/dividend-decision-sequence.md`

## S10.2 Measure what was actually returned
`Cash returned = dividends + buybacks` ("augmented dividends"). Net buybacks against equity issuance where stock compensation is large. Compute payout ratio, dividend yield, **cash payout ratio**, buyback share, and total yield. Place the firm in its region and life-cycle stage.
**Hard rule:** any comparison, screen or regression run on dividends alone will mis-rank a US firm by a factor of two or more. Add buybacks on both sides.
→ `concepts/dividend-policy/cash-returned-dividends-and-buybacks.md`, `concepts/dividend-policy/dividend-payout-and-yield-measures.md`, `concepts/dividend-policy/dividend-empirical-facts.md`, `concepts/dividend-policy/dividend-life-cycle.md`

## S10.3 Measure capacity: FCFE, three variants
Over the chosen window (5 years default), per year and in aggregate:
- **Pre-debt FCFE** = NI − (Capex − Depreciation) − ΔWC
- **Actual-debt FCFE** = pre-debt FCFE + net debt issued
- **Target-debt-ratio FCFE** = NI − (1 − DR)·[(Capex − Depreciation) + ΔWC]

**Default to the target-debt-ratio variant** for the verdict when net debt cash flows are lumpy — a single heavy borrowing year makes actual-debt FCFE look artificially generous. Report all three; the disagreement is itself the finding, and it can move the firm from one column of the matrix to the other.
DR = the current market debt ratio, or the S7 target if you are deliberately moving the firm — state which.
→ `concepts/dividend-policy/fcfe-potential-dividends.md`

**Bank exception:** FCFE = net income − investment in regulatory capital (**B1**).
→ `concepts/dividend-policy/fcfe-for-banks.md`

## S10.4 Score trust
Two measures, both required:
- **Project quality:** average ROE − cost of equity, and ROC − WACC (from S5).
- **Stock performance:** Jensen's alpha = annual stock return − CAPM required return using that year's riskfree and market returns.
Verdict: both positive → high trust, the firm has earned the flexibility to hold cash. Both negative → low trust, support pressure to pay out. Mixed → weight the **project** measure more heavily (the market measure includes revaluation management did not create) and say which you relied on.
Cash accumulation identity: `cumulated cash_t = cumulated cash_{t−1} + FCFE_t − cash returned_t`. A persistent surplus at a low-trust firm builds the pile that attracts activists.
→ `concepts/dividend-policy/cash-trust-assessment.md`

## S10.5 The dividend matrix
| | **Poor projects** (ROE < k_e) | **Good projects** (ROE > k_e) |
|---|---|---|
| **Cash surplus** (returned < FCFE) | Heavy pressure to pay out more, as dividends or buybacks | **Maximum flexibility** |
| **Cash deficit** (returned > FCFE) | Cut the payout — but the real problem is **investment policy** | Reduce the payout so investments are funded internally |

Sequencing rule for the deficit column: with poor projects, **fix the investment policy first, then cut** — a cut alone leaves the value destruction untouched. State the FCFE variant used, because the quadrant can change with it.
→ `concepts/dividend-policy/dividend-matrix.md`

## S10.6 Cross-checks
- **Peer group.** Same sector, stated geography and size filter. Report both **average and median** (in sectors where most firms pay nothing, the median is zero and the average is a small-sample artifact). Sanity-check the group: if the group's own FCFE is negative, matching it is not a target worth hitting. Add buybacks and compute cash returned / FCFE per peer.
- **Market regression.** `PYT = 0.649 − 0.296·BETA − 0.800·EGR + 0.300·DCAP` (R² 19.6%); `YLD = 0.0324 − 0.0154·BETA − 0.038·EGR + 0.023·DCAP` (R² 25.8%), Jan-2014 US coefficients, **decimals not percentages**. Signs are the durable content: riskier → lower payout; higher growth → lower payout; more levered → higher payout. **Then check buybacks** — the regression is fitted on dividends only and will label a heavy repurchaser a cash hoarder.
Both are cross-checks. Where they disagree with the FCFE/trust analysis, the FCFE analysis wins.
→ `concepts/dividend-policy/peer-group-payout-analysis.md`, `concepts/dividend-policy/market-regression-payout-prediction.md`

## S10.7 Forecast capacity
Project 5 years: revenues, net income, capex, depreciation at stated growth rates; `ΔWC_t = WC% × (Revenues_t − Revenues_{t−1})` (the **increment**, not the level); `FCFE_t = NI_t − (Capex_t − Dep_t)(1−DR) − ΔWC_t(1−DR)`; expected dividends at the historical growth rate (stickiness); **cash available for buybacks = FCFE_t − expected dividends_t**. Negative capacity is the finding, not a bug to be assumption-tuned away.
→ `concepts/dividend-policy/payout-forecasting.md`

## S10.8 Choose the form and execute
**Form:**
- One-time or uncertain surplus → **buyback** or special dividend (no stickiness commitment).
- Recurring, predictable surplus at a mature firm → **dividend increase** (the market reads it as a commitment).
- Income-seeking clientele → dividends. Taxable deferral-preferring base, or management believes the stock is undervalued → buybacks.
Quantify a buyback properly: the value effect runs through **leverage** (relever beta, recompute WACC, revalue EV), a **wealth transfer** ((fair value − buyback price) × shares bought, only meaningful with an independent fair-value estimate), and **EPS accretion** — which is arithmetic, not value, and follows mechanically whenever PE_acquirer > PE_target or the funding cost is below the earnings yield.
→ `concepts/dividend-policy/buyback-value-and-eps-effect.md`

**Constraints to check before recommending a change:**
- *Clientele.* A cut forces turnover in the shareholder base.
- *Contractual.* Preferred-share promises can convert an economic decision into a control transfer.
- *Regulatory.* Mandated minimums hurt high-growth firms most. Caps hurt mature firms with poor projects. Bank capital rules block payout outright.
- *Signaling.* Size the announcement effect before committing.
**Framing a cut:** bundling it with a credible investment/growth announcement is associated with roughly −5.2% at announcement and **+8.8%** the following quarter; bundling it with an earnings decline is roughly −8.2% and only +1.8%. Size the announcement exposure as market cap × |CAR|, and adjust the CAR for the era (the signal has decayed by roughly two-thirds since the 1960s–70s).
**Never** initiate a dividend at a high-growth firm to widen the investor base. FCFE is negative, so the dividend must be funded by issuing stock or by underinvesting. Flotation costs run from 3.5% on large issues to 22% on sub-$1m issues. Initiation also signals the end of high growth.
→ `concepts/dividend-policy/managing-dividend-changes.md`, `concepts/dividend-policy/clientele-effect.md`, `concepts/dividend-policy/dividend-signaling.md`, `concepts/dividend-policy/dividend-wealth-transfer.md`, `concepts/dividend-policy/bad-reasons-for-paying-dividends.md`, `concepts/dividend-policy/ex-dividend-day-and-dividend-capture.md`, `concepts/dividend-policy/three-schools-of-dividend-thought.md`

**Outputs.** `payout`: {dividends, buybacks, cash_returned, payout_ratio, cash_payout_ratio, yield, buyback_share, FCFE_three_variants (annual + aggregate), cash_returned_pct_of_each, trust_scores {ROE−COE, ROC−WACC, jensen_alpha}, quadrant + variant_used, peer_comparison (avg and median), regression_prediction + buyback_adjusted_read, five_year_forecast, recommendation {amount, form, speed}, constraints[]}.

**Validation.** V-19, V-20.

**Deliverable format.** `concepts/deliverables-worked-examples/dividend-policy-deliverable.md`.

---

# S11 — Tying it to valuation

**Purpose.** Convert every recommendation into dollars. Run the DCF **twice** — status quo (the firm as currently run and financed) and restructured (with the S6/S7/S8/S9/S10 recommendations in place) — and report the difference as the **value of control**. Part X.

**Inputs.** S3 cleaned financials; S4 hurdle rates (current and at the recommended structure); S5 ROC and reinvestment rate; S7 optimal ratio; S10 payout recommendation.

## S11.1 Status quo valuation
1. Base year: normalized revenues, operating margin, EBIT, effective/marginal tax rate, invested capital.
2. `Reinvestment rate = (net capex + ΔWC) ÷ EBIT(1−t)`; `ROC = EBIT(1−t) ÷ invested capital`; **`g = reinvestment rate × ROC`**. Never impose a growth rate independently — growth must be paid for.
3. Cost of capital at the **current** structure (S4).
4. `FCFF = EBIT(1−t) × (1 − reinvestment rate)` over the explicit growth period.
5. Terminal value at the end of the growth period.
6. Equity bridge: `+ cash + cross-holdings/non-operating assets − debt (incl. leases) − minority interests − employee option value`, then ÷ shares.
7. Compare to market capitalization.
→ `concepts/acquisitions-control-enhancement/status-quo-valuation.md`, `concepts/deliverables-worked-examples/two-stage-fcff-company-valuation.md`

## S11.2 Growth pattern and terminal discipline
- Stage count:

  | Firm profile | Model |
  |---|---|
  | Grows at or below the economy's rate; or regulated; or average risk and reinvestment | Stable (single stage) |
  | Growth ≤ economy growth + 10%; or a moat with a finite life | 2-stage |
  | Growth > economy growth + 10%; or characteristics far from the norm | 3-stage / n-stage |
- **Terminal caps. All four are mandatory.**
  1. `g ≤ riskfree rate` in the valuation currency. The riskfree rate proxies nominal economy growth.
  2. Stable reinvestment rate = **g/ROC**. For equity models, payout = 1 − g/ROE.
  3. Stable beta → 1.0, with a mature debt ratio and fading country risk.
  4. Any perpetual excess return is argued explicitly or set to zero. At ROC = cost of capital, growth is value-neutral at **any** g.
- Reverse check: `implied perpetual ROC = g ÷ (1 − FCFF_terminal/EBIT(1−t)_terminal)`. Is it defensible?
- Never use an exit multiple and then call the result an intrinsic valuation.
→ `concepts/dcf-cashflows-growth/terminal-value.md`

## S11.3 Restructured valuation — the four levers
Rebuild the DCF with the recommendations in place. Every change must land on exactly one of four levers:
1. **Cash flows from existing assets** — margin improvement, divesting negative-EBIT assets, tax-rate reduction, capex discipline, working-capital reduction. (From S5's benchmarking and S6's post-mortem ladder.)
2. **Expected growth** — higher reinvestment rate and/or higher ROC (= margin × capital turnover). **Only** if ROC > cost of capital; otherwise raising reinvestment *destroys* value and the right move is to shrink.
3. **Length of the growth period** — extend only if you can name the competitive advantage (brand, legal protection, switching costs, cost advantage). This is the most common way to inflate a DCF.
4. **Cost of capital** — move to the S7 optimal debt ratio; reduce operating leverage; make the product less discretionary; match debt to assets (S9).
Benchmark each gap against the sector and, in an acquisition context, against the acquirer.
→ `concepts/acquisitions-control-enhancement/paths-to-value-creation.md`, `concepts/acquisitions-control-enhancement/restructured-value-and-value-of-control.md`, `concepts/dcf-cashflows-growth/value-of-growth.md`

## S11.4 Value of control and the price bridge
- `Value of control = restructured equity value − status quo equity value`. Per share, and as a % of the current price.
- **Discount for delay:** if changes take k years, `adjusted control value = (optimal − status quo)/(1+r)^k`. A three-year turnaround is worth materially less than the undiscounted gap.
- **Market-implied probability of change:** `P = (market price/share − status quo value/share) ÷ (optimal value/share − status quo value/share)`. `P ≤ 0` → the market prices no chance of change. `P ≥ 1` → your optimal value is too low or the market prices something outside your model — investigate before trading on it. Compare P to your own governance-based estimate (from S1.7's counter-force scores and the takeover screen).
- Allocate control value where it can be exercised: to the **voting** class in a dual-class structure (`voting premium = P×(optimal − status quo)/voting shares ÷ per-share status quo value`), and to controlling stakes (priced off optimal) rather than minority stakes (priced off status quo) in a private firm.
→ `concepts/acquisitions-control-enhancement/expected-value-of-control.md`, `concepts/acquisitions-control-enhancement/implied-probability-of-management-change.md`, `concepts/acquisitions-control-enhancement/voting-premium-and-minority-discount.md`, `concepts/deliverables-worked-examples/value-of-control-and-synergy.md`

## S11.5 Decomposition and cross-check
Report the value stack: `status quo value + value of control (+ value of synergy, if B7) = total value`.
Cross-check with EVA: `firm value = capital invested + PV of all future EVA`, including the terminal-capital reconciliation `adjusted terminal capital = EBIT(1−t)_terminal ÷ ROC_terminal`. If the EVA and DCF routes disagree, an assumption is inconsistent — usually the terminal capital adjustment, the beginning-vs-ending capital convention, or a reinvestment rate that is not g/ROC.
→ `concepts/acquisitions-control-enhancement/eva-and-dcf-equivalence.md`

## S11.6 Name the driver
Answer the question the whole playbook exists for: **which variable drives the value**, and what a hired value-enhancer would do first. Run a two-input sensitivity grid around the two levers with the largest effect. If the market price sits above the DCF, state what growth or margin the market must be assuming (invert to the implied growth rate) rather than declaring the stock overvalued.

**Outputs.** `valuation`: {status_quo {assumptions, FCFF path, TV, operating assets, equity bridge, value/share}, restructured {same, with changed levers itemized}, value_of_control (total, per share, delay-adjusted), implied_probability_of_change, value_stack, key_driver, sensitivity_grid, price_vs_value, implied_market_growth}.

**Validation.** V-21 through V-25.

---

# S12 — Synthesis and cross-stage validation

**Purpose.** Compress ten parts to one page, run the cross-artifact validator, and resolve conflicts between stages.

**Procedure.**
1. **Executive scorecard.** One column per company or scenario. One row per headline metric, in stage order:

   | Row | Source |
   |---|---|
   | Power score | S1 |
   | Beta approach and levered beta | S4 |
   | Jensen's alpha, R² | S4.7 |
   | ROE − COE, ROC − WACC, EVA | S5 |
   | Current debt ratio, optimal debt ratio, ΔWACC, Δvalue | S7 / S8 |
   | Dividends, FCFE | S10 |
   | Value per share, price per share | S11 |

   Every cell is **pulled** from its section, never recomputed.
   → `concepts/deliverables-worked-examples/project-executive-summary-scorecard.md`
2. Read across rows to find the outlier for each question; read down columns to build each company's story.
3. **Run the validation rules below.** Any V-rule failure blocks the report.
4. **Resolve conflicts** with the precedence table.
5. State the three decisions as recommendations with magnitudes, and name what would change each.

**Conflict precedence.**

| Conflict | Resolution |
|---|---|
| Intrinsic optimum (S7.3/7.4) vs peer/regression benchmark (S7.4) | Intrinsic wins; explain the gap, do not average |
| FCFE/trust verdict (S10.3–4) vs peer or regression payout benchmark (S10.6) | FCFE/trust wins |
| Bottom-up beta (S4.4) vs regression beta (S4.7) | Bottom-up wins for hurdle rates; regression is a diagnostic |
| Synthetic rating (S4.5) vs actual agency rating | Actual wins unless visibly stale; the gap is usually country risk or normalized earnings |
| Cash-deficit dividend verdict vs poor-project verdict (S10.5) | Investment policy first, payout second |
| S9 debt design raising capacity vs S7 optimum | Re-run S7 once with the improved capacity; then freeze |
| Recommended ratio (S7.5, constrained) vs mechanical argmin | Constrained recommendation is the answer; report both |
| Market price above DCF value (S11.6) | Report the implied growth the market requires; do not declare overvaluation from the DCF alone |
| Positive Jensen's alpha vs negative ROE − COE | Weight the accounting/project measure for payout decisions; disclose the divergence |

**Outputs.** `REPORT.md` (ten parts + scorecard), `scorecard.json`, `validation_report.json`.

---

# Branches

Branches are selected at S1/S2/S3 and **replace or constrain** named stages. Never run the displaced machinery alongside them.

## B1 — Financial-service firm (bank, insurer, brokerage)
**Trigger:** sector classification at S0/S3.
**Replaces:** S4.4 (beta), S4.5 (cost of debt), S7 (entire), S10.3 (FCFE), S11 (FCFF route).
**Rules.**
- Do **not** unlever/relever betas — estimating debt and equity for a bank is not meaningful. Use the **median levered** betas of comparable banks, weighted by net revenues.
- Do **not** synthesize a rating from ordinary coverage. If a coverage-based analysis is unavoidable, use **long-term interest expense only** and the financial-firm table, whose thresholds are far lower.
- Do **not** compute an optimal debt ratio. Capital structure is governed by **regulatory capital**, measured on **book** values. `New equity needed = target equity ratio × post-expansion assets − existing equity`.
- Choose an equity strategy: regulatory minimum / self-regulatory (size equity to absorb potential losses) / combination with buffers.
- `FCFE = net income − investment in regulatory capital`, where `investment_t = (capital ratio_t × risk-adjusted assets_t) − (capital ratio_{t−1} × RAA_{t−1})`, `net income_t = ROE_t × book equity_t`, and book equity grows by the retained capital (the table is recursive). Negative FCFE means dividends and buybacks make no sense regardless of accounting earnings.
- Valuation route: dividend discount or equity excess-return, never FCFF.
**Concepts.** `concepts/capital-structure/financial-firm-capital-structure.md`, `concepts/dividend-policy/fcfe-for-banks.md`, `concepts/cost-of-debt-capital/cost-of-debt-estimation-routes.md`, `concepts/dark-side-difficult/financial-service-firm-valuation.md`, `concepts/dark-side-difficult/bank-fcfe-and-excess-return-models.md`.

## B2 — Private or closely held firm (undiversified owner)
**Trigger:** S2 marginal investor not diversified, or S0 `traded=false`.
**Constrains:** S4.4, S7.3, S7.7, S11.
**Rules.**
- Beta from comparables, using the **median** and never the mean. Private-firm comparable sets routinely contain 500%+ D/E outliers that destroy an average. Unlever at the comparables' median D/E, cash-correct, then relever at the **industry median market D/E**, because a private firm has no market D/E of its own.
- Convert to **total beta = market beta ÷ √(median comparable R²)**. Typical sector correlation ~0.5, so total betas run near twice market betas and the cost of equity rises by half or more.
- Estimate equity value from comparables (net income × peer PE) for the capital-structure schedule.
- Run the S7 schedule entirely on total betas; the optimum typically falls relative to an otherwise identical public firm.
- Value from the owner's perspective (total beta) **and** from a diversified buyer's perspective (market beta). The gap is the value of diversification and is the negotiating range.
- Apply illiquidity and minority discounts per the scenario; do not stack total beta and an illiquidity discount without checking overlap.
**Concepts.** `concepts/cost-of-equity/total-beta.md`, `concepts/cost-of-equity/non-traded-asset-betas.md`, `concepts/capital-structure/optimal-debt-ratio-by-firm-type.md`, `concepts/asset-based-private/private-company-cost-of-capital.md`, `concepts/asset-based-private/illiquidity-discount.md`, `concepts/asset-based-private/minority-discount.md`.

## B3 — Emerging-market exposure
**Trigger:** material revenues, production or assets in non-Aaa countries.
**Constrains:** S4.2, S4.3, S4.5, S4.9, S7.7, S11.
**Rules.**
- Strip the sovereign default spread from the local government bond rate **once**; do not also leave country risk in the cash flows.
- CRP by **operations**, not incorporation. Choose one attachment mechanism (additive / through beta / lambda) — never two.
- Cost of debt: global-agency rating already embeds country risk; local-scale rating does not. Add λ × sovereign spread only in the second case.
- Scale interest coverage down by (local long rate ÷ US long rate) before the synthetic-rating lookup.
- Add the country default spread at every rating in the S7 schedule; the optimum compresses even when cash-flow returns look strong.
- Convert rates and growth by inflation differential; cross-check against a direct local rebuild.
- Consider a truncation/political-risk scenario weight for nationalization or regime change.
**Concepts.** `concepts/cost-of-equity/country-risk-premium.md`, `concepts/cost-of-equity/operation-weighted-erp.md`, `concepts/cost-of-equity/lambda-country-risk-exposure.md`, `concepts/cost-of-debt-capital/country-risk-in-cost-of-debt.md`, `concepts/dark-side-difficult/country-risk-exposure.md`, `concepts/dark-side-difficult/truncation-and-political-risk.md`, `concepts/dark-side-difficult/currency-consistency-and-invariance.md`.

## B4 — Multi-business firm
**Trigger:** material segments with different business risk.
**Constrains:** S4.4, S4.8, S5, S6, S9.
**Rules.**
- Bottom-up beta per business, value-weighted (business value = segment revenues × peer EV/Sales), then relevered.
- Allocate firm debt across divisions on a stated key (identifiable assets by default) and derive divisional D/E and WACC.
- Judge each project against **its own division's** rate. A company-wide rate makes safe divisions subsidize risky ones and tilts the firm toward its riskiest businesses.
- Sanity-check implausible divisional debt ratios produced by the allocation key — an artifact ratio produces an artificially low divisional WACC that lets weak projects clear.
- Debt design: profile each business separately, then aggregate to a firm-level target (S9.1's Disney-style business-by-business table).
**Concepts.** `concepts/cost-of-debt-capital/divisional-cost-of-capital.md`, `concepts/cost-of-equity/bottom-up-beta.md`, `concepts/capital-structure/debt-design-framework.md`.

## B5 — Cyclical or commodity firm
**Trigger:** wide multi-year range in pre-tax operating margin; commodity price driver.
**Constrains:** S3, S5, S7.3, S11.
**Rules.**
- Compute the pre-tax operating margin for each of the last 3–5 years. If the range is wide, produce **both** a last-twelve-month EBIT and a normalized EBIT (average margin × current revenues, or average EBIT over a cycle).
- Run the S7 schedule **twice** and report both optima. Say which you would act on given where the cycle sits — the swing can be 20 percentage points, and it comes entirely from the coverage ratio.
- Never recommend a large debt increase off peak-cycle earnings.
- In S5, judge returns on normalized earnings; in S11, normalize the base year or drive the model off the commodity price.
**Concepts.** `concepts/capital-structure/optimal-debt-ratio-by-firm-type.md`, `concepts/dark-side-difficult/normalized-earnings.md`, `concepts/dark-side-difficult/commodity-and-cyclical-valuation.md`, `concepts/dcf-cashflows-growth/normalizing-depressed-earnings.md`.

## B6 — Money-losing / young growth firm
**Trigger:** negative or trivially small EBIT; EBITDA/EV in low single digits.
**Constrains:** S3, S5, S7, S10, S11.
**Rules.**
- Negative EBIT makes coverage negative → bottom rating bucket. Expect the S7 optimum at **0–10%** and do not force it toward peer leverage.
- No usable ROC/EVA verdict from current earnings; judge on the marginal ROIC and the revenue-driven build instead.
- FCFE will be negative; the payout question becomes a financing question. Zero payout is correct behavior, not a deficiency.
- Valuation route: revenue-driven, working backwards from a mature end-state with margin convergence, an NOL tax engine, fading discount rates, and a sales-to-capital reinvestment link. Add a failure/distress probability branch.
- Tax rate at the margin is effectively zero until the shelter is used; model it explicitly.
**Concepts.** `concepts/dark-side-difficult/young-company-valuation.md`, `concepts/dark-side-difficult/sales-to-capital-reinvestment.md`, `concepts/dark-side-difficult/distress-and-failure-adjusted-value.md`, `concepts/dcf-cashflows-growth/top-down-revenue-growth.md`, `concepts/capital-structure/financing-life-cycle.md`.

## B7 — Acquisition or control situation
**Trigger:** the firm is a live acquirer, a target, or an activist/restructuring subject.
**Extends:** S6.5 and S11.
**Rules.**
1. **Set the prior from the base rate.** Target CARs ~+17% to +19%; bidder CARs ~0% to −2%; ~50% of acquisition programs fail at least one McKinsey value test and 25% fail both; ~50% of deals divested over 10+ years. The burden of proof belongs on the deal.
2. **Audit against the seven sins** before valuing. Fill in Passed/Failed and the rationalization offered for each:

   | Sin | Test statistic |
   |---|---|
   | Risk transference | Discount rate used vs the target's own cost of equity |
   | Debt subsidy | Debt ratio and cost of debt used vs the target's own |
   | Auto-pilot control premium | Is the premium a rule-of-thumb %, or restructured − status quo? |
   | Elusive synergy | Ratio of unquantified to quantified synergy dollars |
   | Relative pricing | Did the price or the terminal value come from a multiple? |
   | Verdict first | Does the valuation post-date the price? |
   | No accountability | Is there a named person whose pay depends on delivery? |
3. **Build the four numbers:** acquisition price; **status quo value**; **restructured value** (S11.3); **synergy value** = combined-with-synergy − combined-without-synergy, where the "without" baseline uses the target's **restructured** value so control gains are not double counted. Verify the no-synergy combined value equals the sum of the standalones exactly.
4. **Apply the acid test by motive:** undervaluation → price < status quo value; control → price < restructured value; synergy → price < restructured value + synergy value. Fail all three and exactly two explanations survive — the synergy is underestimated, or the acquirer is overpaying. Name which.
5. **Map every claimed synergy to one input** (higher ROC, higher reinvestment rate, longer growth period, higher margin, lower tax rate, higher debt ratio). Reject diversification as a synergy for public firms.
6. **Haircut delivery odds.** Split cost from revenue synergies and never blend them. ~70% of mergers miss expected revenue synergies while most hit ≥90% of cost savings. Apply a 2–5% customer-attrition haircut to revenue synergies; subtract one-time costs to achieve on the cost side; assume the synergy is competed into the price if you are one of several bidders.
7. **Deal design shifts the odds:** sole bidder > bidding war; private target or subsidiary > public target; cash > stock; small target > large target (though for private/subsidiary targets, larger deals performed *better*); cost synergies > growth synergies. Set a walk-away price before the auction; the winner's curse runs to −25% to −30% CAR over 40 months for winners against +25% to +30% for losers.
8. **Assign accountability** — name the person whose compensation depends on the promised benefits arriving.
9. **Decompose the price** at announcement, not at the write-off: pre-deal book equity → + purchase-accounting intangibles → + market premium → + acquirer premium = price; goodwill = price − adjusted book equity, which is a public promise of value the acquirer must now create.
**Concepts.** `concepts/acquisitions-control-enhancement/acquisition-empirical-record.md`, `.../seven-sins-of-acquisitions.md`, `.../three-reasons-and-acid-test.md`, `.../status-quo-valuation.md`, `.../restructured-value-and-value-of-control.md`, `.../synergy-taxonomy.md`, `.../valuing-synergy.md`, `.../synergy-delivery-odds.md`, `.../target-discount-rate-discipline.md`, `.../control-premium-rules-of-thumb.md`, `.../transaction-and-exit-multiples.md`, `.../deal-bias-and-ego.md`, `.../acquisition-strategy-design.md`, `.../acquisition-price-buildup-and-goodwill.md`, `.../abinbev-sabmiller-case.md`.

---

# Consistency and validation rules

Every rule is a hard check. A failure blocks the dependent stage (or, at S12, the report).

**Scope and units**
- **V-01 Currency.** The riskfree rate, ERP, cost of debt, cash flows, growth rate and terminal growth rate are all in the mandate currency. A currency mismatch is the single most common silent error.
- **V-02 Vintage.** Spread tables, country ERP tables, marginal tax rates and the mature-market ERP all carry the same `as_of` date as the mandate. Never pair a current riskfree rate with a stale country-ERP table.

**Governance**
- **V-03 Objective.** The objective in S1.9 is derived from (T, E, B) and is stated before any valuation runs. Manager-stockholder and social-cost failures may not be used to change the objective — only the constraint set.

**Statements**
- **V-04 Debt definition closure.** One definition of debt runs through five places: the D/E for beta relevering, the WACC weights, interest coverage, invested capital, and the equity bridge. It includes capitalized leases and the straight-debt half of any convertible.
- **V-05 Lease consistency.** If leases are capitalized, all four consequences are applied: debt up, EBIT restated, interest expense restated, invested capital up. Partial application is a validation failure.
- **V-06 Basis pairing.** Market-value hurdle rates are used with market-value valuation; book/net hurdle rates are used with book accounting returns. Never cross them.

**Hurdle rates**
- **V-07 Claimholder match.** Returns to equity are compared only to a cost of equity; returns to the firm only to a cost of capital.
- **V-08 Risk level match.** A project or division is judged at its own business's rate, not the corporate average.
- **V-09 Leverage consistency.** The D/E used to relever beta equals the D/(D+E) implied by the WACC weights. Gross debt throughout, or net debt throughout — never mixed (levering on net debt and weighting on gross debt produces a WACC that is too low).
- **V-10 Tax shield counted once.** The (1−t) factor is applied to the cost of debt only, never to the whole WACC, and the interest tax shield never appears in FCFF.
- **V-11 Country risk counted once.** The sovereign spread is stripped from the riskfree rate **or** added through the ERP/lambda, and the CRP is attached through exactly one mechanism (additive, beta, or lambda).
- **V-12 Preferred and options.** Preferred stock carries no tax shield and is either a third capital component (≥5% of firm value) or explicitly folded into debt.

**Projects**
- **V-13 Incremental once.** Side costs and side benefits appear either inside the annual cash flows or as a lump-sum PV adjustment — not both. The adjustment route and the direct route reconcile to rounding.
- **V-14 Sunk closure.** Sunk outlays are excluded **and** the depreciation tax shield on any capitalized sunk asset is removed.
- **V-15 Terminal consistency.** The capitalized year is a steady-state year, not a growing forecast year; maintenance capex is consistent with the assumed perpetual growth (positive g requires maintenance above depreciation); g ≤ inflation for a project, ≤ riskfree rate for a firm.

**Capital structure**
- **V-16 Schedule invariance.** EBITDA, depreciation, EBIT, capex, riskfree rate, ERP, unlevered beta, marginal tax rate and total capital are identical across every row of the S7 schedule. Only the mix varies (unless the enhanced approach is on, in which case operating income varies **only** through the rating-keyed haircut).
- **V-17 Objective function match.** Standard approach → select on minimum WACC. Enhanced approach or any approach where operating income varies with `d` → select on **maximum firm value**.
- **V-18 Single protection.** A rating constraint and a downside EBIT haircut are not both applied.

**Payout**
- **V-19 Augmented dividends.** Every payout comparison — peer, regression, FCFE, yield — is run on dividends **plus** buybacks on both sides, or the dividend-only limitation is stated explicitly.
- **V-20 FCFE variant declared.** The dividend-matrix quadrant names the FCFE variant it used, and the other two variants are reported. Negative FCFE makes the cash-returned-as-%-of-FCFE ratio meaningless — report NA, not a negative number. Negative net income makes the payout ratio meaningless — report NA.

**Valuation**
- **V-21 Growth is earned.** `g = reinvestment rate × ROC` in every phase. A growth rate asserted independently of reinvestment is a validation failure.
- **V-22 Terminal caps.** `g ≤ riskfree rate`; stable reinvestment = g/ROC; stable beta → 1.0 with a mature debt ratio; any perpetual excess return is argued explicitly; the implied perpetual ROC is checked in reverse.
- **V-23 Structure declared.** The growth-phase WACC uses either the current or the recommended capital structure — stated, and the same one used in the corresponding scenario.
- **V-24 No double counting in the value stack.** Control value and synergy value do not overlap (synergy is measured off the **restructured** target). Brand, management quality and "strategic" premiums are not added on top of a DCF that already reflects them. Cash counted in the flows is not also added in the bridge.
- **V-25 Reconciliation.** If EVA and DCF are both produced, they must agree; a gap means the terminal-capital adjustment, the capital convention, or the reinvestment rate is inconsistent. Firm and equity routes must agree under constant market-value leverage.

**Cross-stage**
- **V-26 Return spread drives the payout axis.** The "good projects / poor projects" axis in S10.5 is the same verdict as S5's spread, computed on the same basis.
- **V-27 Structure propagation.** The optimal ratio in S7 is the ratio used in S8's recap valuation, S9's capacity check, S10's target-ratio FCFE (if a target is used) and S11's restructured WACC — or the divergence is explained.
- **V-28 Scorecard fidelity.** Every scorecard cell is pulled from its owning section. Discrepancies between the summary and the body are a validation failure, not a rounding issue.

---

# Determinism boundary

| Stage | Script computes | Agent judges |
|---|---|---|
| S1 Governance | CalPERS tests, insider counts, control wedge, group and look-through stakes, withhold %, greenmail transfer, premium and CAR arithmetic, recovery ratio, governance-index counts, takeover screen | Independence beyond formal labels, archetype, the three booleans (T, E, B), counter-force strength, agency-cost size, Power score |
| S2 Stockholders | Ownership percentages of shares and float | Who is actually marginal; whether an "institutional" block is diversified |
| S3 Statements | Lease PV and all four consequences, R&D asset, market value of debt, convertible split, invested capital, TTM roll-up, fixed-point iteration | Which items are non-recurring, whether to capitalize, normalization basis and window, marginal tax rate choice, debt classification of hybrids |
| S4 Hurdle rates | Riskfree derivation, spread and rating lookups, unlever/relever, value weights, coverage, WACC, divisional allocation, currency conversion, regression beta/alpha/R² | Comparable set, ERP method and vintage, country-risk attachment, lambda, gross vs net, rating route, division definitions, allocation key |
| S5 Returns | ROC, ROE, spreads, EVA, industry benchmark lookup | Normalization of the numerator, correction of the denominator, whether future projects resemble past ones, whether one year is representative |
| S6 Projects | NPV, IRR (all roots), MIRR, PI, equivalent annuity, payback, sensitivity grids, break-evens, simulation, side-cost PVs, terminal value | The counterfactual, project life, which costs are incremental, alternative use of owned resources, cannibalization share, whether an option genuinely exists |
| S7 Capital structure | The entire 0–90% schedule including both fixed points, tax caps, argmin/argmax, APV, stress table, constraint cost, regression prediction | Which EBIT (current vs normalized), distress severity, rating floor, bankruptcy-cost %, whether to refinance all debt, peer group definition |
| S8 Transition | Implied growth, both value-gain methods, rational buyback price and its fixed-point check, post-buyback per-share arithmetic | Bankruptcy/takeover threat, whether projects genuinely clear the hurdle, speed, stockholder preference |
| S9 Debt design | Project and bond duration, the eight macro regressions with t-stats, bottom-up weighted coefficients, existing-profile statistics | Whether a slope is actionable, target currency and fixed/floating mix, special features, when tax overrides matching, mispricing judgment |
| S10 Payout | All three FCFE variants, cash returned, payout and yield, trust ratios, Jensen's alpha, quadrant placement, peer statistics, regression prediction, five-year forecast, buyback value model | Window, debt-ratio choice, which variant leads, whether the excess return repeats, clientele, form of payout, framing of a cut |
| S11 Valuation | Both DCFs, terminal value, equity bridge, value of control, implied probability, voting premium, EVA reconciliation, sensitivity grid, implied market growth | Growth-period length, which gaps are closeable and how fast, terminal ROC and whether a moat persists, option value, the key-driver narrative |
| S12 Synthesis | Scorecard assembly, gap computations, all V-rules | Conflict resolution beyond the precedence table, the narrative |

---

# Artifact map

| Stage | Artifact | Consumed by |
|---|---|---|
| S0 | `mandate` | all |
| S1 | `governance` | S2, S8 (takeover threat), S10 (trust context), S11 (probability of change), S12 |
| S2 | `stockholders` | S4 (risk measure), S7 (discipline lens), S12 |
| S3 | `cleaned` | S4, S5, S6, S7, S10, S11 |
| S4 | `hurdle_rates` | S5, S6, S7, S8, S10, S11 |
| S5 | `returns` | S8 (good-projects branch), S10 (trust axis), S11 (growth and ROC), S12 |
| S6 | `investment` | S11 (restructuring levers), S12 |
| S7 | `capital_structure` | S8, S9, S10 (target DR), S11 (restructured WACC), S12 |
| S8 | `transition` | S11 (value bridge), S12 |
| S9 | `debt_design` | S7 (capacity feedback, once), S12 |
| S10 | `payout` | S11 (restructured payout policy), S12 |
| S11 | `valuation` | S12 |
| S12 | `REPORT.md`, `scorecard.json`, `validation_report.json` | terminal |

---

# Pitfall register (the errors that recur across stages)

1. Defaulting to "maximize shareholder value" without running the (T, E, B) matrix.
2. Treating institutional ownership as monitoring.
3. Using book-value weights in the cost of capital because they are already on the balance sheet.
4. Ignoring operating leases — it understates debt, overstates the equity weight, flatters operating income and inflates ROIC, all at once.
5. Using the effective tax rate where the marginal rate belongs, or vice versa.
6. Comparing a market-value cost of equity to a book-value ROE.
7. Comparing a return on capital to a cost of equity (or the reverse).
8. Using one company-wide hurdle rate for every division and every project.
9. Adding country risk twice, or attaching it through two mechanisms.
10. Normalizing the riskfree rate upward while leaving growth, inflation and the ERP untouched.
11. Letting EBIT drift across the capital-structure schedule, or forgetting the tax cap at high leverage, or relevering with the headline tax rate once the cap binds.
12. Selecting on minimum WACC when indirect bankruptcy costs are switched on.
13. Applying both a rating constraint and a downside EBIT haircut.
14. Running the qualitative debt trade-off *after* the schedule and reverse-engineering the story.
15. Reporting the mechanical argmin as the recommendation.
16. Recommending a large debt increase off peak-cycle earnings.
17. Reading a low dividend payout as bad without checking the return spread.
18. Comparing payout on dividends alone in a market where buybacks dominate.
19. Leaning on actual-debt FCFE in a heavy borrowing year and calling the payout affordable.
20. Recommending a dividend cut in the deficit/poor-projects quadrant and stopping there.
21. Growth without reinvestment — the classic terminal-value sleight of hand.
22. Extending the high-growth period without naming the competitive advantage.
23. Using an exit multiple and describing the result as an intrinsic valuation.
24. Adding a control premium, a brand premium and a management-quality premium on top of one DCF.
25. Paying the full value of control or the full synergy value as a premium.
26. Using the acquirer's cost of capital or debt capacity to value a target.
27. Presenting EPS accretion as evidence of value.
28. Treating a positive Jensen's alpha as evidence of management skill, or comparing the raw intercept to zero.
29. Acting on statistically insignificant macro regression slopes in debt design.
30. Recomputing scorecard values instead of pulling them from their sections.
