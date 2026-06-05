import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="SaaS Revenue Analytics", layout="wide")

st.title("SaaS Revenue Analytics Dashboard")
st.write("A dbt-powered revenue analytics project with CRM-style SaaS data.")

con = duckdb.connect("data/saas_analytics.duckdb")
df = con.execute("SELECT * FROM revenue_metrics").fetchdf()
con.close()

total_mrr = df["total_mrr"].sum()
total_arr = df["total_arr"].sum()
avg_churn = df["churn_rate_percent"].mean()
customers = df["total_customers"].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Customers", f"{customers:,.0f}")
col2.metric("MRR", f"€{total_mrr:,.0f}")
col3.metric("ARR", f"€{total_arr:,.0f}")
col4.metric("Avg Churn Rate", f"{avg_churn:.2f}%")

st.subheader("MRR by Region")
fig1 = px.bar(df, x="region", y="total_mrr", color="segment", barmode="group")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("Churn Rate by Segment")
fig2 = px.bar(df, x="segment", y="churn_rate_percent", color="region")
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Revenue Metrics Table")
st.dataframe(df)

st.subheader("Automated Business Insight")

highest_churn = df.sort_values("churn_rate_percent", ascending=False).iloc[0]
best_region = df.groupby("region")["total_mrr"].sum().sort_values(ascending=False).index[0]

st.write(
    f"The highest churn is in the {highest_churn['segment']} segment in "
    f"{highest_churn['region']} at {highest_churn['churn_rate_percent']}%. "
    f"The strongest revenue region is {best_region}. "
    f"Recommended action: investigate churn drivers in high-risk segments and prioritise expansion in stronger regions."
)