from sqlalchemy import create_engine, text
import pandas as pd

engine = create_engine(
    "mysql+pymysql://root:rj20cf0362@localhost/wealth_platform"
)


def recommend_portfolio(risk_profile):

    if risk_profile == "Conservative":
        return {
            "BND": 40,
            "SPY": 40,
            "CASH": 20
        }

    elif risk_profile == "Moderate":
        return {
            "SPY": 60,
            "BND": 30,
            "CASH": 10
        }

    elif risk_profile == "Aggressive":
        return {
            "SPY": 80,
            "BND": 20
        }


client_id = 1

portfolio_name = "Moderate Growth Portfolio"

allocation = recommend_portfolio("Moderate")

with engine.begin() as conn:

    result = conn.execute(
        text("""
        INSERT INTO portfolios
        (client_id, portfolio_name)
        VALUES (:client_id, :portfolio_name)
        """),
        {
            "client_id": client_id,
            "portfolio_name": portfolio_name
        }
    )

    portfolio_id = result.lastrowid

    for ticker, allocation_percent in allocation.items():

        conn.execute(
            text("""
            INSERT INTO holdings
            (
                portfolio_id,
                ticker,
                asset_type,
                allocation_percent
            )
            VALUES
            (
                :portfolio_id,
                :ticker,
                :asset_type,
                :allocation_percent
            )
            """),
            {
                "portfolio_id": portfolio_id,
                "ticker": ticker,
                "asset_type": "ETF",
                "allocation_percent": allocation_percent
            }
        )

print("Portfolio Created Successfully!")












