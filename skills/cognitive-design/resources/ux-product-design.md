# UX & Product Design

This resource provides cognitive design principles for interactive software interfaces (web apps, mobile apps, desktop software).

**Covered topics:**
1. Learnability through familiar patterns
2. Task flow efficiency
3. Cognitive load management
4. Onboarding design
5. Error handling and prevention

---

## Why UX Needs Cognitive Design

### WHY This Matters

**Core insight:** Users approach interfaces with mental models from prior experiences - designs that violate expectations require re-learning and cause cognitive friction.

**Common problems:**
- New users abandon apps (steep learning curve)
- Task flows with too many steps/choices (Hick's Law impact)
- Complex features overwhelm users (cognitive overload)
- Confusing error messages
- Onboarding shows all features at once (memory overload)

**How cognitive principles help:** Leverage existing mental models (Jakob's Law), minimize steps/choices (Hick's/Fitts's Law), progressive disclosure, inline validation, onboarding focused on 3-4 key tasks (working memory limit).

---

## What You'll Learn

1. **Learnability:** Leverage familiar patterns for instant comprehension
2. **Task Flow Efficiency:** Minimize steps and optimize control placement
3. **Cognitive Load Management:** Progressive disclosure and memory aids
4. **Onboarding:** Teaching without overwhelming
5. **Error Handling:** Prevention first, then contextual recovery

---

## Why Learnability Matters

### WHY This Matters

Users spend most time on OTHER sites/apps (Jakob's Law) - they expect interfaces to work like what they already know.

**Benefits of familiar patterns:** Instant recognition (System 1), lower cognitive load, faster completion, reduced errors.

---

### WHAT to Apply

#### Standard UI Patterns

**Navigation:**
- Hamburger menu (☰) for mobile
- Magnifying glass (🔍) for search
- Logo top-left returns home
- User avatar top-right for account
- Breadcrumbs for hierarchy

**Actions:**
- Primary: Right-aligned button
- Destructive: Red, requires confirmation
- Secondary: Gray/outlined
- Disabled: Grayed out

**Forms:**
- Labels above/left of fields
- Required fields: Asterisk (*)
- Validation: Inline as user types
- Submit: Bottom-right

**Feedback:**
- Loading: Spinner for waits >1s
- Success: Green checkmark + message
- Error: Red + icon + message
- Confirmation: Modal for destructive actions

**Application rule:** Use standard patterns by default. Deviate only when standard fails AND provide onboarding. Test if users understand without help.

---

#### Affordances & Signifiers

Controls should signal function through appearance:

**Buttons:** Raised appearance, hover state, active state, focus state
**Links:** Underlined or distinct color, pointer cursor on hover
**Inputs:** Rectangular border, cursor on click, placeholder text, focus state
**Draggable:** Handle icon (≡≡), grab cursor, shadow on drag

**Anti-patterns:** Flat design with no cues, no hover states, buttons looking like labels, clickable areas smaller than visual target.

---

#### Platform Conventions

**iOS:** Back top-left, navigation bottom tabs, swipe gestures, share icon with up arrow
**Android:** System back button, hamburger menu top-left, three-dot overflow, FAB bottom-right
**Web:** Logo top-left to home, primary nav top horizontal, search top-right, footer links

**Rule:** Match platform norms. If cross-platform, adapt to each. Don't invent when standards exist.

---

## Why Task Flow Efficiency Matters

### WHY This Matters

Every decision point and step adds time and cognitive effort.

**Hick's Law:** Decision time increases logarithmically with choices (2 choices = fast, 10 = slow/paralysis)
**Fitts's Law:** Time to target = distance ÷ size (large/nearby = fast, small/distant = slow)

---

### WHAT to Apply

#### Reduce Steps

**Audit method:**
1. Map current flow
2. Question each step: "Necessary? Can automate? Can merge?"
3. Eliminate unnecessary
4. Combine related
5. Pre-fill known info

**Example:** Checkout flow reduced from 8 steps to 4 (pre-fill email/shipping, combine review inline) = 50% fewer steps, higher completion.

---

#### Reduce Choices (Hick's Law)

**Progressive disclosure:** Show 5 most common filters, "More filters" reveals rest
**Smart defaults:** Highlight recommended option, show "Other options" link
**Contextual menus:** 5-7 actions relevant to current mode, not all 50

**Rule:** Common tasks ≤5 options. Advanced features behind "More". Personalize based on usage.

---

#### Optimize Control Placement (Fitts's Law)

Frequent actions = large and nearby. Infrequent = smaller and distant.

**Primary:** Large button (44×44px mobile, 32×32px desktop), bottom-right or natural flow
**Secondary:** Medium, near primary but distinct (outlined, gray)
**Tertiary/destructive:** Smaller, separated, requires confirmation

---

## Why Cognitive Load Management Matters

### WHY This Matters

Working memory holds 4±1 chunks - exceeding this causes confusion/abandonment.

**Load types:** Intrinsic (task complexity), Extraneous (poor design - MINIMIZE), Germane (meaningful learning - support)

---

### WHAT to Apply

#### Progressive Disclosure

Reveal complexity gradually, show only immediate needs.

**Wizards:** 4 steps × 6-8 fields (not 30 fields on one page) = fits working memory, visible progress
**Expandable sections:** Collapsed by default, expand on demand
**"Advanced" options:** Basic visible, "Show advanced" link reveals rest

---

#### Chunking & Grouping

Group related items, separate with whitespace.

**Forms:** Group by relationship (Personal Info, Shipping Address) = 2 chunks
**Navigation:** 5-7 categories × 3-5 items each (not 25 flat items)

---

#### Memory Aids (Recognition over Recall)

Show options, don't require memorization.

**Visible state:** Active filters as chips, current page highlighted, breadcrumbs, progress indicators
**Autocomplete:** Search suggestions, address autocomplete, date picker
**Recent history:** Recently opened files, search history, previous purchases

---

## Why Onboarding Matters

### WHY This Matters

First experience determines continuation/abandonment. Must teach key tasks without overwhelming.

**Failures:** All features upfront, passive tutorials, no contextual help
**Success:** 3-4 core tasks, interactive tutorials, contextual help when encountered

---

### WHAT to Apply

#### Focus on Core Tasks

Limit to 3-4 most important tasks, not comprehensive tour.

**Ask:** "What must users learn to get value?" NOT "What are all features?"

**Example:** Project management app - onboard on: create project, add task, assign to member, mark complete. Skip advanced filtering/custom fields/reporting (teach contextually later).

---

#### Interactive Learning

Users learn by doing, not reading.

**Guided interaction:** Highlight button, require click to proceed (active learning, muscle memory)
**Progressive completion:** Step 1 must complete before Step 2 unlocks = sense of accomplishment, ensures learning

---

#### Contextual Help

Advanced features taught when encountered, not upfront.

**First encounter tooltips:** One-time help when user navigates to new feature
**Empty states:** "No tasks yet! Click + to create first task" with illustrative graphic
**Gradual discovery:** After 1 week show tip, after 1 month show power tip (usage-based timing)

---

## Why Error Handling Matters

### WHY This Matters

Users make errors (slips/mistakes) - good design prevents and provides clear recovery.

**Goal:** Prevention > detection > recovery

---

### WHAT to Apply

#### Prevention (Best)

**Constrain inputs:** Date picker (not free text), numeric keyboard for phone, input masking
**Provide defaults:** Pre-select common option, suggest formats
**Confirm destructive:** Require confirmation modal, "Type DELETE to confirm", undo when possible

---

#### Detection (Inline Validation)

Immediate feedback as user types/on blur, not after submit.

**Real-time validation:** Password strength meter as typing, email format on blur
**Positioning:** Error NEXT TO field (not top of page) - Gestalt proximity

---

#### Recovery (Clear Guidance)

Tell what's wrong and how to fix, in plain language.

**Bad:** "Error 402"
**Good:** "Password must be at least 8 characters"

**Visual:** Red + icon, auto-focus to error field, keep user input (don't clear), green checkmark when fixed
