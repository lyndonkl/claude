# Corporate finance project blueprint (the 10-part deliverable)

**Core idea:** Damodaran's corporate finance project is a fixed, ordered ten-part analysis applied to one real publicly traded company, done in self-formed groups of 4-8 people over a 15-week semester. It is framed as a "live lab experiment": each principle is applied to a real firm as the class covers it. For an analysis system the blueprint is a *complete output template*. Every corporate-finance question about a firm gets covered exactly once — who controls it, who owns it, what it must earn, what it does earn, how it should be financed, how it should return cash, what it is worth. The order matters: each part consumes the outputs of the parts before it. Parts I, II, V and VIII lean qualitative; Parts III, IV, VI, IX and X are heavily quantitative; Part VII is mixed.

**Formulas:** No formula of its own. The blueprint is a dependency graph:
- Part III output (cost of equity, cost of debt, cost of capital) → input to Parts IV, VI, VII, X.
- Part VI output (optimal debt ratio, minimum WACC) → input to Part VII (how to get there) and Part X (discount rate in the growth phase).
- Part IX output (FCFE, cash that could have been returned) → input to Part VIII's recommendation and Part X's cash flows.

**Procedure:**
1. **Form the group and pick the firms.** Groups of 4-8; one company per member; a common (broadly defined) theme; maximum diversity inside the theme. See [[project-company-selection]] for the eligibility and exclusion rules.
2. **Part I — Corporate Governance Analysis.** Is there separation of ownership and management, and how responsive is management to stockholders? What other conflicts of interest exist? How does the firm interact with financial markets and how do markets get information about it? How does it view its social obligations and manage its image? (Class sessions 1-4. No spreadsheet. Data sets: CEO pay by firm (Forbes), Jensen's alpha by industry.) → [[governance-analysis-deliverable]]
3. **Part II — Stockholder Analysis.** Breakdown of holders into insiders, individuals and institutions; identify the *marginal investor* — the investor most likely to be trading and setting the price — because that determines whether risk is measured from a diversified perspective. (Session 5. Data sets: insider holdings by industry, institutional holdings by industry.) → [[stockholder-analysis-marginal-investor]]
4. **Part III — Risk and Return.** How much risk, from where (market/firm/industry/currency), and how is it changing? What return would a stockholder have earned, and did they beat the market — how much is attributable to management? How risky is the equity → cost of equity; how risky is the debt → cost of debt; what is the current cost of capital? (Sessions 6-11. Risk&Ret.xls. Data sets: betas by industry, Jensen's alpha by industry, cost of debt/capital by industry.) → [[regression-performance-diagnostics]], [[cost-of-capital-buildup-deliverable]]
5. **Part IV — Measuring Investment Returns.** Is there a typical project (life, investment needs, cash-flow pattern)? How good are the projects on the books — compare ROE to cost of equity and ROC to cost of capital (EVA)? Will future projects look like past ones? (Sessions 12-16. capbudg.xls. Data sets: ROE and equity EVA by sector, ROC and EVA by sector.) → [[return-spread-and-eva-analysis]]
6. **Part V — Capital Structure Choices.** What financing has been used and where does each instrument sit on the debt-equity continuum? How large are the advantages of debt for *this* firm? How large are the disadvantages? On this qualitative trade-off, is there too much or too little debt? (Session 17. Data sets: debt ratios by industry, trade-off variables by industry.) → [[qualitative-debt-tradeoff]]
7. **Part VI — Optimal Capital Structure.** Using the cost-of-capital approach, what debt ratio minimizes WACC? With reasonable constraints imposed, what would you actually recommend? Too much or too little debt relative to sector and to the market? (Sessions 18-19. capstru.xls, capstruo.xls. Data sets: earnings variance by industry, market debt ratio regression.) → [[optimal-debt-ratio-wacc-schedule]], [[recapitalization-value-and-stress-test]]
8. **Part VII — Mechanics of Moving to the Optimal.** Two decisions: *speed* (gradually or immediately) and *method* (alter the existing mix by buying back stock / retiring debt, or take new projects financed with debt or equity). Then the type of financing going forward: short vs long term, which currency, what special features — matching debt design to asset characteristics. (Sessions 20-21. macrodur.xls. Data set: firm value sensitivity by industry.) → [[debt-design-deliverable]]
9. **Part VIII — Dividend Policy.** How has the firm returned cash (dividends vs buybacks)? How much cash has it accumulated? Given its characteristics today, how should it return cash if it has excess? (Session 22. Data sets: yields/payout by industry, trade-off variables by industry.) → [[dividend-policy-deliverable]]
10. **Part IX — A Framework for Analyzing Dividends.** How much cash *could* the firm have returned (after reinvestment and debt payments) versus how much it *did* return? Given that and the cash balance, push it to return more or less? How does its policy compare to its peer group and the market? (Sessions 23-24. dividends.xls. Data sets: cap-ex ratios, working-capital ratios, debt ratios by industry.) → [[dividend-policy-deliverable]]
11. **Part X — Valuation.** Which growth pattern fits — stable, 2-stage or 3-stage — and how long does high growth last? What is the value of equity and how does it compare to market value? What is the *key variable* (risk, growth, leverage, margins…) driving the value? If hired to enhance value here, what path would you choose? (Session 25. Data sets: betas by industry, growth fundamentals by industry, cap ex and working capital by industry.) → [[two-stage-fcff-company-valuation]]
12. **Assemble** the executive summary scorecard on top of the ten parts → [[project-executive-summary-scorecard]].

**Reference data:**

Project time frame (the semester schedule as published; dates are illustrative of the pacing, not fixed calendar law):

| By week (date) | Done with |
|---|---|
| 1 (2/8) | Find a group |
| 2 (2/15) | Pick your firm; get data |
| 3 (2/22) | Corporate governance; stockholder analysis (Parts I-II) |
| 5 (3/14) | Risk and return (Part III) |
| 6 (3/28) | Measuring investment returns (Part IV) |
| 8 (4/11) | Capital structure choices (Part V) |
| 9 (4/18) | Optimal capital structure (Part VI) |
| 10 (5/1) | Mechanics of moving to the optimal (Part VII) |
| 12 (5/9) | Assess dividend policy (Part VIII) |
| 13 (5/11) | Framework for analyzing dividend policy (Part IX) |
| 13 (5/11) | Valuation (Part X) |
| 5/11, 5 pm | Whole project due |

Quantitative/qualitative weighting by part: I qualitative; II mostly qualitative; III quantitative; IV quantitative; V qualitative; VI quantitative; VII mixed; VIII balanced; IX quantitative; X quantitative.

**Worked example:** The Spring 2015 food-industry project covers Starbucks, McDonald's, Chipotle and Tyson Foods. It is a complete instance of this blueprint, part by part:

| Part | Table the 2015 team produced |
|---|---|
| I | Board/executive comparison vs peers; ISS QuickScores |
| II | Institutional and insider ownership percentages |
| III | Regression beta / alpha / R²; bottom-up levered beta; synthetic rating; WACC |
| IV | ROE, ROC, ROE−COE, ROC−WACC, EVA |
| V | EBITDA/value, revenue volatility, credit rating, institutional holdings |
| VI | WACC at debt ratios 10%-90%, optimum marked; hurdle rates at the optimum |
| VII | Duration and currency matching; fixed vs floating; sector EBIT sensitivities |
| VIII | Payout ratio and dividend yield vs industry and vs regression |
| IX | FCFE vs dividends + buybacks; cash returned / FCFE and / net income |
| X | Two-stage FCFF DCF; value per share vs market price |

**Determinism:** DETERMINISTIC — the *structure* itself (which sections exist, in which order, which prior output feeds which section, which spreadsheet and data set each part uses, the week-by-week schedule lookup) is fully mechanical and can be generated as a template. JUDGMENT — everything inside Parts I, V, VII and VIII, plus every input choice (growth period, constraints on the optimal ratio, marginal investor identification) inside the quantitative parts. A useful rule: the blueprint tells a script *what tables must exist*; the analyst supplies the assumptions that populate them.

**Pitfalls:**
- Doing the parts out of order. Part IV cannot be judged without Part III's hurdle rates; Part X's growth-phase WACC should reflect Part VI's optimal structure.
- Treating the qualitative parts (I, V, VIII) as optional filler — they set up the constraints that make the quantitative recommendations credible.
- Reporting Part VI's mechanical optimum as the recommendation without the "reasonable constraints" step the project explicitly requires.
- Skipping the "key variable" question in Part X — the project asks not just for a value but for what drives it and what a value-enhancer would do.

**Sources:**
- corporate_finance--project--cfproj p.1-14
- corporate_finance--project--food2015 p.2-18

**Related:** [[project-company-selection]], [[equity-valuation-project-blueprint]], [[governance-analysis-deliverable]], [[stockholder-analysis-marginal-investor]], [[cost-of-capital-buildup-deliverable]], [[return-spread-and-eva-analysis]], [[optimal-debt-ratio-wacc-schedule]], [[debt-design-deliverable]], [[dividend-policy-deliverable]], [[two-stage-fcff-company-valuation]], [[project-executive-summary-scorecard]]
