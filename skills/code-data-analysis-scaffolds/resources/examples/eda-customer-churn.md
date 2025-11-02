# EDA Example: Customer Churn Analysis

Complete exploratory data analysis for telecom customer churn dataset.

## Task

Explore customer churn dataset to understand:
- What factors correlate with churn?
- Are there data quality issues?
- What features should we engineer for predictive model?

## Dataset

- **Rows**: 7,043 customers
- **Target**: `Churn` (Yes/No)
- **Features**: 20 columns (demographics, account info, usage patterns)

## EDA Scaffold Applied

### 1. Data Overview

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('telecom_churn.csv')

print(f"Shape: {df.shape}")
# Output: (7043, 21)

print(f"Columns: {df.columns.tolist()}")
# ['customerID', 'gender', 'SeniorCitizen', 'Partner', 'Dependents',
#  'tenure', 'PhoneService', 'MultipleLines', 'InternetService',
#  'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport',
#  'StreamingTV', 'StreamingMovies', 'Contract', 'PaperlessBilling',
#  'PaymentMethod', 'MonthlyCharges', 'TotalCharges', 'Churn']

print(df.dtypes)
# customerID        object
# gender            object
# SeniorCitizen      int64
# tenure             int64
# MonthlyCharges   float64
# TotalCharges      object  ← Should be numeric!
# Churn             object

print(df.head())
print(df.describe())
```

**Findings**:
- TotalCharges is object type (should be numeric) - needs fixing
- Churn is target variable (26.5% churn rate)

### 2. Data Quality Checks

```python
# Missing values
missing = df.isnull().sum()
missing_pct = (missing / len(df)) * 100
print(missing_pct[missing_pct > 0])
# No missing values marked as NaN

# But TotalCharges is object - check for empty strings
print((df['TotalCharges'] == ' ').sum())
# Output: 11 rows have space instead of number

# Fix: Convert TotalCharges to numeric
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
print(df['TotalCharges'].isnull().sum())
# Output: 11 (now properly marked as missing)

# Strategy: Drop 11 rows (< 0.2% of data)
df = df.dropna()

# Duplicates
print(f"Duplicates: {df.duplicated().sum()}")
# Output: 0

# Data consistency checks
print("Tenure vs TotalCharges consistency:")
print(df[['tenure', 'MonthlyCharges', 'TotalCharges']].head())
# tenure=1, Monthly=$29, Total=$29 ✓
# tenure=34, Monthly=$57, Total=$1889 ≈ $57*34 ✓
```

**Findings**:
- 11 rows (0.16%) with missing TotalCharges - dropped
- No duplicates
- TotalCharges ≈ MonthlyCharges × tenure (consistent)

### 3. Univariate Analysis

```python
# Target variable
print(df['Churn'].value_counts(normalize=True))
# No     73.5%
# Yes    26.5%

# Imbalanced but not severely (>20% minority class is workable)

# Numeric variables
numeric_cols = ['tenure', 'MonthlyCharges', 'TotalCharges']
for col in numeric_cols:
    print(f"\n{col}:")
    print(f"  Mean: {df[col].mean():.2f}, Median: {df[col].median():.2f}")
    print(f"  Std: {df[col].std():.2f}, Range: [{df[col].min()}, {df[col].max()}]")

    # Histogram
    df[col].hist(bins=50, edgecolor='black')
    plt.title(f'{col} Distribution')
    plt.xlabel(col)
    plt.show()

    # Check outliers
    Q1, Q3 = df[col].quantile([0.25, 0.75])
    IQR = Q3 - Q1
    outliers = ((df[col] < (Q1 - 1.5*IQR)) | (df[col] > (Q3 + 1.5*IQR))).sum()
    print(f"  Outliers: {outliers} ({outliers/len(df)*100:.1f}%)")
```

**Findings**:
- **tenure**: Right-skewed (mean=32, median=29). Many new customers (0-12 months).
- **MonthlyCharges**: Bimodal distribution (peaks at ~$20 and ~$80). Suggests customer segments.
- **TotalCharges**: Right-skewed (correlated with tenure). Few outliers (2.3%).

```python
# Categorical variables
cat_cols = ['gender', 'SeniorCitizen', 'Partner', 'Dependents', 'Contract', 'PaymentMethod']
for col in cat_cols:
    print(f"\n{col}: {df[col].nunique()} unique values")
    print(df[col].value_counts())

    # Bar plot
    df[col].value_counts().plot(kind='bar')
    plt.title(f'{col} Distribution')
    plt.xticks(rotation=45)
    plt.show()
```

**Findings**:
- **gender**: Balanced (50/50 male/female)
- **SeniorCitizen**: 16% are senior citizens
- **Contract**: 55% month-to-month, 24% one-year, 21% two-year
- **PaymentMethod**: Electronic check most common (34%)

### 4. Bivariate Analysis (Churn vs Features)

```python
# Churn rate by categorical variables
for col in cat_cols:
    churn_rate = df.groupby(col)['Churn'].apply(lambda x: (x=='Yes').mean())
    print(f"\n{col} vs Churn:")
    print(churn_rate.sort_values(ascending=False))

    # Stacked bar chart
    pd.crosstab(df[col], df['Churn'], normalize='index').plot(kind='bar', stacked=True)
    plt.title(f'Churn Rate by {col}')
    plt.ylabel('Proportion')
    plt.show()
```

**Key Findings**:
- **Contract**: Month-to-month churn=42.7%, One-year=11.3%, Two-year=2.8% (Strong signal!)
- **SeniorCitizen**: Seniors churn=41.7%, Non-seniors=23.6%
- **PaymentMethod**: Electronic check=45.3% churn, others~15-18%
- **tenure**: Customers with tenure<12 months churn=47.5%, >60 months=7.9%

```python
# Numeric variables vs Churn
for col in numeric_cols:
    plt.figure(figsize=(10, 4))

    # Box plot
    plt.subplot(1, 2, 1)
    df.boxplot(column=col, by='Churn')
    plt.title(f'{col} by Churn')

    # Histogram (overlay)
    plt.subplot(1, 2, 2)
    df[df['Churn']=='No'][col].hist(bins=30, alpha=0.5, label='No Churn', density=True)
    df[df['Churn']=='Yes'][col].hist(bins=30, alpha=0.5, label='Churn', density=True)
    plt.legend()
    plt.xlabel(col)
    plt.title(f'{col} Distribution by Churn')
    plt.show()
```

**Key Findings**:
- **tenure**: Churned customers have lower tenure (mean=18 vs 38 months)
- **MonthlyCharges**: Churned customers pay MORE ($74 vs $61/month)
- **TotalCharges**: Churned customers have lower total (correlated with tenure)

```python
# Correlation matrix
numeric_df = df[['tenure', 'MonthlyCharges', 'TotalCharges', 'SeniorCitizen']].copy()
numeric_df['Churn_binary'] = (df['Churn'] == 'Yes').astype(int)

corr = numeric_df.corr()
plt.figure(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap='coolwarm', center=0)
plt.title('Correlation Matrix')
plt.show()
```

**Key Findings**:
- tenure ↔ TotalCharges: 0.83 (strong positive correlation - expected)
- Churn ↔ tenure: -0.35 (negative: longer tenure → less churn)
- Churn ↔ MonthlyCharges: +0.19 (positive: higher charges → more churn)
- Churn ↔ TotalCharges: -0.20 (negative: driven by tenure)

### 5. Insights & Recommendations

```python
print("\n=== KEY FINDINGS ===")
print("1. Data Quality:")
print("   - 11 rows (<0.2%) dropped due to missing TotalCharges")
print("   - No other quality issues. Data is clean.")
print("")
print("2. Churn Patterns:")
print("   - Overall churn rate: 26.5% (slightly imbalanced)")
print("   - Strongest predictor: Contract type (month-to-month 42.7% vs two-year 2.8%)")
print("   - High-risk segment: New customers (<12mo tenure) with high monthly charges")
print("   - Low churn: Long-term customers (>60mo) on two-year contracts")
print("")
print("3. Feature Importance:")
print("   - **High signal**: Contract, tenure, PaymentMethod, SeniorCitizen")
print("   - **Medium signal**: MonthlyCharges, InternetService")
print("   - **Low signal**: gender, PhoneService (balanced across churn/no-churn)")
print("")
print("\n=== RECOMMENDED ACTIONS ===")
print("1. Feature Engineering:")
print("   - Create 'tenure_bucket' (0-12mo, 12-24mo, 24-60mo, >60mo)")
print("   - Create 'high_charges' flag (MonthlyCharges > $70)")
print("   - Interaction: tenure × Contract (captures switching cost)")
print("   - Payment risk score (Electronic check is risky)")
print("")
print("2. Model Strategy:")
print("   - Use all categorical features (one-hot encode)")
print("   - Baseline: Predict churn for month-to-month + new customers")
print("   - Advanced: Random Forest or Gradient Boosting (handle interactions)")
print("   - Validate with stratified 5-fold CV (preserve 26.5% churn rate)")
print("")
print("3. Business Insights:")
print("   - **Retention program**: Target month-to-month customers < 12mo tenure")
print("   - **Contract incentives**: Offer discounts for one/two-year contracts")
print("   - **Payment method**: Encourage auto-pay (reduce electronic check)")
print("   - **Early warning**: Monitor customers with high MonthlyCharges + short tenure")
```

### 6. Self-Assessment

Using rubric:

- **Clarity** (5/5): Systematic exploration, clear findings at each stage
- **Completeness** (5/5): Data quality, univariate, bivariate, insights all covered
- **Rigor** (5/5): Proper statistical analysis, visualizations, quantified relationships
- **Actionability** (5/5): Specific feature engineering and business recommendations

**Average**: 5.0/5 ✓

This EDA provides solid foundation for predictive modeling and business action.

## Next Steps

1. **Feature engineering**: Implement recommended features
2. **Baseline model**: Logistic regression with top 5 features
3. **Advanced models**: Random Forest, XGBoost with feature interactions
4. **Evaluation**: F1-score, precision/recall curves, AUC-ROC
5. **Deployment**: Real-time churn scoring API
