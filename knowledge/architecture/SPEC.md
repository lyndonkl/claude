# Financial analysis system — architecture specification

This is the single source of truth for the agent/skill suite. Every builder reads this
so the pieces fit. Terminology, file names, JSON keys and gate names here are binding.

---

## 1. Design rules

1. **Agents reason. Scripts compute.** Any computation that is a pure function of numbers
   is a Python script in a skill, never model arithmetic. Agents choose inputs, interpret
   outputs, and decide; they do not do arithmetic in their heads.
2. **Agents are path-agnostic.** No agent hardcodes a directory. The orchestrator passes
   absolute paths for every input and output at invocation time. Agents know *what* a file
   contains (schema) and *what* they must write (schema), never *where* it sits in a tree.
3. **One writer per artifact.** Every file has exactly one agent authorized to write it.
   Agents never edit another agent's artifact; disagreements travel as findings, not edits.
4. **Gates before work.** Every agent validates its preconditions and refuses to proceed
   when inputs are missing or inconsistent, returning a `blocked` status naming what it needs.
5. **State is on disk, not in conversation.** Agent-to-agent handoff is always a file with a
   declared schema. This survives context loss and makes reruns cheap.
6. **Classification precedes everything.** Company type determines which methods are valid.
   Running standard machinery on a bank, a distressed firm, or a pre-revenue company produces
   confident nonsense — the most expensive failure mode in this domain.

## 2. Analysis modes

The orchestrator resolves the user request into exactly one mode:

| Mode | Question | Terminal artifact |
|---|---|---|
| `valuation` | What is this company worth? Buy/sell/hold? | verdict + value per share |
| `corporate-finance` | Are this firm's investing/financing/payout choices right? | 10-part corporate finance assessment |
| `acquisition` | What should we pay for this target? | maximum price + synergy split |
| `project` | Should we make this investment? | NPV verdict on the project |
| `ipo` | What is this private company worth going public? | offer price range |
| `restructuring` | What is this company worth run differently? | status quo vs optimal + value of control |

Modes share the same substrate: every mode except `project` needs cleaned financials and a
cost of capital, so those stages are common and mode selects what runs after.

## 3. Workspace layout (orchestrator-owned)

The orchestrator creates and owns this tree. Agents receive absolute paths into it.

```
<workspace>/
  00-mandate/     mandate.json           orchestrator
  00-mandate/     state.json             orchestrator   (the state machine's memory)
  01-data/        raw-financials.json    data-collector
  01-data/        market-data.json       data-collector
  01-data/        sources.md             data-collector
  01-data/        gaps.json              data-collector
  02-diagnosis/   classification.json    diagnostician
  02-diagnosis/   diagnosis.md           diagnostician
  03-narrative/   narrative.md           narrative-analyst
  03-narrative/   drivers.json           narrative-analyst
  04-financials/  cleaned-financials.json statement-analyst
  04-financials/  adjustments.md         statement-analyst
  05-capital/     cost-of-capital.json   cost-of-capital-analyst
  05-capital/     cost-of-capital.md     cost-of-capital-analyst
  06-intrinsic/   forecast.json          intrinsic-valuation-analyst
  06-intrinsic/   dcf-result.json        intrinsic-valuation-analyst
  06-intrinsic/   intrinsic.md           intrinsic-valuation-analyst
  07-relative/    relative-result.json   relative-valuation-analyst
  07-relative/    relative.md            relative-valuation-analyst
  08-corpfin/     capital-structure.json capital-structure-analyst
  08-corpfin/     capital-structure.md   capital-structure-analyst
  08-corpfin/     payout.json            payout-policy-analyst
  08-corpfin/     payout.md              payout-policy-analyst
  08-corpfin/     investment.json        investment-analyst
  08-corpfin/     investment.md          investment-analyst
  09-options/     real-options.json      real-options-analyst
  09-options/     real-options.md        real-options-analyst
  10-challenge/   challenge.json         valuation-critic
  10-challenge/   challenge.md           valuation-critic
  11-verdict/     verdict.json           reconciler
  11-verdict/     REPORT.md              reconciler
```

Special-situations work does not get its own directory: the special-situations-analyst writes
into the directory of the stage it replaces (e.g. its bank valuation lands in `06-intrinsic/`
with the same schema), so downstream consumers never branch on company type.

## 4. State machine

`state.json` is the orchestrator's memory. Shape:

```json
{
  "mode": "valuation",
  "company": {"name": "...", "ticker": "...", "currency": "USD", "valuation_date": "YYYY-MM-DD"},
  "gates": {"G0_mandate": "passed", "G1_data": "passed", "G2_classified": "pending"},
  "route": {"primary_path": "standard-fcff", "overlays": ["intangible-heavy"], "constraints": ["..."]},
  "stages": {"cost-of-capital": {"status": "complete", "agent": "...", "artifacts": ["..."], "attempts": 1}},
  "open_findings": [{"id": "F1", "raised_by": "valuation-critic", "severity": "high", "status": "open"}]
}
```

Gates, in order. A gate is a predicate over artifacts, checked by the orchestrator before
dispatching the stages that depend on it.

| Gate | Passes when | Blocks |
|---|---|---|
| `G0_mandate` | Mode, company, currency, valuation date fixed | everything |
| `G1_data` | Minimum viable inputs present, or user supplied them; gaps listed with fallbacks | diagnosis onward |
| `G2_classified` | `classification.json` valid: primary path + constraint set chosen | all analysis |
| `G3_financials` | Cleaned statements exist; adjustments applied; invested capital and EBIT restated | cost of capital, valuation |
| `G4_discount_rate` | Cost of capital fixed **and currency matches mandate currency** | any discounting |
| `G5_forecast` | Forecast passes consistency validator (growth/reinvestment/ROIC, terminal caps) | DCF execution |
| `G6_valued` | Equity bridge complete; value per share produced | challenge |
| `G7_challenged` | Critic ran; every high-severity finding resolved or explicitly disclosed | verdict |
| `G8_reconciled` | Verdict written with value vs price and margin of safety | report |

**Loopback rule.** When the critic raises a high-severity finding, the orchestrator reopens the
owning stage (only that stage and its dependents), increments `attempts`, and re-runs. Cap at
2 loopbacks per stage; on the third, the finding is disclosed in the report as an unresolved
risk rather than looping forever.

## 5. Contracts (abridged schemas)

Full schemas live in `contracts/`. Key shapes every builder must honor:

**classification.json**
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
  "overlays": ["intangible-heavy", "emerging-market", "multi-business", "has-real-options"],
  "constraints": [{"rule": "no-optimal-debt-ratio", "reason": "..."}],
  "confidence": "high|medium|low",
  "unresolved": ["what would change the routing"]
}
```

**cost-of-capital.json** — riskfree rate (with currency and derivation), ERP build-up, beta
(bottom-up components), cost of debt (rating route), weights, WACC, cost of equity, and a
`currency` field that MUST equal the mandate currency.

**forecast.json** — per-year drivers: revenue growth, operating margin, tax rate, sales-to-capital,
cost of capital; plus terminal block (growth, ROC, cost of capital) and failure block
(probability, proceeds basis).

**dcf-result.json** — per-year FCFF/FCFE table, PV, terminal value, operating asset value,
equity bridge line items, value per share, and a `sensitivity` block.

**challenge.json** — findings with `id`, `severity` (high|medium|low), `target_stage`,
`claim`, `evidence`, `suggested_fix`.

## 6. Agent roster

| Agent | Model | Owns | Reads | Writes |
|---|---|---|---|---|
| `valuation-orchestrator` | opus | state machine, routing, workspace, gates | everything | mandate.json, state.json |
| `financial-data-collector` | sonnet | gathering filings + market data | mandate | raw-financials, market-data, sources, gaps |
| `company-diagnostician` | opus | classification and routing | raw data, mandate | classification.json, diagnosis.md |
| `business-narrative-analyst` | opus | the story and its value drivers | raw data, classification | narrative.md, drivers.json |
| `financial-statement-analyst` | sonnet | statement cleanup and normalization | raw data, classification | cleaned-financials.json, adjustments.md |
| `cost-of-capital-analyst` | sonnet | discount rates | cleaned financials, market data, classification | cost-of-capital.json/.md |
| `intrinsic-valuation-analyst` | opus | forecast + DCF + bridge | cleaned, capital, drivers, classification | forecast.json, dcf-result.json, intrinsic.md |
| `relative-valuation-analyst` | sonnet | multiples and peers | cleaned, market data, classification | relative-result.json, relative.md |
| `special-situations-analyst` | opus | non-standard valuation paths | same as intrinsic + classification | writes intrinsic contracts |
| `capital-structure-analyst` | opus | how much debt, what kind | cleaned, capital, classification | capital-structure.json/.md |
| `payout-policy-analyst` | sonnet | dividends and buybacks | cleaned, capital | payout.json/.md |
| `investment-analyst` | opus | projects, acquisitions, synergy | project inputs, capital | investment.json/.md |
| `real-options-analyst` | opus | embedded optionality | classification, dcf, capital | real-options.json/.md |
| `valuation-critic` | opus | adversarial review | all analysis artifacts | challenge.json/.md |
| `investment-reconciler` | opus | verdict and report | everything | verdict.json, REPORT.md |

## 7. Skill roster

**Computation skills (ship Python, zero third-party dependencies):**

| Skill | Provides |
|---|---|
| `financial-statement-normalization` | lease capitalization, R&D capitalization, one-time cleanup, invested capital, FCFF/FCFE, ratio pack, normalized earnings |
| `cost-of-capital-toolkit` | riskfree derivation, ERP/CRP build-up, unlever/relever, bottom-up beta, synthetic rating, cost of debt, market value of debt, WACC, currency conversion, **optimal debt ratio schedule**, APV |
| `dcf-valuation-engine` | driver-based forecast, terminal value, failure adjustment, equity bridge, per-share, sensitivity, implied-expectations reverse solve |
| `relative-valuation-toolkit` | multiple computation, peer statistics, sector/market regression, intrinsic multiple derivation |
| `option-valuation-toolkit` | Black-Scholes, binomial, dilution-adjusted employee options, equity-as-call |
| `project-investment-analysis` | NPV/IRR/MIRR/PI/equivalent annuity, ROC/EVA, synergy valuation |
| `payout-policy-analysis` | FCFE vs cash returned, dividend matrix, sustainability |
| `special-situation-models` | distress adjustment, excess-return (financial services), total beta + illiquidity (private), cyclical normalization, young-firm revenue-driven build |
| `valuation-consistency-checks` | the cross-artifact validator (the feedback loop) |
| `monte-carlo-valuation` | distributional inputs, simulation, percentile outputs |

**Method skills (knowledge and procedure, no scripts):**

| Skill | Provides |
|---|---|
| `company-classification-routing` | the routing decision tree and per-branch constraint sets |
| `narrative-to-numbers` | survey → narrative → possible/plausible/probable → drivers → feedback loop |
| `valuation-red-team` | seven sins, bias diagnostics, failure gallery, implied-expectations attack |
| `financial-data-sourcing` | input inventory, where each comes from, fallbacks and defaults |
| `corporate-governance-analysis` | governance and marginal-investor assessment |
| `debt-design` | matching debt to assets: duration, currency, macro sensitivity |
| `valuation-reporting` | deliverable templates derived from the graded course projects |

## 8. Reference data

Damodaran's lookup tables are bundled as JSON in `cost-of-capital-toolkit/resources/data/`
with an explicit `as_of` field: synthetic rating tables (large, small/risky, financial),
country ERP and default spreads, US and global industry averages. Every consumer reads them
from a path passed in, so a refreshed table can be swapped without touching code. Skills
instruct agents to refresh from Damodaran's site when the data is more than a year stale and
to record the vintage used in the artifact.

## 9. Determinism boundary

For every stage, what is script versus judgment:

| Stage | Script computes | Agent judges |
|---|---|---|
| Statements | lease PV, R&D asset, invested capital, FCFF, ratios | which items are non-recurring, whether to capitalize, normalization basis |
| Cost of capital | rating lookup, spreads, levering, WACC, currency conversion | comparable set, ERP estimator, which riskfree derivation, gross vs net debt |
| Forecast | revenue path, margin fade, reinvestment, tax ramp, NOL burn | growth rate, target margin, sales-to-capital, convergence year |
| Terminal value | TV formula, reinvestment = g/ROC | terminal growth choice, terminal ROC, whether moat persists |
| Bridge | debt, cash, minorities, options, per-share | trapped cash haircut, cross-holding treatment |
| Relative | multiples, peer stats, regressions | comparable selection, which multiple, whether regression is usable |
| Capital structure | full WACC schedule, optimum, value effect | rating constraints, stress scenarios, speed of adjustment |
| Options | Black-Scholes, binomial | whether an option genuinely exists, volatility estimate |

## 10. Constraint catalogue (hard stops)

**The authoritative catalogue is Part III of `frameworks/special-situations-routing.md`** — 28
constraints with their exact trigger branches. The diagnostician compiles them into
`classification.json`; every downstream agent honors them; the critic verifies them.

The most consequential ones, abbreviated:

- `no-fcff-valuation` — financial service firms: debt is raw material, not financing. Use
  dividends or excess return; value equity directly.
- `no-optimal-debt-ratio` — financial service firms: regulatory capital governs; use the
  regulatory-capital approach instead.
- `no-earnings-multiple` — negative or trough earnings: PE and EV/EBIT are meaningless.
- `no-standard-growth-model` — negative earnings: growth must be built from revenue and
  target margin, not from an earnings growth rate.
- `require-failure-probability` — young or distressed firms: going-concern DCF alone
  overstates value; a failure branch is mandatory.
- `require-total-beta` — private company valued for an undiversified owner.
- `require-illiquidity-discount` — private company, unless the buyer is public and liquid.
- `require-normalized-earnings` — commodity or cyclical firms valued at a cycle extreme.
- `no-perpetual-growth-above-riskfree` — universal: terminal growth cannot exceed the
  riskfree rate in the valuation currency.
