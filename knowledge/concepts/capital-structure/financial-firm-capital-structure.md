# Capital structure for banks and financial service firms

**Core idea:** The standard optimal-capital-structure machinery breaks on financial firms for three reasons. Their interest-coverage-to-spread mapping is different, so manufacturing-firm tables assign absurdly low ratings to even the safest bank. Debt is hard to define on their balance sheets, since deposits, repos and short-term funding are raw material rather than financing. And they are regulated with capital ratios stated in *book* value terms, so a "market-value optimal" debt ratio can violate a binding regulatory constraint and endanger the firm. For a bank, capital structure is therefore driven by regulatory capital requirements and by a chosen equity strategy, not by a WACC minimization. The practical question becomes: how much external equity does the bank need to support its planned asset growth and target capital ratio?

**Formulas:**
- `New equity needed = Target equity ratio × Assets (loans) after expansion − Existing equity`.
- Regulatory capital investment for a bank: `Investment in regulatory capital_t = (Capital ratio_t × Asset base_t) − (Capital ratio_{t−1} × Asset base_{t−1})`.
- `Net income_t = ROE_t × Book equity_t`.
- `FCFE (bank) = Net income − Investment in regulatory capital`. Cash is available for dividends or buybacks only if this is positive.
- If you insist on running a coverage-based analysis, define debt narrowly as long-term debt and compute coverage using only long-term interest expense.

**Procedure:**
1. Decide what counts as debt. For a financial firm, deposits and short-term funding are operating raw material. Restrict "debt" to tightly defined long-term debt if you need a debt ratio at all.
2. Use financial-sector-specific coverage-to-spread mappings, never the manufacturing table.
3. Identify the binding regulatory ratios and note that they are measured on book values. Any target capital structure must satisfy them with a buffer.
4. Choose an equity-capital strategy:
   - *Regulatory minimum*: hold the bare minimum required. Aggressive versions hunt for regulatory loopholes — businesses where required capital is set too low relative to true risk.
   - *Self-regulatory*: size equity so that potential losses from the firm's businesses can be absorbed by existing equity, independent of the regulatory minimum.
   - *Combination*: treat the regulatory ratio as a floor for established businesses and add safety buffers where the risk warrants.
5. Project the equity need. Build the asset base path, the capital ratio path, and the ROE path; derive Tier 1 capital, the annual investment in regulatory capital, and net income.
6. Compute FCFE each year. Negative FCFE means the bank must retain everything and may need to raise external equity; it certainly should not be paying dividends or buying back stock.
7. Note the four drivers of external equity need: higher growth → more; existing capitalization below target → more; weaker current earnings → more; larger current dividends → more.

**Reference data:** Deutsche Bank's projected equity path (millions of euros), showing FCFE for a bank:

| Item | Current | Yr 1 | Yr 2 | Yr 3 | Yr 4 | Yr 5 |
|---|---|---|---|---|---|---|
| Asset base | 439,851 | 453,047 | 466,638 | 480,637 | 495,056 | 509,908 |
| Capital ratio | 15.13% | 15.71% | 16.28% | 16.85% | 17.43% | 18.00% |
| Tier 1 capital | 66,561 | 71,156 | 75,967 | 81,002 | 86,271 | 91,783 |
| Change in regulatory capital | — | 4,595 | 4,811 | 5,035 | 5,269 | 5,512 |
| Book equity | 76,829 | 81,424 | 86,235 | 91,270 | 96,539 | 102,051 |
| ROE | −1.08% | 0.74% | 2.55% | 4.37% | 6.18% | 8.00% |
| Net income | −716 | 602 | 2,203 | 3,988 | 5,971 | 8,164 |
| − Investment in regulatory capital | — | 4,595 | 4,811 | 5,035 | 5,269 | 5,512 |
| **FCFE** | — | **−3,993** | **−2,608** | **−1,047** | **702** | **2,652** |

Cumulative five-year FCFE = −4,294 million euros. Even with ROE recovering from −1.08% to 8.00%, the bank generates no distributable cash, so dividends and buybacks make no sense.

**Worked example:** A simple bank. It has $100m of loans, $6m of book equity, and faces a 5% regulatory equity-capital requirement (so it is currently at 6%, above the minimum). It plans to grow loans by $50m to $150m and to raise its equity ratio to 7% of loans. Equity needed after expansion = 7% × $150m = $10.5m. Existing equity = $6.0m. New external equity required = 10.5 − 6.0 = **$4.5m**. Faster growth, a lower starting ratio, weaker earnings, or larger dividends would each raise that number.

**Determinism:**
- DETERMINISTIC: given a loan/asset base, a target capital ratio and existing equity → new equity needed; given asset base, capital ratio and ROE paths → Tier 1 capital, regulatory capital investment, net income and FCFE by year.
- JUDGMENT: which liabilities count as debt; what the financial-sector coverage-to-spread mapping should be; which capital strategy to adopt and how large a buffer to hold above the regulatory floor; the forecast paths for assets, capital ratios and ROE.

**Pitfalls:**
- Running capstru-style analysis on a bank with the manufacturing ratings table. Even the safest bank comes out badly rated with a near-zero optimal debt ratio.
- Optimizing a market-value debt ratio while ignoring book-value regulatory ratios that actually bind.
- Treating deposits as leverage in the trade-off sense.
- Paying dividends out of accounting earnings when FCFE after regulatory capital investment is negative.
- Choosing the regulatory-minimum strategy without pricing the risk it leaves uncovered.

**Sources:**
- corporate_finance--lecture_slides--cfpacket2spr20 p.79-82

**Related:** [[cost-of-capital-approach]], [[synthetic-rating-and-cost-of-debt]], [[debt-equity-tradeoff]], [[fcfe]], [[dividend-policy-framework]]
