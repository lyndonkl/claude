# Finance Foundations — Concept Index

Distilled from Aswath Damodaran's *Foundations of Finance* sessions (NYU Stern): Introduction, Time Value of Money, Interest Rates, Inflation, Currencies & Exchange Rates, What is Risk, The Measurement of Risk, Valuing Bonds, Valuing Equity, and Option Pricing Basics. Reference data uses the most recent edition available in the source packets, with the year noted in each table.

## Concepts

| Slug | What it covers | Determinism |
|---|---|---|
| `finance-first-principles` | The six building blocks; the contractual / residual / contingent cash-flow taxonomy and which valuation machinery each gets; arbitrage and market frictions | MIXED — PV arithmetic deterministic, classification and forecasting judgment |
| `time-value-of-money-and-discount-rates` | Why a future dollar is worth less; the three drivers; the discount rate as opportunity cost; PV/FV mechanics and the aggregation principle | MIXED — discounting deterministic, choosing `r` judgment |
| `present-value-of-the-five-cash-flow-types` | Simple cash flow, annuity, growing annuity, perpetuity, growing perpetuity; closed forms, guard conditions, and how to decompose an asset | DETERMINISTIC formulas; JUDGMENT on decomposition, `g`, `r` |
| `compounding-frequency-and-effective-rates` | Stated versus effective annual rates; the discrete and continuous conversions; matching rate period to cash-flow period | DETERMINISTIC |
| `inflation-measurement-and-causes` | CPI, PPI, GDP deflator; basket and source biases; government incentive to understate; the three causes of inflation | MIXED — index arithmetic deterministic, index choice and credibility judgment |
| `real-vs-nominal-conversion` | Exact and approximate conversion of returns, growth rates, and cash flows; the compounding drag over long horizons | DETERMINISTIC conversions; JUDGMENT on the inflation estimate |
| `fisher-equation-and-intrinsic-riskfree-rate` | Nominal = real + expected inflation; intrinsic riskfree rate as inflation + real GDP growth; TIPS decomposition; the Fed Effect residual | DETERMINISTIC arithmetic; JUDGMENT on expectations and attribution |
| `yield-curve-and-growth-signals` | Curve shapes and slope measures; the maturity premium rationale; inversions; the weak continuous correlation between slope and later GDP growth | DETERMINISTIC spreads and correlations; JUDGMENT on what they predict |
| `currency-consistent-valuation` | Matching currency across numerator and denominator; riskfree rate from a government bond less sovereign default spread; the differential-inflation technique | DETERMINISTIC conversions; JUDGMENT on inflation and sovereign risk |
| `exchange-rate-forecasting-with-parity` | Interest rate parity and purchasing power parity; market forwards; why not to embed personal currency views | DETERMINISTIC parity formulas; JUDGMENT on inflation inputs and method choice |
| `risk-definition-and-risk-aversion` | Two-sided risk; Knight's risk/uncertainty split and why Damodaran rejects it; certainty equivalents; the St. Petersburg paradox; behavioral quirks | MIXED — expected values deterministic, preferences judgment |
| `diversification-and-the-mean-variance-framework` | Variance as the risk measure and its assumptions; the firm-specific to market-wide risk scale; two-asset portfolio variance; correlation and marginal benefit | DETERMINISTIC variance math; JUDGMENT on risk classification and normality |
| `marginal-investor-and-beta` | Who the marginal investor is and why only their risk is priced; the market portfolio; beta from covariance; CAPM; alternatives; the history of risk measures | DETERMINISTIC beta and expected return; JUDGMENT on the investor and the premium |
| `bond-valuation-and-yield-to-maturity` | Pricing a fixed-rate bond as annuity plus face value; solving for YTM; current yield; par relationships; floating-rate bonds | DETERMINISTIC pricing and YTM; JUDGMENT on default-free status |
| `interest-rate-risk-and-bond-propositions` | Convexity; maturity raises sensitivity; lower coupon raises sensitivity; repricing under symmetric rate shocks | DETERMINISTIC |
| `default-risk-and-default-spreads` | Default spread by rating; pricing promised cash flows at riskfree plus spread; the investment-grade cliff; extracting market-implied spreads | DETERMINISTIC given a rating; JUDGMENT on assigning the rating |
| `equity-vs-firm-valuation` | The direct (FCFE at cost of equity) and indirect (FCFF at cost of capital, less debt) routes; the four determinants of DCF value; the consistency identity | DETERMINISTIC PV mechanics; JUDGMENT on all four determinants |
| `cost-of-capital` | Cost of equity for the marginal investor; today's long-term cost of debt; the interest tax shield; market-value weights | DETERMINISTIC weighted average; JUDGMENT on component costs |
| `stable-growth-equity-valuation` | Gordon growth on dividends versus FCFE; potential versus actual payout; comparing intrinsic value with market price | DETERMINISTIC formula; JUDGMENT on `g`, `r`, and the numerator |
| `option-payoffs-and-value-determinants` | Calls, puts, American versus European; payoff and breakeven; the six determinants and the direction of each effect | DETERMINISTIC payoffs; JUDGMENT on identifying real options and volatility |
| `replicating-portfolio-and-binomial-model` | Replication and the arbitrage argument; the three preconditions; backward induction for delta, borrowing, and value; limiting distributions | DETERMINISTIC backward induction; JUDGMENT on tree construction |
| `black-scholes-and-put-call-parity` | The five-input closed form; `N(d1)` as delta; the dividend adjustment; deriving the put from parity; the `N(d)` table | DETERMINISTIC given inputs; JUDGMENT on `σ`, `y`, and `t` |

## How these fit together

The area has a spine and three branches off it.

The spine is present value. Start with `finance-first-principles`, which sets the frame: classify the cash flow, then pick the machinery. Next comes `time-value-of-money-and-discount-rates`, on why discounting exists and what a discount rate contains. Then `present-value-of-the-five-cash-flow-types` supplies the closed forms that make discounting practical. Finally `compounding-frequency-and-effective-rates` makes sure the rate and the cash-flow period agree. Nothing downstream works if these four are wrong.

The first branch builds the discount rate. `inflation-measurement-and-causes` and `real-vs-nominal-conversion` fix the price-level basis. `fisher-equation-and-intrinsic-riskfree-rate` turns that into a riskfree rate. It also gives a fundamentals-based check on the market rate. `yield-curve-and-growth-signals` tells you which maturity to take the rate from, and how much to read into the curve's shape. Are the cash flows in another currency? Then `currency-consistent-valuation` and `exchange-rate-forecasting-with-parity` move the whole apparatus over without breaking the inflation match.

The second branch builds the risk premium. First, `risk-definition-and-risk-aversion` establishes that risk is two-sided and that people demand payment for bearing it. Then `diversification-and-the-mean-variance-framework` shows that most of that risk disappears in a portfolio. Last, `marginal-investor-and-beta` decides whose remaining risk gets priced and turns it into a number. Together with the riskfree rate from the first branch, these produce a cost of equity.

The third branch applies the spine to the three cash-flow types. Contractual: `bond-valuation-and-yield-to-maturity`, then `interest-rate-risk-and-bond-propositions` for rate exposure and `default-risk-and-default-spreads` for credit. Residual: `equity-vs-firm-valuation` picks the route, `cost-of-capital` supplies the discount rate, and `stable-growth-equity-valuation` handles the mature case and the terminal stage of every other case. Contingent: `option-payoffs-and-value-determinants` confirms the claim is really an option, `replicating-portfolio-and-binomial-model` shows where the value comes from, and `black-scholes-and-put-call-parity` gives the closed form.

## Order of use on a real company

1. Classify the claim you are valuing (`finance-first-principles`).
2. Choose the currency and the nominal/real basis (`currency-consistent-valuation`, `real-vs-nominal-conversion`).
3. Set the riskfree rate at the right maturity in that currency (`fisher-equation-and-intrinsic-riskfree-rate`, `yield-curve-and-growth-signals`).
4. Identify the marginal investor and build the cost of equity (`marginal-investor-and-beta`, `diversification-and-the-mean-variance-framework`).
5. Add the cost of debt from the firm's rating and blend to a cost of capital (`default-risk-and-default-spreads`, `cost-of-capital`).
6. Forecast cash flows on the matching route and decompose them into standard shapes (`equity-vs-firm-valuation`, `present-value-of-the-five-cash-flow-types`).
7. Discount, terminate with a stable-growth stage, and compare with the market price (`stable-growth-equity-valuation`).
8. Value any contingent claims separately and add them (`option-payoffs-and-value-determinants`, `black-scholes-and-put-call-parity`).
