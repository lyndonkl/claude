# Selections & Data Joins

## Why Data Joins Matter

**The Problem**: Manually creating, updating, and removing DOM elements for dynamic data is error-prone. You must track which elements correspond to which data items, handle array length changes, and avoid orphaned elements.

**D3's Solution**: Data joins establish declarative one-to-one correspondence between data arrays and DOM elements. Specify desired end state; D3 handles lifecycle automatically.

**Key Principle**: "Join data to elements, then manipulate elements using data." Changes to data propagate to visuals through re-joining.

---

## Selections Fundamentals

### Creating Selections

```javascript
// Select first matching element
const svg = d3.select('svg');
const firstCircle = d3.select('circle');

// Select all matching elements
const allCircles = d3.selectAll('circle');
const allRects = d3.selectAll('rect');

// CSS selectors supported
const blueCircles = d3.selectAll('circle.blue');
const chartGroup = d3.select('#chart');
```

**Key Methods**:
- `select(selector)`: Returns selection with first match
- `selectAll(selector)`: Returns selection with all matches
- Empty selection if no matches (not null)

---

### Modifying Elements

```javascript
// Set attributes
selection.attr('r', 10);              // Set radius to 10
selection.attr('fill', 'steelblue');  // Set fill color

// Set styles
selection.style('opacity', 0.7);
selection.style('stroke-width', '2px');

// Set classes
selection.classed('active', true);    // Add class
selection.classed('hidden', false);   // Remove class

// Set text
selection.text('Label');

// Set HTML
selection.html('<strong>Bold</strong>');

// Set properties (DOM properties, not attributes)
selection.property('checked', true);  // For checkboxes, etc.
```

**Attribute vs Style**:
- Use `.attr()` for SVG attributes: `x`, `y`, `r`, `fill`, `stroke`
- Use `.style()` for CSS properties: `opacity`, `font-size`, `color`

---

### Creating and Removing Elements

```javascript
// Append child element
const g = svg.append('g');           // Returns new selection
g.attr('transform', 'translate(50, 50)');

// Insert before sibling
svg.insert('rect', 'circle');        // Insert rect before first circle

// Remove elements
selection.remove();                   // Delete from DOM
```

---

### Method Chaining

All modification methods return the selection, enabling chains:

```javascript
d3.select('svg')
  .append('circle')
  .attr('cx', 100)
  .attr('cy', 100)
  .attr('r', 50)
  .attr('fill', 'steelblue')
  .style('opacity', 0.7)
  .on('click', handleClick);
```

**Why Chaining Works**: Methods mutate selection and return it.

---

## Data Join Pattern

### Basic Join

```javascript
const data = [10, 20, 30, 40, 50];

svg.selectAll('circle')      // Select all circles (may be empty)
  .data(data)                // Bind data array
  .join('circle')            // Create/update/remove to match data
    .attr('r', d => d);      // Set attributes using data
```

**What `.join()` Does**:
1. **Enter**: Creates `<circle>` elements for data items without elements (5 circles created if none exist)
2. **Update**: Updates existing circles if some already exist
3. **Exit**: Removes circles if data shrinks (e.g., data becomes `[10, 20]`, 3 circles removed)

---

### Accessor Functions

Pass functions to `.attr()` and `.style()` receiving `(datum, index)` parameters:

```javascript
.attr('cx', (d, i) => i * 50 + 25)  // d = data value, i = index
.attr('cy', 100)                    // Static value
.attr('r', d => d)                  // Radius = data value
```

**Pattern**: `(d, i) => expression`
- `d`: Datum (current array element)
- `i`: Index in array (0-based)

---

### Data with Objects

```javascript
const data = [
  {name: 'A', value: 30, color: 'red'},
  {name: 'B', value: 80, color: 'blue'},
  {name: 'C', value: 45, color: 'green'}
];

svg.selectAll('circle')
  .data(data)
  .join('circle')
    .attr('r', d => d.value)       // Access object properties
    .attr('fill', d => d.color);
```

---

## Enter, Exit, Update Pattern

For fine-grained control (especially with custom transitions):

```javascript
svg.selectAll('circle')
  .data(data)
  .join(
    // Enter: new elements
    enter => enter.append('circle')
      .attr('r', 0)                 // Start small
      .call(enter => enter.transition().attr('r', d => d.value)),

    // Update: existing elements
    update => update
      .call(update => update.transition().attr('r', d => d.value)),

    // Exit: removing elements
    exit => exit
      .call(exit => exit.transition().attr('r', 0).remove())
  );
```

**When to Use**:
- Custom enter animations (fade in, slide in)
- Custom exit animations (fade out, fall down)
- Different behavior for enter vs update

**When NOT Needed**: Simple updates use `.join('circle').transition()...` after join.

---

## Key Functions (Object Constancy)

**Problem**: By default, data join matches by index. If data reorders, elements don't track items correctly.

```javascript
// Without key function
const data1 = [{id: 'A', value: 30}, {id: 'B', value: 80}];
const data2 = [{id: 'B', value: 90}, {id: 'A', value: 40}];  // Reordered!

// Element 0 bound to A (30), then B (90) - wrong!
// Element 1 bound to B (80), then A (40) - wrong!
```

**Solution**: Key function returns unique identifier:

```javascript
svg.selectAll('circle')
  .data(data, d => d.id)            // Key function
  .join('circle')
    .attr('r', d => d.value);

// Now element tracks data item by ID, not position
```

**Key Function Signature**: `(datum) => uniqueIdentifier`

**When to Use**:
- Data array reorders
- Data array filters (items removed/added)
- Transitions where element identity matters

---

## Updating Scales

When data changes, update scale domains:

```javascript
function update(newData) {
  // Recalculate domain
  yScale.domain([0, d3.max(newData, d => d.value)]);

  // Update axis
  svg.select('.y-axis')
    .transition()
    .duration(500)
    .call(d3.axisLeft(yScale));

  // Update bars
  svg.selectAll('rect')
    .data(newData, d => d.id)       // Key function
    .join('rect')
    .transition()
    .duration(500)
      .attr('y', d => yScale(d.value))
      .attr('height', d => height - yScale(d.value));
}
```

---

## Event Handling

```javascript
selection.on('click', function(event, d) {
  // `this` = DOM element
  // `event` = mouse event object
  // `d` = bound datum

  console.log('Clicked', d);
  d3.select(this).attr('fill', 'red');
});
```

**Common Events**:
- Mouse: `click`, `mouseover`, `mouseout`, `mousemove`
- Touch: `touchstart`, `touchend`, `touchmove`
- Drag: Use `d3.drag()` behavior instead
- Zoom: Use `d3.zoom()` behavior instead

**Event Object Properties**:
- `event.pageX`, `event.pageY`: Mouse position
- `event.target`: DOM element
- `event.preventDefault()`: Prevent default behavior

---

## Selection Iteration

```javascript
// Apply function to each element
selection.each(function(d, i) {
  // `this` = DOM element
  // `d` = datum
  // `i` = index
  console.log(d);
});

// Call function with selection
function styleCircles(selection) {
  selection
    .attr('stroke', 'black')
    .attr('stroke-width', 2);
}

svg.selectAll('circle').call(styleCircles);
```

**Use `.call()` for**: Reusable functions, axes, behaviors (drag, zoom).

---

## Filtering and Sorting

```javascript
// Filter selection
const largeCircles = svg.selectAll('circle')
  .filter(d => d.value > 50);

largeCircles.attr('fill', 'red');

// Sort elements in DOM
svg.selectAll('circle')
  .sort((a, b) => a.value - b.value);  // Ascending order
```

**Note**: `.sort()` reorders DOM elements, affecting document flow and rendering order.

---

## Nested Selections

```javascript
// Parent selection
const groups = svg.selectAll('g')
  .data(data)
  .join('g');

// Child selection within each group
groups.selectAll('circle')
  .data(d => [d, d, d])     // 3 circles per group
  .join('circle')
    .attr('r', 5);
```

**Pattern**: Each parent element gets its own child selection.

---

## Selection vs Element

```javascript
// Selection (D3 wrapper)
const selection = d3.select('circle');
selection.attr('r', 10);              // D3 methods

// Raw DOM element
const element = selection.node();
element.setAttribute('r', 10);        // Native DOM methods
```

**Use `.node()` to**:
- Access native DOM properties
- Use with non-D3 libraries
- Perform operations D3 doesn't support

---

## Common Patterns

### Pattern 1: Update Function

```javascript
function update(newData) {
  const circles = svg.selectAll('circle')
    .data(newData, d => d.id);

  circles.join('circle')
    .attr('cx', d => xScale(d.x))
    .attr('cy', d => yScale(d.y))
    .attr('r', 5);
}

// Call on data change
update(data);
```

---

### Pattern 2: Conditional Styling

```javascript
svg.selectAll('circle')
  .data(data)
  .join('circle')
    .attr('r', 5)
    .attr('fill', d => d.value > 50 ? 'red' : 'steelblue');
```

---

### Pattern 3: Data-Driven Classes

```javascript
svg.selectAll('rect')
  .data(data)
  .join('rect')
    .classed('high', d => d.value > 80)
    .classed('medium', d => d.value > 40 && d.value <= 80)
    .classed('low', d => d.value <= 40);
```

---

### Pattern 4: Multiple Attributes

```javascript
selection.attr('stroke', 'black').attr('stroke-width', 2).attr('fill', 'none');
```

---

## Debugging

```javascript
console.log(selection.size());       // Number of elements
console.log(selection.nodes());      // Array of DOM elements
console.log(selection.data());       // Array of bound data
```

---

## Common Pitfalls

### Pitfall 1: Forgetting to Return Accessor Value

```javascript
// WRONG - undefined attribute
.attr('r', d => { console.log(d); })

// CORRECT
.attr('r', d => {
  console.log(d);
  return d.value;  // Explicit return
})

// Or use arrow function implicit return
.attr('r', d => d.value)
```

---

### Pitfall 2: Not Using Key Function for Dynamic Data

```javascript
// WRONG - elements don't track items
.data(dynamicData)

// CORRECT
.data(dynamicData, d => d.id)
```

---

### Pitfall 3: Selecting Before Elements Exist

```javascript
// WRONG - circles don't exist yet
const circles = d3.selectAll('circle');
svg.append('circle');  // This circle not in `circles` selection

// CORRECT - select after creating
svg.append('circle');
const circles = d3.selectAll('circle');

// Or use enter selection
const circles = svg.selectAll('circle')
  .data(data)
  .join('circle');  // Creates circles, returns selection
```

---

### Pitfall 4: Modifying Selection Doesn't Update Variable

```javascript
const circles = svg.selectAll('circle');
circles.attr('fill', 'red');           // OK - modifies elements

circles.data(newData).join('circle');  // Returns NEW selection
// `circles` variable still references OLD selection

// CORRECT - reassign
circles = svg.selectAll('circle')
  .data(newData)
  .join('circle');
```

---

## Next Steps

- Learn scale functions: [Scales & Axes](scales-axes.md)
- See data join in action: [Workflows](workflows.md)
- Add transitions: [Transitions & Interactions](transitions-interactions.md)
