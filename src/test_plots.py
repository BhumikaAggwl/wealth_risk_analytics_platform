import pandas as pd
import matplotlib.pyplot as plt

comparison = pd.DataFrame({
    "Metric": ["Return", "Volatility", "Sharpe"],
    "Portfolio A": [0.1403, 0.0108, 0.8210],
    "Portfolio B": [0.1482, 0.0113, 0.8232]
})

comparison.set_index("Metric").plot(kind="bar")

plt.title("Portfolio Comparison")
plt.tight_layout()

plt.savefig("../docs/figures/portfolio_comparison.png")
plt.show()

stress = pd.DataFrame({
    "Scenario": [
        "Market Crash",
        "COVID Crash",
        "Tech Crash"
    ],
    "Loss": [
        100000,
        150000,
        200000
    ]
})

plt.bar(stress["Scenario"], stress["Loss"])

plt.title("Portfolio Stress Testing")
plt.ylabel("Loss (₹)")

plt.tight_layout()

plt.savefig("../docs/figures/stress_testing.png")
plt.show()

from sqlalchemy import create_engine

engine = create_engine(
    "mysql+pymysql://root:rj20cf0362@localhost/wealth_platform"
)

df = pd.read_sql(
    """
    SELECT *
    FROM market_data
    WHERE ticker='SPY'
    """,
    engine
)

plt.figure(figsize=(10,5))

plt.plot(
    pd.to_datetime(df["trade_date"]),
    df["close_price"]
)

plt.title("SPY Historical Price Trend")

plt.xlabel("Date")
plt.ylabel("Price")

plt.tight_layout()

plt.savefig("../docs/figures/spy_price_trend.png")
plt.show()