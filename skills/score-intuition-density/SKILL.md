---
name: score-intuition-density
description: Computes a 0-10 intuition-density score for a seed body using 8 concrete measurable signals — analogy presence, concrete worked example, counterfactual offered, reframe against default, biology-to-AI transfer, question posed, calibrated hedge, math-to-metaphor handoff. Emits both the numeric score and the list of triggered signals for auditability. Use after topic tagging to enrich seed frontmatter in the substacker Librarian pipeline. Trigger keywords: intuition density, score, signals, analogy count, worked example, density proxy.
---

# Score Intuition Density

## Table of Contents

- [The 8 signals](#the-8-signals)
- [Workflow](#workflow)
- [Worked example](#worked-example)
- [Guardrails](#guardrails)

**Related skills:** Called by `ingest-inbox-item` step 3. Reads `shared-context/style-guide.md` (for em-dash reframe pattern). The score enters the seed's frontmatter as `intuition_density.score`; the triggered signals are recorded as `intuition_density.signals`.

## The 8 signals

Each signal is detected by a concrete pattern (not "LLM vibes"). Weighted sum, clamped to [0, 10].

| Signal | Detection rule | Weight |
|---|---|---|
| `analogy_present` | explicit "like", "think of it as", "is secretly", "is to X what Y is to Z", em-dash reframe | 2 |
| `concrete_worked_example` | numbered or named instance with specific numbers / entities (names a system, shows arithmetic) | 2 |
| `counterfactual_offered` | "if it were X instead", "unlike Y", "this is why Z doesn't work" | 1 |
| `reframe_against_default` | "not X — Y", "people say X but", em-dash reframe | 1 |
| `biology_to_ai` | biology vocabulary (antibody, neuron, immune, evolution, synapse, crypt, DNA) in an AI context | 1 |
| `question_posed` | interrogative sentence that drives the piece forward | 1 |
| `hedge_calibrated` | "I do not know", "I am not sure", explicit uncertainty with scope | 1 |
| `math_to_metaphor_handoff` | equation or formal statement followed by prose restatement | 1 |

**Max weight sum**: 10. **Min**: 0.

## Workflow

```
Score one seed body:
- [ ] Step 1: Run each of the 8 detection patterns over body + title
- [ ] Step 2: For each signal that fires, record in signals list
- [ ] Step 3: Sum weights; clamp to [0, 10]
- [ ] Step 4: Return {score: int, signals: [str]}
```

### Detection details

- `analogy_present`: regex for the markers above, AND the analogy must map source → target (a simile that names only one side doesn't count).
- `concrete_worked_example`: presence of numbers + a named entity. "3B params", "$11.35", "fifty queries" — yes. "a model" — no.
- `counterfactual_offered`: look for the 3 phrase patterns above, OR an explicit if-not construction.
- `reframe_against_default`: em-dash reframe pattern (`X — actually Y`) or explicit "not X / rather Y".
- `biology_to_ai`: biology vocabulary present AND the essay is an AI/ML context (inferred from body topic tags if available).
- `question_posed`: ?-terminated sentence that is not rhetorical filler. Excludes questions in a quoted Q&A format.
- `hedge_calibrated`: "I do not know" (full sentence, not "I don't know what to order for dinner"), "I am not claiming", "I can't prove", specific-scope hedges ("on n=1", "in the three teams I've tested").
- `math_to_metaphor_handoff`: inline math/equation/formal statement (LaTeX or prose-math) followed within 2 sentences by a prose restatement.

## Worked example

**Input body** (dropout-as-ensemble):
> had a thought while running — dropout is secretly an ensemble method. each forward pass is a different sub-network. so at test time when you turn dropout off and scale, you're averaging predictions across exponentially many thinned networks. this is why it generalizes. not "regularization" in the L2 sense. more like bagging.
> reminds me of how the immune system doesn't pick one antibody — it runs a population and lets the best ones dominate. dropout is antibody diversity for weights.

**Detection run**:
- `analogy_present` — fires (`dropout is antibody diversity for weights`). +2
- `concrete_worked_example` — fires (`each forward pass is a different sub-network`, specific mechanism). +2
- `counterfactual_offered` — fires (`not "regularization" in the L2 sense`). +1
- `reframe_against_default` — fires (`more like bagging`, reframe against "regularization"). +1
- `biology_to_ai` — fires (immune system / antibody). +1
- `question_posed` — no.
- `hedge_calibrated` — no.
- `math_to_metaphor_handoff` — no.

**Output**: `{score: 7, signals: [analogy_present, concrete_worked_example, counterfactual_offered, reframe_against_default, biology_to_ai]}`.

## Guardrails

1. Signals must be detectable by regex/substring heuristics — never "LLM vibes." Every signal has a concrete pattern.
2. Score is meaningful for ranking, not absolute truth. 3 vs. 4 is noise; 3 vs. 8 is real signal.
3. Do not penalize for length. A 100-word note can score 8.
4. Do not score link-captures with `low_commentary: true` above 3 (capped by caller).
5. Never use the score to auto-kill or auto-promote a seed. The writer decides.
6. Preserve the signals list. The score without the signals is unauditable.

## Quick reference

- 8 signals. Max weight 10. Output: `{score, signals}`.
- Deterministic: same body → same score + signals.
- Runs after tagging, before dedupe.
