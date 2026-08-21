# Sector regressions: statistical control within a peer group

**Core idea:** When peer firms differ on more than one fundamental, regress the multiple on those fundamentals across the sector. The fitted line defines what "normal" looks like given a firm's own characteristics. Then compare the firm's actual multiple with its predicted multiple. This converts a vague eyeball comparison into a number: percent over or under the sector's own pricing rule. It also kills the naive screen. Telebras had one of the lowest PEs in global telecom and was still slightly *over*valued once growth and country risk were controlled for. The regression is only as good as its inputs, though: sector fits drift year to year, and R² can collapse when the sector's story changes.

**Formulas:**
- Generic form: `Multiple = a + b₁ × Fundamental₁ + b₂ × Fundamental₂ + …`
- Comparison: `Under/Over valuation (%) = Actual multiple / Predicted multiple − 1`
- Negative percentage → trades below the sector's own pricing rule (relatively cheap). Positive → relatively expensive.

Choose the fundamentals from the intrinsic derivation of the multiple ([[intrinsic-multiple-derivation]]): PE on growth and risk; PBV on ROE and risk; PS or EV/Sales on margin; EV/EBITDA on reinvestment, tax rate, debt ratio.

**Procedure:**
1. Assemble the peer set and, for each firm, the multiple plus its companion variables.
2. Drop or flag firms where the multiple is not computable (negative earnings, negative EBITDA) and note the resulting bias.
3. Regress the multiple on the fundamentals. Keep the specification small; a 15-30 firm sector cannot support many variables.
4. Check the t-statistics. Above 2 is good, 1 to 2 is marginal, below 1 is noise. Drop insignificant variables and re-run.
5. Check R². A weak fit means the sector is not priced on those fundamentals — say so rather than pushing the prediction.
6. Plug each firm's fundamentals into the equation to get a predicted multiple.
7. Compute the over/under percentage and rank the sector.
8. Before acting, ask what the regression omits. A firm above the line may have an unmodelled advantage; a firm below may have an unmodelled problem.
9. Re-estimate every period. The coefficients move, sometimes violently.

**Reference data:**

**Telecom PE regression** (25 global telecom ADRs; dependent variable PE):
`Predicted PE = 13.1151 + 121.223 × Growth − 13.8531 × Emerging Market dummy`

| Variable | Coefficient | SE | t-ratio | Probability |
|---|---|---|---|---|
| Constant | 13.1151 | 3.471 | 3.78 | 0.0010 |
| Growth rate | 121.223 | 19.27 | 6.29 | ≤0.0001 |
| Emerging Market | −13.8531 | 3.606 | −3.84 | 0.0009 |

R² = 66.2%, adjusted 63.1%. Growth as a decimal; dummy = 1 for emerging-market firms.

Sample (PE and expected growth):

| Company | PE | Growth | Company | PE | Growth |
|---|---|---|---|---|---|
| PT Indosat ADR | 7.8 | 6.0% | Gilat Communications | 22.7 | 31% |
| Telebras ADR | 8.9 | 7.5% | Deutsche Telekom ADR | 24.6 | 11% |
| Telecom New Zealand ADR | 11.2 | 11% | British Telecom ADR | 25.7 | 7% |
| Telecom Argentina ADR B | 12.5 | 8% | Tele Danmark ADR | 27.0 | 9% |
| Hellenic Telecom ADR | 12.8 | 12% | Telekomunikasi Indonesia ADR | 28.4 | 32% |
| Telecom de Chile ADR | 16.6 | 8% | Cable & Wireless ADR | 29.8 | 14% |
| Swisscom ADR | 18.3 | 11% | APT Satellite ADR | 31.0 | 33% |
| Asia Satellite ADR | 19.6 | 16% | Telefonica ADR | 32.5 | 18% |
| Portugal Telecom ADR | 20.8 | 13% | Royal KPN ADR | 35.7 | 13% |
| Telefonos de Mexico ADR L | 21.1 | 14% | Telecom Italia ADR | 42.2 | 14% |
| Matav RT ADR | 21.5 | 22% | Nippon Telegraph ADR | 44.3 | 20% |
| Telstra ADR | 21.7 | 12% | France Telecom ADR | 45.2 | 19% |
| | | | Korea Telecom ADR | 71.3 | 44% |

**European bank PBV regression** (18 banks, 2010):
`Predicted PBV = 2.27 + 3.63 × ROE − 2.68 × Std deviation` (both as decimals). t-statistics: constant 5.56, ROE 3.32, std dev 2.33. R² = 79%.

Predicted values and mispricing:

| Bank | PBV | ROE | Std dev | Predicted PBV | Under/Over |
|---|---|---|---|---|---|
| Bayerische Hypo-und Vereinsbank | 0.80 | −1.66% | 49.06% | 0.89 | −10.60% |
| Commerzbank | 1.09 | −6.72% | 36.21% | 1.05 | +3.25% |
| Deutsche Bank | 1.23 | 1.32% | 35.79% | 1.36 | −9.26% |
| Banca Intesa | 1.66 | 1.56% | 34.14% | 1.41 | +17.83% |
| BNP Paribas | 1.72 | 12.46% | 31.03% | 1.89 | −8.75% |
| Banco Santander | 1.86 | 11.06% | 28.36% | 1.91 | −2.66% |
| Sanpaolo IMI | 1.96 | 8.55% | 26.64% | 1.86 | +5.23% |
| BBVA | 1.98 | 11.17% | 18.62% | 2.17 | −9.12% |
| Societe Generale | 2.04 | 9.71% | 22.55% | 2.02 | +1.37% |
| Royal Bank of Scotland | 2.09 | 20.22% | 18.35% | 2.51 | −16.65% |
| HBOS | 2.15 | 22.45% | 21.95% | 2.49 | −13.71% |
| Barclays | 2.23 | 21.16% | 20.73% | 2.48 | −9.96% |
| Unicredito Italiano | 2.30 | 14.86% | 13.79% | 2.44 | −5.72% |
| Kredietbank Luxembourgeoise | 2.46 | 17.74% | 12.38% | 2.58 | −4.79% |
| Erste Bank | 2.53 | 10.28% | 21.91% | 2.05 | +23.11% |
| Standard Chartered | 2.59 | 20.18% | 19.93% | 2.47 | +5.00% |
| HSBC | 2.94 | 18.50% | 19.66% | 2.41 | +21.91% |
| Lloyds TSB | 3.33 | 32.84% | 18.66% | 2.96 | +12.40% |

**US grocery sector, price-to-sales on net margin, four vintages:**

| Year | Sector regression | R² | Whole Foods margin | Predicted PS | Actual PS | Verdict |
|---|---|---|---|---|---|---|
| Jan 2007 | PS = 0.07 + 10.49 × Net Margin | 0.595 | 3.41% | 0.43 | 1.41 | Overvalued (3x) |
| Jan 2009 | PS = 0.07 + 10.49 × Net Margin | 0.801 | 2.77% | 0.36 | 0.31 | Slightly under |
| Jan 2010 | PS = 0.06 + 11.43 × Net Margin | 0.638 | 1.44% | 0.22 | 0.50 | Overvalued (2x+) |
| Jan 2015 | PS = 0.557 + 8.50 × Net Margin | 0.291 | 4.08% | 0.90 | 1.35 | Overvalued |

Net margins as decimals. By January 2015 Sprouts (SFM) had taken over as the sector's premium name at roughly 2x sales, and the fit had deteriorated badly (R² 0.291).

**Worked example — Telebras:** growth 7.5%, emerging market = 1.
```
Predicted PE = 13.12 + 121.22(0.075) − 13.85(1) = 8.35
Actual PE = 8.9  →  8.9/8.35 − 1 = +6.6%
```
Telebras trades above its predicted PE. Despite having one of the two lowest PEs in the sector, it is slightly overvalued relative to peers. A low multiple is not the same as cheap.

**Determinism:** DETERMINISTIC — running the regression from firm-level data; computing predicted multiples and the over/under percentage; applying the t-statistic thresholds. JUDGMENT — which firms belong in the sector, which fundamentals enter, whether the fit is strong enough to act on, and what an unexplained residual means.

**Pitfalls:**
- Over-fitting a small sector sample with too many variables.
- Trusting a regression whose R² has collapsed. The 2015 grocery fit explained under 30% of the variance, so its predictions carry little weight.
- Assuming stability. The grocery coefficients moved in every vintage, and Whole Foods flipped from overvalued to undervalued and back within two years.
- Ignoring that the whole sector may be mispriced. A sector regression can only say "cheap relative to these peers" ([[pricing-vs-value]]).
- Reading a large positive residual as a sell signal without asking what the regression omits (growth, brand, expected margin recovery).
- Running the regression on current fundamentals when the sector is priced on expected ones ([[pricing-young-companies]]).

**Sources:**
- valpacket2spr21 p.57-59, p.62-63, p.71-74
- valpacket2spr20 p.57-59, p.62-63, p.71-74

**Related:** [[comparable-selection-and-controls]], [[market-wide-regressions]], [[book-value-multiples]], [[ev-sales-and-brand-value]], [[intrinsic-multiple-derivation]], [[pricing-young-companies]], [[multiple-distribution-statistics]], [[pricing-vs-value]]
