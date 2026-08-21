# FCFE: the potential dividend

**Core idea:** Free Cash Flow to Equity is the cash a firm *could* have returned to stockholders after paying non-equity claimholders (debt and preferred) and after making the reinvestment needed to sustain assets and fund growth. It is the benchmark against which actual payout is judged. The logic runs down the residual claim: start with cash flow from operations, pay debt (interest and principal), subtract reinvestment in long-term assets (cap ex) and short-term assets (working capital), and what is left is the potential dividend. A firm that pays out less than FCFE accumulates cash on the balance sheet; a firm that pays out more must draw down cash, borrow, or issue equity. FCFE is the single most important number in dividend analysis.

**Formulas:**

*Standard form:*
FCFE = Net Income + Depreciation − Cap Ex − Change in Non-cash Working Capital + New Debt Issued − Debt Repaid

*Modified form (grouping the terms as they are used in practice):*
FCFE = Net Income − (Cap Ex − Depreciation + Change in Working Capital) + (New Debt Issued − Debt Repaid)
where the middle bracket is **Reinvestment** and the last bracket is **Net Cash Flow from Debt**.

*Simplified form, constant debt ratio (the "target debt ratio" FCFE):*
FCFE = Net Income − (Cap Ex − Depreciation) × (1 − DR) − (Change in Working Capital) × (1 − DR)
= Net Income − (1 − DR) × [(Cap Ex − Depreciation) + Change in Working Capital]

*Full form including preferred stock (application template):*
FCFE = Net Income + Depreciation & Amortization − Capital Expenditures − Change in Non-cash Working Capital − Preferred Dividend − Principal Repaid + New Debt Issued

*From the cash flow statement as reported (sign conventions already embedded):*
FCFE = Net Income + Depreciation & Amortization + Capital Expenditures (as reported, negative) + Changes in Non-cash Working Capital (as reported) + Preferred Dividend (as reported) + Increase in LT Borrowing + Decrease in LT Borrowing + Change in ST Borrowing

*Equity reinvestment view:*
Equity Reinvestment = (Cap Ex − Depreciation) + Change in Working Capital − Change in Debt
Equity Reinvestment Rate = Equity Reinvestment / Net Income
FCFE = Net Income − Equity Reinvestment

**Symbols:**
- Net Income = earnings available to common stockholders, after interest and taxes
- Cap Ex = capital expenditures, including acquisitions and other growth investments
- Depreciation = depreciation and amortization
- Change in Working Capital = change in **non-cash** working capital
- New Debt Issued / Debt Repaid = gross debt cash flows; the difference is net debt issued
- DR = debt ratio, debt as a fraction of capital (Debt / (Debt + Equity)), either the current or a target ratio
- Preferred Dividend = dividends paid to preferred stockholders

**Related cash flow measures for comparison:**
- Augmented Dividends = Dividends + Stock Buybacks (the actual cash returned)
- FCFF = EBIT × (1 − tax rate) − (Cap Ex − Depreciation) − Change in Working Capital (a pre-debt measure; used when the debt ratio is expected to change)

**Procedure:**
1. Choose a period. Damodaran uses the last 5 years (up to 10 in the model), because any single year's cap ex or debt issuance can distort the picture.
2. Pull the raw inputs per year: net income, depreciation and amortization, capital spending (including acquisitions), change in non-cash working capital, net debt issued, and preferred dividends if any.
3. Compute three variants of FCFE for each year and in aggregate:
   - **Pre-debt FCFE** = NI − (CapEx − Depr) − ΔWC. This ignores debt cash flows entirely.
   - **Actual-debt FCFE** = Pre-debt FCFE + Net Debt Issued. This uses what the firm actually borrowed.
   - **Target-debt-ratio FCFE** = NI − (1 − DR) × [(CapEx − Depr) + ΔWC]. This assumes a stable debt ratio funded the reinvestment.
4. Decide which variant to lead with. Rule: use the target-debt-ratio version when actual net debt cash flows are lumpy across the period, because a single large borrowing year makes actual-debt FCFE look artificially generous. Use the actual-debt version when the debt policy is stable and deliberate.
5. Set DR. Use the current debt ratio (market value of debt / (debt + market value of equity)) unless you have a reason to move to a target, in which case use the target and say so.
6. Compare aggregate FCFE with aggregate cash returned (dividends + buybacks) over the same period. Compute Cash returned / FCFE for each of the three variants. Above 100% means overpaying, below means accumulating.
7. Handle special cases. For a financial services firm, conventional cap ex and working capital are meaningless — use the bank version instead (see [[fcfe-for-banks]]). For a firm with negative net income, FCFE is usually deeply negative and the payout question becomes a financing question.
8. Feed the result into the assessment framework ([[cash-trust-assessment]] and [[dividend-matrix]]).

**Reference data — the residual-claim waterfall (the logic behind the formula):**

| Step | Item | Question it answers |
|---|---|---|
| 1 | Cash flow from operations = After-tax operating income + Depreciation | How much does the business generate? |
| 2 | − Principal repaid, − Interest expenses | How much did you borrow? |
| 3 | = Cash flow from operations to equity investors | — |
| 4 | − Cap ex (long-term assets), − Change in working capital (short-term assets) | How good are your investment choices? |
| 5 | = **Potential Dividends (FCFE)** | — |
| 6 | − Cash retained | What is a reasonable cash balance? |
| 7 | = Cash paid out, split between buybacks and dividends | What do your stockholders prefer? |

*Global distribution of firms by FCFE sign and payout (reference for how common each case is):*

| Category | Australia/NZ/Canada | Developed Europe | Emerging Markets | Japan | United States | Global |
|---|---|---|---|---|---|---|
| FCFE>0, Dividends+Buybacks = 0 | 34.68% | 15.35% | 9.33% | 4.55% | 16.08% | 14.53% |
| FCFE>0, FCFE > Dividends+Buybacks | 12.40% | 18.38% | 21.29% | 13.26% | 31.93% | 21.01% |
| **Cash accumulators (subtotal)** | 47.08% | 33.73% | 30.62% | 17.81% | 48.01% | 35.54% |
| FCFE<0, Dividends+Buybacks = 0 | 28.19% | 13.53% | 11.75% | 6.07% | 8.64% | 11.60% |
| FCFE>0, Dividends+Buybacks > FCFE | 14.16% | 33.23% | 30.39% | 44.18% | 22.96% | 29.16% |
| FCFE<0, Dividends+Buybacks > 0 | 10.57% | 19.51% | 27.24% | 31.94% | 20.39% | 23.70% |
| **Cash overpayers (subtotal)** | 24.73% | 52.74% | 57.63% | 76.12% | 43.35% | 52.86% |

Definitions: a **cash accumulator** has FCFE > 0 and returns less than FCFE (including zero). A **cash overpayer** returns more than FCFE (including any positive payout when FCFE < 0).

**Worked example 1 — Disney, 2008–2012 ($ millions):**

| Item | 2012 | 2011 | 2010 | 2009 | 2008 | Aggregate |
|---|---|---|---|---|---|---|
| Net Income | 6,136 | 5,682 | 4,807 | 3,963 | 3,307 | 23,895 |
| − (Cap Ex − Depreciation) | 604 | 1,797 | 1,718 | 397 | 122 | 4,638 |
| − Change in Working Capital | (133) | 940 | 950 | 308 | (109) | 1,956 |
| = FCFE (pre-debt) | 5,665 | 2,945 | 2,139 | 3,258 | 3,294 | 17,301 |
| + Net CF from Debt | 1,881 | 4,246 | 2,743 | 1,190 | (235) | 9,825 |
| = FCFE (actual debt) | 7,546 | 7,191 | 4,882 | 4,448 | 3,059 | 27,126 |
| FCFE (target debt ratio 11.58%) | 5,720 | 3,262 | 2,448 | 3,340 | 3,296 | 18,065 |
| Dividends | 1,324 | 1,076 | 756 | 653 | 648 | 4,457 |
| Dividends + Buybacks | 5,411 | 4,091 | 5,749 | 3,322 | 1,296 | 19,869 |

Check 2012: pre-debt FCFE = 6,136 − 604 − (−133) = 5,665. Target-ratio FCFE = 6,136 − (604 + (−133)) × (1 − 0.115793) = 6,136 − 471 × 0.884207 = 5,719.5. Over the five years Disney returned $19,869M against target-ratio FCFE of $18,065M — about $1.5 billion more than it could afford at its current 11.58% debt ratio (110.0% of target FCFE), but only 73.2% of actual-debt FCFE of $27,126M. The choice of FCFE variant flips the verdict, which is exactly why all three are reported.

**Worked example 2 — Microsoft 1996, how cash balances get built:** Net Income $2,176M; Cap Ex $494M; Depreciation $480M; Change in non-cash Working Capital $35M; Debt: none.
FCFE = 2,176 − (494 − 480) − 35 − 0 = **$2,127M**.
Microsoft could have paid $2,127M in dividends or buybacks in 1996 and paid nothing. That $2,127M shows up as cash and marketable securities on the balance sheet. Repeat this for a decade and you get the $43 billion cash balance Microsoft held by 2002.

**Worked example 3 — equity reinvestment view, Tata Motors (₹ millions):**

| Year | Net Income | Cap Ex | Depreciation | Δ WC | Δ Debt | Equity Reinvestment | Reinvestment Rate |
|---|---|---|---|---|---|---|---|
| 2008-09 | −25,053 | 99,708 | 25,072 | 13,441 | 25,789 | 62,288 | −248.63% |
| 2009-10 | 29,151 | 84,754 | 39,602 | −26,009 | 5,605 | 13,538 | 46.44% |
| 2010-11 | 92,736 | 81,240 | 46,510 | 50,484 | 24,951 | 60,263 | 64.98% |
| 2011-12 | 135,165 | 138,756 | 56,209 | 22,801 | 30,846 | 74,502 | 55.12% |
| 2012-13 | 98,926 | 187,570 | 75,648 | 680 | 32,970 | 79,632 | 80.50% |
| Aggregate | 330,925 | 592,028 | 243,041 | 61,397 | 120,160 | 290,224 | 87.70% |

Check 2012-13: Equity Reinvestment = (187,570 − 75,648) + 680 − 32,970 = 79,632. FCFE = 98,926 − 79,632 = ₹19,294M. In aggregate Tata Motors reinvested 87.70% of net income, leaving only 12.3% as potential dividends.

**Determinism:**
- DETERMINISTIC: every FCFE variant, the equity reinvestment rate, the accumulator/overpayer classification, and the cash-returned-to-FCFE ratios — all follow arithmetically from net income, depreciation, cap ex, change in non-cash working capital, net debt issued, preferred dividends, dividends, buybacks and the debt ratio. A script computes these end to end from a cash flow statement.
- JUDGMENT: whether to use the current or a target debt ratio, and what that target should be. Whether reported cap ex includes acquisitions and whether unusual acquisitions should be normalized. Whether net income needs normalizing for a cyclical or loss-making year. Which of the three FCFE variants best represents sustainable capacity. Where to draw the line on a "reasonable cash balance" in step 6 of the waterfall.

**Pitfalls:**
- Ignoring acquisitions. Cap ex must include acquisitions, or FCFE is overstated at any acquisitive firm — this is exactly why Tata Motors and Vale show negative pre-debt FCFE.
- Leaning on actual-debt FCFE in a year of heavy borrowing. Debt-funded FCFE is not sustainable payout capacity; Tata Motors shows actual-debt FCFE of ₹825bn against target-ratio FCFE of ₹48bn.
- Using change in *total* working capital instead of non-cash working capital. Cash and short-term debt do not belong in the change.
- Sign errors when pulling from the cash flow statement. Cap ex and working capital changes arrive already signed, so they are **added**, not subtracted.
- Treating FCFE as a prescription. It is capacity, not a recommendation; whether to actually pay it out depends on trust in management and the project pipeline ([[cash-trust-assessment]]).
- Applying the standard formula to a bank or insurer. Use [[fcfe-for-banks]].
- Computing FCFE for one year only. A single year is dominated by lumpy cap ex and debt issuance.

**Sources:**
- corporate_finance--lecture_slides--cfpacket2spr20 p.149-150
- corporate_finance--lecture_slides--cfpacket2spr20 p.189
- corporate_finance--lecture_slides--cfpacket2spr20 p.193-196
- corporate_finance--lecture_slides--cfpacket2spr20 p.198-200
- corporate_finance--lecture_slides--cfpacket2spr20 p.233
- corporate_finance--lecture_slides--cfpacket2spr20 p.235
- corpfin-payout-projects — dividends.xls, sheets `Inputs` and `Analysis of past dividends` (rows 6, 8, 9)

**Related:** [[cash-trust-assessment]], [[dividend-matrix]], [[fcfe-for-banks]], [[cash-returned-dividends-and-buybacks]], [[payout-forecasting]], [[dividend-life-cycle]], [[dividend-payout-and-yield-measures]], [[fcff]], [[dividend-discount-model]]
