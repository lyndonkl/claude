# The architecture contract — field reference

`architecture.json` is the artifact. Any markdown companion is generated from it.

Contract version covered here: **1.0**.

---

## Top level

| Field | Type | Required | Notes |
|---|---|---|---|
| `contract_version` | string | yes | `"1.0"`. A run that cannot name its contract cannot be diffed later. |
| `run_header` | object | yes | Provenance. See below. |
| `frame_lock` | object | yes | What is being counted, over what, for whom. |
| `form` | object | yes | The triage verdict and which rung of the downgrade ladder shipped. |
| `protagonist` | object | yes | Person, composite, or system. Systems carry extra obligations. |
| `designing_principle` | object | yes | Statement plus the claims it excludes. |
| `spine` | object | yes | The chosen structure and the one rejected. |
| `slots` | array | yes | The architecture proper. |
| `scenes` | array | no | Tagged scene weave. Present when the form admits scenes. |
| `gaps` | array | yes | May be empty only if genuinely nothing is missing, which is rare. |
| `dead_column` | array | yes | Killed findings, kept. |
| `hypothesis_diff` | object | no | Strongly recommended. What changed between the starting guess and the derived spine. |
| `escalations_received` | array | no | Defects sent back up from the drafting layer. |

## `run_header`

| Field | Type | Notes |
|---|---|---|
| `model` | string | Which model produced this. Tuning on one model silently breaks others. |
| `corpus_ref` | string | A path, a commit, or a freeze tag. |
| `timestamp` | string | ISO 8601. |
| `claim_ids_consulted` | array of string | The **coverage receipt**. If the corpus exceeded the context budget, this is the only record of what was actually seen. |
| `claim_ids_skipped` | array of string | Optional but honest. Silent partial coverage defeats every downstream audit. |

## `frame_lock`

`unit`, `denominator`, `window`, `population`, each a string, plus `rejected_alternatives` — an array of `{field, alternative, why_rejected}`.

Denominator drift is the failure where every exhibit is defensible and the sequence is a lie. Locking the frame once, in writing, is what makes drift detectable.

## `form`

| Field | Type | Notes |
|---|---|---|
| `verdict` | string | `story-narrative`, `explanatory-narrative`, `gathering`, or `do-not-narrate`. |
| `rung` | integer | 1–5 on the downgrade ladder. |
| `failing_questions` | array | Which triage questions failed, by number. |
| `downgrade_reason` | string | Required when `rung > 1`. |
| `research_requests` | array | `{gap, artifact_that_would_fill_it, slot_unblocked}`. Required when `rung > 1`. |

## `protagonist`

`type` is `person`, `composite`, or `system`.

When `type` is `system`, these become required:

| Field | Why |
|---|---|
| `stated_purpose` | Quoted verbatim from a real document — a charter, prospectus, mission statement, launch post. |
| `revealed_function` | What the system reliably converts into what, inferred from outcomes. |
| `gap` | One sentence. The gap between stated and revealed is the dramatic engine; no gap means no narrative. |
| `regimes_evidenced` | At least **two** distinct regimes (boom and bust, normal and incident). A function inferred from one episode is a description of that episode dressed as a character trait. |
| `outcomes_unexplained` | At least one. Every inferred objective function fails to explain something, and that list reaches the reader. |

## `slots[]`

| Field | Type | Notes |
|---|---|---|
| `id` | string | Unique. |
| `name` | string | `inciting_event`, `climax`, `self_revelation`, or a spine-specific slot name. |
| `status` | enum | `FILLED`, `ABSENT`, `INFERRED`. **ABSENT is a passing state.** |
| `evidence` | array of claim ID | Required unless `ABSENT`. **This is the validated field, not `value`.** |
| `warrant` | string | Why this evidence fills this slot. Checked against the tier's permitted verbs. |
| `causal_tier` | enum | `L1` mechanism, `L2` correlation, `L3` sequence, `L4` adjacency, `L5` conjecture. Only L1 may assert causation. |
| `empty_slot_move` | string | Required when `ABSENT`: `DECLARE`, `DOWNGRADE`, or `REDESIGN`. |
| `source_dates` | array | Recommended. A starting weakness needs a source predating the outcome. |

Budget: at most **one** `INFERRED` slot per piece, and never the climax.

## `scenes[]`

| Field | Type | Notes |
|---|---|---|
| `id` | string | Unique. |
| `slot_id` | string | Must match a slot. |
| `tagged_line` | string | **Length-capped.** A tag, not a draft. This cap is what stops the structural layer drafting. |
| `whose_desire`, `opposition`, `plan`, `endpoint`, `twist` | string | Construction fields. |
| `carrier` | enum | `prose`, `exhibit`, or `both`. The non-carrier may not restate the claim at full strength. |
| `position` | string | `opener`, `climax`, `closer`, or a section name. |
| `representativeness` | enum | `median`, `tail`, `unique`. **Required in load-bearing positions.** Assigned upstream against the corpus, never by the drafting agent. |
| `rung` | enum | `R1`–`R4` on the ladder of abstraction. |
| `provenance` | array of claim ID | Required. |

## `gaps[]`

`{slot_id, gap_type, disposition}` where `gap_type` is one of missing scene, motive, quote, number, causal link, outcome; and `disposition` is `RESEARCH`, `REDESIGN`, `DECLARE`, or `CUT`.

There is no `draft and flag`. Flagged drafted text survives review at high rates because it reads well.

## `dead_column[]`

`{claim_id, killed_by, reason}` where `reason` is `did_not_support` or `CONTRADICTED`.

`did_not_support` may be pruned from the deliverable. `CONTRADICTED` always reaches the reader. This distinction is the difference between editing and cherry-picking.

---

## Worked example — a system protagonist

```json
{
  "contract_version": "1.0",
  "run_header": {
    "model": "claude-opus-5",
    "corpus_ref": "corpus/freeze-2026-03-11",
    "timestamp": "2026-03-14T09:22:00Z",
    "claim_ids_consulted": ["c-001", "c-002", "c-118", "c-204"],
    "claim_ids_skipped": []
  },
  "frame_lock": {
    "unit": "settled trades per venue",
    "denominator": "all trades reaching settlement, not all submitted orders",
    "window": "1994-01-01 to 2009-12-31",
    "population": "the four venues with continuous public reporting",
    "rejected_alternatives": [
      {
        "field": "denominator",
        "alternative": "all submitted orders",
        "why_rejected": "two venues stopped publishing rejected-order counts in 1998, so the series breaks"
      }
    ]
  },
  "form": {
    "verdict": "explanatory-narrative",
    "rung": 2,
    "failing_questions": [5, 6],
    "downgrade_reason": "No evidenced point of insight. Behaviour changes across the window, but no dated moment shows participants recognising why, and the record reaches no stable end state.",
    "research_requests": [
      {
        "gap": "A contemporaneous document showing a participant recognising the settlement lag as structural rather than operational",
        "artifact_that_would_fill_it": "Clearing-committee minutes 1999-2001, or an internal risk memo",
        "slot_unblocked": "point_of_insight"
      }
    ]
  },
  "protagonist": {
    "type": "system",
    "stated_purpose": "\"to guarantee settlement of every matched trade\" (1994 rulebook, s.1.2)",
    "revealed_function": "converts counterparty risk into timing risk, by deferring failures to the settlement window rather than preventing them",
    "gap": "The rulebook promises elimination; the record shows relocation.",
    "regimes_evidenced": ["1994-1997 low-volume normal", "1998 stress episode"],
    "outcomes_unexplained": [
      "The 2003 fee change reduced fails by a third with no rule change, which a pure timing-relocation account does not predict."
    ]
  },
  "designing_principle": {
    "statement": "Follow one trade from match to settlement in each of three regimes, and let the widening gap between the rulebook and the tape carry the argument.",
    "claims_excluded": [
      "c-044 the 2011 governance dispute, outside the window",
      "c-077 comparative European venue structure, a different denominator",
      "c-155 the founder's biography, no bearing on the mechanism"
    ]
  },
  "spine": {
    "abt": "The venue guaranteed settlement AND volumes grew twelvefold, BUT the guarantee moved failures into the settlement window rather than removing them, THEREFORE the 1998 stress was a timing failure that the rulebook had no language for.",
    "structure": "layer-cake explanatory narrative on a traveling-object action line",
    "runner_up": "braided mosaic across three venues",
    "runner_up_reason": "Rejected: only one venue has continuous ground-level artifacts, so two strands would run at summary distance and the braid would be decorative.",
    "boredom_permitted": "Inside a digression the preceding scene has paid for, and only for a length not exceeding that scene.",
    "spine_version": 1
  },
  "slots": [
    {
      "id": "s1",
      "name": "inciting_event",
      "status": "FILLED",
      "evidence": ["c-002", "c-118"],
      "warrant": "The 1994 rulebook takes effect and the guarantee language appears; both venues' volumes diverge in the following quarter.",
      "causal_tier": "L3",
      "source_dates": ["1994-02-11", "1994-07-30"]
    },
    {
      "id": "s2",
      "name": "point_of_insight",
      "status": "ABSENT",
      "empty_slot_move": "DECLARE",
      "warrant": "No source records anyone naming the lag as structural before 2004. The absence is stated in the body."
    }
  ],
  "scenes": [
    {
      "id": "sc1",
      "slot_id": "s1",
      "tagged_line": "1994 rulebook takes effect; first matched trade under the guarantee clears in 90 minutes",
      "whose_desire": "clearing members, for a guarantee that removes counterparty checks",
      "opposition": "settlement capacity, fixed at the 1991 build",
      "plan": "guarantee first, add capacity later",
      "endpoint": "the clause is live and the first trade clears",
      "twist": "the 90 minutes is already at the ceiling",
      "carrier": "both",
      "position": "opener",
      "representativeness": "median",
      "rung": "R1",
      "provenance": ["c-002"]
    }
  ],
  "gaps": [
    { "slot_id": "s2", "gap_type": "missing causal link", "disposition": "DECLARE" }
  ],
  "dead_column": [
    {
      "claim_id": "c-091",
      "killed_by": "instrument check",
      "reason": "did_not_support"
    },
    {
      "claim_id": "c-133",
      "killed_by": "graveyard pass",
      "reason": "CONTRADICTED"
    }
  ],
  "hypothesis_diff": {
    "before": "The 1998 stress was caused by the volume surge.",
    "after": "The 1998 stress was a timing failure the guarantee created in 1994; volume made it visible rather than causing it.",
    "what_changed": "The frozen inventory put two fails-to-deliver spikes before the volume surge, which the original hypothesis could not accommodate."
  }
}
```

Note what this example does **not** do. It does not fill `point_of_insight`. It ships at rung 2 with a research request naming exactly what would lift it to rung 1. Its one causal slot is tagged `L3` — sequence, not cause — and its warrant uses no causal verb. That is what a passing architecture looks like.
