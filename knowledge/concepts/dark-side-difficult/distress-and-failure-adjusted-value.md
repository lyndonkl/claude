# Distress- and failure-adjusted value

**Core idea:** A discounted cash flow model values a firm as a going concern. It implicitly assumes the firm lives long enough to reach stable growth. If there is a real chance the firm dies first — and its assets would then fetch less than the present value of expected cash flows — the DCF overstates value. The repair is not a higher discount rate. It is an explicit probability-weighted blend of two outcomes: the going-concern value and the distress-sale value. This single formula covers startup failure, bankruptcy of a levered retailer, a government bailout that wipes out equity, a bank that breaches its capital ratio, and nationalization of a foreign asset.

**Formulas:**
- Firm level: `Value of operating assets = (PV of FCFF + PV of terminal value) × (1 − P(failure)) + Distress proceeds × P(failure)`.
- Equity level: `Value of equity = DCF value of equity × (1 − P(distress)) + Distress sale value of equity × P(distress)`.
- Distress proceeds, two conventions (both in the Ginzu model as a "B" or "V" switch):
  - Book basis: `Proceeds = (Book value of equity + Book value of debt) × recovery %`.
  - Fair-value basis: `Proceeds = (Going-concern DCF value) × recovery %`.
  Default recovery in the model is **50%**.
- Equity in distress is a residual: if `Proceeds < Face value of debt`, the distress value of equity is **zero**.
- Partial wipeout (used when the firm survives but equity holders are diluted or expropriated): `Adjusted value = DCF value × (1 − P(failure) × Loss fraction to equity)`. Boeing: 20% failure probability × 50% equity loss = a 10% haircut on operating assets.
- Cumulative from annual probability: `P(distress over n years) = 1 − (1 − p_annual)^n`.

**Procedure:**
1. Ask whether survival is genuinely in doubt. Triggers: high financial leverage, negative or marginal operating income, a business in decline, a young company with no revenues, a bank near its regulatory minimum, or an asset exposed to expropriation.
2. Estimate the probability of distress. Three routes, in increasing order of information content:
   - **Bond rating.** Use the historical cumulative default rate over 10 years for that rating. Las Vegas Sands was B+ in February 2009, and 28.25% of B+ bonds historically defaulted within 10 years.
   - **Probit / statistical model** fitted on firm characteristics.
   - **Back it out of the market price of the firm's bonds** — the most informative, and usually the most pessimistic. See [[bond-implied-distress-probability]].
   For young companies with no debt to price, use **sector survival statistics** instead (tables below).
3. Estimate the distress-sale value. Best practice is a percentage of book value, and that percentage falls when the economy is weak or when peers in the same business are also distressed (forced sellers, no buyers).
4. Check whether equity gets anything at all. Compare expected proceeds with the face value of debt; if proceeds are lower, equity is worth zero in that branch.
5. Blend with the formula above. Report both branch values and the probability alongside the blended number.
6. Do **not** also raise the discount rate for failure risk, and do not shrink the cash flows for it. Pick one channel — the probability weight.

**Reference data (1):** Startup survival by year after founding, all firms (2007 study, read from the chart). Roughly 81–86% of startups survive year 1 across sectors; by year 7 the range is about 25–45%.

| Year after founding | Survival, all firms |
|---|---|
| 1 | ~81% |
| 2 | ~66% |
| 3 | ~54% |
| 4 | ~44% |
| 5 | ~38% |
| 6 | ~34% |
| 7 | ~31% |

Highest 7-year survival: health services ~44%. Lowest: information ~25%.

**Reference data (2):** Long-run survival by sector, the most recent edition — US Bureau of Labor Statistics, Business Employment Dynamics, 1994–2019 cohorts (share of businesses started in 1994 still alive in 2019).

| Sector | Long-run survival rate |
|---|---|
| Management of companies and enterprises | 35.2% |
| Utilities | 28.4% |
| Health care and social assistance | 19.9% |
| Wholesale trade | 14.0% |
| Transportation and warehousing | 12.9% |
| Information | 11.5% |
| All-sector average | 16.6% |

**Reference data (3):** Failure adjustments actually used in the packet's valuations.

| Company | P(failure or distress) | Source of the probability | Distress value assumption | Effect |
|---|---|---|---|---|
| JC Penney | 20% | Bond rating | 50% of book value = $2,421m | $4,841m → $4,357m operating assets |
| Las Vegas Sands (Feb 2009) | 76.66% cumulative over 10 years | Traded bond price (13.54%/yr) | Proceeds $2,769m < face value of debt, so equity = $0 | $8.12 → $1.92 per share |
| Boeing (Mar 2020) | 20% failure, 50% equity loss | Judgment: too big to fail outright, but a bailout could wipe equity as with GM in 2009 | $10,788m deduction (10% of $107,883m) | Value per share $138.77 |
| Deutsche Bank (Oct 2016) | 10% equity wipeout | Judgment on a crisis bank | Equity worth zero in that branch | $22.97 → $20.67 per share |
| Amazon (2019, 2020) | 0% | No meaningful failure risk | — | No adjustment |
| Saudi Aramco | 20% regime change | Political judgment | Regime-change DCF $0.825T (not zero) | $1.65T → $1.485T |

**Worked example:** JC Penney. The going-concern DCF gives PV of ten years of cash flows $2,362m plus PV of terminal value $2,479m = $4,841m. The bond rating implies a 20% chance of failure. Liquidation would recover 50% of book value, i.e. $2,421m. Value of operating assets = 4,841 × 0.80 + 2,421 × 0.20 = **$4,357m**. Second example, Boeing March 2020: DCF operating assets $107,883m; a 20% failure probability with 50% loss to equity gives a $10,788m deduction; then − debt and minority interests $28,580m + cash and other non-operating assets $10,030m = equity $78,545m; ÷ 566 shares = **$138.77 per share** versus a $127.68 price.

**Determinism:** DETERMINISTIC — (going-concern value, P(failure), distress proceeds) → blended value; (book equity, book debt, recovery %) → proceeds on the book basis; (annual probability, horizon) → cumulative probability. JUDGMENT: the probability itself when it is not read off a bond price (needs rating tables, sector survival data, leverage and coverage), the recovery percentage (needs comparable liquidation and bankruptcy recoveries, plus the state of the economy and of peers), and whether equity retains any claim in the distress branch.

**Pitfalls:**
- Raising the discount rate to "reflect" failure risk and then also probability-weighting the value. That double counts.
- Applying the going-concern DCF alone to a levered firm in a declining business.
- Assuming equity keeps a positive value in distress when the expected proceeds sit below the face value of debt.
- Using an optimistic recovery percentage in an economy-wide downturn, when everyone in the sector is selling the same assets at once.
- Using the average corporate default rate rather than a sector-specific or firm-specific probability; survival differs enormously by sector, from 11.5% to 35.2% over the long run.
- Forgetting that a bailout can save the *firm* while destroying the *equity* — the failure probability that matters to a shareholder is the probability of equity wipeout, not of liquidation.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.305-306
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.321-323
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.325
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.296-297
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.312-314
- spreadsheet model doc: ginzu-fcff-corona.md — Input sheet B47–B50, Valuation output rows 22–24

**Related:** [[bond-implied-distress-probability]], [[declining-firm-valuation]], [[young-company-valuation]], [[truncation-and-political-risk]], [[bank-fcfe-and-excess-return-models]], [[difficult-company-taxonomy]], [[synthetic-rating]], [[default-spread]]
