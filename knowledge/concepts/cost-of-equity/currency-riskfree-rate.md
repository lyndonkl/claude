# Riskfree rate in any currency (default-spread removal and build-up)

**Core idea:** Most currencies have no default-free issuer. The observed local-currency government bond rate then equals a riskfree component plus a sovereign default spread, and you must strip the spread out before using it as a riskfree rate. The sovereign default spread can be estimated three ways — from the sovereign's own US$/Euro-denominated bond, from its traded CDS spread, or from a ratings-based table — which give a range, not a point. When even the local government bond rate is untrustworthy or missing, you can build a riskfree rate up from expected inflation plus a real rate, scale the US$ riskfree rate by differential inflation, do the analysis in real terms, or simply switch the valuation to a currency that has a riskfree rate. Differences in riskfree rates across currencies are driven primarily by differences in **expected inflation**, not by risk.

**Formulas:**
- Riskfree rate in currency C = Government bond rate in currency C − Sovereign default spread of that government in its local currency.
- Default spread (Approach 1, hard-currency bond) = Sovereign's US$-denominated bond rate − US Treasury bond rate of the same maturity. For Euro-denominated sovereign bonds: − the Euro riskfree (German) rate.
- Default spread (Approach 2, CDS) = Sovereign 10-year CDS spread − US CDS spread ("net of US", which forces the US spread to zero).
- Default spread (Approach 3, rating) = table lookup on the sovereign's **local-currency** Moody's/S&P rating.
- Build-up: Riskfree rate = Expected inflation in that currency + Expected real interest rate.
- Differential inflation: Riskfree rate_C = (1 + Riskfree rate_US$) × (1 + Expected inflation_C) / (1 + Expected inflation_US$) − 1.
- Fallback real rate when no indexed bond exists: Real riskfree rate ≈ long-term real growth rate of the economy.

Symbols: Expected inflation_C = expected inflation in the local currency; Expected inflation_US$ = expected US inflation; "same maturity" means matching the tenor of the hard-currency sovereign bond to the Treasury.

**Procedure:**
1. Pull the **10-year local-currency government bond rate** for the currency (table below).
2. Get the government's **local-currency** sovereign rating from Moody's (convert S&P to the Moody's equivalent if only S&P is available). Aaa/AAA → default spread is zero and the bond rate *is* the riskfree rate; stop.
3. Otherwise estimate the sovereign default spread by all three routes where data exists:
   a. US$-denominated sovereign bond spread over the equivalent Treasury (market-based, but the bond may be illiquid);
   b. sovereign CDS spread net of the US CDS spread (market-based, updates daily, but carries CDS-market frictions);
   c. rating-based typical spread from the table below (always available, but stale and lumpy).
   Prefer a market measure when one exists; fall back to the ratings table otherwise.
4. Subtract the chosen spread from the local bond rate. Report the range across the three routes; the spread between them is genuine estimation uncertainty.
5. **If there is no trustworthy local government bond rate at all**, choose one of:
   - Build-up: expected inflation in that currency + expected real interest rate (a TIPS yield is a usable real-rate proxy).
   - Differential inflation: scale the US$ riskfree rate by the inflation ratio (formula above).
   - Forward exchange rates: back the local riskless rate out of forward FX rates plus the riskless rate in an index currency (US$ or Euro) via covered interest parity.
   - Switch to real terms and use an inflation-indexed bond yield, or approximate the real riskfree rate with long-term real economic growth.
   - Switch the whole valuation into US$ or Euros. (Legitimate — but then *every* input, including growth and margins, must be restated in that currency.)
6. Whatever route you take, keep the rest of the valuation internally consistent: a 15%-inflation currency riskfree rate demands cash flows that grow with 15% inflation.

**Reference data:**

Typical sovereign default spreads by rating, January 2021 (use with the sovereign's **local-currency** rating):

| S&P | Moody's | Default spread | S&P | Moody's | Default spread |
|---|---|---|---|---|---|
| AAA | Aaa | 0.00% | BB+ | Ba1 | 2.21% |
| AA+ | Aa1 | 0.35% | BB | Ba2 | 2.65% |
| AA | Aa2 | 0.44% | BB− | Ba3 | 3.18% |
| AA− | Aa3 | 0.53% | B+ | B1 | 3.98% |
| A+ | A1 | 0.62% | B | B2 | 4.86% |
| A | A2 | 0.75% | B− | B3 | 5.75% |
| A− | A3 | 1.06% | CCC+ | Caa1 | 6.63% |
| BBB+ | Baa1 | 1.41% | CCC | Caa2 | 7.96% |
| BBB | Baa2 | 1.68% | CCC− | Caa3 | 8.83% |
| BBB− | Baa3 | 1.95% | CC+ | Ca1 | 10.60% |
| | | | CC | Ca2 | 13.76% |
| | | | CC− | Ca3 | 15.00% |
| | | | C+ | C1 | 16.00% |
| | | | C | C2 | 17.50% |
| | | | C− | C3 | 20.00% |

(January 2020 edition, for reference: Aa1 0.33%, Aa2 0.41%, Aa3 0.51%, A1 0.59%, A2 0.71%, A3 1.00%, Baa1 1.34%, Baa2 1.59%, Baa3 1.84%, Ba1 2.09%, Ba2 2.51%, Ba3 3.01%, B1 3.76%, B2 4.60%, B3 5.44%, Caa1 6.27%, Caa2 7.53%, Caa3 8.36%, Ca1 10.03%, Ca2 13.25%, Ca3 15.00%, C1 18.00%, C2 21.00%, C3 24.00%.)

10-year local-currency government bond rates, 12/31/2020:

| Currency | Rate | Currency | Rate | Currency | Rate |
|---|---|---|---|---|---|
| Australian $ | 1.05% | Indian Rupee | 5.92% | Qatari Dinar | 1.69% |
| Brazilian Real | 7.02% | Indonesian Rupiah | 6.24% | Romanian Lev | 3.50% |
| British Pound | 0.82% | Israeli Shekel | 0.86% | Russian Ruble | 5.82% |
| Bulgarian Lev | 0.40% | Japanese Yen | 0.02% | Singapore $ | 0.92% |
| Canadian $ | 0.77% | Kenyan Shilling | 11.90% | South African Rand | 8.94% |
| Chilean Peso | 2.79% | Korean Won | 1.65% | Swedish Krona | 0.01% |
| Chinese Yuan | 3.35% | Malaysian Ringgit | 2.78% | Swiss Franc | −0.53% |
| Colombian Peso | 4.95% | Mexican Peso | 5.53% | Taiwanese $ | 0.29% |
| Croatian Kuna | 0.85% | Nigerian Naira | 7.27% | Thai Baht | 1.27% |
| Czech Koruna | 1.29% | Norwegian Krone | 0.89% | Turkish Lira | 12.99% |
| Danish Krone | −0.47% | NZ $ | 0.98% | US $ | 0.93% |
| Euro | −0.58% | Pakistani Rupee | 9.90% | Vietnamese Dong | 2.55% |
| HK $ | 0.72% | Peruvian Sol | 4.55% | Zambian kwacha | 34.00% |
| Hungarian Forint | 2.30% | Philippine Peso | 2.94% | | |
| Iceland Krona | 3.08% | Polish Zloty | 1.37% | | |

Sovereign US$-bond default spreads, January 2021 (Approach 1; US riskfree 0.93%):

| Country | $ bond rate | Riskfree | Default spread |
|---|---|---|---|
| Peru | 3.66% | 0.93% | 2.73% |
| Brazil | 2.98% | 0.93% | 2.05% |
| Colombia | 1.93% | 0.93% | 1.00% |
| Poland | 1.33% | 0.93% | 0.40% |
| Turkey | 6.12% | 0.93% | 5.19% |
| Mexico | 2.21% | 0.93% | 1.28% |
| Russia | 2.43% | 0.93% | 1.50% |
| Bulgaria (Euro bond) | 1.00% | −0.58% | 1.58% |

Selected sovereign 10-year CDS spreads, 1/1/2021, raw and net of the US CDS (Approach 2): Brazil 2.15% / 1.92%; India 1.24% / 1.01%; Mexico 1.45% / 1.22%; China 0.56% / 0.33%; Italy 1.43% / 1.20%; Turkey — see table source; Germany 0.23% / 0.00%; Japan 0.28% / 0.05%; Indonesia 1.28% / 1.05%; Egypt 4.08% / 3.85%; Nigeria 3.59% / 3.36%; Ecuador 10.36% / 10.13%; Angola 7.50% / 7.27%; South Africa (2020 edition) 2.48% / 2.30%.

**Worked example (Brazil, January 1, 2021):** The 10-year nominal Brazilian real government bond yields **7.02%**. Three spread estimates:
- Approach 1 — the 2030 Brazil US$ bond trades 2.05% over Treasuries → R$ riskfree = 7.02% − 2.05% = **4.97%**.
- Approach 2 — Brazil CDS 2.15% less the US CDS 0.23% = 1.92% → 7.02% − 1.92% = **5.10%**.
- Approach 3 — Moody's local-currency rating Ba2 → table spread 2.65% → 7.02% − 2.65% = **4.47%**.
So the reais riskfree rate is roughly 4.5%–5.1%; pick one and stay consistent. (Same exercise a year earlier: 6.77% bond rate, spreads 1.71% / 1.56% / 2.51%, giving 5.06% / 5.21% / 4.26%.)

**Worked example (no trustworthy bond rate):** Expected inflation 15%, TIPS real rate 1% → build-up riskfree rate = **16%**. Or with US$ riskfree 2.00%, foreign inflation 15%, US inflation 1.5%: (1.02)(1.15)/(1.015) − 1 = **15.57%**. India, January 1 2021: 10-year rupee bond 5.92%, Baa3 rating → spread 1.95% → rupee riskfree = **3.97%**.

**Determinism:**
- DETERMINISTIC: (local bond rate, chosen default spread) → riskfree rate; (rating) → spread by table lookup; (CDS, US CDS) → net spread; ($ bond rate, Treasury rate) → spread; (US$ riskfree, two inflation rates) → local riskfree; (inflation, real rate) → riskfree.
- JUDGMENT: which of the three spread routes to trust; whether the sovereign rating reflects local-currency or foreign-currency risk; the expected-inflation forecasts in the build-up/differential-inflation routes; whether to abandon the local currency entirely; the "real riskfree ≈ real growth" approximation.

**Pitfalls:**
- Using the **foreign-currency** sovereign rating when the valuation is in local currency — the local-currency rating is the right one, and it is often a notch or two higher.
- Adding the default spread instead of subtracting it (the government bond rate already contains it).
- Double-counting country risk: subtracting the spread from the riskfree rate *and* then also building a country risk premium off a rate that still contains it. Strip once, then handle country equity risk in the ERP.
- Treating the three spread estimates as interchangeable within one valuation — pick one and use it consistently across the riskfree rate and the country risk premium.
- Using a US$ riskfree rate with local-currency cash flows because "the local rate looks weird".
- Forgetting that a high local riskfree rate is mostly high expected inflation, which must also show up in nominal growth and margins.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.31-37, p.39-41
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.31-37, p.39-41
- corporate_finance--lecture_slides--cfpacket1spr20 p.104-107

**Related:** [[riskfree-rate-fundamentals]], [[riskfree-rate-normalization]], [[country-risk-premium]], [[cost-of-equity-assembly]], [[synthetic-rating]], [[currency-consistency-in-valuation]]
