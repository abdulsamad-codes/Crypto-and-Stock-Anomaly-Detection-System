# How to Run the System

This guide explains how to set up and run the **Crypto & Stock Anomaly Detection System** for local testing or presentation.

## 1. Database Setup

1. Open **MySQL Workbench**.
2. Run the `schema.sql` script to create the database and tables.
3. Import Data using the **Table Data Import Wizard**:
   - Right-click `assets` table -> Table Data Import Wizard -> Select `data_exports/assets.csv`.
   - Right-click `price_history` table -> Table Data Import Wizard -> Select `data_exports/price_history.csv`.
4. (Optional) Run `population.sql` to execute validation queries.

## 2. Python Environment Setup

Install the required libraries on your global environment:

```powershell
pip install flask mysql-connector-python pandas yfinance requests
```

## 3. Configure Database Credentials

Open `dashboard_ui/app.py` and update the `db_config` section with your MySQL password:

```python
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'YOUR_PASSWORD_HERE',
    'database': 'crypto_anomaly_db'
}
```

## 4. Run the Dashboard

1. Open your terminal in the project root.
2. Navigate to the UI folder: `cd dashboard_ui`
3. Start the Flask server: `python app.py`
4. Open your browser and go to: `http://127.0.0.1:5000`

## 5. UI Navigation Features

- **Global Nerve Center:** View real-time market pulse and system stats.
- **Deep Dive Analysis:** Select an asset and click the "Deep Dive" button for technical charting and order book visuals.
- **Live Stream:** Explains the "Agentic Reasoning" behind every detected anomaly.
- **Config:** Control system sensitivity and Z-Score thresholds.

## 6. (Optional) Fetch New Data

To update the CSV files with the latest market prices, run the generator script from the root:

```powershell
python data_generator.py
```
