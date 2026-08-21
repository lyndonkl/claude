# Project company selection (screening rules for the analysis set)

**Core idea:** Both the corporate finance project and the equity valuation project begin by choosing the companies to analyze, and the choice is governed by explicit screens rather than taste. The corporate finance project screens for *analyzability* — the standard tools (betas, ROC, optimal debt ratios, FCFF) break down on financial firms, money losers, captive-finance arms and REITs — while the equity valuation project screens deliberately for *difficulty*, forcing the group to cover the hard cases (negative earnings, high growth, non-U.S., service firm). Choosing badly at this step wastes the whole project: a screened-out firm will produce meaningless hurdle rates and capital-structure conclusions.

**Formulas:** Only one numeric threshold appears in either screen: high-growth potential is defined as *expected revenue growth > 25%* over the near future.

**Procedure:**
1. **Group size.** Corporate finance project: self-formed groups of 4-8 people, one company per person. Equity valuation project: also one company per member.
2. **Corporate finance eligibility (all must hold):** publicly traded; at least one year of trading history; at least one set of annual financial statements; listed in any market worldwide.
3. **Corporate finance exclusions (any one disqualifies):**
   - Financial service firms — banks, insurance companies, investment banks (debt is raw material, not financing; regulatory capital distorts capital structure).
   - Money-losing companies (negative earnings break ROE/ROC, synthetic ratings and growth-from-fundamentals).
   - Companies with large capital/finance arms (e.g. GE, the auto makers) — the finance arm's leverage swamps the operating business.
   - Real estate investment trusts (REITs) — mandated payout and tax status distort dividend and capital-structure analysis.
4. **Corporate finance theme rule.** The group needs a common theme, broadly defined — an entertainment group may mix movie studios, TV broadcasters and syndication companies; an automobile group may mix auto makers, auto suppliers and even a dealership. Within the theme, maximize diversity: small and large, domestic and foreign, closely held and widely held.
5. **Equity valuation coverage rules (the group's set, taken together, must contain at least one of each):**
   - a firm with **negative earnings** in the most recent financial period (use year-to-date results if available, else the most recent financial year);
   - a firm with **high growth ahead** — revenues expected to grow more than 25% in the near future;
   - a **non-U.S.** firm, ideally valued in its local currency on its local listing;
   - a **service firm**, e.g. a retailer or a bank.
6. **Double-counting is allowed.** One pick may satisfy two tests — a money-losing high-growth firm covers both the negative-earnings and the high-growth requirement.
7. **Check downstream consequences before locking the pick.** A negative-earnings pick will need an n-stage model with a target growth path, and if its market debt-to-capital exceeds 50% it will also need an option-pricing valuation ([[equity-as-call-option-valuation]]). A non-U.S. pick will need local-currency risk-free rates and may need an ADR to use the U.S. market regression ([[market-wide-multiple-regression]]).

**Reference data:** Damodaran's resource page for high-growth and negative-earnings firms: `http://www.stern.nyu.edu/~adamodar/New_Home_Page/eqass.htm`.

Illustrative selection sets:

| Project | Companies | How the screens were satisfied |
|---|---|---|
| Corporate finance, Spring 2015 | Starbucks, McDonald's, Chipotle, Tyson Foods | Theme = food/restaurants; diversity = different life-cycle stages (rapid-growth CMG, mature MCD), different sub-industries (specialty coffee, fast food, fast casual, meat processing) |
| Equity valuation, ca. 2003 | Affiliated Computer Services, Apple, Biosite, Gundle Environmental, Infosys, Nextel Partners | Service firm = ACS/Infosys; high growth = Biosite/Gundle; non-U.S. = Infosys (India, Rs); negative earnings + high leverage = Nextel Partners |

**Worked example:** The Spring 2015 food group picked four firms at deliberately different maturity stages within one theme: Starbucks (specialty coffee, 65 countries, NASDAQ: SBUX), McDonald's (~35,000 outlets in 119 countries, ~80% franchised), Chipotle (fast casual, ~1,800 outlets, 200+ openings planned in 2015 — the growth pick), Tyson Foods (founded 1935, chicken/beef/pork/prepared foods — the mature, low-margin pick). None is a bank, a REIT, a money loser or a captive-finance owner, so all four survive the corporate finance screen, and the spread of maturities makes the cross-company comparisons in the executive summary meaningful.

**Determinism:** DETERMINISTIC — every hard screen is testable from data: public listing flag, ≥1 year of trading history, ≥1 annual statement, SIC/industry code in {banks, insurance, investment banks, REITs}, most recent net income sign, presence of a captive finance subsidiary, expected revenue growth > 25%, country of incorporation, service-sector classification. A script can accept or reject a ticker against all of these. JUDGMENT — what counts as a "common theme," how broadly to define it, how much diversity to seek, whether a borderline conglomerate has a "large capital arm," and which specific firm best represents a required category.

**Pitfalls:**
- Picking a bank or insurer because it is famous — the entire capital-structure half of the corporate finance project becomes meaningless.
- Picking a money-losing firm for the *corporate finance* project (it is explicitly excluded there) while it is explicitly *required* for the valuation project; the two screens pull in opposite directions and must not be confused.
- A theme so narrow that all firms have identical betas, debt ratios and payout policies — the cross-company comparison, which is the point, collapses.
- Forgetting that "at least one year of trading history" is what makes a regression beta possible at all.

**Sources:**
- corporate_finance--project--cfproj p.2-3
- valuations--projects--eqprojspr19 p.3
- corporate_finance--project--food2015 p.1, p.3
- valuations--projects--valproject2 p.1

**Related:** [[corporate-finance-project-blueprint]], [[equity-valuation-project-blueprint]], [[dcf-model-selection]], [[equity-as-call-option-valuation]]
