import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="e-commerce Analytics Platform",
    page_icon="📊",
    layout="wide"
)

# ==================================================
# LOAD DATA
# ==================================================

@st.cache_data
def load_data():

    orders = pd.read_csv(
        "git_data/fact_orders_clean.csv.gz"
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

# ==================================================
# DATA CLEANING
# ==================================================

orders["Date"] = pd.to_datetime(
    orders["Date"],
    errors="coerce"
)

orders = orders.dropna(
    subset=["Date"]
)

forecast["ds"] = pd.to_datetime(
    forecast["ds"],
    errors="coerce"
)

# ==================================================
# FEATURE ENGINEERING
# ==================================================

orders["YearMonth"] = (
    orders["Date"]
    .dt.strftime("%Y-%m")
)

# ==================================================
# KPI CALCULATIONS
# ==================================================

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
    / max(total_orders, 1)
)

# ==================================================
# REVENUE AGGREGATIONS
# ==================================================

monthly_revenue = (
    orders.groupby(
        "YearMonth",
        as_index=False
    )["payment_value"]
    .sum()
)

payment_revenue = (
    orders.groupby(
        "payment_type",
        as_index=False
    )["payment_value"]
    .sum()
)

state_revenue = (
    orders
    .merge(
        customers,
        on="customer_id",
        how="left"
    )
    .groupby(
        "customer_state",
        as_index=False
    )["payment_value"]
    .sum()
    .sort_values(
        "payment_value",
        ascending=False
    )
)

# ==================================================
# HEADER
# ==================================================

st.title(
    "📊 E-commerce Business Analytics Platform"
)

st.caption(
    """
    Microsoft Fabric • Power BI •
    RFM Segmentation • Prophet Forecasting
    """
)

st.markdown(
    """
    End-to-End E-Commerce Analytics
    Solution built using Microsoft Fabric.
    """
)

# ==================================================
# NAVIGATION
# ==================================================

tab1, tab2, tab3 = st.tabs(
    [
        "📊 Dashboard",
        "👥 Customer Explorer",
        "📈 Forecasting"
    ]
)

# ==================================================
# DASHBOARD TAB
# ==================================================

with tab1:

    st.header("Executive Dashboard")

    # ==========================================
    # KPI CARDS
    # ==========================================

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "💰 Revenue",
        f"${total_revenue:,.0f}"
    )

    c2.metric(
        "📦 Orders",
        f"{total_orders:,}"
    )

    c3.metric(
        "👥 Customers",
        f"{total_customers:,}"
    )

    c4.metric(
        "🛒 AOV",
        f"${aov:,.2f}"
    )

    st.markdown("---")

    # ==========================================
    # REVENUE TREND
    # ==========================================

    left, right = st.columns(2)

    fig_monthly_revenue = px.line(
        monthly_revenue,
        x="YearMonth",
        y="payment_value",
        markers=True,
        title="Monthly Revenue Trend"
    )

    fig_monthly_revenue.update_layout(
        xaxis_title="Month",
        yaxis_title="Revenue"
    )

    left.plotly_chart(
        fig_monthly_revenue,
        use_container_width=True
    )

    # ==========================================
    # PAYMENT TYPE ANALYSIS
    # ==========================================

    fig_payment_type = px.pie(
        payment_revenue,
        names="payment_type",
        values="payment_value",
        hole=0.5,
        title="Revenue by Payment Type"
    )

    right.plotly_chart(
        fig_payment_type,
        use_container_width=True
    )

    st.markdown("---")

    # ==========================================
    # TOP STATES
    # ==========================================

    top_states = (
        state_revenue
        .head(10)
        .copy()
    )

    fig_states = px.bar(
        top_states,
        x="payment_value",
        y="customer_state",
        orientation="h",
        title="Top 10 States by Revenue"
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

    # ==========================================
    # BUSINESS INSIGHTS
    # ==========================================

    st.subheader(
        "📌 Quick Business Insights"
    )

    top_state = (
        top_states
        .iloc[0]["customer_state"]
    )

    top_payment = (
        payment_revenue
        .sort_values(
            "payment_value",
            ascending=False
        )
        .iloc[0]["payment_type"]
    )

    i1, i2 = st.columns(2)

    i1.success(
        f"""
        Top Revenue State:
        {top_state}
        """
    )

    i2.success(
        f"""
        Most Popular Payment Type:
        {top_payment}
        """
    )

    st.markdown("---")

    st.subheader(
        "Executive Summary"
    )

    st.info(
        f"""
        Revenue generated:
        ${total_revenue:,.0f}

        Orders processed:
        {total_orders:,}

        Customers served:
        {total_customers:,}

        Average Order Value:
        ${aov:,.2f}
        """
    )

# ==================================================
# CUSTOMER EXPLORER TAB
# ==================================================

with tab2:

    st.header(
        "👥 Customer Intelligence"
    )

    st.markdown(
        """
        Explore customer segments,
        behavior and spending patterns.
        """
    )

    st.markdown("---")

    # ==========================================
    # SEGMENT SELECTION
    # ==========================================

    segment_filter = st.selectbox(
        "Select Customer Segment",
        sorted(
            rfm[
                "customer_segment"
            ]
            .dropna()
            .unique()
        )
    )

    filtered_rfm = rfm[
        rfm["customer_segment"]
        == segment_filter
    ]

    # ==========================================
    # KPI CARDS
    # ==========================================

    customer_count = (
        st.write(filtered_rfm.columns.tolist())

    avg_monetary = (
        filtered_rfm[
            "monetary"
        ]
        .mean()
    )

    avg_frequency = (
        filtered_rfm[
            "frequency"
        ]
        .mean()
    )

    avg_recency = (
        filtered_rfm[
            "recency"
        ]
        .mean()
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Customers",
        f"{customer_count:,}"
    )

    c2.metric(
        "Avg Spend",
        f"${avg_monetary:,.2f}"
    )

    c3.metric(
        "Avg Frequency",
        f"{avg_frequency:.2f}"
    )

    c4.metric(
        "Avg Recency",
        f"{avg_recency:.0f}"
    )

    st.markdown("---")

    # ==========================================
    # CUSTOMER SEARCH
    # ==========================================

    st.subheader(
        "🔍 Search Customer"
    )

    search_customer = st.text_input(
        "Enter Customer ID"
    )

    if search_customer:

        result = filtered_rfm[
            filtered_rfm[
                "customer_unique_id"
            ]
            .astype(str)
            == search_customer
        ]

        if not result.empty:

            st.success(
                "Customer Found"
            )

            st.dataframe(
                result,
                use_container_width=True
            )

        else:

            st.warning(
                "Customer not found in selected segment"
            )

    st.markdown("---")

    # ==========================================
    # SEGMENT DISTRIBUTION
    # ==========================================

    left, right = st.columns(2)

    segment_distribution = (
        rfm[
            "customer_segment"
        ]
        .value_counts()
        .reset_index()
    )

    segment_distribution.columns = [
        "customer_segment",
        "count"
    ]

    fig_segment_distribution = px.pie(
        segment_distribution,
        names="customer_segment",
        values="count",
        hole=0.5,
        title="Customer Segment Distribution"
    )

    left.plotly_chart(
        fig_segment_distribution,
        use_container_width=True
    )

    # ==========================================
    # REVENUE BY SEGMENT
    # ==========================================

    segment_revenue = (
        rfm.groupby(
            "customer_segment",
            as_index=False
        )["monetary"]
        .sum()
    )

    fig_segment_revenue = px.bar(
        segment_revenue,
        x="monetary",
        y="customer_segment",
        orientation="h",
        title="Revenue by Segment"
    )

    right.plotly_chart(
        fig_segment_revenue,
        use_container_width=True
    )

    st.markdown("---")

    # ==========================================
    # TOP CUSTOMERS
    # ==========================================

    st.subheader(
        "🏆 Top Customers"
    )

    top_customers = (
        filtered_rfm
        .sort_values(
            "monetary",
            ascending=False
        )
        .head(20)
    )

    st.dataframe(
        top_customers[
            [
                "customer_unique_id",
                "customer_segment",
                "recency",
                "frequency",
                "monetary",
                "rfm_score"
            ]
        ],
        use_container_width=True
    )


# ==================================================
# FORECASTING TAB
# ==================================================

with tab3:

    st.header(
        "📈 Forecasting Center"
    )

    st.markdown(
        """
        Revenue forecasting generated
        using Prophet Forecasting Model.
        """
    )

    st.markdown("---")

    # ==========================================
    # FORECAST HORIZON
    # ==========================================

    max_horizon = min(
        12,
        len(forecast)
    )

    horizon = st.slider(
        "Forecast Horizon",
        min_value=1,
        max_value=max_horizon,
        value=min(6, max_horizon)
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
        xaxis_title="Forecast Date",
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

    # ==========================================
    # DOWNLOAD FORECAST
    # ==========================================

    csv = display_forecast.to_csv(
        index=False
    )

    st.download_button(
        label="📥 Download Forecast",
        data=csv,
        file_name="forecast.csv",
        mime="text/csv"
    )

    st.markdown("---")

    st.success(
        f"""
        Expected Revenue for the next
        {horizon} period(s):

        ${forecast_revenue:,.0f}
        """
    )
