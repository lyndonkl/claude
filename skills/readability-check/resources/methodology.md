# Readability methodology

## Contents

- [What each formula measures](#what-each-formula-measures)
- [The shared grade bands](#the-shared-grade-bands)
- [Why the thresholds sit where they do](#why-the-thresholds-sit-where-they-do)
- [Dale-Chall banding, and the alternative](#dale-chall-banding-and-the-alternative)
- [Known limits](#known-limits)

## What each formula measures

All five reduce to two inputs: how long the sentences are, and how hard the words are. They differ in how they define "hard."

| Formula | Word difficulty defined as | Output | Direction |
|---|---|---|---|
| **Flesch Reading Ease** | syllables per word | 0–100 | higher = easier |
| **Flesch-Kincaid Grade** | syllables per word | US grade | lower = easier |
| **Gunning Fog** | words of 3+ syllables | US grade | lower = easier |
| **SMOG** | count of polysyllabic words | US grade | lower = easier |
| **Dale-Chall (v1)** | words absent from a ~3,000-word familiar list | raw score | lower = easier |

Dale-Chall is the odd one out and the reason it earns its place: it uses a **word list** rather than syllable counting. A short but unfamiliar word — `SMOG`, `RAG`, `nexus` — is easy for the syllable-based formulas and hard for Dale-Chall. Running both catches prose that is simple to pronounce and still opaque.

Because they disagree by construction, the script reports all five plus a consensus band. **Disagreement is information.** Low Flesch-Kincaid with high Dale-Chall means short sentences full of jargon. High Flesch-Kincaid with low Dale-Chall means long sentences of ordinary words.

## The shared grade bands

Five scales are hard to compare. Every score is therefore mapped to one band:

| Band | Grade equivalent |
|---|---|
| elementary | below 6 |
| middle school | 6–8 |
| high school | 9–12 |
| college | 13–15 |
| college graduate | 16+ |

Flesch Reading Ease is converted through Flesch's own interpretation table; Flesch-Kincaid, Fog, and SMOG already emit grades; Dale-Chall is converted through the table below. The consensus is the band most formulas agree on, and **ties resolve to the harder band** — understating difficulty is the more costly error for a reader.

## Why the thresholds sit where they do

| Profile | Reading Ease ≥ | FK ≤ | Fog ≤ | SMOG ≤ | Dale-Chall ≤ | Sentence ≤ |
|---|---|---|---|---|---|---|
| `technical` | 40 | 14 | 16 | 14 | 12.9 | 40 |
| `general` | 50 | 12 | 14 | 12 | 8.9 | 35 |
| `public` | 60 | 9 | 11 | 10 | 6.9 | 25 |

- **`technical`** targets the top of the college band. Accurate engineering prose lands there once unavoidable terms are counted as complex, and pushing below it means deleting the terminology rather than clarifying the sentence.
- **`general`** targets the top of high school — the widely used ceiling for professional communication.
- **`public`** targets grade 9, the standard for material intended to be read by the general population without effort.

**Sentence length is the lever that matters.** It appears in all five formulas, so it moves every score at once, and it is the property most responsible for prose that "makes no sense" on first read. When a document fails, fixing the longest sentences usually fixes the aggregate scores as a side effect.

## Dale-Chall banding, and the alternative

This skill maps Dale-Chall v1 as follows:

| Raw score | Band |
|---|---|
| ≤ 4.9 | elementary |
| 5.0–6.9 | middle school |
| 7.0–8.9 | high school |
| 9.0–12.9 | college |
| ≥ 13.0 | college graduate |

**This is wider than the published Chall & Dale (1995) table**, which places everything at 10.0+ in college-graduate. The reason is that v1 — the original 1948 formula, which is what `textstat.dale_chall_readability_score` implements — runs hotter on technical prose than the 1995 revision. Every term outside its familiar-word list counts as difficult, so ordinary professional writing saturates the 1995 top band and the scale stops discriminating between "dense" and "impenetrable."

**To use the stricter published table instead**, edit `DALE_CHALL_TABLE` in `readability.py`:

```python
DALE_CHALL_TABLE = (
    (4.9, 4.0), (5.9, 5.5), (6.9, 7.5),
    (7.9, 9.5), (8.9, 11.5), (9.9, 14.0),
    (float("inf"), 16.0),
)
```

and lower `dale_chall_max` in each profile accordingly.

## Known limits

1. **Formulas measure structure, not sense.** Text can pass every threshold and still be wrong, circular, or empty. Passing is necessary, not sufficient.
2. **They can be gamed.** Chopping every sentence at the comma improves the score and can destroy the argument. Optimize for the reader, then verify with the score.
3. **Dale-Chall penalizes any specialist vocabulary**, including terms the audience knows perfectly well. On domain writing, expect it to read one band harder than the others; that is the formula working as designed, not a defect in the prose.
4. **SMOG needs 30+ sentences.** The script omits it below that rather than reporting a meaningless number.
5. **Under 40 words, nothing is scored.** Short outputs are exempt.
6. **Sentence splitting is regex-based.** Abbreviations occasionally split early. That slightly affects the offender list and not the aggregate scores, which textstat computes independently.
7. **These are English formulas.** The syllable and familiar-word models do not transfer to other languages.
