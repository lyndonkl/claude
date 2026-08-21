# The PEG ratio and why it does not neutralize growth

**Core idea:** PEG divides the PE ratio by the expected growth rate in earnings per share. It is the classic "modified multiple": an attempt to control for one dimension of difference (growth) inside the multiple itself. It fails at that job. Dividing by growth does not strip growth out, because value is a non-linear function of growth. Risk and payout still drive PEG, exactly as they drive PE. Empirically PEG falls as growth rises, so PEG screens systematically flag high-growth firms as cheap. PEG also falls sharply with beta, so the "cheapest" PEG stock in a sector is often just the riskiest one.

**Formulas:**
- `PEG = PE ratio / expected growth rate in EPS`. By convention the growth rate is entered in percentage points (25% growth → divide by 25), so a PE of 28.75 with 25% growth gives PEG 1.15.
- Intrinsic PEG, from the two-stage dividend discount model divided by earnings and again by g:
```
PEG = Payout × (1+g) × [1 − (1+g)^n/(1+r)^n] / [g(r − g)]
    + Payout_n × (1+g)^n × (1+gn) / [g(r − gn)(1+r)^n]
```
Symbols:
- Payout = payout ratio in the high-growth phase; Payout_n = stable-phase payout.
- g = expected high-growth rate in EPS; gn = stable growth rate; n = years of high growth.
- r = cost of equity.

**Procedure:**
1. Match the growth rate to the EPS basis of the PE. A forward PE needs forward growth. Use the same time horizon for both.
2. Compute PEG for the firm and for every comparable, on the same basis.
3. Before reading a low PEG as cheap, run the three checks that follow from the propositions below.
4. Risk check: is the firm's beta or standard deviation above the peer group's? Higher-risk firms deserve lower PEG.
5. Growth-quality check: how much reinvestment buys the growth? Compute the retention (or reinvestment) rate. Firms that generate the same growth with less reinvestment deserve *higher* PEG.
6. Growth-level check: is the firm's growth rate far from the peer average? Very low-growth and very high-growth firms both carry structurally higher PEGs, with the bias worse at the low end.
7. If differences remain on more than one dimension, drop PEG and regress instead. Regress PEG on beta, payout and ln(growth) — the log form is the standard fix for the non-linearity.
8. Compare the actual PEG to the regression-predicted PEG rather than to a peer average.

**Reference data:**

Three propositions on PEG (both editions):
- Proposition 1 — High-risk companies trade at much lower PEG ratios than low-risk companies with the same expected growth. Corollary: the firm that looks most undervalued on PEG in a sector may simply be the riskiest.
- Proposition 2 — Companies that attain growth more efficiently (less reinvestment, higher project returns) have higher PEG ratios. Corollary: firms that look cheap on PEG may have high reinvestment rates and poor project returns.
- Proposition 3 — Companies with very low or very high growth tend to have higher PEG ratios than average-growth firms; the bias is worse for low-growth stocks. PEG does not neutralize growth.

Intrinsic PEG sensitivities (base case: 5 years of growth g, then 8%; payout 20% then 50%):

| Beta | PEG at g=25% | g=20% | g=15% | g=8% |
|---|---|---|---|---|
| 0.75 | ~2.0 | ~2.2 | ~2.5 | ~3.0 |
| 1.00 | ~1.15 | ~1.3 | ~1.4 | ~1.7 |
| 1.50 | ~0.6 | ~0.7 | ~0.8 | ~1.0 |
| 2.00 | ~0.4 | ~0.45 | ~0.5 | ~0.6 |

PEG against retention ratio (same base case): retention 1.0 → PEG ≈ 1.08; retention 0 → PEG ≈ 1.32. Lower reinvestment for the same growth means a higher deserved PEG.

PEG against expected growth is U-shaped: at r = 6%, PEG ≈ 2.45 at g = 5%, falls to a minimum near 1.15 at g ≈ 20-30%, then edges up at very high growth. The whole curve shifts down as required returns rise (at r = 10% it sits near 0.5 across most of the range).

US PEG regression, January 2021 (all US stocks; dependent variable PEG):
`PEG = 5.626 + 0.004 × Payout ratio − 0.660 × ln(Growth) − 1.138 × Beta`

| Predictor | B | Std. Error | t | Sig. |
|---|---|---|---|---|
| Constant | 5.626 | 0.321 | 17.521 | .000 |
| Payout ratio | 0.004 | 0.001 | 3.294 | .001 |
| ln(Growth) | −0.660 | 0.114 | −5.799 | .000 |
| Beta | −1.138 | 0.170 | −6.696 | .000 |

R = 0.341, R² = 0.116, adjusted R² = 0.113, std. error 1.910. Payout enters in absolute percent units in this output.

Fit evidence for the log transform: regressing PEG on raw expected growth gives R² = 0.022 across US stocks; using ln(growth) raises it to 0.053. Both slopes are clearly negative. Even so, R² near 0.12 means fundamentals explain far less of PEG than of PE.

(The January 2020 edition ran a slightly different US PEG specification: `PEG = 1.036 − 1.515 × Beta + 1.362 × Payout + 0.898 × Net Profit Margin − 1.079 × ln(Growth)`, R² = 0.454. Use the 2021 form as canonical; note only that the signs on beta and ln(growth) are negative in both years.)

Regional PEG regressions, January 2021 (beta, payout, and ln of expected EPS growth):

| Region | Regression | R² |
|---|---|---|
| US | PEG = 5.63 − 1.14 Beta + 0.40 Payout − 0.66 ln(g_EPS) | 11.3% |
| Europe | PEG = 6.88 − 0.88 Beta + 0.20 Payout − 1.26 ln(g_EPS) | 27.1% |
| Japan | PEG = 6.66 − 0.62 Beta + 0.60 Payout − 1.21 ln(g_EPS) | 33.2% |
| Emerging Markets | PEG = 4.98 − 0.32 Beta + 0.10 Payout − 0.91 ln(g_EPS) | 20.2% |
| Australia, NZ, Canada | PEG = 6.68 − 0.67 Beta + 0.50 Payout − 1.36 ln(g_EPS) | 27.2% |
| Global | PEG = 5.73 − 2.57 Beta + 0.10 Payout − 0.69 ln(g_EPS) | 13.0% |

**Worked example:** Same firm as the intrinsic PE case. High growth 25% for 5 years with 20% payout, then 8% growth with 50% payout, beta 1.00, riskfree 6%, ERP 5.5%, so r = 11.5%.
```
PEG = 0.2 × 1.25 × [1 − 1.25^5/1.115^5]/[0.25 × (0.115 − 0.25)]
    + 0.5 × 1.25^5 × 1.08/[0.25 × (0.115 − 0.08) × 1.115^5]
    = 1.15
```
That is the intrinsic PE of 28.75 divided by growth of 25 percentage points. A sector peer with the same 25% growth but beta 2.00 would justify a PEG near 0.4. Calling that peer "cheap" on PEG would be a pure risk illusion.

**Determinism:** DETERMINISTIC — the intrinsic PEG from payout, g, gn, n and r; the predicted PEG from any of the regressions above; the actual PEG from PE and a growth forecast. JUDGMENT — the growth forecast itself, whether the growth horizon matches the PE basis, and whether an observed PEG gap reflects risk, reinvestment efficiency, growth level, or genuine mispricing.

**Pitfalls:**
- Treating PEG as growth-neutral. It is not, and the bias runs against low-growth firms.
- Screening on "PEG below 1" — that screen loads on high risk and on mid-to-high growth.
- Mixing a trailing PE with a five-year forward growth estimate.
- Comparing PEGs across firms with different reinvestment efficiency; the efficient grower deserves the higher PEG.
- Regressing PEG on raw growth rather than ln(growth), which mis-specifies a clearly non-linear relationship.

**Sources:**
- valpacket2spr21 p.35-41, p.91-93, p.95
- valpacket2spr20 p.35-41, p.89-91

**Related:** [[intrinsic-pe-fundamentals]], [[intrinsic-multiple-derivation]], [[comparable-selection-and-controls]], [[market-wide-regressions]], [[cross-market-multiple-regressions]], [[sector-regressions]], [[expected-growth-fundamentals]]
