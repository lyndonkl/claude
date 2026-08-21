# Restricted stock, pre-IPO evidence, and the Silber regression

**Core idea:** You cannot observe the illiquidity discount on a private business directly, so the standard approach borrows it from assets that are illiquid but observable. Two classes exist. **Restricted stock** is stock issued by public companies that bypasses SEC registration and cannot be traded for one year after issue; the discount is the gap between the company's traded price and the price paid in the restricted offering. **Pre-IPO transactions** are trades among equity investors in a private firm before its IPO; the discount is the gap between the later IPO offering price and the earlier transaction price. Aggregate studies put restricted-stock discounts near 33–35% and pre-IPO discounts near 42–60%. Silber (1991) went further and related the size of the discount to the offering's characteristics, which is what makes the evidence usable for a specific firm rather than as a blanket number. Both bodies of evidence carry severe sampling bias, and the pure illiquidity component may be under 10%.

**Formulas:**
- Discount definitions:
  - `Discount(restricted stock) = (Traded stock price − Price on restricted stock offering) / Traded stock price`
  - `Discount(pre-IPO) = (IPO offering price − Price on pre-IPO transaction) / IPO offering price`
- Silber (1991) regression: `LN(RPRS) = 4.33 + 0.036 LN(REV) − 0.142 LN(RBRT) + 0.174 DERN + 0.332 DCUST`
  - `RPRS` = relative price of the restricted stock to the publicly traded stock
  - `REV` = revenues of the firm, $ millions
  - `RBRT` = restricted block as a percentage of total common stock (entered as a percent, e.g. 100 for a whole-company block)
  - `DERN` = 1 if earnings are positive, 0 if negative
  - `DCUST` = 1 if there is a customer relationship with the investor, 0 otherwise (usually unused for a private-firm application)
- Implied discount from the regression: `d(REV, RBRT, DERN) = (100 − e^S) / 100`, where `S = 4.33 + 0.036 ln(REV) − 0.142 ln(RBRT) + 0.174 DERN`.
- The "refined bludgeon" as implemented in `liqdisc.xls`:
  `Illiquidity discount = BaseDiscount − [ d(10, RBRT, 1) − d(REV, RBRT, DERN) ]`
  with `BaseDiscount = 0.25`. In words: predict the discount for the subject firm and for a $10M-revenue profitable anchor with the same block size, then shift the 25% base by the gap. Because the block term appears identically in both, `RBRT` cancels exactly as the formula is written and has no effect on the output.

**Procedure:**
1. Decide what evidence class fits your situation. A whole private business resembles a pre-IPO stake more than a one-year-restricted block of a listed stock, so the higher discounts are the closer analogue — but they are also the more biased.
2. To apply the Silber-based refinement, gather: revenues in $ millions, whether earnings are positive, and the block size as a percentage.
3. Compute `S` for the subject firm and for the anchor ($10M revenues, DERN = 1, same block).
4. Convert both to predicted discounts with `d = (100 − e^S)/100`.
5. `Discount = 0.25 − [d(anchor) − d(firm)]`.
6. Sanity check against the pre-computed table below. Small profitable firms land near 25–26%; a $1bn profitable firm near 16%; unprofitable firms run about 8–9 percentage points higher at every size.
7. Discount the headline numbers for sampling bias before defending them. The firms that issue restricted stock are small and troubled and out of conventional financing options. The pre-IPO sellers are exactly the ones with the most pricing uncertainty.
8. If a firm-specific, less biased number is what you need, use the bid-ask spread route instead. See [[bid-ask-spread-illiquidity-regression]].

**Reference data — aggregate restricted-stock studies:**

| Study | Sample | Discount |
|---|---|---|
| Maher | Restricted stock purchases by four mutual funds, 1969–73 | 35.43% average |
| Moroney | 146 restricted issues bought by 10 investment companies, 1970 data | 35% mean |
| Silber (1991) | Restricted stock offerings in the 1980s | 33.75% median |

**Reference data — pre-IPO transaction discounts** (median discount on transactions in the five months before the IPO, by period, with transaction counts):

| Period | Discount | Transactions |
|---|---|---|
| 1980–81 | ~60% | 13 |
| 1985–86 | ~43% | 21 |
| 1987–89 | ~45% | 27 |
| 1989–90 | ~45% | 23 |
| 1990–92 | ~42% | 35 |
| 1991–93 | ~45% | 54 |
| 1994–95 | ~45% | 46 |
| 1995–97 | ~43% | 91 |

**Reference data — extended Silber discounts by revenue** (`liqdisc.xls`, 25% base, block 100%):

| Revenues ($mm) | Profitable | Unprofitable |
|---|---|---|
| 5 | 26.26% | 34.21% |
| 10 | 25.00% | 33.15% |
| 25 | 23.29% | 31.72% |
| 50 | 21.95% | 30.59% |
| 100 | 20.59% | 29.45% |
| 200 | 19.19% | 28.27% |
| 500 | 17.28% | 26.67% |
| 1000 | 15.79% | 25.42% |

**Reference data — the sampling problem.** Compare discounts on *all* private placements with discounts on restricted stock offerings and the difference isolates the bias. One such comparison concluded that illiquidity alone accounts for a discount of **less than 10%**, leaving the remaining 20–25 percentage points of the headline number attributable to sampling problems.

**Worked example — the restaurant.** Revenues $1.2M, profitable (DERN = 1), block 100%.
- Anchor: `S = 4.33 + 0.036 ln(10) − 0.142 ln(100) + 0.174 = 3.932977`; `d = (100 − e^3.932977)/100 = 0.489466`.
- Firm: `S = 4.33 + 0.036 ln(1.2) − 0.142 ln(100) + 0.174 = 3.856630`; `d = (100 − e^3.856630)/100 = 0.527033`.
- `Discount = 0.25 − (0.489466 − 0.527033) = 0.28757`, i.e. **28.75%** — matching the packet's "refined bludgeon" figure. Applied to $520,990 of equity that gives **$371,000**.

**Worked example — the spreadsheet's own case.** Revenues $209M, profitable, block 100%. `S_firm = 4.042398`, `d_firm = 0.430425`; anchor `d = 0.489466`. `Discount = 0.25 − (0.489466 − 0.430425) = 0.190955`, i.e. **19.10%**.

**Determinism:**
- DETERMINISTIC: `{revenues, block %, earnings dummy, base discount} → predicted discount`, exactly as implemented in the spreadsheet. The pre-computed table is a straight lookup.
- JUDGMENT: the 25% base discount itself, which is a calibration choice rather than a regression output; whether restricted stock or pre-IPO evidence is the right analogue; and how much of the headline discount to strip out for sampling bias. That judgment needs the firm's size and profitability, the buyer's situation, and a view on how comparable the study samples are to your subject.

**Pitfalls:**
- Quoting 30–35% as "the" illiquidity discount. Damodaran's own read is that illiquidity alone is worth under 10% and the rest is sampling bias.
- Expecting block size to change the answer in `liqdisc.xls`. It cancels between the anchor and the firm terms as the formula is written. A corrected port would hold the anchor's block fixed.
- Feeding revenues of zero or a block of zero into the formula. Both take a logarithm and are undefined.
- Being surprised when a tiny unprofitable firm gets a discount above the 25% base. That is intended behaviour, not an error.
- Treating pre-IPO discounts of 45% as measuring illiquidity. Those sellers were also pricing genuine uncertainty about whether the IPO would happen at all.
- Mixing editions: the anchor revenue (10) and the anchor's DERN (=1) are hard-coded in the spreadsheet formula. Only the base discount is user-settable.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket2spr21 p.143-147, p.149
- valuations--lecture_notes--spring_2020--valpacket2spr20 p.141-145, p.147
- special-private.md — liqdisc.xls, sheets "Restricted Stock Regression" and "Sheet2"

**Related:** [[illiquidity-discount]], [[bid-ask-spread-illiquidity-regression]], [[minority-discount]], [[ipo-pricing-and-underpricing]], [[private-to-private-valuation]], [[liquidation-valuation]]
