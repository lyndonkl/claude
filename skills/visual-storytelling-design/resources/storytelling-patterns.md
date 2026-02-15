# Storytelling Patterns

Templates, pattern library, and decision tools for structuring data stories.

---

## Section 1: Story Templates

### WHY This Matters

Templates provide proven structures that reduce planning time and ensure narrative completeness. Like scaffolding — provides structure without constraining the content.

### WHAT to Apply

#### Template 1: Step-by-Step Arc

**Best for:** Explaining a process, showing cause-effect, building to a conclusion.

```
1. Hook: Surprising fact or human story (1 sentence)
2. Context: What's the background? (2-3 sentences + overview visual)
3. Build: Show the data step by step (2-4 chart sections)
4. Climax: The key insight (1 annotated chart + callout)
5. Resolution: What it means + what's next (1-2 sentences)
```

**Example:** "How a small town's water quality declined over 20 years" — hook with health impact, show decade trends, highlight inflection point, end with policy recommendation.

#### Template 2: Magazine Feature

**Best for:** Long-form data journalism, in-depth exploration.

```
1. Hero image/chart: Full-width visual capturing the story
2. Lead paragraph: Context + why this matters
3. Section blocks: Alternating text + charts (3-5 sections)
4. Pull quotes: Key statistics styled prominently
5. Conclusion: Summary insight + forward-looking statement
```

#### Template 3: Annotated Chart Story

**Best for:** Single dataset with rich narrative layered on top.

```
1. Clean chart: The visualization without annotation
2. Layer 1: Add main insight annotation (callout box)
3. Layer 2: Add context annotations (shaded regions, event markers)
4. Layer 3: Add detail annotations (specific data point labels)
```

**Key principle:** Annotations guide the reader through the chart like a tour guide.

#### Template 4: Interactive Exploration

**Best for:** Audience-driven discovery, dashboards with narrative.

```
1. Guided intro: Default view shows main insight
2. Exploration controls: Filters, selections, toggles
3. Contextual tooltips: Explain what user is seeing
4. Bookmarks: Pre-set views for key findings
5. Summary panel: Dynamic text updating with selections
```

#### Template 5: Presentation Deck

**Best for:** Live presentations, stakeholder meetings.

```
Slide 1: Title + one-sentence thesis
Slide 2: Context (why this matters now)
Slides 3-6: Evidence (one chart per slide, one point per chart)
Slide 7: Synthesis (combined view or summary)
Slide 8: Implications + call to action
```

**Rule:** One message per slide. If a slide needs two charts, split it.

---

## Section 2: Pattern Library

### WHY This Matters

Recurring data story types have established visual patterns. Using the right pattern matches audience expectations and leverages familiar structures.

### WHAT to Apply

#### Before/After Pattern

**Use when:** Showing change, impact of intervention, transformation.

```
Layout: Side-by-side or overlaid with clear labels
Visual: Same chart type, same scale, different time/condition
Annotation: Highlight the delta (difference)
```

**Critical:** Must use identical scales and chart types for honest comparison.

#### Timeline Pattern

**Use when:** Chronological narrative, historical context, evolution.

```
Layout: Horizontal timeline with event markers
Visual: Line chart or area chart with annotated events
Annotation: Key events labeled on the timeline
```

**Best practice:** Limit to 5-7 key events. Too many events create clutter.

#### Geographic Pattern

**Use when:** Spatial distribution, regional comparison, location-based stories.

```
Layout: Map as primary visual
Visual: Choropleth, bubble map, or dot density
Annotation: Regional labels, callouts for outliers
```

**Caution:** Maps emphasize area, not value. Large-area regions dominate visually even if small in value. Consider cartograms or small multiples.

#### Rankings Pattern

**Use when:** Comparing entities, showing hierarchy, highlighting top/bottom performers.

```
Layout: Horizontal bar chart sorted by value
Visual: Bars with direct value labels
Annotation: Highlight subject of interest, add benchmark line
```

**Why horizontal:** Labels readable without rotation, natural comparison along position axis.

#### Part-to-Whole Pattern

**Use when:** Showing composition, proportions, budget allocation.

```
Layout: Stacked bar, treemap, or waffle chart
Visual: Color-coded segments with direct labels
Annotation: Highlight the segment being discussed
```

**Avoid:** Pie charts with >6 slices. Use treemap or stacked bar instead.

#### Deviation Pattern

**Use when:** Showing variance from baseline, above/below average, positive/negative.

```
Layout: Diverging bar chart or connected dot plot
Visual: Color-coded positive/negative from center line
Annotation: Label the baseline, explain what deviation means
```

---

## Section 3: Choosing the Right Pattern

### WHY This Matters

Pattern choice determines how easily readers grasp the message. Wrong pattern forces readers to work harder than necessary to extract insights.

### WHAT to Apply

#### Decision Matrix

```
Your message is about...          → Use this pattern
─────────────────────────────────────────────────────
Change over time                  → Timeline
Before vs after intervention      → Before/After
How something is divided          → Part-to-Whole
Which is biggest/smallest         → Rankings
Where things are located          → Geographic
How something deviates from norm  → Deviation
A process or journey              → Step-by-Step Arc
Multiple findings to present      → Magazine Feature
A single rich dataset             → Annotated Chart
Audience explores on their own    → Interactive Exploration
Live presentation                 → Presentation Deck
```

#### Pattern Combinations

Complex stories often combine patterns:

```
Common combinations:
- Timeline + Geographic: How a trend spread across regions
- Rankings + Before/After: Who improved most
- Part-to-Whole + Timeline: How composition changed over time
- Deviation + Rankings: Who deviates most from baseline
```

**Rule:** Maximum 2 combined patterns per story section. More creates cognitive overload.

---

## Section 4: Quality Checklist

### WHY This Matters

A final check ensures the story works as intended. Like proofreading — catches issues before publication.

### WHAT to Apply

```
Story Quality Checklist:
- [ ] 1. Can reader state the main insight in one sentence?
- [ ] 2. Does the opening hook create interest?
- [ ] 3. Is context sufficient for the target audience?
- [ ] 4. Does each chart have a clear point (not just data display)?
- [ ] 5. Are annotations guiding interpretation?
- [ ] 6. Is the narrative arc complete (beginning → middle → end)?
- [ ] 7. Are transitions between sections smooth?
- [ ] 8. Is the story self-contained (no external knowledge required)?
- [ ] 9. Does the conclusion deliver on the promise of the opening?
- [ ] 10. Would this pass a fallacy/integrity audit?
```

**Scoring:** 8-10 checks = Ready. 5-7 = Needs revision. <5 = Major rework.
