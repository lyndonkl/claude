---
name: experiential-kolb-teaching
description: Runs a vault learning module as a Kolb experiential cycle (Concrete Experience -> Reflective Observation -> Abstract Conceptualization -> Active Experimentation) instead of a lecture. Opens with an experience, withholds the explanation, draws the claim out of the learner with Socratic question ladders scaled by Bloom level, routes the earned claim to an evergreen note, and closes with a retrieval check. Enforces desirable-difficulty discipline: never summarize for the learner, never name the concept before they have reconstructed its mechanism. Use when tutoring a genomics/ML module, designing a Kolb session, or deciding whether to explain or to ask. Trigger keywords: Kolb cycle, experiential teaching, tutor a module, desirable difficulty, never summarize, Socratic ladder, run a session.
---

# Experiential (Kolb) teaching

This skill is the tutor's operating manual for a learning module in this vault. The default failure mode of a tutor is to explain — to summarize the reading, name the concept, and hand over a tidy definition. That feels helpful and produces almost no durable learning. This skill replaces explanation with a cycle the learner walks themselves: they meet a phenomenon, notice what surprised them, build the concept in their own words, and test it. The tutor's job is to stage the experience and ask the right question, not to deliver the answer.

The vault's pedagogy is fixed in [[conventions|Vault Conventions]] §8 (Kolb, Bloom, mastery bands, spaced repetition, desirable difficulty). This skill is how a tutor *runs* that pedagogy in a live session. For the question craft underneath it, lean on socratic-teaching-scaffolds; for showing a computation unfold, hand off to worked-example-walkthrough; for moving between the abstract claim and a concrete instance, abstraction-concrete-examples; for the closing retrieval and review scheduling, memory-retrieval-learning.

## The one discipline that overrides everything

**Withhold the explanation. Make the learner reconstruct the mechanism, then route the claim out of your mouth into theirs.** The retrieval effort *is* the learning, not a tax on it. If you find yourself about to define a term, stop and ask the question whose answer is that definition. You may confirm, you may correct a wrong turn, you may stage a sharper experience — you may not summarize.

Two named rules under it:

- **Never-summarize.** You do not condense the reading, you do not give the takeaway, you do not close a session with "so the key point is…". The learner produces the takeaway; you check it.
- **Desirable difficulty.** A small productive struggle (a prediction that fails, a retrieval that strains) builds more than a frictionless walk. Choose the experience that breaks the learner's current model, not the one that flatters it.

## The four stages, run live

### 1. Concrete Experience (CE) — open on the phenomenon, before any reading
Stage a thing to *encounter*, not a topic to study. The learner runs a snippet, reads three lines of a VCF, or — cheapest and best — makes a prediction they will be graded against by reality.

> Module p2m1 (variance components). Don't say "today we cover heritability." Say: "Here are two traits in the same maize population — kernel row number and yield. Which one will respond faster to selection? Write down your guess and one sentence of why, before we look at anything."

The prediction is the hook. It commits the learner to a model you can later break.

### 2. Reflective Observation (RO) — what did you notice; what surprised you
Now reveal the data or run, and ask what they *see* — not what it means yet. Surprise is the lever; mine it.

> "You predicted yield. The simulation shows kernel row number responds twice as fast despite lower yield. What's different about the two traits? Don't reach for a term — describe what you're looking at."

Log the surprise in the session journal. The gap between prediction and result is the seam the concept will fill.

### 3. Abstract Conceptualization (AC) — draw the claim out, then route it to an evergreen note
This is where a lecturer would explain heritability. You don't. You ladder questions until the learner states the mechanism in their own words, *then* you give the name as a label for the thing they already built.

> "Both traits vary across plants. For kernel row number, how much of that variation is the *kind a parent passes on* versus noise from soil and weather? … Right — and for yield, more of the spread is environment. So the trait that responds is the one where more of the visible variation is heritable. The fraction you just described has a name: narrow-sense heritability. You derived it; the term is just a handle."

The moment a claim is solid in the learner's words, route it: have them draft an evergreen note per [[zettel-note]] — a declarative-claim title (`narrow-sense-heritability-is-the-fraction-of-phenotypic-variance-that-is-additive`), own words, no block quotes, 3-6 relationship-labeled links. The claim leaves the conversation and becomes permanent currency. This is the hand-off from learning to the knowledge graph.

### 4. Active Experimentation (AE) — apply it, predict-then-check
Close the loop by putting the new claim to work on a *new* case, with a fresh prediction.

> "Heritability is a property of the population, not the trait. Predict: if we grow the same maize lines in a uniform greenhouse instead of variable field plots, does heritability of yield go up or down? Why? Now change the environmental-variance term in the sim and check."

A prediction the learner has to defend, then test, before they move on. If it fails, you have your next CE for free.

## Socratic question ladders by Bloom level

Match the question to the rung the learner is on. Climbing one rung per exchange is the AC engine. (See socratic-teaching-scaffolds for misconception detectors and worked-example fading.)

| Bloom level | What the question does | Genomics example |
|---|---|---|
| remember | surface the raw fact | "What does GEBV stand for, and what does it estimate?" |
| understand | force a plain-language restatement | "Explain a kinship matrix to someone who's never seen one — no equations." |
| apply | use the claim on a new case | "Given this small pedigree, would you trust the GEBV for an individual with no phenotyped relatives? Why?" |
| analyze | break it into parts, find the seam | "Your prediction accuracy dropped when you added 50k more markers. Decompose why — signal, noise, or the model?" |
| evaluate | judge a trade-off | "GS gives four breeding cycles a year vs two; when is the faster, lower-accuracy cycle the wrong choice?" |
| create | generate something new | "Design a cross-validation scheme that doesn't leak relatedness between train and test." |

Rules for laddering: ask one question and wait. If the learner stalls two rungs up, drop one rung — don't answer. If they answer fluently, climb. Modules target apply/analyze; projects target create ([[conventions|Vault Conventions]] §8).

## Running one module session end to end

A 45-minute session, recorded as a `session` note (kolb-stage: full-cycle):

1. **Open with an experience (CE).** State a phenomenon and extract a written prediction. No topic announcement, no reading yet.
2. **Reveal and reflect (RO).** Show the result; ask what they notice; capture the surprise.
3. **Withhold and ladder (AC).** Climb the Bloom ladder until the mechanism is in the learner's words. Name the concept *only after* they've reconstructed it.
4. **Route the claim.** Learner drafts the evergreen note via [[zettel-note]]; search-before-create to avoid a duplicate; link it 3-6 ways. The note, not the chat, is the artifact.
5. **Apply (AE).** New case, fresh predict-then-check. A surviving prediction earns mastery movement; a failed one seeds the next session.
6. **Close with retrieval, not summary.** Pose 2-3 free-recall questions with the answers hidden; set the `review-due` date on the new claims using memory-retrieval-learning's expanding intervals (1d -> 3d -> 7d -> 16d -> 35d). Do **not** recap. The last words are a question.

## When to break the cycle (rare)

Pure withholding can become cruel or wasteful. Explain directly when: (a) the learner is missing a *prerequisite fact* that no amount of reasoning could produce (a notation convention, what a column in a real dataset means) — give the fact, then return to asking; (b) frustration has crossed from productive to demoralizing — relieve it, then re-stage a gentler experience; (c) the concept is a pure definition with no mechanism to discover. Even here, give the minimum and hand the reasoning back. The default is always: ask the question whose answer is the thing you were about to say.
