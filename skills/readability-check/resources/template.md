# Readability report template

Use when reporting a readability pass. Adapt sections to the situation; keep the scores table and the revisions.

---

## Readability: [document or draft name]

**Profile:** `[technical | general | public]` — chosen because [audience].
**Verdict:** [PASS | FAIL] — reads at **[consensus band]**.

| Formula | Score | Band | Limit | |
|---|---|---|---|---|
| Flesch Reading Ease | | | ≥ | ✅/❌ |
| Flesch-Kincaid Grade | | | ≤ | ✅/❌ |
| Gunning Fog | | | ≤ | ✅/❌ |
| SMOG | | | ≤ | ✅/❌ |
| Dale-Chall (v1) | | | ≤ | ✅/❌ |
| Sentences over [N] words | | — | 0 | ✅/❌ |

### Revisions made

| # | Before (words) | After (words) | Move applied |
|---|---|---|---|
| 1 | *"[first 12 words…]"* ([N]w) | *"[first 12 words…]"* ([N]w) | split at conjunction |

### After revision

| Formula | Before | After |
|---|---|---|
| Flesch Reading Ease | | |
| Flesch-Kincaid Grade | | |
| Gunning Fog | | |
| SMOG | | |
| Dale-Chall (v1) | | |

**Result:** [passes the `[profile]` profile | still fails on [metric]].

### Exceptions

Only when something could not be fixed:

- **[sentence or section]** — kept at [N] words because [reason: quoted material, load-bearing term, legal wording]. Trade-off: [what the reader loses].

---

## Short form

For a quick inline check, one line is enough:

> Readability (`general`): **PASS** — reads at high school. FRE 56.2, FK 9.8, Fog 12.1, SMOG 11.4, Dale-Chall 8.1. No sentence over 35 words.

Report failures with the sentences attached:

> Readability (`general`): **FAIL** — Dale-Chall 9.4 (limit 8.9) and 3 sentences over 35 words. Rewriting the three, then re-scoring.
