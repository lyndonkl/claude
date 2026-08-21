# Ownership, control and the marginal investor

Who owns a company and who controls it are different questions. Both need answers. The
first tells you whose cash flows these are. The second tells you whose interests the firm
will actually serve, and therefore how much of the cash flow a minority investor can
expect to receive.

## The arithmetic

```
Economic stake (%)  = Shares owned / Total shares outstanding
Voting stake (%)    = (Shares owned × votes per share) / Total votes outstanding
Control wedge       = Voting stake − Economic stake

Group control (%)   = sum of stakes held by every affiliated entity
Look-through interest = product of ownership fractions down each layer of a pyramid

Voting stake > 50%                          → outright control
Largest voting block, everything else split → de facto control
```

Votes per share differ by class. A golden share carries a government veto regardless of
economic stake, and it appears nowhere in a percentage-of-shares table.

## Procedure

1. Pull the beneficial-ownership table from the proxy, plus 13F and 13D filings. List the
   top holders with shares and percent outstanding. Sum the top 10 and top 20.
2. Classify every large outside holder on three axes: size, active or passive, short or
   long term.
3. Compute insiders' economic and voting stakes separately.
4. Map the share classes. Get votes per share for each, recompute voting stakes, and
   compute the wedge.
5. Look for golden shares and government veto rights.
6. Trace group affiliations. Sum every entity in the same corporate family. Look for a
   holding company controlling a holding company controlling the operating firm.
7. Count the directors the controlling holder nominates, and check who chairs.
8. Check the legal structure. Where is the listed entity incorporated? Is it a shell? Does
   it own the operating assets, or only a contractual claim on them?
9. Write one sentence naming who controls the firm and what conflicts that creates.

## Four canonical structures

| Structure | What it looks like | What it means for a minority holder |
|---|---|---|
| Splintered holders | No holder above roughly 5 percent; the top 15 to 20 sum to under a third | Nobody can discipline management; agency cost is the main risk |
| Dual class plus golden share | Voting class held by a control vehicle; a state veto on top | Control sits on a minority economic stake; expect politically shaped decisions |
| Pyramid or cross-holding | Group entities each hold a slice; the sum controls | Reported financials earn a confidence discount; ask support versus extraction |
| Shell over an operating entity | Offshore listed company holding a contractual interest | The enforceability of shareholder rights is the open question |

**Worked read — Vale.** Common (voting) shares 3,172 million, preferred (non-voting)
1,933 million. Only the common votes. Valespar holds 54 percent of the common and 1
percent of the preferred. Economic stake is (1,713 + 19) / 5,105 = 33.9 percent. Voting
stake is 54 percent. The control wedge is +20.1 points. Valespar is itself 49 percent
owned by Litel, so Litel's look-through interest in Vale is roughly 16.6 percent. Ten of
eleven board seats were nominated by Valepar, and the chair was Valepar's own CEO. Add the
government's golden share. A 17 percent look-through interest plus a state veto controls
the company outright.

**Worked read — Tata Motors, 2013.** Tata Sons 26.07 percent, Tata Steel 5.49 percent,
Tata Industries 2.54 percent, Tata Investment Corp 0.37 percent. The group total is 34.47
percent, well under half. It delivers control because everything else is splintered. The
best case is that stronger group companies support this one through a downturn. The worst
case is that this one props up weaker members. An outside investor cannot easily tell
which is happening, and that opacity is the structural cost of the model.

**Worked read — Disney, 2003 to 2009.** In 2003 the largest holder was Barclays Global at
4.10 percent, and the top 17 summed to 29.3 percent. Nobody could discipline management.
By 2009, after the Pixar deal, Steve Jobs held 7.46 percent, far above any institution.
Structures are not stable. Re-date the analysis.

## The marginal investor

The marginal investor is the holder most likely to trade next, not the largest holder.
This single call decides whether the capital asset pricing model with a market beta is
legitimate, and therefore decides the whole hurdle-rate stack.

```
Institutional % of shares = institutional shares / shares outstanding
Institutional % of float  = institutional shares / (shares outstanding − closely held)
Insider % of shares       = insider shares / shares outstanding
```

Float percentages above 100 percent are a reporting artifact from overlapping filings and
a lagging float definition. They are not an error.

| Institutional | Insider | Marginal investor | Risk measure |
|---|---|---|---|
| High | Low | Diversified institution | Market beta |
| High | High | Institution, with insider influence | Market beta |
| Low | High (founder or manager) | Ambiguous; insiders only if they trade | Judgment |
| Low | High (wealthy individual) | Fairly diversified individual | Market beta |
| Low | Low | Small holder with restricted diversification | Total risk |

When the marginal investor is not diversified, the analysis carries `require-total-beta`
into the cost of capital, and the beta becomes the market beta divided by the square root
of the comparables' R². Sector correlations near 0.5 mean total betas often run at roughly
twice market betas. When the investor is undiversified and there is no usable price
history, fall back to relative-risk measures such as relative earnings volatility.

Record the insider percentage separately. Debt's disciplinary benefit is largest when
insiders control the firm and diversified institutions are absent. That number is an input
to the capital structure work, not just to this section.

## Pitfalls

- Reading only economic stakes. Dual-class and pyramid structures exist to separate the two.
- Treating a large institutional holder as a monitor. Index and mutual funds usually vote
  with management.
- Stopping at the largest single group entity and missing the group total.
- Ignoring domicile and listing structure. A US listing does not guarantee US-style rights
  when the listed entity is a shell over a foreign operating company.
- Confusing the largest investor with the marginal investor.
- Treating a nominally institutional controlling partnership as a diversified holder.
