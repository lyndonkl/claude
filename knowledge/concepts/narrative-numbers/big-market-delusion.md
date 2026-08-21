# The big market delusion

**Core idea:** Every company chasing a huge market can be individually defensible and collectively impossible. Venture investors fund many entrepreneurs going after the same big market. Each one is priced on the potential of that market. Add up what all their valuations imply about future revenue, and the total exceeds any plausible size for the market itself. This is the *implausible* class of narrative failure, and it is invisible from inside a single valuation. You only see it by aggregating across the sector. The test is simple arithmetic: impute the revenue each company's price requires, sum across the sector, and compare with a credible forecast of the whole market.

**Formulas:**
- Breakeven revenues in year N = the revenue level a company must reach in year N to justify its current enterprise value, given plausible margins, reinvestment and cost of capital. Solve the DCF backwards for revenue.
- Imputed sector revenue for company i = Breakeven revenues_i × (% of company i's revenue that comes from the sector).
- Aggregate implied sector revenue = Σ_i Imputed sector revenue_i.
- Delusion test: Aggregate implied sector revenue > Credible forecast of total sector revenue in year N. If it is, the sector is collectively overpriced, however sound each individual story looks.
- The same test in share form: Σ_i implied market share_i must be ≤ 100%.

**Procedure:**
1. **Define the market precisely.** Online advertising, food delivery, ride hailing. Vague market definitions defeat the test.
2. **List every company competing for it,** listed and private, domestic and foreign. Excluding the foreign players understates the total badly.
3. **For each company, impute breakeven revenues** in a common future year. Work backwards from enterprise value through the same DCF you would run forwards.
4. **Multiply by the share of revenue that comes from this market** to get the imputed sector revenue for that company.
5. **Sum across all companies.**
6. **Compare with an independent forecast of total market size** in that year, ideally a third-party one you did not construct.
7. **If the sum exceeds the market, act on the sector, not the name.** The implication is that the sector is collectively overpriced, so reduce exposure across it rather than picking the one you like.
8. **Sanity-check your own single-company model the same way.** Translate your growth rate into year-10 dollar revenues and divide by market size. See [[narrative-consistency-checks]].

**Reference data:** Online advertising, circa 2015. All money figures in $ millions. Breakeven 2025 revenues imputed from enterprise value; imputed online-ad revenue is that figure times the share of revenue from online advertising.

| Company | Market cap | Enterprise value | Current revenues | Breakeven revenues (2025) | % from online advertising | Imputed online ad revenue (2025) |
|---|---|---|---|---|---|---|
| Google | 441,572.00 | 386,954.00 | 69,611.00 | 224,923.20 | 89.50% | 201,306.26 |
| Facebook | 245,662.00 | 234,696.00 | 14,640.00 | 129,375.54 | 92.20% | 119,284.25 |
| Yahoo! | 30,614.00 | 23,836.10 | 4,871.00 | 25,413.13 | 100.00% | 25,413.13 |
| LinkedIn | 23,265.00 | 20,904.00 | 2,561.00 | 22,371.44 | 80.30% | 17,964.26 |
| Twitter | 16,927.90 | 14,912.90 | 1,779.00 | 23,128.68 | 89.50% | 20,700.17 |
| Pandora | 3,643.00 | 3,271.00 | 1,024.00 | 2,915.67 | 79.50% | 2,317.96 |
| Yelp | 1,765.00 | 0.00 | 465.00 | 1,144.26 | 93.60% | 1,071.02 |
| Zillow | 4,496.00 | 4,101.00 | 480.00 | 4,156.21 | 18.00% | 748.12 |
| Zynga | 2,241.00 | 1,142.00 | 752.00 | 757.86 | 22.10% | 167.49 |
| **Total US** | 770,185.90 | 689,817.00 | 96,183.00 | 434,185.98 | | **388,972.66** |
| Alibaba | 184,362.00 | 173,871.00 | 12,598.00 | 111,414.06 | 60.00% | 66,848.43 |
| Tencent | 154,366.00 | 151,554.00 | 13,969.00 | 63,730.36 | 10.50% | 6,691.69 |
| Baidu | 49,991.00 | 44,864.00 | 9,172.00 | 30,999.49 | 98.90% | 30,658.50 |
| Sohu.com | 18,240.00 | 17,411.00 | 1,857.00 | 16,973.01 | 53.70% | 9,114.51 |
| Naver | 13,699.00 | 12,686.00 | 2,755.00 | 12,139.34 | 76.60% | 9,298.74 |
| Yandex | 3,454.00 | 3,449.00 | 972.00 | 2,082.52 | 98.80% | 2,057.52 |
| Yahoo! Japan | 23,188.00 | 18,988.00 | 3,591.00 | 5,707.61 | 69.40% | 3,961.08 |
| Sina | 2,113.00 | 746.00 | 808.00 | 505.09 | 48.90% | 246.99 |
| Netease | 14,566.00 | 11,257.00 | 2,388.00 | 840.00 | 11.90% | 3,013.71 |
| Mail.ru | 3,492.00 | 3,768.00 | 636.00 | 1,676.47 | 35.00% | 586.76 |
| Mixi | 3,095.00 | 2,661.00 | 1,229.00 | 777.02 | 96.00% | 745.94 |
| Kakaku | 3,565.00 | 3,358.00 | 404.00 | 1,650.49 | 11.60% | 191.46 |
| **Total non-US** | 474,131.00 | 444,613.00 | 50,379.00 | 248,495.46 | | **133,415.32** |
| **Global total** | 1,244,316.90 | 1,134,430.00 | 146,562.00 | 682,681.44 | | **522,387.98** |

Aggregate imputed 2025 online advertising revenue: about $522 billion, against current (2015) revenues of $146.6 billion across the same set. That total sits far above any reasonable forecast of the online advertising market, even though every single company's story was defensible on its own.

**Worked example:** Read the table above as the worked example. Google alone needs $224.9 billion of 2025 revenues to justify a $387 billion enterprise value, of which $201.3 billion must come from online advertising. Facebook needs $119.3 billion from the same pot. Those two alone require $320 billion. Add Alibaba's $66.8 billion, Baidu's $30.7 billion, Yahoo!'s $25.4 billion and Twitter's $20.7 billion, and you are at $464 billion before the remaining fifteen companies. The individual valuations are not obviously silly. The sum is.

**Determinism:**
- DETERMINISTIC: the multiplication and summation. Given breakeven revenues and the sector share of revenue, imputed sector revenue and the aggregate follow exactly.
- JUDGMENT: imputing breakeven revenues, which requires an assumed margin, reinvestment level and cost of capital for each company. Also the market definition, the company list, and the credible total-market forecast you compare against.

**Pitfalls:**
- Running the test on the domestic players only. The 2015 example needed the non-US names to see the full $522 billion.
- Using each company's own bullish margin assumptions when imputing breakeven revenue, which understates the required revenue and hides the delusion.
- Concluding that the biggest player is safe. In a big market delusion the whole sector is priced on the same double-counted pot.
- Confusing the big market delusion with a bubble in general. This one is specific and measurable: implied revenues exceed the market.
- Justifying a single company's growth with a macro market story and never doing the aggregation. That is exactly the route into the delusion.

**Sources:**
- valpacket1spr21 p.267
- valpacket1spr20 p.263
- valuationmotleyfool p.16 (proposition: macro stories used to justify high growth lead to a big market delusion)

**Related:** [[narrative-consistency-checks]], [[possible-plausible-probable]], [[runaway-stories]], [[value-vs-price-gap]], [[narrative-scenario-grids]]
