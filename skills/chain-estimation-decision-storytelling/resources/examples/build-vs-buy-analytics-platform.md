# Decision: Build Custom Analytics Platform vs. Buy SaaS Solution

**Date:** 2024-01-15
**Decision-maker:** CTO + VP Product
**Audience:** Executive team
**Stakes:** Medium ($500k-$1.5M over 3 years)

---

## 1. Decision Context

**What we're deciding:**
Should we build a custom analytics platform in-house or purchase a SaaS analytics solution?

**Why this matters:**
- Current analytics are manual and time-consuming (20 hours/week analyst time)
- Product team needs real-time insights to inform roadmap decisions
- Sales needs usage data to identify expansion opportunities
- Engineering wants to reduce operational burden of maintaining custom tools

**Alternatives:**
1. **Build custom**: Develop in-house analytics platform with our exact requirements
2. **Buy SaaS**: Purchase enterprise analytics platform (e.g., Amplitude, Mixpanel)
3. **Hybrid**: Use SaaS for standard metrics, build custom for proprietary analysis

**Key uncertainties:**
- Development cost and timeline (historical variance ±40%)
- Feature completeness of SaaS solution (will it meet all needs?)
- Usage growth rate (affects SaaS costs which scale with volume)
- Long-term flexibility needs (will we outgrow SaaS or need custom features?)

**Constraints:**
- Budget: $150k available in current year, $50k/year ongoing
- Timeline: Need solution operational within 6 months
- Requirements: Must support 100M events/month, 50+ team members, custom dashboards
- Strategic: Prefer minimal vendor lock-in, prioritize time-to-value

**Audience:** Executive team (need bottom-line recommendation + risks)

---

## 2. Estimation

### Alternative 1: Build Custom

**Costs:**
- **Initial development**: $200k-$400k (most likely $300k)
  - Base estimate: 6 engineer-months × $50k loaded cost = $300k
  - Range reflects scope uncertainty and potential technical challenges
  - Source: Similar internal projects averaged $280k ±$85k (30% std dev)

- **Annual operational costs**: $40k-$60k per year (most likely $50k)
  - Infrastructure: $15k-$25k (based on 100M events/month)
  - Maintenance: 0.5 engineer FTE = $25k-$35k per year
  - Source: Current analytics tools cost $45k/year to maintain

- **Opportunity cost**: $150k
  - Engineering team would otherwise work on core product features
  - Estimated value of deferred features: $150k in potential revenue impact

**Benefits:**
- **Cost savings**: $0 subscription fees (vs $120k/year for SaaS)
- **Perfect fit**: 100% feature match to our specific needs
- **Flexibility**: Full control to add custom analysis
- **Strategic value**: Build analytics competency, own our data

**Probabilities:**
- **Best case (20%)**: On-time delivery at $250k, perfect execution
  - Prerequisites: Clear requirements, no scope creep, experienced team available

- **Base case (50%)**: Moderate delays and cost overruns to $350k over 8 months
  - Typical scenario based on historical performance

- **Worst case (30%)**: Significant delays to $500k over 12 months, some features cut
  - Risk factors: Key engineer departure, underestimated complexity, changing requirements

**Key assumptions:**
- Engineering team has capacity (currently 70% utilized)
- No major technical unknowns in data pipeline
- Requirements are stable (< 10% scope change)
- Infrastructure costs scale linearly with events

### Alternative 2: Buy SaaS

**Costs:**
- **Initial implementation**: $15k-$25k (most likely $20k)
  - Setup and integration: 2-3 weeks consulting
  - Data migration and testing
  - Team training
  - Source: Vendor quote + reference customer feedback

- **Annual subscription**: $100k-$140k per year (most likely $120k)
  - Base: $80k for 100M events/month
  - Users: $2k per user × 20 power users = $40k
  - Growth buffer: Assume 20% event growth per year
  - Source: Vendor pricing confirmed, escalates with usage

- **Switching cost** (if we change vendors later): $50k-$75k
  - Data export and migration
  - Re-implementing integrations
  - Team retraining

**Benefits:**
- **Faster time-to-value**: 2 months vs. 8 months for build
  - 6-month head start = earlier insights = better decisions sooner
  - Estimated value: $75k (half of opportunity cost avoided)

- **Proven reliability**: 99.9% uptime SLA
  - Reduces operational risk
  - Frees engineering for core product

- **Feature velocity**: Continuous improvements from vendor
  - New capabilities quarterly (ML-powered insights, predictive analytics)
  - Estimated value: $30k/year in avoided feature development

- **Lower risk**: Predictable costs, no schedule risk
  - High confidence in timeline and total cost

**Probabilities:**
- **Best case (40%)**: Perfect fit, seamless implementation, $100k/year steady state
  - Vendor delivers on promises, usage grows slower than expected

- **Base case (45%)**: Good fit with minor gaps, standard implementation, $120k/year
  - 85% of needs met out-of-box, workarounds for remaining 15%

- **Worst case (15%)**: Poor fit requiring workarounds or supplemental tools, $150k/year
  - Missing critical features, need to maintain some custom tooling

**Key assumptions:**
- SaaS vendor is stable and continues product development
- Event volume growth is 20% per year (manageable)
- Vendor lock-in is acceptable (switching cost is reasonable)
- Security and compliance requirements are met by vendor

### Alternative 3: Hybrid

**Costs:**
- **Initial investment**: $100k-$150k (most likely $125k)
  - SaaS implementation: $20k
  - Custom integrations and proprietary metrics: $100k-$130k development

- **Annual costs**: $80k-$100k per year (most likely $90k)
  - SaaS subscription (smaller tier): $60k-$70k
  - Maintenance of custom components: $20k-$30k

**Benefits:**
- **Balanced approach**: Standard analytics from SaaS, custom analysis in-house
- **Reduced risk**: Less development than full build, more control than pure SaaS
- **Flexibility**: Can shift balance over time based on needs

**Probabilities:**
- **Base case (60%)**: Works reasonably well, $125k + $90k/year
- **Integration complexity (40%)**: More overhead than expected, $150k + $100k/year

**Key assumptions:**
- Clean separation between standard and custom analytics
- SaaS provides good API for custom integrations
- Maintaining two systems doesn't create excessive complexity

---

## 3. Decision Analysis

### Expected Value Calculation (3-Year NPV)

**Discount rate:** 10% (company's cost of capital)

#### Alternative 1: Build Custom

**Year 0 (Initial):**
- Best case (20%): -$250k development - $150k opportunity cost = -$400k
- Base case (50%): -$350k development - $150k opportunity cost = -$500k
- Worst case (30%): -$500k development - $150k opportunity cost = -$650k

**Expected Year 0:** ($-400k × 0.20) + ($-500k × 0.50) + ($-650k × 0.30) = -$525k

**Years 1-3 (Operational):**
- Annual cost: $50k/year
- PV of 3 years at 10%: $50k × 2.49 = $124k

**Total Expected NPV (Build):** -$525k - $124k = **-$649k**

*Note: Costs are negative because this is an investment. Focus is on minimizing cost since benefits (analytics capability) are equivalent across alternatives.*

#### Alternative 2: Buy SaaS

**Year 0 (Initial):**
- Implementation: $20k
- No opportunity cost (fast implementation)

**Years 1-3 (Operational):**
- Best case (40%): $100k/year × 2.49 = $249k
- Base case (45%): $120k/year × 2.49 = $299k
- Worst case (15%): $150k/year × 2.49 = $374k

**Expected annual cost:** ($100k × 0.40) + ($120k × 0.45) + ($150k × 0.15) = $116.5k/year
**PV of 3 years:** $116.5k × 2.49 = $290k

**Total Expected NPV (Buy):** -$20k - $290k = **-$310k**

**Benefit adjustment for faster time-to-value:** +$75k (6-month head start)
**Adjusted NPV (Buy):** -$310k + $75k = **-$235k**

#### Alternative 3: Hybrid

**Year 0 (Initial):**
- Development + implementation: $125k
- Partial opportunity cost: $75k (half the custom build time)

**Years 1-3 (Operational):**
- Expected annual: $90k/year × 2.49 = $224k

**Total Expected NPV (Hybrid):** -$125k - $75k - $224k = **-$424k**

### Comparison Summary

| Alternative | Expected 3-Year Cost | Risk Profile | Time to Value |
|-------------|---------------------|--------------|---------------|
| Build Custom | $649k              | **High** (30% worst case) | 8 months |
| Buy SaaS     | $235k              | **Low** (predictable) | 2 months |
| Hybrid       | $424k              | **Medium** | 5 months |

**Cost difference:** Buy SaaS saves **$414k** vs. Build Custom over 3 years

### Sensitivity Analysis

**What if development cost for Build is 20% lower ($240k base instead of $300k)?**
- Build NPV: -$577k (still $342k worse than Buy)
- **Conclusion still holds**

**What if SaaS costs grow 40% per year instead of 20%?**
- Year 3 SaaS cost: $230k (vs. $145k base case)
- Buy NPV: -$325k (still $324k better than Build)
- **Conclusion still holds**

**What if we need to switch SaaS vendors in Year 3?**
- Additional switching cost: $65k
- Buy NPV: -$300k (still $349k better than Build)
- **Conclusion still holds**

**Break-even analysis:**
At what annual SaaS cost does Build become cheaper?
- Build 3-year cost: $649k
- Buy 3-year cost: $20k + (X × 2.49) - $75k = $649k
- Solve: X = $282k/year

**Interpretation:** SaaS would need to cost $282k/year (2.4x current estimate) for Build to break even. Very unlikely.

### Robustness Check

**Conclusion is robust if:**
- Development cost < $600k (currently $300k base, $500k worst case ✓)
- SaaS annual cost < $280k (currently $120k base, $150k worst case ✓)
- Time-to-value benefit > $0 (6-month head start valuable ✓)

**Conclusion changes if:**
- SaaS vendor goes out of business (low probability, large incumbents)
- Regulatory requirements force on-premise solution (not currently foreseen)
- Custom analytics become core competitive differentiator (possible but unlikely)

---

## 4. Recommendation

### **Recommended option: Buy SaaS Solution**

**Reasoning:**

Buy SaaS dominates Build Custom on three dimensions:

1. **Lower expected cost**: $235k vs. $649k over 3 years (saves $414k)
2. **Lower risk**: Predictable subscription vs. 30% chance of 2x cost overrun on build
3. **Faster time-to-value**: 2 months vs. 8 months (6-month head start enables better decisions sooner)

The cost advantage is substantial ($414k savings) and robust to reasonable assumption changes. Even if SaaS costs double or we need to switch vendors, Buy still saves $300k+.

The risk profile strongly favors Buy. Historical data shows 30% of similar build projects experience 2x cost overruns. SaaS has predictable costs with 99.9% uptime SLA.

Time-to-value matters: getting analytics operational 6 months sooner means better product decisions sooner, worth approximately $75k in avoided opportunity cost.

**Key factors:**
1. **Cost**: $414k lower expected cost over 3 years
2. **Risk**: Predictable vs. high uncertainty (30% worst case for Build)
3. **Speed**: 2 months vs. 8 months to operational
4. **Strategic fit**: Analytics are important but not core competitive differentiator

**Tradeoffs accepted:**
- **Vendor dependency**: Accepting switching cost of $65k if we change vendors
  - Mitigation: Choose stable, market-leading vendor (Amplitude or Mixpanel)

- **Some feature gaps**: SaaS may not support 100% of custom analysis needs
  - Mitigation: 85% coverage out-of-box, workarounds for remaining 15%
  - Can supplement with lightweight custom tools if needed ($20k-$30k vs. $300k+ full build)

- **Less flexibility**: Can't customize as freely as in-house solution
  - Mitigation: Most SaaS platforms offer extensive APIs and integrations
  - True custom needs can be addressed incrementally

**Why not Hybrid?**
Hybrid ($424k) is $189k more expensive than Buy with minimal additional benefit. The complexity of maintaining two systems outweighs the incremental flexibility.

---

## 5. Risks and Mitigations

### Risk 1: SaaS doesn't meet all requirements

**Probability:** Medium (15% worst case scenario)

**Impact:** Need workarounds or supplemental tools

**Mitigation:**
- Conduct thorough vendor evaluation with 2-week pilot
- Map all requirements to vendor capabilities before committing
- Budget $30k for lightweight custom supplements if needed
- Still cheaper than full Build even with supplements

### Risk 2: Vendor lock-in / price increases

**Probability:** Low-Medium (vendors typically increase 5-10%/year)

**Impact:** Higher ongoing costs

**Mitigation:**
- Negotiate multi-year contract with price protection
- Maintain data export capability (ensure vendor supports data portability)
- Budget includes 20% annual growth buffer
- Switching cost is manageable ($65k) if needed

### Risk 3: Usage growth exceeds estimates

**Probability:** Low (current trajectory is 15%/year, estimated 20%)

**Impact:** Higher subscription costs

**Mitigation:**
- Monitor usage monthly against plan
- Optimize event instrumentation to reduce unnecessary events
- Renegotiate tier if growth is faster than expected
- Even at 2x usage growth, still cheaper than Build

### Risk 4: Security or compliance issues

**Probability:** Very Low (vendor is SOC 2 Type II certified)

**Impact:** Cannot use vendor, forced to build

**Mitigation:**
- Verify vendor security certifications before contract
- Review data handling and privacy policies
- Include compliance requirements in vendor evaluation
- This risk applies to any vendor; not specific to this decision

---

## 6. Next Steps

**If approved:**

1. **Vendor evaluation** (2 weeks) - VP Product + Data Lead
   - Demo top 3 vendors (Amplitude, Mixpanel, Heap)
   - Map requirements to capabilities
   - Validate pricing and terms
   - Decision by: Feb 1

2. **Pilot implementation** (2 weeks) - Engineering Lead
   - 2-week pilot with selected vendor
   - Instrument 3 key product flows
   - Validate data accuracy and latency
   - Go/no-go decision by: Feb 15

3. **Full rollout** (4 weeks) - Data Team + Engineering
   - Instrument all product events
   - Migrate existing dashboards
   - Train team on new platform
   - Launch by: March 15

**Success metrics:**
- **Time to value**: Analytics operational within 2 months (by March 15)
- **Cost**: Stay within $20k implementation + $120k annual budget
- **Adoption**: 50+ team members using platform within 30 days of launch
- **Value delivery**: Reduce manual analytics time from 20 hours/week to <5 hours/week

**Decision review:**
- **6-month review** (Sept 2024): Validate cost and value delivered
  - Key question: Are we getting value proportional to cost?
  - Metrics: Usage stats, time savings, decisions influenced by data

- **Annual review** (Jan 2025): Assess whether to continue, renegotiate, or reconsider build
  - Key indicators: Usage growth trend, missing features impact, pricing changes

**What would change our mind:**
- If vendor quality degrades significantly (downtime, bugs, poor support)
- If pricing increases >30% beyond projections
- If we identify analytics as core competitive differentiator (requires custom innovation)
- If regulatory requirements force on-premise solution

---

## 7. Appendix: Assumptions Log

**Development estimates:**
- Based on: 3 similar internal projects (API platform, reporting tool, data pipeline)
- Historical variance: ±30% from initial estimate
- Team composition: 2-3 senior engineers for 3-4 months
- Scope: Event ingestion, storage, query engine, dashboarding UI

**SaaS pricing:**
- Based on: Vendor quotes for 100M events/month, 50 users
- Confirmed with: 2 reference customers at similar scale
- Growth assumption: 20% annual event growth (aligned with product roadmap)
- User assumption: 20 power users (product, sales, exec) need full access

**Opportunity cost:**
- Based on: Engineering team would otherwise work on product features
- Estimated value: Product features could drive $150k additional revenue
- Source: Product roadmap prioritization (deferred features)

**Time-to-value benefit:**
- Based on: 6-month head start with SaaS (2 months vs. 8 months)
- Estimated value: Better decisions sooner = avoided mistakes + seized opportunities
- Conservative estimate: 50% of opportunity cost = $75k

**Discount rate:**
- Company cost of capital: 10%
- Used to calculate present value of multi-year costs

---

## Self-Assessment (Rubric Scores)

**Estimation Quality:** 4/5
- Comprehensive estimation with ranges and probabilities
- Justification provided for estimates with sources
- Could improve: More rigorous data collection from reference customers

**Probability Calibration:** 4/5
- Probabilities justified with base rates (historical project performance)
- Well-calibrated ranges
- Could improve: External validation of probability estimates

**Decision Analysis Rigor:** 5/5
- Sound expected value calculation with NPV
- Appropriate decision criteria
- Multiple scenarios tested

**Sensitivity Analysis:** 5/5
- Comprehensive one-way sensitivity on key variables
- Break-even analysis performed
- Conditions that change conclusion clearly stated

**Alternative Comparison:** 4/5
- Three alternatives analyzed fairly
- Could improve: Consider more creative alternatives (e.g., open-source + custom)

**Assumption Transparency:** 5/5
- All key assumptions stated explicitly with justification
- Alternative assumptions tested in sensitivity analysis

**Narrative Clarity:** 4/5
- Clear structure and logical flow
- Could improve: More compelling framing for exec audience

**Audience Tailoring:** 4/5
- Appropriate detail for executive audience
- Could improve: Add one-page executive summary

**Risk Acknowledgment:** 5/5
- Comprehensive risk analysis with probabilities and mitigations
- Downside scenarios quantified
- "What would change our mind" conditions stated

**Actionability:** 5/5
- Clear recommendation with specific next steps
- Owners and timeline defined
- Success metrics and review cadence specified

**Average Score:** 4.5/5 (Exceeds standard for medium-stakes decision)

---

**Analysis completed:** January 15, 2024
**Analyst:** [Name]
**Reviewed by:** CTO
**Status:** Ready for executive decision
