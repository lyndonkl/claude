---
name: memory-retrieval-learning
description: Creates evidence-based learning plans that maximize long-term retention through spaced repetition, retrieval practice, interleaving, and elaboration. Guides through goal definition, material breakdown, review scheduling, and progress tracking. Use when long-term knowledge retention is needed, studying for exams or certifications, learning new job skills or technology, mastering substantial material, combating forgetting, or when user mentions studying, memorizing, learning plans, spaced repetition, flashcards, active recall, or durable learning.
---

# Memory, Retrieval & Learning

## Table of Contents
- [Workflow](#workflow)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Workflow

Copy this checklist and track your progress:

```
Learning Plan Progress:
- [ ] Step 1: Define learning goals and timeline
- [ ] Step 2: Break down material and create schedule
- [ ] Step 3: Design retrieval practice methods
- [ ] Step 4: Execute daily learning sessions
- [ ] Step 5: Track progress and adjust
```

**Step 1: Define learning goals and timeline**

Clarify what needs to be learned, by when, and how much time is available daily. Identify success criteria (pass exam, demonstrate skill, etc). Use [resources/template.md](resources/template.md) to structure your plan.

**Step 2: Break down material and create schedule**

Chunk material into learnable units. Calculate spaced repetition schedule based on timeline. Plan initial learning + review cycles. For complex schedules or long timelines (6+ months), see [resources/methodology.md](resources/methodology.md) for advanced scheduling techniques.

**Step 3: Design retrieval practice methods**

Create active recall mechanisms: flashcards, practice problems, mock tests, self-quizzing. Avoid passive techniques (highlighting, re-reading). See [Common Patterns](#common-patterns) for domain-specific approaches.

**Step 4: Execute daily learning sessions**

Follow the schedule: new material in morning (peak alertness), reviews in afternoon/evening. Use retrieval practice consistently. Log what's difficult for extra review. For advanced techniques like interleaving or desirable difficulties, see [resources/methodology.md](resources/methodology.md).

**Step 5: Track progress and adjust**

Measure retention with self-tests. Adjust review frequency based on performance (struggle more = review sooner). Update schedule as needed. Validate using [resources/evaluators/rubric_memory_retrieval_learning.json](resources/evaluators/rubric_memory_retrieval_learning.json).

## Common Patterns

**Exam Preparation (3-6 months):**
- Phase 1 (60% time): Initial learning + comprehension
- Phase 2 (30% time): Spaced review + retrieval practice
- Phase 3 (10% time): Mock exams + weak area focus
- Use: Professional certifications, academic finals, bar exam

**Language Learning (ongoing):**
- Daily: 10 new vocabulary words + review old words due today
- Weekly: Grammar lesson + interleaved practice with prior lessons
- Monthly: Conversation practice integrating all learned material
- Use: Spanish, Mandarin, French, any language mastery

**Technology/Job Skill (3-12 weeks):**
- Week 1-2: Fundamentals + hands-on practice
- Week 3-6: Advanced concepts + spaced review of fundamentals
- Week 7+: Real projects + systematic review of challenging concepts
- Use: Learning Python, React, AWS, data analysis

**Medical/Technical Procedures:**
- Day 1: Learn procedure steps + immediate practice
- Day 2: Retrieval practice without notes
- Day 4: Practice + add edge cases
- Day 8: Full simulation
- Day 15, 30: Refresh to maintain
- Use: Clinical skills, safety protocols, lab techniques

**Bulk Memorization (facts, dates, lists):**
- Create spaced repetition flashcard deck
- Review cards daily (Anki algorithm or similar)
- Retire cards after 5+ successful recalls
- Add mnemonic devices for difficult items
- Use: Anatomy, geography, historical dates, pharmacology

## Guardrails

**Avoid Common Mistakes:**
- ❌ Passive re-reading or highlighting → Use active retrieval instead
- ❌ Cramming (massed practice) → Use spaced repetition
- ❌ Blocking by topic (all topic A, then all topic B) → Use interleaving
- ❌ Over-confidence after initial learning → Test yourself repeatedly
- ❌ No tracking → Measure retention to adjust schedule

**Realistic Expectations:**
- Forgetting is normal and necessary for strong memory consolidation
- Initial struggles with retrieval are productive ("desirable difficulties")
- Expect 20-40% forgetting between reviews (that's the sweet spot)
- Spaced repetition feels less productive than massing, but works better
- Plan for 2-3x more time than you think you need

**Time Management:**
- Daily consistency > marathon sessions
- Minimum 15-20 min/day more effective than 2 hours weekly
- Peak retention: 25 min study → 5 min break → repeat
- Review sessions should be shorter than initial learning sessions
- Build buffer for life interruptions (illness, travel, deadlines)

**When to Seek Help:**
- Material isn't making sense after 3+ attempts → Get instructor/expert help
- Retention remains below 60% after 3 review cycles → Reassess study method
- Burnout or motivation collapse → Reduce daily load, add intrinsic rewards
- Test anxiety interfering → Address anxiety separately from memory techniques

## Quick Reference

**Resources:**
- `resources/template.md` - Learning plan template with scheduling
- `resources/methodology.md` - Advanced techniques for complex learning goals
- `resources/evaluators/rubric_memory_retrieval_learning.json` - Quality criteria

**Output:**
- File: `memory-retrieval-learning.md` in current directory
- Contains: Learning goals, material breakdown, review schedule, retrieval methods, tracking system

**Success Criteria:**
- Spaced repetition schedule covers entire timeline
- Retrieval practice methods defined for all material types
- Daily time commitment is realistic and sustainable
- Tracking mechanism in place to measure retention
- Schedule includes buffer for setbacks
- Validated against quality rubric (score ≥ 3.5)

**Evidence-Based Techniques:**
1. **Spacing Effect**: Reviews at 1, 3, 7, 14, 30 days
2. **Testing Effect**: Self-test > re-study for long-term retention
3. **Interleaving**: ABCABC > AAABBBCCC for transfer and discrimination
4. **Elaboration**: Connect to prior knowledge, explain to others
5. **Dual Coding**: Combine verbal + visual representations
