# Financial Dashboard Documentation

## Overview
This documentation provides a detailed explanation of the financial dashboard code. The dashboard is built using Dash, Plotly, and financial data fetched from Alpha Vantage. It includes components for displaying market trends, portfolio performance, and a Volume Weighted Average Price (VWAP) plot.

## Code Structure

### Libraries Used
- `queue`: Standard library for implementing queues.
- `numpy`: Library for numerical operations.
- `pandas`: Data manipulation library.
- `matplotlib.pyplot`: Plotting library.
- `seaborn`: Statistical data visualization library.
- `dash`: Web application framework for building interactive dashboards.
- `dash_core_components` and `dash_html_components`: Dash components for creating the dashboard layout.
- `dash.dependencies`: Dash dependencies for callback functions.
- `requests`: HTTP library for making API requests.

### Functions

#### `fetch_market_data()`
- Fetches daily adjusted stock price data from Alpha Vantage.
- Returns a Pandas DataFrame with date, symbol, and price columns.

#### `fetch_portfolio_data()`
- Generates example portfolio data for demonstration purposes.
- Returns a dictionary with date and value columns.

#### `update_plots(n_intervals)`
- Callback function to update the market trends, portfolio performance, and VWAP plots.
- Fetches market and portfolio data, calculates moving averages, and updates the plots.
- Triggered by the interval component every 60 seconds.

#### `calculate_moving_averages(data, window_sizes)`
- Calculates moving averages for different window sizes.
- Returns a dictionary of moving averages.

#### `calculate_vwap(data)`
- Calculates Volume Weighted Average Price (VWAP) based on market data.
- Returns a Pandas Series with VWAP values.

## Dash App Setup

### Layout
- The layout includes an H1 header and three dcc.Graph components for market trends, portfolio performance, and VWAP.
- An interval component triggers the `update_plots` callback every 60 seconds.

### Plots
1. **Market Trends Plot**
   - Line plot of daily stock prices and moving averages.
   - X-axis: Date, Y-axis: Price.
   
2. **Portfolio Performance Plot**
   - Line plot of portfolio value over time.
   - X-axis: Date, Y-axis: Value.

3. **VWAP Plot**
   - Line plot of Volume Weighted Average Price (VWAP).
   - X-axis: Date, Y-axis: VWAP.

## Prerequisites
- Python environment with required libraries installed.
- Alpha Vantage API key (replace 'YOUR_API_KEY' in the code).

## Running the Dashboard
Execute the script and access the dashboard through a web browser. The server runs in debug mode for development.

```python
if __name__ == "__main__":
    app.run_server(debug=True)
