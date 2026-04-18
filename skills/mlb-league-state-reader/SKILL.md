---
name: mlb-league-state-reader
description: Parses Yahoo Fantasy Baseball league state (roster, standings, current matchup, FAAB remaining, free agents) from authenticated Yahoo team pages via Claude-in-Chrome browser automation, then grounds it against league-config.md and team-profile.md to emit a normalized league-state bundle every other agent can consume without re-scraping. Use when the coach or any downstream agent needs to read Yahoo roster, refresh team profile, pull league state, get current matchup, check FAAB remaining, list free agents, or when user mentions "what's on my roster", "who am I playing this week", "how much FAAB do I have left", or "refresh my team".
---
# MLB League State Reader

## Table of Contents
- [Example](#example)
- [Workflow](#workflow)
- [Degraded Mode](#degraded-mode)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Example

**Scenario**: Morning brief run on 2026-04-17. Coach needs current roster, matchup, FAAB, and standings before launching lineup-optimizer.

**Inputs read first**:
- `~/Documents/Projects/yahoo-mlb/context/league-config.md` (league ID 23756, team 5, 12 teams, 5x5 cats)
- `~/Documents/Projects/yahoo-mlb/context/team-profile.md` (prior known roster skeleton)

**Chrome navigation sequence** (authenticated):
1. `https://baseball.fantasysports.yahoo.com/b1/23756/5` — roster with today's opponents per player
2. `https://baseball.fantasysports.yahoo.com/b1/23756?lhst=stand` — standings + category ranks
3. `https://baseball.fantasysports.yahoo.com/b1/23756/matchup` — this week's head-to-head vs Los Doyers
4. `https://baseball.fantasysports.yahoo.com/b1/23756/transactions` — FAAB spent to date → remaining
5. `https://baseball.fantasysports.yahoo.com/b1/23756/players?status=A` — top free agents (page 1)

**Extracted bundle**:

| Field | Value |
|---|---|
| Record | 8-6-1 |
| Rank | 5 of 12 |
| FAAB spent | $14 |
| FAAB remaining | **$86** |
| This week opp | Los Doyers |
| Live matchup score | 4-3-3 (us leading R, HR, K; losing OBP, ERA, WHIP) |
| Roster returned | 26 of 26 slots populated |
| Free agents top-20 | captured for waiver-analyst |

**Outputs written**:
- `context/team-profile.md` — roster snapshot updated in place (slot, player, MLB team, today's opp, status)
- `signals/2026-04-17-league-state.md` — signal file with YAML frontmatter, source_urls, confidence

Every downstream agent (lineup-optimizer, waiver-analyst, category-strategist) now reads this signal file and team-profile.md rather than re-scraping Yahoo.

## Workflow

Copy this checklist and track progress:

```
League State Reader Progress:
- [ ] Step 1: Read context files (league-config.md + team-profile.md)
- [ ] Step 2: Pull Yahoo pages via Claude-in-Chrome (5 URLs)
- [ ] Step 3: Parse roster, standings, matchup, FAAB, free agents
- [ ] Step 4: Update team-profile.md in place
- [ ] Step 5: Emit signal file with frontmatter + source_urls
```

**Step 1: Read context files**

Load the authoritative contract and the last known state before touching Yahoo. This both verifies the league ID/URL and provides the skeleton to diff against.

- [ ] Read `~/Documents/Projects/yahoo-mlb/context/league-config.md` — confirm league ID 23756, team 5, roster shape (C/1B/2B/3B/SS/3OF/2UTIL/3SP/2RP/5P/3BN/3IL = 26), FAAB budget $100
- [ ] Read `~/Documents/Projects/yahoo-mlb/context/team-profile.md` — capture prior FAAB remaining, prior roster for diff
- [ ] Read `~/Documents/Projects/yahoo-mlb/context/frameworks/signal-framework.md` — confirm signal file format
- [ ] Read `~/Documents/Projects/yahoo-mlb/context/frameworks/data-sources.md` — confirm the 5 Yahoo URLs

**Step 2: Pull Yahoo pages via Claude-in-Chrome**

The user is already authenticated in the browser. Navigate in order; parse page text; if any step fails, jump to [Degraded Mode](#degraded-mode) for that specific URL only (do not abort the whole run). See [resources/methodology.md](resources/methodology.md#yahoo-navigation-sequence) for the exact tool-call sequence and page-parsing patterns.

- [ ] Team page: `https://baseball.fantasysports.yahoo.com/b1/23756/5`
- [ ] Standings: `https://baseball.fantasysports.yahoo.com/b1/23756?lhst=stand`
- [ ] Matchup: `https://baseball.fantasysports.yahoo.com/b1/23756/matchup`
- [ ] Transactions (for FAAB): `https://baseball.fantasysports.yahoo.com/b1/23756/transactions`
- [ ] Free agents: `https://baseball.fantasysports.yahoo.com/b1/23756/players?status=A`

**Step 3: Parse and normalize**

Extract structured data from each page. See [resources/methodology.md](resources/methodology.md#parsing-patterns) for row-level parsing logic, and [resources/methodology.md](resources/methodology.md#faab-remaining-computation) for how to reconstruct FAAB remaining from the transactions log.

- [ ] Roster: for each of 26 slots, capture `{slot, player, mlb_team, opp_today, status: active|IL|DTD|NA|BN}`
- [ ] Standings: W-L-T record, rank, per-category rank (10 cats)
- [ ] Matchup: opponent name, live scoreline by category (W-L-T across the 10 cats so far this week)
- [ ] FAAB: sum all `-$N` entries from transactions history this season; remaining = $100 - total spent
- [ ] Free agents: capture top 25 by rostered% — enough for waiver-analyst to start ranking

**Step 4: Update team-profile.md in place**

See [resources/template.md](resources/template.md#team-profile-output-format) for the exact output shape. Overwrite the existing file (not append); this file is meant to always reflect "as of the latest run."

- [ ] Header: `## As of YYYY-MM-DD`
- [ ] State table: record, rank, FAAB remaining, current opponent, acquisitions used, IL slots used
- [ ] Roster snapshot: full 26-slot YAML block
- [ ] Open questions: empty unless a page failed

**Step 5: Emit signal file**

Write `~/Documents/Projects/yahoo-mlb/signals/YYYY-MM-DD-league-state.md` with YAML frontmatter per the signal framework. Every URL navigated must appear in `source_urls`. Degraded fetches drop `confidence` to 0.5; full-failure fields drop to 0.3 and are flagged. See [resources/template.md](resources/template.md#signal-file-output-format).

- [ ] Frontmatter: `type: league-state`, `date`, `emitted_by: mlb-league-state-reader`, `confidence`, `source_urls[]`
- [ ] Body: roster table, standings table, matchup table, FAAB ledger, top-25 free agents
- [ ] Validate via `mlb-signal-emitter` before writing (if that skill is available in this run); otherwise write directly

## Degraded Mode

Chrome can fail for several reasons: tab not open, session expired, Yahoo rate-limiting, 500 error, unreadable DOM. **Never abort the whole run.** Fail gracefully per-URL.

**Per-URL fallback decision tree:**

| Failure | Fallback |
|---|---|
| Navigation error / timeout | Retry once. If still failing, ask user: "Paste the contents of `{URL}` and I'll parse from that." |
| Session expired (login page returned) | Ask user: "Please log into Yahoo in your Chrome tab, then say 'retry'." Do not attempt to re-authenticate. |
| Page loads but parse fails (unknown layout) | Dump the first ~4000 chars of `get_page_text` into the signal file under `raw_capture:` and drop confidence to 0.4 for that field. |
| Free-agents page gated / empty | Mark `free_agents: []` and flag in the signal. The waiver-analyst can still run on roster + standings. |
| Transactions page gated | Ask user: "What's your FAAB remaining right now? Visible at the top of the transactions page." Accept user value; mark `faab_confidence: 0.6`. |

**User-paste template** (reuse for any Yahoo page):

> "I couldn't reach `{URL}`. Please copy the visible table on that page (select all, paste into chat) and I'll extract the fields I need from your paste."

Parse the pasted text with the same regex/row patterns as the live page. See [resources/methodology.md](resources/methodology.md#paste-parsing).

## Guardrails

1. **Never assume the roster is still what it was yesterday.** Waivers clear daily and trades can fire any time. Always re-read the Yahoo team page at the start of every run, even if `team-profile.md` looks fresh.

2. **FAAB remaining is derived, not displayed.** Yahoo's UI sometimes shows "FAAB Balance" and sometimes doesn't. The authoritative computation is: `$100 minus sum of all winning bids on the transactions page this season`. Do not trust a single visible number over the ledger.

3. **Cite every URL.** The signal file's `source_urls:` list must contain every Yahoo page actually visited. If a page was skipped because of degradation, note it in the signal body, not silently.

4. **Do not re-scrape downstream.** Once this skill has emitted today's league-state signal, lineup-optimizer / waiver-analyst / category-strategist MUST read that signal rather than re-visit Yahoo. Re-scraping wastes tokens and risks drift.

5. **Overwrite team-profile.md; append nowhere.** This file is "current state." Preserving yesterday's roster pollutes it. The append-only log lives in `tracker/decisions-log.md`, not here.

6. **Status values are normalized enums.** Map Yahoo's labels (`P`, `DTD`, `IL-10`, `IL-60`, `NA`, `SUSP`) to the normalized enum: `active | BN | IL | DTD | NA | SUSP`. Downstream agents branch on the enum, not Yahoo's strings.

7. **Today's opponent may be blank.** Off-days, postponements, and doubleheaders all produce unusual `opp_today` values. Record exactly what Yahoo shows (`@TEX`, `TEX`, `Off`, `PPD`, `DH1/DH2`) — do not normalize away information the downstream lineup-optimizer needs.

8. **Don't emit a signal with zero source URLs.** If every page failed, write an empty-body signal with `confidence: 0.0` and a prominent note to the coach: "Could not reach Yahoo — paste or retry required before any downstream agent runs."

## Quick Reference

**The five Yahoo URLs (from `context/frameworks/data-sources.md`):**

```
Team:         https://baseball.fantasysports.yahoo.com/b1/23756/5
Standings:    https://baseball.fantasysports.yahoo.com/b1/23756?lhst=stand
Matchup:      https://baseball.fantasysports.yahoo.com/b1/23756/matchup
Transactions: https://baseball.fantasysports.yahoo.com/b1/23756/transactions
Free agents:  https://baseball.fantasysports.yahoo.com/b1/23756/players?status=A
```

**Chrome tool order (load via `ToolSearch` first, then call):**

```
1. mcp__claude-in-chrome__tabs_context_mcp    (confirm active tab, auth state)
2. mcp__claude-in-chrome__navigate            (go to URL)
3. mcp__claude-in-chrome__get_page_text       (extract DOM text)
4. mcp__claude-in-chrome__read_page           (structured read if text fails)
```

**Roster slot order (for team-profile YAML; matches `league-config.md`):**

```
C, 1B, 2B, 3B, SS, OF, OF, OF, UTIL, UTIL, SP, SP, SP, RP, RP, P, P, P, P, P, BN, BN, BN, IL, IL, IL
```

**Status enum mapping:**

| Yahoo | Normalized |
|---|---|
| (blank) / P | `active` |
| BN | `BN` |
| DTD | `DTD` |
| IL-10 / IL-60 / IL | `IL` |
| NA | `NA` |
| SUSP | `SUSP` |

**Signal frontmatter (minimum fields):**

```yaml
---
type: league-state
date: 2026-04-17
emitted_by: mlb-league-state-reader
variant_synthesis: false
confidence: 0.9
source_urls:
  - https://baseball.fantasysports.yahoo.com/b1/23756/5
  - https://baseball.fantasysports.yahoo.com/b1/23756?lhst=stand
  - https://baseball.fantasysports.yahoo.com/b1/23756/matchup
  - https://baseball.fantasysports.yahoo.com/b1/23756/transactions
  - https://baseball.fantasysports.yahoo.com/b1/23756/players?status=A
---
```

**Key resources:**

- **[resources/template.md](resources/template.md)**: team-profile.md output format, signal file output format, roster YAML schema, free-agents table schema
- **[resources/methodology.md](resources/methodology.md)**: Yahoo navigation sequence, parsing patterns per page, FAAB reconstruction, paste parsing, degraded-mode prompts
- **[resources/evaluators/rubric_mlb_league_state_reader.json](resources/evaluators/rubric_mlb_league_state_reader.json)**: 8 scoring criteria (roster completeness, FAAB accuracy, URL citation, fallback handling, etc.)

**Inputs required:**

- Authenticated Yahoo Fantasy session in Chrome (user's responsibility)
- `context/league-config.md` (league ID, team ID, roster shape)
- `context/team-profile.md` (prior state, may be stub)

**Outputs produced:**

- Updated `context/team-profile.md` (overwrite; reflects today's state)
- `signals/YYYY-MM-DD-league-state.md` (with frontmatter + source_urls)
- Degraded-mode prompts to user if any page fails
