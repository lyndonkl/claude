# The seven-sin audit

Acquisitions fail so consistently that the failure must be structural. Target shareholders
capture nearly all of the announcement gain. Bidders capture roughly nothing and drift
negative. Half of acquisition programmes fail at least one of their own value tests, and a
quarter fail both. Around half of deals are divested within a decade.

Set that as the prior before you read a single number. The burden of proof belongs on the
deal, not on the skeptic.

The scorecard below is a pre-commitment device. Run it before the deal is signed, mark each
row passed or failed, and record the rationalization you were given for each failure.

## The scorecard

| Test | Passed / Failed | Rationalization offered |
|---|---|---|
| Risk transference | | |
| Debt subsidies | | |
| Control premium | | |
| The value of synergy | | |
| Comparables and exit multiples | | |
| Bias | | |
| A successful acquisition strategy | | |

The sins compound. A rule-of-thumb premium, plus a transaction-multiple price, plus a
verdict-first process is the standard failing deal. A single pass is not exculpatory. And
"we used a discounted cash flow model" is not a pass on sins 1, 2 and 5. A model built on
the acquirer's rate with an exit-multiple terminal value commits three sins inside the
wrapper.

## Sin by sin

### 1 · Risk transference

The target is discounted at the acquirer's cost of equity. A risky business does not become
safe because a safe buyer owns it.

**Test.** Read the rate applied to the target's cash flows. Rebuild the target's own rate
with `cost-of-capital-toolkit`: an unlevered beta from the target's businesses, relevered
at the target's own debt-to-equity ratio, with an equity risk premium reflecting the
target's revenue geography.

**Quantify it.** Value the target at both rates. The difference is the wealth handed to the
seller for the buyer's risk profile. In the stylized case, after-tax operating income of 12
at the target's 20% cost of equity is worth 60; at an acquirer's 10% it appears to be worth
120. The correct answer stays 60.

### 2 · Debt subsidies

The acquirer's cheap, plentiful borrowing is built into the target's cost of capital. A
target's debt capacity is a property of the target.

**Test.** Read the debt ratio and pre-tax cost of debt inside the target's weighted average
cost of capital. Both must be the target's own, estimated stand-alone.

**The legitimate version.** Genuine added debt capacity in the *combined* firm is a
financial synergy. Value it separately in the synergy step. Doing both — a financial synergy
line and a lower blended rate on the target — is a double count.

### 3 · Auto-pilot control premium

A fixed percentage is bolted onto the value. There is no defensible lookup table for this,
which is the whole point.

**Test.** Control is worth what you can change and nothing more.
`value of control = restructured value − status quo value`. Ask which specific changes were
named: raise the operating margin, raise the return on capital, move to the optimal debt
ratio, return idle cash. If nobody can name one, the premium is zero.

Two corollaries. A perfectly run target carries a control premium of zero, whatever the
survey says. And the maximum premium is not the premium to pay — paying the full control
value hands your entire improvement plan to the seller.

Check for stacking. Brand premiums and management-quality premiums on top of a model that
already contains the brand and the management are double counts. Check for delay: if the
changes take three years, the gain is discounted for those three years.

### 4 · Elusive synergy

A word with no number attached.

**Test.** Every claimed benefit maps to exactly one valuation input: a higher margin, a
higher return on capital, a higher reinvestment rate, a longer growth period, a lower tax
rate, or a higher debt ratio. A claim that maps to nothing is a buzz word. Diversification
is not a synergy for a public firm.

**Rebuild it.** Two subcommands of `project-investment-analysis` do the work.

| Subcommand | Input | Output |
|---|---|---|
| `synergy` | combined-firm values, or a synergy cash flow schedule | synergy value and the maximum price it supports |
| `synergy-haircut` | a split of cost and revenue components | what the post-merger evidence says will actually arrive |

The evidence is one-sided. Cost synergies land: a large majority of mergers hit 90% or more
of expected savings. Revenue synergies mostly do not: around 70% of mergers miss them.

Four things to check on the schedule.

- Cost and revenue synergies valued separately, never blended into one number.
- Revenue synergies haircut for integration customer attrition, typically 2% to 5%.
- One-time costs to achieve subtracted, since firms routinely underestimate them.
- Cost synergies built bottom-up, location by location, rather than as a percentage of the
  cost base.

Concreteness test: can the plan name the plant, the contract, the headcount and the month?

### 5 · It's all relative

Precedent-transaction multiples are a sample of overpayments. An exit-multiple terminal
value is a relative valuation wearing intrinsic clothing.

**Test.** Read where the price came from and where terminal value came from. If a multiple
set either, back out the growth and return on capital it implies and test them.

Earnings accretion belongs here too. An all-stock deal is accretive whenever the acquirer's
price-earnings ratio exceeds the target's. Accretion is arithmetic and carries no
information about value. Reported as a deal test, it is a finding.

### 6 · Verdict first, trial afterwards

**Test.** Reconstruct the chronology. A valuation dated after the price is a
rationalization. Ask which input was flexed to close the gap.

Two process checks follow. A walk-away price should have been set before any auction, and
the bidder should leave when it is exceeded. Losing a bidding war is better for
shareholders than winning one, by a wide margin over three years. And a fairness opinion is
a document commissioned by a party that wants the deal, paid on completion. It is not
independent evidence.

### 7 · It's not my fault

**Test.** Name the individual whose compensation depends on the promised benefits arriving.
No name means no delivery. Advisor pay tied to completion buys advice to complete. Blame
spread across the old management, the bankers, the target and the auditors is blame
assigned to nobody.

## The four numbers and the acid test

Beyond the sins, confirm the arithmetic spine of the deal exists. Only three value reasons
are admissible: undervaluation, control and synergy. Anything else is not a value reason.
All four numbers must be produced.

| # | Number | Source |
|---|---|---|
| 1 | acquisition price | negotiated, or a premium over the pre-announcement market capitalization |
| 2 | status quo value | a full model of the target as currently run |
| 3 | restructured value | the same target with changed investing, financing and payout policy |
| 4 | synergy value | combined with synergy, less the acquirer standalone plus the **restructured** target |

| Stated motive | The deal works only if |
|---|---|
| undervaluation | price below status quo value |
| control | price below restructured value |
| synergy | price below restructured value plus synergy |

Two structural checks on these numbers.

**The synergy baseline.** Number 4 measures against the restructured target, not the status
quo one. Using the status quo counts the control gains twice, and this is the most common
way the acid test gets passed dishonestly.

**The no-synergy identity.** The combined value with no synergy must equal the sum of the
two standalone values exactly. If it does not, an assumption is inconsistent somewhere in
the build.

When the price exceeds the benchmark, exactly two explanations survive. The synergy was
underestimated, or the acquirer is overpaying. The write-up has to pick one.

## Deal-design odds

These shift the base rate before any number is produced. Note them in `challenge.md` when
the deal sits on the wrong side.

Sole bidder beats a bidding war. A private target or a subsidiary beats a public target.
Cash beats stock. A small target beats a large one. Cost synergies beat growth synergies.

One interaction is worth stating: large deals are dangerous for public targets, while
private and subsidiary deals perform better as size rises.
