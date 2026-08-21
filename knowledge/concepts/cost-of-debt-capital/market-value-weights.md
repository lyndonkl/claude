# Market-value weights in the cost of capital

**Core idea:** The debt and equity weights in the cost of capital must be market values, not book values. The cost of capital is the rate a firm has to earn today to satisfy the people who hold claims on it today. What it would cost to buy out those claims today is their market value. Book values record what was paid in the past. Damodaran rebuts three common arguments for book weights and treats all three as specious. The key practical consequence: because market equity usually far exceeds book equity while market debt sits near book debt, book-value weights typically assign MORE weight to debt — which lowers the computed cost of capital and is anti-conservative, the opposite of what its defenders claim.

**Formulas:**
- Equity weight = E / (D + E + PS); Debt weight = D / (D + E + PS); Preferred weight = PS / (D + E + PS).
  - E = market value of common equity = shares outstanding × current share price.
  - D = market value of debt = estimated market value of interest-bearing debt + debt value of operating leases + straight-debt component of convertibles.
  - PS = market value of preferred stock = preferred shares × preferred price.
- Cost of capital = k_e × E/(D+E+PS) + k_d × (1 − t) × D/(D+E+PS) + k_ps × PS/(D+E+PS).
- Net-debt convention (if used): weights must use NET debt everywhere the beta was levered with net debt. Net debt = Debt − Cash.

**Procedure:**
1. Compute market equity: shares outstanding × current price. Add the equity portion of any convertible ([[convertible-debt-decomposition]]).
2. Compute market debt ([[market-value-of-debt]]) and add capitalized operating leases ([[operating-leases-as-debt]]).
3. Compute market preferred, if material ([[preferred-stock-cost]]).
4. Divide each by the total to get weights. They sum to 1.
5. Use the SAME weights that were used to lever the beta. If the beta was levered at D/E = 13.10%, the cost-of-capital debt ratio must be 13.10% / 113.10% = 11.58%.
6. If you used net debt to lever the beta, use net debt in the weights. Mixing conventions breaks the model.
7. For a private firm with no market equity, assume the industry median market D/E ratio rather than the firm's book ratio.
8. As a diagnostic, recompute the cost of capital with book weights and note the difference. It is usually lower with book weights, which shows why the choice matters.

**Reference data:** The three specious arguments for book-value weights and their rebuttals.

| Argument for book weights | Rebuttal |
|---|---|
| "Book value is more reliable because it is less volatile than market value." | The stability is a weakness, not a strength. A book value that does not update is not tracking anything real. |
| "Using book value is more conservative than using market value." | False for most companies. Book-value weights put MORE weight on debt, and after-tax debt is the cheaper component, so the cost of capital comes out LOWER — the opposite of conservative. |
| "Since accounting returns are computed on book value, consistency requires book-value weights." | It is only apparent consistency. Matching two book numbers makes no economic sense as a required return. |

Discussion-question framing from the valuation packet: the reason to use market values is NOT that "the market is usually right", NOT that "market values are easy to obtain", and NOT that "book values are meaningless". It is that a buyer would have to pay market values today to acquire the claims, so market values reflect the current cost of raising capital — whether or not the market is right.

Application-test rules from the packet: if the average debt maturity is unavailable, use 3 years; always capitalize operating leases and add them to BOTH book and market value of debt; then compute the weights on both bases and compare.

**Worked example:** Disney, 2013 ($ millions).
- Market equity = $121,878. Market debt = $13,028 (interest-bearing, converted from a $14,288 book value) + $2,933 (capitalized operating leases) = $15,961.
- Total capital = $137,839. Equity weight = 121,878 / 137,839 = 88.42%. Debt weight = 15,961 / 137,839 = 11.58%.
- Cost of capital = 8.52% × 0.8842 + 2.40% × 0.1158 = **7.81%**.

Contrast, Embraer 2004 (millions of BR): market equity 11,042 versus book equity 3,350; market debt 2,083 versus book debt 1,953. Market weights are 84% equity / 16% debt. Book weights would have been 3,350 / (3,350 + 1,953) = 63% equity / 37% debt. With a 10.70% cost of equity and a 6.13% after-tax cost of debt, market weights give 9.97% and book weights would give 9.01% — nearly a full point lower, purely from the weighting choice.

**Determinism:**
- DETERMINISTIC: shares, price, market debt, preferred → weights → weighted-average cost of capital. Fully scriptable.
- JUDGMENT: what goes into D and E in the first place — lease capitalization, convertible splitting, preferred materiality, gross versus net debt. Those classification decisions live in [[what-counts-as-debt]].
- JUDGMENT: the D/E ratio for a private firm or a division with no observable market equity. The packet's rule is the industry median market D/E; that needs a comparable set.
- JUDGMENT: whether to use the current debt ratio or a target/optimal debt ratio when the firm is visibly moving toward a new capital structure.

**Pitfalls:**
- Using book weights because they are on the balance sheet already.
- Using market equity but book debt, which is an inconsistent hybrid.
- Forgetting capitalized leases in the debt weight after including them in the debt value elsewhere in the model.
- Levering the beta at one D/E and weighting the WACC at a different one.
- Mixing gross-debt levering with net-debt weights, or the reverse. The cost of equity looks lower under net debt, but the cost of capital roughly evens out only if the weights are net too.
- Using a private firm's book D/E as its market D/E.

**Sources:**
- corporate_finance--lecture_slides--cfpacket1spr20 p.195, p.199-200, p.203
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.110-111, p.115
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.107-108, p.112
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.98 (net-debt consistency requirement)
- corporate_finance--lecture_slides--cfpacket1spr20 p.180 (private firm assumes the industry median market D/E)
- spreadsheet doc `valuation-inputs-1` — wacccalc.xls total capital E62 and weights row 63

**Related:** [[market-value-of-debt]], [[what-counts-as-debt]], [[operating-leases-as-debt]], [[preferred-stock-cost]], [[convertible-debt-decomposition]], [[cost-of-capital-assembly]], [[net-debt-vs-gross-debt]], [[levered-beta]], [[optimal-capital-structure]]
