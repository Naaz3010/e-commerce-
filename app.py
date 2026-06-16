import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Olist Business Analytics",
    layout="wide"
)

st.title("Olist Business Analytics Dashboard")

# Load data

forecast = pd.read_csv("data/sales_forecast.csv")
rfm = pd.read_csv("data/customer_rfm_segments.csv")

# Sidebar

page = st.sidebar.selectbox(
    "Choose Page",
    [
        "Executive Overview",
        "Customer Intelligence",
        "Forecasting"
    ]
)

# PAGE 1

if page == "Executive Overview":

    st.header("Executive Overview")

    col1,col2,col3,col4 = st.columns(4)

    col1.metric("Revenue","$16.0M")
    col2.metric("Orders","99K")
    col3.metric("Customers","96K")
    col4.metric("AOV","$161")

# PAGE 2

elif page == "Customer Intelligence":

    st.header("Customer Intelligence")

    seg = (
        rfm["customer_segment"]
        .value_counts()
        .reset_index()
    )

    fig = px.pie(
        seg,
        names="customer_segment",
        values="count",
        title="Customer Segments"
    )

    st.plotly_chart(fig,use_container_width=True)

# PAGE 3

elif page == "Forecasting":

    st.header("Revenue Forecast")

    fig = px.line(
        forecast,
        x="ds",
        y="yhat",
        title="Forecast Revenue Trend"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    fig2 = px.line(
        forecast,
        x="ds",
        y=[
            "yhat",
            "yhat_lower",
            "yhat_upper"
        ],
        title="Forecast Confidence Interval"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )
