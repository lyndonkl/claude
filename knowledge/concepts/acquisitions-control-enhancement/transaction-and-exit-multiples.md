# Transaction multiples, exit multiples and the EPS accretion fallacy

**Core idea:** Three relative-pricing arguments show up in almost every deal, and all three are traps. First, pricing off precedent transactions: acquirers on average overpay, so a sample of what other acquirers paid is a sample of overpayments. Matching it replicates their mistake. Second, exit multiples in terminal value: setting terminal value at "5x EBIT" smuggles today's market pricing into an intrinsic valuation, and assumes the market will pay the same multiple forever. Third, EPS accretion: buying any firm with a lower PE than yours mechanically raises your EPS, whether or not the deal creates a cent of value. Accretion is arithmetic, not evidence.

**Formulas:**
- Transaction-multiple price: `Price = Multiple from precedent deals × Target's metric`, e.g. `5 × EBIT`.
- Exit-multiple terminal value: `TV_n = Exit multiple × Metric_n`. Contrast with the intrinsic form, `TV_n = CF_{n+1} / (Cost of capital − g)`. The exit multiple form embeds a stationarity assumption: the market pays the same multiple in year n as it pays today.
- EPS accretion condition: an all-stock deal is accretive whenever `PE_acquirer > PE_target`. Post-deal EPS rises purely because you issue shares valued at a high multiple to buy earnings priced at a low multiple.

**Procedure:**
1. Value the target intrinsically first, with its own cash flows, growth, and cost of capital.
2. Use a perpetuity-growth terminal value, not an exit multiple. If an exit multiple is used at all, back out what growth and return on capital it implies and check those against a stable-growth firm.
3. When shown a precedent-transaction multiple, ask what the acquirers in that sample earned afterwards. If the sample is unscreened, it contains the overpayments and cannot set your price.
4. Screen any comparable set for genuine comparability — same growth, same risk, same reinvestment needs. A cherry-picked set can justify almost any price.
5. When told the deal is accretive, compute both PEs. If `PE_acquirer > PE_target`, note that accretion was guaranteed before any analysis and carries no information.
6. Ask the value question instead: does the price fall below the status-quo value, the restructured value, or the restructured value plus synergy?

**Reference data:** No lookup table. Two decision rules:
- Any multiple drawn from a sample of past acquisitions inherits that sample's overpayment bias.
- An exit multiple assumes today's market pricing of comparable companies persists into the terminal year — an assumption that must be stated and defended, not assumed.

**Worked example:** A banker presents a target with EBIT of $20 million. Precedent deals in the sector cleared at 5x EBIT, so the suggested price is `5 × 20 = $100 million`. Three checks follow.

- The precedent sample: those acquirers, on average, destroyed value. The multiple is a record of what buyers paid, not what the businesses were worth.
- The DCF defence fails too if the analyst sets terminal value at 5x EBIT. That is the same number wearing a DCF costume, and it commits the same sin inside an "intrinsic" model.
- The accretion argument: the acquirer's PE is 20, the target's PE is 10. EPS will rise after the deal. It would rise for *any* target with a PE below 20, including a terrible one. Accretion here proves nothing.

Compare with the HP/Autonomy defence, where the CEO cited a "D.C.F.-based model" and stressed the deal would be "on Day 1, accretive to H.P." Both claims were true and neither was evidence.

**Determinism:**
- DETERMINISTIC: multiplying a multiple by a metric; computing the two PEs and confirming accretion; converting an exit multiple into its implied growth and return on capital.
- JUDGMENT: whether a comparable set is genuinely comparable; whether a precedent sample is contaminated by overpayment; whether the market's current multiple can be expected to hold in the terminal year. Screening the sample for post-deal acquirer returns is the information this judgment needs.

**Pitfalls:**
- Believing a DCF is safe because it is a DCF. An exit-multiple terminal value usually dominates the total value, so the multiple sets the answer.
- Using sector pricing metrics built on firms with different growth and risk profiles.
- Reporting accretion/dilution as a deal test. It is a mechanical consequence of relative PEs.
- Being a lemming: "everyone in the sector is consolidating, so we must too." Sector activity is not a valuation argument.
- Letting a cherry-picked comparable set be assembled *after* the price is set. That is the verdict-first sin in relative-valuation clothing.

**Sources:**
- `valuations--lecture_notes--spring_2021--valpacket3spr21 p.104-106`
- `valuations--lecture_notes--spring_2020--valpacket3spr20 p.104-106`

**Related:** [[seven-sins-of-acquisitions]], [[deal-bias-and-ego]], [[three-reasons-and-acid-test]], [[terminal-value]], [[relative-valuation]], [[acquisition-price-buildup-and-goodwill]]
