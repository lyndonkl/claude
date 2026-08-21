# Triangulating the value estimates into a buy/sell/hold call

**Core idea:** Step 6 of the equity valuation project turns several conflicting numbers into one decision. The DCF, the peer average, the sector regression, the market regression and — where it applies — the option value rarely agree. The project forbids reporting them in isolation. The analyst must first check whether news during the analysis period has changed the narrative, update for it, then line the estimates up in a single table and state which one carries the weight and why. The output is a buy, sell or hold call on every stock in the group, with the reasoning visible.

**Formulas:** No formula. Two decision rules do the work:
- Recommend **SELL** when the preferred value estimate sits below the market price.
- Recommend **BUY** when the preferred estimate — and preferably nearly every method — sits above the market price.
- Weighting rule: when comparables selection is ambiguous, weight the DCF above the relative-valuation regressions.

**Procedure:**
1. **Check the news.** Review events during the analysis period. Ask whether any of them changes the narrative, and therefore the inputs. Update the valuation before recommending.
2. **Build the final analysis table.** Standard rows: current price; DCF Base; DCF Lo and DCF Hi from the sensitivity grid; the peer-average multiple's implied price; the sector regression's implied price; the market regression's implied price; and the option value where applicable.
3. **Discard any implausible estimate** and say why, rather than letting it drag an average.
4. **Choose the weighting and defend it.** The default in this project is DCF-heavy, on the grounds that comparables selection is ambiguous, that the DCF carries the richest information, and that its assumptions were deliberately conservative. Where a market regression matches the DCF closely, that agreement strengthens both.
5. **Look for unanimity.** When every method except one points the same way, that is strong evidence and should be stated as such.
6. **Issue the call** — buy, sell or hold — naming the estimate it rests on and the gap to the market price.
7. **Attach the EVA check** as a value-creation cross-reference. A firm with ROC above WACC creates value with any reinvestment, which supports growth assumptions; a firm with ROC below WACC does not. See [[return-spread-and-eva-analysis]].

**Reference data:** Final analysis tables from the six-company equity valuation project.

| Metric | ACS | Apple | Biosite | Gundle | Infosys (Rs) | Nextel |
|---|---|---|---|---|---|---|
| Current price | $50.50 | $20.85 | $26.12 | $19.13 | 4,912 | $11.72 |
| DCF Base | $48.75 | $27.06 | $32.76 | $41.13 | 4,270 | $11.08 |
| DCF Lo | — | $22.58 | $32.76 | $29.20 | 3,651 | — |
| DCF Hi | $54.07 (extreme hi $54.73) | $31.52 | $161.80 | $54.83 | 6,733 | — |
| Peer-average multiple → price | PBV 2.618 | PE $48.31 | VS $22.64 | P/BV $22.06 | PEG 9,043 | V/BVC $11.65 |
| Sector regression → price | PBV 3.283 ($59.87) | PE $24.53 | VS $22.50 | P/BV $29.57 | PEG 5,307 | V/BVC $8.82 |
| Market regression → price | PBV 2.54 ($48.36) | PE $18.31 | VS $29.68 | P/BV $31.49 | PEG 16 (rejected) | V/BVC $12.15 |
| Option value | — | — | — | — | — | $9.09 |
| **Recommendation** | **SELL** | **BUY** | **BUY** | **BUY** | **SELL** | **SELL** |

Note: the Gundle current price is quoted as $19.73 in the DCF section and $19.13 in the final table; the conclusion is unaffected.

**Worked example:** Four contrasting calls.

*Apple — BUY on near-unanimity.* Value $27.06 against a $20.85 price, DCF Lo $22.58 still above price, peer-average PE implying $48.31, sector regression $24.53. Only the market PE regression dissents at $18.31. The authors call this "overwhelming evidence" of undervaluation.

*ACS — SELL on a narrow margin.* DCF base $48.75 sits just under the $50.50 price. The sector regression says $59.87 (undervalued) while the peer average says $47.75 (overvalued) — a 25% disagreement between two peer-based methods. The authors weight the DCF above both because of the ambiguity in choosing comparables, and call SELL.

*Biosite — BUY despite disagreement.* Every DCF case sits above the $26.12 price, including the low case at $32.76. Both comparables methods say roughly $22.50, below price. The DCF wins the weighting because it uses the most conservative estimates and the richest information — high growth, high margins, an extended transition and 100% reinvestment. BUY.

*Nextel — SELL from two independent low estimates.* DCF $11.08 and option value $9.09 both sit below the $11.72 price. Its EVA is deeply negative at −$625m, though less negative than the wireless industry average firm EVA of −5,742, because the ROC−WACC gap applies to a smaller capital base. SELL.

**Determinism:** DETERMINISTIC — assembling the final table, computing every gap to market price, and applying the mechanical rule (preferred estimate above price → BUY, below → SELL) once the preferred estimate is chosen. JUDGMENT — everything upstream of that: whether news has changed the narrative, which estimates to discard, which method to weight, and how to handle a set that splits evenly. That judgment needs the news history for the period, the reasons each method could be wrong for this firm, and an honest read of how ambiguous the comparables selection was.

**Pitfalls:**
- Averaging all the estimates. That gives an implausible market regression the same weight as a carefully built DCF.
- Skipping the news check. A valuation built on a narrative that events have already overtaken is worse than no valuation.
- Reporting the methods side by side without reconciling them, which the project explicitly forbids.
- Letting a wide DCF Hi from an implausible sensitivity cell into the argument. Biosite's $161.80 comes from 28% growth sustained for ten years, which was rejected in the sensitivity section itself.
- Making a call on a small gap without acknowledging it. ACS's SELL rests on a $1.75 difference on a $50.50 stock.
- Forgetting the EVA cross-check. A firm whose ROC is below its WACC cannot justify growth-driven value in the DCF.

**Sources:**
- valuations--projects--eqprojspr19 p.8
- valuations--projects--valproject2 p.4, p.7, p.10, p.12, p.17, p.20

**Related:** [[dcf-model-selection]], [[dcf-sensitivity-analysis]], [[relative-valuation-comparables-regression]], [[market-wide-multiple-regression]], [[equity-as-call-option-valuation]], [[return-spread-and-eva-analysis]], [[equity-valuation-project-blueprint]], [[project-executive-summary-scorecard]]
