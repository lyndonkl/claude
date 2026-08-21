# Valuation misconceptions (three myths and their truths)

**Core idea:** Three myths make analysts value things badly, and each has a corrective truth. Myth 1: valuation is an objective search for "true" value. Truth: every valuation is biased, and the only open questions are how much and in which direction. Myth 2: a good valuation gives a precise estimate. Truth: no valuation is precise, and the payoff is largest exactly where precision is lowest. Myth 3: the more quantitative the model, the better. Truth: your understanding of a model falls as its input count rises, and simple models beat complex ones. Accepting all three changes behaviour. You audit your own incentives first. You value the hard companies instead of avoiding them. You keep models small on purpose. Knowing valuation will not make you rational either. Damodaran opens the course on "lemmingitis" — the urge to follow the crowd off a cliff.

**Formulas:** None. Three stated propositions govern behaviour:
- Bias magnitude and direction ∝ who pays you and how much you are paid.
- Payoff to doing a valuation is *increasing* in the imprecision of that valuation (uncertainty is the source of the edge, not an obstacle).
- Your understanding of a valuation model is *inversely* proportional to the number of inputs it requires.

**Procedure:**
1. **Diagnose bias before opening the spreadsheet.** Write down (a) who is paying for this valuation and how much, (b) what answer they want, (c) what you already believe about the company, and (d) whether you have taken a public position on it. Any "yes" answer predicts the direction of bias.
2. **Neutralise what you can.** Do the qualitative homework (Step 1 of the story process, see [[landscape-survey]]) *before* looking at the market price; if you have already seen the price, treat it as an anchor to be argued against, not toward.
3. **Do not promise precision.** State the value as a point estimate plus an explicit range or distribution (see [[monte-carlo-valuation-simulation]], [[narrative-scenario-grids]]). If a client insists on a single number to two decimals, that is a warning, not a spec.
4. **Choose the simplest model that captures the story.** Decision rule: if adding an input does not change the value by enough to change the investment decision, delete it. Damodaran's own worked valuations run on ~5 story levers (growth, margin, sales-to-capital, cost of capital, failure probability) — see [[narrative-to-value-drivers]].
5. **Target the imprecise.** Deliberately prefer young, uncertain, hard-to-value companies over stable ones: "anyone can value a company that is stable, makes money and has an established business model." That is where the payoff is.
6. **Run the unbiasedness test over time.** Track your revisions: if your valuations are unbiased, you should revise value *up* roughly as often as you revise it *down*. A one-sided revision record is evidence of directional bias.

**Reference data:** None (conceptual). Related empirical anchor used later in the course: over a long forecasting record, you will be wrong 100% of the time, because information keeps arriving; the test is not accuracy but symmetry of revisions.

**Worked example:** Tesla, November 2021 (Damodaran's Motley Fool valuation). The model has only five yellow input cells — 5-year revenue CAGR (35%), target operating margin (16%), sales-to-capital (4.00), initial cost of capital (6.00%), probability of failure (0%). That deliberately tiny input set is Myth 3 in practice: the value per share of $571.29 against a market price of $1,200 is defensible and auditable precisely *because* a reader can argue with five numbers rather than fifty. The estimate is not precise — a plausible narrative range spans several hundred dollars a share — and Damodaran presents it as a story-conditional number, not "the" value.

**Determinism:**
- DETERMINISTIC: nothing here computes a value. The unbiasedness test is mechanical once you keep a revision log (count of upward vs downward revisions → symmetry ratio).
- JUDGMENT: naming your own bias sources. That needs the fee structure, the client's identity, and any prior public position. Deciding which inputs to keep needs a sensitivity run on each input. Deciding when a range beats a point estimate is also a judgment call.

**Pitfalls:**
- Believing a valuation is objective because it is quantitative — the spreadsheet inherits the analyst's bias intact.
- Hiding bias in "conservative" or "aggressive" adjustments instead of stating them.
- Equating model complexity with rigour; the analyst's "quality" degenerating into skill at concealing input tweaks (see [[three-approaches-to-valuation]], DCF disadvantages).
- Avoiding uncertain companies because you cannot be precise about them — that is where the money is.
- Assuming that knowing valuation immunises you from herding. It does not.

**Sources:**
- valintrospr21 p.2-3
- valintrospr20 p.2-3
- valintrospr20-repost p.2-3
- valpacket1spr21 p.308 (you will be wrong 100% of the time; unbiasedness test)
- valpacket1spr21 p.293 (only difficult companies test valuation skill)

**Related:** [[bermuda-triangle-of-valuation]], [[narrative-numbers-bridge]], [[story-to-numbers-process]], [[monte-carlo-valuation-simulation]], [[narrative-updating-feedback-loop]]
