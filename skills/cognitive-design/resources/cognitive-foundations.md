# Cognitive Foundations

This resource explains the core cognitive psychology principles underlying effective visual design.

**Foundation for:** All other paths in this skill

---

## Why Learn Cognitive Foundations

### WHY This Matters

Understanding how humans perceive, attend, remember, and process information enables you to:
- **Predict user behavior:** Know what users will notice, understand, and remember
- **Design with confidence:** Ground decisions in research, not guesswork
- **Diagnose problems:** Identify why designs fail cognitively
- **Advocate effectively:** Explain design rationale with scientific backing

**Mental model:** Like a doctor needs anatomy to diagnose illness, designers need cognitive psychology to diagnose interface problems.

**Research foundation:** Tufte (data visualization), Norman (interaction design), Ware (visual perception), Cleveland & McGill (graphical perception), Miller/Cowan (working memory), Gestalt psychology (perceptual grouping), Mayer (multimedia learning).

Without cognitive foundations: design by intuition alone, inconsistent decisions, inability to explain why designs work or fail.

---

## What You'll Learn

### Core Cognitive Concepts

This section covers 5 foundational areas:
1. **Perception & Attention** - What users notice first, visual search, preattentive processing
2. **Memory & Cognition** - Working memory limits, chunking, cognitive load
3. **Gestalt & Grouping** - Automatic perceptual organization patterns
4. **Visual Encoding** - Hierarchy of perceptual accuracy for different chart types
5. **Mental Models & Mapping** - How prior experience shapes expectations

---

## Why Perception & Attention

### WHY This Matters

**Core insight:** Attention is limited and selective like a spotlight - you can only focus on one thing at high resolution while periphery remains blurry.

**Implications:**
- Visual design controls where attention goes
- Competing elements dilute attention
- Critical information must be made salient
- Users scan, they don't read everything thoroughly

**Mental model:** Human vision is like a camera with a tiny high-resolution center (fovea covers ~1-2° of visual field) and low-resolution periphery. We rapidly move attention spotlight to important areas.

---

### WHAT to Know

#### Preattentive Processing

**Definition:** Detection of basic visual features in under 500ms before conscious attention.

**Preattentive Features:**
- **Color:** A single red item among gray pops out instantly
- **Form:** Unique shapes stand out (circle among squares)
- **Motion:** Moving elements grab attention automatically
- **Position:** Spatial outliers noticed quickly
- **Size:** Largest/smallest items detected fast

**Application Rule:**
```
Use preattentive features sparingly for 1-3 critical elements only.
Too many salient elements = visual noise = nothing stands out.
```

**Example:** Dashboard alert in red among gray metrics → immediate attention

**Anti-pattern:** Everything in bright colors → overwhelm, nothing prioritized

---

#### Visual Search

**Definition:** After preattentive pop-out, users engage in serial visual search - scanning one area at a time with high acuity.

**Predictable Patterns:**
- **F-pattern:** Text-heavy content (read top-left to top-right, then down left side, short horizontal scan middle)
- **Z-pattern:** Visual-heavy content (top-left to top-right, diagonal to bottom-left, then bottom-right)
- **Gutenberg Diagram:** Primary optical area top-left, terminal area bottom-right

**Application Rule:**
```
Position most important elements along scanning path:
- Top-left for primary content (both patterns start here)
- Top-right for secondary actions
- Bottom-right for terminal actions (next/submit)
```

**Example:** Dashboard KPIs top-left, details below, "Export" button bottom-right

---

#### Attention Spotlight Trade-offs

**Attention is zero-sum:** Effort spent on decorations is unavailable for data comprehension.

**Rule:** Maximize attention on task-relevant elements, minimize on decorative elements.

**Squint Test:** Blur design (squint or Gaussian blur) - can you still identify what's important? If hierarchy disappears when blurred, it's too subtle.

---

## Why Memory & Cognition

### WHY This Matters

**Core insight:** Working memory can hold only ~4±1 meaningful chunks of information, and items fade within seconds unless rehearsed.

**Implications:**
- Interfaces must be designed to fit memory limits
- Information must be chunked into groups
- State should be externalized to interface, not user's memory
- Recognition is vastly easier than recall

**Mental model:** Working memory is like juggling - you can keep 3-5 balls in the air, but adding more causes you to drop them all.

**Updated understanding:** Miller (1956) proposed 7±2 chunks, but Cowan (2001) showed actual capacity is 4±1 for most people.

---

### WHAT to Know

#### Working Memory Capacity

**Definition:** "Mental scratchpad" holding active information temporarily (seconds) before transfer to long-term memory or loss.

**Capacity:** **4±1 chunks** for most people

**Chunk:** Meaningful unit of information
- Expert: "555-123-4567" = 1 chunk (phone number)
- Novice: "555-123-4567" = 10 chunks (each digit separate)

**Application Rule:**
```
Design within 4±1 constraint:
- Navigation: ≤7 top-level categories
- Forms: 4-6 fields per screen without wizard
- Dashboards: Group metrics into 3-5 categories
- Choices: Limit concurrent options to ≤7
```

**Example:** Registration wizard with 4 steps (personal info, account, preferences, review) vs single 30-field page

**Why it works:** Each step fits in working memory; progress indicator externalizes "where am I"

---

#### Cognitive Load Types

**Intrinsic Load:** Inherent complexity of the task itself (can't change)

**Extraneous Load:** Mental effort from poor design - confusing interfaces, unclear icons, missing context
→ **MINIMIZE THIS**

**Germane Load:** Meaningful mental effort contributing to learning or understanding
→ **Support this, don't eliminate**

**Application Rule:**
```
Reduce extraneous load to free capacity for germane load:
- Remove decorative elements (chartjunk)
- Simplify workflows (fewer steps, fewer choices)
- Provide memory aids (breadcrumbs, visible state, tooltips)
- Use familiar patterns (standard UI conventions)
```

**Example:** E-learning slide with audio narration + diagram (germane load) vs text + diagram + background music (extraneous load from competing visual text and irrelevant music)

---

#### Recognition vs. Recall

**Recall:** Retrieve from memory without cues (hard, error-prone, slow)
- "What was the error code?"
- "Which menu has the export function?"

**Recognition:** Identify among presented options (easy, fast, accurate)
- Error message shown in context
- Menu items visible

**Application Rule:**
```
Design for recognition over recall:
- Show available options (dropdown) vs requiring typed command
- Display current filters as visible chips vs requiring memory
- Provide breadcrumbs vs expecting user to remember navigation path
- Use icons WITH labels vs icons alone
```

**Example:** File menu with visible "Save" option vs command-line requiring user to remember "save" command

---

#### Chunking Strategy

**Definition:** Grouping related information into single meaningful units to overcome working memory limits.

**Application Patterns:**
- **Lists:** Break into categories (❌ 20 ungrouped nav items → ✓ 5 categories × 4 items)
- **Forms:** Group fields (❌ 30 sequential fields → ✓ 4-step wizard with grouped fields)
- **Phone numbers:** Use conventional chunking (555-123-4567 = 3 chunks vs 5551234567 = 10 chunks)
- **Dashboards:** Group metrics by category (Traffic panel, Conversion panel, Error panel)

---

## Why Gestalt & Grouping

### WHY This Matters

**Core insight:** The brain automatically organizes visual elements based on proximity, similarity, continuity, and other principles - this happens preconsciously before you think about it.

**Implications:**
- Layout directly creates perceived meaning
- Whitespace is not "empty" - it shows separation
- Consistent styling shows relationships
- Alignment implies connection

**Mental model:** Gestalt principles are like visual grammar - rules the brain applies automatically to make sense of what it sees.

**Historical note:** Gestalt psychology (1910s-1920s) discovered these principles, and they remain validated by modern neuroscience.

---

### WHAT to Know

#### Proximity

**Principle:** Items close together are perceived as belonging to the same group.

**Application Rule:**
```
Use spatial grouping to show relationships:
- Related form fields adjacent with minimal spacing
- Unrelated groups separated by whitespace
- Label next to corresponding graphic (not across page)
```

**Example:** Dashboard with 3 panels (traffic, conversions, errors) separated by whitespace → automatically perceived as 3 distinct groups

**Anti-pattern:** Even spacing everywhere → no perceived structure

---

#### Similarity

**Principle:** Elements that look similar (shape, color, size, style) are seen as related or part of a pattern.

**Application Rule:**
```
Use consistent styling for related elements:
- All primary CTAs same color/style
- All error messages same red + icon treatment
- All headings same font/size per level
```

**Example:** All "delete" actions red across interface → users learn "red = destructive action"

**Anti-pattern:** Inconsistent button styles → users can't predict function from appearance

---

#### Continuity

**Principle:** Elements arranged on a line or curve are perceived as more related than elements not aligned.

**Application Rule:**
```
Use alignment to show structure:
- Left-align related items (form fields, list items)
- Grid layouts imply equal status
- Flowing lines guide eye through narrative
```

**Example:** Infographic with visual flow from top to bottom, numbered steps along continuous path

**Anti-pattern:** Haphazard placement → no clear reading order

---

#### Closure

**Principle:** Mind perceives complete figures even when parts are missing, filling gaps mentally.

**Application Rule:**
```
Leverage closure for simplified designs:
- Dotted lines imply connection without solid line visual weight
- Incomplete circles/shapes still recognized (reduce ink)
- Implied boundaries via alignment without explicit borders
```

**Example:** Dashboard cards separated by whitespace only (no borders) → still perceived as distinct containers

---

#### Figure-Ground Segregation

**Principle:** We instinctively separate scene into "figure" (foreground object of focus) and "ground" (background).

**Application Rule:**
```
Ensure clear figure-ground distinction:
- Modal dialogs: dim background, brighten foreground
- Highlighted content: stronger contrast than surroundings
- Active state: clearly differentiated from inactive
```

**Example:** Popup form with darkened background overlay → form is clearly the figure

**Anti-pattern:** Insufficient contrast → users can't distinguish what's active

---

## Why Visual Encoding Hierarchy

### WHY This Matters

**Core insight:** Not all visual encodings are equally effective for human perception - some enable precise comparisons, others make them nearly impossible.

**Cleveland & McGill's Hierarchy (most to least accurate):**
1. Position along common scale (bar chart)
2. Position along non-aligned scales
3. Length
4. Angle/slope
5. Area
6. Volume
7. Color hue (categorical only)
8. Color saturation

**Implications:**
- Chart type choice directly determines user accuracy
- Bar charts enable 5-10x more precise comparison than pie charts
- Color hue has no inherent ordering (don't use for quantities)

**Mental model:** Human visual system is like a measurement tool - some encodings are precision instruments (position), others are crude estimates (area).

---

### WHAT to Know

#### Task-Encoding Matching

**Match encoding to user task:**
- **Compare values:** Bar chart (position/length 5-10x more accurate than pie angle/area)
- **See trend:** Line chart (continuous line shows temporal progression, slope changes visible)
- **Understand distribution:** Histogram/box plot (shape visible, outliers apparent)
- **Part-to-whole:** Stacked bar/treemap (avoid pie >5 slices - angles hard to judge)
- **Find outliers/clusters:** Scatterplot (2D position enables pattern detection)

---

#### Color Encoding Rules

- **Categorical:** Distinct hues (red, blue, green). Limit 5-7 categories. Hue lacks ordering.
- **Quantitative:** Lightness gradient (light→dark). Avoid rainbow (misleading peaks). Darkness = more.
- **Diverging:** Two-hue gradient through neutral (blue←gray→orange). Shows direction/magnitude.
- **Accessible:** Redundant coding (color + icon + label). 8% males colorblind.

---

#### Perceptually Uniform Colormaps

**Problem:** Rainbow spectrum has non-uniform perceptual steps - equal data differences don't produce equal perceived color differences. Can hide or exaggerate patterns.

**Solution:** Use perceptually uniform colormaps:
- **Viridis** (yellow→green→blue)
- **Magma** (purple→red→yellow)
- **Plasma** (purple→orange→yellow)

**Why:** Equal data steps = equal perceived color steps = honest representation

**Application:** Any heatmap, choropleth map, or continuous quantitative color scale

---

## Why Mental Models & Mapping

### WHY This Matters

**Core insight:** Users approach interfaces with preconceived notions (mental models) from past experiences. Designs that violate these models require re-learning and cause confusion.

**Implications:**
- Familiarity reduces cognitive load (System 1 processing)
- Deviation from standards forces conscious thought (System 2 processing)
- Consistent patterns become automatic
- Natural mappings feel intuitive

**Mental model:** Like driving a car - once you've learned, you don't consciously think about pedals. New car with reversed pedals would be dangerous because it violates your mental model.

---

### WHAT to Know

#### Mental Models (User Expectations)

**Definition:** Internal representations of how things work based on prior experience and analogy.

**Sources:**
- **Platform conventions:** iOS vs Android interaction patterns
- **Cultural patterns:** Left-to-right reading in Western contexts
- **Physical world:** Skeuomorphic metaphors (trash can for delete)
- **Other applications:** "Most apps work this way" (Jakob's Law)

**Application Rule:**
```
Use standard UI patterns to leverage existing mental models:
- Hamburger menu for navigation (mobile)
- Magnifying glass for search
- Shopping cart for e-commerce
- Standard keyboard shortcuts (Ctrl+C/V)
```

**When to deviate:** Only when standard pattern demonstrably fails for your use case AND you provide clear onboarding

**Example:** File system trash can - users understand "throw away to delete" from physical world metaphor

---

#### Affordances & Signifiers

**Affordance:** Properties suggesting how to interact (button affords clicking, slider affords dragging)

**Signifier:** Visual cues indicating affordance (button looks raised/has shadow to signal "press me")

**Application Rule:**
```
Design controls to signal their function:
- Buttons: raised appearance, hover state, cursor change
- Text inputs: rectangular field with border, cursor appears on click
- Sliders: handle that looks draggable
- Links: underlined or colored text, cursor changes to pointer
```

**Example:** Flat button vs raised button - raised appearance signals "I'm interactive" without user experimentation

**Anti-pattern:** Everything looks flat and identical → user must experiment to discover what's clickable

---

#### Natural Mapping

**Definition:** Relationship between controls and effects that mirrors spatial/conceptual relationships in intuitive way.

**Application Patterns:**
- **Spatial:** Stove knob layout mirrors burner layout (front-left knob → front-left burner)
- **Directional:** Volume up = move up, zoom in = pinch outward, scroll down = swipe up (matches physical)
- **Conceptual:** Green = go/good/success, Red = stop/bad/error (culturally learned, widely understood)

**Rule:** Align control layout/direction with effect for instant comprehension

---

## Application: Putting Foundations Together

### Dashboard Design Example

**Problem:** 20 equal-weight metrics → cognitive overload

**Applied Principles:**
- **Attention:** 3-4 primary KPIs top-left (large), smaller secondary below, red for violations only
- **Memory:** Group into 3-4 panels (Traffic, Conversions, Errors) = fits 4±1 chunks
- **Gestalt:** Proximity (related metrics within panel), similarity (consistent colors), whitespace (panel separation)
- **Encoding:** Bar charts (comparisons), line charts (trends), avoid pies (poor angle perception)
- **Mental Models:** Standard chart types, conventional axes (time left-to-right), familiar icons + labels

**Result:** 5-second comprehension vs 60-second confusion

---

### Form Wizard Example

**Problem:** 30-field form → 60% abandonment

**Applied Principles:**
- **Attention:** 4 steps revealed gradually, current step prominent
- **Memory:** 4-6 fields per step (fits 4±1 capacity), progress indicator visible (externalizes state)
- **Gestalt:** Related fields grouped (name, address), whitespace between groups
- **Recognition over Recall:** Show step names ("Personal Info" → "Account" → "Preferences" → "Review"), display entered info in review, enable back navigation
- **Natural Mapping:** Linear flow left-to-right/top-to-bottom, "Next" button bottom-right consistently

**Result:** 75% completion, faster task time
