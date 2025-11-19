# Workflows

## Bar Chart Workflow

### Problem
Display categorical data with quantitative values as vertical bars.

### Steps

1. **Prepare data**
```javascript
const data = [
  {category: 'A', value: 30},
  {category: 'B', value: 80},
  {category: 'C', value: 45}
];
```

2. **Create SVG container**
```javascript
const margin = {top: 20, right: 20, bottom: 30, left: 40};
const width = 600 - margin.left - margin.right;
const height = 400 - margin.top - margin.bottom;

const svg = d3.select('#chart')
  .append('svg')
    .attr('width', width + margin.left + margin.right)
    .attr('height', height + margin.top + margin.bottom)
  .append('g')
    .attr('transform', `translate(${margin.left}, ${margin.top})`);
```

3. **Create scales**
```javascript
const xScale = d3.scaleBand()
  .domain(data.map(d => d.category))
  .range([0, width])
  .padding(0.1);

const yScale = d3.scaleLinear()
  .domain([0, d3.max(data, d => d.value)])
  .range([height, 0]);
```

4. **Create axes**
```javascript
svg.append('g')
  .attr('class', 'x-axis')
  .attr('transform', `translate(0, ${height})`)
  .call(d3.axisBottom(xScale));

svg.append('g')
  .attr('class', 'y-axis')
  .call(d3.axisLeft(yScale));
```

5. **Draw bars**
```javascript
svg.selectAll('rect')
  .data(data)
  .join('rect')
    .attr('x', d => xScale(d.category))
    .attr('y', d => yScale(d.value))
    .attr('width', xScale.bandwidth())
    .attr('height', d => height - yScale(d.value))
    .attr('fill', 'steelblue');
```

### Key Concepts
- **scaleBand**: Positions categorical bars with automatic spacing
- **Inverted Y range**: `[height, 0]` puts origin at bottom-left
- **Height calculation**: `height - yScale(d.value)` computes bar height

---

## Line Chart Workflow

### Problem
Show trends over time or continuous data.

### Steps

1. **Prepare temporal data**
```javascript
const data = [
  {date: new Date(2020, 0, 1), value: 30},
  {date: new Date(2020, 1, 1), value: 80},
  {date: new Date(2020, 2, 1), value: 45}
];
```

2. **Create scales**
```javascript
const xScale = d3.scaleTime()
  .domain(d3.extent(data, d => d.date))
  .range([0, width]);

const yScale = d3.scaleLinear()
  .domain([0, d3.max(data, d => d.value)])
  .range([height, 0]);
```

3. **Create line generator**
```javascript
const line = d3.line()
  .x(d => xScale(d.date))
  .y(d => yScale(d.value))
  .curve(d3.curveMonotoneX);
```

4. **Draw line**
```javascript
svg.append('path')
  .datum(data)
  .attr('d', line)
  .attr('fill', 'none')
  .attr('stroke', 'steelblue')
  .attr('stroke-width', 2);
```

5. **Add axes**
```javascript
svg.append('g')
  .attr('transform', `translate(0, ${height})`)
  .call(d3.axisBottom(xScale).ticks(5));

svg.append('g')
  .call(d3.axisLeft(yScale));
```

### Key Concepts
- **scaleTime**: Handles Date objects automatically
- **d3.extent**: Returns `[min, max]` for domain
- **.datum() vs .data()**: Use `.datum()` for single path, `.data()` for multiple paths
- **fill='none'**: Lines need stroke, not fill

---

## Scatter Plot Workflow

### Problem
Visualize relationship between two quantitative variables.

### Steps

```javascript
// 1. Prepare data and scales
const data = [{x: 10, y: 20}, {x: 40, y: 90}, {x: 80, y: 50}];

const xScale = d3.scaleLinear()
  .domain([0, d3.max(data, d => d.x)])
  .range([0, width]);

const yScale = d3.scaleLinear()
  .domain([0, d3.max(data, d => d.y)])
  .range([height, 0]);

// 2. Draw points
svg.selectAll('circle')
  .data(data)
  .join('circle')
    .attr('cx', d => xScale(d.x))
    .attr('cy', d => yScale(d.y))
    .attr('r', 5)
    .attr('fill', 'steelblue')
    .attr('opacity', 0.7);

// 3. Add axes
svg.append('g').attr('transform', `translate(0, ${height})`).call(d3.axisBottom(xScale));
svg.append('g').call(d3.axisLeft(yScale));
```

### Key Concepts
- **Both linear scales**: X and Y are quantitative
- **Opacity for overlaps**: Helps see density

---

## Update Pattern Workflow

### Problem
Dynamically update visualization when data changes.

### Steps

1. **Initial render**
```javascript
const svg = d3.select('#chart').append('svg')...

function render(data) {
  // Update scale domains
  yScale.domain([0, d3.max(data, d => d.value)]);

  // Update axis
  svg.select('.y-axis')
    .transition()
    .duration(750)
    .call(d3.axisLeft(yScale));

  // Update bars
  svg.selectAll('rect')
    .data(data, d => d.id)  // Key function!
    .join(
      enter => enter.append('rect')
        .attr('x', d => xScale(d.category))
        .attr('y', height)
        .attr('width', xScale.bandwidth())
        .attr('height', 0)
        .attr('fill', 'steelblue')
        .call(enter => enter.transition()
          .duration(750)
          .attr('y', d => yScale(d.value))
          .attr('height', d => height - yScale(d.value))),

      update => update
        .call(update => update.transition()
          .duration(750)
          .attr('y', d => yScale(d.value))
          .attr('height', d => height - yScale(d.value))),

      exit => exit
        .call(exit => exit.transition()
          .duration(750)
          .attr('y', height)
          .attr('height', 0)
          .remove())
    );
}

// Initial render
render(initialData);
```

2. **Update on new data**
```javascript
// Later, when data changes
render(newData);
```

### Key Concepts
- **Encapsulate in function**: Reusable render logic
- **Key function**: Tracks element identity across updates
- **Enter/Update/Exit**: Custom animations for each lifecycle
- **Update domain first**: Recalculate scales before rendering

---

## Network Visualization Workflow

### Problem
Display relationships between entities (nodes and links).

### Steps

1. **Prepare data**
```javascript
const nodes = [
  {id: 'A', group: 1},
  {id: 'B', group: 1},
  {id: 'C', group: 2}
];

const links = [
  {source: 'A', target: 'B'},
  {source: 'B', target: 'C'}
];
```

2. **Create force simulation**
```javascript
const simulation = d3.forceSimulation(nodes)
  .force('link', d3.forceLink(links).id(d => d.id).distance(100))
  .force('charge', d3.forceManyBody().strength(-200))
  .force('center', d3.forceCenter(width / 2, height / 2))
  .force('collide', d3.forceCollide().radius(20));
```

3. **Draw links**
```javascript
const link = svg.append('g')
  .selectAll('line')
  .data(links)
  .join('line')
    .attr('stroke', '#999')
    .attr('stroke-width', 2);
```

4. **Draw nodes**
```javascript
const node = svg.append('g')
  .selectAll('circle')
  .data(nodes)
  .join('circle')
    .attr('r', 10)
    .attr('fill', d => d.group === 1 ? 'steelblue' : 'orange');
```

5. **Update positions on tick**
```javascript
simulation.on('tick', () => {
  link
    .attr('x1', d => d.source.x)
    .attr('y1', d => d.source.y)
    .attr('x2', d => d.target.x)
    .attr('y2', d => d.target.y);

  node
    .attr('cx', d => d.x)
    .attr('cy', d => d.y);
});
```

6. **Add drag behavior**
```javascript
function drag(simulation) {
  function dragstarted(event) {
    if (!event.active) simulation.alphaTarget(0.3).restart();
    event.subject.fx = event.subject.x;
    event.subject.fy = event.subject.y;
  }

  function dragged(event) {
    event.subject.fx = event.x;
    event.subject.fy = event.y;
  }

  function dragended(event) {
    if (!event.active) simulation.alphaTarget(0);
    event.subject.fx = null;
    event.subject.fy = null;
  }

  return d3.drag()
    .on('start', dragstarted)
    .on('drag', dragged)
    .on('end', dragended);
}

node.call(drag(simulation));
```

### Key Concepts
- **forceSimulation**: Physics-based layout
- **tick handler**: Updates positions every frame
- **id accessor**: Links reference nodes by ID
- **fx/fy**: Fixed positions during drag

---

## Hierarchy Visualization (Treemap) Workflow

### Problem
Show hierarchical data with nested rectangles.

### Steps

```javascript
// 1. Prepare and process hierarchy
const data = {name: 'root', children: [{name: 'A', value: 100}, {name: 'B', value: 200}]};

const root = d3.hierarchy(data)
  .sum(d => d.value)
  .sort((a, b) => b.value - a.value);

// 2. Apply layout
d3.treemap().size([width, height]).padding(1)(root);

// 3. Draw rectangles
const colorScale = d3.scaleOrdinal(d3.schemeCategory10);

svg.selectAll('rect')
  .data(root.leaves())
  .join('rect')
    .attr('x', d => d.x0)
    .attr('y', d => d.y0)
    .attr('width', d => d.x1 - d.x0)
    .attr('height', d => d.y1 - d.y0)
    .attr('fill', d => colorScale(d.parent.data.name));
```

### Key Concepts
- **d3.hierarchy**: Creates hierarchy from nested object
- **.sum()**: Aggregates values up tree
- **x0, y0, x1, y1**: Layout computes rectangle bounds

---

## Geographic Map (Choropleth) Workflow

### Problem
Visualize regional data on a map.

### Steps

```javascript
// 1. Load data
Promise.all([d3.json('countries.geojson'), d3.csv('data.csv')])
  .then(([geojson, csvData]) => {
    // 2. Setup projection and path
    const projection = d3.geoMercator().fitExtent([[0, 0], [width, height]], geojson);
    const path = d3.geoPath().projection(projection);

    // 3. Create color scale and data lookup
    const colorScale = d3.scaleSequential(d3.interpolateBlues)
      .domain([0, d3.max(csvData, d => +d.value)]);
    const dataById = new Map(csvData.map(d => [d.id, +d.value]));

    // 4. Draw map
    svg.selectAll('path')
      .data(geojson.features)
      .join('path')
        .attr('d', path)
        .attr('fill', d => dataById.get(d.id) ? colorScale(dataById.get(d.id)) : '#ccc')
        .attr('stroke', '#fff');
  });
```

### Key Concepts
- **fitExtent**: Auto-scales projection to fit bounds
- **geoPath**: Converts GeoJSON to SVG paths
- **Map for lookup**: Fast data join by ID

---

## Real-Time Updates Workflow

### Problem
Continuously update visualization with streaming data.

### Steps

```javascript
// 1. Setup sliding window
const maxPoints = 50;
let data = [];

function update(newValue) {
  data.push({time: new Date(), value: newValue});
  if (data.length > maxPoints) data.shift();

  // 2. Update scales and render
  xScale.domain(d3.extent(data, d => d.time));
  yScale.domain([0, d3.max(data, d => d.value)]);

  svg.select('.x-axis').transition().duration(200).call(d3.axisBottom(xScale));
  svg.select('.y-axis').transition().duration(200).call(d3.axisLeft(yScale));

  const line = d3.line().x(d => xScale(d.time)).y(d => yScale(d.value));
  svg.select('.line').datum(data).transition().duration(200).attr('d', line);
}

// 3. Poll data
setInterval(() => update(Math.random() * 100), 1000);
```

### Key Concepts
- **Sliding window**: Fixed-size buffer
- **Short transitions**: 200ms feels responsive

---

## Linked Views Workflow

### Problem
Coordinate highlighting across multiple charts.

### Steps

```javascript
// 1. Shared event handlers
function highlight(id) {
  svg1.selectAll('circle').attr('opacity', d => d.id === id ? 1 : 0.3);
  svg2.selectAll('rect').attr('opacity', d => d.id === id ? 1 : 0.3);
}

function unhighlight() {
  svg1.selectAll('circle').attr('opacity', 1);
  svg2.selectAll('rect').attr('opacity', 1);
}

// 2. Attach to elements
svg1.selectAll('circle')
  .data(data).join('circle')
  .on('mouseover', (event, d) => highlight(d.id))
  .on('mouseout', unhighlight);

svg2.selectAll('rect')
  .data(data).join('rect')
  .on('mouseover', (event, d) => highlight(d.id))
  .on('mouseout', unhighlight);
```

### Key Concepts
- **Shared state**: Common ID across views
- **Coordinated updates**: Single event updates all charts

## Next Steps

- [Getting Started](getting-started.md) | [Common Patterns](common-patterns.md) | [Selections](selections-datajoins.md) | [Scales](scales-axes.md) | [Shapes](shapes-layouts.md)
