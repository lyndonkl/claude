# Value-Destroying Acquisitions as an Agency Cost

**Core idea:** Overpaying on a takeover is the quickest and most decisive way to impoverish stockholders. Acquiring-firm stockholders do not share their managers' enthusiasm: bidder stock prices fall on announcement a significant share of the time. The post-deal evidence is no kinder. Merged firms' profitability relative to their peer group does not rise much, and many mergers are reversed within a few years — an open admission that the deal did not work. An analyst treats a pattern of premium-paying acquisitions as a governance red flag, and uses the acquirer's own announcement return as the market's verdict on the claimed synergies.

**Formulas:**

```
Acquisition premium ($)  = Bid value - Target market value 30 days prior
Acquisition premium (%)  = Premium / Target market value 30 days prior

Market's synergy verdict = Change in ACQUIRER's market value on announcement

Interpretation:
  Acquirer value change ≈ -Premium   -> market expects ZERO synergy;
                                        the entire premium is a transfer
                                        from acquirer to target holders
  Acquirer value change > -Premium   -> market credits partial synergy
  Acquirer value change > 0          -> market credits synergy exceeding
                                        the premium
```

Where: *Bid value* = price per share x target shares outstanding; *Target market value 30 days prior* = pre-rumor market capitalization, taken far enough back to precede leakage; *Change in acquirer's market value* = cumulative abnormal return (CAR) around the announcement x acquirer market capitalization.

Reversal test:
```
Recovery ratio = Total proceeds from later divestitures / Original price paid
Recovery ratio < 1  ->  value destroyed and admitted
```

**Procedure:** Judging an acquisition:
1. Fix the target's market value 30 days before the first bid or rumor. Use 30 days to strip out leakage.
2. Compute the bid value and the premium in dollars and percent.
3. Measure the acquirer's own abnormal return around the announcement day, and multiply by the acquirer's market cap to get the dollar change in acquirer value.
4. Compare that dollar change to the premium. If the acquirer loses roughly the whole premium, the market is telling you it expects no synergy.
5. Read management's stated synergy case. Write down the specific operating numbers it implies — revenue growth, margin, cost savings.
6. Track those numbers for 3-5 years after closing. Compare actual revenues and operating earnings to the synergy case and to the peer group.
7. Check for reversal. Was the business divested? Sum the proceeds and compute the recovery ratio.
8. Fold the verdict into your governance assessment. A serial overpayer with a captive board justifies a higher expected agency cost.

**Reference data:** *Sterling Drug under Eastman Kodak — "Where is the synergy?" (approximate, $ millions, read from the chart):*

| Year | Revenue | Operating earnings |
|---|---|---|
| 1988 | ~3,800 | ~550 |
| 1989 | ~4,000 | ~450 |
| 1990 | ~4,350 | ~550 |
| 1991 | ~4,900 | ~400 |
| 1992 | ~5,000 | ~500 |

Revenues grew modestly. Operating earnings stayed flat or fell. The claimed synergies never appeared in the operating results.

*Empirical regularities the source cites:* bidder stock prices decline on takeover announcements a significant proportion of the time; merged firms' profitability relative to peers does not rise much after mergers; many mergers are reversed within a few years.

**Worked example: Eastman Kodak / Sterling Drugs (1987-1994).**

- Late 1987: Kodak enters a bidding war with Hoffman La Roche for Sterling Drugs, a pharmaceutical company.
- Sterling traded at about **$40/share** when the bidding started.
- At **$72/share** Hoffman La Roche dropped out. Kodak kept bidding.
- Kodak won at **$89.50/share**, and claimed potential synergies justified the premium.
- Kodak's bid = **$5.1 billion**. Sterling's market value 30 days prior = **$3.0 billion**.
- Premium = 5.1 - 3.0 = **$2.1 billion**.
- Decrease in Kodak's own market value around the 1/22 bid announcement = **$2.2 billion** (source: The Alcar Group).
- Verdict: the market wiped roughly the entire premium off Kodak's own value. Investors expected no synergies at all.
- 1988-1992: Sterling's revenues grew from ~$3.8bn to ~$5.0bn while operating earnings went nowhere. No synergy appeared.
- August 1993: a New York Times story suggests Kodak is eager to shed the drug unit. Kodak officials say they have no plans to sell Sterling Winthrop. Chairman Louis Mattis calls the rumors "massive speculation."
- A few months later, Kodak sells Sterling Winthrop's prescription drug business to the Sanofi Group for **$1.68 billion**. Kodak shares rise 75 cents to $47.50 on the news. Analyst Samuel D. Isaly calls the deal "very good for Sanofi and very good for Kodak." CEO George M. C. Fisher says Kodak will be entirely focused on imaging after the divestitures.
- The rest of Sterling Winthrop is sold to SmithKline for **$2.9 billion**.
- Total recovery = 1.68 + 2.9 = **$4.58 billion** against **$5.1 billion** paid. Recovery ratio = 4.58 / 5.1 = **0.90**. Value destroyed, and the acquisition reversed.
- Note the market's reaction on the divestiture announcement: the stock *rose*. Investors were glad to see the deal undone.

**Determinism:**
- DETERMINISTIC: premium in dollars and percent (bid value, prior market value -> premium); acquirer value change (CAR, market cap -> dollars); the comparison of the two; recovery ratio (divestiture proceeds, original price -> ratio); Sterling revenue/earnings table lookup.
- JUDGMENT: choosing the "30 days prior" window and whether leakage began earlier; separating the announcement effect from contemporaneous news; deciding whether a poor post-deal record reflects the deal or the industry; deciding whether a divestiture is an admission of failure or a strategic refocus.

**Pitfalls:**
- Measuring the premium against the price *after* the bidding war started. Sterling was at $40 before the war and $89.50 at the close. Using the $72 intermediate price would understate the premium badly.
- Accepting the synergy story at face value. Kodak claimed synergies and the market priced none.
- Ignoring the acquirer's own stock reaction. It is the cleanest single read on whether the deal creates value.
- Judging a merger only on combined revenue growth. Sterling's revenues grew every year while operating earnings stagnated.
- Believing management's denials of a pending divestiture. Kodak denied it in August 1993 and sold within months.

**Sources:**
- corporate_finance--lecture_slides--cfpacket1spr20 p.22-25

**Related:** [[managerial-entrenchment-and-takeover-defenses]], [[manager-stockholder-agency-conflict]], [[board-independence-assessment]], [[self-correction-and-counter-forces]], [[disney-governance-case-study]], [[synergy-valuation]], [[acquisition-valuation]]
