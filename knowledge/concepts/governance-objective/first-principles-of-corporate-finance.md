# First Principles of Corporate Finance

**Core idea:** Corporate finance is the study of every decision a business makes with a financial dimension, and all of it hangs from one objective: maximize the value of the business (the firm). That single objective decomposes into exactly three decisions — the investment decision, the financing decision, and the dividend (cash-return) decision. Every technique later in the course (hurdle rates, betas, cost of capital, project cash flows, optimal debt ratios, payout policy, valuation) is machinery for executing one of those three decisions. An analyst uses this map to place any corporate action: if a company is doing something with money, it is investing, financing, or returning cash, and it should be judged against the corresponding first principle.

**Formulas:**
- Investment rule: `Accept if Return on investment > Hurdle rate`, where the hurdle rate reflects (a) the riskiness of the investment and (b) the mix of debt and equity used to fund it.
- Financing rule: `Choose D/(D+E) that maximizes firm value`, and choose debt whose tenor matches the life of the assets financed.
- Dividend rule: `If no investment clears the hurdle rate, return the cash to owners.` The amount depends on current and potential investment opportunities; the form (dividends vs. buybacks) depends on owner preference.
- No numeric formula is defined on this slide; the "returns" must reflect the magnitude and timing of cash flows and all side effects.

**Procedure:** Applying the map to a real company:
1. State the objective for this firm. Default: maximize firm value. (Whether you can narrow that to stock price is settled by the modified objective function — see [[modified-objective-function]].)
2. Classify each material corporate action from the last 1-3 years into investment / financing / dividend.
3. For investments: identify the hurdle rate the firm should have used (risk-adjusted, financing-mix-adjusted) and the return actually earned. Flag any investment accepted with return < hurdle rate.
4. For financing: identify the current debt/equity mix and the *kind* of debt (currency, maturity, fixed/floating). Flag mismatches between debt tenor and asset life (e.g. long-lived infrastructure funded with 1-year commercial paper).
5. For dividends: check whether cash is being returned when the firm has no investments clearing the hurdle rate, and whether it is being retained when it does have such investments. Both errors destroy value.
6. Report each of the three decisions as "consistent with first principles" or "violates first principles," and name the violated rule.

**Reference data:** None required — this is a framework slide. The one structural fact to carry forward: the hurdle rate is *investment-specific* (risk of the project), not firm-wide by assumption, and it is *financing-mix-specific*.

**Worked example:** Damodaran's framing example throughout Packet 1 is Disney. Disney's 1996 ABC acquisition is an investment decision: the analyst asks whether the return on the $19bn invested exceeded Disney's risk-adjusted hurdle rate for broadcasting. The board rubber-stamped it (see [[disney-governance-case-study]]), and Disney's stock price halved between 1998 and 2002 — the first-principles verdict is that the investment decision failed the hurdle-rate test, and the governance structure failed to catch it.

**Determinism:**
- DETERMINISTIC: classifying an action into investment/financing/dividend given a description; comparing a computed return to a computed hurdle rate (return, hurdle rate -> accept/reject); comparing weighted-average debt maturity to weighted-average asset life.
- JUDGMENT: estimating the hurdle rate itself (requires risk model, beta, risk premium); estimating project returns including "all side effects" (cannibalization, synergies, options); judging what the owners prefer between dividends and buybacks.

**Pitfalls:**
- Using one firm-wide hurdle rate for every project regardless of project risk. The slide is explicit that the hurdle rate should reflect *the riskiness of the investment*.
- Ignoring side effects when measuring returns — the slide says returns must reflect magnitude, timing, *and all side effects*.
- Treating "the right mix of debt and equity" as the whole financing decision and forgetting "the right *kind* of debt" (tenor matching).
- Treating the dividend decision as a residual afterthought rather than the disciplined consequence of failing the hurdle-rate test.

**Sources:**
- corporate_finance--lecture_slides--cfpacket1spr20 p.2-3
- corporate_finance--lecture_slides--cfpacket1spr20 p.4

**Related:** [[objective-function-and-stock-price-maximization]], [[modified-objective-function]], [[hurdle-rate]], [[cost-of-capital]], [[optimal-debt-ratio]], [[dividend-policy]]
