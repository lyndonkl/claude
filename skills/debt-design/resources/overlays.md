# The overlays: tax, agencies, bondholders, information, mispricing

Matching sets the target design. These five overlays adjust it, and one of them can stop an
issue entirely. Work through them in order and record every one that binds.

## 1. Tax deductibility

The main benefit of debt is that interest is deducted before taxable income. A matched
instrument that fails to deliver that deduction has thrown the benefit away.

Check three things.

**Does the instrument qualify?** Deductibility depends on the local code and on the
instrument's legal form, not on whether it behaves like debt economically. Hybrids are
where this bites. Confirm before recommending, and name the jurisdiction.

**Is there income to shelter?** Interest above EBIT shelters nothing further.

    t_EBIT = t                         if interest ≤ EBIT
    t_EBIT = t × EBIT ÷ interest       otherwise

**Does a statutory cap bind?** Post-2017 US rules limit net interest deductions to 30% of
a measure of earnings.

    t_cap = t                              if interest ≤ 0.30 × M
    t_cap = t × (0.30 × M) ÷ interest      otherwise

`M` is EBITDA through 2022 and EBIT after. The rate that reaches the cost of debt is
`t_used = MIN(t_EBIT, t_cap)`. The optimal-ratio schedule in `cost-of-capital-toolkit`
already applies this, and it relevers beta with the same reduced rate.

Jurisdiction differences are exploitable. Marginal corporate rates vary widely — a 2021
sample gives the US 27% including state taxes, the UK 19%, Germany 30%, France 26.5%,
Japan 30.62%, China 25%, India 30%, Brazil 34%, Ireland 12.5%. Borrowing in the entity that
faces the higher rate is worth more, provided that entity has the income to shelter and the
debt genuinely sits there.

A large enough tax advantage can override matching. Zero-coupon debt is the standard
example: it defers cash interest while still generating deductions. When tax drives the
choice, say so and size the benefit, rather than letting the instrument appear for
unexplained reasons.

## 2. Ratings agencies, analysts and regulators

| Audience | Watches | Bias |
|---|---|---|
| Analysts | Earnings per share, multiples against comparables | Dislike issues that dilute |
| Ratings agencies | Coverage and leverage ratios | Prefer equity |
| Regulators | Book-value measures set by statute | Prefer whatever the rule specifies |

An instrument that satisfies all three at once is rare and short-lived. Trust preferred
stock was the classic case: a fixed payment set at issue, deductible like interest, with
failure to pay handing holders voting rights. Agencies first counted it as equity, which
meant a tax deduction plus equity credit. They now grant only partial equity credit.

The lesson is not that the trick is dead. It is that the beneficiary is specific. Quasi-
equity helps an **under-levered firm with a rating constraint that moving to its optimum
would breach**. That firm captures debt-like tax benefits while keeping its rating. For any
other firm the instrument is expensive complexity.

Agencies also apply qualitative criteria and penalize fast moves toward more leverage. A
rating-constrained firm should move gradually even when the destination is right. Where a
rating constraint binds, price it: firm value at the unconstrained optimum minus firm value
at the constrained ratio.

Do not design around analyst dilution concerns. Earnings-per-share accretion is arithmetic,
not value, and following it produces financing that fails the matching test for no gain.

## 3. Bondholder fears

Some firms pay spreads far above what their fundamentals justify. Three causes, all about
what the lender cannot see or cannot control.

- **Unobservable cash flows.** The harder it is for a lender to verify performance, the
  more it charges.
- **Intangible or illiquid assets.** Tangible, liquid, redeployable assets create few agency
  problems. Intangibles create many, because they lose most of their value in distress.
- **A record against bondholders.** A history of defaults, of debt-financed payouts, or of
  risk-shifting raises the price of every subsequent issue. So does simply being small with
  no borrowing history.

Where agency costs are substantial, hand the lender a claim that improves if the borrower
behaves badly. That is what lets the coupon fall.

| Feature | What the lender gets | Best fit |
|---|---|---|
| Convertible bond | Upside if the firm's equity value rises | High growth, hard-to-verify prospects |
| Puttable bond | The right to demand repayment on defined events | Risk-shifting or control-change fears |
| Ratings-sensitive note | A coupon that steps up if the rating falls | Leverage or payout fears |

Check the existing covenant load first. Covenants come in three categories — investment,
financing and dividend restrictions. A firm already tightly covenanted may be paying twice
for the same protection, and the right recommendation is to renegotiate rather than to add
a feature.

## 4. Information asymmetry

More uncertainty about future cash flows argues for shorter-term debt. So does a
credibility problem with lenders. Short maturities force the firm back to the market
frequently, and that recurring scrutiny is what makes the commitment credible.

This overlay pulls against maturity matching when the assets are long-lived and the firm is
not yet believed. Resolve it by naming which risk is larger: structural mismatch, or the
spread the firm pays for opacity. Say which one you chose.

## 5. Do not lock in a market mistake

This overlay can override the entire design.

**If the firm is under-rated**, issuing long-dated debt fixes a rate far above its true
default risk for the life of the bond. The mismatch cost of borrowing short is usually
smaller than the spread cost of locking in the error.

**If the stock is under-priced**, issuing equity or equity-linked paper transfers wealth
from existing holders to new ones. Convertibles are equity-linked, so a mispricing claim
can rule out the instrument the matching analysis just recommended.

When the firm must finance while mispriced, use short-term or delayed structures until the
mistake corrects.

Hold the claim to evidence. A status-quo valuation against the market price is evidence. A
synthetic rating well above the actual rating, with the gap explained, is evidence.
Management conviction that the stock is cheap is not.

## Instrument menu

| Instrument | Matches | Watch for |
|---|---|---|
| Fixed-rate straight bond | Stable income, weak pricing power, long assets | Locks in the rate, including a wrong one |
| Floating-rate debt | Income rising with inflation or rates | Stacks rate risk on a firm with weak pricing power |
| Foreign-currency debt | Revenues in that currency | Match the net exposure, not gross revenue |
| Convertible | Low current cash flow, high growth, high agency costs | Equity-linked, so mispricing matters |
| Zero-coupon | Back-loaded asset cash flows, tax deferral | Accretes; the rating impact is larger than the cash cost |
| Commodity-linked bond | A single commodity price drives income | Only for a genuinely dominant driver |
| Catastrophe or event-linked note | Insurable, well-defined tail exposure | Basis risk between the trigger and the actual loss |
| Operating lease | Asset use with a matched payment stream | It is debt; capitalize it before measuring anything |
| Quasi-equity (trust preferred) | Rating constraint at an under-levered firm | Only partial equity credit now |

Every one of these is judgment. The arithmetic that supports the choice — duration, macro
slopes, the tax rate that survives at each debt level — is scripted. The mapping from
asset behaviour to instrument is not, so state the reasoning rather than the conclusion.
