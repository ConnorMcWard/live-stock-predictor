import pandas as pd

def compute_trend_agreement(data: pd.DataFrame) -> pd.DataFrame:
    """
    Compute the agreement between the actual and predicted trends.

    Parameters
    ----------
    data : pd.DataFrame
        The DataFrame containing the actual and predicted stock prices.
        Must contain columns "Actual" and "Prediction".

    Returns
    -------
    pd.DataFrame
        The input DataFrame with an additional column "Trend Agreement".
    """
    # Create a column for previous day's Actual values
    data["Prev_Actual"] = data["Actual"].shift(1)
    
    # Drop the first row since it will have NaN for Prev_Actual
    data.dropna(inplace=True)
    
    # Compute trend agreement
    data["Trend Agreement"] = data.apply(
        lambda row: "Agree (Up)" if row["Actual"] > row["Prev_Actual"] and row["Prediction"] > row["Prev_Actual"] 
        else "Agree (Down)" if row["Actual"] < row["Prev_Actual"] and row["Prediction"] < row["Prev_Actual"]
        else "Disagree",
        axis=1
    )
    
    return data