import dash
from dash import dcc, html, dash_table
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from app_functions.data_processing import compute_trend_agreement
from app_functions.plotting import create_prediction_plot

# Load Data (replace with actual file loading logic)
data = pd.read_csv("./data/results/predictions.csv")
data = compute_trend_agreement(data)

# Create Data Table
data_table = data.sort_values(by='Date', ascending=False)
data_table["Actual"] = data_table["Actual"].apply(lambda x: f"${x:.2f}")
data_table["Prediction"] = data_table["Prediction"].apply(lambda x: f"${x:.2f}")

# Data Summary
tot_agree_up = sum(data['Trend Agreement'] ==  'Agree (Up)')
tot_agree_down = sum(data['Trend Agreement'] == 'Agree (Down)')
tot_disagree = sum(data['Trend Agreement'] == 'Disagree')

# Dash App
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1(
        "Stock Prediction Dashboard",
        style={'margin-left': '20px'}  # Move the title slightly to the right
    ),
    
    
    dcc.Graph(
        id='prediction-plot',
        figure=create_prediction_plot(data)
    ),
    
    html.Div([
        html.Div([
            html.H3("Stock Prediction"),
            html.P(
                "Stock will go UP" if data.iloc[-1]['Prediction'] > data.iloc[-1]['Actual']
                else "Stock will go DOWN",
                style={'fontSize': '20px', 'fontWeight': 'bold'}
            ),
        ], style={'width': '33%', 'textAlign': 'center'}),

        html.Div([
            html.H3("Most Recent Trend Agreement"),
            html.P(data.iloc[-1]['Trend Agreement']),
        ], style={'width': '40%', 'textAlign': 'center'}),

        html.Div([
            html.H3("Trend Agreement Summary"),
            html.P(f" Agree (Up): {tot_agree_up}"),
            html.P(f" Agree (Down): {tot_agree_down}"),
            html.P(f"Disagree: {tot_disagree}"),
        ], style={'width': '40%', 'textAlign': 'center'})
    ], style={'display': 'flex', 
              'justify-content': 'space-between', 
              'alignItems': 'center',
              'padding': '20px',
              }),
    
    dash_table.DataTable(
        id='stock-table',
        columns=[
            {'name': 'Date', 'id': 'Date'},
            {'name': 'Actual', 'id': 'Actual'},
            {'name': 'Predicted', 'id': 'Prediction'},
            {'name': 'Trend Agreement', 'id': 'Trend Agreement'}
        ],
        data=data_table.to_dict('records'),
        page_size=10,
        page_action="native",
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'center'},  # Center-align all columns
    )
])

if __name__ == '__main__':
    app.run(debug=True)
