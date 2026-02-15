# Cognitive Design Checklist

Systematic evaluation of designs across 8 cognitive dimensions. Each dimension has a WHY explanation, checklist items, test method, common failures, and fix priorities.

---

## 1. Visibility & Immediate Comprehension

### WHY This Matters

Core message/purpose must be graspable in ≤5 seconds. Information not seen is information not used. Above-the-fold placement and sufficient contrast are prerequisites for all other cognitive dimensions.

### Checklist

- [ ] Can users identify the purpose/main message within 5 seconds?
- [ ] Is important information visible without scrolling (above fold)?
- [ ] Is text/content legible? (sufficient size, contrast, line length)
- [ ] Are interactive elements distinguishable from static content?

### Test Method

**5-second test:** Show design for 5 seconds, ask what they remember. **Pass:** Correctly identify purpose. **Fail:** Remember decoration or miss point.

### Common Failures

Cluttered layout, poor contrast, content buried below fold, interactive elements indistinguishable from text.

### Fix Priorities

CRITICAL (contrast/legibility), HIGH (5-second clarity), MEDIUM (fold placement)

---

## 2. Visual Hierarchy

### WHY This Matters

Users must distinguish primary vs secondary vs tertiary content instantly. Without clear hierarchy, everything competes for attention equally, causing cognitive overload and missed priorities.

### Checklist

- [ ] Is visual hierarchy clear? (size, contrast, position differentiate importance)
- [ ] Do headings/labels form clear levels? (H1 > H2 > H3 > body)
- [ ] Does design pass "squint test"? (important elements visible when blurred)
- [ ] Are calls-to-action visually prominent?

### Test Method

**Squint test:** Blur design (squint or screenshot blur). **Pass:** Important elements visible. **Fail:** Everything same weight.

### Common Failures

Everything same size, primary CTA not distinguished, decoration more prominent than data.

### Fix Priorities

HIGH (primary not prominent), MEDIUM (heading hierarchy), LOW (minor adjustments)

---

## 3. Chunking & Organization

### WHY This Matters

Working memory holds 4±1 chunks (Cowan 2001). Information must be grouped into meaningful units to fit cognitive capacity. Ungrouped lists >7 items overwhelm processing.

### Checklist

- [ ] Are long lists broken into categories? (≤7 items per unbroken list)
- [ ] Are related items visually grouped? (proximity, backgrounds, whitespace)
- [ ] Is navigation organized into logical categories? (≤7 top-level items)
- [ ] Are form fields grouped by relationship? (personal info, account, preferences)

### Test Method

**Count test:** Count ungrouped items in any section. **Pass:** ≤7 items or clear grouping. **Fail:** >7 items ungrouped.

### Common Failures

15+ flat navigation items, 30-field ungrouped forms, 20 equal-weight metrics in dashboards.

### Fix Priorities

CRITICAL (>10 ungrouped), HIGH (7-10 ungrouped), MEDIUM (clearer group boundaries)

---

## 4. Simplicity & Clarity

### WHY This Matters

Every visual element consumes attentional resources. Decorative elements compete with data for attention. Tufte's data-ink ratio: maximize ink showing data, minimize non-data ink.

### Checklist

- [ ] Can you justify every visual element? (conveys information or improves usability?)
- [ ] Is data-ink ratio high? (maximize data, minimize decoration)
- [ ] Are decorative elements eliminated? (chartjunk, unnecessary lines, ornaments)
- [ ] Is terminology familiar or explained? (no unexplained jargon)

### Test Method

**Purpose test:** Point to each element, ask "What purpose?" **Pass:** Every element justified. **Fail:** Decorative/unclear elements.

### Common Failures

Chartjunk (3D effects, heavy gridlines, gradients), unexplained jargon, redundant information.

### Fix Priorities

HIGH (decoration competing with data), MEDIUM (unexplained terms), LOW (minor simplification)

---

## 5. Memory Support

### WHY This Matters

Recognition is easier than recall (Nielsen). Users should never need to remember what could be shown. Current state, navigation context, and available options should be visible.

### Checklist

- [ ] Is current system state visible? (active filters, current page, progress)
- [ ] Are navigation breadcrumbs provided? (where am I, how did I get here)
- [ ] For multi-step processes, is progress shown? (step X of Y)
- [ ] Are options presented rather than requiring recall? (dropdowns vs typed commands)

### Test Method

**Memory test:** Identify what users must remember. Ask "Could this be shown?" **Pass:** State visible. **Fail:** Relying on memory.

### Common Failures

No active filter indication, no progress indicator, hidden state, commands requiring memorization.

### Fix Priorities

CRITICAL (lost in flow), HIGH (critical state invisible), MEDIUM (minor memory aids)

---

## 6. Feedback & Interaction

### WHY This Matters

Every action needs immediate, clear feedback (Norman). Without feedback within 100ms, users don't know if their action registered, leading to repeated actions and confusion.

### Checklist

- [ ] Do all interactive elements provide immediate feedback? (hover states, click feedback)
- [ ] Are loading states shown? (spinners/progress for waits >1 second)
- [ ] Do form fields validate inline? (immediate feedback, not after submit)
- [ ] Are error messages contextual? (next to problem, not top of page)
- [ ] Are success confirmations shown? ("Saved", checkmarks)

### Test Method

**Interaction test:** Click/interact with each element. **Pass:** Feedback within 100ms. **Fail:** No feedback or delayed >1s without indicator.

### Common Failures

No hover states, no loading indicator, errors not contextual, no success confirmation.

### Fix Priorities

CRITICAL (no feedback for critical actions), HIGH (delayed without loading), MEDIUM (missing hover)

---

## 7. Consistency

### WHY This Matters

Consistency enables prediction — users learn patterns and apply them throughout. Inconsistency breaks mental models and forces relearning, increasing cognitive load.

### Checklist

- [ ] Is terminology consistent? (same words for same concepts throughout)
- [ ] Are UI patterns consistent? (buttons, links, inputs styled uniformly)
- [ ] Is color usage consistent? (red = error, green = success throughout)
- [ ] Are interaction patterns predictable? (click/tap behavior consistent)

### Test Method

**Pattern test:** List similar elements, check consistency. **Pass:** Identical styling/behavior. **Fail:** Unjustified variations.

### Common Failures

"Email" vs "E-mail" inconsistency, button styles varying across pages, red meaning both error and negative trend.

### Fix Priorities

HIGH (terminology), MEDIUM (visual styling), LOW (minor patterns)

---

## 8. Scanning Patterns

### WHY This Matters

Eye tracking research shows predictable F-pattern (text-heavy) and Z-pattern (visual-heavy) scanning. Critical content placed off these paths will be missed.

### Checklist

- [ ] Is primary content positioned top-left? (where scanning starts)
- [ ] For text-heavy content, does layout follow F-pattern?
- [ ] For visual-heavy content, does layout follow Z-pattern?
- [ ] Are terminal actions positioned bottom-right? (where scanning ends)

### Test Method

**Trace test:** Trace expected eye movement (F/Z pattern). **Pass:** Critical elements on path. **Fail:** Important content off path.

### Common Failures

Primary CTA bottom-left (off Z-pattern), key info middle-right (off F-pattern).

### Fix Priorities

MEDIUM (CTA off path), LOW (secondary optimization)

---

## Scoring Summary

**Process:**
1. Check each dimension's items
2. Mark each dimension: ✓ (pass), ⚠️ (partial), ❌ (fail)
3. Classify failed dimensions by severity
4. Prioritize fixes: CRITICAL → HIGH → MEDIUM → LOW

**Pass criteria:** No CRITICAL failures, no more than 2 HIGH failures, average score ≥3.5 if using 1-5 scoring per dimension.
