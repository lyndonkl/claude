# Preferred stock in the cost of capital

**Core idea:** Preferred stock is a hybrid. Like debt, it carries a pre-specified dividend that must be paid before any common dividend. Like equity, that dividend is NOT tax deductible, and failure to pay it does not usually trigger default. So it belongs in neither bucket cleanly. Damodaran treats it as a third component of capital with its own cost and its own market-value weight. If the preferred is perpetual — no maturity, fixed dividend — its cost is simply the preferred dividend yield. One practical shortcut: if preferred stock is less than 5% of the firm's total market value, lumping it in with debt makes no meaningful difference to the valuation.

**Formulas:**
- Cost of preferred stock: k_ps = Preferred dividend per share / Market price per preferred share.
  - k_ps = cost of preferred stock (a perpetuity yield).
  - No (1 − t) factor. Preferred dividends are paid from after-tax income.
- Market value of preferred = Number of preferred shares × Market price per preferred share.
- Three-component cost of capital:
  Cost of capital = k_e × E/(D+E+PS) + k_d × (1 − t) × D/(D+E+PS) + k_ps × PS/(D+E+PS)
  - k_e = cost of equity; k_d = pre-tax cost of debt; t = marginal tax rate.
  - E, D, PS = market values of common equity, debt and preferred stock.
- 5% materiality rule: if PS / (D + E + PS) < 5%, folding PS into D is acceptable.

**Procedure:**
1. Find the preferred stock on the balance sheet and in the footnotes: number of shares, stated dividend per share, whether it is cumulative, whether it is convertible, whether it is callable, whether it has a maturity.
2. Get the market price per preferred share. Many preferreds trade; use the traded price, not book value.
3. If the preferred is perpetual and straight: k_ps = annual dividend per share / market price per share.
4. If the preferred has a maturity or a sinking fund, value it like a bond and compute its yield instead of a simple dividend yield.
5. If the preferred is convertible, decompose it the way you decompose a convertible bond: a preferred component plus a conversion option counted as common equity ([[convertible-debt-decomposition]]).
6. Compute PS = shares × price and test materiality: PS / total market capital.
   - ≥ 5% → keep it as a third component with weight PS/(D+E+PS) and cost k_ps.
   - < 5% → lumping with debt is acceptable. Note that you are doing it.
7. Never apply the tax shield to preferred. The (1 − t) factor belongs only to interest.

**Reference data:** No lookup table. The two decision rules:

| Situation | Treatment |
|---|---|
| Perpetual straight preferred, ≥ 5% of firm value | Third component; cost = dividend yield; weight = MV of preferred / total market capital |
| Perpetual straight preferred, < 5% of firm value | Lump with debt (rule of thumb) |
| Preferred with maturity / sinking fund | Value as a bond; use its yield |
| Convertible preferred | Split into a preferred component and a conversion option; option goes to common equity |
| Any preferred | No tax deduction, so no (1 − t) factor |

Model implementation (wacccalc.xls, `Cost of Capital worksheet`): inputs are number of preferred shares (B50), market price per preferred share (B51), and annual preferred dividend per share (B52). Cost of preferred (D64) = B52 / B51. Market value of preferred (D62) = B50 × B51. It enters the total capital base E62 = MV equity + MV debt + MV preferred and gets its own weight D63. In the saved Facebook example B50 = 0, so the preferred weight is zero and the cost of preferred (5/70 = 7.14%) does not affect the WACC. Guard the division when the preferred price is 0.

**Worked example:** A firm has 10 million preferred shares trading at $70 each, paying an annual dividend of $5 per share. Cost of preferred = 5 / 70 = 7.14%. Market value of preferred = 10m × $70 = $700 million. If common equity is worth $8,000 million and debt $1,300 million, total capital is $10,000 million and the preferred weight is 7.0% — above the 5% threshold, so it stays a separate component. With a 9% cost of equity and a 2.4% after-tax cost of debt, the cost of capital = 9% × 0.80 + 2.4% × 0.13 + 7.14% × 0.07 = 7.01%. Folding the preferred into debt instead would have given 9% × 0.80 + 2.4% × 0.20 = 7.68% — a 67 basis point error in the wrong direction, because preferred is far more expensive than after-tax debt.

**Determinism:**
- DETERMINISTIC: dividend and price → cost of preferred; shares and price → market value; the three-component weighted average. A script computes all of it.
- JUDGMENT: whether the preferred is genuinely perpetual and straight. Callability, cumulative arrears, step-up dividends, and conversion features all break the simple yield formula. The judgment needs the preferred's indenture terms.
- JUDGMENT: applying the 5% materiality shortcut when the preferred is close to the line, or when the firm's preferred is unusual (e.g. a distressed firm where preferred trades far below par).

**Pitfalls:**
- Applying a tax shield to preferred dividends. They are not deductible; this is the most common error.
- Using the book value or par value of preferred instead of its market value in the weights.
- Using the stated dividend rate on par instead of the dividend divided by the CURRENT market price. In a distressed firm those differ enormously.
- Ignoring preferred entirely for a firm where it is a large share of capital (common in banks, utilities, and REITs).
- Treating convertible preferred as straight preferred, which puts option value in the wrong bucket.

**Sources:**
- corporate_finance--lecture_slides--cfpacket1spr20 p.194
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.113
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.110
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.118 (preferred dividends subtracted in FCFE)
- spreadsheet doc `valuation-inputs-1` — wacccalc.xls preferred block (B50-B52, D62, D63, D64) and the preferred-price division guard

**Related:** [[convertible-debt-decomposition]], [[cost-of-capital-assembly]], [[what-counts-as-debt]], [[market-value-weights]], [[after-tax-cost-of-debt]], [[fcfe]]
