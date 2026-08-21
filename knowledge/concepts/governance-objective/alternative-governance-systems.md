# Alternative Governance Systems (Solution I)

**Core idea:** When stockholders fail as monitors, one fix is to hand the monitoring job to someone else. Germany and Japan did exactly that, building governance on corporate cross-holdings rather than dispersed shareholders. In Germany banks form the core. In Japan the keiretsu does. Other Asian countries copied the model with family companies at the centre of corporate families. The system has a real upside and a real downside, and the downside includes a problem specific to analysts: cross-holdings make it very hard for outsiders, including investors in these firms, to tell how well or badly the group is doing.

**Formulas:** No arithmetic on the slide. The look-through arithmetic an analyst needs is in [[ownership-and-control-structure-analysis]]:

```
Group control (%) = SUM of stakes held by every affiliated entity
Look-through economic interest = product of ownership fractions
                                 down each layer of the pyramid
```

**Procedure:** Analyzing a company inside a cross-holding group:
1. Map the group. List every affiliated entity holding shares in the target, and every entity the target holds shares in.
2. Compute group control and the controlling family's or bank's look-through economic interest.
3. Ask the core question: does the group *support* the target, or *extract from* it? Look for intra-group loans, guarantees, transfer pricing, and related-party transactions.
4. Adjust reported financials for cross-holdings. Consolidated numbers may double-count, and equity-method holdings may hide losses at affiliates.
5. Discount your confidence in the reported numbers. Opacity is the structural cost of this system.
6. Assess whether minority shareholders in the listed entity can expect to receive their share of the cash flows, or whether value leaks to the group.

**Reference data:** The trade-off, as the source frames it.

| | Cross-holding governance (Germany, Japan, Asian family groups) |
|---|---|
| Structure | Germany: banks at the core. Japan: the keiretsus. Other Asian countries copied Japan, with family companies at the core of corporate families. |
| **At their best** | The most efficient firms in the group bring the less efficient firms up to par. The group provides a corporate welfare system and a more stable corporate structure. |
| **At their worst** | The least efficient firms drag down the best-run firms. |
| **The analyst's problem** | Cross-holdings make it very hard for outsiders — including investors in these firms — to tell how well or badly the group is doing. |

The three candidate solutions when traditional theory breaks down, of which this is the first:

| Solution | What it proposes | Verdict |
|---|---|---|
| **I. Non-stockholder governance** | Assign the job of monitoring managers to someone other than stockholders | This concept. Real upside, real opacity cost. |
| **II. A better objective than stock price** | Shift to a different metric, or to a different stakeholder group | See [[alternative-objective-functions]] |
| **III. Maximize stock price, minimize side costs** | Keep the objective, reduce the conflict: make managers and employees into stockholders, protect lenders from expropriation, provide honest and prompt information to markets, minimize social costs | Damodaran's choice. See [[self-correction-and-counter-forces]] |

**Worked example:** Tata Motors, 2013. Tata group entities held 34.47% in total — Tata Sons 26.07%, Tata Steel 5.49%, Tata Industries 2.54%, Tata Investment Corp 0.37%. The remaining register was splintered: the largest non-group holder, Citibank NA, held 16.56% (largely custodial), then Life Insurance Corp of India at 6.26% and Capital Group at 3.63%. So the Tata group controlled Tata Motors on roughly a third of the shares, via cross-holdings among group companies rather than a direct majority. Best case: the group's stronger companies support Tata Motors through a downturn — which is close to what happened around the Jaguar Land Rover acquisition. Worst case: Tata Motors is used to prop up weaker group members. An outside investor cannot easily tell which is happening, and that is the point.

**Determinism:**
- DETERMINISTIC: group control percentage and look-through interest from a holdings table (affiliate stakes -> group total, layer fractions -> look-through interest); counting related-party transactions disclosed in the notes.
- JUDGMENT: whether the group supports or extracts; whether reported group financials are reliable; whether the stability benefit outweighs the opacity cost for a given group.

**Pitfalls:**
- Treating cross-holding governance as strictly worse than the Anglo-American model. The source presents both a best case and a worst case.
- Taking group financials at face value. Opacity is the defining feature.
- Missing the control because no single holder crosses 50%. Sum the affiliates.
- Assuming a bank or family monitor aligns with minority shareholders. The monitor's interest is the group's, which may differ from the listed entity's.

**Sources:**
- corporate_finance--lecture_slides--cfpacket1spr20 p.48-49

**Related:** [[ownership-and-control-structure-analysis]], [[corporatism-archetypes]], [[alternative-objective-functions]], [[self-correction-and-counter-forces]], [[manager-stockholder-agency-conflict]], [[country-risk]]
