---
name: business-narrative-builder
description: Constructs a structured narrative linking a company's qualitative business story to quantitative valuation drivers (revenue growth, target margin, reinvestment efficiency, cost of capital, failure risk). Classifies the company within a 6-stage corporate life cycle and sizes the total addressable market. Use when starting a company analysis, building a valuation narrative, assessing competitive position, sizing TAM, or when user mentions business narrative, story to numbers, life cycle stage, or company analysis.
---
# Business Narrative Builder

## Table of Contents
- [Example](#example)
- [Workflow](#workflow)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Example

**Company**: Tesla, circa 2018

**Narrative**: "Tesla will become the mass-market electric vehicle company, leveraging its brand and technology lead to capture a meaningful share of the global auto market as it transitions from internal combustion to electric."

**Life Cycle Stage**: Stage 2 -- Young Growth
- Revenue growing rapidly (~80% YoY) but negative operating income
- Key uncertainty: Is there a business model that can be commercialized at scale?
- Company-specific risk dominates macro risk

**TAM Sizing**:
- Global auto market: ~$2T in annual revenues
- EV share trajectory: ~3% today, targeting 25-30% in 10 years (~$500-600B)
- Tesla target share of EV market: 20-30% (~$100-180B in revenue at maturity)

**Value Drivers Derived from Narrative**:

| Driver | Value | Rationale |
|--------|-------|-----------|
| Revenue CAGR (next 10 years) | ~25% | From $21B to ~$150B, bounded by TAM |
| Target operating margin | 10% | Auto industry top quartile; premium brand with manufacturing scale |
| Sales-to-capital ratio | 2.5x | Capital-intensive but improving; factory efficiency gains |
| Cost of capital (WACC) | ~8.5% | Young growth firm, high beta (1.3), moderate debt |
| Failure probability | 10% | Cash burn concerns, but improving production; distress value ~$50B (brand + factories) |

**Alternative narrative**: "Tesla remains a niche luxury EV maker with 2-3% of the global auto market, premium margins (12-15%) but limited scale." This narrative produces a lower revenue path (~$50B) but higher margins, yielding a different but defensible valuation.

## Workflow

Copy this checklist and track progress:

```
Business Narrative Builder Progress:
- [ ] Step 1: Gather company context
- [ ] Step 2: Classify life cycle stage
- [ ] Step 3: Size total addressable market
- [ ] Step 4: Develop business narrative
- [ ] Step 5: Convert narrative to value drivers
- [ ] Step 6: Validate narrative plausibility
```

**Step 1: Gather company context**

Collect: industry, current revenues, operating income, invested capital, products/services, competitive landscape, geographic breakdown, company age/stage. See [resources/template.md](resources/template.md#company-context-questionnaire) for the context questionnaire.

**Step 2: Classify life cycle stage**

Place the company in one of 6 stages (Start-up, Young Growth, High Growth, Mature Growth, Mature Stable, Decline). Each stage has distinct characteristics for revenue growth, earnings, funding, and competitive dynamics. See [resources/methodology.md](resources/methodology.md#6-stage-corporate-life-cycle-model) for the full stage definitions and classification criteria.

**Step 3: Size total addressable market**

Estimate TAM using top-down (total market filtered to addressable segment) and bottom-up (unit count times price). Distinguish between TAM (total), SAM (serviceable), and SOM (obtainable). See [resources/template.md](resources/template.md#tam-sizing-template) for the sizing template.

**Step 4: Develop business narrative**

Write a narrative describing how the business evolves over time. The narrative should answer: What market does the company operate in? How big can it get? What are its competitive advantages? How will it make money? See [resources/methodology.md](resources/methodology.md#narrative-to-numbers-framework) for the 5-step narrative process.

**Step 5: Convert narrative to value drivers**

Translate the narrative into the five quantitative drivers: (1) revenue growth rate and path, (2) target operating margin, (3) reinvestment efficiency (sales-to-capital), (4) risk profile (cost of capital), and (5) failure probability. Each number should trace back to a specific element of the story. See [resources/template.md](resources/template.md#value-driver-mapping-table) for the driver mapping table.

**Step 6: Validate narrative plausibility**

Test whether the narrative is possible (could it happen?), plausible (is it reasonable given evidence?), and probable (is it the most likely outcome?). Develop at least one alternative narrative. Validate using [resources/evaluators/rubric_business_narrative_builder.json](resources/evaluators/rubric_business_narrative_builder.json). Minimum standard: average score of 3.5 or above.

## Common Patterns

**Pattern 1: Young Growth Company**
- **Profile**: Negative or thin earnings, high revenue growth, large TAM, wide range of outcomes
- **Narrative focus**: Can the business model work at scale? What is the path to profitability?
- **Key drivers**: Revenue CAGR (20-50%+), target margin from mature industry peers, high sales-to-capital, elevated failure probability (10-30%)
- **Examples**: Tesla (2018), Uber (pre-profitability), early-stage SaaS companies
- **Watch for**: Overestimating TAM penetration, underestimating time to profitability, ignoring cash burn and survival risk

**Pattern 2: Mature Growth Company**
- **Profile**: Positive and growing earnings, moderate revenue growth, proven business model
- **Narrative focus**: Can the company scale profitably? Where does reinvestment go?
- **Key drivers**: Revenue CAGR (8-20%), operating margin at or near target, reinvestment in existing and adjacent markets
- **Examples**: Amazon (2020s), Alphabet, enterprise software companies in growth mode
- **Watch for**: Assuming current growth rates persist indefinitely, missing margin compression from competition

**Pattern 3: Mature Stable Company**
- **Profile**: Slowing revenue growth, high and stable margins, strong free cash flow
- **Narrative focus**: Can the business be defended? How durable is the competitive advantage?
- **Key drivers**: Revenue growth near GDP (2-5%), stable operating margin, declining reinvestment needs, focus on capital return
- **Examples**: Coca-Cola, Johnson & Johnson, established consumer staples
- **Watch for**: Overvaluing stability (disruption risk exists), ignoring secular decline in legacy segments

**Pattern 4: Decline or Turnaround Company**
- **Profile**: Shrinking revenue, deteriorating margins, potential for narrative change
- **Narrative focus**: Will management face reality? Is there a credible turnaround story?
- **Key drivers**: Negative or low revenue growth, margin pressure, potential asset sales or restructuring, new management or strategy shift
- **Examples**: Legacy retailers, declining media companies, post-disruption incumbents
- **Watch for**: Anchoring on historical performance, overly optimistic turnaround assumptions, ignoring distress costs

## Guardrails

1. **Every narrative should be testable.** Frame the narrative so it can be classified as possible (could happen), plausible (reasonable given evidence), or probable (likely outcome). Untestable narratives produce arbitrary numbers.

2. **Revenue growth path should be bounded by TAM.** The company cannot grow larger than its addressable market. If a 10-year revenue projection implies market share above 30-40% of a competitive market, revisit the assumptions.

3. **Target operating margin should be benchmarked against industry quartiles.** Use mature companies in the same sector as the reference point. A narrative claiming margins 2x the industry median requires a compelling competitive advantage explanation.

4. **Stable growth rate should not exceed the risk-free rate or nominal GDP growth.** No company can grow faster than the economy indefinitely. The terminal growth rate in any narrative should converge to 2-4% (nominal).

5. **Failure probability should be stated for young and distressed firms.** For companies in Start-up, Young Growth, or Decline stages, explicitly estimate the probability that the firm does not survive as a going concern. Base this on cash burn rate, available capital, and industry failure rates.

6. **Alternative narratives should be acknowledged.** A single narrative creates false precision. Develop at least one alternative story (bull/bear, different strategic path) and note how it changes the value drivers. This discipline reduces confirmation bias.

## Quick Reference

**Key formulas:**

```
Expected FCFF = Revenue x Operating Margin x (1 - Tax Rate) - Reinvestment

Revenue Growth (CAGR) = (Target Revenue / Current Revenue)^(1/n) - 1

Sales-to-Capital Ratio = Revenue / Invested Capital
  (measures reinvestment efficiency: higher = less capital needed per dollar of revenue)

Reinvestment = Change in Revenue / Sales-to-Capital Ratio

Value of Firm = Sum of [FCFF_t / (1 + WACC)^t] + Terminal Value / (1 + WACC)^n
  (preview: detailed DCF mechanics are in intrinsic-valuation-dcf)
```

**Life cycle stages (summary):**

| Stage | Revenue Growth | Earnings | Key Question |
|-------|---------------|----------|--------------|
| 1. Start-up | Minimal | Deep negative | Does the idea have potential? |
| 2. Young Growth | Very high (>30%) | Negative/thin | Is there a viable business model? |
| 3. High Growth | High (15-30%) | Turning positive | Will it generate profits at scale? |
| 4. Mature Growth | Moderate (5-15%) | Growing | Can the business scale further? |
| 5. Mature Stable | Low (0-5%) | High and stable | Can the business be defended? |
| 6. Decline | Negative | Declining | Will management face reality? |

**Resources:**

- **[resources/template.md](resources/template.md)**: Company context questionnaire, life cycle classification checklist, TAM sizing template, narrative document template, value driver mapping table
- **[resources/methodology.md](resources/methodology.md)**: 6-stage life cycle model detail, Damodaran's 5-step narrative-to-numbers framework, narrative plausibility testing, competitive advantage assessment, TAM methodology
- **[resources/evaluators/rubric_business_narrative_builder.json](resources/evaluators/rubric_business_narrative_builder.json)**: Quality criteria for narrative clarity, life cycle classification, TAM sizing, driver linkage, plausibility

**Inputs required:**

- Company name, industry, and current financials (revenue, operating income, invested capital)
- Products/services description and competitive landscape
- Geographic revenue breakdown
- Company age, stage, and management assessment

**Outputs produced:**

- `business-narrative.md`: Narrative document linking story to numbers, life cycle classification, TAM estimate, value driver table, alternative narratives
