# Selling a private company to a publicly traded buyer

**Core idea:** When a private firm is sold to a public company, the two sides genuinely see different amounts of risk in the same business. The seller is undiversified and prices total risk. The buyer's investors are diversified and price only market risk. Nothing about the cash flows changes; the discount rate does, and so does the answer. Three things follow. Use the market beta, not the total beta. Use the buyer's tax rate, which can differ from a private owner's. And apply **no illiquidity discount**, because the buyer's investors can sell their shares in a market. The gap between the two values is not an error — it is the bargaining range, and who captures it depends on competition among bidders.

**Formulas:**
- Seller's (private) value: `Cost of equity = Rf + Levered total beta × ERP`, then `Equity value × (1 − Illiquidity discount)`.
- Buyer's (public) value: `Cost of equity = Rf + Levered market beta × ERP`, no illiquidity discount.
- Partially diversified buyer (private equity or VC fund): `Perceived beta = Market beta / ρ_fund`, where `ρ_fund` is the correlation of that fund's portfolio with the market. `0 < ρ_fund < 1` puts the answer between the two extremes.
- `Bargaining range = [Seller's standalone value, Buyer's value]`. The price lands inside it.
- Symbols: `Rf` = riskfree rate; `ERP` = equity risk premium; `ρ` = correlation with the market.

**Procedure:**
1. Run the private-to-private valuation first. That establishes the seller's walk-away value. See [[private-to-private-valuation]].
2. Re-run the discount rate with the **market** beta in place of the total beta. Change nothing else — same D/E, same tax rate handling, same cost of debt, same weights.
3. Check whether the buyer's tax rate differs from the seller's. Public-company tax rates can diverge from a private owner's personal rate, and that changes after-tax cash flows.
4. Set the illiquidity discount to **zero** for the public buyer.
5. Keep the key-person haircut unless the deal keeps the owner. It is a cash-flow fact, not a risk-preference one, so it applies to both parties.
6. Value the business again. The difference is what diversification alone is worth.
7. If the likely bidder is a private equity or venture capital fund rather than a listed corporate, use that fund's portfolio correlation. The value lands between the two poles.
8. Set the asking price inside the range. **Decision rule: the more competing bidders and the less urgent the seller, the closer the price sits to the buyer's value.**
9. Note the seller's strategic implication: to maximize value, find a long-term, well-diversified buyer who does not attribute much of the business to you personally.

**Reference data — the restaurant, private buyer vs public buyer:**

| Input | Private | Public |
|---|---|---|
| Unlevered beta | 2.36 (total) | 1.18 (market) |
| Debt-to-equity ratio | 14.33% | 14.33% |
| Tax rate | 40% | 40% |
| Pre-tax cost of debt | 7.50% | 7.50% |
| Levered beta | 2.56 | 1.28 |
| Riskfree rate | 4.25% | 4.25% |
| Equity risk premium | 4% | 4% |
| Cost of equity | 14.50% | 9.38% |
| After-tax cost of debt | 4.50% | 4.50% |
| Cost of capital | 13.25% | 8.76% |

**Worked example — the restaurant revalued ($000s):**

| Item | Private | Public |
|---|---|---|
| Adjusted EBIT | 370 | 370 |
| Key person discount | 20% | 20% |
| EBIT | 296 | 296 |
| Expected growth rate | 2% | 2% |
| Return on capital | 20% | 20% |
| Reinvestment rate | 10.00% | 10.00% |
| FCFF next year | 163.04 | 163.04 |
| Cost of capital | 13.25% | 8.76% |
| Value of business | 1,449.22 | 2,411.79 |
| − Debt | 928.23 | 928.23 |
| Value of equity | 520.99 | 1,483.56 |
| − Illiquidity discount | 12.88% | 0.00% |
| **Value of equity (final)** | **453.88** | **1,483.56** |

`163.04 / (0.1325 − 0.02) = 1,449.22` and `163.04 / (0.0876 − 0.02) = 2,411.79`. Identical cash flows, 3.3x the equity value. What should the chef ask for — $454,000, $1.484 million, or something in between? Something in between, and where exactly depends on how many buyers are competing and how badly each side wants the deal.

**Determinism:**
- DETERMINISTIC: `{market beta, D/E, tax rate, Rf, ERP, cost of debt} → public buyer's cost of capital → value`, and the whole side-by-side comparison. Also the partially-diversified case, given a correlation.
- JUDGMENT: who the likely buyer actually is; that buyer's portfolio correlation if it is a fund; whether the buyer's tax rate differs; whether the key-person haircut survives the deal structure; and where inside the bargaining range the price lands. That judgment needs the bidder list, the fund's holdings, the tax profiles of both sides, and a read on relative urgency.

**Pitfalls:**
- Carrying the total beta into the buyer's valuation. That hands the entire diversification benefit to the buyer and undervalues the business by a factor of three in this case.
- Applying an illiquidity discount to a public buyer. Its investors have a market.
- Dropping the key-person haircut just because the buyer is diversified. Diversification changes the discount rate, not whether the chef stays.
- Treating a private equity fund like a fully diversified corporate. It sits in between and the correlation of its own portfolio is the right input.
- Quoting one number to both sides. The two valuations are both correct; they answer different questions.
- Assuming the seller captures the spread. With one bidder and an urgent seller, the price sits at the bottom of the range.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket2spr21 p.128, p.150-153, p.170
- valuations--lecture_notes--spring_2020--valpacket2spr20 p.126, p.148-151, p.167

**Related:** [[private-to-private-valuation]], [[total-beta]], [[private-company-cost-of-capital]], [[illiquidity-discount]], [[key-person-discount]], [[private-company-valuation-framework]], [[vc-stage-varying-cost-of-equity]], [[acquisition-valuation]]
