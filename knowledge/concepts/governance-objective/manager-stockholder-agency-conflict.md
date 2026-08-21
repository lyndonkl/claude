# The Manager-Stockholder Agency Conflict

**Core idea:** In theory stockholders control managers through two mechanisms: the annual meeting and the board of directors. In practice neither disciplines managers well. Small holders skip the meeting, unvoted proxies default to management, and large unhappy holders sell rather than fight. Boards are hand-picked by CEOs, own little stock, and lack the expertise or the will to ask hard questions. The gap between theory and practice is the first and largest crack in stock-price maximization. An analyst prices that gap as agency cost: expect empire building, excess cash hoarding, overpriced acquisitions, and pay untied to performance.

**Formulas:** No arithmetic. The two disciplining mechanisms and their failure modes:

```
Mechanism 1: The annual meeting
  Theory   -> unhappy stockholders voice disapproval and vote managers out
  Failure  -> (a) small holders don't attend: travel cost > value of holding
              (b) unvoted proxies count as votes FOR incumbent management
              (c) large unhappy holders "vote with their feet" (sell)
              (d) meetings are tightly scripted and controlled, so rebels
                  cannot raise issues management dislikes

Mechanism 2: The board of directors
  Theory   -> the board represents stockholders and checks management
  Failure  -> (a) the CEO picks the directors
              (b) directors hold token equity stakes
              (c) directors lack expertise and willingness to confront
```

**Procedure:** Measuring the conflict at a real company:
1. Pull the proxy statement (DEF 14A) and the last three annual meeting results.
2. Compute the meeting's real discipline. Look at turnout, at the proportion of shares voted, and at the "withhold"/against percentage on directors and on say-on-pay. A large withhold vote is the visible signal of stockholder anger (Disney 2004: 43% withheld from Eisner).
3. Check who nominated the directors. A nominating committee of independent directors is the reform; CEO recommendation is the failure mode.
4. Check director equity. Compare each director's shareholding value against the director's annual fee. If the fee exceeds the value of the stake, the director's economic interest is aligned with the CEO who sets the fee, not with the shareholders.
5. Check how the stake was acquired. Shares *granted* by the firm are weaker alignment than shares *bought* by the director.
6. Count directors who are sitting CEOs of other firms. Check for interlocks — CEOs sitting on each other's boards.
7. Check whether the CEO is also the chair. If so, the CEO sets the agenda, chairs the meeting, and controls what information directors see.
8. Check institutional holders' voting records. Mainstream mutual fund families historically vote with management about 90-94% of the time.
9. Score the conflict high, medium, or low, and carry it into the valuation as an expected agency cost.

**Reference data:**

*Institutional investor support for resolutions (mainstream mutual fund families):*

| Year | % support for management resolutions | % support for shareholder resolutions |
|---|---|---|
| 2004 | 90.9 | 25.4 |
| 2005 | 92.0 | 25.6 |
| 2006 | 93.5 | 32.0 |
| 2007 | 92.4 | 30.4 |
| 2008 | 91.8 | 31.1 |

Institutions almost always back management and rarely back shareholder proposals. Do not assume a large institutional holder is an active monitor.

*Director selection (Korn/Ferry survey, 1992):*

| Source of new directors | % of companies |
|---|---|
| CEO recommendation | 74% |
| Outside search firm | 16% |

The numbers have improved since (see the board-trend table in [[board-independence-assessment]]), but CEOs still shape who sits on their boards.

*Why directors do not confront the CEO — three mechanisms:*
1. **Robert's Rules of Order.** In most boards the CEO is also the chair. The CEO sets the agenda, chairs the meeting, and controls the information directors receive.
2. **"Be a team player."** The search for consensus overwhelms any attempt at confrontation.
3. **The CEO as authority figure.** Social psychology finds loyalty is hardwired into human behavior. Loyalty builds organizations. It also leads people to suppress their own ethical standards when those standards clash with loyalty to an authority figure. In a board meeting, the CEO is that figure.

**Worked example:** Disney, 1997. The CEO (Eisner) was also chairman. The board included the president (Ovitz), a senior EVP (Litvack), a division chairman (Nunis), a former Disney CEO (Walker), the CEO's children's school principal (Bowers), the president of a university that received Disney support (O'Donovan), the CEO's personal attorney (Russell), and Disney's architect (Stern). Directors held token stakes. Result: the board rubber-stamped the 1996 ABC acquisition, and the stock halved between 1998 and 2002 before shareholders finally revolted in 2004. See [[disney-governance-case-study]].

**Determinism:**
- DETERMINISTIC: counting inside directors; CEO/chair duality (yes/no); director stake value vs. director fee (share count, price, fee -> ratio); withhold-vote percentage; proportion of shares voted; institutional support percentages (table lookup).
- JUDGMENT: whether a nominally "outside" director is truly independent (business, personal, and charitable ties are not disclosed in a computable form); whether the board actually asks hard questions; sizing the agency cost in dollars.

**Pitfalls:**
- Counting an unvoted proxy as neutral. It is a vote *for* incumbent management.
- Treating institutional ownership as monitoring. The 2004-2008 data shows institutions vote with management ~92% of the time.
- Treating "outside director" as "independent director." Disney's 1997 outsiders had dense personal and business ties to Eisner.
- Reading a director's shareholding without comparing it to the director's fee. Most directors earn more as directors than they gain from their stock.
- Assuming exit (selling) disciplines management. Exit by a large holder relieves pressure on management rather than applying it.

**Sources:**
- corporate_finance--lecture_slides--cfpacket1spr20 p.12-16
- corporate_finance--lecture_slides--cfpacket1spr20 p.17

**Related:** [[classical-objective-function-assumptions]], [[board-independence-assessment]], [[managerial-entrenchment-and-takeover-defenses]], [[value-destroying-acquisitions]], [[ownership-and-control-structure-analysis]], [[self-correction-and-counter-forces]], [[disney-governance-case-study]]
