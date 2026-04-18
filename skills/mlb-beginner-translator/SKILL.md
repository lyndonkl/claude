---
name: mlb-beginner-translator
description: Converts baseball and fantasy-baseball jargon into plain English for a user with zero baseball knowledge. Wraps every user-facing sentence produced by the MLB agent team (morning briefs, trade recommendations, waiver calls, chat summaries). Detects jargon terms, attaches an inline parenthetical plain-English gloss on first mention in a document, enforces the action-verb ladder (START / SIT / ADD / DROP / BID $X / ACCEPT / COUNTER / REJECT), and rejects assumed-knowledge phrases like "hot streak" or "positive matchup." Use when asked to translate for beginner, explain in plain English, translate this, write without jargon, make it beginner-friendly, or produce any user-facing MLB output for K L D'Souza's Fantasy Baseball 2K25 team.
---

# MLB Beginner Translator

## Table of Contents
- [Example](#example)
- [Workflow](#workflow)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Example

**Scenario**: The lineup-optimizer has produced a raw recommendation that needs to be rewritten for the user (K L D'Souza, zero baseball knowledge) before it ships in the morning brief.

**Before (raw, jargon-heavy)**:

> Caminero (TB 3B) has positive platoon splits vs RHP and a plus matchup vs Bello at Fenway (park factor 103 R / 105 HR). His 15-day xwOBA is .410 vs a .355 baseline, suggesting a hot streak. OBP contribution is elite given his #3 slot. daily_quality = 66. SB opportunity is middling -- Bello holds runners average but catcher CS% 28%. Regression index +15 on season wOBA gap. START over Hayes (UTIL), who faces a LHP in a bullpen game at Oracle -- negative park, low opportunity, QS unlikely (trivially, he is a hitter; what I mean is his slate has low floor). Verdict: START Caminero, SIT Hayes.

**After (beginner-translated)**:

> **Junior Caminero (Tampa Bay, third base)** -- **START** him today.
>
> Why: he hits right-handed pitchers well (most batters hit better against pitchers who throw from the opposite hand), and today's opposing pitcher (Brayan Bello) throws right-handed. The stadium (Fenway Park in Boston) also favors hitters -- it gives about 3% more runs and 5% more home runs than an average park. On top of that, Caminero has been hitting well lately (his expected-hitting quality over the last 15 days is about 15% above his season average), and he is batting third in the lineup (more times at the plate = more chances to score). Stealing a base today is a coin flip -- the Boston catcher throws out runners at a decent rate, so we are not counting on it.
>
> **Ke'Bryan Hayes (Pittsburgh, third base, in your utility slot)** -- **SIT** him today.
>
> Why: he faces a left-handed pitcher, which is the harder matchup for him, and the game is at Oracle Park in San Francisco (a cold, big-outfield park that suppresses hitting). The opposing team is also using a **bullpen game** (no single starter -- they cycle relief pitchers all game), which tends to produce fewer big hitting opportunities.
>
> **Actions:**
> - **START** Caminero at 3B.
> - **SIT** Hayes (move him to bench, BN).

**What the translator did**:

1. Detected 11 jargon terms (RHP, platoon splits, park factor, xwOBA, OBP contribution, daily_quality, SB, CS%, regression index, bullpen game, QS) and either glossed each on first use or rewrote around them.
2. Rewrote "hot streak" as "has been hitting well lately" (see [Guardrails #2](#guardrails)).
3. Dropped internal agent signals (`daily_quality = 66`, `regression_index = +15`) -- these are inputs, not output.
4. Collapsed the decision to action verbs (**START** / **SIT**) at the end.
5. Kept position abbreviations (3B, BN) only after the position was spelled out in parentheses on first use.
6. Removed the self-correction ("trivially, he is a hitter...") -- the user does not need to see the agent debating itself.

## Workflow

Copy this checklist and track progress:

```
MLB Beginner Translator Progress:
- [ ] Step 1: Receive raw draft from upstream agent
- [ ] Step 2: Scan for jargon terms (use glossary list)
- [ ] Step 3: Apply first-mention-gloss rule per term per document
- [ ] Step 4: Rewrite assumed-knowledge phrases (hot streak, plus matchup, etc.)
- [ ] Step 5: Strip internal signals and agent self-talk
- [ ] Step 6: Collapse to action verbs (START / SIT / ADD / DROP / BID $X / ACCEPT / COUNTER / REJECT)
- [ ] Step 7: Validate against rubric (resources/evaluators)
```

**Step 1: Receive raw draft from upstream agent**

Accept whatever the calling agent produced -- lineup-optimizer synthesis, trade-analyzer verdict, waiver-analyst ranking, category-strategist plan, coach's morning brief. The input can be bullet points, prose, or a signal JSON block; output is always user-facing prose plus an action list.

- [ ] Identify the document type (brief, trade memo, chat reply, alert)
- [ ] Identify every player named -- each first mention must include team and position
- [ ] Identify every recommendation -- each must end in an action verb

**Step 2: Scan for jargon terms**

Walk through the full glossary in [resources/methodology.md](resources/methodology.md#jargon-detection-checklist) and the master `context/frameworks/beginner-glossary.md` in the yahoo-mlb repo. Mark every occurrence of every term. A term can appear in five forms: full word ("On-Base Percentage"), initialism ("OBP"), compound ("OBP contribution"), slang ("hot bat"), and internal signal name ("daily_quality"). All five count as jargon.

- [ ] Category stats detected (R, HR, RBI, SB, OBP, K, ERA, WHIP, QS, SV)
- [ ] Position abbreviations detected (C, 1B, 2B, 3B, SS, OF, UTIL, SP, RP, P, BN, IL, DH)
- [ ] Matchup terms detected (RHP, LHP, platoon, park factor, probable, lineup, two-start, bullpen game, opener, streaming)
- [ ] Advanced stats detected (xwOBA, wOBA, BABIP, FIP, xFIP, SIERA, barrel rate, exit velocity)
- [ ] Transaction terms detected (FAAB, waivers, rolling waivers, H2H, punt, IL stash, DFA, handcuff)
- [ ] Archetypes detected (sleeper, bust, breakout, post-hype, innings-eater, closer committee)
- [ ] Internal signal names detected (daily_quality, form_score, matchup_score, regression_index, qs_probability, streamability_score, etc.)

**Step 3: Apply first-mention-gloss rule per term per document**

For every jargon term detected in Step 2, attach an inline parenthetical plain-English gloss the first time the term appears in the document. Subsequent mentions in the same document can use the bare term. See [resources/methodology.md](resources/methodology.md#first-mention-rule) for the rule, and [resources/template.md](resources/template.md#inline-gloss-patterns) for the gloss patterns.

- [ ] Every first mention is immediately followed by "(plain-English description)"
- [ ] Subsequent mentions do not repeat the gloss (avoids reader fatigue)
- [ ] Player names are always accompanied by team and position on first mention

**Step 4: Rewrite assumed-knowledge phrases**

The dangerous category is not unfamiliar words -- it is familiar-sounding phrases that secretly assume baseball knowledge. "Hot streak," "good matchup," "plus matchup," "tough lefty," "soft slate," "live arm," "plays the hot corner," "juicy park." Each of these requires a rewrite, not a gloss. See [resources/methodology.md](resources/methodology.md#common-traps) and [Guardrails #2](#guardrails) for the full list and rewrite patterns.

- [ ] "Hot streak" / "hot bat" -> "has been hitting well lately"
- [ ] "Plus/positive matchup" -> named concrete reason (park, opposing pitcher hand, weather)
- [ ] "Tough lefty" -> "a good left-handed pitcher"
- [ ] "Juicy park" -> "a stadium that favors hitters (specific park named)"
- [ ] "Bat flip / gas / heater / nasty" -> rewrite in literal terms

**Step 5: Strip internal signals and agent self-talk**

Internal signal values (numeric `daily_quality`, `regression_index`, `streamability_score`) are inputs to the decision, not content for the user. Drop them. Also drop any self-correction, debate remnants, or variant labels ("the advocate says... the critic says... synthesis is..."). The user sees only the synthesized answer.

- [ ] Numeric signal values removed from user-facing prose
- [ ] Variant labels removed ("advocate / critic / synthesis")
- [ ] Self-corrections removed ("trivially," "what I mean is," "to be clear")
- [ ] Confidence labels kept only if expressed in plain English ("high confidence" ok; "confidence: 0.72" not ok)

**Step 6: Collapse to action verbs**

Every recommendation must end in one of the approved action verbs with no hedging. No "consider," "think about," "might want to," "could try." See the full ladder in [CLAUDE.md](/Users/kushaldsouza/Documents/Projects/yahoo-mlb/CLAUDE.md) rule 6. If the upstream agent hedged, collapse the hedge into a single verb plus an explicit fallback action.

- [ ] Every recommendation ends in: START / SIT / ADD / DROP / BID $X / ACCEPT / COUNTER (with suggested counter) / REJECT
- [ ] A dedicated "Actions" bullet list appears at the end of every user-facing output
- [ ] Hedges ("consider," "think about") replaced with a concrete verb + fallback

**Step 7: Validate against rubric**

Score the translated output against [resources/evaluators/rubric_mlb_beginner_translator.json](resources/evaluators/rubric_mlb_beginner_translator.json). Minimum standard: average score of 4.0, and no criterion scored below 3. If the action-verb criterion or the first-mention-rule criterion scores below 4, revise before shipping.

- [ ] Rubric scored, every criterion at 3 or higher
- [ ] Average at 4.0 or above
- [ ] Action-verb and first-mention-rule criteria at 4 or higher

## Common Patterns

**Pattern 1: Daily lineup brief (morning)**
- **Input shape**: list of players with daily_quality scores, matchup notes, confirmed/unconfirmed lineup status
- **Output shape**: one short paragraph per player, then a consolidated action list at the end
- **Critical rewrites**: `daily_quality` score dropped; matchup terms (park factor, RHP/LHP, platoon) glossed; "confirmed" explained as "in today's lineup card"
- **Ends in**: START / SIT per player, with position slot named

**Pattern 2: Trade recommendation memo**
- **Input shape**: trade offer (players in / players out), category impact table, synthesis from mlb-trade-analyzer
- **Output shape**: one-line summary of the offer, short "why" in plain English, a category impact paragraph ("you gain power, you lose speed"), then a single action verb
- **Critical rewrites**: category names spelled out (HR -> home runs; SV -> saves by relief pitchers); archetypes (sleeper, breakout) translated; roster fit (SS / OF eligibility) explained
- **Ends in**: ACCEPT / COUNTER (with suggested counter) / REJECT

**Pattern 3: Waiver / FAAB add memo**
- **Input shape**: player recommendation, FAAB bid, category gap filled, drop candidate
- **Output shape**: why the player is available (injury to starter, breakout, etc.), how much to bid in dollars, who to drop
- **Critical rewrites**: FAAB explained on first mention; "waivers" explained; "handcuff" translated as "backup closer"; percentages expressed as "roughly X of Y starts"
- **Ends in**: BID $X on Player (drop Player Y) / PASS

**Pattern 4: Weekly category-strategy plan**
- **Input shape**: category state (leading / losing / tied), punt decisions, streaming schedule
- **Output shape**: week preview -- "here is where you stand this week" -- followed by specific category actions
- **Critical rewrites**: H2H explained; "punt" explained as "give up on a category to dominate others"; "streaming" explained as "rotating pitchers based on matchups"; QS explained
- **Ends in**: Actions for each lever (START X on Tue, DROP Y, ADD Z via FAAB)

**Pattern 5: Chat reply (ad hoc question)**
- **Input shape**: a user question ("should I drop Arraez?"), agent signals, variant debate
- **Output shape**: a 1-3 sentence answer plus the action
- **Critical rewrites**: Do not dump signals; do not narrate the agent debate; answer in the user's language
- **Ends in**: a single action verb

## Guardrails

1. **The first-mention-gloss rule is per document, not per sentence.** Once you have glossed OBP in the first paragraph, you do not re-gloss it in paragraph four of the same document -- that would annoy the reader. But if the document is a fresh morning brief, every jargon term resets. When in doubt, err toward glossing again in a new document.

2. **Watch for "hot streak" traps.** The phrase "hot streak" sounds self-explanatory but assumes the user knows baseball performance is noisy and streaky. Rewrite as "has been hitting well over the last 1-2 weeks" or "has been pitching well lately." Equivalent traps: "cold streak" -> "has been struggling lately"; "plus matchup" -> name the concrete reason (opposing pitcher, park, weather); "tough lefty" -> "a good left-handed pitcher"; "juicy park" -> name the park and say "favors hitters"; "live arm" -> "throws hard with good movement."

3. **Never use an internal signal name in user output.** `daily_quality`, `form_score`, `matchup_score`, `opportunity_score`, `regression_index`, `streamability_score`, `qs_probability`, `obp_contribution`, `sb_opportunity`, `role_certainty`, `k_ceiling`, `era_whip_risk`, `two_start_bonus`, `save_role_certainty` -- all of these are internal. They are inputs to your decision, not content for the user. If you must convey the idea ("he has been unusually unlucky and is due to improve"), use plain English.

4. **Every player's first mention in a document gets team + position.** "Junior Caminero (Tampa Bay, third base)" not "Caminero." After the first mention, the last name alone is fine. Applies to every document type.

5. **Action verbs are not optional.** The user cannot interpret "consider starting Caminero if the weather holds" -- the user has no model of what "if the weather holds" means. Collapse to a primary action plus an explicit fallback: "START Caminero; if the game is postponed, swap in Hayes." No "consider," "think about," "might want to," "could try," "lean toward," "leaning," "in play."

6. **Dollars, not percentages, for FAAB.** The user has a $100 budget. Say "bid $12" not "bid 12% of remaining FAAB." If the context requires a percentage, translate to dollars explicitly.

7. **Category codes get spelled out on first use.** "HR" is not a baseball term to a beginner -- it is two letters. Write "home runs (HR)" the first time, then "HR" thereafter. Same for R, RBI, SB, K, SV, QS, and even OBP / ERA / WHIP which look familiar but are not.

8. **Do not invent jargon translations.** If an upstream agent uses a term that is not in the master glossary (`context/frameworks/beginner-glossary.md`) or the extended list in [resources/methodology.md](resources/methodology.md#jargon-detection-checklist), either (a) ask the upstream agent to rephrase, or (b) rewrite around the term using only glossary-approved words. Do not freelance a new plain-English gloss -- glossary consistency matters across briefs.

9. **Degrade gracefully on unverified facts.** If the upstream agent's draft includes a fact marked `confidence: low` or a fact that could not be web-verified, surface the uncertainty in plain English ("I could not verify the weather forecast for San Francisco today -- if the game is postponed, see fallback below"). Never hide the uncertainty.

10. **Do not add emojis or decorations.** The user asked for plain English, not performative friendliness. Bold for player names and action verbs is allowed. Emojis, smileys, and cheerleader phrases ("great pick!") are not.

## Quick Reference

**The action-verb ladder (from [CLAUDE.md](/Users/kushaldsouza/Documents/Projects/yahoo-mlb/CLAUDE.md) rule 6):**

```
START             -- put this player in your active lineup today
SIT               -- bench this player today (move to BN)
ADD               -- claim this player (via FAAB or waivers)
DROP              -- release this player from the roster
BID $X            -- submit a FAAB bid of $X (between $0 and remaining budget)
ACCEPT            -- accept the incoming trade offer as-is
COUNTER           -- reject as-is and send back a specific counter (specify the counter)
REJECT            -- reject the incoming trade offer with no counter
PASS              -- do not claim this player (alternative to ADD on waivers)
```

**The first-mention-gloss pattern:**

```
<bare term> -> <term> (<plain-English description>) on first mention in a document
             -> <bare term> on subsequent mentions in the same document
```

Example:
- First mention: "Junior Caminero's OBP (how often he gets on base via hits, walks, or hit-by-pitches) is .360."
- Later mention: "Caminero's OBP is trending up."

**Common rewrites (assumed-knowledge phrases):**

| Agent phrase | User-facing rewrite |
|---|---|
| "Hot streak" | "Has been hitting well over the last 1-2 weeks" |
| "Cold streak" | "Has been struggling lately" |
| "Plus matchup" | Name the concrete reason (park, pitcher hand, weather) |
| "Tough lefty" | "A good left-handed pitcher" |
| "Juicy park" | "Stadium that favors hitters (<park name>)" |
| "Live arm" | "Throws hard with good movement" |
| "Has the hot hand" | "Is in a good stretch of games" |
| "Good slate" | "Plays today in a favorable setup" |
| "Ace" | "One of the best starting pitchers in baseball" |
| "Stud" | "Top-tier player" |
| "Bat flip / dinger / dong" | "Home run" |
| "Gas / cheese / heater" | "Fastball" |
| "Punch out" | "Strikeout" |
| "Free pass / walk" | "Walk (pitcher gives up a base without a hit)" |

**Key resources:**

- **[resources/template.md](resources/template.md)**: Inline gloss patterns by term category (stats, positions, matchups, advanced, transactions, archetypes, signal names). Before/after translation templates for briefs, trade memos, waiver memos, chat replies.
- **[resources/methodology.md](resources/methodology.md)**: The first-mention rule, assumed-knowledge trap list, action-verb enforcement, worked before/after examples including a full lineup recommendation with jargon and without.
- **[resources/evaluators/rubric_mlb_beginner_translator.json](resources/evaluators/rubric_mlb_beginner_translator.json)**: 10-criterion rubric (jargon detection, gloss accuracy, first-mention rule, assumed-knowledge rewrites, signal stripping, action-verb presence, player identification, uncertainty surfacing, tone, overall readability).
- **Master glossary**: `/Users/kushaldsouza/Documents/Projects/yahoo-mlb/context/frameworks/beginner-glossary.md` -- authoritative source for plain-English definitions. This skill mirrors and extends it.

**Inputs required:**

- Raw draft from an upstream MLB agent (coach, lineup-optimizer, waiver-analyst, trade-analyzer, category-strategist, streaming-strategist, playoff-planner)
- The target document type (brief, trade memo, waiver memo, category plan, chat reply)
- Any `confidence: low` flags from web-search failures upstream

**Outputs produced:**

- A fully translated user-facing document: every jargon term glossed on first use, every assumed-knowledge phrase rewritten, every internal signal stripped, every recommendation collapsed to action verbs.
- A consolidated "Actions" bullet list at the end.
- Optional uncertainty notes in plain English for any unverified facts.
