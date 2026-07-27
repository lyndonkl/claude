# Worked rewrites

Every score here was produced by running `readability.py` on the text shown, at the `general` profile. The failure modes are the ones that actually show up in generated prose, not textbook bad writing.

## Contents

- [1. The semicolon-chained list](#1-the-semicolon-chained-list)
- [2. The single sentence that keeps qualifying itself](#2-the-single-sentence-that-keeps-qualifying-itself)
- [3. When Dale-Chall disagrees with everything else](#3-when-dale-chall-disagrees-with-everything-else)
- [4. When not to rewrite](#4-when-not-to-rewrite)

## What generated prose actually gets wrong

Model output is rarely ungrammatical and almost never bureaucratic. It fails in two specific ways:

1. **It packs a list into one sentence**, joined by semicolons, with a parenthetical gloss on each item.
2. **It qualifies mid-sentence**, stacking em-dash asides and subordinate clauses onto a claim instead of finishing the sentence and starting another.

Both produce text that is correct, dense, and exhausting. Both are fixed by splitting, not by simplifying vocabulary.

## 1. The semicolon-chained list

**Before** — 102 words, one sentence:

> The ingestion service handles several concerns at once: schema validation against the registry (rejecting any payload whose version is unknown, and emitting a metric so drift is visible); deduplication on the event key, which matters because the upstream producer retries aggressively and duplicates are common; enrichment from the customer dimension table, joined on account id and effective-dated so historical replays resolve correctly; partitioning by ingest date rather than event date, since late-arriving events would otherwise rewrite closed partitions; and finally a dead-letter path for anything that fails, with the original payload preserved so it can be replayed once the defect is fixed.

**After** — 93 words, eleven sentences:

> The ingestion service handles five concerns:
>
> - **Schema validation** against the registry. Payloads with unknown versions are rejected, and a metric is emitted so drift stays visible.
> - **Deduplication** on the event key. The upstream producer retries aggressively, so duplicates are common.
> - **Enrichment** from the customer dimension table. The join is on account id and effective-dated, so historical replays resolve correctly.
> - **Partitioning by ingest date**, not event date. Late-arriving events would otherwise rewrite closed partitions.
> - **A dead-letter path** for failures. The original payload is preserved so it can be replayed once the defect is fixed.

| Formula | Before | After |
|---|---|---|
| Flesch Reading Ease | **−51.0** | 43.7 |
| Flesch-Kincaid | 45.7 | 9.5 |
| Gunning Fog | 48.3 | 11.9 |
| Dale-Chall | 15.8 | 11.7 |
| Band | college graduate | college |

A Reading Ease of −51 is not a typo. The scale runs 0–100 and goes negative when a sentence is long enough; that is what one 102-word sentence does to a document.

**Nothing was cut.** The content is identical and nine words shorter. The list was always a list — it was only punctuated as a sentence.

## 2. The single sentence that keeps qualifying itself

**Before** — 79 words, one sentence:

> The caching layer is worth adding here — not because read volume is especially high, though it has grown steadily since the last quarter, but because the downstream pricing service has a hard rate limit that we are now brushing against during peak hours, which means that without a cache the checkout path will start returning errors under exactly the conditions where errors are most expensive, and that is a failure mode we should design out rather than monitor for.

**After** — 69 words, five sentences:

> The caching layer is worth adding, though not for the obvious reason. Read volume has grown, but it is not the problem. The problem is that the downstream pricing service has a hard rate limit, and we are brushing against it at peak hours.
>
> Without a cache, the checkout path starts returning errors exactly when errors cost the most. That failure mode should be designed out, not monitored for.

| Formula | Before | After |
|---|---|---|
| Flesch Reading Ease | 2.4 | **73.9** |
| Flesch-Kincaid | 32.5 | 6.4 |
| Gunning Fog | 35.1 | 7.8 |
| Dale-Chall | 12.4 | 9.8 |
| Band | college graduate | middle school |

The argument survives intact, including the "not X but Y" structure that made the original worth writing. What changed is that each move in the argument now gets its own sentence.

## 3. When Dale-Chall disagrees with everything else

Short sentences, dense vocabulary:

> The scheduler is preemptive. Tasks yield at quantum boundaries. Priority inversion is mitigated by inheritance. Starvation is bounded by aging. Throughput degrades gracefully under saturation. Latency percentiles remain stable. Backpressure propagates upstream. Idempotent retries preserve correctness. Observability instruments every transition.

| Formula | Score | Band |
|---|---|---|
| Flesch-Kincaid | 14.8 | college |
| Gunning Fog | 20.8 | college graduate |
| Dale-Chall | **15.3** | college graduate |

Nine sentences averaging four words each, and it still scores at the ceiling. **Splitting sentences cannot help — they are already as short as sentences get.** Every word is doing the damage: `preemptive`, `quantum`, `inversion`, `inheritance`, `starvation`, `saturation`, `percentiles`, `backpressure`, `idempotent`, `observability`.

The remedies are to define terms on first use, add a worked example, or accept the score because the audience is systems engineers who know all ten words. **What does not work is shortening sentences**, which is the move the other formulas appear to be asking for.

This is the whole reason the skill reports five formulas instead of one.

## 4. When not to rewrite

**Before** — 38 words, passes `technical`:

> Under the standard the audit trail must be attributable, legible, contemporaneous, original, and accurate, which means every record needs an actor, a timestamp, and a reason captured at the moment of the change.

**A "fix" that scores better and is professionally useless:**

> Under the rules the log must be clear and correct, so each record needs a person, a time, and a why.

The five adjectives are quoted from the standard being cited. Replacing them with plainer words does not simplify the sentence; it misquotes the source. **The original already passes its profile. Leave it alone.**

The general rule: a score is a reason to look, never a reason to overwrite precise language with vague language.

---

## A note on this file

Running the checker on this file reports a failure: two sentences over 40 words. That is correct, and it stays. The over-length sentences are the quoted "before" examples — they exist to be bad. Guardrail 6 in [SKILL.md](../../SKILL.md) covers this case: quoted material is not yours to edit.

A failing score is a reason to look, not an instruction to rewrite.
