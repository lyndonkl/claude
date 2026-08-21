# Decision trees as the alternative to option pricing

**Core idea:** Optionality is what makes a staged investment worth more than the same investment taken all at once. A decision tree captures that directly: you lay out the stages, attach probabilities and payoffs, and roll back taking the best action at each decision node. Traditional decision tree analysis discounts every branch at one cost of capital, so its answers generally differ from option pricing values. But the gap is about discount rates, not about logic. Adjust the discounting and a decision tree yields the same value as an option pricing model. Damodaran's closing verdict on real options is exactly this: when an option does have significant value, the same inputs used in a binomial model can be used in a decision tree to yield equivalent value.

**Formulas:**
- Static expected value: `EV = sum over states of (probability x payoff)`.
- Roll-back at a chance node: `Node value = sum over branches of (probability x branch value)`.
- Roll-back at a decision node: `Node value = max(value of each available action)`. This max is where optionality enters.
- Two reconciliations with option pricing:
  - *Copeland solution*: use a different discount rate at each node, reflecting where you are in the tree.
  - *Riskfree route*: discount each branch's cash flows at the riskfree rate, compute the probability-weighted expected value, then adjust that expected value for the market risk of the investment.

**Procedure:**
1. Draw the tree. Mark chance nodes (nature decides) and decision nodes (you decide) distinctly. Every real option lives at a decision node.
2. Attach probabilities to every branch out of each chance node; they must sum to 1.
3. Attach payoffs (or continuation values) to terminal nodes.
4. Roll back from the terminal nodes. At chance nodes take the probability weighted average. At decision nodes take the maximum over available actions, including "abandon".
5. Discount. If you use a single cost of capital across the whole tree, expect the answer to differ from the option-pricing value. If you want reconciliation, apply the Copeland node-specific rates or the riskfree-plus-risk-adjustment route.
6. Compare the rolled-back value at the root against the value of the "do nothing / abandon now" branch. Take the action with the higher value.
7. Use a decision tree instead of an option pricing model whenever the pricing test in [[real-options-framework]] fails — untraded underlying, untradable option, or unclear exercise cost — but the option test and exclusivity test pass.

**Reference data:**

Which tool for which situation:

| Situation | Tool |
|---|---|
| Underlying traded, option traded, exercise cost known | Option pricing model (binomial or Black-Scholes) |
| Discrete, identifiable stages with estimable probabilities (FDA trials, exploration phases) | Decision tree |
| Continuous underlying, jumps, early exercise | Binomial tree (structurally similar to a decision tree) |
| Option test or exclusivity test fails | Neither — add no premium |

A binomial tree with outcomes at each node looks a great deal like a capital-budgeting decision tree. The structural difference is the discount rate, not the shape.

**Worked example (the core intuition):** The same investment, unstaged and staged.

*Unstaged (p.4).* One shot today: Success with probability 1/2 pays +100; Failure with probability 1/2 pays -120. `EV = 0.5(100) + 0.5(-120) = -10`. Negative — reject.

*Staged (p.5).* Stage 1: probability 3/4 of an interim +20, probability 1/4 of -20 (and you stop there). Only after the favorable +20 do you commit to Stage 2: probability 2/3 of +80, probability 1/3 of -100. The large downside is now taken only after observing a favorable first stage, and you can walk away after a bad one. The staged expected value turns positive. Same investment, same economics — optionality alone flips the decision.

**Worked example (full tree):** A pharmaceutical company whose only asset is one drug in the FDA pipeline. All figures in $ millions.

Root decision: Test (value $50.36) versus Abandon.
- Test → Succeed 70% (node value $93.37) or Fail 30% (-$50).
- After success, four market outcomes:
  - Types 1 & 2, probability 10%, node $573.71 → Develop: Succeed 75% → $887.05; Fail 25% → -$366.30 (Abandon alternative -$366.30).
  - Type 2 only, probability 10%, node -$143.69 → Develop: Succeed 80% → -$97.43; Fail 20% → -$328.74 (Abandon -$328.74). Note the firm still develops at -$97.43 because abandoning is worse at -$328.74.
  - Type 1 only, probability 30%, node $402.75 → Develop: Succeed 80% → $585.62; Fail 20% → -$328.74 (Abandon -$328.74).
  - Fail at this stage, probability 50% → -$140.91.

Rolled back, the value of testing is $50.36, so the firm tests — despite many losing branches.

**Determinism:** **DETERMINISTIC**: the roll-back arithmetic. Given the tree structure, all probabilities, all terminal payoffs, and the discount rate(s), a script computes every node value and the root value, taking probability-weighted averages at chance nodes and maxima at decision nodes. The unstaged expected value `-10` and the staged comparison are pure arithmetic. **JUDGMENT**: the tree itself. Which stages exist, what decisions are genuinely available at each stage, the probability on every branch, the cash flows on every terminal node, and — most consequentially — what discount rate applies where. A single cost of capital across the tree is a modeling choice that will not match option-pricing values; node-specific rates require a view on how risk changes as you move through the tree.

**Pitfalls:**
- Using one cost of capital for the entire tree and then claiming the answer equals the option value. It generally will not. Risk changes as you move through the tree.
- Forgetting to take the max at decision nodes. Without it you have modeled a passive gamble, not an option, and you will reproduce the unstaged -10 answer.
- Treating branch probabilities as objective when they are estimates. The pharma tree's $50.36 root value depends entirely on 70%/30%, 75%/25%, and the market-type splits.
- Building a decision tree AND adding a real-option premium on top. They are alternative representations of the same optionality, not additive.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket3spr21 p.4-5, p.20-22, p.83
- valuations--lecture_notes--spring_2020--valpacket3spr20 p.4-5, p.20-22, p.83

**Related:** [[real-options-framework]], [[replicating-portfolio-and-binomial-model]], [[option-to-abandon]], [[patent-valuation-as-option]], [[scenario-analysis]], [[simulation]]
