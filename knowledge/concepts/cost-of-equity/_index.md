# Cost of equity — concept index

Determinism flag: **D** = mostly deterministic given named inputs; **M** = mixed (deterministic arithmetic wrapped around judgment inputs); **J** = mostly judgment.

| Slug | What it covers | Determinism |
|---|---|---|
| [[riskfree-rate-fundamentals]] | What makes a rate riskfree; duration and currency matching; 10-year convention; the Euro "lowest sovereign rate" rule; real rates and TIPS | D |
| [[currency-riskfree-rate]] | Stripping the sovereign default spread out of a local government bond rate; three ways to estimate that spread; inflation build-up and differential-inflation routes; what to do when no default-free entity exists | D |
| [[riskfree-rate-normalization]] | Whether to replace a low rate with a normalized one (no); intrinsic riskfree rate = inflation + real growth; the Fed effect; negative rates and internal consistency | J |
| [[equity-risk-premium-basics]] | What the ERP is; sanity checks; the three estimation families (survey, historical, implied); survey data; why premiums move | M |
| [[historical-equity-risk-premium]] | US and global historical premiums; period / T.Bill-vs-T.Bond / arithmetic-vs-geometric choices; standard errors; survivorship bias | D |
| [[implied-equity-risk-premium]] | The full forward-looking ERP computation; base cash flow from dividends + buybacks; growth and terminal-growth rules; solving for r; 2008, 2009, 2013, 2020, 2021 and Sensex worked cases | M |
| [[choosing-an-equity-risk-premium]] | Which premium to use given your market beliefs; predictive-power evidence; the directional valuation bias; the ERP ≈ 2 × Baa spread cross-check | J |
| [[country-risk-premium]] | Three ways to get a CRP (default spread, relative equity volatility, melded); the four-step Jan 2021 estimation template; the country ERP lookup table; PRS scores | M |
| [[operation-weighted-erp]] | Location-based vs operation-based country risk; revenue-, production-, and region-weighted company ERPs; Embraer, Ambev, Coca Cola, Shell, Disney, Vale, Tata | D |
| [[lambda-country-risk-exposure]] | Lambda as a firm-specific loading on country risk; revenue-based and return-regression-based estimation; the five ways to attach country risk to a cost of equity | M |
| [[capm-cost-of-equity]] | The CAPM and its logic; marginal investor and diversification; APM, multi-factor and proxy alternatives; model-evaluation criteria; the cost of equity as a hurdle rate | M |
| [[alternative-relative-risk-measures]] | The two-question grid for choosing a relative risk measure; relative volatility, proxy models, CAPM Plus, accounting betas, cost-of-debt-based models | J |
| [[regression-beta]] | Running and diagnosing a beta regression; standard error, R², confidence ranges, adjusted beta; the GoPro / Nokia / GameStop / Bombardier / Vale failure cases | D |
| [[jensen-alpha]] | The regression intercept as performance; benchmark Rf(1−β); per-period and annualized alpha; what alpha does and does not say | D |
| [[beta-determinants]] | Product discretionary-ness, operating leverage (two measures), financial leverage; the leverage schedule's convexity; sanity-checking a beta against the business | M |
| [[levering-and-unlevering-beta]] | Unlever/relever formulas; debt-beta variant; cash correction; gross vs net debt; market value of debt; merger and portfolio betas | D |
| [[bottom-up-beta]] | The five-step comparable-firm beta procedure; value weights from EV/Sales; divisional betas and debt allocation; banks; Vale, Disney, Embraer, Tata, Baidu, Deutsche Bank | M |
| [[non-traded-asset-betas]] | Betas for private firms, divisions and IPOs; median-not-mean comparables; assuming the industry median market D/E; accounting betas | M |
| [[total-beta]] | Scaling a market beta to total risk for undiversified owners; Total beta = beta / sqrt(R²); when to use it and when not | D |
| [[cost-of-equity-assembly]] | Putting the three inputs together under the currency / claim-type / nominal-real consistency rules; currency conversion by differential inflation; divisional hurdle rates; Embraer, Vale, Disney end to end | M |

## How these fit together

An analyst works through this area in a fixed order, and the order matters because each step constrains the next.

**Start with the currency of the cash flows.** That determines the riskfree rate. [[riskfree-rate-fundamentals]] gives the instrument choice; [[currency-riskfree-rate]] handles every currency without a default-free issuer, which is most of them; [[riskfree-rate-normalization]] settles the recurring argument about whether today's low or negative rate is usable (it is, provided growth and inflation assumptions move with it).

**Then price market risk.** [[equity-risk-premium-basics]] frames the three estimation families. [[historical-equity-risk-premium]] and [[implied-equity-risk-premium]] are the two serious ones, and [[choosing-an-equity-risk-premium]] decides between them — the course default is the current implied premium, 4.72% for mature markets on 1 January 2021. If the company touches risky countries, [[country-risk-premium]] converts a sovereign rating into an additional premium, [[operation-weighted-erp]] attaches it in proportion to where the company actually does business rather than where it is registered, and [[lambda-country-risk-exposure]] refines the exposure measure further when revenue weights are too crude.

**Then measure relative risk.** [[capm-cost-of-equity]] establishes why beta is the measure at all, which rests on the marginal investor being diversified; [[alternative-relative-risk-measures]] is the menu when that assumption fails. [[regression-beta]] shows how the standard estimate is built and why it should not be trusted on its own, with [[jensen-alpha]] extracting the regression's second output. [[beta-determinants]] explains what a beta ought to look like given the business. [[bottom-up-beta]] is the production method, and it depends on [[levering-and-unlevering-beta]] for its unlever/relever mechanics. Two special cases branch off: [[non-traded-asset-betas]] for private firms and divisions, and [[total-beta]] for owners who are not diversified.

**Finish by assembling.** [[cost-of-equity-assembly]] combines riskfree rate, premium, and beta under the consistency rules, converts across currencies where needed, and produces the divisional rates that become project hurdle rates. Its output is the equity leg of the cost of capital, which is where this area hands off to the cost-of-debt and capital-structure areas.

## Scope note

The assigned page ranges span more than this area's focus. Pages covering the DCF framework and discounting consistency (valpacket1 p.1-20), cost of debt, synthetic ratings, capital-structure weights and WACC assembly (valpacket1 p.100-115; cfpacket1 p.184-200), cash flow estimation and earnings adjustments (valpacket1 p.116-120), and the objective function / corporate governance material (cfpacket1 p.41-77) belong to the `cost-of-debt-capital`, `dcf-cashflows-growth`, `capital-structure`, `accounting-statements`, and `governance-objective` areas. Where those pages feed a cost of equity directly — the discounting-consistency principle, the cost-of-capital assembly for Embraer and Disney, the marginal-investor and hurdle-rate framing — they are cited in the concepts above.
