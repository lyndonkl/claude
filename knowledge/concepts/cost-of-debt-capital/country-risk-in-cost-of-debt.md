# Country risk in the cost of debt

**Core idea:** A company borrowing in an emerging market usually pays more than its own financials justify, because it sits inside a country that itself has default risk. Two separate spreads are in play: the SOVEREIGN (country) default spread and the COMPANY default spread. How you combine them depends on where the rating came from. A global-agency rating already embeds country risk, so you add only the company spread to the riskfree rate. A local-agency rating measures company risk against domestic peers only, so you must add the sovereign spread on top. And not every firm bears the full country spread: a large exporter with global revenues bears less than a small domestic firm.

**Formulas:**
- Global rating, country risk already embedded: Pre-tax cost of debt = Riskfree rate (valuation currency) + Company default spread.
- Local rating or explicit build-up: Pre-tax cost of debt = Riskfree rate + λ × Country default spread + Company default spread.
  - λ (lambda) = the fraction of country default risk the firm bears, between 0 and 1.
  - Country default spread = the sovereign's default spread for its rating, or its sovereign CDS spread net of a mature-market CDS.
  - Company default spread = the spread from the firm's own (synthetic or actual) rating.
- Riskfree rate in a local currency: if the local government bond yield itself contains sovereign default risk, strip it: Riskfree rate_local = Local government bond rate − Country default spread. Otherwise you would double count.

**Procedure:**
1. Identify the currency of the valuation and the riskfree rate in that currency.
2. Determine whether the firm's rating is from a global agency (S&P, Moody's, Fitch) or a local-scale agency (e.g. CRISIL in India).
   - Global agency → the rating already reflects country risk. Add only the company default spread. Do NOT add a sovereign spread again.
   - Local scale → the rating ranks the firm against domestic peers only. Add the sovereign spread separately.
3. Estimate the sovereign default spread for the country. Sources, in preference order: the sovereign CDS spread net of a mature-market CDS; the spread on the country's dollar-denominated bonds over US treasuries; a rating-based lookup (table below).
4. Set λ, the fraction of country risk the firm bears.
   - Small firm, all revenues domestic → λ near 1.0. Add the full sovereign spread.
   - Large firm, significant global revenues → λ below 1.0. Calibrate to traded bond spreads of other large domestic firms if available.
   - The packet's Embraer case uses λ = 2/3, calibrated to the traded bond spreads of other large Brazilian companies in 2004.
5. Add the pieces. Then apply the marginal tax rate of the country whose tax shield the firm actually gets.
6. Cross-check the synthetic rating against the actual dollar rating. A large gap in an emerging-market firm is usually country risk, not a modelling error ([[synthetic-vs-actual-rating]]).
7. If you need the answer in a different currency, convert with the differential-inflation method ([[currency-conversion-of-discount-rates]]).

**Reference data:**

**(A) Country default spreads and marginal tax rates**, from the wacccalc.xls `Country risk and taxes` lookup (January 2020 vintage; mature-market ERP 5.75%, country risk premium = default spread × 1.5). Selected rows:

| Country | Country default spread | Total ERP | Marginal tax rate | Country risk premium |
|---|---|---|---|---|
| United States | 0.00% | 5.75% | 40.00% | 0.00% |
| Germany | 0.00% | 5.75% | 29.58% | 0.00% |
| Canada | 0.00% | 5.75% | 26.50% | 0.00% |
| Australia | 0.00% | 5.75% | 30.00% | 0.00% |
| Singapore | 0.00% | 5.75% | 17.00% | 0.00% |
| Switzerland | 0.00% | 5.75% | 17.92% | 0.00% |
| United Kingdom | 0.40% | 6.35% | 21.00% | 0.60% |
| France | 0.40% | 6.35% | 33.33% | 0.60% |
| Hong Kong | 0.40% | 6.35% | 30.00% | 0.60% |
| Chile | 0.60% | 6.65% | 20.00% | 0.90% |
| China | 0.60% | 6.65% | 25.00% | 0.90% |
| Korea | 0.60% | 6.65% | 30.00% | 0.90% |
| Saudi Arabia | 0.60% | 6.65% | 20.00% | 0.90% |
| Taiwan | 0.60% | 6.65% | 17.00% | 0.90% |
| Belgium | 0.60% | 6.65% | 33.99% | 0.90% |
| Israel | 0.70% | 6.80% | 26.50% | 1.05% |
| Japan | 0.70% | 6.80% | 35.64% | 1.05% |
| Poland | 0.85% | 7.03% | 19.00% | 1.275% |
| Malaysia | 1.20% | 7.55% | 25.00% | 1.80% |
| Mexico | 1.20% | 7.55% | 30.00% | 1.80% |
| Peru | 1.20% | 7.55% | 30.00% | 1.80% |
| Ireland | 1.60% | 8.15% | 12.50% | 2.40% |
| Thailand | 1.60% | 8.15% | 20.00% | 2.40% |
| Brazil | 1.90% | 8.60% | 25.00% | 2.85% |
| Italy | 1.90% | 8.60% | 31.40% | 2.85% |
| Russia | 1.90% | 8.60% | 20.00% | 2.85% |
| South Africa | 1.90% | 8.60% | 28.00% | 2.85% |
| Spain | 1.90% | 8.60% | 30.00% | 2.85% |
| Colombia | 1.90% | 8.60% | 25.00% | 2.85% |
| Philippines | 1.90% | 8.60% | 30.00% | 2.85% |
| India | 2.20% | 9.05% | 33.99% | 3.30% |
| Indonesia | 2.20% | 9.05% | 25.00% | 3.30% |
| Turkey | 2.20% | 9.05% | 20.00% | 3.30% |
| Portugal | 2.50% | 9.50% | 23.00% | 3.75% |
| Angola | 3.00% | 10.25% | 35.00% | 4.50% |
| Nigeria | 3.60% | 11.15% | 30.00% | 5.40% |
| Bangladesh | 3.60% | 11.15% | 27.50% | 5.40% |
| Vietnam | 4.50% | 12.50% | 22.00% | 6.75% |
| Cambodia | 5.50% | 14.00% | 20.00% | 8.25% |
| Argentina | 7.50% | 17.00% | 35.00% | 11.25% |
| Egypt | 7.50% | 17.00% | 25.00% | 11.25% |
| Greece | 7.50% | 17.00% | 26.00% | 11.25% |
| Pakistan | 7.50% | 17.00% | 34.00% | 11.25% |
| Venezuela | 7.50% | 17.00% | 34.00% | 11.25% |
| Ukraine | 10.00% | 20.75% | 18.00% | 15.00% |

**(B) Sovereign rating → default spread map** (Moody's local-currency rating, from the riskchecker country table; country risk premium = spread × 1.5, mature-market ERP 5.8% in that vintage):

| Rating | Default spread |
|---|---|
| Aaa | 0.00% |
| Aa1 | 0.25% |
| Aa2 | 0.50% |
| Aa3 | 0.70% |
| A1 | 0.85% |
| A2 | 1.00% |
| A3 | 1.15% |
| Baa1 | 1.50% |
| Baa2 | 1.75% |
| Baa3 | 2.00% |
| Ba1 | 2.40% |
| Ba2 | 2.75% |
| Ba3 | 3.25% |
| B1 | 4.00% |
| B2 | 5.00% |
| B3 | 6.00% |
| Caa1 | 7.00% |
| Caa3 | 10.00% |

CDS-based alternative in the same source: Country risk premium = (Sovereign CDS spread − 0.67%) × 1.5, where 0.67% is the US CDS spread netted out so the US premium is zero.

**Worked examples:**

*Embraer, Brazil, 2004 — explicit build-up with λ.* Synthetic rating A− from a 3.56 interest coverage ratio → company default spread 1.00%. Brazil's 2004 country default spread was 6.01%. Embraer is large and sells aircraft globally, so it does not bear the full sovereign spread; λ = 2/3, calibrated to the traded bond spreads of other large Brazilian companies. Pre-tax cost of debt = 4.29% + (2/3)(6.01%) + 1.00% = 9.29%. In the cost of capital, that 9.29% is taxed at Brazil's 34% marginal rate.

*Tata Motors, India, 2013/14 — local-agency rating.* CRISIL rates Tata Motors AA− on the Indian scale, which measures company risk only. So the sovereign spread is added on top: pre-tax cost of debt = 6.57% (rupee riskfree) + 2.25% (India country default spread) + 0.70% (company spread) = 9.62%. After tax at India's 32.45% marginal rate: 9.62% × (1 − 0.3245) = 6.50%.

*Vale, Brazil — global rating, no extra addition.* S&P rates Vale A− on dollar debt, and that global rating already embeds Brazil risk. Pre-tax cost of debt = 2.75% + 1.30% = 4.05%. No sovereign spread is added a second time. Vale's synthetic rating from coverage alone was AA — the gap IS the country-risk drag, visible rather than added.

**Determinism:**
- DETERMINISTIC: sovereign rating → spread lookup; CDS spread → country risk premium; the addition Riskfree + λ × Country spread + Company spread; the after-tax conversion.
- JUDGMENT: λ, the fraction of country risk the firm bears. Estimating it needs the firm's geographic revenue breakdown, its size, whether its assets and customers are domestic, and ideally the observed bond spreads of comparable large domestic issuers.
- JUDGMENT: whether the rating in hand is a global or a local-scale rating, and therefore whether country risk is already inside it. Getting this wrong either double counts or omits several percentage points.
- JUDGMENT: whether a local-currency government bond rate is a clean riskfree rate or itself contains default risk that must be stripped.

**Pitfalls:**
- Double counting: using a global agency rating (which already reflects country risk) and then adding the sovereign spread again.
- Omitting country risk entirely for a firm rated only on a local scale.
- Applying λ = 1 mechanically to every emerging-market firm, including global exporters.
- Using a local government bond rate as a riskfree rate without checking whether it embeds sovereign default risk.
- Confusing the country DEFAULT spread (a bond-market number, used in the cost of debt) with the country RISK PREMIUM (default spread scaled by relative equity volatility, used in the cost of equity). In the tables above the premium is 1.5× the spread.
- Mismatching tax rates: using a US marginal rate against an emerging-market cost of debt.

**Sources:**
- corporate_finance--lecture_slides--cfpacket1spr20 p.187, p.190-191
- corporate_finance--lecture_slides--cfpacket1spr20 p.222, p.224 (country risk in a project's cost of capital)
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.104-105, p.111-112
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.102-103, p.108-109
- spreadsheet doc `valuation-inputs-1` — wacccalc.xls `Country risk and taxes` (country default spread, ERP, marginal tax rate, CRP) and the `Synthetic rating` sheet's country-default-spread term D12
- spreadsheet doc `corpfin-ratings-risk` — riskchecker.xls `Country Risk Premiums` (rating→spread map, CRP = spread × 1.5, CDS variant)

**Related:** [[cost-of-debt-estimation-routes]], [[synthetic-rating]], [[synthetic-vs-actual-rating]], [[default-spreads-over-time]], [[currency-conversion-of-discount-rates]], [[after-tax-cost-of-debt]], [[country-risk-premium]], [[equity-risk-premium]]
