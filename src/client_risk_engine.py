from sqlalchemy import create_engine
import pandas as pd

engine = create_engine(
    "mysql+pymysql://root:rj20cf0362@localhost/wealth_platform"
)

def calculate_risk_score(age, horizon, market_crash_response):

    score = 0

    if age < 30:
        score += 30
    elif age < 50:
        score += 20
    else:
        score += 10

    if horizon >= 10:
        score += 30
    elif horizon >= 5:
        score += 20
    else:
        score += 10

    if market_crash_response == "Buy More":
        score += 40
    elif market_crash_response == "Hold":
        score += 20

    return score


def classify_risk(score):

    if score >= 80:
        return "Aggressive"

    elif score >= 50:
        return "Moderate"

    else:
        return "Conservative"


portfolios = {

    "Conservative": {
        "BND": 0.70,
        "SPY": 0.30
    },

    "Moderate": {
        "SPY": 0.60,
        "BND": 0.40
    },

    "Aggressive": {
        "SPY": 0.80,
        "QQQ": 0.20
    }
}


score = calculate_risk_score(
    age=21,
    horizon=10,
    market_crash_response="Buy More"
)

risk_profile = classify_risk(score)

print("Risk Score:", score)
print("Risk Profile:", risk_profile)

print("\nRecommended Portfolio")

for asset, weight in portfolios[risk_profile].items():
    print(asset, ":", weight * 100, "%")


market_data = pd.read_sql(
    "SELECT * FROM market_data",
    engine
)

print(market_data.head())


portfolio = portfolios[risk_profile]

prices = []

for ticker in portfolio.keys():

    temp = market_data[
        market_data["ticker"] == ticker
    ][["trade_date", "close_price"]]

    temp = temp.rename(
        columns={
            "close_price": ticker
        }
    )

    prices.append(temp)

final_df = prices[0]

for df in prices[1:]:
    final_df = final_df.merge(
        df,
        on="trade_date"
    )

print(final_df.head())

#return calcualted 
returns = final_df.drop(
    columns=["trade_date"]
).pct_change().dropna()

print(returns.head())
#weights 
weights = pd.Series(portfolio)

portfolio_returns = returns.dot(weights)

print(portfolio_returns.head())


#metrics
volatility = portfolio_returns.std()

annual_return = portfolio_returns.mean() * 252

sharpe = (
    annual_return /
    (volatility * (252**0.5))
)

var95 = portfolio_returns.quantile(0.05)

print("\nAnnual Return:", annual_return)
print("Volatility:", volatility)
print("Sharpe:", sharpe)
print("VaR95:", var95)




#PORTFOLIO RETURNS A AND B 

def portfolio_metrics(weights, returns):

    portfolio_returns = (
        returns[list(weights.keys())]
        .dot(pd.Series(weights))
    )

    annual_return = (
        portfolio_returns.mean() * 252
    )

    volatility = portfolio_returns.std()

    sharpe = (
        annual_return /
        (volatility * (252**0.5))
    )

    var95 = portfolio_returns.quantile(0.05)

    return {
        "Return": annual_return,
        "Volatility": volatility,
        "Sharpe": sharpe,
        "VaR": var95
    }


portfolio_A = {
    "SPY": 1.0
}

portfolio_B = {
    "SPY": 0.8,
    "QQQ": 0.2
}

metrics_A = portfolio_metrics(
    portfolio_A,
    returns
)

metrics_B = portfolio_metrics(
    portfolio_B,
    returns
)

print(metrics_A)
print(metrics_B)

comparison = pd.DataFrame(
    [metrics_A, metrics_B],
    index=["Portfolio_A", "Portfolio_B"]
)

comparison.to_csv(
    "../data/portfolio_comparison.csv"
)
