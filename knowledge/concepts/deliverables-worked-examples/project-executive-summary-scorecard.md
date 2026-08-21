# Executive summary scorecard (the one-page project output)

**Core idea:** A complete corporate finance analysis produces dozens of tables, and the deliverable opens with one page that compresses all of them. The scorecard puts every company in a column and every headline metric in a row, so the cross-company comparison is immediate. Each row is the single number that answers one section of the project: governance power, risk, performance versus the market, return quality, financing, cash return, and value. It is the natural output template for an automated analysis system, because every cell traces back to a specific deterministic computation described elsewhere.

**Formulas:** No new formulas. Each row is a headline output from another section:

| Row | Source | Meaning |
|---|---|---|
| Power | Governance analysis | Shareholder power score, higher is better |
| Approach | Risk section | Beta method used; B = bottom-up |
| Beta | Cost of capital build-up | Levered beta at market values |
| Jensen's alpha | Regression diagnostics | Intercept − Rf(1 − beta) |
| R² | Regression diagnostics | Share of return variance explained by the market |
| ROE − COE | Return spreads | Equity excess return |
| ROC − WACC | Return spreads | Capital excess return |
| EVA | Return spreads | (ROC − WACC) × capital invested |
| Current debt ratio | Cost of capital build-up | D/(D+E) at market values |
| Optimal debt ratio | WACC schedule | argmin of the cost-of-capital grid |
| Change in WACC | Recapitalisation analysis | WACC_new − WACC_old |
| Change in value | Recapitalisation analysis | % gain in firm value at the optimum |
| Dividends | Dividend policy | Cash returned via dividends |
| FCFE | Dividend framework | Cash that could have been returned |
| Value/share | DCF valuation | Intrinsic value per share |
| Price/share | Market | Traded price for comparison |

**Procedure:**
1. Put one column per company and one row per headline metric, in the order the project sections run.
2. Populate each cell from the finished section, not from a separate calculation. The scorecard reports; it does not compute.
3. Include both the estimate and its benchmark wherever the comparison is the point — current versus optimal debt ratio, value per share versus price per share, ROE versus cost of equity.
4. Read the scorecard across rows to find the outlier company for each question, then down columns to build each company's story.
5. Write the summary paragraph from the pattern, not company by company. State which firms create value, which are under-levered, and which look mispriced.
6. Flag internal tensions. A firm with a negative return spread that is also below its optimal debt ratio faces two different problems, and the recommendations must not conflict.

**Reference data:** Spring 2015 food-industry executive summary.

| Item | Starbucks | McDonald's | Chipotle | Tyson |
|---|---|---|---|---|
| Power | 2 | 2 | 0 | 1 |
| Approach | B | B | B | B |
| Beta | 0.85 | 0.97 | 0.73 | 1.09 |
| Jensen's alpha | 1.11% | −1.25% | 36.95% | −0.32% |
| R² | 23.50% | 23.50% | 4.40% | 7.80% |
| ROE − COE | 30.32% | 27.44% | 15.67% | 0.24% |
| ROC − WACC | 15.58% | 13.92% | 15.64% | −0.77% |
| EVA ($m) | 1,409 | 3,587 | 333 | −128 |
| Current debt ratio | 11.92% | 34.99% | 2.45% | 35.54% |
| Optimal debt ratio | 40% | 50% | 30% | 60% |
| Change in WACC | −0.43% | −0.41% | −0.39% | −0.51% |
| Change in value | 21.71% | 15.64% | 9.49% | 18.59% |
| Dividends ($m) | 826 | 6,180 | 0 | −2,004 |
| FCFE ($m) | 863 | 2,111 | 429 | 6,320 |
| Value/share | $42.57 | $97.96 | $408.50 | $53.43 |
| Price/share | $49.78 | $98.23 | $633.82 | $49.78 |

**Worked example:** Reading the 2015 scorecard across rows produces the whole summary in four sentences. Three of the four firms earn large positive return spreads; Tyson is roughly break-even on capital at −0.77% and destroys a small amount of value with an EVA of −$128m. All four sit below their optimal debt ratio, and moving to the optimum would cut WACC by 39-51 bps and raise firm value by 9.5-21.7%. On dividends the four span the full life-cycle range, from Chipotle at zero to McDonald's at $6,180m, with Tyson negative because of a net equity issue. On value, McDonald's is fairly priced at $97.96 against $98.23, Starbucks and especially Chipotle trade well above the DCF estimate, and Tyson trades slightly below it.

**Determinism:** DETERMINISTIC — every cell except one, since each is a completed output from an earlier section. Assembling the table, computing each gap (current versus optimal, value versus price), and flagging outliers are all mechanical. JUDGMENT — only the Power score, which compresses a qualitative governance assessment into a single integer, and the choice of which rows belong on the page. The narrative paragraph written from the table is also judgment, though the raw comparisons that feed it are not.

**Pitfalls:**
- Recomputing values in the summary rather than pulling them from the sections. Discrepancies between summary and body destroy the reader's trust. Note that the 2015 summary lists Tyson's price as $49.78, identical to Starbucks', while the valuation section shows the same figure — an inconsistency worth checking in any reproduction.
- Mixing market-value and book-value versions of the same metric across rows without labelling which is which.
- Omitting the benchmark. "Optimal debt ratio 40%" means nothing without the current 11.92% beside it.
- Compressing governance to a score without the underlying verdict available in the body. The Power score is the most judgment-laden number on the page.
- Presenting the scorecard as the analysis. It is an index into the analysis, and every cell needs its section behind it.

**Sources:**
- corporate_finance--project--food2015 p.1-2
- corporate_finance--project--cfproj p.1

**Related:** [[corporate-finance-project-blueprint]], [[governance-analysis-deliverable]], [[regression-performance-diagnostics]], [[cost-of-capital-buildup-deliverable]], [[return-spread-and-eva-analysis]], [[optimal-debt-ratio-wacc-schedule]], [[recapitalization-value-and-stress-test]], [[dividend-policy-deliverable]], [[two-stage-fcff-company-valuation]], [[valuation-triangulation-and-recommendation]]
