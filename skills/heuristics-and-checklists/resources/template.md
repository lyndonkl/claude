# Heuristics and Checklists Templates

Quick-start templates for designing decision heuristics and error-prevention checklists.

## Decision/Procedure Identification Template

**What needs simplification?**

**Type**: [Decision / Procedure]

**Frequency**: [How often does this occur? Daily / Weekly / Monthly]

**Current approach**: [How is this currently done?]

**Problems with current approach**:
- [ ] Too slow (takes [X] hours/days)
- [ ] Inconsistent outcomes (variance in quality)
- [ ] Errors frequent ([X]% error rate)
- [ ] Cognitive overload (too many factors to consider)
- [ ] Analysis paralysis (can't decide, keep searching)
- [ ] Knowledge not transferable (depends on expert intuition)

**Goal**: [What do you want to achieve? Faster decisions? Fewer errors? Consistent quality?]

---

## Heuristic Design Template

### Step 1: Define the Decision

**Decision question**: [What am I choosing?]
- Example: "Which job candidate to hire?"
- Example: "Which customer segment to prioritize?"

**Options**: [What are the alternatives?]
1. [Option A]
2. [Option B]
3. [Option C]
...

### Step 2: Choose Heuristic Type

**Type selected**: [Recognition / Take-the-Best / Satisficing / Fast & Frugal Tree]

#### Option A: Recognition Heuristic

**Rule**: If you recognize one option but not the other, choose the recognized one.

**Applies when**:
- Recognition correlates with quality (brands, cities, experts)
- Environment stable (not deceptive advertising)

**Example**: "Choose candidate from company I recognize (Google, Amazon) over unknown startup"

#### Option B: Take-the-Best Heuristic

**Most important criterion**: [What single factor best predicts outcome?]

**Rule**: Choose the option that scores best on this criterion alone. Ignore other factors.

**Example**: "For hiring engineers, use 'coding test score' only. Ignore school, years experience, personality."

**Cue validity**: [How often does this criterion predict success? Aim for >70%]

#### Option C: Satisficing

**Minimum acceptable threshold**: [What criteria must be met?]

| Criterion | Minimum | Notes |
|-----------|---------|-------|
| [Criterion 1] | [Threshold] | [e.g., "Coding score ≥80%"] |
| [Criterion 2] | [Threshold] | [e.g., "Experience ≥2 years"] |
| [Criterion 3] | [Threshold] | [e.g., "Culture fit ≥7/10"] |

**Rule**: Choose first option that meets ALL thresholds. Stop searching.

**Search budget**: [How many options to evaluate before lowering threshold? e.g., "Evaluate 3 candidates, if none meet threshold, adjust."]

#### Option D: Fast & Frugal Tree

**Decision tree**:

```
Question 1: [Binary question, e.g., "Is deal >$10k?"]
├─ Yes → [Action A or Question 2]
└─ No → [Action B]

Question 2: [Next binary question]
├─ Yes → [Action C]
└─ No → [Action D]
```

**Example** (Customer routing):
```
Is customer enterprise (>1000 employees)?
├─ Yes → Assign senior rep
└─ No → Is deal value >$10k?
    ├─ Yes → Assign mid-level rep
    └─ No → Self-serve flow
```

### Step 3: Define Exceptions

**When this heuristic should NOT be used**:
- [Condition 1: e.g., "Novel situation with no precedent"]
- [Condition 2: e.g., "Stakes >$100k (requires full analysis)"]
- [Condition 3: e.g., "Adversarial environment (deception likely)"]

---

## Checklist Design Template

### Step 1: Identify Critical Steps

**Procedure**: [What process needs a checklist?]

**Brainstorm all steps** (comprehensive list first):
1. [Step 1]
2. [Step 2]
3. [Step 3]
...

**Filter to critical steps** (keep only steps that meet ≥1 criterion):
- [ ] Often skipped (easy to forget)
- [ ] Serious consequences if missed (failures, errors, safety risks)
- [ ] Not immediately obvious (requires deliberate check)

**Critical steps** (5-10 items max):
1. [Critical step 1]
2. [Critical step 2]
3. [Critical step 3]
4. [Critical step 4]
5. [Critical step 5]

### Step 2: Choose Checklist Format

**Format**: [READ-DO / DO-CONFIRM / Challenge-Response]

**Guidance**:
- **READ-DO**: Novices, unfamiliar procedures, irreversible actions
- **DO-CONFIRM**: Experts, routine procedures, familiar tasks
- **Challenge-Response**: Two-person verification for high-stakes

### Step 3: Write Checklist

**Checklist title**: [e.g., "Software Deployment Pre-Flight Checklist"]

**Pause points**: [When to use this checklist?]
- Before: [e.g., "Before initiating deployment"]
- During: [e.g., "After migration, before going live"]
- After: [e.g., "Post-deployment verification"]

**Format template** (READ-DO):

```
[CHECKLIST TITLE]

☐ [Verb-first action 1]
   └─ [Specific detail or criteria if needed]

☐ [Verb-first action 2]

⚠ [KILLER ITEM - must pass to proceed]

☐ [Verb-first action 3]

☐ [Verb-first action 4]

☐ [Verb-first action 5]

All items checked → Proceed with [next phase]
```

**Format template** (DO-CONFIRM):

```
[CHECKLIST TITLE]

Perform procedure from memory, then confirm each item:

☐ [Action 1 completed?]
☐ [Action 2 completed?]
☐ [Action 3 completed?]
☐ [Action 4 completed?]
☐ [Action 5 completed?]

All confirmed → Procedure complete
```

---

## Example Heuristics

### Example 1: Hiring Decision (Satisficing)

**Decision**: Choose job candidate from pool

**Satisficing threshold**:
| Criterion | Minimum |
|-----------|---------|
| Technical skills (coding test) | ≥75% |
| Communication (interview rating) | ≥7/10 |
| Culture fit (team feedback) | ≥7/10 |
| Reference check | Positive |

**Rule**: Evaluate candidates in order received. First candidate meeting ALL thresholds → Hire immediately. Don't keep searching for "perfect" candidate.

**Search budget**: If first 5 candidates don't meet threshold, lower bar to 70% technical (but keep other criteria).

### Example 2: Investment Decision (Take-the-Best)

**Decision**: Which startup to invest in?

**Most predictive criterion**: Founder track record (prior exits or significant roles)

**Rule**: Rank startups by founder quality alone. Invest in top 2. Ignore market size, product, traction (assume cue validity of founder >70%).

**Validation**: Test on past investments. If founder track record predicts success <70% of time, switch to different criterion.

### Example 3: Customer Triage (Fast & Frugal Tree)

**Decision**: How to route incoming customer inquiry?

**Tree**:
```
Is customer enterprise (>1000 employees)?
├─ Yes → Assign to senior account exec (immediate response)
└─ No → Is issue billing/payment?
    ├─ Yes → Assign to finance team
    └─ No → Is trial user (not paid)?
        ├─ Yes → Self-serve knowledge base
        └─ No → Assign to support queue (24h SLA)
```

---

## Example Checklists

### Example 1: Software Deployment (READ-DO)

```
Software Deployment Pre-Flight Checklist

☐ All tests passing
   └─ Unit, integration, E2E tests green

⚠ Database migrations tested on staging
   └─ KILLER ITEM - Deployment blocked if migrations fail

☐ Rollback plan documented
   └─ Link to runbook: [URL]

☐ Monitoring dashboards configured
   └─ Alerts set for error rate, latency, traffic

☐ On-call engineer identified and notified
   └─ Name: [___], Phone: [___]

☐ Stakeholders notified of deployment window
   └─ Email sent with timing and impact

☐ Feature flags configured
   └─ Gradual rollout enabled (10% → 50% → 100%)

☐ Backups completed
   └─ Database backup timestamp: [___]

All items checked → Proceed with deployment
```

### Example 2: Aviation Pre-Flight (DO-CONFIRM)

```
Pre-Flight Checklist (DO-CONFIRM)

Perform checks, then confirm:

☐ Fuel quantity verified (visual + gauge)
☐ Flaps freedom of movement checked
☐ Landing gear visual inspection complete
☐ Oil level within limits
☐ Control surfaces free and correct
☐ Instruments verified (altimeter, compass, airspeed)
☐ Seatbelts and harness secured
☐ Flight plan filed

All confirmed → Cleared for takeoff
```

### Example 3: Surgical Safety (WHO Checklist - Challenge/Response)

```
WHO Surgical Safety Checklist - Time Out (Before Incision)

[Entire team pauses, nurse reads aloud, surgeon confirms each]

☐ Confirm patient identity
   Response: "Name: [___], DOB: [___]"

☐ Confirm surgical site and procedure
   Response: "Site marked, procedure: [___]"

☐ Anticipated critical events reviewed
   Response: "Surgeon: [Key steps], Anesthesia: [Concerns], Nursing: [Equipment ready]"

☐ Antibiotic prophylaxis given within 60 min
   Response: "Administered at [time]"

☐ Essential imaging displayed
   Response: "[X-ray/MRI] displayed and reviewed"

All confirmed → Surgeon may proceed with incision
```

---

## Application & Monitoring Template

### Applying Heuristic

**Heuristic being applied**: [Name of rule]

**Case log**:

| Date | Decision | Heuristic Used | Outcome | Notes |
|------|----------|----------------|---------|-------|
| [Date] | [What decided] | [Which rule] | [Good / Bad] | [What happened] |
| [Date] | [What decided] | [Which rule] | [Good / Bad] | [What happened] |

**Success rate**: [X good outcomes / Y total decisions = Z%]

**Goal**: ≥80% good outcomes. If <80%, refine heuristic.

### Applying Checklist

**Checklist being applied**: [Name of checklist]

**Usage log**:

| Date | Procedure | Items Caught | Errors Prevented | Time Added |
|------|-----------|--------------|------------------|------------|
| [Date] | [What done] | [# items flagged] | [What would've failed] | [+X min] |
| [Date] | [What done] | [# items flagged] | [What would've failed] | [+X min] |

**Error rate**:
- Before checklist: [X% failure rate]
- After checklist: [Y% failure rate]
- **Improvement**: [(X-Y)/X × 100]% reduction

---

## Refinement Log Template

**Iteration**: [#1, #2, #3...]

**Date**: [When refined]

**Problem identified**: [What went wrong? When did heuristic/checklist fail?]

**Root cause**: [Why did it fail?]
- [ ] Heuristic: Wrong criterion chosen, threshold too high/low, environment changed
- [ ] Checklist: Missing critical step, too long (skipped), wrong format for user

**Refinement made**:
- **Before**: [Old rule/checklist]
- **After**: [New rule/checklist]
- **Rationale**: [Why this change should help]

**Test plan**: [How to validate refinement? Test on X cases, monitor for Y weeks]

**Outcome**: [Did refinement improve performance? Yes/No, by how much?]
