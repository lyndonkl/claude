# MLB Beginner Translator Templates

Inline gloss patterns for every jargon category, plus before/after translation templates for every document type the MLB agent team produces.

## Table of Contents
- [Inline Gloss Patterns](#inline-gloss-patterns)
  - [Scoring categories (the ten)](#scoring-categories-the-ten)
  - [Position abbreviations](#position-abbreviations)
  - [Matchup and context terms](#matchup-and-context-terms)
  - [Advanced stats](#advanced-stats)
  - [Transaction and format terms](#transaction-and-format-terms)
  - [Roles and archetypes](#roles-and-archetypes)
  - [Internal signal names (strip, never gloss)](#internal-signal-names-strip-never-gloss)
- [Assumed-Knowledge Phrase Rewrites](#assumed-knowledge-phrase-rewrites)
- [Document Templates](#document-templates)
  - [Daily lineup brief](#daily-lineup-brief)
  - [Trade recommendation memo](#trade-recommendation-memo)
  - [Waiver / FAAB add memo](#waiver--faab-add-memo)
  - [Weekly category plan](#weekly-category-plan)
  - [Chat reply](#chat-reply)
- [Action-Verb Tail Patterns](#action-verb-tail-patterns)

---

## Inline Gloss Patterns

The generic first-mention pattern:

```
<Player> <Position/Team context>'s <jargon term> (<plain-English description>) is <value>.
```

Subsequent in-document mentions:

```
<Player>'s <jargon term> is <value>.
```

### Scoring categories (the ten)

| Term | First-mention gloss template |
|---|---|
| R (Runs) | "...is projected to score 4 runs (R) this week -- a run is scored whenever a player crosses home plate." |
| HR (Home Runs) | "...hit 2 home runs (HR) last week -- a home run is a ball hit out of the park for an automatic run." |
| RBI (Runs Batted In) | "...drove in 5 runs (RBI) -- an RBI is when your player's hit scores another runner." |
| SB (Stolen Bases) | "...stole 2 bases (SB) -- a stolen base is when a runner advances to the next base without a hit." |
| OBP (On-Base Percentage) | "...his OBP (how often he gets on base via hits, walks, or hit-by-pitches) is .360. Our league uses OBP instead of batting average, so walks count." |
| K (Strikeouts, pitcher) | "...posted 8 strikeouts (K) -- a K is when the pitcher retires the batter on strikes." |
| ERA (Earned Run Average) | "...his ERA (runs allowed per 9 innings -- lower is better) is 3.20." |
| WHIP (Walks + Hits per Inning Pitched) | "...his WHIP (baserunners allowed per inning -- lower is better) is 1.05." |
| QS (Quality Starts) | "...a QS is when a starting pitcher goes at least 6 innings and allows 3 or fewer earned runs. Our league uses QS instead of Wins." |
| SV (Saves) | "...picked up 3 saves (SV) -- a save is when a relief pitcher finishes a close game that their team wins." |

### Position abbreviations

On first mention, pair the abbreviation with the long form. After that, the abbreviation alone is fine within the same document.

| Term | First-mention template |
|---|---|
| C | "catcher (C) -- the player who squats behind home plate" |
| 1B / 2B / 3B | "first base (1B)" / "second base (2B)" / "third base (3B)"; thereafter "1B", "2B", "3B" |
| SS | "shortstop (SS) -- between 2nd and 3rd base" |
| OF | "outfield (OF)"; left/center/right field all count as OF |
| UTIL | "utility slot (UTIL) -- any hitter you want to slot here" |
| SP | "starting pitcher (SP)" |
| RP | "relief pitcher (RP) -- comes in after the starter" |
| P | "pitcher flex slot (P) -- can hold any pitcher type" |
| BN | "bench (BN) -- does not earn stats that day" |
| IL | "Injured List (IL) -- does not count against the active roster" |
| DH | "designated hitter (DH) -- bats but does not play defense" |

### Matchup and context terms

| Term | First-mention gloss template |
|---|---|
| RHP / LHP | "...faces a right-handed pitcher (RHP) today." / "...faces a left-handed pitcher (LHP) today." |
| Platoon split | "...most batters hit better against pitchers who throw from the opposite hand (a platoon split)." |
| Park factor | "...Coors Field in Denver is a hitter-friendly park (thin air, so more home runs)." Translate the concept in place of the term. |
| Probable pitcher | "...today's scheduled starting pitcher (the probable pitcher, posted 24-48 hours in advance) is..." |
| Confirmed lineup | "...he is in today's lineup card (posted 2-3 hours before first pitch)." |
| Two-start week | "...he is scheduled to pitch twice this fantasy week (a two-start week -- double the stats, but also double the risk)." |
| Bullpen game | "...the opposing team is using a bullpen game today (no regular starter -- they cycle relief pitchers instead)." |
| Opener | "...the opposing team is using an opener (a relief pitcher throws the first 1-2 innings, then the real starter enters)." |
| Streaming | "...streaming pitchers means rotating them in and out based on which ones have good matchups that week." |

### Advanced stats

Advanced stats are almost never needed in user output. Translate the conclusion, not the metric.

| Term | User-facing rewrite (not a gloss -- replace) |
|---|---|
| xwOBA | "his expected hitting quality based on how hard he hits the ball" -> simplify to "has been hitting the ball hard" |
| wOBA | Do not use. Say "overall hitting value" or just "has been hitting well." |
| BABIP | "how often his balls in play become hits" -> almost always translate as "has been lucky/unlucky on batted balls" |
| FIP / xFIP / SIERA | Do not use. Say "his underlying pitching has been better/worse than his ERA suggests." |
| Barrel rate | "how often he makes ideal contact" -> translate as "power contact" |
| Exit velocity | "how hard he hits the ball" |

### Transaction and format terms

| Term | First-mention gloss template |
|---|---|
| FAAB | "...spend $12 from your FAAB budget (every team gets $100 for waiver claims across the season)." |
| Waivers | "...he clears waivers (a 1-day claim window) tomorrow." |
| Rolling waivers | "...if no one bids, rolling waiver priority decides -- whoever has the highest priority gets him, and then drops to the bottom." |
| H2H Categories | "...you face one team each week and win the categories you end the week ahead in (head-to-head categories, H2H)." |
| Punt | "...punting a category means deliberately giving it up to dominate the others." |
| IL stash | "...keep an injured star in your IL slot while they recover (an IL stash) -- they do not count against your active roster." |
| DFA risk | "...he is at risk of being dropped from the team's 40-man roster (designated for assignment, DFA), which would cost him playing time." |
| Handcuff | "...the backup closer in line for saves if the current closer loses the job (called a handcuff)." |

### Roles and archetypes

| Term | First-mention gloss template |
|---|---|
| Sleeper | "...a sleeper (a player drafted later than he should be based on expected performance)." |
| Bust | "...a bust (a player drafted too high -- underperformed)." |
| Breakout | "...a breakout (a young player making a big leap)." |
| Post-hype | "...a post-hype prospect (a former top prospect who flopped but might still have it)." |
| Innings-eater | "...an innings-eater (a starter who reliably goes 6+ innings -- great for QS)." |
| Closer committee | "...a closer committee (no single pitcher owns the saves role -- saves are split, hard to predict)." |

### Internal signal names (strip, never gloss)

These are internal to the agent team. **Delete from user output.** Do not gloss them; translate the underlying conclusion instead.

`form_score`, `matchup_score`, `opportunity_score`, `daily_quality`, `regression_index`, `obp_contribution`, `sb_opportunity`, `role_certainty`, `qs_probability`, `k_ceiling`, `era_whip_risk`, `streamability_score`, `two_start_bonus`, `save_role_certainty`, `confidence`, `will_verify_on`.

| Internal signal | Underlying idea for user | Example rewrite |
|---|---|---|
| daily_quality = 66 | Strong start today | "Good setup today" |
| regression_index = +15 | Unlucky, likely to improve | "Has been unlucky lately; likely to bounce back" |
| regression_index = -12 | Hot-but-due-for-a-cooldown | "Has been hitting above his sustainable level; do not expect this to last" |
| qs_probability = 0.28 | Low chance of QS | "Unlikely to pitch deep enough for a quality start" |
| streamability_score = 32 | Do not stream | "Bad matchup for streaming this week" |
| confidence: low | Unverified fact | "I could not confirm this" |

---

## Assumed-Knowledge Phrase Rewrites

Short phrases that sound plain but secretly assume baseball literacy. These are **rewrites**, not glosses -- do not attach an aside; replace the phrase.

| Agent phrase | User-facing rewrite |
|---|---|
| "Hot streak" / "hot bat" / "hot hand" | "Has been hitting well over the last 1-2 weeks" |
| "Cold streak" / "cold stretch" / "in a slump" | "Has been struggling lately" |
| "Plus matchup" / "great matchup" | Name the concrete reason: park, pitcher hand, weather, lineup spot |
| "Tough matchup" / "bad matchup" | Same -- name the concrete reason |
| "Tough lefty" | "A good left-handed pitcher" |
| "Juicy park" / "bandbox" | "A stadium that favors hitters (<name the park>)" |
| "Pitcher's park" | "A stadium that suppresses hitting (<name the park>)" |
| "Live arm" / "electric stuff" | "Throws hard with good movement" |
| "Ace" | "One of the best starting pitchers in baseball" |
| "Stud" / "bat" / "bat with pop" | "Top-tier hitter" / "hits with power" |
| "Bat flip" / "dinger" / "dong" / "bomb" | "Home run" |
| "Gas" / "cheese" / "heater" | "Fastball" |
| "Punch out" | "Strikeout" |
| "Free pass" / "ball four" | "Walk (the pitcher gives up a base without a hit)" |
| "Slate" | "Day's games" |
| "In play" (for a recommendation) | Replace with a verb -- START / SIT / ADD |
| "Leaning toward" | Replace with a verb |
| "Solid floor" | "Unlikely to have a bad night, even if nothing exciting happens" |
| "High ceiling" | "Could have a big night" |
| "Two-way player" | "Plays in the field AND pitches" |
| "Plays the hot corner" | "Plays third base" |
| "Keystone" | "Second base" |
| "Backstop" | "Catcher" |
| "The show" | "The major leagues" |

---

## Document Templates

### Daily lineup brief

```
# Today's Lineup -- <date>

**<Player 1 Name> (<Team>, <position spelled out>)** -- **<START/SIT>**

<1-3 sentences of plain-English reasoning. First-mention-gloss any jargon. Name concrete matchup details -- opposing pitcher (including handedness), stadium, weather if relevant, lineup slot.>

**<Player 2 Name> (<Team>, <position spelled out>)** -- **<START/SIT>**

<same pattern>

... (one block per player in question)

## Actions

- **START** <Player> at <slot>
- **SIT** <Player> (move to BN)
- **START** <Player> at <slot>
...

## Unverified
(only if applicable)
- I could not confirm <fact>. If <fallback condition>, <fallback action>.
```

### Trade recommendation memo

```
# Trade Offer -- <opposing manager's team name>

**Offer:** they send you <Players IN>; you send them <Players OUT>.

**Recommendation: <ACCEPT / COUNTER / REJECT>**

## Why

<2-4 sentences. What you gain in plain English (which categories improve, who fills which slot), what you give up, whether the roster-slot math works.>

## Category impact (plain English)

- **Home runs (HR):** <gain/lose/neutral> -- <reason>
- **Stolen bases (SB):** <gain/lose/neutral> -- <reason>
- **On-base percentage (OBP):** <gain/lose/neutral> -- <reason>
- **Quality starts (QS):** <gain/lose/neutral> -- <reason>
- ... (only categories that meaningfully move)

## Action

- **<ACCEPT>**: accept as-is.
OR
- **<COUNTER>**: reject as-is and send this counter -- <specific counter-offer in plain language>.
OR
- **<REJECT>**: reject with no counter. <Optional: short reason to send if you reply.>
```

### Waiver / FAAB add memo

```
# Waiver Pickup -- <player name>

**<Player Name> (<Team>, <position spelled out>)** is available.

**Recommendation: BID $<X> (drop <Drop candidate>)** OR **PASS**.

## Why he is available

<1-2 sentences -- injury to starter, breakout, called up from the minors, dropped by another team.>

## Why you want him

<1-2 sentences -- which category he fills, where he slots on your roster.>

## The bid

- **Bid: $<X>** out of your remaining $<Y> FAAB budget.
- **Drop: <Player>** -- <reason he is droppable>.
- **Backup plan if outbid:** <alternative player or PASS>.

## Action

- **BID $<X>** on <Player> (drop <Drop candidate>).
```

### Weekly category plan

```
# Week <N> Plan -- <start date> to <end date>

**Opponent:** <opposing team>.

**Where you stand heading in:**

<1-2 sentences on category matchup -- which categories you are favored in, which are tossups, which are uphill.>

## Category-by-category plan

- **Home runs (HR):** <push / punt / hold> -- <specific action>
- **Stolen bases (SB):** <push / punt / hold> -- <specific action>
- **On-base percentage (OBP):** <push / punt / hold> -- <specific action>
- **Quality starts (QS):** <push / punt / hold> -- <specific action>
- ... (all ten, but only spend words on the ones in play)

## Actions this week

- **START** <Player> on <days>
- **SIT** <Player> on <days>
- **ADD** <Player> via FAAB -- **BID $<X>**
- **DROP** <Player>
- **STREAM** <Pitcher> for <one start> on <day>
```

### Chat reply

```
<1-3 sentences answering the user's question in plain English. First-mention-gloss any jargon. No internal signals.>

**Action: <VERB> <Player/Target>.**
```

---

## Action-Verb Tail Patterns

Every user-facing output ends in action verbs. Patterns:

**Single player, single day:**
```
Action: START Caminero at 3B.
```

**Multiple players, single day:**
```
Actions:
- START Caminero at 3B
- SIT Hayes (move to BN)
- START Skenes at SP
```

**Trade:**
```
Action: COUNTER -- offer them (Player A + Player B) for (Player C).
```

**FAAB bid:**
```
Action: BID $12 on Wilyer Abreu (drop Jake Fraley).
```

**Streaming pitcher:**
```
Actions:
- ADD Mitch Keller via FAAB -- BID $3 (drop Kyle Gibson)
- START Keller on Wednesday
- DROP Keller Thursday morning
```

**Fallback when a fact is unverified:**
```
Action: START Caminero at 3B. If the Tampa Bay game is postponed by rain, SIT him and START Hayes.
```
