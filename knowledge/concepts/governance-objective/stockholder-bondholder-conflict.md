# The Stockholder-Bondholder Conflict

**Core idea:** In theory stockholders and bondholders want the same thing: a healthy firm. In practice their objectives diverge because their claims differ. Bondholders hold a fixed claim, so they care about safety and about getting paid. Stockholders hold a residual claim, so they care about upside. That asymmetry gives stockholders three ways to move wealth from lenders to themselves after the debt is issued: pay the cash out, raise the risk of the assets, or borrow more against the same assets. Lenders who saw this coming now defend themselves with covenants and with bond structures that reprice or repay when the firm turns riskier. An analyst checks both sides: how exposed are the lenders, and how well have they protected themselves?

**Formulas:** No arithmetic on the slides. The three expropriation channels, stated as mechanisms:

```
Channel 1: Cash payout (dividend/buyback surge)
  Cash leaves the firm -> firm becomes riskier -> bond value falls,
  stockholders capture the cash.

Channel 2: Risk shifting (asset substitution)
  Lenders set the interest rate on their perception of asset risk at
  issue. Stockholders then invest in riskier assets than agreed.
  Upside accrues to equity; downside is shared with lenders who were
  not paid for it.

Channel 3: Claim dilution (borrowing more on the same assets)
  New debt on the same asset base -> existing lenders' claim is
  diluted -> all existing lenders are worse off.
```

A useful measure of realized expropriation:
```
Bondholder loss (%) = (Bond price before event - Bond price after event)
                      / Bond price before event
```

**Procedure:** Assessing the conflict at a real company:
1. Read the covenants on every outstanding debt instrument. Sort them into three buckets: restrictions on investment policy, on financing policy, and on dividend policy.
2. Score protection. No covenants and long maturities means fully exposed. Tight covenants, short maturities, or bank debt with financial maintenance tests means well protected.
3. Look for Channel 1 events: a jump in dividends or buybacks, or a special dividend, that is not matched by operating cash flow.
4. Look for Channel 2 events: entry into a materially riskier business, a shift in the investment mix, or a rise in earnings volatility after debt was issued.
5. Look for Channel 3 events: new debt issued against the same assets, a leveraged buyout, a leveraged recapitalization, or a large debt-funded acquisition.
6. Check whether the bonds carry structural defenses (below). Puttable bonds and ratings-sensitive notes neutralize Channels 2 and 3.
7. Conclude. If lenders are unprotected and any channel is live, the objective must step back from stockholder wealth to firm value (see [[modified-objective-function]]).

**Reference data:** *How bondholders defend themselves — the three counter-mechanisms.*

| Defense | What it is | Which channel it blocks |
|---|---|---|
| **More restrictive covenants** | Restrictions on investment, financing and dividend policy, now standard in private lending agreements and bond issues. Explicit goal: prevent future "Nabiscos." | All three |
| **New bond types** | *Puttable bonds*: the bondholder can put the bond back to the firm at face value if the firm takes actions that hurt bondholders. *Ratings sensitive notes*: the interest rate adjusts to the rate appropriate for the firm's current rating. | Channels 2 and 3 |
| **Hybrid bonds with an equity component** | Usually a conversion option or a warrant, letting bondholders become equity investors when that serves their interests. | Lets lenders share the upside they would otherwise be denied |

*RJR Nabisco 30-year bond, 8 3/8% coupon due 2016, around the October 1988 LBO announcement:*

| Date window | Approximate price |
|---|---|
| 10/10 - 10/20 (pre-announcement) | ~87 |
| 10/24 - 10/26 (post-announcement) | ~70 |
| Early November | ~74-75 |

**Worked example:** RJR Nabisco, October 1988. The LBO announcement sharply raised the firm's leverage. The 8.375% bond due 2016 fell from about 87 to about 70, then stabilized near 74. Bondholder loss at the trough = (87 - 70) / 87 = **19.5%**. Loss at the stabilized level = (87 - 74) / 87 = **14.9%**. Nothing about the operating business changed in those two weeks. The entire loss is a transfer from unprotected lenders to the LBO's equity, achieved purely through Channel 3, claim dilution. This is why post-1988 bond indentures carry event-risk and change-of-control covenants.

**Determinism:**
- DETERMINISTIC: bondholder loss percentage (pre-price, post-price -> % loss); counting covenants by category; comparing debt maturity schedules; checking for the presence of a put or ratings-sensitive feature.
- JUDGMENT: whether observed actions constitute expropriation or ordinary business; whether covenants are tight enough to count as "protected"; whether a risk shift was deliberate; whether the bond price move reflects expropriation or a change in fundamentals.

**Pitfalls:**
- Assuming no conflict exists because both parties want the firm to survive. They differ on how much risk is acceptable to get there.
- Treating a dividend or buyback as neutral for lenders. Cash leaving the firm makes the remaining claim riskier.
- Ignoring risk shifting because leverage is unchanged. Channel 2 changes asset risk, not the debt ratio.
- Assuming an investment-grade rating means the lenders are protected. RJR Nabisco was investment grade before the LBO.
- Checking covenants only at issue. Covenants can be amended, waived, or superseded by new debt at a different level in the capital structure.

**Sources:**
- corporate_finance--lecture_slides--cfpacket1spr20 p.32-34
- corporate_finance--lecture_slides--cfpacket1spr20 p.69

**Related:** [[classical-objective-function-assumptions]], [[modified-objective-function]], [[self-correction-and-counter-forces]], [[managerial-entrenchment-and-takeover-defenses]], [[cost-of-debt]], [[bond-ratings]], [[optimal-debt-ratio]]
