---
name: code-data-analysis-scaffolds
description: Generates structured scaffolds (frameworks, checklists, templates) for technical work — TDD test suites, exploratory data analysis plans, statistical analysis designs, causal vs predictive modeling objectives, and validation checklists. Use when starting technical work that needs systematic planning before execution. Invoke when user mentions "write tests for", "explore this dataset", "analyze", "model", "validate", "design an A/B test", or when technical work needs scaffolding before execution.
---
# Code Data Analysis Scaffolds

## Table of Contents
- [Overview](#overview)
- [Workflow](#workflow)
- [Scaffold Types](#scaffold-types)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Overview

This skill provides structured scaffolds for common technical patterns:

1. **TDD Scaffold**: Given requirements, generate test structure before implementing code
2. **EDA Scaffold**: Given dataset, create systematic exploration plan
3. **Statistical Analysis Scaffold**: Given question, design appropriate statistical test/model
4. **Validation Scaffold**: Given code/model/data, create comprehensive validation checklist

**Skip this skill** when the user wants immediate execution without scaffolding, already has a clear plan, or the task is trivial.

**Quick example:**

> **Task**: "Write authentication function"
>
> **TDD Scaffold**:
> ```python
> # Test structure (write these FIRST)
> def test_valid_credentials():
>     assert authenticate("user@example.com", "correct_pass") == True
>
> def test_invalid_password():
>     assert authenticate("user@example.com", "wrong_pass") == False
>
> def test_nonexistent_user():
>     assert authenticate("nobody@example.com", "any_pass") == False
>
> def test_empty_credentials():
>     with pytest.raises(ValueError):
>         authenticate("", "")
>
> # Now implement authenticate() to make tests pass
> ```

## Workflow

Copy this checklist and track your progress:

```
Code Data Analysis Scaffolds Progress:
- [ ] Step 1: Clarify task and objectives
- [ ] Step 2: Choose appropriate scaffold type
- [ ] Step 3: Generate scaffold structure
- [ ] Step 4: Validate scaffold completeness
- [ ] Step 5: Deliver scaffold and guide execution
```

**Step 1: Clarify task and objectives**

Ask user for the task, dataset/codebase context, constraints, and expected outcome. Determine if this is TDD (write tests first), EDA (explore data), statistical analysis (test hypothesis), or validation (check quality). See [resources/template.md](resources/template.md) for context questions.

**Step 2: Choose appropriate scaffold type**

Based on task, select scaffold: TDD (testing code), EDA (exploring data), Statistical Analysis (hypothesis testing, A/B tests), Causal Inference (estimating treatment effects), Predictive Modeling (building ML models), or Validation (checking quality). See [Scaffold Types](#scaffold-types) for guidance on choosing.

**Step 3: Generate scaffold structure**

Create systematic framework with clear steps, validation checkpoints, and expected outputs at each stage. For standard cases use [resources/template.md](resources/template.md); for advanced techniques see [resources/methodology.md](resources/methodology.md).

**Step 4: Validate scaffold completeness**

Check scaffold covers all requirements, includes validation steps, makes assumptions explicit, and provides clear success criteria. Self-assess using [resources/evaluators/rubric_code_data_analysis_scaffolds.json](resources/evaluators/rubric_code_data_analysis_scaffolds.json) - minimum score ≥3.5.

**Step 5: Deliver scaffold and guide execution**

Present scaffold with clear next steps. If user wants execution help, follow the scaffold systematically. If scaffold reveals gaps (missing data, unclear requirements), surface these before proceeding.

## Scaffold Types

### TDD (Test-Driven Development)
**When**: Writing new code, refactoring existing code, fixing bugs
**Output**: Test structure (test cases → implementation → refactor)
**Key Elements**: Test cases covering happy path, edge cases, error conditions, test data setup

### EDA (Exploratory Data Analysis)
**When**: New dataset, data quality questions, feature engineering
**Output**: Exploration plan (data overview → quality checks → univariate → bivariate → insights)
**Key Elements**: Data shape/types, missing values, distributions, outliers, correlations

### Statistical Analysis
**When**: Hypothesis testing, A/B testing, comparing groups
**Output**: Analysis design (question → hypothesis → test selection → assumptions → interpretation)
**Key Elements**: Null/alternative hypotheses, significance level, power analysis, assumption checks

### Causal Inference
**When**: Estimating treatment effects, understanding causation not just correlation
**Output**: Causal design (DAG → identification strategy → estimation → sensitivity analysis)
**Key Elements**: Confounders, treatment/control groups, identification assumptions, effect estimation

### Predictive Modeling
**When**: Building ML models, forecasting, classification/regression tasks
**Output**: Modeling pipeline (data prep → feature engineering → model selection → validation → evaluation)
**Key Elements**: Train/val/test split, baseline model, metrics selection, cross-validation, error analysis

### Validation
**When**: Checking data quality, code quality, model quality before deployment
**Output**: Validation checklist (assertions → edge cases → integration tests → monitoring)
**Key Elements**: Acceptance criteria, test coverage, error handling, boundary conditions

## Guardrails

- **Clarify before scaffolding** - Don't guess what user needs; ask clarifying questions first
- **Distinguish causal vs predictive** - Causal inference needs different methods than prediction (RCT/IV vs ML)
- **Make assumptions explicit** - Every scaffold has assumptions (data distribution, user behavior, system constraints)
- **Include validation steps** - Scaffold should include checkpoints to validate work at each stage
- **Provide examples** - Show what good looks like (sample test, sample EDA visualization, sample model evaluation)
- **Surface gaps early** - If scaffold reveals missing data/requirements, flag immediately
- **Avoid premature optimization** - Start with simple scaffold, add complexity only if needed
- **Follow best practices** - TDD: test first, EDA: start with data quality, Modeling: baseline before complex models

## Quick Reference

| Task Type | When to Use | Scaffold Resource |
|-----------|-------------|-------------------|
| **TDD** | Writing/refactoring code | [resources/template.md](resources/template.md) #tdd-scaffold |
| **EDA** | Exploring new dataset | [resources/template.md](resources/template.md) #eda-scaffold |
| **Statistical Analysis** | Hypothesis testing, A/B tests | [resources/template.md](resources/template.md) #statistical-analysis-scaffold |
| **Causal Inference** | Treatment effect estimation | [resources/methodology.md](resources/methodology.md) #causal-inference-methods |
| **Predictive Modeling** | ML model building | [resources/methodology.md](resources/methodology.md) #predictive-modeling-pipeline |
| **Validation** | Quality checks before shipping | [resources/template.md](resources/template.md) #validation-scaffold |
| **Examples** | See what good looks like | [resources/examples/](resources/examples/) |
| **Rubric** | Validate scaffold quality | [resources/evaluators/rubric_code_data_analysis_scaffolds.json](resources/evaluators/rubric_code_data_analysis_scaffolds.json) |
