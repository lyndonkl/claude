# The standard capital budgeting model (capbudg)

**Core idea:** Damodaran's `capbudg.xls` is the canonical single-sheet project model, and it encodes the whole investment-analysis method in one place. It takes a project's revenue, expense, depreciation, and working-capital assumptions and builds a 1–10 year after-tax cash flow table. It discounts that table at either a directly entered rate or a CAPM-based cost of capital. It reports NPV, IRR, and the average accounting return on capital. Two switches carry most of the modeling choices: the discount-rate approach (direct rate versus WACC) and the depreciation method (straight line versus double declining balance). The model also builds in the pieces analysts most often forget — an opportunity cost line, an investment tax credit, working capital as a percent of revenues, and salvage of both equipment and working capital at the end of life.

**Formulas:** Symbols: `r` = discount rate; `t` = tax rate; `L` = project lifetime in years; `BV` = book value of equipment.
- Discount rate, WACC branch: `k_e = Rf + β × MRP`; `r = k_e × (1 − Debt ratio) + k_d × (1 − t) × Debt ratio`
- Net investment: `Net investment = Investment − tax credit rate × Investment`
- Initial outlay at t=0: `Outlay = Net investment + initial working capital + opportunity cost + other (non-depreciable) investment`; `Cash flow_0 = −Outlay`
- Revenues: `Rev_1 = base revenue`; `Rev_t = Rev_{t−1} × (1 + g_rev,t)`
- `Variable expenses_t = variable% × Rev_t`; `Fixed_t = Fixed_{t−1} × (1 + g_fixed,t)`
- `EBITDA_t = Rev_t − Variable_t − Fixed_t`
- Straight-line depreciation: `Dep_t = (Investment − Salvage) / L`
- Double declining balance: `Dep_t = min( (2/L) × BV_beg,t , BV_beg,t − Salvage )`; `BV_end,t = BV_beg,t − Dep_t`
- `EBIT_t = EBITDA_t − Dep_t`; `Tax_t = t × EBIT_t` (negative EBIT gives a negative tax, i.e. full loss offset); `EBIT(1−t)_t = EBIT_t × (1 − t)`
- Working capital: `WC_t = WC% × Rev_t`; `ΔWC_1 = WC% × Rev_1 − initial WC`; `ΔWC_t = WC% × (Rev_t − Rev_{t−1})` for t ≥ 2
- `Net after-tax cash flow_t = EBIT(1−t)_t + Dep_t − ΔWC_t`
- Salvage in the final year: equipment salvage = the entered salvage value; working-capital salvage = `salvageable fraction × WC_L`
- `Discounted CF_t = (NATCF_t + equipment salvage_t + WC salvage_t) / (1 + r)^t`
- `NPV = Σ_{t=0..L} Discounted CF_t`; `IRR` = IRR of the stream including t=0 and final-year salvage
- `ROC = mean(EBIT(1−t)_t) / mean(BV_beg,t)` — beginning-of-year *equipment* book value only, excluding working capital and opportunity cost

**Procedure:**
1. Enter the investment block: initial investment, opportunity cost of any owned resource, lifetime (≤ 10 years), salvage value, depreciation method, investment tax credit rate, and any non-depreciable "other" investment.
2. Enter the working capital block: initial working capital, working capital as a percent of revenues, and the salvageable fraction at the end.
3. Enter the operating block: year-1 revenues, variable expenses as a percent of revenues, year-1 fixed expenses, and the tax rate on net income.
4. Enter the growth vectors for years 2–10: revenue growth and fixed-expense growth (the latter usually defaults to the revenue growth rate).
5. Choose the discount-rate approach. Direct → enter the rate. CAPM → enter beta, riskless rate, market risk premium, debt ratio, and pre-tax cost of borrowing.
6. Read NPV, IRR, and ROC. Accept if NPV > 0 and IRR > the discount rate; cross-check ROC against the same rate.
7. Sensitivity-test by re-running with different revenue growth, price, or discount-rate inputs. See [[uncertainty-payback-sensitivity-simulation]].

**Reference data:** Model input map (with the example values shipped in the sheet):

| Input | Example |
|---|---|
| Initial investment | 50,000 |
| Opportunity cost | 7,484 |
| Lifetime (years, ≤ 10) | 10 |
| Salvage value at end | 10,000 |
| Depreciation method (1 = straight line, 2 = DDB) | 2 |
| Tax credit rate on investment | 10% |
| Other (non-depreciable) investment | 0 |
| Initial working capital | 10,000 |
| Working capital as % of revenues | 25% |
| Salvageable fraction of working capital | 100% |
| Revenues in year 1 | 40,000 |
| Variable expenses as % of revenues | 50% |
| Fixed expenses in year 1 | 0 |
| Tax rate on net income | 40% |
| Discount-rate approach (1 = direct, 2 = CAPM/WACC) | 2 |
| Direct discount rate | 10% |
| Beta | 0.9 |
| Riskless rate | 8% |
| Market risk premium | 5.5% |
| Debt ratio | 30% |
| Pre-tax cost of borrowing | 9% |
| Revenue growth, years 2–10 | 10%, 10%, 10%, 10%, 0, 0, 0, 0, 0 |

Companion models in the same family: `returncalculator.xls` computes ROIC and ROE from financial statements with lease and R&D capitalization built in; `oplease.xls` converts operating-lease commitments to debt; `ratings.xls` produces a synthetic rating and cost of debt from an interest coverage ratio.

**Worked example:** The sheet's shipped example, end to end.

Discount rate (CAPM branch): `k_e` = 8% + 0.9 × 5.5% = 12.95%. `r` = 12.95% × 0.70 + 9% × 0.60 × 0.30 = **10.685%**.

Initial outlay: net investment = 50,000 − 10% × 50,000 = 45,000. Outlay = 45,000 + 10,000 working capital + 7,484 opportunity cost + 0 = **62,484**, entered as a negative cash flow at t=0.

Year 1: revenues 40,000; variable expenses 20,000; EBITDA 20,000; DDB depreciation at 2/10 × 50,000 = 10,000; EBIT 10,000; tax 4,000; EBIT(1−t) 6,000; add back depreciation 10,000; ΔWC = 25% × 40,000 − 10,000 = 0. Net after-tax cash flow = **16,000**. PV = 16,000/1.10685 = 14,455.44.

Revenues grow 10% through year 5 (to 58,564) then flatten, so ΔWC is 25% of each revenue increment (1,000 rising to 1,331, then zero). The DDB schedule runs 10,000; 8,000; 6,400; 5,120; 4,096; 3,276.80; 2,621.44; then 485.76 in year 8 where it is capped at BV − salvage; then zero, with book value parked at the 10,000 salvage floor.

Year 10 adds equipment salvage of 10,000 and working-capital recovery of 100% × 25% × 58,564 = 14,641. PV of that final year = (17,569.20 + 10,000 + 14,641)/1.10685^10 = 15,294.30.

Results: **NPV = 47,927.65**, **IRR = 23.554%**, **ROC = 60.12%** (average EBIT(1−t) of 13,710.72 over average beginning equipment book value of 22,805.70).

**Determinism:** DETERMINISTIC — every output is a pure function of the inputs. A script takes the scalar inputs plus two length-9 growth vectors and returns NPV, IRR, ROC, and the full annual table. IRR needs a root-finder. JUDGMENT — every input. Revenue forecasts, expense ratios, the opportunity cost estimate, project life, salvage value, the depreciation method, and the discount-rate inputs all require reasoning outside the model.

**Pitfalls:**
- The DDB branch must cap each year's charge at `BV − salvage` and hold book value at salvage thereafter. The year-8 cap of 485.76 in the example is the regression test for a correct port.
- Salvage flows land in year `lifetime`, not automatically in year 10. A lifetime index zeroes out all years beyond the project life.
- Year-1 ΔWC is `WC% × Rev_1 − initial WC`, which can be non-zero or negative if the entered initial working capital does not equal `WC% × Rev_1`.
- Negative EBIT produces a negative tax — the model assumes full loss offset against other income. Flag this if the project stands alone in a firm with no other income.
- The ROC denominator uses beginning equipment book value only. Working capital and the opportunity cost are excluded, so the model's ROC is not comparable to a full invested-capital ROIC.
- Salvage is not in the net-after-tax-cash-flow row; it is added inside the final year's discounted cash flow. Do not double count it.
- The model has no loss carryforward, no mid-year convention, and no inflation escalator beyond the growth vectors.

**Sources:**
- corpfin-payout-projects (capbudg.xls: full input map, cash-flow logic, DDB schedule, NPV/IRR/ROC outputs, worked example, edge cases)
- corpfin-ratings-risk (returncalculator.xls, ratings.xls: companion accounting-return and cost-of-debt models)
- corporate_finance--lecture_slides--cfpacket1spr20 p.244
- corporate_finance--lecture_slides--cfpacket1spr20 p.308-310

**Related:** [[earnings-vs-cash-flows]], [[npv-and-irr-mechanics]], [[accounting-returns-roc-roe-eva]], [[opportunity-costs-and-side-costs]], [[terminal-value-and-project-life]], [[project-hurdle-rate-selection]], [[uncertainty-payback-sensitivity-simulation]], [[operating-lease-capitalization]], [[synthetic-rating]]
