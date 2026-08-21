# The debt-equity trade-off (five forces)

**Core idea:** Debt has two real benefits and three real costs. The benefits are the tax deductibility of interest and the discipline debt imposes on managers. The costs are expected bankruptcy costs, agency costs between stockholders and lenders, and the loss of future financing flexibility. Every qualitative judgment about how much a firm should borrow reduces to weighing these five forces. The quantitative approaches ([[cost-of-capital-approach]], [[apv-approach]]) are just formal ways of pricing the same forces.

**Formulas:**
- Annual tax benefit of debt = `Tax Rate × Interest Payment`. Tax Rate = the firm's *marginal* tax rate; Interest Payment = dollar interest expense that year. The benefit accrues only if taxable income covers the interest ([[tax-benefit-of-debt]]).
- Expected bankruptcy cost = `Probability of bankruptcy × Cost of going bankrupt`. Cost of going bankrupt = direct costs (legal/administrative deadweight, empirically 5–10% of firm value) + indirect costs (lost business because customers, suppliers and employees perceive distress).

**Procedure:** Score the firm on each of the five factors, then set a prior on whether it should carry a high or low debt ratio.
1. **Tax benefit.** What is the marginal tax rate on the firm's income? Higher rate → more debt (Proposition 1). Check for offsets: Brazil, for instance, allows a deduction for interest on equity capital, which blunts debt's advantage.
2. **Discipline.** How separated are managers from owners, and how passive is the stockholder base? Debt's disciplinary value is greatest for a conservatively financed, publicly traded firm held by millions of small investors with no large holder. It is smallest for a private, owner-managed firm, and small where activist institutions already discipline managers.
3. **Expected bankruptcy cost.** How volatile are earnings and cash flows? More volatility → higher default probability at any debt level (Proposition 2). Then ask how large the *indirect* costs would be. They are large where customers buy long-lived products needing future service and support (aircraft manufacturers, autos) or where value rests on intangibles and people (high tech). They are small where purchases are for immediate consumption (grocery stores). Greater indirect costs → less debt (Proposition 3).
4. **Agency cost.** How easily can lenders observe and monitor the use of their money? Agency costs are highest with intangible assets and hard-to-observe investments (a technology firm); lowest with visible, tangible, monitored assets (a regulated utility, a mining company). Greater agency problems → less debt (Proposition 4), or debt with heavier covenants and higher rates.
5. **Flexibility.** How predictable are future financing needs, and how good is access to capital markets? More uncertainty about future needs → less debt today (Proposition 5). Firms that can forecast needs and reach capital markets easily can afford to use debt capacity now.
6. Combine: borrow more when the marginal tax rate is high, manager-stockholder separation is wide, earnings are stable, bankruptcy costs are low, lenders can monitor easily, funding needs are forecastable, and market access is good. Borrow less in the opposite cases.
7. Compare the resulting prior to the firm's actual debt ratio. A large gap is the signal to run the quantitative approaches and to ask why the gap exists.

**Reference data:** What CFOs of large US companies say actually drives financing decisions (survey, ranking on a 0–5 scale). Note that flexibility and survival beat stock-price maximization:

| Rank | Factor | Score |
|---|---|---|
| 1 | Maintain financial flexibility | 4.55 |
| 2 | Ensure long-term survival | 4.55 |
| 3 | Maintain predictable source of funds | 4.05 |
| 4 | Maximize stock price | 3.99 |
| 5 | Maintain financial independence | 3.88 |
| 6 | Maintain high debt rating | 3.56 |
| 7 | Maintain comparability with peer group | 2.47 |

Marginal tax rates used in the case applications: US 40% (Disney, Bookscape, pre-2018 code), India 32.5% (Tata Motors), China 25% (Baidu), Brazil 34% (Vale, offset by deductibility of interest on equity capital). Current-vintage rates: US 27% (federal + state), India 30%, China 25%, Brazil 34%, UK 19%, Germany 30%, Japan 30.62%, global average 23.79% (2021 KPMG-style table shipped with capstru.xlsx).

**Worked example:** The four case firms scored on the five forces.
- *Tax benefit*: highest for Disney and Bookscape (40% US rate), lowest for Baidu (25% China); Vale's 34% Brazilian rate is offset by the interest-on-equity deduction.
- *Discipline*: highest at Disney, where ownership and management are clearly separated; low elsewhere (family group at Tata, concentrated control at Baidu and Vale).
- *Bankruptcy cost*: earnings volatility is high at Baidu (young tech), Tata Motors (cyclical autos) and Vale (commodity prices), low at Disney (diversified entertainment). Indirect costs are highest at Tata Motors, since cars are long-lived and need service.
- *Agency cost*: highest at Baidu (intangible assets, services); lowest at Vale (mines are visible and easily monitored) and Tata Motors (tangible assets, group backing). At Disney it varies by business — higher in movies and broadcasting, lower in theme parks.
- *Flexibility*: Baidu values it most (technology shifts unpredictably); Disney and Tata Motors least (mature, well-mapped investment needs). Bookscape needs flexibility because a private firm's access to external capital is poor.
Prediction: Disney can carry the most debt; Baidu the least. The quantitative optima confirm it (Disney 40%, Baidu 0–10%).

**Determinism:**
- DETERMINISTIC: the annual tax benefit given a marginal tax rate and interest expense; the expected bankruptcy cost given a default probability and a bankruptcy-cost percentage.
- JUDGMENT: every input that matters here. The probability of bankruptcy at a given debt level (needs earnings volatility history and a rating), the size of indirect bankruptcy costs (needs product life, service dependence, intangibility of value), the severity of agency conflict (needs asset type and monitorability), and the value of flexibility (needs a view on how forecastable future investment needs are).

**Pitfalls:**
- Using the *effective* tax rate instead of the *marginal* rate for the tax benefit. In 2017 the US marginal rate was ~40% while average effective rates were ~22%; interest saves taxes at the margin, so the marginal rate is the right one.
- Assuming the tax benefit exists when the firm has no taxable income to shelter.
- Double-counting protection: imposing a rating constraint *and* haircutting operating income for a downside scenario ([[downside-risk-and-rating-constraints]]).
- Forgetting that the discipline benefit is an argument about *other people's* managers; it is weakest exactly where owners already run the firm.
- Treating the five forces as independent of the business mix. They all follow from what the firm does, which is why the optimal debt ratio is a function of business risk and the tax rate, not of what the borrowed money is spent on.

**Sources:**
- corporate_finance--lecture_slides--cfpacket2spr20 p.11
- corporate_finance--lecture_slides--cfpacket2spr20 p.13
- corporate_finance--lecture_slides--cfpacket2spr20 p.17-18
- corporate_finance--lecture_slides--cfpacket2spr20 p.19-23
- corporate_finance--lecture_slides--cfpacket2spr20 p.24
- corporate_finance--lecture_slides--cfpacket2spr20 p.25-27
- corpfin-capital-structure — capstru.xlsx, sheet `Marginal tax rate by country` (2021 marginal rates)

**Related:** [[tax-benefit-of-debt]], [[miller-modigliani]], [[pecking-order]], [[cost-of-capital-approach]], [[apv-approach]], [[enhanced-cost-of-capital-approach]], [[determinants-of-optimal-debt-ratio]], [[relative-and-regression-analysis]]
