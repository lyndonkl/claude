# The Modified Objective Function

**Core idea:** This is where the whole governance module lands. The right objective for a company is not fixed. It depends on two things: whether markets are efficient for that company's stock, and whether its lenders are protected. Run those two tests, add the question of whether the firm is even publicly traded, and a decision matrix hands you the objective. Efficient markets plus protected lenders lets you use the stock price. Break efficiency and you fall back to stockholder wealth. Break lender protection too and you fall back to firm value. This is the rule an analyst applies before writing a single line of valuation, because it determines what number the analysis is trying to maximize.

**Formulas:** The objective selection matrix.

```
INPUTS
  T = Is the firm publicly traded?          (yes / no)
  E = Are markets reasonably efficient?     (yes / no)
  B = Are bondholders/lenders protected?    (yes / no)

RULE
  T=yes, E=yes, B=yes  -> MAXIMIZE STOCK PRICE
                          (this also maximizes firm value)
  T=yes, E=no,  B=yes  -> MAXIMIZE STOCKHOLDER WEALTH
                          (also maximizes firm value, but might not
                           maximize the stock price)
  T=yes, E=no,  B=no   -> MAXIMIZE FIRM VALUE
                          (stockholder wealth and stock price may not
                           be maximized at the same point)
  T=no,         B=yes  -> MAXIMIZE STOCKHOLDER WEALTH
  T=no,         B=no   -> MAXIMIZE FIRM VALUE
```

Definitions: *Stock price* = the market's estimate of equity value per share. *Stockholder wealth* = the intrinsic value of equity, whether or not the market agrees. *Firm value* = the value of the whole business, equity plus debt. The nesting matters: firm value is the broadest and safest objective, stock price the narrowest and most demanding.

**Procedure:** Selecting the objective for a real company:
1. **Test T.** Is the equity publicly traded and liquid? A listing alone is not enough — a stock with negligible float and volume behaves like a private firm.
2. **Test E.** Are markets reasonably efficient for this stock? Evidence to gather: trading volume, bid-ask spread, free float, analyst coverage, options market depth, restatement and fraud history, and the timing pattern of bad-news releases. See [[firms-and-financial-markets]].
3. **Test B.** Are lenders protected? Evidence to gather: covenants on outstanding debt, debt maturity, presence of puttable or ratings-sensitive structures, and any recent history of payout surges, risk shifting, or claim dilution. See [[stockholder-bondholder-conflict]].
4. Apply the matrix and state the objective in one sentence.
5. Note what the two remaining failures — the manager-stockholder conflict and social costs — do *not* change. They do not change the objective. They change the constraints you attach to it, and the agency cost you build into your forecasts. See [[self-correction-and-counter-forces]] and [[firms-and-society-social-costs]].
6. Carry the objective forward. It sets which value you compute, which decisions you call value-creating, and how you judge management.

**Reference data:** The matrix in table form.

| Firm type | Markets efficient? | Lenders protected? | Objective | Note |
|---|---|---|---|---|
| Publicly traded | Yes | Yes | **Maximize stock price** | Also maximizes firm value |
| Publicly traded | No | Yes | **Maximize stockholder wealth** | Also maximizes firm value; might not maximize the stock price |
| Publicly traded | No | No | **Maximize firm value** | Stockholder wealth and stock price may not be maximized at the same point |
| Private | — | Yes | **Maximize stockholder wealth** | No stock price exists |
| Private | — | No | **Maximize firm value** | No stock price exists |

*The menu of objectives that were on the table before this rule resolves the question:* maximize stock prices; maximize stockholder wealth; maximize stockholder wealth with good corporate citizen constraints; maximize firm value; maximize stakeholder wealth; something else. The source poses this as an open class poll, then answers it with the matrix above. The "good corporate citizen constraints" variant is constrained corporatism, the archetype Damodaran endorses — see [[corporatism-archetypes]].

**Worked example:** Three companies, same rule.

*Disney (2020, US-listed).* T = yes, liquid and heavily covered. E = yes, no material disclosure failures, deep options market. B = yes, investment-grade debt with standard covenants. **Objective: maximize stock price.** The analyst can therefore treat Disney's stock price as the scoreboard, and read the 1998-2002 halving as a genuine verdict on management's decisions.

*A small emerging-market listed company with 8% free float, no analyst coverage, and a history of late filings.* T = yes technically, but E = no. B = yes, bank debt with maintenance covenants. **Objective: maximize stockholder wealth.** Do not use the stock price to judge management. Value the equity intrinsically and compare.

*A leveraged private company whose sole lender has no covenants and a 7-year bullet maturity.* T = no. B = no. **Objective: maximize firm value.** Any recommendation that raises equity value by expropriating the lender — a special dividend, a risk shift — is off the table, because it does not raise firm value.

**Determinism:**
- DETERMINISTIC: the matrix itself. Given the three booleans, the objective is a lookup with no discretion (T, E, B -> objective). Also deterministic: the liquidity and coverage statistics that feed test E, and the covenant inventory that feeds test B.
- JUDGMENT: all three booleans. "Reasonably efficient" has no threshold in the source. "Protected" has no threshold either. Both require reading evidence and forming a view. This is the classic pattern — a deterministic rule applied to judgment-based inputs.

**Pitfalls:**
- Defaulting to "maximize shareholder value" for every company without running the tests.
- Treating a stock exchange listing as proof of market efficiency. Float, volume and coverage matter more than the listing.
- Forgetting that firm value is the fallback for *both* failure paths. When in doubt, the broader objective is the safer one.
- Using the manager-stockholder conflict to justify abandoning stock price maximization. That conflict is not in the matrix. It changes constraints, not the objective.
- Assuming stockholder wealth and stock price move together when markets are inefficient. The whole point of the middle row is that they do not.
- Setting the objective once and never revisiting it. Liquidity, coverage and covenant protection all change over time.

**Sources:**
- corporate_finance--lecture_slides--cfpacket1spr20 p.74-75

**Related:** [[objective-function-and-stock-price-maximization]], [[classical-objective-function-assumptions]], [[firms-and-financial-markets]], [[stockholder-bondholder-conflict]], [[self-correction-and-counter-forces]], [[corporatism-archetypes]], [[alternative-objective-functions]], [[firms-and-society-social-costs]], [[first-principles-of-corporate-finance]], [[private-company-valuation]]
