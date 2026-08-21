# Writing findings that get fixed

A finding is a claim, its evidence, and a fix. Missing any of the three, it becomes an
opinion, and opinions consume loopbacks without changing anything.

Four habits separate the two.

**One defect per finding.** Two defects in one entry means the orchestrator cannot close
half of it, and the stage re-runs twice for one fix.

**Quote the numbers.** The `evidence` field carries the artifact, the field and the two
values that contradict. A reader who disagrees should be able to check you in one step.

**Name the input, not the output.** The fix changes an assumption. It never changes a
computed value.

**Size it where you can.** Re-run the model with the offending charge removed and report
what it is worth per share. A quantified finding gets fixed. An unquantified one gets
argued about.

## The shape

```json
{
  "findings": [
    {
      "id": "F1",
      "severity": "high",
      "target_stage": "intrinsic",
      "claim": "Terminal growth exceeds the riskfree rate in the valuation currency.",
      "evidence": "forecast.json terminal.growth_rate is 0.035. cost-of-capital.json riskfree_rate is 0.0275, both in USD. The constraint no-perpetual-growth-above-riskfree is compiled in classification.json.",
      "suggested_fix": "Lower terminal growth to 2.75% or below and let the terminal reinvestment rate follow from g divided by the terminal return on capital. If 3.5% is genuinely required, the riskfree rate is wrong and probably in the wrong currency."
    }
  ]
}
```

## Worked findings

Four examples across the attack sequence. Each shows the level of specificity the
`evidence` field needs.

### A route violation

```
claim         Growth was built from an earnings growth rate although the base year
              operating income is negative.
evidence      classification.json compiles no-standard-growth-model from branch B1.
              forecast.json sets revenue_growth from a 28% earnings growth rate applied
              to a base EBIT of -140. Percentage growth off a negative base has no
              meaning.
suggested_fix Rebuild the forecast from a revenue path and a target margin anchored on
              mature firms with this business model, and state the peer percentile the
              target margin came from.
severity      high
target_stage  intrinsic
```

### A double charge

```
claim         Failure risk is charged twice.
evidence      dcf-result.json applies failure.probability of 0.20 with proceeds at 50%
              of book. cost-of-capital.json also carries a 250 basis point distress
              adjustment in the cost of equity, recorded as "for going-concern risk".
              Removing the rate adjustment and re-running the analyst's own payload
              raises value per share from $18.40 to $22.10.
suggested_fix Keep the probability weight and remove the rate adjustment. Failure is not
              a marginal diversifiable risk that a discount rate can carry, and the
              probability branch also states the recovery basis explicitly.
severity      high
target_stage  cost-of-capital
```

Note where this one is routed. The defect appears in the DCF, but the fix belongs upstream
in the rate build, and the DCF will be rebuilt anyway.

### Growth that nobody paid for

```
claim         The forecast assumes efficiency growth with no stated stop date.
evidence      dcf-result.json forecast rows grow revenue at 11% a year while
              reinvestment over invested capital supports about 6%. The validator's
              growth_reconciliation check reports a 4.9 point gap in year 3. The
              sales-to-capital ratio of 4.2 in forecast.json sits above the sector
              median of 2.1 in the bundled industry table. intrinsic.md does not
              mention efficiency growth.
suggested_fix Either lower sales-to-capital toward the sector level, or state the
              efficiency-growth argument and the year it ends. The efficiency term is a
              one-off spread across a transition, not a perpetual source.
severity      high
target_stage  intrinsic
```

### An implied-expectations finding against the thesis

```
claim         The verdict rests on an unstated disagreement with the market.
evidence      Solving the analyst's own payload for operating_margin.end against the
              market price of $42.00 returns 22.4%. peer-stats on the sector returns a
              median mature margin of 11.8% with an upper quartile of 14.1%. No firm in
              the peer set has sustained 22%. intrinsic.md does not mention what the
              price requires.
suggested_fix Add the implied margin and its position in the sector distribution to the
              write-up. The thesis is stronger stated this way, and a reader can check
              it.
severity      medium
target_stage  intrinsic
```

## The severity call in practice

Three questions decide it.

Is there an assumption set under which both halves are true at once? If not, it is `high`.
A contradiction is not a matter of taste.

Does the model make a claim nobody wrote down? That is `medium`, and the fix is usually a
sentence rather than a number.

Does it change the verdict? A defect that is real and immaterial is `low`. Say how much it
is worth, and move on.

Resist grading everything high. A challenge file where every row blocks the verdict tells
the orchestrator nothing about what to fix first. It also burns the two-loopback budget on
cosmetics, after which genuine findings get disclosed as unresolved risks rather than
fixed.

## The prose companion

`challenge.md` carries five sections.

1. **Route validated against.** The primary path, the engine branch, the overlays and the
   compiled constraints you tested.
2. **The mechanical run.** The validator command, its error and warning counts, and any
   check that was skipped for a missing artifact.
3. **Findings.** Ranked by severity, each with the argument in prose. The JSON carries the
   contract; this carries the reasoning.
4. **Attacks that found nothing.** Named, so a reader can tell a systematic review from an
   opportunistic one.
5. **Open questions.** What you could not resolve from the artifacts alone, and what
   evidence would resolve it.

Section 4 is the one people skip and the one that gives the document its weight. A review
that lists only failures reads as advocacy.
