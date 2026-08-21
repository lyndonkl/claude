# Valuing a private company for an IPO

**Core idea:** An IPO opens the business to investors who are diversified, or at least can be. So the market beta applies, not the total beta, and no illiquidity discount comes off. Two other things change with the listing: control (the firm becomes subject to monitoring by investors, analysts and the market) and disclosure (reporting obligations shift to those of a public company). On top of the ordinary DCF, three IPO-specific adjustments apply to *value*: what happens to the offering proceeds, what claims prior equity investors already hold, and how many shares the claims translate into. Get those three wrong and the per-share number is wrong even when the business valuation is right.

**Formulas:**
- `Value of equity = Value of operating assets + Cash + Retained IPO proceeds − Debt`
- `Value of equity in common stock = Value of equity − Value of options, warrants and special claims`
- `Value per share = Value of equity in common stock / Number of common shares`, where the share count includes every claim that converts to common (convertible preferred, RSUs, shares owed under acquisition agreements) but **excludes** options, which are handled by subtracting their value.
- Proceeds treatment:
  - Taken out by existing owners → add nothing.
  - Used to pay down debt → change the debt ratio, recompute the cost of capital, revalue.
  - Held as cash for future reinvestment → add the proceeds dollar for dollar.
- `Terminal value = Terminal-year FCFF / (Stable cost of capital − Stable growth)`; `Stable reinvestment rate = g / ROC`.

**Procedure:**
1. Value the business as an ordinary DCF, using **market** betas and no illiquidity discount. Build the cost of capital from bottom-up betas for the businesses the firm operates in.
2. Let the cost of capital decline over the forecast toward a stable-growth value, since the firm's risk falls as it matures.
3. Read the prospectus for the **use of proceeds**. Classify into one of the three buckets and apply the matching treatment. If proceeds are split — half withdrawn, half retained — add only the retained half.
4. Enumerate **prior equity claims**: founder shares, convertible preferred from each VC round, restricted stock units, employee options, and shares owed under acquisition agreements.
5. Determine what converts at the offering. Convertible preferred normally converts to common at the IPO and joins the share count.
6. Value the options and warrants with an option-pricing model. Subtract that value from equity **before** dividing.
7. Count shares consistently: everything that is or becomes common goes in the denominator; options stay out of the denominator and come out of the numerator instead.
8. Divide to get value per share. That is a *value*, not necessarily the offer price — see [[ipo-pricing-and-underpricing]].

**Reference data — use-of-proceeds decision table:**

| Use of proceeds | Valuation treatment |
|---|---|
| Taken out of the firm by existing owners | Ignore the proceeds entirely |
| Used to pay down debt and other obligations | Change the debt ratio; recompute the cost of capital; revalue the firm |
| Held as cash for future reinvestment needs | Add the cash proceeds to the DCF value |

**Reference data — Twitter's pre-IPO inputs (October 5, 2013):**

| Input | Value |
|---|---|
| Trailing 2013 revenues | $448.2M |
| Trailing operating income | −$92.9M (adjusted: $4.3M) |
| Invested capital | $549.1M |
| Sales/capital (trailing) | 0.82 |
| Revenue growth, years 1–5 | 55%/year, tapering to 2.7% by year 10 |
| Target pre-tax operating margin | 25% over 10 years |
| Sales-to-capital for incremental sales | 1.50 |
| Beta | 1.40 (90% advertising at 1.44 + 10% info services at 1.05) |
| Equity risk premium | 6.15% (75% US at 5.75% + 25% rest of world at 7.23%) |
| Riskfree rate | 2.7% |
| Cost of equity | 11.32% |
| After-tax cost of debt | 5.16% = (2.7% + 5.3%)(1 − 0.40) |
| Weights | E 98.31%, D 1.69% |
| Cost of capital | 11.22%, declining to 8% in years 6–10 |
| Stable growth / ROC / reinvestment rate | 2.7% / 12% / 22.5% |

**Worked example — Twitter, October 2013 ($ millions):**
- Terminal year 11: `EBIT(1−t) = 1,849`, reinvestment `416`, `FCFF = 1,433`.
- `Terminal value(10) = 1,433 / (0.08 − 0.027) = 27,036`.
- Forecast path: year 1 revenues 694.7 with FCFF −141.0; year 5 revenues 4,010.0 with FCFF −584.4; year 10 revenues 11,164.6 with FCFF 1,604.6.
- Bridge: operating assets 9,611 + cash 375 + **IPO proceeds 1,000** − debt 207 = **equity 10,779**.
- Claims on that equity: seven classes of convertible preferred (converting at the offering), 86 million RSUs, 44.16 million employee options (strike $1.82, stated life 6.94 years, maturity used 3.47 years), and 14.791 million shares owed to MoPub stockholders. Common shares excluding RSUs and options: 472.61 million. Share count used: **574.44 million** (all claims except options).
- `Value of equity in common stock = 10,779 − 805 = 9,974`; `9,974 / 574.44 = **$17.36 per share**`.
- The $1,000M of proceeds was added because the prospectus stated the money would stay in the company for future investment. Had the owners planned to withdraw half, only $500M would have been added.

**Determinism:**
- DETERMINISTIC: the whole DCF chain given the assumptions — `{revenue growth path, margin path, sales-to-capital, cost of capital path, terminal inputs} → FCFF → PV → operating assets`. Then `{operating assets, cash, retained proceeds, debt, option value, share count} → value per share`. The use-of-proceeds adjustment is deterministic once the bucket is known.
- JUDGMENT: growth, margin and sales-to-capital assumptions; the beta blend and ERP blend; the cost-of-capital glide path; the option-pricing inputs (notably the maturity, set at half the stated life); and which claims belong in the share count. That judgment needs the prospectus, the cap table, comparable-sector betas, and a narrative for the revenue and margin path.

**Pitfalls:**
- Using a total beta or an illiquidity discount in an IPO valuation. The buyers are diversified and the shares will trade.
- Adding IPO proceeds that the existing owners are taking out. That money never reaches the business.
- Counting options in the share denominator *and* subtracting their value from the numerator. Do one or the other; the packet subtracts value and excludes them from the count.
- Forgetting convertible preferred converts at the offering. Leaving those shares out of the count inflates value per share badly.
- Ignoring RSUs and shares owed under acquisition agreements. Twitter's count rises from 472.61M to 574.44M once they are included — a 22% dilution that moves per-share value by the same proportion.
- Using the stated option life instead of an expected life. The packet uses 3.47 years against a stated 6.94.
- Holding the cost of capital constant for a young company. Twitter's declines from 11.22% to 8%.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket2spr21 p.128, p.154-160
- valuations--lecture_notes--spring_2020--valpacket2spr20 p.126, p.152-158

**Related:** [[ipo-pricing-and-underpricing]], [[private-company-valuation-framework]], [[vc-stage-varying-cost-of-equity]], [[private-to-public-sale]], [[total-beta]], [[employee-options-valuation]], [[young-company-valuation]], [[terminal-value]]
