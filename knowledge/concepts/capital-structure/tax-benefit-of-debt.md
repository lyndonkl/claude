# Tax benefit of debt and the limits on interest deductibility

**Core idea:** Interest is deducted before taxable income; dividends and buybacks are not. That asymmetry is the primary reason debt adds value. The benefit is bounded in three ways. First, it depends on the *marginal* tax rate, not the effective rate. Second, it only exists if there is taxable income to shelter — interest above EBIT buys no further deduction. Third, tax codes can cap deductibility directly: the 2017 US tax reform limits net interest deductions to 30% of EBITDA (through 2022) and 30% of EBIT thereafter. Inside a cost-of-capital or APV model these caps show up as a *reduced tax rate applied to the cost of debt* at high debt ratios, and they are what bends the cost-of-capital curve upward.

**Formulas:**
- `Annual tax benefit = t × Interest expense` (t = marginal tax rate).
- `Maximum tax benefit = EBIT × t` — you cannot shelter more income than you have.
- EBIT-limited tax rate: `t_EBIT = t` if Interest ≤ EBIT, else `t × EBIT / Interest`.
- Statutory-cap tax rate (post-2017 US): `t_cap = t` if Interest ≤ 0.30 × M, else `t × (0.30 × M) / Interest`, where M = EBITDA (through 2022) or EBIT (after 2022).
- Tax rate used for the after-tax cost of debt: `t_used = MIN(t_EBIT, t_cap)` (this is exactly `MIN(row66, row67)` in capstru.xlsx).
- `After-tax cost of debt = Pre-tax cost of debt × (1 − t_used)`.
- Perpetual-tax-benefit shortcut used in APV: `Tax benefits = Dollar Debt × t_used`.

**Procedure:**
1. Pick the marginal tax rate for the country and entity, not the reported effective rate. Use the statutory federal + state (or national) marginal rate on ordinary income.
2. At each candidate debt level, compute dollar interest = pre-tax cost of debt × dollar debt.
3. Compute `t_EBIT`: if interest ≤ EBIT, t stays at the marginal rate; otherwise scale it down by EBIT/Interest.
4. If the tax code caps deductions, compute `t_cap` with the 30% threshold against the specified measure (EBITDA now, EBIT after 2022 in the US).
5. Apply the smaller of the two rates to the pre-tax cost of debt.
6. Re-relever beta with the *same* reduced tax rate at that debt level — the levered beta formula uses `(1 − t)` and the tax shield is what dampens the beta increase. Betas at very high debt ratios therefore rise faster than a constant-t calculation implies (Disney's 70% beta is 2.3762 with the reduced rate vs 2.3016 at the full 36.1%).
7. Sanity-check the direction: a lower statutory tax rate lowers the optimal debt ratio for every firm, all else equal.

**Reference data:**
- Rate history that matters for US analyses: pre-2018 marginal rate ~40% (35–36% federal + state); 2018 onward federal 21%, with capstru.xlsx's 2021 country table listing the US at 27% including state taxes.
- Selected 2021 marginal corporate tax rates (from the table shipped with capstru.xlsx): US 27%, UK 19%, Germany 30%, France 26.5%, Japan 30.62%, China 25%, India 30%, Brazil 34%, Canada 26.5%, Ireland 12.5%, Switzerland 14.93%; global average 23.79%, OECD average 23.05%.
- Sensitivity of optimal debt ratios to the tax rate (case firms, re-optimized at hypothetical rates):

| Tax rate | Disney | Vale | Tata Motors | Baidu | Bookscape |
|---|---|---|---|---|---|
| 0% | 0% | 0% | 0% | 0% | 0% |
| 10% | 20% | 0% | 0% | 0% | 10% |
| 20% | 40% | 0% | 10% | 10% | 30% |
| 30% | 40% | 30% | 20% | 10% | 30% |
| 40% | 40% | 40% | 20% | 10% | 30% |
| 50% | 40% | 40% | 20% | 10% | 30% |

At a zero tax rate the optimal debt ratio is 0% for every firm — with no tax benefit, only the costs of debt remain.

**Worked example:** Disney at a 70% debt ratio (2013 analysis, marginal rate 36.1%, EBIT $10,032m adjusted for leases). Dollar debt = 0.70 × $137,839m = $96,487m at an 11.50% pre-tax rate, so interest = $11,096m. Interest exceeds EBIT, so the maximum tax benefit is capped at 10,032 × 0.361 = $3,622m. The adjusted tax rate is 3,622 / 11,096 = 32.64%, and the after-tax cost of debt is 11.50% × (1 − 0.3264) = 7.75% instead of 7.35%. Through 60% debt (interest $9,511m < EBIT) the full 36.1% applies. A post-2017 example from capstru.xlsx (Facebook): at a 40% debt ratio, interest of $29,494.9m exceeds EBIT $17,521m, so t drops from 0.40 to 0.2376.

**Determinism:**
- DETERMINISTIC: marginal tax rate + EBIT + EBITDA + interest expense + deduction-cap settings → `t_EBIT`, `t_cap`, `t_used`, after-tax cost of debt, and dollar tax benefit. Fully scriptable.
- JUDGMENT: choosing the marginal rate (which jurisdiction, whether to add state/local taxes, whether the firm actually pays at the margin), deciding whether a firm has reliable taxable income to shelter, and forecasting tax-law changes.

**Pitfalls:**
- Using effective tax rates. They average past deferrals and credits; the deduction saves tax at the margin.
- Assuming the tax benefit keeps scaling with debt. Above the EBIT (or 30%-of-EBITDA) threshold the marginal benefit dies, which is a major reason cost of capital turns up sharply.
- Forgetting the reduced tax rate when relevering beta at high debt ratios.
- Ignoring country-specific offsets. Brazil's deduction for interest on equity capital reduces debt's relative advantage.
- Assuming firms respond to tax changes as theory predicts. After the 2017 US reform, dollar debt at US companies kept rising from 2017 to 2019 (total debt roughly $5.8K to $6.6K units, with leases $7.9K to $9.4K); only debt-to-EBITDA fell, from about 3.8 to about 2.55.

**Sources:**
- corporate_finance--lecture_slides--cfpacket2spr20 p.14-16
- corporate_finance--lecture_slides--cfpacket2spr20 p.51
- corporate_finance--lecture_slides--cfpacket2spr20 p.72-74
- corporate_finance--lecture_slides--cfpacket2spr20 p.83
- corpfin-capital-structure — capstru.xlsx, sheet `Optimal Capital Structure` rows 66-68 and `Marginal tax rate by country`

**Related:** [[debt-equity-tradeoff]], [[cost-of-capital-approach]], [[synthetic-rating-and-cost-of-debt]], [[levered-beta-schedule]], [[apv-approach]], [[determinants-of-optimal-debt-ratio]]
