# Accounting valuation and fair value (FAS 157)

**Core idea:** US and international accounting standards have shifted from historical cost toward "fair value". FAS 157 defines fair value as the price that "market participants" would pay or receive. Crucially it is an **exit** price — the price received to sell an asset or paid to transfer a liability — not an entry price. That definition tilts fair value toward relative valuation, because exit prices come from markets. The standard's hierarchy puts observed market prices at the top and accepts intrinsic value only when market prices are not accessible. Accountants are then asked to back those relative valuations with intrinsic valuations, which creates a split mission and invites reverse engineering: the value is fixed first and the valuation is written afterward.

**Formulas:** No closed-form formula. The operative definition is:
- `Fair value(Asset) = Exit price` = price a market participant would pay to buy the asset from you, at the measurement date, in an orderly transaction.
- `Fair value(Liability) = Transfer price` = price paid to transfer the obligation to another party.
- The measurement hierarchy, in priority order: (1) quoted prices in active markets for identical items; (2) observable inputs for similar items; (3) unobservable inputs, i.e. a model — in practice an intrinsic (DCF) valuation.

**Procedure:**
1. Identify the asset or liability being measured and the market in which it would be exited.
2. Search level 1: is there a quoted price in an active market for the identical item? If yes, that is fair value. Stop.
3. Search level 2: are there observable prices for similar items, or observable inputs (rates, spreads, indices) you can adjust? If yes, price off them.
4. Only if levels 1 and 2 fail, go to level 3 and build an intrinsic valuation — expected cash flows discounted at a risk-adjusted rate.
5. When a level 3 model is used to support a level 1 or level 2 number, check the direction of causation. If the model's assumptions were chosen to reproduce a value already decided, the "valuation" is a rationalization.
6. Report the level used. A balance sheet dominated by level 3 measurements is a balance sheet of opinions.

**Reference data:** FAS 157 measurement hierarchy, as taught:

| Level | Input | Valuation approach it implies |
|---|---|---|
| 1 | Quoted price, active market, identical asset | Pure pricing (relative) |
| 2 | Observable prices/inputs for similar assets | Pricing with adjustment (relative) |
| 3 | Unobservable inputs; entity's own assumptions | Intrinsic (DCF) model |

**Worked example:** The packet gives no single numeric case for FAS 157. The mechanics are the same as any asset-level pricing. Take the UTC Fire & Security division of United Technologies (2009), with $5,575M of capital invested and a 6.03% return on capital. The security sector's best-fitting regression is `EV/Capital = 0.55 + 8.22 × ROC` (R² = 55%). That gives `0.55 + 8.22 × 0.0603 = 1.05`, and a fair value of `1.05 × $5,575M = $5,829M`. This is a level 2 measurement: no quoted price for the division exists, but observable pricing of similar businesses does.

**Determinism:**
- DETERMINISTIC: once the level and the input are fixed, the measurement is arithmetic. A quoted price is read off; a level 2 multiple times a scalar is a product; a level 3 DCF is mechanical given cash flows and a discount rate.
- JUDGMENT: which market is the exit market; whether a market is "active"; whether another asset is "similar"; and every level 3 assumption. That judgment needs the transaction record in the asset class, the depth and recency of quotes, and independent evidence for the model inputs.

**Pitfalls:**
- Reverse engineering: deciding the value first and building the intrinsic valuation to support it. Damodaran names this as the predictable consequence of the split mission.
- Confusing exit price with entry price, or with your own value. Fair value is what a market participant would pay, not what the asset is worth to you.
- Treating level 3 numbers as if they carried level 1 reliability.
- Assuming that "fair value accounting" makes the balance sheet a valuation. It restates assets one at a time and still misses anything that only exists at the business level.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket2spr21 p.105, p.109
- valuations--lecture_notes--spring_2020--valpacket2spr20 p.103, p.107

**Related:** [[asset-based-valuation-overview]], [[liquidation-valuation]], [[sum-of-the-parts-pricing]], [[accounting-balance-sheet]], [[intrinsic-vs-relative-valuation]]
