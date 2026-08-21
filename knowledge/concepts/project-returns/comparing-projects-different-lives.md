# Comparing mutually exclusive projects with different lives

**Core idea:** NPVs of mutually exclusive projects with different lives cannot be compared directly. Raw NPV is biased toward the longer project simply because it accumulates value over more years and ties up capital for longer. Two repairs restore comparability. **Replication** repeats the shorter project until both reach a common horizon. **Equivalent annuities** convert each NPV into a level annual value over that project's own life. IRR needs no life adjustment at all, since it is a rate rather than a total, so under an IRR rule you simply pick the higher IRR.

**Formulas:** Symbols: `NPV` = net present value over the project's own life; `r` = hurdle rate; `n` = project life in years.
- `PV annuity factor: PVAF(r, n) = (1 − (1+r)^(−n)) / r`
- `Equivalent annuity = NPV / PVAF(r, n)`
- Replication: extend the shorter project by repeating its full cash flow stream (including the initial investment at the start of each cycle) until the common horizon is reached, usually the least common multiple of the two lives.

**Procedure:**
1. Confirm the projects are mutually exclusive. If the firm can take both, life differences do not matter — take every positive-NPV project.
2. Compute each project's NPV over its own life at the common hurdle rate.
3. Choose a repair. Replication is intuitive and handles irregular cash flows. Equivalent annuities are faster and handle any pair of lives without finding a common multiple.
4. Replication route: find the common horizon, lay out repeated investment cycles, and compute the NPV of the replicated stream for each project. Pick the higher.
5. Equivalent annuity route: divide each NPV by its own PVAF at the hurdle rate. Pick the higher annuity.
6. Cross-check that both routes give the same ranking. They should.
7. Before replicating, ask whether repetition is realistic. Replication assumes the project can actually be repeated on the same terms — same cost, same margins, same demand.

**Reference data:** PV annuity factors at a 12% hurdle rate (used in the worked example):

| n (years) | PVAF(12%, n) |
|---|---|
| 5 | 3.6048 |
| 10 | 5.6502 |

**Worked example:** Two mutually exclusive projects, both at a 12% hurdle rate.

| | Project A | Project B |
|---|---|---|
| Initial investment | $1,000 | $1,500 |
| Annual cash flow | $400 | $350 |
| Life | 5 years | 10 years |
| NPV | $442 | $478 |
| IRR | 28.7% | 19.4% |

Raw NPV picks B ($478 > $442). That comparison is unfair — B runs twice as long.

*Replication:* repeat A with a second $1,000 investment at year 5, extending $400/year to year 10. NPV of A replicated = $693, versus B's $478. A wins.

*Equivalent annuities:* A = 442 / PVAF(12%, 5) = 442 / 3.6048 = $122.62 per year. B = 478 / PVAF(12%, 10) = 478 / 5.6502 = $84.60 per year. A wins, consistent with replication.

IRR also picks A (28.7% > 19.4%) with no adjustment needed.

**Determinism:** DETERMINISTIC — given NPV, hurdle rate, and life, the equivalent annuity is one division. Given cash flow streams and a common horizon, the replicated NPV is a straight discounting exercise. A script can do both and report the ranking. JUDGMENT — whether replication is realistic, what the true project lives are, and whether the projects are genuinely mutually exclusive. That judgment needs the competitive outlook (will the opportunity still exist in five years?) and the technology's shelf life.

**Pitfalls:**
- Comparing raw NPVs across different lives and quietly favoring the longer project.
- Replicating a project that cannot in fact be repeated — a one-off license, a unique site, a first-mover position.
- Assuming replication happens at unchanged costs and margins when inflation or competition would erode them.
- Forgetting to include the repeated initial investment in the replicated stream.
- Using equivalent annuities on projects whose annual cash flows are wildly irregular without checking the answer against replication.

**Sources:**
- corporate_finance--lecture_slides--cfpacket1spr20 p.299-302

**Related:** [[npv-vs-irr-conflicts]], [[npv-and-irr-mechanics]], [[time-value-and-cash-flow-timing]], [[terminal-value-and-project-life]]
