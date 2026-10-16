import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Customer Churn - Data Quality Analysis",
    page_icon="📊",
    layout="wide"
)

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"

st.title("📊 Customer Churn Data Quality & EDA")
st.write(
    "An exploratory analysis dashboard showing data quality, "
    "cleaning results, summary statistics, and customer distributions."
)

# Load datasets
clean_file = DATA_DIR / "customer_churn_cleaned.csv"
raw_file = DATA_DIR / "customer_churn_dataset.csv"

@st.cache_data
def load_csv(path):
    return pd.read_csv(path)

if clean_file.exists():
    df = load_csv(clean_file)
    st.subheader("1. Cleaned Dataset Overview")

    c1, c2, c3 = st.columns(3)
    c1.metric("Customer Records", f"{len(df):,}")
    c2.metric("Columns", len(df.columns))
    c3.metric("Missing Cells", int(df.isna().sum().sum()))

    st.dataframe(df.head(20), use_container_width=True)

    with st.expander("View column data types"):
        profile = pd.DataFrame({
            "Column": df.columns,
            "Data Type": df.dtypes.astype(str).values,
            "Missing Values": df.isna().sum().values
        })
        st.dataframe(profile, use_container_width=True)
else:
    st.warning("Cleaned dataset not found in the data folder.")

if raw_file.exists() and clean_file.exists():
    raw_df = load_csv(raw_file)
    st.subheader("2. Before and After Cleaning")

    c1, c2 = st.columns(2)
    c1.metric("Original Rows", f"{len(raw_df):,}")
    c2.metric("Cleaned Rows", f"{len(df):,}")

    st.write(
        f"Rows removed during cleaning: "
        f"**{len(raw_df) - len(df):,}**"
    )

st.subheader("3. Data Quality Reports")

report_names = [
    "column_profile.csv",
    "data_quality_report.csv",
    "outlier_report.csv",
    "summary_statistics.csv",
    "categorical_distributions.csv",
    "validation_checks.csv",
    "totalcharges_consistency.csv",
]

for name in report_names:
    path = OUTPUT_DIR / name
    if path.exists():
        with st.expander(name.replace(".csv", "").replace("_", " ").title()):
            st.dataframe(load_csv(path), use_container_width=True)

st.subheader("4. Visualizations")

chart_dir = OUTPUT_DIR / "charts"
if chart_dir.exists():
    charts = sorted(chart_dir.glob("*.png"))
    if charts:
        for chart in charts:
            st.markdown(f"**{chart.stem.replace('_', ' ').title()}**")
            st.image(str(chart), use_container_width=True)
    else:
        st.info("No PNG charts found in the outputs/charts folder.")
else:
    st.info("The charts folder has not been found.")

st.subheader("5. Download Cleaned Dataset")

if clean_file.exists():
    st.download_button(
        label="Download Cleaned CSV",
        data=clean_file.read_bytes(),
        file_name="customer_churn_cleaned.csv",
        mime="text/csv"
    )

st.caption("Task 1 | Data Quality and Exploratory Analysis")
