# Shapes & Layouts

## Why Shape Generators Matter

**The Problem**: Creating SVG paths manually for lines, areas, and arcs requires complex math and string concatenation. `<path d="M0,50 L10,40 L20,60...">` is tedious and error-prone.

**D3's Solution**: Shape generators convert data arrays into SVG path strings automatically. You configure the generator, pass data, get path string.

**Key Principle**: "Configure generator once, reuse for all data." Separation of shape logic from data.

---

## Line Generator

### Basic Usage

```javascript
const data = [
  {x: 0, y: 50},
  {x: 100, y: 80},
  {x: 200, y: 40},
  {x: 300, y: 90}
];

const line = d3.line()
  .x(d => d.x)
  .y(d => d.y);

svg.append('path')
  .datum(data)              // Use .datum() for single item
  .attr('d', line)          // line(data) generates path string
  .attr('fill', 'none')
  .attr('stroke', 'steelblue')
  .attr('stroke-width', 2);
```

**Key Methods**:
- `.x(accessor)`: Function returning x coordinate
- `.y(accessor)`: Function returning y coordinate
- Returns path string when called with data

---

### With Scales

```javascript
const xScale = d3.scaleLinear().domain([0, 300]).range([0, width]);
const yScale = d3.scaleLinear().domain([0, 100]).range([height, 0]);

const line = d3.line()
  .x(d => xScale(d.x))
  .y(d => yScale(d.y));
```

---

### Curves

```javascript
const line = d3.line()
  .x(d => xScale(d.x))
  .y(d => yScale(d.y))
  .curve(d3.curveMonotoneX);  // Smooth curve
```

**Curve Types**:
- `d3.curveLinear`: Straight lines (default)
- `d3.curveMonotoneX`: Smooth, preserves monotonicity
- `d3.curveCatmullRom`: Smooth, passes through points
- `d3.curveStep`: Step function
- `d3.curveBasis`: B-spline

---

### Missing Data

```javascript
const line = d3.line()
  .x(d => xScale(d.x))
  .y(d => yScale(d.y))
  .defined(d => d.y !== null);  // Skip null values
```

---

## Area Generator

### Basic Usage

```javascript
const area = d3.area()
  .x(d => xScale(d.x))
  .y0(height)               // Baseline (bottom)
  .y1(d => yScale(d.y));    // Top line

svg.append('path')
  .datum(data)
  .attr('d', area)
  .attr('fill', 'steelblue')
  .attr('opacity', 0.5);
```

**Key Methods**:
- `.y0()`: Baseline (constant or function)
- `.y1()`: Top boundary (usually data-driven)

---

### Stacked Area Chart

```javascript
const stack = d3.stack()
  .keys(['series1', 'series2', 'series3']);

const series = stack(data);  // Returns array of series

const area = d3.area()
  .x(d => xScale(d.data.x))
  .y0(d => yScale(d[0]))    // Lower bound
  .y1(d => yScale(d[1]));   // Upper bound

svg.selectAll('path')
  .data(series)
  .join('path')
    .attr('d', area)
    .attr('fill', (d, i) => colorScale(i));
```

---

## Arc Generator

### Basic Usage

```javascript
const arc = d3.arc()
  .innerRadius(0)           // 0 = pie, >0 = donut
  .outerRadius(100);

const arcData = {
  startAngle: 0,
  endAngle: Math.PI / 2    // 90 degrees
};

svg.append('path')
  .datum(arcData)
  .attr('d', arc)
  .attr('fill', 'steelblue');
```

**Angle Units**: Radians (0 to 2π)

---

### Donut Chart

```javascript
const arc = d3.arc()
  .innerRadius(50)
  .outerRadius(100);

const pie = d3.pie()
  .value(d => d.value);

const arcs = pie(data);    // Generates angles

svg.selectAll('path')
  .data(arcs)
  .join('path')
    .attr('d', arc)
    .attr('fill', (d, i) => colorScale(i));
```

---

### Rounded Corners

```javascript
const arc = d3.arc()
  .innerRadius(50)
  .outerRadius(100)
  .cornerRadius(5);        // Rounded edges
```

---

### Labels

```javascript
// Use centroid for label positioning
svg.selectAll('text')
  .data(arcs)
  .join('text')
    .attr('transform', d => `translate(${arc.centroid(d)})`)
    .attr('text-anchor', 'middle')
    .text(d => d.data.label);
```

---

## Pie Generator

### Basic Usage

```javascript
const data = [30, 80, 45, 60, 20];

const pie = d3.pie();

const arcs = pie(data);
// Returns: [{data: 30, startAngle: 0, endAngle: 0.53, ...}, ...]
```

**What Pie Does**: Converts values → angles. Use with arc generator for rendering.

---

### With Objects

```javascript
const data = [
  {name: 'A', value: 30},
  {name: 'B', value: 80},
  {name: 'C', value: 45}
];

const pie = d3.pie()
  .value(d => d.value);

const arcs = pie(data);
```

---

### Sorting

```javascript
const pie = d3.pie()
  .value(d => d.value)
  .sort((a, b) => b.value - a.value);  // Descending
```

---

### Padding

```javascript
const pie = d3.pie()
  .value(d => d.value)
  .padAngle(0.02);         // Gap between slices
```

---

## Stack Generator

### Basic Usage

```javascript
const data = [
  {month: 'Jan', apples: 30, oranges: 20, bananas: 40},
  {month: 'Feb', apples: 50, oranges: 30, bananas: 35},
  {month: 'Mar', apples: 40, oranges: 25, bananas: 45}
];

const stack = d3.stack()
  .keys(['apples', 'oranges', 'bananas']);

const series = stack(data);
// Returns: [[{0: 0, 1: 30, data: {month: 'Jan', ...}}, ...], [...], [...]]
```

**Output**: Array of series, each with `[lower, upper]` bounds for stacking.

---

### Stacked Bar Chart

```javascript
const xScale = d3.scaleBand()
  .domain(data.map(d => d.month))
  .range([0, width])
  .padding(0.1);

const yScale = d3.scaleLinear()
  .domain([0, d3.max(series, s => d3.max(s, d => d[1]))])
  .range([height, 0]);

svg.selectAll('g')
  .data(series)
  .join('g')
    .attr('fill', (d, i) => colorScale(i))
  .selectAll('rect')
  .data(d => d)
  .join('rect')
    .attr('x', d => xScale(d.data.month))
    .attr('y', d => yScale(d[1]))
    .attr('height', d => yScale(d[0]) - yScale(d[1]))
    .attr('width', xScale.bandwidth());
```

---

### Offsets

```javascript
// Default: stacked on top of each other
const stack = d3.stack().keys(keys);

// Normalized (0-1)
const stack = d3.stack().keys(keys).offset(d3.stackOffsetExpand);

// Centered (streamgraph)
const stack = d3.stack().keys(keys).offset(d3.stackOffsetWiggle);
```

---

## Symbol Generator

### Basic Usage

```javascript
const symbol = d3.symbol()
  .type(d3.symbolCircle)
  .size(100);              // Area in square pixels

svg.append('path')
  .attr('d', symbol())
  .attr('fill', 'steelblue');
```

**Symbol Types**:
- `symbolCircle`, `symbolCross`, `symbolDiamond`, `symbolSquare`, `symbolStar`, `symbolTriangle`, `symbolWye`

---

### In Scatter Plots

```javascript
const symbol = d3.symbol()
  .type(d => d3.symbolCircle)
  .size(d => sizeScale(d.value));

svg.selectAll('path')
  .data(data)
  .join('path')
    .attr('d', symbol)
    .attr('transform', d => `translate(${xScale(d.x)}, ${yScale(d.y)})`);
```

---

## Complete Examples

### Line Chart

```javascript
const xScale = d3.scaleTime().domain(d3.extent(data, d => d.date)).range([0, width]);
const yScale = d3.scaleLinear().domain([0, d3.max(data, d => d.value)]).range([height, 0]);

const line = d3.line()
  .x(d => xScale(d.date))
  .y(d => yScale(d.value))
  .curve(d3.curveMonotoneX);

svg.append('path')
  .datum(data)
  .attr('d', line)
  .attr('fill', 'none')
  .attr('stroke', 'steelblue')
  .attr('stroke-width', 2);

svg.append('g').attr('transform', `translate(0, ${height})`).call(d3.axisBottom(xScale));
svg.append('g').call(d3.axisLeft(yScale));
```

---

### Area Chart

```javascript
const area = d3.area()
  .x(d => xScale(d.date))
  .y0(height)
  .y1(d => yScale(d.value))
  .curve(d3.curveMonotoneX);

svg.append('path')
  .datum(data)
  .attr('d', area)
  .attr('fill', 'steelblue')
  .attr('opacity', 0.5);
```

---

### Donut Chart

```javascript
const pie = d3.pie().value(d => d.value);
const arc = d3.arc().innerRadius(50).outerRadius(100);

const arcs = pie(data);

svg.selectAll('path')
  .data(arcs)
  .join('path')
    .attr('d', arc)
    .attr('fill', (d, i) => colorScale(i))
    .attr('stroke', 'white')
    .attr('stroke-width', 2);

svg.selectAll('text')
  .data(arcs)
  .join('text')
    .attr('transform', d => `translate(${arc.centroid(d)})`)
    .attr('text-anchor', 'middle')
    .text(d => d.data.label);
```

---

### Stacked Bar Chart

```javascript
const stack = d3.stack().keys(['series1', 'series2', 'series3']);
const series = stack(data);

const xScale = d3.scaleBand().domain(data.map(d => d.category)).range([0, width]).padding(0.1);
const yScale = d3.scaleLinear().domain([0, d3.max(series, s => d3.max(s, d => d[1]))]).range([height, 0]);

svg.selectAll('g')
  .data(series)
  .join('g')
    .attr('fill', (d, i) => colorScale(i))
  .selectAll('rect')
  .data(d => d)
  .join('rect')
    .attr('x', d => xScale(d.data.category))
    .attr('y', d => yScale(d[1]))
    .attr('height', d => yScale(d[0]) - yScale(d[1]))
    .attr('width', xScale.bandwidth());
```

---

## Common Pitfalls

### Pitfall 1: Using .data() Instead of .datum()

```javascript
// WRONG - creates path per data point
svg.selectAll('path').data(data).join('path').attr('d', line);

// CORRECT - single path for entire dataset
svg.append('path').datum(data).attr('d', line);
```

---

### Pitfall 2: Forgetting fill="none" for Lines

```javascript
// WRONG - area filled by default
svg.append('path').datum(data).attr('d', line);

// CORRECT
svg.append('path').datum(data).attr('d', line).attr('fill', 'none').attr('stroke', 'steelblue');
```

---

### Pitfall 3: Wrong Angle Units

```javascript
// WRONG - degrees
arc.startAngle(90).endAngle(180);

// CORRECT - radians
arc.startAngle(Math.PI / 2).endAngle(Math.PI);
```

---

## Next Steps

- Apply to real data: [Workflows](workflows.md)
- Add transitions: [Transitions & Interactions](transitions-interactions.md)
- Combine with layouts: [Advanced Layouts](advanced-layouts.md)
