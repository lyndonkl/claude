# Heuristics and Checklists Methodology

Advanced techniques for decision heuristics, checklist design, and cognitive bias mitigation.

## Table of Contents
1. [When to Use Heuristics vs. Checklists](#1-when-to-use-heuristics-vs-checklists)
2. [Heuristics Research and Theory](#2-heuristics-research-and-theory)
3. [Checklist Design Principles](#3-checklist-design-principles)
4. [Validating Heuristics and Checklists](#4-validating-heuristics-and-checklists)
5. [Refinement and Iteration](#5-refinement-and-iteration)
6. [Cognitive Biases and Mitigation](#6-cognitive-biases-and-mitigation)

---

## 1. When to Use Heuristics vs. Checklists

### Heuristics (Decision Shortcuts)

**Use when**:
- Time pressure (need to decide in <1 hour)
- Routine decisions (happens frequently, precedent exists)
- Good enough > perfect (satisficing appropriate)
- Environment stable (patterns repeat reliably)
- Cost of wrong decision low (<$10k impact)

**Don't use when**:
- Novel situations (no precedent, first time)
- High stakes (>$100k impact, irreversible)
- Adversarial environments (deception, misleading information)
- Multiple factors equally important (interactions matter)
- Legal/compliance requirements (need documentation)

### Checklists (Procedural Memory Aids)

**Use when**:
- Complex procedures (>5 steps)
- Error-prone (history of mistakes)
- High consequences if step missed (safety, money, reputation)
- Infrequent procedures (easy to forget details)
- Multiple people involved (coordination needed)

**Don't use when**:
- Simple tasks (<3 steps)
- Fully automated (no human steps)
- Creative/exploratory work (checklist constrains unnecessarily)
- Expert with muscle memory (checklist adds overhead without value)

---

## 2. Heuristics Research and Theory

### Fast and Frugal Heuristics (Gigerenzer)

**Key insight**: Simple heuristics can outperform complex models in uncertain environments with limited information.

**Classic heuristics**:

1. **Recognition Heuristic**: If you recognize one object but not the other, infer that the recognized object has higher value.
   - **Example**: Which city is larger, Detroit or Tallahassee? (Recognize Detroit → Larger)
   - **Works when**: Recognition correlates with criterion (r > 0.5)
   - **Fails when**: Misleading advertising, niche quality

2. **Take-the-Best**: Rank cues by validity, use highest-validity cue that discriminates. Ignore others.
   - **Example**: Hiring based on coding test score alone (if validity >70%)
   - **Works when**: One cue dominates, environment stable
   - **Fails when**: Multiple factors interact, no dominant cue

3. **1/N Heuristic**: Divide resources equally among N options.
   - **Example**: Investment portfolio - equal weight across stocks
   - **Works when**: No information on which option better, diversification reduces risk
   - **Fails when**: Clear quality differences exist

### Satisficing (Herbert Simon)

**Concept**: Search until option meets aspiration level (threshold), then stop. Don't optimize.

**Formula**: 
```
Aspiration level = f(past outcomes, time pressure, search costs)
```

**Adaptive satisficing**: Lower threshold if no options meet it after K searches. Raise threshold if too many options qualify.

**Example**:
- Job search: "Salary ≥$120k, culture fit ≥7/10"
- After 20 applications, no offers → Lower to $110k
- After 5 offers all meeting bar → Raise to $130k

### Ecological Rationality

**Key insight**: Heuristic's success depends on environment, not complexity.

**Environment characteristics**:
- **Redundancy**: Multiple cues correlated (take-the-best works)
- **Predictability**: Patterns repeat (recognition heuristic works)
- **Volatility**: Rapid change (simple heuristics adapt faster than complex models)
- **Feedback speed**: Fast feedback enables learning (trial-and-error refinement)

**Mismatch example**: Using recognition heuristic in adversarial environment (advertising creates false recognition) → Fails

---

## 3. Checklist Design Principles

### Atul Gawande's Checklist Principles

Based on research in aviation, surgery, construction:

1. **Keep it short**: 5-9 items max. Longer checklists get skipped.
2. **Focus on killer items**: Steps that are often missed AND have serious consequences.
3. **Verb-first language**: "Verify backups complete" not "Backups"
4. **Pause points**: Define WHEN to use checklist (before start, after critical phase, before finish)
5. **Fit on one page**: No scrolling or page-flipping

### READ-DO vs. DO-CONFIRM

**READ-DO** (Challenge-Response):
- Read item aloud → Perform action → Confirm → Next item
- **Use for**: Novices, unfamiliar procedures, irreversible actions
- **Example**: Surgical safety checklist (WHO)

**DO-CONFIRM**:
- Perform entire procedure from memory → Then review checklist to confirm all done
- **Use for**: Experts, routine procedures, flow state important
- **Example**: Aviation pre-flight (experienced pilots)

**Which to choose?**:
- Expertise level: Novice → READ-DO, Expert → DO-CONFIRM
- Familiarity: First time → READ-DO, Routine → DO-CONFIRM
- Consequences: Irreversible (surgery) → READ-DO, Reversible → DO-CONFIRM

### Forcing Functions and Fail-Safes

**Forcing function**: Design that prevents proceeding without completing step.

**Examples**:
- Car won't start unless seatbelt fastened
- Deployment script fails if tests not passing
- Door won't lock if key inside

**vs. Checklist item**: Checklist reminds, but can be ignored. Forcing function prevents.

**When to use forcing function instead of checklist**:
- Critical safety step (must be done)
- Automatable check (can be enforced by system)
- High compliance needed (>99%)

**When checklist sufficient**:
- Judgment required (can't automate)
- Multiple valid paths (flexibility needed)
- Compliance good with reminder (>90%)

---

## 4. Validating Heuristics and Checklists

### Testing Heuristics

**Retrospective validation**: Test heuristic on historical cases.

**Method**:
1. Collect past decisions (N ≥ 30 cases)
2. Apply heuristic to each case (blind to actual outcome)
3. Compare heuristic decision to actual outcome
4. Calculate accuracy: % cases where heuristic would've chosen correctly

**Target accuracy**: ≥80% for good heuristic. <70% → Refine or abandon.

**Example** (Hiring heuristic):
- Heuristic: "Hire candidates from top 10 tech companies"
- Test on past 50 hires
- Outcome: 40/50 (80%) from top companies succeeded, 5/10 (50%) from others
- **Conclusion**: Heuristic valid (80% > 50% base rate)

### A/B Testing Heuristics

**Prospective validation**: Run controlled experiment.

**Method**:
1. Group A: Use heuristic
2. Group B: Use existing method (or random)
3. Compare outcomes (quality, speed, consistency)

**Example**:
- A: Customer routing by fast & frugal tree
- B: Customer routing by availability
- **Metrics**: Response time, resolution rate, customer satisfaction
- **Result**: A faster (20% ↓ response time), higher satisfaction (8.2 vs. 7.5) → Adopt heuristic

### Checklist Validation

**Error rate measurement**:

**Before checklist**:
- Track error rate for procedure (e.g., deployments with failures)
- Baseline: X% error rate

**After checklist**:
- Introduce checklist
- Track error rate for same procedure
- New rate: Y% error rate
- **Improvement**: (X - Y) / X × 100%

**Target**: ≥50% error reduction. If <25%, checklist not effective.

**Example** (Surgical checklist):
- Before: 11% complication rate
- After: 7% complication rate
- **Improvement**: (11 - 7) / 11 = 36% reduction (good, continue using)

---

## 5. Refinement and Iteration

### When Heuristics Fail

**Diagnostic questions**:
1. **Wrong cue**: Are we using the best predictor? Try different criterion.
2. **Threshold too high/low**: Should we raise/lower aspiration level?
3. **Environment changed**: Did market shift, competition intensify, technology disrupt?
4. **Exceptions accumulating**: Are special cases becoming the norm? Need more complex rule.

**Refinement strategies**:
- **Add exception**: "Use heuristic EXCEPT when [condition]"
- **Adjust threshold**: Satisficing level up/down based on outcomes
- **Switch cue**: Use different criterion if current one losing validity
- **Add layer**: Convert simple rule to fast & frugal tree (2-3 questions max)

### When Checklists Fail

**Diagnostic questions**:
1. **Too long**: Are people skipping because overwhelming? → Cut to killer items only.
2. **Wrong format**: Are experts resisting READ-DO? → Switch to DO-CONFIRM.
3. **Missing critical step**: Did error happen that checklist didn't catch? → Add item.
4. **False sense of security**: Are people checking boxes without thinking? → Add verification.

**Refinement strategies**:
- **Shorten**: Remove non-critical items. Aim for 5-9 items.
- **Reformat**: Switch READ-DO ↔ DO-CONFIRM based on user feedback.
- **Add forcing function**: Critical items become automated checks (not manual).
- **Add challenge-response**: Two-person verification for high-stakes items.

---

## 6. Cognitive Biases and Mitigation

### Availability Bias

**Definition**: Judge frequency/probability by ease of recall. Recent, vivid events seem more common.

**How it misleads heuristics**:
- Plane crash on news → Overestimate flight risk
- Recent fraud case → Overestimate fraud rate
- Salient failure → Avoid entire category

**Mitigation**:
- Use base rates (statistical frequencies) not anecdotes
- Ask: "What's the actual data?" not "What do I remember?"
- Track all cases, not just memorable ones

**Example**:
- Availability: "Customer from [Country X] didn't pay, avoid all [Country X] customers"
- Base rate check: "Only 2% of [Country X] customers defaulted vs. 1.5% overall" → Marginal difference, not categorical

### Representativeness Bias

**Definition**: Judge probability by similarity to stereotype/prototype. "Looks like X, therefore is X."

**How it misleads heuristics**:
- "Looks like successful founder" (hoodie, Stanford, articulate) → Overestimate success
- "Looks like good engineer" (quiet, focused) → Miss great communicators

**Mitigation**:
- Use objective criteria (track record, test scores) not stereotypes
- Check base rate: How often does stereotype actually predict outcome?
- Blind evaluation: Remove identifying information

**Example**:
- Representativeness: "Candidate reminds me of [successful person], hire"
- Base rate: "Only 5% of hires succeed regardless of who they remind me of"

### Anchoring Bias

**Definition**: Over-rely on first piece of information. Initial number shapes estimate.

**How it misleads heuristics**:
- First salary offer anchors negotiation
- Initial project estimate anchors timeline
- First price seen anchors value perception

**Mitigation**:
- Set your own anchor first (make first offer)
- Deliberately adjust away from anchor (mental correction)
- Use external reference (market data, not internal anchor)

**Example**:
- Anchoring: Candidate asks $150k, you offer $155k (anchored to their ask)
- Better: You offer $130k first (your anchor), negotiate from there

### Confirmation Bias

**Definition**: Seek, interpret, recall information confirming existing belief. Ignore disconfirming evidence.

**How it misleads heuristics**:
- Heuristic works once → Notice only confirming cases
- Initial hypothesis → Search for supporting evidence only

**Mitigation**:
- Actively seek disconfirming evidence ("Why might this heuristic fail?")
- Track all cases (not just successes)
- Pre-commit to decision rule, then test objectively

**Example**:
- Confirmation: "Recognition heuristic worked on 3 cases!" (ignore 5 failures)
- Mitigation: Track all 50 cases → 25/50 = 50% accuracy (coin flip, abandon heuristic)

### Sunk Cost Fallacy

**Definition**: Continue based on past investment, not future value. "Already spent X, can't stop now."

**How it misleads heuristics**:
- Heuristic worked in past → Keep using despite declining accuracy
- Spent time designing checklist → Force it to work despite low adoption

**Mitigation**:
- Evaluate based on future value only ("Will this heuristic work going forward?")
- Pre-commit to abandonment criteria ("If accuracy <70%, switch methods")
- Ignore past effort when deciding

**Example**:
- Sunk cost: "Spent 10 hours designing this heuristic, must use it"
- Rational: "Heuristic only 60% accurate, abandon and try different approach"

---

## Advanced Topics

### Swiss Cheese Model (Error Prevention)

**James Reason's model**: Multiple defensive layers, each with holes. Error occurs when holes align.

**Layers**:
1. Organizational (policies, culture)
2. Supervision (oversight, review)
3. Preconditions (fatigue, time pressure)
4. Actions (individual performance)

**Checklist as defensive layer**: Catches errors that slip through other layers.

**Example** (Deployment failure):
- Organizational: No deployment policy
- Supervision: No code review
- Preconditions: Friday night deployment (fatigue)
- Actions: Developer forgets migration
- **Checklist**: "☐ Database migration tested" catches error

### Adaptive Heuristics

**Concept**: Heuristic parameters adjust based on outcomes.

**Example** (Satisficing with adaptive threshold):
- Start: Threshold = 80% of criteria
- After 10 searches, no options found → Lower to 70%
- After 5 options found → Raise to 85%

**Implementation**:
```
threshold = initial_threshold
search_count = 0
options_found = 0

while not decided:
    search_count += 1
    if option_meets_threshold:
        options_found += 1
        decide(option)
    
    if search_count > K and options_found == 0:
        threshold *= 0.9  # Lower threshold
    if options_found > M:
        threshold *= 1.1  # Raise threshold
```

### Context-Dependent Heuristics

**Concept**: Different rules for different contexts. Meta-heuristic chooses which heuristic to use.

**Example** (Decision approach):
1. **Check context**:
   - Is decision reversible? Yes → Use fast heuristic (satisficing)
   - Is decision irreversible? No → Use slow analysis (full evaluation)

2. **Choose heuristic based on stakes**:
   - <$1k: Recognition heuristic
   - $1k-$10k: Satisficing
   - >$10k: Full analysis

**Implementation**:
```
if stakes < 1000:
    use recognition_heuristic()
elif stakes < 10000:
    use satisficing(threshold=0.8)
else:
    use full_analysis()
```

## Key Takeaways

1. **Heuristics work in stable environments**: Recognition, take-the-best excel when patterns repeat. Fail in novel, adversarial contexts.

2. **Satisficing beats optimization under uncertainty**: "Good enough" faster and often as good as perfect when environment unpredictable.

3. **Checklists catch 60-80% of errors**: Proven in aviation, surgery, construction. Focus on killer items only (5-9 max).

4. **READ-DO for novices, DO-CONFIRM for experts**: Match format to user. Forcing experts into READ-DO creates resistance.

5. **Test heuristics empirically**: Don't assume rules work. Validate on ≥30 historical cases, target ≥80% accuracy.

6. **Forcing functions > checklists for critical steps**: If step must be done, automate enforcement rather than relying on manual check.

7. **Update heuristics when environment changes**: Rules optimized for past may fail when market shifts, tech disrupts, competition intensifies. Re-validate quarterly.
