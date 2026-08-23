---
name: readability-check
description: Scores prose with Flesch Reading Ease, Flesch-Kincaid Grade, SMOG, Gunning Fog, and Dale-Chall, reports every score on one shared grade-band scale, and rewrites the sentences that fail. Runs on markdown files or on piped draft text before it is sent, and can run automatically through Claude Code hooks. Use before delivering any substantial written output, when a draft reads as convoluted or bloated, when a document must hit a reading-level target, or when checking a folder of documents for prose quality. Trigger keywords — readability, reading level, Flesch, Flesch-Kincaid, SMOG, Gunning Fog, Dale-Chall, grade level, hard to read, convoluted, dense prose, plain language, reading ease.
---

# Readability Check

## Contents

- [Quick start](#quick-start)
- [Profiles](#profiles)
- [Workflow](#workflow)
- [Revision moves](#revision-moves)
- [Reading the five formulas together](#reading-the-five-formulas-together)
- [Run it automatically](#run-it-automatically)
- [Guardrails](#guardrails)
- [Reference files](#reference-files)

**Related skills:** `slop-detector` catches AI-explainer patterns, `hedge-detector` catches weak hedging, `voice-check` and `strategist-voice` catch voice violations. This skill catches *structural* unreadability — sentence length and word difficulty — which the others do not measure. Run this last, after voice and slop passes. When a score fails and splitting sentences does not fix it, use `ladder-of-abstraction`: it diagnoses what a failing score means and routes the fix to supplying a concrete particular rather than to swapping in vaguer words.

## Quick start

Requires `textstat`. If missing, the script prints the install line and exits 3:

```bash
python3 -m pip install --user textstat
```

**Check draft prose before sending it** — the most common use:

```bash
cat <<'EOF' | python3 resources/readability.py --stdin --profile general
[the draft text]
EOF
```

**Check files:**

```bash
python3 resources/readability.py doc.md --profile technical
python3 resources/readability.py docs/ --recursive --profile general
python3 resources/readability.py doc.md --json          # machine-readable
```

Exit code is 0 on pass, 1 on fail, 3 if textstat is missing. The script strips code fences, tables, headings, and link URLs before scoring, because readability formulas are only valid on continuous prose.

Output reports each formula with its raw score **and a grade band**, plus the band most of them agree on:

```
FAIL  primer.md
      4934 words / 297 sentences of prose   →  reads at: college
      Flesch Reading Ease 39.8 (college)
      Flesch-Kincaid      11.7 (high school)
      Gunning Fog         14.6 (college)
      Dale-Chall          12.4 (college)
      SMOG                13.6 (college)
      ✗ Flesch Reading Ease 39.8 < 40.0
      ✗ 12 sentence(s) over 40 words
```

## Profiles

| Profile | Reading Ease ≥ | FK ≤ | Fog ≤ | SMOG ≤ | Dale-Chall ≤ | Sentence words ≤ | Use for |
|---|---|---|---|---|---|---|---|
| `technical` | 40 | 14 | 16 | 14 | 12.9 | 40 | Engineering or scientific prose where terminology is load-bearing |
| `general` (default) | 50 | 12 | 14 | 12 | 8.9 | 35 | Explanatory writing for a competent non-specialist |
| `public` | 60 | 9 | 11 | 10 | 6.9 | 25 | Public-facing copy |

Pick by audience, not by what the draft happens to score. Threshold rationale and the shared band scale are in [methodology.md](resources/methodology.md).

## Workflow

Copy this checklist and work through it:

```
Readability pass:
- [ ] Step 1: Pick the profile from the audience
- [ ] Step 2: Score the text
- [ ] Step 3: Rewrite the flagged sentences
- [ ] Step 4: Re-score
- [ ] Step 5: Repeat 3-4 until it passes, or justify the exception
```

**Step 1: Pick the profile.** Audience decides. A design doc for engineers is `technical`; a launch announcement is `public`.

**Step 2: Score.** Run the script. Read the **long-sentence list first** — sentence length dominates every formula here, and over-long sentences are what make prose feel incoherent. The aggregate scores only tell you whether to act; the sentence list tells you where.

**Step 3: Rewrite the flagged sentences.** Apply the [revision moves](#revision-moves). Fix the longest sentences first; a single 60-word sentence can fail a whole document.

**Step 4: Re-score.** Run the same command again.

**Step 5: Loop.** If it still fails, return to Step 3. Two rounds usually suffice. If a document cannot pass without losing meaning, say so explicitly and name which threshold you are missing and why — see [Guardrails](#guardrails).

## Revision moves

Ordered by impact. The first three fix most failures.

Generated prose fails in two characteristic ways, and both are fixed by splitting rather than by simplifying vocabulary. Moves 1 and 2 handle almost every real failure.

**1. Break the packed list out of the sentence.** The dominant failure mode: a list joined by semicolons with a parenthetical gloss on each item. Three or more parallel items inside one sentence belong in a bulleted list. Measured effect on a real 102-word example: Reading Ease −51.0 → 43.7, Fog 48.3 → 11.9, with the content unchanged. See [before-after.md](resources/examples/before-after.md) §1.

**2. Stop qualifying mid-sentence.** The other characteristic failure: em-dash asides and subordinate clauses stacked onto a claim instead of finishing the sentence and starting another. Give each move in the argument its own sentence. Measured: Reading Ease 2.4 → 73.9. See §2.

**3. Split at the conjunction.** Any remaining sentence with `and`, `but`, `which`, or `because` mid-clause is usually two sentences.

**4. Cut the throat-clearing.** "It is important to note that", "In order to", "The fact that". Delete and start at the verb.

**5. Un-nominalize.** "perform an evaluation of" → "evaluate". "make a determination" → "decide". Prefer the shorter synonym when both are exact — but not when the longer word is more precise.

## Reading the five formulas together

Four formulas define word difficulty by **syllables**. Dale-Chall defines it by **absence from a familiar-word list**. That difference is why both are worth running, and **their disagreement is the diagnosis**:

| Pattern | Means | Fix |
|---|---|---|
| High FK/Fog, low Dale-Chall | Long sentences of ordinary words | Split sentences |
| Low FK/Fog, high Dale-Chall | Short sentences of dense jargon | Define terms on first use — **not** shorter sentences |
| Both high | Long sentences *and* dense vocabulary | Split first, then reassess |
| Both pass | Structurally fine | Stop. Check meaning, not readability |

Expect Dale-Chall to read one band harder than the others on domain writing. That is the formula working as designed, not a defect. When the audience genuinely knows the vocabulary, say so and accept the score rather than dumbing down the terms.

## Run it automatically

Optional Claude Code hooks score long prose without anyone asking: a `Stop` hook checks Claude's own output, and a `PostToolUse` hook checks documents as they are written. Both skip anything under 300 words.

Setup, configuration, and safety properties are in **[hooks/README.md](hooks/README.md)**. The hook fails open by design — if anything goes wrong it exits silently rather than disturbing the session.

## Guardrails

1. **Never strip a technical term to hit a score.** Terms like `eventual consistency`, `backpressure`, or a cited standard's exact wording are load-bearing. Simplify the sentence around the term, not the term.
2. **Never optimize tables, code, or headings.** The script already excludes them. If a table scores badly, that is a formatting question, not a readability one.
3. **Formulas measure structure, not sense.** A document can pass every threshold and still be wrong or incoherent. Passing is necessary, not sufficient.
4. **SMOG needs 30+ sentences.** Below that the script omits it rather than reporting a meaningless number. Do not treat its absence as a pass.
4b. **A high Dale-Chall alone is not a rewrite order.** It flags unfamiliar vocabulary, which is often correct and necessary. Diagnose before revising — see [Reading the five formulas together](#reading-the-five-formulas-together).
5. **Under 40 words of prose, nothing is scored.** Short outputs are exempt; do not force a score on them.
6. **Quoted material is not yours to edit.** If a long sentence sits inside a quotation, leave it and note the exception.
7. **State exceptions out loud.** When a document cannot pass without losing meaning, report the score, name the threshold missed, and explain the trade-off. Do not silently ship a failing document or quietly lower the profile.

## Reference files

- **[methodology.md](resources/methodology.md)** — what each formula measures, the shared band scale, why the thresholds sit where they do, the Dale-Chall banding decision, and known limits
- **[template.md](resources/template.md)** — the report format for presenting scores and revisions
- **[examples/before-after.md](resources/examples/before-after.md)** — six worked rewrites, including one showing when *not* to rewrite
- **[hooks/README.md](hooks/README.md)** — automatic checking via Claude Code hooks
- **[evaluators/rubric_readability_check.json](resources/evaluators/rubric_readability_check.json)** — scoring rubric and four evaluation scenarios

## Quick reference

- Input: markdown file, directory, or piped text.
- Output: five scores per input, each with a grade band, a consensus band, pass/fail against the profile, and the long sentences to rewrite.
- Loop: score → rewrite → re-score until pass.
- The long-sentence list is the actionable output. Start there.
- Formula disagreement is a diagnosis, not noise.
