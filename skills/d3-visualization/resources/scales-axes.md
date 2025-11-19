# Scales & Axes

## Why Scales Matter

**The Problem**: Data values (0-1000, dates, categories) don't directly map to visual properties (pixels 0-500, colors, positions). Hardcoding transformations (`x = value * 0.5`) breaks when data changes.

**D3's Solution**: Scale functions encapsulate domain-to-range mapping. Change data → update domain → visualization adapts automatically.

**Key Principle**: "Separate data space from visual space." Scales are the bridge.

---

## Scale Fundamentals

### Domain and Range

```javascript
const scale = d3.scaleLinear()
  .domain([0, 100])      // Data min/max (input)
  .range([0, 500]);      // Visual min/max (output)

scale(0);    // → 0px
scale(50);   // → 250px
scale(100);  // → 500px
```

**Domain**: Input data extent
**Range**: Output visual extent
**Scale**: Function mapping domain → range

---

## Scale Types

### Continuous → Continuous

#### scaleLinear

**Use**: Quantitative data, proportional relationships

```javascript
const xScale = d3.scaleLinear()
  .domain([0, d3.max(data, d => d.value)])
  .range([0, width]);
```

**Math**: Linear interpolation `y = mx + b`

---

#### scaleSqrt

**Use**: Sizing circles by area (not radius)

```javascript
const radiusScale = d3.scaleSqrt()
  .domain([0, 1000000])  // Population
  .range([0, 50]);       // Max radius

// Circle area ∝ population (perceptually accurate)
```

**Why**: `Area = πr²`, so `r = √(Area)`. Sqrt scale makes area proportional to data.

---

#### scalePow

**Use**: Custom exponents

```javascript
const scale = d3.scalePow()
  .exponent(2)           // Quadratic
  .domain([0, 100])
  .range([0, 500]);
```

---

#### scaleLog

**Use**: Exponential data (orders of magnitude)

```javascript
const scale = d3.scaleLog()
  .domain([1, 1000])     // Don't include 0!
  .range([0, 500]);

scale(1);    // → 0
scale(10);   // → 167
scale(100);  // → 333
scale(1000); // → 500
```

**Note**: Log undefined at 0. Domain must be positive.

---

#### scaleTime

**Use**: Temporal data

```javascript
const xScale = d3.scaleTime()
  .domain([new Date(2020, 0, 1), new Date(2020, 11, 31)])
  .range([0, width]);
```

**Works with**: Date objects, timestamps

---

#### scaleSequential

**Use**: Continuous data → color gradients

```javascript
const colorScale = d3.scaleSequential(d3.interpolateBlues)
  .domain([0, 100]);

colorScale(0);    // → light blue
colorScale(50);   // → medium blue
colorScale(100);  // → dark blue
```

**Interpolators**: `interpolateBlues`, `interpolateReds`, `interpolateViridis`, `interpolateRainbow` (avoid rainbow!)

---

### Continuous → Discrete

#### scaleQuantize

**Use**: Divide continuous domain into discrete bins

```javascript
const colorScale = d3.scaleQuantize()
  .domain([0, 100])
  .range(['green', 'yellow', 'orange', 'red']);

colorScale(20);   // → 'green' (0-25)
colorScale(40);   // → 'yellow' (25-50)
colorScale(75);   // → 'orange' (50-75)
colorScale(95);   // → 'red' (75-100)
```

**Equal bins**: Domain divided evenly by range length.

---

#### scaleQuantile

**Use**: Divide data into quantiles (equal-sized groups)

```javascript
const colorScale = d3.scaleQuantile()
  .domain(data.map(d => d.value))  // Actual data values
  .range(['green', 'yellow', 'orange', 'red']);

// Quartiles: 25% of data in each color
```

**Difference from quantize**: Bins have equal data counts, not equal domain width.

---

#### scaleThreshold

**Use**: Explicit breakpoints

```javascript
const colorScale = d3.scaleThreshold()
  .domain([40, 60, 80])          // Split points
  .range(['green', 'yellow', 'orange', 'red']);

colorScale(30);   // → 'green' (<40)
colorScale(50);   // → 'yellow' (40-60)
colorScale(70);   // → 'orange' (60-80)
colorScale(90);   // → 'red' (≥80)
```

**Use for**: Letter grades, risk levels, custom categories.

---

### Discrete → Discrete

#### scaleOrdinal

**Use**: Map categories to categories (often colors)

```javascript
const colorScale = d3.scaleOrdinal()
  .domain(['A', 'B', 'C'])
  .range(['red', 'green', 'blue']);

colorScale('A');  // → 'red'
colorScale('B');  // → 'green'
```

**Built-in schemes**: `d3.schemeCategory10`, `d3.schemeTableau10`

```javascript
const colorScale = d3.scaleOrdinal(d3.schemeCategory10);
```

---

#### scaleBand

**Use**: Position categorical bars

```javascript
const xScale = d3.scaleBand()
  .domain(['A', 'B', 'C', 'D'])
  .range([0, 500])
  .padding(0.1);          // 10% spacing

xScale('A');              // → 0
xScale('B');              // → 125
xScale.bandwidth();       // → 112.5 (width of each band)
```

**Key method**: `.bandwidth()` returns width for bars/columns.

---

#### scalePoint

**Use**: Position categorical points (scatter, line chart categories)

```javascript
const xScale = d3.scalePoint()
  .domain(['A', 'B', 'C', 'D'])
  .range([0, 500])
  .padding(0.5);

xScale('A');              // → 50 (centered in first position)
xScale('B');              // → 200
```

**Difference from band**: Points (no width), bands (width for bars).

---

## Scale Selection Guide

**Quantitative linear**: scaleLinear | **Exponential**: scaleLog | **Circle sizing**: scaleSqrt
**Temporal**: scaleTime | **Categorical bars**: scaleBand | **Categorical points**: scalePoint
**Categorical colors**: scaleOrdinal | **Bins (equal domain)**: scaleQuantize | **Bins (equal data)**: scaleQuantile
**Custom breakpoints**: scaleThreshold | **Color gradient**: scaleSequential

---

## Scale Methods

### Domain from Data

```javascript
// Extent (min, max)
const xScale = scaleLinear()
  .domain(d3.extent(data, d => d.x))  // [min, max]
  .range([0, width]);

// Max only (0 to max)
const yScale = scaleLinear()
  .domain([0, d3.max(data, d => d.y)])
  .range([height, 0]);

// Custom
const yScale = scaleLinear()
  .domain([-100, 100])  // Symmetric around 0
  .range([height, 0]);
```

---

### Inversion

```javascript
const xScale = scaleLinear()
  .domain([0, 100])
  .range([0, 500]);

xScale(50);           // → 250 (data → visual)
xScale.invert(250);   // → 50 (visual → data)
```

**Use**: Convert mouse position to data value.

---

### Clamping

```javascript
const scale = scaleLinear()
  .domain([0, 100])
  .range([0, 500])
  .clamp(true);

scale(-10);   // → 0 (clamped to range min)
scale(150);   // → 500 (clamped to range max)
```

**Without clamp**: `scale(150)` → 750 (extrapolates beyond range).

---

### Nice Domains

```javascript
const yScale = scaleLinear()
  .domain([0.201, 0.967])
  .range([height, 0])
  .nice();

yScale.domain();  // → [0.2, 1.0] (rounded)
```

**Use**: Clean axis labels (0.2, 0.4, 0.6 instead of 0.201, 0.401...).

---

## Axes

### Creating Axes

```javascript
// Scales first
const xScale = scaleBand().domain(categories).range([0, width]);
const yScale = scaleLinear().domain([0, max]).range([height, 0]);

// Axis generators
const xAxis = d3.axisBottom(xScale);
const yAxis = d3.axisLeft(yScale);

// Render axes
svg.append('g')
  .attr('transform', `translate(0, ${height})`)  // Position at bottom
  .call(xAxis);

svg.append('g')
  .call(yAxis);
```

**Axis orientations**:
- `axisBottom`: Ticks below, labels below
- `axisTop`: Ticks above, labels above
- `axisLeft`: Ticks left, labels left
- `axisRight`: Ticks right, labels right

---

### Customizing Ticks

```javascript
// Number of ticks (approximate)
yAxis.ticks(5);  // D3 chooses ~5 "nice" values

// Explicit tick values
xAxis.tickValues([0, 25, 50, 75, 100]);

// Tick format
yAxis.tickFormat(d => d + '%');        // Add percent sign
yAxis.tickFormat(d3.format('.2f'));    // 2 decimal places
yAxis.tickFormat(d3.timeFormat('%b')); // Month abbreviations
```

---

### Tick Styling

```javascript
yAxis.tickSize(10).tickPadding(5);  // Length and spacing
```

---


### Updating Axes

```javascript
function update(newData) {
  // Update scale domain
  yScale.domain([0, d3.max(newData, d => d.value)]);

  // Update axis with transition
  svg.select('.y-axis')
    .transition()
    .duration(500)
    .call(d3.axisLeft(yScale));
}
```

---

## Color Scales

### Categorical Colors

```javascript
const color = d3.scaleOrdinal(d3.schemeCategory10);  // Built-in scheme
const color = d3.scaleOrdinal().domain(['low', 'medium', 'high']).range(['green', 'yellow', 'red']);  // Custom
```

---

### Sequential & Diverging Colors

```javascript
// Sequential
const color = d3.scaleSequential(d3.interpolateBlues).domain([0, 100]);
// Interpolators: Blues, Reds, Greens, Viridis, Plasma, Inferno (avoid Rainbow!)

// Diverging
const color = d3.scaleDiverging(d3.interpolateRdYlGn).domain([-100, 0, 100]);
```

---

## Common Patterns

```javascript
// Responsive: update range on resize
const xScale = scaleLinear().domain([0, 100]).range([0, width]);

// Multi-scale chart
const xScale = scaleTime().domain(dateExtent).range([0, width]);
const colorScale = scaleOrdinal(schemeCategory10);
const sizeScale = scaleSqrt().domain([0, maxPop]).range([0, 50]);

// Symmetric domain
const max = d3.max(data, d => Math.abs(d.value));
const yScale = scaleLinear().domain([-max, max]).range([height, 0]);
```

---

## Common Pitfalls

### Pitfall 1: Forgetting to Invert Y Range

```javascript
// WRONG - high values at bottom
const yScale = scaleLinear().domain([0, 100]).range([0, height]);

// CORRECT - high values at top
const yScale = scaleLinear().domain([0, 100]).range([height, 0]);
```

---

### Pitfall 2: Log Scale with Zero

```javascript
// WRONG - log(0) undefined
const scale = scaleLog().domain([0, 1000]);

// CORRECT - start at small positive number
const scale = scaleLog().domain([1, 1000]);
```

---

### Pitfall 3: Not Updating Domain

```javascript
// WRONG - scale domain never changes
const yScale = scaleLinear().domain([0, 100]).range([height, 0]);
update(newData);  // New max might be 200!

// CORRECT
function update(newData) {
  yScale.domain([0, d3.max(newData, d => d.value)]);
  // Re-render with updated scale
}
```

---

### Pitfall 4: Using Band Scale for Quantitative Data

```javascript
// WRONG
const xScale = scaleBand().domain([0, 10, 20, 30]);  // Numbers!

// CORRECT - use linear for numbers
const xScale = scaleLinear().domain([0, 30]).range([0, width]);
```

---

## Next Steps

- Use scales in charts: [Workflows](workflows.md)
- Combine with shape generators: [Shapes & Layouts](shapes-layouts.md)
- Add to interactive charts: [Transitions & Interactions](transitions-interactions.md)
