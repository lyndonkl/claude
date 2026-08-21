# Payout policy — methodology notes

Long-form backing for `SKILL.md`. Read the operating manual first; come here for the
derivations, the base rates, and the constraints on executing a change.

## 1. The residual-claim waterfall

Payout is the third decision, not the first. Invest in assets that clear the hurdle rate,
finance with the right mix of debt and equity, and return what is left. The waterfall:

| Step | Item | Question it answers |
|---|---|---|
| 1 | Cash flow from operations = after-tax operating income + depreciation | How much does the business generate? |
| 2 | − interest and principal repaid, + new borrowing | How much did you borrow? |
| 3 | = cash flow from operations to equity investors | — |
| 4 | − cap ex, − change in non-cash working capital | How good are your investment choices? |
| 5 | = potential dividends (FCFE) | — |
| 6 | − cash retained | What is a reasonable cash balance? |
| 7 | = cash paid out, split between dividends and buybacks | What do your stockholders prefer? |

Steps 1 to 5 are arithmetic. Steps 6 and 7 are judgment, and that is where the trust
question lives.

Real policy does not run this way. Two forces dominate everywhere: inertia, where firms
will not let go of past dividend behaviour, and me-too-ism, where firms copy their peer
group. Every tool in this skill exists because of the gap between the waterfall and what
firms actually do.

## 2. The FCFE variants in full

**Standard form**

    FCFE = Net Income + Depreciation − Cap Ex − ΔNon-cash Working Capital
           + New Debt Issued − Debt Repaid

**Grouped form**, which is how the engine computes it:

    Reinvestment      = (Cap Ex − Depreciation) + ΔWorking Capital
    FCFE (pre-debt)   = Net Income − Reinvestment
    FCFE (actual)     = FCFE (pre-debt) + Net Debt Issued
    FCFE (target DR)  = Net Income − Reinvestment × (1 − DR)

**Full form with preferred stock**

    FCFE = Net Income + D&A − Cap Ex − ΔNon-cash WC − Preferred Dividend
           − Principal Repaid + New Debt Issued

**From the cash flow statement as reported.** Cap ex and working capital changes arrive
already signed, so they are added rather than subtracted:

    FCFE = Net Income + D&A + Cap Ex (negative as reported)
           + ΔNon-cash WC (as reported) + Preferred Dividend (as reported)
           + Increase in LT Borrowing + Decrease in LT Borrowing + Change in ST Borrowing

**Equity reinvestment view**, useful when you want the reinvestment rate directly:

    Equity Reinvestment      = (Cap Ex − Depreciation) + ΔWorking Capital − ΔDebt
    Equity Reinvestment Rate = Equity Reinvestment / Net Income
    FCFE                     = Net Income − Equity Reinvestment

Tata Motors over five years: aggregate equity reinvestment ₹290,224M on net income of
₹330,925M, a rate of 87.70%. Only 12.3% of earnings was available as potential dividends.

**Cap ex must include acquisitions.** Leaving them out overstates FCFE at any acquisitive
firm, which is exactly why Tata Motors and Vale show negative pre-debt FCFE.

## 3. Global base rates for the cash verdict

A cash accumulator has FCFE above zero and returns less than FCFE. A cash overpayer returns
more than FCFE, including any positive payout on negative FCFE.

| Category | Aus/NZ/Can | Dev. Europe | Emerging | Japan | US | Global |
|---|---|---|---|---|---|---|
| FCFE>0, no payout | 34.68% | 15.35% | 9.33% | 4.55% | 16.08% | 14.53% |
| FCFE>0, payout < FCFE | 12.40% | 18.38% | 21.29% | 13.26% | 31.93% | 21.01% |
| **Accumulators** | **47.08%** | **33.73%** | **30.62%** | **17.81%** | **48.01%** | **35.54%** |
| FCFE<0, no payout | 28.19% | 13.53% | 11.75% | 6.07% | 8.64% | 11.60% |
| FCFE>0, payout > FCFE | 14.16% | 33.23% | 30.39% | 44.18% | 22.96% | 29.16% |
| FCFE<0, with payout | 10.57% | 19.51% | 27.24% | 31.94% | 20.39% | 23.70% |
| **Overpayers** | **24.73%** | **52.74%** | **57.63%** | **76.12%** | **43.35%** | **52.86%** |

Overpaying is the majority case globally. A firm returning more than its FCFE is not
unusual, so the finding is the size of the gap and the quality of the projects, not the
sign alone.

## 4. Case placements from the course

| Firm | Cash | Projects | Prescription |
|---|---|---|---|
| Baidu 2013 | Surplus | Good | Maximum flexibility |
| Disney 2003 | Surplus | Poor | Heavy pressure to pay out |
| Disney 2013 | Deficit on target-ratio FCFE | Good | Reduce the cash payout |
| Deutsche Bank 2013 | Deficit | Poor | Cut, but fix investment policy first |
| Vale 2013 | Deficit (223% of target FCFE) | Good | Reduce the cash payout |
| Tata Motors 2013 | Deficit (157% of target FCFE) | Good | Reduce the cash payout |
| BP 1982–91 | Deficit (262% of FCFE) | Poor | Cut, and restructure |
| The Limited 1983–92 | Deficit (FCFE negative) | Good | Cut or end the payout |

**Disney across three decades** shows that quadrants are not permanent. In 2003 it
generated $969M of FCFE a year and returned $639M, with ROE about 2% below the cost of
equity and a negative Jensen's alpha, most of the damage dating from the 1996 Capital
Cities acquisition. That is surplus plus poor projects. By 2009 Bob Iger had replaced
Michael Eisner, alpha had turned positive, and return on capital had moved above the cost
of capital. By 2013 Disney was earning excess returns and had earned the flexibility to
hold cash. Re-run the assessment annually.

**BP 1992** shows what a forced cut looks like. BP paid 262% of FCFE while earning 1.67%
below its required return. It cut the dividend by 55%, took a $1.52bn pretax restructuring
charge, and laid off 11,500 people, five weeks after its chairman resigned under board
pressure. The ADRs fell 7.36% on the day. The diagnosis matched the framework: costly
acquisitions and capital spending that replaced 120–130% of annual production.

**The Limited 1983–92** shows how a low payout ratio hides a deficit. Its dividend payout
ratio was 18.59%, which looks conservative. Average FCFE was −$34.2M against average
dividends of $40.9M, and the firm had value-creating projects to fund.

## 5. Dividend stickiness and the cost of a cut

Four empirical regularities constrain any recommendation.

1. **Dividends are sticky.** Among US firms from 1988 to 2019, roughly 55–73% of firms
   changed nothing in a given year, 20–40% increased, and 3–12% cut. In the worst quarter
   of the 2008 crisis only 27 of the S&P 500 cut or suspended.
2. **Dividends follow earnings**, with a lag and far less volatility. Payout ratios spike
   when earnings collapse, not when dividends rise.
3. **Tax law moves dividends.** In 2003, when US dividend tax rates fell to parity with
   capital gains, 21 S&P 500 firms initiated and 247 increased. In Q4 2012, ahead of an
   expected reversion, 233 firms paid out $31bn, and 101 of them had insider holdings above
   20% of shares outstanding.
4. **Buybacks displaced dividends.** In 2019 S&P 500 buybacks ran about $770bn against
   $480bn of dividends.

The practical asymmetry: treat an increase as permanent, and treat a cut as expensive.

**Framing a cut changes the market reaction.**

| How the cut was announced | Prior quarter | Announcement | Quarter after |
|---|---|---|---|
| With an earnings decline or loss (N=176) | −7.23% | −8.17% | +1.80% |
| After a prior earnings decline (N=208) | −7.58% | −5.52% | +1.07% |
| With an investment or growth story (N=16) | −7.69% | −5.16% | **+8.79%** |

The growth-story sample is small, so read it as directional. The direction is clear
enough: a cut bundled with a credible investment plan recovers, and a cut bundled with bad
earnings news does not.

## 6. Constraints on executing a change

- **Clientele.** A firm with a long dividend history holds income-seeking shareholders who
  will sell if the dividend is cut. This is why firms facing new investment needs usually
  keep paying and issue stock instead.
- **Contract.** Vale promised preferred stockholders at least 35% of earnings; missing that
  threshold hands them voting rights. An economic decision becomes a control decision.
- **Regulation.** Mandated minimum payouts exist in several emerging markets. They hurt
  high-growth firms worst, profitable or not, because their FCFE is negative and the
  mandated dividend must be funded externally. A cap on payout with forced reinvestment
  does the mirror-image damage to mature firms with poor projects.
- **Flotation cost** of keeping an unaffordable dividend and issuing stock for the
  shortfall: about 22% for issues under $1M, 12.5% at $2–5M, 6% at $10–20M, and 3.5% above
  $50M. Price it before recommending that route.

Where a firm has a large dividend history and now needs to fund major investment, lay out
all three options: cut and invest; keep the dividend and defer investment; or keep the
dividend, invest, and issue stock for the gap. Firms overwhelmingly choose the third
because of the clientele constraint. Say so, price the flotation cost, and make the
tradeoff visible.

**Do not initiate a dividend at a growth firm to widen the investor base.** The argument is
that some institutions cannot hold non-payers. The arithmetic kills it: a high-growth firm
has negative FCFE, so the dividend has to be funded by issuing stock or by underinvesting.
An initiation also signals that high growth is over.

## 7. Choosing the form: dividends or buybacks

Buybacks are roughly 60% of cash returned in the US and 48% in Canada, against 5% in China
and 5% in Africa and the Middle East. Japan sits in the middle at 38%. Any cross-region
payout comparison that ignores this is wrong by a factor of two.

Rules for the form of a payout change:

- One-time or uncertain surplus → buyback or special dividend. No stickiness commitment.
- Recurring, predictable surplus at a mature firm → dividend increase, which the market
  reads as a commitment.
- Income-seeking investor base → dividends.
- Taxable investors who prefer deferral, or management convinced the stock is cheap →
  buybacks.

Net buybacks against equity issuance where stock compensation is large. Gross repurchases
at such a firm partly offset dilution rather than returning cash. A buyback does not create
value per share by shrinking the count; EPS accretion is not value creation.

## 8. FCFE for banks, in detail

Cap ex and non-cash working capital are meaningless at a bank, and debt is part of the
product rather than a financing choice. Reinvestment is the increase in regulatory capital
needed to support a larger balance sheet.

```
Tier 1 Capital_t          = Risk-Adjusted Assets_t × Tier 1 Ratio_t
Investment in Reg Capital = Tier 1 Capital_t − Tier 1 Capital_(t−1)
Book Equity_t             = Book Equity_(t−1) + Investment in Reg Capital_t
Net Income_t              = Book Equity_t × Expected ROE_t
FCFE_t                    = Net Income_t − Investment in Reg Capital_t
```

The table is recursive: retained capital raises book equity, which drives next year's net
income through ROE.

The ratio ramp usually matters more than asset growth. Deutsche Bank in October 2016 had
assets growing only 1% a year. Year one's capital build of €6,552M still came to roughly
four times the steady-state annual build. The cause was the Tier 1 ratio being lifted from
12.41% toward 15.67%.

Tier 1 capital and book equity are not the same thing. Deutsche Bank in 2013 carried Tier 1
of €66,561M against book equity of €76,829M. Project both, and be explicit that one drives
reinvestment while the other drives income.

Do not extrapolate a negative-ROE year forever. The projection needs a convergence
assumption toward a sustainable ROE, and that assumption should be stated and defended,
because for a troubled bank it decides the answer.

## 9. Reference distributions for positioning a firm

*Dividend payers and non-payers, January 2020:* globally 18,823 payers against 8,043
non-payers, so 29.94% of listed firms pay nothing. Non-payer share runs from 13.65% in
China and 17.25% in the UK to 40.35% in the United States and 61.51% in India.

*Payout ratios among payers:* the mode is the 20–30% bucket, and about 15% of payers
globally pay out more than they earn. A payout above 100% is common rather than a data
error.

*Average dividend yields, January 2020:* global 2.34%, United States 1.68%, India 1.29%,
Japan 2.08%, Eastern Europe and Russia 5.91%. Most firms yield between 0.5% and 2.5%, and
roughly 7–8% yield above 8%, which usually signals a depressed price rather than
generosity.

*Payout and yield by expected growth class (US):* payout falls from about 44% in the 0–3%
growth class to about 20% above 25%, and yield from about 3.75% to about 1.1%. Both series
are dividend-only, so buyback-heavy firms look lower-payout than they are.

The machine-readable versions of these tables live in
`resources/data/payout_benchmarks.json`, tagged `as_of: 2020-01`.

## 10. Sources

All figures trace to Aswath Damodaran's corporate finance lecture packet
(`cfpacket2spr20`, pages 148–223) and to `dividends.xls`, sheets `Inputs`,
`Analysis of past dividends` and `Forecasted Dividends & FCFE`. The January 2014 payout and
yield regressions come from pages 222–223. The peer table for US Entertainment comes from
pages 220–221. Its printed payout column was built from per-share trailing figures and does
not reconcile with the net income column beside it. This engine therefore recomputes that
column rather than reproducing it.
