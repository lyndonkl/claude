# The cash/trust assessment of dividend policy

**Core idea:** There are two ways to judge a firm's dividend policy. The **cash/trust nexus** asks how much cash the firm could return versus how much it actually returns, and then asks whether management can be trusted as custodian of any cash held back. The **peer group approach** simply matches the firm to comparable companies (see [[peer-group-payout-analysis]]). The cash/trust approach is the analytically serious one, and it reduces to three steps: how much did you pay out, how much could you have paid out, and how much do I trust you with the difference? Trust is not a feeling — it is measured by whether management earned excess returns on the projects it took and whether the stock beat its required return.

**Formulas:**

*Step 1 — actual payout:*
Cash returned = Dividends + Equity Repurchases (see [[cash-returned-dividends-and-buybacks]])

*Step 2 — potential payout:*
FCFE = Net Income − (Cap Ex − Depreciation) × (1 − DR) − (Change in Working Capital) × (1 − DR), where DR = the debt ratio (fraction of reinvestment funded with debt). Also compute the pre-debt and actual-debt variants; see [[fcfe-potential-dividends]].
Surplus or deficit = FCFE − Cash returned. Cash paid as % of FCFE = Cash returned / FCFE.

*Step 3 — trust, measured two ways:*
- Project quality: ROE_t = Net Income_t / Book Value of Equity_t; Required Return_t = Rf_t + β × (Rm_t − Rf_t); Excess return on equity = ROE_t − Required Return_t. The firm-level analogue is ROC − Cost of Capital.
- Stock performance (Jensen's alpha): α_t = Stock Return_t − Required Return_t, where Stock Return_t = price appreciation plus dividend yield in year t, and Required Return_t is the CAPM return using that year's T-bill rate and market return.
- Period summaries: Average ROE = Σ Net Income / Σ Book Equity (a ratio of sums). Average Required Return and Average Stock Return are arithmetic means over the years used. ROE − Required = the trust verdict on projects; Actual − Required = the trust verdict from the market.

*Cash accumulation identity:*
Cumulated cash_t = Cumulated cash_(t−1) + FCFE_t − Cash returned_t. A firm with persistent positive FCFE and low payout builds a cash pile mechanically.

**Procedure:**
1. Pick a window of 5 years (Damodaran's model allows 1 to 10). Enter net income, depreciation, capital spending including acquisitions, change in non-cash working capital, net debt issued, dividends and equity repurchases for each year, most recent first.
2. Set the debt ratio. Use the current debt-to-capital ratio unless you are deliberately moving the firm to a target, in which case use the target.
3. Compute the three FCFE variants per year and in aggregate, along with cash returned per year.
4. Compute cash returned as a percentage of each FCFE variant. Report all three — they frequently disagree, and the disagreement is itself the finding.
5. Compute annual ROE, the CAPM required return using that year's risk-free rate and market return, the excess ROE, the stock return and Jensen's alpha. Average them over the window.
6. Render the trust verdict:
   - ROE − Required Return > 0 **and** Jensen's alpha > 0 → good project record, high trust, the firm has earned the flexibility to hold cash.
   - Both negative → poor record, low trust, expect and support pressure to pay out more.
   - Mixed → weigh the project measure more heavily for the payout decision (the stock measure includes market-wide revaluation the managers did not create), and say which you are relying on.
7. Combine the cash verdict and the trust verdict into a recommendation using [[dividend-matrix]].
8. Re-run the assessment periodically. Trust is not permanent — it is earned and lost, and the same firm can move across the matrix within a few years.

**Reference data:**

*The three steps:*

| Step | Question | How it is answered |
|---|---|---|
| 1 | How much did the company pay out? | Dividends + buybacks over the period |
| 2 | How much could it have paid out? | FCFE over the period (three variants) |
| 3 | How much do I trust management with the difference? | Quality of past investments (ROE vs cost of equity, ROC vs WACC) and stock performance (Jensen's alpha) |

*Global base rates for the cash verdict (share of firms):* globally about **35.5%** of firms are cash accumulators and about **52.9%** are cash overpayers. Japan has the most overpayers (76.12%); Australia/NZ/Canada (47.08%) and the US (48.01%) have the most accumulators. Full regional table in [[fcfe-potential-dividends]].

*Model implementation (dividends.xls, `Analysis of past dividends`), with the exact aggregation rules:*
- Per year t: FCFE_predebt = NI − (CapEx − Depr) − ΔWC; FCFE_actual = FCFE_predebt + Net Debt Issued; FCFE_target = NI − (CapEx − Depr)(1 − DR) − ΔWC(1 − DR); Cash = Dividends + Buybacks; Payout = Dividends/NI; Cash%FCFE = Cash/FCFE_actual.
- ROE_t = NI_t / Book Equity_t (same-year book value as entered). Required Return_t = Rf_t + β(Rm_t − Rf_t). Jensen's alpha_t = Stock Return_t − Required Return_t.
- Aggregates: ratio-of-sums for payout ratios; arithmetic means for the return series. Both the aggregate ratio and the average-of-annual-ratios are reported and they differ — keep both.
- **Known quirk in the original sheet:** Average ROE sums net income and book equity over **all ten** input rows regardless of how many years the user selected, unlike every other statistic which respects the selected window. A faithful port reproduces this; a corrected port restricts to the selected years and should flag the difference. In the sheet's example, the quirk gives 3.02% versus 3.15% for the mean of the annual ROEs.

**Worked example — Disney, 5 years to FY2013 (dividends.xls default case, $ millions):**
Inputs: net income 6,136 / 5,682 / 4,807 / 3,963 / 3,307; depreciation 2,192 / 1,987 / 1,841 / 1,713 / 1,631; cap ex 2,796 / 3,784 / 3,559 / 2,110 / 1,753; ΔWC −133 / 940 / 950 / 308 / −109; net debt issued 1,881 / 4,246 / 2,743 / 1,190 / −235; dividends 1,324 / 1,076 / 756 / 653 / 648; buybacks 4,087 / 3,015 / 4,993 / 2,669 / 648. Beta 0.9011; current debt-to-capital 11.579%.

Year 1: FCFE_predebt = 6,136 − (2,796 − 2,192) − (−133) = **5,665**; FCFE_actual = 5,665 + 1,881 = **7,546**; FCFE_target = 6,136 − 471 × (1 − 0.115793) = **5,719.5**. Cash returned = 1,324 + 4,087 = **5,411** = 71.7% of actual FCFE. Required return = 0.0155 + 0.9011 × (0.312236 − 0.0155) = **28.29%**; Jensen's alpha = 0.3533 − 0.282889 = **+7.04%**; ROE = 6,136 / 380,078 = **1.61%**.

Over five years: cash returned 19,869 against actual FCFE 27,126 (**73.2%**), pre-debt FCFE 17,301 (**114.8%**) and target-ratio FCFE 18,065 (**110.0%**). Cash payout ratio = 19,869 / 23,895 = **83.2%**. Average ROE 3.02% versus average required return 11.22% → **ROE − Required = −8.21%** (poor projects on this measure), yet the stock beat its required return by **+6.42%** per year.

The verdict is genuinely mixed and shows why both trust measures are reported. On the accounting measure management destroyed value; on the market measure it created value. The cash verdict also depends on the FCFE variant: Disney is a modest accumulator against actual-debt FCFE and a modest overpayer against target-ratio FCFE.

**Two cautionary cases:**
- **Microsoft.** By 2002 it had built a $43 billion cash balance while paying no dividends. At the end of 2003 stockholders were not upset — the project record earned management that trust. In 2004 Microsoft announced a $33 billion special dividend and promised more, showing that flexibility, once granted, can also be handed back.
- **Chrysler, 1985–1994.** FCFE ran far above cash returned in most years — roughly $1.4–1.6bn in 1985-86 and about $2.6bn in 1992, against payouts of a few hundred million. Cumulated cash grew from roughly $1,000M to over $8,000M by 1994, and the pile drew Kirk Kerkorian's activist campaign. Large cash balances at a low-trust firm invite blowback.

**Determinism:**
- DETERMINISTIC: steps 1 and 2 in full — cash returned, all three FCFE variants, payout ratios, cash-as-%-of-FCFE, ROE, the CAPM required return, Jensen's alpha, and all period aggregates. Given the input arrays and beta, a script reproduces the entire model.
- JUDGMENT: step 3's conclusion. The numbers give ROE − cost of equity and alpha; deciding whether that record justifies letting management hold cash requires reading management continuity, governance, the source of the excess returns, and whether the record is likely to repeat. Also judgment: the choice of window, the debt ratio, whether to normalize earnings, and which trust measure to weight when they disagree.

**Pitfalls:**
- Reporting one FCFE variant. Disney's verdict flips between accumulator and overpayer depending on which is used.
- Using actual-debt FCFE in a period of heavy borrowing and calling the payout affordable.
- Judging trust from the stock return alone. A rising market lifts alpha at firms whose managers did nothing well.
- Judging trust from accounting ROE alone. Book equity is distorted by buybacks, write-offs and acquisitions — Disney's ROE of 1.6% in year 1 sits on a book equity figure inflated by acquisition accounting.
- Dividing by zero or negative denominators. Negative net income makes the payout ratio meaningless; negative FCFE makes cash-as-%-of-FCFE meaningless and negative. Report NA rather than a number.
- Reproducing the sheet's ten-row average-ROE quirk without knowing you have done so.
- Treating the assessment as permanent. Disney moved from low trust in 2003 to high trust by 2009–2013 (see [[dividend-matrix]]).

**Sources:**
- corporate_finance--lecture_slides--cfpacket2spr20 p.189-191
- corporate_finance--lecture_slides--cfpacket2spr20 p.195-196
- corporate_finance--lecture_slides--cfpacket2spr20 p.198-200
- corporate_finance--lecture_slides--cfpacket2spr20 p.203
- corporate_finance--lecture_slides--cfpacket2spr20 p.219
- corpfin-payout-projects — dividends.xls, sheets `Inputs` and `Analysis of past dividends` (rows 6–27, summary rows 31–49)

**Related:** [[fcfe-potential-dividends]], [[dividend-matrix]], [[cash-returned-dividends-and-buybacks]], [[peer-group-payout-analysis]], [[payout-forecasting]], [[fcfe-for-banks]], [[managing-dividend-changes]], [[cost-of-equity]], [[jensens-alpha]], [[return-on-capital]]
