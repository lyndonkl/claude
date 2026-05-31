---
name: learning-in-public-voice
description: House style for learning-in-public essays — a curious practitioner thinking out loud while learning a hard technical subject (here, ML-driven crop genetics / genomic selection). First-person, concrete-first, honest about the edge of understanding, mechanism over vocabulary. Provides the register, the hook patterns, the anti-slop hard rules, and the rule for reading a per-writer voice-profile.md so the voice stays the writer's own. Use when drafting a vault-style post from evergreen notes, or as the lens an advisory editor critiques against. This skill never imposes voice; it describes defaults and defers to the writer's profile.
---

# Learning-in-public voice

This is the house style for essays that a data scientist writes *while learning* a technical subject in public — short pieces that turn a day's reading and a small experiment into one earned claim. The model is a practitioner thinking out loud, not an authority lecturing. The reference voices are people who write to understand: they start from a thing they observed, follow the confusion honestly, and land on one idea they can now defend.

This skill is a **lens, not a cage.** The writer's actual idiolect lives in `writing/voice-profile.md` in their vault. That file always wins. This skill supplies sensible defaults and a vocabulary for talking about voice so an editor can flag a deviation as a *suggestion* without ever overwriting the writer's words. When this skill and the profile disagree, follow the profile and note the difference.

## The register

- **First person, learning in motion.** "I kept reading heritability as a property of the trait until a simulation forced me to see it as a property of the population." The reader watches understanding form.
- **Concrete first, concept second.** Open on the observed thing — a number, a plot, a failed prediction, a line of a VCF file — then reach for the idea that explains it. Never open by defining the topic.
- **Honest about the edge.** Mark precisely where your understanding stops. "I can derive the breeder's equation; I cannot yet feel why response shrinks as the population gets more inbred." Precise uncertainty is a feature. Vague hedging ("it seems like maybe") is not — see the hedge rule below.
- **Mechanism over vocabulary.** Explain how the thing works in plain words before naming it. A term the reader cannot reconstruct from your sentence is decoration.
- **One essay, one claim.** The piece earns a single declarative idea, ideally the title. If two claims are fighting for the essay, it is two essays.
- **Show the work.** A snippet, a small table, a figure, the prediction you made before you ran it. Learning-in-public is credible because the work is visible.

## Opening patterns (pick one; never define the topic)

1. **The thing that broke my model.** Start from the moment an expectation failed. "My genomic-prediction model got *worse* when I added more markers. That should have been impossible."
2. **The number with a take.** A single concrete figure pointed enough that the reader wants the analysis. "A wheat breeder runs maybe two selection cycles a year. Genomic selection promises four. That 2x is the whole argument."
3. **The honest confusion.** Name the specific thing you misunderstood, then resolve it. Works because the reader probably shares the misunderstanding.

Banned openings: "In this post I'll explain…", "X is a Y that does Z", "It's worth noting that…", "Today I learned about…".

## Anti-slop hard rules (defaults; the profile may relax any of them)

These are craft tells that make prose read as machine-generated or as a beginner imitating a register. Treat them as defaults; the writer can override in `voice-profile.md`.

1. **No hollow openings.** "It's worth noting", "It's important to understand", "Let's dive in". State the thing or cut it.
2. **No summary closers.** "In conclusion", "Ultimately", "To summarize", "All in all". End on the live question or the next experiment.
3. **No vague hedging.** Replace "it kind of seems like it might" with either a precise uncertainty ("I'm 70% on this; the part I can't check is …") or a clean claim. Hedging should *specify* doubt, not soak the sentence in it.
4. **Vary sentence length.** A run of same-shaped sentences is the clearest tell. Put a four-word sentence next to a thirty-word one on purpose.
5. **Define jargon on first use, inline.** Every genetics or ML term (allele, LD, BLUP, heritability, GEBV, additive variance, kinship matrix, regularization) gets a plain-language gloss the first time, or gets rewritten away. A term used twice and never defined is the signal the writer copied a register instead of understanding it.
6. **No negation cascades.** "It's not the trait, not the gene, not the environment" — replace with a positive claim or one sharp contrast.
7. **Citations don't interrupt the prose.** Default to numbered footnotes (`claim.[^3]` with `[^3]: Author — title — URL` at the end) or a References block. Inline `(Author et al., 2019)` is acceptable when it is genuinely load-bearing, but a paragraph studded with parentheticals reads like a lit-review, not an essay. The writer chooses; flag overuse, do not enforce.
8. **Earn every list.** A bulleted list is for genuinely parallel items (steps, options, a benchmark table). A list standing in for an argument-in-prose is a buried paragraph.

## Opinion and conviction

Signal where you stand without an authority pose. Scale: "I suspect" / "my read is" (tentative) → "the evidence I've seen says" / "the interesting question is" (reasoned) → "I'm now confident that" / "this is the thing that finally clicked" (confident). Use the confident register only where you've actually done the work to earn it; the credibility of learning-in-public comes from not overclaiming.

## Reading the writer's voice-profile.md

`writing/voice-profile.md` accumulates the writer's actual patterns: favored sentence rhythms, words they like and avoid, how they cite, how much they swear, whether they use em dashes, their typical opener and closer moves, recurring analogies. When applying or critiquing voice:

- Load the profile first. Its observed patterns override every default above.
- Treat the profile as evidence of the writer's form, which this skill must protect, not normalize.
- When the writer publishes a new post they're happy with, the profile should be updated from it (the editor proposes the diff; the writer approves). The profile *learns the writer*; it does not teach the writer a house style.

## Output contract

This skill produces or evaluates prose. It **does not silently rewrite a human's draft.** When used by a generative scribe, it shapes a new draft from the writer's own evergreen claims. When used by an advisory editor, it produces *flagged suggestions against the profile*, each marked as the writer's call. The boundary is in [[advisory-edit]]: assembling the writer's claims into a draft is generative; editing the writer's words is advisory-only.
