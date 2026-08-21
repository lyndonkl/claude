# Tax rate in a DCF (effective vs marginal, and NOLs)

**Core idea:** After-tax operating income drives FCFF, so the tax rate is a first-order input. The real choice is between the **effective tax rate** (taxes actually reported divided by taxable income, which mostly reflects timing differences between tax books and reporting books) and the **marginal tax rate** (the statutory rate on the next dollar of income). For projections the marginal rate is safer, because the book-tax differences that drive the effective rate cannot be projected. The standard compromise is to start at the effective rate and converge it to the marginal rate over the forecast. Whatever rate you use in the numerator must be the same rate you use for the after-tax cost of debt in the denominator. Separately, a firm with accumulated losses pays no tax until the net operating loss (NOL) carryforward is exhausted, which produces a 0% rate for several years and then a jump to the marginal rate.

**Formulas:**
- Effective tax rate = Taxes paid (or provision) / Taxable (pre-tax) income.
- Marginal tax rate = statutory corporate rate of the country of domicile (Damodaran's default), or a revenue-weighted average of marginal rates across countries of operation.
- After-tax operating income = `EBIT × (1 − t)` when there is no NOL shield.
- With an NOL balance `NOL_(t−1)` carried into year t:
  - If `EBIT_t <= 0`: taxes = 0 and `NOL_t = NOL_(t−1) + |EBIT_t|`; after-tax operating income = `EBIT_t`.
  - If `0 < EBIT_t <= NOL_(t−1)`: taxes = 0; `NOL_t = NOL_(t−1) − EBIT_t`; after-tax operating income = `EBIT_t`.
  - If `EBIT_t > NOL_(t−1)`: taxes = `(EBIT_t − NOL_(t−1)) × t_marginal`; `NOL_t = 0`; after-tax operating income = `EBIT_t − taxes`.
  - Reported effective rate in that crossover year = taxes / EBIT (a partial rate between 0 and the marginal rate).
- Convergence path used in the standard forecast: hold the effective rate for years 1–5, then ramp linearly to the marginal rate over years 6–10: `t_(n+1) = t_n + (t_marginal − t_5)/5`.
- Consistency requirement: after-tax cost of debt = `Pre-tax cost of debt × (1 − t)` using **the same t** as the operating-income calculation.

**Procedure:**
1. Compute the firm's effective tax rate from the last 12 months (taxes / pre-tax income) and look up the marginal rate for its country of domicile.
2. Decide which rate anchors the forecast. Default: marginal rate, on the grounds that effective-rate gaps are book-tax timing artifacts. If the effective rate is far below the marginal rate for a structural reason you understand and expect to persist, start at the effective rate.
3. If starting from the effective rate, set an explicit convergence path to the marginal rate over the forecast — the standard is: constant through year 5, five equal steps to the marginal rate by year 10, marginal rate in perpetuity. (Override only if you deliberately believe the firm keeps its tax advantage forever.)
4. Check the loss position. If the firm has an NOL carryforward (or is projected to lose money in early forecast years), carry an NOL balance year by year using the three-branch rule above. Taxes are zero until the balance is burned, then jump.
5. Use the *same* rate for the after-tax cost of debt in the WACC in each year. In the years the firm pays no tax, the tax shield on debt is also worth nothing — the after-tax cost of debt equals the pre-tax cost of debt.
6. In the terminal year, use the marginal rate and no NOL shield.
7. Sanity check: a multinational with most revenue abroad may justify a weighted-average marginal rate, but the safe default remains the domicile's marginal rate.

**Reference data:**
- The quiz's answer set, which frames the whole decision: (a) effective rate from the statements; (b) taxes paid / EBIT; (c) marginal rate of the country of operation; (d) weighted-average marginal rate across countries; (e) none of the above; (f) **any of the above, as long as you use the same rate for the after-tax cost of debt.** (f) is the point: consistency dominates the choice.
- Marginal rates seen in the course cases: Brazil 34% (Vale, Embraer); Korea 25%; US 36.1% marginal vs 31.02% effective (Disney FY2013); Airbnb target 25%; Tesla 2015 marginal ~40% at the time.
- Statutory corporate tax rates by country are maintained in Damodaran's country dataset (the same table that carries country ERPs and default spreads); the January 2022 vintage carries a corporate-tax-rate column for ~177 countries.
- Convention worth noting: Disney's FY2013 reinvestment rate was computed on the **effective** rate (31.02%) while its return on capital used the **marginal** rate (36.1%) — a real inconsistency in the source material; prefer one rate throughout unless you can defend the split.

**Worked example — NOL carryforward:** A firm carries **$1,000m of NOLs** and expects **EBIT of $500m per year for 3 years**; the marginal rate for profitable firms is **40%**.

| Year | EBIT | NOL at start | Taxes | EBIT(1−t) | Effective rate |
|---|---|---|---|---|---|
| 1 | 500 | 1,000 | 0 | 500 | 0% |
| 2 | 500 | 500 | 0 | 500 | 0% |
| 3 | 500 | 0 | 200 | 300 | 40% |

Second example — Airbnb (Nov 2020, $ thousands): losses carried forward from a −13.69% base margin mean the firm pays no tax through year 4; the first tax appears in **year 5** (EBIT 904,916 -> EBIT(1−t) 777,799, a partial rate), with the full **25% target rate** applying thereafter.

**Determinism:**
- DETERMINISTIC: effective rate from the tax provision; the whole NOL waterfall given an EBIT path, an opening NOL balance and a marginal rate; the linear convergence path from effective to marginal; the after-tax cost of debt given the rate.
- JUDGMENT: which rate to anchor on and why; whether to use a domicile rate or a revenue-weighted multi-country rate; how fast to converge (years 6–10 is a convention, not a fact); whether an unusually low effective rate is a durable structural advantage (tax haven, R&D credits) or a timing difference; the opening NOL balance when disclosures are vague.

**Pitfalls:**
- Using the effective rate in the numerator and the marginal rate for the debt tax shield (or vice versa). This is the consistency error the framing quiz is built around.
- Locking a very low effective rate in forever — it understates taxes and overstates value.
- Applying `EBIT × (1 − t)` mechanically to a loss-making firm, generating a fictitious tax refund. Negative EBIT gets no tax benefit in the model; it grows the NOL.
- Taxing the whole of EBIT in the crossover year rather than only the excess over the remaining NOL.
- Forgetting that in the zero-tax years the debt tax shield is also zero, so the after-tax cost of debt should not be discounted.
- Extending an NOL shield into the terminal year.

**Sources:**
- valpacket1spr21 p.136-139
- valpacket1spr20 p.133-136
- valpacket1spr21 p.195 (Airbnb: losses carried forward, taxes begin year 5, 25% target rate)
- valpacket1spr20 p.192 (Tesla: operating losses carried forward save taxes in years 3–4)
- cfpacket2spr20 p.236, p.247 (Disney: effective 31.02% vs marginal 36.1%), p.262 (three-phase tax-rate row)
- spreadsheet:fcffsimpleginzu.xlsx — Valuation output rows 6, 7, 10 (tax-rate ramp, NOL roll-forward, three-branch EBIT(1−t))
- spreadsheet:higrowth.xls — `DCFValuation` NOL and effective-tax-rate rows

**Related:** [[fcff]], [[normalizing-depressed-earnings]], [[top-down-revenue-growth]], [[fcff-forecast-engine]], [[terminal-value]], [[cost-of-capital]], [[return-on-invested-capital]]
