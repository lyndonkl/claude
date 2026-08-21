# Distressed equity: why stock in a bankrupt firm is still worth something

**Core idea:** A catastrophic drop in firm value does not wipe out equity, and the option framing explains why. Equity is a call on the firm with a strike equal to the face value of debt. Even when firm value falls far below that face value — the option is deep out of the money — the call retains **time value** as long as there is volatility and time left before the debt comes due. Two consequences follow. Equity falls by *less* than the firm falls, so part of every loss is borne by debtholders. And stock in essentially bankrupt Chapter 11 firms still trades at a positive price, which no DCF of equity cash flows can explain.

**Formulas:**
- Equity value: `E = S x N(d1) - K x e^(-r*t) x N(d2)` with `S` = firm value, `K` = face value of debt.
- Naive (wrong) answer to a firm-value drop: `New equity = New firm value - Old market value of debt`. This understates equity, because the debt's market value also falls.
- Correct decomposition of a firm-value drop: `Change in firm value = Change in equity value + Change in debt value`. Both claims absorb part of the loss.
- Loss sharing: `Debtholders' share of the loss = Drop in firm value - Drop in equity value`.
- Equity stays strictly positive for any `S > 0` whenever `t > 0` and `sigma > 0`, however far `S` sits below `K`.

**Procedure:**
1. Do not conclude "debt exceeds firm value, so equity is worthless". That conclusion is only correct at the instant the debt matures.
2. Re-map the option inputs after the shock. Usually only `S` changes; `K`, `t`, `sigma^2` and `r` are unchanged.
3. Recompute the call. The result is the equity value.
4. Compute the implied debt value as firm value minus equity value.
5. Compare the drop in equity to the drop in the firm. The difference is what debtholders lost.
6. Read the sensitivity. Equity value declines smoothly as firm value falls and never reaches zero while time and volatility remain.
7. Use this to interpret distressed market prices. A traded equity price above zero in a firm with negative book equity is not irrational; it is the market pricing an out-of-the-money call.
8. When the shock also changes the firm's risk, update `sigma^2` too — and see [[risk-shifting-and-stockholder-bondholder-conflict]], where that is the whole story.

**Reference data:**

Equity value as firm value declines, with debt face value fixed at $80 million, `t` = 10 years, `sigma^2` = 0.16, `r` = 10%. Values read from the packet's chart, in $ millions:

| Firm value | Equity value (approx.) |
|---|---|
| 100 | 76 |
| 90 | 66 |
| 80 | 57 |
| 70 | 48 |
| 60 | 39 |
| 50 | 30 |
| 40 | 22 |
| 30 | 14 |
| 20 | 8 |
| 10 | 2 |

Note that at a firm value of $80 million — exactly the face value of debt, so the option is at the money — equity is still worth about $57 million, over 70% of firm value.

**Worked example:** The catastrophe case.

Start from the base firm in [[equity-as-call-option]]: firm value $100 million, debt face value $80 million (10-year zero-coupon), `sigma` = 40%, `r` = 10%. Equity is worth $75.94 million and debt $24.06 million.

A catastrophe halves the firm's value to $50 million. Face value of debt stays at $80 million. What is equity worth?

Three candidate answers were posed.

- (a) It drops to $25.94 million — $50 million minus the prior market value of debt.
- (b) It is worth nothing, since debt outstanding exceeds firm value.
- (c) It is worth more than $25.94 million.

New inputs: `S` = $50 million; `K` = $80 million; `t` = 10 years; `sigma^2` = 0.16; `r` = 10%. The call is now out of the money.

`d1` = 1.0515, `N(d1)` = 0.8534; `d2` = -0.2135, `N(d2)` = 0.4155.

`Equity = 50 x 0.8534 - 80 x e^(-0.10 x 10) x 0.4155 = $30.44 million`.

`Value of the bond = 50 - 30.44 = $19.56 million`.

The answer is (c). Equity fell from $75.94 million to $30.44 million — a drop of $45.50 million against a $50 million drop in firm value. Debtholders absorbed the remaining $4.50 million, their claim falling from $24.06 million to $19.56 million.

**Determinism:** **DETERMINISTIC**: the recomputation. Given `(S, K, t, sigma, r)` a script returns $30.44 million, the implied debt value of $19.56 million, and the whole sensitivity table by sweeping `S` from 100 down to 10. The loss-sharing arithmetic is subtraction. **JUDGMENT**: the post-shock firm value `S`, which in a real distressed situation is exactly the hardest number to pin down. Whether `sigma^2` really is unchanged after a catastrophe — distress usually raises volatility. Whether `t` is still the right horizon, since distressed firms often face acceleration clauses, covenant breaches and restructuring that shorten the effective maturity. And whether the two-claimant assumption survives contact with a real capital structure in default.

**Pitfalls:**
- Subtracting the *old* market value of debt from the new firm value. That is answer (a), and it is wrong because the debt's value fell too.
- Declaring equity worthless whenever debt exceeds firm value. That is answer (b), and it is only true at maturity.
- Concluding that a positive equity price means solvency. Deeply insolvent firms can carry substantial equity value on time value alone.
- Holding `sigma^2` fixed after a catastrophic shock. Real distress typically raises firm-value volatility, which *raises* equity value further.
- Ignoring that management, acting for equity holders, now has a strong incentive to increase risk. That is the subject of [[risk-shifting-and-stockholder-bondholder-conflict]].

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket3spr21 p.67-70
- valuations--lecture_notes--spring_2020--valpacket3spr20 p.67-70

**Related:** [[equity-as-call-option]], [[risk-shifting-and-stockholder-bondholder-conflict]], [[equity-option-inputs-troubled-firms]], [[black-scholes-model]], [[option-payoffs-and-determinants]], [[financial-distress]], [[going-concern-vs-liquidation]]
