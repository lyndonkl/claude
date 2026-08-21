# Country risk premium and country equity risk premiums

**Core idea:** Equity in a risky country should command a higher premium than equity in a mature market. The country risk premium (CRP) is that extra premium, and the country's total ERP is the mature-market premium plus the CRP. Three methods exist. The simplest sets the CRP equal to the sovereign default spread. The second scales the US premium by the relative volatility of the country's equity market. The third — Damodaran's default, the "melded" approach — scales the sovereign default spread up by the ratio of equity-market volatility to bond-market volatility, on the logic that ratings measure default risk, and equity is riskier than debt. Country risk premiums are dynamic and must be re-estimated, not treated as constants.

**Formulas:**
- Total ERP for a country = Mature market premium + Country risk premium.
- Method 1 (raw default spread): CRP = Country default spread.
- Method 2 (relative equity volatility): Total ERP = ERP_US × (σ_country equity / σ_US equity); CRP = Total ERP − ERP_US.
- Method 3 (melded, the default): CRP = Country default spread × (σ_country equity / σ_country bond).
- Damodaran's production form: **ERP_country = ERP_US + Default spread × Relative Equity Market Volatility**, where Relative Equity Market Volatility = σ(emerging-market equity index) / σ(emerging-market bond index). This multiplier was **1.10 in January 2021** (1.18 in January 2020) and is applied uniformly to all countries rather than country by country.
- Implied-cost-of-equity cross-check for a market: Cost of equity = (ROE − g)/PBV + g, where PBV = price-to-book ratio and g = growth rate tied to the US T.Bond rate.

Symbols: σ = annualized standard deviation; ERP_US = the mature-market premium, taken as the implied ERP for the S&P 500; "default spread" = the sovereign's local-currency-rating-based or market-based spread (see [[currency-riskfree-rate]]).

**Procedure (Damodaran's four-step template, January 1, 2021 vintage):**
1. **Estimate the mature market premium.** Use the implied ERP for the S&P 500 — **4.72%** on 1/1/2021 (5.20% on 1/1/2020). Update monthly.
2. **Measure country risk.** Take the Moody's **local-currency** sovereign rating. If Moody's does not rate the country, convert the S&P rating to its Moody's equivalent. If there is no sovereign rating at all, use the PRS (Political Risk Services) composite country risk score.
3. **Convert country risk into a premium.**
   - Rating is Aaa/AAA → CRP = 0 and ERP_country = ERP_US. Stop.
   - Rating below Aaa → get a default spread from one of three sources: the sovereign's US$ bond spread, its CDS spread net of the US CDS, or the ratings table. Then multiply that spread by the relative equity market volatility multiplier (1.10 in Jan 2021).
   - No rating → map the PRS score to an ERP directly.
4. **ERP_country = ERP_US + scaled default spread.** Update the country step every six months (January and July).
5. Apply the country ERP to a *company* using one of the exposure approaches in [[operation-weighted-erp]] and [[lambda-country-risk-exposure]] — do not automatically stamp the country-of-incorporation CRP on every firm.
6. Re-estimate over time. Brazil's CRP shrank in the mid-2000s boom, spiked in 2015-16 (total ERP near 11%), and settled near 3.5% CRP / ~8.5% total by September 2018.

**Reference data:**

Country risk premiums and total ERPs, January 2021 (mature-market ERP = 4.72%; format: Moody's rating | CRP | total ERP):

*Regional weighted averages:* Western Europe 0.84% / 5.56%; North America 0.00% / 4.72%; Caribbean 5.31% / 10.03%; Latin America 3.99% / 8.71%; Eastern Europe & Russia 2.08% / 6.80%; Middle East 1.53% / 6.25%; Africa 4.94% / 9.66%; Australia & NZ 0.00% / 4.72%.

*Western Europe:* Andorra Caa1 7.26% 11.98%; Austria Aa1 0.38% 5.10%; Belgium Aa3 0.59% 5.31%; Cyprus Ba2 2.91% 7.63%; Denmark Aaa 0.00% 4.72%; Finland Aa1 0.38% 5.10%; France Aa2 0.48% 5.20%; Germany Aaa 0.00% 4.72%; Greece Ba3 3.49% 8.21%; Iceland A2 0.82% 5.54%; Ireland A2 0.82% 5.54%; Italy Baa3 2.13% 6.85%; Luxembourg Aaa 0.00% 4.72%; Malta A2 0.82% 5.54%; Netherlands Aaa 0.00% 4.72%; Norway Aaa 0.00% 4.72%; Portugal Baa3 2.13% 6.85%; Spain Baa1 1.55% 6.27%; Sweden Aaa 0.00% 4.72%; Switzerland Aaa 0.00% 4.72%; Turkey B2 5.33% 10.05%; UK Aa3 0.59% 5.31%.

*North America:* Canada Aaa 0.00% 4.72%; United States Aaa 0.00% 4.72%.

*Latin America:* Argentina Ca 11.62% 16.34%; Bolivia B2 5.33% 10.05%; Brazil Ba2 2.91% 7.63%; Chile A1 0.68% 5.40%; Colombia Baa2 1.84% 6.56%; Costa Rica B2 5.33% 10.05%; Ecuador Caa3 9.68% 14.40%; El Salvador B3 6.30% 11.02%; Guatemala Ba1 2.42% 7.14%; Honduras B1 4.36% 9.08%; Mexico Baa1 1.55% 6.27%; Nicaragua B3 6.30% 11.02%; Panama Baa1 1.55% 6.27%; Paraguay Ba1 2.42% 7.14%; Peru A3 1.16% 5.88%; Uruguay B1 4.36% 9.08%; Venezuela C 19.18% 23.90%.

*Eastern Europe & Russia:* Bulgaria Baa1 1.55% 6.27%; Croatia Ba1 2.42% 7.14%; Czech Republic Aa3 0.59% 5.31%; Estonia A1 0.68% 5.40%; Hungary Baa3 2.13% 6.85%; Kazakhstan Baa3 2.13% 6.85%; Latvia A3 1.16% 5.88%; Lithuania A3 1.16% 5.88%; Poland A2 0.82% 5.54%; Romania Baa3 2.13% 6.85%; Russia Baa3 2.13% 6.85%; Serbia Ba3 3.49% 8.21%; Slovakia A2 0.82% 5.54%; Slovenia A3 1.16% 5.88%; Ukraine B3 6.30% 11.02%; Uzbekistan Baa2 1.84% 6.56%; Belarus B3 6.30% 11.02%; Armenia Ba3 3.49% 8.21%; Azerbaijan Ba2 2.91% 7.63%; Georgia Ba2 2.91% 7.63%.

*Middle East:* Abu Dhabi Aa2 0.48% 5.20%; Bahrain B2 5.33% 10.05%; Iraq Caa1 7.26% 11.98%; Israel A1 0.68% 5.40%; Jordan B1 4.36% 9.08%; Kuwait A1 0.68% 5.40%; Lebanon C 19.18% 23.90%; Oman Ba3 3.49% 8.21%; Qatar Aa3 0.59% 5.31%; Saudi Arabia A1 0.68% 5.40%; Sharjah Baa2 1.84% 6.56%; UAE Aa2 0.48% 5.20%.

*Africa:* Angola Caa1 7.26% 11.98%; Botswana A2 0.82% 5.54%; Cameroon B2 5.33% 10.05%; Côte d'Ivoire Ba3 3.49% 8.21%; Egypt B2 5.33% 10.05%; Ethiopia B2 5.33% 10.05%; Gabon Caa1 7.26% 11.98%; Ghana B3 6.30% 11.02%; Kenya B2 5.33% 10.05%; Morocco Ba1 2.42% 7.14%; Mozambique Caa2 8.72% 13.44%; Namibia Ba3 3.49% 8.21%; Nigeria B2 5.33% 10.05%; Rwanda B2 5.33% 10.05%; Senegal Ba3 3.49% 8.21%; South Africa Ba2 2.91% 7.63%; Tanzania B2 5.33% 10.05%; Tunisia B2 5.33% 10.05%; Uganda B2 5.33% 10.05%; Zambia Ca 11.62% 16.34%.

*Asia & Oceania:* Australia Aaa 0.00% 4.72%; Bangladesh Ba3 3.49% 8.21%; China A1 0.68% 5.40%; Hong Kong Aa3 0.59% 5.31%; India Baa3 2.13% 6.85%; Indonesia Baa2 1.84% 6.56%; Japan A1 0.68% 5.40%; Korea Aa2 0.48% 5.20%; Malaysia A3 1.16% 5.88%; Mauritius Baa1 1.55% 6.27%; Mongolia B3 6.30% 11.02%; New Zealand Aaa 0.00% 4.72%; Pakistan B3 6.30% 11.02%; Philippines Baa2 1.84% 6.56%; Singapore Aaa 0.00% 4.72%; Sri Lanka Caa1 7.26% 11.98%; Taiwan Aa3 0.59% 5.31%; Thailand Baa1 1.55% 6.27%; Vietnam Ba3 3.49% 8.21%; Cambodia B2 5.33% 10.05%; Laos Caa2 8.72% 13.44%.

*Unrated countries, from PRS composite risk score (score | CRP | ERP):* Algeria 57.25 8.72% 13.44%; Brunei 80 0.82% 5.54%; Gambia 63.75 6.30% 11.02%; Guinea 53.5 11.62% 16.34%; Guyana 65.75 5.33% 10.05%; Haiti 52.75 11.62% 16.34%; Iran 59.25 8.72% 13.44%; North Korea 50.75 11.62% 16.34%; Liberia 53.5 11.62% 16.34%; Libya 58.25 8.72% 13.44%; Madagascar 63.25 6.30% 11.02%; Malawi 58.75 8.72% 13.44%; Myanmar 63.75 6.30% 11.02%; Sierra Leone 58.75 8.72% 13.44%; Somalia 50.5 11.62% 16.34%; Sudan 38.25 19.18% 23.90%; Syria 47 19.18% 23.90%; Yemen 50 19.18% 23.90%; Zimbabwe 52.25 11.62% 16.34%.

(A January 2020 edition of this table exists on a 5.20% mature premium — e.g. Brazil 8.16% / 2.96%, India 7.08% / 1.88%, China 5.89% / 0.69%. A November 2013 edition sits on a 5.50% mature premium — Brazil 8.50% / 3.00%, India 9.10% / 3.60%, China 6.94% / 1.44%. Use the 2021 numbers unless replicating an older case.)

Emerging-versus-developed cost-of-equity differential, backed out from PBV and ROE (start of year): 2004 developed 7.28% vs emerging 10.55%, differential 3.27%; 2009 7.35% vs 8.91%, 1.56%; 2014 5.99% vs 7.61%, 1.62%; 2019 8.22% vs 9.42%, **1.19%**. Emerging-market risk as priced has converged toward developed-market risk, but has not disappeared.

**Worked example (Brazil, January 2021):** Mature-market premium 4.72%. Brazil's Moody's local-currency rating is Ba2 → table default spread 2.65%.
- Method 1 (raw spread): CRP = 2.65%, Total ERP = 4.72% + 2.65% = 7.37%.
- Method 2 (relative equity volatility): σ(Bovespa) = 30%, σ(S&P 500) = 18% → Total ERP = 4.72% × (30/18) = 7.89%, CRP = 3.17%.
- Method 3 (melded, country-specific volatilities): σ(equity) = 30%, σ(Brazil government bond) = 20% → CRP = 2.65% × (30/20) = 3.98%, Total ERP = 8.70%.
- Production version (uniform 1.10 multiplier): CRP = 2.65% × 1.10 = **2.91%**, Total ERP = **7.63%** — the value in the January 2021 lookup table.

**Determinism:**
- DETERMINISTIC: (mature ERP, default spread, volatility ratio) → CRP and total ERP; (country name, date) → table lookup; (PBV, ROE, growth) → implied cost of equity by market.
- JUDGMENT: which of the three methods to use; which default-spread source to take; whether the uniform 1.10 multiplier or country-specific volatilities are appropriate; converting S&P ratings to Moody's equivalents; mapping PRS scores to ERPs; whether a rating is stale relative to conditions on the ground.

**Pitfalls:**
- Using the **foreign-currency** sovereign rating instead of the local-currency rating.
- Double-counting: stripping the default spread out of the riskfree rate and *also* leaving country risk in the cash flows, or adding it again through both beta and the ERP.
- Setting the CRP equal to the raw default spread and calling it done. Equity is riskier than sovereign debt, which is why the spread gets scaled up.
- Treating the country ERP as a constant across years. It is dynamic on both components — the US ERP itself ranged from ~2.5% (2000) to ~7.7% (2011).
- Stamping the country-of-incorporation CRP on a company with mostly developed-market operations — see [[operation-weighted-erp]].
- Mixing editions: applying a 2013 country ERP table (5.50% mature premium) alongside a 2021 riskfree rate.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.49-53, p.79-80, p.99
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.49-53, p.77-78, p.97
- corporate_finance--lecture_slides--cfpacket1spr20 p.118, p.120-123, p.129-130

**Related:** [[currency-riskfree-rate]], [[implied-equity-risk-premium]], [[operation-weighted-erp]], [[lambda-country-risk-exposure]], [[cost-of-equity-assembly]], [[country-risk-in-cost-of-debt]]
