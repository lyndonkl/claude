# Testing a narrative

Two tests run at step 3. The grading ladder decides which valuation device each claim gets.
The three screens decide whether the assembled set of claims is allowed to exist.

---

## 1. The grading ladder

Sort each claim by how confidently you can attach a probability to it, then route it.

| Grade | Definition | Valuation device | What raises the value | Promotion trigger |
|---|---|---|---|---|
| Possible | the probability cannot be assessed; you do not know what, when, or in what form | option value on top of the DCF | size of the possible market; exclusivity of access | market-potential evidence plus product testing |
| Plausible | low probability, a reasoned argument, no tangible evidence yet | a higher expected growth rate inside the DCF | market size; the firm's competitive advantages | product success plus financial results |
| Probable | expected to happen, with a basis in evidence, though real uncertainty remains | base-year numbers and expected cash flows | evidence of product success and financial results | — |

Three rules govern the routing.

1. **Route each claim exactly once.** A market counted in revenues may not also be counted
   as option value. That is register entry F7 in the double-count register, and it is the
   most common way a narrative pays for the same market twice.
2. **"Possible" is not a synonym for "unlikely".** It means unassessable. A 5% chance you
   can actually estimate is plausible, not possible.
3. **Write the promotion trigger down now.** Step 6 watches those triggers. Without them
   the feedback loop has nothing concrete to look for, and claims stay at their original
   grade long after the evidence arrived, or long after it failed to.

**Uber, June 2014**, drawn as three nested circles. The urban taxi market was **probable**,
so it set total market size, revenues and earnings — a $100 billion market growing 6% a
year, at a 10% share. The suburban car-service and rental market was **plausible**, so it
entered as a higher growth rate. The car-ownership market, where people give up cars
entirely, was only **possible**, so it became option value of $2–3 billion on top of a $5.9
billion DCF.

---

## 2. The impossible screens — never allow

Each is a testable inequality on the model's own outputs plus at most one external number.

| Check | Test | External input |
|---|---|---|
| Bigger than the economy | terminal `g` ≤ riskfree rate in the valuation currency | riskfree rate |
| Bigger than the market | year-N implied revenues / total market size ≤ 100% | market-size estimate |
| Margin above 100% | maximum operating margin over the forecast < 100% | — |
| Depreciation without cap ex | terminal depreciation ≤ terminal cap ex | — |
| Terminal denominator | terminal cost of capital > terminal growth, strictly | — |
| Terminal reinvestment | terminal reinvestment rate = `g / ROC` exactly | — |

The growth cap follows from arithmetic, not convention. The riskfree rate is expected
inflation plus expected real growth in that economy, so nothing can compound above it
forever. The cap may be negative. With a negative euro riskfree rate, Heineken's stable
growth was set at −0.5%, which correctly forces a negative reinvestment rate as the firm
disinvests.

`valuation-consistency-checks` runs all six mechanically. Run them by hand at step 3 too,
before the model exists, because catching an impossible claim in prose costs nothing.

---

## 3. The implausible screens — extraordinary justification required

- **Growth without reinvestment.** Perpetual growth with zero net reinvestment. Zero net
  reinvestment supports approximately zero real growth, and nothing more.
- **Profits without competition.** Rising margins and rising share with no competitive
  response anywhere in the model.
- **Returns without risk.** High returns assumed in a business nobody describes as risky.

These are not arithmetic failures. They are claims about economics, and each needs a named
mechanism — a patent, a regulated monopoly, a network effect with real switching costs.

---

## 4. The improbable screens — the triangle

The dangerous class. Every assumption looks fine alone, and the combination contradicts how
business works. The three corners are **growth**, **risk** and **reinvestment**. You may
have a good outcome on one corner. You may sometimes have two, with a stated reason. Never
all three for free.

The improbable pairings:

- High growth with low risk.
- High growth with low reinvestment.
- Low risk with high reinvestment.

Three computed screens catch them.

**Marginal ROIC over the forecast.**

```
marginal ROIC = change in EBIT(1-t) across the forecast
                / change in invested capital across the forecast
```

If it exceeds what the best firms in the business earn, either reinvestment is too low or
margins are too high. Tesla's chosen sales-to-capital of 4.00, against an auto industry
median of 1.37, produced a marginal ROIC of 51.66%. That is not automatically wrong. It is
automatically a claim, and it has to appear in the prose.

**Terminal excess return.** `terminal ROC − terminal cost of capital`. Anything above zero
claims a moat that survives in perpetuity. State the moat or set them equal. The honest
default is equality, because competition eventually arrives.

**Absolute revenues in year N.** Percentage growth is deceptive. Translate the growth path
into dollars and ask a specific question: who loses that revenue? Then divide by your own
total-market estimate.

One empirical anchor for the fade. Newly public firms beat their industry's revenue growth
for about five years, and the median excess falls to roughly zero by years five to six. A
model that holds the excess for a decade needs a reason. Note the asymmetry: fade growth
faster than you fade excess returns, because median large-cap ROIC has been sustainable in
an 8–12% band over decades while real revenue growth decays reliably toward GDP growth.

---

## 5. The sector aggregation test

Run this whenever the company is one of many chasing one market. It is the only screen that
cannot be run from inside a single valuation.

1. **Define the market precisely.** Online advertising, food delivery, ride hailing. A vague
   market definition defeats the test.
2. **List every competitor**, listed and private, domestic and foreign. Excluding the
   foreign names understates the total badly.
3. **Impute breakeven revenues** for each in a common future year — the revenue level needed
   to justify today's enterprise value, at plausible margins, reinvestment and cost of
   capital. Use `dcf-valuation-engine`'s `implied` subcommand.
4. **Multiply by the share of that company's revenue that comes from this market.**
5. **Sum across all companies.**
6. **Compare with an independent forecast** of total market size in that year, ideally one
   you did not construct.

```
sum of implied market shares <= 100%
```

If the sum exceeds the market, the finding is about the sector, not the name. Reduce
exposure across it rather than picking the one you like. Do not use each company's own
bullish margin assumption when imputing its breakeven revenue — that understates the
revenue required and hides the delusion.

---

## 6. The runaway-story score

Score three ingredients before trusting a story you find appealing.

```
runaway story = charismatic narrator
              + disliked status quo being disrupted
              + claimed societal benefit
```

Two or three yeses means write down the questions you have not asked, and then ask them.
Test the core claim against first principles — "is this even possible?" — rather than
against execution risk. Count board members with real domain knowledge of the central
technical claim, not the average quality of their résumés.

The meltdown equation names when to mark the story down before the market does.

```
meltdown = untrustworthy storyteller
         + story at war with its own numbers
         + bad business model that management denies
```

Two of three present means treating the narrative as at risk of a **break**, not a shift.

The checklist only bites on stories you want to be true. Applying it exclusively to
companies you already dislike wastes it.

---

## 7. What to do when a screen fails

Fix the offending input, not the output. Then re-run from the stage that owns it. A margin
failure re-runs the forecast onward. A terminal-growth failure re-runs the terminal block.
Nudging the answer to clear a screen leaves the contradiction in the story and moves it
somewhere nobody is looking.

Cap re-runs at two per stage. On the third, disclose the finding in the report as an
unresolved risk rather than looping forever.
