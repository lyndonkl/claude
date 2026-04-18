# Two-Start Scout -- Output Template

This file defines the output format for the `mlb-two-start-scout` skill. The skill writes a markdown file with YAML frontmatter (signal file) to `signals/YYYY-MM-DD-two-start.md`. The human-readable body below is what the `mlb-streaming-strategist` reads and what ultimately reaches the user via the coach.

---

## Signal file frontmatter template

```markdown
---
type: two-start
date: 2026-04-20                              # Monday of the fantasy week (ISO)
week_end: 2026-04-26                          # Sunday of the fantasy week (ISO)
emitted_by: mlb-two-start-scout
variant_synthesis: false                      # this skill is a data producer; streaming-strategist is the variant consumer
synthesis_confidence: 0.78                    # overall confidence across the board (lower if sources conflict)
source_urls:
  - https://www.fantasypros.com/mlb/two-start-pitchers.php
  - https://www.fangraphs.com/roster-resource/probables-grid?date=2026-04-20
  - https://www.fangraphs.com/roster-resource/probables-grid?date=2026-04-21
  - https://www.rotowire.com/baseball/weather-forecast.php
  - https://baseball.fantasysports.yahoo.com/b1/23756/players?status=A&pos=SP
red_team_findings:
  - severity: 2
    likelihood: 3
    score: 6
    note: "MIA listed Cabrera twice but opener risk flagged in recent games"
    mitigation: "Removed from board; flagged as opener-risk"
computed_at: 2026-04-19T22:14Z
---
```

---

## Body -- ranked two-start board

The body is a single markdown table ranked by `streamability_score` descending, followed by per-SP narrative blocks only for SPs the user can add (FA status) OR SPs on the user's roster (so they can decide to start both).

### Top-level table

| Rank | SP | Team | Throws | Roster status | Start 1 (date, opp, park) | Start 2 (date, opp, park) | QS prob (avg) | K ceiling (avg) | ERA/WHIP risk (avg) | Streamability | Opener risk | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Bryan Woo | SEA | R | FA | Mon 4/20 vs HOU (T-Mo, pf 70) | Sun 4/26 @ OAK (Coliseum, pf 62) | 66 | 70 | 45 | 71 | no | ADD + START both. Bid $3-5 FAAB |
| 2 | Logan Webb | SFG | R | rostered-other | Mon 4/20 @ COL (Coors, pf 20) | Sat 4/25 vs WSH (Oracle, pf 68) | 58 | 62 | 55 | 62 | no | -- not available |
| 3 | Seth Lugo | KCR | R | FA | Tue 4/21 @ DET (CoPa, pf 55) | Sun 4/26 vs NYY (Kauffman, pf 58) | 45 | 58 | 68 | 48 | no | SKIP -- NYY matchup risky |
| 4 | Ranger Suarez | PHI | L | FA | Tue 4/21 vs NYM (CBP, pf 42) | Sun 4/26 @ ATL (Truist, pf 40) | 40 | 55 | 72 | 42 | no | SKIP -- both matchups are top-10 offenses |
| -- | Sandy Alcantara | MIA | R | FA | Wed 4/23 vs STL (loanDepot, pf 60) | Mon 4/28?? (next week boundary) | -- | -- | -- | -- | yes | IGNORE -- opener risk + start 2 slips to next week |

**Column definitions:**

| Column | Meaning |
|---|---|
| Rank | Order by `streamability_score` descending |
| SP | Pitcher full name |
| Team | MLB team abbreviation |
| Throws | L or R |
| Roster status | `fa` = Yahoo free agent, `rostered-other` = on another team, `rostered-user` = already on user's team |
| Start 1 / Start 2 | Date, opposing team, park name, and park_pitcher_factor |
| QS prob (avg) | Average `qs_probability` across both starts (0-100) |
| K ceiling (avg) | Average `k_ceiling` across both starts (0-100) |
| ERA/WHIP risk (avg) | Average `era_whip_risk` across both starts (0-100, higher = worse) |
| Streamability | Final `streamability_score` (0-100), with penalties applied |
| Opener risk | `yes` if either start is flagged as opener/bullpen game |
| Verdict | Action ladder: `ADD + START both` / `ADD if SP slot open` / `START both` (if already rostered) / `SKIP` / `IGNORE` |

---

### Per-SP narrative blocks (only for actionable FAs and user-rostered SPs)

Each block follows this format:

```markdown
### {Rank}. {SP Name} -- {Team} -- Streamability {score}/100

**Roster status**: {FA / rostered-user / rostered-other}

**Start 1**: {Day Date} {home/away} {Opponent}
- Park: {Park name}, pitcher factor {n}/100 ({hitter / neutral / pitcher} park)
- Opponent offense: {top-N / middle / bottom-N} in wOBA vs {L/R}HP
- Weather: {clear / X% rain / wind {n}mph out to {CF/RF/LF}}
- Per-start signals: qs_probability {n}, k_ceiling {n}, era_whip_risk {n}
- Per-start streamability: {n}

**Start 2**: {Day Date} {home/away} {Opponent}
- Park: {Park name}, pitcher factor {n}/100
- Opponent offense: {top-N / middle / bottom-N}
- Weather: {clear / X% rain}
- Per-start signals: qs_probability {n}, k_ceiling {n}, era_whip_risk {n}
- Per-start streamability: {n}

**Aggregated streamability**: {mean} - {penalty breakdown} = **{final}/100**

**Verdict**: {action verb -- ADD $X FAAB / START both / SKIP}

**Reasoning (plain English, for coach to pass to user)**:
{One paragraph, no jargon. Translate any stat on first use. Example: "Woo pitches twice this week -- once at home vs Houston on Monday, once in Oakland on Sunday. Oakland has the worst lineup in the American League, which means Woo has a strong shot at a Quality Start (pitching 6+ innings while giving up 3 or fewer earned runs). Even if the Monday game goes sideways, the Sunday matchup is likely to save the week."}
```

---

### Footer -- dropped from board (with reason)

List SPs who appeared on the FantasyPros list but were removed, with the specific reason:

| SP | Team | Reason dropped |
|---|---|---|
| Sandy Alcantara | MIA | Opener risk -- last 5 starts average 3.8 IP |
| Jared Jones | PIT | Second start pushed to Monday next week (rotation shift) |
| (example) | OAK | Bullpen day announced for one of the two dates |

---

### Footer -- data quality notes

Brief list of any data gaps, source conflicts, or confidence caveats:

- **FantasyPros vs FanGraphs conflict**: {SP X} listed on FantasyPros but FanGraphs shows {other pitcher} on {date}. Confidence reduced to 0.5. Recommend verification Monday AM.
- **Weather**: {game} has 45% rain probability per RotoWire. Streamability penalty applied.
- **Yahoo FA scrape**: Last refreshed {timestamp}. If stale, `roster_status` may be wrong.

---

## Minimum required fields (validation checklist)

The `mlb-signal-emitter` skill rejects the signal if any of these are missing:

- [ ] Frontmatter `type: two-start`
- [ ] Frontmatter `date` and `week_end` in ISO format
- [ ] Frontmatter `source_urls` with at least FantasyPros + FanGraphs + one weather source
- [ ] Frontmatter `synthesis_confidence` between 0.0 and 1.0
- [ ] Top-level table with every two-start SP for the week (even if dropped)
- [ ] Per-SP narrative block for every FA and user-rostered SP
- [ ] Verdict column populated with an action verb for every row
- [ ] Dropped-from-board footer with reasons
- [ ] `computed_at` timestamp

## Handoff

The emitted signal file is consumed by:

- `mlb-streaming-strategist` -- runs advocate + critic variants on the two-start board, synthesizes, and red-teams
- `mlb-waiver-analyst` -- uses `streamability_score` as input to FAAB bid sizing
- `mlb-fantasy-coach` -- reads the synthesized streaming recommendation and frames it for the user via `communication-storytelling`
