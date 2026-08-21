# Diversification and the Mean-Variance Framework

**Core idea:** Risk averse investors demand a risk premium to hold risky assets. To turn that into a number, finance needs a risk measure that matches what investors dislike. The mean-variance framework supplies one. Variance measures the gap between actual and expected returns. A riskfree asset has zero variance, and higher variance means more risk. The framework assumes investors care about only two things: expected return and variance. That holds only if returns are normal, or if utility depends on nothing but mean and variance. The big payoff is diversification. Risk runs on a scale from firm-specific to market-wide. Holding many assets that are not perfectly correlated averages the firm-specific part away to nothing. The market-wide part stays.

**Formulas:**
- Two-asset portfolio variance: `σ²_p = w₁²σ₁² + w₂²σ₂² + 2w₁w₂ρ₁₂σ₁σ₂`. `w₁, w₂` = portfolio weights (summing to 1); `σ₁, σ₂` = standard deviations of the two assets' returns; `ρ₁₂` = correlation between the two assets' returns.
- Portfolio standard deviation: `σ_p = √(σ²_p)`.
- Number of correlations needed for an n-asset portfolio: `n(n−1)/2`. This is why the mechanical burden explodes as n grows.
- Total risk decomposition: `Total risk = Firm-specific (diversifiable) risk + Market (non-diversifiable) risk`. Only the second survives diversification.

**Procedure:**
1. Classify each risk you have identified on the firm-specific to market-wide scale. Ask how many firms it touches. A project missing its forecast touches one firm; a change in interest rates touches everything.
2. For each risk, decide who can shed it and how. A firm sheds project risk by holding many projects. It sheds rival risk by buying rivals, sector risk by spreading across sectors, and country risk by operating in many countries. No firm can shed market risk. An investor sheds firm, rival, and sector risk by holding many domestic stocks. Going global sheds country risk. Nothing sheds market risk except shifting across asset classes.
3. Compute portfolio variance from the weights, standard deviations, and correlations. Prove the benefit with numbers; do not assert it.
4. Add low-correlation assets first. The less an asset moves with the rest of the portfolio, the more risk it removes.
5. Stop when the marginal benefit dies. Each new asset cuts less risk than the last. Meanwhile the correlation count grows as `n(n−1)/2`.
6. Test the core assumption before leaning on it. Are returns skewed, fat-tailed, or prone to jumps? If so, mean and variance no longer sum up the distribution, and the framework will understate the risk that matters.

**Reference data:**

The risk scale and who can do what about it (Damodaran, Foundations of Finance Session 5):

| Risk source | Scope | Firm can reduce by | Investors can mitigate by |
|---|---|---|---|
| Projects do better or worse than expected | Firm-specific (one firm) | Investing in lots of projects | Diversifying across domestic stocks |
| Competition stronger or weaker than anticipated | Affects a few firms | Acquiring competitors | Diversifying across domestic stocks |
| Entire sector affected by an action | Affects a sector | Diversifying across sectors | Diversifying across domestic stocks |
| Exchange rate and political risk | Affects many firms | Diversifying across countries | Diversifying globally |
| Interest rates, inflation, news about the economy | Market (all investments) | Cannot affect | Diversifying across asset classes |

**Worked example:** Two stocks. Stock 1 has an average monthly return of 1.50% and a monthly standard deviation `σ₁ = 10%`. Stock 2 has an average monthly return of 2.50% and `σ₂ = 15%`. Their correlation is `ρ₁₂ = 0.20`. Hold them 50/50:

`σ²_p = (0.5)²(0.10)² + (0.5)²(0.15)² + 2(0.5)(0.5)(0.10)(0.15)(0.20)`
`= 0.0025 + 0.005625 + 0.0015 = 0.009625`
`σ_p = √0.009625 = 0.0981 = 9.81%`

The portfolio's standard deviation, 9.81%, is lower than either stock alone (10% and 15%), while its expected return is the weighted average, 2.00%. Nothing was given up. That free reduction in risk is the entire case for diversification, and it comes purely from the correlation being below 1. (Source: Damodaran, Foundations of Finance Session 5.)

**Determinism:**
- DETERMINISTIC: portfolio variance and standard deviation from weights, standard deviations, and correlations. Variance and correlation estimates from a return history. The `n(n−1)/2` correlation count.
- JUDGMENT: classifying a risk as firm-specific versus market-wide, which often is not obvious. Whether returns are close enough to normal for mean-variance to apply. Whether historical variances and correlations will hold going forward — correlations notoriously rise in crises, exactly when diversification is most needed. That judgment needs the return history, the distributional shape, and an understanding of what drives the co-movement.

**Pitfalls:**
- Believing diversification reduces all risk. It removes firm-specific risk only. Market-wide risk survives any amount of diversification.
- Applying mean-variance when returns are not normally distributed. The framework's justification is a strong assumption, not a fact.
- Using variance as the risk measure without checking whether investors care about anything else, such as skewness or downside deviation.
- Assuming historical correlations persist. The diversification benefit computed from calm-period correlations overstates what you get in a crisis.
- Adding assets that are highly correlated with what you already hold and calling it diversification.
- Confusing the *firm* diversifying (buying rivals, entering sectors) with the *investor* diversifying. Investors can do it more cheaply, which is why firm-level diversification rarely creates value on risk grounds alone.

**Sources:**
- `foundations_of_finance--measuring_risk p.2-7`

**Related:** [[marginal-investor-and-beta]], [[risk-definition-and-risk-aversion]], [[cost-of-capital]], [[equity-risk-premium]], [[finance-first-principles]]
