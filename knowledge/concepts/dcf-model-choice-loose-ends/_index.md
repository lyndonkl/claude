# dcf-model-choice-loose-ends — concept index

Area scope: choosing the right DCF model (which cash flow, which discount rate, which growth pattern, how many stages), and the loose ends between operating-asset value and value per share.

| Slug | What it covers | Determinism |
|---|---|---|
| dcf-model-choice-framework | The three building blocks of any DCF — cash flow, discount rate, growth pattern — and the canonical model variants they generate | MIXED (formulas deterministic; model selection judgment) |
| equity-versus-firm-valuation | Equity (dividends/FCFE at cost of equity) versus firm (FCFF at WACC); stable-leverage rule, partial-information rule | MIXED (both routes deterministic; leverage classification judgment) |
| dividends-versus-fcfe | The 80%/110% five-year payout screen, the bank exception, the private-firm/IPO exception | MIXED (screen deterministic; estimability judgment) |
| discount-rate-cash-flow-matching | Claimholder, currency and real-versus-nominal matching; the 10% inflation switch; growth/riskfree consistency | MIXED (classification and Fisher conversion deterministic; inflation view judgment) |
| growth-pattern-and-stage-count | Stable / 2-stage / 3-stage selection at the `g_econ + 10%` thresholds; tying growth length to competitive advantage; stable-phase parameter targets | MIXED (screens and stable-phase formulas deterministic; moat assessment judgment) |
| multistage-model-mechanics | How 1-, 2- and 3-stage models are wired: linear transition ramps, cumulative discounting, terminal reinvestment from `g/ROC` | DETERMINISTIC given inputs (inputs themselves judgment) |
| ddm-fcfe-reconciliation | Why a DDM and an FCFE model differ, and the cash-buildup term that reconciles them exactly | DETERMINISTIC (return on retained cash is judgment) |
| fcff-fcfe-reconciliation | Why firm and equity valuations agree exactly under constant market-value leverage, and what breaks the identity | DETERMINISTIC (target debt ratio and ROC are judgment) |
| equity-value-bridge | The full chain from operating assets to value per share, with the open question at each link | DETERMINISTIC arithmetic; every component estimate is judgment |
| cash-in-valuation | Keeping cash and its interest income out of the operating valuation; gross-debt versus net-debt approaches; multiple distortion | MIXED (both approaches deterministic; operating-cash split judgment) |
| marginal-value-of-cash | When $1 of cash is worth less or more than $1; the ROIC test; the $0.75/$1.00/$1.25 evidence; closed-end funds and Berkshire | MIXED (closed-end-fund discount deterministic; deployment risk judgment) |
| cross-holdings | Three accounting categories; the three-step sum-of-the-parts; the price-to-book approximation; Yahoo worked both ways | MIXED (aggregation deterministic; each holding's value judgment) |
| other-non-operating-assets | What may be added (overfunded pensions, unutilized assets) and what may never be (brand, goodwill, operating PP&E) | JUDGMENT (arithmetic trivial) |
| complexity-discount | The complexity experiment, disclosure-page proxy, weighted complexity score, and the PBV regression price of opacity | MIXED (score and regression deterministic; answers and adjustment judgment) |
| defining-debt-for-cost-of-capital | The three-part debt test; include interest-bearing debt and all leases, exclude payables | DETERMINISTIC classification (hybrids and lease discount rate judgment) |
| debt-and-other-claims-in-the-bridge | Book versus market value of debt, going concern versus liquidation, pension underfunding, contingent liabilities, minority interests | MIXED (arithmetic deterministic; frame and probabilities judgment) |
| restricted-stock-and-future-grants | Past restricted stock into the share count; expected future grants as a percent-of-revenue expense | MIXED (mechanics deterministic; grant path judgment) |
| employee-option-per-share-approaches | Diluted share count versus treasury stock versus option value drag, and why the drag method brackets the other two | DETERMINISTIC given option values |
| valuing-employee-options | Dilution-adjusted Black-Scholes, the four caveats, vesting and tax adjustments, and what magnifies the drag | DETERMINISTIC given inputs (volatility, effective maturity, vesting judgment) |
| model-choice-case-studies | Con Ed (stable DDM), 3M (two-stage FCFF, pre- and post-crisis), S&P 500 (two-stage DDM), plus breakeven-growth cross-checks | DETERMINISTIC valuations; model choice and inputs judgment |

## How these connect, and the order to use them

The area splits into two halves that an analyst meets in sequence.

**Half one — pick the model.** Start at `dcf-model-choice-framework`, which names the three choices. Resolve them in order. `equity-versus-firm-valuation` decides the claimholder. `dividends-versus-fcfe` decides the equity cash-flow measure if you went the equity route. `discount-rate-cash-flow-matching` locks the denominator to the numerator on claimholder, currency and inflation basis. `growth-pattern-and-stage-count` sets the number of stages and the stable-phase parameters where most of the value lives. `multistage-model-mechanics` then tells you how to wire the structure you chose. Its transition ramps and cumulative discounting separate a correct implementation from a plausible-looking wrong one. Two reconciliation notes act as unit tests on the finished model. `fcff-fcfe-reconciliation`: firm and equity routes must agree under constant market-value leverage. `ddm-fcfe-reconciliation`: a DDM matches an FCFE model only if retained cash earns the cost of equity. `model-choice-case-studies` shows the whole first half exercised on three real subjects.

**Half two — finish the job.** `equity-value-bridge` is the spine: it lists every adjustment between operating-asset value and value per share, and each remaining concept is one link in it. Work down the bridge in order. Add cash (`cash-in-valuation`, then `marginal-value-of-cash` if you want to charge a discount or premium). Add stakes in other firms (`cross-holdings`). Add genuinely uncounted assets and refuse the double counts (`other-non-operating-assets`). Consider an opacity adjustment at firm level (`complexity-discount`). Subtract debt, defined by the three-part test (`defining-debt-for-cost-of-capital`) and valued correctly for the frame you are in (`debt-and-other-claims-in-the-bridge`, which also covers pensions, contingent liabilities and minority interests). Subtract equity claims (`employee-option-per-share-approaches`, priced by `valuing-employee-options`), and handle grants yet to be made as an operating expense (`restricted-stock-and-future-grants`). Then divide by actual shares.

The two halves are linked by one recurring discipline: every adjustment must be made exactly once. Cash counted in the flows and added back, pension shortfalls in the WACC and in the bridge, option value subtracted alongside diluted shares, brand value on top of brand-driven margins — each is the same error in a different costume.
