# Betas for non-traded assets: private firms, divisions, and IPOs

**Core idea:** A regression beta needs a price history. Private firms, divisions of public companies, and pre-IPO businesses have none. Two routes remain. The first, and the one the course prefers, is the comparable-firm (bottom-up) approach: use publicly traded firms in the same business, unlever their betas, and relever at a leverage ratio you assume for the non-traded asset. The second is an accounting beta: regress changes in the firm's accounting earnings against changes in aggregate earnings. The comparable route also solves a second problem — a private firm has no market D/E ratio, so you assume the industry median market D/E. If the owner is not diversified, the market beta then needs a further adjustment (see [[total-beta]]).

**Formulas:**
- Comparable route, step 1: Unlevered beta for the company = Median levered beta of comparables / (1 + (1 − t) × Median gross D/E of comparables).
- Comparable route, step 2 (cash correction): Unlevered beta for the business = Company unlevered beta / (1 − Median Cash/Firm value).
- Comparable route, step 3: Levered beta = Business unlevered beta × (1 + (1 − t) × Assumed D/E), where the assumed D/E is the **industry median market D/E** when the firm has no market values of its own.
- Cost of equity = Riskfree rate + Levered beta × ERP.
- Accounting beta: regress % change in the firm's accounting earnings on % change in aggregate/market earnings; the slope is the accounting beta.

**Procedure:**
1. Confirm no usable price history exists. If the asset is a division of a listed parent, the parent's beta is the wrong beta unless the division is the whole company.
2. Assemble a comparable set of **publicly traded** firms in the same business. Cast the net wide enough for a meaningful sample; ten to a few hundred firms is normal.
3. Record each comparable's levered beta, marginal tax rate, gross D/E ratio, cash/firm value, and R².
4. Take **medians**, not averages. Private-firm comparable sets routinely contain firms with 500%+ D/E ratios that destroy a mean.
5. Unlever the median beta at the median D/E and tax rate; then strip out cash by dividing by (1 − median cash/firm value).
6. Choose the leverage to relever at. A private firm has only book values, so **assume the industry median market D/E ratio**. If the owner has a specific target capital structure, use that instead and say so.
7. Compute the cost of equity with the CAPM.
8. Ask who bears the risk. If the owner is undiversified, convert to a total beta — see [[total-beta]]. If the buyer is a diversified public acquirer, the market beta stands.
9. Only fall back on accounting betas if no comparables exist. Annual earnings give very few observations, so the standard errors are severe; quarterly earnings help a little.

**Reference data:**

Bookscape (a private book retailer) — comparable firms in publishing and book retailing:

| Company | Industry | Market cap ($m) | Levered beta | Marginal tax rate | Gross D/E | Cash/Firm value | R² |
|---|---|---|---|---|---|---|---|
| Red Giant Entertainment | Publishing | 2.13 | 0.69 | 40.00% | 0.00% | 0.05% | 0.1300 |
| CTM Media Holdings | Publishing | 25.20 | 1.04 | 40.00% | 17.83% | 33.68% | 0.1800 |
| Books-A-Million | Book Stores | 38.60 | 1.42 | 40.00% | 556.55% | 4.14% | 0.1900 |
| Dex Media | Publishing | 90.50 | 4.92 | 40.00% | 3190.39% | 7.86% | 0.2200 |
| Martha Stewart Living | Publishing | 187.70 | 1.11 | 40.00% | 19.89% | 15.86% | 0.3500 |
| Barnes & Noble | Book Stores | 939.30 | 0.11 | 40.00% | 164.54% | 3.22% | 0.2600 |
| Scholastic Corporation | Publishing | 953.80 | 1.08 | 40.00% | 21.41% | 1.36% | 0.2750 |
| John Wiley | Publishing | 2,931.40 | 0.81 | 40.00% | 29.58% | 5.00% | 0.3150 |
| Washington Post | Publishing | 4,833.20 | 0.68 | 40.00% | 21.04% | 16.04% | 0.2680 |
| News Corporation | Publishing | 10,280.40 | 0.49 | 40.00% | 8.73% | 24.05% | 0.2300 |
| Thomson Reuters | Publishing | 31,653.80 | 0.62 | 40.00% | 26.38% | 1.68% | 0.2680 |
| **Average** | | | **1.1796** | 40.00% | **368.76%** | **10.27%** | **0.2442** |
| **Median** | | | **0.8130** | 40.00% | **21.41%** | **5.00%** | **0.2600** |

The gap between the average beta (1.1796) and the median (0.8130) is entirely driven by Dex Media's 3190% D/E and Books-A-Million's 556%. Use the median.

Two ways to estimate betas for non-traded assets: (1) comparable firms — the bottom-up approach; (2) accounting earnings — regress changes in the firm's accounting earnings against changes in market earnings.

**Worked example (Bookscape):**
1. Median levered beta of the eleven comparables = 0.8130; median gross D/E = 21.41%; marginal tax rate 40%.
2. Company unlevered beta = 0.8130 / (1 + (1 − 0.40) × 0.2141) = **0.7205**.
3. Median cash/firm value = 5.00%, so the pure book-business unlevered beta = 0.7205 / (1 − 0.05) = **0.7584**.
4. Bookscape has no market D/E, so assume the industry median of 21.41%. Levered beta = 0.7584 × (1 + (1 − 0.40) × 0.2141) = **0.8558**.
5. With a 2.75% US T.Bond rate and a 5.5% equity risk premium: cost of equity = 2.75% + 0.8558 × 5.5% = **7.46%**.

That 7.46% is the right number for a diversified buyer. It is too low for Bookscape's undiversified owner, who bears total risk — see [[total-beta]], where the same firm's cost of equity rises to 11.98%.

**Determinism:**
- DETERMINISTIC: (comparable betas, D/E, tax rates, cash ratios) → medians → unlevered business beta; (business beta, assumed D/E, tax rate) → levered beta; (Rf, beta, ERP) → cost of equity; (earnings series) → accounting beta.
- JUDGMENT: which firms are genuine comparables; whether the industry median D/E is the right leverage assumption for this private firm; the marginal tax rate for a pass-through entity; whether the buyer is diversified; whether to use accounting betas at all.

**Pitfalls:**
- Using the **average** comparable beta when the sample contains extreme D/E ratios.
- Using the private firm's book D/E ratio to relever. Book ratios are not market ratios.
- Assuming a private firm can carry the industry median leverage when it plainly cannot borrow at industry terms.
- Forgetting that the resulting cost of equity is a *diversified-investor* number, and using it to price a sale to an undiversified individual buyer.
- Relying on annual accounting betas. Ten years of annual data gives ten observations.
- Using the listed parent's beta for a division whose business risk differs — Disney's divisional betas ranged from 0.70 to 1.22 unlevered.

**Sources:**
- corporate_finance--lecture_slides--cfpacket1spr20 p.178-181, p.183
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.95
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.93

**Related:** [[bottom-up-beta]], [[total-beta]], [[levering-and-unlevering-beta]], [[alternative-relative-risk-measures]], [[private-company-valuation]], [[cost-of-equity-assembly]]
