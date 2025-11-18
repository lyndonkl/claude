# Evaluation Tools

This resource provides systematic checklists and frameworks for evaluating designs against cognitive principles.

**Tools covered:**
1. Cognitive Design Checklist (general interface/visualization evaluation)
2. Visualization Audit Framework (4-criteria data visualization quality assessment)

---

## Why Systematic Evaluation

### WHY This Matters

**Core insight:** Cognitive design has multiple dimensions - visibility, hierarchy, chunking, consistency, feedback, memory support, integrity. Ad-hoc review often misses issues in one or more dimensions.

**Benefits of systematic evaluation:**
- **Comprehensive coverage:** Ensures all cognitive principles checked
- **Objective assessment:** Reduces subjective bias
- **Catches issues early:** Before launch or during design critiques
- **Team alignment:** Shared criteria for quality
- **Measurable improvement:** Track fixes over time

**Mental model:** Like a pre-flight checklist for pilots - systematically verify all critical systems before takeoff.

Without systematic evaluation: missed cognitive issues, inconsistent quality, user confusion that could have been prevented.

**Use when:**
- Conducting design reviews/critiques
- Evaluating existing designs for improvement
- Quality assurance before launch
- Diagnosing why design feels "off"
- Teaching/mentoring cognitive design

---

## What You'll Learn

**Two complementary tools:**

**Cognitive Design Checklist:** General-purpose evaluation for any interface, visualization, or content
- Quick questions across 6 dimensions
- Suitable for any design context
- 10-15 minutes for thorough review

**Visualization Audit Framework:** Specialized 4-criteria assessment for data visualizations
- Clarity, Efficiency, Integrity, Aesthetics
- Systematic quality scoring
- 15-30 minutes depending on complexity

---

## Why Cognitive Design Checklist

### WHY This Matters

**Purpose:** Catch glaring cognitive problems before they reach users.

**Coverage areas:**
1. Visibility & Comprehension (can users see and understand?)
2. Visual Hierarchy (what gets noticed first?)
3. Chunking & Organization (fits working memory?)
4. Simplicity & Clarity (extraneous elements removed?)
5. Memory Support (state externalized?)
6. Feedback & Interaction (immediate responses?)
7. Consistency (patterns maintained?)
8. Scanning Patterns (layout leverages F/Z-pattern?)

**Mental model:** Like a doctor's diagnostic checklist - systematically check each vital sign.

---

### WHAT to Check

#### 1. Visibility & Immediate Comprehension

**Goal:** Core message/purpose graspable in ≤5 seconds

**Checklist:**
- [ ] Can users identify the purpose/main message within 5 seconds? (5-second test)
- [ ] Is important information visible without scrolling (above fold)?
- [ ] Is text/content legible? (sufficient size, contrast, line length)
- [ ] Are interactive elements distinguishable from static content?

**Test method:** Show design to unfamiliar user for 5 seconds, ask what they remember
- **Pass:** Correctly identify purpose/main message
- **Fail:** Remember decorative elements or miss key point

**Common failures:**
- Cluttered layout obscuring main message
- Poor contrast making text hard to read
- Everything buried below fold

**Fix priorities:**
- CRITICAL: Insufficient contrast (accessibility issue)
- HIGH: Main message not graspable in 5 seconds
- MEDIUM: Secondary content more prominent than primary

---

#### 2. Visual Hierarchy

**Goal:** Users can distinguish primary vs secondary vs tertiary content

**Checklist:**
- [ ] Is visual hierarchy clear? (size, contrast, position differentiate importance)
- [ ] Do headings/labels form clear levels? (H1 > H2 > H3 > body)
- [ ] Does design pass "squint test"? (important elements still visible when blurred)
- [ ] Are calls-to-action visually prominent?

**Squint Test:**
1. Blur design (actual squint or Gaussian blur filter)
2. Can you still identify what's most important?
   - **Pass:** Hierarchy survives blur
   - **Fail:** Everything looks same weight when blurred

**Common failures:**
- Everything same size/weight
- Primary CTA not visually distinguished
- Decorative elements more prominent than data

**Fix priorities:**
- HIGH: Primary content not prominent
- MEDIUM: Insufficient heading hierarchy
- LOW: Minor visual weight adjustments

---

#### 3. Chunking & Organization

**Goal:** Information grouped to fit working memory capacity (4±1 chunks, max 7)

**Checklist:**
- [ ] Are long lists broken into categories? (≤7 items per unbroken list)
- [ ] Are related items visually grouped? (proximity, backgrounds, whitespace)
- [ ] Is navigation organized into logical categories? (≤7 top-level items)
- [ ] Are form fields grouped by relationship? (personal info, account, preferences)

**Counting test:**
- Count ungrouped items in any section
- **Pass:** ≤7 items or clear visual grouping into chunks
- **Fail:** >7 items without grouping (cognitive overload)

**Common failures:**
- 15+ navigation items in flat list
- 30-field form without visual grouping
- Dashboard with 20 equal-weight metrics

**Fix priorities:**
- CRITICAL: >10 ungrouped items (overwhelming)
- HIGH: 7-10 items that could be grouped
- MEDIUM: Existing groups could be clearer

---

#### 4. Simplicity & Clarity

**Goal:** Every element serves user goal; extraneous elements removed

**Checklist:**
- [ ] Can you justify every visual element? (Does it convey information or improve usability?)
- [ ] Is data-ink ratio high? (maximize ink showing data, minimize decoration)
- [ ] Are decorative elements eliminated? (chartjunk, unnecessary lines, ornaments)
- [ ] Is terminology familiar or explained? (no unexplained jargon)

**Audit method:**
1. Point to each visual element
2. Ask: "What purpose does this serve?"
   - If answer is "decoration" or unclear → remove it
   - **Pass:** Every element justified
   - **Fail:** Decorative/unexplained elements present

**Common failures:**
- Chartjunk (3D effects, background images, excessive gridlines)
- Jargon without definitions
- Redundant elements

**Fix priorities:**
- HIGH: Decorative elements competing with data
- MEDIUM: Unexplained terminology
- LOW: Minor visual simplification

---

#### 5. Memory Support

**Goal:** Users don't need to remember what could be shown (recognition over recall)

**Checklist:**
- [ ] Is current system state visible? (active filters, current page, progress through flow)
- [ ] Are navigation breadcrumbs provided? (where am I, how did I get here)
- [ ] For multi-step processes, is progress shown? (wizard step X of Y)
- [ ] Are options presented rather than requiring recall? (dropdowns vs typed commands)

**Test method:**
- Identify what users must remember
- Ask: "Could this be shown instead?"
  - **Pass:** State externalized to interface
  - **Fail:** Relying on user memory

**Common failures:**
- No visible indication of active filters
- Multi-step process without progress indicator
- Hidden state (users must remember where they are)

**Fix priorities:**
- CRITICAL: Users getting lost in multi-step flow
- HIGH: Critical state not visible (active filters, current context)
- MEDIUM: Minor memory aids (breadcrumbs, tooltips)

---

#### 6. Feedback & Interaction

**Goal:** Every action gets immediate, clear feedback

**Checklist:**
- [ ] Do all interactive elements provide immediate feedback? (hover states, click feedback)
- [ ] Are loading states shown? (spinners, progress bars for waits >1 second)
- [ ] Do form fields validate inline? (immediate feedback, not after submit)
- [ ] Are error messages contextual? (next to problem, not top of page)
- [ ] Are success confirmations shown? ("Saved", checkmarks)

**Timing test:**
- Click button/interact with element
- **Pass:** Visible feedback within 100ms (perceived as immediate)
- **Fail:** No feedback or delayed >1 second without loading indicator

**Common failures:**
- No hover states (unclear what's clickable)
- Form submission without loading indicator
- Errors at top of page, not next to field
- No confirmation of successful actions

**Fix priorities:**
- CRITICAL: No feedback for critical actions (submit, delete)
- HIGH: Delayed feedback without loading state
- MEDIUM: Missing hover states

---

#### 7. Consistency

**Goal:** Repeated patterns throughout (terminology, layout, interactions, visual style)

**Checklist:**
- [ ] Is terminology consistent? (same words for same concepts)
- [ ] Are UI patterns consistent? (buttons, links, inputs styled uniformly)
- [ ] Is color usage consistent? (red = error, green = success throughout)
- [ ] Are interaction patterns predictable? (click/tap behavior consistent)

**Audit method:**
1. List all instances of similar elements (all buttons, all error messages)
2. Check if they're identical or inconsistent
   - **Pass:** Consistent styling and behavior
   - **Fail:** Variations without justification

**Common failures:**
- "Email" in one place, "E-mail address" in another (terminology)
- Some buttons flat, some raised (visual inconsistency)
- Red sometimes means error, sometimes negative value (semantic inconsistency)

**Fix priorities:**
- HIGH: Inconsistent terminology (causes confusion)
- MEDIUM: Inconsistent visual styling (reduces learnability)
- LOW: Minor interaction pattern variations

---

#### 8. Scanning Patterns

**Goal:** Layout leverages predictable F-pattern or Z-pattern scanning

**Checklist:**
- [ ] Is primary content positioned top-left? (where scanning starts)
- [ ] For text-heavy content, does layout follow F-pattern? (top horizontal, then down left, short mid horizontal)
- [ ] For visual-heavy content, does layout follow Z-pattern? (top-left to top-right, diagonal to bottom-left, then bottom-right)
- [ ] Are terminal actions positioned bottom-right? (where scanning ends)

**Pattern test:**
1. Trace expected eye movement (F or Z based on content type)
2. Does path hit important elements?
   - **Pass:** Critical elements along natural scanning path
   - **Fail:** Important content off expected path

**Common failures:**
- Primary CTA bottom-left (off Z-pattern terminus)
- Key information buried middle-right (not on F-pattern)
- Ignoring scanning patterns entirely

**Fix priorities:**
- MEDIUM: Primary CTA not on expected path
- LOW: Secondary content optimization

---

## Why Visualization Audit Framework

### WHY This Matters

**Purpose:** Comprehensive quality assessment for data visualizations across four independent dimensions.

**Key insight:** Visualization quality requires success on ALL four criteria - high score on one doesn't compensate for failure on another.

**Four Criteria:**
1. **Clarity:** Immediately understandable and unambiguous
2. **Efficiency:** Minimal cognitive effort to extract information
3. **Integrity:** Truthful and free from misleading distortions
4. **Aesthetics:** Visually pleasing and appropriate

**Mental model:** Like evaluating a car - needs to be safe (integrity), functional (efficiency), easy to use (clarity), and pleasant (aesthetics). Missing any dimension makes it poor overall.

**Use when:**
- Evaluating data visualizations (charts, dashboards, infographics)
- Choosing between visualization alternatives
- Quality assurance before publication
- Diagnosing why visualization isn't working

---

### WHAT to Audit

#### Criterion 1: Clarity

**Question:** Is visualization immediately understandable and unambiguous?

**Checklist:**
- [ ] Is main message obvious or clearly annotated?
- [ ] Are axes labeled with units?
- [ ] Is legend clear and necessary? (or use direct labels if possible)
- [ ] Is title descriptive? (conveys what's being shown)
- [ ] Are annotations used to guide interpretation?
- [ ] Is chart type appropriate for message?

**5-Second Test:**
- Show visualization for 5 seconds
- Ask: "What's the main point?"
  - **Pass:** Correctly identify main insight
  - **Fail:** Confused or remember decorative elements instead

**Scoring:**
- **5 (Excellent):** Main message graspable in <5 seconds, perfectly labeled
- **4 (Good):** Clear with minor improvements needed (e.g., better title)
- **3 (Adequate):** Understandable but requires effort
- **2 (Needs work):** Ambiguous or missing critical labels
- **1 (Poor):** Incomprehensible

---

#### Criterion 2: Efficiency

**Question:** Can users extract information with minimal cognitive effort?

**Checklist:**
- [ ] Are encodings appropriate for task? (position/length for comparison, not angle/area)
- [ ] Is chart type matched to user task? (compare → bar, trend → line, distribution → histogram)
- [ ] Is comparison easy? (common baseline, aligned scales)
- [ ] Is cross-referencing minimized? (direct labels instead of legend lookups)
- [ ] Are cognitive shortcuts enabled? (sorting by value, highlighting key points)

**Encoding Check:**
- Identify user task (compare, see trend, find outliers)
- Check encoding against Cleveland & McGill hierarchy
  - **Pass:** Position/length used for precise comparisons
  - **Fail:** Angle/area/color used when position would work better

**Scoring:**
- **5 (Excellent):** Optimal encoding, zero wasted cognitive effort
- **4 (Good):** Appropriate with minor inefficiencies
- **3 (Adequate):** Works but more effort than necessary
- **2 (Needs work):** Poor encoding choice (pie when bar would be better)
- **1 (Poor):** Wrong chart type for task

---

#### Criterion 3: Integrity

**Question:** Is visualization truthful and free from misleading distortions?

**Checklist:**
- [ ] Do axes start at zero (or clearly note truncation)?
- [ ] Are scale intervals uniform?
- [ ] Is data complete? (not cherry-picked dates hiding context)
- [ ] Are comparisons fair? (same scale for compared items)
- [ ] Is context provided? (baselines, historical comparison, benchmarks)
- [ ] Are limitations noted? (sample size, data source, margin of error)

**Integrity Tests:**
1. **Axis test:** Does y-axis start at zero for bar charts? If not, is truncation clearly noted?
   - **Pass:** Zero baseline or explicit truncation note
   - **Fail:** Truncated axis exaggerating differences without disclosure

2. **Completeness test:** Is full relevant time period shown? Or cherry-picked subset?
   - **Pass:** Complete data with context
   - **Fail:** Selective dates hiding broader trend

3. **Fairness test:** Are compared items on same scale?
   - **Pass:** Common scale enables fair comparison
   - **Fail:** Dual-axis manipulation creates false correlation

**Scoring:**
- **5 (Excellent):** Completely honest, full context provided
- **4 (Good):** Honest with minor context improvements possible
- **3 (Adequate):** Not misleading but could provide more context
- **2 (Needs work):** Distortions present (truncated axis, cherry-picked data)
- **1 (Poor):** Actively misleading (severe distortions, no context)

**CRITICAL:** Scores below 3 on integrity are unacceptable - fix immediately

---

#### Criterion 4: Aesthetics

**Question:** Is visualization visually pleasing and appropriate for context?

**Checklist:**
- [ ] Is visual design professional and polished?
- [ ] Is color palette appropriate? (not garish, suits content tone)
- [ ] Is whitespace used effectively? (not cramped, not wasteful)
- [ ] Are typography choices appropriate? (readable, professional)
- [ ] Does style match context? (serious for finance, friendly for consumer)

**Important:** Aesthetics should NEVER undermine clarity or integrity

**Scoring:**
- **5 (Excellent):** Beautiful and appropriate, enhances engagement
- **4 (Good):** Pleasant and professional
- **3 (Adequate):** Acceptable, not ugly but not polished
- **2 (Needs work):** Amateurish or inappropriate style
- **1 (Poor):** Ugly or completely inappropriate

**Trade-off Note:** If forced to choose, prioritize Clarity and Integrity over Aesthetics

---

#### Using the 4-Criteria Framework

**Process:**

**Step 1: Evaluate each criterion independently**
- Score Clarity (1-5)
- Score Efficiency (1-5)
- Score Integrity (1-5)
- Score Aesthetics (1-5)

**Step 2: Calculate average**
- Average score = (Clarity + Efficiency + Integrity + Aesthetics) / 4
- **Pass threshold:** ≥3.5 average
- **Critical failures:** Any individual score <3 requires attention

**Step 3: Identify weakest dimension**
- Which criterion has lowest score?
- This is your primary improvement target

**Step 4: Prioritize fixes**
1. **CRITICAL:** Integrity < 3 (fix immediately - misleading is unacceptable)
2. **HIGH:** Clarity or Efficiency < 3 (users can't understand or use it)
3. **MEDIUM:** Aesthetics < 3 (affects engagement)
4. **LOW:** Scores 3-4 (optimization, not critical)

**Step 5: Verify fixes don't harm other dimensions**
- Example: Improving aesthetics shouldn't reduce clarity
- Example: Improving efficiency shouldn't compromise integrity

---

## Examples of Evaluation in Practice

### Example 1: Dashboard Review Using Checklist

**Context:** Team dashboard with 20 metrics, users report feeling overwhelmed and missing critical alerts

**Cognitive Design Checklist Application:**

**1. Visibility:** Can users see core message within seconds?
- ❌ FAIL: Too cluttered, no clear focal point
- Issue: 20 metrics all equal weight

**2. Visual Hierarchy:** Can users distinguish primary vs secondary?
- ❌ FAIL: Everything same size, no hierarchy
- Issue: Critical alerts look same as minor metrics

**3. Chunking:** Are items grouped into ≤7 clusters?
- ❌ FAIL: 15 ungrouped metrics in single view
- Issue: Exceeds working memory capacity

**4. Simplicity:** Every element justified?
- ❌ FAIL: Excessive gridlines, 3D effects, background gradients
- Issue: Chartjunk competing with data

**5. Memory Support:** Is state visible?
- ❌ FAIL: No indication of active filters
- Issue: Users forget which data subset they're viewing

**6. Feedback:** Immediate responses?
- ✓ PASS: Hover states, loading indicators present

**7. Consistency:** Patterns maintained?
- ⚠️ PARTIAL: Mostly consistent but some button styles vary

**8. Scanning Patterns:** Layout leverages F/Z-pattern?
- ❌ FAIL: Most important KPI bottom-right (off F-pattern)

**Diagnosis:** Multiple failures in visibility, hierarchy, chunking, simplicity, memory support, and scanning patterns

**Fix Priority:**
1. **CRITICAL:** Reduce to 3-4 primary KPIs top-left, group others (chunking + hierarchy)
2. **HIGH:** Remove chartjunk, establish clear hierarchy (simplicity + visibility)
3. **MEDIUM:** Show active filters as visible chips (memory support)
4. **LOW:** Standardize button styles (consistency)

**Outcome:** After fixes, users grasp status in 5 seconds, report finding alerts immediately

---

### Example 2: Bar Chart Audit Using 4 Criteria

**Context:** Sales comparison bar chart for quarterly presentation

**Visualization Audit Application:**

**1. Clarity (Score: 4/5 - Good)**
- ✓ Title clear: "Q4 Sales by Region"
- ✓ Direct labels on bars (no legend lookup needed)
- ✓ Axes labeled with units "Sales (thousands USD)"
- ⚠️ Minor: Could add annotation for top performer

**2. Efficiency (Score: 5/5 - Excellent)**
- ✓ Bar chart uses position/length encoding (optimal for comparison per Cleveland & McGill)
- ✓ Sorted descending (easy to identify ranking)
- ✓ Common baseline enables instant magnitude comparison

**3. Integrity (Score: 2/5 - NEEDS WORK)**
- ❌ Y-axis starts at 80 instead of zero → exaggerates differences
- ✓ Complete data (all regions included)
- ❌ No historical context (is this good/bad compared to previous quarters?)

**4. Aesthetics (Score: 4/5 - Good)**
- ✓ Clean design, professional color palette
- ✓ Appropriate whitespace
- ⚠️ Minor: Could use brand colors

**Average Score:** (4 + 5 + 2 + 4) / 4 = 3.75 (just above pass threshold)

**Critical Issue:** Integrity score below 3 - UNACCEPTABLE

**Fix Priority:**
1. **CRITICAL:** Start y-axis at zero (integrity fix)
   - Alternative if truncation necessary: Add break symbol and explicit note "Axis truncated to show detail"
2. **HIGH:** Add baseline comparison (e.g., dotted line showing Q3 average) for context
3. **MEDIUM:** Add annotation: "West region led Q4 with 23% increase over Q3"

**Outcome After Fixes:**
- Clarity: 5/5 (annotation added)
- Efficiency: 5/5 (unchanged)
- Integrity: 5/5 (axis fixed, context added)
- Aesthetics: 4/5 (unchanged)
- **New Average:** 4.75/5 - Excellent

