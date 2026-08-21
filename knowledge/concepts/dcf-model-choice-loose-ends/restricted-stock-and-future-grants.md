# Restricted stock and expected future equity grants

**Core idea:** Firms pay employees, and especially top managers, with equity as well as cash. Two questions follow, and they have different answers. How do grants *already made* affect value per share today? How do grants *expected in the future* affect value today? Restricted stock is the easy case on both counts. Past grants are simply shares, so count them in the share count, which lowers value per share. Future grants are compensation, so forecast them as an expense, which lowers cash flows. The same split governs options: past grants are a claim on existing equity, future grants are an operating cost. Getting the split wrong means either ignoring real compensation cost or charging it twice.

**Formulas:**
- Past restricted stock: `Shares outstanding = Common shares issued + Restricted shares already granted`.
- Future grants as an expense: `Grant expense_t = (historical grant value as % of revenues) × Revenues_t`, with the percentage declining as revenues scale.
- Effect on the model: the grant expense reduces the operating margin, hence `EBIT_t`, hence `FCFF_t`, hence value.

**Reference data — where each grant belongs:**

| Grant | Past / outstanding | Expected future |
|---|---|---|
| Restricted stock | Include in the share count (denominator) | Forecast as compensation expense (numerator) |
| Employee options | Value them and subtract from equity ([[employee-option-per-share-approaches]]) | Forecast as compensation expense (numerator) |

**Procedure:**
1. Pull the restricted-stock footnote. Identify shares already granted, whether vested or not.
2. Add already-granted restricted shares to the share count used in the final division.
3. For future grants, compute the value of equity granted in each of the last few years — restricted stock plus options — and express it as a percentage of that year's revenues.
4. Choose a path for that percentage over the forecast horizon. Let it shrink as revenues grow: a young firm granting equity worth 8% of revenues will not still be doing so at ten times the scale.
5. Build the forecast percentage into operating expenses each year. Operating margin falls; cash flow falls; value falls.
6. Check for double counting. Future grants are an expense. Outstanding options are a claim subtracted from equity. Neither should appear in both places.
7. Do not use diluted share counts if you have already subtracted the value of outstanding options — see [[employee-option-per-share-approaches]].

**Worked example:** Consider a firm whose recent equity grants (restricted stock plus options) averaged 6% of revenues, with revenues of $1,000m growing to $5,000m over ten years. A declining path — 6%, 5.5%, 5%, ... trending to 2% by year 10 — produces a grant expense of $60m in year 1 and $100m in year 10. Every one of those dollars reduces operating income, so the reinvestment and cash-flow lines fall accordingly. Contrast the treatment of grants already outstanding. In the XYZ example used throughout this material, 10 million at-the-money options worth $5.42 each are subtracted from equity as $54.2m. The remaining equity is then divided by the **actual** 100 million shares. Past grants hit the bridge; future grants hit the income statement.

**Determinism:**
- DETERMINISTIC: adding granted restricted shares to the share count; applying a stated percentage path to forecast revenues to get the annual grant expense; the resulting margin and cash-flow effects.
- JUDGMENT: the percentage-of-revenues path and how fast it declines. That needs the firm's compensation philosophy, its stage of life, peer-group grant practices, and any stated policy on dilution ceilings.

**Pitfalls:**
- Treating stock-based compensation as a non-cash charge to be added back. It is a real cost — the firm is paying with a claim on itself.
- Forecasting future grants as an expense *and* adding the resulting shares to the count, which charges the same cost twice.
- Holding the grant percentage flat at a young firm's level for a decade, which overstates the drag at scale.
- Ignoring unvested restricted stock on the grounds that it might be forfeited. Vesting probability is a haircut, not a reason to omit.

**Sources:**
- valpacket1spr21 p.242-243, p.253
- valpacket1spr20 p.238-239, p.249

**Related:** [[employee-option-per-share-approaches]], [[valuing-employee-options]], [[equity-value-bridge]], [[multistage-model-mechanics]], [[operating-margin-forecasting]]
