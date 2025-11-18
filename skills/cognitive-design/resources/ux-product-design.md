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
- New users abandon apps because learning curve too steep
- Task flows have too many steps or choices (Hick's Law impact)
- Complex features overwhelm users (cognitive overload)
- Error messages confusing or missed
- Onboarding shows all features at once (memory overload)

**How cognitive principles help:**
- Leverage existing mental models (Jakob's Law - users expect standard patterns)
- Minimize steps and choices (Hick's Law, Fitts's Law optimization)
- Progressive disclosure (reveal complexity gradually)
- Inline validation with contextual feedback
- Onboarding focused on 3-4 key tasks (working memory limit)

**Mental model:** Interface is a conversation - user asks (through interaction), interface answers (through feedback), understanding evolves through learning loop.

---

## What You'll Learn

**Five key areas:**

1. **Learnability:** How to leverage familiar patterns for instant comprehension
2. **Task Flow Efficiency:** Minimizing steps and optimizing control placement
3. **Cognitive Load Management:** Progressive disclosure and memory aids
4. **Onboarding:** Teaching without overwhelming
5. **Error Handling:** Prevention first, then contextual recovery

---

## Why Learnability Matters

### WHY This Matters

**Core insight:** Users spend most of their time on OTHER sites/apps (Jakob's Law) - they expect interfaces to work like what they already know.

**Mental models from experience:**
- Platform conventions (iOS vs Android interaction patterns)
- Web standards (hamburger menu, magnifying glass = search)
- Cultural patterns (left-to-right reading in Western contexts)
- Physical metaphors (trash can = delete, folder = container)

**Benefits of familiar patterns:**
- Instant recognition (System 1 processing, no conscious thought)
- Lower cognitive load (no need to learn new patterns)
- Faster task completion (muscle memory applies)
- Reduced errors (behavior matches expectations)

**Cost of deviation:**
- Extraneous cognitive load (learning new pattern)
- User frustration (violates expectations)
- Increased support burden (need to explain)

**Mental model:** Standard patterns are like a shared language - everyone understands, no translation needed.

---

### WHAT to Apply

#### Standard UI Patterns

**Navigation:**
```
✓ Hamburger menu (☰) for mobile navigation
✓ Magnifying glass (🔍) for search
✓ Logo top-left returns to home (web convention)
✓ User avatar/name top-right for account menu
✓ Breadcrumbs for hierarchical navigation
```

**Actions:**
```
✓ Primary action: Right-aligned button (Z-pattern terminus)
✓ Destructive actions: Red color, require confirmation
✓ Secondary actions: Gray or outlined buttons
✓ Disabled state: Grayed out, cursor shows "not-allowed"
```

**Forms:**
```
✓ Labels above or left of fields (clear association)
✓ Required fields: Asterisk (*) or "Required" label
✓ Validation: Inline as user types/on blur
✓ Submit button: Bottom-right (flow terminus)
```

**Feedback:**
```
✓ Loading: Spinner or progress bar for waits >1 second
✓ Success: Green checkmark + "Saved" message
✓ Error: Red color + exclamation icon + message
✓ Confirmation: Modal dialog for destructive actions ("Are you sure?")
```

**Application rule:**
```
Default: Use standard pattern
Deviate only when: Standard demonstrably fails for your use case
If deviating: Provide clear onboarding/tooltips explaining new pattern
Test: Can users figure it out without help? If not, revert to standard
```

---

#### Affordances & Signifiers

**Principle:** Controls should signal their function through appearance

**Buttons:**
```
✓ Raised appearance or shadow (looks pressable)
✓ Hover state changes (cursor becomes pointer, button highlights)
✓ Active state (button depresses when clicked)
✓ Focus state for keyboard navigation (visible outline)
```

**Links:**
```
✓ Underlined or distinct color from body text
✓ Cursor changes to pointer on hover
✓ Visited state (purple or dimmed) - though less common now
```

**Input fields:**
```
✓ Rectangular border distinguishes from surrounding content
✓ Cursor appears when clicked (blinking insertion point)
✓ Placeholder text shows expected format
✓ Focus state (border highlights when active)
```

**Draggable elements:**
```
✓ Handle icon (≡≡) suggests grabbability
✓ Cursor changes to grab hand on hover
✓ Element shadows on drag (appears lifted)
```

**Anti-patterns:**
```
❌ Flat design with no visual cues (everything looks like text)
❌ No hover states (unclear what's interactive)
❌ Buttons that look like labels
❌ Clickable areas smaller than visual target (Fitts's Law violation)
```

---

#### Platform Conventions

**iOS:**
```
- Back button: Top-left
- Navigation: Bottom tab bar
- Swipe gestures: Right-to-left = forward, left-to-right = back
- Sharing: Box with up arrow icon
```

**Android:**
```
- Back button: System navigation (bottom or gesture)
- Navigation: Often hamburger menu top-left
- Three-dot menu: Top-right overflow menu
- Floating action button (FAB): Bottom-right primary action
```

**Web:**
```
- Logo: Top-left, links to home
- Primary navigation: Top horizontal bar
- Search: Top-right
- Footer: Contact, legal, social links
```

**Application rule:**
```
Match platform norms for your primary platform
If cross-platform: Adapt to each platform's conventions (don't force iOS patterns on Android)
Don't invent new patterns when standard ones exist
```

---

## Why Task Flow Efficiency Matters

### WHY This Matters

**Core insight:** Every decision point and step adds time and cognitive effort (Hick's Law, Fitts's Law).

**Hick's Law:** Decision time increases logarithmically with number of choices
- 2 choices: Fast decision
- 10 choices: Significantly slower, paralysis possible

**Fitts's Law:** Time to target = function of distance ÷ size
- Large, nearby targets: Fast
- Small, distant targets: Slow, error-prone

**Implication:** Streamline common tasks, optimize frequent control placement

---

### WHAT to Apply

#### Reduce Steps

**Audit method:**
```
1. Map current task flow (list every step/decision)
2. Question each step: "Is this necessary? Can we automate? Can we merge with another step?"
3. Eliminate unnecessary steps
4. Combine related steps
5. Pre-fill known information
```

**Example: Checkout flow optimization**
```
Before (8 steps):
1. Click "Checkout"
2. Enter email
3. Create password
4. Enter shipping address
5. Choose shipping method
6. Enter payment info
7. Review order
8. Click "Place order"

After (4 steps):
1. Click "Checkout" (email + shipping pre-filled from account)
2. Confirm shipping, choose method
3. Enter payment (or use saved card)
4. Click "Place order" (review shown inline, not separate step)

Reduction: 50% fewer steps, higher completion rate
```

---

#### Reduce Choices (Hick's Law)

**Application patterns:**

**Progressive disclosure:**
```
Instead of: 20 filter options visible at once
Better: Show 5 most common filters, "More filters" reveals rest
Why: Reduces initial cognitive load, keeps advanced users happy
```

**Smart defaults:**
```
Instead of: User chooses from 10 shipping options
Better: Highlight recommended option based on delivery needs, show "Other options" link
Why: Most users want good default, power users can explore
```

**Contextual menus:**
```
Instead of: All 50 actions available always
Better: Show 5-7 actions relevant to current mode/selection
Why: Reduces noise, Hick's Law impact minimized
```

**Application rule:**
```
Common tasks: ≤5 clear options
Advanced features: Behind "More" or "Advanced" progressive disclosure
Personalization: Learn from usage, surface frequently-used actions
```

---

#### Optimize Control Placement (Fitts's Law)

**Principle:** Frequent actions should be large and nearby, infrequent actions can be smaller and distant

**Application patterns:**

**Primary actions:**
```
Size: Large button (min 44×44px touch target on mobile, 32×32px desktop)
Position: Bottom-right (Z-pattern terminus) or along natural flow
Example: "Submit" button large, prominent green
```

**Secondary actions:**
```
Size: Medium button
Position: Near primary but visually distinct (outlined, gray)
Example: "Save draft" button outlined gray, next to green "Submit"
```

**Tertiary/destructive actions:**
```
Size: Can be smaller (but still tappable)
Position: Separated from frequent actions (prevent accidental clicks)
Example: "Delete" link in footer, red, requires confirmation
```

**Example: Email app**
```
Primary (large, prominent): "Reply" button (most frequent action)
Secondary (medium): "Forward", "Archive" (less frequent)
Tertiary (small, distant): "Delete", "Mark as spam" (infrequent, destructive)

Fitts's Law benefit: Reply is fastest to target, Delete requires more intentional movement (prevents accidents)
```

---

## Why Cognitive Load Management Matters

### WHY This Matters

**Core insight:** Working memory holds only 4±1 chunks - interfaces exceeding this capacity cause confusion and abandonment.

**Types of cognitive load:**
- **Intrinsic:** Task complexity (can't change)
- **Extraneous:** Poor design (MINIMIZE THIS)
- **Germane:** Meaningful learning (support this)

**Goal:** Reduce extraneous load to free capacity for task completion

---

### WHAT to Apply

#### Progressive Disclosure

**Principle:** Reveal complexity gradually, show only what's immediately needed

**Application patterns:**

**Wizard/multi-step forms:**
```
Instead of: 30 fields on one page
Better: 4 steps × 6-8 fields each
Why: Each step fits working memory, progress visible

Step 1: Personal info (name, email, phone)
Step 2: Account setup (username, password)
Step 3: Preferences (notifications, privacy)
Step 4: Review & submit

Benefits: Higher completion, fewer errors, less overwhelm
```

**Expandable sections:**
```
Instead of: All settings visible always
Better: Sections collapsed by default, expand on demand

Settings page:
▸ Account settings
▸ Privacy settings
▸ Notification settings
▼ Appearance settings (expanded, shows options)

User sees: Only what they need, can explore more
```

**"Advanced" options:**
```
Instead of: Mix basic and advanced options together
Better: Basic options visible, "Show advanced options" link reveals rest

Example: File upload
Basic: File selection, upload button
Advanced (hidden): Compression settings, metadata, batch options

Most users: Get simple interface
Power users: Can access advanced features
```

---

#### Chunking & Grouping

**Principle:** Group related items, separate with whitespace

**Application patterns:**

**Form field grouping:**
```
Personal Information (proximity group, subtle background)
- First name
- Last name
- Email

Shipping Address (proximity group)
- Street address
- City, State, ZIP

Chunk count: 2 (fits working memory)
```

**Navigation grouping:**
```
Instead of: 25 flat menu items
Better: 5-7 categories × 3-5 items each

Example:
▾ File (New, Open, Save, Close)
▾ Edit (Undo, Redo, Cut, Copy, Paste)
▾ View (Zoom, Layout, Panels)
▾ Tools (Preferences, Plugins)
▾ Help (Documentation, Support)

5 top-level chunks, each with manageable sub-items
```

---

#### Memory Aids (Recognition over Recall)

**Principle:** Show options, don't require memorization

**Application patterns:**

**Visible state:**
```
✓ Active filters shown as removable chips
✓ Current page highlighted in navigation
✓ Breadcrumbs show navigation path
✓ Progress indicators for multi-step processes

❌ Hidden state requiring user to remember
```

**Autocomplete & suggestions:**
```
✓ Search suggestions as user types
✓ Address autocomplete from previous entries
✓ Date picker (select from calendar) vs typing format
✓ Dropdown menus vs remembering command names
```

**Recent history:**
```
✓ "Recently opened" files list
✓ Search history dropdown
✓ "Previously purchased" product suggestions
✓ Form fields remember previous entries (with user control)
```

---

## Why Onboarding Matters

### WHY This Matters

**Core insight:** First-time experience determines whether users continue or abandon - onboarding must teach key tasks without overwhelming.

**Common failures:**
- Showing all features upfront (memory overload)
- Passive tutorials (low engagement, poor retention)
- No contextual help for later features

**Successful patterns:**
- Focus on 3-4 core tasks only (working memory limit)
- Interactive tutorials (active learning)
- Contextual help when feature encountered

---

### WHAT to Apply

#### Focus on Core Tasks

**Principle:** Limit onboarding to 3-4 most important tasks, not comprehensive feature tour

**Application rule:**
```
Ask: "What must users learn to get value?"
Not: "What are all our features?"

Example: Project management app
Core tasks for onboarding:
1. Create a project
2. Add a task
3. Assign to team member
4. Mark task complete

Skip in onboarding: Advanced filtering, custom fields, integrations, reporting
(Teach these via contextual help when encountered)
```

---

#### Interactive Learning

**Principle:** Users learn by doing, not by reading

**Application patterns:**

**Guided interaction:**
```
Instead of: "Click + button to add task" (passive instruction)
Better: Highlight + button, require actual click to proceed

Tooltip appears: "Try clicking the + button to create your first task"
User clicks: Task creation form appears
Tutorial: "Great! Now enter a task name"
User types: Active learning, muscle memory forming
```

**Progressive task completion:**
```
Step 1: "Create your first project" ← Active task, user must complete
Step 2: "Add a team member" ← Unlocked after Step 1
Step 3: "Create your first task" ← Unlocked after Step 2

Benefits: Sense of accomplishment, can't skip ahead (ensures learning), voluntary exits available
```

---

#### Contextual Help (Not Upfront)

**Principle:** Advanced features taught when user encounters them, not in initial onboarding

**Application patterns:**

**Tooltips on first encounter:**
```
User navigates to Reports page (first time)
→ Tooltip appears: "Reports let you track progress. Try filtering by team member."
→ Dismiss or interact
→ Tooltip doesn't appear again (one-time help)
```

**Empty states as teaching moments:**
```
User opens Tasks page with no tasks yet
→ Instead of blank page: "No tasks yet! Click + to create your first task"
→ Illustrative graphic showing what tasks look like
→ Clear call-to-action
```

**Gradual feature discovery:**
```
After 1 week: "Did you know you can set due dates? Try clicking the calendar icon"
After 1 month: "Power tip: Use keyboard shortcuts to work faster. Press ? to see shortcuts"

Timing: Based on usage, not dumped upfront
```

---

## Why Error Handling Matters

### WHY This Matters

**Core insight:** Users will make errors (slips and mistakes) - good design prevents errors and provides clear recovery when they occur.

**Error types:**
- **Slips:** Unintended actions (typos, wrong button)
- **Mistakes:** Wrong plan (misunderstanding how it works)

**Goal:** Prevention > detection > recovery

---

### WHAT to Apply

#### Prevention (Best)

**Constrain inputs:**
```
✓ Date picker instead of free text (prevents format errors)
✓ Numeric keyboard for phone numbers on mobile
✓ Input masking (phone: (___) ___-____)
✓ Disable invalid actions (grayed out submit until form valid)
```

**Provide defaults:**
```
✓ Pre-select most common option
✓ Suggest formats ("e.g., john@example.com")
✓ Autocomplete from previous entries
```

**Confirmation for destructive actions:**
```
✓ Delete: Require confirmation modal
✓ Irreversible actions: "Type DELETE to confirm"
✓ Undo available when possible (better than confirmation)
```

---

#### Detection (Inline Validation)

**Principle:** Immediate feedback as user types or on blur, not after submit

**Application patterns:**

**Real-time validation:**
```
Password field:
As user types: Show strength meter + requirements
- ✓ At least 8 characters
- ✓ Contains number
- ❌ Contains special character ← Still needed

Email field:
On blur (when user leaves field): Validate format
If invalid: Red border, message appears below field
If valid: Green checkmark
```

**Positioning:**
```
✓ Error message NEXT TO field (Gestalt proximity)
❌ Error at top of page (requires user to hunt for problem)

Example:
Email: [____________] ← Red border
       ❌ Please enter valid email address ← Message immediately below
```

---

#### Recovery (Clear Guidance)

**Principle:** Tell users what's wrong and how to fix it, in plain language

**Message structure:**
```
❌ "Error 402"
✓ "Password must be at least 8 characters"

❌ "Invalid input"
✓ "Email address must include @ symbol (e.g., john@example.com)"

❌ "Submission failed"
✓ "Card was declined. Please check card number or try a different payment method"
```

**Visual emphasis:**
```
✓ Red color + icon (preattentive salience + dual coding)
✓ Auto-focus to error field (reduce motor effort to fix)
✓ Keep user's input visible (don't clear field - they can edit)
✓ Change to green checkmark when fixed (positive feedback)
```

---

## Return to Hub

**You've completed the UX & Product Design path.**

**Options:**
1. Return to [Path Selection Menu](../skill.md#path-selection-menu) to explore other paths
2. Exit if you have what you need

**Recommended next paths:**
- **Path 1 (Cognitive Foundations)** for deeper understanding of mental models
- **Path 2 (Frameworks)** to apply Design Feedback Loop to your interfaces
- **Path 6 (Quick Reference)** for condensed UX heuristics

