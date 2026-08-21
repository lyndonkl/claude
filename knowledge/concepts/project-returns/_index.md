# project-returns — concept index

Measuring investment returns: earnings versus cash flows, accounting versus cash-flow returns, incremental cash flow principles, NPV/IRR mechanics and conflicts, consistency rules, uncertainty, options, acquisitions, and post-mortems. Twenty concepts.

| Slug | Covers | Determinism |
|---|---|---|
| investment-analysis-first-principles | The corporate finance map; the Return Mantra (time-weighted, incremental, cash flow); what counts as a project; the four running cases | JUDGMENT framework, DETERMINISTIC decision rules |
| time-value-and-cash-flow-timing | Discounting/compounding for the five standard cash flow patterns; annuity and perpetuity formulas; Time-0 and start-of-year timing conventions | DETERMINISTIC |
| earnings-vs-cash-flows | Accrual-to-cash bridge; depreciation tax shield; growth vs maintenance capex; working capital; straight-line vs accelerated depreciation; Rio Disney income statement and FCFF | DETERMINISTIC math, JUDGMENT forecasts |
| accounting-returns-roc-roe-eva | ROC/ROIC, ROE, return spreads, EVA; ROIC distortions and fixes; global spread distribution; returncalculator.xls adjustment engine | DETERMINISTIC ratios, JUDGMENT normalization |
| incremental-cash-flow-principle | Sunk costs, allocated costs, fixed/variable G&A regression; adjustment route vs direct route; ex-ante policing of sunk costs | DETERMINISTIC math, JUDGMENT labeling |
| npv-and-irr-mechanics | NPV and IRR definitions, decision rules, NPV profiles; Rio Disney $3,296M / 12.60%; usage surveys | DETERMINISTIC |
| npv-vs-irr-conflicts | Multiple IRRs, scale and timing conflicts, reinvestment assumption, MIRR, profitability index, capital rationing | DETERMINISTIC computation, JUDGMENT rule choice |
| comparing-projects-different-lives | Why raw NPVs are incomparable across lives; project replication; equivalent annuities | DETERMINISTIC |
| terminal-value-and-project-life | Salvage vs terminal value; steady-state terminal cash flow; growth-versus-reinvestment consistency table; finite vs infinite trade-off | DETERMINISTIC formula, JUDGMENT life and g |
| currency-and-inflation-consistency | Same-currency, same-basis rule; PPP exchange-rate paths; discount-rate conversion; Rio Disney in reais; when currency risk earns no premium | DETERMINISTIC |
| equity-side-project-analysis | ROE vs cost of equity; loan amortization; cash flow to equity; equity NPV and IRR — the Vale Labrador mine | DETERMINISTIC given assumptions |
| project-hurdle-rate-selection | Matching the rate to claimholder, business, geography and currency; divisional rates; total beta for private firms; Rio Disney 8.46%, Netflix Fit 8.01% | DETERMINISTIC arithmetic, JUDGMENT inputs |
| uncertainty-payback-sensitivity-simulation | Payback and discounted payback; sensitivity and break-evens; Monte Carlo simulation; the hedging decision tree | DETERMINISTIC tools, JUDGMENT use |
| opportunity-costs-and-side-costs | Pricing owned resources; excess capacity framework; cannibalization; Disney Rio land $33M; Bookscape adjusted NPV | DETERMINISTIC math, JUDGMENT identification |
| project-synergies | Valuing side benefits explicitly at the receiving business's rate — Bookscape café, Netflix Fit, Tata/Harman | DETERMINISTIC math, JUDGMENT existence |
| acquisitions-as-projects | Target-risk discounting; normalizing the base year; stand-alone value + synergy = ceiling price; Harman case | DETERMINISTIC math, JUDGMENT normalization |
| project-options | Options to delay (call), expand (call), abandon (put); when a negative NPV is not a rejection; Disney California Adventure | JUDGMENT identification, DETERMINISTIC once inputs set |
| assessing-existing-investments | Post-mortem (chance vs bias diagnostics); liquidate/terminate/divest/continue ladder; DCA 2008 decision | DETERMINISTIC ladder, JUDGMENT re-forecasts |
| capital-budgeting-model | capbudg.xls engine: full input map, DDB schedule, salvage handling, NPV/IRR/ROC outputs, quirks to replicate | DETERMINISTIC |
| netflix-fit-case | The full worked case tying the whole area together, with the instructor's solution and class dispersion | DETERMINISTIC model, JUDGMENT assumptions |

## How these concepts connect

An analyst works this area in a fixed order. Start with the framing in [[investment-analysis-first-principles]], which fixes the objective and the Return Mantra, and with [[time-value-and-cash-flow-timing]], which fixes the conventions everything else obeys. Then build the numerator. Convert accounting earnings into cash flows with [[earnings-vs-cash-flows]], strip the stream to what is truly incremental with [[incremental-cash-flow-principle]], charge the side costs from [[opportunity-costs-and-side-costs]], credit the side benefits from [[project-synergies]], and close the stream with [[terminal-value-and-project-life]]. In parallel, build the denominator: [[project-hurdle-rate-selection]] matches the rate to claimholder, business, geography and currency, and [[currency-and-inflation-consistency]] guarantees the verdict does not depend on which currency or nominal/real basis you chose.

With both halves in hand, run the tests. [[accounting-returns-roc-roe-eva]] is the quick screen and the standard measure for existing investments; [[equity-side-project-analysis]] is the same machinery run from the equity investors' side when the project carries its own financing. [[npv-and-irr-mechanics]] is the primary test. When projects compete, [[npv-vs-irr-conflicts]] and [[comparing-projects-different-lives]] govern the ranking. Then stress the answer: [[uncertainty-payback-sensitivity-simulation]] finds the break-evens and the downside, and [[project-options]] adds the value of flexibility before anything marginal is rejected. The same toolkit prices deals in [[acquisitions-as-projects]] and re-evaluates live assets in [[assessing-existing-investments]].

Two notes anchor the practice. [[capital-budgeting-model]] is the scriptable engine that automates the mechanical middle of the sequence. [[netflix-fit-case]] is the integrated rehearsal — one project that requires nearly every concept above and ends, honestly, in a marginal answer.
