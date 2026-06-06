import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

engine = create_engine(
    "mysql+pymysql://root:rj20cf0362@localhost/wealth_platform"
)

st.set_page_config(
    page_title="Wealth Risk Analytics Platform",
    layout="wide"
)

st.title("Wealth Risk Analytics Platform")

clients = pd.read_sql(
    "SELECT * FROM clients",
    engine
)

holdings = pd.read_sql(
    "SELECT * FROM holdings",
    engine
)

risk = pd.read_sql(
    "SELECT * FROM risk_metrics",
    engine
)

market_data = pd.read_sql(
    "SELECT * FROM market_data",
    engine
)

st.header("Clients")
st.dataframe(clients)

st.header("Portfolio Holdings")
st.dataframe(holdings)

st.header("Risk Metrics")
st.dataframe(risk)

if not holdings.empty:

    allocation = (
        holdings.groupby("ticker")
        ["allocation_percent"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        allocation,
        values="allocation_percent",
        names="ticker",
        title="Portfolio Allocation"
    )

    st.plotly_chart(fig)

if not market_data.empty:

    ticker = st.selectbox(
        "Select ETF",
        market_data["ticker"].unique()
    )

    chart_data = market_data[
        market_data["ticker"] == ticker
    ]

    fig2 = px.line(
        chart_data,
        x="trade_date",
        y="close_price",
        title=f"{ticker} Historical Prices"
    )

    st.plotly_chart(fig2)

if not risk.empty:

    latest = risk.iloc[-1]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Volatility",
        round(latest["volatility"], 4)
    )

    col2.metric(
        "Sharpe Ratio",
        round(latest["sharpe_ratio"], 4)
    )

    col3.metric(
        "VaR 95%",
        round(latest["var_95"], 4)
    )

    col4.metric(
        "Max Drawdown",
        round(latest["max_drawdown"], 4)
    )