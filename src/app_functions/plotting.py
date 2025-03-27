import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def create_prediction_plot(results_df: pd.DataFrame) -> px.line:
    """
    Plot the actual and predicted stock prices from the model.

    Parameters
    ----------
    results_df : pd.DataFrame
        The DataFrame used for training and evaluation. 
        Must contain columns "Date", "Actual", "Prediction", and "Trend Agreement".

    Returns
    -------
    plotly.express.Figure
        The Plotly figure object.
    """

    # Ensure Date column is in datetime format
    results_df["Date"] = pd.to_datetime(results_df["Date"])
    
    # Create interactive plot with Plotly Express
    fig = px.line(
        results_df,
        x="Date",
        y=["Actual", "Prediction"],
        title=f"Stock Price Prediction - AAPL",
        labels={"value": "Price", "variable": "Type"},
        template="plotly_white"
    )
    
    # Define custom hover template for Actual and Prediction
    fig.update_traces(
        hovertemplate="     <b>%{y:$,.2f}</b>",
        selector=dict(name="Actual")
    )
    fig.update_traces(
        hovertemplate="<b>%{y:$,.2f}</b>",
        selector=dict(name="Prediction")
    )

    # Define time ranges
    latest_date = results_df["Date"].max()
    time_ranges = {
        "5 years": latest_date - pd.DateOffset(years=5),
        "2 years": latest_date - pd.DateOffset(years=2),
        "1 year": latest_date - pd.DateOffset(years=1),
        "6 months": latest_date - pd.DateOffset(months=6),
        "3 months": latest_date - pd.DateOffset(months=3),
        "1 month": latest_date - pd.DateOffset(months=1),
        "2 weeks": latest_date - pd.DateOffset(days=14),
    }

    # Add buttons for different time scales and set default to 2 years
    fig.update_layout(
        updatemenus=[
            {
                "buttons": [
                    {"label": label, "method": "relayout", "args": ["xaxis.range", [time_ranges[label], latest_date]]}
                    for label in time_ranges
                ],
                "direction": "down",
                "showactive": True,
                "active": 1,  # Set active button to 2 years
                "x": 0.375,
                "xanchor": "right",
                "y": 1.275,
                "yanchor": "top",
            }
        ],
        hovermode="x unified",
        xaxis_range=[time_ranges["2 years"], latest_date],  # Set default to 2 years
        margin=dict(b=0),
    )

    return fig