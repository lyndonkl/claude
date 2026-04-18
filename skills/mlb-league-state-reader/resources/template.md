# MLB League State Reader Templates

Output formats for the two artifacts this skill produces: the overwritten `team-profile.md` and the dated signal file.

## Table of Contents
- [Team Profile Output Format](#team-profile-output-format)
- [Signal File Output Format](#signal-file-output-format)
- [Roster YAML Schema](#roster-yaml-schema)
- [Standings Table Schema](#standings-table-schema)
- [Matchup Table Schema](#matchup-table-schema)
- [FAAB Ledger Schema](#faab-ledger-schema)
- [Free Agents Table Schema](#free-agents-table-schema)
- [Degraded-Mode Note Block](#degraded-mode-note-block)

---

## Team Profile Output Format

Overwrite `~/Documents/Projects/yahoo-mlb/context/team-profile.md` with the following structure. This file is "current state" — do not preserve prior runs.

```markdown
# Team Profile — ⚾ K L's Boomers

**Refresh:** Rebuilt from Yahoo by `mlb-league-state-reader` at the start of every run. Owner of truth for "what I have right now."

## As of YYYY-MM-DD

| Field | Value |
|---|---|
| Record | W-L-T |
| Rank | N of 12 |
| Level rating | (from Yahoo, if shown) |
| Current opponent | (opponent team name) |
| FAAB remaining | $NN |
| Acquisitions used | N |
| IL slots used | N of 3 |

## Roster snapshot

```yaml
roster:
  - slot: C
    player: <name>
    mlb_team: <3-letter code>
    opp_today: <@TEX | TEX | Off | PPD | DH1/DH2>
    status: <active | BN | IL | DTD | NA | SUSP>
  # ... 26 total entries in slot order:
  # C, 1B, 2B, 3B, SS, OF, OF, OF, UTIL, UTIL,
  # SP, SP, SP, RP, RP, P, P, P, P, P,
  # BN, BN, BN, IL, IL, IL
```

## This week's matchup

| Category | Us | Them | Status |
|---|---|---|---|
| R | N | N | winning/tied/losing |
| HR | N | N | ... |
| RBI | N | N | ... |
| SB | N | N | ... |
| OBP | .xxx | .xxx | ... |
| K | N | N | ... |
| ERA | x.xx | x.xx | ... |
| WHIP | x.xx | x.xx | ... |
| QS | N | N | ... |
| SV | N | N | ... |
| **Scoreline** | **W-L-T** | | |

## Category standings (league-wide rank out of 12)

| Cat | Our rank |
|---|---|
| R | N |
| HR | N |
| RBI | N |
| SB | N |
| OBP | N |
| K | N |
| ERA | N |
| WHIP | N |
| QS | N |
| SV | N |

## Open questions

- [ ] (only present if a page failed; otherwise omit this section)
```

---

## Signal File Output Format

Write to `~/Documents/Projects/yahoo-mlb/signals/YYYY-MM-DD-league-state.md`. Must conform to `context/frameworks/signal-framework.md`.

```markdown
---
type: league-state
date: 2026-04-17
emitted_by: mlb-league-state-reader
variant_synthesis: false
variants_fired: []
confidence: 0.9
computed_at: 2026-04-17T13:42Z
source_urls:
  - https://baseball.fantasysports.yahoo.com/b1/23756/5
  - https://baseball.fantasysports.yahoo.com/b1/23756?lhst=stand
  - https://baseball.fantasysports.yahoo.com/b1/23756/matchup
  - https://baseball.fantasysports.yahoo.com/b1/23756/transactions
  - https://baseball.fantasysports.yahoo.com/b1/23756/players?status=A
degraded_pages: []                     # list any URL that failed
---

# League State — 2026-04-17

## Team state

| Field | Value |
|---|---|
| Record | 8-6-1 |
| Rank | 5 of 12 |
| Current opponent | Los Doyers |
| FAAB remaining | $86 |
| Acquisitions used | 4 |
| IL slots used | 2 of 3 |

## Roster (26 slots)

| Slot | Player | MLB | Opp today | Status |
|---|---|---|---|---|
| C | Drake Baldwin | ATL | @PHI | active |
| 1B | ... | ... | ... | ... |
| ... | ... | ... | ... | ... |

## This week's matchup (live)

| Cat | Us | Them | Status |
|---|---|---|---|
| R | 23 | 19 | winning |
| ... | ... | ... | ... |
| **Scoreline** | **4-3-3** | | |

## Category standings (league-wide)

| Cat | Rank |
|---|---|
| R | 4 |
| ... | ... |

## FAAB ledger (this season)

| Date | Player added | Player dropped | Winning bid |
|---|---|---|---|
| 2026-04-08 | <name> | <name> | $6 |
| ... | ... | ... | ... |
| **Total spent** | | | **$14** |
| **Remaining** | | | **$86** |

## Top 25 free agents (by rostered %)

| Rank | Player | Pos | MLB | Rostered % | Note |
|---|---|---|---|---|---|
| 1 | ... | ... | ... | ...% | ... |
| ... | ... | ... | ... | ... | ... |

## Notes

(If any URL was degraded, describe here exactly what's missing and what fallback was applied. Otherwise: "All five Yahoo pages fetched and parsed cleanly.")
```

---

## Roster YAML Schema

Exact schema for the `roster:` block inside `team-profile.md`. Every run must produce exactly 26 entries in the canonical slot order.

```yaml
roster:
  - slot: C            # enum: C, 1B, 2B, 3B, SS, OF, UTIL, SP, RP, P, BN, IL
    player: string     # full name as shown on Yahoo
    mlb_team: string   # 3-letter code (SEA, ATL, LAD, ...)
    opp_today: string  # "@TEX" = away, "TEX" = home, "Off" = off-day, "PPD" = postponed, "DH1"/"DH2" = doubleheader
    status: string     # enum: active, BN, IL, DTD, NA, SUSP
```

**Canonical slot order (26 entries):**

```
C, 1B, 2B, 3B, SS, OF, OF, OF, UTIL, UTIL,
SP, SP, SP, RP, RP, P, P, P, P, P,
BN, BN, BN, IL, IL, IL
```

If a slot is empty on Yahoo (uncommon — usually a dropped player not yet replaced), still emit the entry with `player: null` and `status: active`.

---

## Standings Table Schema

Two tables are extracted from `...?lhst=stand`:

**Overall standings:**

| Rank | Team | W | L | T | GB |
|---|---|---|---|---|---|
| 1 | ... | N | N | N | - |

Only record our rank and record in `team-profile.md`; full table only needs to appear in the signal file.

**Per-category ranks (our team's rank in each of the 10 cats, out of 12):**

| Cat | Our rank | League leader value | Our value |
|---|---|---|---|

---

## Matchup Table Schema

Pulled from `/matchup`. The header shows the opponent; the body shows live tallies per category.

| Column | Content |
|---|---|
| Category | R, HR, RBI, SB, OBP, K, ERA, WHIP, QS, SV |
| Us | Our running total (or rate stat) |
| Them | Opponent's running total |
| Status | `winning` if our number is better, `losing` if worse, `tied` if equal — **remember OBP is higher-is-better, ERA/WHIP is lower-is-better** |

**Scoreline**: W-L-T summing statuses across the 10 cats.

---

## FAAB Ledger Schema

Pulled from `/transactions`. Filter to rows with a bid amount (waiver claim wins). Free adds (FA→roster, no bid) do not count against FAAB.

| Column | Content |
|---|---|
| Date | YYYY-MM-DD |
| Player added | Name + position |
| Player dropped | Name (or "—" if a drop to IL without add) |
| Winning bid | `$N` |

Remaining = $100 − sum of winning bids. See [resources/methodology.md](methodology.md#faab-remaining-computation) for edge cases (failed bids, trade-related adjustments, commish overrides).

---

## Free Agents Table Schema

Top 25 from `/players?status=A`, sorted by Yahoo's default "Rostered %" descending. This is the discovery set for `mlb-waiver-analyst`; the full ranking happens downstream.

| Column | Content |
|---|---|
| Rank | 1–25 |
| Player | Name |
| Pos | Primary position(s), e.g. "SS, 2B" |
| MLB | 3-letter team code |
| Rostered % | Yahoo's ownership % |
| Note | "On IL", "Probable today", "Hot streak" — only if Yahoo shows it |

If the page shows fewer than 25 (early season, obscure league), capture everything visible and record the actual count.

---

## Degraded-Mode Note Block

When any page fails, include a structured note in the signal file's `## Notes` section. Template:

```markdown
## Notes

**Degraded pages:**

- `https://baseball.fantasysports.yahoo.com/b1/23756/transactions` — navigation timeout after 2 retries. Fallback applied: asked user for FAAB remaining directly; user reported $86. FAAB ledger detail is unavailable for this run.

**Impact on downstream agents:**

- `mlb-waiver-analyst` can still run (FAAB total known); but bid-history-based pattern detection will be skipped until next successful run.
```

Also set:
- `degraded_pages:` in frontmatter — list of failed URLs
- `confidence:` in frontmatter — drop 0.1 per degraded page (minimum 0.3)
