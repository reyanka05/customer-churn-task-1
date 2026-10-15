# Data Analytics — Task 1: Data Quality and Exploratory Analysis

## Objective
Audit and clean the supplied customer churn dataset, document data-quality decisions and validation checks, calculate summary statistics, and inspect meaningful distributions.

## Dataset
- Raw rows: **1,003**
- Columns: **11**
- Cleaned unique customers: **1,000**
- Target column: `Churn`

## Task-1 checklist

### 1. Profile the data
Completed:
- Column names and data types
- Missing values
- Duplicate rows
- Duplicate CustomerIDs
- Numeric outlier detection using the IQR rule
- Categorical value inspection

### 2. Clean the data
Documented decisions:
- Trim whitespace in categorical fields.
- Standardize obvious category variants.
- Remove exact duplicate rows.
- Keep the first record for repeated CustomerIDs after exact-duplicate removal.
- Fill missing `Age` and `MonthlyCharges` with the cleaned-data median.
- Fill missing `ContractType` with the mode.
- Round monetary fields to two decimals.
- Flag IQR outliers rather than deleting them automatically.

### 3. Summary statistics and distributions
Included:
- Descriptive statistics for numeric variables.
- Categorical distributions.
- Churn distribution.
- Contract distribution.
- Boxplots for Age, MonthlyCharges and SupportCalls.

### 4. One proof link
This repository is designed to be uploaded as one public GitHub repository. The README, notebook, code, data and outputs are all inside the same project, so one repository URL is enough for review.

## Important findings

- Raw dataset: **1,003 rows**
- Exact duplicate rows: **3**
- Duplicate CustomerIDs: **3**
- Missing Age: **4**
- Missing MonthlyCharges: **3**
- Missing ContractType: **2**
- Cleaned dataset: **1,000 unique customers**
- Missing cells after cleaning: **0**

## Files

- `data_quality_analysis.ipynb` — complete analysis notebook.
- `data_quality_analysis.py` — reproducible Python script.
- `data/customer_churn_dataset.csv` — original supplied dataset.
- `data/customer_churn_cleaned.csv` — cleaned analysis-ready dataset.
- `outputs/column_profile.csv` — column/data-type/missing-value profile.
- `outputs/data_quality_report.csv` — quality summary.
- `outputs/outlier_report.csv` — IQR outlier analysis.
- `outputs/summary_statistics.csv` — numeric descriptive statistics.
- `outputs/categorical_distributions.csv` — category counts and percentages.
- `outputs/validation_checks.csv` — cleaning validation evidence.
- `outputs/charts/` — distribution and outlier charts.
- `SUBMISSION_CHECKLIST.md` — final submission checklist.

## Limitation
The analysis is descriptive and based only on the supplied dataset. Outliers are flagged, not automatically treated as errors. No causal conclusion is made from the exploratory patterns.
