import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Olist Business Analytics Platform",
    page_icon="📊",
    layout="wide"
)

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_data():

    orders = pd.read_csv(
        "git_data/fact_orders_clean.csv"
    )

    customers = pd.read_csv(
        "git_data/dim_customers_clean.csv"
    )

    products = pd.read_csv(
        "git_data/dim_products_clean.csv"
    )

    rfm = pd.read_csv(
        "git_data/customer_rfm_segments.csv"
    )

    forecast = pd.read_csv(
        "git_data/sales_forecast.csv"
    )

    return (
        orders,
        customers,
        products,
        rfm,
        forecast
    )

orders, customers, products, rfm, forecast = load_data()

# =====================================================
# DATA PREPARATION
# =====================================================

orders["Date"] = pd.to_datetime(
    orders["Date"]
)

forecast["ds"] = pd.to_datetime(
    forecast["ds"]
)

# Monthly Revenue

monthly_revenue = (
    orders.groupby(
        pd.Grouper(
            key="Date",
            freq="M"
        )
    )["payment_value"]
    .sum()
    .reset_index()
)

# State Revenue

state_revenue = (
    orders.merge(
        customers,
        on="customer_id",
        how="left"
    )
    .groupby("customer_state")
    ["payment_value"]
    .sum()
    .reset_index()
    .sort_values(
        "payment_value",
        ascending=False
    )
)

# Payment Revenue

payment_revenue = (
    orders.groupby(
        "payment_type"
    )["payment_value"]
    .sum()
    .reset_index()
)

# =====================================================
# KPI CALCULATIONS
# =====================================================

total_revenue = (
    orders["payment_value"]
    .sum()
)

total_orders = (
    orders["order_id"]
    .nunique()
)

total_customers = (
    customers["customer_unique_id"]
    .nunique()
)

aov = (
    total_revenue
    / total_orders
)

# =====================================================
# HEADER
# =====================================================

st.title(
    "📊 Olist Business Analytics Platform"
)

st.markdown(
    """
    End-to-End E-Commerce Analytics Solution
    built using Microsoft Fabric, Power BI,
    Python, RFM Segmentation and Forecasting.
    """
)

# =====================================================
# NAVIGATION
# =====================================================

tab1, tab2, tab3 = st.tabs(
    [
        "📊 Dashboard",
        "👥 Customer Explorer",
        "📈 Forecasting"
    ]
)




# =====================================================
# DASHBOARD TAB
# =====================================================

with tab1:

    st.header("Executive Dashboard")

    # KPI ROW

    k1, k2, k3, k4 = st.columns(4)

    k1.metric(
        "💰 Total Revenue",
        f"${total_revenue:,.0f}"
    )

    k2.metric(
        "📦 Total Orders",
        f"{total_orders:,}"
    )

    k3.metric(
        "👥 Total Customers",
        f"{total_customers:,}"
    )

    k4.metric(
        "🛒 Average Order Value",
        f"${aov:,.2f}"
    )

    st.markdown("---")

    # REVENUE TREND

    left, right = st.columns(2)

    fig_revenue = px.line(
        monthly_revenue,
        x="Date",
        y="payment_value",
        markers=True,
        title="Monthly Revenue Trend"
    )

    fig_revenue.update_layout(
        xaxis_title="Month",
        yaxis_title="Revenue"
    )

    left.plotly_chart(
        fig_revenue,
        use_container_width=True
    )

    # PAYMENT TYPE

    fig_payment = px.pie(
        payment_revenue,
        names="payment_type",
        values="payment_value",
        hole=0.5,
        title="Revenue by Payment Type"
    )

    right.plotly_chart(
        fig_payment,
        use_container_width=True
    )

    st.markdown("---")

    # TOP STATES

    top_states = state_revenue.head(10)

    fig_states = px.bar(
        top_states,
        x="payment_value",
        y="customer_state",
        orientation="h",
        title="Top 10 States by Revenue",
        text_auto=".2s"
    )

    fig_states.update_layout(
        yaxis=dict(
            categoryorder="total ascending"
        )
    )

    st.plotly_chart(
        fig_states,
        use_container_width=True
    )

    st.markdown("---")

    # QUICK INSIGHTS

    st.subheader("📌 Business Insights")

    top_state = top_states.iloc[0]["customer_state"]

    top_payment = (
        payment_revenue
        .sort_values(
            "payment_value",
            ascending=False
        )
        .iloc[0]["payment_type"]
    )

    insight1, insight2 = st.columns(2)

    insight1.info(
        f"""
        Top Revenue State:
        {top_state}
        """
    )

    insight2.info(
        f"""
        Most Used Payment Type:
        {top_payment}
        """
    )



