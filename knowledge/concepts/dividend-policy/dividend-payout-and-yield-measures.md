# Dividend payout ratio and dividend yield

**Core idea:** Two ratios summarize how much cash a firm returns as dividends. The **dividend payout ratio** scales dividends by earnings and answers "what fraction of profits is paid out?" The **dividend yield** scales dividends by price and answers "what return do I get from dividends alone?" Payout speaks to sustainability relative to earnings; yield is a component of the investor's expected return alongside price appreciation. Both are needed because they can diverge: a firm can have a high payout ratio and a low yield if it trades at a high multiple of earnings. Neither measure captures buybacks, so both understate cash returned at firms that repurchase stock.

**Formulas:**
- Dividend Payout Ratio = Dividends / Net Income. Equivalently Dividends per share / Earnings per share. Dividends = aggregate common dividends declared for the period; Net Income = earnings available to common stockholders.
- Dividend Yield = Dividends per share / Stock price. Aggregate form: Dividend Yield = Total Dividends / Market Capitalization.
- Retention Ratio = 1 − Payout Ratio (the fraction of earnings ploughed back).
- Link between the two: Dividend Yield = Payout Ratio / (Price/Earnings ratio) = Payout Ratio × (EPS / Price).
- Cash payout ratio (buyback-inclusive; see [[cash-returned-dividends-and-buybacks]]) = (Dividends + Buybacks) / Net Income.

**Procedure:**
1. Take dividends actually paid (cash flow statement "dividends paid on common stock", not declared-per-share × current share count, if buybacks changed the count mid-year).
2. Compute payout = Dividends / Net Income. Rule: if Net Income ≤ 0, the payout ratio cannot be computed — report NA rather than a negative number.
3. Compute yield = DPS / current price, or total dividends / current market cap. Use the *current* price for a forward-looking yield and the average price for a historical comparison; be explicit about which.
4. Compute both on trailing twelve months **and** on a multi-year average (Damodaran uses a 5-year window). A single year can be distorted by a special dividend or an earnings collapse.
5. Sanity-check the payout against 100%. Above 100% means dividends exceed earnings — flag it as unsustainable unless earnings are temporarily depressed. Deutsche Bank's 362.63% trailing payout in the case set is the archetype.
6. Position the firm in the cross-section using the reference distributions below, then against its own peer group ([[peer-group-payout-analysis]]) and against a fundamentals-based prediction ([[market-regression-payout-prediction]]).
7. Before concluding "pays too little", add buybacks. Dividend-only measures mis-rank US firms badly.

**Reference data (January 2020):**

*Dividend payers vs non-payers by sub-region:*

| Sub Region | Dividend Payers | Non-Payers | % Non-payers |
|---|---|---|---|
| Africa and Middle East | 1,128 | 427 | 27.46% |
| Australia & NZ | 432 | 147 | 25.39% |
| Canada | 293 | 255 | 46.53% |
| China | 3,921 | 620 | 13.65% |
| EU & Environs | 2,266 | 1,176 | 34.17% |
| Eastern Europe & Russia | 212 | 131 | 38.19% |
| India | 943 | 1,507 | 61.51% |
| Japan | 2,496 | 828 | 24.91% |
| Latin America & Caribbean | 520 | 123 | 19.13% |
| Small Asia | 4,348 | 1,565 | 26.47% |
| UK | 571 | 119 | 17.25% |
| United States | 1,693 | 1,145 | 40.35% |
| **Global** | **18,823** | **8,043** | **29.94%** |

*Distribution of payout ratios among dividend-paying firms (% of payers in each bucket):*

| Payout bucket | Global | US |
|---|---|---|
| <10% | 8.3% | 7.8% |
| 10–20% | 12.7% | 13.7% |
| 20–30% (mode) | 14.7% | 18.0% |
| 30–40% | 13.0% | 14.6% |
| 40–50% | 10.0% | 11.0% |
| 50–60% | 8.2% | 7.8% |
| 60–70% | 6.1% | 4.9% |
| 70–80% | 5.0% | 2.5% |
| 80–90% | 3.8% | 2.1% |
| 90–100% | 3.3% | 2.6% |
| >100% | 14.7% | 15.0% |

*Average dividend yields by sub-region:*

| Sub Region | Dividend Yield | Market Cap ($M) | Dividends ($M) |
|---|---|---|---|
| Africa and Middle East | 3.78% | 3,855,024 | 145,871 |
| Australia & NZ | 3.45% | 1,450,172 | 49,964 |
| Canada | 2.54% | 2,262,795 | 57,484 |
| China | 2.98% | 12,856,855 | 383,121 |
| EU & Environs | 2.65% | 13,325,629 | 352,810 |
| Eastern Europe & Russia | 5.91% | 572,241 | 33,809 |
| India | 1.29% | 2,176,461 | 28,009 |
| Japan | 2.08% | 6,162,898 | 128,485 |
| Latin America & Caribbean | 2.53% | 1,896,883 | 48,011 |
| Small Asia | 2.70% | 5,219,729 | 141,139 |
| UK | 3.01% | 3,170,789 | 95,403 |
| United States | 1.68% | 33,887,561 | 570,044 |
| **Global** | **2.34%** | **86,837,038** | **2,034,150** |

Most firms cluster at yields between 0.5% and 2.5%; roughly 7–8% of firms yield above 8% (usually a sign of a depressed price, not generosity).

*Case companies (2013 packet, trailing twelve months and 2008–2012 average):*

| Metric | Disney | Vale | Tata Motors | Baidu | Deutsche Bank |
|---|---|---|---|---|---|
| Dividend yield, LTM | 1.09% | 6.56% | 1.31% | 0.00% | 1.96% |
| Payout ratio, LTM | 21.58% | 113.45% | 16.09% | 0.00% | 362.63% |
| Dividend yield, 2008–12 | 1.17% | 4.01% | 1.82% | 0.00% | 3.14% |
| Payout ratio, 2008–12 | 17.11% | 37.69% | 15.53% | 0.00% | 37.39% |

**Worked example:** Disney, FY2013. Dividends $1,324M, net income $6,136M, market cap $134,256M. Payout = 1,324 / 6,136 = 21.58%. Yield = 1,324 / 134,256 = 0.99% (the packet's 1.09% uses a different price date). Now add buybacks of $4,087M: cash returned = $5,411M, cash payout ratio = 5,411 / 6,136 = 88.2%. The dividend payout ratio of 21.58% makes Disney look stingy; the cash payout ratio of 88.2% shows it returned almost all of its earnings.

**Determinism:**
- DETERMINISTIC: payout ratio, yield, retention ratio, cash payout ratio, and the bucket a firm falls into — from dividends, buybacks, net income, price and share count.
- JUDGMENT: which price date and which averaging window to use. Whether to normalize earnings first. Whether a payout above 100% is a temporary earnings dip or a structural problem. Whether a high yield is a value opportunity or a distressed price about to be cut.

**Pitfalls:**
- Computing payout with negative or near-zero net income. The ratio explodes or flips sign; report NA.
- Using declared dividends per share × today's share count instead of dividends actually paid.
- Confusing dividend yield with total return. Yield is one component; the ex-dividend price drop offsets it (see [[ex-dividend-day-and-dividend-capture]]).
- Ranking firms on dividend measures across regions without noting that the US returns 60% of its cash via buybacks and would rank far higher on a cash-payout basis.
- Treating the trailing-twelve-month figure as policy. Damodaran always pairs it with a 5-year average precisely because one-year numbers are noisy.

**Sources:**
- corporate_finance--lecture_slides--cfpacket2spr20 p.158-160
- corporate_finance--lecture_slides--cfpacket2spr20 p.162-163

**Related:** [[dividend-empirical-facts]], [[dividend-life-cycle]], [[cash-returned-dividends-and-buybacks]], [[peer-group-payout-analysis]], [[market-regression-payout-prediction]], [[fcfe-potential-dividends]]
