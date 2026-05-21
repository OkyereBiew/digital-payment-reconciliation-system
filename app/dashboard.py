# ==========================================
# DIGITAL PAYMENT RECONCILIATION DASHBOARD
# ==========================================

# Import libraries
import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------------------
# PAGE CONFIG
# ------------------------------------------

st.set_page_config(
    page_title="Payment Operations Dashboard",
    layout="wide"
)

# ------------------------------------------
# LOAD DATA
# ------------------------------------------

df = pd.read_csv(
    "data/processed/final_dashboard_dataset.csv"
)

# ------------------------------------------
# DASHBOARD TITLE
# ------------------------------------------

st.title("Digital Payment Reconciliation Dashboard")

st.markdown("""
Operational analytics dashboard for monitoring digital payment reconciliation, settlement delays, and suspicious transactions.
""")

# ------------------------------------------
# KPI METRICS
# ------------------------------------------

total_transactions = len(df)

reconciled_transactions = len(
    df[
        df["reconciliation_status"] == "RECONCILED"
    ]
)

unmatched_transactions = len(
    df[
        df["reconciliation_status"] == "UNMATCHED"
    ]
)

suspicious_transactions = len(
    df[
        df["suspicious_flag"] == "YES"
    ]
)

# ------------------------------------------
# KPI CARDS
# ------------------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Transactions",
    total_transactions
)

col2.metric(
    "Reconciled",
    reconciled_transactions
)

col3.metric(
    "Unmatched",
    unmatched_transactions
)

col4.metric(
    "Suspicious",
    suspicious_transactions
)

# ------------------------------------------
# RECONCILIATION STATUS CHART
# ------------------------------------------

status_counts = df[
    "reconciliation_status"
].value_counts().reset_index()

status_counts.columns = [
    "Status",
    "Count"
]

fig1 = px.bar(
    status_counts,
    x="Status",
    y="Count",
    title="Reconciliation Status"
)

st.plotly_chart(fig1)

# ------------------------------------------
# PROVIDER PERFORMANCE
# ------------------------------------------

provider_summary = df.groupby(
    "payment_provider"
)["settlement_delay_minutes"].mean().reset_index()

fig2 = px.bar(
    provider_summary,
    x="payment_provider",
    y="settlement_delay_minutes",
    title="Average Settlement Delay by Provider"
)

st.plotly_chart(fig2)

# ------------------------------------------
# TRANSACTION TYPE ANALYSIS
# ------------------------------------------

transaction_types = df[
    "type"
].value_counts().reset_index()

transaction_types.columns = [
    "Transaction Type",
    "Count"
]

fig3 = px.pie(
    transaction_types,
    names="Transaction Type",
    values="Count",
    title="Transaction Type Distribution"
)

st.plotly_chart(fig3)

# ------------------------------------------
# SUSPICIOUS TRANSACTIONS TABLE
# ------------------------------------------

st.subheader("Suspicious Transactions")

suspicious_df = df[
    df["suspicious_flag"] == "YES"
]

st.dataframe(
    suspicious_df.head(20)
)
