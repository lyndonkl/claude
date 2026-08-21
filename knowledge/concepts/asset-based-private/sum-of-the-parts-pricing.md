# Sum of the parts with multiples (pricing the parts)

**Core idea:** Price each division off its own sector's peers, then add. The crude version applies each sector's *median* multiple to the division's scalar. The refined version recognizes that a division is not the median firm in its sector. For each sector you pick the multiple that fundamentals explain best, run that sector's regression of the multiple on its drivers, and evaluate the regression at the division's own return on capital, margin and tax rate. That gives a division-specific predicted multiple. Controlling for fundamentals matters: for United Technologies it raised the sum of the parts from $61.7bn to $74.2bn, because UTC's divisions earn above-average returns.

**Formulas:**
- Crude: `Value(Division_i) = Scalar_i × Median sector multiple_i`
- Refined: `Predicted multiple_i = f_sector(division fundamentals)`, then `Value(Division_i) = Scalar_i × Predicted multiple_i`
- Sector regression forms used (all fundamentals as decimals):
  - `EV/EBITDA = a + b × Tax Rate + c × ROC`
  - `EV/Revenues = a + b × Pre-tax operating margin`
  - `EV/Capital = a + b × ROC`
- Segment EBITDA when only EBIT is reported: `EBITDA_i = Normalized EBIT_i + D&A_i`
- Equity bridge: `Equity = Σ_i Value(Division_i) − Debt − Financing-arm debt − Minority interests + Cash`; `Value per share = (Equity − Value of options) / Shares outstanding`
- Symbols: `Scalar_i` = the division's revenues, EBITDA, or capital invested, matched to the multiple; `ROC` = after-tax operating income / capital invested; `Pre-tax operating margin` = pre-tax operating income / revenues; `D&A` = depreciation and amortization.

**Procedure:**
1. Assemble the divisional scalars: revenues, EBITDA, operating income, capital invested. Normalize the earnings measure if the latest year is not representative — for GE, Damodaran used each segment's average 2013–17 EBIT margin applied to 2017 revenues.
2. Assign each division to a sector and collect the peer group for that sector.
3. Choose the multiple per sector. Decision rule: use the multiple whose regression on fundamentals has the **highest R²** for that sector. Do not force one multiple across all divisions.
4. Estimate (or look up) the sector regression of that multiple on its companion variables.
5. Evaluate the regression at the division's own fundamentals to get a predicted multiple.
6. Multiply: predicted multiple × the division's matching scalar = the division's value.
7. Sum the divisions. Then subtract the capitalized value of unallocated corporate expenses (see [[sum-of-the-parts-dcf]] for the capitalization formula) if the segment earnings were reported before corporate G&A.
8. Bridge to equity: subtract all debt (including a captive finance arm's debt) and minority interests, add cash, subtract the value of employee options, divide by shares.
9. Compare with the intrinsic sum of the parts and with the market price.

**Reference data:**

Sector regressions used for United Technologies (2009), with R²:

| Business | Best multiple | Regression | R² |
|---|---|---|---|
| Refrigeration systems | EV/EBITDA | 5.35 − 3.55 Tax Rate + 14.17 ROC | 42% |
| Defense | EV/Revenues | 0.85 + 7.32 Pre-tax operating margin | 47% |
| Construction | EV/EBITDA | 3.17 − 2.87 Tax Rate + 14.66 ROC | 36% |
| Security | EV/Capital | 0.55 + 8.22 ROC | 55% |
| Industrial products | EV/Revenues | 0.51 + 6.13 Pre-tax operating margin | 48% |
| Aircraft | EV/Capital | 0.65 + 6.98 ROC | 40% |

Median sector EV/EBITDA multiples used in the crude version (2009): Refrigeration 5.25, Defense 8.00, Construction 6.00, Security 7.50, Industrial products 5.50, Aircraft 9.00.

Peer-group EV/EBITDA multiples used for GE's segments (2018 analysis of 2017 data): Power 10.55, Renewable Energy 15.13, Oil & Gas 12.15, Aviation 6.56, Healthcare 10.97, Transportation 11.22, Lighting 12.80, GE Capital 10.13.

**Worked example — United Technologies, 2009 ($ millions, tax rate 38% for all divisions):**

| Division | Scalar | Scalar value | ROC | Op. margin | Predicted multiple | Value |
|---|---|---|---|---|---|---|
| Carrier | EBITDA | 1,510 | 13.57% | 8.81% | 5.35 − 3.55(.38) + 14.17(.1357) = 5.92 | 8,944.47 |
| Pratt & Whitney | Revenues | 12,965 | 24.51% | 16.37% | 0.85 + 7.32(.1637) = 2.05 | 26,553.29 |
| Otis | EBITDA | 2,680 | 35.71% | 19.13% | 3.17 − 2.87(.38) + 14.66(.3571) = 7.31 | 19,601.70 |
| UTC Fire & Security | Capital | 5,575 | 6.03% | 8.39% | 0.55 + 8.22(.0603) = 1.05 | 5,828.76 |
| Hamilton Sundstrand | Revenues | 6,207 | 14.16% | 17.71% | 0.51 + 6.13(.1771) = 1.59 | 9,902.44 |
| Sikorsky | Capital | 2,217 | 13.37% | 8.90% | 0.65 + 6.98(.1337) = 1.58 | 3,509.61 |
| **Sum of the parts (operating assets)** | | | | | | **74,230.37** |

The same divisions priced at raw sector medians give only $61,661M. The $12.6bn difference is what controlling for fundamentals buys.

**Worked example — GE, 2018 analysis on 2017 data ($ millions):** Segment EBITDA = normalized EBIT (2013–17 average margin × 2017 revenues) + 2017 D&A. Power: 4,061.80 + 1,358.00 = 5,419.80 × 10.55 = 57,179. Aviation: 5,209.28 + 979.00 = 6,188.28 × 6.56 = 40,595. Summing all segments including GE Capital gives a pricing of the business of 212,027.44. Bridge: − GE debt 83,568.00 − GE Capital debt 51,023.00 − minority interests 17,723.00 + cash 43,299.00 = 103,012.44; − options 218.94 = 102,793.50; ÷ GE's shares outstanding (about 8.68 billion, implied by the packet's per-share figure) = **$11.84 per share**. The intrinsic sum of the parts gave $10.92 per share on the identical bridge.

**Determinism:**
- DETERMINISTIC: `{division scalars, division fundamentals, sector regression coefficients} → predicted multiples → division values → sum`. Also the entire equity bridge and the per-share division. A script can compute the whole thing.
- JUDGMENT: sector assignment for each division; the peer group; whether to normalize earnings and over what window; which multiple to use when two sector regressions have similar R²; how to allocate corporate G&A across segments; and the option value in the bridge. That judgment needs segment disclosures, sector peer data, and the company's own margin history.

**Pitfalls:**
- Applying one multiple (usually EV/EBITDA) to every division regardless of sector. The crude version understated UTC by $12.6bn.
- Mismatching multiple and scalar — an EV/Capital multiple applied to EBITDA, or an equity multiple applied to an enterprise scalar.
- Using an unnormalized trough or peak year for a cyclical segment.
- Forgetting that segment EBIT is often reported *before* corporate G&A, so segment values double-count the missing overhead until you subtract its capitalized value.
- Forgetting the financing arm's debt. GE's bridge subtracts $51.0bn of GE Capital debt separately from $83.6bn of industrial debt.
- Believing the pricing answer is a value. It is a price, and it inherits whatever the peer group's own mispricing is.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket2spr21 p.111-114, p.120, p.122
- valuations--lecture_notes--spring_2020--valpacket2spr20 p.109-112, p.118, p.120

**Related:** [[sum-of-the-parts-framework]], [[sum-of-the-parts-dcf]], [[asset-based-valuation-overview]], [[liquidation-valuation]], [[market-regression-multiples]], [[ev-ebitda-multiple]], [[choosing-comparable-firms]]
