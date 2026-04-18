# MLB League State Reader Methodology

Detailed how-to for every step of reading Yahoo Fantasy Baseball state via Claude-in-Chrome, parsing each page, and handling failures.

## Table of Contents
- [Yahoo Navigation Sequence](#yahoo-navigation-sequence)
- [Chrome Tool Loading](#chrome-tool-loading)
- [Parsing Patterns](#parsing-patterns)
  - [Team page (roster)](#team-page-roster)
  - [Standings page](#standings-page)
  - [Matchup page](#matchup-page)
  - [Transactions page (FAAB)](#transactions-page-faab)
  - [Free agents page](#free-agents-page)
- [FAAB Remaining Computation](#faab-remaining-computation)
- [Status Enum Mapping](#status-enum-mapping)
- [Chrome Failure Modes and Fallbacks](#chrome-failure-modes-and-fallbacks)
- [Paste Parsing](#paste-parsing)
- [Signal Emission and Validation](#signal-emission-and-validation)

---

## Yahoo Navigation Sequence

Always visit the five pages **in this order**, because each later step depends on context from the earlier ones:

1. **Team page** — `https://baseball.fantasysports.yahoo.com/b1/23756/5`
   - Authoritative for: roster, today's opponents per player, status flags
   - Reveals: whether the session is still authenticated (if redirected to login, stop and prompt user)

2. **Standings** — `https://baseball.fantasysports.yahoo.com/b1/23756?lhst=stand`
   - Authoritative for: W-L-T, rank, per-category league rank
   - Reveals: whether the season has started scoring yet (pre-Week 3, this page shows zeros)

3. **Matchup** — `https://baseball.fantasysports.yahoo.com/b1/23756/matchup`
   - Authoritative for: this week's opponent + live scoreline across 10 cats
   - Reveals: day-of-week position within the weekly matchup (early-week scores dominated by randomness)

4. **Transactions** — `https://baseball.fantasysports.yahoo.com/b1/23756/transactions`
   - Authoritative for: FAAB bid history → FAAB remaining
   - Also captures: trades, add/drops without bids, IL moves

5. **Free agents** — `https://baseball.fantasysports.yahoo.com/b1/23756/players?status=A`
   - Authoritative for: top-25 list for `mlb-waiver-analyst` to rank downstream

Why this order? If step 1 fails (auth), none of the rest will work either — bail early. If steps 1–3 succeed and 4 fails, downstream lineup decisions are still possible; only waiver bidding is blocked.

---

## Chrome Tool Loading

Claude-in-Chrome tools are deferred. Before any `mcp__claude-in-chrome__*` call, load the tool schema via `ToolSearch`:

```
ToolSearch(query: "select:mcp__claude-in-chrome__tabs_context_mcp,mcp__claude-in-chrome__navigate,mcp__claude-in-chrome__get_page_text,mcp__claude-in-chrome__read_page", max_results: 10)
```

Load all four at once — they will all be needed. Then the call sequence per page is:

```
1. mcp__claude-in-chrome__tabs_context_mcp      # (first page only) verify active tab and auth
2. mcp__claude-in-chrome__navigate(url=<URL>)   # goto
3. mcp__claude-in-chrome__get_page_text()       # extract text
```

If `get_page_text` returns something that looks like a login form ("Sign in to Yahoo", "Enter email"), the session is dead — go to [Chrome Failure Modes](#chrome-failure-modes-and-fallbacks).

If `get_page_text` returns the expected table but parsing fails, fall back to `mcp__claude-in-chrome__read_page` which returns a more structured accessibility-tree view.

---

## Parsing Patterns

### Team page (roster)

Yahoo's team page renders a table where each row is a roster slot. The columns (left to right) typically are:

```
Slot | Player (name, team-pos, status badge) | Opp / Game Time | Season Stats ...
```

Parsing strategy:

- **Find the roster table** by looking for the header row containing "Pos" and "Offense" or "Player" columns.
- **Iterate rows in DOM order** — Yahoo renders slots in the canonical order (C, 1B, 2B, 3B, SS, OF×3, UTIL×2, SP×3, RP×2, P×5, BN×3, IL×3).
- For each row, extract:
  - `slot`: first cell's text (e.g. "C", "1B", "Util", "BN", "IL")
  - `player`: the hyperlinked player name (first anchor in the player cell)
  - `mlb_team`: the 3-letter code that appears immediately after the player name (e.g. "ATL - C"). Take the token before " - ".
  - `opp_today`: the next cell. Preserve Yahoo's formatting — `@TEX`, `TEX`, `Off`, or `PPD`.
  - `status`: look for status badges ("DTD", "IL10", "IL60", "NA", "P"/starting, blank). Normalize via [Status Enum Mapping](#status-enum-mapping).

**Edge cases:**
- *Doubleheaders* show "DH1/DH2" or two opponent cells — record exactly as shown.
- *Empty slot* (no player): emit `player: null`, `status: active`, `mlb_team: null`, `opp_today: null`. This usually means the user dropped someone and hasn't added a replacement.
- *Slot label differences*: Yahoo shows "Util" (your output uses `UTIL`), "BN" (same), "IL" (same). Normalize to uppercase.

### Standings page

The page has two key tables: the overall standings, and an expandable "Cat Stats" view.

**Overall standings parse:**
- Find the row whose team cell contains "K L's Boomers" (or the team ID 5).
- Extract: rank (column 1), W-L-T (columns 2-4 or a combined "W-L-T" column), GB.

**Per-category rank:** Yahoo shows each team's total in each cat. To compute our rank in each cat:
- Extract all 12 teams' values for each cat.
- For rate stats (OBP: higher=better; ERA/WHIP: lower=better), sort accordingly.
- Our rank = position in the sorted list.

If the season hasn't started scoring yet (pre-Week 3 or before first game), all values will be 0 or "--". Record `rank: null` and note "season not yet scoring" in the signal.

### Matchup page

The matchup page shows a head-to-head breakdown: your team on one side, opponent on the other, 10 rows for the 10 categories.

**Parse:**
- Header row: opponent team name (look for a team link that isn't "K L's Boomers").
- 10 category rows: each has our value, opponent value, and often a visual indicator (green checkmark = winning).
- Compute `status` per row yourself (don't trust Yahoo's indicator in case of rendering oddities):
  - **Counting stats (R, HR, RBI, SB, K, QS, SV):** higher wins
  - **OBP:** higher wins
  - **ERA, WHIP:** lower wins
  - Equal → `tied`

**Scoreline:** W = count of `winning`, L = count of `losing`, T = count of `tied`. Should sum to 10.

### Transactions page (FAAB)

The transactions page lists every roster move in chronological order (newest first). Relevant types:

- **Add** with a bid amount visible (e.g., "Added <player> ($6)") → counts toward FAAB.
- **Add** without a bid (free add when no other team claimed) → does NOT count toward FAAB.
- **Drop** only → neutral.
- **Trade** → neutral for FAAB.
- **IL move** → neutral.
- **Failed bid** → Yahoo usually doesn't show these on the transactions page (only winning bids). If you see one, do NOT count it.

**Parse strategy:**
- Iterate all transaction rows filtered to our team ("K L's Boomers").
- For each row containing a `$N` token in the add line, extract: `date`, `player added`, `player dropped` (if any), `bid amount`.
- Sum all bid amounts → `FAAB spent`.
- `FAAB remaining = $100 − FAAB spent`.

### Free agents page

`/players?status=A` returns the available-players list. Default sort is typically "Rostered %" descending, which is what we want.

**Parse strategy:**
- Take the first 25 rows.
- For each row: rank (1–25 by position), player, positions (often comma-separated like "SS, 2B"), MLB team code, rostered %.
- If Yahoo shows a flag ("IL", "Probable SP today"), capture in `note`; otherwise leave blank.

Do not rank or score players here — that is `mlb-waiver-analyst`'s job. This is a capture-only step.

---

## FAAB Remaining Computation

**Formula:**

```
FAAB remaining = FAAB budget − Σ(all winning bids this season)
```

FAAB budget defaults to $100 (from `league-config.md`). Verify against Yahoo's "FAAB balance" header if visible — if they disagree, trust the ledger computation and flag the discrepancy in the signal.

**Edge cases:**

1. **Commish adjustment.** If the commissioner has manually adjusted balances, the transactions page may show an entry like "Balance adjusted by commissioner: -$5." Include this as a negative addition to "spent."

2. **Trade-related FAAB swaps.** Yahoo doesn't typically allow trading FAAB in this format, but if the league has enabled it, a trade line may show "+$10 FAAB" or "-$10 FAAB." Adjust accordingly.

3. **Ties / coin flips.** Continuous FAAB with rolling-list tiebreak means ties are broken by rolling list, not price. You still pay the bid you entered. No adjustment needed.

4. **Season restart or re-draft.** Not applicable to this league format; if it ever occurs, reset `FAAB spent = 0` and note it.

If the transactions page fails to load and Yahoo's "FAAB balance" header IS visible on the team page, use that as a fallback with `faab_confidence: 0.7` — it's usually accurate but occasionally lags by a few hours after a bid clears.

---

## Status Enum Mapping

Yahoo shows a small badge next to each player's name indicating availability. Normalize as follows:

| Yahoo badge | Normalized status | Downstream meaning |
|---|---|---|
| (blank) | `active` | Healthy, on active roster |
| P (with green dot) | `active` | Playing / starting today |
| BN | `BN` | On bench (roster slot BN) |
| DTD | `DTD` | Day-to-day (may or may not play) |
| IL10 / IL15 / IL60 | `IL` | On MLB injured list |
| NA | `NA` | Not Active (minors, COVID-IL, etc.) |
| SUSP | `SUSP` | Suspended |
| PPD | `active` + `opp_today: PPD` | Game postponed — status unchanged, opp reflects it |

**Rule:** `status` describes the player's availability, not the slot they occupy. A healthy player in the BN slot has `status: active` and `slot: BN`. An IL'd player in the IL slot has `status: IL` and `slot: IL`. An IL'd player accidentally left in the starting lineup (user error) has `status: IL` and `slot: C` (or wherever) — flag this prominently to the coach.

---

## Chrome Failure Modes and Fallbacks

| Failure | Detection | Fallback |
|---|---|---|
| No Chrome tab open | `tabs_context_mcp` returns empty or errors | Ask user: "Please open Chrome with your Yahoo Fantasy tab logged in, then say 'ready'." |
| Session expired | Page text contains "Sign in to Yahoo" or redirects to login.yahoo.com | Ask user: "Your Yahoo session expired. Please log in at `https://baseball.fantasysports.yahoo.com`, then say 'retry'." Do not attempt to auto-login. |
| Navigation timeout | `navigate` returns error or `get_page_text` is empty after timeout | Retry once. If still failing, apply [Paste Parsing](#paste-parsing) fallback for that specific URL. |
| Rate limited (429, captcha) | Page text contains "unusual activity" or captcha markers | Wait 30 seconds, retry once. If still blocked, prompt user to solve captcha manually. |
| Unknown layout (Yahoo A/B test or redesign) | Expected table markers not found | Dump first ~4000 chars of page text into signal file under `raw_capture:`, drop confidence for that page's fields to 0.4, and continue to next URL. |
| Parse error (regex misses) | Row count doesn't match expected (26 for roster, 10 for cats) | Re-fetch using `read_page` (accessibility tree) instead of `get_page_text`. If still wrong, fall back to paste parsing. |

**Golden rule:** Never silently drop a page. Every failure must appear in `degraded_pages:` in the signal frontmatter and be described in the `## Notes` section of the signal body.

---

## Paste Parsing

When a Yahoo page can't be fetched, ask the user to paste the page's contents. Standard prompt:

> "I couldn't reach `<URL>`. Please open that page in your browser, select all (Cmd-A), copy (Cmd-C), and paste it into the chat. I'll extract what I need."

Parsing the paste uses the same logic as live-page parsing — Yahoo's text rendering is consistent whether captured via Chrome automation or copy-paste. Apply the same patterns from [Parsing Patterns](#parsing-patterns).

**User-friendliness:**
- If the paste is very long (>10,000 chars), tell the user it's fine — you'll just extract what's relevant.
- If the paste is obviously truncated (stops mid-table), ask them to scroll and paste the rest.
- If the paste is from the wrong page (e.g., they pasted the league home instead of transactions), note it politely and ask for the right one.

Mark fields populated from paste with `confidence: 0.85` (slightly lower than live fetch because paste may miss hidden/collapsed rows).

---

## Signal Emission and Validation

Before writing the signal file, validate it against `context/frameworks/signal-framework.md`:

1. **Frontmatter present and valid YAML.** Keys required: `type`, `date`, `emitted_by`, `confidence`, `source_urls`, `computed_at`.
2. **`type` must be `league-state`.**
3. **`confidence` in [0.0, 1.0].** Typical values:
   - All five pages fetched cleanly: **0.9**
   - One page degraded or pasted: **0.8**
   - Two or more pages degraded: **0.6**
   - FAAB uncertain: **0.6**
   - Everything failed: **0.3** (still write the signal, as a record of the failure)
4. **`source_urls` must list every URL actually visited** (including failed attempts, marked in the body).
5. **`degraded_pages` must list every URL that failed** (so downstream agents can decide whether to trust this signal).

If the `mlb-signal-emitter` skill is available in this run, invoke it to validate before write. Otherwise, write directly and note in `tracker/decisions-log.md` that validation was skipped.

**File path:** `~/Documents/Projects/yahoo-mlb/signals/YYYY-MM-DD-league-state.md` — one signal per day. If two runs happen on the same day, overwrite (the newer is more accurate). Do not append.

**Downstream contract:** Once this signal exists for today, every other agent must read it instead of re-scraping Yahoo. This is the single source of truth for league state until tomorrow.
