# The Classical Objective Function and Its Four Assumptions

**Core idea:** "Maximize the stock price" works as an objective only if four links in a chain hold. Stockholders must control managers. Bondholders must be protected. Managers must tell markets the truth on time, and markets must price it well. And the firm's costs must all land on the firm, not on society. When all four hold, a higher stock price means higher stockholder wealth and no one else is harmed. Break any one link and the objective is undermined. An analyst uses this chain as a diagnostic checklist: test each link for the company in front of you, and the failures tell you which objective you can actually use.

**Formulas:** No arithmetic. The chain, stated as a conjunction:

```
Stock price maximization is valid IF AND ONLY IF
  (1) Stockholders control managers          (board + annual meeting work)
AND (2) Bondholders are protected            (covenants or reputation)
AND (3) Managers inform honestly AND markets are efficient
AND (4) No untraced social costs             (all costs charged to the firm)
```

The four failure modes, one per link:

| # | Link | Theory | What goes wrong in practice |
|---|---|---|---|
| I | Stockholders ↔ Managers | Stockholders hire and fire managers via board and annual meeting | Stockholders have little control; managers put their own interests first |
| II | Bondholders ↔ Managers | Bondholders lend, their interests are protected | Bondholders get ripped off (expropriated) |
| III | Managers ↔ Financial Markets | Managers reveal information honestly and promptly; markets assess value | Managers delay or spin bad news; markets make mistakes and overreact |
| IV | Managers ↔ Society | All costs trace back to the firm | Large social costs; some cannot be traced to the firm |

**Procedure:** Running the four-link diagnostic on a real company:
1. **Link I.** Count inside directors. Check whether the CEO is also chair. Check the ownership register for a blockholder who can discipline management. Check the last three annual meetings for contested votes. See [[manager-stockholder-agency-conflict]] and [[board-independence-assessment]].
2. **Link II.** Read the covenants on outstanding debt. Look for recent dividend surges, leverage increases, or shifts into riskier businesses funded on old debt. See [[stockholder-bondholder-conflict]].
3. **Link III.** Check restatements, SEC actions, and the timing of bad-news releases. Check whether the stock is liquid and analyst-covered. See [[firms-and-financial-markets]].
4. **Link IV.** List the firm's externalities — pollution, congestion, health, safety — and ask which are already priced or regulated. See [[firms-and-society-social-costs]].
5. Record a pass/fail for each of the four links.
6. Map the failures to an objective using [[modified-objective-function]]. Any Link III failure pushes you from stock price to stockholder wealth. Any Link II failure pushes you from stockholder wealth to firm value. Link I and Link IV failures do not change the objective; they change the *constraints* you attach to it (see [[self-correction-and-counter-forces]]).

**Reference data:** The two poles of the diagnostic, stated as end games.

*Utopian corporatism* — all four links hold. Shareholders own the company with equal voting rights. The board checks the CEO, and shareholders vote at annual meetings. Bondholders are fully protected, by covenant or by reputation. The firm maximizes stock price in efficient markets with full information. It wins by making better products or charging lower prices, so the sector is winnowed to the best firms. Unions or a tight labor market even the game, so wages are fair. Every cost the firm creates is traced and charged to it, so society bears nothing. Customers are treated well and come back. End game: managers maximizing stock price also maximize stockholder wealth, every other stakeholder gets its due, and society is better off.

*The full breakdown* — all four links fail at once. This is the "what can go wrong" diagram, and it is the mirror image of the classical one.

**Worked example:** Disney in 1997. Link I fails outright: the board was packed with insiders and CEO associates, and Disney was the only S&P 500 firm to fail all three CalPERS independence tests. Link III held reasonably — Disney was liquid and widely covered. Link II held — Disney's debt was investment grade and covenanted. Link IV was not a major issue for a media company. Diagnosis: a Link I failure only. So the objective for Disney stays "maximize stock price," but the analyst should expect agency costs, and should discount management's claims about value-creating acquisitions. That expectation was borne out: the ABC deal, the halving of the stock 1998-2002, and the 2004 shareholder revolt.

**Determinism:**
- DETERMINISTIC: the logical combination once each link is scored (four booleans -> valid/invalid, and -> which objective); counting inside directors; checking CEO/chair duality; checking whether covenants exist.
- JUDGMENT: scoring each link. Every one of the four requires reading evidence and weighing it. "Are markets efficient enough?" and "are social costs significant?" have no threshold in the source.

**Pitfalls:**
- Treating the classical model as a description of reality. It is a set of assumptions, and the course spends the next sixty slides breaking each one.
- Treating the failure of any single link as fatal to stock-price maximization. The source's own answer (Solution III) is to keep the objective and fix the linkage — see [[self-correction-and-counter-forces]].
- Assuming the links are independent. They are not: a captive board (I) makes information games (III) easier, and both make expropriation (II) easier.
- Testing the links once and assuming they stay fixed. Governance drifts — see [[disney-governance-case-study]].

**Sources:**
- corporate_finance--lecture_slides--cfpacket1spr20 p.9-11
- corporate_finance--lecture_slides--cfpacket1spr20 p.10
- corporate_finance--lecture_slides--cfpacket1spr20 p.46-47

**Related:** [[objective-function-and-stock-price-maximization]], [[manager-stockholder-agency-conflict]], [[stockholder-bondholder-conflict]], [[firms-and-financial-markets]], [[firms-and-society-social-costs]], [[modified-objective-function]], [[corporatism-archetypes]], [[self-correction-and-counter-forces]]
