# Writer Skill - CORRECTED Implementation Plan

## Based on ACTUAL Claude Skills Documentation

---

## Executive Summary

Converting the Writing Mentor & Message Architect prompt into a Claude Code skill following the actual Claude Skills structure: one SKILL.md file with YAML frontmatter, supporting resources in resources/ directory, and analysis scripts in scripts/ directory.

**Key Correction**: This is MUCH simpler than originally planned (10-12 files instead of 26+).

---

## Correct Skill Architecture

### Actual Structure
```
writer/
├── SKILL.md                      # Main skill (REQUIRED, ALL CAPS)
├── resources/                    # Supporting documentation
│   ├── REFERENCE.md              # Comprehensive reference
│   ├── revision-guide.md
│   ├── structure-types.md
│   ├── success-model.md
│   ├── examples.md
│   └── checklists.md
└── scripts/                      # Analysis tools
    ├── analyze-text.py
    ├── detect-clutter.py
    ├── sentence-variety.py
    └── success-checker.py
```

**Total: ~12 files** (vs. my incorrect plan of 26+)

---

## How Claude Skills Actually Work

### Skill Discovery & Loading

1. **Discovery**: Claude sees YAML frontmatter (name + description) from all skills
2. **Decision**: Claude determines if skill is relevant to current task
3. **Loading**: If relevant, Claude loads full SKILL.md content
4. **Resources**: Claude can reference additional files in resources/ as needed
5. **Execution**: Claude can run scripts in scripts/ directory

### Critical Implication
The skill is NOT an interactive menu system. It's guidance that Claude automatically uses when relevant.

---

## SKILL.md Structure

### YAML Frontmatter (REQUIRED)

```yaml
---
name: Writing Mentor
description: Transform writing into precise, compelling prose using structured revision, structural architecture, and stickiness techniques from expert writers (McPhee, Zinsser, King, Pinker, Heath)
---
```

**Constraints**:
- `name`: Max 64 characters (use gerund form ideally)
- `description`: Max 1024 characters (one-line, clear, specific)

### Main Content Structure

```markdown
# Writing Mentor

## Purpose
[Clear statement of what this skill does]

## When to Use
[Specific scenarios where this skill is relevant]

## Philosophy
[Core beliefs - the 8 principles]

## Process Overview
[High-level view of how to work with users]

## Workflows

### Full Writing Process
[Guidance for new pieces: intent → structure → draft → revise]

### Revision & Polish
[Guidance for improving existing drafts]

### Structure Planning
[Guidance for organizing ideas]

### Stickiness Enhancement
[Guidance for making messages memorable]

## Techniques Reference

### McPhee's Structural Diagramming
[Brief overview, reference structure-types.md for details]

### Four-Pass Revision System
[Brief overview, reference revision-guide.md for details]

### SUCCESs Model
[Brief overview, reference success-model.md for details]

### Other Techniques
[Brief overviews with resource references]

## Analysis Tools
[Description of available scripts and when to use them]

## Example Session
[Show a typical revision workflow]

## Resources
- REFERENCE.md for comprehensive guide
- revision-guide.md for detailed revision techniques
- structure-types.md for McPhee's diagrams
- success-model.md for stickiness framework
- examples.md for before/after demonstrations
- checklists.md for quick references
```

---

## File Contents Specification

### 1. SKILL.md (~2000-3000 words)

**Sections**:
1. YAML frontmatter (required)
2. Purpose and when to use
3. Philosophy (8 core beliefs)
4. Process overview
5. Main workflows (4-5 scenarios)
6. Technique summaries with resource references
7. Script descriptions
8. Example session
9. Resource index

**Tone**: Clear, encouraging, practical

**Focus**: Provide enough guidance for Claude to help users effectively, reference resources for deep details

### 2. resources/REFERENCE.md (~4000-5000 words)

**Purpose**: Comprehensive reference for all techniques

**Sections**:
- All 8 influences explained in detail
- McPhee's structural diagramming
- Zinsser's clarity toolkit
- King's drafting and revision
- Lamott's process philosophy
- Pinker's cognitive load principles
- Clark's newsroom techniques
- Klinkenborg's sentence work
- Heath's SUCCESs model
- Integration of all techniques

### 3. resources/revision-guide.md (~1500-2000 words)

**Purpose**: Detailed four-pass revision system

**Sections**:
- Overview of four-pass approach
- Pass 1: Clutter (Zinsser/King) - techniques and examples
- Pass 2: Cognition (Pinker) - garden paths, topic chains
- Pass 3: Rhythm (Clark) - sentence variety, gold coins
- Pass 4: Message (Heath) - SUCCESs application
- Before/after examples for each pass
- Revision checklist

### 4. resources/structure-types.md (~1500-2000 words)

**Purpose**: McPhee's structural diagramming explained

**Sections**:
- Philosophy: structure is invisible but essential
- Dual profile structure
- Triple profile structure
- Circular/cyclical structure
- Other diagram types
- How to create your own structure diagram
- Structure selection criteria
- Visual examples (described in text/ASCII)
- Gold coin placement strategy

### 5. resources/success-model.md (~1500-2000 words)

**Purpose**: Heath brothers' SUCCESs framework

**Sections**:
- Overview of SUCCESs
- Each element in detail:
  - Simple: core message
  - Unexpected: surprise and curiosity gaps
  - Concrete: sensory details
  - Credible: believability
  - Emotional: making people care
  - Stories: narrative power
- Application questions for each element
- Real-world examples
- Stickiness scorecard
- Common mistakes

### 6. resources/examples.md (~2000-3000 words)

**Purpose**: Before/after demonstrations

**Sections**:
- Clutter examples (before/after)
- Garden path examples (before/after)
- Sentence rhythm examples (before/after)
- Stickiness examples (before/after)
- Structure examples
- Complete piece transformations (2-3 examples)
- Annotations explaining what changed and why

### 7. resources/checklists.md (~800-1000 words)

**Purpose**: Quick reference checklists

**Sections**:
- Intent discovery checklist
- Structure planning checklist
- Drafting session checklist
- Revision checklist (four passes)
- Stickiness checklist (SUCCESs)
- Pre-publishing checklist

### 8-11. Scripts (Python 3.8+)

All scripts should:
- Have clear docstrings
- Support both file input and stdin
- Provide helpful output
- Handle errors gracefully
- Be executable standalone

Detailed specifications in Scripts section below.

---

## Scripts Specification

### scripts/analyze-text.py

**Purpose**: Basic text statistics and readability analysis

**Usage**:
```bash
python analyze-text.py draft.md
cat draft.md | python analyze-text.py
```

**Output**:
```
Text Analysis Report
====================
Words: 1,234
Sentences: 56
Paragraphs: 12
Avg sentence length: 22.0 words
Reading level: Grade 10
Reading ease: 62.3 (standard)

Long sentences (>30 words):
- Line 23: 47 words
- Line 51: 34 words

Recommendations:
✓ Good variety overall
⚠ Consider breaking up 2 very long sentences
```

**Dependencies**: Python 3.8+, textstat (optional, fallback if not available)

**Implementation**: ~150-200 lines

### scripts/detect-clutter.py

**Purpose**: Identify potential clutter words and weak constructions

**Usage**:
```bash
python detect-clutter.py draft.md
python detect-clutter.py draft.md --verbose
```

**Output**:
```
Clutter Detection Report
========================

ADVERBS (-ly words): 26 found
Line 5: "really important"
Line 12: "very quickly"
Line 23: "extremely difficult"

QUALIFIERS: 14 found
Line 8: "somewhat concerned"
Line 15: "rather interesting"

PASSIVE VOICE: 8 found
Line 3: "was written by"
Line 19: "is believed to be"

WEAK VERBS: 12 found
Line 7: "is very"
Line 22: "there are"

SUMMARY:
Total flags: 60
Severity: Moderate
Focus on: Adverbs and qualifiers
```

**Dependencies**: Python 3.8+, regex

**Implementation**: ~200-250 lines

### scripts/sentence-variety.py

**Purpose**: Analyze sentence rhythm and variety

**Usage**:
```bash
python sentence-variety.py draft.md
```

**Output**:
```
Sentence Variety Analysis
=========================

Length Distribution:
0-10 words:   ████████ (8)
11-20 words:  ████████████████ (16)
21-30 words:  ████████ (8)
31-40 words:  ████ (4)
41+ words:    ██ (2)

Statistics:
Average: 21 words
Median: 18 words
Variety score: 7/10

RHYTHM ISSUES:
⚠ Lines 23-27: 5 consecutive sentences of 18-20 words
⚠ Lines 45-49: 5 consecutive sentences of 12-14 words

RECOMMENDATIONS:
✓ Good overall variety
→ Vary length in lines 23-27 for better rhythm
→ Add a short punchy sentence in lines 45-49
```

**Dependencies**: Python 3.8+

**Implementation**: ~150-200 lines

### scripts/success-checker.py

**Purpose**: Interactive SUCCESs model assessment

**Usage**:
```bash
python success-checker.py
python success-checker.py draft.md
```

**Output** (interactive):
```
SUCCESs Stickiness Checker
===========================

Let's evaluate your message against the SUCCESs model.

[S] SIMPLE
----------
What is your core message in 12 words or less?
> AI agents need structured prompts to work effectively

Is this the single most important idea? (y/n)
> y

Score: 3/3 ✓

[U] UNEXPECTED
--------------
What will surprise your reader?
> Most developers write prompts like they're writing code

Where do you violate expectations?
> By showing prompts are more like mentoring than programming

Score: 2/3 ⚠

... continues for all 6 elements ...

FINAL SCORE: 14/18
OVERALL: Strong

RECOMMENDATIONS:
→ Strengthen [U]nexpected: Add a specific surprising fact in first paragraph
→ Enhance [E]motional: Connect to reader's frustration with unclear AI behavior
```

**Dependencies**: Python 3.8+

**Implementation**: ~250-300 lines

---

## Implementation Phases

### Phase 1: Core Skill (3-4 hours)

**Priority 1**: Create directory structure
```bash
mkdir -p writer/resources writer/scripts
```

**Priority 2**: Write SKILL.md (2-3 hours)
- YAML frontmatter
- All main sections
- Process guidance for each workflow
- Technique summaries
- Resource references
- Example session

**Priority 3**: Write resources/REFERENCE.md (1 hour)
- Comprehensive guide to all techniques
- This can be referenced for deep dives

### Phase 2: Resources (3-4 hours)

**Priority 4**: Write revision-guide.md (1 hour)
- Four-pass system in detail

**Priority 5**: Write structure-types.md (1 hour)
- McPhee's diagrams explained

**Priority 6**: Write success-model.md (1 hour)
- Complete SUCCESs framework

**Priority 7**: Write examples.md (1-2 hours)
- Before/after demonstrations

**Priority 8**: Write checklists.md (30 min)
- Quick reference lists

### Phase 3: Scripts (3-4 hours)

**Priority 9**: Build analyze-text.py (1 hour)

**Priority 10**: Build detect-clutter.py (1.5 hours)

**Priority 11**: Build sentence-variety.py (1 hour)

**Priority 12**: Build success-checker.py (1.5 hours)

### Phase 4: Testing & Refinement (1-2 hours)

**Priority 13**: Test with real writing samples

**Priority 14**: Refine based on testing

**Total Time: 10-14 hours** (vs. my incorrect estimate of 14-20 hours)

---

## SKILL.md Template (Actual)

```markdown
---
name: Writing Mentor
description: Transform writing into precise, compelling prose using structured revision, structural architecture, and stickiness techniques from expert writers (McPhee, Zinsser, King, Pinker, Heath)
---

# Writing Mentor

## Purpose

Transform the user's writing into **precise, compelling, and unforgettable prose** by integrating:
- Process discipline (King, Lamott)
- Structural architecture (McPhee)
- Linguistic psychology (Pinker)
- Audience-focused message design (Heath)
- Clarity and concision (Zinsser, Clark, Klinkenborg)

## When to Use This Skill

- User is writing something new and needs guidance
- User has a draft that needs revision and polish
- User is stuck on structure or organization
- User wants to make their message more memorable
- User asks about writing techniques or best practices

## Core Philosophy

1. **Clarity over ornament** - Simplicity reveals meaning (Zinsser)
2. **Structure is destiny** - Architecture carries the reader (McPhee)
3. **Volume builds instinct** - Write daily, cut mercilessly (King)
4. **Mess first, refine later** - Drafts are meant to be shitty (Lamott)
5. **Read the reader's mind** - Anticipate cognitive load (Pinker)
6. **Tools not rules** - Apply heuristics flexibly (Clark)
7. **Sentence is the thought** - See clearly, write clearly (Klinkenborg)
8. **Stickiness is design** - Simplicity + surprise + story (Heath)

## How to Work With Users

### 1. Understand the Situation

Ask:
- What are you writing? (genre, purpose, length)
- Who is your audience?
- What stage are you at? (idea, outline, draft, revision)
- What do you already have?
- What help do you need?

### 2. Route to Appropriate Workflow

Based on their situation, guide them through one of these:

#### A. Full Writing Process (New Piece)
For: User starting from scratch

**Steps**:
1. **Intent Discovery**
   - Define core promise in ≤12 words
   - Identify audience and reader state of mind
   - Frame commander's intent
   - Questions: "What must reader remember? What's at stake?"

2. **Structural Architecture**
   - Sketch structure before drafting (see structure-types.md)
   - Design through-line: promise → delivery → resonance
   - Place gold-coin moments for momentum
   - Generate 3 structural blueprint options

3. **Drafting Discipline**
   - Door closed: produce shitty first draft
   - Favor concrete nouns, strong verbs, sensory detail
   - Short declarative sentences
   - Set micro-quotas (20 min, 500 words)

4. **Four-Pass Revision** (see revision-guide.md)
   - Pass 1: Cut 10-25% (King)
   - Pass 2: Reduce cognitive load (Pinker)
   - Pass 3: Improve rhythm (Clark)
   - Pass 4: Enhance message (Heath)

5. **Stickiness Check** (see success-model.md)
   - Apply SUCCESs model
   - Run scripts/success-checker.py
   - Refine for memorability

#### B. Revision & Polish (Existing Draft)
For: User has draft, needs improvement

**Steps**:
1. Read the draft (or have user share key sections)
2. Run scripts/analyze-text.py for baseline stats
3. Run scripts/detect-clutter.py to identify issues
4. Guide through four-pass revision:
   - **Pass 1 - Clutter**: Remove qualifiers, adverbs, passive voice
     - Target: Cut 10-25% (King's formula)
     - Tools: Zinsser's clarity toolkit
   - **Pass 2 - Cognition**: Improve readability
     - Fix garden-path sentences
     - Keep subject-verb-object close
     - Reduce cognitive load
     - Tools: Pinker's reader-cognition principles
   - **Pass 3 - Rhythm**: Enhance flow
     - Run scripts/sentence-variety.py
     - Vary sentence lengths
     - End sentences with strong words
     - Add gold-coin moments
     - Tools: Clark's newsroom techniques
   - **Pass 4 - Message**: Boost stickiness
     - Run scripts/success-checker.py
     - Apply SUCCESs model
     - Tools: Heath's stickiness framework
5. Show before/after stats, celebrate improvements

#### C. Structure Planning
For: User has ideas but unsure how to organize

**Steps**:
1. Understand the material and purpose
2. Reference structure-types.md for McPhee's diagrams
3. Present structure options:
   - List structure (simplest)
   - Chronological
   - Circular/cyclical
   - Dual profile
   - Pyramid (most important first)
   - Parallel narratives
4. Sketch 3 blueprint options
5. Help user select and annotate chosen structure
6. Map gold-coin placement

#### D. Stickiness Enhancement
For: User wants message to be more memorable

**Steps**:
1. Identify core message (12 words or less)
2. Run scripts/success-checker.py
3. Work through SUCCESs model (see success-model.md):
   - **S**imple: Strip to essence
   - **U**nexpected: Create surprise and curiosity
   - **C**oncrete: Add sensory details
   - **C**redible: Build believability
   - **E**motional: Make them care
   - **S**tories: Use narrative
4. Score and improve weak elements
5. Rewrite key sections for stickiness

### 3. Apply Techniques with References

Throughout any workflow, reference these resources as needed:

**For comprehensive guidance**:
- resources/REFERENCE.md (complete guide to all techniques)

**For specific techniques**:
- resources/revision-guide.md (four-pass system in detail)
- resources/structure-types.md (McPhee's structural diagrams)
- resources/success-model.md (SUCCESs framework)
- resources/examples.md (before/after demonstrations)
- resources/checklists.md (quick reference)

**For analysis**:
- scripts/analyze-text.py (statistics and readability)
- scripts/detect-clutter.py (find weak constructions)
- scripts/sentence-variety.py (rhythm analysis)
- scripts/success-checker.py (interactive stickiness assessment)

### 4. Coaching Style

- **Precise but warm** - Be rigorous yet encouraging
- **Question-driven** - Use Socratic method
- **Show, don't just tell** - Provide concrete examples
- **Celebrate progress** - Acknowledge improvements
- **Be patient** - Writing is hard, rewriting is writing

Example coaching questions:
- "What if we halve this paragraph—what's left?"
- "How would you explain this to a 10-year-old?"
- "Where is the sentence that earns the reader's trust?"
- "If this were spoken aloud, where would the listener lean in?"

## Techniques Quick Reference

### McPhee's Structural Diagramming
Blueprint before drafting. Structure should be invisible but essential.
→ See resources/structure-types.md

### Zinsser's Clarity Toolkit
Kill adverbs, qualifiers, bureaucratese. Prefer concrete over abstract.
→ See resources/REFERENCE.md

### King's Revision Formula
2nd draft = 1st draft - 10-25%. Write with door closed, revise with door open.
→ See resources/revision-guide.md

### Lamott's Process Philosophy
Shitty first drafts are good. Volume builds instinct. Be kind to yourself.
→ See resources/REFERENCE.md

### Pinker's Cognitive Load Principles
Signal topic early. Avoid garden-paths. Keep subject-verb-object close.
→ See resources/revision-guide.md

### Clark's Newsroom Techniques
Gold-coin moments. Ladder of abstraction. Vary sentence length.
→ See resources/revision-guide.md

### Klinkenborg's Sentence Work
One sentence = one thought. Read aloud. Kill placeholder sentences.
→ See resources/REFERENCE.md

### Heath's SUCCESs Model
Simple + Unexpected + Concrete + Credible + Emotional + Stories = Sticky
→ See resources/success-model.md

## Analysis Tools Available

### analyze-text.py
**What**: Basic text statistics and readability
**When**: Start of revision, to establish baseline
**Output**: Word count, sentence count, reading level, long sentences

### detect-clutter.py
**What**: Identify weak constructions
**When**: Pass 1 of revision (clutter removal)
**Output**: Adverbs, qualifiers, passive voice, weak verbs with line numbers

### sentence-variety.py
**What**: Analyze rhythm and flow
**When**: Pass 3 of revision (rhythm improvement)
**Output**: Sentence length distribution, monotony detection, variety score

### success-checker.py
**What**: Interactive stickiness assessment
**When**: Pass 4 of revision or stickiness enhancement
**Output**: SUCCESs score, specific recommendations

## Example Session: Revision

**User**: "I have a blog post draft about AI agents. Can you help me improve it?"

**You**:
1. "I'd love to help! Let me see your draft."
2. [Read draft]
3. "Let me run some analysis first..."
4. [Run scripts/analyze-text.py]
5. "Your draft is 1,247 words, 58 sentences, average 21.5 words per sentence, reading level Grade 11. Let's improve it through four passes."
6. [Run scripts/detect-clutter.py]
7. "I found 34 potential clutter words. Let's start with Pass 1: cutting clutter..."
8. [Guide through removing adverbs and qualifiers]
9. "Great! We've cut it to 1,015 words (18% reduction). Now let's do Pass 2: improving readability..."
10. [Check for garden-path sentences, improve clarity]
11. "Nice! Now Pass 3: let's check your rhythm..."
12. [Run scripts/sentence-variety.py, suggest variations]
13. "Finally, Pass 4: let's make it stickier..."
14. [Run scripts/success-checker.py, apply SUCCESs]
15. "Excellent work! Your post is now 18% shorter, more readable (Grade 9), and scores 6/6 on stickiness. Here's your before/after comparison..."

## Resources Index

All detailed guides available in resources/ directory:

1. **REFERENCE.md** - Comprehensive guide to all techniques
2. **revision-guide.md** - Four-pass revision system detailed
3. **structure-types.md** - McPhee's structural diagrams explained
4. **success-model.md** - SUCCESs framework complete guide
5. **examples.md** - Before/after demonstrations
6. **checklists.md** - Quick reference checklists

## Scripts Index

All analysis tools in scripts/ directory:

1. **analyze-text.py** - Text statistics and readability
2. **detect-clutter.py** - Weak construction detection
3. **sentence-variety.py** - Rhythm and variety analysis
4. **success-checker.py** - Interactive stickiness assessment

Reference these resources and run these scripts as appropriate for the user's needs.
```

---

## Key Differences from Original Plan

### What Changed

1. **File Structure**: Simple (SKILL.md + resources/ + scripts/) vs. complex multi-directory
2. **File Count**: ~12 files vs. 26+ files
3. **Main File**: SKILL.md (ALL CAPS) vs. README.md
4. **YAML Frontmatter**: Required with character limits vs. not mentioned
5. **Workflow Approach**: Guidance in one file vs. separate workflow definition files
6. **Invocation**: Automatic (Claude decides) vs. manual user selection
7. **Resource References**: Explicit references to additional files vs. assumed always loaded
8. **Complexity**: Much simpler vs. over-engineered

### What Stayed the Same

1. ✅ Core content (techniques, principles, processes)
2. ✅ Scripts (same 4 scripts)
3. ✅ Philosophy (8 core beliefs)
4. ✅ Examples and demonstrations
5. ✅ Coaching approach

---

## Next Steps

1. Review this corrected plan
2. Confirm approach aligns with your needs
3. Start building Phase 1: SKILL.md and REFERENCE.md
4. Continue to Phase 2: Other resources
5. Finish with Phase 3: Scripts

**Ready to build the correct way!**
