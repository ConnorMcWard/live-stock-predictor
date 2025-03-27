import pandas as pd
import matplotlib.pyplot as plt
from river import linear_model, optim
from river import metrics
import plotly.express as px
import pickle
import os

# Load data
df = pd.read_csv("data/input/AAPL.csv")
df["Date"] = pd.to_datetime(df["Date"])

# Extract date-based features
df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month
df["DayOfWeek"] = df["Date"].dt.dayofweek
df["MA_5"] = df["Adj Close"].rolling(window=5).mean().shift(1)  # 5-day moving average
df["MA_10"] = df["Adj Close"].rolling(window=10).mean().shift(1)  # 10-day moving average
df["Volatility"] = df["Adj Close"].rolling(window=5).std().shift(1)
df["Momentum"] = df["Adj Close"].diff(5).shift(1)

# Create a lag feature (previous day's adjusted close)
df["Prev_Close"] = df["Adj Close"].shift(1)
df.dropna(inplace=True)  # Remove first row with NaN

# Convert to river format
dataset = [
    (
        {
            "Year": row["Year"],
            "Month": row["Month"],
            "DayOfWeek": row["DayOfWeek"],
            "Prev_Close": row["Prev_Close"],
            "MA_5": row["MA_5"],
            "MA_10": row["MA_10"],
            "Volatility": row["Volatility"],
            "Momentum": row["Momentum"],
        },
        row["Adj Close"],
        row["Date"]  # Store date separately
    )
    for _, row in df.iterrows()
]

model = linear_model.LinearRegression(optimizer=optim.Adam(lr=0.009))

# Evaluate model
def predict_train_model(model, dataset) -> pd.DataFrame: 
    """
    Predict the stock price and train the model incremenentally.

    Parameters
    ----------
    model : river.base.Estimator
        The model to train and evaluate.
    dataset : list
        A list of tuples containing features, target, and date. \n
        Example: [(features, target, date), ...]
    
    Returns
    -------
    pd.DataFrame
        A DataFrame containing the actual and predicted stock prices.
    river.base.Estimator
        The trained model.
    """

    metric = metrics.MAE()  # Use MAE directly

    results = []

    for x, y, date in dataset:
        y_pred = model.predict_one(x)
        model.learn_one(x, y)
        metric.update(y, y_pred)
        results.append((date, y, y_pred))

    results_df = pd.DataFrame(results, columns=["Date", "Actual", "Prediction"])
    
    return results_df, model
    

if __name__ == "__main__":
    # Run model evaluation
    df_results, model = predict_train_model(model, dataset)

    # Save results
    os.makedirs("../data/results", exist_ok=True)
    df_results.to_csv("data/results/predictions.csv", index=False)

    # Save model
    with open('models/model.pkl', 'wb') as f:
        pickle.dump(model, f)

    print("Model training complete.")

