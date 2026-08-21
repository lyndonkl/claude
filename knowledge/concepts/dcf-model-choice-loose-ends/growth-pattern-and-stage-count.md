# Choosing the growth pattern and the number of stages

**Core idea:** The third DCF choice is the shape of the growth path. A stable-growth (one-stage) model assumes the firm already grows at its perpetual rate. A two-stage model adds a finite high-growth phase that ends abruptly. A three-stage model inserts a transition in which growth, payout, beta and leverage glide to their stable values. The right shape follows from the firm's size, its growth rate relative to the economy, and the strength of its barriers to entry. Two disciplines matter more than the stage count. Do not stretch the high-growth period beyond what the moat can defend. Make the stable phase internally consistent, because most of the value lives there.

**Formulas:**
- Screen: compare the firm's expected growth `g_firm` with the economy's nominal growth `g_econ` (proxied by the riskfree rate or nominal GDP growth).
- Stable-period reinvestment (firm): `Reinvestment Rate = g / ROC`.
- Stable-period payout (equity): `Payout = 1 − g / ROE`.
- Terminal value (firm): `TV_n = EBIT_{n+1}(1 − t)(1 − g/ROC) / (Cost of Capital − g)`.
- Fundamental growth: `g = Reinvestment Rate × Return on Invested Capital + growth from improved efficiency`. In stable growth the efficiency term is dropped.
- Ceiling: `g ≤ g_econ ≈ riskfree rate in the same currency`.

**Reference data — stage-selection rules:**

| Firm characteristics | Model |
|---|---|
| Large and growing at or below the economy's growth rate; or constrained by regulation from growing faster; or already showing stable-firm traits (average risk, average reinvestment) | **Stable growth** (1-stage) |
| Large and growing at a moderate rate: `g_firm ≤ g_econ + 10%`; or a single product protected by a finite-life barrier such as a patent | **Two-stage** |
| Small and growing very fast: `g_firm > g_econ + 10%`; or significant barriers to entry; or firm characteristics far from the norm | **Three-stage / n-stage** |

Stable-phase parameter targets (apply in the terminal period regardless of stage count):

| Parameter | Stable-phase value |
|---|---|
| Beta | Close to 1 (empirical stable range 0.8–1.2) |
| Debt ratio | Close to the industry or mature-company average |
| Country risk premium | Fading over time, especially for emerging-market firms |
| Excess returns | Approaching zero: ROC → cost of capital, ROE → cost of equity |
| Reinvestment / payout | Set by `g/ROC` and `1 − g/ROE`, never carried over from the high-growth phase |

**Procedure:**
1. Estimate the firm's near-term expected growth and the economy's nominal growth in the same currency.
2. Apply the table: at or below `g_econ` → one stage; up to `g_econ + 10%` → two stages; above that → three stages.
3. Override on structure. A single patented product with a known expiry argues for two stages even at high growth. A young firm with strong, broad barriers argues for three.
4. Set the length of the high-growth phase from the competitive advantage, not from convenience. Growth alone creates no value; only growth earning returns above the cost of capital does. The stronger and more sustainable the moat, the longer the phase — and such moats are rare.
5. Resist long high-growth windows for freshly listed growth firms. The evidence shows analysts routinely over-assume both the length of growth and the persistence of excess returns.
6. Build the stable phase to the target table above. Recompute reinvestment as `g/ROC` and payout as `1 − g/ROE`.
7. Cap perpetual growth at the riskfree rate / nominal GDP growth in the cash-flow currency.
8. Let growth mean-revert faster than excess returns. Real revenue growth reliably decays toward GDP growth, while median ROIC has proved sustainable around 8–12% over decades. Zero excess returns in perpetuity is a defensible choice, not a requirement.

**Worked example (terminal-value sensitivity, $100m after-tax operating income in year n+1, 10% cost of capital):**

| Growth forever \ ROC in perpetuity | 6% | 8% | 10% | 12% | 14% |
|---|---|---|---|---|---|
| 0.0% | $1,000 | $1,000 | $1,000 | $1,000 | $1,000 |
| 1.0% | $926 | $972 | $1,000 | $1,019 | $1,032 |
| 2.0% | $833 | $938 | $1,000 | $1,042 | $1,071 |
| 3.0% | $714 | $893 | $1,000 | $1,071 | $1,122 |

Each cell is `100 × (1 − g/ROC)/(0.10 − g)`. Read the ROC = 10% column: when the return on capital equals the cost of capital, terminal value is $1,000 at every growth rate. Growth is value-neutral without excess returns, and value-destroying when ROC < cost of capital.

**Determinism:**
- DETERMINISTIC: the `g_econ + 10%` screen; the stable reinvestment and payout formulas; the terminal-value grid; the growth cap check against the riskfree rate.
- JUDGMENT: the length of the high-growth phase, the strength and durability of competitive advantages, the stable-period ROC/ROE, and how fast country risk fades. This judgment needs industry structure, patent and contract expiries, regulatory constraints, and peer-group return histories.

**Pitfalls:**
- Assuming a long high-growth period with large excess returns because the company is exciting. Growth firms rarely sustain both.
- Setting perpetual growth above the economy's growth rate; the firm eventually becomes larger than the economy.
- The cap-ex-equals-depreciation trick: assuming zero net reinvestment in the terminal year while still claiming positive real growth. Zero net reinvestment supports zero real growth, at best inflation-level nominal growth.
- Leaving a high-growth beta, high-growth debt ratio or high-growth payout in the terminal year.
- Adding stages instead of thinking. A third stage on a mature utility is decoration.

**Sources:**
- valpacket1spr21 p.216
- valpacket1spr20 p.212
- valpacket1spr21 p.204-210 (growth period length, competitive advantage, growth must be earned, TV sensitivity, excess returns, cap-ex sleight of hand, internal consistency)
- valpacket1spr20 p.201-206 (same sequence, 2020 edition)
- valpacket1spr21 p.201 (riskfree rate as growth cap)

**Related:** [[dcf-model-choice-framework]], [[multistage-model-mechanics]], [[discount-rate-cash-flow-matching]], [[terminal-value]], [[stable-growth-inputs]], [[fundamental-growth-rate]], [[excess-returns]]
