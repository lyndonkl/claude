# Advanced Layouts

## Why Layouts Matter

**The Problem**: Calculating positions for complex visualizations (network graphs, treemaps, maps) involves sophisticated algorithms—force-directed simulation, spatial partitioning, map projections—that are mathematically complex.

**D3's Solution**: Layout generators compute positions/sizes/angles automatically. You provide data, configure layout, receive computed coordinates.

**Key Principle**: "Layouts transform data, don't render." Layouts add properties (`x`, `y`, `width`, etc.) that you bind to visual elements.

---

## Force Simulation

### Why Force Layouts

**Use Case**: Network diagrams, organic clustering where fixed positions are unnatural.

**How It Works**: Physics simulation with forces (repulsion, attraction, gravity) that iteratively compute node positions.

---

### Basic Setup

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

const simulation = d3.forceSimulation(nodes)
  .force('link', d3.forceLink(links).id(d => d.id))
  .force('charge', d3.forceManyBody())
  .force('center', d3.forceCenter(width / 2, height / 2));
```

---

### Forces

**forceLink**: Maintains fixed distance between connected nodes
```javascript
.force('link', d3.forceLink(links)
  .id(d => d.id)
  .distance(50))
```

**forceManyBody**: Repulsion (negative) or attraction (positive)
```javascript
.force('charge', d3.forceManyBody().strength(-100))
```

**forceCenter**: Pulls nodes toward center point
```javascript
.force('center', d3.forceCenter(width / 2, height / 2))
```

**forceCollide**: Prevents overlapping circles
```javascript
.force('collide', d3.forceCollide().radius(20))
```

**forceX / forceY**: Attracts to specific coordinates
```javascript
.force('x', d3.forceX(width / 2).strength(0.1))
```

---

### Rendering

```javascript
const link = svg.selectAll('line')
  .data(links)
  .join('line')
    .attr('stroke', '#999');

const node = svg.selectAll('circle')
  .data(nodes)
  .join('circle')
    .attr('r', 10)
    .attr('fill', d => colorScale(d.group));

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

**Key**: Update positions in `tick` handler as simulation runs.

---

### Drag Behavior

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

---

## Hierarchies

### Creating Hierarchies

```javascript
const data = {
  name: 'root',
  children: [
    {name: 'child1', value: 10},
    {name: 'child2', value: 20, children: [{name: 'grandchild', value: 5}]}
  ]
};

const root = d3.hierarchy(data)
  .sum(d => d.value)           // Aggregate values up tree
  .sort((a, b) => b.value - a.value);
```

**Key Methods**:
- `hierarchy(data)`: Creates hierarchy from nested object
- `.sum(accessor)`: Computes values (leaf → root)
- `.sort(comparator)`: Orders siblings
- `.descendants()`: All nodes (breadth-first)
- `.leaves()`: Leaf nodes only

---

### Tree Layout

**Use**: Node-link diagrams (org charts, file systems)

```javascript
const tree = d3.tree().size([width, height]);
tree(root);

// Creates x, y properties on each node
svg.selectAll('circle')
  .data(root.descendants())
  .join('circle')
    .attr('cx', d => d.x)
    .attr('cy', d => d.y)
    .attr('r', 5);

// Links
svg.selectAll('line')
  .data(root.links())
  .join('line')
    .attr('x1', d => d.source.x)
    .attr('y1', d => d.source.y)
    .attr('x2', d => d.target.x)
    .attr('y2', d => d.target.y);
```

---

### Treemap Layout

**Use**: Space-filling rectangles (disk usage, budget allocation)

```javascript
const treemap = d3.treemap()
  .size([width, height])
  .padding(1);

treemap(root);

svg.selectAll('rect')
  .data(root.leaves())
  .join('rect')
    .attr('x', d => d.x0)
    .attr('y', d => d.y0)
    .attr('width', d => d.x1 - d.x0)
    .attr('height', d => d.y1 - d.y0)
    .attr('fill', d => colorScale(d.value));
```

---

### Pack Layout

**Use**: Circle packing (bubble charts)

```javascript
const pack = d3.pack().size([width, height]).padding(3);
pack(root);

svg.selectAll('circle')
  .data(root.descendants())
  .join('circle')
    .attr('cx', d => d.x)
    .attr('cy', d => d.y)
    .attr('r', d => d.r)
    .attr('fill', d => d.children ? '#ccc' : colorScale(d.value));
```

---

### Partition Layout

**Use**: Sunburst, icicle charts

```javascript
const partition = d3.partition().size([2 * Math.PI, radius]);
partition(root);

const arc = d3.arc()
  .startAngle(d => d.x0)
  .endAngle(d => d.x1)
  .innerRadius(d => d.y0)
  .outerRadius(d => d.y1);

svg.selectAll('path')
  .data(root.descendants())
  .join('path')
    .attr('d', arc)
    .attr('fill', d => colorScale(d.depth));
```

---

## Geographic Maps

### GeoJSON

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Polygon",
        "coordinates": [[[-100, 40], [-100, 50], [-90, 50], [-90, 40], [-100, 40]]]
      },
      "properties": {"name": "Region A"}
    }
  ]
}
```

---

### Projections

```javascript
// Mercator (world maps)
const projection = d3.geoMercator()
  .center([0, 0])
  .scale(150)
  .translate([width / 2, height / 2]);

// Albers (US maps)
const projection = d3.geoAlbersUsa().scale(1000).translate([width / 2, height / 2]);

// Orthographic (globe)
const projection = d3.geoOrthographic().scale(250).translate([width / 2, height / 2]);
```

**Common Projections**: Mercator, Albers, Equirectangular, Orthographic, Azimuthal, Conic

---

### Path Generator

```javascript
const path = d3.geoPath().projection(projection);

d3.json('countries.geojson').then(geojson => {
  svg.selectAll('path')
    .data(geojson.features)
    .join('path')
      .attr('d', path)
      .attr('fill', '#ccc')
      .attr('stroke', '#fff');
});
```

---

### Auto-Fit

```javascript
const projection = d3.geoMercator()
  .fitExtent([[0, 0], [width, height]], geojson);
```

**fitExtent**: Automatically scales/centers projection to fit data in bounds.

---

### Choropleth

```javascript
const colorScale = d3.scaleSequential(d3.interpolateBlues)
  .domain([0, d3.max(data, d => d.value)]);

svg.selectAll('path')
  .data(geojson.features)
  .join('path')
    .attr('d', path)
    .attr('fill', d => {
      const value = data.find(v => v.id === d.id)?.value;
      return value ? colorScale(value) : '#ccc';
    });
```

---

## Chord Diagrams

### Use Case
Visualize flows/relationships between entities (migrations, trade, connections).

---

### Data Format

```javascript
const matrix = [
  [0, 10, 20],    // From A to: A, B, C
  [15, 0, 5],     // From B to: A, B, C
  [25, 30, 0]     // From C to: A, B, C
];
```

**Matrix[i][j]**: Flow from entity i to entity j.

---

### Creating Chord

```javascript
const chord = d3.chord()
  .padAngle(0.05)
  .sortSubgroups(d3.descending);

const chords = chord(matrix);

const arc = d3.arc()
  .innerRadius(200)
  .outerRadius(220);

const ribbon = d3.ribbon()
  .radius(200);

// Outer arcs (groups)
svg.selectAll('g')
  .data(chords.groups)
  .join('path')
    .attr('d', arc)
    .attr('fill', (d, i) => colorScale(i));

// Inner ribbons (connections)
svg.selectAll('path.ribbon')
  .data(chords)
  .join('path')
    .attr('class', 'ribbon')
    .attr('d', ribbon)
    .attr('fill', d => colorScale(d.source.index))
    .attr('opacity', 0.7);
```

---

## Choosing Layouts

| Visualization | Layout |
|---------------|--------|
| Network graph, organic clusters | Force simulation |
| Org chart, file tree (node-link) | Tree layout |
| Space-filling rectangles | Treemap |
| Bubble chart, circle packing | Pack layout |
| Sunburst, icicle chart | Partition layout |
| World/regional maps | Geographic projection |
| Flow diagram (migration, trade) | Chord diagram |

---

## Common Pitfalls

### Pitfall 1: Not Handling Tick Updates

```javascript
// WRONG - positions never update
const node = svg.selectAll('circle').data(nodes).join('circle');
simulation.on('tick', () => {});  // Empty!

// CORRECT
simulation.on('tick', () => {
  node.attr('cx', d => d.x).attr('cy', d => d.y);
});
```

---

### Pitfall 2: Wrong Hierarchy Accessor

```javascript
// WRONG - d3.hierarchy expects nested structure
const root = d3.hierarchy(flatArray);

// CORRECT - nest data first or use stratify
const root = d3.hierarchy(nestedObject);
```

---

### Pitfall 3: Forgetting to Apply Layout

```javascript
// WRONG - root has no x, y properties
const root = d3.hierarchy(data);
svg.selectAll('circle').data(root.descendants()).join('circle').attr('cx', d => d.x);

// CORRECT - apply layout first
const tree = d3.tree().size([width, height]);
tree(root);  // Now root.descendants() have x, y
```

---

## Next Steps

- See complete workflows: [Workflows](workflows.md)
- Add interactions: [Transitions & Interactions](transitions-interactions.md)
- Use code templates: [Common Patterns](common-patterns.md)
