# Riskfree rate: definition and instrument choice

**Core idea:** A riskfree investment is one where the actual return always equals the expected return — there is zero variance around the expected return. Two conditions must hold: **no default risk** (which effectively restricts you to government issuers, and not all of those) and **no reinvestment risk** (which strictly means a zero-coupon security whose maturity matches the timing of the cash flow being discounted). Three consequences follow: the riskfree rate is horizon-specific, it is currency-specific, and government bond rates are not automatically riskfree. In practice, because corporate finance and valuation cash flows are long-lived and cash-flow uncertainty dwarfs the effect of a term structure, analysts use a single long-term (10-year) default-free government bond rate in the currency of the cash flows rather than a separate zero rate for each year.

**Formulas:**
- Theoretical: Riskfree rate for a year-t cash flow = yield on a zero-coupon, default-free bond maturing in year t, denominated in the cash flow's currency.
- Practical convention: Riskfree rate = 10-year government bond rate of a default-free (Aaa/AAA-rated) government issuing in the currency of analysis.
- Multi-issuer currency (e.g. the Euro): Riskfree rate = min over sovereigns issuing in that currency of their 10-year government bond rate (the lowest rate carries the least default risk).
- Real analysis: Real riskfree rate = yield on an inflation-indexed government bond (TIPS) of matching maturity.
- Cost of equity that uses it: Cost of Equity = Riskfree rate + Beta × Equity Risk Premium (see [[cost-of-equity-assembly]]).

Symbols: "default-free" = the issuer's own-currency obligations carry no credit risk; "10-year" is the duration-matching convention for perpetual/long-lived corporate cash flows.

**Procedure:**
1. Identify the **currency** in which your cash flows are stated. The riskfree rate must be in that same currency. (Currency mismatch is one of the three consistency rules for discount rates, alongside equity-vs-firm and nominal-vs-real.)
2. Identify whether cash flows are **nominal or real**. Nominal cash flows → nominal government bond rate. Real cash flows → inflation-indexed bond (TIPS) yield.
3. Identify the **horizon**. Corporate valuations run effectively forever, so use a long-term rate: the 10-year government bond is the standard. Use a short-term government rate only for genuinely short-term analyses. Do not use the 3-month T-bill for a going-concern valuation, and do not automatically jump to the 30-year rate — the 10-year matches the duration of typical valuation cash flows.
4. Check whether the government issuing in that currency is **default-free**. If Moody's/S&P rate its local-currency debt Aaa/AAA, use its 10-year bond rate as the riskfree rate directly.
5. If **several governments issue in the same currency** (Euro), do not average them and do not use your own country's bond. Take the *lowest* 10-year rate among them — in the Euro that is Germany. The spread of every other issuer over Germany is sovereign default risk, not currency.
6. If the issuing government is **not** default-free, or no default-free entity exists in the currency, go to [[currency-riskfree-rate]] to strip the default spread or switch currency/real terms.
7. If today's rate looks abnormally low or high relative to history, do **not** substitute a "normalized" rate on its own — see [[riskfree-rate-normalization]].

**Reference data:**

US Treasury rates, January 1, 2021 (the packet's default choice is the 10-year T.Bond = 0.93%):

| Instrument | Rate |
|---|---|
| 3-month T.Bill | 0.09% |
| 10-year T.Bond | 0.93% |
| 30-year T.Bond | 1.40% |
| 10-year TIPS (real) | −1.00% |

(January 1, 2020 comparators: T.Bill 1.5%, 10-year 1.92%, 30-year 2.2%, TIPS 0.6%.)

Euro-denominated 10-year government bond rates, January 1, 2021 — same currency, eleven different rates, so they cannot all be riskfree:

| Country | 10-yr rate | Country | 10-yr rate |
|---|---|---|---|
| Germany | −0.58% | Slovenia | −0.14% |
| Austria | −0.48% | Portugal | 0.02% |
| Finland | −0.39% | Spain | 0.05% |
| Belgium | −0.38% | Italy | 0.58% |
| France | −0.34% | Greece | 0.65% |
| Ireland | −0.27% | | |

(January 1, 2020: Germany −0.28%, Finland −0.15%, Austria −0.03%, France 0.03%, Belgium 0.07%, Ireland 0.12%, Slovenia 0.24%, Portugal 0.44%, Spain 0.48%, Italy 1.39%, Greece 2.08%.)

**Worked example:** Valuing a company whose cash flows are in Euros on January 1, 2021. Germany's 10-year Euro bond yields −0.58% and is Aaa-rated; Greece's yields 0.65%. The Euro riskfree rate is **−0.58%**, and the 1.23% Greek excess is Greek sovereign default risk, which belongs in the equity risk premium for Greek operations (see [[country-risk-premium]]), not in the riskfree rate. For the same company valued in US dollars, the riskfree rate on the same date is the 10-year T.Bond rate of **0.93%**.

**Determinism:**
- DETERMINISTIC: given (currency, date, table of sovereign 10-year rates, sovereign ratings) → riskfree rate. The Euro case is a pure `min()` over the rate table; the US case is a lookup of the 10-year Treasury.
- JUDGMENT: choosing the maturity convention (10-year vs 30-year vs matched zero rates); deciding whether a given sovereign is genuinely default-free; deciding whether to run the valuation in nominal or real terms.

**Pitfalls:**
- Using a T-bill rate for a long-horizon valuation (reinvestment risk; also mismatches the historical premium you pair it with).
- Assuming every government bond is riskfree. Some governments default in their own currency.
- Averaging the Euro sovereigns, or using your home sovereign's Euro bond as "the" Euro riskfree rate.
- Mixing currencies: a Euro riskfree rate with dollar cash flows, or a nominal rate with real cash flows.
- Using a TIPS yield as the riskfree rate for nominal cash flows.
- Forgetting that using Treasury rates implicitly assumes the US Treasury has no default risk — an assumption, not a fact.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.27-30, p.38
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.27-30, p.38
- corporate_finance--lecture_slides--cfpacket1spr20 p.99-103

**Related:** [[currency-riskfree-rate]], [[riskfree-rate-normalization]], [[cost-of-equity-assembly]], [[capm-cost-of-equity]], [[sovereign-ratings-and-default-spreads]], [[discount-rate-consistency]]
