# Getting Started with D3.js

## Why Learn D3

**Problem D3 Solves**: Chart libraries (Chart.js, Highcharts, Plotly) offer pre-made chart types with limited customization. When you need bespoke visualizations—unusual chart types, specific interactions, custom layouts—you need low-level control. D3 provides primitive building blocks that compose into any visualization.

**Trade-off**: Steeper learning curve and more code than chart libraries, but unlimited customization and flexibility.

**When D3 is the Right Choice**:
- Custom visualization designs not available in libraries
- Complex interactions (linked views, custom brushing, coordinated highlighting)
- Network graphs, force-directed layouts, geographic maps
- Full control over visual encoding, transitions, animations
- Integration with data pipelines for real-time dashboards

---

## Prerequisites

D3 assumes you know these web technologies:

**Required**:
- **HTML**: Document structure, elements, attributes
- **SVG**: Scalable Vector Graphics (`<svg>`, `<circle>`, `<rect>`, `<path>`, `viewBox`, transforms)
- **CSS**: Styling, selectors, specificity
- **JavaScript**: ES6 syntax, functions, arrays, objects, arrow functions, promises, async/await

**Helpful**:
- Modern frameworks (React, Vue) for integration patterns
- Data formats (CSV, JSON, GeoJSON)
- Basic statistics (distributions, correlations) for visualization design

**If you lack prerequisites**: Learn HTML/SVG/CSS/JavaScript fundamentals first. D3 documentation assumes this knowledge.

---

## Setup

### Option 1: CodePen (Recommended for Learning)

**Quick start without tooling**:

1. **Create HTML file** (`index.html`):
```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>D3 Visualization</title>
  <style>
    svg { border: 1px solid #ccc; }
  </style>
</head>
<body>
  <svg width="600" height="400"></svg>
  <script type="module" src="index.js"></script>
</body>
</html>
```

2. **Create JavaScript file** (`index.js`):
```javascript
// Import from Skypack CDN (ESM)
import * as d3 from 'https://cdn.skypack.dev/d3@7';

// Your D3 code here
console.log(d3.version);
```

3. **Open HTML in browser** or use Live Server extension in VS Code

---

### Option 2: Bundler (Vite, Webpack)

**For production apps**:

1. **Install D3**:
```bash
npm install d3
```

2. **Import modules**:
```javascript
// Import specific modules (recommended - smaller bundle)
import { select, selectAll } from 'd3-selection';
import { scaleLinear, scaleBand } from 'd3-scale';
import { axisBottom, axisLeft } from 'd3-axis';

// Or import entire D3 namespace
import * as d3 from 'd3';
```

3. **Use in your code**:
```javascript
const svg = d3.select('svg');
```

---

### Option 3: UMD Script Tag (Legacy)

```html
<script src="https://d3js.org/d3.v7.min.js"></script>
<script>
  // d3 available globally
  const svg = d3.select('svg');
</script>
```

**Note**: Modern approach uses ES modules (options 1-2).

---

## Core Concepts

### Concept 1: Selections

**What**: D3 selections are wrappers around DOM elements enabling method chaining for manipulation.

**Why**: Declarative syntax; modify multiple elements concisely.

**Basic Pattern**:
```javascript
// Select single element
const svg = d3.select('svg');

// Select all matching elements
const circles = d3.selectAll('circle');

// Modify attributes
circles.attr('r', 10).attr('fill', 'steelblue');

// Add elements
svg.append('circle').attr('cx', 50).attr('cy', 50).attr('r', 20);
```

**Methods**:
- `.select(selector)`: First matching element
- `.selectAll(selector)`: All matching elements
- `.attr(name, value)`: Set attribute
- `.style(name, value)`: Set CSS style
- `.text(value)`: Set text content
- `.append(type)`: Create and append child
- `.remove()`: Delete elements

---

### Concept 2: Data Joins

**What**: Binding data arrays to DOM elements, establishing one-to-one correspondence.

**Why**: Enables data-driven visualizations; DOM automatically reflects data changes.

**Pattern**:
```javascript
const data = [10, 20, 30, 40, 50];

svg.selectAll('circle')
  .data(data)               // Bind array to selection
  .join('circle')           // Create/update/remove elements to match data
    .attr('cx', (d, i) => i * 50 + 25)  // d = datum, i = index
    .attr('cy', 50)
    .attr('r', d => d);     // Radius = data value
```

**What `.join()` does**:
- **Enter**: Creates new elements for array items without elements
- **Update**: Updates existing elements
- **Exit**: Removes elements without corresponding array items

---

### Concept 3: Scales

**What**: Functions mapping data domain (input range) to visual range (output values).

**Why**: Data values (e.g., 0-1000) don't directly map to pixels. Scales handle transformation.

**Example**:
```javascript
const data = [{x: 0}, {x: 50}, {x: 100}];

// Create scale
const xScale = d3.scaleLinear()
  .domain([0, 100])         // Data min/max
  .range([0, 500]);         // Pixel min/max

// Use scale
svg.selectAll('circle')
  .data(data)
  .join('circle')
    .attr('cx', d => xScale(d.x));  // 0→0px, 50→250px, 100→500px
```

**Common scales**:
- `scaleLinear()`: Quantitative, proportional
- `scaleBand()`: Categorical, for bars
- `scaleTime()`: Temporal data
- `scaleOrdinal()`: Categorical → categories (colors)

---

### Concept 4: Method Chaining

**What**: D3 methods return the selection, enabling sequential calls.

**Why**: Concise, readable code that mirrors workflow steps.

**Example**:
```javascript
d3.select('svg')
  .append('g')
  .attr('transform', 'translate(50, 50)')
  .selectAll('rect')
  .data(data)
  .join('rect')
  .attr('x', (d, i) => i * 40)
  .attr('y', d => height - d.value)
  .attr('width', 30)
  .attr('height', d => d.value)
  .attr('fill', 'steelblue');
```

Reads like: "Select SVG → append group → position group → select rects → bind data → create rects → set attributes"

---

## First Visualization: Simple Bar Chart

### Goal
Create a vertical bar chart from array `[30, 80, 45, 60, 20, 90, 50]`.

### Setup SVG Container

```javascript
// Dimensions
const width = 500;
const height = 300;
const margin = {top: 20, right: 20, bottom: 30, left: 40};
const innerWidth = width - margin.left - margin.right;
const innerHeight = height - margin.top - margin.bottom;

// Create SVG
const svg = d3.select('svg')
  .attr('width', width)
  .attr('height', height);

// Create inner group for margins
const g = svg.append('g')
  .attr('transform', `translate(${margin.left}, ${margin.top})`);
```

**Why margins?** Leave space for axes outside the data area.

---

### Create Data and Scales

```javascript
// Data
const data = [30, 80, 45, 60, 20, 90, 50];

// X scale (categorical - bar positions)
const xScale = d3.scaleBand()
  .domain(d3.range(data.length))  // [0, 1, 2, 3, 4, 5, 6]
  .range([0, innerWidth])
  .padding(0.1);                  // 10% spacing between bars

// Y scale (quantitative - bar heights)
const yScale = d3.scaleLinear()
  .domain([0, d3.max(data)])      // 0 to 90
  .range([innerHeight, 0]);       // Inverted (SVG y increases downward)
```

**Why inverted y-range?** SVG y-axis increases downward; we want high values at top.

---

### Create Bars

```javascript
g.selectAll('rect')
  .data(data)
  .join('rect')
    .attr('x', (d, i) => xScale(i))
    .attr('y', d => yScale(d))
    .attr('width', xScale.bandwidth())
    .attr('height', d => innerHeight - yScale(d))
    .attr('fill', 'steelblue');
```

**Breakdown**:
- `x`: Bar position from xScale
- `y`: Top of bar from yScale
- `width`: Automatic from scaleBand
- `height`: Distance from bar top to bottom (innerHeight - y)

---

### Add Axes

```javascript
// X axis
g.append('g')
  .attr('transform', `translate(0, ${innerHeight})`)
  .call(d3.axisBottom(xScale));

// Y axis
g.append('g')
  .call(d3.axisLeft(yScale));
```

**What `.call()` does**: Invokes function with selection as argument. `d3.axisBottom(xScale)` is a function that generates axis.

---

### Complete Code

```javascript
import * as d3 from 'https://cdn.skypack.dev/d3@7';

const width = 500, height = 300;
const margin = {top: 20, right: 20, bottom: 30, left: 40};
const innerWidth = width - margin.left - margin.right;
const innerHeight = height - margin.top - margin.bottom;

const data = [30, 80, 45, 60, 20, 90, 50];

const svg = d3.select('svg').attr('width', width).attr('height', height);
const g = svg.append('g').attr('transform', `translate(${margin.left}, ${margin.top})`);

const xScale = d3.scaleBand()
  .domain(d3.range(data.length))
  .range([0, innerWidth])
  .padding(0.1);

const yScale = d3.scaleLinear()
  .domain([0, d3.max(data)])
  .range([innerHeight, 0]);

g.selectAll('rect')
  .data(data)
  .join('rect')
    .attr('x', (d, i) => xScale(i))
    .attr('y', d => yScale(d))
    .attr('width', xScale.bandwidth())
    .attr('height', d => innerHeight - yScale(d))
    .attr('fill', 'steelblue');

g.append('g').attr('transform', `translate(0, ${innerHeight})`).call(d3.axisBottom(xScale));
g.append('g').call(d3.axisLeft(yScale));
```

---

## Loading Data

### CSV Files

**File**: `data.csv`
```
name,value
A,30
B,80
C,45
```

**Load and Parse**:
```javascript
d3.csv('data.csv').then(data => {
  // data = [{name: 'A', value: '30'}, ...] (values are strings!)

  // Convert strings to numbers
  data.forEach(d => { d.value = +d.value; });

  // Or use conversion function
  d3.csv('data.csv', d => ({
    name: d.name,
    value: +d.value
  })).then(data => {
    // Now d.value is number
    createVisualization(data);
  });
});
```

**Key Points**:
- Returns Promise
- Values are strings by default (CSV has no types)
- Use `+` operator or `parseFloat()` for numbers
- Use `d3.timeParse()` for dates

---

### JSON Files

**File**: `data.json`
```json
[
  {"name": "A", "value": 30},
  {"name": "B", "value": 80}
]
```

**Load**:
```javascript
d3.json('data.json').then(data => {
  // data already has correct types
  createVisualization(data);
});
```

**Advantage**: Types preserved (numbers are numbers, not strings).

---

### Async/Await Pattern

```javascript
async function init() {
  const data = await d3.csv('data.csv', d => ({
    name: d.name,
    value: +d.value
  }));

  createVisualization(data);
}

init();
```

---

## Common Pitfalls

### Pitfall 1: Forgetting Data Type Conversion

```javascript
// WRONG - CSV values are strings
d3.csv('data.csv').then(data => {
  const max = d3.max(data, d => d.value);  // String comparison! '9' > '80'
});

// CORRECT
d3.csv('data.csv').then(data => {
  data.forEach(d => { d.value = +d.value; });
  const max = d3.max(data, d => d.value);  // Numeric comparison
});
```

---

### Pitfall 2: Inverted Y-Axis

```javascript
// WRONG - bars upside down
const yScale = scaleLinear().domain([0, 100]).range([0, height]);

// CORRECT - high values at top
const yScale = scaleLinear().domain([0, 100]).range([height, 0]);
```

---

### Pitfall 3: Missing Margins

```javascript
// WRONG - axes overlap chart
svg.selectAll('rect').attr('x', d => xScale(d.x))...

// CORRECT - use margin convention
const g = svg.append('g').attr('transform', `translate(${margin.left}, ${margin.top})`);
g.selectAll('rect').attr('x', d => xScale(d.x))...
```

---

### Pitfall 4: Not Using .call() for Axes

```javascript
// WRONG - won't work
g.append('g').axisBottom(xScale);

// CORRECT
g.append('g').call(d3.axisBottom(xScale));
```

---

## Next Steps

- **Understand data joins**: [Selections & Data Joins](selections-datajoins.md)
- **Master scales**: [Scales & Axes](scales-axes.md)
- **Build more charts**: [Workflows](workflows.md)
- **Add interactions**: [Transitions & Interactions](transitions-interactions.md)
