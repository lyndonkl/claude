# Valuing employee options (dilution-adjusted Black-Scholes)

**Core idea:** Employee options can be valued with a standard option pricing model, but four features of these options strain the standard assumptions. They are long term, so constant variance and constant dividend yield are shakier. They cause dilution, because exercise creates new shares rather than transferring existing ones. They are frequently exercised early, which makes a European model dangerous. And they cannot be exercised before the employee vests. The practical fix is a dilution-adjusted Black-Scholes. Feed the model a stock price marked down for the shares that exercise would create. Shorten the maturity to reflect early exercise. Then scale the result by the odds of vesting. The output is a per-option value that goes straight into the equity bridge.

**Formulas:**
- Dilution-adjusted stock price (circular — solve iteratively):
  `S_adj = (S × N_shares + C × N_options) / (N_shares + N_options)`, where C is the call value from the model.
- Black-Scholes call: `C = S_adj × e^{−yT} × N(d₁) − K × e^{−rT} × N(d₂)`
  with `d₁ = [ln(S_adj/K) + (r − y + σ²/2)T] / (σ√T)` and `d₂ = d₁ − σ√T`.
  S_adj = dilution-adjusted stock price; K = strike (average exercise price); T = maturity in years (average, shortened for early exercise); σ = annualized standard deviation of the stock price; r = riskless rate; y = dividend yield; N(·) = standard normal CDF.
- Total option claim: `Value of options = C × Number of options outstanding`.
- Vesting adjustment: `Adjusted value = C × Number of options × Probability of vesting`.
- Tax adjustment: `After-tax option cost = Value of options × (1 − marginal tax rate)`.
- Per share: `Value per share = (Equity value − Value of options) / Actual shares outstanding`.

**Reference data — what raises the option drag:**

| Driver | Effect on the per-share hit |
|---|---|
| Strike price low relative to the stock price | Larger |
| Long maturity | Larger |
| High stock volatility | Larger |
| Repricing / reset provisions (strike reset downward after a price fall) | Larger still — value transfers from shareholders to option holders |

Four caveats and their partial fixes:

| Caveat | Fix |
|---|---|
| Long-term options: constant variance and dividend yield are unrealistic | Use a model allowing shifting variance |
| Options cause dilution | Use the dilution-adjusted stock price above |
| Early exercise is common | Use a model allowing early exercise, or shorten T |
| Cannot exercise before vesting | Multiply the value by the probability the employee vests |

**Procedure:**
1. Gather the option footnote: number outstanding, average exercise price, average remaining maturity, and vesting terms.
2. Estimate volatility from the stock's history, adjusted for expected changes as the firm matures.
3. Shorten the maturity from contractual life to expected life to reflect early exercise.
4. Solve the dilution-adjusted price and the call value together as a fixed point: guess C, compute S_adj, recompute C, repeat. Convergence is fast.
5. Multiply the per-option value by the number of options outstanding.
6. Multiply by the probability of vesting if a material share of the options is unvested.
7. If exercise creates a tax deduction for the firm, multiply by (1 − marginal tax rate).
8. Subtract the result from equity value and divide by actual shares ([[employee-option-per-share-approaches]]).

**Worked example A (XYZ):** Inputs: stock price $10, adjusted for dilution to **$9.58**; strike $10; maturity 10 years (reducible for early exercise); standard deviation 40%; riskless rate 4%. Model output: N(d₁) = 0.8199, N(d₂) = 0.3624.
`C = 9.58(0.8199) − 10 × e^{−0.04×10}(0.3624) = **$5.42** per call.`
With 10 million options, the total claim is $54.2m. Equity of $1,000m less $54.2m leaves $945.8m; divided by 100 million actual shares → **$9.46 per share**, against $10.00 before the grant.

**Worked example B (the Amazon-vintage `fcffgen` option sheet):** Inputs: stock price $84; strike $13.375; maturity 8.4 years; volatility 50%; dividend yield 0%; T-bond rate 6.5%; 38 million warrants; 340.79 million shares. The circular solve converges to `S_adj = (84 × 340.79 + 76.104 × 38)/378.79 = 83.208`. Then `d₁ = 2.3628`, `N(d₁) = 0.99093`, `d₂ = 0.9136`, `N(d₂) = 0.81954`, and `C = 83.208 × 0.99093 − 13.375 × e^{−0.546} × 0.81954 = 76.104`. Total option value = 76.104 × 38 = **$2,891.9m**, subtracted from equity of $15,692.3m before dividing by 340.79 shares → **$37.56 per share**.

**Determinism:**
- DETERMINISTIC: the Black-Scholes value given S, K, T, σ, r and y; the dilution fixed-point solve; the tax and vesting multiplications; the resulting per-share value.
- JUDGMENT: volatility, effective (as opposed to contractual) maturity, the probability of vesting, whether variance will shift over a ten-year option's life, and whether the firm can reprice. This needs the option footnote, historical volatility, employee turnover data, and the plan documents.

**Pitfalls:**
- Using the unadjusted stock price, which overstates the option value by ignoring dilution.
- Using contractual maturity for options that will be exercised in half that time.
- Applying a European model to options that are routinely exercised early.
- Valuing only vested options, or valuing all options as if vesting were certain. Both are wrong; use a probability.
- Tax-adjusting when exercise creates no deduction for the firm.
- Forgetting that a repricing provision converts a worthless option back into a valuable one, at shareholders' expense.

**Sources:**
- valpacket1spr21 p.249-250, p.252, p.254
- valpacket1spr20 p.245-246, p.248, p.250
- focussed-fcff (fcffgen.xls, "Option Valuation" sheet)

**Related:** [[employee-option-per-share-approaches]], [[restricted-stock-and-future-grants]], [[equity-value-bridge]], [[multistage-model-mechanics]], [[real-options-in-valuation]], [[convertible-bond-valuation]]
