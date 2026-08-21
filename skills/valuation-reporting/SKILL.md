---
name: valuation-reporting
description: Assembles a finished company analysis into the deliverable a decision-maker reads — the executive summary, the value bridge, the assumptions that matter, the sensitivity range, and the recommendation with its catalysts and risks. Use when writing up a valuation, DCF, acquisition, IPO, restructuring or corporate finance analysis, when drafting REPORT.md or the verdict, or when deciding what belongs in the report.
---

# Valuation reporting

The analysis is done. Every number sits in an artifact on disk. What remains is the part
the decision-maker actually reads, and it is the part most often written badly.

Two failures dominate. The first is the data dump: forty pages of tables with the answer
buried on page thirty-one. The second is false confidence: one number to the cent, no
range, no disclosure of what the critic found. This skill exists to prevent both.

The report is written by the `investment-reconciler`, which owns `11-verdict/REPORT.md`
and `11-verdict/verdict.json`. It reads every other artifact and writes no other file.
That ownership rule has a direct consequence for style, covered under "Pull, never
recompute" below.

## The templates

One template per analysis mode. Read the one that matches `mandate.json.mode` before
drafting. Each gives the sections in order, what belongs in each, and which artifact
supplies each number.

| Mode | Template | Terminal question |
|---|---|---|
| `valuation` | [resources/template-valuation.md](resources/template-valuation.md) | What is this worth, and is it a buy? |
| `corporate-finance` | [resources/template-corporate-finance.md](resources/template-corporate-finance.md) | Are the investing, financing and payout choices right? |
| `acquisition` | [resources/template-acquisition.md](resources/template-acquisition.md) | What is the most we should pay? |
| `project` | [resources/template-project.md](resources/template-project.md) | Should we make this investment? |
| `ipo` | [resources/template-ipo.md](resources/template-ipo.md) | What is the offer price range? |
| `restructuring` | [resources/template-restructuring.md](resources/template-restructuring.md) | What is it worth run differently? |

Two method files support every template:

- [resources/value-bridge-and-range.md](resources/value-bridge-and-range.md) — laying out
  the bridge, choosing and presenting the range, value against price.
- [resources/disclosure-and-vintage.md](resources/disclosure-and-vintage.md) — the pivotal
  assumption ledger, unresolved findings, data gaps, source vintages.

## Six disciplines, every mode

### 1. Lead with the answer

The first screen carries the recommendation, the number behind it, the range around it,
and the one sentence that says why. Assume the reader stops there. Everything after the
first screen exists to let a sceptic audit the claim, not to build up to it.

A report that opens with company history has buried its own finding.

### 2. Show the bridge

A single value per share tells nobody where the value came from. The bridge does. In an
intrinsic valuation it is the ladder from operating assets to value per share. In a
restructuring or acquisition it is the value stack: status quo, plus control, plus
synergy. Both are laid out in `resources/value-bridge-and-range.md`.

Show the line items with their bases. Most disputes between competent analysts happen in
the bridge, not in the growth forecast, and a bridge on the page is what lets a reader
find the line they disagree with.

### 3. Name the two or three assumptions the answer turns on

Every valuation has dozens of inputs and two or three that decide it. Find them in the
sensitivity block of `dcf-result.json`: they are the inputs whose plausible range moves
value enough to change the recommendation. Name them, give each a value, a source and a
range, and say which way the answer flips.

Everything else goes in an appendix table. Listing forty assumptions with equal weight
tells the reader you have not worked out which ones matter.

### 4. Present a range, not a point

The payoff from a valuation is largest exactly where precision is lowest. A point estimate
to the cent claims a precision the inputs cannot support, and a reader who spots that
distrusts the rest.

Report a base case with a range around it, and label the range with what produced it —
a two-input sensitivity grid, a named scenario grid, or simulation percentiles. Rule out
the cells the narrative cannot support and say why you ruled them out. A grid with
impossible cells left in it is not a range, and neither is a wish list of scenarios
without likelihood labels.

Round to the precision the inputs justify. Value per share to the cent is defensible only
when the share count and the bridge are exact to the cent, which is rare.

### 5. Disclose unresolved critic findings

`G7_challenged` passes when every high-severity finding in `challenge.json` is resolved
**or** explicitly disclosed. The loopback rule caps reruns at two per stage. A finding
that survives the third attempt is disclosed in the report as an unresolved risk.

Disclosure is a named section, not a footnote. Give the finding's `id`, its `claim`, the
stage it targets, what was attempted, and how the value would move if the critic is right.
A report that quietly drops a finding the critic raised is the one failure that destroys
the reader's trust in every other number.

### 6. Record the data vintage

Every external input has a date. The riskfree rate, the equity risk premium, the default
spread table, the country risk premium table, the industry averages, the market price.
Mixing vintages is the most common silent error in this domain, and the report is where it
becomes visible or stays hidden.

Carry one vintage table. Name the `as_of` field of every bundled reference table used, and
the `valuation_date` from `mandate.json`. Note anything more than a year stale and say
what it would change. List the entries from `gaps.json` with the fallback used for each.

## Value against price, without pretending certainty

The gap between value and price is the point of a valuation mandate, and it is the easiest
place to overclaim. Report it in four steps, in this order.

1. **The gap.** Value per share, price per share, the difference, and price as a percent of
   value. Below 50% or above 200% is a prompt to re-examine your own inputs. Say that you
   did, and what you found.
2. **The implied input.** Solve for the growth rate or margin that makes model value equal
   the market price. That number is what the market is assuming. Then ask whether it is
   probable, not merely possible. Some scenario justifies any price.
3. **The closing mechanism.** A gap with no mechanism and no horizon is an opinion, not a
   trade. Name what closes it: an earnings report, a product milestone, an activist, an
   acquirer, an index event, a refinancing. If you cannot name one, say so plainly and let
   the recommendation carry that weight.
4. **The margin of safety.** The gap net of the range. If the conservative end of your
   range still sits above the price, say it — that is a far stronger argument than the base
   case alone. If it does not, the recommendation rests on the base case and the reader
   deserves to know.

Never average a DCF value with a multiple-based price into one number. Report both,
explain the difference, and say which one carries the decision and why. Where the intrinsic
and relative answers disagree, the explanation is the finding.

Say plainly that the value estimate moves too. Intrinsic value changes as information
arrives; today's gap is not tomorrow's.

## Pull, never recompute

Every number in the report comes from the artifact that owns it. The report reports; it
does not calculate. A figure in the executive summary that disagrees with the same figure
in the body is a validation failure, not a rounding difference.

This applies to derived figures as well. If the gap between value and price appears twice,
it is computed once and quoted twice. When a number needs recomputing, the owning stage
reruns and rewrites its artifact; the report then picks up the new value.

Arithmetic that genuinely belongs to the report — a percentage gap, a per-share
conversion, a sum of disclosed line items — runs through the computation skills rather
than in your head. `valuation-consistency-checks` validates the assembled set before the
report ships.

## What the verdict carries

`verdict.json` is the machine-readable half of the same deliverable, and `G8_reconciled`
passes only when it states value against price with a margin of safety. Full schemas live
in `contracts/`. The fields the gate and the report both need:

- `mode`, `company`, `currency`, `valuation_date` — copied from `mandate.json`.
- `recommendation` — the call, in the vocabulary of the mode.
- `value` and `price` — with the unit stated, and the range around the value.
- `margin_of_safety` — the gap net of the range.
- `key_assumptions` — the two or three, each with value, source and range.
- `catalysts` and `risks` — each with a horizon.
- `unresolved_findings` — the `id` and `claim` of every disclosed finding.
- `data_vintage` — the `as_of` of every reference table used.
- `confidence` — high, medium or low, with the reason.

Keep `verdict.json` and `REPORT.md` in agreement figure by figure. They are one artifact
in two formats.

## Writing the prose

State the finding, then the evidence. Not the reverse. A paragraph that walks through the
method before arriving at the conclusion makes the reader do work you should have done.

Give every number its unit and currency on first use in a section. A table of figures with
no currency header is unusable in a multi-currency mandate, and the mandate currency is
binding on every rate and cash flow in the analysis.

Hedge once or not at all. "Roughly 12%" is honest. "Approximately around 12% or so,
subject to considerable uncertainty" is noise, and it reads as an attempt to avoid being
wrong rather than an attempt to be useful.

Attribute judgment calls to the judgment, not to the machinery. Write "we set the terminal
return on capital equal to the cost of capital because no moat survives ten years in this
business", not "the model assumes convergence". The second sentence hides a decision
somebody made.

State your own bias exposure in one line where it exists: who commissioned the work, what
answer they want, whether the market price was seen before the qualitative work was done.

## What sinks a report

- The answer arrives on page thirty, after the methodology.
- A point estimate with no range, or a range with no likelihood labels.
- Forty assumptions listed with equal weight and no statement of which two decide it.
- A high-severity critic finding that appears nowhere.
- A riskfree rate from this year paired with a country risk table from four years ago.
- The summary and the body disagreeing because the summary was recomputed.
- A DCF value and a peer multiple averaged into one number.
- A buy call with no catalyst and no horizon.
- Value per share quoted to four decimals off a share count rounded to millions.
- Control value, synergy value and a strategic premium stacked on one DCF.
- The offer price presented as the value, or an exit multiple presented as intrinsic.

## Where the detail lives

- Report structure per mode: the six template files above.
- Pipeline stages and their outputs: `knowledge/frameworks/intrinsic-valuation-playbook.md` (S15–S18)
  and `knowledge/frameworks/corporate-finance-playbook.md` (S12).
- Gap, expected return and the three investor questions:
  `knowledge/concepts/narrative-numbers/value-vs-price-gap.md`.
- Precision, bias and the small-model rule:
  `knowledge/concepts/narrative-numbers/valuation-misconceptions.md`.
- Range construction: `knowledge/concepts/deliverables-worked-examples/dcf-sensitivity-analysis.md`,
  `knowledge/concepts/narrative-numbers/narrative-scenario-grids.md`,
  `knowledge/concepts/narrative-numbers/monte-carlo-valuation-simulation.md`.
- Reconciling conflicting estimates:
  `knowledge/concepts/deliverables-worked-examples/valuation-triangulation-and-recommendation.md`.
- The one-page scorecard:
  `knowledge/concepts/deliverables-worked-examples/project-executive-summary-scorecard.md`.
