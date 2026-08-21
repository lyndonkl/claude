# Descriptive tests: distributions of multiples and why averages mislead

**Core idea:** Multiples are bounded at zero on the left and unbounded on the right. Their cross-sectional distributions are therefore heavily right-skewed, and the mean sits far above the median. In January 2021 the average US trailing PE was 103.25 against a median of 20.30. Samples are also truncated: a multiple cannot be computed for money-losing firms, so PE samples silently drop them (only about a third of US firms had a usable PE in Jan 2021). Any comparison point must come from the current distribution — medians and percentiles — not from means, memory, or rules of thumb. Distributions also move across time and geography, so a fixed threshold flips meaning.

**Formulas:** Standard summary statistics (median, percentiles). No closed forms beyond that.

**Procedure:**
1. Pull the multiple for every firm in the universe (market or sector), not just estimable ones. Record how many firms drop out and why (negative earnings, negative book value, etc.).
2. Compute median, 10th/25th/75th/90th percentiles, and the mean. Expect mean >> median.
3. Use the median (or a percentile band) as "typical." Do not use the mean.
4. Handle outliers carefully. Outliers lie almost entirely on the positive side. Trimming them biases the estimate downward; capping or using percentiles is safer.
5. Check sample bias from dropped firms. If 60-80% of a market has no PE (Canada ~82% without positive earnings in Jan 2021), PE-based conclusions describe a biased subsample.
6. Locate your firm's multiple in the current distribution before calling it high or low. Re-check by region: the same number can be cheap in the US and expensive in Japan.
7. Track the distribution over time; thresholds decay. 6x EBITDA was near the middle of the US distribution in January 2010 (mode bucket 4-6x). By January 2021 the US median EV/EBITDA was 16.6, so 6x had become genuinely cheap — yet in Japan (median 8.46) it was near normal.

**Reference data (January 2021 unless noted):**

US PE summary statistics, Jan 2021 (7,584 firms):

| Statistic | Current PE | Trailing PE | Forward PE |
|---|---|---|---|
| Firms with PE | 2,780 | 2,481 | 2,354 |
| Average | 109.79 | 103.25 | 79.74 |
| Median | 18.15 | 20.30 | 18.89 |
| 10th pct | 6.95 | 7.68 | 8.96 |
| 25th pct | 10.41 | 11.50 | 12.36 |
| 75th pct | 37.26 | 40.79 | 33.20 |
| 90th pct | 95.44 | 96.80 | 69.40 |
| Maximum | 36,157 | 25,020 | 42,390 |

Trailing PE by region, Jan 2021 (percentiles; % of firms with PE > 0):

| Region | 10th | 25th | Median | 75th/90th | % PE>0 |
|---|---|---|---|---|---|
| Africa & Middle East | 4.84 | 8.50 | 29.27 | 64.75 | 59.7% |
| Australia & NZ | 8.13 | 14.51 | 52.33 | 120.43 | 31.0% |
| Canada | 3.32 | 9.08 | 37.35 | 138.65 | 18.3% |
| China | 7.15 | 14.79 | 60.85 | 118.27 | 67.4% |
| EU & Environs | 6.83 | 11.93 | 43.38 | 107.75 | 55.3% |
| E. Europe & Russia | 2.99 | 6.68 | 21.62 | 51.87 | 61.4% |
| India | 5.10 | 9.66 | 41.29 | 97.73 | 57.2% |
| Japan | 7.76 | 11.04 | 33.18 | 75.12 | 74.6% |
| Latin America | 6.58 | 10.66 | 32.45 | 74.42 | 60.7% |
| Small Asia | 6.85 | 11.13 | 36.33 | 87.26 | 61.0% |
| UK | 8.98 | 14.99 | 50.71 | 98.91 | 44.0% |
| United States | 7.68 | 11.50 | 40.79 | 96.80 | 32.4% |
| Global | 6.71 | 11.28 | 42.41 | 96.73 | 53.2% |

EV/EBITDA medians by region, start of 2021: US 16.60; EU 14.44; China 21.15; Japan 8.46; E. Europe & Russia 8.07; India 12.95; Australia & NZ 16.29; Canada 12.44; UK 15.16; Latin America 11.13; Africa & ME 11.51; Small Asia 12.74.

Price-to-book medians, global, Jan 2013 (illustrating cross-market gaps): US 1.54; Europe 1.22; Japan 0.67; Aus/NZ/Canada 1.21; Emerging Markets 1.18; Global 1.16. Japan's discount raises the analytical question: cheap, or justified by low ROE?

Industry-level current reference: the January-2022 US industry-averages dataset (tables.md) gives, per industry, EV/Sales, EV/EBITDA, EV/EBIT, Price/Book, Trailing PE, plus margins, betas, ROC/ROE, payout, and reinvestment measures. Use it as the sector distribution snapshot.

**Worked example:** The private-equity rule "buy below 6x EBITDA" in January 2010: the modal US EV/EBITDA bucket was 4-6x with heavy mass at 2-4x, so 6x was not cheap. In January 2021 the US median was 16.6x, so the same 6x was well below the 10th percentile — cheap. Same rule, opposite verdicts, purely because the distribution moved.

**Determinism:** DETERMINISTIC: all summary statistics from firm-level data; locating a firm's percentile. JUDGMENT: how to treat outliers and missing-multiple firms, and what the bias implies for conclusions.

**Pitfalls:**
- Using the average of a skewed multiple; it is nearly meaningless.
- One-sided outlier trimming, which biases the "typical" multiple down.
- Ignoring firms where the multiple is inestimable — survivorship of profitable firms biases the sample.
- Applying absolute thresholds ("cheap below 6x") without checking the current, local distribution.

**Sources:**
- valpacket2spr21 p.13-19
- valpacket2spr20 p.13-19
- tables (Jan-2022 US industry averages: multiples columns)

**Related:** [[four-step-multiple-framework]], [[multiple-definition-tests]], [[sector-regressions]], [[market-pe-vs-bond-alternative]]
