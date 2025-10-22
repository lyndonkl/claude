# Writer Skill - Implementation Checklist

## Based on Corrected Implementation Plan

**Total Estimated Time**: 10-14 hours

---

## Phase 1: Setup & Core Skill (3-4 hours)

### 1.1 Directory Structure Setup
- [ ] Create main skill directory: `skills/writer/`
- [ ] Create resources subdirectory: `skills/writer/resources/`
- [ ] Create scripts subdirectory: `skills/writer/scripts/`
- [ ] Verify structure with `ls -la skills/writer/`

**Time**: 5 minutes

---

### 1.2 Create SKILL.md (Main Skill File)

#### 1.2.1 YAML Frontmatter
- [ ] Create `skills/writer/SKILL.md` file
- [ ] Add YAML frontmatter section with `---` delimiters
- [ ] Write `name:` field (max 64 characters)
  - Consider: "Writing Mentor" or gerund form like "Mentoring Writers"
- [ ] Write `description:` field (max 1024 characters)
  - Must clearly explain what skill does and when to use it
  - Include key techniques: McPhee, Zinsser, King, Pinker, Heath
- [ ] Verify YAML syntax is correct

**Time**: 15 minutes

#### 1.2.2 Purpose & Philosophy Section
- [ ] Write `# Writing Mentor` heading
- [ ] Write `## Purpose` section (2-3 paragraphs)
  - What this skill does
  - Integration of all expert techniques
- [ ] Write `## When to Use This Skill` section
  - List 4-5 specific use cases
  - Be clear about when skill is relevant
- [ ] Write `## Core Philosophy` section
  - List all 8 core beliefs
  - Attribute to each expert (Zinsser, McPhee, King, etc.)

**Time**: 30 minutes

#### 1.2.3 How to Work With Users Section
- [ ] Write `## How to Work With Users` heading
- [ ] Write subsection: `### 1. Understand the Situation`
  - Questions to ask users
  - How to assess their needs
- [ ] Write subsection: `### 2. Route to Appropriate Workflow`
  - Explain the 4 main workflows

**Time**: 20 minutes

#### 1.2.4 Workflow A: Full Writing Process
- [ ] Write `#### A. Full Writing Process (New Piece)` section
- [ ] Document "For:" use case
- [ ] Write **Steps** with all 5 phases:
  - [ ] 1. Intent Discovery (with questions and techniques)
  - [ ] 2. Structural Architecture (reference structure-types.md)
  - [ ] 3. Drafting Discipline (techniques and quotas)
  - [ ] 4. Four-Pass Revision (reference revision-guide.md)
  - [ ] 5. Stickiness Check (reference success-model.md)

**Time**: 30 minutes

#### 1.2.5 Workflow B: Revision & Polish
- [ ] Write `#### B. Revision & Polish (Existing Draft)` section
- [ ] Document "For:" use case
- [ ] Write **Steps** with numbered sequence:
  - [ ] Step 1: Read the draft
  - [ ] Step 2: Run analyze-text.py
  - [ ] Step 3: Run detect-clutter.py
  - [ ] Step 4: Guide through four passes (detailed)
    - [ ] Pass 1 - Clutter (tools and targets)
    - [ ] Pass 2 - Cognition (techniques)
    - [ ] Pass 3 - Rhythm (scripts and tools)
    - [ ] Pass 4 - Message (SUCCESs application)
  - [ ] Step 5: Show before/after stats

**Time**: 30 minutes

#### 1.2.6 Workflow C: Structure Planning
- [ ] Write `#### C. Structure Planning` section
- [ ] Document "For:" use case
- [ ] Write **Steps** (1-6):
  - [ ] Understand material and purpose
  - [ ] Reference structure-types.md
  - [ ] Present structure options (list all types)
  - [ ] Sketch 3 blueprints
  - [ ] Help select and annotate
  - [ ] Map gold-coin placement

**Time**: 20 minutes

#### 1.2.7 Workflow D: Stickiness Enhancement
- [ ] Write `#### D. Stickiness Enhancement` section
- [ ] Document "For:" use case
- [ ] Write **Steps** (1-5):
  - [ ] Identify core message
  - [ ] Run success-checker.py
  - [ ] Work through SUCCESs model (all 6 elements)
  - [ ] Score and improve
  - [ ] Rewrite key sections

**Time**: 15 minutes

#### 1.2.8 Techniques & Resources Section
- [ ] Write `### 3. Apply Techniques with References`
- [ ] List resource references:
  - [ ] REFERENCE.md (when to use)
  - [ ] revision-guide.md (when to use)
  - [ ] structure-types.md (when to use)
  - [ ] success-model.md (when to use)
  - [ ] examples.md (when to use)
  - [ ] checklists.md (when to use)
- [ ] List script references:
  - [ ] analyze-text.py (what and when)
  - [ ] detect-clutter.py (what and when)
  - [ ] sentence-variety.py (what and when)
  - [ ] success-checker.py (what and when)

**Time**: 15 minutes

#### 1.2.9 Coaching Style Section
- [ ] Write `### 4. Coaching Style`
- [ ] List coaching principles (4-5 bullet points)
- [ ] Add example coaching questions (4-6 questions)

**Time**: 10 minutes

#### 1.2.10 Techniques Quick Reference
- [ ] Write `## Techniques Quick Reference` section
- [ ] Create subsection for each expert:
  - [ ] McPhee's Structural Diagramming (1-2 sentences + reference)
  - [ ] Zinsser's Clarity Toolkit (1-2 sentences + reference)
  - [ ] King's Revision Formula (1-2 sentences + reference)
  - [ ] Lamott's Process Philosophy (1-2 sentences + reference)
  - [ ] Pinker's Cognitive Load Principles (1-2 sentences + reference)
  - [ ] Clark's Newsroom Techniques (1-2 sentences + reference)
  - [ ] Klinkenborg's Sentence Work (1-2 sentences + reference)
  - [ ] Heath's SUCCESs Model (1-2 sentences + reference)

**Time**: 20 minutes

#### 1.2.11 Analysis Tools Section
- [ ] Write `## Analysis Tools Available` section
- [ ] Document each script:
  - [ ] analyze-text.py (What, When, Output)
  - [ ] detect-clutter.py (What, When, Output)
  - [ ] sentence-variety.py (What, When, Output)
  - [ ] success-checker.py (What, When, Output)

**Time**: 15 minutes

#### 1.2.12 Example Session
- [ ] Write `## Example Session: Revision` section
- [ ] Create realistic dialogue showing:
  - [ ] User request
  - [ ] Initial assessment
  - [ ] Running scripts
  - [ ] Guiding through passes
  - [ ] Final results with stats
- [ ] Make it concrete and actionable

**Time**: 20 minutes

#### 1.2.13 Indexes
- [ ] Write `## Resources Index` section
  - [ ] List all 6 resource files with descriptions
- [ ] Write `## Scripts Index` section
  - [ ] List all 4 scripts with descriptions
- [ ] Add closing statement about referencing resources

**Time**: 10 minutes

#### 1.2.14 Review & Polish SKILL.md
- [ ] Read through entire SKILL.md file
- [ ] Check for clarity and concision
- [ ] Verify all resource references are correct
- [ ] Ensure YAML frontmatter is valid
- [ ] Test that file is well-structured
- [ ] Verify length is appropriate (aim for 2000-3000 words)

**Time**: 15 minutes

**Total Phase 1 Time**: 3-4 hours

---

## Phase 2: Resources (3-4 hours)

### 2.1 Create REFERENCE.md (Comprehensive Guide)

- [ ] Create `skills/writer/resources/REFERENCE.md`
- [ ] Write introduction explaining purpose of this reference
- [ ] Create section: `## The 8 Core Influences`
  - [ ] Brief intro to each expert

**Time**: 15 minutes

#### 2.1.1 McPhee's Structural Diagramming
- [ ] Write `## John McPhee: Structural Architecture`
- [ ] Explain philosophy: structure is invisible but essential
- [ ] Describe his method:
  - [ ] Learned from Mrs. McKee
  - [ ] Blueprint before drafting
  - [ ] Structure arises from material, not imposed
- [ ] Explain key structure types:
  - [ ] Dual profile structure
  - [ ] Triple profile structure
  - [ ] Circular/cyclical structure
  - [ ] Other diagram types
- [ ] Provide guidelines for creating diagrams
- [ ] Add examples (text-based descriptions)

**Time**: 30 minutes

#### 2.1.2 Zinsser's Clarity Principles
- [ ] Write `## William Zinsser: Clarity and Simplicity`
- [ ] Explain philosophy: clarity over ornament
- [ ] Document clarity toolkit:
  - [ ] Kill adverbs
  - [ ] Remove qualifiers
  - [ ] Eliminate bureaucratese
  - [ ] Prefer Anglo-Saxon over Latinate
  - [ ] Concrete over abstract
- [ ] Provide examples for each principle
- [ ] Add "clutter words" list

**Time**: 25 minutes

#### 2.1.3 King's Discipline & Revision
- [ ] Write `## Stephen King: Disciplined Process`
- [ ] Explain philosophy: volume builds instinct
- [ ] Document drafting approach:
  - [ ] Write with door closed
  - [ ] First draft for discovery
  - [ ] Sensory grounding
  - [ ] Concrete nouns, strong verbs
- [ ] Document revision formula:
  - [ ] 2nd draft = 1st draft - 10-25%
  - [ ] How to cut effectively
- [ ] Provide examples

**Time**: 25 minutes

#### 2.1.4 Lamott's Process Compassion
- [ ] Write `## Anne Lamott: Creative Psychology`
- [ ] Explain philosophy: mess first, refine later
- [ ] Document "shitty first draft" concept
- [ ] Explain door closed vs. door open
- [ ] Discuss creative psychology principles
- [ ] Provide encouragement framework

**Time**: 20 minutes

#### 2.1.5 Pinker's Cognitive Science
- [ ] Write `## Steven Pinker: Reader Cognition`
- [ ] Explain philosophy: reduce cognitive load
- [ ] Document key principles:
  - [ ] Signal topic early
  - [ ] Avoid garden-path sentences
  - [ ] Keep subject-verb-object close
  - [ ] Map coherence via topic chains
  - [ ] Manage working memory load
  - [ ] Pronoun clarity
- [ ] Provide garden-path examples
- [ ] Add parsing load examples

**Time**: 30 minutes

#### 2.1.6 Clark's Newsroom Tactics
- [ ] Write `## Roy Peter Clark: Newsroom Tools`
- [ ] Explain philosophy: tools not rules
- [ ] Document techniques:
  - [ ] Gold-coin moments (detailed)
  - [ ] Nut graf placement
  - [ ] Ladder of abstraction
  - [ ] Sentence length variation
  - [ ] Strong endings
- [ ] Provide examples of gold coins
- [ ] Add newsroom rules of thumb

**Time**: 25 minutes

#### 2.1.7 Klinkenborg's Sentence Work
- [ ] Write `## Verlyn Klinkenborg: Sentence as Thought`
- [ ] Explain philosophy: see clearly, write clearly
- [ ] Document principles:
  - [ ] One sentence = one thought
  - [ ] All writing is revision
  - [ ] Eliminate transitions boldly
  - [ ] Don't save point for end
  - [ ] Read aloud for cadence
  - [ ] Replace placeholder sentences
- [ ] Provide sentence examples
- [ ] Add exercises

**Time**: 25 minutes

#### 2.1.8 Heath's SUCCESs Framework
- [ ] Write `## Chip & Dan Heath: Sticky Messages`
- [ ] Explain philosophy: stickiness is design
- [ ] Document SUCCESs model overview
- [ ] Provide brief explanation of each element
- [ ] Note: detailed breakdown in success-model.md
- [ ] Add famous examples (CSPI popcorn, etc.)

**Time**: 20 minutes

#### 2.1.9 Integration Section
- [ ] Write `## Integrating All Techniques`
- [ ] Explain how techniques work together
- [ ] Show planning phase uses McPhee
- [ ] Show drafting phase uses Lamott/Klinkenborg
- [ ] Show revision uses Zinsser/King/Pinker/Clark
- [ ] Show message phase uses Heath
- [ ] Provide integrated workflow example

**Time**: 20 minutes

#### 2.1.10 Review REFERENCE.md
- [ ] Read through entire file
- [ ] Check for completeness
- [ ] Verify examples are clear
- [ ] Ensure length is 4000-5000 words
- [ ] Polish for clarity

**Time**: 15 minutes

**Subtotal**: 4000-5000 words, ~4 hours

---

### 2.2 Create revision-guide.md (Four-Pass System)

- [ ] Create `skills/writer/resources/revision-guide.md`
- [ ] Write introduction to four-pass approach
- [ ] Explain why multiple passes work better than one

**Time**: 10 minutes

#### 2.2.1 Pass 1: Clutter
- [ ] Write `## Pass 1: Cut Clutter (Zinsser/King)`
- [ ] Explain goal: cut 10-25%
- [ ] Document what to cut:
  - [ ] Adverbs (-ly words)
  - [ ] Qualifiers (very, really, quite)
  - [ ] Passive voice
  - [ ] Weak verbs
  - [ ] Clichés
  - [ ] Throat-clearing
- [ ] Provide before/after examples (3-4 examples)
- [ ] Add checklist for this pass

**Time**: 25 minutes

#### 2.2.2 Pass 2: Cognition
- [ ] Write `## Pass 2: Reduce Cognitive Load (Pinker)`
- [ ] Explain goal: easier reading, less backtracking
- [ ] Document techniques:
  - [ ] Fix garden-path sentences
  - [ ] Signal topic early
  - [ ] Keep subject-verb-object close
  - [ ] Check pronoun clarity
  - [ ] Map topic chains
- [ ] Provide garden-path examples (3-4 examples)
- [ ] Add checklist for this pass

**Time**: 25 minutes

#### 2.2.3 Pass 3: Rhythm
- [ ] Write `## Pass 3: Improve Rhythm (Clark)`
- [ ] Explain goal: better flow and engagement
- [ ] Document techniques:
  - [ ] Vary sentence length
  - [ ] End sentences with strong words
  - [ ] Add gold-coin moments
  - [ ] Use ladder of abstraction
  - [ ] Check for monotony
- [ ] Provide rhythm examples (3-4 examples)
- [ ] Add checklist for this pass

**Time**: 25 minutes

#### 2.2.4 Pass 4: Message
- [ ] Write `## Pass 4: Enhance Message (Heath)`
- [ ] Explain goal: make it stick
- [ ] Document SUCCESs application in revision
- [ ] Reference success-model.md for details
- [ ] Provide stickiness examples (2-3 examples)
- [ ] Add checklist for this pass

**Time**: 20 minutes

#### 2.2.5 Complete Example
- [ ] Write `## Complete Four-Pass Example`
- [ ] Show a paragraph going through all 4 passes
- [ ] Annotate what changed in each pass
- [ ] Show final before/after comparison
- [ ] Include statistics (word count reduction, etc.)

**Time**: 20 minutes

#### 2.2.6 Review revision-guide.md
- [ ] Read through entire file
- [ ] Verify examples are clear
- [ ] Check checklists are complete
- [ ] Ensure 1500-2000 words
- [ ] Polish for clarity

**Time**: 10 minutes

**Subtotal**: 1500-2000 words, ~2 hours

---

### 2.3 Create structure-types.md (McPhee's Diagrams)

- [ ] Create `skills/writer/resources/structure-types.md`
- [ ] Write introduction to structural diagramming
- [ ] Explain McPhee's philosophy: invisible but essential

**Time**: 10 minutes

#### 2.3.1 Document Structure Types
- [ ] Write `## Structure Types Overview`
- [ ] Create section: `### 1. List Structure`
  - [ ] When to use
  - [ ] How it works
  - [ ] Diagram (text/ASCII)
  - [ ] Example use case
- [ ] Create section: `### 2. Chronological Structure`
  - [ ] When to use, how it works, diagram, example
- [ ] Create section: `### 3. Dual Profile Structure`
  - [ ] When to use, how it works, diagram, example
- [ ] Create section: `### 4. Triple Profile Structure`
  - [ ] When to use, how it works, diagram, example
- [ ] Create section: `### 5. Circular/Cyclical Structure`
  - [ ] When to use, how it works, diagram, example
- [ ] Create section: `### 6. Pyramid Structure`
  - [ ] When to use, how it works, diagram, example
- [ ] Create section: `### 7. Parallel Narratives`
  - [ ] When to use, how it works, diagram, example

**Time**: 45 minutes

#### 2.3.2 How to Create Your Own
- [ ] Write `## Creating Your Own Structure Diagram`
- [ ] Provide step-by-step process:
  - [ ] Step 1: Understand your material
  - [ ] Step 2: Identify natural organizing principle
  - [ ] Step 3: Sketch 3 different options
  - [ ] Step 4: Annotate with gold-coin placement
  - [ ] Step 5: Select structure that serves content
- [ ] Add examples of the process

**Time**: 20 minutes

#### 2.3.3 Gold-Coin Placement Strategy
- [ ] Write `## Gold-Coin Placement Strategy`
- [ ] Explain Clark's gold-coin concept
- [ ] Show how to map gold coins onto structure
- [ ] Provide examples of good placement
- [ ] Warn against top-heavy structures

**Time**: 15 minutes

#### 2.3.4 Structure Selection Criteria
- [ ] Write `## How to Select the Right Structure`
- [ ] Provide decision framework
- [ ] Add questions to ask
- [ ] Include examples of good/bad matches

**Time**: 15 minutes

#### 2.3.5 Review structure-types.md
- [ ] Read through entire file
- [ ] Verify all structure types covered
- [ ] Check diagrams are clear
- [ ] Ensure 1500-2000 words
- [ ] Polish for clarity

**Time**: 10 minutes

**Subtotal**: 1500-2000 words, ~2 hours

---

### 2.4 Create success-model.md (SUCCESs Framework)

- [ ] Create `skills/writer/resources/success-model.md`
- [ ] Write introduction to SUCCESs model
- [ ] Explain Heath brothers' research

**Time**: 10 minutes

#### 2.4.1 Document Each Element
- [ ] Write `## S - Simple`
  - [ ] Principle explained
  - [ ] How to apply
  - [ ] Questions to ask
  - [ ] Examples (Golden Rule, etc.)
  - [ ] Common mistakes
- [ ] Write `## U - Unexpected`
  - [ ] Principle explained (surprise + interest)
  - [ ] How to create surprise
  - [ ] Curiosity gap technique
  - [ ] Examples (schema violation)
  - [ ] Common mistakes
- [ ] Write `## C - Concrete`
  - [ ] Principle explained
  - [ ] Sensory details
  - [ ] How to make abstract concrete
  - [ ] Examples
  - [ ] Common mistakes
- [ ] Write `## C - Credible`
  - [ ] Principle explained
  - [ ] Types of credibility
  - [ ] Human-scale statistics
  - [ ] Sinatra Test
  - [ ] Examples
  - [ ] Common mistakes
- [ ] Write `## E - Emotional`
  - [ ] Principle explained
  - [ ] Individual vs. masses
  - [ ] Appeal to identity
  - [ ] Self-interest
  - [ ] Examples
  - [ ] Common mistakes
- [ ] Write `## S - Stories`
  - [ ] Principle explained
  - [ ] Mental simulation
  - [ ] Three plot types (Challenge, Connection, Creativity)
  - [ ] Examples
  - [ ] Common mistakes

**Time**: 60 minutes

#### 2.4.2 Application Guide
- [ ] Write `## How to Apply SUCCESs`
- [ ] Provide step-by-step process
- [ ] Show how to score your message (1-6)
- [ ] Explain how to improve weak elements

**Time**: 15 minutes

#### 2.4.3 Real-World Examples
- [ ] Write `## Real-World Examples`
- [ ] Document CSPI popcorn campaign
- [ ] Document Save the Children approach
- [ ] Document blue eye/brown eye exercise
- [ ] Analyze each with SUCCESs lens

**Time**: 20 minutes

#### 2.4.4 Stickiness Scorecard
- [ ] Write `## Stickiness Scorecard`
- [ ] Create assessment framework
- [ ] Provide scoring rubric
- [ ] Add interpretation guide

**Time**: 15 minutes

#### 2.4.5 Review success-model.md
- [ ] Read through entire file
- [ ] Verify all 6 elements complete
- [ ] Check examples are clear
- [ ] Ensure 1500-2000 words
- [ ] Polish for clarity

**Time**: 10 minutes

**Subtotal**: 1500-2000 words, ~2 hours

---

### 2.5 Create examples.md (Before/After Demonstrations)

- [ ] Create `skills/writer/resources/examples.md`
- [ ] Write introduction explaining purpose

**Time**: 5 minutes

#### 2.5.1 Clutter Examples
- [ ] Write `## Clutter Removal Examples`
- [ ] Create 4-5 before/after pairs:
  - [ ] Adverb removal example
  - [ ] Qualifier removal example
  - [ ] Passive to active voice example
  - [ ] Weak verb replacement example
  - [ ] Combined clutter example
- [ ] Annotate each showing what changed and why

**Time**: 30 minutes

#### 2.5.2 Cognitive Load Examples
- [ ] Write `## Cognitive Load Reduction Examples`
- [ ] Create 3-4 before/after pairs:
  - [ ] Garden-path sentence fixes
  - [ ] Subject-verb-object proximity
  - [ ] Topic signaling
  - [ ] Pronoun clarity
- [ ] Annotate showing improvement in readability

**Time**: 25 minutes

#### 2.5.3 Rhythm Examples
- [ ] Write `## Sentence Rhythm Examples`
- [ ] Create 3-4 before/after pairs:
  - [ ] Monotonous to varied rhythm
  - [ ] Weak to strong endings
  - [ ] Adding gold-coin moments
- [ ] Show sentence length patterns

**Time**: 20 minutes

#### 2.5.4 Stickiness Examples
- [ ] Write `## Stickiness Enhancement Examples`
- [ ] Create 3-4 before/after pairs for:
  - [ ] Simple (core message)
  - [ ] Unexpected (adding surprise)
  - [ ] Concrete (abstract to sensory)
  - [ ] Emotional (making them care)
- [ ] Annotate with SUCCESs analysis

**Time**: 30 minutes

#### 2.5.5 Complete Piece Transformations
- [ ] Write `## Complete Transformation Examples`
- [ ] Create 2 full examples:
  - [ ] Example 1: Blog post paragraph (original → final)
  - [ ] Example 2: Essay opening (original → final)
- [ ] Show all four passes
- [ ] Annotate each change
- [ ] Include before/after statistics

**Time**: 40 minutes

#### 2.5.6 Review examples.md
- [ ] Read through entire file
- [ ] Verify examples are diverse
- [ ] Check annotations are helpful
- [ ] Ensure 2000-3000 words
- [ ] Polish for clarity

**Time**: 10 minutes

**Subtotal**: 2000-3000 words, ~2.5 hours

---

### 2.6 Create checklists.md (Quick References)

- [ ] Create `skills/writer/resources/checklists.md`
- [ ] Write introduction explaining use of checklists

**Time**: 5 minutes

#### 2.6.1 Create All Checklists
- [ ] Write `## Intent Discovery Checklist`
  - [ ] 8-10 checkbox items covering core promise, audience, stakes
- [ ] Write `## Structure Planning Checklist`
  - [ ] 8-10 checkbox items covering diagram creation, blueprint selection
- [ ] Write `## Drafting Session Checklist`
  - [ ] 8-10 checkbox items covering setup, techniques, quotas
- [ ] Write `## Revision Checklist - Pass 1: Clutter`
  - [ ] 10-12 checkbox items for clutter detection and removal
- [ ] Write `## Revision Checklist - Pass 2: Cognition`
  - [ ] 8-10 checkbox items for readability improvements
- [ ] Write `## Revision Checklist - Pass 3: Rhythm`
  - [ ] 8-10 checkbox items for flow and variety
- [ ] Write `## Revision Checklist - Pass 4: Message`
  - [ ] 6 checkbox items for SUCCESs
- [ ] Write `## Stickiness Checklist (SUCCESs)`
  - [ ] 6 sections, 2-3 questions each
- [ ] Write `## Pre-Publishing Checklist`
  - [ ] 12-15 checkbox items for final review

**Time**: 45 minutes

#### 2.6.2 Review checklists.md
- [ ] Read through all checklists
- [ ] Verify completeness
- [ ] Check for clarity
- [ ] Ensure 800-1000 words
- [ ] Test with sample writing

**Time**: 10 minutes

**Subtotal**: 800-1000 words, ~1 hour

**Total Phase 2 Time**: 13-14 hours (can be done in 3-4 hour blocks)

---

## Phase 3: Scripts (3-4 hours)

### 3.1 Create analyze-text.py

- [ ] Create `skills/writer/scripts/analyze-text.py`
- [ ] Add shebang: `#!/usr/bin/env python3`
- [ ] Add module docstring with description and usage

**Time**: 5 minutes

#### 3.1.1 Imports and Setup
- [ ] Import sys, re, pathlib
- [ ] Import argparse for CLI
- [ ] Try importing textstat (with fallback if not available)
- [ ] Add constants/configuration

**Time**: 10 minutes

#### 3.1.2 Core Functions
- [ ] Write `count_words(text)` function
- [ ] Write `count_sentences(text)` function
- [ ] Write `count_paragraphs(text)` function
- [ ] Write `analyze_sentences(text)` function
  - [ ] Return list of sentences with lengths
  - [ ] Identify longest sentences
  - [ ] Calculate average
- [ ] Write `calculate_readability(text)` function
  - [ ] Use textstat if available
  - [ ] Simple fallback calculation if not

**Time**: 30 minutes

#### 3.1.3 Output Formatting
- [ ] Write `format_report(stats)` function
  - [ ] Create formatted text report
  - [ ] Include all statistics
  - [ ] Add recommendations based on stats

**Time**: 15 minutes

#### 3.1.4 Main Function and CLI
- [ ] Write `main()` function
  - [ ] Parse command line arguments
  - [ ] Read from file or stdin
  - [ ] Run analysis
  - [ ] Print report
- [ ] Add error handling
- [ ] Add `if __name__ == '__main__':` block
- [ ] Make file executable

**Time**: 15 minutes

#### 3.1.5 Test analyze-text.py
- [ ] Test with sample text file
- [ ] Test with stdin input
- [ ] Verify output is helpful
- [ ] Test error cases
- [ ] Verify statistics are accurate

**Time**: 15 minutes

**Subtotal**: ~1.5 hours

---

### 3.2 Create detect-clutter.py

- [ ] Create `skills/writer/scripts/detect-clutter.py`
- [ ] Add shebang and docstring

**Time**: 5 minutes

#### 3.2.1 Imports and Setup
- [ ] Import sys, re, pathlib, argparse
- [ ] Define clutter word lists:
  - [ ] ADVERB_PATTERN (regex for -ly words)
  - [ ] QUALIFIERS list
  - [ ] PASSIVE_INDICATORS list
  - [ ] WEAK_VERBS list

**Time**: 10 minutes

#### 3.2.2 Detection Functions
- [ ] Write `detect_adverbs(text, line_num)` function
- [ ] Write `detect_qualifiers(text, line_num)` function
- [ ] Write `detect_passive_voice(text, line_num)` function
- [ ] Write `detect_weak_verbs(text, line_num)` function
- [ ] Each function returns list of findings with context

**Time**: 40 minutes

#### 3.2.3 Output Formatting
- [ ] Write `format_findings(findings_dict)` function
  - [ ] Group by type
  - [ ] Format with line numbers
  - [ ] Add suggestions
  - [ ] Create summary section

**Time**: 15 minutes

#### 3.2.4 Main Function and CLI
- [ ] Write `main()` function
  - [ ] Parse arguments (file, verbose flag)
  - [ ] Read file line by line
  - [ ] Run all detectors
  - [ ] Print formatted report
- [ ] Add error handling
- [ ] Make executable

**Time**: 15 minutes

#### 3.2.5 Test detect-clutter.py
- [ ] Test with cluttered text sample
- [ ] Verify all detection types work
- [ ] Check line numbers are accurate
- [ ] Test verbose mode
- [ ] Verify suggestions are helpful

**Time**: 15 minutes

**Subtotal**: ~1.5 hours

---

### 3.3 Create sentence-variety.py

- [ ] Create `skills/writer/scripts/sentence-variety.py`
- [ ] Add shebang and docstring

**Time**: 5 minutes

#### 3.3.1 Imports and Setup
- [ ] Import sys, re, pathlib, argparse
- [ ] Import collections for histogram

**Time**: 5 minutes

#### 3.3.2 Analysis Functions
- [ ] Write `parse_sentences(text)` function
  - [ ] Split into sentences
  - [ ] Count words in each
  - [ ] Return list of (sentence, length, line_num)
- [ ] Write `create_histogram(lengths)` function
  - [ ] Create length distribution
  - [ ] Group into buckets (0-10, 11-20, etc.)
- [ ] Write `detect_monotony(sentences)` function
  - [ ] Find consecutive similar-length sentences
  - [ ] Flag patterns of 5+
- [ ] Write `calculate_variety_score(lengths)` function
  - [ ] Use standard deviation
  - [ ] Score 1-10

**Time**: 40 minutes

#### 3.3.3 Output Formatting
- [ ] Write `format_histogram(histogram)` function
  - [ ] Create ASCII bar chart
- [ ] Write `format_report(analysis)` function
  - [ ] Show distribution
  - [ ] Show statistics
  - [ ] Show monotony warnings
  - [ ] Add recommendations

**Time**: 20 minutes

#### 3.3.4 Main Function
- [ ] Write `main()` function
  - [ ] Parse arguments
  - [ ] Read file
  - [ ] Run analysis
  - [ ] Print report
- [ ] Add error handling
- [ ] Make executable

**Time**: 10 minutes

#### 3.3.5 Test sentence-variety.py
- [ ] Test with varied text
- [ ] Test with monotonous text
- [ ] Verify histogram displays correctly
- [ ] Check monotony detection
- [ ] Verify recommendations

**Time**: 15 minutes

**Subtotal**: ~1.5 hours

---

### 3.4 Create success-checker.py

- [ ] Create `skills/writer/scripts/success-checker.py`
- [ ] Add shebang and docstring

**Time**: 5 minutes

#### 3.4.1 Imports and Setup
- [ ] Import sys, pathlib, argparse
- [ ] Define SUCCESS_QUESTIONS data structure
  - [ ] For each element (S, U, C, C, E, S)
  - [ ] Questions to ask
  - [ ] Scoring criteria

**Time**: 15 minutes

#### 3.4.2 Interactive Functions
- [ ] Write `ask_question(question)` function
  - [ ] Display question
  - [ ] Get user input
  - [ ] Return response
- [ ] Write `assess_element(element_name, questions)` function
  - [ ] Ask all questions for element
  - [ ] Calculate score
  - [ ] Return score and notes
- [ ] Write `calculate_overall_score(element_scores)` function
- [ ] Write `generate_recommendations(element_scores)` function
  - [ ] Identify weak elements
  - [ ] Suggest specific improvements

**Time**: 40 minutes

#### 3.4.3 Output Formatting
- [ ] Write `format_element_result(element, score, notes)` function
- [ ] Write `format_final_report(scores, recommendations)` function
  - [ ] Show individual scores
  - [ ] Show total score
  - [ ] Show overall assessment
  - [ ] List recommendations

**Time**: 20 minutes

#### 3.4.4 Main Function
- [ ] Write `main()` function
  - [ ] Parse arguments (optional file to read first)
  - [ ] Display intro
  - [ ] Walk through each element
  - [ ] Generate final report
  - [ ] Option to save results
- [ ] Add error handling
- [ ] Make executable

**Time**: 15 minutes

#### 3.4.5 Test success-checker.py
- [ ] Run interactively with test inputs
- [ ] Verify all questions are asked
- [ ] Check scoring works correctly
- [ ] Verify recommendations are relevant
- [ ] Test with file input

**Time**: 20 minutes

**Subtotal**: ~2 hours

**Total Phase 3 Time**: ~6.5 hours (can optimize to 3-4 hours)

---

## Phase 4: Testing & Refinement (1-2 hours)

### 4.1 Integration Testing

- [ ] Create test directory with sample texts
- [ ] Test complete workflow with real writing sample:
  - [ ] Start with rough draft
  - [ ] Run analyze-text.py on original
  - [ ] Run detect-clutter.py
  - [ ] Apply Pass 1 revisions
  - [ ] Run sentence-variety.py
  - [ ] Apply Pass 3 revisions
  - [ ] Run success-checker.py
  - [ ] Apply Pass 4 revisions
  - [ ] Run analyze-text.py on final
  - [ ] Compare before/after

**Time**: 30 minutes

### 4.2 Resource Testing

- [ ] Verify all resource file references in SKILL.md are correct
- [ ] Check that REFERENCE.md is comprehensive
- [ ] Confirm revision-guide.md has all techniques
- [ ] Verify structure-types.md has clear diagrams
- [ ] Check success-model.md covers all elements
- [ ] Ensure examples.md has good variety
- [ ] Confirm checklists.md is complete

**Time**: 20 minutes

### 4.3 Documentation Review

- [ ] Read through SKILL.md completely
  - [ ] Check YAML frontmatter is valid
  - [ ] Verify all workflows are clear
  - [ ] Ensure all resources are referenced
  - [ ] Confirm example session is realistic
- [ ] Verify all resource files are well-written
- [ ] Check all scripts have good docstrings
- [ ] Ensure consistent tone throughout

**Time**: 30 minutes

### 4.4 Bug Fixes and Polish

- [ ] Fix any issues found during testing
- [ ] Polish unclear sections
- [ ] Improve examples if needed
- [ ] Optimize script performance
- [ ] Add any missing error handling

**Time**: 20 minutes

### 4.5 Final Checklist

- [ ] All files created in correct locations
- [ ] SKILL.md has valid YAML frontmatter
- [ ] All resource files are complete
- [ ] All scripts are executable
- [ ] All scripts handle errors gracefully
- [ ] Documentation is clear and helpful
- [ ] Examples are concrete and useful
- [ ] Checklists are actionable
- [ ] File sizes are reasonable
- [ ] No broken references

**Time**: 10 minutes

**Total Phase 4 Time**: 1-2 hours

---

## Summary

### Total Checklist Items: ~200+

### Total Estimated Time: 10-14 hours

**Phase Breakdown**:
- Phase 1 (Setup & SKILL.md): 3-4 hours
- Phase 2 (Resources): 3-4 hours
- Phase 3 (Scripts): 3-4 hours
- Phase 4 (Testing): 1-2 hours

### Files to Create: 11 files

1. `skills/writer/SKILL.md` (2000-3000 words)
2. `skills/writer/resources/REFERENCE.md` (4000-5000 words)
3. `skills/writer/resources/revision-guide.md` (1500-2000 words)
4. `skills/writer/resources/structure-types.md` (1500-2000 words)
5. `skills/writer/resources/success-model.md` (1500-2000 words)
6. `skills/writer/resources/examples.md` (2000-3000 words)
7. `skills/writer/resources/checklists.md` (800-1000 words)
8. `skills/writer/scripts/analyze-text.py` (~150-200 lines)
9. `skills/writer/scripts/detect-clutter.py` (~200-250 lines)
10. `skills/writer/scripts/sentence-variety.py` (~150-200 lines)
11. `skills/writer/scripts/success-checker.py` (~250-300 lines)

### Progress Tracking

- [ ] Phase 1 Complete (SKILL.md)
- [ ] Phase 2 Complete (All resources)
- [ ] Phase 3 Complete (All scripts)
- [ ] Phase 4 Complete (Testing & polish)
- [ ] Final Review Complete
- [ ] Skill Ready to Use!

---

## Notes

- Each checkbox represents a discrete task
- Time estimates are approximate
- Can work on resources in parallel if desired
- Scripts can be built incrementally
- Test early and often
- Refer to corrected implementation plan for details
- Use research-findings.md for content details

**Ready to start building!**
