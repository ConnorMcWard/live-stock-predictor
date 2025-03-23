import yfinance as yf
import pandas as pd
import os


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
        df = df[["Date", "Adj Close"]]

    except Exception as e:
        print(f"Error downloading {ticker}: {e}")
        data=pd.DataFrame()

    return df


def save_stock_data(ticker: str, full_df: pd.DataFrame, output_path: str) -> None:
    """
    Save metadata and historical stock data to data output folder for model training

    Args:
        ticker (str): Stock ticker symbol.
        full_df (pd.DataFrame): DataFrame after being combined using combine_stock_data.
        output_path (str): output directory for storing data.
    """
    # create directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)

    full_file_path = os.path.join(output_path, f"{ticker}.csv")
    full_df.to_csv(path_or_buf=full_file_path, index=False)


if __name__ == "__main__":
    # get Apple Ticker data ("AAPL")
    ticker = "AAPL"

    print(f"Downloading Ticker: {ticker}")

    df = fetch_ticker_data(ticker=ticker, period='2y', interval='1d')

    save_stock_data(ticker, full_df=df, output_path="data/input/")

    print(f"{ticker} stock(s) download complete!")
