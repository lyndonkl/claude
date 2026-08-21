# Corporate governance analysis deliverable

**Core idea:** Part I of the corporate finance project asks how far managers act in shareholders' interests. It is answered with a peer-benchmarked board and executive table, a third-party governance score, a read of the company's own policies, and a social-responsibility assessment. The output is a verdict per company on shareholder power, usually compressed to a single "Power" score. Governance matters because every later recommendation assumes management will act on it. A board with staggered terms, takeover defenses and no majority-vote standard can ignore an optimal-debt-ratio recommendation indefinitely.

**Formulas:**
- Non-employee % = Non-employee directors / Total board members.
- Owning % = Board members owning shares / Total board members.
- Other boards % = Directors sitting on other companies' boards / Total board members.
- No governance score is computed from a formula; ISS QuickScore is a vendor input on a 1-10 scale (1 = best / lowest risk, 10 = worst).

**Procedure:**
1. **State the four project questions.** Is there separation between management and ownership, and how responsive is management to stockholders? What other conflicts of interest exist? How does the firm interact with financial markets and how do markets get information on it? How does it view its social obligations and manage its image?
2. **Build the board/executive table against peer averages.** Rows: number of executives, average reported compensation, executive average age, executive average tenure, number of board members, non-employee directors and %, members owning shares and %, shares held by the board, average meeting attendance, directors on peer boards and %, directors on other companies' boards and %, board average age, board average tenure. Report the peer average alongside each value.
3. **Pull a third-party governance score.** ISS Governance QuickScore (via Yahoo Finance) with its sub-scores: overall, audit, board, shareholder rights, compensation.
4. **Read the underlying policies the score flags.** Do not take the score at face value in either direction. Look for mitigants the score misses and for weaknesses the score understates.
5. **Apply the red-flag checklist.** Score shareholder power down for: a staggered board; no majority-vote requirement in uncontested director elections (a single "for" vote can reappoint a director); takeover defenses; weak policies on terminating non-performing executives; "independence" defined only by NYSE rules, which are not stringent.
6. **Check compensation structure for risk incentives.** A pay package with an extremely high performance-linked share amid rapid growth rewards growth and can encourage excessive risk-taking.
7. **Look for evidence of responsiveness.** A management change made in response to shareholder dissatisfaction is a positive signal of respect for shareholders.
8. **Assess social responsibility separately.** Distinguish CSR that is core to the brand and business model from CSR that is peripheral marketing. Note where declining a CSR position (e.g. not advocating non-GMO) arguably serves shareholders by keeping costs down.
9. **Issue a verdict** — strongest and weakest governance in the peer set, and a numeric Power score for the summary scorecard.

**Reference data:** Spring 2015 board and executive comparison; company value first, peer average in parentheses.

| Metric | SBUX | MCD | CMG | TSN |
|---|---|---|---|---|
| Number of executives | 7 (10) | 12 (9) | 5 (10) | 15 (11) |
| Avg reported compensation ($m) | 8.4 (4.2) | 2.5 (4.8) | 18.2 (3.3) | 7.7 (4.4) |
| Executive avg age | 56.7 (53) | N/A (53) | 53 (N/A) | N/A (N/A) |
| Executive avg tenure (yrs) | 12.6 (9.3) | 17.8 (9.4) | 9.7 (9.8) | 12 (12.3) |
| Number of board members | 12 (10) | 14 (10) | 9 (10) | 8 (12) |
| Non-employee directors | 10 (8) | 13 (8) | 7 (8) | 6 (10) |
| Non-employee % | 83.3% (80%) | 92.9% (80%) | 77.8% (80%) | 75% (83.3%) |
| Members owning shares | 12 (9) | 11 (9) | 7 (9) | 8 (11) |
| Owning % | 100% (90%) | 78.6% (90%) | 77.8% (90%) | 100% (91.7%) |
| Shares held | 2.6% (1.7%) | 0% (3.3%) | 0.8% (2.5%) | 0.6% (1.6%) |
| Avg meeting attendance | 75% (75%) | 75% (75%) | 75% (75%) | 97% (79.9%) |
| On boards of peers | 0 (0.2) | 0 (0) | 0 (0) | 0 (0.2) |
| On peer boards % | 0% (2%) | 0% (0%) | 0% (0%) | 0% (1.7%) |
| On boards of other companies | 12 (8) | 12 (7) | 4 (8) | 4 (9) |
| Other boards % | 100% (78%) | 85.7% (73%) | 44.4% (77%) | 50% (77.5%) |
| Board avg age | 67.3 (58.6) | 63.1 (60.6) | N/A (61.3) | N/A (66.5) |
| Board avg tenure (yrs) | 12 (8.1) | 12.2 (8.1) | 11.4 (8.2) | 12.5 (8.6) |

ISS Governance QuickScore, 2015 (1 = best, 10 = worst):

| Sub-score | SBUX | MCD | CMG | TSN |
|---|---|---|---|---|
| Overall | 1 | 5 | 10 | 8 |
| Audit | 1 | 1 | 2 | 2 |
| Board | 6 | 9 | 4 | 10 |
| Shareholder rights | 1 | 6 | 10 | 5 |
| Compensation | 1 | 4 | 10 | 9 |

Resulting "Power" scores used in the summary: SBUX 2, MCD 2, CMG 0, TSN 1.

Useful published data sets for this part: CEO pay by firm (Forbes); Jensen's alpha by industry.

**Worked example:** Chipotle, Spring 2015. Its ISS overall score is 10 — the worst possible. The team confirmed it rather than softening it. Chipotle has an entrenched board, no majority-vote requirement in uncontested elections, staggered board terms and takeover defenses. Executive pay averages $18.2m against a $3.3m peer average, because the performance-linked portion is extremely high amid rapid growth — a structure that can encourage excessive risk-taking. Verdict: very low shareholder rights, which would matter in a period of sustained underperformance. Power score 0, the lowest in the group. Tyson runs the other way: its ISS overall score of 8 is judged too harsh, because Chairman John Tyson (the founder's grandson) holds a significant stake through the Tyson Limited Partnership, managers must hold up to 3x salary in stock within five years, and CEO Donnie Smith has been with the company since 1980. The stock rule is escapable — failing it merely converts 25% of the cash bonus into stock — so the mitigant is partial.

**Determinism:** DETERMINISTIC — every count and ratio in the board table (director counts, non-employee %, owning %, tenure and age averages, other-board counts) is computable from proxy filings; the ISS QuickScore is a lookup, not a computation; the red-flag checklist is a set of boolean tests against charter and bylaw provisions. JUDGMENT — weighing mitigants against the score, deciding whether a pay structure is dangerous or merely generous, distinguishing core from peripheral CSR, and compressing everything into a single Power score. The judgment needs: the proxy statement, the charter/bylaws, the ISS policy flags, the recent history of management changes and shareholder actions, and the peer set's own practices.

**Pitfalls:**
- Taking the vendor score as the answer. Both directions fail — the 2015 team overrode a bad Tyson score and confirmed a bad Chipotle score, after reading the policies in each case.
- Treating "independent director" as meaningful when independence is defined only by NYSE rules, which are not stringent.
- Missing over-boarding. At Starbucks and McDonald's most directors serve on other boards, sometimes several, which may dilute commitment to any one firm.
- Reporting director share ownership as a percentage of the board without the size of the stake. 100% of directors owning shares means little if the board holds 0.6% of the company.
- Confusing brand-integral sustainability with CSR gloss when judging social obligations.

**Sources:**
- corporate_finance--project--cfproj p.4
- corporate_finance--project--food2015 p.3-6

**Related:** [[corporate-finance-project-blueprint]], [[stockholder-analysis-marginal-investor]], [[project-executive-summary-scorecard]], [[value-of-control-and-synergy]]
