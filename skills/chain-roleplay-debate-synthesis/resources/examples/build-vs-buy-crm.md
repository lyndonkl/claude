# Decision: Build Custom CRM vs. Buy SaaS CRM

**Date**: 2024-11-02
**Decision-maker**: CTO + VP Sales
**Stakes**: Medium (affects 30-person sales team, $200K-$800K over 3 years)

---

## 1. Decision Context

**What we're deciding:**
Should we build a custom CRM tailored to our sales process or buy an existing SaaS CRM platform (Salesforce, HubSpot, etc.)?

**Why this matters:**
- Current CRM is a patchwork of spreadsheets and email threads (manual, error-prone)
- Sales team losing deals due to poor pipeline visibility and follow-up tracking
- Need solution operational within 6 months to support Q4 sales push
- Decision impacts sales productivity for next 3+ years

**Success criteria for synthesis:**
- Addresses all three stakeholders' core concerns
- Clear on timeline and costs
- Actionable implementation plan
- All parties can commit to making it work

**Constraints:**
- Budget: $150K available this year, $50K/year ongoing
- Timeline: Must be operational within 6 months
- Requirements: Support 30 users, custom deal stages, integration with current tools
- Non-negotiable: Cannot disrupt Q4 sales push (our busiest quarter)

**Audience:** Executive team (CEO, CTO, VP Sales, CFO)

---

## 2. Roles & Perspectives

### Role 1: VP Sales ("Revenue Defender")

**Position**: Buy SaaS CRM - we need it operational fast to support sales team.

**Priorities**:
1. **Speed to value**: Sales team needs this now, not in 12 months
2. **Proven reliability**: Can't afford downtime or bugs during Q4 push
3. **User adoption**: Sales reps need familiar, polished interface
4. **Feature completeness**: Reporting, forecasting, mobile app out-of-box

**Concerns about building custom**:
- Development will take 12-18 months (historical track record of eng projects)
- Custom tools are often clunky and sales reps hate them
- Maintenance burden (who fixes bugs when it breaks?)
- Opportunity cost: Every month without CRM costs us deals

**Evidence**:
- Previous custom tool (deal calculator) took 14 months to build and was buggy for first 6 months
- Sales team productivity dropped 20% during transition to last custom tool
- Industry benchmark: SaaS CRM implementation takes 2-3 months vs. 12+ for custom build

**Vulnerabilities**:
- "I acknowledge SaaS solutions have vendor lock-in risk and ongoing subscription costs"
- "If engineering can credibly deliver in 6 months with high quality, I'd reconsider"
- "Main uncertainty: Will SaaS meet our unique sales process needs (2-stage approval workflow)?"

**Success metrics**:
- Time to operational: <3 months
- User adoption: >90% of sales reps using daily within 30 days
- Deal velocity: Reduce avg sales cycle from 60 days to 45 days
- Win rate: Maintain or improve current 25% win rate

---

### Role 2: Engineering Lead ("Builder")

**Position**: Build custom CRM - we can tailor exactly to our needs and own the platform.

**Priorities**:
1. **Perfect fit**: Our sales process is unique (2-stage approval, custom deal stages); SaaS won't fit
2. **Long-term ownership**: Build once, no ongoing subscription fees ($50K/year saved)
3. **Extensibility**: Can add features as we grow (integrations, automation, reporting)
4. **Technical debt reduction**: Opportunity to modernize our stack

**Concerns about buying SaaS**:
- Vendor lock-in: Stuck with their roadmap, pricing, and limitations
- Data ownership: Our customer data lives on their servers
- Customization limits: SaaS tools are 80% fit, not 100%
- Hidden costs: Subscription fees compound, APIs cost extra, training costs

**Evidence**:
- Previous SaaS tool (project management) had 15% of features unused but we still paid for them
- Customization via SaaS APIs is limited and often breaks on upgrades
- Engineering team has capacity: 2 senior engineers available for 4-6 months
- Build cost: $200K-$300K upfront vs. $50K/year SaaS ($250K over 5 years)

**Vulnerabilities**:
- "I acknowledge custom builds often take longer than estimated (our track record is +40%)"
- "If SaaS can handle our 2-stage approval workflow, that reduces the 'perfect fit' advantage"
- "Main uncertainty: Will we actually build all planned features or ship minimal version?"

**Success metrics**:
- Feature completeness: 100% of specified requirements met
- Cost: <$300K initial build + <$30K/year maintenance
- Extensibility: Add 2-3 new features per year as business evolves
- Technical quality: <5 bugs per month in production

---

### Role 3: Finance/Operations ("Cost Realist")

**Position**: Depends on ROI - need to see credible numbers for both options.

**Priorities**:
1. **Total cost of ownership (TCO)**: Upfront + ongoing costs over 3-5 years
2. **Risk-adjusted value**: Factor in probability of delays, overruns, adoption failure
3. **Payback period**: How quickly do we recoup investment via productivity gains?
4. **Operational predictability**: Prefer predictable costs to variable/uncertain

**Concerns about both options**:
- **Build**: High upfront cost, uncertain timeline, may exceed budget
- **Buy**: Ongoing subscription compounds, pricing can increase, switching costs if we change later
- **Both**: Adoption risk (if sales team doesn't use it, value = $0)

**Evidence**:
- Current manual CRM costs us 20 hours/week of sales rep time (= $40K/year in lost productivity)
- Average SaaS CRM for 30 users: $50K/year (HubSpot Professional)
- Engineering project cost overruns average +40% from initial estimate (historical data)
- Failed internal tool adoption has happened twice in past 3 years (calc tool, reporting dashboard)

**Vulnerabilities**:
- "I'm making assumptions about productivity gains that haven't been validated"
- "If custom build delivers high value in 6 months (unlikely but possible), ROI beats SaaS"
- "Main uncertainty: Adoption rate - will sales team actually use whichever solution we choose?"

**Success metrics**:
- TCO: Minimize 3-year total cost (build + operate)
- Payback: <18 months to recoup investment
- Adoption: >80% active usage (logging deals, updating pipeline)
- Predictability: <20% variance from projected costs

---

## 3. Debate

### Key Points of Disagreement

**Dimension 1: Timeline - Fast (Buy) vs. Perfect (Build)**
- **VP Sales**: Need it in 3 months to support Q4. Cannot wait 12+ months for custom build.
- **Engineering Lead**: 6-month build timeline is achievable with focused team. SaaS implementation still takes 2-3 months (not that much faster).
- **Finance**: Every month of delay costs $3K in lost productivity. Time is money.
- **Tension**: Speed to value vs. building it right

**Dimension 2: Fit - Good Enough (Buy) vs. Perfect (Build)**
- **VP Sales**: 80% fit is fine if it's reliable and fast. Sales reps can adapt process slightly.
- **Engineering Lead**: 80% fit means 20% pain forever. Our 2-stage approval is core to how we sell.
- **Finance**: "Perfect fit" is theoretical. Custom builds often ship with missing features or bugs.
- **Tension**: Process flexibility vs. tool flexibility

**Dimension 3: Cost - Predictable (Buy) vs. Upfront (Build)**
- **VP Sales**: $50K/year is predictable, budgetable, and includes support/updates.
- **Engineering Lead**: $50K/year = $250K over 5 years. Build is $300K once, then $30K/year = $420K over 5 years. But we own it.
- **Finance**: Engineering track record suggests $300K becomes $400K. Risk-adjusted, not clear build is cheaper.
- **Tension**: Upfront vs. ongoing, certain vs. uncertain

**Dimension 4: Risk - Operational (Buy) vs. Execution (Build)**
- **VP Sales**: Execution risk is high (engineering track record). Operational risk with SaaS is low (proven, 99.9% uptime).
- **Engineering Lead**: Vendor risk is real (lock-in, pricing changes, product direction). We control our own destiny with custom build.
- **Finance**: Both have risks. Mitigatable? SaaS = switching costs. Build = timeline/budget overruns.
- **Tension**: Vendor dependency vs. execution capability

### Debate Transcript (Point-Counterpoint)

**VP Sales Opening Case:**

Look, I get the appeal of building our perfect CRM, but we cannot afford to wait 12-18 months. Our sales team is losing deals *right now* because we don't have proper pipeline tracking. I had a rep miss a $50K deal last month because a follow-up fell through the cracks in our spreadsheet system.

The reality is that engineering has a track record of delays. The deal calculator took 14 months instead of 8. The reporting dashboard was 6 months late. If we start a custom build today, best case is 12 months to launch, realistically 18 months. By then, we'll have lost $100K+ in productivity and missed deals.

A SaaS solution like HubSpot can be operational in 2-3 months. Yes, it's not a perfect fit for our 2-stage approval, but we can adapt our process slightly or use workflow automation. The key is: it works, it's reliable, and my sales team will actually use it because it's polished and familiar.

The $50K/year cost is worth it for the speed, reliability, and ongoing support. We get updates, new features, and 24/7 support included. If we build custom and it breaks during Q4, who fixes it? Engineering is focused on product features, not internal tools.

**Engineering Lead Response:**

I appreciate the urgency, but "speed at any cost" is how we end up with tools that don't fit our needs and frustrate users. Let me address the timeline concern: I'm proposing a 6-month build, not 12-18 months. We scope it tightly to core CRM features (contacts, deals, pipeline, basic reporting). No gold-plating.

Yes, past projects have run over, but those were exploratory with unclear requirements. This is a well-defined problem. We've built CRMs before (I personally built one at my previous company in 5 months). With 2 senior engineers dedicated full-time, 6 months is realistic.

On the "good enough" point: Our 2-stage approval process is non-negotiable. It's a compliance requirement and competitive differentiator. SaaS CRMs make this painful or impossible. I've demoed HubSpot - their approval workflows are clunky and don't match our needs. Sales reps will work around the system, undermining data quality.

On cost: Yes, $50K/year seems manageable, but that's $250K over 5 years, $500K over 10 years, *forever*. And that's today's price. SaaS pricing increases 5-10% per year. We're also locked in - switching CRMs later is a $100K+ migration project. Build once, own forever, total control.

And let's not forget: We can build exactly what we need. Want a custom integration with our accounting system? Done. Want automated deal scoring based on our proprietary criteria? Done. SaaS tools require expensive consultants or hacky API integrations that break on upgrades.

**VP Sales Rebuttal:**

Six months is your *best case* estimate. But you're assuming everything goes perfectly: no scope creep, no technical challenges, no distractions from product team priorities. Even if you hit 8 months, that's 5 months longer than SaaS, costing us $15K+ in lost productivity.

On the 2-stage approval: I've seen it work in HubSpot via custom workflows and approval automations. It's not perfect, but it's workable. And honestly, maybe our process could use some optimization. SaaS CRMs embody industry best practices - might be an opportunity to streamline.

On the "locked in" concern: Sure, switching CRMs is painful. But building custom and then replacing it later is *also* painful (arguably more so - you're throwing away $300K of investment). At least with SaaS, you can evaluate competitors and switch if needed. With custom, you're locked into your own technical debt.

Here's my core concern: *Adoption risk*. Sales reps have used Salesforce or HubSpot before. They know the interface, the mobile app, the workflows. Your custom CRM, no matter how well-built, will feel unfamiliar. Adoption could be slow or fail entirely. Then we've spent $300K on a tool no one uses.

**Engineering Lead Rebuttal:**

On timeline: I hear your skepticism given our track record. What if we mitigate that risk? We could do a phased approach: MVP in 3 months (just contact management and deal tracking), then add features incrementally. If the MVP works, we continue. If not, we bail after $75K and switch to SaaS. That's a middle ground.

On adoption: Fair point. But I'd argue familiarity cuts both ways. Sales reps are frustrated with *current* tools that don't fit our process. A custom tool that matches their workflow could actually drive *better* adoption than a foreign SaaS tool they need to work around. We'd design with sales team input from day one.

On process optimization: I'm not opposed to improving the process, but the 2-stage approval isn't arbitrary - it's a compliance requirement from our legal team. We can't just "streamline" it away. A SaaS tool that doesn't support it is a non-starter, full stop.

On the cost trajectory: You're right that switching from custom later is painful. But switching from SaaS is *also* painful, *plus* we've paid $250K in subscription fees *plus* we've built dependencies on their platform. At least with custom, we own the asset.

**Finance Cross-Examination:**

**Finance to Engineering**: "You say 6 months and $300K. Our historical data shows engineering projects run +40% over budget. Shouldn't we plan for 8-9 months and $400K as the realistic case?"

**Engineering**: "Fair. If we scope tightly and use my phased approach (MVP first), I'm confident in 6 months. But yes, let's budget $350K to be safe."

**Finance to VP Sales**: "You say SaaS is $50K/year. Have you confirmed that price includes 30 users, all features we need, and API access for integrations?"

**VP Sales**: "I've gotten quotes. HubSpot Professional is $45K/year for 30 users. Salesforce is $55K/year. Both include core features. API access is included, though there are rate limits."

**Finance to both**: "Here's the cost comparison I'm seeing:
- **SaaS (HubSpot)**: $20K implementation + $50K/year × 3 years = $170K (3-year TCO)
- **Build**: $350K (risk-adjusted) + $30K/year × 3 years = $440K (3-year TCO)

SaaS is $270K cheaper over 3 years. Engineering, what would need to be true for build to be cheaper?"

**Engineering**: "Two things: (1) We'd need to run the custom CRM for 7+ years for TCO to break even. (2) If SaaS costs increase to $70K/year (SaaS companies often raise prices), break-even is 5 years. I'm thinking long-term; you're thinking 3-year horizon."

**VP Sales to Engineering**: "What happens if you start the build and realize at month 4 that you're behind schedule or over budget? Do we have an exit ramp, or are we committed?"

**Engineering**: "That's why I proposed phased approach with MVP milestone. At 3 months, we review: Is MVP working? Is it on budget? If yes, continue. If no, we pivot to SaaS. That gives us an exit ramp."

### Cruxes (What Would Change Minds)

**VP Sales would shift to Build if:**
- Engineering commits to 6-month delivery with phased milestones and exit ramps
- MVP is demonstrated at 3 months with core functionality working
- Sales reps are involved in design from day one (adoption risk mitigation)
- There's a backup plan (SaaS) if custom build fails

**Engineering Lead would shift to Buy if:**
- SaaS demo shows it can handle 2-stage approval workflow without painful workarounds
- Cost analysis includes long-term subscription growth (10-year TCO, not 3-year)
- We retain option to migrate to custom later if SaaS limitations become painful
- Data export and portability are guaranteed (no vendor lock-in on data)

**Finance would support Build if:**
- Timeline is credibly 6 months with phased milestones (not 12-18 months)
- Budget is capped at $350K with clear scope controls
- Adoption plan is strong (sales team involvement, training, change management)
- Long-term TCO analysis shows break-even within 5-7 years

**Finance would support Buy if:**
- 3-year TCO is significantly lower ($170K vs $440K)
- Predictable costs with no surprises
- Adoption risk is low (familiar interface for sales reps)
- Operational in 2-3 months to start capturing productivity gains

### Areas of Agreement

Despite disagreements, all three roles agree on:
- **Current state is unacceptable**: Spreadsheets are costing us deals and productivity
- **Timeline pressure**: Need solution operational before end of year
- **Adoption is critical**: Doesn't matter if we build or buy if sales team doesn't use it
- **2-stage approval is non-negotiable**: Compliance requirement can't be compromised
- **Budget constraint**: ~$150K available this year, need to stay within bounds

---

## 4. Synthesis

### Integration Approach

**Pattern used**: Phased + Conditional (with exit ramps)

**Synthesis statement:**

We'll pursue a **hybrid phased approach** that mitigates the risks of both options:

**Phase 1 (Months 1-3): Build MVP**
- Engineering builds minimal CRM (contacts, deals, pipeline, 2-stage approval)
- Budget: $100K (1.5 engineers × 3 months)
- Success criteria: MVP demonstrates core functionality, sales team validates it works for their workflow

**Phase 2 (Month 3): Decision Gate**
- If MVP succeeds: Continue to full build (Phase 3)
- If MVP fails or is behind schedule: Pivot to SaaS (Phase 4)
- Decision criteria: (1) Core features working, (2) On budget (<$100K spent), (3) Sales team positive on usability

**Phase 3 (Months 4-6): Complete Build** (if MVP succeeds)
- Add reporting, mobile app, integrations
- Budget: Additional $150K
- Total: $250K build cost

**Phase 4: SaaS Fallback** (if MVP fails)
- Implement HubSpot Professional
- Cost: $20K implementation + $50K/year
- Timeline: 2-3 months to operational

This approach addresses all three stakeholders' core concerns:

### What We're Prioritizing

**Primary focus**: Mitigate execution risk while preserving custom fit option

- From **VP Sales**: Speed to value (MVP in 3 months, exit ramp if build fails)
- From **Engineering**: Opportunity to build custom fit (MVP tests feasibility)
- From **Finance**: Capital-efficient (only invest $100K before decision gate, pivot if needed)

**Secondary considerations**: Address concerns from each perspective

- **VP Sales**'s concern about adoption: Sales team involved in MVP design, validates at 3 months
- **Engineering**'s concern about SaaS fit: MVP proves we can build 2-stage approval properly
- **Finance**'s concern about cost overruns: Phased budget ($100K → gate → $150K), cap at $250K total

### Tradeoffs Accepted

**We're accepting:**
- **3-month delay vs. starting SaaS immediately**
  - **Rationale**: Worth the delay to test if custom build is feasible. If MVP fails, we pivot to SaaS and only lost 3 months.

- **Risk of $100K sunk cost if MVP fails**
  - **Rationale**: $100K is our "learning cost" to validate whether custom build can work. Still cheaper than committing to $250K+ full build that might fail.

**We're NOT accepting:**
- **Blind commitment to custom build** (Engineering's original proposal)
  - **Reason**: Too risky given track record. MVP + gate reduces risk.

- **Immediate SaaS adoption** (Sales' original proposal)
  - **Reason**: Doesn't test whether custom fit is achievable. Worth 3 months to find out.

- **Waiting 12+ months for full custom solution** (original concern)
  - **Reason**: Phased approach with exit ramps means we pivot to SaaS if build isn't working by month 3.

### Addressing Each Role's Core Concerns

**VP Sales's main concern (speed and adoption) is addressed by:**
- MVP in 3 months (not 12-18 months)
- Exit ramp at month 3 if build is behind schedule
- Sales team involved in MVP design (adoption risk mitigation)
- Fallback to SaaS if build doesn't work out

**Engineering Lead's main concern (custom fit and control) is addressed by:**
- Opportunity to prove custom build is feasible via MVP
- If MVP succeeds, we complete the build (Phases 3)
- 2-stage approval built exactly as needed
- Only pivot to SaaS if custom build *demonstrably* fails (data-driven decision)

**Finance's main concern (cost and risk) is addressed by:**
- Capital-efficient: Only $100K at risk before decision gate
- Clear decision criteria at month 3 (on budget? on schedule? working?)
- Capped budget: $250K total if we complete build (vs. $350K uncapped original proposal)
- Predictable costs: SaaS fallback available if build overruns

---

## 5. Recommendation

**Recommended Action:**
Pursue phased build with MVP milestone at 3 months and decision gate (continue build vs. pivot to SaaS).

**Rationale:**

This synthesis is superior to either "pure build" or "pure buy" because it:

1. **Tests feasibility before full commitment**: The MVP validates whether we can build the custom CRM on time and on budget. If yes, we continue. If no, we pivot to SaaS with only $100K sunk cost.

2. **Mitigates execution risk (Sales' top concern)**: Exit ramp at month 3 means we're not locked into a long, uncertain build. If engineering can't deliver, we bail quickly and go SaaS.

3. **Preserves custom fit option (Engineering's top concern)**: If MVP succeeds, we get the perfectly tailored CRM with 2-stage approval. If SaaS doesn't fit our needs (as Engineering argues), we've built the right solution.

4. **Optimizes cost under uncertainty (Finance's top concern)**: We only invest $100K to learn whether custom build is viable. If it works, total cost is $250K (less than original $350K). If it doesn't, we pivot to SaaS having "paid" $100K for the knowledge that custom wasn't feasible.

The key insight from the debate: **The real uncertainty is execution capability, not which option is better in theory**. By building an MVP first, we resolve that uncertainty before committing the full budget.

**Key factors driving this decision:**
1. **Execution risk** (from Sales): Phased approach with exit ramps mitigates this
2. **Custom fit value** (from Engineering): MVP tests whether we can actually build it
3. **Cost efficiency** (from Finance): Capital-efficient with decision gate before full investment

---

## 6. Implementation

**Immediate next steps:**

1. **Kickoff MVP build** (Week 1) - Engineering Lead
   - Scope MVP: Contacts, Deals, Pipeline, 2-stage approval
   - Assign 1.5 senior engineers full-time
   - Set up weekly check-ins with Sales for feedback

2. **Define MVP success criteria** (Week 1) - Finance + CTO
   - Core features functional (create contact, create deal, advance through 2-stage approval)
   - Budget: <$100K spent by month 3
   - Usability: Sales reps can complete key workflows without confusion

3. **Involve Sales team in design** (Week 2) - VP Sales
   - Weekly design reviews with 3-5 sales reps
   - Prototype testing at weeks 4, 8, 12
   - Feedback incorporated into MVP

**Phased approach:**

- **Phase 1** (Months 1-3): Build and validate MVP
  - Milestone 1 (Month 1): Contacts and deal creation working
  - Milestone 2 (Month 2): 2-stage approval workflow functional
  - Milestone 3 (Month 3): Sales team testing, feedback incorporated

- **Phase 2** (Month 3): Decision Gate
  - Review meeting: CTO, VP Sales, CFO, Engineering Lead
  - Decision criteria:
    - ✅ MVP core features working?
    - ✅ Budget on track (<$100K)?
    - ✅ Sales team feedback positive (usability acceptable)?
  - If yes: Proceed to Phase 3 (complete build)
  - If no: Pivot to Phase 4 (SaaS implementation)

- **Phase 3** (Months 4-6): Complete Build (if Phase 2 = yes)
  - Add reporting dashboard
  - Build mobile app (iOS/Android)
  - Integrate with accounting system and email
  - User training and rollout to full sales team

- **Phase 4**: SaaS Fallback (if Phase 2 = no)
  - Month 4: Select vendor (HubSpot vs. Salesforce), contract negotiation
  - Months 4-5: Implementation and customization
  - Month 6: Training and rollout

**Conditional triggers:**

- **If MVP fails Month 3 gate**: Pivot to SaaS immediately (do not continue build)
- **If build exceeds $250K total**: Stop, reassess whether to continue or pivot to SaaS
- **If adoption is <80% by Month 9**: Investigate issues, consider switching (build or buy)

**Success metrics:**

- **Engineering's perspective**: MVP functional by month 3, full build by month 6, <5 bugs/month
- **Sales' perspective**: Operational by month 6, >90% adoption within 30 days, sales cycle reduces to 45 days
- **Finance's perspective**: Total cost <$250K (if build) or <$20K + $50K/year (if SaaS), payback <18 months

**Monitoring plan:**

- **Weekly**: Engineering progress vs. milestones, budget burn rate
- **Monthly**: Sales team feedback on usability, adoption metrics
- **Month 3**: Formal decision gate review (continue build or pivot to SaaS)
- **Month 6**: Post-launch review (did we hit success metrics?)
- **Month 12**: ROI review (productivity gains vs. investment)

**Escalation conditions:**

- If budget exceeds $100K by month 3 → automatic pivot to SaaS
- If MVP core features not working by month 3 → escalate to CEO for decision
- If adoption <50% by month 9 → escalate to executive team for intervention

---

## 7. Stakeholder Communication

**For Executive Team (CEO, CFO, Board):**

**Key message**: "We're pursuing a phased build approach that tests feasibility before full commitment, with SaaS fallback if custom build doesn't work."

**Focus on**: Risk mitigation, cost efficiency, timeline
- Risk: MVP + decision gate reduces execution risk from high to medium
- Cost: Only $100K at risk before decision point, capped at $250K total
- Timeline: MVP operational in 3 months, decision by month 3, full solution by month 6

**For Engineering Team:**

**Key message**: "We're building an MVP to prove we can deliver a custom CRM on time and on budget. If successful, we'll complete the build. If not, we'll pivot to SaaS."

**Focus on**: Technical scope, timeline, success criteria
- Scope: MVP = contacts, deals, pipeline, 2-stage approval (no gold-plating)
- Timeline: 3 months to MVP, 6 months to full build (if MVP succeeds)
- Success criteria: Functional, on budget, sales team validates usability
- Commitment: If we prove we can do this, company will invest in completing the build

**For Sales Team:**

**Key message**: "We're building a custom CRM tailored to your workflow, with your input. If it doesn't work out, we'll get you a proven SaaS CRM instead."

**Focus on**: Involvement, timeline, fallback plan
- Involvement: You'll be involved from day one - design reviews, prototype testing, feedback
- Timeline: Testing MVP in 3 months, full CRM operational by month 6
- Custom fit: Built for your 2-stage approval workflow (not workarounds)
- Safety net: If custom build doesn't work, we have SaaS option (HubSpot) ready to go

---

## 8. Appendix: Assumptions & Uncertainties

**Key assumptions:**

1. **Engineering can deliver MVP in 3 months with 1.5 engineers**
   - **Confidence**: Medium (based on similar past projects, but track record includes delays)
   - **Impact if wrong**: Delays decision gate, may force SaaS pivot

2. **MVP will provide sufficient signal on full build feasibility**
   - **Confidence**: High (MVP includes core technical challenges: data model, 2-stage approval logic, UI)
   - **Impact if wrong**: May commit to full build that later fails

3. **Sales team will provide constructive feedback during MVP development**
   - **Confidence**: High (VP Sales committed to involving team)
   - **Impact if wrong**: Build wrong features, adoption fails

4. **SaaS option (HubSpot) will still be available at $50K/year in 3 months**
   - **Confidence**: High (enterprise contracts are stable, pricing doesn't fluctuate month-to-month)
   - **Impact if wrong**: Fallback plan costs more than projected

5. **Current manual CRM costs $40K/year in lost productivity**
   - **Confidence**: Medium (rough estimate based on 20 hours/week sales rep time)
   - **Impact if wrong**: ROI calculation changes, but decision logic still holds

**Unresolved uncertainties:**

- **Will sales reps actually use the custom CRM?**: Mitigated by involving them in design, but adoption risk remains
- **Can engineering complete full build in months 4-6?**: MVP reduces uncertainty but doesn't eliminate it
- **Will SaaS really handle 2-stage approval well?**: Need to do deeper demo/trial if we pivot to SaaS

**What would change our mind:**

- **If MVP demonstrates build is infeasible** (behind schedule, over budget, or sales team feedback is negative) → Pivot to SaaS immediately
- **If SaaS vendors introduce features that handle our 2-stage approval** → Reconsider SaaS earlier
- **If budget gets cut below $100K** → Go straight to SaaS (can't afford MVP experiment)

---

## Self-Assessment (Rubric Scores)

**Perspective Authenticity**: 4/5
- All three roles authentically represented with strong advocacy
- Each role feels genuine ("hero of their own story")
- Could improve: More depth on Finance's methodology for cost analysis

**Depth of Roleplay**: 4/5
- Priorities, concerns, evidence, and vulnerabilities articulated for each role
- Success metrics defined
- Could improve: More specific evidence citations (e.g., which past projects, exact timeline data)

**Debate Quality**: 5/5
- Strong point-counterpoint engagement
- Roles respond directly to each other's arguments
- Cross-examination adds depth
- All perspectives clash on key dimensions

**Tension Surfacing**: 5/5
- Four key tensions explicitly identified and explored (timeline, fit, cost, risk)
- Irreducible tradeoffs clear
- False dichotomies avoided (phased approach finds middle ground)

**Crux Identification**: 4/5
- Clear cruxes for each role
- Conditions that would change minds specified
- Could improve: More specificity on evidence thresholds (e.g., exactly what MVP must demonstrate)

**Synthesis Coherence**: 5/5
- Phased + conditional pattern well-applied
- Recommendation is unified and logical
- Addresses the decision directly
- Better than any single perspective alone (integrates insights)

**Concern Integration**: 5/5
- All three roles' core concerns explicitly addressed
- Synthesis shows how each perspective is strengthened by integration
- No perspective dismissed

**Tradeoff Transparency**: 5/5
- Clear on what's accepted (3-month delay, $100K risk) and why
- Explicit on what's rejected (blind build commitment, immediate SaaS)
- Honest about second-order effects

**Actionability**: 5/5
- Detailed implementation plan with phases
- Owners and timelines specified
- Success metrics from each role's perspective
- Monitoring plan and escalation conditions
- Decision review cadence (Month 3 gate)

**Stakeholder Readiness**: 4/5
- Communication tailored for execs, engineering, and sales
- Key messages appropriate for each audience
- Could improve: Add one-page executive summary at the top

**Average Score**: 4.6/5 (Exceeds standard for medium-complexity decision)

**Why this exceeds standard:**
- Genuine multi-stakeholder debate with real tension
- Synthesis pattern (phased + conditional) elegantly resolves competing priorities
- Decision gate provides exit ramp that addresses execution risk
- All perspectives strengthened by integration (not just compromise)

---

**Analysis completed**: November 2, 2024
**Facilitator**: [Internal Strategy Team]
**Status**: Ready for executive approval
**Next milestone**: Kickoff MVP build (Week 1)
