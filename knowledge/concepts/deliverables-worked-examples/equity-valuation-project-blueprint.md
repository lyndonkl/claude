# Equity valuation project blueprint (the 6-step deliverable)

**Core idea:** The equity valuation project is a six-step deliverable applied to one stock per group member. It moves from story to intrinsic value, then to two relative benchmarks, then to an optional option-pricing case, and ends with one buy/sell/hold call. The point of the sequence is triangulation. No single method is trusted alone. The DCF carries the narrative, the sector regression tests the firm against its peers, the market regression tests it against every listed firm, and option pricing rescues the case where equity is a levered bet on survival.

**Formulas:** No formula of its own. Two hard rules carry numbers:
- Option-pricing trigger: use it when the negative-earnings firm's **market-value debt-to-capital ratio > 50%**.
- High-growth screen for the pick: **expected revenue growth > 25%**.

**Procedure:**
1. **Step 1 — Pick the companies.** One per member. The set must include a negative-earnings firm, a high-growth firm, a non-U.S. firm and a service firm. See [[project-company-selection]].
2. **Step 2 — Intrinsic (DCF) valuation.** Start with a *narrative*: your story of how the firm will evolve given its market and its rivals. Tie the story to the key numbers you will use as inputs. Then value the stock with a discounted cash flow model. Test how much the value shifts when the story changes. This is the "narrative and numbers" method — every DCF input must be backed by the story. See [[dcf-model-selection]] and [[dcf-sensitivity-analysis]].
3. **Step 3 — Relative valuation against comparables.** Build a peer list using criteria you can defend. Pick one multiple for the whole group; you may need to try a few first. Judge the firm two ways: qualitatively adjust the peer average for differences, and run a sector regression of the multiple on its drivers. See [[relative-valuation-comparables-regression]].
4. **Step 4 — Relative valuation against the market.** Take the latest market-wide regression posted on Damodaran's site, combined with the multiple chosen in Step 3. Judge the firm against the whole market rather than its sector. A non-U.S. firm with a U.S.-listed ADR may use the U.S. market regression. Optional stretch: run your own regression in the foreign market on the 50 largest firms there. See [[market-wide-multiple-regression]].
5. **Step 5 — Option pricing, conditionally.** Apply it only to the negative-earnings firm, and only if it is highly levered. Threshold: market-value debt-to-capital above 50%. Otherwise skip. See [[equity-as-call-option-valuation]].
6. **Step 6 — Final value estimate and recommendation.** First check the news from the analysis period. Ask whether any event has changed your narrative and therefore your valuation, and update for it. Then line up the DCF, relative and option values, reconcile them into one view, and close with a buy, sell or hold call on every stock in the group. See [[valuation-triangulation-and-recommendation]].

**Reference data:**

Deadline structure (Spring 2019 instance):

| Deliverable | Timing | Graded? |
|---|---|---|
| Steps 1-2 (company picks + DCF valuations) | Midway through semester, March 29, 5 pm | Not graded; reviewed and returned with comments |
| Full project report (all six steps) | Last day of class, May 13, 5 pm | Graded |

Resource page for high-growth and negative-earnings firms: `http://www.stern.nyu.edu/~adamodar/New_Home_Page/eqass.htm`.

**Worked example:** A six-company student project (Affiliated Computer Services, Apple, Biosite, Gundle Environmental, Infosys, Nextel Partners) executes all six steps. Each company gets: a model-choice paragraph and assumption table, a DCF value per share, a sensitivity grid, a sector-comparables regression, a market regression, an EVA check, and a final table listing current price against every value estimate with a BUY or SELL verdict. Nextel Partners — negative earnings, 39% debt ratio, deeply distressed — additionally gets a Black-Scholes equity-as-call valuation. Infosys, the non-U.S. pick, is valued in rupees on its local listing and additionally gets a value-of-control and merger-synergy analysis.

**Determinism:** DETERMINISTIC — the step sequence, the required output list per company, the option-pricing trigger (debt/capital > 50% in market value), and the deadline structure. Once assumptions exist, every value estimate in Steps 2-5 is computable. JUDGMENT — the narrative itself, which inputs the narrative implies, the peer criteria, which multiple to use, which regression to trust, and the final reconciliation into one call.

**Pitfalls:**
- Running the DCF before writing the narrative. Numbers with no story behind them cannot be defended when the story changes.
- Reporting DCF, relative and option values side by side without reconciling them. Step 6 explicitly forbids reporting them in isolation.
- Forgetting the news check. An event during the analysis period can invalidate the narrative that produced the value.
- Applying option pricing to a firm that is merely unprofitable but not highly levered. The 50% market debt-to-capital gate exists precisely to stop this.

**Sources:**
- valuations--projects--eqprojspr19 p.1-8
- valuations--projects--valproject2 p.1

**Related:** [[project-company-selection]], [[dcf-model-selection]], [[dcf-sensitivity-analysis]], [[relative-valuation-comparables-regression]], [[market-wide-multiple-regression]], [[equity-as-call-option-valuation]], [[valuation-triangulation-and-recommendation]], [[corporate-finance-project-blueprint]], [[value-of-control-and-synergy]]
