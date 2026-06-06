import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "mysql+pymysql://root:rj20cf0362@localhost/wealth_platform"
)

tickers = ["SPY", "QQQ", "BND"]

for ticker in tickers:

    df = yf.download(
        ticker,
        period="5y",
        auto_adjust=True
    )

    df = df.reset_index()

    df = df[["Date", "Close"]]

    df.columns = ["trade_date", "close_price"]

    df["ticker"] = ticker

    df.to_sql(
        "market_data",
        engine,
        if_exists="append",
        index=False
    )

    print(f"{ticker} loaded")

for ticker in tickers:

    # all your existing code

    print(f"{ticker} loaded")

# ADD BELOW THIS

market_data = pd.read_sql(
    "SELECT * FROM market_data",
    engine
)

market_data.to_csv(
    "../data/market_data.csv",
    index=False
)

print("CSV Saved")