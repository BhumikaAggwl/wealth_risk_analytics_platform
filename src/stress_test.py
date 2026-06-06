import pandas as pd
portfolio_value = 500000

scenarios = {

    "Market Crash": -0.20,

    "Tech Crash": -0.40,

    "COVID Style Crash": -0.30

}

results = []

for scenario, shock in scenarios.items():

    stressed_value = (
        portfolio_value * (1 + shock)
    )

    loss = (
        portfolio_value - stressed_value
    )

    results.append(
        {
            "Scenario": scenario,
            "Loss": loss,
            "Portfolio_Value": stressed_value
        }
    )

    print(
        scenario,
        stressed_value,
        loss
    )
pd.DataFrame(results).to_csv(
    "../data/stress_test_results.csv",
    index=False
)
