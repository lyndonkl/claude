# Prototyping & Pretotyping: Advanced Methodologies

## Table of Contents
1. [Pretotyping Techniques](#1-pretotyping-techniques)
2. [Fidelity Selection Framework](#2-fidelity-selection-framework)
3. [Experiment Design Principles](#3-experiment-design-principles)
4. [Measurement and Validation](#4-measurement-and-validation)
5. [Common Failure Patterns](#5-common-failure-patterns)

## 1. Pretotyping Techniques

### Fake Door Test
**What**: Feature appears in UI but doesn't exist yet
**Setup**: Add button/link "New Feature X", tracks clicks, shows "Coming Soon"
**Measures**: Click-through rate (interest), wait list sign-ups (intent)
**Example**: Amazon tested new category by showing link, measuring clicks before building inventory
**When**: Test demand for new feature/product before building

### Concierge MVP
**What**: Manually deliver service that will eventually be automated
**Setup**: Humans do work (curation, matching, analysis) as if algorithm did it
**Measures**: Customer satisfaction, willingness to pay, time/cost to deliver manually
**Example**: Food delivery app founders manually taking orders/delivering before building platform
**When**: Learn what "good" looks like before automating, validate service value proposition

### Wizard of Oz
**What**: System appears automated but humans power it behind scenes
**Setup**: Build UI, users interact thinking it's automated, humans respond in real-time
**Measures**: User acceptance of automated experience, performance expectations, edge cases
**Example**: IBM speech recognition - person typing what user said, appeared like AI transcription
**When**: Test if users accept automated interface before building complex AI/automation

### Painted Door
**What**: Feature shown in UI as "Beta" or "Early Access" but not built yet
**Setup**: Badge/flag on fake feature, measure attempts to access
**Measures**: Click rate, request rate for access
**Example**: Slack showed "Calls" feature as "Beta", measured requests before building voice infrastructure
**When**: Test interest in feature when UI space is limited (avoiding clutter)

### Single-Feature MVP
**What**: Build one feature extremely well, ignore everything else
**Setup**: Identify core value hypothesis, build only that feature
**Measures**: Retention (do users come back?), engagement (how often used?), WTP (will they pay?)
**Example**: Twitter v1 - just 140-char posts, no replies/retweets/hashtags/DMs
**When**: Test if core value alone is enough before adding features

### Pre-Order / Crowdfunding
**What**: Collect money before building product
**Setup**: Landing page with product description, pre-order button, collect payments
**Measures**: Conversion rate (visitors → buyers), funding amount vs target
**Example**: Pebble smartwatch raised $10M on Kickstarter before manufacturing
**When**: Test willingness to pay and validate demand with financial commitment

### Explainer Video
**What**: Video showing product in use before building it
**Setup**: 2-3 min video demonstrating value prop, post to landing page, measure sign-ups
**Measures**: View-to-signup conversion, qualitative feedback in comments
**Example**: Dropbox video (3min) drove 70K→75K beta sign-ups overnight (10% conversion)
**When**: Complex product hard to explain in text, want viral sharing

### Manual-First Approach
**What**: Do work manually before building tools/automation
**Setup**: Spreadsheets, email, manual processes instead of software
**Measures**: Feasibility (can we do manually?), bottlenecks (what takes time?), quality (output good enough?)
**Example**: Zapier founders manually connecting APIs for first customers before building platform
**When**: Learn workflow requirements before automation, validate service value before tooling

## 2. Fidelity Selection Framework

### Decision Matrix

| Question | Recommended Fidelity | Timeline | Cost |
|----------|---------------------|----------|------|
| Do people want this? | Pretotype (Fake Door) | Hours-Days | $0-100 |
| Will they pay $X? | Pretotype (Pricing on landing page) | Days | $0-500 |
| Is workflow intuitive? | Paper Prototype | Hours-Days | $0-50 |
| Do interactions feel right? | Clickable Prototype | Days-Week | $100-500 |
| Can we build technically? | Coded Prototype | Weeks | $1K-10K |
| Will they retain/engage? | MVP | Months | $10K-100K+ |

### Fidelity Ladder Climber

Start low fidelity, climb only if validated:

1. **Pretotype** (Fake Door): 5% conversion → demand validated → climb to prototype
2. **Paper Prototype**: 8/10 users complete workflow → UX validated → climb to clickable
3. **Clickable Prototype**: 15% task completion <2 min → flow validated → climb to coded
4. **Coded Prototype**: <500ms latency at 100 req/sec → technical validated → build MVP
5. **MVP**: 40% week-1 retention → value validated → build full product

**Don't skip steps**: Each step de-risks before higher investment

### Cost-Benefit Analysis

**Example - Should we code prototype or stick with clickable?**

Clickable prototype cost: $500 (1 week designer)
Coded prototype cost: $8K (1 month engineer)
**Delta**: $7.5K, 3 weeks

Information gained from coded vs clickable:
- Performance data (real latency, not estimated)
- Integration complexity (real API issues, not mocked)
- Scalability constraints (actual database limits)

**Is $7.5K worth it?**
- If performance/integration unknown and high risk: Yes (de-risking worth cost)
- If performance/integration well-understood: No (clickable sufficient)

## 3. Experiment Design Principles

### Minimum Viable Data

**Qualitative**: n=5-10 for pattern identification (Nielsen Norman Group: 5 users find 85% of usability issues)
**Quantitative**: n=100+ for statistical confidence (conversions, A/B tests)

**Don't over-collect**: More users = more time/cost. Stop when pattern clear.

### Success Criteria Template

**Good criteria** (set before testing):
- Specific: "10% landing page conversion"
- Measurable: Can be tracked with analytics
- Actionable: Tells you to pivot or persevere
- Realistic: Based on industry benchmarks
- Time-bound: "In 2 weeks"

**Decision thresholds**:
- **Persevere**: ≥10% conversion → validated, build it
- **Pivot**: <5% conversion → assumption wrong, change direction
- **Iterate**: 5-10% conversion → unclear, refine and re-test

### Bias Mitigation

**Confirmation bias**: Seeing what we want to see
- Fix: Set success criteria before testing, blind analysis (analyst doesn't know hypothesis)

**Sampling bias**: Testing wrong users
- Fix: Screen participants (e.g., "Do you currently use X?"), recruit from target segment

**Social desirability bias**: Users say what's polite
- Fix: Observe behavior (clicks, time), don't just ask opinions

**Leading questions**: "Wouldn't you love feature X?"
- Fix: Neutral framing: "How would you solve problem Y?"

## 4. Measurement and Validation

### Behavioral Metrics (Reliable)

**Pre-commitment signals** (ranked by strength):
1. **Paid**: Actual payment (strongest signal)
2. **Pre-ordered**: Credit card on file, will be charged later
3. **Waitlist with phone/email**: Provided contact info
4. **Clicked "Buy"**: Navigated to checkout (even if abandoned)
5. **Clicked feature**: Showed interest by interaction

**Engagement metrics**:
- Task completion rate: % who finished workflow
- Time on task: How long (too long = confusing)
- Error rate: Mis-clicks, form errors
- Return visits: Came back without prompt
- Referrals: Told others (strongest retention signal)

### Opinion Metrics (Less Reliable)

**Survey responses**: "Would you pay $X?" (70% say yes, 10% actually pay → 7× overestimate)
**Net Promoter Score**: "Would you recommend?" (aspirational, not predictive)
**Satisfaction ratings**: "How satisfied?" (grade inflation, social desirability)

**Use opinions for context, not decisions**: "Why did you abandon checkout?" (explains behavior) not "Would you buy this?" (unreliable prediction)

### Statistical Confidence

**Sample size for conversions**:
- Baseline conversion: 10%
- Want to detect: 2% change (10% → 12%)
- Confidence: 95%
- **Required sample**: ~1,000 per variant (use online calculators)

**Too small sample**: False confidence (random noise looks like signal)
**Too large sample**: Wasted time/money (pattern already clear at n=200)

### Qualitative Analysis

**Thematic coding**:
1. Collect observations/quotes (n=10 interviews)
2. Identify recurring themes (e.g., "confused by pricing", "wanted export feature")
3. Count frequency (7/10 mentioned pricing confusion)
4. Prioritize by frequency + severity

**Think-aloud protocol**:
- Users narrate thoughts while completing task
- Reveals mental model mismatches: "I expected X here but saw Y"
- Uncovers unspoken assumptions: "I assume this button does..."

## 5. Common Failure Patterns

### Overbuilding

**Symptom**: Coded prototype for question answerable with landing page
**Root cause**: Excitement to build, uncomfortable with "fakery", underestimating learning from cheap tests
**Fix**: Force fidelity ladder (start low, justify climbing), set "maximum time to first test" (e.g., 1 week)

### No Success Criteria

**Symptom**: Ran test, got data, unclear what it means
**Root cause**: Didn't define success before testing, moving goalposts
**Fix**: Write success criteria document before building prototype, get stakeholder sign-off

### Testing with Wrong Users

**Symptom**: Positive feedback from test, market launch flops
**Root cause**: Tested with friends/family (not target), convenience sample (not representative)
**Fix**: Screen participants (qualifying questions), recruit from target segment (ads, outreach)

### Opinion over Behavior

**Symptom**: "Users loved it in interviews" but no one uses product
**Root cause**: Relying on what users say, not what they do (social desirability, hypothetical bias)
**Fix**: Measure behavior (clicks, payments, retention) as primary, opinions as secondary context

### Single Test Overconfidence

**Symptom**: One test shows X, assume validated forever
**Root cause**: Confirmation bias, small sample, didn't test alternatives
**Fix**: Multiple tests, test variations, update beliefs with new evidence

### Prototype Becomes Product

**Symptom**: Shipped prototype code, now have technical debt/security issues
**Root cause**: Pressure to ship fast, reluctance to "throw away" working code
**Fix**: Treat prototypes as disposable (document learnings, rebuild properly for production)

### Analysis Paralysis

**Symptom**: Months refining prototype before testing
**Root cause**: Perfectionism, fear of negative feedback, unclear scope
**Fix**: Time-box prototype building (e.g., 1 week max), test with "good enough" version

### Ignoring Negative Results

**Symptom**: Test shows assumption wrong, but team proceeds anyway (sunk cost fallacy)
**Root cause**: Ego, sunk cost, optimism bias ("this time will be different")
**Fix**: Pre-commit to decision rule ("if conversion <5%, we pivot"), make pivoting psychologically safe
