---
name: spoken-draft-cleanup
description: Turns a raw dictation transcript into a clean, editable draft while preserving the writer's voice and form exactly. MECHANICAL ONLY — removes fillers and false starts, restores sentence-boundary punctuation and paragraph breaks, and FLAGS likely transcription errors as questions rather than silently fixing them. It does NOT restructure, restyle, reword, or improve. Produces the cleaned draft plus a cleanup log of every change and every flag. This is the strict intake bridge from "speak out my article" to an editable draft, run before the advisory-edit passes. Use when cleaning a dictation/voice transcript, prepping a spoken draft for editing, or doing transcript intake. Trigger keywords: clean up transcript, dictation cleanup, spoken draft, transcript intake, remove fillers, flag transcription errors.
---

# Spoken-draft cleanup

The writer dictates essays out loud. The transcript that comes back is the writer's thinking, verbatim — including the "um"s, the restarts, the missing commas, and the words the speech-to-text engine guessed wrong. This skill does exactly one job: make that transcript *readable as a draft* without changing what the writer said or how they said it. It is mechanical hygiene, not editing.

This is the intake step in the vault's write loop: `transcripts/ -> drafts/` ([[conventions|Vault Conventions]] §2). It runs **before** any [[advisory-edit]] pass. The division of labor is strict — this skill produces a clean `draft` (status: cleaned) that still sounds 100% like the writer; advisory-edit then critiques that draft without touching it. Cleanup is allowed to alter the text (mechanically); advisory-edit is not.

## The one rule that overrides everything

**Mechanical only. Preserve voice and form. Never restructure, restyle, or reword.** If a change would alter *what the writer is saying* or *how they characteristically say it*, you do not make it — you flag it. The writer's word choice, sentence rhythm, paragraph logic, idioms, hedges, jargon, and ordering are all sovereign and out of scope. You are a transcriptionist's assistant, not an editor.

When in doubt about whether a fix is mechanical or editorial: it is editorial. Flag it.

## What cleanup MAY do vs MAY NOT do

| MAY (mechanical) | MAY NOT (editorial — flag instead, or leave alone) |
|---|---|
| Delete fillers: "um", "uh", "like", "you know", "I mean" (when filler, not meaning) | Replace a word with a "better" one |
| Cut false starts and self-corrections, keeping the landing: "the additive— the *narrow-sense* heritability" -> "the narrow-sense heritability" | Reorder sentences or paragraphs |
| Cut verbatim repetition the speaker clearly didn't intend: "the the model" -> "the model" | Tighten or shorten for concision |
| Restore sentence-boundary punctuation: periods, capitalization, question marks | Add transitions, topic sentences, or connective tissue |
| Insert obvious commas at clause boundaries the speaker plainly paused on | Fix grammar that is part of the writer's spoken voice |
| Break the wall of text into paragraphs at the speaker's clear topic shifts | Merge or split the writer's actual ideas |
| Render spoken numbers/units when unambiguous: "ten thousand markers" -> "10,000 markers" (and log it) | Change tone, register, or formality |
| FLAG a likely transcription error as a question | Silently substitute the word you think they meant |

A filler word that carries meaning is not a filler. "Like" in "a kinship matrix is *like* a covariance matrix" is a comparison — keep it. "Like, the model broke" is filler — cut it. When unsure, keep and flag.

## Flagging transcription errors (never silently fix)

Speech-to-text mangles exactly the terms this domain lives on: homophones, jargon, names, and numbers. You must **flag, never fix**, because guessing wrong corrupts the writer's meaning under the guise of cleanup.

Flag inline with a bracketed tag the writer can scan for, and log it:

> "…the model uses **best linear unbiased prediction** to estimate breeding values, and the **`[?]` heritability `[?]`** — `[transcription? "narrow-sense heritability"? sounded like "narrow sense heritage"]` — caps the accuracy."

Inline marker convention: wrap the suspect span and append `[?: your best guess, as a question]`. Leave the original words in place. The writer resolves every `[?]` during the first advisory pass.

High-risk flag categories in this domain:

| Category | Mangle example | Flag as |
|---|---|---|
| Homophone | "allele" -> "a deal", "locus" -> "low cus" | `[?: "allele"?]` |
| Jargon term | "GEBV" -> "gee bee", "epistasis" -> "epic stasis" | `[?: "GEBV"? "epistasis"?]` |
| Proper noun | "Falconer" -> "falconry", "PLINK" -> "blink" | `[?: name — "Falconer"?]` |
| Number/unit | "h-squared of 0.4" -> "age squared of point four" | `[?: "h² of 0.4"?]` |
| Dropped negation | "does not respond" -> "does respond" | `[?: negation — "does not"?]` if audible doubt |

If you cannot even guess, flag the span with `[?: unclear — verify against audio]` and move on. Never delete an unclear span; the writer needs to see where the gap is.

## The cleanup log

Every cleaned draft ships with a log so the writer can audit exactly what you touched. No silent changes — that is the whole contract. Append it at the foot of the draft (or as a sibling note). Structure:

```markdown
## Cleanup log

**Removed (fillers / false starts / repetitions):**
- L3: cut "um, you know" (filler)
- L7: cut false start "the gene— the locus", kept "the locus"
- L12: cut repeated "that that"

**Punctuation / paragraphing restored:**
- L4: sentence boundary after "broke" (period + capital)
- L9: comma at clause boundary ("Once it saturates, accuracy sags")
- Para break inserted before L15 (topic shift: heritability -> prediction)

**Numbers/units rendered (logged):**
- L11: "ten thousand markers" -> "10,000 markers"

**FLAGGED for the writer (NOT changed):**
- L6: [?: "allele"? sounded like "a deal"]
- L8: [?: "GEBV"? — "gee bee vee"]
- L14: [?: negation — "does not respond"? audible hesitation]

**Untouched by design:** word choice, sentence order, paragraph logic, voice.
```

## Worked micro-example

**Raw transcript fragment:**
> um so the thing that surprised me was like the the model got worse when i added more markers which uh shouldnt be possible right because more data is supposed to help but it turns out past a certain point the the markers are just tagging the same a deal over and over

**Cleaned draft:**
> The thing that surprised me was the model got worse when I added more markers, which shouldn't be possible — more data is supposed to help. But it turns out past a certain point the markers are just tagging the same **`[?: "allele"? sounded like "a deal"]`** over and over.

**Log:**
- Cut fillers "um", "so", "like", "uh"; cut repeated "the the" (x2).
- Restored capitalization, periods, the comma after "markers", and the em dash the speaker paused on (within their voice — they pause that way).
- Kept "which shouldn't be possible right" structure; the colloquial "right" is voice, not filler — left it (rendered as a clause, not flagged).
- FLAGGED: `[?: "allele"?]` — did not substitute.

Notice what did *not* happen: no tightening, no reordering, no "improving" the run-on. The draft still sounds exactly like the writer talking. That is the deliverable. The next step is the writer resolving the flags and handing the draft to [[advisory-edit]].
