# The four-step framework for any multiple

**Core idea:** Damodaran's discipline for using any multiple: run it through four tests — definitional, descriptive, analytical, and application — before trusting it. (1) DEFINE it: the same multiple is defined differently by different users, so check numerator/denominator consistency and uniform estimation across firms. (2) DESCRIBE it: know its cross-sectional distribution, because you cannot judge "high" or "low" without it, and multiples are heavily skewed. (3) ANALYZE it: identify the fundamentals (its "companion variable") that drive it and the — usually non-linear — relationship. (4) APPLY it: define the comparable universe and control for differences, which is far harder in practice than in theory.

**Formulas:** none — this is the organizing checklist. Each step's machinery lives in its own concept.

**Procedure:**
1. Definitional tests: verify claimholder consistency and uniform estimation ([[multiple-definition-tests]]).
2. Descriptive tests: compute median, percentiles, skew; check how many firms drop out because the multiple cannot be estimated ([[multiple-distribution-statistics]]). Use medians, not means.
3. Analytical tests: derive the intrinsic version of the multiple from a DCF model to find its drivers and companion variable ([[intrinsic-multiple-derivation]]). Companion variables: PE → growth (with payout, risk); PBV → ROE; EV/EBITDA → reinvestment needs, tax rate; EV/Sales → operating margin; EV/Invested Capital → ROIC.
4. Application tests: choose the comparable set and control technique ([[comparable-selection-and-controls]]), then compare actual vs. justified multiple.

**Reference data:** none.

**Worked example:** Run PE through the four steps. Define: pick trailing vs. forward, diluted vs. primary EPS. Describe: US median trailing PE was about 20.3 in Jan 2021 while the mean was 103 — skew makes the mean useless. Analyze: PE = f(payout, growth, cost of equity), non-linear in growth. Apply: regress PE on growth and payout across peers or the market, then compare actual PE to predicted PE.

**Determinism:** The framework itself is JUDGMENT (a checklist of analyst obligations). Steps 2 and 3 contain DETERMINISTIC computations once data and model inputs are fixed.

**Pitfalls:**
- Borrowing someone else's multiple without knowing how they estimated it (step 1 skipped).
- Judging a multiple high or low from memory or rules of thumb instead of the current distribution (step 2 skipped).
- Comparing firms on a multiple without knowing how fundamentals move it (step 3 skipped) — Proposition 3: this is impossible to do properly.
- Assuming sector membership equals comparability (step 4 skipped).

**Sources:**
- valpacket2spr21 p.7, p.102
- valpacket2spr20 p.7, p.100

**Related:** [[multiple-definition-tests]], [[multiple-distribution-statistics]], [[intrinsic-multiple-derivation]], [[comparable-selection-and-controls]], [[pricing-vs-value]]
