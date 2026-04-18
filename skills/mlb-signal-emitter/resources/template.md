# Signal File Template

This file documents the canonical shape of a signal file. Every signal written to `~/Documents/Projects/yahoo-mlb/signals/` matches this template. The `mlb-signal-emitter` skill validates every file against these rules before persisting.

## Table of Contents
- [Canonical Blank Template](#canonical-blank-template)
- [Frontmatter Field Reference](#frontmatter-field-reference)
- [Body Conventions](#body-conventions)
- [Fully Populated Validated Example](#fully-populated-validated-example)
- [Intermediate Variant File Template](#intermediate-variant-file-template)

---

## Canonical Blank Template

Copy this as the starting point for any signal file. Fill in every `<placeholder>`. Required fields are marked REQUIRED; optional fields can be omitted but should be included when applicable.

```markdown
---
# REQUIRED — one of the allowed enum values
type: <lineup | waivers | streaming | trade | category-plan | playoff-push | player | matchup | regression | two-start | closer | faab | cat-state>

# REQUIRED — ISO date (YYYY-MM-DD)
date: <YYYY-MM-DD>

# REQUIRED — skill or agent name (e.g., mlb-player-analyzer)
emitted_by: <skill-or-agent-name>

# REQUIRED — float in [0.0, 1.0]
confidence: <0.0 to 1.0>

# REQUIRED — non-empty list of URLs grounding the signal
source_urls:
  - <https://...>
  - <https://...>

# OPTIONAL but REQUIRED if this is a synthesized (final) signal
variant_synthesis: <true | false>
variants_fired: [<advocate>, <critic>]          # REQUIRED if variant_synthesis: true, len >= 1
synthesis_confidence: <0.0 to 1.0>              # REQUIRED if variant_synthesis: true

# OPTIONAL — machine timestamp (ISO 8601, UTC)
computed_at: <YYYY-MM-DDTHH:MMZ>

# OPTIONAL — red-team findings from deliberation-debate-red-teaming
red_team_findings:
  - severity: <1-5>
    likelihood: <1-5>
    score: <severity * likelihood>
    note: <short string>
    mitigation: <short string>

# OPTIONAL — provenance chain (paths to upstream signal files consumed)
consumes:
  - signals/<YYYY-MM-DD-upstream-type>.md
---

# <Human-readable title>

## Signal values

| Signal | Value | Range | Interpretation |
|---|---|---|---|
| <signal_name> | <value> | <range> | <plain-English> |

## Supporting tables

(Tables, not prose. Keep commentary terse.)

## Action ladder (if applicable)

<START | SIT | ADD | DROP | BID $X | ACCEPT | COUNTER | REJECT> — <one-line reason>
```

---

## Frontmatter Field Reference

| Field | Required | Type | Constraint |
|---|---|---|---|
| `type` | yes | enum | One of: `lineup`, `waivers`, `streaming`, `trade`, `category-plan`, `playoff-push`, `player`, `matchup`, `regression`, `two-start`, `closer`, `faab`, `cat-state` |
| `date` | yes | string | `YYYY-MM-DD` |
| `emitted_by` | yes | string | Skill or agent name; may include `/variant` suffix for intermediate dumps |
| `confidence` | yes | float | `0.0 <= x <= 1.0` |
| `source_urls` | yes | list[string] | Non-empty; each entry parses as a URL |
| `variant_synthesis` | conditional | bool | Required for final synthesized signals |
| `variants_fired` | conditional | list[string] | Required if `variant_synthesis: true`; length >= 1 |
| `synthesis_confidence` | conditional | float | Required if `variant_synthesis: true`; `0.0 <= x <= 1.0` |
| `computed_at` | optional | string | ISO 8601 UTC, e.g. `2026-04-17T13:42Z` |
| `red_team_findings` | optional | list[obj] | Each entry: `severity` (1-5), `likelihood` (1-5), `score`, `note`, `mitigation` |
| `consumes` | optional | list[string] | Paths to upstream signal files consumed |

---

## Body Conventions

1. **Tables over prose.** Per signal-framework.md, the body should be markdown tables, not paragraphs. Agents read signals; brevity helps.
2. **One "Signal values" table** listing every numeric signal with its value, declared range, and a one-line plain-English interpretation.
3. **Plain-English interpretation.** Because the end user has zero baseball knowledge (CLAUDE.md), every signal must translate to plain English at the row level. No jargon.
4. **Action ladder closer.** If the signal is directly actionable, end with a verb from `{START, SIT, ADD, DROP, BID $X, ACCEPT, COUNTER, REJECT}`.

---

## Fully Populated Validated Example

The following is a complete, validated signal file for a per-player daily signal. Every required frontmatter field is present. Every numeric signal in the body is inside its declared range. This file would pass `mlb-signal-emitter` validation cleanly and be written to `~/Documents/Projects/yahoo-mlb/signals/2026-04-17-player-caminero.md`.

```markdown
---
type: player
date: 2026-04-17
emitted_by: mlb-player-analyzer
variant_synthesis: true
variants_fired: [advocate, critic]
synthesis_confidence: 0.78
computed_at: 2026-04-17T13:42Z
confidence: 0.78
source_urls:
  - https://baseballsavant.mlb.com/savant-player/junior-caminero-687091
  - https://www.fangraphs.com/players/junior-caminero/27479/stats
  - https://www.mlb.com/gameday/2026/04/17/tb-vs-bos
  - https://www.rotowire.com/baseball/player/junior-caminero-18234
red_team_findings:
  - severity: 2
    likelihood: 3
    score: 6
    note: "Boston weather — rain probability 35% at first pitch"
    mitigation: "Re-check 1pm forecast; fallback SIT if game is postponed"
  - severity: 3
    likelihood: 2
    score: 6
    note: "Opposing starter has reverse-platoon splits this season (small sample)"
    mitigation: "matchup_score already discounted by 8 pts to reflect uncertainty"
consumes:
  - signals/2026-04-17-matchup-tb-bos.md
---

# Junior Caminero — 2026-04-17 daily signal

## Signal values

| Signal | Value | Range | Interpretation |
|---|---|---|---|
| form_score | 68 | 0-100 | Hitting better than his season average over the last 15 days (50 = average) |
| matchup_score | 74 | 0-100 | Favorable matchup: opposing starter is below-average, small-park, right-handed pitcher |
| opportunity_score | 62 | 0-100 | Batting 3rd, expected 4-5 plate appearances |
| daily_quality | 69 | 0-100 | Primary START/SIT signal. Clear start today. |
| regression_index | +18 | -100 to +100 | Slightly unlucky recently — underlying contact quality better than results |
| obp_contribution | 58 | 0-100 | Above-average on-base projection for the day |
| sb_opportunity | 22 | 0-100 | Low — Caminero rarely attempts steals |
| role_certainty | 100 | 0-100 | Confirmed in lineup (MLB.com, 12:30pm ET posting) |

## Action ladder

**START** — High daily_quality (69), confirmed in lineup, favorable matchup. Weather is the only live risk; re-check at 1pm.

## Provenance

Consumed upstream signals:
- `signals/2026-04-17-matchup-tb-bos.md` (park, weather, opposing SP)

Variant summary:
- **Advocate** (steelman starting Caminero): form trend positive, confirmed lineup, plus matchup. Score 72.
- **Critic** (steelman benching): weather risk + thin matchup margin. Score 58.
- **Synthesis**: start, but flag weather. Final daily_quality 69, synthesis_confidence 0.78.
```

---

## Intermediate Variant File Template

When an agent wants to persist the raw output of a single variant (advocate OR critic) BEFORE synthesis, use this shape. The filename carries the variant suffix.

```markdown
---
type: lineup
date: 2026-04-17
emitted_by: mlb-lineup-optimizer/advocate     # note the /variant suffix
variant_synthesis: false                       # this IS a variant, not a synthesis
confidence: 0.65
source_urls:
  - https://...
---

# Lineup — advocate variant (start everyone plausibly startable)

| Player | Recommendation | daily_quality | Rationale |
|---|---|---|---|
| ... | START | 72 | ... |
```

Filename: `signals/2026-04-17-lineup-advocate.md`. The synthesis file is still written separately as `signals/2026-04-17-lineup.md` with `variant_synthesis: true`.
