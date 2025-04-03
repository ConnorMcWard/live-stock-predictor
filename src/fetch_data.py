import yfinance as yf
import pandas as pd
import os
import time
from sqlalchemy import create_engine, text


def fetch_ticker_data(ticker: str, period: str, interval: str) -> pd.DataFrame:
    """
    Download historical stock data from Yahoo Finance.

    Args:
        ticker (str): Stock ticker symbol.
        period (str): How far to look back from last available trading day. \n
                        Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        interval (str): How frequently to sample data. \n
                        Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo \n
                        Intraday data cannot extend last 60 days

    Returns:
        data (pd.DataFrame): A DataFrame containing historical stock data for the given ticker.
    """
    try:
        # download historical ticker data
        data = yf.download(
            tickers=ticker, 
            period=period,
            interval=interval,
            actions=False, 
            threads=True, 
            auto_adjust=False,
            multi_level_index=False,
        ).reset_index()

        df = data.copy()

    except Exception as e:
        print(f"Error downloading {ticker}: {e}")
        df = pd.DataFrame()

    return df

def save_stock_data_to_db(ticker: str, df: pd.DataFrame, engine, table_name: str = "stock_data") -> None:
    """
    Insert new stock data into the database.
    """
    df['Ticker'] = ticker
    df.to_sql(table_name, engine, if_exists='append', index=False)
    print(f"Data for {ticker} inserted into table '{table_name}'.")

def check_if_initial_run(engine, ticker: str) -> bool:
    """
    Return True if no data exists in the table for the given ticker.
    """
    try:
        query = text("SELECT COUNT(*) FROM stock_data WHERE \"Ticker\" = :ticker")
        with engine.connect() as conn:
            count = conn.execute(query, {'ticker': ticker}).scalar()
            return count == 0
    except Exception as e:
        # If table doesn't exist or any error occurs, assume initial run.
        return True

if __name__ == "__main__":
    # get Apple Ticker data ("AAPL")
    ticker = "AAPL"
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL environment variable not set")
    engine = create_engine(db_url)
    
    while True:
        print("=== Fetch Data Process Started ===")
        initial_run = check_if_initial_run(engine, ticker)
        period = "3mo" if initial_run else "1d"
        interval = "1d"  # Adjust as needed
        
        print(f"Fetching data for {ticker} with period '{period}'")
        df = fetch_ticker_data(ticker=ticker, period=period, interval=interval)
        if not df.empty:
            save_stock_data_to_db(ticker, df, engine, table_name="stock_data")
        else:
            print("No data fetched.")
        
        print("Fetch process complete. Sleeping for 12 hours...")
        time.sleep(43200)  # Sleep for 12 hours
