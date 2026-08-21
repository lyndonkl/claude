# Cost of debt: choosing an estimation route

**Core idea:** The cost of debt is the rate at which the firm can borrow TODAY, long term. It is not the coupon on old bonds, not the accounting interest rate (interest expense / book debt), and not the historical average borrowing cost. Two things drive it: the firm's default risk and the current level of market interest rates. Damodaran gives a decision tree with four routes, ranked by data quality. The route you pick changes only how you get the default spread; the final structure is always riskfree rate plus spread. One hard constraint runs through all of it: the cost of debt must be in the same currency as the cost of equity and the cash flows.

**Formulas:**
- Pre-tax cost of debt = Riskfree rate (in the valuation currency, long-term government bond) + Default spread for the firm's rating.
- Pre-tax cost of debt (traded-bond route) = Yield to maturity on a long-term, liquid, STRAIGHT bond of the firm.
- After-tax cost of debt = Pre-tax cost of debt × (1 − marginal tax rate). See [[after-tax-cost-of-debt]].
- Accounting cost of debt (WRONG, shown for contrast) = Interest expense / Book value of debt.

Symbols: "straight bond" = no conversion feature, no put/call, no floating rate, no other embedded option. Riskfree rate must match the cash-flow currency.

**Procedure:**
1. Ask: does the firm have long-term straight bonds that trade liquidly and widely?
   - Yes → use the yield to maturity on the longest such straight bond. Stop.
   - No → step 2. (This is the usual case: very few firms have liquid long-term straight bonds.)
2. Ask: is the firm rated by a global agency (S&P, Moody's, Fitch)?
   - Yes → take the rating. If different bonds of the firm carry different ratings, use the MEDIAN rating. Look the rating's default spread up in the current spread table (see [[default-spreads-over-time]]). Pre-tax cost of debt = riskfree rate + that spread. Go to step 5.
   - No, or conflicting ratings → step 3.
3. Unrated firm, alternative A: use the interest rate on a RECENT long-term bank borrowing by the firm. Recency matters; a loan struck years ago carries a stale rate level and a stale credit view.
4. Unrated firm, alternative B (the general route): estimate a synthetic rating from the interest coverage ratio and read the spread off the table. See [[synthetic-rating]]. This is the route Damodaran defaults to, because it works for private firms, divisions, and any firm without bonds.
5. If the rating comes from a LOCAL agency that scores only company risk relative to other domestic firms (e.g. CRISIL in India), the sovereign default spread is not embedded in that rating. Add it. See [[country-risk-in-cost-of-debt]].
6. Sanity-check the answer. If the firm has traded debt, compare with the observed yield. If the firm is rated, compare the synthetic rating with the actual rating and explain any gap. See [[synthetic-vs-actual-rating]].
7. Apply the marginal tax rate to get the after-tax cost of debt for the WACC.
8. If the valuation currency differs from the currency in which you built the rate, convert it. See [[currency-conversion-of-discount-rates]].

**Reference data:** Route selection table.

| Situation | Route | Inputs needed |
|---|---|---|
| Liquid long-term straight bond outstanding | Yield to maturity on that bond | Bond price, coupon, maturity |
| Rated, no liquid bond | Rating → default spread | Median rating, current spread table, riskfree rate |
| Unrated, recent bank loan | Loan rate | Loan documentation, loan date |
| Unrated, no recent loan; private firm; division | Synthetic rating | EBIT, interest expense, firm size class, spread table, riskfree rate |
| Bank or financial-service firm | Do NOT synthesize from ordinary coverage; use actual rating, or the long-term-interest-only coverage table | Actual rating; or long-term interest expense |
| Local-agency rating (company risk only) | Riskfree + country default spread + company spread | Local rating, sovereign spread |

Illustrative worked rates from the corporate finance packet (2013/14 data, riskfree rates by currency):

| Company | Rating source | Rating | Riskfree rate | Default spread | Pre-tax cost of debt |
|---|---|---|---|---|---|
| Disney | Actual S&P | A | 2.75% (US$) | 1.00% | 3.75% |
| Deutsche Bank | Actual S&P | A | 1.75% (Euro) | 1.00% | 2.75% |
| Vale | Actual S&P | A− | 2.75% (US$) | 1.30% | 4.05% |
| Bookscape (private) | Synthetic (coverage 5.16, small-firm table) | A− | 2.75% (US$) | 1.30% | 4.05% |
| Tata Motors | CRISIL local AA− plus India sovereign | AA− + country | 6.57% (Rupee) | 2.25% country + 0.70% company | 9.62% |

**Worked example:** Bookscape is a private US book retailer with no rating and no traded debt, so routes 1-3 are unavailable. Its EBIT is $2,536 and interest expense $492, giving an interest coverage ratio of 5.16. It is small (market value under $5 billion), so the small-cap/risky column applies: coverage 5.16 falls in the 4.5-6 bracket → synthetic rating A−, default spread 1.30% (November 2013 table). Pre-tax cost of debt = 2.75% + 1.30% = 4.05%. At a 40% marginal tax rate the after-tax cost of debt is 4.05% × 0.60 = 2.43%.

**Determinism:**
- DETERMINISTIC: rating → spread lookup; riskfree + spread → pre-tax cost of debt; pre-tax × (1 − t) → after-tax cost of debt; YTM from bond price, coupon and maturity; the synthetic-rating table lookup once coverage and size class are set.
- JUDGMENT: which route applies. That needs the firm's bond inventory (are the bonds straight and liquid?), its rating status (how many ratings, how dispersed), the age of any bank loan, and whether the firm is a financial-service firm. Also judgment: whether a local rating already embeds sovereign risk.

**Pitfalls:**
- Using the accounting cost of debt (interest expense / book debt). It reflects old borrowings at old rates and old credit quality.
- Using a bond with embedded options (convertible, callable, floating) — its yield is contaminated by the option value, not just default risk.
- Using a short-maturity bond's yield when the valuation horizon is long.
- Taking the lowest of multiple ratings, or the highest. Use the median.
- Estimating a synthetic rating for a bank. Defining "interest expense on debt" for a bank is not meaningful in the ordinary way; deposits are raw material, not just financing.
- Mismatching currency: a rupee cash flow discounted at a dollar-built cost of debt.
- Forgetting that the spread table itself moves year to year and must be refreshed.

**Sources:**
- corporate_finance--lecture_slides--cfpacket1spr20 p.184, p.186-187, p.191, p.193
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.101, p.115
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.99, p.112
- spreadsheet doc `valuation-inputs-1` — wacccalc.xls, cost-of-debt approach dropdown {Direct input, Synthetic rating, Actual rating} and the rating→spread list
- spreadsheet doc `corpfin-ratings-risk` — ratings.xls purpose and structure

**Related:** [[synthetic-rating]], [[synthetic-vs-actual-rating]], [[default-spreads-over-time]], [[country-risk-in-cost-of-debt]], [[after-tax-cost-of-debt]], [[interest-coverage-ratio]], [[currency-conversion-of-discount-rates]], [[cost-of-capital-assembly]], [[riskfree-rate]]
