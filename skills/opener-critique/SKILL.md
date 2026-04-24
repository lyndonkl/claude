---
name: opener-critique
description: Evaluates the first 1-3 sentences of a substacker draft against the writer's signature opener patterns — confession / "I hadn't done X" / reframe / small concrete admission. Classifies opener as confession | reframe | admission | news-hook | generic-opener and flags news-hook/generic as tier-1. The opener sets the voice contract for the essay. Use on every draft. Trigger keywords: opener, hook, first sentence, opening, confession opener, news hook, generic opener.
---

# Opener Critique

## Table of Contents

- [Classifier](#classifier)
- [Workflow](#workflow)
- [Worked example](#worked-example)
- [Guardrails](#guardrails)

**Related skills:** Called by Editor in structural pass. Sets tone contract; downstream skills (`voice-check`, `slop-detector` S1) can reference its classification.

## Classifier

| Class | Markers | Voice verdict |
|---|---|---|
| **confession** | `I hadn't`, `I used to think`, `I did not know`, `Until last week`, `I spent three hours`, `I was wrong about` | PASS |
| **reframe** | `X is commonly called Y — actually Z`, `Most people think X; actually Y` | PASS |
| **admission** | `I substitute learning for doing`, `I have been meaning to`, `I have opinions about X — the kind that feel like knowledge` | PASS |
| **puzzle** (biology cold open) | Biological/systems question opened with a specific number or contradiction | PASS |
| **epistolary** | `Dear friend`, `Dear reader`, second-person address to a specific imagined reader | PASS (rare but valid) |
| **news-hook** | `GPT-5 launched`, `Last week OpenAI`, `With the release of X`, reacting to an external event | **FLAG tier-1** |
| **generic-opener** | `AI is transforming`, `In a world where`, `In today's fast-paced`, `As we enter a new era` | **FLAG tier-1** |

## Workflow

```
Evaluate opener:
- [ ] Step 1: Extract first 1-3 sentences
- [ ] Step 2: Match against classifier marker lists
- [ ] Step 3: Assign class
- [ ] Step 4: Write one-line justification
- [ ] Step 5: If news-hook or generic-opener, produce 2 rewrite options in the confession/admission register
```

## Worked example

**Draft opener** (bad): "In today's rapidly evolving AI landscape, teams face a critical choice between RAG and fine-tuning for domain knowledge."

**Classification**: generic-opener. Tier-1.

**Rewrites**:
- (a) "I spent four months trying to make a RAG demo not lie. The model was never the problem."
- (b) "I had not shipped a fine-tune until last quarter. I assumed the model was the hard part. It wasn't."

**Draft opener** (good): "I spent a week re-prompting a customer-service agent before I realised the agent was the wrong unit of analysis."

**Classification**: confession (`I spent`, `I realised`). PASS.

**Draft opener** (puzzle — valid): "Your immune system can recognize roughly ten trillion distinct molecular threats. It does this with a genome that contains fewer than twenty thousand protein-coding genes. The math should not work."

**Classification**: puzzle. PASS.

## Guardrails

1. First 3 sentences only. If the writer's opener is 1 sentence, use that alone.
2. Never rewrite the opener beyond 2 suggested options, each ≤2 sentences.
3. News-hook and generic-opener are automatic tier-1. Never soften.
4. If the opener is borderline (e.g., an admission that's ALMOST generic), default to PASS and note as candidate for Editor's drift review.
5. Series-log posts often open with the scoreboard or a direct match reference — that's admission-adjacent, accept.
6. Epistolary register is valid but RARE. Flag if the writer uses it more than 1 in 10 posts.

## Quick reference

- Input: first 3 sentences of draft.
- Output: classification + verdict (PASS / FLAG tier-1) + rewrites if flagged.
- Seven classes: confession, reframe, admission, puzzle, epistolary (all pass); news-hook, generic-opener (flag).
