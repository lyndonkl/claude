# Stockholder analysis and the marginal investor

**Core idea:** Part II of the corporate finance project profiles who owns the firm and, more importantly, who *sets its price*. The marginal investor is the investor most likely to be trading the stock. That identity decides whether risk should be measured from a diversified perspective. If the marginal investor is a large, well-diversified institution, only market risk matters, and CAPM with a market beta is the right hurdle-rate model. If the marginal investor is an undiversified insider or founder family, total risk matters and CAPM understates the cost of equity. The whole risk-and-return section that follows rests on this one call.

**Formulas:**
- % of shares held by institutional investors = Institutional shares / Shares outstanding.
- % of *float* held by institutional investors = Institutional shares / Float, where Float = shares outstanding − closely held shares. This can exceed 100% when reported institutional holdings overlap or when the float definition lags reported positions.
- % of shares held by insiders = Insider-held shares / Shares outstanding.

**Procedure:**
1. Break the shareholder base into three buckets: insiders, individuals, institutional investors.
2. Compute institutional holdings as a share of both total shares and float, plus insider holdings as a share of total shares.
3. Apply the decision rule. High institutional share of float → the marginal investor is a diversified institution → CAPM is applicable and a market beta is the right risk measure.
4. If insiders hold a large block and institutions a small one, flag the marginal investor as undiversified. The cost of equity must then reflect total risk, not just market risk.
5. Also record the insider stake as an input to later sections. Low insider ownership supports carrying above-industry-average leverage; a large family stake is a governance mitigant and a debt-discipline argument.
6. Carry the conclusion forward as an explicit assumption into the cost of equity ([[cost-of-capital-buildup-deliverable]]) and into the debt-discipline argument ([[qualitative-debt-tradeoff]]).

**Reference data:** Spring 2015 food-industry ownership.

| Ownership | SBUX | MCD | CMG | TSN |
|---|---|---|---|---|
| % shares held by institutional investors | 78.09% | 68.91% | 92% | 98.48% |
| % float held by institutional investors | 80.24% | 100% | 107.77% | 68.94% |
| % shares held by insiders | 2.67% | 0.05% | 1.75% | 1.14% |
| Institutional holdings, industry average | 48.46% | 58.06% | 58.06% | 50.80% |

Published data sets for this part: insider holdings by industry; institutional holdings by industry.

**Worked example:** All four 2015 food companies show institutional investors dominating the float — 80.24% at Starbucks, 100% at McDonald's, 107.77% at Chipotle (an artifact of the float definition), 68.94% at Tyson. Insider holdings are tiny everywhere, from 0.05% at McDonald's to 2.67% at Starbucks. Conclusion: the marginal investor at every one of the four is a diversified institution, so the CAPM assumption holds and market betas are appropriate risk measures. The same numbers reappear in Part V: institutional holdings far above industry average mean debt's disciplinary role is less needed, because diversified institutions can already discipline management.

**Determinism:** DETERMINISTIC — the three-bucket ownership breakdown and all three percentages, straight from 13F/insider filings and share-count data. Applying a fixed threshold (say, institutional float share above some cutoff) is also mechanical. JUDGMENT — the actual identification of the marginal investor, which needs trading-volume patterns, block-holder identity, whether large "institutional" holders are index funds or concentrated activists, and whether a founder family trades at all. A high institutional percentage that consists of one entrenched strategic holder is not the same as a broad institutional base.

**Pitfalls:**
- Reading float percentages above 100% as an error rather than as an artifact of overlapping reporting and float definitions.
- Assuming institutional ownership automatically means diversified ownership. A controlling stake held through a partnership (Tyson Limited Partnership) is an undiversified holder even when it is nominally institutional.
- Confusing the *largest* investor with the *marginal* investor. The marginal investor is the one trading at the margin and setting price, not the one holding the most shares.
- Skipping this section and defaulting to CAPM silently. The project asks for the assumption to be stated and defended.

**Sources:**
- corporate_finance--project--cfproj p.5
- corporate_finance--project--food2015 p.6, p.10

**Related:** [[corporate-finance-project-blueprint]], [[cost-of-capital-buildup-deliverable]], [[governance-analysis-deliverable]], [[qualitative-debt-tradeoff]]
