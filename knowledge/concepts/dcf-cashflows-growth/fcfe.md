# Free cash flow to equity (FCFE)

**Core idea:** FCFE is the cash left over for equity investors after operating expenses, taxes, interest, reinvestment, and net debt repayment — the **potential dividend**. It matters because the only cash an equity investor literally receives is the dividend, but managers set dividends conservatively (they smooth them, and they like holding cash for contingencies and opportunities), so actual dividends are usually below what could have been paid. Discounting actual dividends when they fall short of FCFE understates equity value. FCFE is discounted at the **cost of equity** and gives equity value directly. It is the right cash flow when leverage is stable; when leverage is changing, forecasting the debt flows becomes the hard part and firm valuation is easier.

**Formulas:**
- **Full definition:** `FCFE = Net Income − (Capital expenditures − Depreciation) − Change in non-cash working capital − (Principal repayments − New debt issues) − Preferred dividends`
- **Stable-leverage shortcut** (assume a constant fraction `DR` of reinvestment is debt-funded): `FCFE = Net Income − (1 − DR) × (Cap ex − Depreciation) − (1 − DR) × (Change in working capital)`, where `DR` = debt-to-capital ratio. This is equivalent to assuming `New debt issues = Principal repayments + DR × (Net cap ex + ΔWC)`.
- **Equity reinvestment form:** `Equity reinvestment = (Cap ex − Depreciation) + ΔWC − Change in debt`; `Equity reinvestment rate = Equity reinvestment / Net income`; `FCFE = Net income × (1 − Equity reinvestment rate)`.
- **From the cash-flow statement:** `FCFE = Cash flow from operations − Capital expenditures − Cash acquisitions − (Debt repaid − Debt issued)`.
- **Cross-check identity:** `FCFE = Dividends + Stock buybacks − Stock issuances + Change in cash balance`.
- **For banks/financial firms** (where cap ex and working capital are meaningless): reinvestment is the build-up of regulatory capital. `Tier 1 capital = Risk-adjusted assets × Tier 1 ratio`; `Investment in regulatory capital_t = Tier1_t − Tier1_(t−1)`; `Net income_t = Book equity_t × Expected ROE_t`; `FCFE_t = Net income_t − Investment in regulatory capital_t`.
- Which `DR`: use the **book** debt-to-capital ratio when computing historical FCFE, the **market** debt-to-capital ratio when forecasting.

**Procedure:**
1. Start from net income (after interest and taxes). Cleanse it the same way you cleanse EBIT if you have made R&D or lease adjustments.
2. Subtract net cap ex (including capitalized R&D and normalized acquisitions) and the change in non-cash working capital.
3. Handle debt: either forecast principal repayments and new issues explicitly, or — if leverage is stable — use the `DR` shortcut so that debt funds a constant fraction `DR` of every dollar of reinvestment.
4. Subtract preferred dividends if preferred stock exists.
5. If you are backing FCFE out of the cash-flow statement, do not trust the statement's own subtotals: build it from CFO minus cap ex minus cash acquisitions minus net debt repaid, then cross-check against dividends + buybacks − issuances + change in cash.
6. For a bank, replace steps 2–4 entirely with the regulatory-capital route: project risk-adjusted assets, apply a rising Tier 1 capital ratio, treat the increase in Tier 1 capital as the reinvestment, and project net income as book equity times an ROE path.
7. Discount at the **cost of equity**. If cash and its interest income are inside net income, the beta must be the whole-company beta (operating-asset beta weighted down by the cash holding), not the operating-asset beta.
8. Do not add cash back afterwards if its interest income is already in net income — pick one convention and stay with it.

**Reference data:**

Firms return far more cash than they generate as FCFE — the global picture ($ millions):
| Region | FCFE | Dividends | Buybacks | Dividends + Buybacks | % of firms paying dividends |
|---|---|---|---|---|---|
| Africa & Middle East | 85,659 | 114,879 | 3,083 | 117,963 | 54.64% |
| Australia & NZ | 14,445 | 31,975 | 9,846 | 41,821 | 27.63% |
| Canada | 5,499 | 36,040 | 31,425 | 67,466 | 12.41% |
| China | 50,327 | 299,196 | 19,147 | 318,342 | 73.63% |
| EU & Environs | 167,899 | 290,900 | 117,861 | 408,762 | 43.67% |
| E. Europe & Russia | 34,187 | 27,491 | 5,546 | 33,037 | 43.01% |
| India | 44,762 | 24,602 | 6,669 | 31,271 | 29.41% |
| Japan | (42,357) | 110,331 | 70,847 | 181,178 | 69.68% |
| Latin America | (13,487) | 35,631 | 5,068 | 40,700 | 60.00% |
| Small Asia | (43,076) | 116,261 | 10,655 | 126,916 | 54.69% |
| UK | 11,429 | 70,864 | 35,382 | 106,245 | 51.60% |
| United States | 290,411 | 499,570 | 700,425 | 1,199,995 | 21.95% |
| **Global** | **605,699** | **1,657,741** | **1,015,955** | **2,673,696** | **46.66%** |

FCFE rises mechanically with leverage — but so does risk. For Disney, sweeping the debt ratio from 0% to 90%:
| Debt ratio | 0% | 20% | 40% | 50% | 60% | 80% | 90% |
|---|---|---|---|---|---|---|---|
| FCFE ($m) | ~445 | ~660 | ~880 | ~990 | ~1,100 | ~1,320 | ~1,430 |
| Levered beta | ~1.09 | ~1.25 | ~1.55 | ~1.80 | ~2.15 | ~3.90 | ~7.35 |

FCFE rises roughly linearly in the debt ratio; beta rises slowly at first and then explodes. Leverage is not a free lunch: whether it raises or lowers equity value depends on the specific firm and where its current leverage sits relative to its optimal debt ratio.

**Worked example — Disney 1997 ($ millions), stable-leverage shortcut:**
Net income 1,533; capital spending 1,746; depreciation 1,134; increase in non-cash working capital 477; debt-to-capital ratio DR = 23.83%.
```
FCFE = 1,533 − (1,746 − 1,134) × (1 − 0.2383) − 477 × (1 − 0.2383)
     = 1,533 − 465.90 − 363.33
     = 704
```
Dividends actually paid were **$345m** — Disney could have paid out roughly twice what it did.

Second example — Tata Motors, aggregate 2008-09 to 2012-13 (Rs millions): net income 330,925; cap ex 592,028; depreciation 243,041; change in WC 61,397; change in debt 120,160. Equity reinvestment = 592,028 − 243,041 + 61,397 − 120,160 = **290,224**; equity reinvestment rate = 290,224/330,925 = **87.70%**; FCFE = 330,925 − 290,224 = **40,701**.

Third example — Deutsche Bank, October 2016 (bank FCFE, $ millions): Tier 1 capital rises from 55,282 to 61,834 in year 1, so investment in regulatory capital = **6,552**; projected net income = book equity × ROE = −5,111; FCFE = −5,111 − 6,552 = **−11,663**. FCFE turns positive in year 5 (+2,874) as ROE recovers.

**Determinism:**
- DETERMINISTIC: all five FCFE formulas given their inputs; the equity reinvestment rate; the cash-flow-statement reconstruction and its cross-check; the bank version given projected risk-adjusted assets, Tier 1 ratios and an ROE path; the FCFE-vs-debt-ratio sweep given the stable-leverage formula.
- JUDGMENT: whether leverage is stable enough to use the `DR` shortcut; which `DR` (book vs market, current vs target); whether reported net income is clean; for banks, the entire regulatory-capital trajectory (asset growth, target Tier 1 ratio, ROE recovery path) and any probability of equity wipeout.

**Pitfalls:**
- Discounting **earnings** as if they were potential dividends. Earnings are not cash flows (they contain non-cash items), and a firm paying out all earnings could never grow — discounting earnings overstates equity value.
- Splitting cap ex into "discretionary" and "non-discretionary" and only subtracting the latter. Once future growth is in the forecast, the reinvestment that produces it is not discretionary.
- Mixing conventions: using a net-debt-based leverage measure for the beta but a gross-debt ratio in the FCFE formula.
- Using the book debt ratio for forward-looking FCFE when the market ratio is far different (or vice versa).
- Concluding that more leverage always raises equity value because it raises FCFE — the cost of equity rises with it.
- Applying the standard FCFE formula to a bank, where cap ex and working capital have no meaning.
- Forgetting preferred dividends.

**Sources:**
- valpacket1spr21 p.117-118, p.147-157
- valpacket1spr20 p.114-115, p.144-154
- valpacket1spr21 p.213-214, p.217 / valpacket1spr20 p.209-210, p.213 (when to use FCFE)
- cfpacket2spr20 p.228, p.230, p.233-235 (FCFE menu; Deutsche Bank regulatory-capital FCFE; Tata Motors historical FCFE), p.239 (cash-adjusted beta for an FCFE discount rate), p.244, p.258-260
- spreadsheet:model.xls — FCFE formula with the debt-ratio shortcut, and the dividends-vs-FCFE comparison

**Related:** [[fcff]], [[dividends-versus-fcfe]], [[net-capital-expenditures]], [[non-cash-working-capital]], [[fundamental-growth-equity]], [[dcf-model-choice-framework]], [[equity-versus-firm-valuation]], [[dcf-case-valuations]], [[cost-of-equity]], [[levered-beta]], [[dividend-discount-model]]
