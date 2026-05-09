---
name: paper-relevance-filter
description: Scores a candidate paper against a keyword watchlist and a relevance-criteria document, returning KEEP/DROP/REVIEW with a one-line rationale and a 0-100 relevance score. Combines keyword-match strength, criteria-fit, and a historical-context check (was this paper or its preprint already covered in a recent digest). Domain-neutral - usable for any literature-scan workflow. Use after fetching candidate papers from bioRxiv, medRxiv, or PubMed and before clustering or synthesis. Trigger keywords - paper relevance, filter papers, keep or drop, score papers, relevance rationale.
---

# paper-relevance-filter

Decide whether a fetched paper belongs in this week's digest. Output is a per-paper decision (KEEP / DROP / REVIEW), a 0-100 score, and a one-line rationale that the user can audit.

## Workflow

```
- [ ] Step 1: Load relevance criteria + the watchlist + last-4-weeks kept-paper IDs
- [ ] Step 2: Score each paper on three axes (match, criteria, novelty)
- [ ] Step 3: Combine to a 0-100 score; map to KEEP / REVIEW / DROP via thresholds
- [ ] Step 4: Apply tie-breakers (cap output at requested max kept count)
- [ ] Step 5: Return decisions + a calibration summary
```

**Step 1 — Inputs**

The caller hands the skill:
- `papers`: list of normalized paper records (output of `fetch-preprint-recent` or `fetch-pubmed-recent`)
- `watchlist`: list of keywords/phrases (with optional weights — default weight 1.0)
- `criteria`: text from `relevance-criteria.md` describing what fits and what doesn't
- `prior_ids`: set of `id` values that appeared as KEEP in any of the last 4 digests (used for novelty)
- `max_kept`: target ceiling, e.g. 25 (the digest will not exceed this)

**Step 2 — Three-axis scoring**

For each paper, compute three sub-scores in [0, 1]:

**Axis 1 — Match strength (0-1)**
- 0.0 if no watchlist keyword appears in title or abstract
- 0.5 if a keyword appears once in the abstract only
- 0.7 if a keyword appears in the abstract more than once OR in title once
- 1.0 if a keyword appears in the title AND abstract, or multiple distinct keywords match

If keywords carry weights (some matter more than others), use the max weight among matched keywords as a multiplier capped at 1.0.

**Axis 2 — Criteria fit (0-1)**
This is the qualitative axis. Read the abstract against the relevance-criteria document. The criteria typically state:
- In-scope concepts (the field/method the user actually wants)
- Out-of-scope concepts (look-alikes the keyword filter might let through)
- Required minimums (e.g., "must report empirical results", "must be primary research, not commentary")

Score:
- 1.0 — clearly in-scope, meets minimums, no look-alike traps triggered
- 0.7 — in-scope but borderline (review article on the topic; short report; preprint with no methods detail in abstract)
- 0.4 — partially in-scope (touches the topic but the paper's main subject is elsewhere)
- 0.0 — out-of-scope or trips an explicit exclusion (e.g., "exclude pure-theory papers" and the abstract is pure theory)

If the criteria document is silent on a paper's territory, default to 0.7 and flag for REVIEW.

**Axis 3 — Novelty (0-1)**
- 1.0 if `id` is not in `prior_ids` and the title doesn't fuzzy-match any prior title
- 0.5 if a prior preprint version exists in `prior_ids` (e.g., same DOI prefix `10.1101/...` matched, this is a journal version) — KEEP-worthy but tag as "journal version of preprint covered YYYY-WW"
- 0.0 if exact `id` match in `prior_ids` (already covered)

Use normalized title (lowercase, strip punctuation, collapse whitespace) for fuzzy matching. A Levenshtein ratio > 0.9 against any prior title counts as a match.

**Step 3 — Combine and threshold**

```
score = 100 * (0.45 * match + 0.45 * criteria + 0.10 * novelty)
```

Match and criteria carry equal weight (a paper that mentions your keywords once but is wildly out-of-topic should not score higher than one that's deeply on-topic with a single mention). Novelty is a small finger on the scale — enough to demote already-covered work but not enough to drop a genuinely important journal-version-of-preprint update.

Decision thresholds (default; the calling agent may override):

| Score    | Decision | Notes                                                          |
| -------- | -------- | -------------------------------------------------------------- |
| 70-100   | KEEP     | Goes into the digest                                           |
| 50-69    | REVIEW   | Boundary cases — caller decides whether to escalate to user    |
| 0-49     | DROP     | Filtered out, reason logged in the dropped-papers section      |

Special-case override: if `novelty == 0.0` (already in a prior digest), force DROP regardless of score. The papers section may still list it as "already covered" for traceability.

**Step 4 — Tie-breakers when KEEP > max_kept**

When more papers score ≥ 70 than `max_kept`:

1. Re-score with stricter axis-2 thresholds (review articles drop from 0.7 to 0.4; partial-fit drops from 0.4 to 0.2). This is the cleanest tightening.
2. If still over, sort KEEPs by score descending, take the top `max_kept`, and demote the rest to REVIEW (not DROP — they were good enough; just couldn't fit). Surface this in the calibration summary.

Never demote to DROP what scored ≥ 70 unless explicitly forced.

**Step 5 — Return**

```json
{
  "decisions": [
    {
      "id": "10.1101/2026.05.07.123456",
      "decision": "KEEP",
      "score": 84,
      "axes": {"match": 0.9, "criteria": 1.0, "novelty": 1.0},
      "rationale": "Title + abstract hit 'protein language model' twice; in-scope (primary methods paper, empirical); novel.",
      "tags": []
    },
    {
      "id": "PMID:39000000",
      "decision": "KEEP",
      "score": 72,
      "axes": {"match": 1.0, "criteria": 0.7, "novelty": 0.5},
      "rationale": "Strong keyword match; review article (criteria penalty); journal version of preprint covered 2026-15.",
      "tags": ["journal-version-of:2026-15"]
    },
    {
      "id": "PMID:39111111",
      "decision": "DROP",
      "score": 31,
      "axes": {"match": 0.5, "criteria": 0.0, "novelty": 1.0},
      "rationale": "'protein language model' appears once in abstract but the paper is a clinical trial enrollment report — out of scope.",
      "tags": ["look-alike-trap"]
    }
  ],
  "calibration": {
    "kept": 17,
    "review": 3,
    "dropped": 84,
    "force_dropped_already_covered": 2,
    "demoted_for_cap": 0,
    "stricter_pass_applied": false
  }
}
```

## Common Patterns

**Pattern A — Strict weekly digest**: defaults above. Tight thresholds; max_kept=25.

**Pattern B — Catch-up over multiple weeks**: run per-week with the same prior_ids growing each iteration. Don't pool all 3 weeks of papers and filter once — you'll lose the historical-context signal.

**Pattern C — Topic deep-dive (user wants more, not less)**: relax max_kept to a high number (e.g. 100), keep thresholds, return the full ranked list. Only do this on explicit user request.

**Pattern D — Sanity-check the watchlist itself**: run with `prior_ids = []` and look at calibration.dropped. If the same theme keeps getting dropped for criteria reasons, the watchlist may be drifting away from intent.

## Guardrails

1. **Never decide based on title alone if the abstract is available.** Titles overstate; abstracts qualify.
2. **Never KEEP a paper whose abstract isn't returned.** Tag it REVIEW so the user can decide; an empty abstract is a signal something went wrong upstream, not a green light.
3. **Always explain the DROP.** A one-line rationale per dropped paper is non-negotiable — without it the user cannot audit the filter or notice systematic blind spots.
4. **Don't conflate "out of scope" with "low quality".** This skill judges fit, not quality. A high-quality paper outside scope is a DROP; a low-quality paper inside scope is a KEEP with a rationale flag.
5. **Don't auto-update the watchlist.** If you notice the criteria are pulling in a class of papers the watchlist doesn't anticipate, surface it in the calibration summary; the user owns the watchlist edit.
6. **Don't dedupe inside this skill.** The caller is responsible for cross-source dedupe (a bioRxiv preprint and its PubMed publication are *the same paper* and must be merged before this skill sees them, otherwise novelty scoring breaks).
7. **Don't use unbounded LLM judgment for axis 2.** Keep the criteria-fit decision anchored to the explicit `relevance-criteria.md` text. If something's not in the criteria, the answer is REVIEW with rationale "criteria silent" — not "I think it fits."

## Quick Reference

| Decision | Score | Action by caller                                     |
| -------- | ----- | ---------------------------------------------------- |
| KEEP     | 70+   | Include in digest, cluster, synthesize                |
| REVIEW   | 50-69 | Surface in a "boundary cases" section, ask user       |
| DROP     | 0-49  | Log in dropped-papers list with rationale             |

| Axis     | Default weight | What it measures                                    |
| -------- | -------------- | --------------------------------------------------- |
| Match    | 0.45           | How strongly watchlist keywords appear in title/abs |
| Criteria | 0.45           | Qualitative fit against `relevance-criteria.md`     |
| Novelty  | 0.10           | Not already in last-4-weeks digests                 |
