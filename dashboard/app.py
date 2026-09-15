import pandas as pd
import streamlit as st
from pathlib import Path


# -----------------------------
# Page setup
# -----------------------------
st.set_page_config(
    page_title="SaaS Customer Health Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("SaaS Customer Health & Churn Dashboard")

st.caption(
    "Customer churn risk, health scores and retention priorities."
)


# -----------------------------
# Locate project files
# -----------------------------
project_root = Path(__file__).resolve().parent.parent

customer_health_path = (
    project_root
    / "data"
    / "processed"
    / "customer_health_scores.csv"
)


# -----------------------------
# Load customer health data
# -----------------------------
customer_health_data = pd.read_csv(
    customer_health_path
)


# -----------------------------
# Dashboard KPIs
# -----------------------------
total_customers = len(customer_health_data)

high_risk_customers = (
    customer_health_data["risk_level"]
    .eq("High")
    .sum()
)

average_health_score = (
    customer_health_data["health_score"]
    .mean()
)

average_churn_risk = (
    customer_health_data["churn_probability_percent"]
    .mean()
)

column1, column2, column3, column4 = st.columns(4)

column1.metric(
    "Total Customers",
    total_customers
)

column2.metric(
    "High Risk Customers",
    high_risk_customers
)

column3.metric(
    "Average Health Score",
    f"{average_health_score:.1f}/100"
)

column4.metric(
    "Average Churn Risk",
    f"{average_churn_risk:.1f}%"
)


# -----------------------------
# Risk filter
# -----------------------------
st.subheader("Customer Risk Overview")

risk_filter = st.selectbox(
    "Filter by risk level",
    ["All", "High", "Medium", "Low"]
)

if risk_filter == "All":
    filtered_customers = customer_health_data.copy()
else:
    filtered_customers = customer_health_data[
        customer_health_data["risk_level"] == risk_filter
    ].copy()


# -----------------------------
# Customer table
# -----------------------------
display_columns = [
    "account_id",
    "industry",
    "latest_plan_tier",
    "latest_mrr",
    "churn_probability_percent",
    "health_score",
    "risk_level",
    "action_priority"
]

st.dataframe(
    filtered_customers[display_columns],
    use_container_width=True,
    hide_index=True
)

# -----------------------------
# Risk distribution
# -----------------------------
st.subheader("Risk Distribution")

risk_distribution = (
    customer_health_data["risk_level"]
    .value_counts()
    .reindex(["High", "Medium", "Low"])
)

st.bar_chart(risk_distribution)


# -----------------------------
# Individual customer view
# -----------------------------
st.subheader("Customer Detail")

selected_account = st.selectbox(
    "Select customer account",
    customer_health_data["account_id"].tolist()
)

selected_customer = customer_health_data[
    customer_health_data["account_id"] == selected_account
].iloc[0]


detail_column1, detail_column2, detail_column3 = st.columns(3)

detail_column1.metric(
    "Churn Risk",
    f"{selected_customer['churn_probability_percent']:.1f}%"
)

detail_column2.metric(
    "Health Score",
    f"{selected_customer['health_score']:.1f}/100"
)

detail_column3.metric(
    "Risk Level",
    selected_customer["risk_level"]
)


st.write(
    "**Industry:**",
    selected_customer["industry"]
)

st.write(
    "**Latest Plan:**",
    selected_customer["latest_plan_tier"]
)

st.write(
    "**Monthly Recurring Revenue:**",
    f"£{selected_customer['latest_mrr']:,.0f}"
)

st.write(
    "**Action Priority:**",
    selected_customer["action_priority"]
)

st.write(
    "**Top Model Risk Signals:**",
    selected_customer["top_risk_signals"]
)

st.write(
    "**Recommended Action:**",
    selected_customer["recommended_action"]
)