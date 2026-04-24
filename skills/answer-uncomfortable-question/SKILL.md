---
name: answer-uncomfortable-question
description: Takes one strategic question about substacker ("should we launch paid?", "is this section dead?", "are we writing for the wrong audience?") and produces the mandatory evidence + reasoning + downside triad plus a recommendation. Used 3 times per Growth Strategist review. Trigger keywords: uncomfortable question, strategic question, evidence reasoning downside, triad.
---

# Answer Uncomfortable Question

## Workflow

```
Per question:
- [ ] Step 1: Reject if not answerable with current inputs → "I'd like to ask X, but I don't have the data. Here's what to collect before next quarter."
- [ ] Step 2: Gather evidence: numbers, quotes, specific posts. Cite them.
- [ ] Step 3: Write reasoning as a chain: evidence A → inference B → inference C → recommendation
- [ ] Step 4: Write downside: what SPECIFICALLY goes wrong if the recommendation is wrong?
- [ ] Step 5: End with one-line recommendation: do X / don't do X / watch Y
- [ ] Step 6: 200-400 words per question
```

## Uncomfortable-question selection criteria

The Strategist chooses 3 per quarter. Scoring:
1. **Data-backed**: answerable from current inputs. Reject otherwise.
2. **Decision-relevant**: answering it changes what the writer does next quarter.
3. **Recency filter**: don't re-ask last quarter's unresolved question without significant new data.
4. **User-prompted override**: if writer invoked with specific question, force-include it.
5. **Portfolio coverage**: across quarters, hit growth / product / voice axes.

## Format per question

```markdown
### Q{N}: {phrased as a real question, not a topic}
**Evidence**: What the numbers / corpus / audience actually say. Cite Growth Analyst report or specific posts.
**Reasoning**: Why the evidence leads to {answer}. Chain: A → B → C.
**Downside**: What specifically breaks if this recommendation is wrong.
**Recommendation**: Do X / Don't do X / Watch Y before deciding.
```

## Guardrails

1. Evidence-reasoning-downside triad is mandatory. Missing any → suppress the question.
2. Never fabricate evidence. If the data doesn't exist, reject the question.
3. Downside must be specific. "We lose time" is not a downside; "we lock in a topic the audience has outgrown" is.
4. Recommendation is one line. Not a paragraph of hedging.
5. 200-400 words per question. The full review has 3 questions at ~300 words each.
