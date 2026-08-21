# dcf-cashflows-growth — concept index

DCF inputs on the numerator side: turning reported accounting into usable cash flows, estimating growth, and closing the valuation with a terminal value. 19 concepts.

| Slug | What it covers | Determinism |
|---|---|---|
| reported-to-actual-earnings | Update (trailing 12-month), cleanse (financial/capital/non-recurring expenses), normalize; the one-time-charge rule; the six accounting-malfeasance red flags | MIXED — TTM and charge annualization deterministic; expense classification and "is it really one-time" are judgment |
| operating-lease-capitalization | Full procedure: PV lease commitments at the pre-tax cost of debt, create the counter-asset, adjust EBIT and debt; The Gap worked end to end; the 2019 IFRS/GAAP change | DETERMINISTIC given the commitment schedule, cost of debt and asset life |
| rnd-capitalization | Full procedure: research asset, amortization, EBIT/net income/capital/cap-ex adjustments; the untaxed add-back; industry amortization-life table; SAP worked | MIXED — mechanical given the life; choosing the life is judgment |
| normalizing-depressed-earnings | Five causes of negative or abnormally low earnings and the two treatment paths: dollar or return-based normalization vs revenue-driven forecasting to a target | MIXED — arithmetic deterministic; diagnosis and window are judgment |
| tax-rate-and-nols | Effective vs marginal, the consistency requirement with the after-tax cost of debt, convergence paths, the full NOL waterfall | MIXED — NOL waterfall and convergence deterministic; rate choice is judgment |
| net-capital-expenditures | Net cap ex, adding capitalized R&D and normalized acquisitions, three stable-growth estimators, sector cap-ex ratios; Cisco 1999 worked | MIXED — formulas deterministic; normalizing acquisitions and the estimator choice are judgment |
| non-cash-working-capital | The valuation definition, forecasting as a percent of revenues, negative working capital; Amazon/Cisco/Motorola judgment calls | MIXED — measurement deterministic; the forecast ratio is judgment |
| fcff | Three equivalent pathways, the reinvestment rate, where the interest tax shield lives; Disney FY2013 worked | DETERMINISTIC given cleansed inputs |
| fcfe | Full and stable-leverage definitions, equity reinvestment rate, cash-flow-statement routes, the bank/regulatory-capital version, leverage and FCFE; global FCFE-vs-payout data | DETERMINISTIC given inputs; the debt-ratio assumption is judgment |
| historical-growth | Arithmetic vs geometric, period and metric sensitivity, negative bases, the scaling effect, extrapolation dangers; Motorola, Callaway, Time Warner | MIXED — all statistics deterministic; period/metric choice and interpretation are judgment |
| analyst-growth-estimates | Forecast-accuracy evidence, All-America analysts, the five deadly sins, the three propositions, herding vs noise | JUDGMENT — retrieval and dispersion are deterministic, use is not |
| fundamental-growth-equity | g = retention x ROE and the non-cash net income version; changing-ROE efficiency term; ROE = ROC + leverage spread; Wells Fargo, Coca-Cola, Brahma, Titan, Deutsche Bank, Tata | DETERMINISTIC given accounting inputs; sustainability of the return is judgment |
| fundamental-growth-operating | g = reinvestment rate x ROC, the changing-ROC efficiency term, the derivation, four sustainability worries; Cisco vs Motorola, Disney | DETERMINISTIC given inputs; target ROC and representativeness are judgment |
| return-on-invested-capital | ROIC definition, the six ways it misleads, marginal ROIC, and the reverse check on the implied perpetual ROC | MIXED — computation deterministic; the six corrections are judgment |
| value-of-growth | Growth creates value only above the cost of capital; the five-firm table; the ROC-vs-g sensitivity grid; price of growth vs value of growth | DETERMINISTIC arithmetic; the ROIC on new investment is judgment |
| top-down-revenue-growth | The three-step route for money-losers and changing margins: revenue path, target-margin convergence, sales-to-capital reinvestment; Airbnb, Tesla, market-share sizing | MIXED — the table is deterministic; every driver is judgment |
| fcff-forecast-engine | The full reference implementation: fades for growth/margin/tax/WACC, NOLs, terminal value, failure probability, equity bridge, options, diagnostics; SK Innovation worked | DETERMINISTIC — a pure function from ~25 inputs to a per-share value (two circularities need iteration) |
| terminal-value | Growth cap and riskfree consistency, growth-period length and moats, stable reinvestment = g/ROC, perpetual ROC, internal consistency; Disney, Heineken, Deutsche Bank, Baidu | MIXED — formulas deterministic; g, ROC, N and the mature-firm inputs are judgment |
| dcf-case-valuations | Five complete valuations — Disney (3-stage FCFF, plus a restructured re-run), Vale (normalized single-stage FCFF), Tata Motors (2-stage FCFE in rupees), Baidu (changing-margin FCFF), Deutsche Bank (DDM 2008, regulatory-capital FCFE 2016) | DETERMINISTIC given each assumption set; model and growth-period choice are judgment |

## How these connect, and the order an analyst uses them

The numerator of a DCF is built in four passes.

**Pass 1 — get honest earnings.** Start with `reported-to-actual-earnings`: update to trailing-12-month numbers, then run the two mechanical cleansings, `operating-lease-capitalization` and `rnd-capitalization`, which change operating income, debt and invested capital together. Strip one-time items and screen for aggressive accounting. If the current year is unrepresentative or negative, `normalizing-depressed-earnings` decides whether to normalize (transient or cyclical causes) or to abandon current earnings entirely and forecast from revenues (life-cycle, leverage or structural causes). Then apply `tax-rate-and-nols` to get after-tax operating income.

**Pass 2 — get reinvestment.** `net-capital-expenditures` and `non-cash-working-capital` together define reinvestment. Both must be adjusted for the same capitalizations made in Pass 1, and neither can be assumed independently of growth.

**Pass 3 — assemble the cash flow.** `fcff` and `fcfe` are the two cash-flow definitions and the two discount-rate pairings. Which one you actually discount, at what rate, with how many growth stages, is decided in the sibling area (`[[dcf-model-choice-framework]]`, `[[equity-versus-firm-valuation]]`, `[[dividends-versus-fcfe]]`, `[[growth-pattern-and-stage-count]]`).

**Pass 4 — get growth, then close.** Growth comes from three sources, in ascending order of reliability: `historical-growth` (a starting point, badly behaved off negative or small bases), `analyst-growth-estimates` (an input, not an answer), and fundamentals — `fundamental-growth-equity` for EPS and net income, `fundamental-growth-operating` for EBIT. Both fundamental routes rest on `return-on-invested-capital`, whose six measurement distortions must be checked before any growth rate built on it is trusted. `value-of-growth` is the test that decides whether the growth you just estimated is worth anything: only growth earning more than the cost of capital creates value. When earnings are negative or margins are changing, the fundamental equations break and `top-down-revenue-growth` replaces them with revenues, a target margin and a sales-to-capital ratio. `terminal-value` closes the valuation, and it is where the growth cap, the perpetual return and the `g/ROC` reinvestment discipline all bind at once.

**Reference implementations.** `fcff-forecast-engine` is the assembled machine — every concept above occupies one slot in it — and `dcf-case-valuations` shows the same machine run five different ways on five real companies, which is the fastest way to see which assumptions actually move the answer.

## Scope note

The page-note files read for this area also contain material owned by neighbouring areas, deliberately not duplicated here:
- **Discount rates** (regression and bottom-up betas, cost of debt and synthetic ratings, equity risk premiums, cost of capital) — valpacket1spr21 p.81-115 / valpacket1spr20 p.81-112.
- **Model choice and the post-DCF loose ends** (equity vs firm valuation, dividends vs FCFE, growth patterns, cash, cross holdings, complexity discounts, defining debt, employee options, the equity bridge) — valpacket1spr21 p.211-240 / valpacket1spr20 p.207-240 -> the `dcf-model-choice-loose-ends` area.
- **Dividend policy** (the dividend matrix, cash-trust assessment, peer-group and regression payout benchmarks, managing a dividend cut, the Disney/Vale/Tata/BP/Limited payout cases) — cfpacket2spr20 p.201-223 -> the `dividend-policy` area. This area covers only the FCFE machinery those analyses consume.

Cross-area references appear as wiki-style links to those areas' slugs (e.g. `[[bottom-up-beta]]`, `[[cost-of-capital]]`, `[[synthetic-rating]]`, `[[equity-value-bridge]]`, `[[dividends-versus-fcfe]]`).

An earlier, incomplete pass at this area was moved to `../_superseded-dcf-cashflows-growth-earlier-run/`; its files are superseded by the 19 above.
