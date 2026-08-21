# The Objective Function and Stock Price Maximization

**Core idea:** A firm can have only one objective. You cannot maximize two things at once, and with two goals no one can rank decisions or be held to account. Traditional corporate finance picks the value of the *firm*. A narrower choice is *stockholder wealth*. If the stock trades and markets work well, the narrowest choice is the *stock price*. Why put stockholders first? They hold the residual claim. Every other claimholder — lender, employee, customer, supplier — has a contract they can bargain over to protect themselves. Stockholders get only what is left. Why the stock price? It is easy to see, it updates all day, and if investors are rational it prices good and bad decisions right away, short term and long term alike.

**Formulas:** The financial balance sheet, which defines the three nested objectives:

```
        ASSETS                              LIABILITIES
Assets in Place    (existing investments   Debt   (fixed claim on cash flows,
                    generating cash flows           little/no management role,
                    today: long-lived fixed         fixed maturity, tax deductible)
                    assets + short-lived
                    working capital)
Growth Assets      (expected value of      Equity (residual claim on cash flows,
                    future investments)            significant management role,
                                                   perpetual life)
```

- `Firm value = Value(Assets in Place) + Value(Growth Assets) = Value(Debt) + Value(Equity)`  → "maximize firm value" targets the entire asset side.
- `Equity value = Firm value - Debt value` → "maximize stockholder wealth" targets the equity block.
- `Stock price = Market's estimate of Equity value / Shares outstanding` → "maximize the stock price" targets the market's *estimate* of the equity block.

Symbols: Assets in Place = investments already made; Growth Assets = present value of investments not yet made; Debt = fixed contractual claim; Equity = residual claim.

**Procedure:** Choosing the objective for a specific company:
1. Ask: is the equity publicly traded? If no, the stock price is unavailable — the objective is stockholder wealth (or firm value).
2. If traded, ask: are markets reasonably efficient for *this* stock (liquid, followed, priced on information)? If yes, stock price is a legitimate proxy for stockholder wealth.
3. Ask: are lenders protected (covenants, reputation, short maturities)? If yes, maximizing equity does not come at debt's expense, so maximizing stockholder wealth also maximizes firm value.
4. Only when steps 1-3 all pass may you use stock price as the objective. Otherwise step back to stockholder wealth or firm value per [[modified-objective-function]].
5. Having fixed the objective, rank every corporate decision by its effect on that one number. Do not add a second objective.

**Reference data:** The stakeholder map, used to identify who else has a claim and what protects them:

| Stakeholder | Relationship to the firm | What protects them |
|---|---|---|
| Shareholders | Invest equity, own the company | Board of directors, annual meeting, voting rights |
| Banks & bondholders | Lend money | Debt covenants, veto power over some actions |
| Employees | Make the products | Wages/benefits set by the labor market; unions |
| Customers | Buy the products | Product-market competition, consumer protection laws |
| Competitors | Offer similar products | Competition/antitrust law |
| Society | Receives side benefits, bears side costs | Laws and societal norms on acceptable behavior |

**Worked example:** Disney (publicly traded, NYSE-listed, heavily followed, investment-grade with covenanted debt). All three screens pass: traded ✓, reasonably efficient market ✓, lenders protected ✓. So for Disney the objective is legitimately "maximize the stock price," and the analyst can use Disney's 1998-2002 stock-price halving as direct evidence that the firm's decisions destroyed stockholder wealth. For a private family firm with a single bank lender and no covenants, the same test fails at steps 1 and 3, and the objective must be firm value.

**Determinism:**
- DETERMINISTIC: the balance-sheet identities (firm value, debt value -> equity value; equity value, share count -> stock price); the classification screen once the three yes/no answers are supplied.
- JUDGMENT: whether markets are "reasonably efficient" for this stock; whether lenders are "protected"; whether stockholders' residual-claim status justifies privileging them in a given legal/social environment.

**Pitfalls:**
- Adopting more than one objective. The slide is emphatic: you can have only one objective function, one interest group whose interests come first. Multiple objectives produce the paralysis described in [[alternative-objective-functions]].
- Treating "maximize stock price" as a choice *against* employees or customers. The source calls that a false trade-off. Employees in many firms are stockholders too. Firms that maximize stock price tend to be profitable, so they can afford to treat employees well. In most businesses, keeping customers happy *is* the route to a higher stock price. And a high stock price does not require breaking the law or flouting social norms.
- Conflating "maximize equity value" with "maximize stock price." They diverge whenever markets misprice the stock.
- Forgetting that Growth Assets are part of firm value — decisions that boost current earnings while destroying growth assets lower firm value even as they lift reported profit.

**Sources:**
- corporate_finance--lecture_slides--cfpacket1spr20 p.4
- corporate_finance--lecture_slides--cfpacket1spr20 p.5-6
- corporate_finance--lecture_slides--cfpacket1spr20 p.8

**Related:** [[first-principles-of-corporate-finance]], [[classical-objective-function-assumptions]], [[modified-objective-function]], [[alternative-objective-functions]], [[corporatism-archetypes]], [[firm-value-vs-equity-value]]
