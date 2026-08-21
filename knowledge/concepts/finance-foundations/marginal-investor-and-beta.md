# The Marginal Investor, the Market Portfolio and Beta

**Core idea:** Not all risk should be priced. The question is whose risk counts. Finance answers: the marginal investor's. That is the investor most likely to buy or sell on the next trade, and therefore the one who moves the price. Every risk and return model assumes this investor is well diversified. A well diversified investor has already averaged away firm-specific risk. The only risk left in their eyes is market risk, so only market risk belongs in the cost of equity. Push diversification to its limit — no transaction costs, all assets tradable — and every investor holds the same market portfolio, in proportion to market value. Investors then adjust risk not by changing that portfolio but by mixing it with a riskless asset. In that world an asset's risk is the risk it adds to the market portfolio, measured by its covariance with the market and standardized into beta.

**Formulas:**
- Beta: `β = Covariance(asset returns, market returns) / Variance(market returns)`. Beta measures the non-diversifiable risk of the asset. The market portfolio has a beta of 1 by construction.
- Expected return (CAPM): `E(R) = Riskfree rate + β × (E(R_market) − Riskfree rate)`. The bracketed term is the equity risk premium. Required return is a linear function of beta.
- Two-part investor choice: hold `w` in the market portfolio and `1 − w` in the riskless asset. `w > 1` means borrowing to buy more of the market portfolio.

**Procedure:**
1. Identify the marginal investor in the stock. Look for holders who own a large stake *and* trade actively. Both conditions are required.
2. Rule out large but inactive holders. A founder or manager with 30% who never trades is not marginal, however big the stake.
3. Ask whether that marginal investor is diversified. Institutional holders and active funds usually are. A closely held firm dominated by an undiversified founder is the case where the standard models fit worst.
4. If the marginal investor is diversified, price only market risk. Firm-specific risk goes into the expected cash flows, never into the discount rate.
5. Estimate beta as the covariance of the asset with the market divided by market variance, using a return history and a chosen market index.
6. Build the cost of equity as `riskfree rate + β × equity risk premium`, keeping the riskfree rate in the same currency as the cash flows.
7. Decide whether the CAPM is enough. If you need to relax its assumptions, choose from the three families below and be explicit about what you gained and what you gave up.

**Reference data:**

How the investor sets risk, given a market portfolio and a riskless asset:

| Preferred risk level | Allocation |
|---|---|
| No risk | 100% in T-Bills |
| Some risk | 50% in T-Bills, 50% in the market portfolio |
| More risk | 100% in the market portfolio |
| A risk hog | Borrow money and invest more than 100% in the market portfolio |

Families of alternatives to the CAPM:

| Family | What it does | Cost |
|---|---|---|
| Modified CAPM | Relaxes assumptions about transaction costs, taxes, or return distributions | More parameters, same single factor |
| Extended models | Allows several market risk factors. The arbitrage pricing model (APM) derives factors statistically and leaves them unnamed. Multifactor models use macroeconomic variables as stand-ins. | Factors must be estimated and may be unstable |
| Proxy models | Finds traits shared by stocks that earned high past returns and uses them as risk proxies. Fama-French uses market cap and book-to-price. | No theory behind the traits |

The history of risk measurement (Damodaran, Foundations of Finance Session 5):

| Date | Key event | Risk measure in use |
|---|---|---|
| Pre-1494 | Risk seen as fate or divine providence, alterable only by prayer or sacrifice | None or gut feeling |
| 1494 | Pacioli poses his puzzle about two gamblers in a coin-tossing game | — |
| 1654 | Pascal and Fermat solve it and lay the foundations of probability | Computed probabilities |
| 1662 | Graunt builds a life table from London births and deaths | — |
| 1711 | Bernoulli states the law of large numbers, the basis for sampling | Sample-based probabilities |
| 1738 | de Moivre derives the normal distribution; Gauss and Laplace refine it | — |
| 1763 | Bayes shows how to update prior beliefs with new information | — |
| 1800s | The insurance business develops actuarial measures from historical data | Expected loss |
| 1900 | Bachelier studies Paris stock and option prices and argues prices follow a random walk | Price variance |
| 1909-1915 | Standard Statistics Bureau, Moody's and Fitch begin rating corporate bonds | Bond and stock ratings |
| 1952 | Markowitz gives diversification a statistical basis and builds efficient portfolios | Variance added to a portfolio |
| 1964 | Sharpe and Lintner add a riskless asset and show that combinations of it and the market portfolio are optimal for all investors. The CAPM is born. | Market beta |
| 1960- | Models built on alternatives to the normal distribution: power law, asymmetric, and jump processes | — |
| 1976 | Ross derives the arbitrage pricing model from a no-arbitrage argument, with factors from historical data | Factor betas |
| 1986 | Macroeconomic variables tested as market risk factors, giving the multifactor model | Macroeconomic betas |
| 1992 | Fama and French conclude market cap and book-to-price beat beta as risk proxies | Proxies |

**Worked example:** A stock has a covariance with the market of 0.024 and the market's return variance is 0.020. Then `β = 0.024 / 0.020 = 1.2`. With a riskfree rate of 2% and an equity risk premium of 5%, the cost of equity is `2% + 1.2 × 5% = 8.0%`. That 8% is the rate at which you would discount the residual cash flows to equity. It is also the exact rate used in the Con Ed valuation, where `$4.00 × 1.02 / (0.08 − 0.02) = $68.00` per share.

**Determinism:**
- DETERMINISTIC: beta from covariance and market variance. Expected return from the riskfree rate, beta, and the equity risk premium. Portfolio allocations between the riskless asset and the market portfolio.
- JUDGMENT: identifying the marginal investor and deciding whether they are diversified. Choosing the market index and the estimation window for beta. Choosing the equity risk premium. Choosing among the CAPM and its alternatives. These need the shareholder register, trading volume by holder, a return history, and a view on which model's assumptions the situation violates least.

**Pitfalls:**
- Treating the largest shareholder as the marginal investor. Trading is required, and the largest holder often does not trade.
- Loading firm-specific risk into the discount rate. If the marginal investor is diversified, that risk is already gone and charging for it double-counts.
- Applying the CAPM to a closely held firm where the marginal investor is an undiversified owner. The model's central assumption fails.
- Assuming beta is stable. It is estimated from a history and moves with the index, the window, and the return interval chosen.
- Adopting a multifactor or proxy model because it fits the past better, without asking whether the factors mean anything.
- Forgetting that the market portfolio in theory holds *every* asset in the economy, while any index you use is a rough stand-in.

**Sources:**
- `foundations_of_finance--measuring_risk p.8-13`

**Related:** [[diversification-and-the-mean-variance-framework]], [[risk-definition-and-risk-aversion]], [[stable-growth-equity-valuation]], [[cost-of-capital]], [[equity-risk-premium]], [[bottom-up-beta]]
