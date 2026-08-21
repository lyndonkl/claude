# Managerial Entrenchment and Takeover Defenses

**Core idea:** When managers do not fear stockholders, they put their own interests first. The tools they use are entrenchment devices, and they sort by one crucial line: whether stockholders have to approve them. Greenmail, golden parachutes and poison pills need no stockholder vote, so management can adopt them unilaterally. Shark repellents are charter amendments and do require stockholder assent. An analyst reads the entrenchment package as a direct measure of how insulated management is from discipline, and therefore as a measure of expected agency cost.

**Formulas:** No arithmetic, but greenmail has a computable transfer:

```
Greenmail transfer to the raider
  = (Buyback price per share - Raider's average purchase price) x Shares bought back

Cost to remaining stockholders
  = the same amount, paid out of corporate cash for no operating benefit
```

**Reference data:** The five entrenchment mechanisms, ordered from no stockholder approval needed to stockholder approval needed.

| Mechanism | Stockholder approval? | What it is | Why it entrenches |
|---|---|---|---|
| **Greenmail** | Not needed | Managers of a hostile-takeover target buy out the potential acquirer's existing stake at a price far above what the raider paid, in return for a signed "standstill" agreement | Corporate cash buys off the disciplining threat; the raider profits, other stockholders pay |
| **Golden parachutes** | Not needed | Employment-contract provisions paying a lump sum, or cash flows over a period, if the covered managers lose their jobs in a takeover | Managers are paid to lose, so they can resist a value-creating deal without personal cost |
| **Poison pills** | Not needed | Securities whose rights or cash flows are triggered by an outside event, generally a hostile takeover | Makes an unwanted acquisition prohibitively dilutive, so the bid never arrives |
| **Shark repellents** | **Required** | Anti-takeover charter amendments (staggered boards, supermajority provisions, fair-price provisions) | Same aim as a pill, but stockholders must consent, so it carries a legitimacy the others lack |
| **Overpaying on takeovers** | Not needed (usually) | Acquisitions driven by management interests rather than stockholder interests | Builds an empire and raises the cost of acquiring the acquirer; see [[value-destroying-acquisitions]] |

**Procedure:** Assessing entrenchment at a real company:
1. Read the charter and bylaws. List the anti-takeover provisions in force: poison pill (and its trigger threshold), staggered/classified board, supermajority merger vote, fair-price provision, restrictions on written consent and special meetings, dual-class stock.
2. Note which were adopted *without* a stockholder vote. Those are the strongest signal of managerial self-dealing, because stockholders never consented.
3. Read the executive employment agreements for change-of-control provisions. Size each parachute as a multiple of salary plus bonus, and total the package.
4. Check the history for greenmail — any repurchase of a single large holder's block at a premium, paired with a standstill agreement.
5. Check acquisition history for premiums paid, and for the acquirer's own stock reaction on announcement.
6. Aggregate. The more provisions in force, and the more adopted without a vote, the weaker investor protection is, and the lower the value the market should assign (see the governance-index evidence in [[governance-legislation-and-payoff]]).
7. Set expectations. A heavily entrenched management is unlikely to be disciplined by a hostile bid, so the market for corporate control cannot be relied on as a counter-force here.

**Worked example:** Disney under Eisner. Entrenchment came less from charter provisions than from board capture — a hand-picked board that rubber-stamped major decisions, plus a CEO who was also chairman. The overpaying channel is visible in the 1996 ABC acquisition, which the board approved without challenge. The entrenchment held until an external threat arrived that the board could not absorb: Comcast's 2004 hostile bid, combined with 43% of shareholders withholding votes on Eisner's re-election. Eisner then lost the chairmanship to George Mitchell. Entrenchment delayed discipline for roughly eight years, and the delay cost shareholders half the stock price between 1998 and 2002.

**Determinism:**
- DETERMINISTIC: counting anti-takeover provisions in the charter; classifying each provision by whether stockholder approval was required (provision type -> approval class); computing greenmail transfer (buyback price, raider cost, share count -> transfer); computing parachute value as a salary multiple.
- JUDGMENT: whether a given provision is entrenchment or legitimate bargaining leverage for shareholders; how much value the package destroys; whether a takeover premium reflects synergy or empire building.

**Pitfalls:**
- Treating all five mechanisms as equivalent. The approval line matters. A shark repellent that stockholders voted for carries consent; a poison pill adopted by the board alone does not.
- Assuming a poison pill always hurts shareholders. It can raise the price in a negotiated deal. The source's concern is its use to block discipline entirely.
- Missing the quiet channel. Overpaying on takeovers is the "quickest and most decisive way to impoverish stockholders," and it needs no charter provision at all.
- Reading a golden parachute as pure alignment. It removes the personal cost of losing a control contest, which is exactly the cost that would otherwise deter resistance.

**Sources:**
- corporate_finance--lecture_slides--cfpacket1spr20 p.21

**Related:** [[manager-stockholder-agency-conflict]], [[board-independence-assessment]], [[value-destroying-acquisitions]], [[self-correction-and-counter-forces]], [[governance-legislation-and-payoff]], [[ownership-and-control-structure-analysis]]
