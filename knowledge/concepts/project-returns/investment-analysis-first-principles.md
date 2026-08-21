# Investment analysis first principles

**Core idea:** Corporate finance has one objective: maximize the value of the business. Three decisions hang off it. The investment decision takes assets that earn more than a risk-adjusted hurdle rate. The financing decision picks the right kind and mix of debt. The payout decision returns cash the firm cannot invest above the hurdle rate. The investment decision has two halves. The *hurdle rate* must reflect the riskiness of the investment and the debt/equity mix funding it. The *return* must reflect the magnitude and timing of the cash flows plus all side effects. Everything in project analysis elaborates the return half. The operating summary is the Return Mantra: **time-weighted, incremental cash flow return**. Use cash flows rather than earnings, since you cannot spend earnings. Count only cash flows that occur *as a consequence* of the decision. Weight earlier cash flows more than later ones. A "project" is far broader than a factory. It covers strategic entries into new businesses or markets. It covers acquisitions of other firms, which are projects too, despite the habit of judging them under separate and looser rules. It covers new ventures inside existing businesses, changes in how an existing venture is run, and even the choice of how best to deliver an internal service. Essentially every choice a firm makes can be framed as an investment.

**Formulas:**
- Decision rule (firm perspective): accept if `NPV > 0`, equivalently if `IRR > cost of capital`, equivalently if `ROC > cost of capital`, where ROC = after-tax operating income / book value of capital.
- Decision rule (equity perspective): accept if `equity NPV > 0`, `equity IRR > cost of equity`, or `ROE > cost of equity`, where ROE = net income / book value of equity.
- Return Mantra: `Project return = f(incremental cash flows, timing of those cash flows, all side effects)`.

**Procedure:**
1. Define the project precisely: what is being bought/built/changed, over what life, and what would happen if the firm did *not* do it. The counterfactual defines "incremental."
2. Decide the claimholder perspective — whole firm (cash flows to the firm, cost of capital) or equity only (cash flows after debt payments, cost of equity). Never mix. See [[project-hurdle-rate-selection]].
3. Forecast earnings for the project (revenues, operating expenses, depreciation, taxes at the *marginal* rate). See [[earnings-vs-cash-flows]].
4. Convert earnings to cash flows: add back non-cash charges, subtract capital expenditures and working-capital investment.
5. Strip out non-incremental items (sunk costs, fixed allocated costs) and add in side costs and side benefits (opportunity costs, cannibalization, synergies). See [[incremental-cash-flow-principle]], [[opportunity-costs-and-side-costs]], [[project-synergies]].
6. Close the cash flows: salvage value for a short finite life, terminal value for a long/infinite life. See [[terminal-value-and-project-life]].
7. Time-weight: discount at the matched hurdle rate to get NPV and IRR. See [[npv-and-irr-mechanics]].
8. Stress the answer for uncertainty and interactions with other projects; add option value where the project embeds delay/expand/abandon rights. See [[uncertainty-payback-sensitivity-simulation]], [[project-options]].
9. Decide, then revisit: apply the same machinery to existing investments as a post-mortem and a keep/expand/divest test. See [[assessing-existing-investments]].

**Reference data:** Four running examples used throughout the Damodaran corporate finance investment-analysis section (2020 packet vintage):

| Example | What it is | Analytical issue it raises |
|---|---|---|
| Rio Disney | Disney's first theme parks in South America (Magic Kingdom + Epcot Rio near Rio de Janeiro) | Emerging-market country risk, currency, sunk costs, allocated G&A, long life/terminal value |
| Vale Labrador mine | New iron ore mine in Western Labrador, Canada, 8M tons capacity | Equity-side analysis, commodity-price and exchange-rate sensitivity, excess capacity |
| Bookscape Online | Online store extension for a privately held bookstore | Private-firm total beta, project-specific hurdle rate, side costs, café synergy |
| Tata Motors / Harman | Indian automaker's cross-border bid for a US high-end audio maker | Acquisition as a project, target's risk not acquirer's, synergy valuation |
| Netflix Fit (2020 case) | Netflix entering equipment-plus-subscription fitness (Peloton model) | Full end-to-end worked case: sunk R&D, allocated G&A, excess studio capacity, synergy, finite vs infinite life |

**Worked example:** Rio Disney end-to-end (all figures $ millions, 2020 packet). Accounting earnings give a 10-year average return on capital of 4.18%, below the 8.46% Brazil-adjusted theme-park cost of capital — a naive reject. Three adjustments convert this to incremental cash flows: add back the $500 sunk pre-project investment, remove its $18/yr depreciation tax shield, and add back the non-incremental two-thirds of allocated G&A. Adding a year-10 terminal value of $11,275 then gives NPV = +$3,296 at 8.46% and IRR = 12.60% — accept. The gap between the two verdicts is entirely the Return Mantra at work: cash flows not earnings, incremental not total, time-weighted over the project's true (perpetual) life rather than an arbitrary 10-year window.

**Determinism:** DETERMINISTIC — once cash flows, hurdle rate, and life are fixed, every decision measure (NPV, IRR, ROC, ROE, payback) and the accept/reject verdict follow mechanically. JUDGMENT — defining the counterfactual (what is truly incremental), choosing the claimholder perspective, choosing project life, and deciding whether a listed side effect is real. That judgment needs: the firm's existing cost structure (which costs are fixed), competitive context (would cannibalized sales be lost anyway), and the strategic rationale (which future options the project opens).

**Pitfalls:**
- Treating acquisitions as a separate species of decision with their own looser rules; they are projects and take the same NPV test.
- Judging returns to capital against a cost of equity (or vice versa) — a claimholder mismatch.
- Using company-wide hurdle rates for a project whose risk, geography, or currency differ.
- Using earnings as if they were spendable cash.
- Letting a long-lived project's average accounting return over an arbitrary 10-year window drive the decision.

**Sources:**
- corporate_finance--lecture_slides--cfpacket1spr20 p.205-207
- corporate_finance--lecture_slides--cfpacket1spr20 p.209-212
- corporate_finance--lecture_slides--cfpacket1spr20 p.283
- corporate_finance--lecture_slides--cfpacket1spr20 p.332

**Related:** [[earnings-vs-cash-flows]], [[incremental-cash-flow-principle]], [[npv-and-irr-mechanics]], [[project-hurdle-rate-selection]], [[accounting-returns-roc-roe-eva]], [[acquisitions-as-projects]], [[netflix-fit-case]], [[cost-of-capital]], [[bottom-up-beta]]
