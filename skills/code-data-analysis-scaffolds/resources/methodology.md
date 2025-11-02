# Code Data Analysis Scaffolds Methodology

Advanced techniques for causal inference, predictive modeling, property-based testing, and complex data analysis.

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

**Step 1: Clarify task** - Assess complexity and determine if advanced techniques needed. See [1. When to Use Advanced Methods](#1-when-to-use-advanced-methods).

**Step 2: Choose scaffold** - Select from Causal Inference, Predictive Modeling, Property-Based Testing, or Advanced EDA. See specific sections below.

**Step 3: Generate structure** - Apply advanced scaffold matching task complexity. See [2. Causal Inference Methods](#2-causal-inference-methods), [3. Predictive Modeling Pipeline](#3-predictive-modeling-pipeline), [4. Property-Based Testing](#4-property-based-testing), [5. Advanced EDA Techniques](#5-advanced-eda-techniques).

**Step 4: Validate** - Check assumptions, sensitivity analysis, robustness checks using [6. Advanced Validation Patterns](#6-advanced-validation-patterns).

**Step 5: Deliver** - Present with caveats, limitations, and recommendations for further analysis.

## 1. When to Use Advanced Methods

| Task Characteristic | Standard Template | Advanced Methodology |
|---------------------|-------------------|---------------------|
| **Causal question** | "Does X correlate with Y?" | "Does X cause Y?" → Causal inference needed |
| **Sample size** | < 1000 rows | > 10K rows with complex patterns |
| **Model complexity** | Linear/logistic regression | Ensemble methods, neural nets, feature interactions |
| **Test sophistication** | Unit tests, integration tests | Property-based tests, mutation testing, fuzz testing |
| **Data complexity** | Clean, tabular data | Multi-modal, high-dimensional, unstructured data |
| **Stakes** | Low (exploratory) | High (production ML, regulatory compliance) |

## 2. Causal Inference Methods

Use when research question is "Does X **cause** Y?" not just "Are X and Y correlated?"

### Causal Inference Scaffold

```python
# CAUSAL INFERENCE SCAFFOLD

# 1. DRAW CAUSAL DAG (Directed Acyclic Graph)
# Explicitly model: Treatment → Outcome, Confounders → Treatment & Outcome
#
#  Example:
#    Education → Income
#         ↑          ↑
#    Family Background
#
# Treatment: Education
# Outcome: Income
# Confounder: Family Background (affects both education and income)

# 2. IDENTIFY CONFOUNDERS
confounders = ['age', 'gender', 'family_income', 'region']
# These variables affect BOTH treatment and outcome
# If not controlled, they bias causal estimate

# 3. CHECK IDENTIFICATION ASSUMPTIONS
# For causal effect to be identifiable:
# a) No unmeasured confounders (all variables in DAG observed)
# b) Treatment assignment as-if random conditional on confounders
# c) Positivity: Every unit has nonzero probability of treatment/control

# 4. CHOOSE IDENTIFICATION STRATEGY

# Option A: RCT - Random assignment eliminates confounding. Check balance on confounders.
from scipy import stats
for var in confounders:
    _, p = stats.ttest_ind(treatment_group[var], control_group[var])
    print(f"{var}: {'✓' if p > 0.05 else '✗'} balanced")

# Option B: Regression - Control for confounders. Assumes no unmeasured confounding.
import statsmodels.formula.api as smf
model = smf.ols('outcome ~ treatment + age + gender + family_income', data=df).fit()
treatment_effect = model.params['treatment']

# Option C: Propensity Score Matching - Match treated to similar controls on P(treatment|X).
from sklearn.linear_model import LogisticRegression; from sklearn.neighbors import NearestNeighbors
ps_model = LogisticRegression().fit(df[confounders], df['treatment'])
df['ps'] = ps_model.predict_proba(df[confounders])[:,1]
treated, control = df[df['treatment']==1], df[df['treatment']==0]
nn = NearestNeighbors(n_neighbors=1).fit(control[['ps']])
_, indices = nn.kneighbors(treated[['ps']])
treatment_effect = treated['outcome'].mean() - control.iloc[indices.flatten()]['outcome'].mean()

# Option D: IV - Need instrument Z: affects treatment, not outcome (except through treatment).
from statsmodels.sandbox.regression.gmm import IV2SLS
iv_model = IV2SLS(df['income'], df[['education'] + confounders], df[['instrument'] + confounders]).fit()

# Option E: RDD - Treatment assigned at cutoff. Compare units just above/below threshold.
df['above_cutoff'] = (df['running_var'] >= cutoff).astype(int)
# Use local linear regression around cutoff to estimate effect

# Option F: DiD - Compare treatment vs control, before vs after. Assumes parallel trends.
t_before, t_after = df[(df['group']=='T') & (df['time']=='before')]['y'].mean(), df[(df['group']=='T') & (df['time']=='after')]['y'].mean()
c_before, c_after = df[(df['group']=='C') & (df['time']=='before')]['y'].mean(), df[(df['group']=='C') & (df['time']=='after')]['y'].mean()
did_estimate = (t_after - t_before) - (c_after - c_before)

# 5. SENSITIVITY ANALYSIS
print("\n=== SENSITIVITY CHECKS ===")
print("1. Unmeasured confounding: How strong would confounder need to be to change conclusion?")
print("2. Placebo tests: Check for effect in period before treatment (should be zero)")
print("3. Falsification tests: Check for effect on outcome that shouldn't be affected")
print("4. Robustness: Try different model specifications, subsamples, bandwidths (RDD)")

# 6. REPORT CAUSAL ESTIMATE WITH UNCERTAINTY
print(f"\nCausal Effect: {treatment_effect:.3f}")
print(f"95% CI: [{ci_lower:.3f}, {ci_upper:.3f}]")
print(f"Interpretation: Treatment X causes {treatment_effect:.1%} change in outcome Y")
print(f"Assumptions: [List key identifying assumptions]")
print(f"Limitations: [Threats to validity]")
```

### Causal Inference Checklist

- [ ] **Causal question clearly stated**: "Does X cause Y?" not "Are X and Y related?"
- [ ] **DAG drawn**: Treatment, outcome, confounders, mediators identified
- [ ] **Identification strategy chosen**: RCT, regression, PS matching, IV, RDD, DiD
- [ ] **Assumptions checked**: No unmeasured confounding, positivity, parallel trends (DiD), etc.
- [ ] **Sensitivity analysis**: Test robustness to violations of assumptions
- [ ] **Limitations acknowledged**: Threats to internal/external validity stated

## 3. Predictive Modeling Pipeline

Use for forecasting, classification, regression - when goal is prediction not causal understanding.

### Predictive Modeling Scaffold

```python
# PREDICTIVE MODELING SCAFFOLD

# 1. DEFINE PREDICTION TASK & METRIC
task = "Predict customer churn (binary classification)"
primary_metric = "F1-score"  # Balance precision/recall
secondary_metrics = ["AUC-ROC", "precision", "recall", "accuracy"]

# 2. TRAIN/VAL/TEST SPLIT (before any preprocessing!)
from sklearn.model_selection import train_test_split

# Split: 60% train, 20% validation, 20% test
train_val, test = train_test_split(df, test_size=0.2, random_state=42, stratify=df['target'])
train, val = train_test_split(train_val, test_size=0.25, random_state=42, stratify=train_val['target'])

print(f"Train: {len(train)}, Val: {len(val)}, Test: {len(test)}")
print(f"Class balance - Train: {train['target'].mean():.2%}, Test: {test['target'].mean():.2%}")

# 3. FEATURE ENGINEERING (fit on train, transform train/val/test)
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

# Numeric features: impute missing, standardize
numeric_features = ['age', 'income', 'tenure']
num_imputer = SimpleImputer(strategy='median').fit(train[numeric_features])
num_scaler = StandardScaler().fit(num_imputer.transform(train[numeric_features]))

X_train_num = num_scaler.transform(num_imputer.transform(train[numeric_features]))
X_val_num = num_scaler.transform(num_imputer.transform(val[numeric_features]))
X_test_num = num_scaler.transform(num_imputer.transform(test[numeric_features]))

# Categorical features: one-hot encode
from sklearn.preprocessing import OneHotEncoder
cat_features = ['region', 'product_type']
cat_encoder = OneHotEncoder(handle_unknown='ignore', sparse=False).fit(train[cat_features])

X_train_cat = cat_encoder.transform(train[cat_features])
X_val_cat = cat_encoder.transform(val[cat_features])
X_test_cat = cat_encoder.transform(test[cat_features])

# Combine features
import numpy as np
X_train = np.hstack([X_train_num, X_train_cat])
X_val = np.hstack([X_val_num, X_val_cat])
X_test = np.hstack([X_test_num, X_test_cat])
y_train, y_val, y_test = train['target'], val['target'], test['target']

# 4. BASELINE MODEL (always start simple!)
from sklearn.dummy import DummyClassifier
baseline = DummyClassifier(strategy='most_frequent').fit(X_train, y_train)
baseline_f1 = f1_score(y_val, baseline.predict(X_val))
print(f"Baseline F1: {baseline_f1:.3f}")

# 5. MODEL SELECTION & HYPERPARAMETER TUNING
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import f1_score, roc_auc_score

# Try multiple models
models = {
    'Logistic Regression': LogisticRegression(max_iter=1000),
    'Random Forest': RandomForestClassifier(random_state=42),
    'Gradient Boosting': GradientBoostingClassifier(random_state=42)
}

results = {}
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_val)
    y_proba = model.predict_proba(X_val)[:,1]

    results[name] = {
        'F1': f1_score(y_val, y_pred),
        'AUC': roc_auc_score(y_val, y_proba),
        'Precision': precision_score(y_val, y_pred),
        'Recall': recall_score(y_val, y_pred)
    }
    print(f"{name}: F1={results[name]['F1']:.3f}, AUC={results[name]['AUC']:.3f}")

# Select best model (highest F1 on validation)
best_model_name = max(results, key=lambda x: results[x]['F1'])
best_model = models[best_model_name]
print(f"\nBest model: {best_model_name}")

# Hyperparameter tuning on best model
if best_model_name == 'Random Forest':
    param_grid = {
        'n_estimators': [100, 200, 300],
        'max_depth': [10, 20, None],
        'min_samples_split': [2, 5, 10]
    }
    grid_search = GridSearchCV(best_model, param_grid, cv=5, scoring='f1', n_jobs=-1)
    grid_search.fit(X_train, y_train)
    best_model = grid_search.best_estimator_
    print(f"Best params: {grid_search.best_params_}")

# 6. CROSS-VALIDATION (check for overfitting)
from sklearn.model_selection import cross_val_score
cv_scores = cross_val_score(best_model, X_train, y_train, cv=5, scoring='f1')
print(f"CV F1 scores: {cv_scores}")
print(f"Mean: {cv_scores.mean():.3f}, Std: {cv_scores.std():.3f}")

# 7. FINAL EVALUATION ON TEST SET (only once!)
y_test_pred = best_model.predict(X_test)
y_test_proba = best_model.predict_proba(X_test)[:,1]

test_f1 = f1_score(y_test, y_test_pred)
test_auc = roc_auc_score(y_test, y_test_proba)
print(f"\n=== FINAL TEST PERFORMANCE ===")
print(f"F1: {test_f1:.3f}, AUC: {test_auc:.3f}")

# 8. ERROR ANALYSIS
from sklearn.metrics import confusion_matrix, classification_report
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_test_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_test_pred))

# Analyze misclassifications
test_df = test.copy()
test_df['prediction'] = y_test_pred
test_df['prediction_proba'] = y_test_proba
false_positives = test_df[(test_df['target']==0) & (test_df['prediction']==1)]
false_negatives = test_df[(test_df['target']==1) & (test_df['prediction']==0)]
print(f"False Positives: {len(false_positives)}")
print(f"False Negatives: {len(false_negatives)}")
# Inspect these cases to understand failure modes

# 9. FEATURE IMPORTANCE
if hasattr(best_model, 'feature_importances_'):
    feature_names = numeric_features + list(cat_encoder.get_feature_names_out(cat_features))
    importances = pd.DataFrame({
        'feature': feature_names,
        'importance': best_model.feature_importances_
    }).sort_values('importance', ascending=False)
    print("\nTop 10 Features:")
    print(importances.head(10))

# 10. MODEL DEPLOYMENT CHECKLIST
print("\n=== DEPLOYMENT READINESS ===")
print(f"✓ Test F1 ({test_f1:.3f}) > Baseline ({baseline_f1:.3f})")
print(f"✓ Cross-validation shows consistent performance (CV std={cv_scores.std():.3f})")
print("✓ Error analysis completed, failure modes understood")
print("✓ Feature importance computed, no surprising features")
print("□ Model serialized and saved")
print("□ Monitoring plan in place (track drift in input features, output distribution)")
print("□ Rollback plan if model underperforms in production")
```

### Predictive Modeling Checklist

- [ ] **Clear prediction task**: Classification, regression, time series forecasting
- [ ] **Appropriate metrics**: Match business objectives (precision vs recall tradeoff, etc.)
- [ ] **Train/val/test split**: Before any preprocessing (no data leakage)
- [ ] **Baseline model**: Simple model for comparison
- [ ] **Feature engineering**: Proper handling of missing values, scaling, encoding
- [ ] **Cross-validation**: k-fold CV to check for overfitting
- [ ] **Model selection**: Compare multiple model types
- [ ] **Hyperparameter tuning**: Grid/random search on validation set
- [ ] **Error analysis**: Understand failure modes, inspect misclassifications
- [ ] **Test set evaluation**: Final performance check (only once!)
- [ ] **Deployment readiness**: Monitoring, rollback plan, model versioning

## 4. Property-Based Testing

Use for testing complex logic, data transformations, invariants. Goes beyond example-based tests.

### Property-Based Testing Scaffold

```python
# PROPERTY-BASED TESTING SCAFFOLD
from hypothesis import given, strategies as st
import pytest

# Example: Testing a sort function
def my_sort(lst):
    return sorted(lst)

# Property 1: Output length equals input length
@given(st.lists(st.integers()))
def test_sort_preserves_length(lst):
    assert len(my_sort(lst)) == len(lst)

# Property 2: Output is sorted (each element <= next element)
@given(st.lists(st.integers()))
def test_sort_is_sorted(lst):
    result = my_sort(lst)
    for i in range(len(result) - 1):
        assert result[i] <= result[i+1]

# Property 3: Output contains same elements as input (multiset equality)
@given(st.lists(st.integers()))
def test_sort_preserves_elements(lst):
    result = my_sort(lst)
    assert sorted(lst) == sorted(result)  # Canonical form comparison

# Property 4: Idempotence (sorting twice = sorting once)
@given(st.lists(st.integers()))
def test_sort_is_idempotent(lst):
    result = my_sort(lst)
    assert my_sort(result) == result

# Property 5: Empty input → empty output
def test_sort_empty_list():
    assert my_sort([]) == []

# Property 6: Single element → unchanged
@given(st.integers())
def test_sort_single_element(x):
    assert my_sort([x]) == [x]
```

### Property-Based Testing Strategies

**For data transformations:**
- Idempotence: `f(f(x)) == f(x)`
- Round-trip: `decode(encode(x)) == x`
- Commutativity: `f(g(x)) == g(f(x))`
- Invariants: Properties that never change (e.g., sum after transformation)

**For numeric functions:**
- Boundary conditions: Zero, negative, very large numbers
- Inverse relationships: `f(f_inverse(x)) ≈ x`
- Known identities: `sin²(x) + cos²(x) = 1`

**For string/list operations:**
- Length preservation or predictable change
- Character/element preservation
- Order properties (sorted, reversed)

## 5. Advanced EDA Techniques

For high-dimensional, multi-modal, or complex data.

### Dimensionality Reduction

```python
# PCA: Linear dimensionality reduction
from sklearn.decomposition import PCA
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)
print(f"Explained variance: {pca.explained_variance_ratio_}")

# t-SNE: Non-linear, good for visualization
from sklearn.manifold import TSNE
tsne = TSNE(n_components=2, perplexity=30, random_state=42)
X_tsne = tsne.fit_transform(X_scaled)
plt.scatter(X_tsne[:,0], X_tsne[:,1], c=y, cmap='viridis'); plt.show()

# UMAP: Faster alternative to t-SNE, preserves global structure
# pip install umap-learn
import umap
reducer = umap.UMAP(n_components=2, random_state=42)
X_umap = reducer.fit_transform(X_scaled)
```

### Cluster Analysis

```python
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score

# Elbow method: Find optimal K
inertias = []
for k in range(2, 11):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X_scaled)
    inertias.append(kmeans.inertia_)
plt.plot(range(2, 11), inertias); plt.xlabel('K'); plt.ylabel('Inertia'); plt.show()

# Silhouette score: Measure cluster quality
for k in range(2, 11):
    kmeans = KMeans(n_clusters=k, random_state=42).fit(X_scaled)
    score = silhouette_score(X_scaled, kmeans.labels_)
    print(f"K={k}: Silhouette={score:.3f}")

# DBSCAN: Density-based clustering (finds arbitrary shapes)
dbscan = DBSCAN(eps=0.5, min_samples=5)
clusters = dbscan.fit_predict(X_scaled)
print(f"Clusters found: {len(set(clusters)) - (1 if -1 in clusters else 0)}")
print(f"Noise points: {(clusters == -1).sum()}")
```

## 6. Advanced Validation Patterns

### Mutation Testing

Tests the quality of your tests by introducing bugs and checking if tests catch them.

```python
# Install: pip install mutmut
# Run: mutmut run --paths-to-mutate=src/
# Check: mutmut results
# Survivors (mutations not caught) indicate weak tests
```

### Fuzz Testing

Generate random/malformed inputs to find edge cases.

```python
from hypothesis import given, strategies as st

@given(st.text())
def test_function_doesnt_crash_on_any_string(s):
    result = my_function(s)  # Should never raise exception
    assert result is not None
```

### Data Validation Framework (Great Expectations)

```python
import great_expectations as gx

# Define expectations
expectation_suite = gx.ExpectationSuite(name="my_data_suite")
expectation_suite.add_expectation(gx.expectations.ExpectColumnToExist(column="user_id"))
expectation_suite.add_expectation(gx.expectations.ExpectColumnValuesToNotBeNull(column="user_id"))
expectation_suite.add_expectation(gx.expectations.ExpectColumnValuesToBeBetween(column="age", min_value=0, max_value=120))

# Validate data
results = context.run_validation(batch_request, expectation_suite)
print(results["success"])  # True if all expectations met
```

## 7. When to Use Each Method

| Research Goal | Method | Key Consideration |
|---------------|--------|-------------------|
| Causal effect estimation | RCT, IV, RDD, DiD | Identify confounders, check assumptions |
| Prediction/forecasting | Supervised ML | Avoid data leakage, validate out-of-sample |
| Pattern discovery | Clustering, PCA, t-SNE | Dimensionality reduction first if high-D |
| Complex logic testing | Property-based testing | Define invariants that must hold |
| Data quality | Great Expectations | Automate checks in pipelines |
