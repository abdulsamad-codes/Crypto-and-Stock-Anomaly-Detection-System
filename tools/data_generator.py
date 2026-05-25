import pandas as pd
import yfinance as yf
import requests
from datetime import datetime
import os

# --- PREPROCESSING CONFIG ---
# This script handles Milestone 3: Fetching, Cleaning, and Exporting Real Data
ASSETS_CRYPTO = ['bitcoin', 'ethereum']
ASSETS_STOCKS = ['NVDA', 'TSLA']
OUTPUT_DIR = 'data_exports'

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def fetch_crypto_data(coin_id):
    """Fetches real crypto data from CoinGecko API"""
    print(f"Fetching data for {coin_id}...")
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days=7"
    response = requests.get(url)
    data = response.json()
    
    # Preprocessing: Mapping JSON to our schema format (Price and Timestamp)
    prices = data['prices'] # List of [timestamp, price]
    df = pd.DataFrame(prices, columns=['timestamp', 'price_close'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    
    # Cleaning: Standardizing decimals and adding dummy volume for the lab
    df['volume'] = df['price_close'] * 100 # Simulated volume relative to price
    df['asset_id'] = 1 if coin_id == 'bitcoin' else 2
    return df.head(100) # Milestone 3 requires 50-100 rows

def fetch_stock_data(symbol, asset_id):
    """Fetches real stock data from Yahoo Finance"""
    print(f"Fetching data for {symbol}...")
    stock = yf.Ticker(symbol)
    df = stock.history(period="1mo", interval="1h")
    
    # Preprocessing: Resetting index to get timestamp and renaming columns
    df = df.reset_index()
    df = df[['Datetime', 'Close', 'Volume']]
    df.columns = ['timestamp', 'price_close', 'volume']
    
    # Cleaning: Removing timezone info for MySQL compatibility
    df['timestamp'] = df['timestamp'].dt.tz_localize(None)
    df['asset_id'] = asset_id
    return df.head(100)

def main():
    # 1. Assets Metadata Table
    assets_data = [
        [1, 'BTC', 'Bitcoin', 'Crypto'],
        [2, 'ETH', 'Ethereum', 'Crypto'],
        [3, 'NVDA', 'NVIDIA', 'Stock'],
        [4, 'TSLA', 'Tesla', 'Stock']
    ]
    pd.DataFrame(assets_data, columns=['asset_id', 'symbol', 'name', 'asset_type']).to_csv(f'{OUTPUT_DIR}/assets.csv', index=False)

    # 2. Fetch and Clean Price History
    all_prices = []
    
    # Fetch Crypto
    all_prices.append(fetch_crypto_data('bitcoin'))
    all_prices.append(fetch_crypto_data('ethereum'))
    
    # Fetch Stocks
    all_prices.append(fetch_stock_data('NVDA', 3))
    all_prices.append(fetch_stock_data('TSLA', 4))
    
    # Combine and Export Price History CSV
    final_df = pd.concat(all_prices)
    final_df.to_csv(f'{OUTPUT_DIR}/price_history.csv', index=False)
    
    print(f"\nSUCCESS: Data exported to {OUTPUT_DIR}/ folder for Milestone 5 population.")

if __name__ == "__main__":
    main()
