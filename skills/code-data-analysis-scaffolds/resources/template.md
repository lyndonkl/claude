# Code Data Analysis Scaffolds Template

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

**Step 1: Clarify task** - Ask context questions to understand task type, constraints, expected outcomes. See [Context Questions](#context-questions).

**Step 2: Choose scaffold** - Select TDD, EDA, Statistical Analysis, or Validation based on task. See [Scaffold Selection Guide](#scaffold-selection-guide).

**Step 3: Generate structure** - Use appropriate scaffold template. See [TDD Scaffold](#tdd-scaffold), [EDA Scaffold](#eda-scaffold), [Statistical Analysis Scaffold](#statistical-analysis-scaffold), or [Validation Scaffold](#validation-scaffold).

**Step 4: Validate completeness** - Check scaffold covers requirements, includes validation steps, makes assumptions explicit. See [Quality Checklist](#quality-checklist).

**Step 5: Deliver and guide** - Present scaffold, highlight next steps, surface any gaps discovered. Execute if user wants help.

## Context Questions

**For all tasks:**
- What are you trying to accomplish? (Specific outcome expected)
- What's the context? (Dataset characteristics, codebase state, existing work)
- Any constraints? (Time, tools, data limitations, performance requirements)
- What does success look like? (Acceptance criteria, quality bar)

**For TDD tasks:**
- What functionality needs tests? (Feature, bug fix, refactor)
- Existing test coverage? (None, partial, comprehensive)
- Test framework preference? (pytest, jest, junit, etc.)
- Integration vs unit tests? (Scope of testing)

**For EDA tasks:**
- What's the dataset? (Size, format, source)
- What questions are you trying to answer? (Exploratory vs. hypothesis-driven)
- Existing knowledge about data? (Schema, distributions, known issues)
- End goal? (Feature engineering, quality assessment, insights)

**For Statistical/Modeling tasks:**
- What's the research question? (Descriptive, predictive, causal)
- Available data? (Sample size, variables, treatment/control)
- Causal or predictive goal? (Understanding why vs. forecasting what)
- Significance level / acceptable error rate?

## Scaffold Selection Guide

| User Says | Task Type | Scaffold to Use |
|-----------|-----------|-----------------|
| "Write tests for..." | TDD | [TDD Scaffold](#tdd-scaffold) |
| "Explore this dataset..." | EDA | [EDA Scaffold](#eda-scaffold) |
| "Analyze the effect of..." / "Does X cause Y?" | Causal Inference | See methodology.md |
| "Predict..." / "Classify..." / "Forecast..." | Predictive Modeling | See methodology.md |
| "Design an A/B test..." / "Compare groups..." | Statistical Analysis | [Statistical Analysis Scaffold](#statistical-analysis-scaffold) |
| "Validate..." / "Check quality..." | Validation | [Validation Scaffold](#validation-scaffold) |

## TDD Scaffold

Use when writing new code, refactoring, or fixing bugs. **Write tests FIRST, then implement.**

### Quick Template

```python
# Test file: test_[module].py
import pytest
from [module] import [function_to_test]

# 1. HAPPY PATH TESTS (expected usage)
def test_[function]_with_valid_input():
    """Test normal, expected behavior"""
    result = [function](valid_input)
    assert result == expected_output
    assert result.property == expected_value

# 2. EDGE CASE TESTS (boundary conditions)
def test_[function]_with_empty_input():
    """Test with empty/minimal input"""
    result = [function]([])
    assert result == expected_for_empty

def test_[function]_with_maximum_input():
    """Test with large/maximum input"""
    result = [function](large_input)
    assert result is not None

# 3. ERROR CONDITION TESTS (invalid input, expected failures)
def test_[function]_with_invalid_input():
    """Test proper error handling"""
    with pytest.raises(ValueError):
        [function](invalid_input)

def test_[function]_with_none_input():
    """Test None handling"""
    with pytest.raises(TypeError):
        [function](None)

# 4. STATE TESTS (if function modifies state)
def test_[function]_modifies_state_correctly():
    """Test side effects are correct"""
    obj = Object()
    obj.[function](param)
    assert obj.state == expected_state

# 5. INTEGRATION TESTS (if interacting with external systems)
@pytest.fixture
def mock_external_service():
    """Mock external dependencies"""
    return Mock(spec=ExternalService)

def test_[function]_with_external_service(mock_external_service):
    """Test integration points"""
    result = [function](mock_external_service)
    mock_external_service.method.assert_called_once()
    assert result == expected_from_integration
```

### Test Data Setup

```python
# conftest.py or test fixtures
@pytest.fixture
def sample_data():
    """Reusable test data"""
    return {
        "valid": [...],
        "edge_case": [...],
        "invalid": [...]
    }

@pytest.fixture(scope="session")
def database_session():
    """Database for integration tests"""
    db = create_test_db()
    yield db
    db.cleanup()
```

### TDD Cycle

1. **Red**: Write failing test (defines what success looks like)
2. **Green**: Write minimal code to make test pass
3. **Refactor**: Improve code while keeping tests green
4. **Repeat**: Next test case

## EDA Scaffold

Use when exploring new dataset. Follow systematic plan to understand data quality and patterns.

### Quick Template

```python
# 1. DATA OVERVIEW
# Load and inspect
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_[format]('data.csv')

# Basic info
print(f"Shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
print(df.dtypes)
print(df.head())
print(df.info())
print(df.describe())

# 2. DATA QUALITY CHECKS
# Missing values
missing = df.isnull().sum()
missing_pct = (missing / len(df)) * 100
print(missing_pct[missing_pct > 0])

# Duplicates
print(f"Duplicates: {df.duplicated().sum()}")

# Data types consistency
print("Check: Are numeric columns actually numeric?")
print("Check: Are dates parsed correctly?")
print("Check: Are categorical variables encoded properly?")

# 3. UNIVARIATE ANALYSIS
# Numeric: mean, median, std, range, distribution plots, outliers (IQR method)
for col in df.select_dtypes(include=[np.number]).columns:
    print(f"{col}: mean={df[col].mean():.2f}, median={df[col].median():.2f}, std={df[col].std():.2f}")
    df[col].hist(bins=50); plt.title(f'{col} Distribution'); plt.show()
    Q1, Q3 = df[col].quantile([0.25, 0.75])
    outliers = ((df[col] < (Q1 - 1.5*(Q3-Q1))) | (df[col] > (Q3 + 1.5*(Q3-Q1)))).sum()
    print(f"  Outliers: {outliers} ({outliers/len(df)*100:.1f}%)")

# Categorical: value counts, unique values, bar plots
for col in df.select_dtypes(include=['object', 'category']).columns:
    print(f"{col}: {df[col].nunique()} unique, most common={df[col].mode()[0]}")
    df[col].value_counts().head(10).plot(kind='bar'); plt.show()

# 4. BIVARIATE ANALYSIS
# Correlation heatmap, pairplots, categorical vs numeric boxplots
sns.heatmap(df.select_dtypes(include=[np.number]).corr(), annot=True, cmap='coolwarm')
sns.pairplot(df[['var1', 'var2', 'var3', 'target']], hue='target'); plt.show()
# For each categorical-numeric pair, create boxplots to see distributions

# 5. INSIGHTS & NEXT STEPS
print("\n=== KEY FINDINGS ===")
print("1. Data quality: [summary]")
print("2. Distributions: [any skewness, outliers]")
print("3. Correlations: [strong relationships found]")
print("4. Missing patterns: [systematic missingness?]")
print("\n=== RECOMMENDED ACTIONS ===")
print("1. Handle missing data: [imputation strategy]")
print("2. Address outliers: [cap, remove, transform]")
print("3. Feature engineering: [ideas based on EDA]")
print("4. Data transformations: [log, standardize, encode]")
```

### EDA Checklist

- [ ] Load data and check shape/dtypes
- [ ] Assess missing values (how much, which variables, patterns?)
- [ ] Check for duplicates
- [ ] Validate data types (numeric, categorical, dates)
- [ ] Univariate analysis (distributions, outliers, summary stats)
- [ ] Bivariate analysis (correlations, relationships with target)
- [ ] Identify data quality issues
- [ ] Document insights and recommended next steps

## Statistical Analysis Scaffold

Use for hypothesis testing, A/B tests, comparing groups.

### Quick Template

```python
# STATISTICAL ANALYSIS SCAFFOLD

# 1. DEFINE RESEARCH QUESTION
question = "Does treatment X improve outcome Y?"

# 2. STATE HYPOTHESES
H0 = "Treatment X has no effect on outcome Y (null hypothesis)"
H1 = "Treatment X improves outcome Y (alternative hypothesis)"

# 3. SET SIGNIFICANCE LEVEL
alpha = 0.05  # 5% significance level (Type I error rate)
power = 0.80  # 80% power (1 - Type II error rate)

# 4. CHECK ASSUMPTIONS (t-test: independence, normality, equal variance)
from scipy import stats
_, p_norm = stats.shapiro(treatment_group)  # Normality test
_, p_var = stats.levene(treatment_group, control_group)  # Equal variance test
print(f"Normality: p={p_norm:.3f} {'✓' if p_norm > 0.05 else '✗ use non-parametric'}")
print(f"Equal variance: p={p_var:.3f} {'✓' if p_var > 0.05 else '✗ use Welch t-test'}")

# 5. PERFORM STATISTICAL TEST
# Choose appropriate test based on data type and assumptions

# For continuous outcome, 2 groups:
statistic, p_value = stats.ttest_ind(treatment_group, control_group)
print(f"t-statistic: {statistic:.3f}, p-value: {p_value:.4f}")

# For categorical outcome, 2 groups:
from scipy.stats import chi2_contingency
contingency_table = pd.crosstab(df['group'], df['outcome'])
chi2, p_value, dof, expected = chi2_contingency(contingency_table)
print(f"Chi-square: {chi2:.3f}, p-value: {p_value:.4f}")

# 6. INTERPRET RESULTS & EFFECT SIZE
if p_value < alpha:
    cohen_d = (treatment_group.mean() - control_group.mean()) / pooled_std
    effect = "Small" if abs(cohen_d) < 0.2 else "Medium" if abs(cohen_d) < 0.5 else "Large"
    print(f"REJECT H0 (p={p_value:.4f}). Effect size (Cohen's d)={cohen_d:.3f} ({effect})")
else:
    print(f"FAIL TO REJECT H0 (p={p_value:.4f}). Insufficient evidence for effect.")

# 7. CONFIDENCE INTERVAL & SENSITIVITY
ci_95 = stats.t.interval(0.95, len(treatment_group)-1, loc=treatment_group.mean(), scale=stats.sem(treatment_group))
print(f"95% CI: [{ci_95[0]:.2f}, {ci_95[1]:.2f}]")
print("Sensitivity: Check without outliers, with non-parametric test, with confounders")
```

### Statistical Test Selection

| Data Type | # Groups | Test |
|-----------|----------|------|
| Continuous | 2 | t-test (or Welch's if unequal variance) |
| Continuous | 3+ | ANOVA (or Kruskal-Wallis if non-normal) |
| Categorical | 2 | Chi-square or Fisher's exact |
| Ordinal | 2 | Mann-Whitney U |
| Paired/Repeated | 2 | Paired t-test or Wilcoxon signed-rank |

## Validation Scaffold

Use for validating data quality, code quality, or model quality before shipping.

### Data Validation Template

```python
# DATA VALIDATION CHECKLIST

# 1. SCHEMA VALIDATION
expected_columns = ['id', 'timestamp', 'value', 'category']
assert set(df.columns) == set(expected_columns), "Column mismatch"

expected_dtypes = {'id': 'int64', 'timestamp': 'datetime64', 'value': 'float64', 'category': 'object'}
for col, dtype in expected_dtypes.items():
    assert df[col].dtype == dtype, f"{col} type mismatch: expected {dtype}, got {df[col].dtype}"

# 2. RANGE VALIDATION
assert df['value'].min() >= 0, "Negative values found (should be >= 0)"
assert df['value'].max() <= 100, "Values exceed maximum (should be <= 100)"

# 3. UNIQUENESS VALIDATION
assert df['id'].is_unique, "Duplicate IDs found"

# 4. COMPLETENESS VALIDATION
required_fields = ['id', 'value']
for field in required_fields:
    missing_pct = df[field].isnull().mean() * 100
    assert missing_pct == 0, f"{field} has {missing_pct:.1f}% missing (required field)"

# 5. CONSISTENCY VALIDATION
assert (df['start_date'] <= df['end_date']).all(), "start_date after end_date found"

# 6. REFERENTIAL INTEGRITY
valid_categories = ['A', 'B', 'C']
assert df['category'].isin(valid_categories).all(), "Invalid categories found"

print("✓ All data validations passed")
```

### Code Validation Checklist

- [ ] **Unit tests**: All functions have tests covering happy path, edge cases, errors
- [ ] **Integration tests**: APIs, database interactions tested end-to-end
- [ ] **Test coverage**: ≥80% coverage for critical paths
- [ ] **Error handling**: All exceptions caught and handled gracefully
- [ ] **Input validation**: All user inputs validated before processing
- [ ] **Logging**: Key operations logged for debugging
- [ ] **Documentation**: Functions have docstrings, README updated
- [ ] **Performance**: No obvious performance bottlenecks (profiled if needed)
- [ ] **Security**: No hardcoded secrets, SQL injection protected, XSS prevented

### Model Validation Checklist

- [ ] **Train/val/test split**: Data split before any preprocessing (no data leakage)
- [ ] **Baseline model**: Simple baseline implemented for comparison
- [ ] **Cross-validation**: k-fold CV performed (k≥5)
- [ ] **Metrics**: Appropriate metrics chosen (accuracy, precision/recall, AUC, RMSE, etc.)
- [ ] **Overfitting check**: Training vs validation performance compared
- [ ] **Error analysis**: Failure modes analyzed, edge cases identified
- [ ] **Fairness**: Model checked for bias across sensitive groups
- [ ] **Interpretability**: Feature importance or SHAP values computed
- [ ] **Robustness**: Model tested with perturbed inputs
- [ ] **Monitoring**: Drift detection and performance tracking in place

## Quality Checklist

Before delivering, verify:

**Scaffold Structure:**
- [ ] Clear step-by-step process defined
- [ ] Each step has concrete actions (not vague advice)
- [ ] Validation checkpoints included
- [ ] Expected outputs specified

**Completeness:**
- [ ] Covers all requirements from user's task
- [ ] Includes example code/pseudocode where helpful
- [ ] Anticipates edge cases and error conditions
- [ ] Provides decision guidance (when to use which approach)

**Clarity:**
- [ ] Assumptions stated explicitly
- [ ] Technical terms defined or illustrated
- [ ] Success criteria clear
- [ ] Next steps obvious

**Actionability:**
- [ ] User can execute scaffold without further guidance
- [ ] Code snippets are runnable (or nearly runnable)
- [ ] Gaps surfaced early (missing data, unclear requirements)
- [ ] Includes validation/quality checks

**Rubric Score:**
- [ ] Self-assessed with rubric ≥ 3.5 average
