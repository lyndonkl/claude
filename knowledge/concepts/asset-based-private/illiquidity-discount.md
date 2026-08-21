# The illiquidity discount

**Core idea:** A buyer of a private business cannot sell it back to a market tomorrow. That lack of an exit is worth something, and the value of the equity has to be reduced for it. Practice collapses this into a rule of thumb — a flat 20% to 30% off every private firm — which Damodaran attacks directly. The discount should vary on three dimensions: the **company** (healthier, larger firms with more liquid assets deserve smaller discounts than small money-losing firms with illiquid assets), the **time** (liquidity is worth more in a bad economy with tight credit than in a boom), and the **buyer** (liquidity is worth more to a buyer with a short horizon and high cash needs than to a long-term holder). Three estimation routes exist, and they give materially different answers on the same firm.

**Formulas:**
- `Final equity value = Equity value from DCF × (1 − Illiquidity discount)`
- Route 1 — fixed discount ("bludgeon"): `Discount = 20% to 30%`, typically 25%. No firm-specific input.
- Route 2 — refined fixed discount (Silber-adjusted): shift a 25% base by the difference between the Silber-predicted discount for the subject firm and for a $10M-revenue profitable anchor. See [[silber-restricted-stock-regression]] for the exact formula.
- Route 3 — bid-ask spread regression: `Discount = 0.145 − 0.0022 ln(Revenues) − 0.015 DERN − 0.016 (Cash/Firm Value) − 0.11 (Monthly trading volume/Firm Value)`. See [[bid-ask-spread-illiquidity-regression]].
- Symbols: `DERN` = 1 if earnings are positive, 0 if negative; revenues in $ millions; trading volume = 0 for a private firm.

**Procedure:**
1. Confirm the discount applies at all. **Decision rule: apply an illiquidity discount only when the buyer cannot exit into a market.** A private-to-private buyer gets one. A publicly traded acquirer does not, because its own investors can sell their shares. An IPO buyer does not.
2. Complete the DCF and get to an equity value *before* any discount.
3. Choose the route:
   - Use the bid-ask spread regression when you have the firm's revenues, profitability and cash position. It is the most firm-specific and the most defensible.
   - Use the Silber-refined base when you want a restricted-stock-anchored number that still varies with size and profitability.
   - Use a flat 20–30% only as a sanity check or when the counterparty expects it.
4. Adjust for the dimensions the chosen model does not capture:
   - **Company**: is it larger/healthier than the model's typical firm? Shrink the discount. Small, money-losing, asset-illiquid? Widen it.
   - **Time**: tight credit and a bad economy raise the discount. Booming markets lower it.
   - **Buyer**: short horizon and high cash needs raise it. A long-term holder with no liquidity needs faces a smaller one.
5. Apply the discount multiplicatively to the equity value.
6. If the stake being valued is a minority stake, a separate lack-of-control discount also applies. See [[minority-discount]]. Do not fold the two together.
7. Report which route you used. The spread between them is large enough to matter to a negotiation.

**Reference data — the three dimensions of variation:**

| Dimension | Smaller discount | Larger discount |
|---|---|---|
| Company | Larger, healthier, profitable, liquid assets | Small, money-losing, illiquid assets |
| Time | Booming markets, easy credit | Bad economy, tight credit |
| Buyer | Long horizon, no cash needs | Short horizon, high cash needs |

**Reference data — pre-computed discounts by revenue** (from `liqdisc.xls`, generated from the Silber-based restricted-stock formula with a 25% base and a 100% block; profitable = DERN 1, unprofitable = DERN 0):

| Revenues ($mm) | Profitable firm | Unprofitable firm |
|---|---|---|
| 5 | 26.26% | 34.21% |
| 10 | 25.00% | 33.15% |
| 15 | 24.25% | 32.52% |
| 20 | 23.71% | 32.07% |
| 25 | 23.29% | 31.72% |
| 30 | 22.94% | 31.42% |
| 35 | 22.64% | 31.17% |
| 40 | 22.39% | 30.96% |
| 45 | 22.16% | 30.77% |
| 50 | 21.95% | 30.59% |
| 100 | 20.59% | 29.45% |
| 200 | 19.19% | 28.27% |
| 300 | 18.35% | 27.57% |
| 400 | 17.75% | 27.06% |
| 500 | 17.28% | 26.67% |
| 1000 | 15.79% | 25.42% |

**Worked example — the restaurant.** Equity value before any discount is $520,990 (revenues $1.2M, positive earnings, cash 5% of firm value, zero trading volume).

| Route | Discount | Value of equity |
|---|---|---|
| Bludgeon (flat) | 25% | 0.521 × 0.75 = **$0.391M** |
| Refined bludgeon (Silber-adjusted 25% base) | 28.75% | 0.521 × 0.7125 = **$0.371M** |
| Bid-ask spread regression | 0.145 − 0.0022 ln(1.2) − 0.015(1) − 0.016(0.05) − 0.11(0) = 12.88% | 0.521 × 0.8712 = **$0.454M** |

The spread between the crudest and the most refined route is $83,000 on a $521,000 business — about 16% of the value. The choice of method is not a rounding decision.

**Determinism:**
- DETERMINISTIC: `{equity value, discount} → discounted value`. Each of the three routes is itself deterministic given its inputs — the flat rate is a constant, and the Silber and bid-ask forms are closed-form functions of revenues, profitability, block size and cash.
- JUDGMENT: whether a discount applies at all (which follows from the buyer type); which route to use; and any overlay for time, buyer horizon or asset liquidity that the regressions do not capture. That judgment needs the buyer's identity and horizon, the credit environment, and the composition of the firm's assets.

**Pitfalls:**
- Applying the same 25% to every private firm regardless of size, health, timing or buyer. That is the practice Damodaran is arguing against.
- Applying an illiquidity discount when the buyer is a public company or when the firm is going public. Neither buyer faces the illiquidity.
- Taking the headline restricted-stock and pre-IPO discounts at face value. Sampling bias inflates them badly — see [[silber-restricted-stock-regression]].
- Stacking discounts carelessly. Illiquidity and lack of control are different frictions, but applying both to the same stake needs a reason, not reflex.
- Applying the discount to firm value rather than to equity value.
- Letting the discount become the negotiation. It is a large, poorly identified number, and both sides know it.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket2spr21 p.129, p.142-143, p.149, p.150, p.152
- valuations--lecture_notes--spring_2020--valpacket2spr20 p.127, p.140-141, p.147, p.148, p.150
- special-private.md — liqdisc.xls, sheets "Restricted Stock Regression", "Bid-Ask Spread", "Sheet2"

**Related:** [[silber-restricted-stock-regression]], [[bid-ask-spread-illiquidity-regression]], [[minority-discount]], [[private-to-private-valuation]], [[private-to-public-sale]], [[private-company-valuation-framework]], [[liquidation-valuation]]
