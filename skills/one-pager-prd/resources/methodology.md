# One-Pager PRD Methodology

## Table of Contents
1. [Problem Framing Techniques](#1-problem-framing-techniques)
2. [Metric Definition & Trees](#2-metric-definition--trees)
3. [Scope Prioritization Methods](#3-scope-prioritization-methods)
4. [Writing for Clarity](#4-writing-for-clarity)
5. [Stakeholder Management](#5-stakeholder-management)
6. [User Story Mapping](#6-user-story-mapping)
7. [PRD Review & Iteration](#7-prd-review--iteration)

---

## 1. Problem Framing Techniques

### Jobs-to-be-Done Framework

**Template:** "When I [situation], I want to [motivation], so I can [outcome]."

**Example:** ❌ "Users want better search" → ✓ "When looking for a document among thousands, I want to filter by type/date/author, so I can find it in <30 seconds"

**Application:** Interview users for triggers, understand workarounds, quantify pain.

### Problem Statement Formula

**Template:** "[User segment] struggles to [task] because [root cause], resulting in [quantified impact]. Evidence: [data]."

**Example:** "Power users (15% of users, 60% usage) struggle to edit multiple rows because single-row editing only, resulting in 5h/week manual work and 12% higher churn. Evidence: churn interviews (8/10 cited), analytics (300 edits/user/week)."

### 5 Whys (Root Cause Analysis)

Ask "why" 5 times to get from symptom to root cause.

**Example:** Users complain search is slow → Why? Query takes 3s → Why? DB not indexed → Why? Schema not designed for search → Why? Original use case was CRUD → Why? Product pivoted.

**Root Cause:** Product pivot created tech debt. Real problem: Re-architect for search-first, not just optimize queries.

### Validation Checklist
- [ ] Talked to 5+ users
- [ ] Quantified frequency and severity
- [ ] Identified workarounds
- [ ] Confirmed top 3 pain point
- [ ] Checked if competitors solve this
- [ ] Estimated TAM

---

## 2. Metric Definition & Trees

### SMART Metrics

Specific, Measurable, Achievable, Relevant, Time-bound.

❌ "Improve engagement" → ✓ "Increase WAU from 10K to 15K (+50%) in Q2"
❌ "Make search faster" → ✓ "Reduce p95 latency from 3s to <1s by Q1 end"

### Leading vs Lagging Metrics

**Lagging:** Outcomes (revenue, retention). Slow to change, final success measure.
**Leading:** Early signals (adoption, usage). Fast to change, enable corrections.

**Example:** Lagging = Revenue. Leading = Adoption rate, usage frequency.

### Metric Tree Decomposition

Break down North Star into actionable sub-metrics.

**Example:** Revenue = Users × Conversion × Price
- Users = Signups + Reactivated
- Conversion = Activate × Value × Paywall × Pay Rate

**Application:** Pick 2-3 metrics from tree you can influence.

### Metric Anti-Patterns

❌ **Vanity:** Signups without retention, page views without engagement
❌ **Lagging-Only:** Only revenue (too slow). Add adoption/engagement.
❌ **Too Many:** 15 metrics. Pick 1 primary + 2-3 secondary.
❌ **No Baselines:** "Increase engagement" vs "From 2.5 to 4 sessions/week"

---

## 3. Scope Prioritization Methods

### MoSCoW Method

**Must-Have:** Feature doesn't work without this
**Should-Have:** Important but feature works without it (next iteration)
**Could-Have:** Nice to have if time permits
**Won't-Have:** Explicitly out of scope

**Example: Bulk Edit**
- **Must:** Select multiple rows, edit common field, apply
- **Should:** Undo/redo, validation error handling
- **Could:** Bulk delete, custom formulas
- **Won't:** Conditional formatting (separate feature)

### Kano Model

**Basic Needs:** If missing, users dissatisfied. If present, users neutral.
- Example: Search must return results

**Performance Needs:** More is better (linear satisfaction)
- Example: Faster search is better

**Delight Needs:** Unexpected features that wow users
- Example: Search suggests related items

**Application:** Must-haves = Basic needs. Delights can wait for v2.

### RICE Scoring

**Reach:** How many users per quarter?
**Impact:** How much does it help each user? (0.25 = minimal, 3 = massive)
**Confidence:** How sure are you? (0% to 100%)
**Effort:** Person-months

**Score = (Reach × Impact × Confidence) / Effort**

**Example:**
- Feature A: (1000 users × 3 impact × 80% confidence) / 2 months = 1200
- Feature B: (5000 users × 0.5 impact × 100%) / 1 month = 2500
- **Prioritize Feature B**

### Value vs Effort Matrix

**2×2 Grid:**
- **High Value, Low Effort:** Quick wins (do first)
- **High Value, High Effort:** Strategic projects (plan carefully)
- **Low Value, Low Effort:** Fill-ins (do if spare capacity)
- **Low Value, High Effort:** Avoid

**Determine Scope:**
1. List all potential features/requirements
2. Plot on matrix
3. MVP = High Value (both high/low effort)
4. v2 = Medium Value
5. Backlog/Never = Low Value

---

## 4. Writing for Clarity

### Pyramid Principle

**Structure:** Lead with conclusion, then support.

**Template:**
1. **Conclusion:** Main point (problem statement)
2. **Key Arguments:** 3-5 supporting points
3. **Evidence:** Data, examples, details

**Example:**
1. **Conclusion:** "We should build bulk edit because power users churn without it"
2. **Arguments:**
   - 12% higher churn among power users
   - Competitors all have bulk edit
   - Users hack workarounds (exports to Excel)
3. **Evidence:** Churn analysis, competitive audit, user interviews

**Application:** Start PRD with executive summary using pyramid structure.

### Active Voice & Concrete Language

**Passive → Active:**
- ❌ "The feature will be implemented by engineering"
- ✓ "Engineering will implement the feature"

**Vague → Concrete:**
- ❌ "Improve search performance"
- ✓ "Reduce search latency from 3s to <1s"

**Abstract → Specific:**
- ❌ "Enhance user experience"
- ✓ "Reduce clicks from 10 to 3 for common task"

### Avoid Jargon & Acronyms

**Bad:** "Implement CQRS with event sourcing for the BFF layer to optimize TTFB for SSR"

**Good:** "Separate read and write databases to make pages load faster (3s → 1s)"

**Rule:** Define acronyms on first use, or avoid entirely if stakeholders unfamiliar.

### Use Examples Liberally

**Before (Abstract):**
"Users need flexible filtering options"

**After (Concrete Example):**
"Users need flexible filtering. Example: Data analyst wants to see 'all invoices from Q4 2023 where amount > $10K and status = unpaid' without opening each invoice."

**Benefits:** Examples prevent misinterpretation, make requirements testable.

### Scannable Formatting

**Use:**
- **Bullets:** For lists (easier than paragraphs)
- **Headers:** Break into sections (5-7 sections max per page)
- **Bold:** For key terms (not entire sentences)
- **Tables:** For comparisons or structured data
- **Short paragraphs:** 3-5 sentences max

**Avoid:**
- Long paragraphs (>6 sentences)
- Wall of text
- Too many indentation levels (max 2)

---

## 5. Stakeholder Management

### Identifying Stakeholders

**Categories:**
- **Accountable:** PM (you) - owns outcome
- **Approvers:** Who must say yes (eng lead, design lead, exec sponsor)
- **Contributors:** Who provide input (engineers, designers, sales, support)
- **Informed:** Who need to know (marketing, legal, customer success)

**Mapping:**
1. List everyone who touches this feature
2. Categorize by role
3. Identify decision-makers vs advisors
4. Note what each stakeholder cares about most

### Tailoring PRD for Stakeholders

**For Engineering:**
- Emphasize: Technical constraints, dependencies, edge cases
- Include: Non-functional requirements (performance, scalability, security)
- Avoid: Over-specifying implementation

**For Design:**
- Emphasize: User flows, personas, success criteria
- Include: Empty states, error states, edge cases
- Avoid: Specifying UI components

**For Business (Sales/Marketing/Exec):**
- Emphasize: Business impact, competitive positioning, revenue potential
- Include: Go-to-market plan, pricing implications
- Avoid: Technical details

**For Legal/Compliance:**
- Emphasize: Privacy, security, regulatory requirements
- Include: Data handling, user consent, audit trails
- Avoid: Underestimating compliance effort

### Getting Buy-In

**Technique 1: Pre-socialize**
- Share draft with key stakeholders 1:1 before group review
- Gather feedback, address concerns early
- Avoid surprises in group meeting

**Technique 2: Address Objections Preemptively**
- Anticipate concerns (cost, timeline, technical risk)
- Include "Risks & Mitigation" section
- Show you've thought through trade-offs

**Technique 3: Present Options**
- Don't present single solution as fait accompli
- Offer 2-3 options with pros/cons
- Recommend one, but let stakeholders weigh in

**Technique 4: Quantify**
- Back up claims with data
- "This will save users 5 hours/week" (not "improve efficiency")
- Estimate revenue impact, churn reduction, support ticket decrease

---

## 6. User Story Mapping

### Concept
Map user journey horizontally (steps), features vertically (priority).

### Structure

**Backbone (Top Row):** High-level activities
**Walking Skeleton (Row 2):** MVP user flow
**Additional Features (Rows 3+):** Nice-to-haves

**Example: E-commerce Checkout**
```
Backbone:      Browse Products → Add to Cart → Checkout → Pay → Confirm
Walking Skeleton: View list    → Click "Add"  → Enter info → Card → Email receipt
v2:           Filters, search  → Save for later → Promo codes → Wallet → Order tracking
v3:           Recommendations  → Wish list    → Gift wrap  → BNPL → Returns
```

### Application to PRD

1. **Define backbone:** Key user activities (happy path)
2. **Identify MVP:** Minimum to complete journey
3. **Slice vertically:** Each slice is shippable increment
4. **Prioritize:** Top rows are must-haves, bottom rows are v2/v3

### Benefits
- Visual representation of scope
- Easy to see MVP vs future
- Stakeholder alignment on priorities
- Clear release plan

---

## 7. PRD Review & Iteration

### Review Process

**Phase 1: Self-Review**
- Let draft sit 24 hours
- Re-read with fresh eyes
- Check against rubric
- Run spell check

**Phase 2: Peer Review**
- Share with fellow PM or trusted colleague
- Ask: "Is problem clear? Is solution sensible? Any gaps?"
- Iterate based on feedback

**Phase 3: Stakeholder Review**
- Share with approvers (eng, design, business)
- Schedule review meeting or async comments
- Focus on: Do we agree on problem? Do we agree on approach? Are we aligned on scope/metrics?

**Phase 4: Sign-Off**
- Get explicit approval from each approver
- Document who approved and when
- Proceed to detailed design/development

### Feedback Types

**Clarifying Questions:**
- "What do you mean by X?"
- **Response:** Clarify in PRD (you were unclear)

**Concerns/Objections:**
- "This will take too long / cost too much / won't work because..."
- **Response:** Address in Risks section or adjust approach

**Alternative Proposals:**
- "What if we did Y instead?"
- **Response:** Evaluate alternatives, update PRD if better option

**Out of Scope:**
- "Can we also add feature Z?"
- **Response:** Acknowledge, add to "Out of Scope" or "Future Versions"

### Iterating Based on Feedback

**Don't:**
- Defend original idea blindly
- Take feedback personally
- Ignore concerns

**Do:**
- Thank reviewers for input
- Evaluate objectively (is their concern valid?)
- Update PRD with new information
- Re-share revised version with change log

### Version Control

**Track Changes:**
- **V1.0:** Initial draft
- **V1.1:** Updated based on eng feedback (added technical constraints)
- **V1.2:** Updated based on design feedback (clarified user flows)
- **V2.0:** Approved version

**Change Log:**
- Date, version, what changed, why
- Helps stakeholders see evolution
- Prevents confusion ("I thought we agreed on X?")

**Example:**
```markdown
## Change Log

**V1.2 (2024-01-15):**
- Updated scope: Removed bulk delete (security concern from eng)
- Added section: Performance requirements (feedback from eng)
- Clarified metric: Changed "engagement" to "% users who use bulk edit >3 times/week"

**V1.1 (2024-01-10):**
- Added personas: Broke out "power users" into data analysts vs operations teams
- Updated flows: Added error handling for validation failures

**V1.0 (2024-01-05):**
- Initial draft
```

### When to Stop Iterating

**Signs PRD is Ready:**
- All approvers have signed off
- Open questions resolved or have clear decision timeline
- Scope boundaries clear (everyone agrees on in/out)
- Metrics defined and measurable
- No blocking concerns remain

**Don't:**
- Iterate forever seeking perfection
- Delay unnecessarily
- Overspecify (leave room for design/eng creativity)

**Rule:** If 80% aligned and no blocking concerns, ship it. Can iterate during development if needed.

---

## Quick Reference: Methodology Selection

**Use Jobs-to-be-Done when:**
- Framing new problem
- Understanding user motivation
- Validating problem-solution fit

**Use Metric Trees when:**
- Defining success criteria
- Connecting feature to business outcomes
- Identifying leading indicators

**Use MoSCoW/RICE when:**
- Prioritizing features for MVP
- Managing scope creep
- Communicating trade-offs

**Use Pyramid Principle when:**
- Writing executive summary
- Structuring arguments
- Making PRD scannable

**Use Stakeholder Mapping when:**
- Complex cross-functional initiative
- Need to manage many approvers
- Tailoring PRD for different audiences

**Use Story Mapping when:**
- Planning multi-phase rollout
- Aligning team on scope
- Visualizing user journey

**Use Review Process when:**
- Every PRD (always peer review)
- High-stakes features (multiple review rounds)
- Contentious decisions (pre-socialize)
