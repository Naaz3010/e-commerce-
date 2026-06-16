import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Olist Analytics Platform",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# LOAD DATA
# -----------------------------

@st.cache_data
def load_data():

    orders = pd.read_csv("git_data/fact_orders_clean.csv")

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

# -----------------------------
# KPI CALCULATIONS
# -----------------------------

total_revenue = orders["payment_value"].sum()

total_orders = orders["order_id"].nunique()

total_customers = customers[
    "customer_unique_id"
].nunique()

aov = total_revenue / total_orders

# -----------------------------
# SIDEBAR
# -----------------------------

page = st.sidebar.radio(
    "Navigation",
    [
        "Executive Overview",
        "Customer Intelligence",
        "Forecasting"
    ]
)

# ==================================================
# PAGE 1
# ==================================================

if page == "Executive Overview":

    st.title("Executive Overview")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total Revenue",
        f"${total_revenue:,.0f}"
    )

    c2.metric(
        "Total Orders",
        f"{total_orders:,}"
    )

    c3.metric(
        "Total Customers",
        f"{total_customers:,}"
    )

    c4.metric(
        "Average Order Value",
        f"${aov:,.2f}"
    )

    st.markdown("---")

    # Revenue by Payment Type

    payment_df = (
        orders.groupby("payment_type")
        ["payment_value"]
        .sum()
        .reset_index()
    )

    fig1 = px.pie(
        payment_df,
        names="payment_type",
        values="payment_value",
        title="Revenue by Payment Type"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

# ==================================================
# PAGE 2
# ==================================================

elif page == "Customer Intelligence":

    st.title("Customer Intelligence")

    champions = (
        rfm[
            rfm["customer_segment"]
            == "Champions"
        ]
        ["customer_id"]
        .nunique()
    )

    at_risk = (
        rfm[
            rfm["customer_segment"]
            == "At Risk"
        ]
        ["customer_id"]
        .nunique()
    )

    revenue_per_customer = (
        total_revenue / total_customers
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Customers",
        f"{total_customers:,}"
    )

    c2.metric(
        "Revenue / Customer",
        f"${revenue_per_customer:,.2f}"
    )

    c3.metric(
        "Champions",
        f"{champions:,}"
    )

    c4.metric(
        "At Risk",
        f"{at_risk:,}"
    )

    st.markdown("---")

    left, right = st.columns(2)

    # Segment Distribution

    seg_df = (
        rfm["customer_segment"]
        .value_counts()
        .reset_index()
    )

    seg_df.columns = [
        "customer_segment",
        "count"
    ]

    fig2 = px.pie(
        seg_df,
        names="customer_segment",
        values="count",
        title="Customer Segment Distribution"
    )

    left.plotly_chart(
        fig2,
        use_container_width=True
    )

    # Revenue by Segment

    seg_rev = (
        rfm.groupby(
            "customer_segment"
        )["monetary"]
        .sum()
        .reset_index()
    )

    fig3 = px.bar(
        seg_rev,
        x="monetary",
        y="customer_segment",
        orientation="h",
        title="Revenue by Segment"
    )

    right.plotly_chart(
        fig3,
        use_container_width=True
    )

    # Scatter

    fig4 = px.scatter(
        rfm,
        x="recency",
        y="monetary",
        color="customer_segment",
        title="Recency vs Monetary"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

# ==================================================
# PAGE 3
# ==================================================

elif page == "Forecasting":

    st.title("Sales Forecast & Future Outlook")

    forecast_revenue = (
        forecast["yhat"].sum()
    )

    forecast_upper = (
        forecast["yhat_upper"].sum()
    )

    forecast_lower = (
        forecast["yhat_lower"].sum()
    )

    forecast_range = (
        forecast_upper
        - forecast_lower
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Forecast Revenue",
        f"${forecast_revenue:,.0f}"
    )

    c2.metric(
        "Best Case",
        f"${forecast_upper:,.0f}"
    )

    c3.metric(
        "Worst Case",
        f"${forecast_lower:,.0f}"
    )

    c4.metric(
        "Forecast Range",
        f"${forecast_range:,.0f}"
    )

    st.markdown("---")

    fig5 = px.line(
        forecast,
        x="ds",
        y="yhat",
        title="Forecast Revenue Trend"
    )

    st.plotly_chart(
        fig5,
        use_container_width=True
    )

    fig6 = px.line(
        forecast,
        x="ds",
        y=[
            "yhat",
            "yhat_upper",
            "yhat_lower"
        ],
        title="Forecast Confidence Interval"
    )

    st.plotly_chart(
        fig6,
        use_container_width=True
    )

    st.subheader("Forecast Details")

    st.dataframe(
        forecast,
        use_container_width=True
    )
