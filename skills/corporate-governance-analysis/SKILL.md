---
name: corporate-governance-analysis
description: Assesses who actually controls a company and whether management is accountable — board independence, dual-class and voting structures, cross-holdings and pyramids, the marginal investor, and the gap between stated and real accountability. Use in a corporate finance analysis, when setting the objective function for a valuation, when assessing the odds that bad management gets replaced, or when valuing control.
---

# Corporate governance analysis

Two questions sit under this work. What number is this firm actually trying to maximize?
And if the firm is run badly, what are the odds that changes? The first answer fixes the
objective the whole analysis serves. The second one is worth money, and it can be priced.

Governance is read first, not scored last. It decides which objective is legitimate, and
it decides how much of any later recommendation management will act on. A board with
staggered terms, a poison pill and no majority-vote standard can ignore an optimal debt
ratio for years. That is a fact about the analysis, not a footnote to it.

## Two rules that hold throughout

**Weak governance is never an arbitrary discount to value.** It enters the model in four
named places: a low return on capital, a reinvestment policy that keeps funding sub-hurdle
projects, a financing and payout policy that never moves, and a low probability of change.
A haircut applied to the final number hides every one of those and cannot be argued with.
Detail in [value-of-control.md](resources/value-of-control.md).

**Structure is evidence, not the verdict.** A board can pass every formal independence
test and still rubber-stamp. In the cross-sectional evidence, investor-protection
provisions predict value and board composition barely does. So count the provisions, then
look for a decision the board actually stopped or slowed.

## What this analysis produces

The record is the `governance` block: objective, four_link_scores, archetype, control_map
(economic, voting, wedge, group), board_table_vs_peers, calpers_pass, entrenchment_inventory,
covenant_inventory, counter_force_scores, power_score, agency_cost_prior, constraint_set.
Alongside it sits the `stockholders` block: institutional_pct_shares, institutional_pct_float,
insider_pct, holder_classification, marginal_investor, risk_measure.

Where those two records land:

| Consumer | What it takes |
|---|---|
| `classification.json` | `ownership`, plus any `constraints` this analysis triggers. Gate `G2_classified` |
| `cost-of-capital.json` | the marginal investor sets the risk measure, which sets the beta route |
| `capital-structure.json` | insider and institutional percentages drive the discipline lens |
| `payout.json` | the trust context behind the cash-holding argument |
| `dcf-result.json` | the probability of change and the restructured case, in `restructuring` mode |
| `REPORT.md` | Parts I and II of the corporate finance assessment, and the Power score row |

One constraint is raised here rather than anywhere else. When the marginal investor is
undiversified, the analysis carries `require-total-beta` forward into the cost of capital.

## The objective function and its four links

Stock price maximization is legitimate only when four links hold. Each link has a
characteristic failure, and the failures are not independent — a captive board makes
information games easier, and both make lender expropriation easier.

| Link | What must hold | The failure | Where to look |
|---|---|---|---|
| I. Managers vs stockholders | The board and the annual meeting discipline managers | Managers put themselves first | Board, ownership, entrenchment |
| II. Stockholders vs lenders | Lenders are protected by covenant or reputation | Lenders are expropriated | Covenants, payout surges, risk shifts |
| III. Firms vs markets | Managers disclose honestly and promptly; the market prices it | News is delayed or spun; the stock is thin | Restatements, bad-news timing, float |
| IV. Firms vs society | Every cost the firm creates is charged to the firm | Untraced externalities | Regulation pipeline, backlash risk |

Score each link, then apply the matrix. Three booleans: T = publicly traded and liquid,
E = markets reasonably efficient for this stock, B = lenders protected.

| T | E | B | Objective |
|---|---|---|---|
| yes | yes | yes | Maximize stock price |
| yes | no | yes | Maximize stockholder wealth |
| yes | no | no | Maximize firm value |
| no | — | yes | Maximize stockholder wealth |
| no | — | no | Maximize firm value |

Link I and Link IV failures do not appear in the matrix. They do not change the objective.
They change the constraint set and the agency-cost prior you carry into the forecast.
That distinction is worth defending, because it is the most common place this analysis
gets short-circuited into a general complaint about management.

State the objective in one sentence before any valuation runs. The four-link detail, the
archetype vocabulary and the counter-force scoring are in
[objective-and-links.md](resources/objective-and-links.md).

## The assessment procedure

Run these in order. The ownership answer changes how you read the board, and the board
answer changes how you read everything else.

**1. Read the ownership table.** Compute the economic stake, the voting stake and the
control wedge for every material holder. Sum affiliated entities for group control, and
trace pyramids down to a look-through economic interest. Record dual-class ratios, golden
shares, board nomination rights, and whether the listed entity owns the operating assets
or only a contractual interest in them. Write one sentence naming who controls the firm.

**2. Identify the marginal investor.** This is the holder most likely to trade next, not
the largest holder. It decides whether market beta is legitimate. An index fund at 4% is
not a monitor; an activist at 4% is. A controlling partnership is an undiversified holder
even when it is nominally institutional. Both steps are worked in
[ownership-and-control.md](resources/ownership-and-control.md).

**3. Grade the board.** Run the three CalPERS tests: a majority of outside directors, a
chair who is not the CEO, and audit and compensation committees composed entirely of
outsiders. Then go past the labels. Look for consulting and legal fees, charitable ties,
board interlocks, and director stakes worth less than the director's own fee. Compare
board size to the 9 to 11 benchmark. These tests are necessary and nowhere near sufficient.

**4. Check the CEO tenure clock.** Long tenure plus early success is the risk condition.
Watch for a chair and CEO role that was separated and then recombined, for heirs apparent
who leave, and for term extensions justified as essential to a pending deal. Governance is
a cycle, not a state, and tenure is the clock. Steps 3 and 4 are worked in
[board-and-entrenchment.md](resources/board-and-entrenchment.md).

**5. Inventory the entrenchment devices.** Sort them by whether stockholders had to
approve. Greenmail, golden parachutes and poison pills need no vote, so they are the
stronger signal of self-dealing. Shark repellents are charter amendments and carry
consent. Size the parachutes as a multiple of salary plus bonus, and compute any greenmail
transfer explicitly.

**6. Read the acquisition record.** Overpaying is the quickest way to impoverish
stockholders and needs no charter provision at all. For each material deal, compute the
premium against the target's value 30 days before the first bid or rumor. Then compute the
acquirer's own announcement return in dollars. When the acquirer loses roughly the whole
premium, the market has told you it expects no synergy. Check later divestitures for a
recovery ratio below one.

**7. Check lender protection.** Inventory covenants by category: investment, financing,
payout. Look for puttable bonds and ratings-sensitive notes. Then screen for live
expropriation. The three channels are a payout surge unmatched by operating cash flow, a
shift into a materially riskier business, and new debt issued against the same assets. An
investment-grade rating is not protection.

**8. Test information and market quality.** Restatements, late filings, auditor changes
and material weaknesses. The timing of bad news against its base rate. The gap between
reported and adjusted earnings. Then float, volume, bid-ask spread, analyst coverage and
options depth. This step answers the E boolean.

**9. List the social costs.** Split them in two. Costs already priced or regulated go
straight into the cash flows as operating costs, capital spending or contingent
liabilities. For the rest, do not invent a social-cost number. Model the societal response
instead, as regulation risk, revenue risk, or a narrower investor base.

**10. Score the counter-forces and name the archetype.** For each of the four failures, ask
whether its counter-force is present, weak or absent. Then run the hostile-takeover target
screen: return on equity roughly 5 points below the peer group, two-year relative
underperformance, and managers holding little or no stock. All three hit with no
entrenchment blocker in the way, and discipline usually arrives within 12 to 24 months. If
a pill and a staggered board block it, the underperformance can persist indefinitely.

## Reading the numbers

A few thresholds carry real weight, and a few widely cited numbers do not.

- Withhold votes above 20 to 30 percent are a serious revolt signal. Change normally needs
  two or three signals arriving together, such as protest resignations, a hostile bid and
  a mass withhold vote.
- Institutional ownership is not monitoring. Mainstream fund families historically support
  management around 92 percent of the time.
- The governance-index evidence is a magnitude prior only. The strongest-protection minus
  weakest-protection portfolio earned about 8.5 percent a year, and each point toward fewer
  protections was associated with about 8.9 percent lower market value in the 1999
  cross-section. Do not turn that into a firm-specific discount.
- The 20 percent control premium quoted from transaction surveys has no valuation content.
  Control is worth what you can change and nothing more.
- Cross-holding and group structures earn a confidence discount on the reported financials.
  Ask explicitly whether the group supports the listed entity or extracts from it.

## Connecting governance to value

Governance changes the valuation in exactly two ways.

**It changes the status quo case.** A captive board that funds sub-hurdle projects shows
up as a return on capital below the cost of capital, and therefore as growth that destroys
value. The right modelling response is a lower return on capital and less reinvestment, not
a bigger discount rate. Around 52 percent of non-financial firms globally earn less than
their cost of capital, so assume this firm is in the majority until the numbers say
otherwise.

**It changes the odds that the status quo ends.** That is the probability term below.

Both run through the same machine. Value the firm as it is run today. Then value it under
the policy changes you can name, using the four levers: cash flows from existing assets,
expected growth, the length of the growth period, and the cost of capital. Build both
cases with `dcf-valuation-engine` and take the optimal debt ratio from
`cost-of-capital-toolkit`'s `debt-schedule` subcommand.

    Value of control = restructured equity value − status quo equity value

    Expected value of control = P(management change) × value of control

    Delay-adjusted control value = (optimal − status quo) / (1 + r)^k

    Market-implied P = (price/share − status quo/share) / (optimal/share − status quo/share)

The last line inverts the market price into the odds the market is already paying for.
Compare that number to your own estimate from step 10. When P comes out at or below zero,
the market prices no chance of change. When it comes out above one, your optimal value is
probably too low — investigate before trading on it.

Four things move the probability of change: takeover restrictions, voting rules,
whether a challenger can raise the money, and firm size. Larger, better defended and more
closely held means lower. Forced turnover is more likely when the firm underperforms
peers, the board is small and outsider-dominated, insider holdings are low, and the firm
depends on equity markets for new capital.

A well-run firm has a zero value gap, so its expected value of control is zero whatever
the probability. Control value and synergy value do not overlap, and neither is added on
top of a valuation that already reflects them. Full mechanics, including voting premiums
and minority discounts, in [value-of-control.md](resources/value-of-control.md).

## What is computed and what is judged

| Computed | Judged |
|---|---|
| Economic and voting stakes, control wedge, group and look-through totals | Whether a holder is active or passive, and who is marginal |
| CalPERS tests, insider counts, board size, director stake against fee | Independence beyond the formal label |
| Withhold percentages, greenmail transfer, parachute multiples | Whether the board actually constrains the CEO |
| Acquisition premium, acquirer announcement loss, recovery ratio | Whether a divestiture admits failure or refocuses the firm |
| Governance-provision counts, takeover screen, liquidity statistics | The three booleans, counter-force strength, the archetype |
| Both valuations, the value gap, implied probability, voting premium | The probability itself, which gaps close, and how fast |

The Power score that ends the assessment is a judgment compressed to one integer. Say what
drove it.

## Common failures

| Symptom | Cause |
|---|---|
| Every company gets "maximize shareholder value" | The (T, E, B) matrix was never run |
| A large institutional base is read as good governance | Institutions vote with management about 92 percent of the time |
| A governance discount appears in the discount rate | Weak governance belongs in returns and in the probability of change |
| Control premium quoted as a percentage | No restructured valuation was built, so the premium has no content |
| Implied probability of change above 100 percent | The optimal value is too low, or the market prices something outside the model |
| Group company's reported numbers taken at face value | Cross-holdings were not traced, and support versus extraction was never asked |
| Governance verdict from three years ago still in use | Boards drift as a successful CEO's tenure lengthens |
| Board passes every test and the analysis stops there | Composition is a weak predictor; provisions and behavior are the signal |
