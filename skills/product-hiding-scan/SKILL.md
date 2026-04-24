---
name: product-hiding-scan
description: Scans the substacker published corpus for clusters of posts that could become a product — a course, a book, a cohort, or a consulting offer. Produces at most 2 candidates with evidence + audience signal, or an honest "not yet" verdict if nothing qualifies. Typically fires once the writer has 30+ posts. Trigger keywords: product hiding, course from essays, book from essays, corpus to product, product scan.
---

# Product Hiding Scan

## Workflow

```
Per quarterly run (with corpus ≥30 posts):
- [ ] Step 1: Cluster published corpus by theme (NOT by section — themes may cut across)
- [ ] Step 2: For each cluster with ≥5 posts, check product templates:
    - Course: 5+ posts forming a progression
    - Book: 15+ posts on one theme with coherent through-line
    - Cohort: reader-demand signal in audience-notes
    - Consulting: "can you help me do this" signal
- [ ] Step 3: For each qualifying cluster, write candidate block
- [ ] Step 4: If no cluster qualifies, say so plainly
```

## Product templates

- **Course**: Shaan Puri's Power Writing on Maven — newsletter essays became the course syllabus. 5-8 posts forming a progression with exercises.
- **Book**: Paul Graham's *Hackers & Painters* — ~15 essays on adjacent themes, lightly edited. 15+ posts needed.
- **Cohort / community**: readers write back with their own versions of the problem → peer-learning value.
- **Consulting / advisory**: readers write back with "can you help me do this?" inquiries → productized consult.

## Output per candidate

```markdown
**Theme**: {name}
**Product type**: course | book | cohort | consulting
**Supporting posts**: {slug list}
**Minimum-viable product**: {1-2 sentences}
**Audience signal**: {what in the corpus or audience-notes suggests demand}
**Not yet if**: {the condition that would flip this from candidate to real}
```

## Guardrails

1. Max 2 candidates per review. More than 2 overwhelms.
2. "No product is hiding yet. Come back at 30 posts" is a valid output.
3. Require ≥5 posts on the theme before calling it a course.
4. Require ≥15 posts on the theme before calling it a book.
5. Audience signal is required. A cluster without reader demand is a future possibility, not a current candidate.
6. Never propose a product the writer can't execute in 6 months (cohorts need infrastructure; books need a year).
