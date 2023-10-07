import queue
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import requests

# Define your data sources and fetch the necessary data
def fetch_market_data():
    # Replace 'YOUR_API_KEY' with your actual Alpha Vantage API key
    api_key = 'YOUR_API_KEY'

    # Define the parameters for the API request
    symbol = "AAPL"  # Example stock symbol (you can change this)
    interval = "1d"  # Daily data
    output_size = "compact"  # Compact data size (for demonstration purposes)

    # Make the API request to Alpha Vantage to fetch stock price data
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={api_key}&outputsize={output_size}"
    response = requests.get(url)
    data = response.json()

    # Extract the date and price data from the response
    dates = list(data['Time Series (Daily)'].keys())
    prices = [float(data['Time Series (Daily)'][date]['4. close']) for date in dates]

    # Create a DataFrame from the fetched data
    market_data = pd.DataFrame({
        "Date": pd.to_datetime(dates),
        "Symbol": symbol,
        "Price": prices,
    })

    return market_data

def fetch_portfolio_data():
    # Fetch and preprocess portfolio data
    # Example: Replace this with your actual data fetching and preprocessing logic
    portfolio_data = {
        "Date": pd.date_range(start="2023-01-01", periods=100, freq="D"),
        "Value": np.cumsum(np.random.normal(0, 10, size=100)) + 10000,
    }
    return portfolio_data

# Set up the Dash app
app = dash.Dash(__name__)

# Define the layout of the dashboard
app.layout = html.Div([
    html.H1("Automated Financial Data Visualization Dashboard"),
    dcc.Graph(id="market-trends-plot"),
    dcc.Graph(id="portfolio-performance-plot"),
    dcc.Graph(id="vwap-plot"),  # Added VWAP plot
    dcc.Interval(
        id="interval-component",
        interval=60000,  # Update every 60 seconds (adjust as needed)
        n_intervals=0
    ),
])

# Define callback functions to update the plots
@app.callback(
    Output("market-trends-plot", "figure"),
    Output("portfolio-performance-plot", "figure"),
    Output("vwap-plot", "figure"),  # Output for VWAP plot
    Input("interval-component", "n_intervals")  # For periodic updates
)
def update_plots(n_intervals):
    # Fetch and process the data
    market_data = fetch_market_data()
    portfolio_data = fetch_portfolio_data()

    # Calculate moving averages for different window sizes
    window_sizes = [10, 30, 50]
    moving_averages = calculate_moving_averages(market_data, window_sizes)

    # Calculate VWAP
    vwap = calculate_vwap(market_data)

    # Create comprehensive market trends plot using Plotly
    market_trends_plot = dcc.Graph(
        figure={
            "data": [
                {"x": market_data["Date"], "y": market_data["Price"], "type": "line", "name": "Price"},
                {"x": market_data["Date"], "y": moving_averages[f"MA_{window_size}"], "type": "line", "name": f"MA_{window_size}"}
            ],
            "layout": {
                "title": "Market Trends",
                "xaxis": {"title": "Date"},
                "yaxis": {"title": "Price"},
            },
        }
    )

    # Create portfolio performance plot using Plotly
    portfolio_performance_plot = dcc.Graph(
        figure={
            "data": [
                {"x": portfolio_data["Date"], "y": portfolio_data["Value"], "type": "line"}
            ],
            "layout": {
                "title": "Portfolio Performance",
                "xaxis": {"title": "Date"},
                "yaxis": {"title": "Value"},
            },
        }
    )

    # Create VWAP plot
    vwap_plot = dcc.Graph(
        figure={
            "data": [
                {"x": market_data["Date"], "y": vwap, "type": "line", "name": "VWAP"},
            ],
            "layout": {
                "title": "Volume Weighted Average Price (VWAP)",
                "xaxis": {"title": "Date"},
                "yaxis": {"title": "VWAP"},
            },
        }
    )

    # Return the plots
    return market_trends_plot, portfolio_performance_plot, vwap_plot

# Define a function to calculate the moving averages
def calculate_moving_averages(data, window_sizes):
    moving_averages = {}
    for window_size in window_sizes:
        # Calculate the moving average for each window size
        moving_averages[f'MA_{window_size}'] = data['Price'].rolling(window=window_size).mean()
    return moving_averages

# Define a function to calculate VWAP
def calculate_vwap(data):
    data['Volume_Price'] = data['Volume'] * data['Price']
    vwap = data['Volume_Price'].cumsum() / data['Volume'].cumsum()
    return vwap

# Inside your update_plots callback function, after fetching data
# ... (code provided above)

# Run the Dash app
if __name__ == "__main__":
    app.run_server(debug=True)
