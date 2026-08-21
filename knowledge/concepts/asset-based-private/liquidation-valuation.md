# Liquidation valuation

**Core idea:** Liquidation valuation asks what you would get from selling a business's assets today, piecemeal, rather than running them as a going concern. Because you are selling into a market rather than operating, it makes more sense to *price* the assets off comparable transactions than to intrinsically value their future cash flows — the buyer's cash flows, not yours, are what matter. For assets with no observable market, book value is the usual fallback proxy or starting basis. If the liquidation is forced or urgent, an additional discount comes off the estimated values, because a seller who must transact now cannot wait for the right buyer. Liquidation value is normally a floor on the value of a healthy business and can become the operative value for a distressed one.

**Formulas:**
- `Liquidation value = [ Σ_i Estimated sale price(Asset_i) ] × (1 − d_urgency) − Liabilities`, where:
  - `Estimated sale price(Asset_i)` = price from comparable recent transactions in that asset class, or book value where no market exists.
  - `d_urgency` = additional fire-sale discount for a forced/urgent liquidation (analyst-set; 0 for an orderly wind-down).
  - `Liabilities` = debt and other claims to be settled out of proceeds, if you want liquidation value of equity rather than of assets.
- Per asset with a market: `Estimated sale price(Asset_i) = Transaction multiple × Scalar_i` (e.g. price per square foot × square feet, or EV/EBITDA of recent divisional sales × division EBITDA).

**Procedure:**
1. Break the business into asset classes that can actually be sold separately (real estate, equipment, receivables, inventory, whole divisions, intangibles with transferable title).
2. For each class, decide the evidence source, in this priority order:
   - Recent arm's-length transactions in similar assets → price directly off them. This is the preferred route.
   - No active market but a reliable carrying amount → use book value as the proxy/basis, flagging it as such.
   - Neither → the asset is probably not separable; consider whether liquidation valuation is the right frame at all.
3. Do **not** build a DCF of each asset for a liquidation. The relevant number is the exit price, not your own present value of holding it.
4. Classify the liquidation as orderly or urgent. If urgent — creditor-forced sale, bankruptcy timetable, tight credit market with few bidders — apply an additional discount on top of the estimated prices. The size is judgment; it grows with asset specificity, thinness of the buyer pool, and shortness of the sale window.
5. Subtract liabilities to get liquidation value of equity.
6. Compare with going-concern value. If liquidation value exceeds going-concern value, the business is worth more dead than alive and the "value" of continuing operations is negative.

**Reference data:** Evidence that anchors the urgency haircut. It is the same evidence base as the marketability discounts, covered fully in [[silber-restricted-stock-regression]].

| Evidence class | Observed discount | Period |
|---|---|---|
| Restricted stock (cannot trade for one year) | 33.75% median (Silber), 35%–35.43% average (Moroney, Maher) | 1969–1990 |
| Pre-IPO transactions, 5 months before offering | 42%–60% median by sub-period | 1980–1997 |

These bracket what "cannot sell freely right now" has cost historically. Damodaran's own critique: strip out sampling bias and the pure illiquidity component may be under 10%.

**Worked example:** United Technologies' six divisions (2009). Price each off its median sector EV/EBITDA multiple — the mechanic a liquidator would use.

| Division | EBITDA ($M) | Sector median EV/EBITDA | Price ($M) |
|---|---|---|---|
| Carrier | 1,510 | 5.25 | 7,928 |
| Pratt & Whitney | 2,490 | 8.00 | 19,920 |
| Otis | 2,680 | 6.00 | 16,080 |
| UTC Fire & Security | 780 | 7.50 | 5,850 |
| Hamilton Sundstrand | 1,277 | 5.50 | 7,024 |
| Sikorsky | 540 | 9.00 | 4,860 |
| **Total** | | | **61,661** |

An urgent liquidation takes a further discount off that $61,661M. An orderly divestiture programme does not.

**Determinism:**
- DETERMINISTIC: given a transaction multiple and a scalar per asset (or a book value), the per-asset price, the sum, the application of a stated urgency discount, and the liability subtraction are all mechanical. Inputs → output: `{asset scalars, transaction multiples, book values, d_urgency, liabilities} → liquidation value`.
- JUDGMENT: which assets are genuinely separable and saleable; which comparable transactions are relevant; whether book value is a defensible proxy for a given asset; and the size of the urgency discount. That judgment needs the transaction record in each asset class, the number of plausible bidders, and the timetable forced on the seller.

**Pitfalls:**
- Running a DCF on each asset in a liquidation. Liquidation is a pricing exercise; intrinsic value of assets you are about to sell is the wrong question.
- Taking book value as the liquidation value. It is a proxy of last resort, and for specialized or obsolete assets it is usually far too high.
- Ignoring the urgency discount when the seller is distressed — the exact situation in which liquidation valuation is most often demanded.
- Adding back going-concern items (brand, assembled workforce, synergies) that do not survive a piecemeal sale.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket2spr21 p.105, p.108, p.112, p.144, p.146
- valuations--lecture_notes--spring_2020--valpacket2spr20 p.103, p.106, p.110, p.142, p.144

**Related:** [[asset-based-valuation-overview]], [[fair-value-accounting-fas157]], [[sum-of-the-parts-pricing]], [[illiquidity-discount]], [[silber-restricted-stock-regression]], [[distressed-firm-valuation]]
