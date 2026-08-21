# Definitional tests: anatomy and consistency of a multiple

**Core idea:** A multiple is a standardized price: what you pay divided by what you get. Before using one, pass two definitional tests. Consistency: the numerator and denominator must belong to the same claimholders. Equity value goes with equity earnings or equity book value; firm/enterprise value goes with operating measures. Price/EBITDA mixes claims and is inconsistent. Uniformity: every variable must be estimated the same way across all firms in the comparable list, including accounting rules. The same name ("PE") hides many variants, so you must know how any borrowed multiple was built.

**Formulas:**
- Multiple = Numerator (price paid) / Denominator (what you get in return).
- Firm Value = Market value of equity + Market value of debt.
- Enterprise Value (EV) = Market value of equity + Market value of debt − Cash. (EV prices only the operating assets.)
- Invested Capital = Book value of equity + Book value of debt − Cash.
- PE = Market price per share / Earnings per share.
- EV/EBITDA = (MV equity + MV debt − Cash) / EBITDA.

Numerator choices: market value of equity; firm value; enterprise value. Denominator families: revenues (or drivers: users, subscribers, units); earnings (net income/EPS for equity, EBIT for the firm); cash flow (net income + depreciation or FCFE for equity; EBITDA or FCFF for the firm); book value (equity book value; firm book value; invested capital).

**Procedure:**
1. Classify the numerator: equity, firm, or enterprise value.
2. Classify the denominator by claimholder. Reject or restate mismatches (Proposition 1): equity value ÷ equity measure; firm value ÷ firm measure.
3. Pin down the timing variant. For PE: current PE (last fiscal year EPS), trailing PE (trailing 12 months), forward PE (next-year forecast), or a future-year PE. Never mix variants across firms.
4. Pin down the share-count convention for per-share multiples. Options are equity claims: primary EPS ignores them, fully diluted counts all of them, partially diluted counts in-the-money ones. None is perfect — value options separately if they are material; fully diluted is the rough second best.
5. For EV multiples, net cash out of the numerator. Reason: interest income from cash is not in EBITDA or EBIT, so leaving cash in creates a mismatch.
6. Adjust for cross holdings. Consolidated but partly-owned subsidiaries put 100% of EBITDA in the denominator while you own only part of the equity — correct for minority interests. Passive holdings pose the mirror problem.
7. Confirm every comparable's multiple was estimated with the same rules (uniformity).

**Reference data:** none required; the tests are structural.

**Worked example:** A housing-bubble gauge divides house price by annual net rental income. House price is the value of the whole asset (like EV). Net rental income is income after operating expenses but before depreciation (like EBITDA). The closest stock-market analog is therefore EV/EBITDA — a consistency classification in action.

**Determinism:** DETERMINISTIC: computing firm value, EV, invested capital, and any multiple from market values, book values, cash, and the chosen denominator. JUDGMENT: classifying consistency, choosing the timing and dilution variant, and deciding how to fix cross-holding distortions.

**Pitfalls:**
- Price/EBITDA and similar claimholder mismatches.
- Comparing a trailing PE to a forward PE across firms.
- Ignoring option overhang in per-share multiples for option-heavy firms; the share-count convention changes cross-firm rankings.
- Leaving cash in EV while excluding interest income from the denominator.
- Ignoring minority interests in consolidated EV/EBITDA.

**Sources:**
- valpacket2spr21 p.6, p.8-12
- valpacket2spr20 p.6, p.8-12

**Related:** [[four-step-multiple-framework]], [[multiple-distribution-statistics]], [[intrinsic-multiple-derivation]], [[cross-holdings]], [[employee-options]]
