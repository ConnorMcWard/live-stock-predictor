# Live Stock Predictor
![image](https://github.com/user-attachments/assets/dbc0c71a-99c7-4a19-a030-c0a4ec55bdd9)

A containerized live stock predictor system that fetches daily stock data, updates a online incremental learning (OIL) predictive model, and visualizes the predictions via an interactive dashboard — all running in Docker.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
- [Contributing](#contributing)

## Overview

The Live Stock Predictor is designed to provide real-time stock predictions by:
- Fetching daily stock data using a `yfinance`-based script.
- Updating and training a predictive (OIL) model with the latest data.
- Visualizing predictions using a Plotly-powered dashboard.

All components are containerized for consistency, reproducibility, and ease of deployment using Docker Desktop.

## Architecture

The system is built as a multi-container Docker application, where each service operates in its own container:

- **PostgreSQL Database:** <br>
  Stores both the historical stock data (and subsequent features) as well as predictions.

- **Data Ingestion:**  
  Fetches daily stock data and stores it in the `stock_data` database.

- **Model Trainer & Predictor:**  
  Consumes the latest data, updates the predictive model, and saves new predictions to the `predictions` database.

- **Plotly Dashboard App:**  
  Retrieves prediction data from the `predictions` database and renders interactive visualizations.

## Getting Started

### Setup

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/live-stock-predictor.git
   cd live-stock-predictor
   ```
2. **Build and Run the Containers:**
    ```bash
    docker-compose up --build
    ```
3. **Access the Dashboard:** <br>
    Open your browser and navigate to http://localhost:8050.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your enhancements.
