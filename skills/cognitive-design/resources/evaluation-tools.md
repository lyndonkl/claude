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

**Test:** 5-second test (show design, ask what they remember). **Pass:** Identify purpose. **Fail:** Remember decoration or miss point.
**Common failures:** Cluttered layout, poor contrast, content buried below fold.
**Fix priorities:** CRITICAL (contrast), HIGH (5-second clarity), MEDIUM (hierarchy)

---

#### 2. Visual Hierarchy

**Goal:** Users can distinguish primary vs secondary vs tertiary content

**Checklist:**
- [ ] Is visual hierarchy clear? (size, contrast, position differentiate importance)
- [ ] Do headings/labels form clear levels? (H1 > H2 > H3 > body)
- [ ] Does design pass "squint test"? (important elements still visible when blurred)
- [ ] Are calls-to-action visually prominent?

**Test:** Squint test (blur design). **Pass:** Important elements visible when blurred. **Fail:** Everything same weight.
**Common failures:** Everything same size, primary CTA not distinguished, decoration more prominent than data.
**Fix priorities:** HIGH (primary not prominent), MEDIUM (heading hierarchy), LOW (minor adjustments)

---

#### 3. Chunking & Organization

**Goal:** Information grouped to fit working memory capacity (4±1 chunks, max 7)

**Checklist:**
- [ ] Are long lists broken into categories? (≤7 items per unbroken list)
- [ ] Are related items visually grouped? (proximity, backgrounds, whitespace)
- [ ] Is navigation organized into logical categories? (≤7 top-level items)
- [ ] Are form fields grouped by relationship? (personal info, account, preferences)

**Test:** Count ungrouped items. **Pass:** ≤7 items or clear grouping. **Fail:** >7 items ungrouped.
**Common failures:** 15+ flat navigation, 30-field ungrouped form, 20 equal-weight metrics.
**Fix priorities:** CRITICAL (>10 ungrouped), HIGH (7-10 ungrouped), MEDIUM (clearer groups)

---

#### 4. Simplicity & Clarity

**Goal:** Every element serves user goal; extraneous elements removed

**Checklist:**
- [ ] Can you justify every visual element? (Does it convey information or improve usability?)
- [ ] Is data-ink ratio high? (maximize ink showing data, minimize decoration)
- [ ] Are decorative elements eliminated? (chartjunk, unnecessary lines, ornaments)
- [ ] Is terminology familiar or explained? (no unexplained jargon)

**Test:** Point to each element, ask "What purpose?" **Pass:** Every element justified. **Fail:** Decorative/unclear elements.
**Common failures:** Chartjunk (3D, backgrounds, excess gridlines), jargon, redundant elements.
**Fix priorities:** HIGH (decoration competing with data), MEDIUM (unexplained terms), LOW (minor simplification)

---

#### 5. Memory Support

**Goal:** Users don't need to remember what could be shown (recognition over recall)

**Checklist:**
- [ ] Is current system state visible? (active filters, current page, progress through flow)
- [ ] Are navigation breadcrumbs provided? (where am I, how did I get here)
- [ ] For multi-step processes, is progress shown? (wizard step X of Y)
- [ ] Are options presented rather than requiring recall? (dropdowns vs typed commands)

**Test:** Identify what users must remember. Ask "Could this be shown?" **Pass:** State visible. **Fail:** Relying on memory.
**Common failures:** No active filter indication, no progress indicator, hidden state.
**Fix priorities:** CRITICAL (lost in flow), HIGH (critical state invisible), MEDIUM (minor memory aids)

---

#### 6. Feedback & Interaction

**Goal:** Every action gets immediate, clear feedback

**Checklist:**
- [ ] Do all interactive elements provide immediate feedback? (hover states, click feedback)
- [ ] Are loading states shown? (spinners, progress bars for waits >1 second)
- [ ] Do form fields validate inline? (immediate feedback, not after submit)
- [ ] Are error messages contextual? (next to problem, not top of page)
- [ ] Are success confirmations shown? ("Saved", checkmarks)

**Test:** Click/interact. **Pass:** Feedback within 100ms. **Fail:** No feedback or delayed >1s without indicator.
**Common failures:** No hover states, no loading indicator, errors not contextual, no success confirmation.
**Fix priorities:** CRITICAL (no feedback for critical actions), HIGH (delayed without loading), MEDIUM (missing hover)

---

#### 7. Consistency

**Goal:** Repeated patterns throughout (terminology, layout, interactions, visual style)

**Checklist:**
- [ ] Is terminology consistent? (same words for same concepts)
- [ ] Are UI patterns consistent? (buttons, links, inputs styled uniformly)
- [ ] Is color usage consistent? (red = error, green = success throughout)
- [ ] Are interaction patterns predictable? (click/tap behavior consistent)

**Test:** List similar elements, check consistency. **Pass:** Identical styling/behavior. **Fail:** Unjustified variations.
**Common failures:** Inconsistent terminology ("Email" vs "E-mail"), visual inconsistency (button styles vary), semantic inconsistency (red means error and negative).
**Fix priorities:** HIGH (terminology), MEDIUM (visual styling), LOW (minor patterns)

---

#### 8. Scanning Patterns

**Goal:** Layout leverages predictable F-pattern or Z-pattern scanning

**Checklist:**
- [ ] Is primary content positioned top-left? (where scanning starts)
- [ ] For text-heavy content, does layout follow F-pattern? (top horizontal, then down left, short mid horizontal)
- [ ] For visual-heavy content, does layout follow Z-pattern? (top-left to top-right, diagonal to bottom-left, then bottom-right)
- [ ] Are terminal actions positioned bottom-right? (where scanning ends)

**Test:** Trace eye movement (F/Z pattern). **Pass:** Critical elements on path. **Fail:** Important content off path.
**Common failures:** Primary CTA bottom-left (off Z-pattern), key info middle-right (off F-pattern), patterns ignored.
**Fix priorities:** MEDIUM (CTA off path), LOW (secondary optimization)

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

**Context:** Team dashboard with 20 metrics, users overwhelmed and missing alerts

**Checklist Results:**
- ❌ **Visibility:** Too cluttered, 20 equal-weight metrics
- ❌ **Hierarchy:** Everything same size, alerts not prominent
- ❌ **Chunking:** 15 ungrouped metrics (exceeds working memory)
- ❌ **Simplicity:** Chartjunk (gridlines, 3D, gradients)
- ❌ **Memory:** No active filter indication
- ✓ **Feedback:** Hover states, loading indicators present
- ⚠️ **Consistency:** Mostly consistent, minor button variations
- ❌ **Scanning:** Key KPI bottom-right (off F-pattern)

**Fixes:** (1) Reduce to 3-4 primary KPIs top-left, group others. (2) Remove chartjunk, establish hierarchy. (3) Show active filters as chips. (4) Standardize buttons.

**Outcome:** Users grasp status in 5 seconds, find alerts immediately

---

### Example 2: Bar Chart Audit Using 4 Criteria

**Context:** Q4 sales bar chart for presentation

**Audit Scores:**
- **Clarity (4/5):** Clear title/labels, direct bar labels. Minor: Could annotate top performer.
- **Efficiency (5/5):** Optimal position/length encoding, sorted descending, common baseline.
- **Integrity (2/5 - CRITICAL):** ❌ Y-axis starts at 80 (exaggerates differences), ❌ No historical context.
- **Aesthetics (4/5):** Clean, professional. Minor: Could use brand colors.

**Average:** 3.75/5 (barely passes). **Critical issue:** Integrity <3 unacceptable.

**Fixes:** (1) Start y-axis at zero or add break symbol + "Axis truncated" note. (2) Add Q3 baseline for context. (3) Annotate: "West region led Q4 with 23% increase."

**After fixes:** Clarity 5/5, Efficiency 5/5, Integrity 5/5, Aesthetics 4/5 = **4.75/5 Excellent**

