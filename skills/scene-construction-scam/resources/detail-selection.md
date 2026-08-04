# The 1-of-20 Telling-Detail Cut

The discipline is subtraction, not collection. List 15 to 20 candidate details for the passage before writing a word. Score them. Keep one, occasionally two. Delete the rest, and do not demote the survivors into a list.

## The seven tests

Run all seven per candidate. PROVENANCE is a veto: it overrides every other score, and there is no override on it.

| # | Test | Question | Fail action |
|---|------|----------|-------------|
| 1 | **PROVENANCE** | Is it in the record, sourced, and datable to this moment? | **Cut. Absolute veto, regardless of every other score.** |
| 2 | **LOAD** | Does it carry an inference the reader would otherwise need a full sentence of assertion to reach? | Cut. A detail that carries nothing is texture. |
| 3 | **OWNERSHIP** | Could this detail belong to any other subject in the same category? | Cut. "A busy trading floor" belongs to every trading floor. |
| 4 | **REDUNDANCY** | Does a nearby surviving detail already carry this inference? | Keep the stronger one only. |
| 5 | **EXPLANATION** | Have I attached an adjective or clause explaining what it means? | Delete the explanation. If the detail then fails, the explanation was doing the work. |
| 6 | **REPRESENTATIVENESS** | Is this typical of the pattern I am claiming, or the most extreme instance I found? | If extreme, flag it as extreme in the text, or do not use it in a load-bearing position. |
| 7 | **COUNT** | Am I keeping more than two? | You are building an inventory, not making a point. Cut to one. |

## The two failure modes

**DETAIL CONFETTI.** Six details each passed the tests, so all six were kept. The result is an inventory paragraph that reads as texture and carries no inference, and the reader skims exactly where the evidence is densest.

- Bad: "The line ran three shifts, the yard held 40,000 TEU, the gate opened at 06:00, the reefer plugs were at 92% occupancy, the crane fleet numbered eleven, and dwell time had reached 8.7 days."
- Good: "Dwell time had reached 8.7 days. The reefer plugs were at 92%, which is the number that decides whether a box can wait at all."

**INVENTED SPECIFICITY.** Under instruction to be concrete, the writer supplies a plausible-sounding detail that is not in the source. In technical, historical, and financial domains this is fabrication wearing the costume of craft. It is the single most dangerous thing this skill can produce, because it scores well on every test except the one that matters.

The scan must key on **missing pointers, never on vividness**. A vivid detail with a pointer survives no matter how good it sounds. A flat detail with no pointer is still cut. If the scan is applied by confidence rather than by provenance, it strips the genuinely reported detail that made the piece worth reading, and the writer learns to turn the scan off.

## Worked cut — engineering post-mortem

Candidates (abbreviated from 18):

| Detail | 1 Prov | 2 Load | 3 Own | Verdict |
|--------|--------|--------|-------|---------|
| The room was quiet at 03:12 | none | — | — | **Cut on veto.** Nobody logged the room. |
| The page went to the retired rotation | pagerduty audit log, evt 91d4 | high — carries the whole "nobody owned this" claim | high | **KEEP** |
| The runbook's last edit was 19 months earlier | git blame, runbooks/api.md | medium | high | Cut on redundancy: same inference, weaker |
| The on-call engineer had joined six weeks earlier | HR start date | medium | medium | Cut on count |
| Error rate hit 31% | Grafana export | belongs in the CHARACTER slot, not here | — | Belongs to SCAM C, not to the detail cut |

Kept: one. "The page went to a rotation that had been retired in March." No adjective attached. No sentence explaining that this means ownership had lapsed.

## Worked cut — biography

Candidates: the office, the light, the stacked papers, the brand of typewriter, the marginal note.

Only the marginal note has a pointer (the annotated carbon copy in the archive, box 14). Everything else is cut on the veto, no matter how much better the paragraph would read with them. The output is one detail and one sentence: "In the margin of the carbon copy she wrote *ask again in June*."

## Worked cut — market history

Candidates: the auction tail, the dealer share, the trader's mood, the screen colors, the after-hours repricing.

Mood and screen colors are cut on the veto. Dealer share and the tail both point at the same inference, so REDUNDANCY keeps the stronger one. The kept detail is the dealer share at 34.1% against a 12-month average of 17.8%, because the comparison is what carries the load. A number with no comparison on the same screen is not yet a telling detail.

## Representativeness, and why this test exists

Every technique in this skill creates pressure to promote unrepresentative material, because the most vivid case is rarely the most typical one. Applied mechanically, scene craft systematically over-weights the anecdote and under-weights the base rate.

The fix is not to ban the extreme case. It is to make the text carry the flag:

- Bad: "One shipment sat 22 days at the dock."
- Good: "One shipment sat 22 days, the longest in the sample; median dwell that month was 8.7."

The same rule applies to the whole scene. If the scene is atypical of the period it represents, the text says so on the page, not in a footnote.

## Auditing the cut as a set

Record the detail kept and the ones cut, per passage. Then review the cuts together, not one at a time.

Individual cuts are almost always defensible on length or flow. A pattern in the cuts is a different object. If the nineteen discarded details all pointed the other way from the one kept, the passage is sourced and false. This is the failure that refusal training does not catch, because subtraction never trips a refusal.
