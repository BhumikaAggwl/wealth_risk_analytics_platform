import yfinance as yf 
import pandas as pd 
from sqlalchemy import create_engine, text
engine = create_engine(
    "mysql+pymysql://root:rj20cf0362@localhost/wealth_platform"
)
tickers=['SPY','BND']

data=yf.download(
        tickers,
        period='5y',
        auto_adjust=True 
)['Close']
weights={
    'SPY':0.60,
    'BND':0.60
}
print(data.head())
returns=data.pct_change().dropna()

print("\nDaily Returns")
print(returns.head())

weights=pd.Series(weights)
portfolio_returns =returns.dot(weights)
print(portfolio_returns.head())


volatility = portfolio_returns.std()

print("\nVolatility:")
print(volatility)


#sharpe ratio 
risk_free_rate=0.05 
daily_rf=risk_free_rate/252

sharpe_ratio=(
    (portfolio_returns.mean()-daily_rf)
    /portfolio_returns.std()
)

print("\nsharpe_ratio:")
print(sharpe_ratio)

# VAR 
var_95 =portfolio_returns.quantile(0.05)
print("\nVaR(95%):")
print(var_95)


stress_scenarios = {
    "Market Crash": -0.20,
    "Mild Correction": -0.10,
    "Tech Crash": -0.30
}
portfolio_value = 500000

for scenario, shock in stress_scenarios.items():

    stressed_value = portfolio_value * (1 + shock)

    loss = portfolio_value - stressed_value

    print(f"\n{scenario}")

    print(f"Portfolio Value: ₹{stressed_value:,.2f}")

    print(f"Loss: ₹{loss:,.2f}")


##saving risk metrics
portfolio_id = 1
cumulative_returns = (1 + portfolio_returns).cumprod()

rolling_max = cumulative_returns.cummax()

drawdown = (
    cumulative_returns - rolling_max
) / rolling_max

max_drawdown = drawdown.min()

print("\nMax Drawdown:")
print(max_drawdown)

with engine.begin() as conn:

    conn.execute(
        text("""
        INSERT INTO risk_metrics
        (
            portfolio_id,
            expected_return,
            volatility,
            sharpe_ratio,
            var_95,
            max_drawdown
        )
        VALUES
        (
            :portfolio_id,
            :expected_return,
            :volatility,
            :sharpe_ratio,
            :var_95,
            :max_drawdown
        )
        """),
        {
            "portfolio_id": portfolio_id,
            "expected_return": float(portfolio_returns.mean()),

            "volatility": float(volatility),

            "sharpe_ratio": float(sharpe_ratio),

            "var_95": float(var_95),

            "max_drawdown": float(max_drawdown)
        }
    )

print("Risk metrics saved!")