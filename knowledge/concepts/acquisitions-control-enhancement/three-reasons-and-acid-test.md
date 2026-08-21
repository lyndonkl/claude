# The three reasons for acquisitions and the acid test

**Core idea:** Only three value-based reasons exist for buying a company: undervaluation, control, and synergy. Everything else is a buzz word. Each reason has its own value benchmark, and each benchmark is one of four numbers you must estimate for any deal. The four are the acquisition price, the status-quo value, the restructured value, and the synergy value. The acid test compares price to the benchmark that matches the stated motive. Fail the test and you are overpaying — unless your value estimates are wrong, which is a claim the deal's proponents must prove.

**Formulas:**

The four numbers:
1. `Acquisition Price` — what you pay. For a private business, a negotiated price, often off comparable deals. For a public company, a premium over market price.
2. `Status Quo Value` — DCF value of the target run by existing management.
3. `Restructured Value` — DCF value of the target with changed investing, financing and dividend policies.
4. `Synergy Value = Value of combined company with synergy − [Value of acquirer stand-alone + Restructured value of target]`.

The acid test, by motive:

| Motive | Deal makes sense only if |
|---|---|
| Undervaluation | `Price for target < Status Quo Value` |
| Control | `Price for target < Restructured Value` |
| Synergy | `Price for target < Restructured Value + Value of Synergy` |

Derived quantities: `Value of control = Restructured Value − Status Quo Value`, and `Premium to justify = Price − Pre-announcement market capitalization`.

**Procedure:**
1. Write down the stated motive for the deal, and classify it as undervaluation, control or synergy. Synergy subdivides into offensive (higher growth, more pricing power), defensive (cost cutting, consolidation, preempting competitors) and tax (direct tax clauses, or indirect through debt).
2. If the rationale fits none of the three, it is not a value reason. Send it back.
3. Compute the status-quo value with a full DCF, using the target's own risk and debt capacity.
4. Compare status-quo value to the pre-announcement market capitalization. If market cap exceeds status-quo value, the undervaluation motive is dead.
5. Benchmark the target against the acquirer and the sector, define the specific policy changes, and compute the restructured value.
6. Compute `Value of control = Restructured − Status Quo`.
7. Value the combined firm with synergy against the combined firm without, using the *restructured* target value in the baseline. This avoids double counting.
8. Apply the acid test row that matches the motive.
9. If price exceeds the benchmark, exactly two explanations remain: the synergy potential is underestimated, or the acquirer is overpaying. Decide which, and say so.

**Reference data:** No lookup table. The three-way classification and the three acid-test inequalities above are the reference.

The three flavours of synergy:

| Flavour | Content |
|---|---|
| Offensive | Higher growth, increased pricing power |
| Defensive | Cost cutting, consolidation, preempting competitors |
| Tax | Directly from tax clauses, or indirectly through added debt |

**Worked example — AB InBev / SABMiller, $ billions:**

SABMiller's market capitalization was $75B on September 15, 2015, the day AB InBev announced its intent. A month later AB InBev agreed to pay $104B. The premium to justify is `104 − 75 = $29B`. The market appeared to agree it existed, adding $33B of market value to the combined company on the news.

Run the acid test on all three motives.

| Number | Value |
|---|---|
| Acquisition price | $104B |
| Status quo value of SABMiller equity | $51.5B |
| Restructured (optimal) value | $56.2B |
| Value of control | $4.7B |
| Value of synergy | $14.6B |
| Restructured + synergy | $70.8B |

- Undervaluation: `$104B < $51.5B`? No. The market price of $75B already exceeded the status-quo value, so the target was not undervalued even before the premium.
- Control: `$104B < $56.2B`? No.
- Synergy: `$104B < $70.8B`? No.

The deal fails all three tests by roughly $33B. Two readings follow. Either the synergy potential was massively underestimated — higher margins or higher growth than assumed — or AB InBev significantly overpaid. Overpayment would run against its history as a disciplined acquirer and 3G Capital's reputation as a steward of capital, which is exactly the tension the case is built to expose.

**Determinism:**
- DETERMINISTIC: all three acid-test comparisons once the four numbers exist; the value of control as a subtraction; the premium as price minus market cap.
- JUDGMENT: all four numbers require full valuations. The status-quo DCF needs operating and risk assumptions. The restructured value needs a specific improvement plan. The synergy value needs input-level synergy estimates. The price may be negotiated rather than derived.

**Pitfalls:**
- Adding the value of control and the value of synergy to the *market price* rather than testing them against the price paid. The benchmarks are values, not prices.
- Using the target's status-quo value in the synergy baseline while also claiming control value. Control gains then get counted twice.
- Declaring a target undervalued without comparing status-quo value to the pre-announcement market cap.
- Accepting "strategic" as a fourth reason. It is not one.
- Concluding "our numbers must be too conservative" whenever the test fails. That is the verdict-first sin, restated.

**Sources:**
- `valuations--lecture_notes--spring_2021--valpacket3spr21 p.122-124, p.130`
- `valuations--lecture_notes--spring_2020--valpacket3spr20 p.122-124, p.130`

**Related:** [[status-quo-valuation]], [[restructured-value-and-value-of-control]], [[valuing-synergy]], [[synergy-taxonomy]], [[abinbev-sabmiller-case]], [[control-premium-rules-of-thumb]], [[seven-sins-of-acquisitions]]
