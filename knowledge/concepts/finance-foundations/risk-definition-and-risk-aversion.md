# Defining Risk and Measuring Risk Aversion

**Core idea:** Risk in finance must be defined as two-sided. Dictionaries define it as "exposing to danger or hazard," but if risk were purely negative the rational response would be to avoid it entirely, and no business would exist. Risk produces good and bad outcomes, and the decision to take it or avoid it turns on whether the upside outweighs the downside. Frank Knight's 1921 split — quantifiable uncertainty is "risk," unquantifiable uncertainty is "uncertainty" — is a distinction Damodaran considers misplaced. Measurable risk is easier to insure, but finance must price all uncertainty, measurable or not. All of this matters for valuation because of risk aversion. People will not pay the expected value for a risky bet. The gap between what a bet is worth in expectation and what they will actually pay is what a risk premium compensates.

**Formulas:**
- Certainty equivalent measure of risk aversion: `Risk aversion = Expected value of the gamble − Certainty equivalent`. The certainty equivalent (CE) is the sure amount a person treats as equally good as the risky bet. A larger gap means greater risk aversion; a zero gap means risk neutrality; a negative gap means risk seeking.
- Risk aversion coefficient: if utility is written as a function of wealth, `U(W)`, the risk aversion coefficient measures how much utility is gained or lost as wealth is added or subtracted. Diminishing marginal utility of wealth is the root of risk aversion.
- St. Petersburg gamble expected value: with probability `1/2^n` of reaching stage n and a payoff of `2^(n−1)`, each stage contributes `$0.50`, and the sum over infinite stages diverges. Expected value = infinite.

**Procedure:**
1. State the risk two-sidedly. Write down both the upside and the downside outcomes of the exposure, not just the loss scenarios. A one-sided description of risk leads to a one-sided decision.
2. Refuse the Knightian escape. If a risk cannot be quantified precisely, that is not a reason to leave it out of the valuation. Estimate it roughly and say so.
3. Decide whose risk aversion matters. In valuing a business, it is the marginal investor's, not the founder's and not yours.
4. Elicit or infer the certainty equivalent when you need a magnitude. Ask what sure amount the decision-maker would trade the gamble for, then take `EV − CE` as the measure.
5. Scale expectations to the stake. Risk aversion grows with the size of the bet. Evidence from small-stakes experiments does not transfer to consequential decisions.
6. Check the four evidence channels before asserting a risk preference. Controlled experiments give clean design but few subjects. Surveys of actual portfolio and insurance choices give large samples of real behavior. Asset prices are an experiment in progress, with millions expressing preferences through the prices they set. And gambling data from game shows, race tracks, and casinos shows how people choose under real stakes.
7. Screen the decision for the documented behavioral quirks listed below, especially if the decision-maker has recent losses or is being shown frequent performance updates.

**Reference data:**

Group differences in risk aversion (Damodaran, Foundations of Finance Session 4):

| Comparison | Finding |
|---|---|
| Male vs female | Men are less risk averse than women for small bets. For large, consequential bets they are as risk averse, if not more. |
| Naive vs experienced | Naive students bid more conservatively than construction-industry experts for the same asset; experience lowers measured risk aversion. |
| Young vs old | Risk aversion rises with age. Single people are less risk averse than married people. |
| Racial and cultural | Humans share far more in common on risk aversion than they differ. Cultural differences are second-order. |

Documented behavioral quirks:

| Quirk | Description |
|---|---|
| Framing | Presentation changes choices among mathematically identical options. |
| Loss aversion | Losses loom larger than equal gains. People are risk averse over gains but risk seeking over losses. |
| Myopic loss aversion | More frequent feedback on where they stand makes people more risk averse. |
| House money effect | People take more risk with money obtained easily than with money they earned. |
| Break-even effect | People who have lost money will gamble on otherwise unattractive lotteries that offer a chance to break even. |
| Long shot bias | People chase a large payoff with a tiny chance of success, abandoning risk aversion. |

**Worked example:** The St. Petersburg gamble. A coin is flipped; you win $1 if the first flip is tails, and the game stops the moment heads appears. Each further tails doubles the prize, so n straight tails pays `2^(n−1)` dollars. The probability of reaching stage n is `1/2^n`, so each stage contributes `(1/2^n) × 2^(n−1) = $0.50` to expected value, and the infinite sum diverges. The gamble is worth infinitely much in expectation. Nicholas Bernoulli found in the 1700s that people paid on average about $2 to play. That gap — infinite expected value versus a $2 certainty equivalent — is the St. Petersburg Paradox, and it is the cleanest demonstration that people do not price risky bets at expected value.

A second, sharper example of loss aversion. Most people take $750 for sure over a 75% chance of $1,000 (both have an expected value of $750). The same people will gamble on a 75% chance of losing $1,000 rather than accept a certain loss of $750 (both have an expected value of −$750). Risk aversion over gains flips to risk seeking over losses.

**Determinism:**
- DETERMINISTIC: expected values of stated gambles, from probabilities and payoffs. The `EV − CE` gap once a certainty equivalent is stated. Any utility-function calculation once the function is specified.
- JUDGMENT: what price a specific person or investor would pay for a gamble; which utility function describes them; how large the stake feels to them; whether a risk is quantifiable at all. Eliciting a certainty equivalent requires actually asking the decision-maker or observing their trades. Attributing a risk premium to a market requires asset price data.

**Pitfalls:**
- Defining risk as only downside. That framing makes avoidance look rational and destroys the analysis before it starts.
- Excluding a risk from the valuation because it cannot be measured precisely. Knight's line is a measurement convenience, not a pricing rule.
- Assuming one risk aversion level for everyone. It varies systematically by age, experience, marital status, and stake size.
- Extrapolating small-stakes experimental results to large decisions, where risk aversion is higher.
- Reporting performance frequently to an investor and then being surprised at how conservative they become. Myopic loss aversion is a direct consequence of the reporting frequency.
- Ignoring that a decision-maker sitting on losses will take gambles they would otherwise reject.

**Sources:**
- `foundations_of_finance--introduction p.6`
- `foundations_of_finance--what_is_risk p.2-11`

**Related:** [[diversification-and-the-mean-variance-framework]], [[marginal-investor-and-beta]], [[time-value-of-money-and-discount-rates]], [[finance-first-principles]], [[equity-risk-premium]]
