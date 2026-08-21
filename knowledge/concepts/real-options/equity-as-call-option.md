# Equity as a call option on the firm

**Core idea:** Equity is a residual claim. Equity holders receive whatever cash flows remain after all other financial claim-holders — debt, preferred stock and the rest — are satisfied, and the same rule applies in liquidation. Limited liability means that if firm value falls below the outstanding debt, equity investors cannot lose more than their investment. Residual claim plus limited liability is exactly a call option payoff. The underlying asset is the value of the firm, the strike is the face value of debt, and the option's life is the maturity of the debt. Once you see it this way, three things follow that a straight DCF cannot explain: distressed equity trades above zero, stockholders can gain by raising risk, and diversifying mergers can transfer wealth to bondholders.

**Formulas:**
- Equity payoff at debt maturity: `max(V - D, 0)`, where `V` = value of the firm and `D` = face value of debt.
- Equity value (Black-Scholes call): `E = S x N(d1) - K x e^(-r*t) x N(d2)`
  - `d1 = [ln(S/K) + (r + sigma^2/2) x t] / (sigma x sqrt(t))`, `d2 = d1 - sigma x sqrt(t)`
- Input mapping: `S` = value of the firm; `K` = face value of outstanding debt; `t` = life of the (zero-coupon) debt; `sigma^2` = variance in firm value; `r` = riskless rate corresponding to the option's life.
- Implied market value of debt: `Debt = Firm value - Equity value`.
- Implied interest rate on zero-coupon debt: `r_debt = (Face value / Market value of debt)^(1/t) - 1`.
- The spread `r_debt - r` is the default spread the option model implies.

**Procedure:**
1. Estimate the value of the firm's assets, `S`. Cumulate the market values of equity and debt, or value the assets in place with FCFF and the WACC. See [[equity-option-inputs-troubled-firms]] for the full menu.
2. Estimate the variance in firm value, `sigma^2` — not the variance in equity value. These differ sharply in a levered firm.
3. Set `K` = the face value of outstanding debt.
4. Set `t` = the life of the debt. In the clean case this is the maturity of a zero-coupon bond. For real capital structures use the face-value-weighted duration.
5. Set `r` = a government bond rate whose maturity or duration matches `t`.
6. Compute `d1`, `d2`, `N(d1)`, `N(d2)`, and the call value. That is the equity value.
7. Back out the market value of debt as firm value minus equity value.
8. Back out the implied interest rate on the debt. Compare it with the riskless rate; the difference is the model's implied default spread.
9. Use the comparative statics to reason about conflicts. Equity value rises with firm value, with variance, with time to maturity, and with the riskless rate; it falls with the face value of debt.

**Reference data:**

Mapping from firm facts to option inputs:

| Option input | Firm equivalent |
|---|---|
| `S` — value of the underlying asset | Value of the firm |
| `K` — exercise price | Face value of outstanding debt |
| `t` — life of the option | Life of the zero-coupon debt (or weighted duration of debt) |
| `sigma^2` — variance of the underlying | Variance in firm value |
| `r` — riskless rate | Treasury bond rate matching the option's life |

Simplifying assumptions embedded in the clean version of this model. Real firms violate all four, and [[equity-option-inputs-troubled-firms]] gives the workarounds:

| # | Assumption |
|---|---|
| 1 | Only two claim holders in the firm — debt and equity |
| 2 | Only one issue of debt outstanding, retirable at face value |
| 3 | The debt is zero-coupon with no special features (no convertibility, no put clauses) |
| 4 | The value of the firm and its variance can be estimated |

**Worked example:** The base case used throughout this section of the packet.

A firm's assets are currently valued at $100 million. The standard deviation of asset value is 40%. The face value of debt is $80 million, zero-coupon, with 10 years to maturity. The ten-year treasury bond rate is 10%.

| Input | Value |
|---|---|
| `S` = value of the firm | $100 million |
| `K` = face value of debt | $80 million |
| `t` = life of the zero-coupon debt | 10 years |
| `sigma^2` = variance in firm value | 0.16 (0.40 squared) |
| `r` = riskless rate | 10% |

`d1` = 1.5994, `N(d1)` = 0.9451; `d2` = 0.3345, `N(d2)` = 0.6310.

`Equity = 100 x 0.9451 - 80 x e^(-0.10 x 10) x 0.6310 = $75.94 million`.

`Value of outstanding debt = 100 - 75.94 = $24.06 million`.

`Interest rate on debt = (80 / 24.06)^(1/10) - 1 = 12.77%`.

The implied 12.77% exceeds the 10% riskless rate by 2.77 percentage points. That spread is the default risk the model prices into the debt.

**Determinism:** **DETERMINISTIC**: everything after the inputs. A script takes `(S, K, t, sigma, r)` and returns equity value, implied debt value, and the implied interest rate on debt. The base case returns $75.94 million, $24.06 million, and 12.77%. **JUDGMENT**: the value of the firm `S`, which requires either a market-value cumulation or a full FCFF valuation. The variance in **firm** value `sigma^2`, which is not directly observable for a levered firm and must be constructed. The effective life `t` when debt is not a single zero-coupon issue. And whether the four simplifying assumptions are close enough to reality to make the output meaningful for this particular firm.

**Pitfalls:**
- Using the variance of *equity* where the model wants the variance of *firm value*. Equity in a levered firm is far more volatile than the firm.
- Treating the four simplifying assumptions as harmless. Multiple debt issues, coupons, convertibility and put clauses all break the clean mapping.
- Reading a positive equity value as evidence that the firm is healthy. It may reflect nothing but option time value; see [[distressed-equity-time-value]].
- Using a short riskless rate against a ten-year option life.
- Forgetting that this model treats equity and debt as the only claims. Preferred stock, leases and pension obligations all sit somewhere and must be handled explicitly.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket3spr21 p.62-66, p.77
- valuations--lecture_notes--spring_2020--valpacket3spr20 p.62-66, p.77

**Related:** [[distressed-equity-time-value]], [[risk-shifting-and-stockholder-bondholder-conflict]], [[conglomerate-merger-wealth-transfer]], [[equity-option-inputs-troubled-firms]], [[black-scholes-model]], [[option-payoffs-and-determinants]], [[real-options-framework]], [[cost-of-debt]], [[financial-distress]]
