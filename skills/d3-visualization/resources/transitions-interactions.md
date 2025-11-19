# Transitions & Interactions

## Transitions

### Why Transitions Matter

**The Problem**: Instant changes are jarring. Users miss updates or lose track of which element changed.

**D3's Solution**: Smooth interpolation between old and new states over time. Movement helps users track element identity (object constancy).

**When to Use**: Data updates, not initial render. Transitions show *change*, so there must be a previous state.

---

### Basic Pattern

```javascript
// Without transition (instant)
selection.attr('r', 10);

// With transition (animated)
selection.transition().duration(500).attr('r', 10);
```

**Key**: Insert `.transition()` before `.attr()` or `.style()` calls you want animated.

---

### Duration and Delay

```javascript
selection
  .transition()
  .duration(750)           // Milliseconds
  .delay(100)              // Wait before starting
  .attr('r', 20);

// Staggered (delay per element)
selection
  .transition()
  .duration(500)
  .delay((d, i) => i * 50)  // 0ms, 50ms, 100ms...
  .attr('opacity', 1);
```

---

### Easing Functions

```javascript
selection
  .transition()
  .duration(500)
  .ease(d3.easeCubicOut)   // Fast start, slow finish
  .attr('r', 20);
```

**Common Easings**:
- `d3.easeLinear`: Constant speed
- `d3.easeCubicIn`: Slow start
- `d3.easeCubicOut`: Slow finish
- `d3.easeCubic`: Slow start and finish
- `d3.easeBounceOut`: Bouncing effect
- `d3.easeElasticOut`: Elastic spring

---

### Chained Transitions

```javascript
selection
  .transition()
  .duration(500)
  .attr('r', 20)
  .transition()            // Second transition starts after first
  .duration(500)
  .attr('fill', 'red');
```

---

### Named Transitions

```javascript
// Interrupt previous transition with same name
selection
  .transition('resize')
  .duration(500)
  .attr('r', 20);

// Later (cancels previous 'resize' transition)
selection
  .transition('resize')
  .attr('r', 30);
```

---

### Update Pattern with Transitions

```javascript
function update(newData) {
  // Update scale
  yScale.domain([0, d3.max(newData, d => d.value)]);

  // Update bars
  svg.selectAll('rect')
    .data(newData, d => d.id)  // Key function
    .join('rect')
    .transition()
    .duration(750)
      .attr('y', d => yScale(d.value))
      .attr('height', d => height - yScale(d.value));

  // Update axis
  svg.select('.y-axis')
    .transition()
    .duration(750)
    .call(d3.axisLeft(yScale));
}
```

---

### Enter/Exit Transitions

```javascript
svg.selectAll('circle')
  .data(data, d => d.id)
  .join(
    enter => enter.append('circle')
      .attr('r', 0)
      .call(enter => enter.transition().attr('r', 5)),

    update => update
      .call(update => update.transition().attr('fill', 'blue')),

    exit => exit
      .call(exit => exit.transition().attr('r', 0).remove())
  );
```

---

## Interactions

### Event Handling

```javascript
selection.on('click', function(event, d) {
  console.log('Clicked', d);
  d3.select(this).attr('fill', 'red');
});
```

**Common Events**: `click`, `mouseover`, `mouseout`, `mousemove`, `dblclick`

---

### Tooltips

```javascript
const tooltip = d3.select('body').append('div')
  .attr('class', 'tooltip')
  .style('position', 'absolute')
  .style('visibility', 'hidden')
  .style('background', '#fff')
  .style('padding', '5px')
  .style('border', '1px solid #ccc');

svg.selectAll('circle')
  .data(data)
  .join('circle')
    .attr('r', 5)
    .on('mouseover', (event, d) => {
      tooltip.style('visibility', 'visible')
             .html(`<strong>${d.label}</strong><br/>Value: ${d.value}`);
    })
    .on('mousemove', (event) => {
      tooltip.style('top', (event.pageY - 10) + 'px')
             .style('left', (event.pageX + 10) + 'px');
    })
    .on('mouseout', () => {
      tooltip.style('visibility', 'hidden');
    });
```

---

### Hover Effects

```javascript
svg.selectAll('rect')
  .data(data)
  .join('rect')
    .attr('fill', 'steelblue')
    .on('mouseover', function() {
      d3.select(this)
        .transition()
        .duration(200)
        .attr('fill', 'orange');
    })
    .on('mouseout', function() {
      d3.select(this)
        .transition()
        .duration(200)
        .attr('fill', 'steelblue');
    });
```

---

## Drag Behavior

### Basic Dragging

```javascript
const drag = d3.drag()
  .on('start', dragstarted)
  .on('drag', dragged)
  .on('end', dragended);

function dragstarted(event, d) {
  d3.select(this).raise().attr('stroke', 'black');
}

function dragged(event, d) {
  d3.select(this)
    .attr('cx', event.x)
    .attr('cy', event.y);
}

function dragended(event, d) {
  d3.select(this).attr('stroke', null);
}

svg.selectAll('circle').call(drag);
```

**Event Properties**:
- `event.x`, `event.y`: New position
- `event.dx`, `event.dy`: Change from last position
- `event.subject`: Bound datum

---

### Drag with Constraints

```javascript
function dragged(event, d) {
  d3.select(this)
    .attr('cx', Math.max(0, Math.min(width, event.x)))
    .attr('cy', Math.max(0, Math.min(height, event.y)));
}
```

---

## Zoom and Pan

### Basic Zoom

```javascript
const zoom = d3.zoom()
  .scaleExtent([0.5, 5])          // Min/max zoom
  .on('zoom', zoomed);

function zoomed(event) {
  g.attr('transform', event.transform);
}

svg.call(zoom);

// Container for zoomable content
const g = svg.append('g');
g.selectAll('circle').data(data).join('circle')...
```

**Key**: Apply transform to container group, not individual elements.

---

### Programmatic Zoom

```javascript
// Zoom to specific level
svg.transition()
  .duration(750)
  .call(zoom.transform, d3.zoomIdentity.scale(2));

// Zoom to fit
svg.transition()
  .duration(750)
  .call(zoom.transform, d3.zoomIdentity.translate(100, 100).scale(1.5));
```

---

### Zoom with Constraints

```javascript
const zoom = d3.zoom()
  .scaleExtent([0.5, 5])
  .translateExtent([[0, 0], [width, height]])  // Pan limits
  .on('zoom', zoomed);
```

---

## Brush Selection

### 2D Brush

```javascript
const brush = d3.brush()
  .extent([[0, 0], [width, height]])
  .on('end', brushended);

function brushended(event) {
  if (!event.selection) return;  // No selection
  const [[x0, y0], [x1, y1]] = event.selection;

  // Filter data
  const selected = data.filter(d => {
    const x = xScale(d.x), y = yScale(d.y);
    return x >= x0 && x <= x1 && y >= y0 && y <= y1;
  });

  console.log('Selected', selected);
}

svg.append('g').attr('class', 'brush').call(brush);
```

---

### 1D Brush

```javascript
// X-axis only
const brushX = d3.brushX()
  .extent([[0, 0], [width, height]])
  .on('end', brushended);

// Y-axis only
const brushY = d3.brushY()
  .extent([[0, 0], [width, height]])
  .on('end', brushended);
```

---

### Clear Brush

```javascript
svg.select('.brush').call(brush.move, null);  // Clear selection
```

---

### Programmatic Brush

```javascript
// Set selection programmatically
svg.select('.brush').call(brush.move, [[100, 100], [200, 200]]);
```

---

## Common Pitfalls

### Pitfall 1: Transition on Initial Render

```javascript
// WRONG - transition when no previous state
svg.selectAll('circle').data(data).join('circle').transition().attr('r', 5);

// CORRECT - transition only on updates
const circles = svg.selectAll('circle').data(data).join('circle').attr('r', 5);
circles.transition().attr('r', 10);  // Later, on update
```

---

### Pitfall 2: Not Using Key Function

```javascript
// WRONG - elements don't track data items
.data(newData).join('circle').transition().attr('cx', d => xScale(d.x));

// CORRECT - use key function
.data(newData, d => d.id).join('circle').transition().attr('cx', d => xScale(d.x));
```

---

### Pitfall 3: Applying Zoom to Wrong Element

```javascript
// WRONG - zoom affects individual elements
svg.selectAll('circle').call(zoom);

// CORRECT - zoom affects container
const g = svg.append('g');
svg.call(zoom);
g.selectAll('circle')...  // Elements in zoomable container
```

---

## Next Steps

- Apply to workflows: [Workflows](workflows.md)
- See complete examples: [Common Patterns](common-patterns.md)
- Combine with layouts: [Advanced Layouts](advanced-layouts.md)
