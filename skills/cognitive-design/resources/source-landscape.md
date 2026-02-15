# Source Landscape

This resource maps the key researchers, publications, and theoretical traditions that inform cognitive design principles.

**Purpose:** Provide intellectual context and citation backing for design recommendations.

---

## Why Know the Sources

### WHY This Matters

**Core insight:** Cognitive design principles aren't arbitrary rules — they emerge from decades of empirical research across perception, cognition, HCI, and information visualization.

**Benefits of source awareness:**
- **Credibility:** Ground recommendations in published research
- **Depth:** Understand WHY principles work, not just WHAT to do
- **Judgment:** Apply principles flexibly when contexts differ
- **Communication:** Cite authoritative sources when advocating for design decisions

---

## WHAT to Reference

### Foundational Authors and Works

#### Edward Tufte — Visual Information Design
**Key works:** The Visual Display of Quantitative Information (1983), Envisioning Information (1990), Visual Explanations (1997)

**Core contributions:**
- **Data-ink ratio:** Maximize proportion of ink showing data, minimize non-data ink
- **Chartjunk:** Named and cataloged gratuitous visual decoration that obscures data
- **Small multiples:** Repeating chart structure for comparison across categories
- **Sparklines:** Word-sized graphics embedded in text for inline data context
- **Graphical integrity:** Visual representation proportional to numerical quantities

**When to cite:** Arguing for simplicity, removing decoration, defending minimalist design choices

---

#### Don Norman — Human-Centered Design
**Key works:** The Design of Everyday Things (1988), Emotional Design (2004)

**Core contributions:**
- **Affordances:** Visual properties suggesting how objects can be used
- **Signifiers:** Indicators showing where action should take place
- **Mapping:** Relationship between controls and their effects (natural vs arbitrary)
- **Feedback:** Immediate system response to user actions
- **Conceptual models:** User's understanding of how system works
- **Gulf of execution/evaluation:** Gap between user intent and system state

**When to cite:** Designing interactive interfaces, explaining usability principles, justifying feedback mechanisms

---

#### Colin Ware — Information Visualization
**Key works:** Information Visualization: Perception for Design (2004, 4th ed 2021), Visual Thinking for Design (2008)

**Core contributions:**
- **Preattentive processing:** Visual features detected in <200ms without conscious search (color, orientation, size, motion)
- **Visual channels:** Properties that can encode data (position, length, angle, area, color hue/saturation/lightness)
- **Attention mechanisms:** Bottom-up (stimulus-driven) vs top-down (goal-driven) attention
- **Visual working memory:** Limited to ~4 items simultaneously
- **Gestalt principles:** Applied to information display grouping

**When to cite:** Choosing visual encodings, designing for preattentive pop-out, managing visual complexity

---

#### Cleveland & McGill — Graphical Perception
**Key work:** Graphical Perception: Theory, Experimentation, and Application to the Development of Graphical Methods (1984)

**Core contributions:**
- **Visual encoding accuracy hierarchy:** Position (common scale) > Position (non-aligned) > Length > Angle > Area > Volume > Color saturation > Color hue
- **Empirical ranking:** Based on experiments measuring accuracy of human judgment
- **Task-encoding alignment:** Match data comparison task to most accurate encoding

**When to cite:** Choosing chart types, justifying bar charts over pie charts, defending position-based encodings

---

#### Gestalt Psychologists — Perceptual Grouping
**Key figures:** Max Wertheimer, Kurt Koffka, Wolfgang Köhler (1920s-1940s)

**Core contributions:**
- **Proximity:** Elements close together perceived as group
- **Similarity:** Elements sharing properties (color, shape, size) perceived as group
- **Continuity:** Elements aligned on curve/line perceived as related
- **Closure:** Mind completes incomplete shapes
- **Figure-ground:** Automatic separation of foreground from background
- **Common fate:** Elements moving together perceived as group

**When to cite:** Explaining layout decisions, justifying grouping strategies, defending whitespace usage

---

#### George Miller — Working Memory
**Key work:** The Magical Number Seven, Plus or Minus Two (1956)

**Core contributions:**
- **Chunking:** Grouping information into meaningful units
- **Working memory capacity:** ~7±2 items (later revised to 4±1 by Cowan 2001)
- **Implications for design:** Limit ungrouped items, use categories, progressive disclosure

**When to cite:** Justifying chunking decisions, limiting navigation items, grouping form fields

---

#### Richard Mayer — Multimedia Learning
**Key work:** Multimedia Learning (2001, 3rd ed 2021)

**Core contributions:**
- **Multimedia principle:** People learn better from words + pictures than words alone
- **Contiguity principle:** Place related text and images near each other (spatial) and present simultaneously (temporal)
- **Coherence principle:** Remove extraneous material
- **Signaling principle:** Highlight essential material
- **Redundancy principle:** Don't present identical text and narration simultaneously
- **Segmenting principle:** Break complex lessons into manageable parts
- **Pre-training principle:** Teach key concepts before the main lesson

**When to cite:** Designing educational content, justifying layout proximity, removing decorative elements

---

#### Jakob Nielsen — Usability Heuristics
**Key work:** 10 Usability Heuristics for User Interface Design (1994)

**Core contributions:**
- **Visibility of system status:** Keep users informed
- **Match between system and real world:** Use familiar language
- **User control and freedom:** Support undo and redo
- **Consistency and standards:** Follow conventions
- **Error prevention:** Design to prevent errors before they happen
- **Recognition rather than recall:** Show options, don't require memory
- **Flexibility and efficiency:** Support both novice and expert users
- **Aesthetic and minimalist design:** Remove irrelevant information
- **Help users recognize, recover from errors:** Clear error messages
- **Help and documentation:** Available when needed

**When to cite:** Evaluating interfaces, justifying design heuristics, conducting expert reviews

---

### Emerging Research

#### Accessibility and Inclusive Design
- WCAG guidelines for color contrast, screen readers, keyboard navigation
- Colorblind-safe palette design (Viridis, Cividis)
- Universal design principles

#### Dark Patterns and Ethical Design
- Deceptive design patterns catalog (Brignull)
- Ethical visualization principles
- Informed consent in data presentation

#### Cognitive Load Theory (Sweller)
- Intrinsic load (inherent complexity)
- Extraneous load (poor design)
- Germane load (productive learning)
- Design should minimize extraneous, manage intrinsic, maximize germane

#### Dual Process Theory (Kahneman)
- System 1: Fast, automatic, intuitive
- System 2: Slow, deliberate, analytical
- Design implications: Leverage System 1 for scanning, support System 2 for analysis

---

## Quick Citation Guide

| Principle | Cite |
|---|---|
| Remove decoration | Tufte — data-ink ratio |
| Use position encoding | Cleveland & McGill — encoding hierarchy |
| Group related items | Gestalt — proximity/similarity |
| Limit to 4-7 items | Miller/Cowan — working memory |
| Show don't require recall | Nielsen — recognition over recall |
| Text near images | Mayer — contiguity principle |
| Provide feedback | Norman — feedback/affordances |
| Preattentive pop-out | Ware — preattentive processing |
| Minimize cognitive load | Sweller — cognitive load theory |
| Support fast scanning | Kahneman — System 1/System 2 |
