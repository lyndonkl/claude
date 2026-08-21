# Synergy taxonomy: mapping claimed benefits to valuation inputs

**Core idea:** Synergy is created when two firms combine and can do something neither could do alone. The word is used loosely, so the discipline is to force every claimed synergy onto a specific valuation input. If a claimed benefit does not change a margin, a return on capital, a reinvestment rate, a growth period, a tax rate or a debt ratio, it cannot change value. Synergy splits into operating and financial. Operating synergy has two branches: strategic advantages and economies of scale. Financial synergy has three: tax benefits, added debt capacity, and diversification. Diversification is the suspect one — it lowers the cost of equity only for a private or closely held firm, never for a public firm whose investors diversify on their own account.

**Formulas:** No single formula. The taxonomy is a mapping table from synergy type to the input it moves:

| Synergy | Type | Valuation input it changes |
|---|---|---|
| Higher returns on new investments | Operating — strategic | Higher ROC → higher growth rate |
| More new investments | Operating — strategic | Higher reinvestment rate → higher growth rate |
| More sustainable excess returns | Operating — strategic | Longer high-growth period |
| Cost savings in current operations | Operating — economies of scale | Higher operating margin, higher base-year EBIT |
| Lower taxes (higher depreciation, NOL carryforwards) | Financial — tax | Lower effective tax rate |
| Added debt capacity | Financial — debt | Higher debt ratio → lower cost of capital |
| Diversification | Financial — questionable | Lower cost of equity, **private/closely held firms only** |

Supporting identities: `Expected growth = Reinvestment rate × Return on capital`, and `EBIT = Revenues × Operating margin`.

**Procedure:**
1. Take the deal's stated rationale and list each claimed benefit separately.
2. Classify each as operating or financial, then place it in one of the seven rows above.
3. If a claim fits no row, it is a buzz word. Reject it or force the proponent to restate it as an input change.
4. Quantify the input change: how many basis points of margin, how many points of ROC, how many extra years of excess returns.
5. Check diversification claims against ownership. For a publicly traded acquirer and target, "the combined firm is less risky, so use a lower cost of capital" is not a valid synergy. Investors already diversify at lower cost than a merger.
6. Check for double counting across rows. Cost savings raise the margin; do not also raise the ROC for the same savings.
7. Feed the surviving input changes into the three-step synergy valuation.

**Reference data:** The mapping table above is the reference. The one hard rule with a stated condition: diversification reduces the cost of equity only for private or closely held firms.

**Worked example:** AB InBev's stated motives for buying SABMiller were global complementarity (grow AB in Africa, SAB in Latin America) and consolidation (cost cutting in Latin America). Mapped onto the taxonomy: complementarity is an operating-strategic synergy that raises the reinvestment rate and the return on capital, hence growth. Consolidation is an economies-of-scale synergy that raises the operating margin. The analyst's synergy case therefore lifted the combined operating margin from 28.27% to 30.00%, ROC from 11.68% to 12.00%, the reinvestment rate from 43.58% to 50.00%, and expected growth from 5.09% to 6.00%. Every red-ink assumption traces to a row in the table.

**Determinism:**
- DETERMINISTIC: once a synergy is expressed as an input change, the value effect is a DCF computation. `Expected growth = Reinvestment rate × ROC` is arithmetic.
- JUDGMENT: the classification itself, the magnitude of each input change, and whether a claimed benefit is real. That judgment needs the combined firm's operating plan, overlap analysis, and evidence from comparable integrations.

**Pitfalls:**
- Accepting diversification as a synergy for public firms. It is the classic conglomerate fallacy.
- Leaving synergies as adjectives ("strategic", "transformational") instead of numbers.
- Assigning one benefit to two inputs and counting the value twice.
- Forgetting that added debt capacity belongs here, not in the target's own cost of capital.
- Treating tax benefits as fully and immediately available; usable NOLs depend on the acquirer's taxable income.

**Sources:**
- `valuations--lecture_notes--spring_2021--valpacket3spr21 p.98-99, p.123`
- `valuations--lecture_notes--spring_2020--valpacket3spr20 p.98-99, p.123`

**Related:** [[valuing-synergy]], [[synergy-delivery-odds]], [[target-discount-rate-discipline]], [[three-reasons-and-acid-test]], [[abinbev-sabmiller-case]], [[paths-to-value-creation]]
