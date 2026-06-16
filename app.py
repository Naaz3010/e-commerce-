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
    orders["Date"],
    errors="coerce"
)

orders = orders.dropna(
    subset=["Date"]
)

orders["YearMonth"] = (
    orders["Date"]
    .dt.strftime("%Y-%m")
)

monthly_revenue = (
    orders.groupby(
        "YearMonth"
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
        x="YearMonth",
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
        x="YearMonth",
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


# =====================================================
# FORECASTING TAB
# =====================================================

with tab3:

    st.header("📈 Sales Forecast & Future Outlook")

    st.markdown(
        """
        Revenue forecast generated using
        Prophet Forecasting Model.
        """
    )

    st.caption(
    "Microsoft Fabric • Power BI • RFM Segmentation • Prophet Forecasting • Streamlit"
    )

    st.markdown("---")

    # ==========================================
    # FORECAST HORIZON
    # ==========================================

    horizon = st.slider(
        "Forecast Horizon (Months)",
        min_value=3,
        max_value=min(
            12,
            len(forecast)
        ),
        value=min(
            6,
            len(forecast)
        )
    )

    forecast_filtered = (
        forecast
        .head(horizon)
        .copy()
    )

    # ==========================================
    # KPI CARDS
    # ==========================================

    forecast_revenue = (
        forecast_filtered["yhat"]
        .sum()
    )

    forecast_upper = (
        forecast_filtered["yhat_upper"]
        .sum()
    )

    forecast_lower = (
        forecast_filtered["yhat_lower"]
        .sum()
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

    # ==========================================
    # FORECAST TREND
    # ==========================================

    fig_forecast = px.line(
        forecast_filtered,
        x="ds",
        y="yhat",
        markers=True,
        title="Revenue Forecast Trend"
    )

    fig_forecast.update_layout(
        xaxis_title="Date",
        yaxis_title="Forecast Revenue"
    )

    st.plotly_chart(
        fig_forecast,
        use_container_width=True
    )

    st.markdown("---")

    # ==========================================
    # CONFIDENCE INTERVAL
    # ==========================================

    fig_confidence = go.Figure()

    fig_confidence.add_trace(
        go.Scatter(
            x=forecast_filtered["ds"],
            y=forecast_filtered["yhat"],
            mode="lines",
            name="Forecast"
        )
    )

    fig_confidence.add_trace(
        go.Scatter(
            x=forecast_filtered["ds"],
            y=forecast_filtered["yhat_upper"],
            mode="lines",
            name="Upper Bound"
        )
    )

    fig_confidence.add_trace(
        go.Scatter(
            x=forecast_filtered["ds"],
            y=forecast_filtered["yhat_lower"],
            mode="lines",
            name="Lower Bound"
        )
    )

    fig_confidence.update_layout(
        title="Forecast Confidence Interval",
        xaxis_title="Date",
        yaxis_title="Revenue"
    )

    st.plotly_chart(
        fig_confidence,
        use_container_width=True
    )

    st.markdown("---")

    # ==========================================
    # FORECAST TABLE
    # ==========================================

    st.subheader(
        "Forecast Details"
    )

    display_forecast = (
        forecast_filtered[
            [
                "ds",
                "yhat",
                "yhat_lower",
                "yhat_upper"
            ]
        ]
        .copy()
    )

    display_forecast.columns = [
        "Forecast Date",
        "Expected Revenue",
        "Lower Estimate",
        "Upper Estimate"
    ]

    st.dataframe(
        display_forecast,
        use_container_width=True
    )

    st.markdown("---")

    st.success(
        f"""
        Expected Revenue for next
        {horizon} month(s):
        ${forecast_revenue:,.0f}
        """
    )



