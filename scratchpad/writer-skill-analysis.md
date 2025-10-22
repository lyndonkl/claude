# Writer Skill Analysis & Design

## Overview
Converting the Writing Mentor & Message Architect prompt into a comprehensive skill that guides users through the writing process with interactive checklists and reference materials.

---

## Prompt Analysis

### Core Structure
The prompt is built on a 7-layer framework that represents the complete writing process:

1. **Layer 1: Intent Discovery** - Define core promise, audience, stakes
2. **Layer 2: Structural Architecture** - Blueprint before drafting
3. **Layer 3: Drafting Discipline** - First draft with specific techniques
4. **Layer 4: Revision Engine** - Multi-pass editing (cut, cognition, rhythm, message)
5. **Layer 5: Messaging & Stickiness** - SUCCESs model application
6. **Layer 6: Micro-Toolkits** - 5 specialized toolkits (Zinsser, Pinker, Clark, Klinkenborg, Heath)
7. **Layer 7: Socratic Coaching** - Guiding questions

### Key Influences
- John McPhee (structure)
- William Zinsser (clarity)
- Stephen King (discipline)
- Anne Lamott (process compassion)
- Steven Pinker (cognitive science)
- Roy Peter Clark (newsroom tactics)
- Verlyn Klinkenborg (sentence-level)
- Chip & Dan Heath (sticky messages)

---

## Identified Workflows

### 1. Full Writing Process (New Piece)
**Use case**: User wants to write something from scratch
**Steps**: Layers 1 → 2 → 3 → 4 → 5 → Final Output
**Duration**: Multiple sessions

### 2. Intent & Structure Planning
**Use case**: User needs to plan before writing
**Steps**: Layers 1 → 2
**Duration**: Single session

### 3. Drafting Session
**Use case**: User has plan and needs to draft
**Steps**: Layer 3 (with Layer 1-2 context)
**Duration**: Single session

### 4. Revision & Polish
**Use case**: User has draft and needs to refine
**Steps**: Layer 4 → Layer 5
**Duration**: Single session

### 5. Specific Toolkit Application
**Use case**: User wants to apply one specific technique
**Steps**: Choose from Layer 6 toolkits
**Duration**: Quick session

### 6. Stickiness Check
**Use case**: User wants to make message more memorable
**Steps**: Layer 5 only
**Duration**: Quick session

### 7. Structure Consultation
**Use case**: User is stuck on how to organize
**Steps**: Layer 2 only
**Duration**: Quick session

---

## Reference Files Needed

### Core Layers (7 files)

#### 1. `intent-discovery.md`
**Purpose**: Guide users through defining purpose, audience, and stakes
**Content**:
- Core promise formulation (≤12 words technique)
- Audience profiling framework
- Reader state of mind analysis
- Commander's intent framework (from military strategy)
- Guiding questions
- Examples of good vs. poor intent statements
- Exercises

#### 2. `structural-architecture.md`
**Purpose**: Help users blueprint their piece before drafting
**Content**:
- McPhee's structural diagramming method
- Structure types: list, concentric circles, pyramid, chronology, parallel narratives, hourglass
- Through-line design (promise → delivery → resonance)
- Gold-coin moments (Clark) - placing rewards for readers
- 3-blueprint technique
- Structure selection criteria
- Examples with annotations
- Visual diagrams

#### 3. `drafting-discipline.md`
**Purpose**: Guide first draft creation
**Content**:
- "Shitty first draft" philosophy (Lamott)
- Door closed vs. door open phases
- Sensory grounding techniques
- Concrete nouns + strong verbs
- Short declarative sentences
- Flow state triggers
- Micro-quotas and timeboxing
- Exercises (12 short sentences, fast/messy vs. simple)
- Anti-patterns to avoid

#### 4. `revision-engine.md`
**Purpose**: Multi-pass revision methodology
**Content**:
- King's 10-25% cutting formula
- Four-pass system:
  - Pass 1: Clutter (Zinsser/King)
  - Pass 2: Cognition (Pinker)
  - Pass 3: Rhythm (Clark)
  - Pass 4: Message (Heath)
- Specific techniques for each pass
- Revision checklist
- Before/after examples
- Common revision mistakes

#### 5. `messaging-stickiness.md`
**Purpose**: Make writing memorable using SUCCESs model
**Content**:
- Detailed SUCCESs breakdown:
  - **S**imple: one-line core
  - **U**nexpected: schema violation, curiosity gap
  - **C**oncrete: sensory, tangible details
  - **C**redible: authority, statistics, testability
  - **E**motional: tie to values
  - **S**tories: human challenge, problem-solving
- Application questions for each element
- Examples from famous writing
- Stickiness scorecard
- Common pitfalls

#### 6. `socratic-coaching.md`
**Purpose**: Question bank for self-coaching
**Content**:
- Questions organized by phase (intent, structure, draft, revise)
- Diagnostic questions (when stuck)
- Deepening questions (to improve)
- Challenge questions (to test)
- Examples of how to use questions effectively

#### 7. `output-templates.md`
**Purpose**: Standardized output formats
**Content**:
- Intent Brief template
- Structure Options template
- Draft Guidance template
- Revision Notes template
- Final Output template
- Title variants framework
- Lede variants framework

### Micro-Toolkits (5 files)

#### 8. `clarity-toolkit-zinsser.md`
**Purpose**: Zinsser's clarity principles
**Content**:
- Kill list: adverbs, qualifiers, bureaucratese, pomp
- Anglo-Saxon vs. Latinate words
- Abstractions → sensory concretes conversion
- Clutter examples
- Simplification exercises
- Clear vs. unclear examples

#### 9. `reader-cognition-toolkit-pinker.md`
**Purpose**: Psycholinguistic principles for readability
**Content**:
- Topic signaling techniques
- Garden-path sentence avoidance
- Subject-verb-object proximity
- Coherence via topic chains
- Memory load management
- Pronoun clarity
- Parsing ease checklist
- Cognitive load examples

#### 10. `newsroom-toolkit-clark.md`
**Purpose**: Journalistic techniques for compelling writing
**Content**:
- Nut graf technique (first 5-7 sentences)
- Ladder of abstraction (concrete → general → concrete)
- Gold-coin moments placement
- Lead types (summary, anecdotal, descriptive, question)
- Sentence length variation
- Strong endings
- Newsroom rules of thumb

#### 11. `sentence-toolkit-klinkenborg.md`
**Purpose**: Sentence-level precision
**Content**:
- One sentence = one thought principle
- Cadence and rhythm
- Reading aloud technique
- Placeholder sentence identification
- Sentence combining and splitting
- Active voice preference
- Specific sentence patterns
- Examples and exercises

#### 12. `stickiness-toolkit-heath.md`
**Purpose**: Detailed Heath brothers framework
**Content**:
- Commander's intent writing
- Curiosity gap creation
- Image + data + story triple
- Schema violation techniques
- Concrete language examples
- Credibility markers
- Emotional hooks
- Story structure for messages

### Supporting Materials

#### 13. `writing-examples.md`
**Purpose**: Before/after examples for all techniques
**Content**:
- Examples organized by layer
- Annotated improvements
- Failed examples (what not to do)
- Different genres (blog, essay, business, narrative)

#### 14. `quick-reference-checklist.md`
**Purpose**: One-page checklist for each workflow
**Content**:
- Full process checklist
- Revision-only checklist
- Intent discovery checklist
- Structure planning checklist
- Drafting checklist
- Polish checklist

#### 15. `writing-principles.md`
**Purpose**: Core beliefs and philosophy
**Content**:
- 8 core beliefs expanded
- Philosophy of each master
- When to apply which principle
- Resolving conflicting advice

---

## Scripts & Tools Needed

### 1. `analyze-text.py` or `analyze-text.sh`
**Purpose**: Basic text analysis
**Features**:
- Word count
- Sentence count
- Average sentence length
- Paragraph count
- Reading level (Flesch-Kincaid)
- Longest sentences flagged

### 2. `detect-clutter.py`
**Purpose**: Flag potential clutter words
**Features**:
- Detect adverbs (-ly words)
- Detect qualifiers (very, really, quite, etc.)
- Detect passive voice
- Detect weak verbs (is, are, was, were)
- Detect clichés (configurable list)
- Output with line numbers

### 3. `sentence-variety.py`
**Purpose**: Analyze sentence rhythm
**Features**:
- Sentence length histogram
- Identify monotonous patterns (5+ similar length sentences)
- Suggest variation points
- Chart visualization (optional)

### 4. `count-cuts.py`
**Purpose**: Track revision progress
**Features**:
- Compare two versions
- Calculate percentage cut
- Show deletions and additions
- Track toward King's 10-25% goal

### 5. `extract-core-message.py` (Advanced - Optional)
**Purpose**: Help identify the core message
**Features**:
- Use simple NLP to extract key phrases
- Identify most common nouns/verbs
- Suggest potential core message candidates
- Requires: basic NLP library

### 6. `success-checker.py`
**Purpose**: Check against SUCCESs model
**Features**:
- Checklist-based interactive script
- Prompt for each SUCCESs element
- Generate stickiness score
- Suggest improvements

---

## Skill Workflow Design

### Entry Point
The skill should start with a question-based router:

```
What would you like to do?
1. Write something new (full process)
2. Plan structure for existing idea
3. Get help drafting
4. Revise and polish existing draft
5. Check message stickiness
6. Apply specific toolkit
7. Quick consultation (stuck on something)
```

### Workflow Execution Pattern

For each workflow, the skill should:

1. **Understand Context**
   - What are you writing? (genre, length, audience)
   - What stage are you at?
   - What do you already have? (notes, draft, outline)

2. **Load Relevant References**
   - Pull in appropriate reference files
   - Present relevant sections
   - Offer quick-reference checklists

3. **Guide Through Steps**
   - Present each step from the checklist
   - Ask guiding questions
   - Provide examples when needed
   - Offer to run relevant scripts

4. **Gather Outputs**
   - Collect user's work at each stage
   - Store in organized format
   - Allow returning to previous stages

5. **Generate Deliverables**
   - Use output templates
   - Create final package with all artifacts
   - Provide next steps

### State Management

The skill needs to track:
- Current workflow
- Current step in workflow
- Artifacts created (intent brief, structure, drafts, etc.)
- Which references have been shown
- Which scripts have been run

This could be managed via:
- A working document in scratchpad
- Structured file naming convention
- Session summary at the end

---

## Additional Research Needed

Areas where web research could enhance the skill:

### 1. McPhee's Structural Diagramming
- Need specific examples of his structure diagrams
- His book "Draft No. 4" has detailed examples
- Visual representation techniques

### 2. Clark's Gold-Coin Moments
- Specific examples from "Writing Tools"
- How to identify natural reward points
- Pacing strategies

### 3. Heath's SUCCESs Model Details
- More examples from "Made to Stick"
- Case studies of effective application
- Common mistakes in applying the model

### 4. Klinkenborg's Sentence Philosophy
- Examples from "Several Short Sentences About Writing"
- Specific sentence patterns he recommends
- His revision process

### 5. Pinker's Cognitive Load Concepts
- Specific rules from "The Sense of Style"
- Garden-path sentence examples
- Topic chain techniques

### 6. Writing Process Best Practices
- Modern research on writing workflows
- Digital tools integration
- Iterative writing methodologies

### 7. Genre-Specific Adaptations
- How these principles adapt for:
  - Blog posts
  - Essays
  - Business writing
  - Technical writing
  - Creative nonfiction

---

## User Experience Design

### Interaction Style
- **Conversational but structured**: Guide naturally while following the process
- **Questioning**: Use Socratic method, don't just tell
- **Encouraging**: Balance rigor with Lamott's compassion
- **Practical**: Show, don't just explain

### Pacing
- **Allow skipping**: User can skip steps they've already done
- **Allow depth control**: Quick pass vs. deep dive
- **Save and resume**: Support multi-session work
- **Flexible order**: Sometimes revision before structure, etc.

### Output Format
- **Clear sections**: Use headings and structure
- **Actionable**: Every output should enable next step
- **Examples-rich**: Show, don't just tell
- **Summarized**: Provide TL;DR for busy users

---

## File Organization

```
skills/
└── writer/
    ├── skills.md                           # Main skill definition
    ├── docs/
    │   ├── writing-principles.md
    │   ├── writing-examples.md
    │   └── quick-reference-checklist.md
    ├── layers/
    │   ├── 01-intent-discovery.md
    │   ├── 02-structural-architecture.md
    │   ├── 03-drafting-discipline.md
    │   ├── 04-revision-engine.md
    │   ├── 05-messaging-stickiness.md
    │   ├── 06-socratic-coaching.md
    │   └── 07-output-templates.md
    ├── toolkits/
    │   ├── clarity-toolkit-zinsser.md
    │   ├── reader-cognition-toolkit-pinker.md
    │   ├── newsroom-toolkit-clark.md
    │   ├── sentence-toolkit-klinkenborg.md
    │   └── stickiness-toolkit-heath.md
    ├── scripts/
    │   ├── analyze-text.py
    │   ├── detect-clutter.py
    │   ├── sentence-variety.py
    │   ├── count-cuts.py
    │   └── success-checker.py
    ├── examples/
    │   ├── full-process-example.md
    │   ├── revision-example.md
    │   └── structure-example.md
    └── workflows/
        ├── full-writing-process.md
        ├── intent-and-structure.md
        ├── drafting-session.md
        ├── revision-and-polish.md
        ├── toolkit-application.md
        ├── stickiness-check.md
        └── structure-consultation.md
```

---

## Next Steps

1. ✅ Analyze the prompt (DONE)
2. ✅ Identify workflows (DONE)
3. ✅ Design file structure (DONE)
4. 🔄 Research specific techniques (IN PROGRESS - need web searches)
5. ⏳ Create reference files
6. ⏳ Write scripts
7. ⏳ Build main skill README
8. ⏳ Create workflow definitions
9. ⏳ Test with sample writing projects
10. ⏳ Iterate based on testing

---

## Open Questions

1. **Script language preference**: Python or Bash? (Python more powerful, Bash more portable)
2. **Depth of reference files**: How detailed should each be? (Suggest: 500-1000 words each with examples)
3. **Interactive vs. Batch**: Should scripts be interactive CLI or take file args? (Suggest: support both)
4. **Example sources**: Can we use published examples or create our own? (Create our own to avoid copyright)
5. **Session persistence**: How to handle multi-session workflows? (Use scratchpad with structured naming)
6. **Skill invocation**: Single skill with modes, or multiple sub-skills? (Single skill, multiple workflows)

---

## Key Insights

1. **The skill is really a process guide**: Not just a prompt, but an interactive coach that walks through a methodology
2. **Layered references are essential**: Can't fit everything in one README, need organized sub-documents
3. **Scripts add tangible value**: Objective analysis complements subjective coaching
4. **Examples are crucial**: Each technique needs before/after examples
5. **Flexibility is key**: Users enter at different stages, need non-linear navigation
6. **Balance structure with creativity**: Too rigid kills creativity, too loose loses effectiveness
7. **Multiple passes are fundamental**: Writing is rewriting - build this into every workflow
