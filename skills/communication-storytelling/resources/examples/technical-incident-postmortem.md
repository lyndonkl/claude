# Example: Technical Incident Postmortem

## Scenario

**Context:** Major database outage affected 80% of customers for 4 hours on a Saturday. Need to communicate to executive team on Monday.

**Audience:** CEO, CTO, VP Product, VP Customer Success
- Expertise: Mixed (CEO non-technical, others technical)
- Concerns: Customer impact, reputation, revenue risk, engineering capability
- Time available: 15 minutes in emergency exec meeting

**Purpose:** Build trust through accountability, explain root cause, commit to prevention

**Tone:** Serious but measured, accountable not defensive, solution-oriented

---

## Story Structure Used

**Crisis Communication Arc (Trust Building):**
1. Acknowledge problem honestly
2. Show accountability and action taken
3. Explain root cause and prevention
4. Commit to transparency and improvement

---

## Draft: Communication

### Before (Weak - Data Dump)

> Subject: Database Incident - Saturday Nov 2
>
> On Saturday November 2nd from 2:14am to 6:47am PT, our primary database experienced corrupted indexes causing query failures. 80% of customer requests returned errors. The incident was triggered by a combination of factors including a schema migration deployed on Friday evening and increased load from a batch job. We rolled back the migration at 5:30am which partially restored service. Full recovery occurred at 6:47am after rebuilding indexes.
>
> Impact: 4h 33min outage, 847 customers affected, 12,400 failed requests. Root cause was insufficient testing of migration under production load patterns. We are implementing better testing procedures.
>
> Let me know if you have questions.

**Problems:**
- ❌ Buries emotional acknowledgment (no empathy for customer impact)
- ❌ Technical jargon obscures key insights ("corrupted indexes" - what does that mean for business?)
- ❌ Passive voice avoids accountability ("was triggered by" - who's responsible?)
- ❌ Vague prevention ("better testing" - what specifically?)
- ❌ No explicit commitment to transparency

### After (Strong - Storytelling)

> Subject: Saturday Outage: What Happened, Why, and What We're Doing About It
>
> # We Failed 80% of Our Customers on Saturday
>
> On Saturday at 2am, our main database went down, affecting 80% of customers for 4.5 hours. This is unacceptable. Our customers trust us to keep their businesses running, and we broke that trust. Here's what happened, why it happened, and how we're ensuring it never happens again.
>
> ## What Happened
>
> **Timeline:**
> - **2:14am:** Automated monitoring alerted on-call engineer (Sarah) to 80% error rate
> - **2:20am:** Sarah paged database team, identified corrupted database indexes causing all queries to fail
> - **2:45am:** CTO (me) joined incident call after Sarah escalated
> - **5:30am:** Rolled back Friday's schema migration, partially restored service (50% → 80% success rate)
> - **6:47am:** Fully recovered after manually rebuilding indexes
>
> **Customer Impact:**
> - 847 customers (80% of active base) affected
> - 12,400 failed requests (orders, login attempts, data syncs)
> - 23 support tickets filed, 8 customers escalated to executives
> - Estimated revenue impact: $15K in SLA credits
>
> **Our Response:**
> - 6 engineers worked through the night
> - We proactively emailed all affected customers by 8am Saturday with status and apology
> - We held customer office hours Sunday 2-6pm (47 customers attended)
> - We're issuing automatic SLA credits (no request needed)
>
> ## Why It Happened (Root Cause)
>
> **Immediate cause:** Friday evening we deployed a database schema migration (adding index to support new feature). Under normal load, this worked fine in staging. But Saturday at 2am, a scheduled batch job ran that queries the same table. The combination of migration + batch job created a race condition that corrupted the index.
>
> **Underlying causes (honest reflection):**
> 1. **Insufficient testing:** We tested the migration, but not under realistic load patterns that include batch jobs
> 2. **Risky timing:** Deploying database changes Friday evening meant skeleton crew if problems emerged
> 3. **Missing safeguards:** Batch job didn't have circuit breaker to stop if error rate spiked
>
> **I take responsibility.** As CTO, I approved the deployment plan that didn't account for batch job interaction. The engineering team followed our process—the process was inadequate.
>
> ## What We're Doing About It
>
> **Immediate (This Week):**
> 1. **Deployment freeze:** No schema changes until new process is in place (unfreezes Nov 10)
> 2. **Load testing:** Adding batch job scenarios to staging environment (reproduces Saturday's load pattern)
> 3. **Circuit breakers:** Batch jobs now halt if error rate >5% (prevents cascading failures)
>
> **Short-term (Next 30 Days):**
> 1. **Deployment policy:** No risky changes on Fridays or weekends (lessons from Saturday)
> 2. **Runbook updates:** Document recovery procedures for index corruption (today it was tribal knowledge)
> 3. **Customer communication template:** Pre-written incident comms for <30min response time
>
> **Long-term (Next Quarter):**
> 1. **Incident response training:** All engineers will complete tabletop exercises (scheduled for Dec)
> 2. **Database reliability investment:** Hiring database SRE, implementing automated failover
> 3. **Proactive monitoring:** Detect schema migration risks before they reach production
>
> ## Transparency Commitment
>
> **Public postmortem:** I'm publishing a blameless postmortem on our engineering blog by Friday (I'll share draft with you first for input). Customers deserve to know we're taking this seriously and learning from it.
>
> **Monthly reliability reports:** Starting this month, I'll share incident metrics at exec meetings (MTTR, incident count, severity breakdown) so you have visibility into trends.
>
> **Ask anything:** I know you'll have questions. I'm available all day Monday—no meeting too small, no question too uncomfortable.
>
> ## What I Need from You
>
> 1. **Approval for database SRE hire** (unplanned $180K/year) - this is our #1 reliability gap
> 2. **Customer outreach support** - If any of the 8 executive escalations need personal attention from CEO/CTO, let me know
> 3. **Patience** - We'll have fewer feature releases next 2 weeks while we prioritize reliability
>
> I'm deeply sorry for this failure. Our customers and our team deserved better. We're fixing it.
>
> —CTO Name
>
> **Office hours:** Monday 9am-6pm, my door is open

**Why This Works:**

✅ **Headline:** Acknowledges failure explicitly ("We Failed") - shows accountability, builds trust
✅ **Structure:** What/Why/What We're Doing - clear, logical flow
✅ **Specificity:** Exact numbers (847 customers, 4.5 hours, $15K) not vague ("many," "several")
✅ **Accountability:** "I take responsibility" (named CTO) vs passive "mistakes were made"
✅ **Show don't tell:** Timeline with timestamps shows urgency, not just "we responded quickly"
✅ **Humanization:** Named engineer (Sarah), personal language ("deeply sorry"), emotional honesty
✅ **Transparency:** Admits underlying causes (not just immediate trigger), commits to public postmortem
✅ **Credibility:** Concrete actions with timelines (not vague "we'll do better")
✅ **Stakes:** Shows revenue impact ($15K SLA credits) and customer escalations (8 to executives)
✅ **Call-to-action:** Specific asks (SRE hire approval, customer outreach, patience on features)
✅ **Accessibility:** "Office hours Monday 9am-6pm" - invites conversation, not defensive

---

## Self-Assessment Using Rubric

**Headline Clarity (5/5):** "We Failed 80% of Our Customers" - impossible to misunderstand
**Structure (5/5):** What/Why/What We're Doing + Transparency Commitment - clear flow
**Evidence Quality (5/5):** Specific data (847 customers, timeline with timestamps, $15K impact)
**Audience Fit (5/5):** Mixed technical/non-technical with explanations, addresses exec concerns (customer impact, revenue, capability)
**Storytelling (5/5):** Shows (timeline, named people) vs tells, humanizes data (8 escalations to executives = serious)
**Accountability (5/5):** CTO takes responsibility explicitly, no passive voice or blame-shifting
**Actionability (5/5):** Concrete preventions with timelines, clear asks with budget impact
**Tone (5/5):** Serious, accountable, solution-oriented - matches crisis situation
**Transparency (5/5):** Admits underlying causes, commits to public postmortem, invites questions
**Credibility (5/5):** Vulnerable (admits inadequate process), shows work (root cause analysis), commits with specifics

**Average: 5.0/5** ✓ Production-ready

---

## Key Techniques Demonstrated

1. **Crisis Communication Pattern:** Acknowledge → Accountability → Action → Transparency
2. **Specificity:** 847 customers (not "many"), 4.5 hours (not "extended"), $15K (not "financial impact")
3. **Named Accountability:** "As CTO, I approved..." (not "the team" or "we")
4. **Timeline Storytelling:** Timestamps create urgency and show response speed
5. **Tiered Actions:** Immediate (this week) / Short-term (30 days) / Long-term (quarter) - shows comprehensive thinking
6. **Vulnerability:** "I take responsibility", "deeply sorry", "customers deserved better" - builds trust through honesty
7. **Stakeholder Addressing:** Customers (SLA credits, office hours), Team (supported through incident), Executives (asks for support)
8. **Open Communication:** "Ask anything", "no question too uncomfortable", "my door is open" - invites dialogue

---

## Alternative Version: External Customer Communication

If communicating to customers (not internal execs), use Before-After-Bridge structure:

**Before:** "On Saturday morning, you may have experienced errors accessing our service. For 4.5 hours, 80% of requests failed."

**After:** "Service is fully restored. We've issued automatic SLA credits to affected accounts (no action needed), and we've implemented safeguards to prevent this specific failure."

**Bridge:** "Here's what happened and what we learned: [simplified root cause without technical jargon]. We're publishing a detailed postmortem on our blog Friday, and I'm personally available for questions: [email]."

**Key differences from internal version:**
- Less technical detail (no "corrupted indexes")
- More emphasis on customer impact and resolution
- Explicit next steps for customers (SLA credits automatic, email for questions)
- Still accountable and transparent, but focused on customer needs not internal process
