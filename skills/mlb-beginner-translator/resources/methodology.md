# MLB Beginner Translator Methodology

The rules, procedures, and worked examples that turn a raw jargon-heavy draft from an upstream MLB agent into a user-facing document that a zero-baseball-knowledge user (K L D'Souza) can act on.

## Table of Contents
- [Core Rules](#core-rules)
  - [First-mention rule](#first-mention-rule)
  - [Action-verb rule](#action-verb-rule)
  - [Internal-signal strip rule](#internal-signal-strip-rule)
  - [Player-identification rule](#player-identification-rule)
- [Jargon Detection Checklist](#jargon-detection-checklist)
- [Common Traps (assumed-knowledge phrases)](#common-traps-assumed-knowledge-phrases)
- [Worked Examples](#worked-examples)
  - [Example 1: Single player analysis paragraph](#example-1-single-player-analysis-paragraph)
  - [Example 2: Full lineup recommendation (mandatory)](#example-2-full-lineup-recommendation-mandatory)
  - [Example 3: Trade memo](#example-3-trade-memo)
  - [Example 4: Waiver memo with unverified fact](#example-4-waiver-memo-with-unverified-fact)
- [Common Failure Modes](#common-failure-modes)

---

## Core Rules

### First-mention rule

**The rule:**

> The first time a jargon term appears in a document, it must be immediately followed by a parenthetical plain-English gloss. Every subsequent mention of the same term **in the same document** can use the bare term alone.

**Why it matters:** A gloss on every mention becomes noise that the reader learns to skip -- and then misses the real content. A gloss only on the first mention rewards attention to the early paragraphs and lets the rest read cleanly.

**How to apply:**

1. Scan the document top-to-bottom. Build a running set of "already-glossed" terms as you go.
2. For each jargon term encountered:
   - If the term is not in the set: add a gloss; add the term to the set.
   - If the term is in the set: leave the bare term alone.
3. Each new document starts with an empty set. Yesterday's brief having glossed OBP does not excuse today's brief from glossing OBP.

**Canonical example:**

> **Junior Caminero's OBP (how often he gets on base via hits, walks, or hit-by-pitches) is .360**, well above the league average of .315. His OBP has been trending up over the last two weeks.

First mention of OBP carries the gloss. The second mention in the next sentence is bare.

**Edge cases:**

- **Two terms in one sentence on first mention:** gloss both, but do not stack two parentheticals inside one phrase -- split into two sentences if needed.
- **A term buried in an action verb tail:** if "ADD via FAAB" is the first FAAB mention in the document, the gloss belongs inline with that bullet: "ADD via FAAB (the $100 season-long waiver budget)."
- **Player names with team/position:** the team + position spelling-out is a first-mention rule too, and runs in parallel to the jargon gloss rule. "Junior Caminero (Tampa Bay, third base)" on first mention; "Caminero" thereafter.

### Action-verb rule

**The rule:**

> Every user-facing recommendation ends in an approved action verb with no hedging. Every document ends in an "Actions" list.

**The approved verbs:** `START`, `SIT`, `ADD`, `DROP`, `BID $X`, `ACCEPT`, `COUNTER` (with the specific counter stated), `REJECT`, `PASS`.

**Forbidden hedges:** "consider," "think about," "might want to," "could try," "lean toward," "leaning," "in play," "worth a look," "on the radar."

**How to apply:**

1. Read the upstream agent's recommendation. If it already ends in a single approved verb, keep it.
2. If the upstream hedged, collapse to a primary verb plus an explicit fallback if a contingency is real.
   - Do: "**START** Caminero at 3B. If the game is postponed by rain, **SIT** him and **START** Hayes."
   - Do not: "Consider starting Caminero if the weather holds."
3. The final block of every document is an "Actions" list, even if only one action. Consistency matters.

### Internal-signal strip rule

**The rule:**

> Internal signal names and numeric signal values never appear in user output. They are inputs to the decision, not content for the user.

**The list to strip:** `form_score`, `matchup_score`, `opportunity_score`, `daily_quality`, `regression_index`, `obp_contribution`, `sb_opportunity`, `role_certainty`, `qs_probability`, `k_ceiling`, `era_whip_risk`, `streamability_score`, `two_start_bonus`, `save_role_certainty`, `confidence: <value>`, `will_verify_on: <date>`, variant labels (advocate / critic / synthesis).

**How to apply:**

1. Find each internal signal name in the draft. Read the surrounding sentence to extract the underlying idea.
2. Replace the signal reference with a plain-English description of the idea. Map table:
   - `daily_quality >= 60` -> "good setup today"
   - `daily_quality < 40` -> "bad setup today"
   - `regression_index > +10` -> "has been unlucky; likely to bounce back"
   - `regression_index < -10` -> "has been hitting above a sustainable level; do not expect this to last"
   - `qs_probability < 0.35` -> "unlikely to pitch deep enough for a quality start"
   - `streamability_score < 50` -> "bad streaming option this week"
   - `confidence: low` -> "I could not confirm this"
3. Delete variant labels ("the advocate says...") and keep only the synthesized conclusion.

### Player-identification rule

**The rule:**

> Every player's first mention in a document includes their team and their position spelled out in plain English. After the first mention, the last name alone is fine.

**Format:** `<Full Name> (<Team city or team>, <position spelled out>)`.

**Examples:**
- "Junior Caminero (Tampa Bay, third base)"
- "Paul Skenes (Pittsburgh, starting pitcher)"
- "Wilyer Abreu (Boston, outfield)"

After first mention: "Caminero," "Skenes," "Abreu."

---

## Jargon Detection Checklist

Walk the draft and tag every occurrence of every term below. Use the [template.md gloss patterns](template.md#inline-gloss-patterns) for first-mention glosses. For internal signals, apply the [strip rule](#internal-signal-strip-rule).

**Category stats (the ten):** R, HR, RBI, SB, OBP, K, ERA, WHIP, QS, SV. Also: "batting average," "OPS," "AVG," "SO" -- translate these as well even though our league does not score them.

**Position abbreviations:** C, 1B, 2B, 3B, SS, OF, LF, CF, RF, UTIL, SP, RP, P, BN, IL, DH.

**Matchup and context:** RHP, LHP, RHB, LHB, platoon split, park factor, probable pitcher, confirmed lineup, two-start week, bullpen game, opener, streaming, split, handedness, L/R, R/R, lineup spot, batting order, leadoff, cleanup, PA, AB, IP.

**Advanced stats:** xwOBA, wOBA, xBA, BABIP, FIP, xFIP, SIERA, barrel rate, barrel%, exit velocity, EV, launch angle, hard-hit rate, HH%, K%, BB%, K/9, BB/9, HR/9, GB%, FB%, LOB%, CSW%, chase rate, whiff rate, zone contact, pull%.

**Transaction and format:** FAAB, waivers, rolling waivers, H2H, categories, punt, IL stash, DFA, handcuff, 40-man, 60-day IL, optioned, recalled.

**Archetypes:** sleeper, bust, breakout, post-hype, innings-eater, closer committee, ace, stud, workhorse, glass cannon, flier.

**Internal signals (STRIP):** form_score, matchup_score, opportunity_score, daily_quality, regression_index, obp_contribution, sb_opportunity, role_certainty, qs_probability, k_ceiling, era_whip_risk, streamability_score, two_start_bonus, save_role_certainty, confidence, will_verify_on.

---

## Common Traps (assumed-knowledge phrases)

These are phrases that sound conversational but silently assume baseball literacy. Always rewrite -- do not gloss.

| Trap phrase | What it assumes | Rewrite |
|---|---|---|
| "Hot streak" / "hot bat" / "hot hand" | The user knows that baseball performance is noisy and that "hot" means "recently above baseline" | "Has been hitting well over the last 1-2 weeks" |
| "Cold streak" / "in a slump" | Same | "Has been struggling lately" |
| "Plus matchup" / "great matchup" / "soft matchup" | The user can mentally assemble park + pitcher + weather into a value judgment | Name the actual components: "today's game is at Coors Field in Denver, which favors hitters, and the opposing pitcher is a weaker starter" |
| "Tough matchup" / "bad matchup" | Same | Name the components |
| "Tough lefty" | The user knows lefty = left-handed pitcher and that this is a problem for left-handed batters | "A good left-handed pitcher (and our hitter bats left-handed, which is the harder matchup for him)" |
| "Juicy park" / "bandbox" | The user knows that some parks inflate offense | "A stadium that favors hitters (name the park)" |
| "Pitcher's park" | Same, inverted | "A stadium that suppresses hitting (name the park)" |
| "Live arm" / "electric stuff" / "nasty" | The user can translate pitcher-quality adjectives | "Throws hard with good movement" |
| "Ace" | The user knows there is a tier system among starters | "One of the best starting pitchers in baseball" |
| "Stud" / "bat" / "big bat" | Same, for hitters | "Top-tier hitter" / "hits with power" |
| "Plays the hot corner" | The user knows baseball position slang | "Plays third base" |
| "Keystone" | Same | "Second base" |
| "Backstop" | Same | "Catcher" |
| "Has a good slate" | The user knows "slate" = the day's set of games | "Has a favorable day of games" |
| "Solid floor" | The user knows floor-vs-ceiling fantasy-speak | "Unlikely to have a bad night, even if nothing exciting happens" |
| "High ceiling" | Same | "Could have a big night" |
| "Two-way player" | The user knows Ohtani-style roles | "Plays in the field AND pitches" |

**Rule of thumb:** if the agent drafted a phrase and your hand hovered near a parenthetical, ask whether the phrase itself is assuming anything. If yes, rewrite the phrase; do not bolt on a gloss.

---

## Worked Examples

### Example 1: Single player analysis paragraph

**Before:**

> Caminero has positive platoon splits vs RHP and a plus matchup at Fenway today. 15-day xwOBA .410 (baseline .355) suggests a hot streak. OBP contribution is elite given #3 slot. daily_quality = 66. regression_index = +15.

**After:**

> **Junior Caminero (Tampa Bay, third base)** has a good setup today. The opposing pitcher (Brayan Bello) throws right-handed, and Caminero hits right-handed pitchers well -- most batters hit better against pitchers who throw from the opposite hand (a platoon split). Today's game is also at Fenway Park in Boston, which slightly favors hitters. He has been hitting well over the last two weeks, and he is batting third in the lineup, which means more plate appearances (more chances to score). His OBP (how often he gets on base via hits, walks, or hit-by-pitches) has been trending up.

**What changed:**
- Player named with team + position on first mention.
- "positive platoon splits vs RHP" glossed inline ("most batters hit better... a platoon split").
- "Plus matchup" replaced with concrete components (right-handed pitcher, park).
- "Hot streak" rewritten ("has been hitting well over the last two weeks").
- "xwOBA .410 vs baseline .355" rewritten as the underlying idea.
- "OBP contribution" stripped; OBP itself glossed on first mention.
- "daily_quality = 66" stripped; replaced with "good setup today."
- "regression_index = +15" stripped; the trend idea was already captured.

### Example 2: Full lineup recommendation (mandatory)

This is the canonical before/after for a full lineup brief. Every rule in this document is applied.

**Before (raw from lineup-optimizer synthesis):**

> ## Morning Lineup -- 2026-04-17
>
> Active roster call for tonight's slate. Six games impact our roster.
>
> **Caminero (TB 3B)** -- daily_quality 66, regression_index +15. Platoon vs RHP (Bello), Fenway park factor 103 R / 105 HR, 15-day xwOBA .410. Hot bat, confirmed #3 slot. obp_contribution 62. sb_opportunity 35 (Bello holds avg, BOS catcher CS% 28%). role_certainty 100. START.
>
> **Hayes (PIT UTIL)** -- daily_quality 31, regression_index -4. Faces LHP (Webb SF), Oracle negative park (92 R / 85 HR). Bullpen game indicated, lineup unconfirmed. SIT, move to BN.
>
> **Witt Jr. (KC SS)** -- daily_quality 72. Plus matchup vs a weak RHP at Kauffman, sb_opportunity 78 (catcher CS% 18%, sprint 30.1 ft/s). Hot streak continuing. START.
>
> **Abreu (BOS OF)** -- daily_quality 58. Platoon vs LHP today (Eflin TB), actually strong vs lefties per splits. Neutral park, confirmed. Borderline START; synthesis leans advocate.
>
> **Skenes (PIT SP)** -- qs_probability 0.62, k_ceiling 78, streamability_score 74. Two-start week with SF and ARI. start2_bonus = +12. Ace stuff, confirmed starter. START.
>
> **Bowden Francis (TOR SP)** -- at COL. streamability_score 32, qs_probability 0.28, era_whip_risk 82. Coors kills everyone. SIT / DO NOT STREAM.
>
> Variant synthesis: advocate and critic agreed on Caminero, Witt, Skenes (confidence high). Critic flagged Hayes as higher-variance than daily_quality suggests -- consider alternative if needed.

**After (user-facing):**

> # Today's Lineup -- Friday, April 17, 2026
>
> Six of your players have games tonight. Here is who to start and who to sit.
>
> **Junior Caminero (Tampa Bay, third base)** -- **START** him at third base.
>
> Today's opposing pitcher (Brayan Bello) throws right-handed, and Caminero hits right-handed pitchers well (most batters hit better against pitchers who throw from the opposite hand). The game is at Fenway Park in Boston, which slightly favors hitters. He has been hitting well over the last two weeks and is batting third in the lineup (more times at the plate = more chances to score). He is already in tonight's lineup card, so there is no risk of a late scratch.
>
> **Ke'Bryan Hayes (Pittsburgh, in your utility slot)** -- **SIT** him tonight (move to bench, BN).
>
> He faces a left-handed pitcher tonight (Logan Webb), which is the harder matchup for him. The game is at Oracle Park in San Francisco, a cold, big-outfield stadium that suppresses hitting. On top of that, the opposing team is using a bullpen game (no regular starter -- they cycle relief pitchers all game), which tends to reduce the big hitting opportunities we look for. His lineup spot is not yet confirmed either.
>
> **Bobby Witt Jr. (Kansas City, shortstop)** -- **START** him at shortstop.
>
> He faces a weaker right-handed pitcher at Kauffman Stadium in Kansas City. The opposing catcher does not throw out baserunners often, and Witt is one of the fastest runners in the league, so there is a real chance he steals a base today. He has been hitting well lately.
>
> **Wilyer Abreu (Boston, outfield)** -- **START** him in the outfield.
>
> He faces a left-handed pitcher tonight, which is normally the harder matchup for a left-handed hitter -- but Abreu has actually been hitting left-handed pitchers well this season, so we are comfortable starting him. The stadium does not meaningfully help or hurt, and he is in tonight's lineup card.
>
> **Paul Skenes (Pittsburgh, starting pitcher)** -- **START** him as a starting pitcher.
>
> Skenes is one of the best starting pitchers in baseball. He is also scheduled to pitch twice this fantasy week (a two-start week -- double the stats, double the risk, but the upside here is clearly worth it), first against San Francisco and then against Arizona. Both matchups look good. He is confirmed as the starting pitcher tonight.
>
> **Bowden Francis (Toronto, starting pitcher)** -- **SIT** him (move to bench).
>
> He is pitching at Coors Field in Denver tonight. Coors Field is the most hitter-friendly park in baseball (thin air at altitude, so balls travel farther and more turn into home runs). Even good pitchers tend to get hit hard there. We never start a pitcher at Coors unless we have no other option.
>
> ## Actions
>
> - **START** Caminero at 3B
> - **SIT** Hayes (move to BN)
> - **START** Witt Jr. at SS
> - **START** Abreu in OF
> - **START** Skenes at SP
> - **SIT** Francis (move to BN)

**What changed (checklist):**

- Every player's first mention has team + full position name.
- Every jargon term was either glossed on first use (OBP-style terms did not appear in this brief, but 3B / BN / SP / OF / SS are glossed by pairing the long form with the abbreviation) or rewritten (platoon splits -> "most batters hit better against pitchers who throw from the opposite hand").
- "Hot bat" / "hot streak" / "hot streak continuing" all rewritten as "has been hitting well lately" / "has been hitting well over the last two weeks."
- "Plus matchup" replaced with concrete components (park + opposing pitcher handedness).
- "Ace stuff" rewritten as "one of the best starting pitchers in baseball."
- "Two-start week" glossed inline with the stakes explained.
- "Bullpen game" glossed inline.
- Coors Field translated instead of just named.
- All internal signals stripped: `daily_quality`, `regression_index`, `obp_contribution`, `sb_opportunity`, `role_certainty`, `qs_probability`, `k_ceiling`, `streamability_score`, `era_whip_risk`, `start2_bonus` are gone.
- Variant-synthesis paragraph deleted; only the synthesized conclusion remains.
- Every recommendation ends in START or SIT. No "borderline," no "consider," no "lean."
- Final "Actions" list consolidates.

### Example 3: Trade memo

**Before:**

> Trade offer from Team 9. Incoming: Bichette (TOR SS), Framber Valdez (HOU SP). Outgoing: Tucker (HOU OF), Pete Alonso (NYM 1B). Category impact: -7 HR, -4 RBI, +3 OBP, +1.2 SB, +0.4 QS, +2 K. Roster fit: SS upgrade (Witt is owner's 2B now, Bichette slots SS; Alonso was at 1B, we have Mountcastle as waiver replacement). Valdez is an innings-eater, adds a stable SP4. Advocate: accept, rotation is our weak category. Critic: HR hit is real, Alonso's power is scarce. Synthesis: COUNTER -- ask for a mid-tier OF back to recover HR. Suggested counter: Bichette + Valdez for Tucker + Nimmo (instead of Alonso).

**After:**

> # Trade Offer -- Team 9
>
> **Offer:** they send you Bo Bichette (Toronto, shortstop) and Framber Valdez (Houston, starting pitcher); you send them Kyle Tucker (Houston, outfield) and Pete Alonso (New York Mets, first base).
>
> **Recommendation: COUNTER.**
>
> ## Why
>
> The trade helps your pitching, where you have been losing weekly. Valdez is an innings-eater (a starter who reliably goes 6+ innings, which gives you more quality starts -- QS -- the category our league uses instead of Wins). Bichette also helps your on-base percentage (OBP, which our league uses instead of batting average -- walks count). But the trade gives up too much home-run (HR) power -- Alonso is one of the league's top HR hitters and hard to replace.
>
> ## Category impact (plain English)
>
> - **Home runs (HR):** you lose -- Alonso's power is scarce on waivers.
> - **On-base percentage (OBP):** you gain -- Bichette is an upgrade over Tucker here.
> - **Stolen bases (SB):** slight gain.
> - **Quality starts (QS):** you gain -- Valdez is a workhorse starter.
> - **Strikeouts (K):** slight gain.
>
> ## Action
>
> - **COUNTER:** reply with "Bichette + Valdez for Tucker + Brandon Nimmo (New York Mets, outfield) instead of Alonso." That lets you keep Alonso's power and still upgrade your pitching.

**What changed:** every jargon term glossed on first mention (QS, OBP, HR, SB, K, innings-eater), every player has team + position, internal category-impact numbers rewritten as plain-English gains/losses, variant debate removed, clear COUNTER with a specific counter offer.

### Example 4: Waiver memo with unverified fact

**Before:**

> Wilyer Abreu (BOS OF) FAAB call. Market eval suggests 8-12% bid, but confidence: low on whether he re-enters the lineup this week (source: RotoWire injury note unverified). daily_quality 61 when he does play. Drop candidate: Fraley (lost starting job, bench OF5). BID $9, drop Fraley.

**After:**

> # Waiver Pickup -- Wilyer Abreu
>
> **Wilyer Abreu (Boston, outfield)** is available on waivers.
>
> **Recommendation: BID $9 (drop Jake Fraley).**
>
> ## Why he is available
>
> He recently returned from a minor injury, and some managers dropped him rather than waiting. He is a solid starting outfielder when healthy.
>
> ## Why you want him
>
> He plugs into your outfield slot, and he has been hitting well against both left- and right-handed pitchers this season. He helps your home runs (HR) and on-base percentage (OBP) categories.
>
> ## The bid
>
> - **Bid: $9** out of your remaining $76 FAAB budget (every team gets $100 for waiver claims across the season -- you have $76 left).
> - **Drop: Jake Fraley** -- he has lost his starting job in Cincinnati and has been sitting on your bench.
> - **Backup plan if outbid:** PASS and revisit next week.
>
> ## Unverified
>
> I could not confirm that Abreu is definitely in the starting lineup this week -- the injury report was ambiguous. If he is still inactive by Monday, DROP him and pick up a replacement via rolling waivers (the 1-day claim window where the highest-priority team gets the player if no one FAABs).
>
> ## Action
>
> - **BID $9** on Abreu (drop Fraley).

**What changed:** `confidence: low` translated into a plain-English "Unverified" block with a specific fallback action, FAAB glossed, rolling waivers glossed, internal `daily_quality` stripped, clear BID / DROP action.

---

## Common Failure Modes

**Failure 1: First mention is glossed but so is every subsequent mention.**
- Symptom: the reader gets "OBP (how often he gets on base)" four times in one document.
- Detection: search the document for parentheticals -- if the same gloss appears twice, trim.
- Fix: build the running "already-glossed" set and enforce it.

**Failure 2: A new document reuses yesterday's glosses.**
- Symptom: today's brief says "OBP has been trending up" in paragraph 1 because "we already explained OBP yesterday."
- Detection: does paragraph 1 of today's document introduce a term without a gloss?
- Fix: reset the glossed set at the start of every new document.

**Failure 3: "Hot streak" slips through as "a gloss, not a rewrite."**
- Symptom: "has been on a hot streak (hitting well lately)" -- the phrase was detected but not excised.
- Detection: grep the final draft for any of the traps in the [trap table](#common-traps-assumed-knowledge-phrases).
- Fix: remove the trap phrase entirely; keep only the plain-English rewrite.

**Failure 4: Internal signal values leak into user output.**
- Symptom: "Caminero has a daily_quality of 66, which is strong."
- Detection: grep for `_score`, `_quality`, `_index`, `_probability`, `_ceiling`, `_risk`, `_certainty`, `confidence:`, `will_verify_on:`.
- Fix: delete the signal; replace with the underlying idea.

**Failure 5: A recommendation ends in a hedge.**
- Symptom: "consider starting Caminero if the weather holds."
- Detection: grep for "consider," "think about," "might," "could," "lean," "in play."
- Fix: collapse to a verb + explicit fallback ("START Caminero; if postponed, SIT him and START Hayes").

**Failure 6: A player is named without team or position on first mention.**
- Symptom: "Caminero has a good matchup today" -- but the user has never heard of Caminero.
- Detection: find every player-name first occurrence; check that it is followed by `(Team, position)`.
- Fix: add the team + spelled-out position.

**Failure 7: Abbreviation introduced without the long form.**
- Symptom: "START Caminero at 3B" in the first actions bullet, with no prior gloss.
- Detection: cross-reference the abbreviations list in [template.md](template.md#position-abbreviations) against the first occurrence in the document.
- Fix: either spell out the position earlier in the prose, or expand the abbreviation in the actions bullet on first use.

**Failure 8: The variant debate leaked into the user output.**
- Symptom: "Advocate said START; critic said SIT; synthesis leans START."
- Detection: grep for "advocate," "critic," "synthesis," "variant."
- Fix: keep only the synthesized conclusion. The variant debate belongs in the decision log, not the brief.

**Failure 9: Uncertainty hidden rather than surfaced.**
- Symptom: a `confidence: low` fact is quietly written as a confident statement.
- Detection: cross-reference the upstream draft's confidence tags against the translated output.
- Fix: surface the uncertainty in plain English with a fallback action.

**Failure 10: Emoji or cheerleader tone added.**
- Symptom: "Great start for Caminero tonight!" or a smiley appears.
- Detection: grep for non-ASCII characters and exclamation marks.
- Fix: revert to neutral tone. Bold for player names and action verbs is the only decoration allowed.
