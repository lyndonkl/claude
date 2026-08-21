# The impossible, the implausible and the improbable

**Core idea:** A narrative can fail three ways, and each failure has its own screen. The **impossible** breaks arithmetic or economics, and you never allow it. The **implausible** is not impossible but needs extraordinary justification. The **improbable** is a combination: each assumption looks fine alone, but together they contradict how business works. The improbable cases sit on the Value Narrative triangle of growth, risk and reinvestment. You can have a good outcome on one corner, sometimes two with a real reason, but never all three for free. Most of these checks can be run mechanically on a finished model, which makes them the cheapest quality control in valuation.

**Formulas:** Each screen is a testable inequality on the model's own outputs.

**Impossible — never allow:**
- Bigger than the economy: perpetuity growth rate g ≤ growth rate of the economy. In practice, cap g at the riskfree rate in the same currency.
- Bigger than the total market: implied revenues / total market size ≤ 100%.
- Profit margin > 100%: earnings growth cannot exceed revenue growth long enough to push operating margin above 100%.
- Depreciation without cap ex: depreciation ≤ cap ex in perpetuity.

**Implausible — needs extraordinary justification:**
- Growth without reinvestment: growth forever with no reinvestment.
- Profits without competition: high growth and rising profits with no competitive response.
- Returns without risk: high returns in a business with no risk.

**Improbable — internally inconsistent pairings on the growth/risk/reinvestment triangle:**
- High growth and low risk.
- High growth and low reinvestment.
- Low risk and high reinvestment.

Supporting identities used by the screens:
- Expected growth rate = Reinvestment rate × Return on capital. So low reinvestment plus high growth forces an implausible ROC.
- Stable-period reinvestment rate = Stable growth g / Stable return on capital.
- Marginal ROIC = Change in EBIT(1−t) over the forecast / Change in invested capital over the forecast.

**Procedure:**
1. **Run the four impossible screens on the finished model.** Compare terminal g with the riskfree rate. Divide year-10 revenues by your own total-market estimate. Check the maximum margin in the forecast. Check terminal depreciation against terminal cap ex.
2. **Compute the implied marginal ROIC.** Divide the change in after-tax operating income across the forecast by the change in invested capital. If it exceeds what the best firms in the business earn, either reinvestment is too low or margins are too high.
3. **Check the terminal excess return.** Terminal ROC above the terminal cost of capital means you are claiming a moat that survives forever. State the moat or set them equal.
4. **Ask the three triangle questions.** Is your risk consistent with how much, how and where you are growing? Are you reinvesting enough given your growth? Is your risk consistent with your reinvestment strategy?
5. **Sanity-check absolute revenues, not just growth rates.** Percentage growth is deceptive. Translate the growth path into dollars in year 10 and ask who loses that revenue.
6. **Fade excess growth.** Newly public companies beat their industry's revenue growth for about five years, and the median excess falls to roughly zero by years five to six. A model that keeps the excess for a decade needs a reason.
7. **Fix the offending input, not the output.** If a screen fails, change the assumption that caused it and let value fall where it falls.

**Reference data:** The three failure classes and their tests:

| Class | Failure | Test |
|---|---|---|
| Impossible | Bigger than the economy | Perpetuity g > economy growth (proxy: riskfree rate) |
| Impossible | Bigger than the total market | Implied market share > 100% |
| Impossible | Margin above 100% | Earnings growth > revenue growth long enough to push margin over 100% |
| Impossible | Depreciation without cap ex | Depreciation > cap ex in perpetuity |
| Implausible | Growth without reinvestment | Perpetual growth with zero reinvestment |
| Implausible | Profits without competition | Rising margins and share with no competitive response modelled |
| Implausible | Returns without risk | High returns assumed in a business with no risk |
| Improbable | High growth + low risk | Growth, risk and reinvestment corners all favourable at once |
| Improbable | High growth + low reinvestment | Implied marginal ROIC far above industry best |
| Improbable | Low risk + high reinvestment | Heavy reinvestment paired with a mature-company cost of capital |

Growth-margin trade-off (stated as a proposition): strategies that push for more growth deliver less margin, and vice versa. Scaling up is not an automatic cure for losing money — costs have to grow slower than revenues, and that is not guaranteed.

**Worked example:** "Willy Wonkitis" — a sell-side 15-year DCF for Tesla dated mid-2013, covering FY2013 to FY2028. Unit volume grows from 24,298 to 1,137,780 vehicles. Annual unit growth runs 52%, 75%, 34%, 73%, 43%, 36%, 32%, 21%, 18%, 17%, 13%, 13%, 12%, 12%, 10%. Revenue per unit drifts from $93,403 to $59,554. Total sales rise from $2,478M to $68,059M. EBITDA margin climbs from 6.0% to 17.8% ($148M to $12,099M) and EBIT margin from 1.8% to 15.3%. Net income goes from $44M to $9,050M, and unlevered free cash flow from $78M to $8,005M. Cap ex settles at just 3% of sales, with negative working-capital changes. Exit assumptions: EBITDA multiple 8.0x–12.0x, perpetuity growth 3.0%–5.0%, P/Sales 130%–180%, discount rate 9.0%–13.0%. Line by line each input is arguable. Together they are the classic improbable combination: enormous growth, expanding margins and almost no reinvestment. Note also the exit perpetuity growth of 3%–5%, which trips the impossible screen if it exceeds the economy's growth rate.

**Determinism:**
- DETERMINISTIC: every impossible screen, given the model's outputs and one external number (economy growth or riskfree rate, total market size). The implied market share, maximum margin, terminal depreciation-to-cap-ex ratio, marginal ROIC, and terminal excess return are all computable.
- JUDGMENT: the total market size the share is measured against; whether a moat justifies terminal excess returns; whether a given growth-margin-reinvestment triple is defensible in this specific business; how fast excess growth should fade.

**Pitfalls:**
- Setting terminal growth above the riskfree rate because "this company is special". Nothing outgrows the economy forever.
- Checking growth rates but never absolute revenues, so nobody notices the model implies more than the whole market.
- Assuming margin expansion and heavy growth at once with no reinvestment to pay for either.
- Leaving the terminal return on capital above the terminal cost of capital by default rather than by argument.
- Fixing a failed screen by nudging the output instead of the offending assumption.

**Sources:**
- valpacket1spr21 p.262, p.268
- valpacket1spr20 p.258, p.264
- valuationmotleyfool p.15, p.16, p.17, p.21
- valpacket1spr21 p.302 (excess revenue growth over industry fades to zero in about five years post-IPO), p.317 (growth only creates value when ROIC exceeds the cost of capital)
- motley-fool-tesla-xlsx: `Diagnostics` B6 marginal ROIC 0.5166, B7 ROIC at end 0.3424, `Stories to Numbers` F12 stable reinvestment rate = g/ROC = 0.0156/0.15 = 0.104

**Related:** [[possible-plausible-probable]], [[narrative-to-value-drivers]], [[big-market-delusion]], [[story-to-numbers-process]], [[bermuda-triangle-of-valuation]], [[tesla-motley-fool-valuation]]
