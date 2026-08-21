# Life-cycle view of dividend capacity

**Core idea:** A firm's capacity to pay dividends is a function of where it sits in its life cycle, not of management preference. Early on, funding needs are large and internal cash flow is negative or small, so there is nothing to pay out. As the firm matures, projects dry up, internal financing exceeds funding needs, and payout capacity rises. In decline, internal cash flow far exceeds funding needs and payout should be high. The practical consequence: dividend policy is not a fixed attribute of a company. It must change as the company ages, and a mismatch between life-cycle stage and payout is the single most common dividend pathology.

**Formulas:**
- Payout capacity in any stage ≈ Internal financing (cash from operations after reinvestment) − External funding needs. Positive and growing capacity is what makes dividends feasible.
- The quantitative version of "capacity" is FCFE — see [[fcfe-potential-dividends]]: FCFE = Net Income − (Cap Ex − Depreciation) − ΔNon-cash Working Capital + (New Debt Issued − Debt Repaid).
- Sustainable growth link: Expected growth in net income = Retention ratio × Return on Equity = (1 − Payout Ratio) × ROE. A firm cannot simultaneously promise high growth and a high payout unless its ROE is very high.

**Procedure:**
1. Place the firm in one of the five stages using revenue growth, earnings sign and level, reinvestment relative to earnings, and access to external capital. Use the table below.
2. Verify with FCFE. A firm in stages 1–3 will typically have negative or small FCFE; stages 4–5 produce large positive FCFE. If the stage label and the FCFE sign disagree, trust FCFE and re-examine the stage call.
3. Set a payout norm from the stage: Stage 1 and 2 → zero payout. Stage 3 → very low (token) payout at most. Stage 4 → increasing payout, and this is where dividend initiation belongs. Stage 5 → high payout, including return of capital via large buybacks or special dividends.
4. Cross-check the norm against the expected-growth benchmark table below. A firm with 20%+ expected growth that pays out 40% of earnings is either mislabeled or misfinancing itself.
5. Where growth is uncertain, prefer buybacks to dividends. Buybacks carry no stickiness commitment (see [[dividend-empirical-facts]]), so a stage-3-to-4 firm can return cash without locking in a permanent obligation.
6. Re-run the stage assessment each year. The classic failure is a stage-5 firm still paying stage-3 dividends (hoarding cash), or a stage-2 firm initiating dividends to widen its investor base (see [[managing-dividend-changes]]).

**Reference data:**

*Life-cycle stages and dividend capacity (Figure 10.7):*

| Stage | External funding needs | Internal financing | Capacity to pay dividends |
|---|---|---|---|
| 1. Start-up | High, but constrained by infrastructure | Negative or low | None |
| 2. Rapid Expansion | High, relative to firm value | Negative or low | None |
| 3. High Growth | Moderates, relative to firm value | Low, relative to funding needs | Very low |
| 4. Mature Growth | Low, as projects dry up | High, relative to funding needs | Increasing |
| 5. Decline | Low, as projects dry up | More than funding needs | High |

Across the cycle: revenues and earnings rise, flatten, then fall; external funding needs shrink; internal financing grows.

*Empirical confirmation — US firms sorted by expected growth rate (approximate values read from the chart):*

| Expected growth class | Dividend payout ratio | Dividend yield |
|---|---|---|
| 0–3% | ~44% | ~3.75% |
| 3–5% | ~39% | ~3.25% |
| 5–10% | ~40% | ~3.0% |
| 10–15% | ~35% | ~2.4% |
| 15–20% | ~20% | ~1.1% |
| 20–25% | ~21% | ~1.35% |
| >25% | ~20% | ~1.1% |

Payout and yield both fall monotonically (with noise) as expected growth rises — exactly what the life-cycle story predicts.

**Worked example:** Baidu in the 2013 case set. Expected growth is high, reinvestment is heavy, and the firm is in stage 2/3. Its dividend yield is 0.00% and its payout ratio is 0.00%, both in the trailing year and over 2008–2012. Its peer group (global online advertising) has a group yield of 0.09% and a group payout of 8.66%. The life-cycle model says this is correct behavior, not a deficiency — and the fact that Baidu still generates positive FCFE with good projects is what earns it "maximum flexibility" in [[dividend-matrix]]. Contrast Vale, a mature/declining cyclical: payout 113.45% trailing, yield 6.56% — a stage-5 payout profile, which is defensible in principle but exceeded its FCFE in practice.

**Determinism:**
- DETERMINISTIC: given expected growth, the benchmark payout and yield are a table lookup. Given financial statements, FCFE and the payout ratio are computable, and the sign of FCFE is a mechanical stage cross-check.
- JUDGMENT: assigning the life-cycle stage itself. This requires reading the business — the durability of growth, whether the reinvestment is genuine growth investment or maintenance, whether the industry itself is in decline, and how long the growth period will last. The chart values are approximate and are meant as anchors, not targets.

**Pitfalls:**
- Treating dividend policy as a permanent corporate attribute. The mature firm that never raises its payout accumulates the cash pile that invites activists (see the Chrysler and Microsoft cases in [[cash-trust-assessment]]).
- Initiating a dividend at a high-growth firm to widen the investor base. With negative FCFE the dividend must be funded by issuing stock or by underinvesting.
- Confusing high current earnings with maturity. A cyclical peak is not stage 5.
- Reading the growth-class table as causal. Low payout does not cause growth; both reflect where the firm is in its life.
- Ignoring that the benchmark table covers dividends only. High-growth firms that buy back stock look lower-payout than they are.

**Sources:**
- corporate_finance--lecture_slides--cfpacket2spr20 p.161-163

**Related:** [[dividend-payout-and-yield-measures]], [[fcfe-potential-dividends]], [[dividend-empirical-facts]], [[dividend-matrix]], [[managing-dividend-changes]], [[market-regression-payout-prediction]]
