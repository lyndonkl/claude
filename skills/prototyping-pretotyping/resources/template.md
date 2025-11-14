# Prototyping & Pretotyping Experiment Template

## Workflow

```
Prototyping Progress:
- [ ] Step 1: Identify riskiest assumption to test
- [ ] Step 2: Choose pretotype/prototype approach
- [ ] Step 3: Design and build minimum test
- [ ] Step 4: Run experiment and collect data
- [ ] Step 5: Analyze results and decide
```

## Experiment Design Template

### 1. Assumption to Test

**Assumption**: [What are we assuming? E.g., "Users will pay $49/mo for AI-powered analytics"]
**Why risky**: [Why might this be wrong? Impact if wrong?]
**Risk score**: [Probability wrong (1-5) × Impact if wrong (1-5) = Risk (1-25)]

### 2. Test Method

**Approach**: [Pretotype / Paper / Clickable / Coded / MVP]
**Fidelity choice rationale**: [Why this fidelity level? What question does it answer?]
**Estimated cost**: [$X or X hours]
**Timeline**: [X days to build, Y days to test]

### 3. Success Criteria

**Primary metric**: [E.g., "10% landing page → sign-up conversion"]
**Secondary metrics**: [E.g., "50% complete onboarding, 5 min avg session"]
**Minimum sample**: [n=X users/observations]
**Decision rule**: 
- **Persevere** (build it): [Metric ≥ X means validated]
- **Pivot** (change direction): [Metric < Y means assumption wrong]
- **Iterate** (refine and re-test): [X > Metric ≥ Y means unclear, need more data]

### 4. Experiment Build

**What we're building**: [Landing page, paper prototype, working feature, etc.]
**Components needed**:
- [ ] [Component 1, e.g., Landing page copy/design]
- [ ] [Component 2, e.g., Sign-up form]
- [ ] [Component 3, e.g., Analytics tracking]

**Fake vs Real**:
- **Faking**: [What appears real but isn't? E.g., "Buy Now button shows 'Coming Soon'"]
- **Real**: [What must actually work? E.g., "Email capture must work"]

### 5. Participant Recruitment

**Target users**: [Who are we testing with? Demographics, behaviors, context]
**Sample size**: [n=X, reasoning: qualitative vs quantitative]
**Recruitment method**: [Ads, existing users, outreach, intercepts]
**Screening**: [How do we ensure target users? Screener questions]

### 6. Data Collection Plan

**Quantitative data**:
| Metric | How measured | Tool | Target |
|--------|--------------|------|--------|
| [Sign-ups] | [Form submissions] | [Google Analytics] | [≥100] |
| [Conversion] | [Sign-ups / Visitors] | [GA] | [≥10%] |

**Qualitative data**:
| Method | N | Questions/Tasks |
|--------|---|-----------------|
| [User interview] | [5-10] | [What problem were you trying to solve? Did prototype help?] |
| [Task observation] | [10] | [Complete checkout, note errors/confusion] |

### 7. Results

**Quantitative**:
| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| [Sign-ups] | [≥100] | [X] | [✓ / ✗] |
| [Conversion] | [≥10%] | [Y%] | [✓ / ✗] |

**Qualitative**:
- **Observation 1**: [E.g., "7/10 users confused by pricing page"]
- **Observation 2**: [E.g., "All users expected 'Export' feature"]
- **Quote 1**: [User said...]
- **Quote 2**: [User said...]

### 8. Decision

**Decision**: [Persevere / Pivot / Iterate]
**Rationale**: [Why? Which criteria met/not met?]
**Next steps**:
- [ ] [If Persevere: Build MVP with features X, Y, Z]
- [ ] [If Pivot: Test alternative approach A]
- [ ] [If Iterate: Refine prototype addressing issues 1, 2, 3, re-test in 2 weeks]

**Learnings**:
1. [What we learned about assumption]
2. [What surprised us]
3. [What to test next]

---

## Quick Patterns

### Pretotype Methods

**Fake Door Test** (Test demand):
- Build: Landing page "New Feature X - Coming Soon" with "Notify Me" button
- Measure: Click rate, email sign-ups
- Example: "500 visitors, 50 sign-ups (10%) → validates demand"

**Concierge MVP** (Test workflow manually before automating):
- Build: Manual service delivery (no automation)
- Measure: Customer satisfaction, willingness to pay, time spent
- Example: "Manually curate recommendations for 10 users → learn what good looks like before building algorithm"

**Wizard of Oz** (Appear automated, human-powered):
- Build: UI looks automated, humans behind scenes
- Measure: User perception, task success, performance expectations
- Example: "Chatbot UI, humans answering questions → test if users accept chatbot interaction before building NLP"

**Single-Feature MVP** (Test one feature well):
- Build: One core feature, ignore rest
- Measure: Usage, retention, WTP
- Example: "Instagram v1: photo filters only → test if core value enough before building stories/reels"

### Prototype Methods

**Paper Prototype** (Test workflow):
- Build: Hand-drawn screens on paper/cards
- Test: Users "click" on paper, swap screens, observe
- Measure: Task completion, errors, confusion points
- Example: "10 users complete checkout, 3 confused by shipping step → redesign before coding"

**Clickable Prototype** (Test UI/UX):
- Build: Interactive mockup in Figma/InVision (no real code)
- Test: Users complete tasks, measure success/time
- Measure: Completion rate, time, errors, satisfaction
- Example: "20 users, 85% complete task <3 min → validates flow"

**Coded Prototype** (Test feasibility):
- Build: Working code, limited features/data
- Test: Real users, real tasks, measure performance
- Measure: Latency, error rate, scalability, cost
- Example: "Search 10K docs <500ms → validates approach, ready to scale to 10M docs"

### Measurement Approaches

**Quantitative (n=100+)**:
- Conversion rates (landing page → sign-up, sign-up → payment)
- Task completion rates (% who finish checkout)
- Time on task (how long to complete)
- Error rates (clicks on wrong element, form errors)

**Qualitative (n=5-10)**:
- Think-aloud protocol (users narrate thought process)
- Retrospective interview (after task, ask about confusion/delight)
- Observation notes (where they pause, retry, look confused)
- Open-ended feedback (what worked, what didn't)

**Behavioral > Opinions**:
- ✓ "50 clicked 'Buy', 5 completed payment" (behavior)
- ❌ "Users said they'd pay $99" (opinion, unreliable)

---

## Quality Checklist

- [ ] Assumption is risky (high probability wrong × high impact if wrong)
- [ ] Fidelity matches question (not overbuilt)
- [ ] Success criteria set before testing (no moving goalposts)
- [ ] Recruited real target users (not friends/family)
- [ ] Sample size appropriate (n=5-10 qualitative, n=100+ quantitative)
- [ ] Measuring behavior (clicks, conversions), not just opinions
- [ ] Clear decision rule (persevere/pivot/iterate thresholds)
- [ ] Results documented and shared with team
