---
name: section-break-check
description: Verifies the section-break style in a substacker draft matches the post register — asterisks (* * *) for essayistic posts under 2500 words, H2 for methodology / how-to / technical posts. Flags mixed registers (H2 in a reflective essay, asterisks in a structured how-to). Per the style-guide rhythm rule. Use every draft. Trigger keywords: section break, asterisk, H2, headers, register, essayistic vs methodology.
---

# Section Break Check

## Table of Contents

- [The two registers](#the-two-registers)
- [Workflow](#workflow)
- [Worked example](#worked-example)
- [Guardrails](#guardrails)

**Related skills:** Called by Editor in structural pass. Reads `shared-context/style-guide.md` for the break rule.

## The two registers

From `style-guide.md`:

- **Essays (<1500 words, reflective register)**: no H1/H2 in body; use `* * *` between movements.
- **Essays (1500+ words)**: `* * *` preferred; H2 only if structured as a how-to.
- **Methodology / technical posts**: H2 is fine and often necessary.
- **Never use H3 or H4.**

How to detect register:

- **Reflective**: first-person throughout, confession or admission opener, narrative arc, no numbered steps, no code blocks, <2500 words.
- **Methodology**: numbered steps, code blocks, command invocations, technical diagrams, "how to X" or "building Y" framing.
- **Hybrid** (e.g., *Architecture, Not Prompting*): both analytical claim and how-to sections. H2 is acceptable here.

## Workflow

```
Section-break check draft D:
- [ ] Step 1: Detect register: reflective | methodology | hybrid
- [ ] Step 2: Scan for section breaks: count H1s, H2s, H3+, asterisk dividers
- [ ] Step 3: Apply register-appropriate rules
- [ ] Step 4: Flag mismatches
```

### Scoring matrix

| Register | Word count | H2 OK? | `* * *` OK? | Flag conditions |
|---|---|---|---|---|
| Reflective | <1500 | No | Yes | H2 in body → tier-2 |
| Reflective | 1500–2500 | Avoid | Preferred | Frequent H2 → tier-2 |
| Hybrid | any | Yes | Yes | Mixing both in same section → tier-2 |
| Methodology | any | Yes | Rare | H3+ usage → tier-2 |

## Worked example

**Draft 1**: A 1200-word reflective essay on pathology AI with H2s (`## The Training Set`, `## The Failure`, `## What I Learned`).

**Flag**: (Tier-2) H2s in a short reflective post break register. Essays under 1500 words use `* * *`. Rewrite: replace each `## Heading` with `* * *` and fold the heading concept into the first sentence of the new movement.

**Draft 2**: A 3000-word methodology post on building an agent system with no H2s, only `* * *` dividers.

**Flag**: (Tier-2) Methodology register typically uses H2 for navigation. Consider H2 for each major step of the build. Not blocking, but worth the writer's attention.

**Draft 3**: A 1800-word essay mixing analysis with a concrete build walk-through, with both H2 and `* * *` (some sections have H2, some have asterisks).

**Flag**: (Tier-2) Mixing within one essay breaks register. Pick one. Rewrite suggestion: use H2 for the methodology sections and `* * *` for the analytical transitions — but be consistent within each register.

## Guardrails

1. Section-break issues are tier-2. Writer can publish anyway; it's a craft miss, not a voice violation.
2. Don't flag H1 in the draft — H1 is the post title and belongs there.
3. Don't flag section breaks in code blocks or quoted content.
4. H3+ is always flagged (style-guide rule: "Never use H3 or H4").
5. Series-log posts (frontmatter `series: {slug}`) typically use `* * *` — if a series post uses H2, flag softly.
6. Don't propose a full restructure; suggest the one change (replace H2 with `* * *` or vice versa) and let the writer execute.

## Quick reference

- Detect register → apply rule.
- Two tolerated registers: reflective (asterisks) and methodology (H2).
- Mixed within one essay = tier-2 flag.
