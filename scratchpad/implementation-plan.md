# Writer Skill Implementation Plan

## Executive Summary

We're converting the Writing Mentor & Message Architect prompt into a comprehensive, interactive skill that guides users through professional writing processes. The skill will be modular, workflow-based, and deeply resourced with reference materials, examples, and analysis scripts.

---

## Skill Architecture

### Core Structure
```
skills/writer/
├── skills.md                    # Main skill definition & router
├── workflows/                   # 7 workflow definitions
├── layers/                      # 7 core layer references
├── toolkits/                    # 5 specialized toolkits
├── scripts/                     # 4-6 analysis scripts
├── examples/                    # Before/after examples
└── docs/                        # Supporting documentation
```

### Interaction Model

**Phase 1: Intent Discovery**
```
User invokes skill → Skill asks: "What do you want to do?"
↓
User selects workflow (or skill recommends based on context)
↓
Skill loads relevant workflow definition
```

**Phase 2: Workflow Execution**
```
For each step in workflow:
  1. Present step description
  2. Pull in relevant reference content
  3. Ask guiding questions
  4. Offer to run relevant scripts
  5. Collect user's work
  6. Validate before proceeding
```

**Phase 3: Output Generation**
```
Generate deliverables using templates
Save artifacts to user-specified location
Provide next steps
```

---

## Implementation Phases

### Phase 1: Foundation (MVP)
**Goal**: Core skill with essential workflows functioning

#### Files to Create:
1. **skills.md** (main skill)
   - Purpose and when to use
   - Workflow router
   - Basic instructions
   - Prerequisites

2. **workflows/full-writing-process.md**
   - Complete 7-layer walkthrough
   - Step-by-step checklist
   - Reference file calls

3. **workflows/revision-and-polish.md**
   - Most commonly used workflow
   - Layers 4-5 focused

4. **layers/04-revision-engine.md**
   - Four-pass system
   - Detailed techniques
   - Examples

5. **layers/05-messaging-stickiness.md**
   - Complete SUCCESs framework
   - Questions and checklist
   - Examples

6. **scripts/analyze-text.py**
   - Word count, sentence count
   - Average sentence length
   - Reading level
   - Basic statistics

7. **scripts/detect-clutter.py**
   - Adverb detection
   - Qualifier detection
   - Passive voice detection
   - Weak verb detection

#### Success Criteria:
- User can invoke skill
- Revision workflow works end-to-end
- Scripts run and provide useful output
- Reference content is helpful

---

### Phase 2: Expansion
**Goal**: Add remaining workflows and reference materials

#### Files to Create:
8. **workflows/intent-and-structure.md**
   - Layers 1-2 focused
   - Planning before drafting

9. **workflows/drafting-session.md**
   - Layer 3 focused
   - First draft creation

10. **workflows/toolkit-application.md**
    - Quick application of specific toolkit
    - Menu of toolkits

11. **layers/01-intent-discovery.md**
    - Core promise formulation
    - Audience analysis
    - Commander's intent

12. **layers/02-structural-architecture.md**
    - McPhee's diagrams
    - Structure types
    - Visual examples

13. **layers/03-drafting-discipline.md**
    - Lamott, King, Klinkenborg synthesis
    - Exercises and techniques

14. **toolkits/sentence-toolkit-klinkenborg.md**
    - Sentence-level work
    - One thought per sentence
    - Examples

15. **toolkits/reader-cognition-toolkit-pinker.md**
    - Garden path avoidance
    - Cognitive load reduction
    - Topic chains

#### Success Criteria:
- All major workflows functional
- Core layers fully documented
- Essential toolkits available

---

### Phase 3: Polish
**Goal**: Complete all materials, add examples, refine experience

#### Files to Create:
16. **toolkits/clarity-toolkit-zinsser.md**
17. **toolkits/newsroom-toolkit-clark.md**
18. **toolkits/stickiness-toolkit-heath.md**
19. **layers/06-socratic-coaching.md**
20. **layers/07-output-templates.md**
21. **examples/full-process-example.md**
22. **examples/revision-example.md**
23. **docs/writing-principles.md**
24. **docs/quick-reference-checklist.md**
25. **scripts/sentence-variety.py**
26. **scripts/success-checker.py**

#### Success Criteria:
- All reference files complete
- Rich examples for every technique
- All scripts functional
- Documentation comprehensive

---

## Detailed File Specifications

### skills.md (Main Skill Definition)

**Purpose**: Entry point and router for the skill

**Structure**:
```markdown
# Writing Mentor Skill

## Purpose
Transform your writing into precise, compelling, unforgettable prose

## When to Use
- Writing something new from scratch
- Revising and polishing a draft
- Stuck on structure or organization
- Want to make your message stickier
- Need to apply specific writing techniques

## When NOT to Use
- Quick grammar checks (use editing tools)
- Formatting/style guide compliance
- Citation management

## Prerequisites
- Draft or idea to work with (for most workflows)
- Text editor or document
- Time to iterate (writing is rewriting)

## How It Works

### Step 1: Choose Your Workflow
[Interactive menu or questions to route]

### Step 2: Follow the Process
[Workflow-specific guidance]

### Step 3: Generate Deliverables
[Templates and outputs]

## Available Workflows

1. **Full Writing Process** - Start to finish for new pieces
2. **Intent & Structure Planning** - Blueprint before drafting
3. **Drafting Session** - Get words on paper
4. **Revision & Polish** - Refine existing draft
5. **Toolkit Application** - Apply specific technique
6. **Stickiness Check** - Make it memorable
7. **Structure Consultation** - Solve organization problems

## Core Principles
[8 core beliefs from original prompt]

## Philosophy
[Brief overview of the approach]

## Workflow Router

[Logic for determining which workflow to recommend based on user's situation]

## Example Outputs
[What you'll get from this skill]
```

**Implementation Notes**:
- Use AskUserQuestion to route workflows
- Present clear options with descriptions
- Allow experienced users to jump directly
- Provide examples upfront

---

### Workflow File Template

Each workflow file follows this structure:

```markdown
# [Workflow Name]

## Use Case
[When to use this workflow]

## Duration
[Expected time commitment]

## Prerequisites
[What you need before starting]

## Deliverables
[What you'll produce]

## Process

### Phase 1: [Name]
**Objective**: [What we're accomplishing]

**Steps**:
1. [Step 1]
   - Guiding questions: [...]
   - Reference: [link to layers/xyz.md section]
   - Optional script: [script name]

2. [Step 2]
   - Guiding questions: [...]
   - Reference: [link to toolkits/xyz.md section]

**Checkpoint**: [How to verify phase complete]

### Phase 2: [Name]
[Same structure]

## Final Output
[Template for deliverables]

## Next Steps
[What to do after this workflow]

## Troubleshooting
[Common issues and solutions]
```

---

### Layer Reference File Template

Each layer file follows this structure:

```markdown
# Layer X: [Name]

## Philosophy
[Why this layer matters - 2-3 paragraphs]

## When to Use
- [Scenario 1]
- [Scenario 2]

## Core Principles
[3-5 key principles]

## Techniques

### Technique 1: [Name]
**What**: [Brief description]
**Why**: [Rationale]
**How**: [Step-by-step]
**Example**: [Before/After]

### Technique 2: [Name]
[Same structure]

## Exercises

### Exercise 1: [Name]
**Goal**: [What you'll learn]
**Instructions**: [Step-by-step]
**Time**: [Duration]

## Guiding Questions
- [Question 1]
- [Question 2]
- [Question 3]

## Checklist
- [ ] [Checkpoint 1]
- [ ] [Checkpoint 2]

## Common Mistakes
1. **Mistake**: [Description]
   **Fix**: [Solution]

## Further Reading
- [Source 1]
- [Source 2]

## Integration with Other Layers
[How this connects to other layers]
```

---

### Toolkit Reference File Template

Similar to layer files but more focused:

```markdown
# [Toolkit Name]

## Source
[Original author/book]

## Philosophy
[1-2 paragraphs on the approach]

## When to Use This Toolkit
[Specific use cases]

## Techniques

### Technique 1: [Name]
**Rule**: [The principle]
**Application**: [How to apply]
**Example**:
- Before: [unclear version]
- After: [improved version]
- Analysis: [what changed and why]

## Quick Reference
[Bulleted list of key rules]

## Application Checklist
- [ ] [Check 1]
- [ ] [Check 2]

## Examples

### Example 1: [Context]
[Full before/after with annotation]

## Common Pitfalls
[What to avoid]
```

---

### Script Specifications

#### 1. analyze-text.py

**Purpose**: Provide objective text statistics

**Inputs**:
- File path or stdin
- Optional: comparison file (for tracking changes)

**Outputs**:
```
Text Analysis Report
===================
Total words: 1,234
Total sentences: 56
Total paragraphs: 12
Average words per sentence: 22.0
Longest sentence: 47 words (line 23)
Shortest sentence: 3 words (line 45)
Reading level: Grade 10 (Flesch-Kincaid)
Reading ease: 62.3 (standard)

Suggestions:
- 3 sentences exceed 30 words (lines 23, 34, 51)
- Consider breaking up longer sentences
```

**Tech Stack**: Python 3, textstat library for readability

**Implementation**:
```python
#!/usr/bin/env python3
"""
Analyze text for basic statistics and readability.

Usage:
    python analyze-text.py input.txt
    cat input.txt | python analyze-text.py
"""

import sys
import re
from pathlib import Path

def count_sentences(text):
    # Use regex to count sentence-ending punctuation
    sentences = re.split(r'[.!?]+', text)
    return len([s for s in sentences if s.strip()])

def count_words(text):
    return len(text.split())

def count_paragraphs(text):
    paragraphs = text.split('\n\n')
    return len([p for p in paragraphs if p.strip()])

def analyze_sentences(text):
    sentences = re.split(r'([.!?]+)', text)
    # Combine sentence with its punctuation
    # ... more implementation

def main():
    # Read from file or stdin
    # Perform analysis
    # Generate report
    pass

if __name__ == '__main__':
    main()
```

#### 2. detect-clutter.py

**Purpose**: Flag potential clutter words and constructions

**Inputs**:
- File path or stdin

**Outputs**:
```
Clutter Detection Report
========================

ADVERBS (26 found):
- Line 5: "really important" → Consider "important" or find stronger word
- Line 12: "very quickly" → Consider "quickly" or "rapidly"
- Line 23: "extremely difficult" → Consider "difficult" or "arduous"

QUALIFIERS (14 found):
- Line 8: "somewhat concerned" → Consider "concerned"
- Line 15: "rather interesting" → Consider "interesting" or "fascinating"

PASSIVE VOICE (8 found):
- Line 3: "was written by" → Consider active voice
- Line 19: "is believed to be" → Consider active voice

WEAK VERBS (12 found):
- Line 7: "is very" → Consider stronger verb
- Line 22: "there are several" → Consider concrete subject

SUMMARY:
Total potential clutter: 60 instances
Estimated wordiness: moderate
Recommended focus: adverbs and qualifiers
```

**Tech Stack**: Python 3, regex

**Implementation**:
```python
#!/usr/bin/env python3
"""
Detect clutter words and weak constructions.

Usage:
    python detect-clutter.py input.txt
"""

import re
import sys
from pathlib import Path
from collections import defaultdict

ADVERBS = r'\b\w+ly\b'
QUALIFIERS = ['very', 'really', 'quite', 'rather', 'somewhat', 'fairly']
PASSIVE_INDICATORS = ['is', 'are', 'was', 'were', 'been', 'being']
WEAK_VERBS = ['is', 'are', 'was', 'were', 'has', 'have', 'had']

def detect_adverbs(text, line_num):
    # Find -ly words
    pass

def detect_qualifiers(text, line_num):
    # Find qualifier words
    pass

def detect_passive(text, line_num):
    # Find passive constructions
    pass

def detect_weak_verbs(text, line_num):
    # Find weak verb usage
    pass

def main():
    # Read file
    # Run detectors
    # Generate report
    pass

if __name__ == '__main__':
    main()
```

#### 3. sentence-variety.py

**Purpose**: Analyze sentence length patterns

**Outputs**:
```
Sentence Variety Analysis
=========================

Sentence Length Distribution:
0-10 words:   ████████ (8 sentences)
11-20 words:  ████████████████ (16 sentences)
21-30 words:  ████████ (8 sentences)
31-40 words:  ████ (4 sentences)
41+ words:    ██ (2 sentences)

Average: 21 words
Median: 18 words
Std dev: 9.2 words

RHYTHM ANALYSIS:
✓ Good variety overall
⚠ Lines 23-27: 5 consecutive sentences of 18-20 words (monotonous)
⚠ Lines 45-49: 5 consecutive sentences of 12-14 words (monotonous)

RECOMMENDATIONS:
- Consider varying sentence length in lines 23-27
- Mix short punchy sentences with longer flowing ones
- Current variety score: 7/10 (good)
```

**Tech Stack**: Python 3

#### 4. success-checker.py

**Purpose**: Interactive checklist for SUCCESs model

**Implementation**: Interactive CLI script that prompts for each element

```
SUCCESs Stickiness Checker
===========================

Let's evaluate your message against the SUCCESs model.

[S] SIMPLE
----------
What is your core message in 12 words or less?
> [user input]

Can you cut it to one sentence?
> [user input]

Is this the single most important idea?
(y/n) >

Score: [X]/3
Notes: [Generated feedback]

[U] UNEXPECTED
--------------
What will surprise your reader?
> [user input]

Where does your message violate expectations?
> [user input]

What curiosity gap do you create?
> [user input]

Score: [X]/3
Notes: [Generated feedback]

...continues for all 6 elements...

FINAL SCORE: [X]/18
OVERALL: [Weak/Moderate/Strong]

RECOMMENDATIONS:
- [Specific suggestions based on low scores]
```

---

## Workflow Logic Details

### Full Writing Process Workflow

**Sequence**: Layers 1 → 2 → 3 → 4 → 5 → Output

**Step-by-Step**:

1. **Intent Discovery (Layer 1)**
   ```
   → Ask: What are you writing?
   → Ask: Who is your audience?
   → Ask: What must they remember?
   → Guide through core promise formulation
   → Generate Intent Brief
   → Checkpoint: Is intent clear?
   ```

2. **Structural Architecture (Layer 2)**
   ```
   → Present structure types
   → Ask guiding questions about material
   → Generate 3 blueprint options
   → User selects preferred structure
   → Annotate structure with gold coin placement
   → Generate Structure Document
   → Checkpoint: Does structure support intent?
   ```

3. **Drafting Discipline (Layer 3)**
   ```
   → Set up drafting session (timeboxing)
   → Remind: shitty first draft is good
   → Provide techniques: concrete nouns, strong verbs
   → User drafts (skill waits or checks in)
   → Optional: read draft for next phase
   → Checkpoint: Is draft complete?
   ```

4. **Revision Engine (Layer 4)**
   ```
   → Pass 1: Cut clutter
     - Run detect-clutter.py
     - Guide through cutting 10-25%
     - Checkpoint: Leaner?

   → Pass 2: Cognitive load
     - Check for garden paths
     - Subject-verb proximity
     - Topic chains
     - Checkpoint: Easier to read?

   → Pass 3: Rhythm
     - Run sentence-variety.py
     - Vary sentence length
     - Strong endings
     - Checkpoint: Better flow?

   → Pass 4: Message
     - Apply specific toolkit if needed
     - Checkpoint: Clearer message?
   ```

5. **Messaging & Stickiness (Layer 5)**
   ```
   → Run success-checker.py
   → Work through each SUCCESs element
   → Generate stickiness score
   → Make improvements
   → Checkpoint: Is it sticky?
   ```

6. **Final Output**
   ```
   → Generate complete package:
     - Intent Brief
     - Structure Diagram
     - Final Draft (multiple versions)
     - Revision Notes
     - SUCCESs Analysis
     - Title Variants
     - Lede Variants
   → Save to user location
   ```

---

### Revision & Polish Workflow

**Sequence**: Layers 4 → 5 → Output

**Assumptions**:
- User has existing draft
- Intent and structure already clear (or can infer)

**Step-by-Step**:

1. **Intake**
   ```
   → Ask: Where is your draft?
   → Read draft
   → Run analyze-text.py for baseline
   → Ask: What are you trying to achieve? (quick intent check)
   ```

2. **Four-Pass Revision (Layer 4)**
   ```
   [Same as in Full Process]
   ```

3. **Stickiness Enhancement (Layer 5)**
   ```
   [Same as in Full Process]
   ```

4. **Output**
   ```
   → Before/After comparison
   → Statistics (words cut, readability improvement)
   → Stickiness score
   → Suggested next steps
   ```

---

## User Experience Flows

### Example Session 1: Full Process

```
USER: /writer

SKILL: Welcome to the Writing Mentor skill!

What would you like to do?
1. Write something new (full process)
2. Revise an existing draft
3. Plan structure for an idea
4. Quick toolkit application
5. Stickiness check

USER: 1

SKILL: Great! Let's walk through the complete writing process together.

First, let's discover your intent. What are you writing?
- Blog post
- Essay
- Article
- Other

USER: Blog post

SKILL: Perfect. Who is your primary audience?

USER: Software engineers interested in AI

SKILL: Excellent. Now, what must they remember if they forget everything else?
What's the one core idea?

USER: AI agents need structured prompts to work effectively

SKILL: Good start. Let's refine that to 12 words or less...

[Continues through all phases...]
```

### Example Session 2: Quick Revision

```
USER: /writer

SKILL: What would you like to do?

USER: I have a draft I need to polish

SKILL: Perfect. Where is your draft?

USER: /Users/kushaldsouza/Documents/blog-post.md

SKILL: [Reads file]

I've analyzed your draft. Here are the basics:
- 1,247 words
- 58 sentences
- Average sentence length: 21.5 words
- Reading level: Grade 11

Let's start with the clutter pass. I'm running the clutter detector...

[Shows clutter report]

I found 34 potential clutter words. Let's start with the adverbs...

[Continues through revision passes...]
```

---

## Integration Points

### Saving Work
- Ask user where to save deliverables
- Default to current working directory
- Create organized structure:
  ```
  writing-project-name/
  ├── intent-brief.md
  ├── structure-diagram.md
  ├── draft-v1.md
  ├── draft-v2-revised.md
  ├── revision-notes.md
  └── success-analysis.md
  ```

### Multi-Session Support
- Use scratchpad for session state
- File naming: `writer-session-TIMESTAMP.md`
- Allow resuming from checkpoints

### Script Integration
- Run scripts automatically at appropriate points
- Always ask before running (don't surprise user)
- Show output inline, offer to save full report

---

## Success Metrics

### For MVP (Phase 1):
- [ ] User can complete revision workflow end-to-end
- [ ] Scripts run without errors
- [ ] Reference content is helpful and clear
- [ ] Output deliverables are usable
- [ ] Process feels natural, not forced

### For Full Release (Phase 3):
- [ ] All 7 workflows functional
- [ ] All reference files complete with examples
- [ ] All scripts working and useful
- [ ] User feedback is positive
- [ ] Skill improves writing quality measurably

---

## Timeline Estimate

### Phase 1 (MVP): 4-6 hours
- skills.md: 1 hour
- 2 workflow files: 1.5 hours
- 2 layer files: 1.5 hours
- 2 scripts: 1.5 hours
- Testing: 0.5 hours

### Phase 2 (Expansion): 6-8 hours
- 5 workflow files: 2 hours
- 4 layer files: 2 hours
- 3 toolkit files: 2 hours
- Testing: 1 hour
- Iteration: 1 hour

### Phase 3 (Polish): 4-6 hours
- Remaining toolkit files: 1.5 hours
- Example files: 1.5 hours
- Documentation: 1 hour
- Final scripts: 1 hour
- Testing & refinement: 1.5 hours

**Total: 14-20 hours**

---

## Recommended Build Order

1. ✅ Analysis complete (done)
2. ✅ Research complete (done)
3. Start Phase 1:
   a. Create file structure
   b. Write skills.md (router logic)
   c. Write revision-and-polish workflow
   d. Write revision-engine layer reference
   e. Write messaging-stickiness layer reference
   f. Build analyze-text.py
   g. Build detect-clutter.py
   h. Test MVP workflow
4. Start Phase 2:
   a. Write remaining workflow files
   b. Write remaining core layer files
   c. Write essential toolkit files
   d. Test all workflows
5. Start Phase 3:
   a. Complete toolkit files
   b. Create rich examples
   c. Build remaining scripts
   d. Write documentation
   e. Final testing
   f. Launch!

---

## Notes for Building

### Technical Considerations
- **Python version**: Use Python 3.8+ (for broad compatibility)
- **Dependencies**: Minimize external dependencies, document clearly
- **Error handling**: Scripts should fail gracefully
- **User input**: Validate all user input
- **File paths**: Handle spaces, special characters

### Writing Considerations
- **Tone**: Match original prompt (precise but warm, rigorous but encouraging)
- **Examples**: Create our own to avoid copyright issues
- **Clarity**: Follow our own advice (concrete, simple, clear)
- **Actionability**: Every section should enable action

### User Experience Considerations
- **Don't overwhelm**: Progressive disclosure of information
- **Allow skipping**: Expert users can jump ahead
- **Provide examples**: Show, don't just tell
- **Encourage**: Writing is hard, be supportive
- **Be flexible**: Not everyone works the same way

---

## Ready to Build

All analysis complete. All research complete. Implementation plan ready.

**Recommendation**: Start with Phase 1 MVP focusing on the revision workflow, which is likely the most commonly used entry point. Get that working well, then expand.

**First file to create**: `skills/writer/skills.md` with the basic router logic and workflow descriptions.
