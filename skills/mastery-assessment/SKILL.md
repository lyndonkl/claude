---
name: mastery-assessment
description: A closed-book-first probing protocol that assesses how well the learner actually holds a module's claims — asking before telling, probing the gap, detecting misconceptions, then confirming. Tags each probe with a Bloom level, places the learner in a Dreyfus mastery band (unfamiliar/aware/functional/proficient/fluent), scores the session, and schedules the next spaced-repetition surfacing on expanding intervals (1d, 3d, 7d, 16d, 35d) — pulling the next date earlier on a miss. Writes an assessment-session note to assessments/log/ and proposes a review-due update on each evergreen note touched. Use when checking mastery of a module, running a spaced-repetition review, or gating phase progression. Trigger keywords: assess mastery, review-due, spaced repetition, Bloom check, mastery band, am I ready to move on.
---

# Mastery assessment

This skill checks whether the learner *holds* a module's claims — not whether they recognize them. Recognition is cheap and treacherous: a learner reads "heritability is a property of a population, not a trait," nods, and feels they know it. Retrieval is the test. This skill asks the learner to produce the claim, the mechanism, and an application from memory **before** any prompt is shown, then probes exactly where production broke. The retrieval effort is the point, not a side effect — see [[learning-system|LEARNING_SYSTEM.md]] and the desirable-difficulty principle in `conventions.md` §8.

It composes three skills: [[evaluation-rubrics]] supplies the band descriptors and scoring scale, memory-retrieval-learning supplies the spacing schedule and the case for testing-as-encoding, and socratic-teaching-scaffolds supplies the question ladder used to probe a gap without lecturing the answer back in.

This is an **assessment**, not a tutoring session. The job is to measure and schedule, not to teach. When a gap is found, probe it once or twice to characterize it, then record it — do not slide into a lecture. The reading loop handles teaching; this loop handles measurement.

## Inputs

- The module being assessed (`pNmM`) and its `question-bank` note in `assessments/question-banks/`.
- The evergreen notes tagged with that module (the core claims under test).
- Each note's current `mastery` band and `review-due` date.
- The last `assessment-session` note for this module, if one exists (for trend and to recall prior misconceptions).

## The closed-book-first protocol

Run every probe through four moves, in order. Never collapse them.

1. **Ask.** Pose the question cold. No hint, no multiple choice, no restating the claim. "What does the breeder's equation predict, and what are its terms?" The learner answers from memory only.
2. **Wait.** Give the learner room to produce a full answer, including "I don't know" or a partial one. Do not fill the silence with the answer. A struggled retrieval that eventually lands is worth more, for retention, than a smooth recognition.
3. **Probe the gap.** Where the answer is incomplete, wrong, or memorized-but-hollow, ask one or two scaffolded follow-ups (the socratic-teaching-scaffolds ladder: from a concrete instance up to the principle, or a "what would happen if…" counterfactual). The probe diagnoses *whether the structure is there*, not whether they can be led to the words.
4. **Confirm.** Only now reveal the canonical claim from the evergreen note. State plainly whether the learner had it, partly had it, or missed it, and name the specific gap. The learner sees the correct answer last, against their own attempt — this contrast is itself an encoding event.

A hollow answer (correct words, no mechanism behind them) scores below a struggled answer that reconstructs the mechanism in the learner's own terms. Production over recognition, always.

## Bloom-tagged probes

Tag each probe with the Bloom level it exercises (`conventions.md` §8). A module assessed only at `remember`/`understand` has not been assessed. Push to `apply`/`analyze`; a capstone-adjacent module reaches `create`.

| Bloom level | What the probe demands | Genomics example |
|---|---|---|
| remember | recall a definition or term | "What does GEBV stand for?" |
| understand | restate a claim in own words + mechanism | "Why is heritability a property of a population, not a trait?" |
| apply | use the idea on a fresh case | "Selection intensity doubles; what happens to predicted response, holding h² and σ_P fixed?" |
| analyze | decompose, compare, find the flaw | "A model's accuracy rose with markers then fell. Decompose the two forces in tension." |
| evaluate | judge a claim or a design | "Is it sound to validate genomic prediction by random CV when families are structured? Defend." |
| create | design or simulate something new | "Sketch a simulation that would let you *see* response shrink as the population inbreeds." |

Cover at least three Bloom levels per session, including one at `apply` or higher. Record which levels were probed in the session note's `bloom-levels` field.

## Dreyfus mastery bands

Place the learner in one band *per core claim*, then take the module's band as the modal (typical) claim band, noting the spread. Bands are Dreyfus-flavored (`conventions.md` §8); a module is `mastered` at `proficient`+ on its core claims.

| Band | Behavioral signature under closed-book probing |
|---|---|
| unfamiliar | cannot produce the claim or recognize it when shown |
| aware | recognizes the claim when shown; cannot reconstruct it cold |
| functional | reconstructs the claim and its mechanism cold, follows the standard steps, but needs prompting on edge cases |
| proficient | applies the claim to a fresh case unprompted, connects it to neighboring claims, sees when it breaks |
| fluent | reasons with the claim instinctively, teaches it, recognizes its limits and the assumptions it rides on |

Borrow the descriptor-per-level discipline of [[evaluation-rubrics]]: each band is a *behavioral* descriptor you can match against a transcript, not a vibe. If you cannot point at the move in the answer that earns a band, you have over-rated it.

## Misconception detection

A wrong answer is data; a *structured* wrong answer is gold. Watch for the recurring genomics misconceptions and log each one explicitly, because a misconception that survives is what the next review must target.

- **Heritability as destiny / as a trait property** — treating h² as fixed and trait-intrinsic rather than population- and environment-specific.
- **Correlation read as cause in GWAS** — a significant marker *is* the causal variant, ignoring linkage disequilibrium and the fact the SNP is usually a tag.
- **"More markers must mean more accuracy"** — ignoring the bias–variance tradeoff and that informative content saturates with LD.
- **Confusing additive with total genetic variance** — folding dominance/epistasis into "the genetics" when response to selection rides on additive variance.
- **Leakage in prediction CV** — random cross-validation across related individuals inflates accuracy; the honest test holds out families/environments.

For each misconception caught, record the claim it attaches to, the exact wrong reasoning the learner produced, and the probe that surfaced it. This goes in the session note and steers the next surfacing.

## Scoring

1. Score each probe 0 / 0.5 / 1: miss / partial-or-hollow / clean cold reconstruction. A hollow recognition caps at 0.5.
2. Session score is the sum over total, reported as `n/m` (e.g. `7/10`), and matched to the module band.
3. Map score band to mastery band as a prior, then *override from behavior* if the transcript shows otherwise (a learner can score 8/10 yet reveal a load-bearing misconception that pins them at `functional`). Behavior wins over arithmetic.
4. The module is clear to advance only at `proficient`+ on its core claims with no live misconception on a core claim.

## Spaced-repetition scheduling

Each evergreen note and module carries a `review-due` date. Schedule the next surfacing on **expanding intervals**: `1d → 3d → 7d → 16d → 35d`, then continue stretching (~2.2×) for fluent material. The interval *expands on success* (the spacing effect: a recall that's just hard enough cements the trace) and **contracts on a miss**.

Per claim, track its position on the ladder:

1. **Clean reconstruction (score 1):** advance one rung — `7d` becomes `16d`.
2. **Partial/hollow (0.5):** repeat the current rung — `7d` stays `7d`.
3. **Miss, or a live misconception (0):** pull *back* down the ladder — drop to `3d` (or `1d` if it was a core claim at an early rung). Pulling the date earlier is the whole point: missed material must come back fast.

Worked example. The claim *"response to selection scales with additive variance, not total genetic variance"* sits at the `7d` rung, last reviewed today, 2026-05-30.

- Clean cold reconstruction → next rung `16d` → `review-due: 2026-06-15`, band nudges toward `proficient`.
- Hollow answer (named the equation, couldn't say *why* additive) → repeat `7d` → `review-due: 2026-06-06`, band holds at `functional`, misconception "additive vs total variance" logged.
- Missed, asserted total variance drives response → contract to `3d` → `review-due: 2026-06-02`, band drops to `aware`, misconception logged as the target of the next session.

Set the module's `review-due` to the *earliest* `review-due` among its core claims, so the soonest-failing claim pulls the whole module back.

## Outputs (everything proposes; the learner approves)

This skill never writes to the vault autonomously (`conventions.md` §10). It proposes two artifacts and waits for go-ahead.

**1. An assessment-session note** at `assessments/log/pNmM-assessment-YYYY-MM-DD.md`, frontmatter exactly per `conventions.md` §6:

```yaml
---
type: assessment-session
module: p2m3
date: 2026-05-30
bloom-levels: [understand, apply, analyze]
mastery-band: functional
score: "7/10"
next-review: 2026-06-06
tags: [assessment]
---
```

Body: a per-claim table (claim link `[[slug|Title]]` · Bloom level · score · band · the gap) using the piped link form (`conventions.md` §3), a misconceptions section quoting the learner's own wrong reasoning, the verdict on advancement, and the per-claim schedule moves.

**2. A proposed `review-due` (and, where it changed, `mastery`) update on each evergreen note touched** — shown as a diff per note, never applied without approval. Format the proposal so the learner can accept the whole batch or cherry-pick.

End the session with **one retrieval the learner should attempt unaided before the next surfacing** — the weakest core claim, posed as a cold question, not a summary of how they did. Leaving the loop open on an effortful question is itself spaced encoding.
