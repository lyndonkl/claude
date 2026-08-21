# Three schools of thought on dividends and MM irrelevance

**Core idea:** Whether dividends affect firm value depends entirely on the assumptions you make about taxes, issuance costs and managerial behavior. Three positions follow. **Dividends are irrelevant** if dividends carry no tax disadvantage and firms can issue stock costlessly whenever they need cash. **Dividends are bad** if investors pay more tax on dividends than on capital gains, so raising dividends lowers value. **Dividends are good** if dividends carry a tax advantage or stockholders simply like them, so raising dividends raises value. The Miller-Modigliani (MM) irrelevance proposition is the anchor: hold investment policy fixed, and value cannot change with the dividend, because the higher dividend yield is exactly offset by lower price appreciation. The practical resolution is the balanced view: paying out is good when the firm has excess cash and few good projects, and bad otherwise.

**Formulas:**
- MM logic. If investment policy is fixed, cash flows are fixed, so firm value V is fixed. A firm paying an extra dividend D must raise D in new equity to fund the same projects. Existing holders receive D in cash and give up D in market value. Total return is unchanged:
  Total Return = Dividend Yield + Price Appreciation, and MM says raising the first lowers the second one-for-one.
- Tax comparison for an investor choosing between a dollar of dividend and a dollar of capital gain:
  After-tax value of dividend = D × (1 − t_o); After-tax value of capital gain = G × (1 − t_cg), where t_o = tax rate on ordinary income/dividends and t_cg = tax rate on capital gains. Dividends are penalized when t_o > t_cg.
- Balanced-view decision rule: Return cash if (Excess cash > 0) AND (few or no projects with NPV > 0). Retain cash if (no excess cash) OR (several projects with NPV > 0).

**MM's three underlying assumptions (each is also the point at which the theory breaks):**
(a) No tax differences between dividends and capital gains.
(b) A firm that pays out too much can issue new stock with no flotation costs and no signaling consequences.
(c) A firm that pays out too little does not waste the retained cash on bad projects or acquisitions.

**Procedure:**
1. Check assumption (a) for the investor base and jurisdiction. Compare the tax rate on dividends with the tax rate on capital gains for the marginal investor. In the US since 2003 these are equal, so the "dividends are bad" case is much weaker than the historical record suggests.
2. Check assumption (b). Estimate the flotation cost of re-raising the cash later (see [[bad-reasons-for-paying-dividends]] for the cost table). Large firms issuing more than $50M face roughly 3.5% on equity; small issuers face 15–22%. The higher the flotation cost, the more expensive it is to pay out cash now and re-raise it.
3. Check assumption (c). This is the trust question. Look at ROE vs cost of equity and ROC vs cost of capital over the past 5–10 years. A firm that destroys value with retained cash violates (c), and paying dividends becomes value-increasing even if MM's other assumptions hold.
4. Apply the balanced view. Estimate excess cash (cash beyond operating needs, or FCFE not yet returned) and the quality/quantity of NPV > 0 projects. Recommend paying out only where excess cash exists and the project pipeline is thin.
5. State which school you are implicitly using when you make a recommendation. Any statement like "the firm should raise its dividend to support the stock" is a claim that dividends are good — you must then name the mechanism (clientele, signaling, or discipline), not just assert it.

**Reference data:**

*US tax rates on dividends vs capital gains, 1916–2015 (from Figure 10.10, approximate):*

| Era | Top rate on dividends | Top rate on capital gains | Gap |
|---|---|---|---|
| 1940s–1960s | ~90–94% (peak) | ~25% | Up to 66 percentage points (peak in the 1950s) |
| 1970s | ~70% | ~28–35% | Large |
| 1981–1985 | 50% | 20% | 30 pts |
| 1986–1990 | 28% | 28% | 0 |
| 1991–2002 | ~39.6% | ~20% | ~20 pts |
| 2003 onward | Same as capital gains (~15–24% recently) | ~15–24% | 0 |

The "dividends are bad" school rests on a tax penalty that was enormous for four decades and has been zero since 2003.

*Survey of manager beliefs (what practitioners actually think):*

| Statement | Agree | No opinion | Disagree |
|---|---|---|---|
| 1. A firm's dividend payout ratio affects the price of the stock | 61% | 33% | 6% |
| 2. Dividend payments provide a signaling device of future prospects | 52% | 41% | 7% |
| 3. The market uses dividend announcements to assess firm value | 43% | 51% | 6% |
| 4. Investors perceive dividends and retained earnings as differently risky | 56% | 42% | 2% |
| 5. Investors are basically indifferent between dividends and capital gains | 6% | 30% | 64% |
| 6. Stockholders are attracted to firms whose dividend policy fits their tax environment | 44% | 49% | 7% |
| 7. Management should be responsive to shareholder dividend preferences | 41% | 49% | 10% |

Managers overwhelmingly reject MM: only 6% agree investors are indifferent.

**Worked example:** A US investor in 1955 choosing between a firm that pays $1 of dividends and one that retains it and delivers $1 of price appreciation. Dividend route: $1 × (1 − 0.90) = $0.10 after tax. Capital gain route: $1 × (1 − 0.25) = $0.75 after tax. The dividend destroys 65 cents of after-tax value per dollar — the "dividends are bad" school in one line. Repeat the same calculation in 2020 with t_o = t_cg = 20%: $0.80 either way, and the tax argument disappears. This is why the empirical ex-dividend price drop moved from 78% of the dividend in 1966–69 toward 90%+ once rates converged (see [[ex-dividend-day-and-dividend-capture]]).

**Determinism:**
- DETERMINISTIC: the after-tax comparison of a dividend versus a capital gain given t_o and t_cg. The flotation-cost lookup. The excess-cash calculation once FCFE and a target cash balance are set.
- JUDGMENT: identifying the marginal investor and their tax rates. Assessing whether management would waste retained cash (assumption c). Deciding whether the project pipeline counts as "several NPV > 0 opportunities". Choosing which school applies to this firm's investor base.

**Pitfalls:**
- Treating MM irrelevance as a description of the world rather than as a benchmark that isolates what must be true for dividends to matter. The value of MM is in its assumptions, not its conclusion.
- Forgetting that MM holds *investment policy fixed*. Most real dividend decisions change investment policy, and then value does change — but through the investment decision, not the dividend.
- Applying pre-2003 US "dividends are bad" logic to a post-2003 investor base, or to tax-exempt and foreign holders for whom the penalty never applied.
- Arguing that dividends are good because the stock price rises on the announcement, which conflates the signal with the cash transfer (see [[dividend-signaling]]).
- Ignoring assumption (c). At a firm with a poor project record, the strongest argument for dividends has nothing to do with taxes or clienteles — it is that retained cash gets destroyed.

**Sources:**
- corporate_finance--lecture_slides--cfpacket2spr20 p.164-167
- corporate_finance--lecture_slides--cfpacket2spr20 p.187

**Related:** [[ex-dividend-day-and-dividend-capture]], [[bad-reasons-for-paying-dividends]], [[clientele-effect]], [[dividend-signaling]], [[dividend-wealth-transfer]], [[cash-trust-assessment]]
