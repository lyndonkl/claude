# CAPM and the structure of a cost of equity

**Core idea:** Every risk-and-return model answers two questions: how do you measure risk, and how do you convert that measure into a premium? The CAPM answers both. Risk is variance of actual returns around expected returns. Part of that variance is firm-specific and diversifiable, so it earns no reward; only the non-diversifiable part is priced. The CAPM assumes the **marginal investor** — the one most likely to trade next and therefore to set the price — is well diversified, and that with no transactions costs everyone holds the market portfolio. An asset's risk is then the risk it adds to that portfolio, measured by beta, and the expected return is linear in beta. The result is the standard cost of equity: riskfree rate plus beta times the equity risk premium.

**Formulas:**
- **Cost of Equity = Riskfree Rate + Beta × Equity Risk Premium.**
- CAPM: E(R) = R_f + β × (E(R_m) − R_f), where E(R_m) − R_f is the market/equity risk premium.
- Beta = Covariance(asset returns, market returns) / Variance(market returns).
- General risk-adjusted form: Cost of Equity = Riskfree rate in the currency of analysis + Relative risk of the equity × Equity Risk Premium for average-risk equity.
- APM (arbitrage pricing): E(R) = R_f + Σ_j β_j × (R_j − R_f), with β_j = exposure to unspecified statistical factor j from a factor analysis.
- Multi-factor: same algebra as APM, but the factors are specified macroeconomic variables and the betas come from regressions.
- Proxy models: E(R) = a + Σ_j b_j × Y_j, where Y_j are firm characteristics (size, book-to-market, momentum) and b_j are regression coefficients.
- Hurdle rate framing: Hurdle rate = Riskless rate + Risk premium.

**Procedure:**
1. **Establish who the marginal investor is.** A marginal investor must both hold a lot of the stock and trade it regularly. The largest holder is not necessarily marginal — a founder who never sells (Ellison at Oracle, Zuckerberg at Facebook) is not setting the price. Use institutional and insider holdings to classify (table below).
2. If the marginal investor is diversified, only market risk is priced, and a beta-based model is appropriate. If not, move to total risk — see [[total-beta]] and [[alternative-relative-risk-measures]].
3. **Pick the three CAPM inputs**: current riskfree rate ([[riskfree-rate-fundamentals]]), equity risk premium ([[equity-risk-premium-basics]]), beta ([[bottom-up-beta]]).
4. Compute the cost of equity. Match its currency and nominal/real basis to the cash flows.
5. Interpret it two ways, both valid: for an investor it is the return required to break even given the risk; for management it is the minimum acceptable return on equity-funded projects — the equity hurdle rate.
6. Apply the decision rule: if your forecast return exceeds the CAPM required return, the stock is undervalued and you buy. If a project's expected equity return falls short of the divisional cost of equity, reject it.
7. Sort risk into the right place. Only economic, macro, continuous risk belongs in the cost of equity. Estimation risk, micro/firm-specific risk, and discrete risks (an FDA rejection, a nationalization) belong in the expected cash flows or are diversified away.

**Reference data:**

Competing models and what each needs:

| Model | Expected return | Inputs required |
|---|---|---|
| CAPM | R_f + β(R_m − R_f) | Riskfree rate; beta vs the market portfolio; market risk premium |
| APM | R_f + Σβ_j(R_j − R_f) | Riskfree rate; number of factors; betas vs each factor; factor risk premiums |
| Multi-factor | R_f + Σβ_j(R_j − R_f) | Riskfree rate; specified macro factors; betas vs those factors; macro risk premiums |
| Proxy | a + Σb_j Y_j | Proxy variables; regression coefficients |

Identifying the marginal investor from ownership structure:

| % held by institutions | % held by insiders | Marginal investor |
|---|---|---|
| High | Low | Institutional investor |
| High | High | Institutional investor, with insider influence |
| Low | High (founder/manager) | Hard to tell — insiders only if they trade; otherwise individual investors |
| Low | High (wealthy individual) | Wealthy individual investor, fairly diversified |
| Low | Low | Small individual investor with restricted diversification |

Ownership of the running case companies (supporting the diversified-marginal-investor assumption):

| Holder type | Disney | Deutsche Bank | Vale (pref) | Tata Motors | Baidu (Class A) |
|---|---|---|---|---|---|
| Institutions | 70.2% | 40.9% | 71.2% | 44% | 70% |
| Individuals | 21.3% | 58.9% | 27.8% | 25% | 20% |
| Insiders | 7.5% | 0.2% | 1.0% | 31% (Tata Sons) | 10% |

Five criteria for a good risk-and-return model: (1) a risk measure that applies to all assets; (2) a clear split between rewarded and unrewarded risk, with a rationale; (3) standardized measures, so an investor can tell above-average from below-average risk; (4) a translation from risk into a required rate of return; (5) power to explain past returns *and* predict future ones.

Risk continuum, from most diversifiable to least: project-specific surprises → competitive surprises affecting the firm and a few rivals → sector-wide effects → exchange-rate and political risk → interest rates, inflation, and economy-wide news (pure market risk).

**Worked example (Disney, November 2013):** Beta 1.25 (regression estimate), riskfree rate 2.75% (10-year US T.Bond), equity risk premium 5.76% (operation-weighted, not the raw US 5.50%).

Cost of equity = 2.75% + 1.25 × 5.76% = **9.95%**.

To an investor, 9.95% is the long-run return to expect if Disney is correctly priced and the CAPM holds; a research view of 12.5% expected return therefore says buy. To Disney's managers, 9.95% is the hurdle every equity-funded project must clear, and failing to deliver it destroys shareholder value.

**Determinism:**
- DETERMINISTIC: (R_f, β, ERP) → cost of equity; (return series) → covariance, variance, beta; (holdings data, thresholds) → marginal-investor classification via the table.
- JUDGMENT: whether the marginal investor really is diversified; which model to use (CAPM versus APM versus multi-factor versus proxy); every one of the three CAPM inputs; how to split a company's risks between the cash flows and the discount rate.

**Pitfalls:**
- Assuming the largest shareholder is the marginal investor. Marginality requires trading, not just holding.
- Putting firm-specific, discrete, or estimation risk into the discount rate. It belongs in expected cash flows, which are probability-weighted across good and bad scenarios.
- Believing the CAPM's empirical record is strong. It is not: the beta-return relationship is weak, and size and price-to-book explain returns better. Damodaran's defense is pragmatic — it works about as well as the next-best alternative, and the richer models' advantage in explaining the past fades when predicting the future.
- Adding multiple betas and factor premiums for a company where the answer barely differs from CAPM. The added complexity and data burden rarely pay.
- Managing the firm to lower its beta. Beta drops come from making products less discretionary, cutting fixed costs, or cutting leverage — all real business changes. Taking good investments is the goal; a low beta is not.
- Living in a strict mean-variance world when investors visibly care about skewness and downside — two investments with identical mean and standard deviation are not identical if one can lose 100% and the other 50%.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.20-26
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.20-26
- corporate_finance--lecture_slides--cfpacket1spr20 p.76-96, p.98, p.144-146

**Related:** [[alternative-relative-risk-measures]], [[regression-beta]], [[bottom-up-beta]], [[equity-risk-premium-basics]], [[riskfree-rate-fundamentals]], [[cost-of-equity-assembly]], [[total-beta]], [[hurdle-rate]]
