# Deriving the intrinsic version of any multiple

**Core idea:** Every multiple is a DCF valuation in compressed form. Embedded in it are the same drivers — growth, risk, and cash-flow generation — that drive intrinsic value (Proposition 2). You can recover them mechanically. Start with a simple intrinsic value model. Divide both sides by the denominator of the multiple you care about. What remains is the "intrinsic" or "justified" version of that multiple, written as a function of a few fundamentals. Use an equity DCF (dividends or FCFE) for equity multiples. Use an operating-asset DCF (FCFF) for enterprise-value multiples. The driver that matters most for a given multiple is its **companion variable**. That is the variable you must control for when you compare the multiple across firms. Fundamentals almost never move a multiple in a straight line. Hence Proposition 3: you cannot compare firms on a multiple without knowing how the multiple and its fundamentals move together.

**Formulas:**

The three-step recipe:
1. Value model: equity multiples start from `P = Dividends₁/(ke − g) = Net Income₁ × (1 − RIR_equity)/(ke − g)`; EV multiples start from `EV = FCFF₁/(WACC − g) = EBIT₁(1 − t)(1 − RIR)/(WACC − g)`.
2. Divide both sides by the multiple's denominator.
3. Read off the drivers.

Master map of intrinsic multiples (all in stable growth; subscript 1 = next year):

Equity side
- `P/Div₁ = 1/(ke − g)`  → Dividend yield = f(ke, g)
- `P/E₁ = Payout/(ke − g)` (equivalently `(1 − RIR_equity)/(ke − g)`) → PE = f(ke, g, Payout)
- `P/Book Equity = ROE × Payout/(ke − g)` → PBV = f(ROE, ke, g, Payout)
- `P/Sales₁ = Net Margin × Payout/(ke − g)` → PS = f(Net Margin, ROE, ke, g, Payout)
- Identities: `Net Income₁ = Net Margin × Sales = ROE × Book Equity = Net Income₀(1+g)`

Enterprise side
- `EV/FCFF₁ = 1/(WACC − g)`
- `EV/EBIT₁(1−t) = (1 − RIR)/(WACC − g)`
- `EV/EBIT₁ = (1 − t)(1 − RIR)/(WACC − g)`
- `EV/Sales₁ = ATOM × (1 − RIR)/(WACC − g)`
- `EV/IC = ROIC × (1 − RIR)/(WACC − g)`
- Identities: `EBIT₁(1−t) = ATOM × Sales = ROIC × IC = EBITDA₁(1−t) + t × DA`

Symbol definitions
- ke = cost of equity; WACC = cost of capital; g = expected growth rate; t = tax rate.
- Payout = Dividends/Net Income; RIR_equity = 1 − Payout (or 1 − FCFE/Net Income).
- ROE = Net Income₁ / Book Equity₀; Net Margin = Net Income/Sales.
- IC (invested capital) = Book Equity + Debt − Cash; ROIC = EBIT₁(1−t)/IC.
- ATOM (after-tax operating margin) = EBIT(1−t)/Sales.
- RIR (reinvestment rate) = (Cap Ex − DA + ΔWorking Capital)/EBIT(1−t); also `RIR = g/ROIC` in steady state.
- DA = depreciation and amortization.

Two illustrative derivations (both editions use these as the teaching examples):
- `Price = EPS × Payout/(r − g)`; divide by book value per share → `Price/Book = ROE × Payout/(r − g)`.
- `EV = EBIT(1−t)(1 − RIR)/(WACC − g)`; divide by sales → `EV/Sales = ATOM × (1 − RIR)/(WACC − g)`.

**Procedure:**
1. Classify the multiple as equity or enterprise (see [[multiple-definition-tests]]).
2. Pick the matching value model: DDM/FCFE for equity, FCFF for enterprise. Use the stable-growth form for a first pass; use the two-stage form if the firm has a distinct high-growth phase.
3. Divide the model by the multiple's denominator and simplify using the identities above.
4. Name the companion variable — the driver that appears in the numerator of the resulting expression and dominates cross-sectional differences:
   - PE → expected growth (with payout and cost of equity as secondary controls)
   - PEG → risk, payout, and the *level* of growth
   - PBV → ROE
   - EV/Invested Capital → ROIC
   - EV/Sales (or PS) → after-tax operating margin (net margin for PS)
   - EV/EBITDA → reinvestment needs (Cap Ex/EBITDA), tax rate, cost of capital
5. Plug the firm's fundamentals into the intrinsic formula to get a justified multiple, and compare it to the traded multiple. Alternatively, use the companion variable as the control variable in a peer or market regression ([[sector-regressions]], [[market-wide-regressions]]).
6. Never assume linearity: check the shape of the relationship (see the sensitivity results in [[intrinsic-pe-fundamentals]] and [[peg-ratio]]) before extrapolating.

**Reference data:** none. The map above is the lookup table.

**Worked example:** Take a firm with ROE = 15%, payout = 40%, cost of equity = 9%, stable growth = 4%. Intrinsic PE = 0.40 × 1.04/(0.09 − 0.04) = 8.32. Intrinsic PBV = 0.15 × 0.40 × 1.04/(0.09 − 0.04) = 1.25. The short form (ROE − g)/(r − g) gives (0.15 − 0.04)/(0.09 − 0.04) = 2.20 instead. The two forms disagree because the inputs are internally inconsistent. Sustainable growth here is (1 − 0.40) × 15% = 9%, not 4%. Reconcile payout, ROE and growth first. This is the routine trap the derivation exposes.

**Determinism:** DETERMINISTIC — given ROE (or ROIC), payout (or RIR), margin, growth, tax rate and discount rate, every intrinsic multiple above is a closed-form calculation. JUDGMENT — choosing which value model applies (stable vs. two-stage, equity vs. firm), estimating the fundamentals themselves, and ensuring internal consistency between growth, payout/reinvestment and return (g = (1 − Payout) × ROE, or g = RIR × ROIC).

**Pitfalls:**
- Assuming the multiple/fundamental relationship is linear. It is not, and the non-linearity is what defeats naive screens.
- Deconstructing an equity multiple with a firm-level model or vice versa.
- Feeding in growth, payout and return assumptions that violate g = (1 − Payout) × ROE or g = RIR × ROIC, producing a "justified" multiple that no firm could sustain.
- Treating the intrinsic multiple as the answer rather than as the map of what to control for.

**Sources:**
- valpacket2spr21 p.20-21, p.51
- valpacket2spr20 p.20-21, p.51

**Related:** [[four-step-multiple-framework]], [[intrinsic-pe-fundamentals]], [[peg-ratio]], [[book-value-multiples]], [[ev-ebitda-multiple]], [[ev-sales-and-brand-value]], [[sector-regressions]], [[market-wide-regressions]], [[dcf-valuation]], [[expected-growth-fundamentals]]
