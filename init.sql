-- Ensure the database exists
CREATE DATABASE stockdb;

\c stockdb;  -- Switch to stockdb

-- Create stock_data table
CREATE TABLE IF NOT EXISTS stock_data (
    "Date" TIMESTAMP,
    "Open" FLOAT,
    "High" FLOAT,
    "Low" FLOAT,
    "Close" FLOAT,
    "Adj Close" FLOAT,
    "Volume" INTEGER,
    "Ticker" VARCHAR(10)
);

-- Create predictions table
CREATE TABLE IF NOT EXISTS predictions (
    "Date" TIMESTAMP,
    "Actual" FLOAT,
    "Prediction" FLOAT
);