---
name: adverse-selection-prior
description: Produces a Bayesian prior probability that an offered transaction is +EV for the recipient, given that the counterparty chose to propose it. Applies Akerlof market-for-lemons logic -- if they offered it, they believe it is +EV for them, so the prior that it is +EV for us is materially below 50%. Reusable across trade evaluation, waiver drops (another team dropping a player is also adverse selection), job-offer analysis, M&A, and any "someone offered me this" situation. Use when you receive an unsolicited trade/offer/proposal, analyzing incoming trade prior, evaluating why a counterparty proposed a deal, or when user mentions adverse selection, market for lemons, why did they offer this, incoming trade prior, they proposed it, Bayesian adjustment on received offer.
---
# Adverse Selection Prior

## Table of Contents
- [Example](#example)
- [Workflow](#workflow)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Example

**Scenario**: We receive a fantasy trade offer. Opponent (classified `active` archetype) offers us a star hitter (their side) for two of our mid-tier hitters (our side). On surface the offer looks roughly fair -- our own projection model says the deal is +3% EV for us.

**Inputs**:
- `offer_type`: `trade`
- `proposer_archetype`: `active`
- `offer_symmetry_score`: 72 (looks fair-to-slightly-favorable for us)
- `proposer_info_asymmetry`: 55 (moderate -- we do not have closer news that they might have, but no public bombshell either)

**Step 1 -- Base prior by offer type**:
- Received trade offer base prior = **0.40** (below 50% because they chose to propose it).

**Step 2 -- Symmetry adjustment**:
- `offer_symmetry_score` = 72 > 70 threshold -> **+0.07**.
- Running prior: 0.47.

**Step 3 -- Asymmetry adjustment**:
- `proposer_info_asymmetry` = 55 (below 60 threshold but non-trivial) -> **-0.05**.
- Running prior: 0.42.

**Step 4 -- Archetype adjustment**:
- `active` archetype -> they analyzed before offering -> **-0.05**.
- Final `prior_ev_probability`: **0.37**.

**Step 5 -- Recommended adjustment (EV haircut)**:
- Prior is 0.37 (vs neutral 0.50). Map to multiplicative haircut.
- `recommended_adjustment` = 0.88 (apply a 12% EV haircut to our own projection).
- Our model said +3% EV; after haircut: 1.03 x 0.88 = **0.907** -> expected value is actually **negative 9.3%**.

**Step 6 -- Bayesian rationale**:
"Active trader proposed this offer. They had the option to propose any trade or no trade, and they selected this one -- strong evidence it is +EV for them. Surface symmetry (72) partially offsets, but moderate info asymmetry (55) and analytical archetype push the prior to 0.37. Apply 12% EV haircut. Our +3% projection becomes -9% after adjustment; this is below the accept threshold."

**Step 7 -- Override hints**:
- "If closer news broke in last 48h and we have not checked news feeds, asymmetry is actually 85+; re-run with asymmetry=85 (prior drops to ~0.22)."
- "If we can independently confirm the star hitter has no hidden injury/suspension, symmetry is actually 80+; re-run with symmetry=85 (prior rises to ~0.44)."
- "If this is a repeated-game partner we have cooperated with 5+ times and they have never sent a -EV offer, archetype effectively shifts toward 'good-faith' and base prior rises by +0.05."

**Output contract**:
```json
{
  "prior_ev_probability": 0.37,
  "recommended_adjustment": 0.88,
  "bayesian_rationale": "Active trader selected this offer from all possible offers they could have made -- strong signal it is +EV for them. Surface symmetry (72) partially offsets, but moderate info asymmetry (55) and analytical archetype push prior below 0.40.",
  "override_hints": [
    "If closer/injury news broke in last 48h, asymmetry jumps to 85+; re-run.",
    "If we can independently confirm the star has no hidden issue, symmetry rises to 85; re-run.",
    "If repeated-game partner with cooperation history, base prior rises by +0.05."
  ]
}
```

## Workflow

Copy this checklist and track progress:

```
Adverse Selection Prior Progress:
- [ ] Step 1: Identify offer_type and set base prior
- [ ] Step 2: Collect proposer_archetype from opponent classifier
- [ ] Step 3: Score offer_symmetry (0-100) from surface analysis
- [ ] Step 4: Score proposer_info_asymmetry (0-100)
- [ ] Step 5: Apply adjustments to produce prior_ev_probability
- [ ] Step 6: Convert prior to recommended_adjustment (multiplicative haircut)
- [ ] Step 7: Write bayesian_rationale and override_hints
- [ ] Step 8: Validate against rubric
```

**Step 1: Identify offer type and set base prior**

Classify the incoming proposal. Different offer types carry different base priors because the counterparty's selection pressure differs. See [resources/template.md](resources/template.md#base-prior-by-offer-type) for the base-prior table.

- [ ] `trade` -> base prior 0.40 (active selection; they wrote the offer)
- [ ] `waiver_claim_dropped_by_other` -> base prior 0.42 (they chose to drop the player; weaker selection than a trade)
- [ ] `free_agent_pickup_available` -> base prior 0.48 (no one claimed; may just mean no one noticed, weaker adverse selection)
- [ ] `counter_offer` -> base prior 0.38 (they rejected our first offer and crafted a counter -- the selection is tighter)
- [ ] `generic` -> base prior 0.40 (unknown context)

**Step 2: Collect proposer archetype**

Read the counterparty's archetype from the opponent classifier (if available) or estimate it. See [resources/methodology.md](resources/methodology.md#archetype-adjustments) for the full adjustment table.

- [ ] `active` -> analyzed before offering -> archetype_delta = -0.05
- [ ] `expert` -> strongest selection pressure -> archetype_delta = -0.08
- [ ] `dormant` -> may be clicking without deep analysis -> archetype_delta = +0.08
- [ ] `frustrated` -> mixed (panic-selling vs scheming) -> archetype_delta = 0.0 (but flag for case-by-case review)
- [ ] `unknown` -> neutral -> archetype_delta = 0.0

**Step 3: Score offer symmetry**

Compute `offer_symmetry_score` (0-100) for how fair the offer looks on surface using our own valuation model.

- [ ] 0-30: clearly lopsided in their favor (rare; usually predatory)
- [ ] 30-70: asymmetric but plausible
- [ ] 70-100: looks fair or slightly favorable for us on surface
- [ ] Apply adjustment: if `offer_symmetry_score` > 70, add +0.05 to +0.10 (higher for scores above 85)
- [ ] If `offer_symmetry_score` < 30 (and still not obviously predatory), flag as "too good to be true" -- investigate

**Step 4: Score proposer info asymmetry**

Estimate `proposer_info_asymmetry` (0-100) -- do they plausibly have information we do not?

- [ ] Check for recent news (injury, suspension, closer change, lineup shift, management commentary)
- [ ] Check for public signals (roster construction implying knowledge of upcoming trade, DFA watch, platoon changes)
- [ ] 0-30: public information parity (both sides know everything relevant)
- [ ] 30-60: minor gap (they may follow a beat reporter we skipped)
- [ ] 60-100: material gap (fresh news broke, insider-ish timing)
- [ ] Apply adjustment: subtract 0.10 to 0.20 if asymmetry > 60 (larger subtraction for scores above 80)

**Step 5: Apply adjustments to produce prior**

Combine base prior with all deltas. See [resources/methodology.md](resources/methodology.md#bayesian-update-derivation) for the derivation.

- [ ] Start with `base_prior` from Step 1
- [ ] Apply `symmetry_delta` from Step 3
- [ ] Apply `asymmetry_delta` from Step 4
- [ ] Apply `archetype_delta` from Step 2
- [ ] Clip final result to [0.10, 0.70] -- priors outside this band indicate specification error
- [ ] `prior_ev_probability` = clipped sum

**Step 6: Convert prior to recommended adjustment**

Translate the prior into a multiplicative EV haircut that downstream consumers can apply to their own EV calculation. See [Quick Reference](#quick-reference) for the mapping.

- [ ] If prior >= 0.50: `recommended_adjustment` = 1.00 (no haircut; rare case)
- [ ] If prior = 0.45: `recommended_adjustment` = 0.95
- [ ] If prior = 0.40: `recommended_adjustment` = 0.90
- [ ] If prior = 0.35: `recommended_adjustment` = 0.85
- [ ] If prior <= 0.30: `recommended_adjustment` = 0.80 (deep haircut; strong adverse-selection signal)
- [ ] Downstream consumer multiplies their own EV by this factor: `adjusted_EV = own_EV x recommended_adjustment`

**Step 7: Write rationale and override hints**

Produce the string outputs that make the prior reviewable.

- [ ] `bayesian_rationale`: 2-4 sentences naming the base prior, the two largest adjustments, and the conclusion
- [ ] `override_hints`: 2-5 conditional statements of the form "If X, then re-run with Y adjusted to Z"
- [ ] Hints must be actionable -- each should identify a specific input that would change the prior by >= 0.05

**Step 8: Validate against rubric**

Score the output against [resources/evaluators/rubric_adverse_selection_prior.json](resources/evaluators/rubric_adverse_selection_prior.json). Minimum standard: average score of 3.5 or above.

## Common Patterns

**Pattern 1: Dormant-manager trade offer (prior rises toward 0.50)**
- **Signal**: Counterparty has made < 3 roster moves in the past 30 days; archetype = `dormant`
- **Interpretation**: They may be clicking without analyzing; the selection pressure that normally makes offered deals adversely selected is weak
- **Adjustments**: archetype_delta = +0.08; if symmetry high, prior can approach 0.50
- **Recommended adjustment**: 0.95 (only 5% haircut)
- **Domain examples**: Disengaged sellers in M&A (founder retiring without diligence), uninformed recruiters spamming job offers, estate liquidators pricing used goods below market

**Pattern 2: Expert-trader offer (prior drops toward 0.25)**
- **Signal**: Counterparty is a known sharp -- wins auctions efficiently, trades frequently and profitably; archetype = `expert`
- **Interpretation**: Strongest possible selection pressure. They have analyzed this and other possible offers; they chose this specific one because it is most +EV for them
- **Adjustments**: archetype_delta = -0.08; asymmetry likely elevated even without explicit news
- **Recommended adjustment**: 0.80-0.85 (deep haircut)
- **Domain examples**: Activist investor offering to buy your block (they see value you missed), quant fund bidding on your illiquid position, top-decile recruiter pitching a role (role likely has hidden downside -- you are plan-C)

**Pattern 3: Frustrated/panic-selling offer (mixed; case-by-case)**
- **Signal**: Counterparty is losing badly, emotional trades, archetype = `frustrated`
- **Interpretation**: Two sub-cases -- (a) genuine tilt/panic-sell (+EV for us) or (b) schemer using frustration as cover (-EV for us)
- **Adjustments**: archetype_delta = 0; require additional signal (recent heavy losses + chat/message tone) to classify
- **Recommended adjustment**: 0.90 default; can rise to 1.05 if panic-sell is confirmed, drop to 0.80 if scheming is suspected
- **Domain examples**: Distressed-seller in M&A (bankruptcy-driven), job candidate "dumping" a role they just took (why are they leaving so fast?), garage-sale pricing during a divorce

**Pattern 4: Unsolicited job offer or M&A approach**
- **Signal**: Offer arrives without you having signaled availability
- **Interpretation**: They selected you from a wide pool. Why you specifically? Either (a) you are genuinely scarce/matched (+EV) or (b) you are plan-B and the role/deal has a defect
- **Adjustments**: base_prior 0.40; symmetry_delta depends on apparent fit; asymmetry_delta depends on whether you can diligence the role/target
- **Recommended adjustment**: 0.85-0.95
- **Override**: If you can confirm (via back-channels) that plan-A candidates exist and were passed over, prior drops further

**Pattern 5: Waiver drop by another team**
- **Signal**: Another team drops a player; player is now available to claim
- **Interpretation**: Weaker selection than a trade (the dropping team gained nothing by offering to us specifically), but still adverse selection -- they judged the player not worth a roster slot. The average dropped player is worse than the average player of that name
- **Adjustments**: base_prior 0.42 (slightly higher than trade); archetype of dropper matters less
- **Recommended adjustment**: 0.92 (mild haircut)
- **Domain examples**: Used cars abandoned at dealer auctions, stocks dumped in forced liquidation, former employees on the market

## Guardrails

1. **Base prior is always below 0.50 for received offers**. This is the core of the market-for-lemons insight. If your prior exceeds 0.50, you have either (a) mis-specified the archetype (e.g., dormant with very high symmetry can approach but rarely cross 0.50) or (b) ignored the selection pressure. Double-check.

2. **"Seems fair" = "probably bad"**. Counterparties who propose transactions have selected them from the space of possible transactions. A surface-fair offer is the worst-case from an adverse-selection standpoint because they had many fair-looking options and chose the one best for them.

3. **Do not double-count adjustments**. If you have already adjusted your own EV for known information (e.g., you penalized the player because you know about an injury), do not also treat that information as asymmetry reducing the prior. Asymmetry captures information they have that you do not.

4. **Clip priors to [0.10, 0.70]**. Priors outside this band are almost always specification errors. A 0.05 prior implies near-certainty of a predatory offer, which is rare even from experts. A 0.75 prior implies we should take every offer, contradicting the selection argument.

5. **Archetype signal comes from behavior, not self-report**. A counterparty who claims to be a "casual player" but has made 40 waiver claims and won 3 bidding wars is not dormant. Read archetype from observed actions.

6. **Panic-sell signals must be triangulated**. "They seem frustrated" is not sufficient to raise the prior. Require at least two of: recent heavy losses, message-tone evidence, visible tilt-trades (overreaching for recently-hot players), public complaint about the league.

7. **Repeated-game reputation adjusts the prior**. If you have cooperated with this counterparty 5+ times and they have never sent a -EV offer, the archetype-independent base prior rises by ~0.05. If they have sent a predatory offer before, the base prior drops by ~0.05. Track per-counterparty history.

8. **Override hints must be actionable and specific**. "Do more research" is not a hint. "If the team's closer has been pulled from the role this week, re-run with asymmetry=85" is actionable.

9. **The recommended adjustment is multiplicative, not additive**. Downstream consumers apply `adjusted_EV = own_EV x recommended_adjustment`. Do not output an additive haircut -- it breaks when own_EV is near zero or negative.

10. **This skill produces a prior, not a verdict**. Downstream decision logic (accept/counter/reject) belongs in the consumer skill (e.g., `mlb-trade-analyzer` or the M&A decision agent). This skill only outputs the prior and the haircut factor.

## Quick Reference

**Base priors by offer type:**

| Offer type | Base prior | Rationale |
|------------|------------|-----------|
| `trade` | 0.40 | Active selection; they wrote the offer |
| `waiver_claim_dropped_by_other` | 0.42 | They dropped it; weaker selection than targeted trade |
| `free_agent_pickup_available` | 0.48 | Weak selection; may be unclaimed due to oversight |
| `counter_offer` | 0.38 | Tighter selection -- they rejected first offer and crafted this |
| `generic` | 0.40 | Default when context unknown |

**Archetype adjustments:**

| Archetype | Delta | Interpretation |
|-----------|-------|----------------|
| `expert` | -0.08 | Strongest selection; they chose this from many offers |
| `active` | -0.05 | Analyzed before offering |
| `frustrated` | 0.0 (flag) | Mixed: panic-sell (+) vs scheme (-); require sub-signal |
| `dormant` | +0.08 | May be clicking without analysis |
| `unknown` | 0.0 | Neutral |

**Symmetry adjustments** (based on `offer_symmetry_score`):

| Score | Delta |
|-------|-------|
| 85-100 | +0.10 |
| 70-85 | +0.05 to +0.07 |
| 30-70 | 0.0 |
| < 30 | 0.0 (and flag as "too good to be true") |

**Asymmetry adjustments** (based on `proposer_info_asymmetry`):

| Score | Delta |
|-------|-------|
| 0-30 | 0.0 |
| 30-60 | -0.03 to -0.05 |
| 60-80 | -0.10 to -0.15 |
| 80-100 | -0.15 to -0.20 |

**Prior-to-adjustment mapping:**

| `prior_ev_probability` | `recommended_adjustment` | Interpretation |
|------------------------|--------------------------|----------------|
| >= 0.50 | 1.00 | No haircut; unusual for received offer |
| 0.45 | 0.95 | Light haircut |
| 0.40 | 0.90 | Standard haircut |
| 0.35 | 0.85 | Moderate haircut |
| 0.30 | 0.80 | Deep haircut -- strong adverse selection |
| <= 0.25 | 0.75 | Predatory suspicion -- default to reject |

**Output contract:**

```
prior_ev_probability: float in [0.10, 0.70]
recommended_adjustment: float in [0.75, 1.00]
bayesian_rationale: string (2-4 sentences)
override_hints: string[] (2-5 conditional statements)
```

**Key resources:**

- **[resources/template.md](resources/template.md)**: Decision tree for prior adjustment, worked examples (dormant, expert, frustrated), output contract template
- **[resources/methodology.md](resources/methodology.md)**: Akerlof market-for-lemons derivation, Bayesian update math, why "seems fair" means "probably bad", cross-domain examples (finance, labor)
- **[resources/evaluators/rubric_adverse_selection_prior.json](resources/evaluators/rubric_adverse_selection_prior.json)**: 10 quality criteria

**Inputs required:**

- `offer_type` (enum: trade | waiver_claim_dropped_by_other | free_agent_pickup_available | counter_offer | generic)
- `proposer_archetype` (enum: active | dormant | frustrated | expert | unknown)
- `offer_symmetry_score` (int, 0-100)
- `proposer_info_asymmetry` (int, 0-100)

**Outputs produced:**

- `prior_ev_probability` (float, 0-1, baseline < 0.5 for received offers)
- `recommended_adjustment` (float, multiplicative factor)
- `bayesian_rationale` (string)
- `override_hints` (string[])
