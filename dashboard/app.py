from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd
import plotly.express as px
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.append(str(SRC_PATH))

from analysis_utils import (  # noqa: E402
    build_kpis,
    category_performance,
    load_sales_data,
    monthly_revenue,
    regional_performance,
    top_products,
)


st.set_page_config(page_title="Business Sales Performance Dashboard", layout="wide")
st.title("Business Sales Performance Dashboard")
st.caption("Task 1 – Data Science & Analytics (Future Interns, 2026)")


data_path = PROJECT_ROOT / "data" / "processed" / "business_sales_curated.csv"
df = load_sales_data(data_path)

st.sidebar.header("Filters")
selected_country = st.sidebar.multiselect("Country", sorted(df["country"].unique()), default=sorted(df["country"].unique()))
selected_region = st.sidebar.multiselect("Region", sorted(df["region"].unique()), default=sorted(df["region"].unique()))
selected_category = st.sidebar.multiselect("Category", sorted(df["category"].unique()), default=sorted(df["category"].unique()))

filtered = df[
    df["country"].isin(selected_country)
    & df["region"].isin(selected_region)
    & df["category"].isin(selected_category)
].copy()

if filtered.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

kpi = build_kpis(filtered)

col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.metric("Revenue", f"${kpi['total_revenue']:,.0f}")
col2.metric("Profit", f"${kpi['total_profit']:,.0f}")
col3.metric("Orders", f"{kpi['total_orders']:,}")
col4.metric("Avg Order Value", f"${kpi['avg_order_value']:,.0f}")
col5.metric("Profit Margin", f"{kpi['profit_margin_pct']:.1f}%")
col6.metric("Return Rate", f"{kpi['return_rate_pct']:.1f}%")

monthly = monthly_revenue(filtered)
fig_trend = px.line(monthly, x="month_start", y=["revenue", "profit"], markers=True, title="Monthly Revenue & Profit Trend")
st.plotly_chart(fig_trend, use_container_width=True)

left, right = st.columns(2)

with left:
    cat = category_performance(filtered)
    fig_cat = px.bar(cat, x="category", y="revenue", color="profit", title="Category Performance (Revenue with Profit Color)")
    st.plotly_chart(fig_cat, use_container_width=True)

with right:
    prod = top_products(filtered, n=10)
    fig_prod = px.bar(prod.sort_values("revenue"), x="revenue", y="product_name", orientation="h", title="Top 10 Products by Revenue")
    st.plotly_chart(fig_prod, use_container_width=True)

regional = regional_performance(filtered)
fig_region = px.bar(
    regional,
    x="region",
    y="revenue",
    color="country",
    barmode="group",
    title="Regional Revenue Performance",
)
st.plotly_chart(fig_region, use_container_width=True)

st.subheader("Actionable Recommendations")
recommendations = [
    "Prioritize inventory and promotions for the top 3 revenue products to protect peak-season sales.",
    "Increase budget allocation for high-margin categories while reducing discount depth in low-margin segments.",
    "Replicate best-performing regional playbooks (pricing, channel mix) in underperforming regions.",
    "Track monthly revenue and profit jointly to avoid growth that comes at the cost of margin erosion.",
]
for item in recommendations:
    st.write(f"- {item}")
