# System Dataflow - Milestone 3

## Overview

This document explains the data lifecycle within the **Crypto & Stock Anomaly Detection System**. Since we are handling high-frequency market data from both Cryptocurrency and Stock markets, we have designed a pipeline that ensures data is cleaned and validated before it enters our MySQL database.

---

## 1. Data Ingestion (Source)

Our data enters the system from two primary external sources:

- **Cryptocurrency Data:** Fetched using the **CoinGecko API** for assets like Bitcoin (BTC) and Ethereum (ETH).
- **Stock Market Data:** Fetched using the **Yahoo Finance (yfinance)** library for stocks like NVIDIA (NVDA) and Tesla (TSLA).

## 2. Preprocessing & Cleaning (Python Layer)

Before reaching the database, all raw API data passes through a Python preprocessing script. We perform the following cleaning steps:

- **Timestamp Standardization:** Converting various API timestamp formats into a uniform `YYYY-MM-DD HH:MM:SS` format for MySQL `DATETIME` compatibility.
- **Handling Nulls:** Removing any incomplete trading intervals where price or volume data might be missing.
- **Normalization:** Ensuring price and volume values are consistently formatted as decimals.

## 3. Storage (Database Layer)

The clean data is then mapped to our normalized tables:

- **`assets`**: Stores the static metadata (Symbol, Name, Type).
- **`price_history`**: Receives the continuous stream of OHLCV (Open, High, Low, Close, Volume) data.
- All price records are linked to their respective assets via the `asset_id` Foreign Key to maintain referential integrity.

## 4. Output & Analysis (What comes out)

After the data is stored in MySQL, the system produces several outputs:

- **Anomaly detection:** Our Python script reads the stored price data from `price_history` and uses the Isolation Forest model to find spikes or drops. The results get saved into the `anomalies` table.
- **Automatic Alerts:** We have a trigger in the database so that as soon as a new anomaly is found, it creates an alert in the `alerts` table.
- **Dashboard Visuals:** Finally, the web dashboard pulls this data to show charts with markers where the anomalies happened.

This flow ensures that we aren't just storing data—but actually making sense of it.
