# Narrative Techniques

Cognitive design principles for data journalism, presentations, infographics, and visual storytelling.

---

## Section 1: Why Storytelling Needs Cognitive Design

### WHY This Matters

People naturally seek stories with cause-effect and chronology. Structuring data as narrative aids comprehension and retention.

**How cognitive principles help:**
- **Narrative structure:** Context → Problem → Resolution chunks information meaningfully
- **Annotations:** Guide attention to key insights, prevent misinterpretation
- **Self-contained graphics:** Include all context (recognition over recall)
- **Progressive disclosure:** Scrollytelling reveals complexity gradually

**Mental model:** Data journalism is a guided tour, not a data dump — designer leads readers to insights while allowing exploration.

---

## Section 2: Narrative Structure

### WHY This Matters

Human brains are wired for stories. Story arc provides natural chunking (beginning/middle/end), improves retention, and engages emotions.

### WHAT to Apply

#### Classic Narrative Arc for Data

**Structure:** Context → Problem/Question → Data/Evidence → Resolution/Insight

**Context (Set the stage):**
- Title that frames the story: "How Climate Change is Affecting Crop Yields"
- Subtitle/intro: Brief background (2-3 sentences)
- Visual: Overall trend or map showing scope

**Problem/Question (Establish stakes):**
- Specific question posed: "Will traditional farming regions remain viable?"
- Visual highlighting the problem area
- Human impact stated (not just abstract data)

**Data/Evidence (Show the findings):**
- Clear visualizations (chart type matched to message)
- Annotations highlighting key patterns
- Comparisons (before/after, with/without intervention)

**Resolution/Insight (Deliver the takeaway):**
- Main insight clearly stated
- Implications for future
- Call-to-action or next question (optional)

#### Opening Strategies

**Lead with human impact:**
```
❌ "Agricultural productivity data shows regional variations"
✓ "Sarah Miller's family has farmed Iowa corn for 4 generations.
   Now her yields are declining while her neighbor 200 miles north is thriving."
```

**Lead with surprising finding:**
```
❌ "Unemployment rates changed over time"
✓ "Despite recession fears, unemployment in Tech Hub cities fell 15%
   while national rates rose"
```

**Lead with visual:** Strong opening image/chart that encapsulates story, followed by "This is the story of..." text.

---

## Section 3: Annotation Strategies

### WHY This Matters

Readers scan rather than study. Without guidance, they may miss key insights or misinterpret data. Annotations are like a tour guide pointing out important sights.

### WHAT to Apply

#### Annotation Types

**Callout boxes:** Highlight main insight. Position near relevant data, contrasting background. 1-2 sentences max, larger font.

**Arrows and leader lines:** Connect explanation to specific data element. Simple arrows, not decorative.

**Shaded regions:** Mark time periods or ranges of interest. Subtle shading (10-20% opacity), doesn't obscure data.

**Direct labels on data:** Label lines/bars directly instead of separate legend. Eliminates cross-referencing.

**Contextual annotations:** Explain anomalies, methodology notes, definitions.

#### Annotation Guidelines

**What to annotate:**
- ✓ Main insight (what should reader take away?)
- ✓ Unexpected patterns (outliers, inflection points)
- ✓ Important events (policy changes, launches, crises)
- ✓ Comparisons (how does this compare to baseline?)
- ✓ Methodological notes (data sources, limitations)
- ❌ Don't annotate obvious patterns
- ❌ Don't over-annotate (too many = visual noise)

**Placement:** Near data being explained (Gestalt proximity). Outside chart area if possible. Consistent positioning.

---

## Section 4: Scrollytelling

### WHY This Matters

Complex data stories benefit from progressive revelation. Scrollytelling maintains context while building understanding step-by-step. Like flipping through graphic novel panels — each scroll reveals next part while maintaining continuity.

### WHAT to Apply

#### Basic Pattern

1. Sticky chart (stays visible as user scrolls)
2. Text sections (scroll past, trigger chart updates)
3. Smooth transitions (not jarring jumps)
4. User control (can scroll back up to review)

#### Example Implementation

**Section 1 (scroll 0%):** Full trend line 2010-2024. Text: "Overall growth shows steady increase." User sees big picture.

**Section 2 (scroll 33%):** Highlight 2015-2018 in color, rest faded. Text: "First phase: Rapid growth following policy change."

**Section 3 (scroll 66%):** Highlight 2020 dip in red. Text: "COVID-19 caused temporary decline."

**Section 4 (scroll 100%):** Full color restored, add dotted projection. Text: "Projected recovery to pre-2020 trend by 2026."

#### Best Practices

**Transitions:** Smooth animations (300-500ms). Maintain reference points (axes don't jump). One change at a time.

**User control:** Can scroll back. Trigger based on position not speed. "Skip to end" option. Pause/play for auto-animations.

**Accessibility:** Content accessible without scrolling (fallback). Keyboard navigation. Works without JavaScript (progressive enhancement).

---

## Section 5: Framing & Context

### WHY This Matters

Same data can support different conclusions based on framing (Tversky & Kahneman). Ethical journalism provides complete context for accurate interpretation.

### WHAT to Apply

#### Provide Baselines & Comparisons

Always include:
- ✓ Historical comparison (how does this compare to past?)
- ✓ Peer comparison (vs similar entities?)
- ✓ Benchmark (what's the standard/goal?)
- ✓ Absolute + relative (numbers + percentages both shown)

```
❌ "Unemployment rises to 5.2%"
✓ "Unemployment rises to 5.2% from 4.8% last quarter (historical average: 5.5%)"
```

#### Avoid Cherry-Picking

```
❌ Show only favorable time period
✓ Show full relevant period + note any focus area
```

#### Clarify Denominator

```
❌ "50% increase!" (50% of what?)
✓ "Increased from 10 to 15 users (50% increase)"
```

#### Note Limitations

- ✓ Data source stated
- ✓ Sample size noted
- ✓ Margin of error provided
- ✓ Missing data acknowledged
- ✓ Selection criteria clarified

---

## Section 6: Visual Metaphors

### WHY This Matters

Familiar metaphors leverage existing knowledge to explain new concepts. But only if the metaphor resonates with the audience and accurately represents the concept.

### WHAT to Apply

**Effective metaphors:**
- ✓ Virus spread as fire spreading across map (leverages fire = spread schema)
- ✓ Data flow as river (volume, direction, obstacles)
- ✓ Economic inequality as wealth distribution pyramid

**Problematic metaphors:**
- ❌ Complex process as simple machine (oversimplifies)
- ❌ Culture-specific metaphors for international audience
- ❌ Metaphors contradicting data

**Test your metaphor:**
1. Does it help understanding or just decorate?
2. Is it universally recognized by target audience?
3. Does it accurately represent the concept?
4. Does it oversimplify in misleading ways?
5. Could it be misinterpreted?

If any answer is problematic → reconsider.

**Clarify limitations:** Note where analogy breaks down to prevent overgeneralization.
