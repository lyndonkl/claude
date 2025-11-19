# Common D3 Patterns - Code Templates

## Bar Chart Template

```javascript
const data = [{label: 'A', value: 30}, {label: 'B', value: 80}, {label: 'C', value: 45}];

const xScale = d3.scaleBand()
  .domain(data.map(d => d.label))
  .range([0, width])
  .padding(0.1);

const yScale = d3.scaleLinear()
  .domain([0, d3.max(data, d => d.value)])
  .range([height, 0]);

svg.selectAll('rect')
  .data(data)
  .join('rect')
    .attr('x', d => xScale(d.label))
    .attr('y', d => yScale(d.value))
    .attr('width', xScale.bandwidth())
    .attr('height', d => height - yScale(d.value))
    .attr('fill', 'steelblue');

svg.append('g').attr('transform', `translate(0, ${height})`).call(d3.axisBottom(xScale));
svg.append('g').call(d3.axisLeft(yScale));
```

## Line Chart Template

```javascript
const parseDate = d3.timeParse('%Y-%m-%d');
data.forEach(d => { d.date = parseDate(d.date); });

const xScale = d3.scaleTime()
  .domain(d3.extent(data, d => d.date))
  .range([0, width]);

const yScale = d3.scaleLinear()
  .domain([0, d3.max(data, d => d.value)])
  .range([height, 0]);

const line = d3.line()
  .x(d => xScale(d.date))
  .y(d => yScale(d.value));

svg.append('path')
  .datum(data)
  .attr('d', line)
  .attr('fill', 'none')
  .attr('stroke', 'steelblue')
  .attr('stroke-width', 2);

svg.append('g').attr('transform', `translate(0, ${height})`).call(d3.axisBottom(xScale));
svg.append('g').call(d3.axisLeft(yScale));
```

## Scatter Plot Template

```javascript
const xScale = d3.scaleLinear()
  .domain(d3.extent(data, d => d.x))
  .range([0, width]);

const yScale = d3.scaleLinear()
  .domain(d3.extent(data, d => d.y))
  .range([height, 0]);

const colorScale = d3.scaleOrdinal(d3.schemeCategory10);

svg.selectAll('circle')
  .data(data)
  .join('circle')
    .attr('cx', d => xScale(d.x))
    .attr('cy', d => yScale(d.y))
    .attr('r', 5)
    .attr('fill', d => colorScale(d.category))
    .attr('opacity', 0.7);
```

## Network Graph Template

```javascript
const simulation = d3.forceSimulation(nodes)
  .force('link', d3.forceLink(links).id(d => d.id))
  .force('charge', d3.forceManyBody().strength(-100))
  .force('center', d3.forceCenter(width / 2, height / 2));

const link = svg.selectAll('line')
  .data(links)
  .join('line')
    .attr('stroke', '#999');

const node = svg.selectAll('circle')
  .data(nodes)
  .join('circle')
    .attr('r', 10)
    .attr('fill', d => d3.schemeCategory10[d.group]);

simulation.on('tick', () => {
  link.attr('x1', d => d.source.x).attr('y1', d => d.source.y)
      .attr('x2', d => d.target.x).attr('y2', d => d.target.y);
  node.attr('cx', d => d.x).attr('cy', d => d.y);
});
```

## Treemap Template

```javascript
const root = d3.hierarchy(data)
  .sum(d => d.value)
  .sort((a, b) => b.value - a.value);

const treemap = d3.treemap().size([width, height]).padding(1);
treemap(root);

svg.selectAll('rect')
  .data(root.leaves())
  .join('rect')
    .attr('x', d => d.x0)
    .attr('y', d => d.y0)
    .attr('width', d => d.x1 - d.x0)
    .attr('height', d => d.y1 - d.y0)
    .attr('fill', d => d3.interpolateBlues(d.value / root.value));

svg.selectAll('text')
  .data(root.leaves())
  .join('text')
    .attr('x', d => d.x0 + 5)
    .attr('y', d => d.y0 + 15)
    .text(d => d.data.name);
```

## Geographic Map Template

```javascript
d3.json('world.geojson').then(geojson => {
  const projection = d3.geoMercator()
    .fitExtent([[0, 0], [width, height]], geojson);

  const path = d3.geoPath().projection(projection);

  svg.selectAll('path')
    .data(geojson.features)
    .join('path')
      .attr('d', path)
      .attr('fill', '#ccc')
      .attr('stroke', '#fff');
});
```

## Zoom and Pan Pattern

```javascript
const zoom = d3.zoom()
  .scaleExtent([0.5, 5])
  .on('zoom', (event) => g.attr('transform', event.transform));

svg.call(zoom);

const g = svg.append('g');
g.selectAll('circle').data(data).join('circle')...
```

## Brush Selection Pattern

```javascript
const brush = d3.brush()
  .extent([[0, 0], [width, height]])
  .on('end', (event) => {
    if (!event.selection) return;
    const [[x0, y0], [x1, y1]] = event.selection;
    const selected = data.filter(d => {
      const x = xScale(d.x), y = yScale(d.y);
      return x >= x0 && x <= x1 && y >= y0 && y <= y1;
    });
    updateChart(selected);
  });

svg.append('g').attr('class', 'brush').call(brush);
```

## Transition Pattern

```javascript
function update(newData) {
  yScale.domain([0, d3.max(newData, d => d.value)]);

  svg.selectAll('rect')
    .data(newData)
    .join('rect')
    .transition().duration(750).ease(d3.easeCubicOut)
      .attr('y', d => yScale(d.value))
      .attr('height', d => height - yScale(d.value));

  svg.select('.y-axis').transition().duration(750).call(d3.axisLeft(yScale));
}
```

## Tooltip Pattern

```javascript
const tooltip = d3.select('body').append('div')
  .attr('class', 'tooltip')
  .style('position', 'absolute')
  .style('visibility', 'hidden');

svg.selectAll('circle')
  .data(data)
  .join('circle')
    .attr('r', 5)
    .on('mouseover', (event, d) => {
      tooltip.style('visibility', 'visible').html(`Value: ${d.value}`);
    })
    .on('mousemove', (event) => {
      tooltip.style('top', (event.pageY - 10) + 'px')
             .style('left', (event.pageX + 10) + 'px');
    })
    .on('mouseout', () => tooltip.style('visibility', 'hidden'));
```
