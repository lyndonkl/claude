# Methodology: Designing a Rediscovery Walk

Heuristics for the harder design choices in walk construction. Read this when a walk isn't landing and you're not sure why.

## How to choose the seed

A seed is the first sentence of the walk — the door the learner steps through. Three tests for a good seed:

1. **The 30-second test.** Can the learner picture the seed within 30 seconds, with no further setup? If you need to explain notation, define terms, or set context, the seed is too heavy. Find a more concrete one.
2. **The motivation test.** Does the seed make the learner *want* to know the answer? Eigenvectors framed as "directions a transformation leaves alone" is much more motivating than "vectors satisfying Av = λv". The first is a question; the second is a statement.
3. **The reachability test.** Is the formal concept reachable from the seed in 3-5 rungs? If you can't sketch a path, the seed is too far.

A few seed templates that work across many concepts:

- **The leftover question:** "Most X get Y'd. Are there special X that don't?"
  - Eigenvectors: "Most arrows get rotated *and* stretched. Are there ones that only get stretched?"
  - Fixed points: "Most points move under the function. Are there ones that don't?"

- **The natural ingredient question:** "We want to do X. What's the most obvious thing to try? Why does it fail? What might fix it?"
  - Softmax: "Turn scores into probabilities. Just normalize? But scores can be negative…"
  - Layer norm: "Stabilize activations. Just shift them? But scale also drifts…"

- **The anomaly question:** "Here's something that should feel wrong. Why might it be true?"
  - Concentration of measure: "Gaussian samples in high D live on a shell, not near the origin."
  - KL asymmetry: "KL(p‖q) ≠ KL(q‖p). Why on earth would it be asymmetric?"

## How to size a rung

A rung is one question. Two errors are common:

**Rung too big.** The learner stares blankly. Symptom: long pauses, "I'm not sure what you're asking", or worse, silence followed by the learner trying to look up the answer.

**Rung too small.** The walk feels patronizing. Symptom: "obviously…", or the learner skipping ahead and answering the next 2 rungs in one shot.

The goal is what Vygotsky called the zone of proximal development — the rung is *just* beyond what the learner can answer alone, but reachable with the seed and the prior rungs as scaffolding.

Calibration heuristics:

- **First rung:** If the learner doesn't know the rest of the concept yet, the first rung should be answerable from the seed alone, with no prior knowledge.
- **Each subsequent rung:** Should require *only* what was established in the previous rungs.
- **Final rung:** Should produce the formal definition as the answer. Ideally the learner *says* the definition or its equation; the coach only confirms.

If you find a rung the learner can't answer, you've identified a missing intuition. Insert a sub-rung *before* it. The walk often goes: 4-rung plan → walked → discovered missing intuition at rung 3 → 5-rung walk on the rerun.

## How to handle wrong guesses

A wrong guess is diagnostic gold. The temptation is to correct: "no, the answer is X." Resist it.

Instead, *probe the source*: "What made you think that? Let's test it." Three responses cover most cases:

**The guess is partially right.** Affirm the right part, probe the gap.
- *Coach:* "Are there arrows that only get stretched?"
- *Learner:* "Maybe, like (1, 1) for a stretching matrix?"
- *Coach:* "Right intuition — special arrows for special matrices. But (1, 1) won't work for *every* matrix. What property would such an arrow need to have, in general?"

**The guess is plausible but wrong.** Test it on a small example. The example will reveal the problem and produce the next guess.
- *Coach:* "How would you turn (2, 1, -1) into a probability distribution?"
- *Learner:* "Divide by the sum?"
- *Coach:* "Try it — what do you get?"
- *Learner:* "...one of them is negative. So that doesn't work."
- *Coach:* "Right. So we need something else first. What?"

**The guess is fundamentally confused.** This is rare; usually the walk is too far ahead. Back up to the prior rung and try a smaller step.

Never say "no" without a follow-up question. "No" without a probe trains the learner to wait for you to talk.

## When to abandon the walk

Some walks fail. Recognize the failure modes and switch approaches.

**The learner has the answer pre-loaded.** They've memorized the formula and are reciting, not deriving. Symptoms: they jump rungs without reasoning; their answers are formulaic; they can't answer the verification rung from first principles. Switch to the `geometric-algebraic-bridge` skill — they have algebra without geometry, and bridging is more useful than re-walking.

**The learner is missing prerequisites.** They can't answer rung 2 because they don't know what a matrix is, or can't compute a partial derivative. Stop, name the prerequisite, recommend they fix it (or walk *that* concept first), and resume.

**The learner is ahead.** They answer rung 1 with the formal definition. Skip to verification — they may already own the concept and just want confirmation. If verification passes, they were already there; congratulate and offer the next concept. If verification fails, they have recognition not understanding — bridge or apply.

## How to verify ownership

The verification question (Step 6) is the load-bearing element. A walk without verification is performance.

A good verification question has three properties:

1. **Unfamiliar to the walk.** It's not just rung 5 reworded. It's a fresh scenario.
2. **Answerable with the picture, not the formula.** "What are the eigenvectors of a 90° rotation?" is answered geometrically (no real direction is left unrotated), not by computing a characteristic polynomial.
3. **Diagnostic of the picture's depth.** Different wrong answers reveal different gaps.

For the eigenvector walk, "what are the eigenvectors of a 90° rotation?" diagnostics:
- "None — every direction gets rotated." → ✓ owns the geometric picture.
- "I'd compute det(A − λI) = 0." → has the algorithm, not the picture. Insert a geometric coda.
- "(1, 0) and (0, 1)?" → wrong picture. Re-walk with a different angle.

If the verification question has only one good answer ("the eigenvectors are…"), it's not a good verification question — it's a quiz. Reword to require the *reason*, not just the result.

## When walking takes too long

A walk should usually take 5-15 minutes. If it's running longer, one of three things is wrong:

- **Too many rungs.** Cut to 3-5.
- **Coach talking too much.** Aim for 1-2 sentences per turn from the coach. If you're writing paragraphs, you've stopped walking.
- **Wrong walk for this learner.** Some learners genuinely prefer "give me the formula, then explain". Honor that — switch to direct exposition with the `geometric-algebraic-bridge` skill.
