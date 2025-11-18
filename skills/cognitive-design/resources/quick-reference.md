# Quick Reference

This resource provides rapid access to core cognitive design principles and quick validation checks.

---

## Why Quick Reference

### WHY This Matters

Quick references enable:
- **Fast decision-making** during active design work
- **Rapid validation** without deep dive into theory
- **Team alignment** through shared heuristics
- **Design advocacy** with memorable, citable principles

**Mental model:** Like a cheat sheet or checklist for design decisions - quick lookups when you need them.

Without quick reference: slowed workflow, inconsistent application, forgetting key principles under time pressure.

---

## What to Use

### 20 Core Actionable Principles

#### Attention & Perception

1. **Selective Salience:** Use preattentive features (color, contrast, motion, size) sparingly for critical elements only; overuse overwhelms
2. **Visual Hierarchy:** Organize by importance using size, contrast, position, spacing; guide attention along F-pattern or Z-pattern
3. **Perceptual Grouping:** Use proximity (close = related), similarity (alike = grouped), continuity (aligned = connected), closure (mind fills gaps)
4. **Figure-Ground Distinction:** Ensure clear separation between foreground content and background

#### Memory & Cognition

5. **Working Memory Respect:** Limit concurrent elements to 4±1 chunks; group related items; show context rather than requiring memorization
6. **Recognition Over Recall:** Make options visible rather than requiring memory; show current state, breadcrumbs, available actions
7. **Chunking Strategy:** Group related information into meaningful units (phone: 555-123-4567; navigation: categories not flat list)
8. **Progressive Disclosure:** Reveal complexity gradually; show only what's immediately needed, provide details on demand

#### Encoding & Communication

9. **Encoding Hierarchy:** Use position/length for precise comparisons (bar charts), reserve angle/area/color for less critical distinctions
10. **Data-Ink Maximization:** Remove decorative elements that don't convey information; maximize proportion showing actual data
11. **Dual Coding:** Combine relevant visuals with text (two memory traces); use audio narration with complex visuals
12. **Spatial Contiguity:** Place labels/annotations adjacent to content they describe; prevent split-attention

#### Consistency & Standards

13. **Pattern Consistency:** Use predictable, familiar patterns (standard icons, conventional layouts, platform norms)
14. **Terminology Consistency:** Use same words for same concepts throughout
15. **Natural Mapping:** Align controls with effects intuitively (increase volume = move up; zoom in = pinch outward)

#### Feedback & Interaction

16. **Immediate Feedback:** Provide visible response to every action within milliseconds (loading states, confirmations, validation)
17. **Visible State:** Externalize system state to interface (show active filters, current page, progress); don't rely on user memory
18. **Error Prevention First:** Constrain inputs, disable invalid actions, provide guidance before errors; when errors occur, provide contextual recovery

#### Emotional & Behavioral

19. **Emotional Calibration:** Pleasant aesthetics improve problem-solving; frustration narrows attention and reduces working memory
20. **Behavioral Guidance:** Use visual emphasis, clear calls-to-action, ethical nudges to guide toward desired outcomes

---

### 3-Question Quick Check

**Use this for rapid validation:**

#### Question 1: Attention
**"Is it obvious what to look at first?"**
- [ ] Visual hierarchy is clear (primary vs secondary vs tertiary)
- [ ] Most important element is preattentively salient (but not overwhelming)
- [ ] Layout follows predictable scanning pattern (F or Z)

**If NO:** Increase size/contrast of primary elements, reduce visual weight of secondary items, establish clear entry point

---

#### Question 2: Memory
**"Is user required to remember anything that could be shown?"**
- [ ] Current state is visible (filters, progress, location)
- [ ] Options are presented, not requiring recall
- [ ] Concurrent elements fit in 4±1 chunks

**If NO:** Externalize state to interface, show don't tell, chunk information into groups

---

#### Question 3: Clarity
**"Can someone unfamiliar understand this in 5 seconds?"**
- [ ] Purpose/main message is immediately graspable
- [ ] No unnecessary decorative elements competing for attention
- [ ] Terminology is familiar or explained

**If NO:** Simplify, add labels/titles, remove extraneous elements, use annotations to guide interpretation

**If all three are YES → design is likely cognitively sound**

---

### Common Decision Rules

#### Chart Selection

**Task: Compare values**
→ **Use:** Bar chart (position/length encoding)
→ **Avoid:** Pie chart (angle/area less accurate)
→ **Why:** Cleveland & McGill hierarchy - position > angle

**Task: Show trend over time**
→ **Use:** Line chart with time on x-axis
→ **Avoid:** Stacked area (hard to compare non-bottom series)
→ **Why:** Continuous lines show temporal progression naturally

**Task: Show distribution**
→ **Use:** Histogram or box plot
→ **Avoid:** Multiple pie charts
→ **Why:** Enables shape perception (normal, skewed, bimodal)

**Task: Show part-to-whole**
→ **Use:** Stacked bar chart or treemap
→ **Avoid:** Pie chart with >5 slices
→ **Why:** Easier to compare bar lengths than angles

**Task: Find outliers**
→ **Use:** Scatterplot
→ **Avoid:** Table of numbers
→ **Why:** Visual pattern makes outliers pop out preattentively

---

#### Color Usage

**Categorical data (types, categories)**
→ **Use:** Distinct hues (red, blue, green - perceptually different)
→ **Avoid:** Shades of same hue
→ **Why:** Hue lacks inherent ordering; best for nominal categories

**Quantitative data (amounts, rankings)**
→ **Use:** Lightness/saturation gradient (light to dark)
→ **Avoid:** Rainbow spectrum or varied hues
→ **Why:** Lightness has natural perceptual ordering (more = darker)

**Alerts/errors**
→ **Use:** Red sparingly for threshold violations only
→ **Avoid:** Red for all negative values
→ **Why:** Overuse causes alert fatigue; preattentive salience needs restraint

**Accessible color**
→ **Use:** Redundant coding (color + icon/shape/text)
→ **Why:** 8% of males are colorblind; don't rely on color alone

---

#### Chunking Information

**Long lists (>7 items)**
→ **Action:** Group into 3-7 categories with visual separation
→ **Why:** Working memory limit; chunking fits capacity

**Multi-step processes**
→ **Action:** Break into 3-5 steps, show progress indicator
→ **Why:** Progressive disclosure reduces overwhelm, visible state reduces anxiety

**Form fields**
→ **Action:** 4-6 fields per screen; group related fields with proximity/backgrounds
→ **Why:** Fits working memory; Gestalt proximity shows relationships

**Navigation menus**
→ **Action:** 5-7 top-level categories max
→ **Why:** Decision time increases with choices (Hick's Law)

---

#### Error Handling

**Error message location**
→ **Action:** Next to problematic field, not top of page
→ **Why:** Gestalt proximity; spatial contiguity reduces cognitive load

**Error message language**
→ **Action:** Plain language ("Password must be 8+ characters") not error codes
→ **Why:** Reduces interpretation load, especially under stress

**Error prevention**
→ **Action:** Disable invalid actions, constrain inputs, validate inline
→ **Why:** Prevention > correction; immediate feedback enables learning

**Error recovery**
→ **Action:** Show what to fix, auto-focus to field, keep prior input visible
→ **Why:** Recognition over recall; reduce motor effort

---

#### Typography & Layout

**Heading hierarchy**
→ **Action:** Use size + weight to distinguish levels (H1 > H2 > H3 > body)
→ **Why:** Visual hierarchy guides scanning, shows structure

**Line length**
→ **Action:** 50-75 characters per line for body text
→ **Why:** Longer lines cause eye strain; shorter disrupt reading rhythm

**Whitespace**
→ **Action:** Use to separate unrelated groups, create breathing room
→ **Why:** Gestalt principle - separated = unrelated; crowding increases cognitive load

**Alignment**
→ **Action:** Left-align text in Western contexts; align related elements
→ **Why:** Gestalt continuity; consistent starting point aids scanning

---

### Design Heuristics at a Glance

#### Tufte's Principles
- **Maximize data-ink ratio:** Remove chart junk, keep only ink showing data
- **Graphical integrity:** Visual representation matches data proportionally
- **Small multiples:** Repeated structure enables comparison across conditions

#### Norman's Principles
- **Visibility:** State and options should be visible
- **Affordances:** Controls suggest their use (buttons look pressable)
- **Feedback:** Every action gets immediate, visible response
- **Mapping:** Controls arranged to match effects spatially
- **Constraints:** Prevent errors by limiting invalid actions

#### Gestalt Principles (Quick)
- **Proximity:** Close = related
- **Similarity:** Alike = grouped
- **Continuity:** Aligned = connected
- **Closure:** Mind completes incomplete figures
- **Figure-Ground:** Foreground vs background separation

#### Cognitive Load Principles
- **Intrinsic load:** Task complexity (can't change)
- **Extraneous load:** Bad design (MINIMIZE THIS)
- **Germane load:** Meaningful learning effort (support this)

#### Mayer's Multimedia Principles (Quick)
- **Multimedia:** Words + pictures > words alone
- **Modality:** Audio + visual > text + visual (splits load)
- **Contiguity:** Place text near corresponding graphic
- **Coherence:** Exclude extraneous content
- **Segmenting:** Break into user-paced chunks

---

### When to Use Which Framework

**Cognitive Design Pyramid**
→ **Use when:** Comprehensive quality check needed, evaluating all dimensions of design
→ **Tiers:** Perception → Coherence → Emotion → Behavior

**Design Feedback Loop**
→ **Use when:** Designing interactive interfaces, ensuring each screen answers user questions
→ **Stages:** Perceive → Interpret → Decide → Act → Learn

**Three-Layer Visualization Model**
→ **Use when:** Creating data visualizations, checking data quality through to interpretation
→ **Layers:** Data → Encoding → Interpretation

---

### 5-Second Tests

**Dashboard:** Can user identify current status within 5 seconds?

**Form:** Can user determine what information is needed within 5 seconds?

**Visualization:** Can user grasp main insight within 5 seconds?

**Infographic:** Can user recall key message after 5 seconds viewing?

**Interface:** Can user identify primary action within 5 seconds?

**If NO to any → simplify, strengthen hierarchy, add annotations**

---

### Common Rationales for Advocacy

**"Why bar chart instead of pie chart?"**
→ "Cleveland & McGill's research shows position/length encoding is 5-10x more accurate than angle/area for human perception. Bar charts enable precise comparisons; pie charts make them difficult."

**"Why simplify the interface?"**
→ "Working memory holds only 4±1 chunks. Current design exceeds this, causing cognitive overload. Chunking into groups fits human capacity and improves task completion."

**"Why inline validation?"**
→ "Immediate feedback enables learning through the perception-action loop. Delayed feedback breaks the cognitive connection between action and outcome."

**"Why not use red for all negative values?"**
→ "Preattentive salience depends on contrast. If everything is red, nothing stands out (alert fatigue). Reserve red for true threshold violations requiring immediate action."

**"Why accessible color schemes?"**
→ "8% of males have color vision deficiency. Redundant coding (color + icon + text) ensures all users can perceive information, not just those with typical vision."

---

## Return to Hub

**You've completed the Quick Reference path.**

**Options:**
1. Return to [Path Selection Menu](../SKILL.md#path-selection-menu) to choose another path
2. Exit if you have what you need

