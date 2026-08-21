# Balance sheet: dueling views and asset measurement

**Core idea:** Three rival schools disagree about what a balance sheet should measure. The first says it should record how much a business has invested in its assets-in-place; this is Damodaran's own preferred view. The second, held by a large and perhaps dominant school of rule-writers, says it should reflect the business's value today — fair value. The third, pushed by lenders, says it should show liquidation value. Modern balance sheets try to serve all three and end up measuring none of them cleanly. The practical consequence: the only items you can really trust are cash and marketable securities, which are not subject to accounting nuance, and interest-bearing debt, which closely measures what is owed.

**Formulas:**
- `Assets = Liabilities + Shareholders' Equity` (with a mezzanine layer where one exists, as in Toyota's Model AA class shares).
- Historical-cost carrying value: `Net Fixed Assets = Original Cost − Accumulated Depreciation`.
- Book-to-market divergence indicator: `Divergence ≈ f(asset age, asset type)`. Divergence is larger for older assets than newer ones, and larger for fixed assets than current assets.
- Reliable-value core: `Trustworthy book items = Cash + Marketable Securities + Interest-bearing Debt`. Treat everything else as neither invested capital nor fair value.
- `Book age of asset base = Accumulated Depreciation / Gross PP&E`. A high ratio means an old asset base and therefore a wide cost-versus-value gap.

**Reference data:** The standard structure, both sides.

| Asset category | Description | Liability/equity category | Description |
|---|---|---|---|
| Fixed Assets | Long-lived physical assets | Current Liabilities | Short-term obligations |
| Current Assets | Short-lived assets | Debt | Long-term debt |
| Financial Assets | Investments in securities & other businesses | Other Liabilities | Other long-term obligations |
| Intangible Assets | Assets which are not physical | Equity | Shareholders' equity |

The three views of what the balance sheet should measure.

| View | Claim | Who holds it |
|---|---|---|
| Record of capital invested | Should record how much the business put into the assets that let current operations run | Damodaran's preferred view; old-time historical-cost accounting |
| Measure of current value | Should reflect the value of the business today (fair value) | A large, perhaps dominant school of accounting rule-writers |
| Liquidation value | Should show what you would get if you sold off the firm's assets today | Lenders to the firm |

Measurement basis by asset type:

| Asset type | Old way | New way |
|---|---|---|
| Fixed assets | Original cost net of accounting depreciation | Marked toward current market value under fair-value standards |
| Current assets | Original cost | Closer to market; the gap is smaller than for fixed assets |
| Publicly traded securities | Cost | Almost always marked to current market prices |
| Minority stake held for trading | — | Marked to market |
| Minority stake held long-term | Book value | Book value |
| Bank debt | Amount first borrowed | Mostly still the amount first borrowed |
| Corporate bonds due | Face/issue value | Mostly not marked to market |

**Procedure:**
1. Map every line on the balance sheet into one of the four asset categories and one of the four liability/equity categories. Nothing may be left unclassified.
2. Confirm the identity balances, including any mezzanine equity and noncontrolling interests.
3. Separate the trustworthy items. Extract cash and marketable securities on the asset side, and interest-bearing debt on the liability side. These carry into valuation directly.
4. For every other asset, ask which measurement basis produced the number: historical cost, fair value, or a mixture.
5. Estimate the cost-versus-value gap. Use the accumulated-depreciation ratio for PP&E and the asset's age. Older and more fixed means a wider gap.
6. Do not read book equity as the value of equity. Convert deliberately using [[financial-balance-sheet]].
7. Note the presentation order. IFRS filers list non-current assets first and often equity before liabilities; the content is the same, the order is not.

**Worked example:** Coca-Cola, 31 December 2019 ($ millions). Total assets 86,381 = total liabilities plus total equity 86,381 (total equity 21,098, of which 2,117 is noncontrolling interests). Trustworthy items: cash and equivalents 6,480, short-term investments 1,467, marketable securities 3,228, plus total debt of 31,769 from the debt footnote. Untrustworthy items dominate the rest: goodwill 16,764 and trademarks with indefinite lives 9,266 are acquisition residues, and equity method investments of 19,025 sit at a mixture of cost and equity-method roll-forward. Net PP&E of 10,838 is a historical-cost number for a firm whose real value is a brand that appears nowhere on this statement. That is the source's "mess" in one page: the statement measures neither invested capital nor fair value.

**Determinism:**
- DETERMINISTIC: the classification map from line item to category; the balance check; the extraction of cash, marketable securities and interest-bearing debt; the accumulated-depreciation ratio.
- JUDGMENT: assessing how far book value diverges from market value for each asset. That needs the asset's age, its type, the accounting-policy footnote, and an independent view of the business's earning power. Choosing which of the three views to apply is itself a judgment about purpose.

**Pitfalls:**
- Reading book equity as intrinsic equity value. Book equity has little hope of measuring it under either the old or the new rules.
- Assuming fair-value marking is complete. It has been muted on the liability side: bank debt sits at the amount borrowed and bonds are mostly not marked.
- Treating a large book asset base as evidence of a valuable business, or a small one as evidence of the opposite.
- Missing mezzanine equity and noncontrolling interests when checking that the sheet balances.
- Forgetting the balance sheet is a snapshot at a point in time, while the other two statements cover a period. Any ratio mixing them needs an average balance.

**Sources:**
- accounting__101--balance_sheet p.2-4
- accounting__101--financial_statements_overview p.5
- accounting__101--balance_sheet_illustrations p.5
- accounting__101--balance_sheet_illustrations p.15

**Related:** [[financial-balance-sheet]], [[intangibles-and-goodwill]], [[liabilities-debt-and-leases]], [[shareholders-equity-book-value]], [[non-operating-items-and-cross-holdings]], [[life-cycle-patterns-in-financial-statements]], [[invested-capital-and-return-on-capital]]
