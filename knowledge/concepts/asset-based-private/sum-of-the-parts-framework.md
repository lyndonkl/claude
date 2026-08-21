# Sum-of-the-parts: choosing the approach from your motive

**Core idea:** A multi-business company can be valued piece by piece, either intrinsically or relatively. Which one you should use depends on who you are and what you plan to do. A long-term passive investor is betting that the market has made a mistake and will correct it. That investor should value each division intrinsically, because the whole thesis rests on value the market is missing. An activist or acquirer plans to buy the company, split it, and sell or spin the pieces. That investor should price each division relatively, because the pieces will change hands at market prices, not at intrinsic values. The same analysis with the wrong lens produces a number nobody can transact on.

**Formulas:**
- `Sum-of-the-parts value = Σ_i Value(Division_i) − Value(unallocated corporate costs) + Non-operating assets − Debt and other claims`
- Intrinsic route: `Value(Division_i) = PV of FCFF_i at cost of capital_i` (see [[sum-of-the-parts-dcf]]).
- Relative route: `Value(Division_i) = Multiple_i × Scalar_i`, where `Multiple_i` comes from division *i*'s sector peers (see [[sum-of-the-parts-pricing]]).
- Conglomerate discount: `Conglomerate discount = 1 − (Market enterprise value / Sum-of-the-parts value)`.

**Procedure:**
1. State your motive. It sets the route.
   - Passive long-term investor hunting a mispricing → **intrinsic** sum of the parts.
   - Activist, acquirer, or a board considering a break-up → **relative** (pricing) sum of the parts.
   - A firm preparing a spin-off or divisional sale → relative for the transaction price, intrinsic for the reservation price.
   - A firm testing whether it is being run efficiently → run both, and compare each to the whole-company DCF.
2. Define the parts. Use the company's own reported segments unless you can do better; you need revenues, operating income, capital invested and, ideally, cap ex and depreciation per segment.
3. Deal with what the segments do not contain: unallocated corporate expenses, cash, cross-holdings, minority interests, and debt. Every one of these has to appear somewhere in the bridge or the total is wrong.
4. Value or price each part on its own economics — its own cost of capital or its own sector multiple. Do **not** apply a company-wide number to every division.
5. Aggregate, net out corporate costs, and bridge to equity.
6. Compare four numbers: sum-of-parts intrinsic, sum-of-parts relative, whole-company DCF, and market enterprise value. The spread between them is the finding.

**Reference data:** The four comparison numbers for United Technologies (2009, $ millions), which is the template for step 6:

| Estimate | Value ($M) |
|---|---|
| Sum of the parts, DCF (after corporate expenses) | 75,663 |
| Sum of the parts, relative valuation | 74,230 |
| Whole-company DCF | 71,410 |
| Enterprise value at market prices | 52,261 |

Motive-to-method mapping:

| Who you are | Route | Reason |
|---|---|---|
| Passive long-term investor | Intrinsic | Betting the market misprices the pieces and will correct |
| Activist / acquirer | Relative | Pieces will be sold or spun at market prices |
| Accountant under fair value | Relative first | Standard demands an exit price |
| Liquidator | Relative | You are selling, not holding |

**Worked example:** United Technologies, 2009. All three of Damodaran's estimates of value ($71.4bn to $75.7bn) sit far above the $52.3bn the market was assigning to the enterprise. That gap — roughly 30% — is the conglomerate discount. For an activist, the relevant number is the $74,230M relative sum of the parts, because a break-up would realize sector prices. For a passive investor, the relevant number is the $75,663M DCF sum of the parts, because the thesis is that the market will eventually pay for the cash flows.

**Determinism:**
- DETERMINISTIC: the aggregation, the bridge, and the conglomerate-discount ratio, given per-division values.
- JUDGMENT: the motive (which is an input, not an output); how to define the parts when segment reporting is coarse; how to allocate corporate costs; and whether the observed gap is a genuine mispricing or compensation for a real cost of conglomeration (bad capital allocation, cross-subsidy, entrenchment). That judgment needs segment disclosures, the history of divisional performance, and evidence on whether break-ups in this sector have actually realized the sum of the parts.

**Pitfalls:**
- Using one company-wide cost of capital or one company-wide multiple across divisions with different risk. This is the single most common error and it moves the answer a lot.
- Forgetting unallocated corporate expenses. They are a real, permanent cash drain and must be capitalized and subtracted.
- Double counting: a division's value already includes its own cash-generating capacity, so do not add corporate cash twice.
- Reading a conglomerate discount as automatic free money. The pieces only fetch peer multiples if somebody actually buys them.
- Ignoring that the pieces may be worth less apart than together when real synergies exist.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket2spr21 p.105, p.110, p.119, p.127
- valuations--lecture_notes--spring_2020--valpacket2spr20 p.103, p.108, p.117, p.125

**Related:** [[asset-based-valuation-overview]], [[sum-of-the-parts-pricing]], [[sum-of-the-parts-dcf]], [[private-company-valuation-framework]], [[divestitures-and-spinoffs]], [[relative-valuation-fundamentals]]
