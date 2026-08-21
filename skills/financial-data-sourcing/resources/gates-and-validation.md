# Gates, minimum dataset and validation

What has to be true before data leaves the collector, and the consolidated list of checks
the pipeline runs over it.

## The G1 predicate

`G1_data` passes when the universal minimum holds, the mode-specific additions hold, and no
blocking rule fires.

### Universal minimum

| Requirement | Fields |
|---|---|
| Identity | Mode, name or ticker, country of incorporation, valuation currency, valuation date, industry key |
| One full fiscal year of statements | Income statement through net income; a balance sheet that balances; a cash flow statement with all three sections |
| Debt boundary | Book debt — short-term, long-term and the current portion — plus either a lease schedule or a reported lease liability |
| Cash | Cash and marketable securities |
| Share base | Actual shares outstanding, or a private-firm equity-value proxy |
| Riskfree rate | A ten-year rate in the valuation currency, from any rung of the ladder |
| Equity risk premium | A mature-market premium at a stated vintage |
| Beta path | A comparable set, or an industry unlevered beta |
| Tax rate | A marginal rate for the domicile |
| Reference vintage | Every vintage-critical table loaded at one consistent `as_of` |

### Mode-specific additions

| Mode | Additional minimum |
|---|---|
| `valuation` | Three or more years of statements, five preferred; a growth-driver route with its inputs; terminal-value inputs |
| `corporate-finance` | Ten years of operating income history for volatility; the ownership breakdown; five years of dividends and buybacks; a peer group; EBITDA and capital expenditure |
| `acquisition` | Full sets for both target and acquirer; named synergy assumptions |
| `project` | The project's cash-flow schedule and life; the divisional business classification; the project's currency and country |
| `ipo` | The private-company set, plus the use of proceeds, prior equity claims, and the post-issue share count and options |
| `restructuring` | The status-quo set, plus the optimal-structure inputs, plus a target return-on-capital assumption |

### Blocking rules

- The balance-sheet tie, the net-income tie or the cash tie failing blocks the run. The
  statements are not internally consistent, so nothing downstream is trustworthy.
- A vintage-critical table missing with no fallback blocks.
- A live requirement for a failure probability with no source and no table fallback blocks.
- A live requirement for a total beta with no comparable R² blocks.
- Statements older than eighteen months with no interim filing block a valuation. They
  degrade to stale for corporate-finance work.
- Geography weights defaulted to the country of incorporation do not block a firm carrying
  country risk above zero. They carry a mandatory disclosure and a required sensitivity.

## Validation catalogue

Grouped by what each group protects. The cross-artifact validator that runs these lives in
the `valuation-consistency-checks` skill.

**Statement integrity.** The balance sheet balances. Net income ties into operating cash
flow. Retained earnings roll forward. Depreciation ties across statements. The cash tie
closes. Segments reconcile to consolidated revenue.

**Adjustment integrity.** Lease capitalization leaves net income unchanged. R&D
capitalization leaves free cash flow to the firm unchanged, because earnings and
reinvestment rise by the same amount. Every earnings adjustment has a matching capital
adjustment. The quality-of-earnings trend is computed. Excise taxes are stripped for a
commodity filer. A bank's revenue is built from net interest, net fee and trading income.

**Matching.** Currency, claimholder, nominal against real, vintage, and the debt
convention. The same tax rate appears in the beta relevering and in the after-tax cost of
debt. The same debt-to-equity ratio appears in the beta relevering and in the cost-of-
capital weights.

**Single count.** The tax shield, country risk, options against dilution, cash,
cross-holdings, failure risk, downside protection, complexity, real options, control value.

**Forecast consistency.** Growth equals the reinvestment rate times the return on capital
in every explicit year. The implied marginal return is plausible. The absolute revenue
level in the terminal year is plausible against market size. Growth stays inside the
market's ceiling. Growth and reinvestment are never set independently. Working capital is
not double-counted alongside a sales-to-capital reinvestment. Loss carryforwards do not
extend into the terminal year.

**Terminal.** Growth does not exceed the riskfree rate. Reinvestment equals growth divided
by the return on capital. The implied perpetual return is computed and reported. Beta, the
debt ratio and the country premium are all at mature levels.

**Bridge.** Every line has a value or an explicit zero with a reason. Actual shares, not
diluted. The book-or-market debt convention is declared and matches the weights.

**Statistical.** Report t-statistics and R² and honour their thresholds. Use medians rather
than means. Record dropped-observation counts. Record which units form each set of
regression coefficients uses, because a decimal-against-percent mismatch is a silent factor
of one hundred.

## Diagnostics

None of these blocks a run. Each one means an input is probably wrong, and each deserves a
second look before the report ships.

- A value-to-price ratio above two or below one half.
- A marginal return on capital far above the firm's own history.
- The equity risk premium divided by the Baa spread far from two.
- A synthetic rating more than two notches from the actual rating.
- A peer group whose average free cash flow to equity is negative.
- A regression with R² below fifteen percent carrying a recommendation.
