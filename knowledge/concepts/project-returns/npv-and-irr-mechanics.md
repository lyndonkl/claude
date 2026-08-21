# NPV and IRR mechanics

**Core idea:** Net Present Value sums the present values of *all* cash flows on a project, including the initial investment, discounted at the appropriate hurdle rate. A positive NPV means the project earns more than the cost of capital and adds value. The NPV figure is literally the expected increase in firm value from taking the project. Internal Rate of Return is the discount rate that drives NPV to zero — a percentage return built from the same incremental, time-weighted cash flows. Plotting NPV against a range of discount rates gives the NPV profile; the IRR is where that curve crosses the x-axis. The two rules almost always agree on accept/reject for a stand-alone project. They can disagree when ranking projects against each other.

**Formulas:** Symbols: `CF_t` = cash flow in year t (t = 0 is the initial investment, normally negative); `r` = hurdle rate; `n` = project life.
- `NPV = Σ_{t=0..n} CF_t / (1 + r)^t`
- `IRR` = the value of r solving `Σ_{t=0..n} CF_t / (1 + r)^t = 0`
- Discount-rate matching: `r = cost of capital` when CF are cash flows to the firm; `r = cost of equity` when CF are cash flows to equity.
- `Profitability index = NPV / initial investment`
- `Payback` = the year in which cumulated undiscounted cash flow first turns positive (interpolate within the year). `Discounted payback` uses cumulated present values.

**Procedure:**
1. Assemble the incremental after-tax cash flow stream, year 0 through the end of the estimation period. Include salvage or terminal value in the final year.
2. Select the hurdle rate matched to the cash flows' claimholder, currency, business risk, and geography. See [[project-hurdle-rate-selection]].
3. Discount each year's cash flow and sum. Accept if `NPV > 0`.
4. Solve for IRR by root-finding on the same stream. Accept if `IRR > hurdle rate`.
5. Build the NPV profile across a grid of discount rates (e.g. 8% to 30%). Read off the crossing point and check for more than one crossing. Multiple crossings signal multiple IRRs.
6. Report the NPV as a dollar statement of value added, not just a sign.
7. Where cash flows for a synergy or a differently-risky sub-stream are involved, discount each stream at *its own* rate and add the NPVs. Do not blend rates.

**Reference data:** Primary capital-budgeting rule used by firms (survey, % of firms):

| Decision rule | 1976 | 1986 | 1998 |
|---|---|---|---|
| IRR | 53.6% | 49.0% | 42.0% |
| Accounting return | 25.0% | 8.0% | 7.0% |
| NPV | 9.8% | 21.0% | 34.0% |
| Payback period | 8.9% | 19.0% | 14.0% |
| Profitability index | 2.7% | 3.0% | 3.0% |

IRR remains the most popular primary rule, but its share has fallen while NPV's has risen sharply. Accounting returns have collapsed.

**Worked example:** Rio Disney NPV at an 8.46% cost of capital ($ millions).

| Year | Annual cash flow | Terminal value | Present value |
|---|---|---|---|
| 0 | −$2,000 | | −$2,000 |
| 1 | −$1,000 | | −$922 |
| 2 | −$859 | | −$730 |
| 3 | −$267 | | −$210 |
| 4 | $340 | | $246 |
| 5 | $466 | | $311 |
| 6 | $516 | | $317 |
| 7 | $555 | | $314 |
| 8 | $615 | | $321 |
| 9 | $681 | | $328 |
| 10 | $715 | $11,275 | $5,321 |
| **NPV** | | | **$3,296** |

Year 10 PV = (715 + 11,275)/1.0846^10 = $5,321. NPV = +$3,296 million, so Disney's value rises by $3,296 million if it takes the project. The NPV profile falls from roughly +$4,000 million at an 8% discount rate to about −$2,500 million at 30%, crossing zero at IRR = 12.60%. Because 12.60% > 8.46%, the IRR rule agrees: accept.

Second example, Bookscape Online. Stand-alone incremental cash flows of −$1,150,000; $340,000; $415,000; $446,500; $720,730 over four years, discounted at the project's 18.12% cost of capital, give NPV = $76,375 — positive, so the stand-alone project passes.

**Determinism:** DETERMINISTIC — given the cash flow stream and a hurdle rate, a script computes every present value, the NPV, the accept/reject verdict, the NPV profile across any rate grid, the IRR by root-finding, the profitability index, and payback. JUDGMENT — building the cash flow stream and choosing the hurdle rate. Both sit upstream of this computation, and both dominate the answer.

**Pitfalls:**
- Discounting cash flows to the firm at a cost of equity, or equity cash flows at a WACC.
- Forgetting the year-0 investment, or double counting it inside the cash flow stream *and* as a separate outflow.
- Reporting IRR without checking the NPV profile for multiple sign changes.
- Blending one discount rate across streams with genuinely different risk (project vs synergy).
- Treating a marginally positive NPV as a strong recommendation. Netflix Fit's stand-alone NPV of $106 million on a $2.4 billion investment is a thin margin, and small assumption changes flip it.

**Sources:**
- corporate_finance--lecture_slides--cfpacket1spr20 p.244
- corporate_finance--lecture_slides--cfpacket1spr20 p.246-249
- corporate_finance--lecture_slides--cfpacket1spr20 p.303-304
- corporate_finance--lecture_slides--cfpacket1spr20 p.308
- corporate_finance--lecture_slides--cfpacket1spr20 p.310
- corporate_finance--case--netflixfit p.7
- corporate_finance--case--netflixfitpresentation p.13
- corporate_finance--case--netflixfitpresentation p.19

**Related:** [[npv-vs-irr-conflicts]], [[time-value-and-cash-flow-timing]], [[terminal-value-and-project-life]], [[project-hurdle-rate-selection]], [[uncertainty-payback-sensitivity-simulation]], [[capital-budgeting-model]], [[netflix-fit-case]]
