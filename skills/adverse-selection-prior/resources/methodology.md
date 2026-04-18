# Adverse Selection Prior -- Methodology

## Table of Contents
- [The Akerlof Market for Lemons](#the-akerlof-market-for-lemons)
- [Bayesian Update Derivation](#bayesian-update-derivation)
- [Why "Seems Fair" Means "Probably Bad"](#why-seems-fair-means-probably-bad)
- [How Asymmetric Information Shifts the Prior](#how-asymmetric-information-shifts-the-prior)
- [Archetype Adjustments](#archetype-adjustments)
- [Cross-Domain Examples](#cross-domain-examples)
  - [Finance: Insider Trading Signals](#finance-insider-trading-signals)
  - [Labor Markets: Unsolicited Job Offers](#labor-markets-unsolicited-job-offers)
  - [Used-Car Markets](#used-car-markets)
  - [M&A and Corporate Deal-Making](#ma-and-corporate-deal-making)
  - [Fantasy Sports Trades](#fantasy-sports-trades)
- [Edge Cases and Overrides](#edge-cases-and-overrides)
- [Calibration and Backtesting](#calibration-and-backtesting)

---

## The Akerlof Market for Lemons

George Akerlof's 1970 paper *The Market for Lemons* established the canonical result: in markets where sellers have better information than buyers about quality, low-quality goods drive out high-quality goods. The mechanism:

1. Seller knows the true quality of their item (a car, a stock, a player, a company).
2. Buyer only knows the distribution of qualities in the market.
3. Buyer offers the average price for the distribution.
4. Sellers of above-average items refuse to sell at the average price (they would take a loss).
5. Only below-average items remain for sale.
6. Buyer, recognizing this, lowers their offer further.
7. Process continues until the market either collapses or reaches an equilibrium dominated by lemons.

**The generalization that powers this skill**: When a counterparty *proposes* a transaction to you, the fact of the proposal is itself information. They have done a private analysis and concluded the deal is good for them. If their analysis is approximately correct, and the deal is zero-sum or near-zero-sum, the deal is bad for you in expectation.

This is not a moral claim about the counterparty -- they can be acting in perfect good faith. The adverse selection arises purely from the selection mechanism: the subset of possible deals they *propose* is not a random subset of all possible deals; it is the subset they believe is good for them.

---

## Bayesian Update Derivation

Let `E` = event "the offered transaction is +EV for me".
Let `O` = event "the counterparty proposed this offer".

We want `P(E | O)`, the probability that the offer is +EV for us *given that they offered it*.

By Bayes' theorem:
```
P(E | O) = P(O | E) * P(E) / P(O)
```

**Prior `P(E)`**: In a world with no selection, what is the probability a random transaction between us is +EV for me? For zero-sum trades this is approximately 0.50 (with some noise from valuation error). Call this `p0`.

**Likelihood `P(O | E)`**: If the transaction is +EV for me, it is (in zero-sum) -EV for them. How likely are they to propose a deal that is -EV for them? Low. Call this `q_bad`.

**Likelihood `P(O | ~E)`**: If the transaction is +EV for them (-EV for me), how likely are they to propose it? Much higher. Call this `q_good`.

**Posterior**:
```
P(E | O) = q_bad * p0 / (q_bad * p0 + q_good * (1 - p0))
```

Example with `p0 = 0.50`, `q_bad = 0.10`, `q_good = 0.70`:
```
P(E | O) = 0.10 * 0.50 / (0.10 * 0.50 + 0.70 * 0.50)
         = 0.05 / 0.40
         = 0.125
```

This is extreme (a perfectly selecting counterparty drives the posterior to ~0.12). Real counterparties are noisier, and real deals are not perfectly zero-sum (positional fit, roster-construction asymmetry, consolidation bonuses, etc.), which pushes the prior back up. Empirically a base prior of 0.40 for received trade offers is a reasonable starting point that reflects:
- Imperfect selection (counterparties make mistakes)
- Non-zero-sum effects (both sides can gain from positional fit)
- Valuation noise (our own model has error)

**Archetype modulates `q_good` vs `q_bad`**. An expert has `q_good/q_bad` near 7:1; a dormant manager might be closer to 2:1 (they click on many offers without careful analysis). This is the mechanical origin of the archetype adjustments.

**Information asymmetry modulates `p0`**. If they know something we do not, our own valuation is systematically biased, so `p0` for this specific offer is below 0.50 before any selection effect.

---

## Why "Seems Fair" Means "Probably Bad"

A subtle but important implication: among offers that *look fair on surface*, the ones you actually receive are adversely selected *harder* than offers that look lopsided.

**Reasoning**:
- Counterparties know you will not accept obviously lopsided offers.
- So they construct offers that look fair enough to be accepted.
- An offer that is *actually* fair is unlikely to be offered (why would they bother?).
- An offer that *looks* fair but is actually -EV for you is exactly the offer they want to propose.
- Therefore: among surface-fair offers, the share that is actually -EV for you is *higher* than the share of -EV offers in the general population.

**Numerical illustration**: Suppose the counterparty's population of potential offers breaks down as:
- 30% actually +EV for us (they overlooked something)
- 70% actually -EV for us (they saw value)

Of those, suppose the surface-fair subset (symmetry 70+) consists of:
- 10% actually +EV for us
- 90% actually -EV for us

The surface-fair offers are *more* adversely selected than the population. The symmetry adjustment in this skill (+0.05 to +0.10) partially offsets this by acknowledging surface fairness as a weak signal of fairness -- but the net effect never completely erases the base prior.

This is why the symmetry adjustment caps at +0.10 rather than +0.30 or more. Surface fairness is a weak positive signal against a strong adverse-selection base.

---

## How Asymmetric Information Shifts the Prior

The `proposer_info_asymmetry` input captures the second dimension of lemons-market risk: they may have private information about the value of the thing being traded.

**Categories of information asymmetry** (from lowest to highest):

1. **Public information parity** (asymmetry 0-30): both sides read the same news sources, have access to the same stats, and observe the same public actions. Minimal correction needed.

2. **Beat-reporter gap** (asymmetry 30-60): one side follows a specialized source the other does not. Small corrections. Example in fantasy: they read a minor-league beat reporter who noted a prospect call-up rumor. Example in M&A: they attended a conference where the CEO hinted at a strategic shift.

3. **Material recent news** (asymmetry 60-80): meaningful information has just broken that one side has seen and the other has not. Large corrections. Example: a closer was pulled from the ninth-inning role during this afternoon's game and only a subset of managers have checked. Example in finance: an 8-K was filed 30 minutes ago and not everyone has parsed it.

4. **Insider-ish timing** (asymmetry 80-100): the timing of the offer itself is suspicious -- it arrives just before an expected announcement, or just after a private channel surfaced. Deepest corrections. Example: a trade offer arrives the day before the MLB trade deadline for a player rumored to be moving teams. Example in finance: a tender offer proposed days before a regulatory decision.

The skill's asymmetry adjustment (-0.03 to -0.20) scales with the score. At asymmetry 80+, the combined effect with an expert archetype can drive the prior to 0.15-0.20, triggering the deepest haircut.

**Detection heuristics** (what to look for):
- Unusual timing relative to news cycles
- Offers involving specifically the player/asset most likely affected by recent events
- Offers from counterparties with known reach (reporter friends, industry contacts)
- Offers that become *more* aggressive after a piece of news drops

---

## Archetype Adjustments

Archetypes encode the *selection strength* of the counterparty. See `/context/opponents/*.md` in the consuming domain or equivalent archetype documentation for how each is inferred from behavior.

| Archetype | Delta | Rationale |
|-----------|-------|-----------|
| `expert` | -0.08 | Strongest selection. They have analyzed many possible offers and chose this one because it maximizes their EV. `q_good/q_bad` ratio is high. |
| `active` | -0.05 | Strong selection, but noisier than expert. They analyze but may make errors. |
| `frustrated` | 0.00 (flag) | Mixed. Panic-sellers are *under*-selecting (+EV for us). Schemers using frustration as cover are *over*-selecting (-EV for us). Triangulate before applying. |
| `dormant` | +0.08 | Weak selection. They may be clicking offers without careful analysis. `q_good/q_bad` ratio approaches 1:1. |
| `unknown` | 0.00 | No prior; use base. |

**Panic triangulation** (for `frustrated`): require at least two of four signals to classify as genuine panic:
1. Recent heavy losses (e.g., 1-8 record, or -15% portfolio drawdown, or 3 failed projects)
2. Tone evidence (chat messages, public statements, body language)
3. Tilt-trades (erratic, high-volume activity outside their pattern)
4. Public complaint ("this league is rigged", "market is broken", "this company is falling apart")

If confirmed, override archetype_delta to +0.05 (treat as semi-dormant -- selection pressure has weakened).

If the offer looks *too* fair AND there is no public frustration signal, suspect scheming-disguised-as-frustration and override to -0.05 (treat as semi-active).

---

## Cross-Domain Examples

### Finance: Insider Trading Signals

**Context**: A large block of shares is offered to you privately at a small discount to market.

- `offer_type`: `trade` (block sale)
- `proposer_archetype`: likely `expert` (institutional seller)
- `offer_symmetry_score`: high if discount is small (looks fair)
- `proposer_info_asymmetry`: potentially very high if they hold inside information

The canonical Wall Street heuristic -- "if they want to sell, why do you want to buy?" -- is precisely adverse selection. The 10b5-1 trading plans that insiders use exist partly to manage this concern (pre-committed sales reduce the signal). An unsolicited block offer at a small discount, especially near an earnings announcement, should trigger the deepest haircut.

**Empirical anchor**: Studies of block trades find that large privately-negotiated sales predict negative abnormal returns in the 60 days following the trade, consistent with information-based selling. The adverse-selection prior is not theoretical; it shows up in return data.

### Labor Markets: Unsolicited Job Offers

**Context**: A recruiter contacts you about a role you did not apply for.

- `offer_type`: `generic` (or `trade` if highly specific)
- `proposer_archetype`: depends on recruiter sophistication (top firm = `expert`; generic spam = `dormant`)
- `offer_symmetry_score`: depends on compensation, title, scope alignment
- `proposer_info_asymmetry`: do they know something about the role that you do not? Plan-B candidates? Team dysfunction? Pending layoffs?

**The two sub-cases**:
1. **Positive selection** (high prior): you are genuinely scarce/matched. The role is well-defined and the compensation reflects market-clearing for your specific skill set. Prior: 0.45-0.50.
2. **Negative selection** (low prior): you are plan-B. The role has defects (difficult manager, impending layoffs, under-resourced, political minefield). Plan-A candidates have turned it down. Prior: 0.25-0.35.

**Detection**: diligence the role through back-channels. Has anyone you trust left recently? Has the role been open for > 6 months? Is the recruiter unable to explain why the previous occupant left? Each positive finding is an override hint.

**Connection to repeated games**: if the recruiter has placed people successfully before and the placements are thriving, `q_good/q_bad` for this recruiter specifically is better than the industry baseline.

### Used-Car Markets

**Context**: Akerlof's original example. A seller offers you their 2019 sedan at $2,000 below blue-book.

- `offer_type`: `trade`
- `proposer_archetype`: `unknown` (private seller) or `expert` (dealer)
- `offer_symmetry_score`: high (looks like a deal)
- `proposer_info_asymmetry`: very high -- they have driven the car for years; you have driven it for 20 minutes

**Resolution**: the discount is exactly the lemons premium. The seller knows something about the car (transmission whine, accident history, electrical gremlin) that justifies their willingness to sell below market. The rational buyer either (a) does a mechanic inspection (reduces asymmetry) or (b) applies the lemons discount to their own valuation.

**Why private seller != expert archetype**: private sellers often do not systematically compare to all possible offers they could construct. Their selection is weaker than an expert dealer's. A dealer offering the same car at the same discount is more concerning.

### M&A and Corporate Deal-Making

**Context**: A competitor approaches you with an unsolicited bid to acquire your division.

- `offer_type`: `trade` or `counter_offer` if you previously floated a sale
- `proposer_archetype`: `expert` (M&A professionals)
- `offer_symmetry_score`: moderate-to-high (sophisticated bidders construct fair-looking bids)
- `proposer_info_asymmetry`: very high -- they see strategic value we do not, OR they see defects in us we have not yet acknowledged

**Two sub-cases**:
1. **Strategic premium**: they see synergies that justify paying above our intrinsic value. This is +EV for us.
2. **Hidden defect**: they see a defect (upcoming regulation, technology shift, customer loss) we have not priced in. This is -EV for us.

**Resolution**: run a defensive diligence (what do they know?) in parallel with the offense diligence (what synergies do they see?). Unsolicited bids that arrive within weeks of a material external event (new regulation, competitor launch) carry especially high asymmetry.

### Fantasy Sports Trades

**Context**: The canonical application (principle #4 in game-theory-principles.md).

- `offer_type`: `trade`
- `proposer_archetype`: derived from opponent-classifier
- `offer_symmetry_score`: from our own trade-valuation model
- `proposer_info_asymmetry`: from news-feed checks

The `mlb-trade-analyzer` critic variant uses this skill to set the adverse-selection haircut before computing the final accept/counter/reject decision. The convention: if our own projection shows the trade as exactly even in value after the haircut, we reject. Only clearly positive trades pass.

---

## Edge Cases and Overrides

### Edge case 1: Multi-team trade proposals

When a three-way or four-way trade is proposed, the adverse-selection signal strengthens -- the proposer has constructed an offer that pleases *multiple* counterparties' valuations while still being +EV for themselves. Apply archetype_delta -0.03 additional.

### Edge case 2: Reverse-asymmetry cases

Rarely, *we* have information the counterparty lacks (we are the asymmetric insider). The skill assumes asymmetric information runs against us; if we believe we hold the information advantage, set `proposer_info_asymmetry` to 0 and do not discount. This should be rare -- if you think you are the informed party, double-check (the prior is always that the proposer is more informed, because they initiated).

### Edge case 3: Panic-sell override disagreement

If the panic signals are contested (2 present, 2 absent), leave archetype_delta at 0.00 and emit an override hint identifying the missing signals. Do not make up panic signals to justify a desired conclusion.

### Edge case 4: Repeated-game cooperative history

If you have a 5+ trade history with the counterparty and zero predatory offers, add +0.05 to base_prior. If you have any prior predatory offers (offers with realized post-trade asymmetry > 60), subtract 0.05 from base_prior.

### Edge case 5: The offer is for information, not value

If the counterparty is offering something strictly informational (a tip, a research report, a recommendation) rather than a transaction, the adverse-selection frame shifts -- they may be trying to move the market in a direction they have already positioned for. Apply the prior to the *implied trade* the information would induce.

---

## Calibration and Backtesting

The adverse-selection prior is only useful if it is calibrated -- its 0.40 should actually mean 40%. Over time, the consumer system should track:

- **Decisions where the prior said accept (>= 0.50)**: what fraction turned out +EV ex post?
- **Decisions where the prior said reject (< 0.30)**: what fraction turned out -EV ex post?
- **Decisions in the middle (0.30-0.50)**: are outcomes clustered near neutral?

If the prior is well-calibrated, a prior of 0.35 should be accurate to within ~0.05 (i.e., 30-40% of "prior 0.35" offers turn out +EV). If the prior is systematically too low, the base_prior and asymmetry adjustments need to be loosened. If systematically too high, tightened.

**Recommended tracking**:
- Log every emitted prior with the inputs
- Log the realized outcome (ex post EV) 60-90 days after the decision
- Compute calibration curves quarterly
- Adjust base priors and deltas if material drift

**Common recalibration findings**:
- Expert archetype is often too lenient (consider shifting from -0.08 to -0.10)
- Surface-symmetry adjustment is often too generous (consider capping at +0.07 instead of +0.10)
- Dormant archetype adjustments are often too aggressive (clicking is not actually uncorrelated with value)

Calibration is the bridge between this skill's theoretical framework and the empirical reality of your specific domain. Run it annually at minimum.
