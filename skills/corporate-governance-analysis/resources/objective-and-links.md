# The objective function, the four links, and the counter-forces

Stock price maximization is not a default. It is a conclusion, and it holds only when four
links in a chain hold. This file works each link, then converts the findings into an
objective, an archetype and a set of counter-force scores.

## Link I — managers against stockholders

In theory stockholders control managers through the annual meeting and the board. Both
mechanisms fail in predictable ways.

The annual meeting fails because small holders do not attend, unvoted proxies count as
votes for management, large unhappy holders sell rather than fight, and meetings are
scripted so that rebels cannot raise unwelcome topics.

The board fails because the chief executive shapes who sits on it, directors hold token
stakes, and directors lack the expertise or the will to confront. Three forces keep them
quiet. The chief executive usually chairs, so he or she sets the agenda and controls what
directors see. Consensus-seeking overwhelms confrontation. And loyalty to an authority
figure is a strong human default.

Evidence to gather is in [board-and-entrenchment.md](board-and-entrenchment.md) and
[ownership-and-control.md](ownership-and-control.md). Score the link, then price it as an
expected agency cost: empire building, cash hoarding, overpriced acquisitions, and pay
untied to performance.

A Link I failure does not change the objective. It changes the constraint set.

## Link II — stockholders against lenders

Lenders hold a fixed claim and care about safety. Stockholders hold the residual claim and
care about upside. That asymmetry opens three channels for moving wealth from lenders to
owners after the debt is issued.

| Channel | Mechanism | Defense that blocks it |
|---|---|---|
| Cash payout | A dividend or buyback surge leaves the firm riskier | Dividend covenants |
| Risk shifting | Assets become riskier than the ones the rate was set on | Investment covenants, puttable bonds, ratings-sensitive notes |
| Claim dilution | New debt is issued against the same assets | Financing covenants, event-risk and change-of-control clauses |

Inventory the covenants by category. Score the lenders exposed when there are no covenants
and long maturities. Score them protected under tight covenants, short maturities, or bank
debt with maintenance tests. An investment-grade rating is not protection. RJR Nabisco was
investment grade before its leveraged buyout, and its 2016 bond fell from about 87 to about
70 on the announcement, a 19.5 percent loss with no change in the operating business.

A Link II failure moves the objective from stockholder wealth to firm value.

## Link III — firms against markets

Two things have to hold. Managers must disclose honestly and promptly. The market must
price the disclosure well.

Check disclosure quality: restatements, late filings, auditor changes, enforcement actions,
material weaknesses. Check the timing of bad news against its base rate. Announced earnings
changes average roughly minus 4.8 percent on Fridays against plus 1.2 to plus 3.5 percent
on other weekdays, which is the classic tell for managed timing. Check the widening gap
between reported and adjusted earnings. Then check market quality for this stock: volume,
bid-ask spread, free float, analyst coverage, options depth.

Take the efficiency critiques seriously without accepting them wholesale. Markets pay high
prices for young firms with no near-term earnings, appear to overvalue future growth
relative to current earnings, and respond positively to announcements of research spending
and capital investment. None of that is the behavior of a market that sees only the next
quarter.

The practical question is not whether the market is perfect. It is whether this stock's
price is a usable proxy for value. A Link III failure moves the objective from stock price
to stockholder wealth.

## Link IV — firms against society

A social cost accrues to society rather than to the decision maker. These resist
quantification for three structural reasons. They can be unknown at the time of the
decision, as asbestos was for decades. They are weighed differently by different people.
And carried to extremes, weighing every one of them paralyzes decision making.

So split them. Costs already priced or regulated go into the model directly: permit prices,
carbon costs, tort liability, fines, remediation obligations. For everything else, do not
invent a social-cost number. Model the societal response, which is quantifiable because it
lands on cash flows and on the cost of capital.

- Governments pass laws against firms that flout norms. Model a probability-weighted future
  cost.
- Firms serving a socially conscious clientele lose business when they fall short, even
  when the behavior is legal. Model revenue risk.
- Some investors refuse to hold the stock. Model a narrower investor base and a higher cost
  of equity.

Disclose the assumptions, because another analyst weighing these differently should be able
to see and change your inputs. A Link IV failure does not change the objective. It changes
the constraint set.

## Setting the objective

Three booleans. T is publicly traded and liquid. E is markets reasonably efficient for this
stock. B is lenders protected. A listing alone does not settle T; a stock with negligible
float and volume behaves like a private company.

| T | E | B | Objective |
|---|---|---|---|
| yes | yes | yes | Maximize stock price, which also maximizes firm value |
| yes | no | yes | Maximize stockholder wealth |
| yes | no | no | Maximize firm value |
| no | — | yes | Maximize stockholder wealth |
| no | — | no | Maximize firm value |

Firm value is the fallback on both failure paths. When in doubt, the broader objective is
the safer one. Re-date the call, because liquidity, coverage and covenant protection all
change.

## The archetypes

Naming the archetype names the governance risk and the expected agency cost in one word.

| Archetype | Who controls | What it maximizes | Analytical consequence |
|---|---|---|---|
| Cutthroat | Founder or family with a controlling stake and a compliant board | Founder wealth | Expect wealth transfer away from minority holders; expect backlash risk |
| Utopian | Shareholders with equal voting rights | Stock price | The benchmark case, not a description of any real firm |
| Managerial | Managers, over a dispersed and powerless register | Managerial interests | Expect empire building and excess cash |
| Crony | Founder, family or official, with rule writers co-opted | Founder and official wealth | Expect politically shaped pricing and investment |
| Confused | Shared between shareholders and other stakeholders | Stakeholder wealth | Expect efficiency drag and no accountability |
| Constrained | Shareholders, with a board that checks the chief executive | Shareholder wealth subject to constraints | Take reported governance close to face value |

Constrained corporatism is the endorsed equilibrium. Two distinctions matter. Cutthroat is
presented as a strawman caricature of shareholder wealth maximization, not as what the
objective means. And the constrained model differs from the confused one because the
constraints are imposed and paid for rather than assumed away.

Legal form does not settle the archetype. A firm listed on a major exchange can sit in
crony corporatism through a dual-class or shell structure.

## Two repairs that do not work, and one that does

**Hand monitoring to someone else.** German bank-centered governance and Japanese keiretsu
cross-holdings replace dispersed shareholders with corporate families. At their best, the
efficient firms in the group pull the weaker ones up and the structure is more stable. At
their worst, the weakest firms drag the best ones down. Either way the outside investor
cannot easily tell which is happening, and that opacity is the analyst's problem. Map the
group, compute look-through interests, read the related-party notes, and ask directly
whether the group supports the listed entity or extracts from it.

**Swap the metric or the constituency.** Earnings, revenues, size, market share and
economic value added are intermediate objectives. Each works only where it correlates with
long-term value. Read the compensation plan to find the metric the firm actually maximizes,
then ask what a manager would do to maximize that number alone. Market share bought below
cost, revenue growth bought by loosening credit, earnings growth bought by underinvesting:
these are the decoupling cases. A stakeholder objective has the same defect in a different
place. When there is no rule for resolving conflicts between stakeholders, there is no
accountability, and a manager answerable to everyone is answerable to no one.

**Keep the objective and repair the linkages.** This is the workable answer. Make managers
and employees into stockholders, protect lenders from expropriation, disclose honestly and
promptly, and minimize social costs.

## The four counter-forces

Each failure has a counter-force. Where the failure is live and the counter-force is
absent, the excess persists and should be priced. Score each present, weak or absent.

| Failure | Counter-force | What to check |
|---|---|---|
| I. Managers vs stockholders | Activists and the market for corporate control | 13D filings, dissent votes, whether the firm is takeable, whether defenses block a bid |
| II. Stockholders vs lenders | Covenants and new bond types | Covenant load, puttable bonds, ratings-sensitive notes |
| III. Firms vs markets | Analyst and options-market scrutiny | Coverage, options depth, short interest, information access |
| IV. Firms vs society | Regulation plus customer and investor backlash | Regulatory pipeline, customer base, exclusion by mandate |

**The hostile-takeover target screen.** The typical target has three traits: return on
equity roughly 5 percentage points below the peer group, significant relative
underperformance over the previous two years, and managers holding little or no stock. All
three hitting with no entrenchment blocker points to discipline within 12 to 24 months. A
poison pill plus a staggered board neutralizes the screen entirely.

Self-correction is neither automatic nor fast. Disney's entrenchment held for eight years,
and it broke only when three signals arrived together.

## Does governance pay, and can it be legislated?

It pays, and it cannot be legislated. The most cited evidence scores 24 provisions across
1,500 firms. A portfolio long the strongest protections and short the weakest earned about
8.5 percent a year in excess return. Each point toward fewer protections was associated with
about 8.9 percent lower market value in the 1999 cross-section. High-protection firms also
showed higher profits, higher sales growth and fewer acquisitions.

Use those numbers as a magnitude prior and a corroboration check, never as a firm-specific
discount. They come from a single cross-section, the direction of causation is not
established, and the finding attaches to investor-protection provisions rather than to
board composition.

Legislation is a blunt instrument. Compliance costs often exceed the benefits, unintended
consequences follow, and the burden falls harder on good companies than on bad ones.
Discount any governance improvement a firm made only because a law required it.
