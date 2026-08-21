# NPV versus IRR: ranking conflicts, MIRR and the profitability index

**Core idea:** Independent projects are the exception. Firms often must choose between investments, either because the projects are mutually exclusive (both serve the same purpose) or because capital is rationed. Ranking is where NPV and IRR part company, for three reasons. First, a project has exactly one NPV but can have as many IRRs as its cash flows have sign changes. Second, NPV is a dollar surplus while IRR is a percentage, so NPV favors large projects and IRR favors small ones. Third, NPV assumes intermediate cash flows are reinvested at the hurdle rate; IRR assumes reinvestment at the IRR itself, which implicitly assumes an endless stream of equally lucrative projects. Two repairs exist: the Modified IRR fixes the reinvestment assumption, and the profitability index converts NPV into value per dollar invested for capital-rationed firms.

**Formulas:** Symbols: `CF_t` = cash flow in year t; `r` = hurdle rate; `n` = project life.
- `MIRR`: compound each intermediate cash flow forward at the hurdle rate. `Terminal Value = Σ_t CF_t × (1 + r)^(n − t)`. Then solve `Initial Investment × (1 + MIRR)^n = Terminal Value`.
- `Profitability index (PI) = NPV / Initial investment`
- Multiple-IRR condition: the number of IRRs can equal the number of sign changes in the cash flow stream.

**Procedure:**
1. Establish whether the projects are genuinely mutually exclusive, or whether the constraint is capital rationing. The remedy differs.
2. Compute NPV, IRR, and the NPV profile for each candidate.
3. Count sign changes in each cash flow stream. More than one sign change → IRR is unreliable. Fall back on NPV evaluated at the actual cost of capital.
4. If the projects differ in scale, prefer NPV. It measures dollars of value created, which is what the objective function maximizes.
5. If the projects differ in cash-flow timing at the same scale, the divergence is the reinvestment assumption. Compute MIRR to see the IRR corrected for it, then decide with NPV.
6. If capital is genuinely rationed, rank by profitability index — value created per dollar of scarce capital — rather than raw NPV.
7. If the projects have different lives, do not compare raw NPVs at all. See [[comparing-projects-different-lives]].
8. Match the rule to the firm's circumstances (see the reference table below) rather than insisting on one rule everywhere.

**Reference data:**

Rule-selection heuristics:

| Firm circumstance | More defensible rule |
|---|---|
| Limited access to capital, stream of surplus-value projects, uncertain cash flows | IRR (small, high-growth, private firms) |
| Substantial funds on hand, good capital access, few surplus projects, certain cash flows | NPV (large, public, mature firms) |
| Genuine capital rationing | Profitability index |
| Non-conventional cash flows (multiple sign changes) | NPV only |

Sources of capital rationing (survey):

| Cause | Firms | % of total |
|---|---|---|
| Debt limit imposed by outside agreement | 10 | 10.7% |
| Debt limit placed by management external to firm | 3 | 3.2% |
| Limit placed on borrowing by internal management | 65 | 69.1% |
| Restrictive policy imposed on retained earnings | 2 | 2.1% |
| Maintenance of target EPS or PE ratio | 14 | 14.9% |

Capital rationing is overwhelmingly self-imposed.

**Worked example:** Three cases, all from the packet.

*Case 1 — multiple IRRs.* Two projects with the same $1,000 investment:

| Year | Project 1 | Project 2 |
|---|---|---|
| 0 | −1,000 | −1,000 |
| 1 | 800 | 200 |
| 2 | 1,000 | 300 |
| 3 | 1,300 | 400 |
| 4 | −2,200 | 500 |

Project 1's cash flows change sign twice, so it has two IRRs: 6.60% and 36.55%. Its NPV profile is hump-shaped, negative at low rates, peaking near +$50 around 16–20%, then crossing zero again near 36%. Project 2 is conventional with a single IRR of about 12.8%. At a 12% cost of capital, the IRR rule gives no usable answer for Project 1; NPV does.

*Case 2 — scale.* Project A: −$1,000,000 then $350K, $450K, $600K, $750K → NPV $467,937, IRR 33.66%. Project B: −$10,000,000 then $3.0M, $3.5M, $4.5M, $5.5M → NPV $1,358,664, IRR 20.88%. IRR picks A ("bigger bang for the buck, more margin for error"); NPV picks B ("creates more dollar value"). Profitability index: A = 467,937/1,000,000 = 46.79%; B = 1,358,664/10,000,000 = 13.59%. Under capital rationing, A wins. With money to spare, B wins. The worry with A is whether the leftover $9 million can be reinvested at comparable returns; the worry with B is the thin margin if the cost of capital is misestimated.

*Case 3 — timing at equal scale.* Both projects invest $10,000,000. Front-loaded A: $5.0M, $4.0M, $3.2M, $3.0M → NPV $1,191,712, IRR 21.41%. Back-loaded B: $3.0M, $3.5M, $4.5M, $5.5M → NPV $1,358,664, IRR 20.88%. IRR favors A, NPV favors B. The cause is purely the reinvestment assumption.

*MIRR.* Invest $1,000, receive $300, $400, $500, $600 over four years at a 15% hurdle rate. Reinvested forward: 300(1.15)³ = $456; 400(1.15)² = $529; 500(1.15) = $575; 600 = $600. Terminal value = $2,160. Ordinary IRR = 24.89%. MIRR solves 1,000(1+r)⁴ = 2,160 → 21.23%. The 3.7-point gap is the reinvestment illusion.

**Determinism:** DETERMINISTIC — NPV, IRR (all roots), NPV profiles, MIRR, and the profitability index are all computable from a cash flow stream and a hurdle rate. A script can also count sign changes and flag multiple-IRR risk automatically. JUDGMENT — deciding whether capital is genuinely rationed, whether the projects really are mutually exclusive, and which rule the firm should adopt. That judgment needs the firm's access to capital, its pipeline of positive-NPV projects, and the reliability of its cash flow forecasts.

**Pitfalls:**
- Quoting an IRR on a stream with a large negative terminal cash flow (decommissioning, cleanup, restoration) without checking for a second root.
- Using IRR to rank projects of very different scale.
- Believing the IRR is achievable when the project is long-lived and the IRR is far above the hurdle rate. In that case IRR overstates the true return.
- Applying the profitability index when capital is *not* rationed, which biases the firm toward small projects and leaves value on the table.
- Treating self-imposed borrowing limits as an immovable constraint. Nearly 70% of rationing is internal management policy.

**Sources:**
- corporate_finance--lecture_slides--cfpacket1spr20 p.249
- corporate_finance--lecture_slides--cfpacket1spr20 p.283-298
- corporate_finance--lecture_slides--cfpacket1spr20 p.303-304

**Related:** [[npv-and-irr-mechanics]], [[comparing-projects-different-lives]], [[time-value-and-cash-flow-timing]], [[uncertainty-payback-sensitivity-simulation]], [[project-options]], [[investment-analysis-first-principles]]
