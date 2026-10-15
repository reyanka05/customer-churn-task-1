"""
DATA ANALYTICS - TASK 1
Data Quality and Exploratory Analysis

This script:
1. Profiles columns, data types, missing values, outliers and duplicates.
2. Cleans the customer churn data using documented assumptions.
3. Calculates summary statistics and categorical distributions.
4. Runs validation checks and saves evidence files/charts.

Run from this project folder:
    pip install pandas numpy matplotlib
    python data_quality_analysis.py
"""

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "data" / "customer_churn_dataset.csv"
DATA_DIR = ROOT / "data"
OUT = ROOT / "outputs"
CHARTS = OUT / "charts"

OUT.mkdir(exist_ok=True)
CHARTS.mkdir(exist_ok=True)

raw = pd.read_csv(INPUT)

# 1) Normalize whitespace in categorical columns
df = raw.copy()
cat_cols = ["CustomerID", "Gender", "ContractType", "PaymentMethod", "InternetService", "Churn"]
for c in cat_cols:
    df[c] = df[c].apply(lambda x: x.strip() if isinstance(x, str) else x)

# Standardize known category variants
df["Gender"] = df["Gender"].replace({"female": "Female", "Female": "Female",
                                     "male": "Male", "Male": "Male"})
df["ContractType"] = df["ContractType"].replace({
    "month-to-month": "Month-to-month", "Month-to-month": "Month-to-month",
    "One year": "One year", "Two year": "Two year"
})

# 2) Numeric coercion
num_cols = ["Age", "TenureMonths", "MonthlyCharges", "TotalCharges", "SupportCalls"]
for c in num_cols:
    df[c] = pd.to_numeric(df[c], errors="coerce")

# 3) Remove exact duplicates, then duplicate CustomerIDs
df = df.drop_duplicates()
df = df.drop_duplicates(subset=["CustomerID"], keep="first")

# 4) Missing-value treatment
df["Age"] = df["Age"].fillna(df["Age"].median())
df["MonthlyCharges"] = df["MonthlyCharges"].fillna(df["MonthlyCharges"].median())
df["ContractType"] = df["ContractType"].fillna(df["ContractType"].mode().iloc[0])

# 5) Round monetary fields
df["MonthlyCharges"] = df["MonthlyCharges"].round(2)
df["TotalCharges"] = df["TotalCharges"].round(2)

# Save cleaned data
df.to_csv(DATA_DIR / "customer_churn_cleaned.csv", index=False)

# 6) Column profile
profile = pd.DataFrame({
    "Column": raw.columns,
    "Data_Type": [str(raw[c].dtype) for c in raw.columns],
    "Non_Null": [raw[c].notna().sum() for c in raw.columns],
    "Missing": [raw[c].isna().sum() for c in raw.columns],
    "Unique_Non_NA": [raw[c].nunique() for c in raw.columns]
})
profile.to_csv(OUT / "column_profile.csv", index=False)

# 7) Summary statistics
summary = df[num_cols].describe().T.reset_index().rename(columns={"index":"Variable"})
summary["Missing"] = df[num_cols].isna().sum().values
summary.round(2).to_csv(OUT / "summary_statistics.csv", index=False)

# 8) Categorical distributions
parts = []
for c in ["Gender","ContractType","PaymentMethod","InternetService","Churn"]:
    x = df[c].value_counts(dropna=False).rename_axis("Category").reset_index(name="Count")
    x["Column"] = c
    x["Percentage"] = (x["Count"] / len(df) * 100).round(2)
    parts.append(x[["Column","Category","Count","Percentage"]])
pd.concat(parts, ignore_index=True).to_csv(OUT / "categorical_distributions.csv", index=False)

# 9) IQR outlier report
rows = []
for c in num_cols:
    s = raw[c].dropna()
    q1, q3 = s.quantile([.25,.75])
    iqr = q3 - q1
    lo, hi = q1 - 1.5*iqr, q3 + 1.5*iqr
    count = int(((s < lo) | (s > hi)).sum())
    rows.append([c,q1,q3,iqr,lo,hi,count,s.min(),s.max(),
                 "Flagged and retained; an IQR outlier is not automatically an invalid record."])
pd.DataFrame(rows, columns=["Column","Q1","Q3","IQR","Lower_Bound","Upper_Bound",
                            "Outlier_Count","Min","Max","Treatment"]).round(2).to_csv(
                                OUT / "outlier_report.csv", index=False)

# 10) Validation checks
checks = pd.DataFrame({
    "Check": [
        "No missing values after cleaning",
        "CustomerID unique",
        "Age between 18 and 100",
        "TenureMonths between 0 and 120",
        "MonthlyCharges non-negative",
        "TotalCharges non-negative",
        "SupportCalls non-negative",
        "Churn only Yes/No"
    ],
    "Result": [
        not df.isna().any().any(),
        not df["CustomerID"].duplicated().any(),
        df["Age"].between(18,100).all(),
        df["TenureMonths"].between(0,120).all(),
        df["MonthlyCharges"].ge(0).all(),
        df["TotalCharges"].ge(0).all(),
        df["SupportCalls"].ge(0).all(),
        df["Churn"].isin(["Yes","No"]).all()
    ]
})
checks.to_csv(OUT / "validation_checks.csv", index=False)

# 11) Charts
df["Churn"].value_counts().reindex(["No","Yes"]).plot(kind="bar", figsize=(8,5))
plt.title("Customer Churn Distribution")
plt.xlabel("Churn"); plt.ylabel("Customers"); plt.xticks(rotation=0)
plt.tight_layout(); plt.savefig(CHARTS/"churn_distribution.png", dpi=160); plt.close()

df["ContractType"].value_counts().reindex(["Month-to-month","One year","Two year"]).plot(
    kind="bar", figsize=(8,5))
plt.title("Contract Type Distribution")
plt.xlabel("Contract Type"); plt.ylabel("Customers"); plt.xticks(rotation=15)
plt.tight_layout(); plt.savefig(CHARTS/"contract_distribution.png", dpi=160); plt.close()

for c, title in [("MonthlyCharges","Monthly Charges Distribution and Potential Outliers"),
                 ("SupportCalls","Support Calls Distribution and Potential Outliers"),
                 ("Age","Age Distribution")]:
    df.boxplot(column=c, figsize=(8,5))
    plt.title(title); plt.ylabel(c)
    plt.tight_layout(); plt.savefig(CHARTS/(c.lower()+"_boxplot.png"), dpi=160); plt.close()

print("Task-1 analysis completed.")
print("Cleaned rows:", len(df))
print("Outputs saved in:", OUT)
