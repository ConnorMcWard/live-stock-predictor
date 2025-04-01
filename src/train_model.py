import pandas as pd
from river import linear_model, optim, metrics
import os
import time
from sqlalchemy import create_engine, text

def get_unprocessed_data(engine, ticker: str) -> pd.DataFrame:
    """
    Retrieve records from stock_data that have not yet been processed.
    """
    # Get last processed date from predictions table
    query_last = text("SELECT MAX(\"Date\") FROM predictions")
    with engine.connect() as conn:
        last_date = conn.execute(query_last).scalar()
    
    if last_date:
        query = text(
            "SELECT * FROM stock_data WHERE \"Ticker\" = :ticker AND \"Date\" > :last_date ORDER BY \"Date\" ASC"
        )
        df = pd.read_sql(query, engine, params={"ticker": ticker, "last_date": last_date})
    else:
        # Process all records if no predictions exist yet
        query = text("SELECT * FROM stock_data WHERE \"Ticker\" = :ticker ORDER BY \"Date\" ASC")
        df = pd.read_sql(query, engine, params={"ticker": ticker})
    return df

def process_and_train(engine, ticker: str, model):
    # Get new data from stock_data table
    df = get_unprocessed_data(engine, ticker)
    if df.empty:
        print("No new records to process.")
        return

    df["Date"] = pd.to_datetime(df["Date"])
    # Feature engineering
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["DayOfWeek"] = df["Date"].dt.dayofweek
    df["MA_5"] = df["Adj Close"].rolling(window=5).mean().shift(1)
    df["MA_10"] = df["Adj Close"].rolling(window=10).mean().shift(1)
    df["Volatility"] = df["Adj Close"].rolling(window=5).std().shift(1)
    df["Momentum"] = df["Adj Close"].diff(5).shift(1)
    df["Prev_Close"] = df["Adj Close"].shift(1)
    df.dropna(inplace=True)

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
            row["Date"]
        )
        for _, row in df.iterrows()
    ]
    
    results = []
    metric = metrics.MAE()
    for x, y, date in dataset:
        y_pred = model.predict_one(x)
        model.learn_one(x, y)
        metric.update(y, y_pred)
        results.append((date, y, y_pred))
    
    if results:
        results_df = pd.DataFrame(results, columns=["Date", "Actual", "Prediction"])
        # Append new predictions to the predictions table.
        results_df.to_sql("predictions", engine, if_exists="append", index=False)
        print(f"Processed and trained on {len(results_df)} new records.")
    else:
        print("No new predictions generated.")

if __name__ == "__main__":
    ticker = "AAPL"
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL environment variable not set")
    engine = create_engine(db_url)
    
    # Initialize the River model.
    model = linear_model.LinearRegression(optimizer=optim.Adam(lr=0.009))
    
    while True:
        print("=== Train Model Process Started ===")
        process_and_train(engine, ticker, model)
        print("Training process complete. Sleeping for 12 hours...")
        time.sleep(43200)  # Check for new data every 12 hours.
