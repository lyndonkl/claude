# Ownership and Control Structure Analysis

**Core idea:** Who owns a company is not the same question as who controls it. An analyst must answer both. Pull the holdings register, then ask four things. Are the outside holders large or splintered, active or passive, short or long term? Do insiders hold a stake, and do they hold a superior class of voting shares? Is there a pyramid or cross-holding structure that delivers control on a small economic stake? And does the legal structure actually give listed shareholders enforceable rights over the operating business? The answers tell you whose interests the firm will serve, and therefore how much of the firm's cash flow a minority investor can expect to receive.

**Formulas:**

```
Economic stake (%)      = Shares owned / Total shares outstanding
Voting stake (%)        = (Shares owned x votes per share)
                          / Total votes outstanding
Control wedge           = Voting stake (%) - Economic stake (%)

Group control (%)       = SUM over all affiliated entities of their stakes
                          (cross-holdings and pyramids)

Effective control test:
  Voting stake > 50%  -> outright control
  Largest voting block, with the rest splintered -> de facto control
```

Symbols: *votes per share* differs by class (Baidu Class B carries 10x Class A). *Affiliated entities* are parents, subsidiaries and sister companies of the same group. *Golden share* = a government-held share carrying veto rights regardless of economic stake.

**Procedure:** Running the analysis on a real company:
1. Pull the holdings screen (Bloomberg HDS, or the proxy's beneficial-ownership table plus 13F/13D filings).
2. List the top holders with shares held and percent outstanding. Sum the top 10 and top 20 to gauge concentration.
3. Classify each large outside holder on three axes: size of holding, active or passive, short or long term. An index fund at 4% is not a monitor. An activist at 4% is.
4. Identify insiders. Compute their economic and voting stakes separately.
5. Map the share classes. Get votes per share for each class and recompute voting stakes. Compute the control wedge.
6. Look for golden shares or government veto rights.
7. Trace group affiliations. Sum the stakes of every entity in the same corporate family to get group control. Look for pyramids — a holding company controlling a holding company controlling the operating firm.
8. Check board nomination rights. Count how many directors the controlling holder nominates, and who chairs.
9. Check the legal structure. Where is the listed entity incorporated? Is it a shell? Does it own the operating assets, or only a contractual interest in them?
10. Draw the control triangle (below) and write one sentence naming who controls the firm and what conflicts that creates.

**Reference data:** *The control triangle.* Control of the firm is contested among three corners, with three outside influences pressing on it.

| Corner | What to record |
|---|---|
| **Outside stockholders** | Size of holding; active or passive; short-term or long-term |
| **Inside stockholders** | % of stock held; voting vs. non-voting shares; control structure |
| **Managers** | Length of tenure; links to insiders |
| Surrounding influences | Government; employees; lenders |

*Four canonical structures, with the case that illustrates each:*

**Case 1 — Splintering of stockholders (Disney, 2003).** No holder is large enough to matter. Largest holder Barclays Global at 4.10%. Top 17 holders sum to about 29.3%.

| Holder | Shares (M) | % outstanding |
|---|---|---|
| Barclays Global | 83.63 | 4.10 |
| Citigroup | 62.86 | 3.08 |
| Fidelity | 56.13 | 2.75 |
| State Street | 54.64 | 2.68 |
| Southeastern Asset | 47.33 | 2.32 |
| State Farm Mutual | 41.94 | 2.05 |
| Vanguard | 34.72 | 1.70 |
| Mellon Bank | 32.69 | 1.60 |
| Putnam | 28.15 | 1.38 |
| Lord Abbett | 24.54 | 1.20 |
| Montag & Caldwell | 24.47 | 1.20 |
| Deutsche Bank | 23.24 | 1.14 |
| Morgan Stanley | 19.66 | 0.96 |
| T. Rowe Price | 19.13 | 0.94 |
| Roy Edward Disney | 17.55 | 0.86 |
| AXA/Alliance Capital | 14.28 | 0.70 |
| JP Morgan Chase | 14.21 | 0.70 |
| **Sub-total** | **~599.16** | **29.34** |

**Case 2 — Voting vs. non-voting shares and golden shares (Vale).** Common (voting) shares 3,172 million; preferred (non-voting) shares 1,933 million. Valespar holds **54% of the common** and controls the vote. The Brazilian government also holds golden (veto) shares.

| Common (voting) holders | % | Preferred (non-voting) holders | % |
|---|---|---|---|
| Valespar | 54 | Non-Brazilian | 59 |
| Non-Brazilian (ADR & Bovespa) | 29 | Brazilian institutional | 18 |
| Brazilian government | 6 | Brazilian retail | 18 |
| Brazilian institutional | 6 | Brazilian government | 4 |
| Brazilian retail | 5 | Valespar | 1 |

Who owns Valespar itself (the pyramid's next layer up):

| Valespar owner | Stake |
|---|---|
| Litel Participações | 49.00% |
| Bradespar S.A. | 21.21% |
| Mitsui & Co. | 18.24% |
| BNDESPAR | 11.51% |
| Eletron S.A. | 0.03% |

Vale had eleven board members. Ten were nominated by Valepar, and the board was chaired by Don Conrado, the CEO of Valepar. A minority economic stake exercised full control.

**Case 3 — Cross and pyramid holdings (Tata Motors, 2013).** Tata group entities together control the company without a direct majority.

| Holder | % outstanding |
|---|---|
| Tata Sons | 26.07 |
| Citibank NA | 16.56 |
| Life Insurance Corp of India | 6.26 |
| Tata Steel | 5.49 |
| Capital Group | 3.63 |
| Tata Industries | 2.54 |
| Vanguard | 1.53 |
| Prudential PLC | 1.26 |
| GIC | 1.13 |
| William Blair | 1.12 |
| JPMorgan Chase | 0.92 |
| Schroder | 0.71 |
| BlackRock | 0.52 |
| Norges Bank | 0.40 |
| T. Rowe Price | 0.37 |
| Tata Investment Corp | 0.37 |
| SBI Life | 0.34 |
| Allianz | 0.30 |
| **Total shown** | **~76.19** |

Tata group total = 26.07 + 5.49 + 2.54 + 0.37 = **34.47%**. That is well under half, yet it delivers control because everything else is splintered.

**Case 4 — Legal rights and corporate structure (Baidu).** Three layers weaken shareholder rights at once.
- *The board:* six directors, one of whom is Robin Li, the founder and CEO.
- *The shares:* Li owns a majority of Class B shares, which carry **ten times** the voting rights of Class A. That gives him effective control on a minority economic stake.
- *The structure:* Baidu is a Chinese company incorporated in the Cayman Islands and listed primarily on NASDAQ. The listed company is a shell, structured to get around Chinese restrictions on foreign investors holding shares in Chinese corporations.
- *The legal system:* Baidu's operating counterpart in China is a Variable Interest Entity (VIE). It is unclear how much legal power shareholders in the shell company have to force changes at the VIE.

*Things change — Disney, January 2009 (price $24.24).* After the Pixar acquisition, Steve Jobs became the largest single holder at 7.46%, far above any institution. A large individual blockholder changes the governance dynamic completely versus the splintered 2003 base.

| Holder | Market value | % outstanding |
|---|---|---|
| Steve Jobs (Form 4) | $3.34B | 7.46 |
| Fidelity | $2.05B | 4.58 |
| State Street | $1.7B | 3.79 |
| Barclays Global | $1.66B | 3.70 |
| Vanguard | $1.38B | 3.08 |
| Southeastern Asset | $1.12B | 2.50 |
| State Farm Mutual | $1.02B | 2.28 |
| Wellington | $939M | 2.09 |
| ClearBridge | $816M | 1.82 |
| JP Morgan Chase | $693M | 1.55 |
| Massachusetts Financial | $682M | 1.52 |
| Bank of New York Mellon | $682M | 1.52 |
| Northern Trust | $610M | 1.36 |
| AXA | $486M | 1.08 |
| BlackRock | $476M | 1.06 |
| Jennison | $429M | 0.96 |
| T. Rowe Price | $352M | 0.78 |
| **Total shown** | | **41.12** |

**Worked example:** Vale, worked end to end. Total shares = 3,172m common + 1,933m preferred = 5,105m. Only the common votes. Valespar holds 54% of 3,172m = 1,713m voting shares, plus 1% of 1,933m = 19m non-voting. Economic stake = (1,713 + 19) / 5,105 = **33.9%**. Voting stake = **54%**. Control wedge = 54% - 33.9% = **+20.1 percentage points**. Valespar itself is 49% owned by Litel, so Litel's look-through economic interest in Vale is roughly 0.49 x 33.9% = **16.6%**, while directing 100% of Vale's board nominations (10 of 11 seats). Add the government's golden share veto. Conclusion: a ~17% look-through economic interest plus a state veto controls Vale outright. A minority investor should not assume Vale's decisions maximize the value of the shares they own.

**Determinism:**
- DETERMINISTIC: economic stake, voting stake, control wedge, group totals, look-through interest through a pyramid, top-N concentration sums — all computable from a holdings table plus a class-voting schedule (holdings, share classes, votes per share -> control percentages).
- JUDGMENT: classifying holders as active or passive, short or long term; deciding whether de facto control exists below 50%; assessing whether a VIE or shell structure leaves shareholders with enforceable rights; deciding what conflicts a given structure creates.

**Pitfalls:**
- Reading only economic stakes. Vale, Baidu and Tata all separate ownership from control.
- Treating a large institutional holder as a monitor. Index and mutual funds are usually passive and vote with management.
- Missing the pyramid. Stopping at "Tata Sons owns 26%" hides the fact that the group controls 34%, and that Tata Sons is itself controlled further up.
- Ignoring the domicile and listing structure. A NASDAQ listing does not guarantee US-style shareholder rights when the listed entity is a Cayman shell over a Chinese VIE.
- Assuming the structure is stable. Disney went from fully splintered in 2003 to a 7.46% individual blockholder in 2009.
- Forgetting golden shares. A government veto does not appear anywhere in a percentage-of-shares table.

**Sources:**
- corporate_finance--lecture_slides--cfpacket1spr20 p.26-31

**Related:** [[manager-stockholder-agency-conflict]], [[corporatism-archetypes]], [[board-independence-assessment]], [[alternative-governance-systems]], [[modified-objective-function]], [[country-risk]], [[voting-share-premium]]
