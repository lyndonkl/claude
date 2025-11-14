# Research Claim Map: Advanced Methodologies

## Table of Contents
1. [Triangulation Techniques](#1-triangulation-techniques)
2. [Source Verification Methods](#2-source-verification-methods)
3. [Evidence Synthesis Frameworks](#3-evidence-synthesis-frameworks)
4. [Bias Detection and Mitigation](#4-bias-detection-and-mitigation)
5. [Confidence Calibration Techniques](#5-confidence-calibration-techniques)
6. [Advanced Investigation Patterns](#6-advanced-investigation-patterns)

## 1. Triangulation Techniques

### Multi-Source Verification

**Independent corroboration**:
- **Minimum 3 independent sources** for high-confidence claims
- Sources are independent if: different authors, organizations, funding, data collection methods
- Example: Government report + Academic study + Industry analysis (all using different data)

**Detecting circular citations**:
- Trace back to original source - if A cites B, B cites C, C cites A → circular, invalid
- Check publication dates - later sources should cite earlier, not reverse
- Use citation indexes (Google Scholar, Web of Science) to map citation networks

**Convergent evidence**:
- Different methodologies reaching same conclusion (surveys + experiments + observational)
- Different populations/contexts showing same pattern
- Example: Lab studies + field studies + meta-analyses all finding same effect

### Cross-Checking Strategies

**Fact-checking databases**:
- Snopes, FactCheck.org, PolitiFact for public claims
- Retraction Watch for scientific papers
- OpenSecrets for political funding claims
- SEC EDGAR for financial claims

**Domain-specific verification**:
- Medical: PubMed, Cochrane Reviews, FDA databases
- Technology: CVE databases, vendor security advisories, benchmark repositories
- Business: Crunchbase, SEC filings, earnings transcripts
- Historical: Primary source archives, digitized records

**Temporal consistency**:
- Check if claim was true at time stated (not just currently)
- Verify dates in citations match narrative
- Look for anachronisms (technology/events cited before they existed)

## 2. Source Verification Methods

### CRAAP Test (Currency, Relevance, Authority, Accuracy, Purpose)

**Currency**: When was it published/updated?
- High: Within last year for fast-changing topics, within 5 years for stable domains
- Medium: Dated but still applicable
- Low: Outdated, context has changed significantly

**Relevance**: Does it address your specific claim?
- High: Directly addresses claim with same scope/context
- Medium: Related but different scope (e.g., different population, timeframe)
- Low: Tangentially related, requires extrapolation

**Authority**: Who is the author/publisher?
- High: Recognized expert, peer-reviewed publication, established institution
- Medium: Knowledgeable but not top-tier, some editorial oversight
- Low: Unknown author, self-published, no credentials

**Accuracy**: Can it be verified?
- High: Data/methods shared, replicable, other sources corroborate
- Medium: Some verification possible, mostly consistent with known facts
- Low: Unverifiable claims, contradicts established knowledge

**Purpose**: Why was it created?
- High: Inform/educate, transparent about limitations
- Medium: Persuade but with evidence, some bias acknowledged
- Low: Sell/propagandize, misleading framing, undisclosed conflicts

### Domain Authority Assessment

**Academic sources**:
- Journal impact factor (higher = more rigorous peer review)
- H-index of authors (citation impact)
- Institutional affiliation (R1 research university > teaching-focused college)
- Funding source disclosure (NIH grant > pharmaceutical company funding for drug study)

**News sources**:
- Editorial standards (corrections policy, fact-checking team)
- Awards/recognition (Pulitzer, Peabody, investigative journalism awards)
- Ownership transparency (independent > owned by entity with vested interest)
- Track record (history of accurate reporting vs retractions)

**Technical sources**:
- Benchmark methodology disclosure (reproducible specs, public data)
- Vendor independence (third-party testing > vendor self-reporting)
- Community verification (open-source code, peer reproduction)
- Standards compliance (IEEE, NIST, OWASP standards)

## 3. Evidence Synthesis Frameworks

### GRADE System (Grading of Recommendations Assessment, Development and Evaluation)

**Start with evidence type**:
- Randomized controlled trials (RCTs): Start HIGH quality
- Observational studies: Start LOW quality
- Expert opinion: Start VERY LOW quality

**Downgrade for**:
- Risk of bias (methodology flaws, conflicts of interest)
- Inconsistency (conflicting results across studies)
- Indirectness (different population/intervention than claim)
- Imprecision (small sample, wide confidence intervals)
- Publication bias (only positive results published)

**Upgrade for**:
- Large effect size (strong signal)
- Dose-response gradient (more X → more Y)
- All plausible confounders would reduce effect (conservative estimate)

**Final quality rating**:
- **High**: Very confident true effect is close to estimate
- **Moderate**: Moderately confident, true effect likely close
- **Low**: Limited confidence, true effect may differ substantially
- **Very Low**: Very little confidence, true effect likely very different

### Meta-Analysis Interpretation

**Effect size + confidence intervals**:
- Large effect + narrow CI = high confidence
- Small effect + narrow CI = real but modest effect
- Any effect + wide CI = uncertain
- Example: "10% improvement (95% CI: 5-15%)" vs "10% improvement (95% CI: -5-25%)"

**Heterogeneity (I² statistic)**:
- I² < 25%: Low heterogeneity, studies agree
- I² 25-75%: Moderate heterogeneity, some variation
- I² > 75%: High heterogeneity, studies conflict (be skeptical of pooled estimate)

**Publication bias detection**:
- Funnel plot asymmetry (missing small negative studies)
- File drawer problem (unpublished null results)
- Check trial registries (ClinicalTrials.gov) for unreported studies

## 4. Bias Detection and Mitigation

### Common Cognitive Biases in Claim Evaluation

**Confirmation bias**:
- **Symptom**: Finding only supporting evidence, ignoring contradictions
- **Mitigation**: Actively search for "why this might be wrong", assign someone to argue against
- **Example**: Believing vendor claim because you want product to work

**Availability bias**:
- **Symptom**: Overweighting vivid anecdotes vs dry statistics
- **Mitigation**: Prioritize data over stories, ask "how representative?"
- **Example**: Fearing plane crashes (vivid news) over car crashes (statistically riskier)

**Authority bias**:
- **Symptom**: Accepting claims because source is prestigious (Nobel Prize, Harvard, etc.)
- **Mitigation**: Evaluate evidence quality independently, check if expert in this specific domain
- **Example**: Believing physicist's medical claims (out of domain expertise)

**Anchoring bias**:
- **Symptom**: First number heard becomes reference point
- **Mitigation**: Seek base rates, compare to industry benchmarks, gather range of estimates
- **Example**: Vendor says "saves 50%" → anchor on 50%, skeptical of analyst saying 10%

**Recency bias**:
- **Symptom**: Overweighting latest information, dismissing older evidence
- **Mitigation**: Consider full timeline, check if latest is outlier or trend
- **Example**: One bad quarter → ignoring 5 years of growth

### Source Bias Indicators

**Financial conflicts of interest**:
- Study funded by company whose product is being evaluated
- Author owns stock, serves on board, receives consulting fees
- Disclosure: Look for "Conflicts of Interest" section in papers, FDA disclosures

**Ideological bias**:
- Think tank with known political lean
- Advocacy organization with mission-driven agenda
- Framing: Watch for loaded language, cherry-picked comparisons

**Selection bias in studies**:
- Participants not representative of target population
- Dropout rate differs between groups
- Outcomes measured selectively (dropped endpoints with null results)

**Reporting bias**:
- Positive results published, negative results buried
- Outcomes changed after seeing data (HARKing: Hypothesizing After Results Known)
- Subsetting data until significance found (p-hacking)

## 5. Confidence Calibration Techniques

### Bayesian Updating

**Start with prior probability** (before seeing evidence):
- Base rate: How often is this type of claim true?
- Example: "New product will disrupt market" - base rate ~5% (most fail)

**Update with evidence** (likelihood ratio):
- How much more likely is this evidence if claim is true vs false?
- Strong evidence: Likelihood ratio >10 (evidence 10× more likely if claim true)
- Weak evidence: Likelihood ratio <3

**Calculate posterior probability** (after evidence):
- Use Bayes theorem or intuitive updating
- Example: Prior 5%, strong evidence (LR=10) → Posterior ~35%

### Fermi Estimation for Sanity Checks

**Decompose claim into estimable parts**:
- Claim: "Company has 10,000 paying customers"
- Decompose: Employees × customers per employee, or revenue ÷ price per customer
- Cross-check: Do the numbers add up?

**Example**:
- Claim: Startup has 1M users
- Check: Founded 2 years ago → 1,370 new users/day → 57/hour (24/7) or 171/hour (8hr workday)
- Reality check: Plausible for viral product? Need marketing spend estimate.

### Confidence Intervals and Ranges

**Avoid point estimates** ("70% confident"):
- Use ranges: "60-80% confident" acknowledges uncertainty
- Ask: What would make me 90% confident? What's missing?

**Sensitivity analysis**:
- Best case scenario (all assumptions optimistic) → upper bound confidence
- Worst case scenario (all assumptions pessimistic) → lower bound confidence
- Most likely scenario → central estimate

## 6. Advanced Investigation Patterns

### Investigative Journalism Techniques

**Paper trail following**:
- Follow money: Who benefits financially from this claim being believed?
- Follow timeline: Who said what when? Any story changes over time?
- Follow power: Who has authority/incentive to suppress contradicting evidence?

**Source cultivation**:
- Insider sources (whistleblowers, former employees) for claims companies hide
- Expert sources (academics, consultants) for technical evaluation
- Documentary sources (contracts, emails, internal memos) for ground truth

**Red flags in interviews**:
- Vague answers to specific questions
- Defensiveness or hostility when questioned
- Inconsistencies between different tellings
- Refusal to provide documentation

### Legal Evidence Standards

**Burden of proof levels**:
- **Beyond reasonable doubt** (criminal): 95%+ confidence
- **Clear and convincing** (civil high stakes): 75%+ confidence
- **Preponderance of evidence** (civil standard): 51%+ confidence (more likely than not)

**Hearsay rules**:
- Firsthand testimony > secondhand ("I saw X" > "Someone told me X")
- Exception: Business records, public records (trustworthy hearsay)
- Watch for: Anonymous sources, "people are saying", "experts claim"

**Chain of custody**:
- Document handling: Who collected, stored, analyzed evidence?
- Tampering risk: Could evidence have been altered?
- Authentication: How do we know this document/photo is genuine?

### Competitive Intelligence Validation

**HUMINT (Human Intelligence)**:
- Customer interviews: "Do you use competitor's product? How does it work?"
- Former employees: Glassdoor reviews, LinkedIn networking
- Conference presentations: Technical details revealed publicly

**OSINT (Open Source Intelligence)**:
- Public filings: SEC 10-K, patents, trademarks
- Job postings: What skills are they hiring for? (reveals technology stack, strategic priorities)
- Social media: Employee posts, company announcements
- Web archives: Wayback Machine to see claim history, website changes

**TECHINT (Technical Intelligence)**:
- Reverse engineering: Analyze product directly
- Benchmarking: Test performance claims yourself
- Network analysis: DNS records, API endpoints, infrastructure footprint

### Scientific Reproducibility Assessment

**Replication indicator**:
- Has anyone reproduced the finding? (Strong evidence)
- Did replication attempts fail? (Evidence against)
- Has no one tried to replicate? (Unknown, be cautious)

**Pre-registration check**:
- Was study pre-registered (ClinicalTrials.gov, OSF)? Reduces p-hacking risk
- Do results match pre-registered outcomes? If different, why?

**Data/code availability**:
- Can you access raw data to re-analyze?
- Is code available to reproduce analysis?
- Are materials specified to replicate experiment?

**Robustness checks**:
- Do findings hold with different analysis methods?
- Are results sensitive to outliers or specific assumptions?
- Do subsample analyses show consistent effects?

---

## Workflow Integration

**When to use advanced techniques**:

**Triangulation** → Every claim (minimum requirement)
**CRAAP Test** → When assessing unfamiliar sources
**GRADE System** → Medical/health claims, policy decisions
**Bayesian Updating** → When you have prior knowledge/base rates
**Fermi Estimation** → Quantitative claims that seem implausible
**Investigative Techniques** → High-stakes business decisions, fraud detection
**Legal Standards** → Determining action thresholds (e.g., firing employee, lawsuit)
**Reproducibility Assessment** → Scientific/technical claims

**Start simple, add complexity as needed**:
1. Quick verification: CRAAP test + Google fact-check
2. Moderate investigation: Triangulate 3 sources + basic bias check
3. Deep investigation: Full methodology above + expert consultation
