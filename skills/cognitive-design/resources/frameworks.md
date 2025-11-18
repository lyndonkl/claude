# Design Frameworks

This resource provides three systematic frameworks for structuring cognitive design thinking and decision-making.

**Frameworks covered:**
1. Cognitive Design Pyramid (hierarchical quality assessment)
2. Design Feedback Loop (interaction cycles)
3. Three-Layer Visualization Model (data communication fidelity)

---

## Why Use Frameworks

### WHY This Matters

Frameworks provide:
- **Systematic structure** for design thinking (not ad-hoc)
- **Complete coverage** across multiple dimensions
- **Prioritization guidance** (what to fix first)
- **Shared vocabulary** for team communication
- **Repeatable process** applicable across projects

**Mental model:** Like architectural blueprints - frameworks give structure to design decisions so nothing critical is forgotten.

Without frameworks: inconsistent application of principles, missed dimensions, unclear priorities, reinventing approach each time.

---

##What You'll Learn

Three complementary frameworks, each suited for different contexts:

**Cognitive Design Pyramid:** When you need comprehensive multi-dimensional quality assessment

**Design Feedback Loop:** When you're designing interactive interfaces and need to support user perception-action cycles

**Three-Layer Visualization Model:** When you're creating data visualizations and need to ensure fidelity from data through interpretation

---

## Why Cognitive Design Pyramid

### WHY This Matters

**Core insight:** Design effectiveness depends on satisfying multiple needs in hierarchical sequence - perceptual clarity is foundation, enabling cognitive coherence, which enables emotional engagement, which enables behavioral outcomes.

**Key principle:** Lower levels are prerequisites for higher levels:
- If users can't perceive elements clearly → coherence impossible
- If design isn't coherent → engagement suffers
- If not engaging → behavior change fails

**Mental model:** Like Maslow's hierarchy of needs - must satisfy foundational needs before higher-level needs matter.

**Use when:**
- Comprehensive design quality check needed
- Diagnosing what level is failing
- Prioritizing improvements (fix foundation first)
- Evaluating entire user experience holistically

---

### WHAT to Apply

#### The Pyramid (4 Tiers)

```
        ┌─────────────────────────┐
        │ BEHAVIORAL ALIGNMENT    │ ← Peak: Guides actual user behavior
        ├─────────────────────────┤
        │ EMOTIONAL ENGAGEMENT    │ ← Higher: Motivates and doesn't frustrate
        ├─────────────────────────┤
        │ COGNITIVE COHERENCE     │ ← Middle: Makes logical sense
        ├─────────────────────────┤
        │ PERCEPTUAL EFFICIENCY   │ ← Base: Seen and registered correctly
        └─────────────────────────┘
```

---

#### Tier 1: Perceptual Efficiency (Foundation)

**Goal:** Users can see and register all necessary elements clearly.

**Checkpoints:**
- [ ] Sufficient contrast for all text and key elements (WCAG AA minimum: 4.5:1 for body text, 3:1 for large text)
- [ ] Visual hierarchy obvious (squint test - primary elements still visible when blurred)
- [ ] No overwhelming clutter or visual noise (data-ink ratio high)
- [ ] Typography legible (appropriate size, line height, line length)
- [ ] Color distinguishable (not relying solely on hue for colorblind users)
- [ ] Grouping perceivable (Gestalt principles applied)

**Common failures:**
- Low contrast text (gray on light gray)
- Everything same visual weight (no hierarchy)
- Chartjunk obscuring data
- Text too small or lines too long

**Fix priority:** HIGHEST - without perception, nothing else works

**Example application:**
```
Dashboard review:
❌ Metrics all gray text, 12px, same size
✓ Primary KPIs 36px bold black, secondary 18px gray
```

---

#### Tier 2: Cognitive Coherence (Comprehension)

**Goal:** Information is organized to align with how users think and expect.

**Checkpoints:**
- [ ] Layout matches mental models and familiar patterns (standard UI conventions)
- [ ] Terminology consistent throughout (same words for same concepts)
- [ ] Navigation/flow logical and predictable (no mystery meat navigation)
- [ ] Memory aids present (breadcrumbs, state indicators, progress bars)
- [ ] Chunking within working memory capacity (≤7 items per group, ideally 4±1)
- [ ] Recognition over recall (show options, don't require memorization)

**Common failures:**
- Inconsistent terminology confusing users
- Non-standard UI patterns requiring re-learning
- Hidden navigation or state
- Unchunked long lists overwhelming memory

**Fix priority:** HIGH - enables users to understand and navigate

**Example application:**
```
Form review:
❌ 30 fields in sequence, no grouping, inconsistent labels ("Email" vs "E-mail address")
✓ 4-step wizard, grouped fields, consistent terminology, progress visible
```

---

#### Tier 3: Emotional Engagement (Motivation)

**Goal:** Design feels pleasant and motivating, not frustrating or anxiety-inducing.

**Checkpoints:**
- [ ] Aesthetic quality appropriate for context (professional/friendly/serious)
- [ ] Design feels pleasant to use (not frustrating)
- [ ] Anxiety reduced (progress shown, undo available, clear next steps)
- [ ] Tone matches user emotional state (encouraging for learning, calm for high-stress tasks)
- [ ] Accomplishment visible (checkmarks, confirmations, completed states)

**Common failures:**
- Ugly or amateurish appearance reducing trust
- Frustrating interactions causing stress
- No reassurance in multi-step processes
- Inappropriate tone (playful for serious tasks)

**Fix priority:** MEDIUM - affects engagement and trust, but only after foundation solid

**Why it matters:** Emotional state influences cognitive performance - pleasant affect improves problem-solving, stress narrows attention

**Example application:**
```
Onboarding review:
❌ Dense wall of text, no progress indicator, no encouragement
✓ Friendly tone, progress bar, checkmarks on completion, "You're almost done!"
```

---

#### Tier 4: Behavioral Alignment (Action)

**Goal:** Design guides users toward desired behaviors and outcomes.

**Checkpoints:**
- [ ] Calls-to-action clear and prominent (primary action obvious)
- [ ] Visual emphasis on actionable items (buttons stand out)
- [ ] Key takeaways highlighted (not buried in text)
- [ ] Ethical nudges toward good decisions (defaults favor user)
- [ ] Success paths more accessible than failure paths

**Common failures:**
- Primary CTA not visually prominent
- Actionable insights buried in data
- Destructive actions too easy (no confirmation)
- Defaults favor business over user

**Fix priority:** MEDIUM-LOW - optimize after foundation, coherence, engagement work

**Example application:**
```
Dashboard review:
❌ Insights hidden in footnotes, "View Details" button same size as "Export PDF"
✓ Key insight in large text at top, "Take Action" button prominent green, export secondary gray
```

---

#### Applying the Pyramid

**Process:**

**Step 1: Assess each tier bottom-up**
- Evaluate Tier 1 (Perceptual) - can users see clearly?
- Evaluate Tier 2 (Cognitive) - does it make sense?
- Evaluate Tier 3 (Emotional) - is it pleasant?
- Evaluate Tier 4 (Behavioral) - does it guide action?

**Step 2: Identify weakest tier**
- Where are the most failures?
- Which tier is blocking user success?

**Step 3: Prioritize fixes from foundation up**
- Fix Tier 1 issues first (perception enables everything)
- Then Tier 2 (coherence)
- Then Tier 3 and 4

**Step 4: Re-evaluate**
- Check that fixes at lower tiers didn't break higher tiers
- Iterate until all tiers pass

---

## Why Design Feedback Loop

### WHY This Matters

**Core insight:** Users don't passively consume interfaces - they actively engage in continuous perception-action-learning cycles.

**Loop stages:** Perceive → Interpret → Decide → Act → Learn → (loop repeats)

**Key principle:** Design must support every stage; break anywhere causes confusion or failure.

**Mental model:** Like a conversation - user asks (via perception), interface answers (via display), user responds (via action), interface confirms (via feedback), understanding updates (learning).

**Use when:**
- Designing interactive interfaces (apps, dashboards, tools)
- Ensuring each screen answers user's questions
- Providing appropriate feedback for actions
- Diagnosing where interaction breaks down

---

### WHAT to Apply

#### The Loop (5 Stages)

```
┌──────────┐
│ PERCEIVE │ → "What am I seeing?"
└────┬─────┘
     ↓
┌──────────┐
│INTERPRET │ → "What does this mean?"
└────┬─────┘
     ↓
┌──────────┐
│  DECIDE  │ → "What can I do next?"
└────┬─────┘
     ↓
┌──────────┐
│   ACT    │ → "How do I do it?"
└────┬─────┘
     ↓
┌──────────┐
│  LEARN   │ → "What happened? Was it successful?"
└────┬─────┘
     ↓
 (repeat)
```

---

#### Stage 1: Perceive

**User question:** "What am I seeing?"

**Design must provide:**
- [ ] Visibility of system status (current page, active state, what's happening)
- [ ] Clear visual hierarchy (where to look first)
- [ ] Salient critical elements (preattentive cues for important items)

**Common failures:**
- Hidden state (user doesn't know where they are)
- No visual hierarchy (don't know what's important)
- Loading without indicator (appears broken)

**Example application:**
```
Dashboard:
❌ No indication which filters are active
✓ Active filters shown as visible chips at top
```

---

#### Stage 2: Interpret

**User question:** "What does this mean?"

**Design must provide:**
- [ ] Clear labels and context (explain what user is seeing)
- [ ] Familiar terminology (or definitions for specialized terms)
- [ ] Adequate context (why am I here, what are these options)
- [ ] Visual encoding that matches meaning (charts appropriate for data type)

**Common failures:**
- Jargon or abbreviations without explanation
- Missing context (chart without title/axes labels)
- Unclear purpose of page/screen

**Example application:**
```
Data visualization:
❌ Chart with no title, axis labels "X" and "Y", no units
✓ "Q4 Sales by Region (thousands USD)", labeled axes, annotated key events
```

---

#### Stage 3: Decide

**User question:** "What can I do next?"

**Design must provide:**
- [ ] Available actions obvious (clear CTAs)
- [ ] Choices not overwhelming (Hick's Law - limit options)
- [ ] Recommended/default option suggested when appropriate
- [ ] Consequences of choices clear (especially for destructive actions)

**Common failures:**
- Too many options causing paralysis
- No guidance on what to do next
- Unclear consequences ("Are you sure?" without explaining what happens)

**Example application:**
```
Form:
❌ 10 buttons with unclear purposes
✓ Primary "Continue" button prominent, secondary "Save Draft" gray, "Cancel" text link
```

---

#### Stage 4: Act

**User question:** "How do I do it?"

**Design must provide:**
- [ ] Affordances clear (buttons look pressable, sliders look draggable)
- [ ] Controls accessible (appropriate size/position per Fitts's Law)
- [ ] Keyboard shortcuts available for power users
- [ ] Constraints prevent invalid actions (disabled states, input masking)

**Common failures:**
- Unclear what's clickable (flat design with no affordances)
- Tiny touch targets on mobile
- No keyboard access
- Allowing invalid inputs

**Example application:**
```
Button design:
❌ Flat text label, no visual cue it's interactive
✓ Raised appearance, hover state, cursor changes to pointer, focus ring for keyboard
```

---

#### Stage 5: Learn

**User question:** "What happened? Was it successful?"

**Design must provide:**
- [ ] Immediate feedback for every action (< 100ms for responsiveness perception)
- [ ] Confirmations for successful actions (checkmarks, "Saved" message, state change)
- [ ] Clear error messages in context (next to problem, plain language)
- [ ] Updated system state visible (if filter applied, data updates)

**Common failures:**
- No feedback (user clicks button, nothing visible happens)
- Delayed feedback (loading without indication)
- Generic errors ("Error occurred" without explanation)
- Feedback hidden or dismissible before user sees it

**Example application:**
```
Form submission:
❌ Button click → nothing visible → page eventually changes (or doesn't - user unsure if it worked)
✓ Button click → button shows spinner → success message appears → page transitions with confirmation
```

---

#### Applying the Feedback Loop

**For each screen/interaction, ask:**

1. **Perceive:** Can user see current state and what's important?
2. **Interpret:** Will user understand what they're seeing?
3. **Decide:** Are next actions clear and not overwhelming?
4. **Act:** Are controls obvious and accessible?
5. **Learn:** Will user get immediate, clear feedback?

**Example: Login form using loop**

**Perceive:** Username and password fields visible, labels clear
**Interpret:** "Log in to your account" heading provides context
**Decide:** Single "Log in" button obvious, "Forgot password?" link available
**Act:** Fields have focus states, button looks clickable, Enter key submits
**Learn:** Spinner appears on submit, success → redirect, error → message next to field with red border

---

## Why Three-Layer Visualization Model

### WHY This Matters

**Core insight:** Effective data visualization requires success at three distinct layers - accurate data, appropriate visual encoding, and correct user interpretation. Failure at any layer breaks the entire communication chain.

**Layers:** Data → Visual Encoding → Cognitive Interpretation

**Key principle:** You can have perfect data with wrong chart type (encoding failure) or perfect chart with user misunderstanding (interpretation failure). All three must succeed.

**Mental model:** Like a telephone game - message (data) must be transmitted (encoding) and received (interpretation) accurately or communication fails.

**Use when:**
- Creating any data visualization
- Diagnosing why visualization isn't working
- Choosing chart types
- Validating user understanding

---

### WHAT to Apply

#### Layer 1: Data

**Question:** Is the underlying data accurate, complete, and relevant?

**Checkpoints:**
- [ ] Data quality verified (no errors, outliers investigated)
- [ ] Complete dataset (not cherry-picked subset that misleads)
- [ ] Relevant to question being answered (not tangential data)
- [ ] Appropriate aggregation/granularity (not hiding or overwhelming with detail)
- [ ] Time period representative (not artificially truncated to show desired trend)

**Common failures:**
- Garbage data → garbage visualization
- Cherry-picked dates hiding broader context
- Outliers distorting scale
- Wrong metric for question

**Fix:** Validate data quality before designing visualization

**Example:**
```
Question: "Are sales improving?"
❌ Show only last 3 months (where sales happen to be up) hiding 2-year decline
✓ Show 2-year trend with annotation: "Recent uptick after sustained decline"
```

---

#### Layer 2: Visual Encoding

**Question:** Are visualization choices appropriate for the data type, user task, and perceptual capabilities?

**Checkpoints:**
- [ ] Chart type matches task (compare → bar, trend → line, distribution → histogram)
- [ ] Encoding matches perceptual hierarchy (position > angle > area)
- [ ] Axes scaled appropriately (start at zero for bars, or clearly note truncation)
- [ ] Color usage correct (hue for categories, lightness for quantities)
- [ ] Labels clear and sufficient (title, axes, units, legend if needed)

**Common failures:**
- Pie chart when bar chart would be clearer
- Truncated axis exaggerating differences
- Rainbow color scale for quantitative data
- Missing units or context

**Fix:** Match encoding to task using Cleveland & McGill hierarchy

**Example:**
```
Task: Compare 6 regional sales values
❌ Pie chart (angle/area encoding poor for comparison)
✓ Bar chart (position/length encoding enables precise comparison)
```

---

#### Layer 3: Cognitive Interpretation

**Question:** Will users correctly understand the message and draw valid conclusions?

**Checkpoints:**
- [ ] Main insight obvious or annotated (don't require users to discover it)
- [ ] Context provided (baselines, comparisons, historical trends)
- [ ] Audience knowledge level accommodated (annotations for novices)
- [ ] Potential misinterpretations prevented (annotations clarifying what NOT to conclude)
- [ ] Self-contained (doesn't require remembering distant information)

**Common failures:**
- Heap of data without guidance to key insight
- Missing context (percentage without denominator, comparison without baseline)
- Assumes expert knowledge novices lack
- Spurious correlation without clarification

**Fix:** Add titles, annotations, context; test with target users

**Example:**
```
Chart showing correlation between ice cream sales and drowning deaths
❌ No annotation → viewers conclude causation
✓ Annotation: "Both increase in summer (common cause), not causally related"
```

---

#### Applying the Three-Layer Model

**Process:**

**Step 1: Validate data layer**
- Check data quality, completeness, relevance
- Investigate outliers
- Ensure time period representative
- Verify aggregation appropriate

**Step 2: Choose encoding layer**
- Identify user task (compare, see trend, find outliers, etc.)
- Select chart type matching task + perceptual hierarchy
- Design axes, colors, labels appropriately
- Maximize data-ink ratio

**Step 3: Support interpretation layer**
- Add title conveying main message
- Annotate key insights
- Provide context (baselines, comparisons)
- Test with target users
- Add clarifications for potential misinterpretations

**Step 4: Iterate**
- Fix any layer showing weakness
- Re-validate that fixes don't break other layers

**Example: Sales dashboard using model**

**Layer 1 (Data):**
- Pull complete 2-year sales data
- Verify data quality (reconcile with finance)
- Identify 2 outlier months (big sale event) - note in visualization

**Layer 2 (Encoding):**
- User task: See trend + compare regions
- Chart: Line chart for trend (position over time), separate colored lines per region
- Axes: Start y-axis at zero, label units "Sales (thousands USD)", time on x-axis
- Color: Distinct hues per region (categorical), limit to 5 regions for clarity

**Layer 3 (Interpretation):**
- Title: "Regional Sales Trends 2023-2024: Overall Growth with West Leading"
- Annotate outlier months: "Holiday promotion (Nov 2023)", "Product launch (June 2024)"
- Provide context: Show previous year dotted line as comparison baseline
- Test with sales team - confirmed they grasp trends correctly

**Result:** Accurate data + appropriate encoding + correct interpretation = insight

---

## Choosing the Right Framework

**Use Cognitive Design Pyramid when:**
- Comprehensive multi-dimensional quality assessment needed
- Diagnosing which aspect of design is failing
- Prioritizing fixes (foundation → higher tiers)
- Evaluating entire user experience

**Use Design Feedback Loop when:**
- Designing interactive interfaces
- Ensuring each screen supports user questions
- Providing appropriate feedback
- Diagnosing where interaction breaks down

**Use Three-Layer Model when:**
- Creating data visualizations
- Choosing chart types
- Validating data quality through interpretation
- Diagnosing visualization failures

**Use multiple frameworks together for complete coverage**

