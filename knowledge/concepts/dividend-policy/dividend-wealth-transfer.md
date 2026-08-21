# Dividends as a wealth transfer from lenders to stockholders

**Core idea:** The third defensible reason for paying dividends is uncomfortable but real. Cash on the balance sheet is collateral for lenders. Paying it out to stockholders shrinks the asset base backing the debt, raises the effective leverage of the remaining firm, and increases default risk. Equity gains at the expense of debt. The event-study evidence confirms it: around dividend increases, stock prices rise while bond prices fall. This is good for equity investors and bad for lenders, which makes it a reason for stockholders to want dividends and a reason for lenders to write covenants against them.

**Formulas:**
- Book effect of a cash dividend of D: Cash falls by D, Book equity falls by D, Debt unchanged. So Debt/Equity and Debt/(Debt+Equity) both rise mechanically.
- Net debt effect: Net Debt = Total Debt − Cash. Paying a dividend of D from cash raises net debt by D without issuing a single bond.
- Wealth transfer measure from an event study: Transfer ≈ (ΔBond value) measured as Bond CAR × Market value of debt, set against Stock CAR × Market value of equity. A negative bond CAR paired with a positive stock CAR is the signature of the transfer.
- Coverage deterioration: if the dividend is funded by new debt, Interest coverage = EBIT / Interest expense falls, and the default spread and cost of debt rise with it.

**Procedure:**
1. Identify whether the firm has meaningful debt outstanding. With no debt there is no transfer, and this reason for dividends does not apply.
2. Measure the balance-sheet effect of the proposed payout. Recompute the debt ratio, net debt, and interest coverage after removing the cash. A payout that pushes the firm across a rating threshold is a large transfer.
3. Check the bond indentures. Most debt contracts written by sophisticated lenders contain dividend restriction covenants precisely because of this effect. A payout that breaches a covenant is not available.
4. If the transfer is large, expect lenders to price it into any future borrowing. The gain to stockholders today is partly paid back through a higher cost of debt tomorrow, so the transfer is not free money for a firm that will borrow again.
5. Use this as an explanatory factor, not a recommendation. Damodaran lists it among the "good" reasons because it genuinely benefits stockholders, and simultaneously flags it as the reason lenders resist.
6. When valuing the firm, do not double count. A dividend-driven wealth transfer moves value between claimholders; it does not create firm value.

**Reference data — event study of excess returns around dividend increases:**

| Security | Cumulative abnormal return around the announcement |
|---|---|
| Stock | drifts up to about **+0.5%** |
| Bond | falls to about **−1.5% to −2%** |

Stock prices rise and bond prices drop on the same announcement. This is the empirical support for the wealth-appropriation story.

For context, the three "good" reasons for paying dividends are: (1) the **clientele effect** — your investors like dividends (see [[clientele-effect]]); (2) the **signaling story** — dividends tell the market that management expects good cash flows (see [[dividend-signaling]]); (3) the **wealth appropriation story** — this concept.

**Worked example:** A firm has a market value of equity of $8 billion and market value of debt of $2 billion, and announces a large dividend increase. Applying the event-study magnitudes: equity gains 0.5% × $8,000M = **+$40M**; debt loses 1.75% (midpoint of the −1.5% to −2% range) × $2,000M = **−$35M**. Almost the entire equity gain is accounted for by the loss to lenders — total firm value barely moves. The stockholders are better off, but nothing was created; value moved across the capital structure. Note also that the same announcement carries a signaling component (see [[dividend-signaling]]), so the observed stock CAR blends both effects and cannot be attributed cleanly to the transfer.

**Determinism:**
- DETERMINISTIC: the post-dividend debt ratio, net debt, and interest coverage from the balance sheet and the dividend amount. Bond and stock CARs from price data. The dollar transfer estimate given CARs and market values of debt and equity.
- JUDGMENT: separating the wealth-transfer component of the stock reaction from the signaling component. Assessing whether covenants permit the payout. Estimating how much lenders will charge next time to compensate. Deciding whether the transfer is large enough to matter at this leverage level.

**Pitfalls:**
- Presenting the wealth transfer as value creation. Firm value is unchanged; only the split changes.
- Ignoring dividend restriction covenants, which make the transfer unavailable at most levered firms.
- Applying the argument at an unlevered or cash-rich firm where it has no force.
- Assuming the transfer is repeatable. Lenders reprice, and a firm known for stripping collateral pays more for debt.
- Attributing the whole stock-price rise on a dividend increase to the transfer. The bond reaction is the only clean evidence of the transfer itself.

**Sources:**
- corporate_finance--lecture_slides--cfpacket2spr20 p.177
- corporate_finance--lecture_slides--cfpacket2spr20 p.186

**Related:** [[clientele-effect]], [[dividend-signaling]], [[three-schools-of-dividend-thought]], [[cash-returned-dividends-and-buybacks]], [[buyback-value-and-eps-effect]]
