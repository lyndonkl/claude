---
name: genomics-viz
description: Builds interactive D3 visualizations of genetics and genomics concepts for the vault's docs/ GitHub Pages site — each one a teaching object with a takeaway-stating title, an annotation layer, and a guided reading order. Specializes d3-visualization, visual-storytelling-design, and cognitive-design for the crop-genetics / genomic-selection domain, supplying a concept-to-visualization catalog, preattentive encoding guidance, colorblind-safe palettes, accessibility requirements, and a fixed docs/ file layout. Delegates design review to the cognitive-design-architect agent and runs design-evaluation-audit and cognitive-fallacies-guard before publish. Use when turning an evergreen claim into an interactive figure, building or revising a docs/ visualization, or planning the site's viz layout. Trigger keywords: D3 viz, interactive figure, GitHub Pages chart, Hardy-Weinberg, Manhattan plot, allele drift, LD decay, breeder's equation, genomic prediction accuracy, reaction norm, kinship heatmap.
---

# Genomics visualization

A visualization in this vault is a *teaching object*, not a decoration on a post. It exists to make one genetics claim — usually a single evergreen note — *feel* true to a reader who has the algebra but not yet the intuition. The bar is high: an interactive figure earns its place only when motion or interactivity does work that a static plot cannot (watching allele frequency drift to fixation across replicate populations teaches drift in a way a single trajectory never will).

This skill is the domain specialization layer. The mechanics live elsewhere and are assumed: d3-visualization for scales, shapes, layouts, transitions, and interaction (zoom/pan/brush); visual-storytelling-design for narrative structure and the annotation layer; cognitive-design for *why* an encoding works (preattentive processing, encoding hierarchy, working-memory limits). Use those three for the how; use this for the what, the genomics-specific encodings, and the publish path into `docs/`.

Every figure is built around the publishing claim, so begin from the evergreen note it serves, and let its declarative title become the figure's takeaway title.

## 1. Concept → visualization catalog

Pick the form from the concept. Each row names the encoding spine and the one interaction that earns the "interactive" label.

| Concept (evergreen claim) | Chart form | Encoding spine | The interaction that teaches |
|---|---|---|---|
| Hardy–Weinberg equilibrium | parabola of genotype freqs vs allele freq p | x = p, y = freq of AA/Aa/aa as curves | drag p; watch the three curves and the Aa maximum at p=0.5 |
| Allele-frequency drift | small-multiples of replicate trajectories | x = generation, y = p, one line per population | set N and replicates; press run; watch fixation/loss spread |
| LD decay vs distance | scatter + fitted decay curve | x = distance (kb/cM), y = r² | slide recombination rate / N_e; the curve's half-life moves |
| Recombination | chromosome ribbon with crossovers | position along homologs, crossover marks | step meioses; watch haplotype blocks reshuffle |
| Additive vs dominance variance | stacked decomposition of genotypic values | genotype on x, value on y, V_A vs V_D bands | drag the heterozygote value; V_D appears as the curvature |
| Breeder's equation / response | selection on a phenotype distribution | trait density, truncation point, shifted mean | drag the selection threshold; R = h²·S animates next gen |
| GxE reaction norms | lines across environments | x = environment index, y = genotype mean | toggle genotypes; crossing norms = the interaction |
| Genomic-prediction accuracy vs training-set size | learning curve | x = N_train (log), y = prediction accuracy r | slide heritability and marker density; curve saturates |
| Population-structure PCA | scatter of PC1×PC2 | x = PC1, y = PC2, color = subpopulation | brush a cluster; lasso to inspect membership |
| Manhattan plot | scatter of −log10(p) along the genome | x = genomic position, y = −log10(p), color = chr | hover a peak; zoom a region; significance line draggable |
| Kinship / G-matrix heatmap | symmetric matrix heatmap | row × col = individuals, color = relatedness | reorder by cluster; hover a cell for the pair's coefficient |

Hold one claim per figure (the atomicity rule of `conventions.md` mirrored in pixels). A figure trying to show both drift *and* selection is two figures.

## 2. Encoding guidance

Encode the load-bearing variable in the channel the eye reads first. The cognitive-design encoding hierarchy for quantitative data, most to least accurate: **position → length → angle/slope → area → color hue/saturation**. Spend the top of the hierarchy on the variable the claim is about.

- **Preattentive attributes** (color, motion, orientation, size) make one thing pop *before* the reader attends. Use exactly one to mark the focus — a single red point in a gray Manhattan field, the one fixated population among the drifting gray ensemble. More than one preattentive pop and nothing pops.
- **The Manhattan-plot trap:** rainbow-coloring 20 chromosomes spends hue on a *labeling* variable (which chromosome) while the claim is about *height* (significance). Use two alternating muted grays for chromosomes; reserve a single saturated accent for hits above the line. Hue carries the categorical label only.
- **Heatmaps (kinship/G-matrix):** relatedness is sequential and one-directional, so use a single-hue sequential ramp (e.g. viridis), never a rainbow. A diverging ramp is only for data with a meaningful midpoint (signed values around zero).
- **Colorblind-safe by default:** ~8% of male readers have red–green deficiency. Use viridis/cividis for sequential, Okabe–Ito or ColorBrewer "Set2"/"Dark2" for categorical. Never encode a distinction by red-vs-green alone — pair color with shape, position, or a direct label. Verify the final palette against a deuteranopia simulation.
- **Direct-label over legend** wherever lines or clusters can carry their name at their end (reaction norms, learning curves). A legend forces a working-memory round-trip; a label at the line end does not.

## 3. The annotation layer (visual-storytelling-design)

A bare chart asks the reader to find the point. An annotated chart *makes* it. Build the annotation layer on top, never inside, the data layer.

1. **Title states the takeaway, not the variables.** "Heterozygosity is maximized at p = 0.5" beats "Genotype frequencies vs allele frequency." The title is the evergreen claim, lightly shortened. This is the single most important element.
2. **Annotate the focus points.** A short callout on the meaningful feature: the Aa peak, the significance line, the point where the learning curve flattens. Two or three callouts maximum; an annotation on everything annotates nothing.
3. **Guide the reading order.** Number the entry points or stage them on interaction/scroll so the eye moves takeaway → mechanism → detail. For a stepped or scrollytelling figure, reveal one idea per step.
4. **Honest framing.** Start counts and rates at a zero baseline where truncation would mislead; label log axes as log; show uncertainty (CI band on the LD decay fit, replicate spread on drift) rather than a single clean line that implies more certainty than the data holds.

## 4. Accessibility

Non-negotiable, because this publishes to a public GitHub Pages site.

- Every figure carries a text `<figure><figcaption>` describing the takeaway, and an SVG `<title>`/`<desc>` so screen readers reach the claim.
- Color is never the sole carrier of meaning (see §2).
- Interactive controls are keyboard-reachable and labeled (`aria-label`); hover-only information also appears on focus.
- Body text and labels meet WCAG AA contrast; minimum on-screen label size ~12px.
- Provide a static fallback (the figure's default state renders meaningfully with JS disabled, or ships a PNG alongside).

## 5. Build and review loop

1. **Frame from the claim.** Open the evergreen note; write the takeaway title; pick the catalog row; name the one interaction that teaches.
2. **Draft the data + scales** using d3-visualization. Simulate the genetics with a small, transparent, seeded model (e.g. binomial sampling per generation for drift) so the figure is reproducible and the data file is inspectable.
3. **Apply encodings** (§2) and the **annotation layer** (§4 of visual-storytelling-design, summarized in §3 here).
4. **Self-check with cognitive-design** for load and hierarchy before asking for review.
5. **Delegate design review to the cognitive-design-architect agent.** Hand it the rendered figure and the claim. It runs `design-evaluation-audit` (clarity, hierarchy, encoding correctness, accessibility) and `cognitive-fallacies-guard` (does the framing invite a misread — truncated axis implying a big effect, correlation in the Manhattan plot read as cause, a smoothed line hiding noise). Treat its output as advisory in the spirit of `conventions.md` §10: it proposes, the author approves.
6. **Fix and re-audit** until clean, then propose the publish.

## 6. docs/ file layout

The site is plain static HTML/JS/CSS (`conventions.md` §2). One self-contained directory per figure so a post can embed it via iframe and it also stands alone.

```
docs/
  index.html                      # gallery: cards linking each viz, grouped by phase
  assets/
    css/site.css
    js/d3.v7.min.js               # pinned D3; vizzes share one copy
    js/palettes.js                # viridis + Okabe–Ito, the house palettes
  viz/
    hardy-weinberg/
      index.html                  # the standalone figure page
      hardy-weinberg.js           # the D3 build
      data.json                   # seeded/simulated data (inspectable, reproducible)
      README.md                   # claim, evergreen slug it serves, how to regenerate data
    allele-drift/
      index.html
      allele-drift.js
      ...
```

Conventions for the layout:

- Directory slug = the concept slug, matching a catalog row (`hardy-weinberg`, `ld-decay`, `manhattan-plot`).
- The figure's `README.md` records the **evergreen slug** it visualizes (provenance, mirroring the post `viz:` and `based-on:` fields), the takeaway title, the data source or simulation seed, and the regeneration command.
- The owning `post` note links the figure via its `viz:` frontmatter field (`docs/viz/hardy-weinberg/`).
- Keep each `*.js` build self-contained and dependency-light; share only D3 and `palettes.js` from `assets/`.

## Output contract

This skill produces or revises files under `docs/`. Like every agent in the system it **proposes; the author approves** (`conventions.md` §10) — it does not commit or publish on its own. A completed figure is: one claim, a takeaway title, a teaching interaction, correct encodings, a clean annotation layer, accessibility met, and a passed cognitive-design-architect review. If interactivity adds nothing the claim needs, ship a static figure and say so.
