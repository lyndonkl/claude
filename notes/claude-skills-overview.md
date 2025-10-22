# Claude Agent Skills - Comprehensive Guide

## What are Agent Skills?

Agent skills are modular, reusable capabilities that extend Claude's functionality for specific tasks. They are essentially:

- **Specialized prompts** with optional supporting code/tools
- **Composable units** that can be combined to solve complex problems
- **Domain-specific knowledge** packaged in a reusable format

## Core Components of a Skill

### 1. Skill Definition (Prompt)
- Clear description of what the skill does
- Step-by-step instructions for the agent
- Expected inputs and outputs
- Success criteria

### 2. Supporting Resources (Optional)
- Scripts or executables
- Configuration files
- Reference documentation
- Example data

### 3. Tool Access
- Skills can leverage built-in tools (file operations, bash, etc.)
- Custom tools specific to the skill's domain

## Best Practices for Defining Skills

### 1. Clear Scope and Purpose
- Define a single, well-scoped responsibility
- Make the skill's objective explicit
- Include when to use (and when NOT to use) the skill
- Avoid feature creep - keep skills focused

### 2. Structured Instructions
- Use step-by-step workflows
- Include decision points and conditionals
- Provide examples of expected behavior
- Use clear, imperative language
- Number steps for clarity

### 3. Layering Information

Skills should layer information from most to least important:

#### a) Core Instructions (Essential)
- The primary steps required to complete the task
- Must be clear and unambiguous
- Should be executable without additional context

#### b) Context (Background Knowledge)
- Domain knowledge required to understand the task
- Terminology definitions
- Relevant concepts and principles
- Links to external documentation

#### c) Examples (Concrete Demonstrations)
- Show, don't just tell
- Include both simple and complex cases
- Cover common use cases
- Demonstrate expected output format

#### d) Edge Cases (Unusual Situations)
- Handle boundary conditions
- Address potential errors
- Define behavior for unexpected inputs
- Specify fallback strategies

#### e) Constraints (Limitations and Boundaries)
- What the skill should NOT do
- Performance limitations
- Required permissions or access
- Dependencies

### 4. Error Handling
- Define failure modes
- Specify recovery strategies
- Include validation steps
- Provide clear error messages
- Define rollback procedures

## Skill Structure Template

```markdown
# Skill Name

## Purpose
[What this skill does and when to use it]

## When to Use
- [Scenario 1]
- [Scenario 2]

## When NOT to Use
- [Anti-pattern 1]
- [Anti-pattern 2]

## Prerequisites
[Required tools, access, or context]

## Instructions

### Phase 1: [Planning/Setup]
1. [Step 1]
2. [Step 2]
   - [Sub-step if needed]

### Phase 2: [Execution]
1. [Step 1]
2. [Step 2]

### Phase 3: [Validation]
1. [Verification step 1]
2. [Verification step 2]

## Validation
[How to verify success]

## Examples

### Example 1: [Simple Case]
Input:
```
[example input]
```

Output:
```
[expected output]
```

### Example 2: [Complex Case]
[More detailed example]

## Edge Cases
- **Case 1**: [How to handle]
- **Case 2**: [How to handle]

## Troubleshooting
| Issue | Solution |
|-------|----------|
| [Problem 1] | [Resolution 1] |
| [Problem 2] | [Resolution 2] |

## Constraints
- [Limitation 1]
- [Limitation 2]
```

## Creating Workflows

For complex multi-step processes:

### 1. Break Down into Phases
- **Planning phase**: Gather requirements, assess feasibility
- **Execution phase**: Perform the actual work
- **Validation phase**: Verify success, test results

### 2. Define Checkpoints
- Clear milestones
- Validation at each step
- Rollback procedures if needed
- Progress tracking

### 3. State Management
- Track progress through the workflow
- Handle interruptions gracefully
- Resume capability for long-running tasks
- Save intermediate results

### 4. Workflow Template

```markdown
## Workflow: [Workflow Name]

### Overview
[Brief description of the end-to-end process]

### Phases

#### 1. Planning
- [ ] Task 1
- [ ] Task 2
**Checkpoint**: [What to verify before proceeding]

#### 2. Execution
- [ ] Task 1
- [ ] Task 2
**Checkpoint**: [What to verify before proceeding]

#### 3. Validation
- [ ] Task 1
- [ ] Task 2
**Checkpoint**: [Final verification]

### Rollback Procedures
If Phase X fails:
1. [Rollback step 1]
2. [Rollback step 2]
```

## Scripts and Automation

When skills include scripts:

### 1. Keep Scripts Focused
- One clear purpose per script
- Single Responsibility Principle
- Avoid monolithic scripts

### 2. Document Thoroughly
- Header comments with purpose, usage, and examples
- Inline comments for complex logic
- Usage instructions
- Parameter descriptions
- Example invocations

### 3. Handle Errors Gracefully
- Use proper exit codes (0 for success, non-zero for failure)
- Provide meaningful error messages
- Log errors appropriately
- Clean up resources on failure

### 4. Make Them Portable
- Minimize dependencies
- Document required dependencies clearly
- Use virtual environments for language-specific tools
- Check for prerequisites before execution
- Support multiple platforms when possible

### 5. Script Template

```bash
#!/bin/bash
# Script Name: script-name.sh
# Purpose: [What this script does]
# Usage: ./script-name.sh [args]
# Example: ./script-name.sh input.txt output.txt
# Dependencies: [list required tools/packages]

set -euo pipefail  # Exit on error, undefined vars, pipe failures

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Functions
function error_exit() {
    echo "ERROR: $1" >&2
    exit 1
}

function main() {
    # Validate prerequisites
    command -v required_tool >/dev/null 2>&1 || error_exit "required_tool not found"

    # Main logic here

    # Clean exit
    exit 0
}

main "$@"
```

## Key Design Principles

### 1. Modularity
- Skills should be self-contained
- Minimal dependencies on other skills
- Clear interfaces and boundaries
- Easy to understand in isolation

### 2. Composability
- Skills should work well together
- Output of one skill can be input to another
- Consistent formatting and conventions
- Avoid conflicting assumptions

### 3. Clarity
- Instructions should be unambiguous
- Use precise language
- Avoid jargon unless defined
- Prefer explicit over implicit

### 4. Robustness
- Handle edge cases and errors
- Validate inputs
- Provide helpful error messages
- Degrade gracefully when possible

### 5. Testability
- Define clear success/failure criteria
- Include validation steps
- Provide test cases or examples
- Make verification easy

### 6. Maintainability
- Use clear naming conventions
- Document assumptions
- Keep skills up to date
- Version control skill definitions

## Advanced Concepts

### Skill Composition

Skills can be composed to create more complex behaviors:

1. **Sequential Composition**: Execute skills in order
   - Skill A → Skill B → Skill C
   - Output of each feeds into the next

2. **Conditional Composition**: Branch based on results
   - If Skill A succeeds → Skill B
   - If Skill A fails → Skill C

3. **Parallel Composition**: Execute multiple skills concurrently
   - Skill A, Skill B, and Skill C run in parallel
   - Aggregate results when all complete

### Context Management

Skills need to manage context effectively:

- **Required Context**: What information must be provided
- **Optional Context**: What information enhances performance
- **Context Validation**: Verify context is sufficient
- **Context Propagation**: Pass context between composed skills

### Performance Considerations

- **Scope Appropriately**: Don't make skills too broad or too narrow
- **Minimize Tool Calls**: Batch operations when possible
- **Cache Results**: Reuse results from expensive operations
- **Fail Fast**: Validate early to avoid wasted work

## Common Patterns

### 1. Analysis Pattern
```
1. Gather relevant data
2. Process/analyze data
3. Generate insights
4. Present findings
```

### 2. Transform Pattern
```
1. Validate input
2. Transform data
3. Validate output
4. Return result
```

### 3. Search Pattern
```
1. Define search criteria
2. Execute search
3. Filter results
4. Rank/sort results
5. Return top matches
```

### 4. Generate Pattern
```
1. Understand requirements
2. Plan structure
3. Generate content
4. Validate against requirements
5. Refine if needed
```

## Testing Skills

### Unit Testing
- Test individual components
- Mock dependencies
- Verify expected outputs
- Test edge cases

### Integration Testing
- Test skill composition
- Verify end-to-end workflows
- Test with real dependencies
- Validate complete scenarios

### Validation Checklist
- [ ] Skill has clear purpose
- [ ] Instructions are step-by-step
- [ ] Examples are provided
- [ ] Edge cases are handled
- [ ] Error handling is defined
- [ ] Success criteria are clear
- [ ] Prerequisites are documented
- [ ] Constraints are specified

## Resources and References

### Documentation Structure
```
skill-name/
├── README.md           # Main skill definition
├── examples/          # Example inputs/outputs
│   ├── example1.md
│   └── example2.md
├── scripts/           # Supporting scripts
│   ├── helper1.sh
│   └── helper2.py
├── docs/              # Additional documentation
│   ├── architecture.md
│   └── troubleshooting.md
└── tests/             # Test cases
    ├── test1.md
    └── test2.md
```

## Next Steps

To build effective skills:

1. **Start Small**: Begin with a focused, well-scoped skill
2. **Iterate**: Test and refine based on real usage
3. **Document**: Keep documentation up to date
4. **Compose**: Build more complex skills from proven components
5. **Share**: Create reusable skills for common tasks

## Common Pitfalls to Avoid

1. **Over-complication**: Keep skills as simple as possible
2. **Insufficient examples**: Always include concrete examples
3. **Vague instructions**: Be explicit and specific
4. **Missing error handling**: Always consider what can go wrong
5. **Lack of validation**: Include success verification steps
6. **Poor naming**: Use descriptive, clear names
7. **Scope creep**: Resist adding unrelated functionality
8. **Inadequate testing**: Validate skills thoroughly before deployment
