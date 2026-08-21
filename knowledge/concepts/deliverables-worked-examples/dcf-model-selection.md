# Choosing the DCF model (FCFE vs FCFF, 2-stage vs 3-stage vs n-stage)

**Core idea:** Before any DCF is built, two choices must be made and defended: which cash flow to discount, and how many growth stages to use. The cash-flow choice turns on leverage. Discount FCFE when leverage is low and stable; discount FCFF when leverage is expected to change materially. The stage choice turns on the growth path. Use two stages when growth steps down once, three stages when growth needs to taper through a transition, and an n-stage model with an explicit year-by-year growth path when earnings are negative and growth must be modelled to a target. Every worked valuation in the equity valuation project opens with a paragraph justifying both choices, and that paragraph is a required part of the deliverable.

**Formulas:**
- FCFE = cash flow available to equity after reinvestment and debt payments; discount at the cost of equity to get equity value directly.
- FCFF = EBIT × (1 − t) − Reinvestment; discount at WACC to get firm value, then subtract debt to get equity value.
- Expected growth (fundamental) = Reinvestment rate × Return on capital (for FCFF) or Retention ratio × Return on equity (for FCFE).
- Two-stage: high growth for n years, then stable growth forever.
- Three-stage: high growth, then a transition phase where growth and beta taper, then stable growth.
- n-stage: an explicit declining growth path (e.g. 24% down to 8% over five years), then stable growth.

**Procedure:**
1. **Check leverage.** Little or no debt with stable leverage → FCFE. Leverage expected to move toward an industry-average D/E → FCFF. Shifting leverage with moderate growth → two-stage FCFF.
2. **Check the earnings sign.** Negative earnings → n-stage FCFF with a target growth path taken from analyst estimates.
3. **Choose the number of stages** from the growth path. A single step down → two stages. A need to taper earnings gradually to terminal growth, or a beta that must migrate to 1 → three stages, with a transition period of roughly five years.
4. **Choose the growth rate source, in order of preference:** fundamentals (reinvestment × return) first; historical growth only when the history is meaningful; analyst consensus as a cross-check. When earnings have only recently turned positive, historical rates are unusable and fundamentals should be used, even if that means being more conservative than the analysts.
5. **Handle accounting distortions before valuing.** Capitalise R&D when R&D spending is significant. Normalise earnings when the latest year is unrepresentative.
6. **Set stable-phase parameters:** beta drifting to 1.0 (or 1.2 where risk stays above average), a stable growth rate at or below the economy's growth rate, a stable debt ratio, and a reinvestment rate consistent with the stable ROC.
7. **Handle taxes in loss-making firms.** Set the tax rate to 0% while losses persist, because net operating losses shield income, and to the marginal rate once the firm is profitable.
8. **Watch for a cash-distorted beta.** A large cash balance depresses the observed beta; assume it drifts toward 1 as the cash is deployed into operations.
9. **Write the justification paragraph** naming the model, the reason, and the accounting adjustments made.

**Reference data:** Model choices and full assumption sets from the six-company equity valuation project (ca. 2003).

| Firm | Model | Reason given |
|---|---|---|
| Affiliated Computer Services | 2-stage FCFF | Best suited to firms with shifting leverage growing at a moderate rate |
| Apple | 2-stage FCFE | Historically very little debt; R&D capitalised; last year's earnings normalised |
| Biosite | 3-stage FCFE | Stable leverage plus high growth; transition needed as beta drifts to 1 |
| Gundle Environmental | 3-stage FCFF | High growth needing a taper; D/E assumed to reach the industry average, so FCFF not FCFE |
| Infosys | 2-stage FCFF | Analysts predict >15% growth for 5 years, then a sustainable 5% perpetual rate |
| Nextel Partners | n-stage FCFF | Negative earnings; target growth path from analyst estimates; also valued as an option |

Assumption tables as filed:

| Assumption | ACS high / stable | Apple high / stable | Biosite high / stable |
|---|---|---|---|
| Length of growth period | 5 / forever | 10 / forever | 5 / forever |
| Growth rate | 10.00% / 3% | 15% / 4% | 14.97% / 4.5% |
| Debt ratio | 11.51% / 16.00% | 0 / 0 | D/E 10.60% / 6.93% |
| Beta | 1.27 / 1 | 2.15 / 1.2 | 0.56 / 1 |
| Risk-free rate | 4.3% | 4.4% | 4.21% |
| Risk premium | 4.53% | 4.1% | 4.53% |
| Cost of debt | 6.55% | — | — |
| Tax rate | 35% | 35% | 38% |
| Return on capital / equity | ROC 11.27% / 8.83% | ROE 13% / 15% | ROC 14.60% / 7% |
| Reinvestment rate | 56.61% / 37.04% | 15% / 30.77% | 100% / 20% |
| Cost of equity | 10.03% / 8.83% | 13.21% / 9.31% | 6.75% / 8.74% |
| Cost of capital | 9.37% / 8.10% | — | — |

| Assumption | Gundle high / stable | Infosys high / stable | Nextel high / stable |
|---|---|---|---|
| Length of growth period | 6 / forever | 5 / forever | 5 / forever |
| Growth rate | 10.0% / 3% | 17.23% / 5% | declining 24%→8% / 4.75% |
| Debt ratio | 7.67% / 42.53% | 0 / 5.5% | 39% / 39% |
| Beta | 0.55 / 1 | 2.09 / 1.2 | 3.93 / 1.00 |
| Risk-free rate | 4.5% | 5.5% | 4.4% |
| Risk premium | 4.5% | 4% | 4.0% |
| Cost of debt | 5.5% | 6.25% | 15.9% / 7.6% |
| Tax rate | 35% | 35% | 0% / 40% |
| Return on capital | 11.73% / 10.67% | 28.12% / 15% | −19.71% / 8.10% |
| Reinvestment rate | 80.0% / 28.12% | 61.27% / 33.3% | 100% / 100% |
| Cost of equity | — | 13.86% / 10.3% | 20.12% / 8.39% |
| Cost of capital | — | 13.86% / 9.96% | 18.57% / 8.10% |

DCF outputs:

| Firm | Firm value | Equity value | Value/share | Market price | Verdict |
|---|---|---|---|---|---|
| ACS | $7,640.96m | $6,734.72m | $48.75 | $50.50 | Slightly overvalued |
| Apple | — | $5,400m (incl. $4,545m cash and securities) | $27.06 | $20.85 | Undervalued |
| Biosite | — | $487.96m | $32.76 | $26.12 | Undervalued |
| Gundle | $509,549k | $490,891k | $41.13 | $19.73 | Undervalued |
| Infosys | Rs 29,114 crore | Rs 29,088 crore | Rs 4,270 | Rs 4,912 | Overvalued |
| Nextel Partners | $2,525m | $1,026m (debt $1,706m) | $11.08 | $11.72 | Slightly overvalued |

**Worked example:** Biosite, a rapid medical diagnostics company. A 3-stage FCFE model was chosen because leverage is stable and growth is high. The growth rate is the sticking point: analysts said 28%, historical rates were unusable because earnings had only recently turned positive, so a *fundamental* growth rate of 14.97% was used instead, deliberately conservative. High growth was limited to five years, after which risk transitions toward average (beta → 1) and growth mimics the economy at 4.5%. Capital spending stays high throughout because the business depends on research and new products, so the high-growth reinvestment rate is 100%. Biosite's observed beta of 0.56 was judged artificially low — partly the low Medical Supply industry beta, but mostly its large cash balance — so beta was assumed to drift to 1 as cash funds new projects. Result: $32.76 per share against a $26.12 market price.

**Determinism:** DETERMINISTIC — once the assumption table is fixed, every DCF output follows: cash flows, present values, terminal value, firm value, equity value, value per share. The leverage test (is D/E stable?) and the earnings-sign test are mechanical. JUDGMENT — the model choice itself, the length of the growth period, which growth-rate source to trust, whether to capitalise R&D or normalise earnings, whether an observed beta is distorted by cash, and where the stable-phase parameters land. These need the competitive narrative, the analyst consensus, the R&D history and the cash balance.

**Pitfalls:**
- Using FCFE for a firm whose leverage is about to change materially. Gundle's D/E moves from 7.67% to a 42.53% industry-average target; FCFE would misprice that.
- Taking analyst growth rates uncritically when earnings only just turned positive.
- Leaving the tax rate at the marginal rate for a firm with large loss carryforwards. Nextel uses 0% during losses and 40% in stability.
- Failing to capitalise significant R&D. Apple's research asset is worth over $1.1bn and is a third of its invested capital.
- Accepting a low beta from a cash-rich firm at face value.
- Letting a valuation be dominated by a balance-sheet item without saying so. Apple's $4,545m of cash and marketable securities dominates its $5,400m equity value.

**Sources:**
- valuations--projects--eqprojspr19 p.4
- valuations--projects--valproject2 p.2, p.5, p.8, p.11, p.13, p.18

**Related:** [[equity-valuation-project-blueprint]], [[dcf-sensitivity-analysis]], [[two-stage-fcff-company-valuation]], [[equity-as-call-option-valuation]], [[valuation-triangulation-and-recommendation]], [[value-of-control-and-synergy]]
