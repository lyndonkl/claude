# Business Narrative Builder Templates

Templates for company context gathering, life cycle classification, TAM sizing, narrative construction, and value driver mapping.

## Table of Contents
- [Company Context Questionnaire](#company-context-questionnaire)
- [Life Cycle Classification Checklist](#life-cycle-classification-checklist)
- [TAM Sizing Template](#tam-sizing-template)
- [Narrative Document Template](#narrative-document-template)
- [Value Driver Mapping Table](#value-driver-mapping-table)
- [Alternative Narrative Template](#alternative-narrative-template)

---

## Company Context Questionnaire

Gather this information before constructing a narrative:

### Company Profile

- **Company name**:
- **Industry / sector**:
- **Founded / age**:
- **Public or private**:
- **Headquarters / geography**:

### Current Financials

- **Revenue (trailing 12 months)**:
- **Revenue growth rate (1-year, 3-year)**:
- **Operating income / EBIT**:
- **Operating margin**:
- **Net income**:
- **Invested capital (debt + equity - cash)**:
- **Cash on hand**:
- **Total debt**:

### Business Description

- **Products/services** (what does the company sell?):
- **Revenue model** (subscription, transactional, advertising, licensing):
- **Key customers/segments**:
- **Geographic revenue breakdown** (by region or country):

### Competitive Landscape

- **Primary competitors** (3-5):
- **Market position** (leader, challenger, niche):
- **Competitive advantages** (brand, network effects, IP, cost structure, regulatory):
- **Barriers to entry** (capital, regulation, technology, scale):

### Management and Strategy

- **CEO tenure and track record**:
- **Stated strategy / vision**:
- **Recent major decisions** (acquisitions, divestitures, pivots):
- **Capital allocation priorities** (growth investment, dividends, buybacks, debt reduction):

### Risk Profile

- **Key risks** (competitive, regulatory, technological, financial):
- **Cash burn rate** (if unprofitable):
- **Months of cash remaining** (if applicable):
- **Debt maturity profile**:

---

## Life Cycle Classification Checklist

Use this checklist to classify the company into one of the 6 stages. Check the characteristics that apply, then select the stage with the most matching items.

### Stage 1: Start-up
- [ ] Revenue is minimal or zero
- [ ] Deep operating losses
- [ ] Product still in development or early market testing
- [ ] Funded primarily by founders, angels, or early-stage VC
- [ ] No meaningful competition yet (market may not exist)
- [ ] Key question: Does the idea have potential?

### Stage 2: Young Growth
- [ ] Revenue growing rapidly (>30% per year)
- [ ] Operating income is negative or barely positive
- [ ] Business model being validated and refined
- [ ] Funded by venture capital, early public markets, or private equity
- [ ] Competition emerging but market is still forming
- [ ] Key question: Is there a viable business model to commercialize?

### Stage 3: High Growth
- [ ] Revenue growing at 15-30% per year
- [ ] Operating income turning positive or becoming meaningful
- [ ] Business model proven; focus is on scaling
- [ ] Generating some internal cash flow, supplemented by external capital
- [ ] Multiple competitors in the space
- [ ] Key question: Will the business generate profits at scale?

### Stage 4: Mature Growth
- [ ] Revenue growing at 5-15% per year
- [ ] Positive and growing operating income
- [ ] Cash flows fund most reinvestment needs
- [ ] Looking to expand into adjacent markets or geographies
- [ ] Competition is established with clear market structure
- [ ] Key question: Can the business continue to scale profitably?

### Stage 5: Mature Stable
- [ ] Revenue growth near GDP (0-5%)
- [ ] High and stable operating margins
- [ ] Strong free cash flow generation
- [ ] Returning cash to shareholders (dividends, buybacks)
- [ ] Defending market position against disruptors
- [ ] Key question: Can the business be defended?

### Stage 6: Decline
- [ ] Revenue declining
- [ ] Operating margins under pressure
- [ ] Market shrinking or being disrupted
- [ ] Considering asset sales, restructuring, or strategic alternatives
- [ ] Management facing existential strategic choices
- [ ] Key question: Will management face reality?

**Selected stage**: ____________

**Confidence**: High / Medium / Low

**Rationale**: (explain why this stage was chosen; note any characteristics that point to an adjacent stage)

---

## TAM Sizing Template

### Top-Down Approach

Start with the broadest relevant market and filter to the addressable segment.

```
Total market (global or regional):               $________
  x Relevant segment filter 1 (________):        x ____%
  x Relevant segment filter 2 (________):        x ____%
  x Geographic filter (if applicable):            x ____%
= Total Addressable Market (TAM):                $________

  x Realistic penetration rate (5-year):          x ____%
= Serviceable Obtainable Market (SOM):            $________
```

**Sources and assumptions**:
- Total market estimate source:
- Filter rationale:
- Penetration rate basis:

### Bottom-Up Approach

Start with the unit economics and scale to the addressable population.

```
Number of potential customers/units:              ________
  x Addressable percentage:                       x ____%
= Addressable customers/units:                    ________
  x Revenue per customer/unit per year:           $________
= Total Addressable Market (TAM):                 $________
```

**Sources and assumptions**:
- Customer count source:
- Revenue per customer basis:

### TAM Cross-Check

| Metric | Top-Down | Bottom-Up |
|--------|----------|-----------|
| TAM estimate | $ | $ |
| Ratio (higher / lower) | | |
| Within 3x? | Yes / No | |

If estimates differ by more than 3x, investigate which assumptions diverge and refine.

### Market Growth Trajectory

| Year | Market Size | Company Revenue | Implied Share |
|------|-------------|-----------------|---------------|
| Current | $ | $ | % |
| Year 3 | $ | $ | % |
| Year 5 | $ | $ | % |
| Year 10 | $ | $ | % |

Sanity check: Does implied market share at year 10 exceed 30-40% in a competitive market? If so, revisit the revenue growth assumption.

---

## Narrative Document Template

### The Narrative

**One-sentence summary**: (e.g., "Tesla will become the mass-market EV maker, capturing 10% of the global auto market")

**Full narrative** (3-5 sentences describing the story of how the business evolves over time):

### Life Cycle Assessment

**Current stage**: (from classification checklist)

**Expected trajectory**: (e.g., "Move from Young Growth to High Growth within 3-5 years as production scales")

### Market Opportunity

**TAM**: $________ (source and methodology)

**Target share at maturity**: ________%

**Revenue at maturity**: $________

### Competitive Position

**Primary advantages**:
1.
2.
3.

**Length of competitive advantage period**: ________ years

**Basis**: (what sustains the advantage -- brand, network effects, IP, regulation, cost structure?)

### Value Drivers (Summary)

| Driver | Value | Narrative Link |
|--------|-------|----------------|
| Revenue CAGR (high-growth period) | % | |
| Length of high-growth period | years | |
| Target operating margin | % | |
| Sales-to-capital ratio | x | |
| Cost of capital (WACC) | % | |
| Stable growth rate | % | |
| Failure probability | % | |

### Alternative Narratives

(See [Alternative Narrative Template](#alternative-narrative-template) below)

---

## Value Driver Mapping Table

For each driver, trace the connection from narrative element to number.

### Revenue Growth

| Element | Value | Source |
|---------|-------|--------|
| Current revenue | $ | Company financials |
| TAM at maturity | $ | TAM sizing template |
| Target market share | % | Competitive analysis |
| Target revenue at maturity | $ | TAM x share |
| Years to maturity | | Life cycle assessment |
| Implied CAGR | % | (Target/Current)^(1/n) - 1 |

### Operating Margin

| Element | Value | Source |
|---------|-------|--------|
| Current operating margin | % | Company financials |
| Industry median margin (mature peers) | % | Industry data |
| Industry 75th percentile margin | % | Industry data |
| Target operating margin | % | Narrative rationale |
| Years to reach target | | Growth period assumption |

**Narrative rationale for target margin**: (why this number? competitive advantage? cost structure? pricing power?)

### Reinvestment Efficiency

| Element | Value | Source |
|---------|-------|--------|
| Current sales-to-capital ratio | x | Revenue / Invested Capital |
| Industry average sales-to-capital | x | Industry data |
| Target sales-to-capital ratio | x | Narrative assumption |

**Narrative rationale**: (capital-light or capital-heavy model? improving or declining efficiency?)

### Risk Profile

| Element | Value | Source |
|---------|-------|--------|
| Estimated WACC | % | From cost-of-capital-estimator or estimate |
| Beta (estimated) | | Comparable firms or regression |
| Risk-free rate | % | Government bond yield |
| Equity risk premium | % | Market estimate |

### Failure Risk (for Young Growth or Distressed firms)

| Element | Value | Source |
|---------|-------|--------|
| Probability of failure | % | Cash burn analysis, industry base rates |
| Distress/liquidation value | $ | Asset-based estimate |
| Basis for failure probability | | (cash runway, Altman Z-score, industry data) |

---

## Alternative Narrative Template

Develop at least one alternative to the primary narrative.

### Alternative Narrative: ____________ (name: e.g., "Bull Case", "Bear Case", "Niche Player")

**One-sentence summary**:

**Full narrative** (3-5 sentences):

**How it differs from primary narrative**:

| Driver | Primary | Alternative | Difference |
|--------|---------|-------------|------------|
| Revenue CAGR | % | % | |
| Target operating margin | % | % | |
| Sales-to-capital | x | x | |
| WACC | % | % | |
| Failure probability | % | % | |

**What would make this narrative more likely?** (specific events, data, or signals):

**What would make this narrative less likely?**:

---

## Complete Estimation Workflow

1. **Context**: Fill out Company Context Questionnaire
2. **Stage**: Complete Life Cycle Classification Checklist
3. **Market**: Fill in TAM Sizing Template (both top-down and bottom-up)
4. **Story**: Write the Narrative Document
5. **Numbers**: Complete the Value Driver Mapping Table
6. **Alternatives**: Write at least one Alternative Narrative
7. **Validate**: Score against rubric (target average >= 3.5)
